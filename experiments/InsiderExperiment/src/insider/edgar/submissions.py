"""The submissions JSON API at data.sec.gov.

Used to confirm that an issuer CIK maps to the ticker the structured data sets
carry. A data set that names a symbol the SEC does not associate with that CIK
is a fact to record before the symbol is joined to a price series.
"""

from __future__ import annotations

import json
from typing import Any

from insider.config import CONFIG, Config
from insider.edgar.client import fetch

SUBMISSIONS = "https://data.sec.gov/submissions/CIK{cik:010d}.json"


def submission_metadata(cik: int, cfg: Config = CONFIG) -> dict[str, Any]:
    payload: dict[str, Any] = json.loads(fetch(SUBMISSIONS.format(cik=cik), cfg=cfg))
    return payload


def tickers_for(cik: int, cfg: Config = CONFIG) -> tuple[str, ...]:
    """Every ticker the SEC currently associates with this CIK.

    Present-day, not point-in-time. A delisted issuer answers with an empty
    tuple, which is a recorded absence at the call site and never evidence that
    the data set's symbol was wrong.
    """
    meta = submission_metadata(cik, cfg=cfg)
    return tuple(str(t).upper() for t in meta.get("tickers", []))
