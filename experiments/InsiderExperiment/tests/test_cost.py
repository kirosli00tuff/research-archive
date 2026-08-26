"""The cost band, amortized rather than asserted."""

from __future__ import annotations

import pytest

from insider.config import CONFIG
from insider.cost import hold_months, monthly_cost_drag, net_band_bp_per_month, spread_band_bp


def test_the_measured_band_is_the_one_in_force() -> None:
    assert spread_band_bp() == (15.8, 50.0)
    assert (CONFIG.round_trip_bp_low, CONFIG.round_trip_bp_high) == (32.0, 100.0)


def test_the_six_month_hold_is_six_trading_months() -> None:
    assert hold_months(126) == pytest.approx(6.0)
    assert hold_months(21) == pytest.approx(1.0)
    assert hold_months(63) == pytest.approx(3.0)


def test_a_longer_hold_amortizes_the_round_trip_further() -> None:
    one = monthly_cost_drag(21)
    six = monthly_cost_drag(126)
    assert one.pessimistic_bp_per_month == pytest.approx(100.0)
    assert six.pessimistic_bp_per_month == pytest.approx(16.667, abs=0.01)
    assert six.optimistic_bp_per_month == pytest.approx(5.333, abs=0.01)
    assert six.pessimistic_bp_per_month < one.pessimistic_bp_per_month


def test_the_net_band_at_the_six_month_hold() -> None:
    low, high = net_band_bp_per_month(126)
    assert low == pytest.approx(13.33, abs=0.01)
    assert high == pytest.approx(34.67, abs=0.01)


def test_at_the_one_month_hold_the_pessimistic_cost_eats_the_whole_gross_band() -> None:
    low, high = net_band_bp_per_month(21)
    assert low < 0, "a one-month hold pays the full round trip against a 30 bp gross"
    assert high < CONFIG.decayed_gross_band_bp[1]


def test_a_zero_hold_is_refused_rather_than_dividing() -> None:
    with pytest.raises(ValueError):
        monthly_cost_drag(0)
