"""Section 6 — every component pinned against a hand-computed example.

The arithmetic in each docstring was computed by hand, not by the code under
test. Where a threshold binds, the fixture sits **on** it.
"""

from __future__ import annotations

from datetime import date

import pytest

from orb.absence import Absent
from orb.costs import Band, CostModel, Leg, SecFeeSchedule, Side

# A SYNTHETIC fixture schedule, present only to exercise a rate change across a
# date boundary. **These are not the registered rates.** The registered schedule
# lives in `orb.costs_registered` and currently holds one measured rate with an
# unmeasured effective date, so it returns Absent across the whole registered
# window. Only the 0.0000206 below was measured (IBKR pass-through page,
# 2026-08-29); 0.0000218 is a fixture value chosen to differ from it.
SEC = SecFeeSchedule(
    effective_dates=(date(2016, 1, 4), date(2026, 5, 14)),
    rates_per_dollar=(0.0000218, 0.0000206),
)

MODEL = CostModel(
    commission_per_share=0.0035,
    commission_order_minimum=0.35,
    commission_max_fraction_of_trade_value=0.01,
    finra_taf_per_share_sold=0.000195,
    finra_cat_per_share=0.000003,
    clearing_per_share=0.00020,
    sec_fees=SEC,
    entry_slippage=(0.010, 0.020, 0.040),
    stop_slippage=(0.020, 0.040, 0.080),
    close_slippage=(0.005, 0.010, 0.020),
)

SESSION = date(2026, 6, 1)


# --- Commission -----------------------------------------------------------


def test_commission_is_per_share_above_the_minimum() -> None:
    """500 shares x 0.0035 = 1.75, above the 0.35 minimum, below the 1% cap."""
    assert MODEL.commission(500, 50.00) == pytest.approx(1.75)


def test_the_order_minimum_binds_on_a_small_share_count() -> None:
    """50 shares x 0.0035 = 0.175, below the 0.35 minimum. The minimum wins."""
    assert pytest.approx(0.175) == 50 * 0.0035
    assert MODEL.commission(50, 50.00) == pytest.approx(0.35)


def test_the_order_minimum_sits_exactly_on_its_boundary() -> None:
    """0.35 / 0.0035 = exactly 100 shares. At 100 the two are equal."""
    assert MODEL.commission(100, 50.00) == pytest.approx(0.35)
    assert MODEL.commission(101, 50.00) == pytest.approx(101 * 0.0035)
    assert MODEL.commission(99, 50.00) == pytest.approx(0.35)


def test_the_one_percent_cap_binds_below_the_minimum_on_a_cheap_order() -> None:
    """Measured, not carried: IBKR caps an order at 1% of trade value.

    10 shares at 1.00 USD is a 10.00 USD trade. 1% is 0.10, which is **below**
    the 0.35 minimum, so the cap wins and the minimum does not survive it.
    """
    assert MODEL.commission(10, 1.00) == pytest.approx(0.10)


def test_the_cap_does_not_bind_on_a_normal_order() -> None:
    """500 shares at 50 USD is 25,000; 1% is 250, far above 1.75."""
    assert MODEL.commission(500, 50.00) == pytest.approx(1.75)


def test_a_non_positive_share_count_is_refused() -> None:
    """Integer share counts only, and zero is not a trade."""
    with pytest.raises(ValueError, match="must be positive"):
        MODEL.commission(0, 50.0)
    with pytest.raises(ValueError, match="must be positive"):
        MODEL.commission(-5, 50.0)


# --- Regulatory and clearing ---------------------------------------------


def test_finra_taf_is_charged_per_share_sold() -> None:
    """1,000 shares x 0.000195 = 0.195."""
    assert MODEL.finra_taf(1000) == pytest.approx(0.195)


def test_finra_cat_is_charged_on_every_leg() -> None:
    """1,000 shares x 0.000003 = 0.003."""
    assert MODEL.finra_cat(1000) == pytest.approx(0.003)


