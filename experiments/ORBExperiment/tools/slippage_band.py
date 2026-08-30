"""A.3 TASK 2 — Change A. The slippage band, measured on the traded instruments.

**The carried band came from an ETF.** 0.020 central and 0.040 pessimistic on
entry, 0.040 and 0.080 on stop exits, 0.010 and 0.020 on close exits — all from
the QQQ replication (carried, C-6), an instrument whose spread sits near one
cent. **This universe selects news-driven single names, and the carried figures
were never measured on them.**

**The assignment is fixed here, before the shift is computed, and it does not
depend on which produces a favourable number.**

- **Median → the CENTRAL end.** The central band is the modal execution a
  registered trade actually gets, and the median of a per-trade slippage
  distribution is the figure half of trades beat. A mean would be dragged by the
  gap-through tail, which is the pessimistic case, not the central one.
- **90th percentile → the PESSIMISTIC end.** Section 6 calls the pessimistic end
  a plausible bad execution rather than a worst case. The 90th percentile is a
  bad-but-reachable decile; a maximum would be a single session's news gap.

**What one-minute data can and cannot support**, stated before the run because
it bounds the result. When the trigger bar **opens through** the boundary, the
first trade of that bar **is** the first trade through it and the overshoot is
**exactly measurable**. When the bar opens inside and crosses within the minute,
**one-minute data cannot locate the first trade through the boundary**, and the
writer records **0.0** for that trade. **The overshoot distributions are
therefore LOWER BOUNDS, the resulting band is a lower bound, and any power
computed on it is an UPPER bound on power.** The two cases are counted
separately.

**The quoted spread is measured, not assumed.** The tier serves historical NBBO
quotes — probed and confirmed before this tool was written — so the
time-weighted quoted **half** spread across each entry and stop minute is
measured and added to the overshoot. A minute whose quotes are unusable is a
**refused minute**, counted as such, **never a zero spread**.
"""

from __future__ import annotations

import json
import sys
from datetime import date
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))

from _a1r import DATA, REPORTS, send, wire

from orb.calendar import sessions
from orb.dispersion import measure_carve_out_slippage_band
from orb.ledger import AppendOnlyLedger
from orb.redact import say
from orb.vendors import alpaca_quotes, consolidated_feed

MANIFEST = REPORTS / "task5b_post_holdout_pull.json"
SEALED_ROOT = DATA / "sealed_credentialed"
OUT = Path(__file__).resolve().parent.parent / "reports" / "stage_a3rescue"
STOP_EXIT_SHARE = 0.3818181818181818
"""Measured at A.1 TASK 3 of the inference-repair pass, `n = 550` resolved exits."""

CARRIED = {
    "entry_central": 0.020,
    "entry_pessimistic": 0.040,
    "stop_central": 0.040,
    "stop_pessimistic": 0.080,
    "close_central": 0.010,
    "close_pessimistic": 0.020,
}
QUOTE_LIMIT = 10000


