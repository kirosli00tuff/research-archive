"""The commission function honours the cap-below-minimum rule."""
import pytest

from hfexperiment.commission import (
    FIXED,
    TIERED,
    commission,
    crossover_notional_usd,
    fractional_commission,
    sell_leg_regulatory,
)

SHARE_PRICE = 45.0


def shares_for(value: float) -> float:
    return value / SHARE_PRICE


def test_tiered_cap_binds_below_crossover() -> None:
    for value, expected in ((30.0, 0.15), (45.0, 0.225)):
        result = commission(TIERED, shares_for(value), value)
        assert result.binding == "cap"
        assert result.amount_usd == pytest.approx(expected)


def test_tiered_crossover_at_seventy() -> None:
    result = commission(TIERED, shares_for(70.0), 70.0)
    assert result.amount_usd == pytest.approx(0.35)


def test_tiered_minimum_binds_above_crossover() -> None:
    result = commission(TIERED, shares_for(100.0), 100.0)
    assert result.binding == "minimum"
    assert result.amount_usd == pytest.approx(0.35)


def test_fixed_cap_binds_below_crossover() -> None:
    for value, expected in ((30.0, 0.30), (45.0, 0.45), (70.0, 0.70)):
        result = commission(FIXED, shares_for(value), value)
        assert result.binding == "cap"
        assert result.amount_usd == pytest.approx(expected)


def test_fixed_crossover_at_one_hundred() -> None:
    result = commission(FIXED, shares_for(100.0), 100.0)
    assert result.amount_usd == pytest.approx(1.00)


def test_crossovers_derive_from_plan_figures() -> None:
    assert crossover_notional_usd(TIERED) == pytest.approx(70.0)
    assert crossover_notional_usd(FIXED) == pytest.approx(100.0)


def test_fractional_schedule_is_one_percent_with_penny_floor() -> None:
    assert fractional_commission(45.0) == pytest.approx(0.45)
    assert fractional_commission(0.75) == pytest.approx(0.01)


def test_sell_leg_holds_worst_case_taf_floor() -> None:
    fees = sell_leg_regulatory(1.0, 45.0)
    assert fees.taf_usd == pytest.approx(0.01)
    assert fees.sec_usd == pytest.approx(45.0 * 0.0000206)


def test_rejects_nonpositive_inputs() -> None:
    with pytest.raises(ValueError):
        commission(TIERED, 0.0, 45.0)
    with pytest.raises(ValueError):
        fractional_commission(0.0)
