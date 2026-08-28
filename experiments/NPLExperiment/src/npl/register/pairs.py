"""H2 pair verdict machinery, built dark. H2's Stage B calls it exactly once.

Pure arithmetic over in-memory records, exactly the H1 verdict.py shape: no
path, no file API, no parser, imports only the pure modules — pinned against
its parse tree by test. Until H2's registered Stage B read, the only inputs
this module ever sees are synthetic fixtures with known answers.

The four-leg sign conventions, registered (registrations/H2 Section 4) and
pinned by known-answer tests:

    pair_net(H) = young_leg_net_short + elder_leg_net_long
    young short: -price_return(young) + sum(funding_young) - cost_young
    elder long:  +price_return(elder) - sum(funding_elder) - cost_elder

A positive hourly rate pays the young short and costs the elder long. Tie
rules, registered: a pair net exactly at zero fails E1; a pair net exactly
at the E2 floor passes E2 (inclusive).
"""

from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass

from npl.absence import Absent
from npl.census import EVENT_HIP3
from npl.config import CONFIG, Config
from npl.coverage import EventCoverage
from npl.power import upper_tail


@dataclass(frozen=True, slots=True)
class PairDecomposition:
    """The pair's H8-style decomposition: each leg's price and funding terms."""

    young_price_term: float
    young_funding_term: float
    elder_price_term: float
    elder_funding_term: float
    cost_term: float

    def net(self) -> float:
        return (
            self.young_price_term
            + self.young_funding_term
            + self.elder_price_term
            + self.elder_funding_term
            - self.cost_term
        )


def leg_cost_central_bp(leg_class: str, cfg: Config = CONFIG) -> float:
    """One leg's central round trip by venue class (H1 Section 5 figures)."""
    return (cfg.hip3_round_trip_bp if leg_class == EVENT_HIP3 else cfg.vanilla_round_trip_bp)[1]


def pair_cost_bp(
    young_class: str, elder_class: str, cfg: Config = CONFIG, band: str = "central"
) -> float:
    """The registered pair cost: sum of the legs' centrals; bands half/double.

    registrations/H2 Section 5: both-vanilla 18 (9, 18, 36), both-HIP-3 36
    (18, 36, 72), mixed 27 (13.5, 27, 54).
    """
    central = leg_cost_central_bp(young_class, cfg) + leg_cost_central_bp(elder_class, cfg)
    by_band = {"low": central / 2.0, "central": central, "high": central * 2.0}
    if band not in by_band:
        raise ValueError(f"unregistered pair cost band {band!r}")
    return by_band[band]


def pair_net_decomposition(
    young_entry_close: float,
    young_exit_close: float,
    young_hourly_rates: Iterable[float],
    elder_entry_close: float,
    elder_exit_close: float,
    elder_hourly_rates: Iterable[float],
    pair_round_trip_bp: float,
) -> PairDecomposition:
    """The registered four-leg arithmetic, constant notional per leg."""
    for name, price in (
        ("young entry", young_entry_close),
        ("elder entry", elder_entry_close),
    ):
        if price <= 0.0:
            raise ValueError(f"{name} close must be positive, got {price!r}")
    if young_exit_close < 0.0 or elder_exit_close < 0.0:
        raise ValueError("exit closes must be non-negative; truncation uses last served close")
    young_return = young_exit_close / young_entry_close - 1.0
    elder_return = elder_exit_close / elder_entry_close - 1.0
    return PairDecomposition(
        young_price_term=-young_return,
        young_funding_term=float(sum(young_hourly_rates)),
        elder_price_term=+elder_return,
        elder_funding_term=-float(sum(elder_hourly_rates)),
        cost_term=pair_round_trip_bp / 1e4,
    )


@dataclass(frozen=True, slots=True)
class PairNet:
    """One pair's computed nets. An Absent net is underpowered, never zero."""

    event_coin: str
    control_coin: str
    dex: str
    cohort: str  # "backfill" | "forward"
    truncated_young: bool
    truncated_elder: bool
    pair_central_cost_bp: float
    net_30: float | Absent
    net_90: float | Absent
    young_funding_term_30: float | Absent
    young_price_term_30: float | Absent
    elder_funding_term_30: float | Absent
    elder_price_term_30: float | Absent

    def truncated(self) -> bool:
        return self.truncated_young or self.truncated_elder


@dataclass(frozen=True, slots=True)
class PairTest:
    n: int
    successes: int
    p_value: float
    passes: bool
    n_underpowered: int
    n_truncated: int


def _present_30(pairs: list[PairNet]) -> tuple[list[tuple[PairNet, float]], int]:
    present: list[tuple[PairNet, float]] = []
    underpowered = 0
    for pair in pairs:
        if isinstance(pair.net_30, Absent):
            underpowered += 1
        else:
            present.append((pair, pair.net_30))
    return present, underpowered


