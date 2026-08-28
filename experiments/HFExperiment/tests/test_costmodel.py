"""The three billing regimes stay correct and stay apart."""
import pytest

from hfexperiment.costmodel import (
    UNMEASURED_SPREAD_BP,
    Regime,
    annual_commission_drag,
    daily_cost_hurdle_bp,
    liquidity_tier,
    regime_commission,
    round_trip,
    tick_multiple_spread_bp,
)

SHARE_PRICE = 103.25  # measured median mid of the width-20 book
NOTIONALS = (30.0, 45.0, 70.0, 100.0, 180.0)


def shares_for(value: float) -> float:
    return value / SHARE_PRICE


class TestRegimeDispatch:
    def test_tiered_cap_below_minimum_branch(self) -> None:
        for value, expected in ((30.0, 0.15), (45.0, 0.225)):
            r = regime_commission(Regime.WHOLE_TIERED, shares_for(value), value)
            assert r.binding == "cap"
            assert r.amount_usd == pytest.approx(expected)

    def test_tiered_minimum_above_crossover(self) -> None:
        for value in (100.0, 180.0):
            r = regime_commission(Regime.WHOLE_TIERED, shares_for(value), value)
            assert r.binding == "minimum"
            assert r.amount_usd == pytest.approx(0.35)

    def test_fixed_cap_below_minimum_branch(self) -> None:
        for value, expected in ((30.0, 0.30), (45.0, 0.45), (70.0, 0.70)):
            r = regime_commission(Regime.WHOLE_FIXED, shares_for(value), value)
            assert r.binding == "cap"
            assert r.amount_usd == pytest.approx(expected)

    def test_fixed_minimum_above_crossover(self) -> None:
        for value in (100.0, 180.0):
            r = regime_commission(Regime.WHOLE_FIXED, shares_for(value), value)
            assert r.binding == "minimum"
            assert r.amount_usd == pytest.approx(1.00)

    def test_fractional_is_flat_one_percent_everywhere(self) -> None:
        for value in NOTIONALS:
            r = regime_commission(Regime.FRACTIONAL, shares_for(value), value)
            assert r.binding == "fractional_1pct"
            assert r.amount_usd == pytest.approx(value * 0.01)
            assert r.amount_usd / value * 1e4 == pytest.approx(100.0)


class TestRegimesNeverBlend:
    """Collapsing the fractional regime into Tiered must fail here."""

    def test_fractional_differs_from_tiered_at_every_notional(self) -> None:
        for value in NOTIONALS:
            frac = regime_commission(Regime.FRACTIONAL, shares_for(value), value)
            tier = regime_commission(
                Regime.WHOLE_TIERED, shares_for(value), value
            )
            assert frac.amount_usd != pytest.approx(tier.amount_usd)
            assert frac.binding != tier.binding

    def test_fractional_has_no_size_relief(self) -> None:
        small = regime_commission(Regime.FRACTIONAL, shares_for(30.0), 30.0)
        large = regime_commission(Regime.FRACTIONAL, shares_for(180.0), 180.0)
        assert small.amount_usd / 30.0 == pytest.approx(large.amount_usd / 180.0)

    def test_tiered_has_size_relief_where_fractional_does_not(self) -> None:
        tier = regime_commission(Regime.WHOLE_TIERED, shares_for(180.0), 180.0)
        assert tier.amount_usd / 180.0 * 1e4 == pytest.approx(19.44, abs=0.01)


class TestRoundTrip:
    def test_terms_report_separately_and_sum(self) -> None:
        rt = round_trip(Regime.WHOLE_TIERED, 45.0, SHARE_PRICE, 12.77)
        assert rt.total_rt_bp == pytest.approx(
            rt.commission_rt_bp + rt.regulatory_bp + rt.spread_rt_bp
        )
        assert rt.spread_measured

    def test_unmeasured_spread_carries_band_upper_bound(self) -> None:
        rt = round_trip(Regime.FRACTIONAL, 45.0, SHARE_PRICE, None)
        assert not rt.spread_measured
        assert rt.spread_bp == UNMEASURED_SPREAD_BP == 50.0

    def test_rejects_nonpositive_inputs(self) -> None:
        with pytest.raises(ValueError):
            round_trip(Regime.FRACTIONAL, 0.0, SHARE_PRICE, None)
        with pytest.raises(ValueError):
            round_trip(Regime.FRACTIONAL, 45.0, 0.0, None)


class TestAnnualDrag:
    def test_width20_tiered_at_measured_churn(self) -> None:
        d = annual_commission_drag(
            Regime.WHOLE_TIERED, 20, 5.2, 900.0, SHARE_PRICE
        )
        assert d.fills_per_month == pytest.approx(10.4)
        assert d.commission_usd == pytest.approx(10.4 * 12 * 0.225)

    def test_width5_fractional_at_measured_churn(self) -> None:
        d = annual_commission_drag(
            Regime.FRACTIONAL, 5, 2.0, 900.0, SHARE_PRICE
        )
        assert d.fills_per_month == pytest.approx(4.0)
        assert d.commission_usd == pytest.approx(4.0 * 12 * 1.80)

    def test_rejects_bad_width(self) -> None:
        with pytest.raises(ValueError):
            annual_commission_drag(Regime.FRACTIONAL, 0, 2.0, 900.0, 100.0)


class TestSpreadFallback:
    def test_liquidity_tiers_partition_adv(self) -> None:
        assert liquidity_tier(300e6) == 1
        assert liquidity_tier(70e6) == 2
        assert liquidity_tier(20e6) == 3
        assert liquidity_tier(5e6) == 4
        assert liquidity_tier(300e3) == 5
        assert liquidity_tier(100e3) == 6

    def test_measured_tier_multiples_apply(self) -> None:
        assert tick_multiple_spread_bp(45.0, 20e6) == pytest.approx(
            0.08 / 45.0 * 1e4
        )
        assert tick_multiple_spread_bp(45.0, 5e6) == pytest.approx(
            0.09 / 45.0 * 1e4
        )

    def test_unknown_liquidity_carries_upper_bound(self) -> None:
        assert tick_multiple_spread_bp(45.0, 0.0) == UNMEASURED_SPREAD_BP


class TestHurdle:
    def test_registered_hurdle_arithmetic(self) -> None:
        assert daily_cost_hurdle_bp(5, 2.0, 213.84) == pytest.approx(
            4.07, abs=0.005
        )

    def test_rejects_bad_inputs(self) -> None:
        with pytest.raises(ValueError):
            daily_cost_hurdle_bp(0, 2.0, 200.0)
