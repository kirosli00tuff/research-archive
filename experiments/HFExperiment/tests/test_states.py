"""The five accrual states never merge and each has an enforcement site."""
import pytest

from hfexperiment.states import (
    EXCLUDING_STATES,
    HALT_CONFIRM_SESSIONS,
    MARKING_STATES,
    AccrualState,
    classify_name_day,
    excludes_day,
    marks_at_last_close,
)


def _classify(**overrides: object) -> AccrualState:
    base: dict[str, object] = dict(
        fetch_ok=True,
        has_bar=False,
        asset_active=True,
        bar_exists_later=False,
        absent_streak=1,
    )
    base.update(overrides)
    return classify_name_day(**base)  # type: ignore[arg-type]


def test_exactly_five_states_in_two_disjoint_families() -> None:
    values = {state.value for state in AccrualState}
    assert values == {
        "computed", "missing_bar", "halted", "delisted", "source_failed"
    }
    assert not (MARKING_STATES & EXCLUDING_STATES)
    assert MARKING_STATES | EXCLUDING_STATES | {
        AccrualState.COMPUTED
    } == frozenset(AccrualState)


def test_classifier_produces_each_of_the_five_states() -> None:
    assert _classify(has_bar=True) is AccrualState.COMPUTED
    assert _classify() is AccrualState.MISSING_BAR
    assert _classify(asset_active=False) is AccrualState.DELISTED
    assert _classify(bar_exists_later=True) is AccrualState.HALTED
    assert (
        _classify(absent_streak=HALT_CONFIRM_SESSIONS) is AccrualState.HALTED
    )
    assert _classify(fetch_ok=False) is AccrualState.SOURCE_FAILED


def test_source_failed_never_merges_into_missing_bar() -> None:
    # A failed source and a missing bar are different facts. Merging
    # them is the second registered mutation and this test catches it.
    assert _classify(fetch_ok=False) is AccrualState.SOURCE_FAILED
    assert _classify(fetch_ok=False) is not AccrualState.MISSING_BAR
    assert _classify() is AccrualState.MISSING_BAR
    assert _classify() is not AccrualState.SOURCE_FAILED
    assert (
        _classify(fetch_ok=False, absent_streak=0)
        is AccrualState.SOURCE_FAILED
    )


def test_a_mark_persists_intra_month_even_when_bars_resume() -> None:
    resumed = _classify(has_bar=True, already_marked=AccrualState.HALTED)
    assert resumed is AccrualState.HALTED
    gone = _classify(has_bar=True, already_marked=AccrualState.DELISTED)
    assert gone is AccrualState.DELISTED


def test_only_marking_states_persist_as_marks() -> None:
    with pytest.raises(ValueError):
        _classify(already_marked=AccrualState.COMPUTED)
    with pytest.raises(ValueError):
        _classify(already_marked=AccrualState.MISSING_BAR)


def test_excluding_family_enforcement() -> None:
    assert excludes_day(AccrualState.MISSING_BAR)
    assert excludes_day(AccrualState.SOURCE_FAILED)
    assert not excludes_day(AccrualState.COMPUTED)
    assert not excludes_day(AccrualState.HALTED)
    assert not excludes_day(AccrualState.DELISTED)


def test_marking_family_enforcement() -> None:
    assert marks_at_last_close(AccrualState.HALTED)
    assert marks_at_last_close(AccrualState.DELISTED)
    assert not marks_at_last_close(AccrualState.COMPUTED)
    assert not marks_at_last_close(AccrualState.MISSING_BAR)
    assert not marks_at_last_close(AccrualState.SOURCE_FAILED)


def test_short_unexplained_absence_stays_missing_bar() -> None:
    assert (
        _classify(absent_streak=HALT_CONFIRM_SESSIONS - 1)
        is AccrualState.MISSING_BAR
    )
