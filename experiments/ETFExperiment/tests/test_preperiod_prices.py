"""The carve-out reader: fixtures exactly on the boundary, and a total refusal past it."""

from __future__ import annotations

import json

import pytest

from etf.config import CONFIG
from etf.preperiod import PrePeriodViolation
from etf.preperiod_prices import (
    ALLOWED_PRE_PERIOD_FIELDS,
    PrePeriodPayloadShape,
    daily_volatility,
    pre_period_closes,
)

B = CONFIG.pre_period_end_ms
DAY = 86_400_000


def candle(close_ms: int, close: float) -> dict[str, object]:
    return {
        "t": close_ms - DAY + 1,
        "T": close_ms,
        "s": "BTC",
        "i": "1d",
        "o": "1.0",
        "h": "2.0",
        "l": "0.5",
        "c": str(close),
        "v": "10",
        "n": 3,
    }


def test_the_reader_declares_only_t_T_and_c() -> None:
    assert ALLOWED_PRE_PERIOD_FIELDS == ("t", "T", "c")


def test_a_series_wholly_inside_the_carve_out_reads() -> None:
    payload = json.dumps([candle(B - 3 * DAY, 100.0), candle(B - 2 * DAY, 101.0)])
    rows = pre_period_closes(payload)
    assert [r.close for r in rows] == [100.0, 101.0]


def test_a_close_one_millisecond_before_the_boundary_reads() -> None:
    rows = pre_period_closes(json.dumps([candle(B - 1, 100.0)]))
    assert rows[0].close_ms == B - 1


def test_a_close_exactly_on_the_boundary_is_refused() -> None:
    """Exclusive, and the fixture sits exactly on 2025-05-01T00:00:00.000Z."""
    with pytest.raises(PrePeriodViolation, match="Section 9 carve-out"):
        pre_period_closes(json.dumps([candle(B, 100.0)]))


def test_one_post_boundary_row_refuses_the_whole_series_rather_than_truncating_it() -> None:
    """A silently truncated volatility series is a synthesized one."""
    payload = json.dumps(
        [candle(B - 2 * DAY, 100.0), candle(B - DAY, 101.0), candle(B + DAY, 102.0)]
    )
    with pytest.raises(PrePeriodViolation):
        pre_period_closes(payload)


def test_a_non_list_payload_is_refused() -> None:
    with pytest.raises(PrePeriodPayloadShape, match="not a list"):
        pre_period_closes(json.dumps({"error": "no such coin"}))


def test_an_empty_payload_is_an_absence_not_a_zero_volatility() -> None:
    with pytest.raises(PrePeriodPayloadShape, match="an absence"):
        pre_period_closes(json.dumps([]))


def test_a_volatility_on_two_closes_is_refused() -> None:
    rows = pre_period_closes(json.dumps([candle(B - 2 * DAY, 100.0), candle(B - DAY, 101.0)]))
    with pytest.raises(PrePeriodPayloadShape, match="at least 3 closes"):
        daily_volatility(rows)


def test_the_volatility_is_the_sample_sd_of_log_returns_and_carries_its_n() -> None:
    closes = [100.0, 110.0, 99.0, 108.0, 101.0]
    rows = pre_period_closes(
        json.dumps([candle(B - (len(closes) - i) * DAY, c) for i, c in enumerate(closes)])
    )
    vol = daily_volatility(rows)
    assert vol.n_returns == len(closes) - 1
    assert vol.daily_sd > 0.0
    assert vol.first_close_ms < vol.last_close_ms < B


def test_the_series_is_ordered_by_clock_before_differencing() -> None:
    closes = [(B - 3 * DAY, 100.0), (B - DAY, 121.0), (B - 2 * DAY, 110.0)]
    rows = pre_period_closes(json.dumps([candle(ms, c) for ms, c in closes]))
    vol = daily_volatility(rows)
    assert vol.daily_sd == pytest.approx(0.0, abs=1e-12), (
        "two equal 10 percent steps have zero dispersion only if the series was sorted"
    )
