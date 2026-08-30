"""A.2 TASK 6 (inference repair) — re-fire Section 0 on the corrected inference.

The three earlier firing tools are **left untouched** as the artefacts of their
moments. This is a fourth tool for a fourth firing, and all four records sit in
the same append-only ledger at `data/state/section0.jsonl`.

**What is new since the last firing:** the corrected `alpha = 0.05` (Amendment
18), the amended economic E2 (Amendment 19), the measured stop-exit share and
ambiguous rate (Amendment 20), and the **joint power** figure that Section 10.1
makes the latch condition (Amendment 21).

**Two questions are recorded separately, because they have different answers and
the verdict must not conflate them:** whether the corrected alpha alone moves E1
across its 80 percent bar, and whether **joint** power does.

**The expected landing is `PENDING_REVISION`**, because both integrity inputs
remain recorded absences ineligible before 2026-09-12. The tool **refuses to
record `GO` or `DEGRADED`** and exits 78 if the map ever hands it one.
"""

from __future__ import annotations

import json
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))

from _a1r import REPORTS, write_report

from orb.absence import AbsenceReason, Absent
from orb.access import CollectionAccess
from orb.config import CONFIG
from orb.ledger import AppendOnlyLedger
from orb.power import power_one_sided, sessions_for_power
from orb.redact import say
from orb.section0 import PowerInputs, Section0Verdict, fire_section0
from orb.verdict import alpha_adj, per_test_alpha

ROOT = Path(__file__).resolve().parent.parent
REPAIR = ROOT / "reports" / "stage_a2repair"
HOLDOUT_N = 875
IN_SAMPLE_N = 1762

CLOCK = (
    "the registered 14-calendar-day wait started 2026-08-29 and is eligible "
    "2026-09-12; A.1 TASK 9 sealed 480 files, 737,507 bars, 2,400 "
    "session-ticker pairs on a feed confirmed by measurement to be consolidated"
)
NO_AGREEMENT = (
    "A.1 TASK 4 measured the tape (SAME_TAPE, median 1.005197, n = 100 pairs); "
    "the registered first-5-minute high-or-low agreement share is a separate "
    "measurement and has not been made"
)


