"""Ten named ticker-sessions, hand-computed, pinned to the cent.

**Every quantity in the table below was computed by hand — by reading the bars
and applying Section 3 on paper — and not by the code under test.** That is the
point of a known-answer test: if the code and the hand computation ever
disagree, the hand computation is the referee.

**A recorded limitation, stated rather than glossed.** The task asks for ten
ticker-sessions *drawn from the pre-period carve-out window*. **These bars are
synthetic fixtures stamped inside that window, not real vendor bars**, because
A.1 TASK 1 measured that **0 of 9 vendors serve a bar to this repository**
(`docs/ACCESS.md`). Every timestamp sits strictly before
2016-01-04T14:30:00.000Z and every bar carries `Provenance.PRE_PERIOD`, so the
carve-out gate is genuinely exercised — but the *prices* are constructed. **When
a credential exists, these same ten ticker-sessions are re-run against real
pre-period bars and the hand computations are redone against them.** Recorded as
an open item; nothing here is presented as a measurement of the world.
"""

from __future__ import annotations

from dataclasses import dataclass

import pytest

from orb.bars import Bar, Provenance
from orb.config import CONFIG
from orb.costs import Side
from orb.signal import Trigger, close_exit_c, find_trigger, opening_range

MS = 60_000
DAY = 24 * 60 * 60 * 1000

# 09:30 Eastern on 2015-12-28, five sessions before the carve-out boundary.
# Every fixture is offset backwards from the boundary, so all are pre-period.
BOUNDARY = CONFIG.pre_period_end_ms


def session_open(days_before: int) -> int:
    return BOUNDARY - days_before * DAY


def pre_bar(base: int, minute: int, o: int, h: int, low: int, c: int, v: int) -> Bar:
    return Bar(base + minute * MS, o, h, low, c, v, Provenance.PRE_PERIOD)


type Row = tuple[int, int, int, int, int]


@dataclass(frozen=True, slots=True)
class Case:
    """One named ticker-session, with its HAND-COMPUTED answers."""

    ticker: str
    days: int
    range_bars: tuple[Row, ...]
    post_bars: tuple[Row, ...]
    high: int
    low: int
    trigger: Trigger
    entry: int | None
    stop: int | None
    close: int


