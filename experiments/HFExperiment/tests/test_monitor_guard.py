"""The verdict view guard: the render fails if anything else enters it."""
import pytest

from hfexperiment.monitor import (
    _ALLOWED_VERDICT_LINES,
    VerdictViewError,
    verdict_view,
)
from hfexperiment.verdictengine import width_verdict

FORBIDDEN = (
    "missing_bar", "halted", "delisted", "source_failed",
    "timer", "gap", "membership", "fetch", "ledger", "credentials",
)


def _assert_allowlisted(text: str) -> None:
    # Independent of the module's internal raise: every line must match
    # a confidence-sequence shape, so a mutation that renders an accrual
    # row fails here even if it also disabled the internal guard.
    for line in text.splitlines():
        assert any(
            pattern.match(line) for pattern in _ALLOWED_VERDICT_LINES
        ), f"non-confidence-sequence line rendered: {line!r}"


def test_pre_start_state_is_empty_confidence_sequence_only() -> None:
    text = verdict_view([])
    assert "observations: 0" in text
    assert "bounds: none, the series has not started" in text
    assert "success bar: lower bound above 4.07 bp/day" in text
    assert "futility bar: upper bound below 10.0 bp/day" in text
    assert "clears zero at day 2061, clears the hurdle at day 2852" in text
    for word in FORBIDDEN:
        assert word not in text
    _assert_allowlisted(text)


def test_live_record_renders_bounds_and_nothing_else() -> None:
    series = [
        ("2026-09-02", 30.0), ("2026-09-03", -10.0), ("2026-09-04", 15.0)
    ]
    record = width_verdict(5, series, "run")
    text = verdict_view([record])
    assert "observations: 3" in text
    assert "bounds: lower" in text
    for word in FORBIDDEN:
        assert word not in text
    _assert_allowlisted(text)


def test_guard_fails_the_render_when_anything_else_enters() -> None:
    record = width_verdict(
        5, [("2026-09-02", 30.0), ("2026-09-03", 10.0)], "run"
    )
    poisoned = dict(record)
    poisoned["state"] = "computed 2026-09-02 WOLF accrual row"
    with pytest.raises(VerdictViewError):
        verdict_view([poisoned])
