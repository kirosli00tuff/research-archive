"""The H5 retrospective deviation read (Task 3). Gated, and never a rate.

The venue serves no historical mark and no historical oracle in the same
row, so a **retrospective basis of the registered construction does not
exist** (Amendment H5-1 Change 2). What it does serve is `premium`, hourly,
in the same `fundingHistory` row as its timestamp: its own impact-price
deviation index. That is a **named secondary** series — reported in full,
sizing the census window, able to fire CLOSED and never VIABLE.

Because `premium` is a near-deterministic function of the funding rate, the
cohort gate is structural here rather than left to the caller: `fetch_series`
calls `require_ungated` before it sends anything, so a generating-sample,
fresh-plan, or H2-pair coin cannot reach this path at all.
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass

from npl.absence import Absent, is_absent
from npl.api import EP_FUNDING_HISTORY, funding_history_body
from npl.blindness import deviation_rows
from npl.callstate import CallState
from npl.clock import MS_PER_DAY
from npl.config import CONFIG, Config
from npl.h5.basis import BP
from npl.h5.calendar import session_tag_of_ms
from npl.h5.gate import Cohorts, require_ungated
from npl.venue import Venue

# The venue serves at most this many rows per fundingHistory page (measured
# 2026-08-28: exactly 500 on a 500-plus-hour window).
PAGE_ROWS = 500


@dataclass(frozen=True, slots=True)
class Observation:
    """One hourly deviation observation, tagged by underlying-market session."""

    coin: str
    time_ms: int
    session_tag: str
    deviation_bp: float | Absent


@dataclass(frozen=True, slots=True)
class Series:
    """One instrument's retrospective series, with its coverage and absences."""

    coin: str
    state: str
    pages_fetched: int
    observations: tuple[Observation, ...]
    first_time_ms: int | None
    last_time_ms: int | None
    covered_days: int

    @property
    def n(self) -> int:
        return sum(1 for o in self.observations if not is_absent(o.deviation_bp))


def covered_days_of(observations: tuple[Observation, ...]) -> int:
    """Distinct UTC days carrying at least one served observation."""
    return len({o.time_ms // MS_PER_DAY for o in observations if not is_absent(o.deviation_bp)})


def fetch_series(
    venue: Venue,
    coin: str,
    cohorts: Cohorts,
    start_ms: int,
    end_ms: int,
    cfg: Config = CONFIG,
) -> Series:
    """Page the deviation series over the registered window. Gated first.

    The gate runs before the first request, so a quarantined coin costs
    nothing and reaches nothing. Paging stops at the registered page budget,
    at a short page, or at the window's end — never on a silent retry.
    """
    require_ungated(coin, cohorts)
    observations: list[Observation] = []
    cursor = start_ms
    pages = 0
    state = CallState.NO_DATA.value
    while pages < cfg.h5_retro_page_budget and cursor < end_ms:
        outcome = venue.request(funding_history_body(coin, cursor, end_ms), EP_FUNDING_HISTORY)
        pages += 1
        if outcome.state is not CallState.STORED or outcome.body is None:
            state = outcome.state.value
            break
        rows = deviation_rows(outcome.body)
        if not rows:
            break
        state = CallState.STORED.value
        for row in rows:
            premium = row.premium
            deviation: float | Absent = premium * BP if isinstance(premium, float) else premium
            observations.append(
                Observation(
                    coin=coin,
                    time_ms=row.time_ms,
                    session_tag=session_tag_of_ms(row.time_ms),
                    deviation_bp=deviation,
                )
            )
        if len(rows) < PAGE_ROWS:
            break
        cursor = rows[-1].time_ms + 1
    frozen = tuple(observations)
    return Series(
        coin=coin,
        state=state,
        pages_fetched=pages,
        observations=frozen,
        first_time_ms=frozen[0].time_ms if frozen else None,
        last_time_ms=frozen[-1].time_ms if frozen else None,
        covered_days=covered_days_of(frozen),
    )


def by_session_tag(series: list[Series]) -> dict[str, list[float | Absent]]:
    """Pool every instrument's observations into the four registered tags."""
    pooled: dict[str, list[float | Absent]] = {}
    for one in series:
        for obs in one.observations:
            pooled.setdefault(obs.session_tag, []).append(obs.deviation_bp)
    return pooled


def run_retrospective(
    venue: Venue,
    coins: list[str],
    cohorts: Cohorts,
    start_ms: int,
    end_ms: int,
    progress: Callable[[str], None] = lambda _: None,
    cfg: Config = CONFIG,
) -> list[Series]:
    """Fetch every ungated coin's series. A gated coin never reaches here."""
    out: list[Series] = []
    for i, coin in enumerate(coins, start=1):
        out.append(fetch_series(venue, coin, cohorts, start_ms, end_ms, cfg))
        if i % 10 == 0:
            progress(f"retro {i}/{len(coins)}: {coin} n={out[-1].n} days={out[-1].covered_days}")
    return out