def test_clearing_is_charged_per_share() -> None:
    """1,000 shares x 0.00020 = 0.20."""
    assert MODEL.clearing(1000) == pytest.approx(0.20)


# --- The SEC fee, across a rate-change date ------------------------------


def test_the_sec_fee_uses_the_rate_in_force_on_the_session_date() -> None:
    """1,000 shares at 50 USD = 50,000 notional.

    At 0.0000218 that is 1.09; at 0.0000206 it is 1.03. The date decides.
    """
    before = MODEL.sec_fee(1000, 50.00, date(2026, 5, 13))
    after = MODEL.sec_fee(1000, 50.00, date(2026, 5, 14))
    assert before == pytest.approx(1.09)
    assert after == pytest.approx(1.03)
    assert before != after


def test_the_rate_change_date_is_inclusive_of_the_new_rate() -> None:
    """The fixture sits exactly on the effective date, and one day either side."""
    assert MODEL.sec_fees.rate_on(date(2026, 5, 13)) == 0.0000218
    assert MODEL.sec_fees.rate_on(date(2026, 5, 14)) == 0.0000206
    assert MODEL.sec_fees.rate_on(date(2026, 5, 15)) == 0.0000206


def test_a_session_before_the_first_recorded_rate_is_a_recorded_absence() -> None:
    """Never the nearest rate. A fee taken from the wrong year is indefensible."""
    missing = MODEL.sec_fees.rate_on(date(2015, 12, 31))
    assert isinstance(missing, Absent)
    assert "no SEC Section 31 rate recorded" in missing.detail


def test_an_absent_sec_rate_propagates_and_never_becomes_zero() -> None:
    """The whole round trip refuses rather than under-charging the trade."""
    cost = MODEL.round_trip_cost(
        100, 50.0, 51.0, Leg.CLOSE_EXIT, Side.LONG, date(2015, 6, 1)
    )
    assert isinstance(cost, Absent)
    net = MODEL.net_pnl(100, 50.0, 51.0, Leg.CLOSE_EXIT, Side.LONG, date(2015, 6, 1))
    assert isinstance(net, Absent)


def test_an_unsorted_schedule_is_refused_at_construction() -> None:
    with pytest.raises(ValueError, match="sorted ascending"):
        SecFeeSchedule((date(2026, 1, 1), date(2016, 1, 1)), (1.0, 2.0))
    with pytest.raises(ValueError, match="differ in length"):
        SecFeeSchedule((date(2016, 1, 1),), (1.0, 2.0))


# --- Slippage bands -------------------------------------------------------


def test_the_stop_band_is_the_widest_because_a_stop_is_gap_prone() -> None:
    entry = MODEL.slippage_per_share(Leg.ENTRY, Band.CENTRAL)
    stop = MODEL.slippage_per_share(Leg.STOP_EXIT, Band.CENTRAL)
    close = MODEL.slippage_per_share(Leg.CLOSE_EXIT, Band.CENTRAL)
    assert stop > entry > close
    assert (stop, entry, close) == (0.040, 0.020, 0.010)


def test_every_band_is_ordered_optimistic_central_pessimistic() -> None:
    for leg in (Leg.ENTRY, Leg.STOP_EXIT, Leg.CLOSE_EXIT):
        o = MODEL.slippage_per_share(leg, Band.OPTIMISTIC)
        c = MODEL.slippage_per_share(leg, Band.CENTRAL)
        p = MODEL.slippage_per_share(leg, Band.PESSIMISTIC)
        assert o < c < p, leg


def test_the_central_entry_assumption_sits_below_the_measured_break_even() -> None:
    """0.020 against the replication's measured 0.022 USD/share zero-crossing.

    This is the whole experiment in one assertion: the registered central case
    is two-tenths of a cent inside the point where the sibling strategy's net
    PnL crossed zero.
    """
    central = MODEL.slippage_per_share(Leg.ENTRY, Band.CENTRAL)
    replication_break_even = 0.022
    assert central < replication_break_even
    assert replication_break_even - central == pytest.approx(0.002)


