"""A.2 Task 3 / A.3 Task 3: the sealed outcome substrate. Written by the sealed writer only.

Hourly candles and hourly funding covering each admissible day's anchor and its
24-hour hold window are fetched and **sealed as raw response bytes**. Nothing
in this module parses a price: coverage is accounted through
`etf.blindness.candle_times` and `etf.blindness.funding_rows`, which see
timestamps and row counts and are structurally incapable of returning a close.

**Urgency, measured at A.1 Task 1 and not anticipated by the design.** The venue
serves a rolling 5,001-candle window, so hourly candles reach back only about
208 days and the boundary slides forward one hour per hour. A day's hold window
that is not sealed before it falls out of that window can never be sealed. There
is no archive for it — the durability argument the brief makes for the forward
flow ledger binds harder here.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime, timedelta

from etf.anchor import entry_anchor
from etf.blindness import candle_times, funding_rows
from etf.callstate import CallState
from etf.clock import MS_PER_HOUR, utc_ms
from etf.config import CONFIG
from etf.http import PacedClient
from etf.paths import FUNDING_DIR, OUTCOMES_DIR
from etf.seal import SealedWrite, seal_bytes

# The registered one-day primary horizon (Section 7), in hours. A literal 24
# here would duplicate the registered figure and drift from it silently.
HOLD_HOURS = CONFIG.horizon_primary_days * 24


@dataclass(frozen=True, slots=True)
class DayCoverage:
    """Counts, timestamps and reasons. Never a value."""

    trade_date: date
    anchor: datetime
    candle_state: CallState
    candle_rows: int
    candle_expected: int
    funding_state: CallState
    funding_rows: int
    funding_expected: int
    candle_sha256: str | None
    funding_sha256: str | None

    @property
    def candle_coverage(self) -> float:
        return self.candle_rows / self.candle_expected if self.candle_expected else 0.0

    @property
    def funding_coverage(self) -> float:
        return self.funding_rows / self.funding_expected if self.funding_expected else 0.0

    @property
    def covered(self) -> bool:
        """Under either bar the day reports underpowered, never a return."""
        return (
            self.candle_coverage >= CONFIG.min_outcome_coverage_candles
            and self.funding_coverage >= CONFIG.min_outcome_coverage_funding
        )


def hold_window(
    trade_day: date, anchor_hour_utc: int = CONFIG.entry_anchor_hour_utc
) -> tuple[datetime, datetime]:
    """The anchor and the anchor plus the registered 24-hour hold."""
    anchor = entry_anchor(trade_day, anchor_hour_utc)
    return anchor, anchor + timedelta(hours=HOLD_HOURS)


def record_day(
    client: PacedClient,
    trade_day: date,
    *,
    anchor_hour_utc: int = CONFIG.entry_anchor_hour_utc,
) -> DayCoverage:
    """Fetch and seal one day's hold window. Returns counts and reasons only."""
    start, end = hold_window(trade_day, anchor_hour_utc)
    start_ms, end_ms = utc_ms(start), utc_ms(end)

    candle_sha: str | None = None
    candle_state = CallState.SOURCE_FAILED
    candle_n = 0
    response = client.post_json(
        CONFIG.hyperliquid_info_url,
        {
            "type": "candleSnapshot",
            "req": {
                "coin": CONFIG.perp_coin,
                "interval": "1h",
                "startTime": start_ms,
                "endTime": end_ms,
            },
        },
        source="venue",
        endpoint="venue.candleSnapshot",
    )
    if response.status == 429:
        candle_state = CallState.RATE_LIMITED
    elif response.status == 200:
        written: SealedWrite = seal_bytes(
            OUTCOMES_DIR / f"btc-1h-{trade_day.isoformat()}.json", response.body
        )
        candle_sha = written.sha256
        times = candle_times(response.body)
        candle_n = times.row_count
        candle_state = CallState.STORED if candle_n else CallState.NO_DATA

    funding_sha: str | None = None
    funding_state = CallState.SOURCE_FAILED
    funding_n = 0
    response = client.post_json(
        CONFIG.hyperliquid_info_url,
        {
            "type": "fundingHistory",
            "coin": CONFIG.perp_coin,
            "startTime": start_ms,
            "endTime": end_ms,
        },
        source="venue",
        endpoint="venue.fundingHistory",
    )
    if response.status == 429:
        funding_state = CallState.RATE_LIMITED
    elif response.status == 200:
        written = seal_bytes(
            FUNDING_DIR / f"btc-funding-{trade_day.isoformat()}.json", response.body
        )
        funding_sha = written.sha256
        rows = funding_rows(response.body)
        funding_n = len(rows)
        funding_state = CallState.STORED if funding_n else CallState.NO_DATA

    expected = (end_ms - start_ms) // MS_PER_HOUR
    return DayCoverage(
        trade_date=trade_day,
        anchor=start,
        candle_state=candle_state,
        candle_rows=candle_n,
        candle_expected=expected,
        funding_state=funding_state,
        funding_rows=funding_n,
        funding_expected=expected,
        candle_sha256=candle_sha,
        funding_sha256=funding_sha,
    )
