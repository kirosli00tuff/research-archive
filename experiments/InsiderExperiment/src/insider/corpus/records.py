"""The one shape a candidate transaction has as it moves down the funnel."""

from __future__ import annotations

import datetime as dt
from dataclasses import dataclass, replace

from insider.absence import Absent
from insider.callstate import CallState


@dataclass(frozen=True, slots=True)
class Transaction:
    """One Form 4 non-derivative transaction, before any filter has run."""

    accession: str
    issuer_cik: int
    symbol: str
    filer_cik: int
    roles: frozenset[str]
    transaction_date: dt.date
    filing_date: dt.date
    code: str
    shares: float
    price_per_share: float
    aff10b5one: bool | Absent

    @property
    def value_usd(self) -> float:
        return self.shares * self.price_per_share

    @property
    def filing_lag_days(self) -> int:
        return (self.filing_date - self.transaction_date).days


@dataclass(frozen=True, slots=True)
class Verdict:
    """Where one transaction stopped, and why in its own words.

    `state` is the registered call state. `reason` is the sub-reason inside it.
    The pair is never collapsed: filtered_routine covers both a routine insider
    and an insider with too little history to classify, and those are different
    facts about the sample.
    """

    state: CallState
    reason: str

    def with_reason(self, reason: str) -> Verdict:
        return replace(self, reason=reason)


PASSED = Verdict(CallState.PARSED, "qualifying")
