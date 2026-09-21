"""The dark verdict machinery, on synthetic fixtures with known answers.

Includes the structural pin that verdict.py can never reach real sealed
data: its parse tree names no path, no file API, no parser, and imports only
the pure modules.
"""

from __future__ import annotations

import ast
from pathlib import Path

import pytest

from npl.absence import BLINDNESS_GATED, NO_CANDLES, Absent
from npl.census import EVENT_HIP3, EVENT_VANILLA
from npl.config import CONFIG
from npl.outcome import cost_round_trip_bp, net_short_decomposition, net_short_return
from npl.power import critical_k
from npl.verdict import (
    Cohort,
    EventNet,
    clopper_pearson_lower,
    p1_profitability,
    p2_magnitude,
    p3_contrast,
    run_verdict,
)

VERDICT_FILE = Path(__file__).resolve().parents[1] / "src" / "npl" / "verdict.py"

ALLOWED_IMPORTS = {"npl.absence", "npl.config", "npl.power", "dataclasses", "enum", "__future__"}


def _event(
    net30: float | Absent,
    control: float | Absent = NO_CANDLES,
    net90: float | Absent = BLINDNESS_GATED,
    event_type: str = EVENT_VANILLA,
    cohort: Cohort = Cohort.RETRO,
    truncated: bool = False,
) -> EventNet:
    return EventNet(
        coin="X",
        event_type=event_type,
        cohort=cohort,
        truncated_by_delisting=truncated,
        net_short_30=net30,
        net_short_90=net90,
        funding_term_30=BLINDNESS_GATED,
        price_term_30=BLINDNESS_GATED,
        control_net_short_30=control,
        control_net_short_90=BLINDNESS_GATED,
    )


# ---------------------------------------------------------------- outcome ---


def test_net_short_return_known_answer_with_sign_convention() -> None:
    # Price falls 20%, funding paid the short 1% total, cost 9 bp.
    net = net_short_return(1.0, 0.8, [0.01], 9.0)
    assert net == pytest.approx(0.20 + 0.01 - 0.0009)


def test_negative_funding_costs_the_short() -> None:
    decomposition = net_short_decomposition(1.0, 1.0, [-0.0001] * 720, 9.0)
    assert decomposition.funding_term == pytest.approx(-0.072)
    assert decomposition.net() == pytest.approx(-0.072 - 0.0009)


def test_cost_bands_are_the_registered_section5_figures() -> None:
    assert cost_round_trip_bp(EVENT_VANILLA) == 9.0
    assert cost_round_trip_bp(EVENT_HIP3) == 18.0
    assert cost_round_trip_bp(EVENT_VANILLA, band="low") == 3.0
    assert cost_round_trip_bp(EVENT_HIP3, band="high") == 36.0
    with pytest.raises(ValueError, match="unregistered"):
        cost_round_trip_bp(EVENT_VANILLA, band="median")


def test_a_zero_entry_price_is_refused() -> None:
    with pytest.raises(ValueError, match="positive"):
        net_short_return(0.0, 1.0, [], 9.0)


# ---------------------------------------------------------------- verdict ---


def test_clopper_pearson_duality_with_the_exact_test() -> None:
    # The lower bound clears p0 exactly when the exact test rejects p0.
    from npl.power import upper_tail

    n, successes = 100, 72
    bound = clopper_pearson_lower(successes, n, CONFIG.alpha_adj)
    rejects = upper_tail(n, successes, CONFIG.p1_bar) <= CONFIG.alpha_adj
    assert (bound >= CONFIG.p1_bar) == rejects


def test_p1_on_boundary_fixture() -> None:
    # The smallest success count that rejects p0=0.60 at alpha_adj, n=100.
    k_star = critical_k(100, CONFIG.p1_bar, CONFIG.alpha_adj)
    assert k_star is not None
    passing = [_event(0.5)] * k_star + [_event(-0.5)] * (100 - k_star)
    failing = [_event(0.5)] * (k_star - 1) + [_event(-0.5)] * (100 - k_star + 1)
    assert p1_profitability(passing).passes
    assert not p1_profitability(failing).passes


