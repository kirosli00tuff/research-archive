"""Where artifacts are written, and the one function that writes them.

Every recorded figure in this repository reaches disk through :func:`emit`, so
there is a single place where the serialisation, the sort order and the trailing
newline are decided. Artifacts are sorted by key so a diff between two runs shows
what changed rather than what moved.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

REPO = Path(__file__).resolve().parents[2]
REPORTS = REPO / "reports"
CENSUS_PATH = REPO / "data" / "quotes" / "census.jsonl"


def emit(payload: dict[str, Any], out: Path | None) -> None:
    """Write an artifact and echo it. ``default=str`` never invents a value."""
    text = json.dumps(payload, indent=2, sort_keys=True, default=str) + "\n"
    if out is not None:
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(text, encoding="utf-8")
    print(text, end="")
