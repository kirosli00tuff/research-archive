"""Task 2 of the H2 amendment stage: backfill the main-dex fallback controls.

One shot over the 24 fresh-cohort events the same-dex rule could not pair
(`data/eligibility/h2.jsonl`, reason `no_control_candidate`). For each, at
its **original** entry timestamp:

  1. re-verify the same-dex candidate set is empty by the census dates —
     a non-empty set here would contradict the A.2 ledger and is a loud
     refusal, never a silent overwrite;
  2. assign the nearest funding-matched main-dex elder through the pinned
     matcher, trailing-only, append-only, tagged `cross_dex`;
  3. queue the control leg on the fresh plan and advance its funding
     archive to min(now, entry + 91d), the same bars as every other leg;
  4. take the control-leg l2Book snapshot where the entry window is still
     open, and write the loud `expired` record where it has closed.

The candidate trailing windows are sealed once as a single wide raw window
per candidate and then read back **through the blindness gate at each
event's own entry**, so no event ever sees a rate stamped after itself.
Nothing here parses a candle field or a post-entry rate.
"""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

from npl.absence import Absent
from npl.archive import advance_funding_archive
from npl.census import CensusLedger, CensusRow
from npl.clock import MS_PER_DAY, MS_PER_HOUR, iso_z, now_utc, utc_ms
from npl.config import CONFIG
from npl.controls import PAIR_TYPE_CROSS_DEX, Candidate, assign_control
from npl.http import InfoClient
from npl.ledger.append_only import AppendOnlyLedger
from npl.ledger.requests import RequestLedger
from npl.pacing import OPERATING_PACING_S
from npl.paths import (
    ELIGIBILITY_DIR,
    FRESH_PLAN,
    FUNDING_DIR,
    H2_PAIRS_LEDGER,
    REPORTS,
    SPREADS_DIR,
)
from npl.register.fallback import (
    candidate_census_rows,
    main_dex_candidate_rows,
    read_sealed_trail,
    seal_trail_window,
)
from npl.register.forward import append_fresh_plan_row, existing_pair_keys, latest_census
from npl.spread import record_leg_spread
from npl.venue import Venue

REPORT = REPORTS / "stage_a_h2" / "backfill_fallback.json"
PAIR_SPREADS = SPREADS_DIR / "pair_spreads.jsonl"
TRAIL_HOURS = CONFIG.control_trailing_window_hours


class BackfillRefusal(RuntimeError):
    """A precondition of the backfill does not hold. Loud, never repaired."""


def unpairable_events() -> list[dict[str, object]]:
    """The A.2 ledger's `no_control_candidate` rows, in ledger order."""
    rows = AppendOnlyLedger(ELIGIBILITY_DIR / "h2.jsonl").read().rows
    return [r for r in rows if not r.get("eligible") and r.get("reason") == "no_control_candidate"]


