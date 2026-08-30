"""Section 8 — the inference. **Built dark. Stage C calls it exactly once.**

Two co-primaries, one-sided, at ``alpha_adj = 1 - 0.95 ** (1/2) = 0.02532``,
**and both must pass**:

- **E1, risk-adjusted.** Deflated Sharpe ratio of the daily net portfolio return
  series over the holdout, by the Bailey and Lopez de Prado method, trial count
  registered at **8**, skewness and kurtosis taken from the realized series.
  **Bar: deflated Sharpe at or above 1.00.**
- **E2, economic.** Mean net PnL per trade, one-sided lower bound above zero, by
  **permutation on session labels with trades clustered by session date**, so
  that a single strong session cannot masquerade as many independent
  observations.

Two structural gates apply alongside, **registered as pass-fail and not as
tests**: no single holdout calendar year contributes more than 50 percent of
holdout net PnL, and holdout net PnL is positive in at least 3 of the 4 holdout
calendar years.
"""

from __future__ import annotations

import math
import random
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from statistics import NormalDist, fmean, stdev
from typing import Final, final

from orb.absence import AbsenceReason, Absent, Maybe
from orb.config import CONFIG

EULER_MASCHERONI: Final[float] = 0.5772156649015329
_NORMAL: Final[NormalDist] = NormalDist()


def alpha_adj(n_co_primaries: int = CONFIG.n_co_primaries) -> float:
    """``1 - 0.95 ** (1 / k)``. At k = 2 this is 0.02532057...

    **SUPERSEDED by Amendment 18 as the per-co-primary level.** It is kept, and
    kept correct, because it is already pushed and because every amended table
    reports the new level **beside** it so the change is legible. **It is the
    right correction for a union rule and the wrong one for Section 8's
    conjunction.** Use :func:`per_test_alpha` for the co-primaries.
    """
    adjusted: float = 1.0 - 0.95 ** (1.0 / n_co_primaries)
    return adjusted


def per_test_alpha() -> float:
    """The registered per-co-primary level, one-sided. **0.05.**

    **Amendment 18.** Section 8 requires **both** co-primaries to pass, which is
    an **intersection-union test**. Berger (1982) — *Multiparameter hypothesis
    testing and acceptance sampling*, `Technometrics` 24(4), 295-300 — shows that
    an IUT whose components each run at level ``a`` has overall size **at most**
    ``a``: under the global null the event that **all** components reject is
    contained in the event that **any one** does, so no multiplicity correction
    is owed.

    **This is a correction, not a loosening.** The conjunction itself supplies
    the conservatism: requiring two independent-ish tests to clear 0.05 is
    stricter than requiring one to clear 0.05, and the size of the combined
    procedure is what a reader is entitled to know. **Applying a union
    correction to an intersection rule made the registered design harder than it
    claimed to be, in a direction nobody had chosen.**

    **The deflated Sharpe keeps its own, separate correction** for the **8
    registered parameterization trials** (four range lengths crossed with two
    entry rules). That is a **different multiplicity** — the number of ways the
    rule could have been specified — and Amendment 18 does not touch it.
    """
    return CONFIG.per_test_alpha


# --- Sharpe and its deflation ---------------------------------------------


def sharpe(returns: Sequence[float]) -> float:
    """Per-observation Sharpe. Zero excess assumed; the series is already net."""
    if len(returns) < 2:
        raise ValueError("need at least two observations")
    spread = stdev(returns)
    if spread == 0:
        raise ValueError("zero dispersion: a Sharpe is undefined")
    return fmean(returns) / spread


def annualize(per_observation_sharpe: float) -> float:
    return per_observation_sharpe * math.sqrt(CONFIG.trading_days_per_year)


def daily_from_annual(annual_sharpe: float) -> float:
    return annual_sharpe / math.sqrt(CONFIG.trading_days_per_year)


def skewness(returns: Sequence[float]) -> float:
    n = len(returns)
    mean, spread = fmean(returns), stdev(returns)
    return sum(((r - mean) / spread) ** 3 for r in returns) / n


def kurtosis(returns: Sequence[float]) -> float:
    """Non-excess kurtosis: a normal series returns 3.0."""
    n = len(returns)
    mean, spread = fmean(returns), stdev(returns)
    return sum(((r - mean) / spread) ** 4 for r in returns) / n


def expected_max_sharpe(n_trials: int, trial_sharpe_sd: Maybe[float]) -> Maybe[float]:
    """SR0 — the Sharpe a maximum over ``n_trials`` reaches by chance alone.

    Bailey and Lopez de Prado. **It scales with the dispersion of Sharpes across
    the trials**, which is a measured quantity. Where that dispersion has not
    been measured this returns a recorded absence rather than assuming one: a
    deflation benchmark computed from an invented dispersion would deflate by an
    invented amount.
    """
    if isinstance(trial_sharpe_sd, Absent):
        return trial_sharpe_sd
    if n_trials < 2:
        raise ValueError("deflation needs at least two trials")
    gamma = EULER_MASCHERONI
    term_a = _NORMAL.inv_cdf(1.0 - 1.0 / n_trials)
    term_b = _NORMAL.inv_cdf(1.0 - 1.0 / (n_trials * math.e))
    return trial_sharpe_sd * ((1.0 - gamma) * term_a + gamma * term_b)


