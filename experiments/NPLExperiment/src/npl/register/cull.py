"""The outcome-blind power cull and the per-hypothesis Section 0 analog.

This module is pure arithmetic over counts, rates, and registered
probabilities — it is structurally incapable of reaching sealed data (no
path, no file API, no parser; pinned against its parse tree by test), and
the registered true shares it consumes are generating-sample-derived
assumptions, never successor measurements.

The registered rules, fixed before any successor measurement:

- alpha_h = 1 - family_confidence^(1/k), k = the surviving hypotheses.
- The cull runs to the k/alpha fixed point: starting from every registered
  hypothesis, any hypothesis whose required co-primary power at the
  achievable N by the projection deadline falls under the 0.50 floor at the
  current alpha_h fires BLOCKED and is removed; alpha_h is recomputed and
  the pass repeats. Power weakly increases as k falls (alpha_h grows), so a
  removal is final and the iteration terminates.
- Requirement modes, registered per hypothesis: H2 and H3 require every
  co-primary (the weakest governs); H4's grid is disjunctive within the
  hypothesis (Sidak-corrected), so its best cell governs.
- Exactly 0.50 survives the cull ("under 50 percent" fires BLOCKED); the
  boundary fixture in tests sits on it.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

from npl.config import CONFIG, Config
from npl.power import exact_power, min_n_for_power
from npl.register.conditioning import sidak_within, threshold_cells

SpecKey = tuple[str, str]

# Registered requirement mode per hypothesis: "all" = every co-primary is
# required (the weakest governs); "any" = the grid is disjunctive and the
# best cell governs (H4, Sidak-corrected within).
REQUIREMENT_MODE: dict[str, str] = {"H2": "all", "H3": "all", "H4": "any"}


def alpha_h(k: int, cfg: Config = CONFIG) -> float:
    """The familywise split: 1 - family_confidence^(1/k)."""
    if k < 1:
        raise ValueError(f"alpha_h needs at least one surviving hypothesis, got k={k}")
    return 1.0 - float(cfg.family_confidence ** (1.0 / k))


@dataclass(frozen=True, slots=True)
class CoPrimarySpec:
    """One registered co-primary: its null, its governing true share, and
    the reported-beside share where the registration names an honest range."""

    hypothesis: str
    name: str
    p0: float
    p_true_governing: float
    p_true_reported: float | None
    sidak_m: int


def register_specs(cfg: Config = CONFIG) -> tuple[CoPrimarySpec, ...]:
    """Every co-primary of every registered successor hypothesis."""
    specs: list[CoPrimarySpec] = [
        CoPrimarySpec("H2", "E1", 0.5, cfg.h2_e1_true_share, None, 1),
        # Amendment H2-3 Change 2: the governing share is the interpolated
        # 1x-floor figure; the old 2x-floor 0.60 rides beside it as the
        # reported figure, so the cost of the weakening stays legible.
        CoPrimarySpec(
            "H2", "E2", 0.5, cfg.h2_e2_true_share, cfg.h2_e2_true_share_two_times_floor, 1
        ),
        CoPrimarySpec("H3", "P1", cfg.p1_bar, cfg.h3_share_positive_true, None, 1),
        CoPrimarySpec(
            "H3",
            "MAG",
            0.5,
            cfg.h3_magnitude_true_generating,
            cfg.h3_magnitude_true_h1_registered,
            1,
        ),
    ]
    cells = threshold_cells(cfg)
    specs.extend(
        CoPrimarySpec(
            "H4",
            cell.label,
            cfg.p1_bar,
            cfg.h4_true_share_generating,
            cfg.h4_true_share_h1_registered,
            len(cells),
        )
        for cell in cells
    )
    return tuple(specs)


@dataclass(frozen=True, slots=True)
class SpecPower:
    """One co-primary's exact power at one sample size and one alpha_h."""

    spec: CoPrimarySpec
    n: int
    alpha_h: float
    alpha_effective: float
    power_governing: float
    power_reported: float | None


def spec_power(spec: CoPrimarySpec, n: int, alpha_h_value: float) -> SpecPower:
    """Exact binomial power, Sidak-corrected within the hypothesis where
    the spec is one cell of a registered grid."""
    effective = sidak_within(alpha_h_value, spec.sidak_m) if spec.sidak_m > 1 else alpha_h_value
    return SpecPower(
        spec=spec,
        n=n,
        alpha_h=alpha_h_value,
        alpha_effective=effective,
        power_governing=exact_power(n, spec.p0, spec.p_true_governing, effective),
        power_reported=(
            exact_power(n, spec.p0, spec.p_true_reported, effective)
            if spec.p_true_reported is not None
            else None
        ),
    )


def min_n_statement(
    spec: CoPrimarySpec, alpha_h_value: float, target: float, n_max: int = 5000
) -> int | None:
    """The smallest n from which the governing power stays at or above target."""
    effective = sidak_within(alpha_h_value, spec.sidak_m) if spec.sidak_m > 1 else alpha_h_value
    return min_n_for_power(spec.p0, spec.p_true_governing, effective, target, n_max)


def required_power(powers: list[SpecPower], mode: str) -> float:
    """The governing figure for the cull: weakest under "all", best under "any"."""
    if not powers:
        raise ValueError("a hypothesis with no co-primary powers cannot be culled")
    governing = [p.power_governing for p in powers]
    if mode == "all":
        return min(governing)
    if mode == "any":
        return max(governing)
    raise ValueError(f"unregistered requirement mode {mode!r}")


