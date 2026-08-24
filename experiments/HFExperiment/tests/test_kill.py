"""The restart-versus-termination distinction is load-bearing."""
import pytest

from hfexperiment.kill import (
    FLOOR_BREACH_EVENT,
    TERMINATION_EVENTS,
    StopKind,
    breach_record,
    classify,
    floor_breached,
)
from hfexperiment.registered import THRESHOLDS


def test_floor_breach_is_a_restart_not_a_termination() -> None:
    kind = classify(FLOOR_BREACH_EVENT)
    assert kind is StopKind.RESTART
    assert kind is not StopKind.TERMINATION


def test_every_termination_event_terminates() -> None:
    assert {
        "two_consecutive_formation_failures",
        "order_gate_bypass",
        "fill_without_arrival_mid",
        "formation_reproduction_failure",
    } == TERMINATION_EVENTS
    for event in TERMINATION_EVENTS:
        assert classify(event) is StopKind.TERMINATION


def test_unknown_event_refuses_rather_than_defaults() -> None:
    with pytest.raises(ValueError):
        classify("bad_hair_day")


def test_floor_breached_at_registered_level() -> None:
    floor = THRESHOLDS.restart_floor_usd
    assert floor == 500.0
    assert floor_breached(floor)
    assert floor_breached(floor - 0.01)
    assert not floor_breached(floor + 0.01)


def test_breach_record_pauses_capital_and_keeps_the_measurement() -> None:
    record = breach_record(equity_usd=498.20)
    assert record["kind"] == StopKind.RESTART.value
    assert record["kind"] != StopKind.TERMINATION.value
    assert record["requires_operator_resume"] is True
    assert record["preserves_fill_history"] is True
    assert record["floor_usd"] == THRESHOLDS.restart_floor_usd
