"""Task 2 of H2 Amendment Stage 2: reassign every pair under the tiered rule.

One shot over the 63 events in the superseded ledger
(`data/controls/h2_pairs.jsonl`), each at its **original** entry timestamp.
For each event, in entry order:

  1. classify the event's ticker through the registered taxonomy — an
     unclassifiable ticker is recorded with its reason and never guessed;
  2. build the admissible elders by the registered census dates (aged 180
     days, still serving) across **every** dex, and classify each;
  3. assign through the tiered selector — tier 1 same dex and exact class,
     tier 2 any dex and exact class, tier 3 any dex within the equity
     complex for equity-complex legs only — trailing-only, append-only;
  4. write the row to `data/controls/h2_pairs_v2.jsonl`, carrying the tier,
     the class pair, both trailing means, the funding distance, the
     candidates considered, and the assignment timestamp.

The superseded ledger is **read and never written**: `assert_not_superseded`
refuses any assignment target that resolves to it, and its hash is verified
at the close of the stage.

Trailing windows are read back from sealed raw bytes **through the blindness
gate at each event's own entry**, so no event sees a rate stamped after
itself. A window that is not yet sealed to the coverage bar is fetched and
sealed under the request ledger, which charges before sending. Nothing here
parses a candle field or a post-entry rate.
"""

from __future__ import annotations

import json
from collections import Counter
from dataclasses import asdict

from npl.blindness import FundingRow
from npl.census import CensusLedger
from npl.clock import MS_PER_HOUR, iso_z, now_utc
from npl.config import CONFIG
from npl.controls import trailing_mean
from npl.http import InfoClient
from npl.ledger.append_only import AppendOnlyLedger
from npl.ledger.requests import RequestLedger
from npl.pacing import OPERATING_PACING_S
from npl.paths import FUNDING_DIR, H2_PAIRS_LEDGER, H2_PAIRS_V2_LEDGER, REPORTS
from npl.register.assetclass import asset_class
from npl.register.fallback import admissible_census_rows, read_sealed_trail, seal_trail_window
from npl.register.forward import latest_census
from npl.register.tiered import (
    CandidateRef,
    TieredAssignment,
    assign_control_tiered,
)
from npl.venue import Venue

REPORT = REPORTS / "stage_a_h2" / "reassign_tiered.json"
TRAIL_HOURS = CONFIG.control_trailing_window_hours


class ReassignRefusal(RuntimeError):
    """A precondition of the reassignment does not hold. Loud, never repaired."""


def superseded_events() -> list[dict[str, object]]:
    """The 63 events of the H2-3 assignment, in entry order. Read only."""
    rows = AppendOnlyLedger(H2_PAIRS_LEDGER).require_intact()
    return sorted(rows, key=lambda r: (int(str(r["entry_ms"])), str(r["event_coin"])))


