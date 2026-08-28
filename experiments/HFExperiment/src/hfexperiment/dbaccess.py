"""Read-only access to the AiTrader analysis database.

The database belongs to another repository and another running experiment.
Every connection here opens with SQLite's read-only URI mode, so a write
raises OperationalError at the database layer rather than relying on
discipline. tests/test_readonly.py produces that refusal.
"""
from __future__ import annotations

import sqlite3
from pathlib import Path

ANALYSIS_DB = Path.home() / "Documents/GitHub/AiTrader/analysis_bars.db"


def open_readonly(path: str | Path = ANALYSIS_DB) -> sqlite3.Connection:
    """A read-only connection. Writes raise sqlite3.OperationalError."""
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(p)
    return sqlite3.connect(f"file:{p}?mode=ro", uri=True)
