"""The forward H5 daily snapshot (Task 4). Runs last, yields to H2, zero dollars.

One pass per day, riding the existing daily pass under the measured pacing:
`perpDexs`, one `meta` and one `metaAndAssetCtxs` per HIP-3 dex, then one
`fundingHistory` service probe and one `l2Book` per **live** resolved
instrument (Amendment H5-2 Change 1 — a delisted instrument is enumerated
and recorded but not re-probed, because it has no market to probe).

Two protections keep it from displacing H2 work, neither of them a promise:
it is invoked last in the daily pass, and it refuses to start once the day's
ledger spend has reached the H2 soft budget. Its own per-pass cap is checked
as arithmetic before anything is sent.
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import asdict, dataclass
from pathlib import Path

from npl.clock import iso_z, now_utc, utc_ms
from npl.config import CONFIG, Config
from npl.h5.calendar import session_tag_of_ms
from npl.h5.census import InstrumentRow, run_census
from npl.h5.coverage import PassCoverage, coverage_of
from npl.h5.gate import Cohorts
from npl.h5.spend import daily_pass_budget, refuse_over_h5_cap
from npl.h5.stores import h5_store
from npl.ledger.requests import RequestLedger
from npl.paths import H5_SNAPSHOTS
from npl.venue import Venue


class H5YieldedToH2(RuntimeError):
    """The day's spend reached the H2 soft budget. H5 postpones, never displaces."""


@dataclass(frozen=True, slots=True)
class PassResult:
    """One forward pass: what was collected, what it cost, what it covered."""

    pass_id: str
    coverage: PassCoverage
    requests_charged: int
    ledger_day_before: int
    ledger_day_after: int


def require_headroom(ledger: RequestLedger, soft_budget: int, day: str) -> None:
    """H5 runs only while the day still has H2 headroom. Refused loudly, not silently."""
    spent = ledger.spent_on(day)
    if spent >= soft_budget:
        raise H5YieldedToH2(
            f"{spent} requests charged on {day} have reached the H2 soft budget of "
            f"{soft_budget}. H5 postpones to tomorrow rather than competing with H2 "
            f"work; nothing was sent."
        )


def record_yield(reason: str, store_path: Path = H5_SNAPSHOTS) -> None:
    """A postponement is a recorded state, not a swallowed exception."""
    h5_store(store_path).append({"kind": "pass_yielded", "at": iso_z(now_utc()), "reason": reason})


def run_daily_pass(
    venue: Venue,
    ledger: RequestLedger,
    cohorts: Cohorts,
    soft_budget: int,
    expected_dexs: int = 10,
    expected_instruments: int = 151,
    store_path: Path = H5_SNAPSHOTS,
    progress: Callable[[str], None] = lambda _: None,
    cfg: Config = CONFIG,
) -> PassResult:
    """One forward H5 snapshot, charged, capped, and covered."""
    at = now_utc()
    day = at.date().isoformat()
    require_headroom(ledger, soft_budget, day)
    refuse_over_h5_cap(daily_pass_budget(expected_dexs, expected_instruments), cfg)

    before = ledger.spent_on(day)
    rows: list[InstrumentRow] = run_census(
        venue, cohorts, ledger_path=store_path, progress=progress, probe_live_only=True
    )
    after = ledger.spent_on(day)
    at_ms = rows[0].at_ms if rows else utc_ms(at)
    pass_id = rows[0].snapshot_id if rows else f"h5-pass-{iso_z(at)}"
    coverage = coverage_of(pass_id, at_ms, session_tag_of_ms(at_ms), rows)
    h5_store(store_path).append({"kind": "pass_coverage", **asdict(coverage)})
    return PassResult(
        pass_id=pass_id,
        coverage=coverage,
        requests_charged=after - before,
        ledger_day_before=before,
        ledger_day_after=after,
    )
