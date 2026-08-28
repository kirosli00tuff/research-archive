"""Stage B.0 preconditions. Counts, timestamps, and hashes only — no value.

Every check here refuses loudly on failure, and nothing here can read an
outcome value: the sealed stores are opened through the blindness readers,
which serve t, T, time, and row counts only. The checks, in order: the
operator prior slot; sealed completeness (every event and control candle
window sealed and hash-verified, every funding archive advanced past its
verdict window); the coverage bars (candles >= 0.90, funding hours >= 0.95
inside each verdict window), with a failing window excluded underpowered
and counted; the effective N per co-primary against the registered
minimums; and the latch, which must not exist.
"""

from __future__ import annotations

import json
import sys
from dataclasses import asdict, dataclass
from hashlib import sha256
from pathlib import Path
from typing import Any

from npl.blindness import FundingRow, candle_times, funding_rows
from npl.census import CensusLedger, CensusRow
from npl.clock import MS_PER_DAY, MS_PER_HOUR, iso_z, now_utc
from npl.config import CONFIG, Config
from npl.coverage import WindowCoverage, candle_day_coverage, funding_hour_coverage
from npl.eligibility import entry_anchor_ms, resolve_event
from npl.ledger.append_only import AppendOnlyLedger
from npl.paths import FUNDING_DIR, OUTCOMES_DIR, PAIRS_LEDGER, REPORTS, ROOT, STATE_DIR
from npl.registration_check import require_operator_prior
from npl.seals import verify_seal

RETRO_PLAN = STATE_DIR / "retro_plan.jsonl"
STAGE_B_LATCH = STATE_DIR / "stage_b_read.json"
PRECONDITIONS_JSON = REPORTS / "stage_b" / "preconditions.json"
HASHES_B0_JSON = REPORTS / "stage_b" / "hashes_b0.json"

# The registered minimum effective N per co-primary (Section 0 verdict
# record, 2026-08-27): the smallest N from which exact power at the
# registered assumptions stays at or above 0.80. Pinned against
# npl.power.min_n_for_power by test.
MIN_N_P1 = 34
MIN_N_P2 = 103
MIN_N_P3 = 60

# The registered Stage A retro cohort (Section 0 verdict record).
REGISTERED_EVENT_N = 312
REGISTERED_PAIR_N = 176

# Every module the read will touch, hashed at B.0 and re-hashed at B.1.
# A diff in any B.0-hashed module after the B.1 re-hash voids the read
# authorization and requires an amendment.
READ_SURFACE: tuple[str, ...] = (
    "absence.py",
    "blindness.py",
    "callstate.py",
    "census.py",
    "clock.py",
    "config.py",
    "coverage.py",
    "eligibility.py",
    "intervals.py",
    "ledger/__init__.py",
    "ledger/append_only.py",
    "outcome.py",
    "paths.py",
    "power.py",
    "registration_check.py",
    "seals.py",
    "verdict.py",
    "stageb/__init__.py",
    "stageb/preconditions.py",
)


class PreconditionFailure(RuntimeError):
    """A Stage B precondition failed. The stage stops; nothing is read."""


@dataclass(frozen=True, slots=True)
class CohortEvent:
    """One registered retro event, reconstructed from plan and census."""

    coin: str
    dex: str
    event_type: str
    listing_open_ms: int
    entry_ms: int
    truncated_by_delisting: bool
    truncation_close_ms: int | None


@dataclass(frozen=True, slots=True)
class ControlWindow:
    """One assigned control's verdict window, from the pairs ledger."""

    event_coin: str
    control_coin: str
    dex: str
    entry_ms: int
    truncation_close_ms: int | None


def census_by_key(rows: list[CensusRow]) -> dict[tuple[str, str], CensusRow]:
    """First row per (coin, dex): the Stage A census pass is the registered basis."""
    out: dict[tuple[str, str], CensusRow] = {}
    for row in rows:
        out.setdefault((row.coin, row.dex), row)
    return out


def _truncation(row: CensusRow, entry_ms: int, cfg: Config) -> tuple[bool, int | None]:
    """Section 7: delisted before entry + 90d truncates at the last served close."""
    required_end = entry_ms + cfg.retro_history_required_days * MS_PER_DAY
    last_close = row.last_1d_close_ms
    if row.is_delisted and last_close is not None and last_close < required_end:
        return True, last_close
    return False, None


