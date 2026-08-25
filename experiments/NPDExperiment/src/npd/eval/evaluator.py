"""Stage B.2. The only module permitted to read the sealed forward returns.

Nothing else in this repository may name var/npd_sealed.db, query its
forward_return table, or call read_sealed_returns. tests/test_guards.py walks
every source file and fails the moment another module does.

The evaluator refuses to run while Amendment 0 is empty. That refusal is the
mechanism, not a reminder: the operator writes his prior down before he can see
a number.
"""

from __future__ import annotations

import math
import random
import re
import sqlite3
from collections.abc import Sequence
from dataclasses import dataclass, field
from pathlib import Path

from npd.baselines import BASELINE_NAMES
from npd.config import CONFIG, Config
from npd.paths import REPO_ROOT, SEALED_DB

AMENDMENT_0_EMPTY_MARKER = "[ EMPTY."
REGISTRATION = REPO_ROOT / "REGISTRATION.md"


class AmendmentZeroMissing(RuntimeError):
    """The operator prior is not recorded. B.2 refuses to run."""


class LeakageDetected(RuntimeError):
    """The negative control did not collapse. Everything stops."""


def amendment_zero_section(path: Path = REGISTRATION) -> str | None:
    """The text of Section 13, or None when it cannot be found."""
    if not path.exists():
        return None
    text = path.read_text(encoding="utf-8")
    match = re.search(r"## Section 13\.(.*?)(?=\n## Section 14\.)", text, re.S)
    return None if match is None else match.group(1)


def amendment_zero_prior(path: Path = REGISTRATION) -> float | None:
    """The recorded operator prior as a probability, or None when absent.

    The slot has to hold a number in [0, 1], not merely lack the empty marker.
    A section that says a prior was recorded without recording one is empty in
    every sense that matters here.
    """
    section = amendment_zero_section(path)
    if section is None or AMENDMENT_0_EMPTY_MARKER in section:
        return None
    match = re.search(
        r"probability that a rigorous version.*?\n>\s*\n>\s+([01](?:\.\d+)?)",
        section,
        re.S,
    )
    if match is None:
        return None
    value = float(match.group(1))
    return value if 0.0 <= value <= 1.0 else None


def amendment_zero_filled(path: Path = REGISTRATION) -> bool:
    """Whether the operator has written a usable prior into Section 13."""
    return amendment_zero_prior(path) is not None


def require_amendment_zero(path: Path = REGISTRATION) -> None:
    if not amendment_zero_filled(path):
        raise AmendmentZeroMissing(
            "Amendment 0 is empty. The operator writes his registered prior into "
            "REGISTRATION.md Section 13 before B.2 runs. Refusing."
        )


def read_sealed_returns(horizon: int, path: Path = SEALED_DB) -> dict[tuple[str, str], float]:
    """The sealed forward returns. This function has exactly one caller."""
    if not path.exists():
        raise FileNotFoundError(f"sealed store missing: {path}")
    con = sqlite3.connect(f"file:{path}?mode=ro", uri=True)
    try:
        rows = con.execute(
            "SELECT date, symbol, ret FROM forward_return WHERE horizon = ? AND ret IS NOT NULL",
            (horizon,),
        ).fetchall()
    finally:
        con.close()
    return {(r[0], r[1]): float(r[2]) for r in rows}


def spearman(ranks_a: Sequence[float], ranks_b: Sequence[float]) -> float:
    """Pearson correlation of two rank vectors."""
    n = len(ranks_a)
    if n != len(ranks_b) or n < 3:
        raise ValueError("need at least three paired ranks")
    ma = sum(ranks_a) / n
    mb = sum(ranks_b) / n
    num = sum((a - ma) * (b - mb) for a, b in zip(ranks_a, ranks_b, strict=True))
    da = math.sqrt(sum((a - ma) ** 2 for a in ranks_a))
    db = math.sqrt(sum((b - mb) ** 2 for b in ranks_b))
    if da <= 0 or db <= 0:
        raise ValueError("a rank vector has zero spread")
    return num / (da * db)


def _ranks_from_order(order: Sequence[str]) -> dict[str, float]:
    return {sym: float(i + 1) for i, sym in enumerate(order)}


