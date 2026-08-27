"""Append-only fsynced ledgers and the request cap. Ported guard 3."""

from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path

import pytest

from npl.ledger.append_only import AppendOnlyLedger, LedgerCorruption, LedgerTruncation
from npl.ledger.requests import CapExceeded, RequestLedger


def test_rows_land_one_per_line_and_read_back(tmp_path: Path) -> None:
    ledger = AppendOnlyLedger(tmp_path / "l.jsonl")
    ledger.append({"a": 1})
    ledger.append({"b": 2})
    result = ledger.read()
    assert result.rows == [{"a": 1}, {"b": 2}]
    assert result.trailing_partial_line is None


def test_a_truncated_final_line_is_reported_never_repaired(tmp_path: Path) -> None:
    path = tmp_path / "l.jsonl"
    ledger = AppendOnlyLedger(path)
    ledger.append({"a": 1})
    with path.open("a", encoding="utf-8") as fh:
        fh.write('{"partial": tru')
    result = ledger.read()
    assert result.rows == [{"a": 1}]
    assert result.trailing_partial_line == '{"partial": tru'
    with pytest.raises(LedgerTruncation, match="never repaired"):
        ledger.require_intact()
    # The file was not repaired by reading it.
    assert path.read_text(encoding="utf-8").endswith('{"partial": tru')


def test_a_corrupt_interior_line_raises_rather_than_dropping(tmp_path: Path) -> None:
    path = tmp_path / "l.jsonl"
    path.write_text('{"a": 1}\nnot json\n{"b": 2}\n', encoding="utf-8")
    with pytest.raises(LedgerCorruption, match=":2"):
        AppendOnlyLedger(path).read()


def test_the_ledger_has_no_rewrite_or_delete_api(tmp_path: Path) -> None:
    ledger = AppendOnlyLedger(tmp_path / "l.jsonl")
    public = {name for name in dir(ledger) if not name.startswith("_")}
    assert public == {"append", "count", "iter_rows", "path", "read", "require_intact"}


def _clock_at(iso: str) -> datetime:
    return datetime.fromisoformat(iso).replace(tzinfo=UTC)


def test_the_charge_lands_before_the_cap_and_refuses_past_it(tmp_path: Path) -> None:
    ledger = RequestLedger(
        tmp_path / "req.jsonl", cap_per_day=2, clock=lambda: _clock_at("2026-08-27T10:00:00")
    )
    ledger.charge("info:meta")
    ledger.charge("info:meta")
    with pytest.raises(CapExceeded, match=r"2 charged on 2026-08-27.*cap of 2"):
        ledger.charge("info:meta")
    assert ledger.spent_on("2026-08-27") == 2


def test_the_cap_is_per_utc_day(tmp_path: Path) -> None:
    moments = iter(["2026-08-27T23:59:59", "2026-08-28T00:00:01"])
    ledger = RequestLedger(
        tmp_path / "req.jsonl", cap_per_day=1, clock=lambda: _clock_at(next(moments))
    )
    ledger.charge("info:meta")
    ledger.charge("info:meta")  # a new day, a new budget
    assert ledger.spent_on("2026-08-27") == 1
    assert ledger.spent_on("2026-08-28") == 1


def test_a_settle_row_never_moves_the_cap(tmp_path: Path) -> None:
    ledger = RequestLedger(
        tmp_path / "req.jsonl", cap_per_day=1, clock=lambda: _clock_at("2026-08-27T10:00:00")
    )
    ledger.charge("info:meta")
    ledger.settle("info:meta", "http", 200)
    ledger.settle("info:meta", "http", 429)
    assert ledger.spent_on("2026-08-27") == 1
    with pytest.raises(CapExceeded):
        ledger.charge("info:meta")


def test_the_count_survives_restart(tmp_path: Path) -> None:
    path = tmp_path / "req.jsonl"
    first = RequestLedger(path, cap_per_day=2, clock=lambda: _clock_at("2026-08-27T10:00:00"))
    first.charge("info:meta")
    second = RequestLedger(path, cap_per_day=2, clock=lambda: _clock_at("2026-08-27T11:00:00"))
    assert second.spent_on("2026-08-27") == 1
    second.charge("info:meta")
    with pytest.raises(CapExceeded):
        second.charge("info:meta")


def test_a_truncated_request_ledger_refuses_to_start(tmp_path: Path) -> None:
    path = tmp_path / "req.jsonl"
    path.write_text('{"day":"2026-08-27","endpoint":"e","kind":"charge","ts":"t"}\n{"par', "utf-8")
    with pytest.raises(LedgerTruncation):
        RequestLedger(path, cap_per_day=2, clock=lambda: _clock_at("2026-08-27T10:00:00"))
