"""The register substrate: quarantine, views, conditioning, cull, priors.

Every refusal here is produced, never asserted: the generating-sample gate
raises on an admitted ID fed through a real view; the empty operator slot
raises through the real parser on a real temp file; the cull's boundary
fixtures sit exactly on the registered 0.50 floor.
"""

from __future__ import annotations

import ast
from pathlib import Path

import pytest

from npl.absence import NO_FUNDING_ROWS, Absent
from npl.census import CensusRow
from npl.config import CONFIG
from npl.power import exact_power
from npl.register.conditioning import (
    HOURS_PER_YEAR,
    conditioning_shares,
    sidak_within,
    threshold_cells,
)
from npl.register.cull import (
    REQUIREMENT_MODE,
    CoPrimarySpec,
    RegisterVerdict,
    alpha_h,
    fire_hypothesis_section0,
    register_specs,
    run_cull,
    spec_power,
)
from npl.register.generating_sample import (
    GeneratingSampleAdmitted,
    GeneratingSampleUnavailable,
    build_generating_sample,
    event_id,
    load_generating_sample,
    refuse_generating_sample,
    write_generating_sample,
)
from npl.register.priors import (
    RegisterOperatorPriorMissing,
    UnknownHypothesis,
    assistant_priors,
    operator_prior,
    require_operator_prior,
)
from npl.register.views import (
    FreshEvent,
    h2_pairable_view,
    h3_main_dex_view,
    h4_conditioned_view,
)

CULL_FILE = Path(__file__).resolve().parents[1] / "src" / "npl" / "register" / "cull.py"

DAY_MS = 86_400_000
EPOCH = CONFIG.funding_archive_epoch_ms


def _census_row(coin: str, dex: str, listing_day: int) -> CensusRow:
    """A post-epoch census row whose resolution reproduces its listing."""
    open_ms = EPOCH + listing_day * DAY_MS
    return CensusRow(
        coin=coin,
        dex=dex,
        event_type="hip3" if dex else "vanilla",
        hyperp_source="",
        is_delisted=False,
        sz_decimals=2,
        max_leverage=10,
        state="stored",
        first_1d_open_ms=open_ms,
        last_1d_close_ms=open_ms + 200 * DAY_MS,
        candle_rows=200,
        funding_state="stored",
        first_funding_time_ms=open_ms + 3_600_000,
        funding_page_rows=500,
        recorded_at="2026-08-27T00:00:00Z",
    )


def _fresh(coin: str, dex: str = "", listing_day: int = 400) -> FreshEvent:
    open_ms = EPOCH + listing_day * DAY_MS
    return FreshEvent(
        coin=coin,
        dex=dex,
        event_type="hip3" if dex else "vanilla",
        listing_open_ms=open_ms,
        entry_ms=open_ms + 2 * DAY_MS,
    )


# ------------------------------------------------------- generating sample --


def test_build_reproduces_exactly_the_resolving_event_rows() -> None:
    rows = [_census_row("AAA", "", 10), _census_row("BBB", "", 20)]
    plan = [
        {"kind": "event", "coin": "AAA", "dex": "", "listing_open_ms": EPOCH + 10 * DAY_MS},
        {"kind": "event", "coin": "BBB", "dex": "", "listing_open_ms": EPOCH + 20 * DAY_MS},
        # A queued control window: kind=event but the resolution differs.
        {"kind": "event", "coin": "AAA", "dex": "", "listing_open_ms": EPOCH + 99 * DAY_MS},
        {"kind": "candidate", "coin": "CCC", "dex": "", "listing_open_ms": EPOCH},
    ]
    ids = build_generating_sample(rows, plan, expected_n=2)
    assert ids == {
        event_id("AAA", "", EPOCH + 10 * DAY_MS),
        event_id("BBB", "", EPOCH + 20 * DAY_MS),
    }


def test_build_refuses_a_count_that_does_not_reproduce() -> None:
    rows = [_census_row("AAA", "", 10)]
    plan = [{"kind": "event", "coin": "AAA", "dex": "", "listing_open_ms": EPOCH + 10 * DAY_MS}]
    with pytest.raises(GeneratingSampleUnavailable, match="refusing to record"):
        build_generating_sample(rows, plan, expected_n=312)


def test_write_is_write_once_and_a_mismatch_is_loud(tmp_path: Path) -> None:
    target = tmp_path / "generating_sample.json"
    write_generating_sample(frozenset({"A|x|1"}), target)
    write_generating_sample(frozenset({"A|x|1"}), target)  # idempotent re-record
    with pytest.raises(GeneratingSampleUnavailable, match="write-once"):
        write_generating_sample(frozenset({"B|x|2"}), target)


