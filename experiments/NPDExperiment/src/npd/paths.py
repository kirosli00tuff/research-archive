"""Every path the experiment writes to or reads from. One place, no literals elsewhere."""

from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]

VAR = REPO_ROOT / "var"
REPORTS = REPO_ROOT / "reports"
LEDGERS = REPO_ROOT / "ledgers"

# The experiment's own store. Nothing outside npd.data writes here.
STORE_DB = VAR / "npd.db"

# The sealed store. Only npd.eval.evaluator may open it. tests/test_guards.py
# fails when any other module names it.
SEALED_DB = VAR / "npd_sealed.db"

SPEND_LEDGER = LEDGERS / "spend.jsonl"
EVIDENCE_LEDGER = LEDGERS / "evidence.jsonl"

# Read-only source paths in the neighbouring repository. Opened read-only and
# hash-verified. Nothing here is ever written.
AITRADER_ROOT = Path.home() / "Documents" / "GitHub" / "AiTrader"
SOURCE_BARS_DB = AITRADER_ROOT / "analysis_bars.db"
SOURCE_UNIVERSE_PY = AITRADER_ROOT / "backtest" / "universe.py"


def ensure_dirs() -> None:
    for d in (VAR, REPORTS, LEDGERS):
        d.mkdir(parents=True, exist_ok=True)
