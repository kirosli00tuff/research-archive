"""TASK 6 — the premium measurement. One sealed read, behind the latch.

Two modes, and only one of them touches real data.

``--fixture`` runs the entire pipeline against a synthetic source with a known
answer. It writes **no latch** and reads **no real data**. Its purpose is to
verify the plumbing — pagination, date alignment, the percent-to-decimal
conversion, the forward-window construction — on data whose answer is already
known, so that a defect in the plumbing cannot be mistaken for a finding.

``--real`` writes the latch **first**, recording the SHA-256 of every
participating module, and then reads the public endpoints **once**. A second
invocation refuses: the latch is spent and `LatchAlreadySpentError` is raised.

Nothing in `src/vrp/sealed_read.py` can tell which mode called it.
"""

from __future__ import annotations

import argparse
import json
import math
import random
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import UTC, date, datetime, timedelta
from pathlib import Path
from typing import Any

from vrp.absence import Absent
from vrp.latch import Latch
from vrp.sealed_read import (
    TENOR_DAYS,
    PremiumResult,
    RebalanceCount,
    bps_per_volatility_point,
    build_premium_series,
    count_rebalances,
    estimate_premium,
    non_overlapping,
    realized_volatility,
)

REPO_ROOT = Path(__file__).resolve().parent.parent
SRC = REPO_ROOT / "src" / "vrp"
OUT = REPO_ROOT / "reports" / "task6"
RAW = REPO_ROOT / "data" / "raw" / "task6"
LATCH_PATH = REPO_ROOT / "reports" / "task6" / "task6.latch.json"
BASE = "https://www.deribit.com/api/v2/public/"
UA = "VRPExperiment/0.1 (research; contact [private email removed])"
MS_PER_DAY = 86_400_000

OBSERVATION_HOUR_UTC = 8
"""The fixed UTC instant of Section 2.5, chosen at the first read and never
moved. **08:00 UTC is Deribit's option settlement instant**, so a 30-day tenor
measured 08:00 to 08:00 is exactly the interval an option spans.

It is also the only choice that aligns the two endpoints. Measured before the
latch: ``get_volatility_index_data`` at ``resolution=1D`` stamps its buckets at
**00:00 UTC**, while ``get_tradingview_chart_data`` at ``resolution=1D`` stamps
**08:00 UTC** -- an eight-hour misalignment that daily bars cannot fix. Both
series are therefore taken **hourly** and filtered to this instant.
"""

HOURLY_CHUNK_DAYS = 40
"""960 hourly rows per request, safely under the 1,000-row page cap measured in
TASK 4, so no call can silently truncate."""


def hourly_chunks(days_back: int) -> list[tuple[int, int]]:
    end = int(datetime.now(tz=UTC).timestamp() * 1000)
    start = end - days_back * MS_PER_DAY
    chunks: list[tuple[int, int]] = []
    cursor = start
    while cursor < end:
        stop = min(cursor + HOURLY_CHUNK_DAYS * MS_PER_DAY, end)
        chunks.append((cursor, stop))
        cursor = stop
    return chunks


def at_observation_hour(timestamp_ms: int) -> date | None:
    """The date, if this stamp is exactly the registered instant. Else None."""
    moment = datetime.fromtimestamp(timestamp_ms / 1000, tz=UTC)
    if moment.hour != OBSERVATION_HOUR_UTC or moment.minute != 0:
        return None
    return moment.date()


def iso_now() -> str:
    return datetime.now(tz=UTC).isoformat(timespec="seconds").replace("+00:00", "Z")


def call(endpoint: str, params: dict[str, str]) -> Any:
    url = BASE + endpoint + "?" + urllib.parse.urlencode(params)
    request = urllib.request.Request(url, headers={"User-Agent": UA})
    for attempt in range(3):
        try:
            with urllib.request.urlopen(request, timeout=45) as response:
                return json.loads(response.read())
        except (urllib.error.URLError, TimeoutError, OSError, json.JSONDecodeError):
            if attempt == 2:
                raise
            time.sleep(2.0 * (attempt + 1))
    return None


def fetch_dvol_daily(currency: str, days_back: int) -> dict[date, float]:
    """DVOL closes at the fixed 08:00 UTC instant. **A blind field, read once.**"""
    series: dict[date, float] = {}
    rows_seen = 0
    for start, stop in hourly_chunks(days_back):
        payload = call(
            "get_volatility_index_data",
            {
                "currency": currency,
                "start_timestamp": str(start),
                "end_timestamp": str(stop),
                "resolution": "3600",
            },
        )
        rows = payload["result"]["data"]
        rows_seen += len(rows)
        if len(rows) >= 1000:
            raise RuntimeError(
                f"DVOL chunk returned {len(rows)} rows and may be truncated at "
                "the page cap; the chunk must be narrowed rather than the "
                "truncation accepted"
            )
        for row in rows:
            day = at_observation_hour(int(row[0]))
            if day is not None:
                series[day] = float(row[4])  # close
        time.sleep(0.25)
    sys.stdout.write(
        f"  {currency} DVOL: {rows_seen} hourly rows -> {len(series)} daily "
        f"observations at {OBSERVATION_HOUR_UTC:02d}:00 UTC\n"
    )
    return series


