"""Section 0 — every boundary fixture sits exactly on its registered threshold.

A fixture comfortably inside a boundary lets a moved threshold pass unnoticed.
That is the InsiderExperiment mutation lesson and it is why every test below
pins the boundary value itself, then steps one ULP or one count across it.
"""

from __future__ import annotations

import math

import pytest

from orb.absence import AbsenceReason, Absent
from orb.access import CollectionAccess
from orb.config import CONFIG
from orb.integrity import AgreementFinding, IntegrityVerdict, RevisionFinding
from orb.section0 import PowerInputs, Section0Verdict, fire_section0


def revision(share: float, *, bars: int = 100_000, wait: int = 14) -> RevisionFinding:
    return RevisionFinding(
        changed_bar_share=share,
        bars_compared=bars,
        changed_bar_count=round(share * bars),
        session_ticker_pairs_compared=2_400,
        pairs_with_changed_bar_count=0,
        pairs_with_timestamp_change=0,
        changes_coinciding_with_corporate_action=0,
        wait_days_observed=wait,
    )


def agreement(
    share: float = 0.99, delisted: int = 250, *, pairs: int = 2_400
) -> AgreementFinding:
    return AgreementFinding(
        first5_high_low_agreement_share=share,
        session_ticker_pairs_compared=pairs,
        bars_present_in_both=95_000,
        bars_agreeing_to_the_cent=94_000,
        delisted_names_served=delisted,
        delisted_names_with_intraday_history=delisted,
    )


def power(
    e1_reg: float = 0.95,
    e2_reg: float = 0.95,
    e1_pub: float = 0.999,
    e2_pub: float = 0.999,
) -> PowerInputs:
    return PowerInputs(e1_reg, e2_reg, e1_pub, e2_pub, sessions_achievable=880)


def up(x: float) -> float:
    """One ULP above ``x``."""
    return math.nextafter(x, math.inf)


def down(x: float) -> float:
    """One ULP below ``x``."""
    return math.nextafter(x, -math.inf)


# --- The revision verdict, on its boundaries -------------------------------


def test_revision_exactly_on_the_pass_bar_is_pass() -> None:
    """0.005 exactly. 'at or below 0.5 percent' — inclusive."""
    assert revision(CONFIG.revision_pass_max_share).verdict() is IntegrityVerdict.PASS


def test_revision_one_ulp_above_the_pass_bar_is_partial() -> None:
    assert (
        revision(up(CONFIG.revision_pass_max_share)).verdict()
        is IntegrityVerdict.PARTIAL
    )


def test_revision_exactly_on_the_partial_bar_is_partial() -> None:
    """0.020 exactly. 'at or below 2.0 percent' — inclusive."""
    assert (
        revision(CONFIG.revision_partial_max_share).verdict()
        is IntegrityVerdict.PARTIAL
    )


def test_revision_one_ulp_above_the_partial_bar_is_fail() -> None:
    assert (
        revision(up(CONFIG.revision_partial_max_share)).verdict()
        is IntegrityVerdict.FAIL
    )


def test_the_registered_wait_is_tracked_separately_from_the_verdict() -> None:
    """A clean re-pull taken too early is not evidence of a clean vendor."""
    assert not revision(0.0, wait=13).wait_satisfied()
    assert revision(0.0, wait=14).wait_satisfied()


# --- The agreement and delisted verdicts, on their boundaries --------------


def test_agreement_exactly_on_the_pass_bar_is_pass() -> None:
    """0.95 exactly. 'at or above 95 percent' — inclusive."""
    assert (
        agreement(CONFIG.agreement_pass_min_share).agreement_verdict()
        is IntegrityVerdict.PASS
    )


def test_agreement_one_ulp_below_the_pass_bar_is_partial() -> None:
    assert (
        agreement(down(CONFIG.agreement_pass_min_share)).agreement_verdict()
        is IntegrityVerdict.PARTIAL
    )


def test_agreement_exactly_on_the_partial_floor_is_partial() -> None:
    """0.85 exactly. FAIL is 'below 85 percent', so 0.85 itself is PARTIAL."""
    assert (
        agreement(CONFIG.agreement_partial_min_share).agreement_verdict()
        is IntegrityVerdict.PARTIAL
    )


def test_agreement_one_ulp_below_the_partial_floor_is_fail() -> None:
    assert (
        agreement(down(CONFIG.agreement_partial_min_share)).agreement_verdict()
        is IntegrityVerdict.FAIL
    )


