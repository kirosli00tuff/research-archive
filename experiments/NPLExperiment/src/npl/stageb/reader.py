"""The sealed reader — the single registered blindness exemption.

Amendment 3 registers this module, alone in the repository, as the parser
of candle closes and unrestricted funding rates from the sealed raw
stores, with the Stage B CLI as its only importer — both held by AST pin.
Everything here implements Sections 3-7 and the Amendment 3 reading rules
verbatim: entry at the second daily close; exit at the close stamped
entry + H days, else the last served close at or before it; a positive
funding rate pays the short on constant notional; truncated instruments
valued at their last served close and retained; pending events excluded
per horizon with counts; controls valued by the same arithmetic with
symmetric truncation. It opens files already on disk and sends nothing.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

from npl.absence import (
    NO_CANDLES,
    NO_CONTROL_CANDIDATE,
    NO_FUNDING_ROWS,
    PENDING_HORIZON,
    Absent,
)
from npl.census import EVENT_HIP3
from npl.clock import MS_PER_DAY
from npl.config import CONFIG, Config
from npl.outcome import cost_round_trip_bp, net_short_decomposition
from npl.paths import FUNDING_DIR, OUTCOMES_DIR
from npl.stageb.preconditions import CohortEvent, ControlWindow, WindowReport
from npl.verdict import Cohort, EventNet

BANDS: tuple[str, ...] = ("low", "central", "high")


class ReadError(RuntimeError):
    """A sealed store did not have the shape the read requires. Loud, no guess."""


def _coin_dir(root: Path, coin: str) -> Path:
    return root / coin.replace(":", "_")


def read_window_closes(
    coin: str, entry_ms: int, outcomes_root: Path = OUTCOMES_DIR
) -> dict[int, float]:
    """Candle open t -> close price, from one sealed verdict window."""
    path = _coin_dir(outcomes_root, coin) / f"retro-candles-{entry_ms // MS_PER_DAY}.raw"
    if not path.exists():
        raise ReadError(f"sealed candle window missing at read time: {path}")
    parsed = json.loads(path.read_bytes())
    if not isinstance(parsed, list):
        raise ReadError(f"candle window {path} is not a list; refusing to guess")
    out: dict[int, float] = {}
    for row in parsed:
        if not isinstance(row, dict):
            raise ReadError(f"candle row in {path} is not an object; refusing to guess")
        out[int(row["t"])] = float(row["c"])
    return out


class FundingRates:
    """Per-coin (time, rate) pairs from the sealed archive pages, cached."""

    def __init__(self, root: Path = FUNDING_DIR) -> None:
        self._root = root
        self._cache: dict[str, tuple[tuple[int, float], ...]] = {}

    def rows(self, coin: str) -> tuple[tuple[int, float], ...]:
        if coin not in self._cache:
            directory = _coin_dir(self._root, coin)
            loaded: list[tuple[int, float]] = []
            if directory.exists():
                for page in sorted(directory.glob("page-*.raw")):
                    parsed = json.loads(page.read_bytes())
                    if not isinstance(parsed, list):
                        raise ReadError(f"funding page {page} is not a list; refusing to guess")
                    for row in parsed:
                        loaded.append((int(row["time"]), float(row["fundingRate"])))
            self._cache[coin] = tuple(sorted(loaded))
        return self._cache[coin]


@dataclass(frozen=True, slots=True)
class Valued:
    """One window's Section 4 terms at one horizon, before the cost term."""

    price_term: float
    funding_term: float
    funding_rows_n: int
    exit_open_ms: int


