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

from orb.absence import AbsenceReason, Absent, Maybe
from orb.access import CollectionAccess
from orb.config import CONFIG
from orb.integrity import AgreementFinding, IntegrityVerdict, RevisionFinding


@unique
class Section0Verdict(StrEnum):
    GO = "GO"
    DEGRADED = "DEGRADED"
    BLOCKED = "BLOCKED"

    PENDING_ACCESS = "PENDING_ACCESS"
    """Registered by Amendment 1, 2026-08-29, while holding **zero** bar data.

    Fires when an integrity input does not exist because **no vendor is
    reachable**, which is a different state from an integrity input that was
    measured and failed. It **arms nothing** and it is **not a verdict on the
    hypothesis** — it is a verdict on this repository's access.

    Without it the map would have to treat a missing measurement as a failed
    one, which would close H1 as ``source-integrity-blocked`` on evidence that
    does not exist. Standing rule 5: absence is a recorded state, never a
    synthesized value.
    """

    PENDING_SPEND = "PENDING_SPEND"
    """Registered by Amendment 10, 2026-08-29.

    A credentialed vendor **serves bars**, and its **measured** historical reach
    does **not** cover the registered windows. The question is then a **costed
    operator decision**, not a design question and not a verdict on H1. **It arms
    nothing and it authorises no spend** — it hands over a decision.
    """

    PENDING_REVISION = "PENDING_REVISION"
    """Registered by Amendment 10, 2026-08-29.

    Access passes — a vendor serves, and its measured reach covers the registered
    windows — and an integrity measurement **still does not exist**, because the
    registered 14-calendar-day wait between the probe pull and its identical
    re-pull has not elapsed.

    **This is a legitimate parked outcome rather than a failure.** The wait *is*
    the measurement: a re-pull sent early measures a revision rate biased toward
    zero, and zero is the shape of a PASS. Distinguishing it from
    ``PENDING_ACCESS`` matters because the two have completely different next
    actions — one needs a credential, the other needs a calendar.
    """


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


DELISTED_UNMEASURED: Absent = Absent(
    AbsenceReason.NOT_YET_MEASURED, "delisted coverage has not been measured"
)
"""The default for the Amendment 10 delisted parameter. A recorded absence."""


def _missing(
    revision: Maybe[RevisionFinding], agreement: Maybe[AgreementFinding]
) -> list[str]:
    """Which integrity inputs are recorded absences, and why."""
    out: list[str] = []
    if isinstance(revision, Absent):
        out.append(f"bar revision ({revision.reason}: {revision.detail})")
    if isinstance(agreement, Absent):
        out.append(f"cross-vendor agreement ({agreement.reason}: {agreement.detail})")
    return out


