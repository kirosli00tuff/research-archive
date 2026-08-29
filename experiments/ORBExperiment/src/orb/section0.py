"""Section 0 — the outcome map. It judges feasibility, integrity and power.

**It reads no outcome value.** Every input is a count-derived power, a measured
share, a measured count, or an operational verdict.

Precedence is fixed and is evaluated in the order written: the BLOCKED triggers
first, then GO, and **DEGRADED is the residual**. A BLOCKED trigger fires even
at perfect power, because a design that cannot trust its own bars is not
rescued by sample size.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum, unique
from typing import final

from orb.config import CONFIG
from orb.integrity import AgreementFinding, IntegrityVerdict, RevisionFinding


@unique
class Section0Verdict(StrEnum):
    GO = "GO"
    DEGRADED = "DEGRADED"
    BLOCKED = "BLOCKED"


@final
@dataclass(frozen=True, slots=True)
class PowerInputs:
    """Powers computed at A.2 TASK 4. Count-derived; no outcome is read."""

    e1_power_at_registered: float
    e2_power_at_registered: float
    e1_power_at_published: float
    e2_power_at_published: float
    sessions_achievable: int


@final
@dataclass(frozen=True, slots=True)
class Section0Result:
    verdict: Section0Verdict
    reason: str
    clause: str

    def __str__(self) -> str:
        return f"{self.verdict} [{self.clause}] {self.reason}"


def fire_section0(
    power: PowerInputs,
    revision: RevisionFinding,
    agreement: AgreementFinding,
) -> Section0Result:
    """Fire the registered outcome map. Pure, total, and order-fixed."""
    revision_verdict = revision.verdict()
    agreement_verdict = agreement.verdict()

    # --- BLOCKED triggers, evaluated first and in the order written ----
    if power.e1_power_at_published < CONFIG.blocked_power_floor:
        return Section0Result(
            Section0Verdict.BLOCKED,
            f"E1 power {power.e1_power_at_published:.4f} at the published "
            f"magnitude ({CONFIG.published_sharpe_assumption} Sharpe) is below "
            f"the {CONFIG.blocked_power_floor} floor at n = "
            f"{power.sessions_achievable} achievable sessions.",
            "BLOCKED-1 power floor",
        )

    if revision_verdict is IntegrityVerdict.FAIL:
        return Section0Result(
            Section0Verdict.BLOCKED,
            f"bar revision rate {revision.changed_bar_share:.4f} exceeds "
            f"{CONFIG.revision_partial_max_share} over n = "
            f"{revision.bars_compared} bars compared; the vendor rewrites "
            "history and no downstream figure can survive it.",
            "BLOCKED-2 bar integrity FAIL",
        )

    if agreement.delisted_names_with_intraday_history == 0:
        return Section0Result(
            Section0Verdict.BLOCKED,
            "zero delisted names served with intraday history across "
            f"{CONFIG.in_sample_start} to {CONFIG.holdout_end}; the universe "
            "would be survivor-only and unrecoverable after the fact.",
            "BLOCKED-3 zero delisted coverage",
        )

    if agreement.agreement_verdict() is IntegrityVerdict.FAIL:
        return Section0Result(
            Section0Verdict.BLOCKED,
            "cross-vendor first-5-minute agreement "
            f"{agreement.first5_high_low_agreement_share:.4f} is below "
            f"{CONFIG.agreement_partial_min_share} over n = "
            f"{agreement.session_ticker_pairs_compared} session-ticker pairs; "
            "the top-20 selection is not reproducible across vendors.",
            "BLOCKED-4 selection not reproducible",
        )

    if agreement.delisted_verdict() is IntegrityVerdict.FAIL:
        return Section0Result(
            Section0Verdict.BLOCKED,
            f"only {agreement.delisted_names_with_intraday_history} delisted "
            f"names served with intraday history, below the "
            f"{CONFIG.delisted_partial_min_count} floor.",
            "BLOCKED-5 delisted coverage FAIL",
        )

    # --- GO -----------------------------------------------------------
    powers_pass = (
        power.e1_power_at_registered >= CONFIG.target_power
        and power.e2_power_at_registered >= CONFIG.target_power
    )
    integrity_full = (
        revision_verdict is IntegrityVerdict.PASS
        and agreement_verdict is IntegrityVerdict.PASS
    )
    if powers_pass and integrity_full:
        return Section0Result(
            Section0Verdict.GO,
            f"both co-primaries reach {CONFIG.target_power} power at the "
            f"registered {CONFIG.registered_sharpe_assumption} Sharpe "
            f"assumption (E1 {power.e1_power_at_registered:.4f}, E2 "
            f"{power.e2_power_at_registered:.4f}) at n = "
            f"{power.sessions_achievable} sessions, bar integrity passes in "
            f"full (revision {revision.changed_bar_share:.4f} over n = "
            f"{revision.bars_compared} bars; agreement "
            f"{agreement.first5_high_low_agreement_share:.4f} over n = "
            f"{agreement.session_ticker_pairs_compared} pairs), and delisted "
            f"coverage passes at {agreement.delisted_names_with_intraday_history} "
            "names.",
            "GO",
        )

    # --- DEGRADED, the residual ---------------------------------------
    causes: list[str] = []
    if not powers_pass:
        if power.e1_power_at_published >= CONFIG.target_power:
            causes.append(
                f"E1 reaches {CONFIG.target_power} power at the published "
                f"magnitude ({power.e1_power_at_published:.4f}) but not at the "
                f"registered assumption ({power.e1_power_at_registered:.4f})"
            )
        else:
            causes.append(
                "E1 power at the published magnitude "
                f"({power.e1_power_at_published:.4f}) sits in the registered "
                f"residual band between the {CONFIG.blocked_power_floor} "
                f"BLOCKED floor and the {CONFIG.target_power} GO floor"
            )
        if power.e2_power_at_registered < CONFIG.target_power:
            causes.append(
                f"E2 power at the registered assumption is "
                f"{power.e2_power_at_registered:.4f}"
            )
    if revision_verdict is IntegrityVerdict.PARTIAL:
        causes.append(
            f"bar integrity PARTIAL at revision share "
            f"{revision.changed_bar_share:.4f} over n = "
            f"{revision.bars_compared} bars"
        )
    if agreement_verdict is IntegrityVerdict.PARTIAL:
        causes.append(
            "cross-vendor or delisted coverage PARTIAL at agreement "
            f"{agreement.first5_high_low_agreement_share:.4f} over n = "
            f"{agreement.session_ticker_pairs_compared} pairs and "
            f"{agreement.delisted_names_with_intraday_history} delisted names"
        )

    return Section0Result(
        Section0Verdict.DEGRADED,
        "; ".join(causes)
        + ". Collection proceeds under the registered narrowing: a later FAIL "
        "establishes that the effect is not present at its published "
        "magnitude, and cannot distinguish a decayed effect from no effect at "
        "all.",
        "DEGRADED residual",
    )
