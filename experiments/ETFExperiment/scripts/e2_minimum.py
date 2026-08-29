"""A.2 Task 4: the minimum N clearing the registered power target for E2.

Reported beside E1's, because Section 10 requires **both** co-primaries at or
above the target at achieved admissible N, so the larger of the two governs.
"""

from __future__ import annotations

import json
import sys

from etf.clock import iso_z, now_utc
from etf.config import CONFIG
from etf.costs import hyperliquid_band
from etf.paths import REPORTS
from etf.power import EconomicInputs, e2_power

REPORT = REPORTS / "stage_a2" / "e2_minimum_n.json"
BP = 1e-4


def main() -> int:
    census = json.loads((REPORTS / "stage_a2" / "census.json").read_text(encoding="utf-8"))
    pre = json.loads((REPORTS / "stage_a2" / "preperiod_inputs.json").read_text(encoding="utf-8"))
    band = hyperliquid_band()
    inputs = EconomicInputs(
        daily_sd=float(pre["daily_sd"]),
        daily_funding_sum=float(pre["daily_funding_sum"]),
        round_trip_cost=band.central_bp * BP,
        trade_share=float(census["signal_distribution_live_descriptive"]["trade_share"]),
        n_volatility_returns=int(pre["n_volatility_returns"]),
        n_funding_hours=int(pre["n_funding_hours"]),
    )
    out: dict[str, object] = {"computed_at": iso_z(now_utc()), "target": CONFIG.power_go_floor}
    grid: dict[str, dict[str, float]] = {}
    for label, rho in (
        ("published_0.18", CONFIG.rho_undecayed),
        ("registered_0.09", CONFIG.rho_registered),
    ):
        grid[label] = {}
        for n in (200, 250, 300, 350, 400, 600, 900, 1200):
            power = e2_power(n, rho, inputs, draws=1200, simulations=300)
            grid[label][str(n)] = power
            print(f"E2 {label:16s} n={n:5d}  power={power:.4f}")
            if power >= CONFIG.power_go_floor:
                print(f"   -> E2 clears {CONFIG.power_go_floor:.2f} at or below n = {n}")
                break
    out["grid"] = grid
    REPORT.write_text(json.dumps(out, indent=2, sort_keys=True), encoding="utf-8")
    print(f"\nwrote {REPORT}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
