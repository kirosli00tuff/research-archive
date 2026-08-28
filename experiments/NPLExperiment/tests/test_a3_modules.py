"""The A.3 collectors: seals, watcher, coverage, checkpoints, controls,
archive, spread. Fakes only; no socket opens in this suite."""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from datetime import UTC, date, datetime
from pathlib import Path

import pytest

from npl.absence import NO_CONTROL_CANDIDATE, Absent
from npl.archive import advance_funding_archive, archive_last_time, backfill_event_candles
from npl.blindness import CandleTimes, FundingRow
from npl.callstate import CallState
from npl.checkpoints import CheckpointRunner, classify_due, schedule
from npl.clock import MS_PER_DAY, MS_PER_HOUR
from npl.config import CONFIG
from npl.controls import Candidate, PostEntryRead, assign_control, trailing_mean
from npl.coverage import (
    WindowCoverage,
    assess_event_coverage,
    candle_day_coverage,
    funding_hour_coverage,
)
from npl.http import InfoResponse
from npl.ledger.append_only import AppendOnlyLedger
from npl.seals import SealViolation, seal_raw, verify_seal
from npl.spread import parse_l2_snapshot
from npl.venue import Venue
from npl.watcher import SealError, Watcher, births_path, seal_closed_day, verify_closed_day

D0 = 1_760_000_000_000 - (1_760_000_000_000 % MS_PER_DAY)


# ------------------------------------------------------------------- seals --


def test_sealed_writes_are_write_once(tmp_path: Path) -> None:
    target = seal_raw(tmp_path, "page-00000", b"abc")
    assert verify_seal(target)
    with pytest.raises(SealViolation, match="write-once"):
        seal_raw(tmp_path, "page-00000", b"other")


def test_a_tampered_seal_fails_verification(tmp_path: Path) -> None:
    target = seal_raw(tmp_path, "x", b"abc")
    target.write_bytes(b"abcd")
    assert not verify_seal(target)


# ----------------------------------------------------------------- watcher --


def _meta_body(names: list[str]) -> bytes:
    return json.dumps(
        {"universe": [{"name": n, "szDecimals": 1, "maxLeverage": 10} for n in names]}
    ).encode()


@dataclass
class _WatchClient:
    responses: dict[str, tuple[int, bytes]]
    calls: list[str] = field(default_factory=list)

    def post(self, body: dict[str, object], endpoint: str) -> InfoResponse:
        kind = str(body.get("type"))
        key = kind if kind != "meta" else f"meta:{body.get('dex', '')}"
        self.calls.append(key)
        status, payload = self.responses[key]
        return InfoResponse(status=status, body=payload, elapsed_s=0.0)


def _watch_env(tmp_path: Path, responses: dict[str, tuple[int, bytes]]) -> Watcher:
    venue = Venue(_WatchClient(responses))  # type: ignore[arg-type]
    return Watcher(
        venue, births_root=tmp_path / "births", state_root=tmp_path / "state", census=None
    )


def test_a_new_instrument_writes_a_birth_row(tmp_path: Path) -> None:
    watcher = _watch_env(
        tmp_path,
        {
            "meta:": (200, _meta_body(["BTC", "NEWCOIN"])),
            "perpDexs": (200, b"[null]"),
        },
    )
    at = datetime(2026, 8, 27, 12, 0, tzinfo=UTC)
    report = watcher.poll_once(at)
    assert report.new_births == 2  # an empty known set: everything is new once
    second = watcher.poll_once(at)
    assert second.new_births == 0  # and never twice
    rows = AppendOnlyLedger(births_path(at.date(), tmp_path / "births")).read().rows
    assert {r["coin"] for r in rows} == {"BTC", "NEWCOIN"}


