"""Amendment H2-5 section 1: the asset-class taxonomy.

Every refusal is produced through the real mapping, never asserted. The
taxonomy is a partition and a ticker in no table is `excluded_unclassifiable`
with a reason — never a default, never a guess.
"""

from __future__ import annotations

import ast
from pathlib import Path

import pytest

from npl.register import assetclass
from npl.register.assetclass import (
    CLASS_COMMODITY,
    CLASS_CRYPTO,
    CLASS_EQUITY,
    CLASS_ETF,
    CLASS_FX,
    CLASS_INDEX,
    CLASS_RATES,
    CLASS_VOL,
    EQUITY_COMPLEX,
    REASON_AMBIGUOUS,
    REASON_CRYPTO_ON_BUILDER,
    REASON_HOUSE_INDEX,
    REASON_NOT_IN_MAPPING,
    REGISTERED_CLASSES,
    TICKER_CLASS,
    UNCLASSIFIABLE,
    asset_class,
    bare_ticker,
    class_pair,
    in_equity_complex,
    unclassifiable_reason,
)

# --------------------------------------------- step 1: the dex rule --------


@pytest.mark.parametrize("coin", ["BTC", "PONS", "kPEPE", "GRAM", "CASHCAT"])
def test_every_main_dex_instrument_is_crypto_by_the_dex_rule(coin: str) -> None:
    assert asset_class(coin, "") == CLASS_CRYPTO


@pytest.mark.parametrize("coin", ["hyna:BTC", "hyna:GOLD", "hyna:SILVER", "hyna:LIT"])
def test_every_hyna_instrument_is_crypto_including_the_three_the_rule_sweeps_in(
    coin: str,
) -> None:
    """hyna:GOLD/SILVER/LIT are crypto by the registered dex rule.

    Amendment H2-5 records this as a stated consequence rather than patching
    it. The test pins the consequence so a later reader cannot mistake it for
    an oversight.
    """
    assert asset_class(coin, "hyna") == CLASS_CRYPTO


def test_a_crypto_referenced_instrument_on_a_builder_dex_takes_no_class() -> None:
    """The builder-dex class list contains no crypto class, by construction."""
    assert asset_class("flx:BTC", "flx") is None
    assert unclassifiable_reason("flx:BTC", "flx") == REASON_CRYPTO_ON_BUILDER
    assert asset_class("para:TOTAL2", "para") is None
    assert unclassifiable_reason("para:TOTAL2", "para") == REASON_CRYPTO_ON_BUILDER


# ----------------------------------- step 2: the builder-dex ticker table ---


@pytest.mark.parametrize(
    ("coin", "dex", "expected"),
    [
        ("xyz:MSFT", "xyz", CLASS_EQUITY),
        ("io:ANTH", "io", CLASS_EQUITY),
        ("xyz:MINIMAX", "xyz", CLASS_EQUITY),
        ("xyz:SKHY", "xyz", CLASS_EQUITY),
        ("xyz:SMH", "xyz", CLASS_ETF),
        ("xyz:URNM", "xyz", CLASS_ETF),
        ("mkts:US500", "mkts", CLASS_INDEX),
        ("vntl:MAG7", "vntl", CLASS_INDEX),
        ("xyz:COPPER", "xyz", CLASS_COMMODITY),
        ("xyz:H100", "xyz", CLASS_COMMODITY),
        ("xyz:JPY", "xyz", CLASS_FX),
        ("para:10Y", "para", CLASS_RATES),
        ("mkts:USBOND", "mkts", CLASS_RATES),
        ("xyz:VIX", "xyz", CLASS_VOL),
    ],
)
def test_the_registered_table_assigns_the_registered_class(
    coin: str, dex: str, expected: str
) -> None:
    assert asset_class(coin, dex) == expected


@pytest.mark.parametrize(
    "coin", ["xyz:QNT", "xyz:BOT", "xyz:SHAZ", "xyz:LYTE", "xyz:NCLD", "para:ANSEM"]
)
def test_the_six_tickers_this_refusal_actually_costs_a_pair_are_refused(coin: str) -> None:
    """These six are the whole measured cost of the class test. Pinned by name.

    Silently classifying any of them — as `equity`, or as anything — is the
    registered mutation of Task 6, and this is the test that catches it.
    """
    dex = coin.split(":")[0]
    assert asset_class(coin, dex) is None
    assert unclassifiable_reason(coin, dex) == REASON_AMBIGUOUS


def test_the_house_index_carries_its_own_reason_not_the_ambiguous_one() -> None:
    assert asset_class("xyz:XYZ100", "xyz") is None
    assert unclassifiable_reason("xyz:XYZ100", "xyz") == REASON_HOUSE_INDEX


def test_a_ticker_in_no_table_at_all_is_refused_with_not_in_registered_mapping() -> None:
    """A ticker nobody has ever seen takes no default and no guess."""
    assert asset_class("xyz:NOTATICKER", "xyz") is None
    assert unclassifiable_reason("xyz:NOTATICKER", "xyz") == REASON_NOT_IN_MAPPING


def test_asking_for_an_exclusion_reason_on_a_classified_coin_is_a_loud_refusal() -> None:
    with pytest.raises(ValueError, match="is classified"):
        unclassifiable_reason("xyz:MSFT", "xyz")