def test_load_refuses_an_absent_record(tmp_path: Path) -> None:
    with pytest.raises(GeneratingSampleUnavailable, match="does not exist"):
        load_generating_sample(tmp_path / "missing.json")


def test_load_round_trips_the_record(tmp_path: Path) -> None:
    target = tmp_path / "generating_sample.json"
    ids = frozenset({"A|x|1", "B||2"})
    write_generating_sample(ids, target)
    assert load_generating_sample(target, expected_n=2) == ids


def test_the_refusal_is_produced_on_an_admitted_generating_event() -> None:
    sample = frozenset({"OLD||100"})
    with pytest.raises(GeneratingSampleAdmitted, match="never for verdicts"):
        refuse_generating_sample(["FRESH||200", "OLD||100"], sample)
    refuse_generating_sample(["FRESH||200"], sample)  # clean ids pass silently


# ------------------------------------------------------------------- views --


def test_every_view_refuses_a_generating_event_before_any_decision() -> None:
    generating = _fresh("OLD", "", 100)
    sample = frozenset({generating.event_id()})
    events = (generating, _fresh("NEW", "", 400))
    with pytest.raises(GeneratingSampleAdmitted):
        h2_pairable_view(events, {}, sample)
    with pytest.raises(GeneratingSampleAdmitted):
        h3_main_dex_view(events, sample)
    with pytest.raises(GeneratingSampleAdmitted):
        h4_conditioned_view(events, {}, sample)


def test_h2_view_counts_reasons_and_never_guesses_a_missing_count() -> None:
    events = (_fresh("A"), _fresh("B"), _fresh("C"))
    counts = {events[0].event_id(): 3, events[1].event_id(): 0}
    result = h2_pairable_view(events, counts, frozenset())
    assert [row.event.coin for row in result.rows if row.eligible] == ["A"]
    assert result.excluded_counts() == {
        "no_control_candidate": 1,
        "candidate_count_unmeasured": 1,
    }


def test_h3_view_reads_the_dex_field_only() -> None:
    events = (_fresh("A", ""), _fresh("B", "xyz"), _fresh("C", ""))
    result = h3_main_dex_view(events, frozenset())
    assert [e.coin for e in result.eligible_events()] == ["A", "C"]
    assert result.excluded_counts() == {"hip3_builder_dex": 1}


def test_h4_view_cells_are_inclusive_at_the_threshold_boundary() -> None:
    cells = threshold_cells()
    events = (_fresh("ON"), _fresh("ABOVE"), _fresh("ABSENT"))
    on_threshold = cells[0].hourly  # exactly at -10%/yr hourly: clears
    means: dict[str, float | Absent] = {
        events[0].event_id(): on_threshold,
        events[1].event_id(): on_threshold + 1e-12,
        events[2].event_id(): NO_FUNDING_ROWS,
    }
    views = h4_conditioned_view(events, means, frozenset())
    first = views[cells[0].label]
    assert [e.coin for e in first.eligible_events()] == ["ON"]
    assert first.excluded_counts() == {
        "above_threshold": 1,
        "trailing_funding_absent_no_funding_rows": 1,
    }


# ------------------------------------------------------------ conditioning --


def test_threshold_cells_are_the_registered_grid() -> None:
    cells = threshold_cells()
    assert [c.annualized for c in cells] == [-0.10, -0.20, -0.40]
    assert cells[0].hourly == pytest.approx(-0.10 / HOURS_PER_YEAR)


def test_sidak_within_reproduces_the_h1_family_split() -> None:
    # Three cells at 0.05 reproduce the H1 alpha_adj to the digit.
    assert sidak_within(0.05, 3) == pytest.approx(CONFIG.alpha_adj)
    assert sidak_within(0.05, 1) == pytest.approx(0.05)


def test_conditioning_shares_count_absences_never_zeros() -> None:
    cells = threshold_cells()
    means: list[float | Absent] = [cells[2].hourly, cells[0].hourly + 1e-9, NO_FUNDING_ROWS]
    shares = conditioning_shares(means)
    deepest = shares[2]
    assert deepest.cleared == 1 and deepest.measured_n == 2 and deepest.absent_n == 1
    assert deepest.rate() == pytest.approx(0.5)


# -------------------------------------------------------------------- cull --


