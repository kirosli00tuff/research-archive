"""Forward outcome checkpoints: day +2 (entry row), +32, +92. Fetch and seal.

The state ledger records every attempt with its call state. A closed
catch-up window writes a loud expired record. Nothing here parses a candle
field: payloads go to the sealed store as bytes, and coverage is counted
elsewhere from timestamps.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, date, datetime, timedelta
from pathlib import Path

from npl.callstate import CallState
from npl.clock import MS_PER_DAY, iso_z, now_utc
from npl.config import CONFIG, Config
from npl.ledger.append_only import AppendOnlyLedger
from npl.paths import FUNDING_DIR, OUTCOMES_DIR, STATE_DIR
from npl.seals import seal_raw
from npl.venue import Venue


@dataclass(frozen=True, slots=True)
class DueCheckpoint:
    coin: str
    dex: str
    listing_day: date
    offset_days: int
    due_day: date


def schedule(listing_day: date, cfg: Config = CONFIG) -> tuple[date, ...]:
    return tuple(listing_day + timedelta(days=o) for o in cfg.checkpoint_offsets_days)


def classify_due(
    coin: str,
    dex: str,
    listing_day: date,
    today: date,
    attempted: set[tuple[str, int]],
    cfg: Config = CONFIG,
) -> tuple[list[DueCheckpoint], list[DueCheckpoint], list[DueCheckpoint]]:
    """(due_now, expired, not_yet_due) for one event. Attempted are skipped."""
    due_now: list[DueCheckpoint] = []
    expired: list[DueCheckpoint] = []
    upcoming: list[DueCheckpoint] = []
    for offset in cfg.checkpoint_offsets_days:
        if (coin, offset) in attempted:
            continue
        due_day = listing_day + timedelta(days=offset)
        record = DueCheckpoint(coin, dex, listing_day, offset, due_day)
        close = due_day + timedelta(days=cfg.catch_up_window_days)
        if due_day <= today <= close:
            due_now.append(record)
        elif today > close:
            expired.append(record)
        else:
            upcoming.append(record)
    return due_now, expired, upcoming


def _day_ms(day: date) -> int:
    return int(datetime(day.year, day.month, day.day, tzinfo=UTC).timestamp() * 1000)


class CheckpointRunner:
    """Fetches one due checkpoint's candles and funding, seals both raw."""

    def __init__(
        self,
        venue: Venue,
        outcomes_root: Path = OUTCOMES_DIR,
        funding_root: Path = FUNDING_DIR,
        state_root: Path = STATE_DIR,
        cfg: Config = CONFIG,
    ) -> None:
        self._venue = venue
        self._outcomes = outcomes_root
        self._funding = funding_root
        self._state = AppendOnlyLedger(state_root / "checkpoints.jsonl")
        self._cfg = cfg

    def attempted(self) -> set[tuple[str, int]]:
        return {
            (str(r["coin"]), int(r["offset_days"]))
            for r in self._state.read().rows
            if r.get("kind") == "attempt" and r.get("state") == CallState.STORED.value
        }

    def record_expired(self, item: DueCheckpoint) -> None:
        """The loud expired record for a closed catch-up window."""
        self._state.append(
            {
                "kind": "expired",
                "coin": item.coin,
                "offset_days": item.offset_days,
                "due_day": item.due_day.isoformat(),
                "state": CallState.EXPIRED.value,
                "at": iso_z(now_utc()),
                "note": "catch-up window closed; the hole is permanent and recorded",
            }
        )

    def run_one(self, item: DueCheckpoint) -> CallState:
        listing_ms = _day_ms(item.listing_day)
        start = listing_ms - MS_PER_DAY
        end = listing_ms + (item.offset_days + 1) * MS_PER_DAY
        stamp = item.due_day.isoformat()

        candle = self._venue.candles(item.coin, "1d", start, end)
        if candle.state is CallState.STORED and candle.body is not None:
            seal_raw(
                self._outcomes / item.coin.replace(":", "_"),
                f"cp{item.offset_days}-candles-{stamp}",
                candle.body,
            )
        funding = self._venue.funding(item.coin, start, end)
        if funding.state is CallState.STORED and funding.body is not None:
            seal_raw(
                self._funding / item.coin.replace(":", "_"),
                f"cp{item.offset_days}-funding-{stamp}",
                funding.body,
            )
        state = candle.state if candle.state is not CallState.STORED else funding.state
        self._state.append(
            {
                "kind": "attempt",
                "coin": item.coin,
                "offset_days": item.offset_days,
                "due_day": stamp,
                "candle_state": candle.state.value,
                "funding_state": funding.state.value,
                "state": state.value,
                "at": iso_z(now_utc()),
            }
        )
        return state
