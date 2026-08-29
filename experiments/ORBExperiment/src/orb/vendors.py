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

from collections.abc import Mapping
from dataclasses import dataclass
from typing import Final, final

from orb.config import CONFIG
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
"""Measured **sustained** per-minute ceilings per endpoint, A.1 TASK 7 and the
amendment pass of 2026-08-29.

`None` means **the sustained ceiling was not reached**, which is a different
statement from *"there is no ceiling"* and is recorded as its own value rather
than as a large number. Massive's figure is a **measured 429 boundary**:
`HTTP 429`,
`{"status":"ERROR",…,"error":"You've exceeded the maximum requests per minute…"}`,
first refusal at request **6** in both `n = 8` cells.

**`alpaca:bars` stays `None` after the amendment pass, and the reason is
precise.** A refusal boundary *was* reached — see
:data:`MEASURED_BURST_REFUSAL` — but it is a **burst allowance**, not a
sustained rate. Sending at the documented 200 per minute for **75.10 s**, which
is longer than one rolling minute, drew **0 refusals over `n = 250`**. So the
sustained ceiling is **at or above 199.73 per minute and is not known exactly**,
and `None` is the honest entry. See
:data:`MEASURED_SUSTAINED_ADMITTED_PER_MINUTE` for the lower bound.

Per endpoint, never per host (solattn ADR-021) — and the two Massive endpoints
were measured **separately** and agreed, which is evidence rather than an
assumption that they share a limiter.
"""

MEASURED_BURST_REFUSAL: Final[dict[str, tuple[int, float] | None]] = {
    "massive:reference": (5, 15.76),
    "massive:aggs": (5, 16.74),
    "massive:grouped": None,
    "alpaca:bars": (384, 55.96),
    "alpaca:multibars": None,
    "alpaca:account": None,
    "alpaca:assets": None,
}
"""**(requests admitted before the first refusal, window in seconds).**

The measured **burst allowance**. `alpaca:bars` admitted **384 requests in
55.96 s** and refused the **385th** with `HTTP 429`,
`{"message": "too many requests."}`, under an escalation that ran 1 worker at
0.2 s, 0.05 s and 0 s spacing and then 2, 4 and 8 workers, `n = 391` sent.

**The whole escalation fit inside one rolling minute**, which is exactly why
this is recorded as a burst allowance and not as a ceiling: **a token bucket of
capacity near 400 refilling at the documented 200 per minute would produce this
observation**, and so would a hard 411-per-minute limiter. The measurement does
not distinguish them, and does not pretend to.
"""

MEASURED_SUSTAINED_ADMITTED_PER_MINUTE: Final[dict[str, float | None]] = {
    "massive:reference": None,
    "massive:aggs": None,
    "massive:grouped": None,
    "alpaca:bars": 199.73,
    "alpaca:multibars": None,
    "alpaca:account": None,
    "alpaca:assets": None,
}
"""The highest rate **sustained for longer than one rolling minute with zero
refusals**. **A lower bound, never a ceiling.**

`alpaca:bars`: **250 of 250 admitted over 75.10 s at a scheduled 200 per
minute**, `n = 250`, `0` refusals, after a 75 s cooldown. That is a lower bound
on the sustained ceiling and is **not** a statement that the ceiling is 199.73.
It also **falsifies nothing about the documented 200 per minute** — it confirms
the documented figure is achievable as a rate, which the previous 134.05 per
minute could not, because a single-threaded client is latency-bound below it.
"""

