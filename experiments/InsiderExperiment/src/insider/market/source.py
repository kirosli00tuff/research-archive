"""The only module that touches the neighbouring repository.

Two paths are permitted and no others. analysis_bars.db is opened through a
SQLite immutable read-only URI, so a write is impossible at the driver level
rather than by convention. Both source files are hashed before and after any
read session and the pair is recorded, which is what lets a later reader prove
the copy was taken from an unchanged file.

news_experiment.db is never opened. The news-drift collection runs nightly at
22:30 UTC and must not be disturbed.
"""

from __future__ import annotations

import datetime as dt
import hashlib
import sqlite3
from collections.abc import Iterator
from contextlib import contextmanager
from dataclasses import dataclass
from pathlib import Path

from insider.paths import SOURCE_BARS_DB, SOURCE_UNIVERSE_PY

_FORBIDDEN_NAMES = ("news_experiment",)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 22), b""):
            digest.update(chunk)
    return digest.hexdigest()


@dataclass(frozen=True, slots=True)
class SourceIntegrity:
    bars_sha256_before: str
    bars_sha256_after: str
    universe_sha256_before: str
    universe_sha256_after: str
    bars_size_bytes: int
    checked_at: str

    @property
    def unchanged(self) -> bool:
        return (
            self.bars_sha256_before == self.bars_sha256_after
            and self.universe_sha256_before == self.universe_sha256_after
        )


def hash_sources() -> tuple[str, str]:
    """SHA-256 of both permitted source files, bars first."""
    return sha256(SOURCE_BARS_DB), sha256(SOURCE_UNIVERSE_PY)


def integrity(before: tuple[str, str], after: tuple[str, str]) -> SourceIntegrity:
    return SourceIntegrity(
        bars_sha256_before=before[0],
        bars_sha256_after=after[0],
        universe_sha256_before=before[1],
        universe_sha256_after=after[1],
        bars_size_bytes=SOURCE_BARS_DB.stat().st_size,
        checked_at=dt.datetime.now(dt.UTC).isoformat(timespec="seconds"),
    )


@contextmanager
def read_only_bars() -> Iterator[sqlite3.Connection]:
    """Open the source bar store read-only and immutable.

    immutable=1 tells SQLite the file will not change while open, which also
    stops it creating journal or WAL files beside a database another process
    owns. mode=ro makes any write attempt raise.
    """
    for bad in _FORBIDDEN_NAMES:
        if bad in SOURCE_BARS_DB.name:
            raise PermissionError(f"refusing to open {SOURCE_BARS_DB}")
    if not SOURCE_BARS_DB.exists():
        raise FileNotFoundError(f"source bar store missing: {SOURCE_BARS_DB}")
    con = sqlite3.connect(f"file:{SOURCE_BARS_DB}?mode=ro&immutable=1", uri=True)
    try:
        yield con
    finally:
        con.close()


def sessions(con: sqlite3.Connection, start: str, end: str) -> list[str]:
    rows = con.execute(
        "SELECT date FROM trading_calendar WHERE date >= ? AND date <= ? ORDER BY date",
        (start, end),
    ).fetchall()
    return [r[0] for r in rows]


def stored_membership(con: sqlite3.Connection, rule: str, formation_date: str) -> list[tuple[str, int, float, float, int]]:
    rows = con.execute(
        "SELECT symbol, rank, median_dollar_volume, median_close, window_bars "
        "FROM universe_membership WHERE rule = ? AND formation_date = ? ORDER BY rank",
        (rule, formation_date),
    ).fetchall()
    return [(r[0], int(r[1]), float(r[2]), float(r[3]), int(r[4])) for r in rows]


def formation_dates_available(con: sqlite3.Connection, rule: str) -> list[str]:
    rows = con.execute(
        "SELECT DISTINCT formation_date FROM universe_membership WHERE rule = ? "
        "ORDER BY formation_date",
        (rule,),
    ).fetchall()
    return [r[0] for r in rows]


def daily_bars_for(
    con: sqlite3.Connection, symbols: list[str], start: str, end: str, chunk: int = 400
) -> Iterator[tuple[str, str, float, float]]:
    """Daily bars for named symbols in [start, end] as (symbol, date, close, volume).

    Every 1day row in the source carries adjustment 'all' and venue 'alpaca'.
    The filter is stated anyway so a future source holding a second convention
    cannot silently mix two price series.
    """
    for i in range(0, len(symbols), chunk):
        batch = symbols[i : i + chunk]
        placeholders = ",".join("?" * len(batch))
        cursor = con.execute(
            f"SELECT symbol, substr(timestamp,1,10), close, volume FROM bars "  # noqa: S608
            f"WHERE timeframe = '1day' AND adjustment = 'all' AND venue = 'alpaca' "
            f"AND symbol IN ({placeholders}) "
            f"AND substr(timestamp,1,10) >= ? AND substr(timestamp,1,10) <= ?",
            (*batch, start, end),
        )
        while True:
            rows = cursor.fetchmany(200_000)
            if not rows:
                break
            for row in rows:
                yield row[0], row[1], float(row[2]), float(row[3])


def window_bars_all_symbols(
    con: sqlite3.Connection, start: str, end: str
) -> Iterator[tuple[str, str, float, float]]:
    """Every symbol's daily bars in [start, end]. Used only by the port check."""
    cursor = con.execute(
        "SELECT symbol, substr(timestamp,1,10), close, volume FROM bars "
        "WHERE timeframe = '1day' AND adjustment = 'all' AND venue = 'alpaca' "
        "AND substr(timestamp,1,10) >= ? AND substr(timestamp,1,10) <= ?",
        (start, end),
    )
    while True:
        rows = cursor.fetchmany(200_000)
        if not rows:
            return
        for row in rows:
            yield row[0], row[1], float(row[2]), float(row[3])


def asset_metadata(con: sqlite3.Connection) -> list[tuple[str, str, str]]:
    rows = con.execute("SELECT symbol, name, exchange FROM universe_asset").fetchall()
    return [(r[0], r[1] or "", r[2] or "") for r in rows]
