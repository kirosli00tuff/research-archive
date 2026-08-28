"""Register entry H5, Task 1: the registered surface, before any H5 network call.

Every fixture that touches a registered boundary sits ON it, not comfortably
inside it (the InsiderExperiment mutation lesson): a moved 54 bp bar, a moved
20-instrument bar, a moved 0.5 funding share, and a moved weekend boundary
all have a test that fails on the move alone.
"""

from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path

import pytest

from npl.absence import NOT_SERVED, AbsenceReason, Absent, is_absent
from npl.config import CONFIG
from npl.h5 import basis as h5basis
from npl.h5 import calendar as h5cal
from npl.h5 import outcome as h5out
from npl.h5 import priors as h5priors
from npl.h5 import resolution as h5res
from npl.h5 import spend as h5spend
from npl.h5 import stats as h5stats
from npl.h5.gate import (
    Cohorts,
    H5RetrospectiveGated,
    load_cohorts,
    require_ungated,
)
from npl.h5.stores import H5StoreViolation, assert_inside_h5, h5_store
from npl.paths import H5_DIR, H5_REGISTRATION_MD

# --------------------------------------------------------------------------
# Section 2 — the registered resolution mapping
# --------------------------------------------------------------------------


def test_the_three_resolution_tables_partition_their_tickers() -> None:
    """A ticker in two tables would make the mapping pick a winner. It refuses."""
    h5res._check_tables()
    assert set(h5res.RESOLVED) & set(h5res.NON_EQUITY) == set()
    assert set(h5res.RESOLVED) & set(h5res.UNRESOLVABLE) == set()
    assert set(h5res.NON_EQUITY) & set(h5res.UNRESOLVABLE) == set()


def test_bare_ticker_strips_exactly_one_dex_prefix() -> None:
    assert h5res.bare_ticker("xyz:AAPL") == "AAPL"
    assert h5res.bare_ticker("BTC") == "BTC"
    assert h5res.bare_ticker("km:US500") == "US500"


def test_resolution_states_and_kinds() -> None:
    equity = h5res.resolve("xyz:AAPL", "xyz")
    assert equity.state == h5res.STATE_RESOLVED
    assert equity.underlying is not None and equity.underlying.kind == h5res.KIND_EQUITY

    etf = h5res.resolve("xyz:SOXL", "xyz")
    assert etf.underlying is not None and etf.underlying.kind == h5res.KIND_ETF

    index = h5res.resolve("km:US500", "km")
    assert index.underlying is not None and index.underlying.symbol == "SPX"

    crypto = h5res.resolve("hyna:BTC", "hyna")
    assert crypto.state == h5res.STATE_NON_EQUITY
    assert crypto.reason == h5res.CLASS_CRYPTO
    assert crypto.underlying is None

    private = h5res.resolve("vntl:SPACEX", "vntl")
    assert private.state == h5res.STATE_UNRESOLVABLE
    assert private.reason == h5res.REASON_PRIVATE

    house = h5res.resolve("xyz:XYZ100", "xyz")
    assert house.reason == h5res.REASON_HOUSE_INDEX


def test_an_unknown_ticker_is_unresolvable_and_never_guessed() -> None:
    """The mapping is exact-string. A ticker it has never seen resolves to nothing."""
    unknown = h5res.resolve("xyz:NOTATICKER", "xyz")
    assert unknown.state == h5res.STATE_UNRESOLVABLE
    assert unknown.reason == h5res.REASON_NOT_IN_MAPPING
    assert unknown.underlying is None
    assert not unknown.is_resolved


def test_the_same_underlying_resolves_identically_across_dexs() -> None:
    """US500 on km, mkts and abcd's USA500 all name the S&P 500."""
    symbols = {
        h5res.resolve(coin, dex).underlying.symbol  # type: ignore[union-attr]
        for coin, dex in (("km:US500", "km"), ("mkts:US500", "mkts"), ("abcd:USA500", "abcd"))
    }
    assert symbols == {"SPX"}


