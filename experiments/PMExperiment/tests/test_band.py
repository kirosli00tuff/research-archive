"""The fee-versus-edge band, pinned to REGISTRATION.md Amendments 2 and 4.

Written before `pmexperiment/band.py` existed, so the module was implemented
against these assertions rather than the assertions against the module.

Two cross-checks carry the weight. The first pins the new module to the cost
floor the registration already published: `required_underpricing` on the
round-trip route at turnover 1 must equal `power.cost_floor` exactly, and must
land on the two values Section 11 states in prose — C(0.95) = 0.0785 and
C(0.05) = 0.0515. A band module that could not reproduce the registered floor
would be computing something the registration never sanctioned. The second
pins the fired verdict's own figures, so a later session cannot move the
surviving region without a failing test.
"""

import math

import pytest

from pmexperiment import band, power, registry

# The two registered anchor prices of REGISTRATION.md Section 11.
FAVOURITE_TAIL = 0.95
LONGSHOT_TAIL = 0.05

# Bürgi-Deng-Whelan's 95c contract is recorded as winning 98% of the time.
FAVOURITE_TAIL_REALIZED = 0.98


def test_round_trip_route_reproduces_the_registered_cost_floor() -> None:
    """Section 11: C(p) = 0.05 + 0.03p, with C(0.95) and C(0.05) stated."""
    for price in (0.01, 0.05, 0.25, 0.5, 0.755, 0.95, 0.99):
        assert band.required_underpricing(
            price, band.ExitRoute.EXITED_BEFORE_RESOLUTION, turnover=1.0
        ) == pytest.approx(power.cost_floor(price))
    assert band.required_underpricing(
        FAVOURITE_TAIL, band.ExitRoute.EXITED_BEFORE_RESOLUTION, turnover=1.0
    ) == pytest.approx(0.0785)
    assert band.required_underpricing(
        LONGSHOT_TAIL, band.ExitRoute.EXITED_BEFORE_RESOLUTION, turnover=1.0
    ) == pytest.approx(0.0515)


def test_the_two_routes_differ_by_exactly_one_side_of_fee() -> None:
    """Amendment 2: held to resolution bears one fee, an early exit bears two."""
    for price in (0.05, 0.5, 0.95):
        held = band.required_underpricing(
            price, band.ExitRoute.HELD_TO_RESOLUTION, turnover=1.0
        )
        exited = band.required_underpricing(
            price, band.ExitRoute.EXITED_BEFORE_RESOLUTION, turnover=1.0
        )
        assert exited - held == pytest.approx(registry.FEE_PER_SIDE_USD)


def test_held_route_at_the_favourite_tail_is_the_registered_figure() -> None:
    assert band.required_underpricing(
        FAVOURITE_TAIL, band.ExitRoute.HELD_TO_RESOLUTION, turnover=1.0
    ) == pytest.approx(0.0585)


def test_fx_amortizes_with_turnover_and_vanishes_in_the_limit() -> None:
    """Amendment 4: FX is a conversion cost, so it divides by deployments."""
    single = band.fx_cost(FAVOURITE_TAIL, turnover=1.0)
    assert single == pytest.approx(0.0285)
    assert band.fx_cost(FAVOURITE_TAIL, turnover=12.0) == pytest.approx(single / 12)
    assert band.fx_cost(FAVOURITE_TAIL, turnover=math.inf) == 0.0


def test_turnover_below_one_is_rejected() -> None:
    """Principal cannot be deployed less than once and still be converted."""
    with pytest.raises(ValueError, match="turnover"):
        band.fx_cost(FAVOURITE_TAIL, turnover=0.5)


def test_entry_price_must_sit_strictly_inside_the_dollar() -> None:
    for bad in (0.0, 1.0, -0.1, 1.5):
        with pytest.raises(ValueError, match="entry price"):
            band.required_underpricing(
                bad, band.ExitRoute.HELD_TO_RESOLUTION, turnover=1.0
            )


