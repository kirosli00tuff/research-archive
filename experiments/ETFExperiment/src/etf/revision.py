"""A.1 Task 4, forward leg: the revision rate, and the two rates that matter.

For every trading day with at least two captures, the first value served is
compared against the value standing `revision_settle_hours` later. The share of
days revised is reported, and so is the distribution of revision sizes — but
**the sign-flip rate and the threshold-cross rate are the figures that decide
the verdict**, because they are the ones that would corrupt the test toward a
false positive: a day whose as-printed signal said "long" and whose settled
value says "short" is a day the registered rule traded on a number that no
longer exists.
"""

from __future__ import annotations

import statistics
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from datetime import date, datetime, timedelta

from etf.config import CONFIG
from etf.signal import position


@dataclass(frozen=True, slots=True)
class ValueAt:
    captured_at: datetime
    signal_usd: float


@dataclass(frozen=True, slots=True)
class DayRevision:
    trade_date: date
    first_value_usd: float
    first_captured_at: datetime
    settled_value_usd: float
    settled_captured_at: datetime
    delta_usd: float
    delta_share: float | None
    sign_flipped: bool
    threshold_crossed: bool

    @property
    def revised(self) -> bool:
        return self.delta_usd != 0.0

    @property
    def intact(self) -> bool:
        """The signal survives if neither its sign nor its threshold side moved."""
        return not self.sign_flipped and not self.threshold_crossed


@dataclass(frozen=True, slots=True)
class RevisionReport:
    days: tuple[DayRevision, ...]
    n_days: int
    revised_days: int
    revised_share: float | None
    sign_flip_days: int
    sign_flip_share: float | None
    threshold_cross_days: int
    threshold_cross_share: float | None
    intact_days: int
    intact_share: float | None
    median_abs_delta_usd: float | None
    max_abs_delta_usd: float | None
    median_abs_delta_share: float | None


def compare_day(trade_date: date, values: Sequence[ValueAt]) -> DayRevision | None:
    """First served value against the value standing at the registered settle horizon."""
    if len(values) < 2:
        return None
    ordered = sorted(values, key=lambda v: v.captured_at)
    first = ordered[0]
    horizon = first.captured_at + timedelta(hours=CONFIG.revision_settle_hours)
    at_or_before = [v for v in ordered if v.captured_at <= horizon]
    settled = at_or_before[-1] if at_or_before else ordered[-1]
    if settled.captured_at == first.captured_at:
        return None
    delta = settled.signal_usd - first.signal_usd
    denominator = abs(first.signal_usd)
    first_pos = position(first.signal_usd)
    settled_pos = position(settled.signal_usd)
    return DayRevision(
        trade_date=trade_date,
        first_value_usd=first.signal_usd,
        first_captured_at=first.captured_at,
        settled_value_usd=settled.signal_usd,
        settled_captured_at=settled.captured_at,
        delta_usd=delta,
        delta_share=(delta / denominator) if denominator > 0 else None,
        # A sign flip is a change of sign in the raw signal, whether or not
        # either side clears the threshold: it is the fact that corrupts a
        # rank-correlation test, which E1 is.
        sign_flipped=(first.signal_usd > 0) != (settled.signal_usd > 0)
        and first.signal_usd != 0.0
        and settled.signal_usd != 0.0,
        # A threshold cross is a change in the position the Section 4 rule
        # would have taken: it is the fact that corrupts E2. A revision that
        # moves the value but leaves it on the same side of T is not a cross,
        # and a sign flip entirely inside the band is not one either — that
        # case is caught by sign_flipped, which is what corrupts E1.
        threshold_crossed=first_pos is not settled_pos,
    )


def build_report(per_day: Mapping[date, Sequence[ValueAt]]) -> RevisionReport:
    """Every forward-revision figure, each with the n it rests on."""
    days = tuple(r for d in sorted(per_day) if (r := compare_day(d, per_day[d])) is not None)
    n = len(days)
    if n == 0:
        return RevisionReport(
            days=(),
            n_days=0,
            revised_days=0,
            revised_share=None,
            sign_flip_days=0,
            sign_flip_share=None,
            threshold_cross_days=0,
            threshold_cross_share=None,
            intact_days=0,
            intact_share=None,
            median_abs_delta_usd=None,
            max_abs_delta_usd=None,
            median_abs_delta_share=None,
        )
    revised = [d for d in days if d.revised]
    flips = [d for d in days if d.sign_flipped]
    crosses = [d for d in days if d.threshold_crossed]
    intact = [d for d in days if d.intact]
    shares = [abs(d.delta_share) for d in days if d.delta_share is not None]
    return RevisionReport(
        days=days,
        n_days=n,
        revised_days=len(revised),
        revised_share=len(revised) / n,
        sign_flip_days=len(flips),
        sign_flip_share=len(flips) / n,
        threshold_cross_days=len(crosses),
        threshold_cross_share=len(crosses) / n,
        intact_days=len(intact),
        intact_share=len(intact) / n,
        median_abs_delta_usd=statistics.median(abs(d.delta_usd) for d in days),
        max_abs_delta_usd=max(abs(d.delta_usd) for d in days),
        median_abs_delta_share=statistics.median(shares) if shares else None,
    )
