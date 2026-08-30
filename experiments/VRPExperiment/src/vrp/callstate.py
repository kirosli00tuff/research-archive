"""Guard 4 — operational health and sample composition never merge.

Two families of state, separate types, no common supertype, no arithmetic
across them. A venue that **refuses Canadian residents** is a composition fact
about the venue set; a venue whose **endpoint returned 429** is an operational
fact about one request. Merging them would let a rate limit be counted as a
jurisdiction block, which is exactly the error this repository exists not to
make.
"""

from __future__ import annotations

from enum import StrEnum, unique
from typing import final


@unique
class HealthState(StrEnum):
    """What happened to the request. Never a statement about the venue set."""

    STORED = "stored"
    """Bytes were served and sealed."""

    NO_DATA = "no_data"
    """The endpoint answered successfully and served nothing."""

    SOURCE_FAILED = "source_failed"
    """A 5xx, a timeout, or an unparseable envelope."""

    RATE_LIMITED = "rate_limited"
    """The endpoint refused on a limit. Never a no_data, never a block."""

    ACCESS_REFUSED = "access_refused"
    """A 401/403 on a public endpoint: an account was demanded. This is an
    operational refusal, not a jurisdiction finding — a jurisdiction finding
    comes from published policy text, never from a status code."""


@unique
class VenueState(StrEnum):
    """What the venue set is made of. Never a statement about a request."""

    PERMITTED = "permitted"
    """Published policy permits Canadian and British Columbia residents."""

    PROHIBITED = "prohibited"
    """Published policy prohibits Canadian residents. Measured, never
    worked around."""

    CAPITAL_BLOCKED = "capital_blocked"
    """Permitted, but the sleeve supports fewer than one position."""

    UNCLEAR = "unclear"
    """Published policy does not resolve Canada or British Columbia. Unclear
    is a recorded state and is never read as permission."""

    NO_PRODUCT = "no_product"
    """The venue is reachable but lists no option product to measure."""


CALL_STATES: tuple[str, ...] = tuple(
    [s.value for s in HealthState] + [s.value for s in VenueState]
)
"""The ten registered states, health first, venue second."""


class CallStateMergeError(TypeError):
    """Raised when health and venue classification are asked to combine."""


@final
class CallStateTally:
    """Counts the two families side by side and refuses to add across them."""

    __slots__ = ("_health", "_venue")

    def __init__(self) -> None:
        self._health: dict[HealthState, int] = dict.fromkeys(HealthState, 0)
        self._venue: dict[VenueState, int] = dict.fromkeys(VenueState, 0)

    def record_health(self, state: HealthState) -> None:
        if not isinstance(state, HealthState):
            raise CallStateMergeError(
                f"record_health refuses {state!r}: only a HealthState is "
                "operational health. A venue classification is not a request."
            )
        self._health[state] += 1

    def record_venue(self, state: VenueState) -> None:
        if not isinstance(state, VenueState):
            raise CallStateMergeError(
                f"record_venue refuses {state!r}: only a VenueState classifies "
                "a venue. A rate limit is not a jurisdiction block."
            )
        self._venue[state] += 1

    def health(self, state: HealthState) -> int:
        return self._health[state]

    def venue(self, state: VenueState) -> int:
        return self._venue[state]

    def health_total(self) -> int:
        """Requests made. Never a venue count."""
        return sum(self._health.values())

    def venue_total(self) -> int:
        """Venues classified. Never a request count."""
        return sum(self._venue.values())

    def combined_total(self) -> int:
        """Structurally unavailable. The two families never merge."""
        raise CallStateMergeError(
            "operational health and venue classification never merge: call "
            "health_total() or venue_total(), never both summed. A "
            "rate_limited request is not a prohibited venue, and an "
            "access_refused status code is not a jurisdiction finding."
        )

    def as_report(self) -> dict[str, dict[str, int]]:
        """Two named families, never one flat dictionary."""
        return {
            "health": {s.value: self._health[s] for s in HealthState},
            "venue": {s.value: self._venue[s] for s in VenueState},
        }
