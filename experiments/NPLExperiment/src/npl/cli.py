"""Entry points: verify, watch, daily. Scheduling belongs to systemd.

watch: one poll pass over the metas, plus the entry-anchor spread snapshots
whose registered window is open right now.
daily: seal yesterday's births manifest first (a failed attestation stops
the pass loudly before anything else runs), then checkpoints, then the
funding archive and retro backfill catch-up, all under the ledger and a
soft daily budget that leaves headroom under the registered cap.
"""

from __future__ import annotations

import sys
from datetime import UTC, datetime, timedelta

from npl.archive import advance_funding_archive, backfill_event_candles
from npl.census import CensusLedger
from npl.checkpoints import CheckpointRunner, classify_due
from npl.clock import now_utc, utc_ms
from npl.config import CONFIG
from npl.http import InfoClient
from npl.ledger.append_only import AppendOnlyLedger
from npl.ledger.requests import RequestLedger
from npl.pacing import OPERATING_PACING_S
from npl.paths import BIRTHS_DIR, STATE_DIR
from npl.spread import record_entry_spread
from npl.venue import Venue
from npl.watcher import Watcher

DAILY_SOFT_BUDGET = 15_000  # requests; leaves 5,000 headroom under the cap
RETRO_PLAN = STATE_DIR / "retro_plan.jsonl"


def _venue() -> tuple[Venue, RequestLedger]:
    ledger = RequestLedger()
    return Venue(InfoClient(ledger, pacing_s=OPERATING_PACING_S)), ledger


def _forward_entry_coins(now: datetime) -> list[tuple[str, int]]:
    """Forward events whose entry anchor (00:00Z today) is within the window."""
    out: list[tuple[str, int]] = []
    if not BIRTHS_DIR.exists():
        return out
    target_day = now.date() - timedelta(days=CONFIG.entry_anchor_offset_days + 1)
    manifest = BIRTHS_DIR / f"births-{target_day.isoformat()}.jsonl"
    if not manifest.exists():
        return out
    entry_ms = int(datetime(now.year, now.month, now.day, tzinfo=UTC).timestamp() * 1000)
    for row in AppendOnlyLedger(manifest).read().rows:
        if row.get("kind") == "birth" and not row.get("is_delisted", False):
            out.append((str(row["coin"]), entry_ms))
    return out


def cmd_verify() -> int:
    venue, ledger = _venue()
    outcome = venue.meta()
    print(f"meta: {outcome.state.value} http={outcome.http_status}")
    print(f"ledger today: {ledger.spent_on(now_utc().date().isoformat())}")
    return 0 if outcome.state.value == "stored" else 1


def cmd_watch() -> int:
    venue, _ = _venue()
    watcher = Watcher(venue, census=CensusLedger())
    report = watcher.poll_once()
    print(
        f"watch: dexs={report.dexs_polled} failed={report.dexs_failed} "
        f"instruments={report.instruments_seen} births={report.new_births}"
    )
    now = now_utc()
    for coin, entry_ms in _forward_entry_coins(now):
        state = record_entry_spread(venue, coin, entry_ms)
        print(f"spread {coin}: {state.value}")
    return 0


def cmd_daily() -> int:
    venue, ledger = _venue()
    watcher = Watcher(venue, census=CensusLedger())
    sealed = watcher.seal_yesterday()
    print(f"seal yesterday: {'none (no manifest)' if sealed is None else sealed[:12]}")

    today = now_utc().date()
    runner = CheckpointRunner(venue)
    attempted = runner.attempted()
    if BIRTHS_DIR.exists():
        for manifest in sorted(BIRTHS_DIR.glob("births-*.jsonl")):
            day = (
                datetime.strptime(manifest.stem.removeprefix("births-"), "%Y-%m-%d")
                .replace(tzinfo=UTC)
                .date()
            )
            for row in AppendOnlyLedger(manifest).read().rows:
                if row.get("kind") != "birth":
                    continue
                due, expired, _ = classify_due(
                    str(row["coin"]), str(row["dex"]), day, today, attempted
                )
                for item in expired:
                    runner.record_expired(item)
                for item in due:
                    state = runner.run_one(item)
                    print(f"checkpoint {item.coin}+{item.offset_days}: {state.value}")

    spent = ledger.spent_on(today.isoformat())
    if RETRO_PLAN.exists():
        now_ms = utc_ms(now_utc())
        for row in AppendOnlyLedger(RETRO_PLAN).read().rows:
            if ledger.spent_on(today.isoformat()) >= DAILY_SOFT_BUDGET:
                print("daily soft budget reached; the plan resumes tomorrow")
                break
            coin = str(row["coin"])
            listing = int(row["listing_open_ms"])
            if row.get("kind") == "event":
                state = backfill_event_candles(venue, coin, listing)
                print(f"backfill candles {coin}: {state.value}")
            span_start = int(row["span_start_ms"])
            span_end = min(int(row["span_end_ms"]), now_ms)
            advance = advance_funding_archive(venue, coin, span_start, span_end, page_budget=60)
            if advance.pages_fetched or not advance.caught_up:
                print(
                    f"funding {coin}: +{advance.pages_fetched} pages "
                    f"({advance.terminal_state}, caught_up={advance.caught_up})"
                )
    print(f"daily done; ledger today: {ledger.spent_on(today.isoformat())} (was {spent})")
    return 0


def main(argv: list[str]) -> int:
    if len(argv) != 2 or argv[1] not in {"verify", "watch", "daily"}:
        print("usage: python -m npl.cli {verify|watch|daily}", file=sys.stderr)
        return 2
    if argv[1] == "verify":
        return cmd_verify()
    if argv[1] == "watch":
        return cmd_watch()
    return cmd_daily()


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