def reconstruct_cohort(
    census: list[CensusRow],
    plan_rows: list[dict[str, Any]],
    pair_rows: list[dict[str, Any]],
    cfg: Config = CONFIG,
) -> tuple[list[CohortEvent], list[ControlWindow]]:
    """The registered cohort from the plan, census, and pairs ledgers.

    A plan row is an event iff the Amendment 1 resolution of its census row
    reproduces its listing timestamp; every other plan row must be one of
    the queued control windows, cross-checked against the pairs ledger. A
    row matching neither is a loud failure, never a silent skip.
    """
    by_key = census_by_key(census)
    pair_windows = {(str(p["control_coin"]), int(p["entry_ms"])) for p in pair_rows}

    events: dict[tuple[str, str, int], CohortEvent] = {}
    for raw in plan_rows:
        if raw.get("kind") != "event":
            continue
        coin, dex = str(raw["coin"]), str(raw["dex"])
        listing = int(raw["listing_open_ms"])
        row = by_key.get((coin, dex))
        if row is None:
            raise PreconditionFailure(
                f"plan row for {coin!r} on dex {dex!r} has no census row; the plan and the "
                f"census disagree and nothing here guesses"
            )
        resolved = resolve_event(row, cfg)
        entry = entry_anchor_ms(listing, cfg)
        if resolved.event_listing_ms == listing:
            truncated, trunc_close = _truncation(row, entry, cfg)
            events.setdefault(
                (coin, dex, listing),
                CohortEvent(
                    coin=coin,
                    dex=dex,
                    event_type=resolved.event_type,
                    listing_open_ms=listing,
                    entry_ms=entry,
                    truncated_by_delisting=truncated,
                    truncation_close_ms=trunc_close,
                ),
            )
        elif (coin, entry) not in pair_windows:
            raise PreconditionFailure(
                f"plan row for {coin!r} at listing {listing} is neither a resolved event "
                f"(resolution gives {resolved.event_listing_ms}) nor a queued control "
                f"window in the pairs ledger"
            )

    controls: dict[tuple[str, str, int], ControlWindow] = {}
    for raw in pair_rows:
        control_coin = str(raw["control_coin"])
        event_coin = str(raw["event_coin"])
        dex = str(raw["dex"])
        entry = int(raw["entry_ms"])
        row = by_key.get((control_coin, dex))
        if row is None:
            raise PreconditionFailure(
                f"pair control {control_coin!r} on dex {dex!r} has no census row"
            )
        _, trunc_close = _truncation(row, entry, cfg)
        controls.setdefault(
            (event_coin, control_coin, entry),
            ControlWindow(
                event_coin=event_coin,
                control_coin=control_coin,
                dex=dex,
                entry_ms=entry,
                truncation_close_ms=trunc_close,
            ),
        )
    return list(events.values()), list(controls.values())


def _coin_dir(root: Path, coin: str) -> Path:
    return root / coin.replace(":", "_")


class FundingTimes:
    """Per-coin funding rows (times only), loaded once from the sealed pages."""

    def __init__(self, root: Path = FUNDING_DIR) -> None:
        self._root = root
        self._cache: dict[str, tuple[FundingRow, ...]] = {}

    def rows(self, coin: str) -> tuple[FundingRow, ...]:
        if coin not in self._cache:
            directory = _coin_dir(self._root, coin)
            loaded: list[FundingRow] = []
            if directory.exists():
                for page in sorted(directory.glob("page-*.raw")):
                    loaded.extend(funding_rows(page.read_bytes(), entry_ms=None))
            self._cache[coin] = tuple(sorted(loaded, key=lambda r: r.time_ms))
        return self._cache[coin]


@dataclass(frozen=True, slots=True)
class WindowReport:
    """One verdict window's completeness and coverage. Counts and times only."""

    key: str
    coin: str
    role: str
    entry_ms: int
    sealed: bool
    seal_verified: bool
    archive_last_ms: int | None
    archive_advanced: bool
    candles_30: WindowCoverage | None
    funding_30: WindowCoverage | None
    candles_90: WindowCoverage | None
    funding_90: WindowCoverage | None
    covered_30: bool
    covered_90: bool
    reasons: tuple[str, ...]


