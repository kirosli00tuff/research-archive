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
        if setup.trigger in (Trigger.LONG, Trigger.SHORT):
            assert setup.triggered_at_ms is not None
            stopped_at = stop_hit(inside, setup, setup.triggered_at_ms)
            if stopped_at is not None:
                exit_price = setup.stop_c
                leg = Leg.STOP_EXIT
            else:
                exit_price = close_exit_c(inside, (exit_start_ms, exit_end_ms))
                leg = Leg.CLOSE_EXIT

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
