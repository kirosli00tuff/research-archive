"""Section 0 — every boundary fixture sits exactly on its registered threshold.

A fixture comfortably inside a boundary lets a moved threshold pass unnoticed.
That is the InsiderExperiment mutation lesson and it is why every test below
pins the boundary value itself, then steps one ULP or one count across it.
"""

from __future__ import annotations

import math

import pytest

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
