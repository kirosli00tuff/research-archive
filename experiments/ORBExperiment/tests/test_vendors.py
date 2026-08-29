"""A.1 TASK 7 — the registered operating pace, pinned against its measurement.

A pace that is faster than its measurement licenses is the failure this file
exists to make impossible. Every endpoint with a **measured** ceiling must be
paced at **no more than half** of it; every endpoint without one must say so.
"""

from __future__ import annotations

import pytest

from orb.config import CONFIG
from orb.credentials import (
    ALPACA_API_KEY,
    ALPACA_SECRET_KEY,
    MASSIVE_API_KEY,
    CredentialStore,
)
from orb.vendors import (
    ALPACA,
    ALPACA_DOCUMENTED_PER_MINUTE,
    CONSERVATIVE_SPACING_S,
    MASSIVE,
    MASSIVE_DOCUMENTED_PER_MINUTE,
    MEASURED_CEILING_PER_MINUTE,
    PACE_BASIS,
    PROVISIONAL_DAILY_CAPS,
    alpaca_headers,
    alpaca_minute_bars,
    massive_delisted,
    massive_headers,
    massive_minute_bars,
    massive_reference,
)

SECRET = "SECRET-VALUE-FOR-TESTS-0123456789"


@pytest.fixture
def store() -> CredentialStore:
    return CredentialStore(
        {
            MASSIVE_API_KEY: SECRET,
            ALPACA_API_KEY: SECRET + "-A",
            ALPACA_SECRET_KEY: SECRET + "-B",
        }
    )


# --- the pace, against the measurement ------------------------------------


def test_every_paced_endpoint_has_a_recorded_basis() -> None:
    """A pace with no stated basis is a number nobody has to defend."""
    assert sorted(CONSERVATIVE_SPACING_S) == sorted(PACE_BASIS)
    assert sorted(CONSERVATIVE_SPACING_S) == sorted(MEASURED_CEILING_PER_MINUTE)
    assert all(basis.strip() for basis in PACE_BASIS.values())

    from orb.vendors import (
        MEASURED_BURST_REFUSAL,
        MEASURED_SUSTAINED_ADMITTED_PER_MINUTE,
    )

    assert sorted(CONSERVATIVE_SPACING_S) == sorted(MEASURED_BURST_REFUSAL)
    assert sorted(CONSERVATIVE_SPACING_S) == sorted(
        MEASURED_SUSTAINED_ADMITTED_PER_MINUTE
    )


def test_the_operating_pace_is_at_most_half_the_measured_ceiling() -> None:
    """Half the measured ceiling, per endpoint. Never faster."""
    too_fast: list[str] = []
    for endpoint, ceiling in MEASURED_CEILING_PER_MINUTE.items():
        if ceiling is None:
            continue
        operating_per_minute = 60.0 / CONSERVATIVE_SPACING_S[endpoint]
        if operating_per_minute > ceiling / 2.0 + 1e-9:
            too_fast.append(
                f"{endpoint}: {operating_per_minute:.3f}/min against a measured "
                f"ceiling of {ceiling}/min"
            )
    assert not too_fast, f"paced faster than the measurement licenses: {too_fast}"


def test_an_unreached_ceiling_is_none_and_not_a_large_number() -> None:
    """*The ceiling was not reached* is a different statement from *there is
    no ceiling*, and it is recorded as its own value.

    **Amendment 14 sharpened what this protects.** A refusal boundary on
    ``alpaca:bars`` *was* reached — 384 admitted in 55.96 s, the 385th refused
    `429` — but the whole escalation fit inside one rolling minute, so it is a
    **burst allowance**. Sending at the documented 200 per minute for 75.10 s,
    longer than one rolling minute, drew **0 refusals over n = 250**. The
    sustained ceiling is therefore **at or above 199.73 and not known exactly**,
    and the ceiling entry stays ``None``.

    **A lower bound must never be written into the ceiling dict.** That is the
    exact shape of the error ADR-026 was written against, running the other way.
    """
    from orb.vendors import (
        MEASURED_BURST_REFUSAL,
        MEASURED_SUSTAINED_ADMITTED_PER_MINUTE,
    )

    assert MEASURED_CEILING_PER_MINUTE["alpaca:bars"] is None
    assert "NOT reached" in PACE_BASIS["alpaca:bars"]

    burst = MEASURED_BURST_REFUSAL["alpaca:bars"]
    assert burst == (384, 55.96)
    floor = MEASURED_SUSTAINED_ADMITTED_PER_MINUTE["alpaca:bars"]
    assert floor == 199.73

    for endpoint, bound in MEASURED_SUSTAINED_ADMITTED_PER_MINUTE.items():
        if bound is None:
            continue
        assert MEASURED_CEILING_PER_MINUTE[endpoint] != bound, (
            f"{endpoint}: a sustained lower bound has been written into the "
            "ceiling dict, which is exactly the ADR-026 error in reverse"
        )


