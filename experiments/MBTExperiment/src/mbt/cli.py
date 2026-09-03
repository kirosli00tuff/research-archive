"""Command line entry points. Every one is a preview or a read; none transmits.

``whatif-live`` does not exist as a subcommand. The paper-only clause is enforced
in :meth:`GatewayConfig.load`, which refuses a live request before a socket is
opened, and the Makefile target prints the refusal and exits non-zero.
"""

from __future__ import annotations

import argparse
import sys
from typing import Any

from mbt.absence import AbsenceReason, Absent
from mbt.artifacts import CENSUS_PATH, REPORTS, emit
from mbt.census import CensusLedger, summarise
from mbt.clock import iso_utc, utc_now
from mbt.config import ConfigError, GatewayConfig
from mbt.gates import GateName, fire, fire_lower_bound
from mbt.provenance import Environment
from mbt.registry import (
    COST_CEILING_BPS,
    MARGIN_CEILING_USD_PER_CONTRACT,
    MIN_OBSERVATION_WINDOWS,
    REGISTERED_PREMIUM_BASIS,
)
from mbt.session import unreachable
from mbt.verdict import decide


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
    emit(payload, REPORTS / "task0" / "probe_session.json")
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

    # The COST gate. Its fee leg is Absent(not_served) regardless of environment,
    # so the all-in sum cannot be formed and the gate falls back to the measured
    # legs as a strict lower bound. That bound can FAIL and can never PASS.
    absent_legs = ["exchange_and_regulatory_fee", "ibkr_daily_exposure_fee"]
    if summary.meets_minimum and not isinstance(summary.p90_bps, Absent):
        cost_result = fire_lower_bound(
            GateName.COST,
            summary.p90_bps,
            ceiling=COST_CEILING_BPS,
            unit="bps_of_notional",
            absent_legs=absent_legs,
        )
    else:
        cost_result = fire(
            GateName.COST,
            Absent(
                AbsenceReason.INSUFFICIENT_SAMPLE,
                f"{summary.n_accepted} of {MIN_OBSERVATION_WINDOWS} registered "
                f"windows collected, and the fee leg is Absent(not_served) "
                f"regardless. The gate fires only when the minimum is met.",
            ),
            ceiling=COST_CEILING_BPS,
            unit="bps_of_notional",
        )

    outcome = decide()
    payload = {
        "command": "gates",
        "at": iso_utc(utc_now(), "cmd_gates"),
        "registered_premium_basis": str(REGISTERED_PREMIUM_BASIS),
        "registered_cost_ceiling_bps": COST_CEILING_BPS,
        "census": summary.as_row(),
        "gates": [margin_result.as_row(), cost_result.as_row()],
        "stage_verdict": outcome.as_row(),
        "open_operator_items": [
            "MBT_IB_PAPER_CLIENT_ID is unset in .env",
            "IB Gateway is not running; it needs an interactive IBKR login",
            "the live margin read needs a U-prefixed session, blocked by the "
            "non-functioning internal fans and by the absence of a live profile",
        ],
    }
    emit(payload, REPORTS / "task7" / "gates.json")
    return 0


def cmd_verdict(_: argparse.Namespace) -> int:
    """Offline. Recompute the stage verdict from the recorded artifacts."""
    outcome = decide()
    emit(outcome.as_row(), REPORTS / "task7" / "verdict.json")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="mbt", description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)

    from mbt.live_commands import (
        cmd_census,
        cmd_known_answer,
        cmd_probe_full,
        cmd_straddle,
    )

    probe_p = sub.add_parser("probe", help="PAPER. Connect and record provenance")
    probe_p.add_argument("--env", default="paper", choices=[e.value for e in Environment])
    probe_p.set_defaults(func=cmd_probe)

    census_p = sub.add_parser("census", help="PAPER. Append one observation window")
    census_p.add_argument("--env", default="paper", choices=[e.value for e in Environment])
    census_p.set_defaults(func=cmd_census)

    full_p = sub.add_parser("probe-full", help="PAPER. Handshake, permission, feed state")
    full_p.add_argument("--env", default="paper", choices=[e.value for e in Environment])
    full_p.set_defaults(func=cmd_probe_full)

    st_p = sub.add_parser("straddle", help="PAPER. Resolve the registered ATM 30-day straddle")
    st_p.add_argument("--env", default="paper", choices=[e.value for e in Environment])
    st_p.set_defaults(func=cmd_straddle)

    ka_p = sub.add_parser("known-answer", help="PAPER. Reproduce a checkable margin")
    ka_p.add_argument("--env", default="paper", choices=[e.value for e in Environment])
    ka_p.set_defaults(func=cmd_known_answer)

    gates_p = sub.add_parser("gates", help="Offline. Fire the gates from recorded figures")
    gates_p.set_defaults(func=cmd_gates)

    verdict_p = sub.add_parser("verdict", help="Offline. Recompute the stage verdict")
    verdict_p.set_defaults(func=cmd_verdict)

    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    result: int = args.func(args)
    return result


if __name__ == "__main__":
    sys.exit(main())
