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

Amendment H2-5 replaced the H2-3 fallback with the tiered control rule, so
every pair now carries a `tier` and a `class_pair`. **Tier is a named
stratum reported beside every primary figure at every look**, alongside the
`same_dex` stratum H2-3 registered — which is retained and, under the tiered
rule, is exactly the tier-1 subset plus any tier-2 or tier-3 pair whose
elder happens to sit on the event's own dex.

Amendment H2-3 makes the reader look-aware. Each co-primary is decided
against the exact two-look boundary of `npl.register.sequential`, not
against a p-value threshold; both co-primaries must clear the same look's
criterion for a GO; look 1 can only GO, CONTINUE, or fire the registered
futility boundary; only look 2 and that futility boundary fire a terminal
row. The `same_dex` stratum and the old 2x economic floor travel beside
every primary figure as named secondaries.
"""

from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass
from enum import StrEnum

from npl.absence import Absent
from npl.census import EVENT_HIP3
from npl.config import CONFIG, Config
from npl.coverage import EventCoverage
from npl.pairtype import PAIR_TYPE_SAME_DEX
from npl.power import upper_tail
from npl.register.sequential import (
    LookOrderViolation,
    TwoLookDesign,
    futility_boundary,
    two_look_design,
)
from npl.tier import REGISTERED_TIERS, TIER_NAMES


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
    pair_type: str  # "same_dex" | "cross_dex" (Amendment H2-3 Change 1)
    tier: int  # 1 | 2 | 3 (Amendment H2-5 section 2)
    class_pair: str  # e.g. "equity->etf" (Amendment H2-5 section 2)
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


# ---------------------------------------------------------------------------
# Amendment H2-3 Change 3: the two-look sequential reader.
# ---------------------------------------------------------------------------


class LookRow(StrEnum):
    """The rows the registered outcome map can fire. CONTINUE is not a verdict."""

    GO = "GO"
    CONTINUE = "CONTINUE"
    FAIL = "FAIL"


@dataclass(frozen=True, slots=True)
class CoPrimaryPlan:
    """One co-primary's registered planning constants, fixed before any read.

    `look2_min_n` is the registered look-2 minimum N. It supplies the n2 the
    look-1 futility computation needs, since the real n2 is not observable
    at look 1; where the observed n1 already exceeds it, the observed n1 is
    used instead (a futility test can never look backwards).
    """

    name: str
    p_true: float
    look2_min_n: int


@dataclass(frozen=True, slots=True)
class SequentialPlan:
    """The registered two-look plan. alpha_1 + alpha_2 = alpha_h = 0.05."""

    alpha_1: float
    alpha_2: float
    e1: CoPrimaryPlan
    e2: CoPrimaryPlan

    def alpha_total(self) -> float:
        return self.alpha_1 + self.alpha_2


def registered_plan(
    e1_look2_min_n: int, e2_look2_min_n: int, cfg: Config = CONFIG
) -> SequentialPlan:
    """The plan from the registered constants and the Task 3 minimum-N table."""
    return SequentialPlan(
        alpha_1=cfg.h2_alpha_look1,
        alpha_2=cfg.h2_alpha_look2,
        e1=CoPrimaryPlan("E1", cfg.h2_e1_true_share, e1_look2_min_n),
        e2=CoPrimaryPlan("E2", cfg.h2_e2_true_share, e2_look2_min_n),
    )


@dataclass(frozen=True, slots=True)
class LookOutcome:
    """One co-primary at one look: the counts, the boundary, and the decision."""

    co_primary: str
    look: int
    n: int
    successes: int
    k1: int | None
    k2: int | None
    crossed_look1: bool
    crossed_look2: bool
    rejects: bool
    n_underpowered: int
    n_truncated: int
    futility_boundary: int | None
    futility_fired: bool
    alpha_spent_1: float
    alpha_spent_2: float


@dataclass(frozen=True, slots=True)
class Look1Record:
    """What look 1 hands forward: counts and nothing else. No rate, no price."""

    n1: int
    e1_successes: int
    e2_successes: int


@dataclass(frozen=True, slots=True)
class H2LookReport:
    look: int
    e1: LookOutcome
    e2: LookOutcome
    row: LookRow
    terminal: bool
    look1_record: Look1Record
    secondaries: dict[str, object]


def _successes_e1(present: list[tuple[PairNet, float]]) -> int:
    """A pair net exactly at zero fails (the registered tie rule)."""
    return sum(1 for _, net in present if net > 0.0)


def _successes_e2(present: list[tuple[PairNet, float]], multiple: float) -> int:
    """The floor is per pair and inclusive (a net exactly at it passes)."""
    return sum(1 for pair, net in present if net >= multiple * pair.pair_central_cost_bp / 1e4)


def _outcome(
    plan_leg: CoPrimaryPlan,
    look: int,
    n: int,
    successes: int,
    prior: Look1Record | None,
    prior_successes: int,
    plan: SequentialPlan,
    underpowered: int,
    truncated: int,
    cfg: Config,
) -> LookOutcome:
    if look == 1:
        design = two_look_design(n, max(n, plan_leg.look2_min_n), plan.alpha_1, plan.alpha_2)
        crossed_1 = design.k1 is not None and successes >= design.k1
        floor = futility_boundary(design, plan_leg.p_true, cfg)
        return LookOutcome(
            co_primary=plan_leg.name,
            look=1,
            n=n,
            successes=successes,
            k1=design.k1,
            k2=design.k2,
            crossed_look1=crossed_1,
            crossed_look2=False,
            rejects=crossed_1,
            n_underpowered=underpowered,
            n_truncated=truncated,
            futility_boundary=floor,
            futility_fired=(not crossed_1) and floor is not None and successes <= floor,
            alpha_spent_1=design.alpha_spent_1,
            alpha_spent_2=design.alpha_spent_2,
        )
    if prior is None:
        raise LookOrderViolation(
            "look 2 needs look 1's recorded counts; a look-2 read without look 1 is refused"
        )
    design = two_look_design(prior.n1, n, plan.alpha_1, plan.alpha_2)
    crossed_1 = design.k1 is not None and prior_successes >= design.k1
    crossed_2 = design.k2 is not None and successes >= design.k2
    return LookOutcome(
        co_primary=plan_leg.name,
        look=2,
        n=n,
        successes=successes,
        k1=design.k1,
        k2=design.k2,
        crossed_look1=crossed_1,
        crossed_look2=crossed_2,
        # Amendment H2-4: a co-primary passes at look 2 when the two-look
        # procedure has rejected its null BY look 2. Requiring S1 < k1 here
        # would turn stronger look-1 evidence on one co-primary into a
        # guaranteed FAIL — a defect of the H2-3 wording, corrected before
        # any outcome existed. Type-I stays at alpha_1 + alpha_2 exactly:
        # this is the union of the two registered rejection regions.
        rejects=crossed_1 or crossed_2,
        n_underpowered=underpowered,
        n_truncated=truncated,
        futility_boundary=None,
        futility_fired=False,
        alpha_spent_1=design.alpha_spent_1,
        alpha_spent_2=design.alpha_spent_2,
    )


def same_dex_stratum(pairs: list[PairNet], cfg: Config = CONFIG) -> dict[str, object]:
    """The named `same_dex` stratum: E1 and E2 counts on same-dex pairs only.

    Descriptive, never verdict-bearing. The subset is taken on the pair's
    registered tag; a cross_dex pair admitted here would misreport the
    stratum, and the mutation exercise targets exactly that.
    """
    present, _ = _present_30(pairs)
    subset = [(pair, net) for pair, net in present if pair.pair_type == PAIR_TYPE_SAME_DEX]
    n = len(subset)
    e1 = _successes_e1(subset)
    e2 = _successes_e2(subset, cfg.h2_cost_floor_multiple)
    return {
        "n": n,
        "n_all_pairs": len(present),
        "e1_successes": e1,
        "e1_share": (e1 / n) if n else 0.0,
        "e2_successes": e2,
        "e2_share": (e2 / n) if n else 0.0,
    }


def tier_stratum(pairs: list[PairNet], cfg: Config = CONFIG) -> dict[str, object]:
    """The named tier stratum: E1 and E2 counts within each registered tier.

    Descriptive, never verdict-bearing, and **every registered tier appears
    even at zero pairs** — an absent row would read as "no such pairs" where
    the truth is "none yet". An unregistered tier is a loud refusal, never a
    new bucket.
    """
    present, _ = _present_30(pairs)
    out: dict[str, object] = {}
    for tier in REGISTERED_TIERS:
        subset = [(pair, net) for pair, net in present if pair.tier == tier]
        n = len(subset)
        e1 = _successes_e1(subset)
        e2 = _successes_e2(subset, cfg.h2_cost_floor_multiple)
        out[f"tier_{tier}"] = {
            "name": TIER_NAMES[tier],
            "n": n,
            "e1_successes": e1,
            "e1_share": (e1 / n) if n else 0.0,
            "e2_successes": e2,
            "e2_share": (e2 / n) if n else 0.0,
        }
    unregistered = sorted({pair.tier for pair, _ in present} - set(REGISTERED_TIERS))
    if unregistered:
        raise ValueError(
            f"unregistered tier(s) {unregistered} among the pairs; "
            f"the registered tiers are {list(REGISTERED_TIERS)}"
        )
    out["n_all_pairs"] = len(present)
    return out


def class_pair_stratum(pairs: list[PairNet]) -> dict[str, object]:
    """The class-pair composition of the sample. Descriptive, counts only.

    Unlike the tiers the set of class pairs is not fixed in advance, so only
    those that occur are reported, in name order.
    """
    present, _ = _present_30(pairs)
    out: dict[str, object] = {}
    for label in sorted({pair.class_pair for pair, _ in present}):
        subset = [(pair, net) for pair, net in present if pair.class_pair == label]
        n = len(subset)
        out[label] = {"n": n, "e1_share": (_successes_e1(subset) / n) if n else 0.0}
    return out


def two_times_floor_secondary(pairs: list[PairNet], cfg: Config = CONFIG) -> dict[str, object]:
    """E2 recomputed at the pre-amendment 2x floor. Descriptive, at every look."""
    present, _ = _present_30(pairs)
    n = len(present)
    successes = _successes_e2(present, cfg.h2_cost_floor_multiple_secondary)
    return {
        "multiple": cfg.h2_cost_floor_multiple_secondary,
        "n": n,
        "successes": successes,
        "share": (successes / n) if n else 0.0,
    }


def run_h2_look(
    pairs: list[PairNet],
    *,
    look: int,
    plan: SequentialPlan,
    prior: Look1Record | None = None,
    cfg: Config = CONFIG,
) -> H2LookReport:
    """One registered look. Both co-primaries at the same look, or no GO.

    look 1: GO when both cross k1; FAIL on the registered futility boundary
    for either co-primary; CONTINUE otherwise — and a CONTINUE fires no row.
    look 2: GO when both have rejected by look 2; FAIL otherwise. Terminal.
    """
    if look not in (1, 2):
        raise LookOrderViolation(f"{look!r} is not a registered look; the plan has exactly two")
    if look == 2 and prior is not None and len(_present_30(pairs)[0]) < prior.n1:
        raise LookOrderViolation(
            f"look 2 sees {len(_present_30(pairs)[0])} pairs against look 1's {prior.n1}; "
            f"the pair count never shrinks and the boundary refuses to guess"
        )
    present, underpowered = _present_30(pairs)
    n = len(present)
    truncated = sum(1 for pair, _ in present if pair.truncated())
    e1_successes = _successes_e1(present)
    e2_successes = _successes_e2(present, cfg.h2_cost_floor_multiple)

    e1 = _outcome(
        plan.e1,
        look,
        n,
        e1_successes,
        prior,
        prior.e1_successes if prior else 0,
        plan,
        underpowered,
        truncated,
        cfg,
    )
    e2 = _outcome(
        plan.e2,
        look,
        n,
        e2_successes,
        prior,
        prior.e2_successes if prior else 0,
        plan,
        underpowered,
        truncated,
        cfg,
    )

    if look == 1:
        if e1.rejects and e2.rejects:
            row, terminal = LookRow.GO, True
        elif e1.futility_fired or e2.futility_fired:
            row, terminal = LookRow.FAIL, True
        else:
            row, terminal = LookRow.CONTINUE, False
    else:
        row = LookRow.GO if (e1.rejects and e2.rejects) else LookRow.FAIL
        terminal = True

    secondaries = h2_named_secondaries(pairs)
    secondaries["same_dex_stratum"] = same_dex_stratum(pairs, cfg)
    secondaries["tier_stratum"] = tier_stratum(pairs, cfg)
    secondaries["class_pair_stratum"] = class_pair_stratum(pairs)
    secondaries["economic_floor_two_times"] = two_times_floor_secondary(pairs, cfg)
    return H2LookReport(
        look=look,
        e1=e1,
        e2=e2,
        row=row,
        terminal=terminal,
        look1_record=Look1Record(n1=n, e1_successes=e1_successes, e2_successes=e2_successes),
        secondaries=secondaries,
    )


def design_at(n1: int, n2: int, plan: SequentialPlan) -> TwoLookDesign:
    """The plan's exact boundary at one pair of look sizes. Used by the k-table."""
    return two_look_design(n1, n2, plan.alpha_1, plan.alpha_2)
