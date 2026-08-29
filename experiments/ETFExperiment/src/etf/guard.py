"""The manual-run guard. A hand-run collector must not race a scheduled one.

The ADR-018 shape, ported: two processes appending to one ledger produce rows
ordered by neither clock nor file position, and the standing rule that
multi-process logs are ordered by clock only holds if the writers are known.
A manual run while the unit is active is refused by default and permitted only
through a named override, so the override appears in the shell history of
whoever took the risk.
"""

from __future__ import annotations

import os
import subprocess

OVERRIDE_ENV = "ETF_ALLOW_MANUAL_RUN"


class UnitActive(RuntimeError):
    """A scheduled unit is running. The manual run is refused, loudly."""


def unit_is_active(unit: str) -> bool:
    """True when systemd reports the unit active. A missing systemctl is not active."""
    try:
        result = subprocess.run(
            ["systemctl", "--user", "is-active", unit],
            capture_output=True,
            text=True,
            check=False,
        )
    except (FileNotFoundError, OSError):
        return False
    return result.stdout.strip() == "active"


def require_no_active_unit(unit: str, *, env: dict[str, str] | None = None) -> None:
    """Refuse a manual run while `unit` is active, unless the override is set."""
    environ = os.environ if env is None else env
    if environ.get(OVERRIDE_ENV) == "1":
        return
    if unit_is_active(unit):
        raise UnitActive(
            f"{unit} is active. A manual run would append to the same ledger concurrently, "
            f"and rows written by two writers cannot be ordered by clock afterwards. "
            f"Refused. Set {OVERRIDE_ENV}=1 to override deliberately."
        )
