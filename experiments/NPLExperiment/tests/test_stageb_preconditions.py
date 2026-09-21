"""Stage B.0 precondition pins. Boundary fixtures sit ON the registered bars.

Counts and timestamps only: nothing in these fixtures gives the reader a
price to see, and the module under test opens sealed bytes through the
blindness readers alone.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from npl.census import CensusRow
from npl.clock import MS_PER_DAY, MS_PER_HOUR
from npl.config import CONFIG
from npl.power import min_n_for_power
from npl.seals import seal_raw
from npl.stageb.preconditions import (
    MIN_N_P1,
    MIN_N_P2,
    MIN_N_P3,
    FundingTimes,
    PreconditionFailure,
    assess_window,
    module_hashes,
    reconstruct_cohort,
    run_preconditions,
)

LISTING = CONFIG.funding_archive_epoch_ms + 400 * MS_PER_DAY
ENTRY = LISTING + 2 * MS_PER_DAY


def _census_row(
    coin: str,
    first_open: int,
    first_funding: int,
    *,
    last_close: int,
    rows: int,
    delisted: bool = False,
) -> CensusRow:
    return CensusRow(
        coin=coin,
        dex="",
        event_type="vanilla",
        hyperp_source="",
        is_delisted=delisted,
        sz_decimals=2,
        max_leverage=10,
        state="stored",
        first_1d_open_ms=first_open,
        last_1d_close_ms=last_close,
        candle_rows=rows,
        funding_state="stored",
        first_funding_time_ms=first_funding,
        funding_page_rows=rows,
        recorded_at="2026-08-27T00:00:00Z",
    )


def _seal_candles(root: Path, coin: str, entry_ms: int, day_opens: list[int]) -> None:
    rows = [
        {
            "t": t,
            "T": t + MS_PER_DAY,
            "s": coin,
            "i": "1d",
            "o": "1.0",
            "c": "1.0",
            "h": "1.0",
            "l": "1.0",
            "v": "1.0",
            "n": 1,
        }
        for t in day_opens
    ]
    seal_raw(root / coin, f"retro-candles-{entry_ms // MS_PER_DAY}", json.dumps(rows).encode())


def _seal_funding(root: Path, coin: str, times: list[int]) -> None:
    rows = [{"coin": coin, "fundingRate": "0.0000125", "time": t} for t in times]
    seal_raw(root / coin, "page-00000", json.dumps(rows).encode())


def _hours(start_exclusive_ms: int, count: int) -> list[int]:
    return [start_exclusive_ms + (i + 1) * MS_PER_HOUR for i in range(count)]


# ------------------------------------------------------------- registered N --


def test_min_n_constants_pin_to_the_power_method() -> None:
    cfg = CONFIG
    assert (
        min_n_for_power(cfg.p1_bar, cfg.p1_true_share, cfg.alpha_adj, cfg.power_go_floor, 150)
        == MIN_N_P1
    )
    assert (
        min_n_for_power(0.5, cfg.p2_true_share, cfg.alpha_adj, cfg.power_go_floor, 150) == MIN_N_P2
    )
    assert (
        min_n_for_power(0.5, cfg.p3_true_share, cfg.alpha_adj, cfg.power_go_floor, 150) == MIN_N_P3
    )


# ------------------------------------------------------------ reconstruction --


def _cohort_fixture() -> tuple[list[CensusRow], list[dict[str, object]], list[dict[str, object]]]:
    census = [
        _census_row("YOUNG", LISTING, LISTING, last_close=LISTING + 95 * MS_PER_DAY, rows=95),
        _census_row(
            "OLD",
            LISTING - 200 * MS_PER_DAY,
            LISTING - 200 * MS_PER_DAY,
            last_close=LISTING + 95 * MS_PER_DAY,
            rows=295,
        ),
    ]
    plan: list[dict[str, object]] = [
        {"kind": "event", "coin": "YOUNG", "dex": "", "listing_open_ms": LISTING},
        {"kind": "event", "coin": "OLD", "dex": "", "listing_open_ms": ENTRY - 2 * MS_PER_DAY},
    ]
    pairs: list[dict[str, object]] = [
        {"event_coin": "YOUNG", "control_coin": "OLD", "dex": "", "entry_ms": ENTRY}
    ]
    return census, plan, pairs


def test_reconstruct_splits_events_from_control_windows() -> None:
    census, plan, pairs = _cohort_fixture()
    events, controls = reconstruct_cohort(census, plan, pairs)
    assert len(events) == 1
    assert len(controls) == 1
    event = events[0]
    assert event.coin == "YOUNG"
    assert event.entry_ms == ENTRY
    assert not event.truncated_by_delisting
    assert controls[0].control_coin == "OLD"
    assert controls[0].event_coin == "YOUNG"


def test_a_plan_row_matching_nothing_is_refused() -> None:
    census, plan, pairs = _cohort_fixture()
    stray: dict[str, object] = {
        "kind": "event",
        "coin": "OLD",
        "dex": "",
        "listing_open_ms": LISTING + 7 * MS_PER_DAY,
    }
    with pytest.raises(PreconditionFailure, match="neither a resolved event"):
        reconstruct_cohort(census, [*plan, stray], pairs)


def test_a_delisted_event_truncates_at_its_last_served_close() -> None:
    census, plan, pairs = _cohort_fixture()
    truncated_close = ENTRY + 40 * MS_PER_DAY
    census[0] = _census_row(
        "YOUNG", LISTING, LISTING, last_close=truncated_close, rows=42, delisted=True
    )
    events, _ = reconstruct_cohort(census, plan, pairs)
    assert events[0].truncated_by_delisting
    assert events[0].truncation_close_ms == truncated_close


# ------------------------------------------------------------ coverage bars --


def test_candle_coverage_boundary_sits_exactly_on_0_90(tmp_path: Path) -> None:
    # Truncated at entry + 19d: the candle window [entry-1d, entry+19d) is 20
    # days. 18 of 20 served days is exactly 0.90 and passes; 17 is 0.85.
    outcomes = tmp_path / "outcomes"
    funding = tmp_path / "funding"
    trunc = ENTRY + 19 * MS_PER_DAY
    day_opens_pass = [ENTRY - MS_PER_DAY + i * MS_PER_DAY for i in range(18)]
    _seal_candles(outcomes, "A", ENTRY, day_opens_pass)
    _seal_funding(funding, "A", _hours(ENTRY, 456))
    on_bar = assess_window("A", "event", ENTRY, trunc, FundingTimes(funding), outcomes)
    assert on_bar.candles_30 is not None
    assert on_bar.candles_30.expected == 20
    assert on_bar.candles_30.present == 18
    assert on_bar.covered_30

    day_opens_fail = day_opens_pass[:17]
    _seal_candles(outcomes, "B", ENTRY, day_opens_fail)
    _seal_funding(funding, "B", _hours(ENTRY, 456))
    below = assess_window("B", "event", ENTRY, trunc, FundingTimes(funding), outcomes)
    assert not below.covered_30
    assert "underpowered_30d" in below.reasons


def test_funding_coverage_boundary_sits_exactly_on_0_95(tmp_path: Path) -> None:
    # Truncated at entry + 20d: 480 expected hours. 456 present is exactly
    # 0.95 and passes; 455 fails. Candles are complete throughout.
    outcomes = tmp_path / "outcomes"
    funding = tmp_path / "funding"
    trunc = ENTRY + 20 * MS_PER_DAY
    day_opens = [ENTRY - MS_PER_DAY + i * MS_PER_DAY for i in range(21)]
    _seal_candles(outcomes, "A", ENTRY, day_opens)
    _seal_funding(funding, "A", _hours(ENTRY, 456))
    on_bar = assess_window("A", "event", ENTRY, trunc, FundingTimes(funding), outcomes)
    assert on_bar.funding_30 is not None
    assert on_bar.funding_30.expected == 480
    assert on_bar.funding_30.present == 456
    assert on_bar.covered_30

    _seal_candles(outcomes, "B", ENTRY, day_opens)
    _seal_funding(funding, "B", _hours(ENTRY, 455))
    below = assess_window("B", "event", ENTRY, trunc, FundingTimes(funding), outcomes)
    assert not below.covered_30
    assert "underpowered_30d" in below.reasons


def test_a_live_window_requires_the_archive_past_the_90d_window(tmp_path: Path) -> None:
    outcomes = tmp_path / "outcomes"
    funding = tmp_path / "funding"
    day_opens = [ENTRY - MS_PER_DAY + i * MS_PER_DAY for i in range(91)]
    _seal_candles(outcomes, "A", ENTRY, day_opens)
    _seal_funding(funding, "A", _hours(ENTRY, 2159))  # last stamp == end - 1h: inside
    short = assess_window("A", "event", ENTRY, None, FundingTimes(funding), outcomes)
    assert short.archive_advanced
    _seal_candles(outcomes, "B", ENTRY, day_opens)
    _seal_funding(funding, "B", _hours(ENTRY, 2100))
    behind = assess_window("B", "event", ENTRY, None, FundingTimes(funding), outcomes)
    assert not behind.archive_advanced
    assert "funding_archive_not_advanced" in behind.reasons


# ----------------------------------------------------------- the full check --


def _happy_stores(tmp_path: Path) -> tuple[Path, Path]:
    outcomes = tmp_path / "outcomes"
    funding = tmp_path / "funding"
    day_opens = [ENTRY - MS_PER_DAY + i * MS_PER_DAY for i in range(91)]
    for coin in ("YOUNG", "OLD"):
        _seal_candles(outcomes, coin, ENTRY, day_opens)
        _seal_funding(funding, coin, _hours(ENTRY, 2160))
    return outcomes, funding


def test_run_preconditions_passes_and_hashes_the_read_surface(tmp_path: Path) -> None:
    census, plan, pairs = _cohort_fixture()
    outcomes, funding = _happy_stores(tmp_path)
    report, windows = run_preconditions(
        census,
        plan,
        pairs,
        FundingTimes(funding),
        outcomes_root=outcomes,
        latch_path=tmp_path / "stage_b_read.json",
        registered_event_n=1,
        registered_pair_n=1,
        min_n=(1, 1, 1),
    )
    assert report.events_total == 1
    assert report.controls_total == 1
    assert report.effective_n_p1 == 1
    assert report.effective_n_p3 == 1
    assert report.latch_absent
    assert set(report.module_hashes) == set(module_hashes())
    assert len(windows) == 2


def test_the_latch_spends_the_read(tmp_path: Path) -> None:
    census, plan, pairs = _cohort_fixture()
    outcomes, funding = _happy_stores(tmp_path)
    latch = tmp_path / "stage_b_read.json"
    latch.write_text("{}", encoding="utf-8")
    with pytest.raises(PreconditionFailure, match=r"already\s+spent"):
        run_preconditions(
            census,
            plan,
            pairs,
            FundingTimes(funding),
            outcomes_root=outcomes,
            latch_path=latch,
            registered_event_n=1,
            registered_pair_n=1,
            min_n=(1, 1, 1),
        )


def test_effective_n_below_the_registered_minimum_refuses_the_read(tmp_path: Path) -> None:
    census, plan, pairs = _cohort_fixture()
    outcomes, funding = _happy_stores(tmp_path)
    with pytest.raises(PreconditionFailure, match="below the registered minimum"):
        run_preconditions(
            census,
            plan,
            pairs,
            FundingTimes(funding),
            outcomes_root=outcomes,
            latch_path=tmp_path / "stage_b_read.json",
            registered_event_n=1,
            registered_pair_n=1,
            min_n=(2, 2, 2),
        )


def test_a_missing_sealed_window_stops_with_the_dated_resume_condition(tmp_path: Path) -> None:
    census, plan, pairs = _cohort_fixture()
    outcomes, funding = _happy_stores(tmp_path)
    sealed = outcomes / "OLD" / f"retro-candles-{ENTRY // MS_PER_DAY}.raw"
    sealed.unlink()
    with pytest.raises(PreconditionFailure, match="next 01:40Z daily pass"):
        run_preconditions(
            census,
            plan,
            pairs,
            FundingTimes(funding),
            outcomes_root=outcomes,
            latch_path=tmp_path / "stage_b_read.json",
            registered_event_n=1,
            registered_pair_n=1,
            min_n=(1, 1, 1),
        )