def _outcome_ranks(symbols: Sequence[str], returns: dict[str, float]) -> dict[str, float]:
    ordered = sorted(symbols, key=lambda s: (-returns[s], s))
    return _ranks_from_order(ordered)


def daily_ic(order: Sequence[str], returns: dict[str, float]) -> float:
    """Rank IC for one day. Predicted order against realized order.

    Both vectors rank best first, so a positive value means the ranking put the
    winners near the top.
    """
    symbols = [s for s in order if s in returns]
    if len(symbols) < 3:
        raise ValueError("too few symbols with a realized return")
    pred = _ranks_from_order([s for s in order if s in returns])
    real = _outcome_ranks(symbols, returns)
    # Rank 1 is best in both vectors, so a perfect ranking correlates at plus
    # one. No negation. tests/test_evaluator_synthetic.py pins the convention.
    return spearman([pred[s] for s in symbols], [real[s] for s in symbols])


@dataclass(frozen=True, slots=True)
class Interval:
    point: float
    low: float
    high: float

    def excludes_zero(self) -> bool:
        return self.low > 0.0 or self.high < 0.0


@dataclass(slots=True)
class Verdict:
    n_days: int
    model_mean_ic: float
    baseline_mean_ic: dict[str, float] = field(default_factory=dict)
    best_baseline: str = ""
    contrast: Interval | None = None
    permutation_p: float = 1.0
    negative_control_mean_ic: float = 0.0
    beats_coin: bool = False
    beats_best_baseline: bool = False
    outcome: str = ""


def block_bootstrap_interval(
    values: Sequence[float],
    *,
    resamples: int,
    block_length: int,
    t_critical: float,
    seed: int,
) -> Interval:
    """Moving-block bootstrap on a day-ordered series.

    Blocks are used rather than independent days because a multi-session horizon
    makes consecutive days share most of their forward window. The block length
    is registered at twice the primary horizon.
    """
    n = len(values)
    if n < block_length:
        raise ValueError("series shorter than one block")
    rng = random.Random(seed)
    point = sum(values) / n
    n_blocks = math.ceil(n / block_length)
    means: list[float] = []
    for _ in range(resamples):
        drawn: list[float] = []
        for _ in range(n_blocks):
            start = rng.randrange(0, n - block_length + 1)
            drawn.extend(values[start : start + block_length])
        drawn = drawn[:n]
        means.append(sum(drawn) / n)
    means.sort()
    sd = math.sqrt(sum((m - point) ** 2 for m in means) / (len(means) - 1))
    return Interval(point=point, low=point - t_critical * sd, high=point + t_critical * sd)


def within_day_permutation_p(
    orders: dict[str, list[str]],
    returns_by_day: dict[str, dict[str, float]],
    observed: float,
    *,
    resamples: int,
    seed: int,
) -> float:
    """Two-sided p under a null that shuffles each ranking inside its own day."""
    rng = random.Random(seed)
    days = sorted(orders)
    count = 0
    for _ in range(resamples):
        total = 0.0
        for d in days:
            shuffled = list(orders[d])
            rng.shuffle(shuffled)
            total += daily_ic(shuffled, returns_by_day[d])
        if abs(total / len(days)) >= abs(observed):
            count += 1
    return (count + 1) / (resamples + 1)


