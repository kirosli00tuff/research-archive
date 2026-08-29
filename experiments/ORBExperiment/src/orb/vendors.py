"""Vendor endpoints, and the one place a credential is turned into a request.

Every URL and every authentication header this repository sends is built here.
Credentials arrive as an :class:`orb.credentials.CredentialStore` and leave as
request headers; **no credential is ever placed in a query string**, so a URL is
safe to record before Guard 8 ever looks at it. Guard 8 still looks at it —
defence at the recording boundary does not depend on the call site being
careful — but the call site is careful anyway.

Two vendors hold credentials:

- **Massive**, the vendor formerly branded Polygon. Measured at A.1 TASK 1:
  ``polygon.io`` 301-redirects to ``massive.com`` while the API host
  ``api.polygon.io`` still answers and still returns Polygon-shaped JSON.
  Authenticates with ``Authorization: Bearer``.
- **Alpaca**. Authenticates with two headers, key and secret.

**Pacing is per endpoint, never per host**, and every spacing here is
**conservative and labelled unmeasured** until A.1 TASK 7 measures the
authenticated paths. Amendment 2's corollary runs both ways: the 88.4 per
minute measured against a 401 is evidence about the refusal path and nothing
else, so it licenses no increase here.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Final, final

from orb.credentials import (
    ALPACA_API_KEY,
    ALPACA_SECRET_KEY,
    MASSIVE_API_KEY,
    CredentialStore,
)

MASSIVE: Final[str] = "massive"
ALPACA: Final[str] = "alpaca"

MASSIVE_HOST: Final[str] = "https://api.polygon.io"
ALPACA_DATA_HOST: Final[str] = "https://data.alpaca.markets"
ALPACA_TRADING_HOST: Final[str] = "https://api.alpaca.markets"
ALPACA_PAPER_HOST: Final[str] = "https://paper-api.alpaca.markets"

MASSIVE_DOCUMENTED_PER_MINUTE: Final[int] = 5
"""Documented free-tier limit. **Carried** (standing rule 4) — and, unusually,
**confirmed by measurement** at A.1 TASK 7: first refusal at request 6 of 8 on
both endpoints, `n = 16`."""

ALPACA_DOCUMENTED_PER_MINUTE: Final[int] = 200
"""Documented free-tier limit. **Carried, never measured** — A.1 TASK 7 admitted
25 of 25 at 134.05 per minute and **never reached a refusal**, so the ceiling is
known to be **at or above 134** and is not known exactly."""

MEASURED_CEILING_PER_MINUTE: Final[dict[str, float | None]] = {
    "massive:reference": 5.0,
    "massive:aggs": 5.0,
    "massive:grouped": 5.0,
    "alpaca:bars": None,
    "alpaca:multibars": None,
    "alpaca:account": None,
    "alpaca:assets": None,
}
"""Measured ceilings per endpoint, A.1 TASK 7, 2026-08-29. `n = 53` requests.

`None` means **the ceiling was not reached**, which is a different statement from
*"there is no ceiling"* and is recorded as its own value rather than as a large
number. Massive's figure is a **measured 429 boundary**: `HTTP 429`,
`{"status":"ERROR",…,"error":"You've exceeded the maximum requests per minute…"}`,
first refusal at request **6** in both `n = 8` cells.

Per endpoint, never per host (solattn ADR-021) — and the two Massive endpoints
were measured **separately** and agreed, which is evidence rather than an
assumption that they share a limiter.
"""

CONSERVATIVE_SPACING_S: Final[dict[str, float]] = {
    # Half the measured 5.0 per minute is 2.5 per minute, which is 24.0 s.
    "massive:aggs": 24.0,
    "massive:reference": 24.0,
    "massive:grouped": 24.0,
    # The ceiling was not reached. Half of the **highest admitted rate observed**
    # (134.05 per minute) is 67 per minute; 1.0 s is 60 per minute, below it and
    # far below the documented 200. **Half of an observed admitted rate is not
    # half of a measured ceiling**, and PACE_BASIS says so per endpoint.
    "alpaca:bars": 1.0,
    "alpaca:multibars": 1.0,
    "alpaca:account": 1.0,
    "alpaca:assets": 1.0,
}
"""The registered operating pace: **half the measured ceiling**, per endpoint.

