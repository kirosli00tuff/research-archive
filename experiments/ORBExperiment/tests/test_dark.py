"""The universe, signal and verdict modules, built dark against known answers.

**No test here touches a real bar.** Every fixture is either a synthetic
construction or a bar stamped inside the pre-period carve-out, and the runtime
provenance pin refuses `SEALED_VENDOR` in every entry point.
"""

from __future__ import annotations

import pytest

from orb.bars import Bar, Provenance, ProvenanceViolationError
from orb.config import CONFIG
from orb.costs import Side
from orb.signal import (
    OpeningRange,
    Trigger,
    close_exit_c,
    entry_price_c,
    find_trigger,
    opening_range,
    stop_hit,
)
from orb.universe import Candidate, relative_volume, select

MS = 60_000
# 2016-01-04T14:30:00.000Z — the pre-period boundary, i.e. 09:30 Eastern.
OPEN_MS = CONFIG.pre_period_end_ms
# Every fixture bar sits strictly BEFORE the boundary unless it is synthetic.
PRE = OPEN_MS - 5 * 24 * 60 * 60 * 1000  # five days earlier, still 09:30-anchored
RANGE_END = 5 * MS


def bar(
    minute: int,
    o: int,
    h: int,
    low: int,
    c: int,
    v: int = 1000,
    *,
    base: int = PRE,
    provenance: Provenance = Provenance.SYNTHETIC_FIXTURE,
) -> Bar:
    return Bar(base + minute * MS, o, h, low, c, v, provenance)


# --- The provenance pin ---------------------------------------------------


def test_a_sealed_vendor_bar_is_refused_by_every_entry_point() -> None:
    """The dark modules are never pointed at real bars before the latch."""
    sealed = [
        bar(0, 1000, 1050, 950, 1025, base=1_700_000_000_000),
    ]
    sealed = [
        Bar(1_700_000_000_000, 1000, 1050, 950, 1025, 100, Provenance.SEALED_VENDOR)
    ]
    window = (1_700_000_000_000, 1_700_000_000_000 + RANGE_END)
    with pytest.raises(ProvenanceViolationError, match="built dark"):
        opening_range(sealed, window)
    with pytest.raises(ProvenanceViolationError):
        close_exit_c(sealed, window)


def test_a_pre_period_bar_must_actually_be_pre_period() -> None:
    """Claiming the carve-out does not grant it. The boundary is checked."""
    with pytest.raises(ValueError, match="claims PRE_PERIOD"):
        Bar(CONFIG.pre_period_end_ms, 1000, 1050, 950, 1025, 1, Provenance.PRE_PERIOD)
    ok = Bar(
        CONFIG.pre_period_end_ms - 1, 1000, 1050, 950, 1025, 1, Provenance.PRE_PERIOD
    )
    assert ok.provenance is Provenance.PRE_PERIOD


def test_a_malformed_bar_is_refused_at_construction() -> None:
    with pytest.raises(ValueError, match=r"high .* below low"):
        Bar(PRE, 1000, 900, 950, 950, 1, Provenance.SYNTHETIC_FIXTURE)
    with pytest.raises(ValueError, match="open outside"):
        Bar(PRE, 2000, 1050, 950, 1000, 1, Provenance.SYNTHETIC_FIXTURE)
    with pytest.raises(ValueError, match="close outside"):
        Bar(PRE, 1000, 1050, 950, 2000, 1, Provenance.SYNTHETIC_FIXTURE)
    with pytest.raises(ValueError, match="negative volume"):
        Bar(PRE, 1000, 1050, 950, 1000, -1, Provenance.SYNTHETIC_FIXTURE)


# --- Section 2, the universe ---------------------------------------------


def test_relative_volume_is_todays_over_the_trailing_median() -> None:
    """Hand-computed: today 3,000 over a median of 1,000 is exactly 3.0."""
    trailing = [1000] * 14
    assert relative_volume(3000, trailing) == 3.0


def test_relative_volume_uses_the_median_not_the_mean() -> None:
    """One 100,000-share outlier moves a mean and does not move a median.

    Trailing = thirteen 1,000s and one 100,000. Median = 1,000. Mean = 8,071.
    Today 3,000 therefore gives 3.0 on the registered rule, and 0.37 on a mean.
    """
    trailing = [1000] * 13 + [100_000]
    assert relative_volume(3000, trailing) == 3.0


def test_a_zero_trailing_median_is_refused_not_divided_by() -> None:
    """Otherwise every quiet name ranks first by construction."""
    with pytest.raises(ValueError, match="zero or negative"):
        relative_volume(3000, [0] * 14)