# --- The whole round trip, hand-computed ---------------------------------


def test_the_round_trip_cost_is_the_sum_of_its_hand_computed_parts() -> None:
    """1,000 shares, entry 50.00, close exit 51.00, long, 2026-06-01, central.

    commission  = max(1000*0.0035, 0.35) = 3.50, twice          ->  7.000000
    taf         = 1000 * 0.000195                               ->  0.195000
    sec         = 1000 * 51.00 * 0.0000206                      ->  1.050600
    cat         = 2 * 1000 * 0.000003                           ->  0.006000
    clearing    = 2 * 1000 * 0.00020                            ->  0.400000
    slippage    = 1000 * (0.020 + 0.010)                        -> 30.000000
                                                          total -> 38.651600
    """
    cost = MODEL.round_trip_cost(
        1000, 50.00, 51.00, Leg.CLOSE_EXIT, Side.LONG, SESSION, Band.CENTRAL
    )
    assert not isinstance(cost, Absent)
    assert cost == pytest.approx(38.6516)


def test_slippage_dominates_the_round_trip_cost() -> None:
    """30.00 of a 38.65 total. The cost band is the experiment's second axis."""
    cost = MODEL.round_trip_cost(
        1000, 50.00, 51.00, Leg.CLOSE_EXIT, Side.LONG, SESSION, Band.CENTRAL
    )
    assert not isinstance(cost, Absent)
    assert 30.0 / cost > 0.77


def test_a_stop_exit_costs_more_than_a_close_exit() -> None:
    stop = MODEL.round_trip_cost(
        1000, 50.00, 49.00, Leg.STOP_EXIT, Side.LONG, SESSION, Band.CENTRAL
    )
    close = MODEL.round_trip_cost(
        1000, 50.00, 49.00, Leg.CLOSE_EXIT, Side.LONG, SESSION, Band.CENTRAL
    )
    assert not isinstance(stop, Absent)
    assert not isinstance(close, Absent)
    assert stop - close == pytest.approx(1000 * (0.040 - 0.010))


def test_the_optimistic_band_is_an_upper_bound_of_optimism() -> None:
    opt = MODEL.round_trip_cost(
        1000, 50.0, 51.0, Leg.CLOSE_EXIT, Side.LONG, SESSION, Band.OPTIMISTIC
    )
    pes = MODEL.round_trip_cost(
        1000, 50.0, 51.0, Leg.CLOSE_EXIT, Side.LONG, SESSION, Band.PESSIMISTIC
    )
    assert not isinstance(opt, Absent)
    assert not isinstance(pes, Absent)
    assert opt < pes
    assert pes - opt == pytest.approx(1000 * ((0.040 + 0.020) - (0.010 + 0.005)))


# --- Section 5, the sign convention --------------------------------------


def test_a_positive_number_is_a_gain_for_a_long() -> None:
    """1,000 shares, 50.00 -> 51.00 = 1,000 gross, minus 38.6516."""
    net = MODEL.net_pnl(1000, 50.00, 51.00, Leg.CLOSE_EXIT, Side.LONG, SESSION)
    assert not isinstance(net, Absent)
    assert net == pytest.approx(1000.0 - 38.6516)


def test_a_positive_number_is_a_gain_for_a_short() -> None:
    """A short entered at 51.00 and covered at 50.00 gains 1,000 gross."""
    net = MODEL.net_pnl(1000, 51.00, 50.00, Leg.CLOSE_EXIT, Side.SHORT, SESSION)
    assert not isinstance(net, Absent)
    assert net > 0
    assert net == pytest.approx(1000.0 - 38.6516, abs=0.02)


