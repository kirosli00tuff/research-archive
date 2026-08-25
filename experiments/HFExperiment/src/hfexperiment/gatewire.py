"""The gate, wired. Eight refusals producible, nothing armed.

gate.py holds the A.2 pure logic for refusals 1 through 7. This module
adds refusal 8, account pinning, and runs it FIRST: an intent addressed
anywhere but the pinned account must never reach pricing, because the
Gateway session runs on the operator's full-access login and can see
accounts holding money that is not this project's (ADR-018).

Within gate.check_order the registered order stands: the deferred
parameters refuse before anything else, which is the gate's current
steady state. Amendment 1 has not landed, per-name notional has no
registered value, so every intent is refused at 7. D.1 begins exactly
where PricedReady stops.

Everything here is pure. The ledger writes happen in spendledger.py
and every refusal writes nothing except its own refusal record.
"""
from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass

from hfexperiment import gate
from hfexperiment.brokerconfig import pin_account
from hfexperiment.intents import SMART_ROUTE, Intent
from hfexperiment.registered import (
    BROKER_MIN_NOTIONAL_USD,
    PER_NAME_NOTIONAL_USD,
    DeferredParameter,
)


@dataclass(frozen=True)
class GateInputs:
    """Everything the wired gate reads. The registered deferred
    parameters are the defaults on purpose: resolving them here is
    Amendment 1's job, and a demonstration that resolves them must say
    so in its own record."""

    settled_cash_usd: float
    spend_last_365d_usd: float
    fractionable: Mapping[str, bool]
    reproduced_hash: str | None
    pinned_account: str
    mode: str
    broker_min_notional_usd: float | DeferredParameter = (
        BROKER_MIN_NOTIONAL_USD
    )
    per_name_notional_usd: float | DeferredParameter = PER_NAME_NOTIONAL_USD


@dataclass(frozen=True)
class PricedReady:
    """The terminal object of C.1's pipeline. D.1 begins here. Nothing
    in this stage submits it anywhere."""

    intent: Intent
    settled_cash_after_usd: float


def evaluate(intent: Intent, inputs: GateInputs) -> gate.Refusal | PricedReady:
    """One intent through the pin and the gate, in that order."""
    refusal = pin_account(
        getattr(intent, "account", None), inputs.pinned_account, inputs.mode
    )
    if refusal is not None:
        return refusal
    gate_intent = gate.OrderIntent(
        symbol=intent.symbol,
        side=intent.side,
        notional_usd=intent.notional_usd,
        is_fractionable=inputs.fractionable.get(intent.symbol, False),
        smart_routed=intent.route == SMART_ROUTE,
        formation_reproduced=(
            inputs.reproduced_hash is not None
            and inputs.reproduced_hash == intent.formation_hash
        ),
    )
    refusal = gate.check_order(
        gate_intent,
        settled_cash_usd=inputs.settled_cash_usd,
        spend_last_365d_usd=inputs.spend_last_365d_usd,
        broker_min_notional_usd=inputs.broker_min_notional_usd,
        per_name_notional_usd=inputs.per_name_notional_usd,
    )
    if refusal is not None:
        return refusal
    after = inputs.settled_cash_usd - (
        intent.notional_usd if intent.side == "buy" else 0.0
    )
    return PricedReady(intent=intent, settled_cash_after_usd=after)