def fetch_underlying_daily(currency: str, days_back: int) -> dict[date, float]:
    """Perpetual closes at the same 08:00 UTC instant, from the same venue."""
    series: dict[date, float] = {}
    rows_seen = 0
    for start, stop in hourly_chunks(days_back):
        payload = call(
            "get_tradingview_chart_data",
            {
                "instrument_name": f"{currency}-PERPETUAL",
                "start_timestamp": str(start),
                "end_timestamp": str(stop),
                "resolution": "3600",
            },
        )
        result = payload["result"]
        if result.get("status") == "no_data":
            time.sleep(0.25)
            continue
        ticks = result["ticks"]
        closes = result["close"]
        rows_seen += len(ticks)
        if len(ticks) >= 1000:
            raise RuntimeError(
                f"perpetual chunk returned {len(ticks)} rows and may be "
                "truncated at the page cap"
            )
        for tick, close in zip(ticks, closes, strict=True):
            day = at_observation_hour(int(tick))
            if day is not None:
                series[day] = float(close)
        time.sleep(0.25)
    sys.stdout.write(
        f"  {currency} perp: {rows_seen} hourly rows -> {len(series)} daily "
        f"observations at {OBSERVATION_HOUR_UTC:02d}:00 UTC\n"
    )
    return series


def synthetic_source(
    currency: str, days_back: int
) -> tuple[dict[date, float], dict[date, float], float]:
    """A fixture source with a known planted premium, in the real shape."""
    seed = 20260830 + sum(ord(c) for c in currency)
    rng = random.Random(seed)
    planted = 0.08  # eight volatility points, in decimal
    base_vol = 0.55
    today = datetime.now(tz=UTC).date()
    days = [today - timedelta(days=days_back - i) for i in range(days_back)]
    spot = 50_000.0
    closes: dict[date, float] = {}
    for day in days:
        closes[day] = spot
        spot *= math.exp(rng.gauss(0.0, (base_vol - planted) / math.sqrt(365.0)))
    implied = dict.fromkeys(days, base_vol * 100.0)
    return implied, closes, planted


def build(implied_pct: dict[date, float], closes: dict[date, float]) -> dict[str, Any]:
    """Pair the legs exactly as Section 2 registers, forward-looking."""
    days = sorted(set(implied_pct) & set(closes))
    implied: list[float] = []
    realized: list[float] = []
    kept: list[str] = []
    dropped_missing_window = 0
    for day in days:
        window_days = [day + timedelta(days=k) for k in range(TENOR_DAYS + 1)]
        window = [closes.get(d) for d in window_days]
        if any(c is None for c in window):
            dropped_missing_window += 1
            continue
        measured = realized_volatility([c for c in window if c is not None])
        if isinstance(measured, Absent):
            dropped_missing_window += 1
            continue
        implied.append(implied_pct[day] / 100.0)  # DVOL is in percentage points
        realized.append(measured)
        kept.append(day.isoformat())
    return {
        "implied": implied,
        "realized": realized,
        "dates": kept,
        "days_paired": len(days),
        "dropped_incomplete_forward_window": dropped_missing_window,
    }


