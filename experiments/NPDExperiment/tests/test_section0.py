"""Section 0 fires on coverage alone."""

from __future__ import annotations

from npd.callstate import CallState
from npd.section0 import Section0Verdict, coverage_of, fire


def counts(**kw: int) -> dict[CallState, int]:
    return {CallState(k): v for k, v in kw.items()}


def test_excluded_pre_cutoff_never_enters_the_denominator() -> None:
    stored, eligible, cov = coverage_of(counts(stored=90, excluded_pre_cutoff=500, no_data=10))
    assert eligible == 100
    assert stored == 90
    assert cov == 0.90


def test_model_failed_does_enter_the_denominator() -> None:
    _stored, eligible, cov = coverage_of(counts(stored=90, model_failed=10))
    assert eligible == 100
    assert cov == 0.90


def test_go_at_or_above_ninety_percent() -> None:
    r = fire(counts(stored=90, model_failed=10), window_clears_power_floor=True)
    assert r.verdict is Section0Verdict.GO


def test_degraded_between_seventy_and_ninety() -> None:
    r = fire(counts(stored=80, model_failed=20), window_clears_power_floor=True)
    assert r.verdict is Section0Verdict.DEGRADED
    assert "recomputed power" in r.rationale


def test_blocked_under_seventy() -> None:
    r = fire(counts(stored=60, model_failed=40), window_clears_power_floor=True)
    assert r.verdict is Section0Verdict.BLOCKED
    assert "No verdict claimed" in r.rationale


def test_blocked_when_the_window_falls_under_the_power_floor() -> None:
    r = fire(counts(stored=100), window_clears_power_floor=False)
    assert r.verdict is Section0Verdict.BLOCKED
    assert "power floor" in r.rationale


def test_a_perfect_pass_is_go() -> None:
    r = fire(counts(stored=432), window_clears_power_floor=True)
    assert r.verdict is Section0Verdict.GO
    assert r.coverage == 1.0