def e1_sign(pairs: list[PairNet], alpha_h: float) -> PairTest:
    """E1: exact one-sided sign test, share of pairs positive above one half.

    A pair net exactly at zero fails (the registered tie rule).
    """
    present, underpowered = _present_30(pairs)
    n = len(present)
    successes = sum(1 for _, net in present if net > 0.0)
    truncated = sum(1 for pair, _ in present if pair.truncated())
    if n == 0:
        return PairTest(0, 0, 1.0, False, underpowered, truncated)
    p_value = upper_tail(n, successes, 0.5)
    return PairTest(n, successes, p_value, p_value <= alpha_h, underpowered, truncated)


def e2_floor(pairs: list[PairNet], alpha_h: float, cfg: Config = CONFIG) -> PairTest:
    """E2: the economic floor — net at or above 2x the pair's central cost.

    The floor is inclusive (a net exactly at it passes), and the floor is
    per pair, from its own registered central cost.
    """
    present, underpowered = _present_30(pairs)
    n = len(present)
    successes = sum(
        1
        for pair, net in present
        if net >= cfg.h2_cost_floor_multiple * pair.pair_central_cost_bp / 1e4
    )
    truncated = sum(1 for pair, _ in present if pair.truncated())
    if n == 0:
        return PairTest(0, 0, 1.0, False, underpowered, truncated)
    p_value = upper_tail(n, successes, 0.5)
    return PairTest(n, successes, p_value, p_value <= alpha_h, underpowered, truncated)


@dataclass(frozen=True, slots=True)
class H2VerdictReport:
    e1: PairTest
    e2: PairTest
    both_pass: bool
    secondaries: dict[str, object]


def _share_positive(values: list[float]) -> float:
    return (sum(1 for v in values if v > 0.0) / len(values)) if values else 0.0


def h2_named_secondaries(pairs: list[PairNet]) -> dict[str, object]:
    """Exactly the registered list (registrations/H2 Section 8), descriptive."""
    present, _ = _present_30(pairs)
    nets_90 = [p.net_90 for p in pairs if not isinstance(p.net_90, Absent)]
    by_dex: dict[str, dict[str, float | int]] = {}
    for dex in sorted({p.dex for p, _ in present}):
        subset = [net for p, net in present if p.dex == dex]
        by_dex[dex or "main"] = {"n": len(subset), "share_positive": _share_positive(subset)}
    by_cohort: dict[str, dict[str, float | int]] = {}
    for cohort in ("backfill", "forward"):
        subset = [net for p, net in present if p.cohort == cohort]
        by_cohort[cohort] = {"n": len(subset), "share_positive": _share_positive(subset)}
    terms = [
        (
            p.young_funding_term_30,
            p.young_price_term_30,
            p.elder_funding_term_30,
            p.elder_price_term_30,
        )
        for p, _ in present
        if not any(
            isinstance(x, Absent)
            for x in (
                p.young_funding_term_30,
                p.young_price_term_30,
                p.elder_funding_term_30,
                p.elder_price_term_30,
            )
        )
    ]
    decomposition: dict[str, float | int] = {"n": len(terms)}
    if terms:
        for i, key in enumerate(
            ("mean_young_funding", "mean_young_price", "mean_elder_funding", "mean_elder_price")
        ):
            decomposition[key] = sum(float(t[i]) for t in terms) / len(terms)
    truncated_nets = [net for p, net in present if p.truncated()]
    return {
        "horizon_90d": {"n": len(nets_90), "share_positive": _share_positive(nets_90)},
        "per_dex_strata_30d": by_dex,
        "backfill_vs_forward_30d": by_cohort,
        "pair_decomposition_30d": decomposition,
        "truncated_subgroup_30d": {
            "n": len(truncated_nets),
            "share_positive": _share_positive(truncated_nets),
        },
    }


def run_h2_verdict(pairs: list[PairNet], alpha_h: float, cfg: Config = CONFIG) -> H2VerdictReport:
    """E1, E2, and the named secondaries. Both must pass for the GO row."""
    e1 = e1_sign(pairs, alpha_h)
    e2 = e2_floor(pairs, alpha_h, cfg)
    return H2VerdictReport(
        e1=e1,
        e2=e2,
        both_pass=e1.passes and e2.passes,
        secondaries=h2_named_secondaries(pairs),
    )


def pair_covered(event: EventCoverage, control: EventCoverage) -> bool:
    """The per-hypothesis coverage view for H2: both legs must meet the bars."""
    return event.meets_bars and control.meets_bars