def test_delisted_exactly_on_100_is_pass_and_99_is_partial() -> None:
    assert (
        agreement(delisted=CONFIG.delisted_pass_min_count).delisted_verdict()
        is IntegrityVerdict.PASS
    )
    assert (
        agreement(delisted=CONFIG.delisted_pass_min_count - 1).delisted_verdict()
        is IntegrityVerdict.PARTIAL
    )


def test_delisted_exactly_on_20_is_partial_and_19_is_fail() -> None:
    assert (
        agreement(delisted=CONFIG.delisted_partial_min_count).delisted_verdict()
        is IntegrityVerdict.PARTIAL
    )
    assert (
        agreement(delisted=CONFIG.delisted_partial_min_count - 1).delisted_verdict()
        is IntegrityVerdict.FAIL
    )


def test_the_combined_verdict_takes_the_worst_of_the_two() -> None:
    """Perfect agreement does not offset a survivor-only universe."""
    assert agreement(0.999, delisted=19).verdict() is IntegrityVerdict.FAIL
    assert agreement(0.999, delisted=50).verdict() is IntegrityVerdict.PARTIAL
    assert agreement(0.90, delisted=250).verdict() is IntegrityVerdict.PARTIAL
    assert agreement(0.999, delisted=250).verdict() is IntegrityVerdict.PASS


# --- The fire function -----------------------------------------------------


def test_go_fires_when_powers_and_both_integrity_verdicts_pass() -> None:
    result = fire_section0(power(), revision(0.001), agreement())
    assert result.verdict is Section0Verdict.GO
    assert "880" in result.reason


def test_go_sits_exactly_on_the_power_floor() -> None:
    """0.80 exactly is GO; one ULP below is not."""
    at = power(e1_reg=CONFIG.target_power, e2_reg=CONFIG.target_power)
    assert fire_section0(at, revision(0.001), agreement()).verdict is Section0Verdict.GO

    below = power(e1_reg=down(CONFIG.target_power), e2_reg=CONFIG.target_power)
    assert (
        fire_section0(below, revision(0.001), agreement()).verdict
        is Section0Verdict.DEGRADED
    )


def test_e2_alone_below_the_floor_denies_go() -> None:
    """Both must pass. A single co-primary is not a majority."""
    inputs = power(e1_reg=0.99, e2_reg=down(CONFIG.target_power))
    assert (
        fire_section0(inputs, revision(0.001), agreement()).verdict
        is Section0Verdict.DEGRADED
    )


def test_blocked_fires_on_the_published_power_floor() -> None:
    """0.50 exactly is not BLOCKED; one ULP below is."""
    at = power(e1_pub=CONFIG.blocked_power_floor)
    assert fire_section0(at, revision(0.001), agreement()).verdict is not (
        Section0Verdict.BLOCKED
    )

    below = power(e1_pub=down(CONFIG.blocked_power_floor))
    result = fire_section0(below, revision(0.001), agreement())
    assert result.verdict is Section0Verdict.BLOCKED
    assert result.clause == "BLOCKED-1 power floor"


def test_blocked_fires_on_a_revision_fail_even_at_perfect_power() -> None:
    """A design that cannot trust its bars is not rescued by sample size."""
    result = fire_section0(
        power(1.0, 1.0, 1.0, 1.0),
        revision(up(CONFIG.revision_partial_max_share)),
        agreement(),
    )
    assert result.verdict is Section0Verdict.BLOCKED
    assert result.clause == "BLOCKED-2 bar integrity FAIL"


def test_blocked_fires_on_zero_delisted_names_before_the_count_clause() -> None:
    """Zero is named separately from the count floor, and fires first."""
    result = fire_section0(power(), revision(0.001), agreement(delisted=0))
    assert result.verdict is Section0Verdict.BLOCKED
    assert result.clause == "BLOCKED-3 zero delisted coverage"


def test_blocked_fires_when_the_selection_is_not_reproducible() -> None:
    result = fire_section0(
        power(),
        revision(0.001),
        agreement(down(CONFIG.agreement_partial_min_share)),
    )
    assert result.verdict is Section0Verdict.BLOCKED
    assert result.clause == "BLOCKED-4 selection not reproducible"


def test_blocked_fires_on_thin_delisted_coverage() -> None:
    result = fire_section0(
        power(),
        revision(0.001),
        agreement(delisted=CONFIG.delisted_partial_min_count - 1),
    )
    assert result.verdict is Section0Verdict.BLOCKED
    assert result.clause == "BLOCKED-5 delisted coverage FAIL"


