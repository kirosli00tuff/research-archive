"""The main-dex fallback control (Amendment H2-3 Change 1).

Two things live here, both shared by the one-shot backfill of the 24
previously unpairable events and by the forward pass that runs at every
new birth, so both pair on identical logic:

- `candidate_census_rows` — the census-date filter: instruments on a given
  dex, listed at least the registered 180 days before the entry, still
  serving history across the trailing window. Dates and identities only.
- the sealed-trail pair: `seal_trail_window` fetches and seals raw bytes
  under the request ledger; `read_sealed_trail` parses those bytes back
  **through the blindness gate at the referencing event's own entry**, so
  a rate stamped after that entry is `Absent(blindness_gated)` and never
  reaches the matcher. One wide sealed window can therefore serve several
  entries without any of them seeing a rate from its own future.
"""

from __future__ import annotations

from pathlib import Path

from npl.blindness import FundingRow, funding_rows
from npl.callstate import CallState
from npl.census import CensusRow
from npl.clock import MS_PER_DAY, MS_PER_HOUR
from npl.config import CONFIG, Config
from npl.controls import MAIN_DEX
from npl.paths import FUNDING_DIR
from npl.seals import seal_raw
from npl.venue import Venue

# A trailing window is a handful of 500-row pages; the cap is a loud guard
# against a pathological feed, never an end-of-feed signal (ADR-021).
MAX_TRAIL_PAGES = 16


def candidate_census_rows(
    latest: dict[tuple[str, str], CensusRow],
    dex: str,
    entry_ms: int,
    exclude_coin: str,
    cfg: Config = CONFIG,
) -> list[CensusRow]:
    """Section 6 candidates on one dex by census dates. No value is read.

    The age condition (listed at least `control_min_age_days` before the
    entry) and the still-serving condition (last served close at or after
    the trailing window's start) are date arithmetic. The coverage
    condition is enforced at assignment, from funding row timestamps.
    """
    cutoff = entry_ms - cfg.control_min_age_days * MS_PER_DAY
    trail_start = entry_ms - cfg.control_trailing_window_hours * MS_PER_HOUR
    out: list[CensusRow] = []
    for (coin, candidate_dex), row in latest.items():
        if candidate_dex != dex or coin == exclude_coin:
            continue
        if row.first_1d_open_ms is None or row.first_1d_open_ms > cutoff:
            continue
        last = row.last_1d_close_ms or row.first_1d_open_ms
        if last < trail_start:
            continue
        out.append(row)
    return sorted(out, key=lambda r: (r.first_1d_open_ms or 0, r.coin))


def main_dex_candidate_rows(
    latest: dict[tuple[str, str], CensusRow],
    entry_ms: int,
    exclude_coin: str,
    cfg: Config = CONFIG,
) -> list[CensusRow]:
    """The registered fallback universe: the same conditions, on the main dex."""
    return candidate_census_rows(latest, MAIN_DEX, entry_ms, exclude_coin, cfg)


def _coin_dir(funding_root: Path, coin: str) -> Path:
    return funding_root / coin.replace(":", "_")


def trail_stem(start_ms: int, end_ms: int) -> str:
    """The sealed trail window's name: whole days, as the archive names pages."""
    return f"trail-{start_ms // MS_PER_DAY}-{end_ms // MS_PER_DAY}"


def seal_trail_window(
    venue: Venue,
    coin: str,
    start_ms: int,
    end_ms: int,
    funding_root: Path = FUNDING_DIR,
    max_pages: int = MAX_TRAIL_PAGES,
) -> tuple[int, str]:
    """Fetch (start, end] and seal it raw. Returns (pages sealed, state).

    Nothing is parsed for a value here: pages are sealed as bytes and the
    cursor advances on row timestamps alone. An already-sealed window is a
    no-op — the raw bytes on disk are the record.
    """
    directory = _coin_dir(funding_root, coin)
    stem = trail_stem(start_ms, end_ms)
    if directory.exists() and any(directory.glob(f"{stem}-p*.raw")):
        return 0, CallState.STORED.value
    cursor, pages = start_ms, 0
    while pages < max_pages:
        outcome = venue.funding(coin, cursor, end_ms)
        if outcome.state is not CallState.STORED or outcome.body is None:
            return pages, outcome.state.value
        rows = funding_rows(outcome.body, entry_ms=None)
        if not rows:
            return pages, CallState.NO_DATA.value if pages == 0 else CallState.STORED.value
        seal_raw(directory, f"{stem}-p{pages}", outcome.body)
        pages += 1
        cursor = rows[-1].time_ms + 1
        if cursor > end_ms:
            break
    return pages, CallState.STORED.value


def read_sealed_trail(
    coin: str,
    entry_ms: int,
    window_start_ms: int,
    funding_root: Path = FUNDING_DIR,
) -> tuple[FundingRow, ...]:
    """Every sealed trail row in (window_start, entry], gated at that entry.

    Each sealed page is parsed with `entry_ms` as the blindness gate, so a
    row stamped after this event's entry carries `Absent(blindness_gated)`
    and is then dropped by the window filter as well. Rows are deduplicated
    by timestamp: sealed windows may overlap, and a double-counted hour
    would bias the trailing mean.
    """
    directory = _coin_dir(funding_root, coin)
    if not directory.exists():
        return ()
    by_time: dict[int, FundingRow] = {}
    for page in sorted(directory.glob("trail-*.raw")):
        for row in funding_rows(page.read_bytes(), entry_ms=entry_ms):
            if window_start_ms < row.time_ms <= entry_ms:
                by_time.setdefault(row.time_ms, row)
    return tuple(by_time[t] for t in sorted(by_time))
