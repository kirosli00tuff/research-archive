"""Pins pmexperiment.registry to REGISTRATION.md, figure by figure.

If a registered constant changes in code without a numbered amendment in the
document, or the document changes without the code following, this file
fails. The reader folds whitespace for the same reason test_honesty.py does:
hard wraps are not content.
"""

from itertools import pairwise
from pathlib import Path

from pmexperiment import registry

ROOT = Path(__file__).resolve().parent.parent


def _registration() -> str:
    raw = (ROOT / "REGISTRATION.md").read_text(encoding="utf-8")
    return " ".join(raw.split())


def test_effect_band_is_pinned_to_the_document() -> None:
    doc = _registration()
    assert "0.02 to 0.08" in doc
    assert registry.EFFECT_BAND_LO == 0.02
    assert registry.EFFECT_BAND_HI == 0.08


def test_z_critical_is_pinned() -> None:
    assert "z = 2.0 two-sided" in _registration()
    assert registry.Z_CRITICAL == 2.0


def test_tail_cell_is_pinned() -> None:
    doc = _registration()
    assert "the union of 1–10 and 91–99" in doc  # noqa: RUF001
    assert registry.TAIL_BUCKETS_CENTS == ((1, 10), (91, 99))
    assert registry.TAIL_BUCKETS_CENTS[0] in registry.BUCKET_EDGES_CENTS
    assert registry.TAIL_BUCKETS_CENTS[1] in registry.BUCKET_EDGES_CENTS


def test_buckets_tile_the_price_grid_without_gap_or_overlap() -> None:
    edges = registry.BUCKET_EDGES_CENTS
    assert edges[0][0] == 1
    assert edges[-1][1] == 99
    for (_, hi), (lo_next, _) in pairwise(edges):
        assert lo_next == hi + 1


def test_snapshots_are_pinned() -> None:
    doc = _registration()
    assert "`close_time` minus 24 hours" in doc
    assert "`close_time` minus 30 days" in doc
    assert registry.SNAPSHOT_S24_HOURS == 24
    assert registry.SNAPSHOT_S30_DAYS == 30
    assert registry.PERMITTED_MIN_MATURITY_DAYS == 30


def test_sampling_rule_is_pinned() -> None:
    doc = _registration()
    assert "m = 2,000" in doc
    assert "seed 20260829" in doc
    assert "Wilson 95% lower bound" in doc
    assert registry.UNRESTRICTED_SAMPLE_SIZE == 2000
    assert registry.SAMPLE_SEED == 20260829
    assert registry.WILSON_Z == 1.96


def test_access_floor_is_pinned() -> None:
    doc = _registration()
    assert "At least 1,000 settled markets are enumerable" in doc
    assert "at most five records" in doc
    assert registry.ACCESS_MIN_SETTLED_MARKETS == 1000
    assert registry.ACCESS_OUTCOME_PRESENCE_MAX_RECORDS == 5


def test_volume_floor_is_pinned_to_amendment_five() -> None:
    """The floor is the benchmark's, so the document must show its provenance.

    Pinning the citation as well as the number matters here: a bare 1000.0
    could be re-justified after a count is seen, and the whole point of
    Amendment 5 is that this number was chosen by someone else first.
    """
    doc = _registration()
    assert "total traded volume ≥ $1,000 USD per contract" in doc
    assert "total staked ≥ $1,000, final spread ≤ 20c" in doc
    assert registry.PERMITTED_MIN_VOLUME_USD == 1000.0


def test_cost_model_is_pinned() -> None:
    doc = _registration()
    assert "2 cents per contract per side" in doc
    assert "1 cent half-spread" in doc
    assert "1.5 % of committed principal per direction" in doc
    assert registry.FEE_PER_SIDE_USD == 0.02
    assert registry.FEE_SIDES == 2
    assert registry.HALF_SPREAD_USD == 0.01
    assert registry.FX_PER_DIRECTION == 0.015
    assert registry.FX_DIRECTIONS == 2
