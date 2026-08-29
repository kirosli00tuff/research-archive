"""Credential loading. Presence and character length are recordable; values are not.

Standing rule 3 was written as *"secrets never enter the repo — and none are
needed"*, and **measurement falsified the second half on 2026-08-29**: `n = 9`
vendors, `0` usable without a credential (`docs/ACCESS.md`). The rule is amended
rather than contradicted, and this module is where the amended version is
implemented.

**What may be recorded about a credential:** its variable name, whether it is
present, and its character length. **What may not:** the value, any prefix, any
suffix, and any hash of it. A hash of a 32-character key is a confirmation
oracle for a guess, so no hash is recorded either — that is the non-obvious half
of the rule and it is stated here because it is easy to get wrong.

Loading installs the process-wide redactor of :mod:`orb.redact` **before any
credentialed request can be sent**, which is what makes redaction a property of
the process rather than of the caller's discipline.
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path
from typing import Final, final

from orb.redact import Redactor, install_redactor

MASSIVE_API_KEY: Final[str] = "ORB_MASSIVE_API_KEY"
ALPACA_API_KEY: Final[str] = "ORB_ALPACA_API_KEY"
ALPACA_SECRET_KEY: Final[str] = "ORB_ALPACA_SECRET_KEY"

CREDENTIAL_NAMES: Final[tuple[str, ...]] = (
    MASSIVE_API_KEY,
    ALPACA_API_KEY,
    ALPACA_SECRET_KEY,
)
"""The three registered credential variables. Names only; this is a registry."""


class CredentialMissingError(RuntimeError):
    """Raised when a required credential is absent or empty. Loud, never silent."""


@final
@dataclass(frozen=True, slots=True)
class CredentialPresence:
    """What may be recorded about one credential. A name, a flag and a length."""

    name: str
    is_present: bool
    character_length: int

    def as_row(self) -> dict[str, object]:
        """A ledger row. Carries no value, no prefix, no suffix and no hash."""
        return {
            "kind": "credential_presence",
            "credential": self.name,
            "is_present": self.is_present,
            "character_length": self.character_length,
        }


def parse_env_file(path: Path) -> dict[str, str]:
    """Parse a ``KEY=value`` file. Quotes stripped; blank and comment lines skipped."""
    if not path.exists():
        return {}
    out: dict[str, str] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#") or "=" not in stripped:
            continue
        key, _, raw = stripped.partition("=")
        out[key.strip()] = raw.strip().strip('"').strip("'")
    return out


@final
class CredentialStore:
    """Holds credential values. Exposes presence freely and values narrowly."""

    __slots__ = ("_values",)

    def __init__(self, values: dict[str, str]) -> None:
        self._values = {k: v for k, v in values.items() if k in CREDENTIAL_NAMES}

    def __repr__(self) -> str:
        """Names and lengths. A repr is a recorded string and carries no value."""
        shape = ", ".join(f"{p.name}:len={p.character_length}" for p in self.presence())
        return f"CredentialStore({shape})"

    def presence(self) -> list[CredentialPresence]:
        """Presence and character length for every registered credential."""
        return [
            CredentialPresence(
                name=name,
                is_present=bool(self._values.get(name)),
                character_length=len(self._values.get(name, "")),
            )
            for name in CREDENTIAL_NAMES
        ]

    def missing(self) -> list[str]:
        """Registered credentials that are absent or empty."""
        return [p.name for p in self.presence() if not p.is_present]

    def require(self, name: str) -> str:
        """The one accessor that returns a value. Every caller sends, never records."""
        value = self._values.get(name, "")
        if not value:
            raise CredentialMissingError(
                f"{name} is absent or empty in the environment and in .env; "
                "a credentialed probe cannot be sent. This is a recorded "
                "absence, not a fallback to an unauthenticated request."
            )
        return value

    def redactor(self) -> Redactor:
        """A redactor over every loaded value."""
        return Redactor(dict(self._values))


def load_credentials(env_path: Path | None = None) -> CredentialStore:
    """Load from the environment, then from ``.env``, and install the redactor.

    The redactor is installed **here**, before any caller can hold a value, so
    that no credentialed request can be sent by a process whose recording
    boundary is not already redacting.
    """
    values: dict[str, str] = {}
    for name in CREDENTIAL_NAMES:
        from_env = os.environ.get(name, "")
        if from_env:
            values[name] = from_env
    if env_path is not None:
        for key, value in parse_env_file(env_path).items():
            if key in CREDENTIAL_NAMES and key not in values:
                values[key] = value
    store = CredentialStore(values)
    install_redactor(store.redactor())
    return store
