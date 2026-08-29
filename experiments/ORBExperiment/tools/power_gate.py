"""A.2 TASK 4 — the power gate. Computes; never reads an outcome value."""

from __future__ import annotations

import json
import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from orb.absence import Absent
from orb.calendar import sessions
from orb.config import CONFIG
from orb.power import (
    PowerRow,
    e2_power,
    information_ratio_for_t,
    power_one_sided,
    pre_period_dispersion_absent,
    sessions_for_power,
    sessions_for_t,
    t_statistic,
)
from orb.verdict import alpha_adj

ROOT = Path(__file__).resolve().parent.parent
HOLDOUT_START = date(2023, 1, 3)

ASSUMPTIONS = [
    ("published (undecayed)", CONFIG.published_sharpe_assumption),
    ("REGISTERED (half)", CONFIG.registered_sharpe_assumption),
    ("quartered", CONFIG.quartered_sharpe_assumption),
]

HORIZONS = [
    ("registered holdout, to 2026-06-30", date(2026, 6, 30)),
    ("projected to 2026-12-31", date(2026, 12, 31)),
    ("projected to 2027-06-30", date(2027, 6, 30)),
]


def main() -> int:
    alpha = alpha_adj()
    dispersion = pre_period_dispersion_absent()
    rows: list[PowerRow] = []

    counts = {
        name: sum(1 for _ in sessions(HOLDOUT_START, end)) for name, end in HORIZONS
    }

    for a_name, sharpe in ASSUMPTIONS:
        for h_name, _ in HORIZONS:
            n = counts[h_name]
            rows.append(
                PowerRow(
                    assumption_name=a_name,
                    annual_sharpe=sharpe,
                    horizon_name=h_name,
                    sessions=n,
                    t_statistic=t_statistic(sharpe, n),
                    e1_power=power_one_sided(sharpe, n, alpha),
                    e1_min_n_for_80=sessions_for_power(
                        sharpe, alpha, CONFIG.target_power
                    ),
                    e2_power=e2_power(dispersion, dispersion, n * 20, alpha),
                )
            )

    print(f"alpha_adj = {alpha:.8f} (one-sided, per co-primary)\n")
    print(
        f"{'assumption':<24}{'horizon':<36}{'n':>6}{'t':>8}{'E1 power':>10}{'min N 80%':>11}{'E2 power':>12}"
    )
    print("-" * 107)
    for r in rows:
        e2 = "Absent" if isinstance(r.e2_power, Absent) else f"{r.e2_power:.4f}"
        print(
            f"{r.assumption_name:<24}{r.horizon_name:<36}{r.sessions:>6}"
            f"{r.t_statistic:>8.4f}{r.e1_power:>10.4f}{r.e1_min_n_for_80:>11}{e2:>12}"
        )

    print("\n--- Section 9 arithmetic, reproduced against the prompt's figures ---")
    checks = [
        ("sessions to clear t=2.0 at 1.40", sessions_for_t(1.40, 2.0), 514),
        ("sessions to clear t=3.0 at 1.40", sessions_for_t(1.40, 3.0), 1157),
    ]
    for label, computed, stated in checks:
        flag = "AGREES" if computed == stated else f"DISAGREES (prompt says {stated})"
        print(f"  {label:<38} computed {computed:>6}   {flag}")

    n_hold = counts["registered holdout, to 2026-06-30"]
    print(
        f"  {'t at the computed holdout n':<38} computed {t_statistic(1.40, n_hold):>6.4f}   prompt says 2.62 at n=880"
    )

    print("\n--- Per-trade information ratio, non-binding, at 20 names/session ---")
    for rate in (1.00, 0.75, 0.535, 0.50, 0.25):
        trades = int(n_hold * 20 * rate)
        ir = information_ratio_for_t(trades, 3.0)
        note = "  <- matches the prompt's 0.031" if abs(ir - 0.031) < 0.0006 else ""
        print(f"  trigger rate {rate:>5.3f} -> {trades:>6} trades -> IR {ir:.4f}{note}")

    out = ROOT / "reports" / "stage_a2" / "power.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(
        json.dumps(
            {
                "alpha_adj": alpha,
                "session_counts": counts,
                "rows": [
                    {
                        "assumption": r.assumption_name,
                        "annual_sharpe": r.annual_sharpe,
                        "horizon": r.horizon_name,
                        "sessions": r.sessions,
                        "t": r.t_statistic,
                        "e1_power": r.e1_power,
                        "e1_min_n_for_80": r.e1_min_n_for_80,
                        "e2_power": "Absent",
                    }
                    for r in rows
                ],
                "e2_absence_reason": dispersion.detail,
            },
            indent=2,
            sort_keys=True,
        ),
        encoding="utf-8",
    )
    print(f"\nwrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
