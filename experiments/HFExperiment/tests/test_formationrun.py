"""The formation at all three widths reproduces deterministically."""
import datetime
from pathlib import Path

from hfexperiment import universe
from hfexperiment.alpaca_source import DailyBar
from hfexperiment.barstore import BarStore
from hfexperiment.formationrun import FormationResult, run_formation

FORMATION = "2026-09-01"
N_SYMBOLS = 60
WIDTHS = (5, 20, 50)
PARAMS = universe.RuleParams(top_n=55)


def _sessions() -> list[str]:
    out = []
    day = datetime.date(2025, 6, 2)
    while day <= datetime.date(2026, 9, 4):
        if day.weekday() < 5:
            out.append(day.isoformat())
        day += datetime.timedelta(days=1)
    return out


def _sym(i: int) -> str:
    return f"SY{i:02d}"


class FakeSource:
    """Deterministic bars. Prices positive, dollar volumes distinct."""

    def __init__(self, sessions: list[str], reverse: bool = False) -> None:
        self._index = {s: j for j, s in enumerate(sessions)}
        self._sessions = sessions
        self._reverse = reverse

    def active_assets(self) -> list[tuple[str, str, str, str, int]]:
        symbols = [_sym(i) for i in range(N_SYMBOLS)]
        if self._reverse:
            symbols = list(reversed(symbols))
        return [
            (s, f"Test Corp {s}", "NYSE", "active", 1) for s in symbols
        ]

    def daily_bars(
        self, symbols: list[str], start: str, end: str
    ) -> dict[str, list[DailyBar]]:
        span = [s for s in self._sessions if start <= s <= end]
        ordered = list(reversed(symbols)) if self._reverse else symbols
        out: dict[str, list[DailyBar]] = {}
        for sym in ordered:
            i = int(sym[2:])
            rows: list[DailyBar] = []
            for session in span:
                j = self._index[session]
                close = 10.0 + i + 0.01 * j + 0.001 * ((i * j) % 7)
                rows.append(
                    (session, None, None, None, close, 1000.0 * (i + 1))
                )
            out[sym] = rows
        return out


def _run(tmp_path: Path, name: str, reverse: bool) -> FormationResult:
    sessions = _sessions()
    store = BarStore(tmp_path / name)
    source = FakeSource(sessions, reverse=reverse)
    result = run_formation(
        store, source, sessions, FORMATION, list(WIDTHS), "run",
        params=PARAMS,
    )
    stored = store.formation_books(FORMATION)
    store.close()
    assert stored == result.books
    return result


def test_formation_reproduces_deterministically_at_all_widths(
    tmp_path: Path,
) -> None:
    first = _run(tmp_path, "a.db", reverse=False)
    second = _run(tmp_path, "b.db", reverse=False)
    # Input ordering must not matter: the third run serves assets and
    # bars in reversed order and must produce the identical books.
    third = _run(tmp_path, "c.db", reverse=True)
    assert first.books == second.books == third.books
    assert first.members == second.members == third.members
    for width in WIDTHS:
        assert len(first.books[width]) == width
    assert first.n_measurable >= max(WIDTHS)
