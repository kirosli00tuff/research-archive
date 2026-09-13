"""The two chain-resolution rules, each exercised at its decision boundary.

Both rules are places where a quiet wrong answer produces a valid-looking
straddle either way, so each is tested at the tie it exists to break rather than
only in the easy middle of its range.
"""

from __future__ import annotations

from datetime import UTC, datetime, timedelta

from mbt.absence import AbsenceReason, Absent
from mbt.chain import ListedExpiry, resolve_straddle, select_atm_strike, select_expiry
from mbt.clock import ObservationClock
from mbt.figures import TickDelayStatus
from mbt.quotes import Quote

AT = datetime(2026, 9, 3, 12, 0, 0, tzinfo=UTC)
CME_RULE = "CME crypto option settlement, 16:00 London time on the last Friday"


def expiry(days: float, label: str = "") -> ListedExpiry:
    return ListedExpiry(
        label=label or f"+{days}d",
        settlement=AT + timedelta(days=days),
        exchange="CME",
        settlement_rule=CME_RULE,
    )


def future_quote(bid: float = 78_000.0, ask: float = 78_100.0) -> Quote:
    return Quote(
        leg="future_hedge",
        bid=bid,
        ask=ask,
        clock=ObservationClock(venue=AT, local=AT),
        tick_delay=TickDelayStatus.REALTIME,
    )


# --- the 30-day tenor rule -------------------------------------------------


def test_the_expiry_nearest_thirty_days_is_selected() -> None:
    chosen = select_expiry([expiry(7), expiry(28), expiry(60)], AT)
    assert not isinstance(chosen, Absent)
    assert chosen[0].label == "+28d"
    assert chosen[1] is False


def test_a_tenor_tie_resolves_to_the_LONGER_expiry() -> None:
    """27 and 33 days are equidistant from 30. The registered rule takes 33.

    The registered hedging rule evaluates delta daily over a 30-day tenor, and
    the rebalance counts carried from VRPExperiment were measured over exactly
    that path. The shorter side truncates it.
    """
    chosen = select_expiry([expiry(27), expiry(33)], AT)
    assert not isinstance(chosen, Absent)
    assert chosen[0].label == "+33d"
    assert chosen[1] is True, "the artifact must record that the tie rule fired"


def test_an_expired_series_is_never_selected() -> None:
    chosen = select_expiry([expiry(-1), expiry(45)], AT)
    assert not isinstance(chosen, Absent)
    assert chosen[0].label == "+45d"


def test_a_chain_with_no_live_expiry_is_absent_rather_than_rounded() -> None:
    chosen = select_expiry([expiry(-10), expiry(-1)], AT)
    assert isinstance(chosen, Absent)
    assert chosen.reason is AbsenceReason.NOT_SERVED


def test_the_tenor_is_measured_to_the_settlement_instant_not_to_midnight() -> None:
    """Constructed so a settlement-instant rule and a midnight rule DISAGREE.

    Both expiries fall on the same calendar day, 2026-10-03, so a rule measuring
    to midnight sees both at exactly 30 days, ties, and takes the longer one.
    Measuring to the settlement instant makes them 29.75 and 30.458 days, and the
    nearer is the earlier one. The test therefore fails if the rule ever silently
    reverts to calendar-day arithmetic.
    """
    early = ListedExpiry("06:00Z", datetime(2026, 10, 3, 6, 0, tzinfo=UTC), "CME", CME_RULE)
    late = ListedExpiry("23:00Z", datetime(2026, 10, 3, 23, 0, tzinfo=UTC), "CME", CME_RULE)

    assert early.settlement.date() == late.settlement.date(), "the premise of the test"
    assert abs(early.days_to_expiry(AT) - 29.75) < 1e-9
    assert abs(late.days_to_expiry(AT) - 30.458333333) < 1e-6

    chosen = select_expiry([early, late], AT)
    assert not isinstance(chosen, Absent)
    assert chosen[0].label == "06:00Z", "a midnight rule would have tied and taken 23:00Z"
    assert chosen[1] is False, "measured to the instant there is no tie to break"


# --- the at-the-money strike rule ------------------------------------------


def test_the_strike_nearest_the_reference_is_selected() -> None:
    chosen = select_atm_strike([77_000.0, 78_000.0, 79_000.0], 78_050.0)
    assert not isinstance(chosen, Absent)
    assert chosen[0] == 78_000.0
    assert chosen[1] is False


def test_a_strike_tie_resolves_to_the_LOWER_strike() -> None:
    """78,000 and 78,500 are equidistant from 78,250. The rule takes 78,000.

    Two equidistant strikes are equally at-the-money, so the choice is arbitrary
    by construction. Fixing it before any chain is enumerated is the point: it
    cannot then be made after seeing which of the two quotes tighter.
    """
    chosen = select_atm_strike([78_000.0, 78_500.0], 78_250.0)
    assert not isinstance(chosen, Absent)
    assert chosen[0] == 78_000.0
    assert chosen[1] is True


def test_an_empty_strike_list_is_absent_rather_than_interpolated() -> None:
    chosen = select_atm_strike([], 78_000.0)
    assert isinstance(chosen, Absent)


def test_a_non_positive_reference_yields_no_at_the_money_strike() -> None:
    assert isinstance(select_atm_strike([78_000.0], 0.0), Absent)


# --- the reference price ---------------------------------------------------


def test_the_reference_is_the_hedge_future_touch_midpoint() -> None:
    resolved = resolve_straddle([expiry(30)], [78_000.0, 78_050.0], future_quote(), AT)
    assert not isinstance(resolved, Absent)
    assert resolved.reference_price == 78_050.0
    assert resolved.strike == 78_050.0


def test_a_refused_hedge_quote_refuses_the_whole_straddle() -> None:
    """No reference price means no ATM strike. It is never substituted."""
    crossed = future_quote(bid=78_200.0, ask=78_100.0)
    resolved = resolve_straddle([expiry(30)], [78_000.0], crossed, AT)
    assert isinstance(resolved, Absent)
    assert resolved.reason is AbsenceReason.CROSSED_BOOK


def test_the_resolved_selection_records_its_inputs_for_the_artifact() -> None:
    resolved = resolve_straddle([expiry(7), expiry(30)], [77_000.0, 78_000.0], future_quote(), AT)
    assert not isinstance(resolved, Absent)
    row = resolved.as_row()
    assert row["expiries_listed"] == 2
    assert row["strikes_listed"] == 2
    assert abs(float(row["days_to_expiry"]) - 30.0) < 1e-9  # type: ignore[arg-type]
