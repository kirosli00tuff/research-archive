"""Amendment H2-3: the fallback control, the two-look plan, the per-look latches.

Known answers to the digit; every refusal produced through the real path,
never asserted; boundary fixtures ON the registered boundary, never
comfortably inside it.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from npl.absence import NO_CANDLES, NO_CONTROL_CANDIDATE, Absent
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
from npl.coverage import coverage_by_pair_type
from npl.ledger.append_only import AppendOnlyLedger
from npl.pairtype import PAIR_TYPE_CROSS_DEX, PAIR_TYPE_SAME_DEX
from npl.power import critical_k
from npl.register.fallback import (
    candidate_census_rows,
    main_dex_candidate_rows,
    read_sealed_trail,
)
from npl.register.forward import latest_census
from npl.register.latches import (
    LOOK_LATCHES,
    REGISTERED_LOOKS,
    LookOutOfOrder,
    NoLatchForHypothesis,
    RegisterReadAlreadySpent,
    look_latch_path,
    require_look_unspent,
    write_look_latch,
)
from npl.register.pairs import (
    Look1Record,
    LookRow,
    PairNet,
    SequentialPlan,
    registered_plan,
    run_h2_look,
    same_dex_stratum,
)
from npl.register.sequential import (
    LookOrderViolation,
    futility_boundary,
    planned_n1,
    two_look_design,
    two_look_power,
)
from npl.tier import TIER_SAME_DEX_EXACT_CLASS

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


# ============================================================================
# Change 3: the two-look sequential plan. Known answers to the digit, from
# reports/stage_a_h2/ktable_amended.json (Amendment H2-4, tables 3 and 4).
# ============================================================================

A1 = CONFIG.h2_alpha_look1  # 0.02
A2 = CONFIG.h2_alpha_look2  # 0.03
E1_LOOK2_MIN_N = 84
E2_LOOK2_MIN_N = 117
LOOK1_N = 59  # the registered governing look-1 minimum N
FLOOR_BP = 36.0
CLEARS_FLOOR = CONFIG.h2_cost_floor_multiple * FLOOR_BP / 1e4  # 0.0036


def _pair_net(
    net: float,
    pair_type: str = PAIR_TYPE_SAME_DEX,
    tier: int = TIER_SAME_DEX_EXACT_CLASS,
    class_pair: str = "equity->equity",
) -> PairNet:
    return PairNet(
        event_coin="Y",
        control_coin="E",
        dex="xyz",
        cohort="backfill",
        pair_type=pair_type,
        tier=tier,
        class_pair=class_pair,
        truncated_young=False,
        truncated_elder=False,
        pair_central_cost_bp=FLOOR_BP,
        net_30=net,
        net_90=NO_CANDLES,
        young_funding_term_30=NO_CANDLES,
        young_price_term_30=NO_CANDLES,
        elder_funding_term_30=NO_CANDLES,
        elder_price_term_30=NO_CANDLES,
    )


def _cohort(n: int, e1: int, e2: int, pair_type: str = PAIR_TYPE_SAME_DEX) -> list[PairNet]:
    """n pairs of which e1 are positive and e2 (a subset) clear the 1x floor.

    Clearing the floor implies positive, so e2 <= e1 always; a fixture that
    violated it would describe a state the arithmetic cannot produce.
    """
    assert e2 <= e1 <= n
    return (
        [_pair_net(0.01, pair_type)] * e2  # clears the floor, so also positive
        + [_pair_net(CLEARS_FLOOR - 1e-9, pair_type)] * (e1 - e2)  # positive, under the floor
        + [_pair_net(-0.01, pair_type)] * (n - e1)
    )


def _plan() -> SequentialPlan:
    return registered_plan(E1_LOOK2_MIN_N, E2_LOOK2_MIN_N)


def test_the_registered_boundary_is_the_recorded_known_answer() -> None:
    """Amendment H2-4 table 3, at the look-2 minimum N: n1 59, k1 38, k2 69."""
    design = two_look_design(59, 117, A1, A2)
    assert design.k1 == 38
    assert design.k2 == 69
    assert design.alpha_spent_1 == pytest.approx(0.018172, abs=5e-7)
    assert design.alpha_spent_2 == pytest.approx(0.024025, abs=5e-7)
    assert design.alpha_spent_total() == pytest.approx(0.042197, abs=1e-6)
    # The whole point of the construction: the exact spend never exceeds the
    # registered budget, at any (n1, n2).
    assert design.alpha_spent_total() <= A1 + A2
    assert two_look_power(design, CONFIG.h2_e2_true_share) == pytest.approx(0.823731, abs=5e-7)
    assert two_look_power(design, CONFIG.h2_e1_true_share) == pytest.approx(0.932234, abs=5e-7)


def test_the_look1_boundary_spends_alpha_1_and_not_the_whole_budget() -> None:
    """The mutation this pins: spending look 2's alpha at look 1.

    k1 at alpha_1 alone is 38; at the whole 0.05 it would be 37. The gap is
    one success, which is exactly the size a boundary fixture must have.
    """
    assert two_look_design(59, 117, A1, A2).k1 == 38
    assert critical_k(59, 0.5, A1) == 38
    assert critical_k(59, 0.5, A1 + A2) == 37


def test_the_total_spend_stays_inside_the_budget_across_the_whole_table() -> None:
    for n2 in (20, 59, 84, 117, 135, 200):
        design = two_look_design(planned_n1(n2), n2, A1, A2)
        assert design.alpha_spent_total() <= A1 + A2 + 1e-12, n2


def test_a_look_that_cannot_reject_records_none_and_never_relaxes_alpha() -> None:
    """At n1 = 3 no k reaches alpha_1 = 0.02: P(X >= 3) = 0.125 > 0.02."""
    design = two_look_design(3, 4, A1, A2)
    assert design.k1 is None
    assert design.alpha_spent_1 == 0.0
    # With k1 None the whole null mass reaches look 2 — the conservative
    # accounting, not a silent widening.
    assert design.alpha_spent_2 <= A2 + 1e-12


def test_look_sizes_that_shrink_are_refused() -> None:
    with pytest.raises(LookOrderViolation, match="impossible look sizes"):
        two_look_design(50, 40, A1, A2)


def test_the_futility_boundary_is_the_recorded_known_answer() -> None:
    """Amendment H2-4 table 4: at n1 = 59, E1 f1 = 31 and E2 f1 = 27."""
    e1 = two_look_design(LOOK1_N, E1_LOOK2_MIN_N, A1, A2)
    e2 = two_look_design(LOOK1_N, E2_LOOK2_MIN_N, A1, A2)
    assert futility_boundary(e1, CONFIG.h2_e1_true_share, CONFIG) == 31
    assert futility_boundary(e2, CONFIG.h2_e2_true_share, CONFIG) == 27
    # ON the boundary, not comfortably inside it: the conditional power at
    # f1 sits under the registered floor and at f1 + 1 it does not.
    from npl.power import upper_tail

    increment = E2_LOOK2_MIN_N - LOOK1_N
    assert e2.k2 is not None
    assert upper_tail(increment, e2.k2 - 27, CONFIG.h2_e2_true_share) < 0.10
    assert upper_tail(increment, e2.k2 - 28, CONFIG.h2_e2_true_share) >= 0.10


# ------------------------------------------------- the look-aware reader ---


def test_look_1_go_fires_only_when_both_co_primaries_cross_at_the_same_look() -> None:
    """Boundary-exact: 38 of 59 crosses k1, 37 does not."""
    go = run_h2_look(_cohort(LOOK1_N, 38, 38), look=1, plan=_plan())
    assert go.e1.k1 == 38 and go.e2.k1 == 38
    assert go.e1.rejects and go.e2.rejects
    assert go.row is LookRow.GO and go.terminal

    one_short = run_h2_look(_cohort(LOOK1_N, 38, 37), look=1, plan=_plan())
    assert one_short.e1.rejects and not one_short.e2.rejects
    assert one_short.row is LookRow.CONTINUE and not one_short.terminal


def test_look_1_continue_fires_no_row_and_is_not_a_fail() -> None:
    """E1 35 and E2 30 of 59: neither crosses k1 = 38, neither is futile."""
    report = run_h2_look(_cohort(LOOK1_N, 35, 30), look=1, plan=_plan())
    assert not report.e1.rejects and not report.e2.rejects
    assert not report.e1.futility_fired and not report.e2.futility_fired
    assert report.row is LookRow.CONTINUE
    assert report.terminal is False
    assert report.look1_record == Look1Record(n1=59, e1_successes=35, e2_successes=30)


def test_look_1_futility_fires_a_terminal_fail_exactly_on_the_boundary() -> None:
    """E2's f1 is 27: 27 successes fire futility, 28 continue."""
    fires = run_h2_look(_cohort(LOOK1_N, 35, 27), look=1, plan=_plan())
    assert fires.e2.futility_boundary == 27 and fires.e2.futility_fired
    assert not fires.e1.futility_fired  # E1's own f1 is 31 and 35 clears it
    assert fires.row is LookRow.FAIL and fires.terminal

    survives = run_h2_look(_cohort(LOOK1_N, 35, 28), look=1, plan=_plan())
    assert not survives.e2.futility_fired
    assert survives.row is LookRow.CONTINUE