def rebalance_distribution(
    implied_pct: dict[date, float], closes: dict[date, float], band: float
) -> dict[str, Any]:
    """Section 4.3's count, over every date with a complete forward window."""
    counts: list[int] = []
    drifts: list[float] = []
    for day in sorted(set(implied_pct) & set(closes)):
        window_days = [day + timedelta(days=k) for k in range(TENOR_DAYS + 1)]
        window = [closes.get(d) for d in window_days]
        if any(c is None for c in window):
            continue
        path = [c for c in window if c is not None]
        counted = count_rebalances(
            path, strike=path[0], sigma=implied_pct[day] / 100.0, band=band
        )
        if isinstance(counted, RebalanceCount):
            counts.append(counted.rebalances)
            drifts.append(counted.max_abs_drift)
    if not counts:
        return {"band": band, "n": 0}
    ordered = sorted(counts)
    return {
        "band": band,
        "n": len(ordered),
        "min": ordered[0],
        "median": ordered[len(ordered) // 2],
        "mean": round(sum(ordered) / len(ordered), 4),
        "p90": ordered[min(len(ordered) - 1, round(0.90 * (len(ordered) - 1)))],
        "max": ordered[-1],
        "max_abs_drift_median": round(sorted(drifts)[len(drifts) // 2], 4),
    }


def stability(
    premium: list[float], dates: list[str], parts: int = 4
) -> list[dict[str, Any]]:
    """Section 6's stability requirement: the same estimator on each quarter."""
    size = len(premium) // parts
    out: list[dict[str, Any]] = []
    for i in range(parts):
        lo = i * size
        hi = (i + 1) * size if i < parts - 1 else len(premium)
        chunk = premium[lo:hi]
        result = estimate_premium(chunk, label=f"quarter_{i + 1}")
        row: dict[str, Any] = {
            "part": i + 1,
            "from": dates[lo],
            "to": dates[hi - 1],
            "n": len(chunk),
        }
        if isinstance(result, PremiumResult):
            row.update(
                {
                    "mean_vol_points": round(result.mean_vol_points, 6),
                    "mean_bps": round(result.mean_bps, 3),
                    "t": round(result.t_statistic, 3),
                    "one_sided_p": result.one_sided_p,
                    "positive_share": round(result.positive_share, 4),
                }
            )
        else:
            row["absent"] = f"{result.reason}: {result.detail}"
        out.append(row)
    return out


def run(mode: str, days_back: int) -> dict[str, Any]:
    OUT.mkdir(parents=True, exist_ok=True)
    RAW.mkdir(parents=True, exist_ok=True)
    report: dict[str, Any] = {
        "kind": f"task6_{mode}",
        "mode": mode,
        "started_at": iso_now(),
        "tenor_days": TENOR_DAYS,
        "bps_per_volatility_point": round(bps_per_volatility_point() / 100.0, 6),
        "days_requested": days_back,
        "assets": {},
    }
    if mode == "real":
        latch = Latch(LATCH_PATH)
        modules = [*sorted(SRC.glob("*.py")), Path(__file__)]
        record = latch.write(modules, "TASK 6 single sealed read of Deribit DVOL")
        report["latch"] = record.as_row()
        sys.stdout.write(f"LATCH WRITTEN: {LATCH_PATH}\n")

    for currency in ("BTC", "ETH"):
        if mode == "fixture":
            implied_pct, closes, planted = synthetic_source(currency, days_back)
            asset: dict[str, Any] = {"planted_premium_vol_points": planted}
        else:
            implied_pct = fetch_dvol_daily(currency, days_back)
            closes = fetch_underlying_daily(currency, days_back)
            asset = {}
            (RAW / f"dvol_{currency}_daily.json").write_text(
                json.dumps({d.isoformat(): v for d, v in sorted(implied_pct.items())}),
                encoding="utf-8",
            )
            (RAW / f"underlying_{currency}_daily.json").write_text(
                json.dumps({d.isoformat(): v for d, v in sorted(closes.items())}),
                encoding="utf-8",
            )
        asset["implied_days_served"] = len(implied_pct)
        asset["underlying_days_served"] = len(closes)
        if implied_pct:
            asset["implied_span"] = [
                min(implied_pct).isoformat(),
                max(implied_pct).isoformat(),
            ]
        if closes:
            asset["underlying_span"] = [
                min(closes).isoformat(),
                max(closes).isoformat(),
            ]

        built = build(implied_pct, closes)
        series = build_premium_series(built["implied"], built["realized"])
        asset["days_paired"] = built["days_paired"]
        asset["dropped_incomplete_forward_window"] = built[
            "dropped_incomplete_forward_window"
        ]
        if isinstance(series, Absent):
            asset["absent"] = f"{series.reason}: {series.detail}"
            report["assets"][currency] = asset
            continue
        asset["n"] = series.n
        asset["window"] = [built["dates"][0], built["dates"][-1]]

        primary = estimate_premium(series.premium, label=f"{currency}_overlapping_hac")
        asset["primary_overlapping_hac"] = (
            primary.as_row()
            if isinstance(primary, PremiumResult)
            else f"{primary.reason}: {primary.detail}"
        )
        thinned = non_overlapping(series.premium)
        secondary = estimate_premium(
            thinned, label=f"{currency}_non_overlapping", bandwidth=0
        )
        asset["robustness_non_overlapping_iid"] = (
            secondary.as_row()
            if isinstance(secondary, PremiumResult)
            else f"{secondary.reason}: {secondary.detail}"
        )
        asset["stability_quarters"] = stability(series.premium, built["dates"])
        asset["rebalances"] = [
            rebalance_distribution(implied_pct, closes, band)
            for band in (0.05, 0.10, 0.20)
        ]
        report["assets"][currency] = asset
        if isinstance(primary, PremiumResult):
            sys.stdout.write(
                f"{currency}: n={primary.n} mean={primary.mean_vol_points:.6f} "
                f"vol pts ({primary.mean_bps:.2f} bps) t={primary.t_statistic:.3f} "
                f"p={primary.one_sided_p:.3e} CI_lower={primary.ci_lower_bps:.2f} bps\n"
            )
    report["finished_at"] = iso_now()
    target = OUT / f"{mode}_result.json"
    target.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", "utf-8")
    sys.stdout.write(f"wrote {target}\n")
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mode", choices=("fixture", "real"), required=True)
    parser.add_argument("--days-back", type=int, default=1992)
    args = parser.parse_args()
    run(args.mode, args.days_back)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
