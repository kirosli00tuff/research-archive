"""Absence is a recorded state, never a synthesized value.

Ported by shape from InsiderExperiment. Nothing here carries a value forward,
fills a gap, interpolates, or substitutes a default for a missing observation.
Absence is a type the rest of the code must handle explicitly, and it refuses
coercion to a number so a plausible zero cannot leak into a sum of funding
hours or a coverage share.
"""

from __future__ import annotations

from enum import StrEnum
from typing import Final


class AbsenceReason(StrEnum):
    """Why a value is absent. Recorded alongside the absence itself."""

    NO_CANDLES = "no_candles"
    NO_FUNDING_ROWS = "no_funding_rows"
    BLINDNESS_GATED = "blindness_gated"
    NOT_SERVED = "not_served"
    NON_FINITE = "non_finite"
    ZERO_DENOMINATOR = "zero_denominator"
    PENDING_HORIZON = "pending_horizon"
    NO_CONTROL_CANDIDATE = "no_control_candidate"


class Absent:
    """A recorded absence. Immutable, falsy, and never coercible to a number."""

    __slots__ = ("reason",)

    reason: AbsenceReason

    def __init__(self, reason: AbsenceReason) -> None:
        object.__setattr__(self, "reason", reason)

    def __setattr__(self, name: str, value: object) -> None:
        raise AttributeError("Absent is immutable")

    def __bool__(self) -> bool:
        return False

    def __repr__(self) -> str:
        return f"Absent({self.reason.value})"

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Absent) and other.reason is self.reason

    def __hash__(self) -> int:
        return hash(("Absent", self.reason))

    def __float__(self) -> float:
        raise TypeError(
            "refusing to coerce a recorded absence to a float. "
            "Handle AbsenceReason explicitly or drop the row."
        )

    def __index__(self) -> int:
        raise TypeError("refusing to coerce a recorded absence to an int")


type Maybe[T] = T | Absent

NO_CANDLES: Final = Absent(AbsenceReason.NO_CANDLES)
NO_FUNDING_ROWS: Final = Absent(AbsenceReason.NO_FUNDING_ROWS)
BLINDNESS_GATED: Final = Absent(AbsenceReason.BLINDNESS_GATED)
NOT_SERVED: Final = Absent(AbsenceReason.NOT_SERVED)
NON_FINITE: Final = Absent(AbsenceReason.NON_FINITE)
ZERO_DENOMINATOR: Final = Absent(AbsenceReason.ZERO_DENOMINATOR)
PENDING_HORIZON: Final = Absent(AbsenceReason.PENDING_HORIZON)
NO_CONTROL_CANDIDATE: Final = Absent(AbsenceReason.NO_CONTROL_CANDIDATE)


def is_absent(value: object) -> bool:
    """True when the value is a recorded absence."""
    return isinstance(value, Absent)


def require_present[T](value: Maybe[T], context: str) -> T:
    """Unwrap a value or raise. Use where an absence is a programming error."""
    if isinstance(value, Absent):
        raise ValueError(f"{context}: value is absent ({value.reason.value})")
    return value
