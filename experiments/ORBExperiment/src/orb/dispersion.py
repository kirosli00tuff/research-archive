"""A.1 TASK 5 — the carve-out dispersion writer. **Built dark, run sealed.**

**This is a latched module and a sealed writer at once.** It reads priced bar
fields — an opening-range rule is a statement about highs and lows, so it cannot
be blind — and it **returns exactly two scalars to any caller**:

1. the **standard deviation of net PnL per share** across the registered trades;
2. the **realized trigger rate**.

Everything else it returns is an **integer count**, present because standing rule
13 requires every figure to travel with its n. **It returns no trade, no return
series, no per-name figure, no ranking, no session list and no bar value.**
Pinned by ``tests/test_guards.py::test_the_dispersion_writer_returns_two_scalars``.

**Why a standard deviation and not a mean.** The mean net PnL **is** the outcome
this repository is blind to. A dispersion is not: it sizes a net edge against a
modeled cost, which is the one thing Section 9 says E2's power computation needs.
So the two-scalar contract is not merely a limit on the interface — **it keeps
the outcome sealed even inside a region the carve-out permits reading.**

**Why per share rather than per trade in dollars.** Section 4 registers a risk
fraction (0.25 percent of equity) but **no equity level**, so a per-trade dollar
figure is only defined up to an arbitrary scale. Per share is invariant to it,
and it is the unit the carried gross edge (**0.070 USD/share**, C-6) and the
measured round-trip cost (**≈0.0386/share on a close exit, ≈0.0686 on a stop
exit**, Amendment 3) are already expressed in — so the ratio E2 needs is formed
in one consistent unit rather than across two.

**The region it reads.** Only the amended carve-out of Amendment 11. Every bar is
passed through ``orb.preperiod.require_pre_period``, the two-sided check, and
carries ``Provenance.POST_HOLDOUT``, which `orb.bars` validates at construction.
A bar inside the sealed window raises rather than being silently dropped.

**What it is never pointed at.** The in-sample and holdout windows, before the
Stage C and Stage D latches respectively. That is enforced by the boundary
check above, not by this sentence.

**It has no filesystem.** The caller supplies a loader and a session list, and
this module reaches for nothing else. A module that can read a path can read a
path outside the carve-out.
"""

from __future__ import annotations

import json
import math
from collections.abc import Callable, Iterator, Mapping, Sequence
from dataclasses import dataclass
from datetime import datetime
from itertools import pairwise
from typing import Final, final

from orb.bars import Bar, Provenance
from orb.calendar import Session
from orb.config import CONFIG
from orb.costs import Band, CostModel, Leg, Side
from orb.preperiod import require_pre_period
from orb.signal import (
    Trigger,
    close_exit_c,
    find_trigger,
    opening_range,
    stop_hit,
)
from orb.universe import (
    Candidate,
    first_five_minute_volume,
    relative_volume,
    select,
)

CENT: Final[int] = 100
BAR_ARRAY_KEY: Final[str] = "bars"
"""The envelope key the primary vendor carries its bar array under."""


class DispersionInputError(ValueError):
    """Raised when the inputs cannot support the registered computation."""


@final
@dataclass(frozen=True, slots=True)
class CarveOutDispersion:
    """**Two scalars and their counts. Nothing else leaves this module.**

    ``net_pnl_per_share_stdev`` and ``trigger_rate`` are the only ``float``
    fields, and the guard asserts that. Every other field is an ``int`` count so
    that each scalar travels with its n, per standing rule 13.
    """

    net_pnl_per_share_stdev: float
    trigger_rate: float

    sessions_evaluated: int
    name_sessions_evaluated: int
    name_sessions_triggered: int
    name_sessions_ambiguous: int
    trades_priced: int
    trades_refused_by_cost_model: int
    trades_below_one_share: int
    stop_exits: int
    close_exits: int
    bars_read: int
    tickers_with_bars: int


@final
@dataclass(frozen=True, slots=True)
class CarveOutExecutionMix:
    """**Four scalars and their denominators. Nothing else leaves this module.**

    Registered by **Amendment 20**. The four the operator named are
    ``stop_exit_share``, ``ambiguous_rate``,
    ``mean_pessimistic_shift_usd_per_share`` and ``sessions_used`` — three
    ``float`` measurements and one ``int`` count.

    **The remaining fields are integer denominators and standing rule 13
    requires them.** A rate without its n is not a figure this repository is
    allowed to report, and the deviation is named in Amendment 20 rather than
    taken quietly. **No field is a trade, a series, a per-name figure or a bar
    value**, which is what the four-scalar contract is actually protecting.
    """

    stop_exit_share: float
    ambiguous_rate: float
    mean_pessimistic_shift_usd_per_share: float

    sessions_used: int
    name_sessions_evaluated: int
    name_sessions_ambiguous: int
    name_sessions_triggered: int
    trades_with_a_resolved_exit: int
    stop_exits: int
    close_exits: int
    trades_with_an_unresolved_exit: int
    bars_read: int
    tickers_with_bars: int


