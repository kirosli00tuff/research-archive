"""The universe rule rejects what it must reject."""
from hfexperiment import universe as uv

PARAMS = uv.RuleParams()


def make_candidate(**overrides: object) -> uv.Candidate:
    base: dict = {
        "symbol": "TEST",
        "window_bars": 60,
        "median_close": 25.0,
        "median_dollar_volume": 5_000_000.0,
        "is_fund": False,
        "segment_break_in_window": False,
    }
    base.update(overrides)
    return uv.Candidate(**base)


def test_rejects_fund() -> None:
    cand = make_candidate(is_fund=True)
    assert uv.rejection_reason(cand, PARAMS) == "fund"


def test_rejects_unclassified_as_unknown_not_as_company() -> None:
    cand = make_candidate(is_fund=None)
    assert uv.rejection_reason(cand, PARAMS) == "unclassified"


def test_rejects_sub_five_dollar_median_close() -> None:
    cand = make_candidate(median_close=4.99)
    reason = uv.rejection_reason(cand, PARAMS)
    assert reason is not None and reason.startswith("below_price_floor")


def test_rejects_thin_window() -> None:
    cand = make_candidate(window_bars=39)
    reason = uv.rejection_reason(cand, PARAMS)
    assert reason is not None and reason.startswith("thin_window")


def test_accepts_clean_operating_company() -> None:
    assert uv.rejection_reason(make_candidate(), PARAMS) is None


def test_classifier_flags_fund_names_and_exchanges() -> None:
    assert uv.classify_fund("SPDR S&P 500 ETF Trust", "AMEX") is True
    assert uv.classify_fund("Anything At All", "ARCA") is True
    assert uv.classify_fund("Northern Trust Corporation", "NASDAQ") is False
    assert uv.classify_fund("", "NASDAQ") is None
