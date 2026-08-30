"""Guard 4 — operational health and sample composition never merge.

Seven call states are registered. Three describe **what happened to the
request** (operational health) and four describe **what the sample is made of**
(composition). The two families are separate types with no common supertype and
no arithmetic between them, so a rate_limited call cannot be counted as a
no_data observation by any accident of arithmetic or by any later refactor.

The failure this prevents: a vendor refusal read as an empty session inflates
the denominator of every coverage figure in the repository and is unrecoverable
after the fact.
"""

from __future__ import annotations

from enum import StrEnum, unique
from typing import final


@unique
class HealthState(StrEnum):
    """What happened to the request. Never a statement about the sample."""

    STORED = "stored"
    """Bytes were served and sealed."""

    NO_DATA = "no_data"
    """The vendor answered successfully and served nothing."""

    SOURCE_FAILED = "source_failed"
    """The vendor failed: a 5xx, a timeout, or an unparseable envelope."""

    RATE_LIMITED = "rate_limited"
    """The vendor refused on a limit. Never a no_data."""


@unique
class CompositionState(StrEnum):
    """What the sample is made of. Never a statement about a request."""

    EXCLUDED_INELIGIBLE = "excluded_ineligible"
    """The name or session failed a registered filter of Section 2."""

    EXPIRED = "expired"
    """The name delisted before this session."""

    HALTED = "halted"
    """The session was halted; there is no regular session to slice."""


CALL_STATES: tuple[str, ...] = tuple(
    [s.value for s in HealthState] + [s.value for s in CompositionState]
)
"""The seven registered call states, health first, composition second."""


class CallStateMergeError(TypeError):
    """Raised when health and composition are asked to combine."""


@final
class CallStateTally:
    """Counts the two families side by side and refuses to add across them."""

    __slots__ = ("_composition", "_health")

    def __init__(self) -> None:
        self._health: dict[HealthState, int] = dict.fromkeys(HealthState, 0)
        self._composition: dict[CompositionState, int] = dict.fromkeys(
            CompositionState, 0
        )

    def record_health(self, state: HealthState) -> None:
        if not isinstance(state, HealthState):
            raise CallStateMergeError(
                f"record_health refuses {state!r}: only a HealthState is "
                "operational health."
            )
        self._health[state] += 1

    def record_composition(self, state: CompositionState) -> None:
        if not isinstance(state, CompositionState):
            raise CallStateMergeError(
                f"record_composition refuses {state!r}: only a CompositionState "
                "is sample composition."
            )
        self._composition[state] += 1

    def health(self, state: HealthState) -> int:
        return self._health[state]

    def composition(self, state: CompositionState) -> int:
        return self._composition[state]

    def health_total(self) -> int:
        """Requests made. Never a sample size."""
        return sum(self._health.values())

    def composition_total(self) -> int:
        """Sample rows classified. Never a request count."""
        return sum(self._composition.values())

    def combined_total(self) -> int:
        """Structurally unavailable. Health and composition never merge."""
        raise CallStateMergeError(
            "operational health and sample composition never merge: "
            "call health_total() or composition_total(), never both summed. "
            "A rate_limited request is not an excluded_ineligible row."
        )

    def as_report(self) -> dict[str, dict[str, int]]:
        """Two named families, never one flat dictionary."""
        return {
            "health": {s.value: self._health[s] for s in HealthState},
            "composition": {s.value: self._composition[s] for s in CompositionState},
        }