def fire_section0(
    power: PowerInputs,
    revision: Maybe[RevisionFinding],
    agreement: Maybe[AgreementFinding],
    *,
    access: CollectionAccess = CollectionAccess.NO_VENDOR_SERVES,
    delisted_with_intraday: Maybe[int] = DELISTED_UNMEASURED,
) -> Section0Result:
    """Fire the registered outcome map. Pure, total, and order-fixed.

    **Amendment 1** put one clause ahead of every other: a recorded absence in
    either integrity input fires ``PENDING_ACCESS``, because a measurement that
    does not exist is never read as a measurement that failed.

    **Amendment 10** refines that ordering for a case Amendment 1 could not have
    contemplated — it was written while **no vendor served any bar at all**, so
    no BLOCKED input could be measured and the ordering was untestable in
    practice. Now a vendor serves, and one integrity input can be **measured**
    while another is **absent**. The refinement:

    - When ``access`` is ``NO_VENDOR_SERVES``, Amendment 1's clause stands
      **unchanged**: an absent integrity input fires ``PENDING_ACCESS`` ahead of
      everything.
    - When a vendor serves, a BLOCKED trigger whose input is **measured** fires
      ahead of the pending states, and a BLOCKED trigger whose input is
      **absent** is skipped. *"Evidence that does not exist"* was Amendment 1's
      objection, and it does not apply to evidence that does.

    ``delisted_with_intraday`` exists because the delisted count and the
    agreement share travel together in one record but are **measured at
    different times**. Without it, an absent agreement share would hide a
    measured delisted count, and a measured zero could not fire BLOCKED-3.
    """
    revision_found: RevisionFinding | None = (
        None if isinstance(revision, Absent) else revision
    )
    agreement_found: AgreementFinding | None = (
        None if isinstance(agreement, Absent) else agreement
    )
    revision_absent = revision_found is None
    agreement_absent = agreement_found is None

    # --- Amendment 1 clause, unchanged, for the no-vendor state --------
    if access is CollectionAccess.NO_VENDOR_SERVES and (
        revision_absent or agreement_absent
    ):
        return Section0Result(
            Section0Verdict.PENDING_ACCESS,
            "the integrity measurement this map fires on does not exist: "
            + "; ".join(_missing(revision, agreement))
            + ". Nothing is armed. This is a verdict on access, not on H1, and "
            "it is not a source-integrity closure — no bar has been served to "
            "fail.",
            "PENDING-ACCESS Amendment 1",
        )

    # The delisted count, resolved from whichever input carries it.
    delisted: int | None = None
    if agreement_found is not None:
        delisted = agreement_found.delisted_names_with_intraday_history
    elif not isinstance(delisted_with_intraday, Absent):
        delisted = delisted_with_intraday

    # --- BLOCKED triggers, in the registered order, on measured inputs -
    if power.e1_power_at_published < CONFIG.blocked_power_floor:
        return Section0Result(
            Section0Verdict.BLOCKED,
            f"E1 power {power.e1_power_at_published:.4f} at the published "
            f"magnitude ({CONFIG.published_sharpe_assumption} Sharpe) is below "
            f"the {CONFIG.blocked_power_floor} floor at n = "
            f"{power.sessions_achievable} achievable sessions.",
            "BLOCKED-1 power floor",
        )

    if revision_found is not None and revision_found.verdict() is IntegrityVerdict.FAIL:
        return Section0Result(
            Section0Verdict.BLOCKED,
            f"bar revision rate {revision_found.changed_bar_share:.4f} exceeds "
            f"{CONFIG.revision_partial_max_share} over n = "
            f"{revision_found.bars_compared} bars compared; the vendor rewrites "
            "history and no downstream figure can survive it.",
            "BLOCKED-2 bar integrity FAIL",
        )

    if delisted == 0:
        return Section0Result(
            Section0Verdict.BLOCKED,
            "zero delisted names served with intraday history across "
            f"{CONFIG.in_sample_start} to {CONFIG.holdout_end}; the universe "
            "would be survivor-only and unrecoverable after the fact.",
            "BLOCKED-3 zero delisted coverage",
        )

    if (
        agreement_found is not None
        and agreement_found.agreement_verdict() is IntegrityVerdict.FAIL
    ):
        return Section0Result(
            Section0Verdict.BLOCKED,
            "cross-vendor first-5-minute agreement "
            f"{agreement_found.first5_high_low_agreement_share:.4f} is below "
            f"{CONFIG.agreement_partial_min_share} over n = "
            f"{agreement_found.session_ticker_pairs_compared} session-ticker pairs; "
            "the top-20 selection is not reproducible across vendors.",
            "BLOCKED-4 selection not reproducible",
        )

    if delisted is not None and delisted < CONFIG.delisted_partial_min_count:
        return Section0Result(
            Section0Verdict.BLOCKED,
            f"only {delisted} delisted names served with intraday history, "
            f"below the {CONFIG.delisted_partial_min_count} floor.",
            "BLOCKED-5 delisted coverage FAIL",
        )

    # --- Amendment 10: a measured reach that does not cover the windows -
    if access is CollectionAccess.SERVING_REACH_SHORT:
        return Section0Result(
            Section0Verdict.PENDING_SPEND,
            "a credentialed vendor serves bars, and its measured historical "
            "reach does not cover the registered windows. Nothing is armed and "
            "no spend is authorised: this hands the operator a costed decision, "
            "and it is a verdict on reach, not on H1.",
            "PENDING-SPEND Amendment 10",
        )

    # --- Amendment 10: access passes, the clock has not run ------------
    if revision_absent or agreement_absent:
        return Section0Result(
            Section0Verdict.PENDING_REVISION,
            "access passes and the integrity measurement still does not exist: "
            + "; ".join(_missing(revision, agreement))
            + ". Nothing is armed. The registered "
            f"{CONFIG.revision_repull_wait_days}-calendar-day wait between the "
            "probe pull and its identical re-pull has not elapsed, and that "
            "wait is the measurement — a re-pull sent early measures a revision "
            "rate biased toward zero, and zero is the shape of a PASS. This is "
            "a parked outcome, not a failure, and it is not a "
            "source-integrity closure.",
            "PENDING-REVISION Amendment 10",
        )

    assert revision_found is not None and agreement_found is not None
    revision_verdict = revision_found.verdict()
    agreement_verdict = agreement_found.verdict()

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
            f"full (revision {revision_found.changed_bar_share:.4f} over n = "
            f"{revision_found.bars_compared} bars; agreement "
            f"{agreement_found.first5_high_low_agreement_share:.4f} over n = "
            f"{agreement_found.session_ticker_pairs_compared} pairs), and delisted "
            f"coverage passes at {delisted} names.",
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
            f"{revision_found.changed_bar_share:.4f} over n = "
            f"{revision_found.bars_compared} bars"
        )
    if agreement_verdict is IntegrityVerdict.PARTIAL:
        causes.append(
            "cross-vendor or delisted coverage PARTIAL at agreement "
            f"{agreement_found.first5_high_low_agreement_share:.4f} over n = "
            f"{agreement_found.session_ticker_pairs_compared} pairs and "
            f"{delisted} delisted names"
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