# --------------------------------------------------------------------------
# Section 5 — the registered market calendar and session tagger
# --------------------------------------------------------------------------


def _utc(text: str) -> datetime:
    return datetime.fromisoformat(text.replace("Z", "+00:00")).astimezone(UTC)


@pytest.mark.parametrize(
    ("moment", "expected"),
    [
        # Boundaries ON the registered edges, in New York local time.
        ("2026-08-28T08:00:00Z", h5cal.TAG_EXTENDED),  # Fri 04:00 ET, premarket opens
        ("2026-08-28T07:59:00Z", h5cal.TAG_CLOSED_WEEKDAY),  # Fri 03:59 ET
        ("2026-08-28T13:30:00Z", h5cal.TAG_REGULAR),  # Fri 09:30 ET, the open
        ("2026-08-28T13:29:00Z", h5cal.TAG_EXTENDED),  # Fri 09:29 ET
        ("2026-08-28T20:00:00Z", h5cal.TAG_EXTENDED),  # Fri 16:00 ET, the close
        ("2026-08-28T19:59:00Z", h5cal.TAG_REGULAR),  # Fri 15:59 ET
        ("2026-08-28T23:59:00Z", h5cal.TAG_EXTENDED),  # Fri 19:59 ET, last post-market minute
        ("2026-08-29T00:00:00Z", h5cal.TAG_CLOSED_WEEKDAY),  # Fri 20:00 ET, post-market shuts
        ("2026-08-29T04:00:00Z", h5cal.TAG_WEEKEND),  # Sat 00:00 ET, the boundary
        ("2026-08-29T03:59:00Z", h5cal.TAG_CLOSED_WEEKDAY),  # Fri 23:59 ET
        ("2026-08-31T04:00:00Z", h5cal.TAG_CLOSED_WEEKDAY),  # Mon 00:00 ET
        ("2026-08-31T03:59:00Z", h5cal.TAG_WEEKEND),  # Sun 23:59 ET
        ("2026-11-26T15:00:00Z", h5cal.TAG_CLOSED_WEEKDAY),  # Thanksgiving, a Thursday
        ("2026-11-27T18:00:00Z", h5cal.TAG_EXTENDED),  # early close, 13:00 ET exactly
        ("2026-11-27T17:59:00Z", h5cal.TAG_REGULAR),  # early close, 12:59 ET
        ("2026-03-02T14:30:00Z", h5cal.TAG_REGULAR),  # 09:30 EST, DST boundary check
    ],
)
def test_session_tags_on_the_registered_boundaries(moment: str, expected: str) -> None:
    assert h5cal.session_tag(_utc(moment)) == expected


def test_saturday_is_never_a_weekday_tag() -> None:
    """The mutation target: `weekday() >= SATURDAY`. A Saturday inside regular
    hours must tag weekend, not regular."""
    saturday_noon_et = _utc("2026-08-29T16:00:00Z")
    assert saturday_noon_et.astimezone(h5cal.EXCHANGE_TZ).weekday() == 5
    assert h5cal.session_tag(saturday_noon_et) == h5cal.TAG_WEEKEND


def test_a_year_outside_the_registered_calendar_refuses() -> None:
    with pytest.raises(h5cal.CalendarOutOfRange):
        h5cal.session_tag(_utc("2030-06-03T14:00:00Z"))


def test_the_tagger_refuses_a_naive_timestamp() -> None:
    with pytest.raises(ValueError, match="naive"):
        h5cal.session_tag(datetime(2026, 8, 28, 14, 0))


def test_every_tag_is_one_of_the_four_registered_ones() -> None:
    assert h5cal.SESSION_TAGS == ("regular", "extended", "closed_weekday", "weekend")


# --------------------------------------------------------------------------
# Section 3 — basis, and the same-snapshot rule
# --------------------------------------------------------------------------

