"""Resolving the at-the-money 30-day MBT straddle from a listed chain.

VRPExperiment Sections 4.1 and 4.2 register **what** must be sampled: the ATM
series at the 30-day tenor. They leave two questions to an implementer, and each
is a place where a quiet wrong answer produces a valid-looking straddle either
way. Both are fixed here and registered in REGISTRATION.md Section 3.2 and 3.3,
before any chain was enumerated.

**The at-the-money strike.** The listed strike minimising the absolute distance
from the reference price. The reference price is the **midpoint of the MBT front
future's touch**, not an index level and not the option's own underlying field,
because the straddle is delta-hedged with that future: a strike chosen against
any other reference is not delta-neutral against the instrument that hedges it.
At a tie the **lower** strike is taken. Two equidistant strikes are equally
at-the-money, so the choice between them is arbitrary by construction. What
matters is that it is fixed before any chain is enumerated, so it cannot be made
after seeing which of the two quotes tighter.

**The 30-day tenor.** The listed expiry minimising the absolute distance from 30
days, measured from the observation instant to the expiry's **settlement
instant**, not to midnight. At a tie the **longer** tenor is taken. The
registered hedging rule evaluates delta once per calendar day over a 30-day
tenor, and the rebalance counts carried from VRPExperiment (median 11, p90 16,
n = 1,955 paths) were measured over exactly that path. A tenor shorter than 30
days truncates the path and offers fewer evaluation points than the rule those
counts came from, so at a tie the longer tenor is the one the registered path
fits inside.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import final

from mbt.absence import AbsenceReason, Absent, Maybe
from mbt.clock import require_utc
from mbt.quotes import Quote, screen
from mbt.registry import TENOR_TARGET_DAYS

SECONDS_PER_DAY = 86_400.0


@final
@dataclass(frozen=True, slots=True)
class ListedExpiry:
    """One listed expiry, with the settlement instant that defines its tenor."""

    label: str
    settlement: datetime
    exchange: str
    settlement_rule: str

    def __post_init__(self) -> None:
        require_utc(self.settlement, f"ListedExpiry({self.label}).settlement")
        if not self.exchange.strip():
            raise ValueError("ListedExpiry refuses an empty exchange")
        if not self.settlement_rule.strip():
            raise ValueError("ListedExpiry refuses an empty settlement_rule")

    def days_to_expiry(self, at: datetime) -> float:
        """Days from ``at`` to settlement, as a float. May be negative."""
        require_utc(at, "ListedExpiry.days_to_expiry(at)")
        return (self.settlement - at).total_seconds() / SECONDS_PER_DAY

    def as_row(self) -> dict[str, str]:
        return {
            "label": self.label,
            "settlement": self.settlement.isoformat(timespec="milliseconds").replace("+00:00", "Z"),
            "exchange": self.exchange,
            "settlement_rule": self.settlement_rule,
        }


@final
@dataclass(frozen=True, slots=True)
class StraddleSelection:
    """The resolved straddle, with the reference it was resolved against."""

    expiry: ListedExpiry
    strike: float
    reference_price: float
    days_to_expiry: float
    strikes_listed: int
    expiries_listed: int
    tenor_tie_broken: bool
    strike_tie_broken: bool

    def as_row(self) -> dict[str, object]:
        return {
            "expiry": self.expiry.as_row(),
            "strike": self.strike,
            "reference_price": self.reference_price,
            "days_to_expiry": self.days_to_expiry,
            "strikes_listed": self.strikes_listed,
            "expiries_listed": self.expiries_listed,
            "tenor_tie_broken": self.tenor_tie_broken,
            "strike_tie_broken": self.strike_tie_broken,
        }


def reference_price(future_quote: Quote) -> Maybe[float]:
    """The MBT front future's touch midpoint, or the screening refusal."""
    screened = screen(future_quote)
    if isinstance(screened, Absent):
        return screened
    return screened.mid


def select_expiry(
    expiries: list[ListedExpiry], at: datetime, *, target_days: float = TENOR_TARGET_DAYS
) -> Maybe[tuple[ListedExpiry, bool]]:
    """The listed expiry nearest the target tenor. Ties go to the longer tenor.

    Returns the expiry and whether a tie was broken, so the artifact records that
    the rule was exercised rather than merely present.
    """
    require_utc(at, "select_expiry(at)")
    future = [e for e in expiries if e.days_to_expiry(at) > 0.0]
    if not future:
        return Absent(
            AbsenceReason.NOT_SERVED,
            f"no listed expiry sits in the future at {at.isoformat()}: "
            f"{len(expiries)} enumerated, 0 unexpired. A chain with no live expiry "
            "resolves to no straddle, and is never rounded onto an expired series.",
        )
    best = min(future, key=lambda e: abs(e.days_to_expiry(at) - target_days))
    best_distance = abs(best.days_to_expiry(at) - target_days)
    tied = [
        e for e in future if abs(abs(e.days_to_expiry(at) - target_days) - best_distance) < 1e-9
    ]
    if len(tied) > 1:
        # Registered tie rule: the LONGER tenor, because the registered daily
        # hedging path is 30 days and the shorter side truncates it.
        return max(tied, key=lambda e: e.days_to_expiry(at)), True
    return best, False


def select_atm_strike(strikes: list[float], reference: float) -> Maybe[tuple[float, bool]]:
    """The listed strike nearest the reference. Ties go to the LOWER strike."""
    if not strikes:
        return Absent(
            AbsenceReason.NOT_SERVED,
            "no strikes listed at the selected expiry. An empty strike list is "
            "never interpolated onto a synthetic strike.",
        )
    if reference <= 0:
        return Absent(
            AbsenceReason.NOT_SERVED,
            f"reference price {reference} is not positive, so no strike is "
            "at-the-money against it.",
        )
    best_distance = min(abs(strike - reference) for strike in strikes)
    tied = [s for s in strikes if abs(abs(s - reference) - best_distance) < 1e-9]
    if len(tied) > 1:
        # Registered tie rule: the LOWER strike. Two equidistant strikes are
        # equally at-the-money; fixing the choice beforehand is the point.
        return min(tied), True
    return tied[0], False


def resolve_straddle(
    expiries: list[ListedExpiry],
    strikes: list[float],
    future_quote: Quote,
    at: datetime,
) -> Maybe[StraddleSelection]:
    """Resolve the ATM 30-day straddle under both registered rules."""
    reference = reference_price(future_quote)
    if isinstance(reference, Absent):
        return reference

    expiry_choice = select_expiry(expiries, at)
    if isinstance(expiry_choice, Absent):
        return expiry_choice
    expiry, tenor_tie = expiry_choice

    strike_choice = select_atm_strike(strikes, reference)
    if isinstance(strike_choice, Absent):
        return strike_choice
    strike, strike_tie = strike_choice

    return StraddleSelection(
        expiry=expiry,
        strike=strike,
        reference_price=reference,
        days_to_expiry=expiry.days_to_expiry(at),
        strikes_listed=len(strikes),
        expiries_listed=len(expiries),
        tenor_tie_broken=tenor_tie,
        strike_tie_broken=strike_tie,
    )
