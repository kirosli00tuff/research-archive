"""The generating-sample quarantine (standing rule 12).

The 312 H1 retro events are the generating sample: their outcomes were read
by the spent Stage B read, so they are usable for power assumptions and
never admissible to a successor verdict. Their event IDs are recorded in
data/state/generating_sample.json, built here from the retro plan and the
sealed census (timestamps and counts only, through the Amendment 1
resolution — no outcome value exists on this path). Every successor
eligibility view and every verdict-bearing successor statistic calls
refuse_generating_sample first; the refusal is produced by test, never
asserted.
"""

from __future__ import annotations

import json
from collections.abc import Iterable
from pathlib import Path
from typing import Any

from npl.census import CensusRow
from npl.eligibility import resolve_event
from npl.paths import GENERATING_SAMPLE_JSON

# The registered H1 retro cohort size (root REGISTRATION.md, Section 0
# verdict record). A build that does not reproduce it exactly refuses.
REGISTERED_GENERATING_EVENT_N = 312


class GeneratingSampleAdmitted(RuntimeError):
    """A generating-sample event reached a successor statistic. Refused."""


class GeneratingSampleUnavailable(RuntimeError):
    """The generating-sample record is absent or does not reproduce. Loud."""


def event_id(coin: str, dex: str, listing_open_ms: int) -> str:
    """The registered event identity: coin, dex, and listing timestamp."""
    return f"{coin}|{dex}|{listing_open_ms}"


def build_generating_sample(
    census_rows: list[CensusRow],
    plan_rows: list[dict[str, Any]],
    expected_n: int = REGISTERED_GENERATING_EVENT_N,
) -> frozenset[str]:
    """The 312 event IDs from the plan and census, by Amendment 1 resolution.

    A plan row of kind `event` is a generating event iff the census row's
    resolution reproduces its listing timestamp — the same classification
    the Stage B preconditions used. Plan rows that do not resolve are the
    queued control windows; the equality check on the final count is the
    guard against that classification drifting.
    """
    by_key: dict[tuple[str, str], CensusRow] = {}
    for row in census_rows:
        by_key.setdefault((row.coin, row.dex), row)
    ids: set[str] = set()
    for raw in plan_rows:
        if raw.get("kind") != "event":
            continue
        coin, dex = str(raw["coin"]), str(raw["dex"])
        listing = int(raw["listing_open_ms"])
        census_row = by_key.get((coin, dex))
        if census_row is None:
            raise GeneratingSampleUnavailable(
                f"plan row for {coin!r} on dex {dex!r} has no census row; the generating "
                f"sample cannot be reconstructed and nothing here guesses"
            )
        if resolve_event(census_row).event_listing_ms == listing:
            ids.add(event_id(coin, dex, listing))
    if len(ids) != expected_n:
        raise GeneratingSampleUnavailable(
            f"generating-sample reconstruction produced {len(ids)} events against the "
            f"registered {expected_n}; refusing to record a different sample"
        )
    return frozenset(ids)


def write_generating_sample(ids: frozenset[str], path: Path = GENERATING_SAMPLE_JSON) -> Path:
    """Record the sample once. A differing existing record is a loud refusal."""
    payload = {"count": len(ids), "event_ids": sorted(ids)}
    if path.exists():
        existing = json.loads(path.read_text(encoding="utf-8"))
        if existing != payload:
            raise GeneratingSampleUnavailable(
                f"{path} exists and differs from the reconstruction; the record is "
                f"write-once and a mismatch is reported, never repaired"
            )
        return path
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return path


def load_generating_sample(
    path: Path = GENERATING_SAMPLE_JSON,
    expected_n: int = REGISTERED_GENERATING_EVENT_N,
) -> frozenset[str]:
    """The recorded sample. An absent or short record refuses loudly."""
    if not path.exists():
        raise GeneratingSampleUnavailable(
            f"{path} does not exist. The quarantine cannot run open-loop: build and "
            f"record the generating sample before any successor eligibility view."
        )
    payload = json.loads(path.read_text(encoding="utf-8"))
    ids = frozenset(str(x) for x in payload["event_ids"])
    if len(ids) != int(payload["count"]) or len(ids) != expected_n:
        raise GeneratingSampleUnavailable(
            f"{path} carries {len(ids)} ids against a recorded count of "
            f"{payload['count']} and a registered {expected_n}; refusing to guess"
        )
    return ids


def refuse_generating_sample(ids: Iterable[str], sample: frozenset[str]) -> None:
    """The quarantine gate: any admitted generating event is a loud refusal."""
    admitted = sorted(set(ids) & sample)
    if admitted:
        raise GeneratingSampleAdmitted(
            f"{len(admitted)} generating-sample event(s) reached a successor "
            f"statistic (first: {admitted[:3]}). The 312 retro events are usable "
            f"for power assumptions, never for verdicts."
        )