# ------------------------------------------------------- the partition -----


def test_the_seven_builder_tables_and_the_exclusion_table_are_disjoint() -> None:
    assert not set(TICKER_CLASS) & set(UNCLASSIFIABLE)


def test_every_assigned_class_is_a_registered_class() -> None:
    assert set(TICKER_CLASS.values()) <= REGISTERED_CLASSES


def test_the_partition_check_is_produced_by_the_module_not_asserted(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """`_check_tables` refuses a real collision, through the real function."""
    monkeypatch.setattr(assetclass, "_EQUITY", (*assetclass._EQUITY, "COPPER"))
    with pytest.raises(assetclass.TaxonomyConflict, match="COPPER"):
        assetclass._check_tables()
    monkeypatch.undo()
    assetclass._check_tables()  # and the restored tables still partition


def test_the_exclusion_collision_check_is_produced_not_asserted(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(
        assetclass, "UNCLASSIFIABLE", {**assetclass.UNCLASSIFIABLE, "MSFT": REASON_AMBIGUOUS}
    )
    with pytest.raises(assetclass.TaxonomyConflict, match="MSFT"):
        assetclass._check_tables()
    monkeypatch.undo()
    assetclass._check_tables()


# ------------------------------------------------------ the equity complex -


def test_the_equity_complex_is_exactly_equity_etf_index_and_nothing_else() -> None:
    assert set(EQUITY_COMPLEX) == {CLASS_EQUITY, CLASS_ETF, CLASS_INDEX}
    for other in (CLASS_CRYPTO, CLASS_COMMODITY, CLASS_FX, CLASS_RATES, CLASS_VOL):
        assert not in_equity_complex(other)


def test_no_class_is_in_the_equity_complex_by_accident_of_being_none() -> None:
    assert not in_equity_complex(None)


def test_vol_has_exactly_one_member_so_a_vol_leg_can_never_pair() -> None:
    """Recorded in the amendment; pinned here so the consequence stays visible."""
    assert [t for t, c in TICKER_CLASS.items() if c == CLASS_VOL] == ["VIX"]


# ------------------------------------------------------------- mechanics ---


def test_bare_ticker_strips_exactly_one_dex_prefix() -> None:
    assert bare_ticker("xyz:AAPL") == "AAPL"
    assert bare_ticker("BTC") == "BTC"


def test_class_pair_is_the_stratum_label_written_on_every_row() -> None:
    assert class_pair(CLASS_EQUITY, CLASS_ETF) == "equity->etf"


def test_nothing_fuzzy_matches_a_near_miss_of_a_registered_ticker() -> None:
    assert asset_class("xyz:MSF", "xyz") is None
    assert asset_class("xyz:MSFT2", "xyz") is None


# --------------------------------- the H2 and H5 tables are never merged ---


def test_the_h2_taxonomy_imports_nothing_that_owns_a_path() -> None:
    """A pure module, like `npl.pairtype`, so the dark reader can import it."""
    source = Path(assetclass.__file__).read_text(encoding="utf-8")
    tree = ast.parse(source)
    imported = {
        node.module
        for node in ast.walk(tree)
        if isinstance(node, ast.ImportFrom) and node.module is not None
    }
    assert imported == {"__future__", "typing"}, f"the taxonomy imported {imported}"


def test_the_h2_taxonomy_and_the_h5_resolution_mapping_never_import_each_other() -> None:
    """Different questions, different tables, registered separately as such."""
    h2_path = Path(assetclass.__file__)
    h5_path = h2_path.parents[1] / "h5" / "resolution.py"

    def modules(path: Path) -> set[str]:
        tree = ast.parse(path.read_text(encoding="utf-8"))
        out: set[str] = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom) and node.module is not None:
                out.add(node.module)
            elif isinstance(node, ast.Import):
                out.update(alias.name for alias in node.names)
        return out

    assert not any("h5" in m for m in modules(h2_path))
    assert not any("assetclass" in m for m in modules(h5_path))


def test_the_h2_test_is_weaker_than_h5s_and_the_divergence_is_the_registered_one() -> None:
    """Tickers H5 cannot resolve to a price still take an H2 class, by design.

    H5 asks which instrument a string prices; H2 asks what kind of thing it
    names. The seven private issuers and three ambiguous-but-equity tickers
    named in Amendment H2-5 are the whole of the divergence that costs H2
    nothing — and the six that H2 also refuses are named in their own test.
    """
    from npl.h5.resolution import UNRESOLVABLE

    diverging = {
        "MINIMAX", "ZHIPU", "CXMT", "UNITREE", "ANTH", "SHEIN", "SPCX",
        "STRC", "SKHX", "SKHY",
    }  # fmt: skip
    for ticker in diverging:
        assert ticker in UNRESOLVABLE, f"{ticker} is no longer unresolvable to H5"
        assert TICKER_CLASS[ticker] == CLASS_EQUITY

    also_refused = {"ANSEM", "BOT", "LYTE", "NCLD", "QNT", "SHAZ"}
    for ticker in also_refused:
        assert ticker in UNRESOLVABLE
        assert UNCLASSIFIABLE[ticker] == REASON_AMBIGUOUS