_CTX_PAYLOAD = json.dumps(
    [
        {"universe": [{"name": "AAPL"}, {"name": "NOREF"}]},
        [
            {
                "markPx": "101.0",
                "oraclePx": "100.0",
                "midPx": "100.5",
                "openInterest": "12.5",
                "dayNtlVlm": "9000.0",
                "funding": "0.0000125",
            },
            {"markPx": "50.0", "midPx": "50.1", "openInterest": "3.0"},
        ],
    ]
)


def test_parse_asset_contexts_records_served_fields_and_the_reference_used() -> None:
    ctxs = h5basis.parse_asset_contexts(_CTX_PAYLOAD, "xyz", "snap-1", 1_700_000_000_000)
    assert [c.coin for c in ctxs] == ["xyz:AAPL", "xyz:NOREF"]
    first, second = ctxs
    assert first.reference_field == "oraclePx"
    assert first.funding_served is True
    assert "funding" in first.served_fields
    assert second.reference_field is None
    assert is_absent(second.reference)
    assert second.funding_served is False


def test_basis_is_bp_of_mark_over_the_served_reference() -> None:
    ctxs = h5basis.parse_asset_contexts(_CTX_PAYLOAD, "xyz", "snap-1", 1_700_000_000_000)
    value = h5basis.context_basis_bp(ctxs[0])
    assert isinstance(value, float)
    assert value == pytest.approx(100.0)  # (101 - 100) / 100 = 100 bp


def test_an_unserved_reference_yields_a_recorded_absence_never_a_number() -> None:
    ctxs = h5basis.parse_asset_contexts(_CTX_PAYLOAD, "xyz", "snap-1", 1_700_000_000_000)
    value = h5basis.context_basis_bp(ctxs[1])
    assert isinstance(value, Absent)
    assert value.reason is AbsenceReason.NOT_SERVED
    with pytest.raises(TypeError):
        float(value)


def test_a_basis_across_two_snapshots_is_refused() -> None:
    """Section 3 admits only fields the venue served in the SAME snapshot."""
    mark = h5basis.Served(value=101.0, field="markPx", snapshot_id="snap-1")
    stale = h5basis.Served(value=100.0, field="oraclePx", snapshot_id="snap-0")
    with pytest.raises(h5basis.CrossSnapshotBasis):
        h5basis.basis_bp(mark, stale)


def test_the_registered_reference_fields_exclude_the_book_and_mark_fields() -> None:
    assert h5basis.REFERENCE_FIELDS == ("oraclePx", "indexPx")
    assert set(h5basis.NON_REFERENCE_FIELDS) == {"midPx", "prevDayPx", "impactPxs"}
    assert set(h5basis.REFERENCE_FIELDS) & set(h5basis.NON_REFERENCE_FIELDS) == set()


def test_midpx_is_never_picked_as_a_reference() -> None:
    """A snapshot serving midPx but no oracle must record reference_unserved."""
    ctxs = h5basis.parse_asset_contexts(_CTX_PAYLOAD, "xyz", "snap-1", 1_700_000_000_000)
    assert "midPx" in ctxs[1].served_fields
    assert is_absent(ctxs[1].reference)


def test_a_misaligned_universe_and_context_list_refuses() -> None:
    payload = json.dumps([{"universe": [{"name": "A"}, {"name": "B"}]}, [{"markPx": "1.0"}]])
    with pytest.raises(h5basis.AssetContextShape):
        h5basis.parse_asset_contexts(payload, "xyz", "snap-1", 0)


def _ctx(coin: str, mark: float | None, ref: float | None, snap: str) -> h5basis.AssetContext:
    return h5basis.AssetContext(
        coin=coin,
        dex="xyz",
        snapshot_id=snap,
        at_ms=0,
        served_fields=(),
        mark=(h5basis.Served(mark, "markPx", snap) if mark is not None else NOT_SERVED),
        reference=(h5basis.Served(ref, "oraclePx", snap) if ref is not None else NOT_SERVED),
        open_interest=NOT_SERVED,
        day_notional_volume=NOT_SERVED,
        funding_served=True,
    )


