"""Pins the registry to REGISTRATION.md, so a figure cannot drift between them.

Two directions matter and both are checked. A constant that changes in code
without changing the document is a silent re-registration. A figure deleted from
the document while the code still uses it is a registration nobody can read.

The arithmetic checks are **transcription checks, not recomputations**. Every
input is a number transcribed from a named VRPExperiment document, and the
identity confirms the registered ceilings follow from those inputs exactly as the
source states. No premium is recomputed here: VRPExperiment's 1,955-day sample is
spent and is not re-read.
"""

from __future__ import annotations

from itertools import pairwise
from pathlib import Path

import pytest

from mbt.registry import (
    BTC_PREMIUM_DECAY_FRACTION,
    BTC_PREMIUM_QUARTER_NS,
    BTC_PREMIUM_QUARTERS_BPS,
    BTC_PREMIUM_RECENT_QUARTER_BPS,
    COMMISSION_CENTRAL_BPS,
    COMMISSION_CENTRAL_IDENTITY,
    COMMISSION_P90_BPS,
    COMMISSION_P90_IDENTITY,
    COST_CEILING_BPS,
    COST_CEILING_FULL_SAMPLE_BPS,
    COST_CEILING_FULL_SAMPLE_IDENTITY,
    COST_CEILING_RECENT_QUARTER_BPS,
    COST_CEILING_RECENT_QUARTER_IDENTITY,
    DELTA_BAND_PRIMARY,
    DELTA_BAND_SWEEPS,
    MARGIN_CEILING_FRACTION_OF_NOTIONAL,
    MARGIN_CEILING_USD_PER_CONTRACT,
    MAX_WINDOWS_PER_UTC_DAY,
    MBT_COMMISSION_PER_CONTRACT_USD,
    MBT_NOTIONAL_USD,
    MIN_COLLECTION_DAYS,
    MIN_MINUTES_BETWEEN_WINDOWS,
    MIN_OBSERVATION_WINDOWS,
    REBALANCE_COUNT_BTC_MAX,
    REBALANCE_COUNT_MEDIAN,
    REBALANCE_COUNT_P90,
    REBALANCE_FILL_COMMISSION_BPS,
    REGISTERED_PREMIUM_BASIS,
    STRADDLE_ROUND_TRIP_COMMISSION_BPS,
    VRP_SAMPLE_N,
    PremiumBasis,
)

REPO = Path(__file__).resolve().parents[1]
REGISTRATION = (REPO / "REGISTRATION.md").read_text(encoding="utf-8")
CLAUDE_MD = (REPO / "CLAUDE.md").read_text(encoding="utf-8")


# --- the transcription identities ------------------------------------------


def test_the_commission_identities_hold() -> None:
    """4.352 + 11 x 1.088 = 16.320, and 4.352 + 16 x 1.088 = 21.760."""
    assert COMMISSION_CENTRAL_IDENTITY == COMMISSION_CENTRAL_BPS
    assert COMMISSION_P90_IDENTITY == COMMISSION_P90_BPS


def test_the_full_sample_ceiling_identity_holds() -> None:
    """142.740 / 2 - 21.760 = 49.610, the figure VRPExperiment's handover states."""
    assert COST_CEILING_FULL_SAMPLE_IDENTITY == COST_CEILING_FULL_SAMPLE_BPS
    assert COST_CEILING_FULL_SAMPLE_BPS == 49.610


def test_the_recent_quarter_ceiling_identity_holds() -> None:
    """112.72 / 2 - 21.760 = 34.600, the registered ceiling."""
    assert COST_CEILING_RECENT_QUARTER_IDENTITY == COST_CEILING_RECENT_QUARTER_BPS
    assert COST_CEILING_RECENT_QUARTER_BPS == 34.600


def test_the_quarters_decay_monotonically_as_measured() -> None:
    """The mechanism the premium basis rests on, checked rather than asserted."""
    quarters = BTC_PREMIUM_QUARTERS_BPS
    assert all(a > b for a, b in pairwise(quarters))
    assert quarters[-1] == BTC_PREMIUM_RECENT_QUARTER_BPS
    assert len(BTC_PREMIUM_QUARTER_NS) == len(quarters)
    assert sum(BTC_PREMIUM_QUARTER_NS) == VRP_SAMPLE_N


