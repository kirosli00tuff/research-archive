"""Dispersion statistics for the calendar-time series.

This module reads `var/insider_dispersion.db`, which holds daily portfolio
excess returns already centered on their own mean. The mean is never written
there, so it cannot be read back out, and nothing in this package computes one.

`DispersionStats` carries no first moment of the return series. Its field tuple
is asserted exactly in tests/test_guards.py, so a field cannot be added here
without the guard failing.
"""

from __future__ import annotations

import math
import sqlite3
from collections.abc import Iterator
from contextlib import contextmanager
from dataclasses import dataclass

from insider.config import CONFIG, Config
from insider.paths import DISPERSION_DB


class CenteringBroken(RuntimeError):
    """The stored series does not sum to zero. It was not centered."""


@contextmanager
def _connect() -> Iterator[sqlite3.Connection]:
    if not DISPERSION_DB.exists():
        raise FileNotFoundError(f"dispersion store missing: {DISPERSION_DB}")
    con = sqlite3.connect(f"file:{DISPERSION_DB}?mode=ro", uri=True)
    try:
        yield con
    finally:
        con.close()


@dataclass(frozen=True, slots=True)
class CenteredSeries:
    """Deviations from the series mean, and the book width behind each one.

    Every value here is a deviation. The series sums to zero by construction, so
    no arrangement of these numbers recovers the alpha they were centered on.
    """

    hold_sessions: int
    weighting: str
    dates: tuple[str, ...]
    centered: tuple[float, ...]
    book_width: tuple[int, ...]

    def __post_init__(self) -> None:
        if not self.centered:
            return
        total = math.fsum(self.centered)
        scale = math.sqrt(math.fsum(v * v for v in self.centered))
        if scale > 0 and abs(total) > 1e-9 * scale * math.sqrt(len(self.centered)):
            raise CenteringBroken(
                f"the stored series for hold {self.hold_sessions} sums to {total:.3e}, "
                f"which is not zero. It was not centered, so it carries a first moment."
            )


def load(hold_sessions: int, weighting: str) -> CenteredSeries:
    with _connect() as con:
        rows = con.execute(
            "SELECT date, centered, book_width FROM centered_excess "
            "WHERE hold_sessions = ? AND weighting = ? ORDER BY date",
            (hold_sessions, weighting),
        ).fetchall()
    return CenteredSeries(
        hold_sessions=hold_sessions,
        weighting=weighting,
        dates=tuple(r[0] for r in rows),
        centered=tuple(float(r[1]) for r in rows),
        book_width=tuple(int(r[2]) for r in rows),
    )


def dropped(hold_sessions: int, weighting: str) -> dict[str, int]:
    with _connect() as con:
        return {
            r[0]: int(r[1])
            for r in con.execute(
                "SELECT reason, n FROM dropped WHERE hold_sessions = ? AND weighting = ?",
                (hold_sessions, weighting),
            )
        }


def autocorrelation(centered: tuple[float, ...], lag: int) -> float:
    """Lag-k autocorrelation of an already-centered series."""
    n = len(centered)
    if lag <= 0 or lag >= n:
        raise ValueError(f"lag {lag} outside 1..{n - 1}")
    denominator = math.fsum(v * v for v in centered)
    if denominator <= 0:
        raise ValueError("a series with zero dispersion has no autocorrelation")
    numerator = math.fsum(centered[t] * centered[t + lag] for t in range(n - lag))
    return numerator / denominator


def variance_inflation(centered: tuple[float, ...], lags: int) -> float:
    """Newey-West Bartlett variance inflation for the mean of a serial series.

    1 + 2 * sum over k of (1 - k/(L+1)) * rho_k. The Bartlett weights keep the
    estimate positive semi-definite, which a raw sum of autocorrelations does
    not guarantee.
    """
    n = len(centered)
    if n < 2:
        raise ValueError("variance inflation needs at least two observations")
    usable = min(lags, n - 1)
    total = 1.0 + 2.0 * math.fsum(
        (1.0 - k / (usable + 1)) * autocorrelation(centered, k) for k in range(1, usable + 1)
    )
    if total <= 0:
        raise ValueError(f"the Bartlett estimate came out at {total:.4f}, which is not a variance")
    return total


@dataclass(frozen=True, slots=True)
class DispersionStats:
    """Second moments, counts, and nothing else.

    tests/test_guards.py asserts this exact field tuple. Adding a field fails
    the guard, which is the point: a first moment cannot be smuggled in beside
    the dispersion it was computed from.
    """

    hold_sessions: int
    weighting: str
    n_sessions: int
    sd_daily_excess: float
    annualized_tracking_error: float
    newey_west_lags: int
    variance_inflation: float
    effective_periods: float
    autocorr_lag_1: float
    autocorr_lag_5: float
    autocorr_lag_21: float
    book_width_mean: float
    book_width_min: int
    book_width_p10: int
    book_width_p50: int
    book_width_p90: int
    book_width_max: int


def sample_sd(centered: tuple[float, ...]) -> float:
    """Sample standard deviation of an already-centered series.

    Divides by n minus 1. The series was centered on its own sample mean, so one
    degree of freedom is already spent and this is the unbiased divisor.
    """
    n = len(centered)
    if n < 2:
        raise ValueError("a standard deviation needs at least two observations")
    return math.sqrt(math.fsum(v * v for v in centered) / (n - 1))


def summarize(
    series: CenteredSeries, lags: int | None = None, cfg: Config = CONFIG
) -> DispersionStats:
    """Reduce a centered series to dispersion, counts, and book width."""
    n = len(series.centered)
    if n < 2:
        raise ValueError(f"hold {series.hold_sessions} has {n} sessions, too few to measure")
    use_lags = cfg.newey_west_lags if lags is None else lags
    sd = sample_sd(series.centered)
    vif = variance_inflation(series.centered, use_lags)
    widths = sorted(series.book_width)
    return DispersionStats(
        hold_sessions=series.hold_sessions,
        weighting=series.weighting,
        n_sessions=n,
        sd_daily_excess=sd,
        annualized_tracking_error=sd * math.sqrt(cfg.sessions_per_month * 12),
        newey_west_lags=use_lags,
        variance_inflation=vif,
        effective_periods=n / vif,
        autocorr_lag_1=autocorrelation(series.centered, 1),
        autocorr_lag_5=autocorrelation(series.centered, 5),
        autocorr_lag_21=autocorrelation(series.centered, 21),
        book_width_mean=sum(widths) / len(widths),
        book_width_min=widths[0],
        book_width_p10=widths[len(widths) // 10],
        book_width_p50=widths[len(widths) // 2],
        book_width_p90=widths[len(widths) * 9 // 10],
        book_width_max=widths[-1],
    )
