"""Register A.3: the dark H2 pair machinery, latches, and the forward pass.

Known answers to the digit, including the sign pins on the four-leg pair
arithmetic; every refusal produced, never asserted; the dark pin holds
pairs.py structurally incapable of reaching sealed data.
"""

from __future__ import annotations

import ast
import json
from dataclasses import dataclass
from pathlib import Path

import pytest

from npl.absence import NO_CANDLES, Absent
from npl.census import CensusRow
from npl.clock import MS_PER_DAY
from npl.config import CONFIG
from npl.coverage import WindowCoverage, assess_event_coverage
from npl.http import InfoResponse
from npl.ledger.append_only import AppendOnlyLedger
from npl.pairtype import PAIR_TYPE_SAME_DEX
from npl.power import critical_k
from npl.register.forward import append_fresh_plan_row, forward_pair_pass
from npl.register.latches import (
    NoLatchForHypothesis,
    RegisterReadAlreadySpent,
    latch_path,
    require_unspent,
    write_latch,
)
from npl.register.pairs import (
    PairNet,
    e1_sign,
    e2_floor,
    h2_named_secondaries,
    pair_cost_bp,
    pair_covered,
    pair_net_decomposition,
    run_h2_verdict,
    two_times_floor_secondary,
)
from npl.venue import Venue

PAIRS_FILE = Path(__file__).resolve().parents[1] / "src" / "npl" / "register" / "pairs.py"
ALPHA_H = 0.05  # fixed by the cull (registrations/H2 Amendment H2-1)


def _pair(
    net30: float | Absent,
    net90: float | Absent = NO_CANDLES,
    dex: str = "xyz",
    cohort: str = "backfill",
    truncated_young: bool = False,
    central_bp: float = 36.0,
    pair_type: str = PAIR_TYPE_SAME_DEX,
) -> PairNet:
    return PairNet(
        event_coin="Y",
        control_coin="E",
        dex=dex,
        cohort=cohort,
        pair_type=pair_type,
        truncated_young=truncated_young,
        truncated_elder=False,
        pair_central_cost_bp=central_bp,
        net_30=net30,
        net_90=net90,
        young_funding_term_30=NO_CANDLES,
        young_price_term_30=NO_CANDLES,
        elder_funding_term_30=NO_CANDLES,
        elder_price_term_30=NO_CANDLES,
    )


# ---------------------------------------------------- four-leg arithmetic ---


def test_pair_net_known_answer_to_the_digit() -> None:
    # Young falls 30% (short earns +0.3), 720 hours at +1e-5 pay the short
    # +0.0072; elder rises 5% (long earns +0.05), same positive funding
    # COSTS the long -0.0072; both-HIP-3 cost 36 bp.
    d = pair_net_decomposition(1.0, 0.7, [1e-5] * 720, 2.0, 2.1, [1e-5] * 720, 36.0)
    assert d.young_price_term == pytest.approx(0.3)
    assert d.young_funding_term == pytest.approx(0.0072)
    assert d.elder_price_term == pytest.approx(0.05)
    assert d.elder_funding_term == pytest.approx(-0.0072)
    assert d.cost_term == pytest.approx(0.0036)
    assert d.net() == pytest.approx(0.3 + 0.0072 + 0.05 - 0.0072 - 0.0036)


def test_the_funding_sign_pins_on_both_legs() -> None:
    # Flat prices; negative funding costs the young short and PAYS the
    # elder long. Identical rates on both legs cancel exactly.
    d = pair_net_decomposition(1.0, 1.0, [-1e-4] * 720, 1.0, 1.0, [-1e-4] * 720, 18.0)
    assert d.young_funding_term == pytest.approx(-0.072)
    assert d.elder_funding_term == pytest.approx(+0.072)
    assert d.net() == pytest.approx(-0.0018)
    same = pair_net_decomposition(1.0, 1.0, [1e-4] * 720, 1.0, 1.0, [1e-4] * 720, 18.0)
    assert same.net() == pytest.approx(-0.0018)