def deflated_sharpe_probability(
    returns: Sequence[float], sr0_per_observation: float
) -> float:
    """The Bailey and Lopez de Prado DSR: P(true Sharpe > SR0).

    Skewness and kurtosis are taken from the realized series, as registered.
    """
    n = len(returns)
    if n < 3:
        raise ValueError("need at least three observations")
    sr = sharpe(returns)
    g3, g4 = skewness(returns), kurtosis(returns)
    denominator = 1.0 - g3 * sr + ((g4 - 1.0) / 4.0) * sr * sr
    if denominator <= 0:
        raise ValueError("degenerate moment denominator; DSR is undefined")
    z = (sr - sr0_per_observation) * math.sqrt(n - 1) / math.sqrt(denominator)
    return _NORMAL.cdf(z)


def deflated_sharpe_statistic(
    returns: Sequence[float], sr0_per_observation: Maybe[float]
) -> Maybe[float]:
    """The E1 statistic: **annualized** Sharpe net of the deflation benchmark.

    Registered under ADR-004. Section 8 sets the E1 bar at "deflated Sharpe at
    or above 1.00", and a probability cannot reach 1.00, so the bar is read as
    the **annualized deflated Sharpe value**. The DSR *probability* is computed
    and reported beside it as a named secondary.
    """
    if isinstance(sr0_per_observation, Absent):
        return sr0_per_observation
    return annualize(sharpe(returns) - sr0_per_observation)


# --- E2, the clustered permutation ----------------------------------------


def permutation_lower_bound(
    pnl_by_session: Mapping[str, Sequence[float]],
    *,
    iterations: int = 10_000,
    seed: int = 20260829,
) -> tuple[float, float]:
    """One-sided p-value and the observed mean net PnL per trade.

    **Trades are clustered by session date**: one sign flip applies to every
    trade in a session, so a single strong session contributes one draw and not
    many. Flipping at the trade level would treat trades sharing a session's
    market factor as independent and would understate the p-value.
    """
    sessions = sorted(pnl_by_session)
    if not sessions:
        raise ValueError("no sessions supplied")
    trades = [pnl for s in sessions for pnl in pnl_by_session[s]]
    if not trades:
        raise ValueError("no trades supplied")

    observed = fmean(trades)
    total = len(trades)
    rng = random.Random(seed)
    at_least_as_extreme = 0
    for _ in range(iterations):
        running = 0.0
        for session in sessions:
            flip = 1.0 if rng.random() < 0.5 else -1.0
            running += flip * sum(pnl_by_session[session])
        if running / total >= observed:
            at_least_as_extreme += 1
    p_value = (at_least_as_extreme + 1) / (iterations + 1)
    return p_value, observed


# --- The two structural gates ---------------------------------------------


def concentration_gate(pnl_by_year: Mapping[int, float]) -> bool:
    """No single holdout calendar year above 50 percent of holdout net PnL.

    Registered because **76 percent of the replication's filtered profit came
    from 2022 alone** (carried, C-8). A year with negative PnL cannot satisfy
    the gate by shrinking the denominator: the share is taken over the total,
    and a non-positive total fails.
    """
    total = sum(pnl_by_year.values())
    if total <= 0:
        return False
    return all(
        pnl / total <= CONFIG.max_single_year_pnl_share for pnl in pnl_by_year.values()
    )


def persistence_gate(pnl_by_year: Mapping[int, float]) -> bool:
    """Positive net PnL in at least 3 of the 4 holdout calendar years."""
    positive = sum(1 for pnl in pnl_by_year.values() if pnl > 0)
    return positive >= CONFIG.min_positive_holdout_years


# --- The verdict ----------------------------------------------------------


@final
@dataclass(frozen=True, slots=True)
class VerdictResult:
    e1_statistic: float | None
    e1_passes: bool
    e2_p_value: float
    e2_mean_pnl: float
    e2_passes: bool
    concentration_passes: bool
    persistence_passes: bool

    @property
    def passes(self) -> bool:
        """**All four.** Two co-primaries and two structural gates."""
        return (
            self.e1_passes
            and self.e2_passes
            and self.concentration_passes
            and self.persistence_passes
        )


def fire_verdict(
    daily_returns: Sequence[float],
    pnl_by_session: Mapping[str, Sequence[float]],
    pnl_by_year: Mapping[int, float],
    sr0_per_observation: Maybe[float],
    *,
    iterations: int = 10_000,
) -> Maybe[VerdictResult]:
    """Section 8, fired. Stage C calls this exactly once, behind the latch."""
    e1 = deflated_sharpe_statistic(daily_returns, sr0_per_observation)
    if isinstance(e1, Absent):
        return Absent(
            AbsenceReason.NOT_YET_MEASURED,
            f"E1 cannot be computed: {e1.detail}",
        )
    p_value, mean_pnl = permutation_lower_bound(pnl_by_session, iterations=iterations)
    return VerdictResult(
        e1_statistic=e1,
        e1_passes=e1 >= CONFIG.deflated_sharpe_bar,
        e2_p_value=p_value,
        e2_mean_pnl=mean_pnl,
        e2_passes=p_value < alpha_adj(),
        concentration_passes=concentration_gate(pnl_by_year),
        persistence_passes=persistence_gate(pnl_by_year),
    )
