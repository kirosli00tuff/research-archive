"""Forward pair assignment at the entry anchor (register A.3 Task 2).

On each birth, the pass at the entry anchor assigns the H2 control —
trailing-only, through the pinned matcher — writes the pair row to the
append-only H2 pairs ledger, queues both legs on the fresh plan for the
funding recorder and the mature-window candle seal, and takes the two-leg
l2Book snapshot when the pass lands inside the registered 30-minute
window (a late pass writes a loud expired row; a stale spread is not a
spread). Candidate trailing windows are fetched under the ledger and
sealed raw as trail files; rates are read only at or before the entry
(standing rule 13).

**Amendment H2-5 (2026-09-13) switched this pass to the tiered rule**, so
every new birth pairs on the same logic the 63 existing events were
reassigned under: tier 1 same dex and exact class, tier 2 any dex and exact
class, tier 3 any dex within the equity complex for equity-complex legs
only. Cross-complex is refused at every tier. Rows land in
`data/controls/h2_pairs_v2.jsonl`; the H2-3 ledger is the superseded record
and this pass never writes to it. An event the taxonomy cannot classify, or
whose class admits no elder at any tier, writes its **exclusion** row to the
same ledger — the ledger records what happened to every event, not only the
ones that paired.
"""

from __future__ import annotations

from dataclasses import asdict
from pathlib import Path
from typing import Any

from npl.blindness import FundingRow, funding_rows
from npl.callstate import CallState
from npl.census import CensusRow
from npl.clock import MS_PER_DAY, MS_PER_HOUR, iso_z, now_utc, utc_ms
from npl.config import CONFIG, Config
from npl.ledger.append_only import AppendOnlyLedger
from npl.paths import FRESH_PLAN, FUNDING_DIR, H2_PAIRS_V2_LEDGER, SPREADS_DIR
from npl.register.assetclass import asset_class
from npl.register.fallback import admissible_census_rows
from npl.register.generating_sample import event_id, load_generating_sample
from npl.register.tiered import (
    CandidateRef,
    TieredAssignment,
    assign_control_tiered,
)
from npl.seals import seal_raw
from npl.spread import record_leg_spread
from npl.venue import Venue


def latest_census(rows: list[CensusRow]) -> dict[tuple[str, str], CensusRow]:
    """Last recorded row per (coin, dex): the current known state."""
    out: dict[tuple[str, str], CensusRow] = {}
    for row in rows:
        out[(row.coin, row.dex)] = row
    return out


def existing_pair_keys(pairs_path: Path = H2_PAIRS_V2_LEDGER) -> set[tuple[str, int]]:
    """Every event the ledger has already resolved — paired **or excluded**.

    An excluded event is resolved, not pending: re-running the pass must not
    re-decide it, and the exclusion row is its record.
    """
    return {
        (str(r["event_coin"]), int(r["entry_ms"])) for r in AppendOnlyLedger(pairs_path).read().rows
    }


def append_fresh_plan_row(
    kind: str,
    coin: str,
    dex: str,
    event_coin: str,
    listing_open_ms: int,
    cfg: Config = CONFIG,
    plan_path: Path = FRESH_PLAN,
) -> bool:
    """Queue one leg on the fresh plan, idempotently. Returns True if added."""
    entry = listing_open_ms + (cfg.entry_anchor_offset_days + 1) * MS_PER_DAY
    ledger = AppendOnlyLedger(plan_path)
    for row in ledger.read().rows:
        if (
            row.get("coin") == coin
            and row.get("event_coin") == event_coin
            and int(row.get("listing_open_ms", -1)) == listing_open_ms
        ):
            return False
    ledger.append(
        {
            "kind": kind,
            "coin": coin,
            "dex": dex,
            "event_coin": event_coin,
            "listing_open_ms": listing_open_ms,
            "span_start_ms": entry + cfg.backfill_funding_start_offset_hours * MS_PER_HOUR,
            "span_end_ms": entry + cfg.backfill_funding_end_offset_days * MS_PER_DAY,
        }
    )
    return True


def _fetch_trail(
    venue: Venue, coin: str, start_ms: int, end_ms: int, funding_root: Path = FUNDING_DIR
) -> tuple[FundingRow, ...]:
    """The trailing window (start, end], sealed raw as trail files, gated.

    Existing trail pages for the same window are read from disk rather than
    refetched; every returned row is stamped at or before end_ms.
    """
    directory = funding_root / coin.replace(":", "_")
    name = f"trail-{start_ms // MS_PER_DAY}-{end_ms // MS_PER_DAY}"
    rows: list[FundingRow] = []
    existing = sorted(directory.glob(f"{name}-p*.raw")) if directory.exists() else []
    if existing:
        for page in existing:
            rows.extend(
                r for r in funding_rows(page.read_bytes(), entry_ms=end_ms) if r.time_ms <= end_ms
            )
        return tuple(sorted(rows, key=lambda r: r.time_ms))
    # A trailing window is at most a handful of 500-row pages; the cap is a
    # loud guard against a pathological feed, never an end-of-feed signal.
    max_pages = 16
    cursor, page_i = start_ms, 0
    while page_i < max_pages:
        outcome = venue.funding(coin, cursor, end_ms)
        if outcome.state is not CallState.STORED or outcome.body is None:
            break  # recorded by the caller's states; never end-of-feed
        page_rows = funding_rows(outcome.body, entry_ms=end_ms)
        if not page_rows:
            break
        seal_raw(directory, f"{name}-p{page_i}", outcome.body)
        rows.extend(r for r in page_rows if r.time_ms <= end_ms)
        page_i += 1
        cursor = page_rows[-1].time_ms + 1
        if cursor > end_ms:
            break
    return tuple(sorted(rows, key=lambda r: r.time_ms))


