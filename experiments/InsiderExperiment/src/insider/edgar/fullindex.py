"""The EDGAR full-index archives.

Used as an independent count of how many Form 4 filings each quarter holds, so
the structured data sets can be checked against the filing stream rather than
trusted. A gap between the two is a fact to record, not to smooth.
"""

from __future__ import annotations

from dataclasses import dataclass

from insider.config import CONFIG, Config
from insider.edgar.client import fetch

BASE = "https://www.sec.gov/Archives/edgar/full-index"


@dataclass(frozen=True, slots=True)
class QuarterCount:
    quarter: str
    form4_index_rows: int
    total_index_rows: int


def form_index_url(quarter: str) -> str:
    year, q = quarter[:4], quarter[5]
    return f"{BASE}/{year}/QTR{q}/form.idx"


def count_form4(quarter: str, cfg: Config = CONFIG) -> QuarterCount:
    """Count `4` rows in one quarter's form index.

    form.idx carries one row per filer per filing, so an ownership filing with
    an issuer and two reporting owners contributes three rows. The count is a
    coverage signal, not a filing count, and it is labelled that way.
    """
    text = fetch(form_index_url(quarter), cfg=cfg).decode("latin-1")
    form4 = 0
    total = 0
    started = False
    for line in text.splitlines():
        if not started:
            if line.startswith("---"):
                started = True
            continue
        if not line.strip():
            continue
        total += 1
        if line[:12].strip() == "4":
            form4 += 1
    return QuarterCount(quarter=quarter, form4_index_rows=form4, total_index_rows=total)
