"""A.3 TASK 5 — re-fire Section 0 after the rescue pass.

The four earlier firing tools are **left untouched** as the artefacts of their
moments. This is a fifth tool for a fifth firing, and all five records sit in the
same append-only ledger at `data/state/section0.jsonl`.

**It fires on whatever the rescue criterion returned**, and it records the
outcome — `RESCUED_DEGRADED` or `NOT_RESCUED` — as an input field beside the
verdict, with the deciding number.

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
from orb.power import sessions_for_power
from orb.redact import say
from orb.section0 import PowerInputs, Section0Verdict, fire_section0
from orb.verdict import per_test_alpha

ROOT = Path(__file__).resolve().parent.parent
RESCUE = ROOT / "reports" / "stage_a3rescue"
HOLDOUT_N = 875

CLOCK = (
    "the registered 14-calendar-day wait started 2026-08-29 and is eligible "
    "2026-09-12; A.1 TASK 9 sealed 480 files, 737,507 bars on a feed confirmed "
    "by measurement to be consolidated"
)
NO_AGREEMENT = (
    "A.1 TASK 4 measured the tape (SAME_TAPE, median 1.005197, n = 100 pairs); "
    "the registered first-5-minute high-or-low agreement share is a separate "
    "measurement and has not been made"
)


def main() -> int:
    alpha = per_test_alpha()
    rescue = json.loads(
        (RESCUE / "task3_rescue_verdict.json").read_text(encoding="utf-8")
    )
    band = json.loads((RESCUE / "task2_slippage_band.json").read_text(encoding="utf-8"))
    by = {(r["assumption"], r["horizon"]): r for r in rescue["rows"]}
    reg = by[("REGISTERED_1.40", "holdout_875")]
    pub = by[("published_2.81", "holdout_875")]

    power = PowerInputs(
        e1_power_at_registered=float(reg["e1_power"]),
        e2_power_at_registered=float(reg["e2_power"]),
        e1_power_at_published=float(pub["e1_power"]),
        e2_power_at_published=float(pub["e2_power"]),
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
        say(f"REFUSING to record {result.verdict.value}.")
        return 78

    deciding = rescue["deciding_numbers"]
    record: dict[str, Any] = {
        "kind": "section0_verdict",
        "fired_at": datetime.now(tz=UTC).isoformat(timespec="seconds"),
        "stage": "A.3 rescue pass TASK 5",
        "verdict": result.verdict.value,
        "clause": result.clause,
        "reason": result.reason,
        "rescue_outcome": rescue["outcome"],
        "rescue_criterion_precommitted_on": rescue["criterion_precommitted_on"],
        "rescue_criterion_commit": rescue["criterion_commit"],
        "inputs": {
            "alpha_per_co_primary": alpha,
            "sessions_achievable_holdout": HOLDOUT_N,
            "e1_power_at_registered_1_40": power.e1_power_at_registered,
            "e1_power_at_published_2_81": power.e1_power_at_published,
            "e1_min_n_for_80_at_registered": sessions_for_power(
                CONFIG.registered_sharpe_assumption, alpha, CONFIG.target_power
            ),
            "e2_power_at_registered_1_40": power.e2_power_at_registered,
            "e2_power_at_published_2_81": power.e2_power_at_published,
            "e2_min_n_for_80_at_registered": reg["e2_min_sessions_for_80"],
            "joint_power_at_registered_1_40": reg["joint_power"],
            "joint_power_at_published_2_81": pub["joint_power"],
            "joint_min_n_for_80_at_registered": reg["joint_min_sessions_for_80"],
            "joint_binding_component": reg["joint_binding_component"],
            "measured_shift_usd_per_share": deciding["measured_shift_usd_per_share"],
            "carried_band_shift_usd_per_share": rescue["shift_before_and_after"][
                "carried_band_shift"
            ],
            "central_mean_at_registered_1_40": deciding[
                "central_mean_at_registered_1_40"
            ],
            "pessimistic_cost_mean_at_registered_1_40": deciding[
                "pessimistic_cost_mean_at_registered_1_40"
            ],
            "measured_band": band["measured_band"],
            "measured_band_against_carried": band["measured_against_carried"],
            "one_minute_resolution_caveat": band["one_minute_resolution_caveat"],
            "carve_out_caveat": rescue["carve_out_caveat"],
            "collection_access": access.value,
            "delisted_names_with_intraday_history": delisted[
                "delisted_names_with_intraday_history"
            ],
            "bar_revision_finding": f"Absent(not_yet_measured): {CLOCK}",
            "agreement_finding": f"Absent(not_yet_measured): {NO_AGREEMENT}",
            "earliest_eligible_repull": probe["earliest_eligible_repull"],
            "h1b_status": "REGISTERED_NOT_OPEN — it cannot and did not rescue H1",
        },
    }

    AppendOnlyLedger(ROOT / "data" / "state" / "section0.jsonl").append(record)
    write_report("task5_section0.json", record)
    RESCUE.mkdir(parents=True, exist_ok=True)
    (RESCUE / "task5_section0.json").write_text(
        json.dumps(record, indent=2, sort_keys=True), encoding="utf-8"
    )

    say(f"SECTION 0 VERDICT: {result.verdict.value}  [{result.clause}]")
    say(f"RESCUE OUTCOME:    {rescue['outcome']}")
    say(
        f"  measured shift {deciding['measured_shift_usd_per_share']:.6f} against a "
        f"central mean of {deciding['central_mean_at_registered_1_40']:.6f}"
    )
    say(
        f"  pessimistic-cost mean "
        f"{deciding['pessimistic_cost_mean_at_registered_1_40']:+.6f}; "
        f"E2 {power.e2_power_at_registered:.6f}; "
        f"JOINT {float(reg['joint_power']):.6f}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
