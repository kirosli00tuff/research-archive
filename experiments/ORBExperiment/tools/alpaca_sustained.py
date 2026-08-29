"""A.1 TASK 4 (amendment pass), phase 2 — burst allowance against sustained rate.

**`tools/alpaca_ceiling.py` reached a refusal boundary, and the whole escalation
fit inside one rolling minute.** 391 requests sent, **384 admitted**, first `429`
at cumulative request **385**, elapsed **55.96 s** — `{"message": "too many
requests."}`. That measures a **burst allowance of 384 requests**. It does
**not** measure a sustained per-minute ceiling, and the two are different
numbers: **a token bucket of capacity ≈ 400 refilling at the documented 200 per
minute would produce exactly the observation above.**

Recording 411.72 per minute as *the ceiling* would be the ADR-026 error running
the other way — turning an unmeasured quantity into a large number — so this
phase measures the quantity that was missing.

**The test.** After a cooldown long enough for a per-minute bucket to refill,
send at approximately the **documented 200 per minute** for **longer than one
minute**, and stop at the first refusal. A run that sustains it with zero
refusals establishes that the documented figure is achievable as a *rate*; a run
that refuses partway establishes a sustained ceiling **below** it, and the
elapsed time and cumulative count at the refusal say where.

**Bounded on purpose.** `n = 250` over roughly 75 seconds. It is not a load test,
it charges the registered ledger before every send, and it stops the moment it
has an answer.
"""

from __future__ import annotations

import json
import sys
import threading
import time
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))

from _a1r import DATA, REPORTS, send, wire, write_report

from orb.http import PacedClient
from orb.ledger import RequestLedger
from orb.redact import say
from orb.vendors import (
    ALPACA,
    ALPACA_DOCUMENTED_PER_MINUTE,
    PROVISIONAL_DAILY_CAPS,
    alpaca_minute_bars,
    consolidated_feed,
)

PACE_KEY = "alpaca:bars"

REPORT = REPORTS / "task4b_alpaca_ceiling.json"
PROBE_START_ISO = "2026-07-15T13:30:00Z"
PROBE_END_ISO = "2026-07-15T13:35:00Z"

COOLDOWN_S = 75.0
"""Longer than one minute, so a per-minute bucket has refilled before the test."""

TARGET_PER_MINUTE = float(ALPACA_DOCUMENTED_PER_MINUTE)
"""The documented figure, tested as a **rate** rather than accepted as one."""

SUSTAINED_N = 250
"""≈75 s at the target rate — longer than one rolling minute, and bounded."""

WORKERS = 2
"""Two, because a single-threaded client is latency-bound near 227 per minute."""


