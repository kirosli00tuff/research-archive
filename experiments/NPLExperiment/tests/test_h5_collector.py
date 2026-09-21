"""H5 Task 4: the forward collector's coverage accounting and its yield to H2."""

from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path

import pytest

from npl.callstate import ALL_STATES, CallState
from npl.h5.census import InstrumentRow, census_summary
from npl.h5.collector import H5YieldedToH2, require_headroom
from npl.h5.coverage import coverage_of
from npl.h5.listing import STATUS_DELISTED, STATUS_LIVE
from npl.ledger.requests import RequestLedger

CLOCK = datetime(2026, 8, 28, 21, 0, tzinfo=UTC)


def _row(
    coin: str,
    *,
    resolved: bool = True,
    status: str = STATUS_LIVE,
    l2: str = "stored",
    funding: str = "stored",
    reference: bool = True,
    basis: float | None = 3.0,
    absence: str = "",
) -> InstrumentRow:
    return InstrumentRow(
        coin=coin,
        dex="xyz",
        ticker=coin.split(":")[-1],
        resolution_state="resolved" if resolved else "excluded_non_equity",
        resolution_reason="equity" if resolved else "crypto",
        underlying_symbol=coin.split(":")[-1],
        underlying_kind="equity",
        underlying_family="equity_single",
        is_delisted=status == STATUS_DELISTED,
        listing_status=status,
        sz_decimals=2,
        max_leverage=10,
        snapshot_id="pass-1",
        at_ms=1_787_000_000_000,
        session_tag="regular",
        ctx_state="stored",
        served_fields=("markPx", "oraclePx"),
        mark_served=True,
        reference_field="oraclePx" if reference else "",
        reference_served=reference,
        basis_bp=basis,
        basis_absence=absence,
        open_interest=1.0,
        day_notional_volume=1.0,
        funding_field_served=True,
        funding_history_state=funding,
        funding_history_rows=168,
        funding_first_time_ms=1,
        funding_last_time_ms=2,
        l2_state=l2,
        touch_spread_bp=4.0,
        bid_depth5_notional=1.0,
        ask_depth5_notional=1.0,
        cohorts=(),
        quarantined=False,
    )


def test_coverage_reports_all_six_call_states_even_at_zero() -> None:
    """An omitted state reads as 'no such state'; a zero reads as 'measured, none'."""
    coverage = coverage_of("pass-1", 1_787_000_000_000, "regular", [_row("xyz:AAPL")])
    for states in (coverage.ctx_states, coverage.funding_states, coverage.l2_states):
        assert sorted(states) == sorted(s.value for s in ALL_STATES)
        assert len(states) == 6
    assert coverage.l2_states["stored"] == 1
    assert coverage.l2_states["rate_limited"] == 0


def test_coverage_separates_health_from_composition() -> None:
    rows = [
        _row("xyz:AAPL"),
        _row("xyz:NVDA", l2="rate_limited", funding="source_failed"),
        _row("xyz:DEAD", status=STATUS_DELISTED, l2="excluded_ineligible", funding="no_data"),
        _row("hyna:BTC", resolved=False, l2="excluded_ineligible", funding="excluded_ineligible"),
    ]
    coverage = coverage_of("pass-1", 1_787_000_000_000, "regular", rows)
    assert coverage.instruments_enumerated == 4
    assert coverage.instruments_resolved == 3
    assert coverage.instruments_live == 2
    assert coverage.instruments_probed == 2
    assert coverage.l2_states["rate_limited"] == 1
    assert coverage.l2_states["excluded_ineligible"] == 1
    assert coverage.funding_states["source_failed"] == 1
    assert coverage.funding_states["no_data"] == 1


def test_coverage_counts_reference_service_and_basis_absences() -> None:
    rows = [
        _row("xyz:AAPL"),
        _row("xyz:NOREF", reference=False, basis=None, absence="not_served"),
        _row("xyz:ZERO", basis=None, absence="zero_denominator"),
    ]
    coverage = coverage_of("pass-1", 1, "regular", rows)
    assert coverage.reference_served == 2
    assert coverage.reference_unserved == 1
    assert coverage.basis_served == 1
    assert coverage.basis_absent_by_reason == {"not_served": 1, "zero_denominator": 1}


def test_an_unregistered_call_state_is_refused_not_bucketed() -> None:
    with pytest.raises(ValueError, match="unregistered call state"):
        coverage_of("pass-1", 1, "regular", [_row("xyz:AAPL", l2="probably_fine")])


def test_h5_yields_to_h2_at_the_soft_budget_boundary(tmp_path: Path) -> None:
    """The bar sits AT the soft budget: one under runs, exactly at refuses."""
    path = tmp_path / "requests.jsonl"
    ledger = RequestLedger(path=path, cap_per_day=1_000, clock=lambda: CLOCK)
    for _ in range(9):
        ledger.charge("info:meta")
    require_headroom(ledger, soft_budget=10, day="2026-08-28")
    ledger.charge("info:meta")
    with pytest.raises(H5YieldedToH2, match="postpones to tomorrow"):
        require_headroom(ledger, soft_budget=10, day="2026-08-28")


def test_the_six_registered_states_are_exactly_the_call_state_enum() -> None:
    assert len(ALL_STATES) == 6
    assert CallState.STORED in ALL_STATES


def test_the_census_summary_splits_every_primary_figure_by_listing_status() -> None:
    """Amendment H5-2: the live stratum is the universe, the delisted one rides beside."""
    rows = [
        _row("xyz:AAPL"),
        _row("xyz:NVDA"),
        _row("cash:INTC", status=STATUS_DELISTED, l2="no_data", funding="no_data"),
        _row("hyna:BTC", resolved=False, l2="excluded_ineligible", funding="excluded_ineligible"),
    ]
    summary = census_summary(rows)
    assert summary["instruments_total"] == 4
    assert summary["resolved"] == 3
    assert summary["live"] == 2
    assert summary["excluded_delisted"] == 1
    assert summary["listing_conflicting"] == 0
    assert summary["reference_served_live"] == 2
    assert summary["reference_served_resolved"] == 3
    assert summary["funding_served_of_live_reference_carrying"] == 2
    assert summary["funding_history_states_live"] == {"stored": 2}
    assert summary["funding_history_states_resolved"] == {"stored": 2, "no_data": 1}
    assert summary["by_dex_live"] == {"xyz": 2}


def test_the_census_summary_of_an_empty_pass_reports_zero_not_nothing() -> None:
    summary = census_summary([])
    assert summary["instruments_total"] == 0
    assert summary["live"] == 0
    assert summary["snapshot_id"] == ""
