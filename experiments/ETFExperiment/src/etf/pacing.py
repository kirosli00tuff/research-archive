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

# MEASURED at A.1 Task 2 on 2026-08-28 and registered by Amendment 1.
#
# **No ceiling was found on any endpoint at or above this repository's own
# absolute floor of 1.0 s**: 96 requests across 8 endpoints, every one HTTP 200,
# with the escalation ladder bottoming out at 1.0 s on six of them and at 5.0 s
# on the flow table (deliberately gentler on a small publisher's site).
#
# So the operating pace is **twice the fastest verified-clean spacing** — the
# NPLExperiment pattern for an endpoint whose ceiling was not found, which is
# half the highest verified-clean rate rather than half a measured ceiling,
# because no ceiling exists to halve. The distinction is recorded rather than
# smoothed: these figures are bounded by what was probed, not by what the
# server would refuse.
#
# Highest verified-clean rates, per endpoint, n = 6 requests per rung:
#   flow.table 12.17/min · archive.availability 59.92/min ·
#   archive.timemap 21.28/min · venue.candleSnapshot 59.90/min ·
#   venue.fundingHistory 59.91/min · kraken.ohlc 58.73/min
#
# Per endpoint, never per host (solattn ADR-021). archive.availability and
# archive.timemap share a host and were measured separately; so did the three
# venue endpoints.
MEASURED_MIN_SPACING_S: Final[dict[str, float]] = {
    # Terms-of-service reconnaissance. Fetched once per host before anything
    # else, so the pace here only ever spaces one-shot probes.
    "meta.robots": 5.0,
    "meta.terms": 5.0,
    # Measured: 18 requests at 20 s, 10 s and 5 s, all 200. Operating at twice
    # the fastest clean spacing. The registered snapshot cadence asks for one
    # capture per 20 minutes, so this pace is never the binding constraint on
    # the collector; it bounds a catch-up burst, which is the only thing that
    # could ever approach it.
    "flow.table": 10.0,
    # Measured: 18 requests each at 5 s, 2 s and 1 s, all 200.
    "archive.timemap": 2.0,
    "archive.availability": 2.0,
    # Not measured. An unmeasured endpoint is not a licence to speed up, so it
    # keeps the slowest figure any archive endpoint carried before measurement.
    "archive.snapshot": 10.0,
    # Measured: 12 requests each at 2 s and 1 s, all 200.
    "venue.candleSnapshot": 2.0,
    "venue.fundingHistory": 2.0,
    # Not measured on its own. It keeps the pre-measurement figure rather than
    # inheriting a sibling's, which is precisely the inference ADR-021 forbids.
    "venue.meta": 5.0,
    # Measured: 18 requests at 3 s, 1.5 s and 1 s, all 200.
    "kraken.ohlc": 2.0,
}

# The floor a caller cannot go below even by passing its own map.
ABSOLUTE_MIN_SPACING_S: Final = 1.0


class PacingUnknown(RuntimeError):
    """An endpoint with no registered pace. Refused rather than defaulted fast."""


def min_spacing_s(endpoint: str, overrides: dict[str, float] | None = None) -> float:
    """The registered pace for an endpoint. Raises rather than guessing a fast default."""
    table = {**MEASURED_MIN_SPACING_S, **(overrides or {})}
    if endpoint not in table:
        raise PacingUnknown(
            f"no measured pace registered for endpoint {endpoint!r}. "
            f"An unmeasured endpoint is not a licence to speed up; measure it at "
            f"A.1 Task 2 and register the figure before sending."
        )
    return max(table[endpoint], ABSOLUTE_MIN_SPACING_S)
