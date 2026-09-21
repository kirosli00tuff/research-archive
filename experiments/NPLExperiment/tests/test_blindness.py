"""The blindness pins. Outside sealed writers, OHLCV does not exist.

Candle fields readable: t, T, row count. fundingHistory fields readable: time
always, fundingRate only where time is at or before the referencing event
entry. These tests pin the behaviour and the parse tree.
"""

from __future__ import annotations

import ast
import json
from pathlib import Path

import pytest

from npl.absence import AbsenceReason, Absent
from npl.blindness import (
    ALLOWED_CANDLE_FIELDS,
    BlindnessViolation,
    candle_times,
    funding_rows,
)

BLINDNESS_FILE = Path(__file__).resolve().parents[1] / "src" / "npl" / "blindness.py"

# A full synthetic candle row, shaped like the venue's payload. Values are
# synthetic; the test asserts the reader cannot see the priced fields at all.
CANDLES = json.dumps(
    [
        {
            "t": 1000,
            "T": 2000,
            "s": "X",
            "i": "1d",
            "o": "1.0",
            "c": "2.0",
            "h": "3.0",
            "l": "0.5",
            "v": "9.9",
            "n": 4,
        },
        {
            "t": 2000,
            "T": 3000,
            "s": "X",
            "i": "1d",
            "o": "2.0",
            "c": "1.0",
            "h": "2.5",
            "l": "0.9",
            "v": "8.8",
            "n": 2,
        },
    ]
)

FUNDING = json.dumps(
    [
        {"coin": "X", "fundingRate": "0.0000125", "time": 900},
        {"coin": "X", "fundingRate": "-0.0000125", "time": 1000},
        {"coin": "X", "fundingRate": "0.0000200", "time": 1100},
    ]
)


def test_the_candle_reader_returns_timestamps_and_count_only() -> None:
    times = candle_times(CANDLES)
    assert times.open_ms == (1000, 2000)
    assert times.close_ms == (2000, 3000)
    assert times.row_count == 2
    # The result type structurally has nowhere to put a price.
    assert set(times.__slots__) == {"open_ms", "close_ms", "row_count"}


def test_the_allowed_candle_fields_are_exactly_t_and_capital_t() -> None:
    assert ALLOWED_CANDLE_FIELDS == ("t", "T")


def test_a_non_list_candle_payload_is_refused_loudly() -> None:
    with pytest.raises(BlindnessViolation, match="Refusing to guess"):
        candle_times(json.dumps({"error": "nope"}))


def test_funding_time_is_always_readable() -> None:
    rows = funding_rows(FUNDING, entry_ms=None)
    assert [r.time_ms for r in rows] == [900, 1000, 1100]


def test_funding_rate_at_or_before_entry_is_readable() -> None:
    rows = funding_rows(FUNDING, entry_ms=1000)
    assert rows[0].rate == pytest.approx(0.0000125)
    # The boundary row: time == entry is "at or before" and is readable.
    assert rows[1].rate == pytest.approx(-0.0000125)


def test_funding_rate_after_entry_is_a_recorded_absence() -> None:
    rows = funding_rows(FUNDING, entry_ms=1000)
    assert isinstance(rows[2].rate, Absent)
    assert rows[2].rate.reason is AbsenceReason.BLINDNESS_GATED


def test_a_gated_rate_cannot_be_coerced_into_a_sum() -> None:
    rows = funding_rows(FUNDING, entry_ms=1000)
    gated = rows[2].rate
    assert isinstance(gated, Absent)
    with pytest.raises(TypeError, match="refusing to coerce"):
        float(gated)


def test_a_coverage_read_carries_absences_throughout() -> None:
    rows = funding_rows(FUNDING, entry_ms=None)
    assert all(isinstance(r.rate, Absent) for r in rows)


def test_the_blind_parser_source_never_names_a_priced_field() -> None:
    """The parse tree of blindness.py contains no OHLCV key, by pin."""
    tree = ast.parse(BLINDNESS_FILE.read_text(encoding="utf-8"))
    strings = {
        node.value
        for node in ast.walk(tree)
        if isinstance(node, ast.Constant) and isinstance(node.value, str)
    }
    forbidden = {"o", "h", "l", "c", "v", "open", "high", "low", "close", "volume", "px", "sz"}
    named = sorted(strings & forbidden)
    assert not named, f"blindness.py names priced candle fields: {named}"
    assert "t" in strings
    assert "T" in strings
    assert "time" in strings