def test_alpha_h_known_answers() -> None:
    assert alpha_h(1) == pytest.approx(0.05)
    assert alpha_h(3) == pytest.approx(CONFIG.alpha_adj)
    with pytest.raises(ValueError):
        alpha_h(0)


def test_register_specs_carry_the_registered_assumptions() -> None:
    specs = {(s.hypothesis, s.name): s for s in register_specs()}
    assert specs[("H2", "E1")].p_true_governing == 0.65
    # Amendment H2-3 Change 2: the 1x floor governs, the 2x figure reports beside.
    assert specs[("H2", "E2")].p_true_governing == 0.625
    assert specs[("H2", "E2")].p_true_reported == 0.60
    assert specs[("H3", "P1")].p0 == 0.60
    assert specs[("H3", "MAG")].p_true_governing == 0.356
    assert specs[("H3", "MAG")].p_true_reported == 0.65
    h4 = [s for s in register_specs() if s.hypothesis == "H4"]
    assert len(h4) == 3 and all(s.sidak_m == 3 for s in h4)


def test_the_cull_boundary_sits_exactly_on_the_registered_floor() -> None:
    # The scan finds the first n whose power clears 0.50; the fixture pins
    # both sides of the boundary with the same deterministic computation.
    spec = CoPrimarySpec("H2", "E1", 0.5, 0.65, None, 1)
    a = alpha_h(1)
    n_exact: int | None = None
    for n in range(5, 400):
        if exact_power(n, 0.5, 0.65, a) >= 0.50:
            n_exact = n
            break
    assert n_exact is not None and n_exact > 5
    gate = fire_hypothesis_section0("H2", [spec_power(spec, n_exact, a)], a)
    assert gate.governing_power >= 0.50
    assert gate.verdict is not RegisterVerdict.BLOCKED
    # n_exact - 1 sat under the floor inside the same scan.
    gate_under = fire_hypothesis_section0("H2", [spec_power(spec, n_exact - 1, a)], a)
    assert gate_under.governing_power < 0.50
    assert gate_under.verdict is RegisterVerdict.BLOCKED
    assert not gate_under.collectors_armed


def test_the_fixed_point_reruns_at_the_larger_alpha_after_a_block() -> None:
    specs = register_specs()
    # Deadline Ns chosen so H3 and H4 block on their governing shares while
    # H2 retains power: the fixed point must land at k=1, alpha 0.05.
    deadline_n = {
        ("H2", "E1"): 150,
        ("H2", "E2"): 150,
        ("H3", "P1"): 120,
        ("H3", "MAG"): 120,
        ("H4", "le_-10pct_ann"): 40,
        ("H4", "le_-20pct_ann"): 20,
        ("H4", "le_-40pct_ann"): 10,
    }
    result = run_cull(specs, deadline_n)
    assert result.survivors == ("H2",)
    assert set(result.blocked) == {"H3", "H4"}
    assert result.k == 1
    assert result.alpha_h == pytest.approx(0.05)
    assert result.passes[0].k == 3
    assert result.passes[-1].k == 1
    # Removal is final: every pass's alpha grows.
    alphas = [p.alpha_h for p in result.passes]
    assert alphas == sorted(alphas)


def test_the_cull_refuses_a_missing_sample_size() -> None:
    specs = register_specs()
    with pytest.raises(ValueError, match="refuses"):
        run_cull(specs, {("H2", "E1"): 100})


def test_h4_requirement_is_disjunctive_and_h2_h3_conjunctive() -> None:
    assert REQUIREMENT_MODE == {"H2": "all", "H3": "all", "H4": "any"}
    a = alpha_h(3)
    weak = CoPrimarySpec("H4", "cell_a", 0.60, 0.631, None, 3)
    strong = CoPrimarySpec("H4", "cell_b", 0.60, 0.95, None, 3)
    powers = [spec_power(weak, 50, a), spec_power(strong, 50, a)]
    gate = fire_hypothesis_section0("H4", powers, a)
    # The best cell governs H4; a weak sibling cell does not block it.
    assert gate.governing_power == pytest.approx(max(p.power_governing for p in powers))


def test_go_boundary_fires_go_at_or_above_080() -> None:
    spec = CoPrimarySpec("H2", "E1", 0.5, 0.65, None, 1)
    a = alpha_h(1)
    for n in range(5, 500):
        p = exact_power(n, 0.5, 0.65, a)
        if p >= CONFIG.power_go_floor:
            gate = fire_hypothesis_section0("H2", [spec_power(spec, n, a)], a)
            assert gate.verdict is RegisterVerdict.GO
            break
    else:
        pytest.fail("no n reached the GO floor within the scan")


