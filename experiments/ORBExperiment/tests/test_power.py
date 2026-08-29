"""Section 9 — power, and the disagreements the computation wins.

Section 9 instructs that the arithmetic be reproduced in code and that **the
computation wins** over the figures stated in the prompt. Two of them move by
exactly one session, for a reason worth pinning.
"""

from __future__ import annotations

import math
from datetime import date

import pytest

from orb.absence import Absent
from orb.calendar import sessions
from orb.config import CONFIG
from orb.power import (
    daily_sharpe,
    e2_power,
    information_ratio_for_t,
    power_one_sided,
    pre_period_dispersion_absent,
    sessions_for_power,
    sessions_for_t,
    t_statistic,
)
from orb.verdict import alpha_adj

ALPHA = alpha_adj()
HOLDOUT_N = 875
REGISTERED = CONFIG.registered_sharpe_assumption
PUBLISHED = CONFIG.published_sharpe_assumption
QUARTERED = CONFIG.quartered_sharpe_assumption


def test_the_holdout_session_count_comes_from_the_calendar_not_the_prompt() -> None:
    n = sum(1 for _ in sessions(date(2023, 1, 3), date(2026, 6, 30)))
    assert n == HOLDOUT_N


def test_the_daily_sharpe_reproduces_the_registration() -> None:
    assert daily_sharpe(REGISTERED) == pytest.approx(0.0882, abs=1e-4)


def test_the_minimum_n_figures_are_one_higher_than_the_prompt_states() -> None:
    """Computed 515 and 1,158 against the prompt's 514 and 1,157.

    The prompt's figures are floors: at n = 514 the statistic is **1.9994**,
    which does not clear 2.0, and at n = 1,157 it is **2.9998**, which does not
    clear 3.0. A minimum-N is the smallest count that **reaches** the bar, so it
    ceilings. Section 9 says the computation wins, and this is the whole of the
    disagreement: one session, in the safe direction.
    """
    assert sessions_for_t(REGISTERED, 2.0) == 515
    assert sessions_for_t(REGISTERED, 3.0) == 1158

    assert t_statistic(REGISTERED, 514) == pytest.approx(1.9994, abs=1e-4)
    assert t_statistic(REGISTERED, 514) < 2.0
    assert t_statistic(REGISTERED, 515) >= 2.0

    assert t_statistic(REGISTERED, 1157) == pytest.approx(2.9998, abs=1e-4)
    assert t_statistic(REGISTERED, 1157) < 3.0
    assert t_statistic(REGISTERED, 1158) >= 3.0


def test_the_holdout_t_is_2609_at_the_computed_session_count() -> None:
    """The prompt states 2.62 at n = 880; the calendar gives n = 875."""
    assert t_statistic(REGISTERED, HOLDOUT_N) == pytest.approx(2.6087, abs=1e-4)
    assert t_statistic(REGISTERED, 880) == pytest.approx(2.6162, abs=1e-4)
    assert CONFIG.holdout_per_trade_t_gate < t_statistic(REGISTERED, HOLDOUT_N) < 3.0


# --- The power table, and the DEGRADED expectation it confirms ------------


def test_e1_power_at_the_registered_assumption_is_below_the_go_floor() -> None:
    """0.7435 against the 0.80 floor. This is the DEGRADED clause firing."""
    power = power_one_sided(REGISTERED, HOLDOUT_N, ALPHA)
    assert power == pytest.approx(0.7435, abs=1e-3)
    assert power < CONFIG.target_power


def test_e1_power_at_the_published_magnitude_clears_the_go_floor() -> None:
    """0.9995. Together with the line above, this is exactly DEGRADED."""
    power = power_one_sided(PUBLISHED, HOLDOUT_N, ALPHA)
    assert power == pytest.approx(0.9995, abs=1e-3)
    assert power >= CONFIG.target_power
    assert power >= CONFIG.blocked_power_floor


def test_e1_power_at_the_quartered_assumption_is_far_below_everything() -> None:
    power = power_one_sided(QUARTERED, HOLDOUT_N, ALPHA)
    assert power == pytest.approx(0.2578, abs=1e-3)
    assert power < CONFIG.blocked_power_floor


