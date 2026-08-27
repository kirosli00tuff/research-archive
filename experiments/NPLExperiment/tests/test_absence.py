"""The recorded-absence type refuses numeric coercion. Ported guard 1."""

from __future__ import annotations

import pytest

from npl.absence import (
    BLINDNESS_GATED,
    NO_CANDLES,
    AbsenceReason,
    Absent,
    is_absent,
    require_present,
)


def test_an_absence_refuses_coercion_to_float() -> None:
    with pytest.raises(TypeError, match="refusing to coerce"):
        float(BLINDNESS_GATED)


def test_an_absence_refuses_coercion_to_int() -> None:
    with pytest.raises(TypeError, match="refusing to coerce"):
        int(BLINDNESS_GATED)


def test_an_absence_cannot_enter_arithmetic() -> None:
    with pytest.raises(TypeError):
        BLINDNESS_GATED + 1.0  # type: ignore[operator]
    with pytest.raises(TypeError):
        sum([1.0, BLINDNESS_GATED])  # type: ignore[list-item]


def test_an_absence_is_falsy_and_immutable() -> None:
    assert not NO_CANDLES
    with pytest.raises(AttributeError):
        NO_CANDLES.reason = AbsenceReason.NOT_SERVED


def test_absences_compare_by_reason() -> None:
    assert Absent(AbsenceReason.NO_CANDLES) == NO_CANDLES
    assert Absent(AbsenceReason.NO_CANDLES) != BLINDNESS_GATED
    assert is_absent(NO_CANDLES)
    assert not is_absent(0.0)


def test_require_present_unwraps_or_raises() -> None:
    assert require_present(1.25, "rate") == 1.25
    with pytest.raises(ValueError, match="blindness_gated"):
        require_present(BLINDNESS_GATED, "rate")