def main() -> int:
    alpha = per_test_alpha()
    superseded = alpha_adj()
    jp = json.loads((REPAIR / "task4_joint_power.json").read_text(encoding="utf-8"))
    mix = json.loads((REPAIR / "task3_execution_mix.json").read_text(encoding="utf-8"))
    by = {(r["assumption"], r["horizon"]): r for r in jp["rows"]}
    reg = by[("REGISTERED_1.40", "holdout_875")]
    pub = by[("published_2.81", "holdout_875")]

    power = PowerInputs(
        e1_power_at_registered=float(reg["e1_power_at_0_05"]),
        e2_power_at_registered=float(reg["e2_power_at_0_05"]),
        e1_power_at_published=float(pub["e1_power_at_0_05"]),
        e2_power_at_published=float(pub["e2_power_at_0_05"]),
        sessions_achievable=HOLDOUT_N,
    )

    delisted = json.loads(
        (REPORTS / "task6b_delisted_in_window.json").read_text(encoding="utf-8")
    )
    reach_power = json.loads(
        (REPORTS / "task5_reach_power.json").read_text(encoding="utf-8")
    )
    probe = json.loads(
        (REPORTS / "task9_probe_manifest.json").read_text(encoding="utf-8")
    )
    primary = next(v for v in reach_power["vendors"] if v["vendor"] == "alpaca")
    access = (
        CollectionAccess.SERVING_FULL_REACH
        if primary["covers_in_sample_opening"] and primary["covers_holdout_opening"]
        else CollectionAccess.SERVING_REACH_SHORT
    )

    result = fire_section0(
        power,
        Absent(AbsenceReason.NOT_YET_MEASURED, CLOCK),
        Absent(AbsenceReason.NOT_YET_MEASURED, NO_AGREEMENT),
        access=access,
        delisted_with_intraday=delisted["delisted_names_with_intraday_history"],
    )
    if result.verdict in {Section0Verdict.GO, Section0Verdict.DEGRADED}:
        say(
            f"REFUSING to record {result.verdict.value}: neither is reachable "
            "before the revision and agreement measurements exist."
        )
        return 78

    e1_old = power_one_sided(CONFIG.registered_sharpe_assumption, HOLDOUT_N, superseded)
    e1_new = power.e1_power_at_registered
    alpha_moves_e1 = e1_old < CONFIG.target_power <= e1_new
    joint_clears = float(reg["joint_power_upper_bound"]) >= CONFIG.target_power

    record: dict[str, Any] = {
        "kind": "section0_verdict",
        "fired_at": datetime.now(tz=UTC).isoformat(timespec="seconds"),
        "stage": "A.2 inference repair TASK 6",
        "verdict": result.verdict.value,
        "clause": result.clause,
        "reason": result.reason,
        "two_questions_kept_apart": {
            "does_the_corrected_alpha_alone_move_E1_across_its_80_percent_bar": (
                alpha_moves_e1
            ),
            "e1_at_registered_before_and_after": [e1_old, e1_new],
            "e1_min_sessions_before_and_after": [
                sessions_for_power(
                    CONFIG.registered_sharpe_assumption, superseded, CONFIG.target_power
                ),
                sessions_for_power(
                    CONFIG.registered_sharpe_assumption, alpha, CONFIG.target_power
                ),
            ],
            "does_JOINT_power_clear_its_80_percent_bar": joint_clears,
            "joint_power_at_registered_holdout": reg["joint_power_upper_bound"],
            "joint_min_sessions_for_80_at_registered": reg["joint_min_sessions_for_80"],
            "these_are_different_questions": (
                "Correcting the multiplicity error made E1 powered and left the "
                "DESIGN unpowered. Both are true. Reporting either without the "
                "other would misdescribe this repository."
            ),
        },
        "inputs": {
            "alpha_per_co_primary": alpha,
            "alpha_superseded": superseded,
            "alpha_correction": (
                "Amendment 18: Section 8's rule is a conjunction, an "
                "intersection-union test, and Berger 1982 gives each component "
                "the full nominal level. The union correction was not owed."
            ),
            "sessions_achievable_holdout": HOLDOUT_N,
            "sessions_in_sample": IN_SAMPLE_N,
            "e1_power_at_registered_1_40": e1_new,
            "e1_power_at_published_2_81": power.e1_power_at_published,
            "e1_min_n_for_80_at_registered": sessions_for_power(
                CONFIG.registered_sharpe_assumption, alpha, CONFIG.target_power
            ),
            "e2_null": (
                "Amendment 19: mean net PnL per trade above zero at the "
                "PESSIMISTIC end of the registered Section 6 slippage band"
            ),
            "e2_power_at_registered_1_40": power.e2_power_at_registered,
            "e2_power_at_published_2_81": power.e2_power_at_published,
            "e2_min_n_for_80_at_registered": reg["e2_min_sessions_for_80"],
            "e2_pessimistic_mean_at_registered": reg["pessimistic_mean_usd_per_share"],
            "e2_central_mean_at_registered": reg["central_mean_usd_per_share"],
            "measured_pessimistic_shift_usd_per_share": mix[
                "mean_pessimistic_shift_usd_per_share"
            ],
            "measured_stop_exit_share": mix["stop_exit_share"],
            "measured_stop_exit_share_n": mix["trades_with_a_resolved_exit"],
            "measured_ambiguous_rate": mix["ambiguous_rate"],
            "measured_ambiguous_rate_n": mix["name_sessions_evaluated"],
            "measured_ambiguous_rate_upper_bound_rule_of_three": (
                3 / mix["name_sessions_evaluated"]
            ),
            "e2_dispersion_usd_per_share": jp["dispersion_usd_per_share"],
            "joint_power_at_registered_holdout": reg["joint_power_upper_bound"],
            "joint_power_at_published_holdout": pub["joint_power_upper_bound"],
            "joint_binding_component": reg["joint_binding_component"],
            "latch_condition": (
                "Section 10.1, Amendment 21: JOINT power at or above 0.80. "
                "Neither component power alone satisfies clause 1."
            ),
            "observation_not_a_branch_change": (
                "BLOCKED-1 is registered on E1 power at the PUBLISHED magnitude "
                "against the 0.50 floor, and E1 at 2.81 is "
                f"{power.e1_power_at_published:.6f}, so it does not fire. Recorded "
                "for the operator and NOT acted on: had BLOCKED-1 been defined on "
                "JOINT power at the REGISTERED assumption it would fire, because "
                f"that figure is {reg['joint_power_upper_bound']:.6f}. This pass "
                "does not change the branch."
            ),
            "carve_out_caveat": jp["carve_out_caveat"],
            "scope_limitation_sl3": (
                "REGISTRATION.md §11.1 SL-3: all 1,762 in-sample sessions rest "
                "on a single unverified feed."
            ),
            "hypothesis_restated": (
                "REGISTRATION.md §1.1, Amendment 22: the breakout is a DIRECTION "
                "rule, not a selector. Measured trigger rate 0.982143, n = 560."
            ),
            "collection_access": access.value,
            "delisted_names_with_intraday_history": delisted[
                "delisted_names_with_intraday_history"
            ],
            "delisted_checks_n": delisted["combined_in_window_checks"],
            "bar_revision_finding": f"Absent(not_yet_measured): {CLOCK}",
            "agreement_finding": f"Absent(not_yet_measured): {NO_AGREEMENT}",
            "earliest_eligible_repull": probe["earliest_eligible_repull"],
        },
    }

    AppendOnlyLedger(ROOT / "data" / "state" / "section0.jsonl").append(record)
    write_report("task6c_section0.json", record)
    REPAIR.mkdir(parents=True, exist_ok=True)
    (REPAIR / "task6_section0.json").write_text(
        json.dumps(record, indent=2, sort_keys=True), encoding="utf-8"
    )

    say(f"SECTION 0 VERDICT: {result.verdict.value}  [{result.clause}]")
    say(f"  {result.reason}")
    say("")
    say("The two questions, kept apart:")
    say(
        f"  corrected alpha alone moves E1 across 0.80? {alpha_moves_e1} "
        f"({e1_old:.6f} -> {e1_new:.6f}, min n "
        f"{record['two_questions_kept_apart']['e1_min_sessions_before_and_after']})"
    )
    say(
        f"  JOINT power clears 0.80?                    {joint_clears} "
        f"({float(reg['joint_power_upper_bound']):.6f}, min n "
        f"{reg['joint_min_sessions_for_80']})"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
