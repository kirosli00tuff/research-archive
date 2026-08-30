"""TASK 4, corrected probes — rate ceiling by concurrent escalation, and revision.

Two corrections to `tools/probe_deribit.py`, both recorded rather than silently
applied.

**Correction 1 — the revision digest was a false positive.** Hashing the whole
JSON-RPC response answers the wrong question: Deribit's envelope carries
``usIn``, ``usOut`` and ``usDiff`` server-timing fields that change on every
call, so two identical historical windows produce different whole-response
digests while their **data rows are byte-identical**. The corrected probe hashes
the canonicalised ``result.data`` array only.

**Correction 2 — a sequential burst never found the ceiling.** Sixty sequential
requests achieved only 3.64 req/s and drew no refusal, which measures the
round-trip latency, not the limit. The corrected probe escalates **concurrency**
until the endpoint refuses or a registered ceiling is reached.

Blindness holds: this tool reads no volatility value. It hashes the data array
without inspecting any element, and reads index 0 (timestamp) only for reporting
the window.
"""

from __future__ import annotations

import hashlib
import json
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent.parent
OUT = REPO_ROOT / "reports" / "task4"
RAW = REPO_ROOT / "data" / "raw" / "task4"
BASE = "https://www.deribit.com/api/v2/public/"
UA = "VRPExperiment/0.1 (research; contact [private email removed])"
MS_PER_DAY = 86_400_000

MAX_CONCURRENCY = 64
"""Registered ceiling on the escalation. The probe stops here even if no refusal
has been drawn, and reports 'no refusal at or below this rate' rather than
climbing indefinitely against a venue that has not refused."""


def now_ms() -> int:
    return int(datetime.now(tz=UTC).timestamp() * 1000)


def iso(ms: int) -> str:
    return datetime.fromtimestamp(ms / 1000, tz=UTC).isoformat().replace("+00:00", "Z")


def raw_get(endpoint: str, params: dict[str, str]) -> tuple[int | None, bytes, str]:
    url = BASE + endpoint + "?" + urllib.parse.urlencode(params)
    request = urllib.request.Request(url, headers={"User-Agent": UA})
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            return int(response.status), response.read(), ""
    except urllib.error.HTTPError as exc:
        return int(exc.code), exc.read(), ""
    except (urllib.error.URLError, TimeoutError, OSError) as exc:
        return None, b"", f"{type(exc).__name__}: {exc}"


def data_digest(raw: bytes) -> tuple[str, int | None, list[str]]:
    """SHA-256 of the canonicalised data array. No element is inspected."""
    try:
        parsed = json.loads(raw)
    except json.JSONDecodeError:
        return "", None, []
    result = parsed.get("result") if isinstance(parsed, dict) else None
    if not isinstance(result, dict) or not isinstance(result.get("data"), list):
        return "", None, []
    rows = result["data"]
    canonical = json.dumps(rows, sort_keys=True, separators=(",", ":")).encode("utf-8")
    window: list[str] = []
    if rows and isinstance(rows[0], list) and rows[0]:
        window = [iso(int(rows[0][0])), iso(int(rows[-1][0]))]
    return hashlib.sha256(canonical).hexdigest(), len(rows), window


