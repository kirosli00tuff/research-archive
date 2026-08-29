"""Guard 6 — the pre-period carve-out, and the only exception to blindness.

Power inputs may read US equity bars stamped **strictly before**
2016-01-04T14:30:00.000Z. Every other bar read is sealed.

The rationale, registered rather than convenient: 2016-01-04 is the first
session of the registered in-sample window, so the window before it sits
outside both the in-sample and the holdout samples, and reading it cannot leak
a single observation any verdict will be computed on. The E2 economic-power
computation needs a per-trade dispersion figure to size a net edge against a
modeled cost. Taking that from the test window would be reading the outcome to
plan the test of the outcome; inventing it would register a number this
repository did not measure.

The boundary lives in exactly one place, ``CONFIG.pre_period_end_ms``, and is
read from config by this module alone. The pin sits **exactly on** the
boundary: one millisecond before it passes, the instant itself is refused.
"""

from __future__ import annotations

from orb.absence import AbsenceReason, Absent, Maybe
from orb.config import CONFIG


class PrePeriodViolationError(PermissionError):
    """Raised when a bar at or after the boundary is read through the carve-out."""


def pre_period_end_ms() -> int:
    """The registered boundary, in epoch milliseconds. Exclusive."""
    return CONFIG.pre_period_end_ms


def is_pre_period(timestamp_ms: int) -> bool:
    """True when ``timestamp_ms`` is strictly before the boundary."""
    return timestamp_ms < CONFIG.pre_period_end_ms


def require_pre_period(timestamp_ms: int, context: str) -> int:
    """Refuse loudly. Used where a caller asserts it is inside the carve-out."""
    if not is_pre_period(timestamp_ms):
        raise PrePeriodViolationError(
            f"{context}: bar stamped {timestamp_ms} sits at or after the "
            f"pre-period boundary {CONFIG.pre_period_end_ms} "
            "(2016-01-04T14:30:00.000Z, exclusive). Reading it would read an "
            "observation the verdict will be computed on."
        )
    return timestamp_ms


def gate_pre_period[T](timestamp_ms: int, value: T) -> Maybe[T]:
    """Pass a value through only when it is stamped before the boundary.

    A value at or after the boundary comes back as :class:`Absent`, which
    refuses coercion to a number, so a gated row cannot be summed by accident.
    """
    if is_pre_period(timestamp_ms):
        return value
    return Absent(
        AbsenceReason.PRE_PERIOD_GATED,
        f"timestamp {timestamp_ms} >= pre_period_end_ms {CONFIG.pre_period_end_ms}",
    )
