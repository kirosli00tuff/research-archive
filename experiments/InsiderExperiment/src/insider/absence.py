"""Absence is a recorded state, never a synthesized value.

AiTrader Level 4 computed whale scores from two empty tables and emitted
plausible numbers. Nothing here carries a value forward, fills a gap,
interpolates, or substitutes a default for a missing observation. Absence is a
type the rest of the code must handle explicitly, and it refuses coercion to a
number so a plausible zero cannot leak into an average.
"""

from __future__ import annotations

from enum import StrEnum
from typing import Final, TypeVar

T = TypeVar("T")


class AbsenceReason(StrEnum):
    """Why a value is absent. Recorded alongside the absence itself."""

    NO_BAR = "no_bar"
    NO_SHARES_OUTSTANDING = "no_shares_outstanding"
    NO_PRICE_ON_FILING = "no_price_on_filing"
    INSUFFICIENT_HISTORY = "insufficient_history"
    NON_FINITE = "non_finite"
    ZERO_DENOMINATOR = "zero_denominator"
    NOT_IN_UNIVERSE = "not_in_universe"
    FLAG_NOT_REPORTED = "flag_not_reported"
    EMPTY_BOOK = "empty_book"


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

NO_BAR: Final = Absent(AbsenceReason.NO_BAR)
NO_SHARES_OUTSTANDING: Final = Absent(AbsenceReason.NO_SHARES_OUTSTANDING)
NO_PRICE_ON_FILING: Final = Absent(AbsenceReason.NO_PRICE_ON_FILING)
INSUFFICIENT_HISTORY: Final = Absent(AbsenceReason.INSUFFICIENT_HISTORY)
NON_FINITE: Final = Absent(AbsenceReason.NON_FINITE)
ZERO_DENOMINATOR: Final = Absent(AbsenceReason.ZERO_DENOMINATOR)
NOT_IN_UNIVERSE: Final = Absent(AbsenceReason.NOT_IN_UNIVERSE)
FLAG_NOT_REPORTED: Final = Absent(AbsenceReason.FLAG_NOT_REPORTED)
EMPTY_BOOK: Final = Absent(AbsenceReason.EMPTY_BOOK)


def is_absent(value: object) -> bool:
    """True when the value is a recorded absence."""
    return isinstance(value, Absent)


def require_present[T](value: Maybe[T], context: str) -> T:
    """Unwrap a value or raise. Use where an absence is a programming error."""
    if isinstance(value, Absent):
        raise ValueError(f"{context}: value is absent ({value.reason.value})")
    return value
