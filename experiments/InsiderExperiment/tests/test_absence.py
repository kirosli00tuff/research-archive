"""Absence is a recorded state, never a synthesized value."""

from __future__ import annotations

import pytest

from insider.absence import NO_BAR, AbsenceReason, Absent, is_absent, require_present


def test_an_absence_refuses_to_become_a_float() -> None:
    with pytest.raises(TypeError, match="refusing to coerce"):
        float(NO_BAR)


def test_an_absence_refuses_to_become_an_int() -> None:
    with pytest.raises(TypeError, match="refusing to coerce"):
        int(NO_BAR)


def test_an_absence_is_falsy_so_a_truth_test_cannot_admit_it() -> None:
    assert not NO_BAR
    assert bool(NO_BAR) is False


def test_an_absence_is_immutable() -> None:
    with pytest.raises(AttributeError, match="immutable"):
        NO_BAR.reason = AbsenceReason.NON_FINITE


def test_two_absences_of_the_same_reason_are_equal_and_hashable() -> None:
    assert Absent(AbsenceReason.NO_BAR) == NO_BAR
    assert Absent(AbsenceReason.NO_BAR) != Absent(AbsenceReason.NON_FINITE)
    assert len({Absent(AbsenceReason.NO_BAR), NO_BAR}) == 1


def test_require_present_raises_rather_than_substituting() -> None:
    assert require_present(3.0, "ctx") == 3.0
    with pytest.raises(ValueError, match="no_bar"):
        require_present(NO_BAR, "ctx")


def test_is_absent_distinguishes_absence_from_zero() -> None:
    assert is_absent(NO_BAR)
    assert not is_absent(0.0)
    assert not is_absent(None)
