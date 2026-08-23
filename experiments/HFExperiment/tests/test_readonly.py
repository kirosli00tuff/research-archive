"""A write attempt on the analysis database connection raises."""
import sqlite3
from pathlib import Path

import pytest

from hfexperiment.dbaccess import open_readonly


def make_db(path: Path) -> None:
    con = sqlite3.connect(path)
    con.execute("CREATE TABLE bars (symbol TEXT, close REAL)")
    con.execute("INSERT INTO bars VALUES ('TEST', 1.0)")
    con.commit()
    con.close()


def test_write_attempt_raises(tmp_path: Path) -> None:
    db = tmp_path / "synthetic.db"
    make_db(db)
    con = open_readonly(db)
    assert con.execute("SELECT COUNT(*) FROM bars").fetchone()[0] == 1
    with pytest.raises(sqlite3.OperationalError):
        con.execute("INSERT INTO bars VALUES ('EVIL', 2.0)")
    with pytest.raises(sqlite3.OperationalError):
        con.execute("DROP TABLE bars")
    con.close()


def test_missing_database_raises(tmp_path: Path) -> None:
    with pytest.raises(FileNotFoundError):
        open_readonly(tmp_path / "absent.db")
