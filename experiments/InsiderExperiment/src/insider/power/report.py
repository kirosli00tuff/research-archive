"""Fire the Section 0 power gate.

Reads the dispersion store and nothing else. This module cannot import
insider.portfolio, insider.market or insider.eval, and tests/test_guards.py
fails if it ever does, so the path from here to a realized return does not
exist.
"""

from __future__ import annotations

import json
import sys

from insider.config import CONFIG, Config
from insider.cost import monthly_cost_drag, net_band_bp_per_month, spread_band_bp
from insider.ledger.evidence import record
from insider.paths import REPORTS, ensure_dirs
from insider.power.dispersion import DispersionStats, dropped, load, summarize
from insider.power.mde import MdeResult, band_position, mde_from
from insider.section0 import fire_power_gate


def _plan(cfg: Config) -> list[tuple[int, str, str]]:
    """Every series to report, and whether it bears the verdict."""
    rows = [(cfg.primary_hold_sessions, cfg.primary_weighting, "primary")]
    rows += [(h, cfg.primary_weighting, "secondary hold") for h in cfg.secondary_hold_sessions]
    rows += [(cfg.primary_hold_sessions, cfg.secondary_weighting, "secondary weighting")]
    return rows


def _as_dict(stats: DispersionStats, result: MdeResult) -> dict[str, object]:
    return {
        "hold_sessions": result.hold_sessions,
        "weighting": result.weighting,
        "n_sessions": result.n_sessions,
        "variance_inflation": round(result.variance_inflation, 4),
        "effective_periods": round(result.effective_periods, 1),
        "sd_daily_excess_bp": round(result.sd_daily_excess * 10_000, 4),
        "annualized_tracking_error_pct": round(result.annualized_tracking_error * 100, 4),
        "standard_error_monthly_bp": round(result.standard_error_monthly_bp, 4),
        "mde_bp_per_month": round(result.mde_bp_per_month, 4),
        "autocorr_lag_1": round(stats.autocorr_lag_1, 5),
        "autocorr_lag_5": round(stats.autocorr_lag_5, 5),
        "autocorr_lag_21": round(stats.autocorr_lag_21, 5),
        "book_width_mean": round(stats.book_width_mean, 2),
        "book_width_min": stats.book_width_min,
        "book_width_p10": stats.book_width_p10,
        "book_width_p50": stats.book_width_p50,
        "book_width_p90": stats.book_width_p90,
        "book_width_max": stats.book_width_max,
    }


def main() -> int:
    ensure_dirs()
    cfg = CONFIG
    rows: list[dict[str, object]] = []
    primary: MdeResult | None = None

    print(
        f"critical value {cfg.t_critical}, {cfg.sessions_per_month} sessions per month, "
        f"Newey-West lag {cfg.newey_west_lags}"
    )
    print()
    print(
        f"{'hold':>5} {'weighting':<16} {'role':<20} {'N':>6} {'VIF':>6} {'Neff':>7} "
        f"{'TE ann %':>9} {'MDE bp/mo':>10}"
    )
    for hold, weighting, role in _plan(cfg):
        series = load(hold, weighting)
        stats = summarize(series, cfg=cfg)
        result = mde_from(stats, cfg)
        if role == "primary":
            primary = result
        rows.append({**_as_dict(stats, result), "role": role})
        print(
            f"{hold:>5} {weighting:<16} {role:<20} {stats.n_sessions:>6} "
            f"{stats.variance_inflation:>6.3f} {stats.effective_periods:>7.1f} "
            f"{stats.annualized_tracking_error * 100:>9.3f} {result.mde_bp_per_month:>10.2f}"
        )

    if primary is None:
        print("no primary series. Nothing to fire on.")
        return 1

    print()
    print("Newey-West lag sensitivity on the primary series")
    grid: list[dict[str, object]] = []
    for lag in cfg.newey_west_lag_grid:
        stats = summarize(load(cfg.primary_hold_sessions, cfg.primary_weighting), lags=lag, cfg=cfg)
        result = mde_from(stats, cfg)
        grid.append(
            {
                "lags": lag,
                "variance_inflation": round(stats.variance_inflation, 4),
                "effective_periods": round(stats.effective_periods, 1),
                "mde_bp_per_month": round(result.mde_bp_per_month, 4),
            }
        )
        marker = "  <- registered" if lag == cfg.newey_west_lags else ""
        print(
            f"  lag {lag:>4}  VIF {stats.variance_inflation:6.3f}  "
            f"Neff {stats.effective_periods:8.1f}  MDE {result.mde_bp_per_month:7.2f} bp{marker}"
        )

    gate = fire_power_gate(primary.mde_bp_per_month, cfg)
    drag = monthly_cost_drag(cfg.primary_hold_sessions, cfg)
    net_low, net_high = net_band_bp_per_month(cfg.primary_hold_sessions, cfg)
    gross_low, gross_high = cfg.decayed_gross_band_bp
    spread_low, spread_high = spread_band_bp(cfg)

    print()
    print(f"decayed gross band      {gross_low:.0f} to {gross_high:.0f} bp per month")
    print(f"spread band measured    {spread_low:.1f} to {spread_high:.1f} bp one way")
    print(
        f"round trip amortized    {drag.optimistic_bp_per_month:.2f} to "
        f"{drag.pessimistic_bp_per_month:.2f} bp per month over {drag.hold_months:.1f} months"
    )
    print(f"net band at the hold    {net_low:.1f} to {net_high:.1f} bp per month")
    print(f"computed MDE            {primary.mde_bp_per_month:.2f} bp per month")
    print(f"  against gross         {band_position(primary.mde_bp_per_month, cfg)}")
    print(
        f"  against net           "
        f"{'below' if primary.mde_bp_per_month <= net_low else 'inside' if primary.mde_bp_per_month <= net_high else 'above'}"
        f" the net band {net_low:.1f} to {net_high:.1f} bp"
    )
    print()
    print(f"{gate.verdict.value}: {gate.rationale}")

    payload = {
        "series": rows,
        "newey_west_grid": grid,
        "dropped_primary": dropped(cfg.primary_hold_sessions, cfg.primary_weighting),
        "decayed_gross_band_bp": [gross_low, gross_high],
        "net_band_bp_per_month": [round(net_low, 4), round(net_high, 4)],
        "round_trip_drag_bp_per_month": [
            round(drag.optimistic_bp_per_month, 4),
            round(drag.pessimistic_bp_per_month, 4),
        ],
        "mde_bp_per_month": round(primary.mde_bp_per_month, 4),
        "band_position_gross": band_position(primary.mde_bp_per_month, cfg),
        "verdict": gate.verdict.value,
        "rationale": gate.rationale,
        "stage_b_authorized": gate.stage_b_authorized,
    }
    record("power_gate", **payload)
    out = REPORTS / "stage_a1"
    out.mkdir(parents=True, exist_ok=True)
    (out / "power.json").write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
