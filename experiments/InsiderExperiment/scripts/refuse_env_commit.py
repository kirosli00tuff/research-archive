"""Refuse to commit a .env file. Run by pre-commit, never by hand."""

from __future__ import annotations

import subprocess
import sys


def main() -> int:
    staged = subprocess.run(
        ["git", "diff", "--cached", "--name-only"], capture_output=True, text=True, check=False
    ).stdout.split()
    offenders = [
        p for p in staged if p == ".env" or (p.startswith(".env.") and p != ".env.example")
    ]
    if offenders:
        print(f"refusing to commit: {offenders}")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