@dataclass(frozen=True, slots=True)
class CullPass:
    """One fixed-point iteration: who was active, at what alpha, who fired."""

    k: int
    alpha_h: float
    required_by_hypothesis: dict[str, float]
    blocked: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class CullResult:
    """The fixed point: k, alpha_h, survivors, and every pass recorded."""

    k: int
    alpha_h: float | None
    survivors: tuple[str, ...]
    blocked: tuple[str, ...]
    passes: tuple[CullPass, ...]


def run_cull(
    specs: tuple[CoPrimarySpec, ...],
    deadline_n: dict[SpecKey, int],
    cfg: Config = CONFIG,
) -> CullResult:
    """The registered cull at the k/alpha fixed point, deadline N governing.

    deadline_n maps (hypothesis, co-primary name) to the achievable N by the
    projection deadline — events for subset legs, pairs for pair legs, the
    conditioned count for grid cells. A missing key is a loud refusal.
    """
    hypotheses = list(dict.fromkeys(spec.hypothesis for spec in specs))
    for spec in specs:
        if (spec.hypothesis, spec.name) not in deadline_n:
            raise ValueError(
                f"no deadline N for {spec.hypothesis}/{spec.name}; the cull refuses "
                f"to guess a sample size"
            )
    active = list(hypotheses)
    passes: list[CullPass] = []
    blocked_all: list[str] = []
    while active:
        k = len(active)
        a = alpha_h(k, cfg)
        required: dict[str, float] = {}
        for hypothesis in active:
            powers = [
                spec_power(spec, deadline_n[(spec.hypothesis, spec.name)], a)
                for spec in specs
                if spec.hypothesis == hypothesis
            ]
            required[hypothesis] = required_power(powers, REQUIREMENT_MODE[hypothesis])
        newly_blocked = tuple(h for h in active if required[h] < cfg.power_blocked_floor)
        passes.append(
            CullPass(k=k, alpha_h=a, required_by_hypothesis=required, blocked=newly_blocked)
        )
        if not newly_blocked:
            break
        blocked_all.extend(newly_blocked)
        active = [h for h in active if h not in newly_blocked]
    return CullResult(
        k=len(active),
        alpha_h=alpha_h(len(active), cfg) if active else None,
        survivors=tuple(active),
        blocked=tuple(blocked_all),
        passes=tuple(passes),
    )


class RegisterVerdict(StrEnum):
    GO = "GO"
    DEGRADED = "DEGRADED"
    BLOCKED = "BLOCKED"


@dataclass(frozen=True, slots=True)
class RegisterGate:
    """One hypothesis's Section 0 verdict, fired by function, inputs beside."""

    hypothesis: str
    verdict: RegisterVerdict
    governing_power: float
    alpha_h: float
    rationale: str
    collectors_armed: bool


def fire_hypothesis_section0(
    hypothesis: str,
    powers: list[SpecPower],
    alpha_h_value: float,
    cfg: Config = CONFIG,
) -> RegisterGate:
    """The registered per-hypothesis outcome map.

    GO: the required co-primary power reaches the 0.80 floor at the
    achievable N by the projection deadline. DEGRADED: between the floors,
    collection proceeds with recomputed power stated beside the target.
    BLOCKED: under the 0.50 floor — nothing armed for this hypothesis.
    """
    mode = REQUIREMENT_MODE[hypothesis]
    governing = required_power(powers, mode)
    if not 0.0 <= governing <= 1.0:
        raise ValueError(f"{hypothesis}: impossible power {governing!r}")
    if governing < cfg.power_blocked_floor:
        return RegisterGate(
            hypothesis=hypothesis,
            verdict=RegisterVerdict.BLOCKED,
            governing_power=governing,
            alpha_h=alpha_h_value,
            rationale=(
                f"the required co-primary reaches {governing:.3f} power at the achievable "
                f"N by {cfg.projection_deadline}, under the {cfg.power_blocked_floor:.2f} "
                f"floor. Nothing is armed for {hypothesis}. A BLOCKED here is a "
                f"documented answer, not a failure of process."
            ),
            collectors_armed=False,
        )
    if governing >= cfg.power_go_floor:
        return RegisterGate(
            hypothesis=hypothesis,
            verdict=RegisterVerdict.GO,
            governing_power=governing,
            alpha_h=alpha_h_value,
            rationale=(
                f"the required co-primaries reach {governing:.3f} power at the achievable "
                f"N by {cfg.projection_deadline}, at or above the {cfg.power_go_floor:.2f} "
                f"floor. Collectors are armed for {hypothesis}."
            ),
            collectors_armed=True,
        )
    return RegisterGate(
        hypothesis=hypothesis,
        verdict=RegisterVerdict.DEGRADED,
        governing_power=governing,
        alpha_h=alpha_h_value,
        rationale=(
            f"the required co-primary reaches {governing:.3f} power, between the "
            f"{cfg.power_blocked_floor:.2f} and {cfg.power_go_floor:.2f} floors. "
            f"Collection proceeds for {hypothesis}; recomputed power is stated beside "
            f"the registered {cfg.power_go_floor:.2f} target at every later reading."
        ),
        collectors_armed=True,
    )