@final
@dataclass(frozen=True, slots=True)
class CarveOutSlippageBand:
    """**Summary statistics per leg and the resulting band. Nothing else.**

    Registered by **Amendment 26**. Every ``float`` here is a **summary
    statistic of a distribution** or a **band figure derived from two of them**.
    **No field is a trade, a per-name figure or a bar value**, and the guard
    pins the exact list.

    **The assignment is fixed before any of these are computed**: the **median**
    of a leg's per-trade slippage distribution is the **central** band end, and
    the **90th percentile** is the **pessimistic** end. Amendment 26 records
    why, and the assignment does not depend on which produces a favourable
    shift.
    """

    # --- entry leg ---
    entry_overshoot_mean: float
    entry_overshoot_median: float
    entry_overshoot_p90: float
    entry_half_spread_mean: float
    entry_half_spread_median: float
    entry_half_spread_p90: float
    entry_slippage_mean: float
    entry_slippage_median: float
    entry_slippage_p90: float

    # --- stop-exit leg ---
    stop_overshoot_mean: float
    stop_overshoot_median: float
    stop_overshoot_p90: float
    stop_half_spread_mean: float
    stop_half_spread_median: float
    stop_half_spread_p90: float
    stop_slippage_mean: float
    stop_slippage_median: float
    stop_slippage_p90: float

    # --- close-exit leg ---
    close_slippage_mean: float
    close_slippage_median: float
    close_slippage_p90: float

    # --- the resulting band, and the shift it implies ---
    measured_entry_central: float
    measured_entry_pessimistic: float
    measured_stop_central: float
    measured_stop_pessimistic: float
    measured_close_central: float
    measured_close_pessimistic: float
    stop_exit_share: float
    measured_shift_usd_per_share: float

    # --- integer denominators, required by standing rule 13 ---
    sessions_used: int
    name_sessions_evaluated: int
    entry_observations: int
    entry_gapped_through: int
    entry_crossed_intrabar: int
    entry_quote_minutes_served: int
    entry_quote_minutes_refused: int
    entry_quote_minutes_truncated: int
    stop_observations: int
    stop_gapped_through: int
    stop_crossed_intrabar: int
    stop_quote_minutes_served: int
    stop_quote_minutes_refused: int
    close_observations: int
    close_without_an_official_print: int
    bars_read: int
    tickers_with_bars: int


@final
@dataclass(frozen=True, slots=True)
class CarveOutFloorScanRow:
    """One price floor of the H1b feasibility scan. **Counts and ratios only.**

    Registered by **Amendment 27**. **It carries no verdict and no power
    figure**, because H1b is `REGISTERED_NOT_OPEN` and computing either would be
    opening it.
    """

    price_floor_usd: float
    mean_relative_volume_of_selection: float
    dispersion_usd_per_share: float
    entry_overshoot_median: float
    central_mean_usd_per_share: float
    shift_usd_per_share: float
    central_mean_to_shift_ratio: float

    eligible_name_sessions: int
    selected_name_sessions: int
    sessions_with_a_full_selection: int
    sessions_evaluated: int
    triggered_trades: int
    priced_trades: int


@final
@dataclass(frozen=True, slots=True)
class _NameSession:
    """One name on one session. **Private. Never returned to a caller.**"""

    ticker: str
    session_index: int
    first5_volume: int
    session_volume: int
    session_open_c: int
    session_high_c: int
    session_low_c: int
    session_close_c: int
    trigger: Trigger
    entry_c: int | None
    stop_c: int | None
    side: Side | None
    exit_c: int | None
    exit_leg: Leg | None

    # --- A.3 TASK 2 execution detail. Private, and it stays private. ---
    trigger_boundary_c: int | None
    trigger_ms: int | None
    trigger_bar_open_c: int | None
    stop_ms: int | None
    stop_bar_open_c: int | None
    last_exit_window_close_c: int | None
    official_close_c: int | None


def _to_cents(value: object) -> int | None:
    if isinstance(value, bool) or not isinstance(value, int | float):
        return None
    return round(float(value) * CENT)


def _stamp_ms(raw: object) -> int | None:
    """A bar timestamp in epoch milliseconds. A **readable** field.

    Never a naive timestamp: a stamp carrying no zone is refused rather than
    assumed UTC, per standing rule 14.
    """
    if isinstance(raw, bool):
        return None
    if isinstance(raw, int):
        return raw
    if isinstance(raw, str):
        try:
            moment = datetime.fromisoformat(raw.replace("Z", "+00:00"))
        except ValueError:
            return None
        return None if moment.tzinfo is None else int(moment.timestamp() * 1000)
    return None


def _bars_from_payloads(payloads: Sequence[bytes], context: str) -> list[Bar]:
    """Parse vendor bytes into typed bars. **Enforces the carve-out per bar.**"""
    out: list[Bar] = []
    for payload in payloads:
        try:
            envelope = json.loads(payload)
        except (json.JSONDecodeError, UnicodeDecodeError):
            continue
        if not isinstance(envelope, dict):
            continue
        rows = envelope.get(BAR_ARRAY_KEY)
        if not isinstance(rows, list):
            continue
        for row in rows:
            if not isinstance(row, dict):
                continue
            stamp = _stamp_ms(row.get("t"))
            if stamp is None:
                continue
            require_pre_period(stamp, context)
            o = _to_cents(row.get("o"))
            h = _to_cents(row.get("h"))
            low = _to_cents(row.get("l"))
            c = _to_cents(row.get("c"))
            v = row.get("v")
            if None in (o, h, low, c) or not isinstance(v, int | float):
                continue
            assert o is not None and h is not None and low is not None
            assert c is not None
            if h < low or not (low <= o <= h) or not (low <= c <= h):
                continue
            out.append(
                Bar(
                    timestamp_ms=stamp,
                    open_c=o,
                    high_c=h,
                    low_c=low,
                    close_c=c,
                    volume=int(v),
                    provenance=Provenance.POST_HOLDOUT,
                )
            )
    out.sort(key=lambda b: b.timestamp_ms)
    return out


