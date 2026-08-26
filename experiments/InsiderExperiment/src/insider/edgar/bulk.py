"""The SEC's own structured Form 345 data sets, one zip per calendar quarter.

These files are the parsed contents of the Form 4 XML documents, published free
by the SEC. ADR-002 records why they carry the bulk of the corpus and why the
per-filing XML route is exercised on a sample rather than on every filing.

Nothing here interprets a transaction. It yields rows.
"""

from __future__ import annotations

import csv
import datetime as dt
import io
import zipfile
from collections.abc import Iterator
from typing import Any

from insider.config import CONFIG, Config
from insider.edgar.client import fetch

BASE = "https://www.sec.gov/files/structureddata/data/insider-transactions-data-sets"

SUBMISSION = "SUBMISSION.tsv"
REPORTING_OWNER = "REPORTINGOWNER.tsv"
NONDERIV_TRANS = "NONDERIV_TRANS.tsv"

_MONTHS = {
    "JAN": 1, "FEB": 2, "MAR": 3, "APR": 4, "MAY": 5, "JUN": 6,
    "JUL": 7, "AUG": 8, "SEP": 9, "OCT": 10, "NOV": 11, "DEC": 12,
}


def parse_dera_date(raw: str) -> dt.date | None:
    """DD-MON-YYYY as the data sets write it, or None when the field is blank.

    Returns None rather than a substituted date. A blank transaction date is an
    absence and the caller charges it to `unparseable`.
    """
    text = (raw or "").strip()
    if len(text) != 11 or text[2] != "-" or text[6] != "-":
        return None
    month = _MONTHS.get(text[3:6].upper())
    if month is None:
        return None
    try:
        return dt.date(int(text[7:]), month, int(text[:2]))
    except ValueError:
        return None


def quarters(cfg: Config = CONFIG) -> list[str]:
    """Every quarter tag from the registered first to the registered last."""
    first_year, first_q = int(cfg.dera_first_quarter[:4]), int(cfg.dera_first_quarter[5])
    last_year, last_q = int(cfg.dera_last_quarter[:4]), int(cfg.dera_last_quarter[5])
    out: list[str] = []
    year, quarter = first_year, first_q
    while (year, quarter) <= (last_year, last_q):
        out.append(f"{year}q{quarter}")
        quarter += 1
        if quarter == 5:
            year, quarter = year + 1, 1
    return out


def quarter_url(quarter: str) -> str:
    return f"{BASE}/{quarter}_form345.zip"


def fetch_quarter(quarter: str, cfg: Config = CONFIG) -> zipfile.ZipFile:
    """One quarter's zip, from the cache when it is already there."""
    return zipfile.ZipFile(io.BytesIO(fetch(quarter_url(quarter), cfg=cfg)))


def iter_table(archive: zipfile.ZipFile, member: str) -> Iterator[dict[str, Any]]:
    """Rows of one TSV as dicts. The SEC writes these tab separated with a header."""
    with archive.open(member) as handle:
        text = io.TextIOWrapper(handle, encoding="utf-8", errors="replace", newline="")
        yield from csv.DictReader(text, delimiter="\t")