def evaluate(
    model_orders: dict[str, list[str]],
    baseline_orders: dict[str, dict[str, list[str]]],
    returns_by_day: dict[str, dict[str, float]],
    cfg: Config = CONFIG,
    *,
    seed: int = 20260825,
) -> Verdict:
    """Run the registered inference. Primary contrast, permutation null, control."""
    days = sorted(d for d in model_orders if returns_by_day.get(d))
    if not days:
        raise ValueError("no evaluable days")

    model_ics = [daily_ic(model_orders[d], returns_by_day[d]) for d in days]
    verdict = Verdict(n_days=len(days), model_mean_ic=sum(model_ics) / len(days))

    for name in BASELINE_NAMES:
        orders = baseline_orders.get(name, {})
        ics = [daily_ic(orders[d], returns_by_day[d]) for d in days if d in orders]
        verdict.baseline_mean_ic[name] = sum(ics) / len(ics) if ics else 0.0

    verdict.best_baseline = max(verdict.baseline_mean_ic, key=lambda k: verdict.baseline_mean_ic[k])
    best_orders = baseline_orders[verdict.best_baseline]
    contrast_series = [
        daily_ic(model_orders[d], returns_by_day[d]) - daily_ic(best_orders[d], returns_by_day[d])
        for d in days
    ]

    block = 2 * cfg.primary_horizon_sessions
    verdict.contrast = block_bootstrap_interval(
        contrast_series,
        resamples=cfg.bootstrap_resamples,
        block_length=block,
        t_critical=cfg.t_critical,
        seed=seed,
    )

    coin_interval = block_bootstrap_interval(
        model_ics,
        resamples=cfg.bootstrap_resamples,
        block_length=block,
        t_critical=cfg.t_critical,
        seed=seed + 1,
    )
    verdict.beats_coin = coin_interval.low > 0.0
    verdict.beats_best_baseline = verdict.contrast.low > 0.0

    verdict.permutation_p = within_day_permutation_p(
        {d: model_orders[d] for d in days},
        returns_by_day,
        verdict.model_mean_ic,
        resamples=min(cfg.permutation_resamples, 1000),
        seed=seed + 2,
    )

    control_rng = random.Random(seed + 3)
    control_ics = []
    for d in days:
        shuffled = list(model_orders[d])
        control_rng.shuffle(shuffled)
        control_ics.append(daily_ic(shuffled, returns_by_day[d]))
    verdict.negative_control_mean_ic = sum(control_ics) / len(control_ics)

    if verdict.beats_coin and verdict.beats_best_baseline:
        verdict.outcome = "conditional phase C.1 authorized, labelled a large-effect screen"
    elif verdict.beats_coin:
        verdict.outcome = "an expensive wrapper for a subtraction. No phase. Finding recorded."
    else:
        verdict.outcome = (
            "the replication confirms the council negative under frontier capability "
            "and sane formulation. Closed."
        )
    return verdict


def assert_control_collapsed(verdict: Verdict, tolerance: float = 0.02) -> None:
    """The negative control must collapse toward zero. Non-zero stops everything."""
    if abs(verdict.negative_control_mean_ic) > tolerance:
        raise LeakageDetected(
            f"the within-day shuffle control read {verdict.negative_control_mean_ic:+.4f}, "
            f"outside the {tolerance} tolerance. Everything stops."
        )


# ---------------------------------------------------------------------------
# Stage B.2. The one-shot evaluation.
#
# Everything below runs once. The sealed store is opened here and nowhere else,
# and the order of operations is fixed by the registration: Amendment 0 first,
# the pipeline validity gate second, and the primary contrast only after the
# gate passes.
# ---------------------------------------------------------------------------


def daily_ic_from_ranks(realized_in_predicted_order: Sequence[float]) -> float:
    """Rank IC for one day, given realized ranks already aligned to the ranking.

    The predicted ranks are 1..n by construction, because the argument is
    ordered best-predicted first. Equivalent to daily_ic and asserted against it
    on real data before use, so the demonstrated scorer stays authoritative.
    """
    n = len(realized_in_predicted_order)
    if n < 3:
        raise ValueError("rank IC needs at least three names")
    predicted = [float(i + 1) for i in range(n)]
    return spearman(predicted, list(realized_in_predicted_order))


def realized_rank_row(order: Sequence[str], returns: dict[str, float]) -> list[float] | None:
    """Realized ranks aligned to a predicted order, or None when incomplete.

    A day is evaluable only when every name in its panel carries a realized
    return. A partial panel would change the null variance of the daily IC from
    one day to the next and would put the model and the baselines on different
    names. The absence is recorded and the day is dropped, never filled.
    """
    if any(sym not in returns for sym in order):
        return None
    real = _outcome_ranks(list(order), returns)
    return [real[sym] for sym in order]


def _mean(values: Sequence[float]) -> float:
    return sum(values) / len(values)


def _percentile(sorted_values: Sequence[float], q: float) -> float:
    idx = min(len(sorted_values) - 1, max(0, round(q * (len(sorted_values) - 1))))
    return sorted_values[idx]