def _report(payload: dict[str, object]) -> None:
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def main() -> int:
    events = unpairable_events()
    if not events:
        raise BackfillRefusal("the H2 eligibility ledger holds no unpairable events; nothing to do")

    census_rows: list[CensusRow] = CensusLedger().rows()
    latest = latest_census(census_rows)
    already = existing_pair_keys()

    entries = sorted({int(str(e["entry_ms"])) for e in events})
    window_start = min(entries) - TRAIL_HOURS * MS_PER_HOUR
    window_end = max(entries)

    # The candidate union across every entry: one wide sealed window each.
    universe: dict[str, CensusRow] = {}
    for entry in entries:
        for row in main_dex_candidate_rows(latest, entry, "", CONFIG):
            universe[row.coin] = row

    ledger = RequestLedger()
    venue = Venue(InfoClient(ledger, pacing_s=OPERATING_PACING_S))
    today = now_utc().date().isoformat()
    spent_before = ledger.spent_on(today)

    seal_states: Counter[str] = Counter()
    pages_sealed = 0
    for i, coin in enumerate(sorted(universe), start=1):
        pages, state = seal_trail_window(venue, coin, window_start, window_end, FUNDING_DIR)
        pages_sealed += pages
        seal_states[state] += 1
        if i % 25 == 0:
            print(f"  candidate trails {i}/{len(universe)} (+{pages_sealed} pages)", flush=True)
    print(f"candidate trails: {len(universe)} coins, {pages_sealed} pages, {dict(seal_states)}")

    # Each event's own short trailing window.
    for event in events:
        pages, state = seal_trail_window(
            venue,
            str(event["coin"]),
            int(str(event["entry_ms"])) - TRAIL_HOURS * MS_PER_HOUR,
            int(str(event["entry_ms"])),
            FUNDING_DIR,
        )
        pages_sealed += pages
        seal_states[state] += 1

    assigned: list[dict[str, object]] = []
    unassigned: Counter[str] = Counter()
    for event in events:
        coin = str(event["coin"])
        dex = str(event["dex"])
        entry = int(str(event["entry_ms"]))
        listing = int(str(event["listing_open_ms"]))
        if (coin, entry) in already:
            unassigned["already_assigned"] += 1
            continue
        same_dex = candidate_census_rows(latest, dex, entry, coin, CONFIG)
        if same_dex:
            raise BackfillRefusal(
                f"{coin} has {len(same_dex)} same-dex candidates by the census dates, but the "
                f"A.2 ledger recorded no_control_candidate. The fallback is registered only "
                f"where the same-dex set is empty; refusing to guess which record is right."
            )
        trail_start = entry - TRAIL_HOURS * MS_PER_HOUR
        candidates = [
            Candidate(
                coin=row.coin,
                listing_open_ms=row.first_1d_open_ms or 0,
                rows=read_sealed_trail(row.coin, entry, trail_start, FUNDING_DIR),
            )
            for row in main_dex_candidate_rows(latest, entry, coin, CONFIG)
        ]
        event_rows = read_sealed_trail(coin, entry, trail_start, FUNDING_DIR)
        result = assign_control(
            coin,
            dex,
            entry,
            event_rows,
            [],
            CONFIG,
            # H2's own ledger, never H1's default PAIRS_LEDGER.
            pairs_path=H2_PAIRS_LEDGER,
            fallback_candidates=candidates,
        )
        if isinstance(result, Absent):
            unassigned[result.reason.value] += 1
            print(f"  {coin}: unassigned ({result.reason.value})")
            continue
        if result.pair_type != PAIR_TYPE_CROSS_DEX:
            raise BackfillRefusal(f"{coin} assigned {result.pair_type}; the backfill is cross_dex")
        append_fresh_plan_row("control", result.control_coin, result.control_dex, coin, listing)
        assigned.append(
            {
                "event_coin": coin,
                "dex": dex,
                "control_coin": result.control_coin,
                "control_dex": result.control_dex,
                "pair_type": result.pair_type,
                "entry_ms": entry,
                "candidates_considered": result.candidates_considered,
                "candidates_skipped_low_coverage": result.candidates_skipped_low_coverage,
            }
        )
        print(f"  {coin} -> {result.control_coin} ({result.pair_type})")

    # The control legs: funding archive to the same bars, and the touch state.
    now_ms = utc_ms(now_utc())
    archives: list[dict[str, object]] = []
    spreads: Counter[str] = Counter()
    for pair in assigned:
        control = str(pair["control_coin"])
        entry = int(str(pair["entry_ms"]))
        span_start = entry + CONFIG.backfill_funding_start_offset_hours * MS_PER_HOUR
        span_end = min(entry + CONFIG.backfill_funding_end_offset_days * MS_PER_DAY, now_ms)
        advance = advance_funding_archive(venue, control, span_start, span_end, page_budget=60)
        archives.append(
            {
                "coin": control,
                "pages_fetched": advance.pages_fetched,
                "rows_seen": advance.rows_seen,
                "caught_up": advance.caught_up,
                "terminal_state": advance.terminal_state,
            }
        )
        age_minutes = (now_ms - entry) / 60_000.0
        if 0 <= age_minutes <= CONFIG.spread_snapshot_window_minutes:
            spreads[
                record_leg_spread(
                    venue,
                    control,
                    hypothesis="H2",
                    role="control",
                    event_coin=str(pair["event_coin"]),
                    ledger_path=PAIR_SPREADS,
                ).value
            ] += 1
        else:
            AppendOnlyLedger(PAIR_SPREADS).append(
                {
                    "kind": "expired",
                    "hypothesis": "H2",
                    "event_coin": pair["event_coin"],
                    "coin": control,
                    "role": "control",
                    "entry_ms": entry,
                    "at": iso_z(now_utc()),
                    "state": "expired",
                    "note": (
                        f"the {CONFIG.spread_snapshot_window_minutes}-minute two-leg window "
                        f"closed {age_minutes / 1440.0:.1f} days after entry; never backfilled"
                    ),
                }
            )
            spreads["expired"] += 1

    all_pairs = AppendOnlyLedger(H2_PAIRS_LEDGER).read().rows
    by_tag = Counter(str(r.get("pair_type", "same_dex")) for r in all_pairs)
    payload: dict[str, object] = {
        "ran_at": iso_z(now_utc()),
        "amendment": "H2-3 Change 1",
        "events_attempted": len(events),
        "assigned": assigned,
        "assigned_n": len(assigned),
        "unassigned_reasons": dict(unassigned),
        "distinct_controls": len({str(p["control_coin"]) for p in assigned}),
        "candidate_universe_n": len(universe),
        "candidate_trail_window": {"start_ms": window_start, "end_ms": window_end},
        "trail_seal_states": dict(seal_states),
        "trail_pages_sealed": pages_sealed,
        "control_leg_archives": archives,
        "control_leg_spread_states": dict(spreads),
        "pairs_ledger_total": len(all_pairs),
        "pairs_ledger_by_tag": dict(by_tag),
        "fresh_plan_rows": AppendOnlyLedger(FRESH_PLAN).count(),
        "requests_spent_this_run": ledger.spent_on(today) - spent_before,
        "outcome_values_read": 0,
    }
    _report(payload)
    summary = {k: v for k, v in payload.items() if k not in ("assigned", "control_leg_archives")}
    print(json.dumps(summary, indent=2, sort_keys=True))
    print(f"report -> {REPORT.relative_to(Path.cwd())}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
