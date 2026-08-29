"""Section 9 — power, computed rather than taken from the prompt.

**Where the computation disagrees with the figures stated in the operator
prompt, the computation wins and the disagreement is recorded.** That is Section
9's own instruction and it is why this module exists at all.

E1's power needs only a Sharpe assumption and a session count, both of which
this repository has. **E2's power needs a per-trade dispersion figure, and
Section 9 restricts that input to the pre-period carve-out** — which no vendor
currently serves. E2 power is therefore a recorded absence, and the
**standardized** quantity that does not need dispersion, the minimum per-trade
information ratio, is computed and reported in its place.

This module reads no outcome value. Every input is a count or a registered
assumption.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from statistics import NormalDist
from typing import Final, final

from orb.absence import AbsenceReason, Absent, Maybe
from orb.config import CONFIG

_NORMAL: Final[NormalDist] = NormalDist()


def z(quantile: float) -> float:
    return _NORMAL.inv_cdf(quantile)


def daily_sharpe(annual_sharpe: float) -> float:
    """``annual / sqrt(252)``. At 1.40 this is 0.0882."""
    return annual_sharpe / math.sqrt(CONFIG.trading_days_per_year)


def t_statistic(annual_sharpe: float, sessions: int) -> float:
    """``daily_sharpe * sqrt(n)``. The Section 9 arithmetic, in code."""
    if sessions < 1:
        raise ValueError("session count must be positive")
    return daily_sharpe(annual_sharpe) * math.sqrt(sessions)


def sessions_for_t(annual_sharpe: float, target_t: float) -> int:
    """Smallest whole session count reaching ``target_t``. Ceiling, never round."""
    d = daily_sharpe(annual_sharpe)
    if d <= 0:
        raise ValueError("a non-positive Sharpe assumption clears no t")
    return math.ceil((target_t / d) ** 2)


def power_one_sided(annual_sharpe: float, sessions: int, alpha: float) -> float:
    """Power of the one-sided Sharpe test at ``alpha``.

    Under the alternative the t statistic is approximately normal with mean
    ``daily_sharpe * sqrt(n)`` and unit variance, so power is
    ``Phi(mean - z_{1-alpha})``.
    """
    return _NORMAL.cdf(t_statistic(annual_sharpe, sessions) - z(1.0 - alpha))


def sessions_for_power(annual_sharpe: float, alpha: float, target_power: float) -> int:
    """Minimum N clearing ``target_power``. ``n = ((z_a + z_b) / SR_daily)^2``."""
    d = daily_sharpe(annual_sharpe)
    if d <= 0:
        raise ValueError("a non-positive Sharpe assumption reaches no power")
    return math.ceil(((z(1.0 - alpha) + z(target_power)) / d) ** 2)


def information_ratio_for_t(trades: int, target_t: float) -> float:
    """The per-trade information ratio needed to clear ``target_t``.

    Standardized, so it needs **no dispersion input** — which is why it is
    computable today while E2's power is not.
    """
    if trades < 1:
        raise ValueError("trade count must be positive")
    return target_t / math.sqrt(trades)


def e2_power(
    per_trade_dispersion: Maybe[float],
    per_trade_mean: Maybe[float],
    trades: int,
    alpha: float,
) -> Maybe[float]:
    """E2 power. Refuses unless the pre-period dispersion has been measured."""
    if isinstance(per_trade_dispersion, Absent):
        return per_trade_dispersion
    if isinstance(per_trade_mean, Absent):
        return per_trade_mean
    if per_trade_dispersion <= 0:
        raise ValueError("dispersion must be positive")
    effect = per_trade_mean / per_trade_dispersion * math.sqrt(trades)
    return _NORMAL.cdf(effect - z(1.0 - alpha))


def e2_pessimistic_mean(central_mean: float, pessimistic_shift: float) -> float:
    """The mean net PnL per share once both slippage legs move to the band's end.

    **Amendment 19.** E2's null is that this quantity is at or below zero. The
    shift is an **absolute dollar amount per share**, so it does **not** divide
    out of the ratio the power computation forms — which is the whole reason the
    A.1 TASK 5 dispersion measurement becomes load-bearing under the amended E2
    and was inert under the old one.
    """
    return central_mean - pessimistic_shift


def e2_power_pessimistic(
    per_trade_dispersion: Maybe[float],
    central_mean_per_share: Maybe[float],
    pessimistic_shift_per_share: float,
    trades: int,
    alpha: float,
) -> Maybe[float]:
    """Power of the amended E2, one-sided at ``alpha``.

    **A negative pessimistic-cost mean is not an error and is not clamped.** It
    returns a power **below the size of the test**, which is the correct answer:
    a one-sided test cannot reject a null of *"mean <= 0"* in favour of a true
    mean that is itself negative, and the probability of doing so by chance
    falls below ``alpha``. **Clamping it to ``alpha`` or to zero would hide the
    finding this amendment exists to surface.**
    """
    if isinstance(per_trade_dispersion, Absent):
        return per_trade_dispersion
    if isinstance(central_mean_per_share, Absent):
        return central_mean_per_share
    if per_trade_dispersion <= 0:
        raise ValueError("dispersion must be positive")
    pessimistic = e2_pessimistic_mean(
        central_mean_per_share, pessimistic_shift_per_share
    )
    effect = pessimistic / per_trade_dispersion * math.sqrt(trades)
    return _NORMAL.cdf(effect - z(1.0 - alpha))


def trades_for_e2_power(
    per_trade_dispersion: float,
    pessimistic_mean_per_share: float,
    alpha: float,
    target_power: float,
) -> Maybe[int]:
    """Minimum trade count clearing ``target_power`` under the amended E2.

    Returns a **recorded absence** when the pessimistic-cost mean is at or below
    zero, because **no sample size reaches the target**: the effect the test is
    powered against does not exist in the direction the test looks. **That is a
    property of the registered design at the registered assumption, and it is
    reported as an absence rather than as a very large number** — the same rule
    ADR-026 applies to an unreached rate ceiling.
    """
    if per_trade_dispersion <= 0:
        raise ValueError("dispersion must be positive")
    if pessimistic_mean_per_share <= 0:
        return Absent(
            AbsenceReason.NOT_YET_MEASURED,
            "no trade count reaches the target: the pessimistic-cost mean is "
            f"{pessimistic_mean_per_share:.9f} USD per share, at or below zero, "
            "so the one-sided alternative the test is powered against lies "
            "inside the null",
        )
    ratio = pessimistic_mean_per_share / per_trade_dispersion
    return math.ceil(((z(1.0 - alpha) + z(target_power)) / ratio) ** 2)


@final
@dataclass(frozen=True, slots=True)
class PowerRow:
    """One (assumption, horizon) cell of the reported power table."""

    assumption_name: str
    annual_sharpe: float
    horizon_name: str
    sessions: int
    t_statistic: float
    e1_power: float
    e1_min_n_for_80: int
    e2_power: Maybe[float]


def pre_period_dispersion_absent() -> Absent:
    """The registered reason E2 power cannot be computed today."""
    return Absent(
        AbsenceReason.NOT_YET_MEASURED,
        "Section 9 restricts the E2 dispersion input to the pre-period carve-out, "
        "and A.1 TASK 1 measured 0 of 9 vendors serving a bar to this repository",
    )