def test_an_absent_reference_in_a_series_is_never_carried_forward() -> None:
    """The mutation target: a gap must stay a gap and the n must drop."""
    series = h5basis.basis_series(
        [
            _ctx("xyz:AAPL", 101.0, 100.0, "s0"),
            _ctx("xyz:AAPL", 102.0, None, "s1"),
            _ctx("xyz:AAPL", 103.0, 100.0, "s2"),
        ]
    )
    assert len(series) == 3
    assert is_absent(series[1])
    served = h5basis.present_values(series)
    assert len(served) == 2
    assert served[0] == pytest.approx(100.0)
    assert served[1] == pytest.approx(300.0)
    assert h5basis.absence_reasons(series) == {"not_served": 1}


def test_a_zero_reference_is_a_recorded_absence_not_an_infinity() -> None:
    value = h5basis.context_basis_bp(_ctx("xyz:X", 1.0, 0.0, "s0"))
    assert isinstance(value, Absent)
    assert value.reason is AbsenceReason.ZERO_DENOMINATOR


# --------------------------------------------------------------------------
# Descriptive statistics — every figure with its n
# --------------------------------------------------------------------------


def test_summarize_reports_n_median_iqr_and_exceedance_shares() -> None:
    values: list[float | Absent] = [10.0, -20.0, 60.0, NOT_SERVED, 30.0]
    summary = h5stats.summarize(values, floor_bp=18.0, viable_bp=54.0)
    assert summary.n == 4
    assert summary.n_absent == 1
    assert summary.median_abs_bp == pytest.approx(25.0)  # |10|,|20|,|30|,|60|
    assert summary.q1_abs_bp == pytest.approx(17.5)
    assert summary.q3_abs_bp == pytest.approx(37.5)
    assert summary.iqr_abs_bp == pytest.approx(20.0)
    assert summary.share_over_floor == pytest.approx(0.75)
    assert summary.share_over_viable == pytest.approx(0.25)


def test_summarize_of_an_all_absent_sample_reports_zero_n_and_no_median() -> None:
    summary = h5stats.summarize([NOT_SERVED, NOT_SERVED], floor_bp=18.0, viable_bp=54.0)
    assert summary.n == 0 and summary.n_absent == 2
    assert summary.median_abs_bp is None and summary.iqr_abs_bp is None


def test_a_median_of_an_empty_sample_refuses_rather_than_returning_zero() -> None:
    with pytest.raises(ValueError, match="empty sample"):
        h5stats.median([])


# --------------------------------------------------------------------------
# Section 6 — the outcome map, on its registered boundaries
# --------------------------------------------------------------------------


def test_the_thresholds_are_arithmetic_on_the_registered_cost_band() -> None:
    assert h5out.cost_floor_bp() == CONFIG.hip3_round_trip_bp[1] == 18.0
    assert h5out.viable_threshold_bp() == 54.0
    assert CONFIG.h5_viable_basis_multiple == 3.0


def _fire(
    *,
    n_ref: int = 20,
    n_cov: int = 20,
    medians: dict[str, float] | None = None,
    funding: int = 10,
    kind: str = h5out.SERIES_REGISTERED_BASIS,
) -> h5out.Verdict:
    tags = medians if medians is not None else {"regular": 60.0}
    return h5out.fire(
        series_kind=kind,
        instruments_with_reference=n_ref,
        instruments_meeting_coverage=n_cov,
        median_abs_bp_by_tag=dict(tags),
        n_by_tag=dict.fromkeys(tags, 100),
        funding_served_instruments=funding,
    )


def test_viable_fires_only_above_the_54_bp_bar() -> None:
    assert _fire(medians={"regular": 54.01}).state == h5out.STATE_VIABLE
    on_the_bar = _fire(medians={"regular": 54.0})
    assert on_the_bar.state == h5out.STATE_INDETERMINATE


