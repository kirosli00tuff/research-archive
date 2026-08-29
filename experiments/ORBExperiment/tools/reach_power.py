"""A.1 TASK 5, second half — which registered windows survive each measured reach.

Reach is a **count** question, so it is answered with the existing power module
rather than with a new one. Nothing here reads a bar: every input is a session
count from `orb.calendar` and a measured earliest-served session from the
bisection.
"""

from __future__ import annotations

import json
import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from _a1r import REPORTS, write_report  # noqa: E402
from orb.calendar import sessions  # noqa: E402
from orb.config import CONFIG  # noqa: E402
from orb.power import power_one_sided, sessions_for_power, t_statistic  # noqa: E402
from orb.redact import say  # noqa: E402

ALPHA_ADJ = 1.0 - 0.95 ** (1.0 / CONFIG.n_co_primaries)


def count(start: date, end: date) -> int:
    return sum(1 for _ in sessions(start, end)) if start <= end else 0


def main() -> int:
    reach = json.loads((REPORTS / "task5_reach.json").read_text())
    in_start = date.fromisoformat(CONFIG.in_sample_start)
    in_end = date.fromisoformat(CONFIG.in_sample_end)
    ho_start = date.fromisoformat(CONFIG.holdout_start)
    ho_end = date.fromisoformat(CONFIG.holdout_end)

    full_in = count(in_start, in_end)
    full_ho = count(ho_start, ho_end)
    say(f"registered windows: in-sample n = {full_in}, holdout n = {full_ho}")
    say(f"alpha_adj = {ALPHA_ADJ:.8f}")

    rows: list[dict[str, object]] = []
    for vendor, result in reach["vendors"].items():
        earliest_iso = result["earliest_served_session"]
        earliest = date.fromisoformat(earliest_iso)
        in_reach = count(max(earliest, in_start), in_end)
        ho_reach = count(max(earliest, ho_start), ho_end)
        row: dict[str, object] = {
            "vendor": vendor,
            "earliest_served_session": earliest_iso,
            "probes": result["probes"],
            "in_sample_sessions_registered": full_in,
            "in_sample_sessions_reachable": in_reach,
            "in_sample_shortfall": full_in - in_reach,
            "holdout_sessions_registered": full_ho,
            "holdout_sessions_reachable": ho_reach,
            "holdout_shortfall": full_ho - ho_reach,
            "covers_in_sample_opening": earliest <= in_start,
            "covers_holdout_opening": earliest <= ho_start,
        }
        for label, assumption in (
            ("registered_1_40", CONFIG.registered_sharpe_assumption),
            ("published_2_81", CONFIG.published_sharpe_assumption),
            ("quartered_0_70", CONFIG.quartered_sharpe_assumption),
        ):
            row[f"e1_power_on_reachable_holdout_at_{label}"] = (
                power_one_sided(assumption, ho_reach, ALPHA_ADJ) if ho_reach else 0.0
            )
        row["holdout_t_at_registered"] = (
            t_statistic(CONFIG.registered_sharpe_assumption, ho_reach)
            if ho_reach
            else 0.0
        )
        row["min_sessions_for_target_power_at_registered"] = sessions_for_power(
            CONFIG.registered_sharpe_assumption, ALPHA_ADJ, CONFIG.target_power
        )
        rows.append(row)
        say(
            f"{vendor:8s} earliest={earliest_iso} "
            f"in-sample {in_reach}/{full_in} (short {full_in - in_reach}) "
            f"holdout {ho_reach}/{full_ho} (short {full_ho - ho_reach}) "
            f"E1@1.40={row['e1_power_on_reachable_holdout_at_registered_1_40']:.4f} "
            f"E1@2.81={row['e1_power_on_reachable_holdout_at_published_2_81']:.4f}"
        )

    overlap_start = max(
        date.fromisoformat(r["earliest_served_session"])
        for r in reach["vendors"].values()
    )
    overlap = {
        "cross_vendor_overlap_start": overlap_start.isoformat(),
        "overlap_sessions_in_sample": count(max(overlap_start, in_start), in_end),
        "overlap_sessions_holdout": count(max(overlap_start, ho_start), ho_end),
        "overlap_sessions_total_registered_windows": (
            count(max(overlap_start, in_start), in_end)
            + count(max(overlap_start, ho_start), ho_end)
        ),
    }
    say(
        f"cross-vendor overlap starts {overlap['cross_vendor_overlap_start']}: "
        f"in-sample n = {overlap['overlap_sessions_in_sample']}, "
        f"holdout n = {overlap['overlap_sessions_holdout']}"
    )

    write_report(
        "task5_reach_power.json",
        {"alpha_adj": ALPHA_ADJ, "vendors": rows, "cross_vendor_overlap": overlap},
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
