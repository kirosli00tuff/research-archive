"""Record the toolchain provenance this repository's figures were produced on.

Every figure in the artifact was computed by a specific interpreter with a
specific set of pinned tools. This writes that down, so a later reader can tell
whether a re-run is comparable.
"""

from __future__ import annotations

import json
import platform
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
OUT = REPO_ROOT / "reports" / "env_report.json"


def _run(command: list[str]) -> str:
    try:
        completed = subprocess.run(
            command, capture_output=True, text=True, timeout=30, check=False
        )
    except (OSError, subprocess.SubprocessError) as exc:
        return f"<unavailable: {exc}>"
    return completed.stdout.strip() or completed.stderr.strip() or "<empty>"


def build_report() -> dict[str, object]:
    return {
        "kind": "env_report",
        "python_version": sys.version,
        "python_implementation": platform.python_implementation(),
        "platform": platform.platform(),
        "git_head": _run(["git", "-C", str(REPO_ROOT), "rev-parse", "HEAD"]),
        "git_status_porcelain": _run(
            ["git", "-C", str(REPO_ROOT), "status", "--porcelain"]
        ),
        "ruff": _run([str(REPO_ROOT / ".venv/bin/ruff"), "--version"]),
        "mypy": _run([str(REPO_ROOT / ".venv/bin/mypy"), "--version"]),
        "pytest": _run([str(REPO_ROOT / ".venv/bin/pytest"), "--version"]),
    }


def main() -> int:
    report = build_report()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(
        json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    sys.stdout.write(f"wrote {OUT}\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
