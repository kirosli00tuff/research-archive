"""Outcome blindness: t, T and row count from candles; funding gated by the carve-out."""

from __future__ import annotations

import json

import pytest

from etf.absence import PRE_PERIOD_GATED, Absent
from etf.blindness import ALLOWED_CANDLE_FIELDS, BlindnessViolation, candle_times, funding_rows
from etf.config import CONFIG

BOUNDARY_MS = CONFIG.pre_period_end_ms


def test_only_t_and_T_are_allowed_candle_fields() -> None:
    assert ALLOWED_CANDLE_FIELDS == ("t", "T")


def test_candle_reader_returns_timestamps_and_a_count_and_nothing_else() -> None:
    payload = json.dumps(
        [
            {"t": 1, "T": 2, "o": "1.0", "h": "2.0", "l": "0.5", "c": "1.5", "v": "10"},
            {"t": 2, "T": 3, "o": "1.5", "h": "2.5", "l": "1.0", "c": "2.0", "v": "11"},
        ]
    )
    times = candle_times(payload)
    assert times.open_ms == (1, 2)
    assert times.close_ms == (2, 3)
    assert times.row_count == 2
    assert not hasattr(times, "close")
    assert set(times.__slots__) == {"open_ms", "close_ms", "row_count"}


def test_a_candle_row_missing_a_timestamp_is_refused_never_guessed() -> None:
    with pytest.raises(BlindnessViolation, match="lacks 'T'"):
        candle_times(json.dumps([{"t": 1, "c": "9"}]))


def test_a_non_list_candle_payload_is_refused_loudly() -> None:
    with pytest.raises(BlindnessViolation, match="not a list"):
        candle_times(json.dumps({"error": "no such coin"}))


def test_funding_before_the_boundary_is_readable_and_at_it_is_gated() -> None:
    payload = json.dumps(
        [
            {"time": BOUNDARY_MS - 1, "fundingRate": "0.0000125", "coin": "BTC"},
            {"time": BOUNDARY_MS, "fundingRate": "0.0000125", "coin": "BTC"},
        ]
    )
    rows = funding_rows(payload)
    assert rows[0].time_ms == BOUNDARY_MS - 1
    assert rows[0].rate == 0.0000125
    assert rows[1].time_ms == BOUNDARY_MS
    assert rows[1].rate == PRE_PERIOD_GATED
    assert isinstance(rows[1].rate, Absent)


def test_a_gated_funding_rate_cannot_be_summed_into_a_hold_window() -> None:
    rows = funding_rows(json.dumps([{"time": BOUNDARY_MS + 3_600_000, "fundingRate": "0.001"}]))
    with pytest.raises(TypeError, match="refusing to coerce"):
        float(rows[0].rate)


def test_a_non_list_funding_payload_is_refused_loudly() -> None:
    with pytest.raises(BlindnessViolation, match="not a list"):
        funding_rows(json.dumps({"error": "bad request"}))
