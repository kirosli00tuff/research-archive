"""The carve-out dispersion writer, against synthetic fixtures with known answers.

The bars here are constructed, not served. Every session is engineered so the
registered rule has **one** answer, and the test asserts that answer rather than
whatever the code happens to produce.

The boundary fixtures sit **on** the carve-out edge: a payload carrying a bar
stamped one millisecond before 2026-07-01T04:00:00.000Z is **refused**, and the
instant itself passes.
"""

from __future__ import annotations

import json
from collections.abc import Sequence
from datetime import UTC, date, datetime

import pytest

from orb.calendar import Session, sessions
from orb.config import CONFIG
from orb.costs import CostModel, SecFeeSchedule
from orb.costs_registered import REGISTERED_COST_MODEL
from orb.dispersion import (
    CarveOutDispersion,
    DispersionInputError,
    measure_carve_out_dispersion,
)
from orb.preperiod import PrePeriodViolationError

SLICE = list(sessions(date(2026, 7, 1), date(2026, 8, 28)))
"""42 post-holdout sessions — the same slice the live pull uses."""

ZERO_SEC_MODEL: CostModel = CostModel(
    commission_per_share=REGISTERED_COST_MODEL.commission_per_share,
    commission_order_minimum=REGISTERED_COST_MODEL.commission_order_minimum,
    commission_max_fraction_of_trade_value=(
        REGISTERED_COST_MODEL.commission_max_fraction_of_trade_value
    ),
    finra_taf_per_share_sold=REGISTERED_COST_MODEL.finra_taf_per_share_sold,
    finra_cat_per_share=REGISTERED_COST_MODEL.finra_cat_per_share,
    clearing_per_share=REGISTERED_COST_MODEL.clearing_per_share,
    sec_fees=SecFeeSchedule(
        effective_dates=(date(2026, 1, 1),), rates_per_dollar=(0.0,)
    ),
    entry_slippage=REGISTERED_COST_MODEL.entry_slippage,
    stop_slippage=REGISTERED_COST_MODEL.stop_slippage,
    close_slippage=REGISTERED_COST_MODEL.close_slippage,
)
"""The frozen model with the **one unmeasured component** set to its hard lower
bound of zero. A fee cannot be negative, so this end of the bracket is a fact
about arithmetic rather than an assumption about the world."""


def _iso(ms: int) -> str:
    return (
        datetime.fromtimestamp(ms / 1000, tz=UTC)
        .isoformat(timespec="milliseconds")
        .replace("+00:00", "Z")
    )


def _bar(
    ms: int, o: float, h: float, low: float, c: float, v: int
) -> dict[str, object]:
    return {"t": _iso(ms), "o": o, "h": h, "l": low, "c": c, "v": v}


def _payload(rows: Sequence[dict[str, object]]) -> bytes:
    return json.dumps({"bars": list(rows), "next_page_token": None}).encode()


HALF_RANGE = 0.35
"""The opening range is 0.70 USD wide, so the registered 14-session ATR filter
— **above 0.50 USD** — passes on a quiet session.

A narrower fixture fails that filter and evaluates nothing. The first draft of
these tests used 0.20 and was caught by the filter rather than by an assertion,
which is the InsiderExperiment lesson arriving from the other side: a fixture
that does not clear a registered threshold measures the threshold, not the code.
"""


def _flat_session(
    session: Session, price: float, volume: int
) -> list[dict[str, object]]:
    """A session that never breaks its opening range. Trigger NONE, by design."""
    open_ms, range_end_ms = session.opening_range_utc()
    exit_start, exit_end = session.close_exit_utc()
    high, low = price + HALF_RANGE, price - HALF_RANGE
    rows = [
        _bar(open_ms + i * 60_000, price, high, low, price, volume) for i in range(5)
    ]
    # Every post-range bar stays strictly inside the range, so nothing triggers
    # and nothing touches a stop.
    rows.extend(
        _bar(stamp, price, high - 0.01, low + 0.01, price, volume)
        for stamp in (range_end_ms, exit_start, exit_end - 60_000)
    )
    return rows


