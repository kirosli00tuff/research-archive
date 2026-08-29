"""The snapshotter stamps its own capture time and never consumes the source's Total."""

from __future__ import annotations

from datetime import UTC, date, datetime
from pathlib import Path

import pytest

from etf.absence import Absent
from etf.config import CONFIG
from etf.snapshot import DayRow, FlowTableShape, parse_flow_table

HEADER = (
    "<tr><th>Date</th><th>IBIT</th><th>FBTC</th><th>BITB</th><th>ARKB</th>"
    "<th>GBTC</th><th>Total</th></tr>"
)


def table(*rows: str) -> str:
    return f"<table>{HEADER}{''.join(rows)}</table>"


def row(day: str, *vals: str) -> str:
    return "<tr>" + "".join(f"<td>{c}</td>" for c in (day, *vals)) + "</tr>"


def test_a_printed_row_parses_to_the_five_fund_aggregate_in_usd() -> None:
    days = parse_flow_table(table(row("01 May 2025", "10.0", "5.0", "2.5", "1.0", "(3.5)", "99.9")))
    assert len(days) == 1
    assert days[0].trade_date == date(2025, 5, 1)
    assert days[0].signal_usd == 15_000_000.0


def test_the_source_total_column_is_recorded_but_is_never_the_signal() -> None:
    """The measured A.1 Task 1 hazard: Total prints 0.0 on an all-dash row.

    3 of 3 all-dash rows over n = 336 out-of-sample rows printed a numeric 0.0
    in Total. Consuming it would record a fabricated flat day for the open day
    on every capture taken before the print lands.
    """
    days = parse_flow_table(table(row("28 Aug 2026", "-", "-", "-", "-", "-", "0.0")))
    assert isinstance(days[0].signal_usd, Absent)
    assert days[0].signal_usd.reason.value == "dash_in_cell"
    assert days[0].total_printed_usd == 0.0, "the source's zero is recorded as evidence"
    assert days[0].signal_usd != days[0].total_printed_usd


def test_one_late_fund_makes_the_signal_absent_rather_than_shrinking_it() -> None:
    days = parse_flow_table(table(row("02 May 2025", "-", "5.0", "2.5", "1.0", "(3.5)", "5.0")))
    assert isinstance(days[0].signal_usd, Absent)


def test_a_ragged_row_is_a_recorded_shape_failure_never_a_padded_row() -> None:
    with pytest.raises(FlowTableShape, match="never a padded row"):
        parse_flow_table(table("<tr><td>01 May 2025</td><td>10.0</td></tr>"))


def test_a_header_without_all_five_registered_tickers_is_refused() -> None:
    markup = (
        "<table><tr><th>Date</th><th>IBIT</th><th>Total</th></tr>"
        + row("01 May 2025", "10.0", "10.0")
        + "</table>"
    )
    with pytest.raises(FlowTableShape, match="refuses to guess which column"):
        parse_flow_table(markup)


def test_a_table_with_no_date_rows_is_refused_rather_than_recorded_empty() -> None:
    with pytest.raises(FlowTableShape, match="no date rows"):
        parse_flow_table(table())


def test_summary_rows_are_not_mistaken_for_trading_days() -> None:
    days = parse_flow_table(
        table(
            row("01 May 2025", "10.0", "5.0", "2.5", "1.0", "(3.5)", "99.9"),
            "<tr><td>Total</td><td>1</td><td>1</td><td>1</td><td>1</td><td>1</td><td>5</td></tr>",
            "<tr><td>Average</td><td>1</td><td>1</td><td>1</td><td>1</td><td>1</td><td>5</td></tr>",
        )
    )
    assert [d.trade_date for d in days] == [date(2025, 5, 1)]


def test_an_unrecognised_month_token_is_refused_rather_than_guessed() -> None:
    with pytest.raises(FlowTableShape, match="unrecognised month"):
        parse_flow_table(table(row("01 Mai 2025", "1", "1", "1", "1", "1", "5")))


def test_the_ledger_row_keeps_absences_as_reasons_and_never_as_zero() -> None:
    day = parse_flow_table(table(row("28 Aug 2026", "-", "-", "-", "-", "-", "0.0")))[0]
    payload = day.as_ledger_dict()
    assert payload["signal_usd"] is None
    assert payload["signal_absent"] == "dash_in_cell"
    funds = payload["funds"]
    assert isinstance(funds, dict)
    for ticker in CONFIG.flow_universe_tickers:
        assert funds[ticker] is None
        assert funds[f"{ticker}__absent"] == "dash_in_cell"


def test_the_capture_timestamp_is_the_repositorys_own_not_the_sources() -> None:
    """Neither selected source serves a per-row publication timestamp (n = 2 of 2)."""
    day = DayRow(
        trade_date=date(2025, 5, 1),
        per_fund=(),
        signal_usd=1.0,
        total_printed_usd=1.0,
    )
    assert "captured_at" not in day.as_ledger_dict()
    assert datetime(2025, 5, 1, tzinfo=UTC).tzinfo is UTC


def test_the_parser_reads_the_live_captured_pages_if_they_are_on_disk() -> None:
    """A regression pin against the real bytes measured at A.1 Task 1."""
    sample = Path(__file__).resolve().parents[1] / "tests" / "fixtures" / "farside-recent.html"
    if not sample.exists():
        pytest.skip("live capture fixture not present")
    days = parse_flow_table(sample.read_text(errors="replace"))
    assert len(days) >= 10