def value_window(
    closes: dict[int, float],
    funding: tuple[tuple[int, float], ...],
    entry_ms: int,
    horizon_days: int,
    truncation_close_ms: int | None,
) -> Valued | Absent:
    """The Amendment 3 reading rules for one window and horizon.

    Entry close is the candle opening at entry - 1d. Exit close is the last
    served close at or before entry + H days (the exact horizon candle when
    served, the truncation valuation otherwise). Funding sums served hourly
    rates in (entry, min(entry + H, truncation)], with its n.
    """
    entry_open = entry_ms - MS_PER_DAY
    end = entry_ms + horizon_days * MS_PER_DAY
    funding_end = min(end, truncation_close_ms) if truncation_close_ms is not None else end
    rates = [rate for t, rate in funding if entry_ms < t <= funding_end]
    entry_close = closes.get(entry_open)
    exit_opens = [t for t in closes if entry_open <= t <= end - MS_PER_DAY]
    if entry_close is None or not exit_opens:
        return NO_CANDLES
    exit_open = max(exit_opens)
    decomposition = net_short_decomposition(entry_close, closes[exit_open], rates, 0.0)
    return Valued(
        price_term=decomposition.price_term,
        funding_term=decomposition.funding_term,
        funding_rows_n=len(rates),
        exit_open_ms=exit_open,
    )


def _net(valued: Valued | Absent, round_trip_bp: float) -> float | Absent:
    if isinstance(valued, Absent):
        return valued
    return valued.price_term + valued.funding_term - round_trip_bp / 1e4


def _cost_class(dex: str) -> str:
    """Amendment 3 rule 5: the venue class comes from the instrument's dex."""
    return EVENT_HIP3 if dex else "vanilla"


def _coverage_absent(report: WindowReport, horizon_days: int, cfg: Config) -> Absent | None:
    """The registered underpowered exclusion, with the failing bar as reason."""
    covered = report.covered_30 if horizon_days == cfg.horizon_primary_days else report.covered_90
    if covered:
        return None
    candles = report.candles_30 if horizon_days == cfg.horizon_primary_days else report.candles_90
    if candles is None or candles.share() < cfg.min_outcome_coverage_candles:
        return NO_CANDLES
    return NO_FUNDING_ROWS


@dataclass(frozen=True, slots=True)
class CohortRead:
    """The full sealed read: one EventNet list per cost band, with counts."""

    events_low: tuple[EventNet, ...]
    events_central: tuple[EventNet, ...]
    events_high: tuple[EventNet, ...]
    pending_30: int
    pending_90: int
    funding_rows_30_total: int
    paired_h8_n: int
    paired_h8_mean_funding_diff: float
    paired_h8_mean_price_diff: float

    def by_band(self, band: str) -> tuple[EventNet, ...]:
        by = {
            "low": self.events_low,
            "central": self.events_central,
            "high": self.events_high,
        }
        if band not in by:
            raise ReadError(f"unregistered cost band {band!r}")
        return by[band]


