"""A.3 TASK 3 — recompute the shift, E2 and joint power on the measured band.

**The criterion this evaluates was committed and pushed before the measurement
existed** (Amendment 24, commit `4ae14dc`). This tool applies it and records the
outcome with the deciding number beside it.

**Nothing is adjusted to move the figure.** The effect assumption stays at the
registered 1.40, the alpha at Amendment 18's 0.05, the stop share at the measured
0.381818, and no registered rule is touched. **The assignment of median to
central and 90th percentile to pessimistic was fixed in TASK 2 before the shift
was computed**, and this tool reads the band as measured rather than selecting
among its statistics.
"""

from __future__ import annotations

import json
import math
import sys
from datetime import date
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))


from orb.absence import Absent
from orb.config import CONFIG
from orb.power import (
    e2_pessimistic_mean,
    e2_power_pessimistic,
    joint_power,
    power_one_sided,
    sessions_for_power,
    trades_for_e2_power,
)
from orb.redact import say
from orb.verdict import per_test_alpha

OUT = Path(__file__).resolve().parent.parent / "reports" / "stage_a3rescue"
REPAIR = Path(__file__).resolve().parent.parent / "reports" / "stage_a2repair"
HOLDOUT_N = 875
IN_SAMPLE_N = 1762

CRITERION_DATE = "2026-08-30"
CRITERION_COMMIT = "4ae14dc"


