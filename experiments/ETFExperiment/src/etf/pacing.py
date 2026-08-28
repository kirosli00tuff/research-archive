"""Pacing is measured per endpoint and is never generalised across them.

The solattn ADR-021 lesson, learned there the expensive way: a measurement of
one endpoint is not evidence about another, even on the same host. Two
GeckoTerminal endpoints on one host held 6.0 s and 12.0 s respectively, and the
project's own earlier measurement of the first was exactly the kind of
"documentation" the measured-beats-documented rule warns about.

So the map below is keyed per **endpoint**, not per host, and every figure is
either measured at A.1 Task 2 or provisional and labelled so. An endpoint
nobody has measured keeps the conservative default rather than a fast one: an
unmeasured endpoint is not a licence to speed up.
"""

from __future__ import annotations

from typing import Final

# Provisional at A.0, before any network call. A.1 Task 2 measures each ceiling
# and this map is replaced by amendment with half the measured ceiling, further
# reduced wherever the recorded terms of service ask for it.
PROVISIONAL_MIN_SPACING_S: Final[dict[str, float]] = {
    # Terms-of-service reconnaissance. Fetched once per host before anything
    # else, so the pace here only ever spaces one-shot probes.
    "meta.robots": 5.0,
    "meta.terms": 5.0,
    "flow.table": 30.0,
    "archive.timemap": 10.0,
    "archive.availability": 10.0,
    "archive.snapshot": 10.0,
    "venue.candleSnapshot": 5.0,
    "venue.fundingHistory": 5.0,
    "venue.meta": 5.0,
    "kraken.ohlc": 5.0,
}

# The floor a caller cannot go below even by passing its own map.
ABSOLUTE_MIN_SPACING_S: Final = 1.0


class PacingUnknown(RuntimeError):
    """An endpoint with no registered pace. Refused rather than defaulted fast."""


def min_spacing_s(endpoint: str, overrides: dict[str, float] | None = None) -> float:
    """The registered pace for an endpoint. Raises rather than guessing a fast default."""
    table = {**PROVISIONAL_MIN_SPACING_S, **(overrides or {})}
    if endpoint not in table:
        raise PacingUnknown(
            f"no measured or provisional pace registered for endpoint {endpoint!r}. "
            f"An unmeasured endpoint is not a licence to speed up; measure it at "
            f"A.1 Task 2 and register the figure before sending."
        )
    return max(table[endpoint], ABSOLUTE_MIN_SPACING_S)
