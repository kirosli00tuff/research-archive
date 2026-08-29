"""A.2 Tasks 1 and 2: the admissible-day census and the outcome-blind signal distribution.

Parses flow fields and timestamps only. No price field is touched on this path.
The census ledger is append-only and fsynced.
"""

from __future__ import annotations

import json
import statistics
import sys
from datetime import UTC, date, datetime

from etf.absence import Absent
from etf.archive import Memento, parse_timemap, qualifying_window
from etf.census import build_census
from etf.clock import iso_z, now_utc
from etf.config import CONFIG
from etf.ledger.append_only import AppendOnlyLedger
from etf.paths import CENSUS_LEDGER, DATA, REPORTS, SNAPSHOT_LEDGER
from etf.signal import Position, position
from etf.snapshot import parse_flow_table

REPORT = REPORTS / "stage_a2" / "census.json"


def quantiles(values: list[float]) -> dict[str, float]:
    ordered = sorted(values)
    n = len(ordered)

    def q(p: float) -> float:
        import math

        return ordered[max(0, min(n - 1, math.ceil(p * n) - 1))]

    return {
        "min": ordered[0],
        "p05": q(0.05),
        "p25": q(0.25),
        "median": statistics.median(ordered),
        "p75": q(0.75),
        "p95": q(0.95),
        "max": ordered[-1],
        "mean": statistics.fmean(ordered),
    }


def band_counts(values: list[float]) -> dict[str, int]:
    t = CONFIG.signal_threshold_usd
    return {
        "above_plus_T": sum(1 for v in values if v > t),
        "below_minus_T": sum(1 for v in values if v < -t),
        "inside_band": sum(1 for v in values if -t <= v <= t),
    }