def test_indeterminate_between_the_floor_and_the_bar_including_on_the_floor() -> None:
    assert _fire(medians={"regular": 18.0}).state == h5out.STATE_INDETERMINATE
    assert _fire(medians={"regular": 35.0}).state == h5out.STATE_INDETERMINATE


def test_closed_when_every_tag_sits_under_the_floor() -> None:
    verdict = _fire(medians={"regular": 17.99, "weekend": 2.0})
    assert verdict.state == h5out.STATE_CLOSED
    assert "cost floor in every session tag" in verdict.reasons[0]


def test_one_tag_over_the_floor_is_not_closed() -> None:
    assert _fire(medians={"regular": 18.0, "weekend": 2.0}).state == h5out.STATE_INDETERMINATE


def test_closed_on_the_reference_count_bar_which_sits_at_twenty() -> None:
    assert _fire(n_ref=19, n_cov=19).state == h5out.STATE_CLOSED
    assert _fire(n_ref=20, n_cov=20).state == h5out.STATE_VIABLE


def test_closed_when_funding_is_served_on_fewer_than_half() -> None:
    """The bar sits AT one half: 10 of 20 passes, 9 of 20 closes."""
    assert _fire(funding=10).state == h5out.STATE_VIABLE
    closed = _fire(funding=9)
    assert closed.state == h5out.STATE_CLOSED
    assert closed.funding_share == pytest.approx(0.45)


def test_pending_while_the_census_window_is_open() -> None:
    """20 references but only 5 with 30 days of coverage: the map has not fired."""
    verdict = _fire(n_ref=20, n_cov=5)
    assert verdict.state == h5out.STATE_PENDING
    assert verdict.state not in h5out.TERMINAL_STATES
    assert "census window is open" in verdict.reasons[0]


def test_a_named_secondary_may_close_but_never_fire_viable() -> None:
    high = _fire(medians={"regular": 300.0}, kind=h5out.SERIES_SECONDARY_DEVIATION)
    assert high.state == h5out.STATE_INDETERMINATE
    assert "never fire VIABLE" in high.reasons[0]
    low = _fire(medians={"regular": 1.0}, kind=h5out.SERIES_SECONDARY_DEVIATION)
    assert low.state == h5out.STATE_CLOSED


def test_an_unregistered_series_kind_is_refused() -> None:
    with pytest.raises(h5out.UnregisteredSeriesKind):
        _fire(kind="whatever_i_like")


def test_the_verdict_carries_every_input_figure_beside_the_state() -> None:
    verdict = _fire(medians={"regular": 60.0, "weekend": 20.0}, funding=15)
    assert verdict.instruments_with_reference == 20
    assert verdict.instruments_meeting_coverage == 20
    assert verdict.funding_served_instruments == 15
    assert verdict.funding_share == pytest.approx(0.75)
    assert verdict.n_by_tag == {"regular": 100, "weekend": 100}
    assert verdict.max_median_abs_bp == pytest.approx(60.0)
    assert verdict.floor_bp == 18.0 and verdict.viable_bp == 54.0


# --------------------------------------------------------------------------
# Section 7 — spend and pacing
# --------------------------------------------------------------------------


def test_the_pass_budget_is_stated_as_arithmetic() -> None:
    budget = h5spend.daily_pass_budget(dexs=10, instruments=151)
    assert budget.total == 1 + 10 + 10 + 151 == 172
    assert h5spend.share_of_daily_cap(budget) == pytest.approx(172 / 20_000)


def test_a_pass_over_the_h5_cap_is_refused_before_anything_is_sent() -> None:
    with pytest.raises(h5spend.H5BudgetExceeded, match="Nothing was sent"):
        h5spend.refuse_over_h5_cap(h5spend.daily_pass_budget(dexs=10, instruments=5_000))


def test_the_retrospective_budget_and_window_come_from_the_registered_config() -> None:
    assert h5spend.retro_request_budget(151) == 151 * CONFIG.h5_retro_page_budget
    start, end = h5spend.retro_window_ms(1_800_000_000_000)
    assert end - start == CONFIG.h5_retro_lookback_days * 86_400_000