def test_a_dead_leg_is_truncation_valued_never_zero_priced() -> None:
    with pytest.raises(ValueError, match="positive"):
        pair_net_decomposition(0.0, 1.0, [], 1.0, 1.0, [], 18.0)


def test_pair_costs_are_the_registered_h2_section5_table() -> None:
    assert pair_cost_bp("vanilla", "vanilla") == 18.0
    assert pair_cost_bp("hip3", "hip3") == 36.0
    assert pair_cost_bp("hip3", "vanilla") == 27.0
    assert pair_cost_bp("vanilla", "vanilla", band="low") == 9.0
    assert pair_cost_bp("hip3", "hip3", band="high") == 72.0
    assert pair_cost_bp("vanilla", "hip3", band="low") == 13.5
    with pytest.raises(ValueError, match="unregistered"):
        pair_cost_bp("vanilla", "vanilla", band="median")


# ------------------------------------------------------------- E1 and E2 ---


def test_e1_tie_at_zero_fails_and_boundary_counts() -> None:
    k_star = critical_k(100, 0.5, ALPHA_H)
    assert k_star is not None
    winners = [_pair(0.01)] * k_star
    zeros = [_pair(0.0)] * (100 - k_star)
    result = e1_sign(winners + zeros, ALPHA_H)
    assert result.successes == k_star and result.passes
    one_less = [_pair(0.01)] * (k_star - 1) + [_pair(0.0)] * (100 - k_star + 1)
    assert not e1_sign(one_less, ALPHA_H).passes


def test_e2_floor_is_inclusive_and_per_pair() -> None:
    """Amendment H2-3 Change 2: the floor is 1x the pair's own central cost."""
    assert CONFIG.h2_cost_floor_multiple == 1.0
    k_star = critical_k(100, 0.5, ALPHA_H)
    assert k_star is not None
    floor_36 = CONFIG.h2_cost_floor_multiple * 36.0 / 1e4  # 0.0036
    at_floor = [_pair(floor_36, central_bp=36.0)] * k_star
    under = [_pair(floor_36 - 1e-12, central_bp=36.0)] * (100 - k_star)
    result = e2_floor(at_floor + under, ALPHA_H)
    assert result.successes == k_star and result.passes
    # The floor is per pair: the same net clears a cheaper pair's floor.
    cheaper = e2_floor([_pair(0.0020, central_bp=18.0)], ALPHA_H)
    assert cheaper.successes == 1
    dearer = e2_floor([_pair(0.0020, central_bp=36.0)], ALPHA_H)
    assert dearer.successes == 0
    # The pre-amendment 2x floor survives as a named secondary, and a net
    # between 1x and 2x is exactly what the weakening admits: it clears the
    # primary and fails the secondary.
    between = [_pair(0.0050, central_bp=36.0)]
    assert e2_floor(between, ALPHA_H).successes == 1
    assert two_times_floor_secondary(between)["successes"] == 0


def test_absent_nets_are_underpowered_never_zeros() -> None:
    pairs = [_pair(0.1)] * 10 + [_pair(NO_CANDLES)] * 4
    result = e1_sign(pairs, ALPHA_H)
    assert result.n == 10 and result.n_underpowered == 4 and result.successes == 10


def test_secondaries_are_exactly_the_registered_list() -> None:
    pairs = (
        [_pair(0.1, net90=0.2, dex="xyz")] * 5
        + [_pair(-0.1, net90=-0.1, dex="", cohort="forward")] * 3
        + [_pair(0.2, truncated_young=True)] * 2
    )
    s = h2_named_secondaries(pairs)
    assert set(s) == {
        "horizon_90d",
        "per_dex_strata_30d",
        "backfill_vs_forward_30d",
        "pair_decomposition_30d",
        "truncated_subgroup_30d",
    }
    strata = s["per_dex_strata_30d"]
    assert isinstance(strata, dict) and strata["main"]["n"] == 3
    truncated = s["truncated_subgroup_30d"]
    assert isinstance(truncated, dict) and truncated["n"] == 2
    report = run_h2_verdict(pairs, ALPHA_H)
    assert report.both_pass == (report.e1.passes and report.e2.passes)


