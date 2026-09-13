"""Turning an ``ib_async`` ticker into a screened :class:`mbt.quotes.Quote`.

This is the only place a broker object becomes a quote, and it is deliberately
narrow. Two conversions in it are load-bearing and both fail closed.

**A NaN touch is an absent touch, never a number.** ``ib_async`` fills ``bid``
and ``ask`` with ``float('nan')`` when the feed served nothing. NaN propagates
silently through arithmetic and compares false against every bound, so a NaN
half-spread would sail through a ceiling test and land in a percentile. It is
mapped to ``None`` here, which :func:`mbt.quotes.screen` refuses as
``Absent(unquoted_leg)``.

**The tick delay status is read from what ARRIVED, never from what was
requested.** ``reqMarketDataType(1)`` asks for real-time; it does not grant it.
Measured on this operator's own paper session on 2026-09-03: a real-time request
on MBT returned ``marketDataType = 1`` on the ticker while the feed served no
touch at all and the broker raised error 354, "Requested market data is not
subscribed". **So the status field alone does not establish a subscription.**
The touch has to be present as well, which is why the structural check runs
first and why a status of 1 over a NaN touch is refused as unquoted rather than
admitted as real-time.
"""

from __future__ import annotations

from datetime import datetime
from math import isnan
from typing import Any, final

from mbt.absence import AbsenceReason, Absent, Maybe
from mbt.clock import ObservationClock, require_utc
from mbt.figures import TickDelayStatus, status_from_market_data_type
from mbt.quotes import Quote

#: IBKR serves -1 on a size or price field to mean "no market", which is not a
#: price. It is mapped to absent rather than carried into a spread, where a
#: negative bid would produce a nonsense half-spread that the zero-bid check
#: would then have to catch by accident.
_NO_MARKET = -1.0


def _touch(value: object) -> float | None:
    """Map a ticker price field to a number or to absent. NaN is never a price."""
    if value is None:
        return None
    try:
        parsed = float(value)  # type: ignore[arg-type]
    except (TypeError, ValueError):
        return None
    if isnan(parsed):
        return None
    return None if parsed == _NO_MARKET else parsed


@final
class TickerReader:
    """Reads one leg off a ticker. Holds no state beyond the leg's name."""

    __slots__ = ("_leg", "_subscription_note")

    def __init__(self, leg: str, subscription_note: str = "") -> None:
        self._leg = leg
        self._subscription_note = subscription_note

    def read(self, ticker: Any, local: datetime) -> Maybe[Quote]:
        """Build a quote, or record why the feed served no observation at all.

        A ticker with no venue timestamp carries no observation: the feed
        answered the subscription request and sent no tick. That is an unquoted
        leg under the registered refusal conditions, and it is recorded as one
        rather than being given the local clock as a stand-in. Borrowing the
        local clock would manufacture a venue stamp that no venue produced, and
        the staleness check would then compare local against local and always
        pass.
        """
        require_utc(local, f"TickerReader({self._leg}).read(local)")
        venue = getattr(ticker, "time", None)
        if not isinstance(venue, datetime):
            return Absent(
                AbsenceReason.UNQUOTED_LEG,
                f"{self._leg}: the feed served no tick at all, so there is no venue "
                "timestamp and no touch. A missing venue stamp is never replaced by "
                "the local clock, because that would compare local against local and "
                "the staleness check would always pass.",
            )
        return Quote(
            leg=self._leg,
            bid=_touch(getattr(ticker, "bid", None)),
            ask=_touch(getattr(ticker, "ask", None)),
            clock=ObservationClock(venue=require_utc(venue, f"{self._leg}.venue"), local=local),
            tick_delay=status_from_market_data_type(getattr(ticker, "marketDataType", None)),
            subscription_note=self._subscription_note,
        )


def observed_status(ticker: Any) -> TickDelayStatus:
    """The status the feed reported, defaulting to UNKNOWN and never to live."""
    return status_from_market_data_type(getattr(ticker, "marketDataType", None))
