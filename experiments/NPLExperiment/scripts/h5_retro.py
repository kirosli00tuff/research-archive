"""Register entry H5, Task 3: the retrospective deviation read.

Only the named secondary series exists historically (Amendment H5-1 Change
2): the venue serves `premium` hourly, and no historical mark or oracle. The
read is gated — no generating-sample, fresh-plan, or H2-pair coin reaches
the network — and it never touches a funding rate.

Writes per-instrument and pooled summaries under `data/h5/`. The raw hourly
series is not retained: it is re-derivable from the venue, and 500k fsynced
ledger rows would be a cost with no evidentiary value.
"""

from __future__ import annotations

import json
from dataclasses import asdict

from npl.clock import iso_z, now_utc, utc_ms
from npl.config import CONFIG
from npl.h5.census import load_census
from npl.h5.gate import load_cohorts
from npl.h5.listing import STATUS_LIVE
from npl.h5.outcome import cost_floor_bp, viable_threshold_bp
from npl.h5.retro import run_retrospective
from npl.h5.spend import retro_window_ms
from npl.h5.stats import summarize
from npl.h5.stores import h5_store
from npl.http import InfoClient
from npl.ledger.requests import RequestLedger
from npl.pacing import OPERATING_PACING_S
from npl.paths import H5_REPORTS, H5_RETRO
from npl.venue import Venue

REPORT = H5_REPORTS / "retro.json"


def main() -> int:
    floor, viable = cost_floor_bp(), viable_threshold_bp()
    ledger = RequestLedger()
    today = now_utc().date().isoformat()
    before = ledger.spent_on(today)
    venue = Venue(InfoClient(ledger, pacing_s=OPERATING_PACING_S))
    cohorts = load_cohorts()

    census = load_census()
    resolved = [r for r in census if r.resolution_state == "resolved"]
    # Amendment H5-2 Change 2: a delisted instrument's HISTORY is data from
    # when it traded, so it is admitted here with its status recorded — while
    # the contemporaneous universe (Change 1) excludes it.
    eligible = [r for r in resolved if r.reference_served and not r.quarantined]
    quarantined = [r for r in resolved if r.reference_served and r.quarantined]
    status_of = {r.coin: r.listing_status for r in census}
    coins = sorted(r.coin for r in eligible)
    live_eligible = [r for r in eligible if r.listing_status == STATUS_LIVE]
    print(
        f"census: {len(census)} instruments, {len(resolved)} resolved, "
        f"{len(eligible)} eligible for the retrospective read "
        f"({len(live_eligible)} live), {len(quarantined)} excluded_quarantined",
        flush=True,
    )

    now_ms = utc_ms(now_utc())
    start_ms, end_ms = retro_window_ms(now_ms)
    series = run_retrospective(
        venue, coins, cohorts, start_ms, end_ms, progress=lambda m: print(m, flush=True)
    )

    store = h5_store(H5_RETRO)
    run_id = f"h5-retro-{iso_z(now_utc())}"
    pooled: dict[str, list[float]] = {}
    pooled_absent: dict[str, int] = {}
    pooled_live: dict[str, list[float]] = {}
    per_instrument: list[dict[str, object]] = []
    for one in series:
        by_tag: dict[str, list[float]] = {}
        by_tag_absent: dict[str, int] = {}
        for obs in one.observations:
            value = obs.deviation_bp
            if isinstance(value, float):
                by_tag.setdefault(obs.session_tag, []).append(value)
                pooled.setdefault(obs.session_tag, []).append(value)
                if status_of.get(one.coin) == STATUS_LIVE:
                    pooled_live.setdefault(obs.session_tag, []).append(value)
            else:
                by_tag_absent[obs.session_tag] = by_tag_absent.get(obs.session_tag, 0) + 1
                pooled_absent[obs.session_tag] = pooled_absent.get(obs.session_tag, 0) + 1
        row: dict[str, object] = {
            "kind": "instrument_summary",
            "run_id": run_id,
            "coin": one.coin,
            "listing_status": status_of.get(one.coin, ""),
            "state": one.state,
            "pages_fetched": one.pages_fetched,
            "n": one.n,
            "n_observations": len(one.observations),
            "covered_days": one.covered_days,
            "first_time_ms": one.first_time_ms,
            "last_time_ms": one.last_time_ms,
        }
        store.append(row)
        per_instrument.append(row)
        for tag, values in sorted(by_tag.items()):
            summary = summarize(list(values), floor, viable)
            store.append(
                {
                    "kind": "instrument_tag_summary",
                    "run_id": run_id,
                    "coin": one.coin,
                    "session_tag": tag,
                    "n_absent": by_tag_absent.get(tag, 0),
                    "iqr_abs_bp": summary.iqr_abs_bp,
                    **asdict(summary),
                }
            )

    pooled_summaries: dict[str, dict[str, object]] = {}
    for tag, values in sorted(pooled.items()):
        summary = summarize(list(values), floor, viable)
        one_summary: dict[str, object] = {"iqr_abs_bp": summary.iqr_abs_bp, **asdict(summary)}
        pooled_summaries[tag] = one_summary
        store.append(
            {
                "kind": "pooled_tag_summary",
                "run_id": run_id,
                "session_tag": tag,
                "n_absent": pooled_absent.get(tag, 0),
                **one_summary,
            }
        )

    pooled_live_summaries: dict[str, dict[str, object]] = {}
    for tag, values in sorted(pooled_live.items()):
        summary = summarize(list(values), floor, viable)
        pooled_live_summaries[tag] = {"iqr_abs_bp": summary.iqr_abs_bp, **asdict(summary)}
        store.append(
            {
                "kind": "pooled_tag_summary_live_only",
                "run_id": run_id,
                "session_tag": tag,
                **pooled_live_summaries[tag],
            }
        )

    after = ledger.spent_on(today)
    instruments_meeting_coverage = sum(
        1 for one in series if one.covered_days >= CONFIG.h5_min_coverage_days and one.n > 0
    )
    payload = {
        "stage": "H5 Task 3 - retrospective deviation (named secondary: venue premium)",
        "ran_at": iso_z(now_utc()),
        "run_id": run_id,
        "window_start_ms": start_ms,
        "window_end_ms": end_ms,
        "requests_charged": after - before,
        "instruments_eligible": len(eligible),
        "instruments_eligible_live": len(live_eligible),
        "instruments_excluded_quarantined": len(quarantined),
        "instruments_with_any_observation": sum(1 for s in series if s.n > 0),
        "instruments_meeting_30d_coverage": instruments_meeting_coverage,
        "observations_total": sum(len(s.observations) for s in series),
        "observations_served": sum(s.n for s in series),
        "floor_bp": floor,
        "viable_bp": viable,
        "pooled_by_session_tag": pooled_summaries,
        "pooled_by_session_tag_live_only": pooled_live_summaries,
        "live_instruments_meeting_30d_coverage": sum(
            1
            for one in series
            if status_of.get(one.coin) == STATUS_LIVE
            and one.covered_days >= CONFIG.h5_min_coverage_days
            and one.n > 0
        ),
        "pooled_absent_by_session_tag": pooled_absent,
        "per_instrument": per_instrument,
    }
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    brief = {k: v for k, v in payload.items() if k != "per_instrument"}
    print(json.dumps(brief, indent=2, sort_keys=True))
    print(f"report -> {REPORT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
