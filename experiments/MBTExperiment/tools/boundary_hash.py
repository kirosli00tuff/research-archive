#!/usr/bin/env python3
"""Hash a read-only boundary directory, per path, and emit a single digest.

Standalone by design. It imports nothing from this package and nothing from the
repository it hashes, so it runs before `uv sync` and it cannot make a closed
repository a live dependency of an open one.

The digest is a sha256 over the sorted sequence of relative path, size, and file
sha256, exactly as the stage registration specifies. Sorting is by the raw bytes
of the relative path so the digest does not move with a locale change.

This program opens every file read-only and writes nothing inside the root it is
pointed at. A path it cannot read is recorded as an error and raises a non-zero
exit rather than being skipped, because a silently skipped file is a hole in the
boundary.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
import time
from pathlib import Path

READ_CHUNK = 1024 * 1024

# Subset digests. The full digest covers the root in full and moves if a cache
# byte moves. These subsets let a reader tell "a sealed artifact changed" apart
# from "a build cache breathed", without either digest replacing the other.
VOLATILE_PREFIXES = (".git/", ".venv/", ".mypy_cache/", ".pytest_cache/", ".ruff_cache/")


def file_sha256(path: Path) -> tuple[str, int]:
    """Return (hex digest, byte size) for one file, read in chunks."""
    digest = hashlib.sha256()
    size = 0
    with path.open("rb") as handle:
        while True:
            chunk = handle.read(READ_CHUNK)
            if not chunk:
                break
            size += len(chunk)
            digest.update(chunk)
    return digest.hexdigest(), size


def walk(root: Path) -> tuple[list[tuple[bytes, str, int, str]], list[str]]:
    """Collect (relpath bytes, kind, size, digest) for every entry under root."""
    entries: list[tuple[bytes, str, int, str]] = []
    errors: list[str] = []
    for dirpath, dirnames, filenames in os.walk(root, followlinks=False):
        dirnames.sort()
        for name in sorted(filenames):
            full = Path(dirpath) / name
            rel = full.relative_to(root)
            rel_bytes = os.fsencode(str(rel))
            if full.is_symlink():
                # A symlink is recorded by its target text, never followed. A
                # followed link can leave the boundary and hash something else.
                target = os.readlink(full)
                entries.append((rel_bytes, "link", len(target), hashlib.sha256(os.fsencode(target)).hexdigest()))
                continue
            try:
                digest, size = file_sha256(full)
            except OSError as exc:
                errors.append(f"{rel}: {exc}")
                continue
            entries.append((rel_bytes, "file", size, digest))
    entries.sort(key=lambda row: row[0])
    return entries, errors


def manifest_lines(entries: list[tuple[bytes, str, int, str]]) -> list[bytes]:
    """One canonical line per entry: digest, kind, size, relative path."""
    return [
        b"%s %s %d %s\n" % (row[3].encode("ascii"), row[1].encode("ascii"), row[2], row[0])
        for row in entries
    ]


def digest_of(lines: list[bytes]) -> str:
    rolling = hashlib.sha256()
    for line in lines:
        rolling.update(line)
    return rolling.hexdigest()


def is_volatile(rel_bytes: bytes) -> bool:
    rel = os.fsdecode(rel_bytes)
    return rel.startswith(VOLATILE_PREFIXES)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", required=True, help="boundary root to hash, read-only")
    parser.add_argument("--out", required=True, help="path for the full manifest")
    parser.add_argument("--json", required=True, help="path for the summary json")
    parser.add_argument("--label", required=True, help="snapshot label, for example 'open' or 'close'")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    if not root.is_dir():
        print(f"REFUSED: root is not a directory: {root}", file=sys.stderr)
        return 2

    started = time.time()
    entries, errors = walk(root)
    elapsed = time.time() - started

    lines = manifest_lines(entries)
    full_digest = digest_of(lines)

    stable = [row for row in entries if not is_volatile(row[0])]
    stable_digest = digest_of(manifest_lines(stable))

    total_bytes = sum(row[2] for row in entries)

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("wb") as handle:
        for line in lines:
            handle.write(line)

    summary = {
        "label": args.label,
        "root": str(root),
        "taken_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(started)),
        "entry_count": len(entries),
        "stable_entry_count": len(stable),
        "total_bytes": total_bytes,
        "boundary_sha256_full": full_digest,
        "boundary_sha256_stable": stable_digest,
        "stable_excludes": list(VOLATILE_PREFIXES),
        "manifest_path": str(out_path),
        "elapsed_seconds": round(elapsed, 3),
        "errors": errors,
    }
    json_path = Path(args.json)
    json_path.parent.mkdir(parents=True, exist_ok=True)
    json_path.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    print(json.dumps(summary, indent=2, sort_keys=True))
    if errors:
        print(f"REFUSED: {len(errors)} unreadable paths under the boundary", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
