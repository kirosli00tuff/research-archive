"""Derive the collection window from the verified knowledge cutoff.

The window is never assumed. It is computed from the cutoff recorded in
CONFIG, a guard band, and the session calendar the bar store actually holds.
The guard band exists because the memorization literature shows leakage past
claimed cutoff dates, so the month immediately after the cutoff is discarded
rather than trusted.
"""

from __future__ import annotations

import datetime as dt
from dataclasses import dataclass
from typing import Sequence

from dateutil.relativedelta import relativedelta

from npd.config import CONFIG, Config


@dataclass(frozen=True, slots=True)
class DerivedWindow:
    """The collection window and everything derived from it."""

    cutoff: dt.date
    guard_band_end: dt.date
    start: dt.date
    end: dt.date
    sessions: tuple[dt.date, ...]
    clears_power_floor: bool

    @property
    def n_days(self) -> int:
        return len(self.sessions)

    def evaluable_days(self, horizon_sessions: int) -> int:
        """Days whose forward return of the given horizon lands inside the store.

        A ranking made on session t needs session t plus horizon to exist. The
        last `horizon` sessions of the window therefore have no forward return.
        Those days are still collected. Their absence is recorded at B.2, never
        filled.
        """
        return max(0, self.n_days - horizon_sessions)


def guard_band_end(cutoff: dt.date, months: int) -> dt.date:
    """The last date discarded by the guard band."""
    return cutoff + relativedelta(months=months)


def derive_window(sessions: Sequence[dt.date], cfg: Config = CONFIG) -> DerivedWindow:
    """Build the window from an ascending session calendar.

    `sessions` must be the exchange calendar, ascending and unique. The window
    is every session strictly after the guard band through the registered end
    date inclusive.
    """
    ordered = tuple(sessions)
    if list(ordered) != sorted(set(ordered)):
        raise ValueError("sessions must be ascending and unique")

    band_end = guard_band_end(cfg.knowledge_cutoff, cfg.guard_band_months)
    inside = tuple(d for d in ordered if band_end < d <= cfg.window_end)
    if not inside:
        raise ValueError(
            f"no sessions between {band_end} and {cfg.window_end}. "
            "The calendar does not cover the derived window."
        )
    return DerivedWindow(
        cutoff=cfg.knowledge_cutoff,
        guard_band_end=band_end,
        start=inside[0],
        end=inside[-1],
        sessions=inside,
        clears_power_floor=len(inside) >= cfg.min_trading_days,
    )
