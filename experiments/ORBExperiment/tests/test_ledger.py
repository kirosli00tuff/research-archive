"""Guard 3 — append-only, fsynced. A truncated line is reported, never repaired."""

from __future__ import annotations

from pathlib import Path

import pytest

from orb.ledger import (
    AppendOnlyLedger,
    LedgerError,
    RequestCapExceededError,
    RequestLedger,
    TruncatedLedgerLine,
)


def test_append_is_durable_and_ordered(tmp_path: Path) -> None:
    ledger = AppendOnlyLedger(tmp_path / "l.jsonl")
    ledger.append({"seq": 1})
    ledger.append({"seq": 2})
    rows = ledger.read()
    assert [r["seq"] for r in rows if not isinstance(r, TruncatedLedgerLine)] == [1, 2]


def test_every_row_is_stamped(tmp_path: Path) -> None:
    ledger = AppendOnlyLedger(tmp_path / "l.jsonl")
    ledger.append({"kind": "seal"})
    row = ledger.read()[0]
    assert not isinstance(row, TruncatedLedgerLine)
    assert row["recorded_at"].endswith("Z")


def test_a_truncated_line_is_reported_never_repaired(tmp_path: Path) -> None:
    """The line stays damaged on disk and comes back typed as damaged."""
    path = tmp_path / "l.jsonl"
    ledger = AppendOnlyLedger(path)
    ledger.append({"seq": 1})
    with path.open("a", encoding="utf-8") as fh:
        fh.write('{"seq": 2, "trun')  # a real truncation: no newline, no close brace
    ledger.append({"seq": 3})

    entries = ledger.read()
    damaged = [e for e in entries if isinstance(e, TruncatedLedgerLine)]
    assert len(damaged) == 1, entries
    assert damaged[0].line_number == 2

    # The file is untouched: the damage is still there after reading.
    assert '{"seq": 2, "trun' in path.read_text(encoding="utf-8")
    assert len(ledger.damaged_lines()) == 1


def test_a_damaged_line_becomes_a_recorded_absence(tmp_path: Path) -> None:
    path = tmp_path / "l.jsonl"
    path.write_text("not json\n", encoding="utf-8")
    ledger = AppendOnlyLedger(path)
    damaged = ledger.damaged_lines()
    assert len(damaged) == 1
    absent = damaged[0].as_absent()
    assert absent.reason.value == "truncated_ledger_line"


def test_a_json_array_line_is_damaged_not_a_row(tmp_path: Path) -> None:
    path = tmp_path / "l.jsonl"
    path.write_text("[1, 2, 3]\n", encoding="utf-8")
    assert len(AppendOnlyLedger(path).damaged_lines()) == 1


def test_request_cap_charges_before_sending(tmp_path: Path) -> None:
    """The cap refuses at the boundary, before the caller has sent anything."""
    ledger = RequestLedger(tmp_path / "req.jsonl", {"stooq": 2})
    ledger.charge("stooq", "2026-08-29", "/q/d/l")
    ledger.charge("stooq", "2026-08-29", "/q/d/l")
    assert ledger.spent_today("stooq", "2026-08-29") == 2
    with pytest.raises(RequestCapExceededError, match="already spent"):
        ledger.charge("stooq", "2026-08-29", "/q/d/l")


def test_the_cap_is_per_day(tmp_path: Path) -> None:
    ledger = RequestLedger(tmp_path / "req.jsonl", {"stooq": 1})
    ledger.charge("stooq", "2026-08-29", "/a")
    ledger.charge("stooq", "2026-08-30", "/a")
    assert ledger.spent_today("stooq", "2026-08-29") == 1


def test_an_unregistered_vendor_has_no_cap_and_is_refused(tmp_path: Path) -> None:
    """An unmeasured endpoint is not a licence to send. solattn ADR-021."""
    ledger = RequestLedger(tmp_path / "req.jsonl", {"stooq": 5})
    with pytest.raises(RequestCapExceededError, match="no registered daily cap"):
        ledger.charge("polygon", "2026-08-29", "/v2/aggs")


def test_a_damaged_request_ledger_refuses_to_compute_a_cap(tmp_path: Path) -> None:
    """A cap computed over a damaged ledger is a number nobody can defend."""
    path = tmp_path / "req.jsonl"
    path.write_text("garbage\n", encoding="utf-8")
    ledger = RequestLedger(path, {"stooq": 5})
    with pytest.raises(LedgerError, match="did not parse"):
        ledger.spent_today("stooq", "2026-08-29")
