"""Listing status (Amendment H5-2). Three fields must agree, or it is loud.

A delisted perpetual has no market: no open interest, no volume, no book.
Its mark is a frozen last value and its reference may keep moving against
it, so their difference measures the delisting, not a deviation. Such an
instrument is excluded from the contemporaneous universe and reported as a
named descriptive stratum beside every primary figure.

The rule is conjunctive on purpose. A one-flag exclusion trusts a single
field; requiring `isDelisted`, zero open interest and zero day volume to
agree makes it a measurement. Any other combination is `conflicting` and is
reported, never resolved here.
"""

from __future__ import annotations

from typing import Final

from npl.absence import Maybe, is_absent

STATUS_LIVE: Final = "live"
STATUS_DELISTED: Final = "excluded_delisted"
STATUS_CONFLICTING: Final = "conflicting"

LISTING_STATUSES: Final[tuple[str, ...]] = (STATUS_LIVE, STATUS_DELISTED, STATUS_CONFLICTING)


def listing_status(
    is_delisted: bool,
    open_interest: Maybe[float] | float | None,
    day_notional_volume: Maybe[float] | float | None,
) -> str:
    """The registered three-field rule. An absent field can never mean zero."""
    oi_zero = _is_exactly_zero(open_interest)
    vol_zero = _is_exactly_zero(day_notional_volume)
    if is_delisted and oi_zero and vol_zero:
        return STATUS_DELISTED
    if not is_delisted and not oi_zero and not vol_zero:
        return STATUS_LIVE
    return STATUS_CONFLICTING


def _is_exactly_zero(value: Maybe[float] | float | None) -> bool:
    """Only a served, exact zero counts. An absence is not a zero."""
    if value is None or is_absent(value):
        return False
    return float(value) == 0.0


def is_live(status: str) -> bool:
    return status == STATUS_LIVE
