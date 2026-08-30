"""A.0 TASK 3 — confirm the sealed probe slice was pulled on the consolidated tape.

**Confirm rather than assume.** `reports/stage_a1r/task9_probe_manifest.json`
records ``"feed": "sip"``, and that record was written by the same tool that
chose the feed — so on its own it is an assertion about a code path, not a
measurement of what the vendor actually served.

**The measurement, and why it is price-blind.** ``bar_count per session`` sits on
the readable field list (`orb.seal.READABLE_FIELDS`). The two feeds separate on
it by a wide margin: A.1 TASK 4 measured the single-venue feed at a **median
0.027761 of consolidated first-5-minute volume over `n = 100` pairs**, and the
same asymmetry shows in bar counts — AAPL over the tape window returned **4,134
bars on the consolidated feed and 2,049 on the single-venue one**. So
re-requesting a sealed chunk's *exact* window on **both** feeds and comparing
each served bar count against the **sealed file's recorded count** identifies the
tape without reading one price.

**This is not the re-pull and does not touch the revision clock.** It re-sends a
handful of windows under **new file names** in a separate namespace; the sealed
slice at `data/access/sealed_credentialed/task9_*.raw` is not written to, and
`tools/repull_probe.py` still refuses until 2026-09-12.
"""

from __future__ import annotations

import json
import sys
from datetime import UTC, datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from _a1r import DATA, REPORTS, send, wire, write_report

from orb.comparator import count_bars
from orb.redact import say
from orb.vendors import (
    MEASURED_SINGLE_VENUE_FEED,
    alpaca_minute_bars,
    alpaca_minute_bars_on_feed,
    consolidated_feed,
    require_manifest_feed,
)

MANIFEST = REPORTS / "task9_probe_manifest.json"
SEALED_ROOT = DATA / "sealed_credentialed"
SAMPLE_TICKERS = 8
"""Eight chunks, two feeds each: `n = 16` requests. A confirmation, not a survey.

Eight rather than four because **a chunk can be uninformative**. The first run of
this tool sampled four and one of them, `AADX`, served **0 bars on both feeds** —
a name with no trades in that window. A 0-against-0 comparison identifies no
tape, and counting it either way would be a synthesized measurement. It is
classified `uninformative` below and excluded from the verdict, per standing rule
5 and standing rule 7: an operational condition never quietly becomes a data
condition.
"""

TAPE_CONTROL_REASON = (
    "Amendment 13 feed confirmation: the single-venue feed is requested on "
    "purpose, beside the consolidated one, so that the sealed slice's recorded "
    "bar count can be matched against both and the tape identified rather than "
    "assumed."
)


