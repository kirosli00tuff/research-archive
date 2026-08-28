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
RETRO_PLAN = STATE_DIR / "retro_plan.jsonl"

REGISTRATION_MD = ROOT / "REGISTRATION.md"
DOCS = ROOT / "docs"
REPORTS = ROOT / "reports"

# --- the register architecture (Amendment 4, 2026-08-28) --------------------
REGISTRATIONS = ROOT / "registrations"
H2_REGISTRATION_MD = REGISTRATIONS / "H2" / "REGISTRATION.md"
H3_REGISTRATION_MD = REGISTRATIONS / "H3" / "REGISTRATION.md"
H4_REGISTRATION_MD = REGISTRATIONS / "H4" / "REGISTRATION.md"

# The 312 H1 retro event IDs: the generating sample, never a successor verdict.
GENERATING_SAMPLE_JSON = STATE_DIR / "generating_sample.json"

# Successor eligibility ledgers (A.2 Task 1) and the fresh collection plan.
ELIGIBILITY_DIR = DATA / "eligibility"
H2_PAIRS_LEDGER = CONTROLS_DIR / "h2_pairs.jsonl"
FRESH_PLAN = STATE_DIR / "fresh_plan.jsonl"

# --- register entry H5 (2026-08-28): HIP-3 equity-style basis feasibility ---
# Every H5 write lands under H5_DIR and nowhere else; npl.h5.stores enforces
# the containment and the refusal is produced by test, not asserted.
H5_REGISTRATION_MD = REGISTRATIONS / "H5" / "REGISTRATION.md"
H5_DIR = DATA / "h5"
H5_CENSUS = H5_DIR / "census.jsonl"
H5_ACCESS = H5_DIR / "access.jsonl"
H5_SNAPSHOTS = H5_DIR / "snapshots.jsonl"
H5_RETRO = H5_DIR / "retro.jsonl"
H5_REPORTS = REPORTS / "h5"
H5_ACCESS_MD = DOCS / "H5_ACCESS.md"
