"""Guard 6 — the carve-out, pinned exactly on all four of its edges.

**Amendment 11 made the carve-out two-sided.** The permitted region is any bar
stamped **strictly before** ``2016-01-04T14:30:00.000Z`` or **at or after**
``2026-07-01T04:00:00.000Z`` — which is ``2026-07-01T00:00:00.000`` US Eastern
(EDT, UTC-04:00). Everything between is sealed.

The fixtures below sit **on** all four edges, because a fixture comfortably
inside a boundary lets a moved threshold pass unnoticed — the InsiderExperiment
mutation lesson, and the reason mutation 4 exists:

1. one millisecond **before** 2016-01-04T14:30:00.000Z **passes**;
2. that instant itself is **refused**;
3. the **last instant of 2026-06-30** Eastern is **refused**;
4. the **first instant of 2026-07-01** Eastern **passes**.
"""

from __future__ import annotations

from datetime import UTC, datetime

import pytest

from orb.absence import Absent, AbsentCoercionError
from orb.config import CONFIG
from orb.preperiod import (
    PrePeriodViolationError,
    gate_pre_period,
    is_carve_out,
    is_post_holdout,
    is_pre_period,
    post_holdout_start_ms,
    pre_period_end_ms,
    require_carve_out,
    require_pre_period,
)

BOUNDARY_MS = CONFIG.pre_period_end_ms
ONE_MS_BEFORE = BOUNDARY_MS - 1
ONE_MS_AFTER = BOUNDARY_MS + 1

POST_MS = CONFIG.post_holdout_start_ms
LAST_MS_OF_HOLDOUT = POST_MS - 1
"""Edge 3: 2026-06-30T23:59:59.999 Eastern, the last instant of the holdout."""

FIRST_MS_AFTER_HOLDOUT = POST_MS
"""Edge 4: 2026-07-01T00:00:00.000 Eastern, the first instant outside it."""


# --------------------------------------------------------------------------
# The two boundaries are the registered instants, to the millisecond
# --------------------------------------------------------------------------


def test_the_boundary_is_the_registered_instant() -> None:
    """The literal is what the registration says it is, to the millisecond."""
    resolved = datetime.fromtimestamp(BOUNDARY_MS / 1000, tz=UTC)
    assert resolved == datetime(2016, 1, 4, 14, 30, 0, tzinfo=UTC)
    assert pre_period_end_ms() == BOUNDARY_MS


def test_the_post_holdout_boundary_is_the_registered_instant() -> None:
    """2026-07-01T04:00:00.000Z, registered by Amendment 11."""
    resolved = datetime.fromtimestamp(POST_MS / 1000, tz=UTC)
    assert resolved == datetime(2026, 7, 1, 4, 0, 0, tzinfo=UTC)
    assert post_holdout_start_ms() == POST_MS


def test_the_boundary_is_0930_eastern_on_the_first_in_sample_session() -> None:
    """14:30Z is 09:30 Eastern on 2016-01-04, which is standard time."""
    from orb.sessionclock import is_daylight_time, session_open_utc

    session = datetime(2016, 1, 4, tzinfo=UTC).date()
    assert not is_daylight_time(session)
    assert session_open_utc(session) == datetime(2016, 1, 4, 14, 30, tzinfo=UTC)


def test_the_post_holdout_boundary_is_eastern_midnight_not_utc_midnight() -> None:
    """The distinction is the whole reason the boundary is where it is.

    UTC midnight on 2026-07-01 is **20:00 Eastern on 2026-06-30**, inside the
    last holdout session date. A carve-out beginning there would admit that
    session's after-hours bars. Eastern midnight admits nothing before
    2026-07-01, and 2026-07-01 is inside daylight time, so the offset is -4.
    """
    from orb.sessionclock import EASTERN, is_daylight_time

    eastern = datetime.fromtimestamp(POST_MS / 1000, tz=EASTERN)
    assert (eastern.year, eastern.month, eastern.day) == (2026, 7, 1)
    assert (eastern.hour, eastern.minute, eastern.second) == (0, 0, 0)
    assert is_daylight_time(eastern.date())

    utc_midnight_ms = int(datetime(2026, 7, 1, tzinfo=UTC).timestamp() * 1000)
    assert utc_midnight_ms < POST_MS, (
        "UTC midnight precedes the registered boundary by the Eastern offset"
    )
    assert not is_carve_out(utc_midnight_ms), (
        "UTC midnight on 2026-07-01 is 20:00 Eastern on 2026-06-30 and is sealed"
    )