def test_a_429_writes_a_loud_error_marker_and_is_not_end_of_feed(tmp_path: Path) -> None:
    watcher = _watch_env(
        tmp_path,
        {
            "meta:": (200, _meta_body(["BTC"])),
            "perpDexs": (200, b'[null,{"name":"xyz"}]'),
            "meta:xyz": (429, b"null"),
        },
    )
    at = datetime(2026, 8, 27, 12, 0, tzinfo=UTC)
    report = watcher.poll_once(at)
    assert report.dexs_failed == 1
    assert report.new_births == 1  # the main dex still recorded
    markers = AppendOnlyLedger(tmp_path / "state" / "watcher.jsonl").read().rows
    errors = [m for m in markers if m["kind"] == "error"]
    assert errors
    assert errors[0]["state"] == "rate_limited"
    assert "never read as end-of-feed" in errors[0]["note"]


def test_the_open_day_is_never_sealed(tmp_path: Path) -> None:
    with pytest.raises(SealError, match="open day"):
        seal_closed_day(date(2026, 8, 27), date(2026, 8, 27), tmp_path)


def test_sealing_yesterday_and_reading_back(tmp_path: Path) -> None:
    day = date(2026, 8, 26)
    manifest = AppendOnlyLedger(births_path(day, tmp_path))
    manifest.append({"kind": "birth", "coin": "A"})
    digest = seal_closed_day(day, date(2026, 8, 27), tmp_path)
    assert digest is not None
    assert verify_closed_day(day, date(2026, 8, 27), tmp_path)
    manifest.append({"kind": "birth", "coin": "B"})
    with pytest.raises(SealError, match="grew after sealing"):
        seal_closed_day(day, date(2026, 8, 27), tmp_path)


def test_a_closed_day_without_a_seal_refuses_to_read(tmp_path: Path) -> None:
    day = date(2026, 8, 25)
    AppendOnlyLedger(births_path(day, tmp_path)).append({"kind": "birth", "coin": "A"})
    with pytest.raises(SealError, match="missing attestation"):
        verify_closed_day(day, date(2026, 8, 27), tmp_path)


# ---------------------------------------------------------------- coverage --


def test_candle_day_coverage_unions_overlapping_windows() -> None:
    times = CandleTimes(open_ms=(D0, D0, D0 + MS_PER_DAY), close_ms=(0, 0, 0), row_count=3)
    coverage = candle_day_coverage(times, D0, D0 + 3 * MS_PER_DAY)
    assert coverage == WindowCoverage(expected=3, present=2)


def test_funding_hour_coverage_counts_distinct_hours_in_the_half_open_window() -> None:
    rows = (
        FundingRow(D0 + 1, 0.0),  # inside (D0, end]
        FundingRow(D0 + 1 + MS_PER_HOUR, 0.0),
        FundingRow(D0 + 1 + MS_PER_HOUR, 0.0),  # duplicate hour
        FundingRow(D0, 0.0),  # exactly at start: outside the half-open window
    )
    coverage = funding_hour_coverage(rows, D0, D0 + 3 * MS_PER_HOUR)
    assert coverage == WindowCoverage(expected=3, present=2)


def test_coverage_bars_sit_exactly_on_the_registered_thresholds() -> None:
    candles_at_bar = WindowCoverage(expected=100, present=90)
    funding_at_bar = WindowCoverage(expected=100, present=95)
    assert assess_event_coverage("X", candles_at_bar, funding_at_bar).meets_bars
    below = assess_event_coverage("X", WindowCoverage(100, 89), funding_at_bar)
    assert not below.meets_bars
    assert below.label == "underpowered"


# -------------------------------------------------------------- checkpoints --


def test_the_schedule_is_the_registered_offsets() -> None:
    assert CONFIG.checkpoint_offsets_days == (2, 32, 92)
    days = schedule(date(2026, 8, 1))
    assert days == (date(2026, 8, 3), date(2026, 9, 2), date(2026, 11, 1))


