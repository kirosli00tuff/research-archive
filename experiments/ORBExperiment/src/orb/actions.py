"""The corporate-actions substrate — symbols and dates. It reads no price.

Splits, reverse splits, symbol changes and delistings, with their dates. This
is the substrate A.3 TASK 2 watches daily, because **a split landing on a stored
session is the event most likely to trigger a silent vendor rewrite**, and a
rewrite that is watched is a measurement while a rewrite that is discovered is
the MLCryptoEngine H11 death in a different costume.

Every field here is inside the readable field list: ticker symbol, exchange
code, listing and delisting dates, session date. **No ratio is a price and no
count is a volume**, and a split ratio is recorded because it identifies the
event, never because anything divides a bar by it in Stage A.
"""

from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass
from datetime import date
from enum import StrEnum, unique
from typing import final

from orb.ledger import AppendOnlyLedger


@unique
class ActionKind(StrEnum):
    SPLIT = "split"
    REVERSE_SPLIT = "reverse_split"
    SYMBOL_CHANGE = "symbol_change"
    DELISTING = "delisting"
    LISTING = "listing"


@final
@dataclass(frozen=True, slots=True)
class CorporateAction:
    """One dated event against one symbol. Symbols and dates only."""

    ticker: str
    kind: ActionKind
    effective_date: date
    new_ticker: str | None = None
    ratio_numerator: int | None = None
    ratio_denominator: int | None = None
    exchange: str | None = None

    def key(self) -> str:
        """The session-ticker key this action would collide with."""
        return f"{self.ticker}/{self.effective_date.isoformat()}"

    def as_row(self) -> dict[str, object]:
        return {
            "kind": self.kind.value,
            "ticker": self.ticker,
            "effective_date": self.effective_date.isoformat(),
            "new_ticker": self.new_ticker,
            "ratio_numerator": self.ratio_numerator,
            "ratio_denominator": self.ratio_denominator,
            "exchange": self.exchange,
        }


@final
class ActionsSubstrate:
    """An append-only ledger of dated corporate actions, keyed by symbol."""

    __slots__ = ("_ledger",)

    def __init__(self, ledger: AppendOnlyLedger) -> None:
        self._ledger = ledger

    def record(self, actions: Iterable[CorporateAction]) -> int:
        """Append every action durably. Returns the count appended."""
        n = 0
        for action in actions:
            self._ledger.append(action.as_row())
            n += 1
        return n

    def collision_keys(self, actions: Iterable[CorporateAction]) -> frozenset[str]:
        """Session-ticker keys where an action lands on a stored session.

        This is the set handed to the sealed comparator so that a measured bar
        revision can be attributed to a corporate action rather than merely
        coinciding with one.
        """
        return frozenset(
            a.key()
            for a in actions
            if a.kind in {ActionKind.SPLIT, ActionKind.REVERSE_SPLIT}
        )

    def counts_by_kind(self, actions: Iterable[CorporateAction]) -> dict[str, int]:
        counts: dict[str, int] = dict.fromkeys((k.value for k in ActionKind), 0)
        for action in actions:
            counts[action.kind.value] += 1
        return counts

    def delistings_per_year(
        self, actions: Iterable[CorporateAction], start: date, end: date
    ) -> dict[int, int]:
        """Delisting counts per calendar year inside ``[start, end]``."""
        per_year: dict[int, int] = {}
        for action in actions:
            if action.kind is not ActionKind.DELISTING:
                continue
            if start <= action.effective_date <= end:
                year = action.effective_date.year
                per_year[year] = per_year.get(year, 0) + 1
        return per_year
