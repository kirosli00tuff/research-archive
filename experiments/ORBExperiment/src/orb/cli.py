"""The entry points the systemd units call. **Inert until Stage A.3 is armed.**

Section 0 fired ``PENDING_ACCESS`` on 2026-08-29 and Stage A.3 is registered as
armed *only on GO or DEGRADED*. Both passes therefore refuse loudly and exit
non-zero rather than pretending to collect: **a collector that runs and stores
nothing looks identical in a log to one that ran and found nothing**, which is
the health/composition merge standing rule 7 forbids.
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Final

from orb.manualrun import require_no_active_unit

ROOT: Final[Path] = Path(__file__).resolve().parent.parent.parent

ARM_MESSAGE: Final[str] = (
    "ORBExperiment collectors are NOT ARMED.\n"
    "  Section 0 fired PENDING_ACCESS on 2026-08-29 (REGISTRATION.md Amendment 4).\n"
    "  Stage A.3 arms only on GO or DEGRADED, and PENDING_ACCESS is neither.\n"
    "  Two things arm it, together:\n"
    "    1. a vendor credential (docs/ACCESS.md: 0 of 9 vendors serve a bar today)\n"
    "    2. Section 0 re-firing at DEGRADED or better on real integrity measurements\n"
    "  Nothing was collected and nothing was written."
)


def _refuse() -> int:
    print(ARM_MESSAGE, file=sys.stderr)
    return 78  # EX_CONFIG


def daily() -> int:
    """The 22:15 UTC pass. Inert."""
    require_no_active_unit()
    return _refuse()


def actions() -> int:
    """The 22:45 UTC pass. Inert."""
    require_no_active_unit()
    return _refuse()


def main(argv: list[str] | None = None) -> int:
    args = sys.argv[1:] if argv is None else argv
    if not args:
        print("usage: python -m orb.cli {daily|actions}", file=sys.stderr)
        return 2
    match args[0]:
        case "daily":
            return daily()
        case "actions":
            return actions()
        case other:
            print(f"unknown command {other!r}", file=sys.stderr)
            return 2


if __name__ == "__main__":
    raise SystemExit(main())
