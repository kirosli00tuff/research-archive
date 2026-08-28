"""The benchmark matches the recorded definition on a fixed fixture."""
import pytest

from hfexperiment.benchmark import benchmark_daily_return
from hfexperiment.shadow import advance_panel, initial_panel
from hfexperiment.states import AccrualState


def test_benchmark_is_the_equal_weighted_mean_daily_return() -> None:
    # The recorded definition, REGISTRATION.md Section 1: the
    # equal-weighted mean daily return of the formation universe
    # membership. Arithmetic mean, every member weighted identically.
    returns = {"A": 0.01, "B": -0.02, "C": 0.04}
    assert benchmark_daily_return(returns) == pytest.approx(0.01)


def test_marked_members_stay_in_the_denominator_at_zero() -> None:
    # A halted or delisted member marks at its last close: zero return,
    # still a member until the next formation.
    returns = {"A": 0.03, "B": 0.0}
    assert benchmark_daily_return(returns) == pytest.approx(0.015)


def test_empty_membership_is_an_error_not_a_zero() -> None:
    with pytest.raises(ValueError):
        benchmark_daily_return({})


def test_full_construction_through_the_panel_on_a_fixed_fixture() -> None:
    # Arrange: four members, one delisted mid-month.
    panel = initial_panel(
        "2026-09-01",
        ["A", "B", "C", "D"],
        {"A": 100.0, "B": 50.0, "C": 20.0, "D": 10.0},
    )
    states = {
        "A": AccrualState.COMPUTED,
        "B": AccrualState.COMPUTED,
        "C": AccrualState.COMPUTED,
        "D": AccrualState.DELISTED,
    }
    closes = {"A": 102.0, "B": 49.0, "C": 20.0}
    # Act.
    day = advance_panel(panel, "2026-09-02", states, closes)
    mean = benchmark_daily_return(day.member_returns)
    # Assert: (0.02 - 0.02 + 0.0 + 0.0) / 4.
    assert mean == pytest.approx(0.0)
    assert len(day.member_returns) == 4
