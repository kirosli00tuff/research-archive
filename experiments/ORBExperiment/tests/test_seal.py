"""Guard 5 — the seal. A sealed writer stores bytes and returns no bar value."""

from __future__ import annotations

import hashlib
from pathlib import Path

import pytest

from orb.ledger import AppendOnlyLedger, TruncatedLedgerLine
from orb.seal import (
    PRICED_BAR_FIELDS,
    READABLE_FIELDS,
    SealedWriter,
    SealViolationError,
)


def _writer(tmp_path: Path) -> SealedWriter:
    return SealedWriter(tmp_path / "sealed", AppendOnlyLedger(tmp_path / "l.jsonl"))


def test_the_sealed_writer_stores_bytes_verbatim(tmp_path: Path) -> None:
    payload = b'{"o":1,"h":2,"l":0,"c":1.5,"v":100}\n'
    record = _writer(tmp_path).store("probe/AAPL.json", payload)
    assert record.path.read_bytes() == payload
    assert record.sha256 == hashlib.sha256(payload).hexdigest()
    assert record.byte_count == len(payload)
    assert record.line_count == 1


def test_the_seal_record_carries_counts_and_hashes_never_a_value(
    tmp_path: Path,
) -> None:
    record = _writer(tmp_path).store("probe/AAPL.json", b'{"c":1.5}\n')
    row = record.as_row()
    assert set(row) == {"kind", "path", "sha256", "byte_count", "line_count"}
    assert "1.5" not in str(row)


def test_the_hash_is_recorded_in_the_append_only_ledger(tmp_path: Path) -> None:
    ledger = AppendOnlyLedger(tmp_path / "l.jsonl")
    writer = SealedWriter(tmp_path / "sealed", ledger)
    record = writer.store("probe/AAPL.json", b"x")
    rows = [r for r in ledger.read() if not isinstance(r, TruncatedLedgerLine)]
    assert rows[0]["sha256"] == record.sha256


def test_asking_a_sealed_writer_for_a_value_is_structurally_refused(
    tmp_path: Path,
) -> None:
    with pytest.raises(SealViolationError, match="no bar value"):
        _writer(tmp_path).value("close")


def test_the_forbidden_field_list_covers_every_probed_vendor_dialect() -> None:
    """Polygon's o/h/l/c/v/vw/n, Alpaca's long names, and the quote fields."""
    for field in ("o", "h", "l", "c", "v", "vw", "n"):
        assert field in PRICED_BAR_FIELDS, field
    for field in ("open", "high", "low", "close", "volume", "vwap", "trade_count"):
        assert field in PRICED_BAR_FIELDS, field
    for field in ("bid", "ask", "bid_price", "ask_price"):
        assert field in PRICED_BAR_FIELDS, field


def test_the_readable_list_is_exactly_the_blindness_sections_readable_fields() -> None:
    for field in ("ticker", "exchange", "timestamp", "bar_count", "status_code"):
        assert field in READABLE_FIELDS, field
    assert not READABLE_FIELDS & PRICED_BAR_FIELDS
