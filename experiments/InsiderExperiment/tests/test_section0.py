"""The two gates fire on the registered bars and on nothing else."""

from __future__ import annotations

import pytest

from insider.config import CONFIG
from insider.section0 import (
    CorpusVerdict,
    PowerVerdict,
    fire_corpus_gate,
    fire_power_gate,
)


@pytest.mark.parametrize(
    ("mde", "expected"),
    [
        (5.0, PowerVerdict.GO),
        (19.99, PowerVerdict.GO),
        (20.0, PowerVerdict.GO),
        (20.01, PowerVerdict.DEGRADED),
        (34.29, PowerVerdict.DEGRADED),
        (40.0, PowerVerdict.DEGRADED),
        (40.01, PowerVerdict.BLOCKED),
        (49.35, PowerVerdict.BLOCKED),
    ],
)
def test_the_power_gate_fires_on_the_registered_boundaries(
    mde: float, expected: PowerVerdict
) -> None:
    assert fire_power_gate(mde).verdict is expected


def test_blocked_does_not_authorize_stage_b() -> None:
    assert fire_power_gate(49.35).stage_b_authorized is False
    assert fire_power_gate(34.29).stage_b_authorized is True
    assert fire_power_gate(12.0).stage_b_authorized is True


def test_the_degraded_rationale_names_the_registered_verdict_row() -> None:
    text = fire_power_gate(30.0).rationale
    assert "registered verdict row" in text
    assert "not a disappointment" in text


def test_a_non_positive_mde_is_refused_rather_than_bucketed() -> None:
    for bad in (0.0, -1.0, float("nan")):
        with pytest.raises(ValueError):
            fire_power_gate(bad)


def test_unreachable_edgar_blocks_the_corpus_whatever_the_counts() -> None:
    gate = fire_corpus_gate(edgar_reachable=False, qualifying_events=99_999, session_coverage=1.0)
    assert gate.verdict is CorpusVerdict.CORPUS_BLOCKED
    assert "EDGAR access failed" in gate.rationale


def test_the_event_floor_and_the_coverage_floor_both_bind() -> None:
    below = fire_corpus_gate(
        edgar_reachable=True,
        qualifying_events=CONFIG.corpus_event_floor - 1,
        session_coverage=1.0,
    )
    assert below.verdict is CorpusVerdict.CORPUS_BLOCKED

    thin = fire_corpus_gate(
        edgar_reachable=True,
        qualifying_events=CONFIG.corpus_event_floor,
        session_coverage=CONFIG.corpus_coverage_floor - 0.01,
    )
    assert thin.verdict is CorpusVerdict.CORPUS_BLOCKED
    assert "non-empty book" in thin.rationale

    passes = fire_corpus_gate(
        edgar_reachable=True,
        qualifying_events=CONFIG.corpus_event_floor,
        session_coverage=CONFIG.corpus_coverage_floor,
    )
    assert passes.verdict is CorpusVerdict.CORPUS_GO


def test_the_registered_bars_are_the_ones_in_force() -> None:
    assert CONFIG.mde_go_ceiling_bp == 20.0
    assert CONFIG.mde_degraded_ceiling_bp == 40.0
    assert CONFIG.corpus_event_floor == 1_000
    assert CONFIG.corpus_coverage_floor == 0.80
