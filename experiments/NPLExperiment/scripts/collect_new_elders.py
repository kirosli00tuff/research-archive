"""Task 3 of H2 Amendment Stage 2: collect the control legs the tiered rule introduced.

Every elder the reassignment introduced needs the same collection the
superseded elders already carry, at the **same entry-relative windows**:

  - the registered candle window, entry minus 1 day through entry + 91 days,
    sealed raw by the sealed writer (this script parses no candle field);
  - the registered funding archive, entry minus 168 hours through entry + 91
    days, advanced page by page under the request ledger;
  - the two-leg l2Book touch state where the registered 30-minute window at
    entry is still open, and a **loud `expired` record** where it has closed.
    A stale spread is not a spread and is never backfilled.

Both legs are then queued on the fresh plan, so the daily pass keeps
advancing them exactly as it does every other leg.

An `(elder, entry)` window the superseded assignment already collected is
skipped as already held: the raw bytes on disk are the record.

Coverage is reported per new elder against the registered bars — 0.90 of the
candle days, 0.95 of the funding hours. A window that has not yet elapsed is
reported as what it is: coverage so far, over a window still open. An event
that fails a bar is counted **underpowered**, never a negative.
"""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

from npl.archive import advance_funding_archive, backfill_event_candles, event_funding_span
from npl.blindness import candle_times, funding_rows
from npl.clock import MS_PER_DAY, MS_PER_HOUR, iso_z, now_utc, utc_ms
from npl.config import CONFIG
from npl.coverage import (
    assess_event_coverage,
    candle_day_coverage,
    funding_hour_coverage,
)
from npl.http import InfoClient
from npl.ledger.append_only import AppendOnlyLedger
from npl.ledger.requests import RequestLedger
from npl.pacing import OPERATING_PACING_S
from npl.paths import (
    FUNDING_DIR,
    H2_PAIRS_LEDGER,
    H2_PAIRS_V2_LEDGER,
    OUTCOMES_DIR,
    REPORTS,
    SPREADS_DIR,
)
from npl.register.forward import append_fresh_plan_row
from npl.register.tiered import assigned_rows
from npl.spread import record_leg_spread
from npl.venue import Venue

REPORT = REPORTS / "stage_a_h2" / "collect_new_elders.json"
PAIR_SPREADS = SPREADS_DIR / "pair_spreads.jsonl"
LISTING_LAG_DAYS = CONFIG.entry_anchor_offset_days + 1


def _coin_dir(root: Path, coin: str) -> Path:
    return root / coin.replace(":", "_")


def leg_coverage(coin: str, entry_ms: int, now_ms: int) -> dict[str, object]:
    """Coverage of one leg's registered windows. Timestamps and counts only.

    Reads the sealed candle bytes for `t`, `T`, and the row count, and the
    archived funding pages for `time`. No priced field is parsed here and no
    funding rate is read for a value — `funding_hour_coverage` counts
    distinct hours, nothing else.
    """
    candle_start = entry_ms + CONFIG.backfill_candle_start_offset_days * MS_PER_DAY
    candle_end = entry_ms + CONFIG.backfill_candle_end_offset_days * MS_PER_DAY
    funding_start, funding_end = (
        entry_ms + CONFIG.backfill_funding_start_offset_hours * MS_PER_HOUR,
        entry_ms + CONFIG.backfill_funding_end_offset_days * MS_PER_DAY,
    )
    elapsed_candle_end = min(candle_end, now_ms)
    elapsed_funding_end = min(funding_end, now_ms)

    sealed = _coin_dir(OUTCOMES_DIR, coin) / f"retro-candles-{entry_ms // MS_PER_DAY}.raw"
    if sealed.exists():
        candles = candle_day_coverage(
            candle_times(sealed.read_bytes()), candle_start, elapsed_candle_end
        )
    else:
        candles = candle_day_coverage(candle_times(b"[]"), candle_start, elapsed_candle_end)

    directory = _coin_dir(FUNDING_DIR, coin)
    rows: list[object] = []
    if directory.exists():
        seen: dict[int, object] = {}
        for page in sorted(directory.glob("page-*.raw")):
            for row in funding_rows(page.read_bytes(), entry_ms=None):
                seen.setdefault(row.time_ms, row)
        rows = list(seen.values())
    funding = funding_hour_coverage(
        tuple(rows),  # type: ignore[arg-type]
        funding_start,
        elapsed_funding_end,
    )
    assessed = assess_event_coverage(coin, candles, funding)
    return {
        "coin": coin,
        "entry_ms": entry_ms,
        "window_still_open": candle_end > now_ms,
        "candle_days_expected_so_far": candles.expected,
        "candle_days_present": candles.present,
        "candle_share": candles.share(),
        "funding_hours_expected_so_far": funding.expected,
        "funding_hours_present": funding.present,
        "funding_share": funding.share(),
        "meets_bars": assessed.meets_bars,
        "label": assessed.label,
    }


