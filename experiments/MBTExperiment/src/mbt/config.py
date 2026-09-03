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
            port=int(_require(source, "MBT_IB_PAPER_PORT")),
            client_id=int(_require(source, "MBT_IB_PAPER_CLIENT_ID")),
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