def test_p2_on_boundary_fixture_with_the_inclusive_threshold() -> None:
    k_star = critical_k(100, 0.5, CONFIG.alpha_adj)
    assert k_star is not None
    bar = -CONFIG.p2_net_threshold  # +0.15 net short
    # A net exactly AT +0.15 counts (the registered bound is inclusive).
    passing = [_event(bar)] * k_star + [_event(0.10)] * (100 - k_star)
    failing = [_event(bar)] * (k_star - 1) + [_event(0.10)] * (100 - k_star + 1)
    assert p2_magnitude(passing).passes
    assert not p2_magnitude(failing).passes
    # Just below the threshold does not count.
    below = [_event(bar - 1e-9)] * k_star + [_event(0.10)] * (100 - k_star)
    assert not p2_magnitude(below).passes


def test_p3_ties_count_against_the_hypothesis() -> None:
    k_star = critical_k(60, 0.5, CONFIG.alpha_adj)
    assert k_star is not None
    wins = [_event(0.2, control=0.1)] * k_star
    ties = [_event(0.1, control=0.1)] * (60 - k_star)
    assert p3_contrast(wins + ties).successes == k_star
    assert p3_contrast(wins + ties).passes
    one_less = [_event(0.2, control=0.1)] * (k_star - 1) + [_event(0.1, control=0.1)] * (
        60 - k_star + 1
    )
    assert not p3_contrast(one_less).passes


def test_an_absent_net_is_underpowered_never_a_negative() -> None:
    events = [_event(0.5)] * 10 + [_event(NO_CANDLES)] * 4
    result = p1_profitability(events)
    assert result.n == 10
    assert result.n_underpowered == 4
    # The absent events did not enter the success count as zeros.
    assert result.successes == 10


def test_an_event_without_a_control_drops_from_p3_only() -> None:
    events = [_event(0.5, control=0.1)] * 30 + [_event(0.5, control=NO_CANDLES)] * 20
    p1 = p1_profitability(events)
    p3 = p3_contrast(events)
    assert p1.n == 50
    assert p3.n == 30
    assert p3.n_underpowered == 20


def test_truncated_by_delisting_counts_travel_with_every_figure() -> None:
    events = [_event(0.5, truncated=True)] * 3 + [_event(0.5)] * 7
    assert p1_profitability(events).n_truncated_by_delisting == 3


def test_run_verdict_known_answer_all_pass_and_secondaries_report() -> None:
    events = (
        [_event(0.5, control=0.1, net90=0.4)] * 80
        + [_event(-0.2, control=0.1, net90=-0.1)] * 10
        + [_event(0.16, control=0.2, net90=0.1, event_type=EVENT_HIP3)] * 10
    )
    report = run_verdict(events)
    assert report.p1.n == 100
    assert report.all_co_primaries_pass == (
        report.p1.passes and report.p2.passes and report.p3.passes
    )
    secondaries = report.secondaries
    assert f"horizon_{CONFIG.horizon_secondary_days}d" in secondaries
    strata = secondaries["per_type_strata_30d"]
    assert isinstance(strata, dict)
    assert strata[EVENT_HIP3]["n"] == 10


# ------------------------------------------------------------- the dark pin --


def test_verdict_is_structurally_incapable_of_reaching_sealed_data() -> None:
    tree = ast.parse(VERDICT_FILE.read_text(encoding="utf-8"))
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
    assert imports <= ALLOWED_IMPORTS, f"verdict.py imports outside the pure set: {imports}"
    forbidden_calls = {"open", "loads", "load", "read_text", "read_bytes", "urlopen"}
    assert not (calls & forbidden_calls), f"verdict.py calls a data path: {calls & forbidden_calls}"
    leaky = {s for s in strings if "data/" in s or "outcomes" in s or ".jsonl" in s}
    assert not leaky, f"verdict.py names sealed locations: {leaky}"