CONSERVATIVE_SPACING_S: Final[dict[str, float]] = {
    # Half the measured 5.0 per minute is 2.5 per minute, which is 24.0 s.
    "massive:aggs": 24.0,
    "massive:reference": 24.0,
    "massive:grouped": 24.0,
    # The SUSTAINED ceiling was still not reached. Half of the **maximum rate
    # actually attempted and sustained** (199.73 per minute over 75.10 s, 0
    # refusals) is 99.86 per minute; 0.61 s is 98.36 per minute, below it.
    # **Half of a sustained lower bound is not half of a measured ceiling**, and
    # PACE_BASIS says so. The measured 384-request burst allowance is a looser
    # constraint than this and does not bind.
    "alpaca:bars": 0.61,
    # **Unmeasured endpoints keep the old figure.** Pacing is per endpoint,
    # never per host: a measurement on `alpaca:bars` licenses no change here.
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
    "alpaca:bars": (
        "measured burst allowance 384 requests in 55.96 s; sustained ceiling "
        "NOT reached at 199.73/min over 75.10 s, n = 250, 0 refusals. Pace is "
        "half the maximum rate actually SUSTAINED, spacing rounded up."
    ),
    "alpaca:multibars": "unmeasured endpoint; carries its vendor's figure",
    "alpaca:account": "unmeasured endpoint; carries its vendor's figure",
    "alpaca:assets": "unmeasured endpoint; carries its vendor's figure",
}
"""What each operating pace rests on. **An unmeasured endpoint keeps its
vendor's figure rather than a faster default** — an unmeasured endpoint is not a
licence to speed up."""

PROVISIONAL_DAILY_CAPS: Final[dict[str, int]] = {
    MASSIVE: 600,
    ALPACA: 3000,
}
"""Per-vendor daily caps, charged **before** sending. Registered at A.1 TASK 7;
**Alpaca's moved from 2,000 to 3,000 by Amendment 14**, 2026-08-29.

**Neither is a throughput target; both are circuit breakers against a runaway
loop.** Massive's measured 5 per minute makes 600 about two hours of continuous
full-rate use, which is more than any registered task needs and still a real
brake. Alpaca's 3,000 is about **30 minutes** of continuous use at the registered
98.36 per minute — still a brake, and enough for the 480-file probe slice, its
identical 480-file re-pull, a dispersion pull and measurement overhead **in the
same day**, which 2,000 was not.

**No daily allowance has been measured on either vendor**, and neither cap is
derived from one. The amendment-pass ceiling measurement is evidence about
**rate**, not about a daily total, and it is not used as if it were. Deriving a
cap from an unmeasured daily allowance is exactly the pricing-page reasoning
standing rule 4 forbids.
"""


MEASURED_SINGLE_VENUE_FEED: Final[str] = "iex"
"""The Alpaca single-venue feed, measured at A.1 TASK 4 as a different tape.

**Median 0.027761 of consolidated first-5-minute volume, `n = 100`
session-ticker pairs**, IQR [0.021200, 0.037068], **share below the registered
0.20 single-venue threshold: 1.0**. `DIFFERENT_TAPE` against both Massive and
Alpaca-SIP. It is named here so that the one legitimate use of it — the tape
control of `tools/tape_identify.py` — has a name to ask for, rather than a
string a call site can type by accident.
"""


class VendorCredentialError(RuntimeError):
    """Raised when a vendor is asked for a request it holds no credential for."""


class TapeFeedError(RuntimeError):
    """Raised when a registered bar request is built on a non-consolidated feed.

    **The measured consequence of taking the wrong branch**: a feed carrying a
    **median 0.027761** of consolidated first-5-minute volume over `n = 100`
    pairs. Every bar it serves has a real high, a real low and a real volume,
    and every one of them is wrong about the market — so the error is
    **invisible** in every downstream figure. This is why the feed is a
    configured, guarded field rather than a function default.
    """


def consolidated_feed() -> str:
    """The registered consolidated tape. Read from config, never re-typed."""
    return CONFIG.consolidated_feed


def require_consolidated_feed(feed: str, context: str) -> str:
    """Refuse a registered bar request built on anything but the consolidated tape."""
    if feed != CONFIG.consolidated_feed:
        raise TapeFeedError(
            f"{context}: refusing a bar request on feed {feed!r}. The registered "
            f"feed is {CONFIG.consolidated_feed!r}, the consolidated tape. A.1 "
            f"TASK 4 measured {MEASURED_SINGLE_VENUE_FEED!r} at a median "
            "0.027761 of consolidated first-5-minute volume over n = 100 "
            "session-ticker pairs — a different tape, which would look entirely "
            "normal in every downstream figure. A non-consolidated feed is "
            "reachable only through alpaca_minute_bars_on_feed, which requires "
            "a stated reason."
        )
    return feed


