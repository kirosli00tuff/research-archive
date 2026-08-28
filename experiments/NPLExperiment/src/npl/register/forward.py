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
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from npl.absence import NO_CONTROL_CANDIDATE, Absent
from npl.blindness import FundingRow, funding_rows
from npl.callstate import CallState
from npl.census import CensusRow
from npl.clock import MS_PER_DAY, MS_PER_HOUR, iso_z, now_utc, utc_ms
from npl.config import CONFIG, Config
from npl.controls import Candidate, ControlAssignment, assign_control
from npl.ledger.append_only import AppendOnlyLedger
from npl.paths import FRESH_PLAN, FUNDING_DIR, H2_PAIRS_LEDGER, SPREADS_DIR
from npl.register.fallback import candidate_census_rows, main_dex_candidate_rows
from npl.register.generating_sample import event_id, load_generating_sample
from npl.seals import seal_raw
from npl.spread import record_leg_spread
from npl.venue import Venue


def latest_census(rows: list[CensusRow]) -> dict[tuple[str, str], CensusRow]:
    """Last recorded row per (coin, dex): the current known state."""
    out: dict[tuple[str, str], CensusRow] = {}
    for row in rows:
        out[(row.coin, row.dex)] = row
    return out


def existing_pair_keys(pairs_path: Path = H2_PAIRS_LEDGER) -> set[tuple[str, int]]:
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
    pairs_path: Path = H2_PAIRS_LEDGER,
    plan_path: Path = FRESH_PLAN,
    spread_ledger_path: Path | None = None,
    sample: frozenset[str] | None = None,
    funding_root: Path = FUNDING_DIR,
) -> dict[str, Any]:
    """One forward event's H2 pass: assign, ledger, plan, snapshot.

    Idempotent on the pair ledger: an event already assigned is a no-op.
    The generating sample is refused by construction (a forward birth
    cannot be in it, and the check is still made — the pin is structural,
    not situational).
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

    def build(rows: list[CensusRow]) -> list[Candidate]:
        return [
            Candidate(
                coin=row.coin,
                listing_open_ms=row.first_1d_open_ms or 0,
                rows=_fetch_trail(venue, row.coin, trail_start, entry_ms, funding_root),
            )
            for row in rows
        ]

    same_dex_rows = candidate_census_rows(latest, dex, entry_ms, coin, cfg)
    event_rows = _fetch_trail(venue, coin, trail_start, entry_ms, funding_root)
    result: ControlAssignment | Absent = NO_CONTROL_CANDIDATE
    fallback_n = 0
    if same_dex_rows:
        result = assign_control(
            coin, dex, entry_ms, event_rows, build(same_dex_rows), cfg, pairs_path=pairs_path
        )
    if result == NO_CONTROL_CANDIDATE:
        # Amendment H2-3 Change 1: the same-dex set yielded nothing, so the
        # main-dex universe is consulted — and only now is it fetched.
        fallback_rows = main_dex_candidate_rows(latest, entry_ms, coin, cfg)
        fallback_n = len(fallback_rows)
        if fallback_rows:
            result = assign_control(
                coin,
                dex,
                entry_ms,
                event_rows,
                [],
                cfg,
                pairs_path=pairs_path,
                fallback_candidates=build(fallback_rows),
            )

    out: dict[str, Any] = {
        "event": coin,
        "candidates": len(same_dex_rows),
        "fallback_candidates": fallback_n,
    }
    if isinstance(result, Absent):
        out["state"] = f"unassigned_{result.reason.value}"
        append_fresh_plan_row("event", coin, dex, coin, listing_open_ms, cfg, plan_path)
        return out
    out["state"] = "assigned"
    out["control"] = result.control_coin
    out["pair_type"] = result.pair_type
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
