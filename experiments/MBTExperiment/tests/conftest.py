"""Shared fixtures. The refusal recorder is the load-bearing one.

**Every guard is demonstrated by producing its refusal as an artifact under
``reports/``, never by asserting it in prose.** A test that says "the guard
refuses" and passes is indistinguishable from a test that never ran the guard.
The recorder below captures the actual exception type and the actual message from
every refusal the suite provokes, and writes them to
``reports/guards/refusals.json`` so a reader can see the refusal rather than
being told about it.
"""

from __future__ import annotations

import json
from collections.abc import Iterator
from dataclasses import asdict, dataclass, field
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import pytest

REPO = Path(__file__).resolve().parents[1]
REFUSALS_PATH = REPO / "reports" / "guards" / "refusals.json"


@dataclass
class RefusalRecorder:
    """Collects demonstrated refusals so the suite emits evidence, not claims."""

    records: list[dict[str, Any]] = field(default_factory=list)

    def record(
        self,
        *,
        guard: str,
        scenario: str,
        exception: BaseException,
        expectation: str,
    ) -> None:
        self.records.append(
            {
                "guard": guard,
                "scenario": scenario,
                "expectation": expectation,
                "exception_type": type(exception).__name__,
                "exception_message": str(exception),
                "recorded_at": datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ"),
            }
        )

    def record_finding(self, *, guard: str, scenario: str, expectation: str, finding: Any) -> None:
        """Record a static-analysis finding, which refuses at build time rather than raising."""
        self.records.append(
            {
                "guard": guard,
                "scenario": scenario,
                "expectation": expectation,
                "finding": asdict(finding) | {"rule": str(finding.rule)},
                "recorded_at": datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ"),
            }
        )


@pytest.fixture(scope="session")
def refusals() -> Iterator[RefusalRecorder]:
    recorder = RefusalRecorder()
    yield recorder
    REFUSALS_PATH.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "note": (
            "Each entry is a refusal this suite PROVOKED and captured, carrying the "
            "exception type and message the guard actually produced. Refusals are "
            "demonstrated as artifacts, never asserted in prose."
        ),
        "written_at": datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "count": len(recorder.records),
        "guards_demonstrated": sorted({r["guard"] for r in recorder.records}),
        "refusals": recorder.records,
    }
    REFUSALS_PATH.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
