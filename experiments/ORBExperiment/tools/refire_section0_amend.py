"""A.2 TASK 6 (amendment pass) — re-fire Section 0 with E2 power as a number.

`tools/fire_section0.py` and `tools/refire_section0.py` are **left untouched**:
they are the artefacts of the `PENDING_ACCESS` and `PENDING_REVISION` firings of
2026-08-29, and this is a new tool for a new firing. All three records sit in the
same append-only ledger.

**What changed since the last firing, and what did not.**

- **E2 power is a number**, computed at A.1 TASK 5 of this pass from a dispersion
  measured on the post-holdout half of the amended carve-out. It was
  `Absent(not_served)`.
- **E1 is unchanged.** 0.7435 at the registered 1.40 Sharpe assumption on
  `n = 875` achievable holdout sessions, against a minimum 1,006 for 80 percent
  power. **This tool must not present it as changed**, so it recomputes it from
  the same inputs and records both figures.
- **The bar revision rate and the cross-vendor agreement share still do not
  exist**, and neither is eligible before **2026-09-12**.

**The expected landing is `PENDING_REVISION` again**, and the tool **refuses to
record `GO` or `DEGRADED`** — firing either would claim an integrity measurement
this repository does not hold.
"""

from __future__ import annotations

import json
import sys
from datetime import UTC, datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from _a1r import REPORTS, write_report

from orb.absence import AbsenceReason, Absent
from orb.access import CollectionAccess
from orb.config import CONFIG
from orb.ledger import AppendOnlyLedger
from orb.power import power_one_sided, sessions_for_power
from orb.redact import say
from orb.section0 import PowerInputs, Section0Verdict, fire_section0
from orb.verdict import alpha_adj

ROOT = Path(__file__).resolve().parent.parent
HOLDOUT_N = 875
IN_SAMPLE_N = 1762

CLOCK = (
    "the registered 14-calendar-day wait started 2026-08-29 and is eligible "
    "2026-09-12; A.1 TASK 9 sealed 480 files, 737,507 bars, 2,400 "
    "session-ticker pairs, and A.0 TASK 3 confirmed by measurement that the "
    "slice was pulled on the consolidated tape"
)
NO_AGREEMENT = (
    "A.1 TASK 4 measured the tape (SAME_TAPE, median 1.005197, n = 100 pairs); "
    "the registered first-5-minute high-or-low agreement share is a separate "
    "measurement and has not been made"
)
CARVE_OUT_CAVEAT = (
    "Amendment 11: the E2 dispersion input comes from a POST-HOLDOUT regime "
    "(2026-07-01 to 2026-08-28), later than the sample it is applied to. "
    "Neither direction is neutral; the compromise now runs forward rather than "
    "backward, and this figure may misstate in-sample dispersion in either "
    "direction by an amount this repository has not measured and does not "
    "claim to bound."
)
COLLECTION_NOT_A_READ = (
    "Storing bars is not reading them. The A.1 TASK 9 probe slice overlaps the "
    "holdout from 2026-05-05 to 2026-06-30; those bytes were stored by a sealed "
    "writer that parses nothing and were never handed to the universe, signal or "
    "verdict modules. That is COLLECTION, not a spent read. The Stage D latch "
    "continues to govern the holdout in full, it has not been written, and a "
    "second read of that window would void the hypothesis."
)