def main() -> int:
    store, _client, _seal = wire()
    ledger = RequestLedger(DATA / "requests.jsonl", dict(PROVISIONAL_DAILY_CAPS))
    lock = threading.Lock()
    stop = threading.Event()
    codes: Counter[int] = Counter()
    fragments: set[str] = set()
    first_refusal_at: int | None = None
    first_refusal_elapsed_s: float | None = None
    completed = 0

    spacing = WORKERS * 60.0 / TARGET_PER_MINUTE
    say(
        f"cooldown {COOLDOWN_S:.0f} s so a per-minute bucket refills, then "
        f"n = {SUSTAINED_N} at a target {TARGET_PER_MINUTE:.0f}/min "
        f"({WORKERS} workers, {spacing:.3f} s spacing each)"
    )
    time.sleep(COOLDOWN_S)
    started = time.monotonic()

    def one(index: int) -> None:
        nonlocal first_refusal_at, first_refusal_elapsed_s, completed
        if stop.is_set():
            return
        with lock:
            ledger.charge(ALPACA, time.strftime("%Y-%m-%d", time.gmtime()), PACE_KEY)
        # Pace against the schedule rather than against the previous send, so a
        # slow response does not silently reduce the rate being tested.
        due = started + index * (60.0 / TARGET_PER_MINUTE)
        delay = due - time.monotonic()
        if delay > 0:
            time.sleep(delay)
        if stop.is_set():
            return
        client = PacedClient(ledger, {PACE_KEY: 0.0}, timeout_s=60.0)
        client._ledger = _NoCharge(ledger)  # type: ignore[assignment]  # already charged
        response = send(
            client,
            alpaca_minute_bars(
                store, "AAPL", PROBE_START_ISO, PROBE_END_ISO, feed=consolidated_feed()
            ),
        )
        with lock:
            completed += 1
            codes[response.status_code] += 1
            if not (200 <= response.status_code < 300):
                fragments.add(response.refusal_fragment(300))
                if first_refusal_at is None:
                    first_refusal_at = completed
                    first_refusal_elapsed_s = round(time.monotonic() - started, 2)
                stop.set()

    with ThreadPoolExecutor(max_workers=WORKERS) as pool:
        list(pool.map(one, range(SUSTAINED_N)))
    elapsed = time.monotonic() - started

    admitted = sum(count for code, count in codes.items() if 200 <= code < 300)
    sustained_rate = round(admitted / elapsed * 60, 2) if elapsed else 0.0
    refused = first_refusal_at is not None

    cell = {
        "cell": (
            f"SUSTAINED: {WORKERS} workers, scheduled at "
            f"{TARGET_PER_MINUTE:.0f}/min, after a {COOLDOWN_S:.0f} s cooldown"
        ),
        "workers": WORKERS,
        "target_per_minute": TARGET_PER_MINUTE,
        "cooldown_s": COOLDOWN_S,
        "n_planned": SUSTAINED_N,
        "n_sent": completed,
        "elapsed_s": round(elapsed, 2),
        "attempted_rate_per_min": round(completed / elapsed * 60, 2)
        if elapsed
        else 0.0,
        "admitted": admitted,
        "sustained_admitted_rate_per_min": sustained_rate,
        "status_distribution": dict(codes),
        "refused_429": codes.get(429, 0),
        "first_refusal_at_request": first_refusal_at,
        "first_refusal_elapsed_s": first_refusal_elapsed_s,
        "ran_longer_than_one_rolling_minute": elapsed > 60.0,
        "ceiling_reached": refused,
        "refusal_payloads_verbatim_redacted": sorted(fragments),
    }
    say(
        f"  sent={completed} elapsed={elapsed:.2f}s admitted={admitted} "
        f"sustained={sustained_rate}/min codes={dict(codes)} "
        f"refusal_at={first_refusal_at}"
    )

    findings: dict[str, Any] = json.loads(REPORT.read_text(encoding="utf-8"))
    burst_admitted = sum(int(c["admitted"]) for c in findings["cells"])
    burst_elapsed = sum(float(c["elapsed_s"]) for c in findings["cells"])
    burst_rate = round(burst_admitted / burst_elapsed * 60, 2)

    if refused:
        ceiling = sustained_rate
        state = "MEASURED_SUSTAINED"
        basis = (
            f"the sustained admitted rate up to the first refusal, at "
            f"request {first_refusal_at} after {first_refusal_elapsed_s} s of "
            "continuous sending, in a window longer than one rolling minute"
        )
    else:
        ceiling = sustained_rate
        state = "MEASURED_SUSTAINED_AT_OR_ABOVE"
        basis = (
            f"n = {completed} requests admitted with 0 refusals over "
            f"{elapsed:.2f} s — longer than one rolling minute — so the "
            f"sustained ceiling is AT OR ABOVE {sustained_rate}/min and is not "
            "known exactly. This is a lower bound, never a ceiling."
        )

    operating = min(ceiling / 2.0, TARGET_PER_MINUTE / 2.0)
    findings |= {
        "ceiling_state": state,
        "burst_allowance_requests": burst_admitted,
        "burst_allowance_window_s": round(burst_elapsed, 2),
        "burst_rate_per_min_over_the_escalation": burst_rate,
        "burst_note": (
            "The escalation fit inside one rolling minute, so 384 admitted in "
            "55.96 s is a BURST ALLOWANCE, not a sustained ceiling. A token "
            "bucket of capacity near 400 refilling at the documented 200/min "
            "would produce exactly that observation."
        ),
        "measured_sustained_ceiling_per_minute": ceiling,
        "measured_sustained_ceiling_basis": basis,
        "sustained_cell": cell,
        "operating_pace_per_minute": round(operating, 2),
        "operating_spacing_s": round(60.0 / operating, 3),
        "operating_pace_basis": (
            "half the measured sustained figure, clamped to half the documented "
            f"{TARGET_PER_MINUTE:.0f}/min. The operating figure stays on the "
            "conservative side of both: a measurement may license a faster pace "
            "than a vendor documents, and this repository does not take it."
        ),
        "total_requests_sent": int(findings["total_requests_sent"]) + completed,
    }
    findings["cells"] = [*findings["cells"], cell]
    write_report("task4b_alpaca_ceiling.json", findings)
    say("")
    say(f"CEILING STATE: {state}")
    say(f"  burst allowance      {burst_admitted} requests in {burst_elapsed:.2f} s")
    say(
        f"  sustained            {ceiling}/min over {elapsed:.2f} s, {codes.get(429, 0)} refusals"
    )
    say(
        f"  operating pace       {findings['operating_pace_per_minute']}/min "
        f"(spacing {findings['operating_spacing_s']} s)"
    )
    return 0


class _NoCharge:
    """The charge already happened in the scheduler; this avoids double-charging."""

    def __init__(self, ledger: RequestLedger) -> None:
        self._ledger = ledger

    def charge(self, vendor: str, day: str, endpoint: str) -> None:
        return None


if __name__ == "__main__":
    raise SystemExit(main())
