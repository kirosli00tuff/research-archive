"""The Cohen-Malloy-Pomorski routine versus opportunistic rule.

An insider is routine if she traded in the same calendar month for at least
three consecutive prior years, opportunistic otherwise. Computed purely
look-back: only trades strictly before the candidate transaction enter, so the
label a transaction carries on its own date can never move when later filings
arrive.

An insider whose first observed trade is less than three years before the
candidate has too little history to classify. That is a third state and it is
recorded as one. It is not routine and it is not opportunistic.
"""

from __future__ import annotations

import datetime as dt
from collections import defaultdict
from dataclasses import dataclass, field
from enum import StrEnum

from insider.config import CONFIG, Config


class RoutineClass(StrEnum):
    ROUTINE = "routine"
    OPPORTUNISTIC = "opportunistic"
    INSUFFICIENT_HISTORY = "insufficient_history"


@dataclass
class TradeHistory:
    """Every insider's look-back trade months, built once from the filing stream.

    Only the registered look-back codes enter. Including A grants would make
    almost every insider routine, because grants land in the same calendar month
    every year by design, and that would empty the opportunistic category the
    hypothesis rests on.
    """

    months_traded: dict[int, set[tuple[int, int]]] = field(default_factory=lambda: defaultdict(set))
    first_trade: dict[int, dt.date] = field(default_factory=dict)

    def add(self, filer_cik: int, when: dt.date) -> None:
        self.months_traded[filer_cik].add((when.year, when.month))
        seen = self.first_trade.get(filer_cik)
        if seen is None or when < seen:
            self.first_trade[filer_cik] = when

    def insiders(self) -> int:
        return len(self.first_trade)


def _minus_years(when: dt.date, years: int) -> dt.date:
    try:
        return when.replace(year=when.year - years)
    except ValueError:  # 29 February
        return when.replace(year=when.year - years, day=28)


def classify(
    history: TradeHistory, filer_cik: int, when: dt.date, cfg: Config = CONFIG
) -> RoutineClass:
    """Label one insider on one date from her prior trades and nothing else.

    The routine pattern is tested first, and the history gate second. That
    order is the rule's own. Cohen, Malloy and Pomorski define a routine trader
    by the pattern, and impose the three-year history requirement on the
    opportunistic category, which is the residual. Testing history first
    reverses that: an insider who traded the same calendar month in each of the
    three prior years satisfies the routine definition outright, and gating her
    on whether her earliest trade cleared three full calendar years would file a
    definitionally routine insider under insufficient_history over a few days.
    """
    months = history.months_traded.get(filer_cik, set())
    if all(
        (when.year - back, when.month) in months
        for back in range(1, cfg.routine_consecutive_years + 1)
    ):
        return RoutineClass.ROUTINE

    first = history.first_trade.get(filer_cik)
    if first is None or first > _minus_years(when, cfg.min_history_years):
        return RoutineClass.INSUFFICIENT_HISTORY
    return RoutineClass.OPPORTUNISTIC
