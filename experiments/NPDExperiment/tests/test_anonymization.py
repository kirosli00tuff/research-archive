"""No ticker ever reaches a prompt."""

from __future__ import annotations

import re

from npd.collect.prompt import Prompt, build, template_digest
from npd.config import CONFIG
from npd.data.anonymize import Anonymization, new_nonce
from npd.data.anonymize import build as build_mapping

REAL_TICKERS = [
    "AAPL",
    "MSFT",
    "NVDA",
    "AMZN",
    "GOOGL",
    "META",
    "TSLA",
    "BRKB",
    "JPM",
    "V",
    "UNH",
    "XOM",
    "LLY",
    "JNJ",
    "PG",
    "MA",
    "AVGO",
    "HD",
    "CVX",
    "MRK",
    "ABBV",
    "COST",
    "PEP",
    "ADBE",
    "KO",
    "WMT",
    "CRM",
    "BAC",
    "TMO",
    "MCD",
]


def _panel_prompt() -> tuple[Anonymization, Prompt]:
    nonce = new_nonce()
    anon = build_mapping(list(REAL_TICKERS), nonce)
    labels = list(anon.presentation_order)
    z_by_label = {
        lab: dict.fromkeys(CONFIG.feature_names, (i - 15) / 10.0) for i, lab in enumerate(labels)
    }
    return anon, build(labels, z_by_label)


def test_no_real_ticker_appears_in_the_rendered_prompt() -> None:
    """The mutation target. Letting a symbol through anywhere fails here."""
    anon, prompt = _panel_prompt()
    text = prompt.system + "\n" + prompt.user
    leaked = [t for t in REAL_TICKERS if re.search(rf"\b{re.escape(t)}\b", text)]
    assert not leaked, f"tickers reached the prompt: {leaked}"
    assert set(anon.label_to_symbol.values()) == set(REAL_TICKERS)


def test_labels_are_letters_only() -> None:
    _anon, prompt = _panel_prompt()
    for label in prompt.labels:
        assert re.fullmatch(r"[A-Z]{2}", label), f"label {label} is not letters"


def test_no_label_equals_its_symbol() -> None:
    anon, _ = _panel_prompt()
    assert not [lab for lab, sym in anon.label_to_symbol.items() if lab == sym]


def test_the_mapping_is_remapped_every_call() -> None:
    a = build_mapping(list(REAL_TICKERS), new_nonce())
    b = build_mapping(list(REAL_TICKERS), new_nonce())
    assert a.label_to_symbol != b.label_to_symbol


def test_the_mapping_replays_from_its_nonce() -> None:
    nonce = new_nonce()
    a = build_mapping(list(REAL_TICKERS), nonce)
    b = build_mapping(list(REAL_TICKERS), nonce)
    assert a.label_to_symbol == b.label_to_symbol
    assert a.presentation_order == b.presentation_order


def test_the_prompt_carries_no_date_and_no_absolute_price() -> None:
    _, prompt = _panel_prompt()
    text = prompt.user
    assert not re.search(r"\b(19|20)\d{2}-\d{2}-\d{2}\b", text), "a date reached the prompt"
    assert not re.search(r"\$\s?\d", text), "an absolute price reached the prompt"


def test_the_template_digest_is_stable() -> None:
    assert template_digest() == template_digest()
    assert len(template_digest()) == 64


TWO_LETTER_TICKERS = ["KO", "GE", "HD", "MA", "MU", "ON", "RF", "SQ", "ZS", "PG"]


def test_no_label_collides_with_any_symbol_in_the_same_panel() -> None:
    """Two-letter codes are also real tickers.

    KO is Coca-Cola, GE is General Electric, MA is Mastercard. A label drawn at
    random can equal a ticker standing in the same panel, which puts that ticker
    in front of the model. The panel symbols are struck from the label pool
    before any label is drawn, and this test is what caught the collision on 52
    of the 432 window days before a single call went out.
    """
    symbols = TWO_LETTER_TICKERS + [f"X{i:02d}" for i in range(CONFIG.panel_size - 10)]
    for _ in range(200):
        anon = build_mapping(list(symbols), new_nonce())
        collisions = set(anon.label_to_symbol) & {s.upper() for s in symbols}
        assert not collisions, f"a label equals a panel ticker: {sorted(collisions)}"


def test_a_panel_of_two_letter_tickers_still_renders_cleanly() -> None:
    symbols = TWO_LETTER_TICKERS + [f"X{i:02d}" for i in range(CONFIG.panel_size - 10)]
    anon = build_mapping(list(symbols), new_nonce())
    labels = list(anon.presentation_order)
    z_by_label = {
        lab: dict.fromkeys(CONFIG.feature_names, (i - 15) / 10.0) for i, lab in enumerate(labels)
    }
    prompt = build(labels, z_by_label)
    leaked = [t for t in TWO_LETTER_TICKERS if re.search(rf"\b{re.escape(t)}\b", prompt.user)]
    assert not leaked, f"tickers reached the prompt: {leaked}"