def test_fee_and_spread_alone_already_exceed_the_bottom_of_the_band() -> None:
    """The decisive crossing: a 3.0-point floor against a 2.0-point band edge.

    With FX driven to zero — a limit no amortization can beat — the held route
    still requires 0.03. The registered band's bottom is 0.02. An effect at the
    bottom of the band is therefore unexploitable at every price on every
    route, and no FX argument reaches it.
    """
    floor = band.required_underpricing(
        FAVOURITE_TAIL, band.ExitRoute.HELD_TO_RESOLUTION, turnover=math.inf
    )
    assert floor == pytest.approx(0.03)
    assert floor > registry.EFFECT_BAND_LO


def test_band_bottom_survives_at_no_bucket_on_either_route() -> None:
    """The strict reading of Amendment 2, reported beside the fired one."""
    for bucket in registry.BUCKET_EDGES_CENTS:
        price = band.bucket_midpoint(bucket)
        for route in band.ExitRoute:
            for turnover in (1.0, 12.0, math.inf):
                assert not band.band_bottom_exceeds_requirement(
                    price, route, turnover=turnover
                )


def test_band_top_survives_at_every_bucket_on_both_routes() -> None:
    """Pass 1 of Task 4: the cost curve never rises through the band's top."""
    for bucket in registry.BUCKET_EDGES_CENTS:
        price = band.bucket_midpoint(bucket)
        for route in band.ExitRoute:
            for turnover in (1.0, 12.0, math.inf):
                assert band.band_top_exceeds_requirement(
                    price, route, turnover=turnover
                )


def test_the_published_favourite_tail_magnitudes_do_not_survive() -> None:
    """Bürgi's own 2- and 3-point gaps fail the held route at turnover 1.

    The band's top survives; the specific magnitudes any cited source places at
    this bucket do not. That gap is the finding, and it must stay visible.
    """
    required = band.required_underpricing(
        FAVOURITE_TAIL, band.ExitRoute.HELD_TO_RESOLUTION, turnover=1.0
    )
    for published_gap in (0.02, 0.03):
        assert published_gap < required


def _registered_understatement(fee_sides: int) -> float:
    """How much Section 2's FX base understates cost at the favourite tail.

    Two registered simplifications, both leaning toward H1: the conversion base
    is the entry price, which excludes the fee and half-spread; and the exit
    conversion is valued at the entry price rather than at the $1.00 a winning
    contract returns.
    """
    excluded_base = registry.FEE_PER_SIDE_USD * fee_sides + registry.HALF_SPREAD_USD
    return (
        registry.FX_PER_DIRECTION * registry.FX_DIRECTIONS * excluded_base
        + registry.FX_PER_DIRECTION * (FAVOURITE_TAIL_REALIZED - FAVOURITE_TAIL)
    )


def test_round_trip_margin_at_favourite_tail_sits_inside_its_own_slack() -> None:
    """Route X clears the band top by less than its own registered slack.

    0.0015 of margin against 0.00195 of understatement, so this route's
    survival at the favourite tail is not robust. The fired region excludes it.
    """
    margin = registry.EFFECT_BAND_HI - band.required_underpricing(
        FAVOURITE_TAIL, band.ExitRoute.EXITED_BEFORE_RESOLUTION, turnover=1.0
    )
    assert margin == pytest.approx(0.0015)
    understatement = _registered_understatement(registry.FEE_SIDES)
    assert understatement == pytest.approx(0.00195)
    assert understatement > margin


def test_held_route_margin_is_robust_to_the_same_slack() -> None:
    """2.15 points of margin against 0.135 — the region the power gate inherits."""
    margin = registry.EFFECT_BAND_HI - band.required_underpricing(
        FAVOURITE_TAIL, band.ExitRoute.HELD_TO_RESOLUTION, turnover=1.0
    )
    assert margin == pytest.approx(0.0215)
    understatement = _registered_understatement(1)
    assert understatement == pytest.approx(0.00135)
    assert margin > 10 * understatement


def test_bucket_midpoints_follow_the_registered_edges() -> None:
    assert band.bucket_midpoint((1, 10)) == pytest.approx(0.055)
    assert band.bucket_midpoint((91, 99)) == pytest.approx(0.95)
    for lo, hi in registry.BUCKET_EDGES_CENTS:
        assert band.bucket_midpoint((lo, hi)) == pytest.approx((lo + hi) / 200.0)


def test_the_registered_turnover_is_one() -> None:
    """Amendment 4 registers k = 1 as binding; k > 1 is reported beside it."""
    assert registry.FX_TURNOVER_REGISTERED == 1.0
