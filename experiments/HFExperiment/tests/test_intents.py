"""The construction wall: a malformed intent cannot travel."""
import pytest

from hfexperiment.intents import (
    SMART_ROUTE,
    ConstructionRefusal,
    Intent,
    Quote,
    capture_quote,
    construct_intent,
    diff_books,
    formation_hash,
)

GOOD_QUOTE = Quote(bid=99.9, ask=100.1, mid=100.0,
                   captured_utc="2026-08-25T02:00:00Z")


def _construct(**overrides: object) -> Intent | ConstructionRefusal:
    fields: dict[str, object] = dict(
        symbol="SNDK",
        side="buy",
        notional_usd=45.0,
        quote=GOOD_QUOTE,
        account="[paper account ID removed]",
        route=SMART_ROUTE,
        formation_hash="0b28a5cfda7516fa",
    )
    fields.update(overrides)
    return construct_intent(**fields)  # type: ignore[arg-type]


def test_full_intent_constructs_with_quantity_from_the_mid() -> None:
    intent = _construct()
    assert isinstance(intent, Intent)
    assert intent.quantity == pytest.approx(0.45)
    assert intent.quote.captured_utc == "2026-08-25T02:00:00Z"


def test_every_absent_field_refuses_at_construction() -> None:
    cases: list[dict[str, object]] = [
        {"symbol": None},
        {"symbol": ""},
        {"side": None},
        {"side": "short"},
        {"notional_usd": None},
        {"notional_usd": 0.0},
        {"account": None},
        {"account": ""},
        {"route": None},
        {"route": ""},
        {"formation_hash": None},
        {"formation_hash": ""},
    ]
    for overrides in cases:
        result = _construct(**overrides)
        assert isinstance(result, ConstructionRefusal), overrides
        assert result.reason == "intent_field_absent", overrides


def test_missing_quote_refuses_with_the_arrival_mid_reason() -> None:
    result = _construct(quote=None)
    assert isinstance(result, ConstructionRefusal)
    assert result.reason == "no_arrival_mid"
    assert "fill_without_arrival_mid" in result.arithmetic


def test_capture_quote_refuses_unusable_quotes() -> None:
    bad = capture_quote(0.0, 10.0, "2026-08-25T02:00:00Z")
    assert isinstance(bad, ConstructionRefusal)
    assert bad.reason == "no_arrival_mid"
    crossed = capture_quote(10.0, 9.0, "2026-08-25T02:00:00Z")
    assert isinstance(crossed, ConstructionRefusal)
    assert crossed.reason == "no_arrival_mid"
    unstamped = capture_quote(9.9, 10.1, "")
    assert isinstance(unstamped, ConstructionRefusal)
    assert unstamped.reason == "no_capture_timestamp"
    good = capture_quote(9.9, 10.1, "2026-08-25T02:00:00Z")
    assert isinstance(good, Quote)
    assert good.mid == pytest.approx(10.0)


def test_formation_hash_is_deterministic_and_order_sensitive() -> None:
    a = formation_hash("2026-08-03", 20, ["SNDK", "AXTI"])
    b = formation_hash("2026-08-03", 20, ["SNDK", "AXTI"])
    c = formation_hash("2026-08-03", 20, ["AXTI", "SNDK"])
    assert a == b
    assert a != c


def test_diff_books_buys_entries_and_sells_leavers() -> None:
    diff = diff_books(["AAA", "BBB"], held={"BBB": 1.0, "CCC": 2.0})
    assert ("AAA", "buy") in diff
    assert ("CCC", "sell") in diff
    assert ("BBB", "buy") not in diff
    assert len(diff) == 2
