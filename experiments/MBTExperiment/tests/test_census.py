"""The census: distinctness in clock terms, three legs, and recorded refusals."""

from __future__ import annotations

from datetime import UTC, datetime, timedelta
from pathlib import Path

import pytest

from mbt.absence import Absent
from mbt.census import (
    CensusDistinctnessError,
    CensusLedger,
    CensusWindow,
    RefusedWindow,
    build_window,
    check_distinct,
    percentile,
    straddle_round_trip_bps,
    summarise,
)
from mbt.clock import ObservationClock
from mbt.figures import TickDelayStatus
from mbt.provenance import Environment
from mbt.quotes import Quote
from mbt.registry import (
    MAX_WINDOWS_PER_UTC_DAY,
    MIN_MINUTES_BETWEEN_WINDOWS,
    MIN_OBSERVATION_WINDOWS,
)

NOTIONAL = 7812.46
BASE = datetime(2026, 9, 3, 12, 0, 0, tzinfo=UTC)


def leg(name: str, bid: float, ask: float, at: datetime | None = None) -> Quote:
    stamp = at or BASE
    return Quote(
        leg=name,
        bid=bid,
        ask=ask,
        clock=ObservationClock(venue=stamp, local=stamp),
        tick_delay=TickDelayStatus.REALTIME,
    )


def three_legs(at: datetime | None = None) -> dict[str, Quote]:
    return {
        "option_call": leg("option_call", 100.0, 110.0, at),
        "option_put": leg("option_put", 95.0, 103.0, at),
        "future_hedge": leg("future_hedge", 78_000.0, 78_010.0, at),
    }


def make_window(sequence: int, at: datetime) -> CensusWindow:
    window = build_window(
        sequence, three_legs(at), environment=Environment.PAPER, notional=NOTIONAL, local_ts=at
    )
    assert isinstance(window, CensusWindow)
    return window


# --- all three legs are required -------------------------------------------


def test_a_window_missing_the_hedge_leg_is_refused() -> None:
    """A spread on options alone understates the leg traded 11 to 16 times."""
    legs = three_legs()
    del legs["future_hedge"]
    result = build_window(1, legs, environment=Environment.PAPER, notional=NOTIONAL, local_ts=BASE)
    assert isinstance(result, RefusedWindow)
    assert result.leg == "future_hedge"


@pytest.mark.parametrize("missing", ["option_call", "option_put", "future_hedge"])
def test_every_required_leg_is_actually_required(missing: str) -> None:
    legs = three_legs()
    del legs[missing]
    result = build_window(1, legs, environment=Environment.PAPER, notional=NOTIONAL, local_ts=BASE)
    assert isinstance(result, RefusedWindow)


def test_a_clean_window_records_all_three_half_spreads() -> None:
    window = make_window(1, BASE)
    assert set(window.half_spreads_bps) == {"option_call", "option_put", "future_hedge"}


def test_the_round_trip_is_twice_the_two_option_half_spreads() -> None:
    """The hedge leg is paid per rebalance, so including it here would assume a count."""
    half = {"option_call": 3.0, "option_put": 2.0, "future_hedge": 100.0}
    assert straddle_round_trip_bps(half) == 10.0


def test_a_refused_leg_refuses_the_window_and_names_the_reason() -> None:
    legs = three_legs()
    legs["option_put"] = Quote(
        leg="option_put",
        bid=0.0,
        ask=103.0,
        clock=ObservationClock(venue=BASE, local=BASE),
        tick_delay=TickDelayStatus.REALTIME,
    )
    result = build_window(1, legs, environment=Environment.PAPER, notional=NOTIONAL, local_ts=BASE)
    assert isinstance(result, RefusedWindow)
    assert result.reason == "zero_bid"
    assert result.leg == "option_put"


# --- distinctness, in clock terms ------------------------------------------


def test_two_windows_inside_the_registered_spacing_are_not_distinct() -> None:
    first = make_window(1, BASE)
    too_close = BASE + timedelta(minutes=MIN_MINUTES_BETWEEN_WINDOWS - 1)
    with pytest.raises(CensusDistinctnessError, match="spacing"):
        check_distinct(too_close, [first])


def test_a_window_exactly_at_the_registered_spacing_is_distinct() -> None:
    first = make_window(1, BASE)
    check_distinct(BASE + timedelta(minutes=MIN_MINUTES_BETWEEN_WINDOWS), [first])


def test_the_per_day_cap_forces_the_sample_across_sessions() -> None:
    accepted = [
        make_window(i, BASE + timedelta(hours=i * MIN_MINUTES_BETWEEN_WINDOWS / 60))
        for i in range(MAX_WINDOWS_PER_UTC_DAY)
    ]
    fifth = BASE + timedelta(hours=MAX_WINDOWS_PER_UTC_DAY * 2)
    assert fifth.date() == BASE.date(), "the premise: still the same UTC day"
    with pytest.raises(CensusDistinctnessError, match="cap"):
        check_distinct(fifth, accepted)


def test_the_next_utc_day_reopens_the_cap() -> None:
    accepted = [
        make_window(i, BASE + timedelta(hours=i * MIN_MINUTES_BETWEEN_WINDOWS / 60))
        for i in range(MAX_WINDOWS_PER_UTC_DAY)
    ]
    check_distinct(BASE + timedelta(days=1), accepted)


def test_twenty_windows_need_at_least_five_collection_days() -> None:
    """The arithmetic that makes the census clock-bound rather than effort-bound."""
    assert MIN_OBSERVATION_WINDOWS / MAX_WINDOWS_PER_UTC_DAY == 5.0


# --- the ledger orders by the recorded clock, never by append order ---------


def test_the_ledger_orders_by_the_recorded_clock(tmp_path: Path) -> None:
    """Discrete sampling writes from different processes; file order is not a clock."""
    ledger = CensusLedger(tmp_path / "census.jsonl")
    later = make_window(2, BASE + timedelta(days=1))
    earlier = make_window(1, BASE)
    ledger.append(later)
    ledger.append(earlier)

    stamps = [str(row["local_ts"]) for row in ledger.read_rows()]
    assert stamps == sorted(stamps)
    assert stamps[0].startswith("2026-09-03")


def test_refusals_are_recorded_alongside_windows_rather_than_dropped(tmp_path: Path) -> None:
    ledger = CensusLedger(tmp_path / "census.jsonl")
    ledger.append(make_window(1, BASE))
    ledger.append(
        RefusedWindow(
            local_ts="2026-09-03T13:00:00.000Z",
            environment=Environment.PAPER,
            reason="crossed_book",
            detail="bid above ask",
            leg="option_call",
        )
    )
    summary = summarise(ledger)
    assert summary.n_accepted == 1
    assert summary.n_refused == 1
    assert summary.refusal_reasons == {"crossed_book": 1}
    assert summary.meets_minimum is False
    assert summary.n_required == MIN_OBSERVATION_WINDOWS


def test_an_empty_census_reports_absent_rather_than_zero(tmp_path: Path) -> None:
    summary = summarise(CensusLedger(tmp_path / "census.jsonl"))
    assert isinstance(summary.median_bps, Absent)
    assert isinstance(summary.p90_bps, Absent)
    assert summary.n_accepted == 0


def test_a_percentile_of_an_empty_sample_is_absent_not_nan() -> None:
    assert isinstance(percentile([], 0.9), Absent)


def test_the_percentile_interpolates_as_registered() -> None:
    assert percentile([1.0, 2.0, 3.0, 4.0], 0.5) == 2.5
    assert percentile([10.0], 0.9) == 10.0