def test_look_1_futility_on_e1_alone_is_enough_because_both_are_required() -> None:
    report = run_h2_look(_cohort(LOOK1_N, 31, 20), look=1, plan=_plan())
    assert report.e1.futility_boundary == 31 and report.e1.futility_fired
    assert report.row is LookRow.FAIL


def test_look_2_counts_a_co_primary_that_already_crossed_at_look_1() -> None:
    """Amendment H2-4 §7: rejecting BY look 2, not only AT look 2.

    E1 crossed k1 = 38 at look 1 while E2 did not, so the trial continued.
    At look 2, E2 reaches k2 = 69. Under H2-3's literal wording E1 could
    never satisfy S1 < k1 and the design would have fired FAIL on strong
    early evidence; corrected, this is a GO.
    """
    prior = Look1Record(n1=LOOK1_N, e1_successes=38, e2_successes=30)
    go = run_h2_look(_cohort(E2_LOOK2_MIN_N, 90, 69), look=2, plan=_plan(), prior=prior)
    assert go.e1.crossed_look1 and go.e1.rejects
    assert not go.e2.crossed_look1 and go.e2.crossed_look2 and go.e2.rejects
    assert go.e1.k2 == 69 and go.e2.k2 == 69
    assert go.row is LookRow.GO and go.terminal

    one_short = run_h2_look(_cohort(E2_LOOK2_MIN_N, 90, 68), look=2, plan=_plan(), prior=prior)
    assert not one_short.e2.rejects
    assert one_short.row is LookRow.FAIL and one_short.terminal


