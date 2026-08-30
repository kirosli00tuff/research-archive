"""TASK 5 — quoted bid-ask, sampled across distinct observation windows.

**Blindness discipline.** This tool reads an option's bid and ask because a
spread is a *cost* and Section 2 of the registration deliberately places `bid`,
`ask`, `half_spread` and `spread_bps` in `READABLE_FIELDS`. It **never emits or
stores a mid-price, a mark price, or any premium level** — those are blind until
TASK 6. Every figure it writes is a *difference*, or a ratio of a difference to
a readable notional.

**Deribit is measured here as a labelled REFERENCE, not as a cost input.**
Deribit prohibits Canadian residents (TASK 3), so its spread is not the cost of
a reachable venue and is never substituted for one. Substituting a band measured
on one instrument for the cost of another is the exact defect ORBExperiment
found in its own carried QQQ band, where five of six legs were understated and
the resulting shift was 11.27x too small.
"""

from __future__ import annotations

import json
import statistics
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent.parent
OUT = REPO_ROOT / "reports" / "task5"
BASE = "https://www.deribit.com/api/v2/public/"
UA = "VRPExperiment/0.1 (research; contact [private email removed])"
TENOR_DAYS = 30
WINDOWS = 24
"""Registered at 24, above the >= 20 the task requires, so a dropped window
still leaves the requirement met."""
SPACING_SECONDS = 20.0


def iso_now() -> str:
    return datetime.now(tz=UTC).isoformat(timespec="seconds").replace("+00:00", "Z")


def get(endpoint: str, params: dict[str, str]) -> Any:
    url = BASE + endpoint + "?" + urllib.parse.urlencode(params)
    request = urllib.request.Request(url, headers={"User-Agent": UA})
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            parsed = json.loads(response.read())
    except (urllib.error.URLError, TimeoutError, OSError, json.JSONDecodeError):
        return None
    return parsed.get("result") if isinstance(parsed, dict) else None


def pick_atm_series(currency: str) -> dict[str, Any] | None:
    """Find the expiry nearest the registered tenor and the ATM strike."""
    index = get("get_index_price", {"index_name": f"{currency.lower()}_usd"})
    raw_instruments = get("get_instruments", {"currency": currency, "kind": "option"})
    instruments: list[dict[str, Any]] = (
        raw_instruments if isinstance(raw_instruments, list) else []
    )
    if not isinstance(index, dict) or not instruments:
        return None
    spot = float(index["index_price"])  # an index level, not an option price
    now_ms = int(datetime.now(tz=UTC).timestamp() * 1000)
    target_ms = now_ms + TENOR_DAYS * 86_400_000

    expiries = sorted({int(i["expiration_timestamp"]) for i in instruments})
    expiry = min(expiries, key=lambda e: abs(e - target_ms))
    at_expiry = [i for i in instruments if int(i["expiration_timestamp"]) == expiry]
    strikes = sorted({float(i["strike"]) for i in at_expiry})
    strike = min(strikes, key=lambda s: abs(s - spot))
    names = {
        i["option_type"]: i["instrument_name"]
        for i in at_expiry
        if float(i["strike"]) == strike
    }
    days = (expiry - now_ms) / 86_400_000
    return {
        "currency": currency,
        "spot_index": round(spot, 2),
        "expiry_ms": expiry,
        "expiry_utc": datetime.fromtimestamp(expiry / 1000, tz=UTC).isoformat(),
        "settlement_rule": "Deribit options settle at 08:00 UTC on the expiry date",
        "days_to_expiry": round(days, 3),
        "strike": strike,
        "instruments": names,
        "strikes_at_expiry": len(strikes),
        "expiries_listed": len(expiries),
    }


