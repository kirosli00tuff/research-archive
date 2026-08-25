"""One read-only pass over the source store into the experiment's own store.

The source is opened immutable and read-only, hashed on the file side before
and after, and touched exactly once per build. Everything downstream reads the
local copy, so a rebuild never re-reads a database another system owns.
"""

from __future__ import annotations

import datetime as dt
import sqlite3
from dataclasses import dataclass

from npd.data import source
from npd.data.store import set_meta

# Earliest bar the pipeline needs. The 12-1 momentum baseline looks back about
# 252 sessions, and the logistic fit sample starts at 2022-01-03, so the extract
# reaches a full year further back than the fit sample does.
EXTRACT_START = "2021-01-01"


@dataclass(frozen=True, slots=True)
class ExtractReport:
    sessions_written: int
    bars_written: int
    symbols: int
    first_date: str
    last_date: str
    universe_sha256_before: str
    universe_sha256_after: str
    seconds: float


def run(
    dst: sqlite3.Connection, *, start: str = EXTRACT_START, end: str = "2026-07-24"
) -> ExtractReport:
    """Copy the session calendar and daily bars into the local store."""
    t0 = dt.datetime.now(dt.UTC)
    sha_before = source.hash_universe_source()

    with source.read_only_bars() as src:
        cal = source.sessions(src, "2016-01-01", "2027-12-31")
        dst.execute("DELETE FROM session")
        dst.executemany(
            "INSERT INTO session(date, idx) VALUES(?, ?)",
            [(d, i) for i, d in enumerate(cal)],
        )

        dst.execute("DELETE FROM bar")
        dst.commit()
        dst.execute("PRAGMA synchronous=OFF")
        written = 0
        for chunk in source.iter_daily_bars(src, start, end):
            dst.executemany(
                "INSERT OR REPLACE INTO bar(symbol, date, close, volume) VALUES(?,?,?,?)",
                chunk,
            )
            written += len(chunk)
        dst.commit()

        assets = source.asset_metadata(src)

    dst.execute("DELETE FROM meta WHERE key LIKE 'asset:%'")
    dst.executemany(
        "INSERT OR REPLACE INTO meta(key, value) VALUES(?, ?)",
        [(f"asset:{sym}", f"{name}\t{exch}") for sym, name, exch in assets],
    )

    sha_after = source.hash_universe_source()
    row = dst.execute("SELECT COUNT(DISTINCT symbol), MIN(date), MAX(date) FROM bar").fetchone()

    set_meta(dst, "extract.start", start)
    set_meta(dst, "extract.end", end)
    set_meta(dst, "extract.universe_sha256_before", sha_before)
    set_meta(dst, "extract.universe_sha256_after", sha_after)
    set_meta(dst, "extract.completed_at", dt.datetime.now(dt.UTC).isoformat())
    dst.commit()

    if sha_before != sha_after:
        raise RuntimeError(
            "the ported universe source changed during the extract. "
            f"before {sha_before} after {sha_after}"
        )

    return ExtractReport(
        sessions_written=len(cal),
        bars_written=written,
        symbols=int(row[0]),
        first_date=str(row[1]),
        last_date=str(row[2]),
        universe_sha256_before=sha_before,
        universe_sha256_after=sha_after,
        seconds=(dt.datetime.now(dt.UTC) - t0).total_seconds(),
    )


def asset_lookup(dst: sqlite3.Connection) -> dict[str, tuple[str, str]]:
    """symbol to (name, exchange), as copied from the source asset list."""
    out: dict[str, tuple[str, str]] = {}
    for key, value in dst.execute("SELECT key, value FROM meta WHERE key LIKE 'asset:%'"):
        name, _, exch = str(value).partition("\t")
        out[str(key)[6:]] = (name, exch)
    return out
