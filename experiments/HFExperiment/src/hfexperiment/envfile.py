"""Credentials from .env. Named variables only, refusal on absence.

HFExperiment owns its own Alpaca data keys, separate from AiTrader's,
so two collectors never share a rate window. The operator copies the
keys into .env by hand. When they are absent this loader raises with
the BLOCKED-ON-OPERATOR wording, so the timer's first run fails loudly
rather than silently, which is the failure mode Stage B.1 registered.

Values never appear in logs, exceptions, or any file this repository
writes.
"""
from __future__ import annotations

from pathlib import Path

REQUIRED_KEYS = ("ALPACA_KEY_ID", "ALPACA_SECRET_KEY")


class MissingCredentialsError(RuntimeError):
    """.env lacks a required key. The run must stop loudly."""


def parse_env(text: str) -> dict[str, str]:
    """KEY=VALUE lines. Comments and blanks skipped. No interpolation."""
    out: dict[str, str] = {}
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#") or "=" not in stripped:
            continue
        key, _, value = stripped.partition("=")
        out[key.strip()] = value.strip().strip('"').strip("'")
    return out


def load_credentials(env_path: str | Path) -> dict[str, str]:
    """The required keys from .env, or a loud refusal naming the gap."""
    path = Path(env_path)
    if not path.exists():
        raise MissingCredentialsError(
            f"{path} does not exist. BLOCKED-ON-OPERATOR: copy the "
            "Alpaca data keys into .env by hand. Variable names are in "
            ".env.example."
        )
    values = parse_env(path.read_text(encoding="utf-8"))
    missing = [key for key in REQUIRED_KEYS if not values.get(key)]
    if missing:
        raise MissingCredentialsError(
            f"{path} lacks {missing}. BLOCKED-ON-OPERATOR: copy the "
            "Alpaca data keys into .env by hand. Variable names are in "
            ".env.example."
        )
    return {key: values[key] for key in REQUIRED_KEYS}