def _scan_ticker(
    ticker: str, bars: Sequence[Bar], sessions: Sequence[Session]
) -> list[_NameSession]:
    """Section 2 inputs and the Section 3 setup, per session. **Private.**"""
    rows: list[_NameSession] = []
    for index, session in enumerate(sessions):
        open_ms, range_end_ms = session.opening_range_utc()
        exit_start_ms, exit_end_ms = session.close_exit_utc()
        inside = [b for b in bars if open_ms <= b.timestamp_ms < exit_end_ms]
        if not inside:
            continue

        first5 = first_five_minute_volume(inside, (open_ms, range_end_ms))
        range_ = opening_range(inside, (open_ms, range_end_ms))
        if range_ is None or first5 <= 0:
            continue

        setup = find_trigger(inside, range_, range_end_ms)
        exit_price: int | None = None
        leg: Leg | None = None
        boundary_c: int | None = None
        trigger_open_c: int | None = None
        stopped_at: int | None = None
        stop_open_c: int | None = None
        if setup.trigger in (Trigger.LONG, Trigger.SHORT):
            assert setup.triggered_at_ms is not None
            boundary_c = range_.high_c if setup.side is Side.LONG else range_.low_c
            trigger_bar = next(
                (b for b in inside if b.timestamp_ms == setup.triggered_at_ms), None
            )
            trigger_open_c = None if trigger_bar is None else trigger_bar.open_c
            stopped_at = stop_hit(inside, setup, setup.triggered_at_ms)
            if stopped_at is not None:
                stop_bar = next(
                    (b for b in inside if b.timestamp_ms == stopped_at), None
                )
                stop_open_c = None if stop_bar is None else stop_bar.open_c
                exit_price = setup.stop_c
                leg = Leg.STOP_EXIT
            else:
                exit_price = close_exit_c(inside, (exit_start_ms, exit_end_ms))
                leg = Leg.CLOSE_EXIT

        # The registered exit prices at the last bar of the 15:55-15:59 window.
        # A real market-on-close order fills at the official closing print, and
        # the gap between them is the close leg's realized slippage. Both are
        # read here so the leg can be measured rather than assumed.
        window_close_c = close_exit_c(inside, (exit_start_ms, exit_end_ms))
        official = [
            b for b in bars if exit_end_ms <= b.timestamp_ms < exit_end_ms + 120_000
        ]
        official_close_c = (
            min(official, key=lambda b: b.timestamp_ms).close_c if official else None
        )

        first_bar = min(inside, key=lambda b: b.timestamp_ms)
        rows.append(
            _NameSession(
                ticker=ticker,
                session_index=index,
                first5_volume=first5,
                session_volume=sum(b.volume for b in inside),
                session_open_c=first_bar.open_c,
                session_high_c=max(b.high_c for b in inside),
                session_low_c=min(b.low_c for b in inside),
                session_close_c=max(inside, key=lambda b: b.timestamp_ms).close_c,
                trigger=setup.trigger,
                entry_c=setup.entry_c,
                stop_c=setup.stop_c,
                side=setup.side,
                exit_c=exit_price,
                exit_leg=leg,
                trigger_boundary_c=boundary_c,
                trigger_ms=setup.triggered_at_ms,
                trigger_bar_open_c=trigger_open_c,
                stop_ms=stopped_at,
                stop_bar_open_c=stop_open_c,
                last_exit_window_close_c=window_close_c,
                official_close_c=official_close_c,
            )
        )
    return rows


def _atr_14_c(history: Sequence[_NameSession]) -> float:
    """The 14-session average true range, in cents, from session extremes."""
    window = list(history)[-CONFIG.relvol_lookback_sessions :]
    if len(window) < 2:
        return 0.0
    ranges: list[float] = []
    for previous, current in pairwise(window):
        true_range = max(
            current.session_high_c - current.session_low_c,
            abs(current.session_high_c - previous.session_close_c),
            abs(current.session_low_c - previous.session_close_c),
        )
        ranges.append(float(true_range))
    return sum(ranges) / len(ranges) if ranges else 0.0


def _require_registered_inputs(sessions: Sequence[Session]) -> None:
    """Refuse inputs the registered rule cannot be run over. **Shared.**"""
    expected_range_ms = CONFIG.opening_range_minutes * 60_000
    for session in sessions:
        start_ms, end_ms = session.opening_range_utc()
        if end_ms - start_ms != expected_range_ms:
            raise DispersionInputError(
                f"session {session.day}: the opening-range window is "
                f"{(end_ms - start_ms) / 60_000:g} minutes, and the registered "
                f"length is {CONFIG.opening_range_minutes}. The clock and the "
                "registration disagree, and this writer refuses to average over "
                "the disagreement."
            )
    if len(sessions) <= CONFIG.relvol_lookback_sessions:
        raise DispersionInputError(
            f"need more than {CONFIG.relvol_lookback_sessions} sessions for the "
            f"trailing relative-volume window, got {len(sessions)}"
        )


