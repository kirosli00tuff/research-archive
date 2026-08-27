"""Sealed raw writers. Bytes in, bytes on disk, a hash beside them, no parse.

A sealed file is written exactly once under a timestamped name — nothing
here can overwrite, and nothing here reads a field. The blindness boundary
stays intact because these writers have no parser at all.
"""

from __future__ import annotations

import hashlib
from pathlib import Path


class SealViolation(RuntimeError):
    """An attempt to overwrite a sealed file. Refused loudly."""


def seal_raw(directory: Path, name: str, body: bytes) -> Path:
    """Write one raw payload and its sha256 sidecar. Never overwrites."""
    directory.mkdir(parents=True, exist_ok=True)
    target = directory / f"{name}.raw"
    if target.exists():
        raise SealViolation(f"{target} already exists; sealed writes are write-once")
    target.write_bytes(body)
    digest = hashlib.sha256(body).hexdigest()
    (directory / f"{name}.sha256").write_text(digest + "\n", encoding="utf-8")
    return target


def verify_seal(path: Path) -> bool:
    sidecar = path.with_suffix(".sha256")
    if not sidecar.exists():
        raise SealViolation(f"{path} has no seal sidecar; a missing attestation is an error")
    recorded = sidecar.read_text(encoding="utf-8").strip()
    return recorded == hashlib.sha256(path.read_bytes()).hexdigest()