def test_the_operating_pace_is_at_most_half_a_sustained_lower_bound() -> None:
    """Where no ceiling was reached, the pace comes from what was **attempted**.

    ADR-026's rule, applied to a rate rather than to a refusal: an unreached
    ceiling licenses no assumption, so the pace is set from the **maximum rate
    actually sustained** — 199.73 per minute over 75.10 s with 0 refusals — and
    halved. Never from the documented figure, and never from a guess.
    """
    from orb.vendors import MEASURED_SUSTAINED_ADMITTED_PER_MINUTE

    too_fast: list[str] = []
    for endpoint, bound in MEASURED_SUSTAINED_ADMITTED_PER_MINUTE.items():
        if bound is None:
            continue
        operating = 60.0 / CONSERVATIVE_SPACING_S[endpoint]
        if operating > bound / 2.0 + 1e-9:
            too_fast.append(f"{endpoint}: {operating:.3f}/min against {bound}/min")
    assert not too_fast, f"paced faster than what was sustained: {too_fast}"


def test_an_unmeasured_endpoint_is_never_paced_faster_than_a_measured_sibling() -> None:
    """An unmeasured endpoint keeps its vendor's figure rather than a faster
    default: an unmeasured endpoint is not a licence to speed up.

    **Amendment 14 replaced a proxy with the rule.** The proxy was *every
    endpoint of a vendor shares one spacing*, which held only while **no**
    endpoint of either vendor had been measured on a rate. `alpaca:bars` now has
    a sustained lower bound and its three siblings do not, so the rule is stated
    directly: an endpoint with no rate measurement is paced **at least as slowly
    as the slowest measured endpoint of the same vendor**.
    """
    from orb.vendors import MEASURED_SUSTAINED_ADMITTED_PER_MINUTE

    def measured(endpoint: str) -> bool:
        return (
            MEASURED_CEILING_PER_MINUTE[endpoint] is not None
            or MEASURED_SUSTAINED_ADMITTED_PER_MINUTE[endpoint] is not None
        )

    offenders: list[str] = []
    for prefix in ("massive:", "alpaca:"):
        family = [k for k in CONSERVATIVE_SPACING_S if k.startswith(prefix)]
        measured_spacings = [CONSERVATIVE_SPACING_S[k] for k in family if measured(k)]
        if not measured_spacings:
            spacings = [CONSERVATIVE_SPACING_S[k] for k in family]
            assert min(spacings) == max(spacings), (prefix, spacings)
            continue
        slowest_measured = max(measured_spacings)
        for endpoint in family:
            if measured(endpoint):
                continue
            if CONSERVATIVE_SPACING_S[endpoint] < slowest_measured - 1e-9:
                offenders.append(
                    f"{endpoint} at {CONSERVATIVE_SPACING_S[endpoint]} s is faster "
                    f"than the slowest measured sibling at {slowest_measured} s"
                )
    assert not offenders, f"an unmeasured endpoint was sped up: {offenders}"


def test_the_massive_pace_also_respects_the_documented_limit() -> None:
    """Measured and documented agree here at 5/min; the pace clears both."""
    assert MASSIVE_DOCUMENTED_PER_MINUTE == 5
    assert (
        60.0 / CONSERVATIVE_SPACING_S["massive:aggs"] <= MASSIVE_DOCUMENTED_PER_MINUTE
    )


def test_the_alpaca_pace_clears_the_documented_limit_too() -> None:
    assert ALPACA_DOCUMENTED_PER_MINUTE == 200
    assert 60.0 / CONSERVATIVE_SPACING_S["alpaca:bars"] <= ALPACA_DOCUMENTED_PER_MINUTE


def test_every_registered_vendor_has_a_daily_cap() -> None:
    """An unregistered vendor has no cap and is refused outright."""
    assert set(PROVISIONAL_DAILY_CAPS) == {MASSIVE, ALPACA}
    assert PROVISIONAL_DAILY_CAPS[ALPACA] == 3000, (
        "Amendment 14 moved Alpaca's circuit breaker from 2,000 to 3,000; it is "
        "about 30 minutes of continuous use at the registered pace and is still "
        "not derived from any measured daily allowance, because none exists"
    )
    assert PROVISIONAL_DAILY_CAPS[MASSIVE] == 600
    assert all(cap > 0 for cap in PROVISIONAL_DAILY_CAPS.values())


# --- no credential ever reaches a URL -------------------------------------


def test_no_builder_places_a_credential_in_a_url(store: CredentialStore) -> None:
    """Every credential travels as a header. A URL is safe to record."""
    requests = [
        massive_reference(store),
        massive_delisted(store, delisted_after="2016-01-04"),
        massive_minute_bars(store, "AAPL", "2026-07-01", "2026-07-02"),
        alpaca_minute_bars(
            store,
            "AAPL",
            "2026-07-01T00:00:00Z",
            "2026-07-02T00:00:00Z",
            feed=CONFIG.consolidated_feed,
        ),
    ]
    for request in requests:
        assert SECRET not in request.url, request.pace_key


