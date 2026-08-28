"""Register entry H5, Task 2: instrument resolution and the access census.

One pass over every HIP-3 dex. Charges the shared request ledger before each
send, at the measured operating pacing. Writes only under `data/h5/`.
"""

from __future__ import annotations

import json
from dataclasses import asdict
from pathlib import Path

from npl.clock import iso_z, now_utc
from npl.h5.census import census_summary, run_census
from npl.h5.gate import load_cohorts
from npl.h5.spend import daily_pass_budget, share_of_daily_cap
from npl.http import InfoClient
from npl.ledger.requests import RequestLedger
from npl.pacing import OPERATING_PACING_S
from npl.paths import H5_REPORTS
from npl.venue import Venue

REPORT = H5_REPORTS / "census.json"


def main() -> int:
    ledger = RequestLedger()
    today = now_utc().date().isoformat()
    before = ledger.spent_on(today)
    venue = Venue(InfoClient(ledger, pacing_s=OPERATING_PACING_S))
    cohorts = load_cohorts()
    print(
        f"cohorts: generating={len(cohorts.generating_sample)} "
        f"fresh={len(cohorts.fresh_plan)} h2_pairs={len(cohorts.h2_pairs)}",
        flush=True,
    )
    rows = run_census(venue, cohorts, progress=lambda m: print(m, flush=True))
    after = ledger.spent_on(today)
    summary = census_summary(rows)
    resolved_n = sum(1 for r in rows if r.resolution_state == "resolved")
    budget = daily_pass_budget(dexs=len({r.dex for r in rows}), instruments=resolved_n)
    payload = {
        "stage": "H5 Task 2 - instrument resolution and access census",
        "ran_at": iso_z(now_utc()),
        "requests_charged": after - before,
        "ledger_day_before": before,
        "ledger_day_after": after,
        "projected_daily_pass_requests": budget.total,
        "projected_share_of_daily_cap": round(share_of_daily_cap(budget), 5),
        **summary,
    }
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(
        json.dumps(
            {k: payload[k] for k in sorted(payload) if k != "served_field_sets_resolved"},
            indent=2,
        )
    )
    print(f"report -> {REPORT}")
    Path(REPORT.with_suffix(".rows.json")).write_text(
        json.dumps([asdict(r) for r in rows], indent=1, sort_keys=True, default=list) + "\n",
        encoding="utf-8",
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
