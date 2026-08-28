"""Register entry H5, Task 4: one forward daily snapshot, run on its own.

The same code path `npl.cli.cmd_daily` invokes last, exercised alone so the
collector can be armed and verified without running any H2 collector. Writes
only under `data/h5/`; charges the shared ledger before each send; refuses if
the day has already reached the H2 soft budget.
"""

from __future__ import annotations

import json
from dataclasses import asdict

from npl.cli import DAILY_SOFT_BUDGET
from npl.clock import iso_z, now_utc
from npl.h5.collector import H5YieldedToH2, record_yield, run_daily_pass
from npl.h5.gate import load_cohorts
from npl.http import InfoClient
from npl.ledger.requests import RequestLedger
from npl.pacing import OPERATING_PACING_S
from npl.paths import H5_REPORTS
from npl.venue import Venue

REPORT = H5_REPORTS / "collector.json"


def main() -> int:
    ledger = RequestLedger()
    venue = Venue(InfoClient(ledger, pacing_s=OPERATING_PACING_S))
    try:
        result = run_daily_pass(
            venue,
            ledger,
            load_cohorts(),
            soft_budget=DAILY_SOFT_BUDGET,
            progress=lambda message: print(message, flush=True),
        )
    except H5YieldedToH2 as exc:
        record_yield(str(exc))
        print(f"h5 yielded to H2: {exc}")
        return 0
    payload = {
        "stage": "H5 Task 4 - forward collector, one verified pass",
        "ran_at": iso_z(now_utc()),
        "pass_id": result.pass_id,
        "requests_charged": result.requests_charged,
        "ledger_day_before": result.ledger_day_before,
        "ledger_day_after": result.ledger_day_after,
        "coverage": asdict(result.coverage),
    }
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(payload, indent=2, sort_keys=True))
    print(f"report -> {REPORT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
