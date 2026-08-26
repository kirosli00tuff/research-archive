"""Every path the experiment reads from or writes to. One place, no literals elsewhere."""

from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]

VAR = REPO_ROOT / "var"
REPORTS = REPO_ROOT / "reports"
LEDGERS = REPO_ROOT / "ledgers"
CACHE = REPO_ROOT / "cache"

# Raw SEC responses land here and are never refetched. Gitignored.
EDGAR_CACHE = CACHE / "edgar"

# The experiment's own stores. Nothing outside the writing module touches them.
MARKET_DB = VAR / "insider_market.db"
CORPUS_DB = VAR / "insider_corpus.db"

# Centered daily portfolio excess returns. Each value is a deviation from the
# series mean and the mean itself is never written, so the first moment cannot
# be recovered from this file. insider.power is its permitted reader.
DISPERSION_DB = VAR / "insider_dispersion.db"

# The sealed store. Raw daily portfolio excess returns live here and only here,
# and their mean is the realized alpha. Only insider.eval.evaluator may open it.
# tests/test_guards.py fails when any other module names it.
SEALED_DB = VAR / "insider_sealed.db"

FETCH_LEDGER = LEDGERS / "fetch.jsonl"
EVIDENCE_LEDGER = LEDGERS / "evidence.jsonl"

REGISTRATION = REPO_ROOT / "REGISTRATION.md"

# Read-only source paths in the neighbouring repository. Two paths, no others.
# Nothing here is ever written and news_experiment.db is never named.
AITRADER_ROOT = Path.home() / "Documents" / "GitHub" / "AiTrader"
SOURCE_BARS_DB = AITRADER_ROOT / "analysis_bars.db"
SOURCE_UNIVERSE_PY = AITRADER_ROOT / "backtest" / "universe.py"


def ensure_dirs() -> None:
    for d in (VAR, REPORTS, LEDGERS, CACHE, EDGAR_CACHE):
        d.mkdir(parents=True, exist_ok=True)
