"""The five call states. They are never merged.

model_failed is operational health. excluded_pre_cutoff is sample composition.
source_failed is a data-side fault. Collapsing any pair destroys the distinction
between a model that could not answer and a sample that was never eligible.
The news experiment drew the same boundary for the same reason.
"""

from __future__ import annotations

from enum import StrEnum


class CallState(StrEnum):
    """Terminal state of one scheduled day."""

    STORED = "stored"
    NO_DATA = "no_data"
    MODEL_FAILED = "model_failed"
    EXCLUDED_PRE_CUTOFF = "excluded_pre_cutoff"
    SOURCE_FAILED = "source_failed"


OPERATIONAL_HEALTH_STATES: frozenset[CallState] = frozenset(
    {CallState.MODEL_FAILED, CallState.SOURCE_FAILED}
)

SAMPLE_COMPOSITION_STATES: frozenset[CallState] = frozenset(
    {CallState.EXCLUDED_PRE_CUTOFF, CallState.NO_DATA}
)

ALL_STATES: tuple[CallState, ...] = tuple(CallState)


def is_eligible_state(state: CallState) -> bool:
    """A day counts toward the coverage denominator unless it was never eligible."""
    return state is not CallState.EXCLUDED_PRE_CUTOFF