def test_look_2_is_always_terminal_even_when_nothing_rejects() -> None:
    prior = Look1Record(n1=LOOK1_N, e1_successes=30, e2_successes=25)
    report = run_h2_look(_cohort(E2_LOOK2_MIN_N, 60, 55), look=2, plan=_plan(), prior=prior)
    assert report.row is LookRow.FAIL and report.terminal
    assert report.e1.futility_fired is False  # futility is a look-1 rule only


def test_look_2_without_look_1_and_a_shrinking_count_are_refused() -> None:
    with pytest.raises(LookOrderViolation, match="needs look 1's recorded counts"):
        run_h2_look(_cohort(100, 60, 55), look=2, plan=_plan(), prior=None)
    prior = Look1Record(n1=90, e1_successes=50, e2_successes=45)
    with pytest.raises(LookOrderViolation, match="never shrinks"):
        run_h2_look(_cohort(80, 50, 45), look=2, plan=_plan(), prior=prior)
    with pytest.raises(LookOrderViolation, match="not a registered look"):
        run_h2_look(_cohort(80, 50, 45), look=3, plan=_plan())


# ------------------------------------------------------ named secondaries ---


def test_the_same_dex_stratum_counts_same_dex_pairs_only() -> None:
    """The mutation this pins: admitting a cross_dex pair into the stratum."""
    pairs = _cohort(20, 15, 12, PAIR_TYPE_SAME_DEX) + _cohort(10, 9, 8, PAIR_TYPE_CROSS_DEX)
    stratum = same_dex_stratum(pairs)
    assert stratum["n"] == 20
    assert stratum["n_all_pairs"] == 30
    assert stratum["e1_successes"] == 15
    assert stratum["e2_successes"] == 12
    assert stratum["e1_share"] == pytest.approx(0.75)
    assert stratum["e2_share"] == pytest.approx(0.60)


def test_both_named_secondaries_ride_beside_every_look() -> None:
    pairs = _cohort(30, 20, 15, PAIR_TYPE_SAME_DEX) + _cohort(29, 15, 10, PAIR_TYPE_CROSS_DEX)
    report = run_h2_look(pairs, look=1, plan=_plan())
    assert "same_dex_stratum" in report.secondaries
    assert "economic_floor_two_times" in report.secondaries
    two_x = report.secondaries["economic_floor_two_times"]
    assert isinstance(two_x, dict) and two_x["multiple"] == 2.0
    # Every pair that clears the 1x floor here nets 0.01, well over 2 x 36 bp,
    # so the secondary agrees; the fixture that separates them is in
    # tests/test_register_a3.py::test_e2_floor_is_inclusive_and_per_pair.
    assert two_x["successes"] == 25
    assert report.e2.successes == 25