def test_a_short_lookback_is_refused() -> None:
    with pytest.raises(ValueError, match="need 14 trailing"):
        relative_volume(3000, [1000] * 13)


def _candidate(ticker: str, relvol: float, **kw: object) -> Candidate:
    defaults: dict[str, object] = {
        "session_open_c": 5001,
        "avg_volume_14": 1_000_001.0,
        "atr_14_c": 51.0,
        "has_locate": True,
        "borrow_rate_annual": 0.05,
    }
    defaults.update(kw)
    return Candidate(ticker=ticker, relative_volume=relvol, **defaults)  # type: ignore[arg-type]


def test_the_selection_takes_the_top_twenty_by_relative_volume() -> None:
    names = {f"T{i:02d}": _candidate(f"T{i:02d}", float(i)) for i in range(40)}
    chosen = select(names)
    assert len(chosen) == CONFIG.selection_width == 20
    assert chosen[0] == "T39"
    assert chosen[-1] == "T20"


def test_ties_break_by_ticker_ascending_so_selection_is_deterministic() -> None:
    names = {t: _candidate(t, 5.0) for t in ("ZZZZ", "AAAA", "MMMM")}
    assert select(names) == ("AAAA", "MMMM", "ZZZZ")


def test_every_section_2_filter_sits_exactly_on_its_boundary() -> None:
    """Section 2 says 'above', so the boundary value itself is excluded."""
    assert not _candidate("X", 9.0, session_open_c=500).passes_filters()
    assert _candidate("X", 9.0, session_open_c=501).passes_filters()

    assert not _candidate("X", 9.0, avg_volume_14=1_000_000.0).passes_filters()
    assert _candidate("X", 9.0, avg_volume_14=1_000_000.1).passes_filters()

    assert not _candidate("X", 9.0, atr_14_c=50.0).passes_filters()
    assert _candidate("X", 9.0, atr_14_c=50.1).passes_filters()


def test_a_filtered_name_never_occupies_a_selection_slot() -> None:
    names = {"HIGH": _candidate("HIGH", 99.0, session_open_c=400)}
    names.update({f"T{i}": _candidate(f"T{i}", 1.0) for i in range(3)})
    chosen = select(names)
    assert "HIGH" not in chosen
    assert len(chosen) == 3


def test_the_short_side_exclusion_sits_exactly_on_25_percent() -> None:
    """'above 25 percent' excludes; 25 percent exactly is still shortable."""
    assert _candidate("X", 1.0, borrow_rate_annual=0.25).shortable()
    assert not _candidate("X", 1.0, borrow_rate_annual=0.2500001).shortable()
    assert not _candidate("X", 1.0, has_locate=False).shortable()


# --- Section 3, the signal -----------------------------------------------

# A five-minute opening range: high 1050, low 950.
RANGE_BARS = [
    bar(0, 1000, 1030, 980, 1010),
    bar(1, 1010, 1050, 1000, 1040),
    bar(2, 1040, 1045, 950, 960),
    bar(3, 960, 1000, 955, 990),
    bar(4, 990, 1020, 970, 1000),
]
WINDOW = (PRE, PRE + RANGE_END)


def the_range(bars: list[Bar]) -> OpeningRange:
    """Narrow the optional away once, so the tests read as arithmetic."""
    r = opening_range(bars, WINDOW)
    assert r is not None
    return r


def test_the_opening_range_is_the_high_and_low_of_the_first_five_minutes() -> None:
    """Hand-computed: max high 1050, min low 950, width 100 cents."""
    r = opening_range(RANGE_BARS, WINDOW)
    assert r is not None
    assert (r.high_c, r.low_c, r.bar_count) == (1050, 950, 5)
    assert r.width_c == 100


def test_a_bar_stamped_exactly_at_0935_is_outside_the_range() -> None:
    """The window is half-open. This fixture sits **on** the boundary."""
    intruder = bar(5, 1000, 9999, 1, 1000)
    r = opening_range([*RANGE_BARS, intruder], WINDOW)
    assert r is not None
    assert (r.high_c, r.low_c) == (1050, 950)


def test_the_entry_is_the_boundary_plus_five_basis_points_rounded_against_us() -> None:
    """1050 x 0.0005 = 0.525 cents, rounded up to 1: entry 1051 long.

    950 x 0.0005 = 0.475 cents, rounded up to 1: entry 949 short. The offset is
    always at least one cent and always rounds away from the boundary, so a
    rounding choice never flatters the fill.
    """
    assert entry_price_c(1050, Side.LONG) == 1051
    assert entry_price_c(950, Side.SHORT) == 949
    assert entry_price_c(10000, Side.LONG) == 10005
    assert entry_price_c(10000, Side.SHORT) == 9995


