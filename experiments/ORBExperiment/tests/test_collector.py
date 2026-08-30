"""The collector: error markers are never no-data, and the open session is never sealed."""

from __future__ import annotations

import hashlib
from datetime import UTC, date, datetime
from pathlib import Path

import pytest

from orb.callstate import HealthState
from orb.collector import (
    SealedOpenSessionError,
    classify,
    diff_against_manifest,
    seal_closed_session,
)
from orb.ledger import AppendOnlyLedger, TruncatedLedgerLine

MARKERS = (b'"Information"', b'"Note"')
NOW = datetime(2026, 8, 29, 22, 15, tzinfo=UTC)


def test_a_429_is_rate_limited_and_never_no_data() -> None:
    assert classify(429, b"", MARKERS) is HealthState.RATE_LIMITED
    assert classify(429, b"slow down", MARKERS) is HealthState.RATE_LIMITED


def test_a_5xx_is_source_failed_and_never_no_data() -> None:
    for code in (500, 502, 503, 504):
        assert classify(code, b"", MARKERS) is HealthState.SOURCE_FAILED


def test_a_transport_failure_is_source_failed() -> None:
    assert classify(0, b"connection reset", MARKERS) is HealthState.SOURCE_FAILED


def test_an_empty_200_is_no_data_not_stored() -> None:
    assert classify(200, b"", MARKERS) is HealthState.NO_DATA
    assert classify(200, b"{}", MARKERS) is HealthState.NO_DATA
    assert classify(200, b"[]", MARKERS) is HealthState.NO_DATA


def test_a_refusal_served_at_http_200_is_source_failed_not_stored() -> None:
    """The measured Alpha Vantage hazard, ADR-008.

    A.1 TASK 1 measured a 200 carrying an Information string and no series, and
    a 2-byte `{}` for the delisted query. A status-code-only classifier records
    `stored` for both and then counts a session with zero bars.
    """
    body = b'{"Information": "The **demo** API key is for demo purposes only."}'
    assert classify(200, body, MARKERS) is HealthState.SOURCE_FAILED
    assert (
        classify(200, b'{"Note": "rate limit"}', MARKERS) is HealthState.SOURCE_FAILED
    )


def test_a_real_payload_is_stored() -> None:
    assert classify(200, b'{"results":[{"t":1}]}', MARKERS) is HealthState.STORED


def test_the_open_session_is_never_sealed(tmp_path: Path) -> None:
    """solattn ADR-019: a seal attests a day that is closed and final."""
    ledger = AppendOnlyLedger(tmp_path / "l.jsonl")
    with pytest.raises(SealedOpenSessionError, match="has not closed"):
        seal_closed_session(ledger, NOW.date(), NOW, {"AAPL": b"x"})
    with pytest.raises(SealedOpenSessionError):
        seal_closed_session(ledger, date(2026, 8, 30), NOW, {"AAPL": b"x"})


def test_a_closed_session_seals_and_records_its_manifest(tmp_path: Path) -> None:
    ledger = AppendOnlyLedger(tmp_path / "l.jsonl")
    manifest = seal_closed_session(
        ledger, date(2026, 8, 28), NOW, {"AAPL": b"x", "MSFT": b"y"}
    )
    rows = [r for r in ledger.read() if not isinstance(r, TruncatedLedgerLine)]
    assert rows[0]["kind"] == "session_seal"
    assert rows[0]["manifest_sha256"] == manifest
    assert rows[0]["bar_files"] == 2


def test_the_manifest_is_order_independent_but_content_sensitive(
    tmp_path: Path,
) -> None:
    ledger = AppendOnlyLedger(tmp_path / "l.jsonl")
    a = seal_closed_session(ledger, date(2026, 8, 28), NOW, {"A": b"1", "B": b"2"})
    b = seal_closed_session(ledger, date(2026, 8, 27), NOW, {"B": b"2", "A": b"1"})
    c = seal_closed_session(ledger, date(2026, 8, 26), NOW, {"A": b"1", "B": b"3"})
    assert a == b
    assert a != c


def test_a_changed_bar_produces_a_revision_row_with_both_hashes() -> None:
    """The MLCryptoEngine H11 hazard, turned into a measurement."""
    before = {"AAPL/2026-08-28": hashlib.sha256(b"v1").hexdigest()}
    after = {"AAPL/2026-08-28": b"v2"}
    rows = diff_against_manifest(
        before, after, "2026-08-28T22:15:00Z", "2026-08-29T22:15:00Z"
    )
    assert len(rows) == 1
    row = rows[0]
    assert row["kind"] == "bar_revision"
    assert row["sha256_before"] == hashlib.sha256(b"v1").hexdigest()
    assert row["sha256_after"] == hashlib.sha256(b"v2").hexdigest()
    assert row["pulled_at_before"] == "2026-08-28T22:15:00Z"
    assert row["pulled_at_after"] == "2026-08-29T22:15:00Z"
    assert row["disappeared"] is False
    assert row["appeared"] is False


def test_an_unchanged_bar_produces_no_row() -> None:
    same = hashlib.sha256(b"v1").hexdigest()
    rows = diff_against_manifest({"k": same}, {"k": b"v1"}, "t0", "t1")
    assert rows == []


def test_a_disappearing_and_an_appearing_bar_are_both_recorded() -> None:
    gone = diff_against_manifest({"k": "abc"}, {}, "t0", "t1")
    assert gone[0]["disappeared"] is True
    assert gone[0]["sha256_after"] is None

    new = diff_against_manifest({}, {"k": b"v"}, "t0", "t1")
    assert new[0]["appeared"] is True
    assert new[0]["sha256_before"] is None
