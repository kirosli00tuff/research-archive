"""Guard four — the deciding-read latch. One spend per registered figure.

Ported by copying from VRPExperiment TASK 6, with two changes this repository
needs.

**Keyed per figure.** VRPExperiment had one deciding read and therefore one
latch. This repository has two registered figures, the margin and the cost, and
a latch that could not tell them apart would let spending one lock out the other.

**Fsynced before returning.** VRPExperiment wrote the latch with
``Path.write_text`` and returned. A write that has not reached the platter is a
latch that a power cut converts back into an unspent one, and the whole point of
a latch is that it survives the process that wrote it. The file is fsynced and
then the containing **directory** is fsynced, because on POSIX the directory
entry is a separate write and fsyncing only the file can leave a durable file
nobody can find.

It is built and tested in this stage even though no live read happens here.
Retrofitting a latch into a session that already has a live connection open is
the wrong order: by then the read the latch exists to protect has a path to
happen first.
"""

from __future__ import annotations

import hashlib
import json
import os
from dataclasses import dataclass
from enum import StrEnum, unique
from pathlib import Path
from typing import final

from mbt.clock import iso_utc, utc_now


@unique
class LatchedFigure(StrEnum):
    """The registered figures whose deciding read is latched. One spend each."""

    MARGIN_SHORT_MBT_OPTION = "margin_short_mbt_option"
    """The initial margin on a short MBT option. Needs a U-prefixed session, so
    it is unspent in this stage and recorded Absent(no_live_session)."""

    COST_ABSENT_LEGS_P90 = "cost_absent_legs_p90"
    """The all-in option and future bid-ask plus exchange and regulatory fees at
    the p90 end."""


class LatchError(PermissionError):
    """Base class for every refusal the latch machinery can raise."""


class LatchAlreadySpentError(LatchError):
    """A second spend of a registered figure. **This voids the registration.**"""


class LatchNotWrittenError(LatchError):
    """A latched read was attempted with no latch record on disk."""


@final
@dataclass(frozen=True, slots=True)
class LatchRecord:
    """One latch. Records what was about to be read, and by which code."""

    figure: LatchedFigure
    written_at: str
    module_hashes: dict[str, str]
    note: str

    def as_row(self) -> dict[str, object]:
        return {
            "figure": str(self.figure),
            "written_at": self.written_at,
            "module_hashes": dict(self.module_hashes),
            "note": self.note,
        }


def hash_modules(paths: list[Path]) -> dict[str, str]:
    """SHA-256 of each participating module, keyed by path, sorted."""
    return {str(path): hashlib.sha256(path.read_bytes()).hexdigest() for path in sorted(paths)}


def _write_durably(path: Path, payload: str) -> None:
    """Write, flush, fsync the file, then fsync the directory. In that order.

    Returning before the bytes are durable would make the latch a promise rather
    than a fact. The directory fsync is not optional on POSIX: without it the
    file's own data can be durable while the directory entry naming it is not.
    """
    handle = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o644)
    try:
        os.write(handle, payload.encode("utf-8"))
        os.fsync(handle)
    finally:
        os.close(handle)
    dir_handle = os.open(path.parent, os.O_RDONLY)
    try:
        os.fsync(dir_handle)
    finally:
        os.close(dir_handle)


@final
class Latch:
    """The deciding-read latch, keyed per registered figure."""

    __slots__ = ("_root",)

    def __init__(self, root: Path) -> None:
        self._root = root
        self._root.mkdir(parents=True, exist_ok=True)

    @property
    def root(self) -> Path:
        return self._root

    def path_for(self, figure: LatchedFigure) -> Path:
        return self._root / f"{figure.value}.latch.json"

    def is_spent(self, figure: LatchedFigure) -> bool:
        return self.path_for(figure).exists()

    def spend(self, figure: LatchedFigure, modules: list[Path], note: str) -> LatchRecord:
        """Spend the latch for one figure. Refuses if it is already spent.

        The refusal is checked twice, once by an explicit test and once by
        ``O_EXCL`` on the open. The explicit test gives the caller a readable
        error, and ``O_EXCL`` closes the window between the test and the write in
        which a second process could spend the same figure.
        """
        path = self.path_for(figure)
        if path.exists():
            raise LatchAlreadySpentError(
                f"the latch for {figure.value!r} at {path} is already spent. "
                "One spend per registered figure. A second deciding read voids "
                "the registration; the recorded result stands and is not re-run."
            )
        record = LatchRecord(
            figure=figure,
            written_at=iso_utc(utc_now(), "Latch.spend"),
            module_hashes=hash_modules(modules),
            note=note,
        )
        payload = json.dumps(record.as_row(), sort_keys=True, indent=2) + "\n"
        try:
            _write_durably(path, payload)
        except FileExistsError as exc:
            raise LatchAlreadySpentError(
                f"the latch for {figure.value!r} at {path} was spent by another "
                "writer between the check and the write. One spend per figure."
            ) from exc
        return record

    def read_record(self, figure: LatchedFigure) -> LatchRecord:
        path = self.path_for(figure)
        if not path.exists():
            raise LatchNotWrittenError(
                f"no latch for {figure.value!r} at {path}: a deciding read "
                "requires a latch written before it, not after."
            )
        raw = json.loads(path.read_text(encoding="utf-8"))
        return LatchRecord(
            figure=LatchedFigure(str(raw["figure"])),
            written_at=str(raw["written_at"]),
            module_hashes={str(k): str(v) for k, v in raw["module_hashes"].items()},
            note=str(raw["note"]),
        )

    def drifted_modules(
        self, figure: LatchedFigure, modules: list[Path]
    ) -> dict[str, tuple[str, str]]:
        """Every module whose hash moved since the latch was written."""
        recorded = self.read_record(figure).module_hashes
        current = hash_modules(modules)
        return {
            name: (digest, current.get(name, "<absent>"))
            for name, digest in recorded.items()
            if current.get(name, "<absent>") != digest
        }

    def require_unspent(self, figure: LatchedFigure) -> None:
        """Guard for callers that must not run after a figure's latch is spent."""
        if self.is_spent(figure):
            raise LatchAlreadySpentError(
                f"the latch for {figure.value!r} is spent: this code path may "
                "not run a second time."
            )
