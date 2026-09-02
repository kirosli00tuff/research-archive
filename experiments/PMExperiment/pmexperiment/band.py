"""The fee-versus-edge band. It reads registered constants, and no venue.

REGISTRATION.md Amendment 2 defines the gate this module fires, Amendment 3
orders it ahead of the power gate, and Amendment 4 registers the FX turnover it
charges. The gate is free — it reads published effect magnitudes and the fee
schedule and nothing else — so it can be decisive before a single contract is
enumerated.

No request leaves this module, and no field carrying a market's resolution
enters it. tests/test_guards.py scans it beside power.py and fails if one
appears; that guard is verified by mutation.
"""

from __future__ import annotations

from enum import Enum

from pmexperiment import registry


class ExitRoute(Enum):
    """Amendment 2's two routes. They differ only in fee sides borne."""

    HELD_TO_RESOLUTION = 1
    EXITED_BEFORE_RESOLUTION = 2

    @property
    def fee_sides(self) -> int:
        """One side when held to settlement; both sides on an early exit."""
        return int(self.value)


class BandVerdict(Enum):
    """The registered verdict rows of REGISTRATION.md Amendment 2."""

    BAND_EMPTY = "BAND-EMPTY"
    BAND_NARROW = "BAND-NARROW"
    BAND_OPEN = "BAND-OPEN"


def _check_entry_price(entry_price: float) -> None:
    if not 0.0 < entry_price < 1.0:
        raise ValueError("entry price must sit strictly inside (0, 1) dollars")


def fee_borne(route: ExitRoute) -> float:
    """Venue fee at the registered $0.02 per contract per side."""
    return registry.FEE_PER_SIDE_USD * route.fee_sides


def fx_cost(
    entry_price: float, turnover: float = registry.FX_TURNOVER_REGISTERED
) -> float:
    """The registered FX, shared across the deployments one conversion funds.

    Amendment 4: the schedule charges on currency conversion, not on trades,
    so the per-contract share is the round-trip rate over the turnover. An
    infinite turnover returns exactly zero — the limit no amortization can
    beat, carried so the verdict can be tested against it.
    """
    _check_entry_price(entry_price)
    if turnover < 1.0:
        raise ValueError("turnover below 1 deploys principal it never converted")
    round_trip = registry.FX_PER_DIRECTION * registry.FX_DIRECTIONS
    return round_trip * entry_price / turnover


def required_underpricing(
    entry_price: float,
    route: ExitRoute,
    turnover: float = registry.FX_TURNOVER_REGISTERED,
) -> float:
    """Break-even edge: the true probability must exceed the price by this.

    A contract pays $1.00 on correct resolution and $0.00 otherwise, so the fee
    is flat in cents while the FX scales with price. Section 11's registered
    cost floor C(p) is this function on the round-trip route at turnover 1.
    """
    _check_entry_price(entry_price)
    return fee_borne(route) + registry.HALF_SPREAD_USD + fx_cost(entry_price, turnover)


def band_top_exceeds_requirement(
    entry_price: float,
    route: ExitRoute,
    turnover: float = registry.FX_TURNOVER_REGISTERED,
) -> bool:
    """Could an effect anywhere in the registered band survive at this price?

    Amendment 2 fixes the quantifier in its own rationale: the gate fires
    BAND-EMPTY when there is "no price region where a documented effect could
    survive". The test is therefore existential over the band, judged at its
    top. The strict alternative below is reported beside it, so the quantifier
    is visible rather than buried in a comparison operator.
    """
    return required_underpricing(entry_price, route, turnover) < registry.EFFECT_BAND_HI


def band_bottom_exceeds_requirement(
    entry_price: float,
    route: ExitRoute,
    turnover: float = registry.FX_TURNOVER_REGISTERED,
) -> bool:
    """Would every effect in the registered band survive here? Not the fired test."""
    return required_underpricing(entry_price, route, turnover) < registry.EFFECT_BAND_LO


def bucket_midpoint(bucket: tuple[int, int]) -> float:
    """The representative price of a registered decile, in dollars."""
    low_cents, high_cents = bucket
    return (low_cents + high_cents) / 200.0


def surviving_buckets(
    route: ExitRoute, turnover: float = registry.FX_TURNOVER_REGISTERED
) -> tuple[tuple[int, int], ...]:
    """Registered deciles where an effect in the band could clear the cost."""
    return tuple(
        bucket
        for bucket in registry.BUCKET_EDGES_CENTS
        if band_top_exceeds_requirement(bucket_midpoint(bucket), route, turnover)
    )


def is_band_empty(
    route: ExitRoute, turnover: float = registry.FX_TURNOVER_REGISTERED
) -> bool:
    """Amendment 2's BAND-EMPTY row: no bucket where the band clears the cost.

    BAND-NARROW and BAND-OPEN are deliberately not derived here. They turn on
    whether the surviving region is populated inside the permitted categories,
    which is a count this stage may not read (Sections 4 and 10). Encoding that
    judgement as arithmetic would dress it up as a measurement.
    """
    return surviving_buckets(route, turnover) == ()