@dataclass(frozen=True, slots=True)
class NullDistribution:
    """The within-day permutation null of the mean daily rank IC."""

    draws: int
    grand_mean: float
    sd: float
    monte_carlo_se: float
    p2_5: float
    p97_5: float
    means: tuple[float, ...]

    @property
    def mc_low(self) -> float:
        return self.grand_mean - 1.96 * self.monte_carlo_se

    @property
    def mc_high(self) -> float:
        return self.grand_mean + 1.96 * self.monte_carlo_se


def within_day_null(rows: Sequence[Sequence[float]], *, draws: int, seed: int) -> NullDistribution:
    """Shuffle each day ranking independently and take the mean daily IC.

    Vectorized because the registration asks for 10,000 draws over hundreds of
    days. The formula is the tie-free Spearman identity, and
    assert_scorer_agreement pins it against the demonstrated scorer before this
    runs.
    """
    import numpy as np

    rng = np.random.default_rng(seed)
    y = np.asarray(rows, dtype=float)
    n_days, n = y.shape
    predicted = np.arange(1, n + 1, dtype=float)
    denom = n * (n * n - 1)

    means = np.empty(draws, dtype=float)
    for i in range(draws):
        idx = np.argsort(rng.random((n_days, n)), axis=1)
        shuffled = np.take_along_axis(y, idx, axis=1)
        d = shuffled - predicted
        rho = 1.0 - 6.0 * np.sum(d * d, axis=1) / denom
        means[i] = float(rho.mean())

    ordered = sorted(means.tolist())
    grand = float(means.mean())
    sd = float(means.std(ddof=1))
    return NullDistribution(
        draws=draws,
        grand_mean=grand,
        sd=sd,
        monte_carlo_se=sd / math.sqrt(draws),
        p2_5=_percentile(ordered, 0.025),
        p97_5=_percentile(ordered, 0.975),
        means=tuple(means.tolist()),
    )


def assert_scorer_agreement(
    orders: dict[str, list[str]],
    rows: dict[str, list[float]],
    returns_by_day: dict[str, dict[str, float]],
) -> None:
    """The fast path must agree with the demonstrated scorer, exactly.

    B.0 proved daily_ic correct on synthetic data and caught an inverted sign
    doing it. This session inherits that demonstration rather than repeating it,
    so the vectorized path is checked against daily_ic instead of trusted.
    """
    for date, row in rows.items():
        a = daily_ic(orders[date], returns_by_day[date])
        b = daily_ic_from_ranks(row)
        if abs(a - b) > 1e-9:
            raise RuntimeError(
                f"the fast scorer disagrees with daily_ic on {date}: {a} against {b}"
            )


@dataclass(slots=True)
class HorizonResult:
    """Everything computed for one horizon. Primary or secondary, labelled."""

    horizon: int
    label: str
    n_days: int
    n_dropped_incomplete: int
    model_mean_ic: float
    model_interval: Interval
    baseline_mean_ic: dict[str, float]
    best_baseline: str
    contrast_point: float
    contrast_interval: Interval
    contrast_sd_daily: float
    bootstrap_se: float
    realized_mde: float
    effective_n: float
    beats_coin: bool
    beats_best_baseline: bool


def load_rankings(store_path: Path) -> tuple[dict[str, list[str]], dict[str, dict[str, list[str]]]]:
    """Model and baseline orders from the experiment own store.

    This store holds no outcome. It is not the sealed store and reading it is
    not the one read.
    """
    con = sqlite3.connect(f"file:{store_path}?mode=ro", uri=True)
    try:
        model: dict[str, list[str]] = {}
        for date, _rank, symbol in con.execute(
            "SELECT date, rank, symbol FROM model_ranking ORDER BY date, rank"
        ):
            model.setdefault(str(date), []).append(str(symbol))
        baselines: dict[str, dict[str, list[str]]] = {}
        for name, date, _rank, symbol in con.execute(
            "SELECT baseline, date, rank, symbol FROM baseline_ranking ORDER BY baseline, date, rank"
        ):
            baselines.setdefault(str(name), {}).setdefault(str(date), []).append(str(symbol))
        return model, baselines
    finally:
        con.close()