def _scan_all(
    tickers: Sequence[str],
    load_payloads: Callable[[str], Sequence[bytes]],
    sessions: Sequence[Session],
) -> tuple[dict[str, list[_NameSession]], int]:
    """Scan every ticker, one at a time. **Shared. Returns nothing public.**

    ``load_payloads`` is called once per ticker so only one name's bars are
    resident; the whole slice never is.
    """
    by_ticker: dict[str, list[_NameSession]] = {}
    bars_read = 0
    for ticker in tickers:
        bars = _bars_from_payloads(load_payloads(ticker), f"carve-out read, {ticker}")
        if not bars:
            continue
        bars_read += len(bars)
        rows = _scan_ticker(ticker, bars, sessions)
        if rows:
            by_ticker[ticker] = rows
    return by_ticker, bars_read


def _selections(
    by_ticker: Mapping[str, list[_NameSession]],
    sessions: Sequence[Session],
    *,
    allow_short: bool,
    price_floor_usd: float | None = None,
) -> Iterator[tuple[Session, str, _NameSession, Candidate]]:
    """The registered Section 2 selection, session by session. **Shared.**

    Yields one tuple per **selected** name-session. Everything it yields is
    private to this module; nothing here reaches a caller.
    """
    first_evaluable = CONFIG.relvol_lookback_sessions
    for index in range(first_evaluable, len(sessions)):
        session = sessions[index]
        candidates: dict[str, Candidate] = {}
        rows_today: dict[str, _NameSession] = {}
        for ticker, rows in by_ticker.items():
            by_index = {r.session_index: r for r in rows}
            today = by_index.get(index)
            if today is None:
                continue
            history = [
                by_index[i]
                for i in range(index - CONFIG.relvol_lookback_sessions, index)
                if i in by_index
            ]
            if len(history) < CONFIG.relvol_lookback_sessions:
                continue
            trailing = [r.first5_volume for r in history]
            try:
                relvol = relative_volume(today.first5_volume, trailing)
            except ValueError:
                continue
            candidates[ticker] = Candidate(
                ticker=ticker,
                relative_volume=relvol,
                session_open_c=today.session_open_c,
                avg_volume_14=sum(r.session_volume for r in history) / len(history),
                atr_14_c=_atr_14_c([*history, today]),
                has_locate=allow_short,
                borrow_rate_annual=0.0,
            )
            rows_today[ticker] = today

        if price_floor_usd is not None:
            # A raised floor is applied ON TOP of the registered Section 2
            # filter, never instead of it, so the scan is always a strict
            # subset of the registered universe. H1b is REGISTERED_NOT_OPEN
            # and this changes no registered rule.
            candidates = {
                ticker: candidate
                for ticker, candidate in candidates.items()
                if candidate.session_open_c > price_floor_usd * CENT
            }
        if not candidates:
            continue
        # Section 4: at most ``max_concurrent_positions`` are open at once, and
        # the registered selection is evaluated at a single instant, so the cap
        # and the selection width bind together. Read, not assumed equal.
        for ticker in select(candidates)[: CONFIG.max_concurrent_positions]:
            yield session, ticker, rows_today[ticker], candidates[ticker]


def measure_carve_out_dispersion(
    tickers: Sequence[str],
    load_payloads: Callable[[str], Sequence[bytes]],
    sessions: Sequence[Session],
    cost_model: CostModel,
    *,
    allow_short: bool,
    equity_usd: float,
    band: Band = Band.CENTRAL,
) -> CarveOutDispersion:
    """Run the registered rule over the carve-out. **Returns two scalars.**

    ``allow_short`` stands in for the Section 2 locate and borrow filter, which
    **this repository has not measured**. The caller states it and the caller
    records it; this module does not guess.
    """
    _require_registered_inputs(sessions)
    by_ticker, bars_read = _scan_all(tickers, load_payloads, sessions)

    per_share: list[float] = []
    seen_sessions: set[int] = set()
    name_sessions = 0
    triggered = 0
    ambiguous = 0
    priced = 0
    refused = 0
    below_one_share = 0
    stop_exits = 0
    close_exits = 0

    for session, _ticker, row, candidate in _selections(
        by_ticker, sessions, allow_short=allow_short
    ):
        seen_sessions.add(row.session_index)
        name_sessions += 1
        if row.trigger is Trigger.AMBIGUOUS:
            ambiguous += 1
            continue
        if row.trigger is Trigger.NONE:
            continue
        if row.side is Side.SHORT and not candidate.shortable():
            continue
        triggered += 1
        if row.entry_c is None or row.stop_c is None or row.exit_c is None:
            continue
        assert row.side is not None and row.exit_leg is not None

        risk_per_share = abs(row.entry_c - row.stop_c) / CENT
        if risk_per_share <= 0:
            below_one_share += 1
            continue
        sized = CONFIG.risk_fraction_per_trade * equity_usd / risk_per_share
        # HFExperiment C-17: IBKR refuses fractional API orders, error 10243.
        # The floor is a registered constraint, not a rounding convenience, so
        # the config field is read rather than assumed.
        if not CONFIG.integer_shares_only:
            raise DispersionInputError(
                "integer_shares_only is False; this writer implements only the "
                "registered integer-share sizing and refuses to invent a "
                "fractional one."
            )
        shares = int(sized)
        entry_fill = row.entry_c / CENT
        cap_shares = int(CONFIG.max_gross_notional_multiple * equity_usd / entry_fill)
        shares = min(shares, cap_shares)
        if shares < 1:
            below_one_share += 1
            continue

        net = cost_model.net_pnl(
            shares,
            entry_fill,
            row.exit_c / CENT,
            row.exit_leg,
            row.side,
            session.day,
            band,
        )
        if not isinstance(net, float):
            refused += 1
            continue
        priced += 1
        per_share.append(net / shares)
        if row.exit_leg is Leg.STOP_EXIT:
            stop_exits += 1
        else:
            close_exits += 1

    stdev = _sample_stdev(per_share)
    rate = triggered / name_sessions if name_sessions else 0.0
    return CarveOutDispersion(
        net_pnl_per_share_stdev=stdev,
        trigger_rate=rate,
        sessions_evaluated=len(seen_sessions),
        name_sessions_evaluated=name_sessions,
        name_sessions_triggered=triggered,
        name_sessions_ambiguous=ambiguous,
        trades_priced=priced,
        trades_refused_by_cost_model=refused,
        trades_below_one_share=below_one_share,
        stop_exits=stop_exits,
        close_exits=close_exits,
        bars_read=bars_read,
        tickers_with_bars=len(by_ticker),
    )