def main() -> int:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    tickers: list[str] = list(manifest["tickers"])
    files: dict[str, list[str]] = {}
    for entry in manifest["manifest"]:
        files.setdefault(str(entry["ticker"]), []).append(str(entry["stored_file"]))
    slice_sessions = list(
        sessions(
            date.fromisoformat(manifest["first_session"]),
            date.fromisoformat(manifest["last_closed_session"]),
        )
    )

    store, client, seal = wire()
    sent = {"n": 0}
    cache: dict[tuple[str, int], bytes | None] = {}

    def load_payloads(ticker: str) -> list[bytes]:
        return [(SEALED_ROOT / name).read_bytes() for name in files.get(ticker, [])]

    def load_quotes(ticker: str, start_ms: int, end_ms: int) -> bytes | None:
        """Fetch one minute of NBBO quotes. **Readable fields only cross here.**"""
        key = (ticker, start_ms)
        if key in cache:
            return cache[key]
        from datetime import UTC, datetime

        def iso(ms: int) -> str:
            return (
                datetime.fromtimestamp(ms / 1000, tz=UTC)
                .isoformat(timespec="milliseconds")
                .replace("+00:00", "Z")
            )

        response = send(
            client,
            alpaca_quotes(
                store,
                ticker,
                iso(start_ms),
                iso(end_ms),
                feed=consolidated_feed(),
                limit=QUOTE_LIMIT,
            ),
        )
        sent["n"] += 1
        seal.store(f"task2q_{ticker}_{start_ms}.raw", response.body)
        body = response.body if 200 <= response.status_code < 300 else None
        cache[key] = body
        if sent["n"] % 100 == 0:
            say(f"  quote minutes fetched: {sent['n']}")
        return body

    say(
        f"measuring the slippage band over n = {len(slice_sessions)} post-holdout "
        f"sessions, {len(tickers)} tickers, stop share {STOP_EXIT_SHARE:.6f}"
    )
    band = measure_carve_out_slippage_band(
        tickers,
        load_payloads,
        load_quotes,
        slice_sessions,
        STOP_EXIT_SHARE,
        allow_short=True,
    )

    measured = {
        "entry_central": band.measured_entry_central,
        "entry_pessimistic": band.measured_entry_pessimistic,
        "stop_central": band.measured_stop_central,
        "stop_pessimistic": band.measured_stop_pessimistic,
        "close_central": band.measured_close_central,
        "close_pessimistic": band.measured_close_pessimistic,
    }
    against_carried = {
        name: {
            "carried": CARRIED[name],
            "measured": value,
            "verdict": (
                "MEASURED IS LOWER — the carried figure overstated this leg"
                if value < CARRIED[name]
                else "MEASURED IS HIGHER — the carried figure UNDERSTATED this leg"
                if value > CARRIED[name]
                else "agrees"
            ),
            "ratio_measured_over_carried": (
                value / CARRIED[name] if CARRIED[name] else None
            ),
        }
        for name, value in measured.items()
    }

    findings: dict[str, Any] = {
        "kind": "measured_slippage_band",
        "measured_at": date.today().isoformat(),
        "assignment_fixed_before_computation": {
            "central_end": "median of the per-trade slippage distribution",
            "pessimistic_end": "90th percentile of the same distribution",
            "why": (
                "the central band is the modal execution a registered trade "
                "gets, and a mean would be dragged by the gap-through tail, "
                "which is the pessimistic case; the 90th percentile is a "
                "bad-but-reachable decile where a maximum would be one news gap"
            ),
        },
        "one_minute_resolution_caveat": (
            "An intrabar cross cannot be located at 1-minute resolution and is "
            "recorded as 0.0 overshoot. The overshoot distributions are LOWER "
            "BOUNDS, the band is a lower bound, and any power computed on it is "
            "an UPPER bound on power."
        ),
        "quote_requests_sent": sent["n"],
        "carve_out_half": "post_holdout",
        "first_session": manifest["first_session"],
        "last_closed_session": manifest["last_closed_session"],
        "stop_exit_share_used": STOP_EXIT_SHARE,
        "measured_band": measured,
        "measured_against_carried": against_carried,
        "measured_shift_usd_per_share": band.measured_shift_usd_per_share,
        "carried_shift_usd_per_share": (
            (CARRIED["entry_pessimistic"] - CARRIED["entry_central"])
            + STOP_EXIT_SHARE * (CARRIED["stop_pessimistic"] - CARRIED["stop_central"])
            + (1 - STOP_EXIT_SHARE)
            * (CARRIED["close_pessimistic"] - CARRIED["close_central"])
        ),
        "per_leg_statistics": {
            "entry_overshoot": {
                "mean": band.entry_overshoot_mean,
                "median": band.entry_overshoot_median,
                "p90": band.entry_overshoot_p90,
                "n": band.entry_observations,
                "gapped_through": band.entry_gapped_through,
                "crossed_intrabar": band.entry_crossed_intrabar,
            },
            "entry_half_spread": {
                "mean": band.entry_half_spread_mean,
                "median": band.entry_half_spread_median,
                "p90": band.entry_half_spread_p90,
                "minutes_served": band.entry_quote_minutes_served,
                "minutes_refused": band.entry_quote_minutes_refused,
            },
            "entry_slippage_total": {
                "mean": band.entry_slippage_mean,
                "median": band.entry_slippage_median,
                "p90": band.entry_slippage_p90,
                "n": band.entry_observations,
            },
            "stop_overshoot": {
                "mean": band.stop_overshoot_mean,
                "median": band.stop_overshoot_median,
                "p90": band.stop_overshoot_p90,
                "n": band.stop_observations,
                "gapped_through": band.stop_gapped_through,
                "crossed_intrabar": band.stop_crossed_intrabar,
            },
            "stop_half_spread": {
                "mean": band.stop_half_spread_mean,
                "median": band.stop_half_spread_median,
                "p90": band.stop_half_spread_p90,
                "minutes_served": band.stop_quote_minutes_served,
                "minutes_refused": band.stop_quote_minutes_refused,
            },
            "stop_slippage_total": {
                "mean": band.stop_slippage_mean,
                "median": band.stop_slippage_median,
                "p90": band.stop_slippage_p90,
                "n": band.stop_observations,
            },
            "close_slippage": {
                "mean": band.close_slippage_mean,
                "median": band.close_slippage_median,
                "p90": band.close_slippage_p90,
                "n": band.close_observations,
                "without_an_official_print": band.close_without_an_official_print,
            },
        },
        "sessions_used": band.sessions_used,
        "name_sessions_evaluated": band.name_sessions_evaluated,
        "bars_read": band.bars_read,
        "tickers_with_bars": band.tickers_with_bars,
        "cost_model_note": (
            "The frozen Section 6 model is not consulted here; this tool "
            "measures the slippage band, which is an input to it."
        ),
    }
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "task2_slippage_band.json").write_text(
        json.dumps(findings, indent=2, sort_keys=True), encoding="utf-8"
    )
    AppendOnlyLedger(DATA / "carve_out_reads.jsonl").append(
        {
            "kind": "carve_out_slippage_band",
            "half": "post_holdout",
            "sessions": manifest["sessions"],
            "sessions_used": band.sessions_used,
            "measured_shift_usd_per_share": band.measured_shift_usd_per_share,
            "quote_requests_sent": sent["n"],
        }
    )

    say("")
    say(f"{'leg / end':<26}{'carried':>10}{'measured':>12}{'ratio':>9}  verdict")
    for name, row in against_carried.items():
        ratio = row["ratio_measured_over_carried"]
        say(
            f"{name:<26}{row['carried']:>10.4f}{row['measured']:>12.6f}"
            f"{(ratio if ratio is not None else 0):>9.3f}  {row['verdict']}"
        )
    say("")
    say(
        f"MEASURED SHIFT   {band.measured_shift_usd_per_share:.6f} USD/share "
        f"(carried band gives {findings['carried_shift_usd_per_share']:.6f})"
    )
    say(
        f"  entry n = {band.entry_observations} "
        f"({band.entry_gapped_through} gapped, "
        f"{band.entry_crossed_intrabar} intrabar); "
        f"stop n = {band.stop_observations}; close n = {band.close_observations}"
    )
    served = band.entry_quote_minutes_served + band.stop_quote_minutes_served
    refused = band.entry_quote_minutes_refused + band.stop_quote_minutes_refused
    say(f"  quote minutes served {served}, refused {refused}")
    say(f"  quote requests sent: {sent['n']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
