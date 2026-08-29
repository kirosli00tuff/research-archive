"""A.1 Task 3: the publication lag, measured from this repository's own captures.

Neither selected flow source serves a per-row publication timestamp
(docs/ACCESS.md §2 — n = 2 of 2), so a "first print time" exists only as the
first capture of ours in which the day's value stands. Every figure here is
therefore bounded below by the snapshot cadence and is reported with the
cadence beside it.

Nothing here reads a price. It reads flow values, which are signal, and the
capture timestamps this repository stamped.
"""

from __future__ import annotations

from collections.abc import Iterable, Sequence
from dataclasses import dataclass
from datetime import UTC, date, datetime, timedelta

from etf.anchor import entry_anchor, percentile
from etf.config import CONFIG


@dataclass(frozen=True, slots=True)
class CaptureObservation:
    """One trading day as it stood in one capture."""

    captured_at: datetime
    trade_date: date
    signal_present: bool
    present_tickers: frozenset[str]
    absent_tickers: frozenset[str]


@dataclass(frozen=True, slots=True)
class DayLag:
    trade_date: date
    first_present_at: datetime | None
    captures: int
    hours_past_midnight_next_day: float | None
    before_provisional_anchor: bool


@dataclass(frozen=True, slots=True)
class LagReport:
    days: tuple[DayLag, ...]
    n_days: int
    n_days_with_a_print: int
    p50_hours: float | None
    p90_hours: float | None
    p95_hours: float | None
    largest_fund_late_days: int
    largest_fund_late_share: float | None
    dash_then_number_days: int
    dash_then_number_share: float | None
    no_value_before_anchor_days: int
    meets_registered_minimum: bool
    cadence_floor_minutes: int


def _hours_past_midnight_next_day(moment: datetime, trade_day: date) -> float:
    midnight = datetime.combine(trade_day + timedelta(days=1), datetime.min.time(), tzinfo=UTC)
    return (moment - midnight).total_seconds() / 3600.0


def day_lags(observations: Iterable[CaptureObservation]) -> tuple[DayLag, ...]:
    """Per trading day, the earliest capture in which the aggregate stood."""
    by_day: dict[date, list[CaptureObservation]] = {}
    for obs in observations:
        by_day.setdefault(obs.trade_date, []).append(obs)
    out: list[DayLag] = []
    for trade_date in sorted(by_day):
        # Standing rule: order multi-process logs by clock, never by file position.
        rows = sorted(by_day[trade_date], key=lambda o: o.captured_at)
        first = next((r for r in rows if r.signal_present), None)
        hours = (
            _hours_past_midnight_next_day(first.captured_at, trade_date)
            if first is not None
            else None
        )
        out.append(
            DayLag(
                trade_date=trade_date,
                first_present_at=first.captured_at if first is not None else None,
                captures=len(rows),
                hours_past_midnight_next_day=hours,
                before_provisional_anchor=(
                    first is not None and first.captured_at < entry_anchor(trade_date)
                ),
            )
        )
    return tuple(out)


def _largest_fund() -> str:
    """The largest US spot Bitcoin ETF by assets: the first registered ticker."""
    return CONFIG.flow_universe_tickers[0]


def build_report(observations: Sequence[CaptureObservation]) -> LagReport:
    """Every A.1 Task 3 figure, each with the n it rests on."""
    lags = day_lags(observations)
    printed = [d for d in lags if d.hours_past_midnight_next_day is not None]
    hours = [
        d.hours_past_midnight_next_day
        for d in printed
        if d.hours_past_midnight_next_day is not None
    ]

    by_day: dict[date, list[CaptureObservation]] = {}
    for obs in observations:
        by_day.setdefault(obs.trade_date, []).append(obs)

    largest = _largest_fund()
    largest_late = 0
    dash_then_number = 0
    for rows in by_day.values():
        ordered = sorted(rows, key=lambda o: o.captured_at)
        if any(r.present_tickers and largest in r.absent_tickers for r in ordered):
            largest_late += 1
        seen_absent: set[str] = set()
        flipped = False
        for row in ordered:
            if seen_absent & row.present_tickers:
                flipped = True
            seen_absent |= set(row.absent_tickers)
        if flipped:
            dash_then_number += 1

    n_days = len(lags)
    return LagReport(
        days=lags,
        n_days=n_days,
        n_days_with_a_print=len(printed),
        p50_hours=percentile(hours, 0.50) if hours else None,
        p90_hours=percentile(hours, 0.90) if hours else None,
        p95_hours=percentile(hours, CONFIG.anchor_amendment_percentile) if hours else None,
        largest_fund_late_days=largest_late,
        largest_fund_late_share=(largest_late / n_days) if n_days else None,
        dash_then_number_days=dash_then_number,
        dash_then_number_share=(dash_then_number / n_days) if n_days else None,
        no_value_before_anchor_days=sum(1 for d in lags if not d.before_provisional_anchor),
        meets_registered_minimum=n_days >= CONFIG.lag_min_trading_days,
        cadence_floor_minutes=CONFIG.snapshot_peak_interval_minutes,
    )