def measure_carve_out_execution_mix(
    tickers: Sequence[str],
    load_payloads: Callable[[str], Sequence[bytes]],
    sessions: Sequence[Session],
    cost_model: CostModel,
    *,
    allow_short: bool,
    band_from: Band = Band.CENTRAL,
    band_to: Band = Band.PESSIMISTIC,
) -> CarveOutExecutionMix:
    """The stop-versus-close mix and the ambiguous rate. **Four scalars.**

    **Amendment 19 needs both, and both were assumptions until this ran.** The
    pessimistic-minus-central shift is charged on the entry leg and on
    **whichever exit leg the trade actually took**, so it cannot be computed
    without the realized mix.

    **The exit mix is determined by the bars, not by the cost model.** It is
    counted here from the Section 3 stop and close rules directly, so a cost
    model that **refuses to price a trade** — as the frozen Section 6 model does
    for every session, its SEC effective date being unmeasured — **still yields
    a mix.** Reading the mix off priced trades instead would have made it
    silently zero.
    """
    _require_registered_inputs(sessions)
    by_ticker, bars_read = _scan_all(tickers, load_payloads, sessions)

    seen_sessions: set[int] = set()
    name_sessions = 0
    ambiguous = 0
    triggered = 0
    stop_exits = 0
    close_exits = 0
    unresolved = 0

    for _session, _ticker, row, candidate in _selections(
        by_ticker, sessions, allow_short=allow_short
    ):
        seen_sessions.add(row.session_index)
        name_sessions += 1
        if row.trigger is Trigger.AMBIGUOUS:
            ambiguous += 1
            continue
        if row.trigger is Trigger.NONE:
            continue
        if row.side is Side.SHORT and not candidate.shortable():
            continue
        triggered += 1
        if row.exit_leg is Leg.STOP_EXIT:
            stop_exits += 1
        elif row.exit_leg is Leg.CLOSE_EXIT:
            close_exits += 1
        else:
            unresolved += 1

    exits = stop_exits + close_exits
    stop_share = stop_exits / exits if exits else 0.0
    ambiguous_rate = ambiguous / name_sessions if name_sessions else 0.0
    shift = (
        cost_model.mean_slippage_shift_per_share(
            stop_share, band_from=band_from, band_to=band_to
        )
        if exits
        else 0.0
    )
    return CarveOutExecutionMix(
        stop_exit_share=stop_share,
        ambiguous_rate=ambiguous_rate,
        mean_pessimistic_shift_usd_per_share=shift,
        sessions_used=len(seen_sessions),
        name_sessions_evaluated=name_sessions,
        name_sessions_ambiguous=ambiguous,
        name_sessions_triggered=triggered,
        trades_with_a_resolved_exit=exits,
        stop_exits=stop_exits,
        close_exits=close_exits,
        trades_with_an_unresolved_exit=unresolved,
        bars_read=bars_read,
        tickers_with_bars=len(by_ticker),
    )


def _percentile(values: Sequence[float], q: float) -> float:
    """Linear-interpolation percentile. **0.0 at n = 0, and the caller reads the n.**"""
    ordered = sorted(values)
    if not ordered:
        return 0.0
    if len(ordered) == 1:
        return float(ordered[0])
    position = q * (len(ordered) - 1)
    lower = int(position)
    upper = min(lower + 1, len(ordered) - 1)
    weight = position - lower
    return float(ordered[lower] * (1 - weight) + ordered[upper] * weight)


def _mean(values: Sequence[float]) -> float:
    return sum(values) / len(values) if values else 0.0


