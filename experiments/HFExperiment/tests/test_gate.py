"""Every registered refusal fires, names its arithmetic, writes nothing."""
from hfexperiment.gate import OrderIntent, Refusal, check_order
from hfexperiment.registered import (
    BROKER_MIN_NOTIONAL_USD,
    PER_NAME_NOTIONAL_USD,
    THRESHOLDS,
    DeferredParameter,
)

CLEAN = OrderIntent(
    symbol="MU",
    side="buy",
    notional_usd=45.0,
    is_fractionable=True,
    smart_routed=True,
    formation_reproduced=True,
)


def check(
    intent: OrderIntent,
    settled_cash_usd: float = 900.0,
    spend_last_365d_usd: float = 0.0,
    broker_min_notional_usd: float | DeferredParameter = 1.0,
    per_name_notional_usd: float | DeferredParameter = 45.0,
) -> Refusal | None:
    """The gate with resolved parameters unless a test overrides them."""
    return check_order(
        intent,
        settled_cash_usd=settled_cash_usd,
        spend_last_365d_usd=spend_last_365d_usd,
        broker_min_notional_usd=broker_min_notional_usd,
        per_name_notional_usd=per_name_notional_usd,
        thresholds=THRESHOLDS,
    )


def test_clean_order_passes() -> None:
    assert check(CLEAN) is None


def test_deferred_per_name_notional_refuses() -> None:
    refusal = check(CLEAN, per_name_notional_usd=PER_NAME_NOTIONAL_USD)
    assert refusal is not None
    assert refusal.reason == "deferred_parameter_unresolved"
    assert "Amendment 1" in refusal.arithmetic


def test_deferred_broker_minimum_refuses() -> None:
    refusal = check(CLEAN, broker_min_notional_usd=BROKER_MIN_NOTIONAL_USD)
    assert refusal is not None
    assert refusal.reason == "deferred_parameter_unresolved"
    assert "Amendment 1" in refusal.arithmetic


def test_insufficient_settled_cash_names_both_figures() -> None:
    refusal = check(CLEAN, settled_cash_usd=40.0)
    assert refusal is not None
    assert refusal.reason == "insufficient_settled_cash"
    assert "45.00" in refusal.arithmetic
    assert "40.00" in refusal.arithmetic


def test_sells_do_not_need_settled_cash() -> None:
    sell = OrderIntent(
        symbol="MU", side="sell", notional_usd=45.0, is_fractionable=True,
        smart_routed=True, formation_reproduced=True,
    )
    assert check(sell, settled_cash_usd=0.0) is None


def test_below_broker_minimum_refuses() -> None:
    refusal = check(CLEAN, broker_min_notional_usd=50.0)
    assert refusal is not None
    assert refusal.reason == "below_broker_minimum"
    assert "50.00" in refusal.arithmetic


def test_non_fractionable_symbol_refuses() -> None:
    intent = OrderIntent(
        symbol="BRK.A", side="buy", notional_usd=45.0, is_fractionable=False,
        smart_routed=True, formation_reproduced=True,
    )
    refusal = check(intent)
    assert refusal is not None
    assert refusal.reason == "non_fractionable_symbol"


def test_failed_formation_reproduction_refuses() -> None:
    intent = OrderIntent(
        symbol="MU", side="buy", notional_usd=45.0, is_fractionable=True,
        smart_routed=True, formation_reproduced=False,
    )
    refusal = check(intent)
    assert refusal is not None
    assert refusal.reason == "formation_reproduction_failed"


def test_spend_cap_refuses_at_registered_cap() -> None:
    refusal = check(
        CLEAN, spend_last_365d_usd=THRESHOLDS.spend_cap_usd_per_year
    )
    assert refusal is not None
    assert refusal.reason == "spend_cap_reached"
    assert f"{THRESHOLDS.spend_cap_usd_per_year:.2f}" in refusal.arithmetic


def test_non_smart_routed_refuses() -> None:
    intent = OrderIntent(
        symbol="MU", side="buy", notional_usd=45.0, is_fractionable=True,
        smart_routed=False, formation_reproduced=True,
    )
    refusal = check(intent)
    assert refusal is not None
    assert refusal.reason == "not_smart_routed"
