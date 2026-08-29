"""A.2 Task 4: the power gate. Compute nothing else, read no outcome value.

Exact permutation power by simulation for E1 and E2 at alpha_adj one-sided, at
the registered 0.09 assumption, at the undecayed published 0.18, and at the
quartered 0.045, using achieved admissible N and projected N by the two
registered deadlines from the measured forward admissible rate.

E2's inputs come from the pre-period carve-out only, strictly before
2025-05-01, as Section 9 registers.
"""

from __future__ import annotations

import json
import sys
from datetime import UTC, date

from etf.clock import iso_z, now_utc
from etf.config import CONFIG
from etf.costs import hyperliquid_band
from etf.paths import REPORTS
from etf.power import EconomicInputs, e1_power, e2_power, minimum_n

REPORT = REPORTS / "stage_a2" / "power.json"
TARGET = CONFIG.power_go_floor
BP = 1e-4


def trading_days_between(start: date, end: date) -> int:
    """US trading days, approximated as weekdays less the measured holiday rate.

    The census measured 3 all-dash rows in 336 weekday rows over the
    out-of-sample window, so the flow source's own row count is 336 weekday
    rows of which 333 printed. The projection uses the MEASURED printed-day
    rate rather than a calendar assumption.
    """
    days = 0
    cursor = start
    while cursor < end:
        if cursor.weekday() < 5:
            days += 1
        cursor = date.fromordinal(cursor.toordinal() + 1)
    return days


def main() -> int:
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    now = now_utc()
    census = json.loads((REPORTS / "stage_a2" / "census.json").read_text(encoding="utf-8"))
    pre = json.loads((REPORTS / "stage_a2" / "preperiod_inputs.json").read_text(encoding="utf-8"))

    live = census["signal_distribution_live_descriptive"]
    trade_share = float(live["trade_share"])
    band = hyperliquid_band()

    inputs = EconomicInputs(
        daily_sd=float(pre["daily_sd"]),
        daily_funding_sum=float(pre["daily_funding_sum"]),
        round_trip_cost=band.central_bp * BP,
        trade_share=trade_share,
        n_volatility_returns=int(pre["n_volatility_returns"]),
        n_funding_hours=int(pre["n_funding_hours"]),
    )

    achieved = int(census["admissible"])
    achieved_forward = int(census["admissible_forward_capture"])
    today = now.astimezone(UTC).date()

    # The forward cohort accrues at the measured printed-day rate: the census
    # measured 333 printed days in 336 weekday rows over the window.
    printed_rate = 333 / 336
    to_interim = trading_days_between(today, date.fromisoformat(CONFIG.interim_deadline))
    to_deadline = trading_days_between(today, date.fromisoformat(CONFIG.projection_deadline))

    scenarios = {
        "achieved_total": achieved,
        "achieved_forward_only": achieved_forward,
        "forward_only_by_interim": achieved_forward + round(to_interim * printed_rate),
        "forward_only_by_deadline": achieved_forward + round(to_deadline * printed_rate),
        "all_cohorts_by_deadline": achieved + round(to_deadline * printed_rate),
    }
    assumptions = {
        "registered_0.09": CONFIG.rho_registered,
        "published_0.18": CONFIG.rho_undecayed,
        "quartered_0.045": CONFIG.rho_quartered,
    }

    powers: dict[str, dict[str, dict[str, float]]] = {}
    for scenario, n in scenarios.items():
        powers[scenario] = {}
        for label, rho in assumptions.items():
            if n < 10:
                powers[scenario][label] = {"n": n, "e1": 0.0, "e2": 0.0}
                continue
            e1 = e1_power(n, rho)
            # E2's inner permutation is O(draws x n) per simulation, so the
            # gate runs it at a smaller but stated budget. The simulation error
            # on a power near one half is about 0.025 at 400 simulations, and
            # both registered floors sit far from these values.
            e2 = e2_power(n, rho, inputs, draws=1500, simulations=400)
            powers[scenario][label] = {"n": n, "e1": e1, "e2": e2}
            print(f"{scenario:28s} {label:18s} n={n:5d}  E1={e1:.4f}  E2={e2:.4f}")

    minimums: dict[str, int | None] = {
        label: minimum_n(rho, TARGET) for label, rho in assumptions.items()
    }
    for label, floor in minimums.items():
        shown = floor if floor is not None else "not reached below n = 4000"
        print(f"minimum N clearing {TARGET:.2f} power for E1 at {label}: {shown}")

    out = {
        "computed_at": iso_z(now),
        "alpha_adj": CONFIG.alpha_adj,
        "target_power": TARGET,
        "permutation_draws": CONFIG.permutation_draws,
        "power_simulations": CONFIG.power_simulations,
        "assumptions": assumptions,
        "scenarios": scenarios,
        "printed_day_rate": printed_rate,
        "weekdays_to_interim": to_interim,
        "weekdays_to_deadline": to_deadline,
        "economic_inputs": {
            "daily_sd": inputs.daily_sd,
            "n_volatility_returns": inputs.n_volatility_returns,
            "daily_funding_sum": inputs.daily_funding_sum,
            "n_funding_hours": inputs.n_funding_hours,
            "round_trip_cost_bp": band.central_bp,
            "trade_share": inputs.trade_share,
            "trade_share_n": int(live["n"]),
        },
        "powers": powers,
        "minimum_n_for_e1": minimums,
    }
    REPORT.write_text(json.dumps(out, indent=2, sort_keys=True), encoding="utf-8")
    print(f"\nwrote {REPORT}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