# --------------------------------------------------------------------------
# Edge 1 and edge 2 — the pre-period boundary, unchanged by Amendment 11
# --------------------------------------------------------------------------


def test_one_millisecond_before_the_boundary_passes() -> None:
    """**Edge 1.**"""
    assert is_pre_period(ONE_MS_BEFORE)
    assert is_carve_out(ONE_MS_BEFORE)
    assert require_pre_period(ONE_MS_BEFORE, "power input") == ONE_MS_BEFORE
    assert require_carve_out(ONE_MS_BEFORE, "power input") == ONE_MS_BEFORE


def test_the_boundary_instant_itself_is_refused() -> None:
    """**Edge 2.** Exclusive means exclusive. This is the fixture that binds."""
    assert not is_pre_period(BOUNDARY_MS)
    assert not is_carve_out(BOUNDARY_MS)
    with pytest.raises(PrePeriodViolationError):
        require_pre_period(BOUNDARY_MS, "power input")
    with pytest.raises(PrePeriodViolationError):
        require_carve_out(BOUNDARY_MS, "power input")


def test_one_millisecond_after_the_boundary_is_refused() -> None:
    assert not is_pre_period(ONE_MS_AFTER)
    assert not is_carve_out(ONE_MS_AFTER)
    with pytest.raises(PrePeriodViolationError):
        require_pre_period(ONE_MS_AFTER, "power input")


# --------------------------------------------------------------------------
# Edge 3 and edge 4 — the post-holdout boundary, registered by Amendment 11
# --------------------------------------------------------------------------


def test_the_last_instant_of_the_holdout_is_refused() -> None:
    """**Edge 3.** 2026-06-30T23:59:59.999 Eastern is still the holdout."""
    assert not is_post_holdout(LAST_MS_OF_HOLDOUT)
    assert not is_carve_out(LAST_MS_OF_HOLDOUT)
    with pytest.raises(PrePeriodViolationError):
        require_pre_period(LAST_MS_OF_HOLDOUT, "dispersion input")
    with pytest.raises(PrePeriodViolationError):
        require_carve_out(LAST_MS_OF_HOLDOUT, "dispersion input")


def test_the_first_instant_after_the_holdout_passes() -> None:
    """**Edge 4.** 2026-07-01T00:00:00.000 Eastern is outside both windows."""
    assert is_post_holdout(FIRST_MS_AFTER_HOLDOUT)
    assert is_carve_out(FIRST_MS_AFTER_HOLDOUT)
    assert not is_pre_period(FIRST_MS_AFTER_HOLDOUT)
    assert (
        require_pre_period(FIRST_MS_AFTER_HOLDOUT, "dispersion input")
        == FIRST_MS_AFTER_HOLDOUT
    )
    assert (
        require_carve_out(FIRST_MS_AFTER_HOLDOUT, "dispersion input")
        == FIRST_MS_AFTER_HOLDOUT
    )


def test_the_sealed_window_between_the_two_edges_is_refused_throughout() -> None:
    """Everything between the edges is sealed, including both registered windows."""
    from datetime import date

    from orb.sessionclock import session_open_utc

    sealed_probes = [
        date(2016, 1, 4),  # first in-sample session
        date(2019, 7, 1),
        date(2022, 12, 30),  # last in-sample session
        date(2023, 1, 3),  # first holdout session
        date(2026, 6, 30),  # last holdout session
    ]
    for session in sealed_probes:
        stamp = int(session_open_utc(session).timestamp() * 1000)
        assert not is_carve_out(stamp), session
        with pytest.raises(PrePeriodViolationError):
            require_carve_out(stamp, "sealed probe")


# --------------------------------------------------------------------------
# The gate, on both halves
# --------------------------------------------------------------------------


def test_the_gate_passes_a_pre_period_value_through_unchanged() -> None:
    assert gate_pre_period(ONE_MS_BEFORE, 12.5) == 12.5


def test_the_gate_passes_a_post_holdout_value_through_unchanged() -> None:
    assert gate_pre_period(FIRST_MS_AFTER_HOLDOUT, 12.5) == 12.5


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


def test_the_gate_refuses_the_last_instant_of_the_holdout() -> None:
    gated = gate_pre_period(LAST_MS_OF_HOLDOUT, 12.5)
    assert isinstance(gated, Absent)
    with pytest.raises(AbsentCoercionError):
        _ = float(gated)
