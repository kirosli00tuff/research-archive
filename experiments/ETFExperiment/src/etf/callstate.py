"""The six recorded call states. They are never merged.

Operational health and sample composition never share a representation.
RATE_LIMITED is a source refusing a request. EXCLUDED_INELIGIBLE is a trading
day the registered admissibility rule of Section 3 deliberately excluded.
Collapsing the pair destroys the distinction between a cohort that could not be
fetched and a cohort that was correctly narrowed, which is exactly the
distinction the archive-capture-density bar of A.1 Task 4 turns on.
"""

from __future__ import annotations

from enum import StrEnum


class CallState(StrEnum):
    """Terminal state of one collection attempt or one enumerated trading day."""

    STORED = "stored"
    NO_DATA = "no_data"
    SOURCE_FAILED = "source_failed"
    RATE_LIMITED = "rate_limited"
    EXCLUDED_INELIGIBLE = "excluded_ineligible"
    EXPIRED = "expired"


# A refusal or fault of the instrument. Says nothing about the sample.
OPERATIONAL_HEALTH_STATES: frozenset[CallState] = frozenset(
    {CallState.SOURCE_FAILED, CallState.RATE_LIMITED, CallState.EXPIRED}
)

# A deliberate narrowing by a registered rule. Says nothing about the source.
SAMPLE_COMPOSITION_STATES: frozenset[CallState] = frozenset({CallState.EXCLUDED_INELIGIBLE})

# The source answered, and the answer was empty. Measured absence, not a fault.
MEASURED_ABSENCE_STATES: frozenset[CallState] = frozenset({CallState.NO_DATA})

ALL_STATES: tuple[CallState, ...] = tuple(CallState)


def is_stored(state: CallState) -> bool:
    """Only STORED means a payload landed in a store."""
    return state is CallState.STORED


def is_operational(state: CallState) -> bool:
    """True for the states that describe the instrument, never the sample."""
    return state in OPERATIONAL_HEALTH_STATES
