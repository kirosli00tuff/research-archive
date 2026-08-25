"""The wired gate: eight refusals produced, one intent priced and
stopped exactly at Amendment 1."""
import dataclasses

from hfexperiment.gate import Refusal
from hfexperiment.gatewire import GateInputs, PricedReady, evaluate
from hfexperiment.intents import SMART_ROUTE, Intent, Quote

PINNED = "[paper account ID removed]"
FHASH = "0b28a5cfda7516fa"
QUOTE = Quote(bid=99.9, ask=100.1, mid=100.0,
              captured_utc="2026-08-25T02:00:00Z")


def _intent(**overrides: object) -> Intent:
    fields: dict[str, object] = dict(
        symbol="SNDK",
        side="buy",
        notional_usd=45.0,
        quantity=0.45,
        quote=QUOTE,
        account=PINNED,
        route=SMART_ROUTE,
        formation_hash=FHASH,
    )
    fields.update(overrides)
    return Intent(**fields)  # type: ignore[arg-type]


def _inputs(**overrides: object) -> GateInputs:
    fields: dict[str, object] = dict(
        settled_cash_usd=1000.0,
        spend_last_365d_usd=0.0,
        fractionable={"SNDK": True},
        reproduced_hash=FHASH,
        pinned_account=PINNED,
        mode="paper",
        broker_min_notional_usd=1.0,
        per_name_notional_usd=45.0,
    )
    fields.update(overrides)
    return GateInputs(**fields)  # type: ignore[arg-type]


def _refusal(intent: Intent, inputs: GateInputs) -> Refusal:
    outcome = evaluate(intent, inputs)
    assert isinstance(outcome, Refusal), outcome
    return outcome


def test_refusal_1_insufficient_settled_cash() -> None:
    refusal = _refusal(_intent(), _inputs(settled_cash_usd=30.0))
    assert refusal.reason == "insufficient_settled_cash"
    assert "45.00" in refusal.arithmetic
    assert "30.00" in refusal.arithmetic


def test_refusal_2_below_broker_minimum() -> None:
    refusal = _refusal(
        _intent(notional_usd=0.5), _inputs(broker_min_notional_usd=1.0)
    )
    assert refusal.reason == "below_broker_minimum"


def test_refusal_3_non_fractionable_and_absence_fails_closed() -> None:
    refusal = _refusal(_intent(), _inputs(fractionable={"SNDK": False}))
    assert refusal.reason == "non_fractionable_symbol"
    absent = _refusal(_intent(), _inputs(fractionable={}))
    assert absent.reason == "non_fractionable_symbol"


def test_refusal_4_formation_reproduction_failed() -> None:
    refusal = _refusal(
        _intent(formation_hash="0000deadbeef0000"), _inputs()
    )
    assert refusal.reason == "formation_reproduction_failed"
    missing = _refusal(_intent(), _inputs(reproduced_hash=None))
    assert missing.reason == "formation_reproduction_failed"


def test_refusal_5_spend_cap_reached() -> None:
    refusal = _refusal(_intent(), _inputs(spend_last_365d_usd=100.01))
    assert refusal.reason == "spend_cap_reached"
    assert "100.00" in refusal.arithmetic


def test_refusal_6_not_smart_routed() -> None:
    refusal = _refusal(_intent(route="DIRECTED:ARCA"), _inputs())
    assert refusal.reason == "not_smart_routed"


def test_refusal_7_deferred_is_the_steady_state() -> None:
    steady = GateInputs(
        settled_cash_usd=1000.0,
        spend_last_365d_usd=0.0,
        fractionable={"SNDK": True},
        reproduced_hash=FHASH,
        pinned_account=PINNED,
        mode="paper",
    )
    refusal = _refusal(_intent(), steady)
    assert refusal.reason == "deferred_parameter_unresolved"
    assert "Amendment 1" in refusal.arithmetic


def test_refusal_8_account_pin_four_ways() -> None:
    absent = _refusal(
        dataclasses.replace(_intent(), account=None),  # type: ignore[arg-type]
        _inputs(),
    )
    assert absent.reason == "account_not_pinned"
    assert "absent" in absent.arithmetic
    empty = _refusal(dataclasses.replace(_intent(), account=""), _inputs())
    assert empty.reason == "account_not_pinned"
    assert "default account" in empty.arithmetic
    wrong = _refusal(
        dataclasses.replace(_intent(), account="DU9999999"), _inputs()
    )
    assert wrong.reason == "account_not_pinned"
    mode = _refusal(_intent(), _inputs(mode="live"))
    assert mode.reason == "account_mode_mismatch"


def test_pin_precedes_even_the_deferred_steady_state() -> None:
    steady = GateInputs(
        settled_cash_usd=1000.0,
        spend_last_365d_usd=0.0,
        fractionable={"SNDK": True},
        reproduced_hash=FHASH,
        pinned_account=PINNED,
        mode="paper",
    )
    refusal = _refusal(
        dataclasses.replace(_intent(), account=""), steady
    )
    assert refusal.reason == "account_not_pinned"


def test_priced_and_ready_under_resolved_then_stopped_at_amendment_1(
) -> None:
    intent = _intent()
    ready = evaluate(intent, _inputs())
    assert isinstance(ready, PricedReady)
    assert ready.settled_cash_after_usd == 955.0
    steady = GateInputs(
        settled_cash_usd=1000.0,
        spend_last_365d_usd=0.0,
        fractionable={"SNDK": True},
        reproduced_hash=FHASH,
        pinned_account=PINNED,
        mode="paper",
    )
    stopped = evaluate(intent, steady)
    assert isinstance(stopped, Refusal)
    assert stopped.reason == "deferred_parameter_unresolved"
