"""TASK 4 — probe Deribit's public API for access, depth, rate ceiling, revision.

**Blindness holds here.** This tool never reads a volatility value. From every
payload it extracts only metadata: HTTP status, byte count, row count, the
first and last **timestamps**, and the SHA-256 of the raw bytes. The DVOL rows
are ``[timestamp, open, high, low, close]`` and this tool touches **index 0
only**. The revision question is answered by comparing SHA-256 digests of two
fetches of the same historical window, which needs no value at all.

Reading a public endpoint that requires no account is permitted under standing
rule 5 and is distinct from trading. Nothing here registers, onboards, or
places an order.
"""

from __future__ import annotations

import hashlib
import json
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass, field
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, final

REPO_ROOT = Path(__file__).resolve().parent.parent
RAW_DIR = REPO_ROOT / "data" / "raw" / "task4"
OUT = REPO_ROOT / "reports" / "task4"
BASE = "https://www.deribit.com/api/v2/public/"
UA = "VRPExperiment/0.1 (research; contact [private email removed])"
TIMEOUT = 30.0

MS_PER_DAY = 86_400_000


def now_ms() -> int:
    return int(datetime.now(tz=UTC).timestamp() * 1000)


def iso(ms: int) -> str:
    return datetime.fromtimestamp(ms / 1000, tz=UTC).isoformat().replace("+00:00", "Z")


@final
@dataclass
class Probe:
    """One request. Records status and metadata, never a value."""

    endpoint: str
    params: dict[str, str]
    status: int | None = None
    error: str = ""
    byte_count: int = 0
    sha256: str = ""
    elapsed_ms: float = 0.0
    body_head: str = ""
    row_count: int | None = None
    first_ts: int | None = None
    last_ts: int | None = None
    extra: dict[str, Any] = field(default_factory=dict)

    def as_row(self) -> dict[str, Any]:
        row = {
            "endpoint": self.endpoint,
            "params": self.params,
            "status_code": self.status,
            "error": self.error,
            "byte_count": self.byte_count,
            "sha256": self.sha256,
            "elapsed_ms": round(self.elapsed_ms, 1),
            "row_count": self.row_count,
        }
        if self.first_ts is not None:
            row["first_ts"] = self.first_ts
            row["first_utc"] = iso(self.first_ts)
        if self.last_ts is not None:
            row["last_ts"] = self.last_ts
            row["last_utc"] = iso(self.last_ts)
        if self.body_head:
            row["refusal_payload_verbatim"] = self.body_head
        row.update(self.extra)
        return row


def fetch(endpoint: str, params: dict[str, str], *, seal: str | None = None) -> Probe:
    """One GET. Returns metadata only; raw bytes are sealed to disk if asked."""
    probe = Probe(endpoint=endpoint, params=params)
    url = BASE + endpoint + "?" + urllib.parse.urlencode(params)
    request = urllib.request.Request(url, headers={"User-Agent": UA})
    started = time.monotonic()
    raw = b""
    try:
        with urllib.request.urlopen(request, timeout=TIMEOUT) as response:
            probe.status = int(response.status)
            raw = response.read()
    except urllib.error.HTTPError as exc:
        probe.status = int(exc.code)
        raw = exc.read()
        # A refusal payload is recorded VERBATIM, truncated only for the report.
        probe.body_head = raw.decode("utf-8", errors="replace")[:1200]
    except (urllib.error.URLError, TimeoutError, OSError) as exc:
        probe.error = f"{type(exc).__name__}: {exc}"
    probe.elapsed_ms = (time.monotonic() - started) * 1000.0
    probe.byte_count = len(raw)
    if raw:
        probe.sha256 = hashlib.sha256(raw).hexdigest()
        if seal:
            target = RAW_DIR / seal
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(raw)
        _extract_metadata_only(probe, raw)
    return probe


