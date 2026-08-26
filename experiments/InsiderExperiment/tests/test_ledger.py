"""Append-only ledgers survive restart and are never mutated."""

from __future__ import annotations

from pathlib import Path

import pytest

from insider.ledger.append_only import AppendOnlyLedger, LedgerCorruption


def test_rows_survive_a_new_reader(tmp_path: Path) -> None:
    path = tmp_path / "l.jsonl"
    AppendOnlyLedger(path).append({"a": 1})
    AppendOnlyLedger(path).append({"a": 2})
    assert [r["a"] for r in AppendOnlyLedger(path).iter_rows()] == [1, 2]


def test_a_truncated_final_line_is_reported_not_repaired(tmp_path: Path) -> None:
    path = tmp_path / "l.jsonl"
    ledger = AppendOnlyLedger(path)
    ledger.append({"a": 1})
    with path.open("a", encoding="utf-8") as fh:
        fh.write('{"a": 2')
    result = ledger.read()
    assert [r["a"] for r in result.rows] == [1]
    assert result.trailing_partial_line == '{"a": 2'


def test_a_corrupt_complete_line_raises_rather_than_being_dropped(tmp_path: Path) -> None:
    path = tmp_path / "l.jsonl"
    ledger = AppendOnlyLedger(path)
    ledger.append({"a": 1})
    with path.open("a", encoding="utf-8") as fh:
        fh.write("not json\n")
    with pytest.raises(LedgerCorruption):
        ledger.read()


def test_a_value_carrying_a_newline_still_occupies_one_physical_line(tmp_path: Path) -> None:
    """One row is one line, whatever the row holds.

    A newline inside a value is escaped by the serializer rather than refused,
    so the row round-trips and the line count still equals the row count. The
    one-line assertion inside `append` guards the serializer, not this input.
    """
    path = tmp_path / "l.jsonl"
    ledger = AppendOnlyLedger(path)
    ledger.append({"a": "x\ny"})
    ledger.append({"a": 2})
    assert path.read_text(encoding="utf-8").count("\n") == 2
    assert [r["a"] for r in ledger.iter_rows()] == ["x\ny", 2]


def test_the_ledger_exposes_no_mutation_method(tmp_path: Path) -> None:
    ledger = AppendOnlyLedger(tmp_path / "l.jsonl")
    for forbidden in ("update", "rewrite", "purge", "overwrite"):
        assert not hasattr(ledger, forbidden), f"a ledger must not expose {forbidden}"
