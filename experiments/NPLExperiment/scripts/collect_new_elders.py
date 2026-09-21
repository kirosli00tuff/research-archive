"""Task 3 of H2 Amendment Stage 2: collect the control legs the tiered rule introduced.

Every elder the reassignment introduced needs the same collection the
superseded elders already carry, at the **same entry-relative windows**:

  - the registered candle window, entry minus 1 day through entry + 91 days,
    sealed raw by the sealed writer (this script parses no candle field) —
    **only once the window has matured**, at entry + 92 days, exactly as the
    daily pass gates it. `backfill_event_candles` short-circuits on file
    existence and never refetches, so a premature seal is a partial window
    that stays partial forever. A window not yet mature is recorded
    `pending_seal` and left to the fresh plan, which seals it at maturity;
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
from npl.blindness import FundingRow, candle_times, funding_rows
from npl.census import CensusLedger
from npl.clock import MS_PER_DAY, iso_z, now_utc, utc_ms
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
from npl.register.forward import append_fresh_plan_row, latest_census
from npl.register.tiered import assigned_rows
from npl.spread import record_leg_spread
from npl.venue import Venue

REPORT = REPORTS / "stage_a_h2" / "collect_new_elders.json"
PAIR_SPREADS = SPREADS_DIR / "pair_spreads.jsonl"
LISTING_LAG_DAYS = CONFIG.entry_anchor_offset_days + 1
HORIZON_DAYS = CONFIG.horizon_primary_days
# ADR-019: the candle window seals once, at entry + 92 days. The same gate the
# daily pass uses; a premature seal is a partial window that never refills.
MATURITY_DAYS = CONFIG.backfill_candle_end_offset_days + 1
STATE_PENDING_SEAL = "pending_seal"


def _coin_dir(root: Path, coin: str) -> Path:
    return root / coin.replace(":", "_")


def leg_coverage(coin: str, entry_ms: int, now_ms: int, horizon_days: int) -> dict[str, object]:
    """Coverage of one leg's registered OUTCOME window. Timestamps and counts only.

    The window is the registered one, identical to `npl.stageb.preconditions`:
    **candles from entry minus one day through entry + horizon; funding hours
    from entry through entry + horizon.** It is deliberately *not* the
    collection span (entry minus 168 hours through entry + 91 days) — the
    trailing 168 hours are the matcher's input, not the outcome's, and a young
    leg cannot have funding for the 120 hours before it existed, so measuring
    the bar over the collection span would fail every young leg by
    construction.

    Reads the sealed candle bytes for `t`, `T`, and the row count, and the
    archived funding pages for `time`. No priced field is parsed here and no
    funding rate is read for a value — `funding_hour_coverage` counts distinct
    hours, nothing else.
    """
    candle_start = entry_ms - MS_PER_DAY
    window_end = entry_ms + horizon_days * MS_PER_DAY
    elapsed_end = min(window_end, now_ms)

    sealed = _coin_dir(OUTCOMES_DIR, coin) / f"retro-candles-{entry_ms // MS_PER_DAY}.raw"
    payload = sealed.read_bytes() if sealed.exists() else b"[]"
    candles = candle_day_coverage(candle_times(payload), candle_start, elapsed_end)

    directory = _coin_dir(FUNDING_DIR, coin)
    seen: dict[int, FundingRow] = {}
    if directory.exists():
        for page in sorted(directory.glob("page-*.raw")):
            for row in funding_rows(page.read_bytes(), entry_ms=None):
                seen.setdefault(row.time_ms, row)
    funding = funding_hour_coverage(tuple(seen.values()), entry_ms, elapsed_end)

    assessed = assess_event_coverage(coin, candles, funding)
    return {
        "coin": coin,
        "entry_ms": entry_ms,
        "horizon_days": horizon_days,
        "sealed_candles_present": sealed.exists(),
        "candle_seal_due_ms": entry_ms + MATURITY_DAYS * MS_PER_DAY,
        "window_elapsed": window_end <= now_ms,
        "candle_days_expected": candles.expected,
        "candle_days_present": candles.present,
        "candle_share": candles.share(),
        "funding_hours_expected": funding.expected,
        "funding_hours_present": funding.present,
        "funding_share": funding.share(),
        "meets_bars_so_far": assessed.meets_bars if sealed.exists() else None,
        "label": assessed.label if sealed.exists() else STATE_PENDING_SEAL,
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

        if now_ms >= entry + MATURITY_DAYS * MS_PER_DAY:
            candle_state = backfill_event_candles(venue, elder, listing).value
        else:
            # Not a failure and not a skip: a recorded absence with its date.
            candle_state = STATE_PENDING_SEAL
        candle_states[candle_state] += 1

        span_start, span_end = event_funding_span(listing)
        advance = advance_funding_archive(
            venue, elder, span_start, min(span_end, now_ms), page_budget=60
        )
        archives.append(
            {
                "coin": elder,
                "event": event,
                "entry_ms": entry,
                "candle_state": candle_state,
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
        print(f"  {i:>2}/{len(new_legs)} {elder:<18} for {event:<18} {candle_state}", flush=True)

    # --- coverage per new elder, and the pairs that fail a bar -------------
    per_leg = [
        leg_coverage(str(r["control_coin"]), int(str(r["entry_ms"])), now_ms, HORIZON_DAYS)
        for r in new_legs
    ]
    underpowered: list[dict[str, object]] = []
    pending: list[dict[str, object]] = []
    assessable = 0
    for row in pairs:
        entry = int(str(row["entry_ms"]))
        young = leg_coverage(str(row["event_coin"]), entry, now_ms, HORIZON_DAYS)
        elder = leg_coverage(str(row["control_coin"]), entry, now_ms, HORIZON_DAYS)
        if young["meets_bars_so_far"] is None or elder["meets_bars_so_far"] is None:
            # Neither covered nor underpowered: the seal is not yet due.
            pending.append(
                {
                    "event": row["event_coin"],
                    "elder": row["control_coin"],
                    "entry_ms": entry,
                    "candle_seal_due_ms": young["candle_seal_due_ms"],
                    "young_sealed": young["sealed_candles_present"],
                    "elder_sealed": elder["sealed_candles_present"],
                }
            )
            continue
        assessable += 1
        if young["meets_bars_so_far"] and elder["meets_bars_so_far"]:
            continue
        underpowered.append(
            {
                "event": row["event_coin"],
                "elder": row["control_coin"],
                "entry_ms": entry,
                "tier": row["tier"],
                "class_pair": row["class_pair"],
                "window_elapsed": young["window_elapsed"],
                "failing_leg": (
                    "young"
                    if not young["meets_bars_so_far"]
                    else "elder"
                    if not elder["meets_bars_so_far"]
                    else "both"
                ),
                "young": young,
                "elder_leg": elder,
            }
        )

    # --- elders that stopped serving before their own pair's entry --------
    # The registered admissibility test looks only backwards: an instrument is
    # admissible if it was still serving at the TRAILING window's start. An
    # elder that stopped serving between that start and the entry therefore
    # passes admissibility and then has no outcome window at all. Reported
    # here rather than fixed: adding a delisting condition would change the
    # registered control rule, which is not this stage's registered scope.
    census = latest_census(CensusLedger().rows())
    by_coin = {coin: row for (coin, _dex), row in census.items()}
    dead_elders: list[dict[str, object]] = []
    for row in pairs:
        elder = str(row["control_coin"])
        entry = int(str(row["entry_ms"]))
        record = by_coin.get(elder)
        if record is None or record.last_1d_close_ms is None:
            continue
        if record.last_1d_close_ms >= entry:
            continue
        dead_elders.append(
            {
                "event": row["event_coin"],
                "elder": elder,
                "tier": row["tier"],
                "class_pair": row["class_pair"],
                "entry_ms": entry,
                "elder_last_1d_close_ms": record.last_1d_close_ms,
                "elder_is_delisted": record.is_delisted,
                "census_recorded_at": record.recorded_at,
                "reading": (
                    "delisted before this pair's entry; the pair has no elder entry price "
                    "and will be excluded underpowered at the registered read (Section 7)"
                    if record.is_delisted
                    else "not delisted; the census snapshot simply predates this entry, so "
                    "the elder was live and this row is a staleness artifact, not a gap"
                ),
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
        "coverage_window": {
            "horizon_days": HORIZON_DAYS,
            "candles": "entry minus 1 day through entry + horizon",
            "funding_hours": "entry through entry + horizon",
            "bars": {
                "candles": CONFIG.min_outcome_coverage_candles,
                "funding": CONFIG.min_outcome_coverage_funding,
            },
            "note": (
                "the registered outcome window, identical to npl.stageb.preconditions. NOT "
                "the collection span: the trailing 168 hours are the matcher's input, and a "
                "young leg cannot have funding for the 120 hours before it existed"
            ),
        },
        "elders_not_serving_at_their_pair_entry": {
            "n": len(dead_elders),
            "n_genuinely_delisted": sum(1 for d in dead_elders if d["elder_is_delisted"]),
            "note": (
                "the registered admissibility test (H1 Section 6, unchanged by Amendment "
                "H2-5) requires an elder to be serving at the TRAILING window's start, not "
                "at the entry. An elder delisted in between is admissible by the rule and "
                "then yields no outcome window. Recorded, not repaired: adding a delisting "
                "condition would change the registered control rule, which is outside this "
                "stage's registered scope. The registered machinery already handles it - "
                "the pair fails the 0.90 candle bar and is excluded UNDERPOWERED, counted, "
                "never a negative."
            ),
            "detail": dead_elders,
        },
        "pairs_pending_their_candle_seal": {
            "n": len(pending),
            "counted_as": STATE_PENDING_SEAL,
            "note": (
                "not covered and not underpowered: the candle window seals once, at entry "
                "+ 92 days (ADR-019), and the fresh plan seals it then. Absence is a "
                "recorded state, never a synthesized value and never a failure."
            ),
            "detail": pending,
        },
        "pairs_failing_a_coverage_bar": {
            "n": len(underpowered),
            "pairs_assessable_now": assessable,
            "counted_as": "underpowered",
            "note": (
                "a pair under a bar is underpowered, never a negative (Section 7). A pair "
                "whose window has not yet elapsed is not yet a failure: the 30-day primary "
                "is not readable until the candle window seals at entry + 92 days (ADR-019)."
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
    genuinely_dead = sum(1 for d in dead_elders if d["elder_is_delisted"])
    print(
        f"dead elders:       {genuinely_dead} delisted before their pair entry "
        f"({len(dead_elders)} flagged, the rest census staleness)"
    )
    print(f"pending seal:      {len(pending)} of {len(pairs)} pairs (seal due at entry + 92d)")
    print(f"failing a bar:     {len(underpowered)} of the {assessable} assessable, underpowered")
    print(f"charged this pass: {spent_after - spent_before} of {CONFIG.request_cap_per_day}")
    print(f"report -> {REPORT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