def assess_window(
    coin: str,
    role: str,
    entry_ms: int,
    truncation_close_ms: int | None,
    funding_store: FundingTimes,
    outcomes_root: Path = OUTCOMES_DIR,
    cfg: Config = CONFIG,
) -> WindowReport:
    """Completeness and the coverage bars for one sealed verdict window.

    A live window's funding archive must reach the last hourly stamp inside
    the 90-day window. A truncated window's feed ended with the instrument:
    the archive must exist, and the quantitative gate is the coverage bar
    over the truncated window.
    """
    reasons: list[str] = []
    path = _coin_dir(outcomes_root, coin) / f"retro-candles-{entry_ms // MS_PER_DAY}.raw"
    sealed = path.exists()
    verified = verify_seal(path) if sealed else False
    if not sealed:
        reasons.append("candle_window_not_sealed")
    elif not verified:
        reasons.append("candle_seal_mismatch")

    frows = funding_store.rows(coin)
    archive_last = frows[-1].time_ms if frows else None
    end_30 = entry_ms + cfg.horizon_primary_days * MS_PER_DAY
    end_90 = entry_ms + cfg.horizon_secondary_days * MS_PER_DAY
    if truncation_close_ms is not None:
        end_30 = min(end_30, truncation_close_ms)
        end_90 = min(end_90, truncation_close_ms)

    if truncation_close_ms is None:
        advanced = archive_last is not None and archive_last >= end_90 - MS_PER_HOUR
    else:
        advanced = archive_last is not None
    if not advanced:
        reasons.append("funding_archive_not_advanced")

    candles_30 = candles_90 = funding_30 = funding_90 = None
    covered_30 = covered_90 = False
    if sealed and verified:
        times = candle_times(path.read_bytes())
        start = entry_ms - MS_PER_DAY
        candles_30 = candle_day_coverage(times, start, end_30)
        candles_90 = candle_day_coverage(times, start, end_90)
        funding_30 = funding_hour_coverage(frows, entry_ms, end_30)
        funding_90 = funding_hour_coverage(frows, entry_ms, end_90)
        covered_30 = (
            candles_30.share() >= cfg.min_outcome_coverage_candles
            and funding_30.share() >= cfg.min_outcome_coverage_funding
        )
        covered_90 = (
            candles_90.share() >= cfg.min_outcome_coverage_candles
            and funding_90.share() >= cfg.min_outcome_coverage_funding
        )
        if not covered_30:
            reasons.append("underpowered_30d")
        if not covered_90:
            reasons.append("underpowered_90d")

    return WindowReport(
        key=f"{role}:{coin}@{entry_ms // MS_PER_DAY}",
        coin=coin,
        role=role,
        entry_ms=entry_ms,
        sealed=sealed,
        seal_verified=verified,
        archive_last_ms=archive_last,
        archive_advanced=advanced,
        candles_30=candles_30,
        funding_30=funding_30,
        candles_90=candles_90,
        funding_90=funding_90,
        covered_30=covered_30,
        covered_90=covered_90,
        reasons=tuple(reasons),
    )


def module_hashes(surface: tuple[str, ...] = READ_SURFACE, root: Path = ROOT) -> dict[str, str]:
    """sha256 of every module on the read surface. A missing module is loud."""
    out: dict[str, str] = {}
    for rel in surface:
        path = root / "src" / "npl" / rel
        if not path.exists():
            raise PreconditionFailure(f"read-surface module missing: {rel}")
        out[rel] = sha256(path.read_bytes()).hexdigest()
    return out


@dataclass(frozen=True, slots=True)
class PreconditionReport:
    """The B.0 verdict on whether the read may proceed. Figures carry their n."""

    checked_at: str
    operator_prior: tuple[float, str]
    events_total: int
    controls_total: int
    events_covered_30: int
    controls_covered_30: int
    events_covered_90: int
    controls_covered_90: int
    events_truncated: int
    effective_n_p1: int
    effective_n_p2: int
    effective_n_p3: int
    min_n: tuple[int, int, int]
    latch_absent: bool
    module_hashes: dict[str, str]
    shortfalls: tuple[str, ...]