def test_pair_coverage_requires_both_legs() -> None:
    good = assess_event_coverage("A", WindowCoverage(30, 30), WindowCoverage(720, 720))
    bad = assess_event_coverage("B", WindowCoverage(30, 30), WindowCoverage(720, 600))
    assert pair_covered(good, good)
    assert not pair_covered(good, bad)
    assert not pair_covered(bad, good)


# --------------------------------------------------------------- dark pin ---


def test_the_pair_machinery_is_structurally_incapable_of_reaching_sealed_data() -> None:
    tree = ast.parse(PAIRS_FILE.read_text(encoding="utf-8"))
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
        "npl.absence",
        "npl.census",
        "npl.config",
        "npl.coverage",
        "npl.pairtype",
        "npl.power",
        "npl.register.sequential",
        "dataclasses",
        "collections.abc",
        "enum",
        "__future__",
    }
    assert imports <= allowed, f"pairs.py imports outside the pure set: {imports - allowed}"
    forbidden_calls = {"open", "loads", "load", "read_text", "read_bytes", "urlopen"}
    assert not (calls & forbidden_calls), f"pairs.py calls a data path: {calls & forbidden_calls}"
    leaky = {s for s in strings if "data/" in s or "outcomes" in s or ".jsonl" in s}
    assert not leaky, f"pairs.py names sealed locations: {leaky}"


# ---------------------------------------------------------------- latches ---


def test_only_survivors_have_latches() -> None:
    assert latch_path("H2").name == "h2_read_latch.json"
    with pytest.raises(NoLatchForHypothesis, match="only the cull's survivors"):
        latch_path("H3")
    with pytest.raises(NoLatchForHypothesis):
        latch_path("H4")


def test_the_latch_spends_the_read_exactly_once(tmp_path: Path) -> None:
    target = tmp_path / "h2_read_latch.json"
    require_unspent("H2", target)  # absent: unspent, no raise
    write_latch("H2", {"m.py": "abc"}, target)
    with pytest.raises(RegisterReadAlreadySpent, match="never a silent re-run"):
        require_unspent("H2", target)
    with pytest.raises(FileExistsError):
        write_latch("H2", {"m.py": "abc"}, target)


# ----------------------------------------------------------- forward pass ---


def _census_fixture(entry_ms: int) -> list[CensusRow]:
    def row(coin: str, dex: str, first_open: int, funding_first: int) -> CensusRow:
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
            last_1d_close_ms=entry_ms + MS_PER_DAY,
            candle_rows=100,
            funding_state="stored",
            first_funding_time_ms=funding_first,
            funding_page_rows=100,
            recorded_at="t",
        )

    old = entry_ms - 400 * MS_PER_DAY
    return [
        row("NEW", "xyz", entry_ms - 2 * MS_PER_DAY, entry_ms - 2 * MS_PER_DAY),
        row("ELDER", "xyz", old, old),
        row("TOO_YOUNG", "xyz", entry_ms - 30 * MS_PER_DAY, entry_ms - 30 * MS_PER_DAY),
    ]