def evaluate_horizon(
    horizon: int,
    label: str,
    model_orders: dict[str, list[str]],
    baseline_orders: dict[str, dict[str, list[str]]],
    returns_by_day: dict[str, dict[str, float]],
    cfg: Config,
    *,
    seed: int,
) -> HorizonResult:
    """One horizon, computed identically to every other."""
    candidate_days = sorted(d for d in model_orders if d in returns_by_day)
    days: list[str] = []
    dropped = 0
    for d in candidate_days:
        if realized_rank_row(model_orders[d], returns_by_day[d]) is None:
            dropped += 1
            continue
        if any(d not in baseline_orders.get(n, {}) for n in BASELINE_NAMES):
            dropped += 1
            continue
        days.append(d)
    if not days:
        raise ValueError(f"no evaluable days at horizon {horizon}")

    model_ics = [daily_ic(model_orders[d], returns_by_day[d]) for d in days]
    baseline_ics = {
        n: [daily_ic(baseline_orders[n][d], returns_by_day[d]) for d in days]
        for n in BASELINE_NAMES
    }
    baseline_mean = {n: _mean(v) for n, v in baseline_ics.items()}

    # Best baseline chosen after the fact, which raises the bar the model must
    # clear rather than lowering it. ADR-010 records the conservatism.
    best = max(baseline_mean, key=lambda k: baseline_mean[k])
    contrast_series = [m - b for m, b in zip(model_ics, baseline_ics[best], strict=True)]

    block = 2 * cfg.primary_horizon_sessions
    contrast_iv = block_bootstrap_interval(
        contrast_series,
        resamples=cfg.bootstrap_resamples,
        block_length=block,
        t_critical=cfg.t_critical,
        seed=seed,
    )
    model_iv = block_bootstrap_interval(
        model_ics,
        resamples=cfg.bootstrap_resamples,
        block_length=block,
        t_critical=cfg.t_critical,
        seed=seed + 1,
    )

    se = (contrast_iv.high - contrast_iv.point) / cfg.t_critical
    mean_c = _mean(contrast_series)
    sd_daily = math.sqrt(
        sum((x - mean_c) ** 2 for x in contrast_series) / (len(contrast_series) - 1)
    )
    effective_n = (sd_daily / se) ** 2 if se > 0 else float("nan")

    return HorizonResult(
        horizon=horizon,
        label=label,
        n_days=len(days),
        n_dropped_incomplete=dropped,
        model_mean_ic=_mean(model_ics),
        model_interval=model_iv,
        baseline_mean_ic=baseline_mean,
        best_baseline=best,
        contrast_point=contrast_iv.point,
        contrast_interval=contrast_iv,
        contrast_sd_daily=sd_daily,
        bootstrap_se=se,
        realized_mde=cfg.t_critical * se,
        effective_n=effective_n,
        beats_coin=model_iv.low > 0.0,
        beats_best_baseline=contrast_iv.low > 0.0,
    )


# The registered tolerance for the pipeline validity gate. A shuffled mean
# outside this band means the scorer, the join, or the label mapping is wrong.
CONTROL_TOLERANCE = 0.02


@dataclass(slots=True)
class B2Result:
    amendment_zero_prior: float | None
    gate_passed: bool
    gate: NullDistribution | None
    primary: HorizonResult | None
    secondary: HorizonResult | None
    permutation_null: NullDistribution | None
    permutation_p: float
    first_half_ic: float
    second_half_ic: float
    first_half_days: int
    second_half_days: int
    verdict_row: str
    verdict_text: str
    c1_authorized: bool
    stopped_reason: str