def test_precedence_is_fixed_blocked_before_go() -> None:
    """Perfect power and a FAIL together fire BLOCKED, never GO."""
    result = fire_section0(
        power(1.0, 1.0, 1.0, 1.0), revision(0.05), agreement(0.50, delisted=0)
    )
    assert result.verdict is Section0Verdict.BLOCKED
    assert result.clause == "BLOCKED-2 bar integrity FAIL"


def test_degraded_on_power_at_published_but_not_registered() -> None:
    inputs = power(e1_reg=0.55, e2_reg=0.55, e1_pub=0.95, e2_pub=0.95)
    result = fire_section0(inputs, revision(0.001), agreement())
    assert result.verdict is Section0Verdict.DEGRADED
    assert "published magnitude" in result.reason
    assert "cannot distinguish a decayed effect from no effect" in result.reason


def test_degraded_on_partial_bar_integrity_at_full_power() -> None:
    result = fire_section0(power(), revision(0.01), agreement())
    assert result.verdict is Section0Verdict.DEGRADED
    assert "bar integrity PARTIAL" in result.reason


def test_degraded_on_thin_but_present_delisted_coverage() -> None:
    result = fire_section0(power(), revision(0.001), agreement(delisted=50))
    assert result.verdict is Section0Verdict.DEGRADED
    assert "PARTIAL" in result.reason


def test_the_registered_residual_band_is_degraded_not_a_gap() -> None:
    """E1 published power strictly between 0.50 and 0.80, integrity full.

    The three BLOCKED clauses and the GO clause leave this case unnamed. It is
    registered as DEGRADED: it sits above the floor that stops collection.
    """
    inputs = power(e1_reg=0.30, e2_reg=0.30, e1_pub=0.65, e2_pub=0.65)
    result = fire_section0(inputs, revision(0.001), agreement())
    assert result.verdict is Section0Verdict.DEGRADED
    assert "residual band" in result.reason


def test_the_map_is_total_over_the_verdict_lattice() -> None:
    """Every combination of the inputs fires exactly one registered verdict."""
    shares = [0.0, CONFIG.revision_pass_max_share, 0.01, 0.05]
    agrees = [0.0, 0.85, 0.94, 1.0]
    delisteds = [0, 19, 20, 99, 100, 500]
    powers = [0.0, 0.49, 0.5, 0.79, 0.8, 1.0]
    seen: set[Section0Verdict] = set()
    n = 0
    for s in shares:
        for a in agrees:
            for d in delisteds:
                for p in powers:
                    result = fire_section0(
                        power(p, p, max(p, 0.5), max(p, 0.5)),
                        revision(s),
                        agreement(a, d),
                    )
                    assert isinstance(result.verdict, Section0Verdict)
                    seen.add(result.verdict)
                    n += 1
    assert n == 4 * 4 * 6 * 6
    assert seen == {
        Section0Verdict.GO,
        Section0Verdict.DEGRADED,
        Section0Verdict.BLOCKED,
    }, seen


@pytest.mark.guard
def test_section0_reads_no_bar_value() -> None:
    """Every input is a count, a share, or a power. None is a price."""
    import dataclasses

    from orb.seal import PRICED_BAR_FIELDS

    for cls in (PowerInputs, RevisionFinding, AgreementFinding):
        for field in dataclasses.fields(cls):
            assert field.name not in PRICED_BAR_FIELDS, (cls.__name__, field.name)
            assert field.type in {"float", "int"}, (
                cls.__name__,
                field.name,
                field.type,
            )


# --- Amendment 1, 2026-08-29: the PENDING_ACCESS clause --------------------


def test_an_absent_revision_finding_fires_pending_access() -> None:
    """A measurement that does not exist is never read as one that failed."""
    from orb.absence import AbsenceReason, Absent

    result = fire_section0(
        power(),
        Absent(AbsenceReason.NOT_YET_MEASURED, "no credentialed vendor"),
        agreement(),
    )
    assert result.verdict is Section0Verdict.PENDING_ACCESS
    assert result.clause == "PENDING-ACCESS Amendment 1"
    assert "not a source-integrity closure" in result.reason


