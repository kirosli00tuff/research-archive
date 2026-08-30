"""Section 2 — the universe and the event rule. **Built dark.**

Opening relative volume equals first-5-minute share volume divided by the
trailing 14-session median first-5-minute share volume. Rank descending, take
the top 20, ties broken by ticker ascending so the selection is deterministic
and reproducible **without reference to any price**.

This is a latched module: it reads bar values and is imported by no Stage A
module. Every entry point refuses `SEALED_VENDOR` provenance until the latch.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from statistics import median
from typing import final

from orb.bars import Bar, require_readable
from orb.config import CONFIG


@final
@dataclass(frozen=True, slots=True)
class Candidate:
    """One name's selection inputs on one session. Ordering is total."""

    ticker: str
    relative_volume: float
    session_open_c: int
    avg_volume_14: float
    atr_14_c: float
    has_locate: bool
    borrow_rate_annual: float

    def passes_filters(self) -> bool:
        """Section 2, exactly: open > 5.00, volume > 1,000,000, ATR > 0.50."""
        return (
            self.session_open_c > CONFIG.min_session_open_usd * 100
            and self.avg_volume_14 > CONFIG.min_avg_volume_shares
            and self.atr_14_c > CONFIG.min_atr_usd * 100
        )

    def shortable(self) -> bool:
        """No locate, or borrow above 25 percent, excludes the short side."""
        return self.has_locate and self.borrow_rate_annual <= (
            CONFIG.max_borrow_rate_annual
        )


def first_five_minute_volume(
    bars: Sequence[Bar], window_ms: tuple[int, int], *, latched: bool = False
) -> int:
    """Share volume inside the half-open opening-range window."""
    require_readable(tuple(bars), "first_five_minute_volume", latched=latched)
    start, end = window_ms
    return sum(b.volume for b in bars if start <= b.timestamp_ms < end)


def relative_volume(today: int, trailing: Sequence[int]) -> float:
    """Today's first-5-minute volume over the trailing 14-session median.

    A zero median is a division this repository refuses to perform: it would
    make every name with a quiet history rank first by construction.
    """
    if len(trailing) < CONFIG.relvol_lookback_sessions:
        raise ValueError(
            f"need {CONFIG.relvol_lookback_sessions} trailing sessions, "
            f"got {len(trailing)}"
        )
    window = list(trailing)[-CONFIG.relvol_lookback_sessions :]
    denominator = median(window)
    if denominator <= 0:
        raise ValueError("trailing median first-5-minute volume is zero or negative")
    return today / denominator


def select(candidates: Mapping[str, Candidate]) -> tuple[str, ...]:
    """Rank descending on relative volume, take the top 20, ties by ticker.

    Filters are applied **before** ranking, so an excluded name never occupies a
    selection slot.
    """
    eligible = [c for c in candidates.values() if c.passes_filters()]
    ordered = sorted(eligible, key=lambda c: (-c.relative_volume, c.ticker))
    return tuple(c.ticker for c in ordered[: CONFIG.selection_width])
