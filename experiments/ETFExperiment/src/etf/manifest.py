"""The daily seal. It attests the day that closed, and never the open day.

The solattn ADR-019 shape, ported with its defect already fixed: there, the
daily pass sealed the UTC day it was *running in*, so every seal attested a
40-minute-old partial file and all eight seals mismatched their contents. An
attestation of the wrong content is worth less than no attestation, because it
teaches readers to expect mismatches.

So: the pass on day D+1 seals day D, now closed and final. `seal_day` refuses a
day that has not closed. `read_day` verifies before serving — a sealed day whose
captures no longer match raises, and a closed day with no seal past the grace
window raises rather than reading unattested.
"""

from __future__ import annotations

import hashlib
import json
from collections.abc import Sequence
from dataclasses import dataclass
from datetime import UTC, date, datetime, timedelta
from pathlib import Path
from typing import Any

from etf.clock import iso_z
from etf.paths import MANIFEST_DIR

# The daily pass fires at 12:20 UTC; a seal missing more than this long after
# the day closed is an error, not a pass. 13 hours covers the fire plus a
# generous margin for a slow run.
SEAL_GRACE_HOURS = 13


class SealRefused(RuntimeError):
    """A seal was attempted on a day that has not closed."""


class SealMismatch(RuntimeError):
    """A sealed day's captures no longer match its attestation."""


class ManifestUnattested(RuntimeError):
    """A closed day past the grace window carries no seal. Never read as a pass."""


@dataclass(frozen=True, slots=True)
class DayManifest:
    day: date
    capture_count: int
    capture_digest: str
    sealed_at: datetime
    first_capture_at: str | None
    last_capture_at: str | None


def _digest(captures: Sequence[dict[str, Any]]) -> str:
    ordered = sorted(captures, key=lambda c: (str(c.get("captured_at")), str(c.get("sha256"))))
    payload = json.dumps(
        [[c.get("captured_at"), c.get("sha256")] for c in ordered],
        separators=(",", ":"),
    )
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def manifest_path(day: date, root: Path = MANIFEST_DIR) -> Path:
    return root / f"{day.isoformat()}.json"


def seal_day(
    day: date,
    captures: Sequence[dict[str, Any]],
    *,
    now: datetime,
    root: Path = MANIFEST_DIR,
) -> DayManifest:
    """Seal a closed UTC day. Refuses the open day and every future day."""
    if day >= now.astimezone(UTC).date():
        raise SealRefused(
            f"refusing to seal {day.isoformat()}: it has not closed at {iso_z(now)}. "
            "The pass on D+1 seals D. Sealing the open day attests a partial file."
        )
    stamps = sorted(str(c.get("captured_at")) for c in captures)
    manifest = DayManifest(
        day=day,
        capture_count=len(captures),
        capture_digest=_digest(captures),
        sealed_at=now,
        first_capture_at=stamps[0] if stamps else None,
        last_capture_at=stamps[-1] if stamps else None,
    )
    path = manifest_path(day, root)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(
            {
                "day": manifest.day.isoformat(),
                "capture_count": manifest.capture_count,
                "capture_digest": manifest.capture_digest,
                "sealed_at": iso_z(manifest.sealed_at),
                "first_capture_at": manifest.first_capture_at,
                "last_capture_at": manifest.last_capture_at,
            },
            indent=2,
            sort_keys=True,
        ),
        encoding="utf-8",
    )
    return manifest


def read_day(
    day: date,
    captures: Sequence[dict[str, Any]],
    *,
    now: datetime,
    root: Path = MANIFEST_DIR,
) -> Sequence[dict[str, Any]]:
    """Serve a day's captures, verifying the seal first. `now` is required, never guessed."""
    today = now.astimezone(UTC).date()
    path = manifest_path(day, root)
    if not path.exists():
        if day >= today:
            return captures
        closed_at = datetime.combine(day + timedelta(days=1), datetime.min.time(), tzinfo=UTC)
        if now - closed_at <= timedelta(hours=SEAL_GRACE_HOURS):
            return captures
        raise ManifestUnattested(
            f"{day.isoformat()} closed more than {SEAL_GRACE_HOURS}h ago and carries no seal. "
            "A missing attestation is an error, never a pass."
        )
    stored = json.loads(path.read_text(encoding="utf-8"))
    actual = _digest(captures)
    if stored["capture_digest"] != actual:
        raise SealMismatch(
            f"{day.isoformat()}: sealed digest {stored['capture_digest'][:12]} against actual "
            f"{actual[:12]} over {len(captures)} captures (sealed count "
            f"{stored['capture_count']}). Reported, never repaired."
        )
    return captures
