"""The daily seal attests the day that closed and refuses the open day."""

from __future__ import annotations

from datetime import UTC, date, datetime, timedelta
from pathlib import Path

import pytest

from etf.manifest import (
    SEAL_GRACE_HOURS,
    ManifestUnattested,
    SealMismatch,
    SealRefused,
    read_day,
    seal_day,
)

D = date(2026, 8, 27)
CAPTURES = [
    {"captured_at": "2026-08-27T20:00:00Z", "sha256": "aa"},
    {"captured_at": "2026-08-27T20:20:00Z", "sha256": "bb"},
]
PASS_TIME = datetime(2026, 8, 28, 12, 20, tzinfo=UTC)


def test_the_pass_on_the_next_day_seals_the_day_that_closed(tmp_path: Path) -> None:
    manifest = seal_day(D, CAPTURES, now=PASS_TIME, root=tmp_path)
    assert manifest.day == D
    assert manifest.capture_count == 2
    assert manifest.first_capture_at == "2026-08-27T20:00:00Z"


def test_sealing_the_open_day_is_refused(tmp_path: Path) -> None:
    """The solattn defect this exists to prevent: attesting a partial file."""
    open_day = PASS_TIME.date()
    with pytest.raises(SealRefused, match="has not closed"):
        seal_day(open_day, CAPTURES, now=PASS_TIME, root=tmp_path)


def test_sealing_a_future_day_is_refused(tmp_path: Path) -> None:
    with pytest.raises(SealRefused):
        seal_day(PASS_TIME.date() + timedelta(days=1), CAPTURES, now=PASS_TIME, root=tmp_path)


def test_the_boundary_fixture_sits_exactly_on_the_day_that_just_closed(tmp_path: Path) -> None:
    """One second past midnight, yesterday is sealable and today is not."""
    just_after = datetime(2026, 8, 28, 0, 0, 1, tzinfo=UTC)
    assert seal_day(D, CAPTURES, now=just_after, root=tmp_path).day == D
    with pytest.raises(SealRefused):
        seal_day(date(2026, 8, 28), CAPTURES, now=just_after, root=tmp_path)


def test_a_sealed_day_whose_captures_changed_raises_rather_than_serving(tmp_path: Path) -> None:
    seal_day(D, CAPTURES, now=PASS_TIME, root=tmp_path)
    grown = [*CAPTURES, {"captured_at": "2026-08-27T21:00:00Z", "sha256": "cc"}]
    with pytest.raises(SealMismatch, match="never repaired"):
        read_day(D, grown, now=PASS_TIME, root=tmp_path)


def test_a_sealed_day_that_matches_serves(tmp_path: Path) -> None:
    seal_day(D, CAPTURES, now=PASS_TIME, root=tmp_path)
    assert read_day(D, list(reversed(CAPTURES)), now=PASS_TIME, root=tmp_path)


def test_the_digest_is_order_independent_because_writers_are_not_ordered(tmp_path: Path) -> None:
    a = seal_day(D, CAPTURES, now=PASS_TIME, root=tmp_path)
    b = seal_day(D, list(reversed(CAPTURES)), now=PASS_TIME, root=tmp_path)
    assert a.capture_digest == b.capture_digest


def test_the_open_day_reads_unsealed(tmp_path: Path) -> None:
    today = PASS_TIME.date()
    assert read_day(today, CAPTURES, now=PASS_TIME, root=tmp_path) == CAPTURES


def test_a_closed_day_inside_the_grace_window_reads_unsealed(tmp_path: Path) -> None:
    inside = datetime(2026, 8, 28, SEAL_GRACE_HOURS - 1, tzinfo=UTC)
    assert read_day(D, CAPTURES, now=inside, root=tmp_path) == CAPTURES


def test_a_closed_day_past_the_grace_window_with_no_seal_raises(tmp_path: Path) -> None:
    """A missing attestation is an error, never a pass."""
    past = datetime(2026, 8, 28, SEAL_GRACE_HOURS, 0, 1, tzinfo=UTC)
    with pytest.raises(ManifestUnattested, match="never a pass"):
        read_day(D, CAPTURES, now=past, root=tmp_path)
