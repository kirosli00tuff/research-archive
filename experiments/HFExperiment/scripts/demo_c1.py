#!/usr/bin/env python
"""Stage C.1's demonstration. Every refusal produced, nothing armed.

Runs the full pipeline on the real 2026-08-03 formation at width 20,
against the mock broker, and produces every registered refusal plus
the four-way account pin, the construction wall, the priced-and-ready
intent stopped at Amendment 1, the reconciliation stub, and the
connectivity probe result. Evidence lands in
reports/stage_c1/refusals.md with the demonstration ledgers beside it.

The demonstration ledgers are evidence artifacts regenerated per run.
The real spend ledger at data/ledger/spend.jsonl is never touched by
this script. No order of any kind leaves this process.
"""
from __future__ import annotations

import dataclasses
import datetime
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

from hfexperiment.barstore import BarStore  # noqa: E402
from hfexperiment.brokerconfig import (  # noqa: E402
    DECLARED_MODE,
    load_broker_env,
)
from hfexperiment.gate import Refusal  # noqa: E402
from hfexperiment.gatewire import (  # noqa: E402
    GateInputs,
    PricedReady,
    evaluate,
)
from hfexperiment.ibkrprobe import probe  # noqa: E402
from hfexperiment.intents import (  # noqa: E402
    SMART_ROUTE,
    ConstructionRefusal,
    Intent,
    Quote,
    construct_intent,
    diff_books,
    formation_hash,
)
from hfexperiment.mockbroker import MockBroker  # noqa: E402
from hfexperiment.spendledger import (  # noqa: E402
    SpendLedger,
    reconciliation_stub,
)

FORMATION_JSON = ROOT / "reports" / "stage_c1" / "formation_2026-08-03.json"
C1_STORE = ROOT / "data" / "c1_formation.db"
DEMO_LEDGER = ROOT / "reports" / "stage_c1" / "demo_ledger.jsonl"
DEMO_SPEND_LEDGER = (
    ROOT / "reports" / "stage_c1" / "demo_spend_ledger.jsonl"
)
OUT = ROOT / "reports" / "stage_c1" / "refusals.md"

# The A.2 measured book median spread, 12.77 bp, halves onto each side.
HALF_SPREAD = 0.001277 / 2.0
# Demonstration constants, labelled DEMO everywhere they appear: the
# registered per-name notional is DEFERRED to Amendment 1 and these
# resolve nothing.
DEMO_NOTIONAL = 45.00
DEMO_BROKER_MIN = 1.00
DEMO_PER_NAME = 45.00

lines: list[str] = []


def emit(text: str = "") -> None:
    lines.append(text)


def emit_record(record: dict[str, Any]) -> None:
    emit("```json")
    emit(json.dumps(record, indent=1, sort_keys=True))
    emit("```")


def emit_refusal(refusal: Refusal | ConstructionRefusal) -> None:
    emit(f"Refusal produced: `{refusal.reason}`")
    emit()
    emit(f"Arithmetic: {refusal.arithmetic}")
    emit()


