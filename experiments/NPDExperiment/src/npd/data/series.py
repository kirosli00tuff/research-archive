"""Load the local bar extract once into aligned arrays.

Every downstream stage reads from here rather than re-querying. A formation
window, a feature block, and a forward return all address the same session
index, so alignment is decided once and cannot drift between stages.

Missing bars stay missing. The dense view uses None, never a carried value.
"""

from __future__ import annotations

import sqlite3
from dataclasses import dataclass, field

import numpy as np

from npd.data.features import Series


@dataclass(slots=True)
class SeriesStore:
    """Sparse per-symbol arrays plus a dense view built on demand."""

    sessions: list[str]
    index_of: dict[str, int] = field(default_factory=dict)
    idx: dict[str, np.ndarray] = field(default_factory=dict)
    close: dict[str, np.ndarray] = field(default_factory=dict)
    volume: dict[str, np.ndarray] = field(default_factory=dict)
    _dense_cache: dict[str, Series] = field(default_factory=dict)

    @property
    def symbols(self) -> list[str]:
        return list(self.idx)

    def window(self, symbol: str, start_i: int, end_i: int) -> tuple[np.ndarray, np.ndarray]:
        """Closes and volumes for the sessions in [start_i, end_i] the symbol traded."""
        positions = self.idx.get(symbol)
        if positions is None:
            empty = np.empty(0, dtype=float)
            return empty, empty
        lo = int(np.searchsorted(positions, start_i, side="left"))
        hi = int(np.searchsorted(positions, end_i, side="right"))
        return self.close[symbol][lo:hi], self.volume[symbol][lo:hi]

    def session_indices(self, symbol: str, start_i: int, end_i: int) -> np.ndarray:
        positions = self.idx.get(symbol)
        if positions is None:
            return np.empty(0, dtype=np.int32)
        lo = int(np.searchsorted(positions, start_i, side="left"))
        hi = int(np.searchsorted(positions, end_i, side="right"))
        return positions[lo:hi]

    def last_index_before(self, symbol: str, start_i: int) -> int | None:
        """Session index of the symbol's last bar strictly before start_i."""
        positions = self.idx.get(symbol)
        if positions is None:
            return None
        lo = int(np.searchsorted(positions, start_i, side="left"))
        return None if lo == 0 else int(positions[lo - 1])

    def dense(self, symbol: str) -> Series:
        """Close and volume over the whole calendar, with None where no bar exists."""
        cached = self._dense_cache.get(symbol)
        if cached is not None:
            return cached
        n = len(self.sessions)
        closes: list[float | None] = [None] * n
        vols: list[float | None] = [None] * n
        positions = self.idx.get(symbol)
        if positions is not None:
            c = self.close[symbol]
            v = self.volume[symbol]
            for j, p in enumerate(positions):
                closes[int(p)] = float(c[j])
                vols[int(p)] = float(v[j])
        built = Series(symbol=symbol, close=tuple(closes), volume=tuple(vols))
        self._dense_cache[symbol] = built
        return built

    def drop_dense_cache(self) -> None:
        self._dense_cache.clear()


def load(con: sqlite3.Connection, sessions: list[str]) -> SeriesStore:
    """Read every bar into per-symbol arrays, ascending by symbol then date."""
    store = SeriesStore(sessions=sessions, index_of={d: i for i, d in enumerate(sessions)})
    index_of = store.index_of

    cur_symbol: str | None = None
    idx_buf: list[int] = []
    close_buf: list[float] = []
    vol_buf: list[float] = []

    def flush() -> None:
        if cur_symbol is None or not idx_buf:
            return
        store.idx[cur_symbol] = np.asarray(idx_buf, dtype=np.int32)
        store.close[cur_symbol] = np.asarray(close_buf, dtype=float)
        store.volume[cur_symbol] = np.asarray(vol_buf, dtype=float)

    for symbol, date, close, volume in con.execute(
        "SELECT symbol, date, close, volume FROM bar ORDER BY symbol, date"
    ):
        i = index_of.get(date)
        if i is None:
            # A bar on a date the exchange calendar does not list. Recorded by
            # skipping rather than by inventing a session for it.
            continue
        if symbol != cur_symbol:
            flush()
            cur_symbol = symbol
            idx_buf, close_buf, vol_buf = [], [], []
        idx_buf.append(i)
        close_buf.append(float(close))
        vol_buf.append(float(volume))
    flush()
    return store