# --------------------------------------------------------------------------
# The write containment gate — H2's stores are read-only to this entry
# --------------------------------------------------------------------------


def test_an_h5_write_outside_data_h5_is_refused() -> None:
    """Produced, not asserted: the refusal fires on a real H2 store path."""
    with pytest.raises(H5StoreViolation, match="read-only to this entry"):
        h5_store(Path("data/controls/h2_pairs.jsonl"))
    with pytest.raises(H5StoreViolation):
        assert_inside_h5(Path("data/state/fresh_plan.jsonl"))
    with pytest.raises(H5StoreViolation):
        assert_inside_h5(H5_DIR / ".." / "state" / "watcher.jsonl")


def test_an_h5_write_inside_data_h5_is_admitted(tmp_path: Path) -> None:
    ledger = h5_store(H5_DIR / "snapshots.jsonl")
    assert ledger.path.resolve().parent == H5_DIR.resolve()
    assert tmp_path.exists()


# --------------------------------------------------------------------------
# The retrospective blindness gate
# --------------------------------------------------------------------------


def _cohorts() -> Cohorts:
    return Cohorts(
        generating_sample=frozenset({"xyz:AAPL"}),
        fresh_plan=frozenset({"xyz:AVGO"}),
        h2_pairs=frozenset({"xyz:AVGO", "BTC"}),
    )


def test_the_retrospective_gate_refuses_every_registered_cohort_coin() -> None:
    cohorts = _cohorts()
    for coin, claims in (
        ("xyz:AAPL", ["generating_sample"]),
        ("xyz:AVGO", ["fresh_plan", "h2_pairs"]),
        ("BTC", ["h2_pairs"]),
    ):
        with pytest.raises(H5RetrospectiveGated) as excinfo:
            require_ungated(coin, cohorts)
        assert str(claims) in str(excinfo.value)


def test_a_coin_in_no_cohort_passes_the_gate() -> None:
    require_ungated("xyz:GOOGL", _cohorts())


def test_the_cohorts_load_from_the_real_ledgers_read_only() -> None:
    """The ledgers are read so the quarantine can be honoured; nothing is written."""
    before = {
        path: path.read_bytes()
        for path in (
            Path("data/state/generating_sample.json"),
            Path("data/state/fresh_plan.jsonl"),
            Path("data/controls/h2_pairs.jsonl"),
        )
        if path.exists()
    }
    if len(before) < 3:
        pytest.skip("cohort ledgers not present in this checkout")
    cohorts = load_cohorts()
    assert len(cohorts.generating_sample) > 0
    assert len(cohorts.fresh_plan) > 0
    assert len(cohorts.h2_pairs) > 0
    for path, payload in before.items():
        assert path.read_bytes() == payload


# --------------------------------------------------------------------------
# Section 9 — the reserved operator slot
# --------------------------------------------------------------------------


def test_the_h5_operator_slot_is_empty_and_blocks_the_successor_draft() -> None:
    if not H5_REGISTRATION_MD.exists():
        pytest.skip("the H5 registration is not committed yet")
    assert h5priors.operator_prior() is None
    with pytest.raises(h5priors.H5OperatorPriorMissing, match="successor hypothesis"):
        h5priors.require_operator_prior_for_successor()


def test_a_filled_slot_parses_only_in_the_registered_shape(tmp_path: Path) -> None:
    filled = tmp_path / "REGISTRATION.md"
    filled.write_text("Operator prior on the H5 family: 0.12 (independent)\n", encoding="utf-8")
    assert h5priors.operator_prior(filled) == (0.12, "independent")
    loose = tmp_path / "loose.md"
    loose.write_text("Operator prior on the H5 family: probably low\n", encoding="utf-8")
    assert h5priors.operator_prior(loose) is None


def test_the_assistant_prior_is_the_recorded_number_and_not_the_operators() -> None:
    assert h5priors.assistant_prior() == 0.05 == CONFIG.h5_assistant_prior_edge