def main() -> int:
    alpha = alpha_adj()
    dispersion = json.loads(
        (REPORTS / "task5c_dispersion_e2.json").read_text(encoding="utf-8")
    )
    e2 = {
        (row["assumption"], row["horizon"]): row["e2_power"]
        for row in dispersion["e2_power_rows"]
    }
    e2_registered = float(e2[("REGISTERED_1.40", "holdout_875")])
    e2_published = float(e2[("published_2.81", "holdout_875")])

    power = PowerInputs(
        e1_power_at_registered=power_one_sided(
            CONFIG.registered_sharpe_assumption, HOLDOUT_N, alpha
        ),
        e2_power_at_registered=e2_registered,
        e1_power_at_published=power_one_sided(
            CONFIG.published_sharpe_assumption, HOLDOUT_N, alpha
        ),
        e2_power_at_published=e2_published,
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
    feed = json.loads(
        (REPORTS / "task3b_feed_confirmation.json").read_text(encoding="utf-8")
    )
    ceiling = json.loads(
        (REPORTS / "task4b_alpaca_ceiling.json").read_text(encoding="utf-8")
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
        c for c in tape["comparisons"] if c["comparison"] == "massive_vs_alpaca_sip"
    )
    record = {
        "kind": "section0_verdict",
        "fired_at": datetime.now(tz=UTC).isoformat(timespec="seconds"),
        "stage": "A.1 amendment pass TASK 6",
        "verdict": result.verdict.value,
        "clause": result.clause,
        "reason": result.reason,
        "storing_is_not_reading": COLLECTION_NOT_A_READ,
        "inputs": {
            "alpha_adj": alpha,
            "sessions_achievable_holdout": HOLDOUT_N,
            "sessions_in_sample": IN_SAMPLE_N,
            "e1_power_at_registered_1_40": power.e1_power_at_registered,
            "e1_power_at_published_2_81": power.e1_power_at_published,
            "e1_min_n_for_80_at_registered": sessions_for_power(
                CONFIG.registered_sharpe_assumption, alpha, CONFIG.target_power
            ),
            "e1_unchanged_by_this_pass": True,
            "e2_power_at_registered_1_40_holdout_875": e2_registered,
            "e2_power_at_published_2_81_holdout_875": e2_published,
            "e2_power_at_quartered_0_70_holdout_875": float(
                e2[("quartered_0.70", "holdout_875")]
            ),
            "e2_power_at_registered_1_40_in_sample_1762": float(
                e2[("REGISTERED_1.40", "in_sample_1762")]
            ),
            "e2_power_at_published_2_81_in_sample_1762": float(
                e2[("published_2.81", "in_sample_1762")]
            ),
            "e2_power_at_quartered_0_70_in_sample_1762": float(
                e2[("quartered_0.70", "in_sample_1762")]
            ),
            "e2_dispersion_usd_per_share": dispersion["dispersion_usd_per_share"],
            "e2_dispersion_n_priced_trades": dispersion["runs"][
                "bracket_sec_rate_measured"
            ]["trades_priced"],
            "e2_dispersion_bracket_relative_width": dispersion[
                "dispersion_bracket_relative_width"
            ],
            "e2_dispersion_registered_under_the_frozen_model": dispersion[
                "registered_figure_under_the_frozen_model"
            ],
            "e2_caveat": CARVE_OUT_CAVEAT,
            "e2_equals_e1_finding": (
                "E2 power equals E1 power to five decimal places at every "
                "assumption and horizon. Section 8's permutation clusters on "
                "session date, so the session is the independent unit and the "
                "per-trade dispersion cancels. Amendment 15 records this as a "
                "falsified premise of Section 9, not as a copied figure."
            ),
            "measured_trigger_rate": dispersion["measured_trigger_rate"],
            "measured_trigger_rate_n": dispersion[
                "measured_trigger_rate_n_name_sessions"
            ],
            "trigger_rate_assumption_falsified": dispersion[
                "trigger_rate_assumption_used_until_now"
            ],
            "carve_out_sessions_read": dispersion["sessions_pulled"],
            "carve_out_sessions_evaluated": dispersion[
                "sessions_evaluable_after_trailing_window"
            ],
            "carve_out_tickers": dispersion["tickers_sampled"],
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
            "scope_limitation_sl3": (
                "REGISTRATION.md §11.1 SL-3, Amendment 12: cross-vendor "
                "agreement covers 459 holdout sessions and 0 in-sample "
                "sessions, so all 1,762 in-sample sessions rest on a single "
                "unverified feed. A PASS computed on the in-sample window is "
                "conditional on that vendor's rendering of it being faithful, "
                "and this repository holds no measurement supporting that "
                "condition."
            ),
            "tape_verdict": pair["verdict"],
            "tape_median_ratio": pair["median_ratio"],
            "tape_pairs_n": pair["pairs_with_volume_in_both"],
            "sealed_slice_feed_confirmed": feed["verdict"],
            "sealed_slice_feed": feed["manifest_recorded_feed"],
            "sealed_slice_feed_checks_n": feed["discriminating_checks_n"],
            "alpaca_ceiling_state": ceiling["ceiling_state"],
            "alpaca_burst_allowance_requests": ceiling["burst_allowance_requests"],
            "alpaca_burst_allowance_window_s": ceiling["burst_allowance_window_s"],
            "alpaca_sustained_lower_bound_per_min": ceiling[
                "measured_sustained_ceiling_per_minute"
            ],
            "alpaca_operating_pace_per_min": ceiling["operating_pace_per_minute"],
            "delisted_names_enumerated_in_window": delisted["enumerated_inside_window"],
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
    write_report("task6b_section0.json", record)

    say(f"SECTION 0 VERDICT: {result.verdict.value}  [{result.clause}]")
    say(f"  {result.reason}")
    say("")
    say(COLLECTION_NOT_A_READ)
    say("")
    say("Inputs, each with its n:")
    for key, value in record["inputs"].items():  # type: ignore[attr-defined]
        say(f"  {key:<48} {value}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