def test_an_absent_agreement_finding_fires_pending_access() -> None:
    from orb.absence import AbsenceReason, Absent

    result = fire_section0(
        power(),
        revision(0.001),
        Absent(AbsenceReason.NOT_YET_MEASURED, "no secondary vendor"),
    )
    assert result.verdict is Section0Verdict.PENDING_ACCESS


def test_pending_access_outranks_every_blocked_trigger() -> None:
    """Absent inputs fire first. A missing bar cannot fail an integrity bar."""
    from orb.absence import AbsenceReason, Absent

    result = fire_section0(
        power(e1_pub=0.0),  # would otherwise fire BLOCKED-1
        Absent(AbsenceReason.NOT_YET_MEASURED, "no credentialed vendor"),
        Absent(AbsenceReason.NOT_YET_MEASURED, "no credentialed vendor"),
    )
    assert result.verdict is Section0Verdict.PENDING_ACCESS
    assert "bar revision" in result.reason
    assert "cross-vendor agreement" in result.reason


def test_pending_access_is_not_reachable_when_both_inputs_are_present() -> None:
    """The clause is inert once the measurements exist. It is not a bypass."""
    for share in (0.0, 0.01, 0.5):
        for a, d in ((1.0, 500), (0.9, 50), (0.0, 0)):
            result = fire_section0(power(), revision(share), agreement(a, d))
            assert result.verdict is not Section0Verdict.PENDING_ACCESS


# --- Amendment 10, 2026-08-29: PENDING_SPEND and PENDING_REVISION ----------

ABSENT_REVISION = Absent(AbsenceReason.NOT_YET_MEASURED, "the 14-day wait is running")
ABSENT_AGREEMENT = Absent(AbsenceReason.NOT_YET_MEASURED, "no agreement measurement")


def test_pending_revision_fires_when_access_serves_and_the_clock_has_not_run() -> None:
    """The landing state of the A.1 resumption: a parked outcome, not a failure."""
    result = fire_section0(
        power(e1_reg=0.7435, e2_reg=0.0),
        ABSENT_REVISION,
        ABSENT_AGREEMENT,
        access=CollectionAccess.SERVING_FULL_REACH,
        delisted_with_intraday=203,
    )
    assert result.verdict is Section0Verdict.PENDING_REVISION
    assert result.clause == "PENDING-REVISION Amendment 10"
    assert "not a source-integrity closure" in result.reason
    assert "biased toward zero" in result.reason


def test_pending_access_still_fires_when_no_vendor_serves() -> None:
    """Amendment 1's clause is unchanged for the state it was written for."""
    result = fire_section0(
        power(),
        ABSENT_REVISION,
        ABSENT_AGREEMENT,
        access=CollectionAccess.NO_VENDOR_SERVES,
    )
    assert result.verdict is Section0Verdict.PENDING_ACCESS
    assert result.clause == "PENDING-ACCESS Amendment 1"


def test_pending_spend_fires_on_a_measured_reach_shortfall() -> None:
    result = fire_section0(
        power(),
        ABSENT_REVISION,
        ABSENT_AGREEMENT,
        access=CollectionAccess.SERVING_REACH_SHORT,
        delisted_with_intraday=203,
    )
    assert result.verdict is Section0Verdict.PENDING_SPEND
    assert result.clause == "PENDING-SPEND Amendment 10"
    assert "no spend is authorised" in result.reason


def test_pending_spend_outranks_pending_revision() -> None:
    """A reach shortfall is a harder blocker than a clock that has not run."""
    short = fire_section0(
        power(),
        ABSENT_REVISION,
        ABSENT_AGREEMENT,
        access=CollectionAccess.SERVING_REACH_SHORT,
        delisted_with_intraday=203,
    )
    full = fire_section0(
        power(),
        ABSENT_REVISION,
        ABSENT_AGREEMENT,
        access=CollectionAccess.SERVING_FULL_REACH,
        delisted_with_intraday=203,
    )
    assert short.verdict is Section0Verdict.PENDING_SPEND
    assert full.verdict is Section0Verdict.PENDING_REVISION


def test_pending_revision_is_not_reachable_when_both_inputs_are_present() -> None:
    """The clause is inert once the measurements exist. It is not a bypass."""
    for share in (0.0, 0.01, 0.5):
        for a, d in ((1.0, 500), (0.9, 50), (0.0, 0)):
            for access in CollectionAccess:
                result = fire_section0(
                    power(),
                    revision(share),
                    agreement(a, d),
                    access=access,
                )
                assert result.verdict is not Section0Verdict.PENDING_REVISION


