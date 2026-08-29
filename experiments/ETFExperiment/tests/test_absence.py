"""Absence refuses to become a number. Every refusal path is exercised."""

from __future__ import annotations

import pytest

from etf.absence import (
    DASH_IN_CELL,
    NOT_SERVED,
    AbsenceReason,
    Absent,
    is_absent,
    require_present,
)


def test_absence_is_falsy_but_is_not_zero() -> None:
    assert not DASH_IN_CELL
    assert DASH_IN_CELL != 0
    assert is_absent(DASH_IN_CELL)


def test_float_coercion_is_refused() -> None:
    with pytest.raises(TypeError, match="refusing to coerce"):
        float(DASH_IN_CELL)


def test_int_coercion_is_refused() -> None:
    with pytest.raises(TypeError, match="refusing to coerce"):
        int(NOT_SERVED)


def test_index_coercion_is_refused() -> None:
    with pytest.raises(TypeError, match="refusing to coerce"):
        [1, 2, 3][NOT_SERVED]


def test_summing_an_absence_is_refused_in_both_directions() -> None:
    with pytest.raises(TypeError, match="refusing to sum"):
        _ = DASH_IN_CELL + 1.0
    with pytest.raises(TypeError, match="refusing to sum"):
        _ = 1.0 + DASH_IN_CELL


def test_absence_is_immutable() -> None:
    with pytest.raises(AttributeError):
        DASH_IN_CELL.reason = AbsenceReason.NOT_SERVED


def test_two_absences_of_the_same_reason_are_equal_and_hashable() -> None:
    assert Absent(AbsenceReason.DASH_IN_CELL) == DASH_IN_CELL
    assert Absent(AbsenceReason.DASH_IN_CELL) != NOT_SERVED
    assert len({DASH_IN_CELL, Absent(AbsenceReason.DASH_IN_CELL), NOT_SERVED}) == 2


def test_require_present_raises_with_the_reason_named() -> None:
    with pytest.raises(ValueError, match="dash_in_cell"):
        require_present(DASH_IN_CELL, "aggregate net flow for 2025-06-02")
    assert require_present(3.0, "context") == 3.0