def test_the_registered_assumption_needs_1006_sessions_for_80_percent() -> None:
    """The holdout has 875. The shortfall is 131 sessions."""
    assert sessions_for_power(REGISTERED, ALPHA, CONFIG.target_power) == 1006
    assert 1006 - HOLDOUT_N == 131


def test_the_2026_projection_misses_eighty_percent_by_three_sessions() -> None:
    """A knife-edge worth recording exactly: 1,003 against a required 1,006.

    Extending the holdout to 2026-12-31 gives power 0.7991, which is below 0.80
    by 0.0009. Three sessions decide it.
    """
    n = sum(1 for _ in sessions(date(2023, 1, 3), date(2026, 12, 31)))
    assert n == 1003
    power = power_one_sided(REGISTERED, n, ALPHA)
    assert power == pytest.approx(0.7991, abs=1e-3)
    assert power < CONFIG.target_power
    assert sessions_for_power(REGISTERED, ALPHA, CONFIG.target_power) - n == 3


def test_the_2027_projection_clears_eighty_percent() -> None:
    n = sum(1 for _ in sessions(date(2023, 1, 3), date(2027, 6, 30)))
    assert n == 1126
    assert power_one_sided(REGISTERED, n, ALPHA) >= CONFIG.target_power


def test_minimum_n_is_independent_of_the_horizon() -> None:
    """It is a property of the assumption and alpha, not of the calendar."""
    a = sessions_for_power(PUBLISHED, ALPHA, CONFIG.target_power)
    assert a == 250
    assert sessions_for_power(QUARTERED, ALPHA, CONFIG.target_power) == 4021


def test_power_is_monotone_in_both_sessions_and_effect_size() -> None:
    assert power_one_sided(REGISTERED, 500, ALPHA) < power_one_sided(
        REGISTERED, 1000, ALPHA
    )
    assert (
        power_one_sided(QUARTERED, 875, ALPHA)
        < power_one_sided(REGISTERED, 875, ALPHA)
        < power_one_sided(PUBLISHED, 875, ALPHA)
    )


def test_power_sits_exactly_on_its_own_minimum_n() -> None:
    """The boundary fixture: at the computed minimum N, power reaches 0.80."""
    for sharpe in (PUBLISHED, REGISTERED, QUARTERED):
        n = sessions_for_power(sharpe, ALPHA, CONFIG.target_power)
        assert power_one_sided(sharpe, n, ALPHA) >= CONFIG.target_power
        assert power_one_sided(sharpe, n - 1, ALPHA) < CONFIG.target_power


# --- E2, which cannot be computed today ----------------------------------


def test_e2_power_is_a_recorded_absence_not_a_number() -> None:
    """Section 9 restricts the dispersion input to the pre-period carve-out."""
    missing = pre_period_dispersion_absent()
    result = e2_power(missing, missing, 17_500, ALPHA)
    assert isinstance(result, Absent)
    assert "pre-period carve-out" in result.detail
    assert "0 of 9 vendors" in result.detail


def test_e2_power_computes_once_a_dispersion_exists() -> None:
    """Pinned so that supplying the input later is a visible change."""
    result = e2_power(4.0, 0.20, 9000, ALPHA)
    assert not isinstance(result, Absent)
    assert 0.0 <= result <= 1.0


def test_a_non_positive_dispersion_is_refused() -> None:
    with pytest.raises(ValueError, match="dispersion must be positive"):
        e2_power(0.0, 1.0, 100, ALPHA)


# --- The per-trade information ratio, and what the prompt's figure hides --


def test_the_prompts_per_trade_ir_embeds_an_unmeasured_trigger_rate() -> None:
    """The prompt states an IR 'near 0.031' for t = 3.0. That is a 53.5 percent
    trigger rate in disguise.

    At 20 names per session over 875 holdout sessions, a trigger rate of 1.00
    gives 17,500 trades and an IR of **0.0227**. The prompt's 0.031 corresponds
    to roughly **9,362 trades**, i.e. a trigger rate near **0.535** — and the
    prompt itself says the trigger rate is *"to be measured rather than
    assumed."* The figure is reported here with the assumption it contains made
    explicit.
    """
    assert information_ratio_for_t(20 * HOLDOUT_N, 3.0) == pytest.approx(
        0.0227, abs=1e-4
    )
    trades_at_031 = int(HOLDOUT_N * 20 * 0.535)
    assert information_ratio_for_t(trades_at_031, 3.0) == pytest.approx(
        0.031, abs=0.0006
    )