Reduced further where recorded terms ask for it. No endpoint here is paced
faster than its measurement licenses, and an endpoint whose ceiling was never
reached is paced from an **observed admitted rate**, labelled as such.
"""

PACE_BASIS: Final[dict[str, str]] = {
    "massive:aggs": "measured: half of a measured 5.0/min 429 boundary",
    "massive:reference": "measured: half of a measured 5.0/min 429 boundary",
    "massive:grouped": "unmeasured endpoint; carries its vendor's measured figure",
    "alpaca:bars": "unmeasured ceiling; half of a 134.05/min observed admitted rate",
    "alpaca:multibars": "unmeasured endpoint; carries its vendor's figure",
    "alpaca:account": "unmeasured endpoint; carries its vendor's figure",
    "alpaca:assets": "unmeasured endpoint; carries its vendor's figure",
}
"""What each operating pace rests on. **An unmeasured endpoint keeps its
vendor's figure rather than a faster default** — an unmeasured endpoint is not a
licence to speed up."""

PROVISIONAL_DAILY_CAPS: Final[dict[str, int]] = {
    MASSIVE: 600,
    ALPACA: 2000,
}
"""Per-vendor daily caps, charged **before** sending, registered at A.1 TASK 7.

**Neither is a throughput target; both are circuit breakers against a runaway
loop.** Massive's measured 5 per minute makes 600 about two hours of continuous
full-rate use, which is more than any registered task needs and still a real
brake. Alpaca's 2,000 covers the registered 40-ticker probe slice, its identical
re-pull, and headroom, at an observed 134 per minute.