def test_the_cull_is_structurally_incapable_of_reaching_sealed_data() -> None:
    tree = ast.parse(CULL_FILE.read_text(encoding="utf-8"))
    imports: set[str] = set()
    calls: set[str] = set()
    strings: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom) and node.module:
            imports.add(node.module)
        elif isinstance(node, ast.Import):
            imports.update(alias.name for alias in node.names)
        elif isinstance(node, ast.Call):
            func = node.func
            calls.add(func.attr if isinstance(func, ast.Attribute) else getattr(func, "id", ""))
        elif isinstance(node, ast.Constant) and isinstance(node.value, str):
            strings.add(node.value)
    allowed = {
        "npl.config",
        "npl.power",
        "npl.register.conditioning",
        "dataclasses",
        "enum",
        "__future__",
    }
    assert imports <= allowed, f"cull.py imports outside the pure set: {imports - allowed}"
    forbidden_calls = {"open", "loads", "load", "read_text", "read_bytes", "urlopen"}
    assert not (calls & forbidden_calls), f"cull.py calls a data path: {calls & forbidden_calls}"
    leaky = {s for s in strings if "data/" in s or "outcomes" in s or ".jsonl" in s}
    assert not leaky, f"cull.py names sealed locations: {leaky}"


# ------------------------------------------------------------------- fresh --


def test_fresh_cohort_excludes_generating_events_and_pre_entry_deaths() -> None:
    from dataclasses import replace as dc_replace

    from npl.register.fresh import (
        FreshCohortMismatch,
        fresh_backfillable_events,
        fresh_funding_span,
        require_registered_pending_count,
    )

    old = _census_row("OLD", "", 10)
    young = _census_row("YOUNG", "", 500)
    # Died before its entry anchor: delisted with the last close before entry.
    stillborn = dc_replace(
        _census_row("STILLBORN", "", 510),
        is_delisted=True,
        last_1d_close_ms=EPOCH + 510 * DAY_MS + DAY_MS,
    )
    sample = frozenset({event_id("OLD", "", old.first_1d_open_ms or 0)})
    events = fresh_backfillable_events([old, young, stillborn], sample)
    assert [e.coin for e in events] == ["YOUNG"]

    require_registered_pending_count(events, EPOCH + 500 * DAY_MS, expected=1)
    with pytest.raises(FreshCohortMismatch, match="refusing to guess"):
        require_registered_pending_count(events, EPOCH + 500 * DAY_MS, expected=62)

    start, end = fresh_funding_span(events[0])
    assert start == events[0].entry_ms - 168 * 3_600_000
    assert end == events[0].entry_ms + 91 * DAY_MS


# ------------------------------------------------------------------ priors --


def _registration_with_slot(tmp_path: Path, body: str) -> Path:
    target = tmp_path / "REGISTRATION.md"
    target.write_text(body, encoding="utf-8")
    return target


def test_an_empty_slot_produces_the_structural_refusal(tmp_path: Path) -> None:
    target = _registration_with_slot(
        tmp_path,
        "## 13. Priors\n\n"
        "> Operator prior on the H2 bars clearing: _reserved, empty — only the "
        "operator fills this._\n",
    )
    assert operator_prior("H2", target) is None
    with pytest.raises(RegisterOperatorPriorMissing, match="structurally blocked"):
        require_operator_prior("H2", target)


def test_a_filled_slot_parses_with_its_label(tmp_path: Path) -> None:
    target = _registration_with_slot(
        tmp_path, "> Operator prior on the H2 bars clearing: 0.30 (independent)\n"
    )
    assert require_operator_prior("H2", target) == (0.30, "independent")


def test_a_malformed_fill_stays_empty(tmp_path: Path) -> None:
    target = _registration_with_slot(
        tmp_path, "> Operator prior on the H2 bars clearing: about a third\n"
    )
    assert operator_prior("H2", target) is None


def test_assistant_priors_are_the_recorded_register_numbers() -> None:
    assert assistant_priors("H2") == {"edge_overall": 0.25, "bars_clearing": 0.35}
    assert assistant_priors("H3") == {"bars_clearing": 0.10}
    assert assistant_priors("H4") == {"bars_clearing": 0.05}
    with pytest.raises(UnknownHypothesis):
        assistant_priors("H9")