def main() -> int:
    band = json.loads((OUT / "task2_slippage_band.json").read_text(encoding="utf-8"))
    prior = json.loads((REPAIR / "task4_joint_power.json").read_text(encoding="utf-8"))
    dispersion = float(prior["dispersion_usd_per_share"])
    trades_per_session = float(prior["trades_per_session_measured"])
    mean_per_unit_sharpe = float(prior["central_mean_per_unit_of_annual_sharpe"])
    carried_shift = float(prior["pessimistic_shift_usd_per_share"])
    shift = float(band["measured_shift_usd_per_share"])
    alpha = per_test_alpha()

    central_at_registered = mean_per_unit_sharpe * CONFIG.registered_sharpe_assumption
    pessimistic_at_registered = e2_pessimistic_mean(central_at_registered, shift)

    rows: list[dict[str, Any]] = []
    for name, sharpe in (
        ("published_2.81", CONFIG.published_sharpe_assumption),
        ("REGISTERED_1.40", CONFIG.registered_sharpe_assumption),
        ("quartered_0.70", CONFIG.quartered_sharpe_assumption),
    ):
        central = mean_per_unit_sharpe * sharpe
        pessimistic = e2_pessimistic_mean(central, shift)
        needed = trades_for_e2_power(dispersion, pessimistic, alpha, 0.80)
        if isinstance(needed, Absent):
            e2_min: int | str = f"Absent({needed.detail})"
            joint_min: int | str = "Absent: unreachable because E2's is"
        else:
            e2_min = math.ceil(needed / trades_per_session)
            joint_min = max(e2_min, sessions_for_power(sharpe, alpha, 0.80))
        for horizon, n in (("holdout_875", HOLDOUT_N), ("in_sample_1762", IN_SAMPLE_N)):
            trades = max(1, round(n * trades_per_session))
            e1 = power_one_sided(sharpe, n, alpha)
            e2 = e2_power_pessimistic(dispersion, central, shift, trades, alpha)
            assert isinstance(e2, float)
            jp = joint_power(e1, e2)
            rows.append(
                {
                    "assumption": name,
                    "annual_sharpe": sharpe,
                    "horizon": horizon,
                    "sessions": n,
                    "trades_implied": trades,
                    "central_mean_usd_per_share": central,
                    "measured_shift_usd_per_share": shift,
                    "pessimistic_mean_usd_per_share": pessimistic,
                    "e1_power": e1,
                    "e2_power": e2,
                    "joint_power": jp.upper_bound,
                    "joint_binding_component": jp.binding_component,
                    "e1_min_sessions_for_80": sessions_for_power(sharpe, alpha, 0.80),
                    "e2_min_sessions_for_80": e2_min,
                    "joint_min_sessions_for_80": joint_min,
                }
            )

    reg = next(
        r
        for r in rows
        if r["assumption"] == "REGISTERED_1.40" and r["horizon"] == "holdout_875"
    )
    shift_below_central = shift < central_at_registered
    e2_above_size = float(reg["e2_power"]) > alpha
    rescued = shift_below_central and e2_above_size
    outcome = "RESCUED_DEGRADED" if rescued else "NOT_RESCUED"

    findings: dict[str, Any] = {
        "kind": "rescue_criterion_evaluation",
        "computed_at": date.today().isoformat(),
        "criterion_precommitted_on": CRITERION_DATE,
        "criterion_commit": CRITERION_COMMIT,
        "criterion_precommitted_before_the_measurement": True,
        "outcome": outcome,
        "deciding_numbers": {
            "measured_shift_usd_per_share": shift,
            "central_mean_at_registered_1_40": central_at_registered,
            "shift_strictly_below_central_mean": shift_below_central,
            "margin_central_minus_shift": central_at_registered - shift,
            "pessimistic_cost_mean_at_registered_1_40": pessimistic_at_registered,
            "e2_power_at_registered_1_40_holdout": reg["e2_power"],
            "alpha": alpha,
            "e2_power_above_the_size_of_the_test": e2_above_size,
        },
        "shift_before_and_after": {
            "carried_band_shift": carried_shift,
            "measured_band_shift": shift,
            "change": shift - carried_shift,
            "ratio_measured_over_carried": (
                shift / carried_shift if carried_shift else None
            ),
        },
        "inputs_not_adjusted": [
            "effect assumption held at the registered 1.40",
            "alpha held at Amendment 18's 0.05",
            "stop share held at the measured 0.381818",
            "no registered rule touched",
            "no selection among the TASK 2 statistics: median to central and "
            "90th percentile to pessimistic was fixed before the shift existed",
        ],
        "one_minute_resolution_caveat": band["one_minute_resolution_caveat"],
        "carve_out_caveat": prior["carve_out_caveat"],
        "dispersion_usd_per_share": dispersion,
        "trades_per_session_measured": trades_per_session,
        "rows": rows,
    }
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "task3_rescue_verdict.json").write_text(
        json.dumps(findings, indent=2, sort_keys=True), encoding="utf-8"
    )

    say(f"criterion pre-committed {CRITERION_DATE}, commit {CRITERION_COMMIT}")
    say(
        f"measured shift {shift:.6f} against a carried-band shift of "
        f"{carried_shift:.6f} (ratio {shift / carried_shift:.4f})"
    )
    say(
        f"central mean at 1.40 {central_at_registered:.6f}; "
        f"pessimistic-cost mean {pessimistic_at_registered:+.6f}"
    )
    say("")
    header = (
        f"{'assumption':<16}{'horizon':<16}{'pess.mean':>12}{'E1':>9}{'E2':>9}"
        f"{'JOINT':>9}{'minN E1':>9}{'minN E2':>10}{'minN JOINT':>12}"
    )
    say(header)
    say("-" * len(header))
    for r in rows:
        e2m, jm = r["e2_min_sessions_for_80"], r["joint_min_sessions_for_80"]
        say(
            f"{r['assumption']:<16}{r['horizon']:<16}"
            f"{r['pessimistic_mean_usd_per_share']:>+12.6f}"
            f"{r['e1_power']:>9.4f}{r['e2_power']:>9.4f}{r['joint_power']:>9.4f}"
            f"{r['e1_min_sessions_for_80']:>9}"
            f"{(e2m if isinstance(e2m, int) else 'none'):>10}"
            f"{(jm if isinstance(jm, int) else 'none'):>12}"
        )
    say("")
    say(f"OUTCOME: {outcome}")
    say(
        f"  shift {shift:.6f} {'<' if shift_below_central else '>='} "
        f"central mean {central_at_registered:.6f}; "
        f"E2 power {float(reg['e2_power']):.6f} "
        f"{'>' if e2_above_size else '<='} alpha {alpha}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
