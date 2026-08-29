"""The blindness field registry. **Names only. This module reads nothing.**

The two lists live here, apart from every module that acts on them, for one
reason: Guard 5 flags a bare string constant naming a priced field wherever it
appears, because a field read through a variable alias
(``for k in ("o", "open"): bar[k]``) defeats a constant-subscript walk. **The
declaration site would otherwise flag itself.** Separating the registry from the
readers means the guard needs exactly one structural exemption — this file — and
that exemption is a module containing **no logic at all**.
"""

from __future__ import annotations

from typing import Final

PRICED_BAR_FIELDS: Final[frozenset[str]] = frozenset(
    {
        "open",
        "high",
        "low",
        "close",
        "volume",
        "vwap",
        "trade_count",
        "tradecount",
        "trades",
        "bid",
        "ask",
        "o",
        "h",
        "l",
        "c",
        "v",
        "vw",
        "n",
        "bp",
        "ap",
        "bidprice",
        "askprice",
        "bid_price",
        "ask_price",
        "adjclose",
        "adj_close",
        "openinterest",
    }
)
"""Every spelling of a priced bar field, in every vendor dialect probed.

Guard 5 refuses a read of any of these outside a sealed writer. The list is
deliberately wider than any single vendor's schema: a field this repository
never sees costs nothing to forbid, and a field it forbids too late costs the
whole experiment.
"""

READABLE_FIELDS: Final[frozenset[str]] = frozenset(
    {
        "ticker",
        "symbol",
        "exchange",
        "primary_exchange",
        "listing_date",
        "delisting_date",
        "delisted_utc",
        "timestamp",
        "t",
        "session_date",
        "bar_count",
        "status_code",
        "status",
    }
)
"""The readable field list of the blindness section, stated exactly.

Ticker symbol, exchange code, listing and delisting dates, bar timestamp, bar
count per session, session date, and the vendor response status code. Nothing
else.
"""