def _extract_metadata_only(probe: Probe, raw: bytes) -> None:
    """Counts and timestamps only. **Index 0 of a DVOL row, and nothing else.**"""
    try:
        parsed = json.loads(raw)
    except json.JSONDecodeError:
        return
    if not isinstance(parsed, dict):
        return
    if "error" in parsed and not probe.body_head:
        probe.body_head = json.dumps(parsed["error"], sort_keys=True)[:1200]
    result = parsed.get("result")
    if isinstance(result, dict) and isinstance(result.get("data"), list):
        rows = result["data"]
        probe.row_count = len(rows)
        if rows and isinstance(rows[0], list) and rows[0]:
            probe.first_ts = int(rows[0][0])
            probe.last_ts = int(rows[-1][0])
        probe.extra["continuation"] = result.get("continuation")
        probe.extra["columns_served"] = (
            len(rows[0]) if rows and isinstance(rows[0], list) else None
        )
    elif isinstance(result, list):
        probe.row_count = len(result)


# ---------------------------------------------------------------------------


def probe_endpoints() -> list[dict[str, Any]]:
    """Status codes across the endpoints this measurement could use."""
    end = now_ms()
    start = end - 2 * MS_PER_DAY
    cases: list[tuple[str, dict[str, str], str | None]] = [
        ("get_time", {}, None),
        ("status", {}, None),
        ("get_index_price", {"index_name": "btc_usd"}, None),
        ("get_index_price", {"index_name": "eth_usd"}, None),
        (
            "get_volatility_index_data",
            {
                "currency": "BTC",
                "start_timestamp": str(start),
                "end_timestamp": str(end),
                "resolution": "3600",
            },
            "dvol_btc_2d.json",
        ),
        (
            "get_volatility_index_data",
            {
                "currency": "ETH",
                "start_timestamp": str(start),
                "end_timestamp": str(end),
                "resolution": "3600",
            },
            "dvol_eth_2d.json",
        ),
        ("get_instruments", {"currency": "BTC", "kind": "option"}, None),
        ("get_instruments", {"currency": "ETH", "kind": "option"}, None),
        ("get_currencies", {}, None),
        # A deliberately invalid call, to capture a refusal payload verbatim.
        ("get_volatility_index_data", {"currency": "DOGE"}, None),
        ("get_index_price", {"index_name": "not_a_real_index"}, None),
    ]
    out: list[dict[str, Any]] = []
    for endpoint, params, seal in cases:
        probe = fetch(endpoint, params, seal=seal)
        out.append(probe.as_row())
        sys.stdout.write(
            f"  {endpoint:30} {str(params)[:60]:60} -> "
            f"HTTP {probe.status} rows={probe.row_count} {probe.byte_count}B\n"
        )
        time.sleep(0.25)
    return out


def probe_rate_ceiling(max_burst: int = 60) -> dict[str, Any]:
    """Escalate burst size until the endpoint refuses. Measured, not read."""
    endpoint = "get_index_price"
    params = {"index_name": "btc_usd"}
    attempts: list[dict[str, Any]] = []
    first_refusal_at: int | None = None
    refusal_payload = ""
    refusal_status: int | None = None
    started = time.monotonic()
    for i in range(1, max_burst + 1):
        probe = fetch(endpoint, params)
        attempts.append(
            {
                "n": i,
                "status_code": probe.status,
                "elapsed_ms": round(probe.elapsed_ms, 1),
                "error": probe.error,
            }
        )
        if probe.status is not None and probe.status != 200:
            first_refusal_at = i
            refusal_status = probe.status
            refusal_payload = probe.body_head
            break
    wall = time.monotonic() - started
    completed = len(attempts)
    return {
        "endpoint": endpoint,
        "method": "sequential unthrottled burst, escalating until refusal",
        "max_burst_attempted": max_burst,
        "requests_completed": completed,
        "wall_seconds": round(wall, 2),
        "achieved_rate_per_second": round(completed / wall, 2) if wall > 0 else None,
        "first_refusal_at_request": first_refusal_at,
        "refusal_status": refusal_status,
        "refusal_payload_verbatim": refusal_payload,
        "attempts": attempts,
    }


