"""A.1 TASK 4 (amendment pass) — the Alpaca rate ceiling, measured or absent.

**Alpaca is the primary bar vendor (ADR-023), so its ceiling is the one that
governs collection.** A.1 TASK 7 measured Massive at **5.00 per minute** — first
refusal at request 6 of 8, on both endpoints, `n = 16` — and **did not reach
Alpaca's**: 25 of 25 admitted at **134.05 per minute**, `n = 25`, no refusal.
ADR-026 recorded that as `None` rather than as a large number. **An unreached
ceiling is an unmeasured figure, not headroom**, and this tool exists to try
again.

**Why the registered sequential protocol cannot reach it, stated before the
run.** The A.1 TASK 7 cell requested 0.2 s spacing — 300 per minute — and
achieved **134.05**. The gap is **per-request latency**: a sequential client
sends at most `60 / latency` per minute whatever spacing it asks for. Alpaca's
documented free-tier figure is **200 per minute** (carried, never measured), so
**a single-threaded escalation is structurally incapable of attempting the
documented limit, let alone exceeding it.** Escalating spacing further measures
latency, not a limiter.

**The extension, registered rather than slipped in.** The protocol gains
**bounded concurrency cells** — 2, then 4, then 8 workers — after the sequential
cells. Two workers already attempt roughly 270 per minute, above the documented
200. Every cell **stops at its first refusal**, so the escalation ends the moment
it has what it came for: **the refusal shape and the sustained admitted rate.**
It is bounded at `n` per cell and it is not a load test.

**The charge happens before every send, under a lock**, so the registered daily
cap holds across workers exactly as it holds sequentially. **The recorded terms
permit this**: `docs/ACCESS.md` records `data.alpaca.markets/robots.txt` as a
`401` behind auth and `alpaca.markets/robots.txt` as an HTML 404 page — **no
prohibition is stated on either**, and the access verdict is
`REQUIRES_CREDENTIAL`, not `REFUSED_BY_TERMS`.

**If no cell refuses, the result is `Absent(not_measured)`** carrying the
**maximum rate actually attempted and its n** — never an unbounded or high
ceiling — and the operating pace is set from the maximum attempted rate rather
than from an assumption.
"""

from __future__ import annotations

import sys
import threading
import time
from collections import Counter
from collections.abc import Callable
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))

from _a1r import DATA, send, wire, write_report

from orb.http import PacedClient, Response
from orb.ledger import RequestLedger
from orb.redact import say
from orb.vendors import (
    ALPACA,
    ALPACA_DOCUMENTED_PER_MINUTE,
    PROVISIONAL_DAILY_CAPS,
    VendorRequest,
    alpaca_minute_bars,
    consolidated_feed,
)

PACE_KEY = "alpaca:bars"
PROBE_START_ISO = "2026-07-15T13:30:00Z"
PROBE_END_ISO = "2026-07-15T13:35:00Z"
"""The **identical** request shape A.1 TASK 7 used, so the cells are comparable.

The window is post-holdout, so it also sits inside the amended carve-out; the
tool parses no body in any case.
"""


class LockedLedger:
    """The request ledger, serialised across workers.

    ``charge`` reads the ledger and then appends. Run concurrently and unguarded,
    two workers could both observe ``spent < cap`` and both append, overshooting
    the registered cap. **The cap charges before sending, and that property must
    survive concurrency or the concurrency is not permitted.**
    """

    def __init__(self, ledger: RequestLedger) -> None:
        self._ledger = ledger
        self._lock = threading.Lock()

    def cap(self, vendor: str) -> int:
        with self._lock:
            return self._ledger.cap(vendor)

    def spent_today(self, vendor: str, day: str) -> int:
        with self._lock:
            return self._ledger.spent_today(vendor, day)

    def charge(self, vendor: str, day: str, endpoint: str) -> None:
        with self._lock:
            self._ledger.charge(vendor, day, endpoint)


@dataclass(frozen=True, slots=True)
class Cell:
    label: str
    workers: int
    spacing_s: float
    n: int


CELLS: tuple[Cell, ...] = (
    Cell("sequential, 0.2 s spacing (A.1 TASK 7 shape)", 1, 0.2, 25),
    Cell("sequential, 0.05 s spacing", 1, 0.05, 40),
    Cell("sequential, no spacing", 1, 0.0, 60),
    Cell("2 workers, no spacing", 2, 0.0, 80),
    Cell("4 workers, no spacing", 4, 0.0, 120),
    Cell("8 workers, no spacing", 8, 0.0, 160),
)
"""Worst case `n = 485` requests, against a registered daily cap of 2,000."""


