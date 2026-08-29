"""A.1 TASK 4 (inference repair) — E2 power and the joint power of the conjunction.

**The operative figure for the Section 10 latch is joint power**, not either
component. Section 8 asserts the claim only if **both** co-primaries reject, so
the probability a reader needs is the probability that **both** do, and that is
bounded above by the smaller component power whatever the dependence between
them.

**Every input here is measured or registered.** The dispersion is the A.1 TASK 5
figure; the pessimistic shift is the A.1 TASK 3 figure of this pass; the alpha is
Amendment 18's corrected 0.05; the assumptions are Section 9's three. **Nothing
is adjusted to rescue a number.**
"""

from __future__ import annotations

import json
import math
import sys
from datetime import date
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))

from _a1r import REPORTS

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
from orb.verdict import alpha_adj, per_test_alpha

OUT = Path(__file__).resolve().parent.parent / "reports" / "stage_a2repair"
HOLDOUT_N = 875
IN_SAMPLE_N = 1762

CARVE_OUT_CAVEAT = (
    "Amendment 11: the dispersion input comes from a POST-HOLDOUT regime "
    "(2026-07-01 to 2026-08-28), later than the sample it is applied to, and "
    "may misstate in-sample dispersion in either direction by an amount this "
    "repository has not measured and does not claim to bound."
)