def sample_spread(instrument: str) -> dict[str, Any] | None:
    """One observation. Returns a DIFFERENCE only — never a level."""
    book = get("get_order_book", {"instrument_name": instrument, "depth": "1"})
    if not isinstance(book, dict):
        return None
    bid = book.get("best_bid_price")
    ask = book.get("best_ask_price")
    if not isinstance(bid, int | float) or not isinstance(ask, int | float):
        return None
    if bid <= 0 or ask <= 0 or ask < bid:
        return {"instrument": instrument, "quoted": False, "at": iso_now()}
    spread = float(ask) - float(bid)
    # Deribit option contracts are 1 coin of underlying and are quoted in coin
    # units, so a spread in coin units IS a fraction of notional.
    return {
        "instrument": instrument,
        "quoted": True,
        "at": iso_now(),
        "spread_coin": round(spread, 8),
        "half_spread_coin": round(spread / 2.0, 8),
        "half_spread_bps_of_notional": round(spread / 2.0 * 10_000, 4),
        "round_trip_bps_of_notional": round(spread * 10_000, 4),
        "bid_size": book.get("best_bid_amount"),
        "ask_size": book.get("best_ask_amount"),
    }


def distribution(values: list[float]) -> dict[str, Any]:
    if not values:
        return {"n": 0}
    ordered = sorted(values)
    return {
        "n": len(ordered),
        "min": round(ordered[0], 4),
        "median": round(statistics.median(ordered), 4),
        "mean": round(statistics.fmean(ordered), 4),
        "p90": round(
            ordered[min(len(ordered) - 1, round(0.90 * (len(ordered) - 1)))], 4
        ),
        "max": round(ordered[-1], 4),
        "full_distribution_sorted": [round(v, 4) for v in ordered],
    }


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    report: dict[str, Any] = {
        "kind": "task5_reference_spreads",
        "started_at": iso_now(),
        "venue": "Deribit",
        "venue_classification": "PROHIBITED for Canadian residents (TASK 3)",
        "status": (
            "REFERENCE ONLY. This is NOT the cost input for any verdict. Deribit "
            "prohibits Canadian residents, so its spread is not the cost of a "
            "lawfully reachable venue and is never substituted for one."
        ),
        "tenor_days_target": TENOR_DAYS,
        "windows_registered": WINDOWS,
        "spacing_seconds": SPACING_SECONDS,
    }
    series: dict[str, Any] = {}
    for currency in ("BTC", "ETH"):
        picked = pick_atm_series(currency)
        if picked is None:
            series[currency] = {"error": "series could not be selected"}
            continue
        series[currency] = picked
        sys.stdout.write(
            f"{currency}: expiry {picked['expiry_utc']} "
            f"({picked['days_to_expiry']}d), strike {picked['strike']}, "
            f"{picked['instruments']}\n"
        )
    report["series"] = series

    observations: dict[str, list[dict[str, Any]]] = {}
    for window in range(1, WINDOWS + 1):
        for currency, picked in series.items():
            if "instruments" not in picked:
                continue
            for option_type, name in picked["instruments"].items():
                key = f"{currency}-{option_type}"
                sample = sample_spread(name)
                if sample is not None:
                    observations.setdefault(key, []).append(
                        {"window": window, **sample}
                    )
        sys.stdout.write(f"  window {window}/{WINDOWS}\n")
        if window < WINDOWS:
            time.sleep(SPACING_SECONDS)

    summary: dict[str, Any] = {}
    for key, rows in observations.items():
        quoted = [r for r in rows if r.get("quoted")]
        half = [float(r["half_spread_bps_of_notional"]) for r in quoted]
        summary[key] = {
            "windows_attempted": len(rows),
            "windows_quoted": len(quoted),
            "windows_unquoted": len(rows) - len(quoted),
            "half_spread_bps_of_notional": distribution(half),
            "round_trip_bps_of_notional": distribution([h * 2 for h in half]),
        }
        dist = summary[key]["half_spread_bps_of_notional"]
        sys.stdout.write(
            f"{key}: n={dist['n']} median={dist.get('median')} "
            f"p90={dist.get('p90')} bps half-spread\n"
        )
    report["observations"] = observations
    report["summary"] = summary
    report["finished_at"] = iso_now()
    target = OUT / "reference_spreads_deribit.json"
    target.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", "utf-8")
    sys.stdout.write(f"wrote {target}\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
