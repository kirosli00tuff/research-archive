"""The verdict machinery, built dark. Stage B calls it exactly once.

This module is pure arithmetic over in-memory records. It is structurally
incapable of reaching real sealed data: it names no path, opens no file,
parses no payload, and imports nothing that could — pinned by
tests/test_verdict.py against its parse tree. Until the registered Stage B
read, the only inputs it ever sees are synthetic fixtures with known
answers.

Tie rule, registered here before any real input exists: a value exactly on a
test's threshold that the strict inequality does not clear counts AGAINST
the hypothesis (P1 counts net > 0; P2 counts net >= +threshold per Section
8's 'at or below -15 percent' asset-side inclusive bound; P3 counts
young > control, so an exact tie is a failure).
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

from npl.absence import Absent
from npl.config import CONFIG, Config
from npl.power import upper_tail


class Cohort(StrEnum):
    RETRO = "retro"
    FORWARD = "forward"


@dataclass(frozen=True, slots=True)
class EventNet:
    """One event's computed nets. An Absent net is underpowered, never zero."""

    coin: str
    event_type: str
    cohort: Cohort
    truncated_by_delisting: bool
    net_short_30: float | Absent
    net_short_90: float | Absent
    funding_term_30: float | Absent
    price_term_30: float | Absent
    control_net_short_30: float | Absent
    control_net_short_90: float | Absent


@dataclass(frozen=True, slots=True)
class BinomialTest:
    n: int
    successes: int
    statistic: float
    passes: bool
    n_underpowered: int
    n_truncated_by_delisting: int


@dataclass(frozen=True, slots=True)
class VerdictReport:
    p1: BinomialTest
    p2: BinomialTest
    p3: BinomialTest
    all_co_primaries_pass: bool
    secondaries: dict[str, object]


def clopper_pearson_lower(successes: int, n: int, alpha: float) -> float:
    """Exact one-sided lower confidence bound on a binomial share."""
    if not 0 <= successes <= n or n <= 0:
        raise ValueError(f"impossible counts: {successes}/{n}")
    if successes == 0:
        return 0.0
    lo, hi = 0.0, 1.0
    for _ in range(200):
        mid = (lo + hi) / 2
        if mid <= 0.0 or mid >= 1.0:
            break
        if upper_tail(n, successes, mid) < alpha:
            lo = mid
        else:
            hi = mid
    return lo


def _present_30(events: list[EventNet]) -> tuple[list[tuple[EventNet, float]], int]:
    """Events with a present 30-day net, and the underpowered count."""
    present: list[tuple[EventNet, float]] = []
    underpowered = 0
    for event in events:
        net = event.net_short_30
        if isinstance(net, Absent):
            underpowered += 1
        else:
            present.append((event, net))
    return present, underpowered


def p1_profitability(events: list[EventNet], cfg: Config = CONFIG) -> BinomialTest:
    """P1: exact binomial lower bound on the share with positive 30d net short."""
    present, underpowered = _present_30(events)
    n = len(present)
    successes = sum(1 for _, net in present if net > 0.0)
    truncated = sum(1 for event, _ in present if event.truncated_by_delisting)
    if n == 0:
        return BinomialTest(0, 0, 0.0, False, underpowered, truncated)
    bound = clopper_pearson_lower(successes, n, cfg.alpha_adj)
    return BinomialTest(n, successes, bound, bound >= cfg.p1_bar, underpowered, truncated)


def p2_magnitude(events: list[EventNet], cfg: Config = CONFIG) -> BinomialTest:
    """P2: exact sign test that the share at or below -15 percent asset-side
    (net short at or above +|threshold|) exceeds one half."""
    present, underpowered = _present_30(events)
    n = len(present)
    bar = -cfg.p2_net_threshold
    successes = sum(1 for _, net in present if net >= bar)
    truncated = sum(1 for event, _ in present if event.truncated_by_delisting)
    if n == 0:
        return BinomialTest(0, 0, 1.0, False, underpowered, truncated)
    p_value = upper_tail(n, successes, 0.5)
    return BinomialTest(n, successes, p_value, p_value <= cfg.alpha_adj, underpowered, truncated)


def p3_contrast(events: list[EventNet], cfg: Config = CONFIG) -> BinomialTest:
    """P3: exact sign test on pairs; success is young net short > control's."""
    pairs: list[tuple[EventNet, float, float]] = []
    underpowered = 0
    for event in events:
        net = event.net_short_30
        control = event.control_net_short_30
        if isinstance(net, Absent) or isinstance(control, Absent):
            underpowered += 1
            continue
        pairs.append((event, net, control))
    n = len(pairs)
    successes = sum(1 for _, net, control in pairs if net > control)
    truncated = sum(1 for event, _, _ in pairs if event.truncated_by_delisting)
    if n == 0:
        return BinomialTest(0, 0, 1.0, False, underpowered, truncated)
    p_value = upper_tail(n, successes, 0.5)
    return BinomialTest(n, successes, p_value, p_value <= cfg.alpha_adj, underpowered, truncated)


def _share_positive_90(events: list[EventNet]) -> dict[str, float | int]:
    present = [e.net_short_90 for e in events if not isinstance(e.net_short_90, Absent)]
    n = len(present)
    return {"n": n, "share_positive": (sum(1 for x in present if x > 0.0) / n) if n else 0.0}


def named_secondaries(events: list[EventNet], cfg: Config = CONFIG) -> dict[str, object]:
    """The registered secondaries. Descriptive, never verdict-bearing."""
    present, _ = _present_30(events)
    by_type: dict[str, dict[str, float | int]] = {}
    for etype in sorted({e.event_type for e, _ in present}):
        subset = [net for e, net in present if e.event_type == etype]
        by_type[etype] = {
            "n": len(subset),
            "share_positive": sum(1 for x in subset if x > 0.0) / len(subset),
        }
    by_cohort: dict[str, dict[str, float | int]] = {}
    for cohort in Cohort:
        subset = [net for e, net in present if e.cohort is cohort]
        by_cohort[cohort.value] = {
            "n": len(subset),
            "share_positive": (sum(1 for x in subset if x > 0.0) / len(subset)) if subset else 0.0,
        }
    decomposition: dict[str, float | int] = {
        "n": 0,
        "mean_funding_term": 0.0,
        "mean_price_term": 0.0,
    }
    terms = [
        (e.funding_term_30, e.price_term_30)
        for e, _ in present
        if not isinstance(e.funding_term_30, Absent) and not isinstance(e.price_term_30, Absent)
    ]
    if terms:
        decomposition = {
            "n": len(terms),
            "mean_funding_term": sum(f for f, _ in terms if isinstance(f, float)) / len(terms),
            "mean_price_term": sum(p for _, p in terms if isinstance(p, float)) / len(terms),
        }
    days = cfg.horizon_secondary_days
    return {
        f"horizon_{days}d": _share_positive_90(events),
        "per_type_strata_30d": by_type,
        "forward_vs_retro_30d": by_cohort,
        "h8_decomposition_30d": decomposition,
    }


def run_verdict(events: list[EventNet], cfg: Config = CONFIG) -> VerdictReport:
    """P1, P2, P3 and the named secondaries. All three must pass for GO."""
    p1 = p1_profitability(events, cfg)
    p2 = p2_magnitude(events, cfg)
    p3 = p3_contrast(events, cfg)
    return VerdictReport(
        p1=p1,
        p2=p2,
        p3=p3,
        all_co_primaries_pass=p1.passes and p2.passes and p3.passes,
        secondaries=named_secondaries(events, cfg),
    )
