"""Append-only store: latest row wins, nothing ever mutates."""
import re
import sqlite3
from pathlib import Path

import hfexperiment.barstore as barstore_module
from hfexperiment.barstore import BarStore


def test_source_contains_no_update_and_no_delete() -> None:
    src = Path(barstore_module.__file__).read_text()
    assert not re.search(r"\b(UPDATE|DELETE)\b", src)


def test_adjustment_reentry_latest_row_wins_and_both_rows_persist(
    tmp_path: Path,
) -> None:
    store = BarStore(tmp_path / "bars.db")
    store.append_bars(
        [("AAA", "2026-09-01", None, None, None, 10.0, 100.0)],
        "all",
        "2026-09-01T23:30:00Z",
    )
    # A split lands after the first query. The fresh query re-enters
    # the adjusted close as a newer row. Nothing mutates.
    store.append_bars(
        [("AAA", "2026-09-01", None, None, None, 5.0, 100.0)],
        "all",
        "2026-09-02T23:30:00Z",
    )
    closes = store.latest_closes(["AAA"], "2026-09-01", "2026-09-01")
    assert closes[("AAA", "2026-09-01")] == 5.0
    assert store.last_close_at_or_before("AAA", "2026-09-05") == 5.0
    store.close()
    conn = sqlite3.connect(tmp_path / "bars.db")
    assert conn.execute("SELECT COUNT(*) FROM bars").fetchone()[0] == 2
    conn.close()


def test_sessions_assets_formations_and_fetch_log_roundtrip(
    tmp_path: Path,
) -> None:
    store = BarStore(tmp_path / "bars.db")
    store.append_sessions(
        [("2026-09-01", "09:30", "16:00"), ("2026-09-02", "09:30", "16:00")],
        "t1",
    )
    assert store.session_dates("2026-09-01", "2026-09-02") == [
        "2026-09-01", "2026-09-02"
    ]
    store.append_assets([("AAA", "Alpha Corp", "NYSE", "active", 1)], "t1")
    store.append_assets([("AAA", "Alpha Corp", "NYSE", "inactive", 0)], "t2")
    assert store.latest_assets()["AAA"].active is False
    store.append_universe("2026-09-01", ["AAA", "BBB"], "t1")
    assert store.universe_members("2026-09-01") == ["AAA", "BBB"]
    store.append_formation("2026-09-01", 5, ["BBB", "AAA"], "t1")
    assert store.formation_books("2026-09-01") == {5: ["BBB", "AAA"]}
    assert store.recorded_formation_dates() == ["2026-09-01"]
    store.append_fetch("t1", "calendar", True, "2 sessions")
    run, endpoint, ok, detail = store.recent_fetches(1)[0]
    assert (run, endpoint, ok, detail) == ("t1", "calendar", True,
                                           "2 sessions")
    store.close()
