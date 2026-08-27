"""The listing watcher. Hourly poll, birth rows, seals, loud refusals.

Polls the main-dex meta and each HIP-3 dex meta under the ledger, diffs
against the known universe (census plus every prior birth row), and appends
a birth row for anything new. A 429 or 5xx writes a loud error marker and is
never read as end-of-feed. The daily pass seals yesterday's manifest (the
solattn ADR-019 shape) and never seals the open day.
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass
from datetime import date, datetime, timedelta
from pathlib import Path

from npl.callstate import CallState
from npl.census import CensusLedger
from npl.clock import iso_z, now_utc
from npl.config import CONFIG, Config
from npl.ledger.append_only import AppendOnlyLedger
from npl.paths import BIRTHS_DIR, STATE_DIR
from npl.venue import Venue, parse_meta, parse_perp_dexs


class SealError(RuntimeError):
    """A seal was asked for on a day that must not be sealed, or mismatches."""


def births_path(day: date, root: Path = BIRTHS_DIR) -> Path:
    return root / f"births-{day.isoformat()}.jsonl"


def seal_path(day: date, root: Path = BIRTHS_DIR) -> Path:
    return root / f"births-{day.isoformat()}.sha256"


def _sha256_of(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def seal_closed_day(day: date, today: date, root: Path = BIRTHS_DIR) -> str | None:
    """Seal one closed day's manifest. Refuses the open day, loudly.

    Returns the recorded digest, or None when the day has no manifest (a day
    with no births writes nothing, and an absent file is a recorded state on
    the caller's side, not a sealed empty file invented here).
    """
    if day >= today:
        raise SealError(
            f"refusing to seal {day.isoformat()}: the open day is never sealed "
            f"(today is {today.isoformat()})"
        )
    manifest = births_path(day, root)
    if not manifest.exists():
        return None
    digest = _sha256_of(manifest)
    target = seal_path(day, root)
    if target.exists():
        recorded = target.read_text(encoding="utf-8").strip()
        if recorded != digest:
            raise SealError(
                f"{manifest.name}: recorded seal {recorded[:12]}… does not match the file "
                f"({digest[:12]}…). A sealed manifest grew after sealing; reported, not repaired."
            )
        return recorded
    target.write_text(digest + "\n", encoding="utf-8")
    return digest


def verify_closed_day(day: date, today: date, root: Path = BIRTHS_DIR) -> bool:
    """A closed day with a manifest must carry a matching seal to be read."""
    manifest = births_path(day, root)
    if not manifest.exists():
        return True
    target = seal_path(day, root)
    if day >= today:
        return True  # the open day reads unsealed by design
    if not target.exists():
        raise SealError(
            f"{manifest.name}: closed day with no seal; a missing attestation is an error"
        )
    if target.read_text(encoding="utf-8").strip() != _sha256_of(manifest):
        raise SealError(f"{manifest.name}: seal mismatch")
    return True


@dataclass(frozen=True, slots=True)
class WatchReport:
    dexs_polled: int
    dexs_failed: int
    instruments_seen: int
    new_births: int


class Watcher:
    """One poll pass. Scheduling belongs to systemd, not to this class."""

    def __init__(
        self,
        venue: Venue,
        births_root: Path = BIRTHS_DIR,
        state_root: Path = STATE_DIR,
        census: CensusLedger | None = None,
        cfg: Config = CONFIG,
    ) -> None:
        self._venue = venue
        self._births_root = births_root
        self._lifecycle = AppendOnlyLedger(state_root / "watcher.jsonl")
        self._census = census
        self._cfg = cfg

    def _known_coins(self) -> set[str]:
        known: set[str] = set()
        if self._census is not None:
            known |= {row.coin for row in self._census.rows()}
        if self._births_root.exists():
            for manifest in sorted(self._births_root.glob("births-*.jsonl")):
                for row in AppendOnlyLedger(manifest).read().rows:
                    if row.get("kind") == "birth":
                        known.add(str(row["coin"]))
        return known

    def poll_once(self, now: datetime | None = None) -> WatchReport:
        at = now or now_utc()
        interval_note = f"poll cadence {self._cfg.watcher_poll_minutes}m (systemd timer)"
        known = self._known_coins()
        manifest = AppendOnlyLedger(births_path(at.date(), self._births_root))

        dexs_failed = 0
        instruments = 0
        births = 0

        plan: list[tuple[str, bytes]] = []
        main = self._venue.meta()
        if main.state is not CallState.STORED or main.body is None:
            self._error_marker("meta:main", main.state, at, interval_note)
            dexs_failed += 1
        else:
            plan.append(("", main.body))
        dex_list = self._venue.perp_dexs()
        dex_names: list[str] = []
        if dex_list.state is not CallState.STORED or dex_list.body is None:
            self._error_marker("perpDexs", dex_list.state, at, interval_note)
            dexs_failed += 1
        else:
            dex_names = [d.name for d in parse_perp_dexs(dex_list.body)]
        for name in dex_names:
            per_dex = self._venue.meta(name)
            if per_dex.state is not CallState.STORED or per_dex.body is None:
                # Loud, and never end-of-feed: the dex stays in the universe.
                self._error_marker(f"meta:{name}", per_dex.state, at, interval_note)
                dexs_failed += 1
                continue
            plan.append((name, per_dex.body))

        for dex_name, body in plan:
            for perp in parse_meta(body):
                instruments += 1
                if perp.name in known:
                    continue
                manifest.append(
                    {
                        "kind": "birth",
                        "coin": perp.name,
                        "dex": dex_name,
                        "sighted_at": iso_z(at),
                        "sz_decimals": perp.sz_decimals,
                        "max_leverage": perp.max_leverage,
                        "is_delisted": perp.is_delisted,
                    }
                )
                known.add(perp.name)
                births += 1

        self._lifecycle.append(
            {
                "kind": "heartbeat",
                "at": iso_z(at),
                "dexs_polled": len(plan),
                "dexs_failed": dexs_failed,
                "instruments_seen": instruments,
                "new_births": births,
                "note": interval_note,
            }
        )
        return WatchReport(
            dexs_polled=len(plan),
            dexs_failed=dexs_failed,
            instruments_seen=instruments,
            new_births=births,
        )

    def _error_marker(self, what: str, state: CallState, at: datetime, note: str) -> None:
        self._lifecycle.append(
            {
                "kind": "error",
                "what": what,
                "state": state.value,
                "at": iso_z(at),
                "note": f"never read as end-of-feed; {note}",
            }
        )

    def seal_yesterday(self, now: datetime | None = None) -> str | None:
        at = now or now_utc()
        return seal_closed_day(at.date() - timedelta(days=1), at.date(), self._births_root)