def test_the_information_ratio_needs_no_dispersion_input() -> None:
    """Which is why it is computable today while E2's power is not."""
    assert information_ratio_for_t(9000, 3.0) == pytest.approx(3.0 / math.sqrt(9000))


def test_a_non_positive_trade_count_is_refused() -> None:
    with pytest.raises(ValueError, match="trade count must be positive"):
        information_ratio_for_t(0, 3.0)


# --- Amendment 19 — the amended E2, whose null is a pessimistic-cost mean ---

SHIFT_AT_HALF_STOPS = 0.045
"""0.030 on a close exit and 0.060 on a stop, mixed 50/50. Hand-computed."""


def test_the_pessimistic_mean_subtracts_an_absolute_dollar_amount() -> None:
    """It is a shift, not a rescale, and that is the whole point of Amendment 19.

    Under the **old** E2 the implied mean was a fixed multiple of the Sharpe
    assumption, so the dispersion divided out and E2's power equalled E1's. A
    shift in **USD per share** does not divide out, so the measured dispersion
    becomes load-bearing.
    """
    from orb.power import e2_pessimistic_mean

    assert e2_pessimistic_mean(0.08, 0.045) == pytest.approx(0.035, abs=1e-12)
    assert e2_pessimistic_mean(0.02, 0.045) == pytest.approx(-0.025, abs=1e-12)


def test_a_negative_pessimistic_mean_gives_power_below_the_size_of_the_test() -> None:
    """Not an error, not clamped. **The finding is the number.**

    A one-sided test of *"mean <= 0"* cannot reject in favour of a true mean that
    is itself negative more often than by chance, and less often than ``alpha``.
    Clamping to ``alpha`` or to zero would hide exactly what the amendment is
    for.
    """
    from orb.power import e2_power_pessimistic

    power = e2_power_pessimistic(2.0, 0.02, SHIFT_AT_HALF_STOPS, 10_000, 0.05)
    assert isinstance(power, float)
    assert 0.0 < power < 0.05


def test_a_positive_pessimistic_mean_gives_power_above_the_size() -> None:
    from orb.power import e2_power_pessimistic

    power = e2_power_pessimistic(2.0, 0.10, SHIFT_AT_HALF_STOPS, 10_000, 0.05)
    assert isinstance(power, float)
    assert power > 0.05


def test_e2_power_is_monotone_in_the_shift() -> None:
    """A larger pessimistic shift can only reduce power. Never the reverse."""
    from orb.power import e2_power_pessimistic

    powers = [
        e2_power_pessimistic(2.0, 0.10, shift, 10_000, 0.05)
        for shift in (0.0, 0.030, 0.045, 0.060)
    ]
    assert all(isinstance(p, float) for p in powers)
    assert powers == sorted(powers, reverse=True)


def test_no_trade_count_clears_the_target_when_the_mean_is_not_positive() -> None:
    """A recorded absence, never a very large number. The ADR-026 rule."""
    from orb.absence import Absent
    from orb.power import trades_for_e2_power

    absent = trades_for_e2_power(2.0, -0.001, 0.05, 0.80)
    assert isinstance(absent, Absent)
    assert "at or below zero" in absent.detail

    at_zero = trades_for_e2_power(2.0, 0.0, 0.05, 0.80)
    assert isinstance(at_zero, Absent), "zero is inside the null, not outside it"

    reachable = trades_for_e2_power(2.0, 0.04, 0.05, 0.80)
    assert isinstance(reachable, int) and reachable > 0


def test_the_minimum_trade_count_round_trips_against_the_power_function() -> None:
    """The n it returns actually clears the target, and one fewer does not."""
    from orb.power import e2_power_pessimistic, trades_for_e2_power

    dispersion, central, shift = 2.0, 0.10, SHIFT_AT_HALF_STOPS
    pessimistic = central - shift
    needed = trades_for_e2_power(dispersion, pessimistic, 0.05, 0.80)
    assert isinstance(needed, int)

    at_n = e2_power_pessimistic(dispersion, central, shift, needed, 0.05)
    below = e2_power_pessimistic(dispersion, central, shift, needed - 1, 0.05)
    assert isinstance(at_n, float) and isinstance(below, float)
    assert at_n >= 0.80
    assert below < 0.80
