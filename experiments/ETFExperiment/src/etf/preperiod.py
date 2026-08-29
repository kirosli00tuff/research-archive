"""The fifth guard: the pre-period date pin.

The one registered exception to outcome blindness. Power inputs may read BTC
price and funding data stamped **strictly before 2025-05-01** — inside the
source study's own sample (January 2024 to April 2025) and outside this test
sample, which begins 2025-05-01. Every other price or funding read is sealed
until the registered Stage B read.

This module is the enforcement site named in CLAUDE.md and in REGISTRATION.md
Section 9. A read stamped at or after the boundary raises here; it does not
return a plausible value, and it does not return silently.

The boundary is exclusive on purpose and the tests sit exactly on it: a fixture
at 2025-04-30T23:59:59.999Z passes and one at 2025-05-01T00:00:00.000Z is
refused. A fixture comfortably inside a boundary lets a moved threshold pass
unnoticed (InsiderExperiment mutation lesson).
"""

from __future__ import annotations

from etf.absence import PRE_PERIOD_GATED, Absent
from etf.config import CONFIG


class PrePeriodViolation(RuntimeError):
    """A price or funding read reached the pre-period reader stamped on or after the pin."""


def is_pre_period(timestamp_ms: int) -> bool:
    """True only strictly before the registered pre-period boundary."""
    return timestamp_ms < CONFIG.pre_period_end_ms


def require_pre_period(timestamp_ms: int, context: str) -> int:
    """Return the timestamp, or refuse loudly. The carve-out's enforcement site."""
    if not is_pre_period(timestamp_ms):
        raise PrePeriodViolation(
            f"{context}: refusing a price or funding read stamped {timestamp_ms} ms, at or "
            f"after the registered pre-period boundary {CONFIG.pre_period_end_ms} ms "
            f"({CONFIG.pre_period_end_date}T00:00:00Z). The carve-out covers power inputs "
            f"strictly before that instant and nothing else; everything at or after it is "
            f"sealed until the registered Stage B read."
        )
    return timestamp_ms


def gate_pre_period(timestamp_ms: int, value: float) -> float | Absent:
    """Serve a value only inside the carve-out; outside it, a recorded absence."""
    if is_pre_period(timestamp_ms):
        return value
    return PRE_PERIOD_GATED