# ----------------------------------------------------- coverage by pair type ---


def test_coverage_reports_every_registered_pair_type_even_at_zero() -> None:
    rows = coverage_by_pair_type(
        [(PAIR_TYPE_SAME_DEX, True), (PAIR_TYPE_SAME_DEX, False), (PAIR_TYPE_CROSS_DEX, True)]
    )
    by_type = {r.pair_type: r for r in rows}
    assert set(by_type) == {PAIR_TYPE_SAME_DEX, PAIR_TYPE_CROSS_DEX}
    assert by_type[PAIR_TYPE_SAME_DEX].pairs == 2
    assert by_type[PAIR_TYPE_SAME_DEX].covered == 1
    assert by_type[PAIR_TYPE_SAME_DEX].underpowered == 1
    assert by_type[PAIR_TYPE_SAME_DEX].share() == pytest.approx(0.5)
    assert by_type[PAIR_TYPE_CROSS_DEX].pairs == 1
    # Zero pairs of a type is still a reported row: absent would read as
    # "no such pairs" where the truth is "none yet".
    empty = {r.pair_type: r for r in coverage_by_pair_type([])}
    assert set(empty) == {PAIR_TYPE_SAME_DEX, PAIR_TYPE_CROSS_DEX}
    assert all(r.pairs == 0 and r.share() == 0.0 for r in empty.values())
    with pytest.raises(ValueError, match="unregistered pair_type"):
        coverage_by_pair_type([("main_dex", True)])


# ------------------------------------------------------- per-look latches ---


def test_each_look_is_spent_exactly_once(tmp_path: Path) -> None:
    look1 = tmp_path / "h2_look1_latch.json"
    look2 = tmp_path / "h2_look2_latch.json"
    require_look_unspent("H2", 1, look1)  # absent: unspent
    write_look_latch("H2", 1, {"register/pairs.py": "abc"}, look1)
    with pytest.raises(RegisterReadAlreadySpent, match="look 1 is spent"):
        require_look_unspent("H2", 1, look1)
    with pytest.raises(FileExistsError):
        write_look_latch("H2", 1, {"register/pairs.py": "abc"}, look1)
    payload = json.loads(look1.read_text())
    assert payload["hypothesis"] == "H2" and payload["look"] == 1
    require_look_unspent("H2", 2, look2, previous_path=look1)


def test_look_2_cannot_run_before_look_1_is_spent(tmp_path: Path) -> None:
    """The ordering pin: look 2's counts do not exist until look 1 is spent."""
    look1 = tmp_path / "h2_look1_latch.json"
    look2 = tmp_path / "h2_look2_latch.json"
    with pytest.raises(LookOutOfOrder, match="before look 1 was spent"):
        require_look_unspent("H2", 2, look2, previous_path=look1)
    write_look_latch("H2", 1, {"m": "h"}, look1)
    require_look_unspent("H2", 2, look2, previous_path=look1)


def test_an_unregistered_look_or_hypothesis_has_no_latch() -> None:
    assert look_latch_path("H2", 1).name == "h2_look1_latch.json"
    assert look_latch_path("H2", 2).name == "h2_look2_latch.json"
    with pytest.raises(NoLatchForHypothesis, match="has no registered latch"):
        look_latch_path("H2", 3)
    with pytest.raises(NoLatchForHypothesis):
        look_latch_path("H3", 1)


def test_the_registered_looks_are_exactly_two() -> None:
    """Widening the plan to a third look is a caught change, not a config tweak."""
    assert REGISTERED_LOOKS == (1, 2)
    assert sorted(look for h, look in LOOK_LATCHES if h == "H2") == [1, 2]
    assert sorted({h for h, _ in LOOK_LATCHES}) == ["H2"]


def test_the_registered_alpha_split_sums_to_alpha_h() -> None:
    assert CONFIG.h2_alpha_look1 == 0.02
    assert CONFIG.h2_alpha_look2 == 0.03
    assert CONFIG.h2_alpha_look1 + CONFIG.h2_alpha_look2 == pytest.approx(0.05)
    assert _plan().alpha_total() == pytest.approx(0.05)
