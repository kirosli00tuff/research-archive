"""The manual-run guard, in the ADR-018 shape, with a named override.

A manual pass running while the timer's unit is active writes into the same
ledgers from two processes, and the second writer's rows interleave with the
first's. Standing rule 10 says to union intervals and order by clock, which
is a repair; **refusing is cheaper than repairing.**
"""

from __future__ import annotations

import os
import subprocess
from typing import Final

OVERRIDE_ENV: Final[str] = "ORB_ALLOW_MANUAL_RUN"
"""Set to ``1`` to run anyway. Named, so an override is visible in a shell history."""

UNITS: Final[tuple[str, ...]] = ("orb-daily.service", "orb-actions.service")


class UnitActiveError(RuntimeError):
    """Raised when a manual pass is attempted while a unit is running."""


def active_units(units: tuple[str, ...] = UNITS) -> tuple[str, ...]:
    """Which of ``units`` systemd reports as active right now."""
    active: list[str] = []
    for unit in units:
        try:
            result = subprocess.run(
                ["systemctl", "--user", "is-active", unit],
                capture_output=True,
                text=True,
                timeout=10,
                check=False,
            )
        except (OSError, subprocess.SubprocessError):
            continue
        if result.stdout.strip() == "active":
            active.append(unit)
    return tuple(active)


def require_no_active_unit(units: tuple[str, ...] = UNITS) -> None:
    """Refuse a manual pass while a timer's unit is running."""
    if os.environ.get(OVERRIDE_ENV) == "1":
        return
    running = active_units(units)
    if running:
        raise UnitActiveError(
            f"refusing a manual pass: {', '.join(running)} active. Two writers "
            f"interleave rows in one ledger. Set {OVERRIDE_ENV}=1 to override."
        )
