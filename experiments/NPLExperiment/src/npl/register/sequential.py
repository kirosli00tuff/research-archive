"""The exact two-look binomial boundary (Amendment H2-3 Change 3).

Pure arithmetic over counts and registered probabilities — no path, no file
API, no parser — exactly the shape of `npl.power` and `npl.register.cull`,
and pinned that way by test.

The registered construction, with n1 pairs and S1 successes at look 1, n2
pairs and S2 successes at look 2, and the null p0 = 1/2:

    k1 = min { k : P(Bin(n1, p0) >= k) <= alpha_1 }

    k2 = min { k : sum_{s < k1} P(Bin(n1, p0) = s)
                     * P(Bin(n2 - n1, p0) >= k - s)  <= alpha_2 }

    reject at look 1  <=>  S1 >= k1
    reject at look 2  <=>  S1 < k1  and  S2 >= k2

The look-2 spend is computed conditional on not having rejected at look 1,
over the independent increment Bin(n2 - n1, p0), so the total type-I error
is at most alpha_1 + alpha_2 exactly — no asymptotic approximation appears
anywhere. A look at which no k satisfies its inequality **cannot reject**;
that is recorded as `k is None` and the alpha is never relaxed to
manufacture a boundary.

Validity rests on n1 and n2 being fixed by outcome-blind quantities — pair
counts and the calendar — never by an observed statistic. That is a
property of the collection substrate, registered in Amendment H2-3, not of
this module.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import ceil

from npl.config import CONFIG, Config
from npl.power import critical_k, pmf, upper_tail

NULL_SHARE = 0.5


class LookOrderViolation(ValueError):
    """A look was asked for out of its registered order, or with n2 < n1."""


@dataclass(frozen=True, slots=True)
class TwoLookDesign:
    """One co-primary's exact boundary at one (n1, n2) and one alpha split."""

    n1: int
    n2: int
    alpha_1: float
    alpha_2: float
    k1: int | None
    k2: int | None
    alpha_spent_1: float
    alpha_spent_2: float

    def alpha_spent_total(self) -> float:
        return self.alpha_spent_1 + self.alpha_spent_2


def look2_spend(n1: int, n2: int, k1: int | None, k2: int, p0: float = NULL_SHARE) -> float:
    """P(no rejection at look 1 and S2 >= k2) under p0. The exact look-2 spend.

    With k1 = None (look 1 could not reject at any k) the whole null mass
    reaches look 2, which is the correct and conservative accounting.
    """
    if n2 < n1:
        raise LookOrderViolation(f"look 2 has fewer pairs than look 1: n2={n2} < n1={n1}")
    increment = n2 - n1
    ceiling = n1 + 1 if k1 is None else min(k1, n1 + 1)
    return sum(pmf(n1, s, p0) * upper_tail(increment, k2 - s, p0) for s in range(max(ceiling, 0)))


def look2_critical(
    n1: int, n2: int, k1: int | None, alpha_2: float, p0: float = NULL_SHARE
) -> int | None:
    """The smallest k2 whose conditional spend stays inside alpha_2, or None."""
    if look2_spend(n1, n2, k1, n2, p0) > alpha_2:
        return None
    lo, hi = 0, n2
    while lo < hi:
        mid = (lo + hi) // 2
        if look2_spend(n1, n2, k1, mid, p0) <= alpha_2:
            hi = mid
        else:
            lo = mid + 1
    return lo


def two_look_design(
    n1: int,
    n2: int,
    alpha_1: float,
    alpha_2: float,
    p0: float = NULL_SHARE,
) -> TwoLookDesign:
    """Both boundaries and both exact spends at one (n1, n2)."""
    if n1 < 0 or n2 < n1:
        raise LookOrderViolation(f"impossible look sizes: n1={n1}, n2={n2}")
    k1 = critical_k(n1, p0, alpha_1)
    k2 = look2_critical(n1, n2, k1, alpha_2, p0)
    return TwoLookDesign(
        n1=n1,
        n2=n2,
        alpha_1=alpha_1,
        alpha_2=alpha_2,
        k1=k1,
        k2=k2,
        alpha_spent_1=0.0 if k1 is None else upper_tail(n1, k1, p0),
        alpha_spent_2=0.0 if k2 is None else look2_spend(n1, n2, k1, k2, p0),
    )


def two_look_power(design: TwoLookDesign, p_true: float) -> float:
    """P(reject at look 1 or look 2) at the registered true share."""
    power = 0.0 if design.k1 is None else upper_tail(design.n1, design.k1, p_true)
    if design.k2 is not None:
        power += look2_spend(design.n1, design.n2, design.k1, design.k2, p_true)
    return min(1.0, power)


def planned_n1(n2: int, cfg: Config = CONFIG) -> int:
    """The registered planning interim: ceil(n2 * h2_planning_interim_fraction)."""
    return max(1, ceil(n2 * cfg.h2_planning_interim_fraction))


def min_n2_for_power(
    alpha_1: float,
    alpha_2: float,
    p_true: float,
    target: float,
    n_max: int,
    p0: float = NULL_SHARE,
    cfg: Config = CONFIG,
) -> int | None:
    """Smallest n2 from which two-look power stays at or above target.

    Stays-at-or-above semantics, as H1 and Amendment H2-1: exact binomial
    power saw-tooths as the critical k steps, so the first crossing is not
    the answer. n1 is the registered planning fraction of n2.
    """
    good_from: int | None = None
    for n2 in range(2, n_max + 1):
        design = two_look_design(planned_n1(n2, cfg), n2, alpha_1, alpha_2, p0)
        if two_look_power(design, p_true) >= target:
            if good_from is None:
                good_from = n2
        else:
            good_from = None
    return good_from


def futility_boundary(design: TwoLookDesign, p_true: float, cfg: Config = CONFIG) -> int | None:
    """The registered look-1 futility boundary f1, or None where none exists.

    CP(s) = P(Bin(n2 - n1, p_true) >= k2 - s) is the conditional power of a
    look-2 rejection given S1 = s. It is non-decreasing in s, so the set of
    s with CP(s) under the registered floor is a lower interval and f1 is
    its largest member. Futility fires at look 1 when S1 <= f1.
    """
    if design.k2 is None:
        return None
    ceiling = design.n1 + 1 if design.k1 is None else min(design.k1, design.n1 + 1)
    increment = design.n2 - design.n1
    boundary: int | None = None
    for s in range(max(ceiling, 0)):
        if upper_tail(increment, design.k2 - s, p_true) < cfg.h2_futility_conditional_power:
            boundary = s
        else:
            break
    return boundary


def look1_stop_probability(design: TwoLookDesign, p_true: float) -> float:
    """P(the look-1 boundary is crossed) at the registered alternative.

    The interim's value: a split whose look 1 almost never fires has deleted
    one of its looks (the Amendment H2-3 materiality clause (b)).
    """
    if design.k1 is None:
        return 0.0
    return upper_tail(design.n1, design.k1, p_true)
