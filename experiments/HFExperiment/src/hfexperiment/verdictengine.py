"""The verdict engine. Recompute after each accrual, append, never edit.

Section 11 wired over the shadow series: the studentized asymptotic
confidence sequence from verdict.py at the frozen rho 0.071641, alpha
0.05 one-sided at the primary width 5, 0.025 at each secondary per
Section 4's Bonferroni split. Success when the lower bound clears the
4.07 bp per day cost hurdle. Futility when the upper bound falls below
10 bp per day. Peeking at any time inflates nothing, which is the
reason for the construction.

Every output record carries the registered honest projection: at the
recorded width-5 mean of 27.99 bp per day against 418 bp daily noise,
the lower bound clears zero at day 2061 and clears the hurdle at day
2852 under this exact frozen construction.
"""
from __future__ import annotations

import statistics
from typing import Any

from hfexperiment.accrual import WIDTHS, Ledgers, excess_series
from hfexperiment.registered import (
    PROJECTION_CLEAR_HURDLE_DAY,
    PROJECTION_CLEAR_ZERO_DAY,
    PROJECTION_MEAN_BP,
    PROJECTION_SIGMA_BP,
    RHO_FROZEN,
    THRESHOLDS,
)
from hfexperiment.verdict import (
    alpha_for_width,
    classify_verdict,
    confidence_bounds,
    first_crossing_day,
)


def registered_projection() -> dict[str, float | int]:
    """Section 11's honest arithmetic, in every engine record."""
    return {
        "mean_bp": PROJECTION_MEAN_BP,
        "sigma_bp": PROJECTION_SIGMA_BP,
        "clear_zero_day": PROJECTION_CLEAR_ZERO_DAY,
        "clear_hurdle_day": PROJECTION_CLEAR_HURDLE_DAY,
    }


def width_verdict(
    width: int, series: list[tuple[str, float]], run_utc: str
) -> dict[str, Any]:
    """One width's confidence sequence state over its computed days."""
    alpha = alpha_for_width(width)
    t = len(series)
    record: dict[str, Any] = {
        "kind": "verdict",
        "width": width,
        "alpha": alpha,
        "rho": RHO_FROZEN,
        "t": t,
        "asof_session": series[-1][0] if series else None,
        "success_bar_bp": THRESHOLDS.cost_hurdle_bp_per_day,
        "futility_bar_bp": THRESHOLDS.futility_bp_per_day,
        "projection": registered_projection(),
        "run_utc": run_utc,
    }
    if t < 2:
        record.update(
            mean_bp=None,
            sigma_bp=None,
            lower_bp=None,
            upper_bp=None,
            state="continue",
            days_to_success_at_current_mean=None,
        )
        return record
    values = [bp for _s, bp in series]
    mean_bp = statistics.fmean(values)
    sigma_bp = statistics.stdev(values)
    lower, upper = confidence_bounds(mean_bp, sigma_bp, t, RHO_FROZEN, alpha)
    state = classify_verdict(lower, upper)
    days = first_crossing_day(
        mean_bp,
        sigma_bp,
        RHO_FROZEN,
        THRESHOLDS.cost_hurdle_bp_per_day,
        alpha,
    )
    record.update(
        mean_bp=mean_bp,
        sigma_bp=sigma_bp,
        lower_bp=lower,
        upper_bp=upper,
        state=state.value,
        days_to_success_at_current_mean=days,
    )
    return record


def recompute_and_append(
    ledgers: Ledgers, run_utc: str
) -> list[dict[str, Any]]:
    """Recompute every width and append records with new information.

    Appends when a width's observation count changed since its last
    record. Idempotent re-runs append nothing. History is never edited.
    Before the first accrual there is nothing to recompute and the
    verdict ledger stays empty, which is what the verdict view renders
    as the pre-start state.
    """
    last_t: dict[int, int] = {}
    for r in ledgers.verdict.read_all():
        last_t[int(r["width"])] = int(r["t"])
    appended: list[dict[str, Any]] = []
    for width in WIDTHS:
        series = excess_series(ledgers, width)
        t = len(series)
        if t == 0 and width not in last_t:
            continue
        if last_t.get(width) == t:
            continue
        record = width_verdict(width, series, run_utc)
        ledgers.verdict.append(record)
        appended.append(record)
    return appended