def test_classify_due_boundaries() -> None:
    listing = date(2026, 8, 1)
    # +2 checkpoint due 08-03, catch-up closes 08-08 (5 days).
    due, expired, upcoming = classify_due("C", "", listing, date(2026, 8, 3), set())
    assert [d.offset_days for d in due] == [2]
    due, expired, upcoming = classify_due("C", "", listing, date(2026, 8, 8), set())
    assert [d.offset_days for d in due] == [2]  # the last catch-up day still fetches
    due, expired, upcoming = classify_due("C", "", listing, date(2026, 8, 9), set())
    assert [d.offset_days for d in expired] == [2]
    assert [d.offset_days for d in upcoming] == [32, 92]


@dataclass
class _CheckpointClient:
    candle_status: int = 200
    funding_status: int = 200

    def post(self, body: dict[str, object], endpoint: str) -> InfoResponse:
        if body.get("type") == "candleSnapshot":
            return InfoResponse(self.candle_status, b'[{"t": 1, "T": 2}]', 0.0)
        return InfoResponse(self.funding_status, b'[{"time": 1}]', 0.0)


def test_the_runner_seals_both_payloads_and_records_the_attempt(tmp_path: Path) -> None:
    runner = CheckpointRunner(
        Venue(_CheckpointClient()),  # type: ignore[arg-type]
        outcomes_root=tmp_path / "outcomes",
        funding_root=tmp_path / "funding",
        state_root=tmp_path / "state",
    )
    due, _, _ = classify_due("COIN", "", date(2026, 8, 1), date(2026, 8, 3), set())
    state = runner.run_one(due[0])
    assert state is CallState.STORED
    assert (tmp_path / "outcomes" / "COIN" / "cp2-candles-2026-08-03.raw").exists()
    assert (tmp_path / "funding" / "COIN" / "cp2-funding-2026-08-03.raw").exists()
    assert ("COIN", 2) in runner.attempted()


def test_a_rate_limited_checkpoint_is_recorded_not_stored(tmp_path: Path) -> None:
    runner = CheckpointRunner(
        Venue(_CheckpointClient(candle_status=429)),  # type: ignore[arg-type]
        outcomes_root=tmp_path / "outcomes",
        funding_root=tmp_path / "funding",
        state_root=tmp_path / "state",
    )
    due, _, _ = classify_due("COIN", "", date(2026, 8, 1), date(2026, 8, 3), set())
    assert runner.run_one(due[0]) is CallState.RATE_LIMITED
    assert ("COIN", 2) not in runner.attempted()


def test_an_expired_checkpoint_writes_the_loud_record(tmp_path: Path) -> None:
    runner = CheckpointRunner(
        Venue(_CheckpointClient()),  # type: ignore[arg-type]
        outcomes_root=tmp_path / "o",
        funding_root=tmp_path / "f",
        state_root=tmp_path / "state",
    )
    _, expired, _ = classify_due("COIN", "", date(2026, 1, 1), date(2026, 8, 3), set())
    runner.record_expired(expired[0])
    rows = AppendOnlyLedger(tmp_path / "state" / "checkpoints.jsonl").read().rows
    assert rows[0]["kind"] == "expired"
    assert rows[0]["state"] == "expired"
    assert "permanent" in rows[0]["note"]


# ----------------------------------------------------------------- controls --

ENTRY = D0 + 2 * MS_PER_DAY


def _hours(n: int, end: int = ENTRY, rate: float = 0.0001) -> tuple[FundingRow, ...]:
    return tuple(FundingRow(end - i * MS_PER_HOUR, rate) for i in range(n))


def test_a_post_entry_row_inside_matching_raises_loudly() -> None:
    rows = (*_hours(10), FundingRow(ENTRY + 1, 0.0001))
    with pytest.raises(PostEntryRead, match="after the event entry"):
        trailing_mean(rows, ENTRY)


