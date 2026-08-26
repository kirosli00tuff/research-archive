"""The eight recorded call states. They are never merged.

Operational health and sample composition never share a representation.
UNPARSEABLE is a pipeline fault. FILTERED_ROUTINE is a sample the rule
deliberately excluded. Collapsing the pair destroys the distinction between a
corpus that could not be read and a corpus that was correctly narrowed, which
is exactly the distinction a thin-corpus verdict turns on.
"""

from __future__ import annotations

from enum import StrEnum


class CallState(StrEnum):
    """Terminal state of one candidate Form 4 non-derivative transaction."""

    PARSED = "parsed"
    UNPARSEABLE = "unparseable"
    FILTERED_CODE = "filtered_code"
    FILTERED_ROLE = "filtered_role"
    FILTERED_ROUTINE = "filtered_routine"
    FILTERED_PROGRAMMATIC = "filtered_programmatic"
    NO_BAR = "no_bar"
    OUTSIDE_UNIVERSE = "outside_universe"


OPERATIONAL_HEALTH_STATES: frozenset[CallState] = frozenset(
    {CallState.UNPARSEABLE, CallState.NO_BAR}
)

SAMPLE_COMPOSITION_STATES: frozenset[CallState] = frozenset(
    {
        CallState.FILTERED_CODE,
        CallState.FILTERED_ROLE,
        CallState.FILTERED_ROUTINE,
        CallState.FILTERED_PROGRAMMATIC,
        CallState.OUTSIDE_UNIVERSE,
    }
)

ALL_STATES: tuple[CallState, ...] = tuple(CallState)

# The order attrition is reported in. A transaction is charged to the first
# state it hits, so the stages compose into a funnel rather than a set.
ATTRITION_ORDER: tuple[CallState, ...] = (
    CallState.UNPARSEABLE,
    CallState.FILTERED_CODE,
    CallState.FILTERED_ROLE,
    CallState.OUTSIDE_UNIVERSE,
    CallState.FILTERED_PROGRAMMATIC,
    CallState.FILTERED_ROUTINE,
    CallState.NO_BAR,
    CallState.PARSED,
)


def is_qualifying_state(state: CallState) -> bool:
    """Only PARSED survives every ex-ante filter and enters the portfolio."""
    return state is CallState.PARSED
