"""The ticker-to-quote conversion, where two silent failures were available.

Both are conversions that look like formalities and are not. A NaN touch that
reaches arithmetic compares false against every bound and would pass a ceiling
test. A borrowed venue timestamp would make the staleness check compare the local
clock against itself, so it could never fail.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime, timedelta

from mbt.absence import AbsenceReason, Absent
from mbt.figures import TickDelayStatus
from mbt.marketdata import TickerReader
from mbt.quotes import screen


@dataclass
class StubTicker:
    """Shaped like an ``ib_async`` Ticker in the fields this package reads."""

    bid: float | None
    ask: float | None
    time: datetime | None
    marketDataType: int | None


def _now() -> datetime:
    return datetime(2026, 9, 3, 19, 30, tzinfo=UTC)


def test_a_nan_touch_becomes_absent_rather_than_a_number() -> None:
    """Measured on 2026-09-03: an unsubscribed real-time request serves NaN."""
    ticker = StubTicker(bid=float("nan"), ask=float("nan"), time=_now(), marketDataType=1)
    quote = TickerReader("future_hedge").read(ticker, _now())
    assert not isinstance(quote, Absent)
    assert quote.bid is None and quote.ask is None
    refusal = screen(quote)
    assert isinstance(refusal, Absent)
    assert refusal.reason is AbsenceReason.UNQUOTED_LEG


def test_a_realtime_status_over_a_nan_touch_is_still_refused() -> None:
    """The status field alone does not establish a subscription.

    Measured: a real-time request on MBT returned ``marketDataType = 1`` while
    the feed served no touch and the broker raised error 354. Admitting on the
    status alone would have recorded that as a real-time observation.
    """
    ticker = StubTicker(bid=float("nan"), ask=float("nan"), time=_now(), marketDataType=1)
    quote = TickerReader("option_call").read(ticker, _now())
    assert not isinstance(quote, Absent)
    assert quote.tick_delay is TickDelayStatus.REALTIME
    assert isinstance(screen(quote), Absent)


def test_a_missing_venue_stamp_is_an_unquoted_leg_not_a_borrowed_clock() -> None:
    ticker = StubTicker(bid=100.0, ask=101.0, time=None, marketDataType=1)
    result = TickerReader("option_put").read(ticker, _now())
    assert isinstance(result, Absent)
    assert result.reason is AbsenceReason.UNQUOTED_LEG
    assert "never replaced by" in result.detail


def test_the_no_market_sentinel_is_absent_rather_than_a_negative_price() -> None:
    """Measured on 2026-09-03: an MBT put served bid -1 and ask -1."""
    ticker = StubTicker(bid=-1.0, ask=-1.0, time=_now(), marketDataType=3)
    quote = TickerReader("option_put").read(ticker, _now())
    assert not isinstance(quote, Absent)
    assert quote.bid is None and quote.ask is None


def test_a_delayed_touch_is_carried_then_refused_by_the_registered_rule() -> None:
    """Delayed data is measured and recorded, and never widened into a band."""
    ticker = StubTicker(bid=81770.0, ask=81785.0, time=_now(), marketDataType=3)
    quote = TickerReader("future_hedge").read(ticker, _now())
    assert not isinstance(quote, Absent)
    assert quote.tick_delay is TickDelayStatus.DELAYED
    refusal = screen(quote)
    assert isinstance(refusal, Absent)
    assert refusal.reason is AbsenceReason.DELAYED_TICK


def test_an_unreported_status_is_refused_exactly_as_delayed_is() -> None:
    ticker = StubTicker(bid=100.0, ask=101.0, time=_now(), marketDataType=None)
    quote = TickerReader("option_call").read(ticker, _now())
    assert not isinstance(quote, Absent)
    assert quote.tick_delay is TickDelayStatus.UNKNOWN
    assert isinstance(screen(quote), Absent)


def test_a_stale_venue_stamp_is_refused() -> None:
    stale = _now() - timedelta(seconds=30)
    ticker = StubTicker(bid=100.0, ask=101.0, time=stale, marketDataType=1)
    quote = TickerReader("future_hedge").read(ticker, _now())
    assert not isinstance(quote, Absent)
    refusal = screen(quote)
    assert isinstance(refusal, Absent)
    assert refusal.reason is AbsenceReason.STALE_TIMESTAMP
