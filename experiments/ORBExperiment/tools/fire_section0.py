"""A.2 TASK 5 — fire Section 0, and record every input beside the verdict."""

from __future__ import annotations

import json
import sys
from datetime import UTC, datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from orb.absence import Absent, AbsenceReason  # noqa: E402
from orb.config import CONFIG  # noqa: E402
from orb.ledger import AppendOnlyLedger  # noqa: E402
from orb.power import power_one_sided, sessions_for_power  # noqa: E402
from orb.section0 import PowerInputs, fire_section0  # noqa: E402
from orb.verdict import alpha_adj  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
HOLDOUT_N = 875  # computed by orb.calendar at A.2 TASK 1, not taken from the prompt

NO_VENDOR = "A.1 TASK 1 measured 0 of 9 vendors serving a bar to this repository"


def main() -> int:
    alpha = alpha_adj()
    power = PowerInputs(
        e1_power_at_registered=power_one_sided(
            CONFIG.registered_sharpe_assumption, HOLDOUT_N, alpha
        ),
        e2_power_at_registered=0.0,
        e1_power_at_published=power_one_sided(
            CONFIG.published_sharpe_assumption, HOLDOUT_N, alpha
        ),
        e2_power_at_published=0.0,
        sessions_achievable=HOLDOUT_N,
    )

    revision = Absent(AbsenceReason.NOT_YET_MEASURED, NO_VENDOR)
    agreement = Absent(AbsenceReason.NOT_YET_MEASURED, NO_VENDOR)

    result = fire_section0(power, revision, agreement)

    counterfactual = fire_section0(
        power,
        __import__("orb.integrity", fromlist=["RevisionFinding"]).RevisionFinding(
            0.0, 100_000, 0, 2400, 0, 0, 0, 14
        ),
        __import__("orb.integrity", fromlist=["AgreementFinding"]).AgreementFinding(
            0.99, 2400, 95_000, 94_000, 250, 250
        ),
    )

    record = {
        "kind": "section0_verdict",
        "fired_at": datetime.now(tz=UTC).isoformat(timespec="seconds"),
        "verdict": result.verdict.value,
        "clause": result.clause,
        "reason": result.reason,
        "inputs": {
            "alpha_adj": alpha,
            "sessions_achievable": HOLDOUT_N,
            "e1_power_at_registered_1_40": power.e1_power_at_registered,
            "e1_power_at_published_2_81": power.e1_power_at_published,
            "e1_min_n_for_80_at_registered": sessions_for_power(
                CONFIG.registered_sharpe_assumption, alpha, CONFIG.target_power
            ),
            "e2_power": "Absent(not_yet_measured)",
            "bar_revision_finding": f"Absent(not_yet_measured): {NO_VENDOR}",
            "agreement_finding": f"Absent(not_yet_measured): {NO_VENDOR}",
        },
        "counterfactual_if_integrity_passed_in_full": {
            "verdict": counterfactual.verdict.value,
            "clause": counterfactual.clause,
        },
    }

    AppendOnlyLedger(ROOT / "data" / "state" / "section0.jsonl").append(record)
    out = ROOT / "reports" / "stage_a2" / "section0.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(record, indent=2, sort_keys=True), encoding="utf-8")

    print(f"SECTION 0 VERDICT: {result.verdict.value}  [{result.clause}]")
    print(f"  {result.reason}\n")
    print("Inputs, each with its n:")
    for k, v in record["inputs"].items():  # type: ignore[attr-defined]
        print(f"  {k:<34} {v}")
    print(
        f"\nCounterfactual, had bar integrity passed in full: "
        f"{counterfactual.verdict.value} [{counterfactual.clause}]"
    )
    print(f"\nwrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
