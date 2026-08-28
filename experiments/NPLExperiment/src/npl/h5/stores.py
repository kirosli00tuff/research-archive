"""The H5 write containment gate. H2's stores are read-only to this entry.

Every H5 write goes through `h5_store`, which resolves the target and
refuses any path that is not inside `data/h5/`. The refusal is produced by
test against a real H2 store path, never asserted in a comment, and the
containment check is the single line the registered mutation deletes.

Reading is a different question and is deliberately allowed: the
generating-sample record and the successor cohort ledgers must be *read* for
the H5 blindness gate (`npl.h5.gate`) to honour them. What this module
forbids is a write.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from npl.ledger.append_only import AppendOnlyLedger
from npl.paths import H5_DIR


class H5StoreViolation(RuntimeError):
    """An H5 path tried to write outside data/h5/. Refused loudly, nothing written."""


def h5_root() -> Path:
    return H5_DIR.resolve()


def assert_inside_h5(path: Path) -> Path:
    """Resolve and refuse any target outside the H5 write root."""
    root = h5_root()
    candidate = path if path.is_absolute() else (Path.cwd() / path)
    resolved = candidate.resolve()
    if resolved != root and root not in resolved.parents:
        raise H5StoreViolation(
            f"refusing an H5 write to {resolved}: every H5 store lives under {root}. "
            f"H2's collectors, ledgers, latches, and stores are read-only to this entry."
        )
    return resolved


def h5_store(path: Path) -> AppendOnlyLedger:
    """The only constructor of an append-only ledger on any H5 path."""
    return AppendOnlyLedger(assert_inside_h5(path))


def read_rows(path: Path) -> list[dict[str, Any]]:
    """Read any JSON-lines ledger and return its rows. Never a writable handle.

    The cohort ledgers H5 must honour live outside `data/h5/`, so reading
    them is both allowed and required. This function is the one place an H5
    path may touch a ledger outside the write root, and it hands back plain
    rows: there is no object here anything could append through.
    """
    return AppendOnlyLedger(path).require_intact()
