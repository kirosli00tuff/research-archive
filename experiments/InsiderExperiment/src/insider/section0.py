"""Section 0. The two gates, committed before Task 4 computes anything.

Neither gate reads a first moment. The corpus gate reads counts. The power gate
reads a minimum detectable effect, which is built from a dispersion and a
sample size and from nothing else. NPDExperiment learned its design could not
have detected an effect anywhere in the literature's range after 415 days of
collection, in the same session that read the result. These bars fire first.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

from insider.config import CONFIG, Config


class PowerVerdict(StrEnum):
    GO = "GO"
    DEGRADED = "DEGRADED"
    BLOCKED = "BLOCKED"


class CorpusVerdict(StrEnum):
    CORPUS_GO = "CORPUS-GO"
    CORPUS_BLOCKED = "CORPUS-BLOCKED"


@dataclass(frozen=True, slots=True)
class PowerGate:
    mde_bp_per_month: float
    verdict: PowerVerdict
    rationale: str
    stage_b_authorized: bool


@dataclass(frozen=True, slots=True)
class CorpusGate:
    edgar_reachable: bool
    qualifying_events: int
    session_coverage: float
    verdict: CorpusVerdict
    rationale: str


def fire_power_gate(mde_bp_per_month: float, cfg: Config = CONFIG) -> PowerGate:
    """Fire the registered power verdict on the minimum detectable effect alone."""
    if not (mde_bp_per_month == mde_bp_per_month) or mde_bp_per_month <= 0:
        raise ValueError("a minimum detectable effect must be a positive finite number")

    if mde_bp_per_month <= cfg.mde_go_ceiling_bp:
        return PowerGate(
            mde_bp_per_month=mde_bp_per_month,
            verdict=PowerVerdict.GO,
            rationale=(
                f"the minimum detectable effect is {mde_bp_per_month:.2f} bp per month, at or "
                f"below the {cfg.mde_go_ceiling_bp:.0f} bp bar. The design resolves the decayed "
                f"effect band with margin. Stage B is authorized."
            ),
            stage_b_authorized=True,
        )
    if mde_bp_per_month <= cfg.mde_degraded_ceiling_bp:
        return PowerGate(
            mde_bp_per_month=mde_bp_per_month,
            verdict=PowerVerdict.DEGRADED,
            rationale=(
                f"the minimum detectable effect is {mde_bp_per_month:.2f} bp per month, between "
                f"the {cfg.mde_go_ceiling_bp:.0f} and {cfg.mde_degraded_ceiling_bp:.0f} bp bars. "
                f"The design resolves the top of the decayed gross band but likely not the net "
                f"residual after a {cfg.round_trip_bp_low:.0f} to {cfg.round_trip_bp_high:.0f} bp "
                f"round trip. Stage B is authorized only if the registration records, before B "
                f"runs, that a gross-detectable net-undetectable outcome is a registered verdict "
                f"row and not a disappointment."
            ),
            stage_b_authorized=True,
        )
    return PowerGate(
        mde_bp_per_month=mde_bp_per_month,
        verdict=PowerVerdict.BLOCKED,
        rationale=(
            f"the minimum detectable effect is {mde_bp_per_month:.2f} bp per month, above the "
            f"{cfg.mde_degraded_ceiling_bp:.0f} bp bar. The design cannot detect an effect "
            f"anywhere in the range the literature reports. Stage B is never written and the "
            f"repo closes on the finding."
        ),
        stage_b_authorized=False,
    )


def fire_corpus_gate(
    *,
    edgar_reachable: bool,
    qualifying_events: int,
    session_coverage: float,
    cfg: Config = CONFIG,
) -> CorpusGate:
    """Fire the registered corpus verdict on access and counts alone."""
    if not edgar_reachable:
        return CorpusGate(
            edgar_reachable=False,
            qualifying_events=qualifying_events,
            session_coverage=session_coverage,
            verdict=CorpusVerdict.CORPUS_BLOCKED,
            rationale="EDGAR access failed. No corpus was built. Record and stop.",
        )
    if qualifying_events < cfg.corpus_event_floor:
        return CorpusGate(
            edgar_reachable=True,
            qualifying_events=qualifying_events,
            session_coverage=session_coverage,
            verdict=CorpusVerdict.CORPUS_BLOCKED,
            rationale=(
                f"{qualifying_events} qualifying events survive the ex-ante filters, under the "
                f"registered floor of {cfg.corpus_event_floor}. Record and stop."
            ),
        )
    if session_coverage < cfg.corpus_coverage_floor:
        return CorpusGate(
            edgar_reachable=True,
            qualifying_events=qualifying_events,
            session_coverage=session_coverage,
            verdict=CorpusVerdict.CORPUS_BLOCKED,
            rationale=(
                f"{qualifying_events} qualifying events clear the count floor but only "
                f"{session_coverage:.1%} of in-span sessions carry a non-empty book, under the "
                f"registered {cfg.corpus_coverage_floor:.0%} floor. A book that is empty on most "
                f"days has no calendar-time series to measure. Record and stop."
            ),
        )
    return CorpusGate(
        edgar_reachable=True,
        qualifying_events=qualifying_events,
        session_coverage=session_coverage,
        verdict=CorpusVerdict.CORPUS_GO,
        rationale=(
            f"the EDGAR pipeline builds and {qualifying_events} qualifying events exceed the "
            f"registered floor of {cfg.corpus_event_floor}, with {session_coverage:.1%} of "
            f"in-span sessions carrying a non-empty book."
        ),
    )