def probe_history_depth(currency: str) -> dict[str, Any]:
    """Bisect the earliest served timestamp. Never assumed from documentation."""
    end = now_ms()
    resolution = "43200"  # 12h buckets keep row counts small during the search
    probes: list[dict[str, Any]] = []

    def served(days_back: int) -> tuple[bool, Probe]:
        start = end - days_back * MS_PER_DAY
        probe = fetch(
            "get_volatility_index_data",
            {
                "currency": currency,
                "start_timestamp": str(start),
                "end_timestamp": str(start + 7 * MS_PER_DAY),
                "resolution": resolution,
            },
        )
        probes.append({"days_back": days_back, **probe.as_row()})
        time.sleep(0.2)
        return bool(probe.row_count), probe

    # Exponential expansion to bracket, then bisection.
    lo, hi = 0, 1
    last_good = 0
    while hi <= 4096:
        ok, _ = served(hi)
        if ok:
            last_good = hi
            lo, hi = hi, hi * 2
        else:
            break
    bracket_hi = min(hi, 4096)
    low, high = lo, bracket_hi
    while high - low > 1:
        mid = (low + high) // 2
        ok, _ = served(mid)
        if ok:
            low = mid
            last_good = max(last_good, mid)
        else:
            high = mid
    earliest_ms = end - low * MS_PER_DAY
    return {
        "currency": currency,
        "method": "exponential bracket then bisection on a 7-day window",
        "resolution_seconds": int(resolution),
        "deepest_served_days_back": low,
        "first_empty_days_back": high,
        "approx_earliest_served_utc": iso(earliest_ms),
        "probe_count": len(probes),
        "probes": probes,
    }


def probe_revision(currency: str, days_back: int = 45) -> dict[str, Any]:
    """Does a published historical row ever change? Answered by digest, not value.

    MLCryptoEngine H11 died on a source that regenerated whole files and revised
    past rows. A revised implied-volatility series would silently rewrite this
    measurement, so the question is mandatory.
    """
    end = now_ms() - days_back * MS_PER_DAY
    start = end - 7 * MS_PER_DAY
    params = {
        "currency": currency,
        "start_timestamp": str(start),
        "end_timestamp": str(end),
        "resolution": "3600",
    }
    first = fetch(
        "get_volatility_index_data", params, seal=f"revision_{currency}_a.json"
    )
    time.sleep(5.0)
    second = fetch(
        "get_volatility_index_data", params, seal=f"revision_{currency}_b.json"
    )
    return {
        "currency": currency,
        "window_utc": [iso(start), iso(end)],
        "note": (
            "A fixed, closed historical window requested twice. Identical digests "
            "mean no row in the window changed between the two reads. No value is "
            "read to answer this."
        ),
        "fetch_a": first.as_row(),
        "fetch_b": second.as_row(),
        "digests_identical": bool(first.sha256) and first.sha256 == second.sha256,
        "row_counts_identical": first.row_count == second.row_count,
        "seconds_between_reads": 5.0,
    }


def main() -> int:
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    OUT.mkdir(parents=True, exist_ok=True)
    report: dict[str, Any] = {
        "kind": "task4_deribit_probe",
        "retrieved_at": iso(now_ms()),
        "base_url": BASE,
        "user_agent": UA,
        "blindness_note": (
            "This tool reads no volatility value. It extracts status codes, byte "
            "counts, row counts, index-0 timestamps and SHA-256 digests only."
        ),
    }
    sys.stdout.write("== endpoint status probe ==\n")
    report["endpoints"] = probe_endpoints()
    sys.stdout.write("== rate ceiling by escalation ==\n")
    report["rate_ceiling"] = probe_rate_ceiling()
    sys.stdout.write(
        f"  refusal at request {report['rate_ceiling']['first_refusal_at_request']}, "
        f"rate {report['rate_ceiling']['achieved_rate_per_second']}/s\n"
    )
    sys.stdout.write("== history depth by bisection ==\n")
    report["history_depth"] = [probe_history_depth(c) for c in ("BTC", "ETH")]
    for depth in report["history_depth"]:
        sys.stdout.write(
            f"  {depth['currency']}: deepest {depth['deepest_served_days_back']}d "
            f"(~{depth['approx_earliest_served_utc']}), "
            f"{depth['probe_count']} probes\n"
        )
    sys.stdout.write("== revision behaviour ==\n")
    report["revision"] = [probe_revision(c) for c in ("BTC", "ETH")]
    for rev in report["revision"]:
        sys.stdout.write(
            f"  {rev['currency']}: digests_identical={rev['digests_identical']}\n"
        )
    target = OUT / "deribit_probe.json"
    target.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", "utf-8")
    sys.stdout.write(f"wrote {target}\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
