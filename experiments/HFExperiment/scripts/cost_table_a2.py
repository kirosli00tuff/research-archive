"""Emit the Stage A.2 cost tables from the cost model and measured spreads.

One source of truth. reports/stage_a2/cost_table.md is this output pasted,
tests/test_costmodel.py pins the regime behaviour the tables rely on, and
tests/test_registered.py pins the registered hurdle against the same
derivation this script prints.
"""
from __future__ import annotations

import json
import statistics as st
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from hfexperiment.costmodel import (
    Regime,
    annual_commission_drag,
    daily_cost_hurdle_bp,
    round_trip,
)
from hfexperiment.registered import CHURN_NAMES_PER_MONTH, THRESHOLDS
from hfexperiment.verdict import first_crossing_day, tuned_rho

SPREADS_JSON = Path(__file__).resolve().parent.parent / (
    "reports/stage_a2/book_spreads.json"
)
NOTIONALS = (30.0, 45.0, 70.0, 100.0, 180.0)
DEPLOYED_USD = 900.0
# The already-spent holdout's width-5 figures, recorded in the A.2 stage
# prompt: excess 27.99 bp/day, tracking error 66.4 pct/yr = 418 bp/day.
PRIMARY_EXCESS_BP_PER_DAY = 27.99
PRIMARY_SIGMA_BP_PER_DAY = 418.0
# The width-5 book is the first five names of the width-20 formation.
WIDTH5_NAMES = ("WOLF", "AXTI", "SNDK", "BE", "LITE")


def load_spreads() -> tuple[dict[str, dict[str, float]], list[str]]:
    data = json.loads(SPREADS_JSON.read_text())
    return data["per_name"], data["unmeasured"]


def main() -> None:
    per_name, unmeasured = load_spreads()
    med_bp = st.median(v["median_bp"] for v in per_name.values())
    med_mid = st.median(v["median_mid"] for v in per_name.values())
    w5 = [per_name[s] for s in WIDTH5_NAMES if s in per_name]
    w5_spread = st.median(v["median_bp"] for v in w5)
    w5_mid = st.median(v["median_mid"] for v in w5)

    print("## Round-trip table, measured spreads")
    print()
    print(f"Spread term: measured book median {med_bp:.2f} bp, "
          f"2026-07-01 width-20 book, consolidated tape, sessions "
          f"2026-08-19 to 2026-08-21. Unmeasured names: "
          f"{unmeasured if unmeasured else 'none'}. Share counts use the "
          f"measured median mid {med_mid:.2f} USD. TAF holds the "
          f"worst-case one cent floor, UNMEASURED.")
    print()
    print("| notional | regime | commission/side | binds "
          "| spread rt bp | reg bp | total rt bp |")
    print("|---|---|---|---|---|---|---|")
    for value in NOTIONALS:
        for regime in Regime:
            rt = round_trip(regime, value, med_mid, med_bp)
            print(
                f"| {value:.0f} | {regime.value} "
                f"| {rt.commission_per_side_usd:.4f} "
                f"({rt.commission_rt_bp / 2:.1f} bp) "
                f"| {rt.commission_binding} "
                f"| {rt.spread_rt_bp:.2f} "
                f"| {rt.regulatory_bp:.2f} "
                f"| {rt.total_rt_bp:.1f} |"
            )
    print()

    print("## Annual deterministic drag at measured churn")
    print()
    print("| width | churn/mo | fills/mo | regime | commission/yr "
          "| reg/yr | total/yr |")
    print("|---|---|---|---|---|---|---|")
    for width in (THRESHOLDS.traded_width, THRESHOLDS.primary_width):
        churn = CHURN_NAMES_PER_MONTH[width]
        for regime in Regime:
            d = annual_commission_drag(
                regime, width, churn, DEPLOYED_USD, med_mid
            )
            print(
                f"| {width} | {churn:.1f} | {d.fills_per_month:.1f} "
                f"| {regime.value} | {d.commission_usd:.2f} "
                f"| {d.regulatory_usd:.2f} | {d.total_usd:.2f} |"
            )
    print()

    print("## The registered cost hurdle")
    print()
    w5_rt = round_trip(
        Regime.FRACTIONAL, DEPLOYED_USD / THRESHOLDS.primary_width,
        w5_mid, w5_spread,
    )
    hurdle = daily_cost_hurdle_bp(
        THRESHOLDS.primary_width,
        CHURN_NAMES_PER_MONTH[THRESHOLDS.primary_width],
        w5_rt.total_rt_bp,
    )
    print(f"Primary width {THRESHOLDS.primary_width}, churn "
          f"{CHURN_NAMES_PER_MONTH[THRESHOLDS.primary_width]:.1f} names "
          f"per month, per-name notional "
          f"{DEPLOYED_USD / THRESHOLDS.primary_width:.0f} USD, worst-case "
          f"fractional regime. Width-5 book measured spread "
          f"{w5_spread:.2f} bp at median mid {w5_mid:.2f} USD. Round trip "
          f"{w5_rt.total_rt_bp:.2f} bp. Hurdle "
          f"{hurdle:.2f} bp per day. Registered: "
          f"{THRESHOLDS.cost_hurdle_bp_per_day:.2f}.")
    print()

    print("## Verdict honest arithmetic")
    print()
    rho = tuned_rho()
    zero_day = first_crossing_day(
        PRIMARY_EXCESS_BP_PER_DAY, PRIMARY_SIGMA_BP_PER_DAY, rho, 0.0
    )
    hurdle_day = first_crossing_day(
        PRIMARY_EXCESS_BP_PER_DAY, PRIMARY_SIGMA_BP_PER_DAY, rho,
        THRESHOLDS.cost_hurdle_bp_per_day,
    )
    print(f"rho tuned for {THRESHOLDS.crossing_target_days} trading days "
          f"at alpha {THRESHOLDS.alpha_one_sided}: {rho:.6f}. If the "
          f"width-5 mean holds at {PRIMARY_EXCESS_BP_PER_DAY} bp per day "
          f"against {PRIMARY_SIGMA_BP_PER_DAY:.0f} bp daily noise, the "
          f"lower bound clears zero at day {zero_day} and clears the "
          f"registered hurdle at day {hurdle_day}.")


if __name__ == "__main__":
    main()
