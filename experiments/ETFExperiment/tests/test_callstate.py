"""The six call states never merge operational health with sample composition."""

from __future__ import annotations

from etf.callstate import (
    ALL_STATES,
    MEASURED_ABSENCE_STATES,
    OPERATIONAL_HEALTH_STATES,
    SAMPLE_COMPOSITION_STATES,
    CallState,
    is_operational,
    is_stored,
)


def test_exactly_the_six_registered_states_exist() -> None:
    assert [s.value for s in ALL_STATES] == [
        "stored",
        "no_data",
        "source_failed",
        "rate_limited",
        "excluded_ineligible",
        "expired",
    ]


def test_rate_limited_and_no_data_never_share_a_partition() -> None:
    """The mutation this pins: merging rate_limited into no_data.

    A source refusing a request and a source answering emptily are different
    facts. Merging them turns an operational refusal into a measured absence
    and inflates the archive-capture-density denominator's honest reasons.
    """
    assert CallState.RATE_LIMITED in OPERATIONAL_HEALTH_STATES
    assert CallState.RATE_LIMITED not in MEASURED_ABSENCE_STATES
    assert CallState.NO_DATA in MEASURED_ABSENCE_STATES
    assert CallState.NO_DATA not in OPERATIONAL_HEALTH_STATES


def test_the_three_partitions_are_disjoint_and_cover_everything_but_stored() -> None:
    partitions = [
        OPERATIONAL_HEALTH_STATES,
        SAMPLE_COMPOSITION_STATES,
        MEASURED_ABSENCE_STATES,
    ]
    union: set[CallState] = set()
    for part in partitions:
        assert not (union & part), "partitions overlap"
        union |= part
    assert union == set(ALL_STATES) - {CallState.STORED}


def test_only_stored_is_stored() -> None:
    assert is_stored(CallState.STORED)
    assert not any(is_stored(s) for s in ALL_STATES if s is not CallState.STORED)
    assert is_operational(CallState.SOURCE_FAILED)
    assert not is_operational(CallState.EXCLUDED_INELIGIBLE)