def forward_pair_pass(
    venue: Venue,
    coin: str,
    dex: str,
    entry_ms: int,
    census_rows: list[CensusRow],
    cfg: Config = CONFIG,
    pairs_path: Path = H2_PAIRS_V2_LEDGER,
    plan_path: Path = FRESH_PLAN,
    spread_ledger_path: Path | None = None,
    sample: frozenset[str] | None = None,
    funding_root: Path = FUNDING_DIR,
) -> dict[str, Any]:
    """One forward event's H2 pass: classify, assign by tier, ledger, plan, snapshot.

    Idempotent on the pair ledger: an event already resolved — paired or
    excluded — is a no-op. The generating sample is refused by construction
    (a forward birth cannot be in it, and the check is still made — the pin
    is structural, not situational).
    """
    listing_open_ms = entry_ms - (cfg.entry_anchor_offset_days + 1) * MS_PER_DAY
    if sample is None:
        sample = load_generating_sample()
    if event_id(coin, dex, listing_open_ms) in sample:
        raise RuntimeError(f"forward pass asked for generating-sample event {coin!r}; refused")
    if (coin, entry_ms) in existing_pair_keys(pairs_path):
        return {"event": coin, "state": "already_assigned"}

    latest = latest_census(census_rows)
    trail_start = entry_ms - cfg.control_trailing_window_hours * MS_PER_HOUR

    # Candidate refs are census-level: identity, dex, class, listing date.
    # No trailing window is fetched for a tier the selector never reaches.
    refs: list[CandidateRef] = []
    for row in admissible_census_rows(latest, entry_ms, coin, cfg):
        candidate_class = asset_class(row.coin, row.dex)
        if candidate_class is None:
            continue  # unclassifiable instruments are never candidates
        refs.append(
            CandidateRef(
                coin=row.coin,
                dex=row.dex,
                asset_class=candidate_class,
                listing_open_ms=row.first_1d_open_ms or 0,
            )
        )

    event_class = asset_class(coin, dex)
    event_rows: tuple[FundingRow, ...] = (
        _fetch_trail(venue, coin, trail_start, entry_ms, funding_root) if event_class else ()
    )
    result = assign_control_tiered(
        coin,
        dex,
        entry_ms,
        event_rows,
        refs,
        lambda ref: _fetch_trail(venue, ref.coin, trail_start, entry_ms, funding_root),
        cfg,
        pairs_path=pairs_path,
    )

    out: dict[str, Any] = {
        "event": coin,
        "event_class": event_class,
        "candidates": len(refs),
    }
    if not isinstance(result, TieredAssignment):
        # The exclusion is the event's record, written to the same ledger.
        AppendOnlyLedger(pairs_path).append(asdict(result))
        out["state"] = result.state
        out["reason"] = result.reason
        out["tier_pool_sizes"] = list(result.tier_pool_sizes)
        append_fresh_plan_row("event", coin, dex, coin, listing_open_ms, cfg, plan_path)
        return out
    out["state"] = "assigned"
    out["control"] = result.control_coin
    out["tier"] = result.tier
    out["class_pair"] = result.class_pair
    out["control_dex"] = result.control_dex
    append_fresh_plan_row("event", coin, dex, coin, listing_open_ms, cfg, plan_path)
    append_fresh_plan_row(
        "control", result.control_coin, result.control_dex, coin, listing_open_ms, cfg, plan_path
    )

    # The two-leg snapshot, inside the registered 30-minute window only.
    age_minutes = (utc_ms(now_utc()) - entry_ms) / 60_000.0
    spread_target = (
        spread_ledger_path if spread_ledger_path is not None else SPREADS_DIR / "pair_spreads.jsonl"
    )
    if 0 <= age_minutes <= cfg.spread_snapshot_window_minutes:
        out["spread_young"] = record_leg_spread(
            venue, coin, hypothesis="H2", role="event", event_coin=coin, ledger_path=spread_target
        ).value
        out["spread_elder"] = record_leg_spread(
            venue,
            result.control_coin,
            hypothesis="H2",
            role="control",
            event_coin=coin,
            ledger_path=spread_target,
        ).value
    else:
        AppendOnlyLedger(spread_target).append(
            {
                "kind": "expired",
                "hypothesis": "H2",
                "event_coin": coin,
                "entry_ms": entry_ms,
                "at": iso_z(now_utc()),
                "state": CallState.EXPIRED.value,
                "note": (
                    f"two-leg window closed {age_minutes:.0f} minutes after entry; never backfilled"
                ),
            }
        )
        out["spread"] = "expired"
    return out
