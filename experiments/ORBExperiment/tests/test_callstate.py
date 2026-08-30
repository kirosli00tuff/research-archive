"""Guard 4 — operational health and sample composition never merge."""

from __future__ import annotations

import pytest

from orb.callstate import (
    CALL_STATES,
    CallStateMergeError,
    CallStateTally,
    CompositionState,
    HealthState,
)


def test_the_seven_registered_call_states_are_present_and_distinct() -> None:
    assert len(CALL_STATES) == 7, CALL_STATES
    assert len(set(CALL_STATES)) == 7
    assert set(CALL_STATES) == {
        "stored",
        "no_data",
        "source_failed",
        "rate_limited",
        "excluded_ineligible",
        "expired",
        "halted",
    }


def test_health_and_composition_share_no_member() -> None:
    """A state belongs to exactly one family, structurally."""
    health = {s.value for s in HealthState}
    composition = {s.value for s in CompositionState}
    assert not health & composition


def test_rate_limited_is_health_and_cannot_be_recorded_as_composition() -> None:
    """The failure this prevents: a refusal counted as an empty session."""
    tally = CallStateTally()
    with pytest.raises(CallStateMergeError):
        tally.record_composition(HealthState.RATE_LIMITED)  # type: ignore[arg-type]


def test_excluded_ineligible_is_composition_and_cannot_be_recorded_as_health() -> None:
    tally = CallStateTally()
    with pytest.raises(CallStateMergeError):
        tally.record_health(CompositionState.EXCLUDED_INELIGIBLE)  # type: ignore[arg-type]


def test_the_two_totals_never_combine() -> None:
    tally = CallStateTally()
    tally.record_health(HealthState.STORED)
    tally.record_health(HealthState.RATE_LIMITED)
    tally.record_composition(CompositionState.EXPIRED)

    assert tally.health_total() == 2
    assert tally.composition_total() == 1
    with pytest.raises(CallStateMergeError, match="never merge"):
        tally.combined_total()


def test_the_report_keeps_the_families_named_apart() -> None:
    tally = CallStateTally()
    tally.record_health(HealthState.NO_DATA)
    tally.record_composition(CompositionState.HALTED)
    report = tally.as_report()
    assert set(report) == {"health", "composition"}
    assert report["health"]["no_data"] == 1
    assert report["composition"]["halted"] == 1
    assert "halted" not in report["health"]
    assert "no_data" not in report["composition"]
