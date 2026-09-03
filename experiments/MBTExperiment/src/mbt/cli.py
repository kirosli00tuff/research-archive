"""Command line entry points. Every one is a preview or a read; none transmits.

``whatif-live`` does not exist as a subcommand. The paper-only clause is enforced
in :meth:`GatewayConfig.load`, which refuses a live request before a socket is
opened, and the Makefile target prints the refusal and exits non-zero.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

from mbt.absence import AbsenceReason, Absent
from mbt.census import CensusLedger, summarise
from mbt.clock import iso_utc, utc_now
from mbt.config import ConfigError, GatewayConfig
from mbt.gates import GateName, fire
from mbt.provenance import Environment
from mbt.registry import (
    COST_CEILING_BPS,
    MARGIN_CEILING_USD_PER_CONTRACT,
    MIN_OBSERVATION_WINDOWS,
    REGISTERED_PREMIUM_BASIS,
)
from mbt.session import unreachable

REPO = Path(__file__).resolve().parents[2]
CENSUS_PATH = REPO / "data" / "quotes" / "census.jsonl"
REPORTS = REPO / "reports"


def _emit(payload: dict[str, Any], out: Path | None) -> None:
    text = json.dumps(payload, indent=2, sort_keys=True, default=str) + "\n"
    if out is not None:
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(text, encoding="utf-8")
    print(text, end="")


def _connect_or_record_absent(declared: Environment) -> dict[str, Any]:
    """Load config and attempt a session, recording an absence when it fails.

    ``ib_async`` is imported inside the function rather than at module scope so
    that every offline command runs without it, and so that an import failure is
    recorded as an absence rather than crashing the whole CLI.
    """
    try:
        config = GatewayConfig.load(declared)
    except ConfigError as exc:
        return {
            "ok": False,
            "stage": "config",
            "absent": Absent(AbsenceReason.NOT_SERVED, str(exc)).as_row(),
        }

    try:
        from ib_async import IB
    except ImportError as exc:  # pragma: no cover - dependency is locked
        return {
            "ok": False,
            "stage": "import",
            "absent": Absent(AbsenceReason.NOT_SERVED, f"ib_async unavailable: {exc}").as_row(),
        }

    from mbt.session import probe

    result = probe(IB(), config)
    if not result.reachable:
        return {
            "ok": False,
            "stage": "connect",
            "probe": result.as_row(),
            "config": config.as_row(),
        }
    return {"ok": True, "stage": "connected", "probe": result.as_row(), "config": config.as_row()}


def cmd_probe(args: argparse.Namespace) -> int:
    """PAPER. Connect, read the account back, record measured provenance."""
    payload = _connect_or_record_absent(Environment(args.env))
    payload["command"] = "probe"
    payload["at"] = iso_utc(utc_now(), "cmd_probe")
    if not payload["ok"]:
        payload.setdefault(
            "probe",
            unreachable("no session was established; see the config or connect stage").as_row(),
        )
    _emit(payload, REPORTS / "task0" / "probe_session.json")
    return 0 if payload["ok"] else 1


def cmd_census(args: argparse.Namespace) -> int:
    """PAPER. Append one distinct observation window across all three legs."""
    payload = _connect_or_record_absent(Environment(args.env))
    payload["command"] = "census"
    payload["at"] = iso_utc(utc_now(), "cmd_census")
    ledger = CensusLedger(CENSUS_PATH)
    summary = summarise(ledger)
    payload["census"] = summary.as_row()
    if not payload["ok"]:
        payload["appended"] = False
        payload["reason"] = (
            "no session, so no window was appended. A missed window is a gap in a "
            "discrete sample and is recorded as one, never backfilled."
        )
    _emit(payload, REPORTS / "task5" / "census_status.json")
    return 0 if payload["ok"] else 1


def cmd_gates(_: argparse.Namespace) -> int:
    """Offline. Fire what can be fired from recorded figures, record what cannot."""
    ledger = CensusLedger(CENSUS_PATH)
    summary = summarise(ledger)

    margin_absent = Absent(
        AbsenceReason.NO_LIVE_SESSION,
        "a margin is a property of the ACCOUNT and needs a U-prefixed session. "
        "The paper-only clause is in force: the machine's internal fans are not "
        "functioning, so concurrent live and paper sessions are not run, and no "
        "separate live profile exists for this project.",
    )
    margin_result = fire(
        GateName.MARGIN,
        margin_absent,
        ceiling=MARGIN_CEILING_USD_PER_CONTRACT,
        unit="USD_per_contract",
    )

    cost_absent = Absent(
        AbsenceReason.INSUFFICIENT_SAMPLE,
        f"{summary.n_accepted} of {MIN_OBSERVATION_WINDOWS} registered windows "
        "collected, and the fee leg is Absent(not_served) regardless. The gate "
        "fires only when the minimum is met.",
    )
    cost_result = fire(GateName.COST, cost_absent, ceiling=COST_CEILING_BPS, unit="bps_of_notional")

    payload = {
        "command": "gates",
        "at": iso_utc(utc_now(), "cmd_gates"),
        "registered_premium_basis": str(REGISTERED_PREMIUM_BASIS),
        "registered_cost_ceiling_bps": COST_CEILING_BPS,
        "census": summary.as_row(),
        "gates": [margin_result.as_row(), cost_result.as_row()],
    }
    _emit(payload, REPORTS / "task7" / "gates.json")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="mbt", description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)

    probe_p = sub.add_parser("probe", help="PAPER. Connect and record provenance")
    probe_p.add_argument("--env", default="paper", choices=[e.value for e in Environment])
    probe_p.set_defaults(func=cmd_probe)

    census_p = sub.add_parser("census", help="PAPER. Append one observation window")
    census_p.add_argument("--env", default="paper", choices=[e.value for e in Environment])
    census_p.set_defaults(func=cmd_census)

    gates_p = sub.add_parser("gates", help="Offline. Fire the gates from recorded figures")
    gates_p.set_defaults(func=cmd_gates)

    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    result: int = args.func(args)
    return result


if __name__ == "__main__":
    sys.exit(main())