def _breakout_session(
    session: Session, price: float, volume: int, close_at: float
) -> list[dict[str, object]]:
    """A clean long break of the opening-range high, then a stated close."""
    open_ms, range_end_ms = session.opening_range_utc()
    exit_start, exit_end = session.close_exit_utc()
    high, low = price + HALF_RANGE, price - HALF_RANGE
    rows = [
        _bar(open_ms + i * 60_000, price, high, low, price, volume) for i in range(5)
    ]
    # The first bar after the range clears the high and never reaches the stop,
    # which sits at the opposite extreme of the range.
    rows.append(_bar(range_end_ms, high, high + 1.00, high, high + 0.90, volume))
    rows.extend(
        _bar(stamp, close_at, close_at + 0.05, close_at - 0.05, close_at, volume)
        for stamp in (exit_start, exit_end - 60_000)
    )
    return rows


def _ticker_payloads(breakout_on: set[int], close_at: float = 61.0) -> list[bytes]:
    rows: list[dict[str, object]] = []
    for index, session in enumerate(SLICE):
        # A quiet trailing history, then a volume spike on the breakout day, so
        # relative volume ranks the name first on exactly the sessions chosen.
        volume = 2_000_000 if index in breakout_on else 1_500_000
        if index in breakout_on:
            rows.extend(_breakout_session(session, 60.0, volume, close_at))
        else:
            rows.extend(_flat_session(session, 60.0, volume))
    return [_payload(rows)]


def _run(
    payloads_by_ticker: dict[str, list[bytes]],
    model: CostModel = ZERO_SEC_MODEL,
    *,
    allow_short: bool = True,
) -> CarveOutDispersion:
    return measure_carve_out_dispersion(
        sorted(payloads_by_ticker),
        lambda t: payloads_by_ticker[t],
        SLICE,
        model,
        allow_short=allow_short,
        equity_usd=100_000.0,
    )


# --------------------------------------------------------------------------
# The contract: two scalars, and the counts that carry their n
# --------------------------------------------------------------------------


def test_the_writer_returns_two_scalars_and_integer_counts() -> None:
    import dataclasses

    result = _run({"AAA": _ticker_payloads({20, 25})})
    floats = [f.name for f in dataclasses.fields(result) if f.type == "float"]
    assert floats == ["net_pnl_per_share_stdev", "trigger_rate"]
    assert all(
        isinstance(getattr(result, f.name), int)
        for f in dataclasses.fields(result)
        if f.type == "int"
    )


def test_a_session_that_never_breaks_its_range_does_not_trigger() -> None:
    """Trigger rate 0.0 with a non-zero denominator is a measurement, not an absence."""
    result = _run({"AAA": _ticker_payloads(set())})
    assert result.name_sessions_evaluated > 0
    assert result.name_sessions_triggered == 0
    assert result.trigger_rate == 0.0
    assert result.trades_priced == 0
    assert result.net_pnl_per_share_stdev == 0.0


def test_the_trigger_rate_is_the_realized_share_with_its_denominator() -> None:
    """Two breakouts among the evaluable sessions of one name. Hand-counted."""
    breakouts = {20, 25}
    result = _run({"AAA": _ticker_payloads(breakouts)})
    evaluable = len(SLICE) - CONFIG.relvol_lookback_sessions
    assert result.sessions_evaluated == evaluable
    assert result.name_sessions_evaluated == evaluable
    assert result.name_sessions_triggered == len(breakouts)
    assert result.trigger_rate == pytest.approx(len(breakouts) / evaluable)


