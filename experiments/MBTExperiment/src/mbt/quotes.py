"""One quoted leg, and the registered conditions under which it is refused.

Five refusal conditions are registered in REGISTRATION.md Section 3.4 and
implemented here, each returning a typed :class:`Absent` carrying its reason
rather than a number:

============== ==========================================================
unquoted leg   bid or ask absent at the observation instant
crossed book   bid strictly above ask: a broken book, not a zero spread
zero bid       bid at or below zero: not a price
stale stamp    venue stamp trails local capture beyond the tolerance
delayed/frozen the feed served anything other than a real-time tick
============== ==========================================================

The order of the checks is registered and is not incidental. **Structure is
checked before staleness, and staleness before delay.** A crossed book on a
delayed feed is reported as crossed, because the book being broken is the more
specific fact and the one a reader needs first. Reporting it as merely delayed
would hide that the venue served something impossible.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import final

from mbt.absence import AbsenceReason, Absent, Maybe
from mbt.clock import ObservationClock
from mbt.figures import TickDelayStatus


@final
@dataclass(frozen=True, slots=True)
class Quote:
    """One leg's touch at one instant, with both clocks and the feed status."""

    leg: str
    bid: float | None
    ask: float | None
    clock: ObservationClock
    tick_delay: TickDelayStatus
    subscription_note: str = ""

    @property
    def spread(self) -> float:
        """Ask less bid. Only meaningful after :func:`screen` accepts the quote."""
        if self.bid is None or self.ask is None:
            raise ValueError(f"{self.leg}: spread requires both sides; screen the quote first")
        return self.ask - self.bid

    @property
    def mid(self) -> float:
        """The touch midpoint. Only meaningful after :func:`screen` accepts."""
        if self.bid is None or self.ask is None:
            raise ValueError(f"{self.leg}: mid requires both sides; screen the quote first")
        return (self.bid + self.ask) / 2.0

    def as_row(self) -> dict[str, object]:
        return {
            "leg": self.leg,
            "bid": self.bid,
            "ask": self.ask,
            "tick_delay": str(self.tick_delay),
            "subscription_note": self.subscription_note,
            **self.clock.as_row(),
        }


def screen(quote: Quote) -> Maybe[Quote]:
    """Apply the five registered refusal conditions, in the registered order."""
    if quote.bid is None or quote.ask is None:
        return Absent(
            AbsenceReason.UNQUOTED_LEG,
            f"{quote.leg}: bid={quote.bid!r} ask={quote.ask!r} at "
            f"{quote.clock.as_row()['local_ts']}. An unquoted leg is not a wide leg.",
        )
    if quote.bid > quote.ask:
        return Absent(
            AbsenceReason.CROSSED_BOOK,
            f"{quote.leg}: bid {quote.bid} above ask {quote.ask}. A crossed book "
            "is a broken book, never a zero or negative spread.",
        )
    if quote.bid <= 0.0:
        return Absent(
            AbsenceReason.ZERO_BID,
            f"{quote.leg}: bid {quote.bid} is not positive. A zero bid is not a price.",
        )
    if quote.clock.is_stale:
        return Absent(
            AbsenceReason.STALE_TIMESTAMP,
            f"{quote.leg}: venue stamp trails local capture by "
            f"{quote.clock.lag.total_seconds():.3f} s, beyond the registered tolerance.",
        )
    if quote.tick_delay is TickDelayStatus.DELAYED:
        return Absent(
            AbsenceReason.DELAYED_TICK,
            f"{quote.leg}: the feed served delayed data. A delayed quote carries a "
            "stale and artificially wide spread and is never widened into a cost band.",
        )
    if quote.tick_delay in (TickDelayStatus.FROZEN, TickDelayStatus.DELAYED_FROZEN):
        return Absent(
            AbsenceReason.FROZEN_TICK,
            f"{quote.leg}: the feed served status {quote.tick_delay.value!r}, a "
            "last-known snapshot rather than a live book.",
        )
    if quote.tick_delay is not TickDelayStatus.REALTIME:
        return Absent(
            AbsenceReason.DELAYED_TICK,
            f"{quote.leg}: tick delay status is {quote.tick_delay.value!r}. Only a "
            "real-time tick is admissible, and an unreported status is never "
            "assumed to be real-time.",
        )
    return quote


def half_spread_bps(quote: Quote, notional: float) -> float:
    """Half the touch spread, as basis points of notional.

    Half-spread rather than full: entering pays one side and exiting pays the
    other, and reporting the full spread once would double-count the entry.
    """
    if notional <= 0:
        raise ValueError(f"notional must be positive, got {notional}")
    return (quote.spread / 2.0) / notional * 10_000.0
