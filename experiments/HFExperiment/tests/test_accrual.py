"""The accrual orchestration: exclusion, retry healing, idempotency."""
from pathlib import Path

import pytest

from hfexperiment.accrual import (
    Ledgers,
    chain_pointers,
    excess_series,
    open_ledgers,
    process_pending,
    record_formation_states,
)

SESSIONS = ["2026-09-01", "2026-09-02", "2026-09-03", "2026-09-04"]
MEMBERS = ["AAA", "BBB", "CCC", "DDD", "EEE", "FFF"]
BOOK5 = ["AAA", "BBB", "CCC", "DDD", "EEE"]
ENTRY = {
    "AAA": 10.0, "BBB": 20.0, "CCC": 30.0,
    "DDD": 40.0, "EEE": 50.0, "FFF": 60.0,
}


class FakeView:
    """A BarView over an in-memory close table."""

    def __init__(
        self,
        closes: dict[tuple[str, str], float],
        sessions: list[str],
        active: set[str] | None = None,
    ) -> None:
        self._closes = closes
        self._sessions = sessions
        self._active = active if active is not None else set(MEMBERS)

    def close(self, symbol: str, session: str) -> float | None:
        return self._closes.get((symbol, session))

    def asset_active(self, symbol: str) -> bool:
        return symbol in self._active

    def bar_exists_later(self, symbol: str, session: str) -> bool:
        return any(
            s > session and (symbol, s) in self._closes
            for s in self._sessions
        )

    def absent_streak(self, symbol: str, session: str) -> int:
        streak = 0
        for s in reversed([x for x in self._sessions if x <= session]):
            if (symbol, s) in self._closes:
                break
            streak += 1
        return streak


def _ledgers(tmp_path: Path) -> Ledgers:
    ledgers = open_ledgers(tmp_path)
    record_formation_states(
        ledgers, "2026-09-01", MEMBERS, {5: BOOK5}, ENTRY, "form-run"
    )
    return ledgers


def _closes_for(
    sessions: list[str], skip: set[tuple[str, str]] | None = None
) -> dict[tuple[str, str], float]:
    skipped = skip or set()
    out: dict[tuple[str, str], float] = {}
    for i, session in enumerate(sessions):
        for sym in MEMBERS:
            if (sym, session) in skipped:
                continue
            out[(sym, session)] = ENTRY[sym] * (1.0 + 0.01 * i)
    return out


def test_missing_bar_produces_missing_bar_and_excludes_the_day(
    tmp_path: Path,
) -> None:
    # Arrange: FFF, a benchmark member, has no bar on 2026-09-02.
    ledgers = _ledgers(tmp_path)
    span = SESSIONS[:2]
    view = FakeView(
        _closes_for(span, skip={("FFF", "2026-09-02")}), span
    )
    # Act.
    counts = process_pending(ledgers, view, span, True, "run-1")
    # Assert: the day is excluded, recorded, and nothing accrues.
    assert counts["benchmark_excluded"] == 1
    assert counts["benchmark_computed"] == 0
    assert counts["accrual_computed"] == 0
    record = ledgers.benchmark.read_all()[-1]
    assert record["status"] == "excluded"
    assert record["excluding_state_counts"] == {"missing_bar": 1}
    assert record["excluding_sample"] == {"FFF": "missing_bar"}
    assert excess_series(ledgers, 5) == []


def test_the_excluded_day_heals_on_retry_when_the_bar_backfills(
    tmp_path: Path,
) -> None:
    ledgers = _ledgers(tmp_path)
    span = SESSIONS[:2]
    view = FakeView(_closes_for(span, skip={("FFF", "2026-09-02")}), span)
    process_pending(ledgers, view, span, True, "run-1")
    # The bar backfills. The retry computes the day and appends after
    # the exclusion record. History is never edited.
    healed = FakeView(_closes_for(span), span)
    counts = process_pending(ledgers, healed, span, True, "run-2")
    assert counts["benchmark_computed"] == 1
    assert counts["accrual_computed"] == 1
    statuses = [r["status"] for r in ledgers.benchmark.read_all()]
    assert statuses == ["excluded", "computed"]
    assert [s for s, _bp in excess_series(ledgers, 5)] == ["2026-09-02"]


def test_computed_excess_matches_hand_arithmetic(tmp_path: Path) -> None:
    # Every name moves +1 percent each session, so the equal-weighted
    # book and the benchmark mean both return exactly the same and the
    # excess is zero to float precision.
    ledgers = _ledgers(tmp_path)
    view = FakeView(_closes_for(SESSIONS), SESSIONS)
    process_pending(ledgers, view, SESSIONS, True, "run-1")
    series = excess_series(ledgers, 5)
    assert [s for s, _bp in series] == SESSIONS[1:]
    for _session, bp in series:
        assert bp == pytest.approx(0.0, abs=1e-9)
    pointers = chain_pointers(ledgers)
    assert pointers["benchmark"] == SESSIONS[-1]
    assert pointers["width_5"] == SESSIONS[-1]


def test_source_failed_is_recorded_as_its_own_state(tmp_path: Path) -> None:
    ledgers = _ledgers(tmp_path)
    span = SESSIONS[:2]
    view = FakeView(_closes_for(span), span)
    counts = process_pending(ledgers, view, span, False, "run-1")
    assert counts["benchmark_excluded"] == 1
    record = ledgers.benchmark.read_all()[-1]
    assert record["excluding_state_counts"] == {"source_failed": len(MEMBERS)}
    assert "missing_bar" not in record["excluding_state_counts"]


def test_halted_member_marks_and_the_day_still_computes(
    tmp_path: Path,
) -> None:
    # FFF has no bar on 09-02 but trades again on 09-03: a confirmed
    # single-session halt. The day computes with FFF at zero return.
    ledgers = _ledgers(tmp_path)
    span = SESSIONS[:3]
    view = FakeView(_closes_for(span, skip={("FFF", "2026-09-02")}), span)
    counts = process_pending(ledgers, view, span, True, "run-1")
    assert counts["benchmark_excluded"] == 0
    assert counts["benchmark_computed"] == 2
    first = [
        r for r in ledgers.benchmark.read_all() if r["status"] == "computed"
    ][0]
    assert first["state_counts"] == {"computed": 5, "halted": 1}
    assert first["panel"]["marked"] == {"FFF": "halted"}


def test_idempotent_rerun_appends_nothing(tmp_path: Path) -> None:
    ledgers = _ledgers(tmp_path)
    view = FakeView(_closes_for(SESSIONS), SESSIONS)
    process_pending(ledgers, view, SESSIONS, True, "run-1")
    before = (
        len(ledgers.benchmark.read_all()),
        len(ledgers.accrual.read_all()),
    )
    counts = process_pending(ledgers, view, SESSIONS, True, "run-2")
    after = (
        len(ledgers.benchmark.read_all()),
        len(ledgers.accrual.read_all()),
    )
    assert before == after
    assert counts["benchmark_computed"] == 0
    assert counts["accrual_computed"] == 0
