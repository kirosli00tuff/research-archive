"""Read .env into the process environment. The value is never printed or logged."""

from __future__ import annotations

import os

from npd.paths import REPO_ROOT

ENV_FILE = REPO_ROOT / ".env"


def load_env() -> bool:
    """Load key-value pairs from .env. Returns whether the file was found.

    Existing environment values win, so a caller can override without editing the
    file. Nothing here returns, prints, or logs a value.
    """
    if not ENV_FILE.exists():
        return False
    for raw in ENV_FILE.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))
    return True
