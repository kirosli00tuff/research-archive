"""Credential redaction. A ledger row is a recorded string, so it is redacted.

Every value that looks like a credential becomes a placeholder naming the
variable it came from, before the line is serialised. Redaction is
deterministic, so a ledger stays comparable line for line across runs.

This repository holds no venue credential and plans to hold none — nothing here
registers at a venue. The guard exists anyway, because the cost of it is one
module and the cost of not having it is a pushed secret.
"""

from __future__ import annotations

import os
import re
from collections.abc import Mapping
from typing import Any

_SECRET_KEY_PATTERN = re.compile(
    r"(?i)(secret|token|password|passwd|api[_-]?key|private[_-]?key|"
    r"credential|authorization|auth|bearer|cookie|session[_-]?id)"
)

_MIN_SECRET_LENGTH = 8
"""Shorter environment values are not treated as secrets: redacting every
short string would redact ordinary configuration and make the ledger useless."""


def _environment_secrets() -> dict[str, str]:
    """Environment values long enough to be credentials, keyed by variable."""
    found: dict[str, str] = {}
    for name, value in os.environ.items():
        if len(value) >= _MIN_SECRET_LENGTH and _SECRET_KEY_PATTERN.search(name):
            found[value] = name
    return found


def redact_text(text: str) -> str:
    """Replace any environment credential appearing in ``text`` by its name."""
    result = text
    for value, name in _environment_secrets().items():
        if value and value in result:
            result = result.replace(value, f"<redacted:{name}>")
    return result


def redact_data(data: object) -> object:
    """Redact recursively through mappings, sequences and strings."""
    if isinstance(data, str):
        return redact_text(data)
    if isinstance(data, Mapping):
        redacted_map: dict[str, object] = {}
        for key, value in data.items():
            if isinstance(key, str) and _SECRET_KEY_PATTERN.search(key):
                redacted_map[key] = f"<redacted:key:{key}>"
            else:
                redacted_map[str(key)] = redact_data(value)
        return redacted_map
    if isinstance(data, list | tuple):
        return [redact_data(item) for item in data]
    return data


def redact_row(row: Mapping[str, Any]) -> Mapping[str, Any]:
    """Redact one ledger row. Always returns a mapping."""
    redacted = redact_data(row)
    if not isinstance(redacted, dict):  # pragma: no cover - structurally impossible
        raise TypeError("redact_row expected a mapping")
    return redacted
