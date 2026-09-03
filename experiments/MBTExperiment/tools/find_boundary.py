#!/usr/bin/env python3
"""Locate VRPExperiment by its closure marker rather than by an assumed path.

It sits at ``~/Documents/GitHub/VRPExperiment`` today and relocates to
``~/Documents/GitHub/closed/VRPExperiment`` once ``stage_move_closed.sh`` runs.
Hard-coding either path makes the boundary hash silently wrong the day the move
happens: it would hash a directory that no longer exists, or worse, one that
does. Searching for the marker asks the question that actually identifies it.
"""

from __future__ import annotations

import sys
from pathlib import Path

MARKER = "_CLOSED_DO_NOT_RUN_HERE"
TARGET = "VRPExperiment"
SEARCH_ROOTS = (Path.home() / "Documents" / "GitHub",)


def find() -> Path | None:
    for root in SEARCH_ROOTS:
        if not root.is_dir():
            continue
        for candidate in sorted(root.rglob(f"*/{MARKER}")):
            if candidate.parent.name == TARGET:
                return candidate.parent
    return None


def main() -> int:
    found = find()
    if found is None:
        print(
            f"REFUSED: no directory named {TARGET} carrying a {MARKER} marker was "
            f"found under {[str(r) for r in SEARCH_ROOTS]}. The boundary is "
            "resolved by marker, never by an assumed path.",
            file=sys.stderr,
        )
        return 1
    print(found)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
