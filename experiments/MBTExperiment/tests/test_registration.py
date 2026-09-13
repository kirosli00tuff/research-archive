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
    DERIBIT_REFERENCE_BTC_ROUND_TRIP_BPS,
    MARGIN_CEILING_FRACTION_OF_NOTIONAL,
    MARGIN_CEILING_USD_PER_CONTRACT,
    MAX_WINDOWS_PER_UTC_DAY,
    MBT_COMMISSION_PER_CONTRACT_USD,
    MBT_NOTIONAL_USD,
    MIN_COLLECTION_DAYS,
    MIN_MINUTES_BETWEEN_WINDOWS,
    MIN_OBSERVATION_WINDOWS,
    ORB_PRECEDENT_LEGS_TOTAL,
    ORB_PRECEDENT_LEGS_UNDERSTATED,
    ORB_PRECEDENT_SHIFT_FACTOR,
    REBALANCE_COUNT_BTC_MAX,
    REBALANCE_COUNT_ETH_MAX,
    REBALANCE_COUNT_MEDIAN,
    REBALANCE_COUNT_P90,
    REBALANCE_COUNT_SWEEP_MEDIANS,
    REBALANCE_DAILY_STRUCTURAL_MAX,
    REBALANCE_FILL_COMMISSION_BPS,
    REGISTERED_PREMIUM_BASIS,
    STRADDLE_ROUND_TRIP_COMMISSION_BPS,
    TRIAL_GRID_AFTER_DEFLATION,
    TRIAL_GRID_CONTINUOUS_TOLERANCES,
    TRIAL_GRID_DISCRETE_COMBINATIONS,
    VRP_SAMPLE_N,
    PremiumBasis,
)

REPO = Path(__file__).resolve().parents[1]
REGISTRATION = (REPO / "REGISTRATION.md").read_text(encoding="utf-8")

#: The document is hard-wrapped at 80 columns, so any multi-word phrase can be
#: split across a newline. Prose assertions run against this flattened form;
#: the verbatim-transcription anchors deliberately use the raw text, because the
#: point there is that the quoted block was copied rather than reflowed.
REGISTRATION_FLAT = " ".join(REGISTRATION.split())
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
    assert "49.610" in REGISTRATION_FLAT
    assert "34.600" in REGISTRATION_FLAT


def test_the_registration_states_that_a_later_reselection_voids_it() -> None:
    assert "voids this registration" in REGISTRATION_FLAT


def test_the_registration_states_the_lower_bound_versus_point_estimate_asymmetry() -> None:
    """The weakness of the chosen basis must be stated rather than buried."""
    assert "one-sided 95% lower bound" in REGISTRATION_FLAT
    assert "point estimate" in REGISTRATION_FLAT
    assert "upper bound on the like-for-like ceiling" in REGISTRATION_FLAT


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
    assert phrase in REGISTRATION_FLAT, f"REGISTRATION.md no longer carries {phrase!r}"


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
        assert phrase in CLAUDE_MD and phrase in REGISTRATION_FLAT


# --- the trial grid ---------------------------------------------------------


# --- the three terminal states ---------------------------------------------


@pytest.mark.parametrize("state", ["HARNESS-READY", "HARNESS-BLOCKED"])
def test_the_terminal_states_are_registered(state: str) -> None:
    assert state in REGISTRATION_FLAT


def test_the_unreachable_verdicts_are_registered_as_unreachable() -> None:
    assert "can never reach HARVESTABLE-CONFIRMED" in REGISTRATION_FLAT


# --- Sections 1 onward, added in Task 3 -------------------------------------


def test_vrp_sections_are_transcribed_verbatim_rather_than_paraphrased() -> None:
    """Three anchor sentences, quoted exactly from VRPExperiment 4.1, 4.2 and 4.3."""
    anchors = (
        "sampled across\n>    **at least 20 distinct observation windows**",
        "the statistic assigned to each end registered here, before anything",
        "resized\n> > whenever the position delta moves more than \u00b10.10 from flat",
    )
    for anchor in anchors:
        assert anchor in REGISTRATION, f"the transcription lost: {anchor!r}"


def test_the_upstream_assignment_is_inherited_and_not_reopened() -> None:
    assert "fixed upstream" in REGISTRATION_FLAT
    assert "not reopened here" in REGISTRATION or "Not reopened." in REGISTRATION_FLAT


