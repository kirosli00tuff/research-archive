"""The power gate arithmetic, pinned to hand-computed values.

Boundary cases matter most: REGISTRATION.md Section 0.3 makes the band edges
inclusive at the lower edge, and Section 0.4 derives the planning counts 475
and 30 at the planning dispersion 0.0475. These tests hold the code to those
exact figures.
"""

import math

import pytest

from pmexperiment import registry
from pmexperiment.power import (
    Verdict,
    cost_floor,
    fire_power_gate,
    minimum_detectable_effect,
)

PLANNING_DISPERSION = 0.0475  # p(1-p) at the 5c / 95c tail


def test_mde_matches_hand_computation() -> None:
    # Arrange: n = 100, v = 0.0475 -> 2 * sqrt(0.000475) = 0.0435889...
    expected = 2.0 * math.sqrt(PLANNING_DISPERSION / 100)

    # Act
    mde = minimum_detectable_effect(100, PLANNING_DISPERSION)

    # Assert
    assert mde is not None
    assert mde == pytest.approx(expected)
    assert mde == pytest.approx(0.043589, abs=1e-6)


def test_go_boundary_is_inclusive_at_475_tail_contracts() -> None:
    # 0.0475 / 475 = 1e-4 exactly, so MDE = 2 * 0.01 = 0.02 exactly: GO.
    reading = fire_power_gate("U24", 475, PLANNING_DISPERSION)
    assert reading.mde == pytest.approx(registry.EFFECT_BAND_LO)
    assert reading.verdict is Verdict.GO


def test_one_contract_below_the_go_planning_count_is_degraded() -> None:
    reading = fire_power_gate("U24", 474, PLANNING_DISPERSION)
    assert reading.mde is not None
    assert reading.mde > registry.EFFECT_BAND_LO
    assert reading.verdict is Verdict.DEGRADED


def test_degraded_holds_at_30_tail_contracts() -> None:
    reading = fire_power_gate("P30", 30, PLANNING_DISPERSION)
    assert reading.mde is not None
    assert reading.mde <= registry.EFFECT_BAND_HI
    assert reading.verdict is Verdict.DEGRADED


def test_blocked_fires_at_29_tail_contracts() -> None:
    reading = fire_power_gate("P30", 29, PLANNING_DISPERSION)
    assert reading.mde is not None
    assert reading.mde > registry.EFFECT_BAND_HI
    assert reading.verdict is Verdict.BLOCKED


def test_an_empty_cell_is_blocked_with_no_mde() -> None:
    reading = fire_power_gate("P30", 0, PLANNING_DISPERSION)
    assert reading.mde is None
    assert reading.verdict is Verdict.BLOCKED


def test_a_nonempty_cell_with_zero_dispersion_refuses() -> None:
    with pytest.raises(ValueError):
        minimum_detectable_effect(10, 0.0)


def test_cost_floor_matches_the_registered_schedule() -> None:
    # Section 11: C(p) = 0.05 + 0.03 p; C(0.95) = 0.0785, C(0.05) = 0.0515.
    assert cost_floor(0.95) == pytest.approx(0.0785)
    assert cost_floor(0.05) == pytest.approx(0.0515)


def test_cost_floor_refuses_prices_outside_the_open_interval() -> None:
    for bad in (0.0, 1.0, -0.1, 1.5):
        with pytest.raises(ValueError):
            cost_floor(bad)
