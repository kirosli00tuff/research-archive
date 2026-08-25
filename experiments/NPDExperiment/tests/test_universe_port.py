"""The ported rule must reproduce the source membership exactly."""

from __future__ import annotations

import pytest

from npd.config import CONFIG
from npd.data.formations import PARAMS, verify_against_source
from npd.data.store import open_store
from npd.data.universe import (
    Candidate,
    RuleParams,
    classify_fund,
    formation_dates,
    median,
    rank_members,
    rejection_reason,
    window_bounds,
)
from npd.paths import STORE_DB


def test_the_ported_rule_builds_the_registered_rule_id() -> None:
    assert PARAMS.rule_id == CONFIG.universe_id == "U-LIQ-500-stk-w60-m40-p5"


def test_fund_classification_is_tri_state_and_none_is_not_false() -> None:
    assert classify_fund("SPDR S&P 500 ETF Trust", "ARCA") is True
    assert classify_fund("", "NASDAQ") is None, "an absent name must not read as not a fund"
    assert classify_fund("Northern Trust Corporation", "NASDAQ") is False
    assert classify_fund("Invesco QQQ Trust, Series 1", "NASDAQ") is True


def test_an_unclassified_instrument_is_excluded_not_admitted() -> None:
    cand = Candidate(
        "X",
        window_bars=60,
        median_close=50.0,
        median_dollar_volume=1e9,
        is_fund=None,
        segment_break_in_window=False,
    )
    assert rejection_reason(cand, PARAMS) == "unclassified"
    assert rejection_reason(cand, RuleParams(include_funds=True)) == "unclassified"


def test_rejection_reasons_are_returned_so_they_can_be_recorded() -> None:
    thin = Candidate("X", 10, 50.0, 1e9, False, False)
    cheap = Candidate("X", 60, 1.0, 1e9, False, False)
    broken = Candidate("X", 60, 50.0, 1e9, False, True)
    ok = Candidate("X", 60, 50.0, 1e9, False, False)
    thin_reason = rejection_reason(thin, PARAMS)
    assert thin_reason is not None and thin_reason.startswith("thin_window")
    cheap_reason = rejection_reason(cheap, PARAMS)
    assert cheap_reason is not None and cheap_reason.startswith("below_price_floor")
    assert rejection_reason(broken, PARAMS) == "listing_segment_break_in_window"
    assert rejection_reason(ok, PARAMS) is None


def test_ranking_ties_break_on_symbol_so_membership_is_deterministic() -> None:
    a = Candidate("BBB", 60, 50.0, 1e9, False, False)
    b = Candidate("AAA", 60, 50.0, 1e9, False, False)
    members, _ = rank_members([a, b], PARAMS)
    assert [m.candidate.symbol for m in members] == ["AAA", "BBB"]


def test_the_trailing_window_ends_before_the_formation_date() -> None:
    sessions = [f"2025-01-{d:02d}" for d in range(1, 32)]
    start, end = window_bounds(sessions, "2025-01-31", 10)
    assert end < "2025-01-31"
    assert sessions.index(end) == sessions.index("2025-01-31") - 1
    assert sessions.index(start) == sessions.index("2025-01-31") - 10


def test_a_formation_without_a_full_window_raises() -> None:
    sessions = [f"2025-01-{d:02d}" for d in range(1, 6)]
    with pytest.raises(ValueError, match="no full trailing window"):
        window_bounds(sessions, "2025-01-03", 10)


def test_formation_dates_are_first_sessions_of_months_with_a_full_window() -> None:
    sessions = [f"2025-{m:02d}-{d:02d}" for m in (1, 2, 3) for d in range(1, 21)]
    out = formation_dates(sessions, RuleParams(window_sessions=25))
    assert out == ["2025-03-01"]


def test_median_raises_on_empty_rather_than_guessing() -> None:
    with pytest.raises(ValueError):
        median([])
    assert median([1.0, 3.0]) == 2.0


@pytest.mark.slow
@pytest.mark.skipif(not STORE_DB.exists(), reason="the local store has not been built")
def test_the_port_reproduces_the_source_membership() -> None:
    with open_store() as con:
        dates = [
            r[0]
            for r in con.execute(
                "SELECT DISTINCT formation_date FROM formation ORDER BY formation_date"
            )
        ]
    assert dates, "no formations were built"
    sample = [dates[0], dates[len(dates) // 2], dates[-1]]
    with open_store() as con:
        for f in sample:
            result = verify_against_source(con, f)
            assert result.ok, f"{f} diverged from the source: {result.first_difference}"
            assert result.n_reproduced == 500
