"""The six call states are exactly six, and never merged. Ported guard 4."""

from __future__ import annotations

from npl.callstate import (
    ALL_STATES,
    MEASURED_ABSENCE_STATES,
    OPERATIONAL_HEALTH_STATES,
    SAMPLE_COMPOSITION_STATES,
    CallState,
    is_stored,
)


def test_six_distinct_call_states() -> None:
    assert len(ALL_STATES) == 6, f"expected six states, found {len(ALL_STATES)}"
    values = [s.value for s in ALL_STATES]
    assert len(set(values)) == 6, f"two states share a value: {values}"
    assert set(values) == {
        "stored",
        "no_data",
        "source_failed",
        "rate_limited",
        "excluded_ineligible",
        "expired",
    }


def test_operational_health_and_sample_composition_never_overlap() -> None:
    assert not (OPERATIONAL_HEALTH_STATES & SAMPLE_COMPOSITION_STATES)
    assert not (OPERATIONAL_HEALTH_STATES & MEASURED_ABSENCE_STATES)
    assert not (SAMPLE_COMPOSITION_STATES & MEASURED_ABSENCE_STATES)
    assert CallState.RATE_LIMITED in OPERATIONAL_HEALTH_STATES
    assert CallState.NO_DATA not in OPERATIONAL_HEALTH_STATES
    assert CallState.EXCLUDED_INELIGIBLE in SAMPLE_COMPOSITION_STATES
    assert CallState.EXCLUDED_INELIGIBLE not in OPERATIONAL_HEALTH_STATES


def test_every_state_is_classified_exactly_once_except_stored() -> None:
    classified = OPERATIONAL_HEALTH_STATES | SAMPLE_COMPOSITION_STATES | MEASURED_ABSENCE_STATES
    assert classified == set(ALL_STATES) - {CallState.STORED}


def test_only_stored_counts_as_stored() -> None:
    assert is_stored(CallState.STORED)
    assert not any(is_stored(s) for s in ALL_STATES if s is not CallState.STORED)
