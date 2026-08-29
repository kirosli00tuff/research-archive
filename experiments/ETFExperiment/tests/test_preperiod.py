"""The fifth guard: the pre-period date pin, with fixtures ON the boundary."""

from __future__ import annotations

import pytest

from etf.absence import PRE_PERIOD_GATED
from etf.config import CONFIG
from etf.preperiod import PrePeriodViolation, gate_pre_period, is_pre_period, require_pre_period

BOUNDARY_MS = CONFIG.pre_period_end_ms
ONE_MS_BEFORE = BOUNDARY_MS - 1


def test_the_registered_boundary_is_2025_05_01T00_00_00Z() -> None:
    assert CONFIG.pre_period_end_date == "2025-05-01"
    assert BOUNDARY_MS == 1_746_057_600_000


def test_one_millisecond_before_the_boundary_is_inside_the_carve_out() -> None:
    assert is_pre_period(ONE_MS_BEFORE)
    assert require_pre_period(ONE_MS_BEFORE, "power input") == ONE_MS_BEFORE
    assert gate_pre_period(ONE_MS_BEFORE, 0.0001) == 0.0001


def test_the_boundary_instant_itself_is_refused() -> None:
    """Exclusive, and the fixture sits exactly on it.

    2025-05-01T00:00:00.000Z is the first instant of the test sample. Serving
    it through the carve-out would read one hour of the sample the design must
    stay blind to.
    """
    assert not is_pre_period(BOUNDARY_MS)
    with pytest.raises(PrePeriodViolation, match="at or after the registered pre-period"):
        require_pre_period(BOUNDARY_MS, "power input")
    assert gate_pre_period(BOUNDARY_MS, 0.0001) == PRE_PERIOD_GATED


def test_a_post_boundary_read_returns_an_absence_that_refuses_coercion() -> None:
    gated = gate_pre_period(BOUNDARY_MS + 86_400_000, 0.0001)
    assert gated == PRE_PERIOD_GATED
    with pytest.raises(TypeError, match="refusing to coerce"):
        float(gated)


def test_the_refusal_names_the_boundary_so_the_operator_can_see_the_arithmetic() -> None:
    with pytest.raises(PrePeriodViolation) as exc:
        require_pre_period(BOUNDARY_MS, "A.2 Task 4 volatility input")
    message = str(exc.value)
    assert "A.2 Task 4 volatility input" in message
    assert "2025-05-01" in message
    assert str(BOUNDARY_MS) in message