CASES: list[Case] = [
    Case(
        ticker="ABCD",
        days=5,
        range_bars=(
            (2000, 2040, 1990, 2030, 5000),
            (2030, 2075, 2020, 2060, 4000),
            (2060, 2065, 1975, 1990, 6000),
            (1990, 2010, 1985, 2005, 3000),
            (2005, 2030, 2000, 2025, 3500),
        ),
        # hand: high = max(2040,2075,2065,2010,2030) = 2075
        #       low  = min(1990,2020,1975,1985,2000) = 1975
        post_bars=((2025, 2070, 2015, 2065, 2000), (2065, 2090, 2060, 2085, 2500)),
        high=2075,
        low=1975,
        trigger=Trigger.LONG,
        # hand: 2075 * 0.0005 = 1.0375 cents -> ceil to 2 -> 2075 + 2 = 2077
        entry=2077,
        stop=1975,
        close=2085,
    ),
    Case(
        ticker="BETA",
        days=6,
        range_bars=(
            (1000, 1020, 995, 1015, 9000),
            (1015, 1030, 1010, 1025, 8000),
            (1025, 1028, 990, 995, 7000),
            (995, 1005, 985, 1000, 6000),
            (1000, 1010, 998, 1008, 5000),
        ),
        # hand: high = 1030, low = 985
        post_bars=((1008, 1012, 980, 982, 4000),),
        high=1030,
        low=985,
        trigger=Trigger.SHORT,
        # hand: 985 * 0.0005 = 0.4925 -> ceil to 1 -> 985 - 1 = 984
        entry=984,
        stop=1030,
        close=982,
    ),
    Case(
        ticker="CRUX",
        days=7,
        range_bars=(
            (5000, 5100, 4950, 5050, 12000),
            (5050, 5080, 5000, 5020, 11000),
            (5020, 5060, 4900, 4950, 15000),
            (4950, 5000, 4940, 4990, 9000),
            (4990, 5050, 4980, 5040, 8000),
        ),
        # hand: high = 5100, low = 4900
        post_bars=((5040, 5090, 5030, 5080, 7000), (5080, 5150, 5070, 5140, 6000)),
        high=5100,
        low=4900,
        trigger=Trigger.LONG,
        # hand: 5100 * 0.0005 = 2.55 -> ceil to 3 -> 5103
        entry=5103,
        stop=4900,
        close=5140,
    ),
    Case(
        ticker="DELT",
        days=8,
        range_bars=(
            (800, 815, 795, 810, 20000),
            (810, 812, 800, 805, 18000),
            (805, 820, 790, 800, 22000),
            (800, 808, 798, 802, 17000),
            (802, 806, 799, 804, 16000),
        ),
        # hand: high = 820, low = 790
        post_bars=((804, 806, 802, 805, 5000), (805, 807, 803, 806, 4000)),
        high=820,
        low=790,
        trigger=Trigger.NONE,
        entry=None,
        stop=None,
        close=806,
    ),
    Case(
        ticker="ECHO",
        days=9,
        range_bars=(
            (1500, 1550, 1480, 1520, 30000),
            (1520, 1530, 1500, 1510, 28000),
            (1510, 1515, 1470, 1475, 33000),
            (1475, 1490, 1465, 1485, 25000),
            (1485, 1495, 1480, 1490, 24000),
        ),
        # hand: high = 1550, low = 1465
        # post bar breaks BOTH: high 1560 > 1550 and low 1460 < 1465
        post_bars=((1490, 1560, 1460, 1500, 40000),),
        high=1550,
        low=1465,
        trigger=Trigger.AMBIGUOUS,
        entry=None,
        stop=None,
        close=1500,
    ),
    Case(
        ticker="FOXX",
        days=10,
        range_bars=(
            (10000, 10100, 9950, 10050, 4000),
            (10050, 10080, 10000, 10020, 3800),
            (10020, 10060, 9900, 9950, 4200),
            (9950, 10000, 9940, 9990, 3600),
            (9990, 10050, 9980, 10040, 3400),
        ),
        # hand: high = 10100, low = 9900
        post_bars=((10040, 10120, 10030, 10110, 3000),),
        high=10100,
        low=9900,
        trigger=Trigger.LONG,
        # hand: 10100 * 0.0005 = 5.05 -> ceil to 6 -> 10106
        entry=10106,
        stop=9900,
        close=10110,
    ),
    Case(
        ticker="GOLF",
        days=11,
        range_bars=(
            (600, 610, 590, 605, 50000),
            (605, 608, 600, 602, 48000),
            (602, 606, 585, 588, 52000),
            (588, 595, 583, 592, 45000),
            (592, 598, 590, 596, 44000),
        ),
        # hand: high = 610, low = 583
        post_bars=((596, 600, 580, 582, 60000),),
        high=610,
        low=583,
        trigger=Trigger.SHORT,
        # hand: 583 * 0.0005 = 0.2915 -> ceil to 1 -> 582
        entry=582,
        stop=610,
        close=582,
    ),
    Case(
        ticker="HOTL",
        days=12,
        range_bars=(
            (2500, 2520, 2480, 2510, 7000),
            (2510, 2515, 2495, 2500, 6800),
            (2500, 2530, 2470, 2475, 7200),
            (2475, 2490, 2465, 2485, 6400),
            (2485, 2495, 2480, 2490, 6200),
        ),
        # hand: high = 2530, low = 2465
        # A touch of exactly 2530 is NOT a break.
        post_bars=((2490, 2530, 2485, 2520, 5000), (2520, 2535, 2515, 2532, 4800)),
        high=2530,
        low=2465,
        trigger=Trigger.LONG,
        # hand: 2530 * 0.0005 = 1.265 -> ceil to 2 -> 2532
        entry=2532,
        stop=2465,
        close=2532,
    ),
    Case(
        ticker="INDX",
        days=13,
        range_bars=(
            (3000, 3030, 2990, 3020, 11000),
            (3020, 3040, 3010, 3030, 10500),
            (3030, 3035, 2980, 2985, 11500),
            (2985, 3000, 2975, 2995, 9500),
            (2995, 3010, 2990, 3005, 9000),
        ),
        # hand: high = 3040, low = 2975
        post_bars=((3005, 3020, 2970, 2978, 12000),),
        high=3040,
        low=2975,
        trigger=Trigger.SHORT,
        # hand: 2975 * 0.0005 = 1.4875 -> ceil to 2 -> 2973
        entry=2973,
        stop=3040,
        close=2978,
    ),
    Case(
        ticker="JULI",
        days=14,
        range_bars=(
            (150, 160, 145, 155, 90000),
            (155, 158, 150, 152, 88000),
            (152, 156, 142, 144, 92000),
            (144, 149, 140, 147, 85000),
            (147, 151, 145, 150, 84000),
        ),
        # hand: high = 160, low = 140
        post_bars=((150, 162, 148, 161, 70000),),
        high=160,
        low=140,
        trigger=Trigger.LONG,
        # hand: 160 * 0.0005 = 0.08 -> ceil to 1 (floor of one cent) -> 161
        entry=161,
        stop=140,
        close=161,
    ),
]


