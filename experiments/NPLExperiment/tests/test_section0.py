"""The Section 0 fire function. Every branch, boundary fixtures on the boundary.

The InsiderExperiment lesson: a fixture comfortably inside its boundary lets a
moved threshold pass unnoticed. Every power fixture here sits exactly on a
registered floor.
"""

from __future__ import annotations

import pytest

from npl.config import CONFIG
from npl.section0 import (
    CoPrimaryPowers,
    DelistingObservability,
    Section0Verdict,
    fire_section0,
)

FULL_STRONG = CoPrimaryPowers(p1=0.95, p2=0.90, p3=0.85)
FWD_STRONG = CoPrimaryPowers(p1=0.90, p2=0.85, p3=0.80)


def test_the_registered_floors_are_the_prompt_floors() -> None:
    assert CONFIG.power_go_floor == 0.80
    assert CONFIG.power_blocked_floor == 0.50


def test_go_requires_full_delisting_pass_and_all_powers_at_the_floor() -> None:
    # The weakest co-primary sits exactly on 0.80: "at least 80 percent" is GO.
    gate = fire_section0(
        powers_full=CoPrimaryPowers(p1=0.99, p2=0.80, p3=0.92),
        powers_forward_only=FWD_STRONG,
        delisting=DelistingObservability.PASS,
        listing_dates_inferable=True,
        funding_retention_ok=True,
    )
    assert gate.verdict is Section0Verdict.GO
    assert gate.cohort_basis == "retro_plus_forward"
    assert gate.collectors_armed


def test_a_power_between_the_floors_fires_degraded() -> None:
    # Exactly 0.50 is not "under 50 percent", so it is DEGRADED, not BLOCKED.
    gate = fire_section0(
        powers_full=CoPrimaryPowers(p1=0.99, p2=0.50, p3=0.92),
        powers_forward_only=FWD_STRONG,
        delisting=DelistingObservability.PASS,
        listing_dates_inferable=True,
        funding_retention_ok=True,
    )
    assert gate.verdict is Section0Verdict.DEGRADED
    assert gate.collectors_armed


def test_a_power_under_half_fires_blocked_and_arms_nothing() -> None:
    gate = fire_section0(
        powers_full=CoPrimaryPowers(p1=0.99, p2=0.4999, p3=0.92),
        powers_forward_only=FWD_STRONG,
        delisting=DelistingObservability.PASS,
        listing_dates_inferable=True,
        funding_retention_ok=True,
    )
    assert gate.verdict is Section0Verdict.BLOCKED
    assert not gate.collectors_armed


def test_partial_delisting_demotes_retro_and_reads_forward_powers() -> None:
    # Full-cohort powers are strong; the forward-only cohort carries the
    # verdict, and even at 0.80 everywhere the verdict is DEGRADED, not GO.
    gate = fire_section0(
        powers_full=FULL_STRONG,
        powers_forward_only=CoPrimaryPowers(p1=0.80, p2=0.80, p3=0.80),
        delisting=DelistingObservability.PARTIAL,
        listing_dates_inferable=True,
        funding_retention_ok=True,
    )
    assert gate.verdict is Section0Verdict.DEGRADED
    assert gate.cohort_basis == "forward_only"
    assert "descriptive" in gate.rationale


def test_delisting_fail_also_reads_forward_powers_and_can_block() -> None:
    gate = fire_section0(
        powers_full=FULL_STRONG,
        powers_forward_only=CoPrimaryPowers(p1=0.49, p2=0.80, p3=0.80),
        delisting=DelistingObservability.FAIL,
        listing_dates_inferable=True,
        funding_retention_ok=True,
    )
    assert gate.verdict is Section0Verdict.BLOCKED
    assert gate.cohort_basis == "forward_only"


def test_uninferable_listing_dates_block_regardless_of_power() -> None:
    gate = fire_section0(
        powers_full=FULL_STRONG,
        powers_forward_only=FWD_STRONG,
        delisting=DelistingObservability.PASS,
        listing_dates_inferable=False,
        funding_retention_ok=True,
    )
    assert gate.verdict is Section0Verdict.BLOCKED
    assert not gate.collectors_armed
    assert "plus or minus one day" in gate.rationale


def test_funding_retention_below_the_bar_blocks_regardless_of_power() -> None:
    gate = fire_section0(
        powers_full=FULL_STRONG,
        powers_forward_only=FWD_STRONG,
        delisting=DelistingObservability.PASS,
        listing_dates_inferable=True,
        funding_retention_ok=False,
    )
    assert gate.verdict is Section0Verdict.BLOCKED
    assert not gate.collectors_armed


def test_a_power_outside_the_unit_interval_raises() -> None:
    with pytest.raises(ValueError, match="probability"):
        fire_section0(
            powers_full=CoPrimaryPowers(p1=1.2, p2=0.9, p3=0.9),
            powers_forward_only=FWD_STRONG,
            delisting=DelistingObservability.PASS,
            listing_dates_inferable=True,
            funding_retention_ok=True,
        )


def test_the_rationale_carries_the_deadline_and_the_floor() -> None:
    gate = fire_section0(
        powers_full=CoPrimaryPowers(p1=0.80, p2=0.80, p3=0.80),
        powers_forward_only=FWD_STRONG,
        delisting=DelistingObservability.PASS,
        listing_dates_inferable=True,
        funding_retention_ok=True,
    )
    assert CONFIG.projection_deadline in gate.rationale
    assert "0.80" in gate.rationale