@dataclass
class _ForwardClient:
    """Serves fundingHistory windows and an l2Book, no socket."""

    entry_ms: int
    calls: list[str]

    def post(self, body: dict[str, object], endpoint: str) -> InfoResponse:
        self.calls.append(str(body.get("type")))
        if body.get("type") == "fundingHistory":
            start = int(str(body["startTime"]))
            end = int(str(body.get("endTime", start)))
            # Hour-aligned stamps, as the venue serves them; a window past
            # the last hourly stamp comes back empty (end-of-feed).
            first_hour = (start // 3_600_000 + 1) * 3_600_000
            rows = [
                {"coin": body["coin"], "fundingRate": "0.00001", "time": t}
                for t in range(first_hour, end + 1, 3_600_000)
            ]
            return InfoResponse(status=200, body=json.dumps(rows).encode(), elapsed_s=0.0)
        if body.get("type") == "l2Book":
            book = {
                "coin": body["coin"],
                "time": 1,
                "levels": [
                    [{"px": "99.0", "sz": "2.0", "n": 1}],
                    [{"px": "101.0", "sz": "1.0", "n": 1}],
                ],
            }
            return InfoResponse(status=200, body=json.dumps(book).encode(), elapsed_s=0.0)
        raise AssertionError(f"unexpected request {body}")


def test_forward_pass_assigns_plans_and_snapshots(tmp_path: Path) -> None:
    from npl.clock import now_utc, utc_ms

    entry_ms = (utc_ms(now_utc()) // 60_000) * 60_000 - 5 * 60_000  # 5 min ago
    client = _ForwardClient(entry_ms, [])
    venue = Venue(client)  # type: ignore[arg-type]
    pairs_path = tmp_path / "h2_pairs.jsonl"
    plan_path = tmp_path / "fresh_plan.jsonl"
    spread_path = tmp_path / "pair_spreads.jsonl"
    funding_root = tmp_path / "funding"
    out = forward_pair_pass(
        venue,
        "NEW",
        "xyz",
        entry_ms,
        _census_fixture(entry_ms),
        pairs_path=pairs_path,
        plan_path=plan_path,
        spread_ledger_path=spread_path,
        sample=frozenset(),
        funding_root=funding_root,
    )
    assert out["state"] == "assigned" and out["control"] == "ELDER"
    assert out["candidates"] == 1  # TOO_YOUNG is not aged 180 days
    pairs = AppendOnlyLedger(pairs_path).read().rows
    assert len(pairs) == 1 and pairs[0]["control_coin"] == "ELDER"
    plan = AppendOnlyLedger(plan_path).read().rows
    assert [(r["kind"], r["coin"]) for r in plan] == [("event", "NEW"), ("control", "ELDER")]
    spreads = AppendOnlyLedger(spread_path).read().rows
    assert [r["coin"] for r in spreads] == ["NEW", "ELDER"]
    # Trail seals land in the given root, never in the real store.
    assert sorted(d.name for d in funding_root.iterdir()) == ["ELDER", "NEW"]
    # Idempotent: a second pass is a no-op on the ledger.
    again = forward_pair_pass(
        venue,
        "NEW",
        "xyz",
        entry_ms,
        _census_fixture(entry_ms),
        pairs_path=pairs_path,
        plan_path=plan_path,
        spread_ledger_path=spread_path,
        sample=frozenset(),
        funding_root=funding_root,
    )
    assert again["state"] == "already_assigned"
    assert AppendOnlyLedger(pairs_path).count() == 1


def test_forward_pass_refuses_a_generating_sample_event(tmp_path: Path) -> None:
    from npl.register.generating_sample import event_id

    entry_ms = 1_760_000_000_000 - (1_760_000_000_000 % MS_PER_DAY)
    listing = entry_ms - 2 * MS_PER_DAY
    client = _ForwardClient(entry_ms, [])
    with pytest.raises(RuntimeError, match="refused"):
        forward_pair_pass(
            Venue(client),  # type: ignore[arg-type]
            "OLD",
            "xyz",
            entry_ms,
            _census_fixture(entry_ms),
            pairs_path=tmp_path / "p.jsonl",
            plan_path=tmp_path / "f.jsonl",
            spread_ledger_path=tmp_path / "s.jsonl",
            sample=frozenset({event_id("OLD", "xyz", listing)}),
            funding_root=tmp_path / "funding",
        )


def test_fresh_plan_rows_are_idempotent(tmp_path: Path) -> None:
    plan_path = tmp_path / "fresh_plan.jsonl"
    listing = 1_760_000_000_000 - (1_760_000_000_000 % MS_PER_DAY)
    assert append_fresh_plan_row("event", "A", "xyz", "A", listing, plan_path=plan_path)
    assert not append_fresh_plan_row("event", "A", "xyz", "A", listing, plan_path=plan_path)
    rows = AppendOnlyLedger(plan_path).read().rows
    assert len(rows) == 1
    assert rows[0]["span_start_ms"] == listing + 2 * MS_PER_DAY - 168 * 3_600_000
    assert rows[0]["span_end_ms"] == listing + 2 * MS_PER_DAY + 91 * MS_PER_DAY
