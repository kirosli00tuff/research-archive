"""Order intents as pure data. A malformed intent cannot travel.

The path from formation to would-be submission: formation output,
target book, diff against the held book, order intents, gate. This
module builds the intent and refuses at construction when any field is
absent, so the gate never sees a malformed object. The gate then
re-checks the account anyway, because defense against a defect that
builds an Intent directly is the point of having two walls.

The quote step records arrival mid at construction. That mid anchors
the execution measurement. An intent without a captured mid refuses
with its own named reason, mirroring the registered termination
fill_without_arrival_mid in kill.py: the intent layer refuses earlier,
before anything exists that could fill.
"""
from __future__ import annotations

import hashlib
import json
from collections.abc import Mapping, Sequence
from dataclasses import dataclass

SIDES = ("buy", "sell")
SMART_ROUTE = "SMART"
# IBKR accepts fractional quantities to four decimal places.
QUANTITY_DECIMALS = 4


@dataclass(frozen=True)
class Quote:
    """One captured quote. The mid is computed here, never supplied."""

    bid: float
    ask: float
    mid: float
    captured_utc: str


@dataclass(frozen=True)
class Intent:
    """One would-be order, fully formed. Construction is the only
    blessed path. The gate re-checks the account regardless."""

    symbol: str
    side: str
    notional_usd: float
    quantity: float
    quote: Quote
    account: str
    route: str
    formation_hash: str


@dataclass(frozen=True)
class ConstructionRefusal:
    """A refusal at the construction wall, before the gate."""

    reason: str
    arithmetic: str


def capture_quote(
    bid: float, ask: float, captured_utc: str
) -> Quote | ConstructionRefusal:
    """A quote with its arrival mid, or the reason it cannot anchor."""
    if bid <= 0 or ask <= 0:
        return ConstructionRefusal(
            reason="no_arrival_mid",
            arithmetic=f"bid {bid} ask {ask}: a nonpositive side has no "
                       "mid, and a fill without an arrival mid is the "
                       "registered termination fill_without_arrival_mid",
        )
    if ask < bid:
        return ConstructionRefusal(
            reason="no_arrival_mid",
            arithmetic=f"crossed quote bid {bid} > ask {ask} has no "
                       "usable mid",
        )
    if not captured_utc:
        return ConstructionRefusal(
            reason="no_capture_timestamp",
            arithmetic="a quote without its capture timestamp cannot "
                       "anchor the execution measurement",
        )
    return Quote(
        bid=bid, ask=ask, mid=(bid + ask) / 2.0, captured_utc=captured_utc
    )


def construct_intent(
    *,
    symbol: str | None,
    side: str | None,
    notional_usd: float | None,
    quote: Quote | None,
    account: str | None,
    route: str | None,
    formation_hash: str | None,
) -> Intent | ConstructionRefusal:
    """An Intent, or the named refusal. No field may be absent."""
    if not symbol:
        return ConstructionRefusal(
            reason="intent_field_absent",
            arithmetic="symbol is absent",
        )
    if side not in SIDES:
        return ConstructionRefusal(
            reason="intent_field_absent",
            arithmetic=f"side {side!r} is not one of {SIDES}",
        )
    if notional_usd is None or notional_usd <= 0:
        return ConstructionRefusal(
            reason="intent_field_absent",
            arithmetic=f"notional {notional_usd!r} is absent or "
                       "nonpositive",
        )
    if quote is None:
        return ConstructionRefusal(
            reason="no_arrival_mid",
            arithmetic="no quote was captured. The arrival mid anchors "
                       "the execution measurement, and a fill without "
                       "one is the registered termination "
                       "fill_without_arrival_mid. Refused before the "
                       "gate.",
        )
    if not account:
        return ConstructionRefusal(
            reason="intent_field_absent",
            arithmetic="account is absent or empty. An intent must be "
                       "addressed to the pinned account before it can "
                       "travel.",
        )
    if not route:
        return ConstructionRefusal(
            reason="intent_field_absent",
            arithmetic="route is absent",
        )
    if not formation_hash:
        return ConstructionRefusal(
            reason="intent_field_absent",
            arithmetic="formation hash is absent, so the intent cannot "
                       "carry its reproduction check",
        )
    quantity = round(notional_usd / quote.mid, QUANTITY_DECIMALS)
    if quantity <= 0:
        return ConstructionRefusal(
            reason="intent_field_absent",
            arithmetic=f"quantity {quantity} from notional "
                       f"{notional_usd:.2f} at mid {quote.mid:.4f} "
                       "rounds to nothing",
        )
    return Intent(
        symbol=symbol,
        side=side,
        notional_usd=notional_usd,
        quantity=quantity,
        quote=quote,
        account=account,
        route=route,
        formation_hash=formation_hash,
    )


def formation_hash(
    formation_date: str, width: int, ranked_symbols: Sequence[str]
) -> str:
    """A deterministic hash of one formation's identity."""
    payload = json.dumps(
        {
            "formation_date": formation_date,
            "width": width,
            "symbols": list(ranked_symbols),
        },
        sort_keys=True,
        separators=(",", ":"),
    )
    return hashlib.sha256(payload.encode()).hexdigest()[:16]


def diff_books(
    target: Sequence[str], held: Mapping[str, float]
) -> list[tuple[str, str]]:
    """(symbol, side) pairs turning the held book into the target book.

    Buys for target names not held, sells for held names that left.
    Sizing is the gate's business, not the diff's.
    """
    buys = [(s, "buy") for s in target if s not in held]
    sells = [(s, "sell") for s in sorted(held) if s not in target]
    return buys + sells
