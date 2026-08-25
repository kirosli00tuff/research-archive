"""The only module that touches the neighbouring repository.

Opened read-only through a SQLite immutable URI, so a write is impossible at
the driver level rather than by convention. The universe source file is
hashed before and after any read session and the pair is recorded, which is
what lets a later reader prove the port was taken from an unchanged file.

Two paths are permitted and no others. news_experiment.db is never opened.
"""

from __future__ import annotations

import datetime as dt
import hashlib
import sqlite3
from contextlib import contextmanager
from dataclasses import dataclass
from pathlib import Path
from typing import Iterator

from npd.paths import SOURCE_BARS_DB, SOURCE_UNIVERSE_PY

_FORBIDDEN_NAMES = ("news_experiment",)


def _sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def hash_universe_source() -> str:
    """SHA-256 of the ported universe file. Cheap, so it runs before and after."""
    return _sha256(SOURCE_UNIVERSE_PY)


@dataclass(frozen=True, slots=True)
class SourceIntegrity:
    universe_sha256_before: str
    universe_sha256_after: str
    bars_db_size_bytes: int
    checked_at: dt.datetime

    @property
    def unchanged(self) -> bool:
        return self.universe_sha256_before == self.universe_sha256_after


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
    """Exchange sessions in [start, end] as ascending YYYY-MM-DD."""
    rows = con.execute(
        "SELECT date FROM trading_calendar WHERE date >= ? AND date <= ? ORDER BY date",
        (start, end),
    ).fetchall()
    return [r[0] for r in rows]


def stored_membership(con: sqlite3.Connection, rule: str, formation_date: str) -> list[tuple[str, int]]:
    """The source's own membership for one formation. Used to verify the port."""
    rows = con.execute(
        "SELECT symbol, rank FROM universe_membership WHERE rule = ? AND formation_date = ? "
        "ORDER BY rank",
        (rule, formation_date),
    ).fetchall()
    return [(r[0], r[1]) for r in rows]


def formation_dates_available(con: sqlite3.Connection, rule: str) -> list[str]:
    rows = con.execute(
        "SELECT DISTINCT formation_date FROM universe_membership WHERE rule = ? ORDER BY formation_date",
        (rule,),
    ).fetchall()
    return [r[0] for r in rows]


def iter_daily_bars(
    con: sqlite3.Connection, start: str, end: str, chunk: int = 500_000
) -> Iterator[list[tuple[str, str, float, float]]]:
    """Daily bars in [start, end] as (symbol, date, close, volume) chunks.

    Every 1day row in the source carries adjustment 'all' and venue 'alpaca',
    verified at B.0. The filter is stated anyway so a future source holding a
    second convention cannot silently mix two price series.
    """
    cur = con.execute(
        "SELECT symbol, substr(timestamp,1,10) AS d, close, volume FROM bars "
        "WHERE timeframe = '1day' AND adjustment = 'all' AND venue = 'alpaca' "
        "AND substr(timestamp,1,10) >= ? AND substr(timestamp,1,10) <= ? ",
        (start, end),
    )
    while True:
        rows = cur.fetchmany(chunk)
        if not rows:
            return
        yield [(r[0], r[1], float(r[2]), float(r[3])) for r in rows]


def asset_metadata(con: sqlite3.Connection) -> list[tuple[str, str, str]]:
    """(symbol, name, exchange) for fund classification during the port."""
    rows = con.execute("SELECT symbol, name, exchange FROM universe_asset").fetchall()
    return [(r[0], r[1] or "", r[2] or "") for r in rows]
