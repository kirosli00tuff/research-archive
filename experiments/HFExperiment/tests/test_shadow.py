"""Book and panel accrual arithmetic, and the absence refusal."""
import pytest

from hfexperiment.shadow import (
    BookState,
    accrue_book_day,
    advance_panel,
    day_exclusion,
    initial_book,
    initial_panel,
)
from hfexperiment.states import AccrualState

COMPUTED = AccrualState.COMPUTED


def _book() -> BookState:
    return initial_book(
        "2026-09-01", 2, ["AAA", "BBB"], {"AAA": 10.0, "BBB": 20.0}
    )


def test_initial_book_equal_weights_at_formation() -> None:
    book = _book()
    assert book.values == {"AAA": 0.5, "BBB": 0.5}
    assert book.asof == "2026-09-01"
    assert book.last_closes == {"AAA": 10.0, "BBB": 20.0}
    assert book.marked == {}


def test_initial_book_refuses_wrong_width_or_missing_entry() -> None:
    with pytest.raises(ValueError):
        initial_book("2026-09-01", 3, ["AAA", "BBB"], {"AAA": 1.0, "BBB": 1.0})
    with pytest.raises(ValueError):
        initial_book("2026-09-01", 2, ["AAA", "BBB"], {"AAA": 1.0})


def test_accrue_day_uses_drifting_weights() -> None:
    book = _book()
    # Arrange: AAA +10 percent, BBB -5 percent from equal weights.
    day = accrue_book_day(
        book,
        "2026-09-02",
        {"AAA": COMPUTED, "BBB": COMPUTED},
        {"AAA": 11.0, "BBB": 19.0},
    )
    assert day.book_return == pytest.approx(0.025)
    assert day.state.values["AAA"] == pytest.approx(0.55)
    assert day.state.values["BBB"] == pytest.approx(0.475)
    # Act again: AAA +10 percent, BBB flat, now at drifted weights.
    day2 = accrue_book_day(
        day.state,
        "2026-09-03",
        {"AAA": COMPUTED, "BBB": COMPUTED},
        {"AAA": 12.1, "BBB": 19.0},
    )
    drifted = 0.55 / (0.55 + 0.475)
    assert day2.book_return == pytest.approx(drifted * 0.10)


def test_halted_name_marks_at_last_close_and_mark_persists() -> None:
    book = _book()
    day = accrue_book_day(
        book,
        "2026-09-02",
        {"AAA": AccrualState.HALTED, "BBB": COMPUTED},
        {"BBB": 22.0},
    )
    assert day.name_returns["AAA"] == 0.0
    assert day.state.marked == {"AAA": "halted"}
    assert day.state.last_closes["AAA"] == 10.0
    assert day.book_return == pytest.approx(0.05)
    # The mark persists: even with a close supplied, a marked state
    # keeps zero return until the next formation.
    day2 = accrue_book_day(
        day.state,
        "2026-09-03",
        {"AAA": AccrualState.HALTED, "BBB": COMPUTED},
        {"AAA": 99.0, "BBB": 22.0},
    )
    assert day2.name_returns["AAA"] == 0.0
    assert day2.state.last_closes["AAA"] == 10.0


def test_missing_bar_refuses_a_synthesized_price() -> None:
    # The absence test. The first registered mutation carries a price
    # forward for a missing bar, and this refusal is what catches it.
    book = _book()
    with pytest.raises(ValueError, match="missing_bar"):
        accrue_book_day(
            book,
            "2026-09-02",
            {"AAA": AccrualState.MISSING_BAR, "BBB": COMPUTED},
            {"BBB": 22.0},
        )
    with pytest.raises(ValueError, match="source_failed"):
        accrue_book_day(
            book,
            "2026-09-02",
            {"AAA": AccrualState.SOURCE_FAILED, "BBB": COMPUTED},
            {"BBB": 22.0},
        )


def test_day_exclusion_names_the_excluding_states_only() -> None:
    states = {
        "AAA": AccrualState.MISSING_BAR,
        "BBB": COMPUTED,
        "CCC": AccrualState.HALTED,
        "DDD": AccrualState.SOURCE_FAILED,
    }
    assert day_exclusion(states) == ["AAA", "DDD"]
    assert day_exclusion({"BBB": COMPUTED, "CCC": AccrualState.HALTED}) == []


def test_advance_panel_tracks_last_closes_and_marks() -> None:
    panel = initial_panel(
        "2026-09-01", ["AAA", "BBB"], {"AAA": 10.0, "BBB": 20.0}
    )
    day = advance_panel(
        panel,
        "2026-09-02",
        {"AAA": COMPUTED, "BBB": AccrualState.DELISTED},
        {"AAA": 10.5},
    )
    assert day.member_returns == {"AAA": pytest.approx(0.05), "BBB": 0.0}
    assert day.panel.last_closes == {"AAA": 10.5, "BBB": 20.0}
    assert day.panel.marked == {"BBB": "delisted"}
    assert day.panel.asof == "2026-09-02"
