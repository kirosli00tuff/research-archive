"""The mock broker. The adapter shape D.1's real adapter will match.

Read-only on purpose. It serves quotes, settled cash, fractionability,
and the managed-accounts list, which is everything C.1's pipeline
consumes. No submit method exists anywhere in this stage, because C.1
places nothing, paper or live. D.1 adds submission to the real adapter
behind the gate, and the adapter grows nothing the mock does not
declare first.

Fractionability fails closed: a symbol absent from the eligibility
snapshot reads as not fractionable, never as eligible by default.
"""
from __future__ import annotations

from collections.abc import Mapping, Sequence

from hfexperiment.intents import ConstructionRefusal, Quote, capture_quote


class MockBroker:
    """One in-memory broker state for the demonstrations and tests."""

    def __init__(
        self,
        *,
        settled_cash_usd: float,
        quotes: Mapping[str, tuple[float, float]],
        fractionable: Mapping[str, bool],
        managed_accounts: Sequence[str],
        now_utc: str,
    ) -> None:
        self._cash = settled_cash_usd
        self._quotes = dict(quotes)
        self._fractionable = dict(fractionable)
        self._managed = tuple(managed_accounts)
        self._now = now_utc

    def quote(self, symbol: str) -> Quote | ConstructionRefusal:
        """A captured quote with its arrival mid, or the named refusal."""
        pair = self._quotes.get(symbol)
        if pair is None:
            return ConstructionRefusal(
                reason="no_arrival_mid",
                arithmetic=f"{symbol} has no quote at capture time, so "
                           "no arrival mid exists to anchor the "
                           "execution measurement",
            )
        bid, ask = pair
        return capture_quote(bid, ask, self._now)

    def settled_cash_usd(self) -> float:
        return self._cash

    def is_fractionable(self, symbol: str) -> bool:
        return self._fractionable.get(symbol, False)

    def managed(self) -> tuple[str, ...]:
        return self._managed

    def fractionable_snapshot(self) -> dict[str, bool]:
        return dict(self._fractionable)
