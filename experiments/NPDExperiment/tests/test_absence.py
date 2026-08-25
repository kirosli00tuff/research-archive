"""Absence is a recorded state, never a synthesized value.

Seven historical fabrications in the predecessor were each a plausible value
produced from absent input. These tests fail the moment a hole is filled.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from npd.absence import (
    NO_BAR,
    AbsenceReason,
    Absent,
    is_absent,
    require_present,
)
from npd.data.features import Series, raw_block, realized_vol, trailing_return, volume_trend


def _full_series(n: int = 300) -> Series:
    closes = tuple(100.0 + i * 0.5 for i in range(n))
    vols = tuple(1_000_000.0 + i * 10 for i in range(n))
    return Series(symbol="TEST", close=closes, volume=vols)


def _with_hole(n: int = 300, hole: int = 250) -> Series:
    s = _full_series(n)
    closes = list(s.close)
    vols = list(s.volume)
    closes[hole] = None
    vols[hole] = None
    return Series(symbol="TEST", close=tuple(closes), volume=tuple(vols))


def test_absent_refuses_to_become_a_number() -> None:
    with pytest.raises(TypeError):
        float(NO_BAR)
    with pytest.raises(TypeError):
        int(NO_BAR)
    assert not NO_BAR
    assert is_absent(NO_BAR)


def test_absent_is_immutable() -> None:
    with pytest.raises(AttributeError):
        NO_BAR.reason = AbsenceReason.NON_FINITE


def test_require_present_raises_rather_than_defaulting() -> None:
    with pytest.raises(ValueError, match="absent"):
        require_present(NO_BAR, "a feature")
    assert require_present(1.5, "a feature") == 1.5


def test_a_missing_bar_inside_the_span_produces_an_absence_not_a_number() -> None:
    """The mutation target. Carrying the previous close forward would return a
    float here, and this assertion is what catches it."""
    s = _with_hole(hole=250)
    value = trailing_return(s, 260, 20)
    assert isinstance(value, Absent), f"a hole in the span produced {value!r}"
    assert value.reason is AbsenceReason.NO_BAR


def test_every_feature_reports_the_hole() -> None:
    s = _with_hole(hole=250)
    block = raw_block(s, 260)
    absent = {name for name, v in block.items() if isinstance(v, Absent)}
    assert "ret_20" in absent
    assert "ret_60" in absent
    assert "rvol_20" in absent
    assert "rvol_60" in absent
    assert "dvol_z_60" in absent
    assert "vtrend_5_60" in absent


def test_a_complete_span_produces_numbers() -> None:
    s = _full_series()
    block = raw_block(s, 260)
    assert all(not isinstance(v, Absent) for v in block.values()), block


def test_insufficient_history_is_recorded_not_padded() -> None:
    s = _full_series(n=40)
    value = realized_vol(s, 20, 60)
    assert isinstance(value, Absent)
    assert value.reason is AbsenceReason.INSUFFICIENT_HISTORY


def test_zero_volume_denominator_is_recorded_not_replaced() -> None:
    closes = tuple(100.0 for _ in range(100))
    vols = tuple(0.0 for _ in range(100))
    s = Series(symbol="Z", close=closes, volume=vols)
    value = volume_trend(s, 80)
    assert isinstance(value, Absent)
    assert value.reason is AbsenceReason.ZERO_DENOMINATOR


def test_the_store_refuses_a_value_and_a_reason_together(tmp_path: Path) -> None:
    import sqlite3

    from npd.data.store import SCHEMA

    con = sqlite3.connect(tmp_path / "t.db")
    con.executescript(SCHEMA)
    con.execute(
        "INSERT INTO feature(date, symbol, name, raw, z, absent_reason) VALUES(?,?,?,?,?,?)",
        ("2025-01-02", "AAA", "ret_1", 0.5, 0.5, None),
    )
    with pytest.raises(sqlite3.IntegrityError):
        con.execute(
            "INSERT INTO feature(date, symbol, name, raw, z, absent_reason) VALUES(?,?,?,?,?,?)",
            ("2025-01-02", "BBB", "ret_1", 0.5, 0.5, "no_bar"),
        )
    with pytest.raises(sqlite3.IntegrityError):
        con.execute(
            "INSERT INTO feature(date, symbol, name, raw, z, absent_reason) VALUES(?,?,?,?,?,?)",
            ("2025-01-02", "CCC", "ret_1", None, None, None),
        )
    con.close()