def main() -> int:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    recorded_feed = require_manifest_feed(manifest, f"confirmation of {MANIFEST.name}")

    files_stored = int(manifest["files_stored"])
    bars_stored = int(manifest["bars_stored"])
    say(
        f"manifest records feed={recorded_feed!r}, files_stored={files_stored}, "
        f"bars_stored={bars_stored}"
    )

    on_disk = sorted(p.name for p in SEALED_ROOT.glob("task9_*chunk*_page*.raw"))
    say(f"sealed bar files on disk: n = {len(on_disk)}")

    entries = manifest["manifest"]
    seen: set[str] = set()
    sample: list[dict[str, object]] = []
    for entry in entries:
        ticker = str(entry["ticker"])
        if ticker in seen:
            continue
        seen.add(ticker)
        sample.append(entry)
        if len(sample) >= SAMPLE_TICKERS:
            break

    store, client, seal = wire()
    checks: list[dict[str, object]] = []
    for entry in sample:
        ticker = str(entry["ticker"])
        start_iso = str(entry["start_iso"])
        end_iso = str(entry["end_iso"])
        sealed_count = int(entry["bar_count"])
        stored_file = str(entry["stored_file"])
        sealed_bytes = (SEALED_ROOT / stored_file).read_bytes()
        sealed_recount = count_bars(sealed_bytes)

        consolidated = send(
            client,
            alpaca_minute_bars(
                store, ticker, start_iso, end_iso, feed=recorded_feed, limit=10000
            ),
        )
        seal.store(
            f"task3b_feedconfirm_{ticker}_{recorded_feed}.raw", consolidated.body
        )
        consolidated_count = count_bars(consolidated.body)

        single = send(
            client,
            alpaca_minute_bars_on_feed(
                store,
                ticker,
                start_iso,
                end_iso,
                feed=MEASURED_SINGLE_VENUE_FEED,
                tape_control_reason=TAPE_CONTROL_REASON,
                limit=10000,
            ),
        )
        seal.store(
            f"task3b_feedconfirm_{ticker}_{MEASURED_SINGLE_VENUE_FEED}.raw", single.body
        )
        single_count = count_bars(single.body)

        matches_consolidated = sealed_recount == consolidated_count
        matches_single = sealed_recount == single_count
        # A chunk identifies a tape only when the two feeds actually differ on
        # it. Both serving zero bars is a name that did not trade, not evidence.
        discriminating = consolidated_count != single_count
        checks.append(
            {
                "discriminating": discriminating,
                "why_not_discriminating": (
                    None
                    if discriminating
                    else (
                        "both feeds served the same bar count "
                        f"({consolidated_count}); this window identifies no tape "
                        "and is excluded from the verdict rather than counted "
                        "either way"
                    )
                ),
                "ticker": ticker,
                "stored_file": stored_file,
                "sessions": entry["sessions"],
                "sealed_bar_count_in_manifest": sealed_count,
                "sealed_bar_count_recounted_from_bytes": sealed_recount,
                "consolidated_feed": recorded_feed,
                "consolidated_bar_count": consolidated_count,
                "consolidated_status": consolidated.status_code,
                "single_venue_feed": MEASURED_SINGLE_VENUE_FEED,
                "single_venue_bar_count": single_count,
                "single_venue_status": single.status_code,
                "single_venue_share_of_consolidated": (
                    single_count / consolidated_count if consolidated_count else None
                ),
                "sealed_matches_consolidated": matches_consolidated,
                "sealed_matches_single_venue": matches_single,
            }
        )
        say(
            f"  {ticker}: sealed={sealed_recount} "
            f"{recorded_feed}={consolidated_count} "
            f"{MEASURED_SINGLE_VENUE_FEED}={single_count} "
            f"-> consolidated={matches_consolidated} single={matches_single}"
        )

    informative = [c for c in checks if c["discriminating"]]
    uninformative = [c for c in checks if not c["discriminating"]]
    all_match_consolidated = all(
        bool(c["sealed_matches_consolidated"]) for c in informative
    )
    none_match_single = not any(
        bool(c["sealed_matches_single_venue"]) for c in informative
    )
    confirmed = bool(informative) and all_match_consolidated and none_match_single

    findings = {
        "kind": "sealed_slice_feed_confirmation",
        "confirmed_at": datetime.now(tz=UTC).isoformat(timespec="seconds"),
        "manifest_recorded_feed": recorded_feed,
        "configured_consolidated_feed": consolidated_feed(),
        "manifest_files_stored": files_stored,
        "manifest_bars_stored": bars_stored,
        "sealed_bar_files_found_on_disk": len(on_disk),
        "checks_n": len(checks),
        "discriminating_checks_n": len(informative),
        "uninformative_checks_n": len(uninformative),
        "uninformative_tickers": [c["ticker"] for c in uninformative],
        "requests_sent": len(checks) * 2,
        "median_single_venue_share_of_consolidated": (
            sorted(
                float(c["single_venue_share_of_consolidated"])  # type: ignore[arg-type]
                for c in informative
            )[len(informative) // 2]
            if informative
            else None
        ),
        "all_sealed_counts_match_the_consolidated_feed": all_match_consolidated,
        "no_sealed_count_matches_the_single_venue_feed": none_match_single,
        "verdict": "CONFIRMED_CONSOLIDATED" if confirmed else "NOT_CONFIRMED",
        "checks": checks,
    }
    write_report("task3b_feed_confirmation.json", findings)
    say(
        f"VERDICT: {findings['verdict']} — n = {len(informative)} discriminating "
        f"chunks of {len(checks)} sampled, {len(checks) * 2} requests. "
        f"{len(uninformative)} uninformative (both feeds served an identical "
        "count) and excluded rather than counted."
    )
    say(
        "NOTE: this is not the re-pull and starts no revision clock. The sealed "
        "slice was not written to; the identical re-pull remains due 2026-09-12."
    )
    return 0 if confirmed else 78


if __name__ == "__main__":
    raise SystemExit(main())
