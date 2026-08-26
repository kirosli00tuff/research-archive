"""The ported rule must reproduce the source membership exactly."""

from __future__ import annotations

import pytest

from insider.config import CONFIG
from insider.market.port_check import PARAMS, reproduce
from insider.market.universe import (
    Candidate,
    RuleParams,
    classify_fund,
    formation_dates,
    median,
    rank_members,
    rejection_reason,
    window_bounds,
)
from insider.paths import SOURCE_BARS_DB


def test_the_ported_rule_builds_the_registered_rule_id() -> None:
    assert PARAMS.rule_id == CONFIG.universe_id == "U-LIQ-500-stk-w60-m40-p5"


def test_fund_classification_is_tri_state_and_none_is_not_false() -> None:
    assert classify_fund("SPDR S&P 500 ETF Trust", "ARCA") is True
    assert classify_fund("", "NASDAQ") is None, "an absent name must not read as not a fund"
    assert classify_fund("Northern Trust Corporation", "NASDAQ") is False
    assert classify_fund("Invesco QQQ Trust, Series 1", "NASDAQ") is True


def test_an_unclassified_instrument_is_excluded_not_admitted() -> None:
    cand = Candidate("X", 60, 50.0, 1e9, is_fund=None, segment_break_in_window=False)
    assert rejection_reason(cand, PARAMS) == "unclassified"
    assert rejection_reason(cand, RuleParams(include_funds=True)) == "unclassified"


def test_rejection_reasons_are_returned_so_every_rejection_can_be_recorded() -> None:
    thin = rejection_reason(Candidate("X", 10, 50.0, 1e9, False, False), PARAMS)
    cheap = rejection_reason(Candidate("X", 60, 1.0, 1e9, False, False), PARAMS)
    assert thin is not None and thin.startswith("thin_window")
    assert cheap is not None and cheap.startswith("below_price_floor")
    assert rejection_reason(Candidate("X", 60, 50.0, 1e9, False, True), PARAMS) == (
        "listing_segment_break_in_window"
    )
    assert rejection_reason(Candidate("X", 60, 50.0, 1e9, False, False), PARAMS) is None


def test_ranking_ties_break_on_symbol_so_membership_is_deterministic() -> None:
    members, _ = rank_members(
        [
            Candidate("BBB", 60, 50.0, 1e9, False, False),
            Candidate("AAA", 60, 50.0, 1e9, False, False),
        ],
        PARAMS,
    )
    assert [m.candidate.symbol for m in members] == ["AAA", "BBB"]


def test_the_trailing_window_ends_before_the_formation_date() -> None:
    sessions = [f"2025-01-{d:02d}" for d in range(1, 32)]
    start, end = window_bounds(sessions, "2025-01-31", 10)
    assert end < "2025-01-31"
    assert sessions.index(end) == sessions.index("2025-01-31") - 1
    assert sessions.index(start) == sessions.index("2025-01-31") - 10


def test_a_formation_without_a_full_window_raises() -> None:
    with pytest.raises(ValueError, match="no full trailing window"):
        window_bounds([f"2025-01-{d:02d}" for d in range(1, 6)], "2025-01-03", 10)


def test_formation_dates_are_first_sessions_of_months_with_a_full_window() -> None:
    sessions = [f"2025-{m:02d}-{d:02d}" for m in (1, 2, 3) for d in range(1, 21)]
    assert formation_dates(sessions, RuleParams(window_sessions=25)) == ["2025-03-01"]


def test_median_raises_on_empty_rather_than_guessing() -> None:
    with pytest.raises(ValueError):
        median([])
    assert median([1.0, 3.0]) == 2.0


@pytest.mark.slow
@pytest.mark.skipif(not SOURCE_BARS_DB.exists(), reason="the source bar store is not present")
@pytest.mark.parametrize("formation", ["2016-04-01", "2021-04-01", "2026-07-01"])
def test_the_port_reproduces_the_source_membership(formation: str) -> None:
    result = reproduce(formation, CONFIG.universe_id)
    assert result.ok, f"{formation} diverged from the source: {result.first_difference}"
    assert result.n_stored == result.n_reproduced == 500
