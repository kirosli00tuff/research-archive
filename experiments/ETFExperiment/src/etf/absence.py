"""Absence is a recorded state, never a synthesized value.

Ported by shape from NPLExperiment and InsiderExperiment. Nothing here carries
a value forward, fills a gap, interpolates, or substitutes a default for a
missing observation. Absence is a type the rest of the code must handle
explicitly, and it refuses coercion to a number so a plausible zero cannot leak
into a flow sum, a funding sum, or a coverage share.

The specific hazard this repository faces: a flow table serves an em dash where
a number will later stand. A dash is not zero net flow. Coercing it to 0.0 puts
a fabricated flat day inside the 100M threshold band and silently changes the
trade count.
"""

from __future__ import annotations

from enum import StrEnum
from typing import Final


class AbsenceReason(StrEnum):
    """Why a value is absent. Recorded alongside the absence itself."""

    NOT_SERVED = "not_served"
    DASH_IN_CELL = "dash_in_cell"
    NO_CAPTURE_BEFORE_ANCHOR = "no_capture_before_anchor"
    NO_ARCHIVE_CAPTURE = "no_archive_capture"
    BLINDNESS_GATED = "blindness_gated"
    PRE_PERIOD_GATED = "pre_period_gated"
    NON_FINITE = "non_finite"
    ZERO_DENOMINATOR = "zero_denominator"
    UNDER_COVERED = "under_covered"


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

    def __int__(self) -> int:
        raise TypeError("refusing to coerce a recorded absence to an int")

    def __index__(self) -> int:
        raise TypeError("refusing to coerce a recorded absence to an int")

    def __add__(self, other: object) -> object:
        raise TypeError("refusing to sum a recorded absence")

    def __radd__(self, other: object) -> object:
        raise TypeError("refusing to sum a recorded absence")


type Maybe[T] = T | Absent

NOT_SERVED: Final = Absent(AbsenceReason.NOT_SERVED)
DASH_IN_CELL: Final = Absent(AbsenceReason.DASH_IN_CELL)
NO_CAPTURE_BEFORE_ANCHOR: Final = Absent(AbsenceReason.NO_CAPTURE_BEFORE_ANCHOR)
NO_ARCHIVE_CAPTURE: Final = Absent(AbsenceReason.NO_ARCHIVE_CAPTURE)
BLINDNESS_GATED: Final = Absent(AbsenceReason.BLINDNESS_GATED)
PRE_PERIOD_GATED: Final = Absent(AbsenceReason.PRE_PERIOD_GATED)
NON_FINITE: Final = Absent(AbsenceReason.NON_FINITE)
ZERO_DENOMINATOR: Final = Absent(AbsenceReason.ZERO_DENOMINATOR)
UNDER_COVERED: Final = Absent(AbsenceReason.UNDER_COVERED)


def is_absent(value: object) -> bool:
    """True when the value is a recorded absence."""
    return isinstance(value, Absent)


def require_present[T](value: Maybe[T], context: str) -> T:
    """Unwrap a value or raise. Use where an absence is a programming error."""
    if isinstance(value, Absent):
        raise ValueError(f"{context}: value is absent ({value.reason.value})")
    return value
