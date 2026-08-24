"""The order gate, as pure refusal logic. Priced before sending.

Stage C.1 wires this to the spend ledger and the broker. Here it is a
pure function so every refusal condition is testable now, before an
account exists. A refusal names the arithmetic and writes nothing.
Approval returns None and the caller proceeds to price the order.

The gate also refuses while any parameter it needs is still a
DeferredParameter, which is what makes Amendment 1 a precondition of the
first live order rather than a formality.
"""
from __future__ import annotations

from dataclasses import dataclass

from hfexperiment.registered import (
    THRESHOLDS,
    DeferredParameter,
    RegisteredThresholds,
)


@dataclass(frozen=True)
class OrderIntent:
    """What the gate needs to know about one order before it is priced."""

    symbol: str
    side: str  # buy | sell
    notional_usd: float
    is_fractionable: bool
    smart_routed: bool
    formation_reproduced: bool


@dataclass(frozen=True)
class Refusal:
    """One named refusal with its arithmetic spelled out."""

    reason: str
    arithmetic: str


def check_order(
    intent: OrderIntent,
    settled_cash_usd: float,
    spend_last_365d_usd: float,
    broker_min_notional_usd: float | DeferredParameter,
    per_name_notional_usd: float | DeferredParameter,
    thresholds: RegisteredThresholds = THRESHOLDS,
) -> Refusal | None:
    """None to proceed, or the first refusal in registered order.

    Buys need settled cash. Sells liquidate an existing position and the
    cash check does not apply to them.
    """
    if isinstance(per_name_notional_usd, DeferredParameter):
        return Refusal(
            reason="deferred_parameter_unresolved",
            arithmetic=f"{per_name_notional_usd.name} awaits "
                       f"{per_name_notional_usd.amendment}: "
                       f"{per_name_notional_usd.reason}",
        )
    if isinstance(broker_min_notional_usd, DeferredParameter):
        return Refusal(
            reason="deferred_parameter_unresolved",
            arithmetic=f"{broker_min_notional_usd.name} awaits "
                       f"{broker_min_notional_usd.amendment}: "
                       f"{broker_min_notional_usd.reason}",
        )
    if intent.side == "buy" and intent.notional_usd > settled_cash_usd:
        return Refusal(
            reason="insufficient_settled_cash",
            arithmetic=f"notional {intent.notional_usd:.2f} > settled "
                       f"cash {settled_cash_usd:.2f}",
        )
    if intent.notional_usd < broker_min_notional_usd:
        return Refusal(
            reason="below_broker_minimum",
            arithmetic=f"notional {intent.notional_usd:.2f} < broker "
                       f"minimum {broker_min_notional_usd:.2f}",
        )
    if not intent.is_fractionable:
        return Refusal(
            reason="non_fractionable_symbol",
            arithmetic=f"{intent.symbol} is not fractionable and "
                       f"whole-share sizing is closed at this stake",
        )
    if not intent.formation_reproduced:
        return Refusal(
            reason="formation_reproduction_failed",
            arithmetic="the formation feeding this order did not "
                       "reproduce from the price store",
        )
    if spend_last_365d_usd >= thresholds.spend_cap_usd_per_year:
        return Refusal(
            reason="spend_cap_reached",
            arithmetic=f"spend {spend_last_365d_usd:.2f} >= registered "
                       f"cap {thresholds.spend_cap_usd_per_year:.2f} "
                       f"per rolling 365 days",
        )
    if not intent.smart_routed:
        return Refusal(
            reason="not_smart_routed",
            arithmetic="directed API orders forfeit Tiered pricing in "
                       "IBKR's own words, docs/ACCESS.md",
        )
    return None