def escalate_rate(endpoint: str, params: dict[str, str]) -> dict[str, Any]:
    """Escalate concurrency until refusal or the registered ceiling."""
    steps: list[dict[str, Any]] = []
    refusal: dict[str, Any] | None = None
    concurrency = 2
    while concurrency <= MAX_CONCURRENCY:
        started = time.monotonic()
        with ThreadPoolExecutor(max_workers=concurrency) as pool:
            results = list(
                pool.map(lambda _: raw_get(endpoint, params), range(concurrency))
            )
        wall = time.monotonic() - started
        codes = [status for status, _, _ in results]
        non_200 = [(i, c) for i, c in enumerate(codes) if c != 200]
        step = {
            "concurrency": concurrency,
            "requests": concurrency,
            "wall_seconds": round(wall, 3),
            "achieved_rate_per_second": round(concurrency / wall, 2) if wall else None,
            "status_counts": {
                str(c): codes.count(c) for c in sorted(set(codes), key=str)
            },
            "non_200_count": len(non_200),
        }
        steps.append(step)
        rate = step["achieved_rate_per_second"]
        sys.stdout.write(
            f"  concurrency {concurrency:3d} -> {rate:>7} req/s "
            f"statuses {step['status_counts']}\n"
        )
        if non_200:
            index = non_200[0][0]
            _, body, err = results[index]
            refusal = {
                "at_concurrency": concurrency,
                "achieved_rate_per_second": step["achieved_rate_per_second"],
                "status_code": codes[index],
                "transport_error": err,
                "payload_verbatim": body.decode("utf-8", errors="replace")[:1500],
            }
            break
        concurrency *= 2
        time.sleep(1.0)
    return {
        "endpoint": endpoint,
        "params": params,
        "method": (
            "concurrent burst, doubling concurrency from 2 until a non-200 "
            f"status is drawn or the registered ceiling of {MAX_CONCURRENCY} "
            "concurrent requests is reached"
        ),
        "registered_max_concurrency": MAX_CONCURRENCY,
        "steps": steps,
        "refusal": refusal,
        "peak_rate_without_refusal": max(
            (s["achieved_rate_per_second"] or 0)
            for s in steps
            if s["non_200_count"] == 0
        )
        if any(s["non_200_count"] == 0 for s in steps)
        else None,
    }


def revision_snapshot(currency: str, days_back: int) -> dict[str, Any]:
    """One data-only digest of a fixed, closed historical window."""
    end = now_ms() - days_back * MS_PER_DAY
    start = end - 7 * MS_PER_DAY
    # Snap to whole hours so the window is byte-reproducible across runs.
    start = (start // 3_600_000) * 3_600_000
    end = (end // 3_600_000) * 3_600_000
    params = {
        "currency": currency,
        "start_timestamp": str(start),
        "end_timestamp": str(end),
        "resolution": "3600",
    }
    status, raw, err = raw_get("get_volatility_index_data", params)
    digest, rows, window = data_digest(raw)
    RAW.mkdir(parents=True, exist_ok=True)
    (RAW / f"revision_snapshot_{currency}_{days_back}d.json").write_bytes(raw)
    return {
        "currency": currency,
        "days_back": days_back,
        "params": params,
        "requested_window_utc": [iso(start), iso(end)],
        "served_window_utc": window,
        "status_code": status,
        "transport_error": err,
        "row_count": rows,
        "data_only_sha256": digest,
        "whole_response_sha256": hashlib.sha256(raw).hexdigest() if raw else "",
        "taken_at": iso(now_ms()),
    }


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    report: dict[str, Any] = {
        "kind": "task4_rate_and_revision",
        "retrieved_at": iso(now_ms()),
        "corrections": [
            "revision digest now covers result.data only; the whole-response "
            "digest is contaminated by the usIn/usOut/usDiff server-timing fields",
            "rate ceiling now escalates concurrency; a sequential burst measured "
            "round-trip latency at 3.64 req/s and drew no refusal",
        ],
    }
    sys.stdout.write("== rate ceiling, concurrent escalation: get_index_price ==\n")
    report["rate_light"] = escalate_rate("get_index_price", {"index_name": "btc_usd"})
    time.sleep(3.0)
    end = now_ms()
    sys.stdout.write(
        "== rate ceiling, concurrent escalation: get_volatility_index_data ==\n"
    )
    report["rate_heavy"] = escalate_rate(
        "get_volatility_index_data",
        {
            "currency": "BTC",
            "start_timestamp": str(end - 2 * MS_PER_DAY),
            "end_timestamp": str(end),
            "resolution": "3600",
        },
    )
    sys.stdout.write("== revision baseline snapshots (data-only digests) ==\n")
    snapshots = [
        revision_snapshot(c, d) for c in ("BTC", "ETH") for d in (45, 365, 900)
    ]
    for snap in snapshots:
        cur, back = snap["currency"], snap["days_back"]
        sys.stdout.write(
            f"  {cur} {back:>4}d back: rows={snap['row_count']} "
            f"data_sha={snap['data_only_sha256'][:16]}\n"
        )
    report["revision_baseline"] = snapshots
    target = OUT / "rate_and_revision_baseline.json"
    target.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", "utf-8")
    sys.stdout.write(f"wrote {target}\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
