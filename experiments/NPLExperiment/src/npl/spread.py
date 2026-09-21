"""The entry-anchor spread snapshot. Descriptive cost input only.

This is the single module permitted to read the l2Book px and sz fields
(Section 5; the repo-wide guard allows them here and nowhere else). One
fetch within the registered window after the entry anchor close; a missed
window writes a loud expired record and is never backfilled.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path

from npl.api import EP_L2_BOOK, l2_book_body
from npl.callstate import CallState
from npl.clock import iso_z, ms_to_utc, now_utc, utc_ms
from npl.config import CONFIG, Config
from npl.ledger.append_only import AppendOnlyLedger
from npl.paths import SPREADS_DIR
from npl.venue import Venue

TOP_LEVELS = 5


@dataclass(frozen=True, slots=True)
class SpreadSnapshot:
    coin: str
    entry_ms: int
    fetched_at: str
    bid_px: float
    ask_px: float
    touch_spread_bp: float
    bid_depth5_base: float
    ask_depth5_base: float
    bid_depth5_notional: float
    ask_depth5_notional: float


def parse_l2_snapshot(coin: str, entry_ms: int, body: bytes, fetched_at: str) -> SpreadSnapshot:
    parsed = json.loads(body)
    levels = parsed["levels"]
    bids, asks = levels[0], levels[1]
    if not bids or not asks:
        raise ValueError(f"{coin}: an empty book side is recorded as a refusal, not a spread")
    bid_px = float(bids[0]["px"])
    ask_px = float(asks[0]["px"])
    mid = (bid_px + ask_px) / 2.0
    return SpreadSnapshot(
        coin=coin,
        entry_ms=entry_ms,
        fetched_at=fetched_at,
        bid_px=bid_px,
        ask_px=ask_px,
        touch_spread_bp=(ask_px - bid_px) / mid * 1e4,
        bid_depth5_base=sum(float(level["sz"]) for level in bids[:TOP_LEVELS]),
        ask_depth5_base=sum(float(level["sz"]) for level in asks[:TOP_LEVELS]),
        bid_depth5_notional=sum(
            float(level["sz"]) * float(level["px"]) for level in bids[:TOP_LEVELS]
        ),
        ask_depth5_notional=sum(
            float(level["sz"]) * float(level["px"]) for level in asks[:TOP_LEVELS]
        ),
    )


def record_leg_spread(
    venue: Venue,
    coin: str,
    *,
    hypothesis: str,
    role: str,
    event_coin: str,
    ledger_path: Path = SPREADS_DIR / "pair_spreads.jsonl",
) -> CallState:
    """One descriptive touch-state fetch for a pair leg (register A.1/A.3).

    Unlike the entry-anchor snapshot, this carries no registered timing
    window: it is a descriptive cost input for the pair model, stamped with
    its own fetch time, and never enters an outcome. A refusal or empty
    book is recorded loudly with its state.
    """
    store = AppendOnlyLedger(ledger_path)
    at = now_utc()
    outcome = venue.request(l2_book_body(coin), EP_L2_BOOK)
    if outcome.state is not CallState.STORED or outcome.body is None:
        store.append(
            {
                "kind": "error",
                "hypothesis": hypothesis,
                "coin": coin,
                "role": role,
                "event_coin": event_coin,
                "at": iso_z(at),
                "state": outcome.state.value,
            }
        )
        return outcome.state
    try:
        snapshot = parse_l2_snapshot(coin, 0, outcome.body, iso_z(at))
    except ValueError as exc:
        store.append(
            {
                "kind": "error",
                "hypothesis": hypothesis,
                "coin": coin,
                "role": role,
                "event_coin": event_coin,
                "at": iso_z(at),
                "state": CallState.NO_DATA.value,
                "note": str(exc),
            }
        )
        return CallState.NO_DATA
    row: dict[str, object] = {"kind": "leg_spread", "hypothesis": hypothesis, "role": role}
    row.update({"event_coin": event_coin, "state": CallState.STORED.value})
    row.update(asdict(snapshot))
    store.append(row)
    return CallState.STORED


def record_entry_spread(
    venue: Venue,
    coin: str,
    entry_ms: int,
    ledger_path: Path = SPREADS_DIR / "spreads.jsonl",
    cfg: Config = CONFIG,
) -> CallState:
    """One l2Book fetch within the registered post-entry window."""
    store = AppendOnlyLedger(ledger_path)
    at = now_utc()
    age_minutes = (utc_ms(at) - entry_ms) / 60_000.0
    if age_minutes < 0:
        raise ValueError(f"{coin}: the entry anchor {ms_to_utc(entry_ms)} is in the future")
    if age_minutes > cfg.spread_snapshot_window_minutes:
        store.append(
            {
                "kind": "expired",
                "coin": coin,
                "entry_ms": entry_ms,
                "at": iso_z(at),
                "state": CallState.EXPIRED.value,
                "note": (
                    f"the {cfg.spread_snapshot_window_minutes}-minute window closed "
                    f"{age_minutes:.0f} minutes after entry; never backfilled"
                ),
            }
        )
        return CallState.EXPIRED
    outcome = venue.request(l2_book_body(coin), EP_L2_BOOK)
    if outcome.state is not CallState.STORED or outcome.body is None:
        store.append(
            {
                "kind": "error",
                "coin": coin,
                "entry_ms": entry_ms,
                "at": iso_z(at),
                "state": outcome.state.value,
            }
        )
        return outcome.state
    snapshot = parse_l2_snapshot(coin, entry_ms, outcome.body, iso_z(at))
    store.append({"kind": "spread", **asdict(snapshot)})
    return CallState.STORED