def main() -> int:
    events = superseded_events()
    if not events:
        raise ReassignRefusal("the superseded H2 pairs ledger is empty; nothing to reassign")

    latest = latest_census(CensusLedger().rows())
    done = {
        (str(r["event_coin"]), int(str(r["entry_ms"])))
        for r in AppendOnlyLedger(H2_PAIRS_V2_LEDGER).read().rows
    }

    ledger = RequestLedger()
    venue = Venue(InfoClient(ledger, pacing_s=OPERATING_PACING_S))
    today = now_utc().date().isoformat()
    spent_before = ledger.spent_on(today)

    trails: dict[tuple[str, int], tuple[FundingRow, ...]] = {}
    seal_states: Counter[str] = Counter()

    def trail_for(coin: str, entry_ms: int) -> tuple[FundingRow, ...]:
        """The sealed trailing window, gated at this entry. Sealed if short.

        Read first: the raw bytes already on disk are the record, and a
        fetch is a charge. Only a window that does not already clear the
        registered coverage bar is fetched.
        """
        key = (coin, entry_ms)
        if key in trails:
            return trails[key]
        start = entry_ms - TRAIL_HOURS * MS_PER_HOUR
        rows = read_sealed_trail(coin, entry_ms, start, FUNDING_DIR)
        if isinstance(trailing_mean(rows, entry_ms, CONFIG), float):
            trails[key] = rows
            return rows
        _, state = seal_trail_window(venue, coin, start, entry_ms, FUNDING_DIR)
        seal_states[state] += 1
        rows = read_sealed_trail(coin, entry_ms, start, FUNDING_DIR)
        trails[key] = rows
        return rows

    assignments: list[TieredAssignment] = []
    exclusions: list[dict[str, object]] = []
    tiers: Counter[str] = Counter()
    class_pairs: Counter[str] = Counter()
    reasons: Counter[str] = Counter()

    for i, event in enumerate(events, start=1):
        coin = str(event["event_coin"])
        dex = str(event["dex"])
        entry = int(str(event["entry_ms"]))
        if (coin, entry) in done:
            tiers["already_assigned"] += 1
            continue

        refs: list[CandidateRef] = []
        for row in admissible_census_rows(latest, entry, coin, CONFIG):
            candidate_class = asset_class(row.coin, row.dex)
            if candidate_class is None:
                continue  # counted in the universe report, never a candidate
            refs.append(
                CandidateRef(
                    coin=row.coin,
                    dex=row.dex,
                    asset_class=candidate_class,
                    listing_open_ms=row.first_1d_open_ms or 0,
                )
            )

        event_rows = trail_for(coin, entry) if asset_class(coin, dex) is not None else ()
        result = assign_control_tiered(
            coin,
            dex,
            entry,
            event_rows,
            refs,
            lambda ref, _entry=entry: trail_for(ref.coin, _entry),  # type: ignore[misc]
            CONFIG,
            pairs_path=H2_PAIRS_V2_LEDGER,
        )
        if isinstance(result, TieredAssignment):
            assignments.append(result)
            tiers[f"tier_{result.tier}"] += 1
            class_pairs[result.class_pair] += 1
        else:
            row = asdict(result)
            exclusions.append(row)
            tiers[result.state] += 1
            reasons[f"{result.state}:{result.reason.split(' (')[0]}"] += 1
            AppendOnlyLedger(H2_PAIRS_V2_LEDGER).append(row)
        print(
            f"  {i:>2}/{len(events)} {coin:<18} -> "
            f"{result.control_coin if isinstance(result, TieredAssignment) else result.state}",
            flush=True,
        )

    # --- what changed against the superseded assignment --------------------
    old = {str(r["event_coin"]): r for r in events}
    changed = 0
    kept = 0
    old_distance: list[float] = []
    new_distance: list[float] = []
    changes: list[dict[str, object]] = []
    for a in assignments:
        prior = old[a.event_coin]
        old_d = abs(float(prior["control_trailing_mean"]) - float(prior["event_trailing_mean"]))  # type: ignore[arg-type]
        old_distance.append(old_d)
        new_distance.append(a.funding_distance)
        if str(prior["control_coin"]) != a.control_coin:
            changed += 1
        else:
            kept += 1
        changes.append(
            {
                "event": a.event_coin,
                "superseded_elder": prior["control_coin"],
                "tiered_elder": a.control_coin,
                "elder_changed": str(prior["control_coin"]) != a.control_coin,
                "tier": a.tier,
                "class_pair": a.class_pair,
                "superseded_funding_distance": old_d,
                "tiered_funding_distance": a.funding_distance,
            }
        )

    def mean(xs: list[float]) -> float | None:
        return sum(xs) / len(xs) if xs else None

    spent_after = ledger.spent_on(today)
    payload: dict[str, object] = {
        "stage": "H2 Amendment Stage 2 - Task 2, reassignment under the tiered rule",
        "amendment": "H2-5",
        "computed_at": iso_z(now_utc()),
        "outcome_values_read": 0,
        "events_in_superseded_ledger": len(events),
        "pairs_assigned": len(assignments),
        "tier_distribution": dict(sorted(tiers.items())),
        "class_pair_distribution": dict(sorted(class_pairs.items())),
        "exclusion_reasons": dict(sorted(reasons.items())),
        "exclusions": exclusions,
        "elders_changed": changed,
        "elders_kept": kept,
        "funding_distance": {
            "n": len(new_distance),
            "mean_abs_superseded": mean(old_distance),
            "mean_abs_tiered": mean(new_distance),
            "note": (
                "mean absolute signed trailing 168-hour mean hourly funding distance between "
                "event and elder, over the pairs that survive the tiered rule, against the same "
                "events' superseded distances. A larger figure is the registered accepted "
                "degradation of Amendment H2-5 section 4."
            ),
        },
        "per_event": changes,
        "spend": {
            "day": today,
            "charged_before": spent_before,
            "charged_after": spent_after,
            "charged_by_this_pass": spent_after - spent_before,
            "cap": CONFIG.request_cap_per_day,
            "trail_seal_states": dict(seal_states),
        },
        "superseded_ledger": {
            "path": str(H2_PAIRS_LEDGER),
            "written": False,
            "note": "read only; assert_not_superseded refuses it as an assignment target",
        },
    }
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    print()
    print(f"pairs assigned:       {len(assignments)} of {len(events)} events")
    print(f"tier distribution:    {dict(sorted(tiers.items()))}")
    print(f"class pairs:          {dict(sorted(class_pairs.items()))}")
    print(f"exclusions:           {dict(sorted(reasons.items()))}")
    print(f"elders changed:       {changed} changed, {kept} kept")
    print(
        f"mean |funding dist|:  superseded {mean(old_distance)!r} -> tiered {mean(new_distance)!r}"
    )
    print(f"charged this pass:    {spent_after - spent_before} of {CONFIG.request_cap_per_day}")
    print(f"report -> {REPORT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
