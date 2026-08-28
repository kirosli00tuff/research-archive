"""The spend ledger. Append-only, restart-surviving, the only source.

Every intent, every refusal with its reason and arithmetic, every
would-be submission: one record each, through the A.1 Ledger primitive,
fsynced per append, never mutated. The rolling-year spend query reads
only this ledger, which is what makes the registered 100 USD cap
enforceable without trusting a broker screen.

The reconciliation stub records the task D.1 must run, ledger totals
against the broker statement, to the cent. No broker call exists
behind it yet and the statement side is recorded absent, never
estimated.
"""
from __future__ import annotations

import datetime
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from hfexperiment.gate import Refusal
from hfexperiment.intents import ConstructionRefusal, Intent
from hfexperiment.ledger import Ledger

# The real spend ledger. Created on first real use, D.1 at the
# earliest. Demonstrations write to their own file, never this one.
SPEND_LEDGER_PATH = Path("data/ledger/spend.jsonl")

ROLLING_WINDOW_DAYS = 365


def _intent_record(intent: Intent) -> dict[str, Any]:
    record = asdict(intent)
    record["quote"] = asdict(intent.quote)
    return record


class SpendLedger:
    """One append-only JSONL file of intents, refusals, and spend."""

    def __init__(self, path: str | Path) -> None:
        self._ledger = Ledger(path)

    @property
    def path(self) -> Path:
        return self._ledger.path

    def record_intent(self, intent: Intent, run_utc: str) -> None:
        self._ledger.append(
            {"kind": "intent", "intent": _intent_record(intent),
             "run_utc": run_utc}
        )

    def record_refusal(
        self,
        refusal: Refusal | ConstructionRefusal,
        subject: str,
        run_utc: str,
    ) -> dict[str, Any]:
        """The refusal record. The only thing a refusal ever writes."""
        record = {
            "kind": "refusal",
            "subject": subject,
            "reason": refusal.reason,
            "arithmetic": refusal.arithmetic,
            "run_utc": run_utc,
        }
        self._ledger.append(record)
        return record

    def record_would_submit(self, intent: Intent, run_utc: str) -> None:
        """A priced-and-ready intent, recorded, submitted nowhere."""
        self._ledger.append(
            {"kind": "would_submit", "intent": _intent_record(intent),
             "run_utc": run_utc}
        )

    def record_spend(
        self, spend_usd: float, date: str, description: str, run_utc: str
    ) -> None:
        """One realized commission or fee. D.1 writes these from fills."""
        self._ledger.append(
            {"kind": "spend", "spend_usd": spend_usd, "date": date,
             "description": description, "run_utc": run_utc}
        )

    def rolling_year_spend(self, asof_date: str) -> float:
        """Total spend in the 365 days ending at asof_date, inclusive.

        Reads only this ledger. No broker screen enters the cap.
        """
        cutoff = (
            datetime.date.fromisoformat(asof_date)
            - datetime.timedelta(days=ROLLING_WINDOW_DAYS)
        ).isoformat()
        return sum(
            float(r["spend_usd"])
            for r in self._ledger.read_all()
            if r["kind"] == "spend" and cutoff < r["date"] <= asof_date
        )

    def read_all(self) -> list[dict[str, Any]]:
        return self._ledger.read_all()


@dataclass(frozen=True)
class ReconciliationTask:
    """The registered shape of D.1's reconciliation. Ledger totals
    against the broker statement, to the cent. The statement side is
    absent until a real statement exists, never estimated."""

    period_start: str
    period_end: str
    ledger_total_cents: int
    statement_total_cents: int | None
    status: str


def reconciliation_stub(
    ledger: SpendLedger, period_start: str, period_end: str
) -> ReconciliationTask:
    """What D.1 will run. No broker call exists behind this yet."""
    total = sum(
        float(r["spend_usd"])
        for r in ledger.read_all()
        if r["kind"] == "spend" and period_start <= r["date"] <= period_end
    )
    return ReconciliationTask(
        period_start=period_start,
        period_end=period_end,
        ledger_total_cents=round(total * 100),
        statement_total_cents=None,
        status="awaiting_broker_statement",
    )
