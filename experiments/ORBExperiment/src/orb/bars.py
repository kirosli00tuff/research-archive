"""The typed bar carrier, and the provenance that decides who may hold one.

**This is a latched module.** It names priced fields, which every Stage A
collection module is forbidden to do. The guarantee that replaces the blindness
pin here is stronger and structural: **no Stage A module imports this one**, and
every value that enters it carries a :class:`Provenance` saying where it came
from. `orb.signal` and `orb.universe` refuse a bar whose provenance is a live
vendor read until the Stage C latch exists.

The three provenances, and why the split is the whole safety property:

- ``SYNTHETIC_FIXTURE`` — constructed in a test with a known answer. Always
  readable; it is not data about the world.
- ``PRE_PERIOD`` — a real bar stamped **strictly before**
  2016-01-04T14:30:00.000Z. Readable under the registered carve-out, and gated
  by `orb.preperiod` so the boundary is enforced rather than asserted.
- ``SEALED_VENDOR`` — a real bar inside the registered windows. **Refused
  everywhere until the Stage C latch is written.**
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum, unique
from typing import final

from orb.preperiod import is_pre_period


@unique
class Provenance(StrEnum):
    SYNTHETIC_FIXTURE = "synthetic_fixture"
    PRE_PERIOD = "pre_period"
    SEALED_VENDOR = "sealed_vendor"


class ProvenanceViolationError(PermissionError):
    """Raised when a latched module is handed a bar it may not read yet."""


@final
@dataclass(frozen=True, slots=True)
class Bar:
    """One minute bar, in integer cents. Money is never a float here."""

    timestamp_ms: int
    open_c: int
    high_c: int
    low_c: int
    close_c: int
    volume: int
    provenance: Provenance

    def __post_init__(self) -> None:
        if self.high_c < self.low_c:
            raise ValueError(f"high {self.high_c} below low {self.low_c}")
        if not (self.low_c <= self.open_c <= self.high_c):
            raise ValueError("open outside the high-low range")
        if not (self.low_c <= self.close_c <= self.high_c):
            raise ValueError("close outside the high-low range")
        if self.volume < 0:
            raise ValueError(f"negative volume {self.volume}")
        if self.provenance is Provenance.PRE_PERIOD and not is_pre_period(
            self.timestamp_ms
        ):
            raise ValueError(
                f"bar stamped {self.timestamp_ms} claims PRE_PERIOD provenance but "
                "sits at or after the carve-out boundary"
            )


def require_readable(bars: tuple[Bar, ...], context: str, *, latched: bool) -> None:
    """Refuse a sealed-vendor bar unless the Stage C latch has been written."""
    if latched:
        return
    offenders = {b.provenance for b in bars if b.provenance is Provenance.SEALED_VENDOR}
    if offenders:
        raise ProvenanceViolationError(
            f"{context}: refusing {len(bars)} bars carrying SEALED_VENDOR "
            "provenance. The universe, signal and verdict modules are built "
            "dark and are never pointed at real bars before the Stage C latch."
        )