def run_cell(
    cell: Cell, build: Callable[[], VendorRequest], ledger: LockedLedger
) -> dict[str, Any]:
    codes: Counter[int] = Counter()
    fragments: set[str] = set()
    first_refusal_at: int | None = None
    refusal_lock = threading.Lock()
    stop = threading.Event()
    completed = 0

    def one(index: int) -> Response | None:
        if stop.is_set():
            return None
        client = PacedClient(ledger, {PACE_KEY: cell.spacing_s}, timeout_s=60.0)  # type: ignore[arg-type]
        response = send(client, build())
        with refusal_lock:
            nonlocal first_refusal_at, completed
            completed += 1
            codes[response.status_code] += 1
            if not (200 <= response.status_code < 300):
                fragments.add(response.refusal_fragment(300))
                if first_refusal_at is None:
                    first_refusal_at = index + 1
                stop.set()
        return response

    started = time.monotonic()
    if cell.workers == 1:
        for index in range(cell.n):
            if stop.is_set():
                break
            one(index)
    else:
        with ThreadPoolExecutor(max_workers=cell.workers) as pool:
            list(pool.map(one, range(cell.n)))
    elapsed = time.monotonic() - started

    sent = completed
    admitted = sum(count for code, count in codes.items() if 200 <= code < 300)
    attempted_rate = round(sent / elapsed * 60, 2) if elapsed else 0.0
    row: dict[str, Any] = {
        "cell": cell.label,
        "workers": cell.workers,
        "requested_spacing_s": cell.spacing_s,
        "n_planned": cell.n,
        "n_sent": sent,
        "elapsed_s": round(elapsed, 2),
        "attempted_rate_per_min": attempted_rate,
        "admitted": admitted,
        "sustained_admitted_rate_per_min": (
            round(admitted / elapsed * 60, 2) if elapsed else 0.0
        ),
        "status_distribution": dict(codes),
        "refused_429": codes.get(429, 0),
        "first_refusal_at_request": first_refusal_at,
        "ceiling_reached": first_refusal_at is not None,
        "refusal_payloads_verbatim_redacted": sorted(fragments),
    }
    say(
        f"  {cell.label:<44} sent={sent:>4} elapsed={elapsed:6.2f}s "
        f"attempted={attempted_rate:>7.2f}/min admitted={admitted:>4} "
        f"codes={dict(codes)} refusal_at={first_refusal_at}"
    )
    return row


def main() -> int:
    store, _client, _seal = wire()
    ledger = LockedLedger(
        RequestLedger(DATA / "requests.jsonl", dict(PROVISIONAL_DAILY_CAPS))
    )

    def build() -> VendorRequest:
        return alpaca_minute_bars(
            store, "AAPL", PROBE_START_ISO, PROBE_END_ISO, feed=consolidated_feed()
        )

    say(
        f"escalating {PACE_KEY}; documented {ALPACA_DOCUMENTED_PER_MINUTE}/min (carried)"
    )
    rows: list[dict[str, Any]] = []
    for cell in CELLS:
        row = run_cell(cell, build, ledger)
        rows.append(row)
        if row["ceiling_reached"]:
            say("  ceiling reached; the escalation stops here rather than pressing on")
            break

    reached = [r for r in rows if r["ceiling_reached"]]
    max_attempted = max((float(r["attempted_rate_per_min"]) for r in rows), default=0.0)
    max_attempted_row = next(
        (r for r in rows if float(r["attempted_rate_per_min"]) == max_attempted), None
    )
    max_admitted = max(
        (float(r["sustained_admitted_rate_per_min"]) for r in rows), default=0.0
    )
    total_sent = sum(int(r["n_sent"]) for r in rows)

    if reached:
        cell = reached[0]
        ceiling = float(cell["sustained_admitted_rate_per_min"])
        findings: dict[str, Any] = {
            "ceiling_state": "MEASURED",
            "measured_ceiling_per_minute": ceiling,
            "measured_ceiling_basis": (
                "the sustained admitted rate in the first cell that drew a "
                f"refusal, at request {cell['first_refusal_at_request']} of "
                f"{cell['n_planned']} planned"
            ),
            "first_refusal_at_request": cell["first_refusal_at_request"],
            "refusal_payloads_verbatim_redacted": cell[
                "refusal_payloads_verbatim_redacted"
            ],
            "sustained_admitted_rate_per_min": ceiling,
            "operating_pace_per_minute": round(ceiling / 2.0, 2),
            "operating_spacing_s": (round(120.0 / ceiling, 3) if ceiling else None),
            "operating_pace_basis": "measured: half of a measured refusal boundary",
        }
    else:
        findings = {
            "ceiling_state": "ABSENT_NOT_MEASURED",
            "measured_ceiling_per_minute": None,
            "absence": (
                "Absent(not_measured): the escalation terminated without a "
                f"refusal. n = {total_sent} requests across "
                f"{len(rows)} cells, maximum rate actually attempted "
                f"{max_attempted} per minute over n = "
                f"{max_attempted_row['n_sent'] if max_attempted_row else 0} "
                "requests in that cell. This is NOT a statement that the "
                "ceiling is high or unbounded; it is a statement that this "
                "repository has not measured one."
            ),
            "max_rate_attempted_per_min": max_attempted,
            "max_rate_attempted_n": (
                int(max_attempted_row["n_sent"]) if max_attempted_row else 0
            ),
            "max_sustained_admitted_rate_per_min": max_admitted,
            "operating_pace_per_minute": round(max_attempted / 2.0, 2),
            "operating_spacing_s": (
                round(120.0 / max_attempted, 3) if max_attempted else None
            ),
            "operating_pace_basis": (
                "unmeasured ceiling; half of the MAXIMUM RATE ACTUALLY "
                "ATTEMPTED, never half of an assumption or of a documented "
                "figure"
            ),
        }

    findings |= {
        "kind": "alpaca_rate_ceiling",
        "vendor": ALPACA,
        "pace_key": PACE_KEY,
        "documented_per_minute": ALPACA_DOCUMENTED_PER_MINUTE,
        "documented_label": "carried, vendor documentation, never measured",
        "total_requests_sent": total_sent,
        "cells": rows,
    }
    write_report("task4b_alpaca_ceiling.json", findings)
    say("")
    say(f"CEILING STATE: {findings['ceiling_state']}")
    say(
        f"  operating pace {findings['operating_pace_per_minute']}/min "
        f"(spacing {findings['operating_spacing_s']} s) — {findings['operating_pace_basis']}"
    )
    say(f"  total requests sent: n = {total_sent}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
