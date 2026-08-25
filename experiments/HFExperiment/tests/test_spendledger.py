"""The spend ledger: restart survival, the rolling window, the stub."""
from pathlib import Path

import pytest

from hfexperiment.gate import Refusal
from hfexperiment.intents import SMART_ROUTE, Intent, Quote
from hfexperiment.spendledger import (
    SpendLedger,
    reconciliation_stub,
)

QUOTE = Quote(bid=99.9, ask=100.1, mid=100.0,
              captured_utc="2026-08-25T02:00:00Z")
INTENT = Intent(
    symbol="SNDK", side="buy", notional_usd=45.0, quantity=0.45,
    quote=QUOTE, account="[paper account ID removed]", route=SMART_ROUTE,
    formation_hash="0b28a5cfda7516fa",
)


def test_records_survive_restart(tmp_path: Path) -> None:
    path = tmp_path / "spend.jsonl"
    first = SpendLedger(path)
    first.record_intent(INTENT, "r1")
    first.record_refusal(
        Refusal(reason="spend_cap_reached", arithmetic="demo"), "SNDK", "r1"
    )
    first.record_would_submit(INTENT, "r1")
    first.record_spend(0.45, "2026-08-25", "commission", "r1")
    reopened = SpendLedger(path)
    kinds = [r["kind"] for r in reopened.read_all()]
    assert kinds == ["intent", "refusal", "would_submit", "spend"]
    assert reopened.rolling_year_spend("2026-08-25") == 0.45


def test_rolling_year_reads_only_the_window(tmp_path: Path) -> None:
    ledger = SpendLedger(tmp_path / "spend.jsonl")
    ledger.record_spend(25.0, "2025-08-10", "too old", "r1")
    ledger.record_spend(60.0, "2026-05-11", "counts", "r1")
    ledger.record_spend(40.01, "2026-08-20", "counts", "r1")
    ledger.record_spend(5.0, "2026-08-26", "future, not yet", "r1")
    assert ledger.rolling_year_spend("2026-08-25") == pytest.approx(100.01)


def test_refusal_record_carries_reason_and_arithmetic(
    tmp_path: Path,
) -> None:
    ledger = SpendLedger(tmp_path / "spend.jsonl")
    record = ledger.record_refusal(
        Refusal(reason="account_not_pinned", arithmetic="x != y"),
        "SNDK",
        "r1",
    )
    assert record["kind"] == "refusal"
    assert record["reason"] == "account_not_pinned"
    assert record["arithmetic"] == "x != y"
    assert ledger.read_all()[-1] == record


def test_reconciliation_stub_records_the_task_with_no_broker_side(
    tmp_path: Path,
) -> None:
    ledger = SpendLedger(tmp_path / "spend.jsonl")
    ledger.record_spend(60.0, "2026-05-11", "demo", "r1")
    ledger.record_spend(40.01, "2026-08-20", "demo", "r1")
    task = reconciliation_stub(ledger, "2026-01-01", "2026-08-25")
    assert task.ledger_total_cents == 10001
    assert task.statement_total_cents is None
    assert task.status == "awaiting_broker_statement"
