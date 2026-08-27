"""The funding archive and the retro candle backfill. Sealed raw, resumable.

Funding pages land as raw bytes under data/funding/<coin>/, one sealed file
per page; the cursor derives from the sealed pages' own timestamps through
the blindness reader (times only), so a restart resumes exactly where the
archive ends and can never invent a gap or paper over one. Candle windows
land under data/outcomes/<coin>/. No field is parsed outside the allowed
lists anywhere on this path.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from npl.blindness import funding_rows
from npl.callstate import CallState
from npl.clock import MS_PER_DAY, MS_PER_HOUR
from npl.config import CONFIG, Config
from npl.paths import FUNDING_DIR, OUTCOMES_DIR
from npl.seals import seal_raw
from npl.venue import Venue


def _coin_dir(root: Path, coin: str) -> Path:
    return root / coin.replace(":", "_")


def archive_last_time(coin: str, funding_root: Path = FUNDING_DIR) -> int | None:
    """The newest funding timestamp already sealed for a coin, or None."""
    directory = _coin_dir(funding_root, coin)
    if not directory.exists():
        return None
    newest: int | None = None
    for page in sorted(directory.glob("page-*.raw")):
        rows = funding_rows(page.read_bytes(), entry_ms=None)
        if rows:
            last = rows[-1].time_ms
            newest = last if newest is None or last > newest else newest
    return newest


@dataclass(frozen=True, slots=True)
class ArchiveAdvance:
    coin: str
    pages_fetched: int
    rows_seen: int
    caught_up: bool
    terminal_state: str


def advance_funding_archive(
    venue: Venue,
    coin: str,
    start_ms: int,
    until_ms: int,
    page_budget: int,
    funding_root: Path = FUNDING_DIR,
) -> ArchiveAdvance:
    """Page the archive forward from its cursor (or start_ms) toward until_ms.

    Stops on a served-empty page (caught up: measured absence, no_data), on
    the page budget, or on a refusal — which is recorded and never read as
    end-of-feed.
    """
    cursor = archive_last_time(coin, funding_root)
    next_start = start_ms if cursor is None else cursor + 1
    pages = 0
    rows_seen = 0
    directory = _coin_dir(funding_root, coin)
    existing = len(list(directory.glob("page-*.raw"))) if directory.exists() else 0
    while pages < page_budget and next_start <= until_ms:
        outcome = venue.funding(coin, next_start, until_ms)
        if outcome.state is not CallState.STORED or outcome.body is None:
            return ArchiveAdvance(coin, pages, rows_seen, False, outcome.state.value)
        rows = funding_rows(outcome.body, entry_ms=None)
        if not rows:
            return ArchiveAdvance(coin, pages, rows_seen, True, CallState.NO_DATA.value)
        seal_raw(directory, f"page-{existing + pages:05d}", outcome.body)
        pages += 1
        rows_seen += len(rows)
        next_start = rows[-1].time_ms + 1
    return ArchiveAdvance(coin, pages, rows_seen, next_start > until_ms, CallState.STORED.value)


def backfill_event_candles(
    venue: Venue,
    coin: str,
    listing_open_ms: int,
    outcomes_root: Path = OUTCOMES_DIR,
    cfg: Config = CONFIG,
) -> CallState:
    """The registered retro candle window: entry-1d through entry+91d, sealed raw."""
    entry = listing_open_ms + (cfg.entry_anchor_offset_days + 1) * MS_PER_DAY
    start = entry + cfg.backfill_candle_start_offset_days * MS_PER_DAY
    end = entry + cfg.backfill_candle_end_offset_days * MS_PER_DAY
    directory = _coin_dir(outcomes_root, coin)
    name = f"retro-candles-{entry // MS_PER_DAY}"
    if (directory / f"{name}.raw").exists():
        return CallState.STORED
    outcome = venue.candles(coin, "1d", start, end)
    if outcome.state is CallState.STORED and outcome.body is not None:
        seal_raw(directory, name, outcome.body)
        return CallState.STORED
    return outcome.state


def event_funding_span(listing_open_ms: int, cfg: Config = CONFIG) -> tuple[int, int]:
    """The registered funding window: entry-168h through entry+91d."""
    entry = listing_open_ms + (cfg.entry_anchor_offset_days + 1) * MS_PER_DAY
    return (
        entry + cfg.backfill_funding_start_offset_hours * MS_PER_HOUR,
        entry + cfg.backfill_funding_end_offset_days * MS_PER_DAY,
    )