MANIFEST_FEED_KEY: Final[str] = "feed"
"""The key every pull manifest records its feed under."""


def require_manifest_feed(manifest: Mapping[str, object], context: str) -> str:
    """Refuse a manifest that does not record the feed it was pulled on.

    A manifest is the instruction set for an identical re-pull. **A re-pull sent
    on a different feed than the original measures a tape difference and records
    it as a revision rate**, which is the one number this repository exists to
    measure. An absent feed key is a recorded refusal, never an assumed ``sip``.
    """
    recorded = manifest.get(MANIFEST_FEED_KEY)
    if recorded is None:
        raise TapeFeedError(
            f"{context}: the manifest records no {MANIFEST_FEED_KEY!r}. A "
            "re-pull on an unrecorded feed measures a tape difference and "
            "records it as a revision rate. Absence is a recorded state, never "
            "an assumed consolidated feed."
        )
    if not isinstance(recorded, str):
        raise TapeFeedError(
            f"{context}: the manifest records {MANIFEST_FEED_KEY!r} as "
            f"{type(recorded).__name__}, not a string."
        )
    return require_consolidated_feed(recorded, context)


@final
@dataclass(frozen=True, slots=True)
class VendorRequest:
    """A URL, its auth headers, its vendor and its pace key. Ready to send."""

    vendor: str
    pace_key: str
    url: str
    headers: dict[str, str]
    feed: str | None = None
    """The tape this request was built on, or ``None`` where the endpoint has no
    feed concept. **Carried on the request so a manifest cannot omit it.**"""

    def as_row(self) -> dict[str, object]:
        """A recordable row. **Headers are excluded by construction.**"""
        return {
            "vendor": self.vendor,
            "pace_key": self.pace_key,
            "url": self.url,
            MANIFEST_FEED_KEY: self.feed,
        }


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
    feed: str,
    limit: int = 10000,
    page_token: str | None = None,
) -> VendorRequest:
    """One-minute bars for one ticker between two UTC instants.

    **``feed`` carries no default, by Amendment 13.** It was ``"sip"`` by
    default, and a default is silently overridable at any call site. The
    measured cost of taking the wrong branch is a feed carrying a **median
    0.027761 of consolidated first-5-minute volume over `n = 100` pairs** —
    bars that look entirely normal and are wrong about the market. The feed is
    now required at the call site **and** checked against
    ``CONFIG.consolidated_feed`` here.
    """
    require_consolidated_feed(feed, f"alpaca_minute_bars({ticker})")
    return _alpaca_bars_url(store, ticker, start_iso, end_iso, feed, limit, page_token)


def alpaca_minute_bars_on_feed(
    store: CredentialStore,
    ticker: str,
    start_iso: str,
    end_iso: str,
    *,
    feed: str,
    tape_control_reason: str,
    limit: int = 10000,
    page_token: str | None = None,
) -> VendorRequest:
    """The **only** builder that may request a non-consolidated feed.

    It exists for one registered purpose: the **tape control** of A.1 TASK 4,
    which must request the single-venue feed in order to measure how far it
    sits from the consolidated one. Amendment 7 registered that branch; this
    builder is where it is allowed to happen, and it **demands a stated
    reason** so a later reader meets the justification at the call site rather
    than having to reconstruct it.
    """
    if not tape_control_reason.strip():
        raise TapeFeedError(
            f"alpaca_minute_bars_on_feed({ticker}, feed={feed!r}): refusing "
            "without a stated tape_control_reason. A request off the "
            "consolidated tape is a registered exception, and an exception "
            "with no reason recorded at its call site is a default wearing a "
            "different name."
        )
    return _alpaca_bars_url(store, ticker, start_iso, end_iso, feed, limit, page_token)


def _alpaca_bars_url(
    store: CredentialStore,
    ticker: str,
    start_iso: str,
    end_iso: str,
    feed: str,
    limit: int,
    page_token: str | None,
) -> VendorRequest:
    """URL construction only. **It decides nothing about which feed is right.**"""
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
        feed=feed,
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