**No daily allowance was measured on either vendor**, and neither cap is derived
from one. Deriving a cap from an unmeasured daily allowance is exactly the
pricing-page reasoning standing rule 4 forbids.
"""


class VendorCredentialError(RuntimeError):
    """Raised when a vendor is asked for a request it holds no credential for."""


@final
@dataclass(frozen=True, slots=True)
class VendorRequest:
    """A URL, its auth headers, its vendor and its pace key. Ready to send."""

    vendor: str
    pace_key: str
    url: str
    headers: dict[str, str]

    def as_row(self) -> dict[str, object]:
        """A recordable row. **Headers are excluded by construction.**"""
        return {"vendor": self.vendor, "pace_key": self.pace_key, "url": self.url}


def massive_headers(store: CredentialStore) -> dict[str, str]:
    """Bearer auth. The key never enters a URL."""
    return {"Authorization": f"Bearer {store.require(MASSIVE_API_KEY)}"}


def alpaca_headers(store: CredentialStore) -> dict[str, str]:
    """Key and secret headers. Neither ever enters a URL."""
    return {
        "APCA-API-KEY-ID": store.require(ALPACA_API_KEY),
        "APCA-API-SECRET-KEY": store.require(ALPACA_SECRET_KEY),
    }


# --- Massive ---------------------------------------------------------------


def massive_reference(store: CredentialStore, *, limit: int = 1) -> VendorRequest:
    """The reference endpoint. Serves ticker, exchange and delisting dates."""
    return VendorRequest(
        vendor=MASSIVE,
        pace_key="massive:reference",
        url=f"{MASSIVE_HOST}/v3/reference/tickers?limit={limit}",
        headers=massive_headers(store),
    )


def massive_active_common(
    store: CredentialStore, *, limit: int = 1000, cursor_url: str | None = None
) -> VendorRequest:
    """Active US common stock, ordered by ticker. **Reads no price.**

    ``type=CS`` is applied **in the request** rather than after it: a bare
    ``limit`` returns every security type and filtering afterwards leaves a pool
    smaller than the one asked for, which is how the first probe-pull attempt
    came back with 32 candidates instead of 100.
    """
    url = cursor_url or (
        f"{MASSIVE_HOST}/v3/reference/tickers?market=stocks&active=true"
        f"&type=CS&limit={limit}&sort=ticker&order=asc"
    )
    return VendorRequest(
        vendor=MASSIVE,
        pace_key="massive:reference",
        url=url,
        headers=massive_headers(store),
    )


def massive_delisted(
    store: CredentialStore,
    *,
    limit: int = 1000,
    cursor_url: str | None = None,
    delisted_after: str | None = None,
    delisted_before: str | None = None,
) -> VendorRequest:
    """Delisted common stock on the US exchanges, paged by cursor."""
    if cursor_url is not None:
        url = cursor_url
    else:
        parts = [
            "market=stocks",
            "active=false",
            "type=CS",
            f"limit={limit}",
            "sort=delisted_utc",
            "order=asc",
        ]
        if delisted_after is not None:
            parts.append(f"delisted_utc.gte={delisted_after}")
        if delisted_before is not None:
            parts.append(f"delisted_utc.lte={delisted_before}")
        url = f"{MASSIVE_HOST}/v3/reference/tickers?" + "&".join(parts)
    return VendorRequest(
        vendor=MASSIVE,
        pace_key="massive:reference",
        url=url,
        headers=massive_headers(store),
    )


def massive_minute_bars(
    store: CredentialStore,
    ticker: str,
    start_session: str,
    end_session: str,
    *,
    limit: int = 50000,
) -> VendorRequest:
    """One-minute aggregates for one ticker over an inclusive session range."""
    url = (
        f"{MASSIVE_HOST}/v2/aggs/ticker/{ticker}/range/1/minute/"
        f"{start_session}/{end_session}?adjusted=true&sort=asc&limit={limit}"
    )
    return VendorRequest(
        vendor=MASSIVE,
        pace_key="massive:aggs",
        url=url,
        headers=massive_headers(store),
    )


# --- Alpaca ----------------------------------------------------------------


def alpaca_minute_bars(
    store: CredentialStore,
    ticker: str,
    start_iso: str,
    end_iso: str,
    *,
    feed: str = "sip",
    limit: int = 10000,
    page_token: str | None = None,
) -> VendorRequest:
    """One-minute bars for one ticker between two UTC instants."""
    parts = [
        "timeframe=1Min",
        f"start={start_iso}",
        f"end={end_iso}",
        f"feed={feed}",
        f"limit={limit}",
        "adjustment=raw",
    ]
    if page_token is not None:
        parts.append(f"page_token={page_token}")
    return VendorRequest(
        vendor=ALPACA,
        pace_key="alpaca:bars",
        url=f"{ALPACA_DATA_HOST}/v2/stocks/{ticker}/bars?" + "&".join(parts),
        headers=alpaca_headers(store),
    )


def alpaca_assets(store: CredentialStore, *, status: str = "inactive") -> VendorRequest:
    """The trading-API asset list. Names listing status; carries no bar."""
    return VendorRequest(
        vendor=ALPACA,
        pace_key="alpaca:assets",
        url=f"{ALPACA_TRADING_HOST}/v2/assets?status={status}&asset_class=us_equity",
        headers=alpaca_headers(store),
    )


def alpaca_account(store: CredentialStore, *, paper: bool = False) -> VendorRequest:
    """The account endpoint. Used only to establish which key family this is."""
    host = ALPACA_PAPER_HOST if paper else ALPACA_TRADING_HOST
    return VendorRequest(
        vendor=ALPACA,
        pace_key="alpaca:account",
        url=f"{host}/v2/account",
        headers=alpaca_headers(store),
    )