def test_the_recordable_row_excludes_headers_by_construction(
    store: CredentialStore,
) -> None:
    row = massive_reference(store).as_row()
    assert set(row) == {"vendor", "pace_key", "url", "feed"}
    assert "headers" not in row
    assert row["feed"] is None, "a reference endpoint has no feed concept"

    bars = alpaca_minute_bars(
        store,
        "AAPL",
        "2026-07-01T00:00:00Z",
        "2026-07-02T00:00:00Z",
        feed=CONFIG.consolidated_feed,
    )
    assert bars.as_row()["feed"] == CONFIG.consolidated_feed, (
        "the feed travels on the request so a manifest cannot omit it"
    )


def test_massive_authenticates_by_bearer_header(store: CredentialStore) -> None:
    headers = massive_headers(store)
    assert headers["Authorization"] == f"Bearer {SECRET}"


def test_alpaca_authenticates_by_two_headers(store: CredentialStore) -> None:
    headers = alpaca_headers(store)
    assert headers["APCA-API-KEY-ID"] == SECRET + "-A"
    assert headers["APCA-API-SECRET-KEY"] == SECRET + "-B"


def test_a_missing_credential_refuses_rather_than_sending_unauthenticated() -> None:
    from orb.credentials import CredentialMissingError

    empty = CredentialStore({})
    with pytest.raises(CredentialMissingError):
        massive_reference(empty)
    with pytest.raises(CredentialMissingError):
        alpaca_minute_bars(
            empty,
            "AAPL",
            "2026-07-01T00:00:00Z",
            "2026-07-02T00:00:00Z",
            feed=CONFIG.consolidated_feed,
        )


def test_the_delisted_builder_pages_by_cursor_without_rebuilding_the_query(
    store: CredentialStore,
) -> None:
    """A cursor URL is followed verbatim; a rebuilt query would lose the cursor."""
    cursor = "https://api.polygon.io/v3/reference/tickers?cursor=ABC"
    assert massive_delisted(store, cursor_url=cursor).url == cursor


# --- Amendment 13 — the tape is required at the call site -------------------


def test_a_bar_request_on_the_single_venue_feed_is_refused(
    store: CredentialStore,
) -> None:
    """The single-venue feed carries a **median 0.027761** of the consolidated tape.

    A.1 TASK 4, `n = 100` session-ticker pairs, IQR [0.021200, 0.037068], with
    **every pair below the registered 0.20 single-venue threshold**. The bars it
    serves are real bars — a real high, a real low, a real volume — so a request
    that took this branch would produce a narrower opening range, a different
    trigger minute, a different relative-volume ranking, and **no error
    anywhere**. That invisibility is what this refusal is for.
    """
    from orb.vendors import MEASURED_SINGLE_VENUE_FEED, TapeFeedError

    with pytest.raises(TapeFeedError, match=r"0\.027761"):
        alpaca_minute_bars(
            store,
            "AAPL",
            "2026-07-01T00:00:00Z",
            "2026-07-02T00:00:00Z",
            feed=MEASURED_SINGLE_VENUE_FEED,
        )


def test_a_bar_request_with_no_feed_at_all_is_refused(store: CredentialStore) -> None:
    """``feed`` carries no default, so omitting it is a TypeError, not a guess."""
    with pytest.raises(TypeError):
        alpaca_minute_bars(  # type: ignore[call-arg]
            store, "AAPL", "2026-07-01T00:00:00Z", "2026-07-02T00:00:00Z"
        )


def test_the_tape_control_builder_demands_a_stated_reason(
    store: CredentialStore,
) -> None:
    """A registered exception with no reason at its call site is a default renamed."""
    from orb.vendors import (
        MEASURED_SINGLE_VENUE_FEED,
        TapeFeedError,
        alpaca_minute_bars_on_feed,
    )

    with pytest.raises(TapeFeedError, match="stated tape_control_reason"):
        alpaca_minute_bars_on_feed(
            store,
            "AAPL",
            "2026-07-01T00:00:00Z",
            "2026-07-02T00:00:00Z",
            feed=MEASURED_SINGLE_VENUE_FEED,
            tape_control_reason="   ",
        )

    allowed = alpaca_minute_bars_on_feed(
        store,
        "AAPL",
        "2026-07-01T00:00:00Z",
        "2026-07-02T00:00:00Z",
        feed=MEASURED_SINGLE_VENUE_FEED,
        tape_control_reason="Amendment 7 tape control, measured against the tape",
    )
    assert f"feed={MEASURED_SINGLE_VENUE_FEED}" in allowed.url
    assert allowed.feed == MEASURED_SINGLE_VENUE_FEED