def test_the_carried_rebalance_counts_appear_with_their_n() -> None:
    """A negative with a hidden n is not a result, and neither is a positive."""
    assert "1,955 paths" in REGISTRATION_FLAT
    for value in (REBALANCE_COUNT_MEDIAN, REBALANCE_COUNT_P90, REBALANCE_COUNT_BTC_MAX):
        assert f"**{value}**" in REGISTRATION_FLAT
    assert str(REBALANCE_COUNT_ETH_MAX) in REGISTRATION_FLAT
    assert str(REBALANCE_DAILY_STRUCTURAL_MAX) in REGISTRATION_FLAT


def test_the_swept_bands_are_reported_rather_than_selected() -> None:
    assert REBALANCE_COUNT_SWEEP_MEDIANS == {0.05: 17, 0.20: 5}
    assert "sensitivity" in REGISTRATION_FLAT
    assert "never selected between" in REGISTRATION_FLAT


def test_the_four_implementer_rules_are_each_fixed() -> None:
    """Each is a place where a quiet wrong answer produces a valid straddle."""
    for rule in (
        "The at-the-money strike selection rule",
        "The 30-day tenor resolution rule",
        "What makes two observation windows distinct, in clock terms",
        "The refusal conditions",
    ):
        assert rule in REGISTRATION_FLAT, f"the registration does not fix: {rule}"


def test_the_tenor_rule_states_its_rounding_direction_and_its_tie() -> None:
    assert "rounds to **nearest**" in REGISTRATION_FLAT
    assert "round **up**" in REGISTRATION_FLAT
    assert "At a tie, the LONGER tenor" in REGISTRATION_FLAT


def test_the_strike_rule_states_its_tie() -> None:
    assert "At a tie, the LOWER strike" in REGISTRATION_FLAT


def test_the_distinctness_rule_is_stated_in_clock_terms() -> None:
    assert "60 MINUTES" in REGISTRATION_FLAT
    assert "UTC CALENDAR DAY" in REGISTRATION_FLAT
    assert "5 collection days minimum" in REGISTRATION_FLAT


def test_every_refusal_condition_has_a_typed_absence_registered() -> None:
    for reason in (
        "unquoted_leg",
        "crossed_book",
        "zero_bid",
        "stale_timestamp",
        "delayed_tick",
        "frozen_tick",
    ):
        assert f"Absent({reason})" in REGISTRATION_FLAT


def test_a_refused_window_is_registered_as_recorded_never_dropped() -> None:
    assert "never dropped" in REGISTRATION_FLAT
    assert "never backfilled" in REGISTRATION_FLAT


def test_the_commission_figures_are_ported_as_measured() -> None:
    for phrase in ("USD 0.85", "4.352 bps", "1.088 bps", "16.320 bps", "21.760 bps"):
        assert phrase in REGISTRATION_FLAT


def test_deribit_is_registered_reference_only() -> None:
    assert DERIBIT_REFERENCE_BTC_ROUND_TRIP_BPS == 22.50
    assert "REFERENCE ONLY" in REGISTRATION_FLAT
    assert "22.50 bps" in REGISTRATION_FLAT
    assert "ADR-008" in REGISTRATION_FLAT
    assert str(ORB_PRECEDENT_SHIFT_FACTOR) in REGISTRATION_FLAT


def test_the_orb_precedent_records_the_overstated_leg_too() -> None:
    """Because one leg was OVERstated, 'assume worse' would not have rescued it."""
    assert ORB_PRECEDENT_LEGS_UNDERSTATED == 5
    assert ORB_PRECEDENT_LEGS_TOTAL == 6
    assert "over*stating a\nsixth" in REGISTRATION or "overstated" in REGISTRATION_FLAT
    assert "wrong in both directions" in REGISTRATION_FLAT


def test_the_substitution_ban_names_what_it_forecloses() -> None:
    for source in ("Deribit", "MLCryptoEngine", "tick-size modelling", "comparable instrument"):
        assert source in REGISTRATION_FLAT


def test_the_trial_grid_is_counted_and_deflates_to_one() -> None:
    assert TRIAL_GRID_DISCRETE_COMBINATIONS == 48
    assert TRIAL_GRID_CONTINUOUS_TOLERANCES == 3
    assert TRIAL_GRID_AFTER_DEFLATION == 1
    assert "2 \u00d7 3 \u00d7 2 \u00d7 2 \u00d7 2 = 48" in REGISTRATION_FLAT
    assert "The grid deflates to 1" in REGISTRATION_FLAT


def test_the_operator_prior_slot_exists_and_is_empty() -> None:
    assert "Section 5 — The operator prior" in REGISTRATION_FLAT
    assert "RESERVED — EMPTY" in REGISTRATION_FLAT
    assert "rather than backfilled" in REGISTRATION_FLAT
