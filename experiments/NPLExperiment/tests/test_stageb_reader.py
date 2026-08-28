"""The Stage B known-answer gate, the latch, and the Amendment 3 table.

Every fixture answer here is computed by hand from Section 4 and the
Amendment 3 reading rules and asserted to the digit; a flipped funding
sign, a moved entry anchor, or a bypassed latch goes red here. The sealed
stores are synthetic tmp files with known values.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest

from npl.absence import AbsenceReason, Absent
from npl.census import CensusRow
from npl.clock import MS_PER_DAY, MS_PER_HOUR
from npl.config import CONFIG
from npl.seals import seal_raw
from npl.stageb.cli import (
    B1_SURFACE,
    ReadAlreadySpent,
    ReadAuthorizationVoided,
    execute_read,
    fire_row,
    verify_read_surface,
)
from npl.stageb.preconditions import (
    FundingTimes,
    module_hashes,
    reconstruct_cohort,
    run_preconditions,
)
from npl.stageb.reader import FundingRates, Valued, read_cohort, value_window
from npl.verdict import BinomialTest, run_verdict

LISTING = CONFIG.funding_archive_epoch_ms + 400 * MS_PER_DAY
ENTRY = LISTING + 2 * MS_PER_DAY
AFTER_MATURITY = ENTRY + 91 * MS_PER_DAY


def _hours(start_exclusive_ms: int, count: int) -> list[int]:
    return [start_exclusive_ms + (i + 1) * MS_PER_HOUR for i in range(count)]


def _rates(times: list[int], rate: float) -> tuple[tuple[int, float], ...]:
    return tuple((t, rate) for t in times)


def _closes(entry_close: float, per_day: dict[int, float]) -> dict[int, float]:
    """Candle open t -> close: entry candle plus named day offsets from entry."""
    out = {ENTRY - MS_PER_DAY: entry_close}
    for day, close in per_day.items():
        out[ENTRY + day * MS_PER_DAY] = close
    return out


# ------------------------------------------------------- value_window pins --


def test_known_answer_price_drop_with_positive_funding() -> None:
    # Price 1.0 -> 0.7 over 30d; 720 hourly rates at +1e-5 pay the short.
    closes = _closes(1.0, dict.fromkeys(range(29), 1.0) | {29: 0.7})
    valued = value_window(closes, _rates(_hours(ENTRY, 720), 1e-5), ENTRY, 30, None)
    assert isinstance(valued, Valued)
    assert valued.price_term == pytest.approx(0.3)
    assert valued.funding_term == pytest.approx(0.0072)
    assert valued.funding_rows_n == 720
    assert valued.exit_open_ms == ENTRY + 29 * MS_PER_DAY
    net_central = valued.price_term + valued.funding_term - 9.0 / 1e4
    assert net_central == pytest.approx(0.3 + 0.0072 - 0.0009)


def test_negative_funding_costs_the_short_the_sign_pin() -> None:
    # Flat price, 720 hourly rates at -1e-4: the A.3 fixture answer -0.0729
    # reproduced through the sealed path. A flipped sign goes red here.
    closes = _closes(1.0, dict.fromkeys(range(30), 1.0))
    valued = value_window(closes, _rates(_hours(ENTRY, 720), -1e-4), ENTRY, 30, None)
    assert isinstance(valued, Valued)
    assert valued.price_term == pytest.approx(0.0)
    assert valued.funding_term == pytest.approx(-0.072)
    assert valued.price_term + valued.funding_term - 9.0 / 1e4 == pytest.approx(-0.0729)


def test_truncated_event_is_valued_at_its_last_served_close() -> None:
    # Delisted after day 9: last served close 0.5; funding stops at truncation.
    trunc = ENTRY + 10 * MS_PER_DAY
    closes = _closes(1.0, dict.fromkeys(range(9), 1.0) | {9: 0.5})
    valued = value_window(closes, _rates(_hours(ENTRY, 720), 1e-5), ENTRY, 30, trunc)
    assert isinstance(valued, Valued)
    assert valued.exit_open_ms == ENTRY + 9 * MS_PER_DAY
    assert valued.price_term == pytest.approx(0.5)
    assert valued.funding_rows_n == 240  # hours in (entry, entry+10d] only
    assert valued.funding_term == pytest.approx(0.0024)


def test_exit_falls_back_to_the_last_served_close_before_the_horizon() -> None:
    # The exact horizon candle (day 29) is missing; day 28 serves the exit.
    closes = _closes(1.0, dict.fromkeys(range(28), 1.0) | {28: 0.8})
    valued = value_window(closes, _rates(_hours(ENTRY, 720), 0.0), ENTRY, 30, None)
    assert isinstance(valued, Valued)
    assert valued.exit_open_ms == ENTRY + 28 * MS_PER_DAY
    assert valued.price_term == pytest.approx(0.2)


def test_a_missing_entry_candle_is_a_recorded_absence() -> None:
    closes = {ENTRY + i * MS_PER_DAY: 1.0 for i in range(30)}  # no entry candle
    valued = value_window(closes, _rates(_hours(ENTRY, 720), 1e-5), ENTRY, 30, None)
    assert isinstance(valued, Absent)
    assert valued.reason is AbsenceReason.NO_CANDLES


# ------------------------------------------------------ the sealed cohort --


def _census_row(
    coin: str,
    first_open: int,
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
        first_funding_time_ms=first_open,
        funding_page_rows=rows,
        recorded_at="2026-08-27T00:00:00Z",
    )


def _seal_candles(root: Path, coin: str, closes: dict[int, float]) -> None:
    rows = [
        {
            "t": t,
            "T": t + MS_PER_DAY - 1,
            "s": coin,
            "i": "1d",
            "o": "1.0",
            "c": str(close),
            "h": "1.0",
            "l": "1.0",
            "v": "1.0",
            "n": 1,
        }
        for t, close in sorted(closes.items())
    ]
    seal_raw(root / coin, f"retro-candles-{ENTRY // MS_PER_DAY}", json.dumps(rows).encode())


def _seal_funding(root: Path, coin: str, times: list[int], rate: float) -> None:
    rows = [{"coin": coin, "fundingRate": str(rate), "time": t} for t in times]
    seal_raw(root / coin, "page-00000", json.dumps(rows).encode())


def _sealed_cohort(
    tmp_path: Path,
) -> tuple[list[CensusRow], list[dict[str, Any]], list[dict[str, Any]], Path, Path]:
    """YOUNG (event, 1.0 -> 0.7 at 30d, +1e-5 funding) against OLD (control,
    2.0 -> 1.9 at 30d, -1e-5 funding), both fully served over 90 days."""
    outcomes = tmp_path / "outcomes"
    funding = tmp_path / "funding"
    ninety = dict.fromkeys(range(90), 1.0) | {29: 0.7, 89: 0.6}
    _seal_candles(outcomes, "YOUNG", _closes(1.0, ninety))
    _seal_funding(funding, "YOUNG", _hours(ENTRY, 2160), 1e-5)
    control_days = dict.fromkeys(range(90), 2.0) | {29: 1.9, 89: 1.8}
    _seal_candles(outcomes, "OLD", _closes(2.0, control_days))
    _seal_funding(funding, "OLD", _hours(ENTRY, 2160), -1e-5)
    census = [
        _census_row("YOUNG", LISTING, last_close=LISTING + 95 * MS_PER_DAY, rows=95),
        _census_row(
            "OLD",
            LISTING - 200 * MS_PER_DAY,
            last_close=LISTING + 95 * MS_PER_DAY,
            rows=295,
        ),
    ]
    plan: list[dict[str, Any]] = [
        {"kind": "event", "coin": "YOUNG", "dex": "", "listing_open_ms": LISTING},
        {"kind": "event", "coin": "OLD", "dex": "", "listing_open_ms": ENTRY - 2 * MS_PER_DAY},
    ]
    pairs: list[dict[str, Any]] = [
        {"event_coin": "YOUNG", "control_coin": "OLD", "dex": "", "entry_ms": ENTRY}
    ]
    return census, plan, pairs, outcomes, funding


def test_read_cohort_reproduces_the_hand_computed_answers(tmp_path: Path) -> None:
    census, plan, pairs, outcomes, funding = _sealed_cohort(tmp_path)
    report, windows = run_preconditions(
        census,
        plan,
        pairs,
        FundingTimes(funding),
        outcomes_root=outcomes,
        latch_path=tmp_path / "latch.json",
        registered_event_n=1,
        registered_pair_n=1,
        min_n=(1, 1, 1),
    )
    assert report.events_covered_30 == 1
    events, controls = reconstruct_cohort(census, plan, pairs)
    read = read_cohort(events, controls, windows, AFTER_MATURITY, outcomes, FundingRates(funding))
    assert read.pending_30 == 0 and read.pending_90 == 0
    assert read.funding_rows_30_total == 720

    (event,) = read.events_central
    assert event.net_short_30 == pytest.approx(0.3 + 0.0072 - 0.0009)
    assert event.net_short_90 == pytest.approx(0.4 + 0.0216 - 0.0009)
    assert event.funding_term_30 == pytest.approx(0.0072)
    assert event.price_term_30 == pytest.approx(0.3)
    assert event.control_net_short_30 == pytest.approx(0.05 - 0.0072 - 0.0009)

    (low,) = read.events_low
    (high,) = read.events_high
    assert low.net_short_30 == pytest.approx(0.3 + 0.0072 - 0.0003)
    assert high.net_short_30 == pytest.approx(0.3 + 0.0072 - 0.0018)

    assert read.paired_h8_n == 1
    assert read.paired_h8_mean_funding_diff == pytest.approx(0.0144)
    assert read.paired_h8_mean_price_diff == pytest.approx(0.25)

    verdict = run_verdict(list(read.events_central))
    assert verdict.p3.n == 1
    assert verdict.p3.successes == 1  # young net > control net


# ------------------------------------------------------------- the table --


def _test_stat(passes: bool) -> BinomialTest:
    return BinomialTest(
        n=100,
        successes=60,
        statistic=0.5,
        passes=passes,
        n_underpowered=0,
        n_truncated_by_delisting=0,
    )


def test_the_amendment_3_table_is_mechanical() -> None:
    go = fire_row(_test_stat(True), _test_stat(True), _test_stat(True))
    partial = fire_row(_test_stat(True), _test_stat(True), _test_stat(False))
    fail_p1 = fire_row(_test_stat(False), _test_stat(True), _test_stat(True))
    fail_p2 = fire_row(_test_stat(True), _test_stat(False), _test_stat(True))
    assert go == "GO"
    assert partial == "PARTIAL_DRIFT"
    assert fail_p1 == "FAIL"
    assert fail_p2 == "FAIL"


# ------------------------------------------------------- the latch and hash --


def _write_hashes(tmp_path: Path) -> Path:
    path = tmp_path / "hashes_b1.json"
    path.write_text(
        json.dumps(module_hashes(B1_SURFACE), indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return path


def test_the_read_spends_the_latch_and_a_second_read_is_refused(tmp_path: Path) -> None:
    census, plan, pairs, outcomes, funding = _sealed_cohort(tmp_path)
    latch = tmp_path / "stage_b_read.json"
    hashes = _write_hashes(tmp_path)
    payload = execute_read(
        census,
        plan,
        pairs,
        FundingTimes(funding),
        FundingRates(funding),
        outcomes_root=outcomes,
        latch_path=latch,
        hashes_path=hashes,
        now_ms=AFTER_MATURITY,
        registered_event_n=1,
        registered_pair_n=1,
        min_n=(1, 1, 1),
    )
    assert latch.exists()
    assert payload["row_fired"] in {"GO", "PARTIAL_DRIFT", "FAIL"}
    assert payload["preconditions"]["events_total"] == 1
    latched = json.loads(latch.read_text(encoding="utf-8"))
    assert set(latched["module_hashes"]) == set(module_hashes(B1_SURFACE))
    with pytest.raises(ReadAlreadySpent, match="spent"):
        execute_read(
            census,
            plan,
            pairs,
            FundingTimes(funding),
            FundingRates(funding),
            outcomes_root=outcomes,
            latch_path=latch,
            hashes_path=hashes,
            now_ms=AFTER_MATURITY,
            registered_event_n=1,
            registered_pair_n=1,
            min_n=(1, 1, 1),
        )


def test_a_pre_existing_latch_refuses_before_any_work(tmp_path: Path) -> None:
    census, plan, pairs, outcomes, funding = _sealed_cohort(tmp_path)
    latch = tmp_path / "stage_b_read.json"
    latch.write_text("{}", encoding="utf-8")
    with pytest.raises(ReadAlreadySpent, match="spent"):
        execute_read(
            census,
            plan,
            pairs,
            FundingTimes(funding),
            FundingRates(funding),
            outcomes_root=outcomes,
            latch_path=latch,
            hashes_path=_write_hashes(tmp_path),
            now_ms=AFTER_MATURITY,
            registered_event_n=1,
            registered_pair_n=1,
            min_n=(1, 1, 1),
        )


def test_a_hash_diff_voids_the_read_authorization(tmp_path: Path) -> None:
    recorded = module_hashes(B1_SURFACE)
    tampered = dict(recorded)
    tampered["verdict.py"] = "0" * 64
    path = tmp_path / "hashes_b1.json"
    path.write_text(json.dumps(tampered, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    with pytest.raises(ReadAuthorizationVoided, match="void"):
        verify_read_surface(path)


def test_missing_recorded_hashes_void_the_read_authorization(tmp_path: Path) -> None:
    with pytest.raises(ReadAuthorizationVoided, match="does not exist"):
        verify_read_surface(tmp_path / "absent.json")