def test_trailing_coverage_exactly_at_the_bar_is_readable() -> None:
    hours_at_bar = int(CONFIG.control_trailing_window_hours * CONFIG.funding_coverage_bar)
    below = trailing_mean(_hours(hours_at_bar), ENTRY)
    assert isinstance(below, Absent) == (
        hours_at_bar / CONFIG.control_trailing_window_hours < CONFIG.funding_coverage_bar
    )
    ok = trailing_mean(_hours(hours_at_bar + 1), ENTRY)
    assert not isinstance(ok, Absent)


def test_assignment_picks_the_nearest_signed_mean_with_registered_tie_breaks(
    tmp_path: Path,
) -> None:
    # Exact-tie fixture: rates chosen exactly representable in binary floats,
    # so the two nearest candidates tie to the bit and the tie-break decides.
    event_rows = _hours(40, rate=0.0)
    near = Candidate("NEAR", D0 - 400 * MS_PER_DAY, _hours(168, rate=+1.0))
    far = Candidate("FAR", D0 - 500 * MS_PER_DAY, _hours(168, rate=+4.0))
    tie_old = Candidate("OLD", D0 - 600 * MS_PER_DAY, _hours(168, rate=-1.0))
    # |near - event| = 1.0 == |tie_old - event| exactly; the older listing wins.
    pairs = tmp_path / "pairs.jsonl"
    assignment = assign_control(
        "EVT", "", ENTRY, event_rows, [near, far, tie_old], pairs_path=pairs
    )
    assert not isinstance(assignment, Absent)
    assert assignment.control_coin == "OLD"
    assert assignment.candidates_considered == 3
    recorded = AppendOnlyLedger(pairs).read().rows
    assert recorded[0]["event_coin"] == "EVT"
    assert recorded[0]["control_coin"] == "OLD"


def test_low_coverage_candidates_are_skipped_and_counted(tmp_path: Path) -> None:
    event_rows = _hours(40, rate=-0.0002)
    thin = Candidate("THIN", D0 - 400 * MS_PER_DAY, _hours(10, rate=-0.0002))
    assignment = assign_control(
        "EVT", "", ENTRY, event_rows, [thin], pairs_path=tmp_path / "pairs.jsonl"
    )
    assert assignment == NO_CONTROL_CANDIDATE


# ------------------------------------------------------------------ archive --


def _funding_page(start: int, rows: int) -> bytes:
    return json.dumps(
        [
            {"coin": "X", "fundingRate": "0.0000125", "time": start + i * MS_PER_HOUR}
            for i in range(rows)
        ]
    ).encode()


@dataclass
class _ArchiveClient:
    pages: list[tuple[int, bytes]]
    served: int = 0

    def post(self, body: dict[str, object], endpoint: str) -> InfoResponse:
        if body.get("type") == "candleSnapshot":
            return InfoResponse(200, b'[{"t": 1, "T": 2}]', 0.0)
        if self.served >= len(self.pages):
            return InfoResponse(200, b"[]", 0.0)
        status, payload = self.pages[self.served]
        self.served += 1
        return InfoResponse(status, payload, 0.0)


def test_the_archive_pages_forward_and_resumes_from_its_own_seals(tmp_path: Path) -> None:
    client = _ArchiveClient(
        [(200, _funding_page(D0, 500)), (200, _funding_page(D0 + 500 * MS_PER_HOUR, 100))]
    )
    venue = Venue(client)  # type: ignore[arg-type]
    root = tmp_path / "funding"
    first = advance_funding_archive(venue, "X", D0, D0 + 700 * MS_PER_HOUR, 10, root)
    assert first.pages_fetched == 2
    assert first.caught_up  # the third request served empty
    assert archive_last_time("X", root) == D0 + 599 * MS_PER_HOUR
    # A later advance resumes from the sealed cursor and fetches nothing new.
    again = advance_funding_archive(venue, "X", D0, D0 + 700 * MS_PER_HOUR, 10, root)
    assert again.pages_fetched == 0
    assert again.caught_up


