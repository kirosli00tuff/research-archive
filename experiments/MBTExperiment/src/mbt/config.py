"""Configuration. Secrets and account numbers live in the environment only.

Every value comes from an environment variable, loaded from ``.env`` if present.
A missing variable raises :class:`MissingConfigError` **naming the variable**,
because "configuration error" sends a reader to the wrong file.

Configuration states an **intent**. It never states the environment a figure was
measured in: that is derived from the account the session actually connected to,
in :mod:`mbt.provenance`. The ``declared`` field below is the intent, and it is
carried into :meth:`SessionProvenance.from_connection` to be checked against the
fact rather than trusted.

**The live slots are absent by design.** The paper-only clause is in force, and
filling a live variable does not lift it. Lifting it is an operator edit to
``CLAUDE.md``.
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path
from typing import final

from mbt.provenance import Environment

REPO = Path(__file__).resolve().parents[2]
ENV_PATH = REPO / ".env"


class ConfigError(RuntimeError):
    """Base class for every configuration refusal."""


class MissingConfigError(ConfigError):
    """A required environment variable is unset or empty. Names the variable."""


class MalformedConfigError(ConfigError):
    """A required variable is set to a value of the wrong shape.

    **The offending value is never echoed.** ``int()`` raises a ``ValueError``
    carrying the string it failed on, and the string that reaches this path is
    whatever the operator pasted. When that paste is an account number, the bare
    ``ValueError`` prints it, and an account number never enters a log, a
    traceback or an artifact. This class reports the variable, the expected shape
    and the observed shape, and nothing else.

    It is a :class:`ConfigError`, so the CLI records a typed absence instead of
    exiting on an uncaught traceback.
    """


class PaperOnlyClauseError(ConfigError):
    """A live session was requested while the paper-only clause is in force."""


def load_dotenv(path: Path = ENV_PATH) -> dict[str, str]:
    """Read ``KEY=VALUE`` lines from a ``.env``. Process environment wins."""
    values: dict[str, str] = {}
    if not path.exists():
        return values
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        values[key.strip()] = value.strip()
    return values


def _require_int(source: dict[str, str], name: str) -> int:
    """Require a variable that must parse as a non-negative integer.

    Shape is validated here rather than by ``int()`` at the call site, for two
    reasons that fail differently. ``int()`` raises ``ValueError``, which is not
    a :class:`ConfigError`, so the CLI's absence recording does not catch it. And
    ``ValueError`` embeds the value it failed on, which for a mis-pasted account
    number puts a credential-shaped identifier into a traceback.
    """
    text = _require(source, name)
    if not text.isdigit():
        raise MalformedConfigError(
            f"{name} is set but is not an integer. The TWS API clientId is an "
            f"int32, so a non-numeric value cannot be one. Observed shape: "
            f"length {len(text)}, first character class "
            f"{'alphabetic' if text[:1].isalpha() else 'non-alphanumeric'}. "
            f"The value itself is not reported: a value of that shape in this "
            f"slot is most often an account number pasted into it, and an "
            f"account number never enters a log or an artifact. Set {name} to a "
            f"small integer distinct from every other session against this "
            f"Gateway."
        )
    return int(text)


def _require(source: dict[str, str], name: str) -> str:
    value = source.get(name, "").strip()
    if not value:
        raise MissingConfigError(
            f"{name} is unset or empty. Set it in .env, copying the shape from "
            ".env.example. This repository holds no default for it, because a "
            "default account number or a default port is how a session ends up "
            "somewhere nobody chose."
        )
    return value


@final
@dataclass(frozen=True, slots=True)
class GatewayConfig:
    """What a session was asked to connect to. An intent, never a measurement."""

    declared: Environment
    host: str
    port: int
    client_id: int
    expected_account: str

    @classmethod
    def load(
        cls,
        declared: Environment,
        *,
        environ: dict[str, str] | None = None,
        dotenv_path: Path = ENV_PATH,
    ) -> GatewayConfig:
        """Load configuration for one environment, refusing a live request.

        The paper-only clause is enforced here rather than at connection time, so
        a live session is refused before a socket is opened rather than after.
        """
        if declared is Environment.LIVE:
            raise PaperOnlyClauseError(
                "REFUSED: the paper-only clause is in force and no live Gateway "
                "session runs in this repository. Two operator constraints are "
                "recorded rather than worked around: the machine's internal fans "
                "are not functioning, so concurrent live and paper sessions are "
                "not run, and no separate live profile exists for this project. "
                "Lifting the clause is an operator edit to CLAUDE.md, never a flag."
            )
        source = {
            **load_dotenv(dotenv_path),
            **(environ if environ is not None else dict(os.environ)),
        }
        return cls(
            declared=declared,
            host=_require(source, "MBT_IB_HOST"),
            port=_require_int(source, "MBT_IB_PAPER_PORT"),
            client_id=_require_int(source, "MBT_IB_PAPER_CLIENT_ID"),
            expected_account=_require(source, "MBT_IB_PAPER_ACCOUNT"),
        )

    def as_row(self) -> dict[str, str | int]:
        """Artifact form. The account number never appears, only its shape."""
        return {
            "declared": str(self.declared),
            "host": self.host,
            "port": self.port,
            "client_id": self.client_id,
            "expected_account_prefix": self.expected_account[:1].upper(),
            "expected_account_length": len(self.expected_account),
        }
