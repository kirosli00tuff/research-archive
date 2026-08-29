"""Guard 6 — the pre-period carve-out, pinned exactly on its boundary.

The registered boundary is ``2016-01-04T14:30:00.000Z``, exclusive. The
fixtures below sit **on** it: one millisecond before passes, the instant itself
is refused. A fixture comfortably inside the boundary would let a moved
threshold pass unnoticed — the InsiderExperiment mutation lesson.
"""

from __future__ import annotations

from datetime import UTC, datetime

import pytest

from orb.absence import Absent, AbsentCoercionError
from orb.config import CONFIG
from orb.preperiod import (
    PrePeriodViolationError,
    gate_pre_period,
    is_pre_period,
    pre_period_end_ms,
    require_pre_period,
)

BOUNDARY_MS = CONFIG.pre_period_end_ms
ONE_MS_BEFORE = BOUNDARY_MS - 1
ONE_MS_AFTER = BOUNDARY_MS + 1


def test_the_boundary_is_the_registered_instant() -> None:
    """The literal is what the registration says it is, to the millisecond."""
    resolved = datetime.fromtimestamp(BOUNDARY_MS / 1000, tz=UTC)
    assert resolved == datetime(2016, 1, 4, 14, 30, 0, tzinfo=UTC)
    assert pre_period_end_ms() == BOUNDARY_MS


def test_the_boundary_is_0930_eastern_on_the_first_in_sample_session() -> None:
    """14:30Z is 09:30 Eastern on 2016-01-04, which is standard time."""
    from orb.sessionclock import is_daylight_time, session_open_utc

    session = datetime(2016, 1, 4, tzinfo=UTC).date()
    assert not is_daylight_time(session)
    assert session_open_utc(session) == datetime(2016, 1, 4, 14, 30, tzinfo=UTC)


def test_one_millisecond_before_the_boundary_passes() -> None:
    assert is_pre_period(ONE_MS_BEFORE)
    assert require_pre_period(ONE_MS_BEFORE, "power input") == ONE_MS_BEFORE


def test_the_boundary_instant_itself_is_refused() -> None:
    """Exclusive means exclusive. This is the fixture that binds."""
    assert not is_pre_period(BOUNDARY_MS)
    with pytest.raises(PrePeriodViolationError):
        require_pre_period(BOUNDARY_MS, "power input")


def test_one_millisecond_after_the_boundary_is_refused() -> None:
    assert not is_pre_period(ONE_MS_AFTER)
    with pytest.raises(PrePeriodViolationError):
        require_pre_period(ONE_MS_AFTER, "power input")


def test_the_gate_passes_a_pre_period_value_through_unchanged() -> None:
    assert gate_pre_period(ONE_MS_BEFORE, 12.5) == 12.5


def test_the_gate_returns_a_recorded_absence_at_the_boundary() -> None:
    """A gated row cannot be summed by accident: it refuses arithmetic."""
    gated = gate_pre_period(BOUNDARY_MS, 12.5)
    assert isinstance(gated, Absent)
    assert gated.reason.value == "pre_period_gated"
    with pytest.raises(AbsentCoercionError):
        _ = gated + 1.0
    with pytest.raises(AbsentCoercionError):
        _ = float(gated)


def test_the_gate_refuses_after_the_boundary() -> None:
    assert isinstance(gate_pre_period(ONE_MS_AFTER, 12.5), Absent)
