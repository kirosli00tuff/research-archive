"""Pacing is per endpoint, refuses unmeasured endpoints, and survives process death."""

from __future__ import annotations

from datetime import UTC, datetime, timedelta
from pathlib import Path

import pytest

from etf.http import PacedClient
from etf.ledger.requests import RequestLedger
from etf.pacing import ABSOLUTE_MIN_SPACING_S, PacingUnknown, min_spacing_s


def test_an_unregistered_endpoint_is_refused_not_defaulted_fast() -> None:
    with pytest.raises(PacingUnknown, match="not a licence to speed up"):
        min_spacing_s("flow.some_new_surface")


def test_the_absolute_floor_holds_even_against_an_override() -> None:
    assert min_spacing_s("flow.table", {"flow.table": 0.0}) == ABSOLUTE_MIN_SPACING_S


def test_paces_differ_per_endpoint_on_the_same_host() -> None:
    """solattn ADR-021: a measurement of one endpoint is not evidence about another."""
    assert min_spacing_s("flow.table") != min_spacing_s("meta.robots")


def test_the_pace_survives_process_death_by_reading_the_ledger(tmp_path: Path) -> None:
    """A limiter living in a client instance paces nothing between systemd fires."""
    now = datetime(2026, 8, 28, 12, 0, tzinfo=UTC)
    ledger = RequestLedger(tmp_path / "r.jsonl", caps_per_day={"flow": 10}, clock=lambda: now)
    ledger.charge("flow", "flow.table")

    slept: list[float] = []
    fresh_client = PacedClient(
        ledger,
        sleeper=slept.append,
        monotonic=lambda: 0.0,
        clock=lambda: now + timedelta(seconds=5),
    )
    fresh_client._pace("flow.table")
    assert slept, "a brand-new client must still pace against the ledger"
    assert slept[0] == pytest.approx(min_spacing_s("flow.table") - 5.0)


def test_a_long_enough_gap_needs_no_wait(tmp_path: Path) -> None:
    now = datetime(2026, 8, 28, 12, 0, tzinfo=UTC)
    ledger = RequestLedger(tmp_path / "r.jsonl", caps_per_day={"flow": 10}, clock=lambda: now)
    ledger.charge("flow", "flow.table")
    slept: list[float] = []
    client = PacedClient(
        ledger,
        sleeper=slept.append,
        monotonic=lambda: 0.0,
        clock=lambda: now + timedelta(hours=1),
    )
    client._pace("flow.table")
    assert slept == []


def test_the_ledger_reports_the_latest_charge_not_the_first(tmp_path: Path) -> None:
    stamps = iter(
        [
            datetime(2026, 8, 28, 12, 0, tzinfo=UTC),
            datetime(2026, 8, 28, 12, 30, tzinfo=UTC),
        ]
    )
    ledger = RequestLedger(
        tmp_path / "r.jsonl", caps_per_day={"flow": 10}, clock=lambda: next(stamps)
    )
    ledger.charge("flow", "flow.table")
    ledger.charge("flow", "flow.table")
    assert ledger.last_charge_at("flow.table") == datetime(2026, 8, 28, 12, 30, tzinfo=UTC)
    assert ledger.last_charge_at("venue.candleSnapshot") is None