def run_b2(
    *,
    store_path: Path | None = None,
    sealed_path: Path = SEALED_DB,
    cfg: Config = CONFIG,
    seed: int = 20260825,
) -> B2Result:
    """Stage B.2. Runs once.

    Order is fixed by the registration. Amendment 0 is asserted first. The
    pipeline validity gate runs second and gates everything after it. The
    primary contrast is not computed at all unless the gate passes.
    """
    from npd.paths import STORE_DB

    require_amendment_zero()
    prior = amendment_zero_prior()

    store = store_path or STORE_DB
    model_orders, baseline_orders = load_rankings(store)

    # The one read.
    returns_5 = read_sealed_returns(cfg.primary_horizon_sessions, sealed_path)
    returns_1 = read_sealed_returns(cfg.secondary_horizon_sessions, sealed_path)

    def by_day(flat: dict[tuple[str, str], float]) -> dict[str, dict[str, float]]:
        out: dict[str, dict[str, float]] = {}
        for (d, s), v in flat.items():
            out.setdefault(d, {})[s] = v
        return out

    r5 = by_day(returns_5)
    r1 = by_day(returns_1)

    # Rows for the primary horizon, used by the gate and the permutation null.
    rows: dict[str, list[float]] = {}
    for d in sorted(model_orders):
        if d not in r5:
            continue
        row = realized_rank_row(model_orders[d], r5[d])
        if row is not None:
            rows[d] = row
    if not rows:
        raise ValueError("no evaluable days at the primary horizon")

    assert_scorer_agreement(model_orders, rows, r5)

    # ---- Task 2. The pipeline validity gate. -----------------------------
    ordered_days = sorted(rows)
    gate = within_day_null(
        [rows[d] for d in ordered_days], draws=cfg.permutation_resamples, seed=seed
    )
    gate_passed = abs(gate.grand_mean) <= CONTROL_TOLERANCE
    if not gate_passed:
        return B2Result(
            amendment_zero_prior=prior,
            gate_passed=False,
            gate=gate,
            primary=None,
            secondary=None,
            permutation_null=None,
            permutation_p=float("nan"),
            first_half_ic=float("nan"),
            second_half_ic=float("nan"),
            first_half_days=0,
            second_half_days=0,
            verdict_row="",
            verdict_text="",
            c1_authorized=False,
            stopped_reason=(
                f"the shuffled mean read {gate.grand_mean:+.5f}, outside the "
                f"{CONTROL_TOLERANCE} tolerance. The scorer, the join, or the label "
                "mapping is wrong and every downstream number would be an artifact."
            ),
        )

    # ---- Task 3. The primary contrast. -----------------------------------
    primary = evaluate_horizon(
        cfg.primary_horizon_sessions,
        "primary",
        model_orders,
        baseline_orders,
        r5,
        cfg,
        seed=seed + 10,
    )

    # ---- Task 4. The permutation null, drawn independently of the gate. ---
    perm = within_day_null(
        [rows[d] for d in ordered_days], draws=cfg.permutation_resamples, seed=seed + 20
    )
    observed = primary.model_mean_ic
    hits = sum(1 for m in perm.means if abs(m) >= abs(observed))
    permutation_p = (hits + 1) / (perm.draws + 1)

    # ---- Task 5. Secondaries and descriptives. ---------------------------
    secondary = evaluate_horizon(
        cfg.secondary_horizon_sessions,
        "secondary",
        model_orders,
        baseline_orders,
        r1,
        cfg,
        seed=seed + 30,
    )

    half = len(ordered_days) // 2
    first_days, second_days = ordered_days[:half], ordered_days[half:]
    first_ic = _mean([daily_ic_from_ranks(rows[d]) for d in first_days])
    second_ic = _mean([daily_ic_from_ranks(rows[d]) for d in second_days])

    # ---- Task 6. Fire the verdict, once. ---------------------------------
    if primary.beats_coin and primary.beats_best_baseline:
        verdict_row = "beats coin and beats every baseline at the bar"
        text = (
            "conditional phase C.1 authorized on the frontier trio, each on its own "
            "post-cutoff window, labelled a large-effect screen"
        )
        c1 = True
    elif primary.beats_coin:
        verdict_row = "beats coin, does not beat the baselines"
        text = "an expensive wrapper for a subtraction. No phase. Finding recorded."
        c1 = False
    else:
        verdict_row = "does not beat coin"
        text = (
            "the replication confirms the council negative under frontier capability "
            "and sane formulation. Closed."
        )
        c1 = False

    return B2Result(
        amendment_zero_prior=prior,
        gate_passed=True,
        gate=gate,
        primary=primary,
        secondary=secondary,
        permutation_null=perm,
        permutation_p=permutation_p,
        first_half_ic=first_ic,
        second_half_ic=second_ic,
        first_half_days=len(first_days),
        second_half_days=len(second_days),
        verdict_row=verdict_row,
        verdict_text=text,
        c1_authorized=c1,
        stopped_reason="",
    )
