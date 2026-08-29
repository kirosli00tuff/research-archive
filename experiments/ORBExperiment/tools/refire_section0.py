"""A.1 TASK 10 — re-fire Section 0 on the measured inputs of this resumption.

`tools/fire_section0.py` is left untouched: it recorded the 2026-08-29
`PENDING_ACCESS` firing and is the artefact of that moment. This is a new tool
for a new firing, and both records sit in the same append-only ledger.

**Every input travels with its n**, and every one is a count-derived power, a
measured share, a measured count, or an operational verdict. **No outcome value
is read.**
"""

from __future__ import annotations

import json
import sys
from datetime import UTC, datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from _a1r import REPORTS, write_report  # noqa: E402
from orb.absence import AbsenceReason, Absent  # noqa: E402
from orb.access import CollectionAccess  # noqa: E402
from orb.config import CONFIG  # noqa: E402
from orb.ledger import AppendOnlyLedger  # noqa: E402
from orb.power import power_one_sided, sessions_for_power  # noqa: E402
from orb.redact import say  # noqa: E402
from orb.section0 import PowerInputs, Section0Verdict, fire_section0  # noqa: E402
from orb.verdict import alpha_adj  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
HOLDOUT_N = 875

CLOCK = (
    "the registered 14-calendar-day wait started 2026-08-29 and is eligible "
    "2026-09-12; A.1 TASK 9 sealed 480 files, 737,507 bars, 2,400 "
    "session-ticker pairs"
)
NO_AGREEMENT = (
    "A.1 TASK 4 measured the tape (SAME_TAPE, median 1.005197, n = 100 pairs); "
    "the registered first-5-minute high-or-low agreement share is a separate "
    "measurement and has not been made"
)


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

    delisted = json.loads(
        (REPORTS / "task6b_delisted_in_window.json").read_text(encoding="utf-8")
    )
    tape = json.loads((REPORTS / "task4_tape.json").read_text(encoding="utf-8"))
    reach = json.loads((REPORTS / "task5_reach.json").read_text(encoding="utf-8"))
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
            "before the revision and agreement measurements exist, and firing "
            "one would claim a measurement this repository does not hold."
        )
        return 78

    pair = next(
        c
        for c in tape["comparisons"]
        if c["comparison"] == "massive_vs_alpaca_sip"
    )
    record = {
        "kind": "section0_verdict",
        "fired_at": datetime.now(tz=UTC).isoformat(timespec="seconds"),
        "stage": "A.1 resumption TASK 10",
        "verdict": result.verdict.value,
        "clause": result.clause,
        "reason": result.reason,
        "inputs": {
            "alpha_adj": alpha,
            "sessions_achievable_holdout": HOLDOUT_N,
            "e1_power_at_registered_1_40": power.e1_power_at_registered,
            "e1_power_at_published_2_81": power.e1_power_at_published,
            "e1_min_n_for_80_at_registered": sessions_for_power(
                CONFIG.registered_sharpe_assumption, alpha, CONFIG.target_power
            ),
            "e2_power": "Absent(not_served): neither credential serves the "
            "pre-period carve-out; n = 2 credentials, 0 serving",
            "collection_access": access.value,
            "primary_vendor": "alpaca",
            "primary_earliest_served_session": primary["earliest_served_session"],
            "primary_reach_probes_n": primary["probes"],
            "in_sample_sessions_reachable": (
                f"{primary['in_sample_sessions_reachable']} of "
                f"{primary['in_sample_sessions_registered']}"
            ),
            "holdout_sessions_reachable": (
                f"{primary['holdout_sessions_reachable']} of "
                f"{primary['holdout_sessions_registered']}"
            ),
            "reference_vendor": "massive",
            "reference_earliest_served_session": reach["vendors"]["massive"][
                "earliest_served_session"
            ],
            "cross_vendor_overlap_start": reach_power["cross_vendor_overlap"][
                "cross_vendor_overlap_start"
            ],
            "cross_vendor_overlap_holdout_sessions": reach_power[
                "cross_vendor_overlap"
            ]["overlap_sessions_holdout"],
            "cross_vendor_overlap_in_sample_sessions": reach_power[
                "cross_vendor_overlap"
            ]["overlap_sessions_in_sample"],
            "tape_verdict": pair["verdict"],
            "tape_median_ratio": pair["median_ratio"],
            "tape_pairs_n": pair["pairs_with_volume_in_both"],
            "delisted_names_enumerated_in_window": delisted[
                "enumerated_inside_window"
            ],
            "delisted_names_with_intraday_history": delisted[
                "delisted_names_with_intraday_history"
            ],
            "delisted_checks_n": delisted["combined_in_window_checks"],
            "delisted_registered_verdict": delisted["registered_verdict"],
            "bar_revision_finding": f"Absent(not_yet_measured): {CLOCK}",
            "agreement_finding": f"Absent(not_yet_measured): {NO_AGREEMENT}",
            "probe_slice_sessions": probe["session_count"],
            "probe_slice_tickers": probe["ticker_count"],
            "probe_slice_pairs": probe["session_ticker_pairs"],
            "probe_slice_bars": probe["bars_stored"],
            "earliest_eligible_repull": probe["earliest_eligible_repull"],
        },
    }

    AppendOnlyLedger(ROOT / "data" / "state" / "section0.jsonl").append(record)
    write_report("task10_section0.json", record)

    say(f"SECTION 0 VERDICT: {result.verdict.value}  [{result.clause}]")
    say(f"  {result.reason}")
    say("")
    say("Inputs, each with its n:")
    for key, value in record["inputs"].items():  # type: ignore[attr-defined]
        say(f"  {key:<42} {value}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
