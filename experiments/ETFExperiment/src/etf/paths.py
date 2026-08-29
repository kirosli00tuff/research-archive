"""Every path, one place."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

DATA = ROOT / "data"
LEDGERS = DATA / "ledgers"
REQUEST_LEDGER = LEDGERS / "requests.jsonl"

# A.1 Task 3: the flow snapshot ledger. One row per capture, capture timestamp
# written by this repository, never taken from the source.
SNAPSHOTS_DIR = DATA / "snapshots"
SNAPSHOT_LEDGER = SNAPSHOTS_DIR / "flow_snapshots.jsonl"
SNAPSHOT_BODIES = SNAPSHOTS_DIR / "bodies"

# A.2 Task 1: the admissible-day census.
CENSUS_DIR = DATA / "census"
CENSUS_LEDGER = CENSUS_DIR / "census.jsonl"

# A.3 Task 2: the retro as-printed ledger, archive captures only.
RETRO_DIR = DATA / "retro"
RETRO_LEDGER = RETRO_DIR / "retro_asprinted.jsonl"

# A.2 Task 3: the sealed outcome substrate. Written by the sealed writer only.
OUTCOMES_DIR = DATA / "outcomes"
FUNDING_DIR = DATA / "funding"

STATE_DIR = DATA / "state"
MANIFEST_DIR = STATE_DIR / "manifests"
STAGE_B_LATCH = STATE_DIR / "stage_b_read.json"

REGISTRATION_MD = ROOT / "REGISTRATION.md"
HYPOTHESES_MD = ROOT / "HYPOTHESES.md"
DOCS = ROOT / "docs"
REPORTS = ROOT / "reports"