def run_preconditions(
    census_rows: list[CensusRow],
    plan_rows: list[dict[str, Any]],
    pair_rows: list[dict[str, Any]],
    funding_store: FundingTimes,
    outcomes_root: Path = OUTCOMES_DIR,
    latch_path: Path = STAGE_B_LATCH,
    cfg: Config = CONFIG,
    registered_event_n: int = REGISTERED_EVENT_N,
    registered_pair_n: int = REGISTERED_PAIR_N,
    min_n: tuple[int, int, int] = (MIN_N_P1, MIN_N_P2, MIN_N_P3),
) -> tuple[PreconditionReport, list[WindowReport]]:
    """Every B.0 check, in the registered order, refusing loudly on failure."""
    prior = require_operator_prior()

    events, controls = reconstruct_cohort(census_rows, plan_rows, pair_rows, cfg)
    if len(events) != registered_event_n or len(controls) != registered_pair_n:
        raise PreconditionFailure(
            f"cohort reconstruction produced {len(events)} events and {len(controls)} "
            f"control windows against the registered {registered_event_n} and "
            f"{registered_pair_n}; the stage stops rather than reading a different sample"
        )

    windows: list[WindowReport] = []
    event_covered: dict[tuple[str, str, int], bool] = {}
    shortfalls: list[str] = []
    for event in sorted(events, key=lambda e: (e.coin, e.entry_ms)):
        report = assess_window(
            event.coin,
            "event",
            event.entry_ms,
            event.truncation_close_ms,
            funding_store,
            outcomes_root,
            cfg,
        )
        windows.append(report)
        event_covered[(event.coin, event.dex, event.entry_ms)] = report.covered_30
        if not (report.sealed and report.seal_verified and report.archive_advanced):
            shortfalls.append(f"{report.key}: {', '.join(report.reasons)}")

    control_covered: dict[tuple[str, str, int], bool] = {}
    for control in sorted(controls, key=lambda c: (c.control_coin, c.entry_ms)):
        report = assess_window(
            control.control_coin,
            f"control:{control.event_coin}",
            control.entry_ms,
            control.truncation_close_ms,
            funding_store,
            outcomes_root,
            cfg,
        )
        windows.append(report)
        control_covered[(control.event_coin, control.dex, control.entry_ms)] = report.covered_30
        if not (report.sealed and report.seal_verified and report.archive_advanced):
            shortfalls.append(f"{report.key}: {', '.join(report.reasons)}")

    if shortfalls:
        raise PreconditionFailure(
            "sealed completeness failed on "
            + f"{len(shortfalls)} of {len(windows)} windows: "
            + "; ".join(shortfalls[:20])
            + ("; ..." if len(shortfalls) > 20 else "")
            + ". The dated resume condition is the next 01:40Z daily pass."
        )

    n_events_covered = sum(1 for covered in event_covered.values() if covered)
    n_pairs_covered = sum(
        1 for key, covered in control_covered.items() if covered and event_covered.get(key, False)
    )
    effective = (n_events_covered, n_events_covered, n_pairs_covered)
    for name, n, minimum in zip(("P1", "P2", "P3"), effective, min_n, strict=True):
        if n < minimum:
            raise PreconditionFailure(
                f"effective N for {name} is {n}, below the registered minimum {minimum}: "
                f"the read is refused"
            )

    if latch_path.exists():
        raise PreconditionFailure(
            f"the latch {latch_path} exists: the single registered read is already "
            f"spent. Stop and report; recovery works from partial artifacts under an "
            f"amendment, never a silent re-run."
        )

    report_out = PreconditionReport(
        checked_at=iso_z(now_utc()),
        operator_prior=prior,
        events_total=len(events),
        controls_total=len(controls),
        events_covered_30=n_events_covered,
        controls_covered_30=sum(1 for covered in control_covered.values() if covered),
        events_covered_90=sum(1 for w in windows if w.role == "event" and w.covered_90),
        controls_covered_90=sum(
            1 for w in windows if w.role.startswith("control:") and w.covered_90
        ),
        events_truncated=sum(1 for e in events if e.truncated_by_delisting),
        effective_n_p1=effective[0],
        effective_n_p2=effective[1],
        effective_n_p3=effective[2],
        min_n=min_n,
        latch_absent=not latch_path.exists(),
        module_hashes=module_hashes(),
        shortfalls=tuple(shortfalls),
    )
    return report_out, windows


def main() -> int:
    census_rows = CensusLedger().rows()
    plan_rows = AppendOnlyLedger(RETRO_PLAN).require_intact()
    pair_rows = AppendOnlyLedger(PAIRS_LEDGER).require_intact()
    try:
        report, windows = run_preconditions(census_rows, plan_rows, pair_rows, FundingTimes())
    except PreconditionFailure as exc:
        print(f"PRECONDITION FAILURE: {exc}", file=sys.stderr)
        return 1
    PRECONDITIONS_JSON.parent.mkdir(parents=True, exist_ok=True)
    PRECONDITIONS_JSON.write_text(
        json.dumps(
            {"report": asdict(report), "windows": [asdict(w) for w in windows]},
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )
    HASHES_B0_JSON.write_text(
        json.dumps(report.module_hashes, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(
        f"preconditions PASS at {report.checked_at}: events {report.events_total} "
        f"(covered_30 {report.events_covered_30}, truncated {report.events_truncated}), "
        f"controls {report.controls_total} (covered_30 {report.controls_covered_30}), "
        f"effective N {report.effective_n_p1}/{report.effective_n_p2}/"
        f"{report.effective_n_p3} against minimums {report.min_n}, latch absent, "
        f"operator prior {report.operator_prior[0]} ({report.operator_prior[1]})"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
