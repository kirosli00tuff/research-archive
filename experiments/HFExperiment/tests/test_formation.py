"""The 12-1 formation is deterministic and actually skips a month."""
import random

from hfexperiment import formation as fm

# A synthetic calendar: 21 sessions per month for 15 months.
SESSIONS = [
    f"2025-{m:02d}-{d:02d}" for m in range(1, 13) for d in range(1, 22)
] + [f"2026-{m:02d}-{d:02d}" for m in range(1, 4) for d in range(1, 22)]
SESSION_INDEX = {s: i for i, s in enumerate(SESSIONS)}
FORMATIONS = [s for s in SESSIONS if s.endswith("-01")]


def synthetic_entries(seed: int) -> list[fm.MomentumEntry]:
    rng = random.Random(seed)
    far, near = fm.anchor_sessions(FORMATIONS, "2026-02-01", SESSIONS)
    entries = []
    for i in range(80):
        symbol = f"SYM{i:03d}"
        bars = [(s, 10.0 + rng.random() * 90.0) for s in SESSIONS]
        result = fm.momentum_for_symbol(
            symbol, bars, far, near, SESSION_INDEX)
        assert isinstance(result, fm.MomentumEntry)
        entries.append(result)
    return entries


def test_formation_deterministic_at_all_three_widths() -> None:
    first = synthetic_entries(seed=7)
    second = synthetic_entries(seed=7)
    for width in (5, 20, 50):
        book_a = [e.symbol for e in fm.form_book(first, width)]
        book_b = [e.symbol for e in fm.form_book(second, width)]
        assert book_a == book_b
        assert len(book_a) == width


def test_ties_break_on_symbol_ascending() -> None:
    bar = fm.AnchorBar(date="2026-01-21", close=20.0)
    far = fm.AnchorBar(date="2025-01-21", close=10.0)
    entries = [
        fm.MomentumEntry(symbol=s, momentum=1.0, far_bar=far, near_bar=bar)
        for s in ("BBB", "AAA", "CCC")
    ]
    assert [e.symbol for e in fm.form_book(entries, 2)] == ["AAA", "BBB"]


def test_skip_month_excludes_recent_month_move() -> None:
    """A symbol that only moved in the skipped month must not rank on it.

    PUMP is flat over the measured window and triples in the most recent
    month. STEADY doubles over the measured window. Under 12-1 STEADY
    beats PUMP. Under a plain 12-month lookback PUMP would win. Reverting
    the skip month must fail this test.
    """
    far, near = fm.anchor_sessions(FORMATIONS, "2026-02-01", SESSIONS)
    assert near < "2026-01-01" <= "2026-02-01"

    def series(fn) -> list[tuple[str, float]]:
        return [(s, fn(s)) for s in SESSIONS]

    pump = series(lambda s: 30.0 if s >= "2026-01-01" else 10.0)
    steady = series(lambda s: 20.0 if s >= near else 10.0)

    entries = []
    for symbol, bars in (("PUMP", pump), ("STEADY", steady)):
        result = fm.momentum_for_symbol(
            symbol, bars, far, near, SESSION_INDEX)
        assert isinstance(result, fm.MomentumEntry)
        entries.append(result)
    book = fm.form_book(entries, 1)
    assert book[0].symbol == "STEADY"


def test_anchor_gap_disqualifies_stale_price() -> None:
    far, near = fm.anchor_sessions(FORMATIONS, "2026-03-01", SESSIONS)
    stale_index = SESSION_INDEX[far] - fm.MAX_ANCHOR_GAP_SESSIONS - 1
    assert stale_index >= 0
    stale_cut = SESSIONS[stale_index]
    bars = [(s, 10.0) for s in SESSIONS if s <= stale_cut or s >= near]
    result = fm.momentum_for_symbol("STALE", bars, far, near, SESSION_INDEX)
    assert result == "no_far_anchor_bar"


def test_segment_break_between_anchors_disqualifies() -> None:
    far, near = fm.anchor_sessions(FORMATIONS, "2026-02-01", SESSIONS)
    bars = [(s, 10.0) for s in SESSIONS]
    segments = [(SESSIONS[0], "2025-06-21"), ("2025-08-01", SESSIONS[-1])]
    result = fm.momentum_for_symbol(
        "SPLIT", bars, far, near, SESSION_INDEX, segments=segments)
    assert result == "anchors_span_segments"