def test_a_priced_trade_produces_a_dispersion_and_an_unpriced_one_does_not() -> None:
    """The frozen model refuses every trade; the zero-SEC bracket prices them.

    This is the measured shape of the A.2 TASK 2 finding: the SEC Section 31
    rate was measured at 0.0000206 per dollar and **its effective date was
    not**, so ``SEC_FEE_SCHEDULE`` is empty on purpose and
    :meth:`orb.costs.SecFeeSchedule.rate_on` returns ``Absent`` for every
    session. **The model refuses to price a trade rather than take a fee from
    the wrong year**, and this test pins that the refusal reaches the writer as
    a counted refusal rather than as a silent zero.
    """
    payloads = {"AAA": _ticker_payloads({20, 25, 30})}

    frozen = _run(payloads, REGISTERED_COST_MODEL)
    assert frozen.trades_priced == 0
    assert frozen.trades_refused_by_cost_model == 3
    assert frozen.net_pnl_per_share_stdev == 0.0
    assert frozen.name_sessions_triggered == 3, (
        "a cost-model refusal must not reduce the measured trigger rate"
    )

    bracketed = _run(payloads, ZERO_SEC_MODEL)
    assert bracketed.trades_priced == 3
    assert bracketed.trades_refused_by_cost_model == 0
    assert bracketed.trigger_rate == frozen.trigger_rate


def test_the_dispersion_is_zero_at_n_below_two_and_the_count_says_so() -> None:
    """0.0 at `n < 2` is an absence. The caller reads the n beside it."""
    result = _run({"AAA": _ticker_payloads({20})}, ZERO_SEC_MODEL)
    assert result.trades_priced == 1
    assert result.net_pnl_per_share_stdev == 0.0


def test_two_trades_with_different_outcomes_give_a_positive_dispersion() -> None:
    result = _run(
        {
            "AAA": _ticker_payloads({20, 25}, close_at=61.0),
            "BBB": _ticker_payloads({20, 25}, close_at=59.0),
        },
        ZERO_SEC_MODEL,
    )
    assert result.trades_priced == 4
    assert result.net_pnl_per_share_stdev > 0.0


# --------------------------------------------------------------------------
# The carve-out boundary, enforced per bar
# --------------------------------------------------------------------------


def test_a_bar_inside_the_sealed_window_is_refused_rather_than_dropped() -> None:
    """One millisecond before the boundary. **On the edge, not near it.**"""
    boundary = CONFIG.post_holdout_start_ms
    payload = _payload([_bar(boundary - 1, 60.0, 60.1, 59.9, 60.0, 1000)])
    with pytest.raises(PrePeriodViolationError):
        measure_carve_out_dispersion(
            ["AAA"],
            lambda _t: [payload],
            SLICE,
            ZERO_SEC_MODEL,
            allow_short=True,
            equity_usd=100_000.0,
        )


def test_the_boundary_instant_itself_is_admitted() -> None:
    boundary = CONFIG.post_holdout_start_ms
    payload = _payload([_bar(boundary, 60.0, 60.1, 59.9, 60.0, 1000)])
    result = measure_carve_out_dispersion(
        ["AAA"],
        lambda _t: [payload],
        SLICE,
        ZERO_SEC_MODEL,
        allow_short=True,
        equity_usd=100_000.0,
    )
    assert result.bars_read == 1


# --------------------------------------------------------------------------
# The registered inputs it refuses to average over
# --------------------------------------------------------------------------


def test_too_few_sessions_for_the_trailing_window_is_refused() -> None:
    short_slice = SLICE[: CONFIG.relvol_lookback_sessions]
    with pytest.raises(DispersionInputError, match="trailing relative-volume"):
        measure_carve_out_dispersion(
            ["AAA"],
            lambda _t: [_payload([])],
            short_slice,
            ZERO_SEC_MODEL,
            allow_short=True,
            equity_usd=100_000.0,
        )


def test_the_long_only_restriction_is_the_callers_to_state() -> None:
    """``allow_short`` stands in for a filter this repository has not measured."""
    payloads = {"AAA": _ticker_payloads({20, 25})}
    both = _run(payloads, ZERO_SEC_MODEL, allow_short=True)
    long_only = _run(payloads, ZERO_SEC_MODEL, allow_short=False)
    # These fixtures break upward, so the two agree — which is the point: the
    # flag changes what is *eligible*, never what a long trade is worth.
    assert both.name_sessions_triggered == long_only.name_sessions_triggered