def _time_weighted_half_spread(
    payload: bytes, start_ms: int, end_ms: int
) -> float | None:
    """Time-weighted **half** spread across one minute, in USD per share.

    A marketable order crosses to the far side of the book, which costs
    approximately **half the quoted spread** against the mid. The weighting is
    by **time each quote stood**, not by quote count, so a single flickering
    quote cannot dominate a minute it was barely present for.

    Returns ``None`` when the payload carries no usable quote, which the caller
    counts as a refused minute rather than as a zero spread.
    """
    try:
        envelope = json.loads(payload)
    except (json.JSONDecodeError, UnicodeDecodeError):
        return None
    if not isinstance(envelope, dict):
        return None
    rows = envelope.get("quotes")
    if not isinstance(rows, list) or not rows:
        return None

    stamped: list[tuple[int, float]] = []
    for row in rows:
        if not isinstance(row, dict):
            continue
        stamp = _stamp_ms(row.get("t"))
        bid, ask = row.get("bp"), row.get("ap")
        if stamp is None or not isinstance(bid, int | float):
            continue
        if not isinstance(ask, int | float) or isinstance(bid, bool):
            continue
        if isinstance(ask, bool) or ask <= 0 or bid <= 0 or ask < bid:
            continue
        stamped.append((stamp, float(ask) - float(bid)))
    if not stamped:
        return None

    stamped.sort(key=lambda pair: pair[0])
    weighted = 0.0
    elapsed = 0
    for index, (stamp, spread) in enumerate(stamped):
        nxt = stamped[index + 1][0] if index + 1 < len(stamped) else end_ms
        held = max(0, min(nxt, end_ms) - max(stamp, start_ms))
        weighted += spread * held
        elapsed += held
    if elapsed <= 0:
        return _mean([spread for _stamp, spread in stamped]) / 2.0
    return (weighted / elapsed) / 2.0