def test_a_losing_long_and_a_losing_short_are_both_negative() -> None:
    long_loss = MODEL.net_pnl(100, 50.0, 49.0, Leg.STOP_EXIT, Side.LONG, SESSION)
    short_loss = MODEL.net_pnl(100, 50.0, 51.0, Leg.STOP_EXIT, Side.SHORT, SESSION)
    assert not isinstance(long_loss, Absent)
    assert not isinstance(short_loss, Absent)
    assert long_loss < 0
    assert short_loss < 0


def test_the_sec_fee_is_charged_on_the_sell_leg_of_a_short_too() -> None:
    """A short sells first. The fee follows the sale, not the calendar order."""
    long_cost = MODEL.round_trip_cost(
        1000, 50.0, 60.0, Leg.CLOSE_EXIT, Side.LONG, SESSION
    )
    short_cost = MODEL.round_trip_cost(
        1000, 50.0, 60.0, Leg.CLOSE_EXIT, Side.SHORT, SESSION
    )
    assert not isinstance(long_cost, Absent)
    assert not isinstance(short_cost, Absent)
    # The long sells at 60, the short sells at 50: the SEC fee differs.
    assert long_cost - short_cost == pytest.approx(1000 * 10.0 * 0.0000206)


def test_the_entry_leg_cannot_be_an_exit() -> None:
    with pytest.raises(ValueError, match="stop exit or a close exit"):
        MODEL.round_trip_cost(100, 50.0, 51.0, Leg.ENTRY, Side.LONG, SESSION)


# --- The registered instance, and the deviations it records ---------------


def test_the_registered_model_carries_only_measured_figures() -> None:
    from orb.costs_registered import MEASURED_AGAINST_CARRIED, REGISTERED_COST_MODEL

    assert REGISTERED_COST_MODEL.commission_per_share == 0.0035
    assert REGISTERED_COST_MODEL.commission_order_minimum == 0.35
    assert REGISTERED_COST_MODEL.finra_taf_per_share_sold == 0.000195
    assert REGISTERED_COST_MODEL.clearing_per_share == 0.00020
    assert REGISTERED_COST_MODEL.finra_cat_per_share == 0.000003
    assert REGISTERED_COST_MODEL.commission_max_fraction_of_trade_value == 0.01
    assert MEASURED_AGAINST_CARRIED["finra_taf_per_share_sold"][2] == (
        "CARRIED FIGURE IS STALE"
    )


def test_the_carried_taf_rate_is_stale_by_a_measurable_amount() -> None:
    """Carried 0.000166 against measured 0.000195: the carried figure is 14.9% low."""
    carried, measured, _ = __import__(
        "orb.costs_registered", fromlist=["x"]
    ).MEASURED_AGAINST_CARRIED["finra_taf_per_share_sold"]
    assert carried == 0.000166
    assert measured == 0.000195
    assert (measured - carried) / measured == pytest.approx(0.1487, abs=0.001)


def test_the_registered_model_refuses_every_session_in_the_window() -> None:
    """The SEC schedule is empty on purpose: no effective date was measured.

    The model refuses to price a trade rather than take a 2026 fee rate and
    apply it to a 2016 session. This test pins the refusal, so that populating
    the schedule later is a visible change rather than a silent one.
    """
    from orb.costs_registered import REGISTERED_COST_MODEL

    for session in (date(2016, 1, 4), date(2022, 12, 30), date(2026, 6, 30)):
        cost = REGISTERED_COST_MODEL.round_trip_cost(
            100, 50.0, 51.0, Leg.CLOSE_EXIT, Side.LONG, session
        )
        assert isinstance(cost, Absent), session
        assert "no SEC Section 31 rate recorded" in cost.detail


def test_the_frozen_hash_matches_the_registered_model() -> None:
    """The latch is the model. If the model moves, this fails loudly."""
    import json
    from pathlib import Path

    from tools_freeze import canonical_for_test

    latch = Path(__file__).resolve().parent.parent / "data/state/cost_model_latch.json"
    if not latch.exists():
        pytest.skip("cost model not yet frozen in this tree")
    recorded = json.loads(latch.read_text())["sha256"]
    assert canonical_for_test() == recorded
