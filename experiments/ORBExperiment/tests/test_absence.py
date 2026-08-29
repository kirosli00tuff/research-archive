"""Guard 1 — a recorded absence refuses to become a number, in every direction."""

from __future__ import annotations

import pytest

from orb.absence import (
    AbsenceReason,
    Absent,
    AbsentCoercionError,
    is_absent,
    require_present,
)


def test_absent_refuses_float_and_int() -> None:
    missing = Absent(AbsenceReason.NOT_SERVED, "no bar for 2016-01-04")
    with pytest.raises(AbsentCoercionError):
        float(missing)
    with pytest.raises(AbsentCoercionError):
        int(missing)


def test_absent_refuses_addition_from_both_sides() -> None:
    """The failure mode is ``total += value``, so both directions must refuse."""
    missing = Absent(AbsenceReason.NOT_SERVED)
    with pytest.raises(AbsentCoercionError):
        _ = missing + 1
    with pytest.raises(AbsentCoercionError):
        _ = 1 + missing
    with pytest.raises(AbsentCoercionError):
        _ = sum([1, missing])


def test_absent_refuses_indexing_and_iteration() -> None:
    missing = Absent(AbsenceReason.SEALED)
    with pytest.raises(AbsentCoercionError):
        _ = missing[0]
    with pytest.raises(AbsentCoercionError):
        _ = list(missing)
    with pytest.raises(AbsentCoercionError):
        _ = len(missing)


def test_absent_refuses_truth_testing() -> None:
    """``if value:`` on an absence is the silent-zero bug wearing a hat."""
    missing = Absent(AbsenceReason.HALTED)
    with pytest.raises(AbsentCoercionError):
        _ = bool(missing)

    def branch_on(value: object) -> str:
        """Typed ``object`` so the checker cannot prove the branch unreachable.

        The bug this catches has exactly this shape: an absence reaching an
        ``if`` in code that has lost track of what it is holding.
        """
        return "present" if value else "empty"

    with pytest.raises(AbsentCoercionError):
        branch_on(missing)


def test_absent_refuses_ordering() -> None:
    missing = Absent(AbsenceReason.NOT_YET_MEASURED)
    with pytest.raises(AbsentCoercionError):
        _ = missing > 0
    with pytest.raises(AbsentCoercionError):
        _ = missing < 0


def test_absent_carries_its_reason_and_detail() -> None:
    missing = Absent(AbsenceReason.PRE_PERIOD_GATED, "ts 1451917800000")
    assert missing.reason is AbsenceReason.PRE_PERIOD_GATED
    assert "1451917800000" in missing.detail
    assert is_absent(missing)
    assert not is_absent(0.0)


def test_require_present_raises_rather_than_substituting() -> None:
    with pytest.raises(AbsentCoercionError, match="not_served"):
        require_present(Absent(AbsenceReason.NOT_SERVED), "cost model input")
    assert require_present(3.5, "cost model input") == 3.5


def test_every_absence_reason_is_distinct() -> None:
    values = [r.value for r in AbsenceReason]
    assert len(values) == len(set(values)), values
