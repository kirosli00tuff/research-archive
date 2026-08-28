"""Kill criteria. One restart bar, four terminations, never confused.

A TERMINATION ends the experiment: the failure is evidence about the
machinery, and machinery that fails twice, bypasses its gate, loses an
arrival mid, or cannot reproduce its own formation has no measurement to
continue. A RESTART pauses the capital: a drawdown is not evidence about
execution cost, so breaching the floor halts the sleeve, records the
breach, preserves every fill, and waits for an explicit operator decision
to resume. Collapsing the two kinds into one must fail
tests/test_kill.py.
"""
from __future__ import annotations

from enum import Enum
from typing import Any

from hfexperiment.registered import THRESHOLDS, RegisteredThresholds


class StopKind(Enum):
    """What a stop event does to the experiment."""

    RESTART = "restart"
    TERMINATION = "termination"


FLOOR_BREACH_EVENT = "equity_floor_breach"

TERMINATION_EVENTS = frozenset({
    "two_consecutive_formation_failures",
    "order_gate_bypass",
    "fill_without_arrival_mid",
    "formation_reproduction_failure",
})


def classify(event: str) -> StopKind:
    """The registered kind for a stop event. Unknown events raise.

    An unknown event is a design gap, not a judgment call, so it refuses
    rather than defaulting to either kind.
    """
    if event == FLOOR_BREACH_EVENT:
        return StopKind.RESTART
    if event in TERMINATION_EVENTS:
        return StopKind.TERMINATION
    raise ValueError(f"unregistered stop event: {event}")


def floor_breached(
    equity_usd: float, thresholds: RegisteredThresholds = THRESHOLDS
) -> bool:
    """Whether total account equity sits at or below the restart floor."""
    return equity_usd <= thresholds.restart_floor_usd


def breach_record(
    equity_usd: float, thresholds: RegisteredThresholds = THRESHOLDS
) -> dict[str, Any]:
    """The ledger record a floor breach appends.

    The record is the halt. It requires an operator resume and it
    preserves the fill history, because the execution measurement is not
    voided by a drawdown. To resume, the operator appends a resume record
    naming this breach, states the decision in it, and re-arms the gate.
    """
    return {
        "event": FLOOR_BREACH_EVENT,
        "kind": classify(FLOOR_BREACH_EVENT).value,
        "equity_usd": equity_usd,
        "floor_usd": thresholds.restart_floor_usd,
        "requires_operator_resume": True,
        "preserves_fill_history": True,
    }
