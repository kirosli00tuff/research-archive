"""Guard 1 — recorded absence.

A missing implied volatility where a number will later stand is **not a zero**,
and an unreachable venue's cost is **not zero cost**. :class:`Absent` records
*why* a value is missing and refuses every operation that would let it silently
become a number: no ``float()``, no ``int()``, no indexing, no arithmetic, no
ordering, no truth value.

The failure this prevents is the one the standing rules name directly — "never
synthesize a value for an unreachable venue". A synthesized zero is
indistinguishable from a measured zero once it is written down, and a verdict
computed over synthesized zeros is a verdict about the synthesis.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum, unique
from typing import Never, final


@unique
class AbsenceReason(StrEnum):
    """Why a value is absent. Never merged with an operational call state."""

    NOT_SERVED = "not_served"
    """The endpoint answered and served no value for this key."""

    VENUE_BLOCKED = "venue_blocked"
    """The venue prohibits Canadian residents. A measured finding, never
    a zero and never worked around."""

    VENUE_CAPITAL_BLOCKED = "venue_capital_blocked"
    """The venue is permitted but the sleeve supports fewer than one position.
    Distinct from prohibited and distinct from reachable."""

    VENUE_UNCLEAR = "venue_unclear"
    """The venue's published policy does not resolve Canada or British
    Columbia either way. Unclear is a recorded state, not a permission."""

    SEALED = "sealed"
    """The value exists but sits behind a seal this caller may not open."""

    LATCH_UNSPENT = "latch_unspent"
    """The real-data latch has not been opened. Blindness holds."""

    NOT_YET_MEASURED = "not_yet_measured"
    """A figure this repository has registered as a measurement target."""

    TRUNCATED_LEDGER_LINE = "truncated_ledger_line"
    """A ledger line did not parse. Reported, never repaired."""

    INSUFFICIENT_SAMPLE = "insufficient_sample"
    """Fewer observations than the registered minimum. Never extrapolated."""


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

    def __floor__(self) -> Never:
        self._refuse("floor()")

    def __ceil__(self) -> Never:
        self._refuse("ceil()")

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

    def __pow__(self, other: object) -> Never:
        self._refuse("exponentiation")

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