def measure_carve_out_slippage_band(
    tickers: Sequence[str],
    load_payloads: Callable[[str], Sequence[bytes]],
    load_quotes: Callable[[str, int, int], bytes | None],
    sessions: Sequence[Session],
    stop_exit_share: float,
    *,
    allow_short: bool,
) -> CarveOutSlippageBand:
    """Measure the Section 6 slippage band on the instruments actually traded.

    **The carried band came from an ETF.** 0.020 central and 0.040 pessimistic
    on entry, 0.040 and 0.080 on stop exits, 0.010 and 0.020 on close exits, all
    from the QQQ replication (carried, C-6) — an instrument with a spread near
    one cent. **This universe selects news-driven single names, and the carried
    figures were never measured on them.**

    **``load_quotes`` receives only readable fields** — a ticker symbol and two
    bar timestamps, both on ``orb.seal.READABLE_FIELDS`` — and returns bytes.
    **No priced value crosses that boundary in either direction.** It may return
    ``None``, which is counted as a refused minute and **never** as a zero
    spread.

    **What a minute bar can and cannot support, stated because it bounds the
    result.** When the trigger bar **opens through** the boundary, the first
    trade of that bar **is** the first trade through it and the overshoot is
    **exactly measurable**. When the bar opens inside and crosses within the
    minute, the first trade through the boundary lies somewhere in the bar and
    **one-minute data cannot locate it**; this writer records **0.0** for that
    trade. **The entry and stop overshoot distributions are therefore LOWER
    BOUNDS**, the resulting band is a lower bound, and any power computed on it
    is an **upper** bound. The counts of each case are returned so a reader can
    see how much of the distribution is bounded rather than measured.

    **The assignment is fixed before anything is computed**: **median to
    central, 90th percentile to pessimistic.**
    """
    _require_registered_inputs(sessions)
    by_ticker, bars_read = _scan_all(tickers, load_payloads, sessions)

    entry_overshoot: list[float] = []
    entry_half_spread: list[float] = []
    entry_slippage: list[float] = []
    stop_overshoot: list[float] = []
    stop_half_spread: list[float] = []
    stop_slippage: list[float] = []
    close_slippage: list[float] = []

    seen_sessions: set[int] = set()
    name_sessions = 0
    entry_gapped = entry_crossed = 0
    stop_gapped = stop_crossed = 0
    entry_quotes_ok = entry_quotes_refused = entry_quotes_truncated = 0
    stop_quotes_ok = stop_quotes_refused = 0
    close_missing = 0

    for _session, ticker, row, candidate in _selections(
        by_ticker, sessions, allow_short=allow_short
    ):
        seen_sessions.add(row.session_index)
        name_sessions += 1
        if row.trigger not in (Trigger.LONG, Trigger.SHORT):
            continue
        if row.side is Side.SHORT and not candidate.shortable():
            continue

        # --- entry leg ---
        if (
            row.trigger_boundary_c is not None
            and row.trigger_bar_open_c is not None
            and row.trigger_ms is not None
        ):
            boundary = row.trigger_boundary_c
            opened = row.trigger_bar_open_c
            through = opened > boundary if row.side is Side.LONG else opened < boundary
            overshoot = abs(opened - boundary) / CENT if through else 0.0
            if through:
                entry_gapped += 1
            else:
                entry_crossed += 1
            entry_overshoot.append(overshoot)

            payload = load_quotes(ticker, row.trigger_ms, row.trigger_ms + 60_000)
            half = (
                None
                if payload is None
                else _time_weighted_half_spread(
                    payload, row.trigger_ms, row.trigger_ms + 60_000
                )
            )
            if half is None:
                entry_quotes_refused += 1
            else:
                entry_quotes_ok += 1
                entry_half_spread.append(half)
                entry_slippage.append(overshoot + half)

        # --- stop-exit leg ---
        if (
            row.exit_leg is Leg.STOP_EXIT
            and row.stop_c is not None
            and row.stop_bar_open_c is not None
            and row.stop_ms is not None
        ):
            stop_level = row.stop_c
            opened = row.stop_bar_open_c
            through = (
                opened < stop_level if row.side is Side.LONG else opened > stop_level
            )
            overshoot = abs(opened - stop_level) / CENT if through else 0.0
            if through:
                stop_gapped += 1
            else:
                stop_crossed += 1
            stop_overshoot.append(overshoot)

            payload = load_quotes(ticker, row.stop_ms, row.stop_ms + 60_000)
            half = (
                None
                if payload is None
                else _time_weighted_half_spread(
                    payload, row.stop_ms, row.stop_ms + 60_000
                )
            )
            if half is None:
                stop_quotes_refused += 1
            else:
                stop_quotes_ok += 1
                stop_half_spread.append(half)
                stop_slippage.append(overshoot + half)

        # --- close-exit leg ---
        if row.exit_leg is Leg.CLOSE_EXIT:
            if row.last_exit_window_close_c is None or row.official_close_c is None:
                close_missing += 1
            else:
                close_slippage.append(
                    abs(row.official_close_c - row.last_exit_window_close_c) / CENT
                )

    entry_central = _percentile(entry_slippage, 0.50)
    entry_pessimistic = _percentile(entry_slippage, 0.90)
    stop_central = _percentile(stop_slippage, 0.50)
    stop_pessimistic = _percentile(stop_slippage, 0.90)
    close_central = _percentile(close_slippage, 0.50)
    close_pessimistic = _percentile(close_slippage, 0.90)

    entry_shift = entry_pessimistic - entry_central
    stop_shift = stop_pessimistic - stop_central
    close_shift = close_pessimistic - close_central
    shift = (
        entry_shift
        + stop_exit_share * stop_shift
        + (1.0 - stop_exit_share) * close_shift
    )

    return CarveOutSlippageBand(
        entry_overshoot_mean=_mean(entry_overshoot),
        entry_overshoot_median=_percentile(entry_overshoot, 0.50),
        entry_overshoot_p90=_percentile(entry_overshoot, 0.90),
        entry_half_spread_mean=_mean(entry_half_spread),
        entry_half_spread_median=_percentile(entry_half_spread, 0.50),
        entry_half_spread_p90=_percentile(entry_half_spread, 0.90),
        entry_slippage_mean=_mean(entry_slippage),
        entry_slippage_median=entry_central,
        entry_slippage_p90=entry_pessimistic,
        stop_overshoot_mean=_mean(stop_overshoot),
        stop_overshoot_median=_percentile(stop_overshoot, 0.50),
        stop_overshoot_p90=_percentile(stop_overshoot, 0.90),
        stop_half_spread_mean=_mean(stop_half_spread),
        stop_half_spread_median=_percentile(stop_half_spread, 0.50),
        stop_half_spread_p90=_percentile(stop_half_spread, 0.90),
        stop_slippage_mean=_mean(stop_slippage),
        stop_slippage_median=stop_central,
        stop_slippage_p90=stop_pessimistic,
        close_slippage_mean=_mean(close_slippage),
        close_slippage_median=close_central,
        close_slippage_p90=close_pessimistic,
        measured_entry_central=entry_central,
        measured_entry_pessimistic=entry_pessimistic,
        measured_stop_central=stop_central,
        measured_stop_pessimistic=stop_pessimistic,
        measured_close_central=close_central,
        measured_close_pessimistic=close_pessimistic,
        stop_exit_share=stop_exit_share,
        measured_shift_usd_per_share=shift,
        sessions_used=len(seen_sessions),
        name_sessions_evaluated=name_sessions,
        entry_observations=len(entry_slippage),
        entry_gapped_through=entry_gapped,
        entry_crossed_intrabar=entry_crossed,
        entry_quote_minutes_served=entry_quotes_ok,
        entry_quote_minutes_refused=entry_quotes_refused,
        entry_quote_minutes_truncated=entry_quotes_truncated,
        stop_observations=len(stop_slippage),
        stop_gapped_through=stop_gapped,
        stop_crossed_intrabar=stop_crossed,
        stop_quote_minutes_served=stop_quotes_ok,
        stop_quote_minutes_refused=stop_quotes_refused,
        close_observations=len(close_slippage),
        close_without_an_official_print=close_missing,
        bars_read=bars_read,
        tickers_with_bars=len(by_ticker),
    )


