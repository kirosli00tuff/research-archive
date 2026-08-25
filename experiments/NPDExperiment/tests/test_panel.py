"""The panel draw reproduces from the registered seed and the date alone."""

from __future__ import annotations

import pytest

from npd.config import CONFIG
from npd.data.panel import draw, seed_for, stratum_of


def pool(n: int = 500) -> list[tuple[str, int]]:
    return [(f"S{i:04d}", i) for i in range(1, n + 1)]


def test_the_seed_depends_on_the_date_and_the_registered_seed() -> None:
    assert seed_for("2025-01-02") == seed_for("2025-01-02")
    assert seed_for("2025-01-02") != seed_for("2025-01-03")


def test_the_draw_reproduces_exactly() -> None:
    a = draw("2025-01-02", "2025-01-02", pool())
    b = draw("2025-01-02", "2025-01-02", pool())
    assert a is not None and b is not None
    assert a.picks == b.picks


def test_two_dates_draw_different_panels() -> None:
    a = draw("2025-01-02", "2025-01-02", pool())
    b = draw("2025-01-03", "2025-01-02", pool())
    assert a is not None and b is not None
    assert a.picks != b.picks


def test_the_draw_is_the_registered_size() -> None:
    d = draw("2025-01-02", "2025-01-02", pool())
    assert d is not None
    assert len(d.picks) == CONFIG.panel_size
    assert len(set(d.symbols)) == CONFIG.panel_size


def test_the_draw_spans_every_stratum() -> None:
    d = draw("2025-01-02", "2025-01-02", pool())
    assert d is not None
    strata = {stratum_of(rank, 500, CONFIG.strata_count) for _s, rank in d.picks}
    assert strata == set(range(CONFIG.strata_count))


def test_a_thin_pool_returns_none_rather_than_filling_short() -> None:
    assert draw("2025-01-02", "2025-01-02", pool(20)) is None


def test_strata_split_the_rank_range() -> None:
    assert stratum_of(1, 500, 5) == 0
    assert stratum_of(100, 500, 5) == 0
    assert stratum_of(101, 500, 5) == 1
    assert stratum_of(500, 500, 5) == 4
    with pytest.raises(ValueError):
        stratum_of(0, 500, 5)
    with pytest.raises(ValueError):
        stratum_of(501, 500, 5)
