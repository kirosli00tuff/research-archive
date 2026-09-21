"""The census parses t, T, and row count only, and its ledger round-trips."""

from __future__ import annotations

import json
from pathlib import Path

from npl.callstate import CallState
from npl.census import (
    CensusLedger,
    CensusRow,
    census_instrument,
    event_type_of,
    listings_per_quarter,
    quarter_of_ms,
    trailing_rate_per_quarter,
)
from npl.clock import MS_PER_DAY
from npl.http import InfoResponse
from npl.venue import PerpInfo, Venue

DAY0 = 1690000000000  # synthetic epoch anchor


def _candle_payload(first_day: int, days: int) -> bytes:
    rows = [
        {
            "t": DAY0 + (first_day + i) * MS_PER_DAY,
            "T": DAY0 + (first_day + i + 1) * MS_PER_DAY - 1,
            "s": "X",
            "i": "1d",
            "o": "1.0",
            "c": "2.0",
            "h": "3.0",
            "l": "0.5",
            "v": "9.9",
            "n": 3,
        }
        for i in range(days)
    ]
    return json.dumps(rows).encode()


def _funding_payload(first_time: int, rows: int = 3) -> bytes:
    return json.dumps(
        [
            {"coin": "X", "fundingRate": "0.0000125", "time": first_time + i * 3_600_000}
            for i in range(rows)
        ]
    ).encode()


class _CandleClient:
    """Routes by request type: candles get one body, funding another."""

    def __init__(self, status: int, body: bytes, funding_body: bytes | None = None) -> None:
        self.status = status
        self.body = body
        self.funding_body = funding_body

    def post(self, body: dict[str, object], endpoint: str) -> InfoResponse:
        if body.get("type") == "fundingHistory":
            served = self.funding_body
            if served is None:
                served = _funding_payload(DAY0 + 3 * MS_PER_DAY + 3_600_000)
            return InfoResponse(status=self.status, body=served, elapsed_s=0.0)
        return InfoResponse(status=self.status, body=self.body, elapsed_s=0.0)


def _perp(name: str = "NEW", delisted: bool = False) -> PerpInfo:
    return PerpInfo(name=name, sz_decimals=2, max_leverage=10, is_delisted=delisted)


def test_the_census_row_carries_times_and_count_and_no_price_field() -> None:
    venue = Venue(_CandleClient(200, _candle_payload(first_day=3, days=5)))  # type: ignore[arg-type]
    row = census_instrument(venue, _perp(), "", {})
    assert row.state == CallState.STORED.value
    assert row.first_1d_open_ms == DAY0 + 3 * MS_PER_DAY
    assert row.last_1d_close_ms == DAY0 + 8 * MS_PER_DAY - 1
    assert row.candle_rows == 5
    # The record type structurally has nowhere to put a price.
    assert not {"open", "close", "high", "low", "volume"} & set(CensusRow.__slots__)


def test_a_served_empty_history_is_no_data_not_a_zero_date() -> None:
    venue = Venue(_CandleClient(200, b"[]"))  # type: ignore[arg-type]
    row = census_instrument(venue, _perp(), "", {})
    assert row.state == CallState.NO_DATA.value
    assert row.first_1d_open_ms is None
    assert row.candle_rows == 0


def test_a_429_is_rate_limited_and_carries_no_dates() -> None:
    venue = Venue(_CandleClient(429, b"slow"))  # type: ignore[arg-type]
    row = census_instrument(venue, _perp(), "", {})
    assert row.state == CallState.RATE_LIMITED.value
    assert row.first_1d_open_ms is None


def test_event_type_tagging_rules() -> None:
    assert event_type_of("BTC", "", {}) == ("vanilla", "")
    assert event_type_of("xyz:AAPL", "xyz", {}) == ("hip3", "")
    assert event_type_of("FRIEND", "", {"FRIEND": "docs-url"}) == (
        "hyperp_conversion",
        "docs-url",
    )


def test_the_census_ledger_round_trips(tmp_path: Path) -> None:
    ledger = CensusLedger(tmp_path / "census.jsonl")
    venue = Venue(_CandleClient(200, _candle_payload(first_day=0, days=2)))  # type: ignore[arg-type]
    row = census_instrument(venue, _perp("AAA"), "xyz", {})
    ledger.append(row)
    back = ledger.rows()
    assert back == [row]


def test_quarter_bucketing_and_trailing_rate() -> None:
    # 2026-01-15 and 2026-08-01, synthetic.
    q1 = 1768435200000  # 2026-01-15T00:00:00Z
    q3 = 1785542400000  # 2026-08-01T00:00:00Z
    assert quarter_of_ms(q1) == "2026Q1"
    assert quarter_of_ms(q3) == "2026Q3"
    rows = [
        CensusRow(
            "A", "", "vanilla", "", False, 1, 10, "stored", q1, q1, 10, "stored", q1, 500, "t"
        ),
        CensusRow(
            "B", "", "vanilla", "", False, 1, 10, "stored", q3, q3, 10, "stored", q3, 500, "t"
        ),
        CensusRow(
            "C", "xyz", "hip3", "", False, 1, 10, "stored", q3, q3, 10, "stored", q3, 500, "t"
        ),
        CensusRow(
            "D", "", "vanilla", "", False, 1, 10, "no_data", None, None, 0, "no_data", None, 0, "t"
        ),
    ]
    per_quarter = listings_per_quarter(rows)
    assert per_quarter["2026Q1"] == {"vanilla": 1}
    assert per_quarter["2026Q3"] == {"vanilla": 1, "hip3": 1}
    now_ms = q3 + 30 * MS_PER_DAY
    rate = trailing_rate_per_quarter(rows, now_ms, quarters=2)
    assert rate == {"vanilla": 0.5, "hip3": 0.5}