def test_the_recorded_decay_fraction_matches_the_quarters() -> None:
    first, last = BTC_PREMIUM_QUARTERS_BPS[0], BTC_PREMIUM_QUARTERS_BPS[-1]
    assert abs((1.0 - last / first) - BTC_PREMIUM_DECAY_FRACTION) < 0.001


# --- the registered premium basis ------------------------------------------


def test_the_registered_basis_is_the_recent_quarter() -> None:
    assert REGISTERED_PREMIUM_BASIS is PremiumBasis.RECENT_QUARTER_POINT
    assert COST_CEILING_BPS == COST_CEILING_RECENT_QUARTER_BPS


def test_both_ceilings_stay_visible_in_the_registration() -> None:
    """Registering only the chosen one would hide that a choice was made."""
    assert "49.610" in REGISTRATION
    assert "34.600" in REGISTRATION


def test_the_registration_states_that_a_later_reselection_voids_it() -> None:
    assert "voids this registration" in REGISTRATION


def test_the_registration_states_the_lower_bound_versus_point_estimate_asymmetry() -> None:
    """The weakness of the chosen basis must be stated rather than buried."""
    assert "one-sided 95% lower bound" in REGISTRATION
    assert "point estimate" in REGISTRATION
    assert "upper bound on the like-for-like ceiling" in REGISTRATION


def test_the_registered_ceiling_is_the_stricter_of_the_two() -> None:
    """A stricter ceiling cannot be reached for by a wide measurement."""
    assert COST_CEILING_BPS < COST_CEILING_FULL_SAMPLE_BPS


# --- every constant appears in the document --------------------------------


@pytest.mark.parametrize(
    "phrase",
    [
        "7,812.46",
        "12.80%",
        "142.740",
        "112.72",
        "21.760",
        "49.610",
        "34.600",
        "284.53",
        "250.59",
        "145.13",
        "60.4%",
        "1,955",
    ],
)
def test_every_load_bearing_figure_appears_in_the_registration(phrase: str) -> None:
    assert phrase in REGISTRATION, f"REGISTRATION.md no longer carries {phrase!r}"


def test_the_notional_and_margin_ceiling_agree_with_each_other() -> None:
    assert abs(MBT_NOTIONAL_USD * MARGIN_CEILING_FRACTION_OF_NOTIONAL - 1000.0) < 1.0
    assert MARGIN_CEILING_USD_PER_CONTRACT == 1000.0


def test_the_commission_figures_are_the_measured_ones() -> None:
    assert MBT_COMMISSION_PER_CONTRACT_USD == 0.85
    assert STRADDLE_ROUND_TRIP_COMMISSION_BPS == 4.352
    assert REBALANCE_FILL_COMMISSION_BPS == 1.088


def test_the_rebalance_counts_are_the_measured_ones() -> None:
    assert (REBALANCE_COUNT_MEDIAN, REBALANCE_COUNT_P90) == (11, 16)
    assert REBALANCE_COUNT_BTC_MAX == 20


def test_the_hedging_rule_band_and_its_sweeps_are_registered() -> None:
    assert DELTA_BAND_PRIMARY == 0.10
    assert DELTA_BAND_SWEEPS == (0.05, 0.20)


# --- sampling, and why the census is clock-bound ---------------------------


def test_the_window_rules_make_twenty_windows_take_five_days() -> None:
    assert MIN_OBSERVATION_WINDOWS == 20
    assert MAX_WINDOWS_PER_UTC_DAY == 4
    assert MIN_MINUTES_BETWEEN_WINDOWS == 60
    assert MIN_OBSERVATION_WINDOWS / MAX_WINDOWS_PER_UTC_DAY == MIN_COLLECTION_DAYS


# --- the reference that is never a cost input ------------------------------


def test_claude_md_and_the_registration_agree_on_the_gates() -> None:
    for phrase in ("7,812.46", "12.80%", "49.610", "21.760"):
        assert phrase in CLAUDE_MD and phrase in REGISTRATION


# --- the trial grid ---------------------------------------------------------


# --- the three terminal states ---------------------------------------------


@pytest.mark.parametrize("state", ["HARNESS-READY", "HARNESS-BLOCKED"])
def test_the_terminal_states_are_registered(state: str) -> None:
    assert state in REGISTRATION


def test_the_unreachable_verdicts_are_registered_as_unreachable() -> None:
    assert "can never reach HARVESTABLE-CONFIRMED" in REGISTRATION