def main() -> int:
    data = json.loads(FORMATION_JSON.read_text(encoding="utf-8"))
    book: list[str] = data["books"]["20"]
    closes: dict[str, float] = data["width20_entry_closes"]
    env = load_broker_env(ROOT / ".env")
    now = datetime.datetime.now(datetime.UTC)
    now_utc = now.strftime("%Y-%m-%dT%H:%M:%SZ")
    today = now.strftime("%Y-%m-%d")

    store = BarStore(C1_STORE)
    store_book = store.formation_books("2026-08-03")[20]
    store.close()
    reproduced = formation_hash("2026-08-03", 20, store_book)
    fhash = formation_hash("2026-08-03", 20, book)

    broker = MockBroker(
        settled_cash_usd=1000.0,
        quotes={
            s: (c * (1 - HALF_SPREAD), c * (1 + HALF_SPREAD))
            for s, c in closes.items()
        },
        fractionable=dict.fromkeys(book, True),
        managed_accounts=[env.account_id],
        now_utc=now_utc,
    )
    for path in (DEMO_LEDGER, DEMO_SPEND_LEDGER):
        if path.exists():
            path.unlink()
    ledger = SpendLedger(DEMO_LEDGER)

    def build(
        symbol: str,
        account: str | None = None,
        route: str = SMART_ROUTE,
        notional: float = DEMO_NOTIONAL,
        fh: str | None = None,
    ) -> Intent:
        quote = broker.quote(symbol)
        assert isinstance(quote, Quote), quote
        intent = construct_intent(
            symbol=symbol,
            side="buy",
            notional_usd=notional,
            quote=quote,
            account=env.account_id if account is None else account,
            route=route,
            formation_hash=fhash if fh is None else fh,
        )
        assert isinstance(intent, Intent), intent
        return intent

    registered = GateInputs(
        settled_cash_usd=broker.settled_cash_usd(),
        spend_last_365d_usd=ledger.rolling_year_spend(today),
        fractionable=broker.fractionable_snapshot(),
        reproduced_hash=reproduced,
        pinned_account=env.account_id,
        mode=DECLARED_MODE,
    )

    def demo_inputs(**overrides: Any) -> GateInputs:
        return dataclasses.replace(
            registered,
            broker_min_notional_usd=DEMO_BROKER_MIN,
            per_name_notional_usd=DEMO_PER_NAME,
            **overrides,
        )

    emit("# Stage C.1: the refusals, produced")
    emit()
    emit(f"Generated {now_utc}. Mode {DECLARED_MODE}, pinned account "
         f"{env.account_id}, route {SMART_ROUTE}.")
    emit()
    emit("Formation: the real 2026-08-03 width-20 book, computed fresh "
         "through the registered rule into C.1's own store, because "
         "the B.1 store records formations only from the 2026-09-01 "
         "series start. Quotes: mock, entry close plus and minus half "
         "the A.2 measured 12.77 bp median spread. Demo notional 45.00 "
         "USD, the A.2 GO candidate, labelled DEMO because the "
         "registered per-name notional stays DEFERRED. Refusals 1, 2, "
         "5 and 6 run under demonstration-resolved parameters (broker "
         "minimum 1.00 DEMO, per-name 45.00 DEMO) so each check is "
         "reachable. Nothing here resolves Amendment 1.")
    emit()
    emit(f"Book: {', '.join(book)}")
    emit()
    diff = diff_books(book, held={})
    emit(f"Held book empty, diff produces {len(diff)} buy intents. "
         f"Formation hash {fhash}, reproduced hash {reproduced}, "
         f"match: {fhash == reproduced}.")
    emit()

    # -- Refusal 7, the steady state -------------------------------
    emit("## Refusal 7: deferred_parameter_unresolved, the steady state")
    emit()
    emit("Condition: the registered inputs as they stand today. "
         "Amendment 1 has not landed, per_name_notional_usd has no "
         "value, and the gate refuses the entire book.")
    emit()
    refused = 0
    first_record: dict[str, Any] | None = None
    for symbol, _side in diff:
        intent = build(symbol)
        ledger.record_intent(intent, now_utc)
        outcome = evaluate(intent, registered)
        assert isinstance(outcome, Refusal), outcome
        record = ledger.record_refusal(outcome, symbol, now_utc)
        refused += 1
        if first_record is None:
            first_record = record
            emit_refusal(outcome)
    emit(f"All {refused} of {len(diff)} intents refused. The first "
         "ledger record written:")
    emit()
    assert first_record is not None
    emit_record(first_record)
    emit()

    # -- Refusals 1 through 6 --------------------------------------
    demos: list[tuple[str, str, Intent, GateInputs]] = [
        (
            "Refusal 1: insufficient_settled_cash",
            "Condition constructed: settled cash 30.00 USD against a "
            "45.00 USD buy of SNDK, parameters DEMO-resolved.",
            build("SNDK"),
            demo_inputs(settled_cash_usd=30.0),
        ),
        (
            "Refusal 2: below_broker_minimum",
            "Condition constructed: a 0.50 USD intent against the DEMO "
            "broker minimum of 1.00 USD.",
            build("AXTI", notional=0.50),
            demo_inputs(),
        ),
        (
            "Refusal 3: non_fractionable_symbol",
            "Condition constructed: the eligibility snapshot marks WOLF "
            "not fractionable. Absence fails closed.",
            build("WOLF"),
            demo_inputs(
                fractionable={**broker.fractionable_snapshot(),
                              "WOLF": False}
            ),
        ),
        (
            "Refusal 4: formation_reproduction_failed",
            "Condition constructed: the intent carries formation hash "
            "0000deadbeef0000 while the store reproduces "
            f"{reproduced}.",
            build("MU", fh="0000deadbeef0000"),
            demo_inputs(),
        ),
        (
            "Refusal 6: not_smart_routed",
            "Condition constructed: route DIRECTED:ARCA. Directed API "
            "orders forfeit Tiered pricing in IBKR's own words.",
            build("WDC", route="DIRECTED:ARCA"),
            demo_inputs(),
        ),
    ]
    for title, condition, intent, inputs in demos:
        emit(f"## {title}")
        emit()
        emit(condition)
        emit()
        outcome = evaluate(intent, inputs)
        assert isinstance(outcome, Refusal), (title, outcome)
        record = ledger.record_refusal(outcome, intent.symbol, now_utc)
        emit_refusal(outcome)
        emit("Ledger record written:")
        emit()
        emit_record(record)
        emit()

    # -- Refusal 5, driven by the spend ledger ---------------------
    emit("## Refusal 5: spend_cap_reached")
    emit()
    emit("Condition constructed: a demonstration spend ledger seeded "
         "with 60.00 USD on 2026-05-11 and 40.01 USD on 2026-08-20, "
         "plus 25.00 USD on 2025-08-10 which sits outside the rolling "
         "365 days and must not count. The rolling-year query reads "
         "only the ledger.")
    emit()
    spend_ledger = SpendLedger(DEMO_SPEND_LEDGER)
    spend_ledger.record_spend(25.00, "2025-08-10", "outside window",
                              now_utc)
    spend_ledger.record_spend(60.00, "2026-05-11", "demo commissions",
                              now_utc)
    spend_ledger.record_spend(40.01, "2026-08-20", "demo commissions",
                              now_utc)
    rolling = spend_ledger.rolling_year_spend(today)
    emit(f"rolling_year_spend({today}) = {rolling:.2f} USD, the "
         "2025-08-10 record excluded.")
    emit()
    intent = build("BE")
    outcome = evaluate(intent, demo_inputs(spend_last_365d_usd=rolling))
    assert isinstance(outcome, Refusal), outcome
    record = ledger.record_refusal(outcome, "BE", now_utc)
    emit_refusal(outcome)
    emit("Ledger record written:")
    emit()
    emit_record(record)
    emit()

    # -- Refusal 8, four ways --------------------------------------
    emit("## Refusal 8: the account pin, four ways")
    emit()
    emit("The gate checks the pin before everything, including the "
         "deferred parameters, so a mis-addressed intent never reaches "
         "pricing. The four cases below build Intent objects directly, "
         "simulating a defect that skips construct_intent, and the "
         "gate refuses anyway. The construction wall is shown after.")
    emit()
    good = build("LITE")
    pin_cases: list[tuple[str, Intent, GateInputs]] = [
        ("Absent field",
         dataclasses.replace(good, account=None),  # type: ignore[arg-type]
         registered),
        ("Empty field", dataclasses.replace(good, account=""), registered),
        ("Wrong account", dataclasses.replace(good, account="DU9999999"),
         registered),
        ("Right account under wrong mode", good,
         dataclasses.replace(registered, mode="live")),
    ]
    for label, pinned_intent, inputs in pin_cases:
        emit(f"### {label}")
        emit()
        outcome = evaluate(pinned_intent, inputs)
        assert isinstance(outcome, Refusal), (label, outcome)
        record = ledger.record_refusal(outcome, "LITE", now_utc)
        emit_refusal(outcome)
        emit("Ledger record written:")
        emit()
        emit_record(record)
        emit()

    # -- The construction wall -------------------------------------
    emit("## The construction wall, before the gate")
    emit()
    quote = broker.quote("LITE")
    assert isinstance(quote, Quote)
    wall = [
        ("Absent account", construct_intent(
            symbol="LITE", side="buy", notional_usd=DEMO_NOTIONAL,
            quote=quote, account=None, route=SMART_ROUTE,
            formation_hash=fhash)),
        ("Empty account", construct_intent(
            symbol="LITE", side="buy", notional_usd=DEMO_NOTIONAL,
            quote=quote, account="", route=SMART_ROUTE,
            formation_hash=fhash)),
        ("No captured quote, the arrival-mid mirror", construct_intent(
            symbol="LITE", side="buy", notional_usd=DEMO_NOTIONAL,
            quote=None, account=env.account_id, route=SMART_ROUTE,
            formation_hash=fhash)),
    ]
    for label, result in wall:
        emit(f"### {label}")
        emit()
        assert isinstance(result, ConstructionRefusal), (label, result)
        record = ledger.record_refusal(result, "LITE", now_utc)
        emit_refusal(result)
        emit("Ledger record written:")
        emit()
        emit_record(record)
        emit()

    # -- Priced-and-ready, stopped at Amendment 1 ------------------
    emit("## Priced-and-ready, stopped exactly at Amendment 1")
    emit()
    ready_intent = build("SNDK")
    ready = evaluate(ready_intent, demo_inputs())
    assert isinstance(ready, PricedReady), ready
    ledger.record_would_submit(ready_intent, now_utc)
    emit("Under DEMO-resolved parameters the same intent passes every "
         "check and reaches priced-and-ready. It is recorded as a "
         "would-be submission and submitted nowhere:")
    emit()
    emit(f"symbol {ready_intent.symbol}, side {ready_intent.side}, "
         f"notional {ready_intent.notional_usd:.2f}, quantity "
         f"{ready_intent.quantity}, mid {ready_intent.quote.mid:.4f} "
         f"captured {ready_intent.quote.captured_utc}, account "
         f"{ready_intent.account}, route {ready_intent.route}, "
         f"settled cash after {ready.settled_cash_after_usd:.2f}")
    emit()
    stopped = evaluate(ready_intent, registered)
    assert isinstance(stopped, Refusal), stopped
    record = ledger.record_refusal(stopped, "SNDK", now_utc)
    emit("Under the registered inputs the identical intent stops at "
         "the deferred parameter, which is exactly where D.1 begins:")
    emit()
    emit_refusal(stopped)
    emit("Ledger record written:")
    emit()
    emit_record(record)
    emit()

    # -- The reconciliation stub -----------------------------------
    emit("## The reconciliation stub, D.1's registered task shape")
    emit()
    task = reconciliation_stub(spend_ledger, "2026-01-01", today)
    emit_record(dataclasses.asdict(task))
    emit()

    # -- The connectivity probe ------------------------------------
    emit("## The connectivity probe, read-only twice over")
    emit()
    emit(f"Declared mode {DECLARED_MODE}, .env port {env.port}, host "
         f"{env.host}, pinned {env.account_id}.")
    emit()
    result = probe(env)
    emit_record(dataclasses.asdict(result))
    emit()

    counts: dict[str, int] = {}
    for r in ledger.read_all():
        counts[r["kind"]] = counts.get(r["kind"], 0) + 1
    emit("## The demonstration ledger, counted")
    emit()
    emit(f"{counts} in {DEMO_LEDGER.name}, plus "
         f"{len(spend_ledger.read_all())} spend records in "
         f"{DEMO_SPEND_LEDGER.name}. Append-only, fsynced, one record "
         "per event.")
    OUT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"wrote {OUT}")
    print(f"probe: {result.state}: {result.detail}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