def main() -> int:
    pairs = assigned_rows(AppendOnlyLedger(H2_PAIRS_V2_LEDGER).require_intact())
    superseded = AppendOnlyLedger(H2_PAIRS_LEDGER).require_intact()
    already = {(str(r["control_coin"]), int(str(r["entry_ms"]))) for r in superseded}

    new_legs = [
        r for r in pairs if (str(r["control_coin"]), int(str(r["entry_ms"]))) not in already
    ]
    print(f"{len(pairs)} tiered pairs, {len(new_legs)} control legs the tiered rule introduced")

    ledger = RequestLedger()
    venue = Venue(InfoClient(ledger, pacing_s=OPERATING_PACING_S))
    today = now_utc().date().isoformat()
    spent_before = ledger.spent_on(today)
    now_ms = utc_ms(now_utc())

    candle_states: Counter[str] = Counter()
    spreads: Counter[str] = Counter()
    archives: list[dict[str, object]] = []
    for i, row in enumerate(new_legs, start=1):
        elder = str(row["control_coin"])
        elder_dex = str(row["control_dex"])
        event = str(row["event_coin"])
        entry = int(str(row["entry_ms"]))
        listing = entry - LISTING_LAG_DAYS * MS_PER_DAY

        state = backfill_event_candles(venue, elder, listing)
        candle_states[state.value] += 1

        span_start, span_end = event_funding_span(listing)
        advance = advance_funding_archive(
            venue, elder, span_start, min(span_end, now_ms), page_budget=60
        )
        archives.append(
            {
                "coin": elder,
                "event": event,
                "entry_ms": entry,
                "candle_state": state.value,
                "funding_pages_fetched": advance.pages_fetched,
                "funding_rows_seen": advance.rows_seen,
                "funding_caught_up": advance.caught_up,
                "funding_terminal_state": advance.terminal_state,
            }
        )

        append_fresh_plan_row("control", elder, elder_dex, event, listing)

        age_minutes = (now_ms - entry) / 60_000.0
        if 0 <= age_minutes <= CONFIG.spread_snapshot_window_minutes:
            spreads[
                record_leg_spread(
                    venue,
                    elder,
                    hypothesis="H2",
                    role="control",
                    event_coin=event,
                    ledger_path=PAIR_SPREADS,
                ).value
            ] += 1
        else:
            AppendOnlyLedger(PAIR_SPREADS).append(
                {
                    "kind": "expired",
                    "hypothesis": "H2",
                    "event_coin": event,
                    "coin": elder,
                    "role": "control",
                    "entry_ms": entry,
                    "at": iso_z(now_utc()),
                    "state": "expired",
                    "note": (
                        f"the {CONFIG.spread_snapshot_window_minutes}-minute two-leg window "
                        f"closed {age_minutes / 1440.0:.1f} days after entry; never backfilled. "
                        f"Amendment H2-5 reassigned this pair long after its entry, so the "
                        f"touch state at entry is unrecoverable and is recorded absent."
                    ),
                }
            )
            spreads["expired"] += 1
        print(f"  {i:>2}/{len(new_legs)} {elder:<18} for {event:<18} {state.value}", flush=True)

    # --- coverage per new elder, and the events that now fail a bar --------
    per_leg = [
        leg_coverage(str(r["control_coin"]), int(str(r["entry_ms"])), now_ms) for r in new_legs
    ]
    underpowered: list[dict[str, object]] = []
    for row in pairs:
        entry = int(str(row["entry_ms"]))
        young = leg_coverage(str(row["event_coin"]), entry, now_ms)
        elder = leg_coverage(str(row["control_coin"]), entry, now_ms)
        if not (young["meets_bars"] and elder["meets_bars"]):
            underpowered.append(
                {
                    "event": row["event_coin"],
                    "elder": row["control_coin"],
                    "entry_ms": entry,
                    "window_still_open": young["window_still_open"],
                    "young": young,
                    "elder_leg": elder,
                }
            )

    spent_after = ledger.spent_on(today)
    payload: dict[str, object] = {
        "stage": "H2 Amendment Stage 2 - Task 3, control-leg collection for new elders",
        "amendment": "H2-5",
        "ran_at": iso_z(now_utc()),
        "outcome_values_read": 0,
        "tiered_pairs": len(pairs),
        "new_control_legs": len(new_legs),
        "distinct_new_elders": len({str(r["control_coin"]) for r in new_legs}),
        "candle_seal_states": dict(candle_states),
        "spread_states": dict(spreads),
        "archives": archives,
        "coverage_per_new_elder": per_leg,
        "pairs_failing_a_coverage_bar": {
            "n": len(underpowered),
            "counted_as": "underpowered",
            "note": (
                "a pair under a bar is underpowered, never a negative. Most of these are "
                "windows that have not yet elapsed: the 30-day primary is not readable until "
                "the candle window seals at entry + 92 days (ADR-019)."
            ),
            "detail": underpowered,
        },
        "spend": {
            "day": today,
            "charged_before": spent_before,
            "charged_after": spent_after,
            "charged_by_this_pass": spent_after - spent_before,
            "cap": CONFIG.request_cap_per_day,
        },
    }
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    print()
    print(f"new control legs:  {len(new_legs)} ({payload['distinct_new_elders']} distinct elders)")
    print(f"candle seals:      {dict(candle_states)}")
    print(f"spread states:     {dict(spreads)}")
    print(f"failing a bar:     {len(underpowered)} of {len(pairs)} pairs, counted underpowered")
    print(f"charged this pass: {spent_after - spent_before} of {CONFIG.request_cap_per_day}")
    print(f"report -> {REPORT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
