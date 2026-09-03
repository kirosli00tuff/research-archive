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

from mbt.absence import AbsenceReason, Absent, Maybe
from mbt.broker import build_short_option_order, what_if_order
from mbt.census import CensusLedger, summarise
from mbt.clock import iso_utc, utc_now
from mbt.config import ConfigError, GatewayConfig
from mbt.gates import GateName, fire, fire_lower_bound
from mbt.provenance import Environment, SessionProvenance
from mbt.registry import (
    COST_CEILING_BPS,
    MARGIN_CEILING_USD_PER_CONTRACT,
    MIN_OBSERVATION_WINDOWS,
    REGISTERED_PREMIUM_BASIS,
    TENOR_TARGET_DAYS,
)
from mbt.session import unreachable
from mbt.verdict import decide

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


def cmd_probe_full(args: argparse.Namespace) -> int:
    """PAPER. Stage B.1 Task 1: handshake, accounts, permission, feed state.

    Each measurement is separate because each failed separately in Stage B. A
    TCP connect proves a listener, a handshake proves a session, and neither
    proves a market-data subscription.
    """
    import time

    from mbt.collect import enumerate_series, front_future
    from mbt.probe import BoundedWhatIfBroker, observe_feed, probe_permission

    declared = Environment(args.env)
    try:
        config = GatewayConfig.load(declared)
    except ConfigError as exc:
        payload = {
            "command": "probe-full",
            "ok": False,
            "stage": "config",
            "absent": Absent(AbsenceReason.NOT_SERVED, str(exc)).as_row(),
            "at": iso_utc(utc_now(), "cmd_probe_full"),
        }
        _emit(payload, REPORTS / "task1" / "probe_session.json")
        return 1

    from ib_async import IB, FuturesOption

    ib = IB()
    errors: list[str] = []
    ib.errorEvent += lambda reqId, code, msg, contract: errors.append(
        f"reqId={reqId} code={code} {msg[:180]}"
    )

    started = time.perf_counter()
    ib.connect(config.host, config.port, clientId=config.client_id, timeout=20)
    handshake = time.perf_counter() - started

    try:
        accounts = list(ib.managedAccounts())
        provenance = SessionProvenance.from_connection(
            declared=declared,
            connected_account=accounts[0],
            client_id=config.client_id,
            host=config.host,
            port=config.port,
        )

        at = utc_now()
        future = front_future(ib)
        series = enumerate_series(ib, at)
        nearest = min(
            series,
            key=lambda s: abs(s.expiry.days_to_expiry(at) - TENOR_TARGET_DAYS),
            default=None,
        )

        legs: dict[str, object] = {}
        permission_row: object = Absent(
            AbsenceReason.NOT_SERVED, "no listed series, so no option to price"
        ).as_row()
        if nearest is not None and not isinstance(future, Absent):
            strikes = list(nearest.strikes)
            probe_strike = strikes[len(strikes) // 2]
            call = ib.qualifyContracts(
                FuturesOption(
                    symbol="MBT",
                    lastTradeDateOrContractMonth=nearest.expiry.label.split(":")[1],
                    strike=probe_strike,
                    right="C",
                    exchange="CME",
                    tradingClass=nearest.trading_class,
                    multiplier="0.1",
                )
            )
            put = ib.qualifyContracts(
                FuturesOption(
                    symbol="MBT",
                    lastTradeDateOrContractMonth=nearest.expiry.label.split(":")[1],
                    strike=probe_strike,
                    right="P",
                    exchange="CME",
                    tradingClass=nearest.trading_class,
                    multiplier="0.1",
                )
            )
            if call and put:
                legs = {"future_hedge": future, "option_call": call[0], "option_put": put[0]}
                permission = probe_permission(BoundedWhatIfBroker(ib), call[0], errors)
                permission_row = permission.as_row()

        feed = {
            "realtime_requested": [o.as_row() for o in observe_feed(ib, legs, 1)] if legs else [],
            "delayed_requested": [o.as_row() for o in observe_feed(ib, legs, 3)] if legs else [],
        }

        payload = {
            "command": "probe-full",
            "ok": True,
            "at": iso_utc(utc_now(), "cmd_probe_full"),
            "api_handshake_seconds": round(handshake, 4),
            "accounts_returned": len(accounts),
            "provenance": provenance.as_row(),
            "config": config.as_row(),
            "front_future": (
                future.localSymbol if not isinstance(future, Absent) else future.as_row()
            ),
            "series_listed": len(series),
            "series": [s.as_row() for s in series],
            "nearest_to_registered_tenor": nearest.as_row() if nearest else None,
            "permission_probe": permission_row,
            "feed": feed,
            "orders_open_after_probe": len(ib.openOrders()),
            "trades_after_probe": len(ib.trades()),
            "positions_after_probe": len(ib.positions()),
            "fills_after_probe": len(ib.fills()),
            "broker_errors": errors,
        }
    finally:
        ib.disconnect()

    _emit(payload, REPORTS / "task1" / "probe_session.json")
    return 0


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


def cmd_known_answer(args: argparse.Namespace) -> int:
    """PAPER. Reproduce an independently checkable margin through the MBT path.

    **The product is liquid and the path is the same one that would read MBT.**
    A pipeline that has only ever been pointed at the instrument it was built for
    has never been checked against anything, so the check runs the package's own
    preview wrapper rather than a reimplementation of it that happens to work.

    **The expected margin is an OPERATOR INPUT.** CME refused automated access to
    its schedule, citing its own Data Terms of Use, and that refusal is obeyed
    here. With no operator value supplied the check records an absence and the
    MBT output stays untrusted. An absence is not a pass.
    """
    import os
    import time

    from mbt.config import load_dotenv
    from mbt.probe import BoundedWhatIfBroker
    from mbt.whatif import known_answer_check

    source_env = {**load_dotenv(), **dict(os.environ)}
    symbol = source_env.get("MBT_KNOWN_ANSWER_SYMBOL", "ES").strip() or "ES"
    expected_text = source_env.get("MBT_KNOWN_ANSWER_MARGIN_USD", "").strip()
    expected_source = source_env.get("MBT_KNOWN_ANSWER_SOURCE", "").strip()

    expected: Maybe[float]
    if not expected_text:
        expected = Absent(
            AbsenceReason.NOT_YET_MEASURED,
            "MBT_KNOWN_ANSWER_MARGIN_USD is unset, so no independently checkable "
            "margin was supplied to compare against. The expected value is an "
            "operator input read by a person, because CME's Data Terms of Use "
            "refusal binds automated access to its schedule. This repository does "
            "not scrape it, infer it from a third party, or carry one from "
            "another repository.",
        )
    else:
        try:
            expected = float(expected_text)
        except ValueError:
            expected = Absent(
                AbsenceReason.NOT_SERVED,
                "MBT_KNOWN_ANSWER_MARGIN_USD did not parse as a number.",
            )

    config = GatewayConfig.load(Environment(args.env))
    from ib_async import IB, Future

    ib = IB()
    errors: list[str] = []
    ib.errorEvent += lambda reqId, code, msg, contract: errors.append(
        f"reqId={reqId} code={code} {msg[:180]}"
    )
    ib.connect(config.host, config.port, clientId=config.client_id, timeout=20)
    try:
        accounts = list(ib.managedAccounts())
        provenance = SessionProvenance.from_connection(
            declared=Environment(args.env),
            connected_account=accounts[0],
            client_id=config.client_id,
            host=config.host,
            port=config.port,
        )
        listed = [d.contract for d in ib.reqContractDetails(Future(symbol=symbol, exchange="CME"))]
        dated = [c for c in listed if c is not None and c.lastTradeDateOrContractMonth]
        if not dated:
            raise RuntimeError(f"no listed {symbol} future to check against")
        contract = min(dated, key=lambda c: c.lastTradeDateOrContractMonth)

        broker = BoundedWhatIfBroker(ib)
        started = time.perf_counter()
        order = build_short_option_order(quantity=1)
        preview = what_if_order(broker, contract, order, whatIf=True)
        elapsed = time.perf_counter() - started

        check = known_answer_check(
            product=f"{symbol} front future {contract.localSymbol}",
            expected=expected,
            preview=preview,
            source_of_expected=expected_source
            or "ABSENT: no operator-supplied source was recorded",
        )
        blockers: list[str] = []
        if isinstance(expected, Absent):
            blockers.append(
                "no operator-supplied expected margin "
                f"(MBT_KNOWN_ANSWER_MARGIN_USD unset): {expected.reason}"
            )
        if broker.last_timed_out or not preview.init_margin_change.strip():
            blockers.append(
                "the venue returned no OrderState for a what-if built by this "
                "package, so no margin was measured to compare"
            )
        payload: dict[str, Any] = {
            **check.as_row(),
            "blockers": blockers,
            "blocker_count": len(blockers),
            "detail": (
                check.detail
                if len(blockers) < 2
                else (
                    f"{len(blockers)} independent blockers, so the outcome is "
                    "over-determined and clearing either one alone would not "
                    "reproduce a known answer: " + "; ".join(blockers)
                )
            ),
            "command": "known-answer",
            "environment": str(provenance.measured),
            "code_path": (
                "mbt.broker.build_short_option_order -> mbt.broker.what_if_order, "
                "the same path that would read MBT"
            ),
            "elapsed_seconds": round(elapsed, 4),
            "venue_answered": not broker.last_timed_out,
            "broker_errors": errors,
            "orders_open_after_check": len(ib.openOrders()),
            "trades_after_check": len(ib.trades()),
        }
    finally:
        ib.disconnect()

    _emit(payload, REPORTS / "task4" / "known_answer.json")
    return 0 if payload.get("agrees") is True else 1


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
    _emit(payload, REPORTS / "task7" / "gates.json")
    return 0


def cmd_verdict(_: argparse.Namespace) -> int:
    """Offline. Recompute the stage verdict from the recorded artifacts."""
    outcome = decide()
    _emit(outcome.as_row(), REPORTS / "task7" / "verdict.json")
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

    full_p = sub.add_parser("probe-full", help="PAPER. Handshake, permission, feed state")
    full_p.add_argument("--env", default="paper", choices=[e.value for e in Environment])
    full_p.set_defaults(func=cmd_probe_full)

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
