"""Every path, one place."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

DATA = ROOT / "data"
LEDGERS = DATA / "ledgers"
REQUEST_LEDGER = LEDGERS / "requests.jsonl"

CENSUS_DIR = DATA / "census"
CENSUS_LEDGER = CENSUS_DIR / "census.jsonl"

BIRTHS_DIR = DATA / "births"
OUTCOMES_DIR = DATA / "outcomes"
FUNDING_DIR = DATA / "funding"
SPREADS_DIR = DATA / "spreads"

CONTROLS_DIR = DATA / "controls"
PAIRS_LEDGER = CONTROLS_DIR / "pairs.jsonl"

STATE_DIR = DATA / "state"

REGISTRATION_MD = ROOT / "REGISTRATION.md"
DOCS = ROOT / "docs"
REPORTS = ROOT / "reports"