def _bars(case: Case) -> tuple[list[Bar], tuple[int, int], int]:
    base = session_open(case.days)
    bars = [pre_bar(base, m, *row) for m, row in enumerate(case.range_bars)]
    bars += [pre_bar(base, 5 + i, *row) for i, row in enumerate(case.post_bars)]
    return bars, (base, base + 5 * MS), base


@pytest.mark.parametrize("case", CASES, ids=[c.ticker for c in CASES])
def test_ten_hand_computed_ticker_sessions_match_to_the_cent(case: Case) -> None:
    bars, window, base = _bars(case)

    # Every bar is genuinely inside the carve-out.
    for b in bars:
        assert b.timestamp_ms < CONFIG.pre_period_end_ms
        assert b.provenance is Provenance.PRE_PERIOD

    range_ = opening_range(bars, window)
    assert range_ is not None
    assert range_.high_c == case.high, case.ticker
    assert range_.low_c == case.low, case.ticker
    assert range_.bar_count == 5

    setup = find_trigger(bars, range_, window[1])
    assert setup.trigger is case.trigger, case.ticker
    assert setup.entry_c == case.entry, case.ticker
    assert setup.stop_c == case.stop, case.ticker

    if setup.trigger is Trigger.LONG:
        assert setup.side is Side.LONG
        assert setup.entry_c is not None and setup.entry_c > range_.high_c
        assert setup.stop_c == range_.low_c
    elif setup.trigger is Trigger.SHORT:
        assert setup.side is Side.SHORT
        assert setup.entry_c is not None and setup.entry_c < range_.low_c
        assert setup.stop_c == range_.high_c

    last_minute = 5 + len(case.post_bars) - 1
    exit_window = (base + last_minute * MS, base + (last_minute + 1) * MS)
    assert close_exit_c(bars, exit_window) == case.close, case.ticker


def test_the_ten_cases_cover_every_registered_trigger_state() -> None:
    """A known-answer suite that never exercises a branch pins nothing."""
    seen = {c.trigger for c in CASES}
    assert seen == {Trigger.LONG, Trigger.SHORT, Trigger.NONE, Trigger.AMBIGUOUS}
    assert len(CASES) == 10
    assert len({c.ticker for c in CASES}) == 10


def test_the_entry_offset_floor_of_one_cent_binds_on_a_cheap_name() -> None:
    """JULI: 160 cents x 0.0005 = 0.08 cents. The one-cent floor decides."""
    juli = next(c for c in CASES if c.ticker == "JULI")
    assert 160 * CONFIG.entry_offset_fraction == pytest.approx(0.08)
    assert juli.entry == 161
