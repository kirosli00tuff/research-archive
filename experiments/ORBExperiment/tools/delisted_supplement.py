"""A.1 TASK 6, second pass — the sample re-drawn inside the registered window.

**Why a second pass exists, recorded rather than folded in silently.** The first
pass asked Massive's reference endpoint for delisted names with
``delisted_utc.gte=2016-01-04`` and ``delisted_utc.lte=2026-06-30``. **The filter
was not honoured**: the response carries rows delisted in 2004 through 2015 and
after 2026-06-30. The first sample was therefore drawn from the **whole**
delisted list, and about a quarter of it sits **outside the registered window
and outside Alpaca's measured reach** — so those names miss on **reach**, not on
delisted coverage, and counting them would understate coverage.

**The registered threshold is a count, and a count must be measured, not scaled
up from a rate.** Standing rule 5: a synthesized value is not a measurement. So
the sample is re-drawn **inside the window only** and enlarged until the count
itself clears the registered bar or fails to.

The draw rule is unchanged and still blind: sort by delisting date then ticker,
take a systematic sample at a fixed stride, skip names the first pass already
checked.
"""

from __future__ import annotations

import json
import sys
from datetime import date, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from _a1r import REPORTS, send, wire, write_report

from orb.calendar import sessions
from orb.comparator import count_bars
from orb.config import CONFIG
from orb.integrity import IntegrityVerdict
from orb.redact import say
from orb.vendors import alpaca_minute_bars, consolidated_feed

SUPPLEMENT = 140
SESSIONS_BEFORE_DELISTING = 5


def in_window(iso: str) -> bool:
    return CONFIG.in_sample_start <= iso[:10] <= CONFIG.holdout_end


def session_before(day: date, back: int) -> date | None:
    window = [
        s.day for s in sessions(day - timedelta(days=45), day - timedelta(days=1))
    ]
    return window[-back] if len(window) >= back else None


def main() -> int:
    store, client, seal = wire()
    first = json.loads((REPORTS / "task6_delisted.json").read_text())
    rows = first["enumerated_names"]
    already = {c["ticker"] for c in first["checks"] if c["vendor"] == "alpaca"}

    windowed = sorted(
        (r for r in rows if in_window(r["delisted_utc"])),
        key=lambda r: (r["delisted_utc"], r["ticker"]),
    )
    say(
        f"enumerated n = {len(rows)}, inside the registered window n = "
        f"{len(windowed)}, already checked n = {len(already)}"
    )

    stride = max(1, len(windowed) // SUPPLEMENT)
    picked = [r for r in windowed[::stride] if r["ticker"] not in already][:SUPPLEMENT]
    say(f"supplementary sample n = {len(picked)}, stride {stride}")

    checks: list[dict[str, object]] = []
    for entry in picked:
        delisted_day = date.fromisoformat(entry["delisted_utc"][:10])
        probe_day = session_before(delisted_day, SESSIONS_BEFORE_DELISTING)
        if probe_day is None:
            continue
        iso = probe_day.isoformat()
        response = send(
            client,
            alpaca_minute_bars(
                store,
                entry["ticker"],
                f"{iso}T00:00:00Z",
                f"{iso}T23:59:59Z",
                feed=consolidated_feed(),
            ),
        )
        record = seal.store(f"task6b_alpaca_{entry['ticker']}_{iso}.raw", response.body)
        counted = count_bars(response.body)
        checks.append(
            {
                "vendor": "alpaca",
                "ticker": entry["ticker"],
                "delisted_utc": entry["delisted_utc"],
                "probe_session": iso,
                "status_code": response.status_code,
                "bar_count": counted,
                "served": 200 <= response.status_code < 300 and counted > 0,
                "health": response.health.value,
                "sha256": record.sha256,
            }
        )

    prior = [
        c
        for c in first["checks"]
        if c["vendor"] == "alpaca" and in_window(str(c["delisted_utc"]))
    ]
    combined = prior + checks
    served = sum(1 for c in combined if c["served"])

    def verdict(count: int) -> str:
        if count >= CONFIG.delisted_pass_min_count:
            return IntegrityVerdict.PASS.value
        if count >= CONFIG.delisted_partial_min_count:
            return IntegrityVerdict.PARTIAL.value
        return IntegrityVerdict.FAIL.value

    findings = {
        "window": [CONFIG.in_sample_start, CONFIG.holdout_end],
        "enumerated_total": len(rows),
        "enumerated_inside_window": len(windowed),
        "first_pass_in_window_checks": len(prior),
        "supplementary_checks": len(checks),
        "combined_in_window_checks": len(combined),
        "delisted_names_with_intraday_history": served,
        "served_share": served / len(combined) if combined else 0.0,
        "registered_verdict": verdict(served),
        "checks": checks,
    }
    say(
        f"combined in-window sample n = {len(combined)}, served = {served}, "
        f"share = {findings['served_share']:.4f}, verdict = {findings['registered_verdict']}"
    )
    write_report("task6b_delisted_in_window.json", findings)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