def test_a_measured_delisted_count_reaches_the_map_when_agreement_is_absent() -> None:
    """Without this the agreement share's absence would hide a measured zero."""
    result = fire_section0(
        power(),
        ABSENT_REVISION,
        ABSENT_AGREEMENT,
        access=CollectionAccess.SERVING_FULL_REACH,
        delisted_with_intraday=0,
    )
    assert result.verdict is Section0Verdict.BLOCKED
    assert result.clause == "BLOCKED-3 zero delisted coverage"


def test_the_delisted_floor_binds_exactly_on_20_with_agreement_absent() -> None:
    """On the boundary, and one count across it."""
    on_floor = fire_section0(
        power(),
        ABSENT_REVISION,
        ABSENT_AGREEMENT,
        access=CollectionAccess.SERVING_FULL_REACH,
        delisted_with_intraday=CONFIG.delisted_partial_min_count,
    )
    below = fire_section0(
        power(),
        ABSENT_REVISION,
        ABSENT_AGREEMENT,
        access=CollectionAccess.SERVING_FULL_REACH,
        delisted_with_intraday=CONFIG.delisted_partial_min_count - 1,
    )
    assert on_floor.verdict is Section0Verdict.PENDING_REVISION
    assert below.verdict is Section0Verdict.BLOCKED
    assert below.clause == "BLOCKED-5 delisted coverage FAIL"


def test_a_measured_revision_fail_outranks_pending_revision() -> None:
    """A BLOCKED trigger whose input is measured is evidence, and evidence wins."""
    result = fire_section0(
        power(),
        revision(up(CONFIG.revision_partial_max_share)),
        ABSENT_AGREEMENT,
        access=CollectionAccess.SERVING_FULL_REACH,
        delisted_with_intraday=203,
    )
    assert result.verdict is Section0Verdict.BLOCKED
    assert result.clause == "BLOCKED-2 bar integrity FAIL"


def test_an_absent_blocked_input_is_skipped_rather_than_read_as_a_failure() -> None:
    """Amendment 1's objection was evidence that does not exist. It still binds."""
    result = fire_section0(
        power(),
        ABSENT_REVISION,
        ABSENT_AGREEMENT,
        access=CollectionAccess.SERVING_FULL_REACH,
    )
    assert result.verdict is Section0Verdict.PENDING_REVISION


def test_the_power_floor_still_outranks_every_pending_state_when_a_vendor_serves() -> (
    None
):
    """A power fact is fully measured and independent of any integrity input."""
    result = fire_section0(
        power(e1_pub=down(CONFIG.blocked_power_floor)),
        ABSENT_REVISION,
        ABSENT_AGREEMENT,
        access=CollectionAccess.SERVING_FULL_REACH,
        delisted_with_intraday=203,
    )
    assert result.verdict is Section0Verdict.BLOCKED
    assert result.clause == "BLOCKED-1 power floor"


def test_all_five_registered_verdicts_are_reachable() -> None:
    """A verdict nobody can reach is a clause that does not exist."""
    reached = {
        fire_section0(power(), ABSENT_REVISION, ABSENT_AGREEMENT).verdict,
        fire_section0(
            power(),
            ABSENT_REVISION,
            ABSENT_AGREEMENT,
            access=CollectionAccess.SERVING_REACH_SHORT,
        ).verdict,
        fire_section0(
            power(),
            ABSENT_REVISION,
            ABSENT_AGREEMENT,
            access=CollectionAccess.SERVING_FULL_REACH,
        ).verdict,
        fire_section0(power(), revision(0.001), agreement(0.99, 250)).verdict,
        fire_section0(power(), revision(0.5), agreement(0.99, 250)).verdict,
        fire_section0(power(e1_reg=0.5), revision(0.001), agreement(0.99, 250)).verdict,
    }
    assert reached == set(Section0Verdict)


def test_neither_go_nor_degraded_is_reachable_while_an_input_is_absent() -> None:
    """The A.1 resumption's hard constraint, pinned rather than promised."""
    for access in CollectionAccess:
        for rev, agr in (
            (ABSENT_REVISION, ABSENT_AGREEMENT),
            (ABSENT_REVISION, agreement()),
            (revision(0.001), ABSENT_AGREEMENT),
        ):
            result = fire_section0(
                power(), rev, agr, access=access, delisted_with_intraday=203
            )
            assert result.verdict not in {
                Section0Verdict.GO,
                Section0Verdict.DEGRADED,
            }