def read_cohort(
    events: list[CohortEvent],
    controls: list[ControlWindow],
    windows: list[WindowReport],
    now_ms: int,
    outcomes_root: Path = OUTCOMES_DIR,
    funding: FundingRates | None = None,
    cfg: Config = CONFIG,
) -> CohortRead:
    """The single read: every registered event valued at every band.

    Coverage exclusions arrive from the precondition window reports; an
    uncovered window enters as a recorded absence (underpowered), never a
    number. Pending events are excluded per horizon and counted.
    """
    store = funding if funding is not None else FundingRates()
    event_reports = {(w.coin, w.entry_ms): w for w in windows if w.role == "event"}
    control_reports = {
        (w.role.removeprefix("control:"), w.coin, w.entry_ms): w
        for w in windows
        if w.role.startswith("control:")
    }
    control_by_event = {(c.event_coin, c.dex, c.entry_ms): c for c in controls}

    per_band: dict[str, list[EventNet]] = {band: [] for band in BANDS}
    pending_30 = pending_90 = 0
    funding_rows_30_total = 0
    h8_funding_diffs: list[float] = []
    h8_price_diffs: list[float] = []

    for event in sorted(events, key=lambda e: (e.coin, e.entry_ms)):
        report = event_reports.get((event.coin, event.entry_ms))
        if report is None:
            raise ReadError(f"no precondition window report for event {event.coin}")
        closes = read_window_closes(event.coin, event.entry_ms, outcomes_root)
        frows = store.rows(event.coin)

        horizon_values: dict[int, Valued | Absent] = {}
        for horizon in (cfg.horizon_primary_days, cfg.horizon_secondary_days):
            if not event.truncated_by_delisting and event.entry_ms + horizon * MS_PER_DAY > now_ms:
                horizon_values[horizon] = PENDING_HORIZON
                if horizon == cfg.horizon_primary_days:
                    pending_30 += 1
                else:
                    pending_90 += 1
                continue
            gated = _coverage_absent(report, horizon, cfg)
            if gated is not None:
                horizon_values[horizon] = gated
                continue
            horizon_values[horizon] = value_window(
                closes, frows, event.entry_ms, horizon, event.truncation_close_ms
            )
        value_30 = horizon_values[cfg.horizon_primary_days]
        value_90 = horizon_values[cfg.horizon_secondary_days]
        if isinstance(value_30, Valued):
            funding_rows_30_total += value_30.funding_rows_n

        control = control_by_event.get((event.coin, event.dex, event.entry_ms))
        control_30: Valued | Absent = NO_CONTROL_CANDIDATE
        control_90: Valued | Absent = NO_CONTROL_CANDIDATE
        if control is not None:
            control_report = control_reports.get(
                (event.coin, control.control_coin, control.entry_ms)
            )
            if control_report is None:
                raise ReadError(
                    f"no precondition window report for control {control.control_coin} "
                    f"of event {event.coin}"
                )
            control_closes = read_window_closes(
                control.control_coin, control.entry_ms, outcomes_root
            )
            control_frows = store.rows(control.control_coin)
            for horizon, slot in ((cfg.horizon_primary_days, 30), (cfg.horizon_secondary_days, 90)):
                gated = _coverage_absent(control_report, horizon, cfg)
                value: Valued | Absent
                if gated is not None:
                    value = gated
                else:
                    value = value_window(
                        control_closes,
                        control_frows,
                        control.entry_ms,
                        horizon,
                        control.truncation_close_ms,
                    )
                if slot == 30:
                    control_30 = value
                else:
                    control_90 = value

        if isinstance(value_30, Valued) and isinstance(control_30, Valued):
            h8_funding_diffs.append(value_30.funding_term - control_30.funding_term)
            h8_price_diffs.append(value_30.price_term - control_30.price_term)

        event_class = event.event_type if event.event_type == EVENT_HIP3 else "vanilla"
        control_class = _cost_class(control.dex) if control is not None else "vanilla"
        for band in BANDS:
            event_bp = cost_round_trip_bp(event_class, cfg, band)
            control_bp = cost_round_trip_bp(control_class, cfg, band)
            per_band[band].append(
                EventNet(
                    coin=event.coin,
                    event_type=event.event_type,
                    cohort=Cohort.RETRO,
                    truncated_by_delisting=event.truncated_by_delisting,
                    net_short_30=_net(value_30, event_bp),
                    net_short_90=_net(value_90, event_bp),
                    funding_term_30=(
                        value_30.funding_term if isinstance(value_30, Valued) else value_30
                    ),
                    price_term_30=(
                        value_30.price_term if isinstance(value_30, Valued) else value_30
                    ),
                    control_net_short_30=_net(control_30, control_bp),
                    control_net_short_90=_net(control_90, control_bp),
                )
            )

    n_pairs = len(h8_funding_diffs)
    return CohortRead(
        events_low=tuple(per_band["low"]),
        events_central=tuple(per_band["central"]),
        events_high=tuple(per_band["high"]),
        pending_30=pending_30,
        pending_90=pending_90,
        funding_rows_30_total=funding_rows_30_total,
        paired_h8_n=n_pairs,
        paired_h8_mean_funding_diff=(sum(h8_funding_diffs) / n_pairs) if n_pairs else 0.0,
        paired_h8_mean_price_diff=(sum(h8_price_diffs) / n_pairs) if n_pairs else 0.0,
    )
