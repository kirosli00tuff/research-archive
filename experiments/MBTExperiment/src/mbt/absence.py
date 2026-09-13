"""Guard five — recorded absence. An absence is a state, never a value.

Ported by copying from VRPExperiment's ``absence`` module and widened with the
reasons this repository can actually produce.

A missing quote where a number will later stand is **not a zero**, and an
unavailable live session is **not a margin of zero**. :class:`Absent` records
*why* a value is missing and refuses every operation that would let it silently
become a number: no ``float()``, no ``int()``, no indexing, no arithmetic, no
ordering, no truth value.

The failure this prevents is specific. A synthesized zero is indistinguishable
from a measured zero once it is written down, and a verdict computed over
synthesized zeros is a verdict about the synthesis. Refusing ``__bool__`` matters
as much as refusing ``float``: ``if spread:`` on an absent spread would otherwise
take the false branch and read as a deliberate choice.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum, unique
from typing import Never, final


@unique
class AbsenceReason(StrEnum):
    """Why a value is absent. Never merged with an operational call state."""

    # --- session and environment -------------------------------------
    NO_LIVE_SESSION = "no_live_session"
    """The figure is a property of the ACCOUNT and needs a U-prefixed session.
    The paper-only clause is in force, so no live session runs here."""

    GATEWAY_UNREACHABLE = "gateway_unreachable"
    """No listener answered on the configured Gateway port. Distinct from
    NO_LIVE_SESSION: it says nothing about which environment is blocked."""

    # --- venue and schedule ------------------------------------------
    NOT_SERVED = "not_served"
    """The venue or broker answered and served no value for this key."""

    PAPER_SYNTHETIC = "paper_synthetic"
    """The value exists in the paper environment but measures the simulator
    rather than the venue. A paper commission report is the example."""

    # --- market data refusals, one per registered refusal condition ---
    UNQUOTED_LEG = "unquoted_leg"
    """A leg carried no bid or no ask at the observation instant."""

    CROSSED_BOOK = "crossed_book"
    """Bid exceeded ask. A crossed book is a broken book, never a zero spread."""

    ZERO_BID = "zero_bid"
    """The bid was zero or negative. A zero bid is not a price."""

    STALE_TIMESTAMP = "stale_timestamp"
    """The venue stamp trailed local capture beyond the registered tolerance."""

    DELAYED_TICK = "delayed_tick"
    """The feed served delayed data. A delayed quote carries a stale and
    artificially wide spread and is inadmissible, never widened into a band."""

    FROZEN_TICK = "frozen_tick"
    """The feed served a frozen last-known snapshot rather than a live book."""

    # --- sample and measurement --------------------------------------
    INSUFFICIENT_SAMPLE = "insufficient_sample"
    """Fewer observations than the registered minimum. Never extrapolated."""

    NOT_YET_MEASURED = "not_yet_measured"
    """A figure this repository has registered as a measurement target."""

    PERMISSION_UNKNOWN = "permission_unknown"
    """Account permission could not be asked. Distinct from permission absent,
    and never merged with it: one says nothing about the account."""


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

    def as_row(self) -> dict[str, str]:
        """The only sanctioned way an absence reaches an artifact."""
        return {"absent": "true", "reason": str(self.reason), "detail": self.detail}

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

    def __rpow__(self, other: object) -> Never:
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