def main() -> int:
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    now = now_utc()
    census_date = now.astimezone(UTC).date()
    oos_start = date.fromisoformat(CONFIG.oos_start_date)

    day_rows = parse_flow_table(
        (DATA / "access" / "farside-btc-all.html").read_text(errors="replace")
    )

    mementos: list[Memento] = []
    for label in ("recent", "all_data"):
        mementos += list(parse_timemap((DATA / "access" / f"timemap-{label}.txt").read_bytes()))

    windows = {
        d.trade_date: qualifying_window(d.trade_date)
        for d in day_rows
        if oos_start <= d.trade_date <= census_date
    }

    # Forward captures: a day whose value stood in one of THIS repository's own
    # captures strictly before its anchor. The snapshotter was armed today, so
    # this is expected to be empty at the first census and to grow daily.
    forward: dict[date, datetime] = {}
    for row in AppendOnlyLedger(SNAPSHOT_LEDGER).read().rows:
        stamp = row.get("captured_at")
        if not isinstance(stamp, str):
            continue
        captured = datetime.strptime(stamp, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=UTC)
        for day in row.get("days", []):
            if day.get("signal_usd") is None:
                continue
            trade_date = date.fromisoformat(str(day["date"]))
            start, end = qualifying_window(trade_date)
            if start <= captured < end:
                forward.setdefault(trade_date, captured)

    # Revised days: measured at A.1 Task 4's retro leg where a comparison exists.
    revised: set[date] = set()
    failed: set[date] = set()
    retro_path = REPORTS / "stage_a1" / "retro_revision.json"
    as_printed: dict[date, float] = {}
    served: set[date] | None = None
    if retro_path.exists():
        retro = json.loads(retro_path.read_text(encoding="utf-8"))
        served = set()
        for row in retro.get("rows", []):
            day = date.fromisoformat(str(row["trade_date"]))
            if row.get("state") == "source_failed":
                failed.add(day)
                continue
            if row.get("state") != "stored":
                continue
            as_printed[day] = float(row["as_printed_usd"])
            served.add(day)
            if row.get("revised"):
                revised.add(day)

    rows = build_census(
        day_rows,
        oos_start=oos_start,
        census_date=census_date,
        archive_windows=windows,
        mementos=mementos,
        forward_captures=forward,
        revised_days=frozenset(revised),
        archive_served_values=frozenset(served) if served is not None else None,
        archive_fetch_failed=frozenset(failed),
    )

    ledger = AppendOnlyLedger(CENSUS_LEDGER)
    for entry in rows:
        ledger.append({"census_run_at": iso_z(now), **entry.as_ledger_dict()})

    admissible = [r for r in rows if r.admissible]
    operational = [r for r in rows if r.state.value == "source_failed"]
    by_month: dict[str, dict[str, int]] = {}
    for entry in rows:
        key = entry.trade_date.strftime("%Y-%m")
        bucket = by_month.setdefault(key, {"days": 0, "admissible": 0})
        bucket["days"] += 1
        bucket["admissible"] += int(entry.admissible)

    reasons: dict[str, int] = {}
    for entry in rows:
        if entry.exclusion_reason:
            reasons[entry.exclusion_reason] = reasons.get(entry.exclusion_reason, 0) + 1

    # --- A.2 Task 2, the signal distribution --------------------------------
    admissible_values = [as_printed[r.trade_date] for r in admissible if r.trade_date in as_printed]
    # The full printed series is a DESCRIPTIVE reference, labelled: these are
    # the values the source serves TODAY, not the as-printed values, so they are
    # never admissible. They are reported because 333 days measure the shape of
    # the signal far better than 37, and the shape is what E2's trade-share
    # input needs. Both n's travel with their figures.
    live_values = [
        d.signal_usd
        for d in day_rows
        if oos_start <= d.trade_date <= census_date and not isinstance(d.signal_usd, Absent)
    ]

    def summarise(values: list[float], label: str) -> dict[str, object]:
        if not values:
            return {
                "label": label,
                "n": 0,
                "note": "no values; a distribution over zero days is an absence",
            }
        counts = band_counts(values)
        traded = counts["above_plus_T"] + counts["below_minus_T"]
        positions = [position(v) for v in values]
        return {
            "label": label,
            "n": len(values),
            **quantiles(values),
            **counts,
            "trade_share": traded / len(values),
            "long_days": sum(1 for p in positions if p is Position.LONG),
            "short_days": sum(1 for p in positions if p is Position.SHORT),
            "flat_days": sum(1 for p in positions if p is Position.FLAT),
        }

    out = {
        "census_run_at": iso_z(now),
        "oos_start": oos_start.isoformat(),
        "census_date": census_date.isoformat(),
        "rows": len(rows),
        "admissible": len(admissible),
        "admissible_retro_archive": sum(1 for r in admissible if r.source == "retro_archive"),
        "admissible_forward_capture": sum(1 for r in admissible if r.source == "forward_capture"),
        "revised_flagged": sum(1 for r in rows if r.revised),
        "operational_unknown": len(operational),
        "exclusion_reasons": reasons,
        "by_month": dict(sorted(by_month.items())),
        "signal_distribution_admissible": summarise(admissible_values, "admissible_as_printed"),
        "signal_distribution_live_descriptive": summarise(live_values, "live_values_descriptive"),
    }
    REPORT.write_text(json.dumps(out, indent=2, sort_keys=True), encoding="utf-8")

    print(f"census rows n = {len(rows)}; admissible n = {len(admissible)}")
    print(
        f"  retro-archive {out['admissible_retro_archive']}, "
        f"forward-capture {out['admissible_forward_capture']}"
    )
    print(f"  exclusion reasons: {reasons}")
    print(f"  revised flagged: {out['revised_flagged']}")
    print(f"  operational (admissibility unknown, never excluded): {len(operational)}")
    for key in ("signal_distribution_admissible", "signal_distribution_live_descriptive"):
        d = out[key]
        assert isinstance(d, dict)
        if d.get("n"):
            print(
                f"  {d['label']}: n = {d['n']}, median {float(d['median']) / 1e6:.1f}M, "
                f"long {d['long_days']}, short {d['short_days']}, flat {d['flat_days']}, "
                f"trade share {float(d['trade_share']):.4f}"
            )
    print(f"\nwrote {REPORT}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
