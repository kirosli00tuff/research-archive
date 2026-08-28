"""The ledger survives a restart and refuses malformed records."""
from pathlib import Path

from hfexperiment.ledger import Ledger


def test_ledger_survives_restart(tmp_path: Path) -> None:
    path = tmp_path / "ledger" / "orders.jsonl"
    first = Ledger(path)
    first.append({"seq": 1, "action": "priced", "symbol": "TEST"})
    first.append({"seq": 2, "action": "refused", "symbol": "TEST"})
    del first

    reopened = Ledger(path)
    records = reopened.read_all()
    assert [r["seq"] for r in records] == [1, 2]
    reopened.append({"seq": 3, "action": "priced", "symbol": "TEST"})
    assert len(Ledger(path).read_all()) == 3


def test_ledger_is_append_only_in_interface() -> None:
    assert not hasattr(Ledger, "update")
    assert not hasattr(Ledger, "delete")


def test_ledger_empty_when_absent(tmp_path: Path) -> None:
    assert Ledger(tmp_path / "never_written.jsonl").read_all() == []


def test_ledger_serialises_newlines_safely(tmp_path: Path) -> None:
    """An embedded newline must not split a record into two lines."""
    ledger = Ledger(tmp_path / "orders.jsonl")
    ledger.append({"note": "line one\nline two"})
    raw = (tmp_path / "orders.jsonl").read_text()
    assert raw.count("\n") == 1
    assert ledger.read_all() == [{"note": "line one\nline two"}]
