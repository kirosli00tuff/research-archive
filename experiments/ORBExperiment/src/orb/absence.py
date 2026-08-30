"""Guard 1 — recorded absence.

A missing bar where a number will later stand is **not a zero**. `Absent`
records *why* a value is missing and refuses every operation that would let it
silently become a number: no ``float()``, no ``int()``, no indexing, no
addition, no comparison, no truth value.

The failure this prevents was measured elsewhere in this house: a synthesized
zero is indistinguishable from a measured zero once it is written down, and a
verdict computed over synthesized zeros is a verdict about the synthesis.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from typing import Never, final


class AbsenceReason(StrEnum):
    """Why a value is absent. Never merged with an operational call state."""

    NOT_SERVED = "not_served"
    """The vendor served no value for this key."""

    SEALED = "sealed"
    """The value exists but sits behind a seal this caller may not open."""

    PRE_PERIOD_GATED = "pre_period_gated"
    """The value is stamped at or after the pre-period boundary."""

    NOT_YET_MEASURED = "not_yet_measured"
    """A figure this repository has registered as a measurement target."""

    HALTED = "halted"
    """The session was halted; no bar exists to be missing."""

    TRUNCATED_LEDGER_LINE = "truncated_ledger_line"
    """A ledger line did not parse. Reported, never repaired."""


class AbsentCoercionError(TypeError):
    """Raised whenever an :class:`Absent` is asked to behave like a number."""


@final
@dataclass(frozen=True, slots=True)
class Absent:
    """A recorded absence. Refuses to become a number, in every direction."""

    reason: AbsenceReason
    detail: str = ""

    def _refuse(self, op: str) -> Never:
        raise AbsentCoercionError(
            f"Absent({self.reason}) refuses {op}: "
            f"a recorded absence is never a value. detail={self.detail!r}"
        )

    # Numeric coercion --------------------------------------------------
    def __float__(self) -> Never:
        self._refuse("float()")

    def __int__(self) -> Never:
        self._refuse("int()")

    def __index__(self) -> Never:
        self._refuse("__index__")

    def __complex__(self) -> Never:
        self._refuse("complex()")

    def __round__(self, ndigits: int | None = None) -> Never:
        self._refuse("round()")

    # Arithmetic --------------------------------------------------------
    def __add__(self, other: object) -> Never:
        self._refuse("addition")

    def __radd__(self, other: object) -> Never:
        self._refuse("addition")

    def __sub__(self, other: object) -> Never:
        self._refuse("subtraction")

    def __rsub__(self, other: object) -> Never:
        self._refuse("subtraction")

    def __mul__(self, other: object) -> Never:
        self._refuse("multiplication")

    def __rmul__(self, other: object) -> Never:
        self._refuse("multiplication")

    def __truediv__(self, other: object) -> Never:
        self._refuse("division")

    def __rtruediv__(self, other: object) -> Never:
        self._refuse("division")

    def __neg__(self) -> Never:
        self._refuse("negation")

    def __abs__(self) -> Never:
        self._refuse("abs()")

    # Ordering and truth ------------------------------------------------
    def __lt__(self, other: object) -> Never:
        self._refuse("ordering")

    def __le__(self, other: object) -> Never:
        self._refuse("ordering")

    def __gt__(self, other: object) -> Never:
        self._refuse("ordering")

    def __ge__(self, other: object) -> Never:
        self._refuse("ordering")

    def __bool__(self) -> Never:
        self._refuse("truth testing")

    # Containers --------------------------------------------------------
    def __getitem__(self, key: object) -> Never:
        self._refuse("indexing")

    def __iter__(self) -> Never:
        self._refuse("iteration")

    def __len__(self) -> Never:
        self._refuse("len()")


type Maybe[T] = T | Absent
"""A value that may be recorded-absent. Callers must narrow before arithmetic."""


def is_absent(value: object) -> bool:
    """True when ``value`` is a recorded absence."""
    return isinstance(value, Absent)


def require_present[T](value: Maybe[T], context: str) -> T:
    """Narrow a :data:`Maybe`, raising loudly rather than substituting a value."""
    if isinstance(value, Absent):
        raise AbsentCoercionError(
            f"{context}: required a present value, found Absent({value.reason}). "
            f"detail={value.detail!r}"
        )
    return value
