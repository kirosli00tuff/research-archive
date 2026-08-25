"""Section 0. The outcome map, committed before any call goes out.

Coverage decides this verdict and nothing else does. No statistic relating a
stored ranking to any outcome enters here, because Section 0 fires at the end
of B.1 and B.2 has not run.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from npd.callstate import CallState, is_eligible_state
from npd.config import CONFIG, Config


class Section0Verdict(str, Enum):
    GO = "GO"
    DEGRADED = "DEGRADED"
    BLOCKED = "BLOCKED"


@dataclass(frozen=True, slots=True)
class CoverageReport:
    counts: dict[CallState, int]
    eligible_days: int
    stored_days: int
    coverage: float
    window_clears_power_floor: bool
    verdict: Section0Verdict
    rationale: str


def coverage_of(counts: dict[CallState, int]) -> tuple[int, int, float]:
    """Stored days over eligible days.

    excluded_pre_cutoff never enters the denominator. It is sample composition,
    not a failure to collect. Every other state does enter, including
    model_failed, because a day the model could not answer is a day the sample
    does not have.
    """
    eligible = sum(n for st, n in counts.items() if is_eligible_state(st))
    stored = counts.get(CallState.STORED, 0)
    return stored, eligible, (stored / eligible if eligible else 0.0)


def fire(
    counts: dict[CallState, int],
    *,
    window_clears_power_floor: bool,
    cfg: Config = CONFIG,
) -> CoverageReport:
    """Fire Section 0's verdict on coverage alone."""
    stored, eligible, cov = coverage_of(counts)

    if not window_clears_power_floor:
        verdict = Section0Verdict.BLOCKED
        rationale = (
            f"the derived window falls under the power floor of "
            f"{cfg.min_trading_days} trading days. No verdict claimed."
        )
    elif cov >= cfg.coverage_go_floor:
        verdict = Section0Verdict.GO
        rationale = (
            f"{cov:.1%} of eligible days carry a stored, parseable ranking, "
            f"at or above the {cfg.coverage_go_floor:.0%} bar."
        )
    elif cov >= cfg.coverage_degraded_floor:
        verdict = Section0Verdict.DEGRADED
        rationale = (
            f"{cov:.1%} of eligible days carry a stored, parseable ranking. "
            f"B.2 proceeds with the achieved sample and states its recomputed "
            f"power beside the registered target."
        )
    else:
        verdict = Section0Verdict.BLOCKED
        rationale = (
            f"{cov:.1%} of eligible days carry a stored ranking, under the "
            f"{cfg.coverage_degraded_floor:.0%} bar. No verdict claimed."
        )

    return CoverageReport(
        counts=dict(counts),
        eligible_days=eligible,
        stored_days=stored,
        coverage=cov,
        window_clears_power_floor=window_clears_power_floor,
        verdict=verdict,
        rationale=rationale,
    )
