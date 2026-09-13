"""Amendment H2-5 section 2: the tiered control rule.

Boundary fixtures sit ON the registered boundary — the 180-day age gate and
the 0.95 funding-coverage bar are exercised at the exact threshold, so a
moved bar cannot pass unnoticed. Every refusal is produced through the real
path.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from npl.absence import NO_CANDLES
from npl.blindness import FundingRow
from npl.census import CensusRow
from npl.clock import MS_PER_DAY, MS_PER_HOUR
from npl.config import CONFIG
from npl.controls import PostEntryRead
from npl.coverage import coverage_by_class_pair, coverage_by_tier
from npl.ledger.append_only import AppendOnlyLedger
from npl.pairtype import PAIR_TYPE_SAME_DEX
from npl.paths import H2_PAIRS_LEDGER
from npl.register.assetclass import (
    CLASS_COMMODITY,
    CLASS_CRYPTO,
    CLASS_EQUITY,
    CLASS_ETF,
    CLASS_INDEX,
    CLASS_RATES,
)
from npl.register.fallback import admissible_census_rows
from npl.register.forward import latest_census
from npl.register.pairs import (
    PairNet,
    class_pair_stratum,
    registered_plan,
    run_h2_look,
    tier_stratum,
)
from npl.register.tiered import (
    STATE_ASSIGNED,
    STATE_NO_CLASS_ELDER,
    STATE_UNCLASSIFIABLE,
    CandidateRef,
    CrossComplexControl,
    SupersededLedgerWrite,
    TieredAssignment,
    TieredExclusion,
    assert_coherent,
    assert_not_superseded,
    assign_control_tiered,
    class_pair_of_row,
    rows_from,
    tier_of_row,
    tier_pool,
)
from npl.tier import (
    TIER_ANY_DEX_EQUITY_COMPLEX,
    TIER_ANY_DEX_EXACT_CLASS,
    TIER_SAME_DEX_EXACT_CLASS,
)

ENTRY = 1_760_000_000_000 - (1_760_000_000_000 % MS_PER_HOUR)
AGED = ENTRY - 400 * MS_PER_DAY
FLOOR_BP = 36.0


def _pair_net(
    net: float,
    tier: int = 1,
    class_pair: str = "equity->equity",
) -> PairNet:
    """One synthetic pair net. The reader has seen only fixtures like this."""
    return PairNet(
        event_coin="Y",
        control_coin="E",
        dex="xyz",
        cohort="backfill",
        pair_type=PAIR_TYPE_SAME_DEX,
        tier=tier,
        class_pair=class_pair,
        truncated_young=False,
        truncated_elder=False,
        pair_central_cost_bp=FLOOR_BP,
        net_30=net,
        net_90=NO_CANDLES,
        young_funding_term_30=NO_CANDLES,
        young_price_term_30=NO_CANDLES,
        elder_funding_term_30=NO_CANDLES,
        elder_price_term_30=NO_CANDLES,
    )


def _rows(rate: float, hours: int = 168, end_ms: int = ENTRY) -> tuple[FundingRow, ...]:
    """A fully covered trailing window at a constant rate, ending at end_ms."""
    return tuple(
        FundingRow(time_ms=end_ms - i * MS_PER_HOUR, rate=rate) for i in reversed(range(hours))
    )


# Each fixture candidate is a (ref, rows) pair: the ref decides tier
# membership, the rows are materialised only for the tiers actually consulted.
_TRAILS: dict[str, tuple[FundingRow, ...]] = {}


def _cand(
    coin: str,
    dex: str,
    asset_class: str,
    rate: float,
    hours: int = 168,
    listing_open_ms: int = AGED,
) -> CandidateRef:
    _TRAILS[coin] = _rows(rate, hours=hours)
    return CandidateRef(
        coin=coin, dex=dex, asset_class=asset_class, listing_open_ms=listing_open_ms
    )


def _census(coin: str, dex: str, first_open: int, last_close: int) -> CensusRow:
    return CensusRow(
        coin=coin,
        dex=dex,
        event_type="hip3" if dex else "vanilla",
        hyperp_source="",
        is_delisted=False,
        sz_decimals=2,
        max_leverage=10,
        state="stored",
        first_1d_open_ms=first_open,
        last_1d_close_ms=last_close,
        candle_rows=100,
        funding_state="stored",
        first_funding_time_ms=first_open,
        funding_page_rows=100,
        recorded_at="t",
    )


def _assign(
    candidates: list[CandidateRef],
    tmp_path: Path,
    coin: str = "xyz:AAPL",
    dex: str = "xyz",
    rate: float = 1e-5,
) -> TieredAssignment | TieredExclusion:
    return assign_control_tiered(
        coin,
        dex,
        ENTRY,
        _rows(rate),
        candidates,
        rows_from(_TRAILS),
        CONFIG,
        pairs_path=tmp_path / "v2.jsonl",
    )


# ------------------------------------------------------- the tier order ----


def test_tier_1_wins_even_when_a_tier_2_elder_is_the_nearer_funding_match(
    tmp_path: Path,
) -> None:
    """A higher tier always wins. The tier-2 elder here is the better match."""
    same_dex = _cand("xyz:MSFT", "xyz", CLASS_EQUITY, 5e-5)
    nearer_other_dex = _cand("para:NET", "para", CLASS_EQUITY, 1e-5)
    result = _assign([same_dex, nearer_other_dex], tmp_path)
    assert isinstance(result, TieredAssignment)
    assert result.tier == TIER_SAME_DEX_EXACT_CLASS
    assert result.control_coin == "xyz:MSFT"
    assert result.class_pair == "equity->equity"


def test_tier_2_is_reached_only_when_no_same_dex_elder_of_the_class_exists(
    tmp_path: Path,
) -> None:
    result = _assign([_cand("para:NET", "para", CLASS_EQUITY, 2e-5)], tmp_path)
    assert isinstance(result, TieredAssignment)
    assert result.tier == TIER_ANY_DEX_EXACT_CLASS
    assert result.control_dex == "para"
    assert result.class_pair == "equity->equity"


def test_tier_3_is_reached_only_when_no_exact_class_elder_exists_anywhere(
    tmp_path: Path,
) -> None:
    """An `etf` leg with no `etf` elder takes an equity-complex one at tier 3."""
    result = _assign(
        [_cand("xyz:MSFT", "xyz", CLASS_EQUITY, 2e-5)], tmp_path, coin="xyz:SMH", dex="xyz"
    )
    assert isinstance(result, TieredAssignment)
    assert result.tier == TIER_ANY_DEX_EQUITY_COMPLEX
    assert result.class_pair == "etf->equity"


def test_a_same_dex_elder_of_the_wrong_class_does_not_win_tier_1(tmp_path: Path) -> None:
    """The H2-3 defect, refused: funding proximity never beats the class."""
    perfect_match_wrong_class = _cand("xyz:COPPER", "xyz", CLASS_COMMODITY, 1e-5)
    distant_right_class = _cand("para:NET", "para", CLASS_EQUITY, 9e-4)
    result = _assign([perfect_match_wrong_class, distant_right_class], tmp_path)
    assert isinstance(result, TieredAssignment)
    assert result.control_coin == "para:NET"
    assert result.tier == TIER_ANY_DEX_EXACT_CLASS


# ------------------------------------------ cross-complex, refused always ---


@pytest.mark.parametrize("leg", [CLASS_RATES, CLASS_COMMODITY, CLASS_CRYPTO])
def test_tier_3_is_unavailable_to_any_leg_outside_the_equity_complex(leg: str) -> None:
    """fx, rates, commodity and vol legs get an empty tier-3 pool, by rule."""
    pool = tier_pool(
        TIER_ANY_DEX_EQUITY_COMPLEX, "para", leg, [_cand("xyz:MSFT", "xyz", CLASS_EQUITY, 1e-5)]
    )
    assert pool == []


def test_a_rates_leg_with_no_rates_elder_is_excluded_not_rescued_by_tier_3(
    tmp_path: Path,
) -> None:
    """`para:10Y` and `mkts:USBOND` are exactly this case in the real sample."""
    result = _assign(
        [
            _cand("xyz:MSFT", "xyz", CLASS_EQUITY, 1e-5),
            _cand("mkts:US500", "mkts", CLASS_INDEX, 1e-5),
        ],
        tmp_path,
        coin="para:10Y",
        dex="para",
    )
    assert isinstance(result, TieredExclusion)
    assert result.state == STATE_NO_CLASS_ELDER
    assert result.event_class == CLASS_RATES
    assert result.tier_pool_sizes == (0, 0, 0)


@pytest.mark.parametrize("tier", [TIER_SAME_DEX_EXACT_CLASS, TIER_ANY_DEX_EXACT_CLASS])
def test_the_coherence_refusal_is_produced_at_tiers_1_and_2(tier: int) -> None:
    with pytest.raises(CrossComplexControl, match="the exact class only"):
        assert_coherent(CLASS_EQUITY, CLASS_CRYPTO, tier)


def test_the_coherence_refusal_is_produced_at_tier_3_for_a_non_complex_leg() -> None:
    with pytest.raises(CrossComplexControl, match="equity-complex"):
        assert_coherent(CLASS_RATES, CLASS_EQUITY, TIER_ANY_DEX_EQUITY_COMPLEX)
    with pytest.raises(CrossComplexControl, match="equity-complex"):
        assert_coherent(CLASS_EQUITY, CLASS_COMMODITY, TIER_ANY_DEX_EQUITY_COMPLEX)


def test_an_unregistered_tier_is_a_loud_refusal_never_a_pass_through() -> None:
    with pytest.raises(CrossComplexControl, match="not a registered tier"):
        assert_coherent(CLASS_EQUITY, CLASS_EQUITY, 4)
    with pytest.raises(CrossComplexControl, match="not a registered tier"):
        tier_pool(4, "xyz", CLASS_EQUITY, [])


def test_every_admitted_pair_is_within_one_complex(tmp_path: Path) -> None:
    """The whole point of the amendment, stated as one invariant."""
    from npl.register.assetclass import in_equity_complex

    for leg, elder, expect_pair in (
        (CLASS_EQUITY, _cand("xyz:MSFT", "xyz", CLASS_EQUITY, 1e-5), True),
        (CLASS_ETF, _cand("xyz:MSFT", "xyz", CLASS_EQUITY, 1e-5), True),
        (CLASS_CRYPTO, _cand("xyz:MSFT", "xyz", CLASS_EQUITY, 1e-5), False),
    ):
        coin = {"equity": "xyz:AAPL", "etf": "xyz:SMH", "crypto": "PONS"}[leg]
        dex = "" if leg == CLASS_CRYPTO else "xyz"
        result = assign_control_tiered(
            coin,
            dex,
            ENTRY,
            _rows(1e-5),
            [elder],
            rows_from(_TRAILS),
            CONFIG,
            pairs_path=tmp_path / f"{leg}.jsonl",
        )
        assert isinstance(result, TieredAssignment) is expect_pair
        if isinstance(result, TieredAssignment):
            same = result.event_class == result.control_class
            complexed = in_equity_complex(result.event_class) and in_equity_complex(
                result.control_class
            )
            assert same or complexed


# ----------------------------------------------- the trailing-only pin -----


def test_a_post_entry_funding_row_on_a_candidate_raises_through_the_tiered_path(
    tmp_path: Path,
) -> None:
    """The registered mutation target. Produced, never asserted."""
    poisoned = _cand("xyz:MSFT", "xyz", CLASS_EQUITY, 1e-5)
    _TRAILS["xyz:MSFT"] = (*_rows(1e-5), FundingRow(ENTRY + MS_PER_HOUR, 1e-5))
    with pytest.raises(PostEntryRead, match="reads no row stamped after"):
        _assign([poisoned], tmp_path)


def test_a_post_entry_funding_row_on_the_event_leg_raises_through_the_tiered_path(
    tmp_path: Path,
) -> None:
    with pytest.raises(PostEntryRead, match="extend past its entry"):
        assign_control_tiered(
            "xyz:AAPL",
            "xyz",
            ENTRY,
            (*_rows(1e-5), FundingRow(ENTRY + MS_PER_HOUR, 1e-5)),
            [_cand("xyz:MSFT", "xyz", CLASS_EQUITY, 1e-5)],
            rows_from(_TRAILS),
            CONFIG,
            pairs_path=tmp_path / "v2.jsonl",
        )


# ------------------------------------ the superseded ledger, write-refused --


def test_writing_into_the_superseded_h2_pairs_ledger_is_refused() -> None:
    with pytest.raises(SupersededLedgerWrite, match="superseded"):
        assert_not_superseded(H2_PAIRS_LEDGER)


def test_the_superseded_refusal_fires_before_any_row_is_built(tmp_path: Path) -> None:
    """The refusal is at the top of the assignment, not after the work."""
    with pytest.raises(SupersededLedgerWrite):
        assign_control_tiered(
            "xyz:AAPL",
            "xyz",
            ENTRY,
            _rows(1e-5),
            [_cand("xyz:MSFT", "xyz", CLASS_EQUITY, 1e-5)],
            rows_from(_TRAILS),
            CONFIG,
            pairs_path=H2_PAIRS_LEDGER,
        )


def test_a_relative_path_to_the_superseded_ledger_is_refused_too() -> None:
    """Resolution happens before comparison; a relative spelling is the same file."""
    with pytest.raises(SupersededLedgerWrite):
        assert_not_superseded(Path("data/controls/h2_pairs.jsonl"))


# ------------------------------------------------------- the exclusions ----


def test_an_unclassifiable_event_is_recorded_with_its_reason_never_defaulted(
    tmp_path: Path,
) -> None:
    result = _assign(
        [_cand("xyz:MSFT", "xyz", CLASS_EQUITY, 1e-5)], tmp_path, coin="xyz:BOT", dex="xyz"
    )
    assert isinstance(result, TieredExclusion)
    assert result.state == STATE_UNCLASSIFIABLE
    assert result.reason == "ambiguous_ticker"
    assert result.event_class is None


def test_an_unclassifiable_event_writes_no_pair_row(tmp_path: Path) -> None:
    ledger = tmp_path / "v2.jsonl"
    _assign([_cand("xyz:MSFT", "xyz", CLASS_EQUITY, 1e-5)], tmp_path, coin="xyz:QNT")
    assert not ledger.exists() or AppendOnlyLedger(ledger).read().rows == []


def test_an_event_with_an_empty_candidate_set_is_excluded_no_class_elder(
    tmp_path: Path,
) -> None:
    result = _assign([], tmp_path)
    assert isinstance(result, TieredExclusion)
    assert result.state == STATE_NO_CLASS_ELDER
    assert result.event_class == CLASS_EQUITY


# ------------------------------------------------- boundaries, exactly on --


def test_an_elder_listed_exactly_180_days_before_entry_is_admissible() -> None:
    """ON the boundary. A moved age gate fails this test, not the next one."""
    exactly = ENTRY - CONFIG.control_min_age_days * MS_PER_DAY
    latest = latest_census([_census("xyz:MSFT", "xyz", exactly, ENTRY)])
    assert [r.coin for r in admissible_census_rows(latest, ENTRY, "xyz:AAPL")] == ["xyz:MSFT"]


def test_an_elder_listed_one_millisecond_inside_180_days_is_refused() -> None:
    one_ms_young = ENTRY - CONFIG.control_min_age_days * MS_PER_DAY + 1
    latest = latest_census([_census("xyz:MSFT", "xyz", one_ms_young, ENTRY)])
    assert admissible_census_rows(latest, ENTRY, "xyz:AAPL") == []


def test_coverage_exactly_at_the_bar_admits_and_one_hour_under_it_skips(
    tmp_path: Path,
) -> None:
    """0.95 of 168 hours is 159.6, so 160 served hours clears and 159 does not."""
    bar_hours = CONFIG.funding_coverage_bar * CONFIG.control_trailing_window_hours
    assert bar_hours == pytest.approx(159.6)

    at_bar = _cand("xyz:MSFT", "xyz", CLASS_EQUITY, 1e-5, hours=160)
    result = _assign([at_bar], tmp_path / "a")
    assert isinstance(result, TieredAssignment)
    assert result.candidates_skipped_low_coverage == 0

    under_bar = _cand("xyz:MSFT", "xyz", CLASS_EQUITY, 1e-5, hours=159)
    refused = _assign([under_bar], tmp_path / "b")
    assert isinstance(refused, TieredExclusion)
    assert refused.state == STATE_NO_CLASS_ELDER
    assert "1 under the coverage bar" in refused.reason


# ------------------------------------------------------------ the ledger ---


def test_an_assigned_row_carries_its_tier_and_class_pair(tmp_path: Path) -> None:
    ledger = tmp_path / "v2.jsonl"
    result = _assign([_cand("xyz:MSFT", "xyz", CLASS_EQUITY, 2e-5)], tmp_path)
    assert isinstance(result, TieredAssignment)
    rows = AppendOnlyLedger(ledger).read().rows
    assert len(rows) == 1
    assert tier_of_row(rows[0]) == TIER_SAME_DEX_EXACT_CLASS
    assert class_pair_of_row(rows[0]) == "equity->equity"
    assert rows[0]["state"] == STATE_ASSIGNED
    assert rows[0]["funding_distance"] == pytest.approx(1e-5)


def test_a_row_without_a_tier_is_a_loud_refusal_never_imputed() -> None:
    with pytest.raises(ValueError, match="unregistered tier"):
        tier_of_row({"event_coin": "xyz:AAPL"})


def test_a_row_without_a_class_pair_is_a_loud_refusal_never_imputed() -> None:
    with pytest.raises(ValueError, match="carries no class_pair"):
        class_pair_of_row({"event_coin": "xyz:AAPL"})


def test_append_false_assigns_without_touching_any_ledger(tmp_path: Path) -> None:
    ledger = tmp_path / "v2.jsonl"
    result = assign_control_tiered(
        "xyz:AAPL",
        "xyz",
        ENTRY,
        _rows(1e-5),
        [_cand("xyz:MSFT", "xyz", CLASS_EQUITY, 2e-5)],
        rows_from(_TRAILS),
        CONFIG,
        pairs_path=ledger,
        append=False,
    )
    assert isinstance(result, TieredAssignment)
    assert not ledger.exists()


# ------------------------------------------------ laziness, which is spend --


def test_no_trailing_window_is_materialised_for_a_tier_nobody_reaches(
    tmp_path: Path,
) -> None:
    """A fetch is a charge against the daily cap, so an unreached tier costs nothing."""
    asked: list[str] = []

    def counting(ref: CandidateRef) -> tuple[FundingRow, ...]:
        asked.append(ref.coin)
        return _TRAILS[ref.coin]

    same_dex = _cand("xyz:MSFT", "xyz", CLASS_EQUITY, 2e-5)
    other_dex = _cand("para:NET", "para", CLASS_EQUITY, 1e-5)
    other_class = _cand("xyz:SMH", "xyz", CLASS_ETF, 1e-5)
    result = assign_control_tiered(
        "xyz:AAPL",
        "xyz",
        ENTRY,
        _rows(1e-5),
        [same_dex, other_dex, other_class],
        counting,
        CONFIG,
        pairs_path=tmp_path / "v2.jsonl",
    )
    assert isinstance(result, TieredAssignment)
    assert result.tier == TIER_SAME_DEX_EXACT_CLASS
    assert asked == ["xyz:MSFT"], f"tier 1 resolved, yet {asked} were fetched"


def test_an_elder_in_two_tier_pools_is_materialised_exactly_once(tmp_path: Path) -> None:
    """`xyz:MSFT` sits in the tier-2 and tier-3 pools of an `etf` leg."""
    asked: list[str] = []

    def counting(ref: CandidateRef) -> tuple[FundingRow, ...]:
        asked.append(ref.coin)
        return _TRAILS[ref.coin]

    result = assign_control_tiered(
        "xyz:SMH",
        "xyz",
        ENTRY,
        _rows(1e-5),
        [_cand("xyz:MSFT", "xyz", CLASS_EQUITY, 2e-5)],
        counting,
        CONFIG,
        pairs_path=tmp_path / "v2.jsonl",
    )
    assert isinstance(result, TieredAssignment)
    assert result.tier == TIER_ANY_DEX_EQUITY_COMPLEX
    assert asked == ["xyz:MSFT"]
    assert result.candidates_considered == 1


# ------------------------------- the tier stratum and the coverage views ---


def test_the_tier_stratum_reports_every_registered_tier_even_at_zero() -> None:
    """A tier with no pairs is "none yet", never "no such tier"."""
    pairs = (
        [_pair_net(0.01, tier=TIER_SAME_DEX_EXACT_CLASS)] * 5
        + [_pair_net(-0.01, tier=TIER_SAME_DEX_EXACT_CLASS)] * 2
        + [_pair_net(0.01, tier=TIER_ANY_DEX_EXACT_CLASS)] * 3
    )
    stratum = tier_stratum(pairs)
    assert set(stratum) == {"tier_1", "tier_2", "tier_3", "n_all_pairs"}
    assert stratum["tier_1"] == {
        "name": "same_dex_exact_class",
        "n": 7,
        "e1_successes": 5,
        "e1_share": 5 / 7,
        "e2_successes": 5,
        "e2_share": 5 / 7,
    }
    tier_3 = stratum["tier_3"]
    assert isinstance(tier_3, dict)
    assert tier_3["n"] == 0 and tier_3["e1_share"] == 0.0
    assert stratum["n_all_pairs"] == 10


def test_an_unregistered_tier_among_the_pairs_is_a_loud_refusal() -> None:
    with pytest.raises(ValueError, match="unregistered tier"):
        tier_stratum([_pair_net(0.01, tier=4)])


def test_the_class_pair_stratum_reports_only_what_occurs_in_name_order() -> None:
    pairs = [_pair_net(0.01, class_pair="equity->equity")] * 3 + [
        _pair_net(-0.01, class_pair="etf->equity")
    ]
    stratum = class_pair_stratum(pairs)
    assert list(stratum) == ["equity->equity", "etf->equity"]
    assert stratum["equity->equity"] == {"n": 3, "e1_share": 1.0}
    assert stratum["etf->equity"] == {"n": 1, "e1_share": 0.0}


def test_both_new_strata_ride_beside_every_look() -> None:
    report = run_h2_look(
        [_pair_net(0.01)] * 40 + [_pair_net(-0.01)] * 19,
        look=1,
        plan=registered_plan(84, 117),  # the registered look-2 minimum Ns
    )
    assert "tier_stratum" in report.secondaries
    assert "class_pair_stratum" in report.secondaries


def test_coverage_reports_every_registered_tier_even_at_zero() -> None:
    rows = coverage_by_tier(
        [
            (TIER_SAME_DEX_EXACT_CLASS, True),
            (TIER_SAME_DEX_EXACT_CLASS, False),
            (TIER_ANY_DEX_EXACT_CLASS, True),
        ]
    )
    assert [r.stratum for r in rows] == ["tier_1", "tier_2", "tier_3"]
    assert (rows[0].pairs, rows[0].covered, rows[0].underpowered) == (2, 1, 1)
    assert rows[0].share() == 0.5
    assert rows[2].pairs == 0 and rows[2].share() == 0.0


def test_coverage_refuses_an_unregistered_tier() -> None:
    with pytest.raises(ValueError, match="unregistered tier"):
        coverage_by_tier([(4, True)])


def test_coverage_by_class_pair_reports_what_occurs_in_name_order() -> None:
    rows = coverage_by_class_pair(
        [("etf->equity", True), ("equity->equity", True), ("equity->equity", False)]
    )
    assert [r.stratum for r in rows] == ["equity->equity", "etf->equity"]
    assert (rows[0].pairs, rows[0].underpowered) == (2, 1)


def test_coverage_refuses_a_cross_complex_class_pair_as_an_upstream_defect() -> None:
    """The tiered rule cannot produce one, so seeing one is a defect, not a stratum."""
    with pytest.raises(ValueError, match="cross-complex"):
        coverage_by_class_pair([("index->crypto", True)])
    with pytest.raises(ValueError, match="cross-complex"):
        coverage_by_class_pair([("rates->equity", True)])


def test_coverage_refuses_an_unregistered_class_name() -> None:
    with pytest.raises(ValueError, match="unregistered class pair"):
        coverage_by_class_pair([("equity->stonks", True)])
