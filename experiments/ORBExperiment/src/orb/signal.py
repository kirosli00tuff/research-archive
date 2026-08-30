"""Section 3 — the signal, the entry and the exit. **Built dark.**

This is the section the repository turns on.

- **Opening range:** the high and low of 09:30:00.000 to 09:34:59.999 Eastern,
  resolved as the half-open ``[09:30, 09:35)`` window by `orb.sessionclock`.
- **Entry:** the first trade through the range high goes long, the first through
  the range low goes short, as a marketable limit at the boundary **plus 0.05
  percent of price** in the direction of the break.
- **Stop:** the opposite extreme of the opening range, a resting stop.
- **Exit:** the session close, 15:55 to 15:59 Eastern, **no profit target**.

Two registered departures from the source study, each with an ADR: this is a
**true breakout** and not the paper's immediate first-candle directional entry
(ADR-002), and **the 10R target is removed** (ADR-003).

**One entry per name per session. No re-entry after a stop.** If both sides
trigger inside the same bar the session is recorded `ambiguous` and excluded,
and **the ambiguous rate is a measured figure**, never an assumption.
"""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass
from enum import StrEnum, unique
from typing import final

from orb.bars import Bar, require_readable
from orb.config import CONFIG
from orb.costs import Side


@unique
class Trigger(StrEnum):
    LONG = "long"
    SHORT = "short"
    NONE = "none"
    AMBIGUOUS = "ambiguous"
    """Both sides broke inside one bar. Excluded, and counted."""


@final
@dataclass(frozen=True, slots=True)
class OpeningRange:
    """The registered range, in integer cents."""

    high_c: int
    low_c: int
    bar_count: int

    @property
    def width_c(self) -> int:
        return self.high_c - self.low_c


@final
@dataclass(frozen=True, slots=True)
class Setup:
    """One name's registered setup on one session. Prices in integer cents."""

    ticker: str
    trigger: Trigger
    entry_c: int | None
    stop_c: int | None
    side: Side | None
    triggered_at_ms: int | None
    opening_range: OpeningRange


def opening_range(
    bars: Sequence[Bar], window_ms: tuple[int, int], *, latched: bool = False
) -> OpeningRange | None:
    """The high and low of the half-open opening-range window."""
    require_readable(tuple(bars), "opening_range", latched=latched)
    start, end = window_ms
    inside = [b for b in bars if start <= b.timestamp_ms < end]
    if not inside:
        return None
    return OpeningRange(
        high_c=max(b.high_c for b in inside),
        low_c=min(b.low_c for b in inside),
        bar_count=len(inside),
    )


def entry_price_c(boundary_c: int, side: Side) -> int:
    """Marketable limit at the boundary plus 0.05 percent of price.

    The offset is applied **against** the trader in both directions and rounded
    away from the boundary, so a rounding choice never flatters the fill.
    """
    offset = boundary_c * CONFIG.entry_offset_fraction
    if side is Side.LONG:
        return boundary_c + max(1, int(offset + 0.9999999))
    return boundary_c - max(1, int(offset + 0.9999999))


def find_trigger(
    bars: Sequence[Bar],
    range_: OpeningRange,
    window_end_ms: int,
    *,
    latched: bool = False,
) -> Setup:
    """The first break of the range, after the opening range closes.

    A bar whose high clears the range high **and** whose low clears the range
    low is `AMBIGUOUS`: the minute bar cannot say which came first, and this
    repository refuses to guess. Recorded, excluded, and counted.
    """
    require_readable(tuple(bars), "find_trigger", latched=latched)
    after = sorted(
        (b for b in bars if b.timestamp_ms >= window_end_ms),
        key=lambda b: b.timestamp_ms,
    )
    for bar in after:
        broke_high = bar.high_c > range_.high_c
        broke_low = bar.low_c < range_.low_c
        if broke_high and broke_low:
            return Setup(
                "", Trigger.AMBIGUOUS, None, None, None, bar.timestamp_ms, range_
            )
        if broke_high:
            return Setup(
                "",
                Trigger.LONG,
                entry_price_c(range_.high_c, Side.LONG),
                range_.low_c,
                Side.LONG,
                bar.timestamp_ms,
                range_,
            )
        if broke_low:
            return Setup(
                "",
                Trigger.SHORT,
                entry_price_c(range_.low_c, Side.SHORT),
                range_.high_c,
                Side.SHORT,
                bar.timestamp_ms,
                range_,
            )
    return Setup("", Trigger.NONE, None, None, None, None, range_)


def stop_hit(
    bars: Sequence[Bar],
    setup: Setup,
    from_ms: int,
    *,
    latched: bool = False,
) -> int | None:
    """The first bar after entry that touches the resting stop, if any.

    The stop and the range boundary can coincide to the cent, and a touch **at**
    the stop is a hit: a resting stop at a price is filled when trade prints
    reach it, not only when they pass it.
    """
    require_readable(tuple(bars), "stop_hit", latched=latched)
    if setup.stop_c is None or setup.side is None:
        return None
    for bar in sorted(bars, key=lambda b: b.timestamp_ms):
        if bar.timestamp_ms < from_ms:
            continue
        if setup.side is Side.LONG and bar.low_c <= setup.stop_c:
            return bar.timestamp_ms
        if setup.side is Side.SHORT and bar.high_c >= setup.stop_c:
            return bar.timestamp_ms
    return None


def close_exit_c(
    bars: Sequence[Bar], window_ms: tuple[int, int], *, latched: bool = False
) -> int | None:
    """The close of the last bar inside the registered exit window."""
    require_readable(tuple(bars), "close_exit_c", latched=latched)
    start, end = window_ms
    inside = [b for b in bars if start <= b.timestamp_ms < end]
    if not inside:
        return None
    return max(inside, key=lambda b: b.timestamp_ms).close_c
