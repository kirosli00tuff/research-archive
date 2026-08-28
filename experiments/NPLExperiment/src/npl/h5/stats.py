"""Descriptive statistics over served basis observations. Absences never count.

Every figure produced here travels with its n (standing rule 10): the
functions take the raw `Maybe[float]` series, drop recorded absences, and
return the surviving count alongside the statistic. Nothing imputes.
"""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass

from npl.absence import Maybe
from npl.h5.basis import present_values


def median(values: Sequence[float]) -> float:
    """The sample median. Refuses an empty sample rather than returning zero."""
    if not values:
        raise ValueError("refusing a median of an empty sample; report the absence instead")
    ordered = sorted(values)
    n = len(ordered)
    mid = n // 2
    if n % 2 == 1:
        return ordered[mid]
    return (ordered[mid - 1] + ordered[mid]) / 2.0


def quantile(values: Sequence[float], q: float) -> float:
    """Linear-interpolated quantile, the numpy default, written out."""
    if not values:
        raise ValueError("refusing a quantile of an empty sample")
    if not 0.0 <= q <= 1.0:
        raise ValueError(f"quantile {q} outside [0, 1]")
    ordered = sorted(values)
    if len(ordered) == 1:
        return ordered[0]
    position = q * (len(ordered) - 1)
    low = int(position)
    high = min(low + 1, len(ordered) - 1)
    weight = position - low
    return ordered[low] * (1.0 - weight) + ordered[high] * weight


@dataclass(frozen=True, slots=True)
class Summary:
    """One basis sample, summarized. Every figure carries its n."""

    n: int
    n_absent: int
    median_abs_bp: float | None
    q1_abs_bp: float | None
    q3_abs_bp: float | None
    share_over_floor: float | None
    share_over_viable: float | None

    @property
    def iqr_abs_bp(self) -> float | None:
        if self.q1_abs_bp is None or self.q3_abs_bp is None:
            return None
        return self.q3_abs_bp - self.q1_abs_bp


def summarize(values: Sequence[Maybe[float]], floor_bp: float, viable_bp: float) -> Summary:
    """Median, IQR and exceedance shares of the absolute basis, with its n."""
    served = present_values(values)
    n_absent = len(values) - len(served)
    if not served:
        return Summary(
            n=0,
            n_absent=n_absent,
            median_abs_bp=None,
            q1_abs_bp=None,
            q3_abs_bp=None,
            share_over_floor=None,
            share_over_viable=None,
        )
    magnitudes = [abs(v) for v in served]
    n = len(magnitudes)
    return Summary(
        n=n,
        n_absent=n_absent,
        median_abs_bp=median(magnitudes),
        q1_abs_bp=quantile(magnitudes, 0.25),
        q3_abs_bp=quantile(magnitudes, 0.75),
        share_over_floor=sum(1 for m in magnitudes if m > floor_bp) / n,
        share_over_viable=sum(1 for m in magnitudes if m > viable_bp) / n,
    )
