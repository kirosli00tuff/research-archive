"""Amendment H2-3: the fallback control, the two-look plan, the per-look latches.

Known answers to the digit; every refusal produced through the real path,
never asserted; boundary fixtures ON the registered boundary, never
comfortably inside it.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from npl.absence import NO_CONTROL_CANDIDATE, Absent
from npl.blindness import FundingRow
from npl.census import CensusRow
from npl.clock import MS_PER_DAY, MS_PER_HOUR
from npl.config import CONFIG
from npl.controls import (
    Candidate,
    PostEntryRead,
    assign_control,
    control_dex_of_row,
    pair_type_of_row,
)
from npl.ledger.append_only import AppendOnlyLedger
from npl.pairtype import PAIR_TYPE_CROSS_DEX, PAIR_TYPE_SAME_DEX
from npl.register.fallback import (
    candidate_census_rows,
    main_dex_candidate_rows,
    read_sealed_trail,
)
from npl.register.forward import latest_census

ENTRY = 1_760_000_000_000 - (1_760_000_000_000 % MS_PER_HOUR)
TRAIL_START = ENTRY - CONFIG.control_trailing_window_hours * MS_PER_HOUR


def _rows(rate: float, hours: int = 168, end_ms: int = ENTRY) -> tuple[FundingRow, ...]:
    """A fully covered trailing window at a constant rate, ending at end_ms."""
    return tuple(
        FundingRow(time_ms=end_ms - i * MS_PER_HOUR, rate=rate) for i in reversed(range(hours))
    )


def _census(coin: str, dex: str, first_open: int, last_close: int) -> CensusRow:
    return CensusRow(
        coin=coin,
        dex=dex,
        event_type="hip3" if dex else "vanilla",
        hyperp_source="",
        is_delisted=False,
        sz_decimals=2,
        max_leverage=10,
        state="stored",
        first_1d_open_ms=first_open,
        last_1d_close_ms=last_close,
        candle_rows=100,
        funding_state="stored",
        first_funding_time_ms=first_open,
        funding_page_rows=100,
        recorded_at="t",
    )


# ------------------------------------------------- Change 1: the fallback ---


def test_a_same_dex_candidate_always_wins_and_the_pair_is_tagged_same_dex(
    tmp_path: Path,
) -> None:
    """The fallback is consulted only where the same-dex set yields nothing.

    The main-dex candidate here is a *better* funding match than the
    same-dex one; the registered rule still takes the same-dex elder.
    """
    same = Candidate("SAME", ENTRY - 400 * MS_PER_DAY, _rows(5e-5))
    nearer_but_main = Candidate("MAIN", ENTRY - 400 * MS_PER_DAY, _rows(1e-5))
    result = assign_control(
        "NEW",
        "xyz",
        ENTRY,
        _rows(1e-5),
        [same],
        pairs_path=tmp_path / "p.jsonl",
        fallback_candidates=[nearer_but_main],
    )
    assert not isinstance(result, Absent)
    assert result.control_coin == "SAME"
    assert result.pair_type == PAIR_TYPE_SAME_DEX
    assert result.control_dex == "xyz"


def test_the_fallback_assigns_a_main_dex_elder_and_tags_cross_dex(tmp_path: Path) -> None:
    far = Candidate("MAIN_FAR", ENTRY - 400 * MS_PER_DAY, _rows(9e-5))
    near = Candidate("MAIN_NEAR", ENTRY - 300 * MS_PER_DAY, _rows(2e-5))
    pairs_path = tmp_path / "p.jsonl"
    result = assign_control(
        "NEW",
        "para",
        ENTRY,
        _rows(1e-5),
        [],
        pairs_path=pairs_path,
        fallback_candidates=[far, near],
    )
    assert not isinstance(result, Absent)
    assert result.control_coin == "MAIN_NEAR"
    assert result.pair_type == PAIR_TYPE_CROSS_DEX
    assert result.control_dex == ""
    assert result.dex == "para"  # the event keeps its own dex
    row = AppendOnlyLedger(pairs_path).read().rows[0]
    assert row["pair_type"] == PAIR_TYPE_CROSS_DEX and row["control_dex"] == ""


def test_an_empty_fallback_set_is_still_no_control_candidate(tmp_path: Path) -> None:
    result = assign_control(
        "NEW",
        "para",
        ENTRY,
        _rows(1e-5),
        [],
        pairs_path=tmp_path / "p.jsonl",
        fallback_candidates=[],
    )
    assert result == NO_CONTROL_CANDIDATE
    assert not (tmp_path / "p.jsonl").exists()


def test_a_fallback_candidate_under_the_coverage_bar_is_skipped_and_counted(
    tmp_path: Path,
) -> None:
    """The registered bar is 0.95 of 168 hours = 159.6, so 159 fails and 160 passes."""
    bar_hours = int(CONFIG.funding_coverage_bar * CONFIG.control_trailing_window_hours)
    thin = Candidate("THIN", ENTRY - 400 * MS_PER_DAY, _rows(1e-5, hours=bar_hours))
    thick = Candidate("THICK", ENTRY - 400 * MS_PER_DAY, _rows(9e-5, hours=bar_hours + 1))
    result = assign_control(
        "NEW",
        "para",
        ENTRY,
        _rows(1e-5),
        [],
        pairs_path=tmp_path / "p.jsonl",
        fallback_candidates=[thin, thick],
    )
    assert not isinstance(result, Absent)
    # THIN is the nearer match but sits under the bar; THICK wins by coverage.
    assert result.control_coin == "THICK"
    assert result.candidates_skipped_low_coverage == 1
    assert result.candidates_considered == 2


def test_a_post_entry_row_inside_the_fallback_path_refuses_loudly(tmp_path: Path) -> None:
    """The refusal is produced through the fallback path, not asserted."""
    late = Candidate(
        "MAIN",
        ENTRY - 400 * MS_PER_DAY,
        (*_rows(1e-5), FundingRow(ENTRY + MS_PER_HOUR, 1e-5)),
    )
    with pytest.raises(PostEntryRead, match="no row stamped after the event entry"):
        assign_control(
            "NEW",
            "para",
            ENTRY,
            _rows(1e-5),
            [],
            pairs_path=tmp_path / "p.jsonl",
            fallback_candidates=[late],
        )


def test_pre_amendment_rows_are_same_dex_by_the_rule_that_produced_them() -> None:
    old: dict[str, object] = {"event_coin": "xyz:A", "control_coin": "xyz:B", "dex": "xyz"}
    assert pair_type_of_row(old) == PAIR_TYPE_SAME_DEX
    assert control_dex_of_row(old) == "xyz"
    new: dict[str, object] = {
        "event_coin": "para:A",
        "control_coin": "B",
        "dex": "para",
        "control_dex": "",
        "pair_type": PAIR_TYPE_CROSS_DEX,
    }
    assert pair_type_of_row(new) == PAIR_TYPE_CROSS_DEX
    assert control_dex_of_row(new) == ""
    with pytest.raises(ValueError, match="unregistered pair_type"):
        pair_type_of_row({"event_coin": "X", "pair_type": "same-ish"})
    with pytest.raises(ValueError, match="carries no control_dex"):
        control_dex_of_row({"event_coin": "X", "pair_type": PAIR_TYPE_CROSS_DEX})


# ----------------------------------------------- the candidate universes ---


def test_the_candidate_filter_is_on_the_registered_180_day_boundary() -> None:
    """A candidate listed exactly 180 days before entry qualifies; 179 does not."""
    exact = ENTRY - CONFIG.control_min_age_days * MS_PER_DAY
    rows = [
        _census("ON_BOUNDARY", "", exact, ENTRY),
        _census("ONE_DAY_YOUNG", "", exact + MS_PER_DAY, ENTRY),
        _census("DEAD_BEFORE_TRAIL", "", exact, TRAIL_START - 1),
        _census("OTHER_DEX", "xyz", exact, ENTRY),
    ]
    latest = latest_census(rows)
    assert [r.coin for r in main_dex_candidate_rows(latest, ENTRY, "NEW", CONFIG)] == [
        "ON_BOUNDARY"
    ]
    assert [r.coin for r in candidate_census_rows(latest, "xyz", ENTRY, "NEW", CONFIG)] == [
        "OTHER_DEX"
    ]


def test_the_event_itself_is_never_its_own_control() -> None:
    exact = ENTRY - CONFIG.control_min_age_days * MS_PER_DAY
    latest = latest_census([_census("SELF", "", exact, ENTRY)])
    assert main_dex_candidate_rows(latest, ENTRY, "SELF", CONFIG) == []


# ------------------------------------------------ the sealed trail reader ---


def test_the_sealed_trail_is_gated_at_each_events_own_entry(tmp_path: Path) -> None:
    """One wide sealed window, read at two entries: neither sees its future."""
    payload = [
        {"coin": "MAIN", "fundingRate": "0.00001", "time": TRAIL_START + i * MS_PER_HOUR}
        for i in range(1, 400)
    ]
    directory = tmp_path / "MAIN"
    directory.mkdir()
    (directory / "trail-0-1-p0.raw").write_bytes(json.dumps(payload).encode())

    early = ENTRY - 100 * MS_PER_HOUR
    rows = read_sealed_trail("MAIN", early, early - 168 * MS_PER_HOUR, tmp_path)
    assert rows, "the sealed window served nothing"
    assert max(r.time_ms for r in rows) <= early
    assert all(not isinstance(r.rate, Absent) for r in rows)

    later = read_sealed_trail("MAIN", ENTRY, TRAIL_START, tmp_path)
    assert max(r.time_ms for r in later) <= ENTRY
    assert len(later) > len(rows)


def test_overlapping_sealed_windows_do_not_double_count_an_hour(tmp_path: Path) -> None:
    stamps = [TRAIL_START + i * MS_PER_HOUR for i in range(1, 20)]
    directory = tmp_path / "MAIN"
    directory.mkdir()
    for name in ("trail-0-1-p0.raw", "trail-0-2-p0.raw"):
        (directory / name).write_bytes(
            json.dumps(
                [{"coin": "MAIN", "fundingRate": "0.00001", "time": t} for t in stamps]
            ).encode()
        )
    rows = read_sealed_trail("MAIN", ENTRY, TRAIL_START, tmp_path)
    assert len(rows) == len(stamps)
    assert [r.time_ms for r in rows] == sorted(stamps)


def test_a_missing_trail_directory_is_an_empty_read_not_a_crash(tmp_path: Path) -> None:
    assert read_sealed_trail("NOPE", ENTRY, TRAIL_START, tmp_path) == ()
