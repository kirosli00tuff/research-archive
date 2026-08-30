"""A.1 TASK 5 — historical reach, bisected per credential.

**Do not read reach from a pricing page.** Standing rule 4: a tier limit printed
on a vendor's pricing page is **documented, never measured**, and the measured
limit wins. So this bisects.

**The method.** Binary-search the **earliest registered session** for which a
one-minute aggregate request returns **bars** — not a refusal, and not a served
empty set. The three are separated by **status code plus bar count**, never by
bar count alone: standing rule 7, an error never quietly becomes a data
condition.

**The candidate set is the registered session calendar**, not a raw date range.
A market holiday returns `200` with zero bars on any tier, and bisecting over
raw dates would read that as a reach boundary. Probing only real sessions makes
a zero-bar answer mean *"this tier does not serve this session"* and nothing
else.

**The monotonicity assumption, stated because it is an assumption.** The search
assumes that if a tier serves session `S` it serves every session after `S`.
That is how a rolling history window behaves, and it is **checked rather than
trusted**: after the boundary is found, the sessions immediately before and
after it are probed directly and both results are recorded. A non-monotone
answer would show up there as a contradiction rather than as a quiet wrong
number.

**No priced field is read.** The tool reads a status code and a bar count, both
on the readable field list, and the bar count is computed inside the sealed
comparator.
"""

from __future__ import annotations

import sys
from collections.abc import Callable
from datetime import date, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from _a1r import send, wire, write_report

from orb.calendar import sessions
from orb.comparator import count_bars
from orb.config import CONFIG
from orb.redact import say
from orb.vendors import (
    alpaca_minute_bars,
    consolidated_feed,
    massive_minute_bars,
)

TICKER = "AAPL"
"""One continuously listed liquid name. Listed 1980, never delisted, never
renamed across the searched span, so a zero-bar answer is a tier fact rather
than a listing fact."""

SEARCH_START = date(2003, 1, 2)
"""Earlier than any free tier is plausibly expected to reach, on purpose: a
search whose lower bound is inside the served range cannot find the boundary."""

PROBE_MIN_AGE_DAYS = CONFIG.probe_min_age_days


def candidate_sessions(today: date) -> list[date]:
    """Every registered regular session in the searched span, oldest first."""
    latest = today - timedelta(days=PROBE_MIN_AGE_DAYS)
    return [s.day for s in sessions(SEARCH_START, latest)]


def bisect_earliest(
    days: list[date],
    served: Callable[[date], bool],
) -> tuple[int | None, int]:
    """Leftmost index whose session is served. Returns the index and the n of probes."""
    lo, hi, probes, found = 0, len(days) - 1, 0, None
    while lo <= hi:
        mid = (lo + hi) // 2
        probes += 1
        if served(days[mid]):
            found = mid
            hi = mid - 1
        else:
            lo = mid + 1
    return found, probes


def main() -> int:
    store, client, seal = wire()
    today = date.today()
    days = candidate_sessions(today)
    say(f"candidate sessions, n = {len(days)}: {days[0]} .. {days[-1]}")

    attempts: list[dict[str, object]] = []

    def probe(vendor: str, day: date) -> bool:
        iso = day.isoformat()
        if vendor == "massive":
            request = massive_minute_bars(store, TICKER, iso, iso)
        else:
            request = alpaca_minute_bars(
                store,
                TICKER,
                f"{iso}T00:00:00Z",
                f"{iso}T23:59:59Z",
                feed=consolidated_feed(),
            )
        response = send(client, request)
        record = seal.store(f"task5_{vendor}_{iso}.raw", response.body)
        counted = count_bars(response.body)
        ok = 200 <= response.status_code < 300 and counted > 0
        attempts.append(
            {
                "vendor": vendor,
                "session": iso,
                "status_code": response.status_code,
                "bar_count": counted,
                "served_byte_count": response.byte_count,
                "health": response.health.value,
                "sha256": record.sha256,
                "served": ok,
                "body_redacted": (
                    "<served payload, not recorded: a bar value never leaves the seal>"
                    if 200 <= response.status_code < 300
                    else response.refusal_fragment(500)
                ),
            }
        )
        say(
            f"  {vendor:8s} {iso} http={response.status_code} bars={counted} served={ok}"
        )
        return ok

    findings: dict[str, object] = {
        "ticker": TICKER,
        "today": today.isoformat(),
        "candidate_session_count": len(days),
        "search_span": [days[0].isoformat(), days[-1].isoformat()],
        "in_sample_start": CONFIG.in_sample_start,
        "holdout_start": CONFIG.holdout_start,
        "vendors": {},
    }

    for vendor in ("massive", "alpaca"):
        say(f"bisecting {vendor} …")
        index, probes = bisect_earliest(days, lambda d, v=vendor: probe(v, d))  # type: ignore[misc]
        if index is None:
            findings["vendors"][vendor] = {  # type: ignore[index]
                "earliest_served_session": None,
                "probes": probes,
                "verification": [],
            }
            say(f"  {vendor}: no session served across n = {len(days)} candidates")
            continue

        earliest = days[index]
        verification: list[dict[str, object]] = []
        if index > 0:
            verification.append(
                {
                    "session": days[index - 1].isoformat(),
                    "served": probe(vendor, days[index - 1]),
                }
            )
        verification.append(
            {"session": earliest.isoformat(), "served": probe(vendor, earliest)}
        )
        if index + 1 < len(days):
            verification.append(
                {
                    "session": days[index + 1].isoformat(),
                    "served": probe(vendor, days[index + 1]),
                }
            )
        findings["vendors"][vendor] = {  # type: ignore[index]
            "earliest_served_session": earliest.isoformat(),
            "sessions_served": len(days) - index,
            "probes": probes + len(verification),
            "verification": verification,
        }
        say(f"  {vendor}: earliest served session {earliest} after n = {probes} probes")

    findings["attempts"] = attempts
    write_report("task5_reach.json", findings)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
