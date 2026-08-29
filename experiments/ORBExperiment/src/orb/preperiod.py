"""Guard 6 — the carve-out, and the only exception to blindness.

**AMENDED 2026-08-29 by REGISTRATION.md Amendment 11. The carve-out is now
two-sided.** The original one-sided rule is preserved verbatim below so the
correction is auditable, exactly as standing rule 1 of Section 14 requires:

    Power inputs may read US equity bars stamped **strictly before**
    2016-01-04T14:30:00.000Z. Every other bar read is sealed.

**What falsified it.** A.1 TASK 5, 2026-08-29: neither credential serves any
session before 2016-01-04. Alpaca's earliest served session is **2016-01-04**,
which is exactly ``CONFIG.in_sample_start``, and Massive's is **2024-08-29**;
`n = 2` credentials, **0 serving the carve-out**. E2 power was therefore
recorded ``Absent(not_served)`` rather than computed. **The carve-out as first
registered was never reachable**, and that is a design assumption falsified by
measurement, in the same class as the secrets rule of CLAUDE.md rule 3.

**The amended carve-out, in force.** A bar is readable through the carve-out
when it is stamped **strictly before** ``CONFIG.pre_period_end_ms``
(2016-01-04T14:30:00.000Z, the opening instant of the first in-sample session)
**or at or after** ``CONFIG.post_holdout_start_ms`` (2026-07-01T04:00:00.000Z,
which is 2026-07-01T00:00:00.000 US Eastern, EDT, UTC-04:00). **Every other bar
read is sealed.**

**The rationale, and its cost, stated together.** Both regions sit outside the
in-sample and holdout windows, so reading either leaks no observation any
verdict will be computed on. **They are not equivalent.** A dispersion figure
estimated after 2026-06-30 reflects a regime **later** than the sample it will
be applied to, where a pre-2016 estimate would have reflected an **earlier**
one. Neither is neutral, and the amendment does not pretend otherwise: **the
compromise now runs forward rather than backward**, and a post-holdout
dispersion figure may misstate in-sample dispersion **in either direction by an
amount this repository has not measured and does not claim to bound.**

**The post-holdout region grows as real time advances and never intersects a
registered window.** The sessions actually used in any computation are recorded
in the append-only ledger **at the time of that computation**, never fixed in
advance here.

Both boundaries live in exactly one place each, ``CONFIG.pre_period_end_ms`` and
``CONFIG.post_holdout_start_ms``, and are read from config by this module alone.
**The pins sit exactly on all four edges**: one millisecond before the pre-period
boundary passes, the instant itself is refused, the last instant of 2026-06-30 is
refused, and the first instant of 2026-07-01 passes.
"""

from __future__ import annotations

from orb.absence import AbsenceReason, Absent, Maybe
from orb.config import CONFIG


class PrePeriodViolationError(PermissionError):
    """Raised when a bar outside the carve-out is read through it.

    The name is unchanged from the one-sided registration and is **not**
    renamed: it is already pushed, and Section 14 forbids editing a pushed
    line into something tidier. It now covers both edges of a two-sided window.
    """


def pre_period_end_ms() -> int:
    """The upper edge of the pre-period half, in epoch milliseconds. Exclusive."""
    return CONFIG.pre_period_end_ms


def post_holdout_start_ms() -> int:
    """The lower edge of the post-holdout half, in epoch milliseconds. Inclusive."""
    return CONFIG.post_holdout_start_ms


def is_pre_period(timestamp_ms: int) -> bool:
    """True when ``timestamp_ms`` is strictly before the pre-period boundary.

    **Unchanged in meaning by Amendment 11.** It answers the narrow question it
    always answered, and `orb.bars` still uses it to validate a bar claiming
    ``PRE_PERIOD`` provenance. The two-sided question is :func:`is_carve_out`.
    """
    return timestamp_ms < CONFIG.pre_period_end_ms


def is_post_holdout(timestamp_ms: int) -> bool:
    """True when ``timestamp_ms`` is at or after the post-holdout boundary."""
    return timestamp_ms >= CONFIG.post_holdout_start_ms


def is_carve_out(timestamp_ms: int) -> bool:
    """True inside either half of the amended two-sided carve-out."""
    return is_pre_period(timestamp_ms) or is_post_holdout(timestamp_ms)


def require_carve_out(timestamp_ms: int, context: str) -> int:
    """Refuse loudly. The two-sided check, under the name it will keep."""
    if not is_carve_out(timestamp_ms):
        raise PrePeriodViolationError(
            f"{context}: bar stamped {timestamp_ms} sits inside the sealed "
            f"window [{CONFIG.pre_period_end_ms}, "
            f"{CONFIG.post_holdout_start_ms}) — at or after the pre-period "
            "boundary 2016-01-04T14:30:00.000Z and before the post-holdout "
            "boundary 2026-07-01T04:00:00.000Z (2026-07-01T00:00:00.000 US "
            "Eastern, EDT, UTC-04:00). Reading it would read an observation "
            "the verdict will be computed on."
        )
    return timestamp_ms


def require_pre_period(timestamp_ms: int, context: str) -> int:
    """Refuse loudly. Used where a caller asserts it is inside the carve-out.

    **Amendment 11 made this a two-sided window check.** The name is unchanged
    because it is already pushed; the behaviour now admits the post-holdout
    half as well as the pre-period half.
    """
    return require_carve_out(timestamp_ms, context)


def gate_pre_period[T](timestamp_ms: int, value: T) -> Maybe[T]:
    """Pass a value through only when it is stamped inside the carve-out.

    **Amendment 11 made this a two-sided window check.** A value inside the
    sealed window comes back as :class:`Absent`, which refuses coercion to a
    number, so a gated row cannot be summed by accident.
    """
    if is_carve_out(timestamp_ms):
        return value
    return Absent(
        AbsenceReason.PRE_PERIOD_GATED,
        f"timestamp {timestamp_ms} sits inside the sealed window "
        f"[{CONFIG.pre_period_end_ms}, {CONFIG.post_holdout_start_ms})",
    )