def test_a_refusal_mid_archive_is_recorded_and_keeps_prior_pages(tmp_path: Path) -> None:
    client = _ArchiveClient([(200, _funding_page(D0, 500)), (429, b"null")])
    venue = Venue(client)  # type: ignore[arg-type]
    root = tmp_path / "funding"
    advance = advance_funding_archive(venue, "X", D0, D0 + 9000 * MS_PER_HOUR, 10, root)
    assert advance.pages_fetched == 1
    assert not advance.caught_up
    assert advance.terminal_state == "rate_limited"
    assert archive_last_time("X", root) == D0 + 499 * MS_PER_HOUR


def test_backfill_event_candles_seals_once_and_is_idempotent(tmp_path: Path) -> None:
    venue = Venue(_ArchiveClient([]))  # type: ignore[arg-type]
    root = tmp_path / "outcomes"
    assert backfill_event_candles(venue, "X", D0, root) is CallState.STORED
    assert backfill_event_candles(venue, "X", D0, root) is CallState.STORED
    sealed = list((root / "X").glob("retro-candles-*.raw"))
    assert len(sealed) == 1


# ------------------------------------------------------------------- spread --


def test_parse_l2_snapshot_known_answer() -> None:
    body = json.dumps(
        {
            "coin": "X",
            "time": 1,
            "levels": [
                [{"px": "99.0", "sz": "2.0", "n": 1}, {"px": "98.0", "sz": "3.0", "n": 1}],
                [{"px": "101.0", "sz": "1.0", "n": 1}, {"px": "102.0", "sz": "4.0", "n": 1}],
            ],
        }
    ).encode()
    snapshot = parse_l2_snapshot("X", ENTRY, body, "t")
    assert snapshot.bid_px == 99.0
    assert snapshot.ask_px == 101.0
    assert snapshot.touch_spread_bp == pytest.approx((101 - 99) / 100 * 1e4)
    assert snapshot.bid_depth5_base == pytest.approx(5.0)
    assert snapshot.ask_depth5_notional == pytest.approx(1 * 101.0 + 4 * 102.0)


def test_an_empty_book_side_is_a_refusal_not_a_spread() -> None:
    body = json.dumps({"coin": "X", "time": 1, "levels": [[], [{"px": "1", "sz": "1"}]]}).encode()
    with pytest.raises(ValueError, match="refusal"):
        parse_l2_snapshot("X", ENTRY, body, "t")


def test_record_leg_spread_writes_a_descriptive_row_and_a_loud_error(tmp_path: Path) -> None:
    from npl.spread import record_leg_spread

    book = json.dumps(
        {
            "coin": "Y",
            "time": 1,
            "levels": [
                [{"px": "99.0", "sz": "2.0", "n": 1}],
                [{"px": "101.0", "sz": "1.0", "n": 1}],
            ],
        }
    ).encode()

    @dataclass
    class _LegClient:
        status: int
        payload: bytes

        def post(self, body: dict[str, object], endpoint: str) -> InfoResponse:
            return InfoResponse(status=self.status, body=self.payload, elapsed_s=0.0)

    ledger_path = tmp_path / "pair_spreads.jsonl"
    venue = Venue(_LegClient(200, book))  # type: ignore[arg-type]
    state = record_leg_spread(
        venue, "Y", hypothesis="H2", role="control", event_coin="X", ledger_path=ledger_path
    )
    assert state is CallState.STORED
    refusing = Venue(_LegClient(429, b"null"))  # type: ignore[arg-type]
    state = record_leg_spread(
        refusing, "Y", hypothesis="H2", role="control", event_coin="X", ledger_path=ledger_path
    )
    assert state is CallState.RATE_LIMITED
    rows = AppendOnlyLedger(ledger_path).read().rows
    assert [r["kind"] for r in rows] == ["leg_spread", "error"]
    assert rows[0]["touch_spread_bp"] == pytest.approx((101 - 99) / 100 * 1e4)
    assert rows[1]["state"] == "rate_limited"