def main() -> int:
    dispersion_report = json.loads(
        (REPORTS / "task5c_dispersion_e2.json").read_text(encoding="utf-8")
    )
    mix = json.loads((OUT / "task3_execution_mix.json").read_text(encoding="utf-8"))
    dispersion = float(dispersion_report["dispersion_usd_per_share"])
    shift = float(mix["mean_pessimistic_shift_usd_per_share"])
    trades_per_session = float(dispersion_report["trades_per_session_measured"])

    # The Amendment 15 identity: the implied CENTRAL mean per share is a fixed
    # multiple of the Sharpe assumption. It is read from the measured table
    # rather than re-derived, so the two records cannot drift apart.
    row = next(
        r
        for r in dispersion_report["e2_power_rows"]
        if r["assumption"] == "REGISTERED_1.40" and r["horizon"] == "holdout_875"
    )
    mean_per_unit_sharpe = float(row["implied_mean_usd_per_share"]) / float(
        row["annual_sharpe"]
    )

    alpha = per_test_alpha()
    superseded_alpha = alpha_adj()
    rows: list[dict[str, Any]] = []
    for name, sharpe in (
        ("published_2.81", CONFIG.published_sharpe_assumption),
        ("REGISTERED_1.40", CONFIG.registered_sharpe_assumption),
        ("quartered_0.70", CONFIG.quartered_sharpe_assumption),
    ):
        central_mean = mean_per_unit_sharpe * sharpe
        pessimistic_mean = e2_pessimistic_mean(central_mean, shift)
        needed_trades = trades_for_e2_power(dispersion, pessimistic_mean, alpha, 0.80)
        if isinstance(needed_trades, Absent):
            e2_min_sessions: int | str = f"Absent({needed_trades.detail})"
            joint_min_sessions: int | str = (
                "Absent: the joint condition is unreachable at any n because E2's is"
            )
        else:
            e2_min_sessions = math.ceil(needed_trades / trades_per_session)
            joint_min_sessions = max(
                e2_min_sessions, sessions_for_power(sharpe, alpha, 0.80)
            )

        for horizon, n_sessions in (
            ("holdout_875", HOLDOUT_N),
            ("in_sample_1762", IN_SAMPLE_N),
        ):
            trades = max(1, round(n_sessions * trades_per_session))
            e1 = power_one_sided(sharpe, n_sessions, alpha)
            e2 = e2_power_pessimistic(dispersion, central_mean, shift, trades, alpha)
            assert isinstance(e2, float)
            jp = joint_power(e1, e2)
            rows.append(
                {
                    "assumption": name,
                    "annual_sharpe": sharpe,
                    "horizon": horizon,
                    "sessions": n_sessions,
                    "trades_implied": trades,
                    "central_mean_usd_per_share": central_mean,
                    "pessimistic_shift_usd_per_share": shift,
                    "pessimistic_mean_usd_per_share": pessimistic_mean,
                    "dispersion_usd_per_share": dispersion,
                    "e1_power_at_0_05": e1,
                    "e1_power_at_superseded_0_0253": power_one_sided(
                        sharpe, n_sessions, superseded_alpha
                    ),
                    "e2_power_at_0_05": e2,
                    "joint_power_upper_bound": jp.upper_bound,
                    "joint_power_frechet_lower_bound": jp.frechet_lower_bound,
                    "joint_power_under_nested_rejection": jp.under_nested_rejection,
                    "joint_binding_component": jp.binding_component,
                    "e1_min_sessions_for_80": sessions_for_power(sharpe, alpha, 0.80),
                    "e2_min_sessions_for_80": e2_min_sessions,
                    "joint_min_sessions_for_80": joint_min_sessions,
                    "carve_out_caveat": CARVE_OUT_CAVEAT,
                }
            )

    registered = next(
        r
        for r in rows
        if r["assumption"] == "REGISTERED_1.40" and r["horizon"] == "holdout_875"
    )
    collapsed = float(registered["pessimistic_mean_usd_per_share"]) <= 0.0

    findings: dict[str, Any] = {
        "kind": "e2_and_joint_power_under_the_amended_conjunction",
        "computed_at": date.today().isoformat(),
        "alpha": alpha,
        "superseded_alpha": superseded_alpha,
        "dispersion_usd_per_share": dispersion,
        "pessimistic_shift_usd_per_share": shift,
        "trades_per_session_measured": trades_per_session,
        "central_mean_per_unit_of_annual_sharpe": mean_per_unit_sharpe,
        "e2_collapsed_at_the_registered_assumption": collapsed,
        "collapse_statement": (
            "The measured pessimistic shift of "
            f"{shift:.6f} USD/share EXCEEDS the implied central mean of "
            f"{registered['central_mean_usd_per_share']:.6f} at the registered "
            f"1.40 Sharpe assumption, so the pessimistic-cost mean is "
            f"{registered['pessimistic_mean_usd_per_share']:+.6f} — negative. "
            "E2's alternative lies inside its own null, E2 power falls BELOW the "
            "size of the test, and joint power collapses with it. This is a "
            "measured property of the registered design, recorded rather than "
            "routed around."
            if collapsed
            else "The pessimistic-cost mean is positive at the registered assumption."
        ),
        "latch_condition": (
            "JOINT power at or above 0.80, per Amendment 21. Neither component "
            "power alone satisfies Section 10 clause 1."
        ),
        "carve_out_caveat": CARVE_OUT_CAVEAT,
        "rows": rows,
    }
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "task4_joint_power.json").write_text(
        json.dumps(findings, indent=2, sort_keys=True), encoding="utf-8"
    )

    say(f"alpha = {alpha} (Amendment 18; superseded {superseded_alpha:.8f})")
    say(
        f"dispersion {dispersion:.6f} USD/share; pessimistic shift "
        f"{shift:.6f} USD/share; {trades_per_session:.6f} trades per session"
    )
    say("")
    header = (
        f"{'assumption':<16}{'horizon':<16}{'pess.mean':>12}{'E1@0.05':>10}"
        f"{'E2@0.05':>10}{'JOINT':>10}{'binds':>7}{'minN E1':>9}{'minN E2':>10}"
        f"{'minN JOINT':>12}"
    )
    say(header)
    say("-" * len(header))
    for r in rows:
        e2m = r["e2_min_sessions_for_80"]
        jm = r["joint_min_sessions_for_80"]
        say(
            f"{r['assumption']:<16}{r['horizon']:<16}"
            f"{r['pessimistic_mean_usd_per_share']:>+12.6f}"
            f"{r['e1_power_at_0_05']:>10.4f}{r['e2_power_at_0_05']:>10.4f}"
            f"{r['joint_power_upper_bound']:>10.4f}{r['joint_binding_component']:>7}"
            f"{r['e1_min_sessions_for_80']:>9}"
            f"{(e2m if isinstance(e2m, int) else 'none'):>10}"
            f"{(jm if isinstance(jm, int) else 'none'):>12}"
        )
    say("")
    say(findings["collapse_statement"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