def test_a_long_breakout_triggers_on_the_first_bar_through_the_high() -> None:
    after = [bar(5, 1000, 1040, 990, 1030), bar(6, 1030, 1060, 1020, 1055)]
    setup = find_trigger([*RANGE_BARS, *after], the_range(RANGE_BARS), WINDOW[1])
    assert setup.trigger is Trigger.LONG
    assert setup.side is Side.LONG
    assert setup.entry_c == 1051
    assert setup.stop_c == 950
    assert setup.triggered_at_ms == PRE + 6 * MS


def test_a_short_breakout_triggers_on_the_first_bar_through_the_low() -> None:
    after = [bar(5, 1000, 1010, 960, 970), bar(6, 970, 980, 940, 945)]
    setup = find_trigger([*RANGE_BARS, *after], the_range(RANGE_BARS), WINDOW[1])
    assert setup.trigger is Trigger.SHORT
    assert setup.entry_c == 949
    assert setup.stop_c == 1050


def test_both_sides_inside_one_bar_is_ambiguous_and_excluded() -> None:
    """The registered ambiguous path. A minute bar cannot say which came first."""
    after = [bar(5, 1000, 1060, 940, 1000)]
    setup = find_trigger([*RANGE_BARS, *after], the_range(RANGE_BARS), WINDOW[1])
    assert setup.trigger is Trigger.AMBIGUOUS
    assert setup.entry_c is None
    assert setup.stop_c is None
    assert setup.side is None


def test_a_session_that_never_breaks_the_range_triggers_nothing() -> None:
    after = [bar(5, 1000, 1050, 950, 1000), bar(6, 1000, 1049, 951, 1000)]
    setup = find_trigger([*RANGE_BARS, *after], the_range(RANGE_BARS), WINDOW[1])
    assert setup.trigger is Trigger.NONE


def test_a_touch_of_the_range_boundary_is_not_a_break() -> None:
    """1050 exactly is not 'through' 1050. The fixture sits on the cent."""
    after = [bar(5, 1000, 1050, 950, 1000)]
    setup = find_trigger([*RANGE_BARS, *after], the_range(RANGE_BARS), WINDOW[1])
    assert setup.trigger is Trigger.NONE


def test_the_stop_and_the_range_boundary_coinciding_to_the_cent() -> None:
    """The registered fixture: a long's stop is the range low, exactly.

    A bar whose low touches 950 — the stop and the boundary at the same cent —
    is a hit. A resting stop fills when prints reach it, not only past it.
    """
    r = opening_range(RANGE_BARS, WINDOW)
    assert r is not None
    after = [bar(5, 1030, 1060, 1020, 1055), bar(6, 1055, 1060, 950, 960)]
    setup = find_trigger([*RANGE_BARS, *after], r, WINDOW[1])
    assert setup.stop_c == 950
    hit = stop_hit([*RANGE_BARS, *after], setup, PRE + 5 * MS)
    assert hit == PRE + 6 * MS

    one_cent_above = [bar(5, 1030, 1060, 1020, 1055), bar(6, 1055, 1060, 951, 960)]
    assert stop_hit(one_cent_above, setup, PRE + 5 * MS) is None


def test_the_close_exit_is_the_last_bar_inside_the_exit_window() -> None:
    exit_bars = [
        bar(385, 1100, 1110, 1090, 1105),
        bar(388, 1105, 1120, 1100, 1118),
        bar(390, 1118, 1130, 1110, 1125),  # outside a 385-389 window
    ]
    window = (PRE + 385 * MS, PRE + 389 * MS)
    assert close_exit_c(exit_bars, window) == 1118


def test_a_half_session_exit_window_still_finds_a_close() -> None:
    """The registered half-session fixture. Half sessions are excluded and counted."""
    from datetime import date

    from orb.calendar import SessionKind, sessions

    half = next(s for s in sessions(date(2024, 12, 24), date(2024, 12, 24)))
    assert half.kind is SessionKind.HALF
    start_ms, end_ms = half.close_exit_utc()
    bars = [
        Bar(start_ms, 1100, 1110, 1090, 1105, 10, Provenance.SYNTHETIC_FIXTURE),
        Bar(end_ms - MS, 1105, 1120, 1100, 1118, 10, Provenance.SYNTHETIC_FIXTURE),
        Bar(end_ms, 1118, 1130, 1110, 1125, 10, Provenance.SYNTHETIC_FIXTURE),
    ]
    assert close_exit_c(bars, (start_ms, end_ms)) == 1118