def measure_carve_out_floor_scan(
    tickers: Sequence[str],
    load_payloads: Callable[[str], Sequence[bytes]],
    sessions: Sequence[Session],
    cost_model: CostModel,
    price_floors_usd: Sequence[float],
    annual_sharpe: float,
    *,
    allow_short: bool,
    equity_usd: float,
    band: Band = Band.CENTRAL,
) -> tuple[CarveOutFloorScanRow, ...]:
    """The H1b price-floor **feasibility scan**. Counts and ratios only.

    **H1b is `REGISTERED_NOT_OPEN`.** This function computes **no verdict and no
    power figure**, because computing either would be opening it. It hands the
    operator a table and selects nothing.

    **The raised floor is applied on top of the registered Section 2 filter**,
    never instead of it, so every scanned universe is a **strict subset** of the
    registered one and no registered rule is changed.

    **The comparison figure is `central_mean_to_shift_ratio`.** The mechanism
    H1b registers is that **per-share slippage is roughly price-invariant while
    per-share dispersion and edge scale with price**, so the ratio should rise
    with the floor. The shift here is the **registered Section 6 band shift** at
    each floor's own measured stop-exit share — the invariant half of the
    mechanism — and the measured entry overshoot is reported beside it as an
    independent check on that invariance.

    **A floor that empties the universe is a finding**, and the row still
    returns with its counts at zero rather than being dropped.
    """
    _require_registered_inputs(sessions)
    by_ticker, _bars_read = _scan_all(tickers, load_payloads, sessions)

    rows: list[CarveOutFloorScanRow] = []
    for floor in price_floors_usd:
        per_share: list[float] = []
        overshoot: list[float] = []
        relvols: list[float] = []
        per_session_selected: dict[int, int] = {}
        seen_sessions: set[int] = set()
        eligible = selected = triggered = priced = 0

        for session, _ticker, row, candidate in _selections(
            by_ticker, sessions, allow_short=allow_short, price_floor_usd=floor
        ):
            seen_sessions.add(row.session_index)
            per_session_selected[row.session_index] = (
                per_session_selected.get(row.session_index, 0) + 1
            )
            selected += 1
            eligible += 1
            relvols.append(candidate.relative_volume)

            if row.trigger not in (Trigger.LONG, Trigger.SHORT):
                continue
            if row.side is Side.SHORT and not candidate.shortable():
                continue
            triggered += 1

            if (
                row.trigger_boundary_c is not None
                and row.trigger_bar_open_c is not None
            ):
                boundary, opened = row.trigger_boundary_c, row.trigger_bar_open_c
                through = (
                    opened > boundary if row.side is Side.LONG else opened < boundary
                )
                overshoot.append(abs(opened - boundary) / CENT if through else 0.0)

            if row.entry_c is None or row.stop_c is None or row.exit_c is None:
                continue
            assert row.side is not None and row.exit_leg is not None
            risk_per_share = abs(row.entry_c - row.stop_c) / CENT
            if risk_per_share <= 0:
                continue
            shares = int(CONFIG.risk_fraction_per_trade * equity_usd / risk_per_share)
            entry_fill = row.entry_c / CENT
            shares = min(
                shares,
                int(CONFIG.max_gross_notional_multiple * equity_usd / entry_fill),
            )
            if shares < 1:
                continue
            net = cost_model.net_pnl(
                shares,
                entry_fill,
                row.exit_c / CENT,
                row.exit_leg,
                row.side,
                session.day,
                band,
            )
            if not isinstance(net, float):
                continue
            priced += 1
            per_share.append(net / shares)

        stops = sum(
            1
            for _s, _t, r, c in _selections(
                by_ticker, sessions, allow_short=allow_short, price_floor_usd=floor
            )
            if r.exit_leg is Leg.STOP_EXIT
            and not (r.side is Side.SHORT and not c.shortable())
        )
        exits = sum(
            1
            for _s, _t, r, c in _selections(
                by_ticker, sessions, allow_short=allow_short, price_floor_usd=floor
            )
            if r.exit_leg in (Leg.STOP_EXIT, Leg.CLOSE_EXIT)
            and not (r.side is Side.SHORT and not c.shortable())
        )
        stop_share = stops / exits if exits else 0.0
        shift = (
            cost_model.mean_slippage_shift_per_share(
                stop_share, band_from=Band.CENTRAL, band_to=Band.PESSIMISTIC
            )
            if exits
            else 0.0
        )
        dispersion = _sample_stdev(per_share)
        n_sessions = len(seen_sessions)
        trades_per_session = priced / n_sessions if n_sessions else 0.0
        daily = annual_sharpe / math.sqrt(CONFIG.trading_days_per_year)
        central_mean = (
            dispersion * daily / math.sqrt(trades_per_session)
            if trades_per_session > 0
            else 0.0
        )
        rows.append(
            CarveOutFloorScanRow(
                price_floor_usd=floor,
                mean_relative_volume_of_selection=_mean(relvols),
                dispersion_usd_per_share=dispersion,
                entry_overshoot_median=_percentile(overshoot, 0.50),
                central_mean_usd_per_share=central_mean,
                shift_usd_per_share=shift,
                central_mean_to_shift_ratio=(
                    central_mean / shift if shift > 0 else 0.0
                ),
                eligible_name_sessions=eligible,
                selected_name_sessions=selected,
                sessions_with_a_full_selection=sum(
                    1
                    for count in per_session_selected.values()
                    if count >= CONFIG.selection_width
                ),
                sessions_evaluated=n_sessions,
                triggered_trades=triggered,
                priced_trades=priced,
            )
        )
    return tuple(rows)


def _sample_stdev(values: Sequence[float]) -> float:
    """Sample standard deviation. **Zero at n < 2, and the caller reads the n.**

    A 0.0 at `n = 0` is an absence, not a measurement, and every figure this
    module returns travels with the count that says which it is.
    """
    n = len(values)
    if n < 2:
        return 0.0
    mean = sum(values) / n
    return math.sqrt(sum((v - mean) ** 2 for v in values) / (n - 1))
