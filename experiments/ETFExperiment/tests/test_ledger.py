"""Append-only, fsynced, and a truncated line is reported rather than repaired."""

from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path

import pytest

from etf.ledger.append_only import AppendOnlyLedger, LedgerCorruption, LedgerTruncation
from etf.ledger.requests import CapExceeded, RequestLedger, registered_caps_per_day


def test_rows_survive_and_only_ever_grow(tmp_path: Path) -> None:
    ledger = AppendOnlyLedger(tmp_path / "l.jsonl")
    ledger.append({"a": 1})
    ledger.append({"a": 2})
    assert [r["a"] for r in ledger.read().rows] == [1, 2]
    assert ledger.count() == 2


def test_a_trailing_partial_line_is_reported_never_repaired(tmp_path: Path) -> None:
    path = tmp_path / "l.jsonl"
    ledger = AppendOnlyLedger(path)
    ledger.append({"a": 1})
    with path.open("a", encoding="utf-8") as fh:
        fh.write('{"a": 2')
    result = ledger.read()
    assert [r["a"] for r in result.rows] == [1]
    assert result.trailing_partial_line == '{"a": 2'
    with pytest.raises(LedgerTruncation, match="never repaired"):
        ledger.require_intact()


def test_a_corrupt_complete_line_raises_with_its_line_number(tmp_path: Path) -> None:
    path = tmp_path / "l.jsonl"
    ledger = AppendOnlyLedger(path)
    ledger.append({"a": 1})
    with path.open("a", encoding="utf-8") as fh:
        fh.write("not json\n")
    with pytest.raises(LedgerCorruption, match=":2 did not parse"):
        ledger.read()


def test_a_missing_ledger_reads_empty_rather_than_raising(tmp_path: Path) -> None:
    result = AppendOnlyLedger(tmp_path / "absent.jsonl").read()
    assert result.rows == []
    assert result.trailing_partial_line is None


def test_a_row_that_would_span_two_lines_is_refused(tmp_path: Path) -> None:
    ledger = AppendOnlyLedger(tmp_path / "l.jsonl")
    ledger.append({"a": "one\ntwo"})
    assert ledger.count() == 1, "json.dumps escapes the newline, so the row stays on one line"


def test_the_cap_charges_before_sending_and_refuses_at_the_boundary(tmp_path: Path) -> None:
    clock = lambda: datetime(2026, 8, 28, 12, 0, tzinfo=UTC)  # noqa: E731
    ledger = RequestLedger(tmp_path / "r.jsonl", caps_per_day={"flow": 2}, clock=clock)
    ledger.charge("flow", "flow.table")
    ledger.charge("flow", "flow.table")
    assert ledger.spent_on("2026-08-28", "flow") == 2
    with pytest.raises(CapExceeded, match="cap of 2"):
        ledger.charge("flow", "flow.table")


def test_caps_are_per_source_so_one_budget_cannot_exhaust_another(tmp_path: Path) -> None:
    clock = lambda: datetime(2026, 8, 28, 12, 0, tzinfo=UTC)  # noqa: E731
    ledger = RequestLedger(tmp_path / "r.jsonl", caps_per_day={"flow": 1, "venue": 3}, clock=clock)
    ledger.charge("flow", "flow.table")
    with pytest.raises(CapExceeded):
        ledger.charge("flow", "flow.table")
    ledger.charge("venue", "venue.candleSnapshot")
    assert ledger.spent_on("2026-08-28", "venue") == 1


def test_a_settle_row_never_moves_the_cap(tmp_path: Path) -> None:
    clock = lambda: datetime(2026, 8, 28, 12, 0, tzinfo=UTC)  # noqa: E731
    ledger = RequestLedger(tmp_path / "r.jsonl", caps_per_day={"flow": 1}, clock=clock)
    ledger.charge("flow", "flow.table")
    ledger.settle("flow", "flow.table", "http", 200)
    ledger.settle("flow", "flow.table", "http", 200)
    assert ledger.spent_on("2026-08-28", "flow") == 1


def test_the_registered_caps_name_the_three_sources() -> None:
    assert set(registered_caps_per_day()) == {"flow", "archive", "venue"}
