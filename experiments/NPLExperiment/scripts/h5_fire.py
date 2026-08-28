"""Register entry H5, Task 5: fire the outcome map.

Reads only H5 stores. Fires the Section 6 map twice — once on the registered
basis (mark against the venue's own oracle, contemporaneous) and once on the
named secondary (the venue premium index, retrospective) — and records each
verdict with every input figure beside it.

No network call. No return is read anywhere on this path.
"""

from __future__ import annotations

import json
from collections import Counter
from dataclasses import asdict

from npl.clock import MS_PER_DAY, iso_z, now_utc
from npl.config import CONFIG
from npl.h5 import outcome as h5out
from npl.h5.census import load_census
from npl.h5.listing import STATUS_LIVE
from npl.h5.stats import summarize
from npl.h5.stores import read_rows
from npl.paths import H5_CENSUS, H5_REPORTS, H5_SNAPSHOTS

REPORT = H5_REPORTS / "verdict.json"


def _all_observation_rows() -> list[dict[str, object]]:
    """Every H5 basis observation on disk: the census passes and every forward pass."""
    rows: list[dict[str, object]] = []
    for path in (H5_CENSUS, H5_SNAPSHOTS):
        if path.exists():
            rows.extend(r for r in read_rows(path) if r.get("kind") is None)
    return rows


def main() -> int:
    today = now_utc().date()
    census = load_census()
    live = [r for r in census if r.listing_status == STATUS_LIVE]
    with_reference = [r for r in live if r.reference_served]
    funding_served = sum(1 for r in with_reference if r.funding_history_state == "stored")

    observations = _all_observation_rows()
    live_coins = {r.coin for r in with_reference}
    by_tag: dict[str, list[float]] = {}
    days_by_coin: dict[str, set[int]] = {}
    snapshots: Counter[str] = Counter()
    for row in observations:
        coin = str(row["coin"])
        if coin not in live_coins or str(row["listing_status"]) != STATUS_LIVE:
            continue
        snapshots[str(row["snapshot_id"])] += 1
        basis = row.get("basis_bp")
        days_by_coin.setdefault(coin, set()).add(int(str(row["at_ms"])) // MS_PER_DAY)
        if basis is None:
            continue
        by_tag.setdefault(str(row["session_tag"]), []).append(float(str(basis)))

    tag_summaries = {
        tag: summarize(list(values), h5out.cost_floor_bp(), h5out.viable_threshold_bp())
        for tag, values in sorted(by_tag.items())
    }
    medians = {tag: s.median_abs_bp for tag, s in tag_summaries.items() if s.median_abs_bp}
    n_by_tag = {tag: s.n for tag, s in tag_summaries.items()}
    covered = [len(days) for days in days_by_coin.values()]
    meeting = sum(1 for d in covered if d >= CONFIG.h5_min_coverage_days)

    primary = h5out.fire(
        series_kind=h5out.SERIES_REGISTERED_BASIS,
        instruments_with_reference=len(with_reference),
        instruments_meeting_coverage=meeting,
        median_abs_bp_by_tag=medians,
        n_by_tag=n_by_tag,
        funding_served_instruments=funding_served,
    )

    retro_path = H5_REPORTS / "retro.json"
    retro = json.loads(retro_path.read_text(encoding="utf-8")) if retro_path.exists() else {}
    retro_live_meeting = int(retro.get("live_instruments_meeting_30d_coverage", 0))
    retro_medians = {
        tag: float(summary["median_abs_bp"])
        for tag, summary in retro.get("pooled_by_session_tag_live_only", {}).items()
        if summary.get("median_abs_bp") is not None
    }
    retro_n = {
        tag: int(summary["n"])
        for tag, summary in retro.get("pooled_by_session_tag_live_only", {}).items()
    }
    secondary = h5out.fire(
        series_kind=h5out.SERIES_SECONDARY_DEVIATION,
        instruments_with_reference=int(retro.get("instruments_eligible_live", 0)),
        instruments_meeting_coverage=retro_live_meeting,
        median_abs_bp_by_tag=retro_medians,
        n_by_tag=retro_n,
        funding_served_instruments=int(retro.get("instruments_eligible_live", 0)),
    )

    projection: dict[str, object]
    try:
        fire_on = h5out.projected_fire_date(covered, today)
        projection = {
            "passes_needed": h5out.passes_needed(covered),
            "projected_fire_date": fire_on.isoformat(),
            "covered_days_binding_instrument": sorted(covered, reverse=True)[
                CONFIG.h5_min_instruments_with_reference - 1
            ],
            "note": (
                "one daily pass adds one covered day to every live instrument; the "
                f"{CONFIG.h5_min_instruments_with_reference}th best-covered instrument binds"
            ),
        }
    except h5out.CensusWindowNotProjectable as exc:
        projection = {"projected_fire_date": None, "refusal": str(exc)}

    payload = {
        "stage": "H5 Task 5 - the outcome map, fired",
        "fired_at": iso_z(now_utc()),
        "today": today.isoformat(),
        "floor_bp": h5out.cost_floor_bp(),
        "viable_bp": h5out.viable_threshold_bp(),
        "primary_registered_basis": asdict(primary),
        "secondary_deviation": asdict(secondary),
        "inputs": {
            "instruments_enumerated": len(census),
            "instruments_resolved": sum(1 for r in census if r.resolution_state == "resolved"),
            "instruments_live": len(live),
            "live_with_served_reference": len(with_reference),
            "live_with_funding_served": funding_served,
            "funding_share": funding_served / len(with_reference) if with_reference else 0.0,
            "snapshots_counted": dict(snapshots),
            "observations_counted": sum(n_by_tag.values()),
            "instruments_meeting_coverage": meeting,
            "covered_days_max": max(covered) if covered else 0,
            "by_session_tag": {tag: asdict(s) for tag, s in tag_summaries.items()},
        },
        "census_window": projection,
        "retrospective_inputs": {
            "instruments_eligible": retro.get("instruments_eligible"),
            "instruments_eligible_live": retro.get("instruments_eligible_live"),
            "instruments_excluded_quarantined": retro.get("instruments_excluded_quarantined"),
            "observations_served": retro.get("observations_served"),
            "live_instruments_meeting_30d_coverage": retro_live_meeting,
            "pooled_by_session_tag": retro.get("pooled_by_session_tag"),
        },
    }
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(payload, indent=2, sort_keys=True))
    print(f"report -> {REPORT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
