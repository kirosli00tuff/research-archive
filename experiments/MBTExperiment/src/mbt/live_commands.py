"""The four commands that open a Gateway session. Every one is a preview or a read.

Split from :mod:`mbt.cli`, which keeps the argument wiring and the offline
commands. The division is by whether a command touches the broker, because that
is the line that decides whether it can run in a test without one.

**None of these transmits an order.** ``tools/no_transmit_scan.py`` walks this
parse tree with the rest of the package.
"""

from __future__ import annotations

import argparse
from typing import Any

from mbt.absence import AbsenceReason, Absent, Maybe
from mbt.artifacts import CENSUS_PATH, REPORTS, emit
from mbt.broker import build_short_option_order, what_if_order
from mbt.census import (
    CensusDistinctnessError,
    CensusLedger,
    CensusWindow,
    RefusedWindow,
    build_window,
    check_distinct,
    summarise,
    window_stub_from_row,
)
from mbt.clock import iso_utc, utc_now
from mbt.config import ConfigError, GatewayConfig
from mbt.provenance import Environment, SessionProvenance
from mbt.quotes import Quote
from mbt.registry import MBT_NOTIONAL_USD, TENOR_TARGET_DAYS


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
        emit(payload, REPORTS / "task1" / "probe_session.json")
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

    emit(payload, REPORTS / "task1" / "probe_session.json")
    return 0


def cmd_census(args: argparse.Namespace) -> int:
    """PAPER. Append one distinct observation window across all three legs.

    **Discrete sampling, with the session closed between windows.** The machine's
    internal fans are not functioning, so this is never run as a resident
    collector. One invocation is one attempted window and the session is closed
    on the way out.

    **A refused window is recorded with its reason and never dropped.** Dropping
    refusals to reach 20 would turn the count into a selection, and the selection
    would be on exactly the book states the refusal conditions identify as
    unusual.
    """
    from mbt.chain import resolve_straddle
    from mbt.collect import enumerate_series, front_future
    from mbt.probe import sample_leg

    ledger = CensusLedger(CENSUS_PATH)
    try:
        config = GatewayConfig.load(Environment(args.env))
    except ConfigError as exc:
        payload: dict[str, Any] = {
            "command": "census",
            "ok": False,
            "appended": False,
            "at": iso_utc(utc_now(), "cmd_census"),
            "absent": Absent(AbsenceReason.NOT_SERVED, str(exc)).as_row(),
            "census": summarise(ledger).as_row(),
        }
        emit(payload, REPORTS / "task5" / "census_status.json")
        return 1

    from ib_async import IB, FuturesOption

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
        environment = provenance.measured
        at = utc_now()
        note = "reqMarketDataType(1) requested; the status recorded is what was served"
        ib.reqMarketDataType(1)

        future = front_future(ib)
        if isinstance(future, Absent):
            row: CensusWindow | RefusedWindow = RefusedWindow(
                local_ts=iso_utc(at, "cmd_census"),
                environment=environment,
                reason=str(future.reason),
                detail=future.detail,
                leg="future_hedge",
            )
        else:
            reference_raw, reference = sample_leg(
                ib, future, "future_hedge", subscription_note=note
            )
            if isinstance(reference, Absent):
                # Section 3.1: no reference price means no at-the-money strike,
                # and the whole straddle is refused rather than resolved against
                # a substitute.
                row = RefusedWindow(
                    local_ts=iso_utc(at, "cmd_census"),
                    environment=environment,
                    reason=str(reference.reason),
                    detail=(
                        f"the at-the-money reference leg was refused, so the whole "
                        f"straddle is refused under registered Section 3.1: "
                        f"{reference.detail}"
                    ),
                    leg="future_hedge",
                )
            else:
                series = enumerate_series(ib, at)
                nearest = min(
                    series, key=lambda s: abs(s.expiry.days_to_expiry(at) - TENOR_TARGET_DAYS)
                )
                selection = resolve_straddle(
                    [s.expiry for s in series], list(nearest.strikes), reference, at
                )
                if isinstance(selection, Absent):
                    row = RefusedWindow(
                        local_ts=iso_utc(at, "cmd_census"),
                        environment=environment,
                        reason=str(selection.reason),
                        detail=selection.detail,
                        leg="straddle_resolution",
                    )
                else:
                    expiry_text = selection.expiry.label.split(":")[1]
                    trading_class = selection.expiry.label.split(":")[0]
                    legs: dict[str, Quote] = {}
                    if not isinstance(reference_raw, Absent):
                        legs["future_hedge"] = reference_raw
                    for leg_name, right in (("option_call", "C"), ("option_put", "P")):
                        qualified = ib.qualifyContracts(
                            FuturesOption(
                                symbol="MBT",
                                lastTradeDateOrContractMonth=expiry_text,
                                strike=selection.strike,
                                right=right,
                                exchange="CME",
                                tradingClass=trading_class,
                                multiplier="0.1",
                            )
                        )
                        if qualified:
                            raw, _ = sample_leg(ib, qualified[0], leg_name, subscription_note=note)
                            if not isinstance(raw, Absent):
                                legs[leg_name] = raw
                    row = build_window(
                        len(ledger.accepted()) + 1,
                        legs,
                        environment=environment,
                        notional=MBT_NOTIONAL_USD,
                        local_ts=at,
                        note=f"strike {selection.strike} expiry {selection.expiry.label}",
                    )

        appended = False
        distinctness: str = "not reached"
        if isinstance(row, CensusWindow):
            try:
                check_distinct(at, [window_stub_from_row(r) for r in ledger.accepted()])
                distinctness = "ACCEPTED by the registered distinctness rule"
                ledger.append(row)
                appended = True
            except CensusDistinctnessError as exc:
                distinctness = str(exc)
        else:
            ledger.append(row)
            appended = True
            distinctness = "n/a: a refused window carries no distinctness claim"

        payload = {
            "command": "census",
            "ok": True,
            "at": iso_utc(utc_now(), "cmd_census"),
            "environment": str(environment),
            "attempted": row.as_row(),
            "appended": appended,
            "distinctness": distinctness,
            "census": summarise(ledger).as_row(),
            "broker_errors": errors,
        }
    finally:
        ib.disconnect()

    emit(payload, REPORTS / "task5" / "census_status.json")
    return 0


def cmd_straddle(args: argparse.Namespace) -> int:
    """PAPER. Resolve the registered ATM 30-day straddle from the live chain.

    **Every registered rule is applied as written.** The at-the-money reference
    is the midpoint of the MBT front future's touch, the tenor is measured to the
    expiry's settlement instant, and the whole straddle is refused if the
    future's quote is refused for any of the reasons in Section 3.4. That last
    clause is registered and is obeyed rather than worked around: no reference
    price means no at-the-money strike, and one is never substituted.
    """
    from mbt.chain import resolve_straddle
    from mbt.collect import enumerate_series, front_future
    from mbt.probe import sample_leg

    config = GatewayConfig.load(Environment(args.env))
    from ib_async import IB

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
        at = utc_now()
        future = front_future(ib)
        series = enumerate_series(ib, at)

        ib.reqMarketDataType(1)
        if isinstance(future, Absent):
            reference_row: object = future.as_row()
            resolved: object = future.as_row()
        else:
            raw, screened = sample_leg(
                ib,
                future,
                "future_hedge",
                subscription_note="reqMarketDataType(1) requested for the ATM reference",
            )
            reference_row = raw.as_row()
            if isinstance(screened, Absent):
                resolved = screened.as_row()
            else:
                nearest = min(
                    series, key=lambda s: abs(s.expiry.days_to_expiry(at) - TENOR_TARGET_DAYS)
                )
                outcome = resolve_straddle(
                    [s.expiry for s in series], list(nearest.strikes), screened, at
                )
                resolved = outcome.as_row()

        payload = {
            "command": "straddle",
            "at": iso_utc(utc_now(), "cmd_straddle"),
            "environment": str(provenance.measured),
            "registered_rules_applied": {
                "atm_reference": "the midpoint of the MBT front future's touch (Section 3.1)",
                "atm_strike": "nearest listed strike, ties to the LOWER strike (Section 3.2)",
                "tenor": (
                    "listed expiry nearest 30 days measured to the SETTLEMENT "
                    "INSTANT, ties to the LONGER tenor (Section 3.3)"
                ),
                "refusal": (
                    "if the future's quote is refused for any reason in Section "
                    "3.4, the whole straddle is refused (Section 3.1)"
                ),
            },
            "front_future": (
                future.localSymbol if not isinstance(future, Absent) else future.as_row()
            ),
            "series_listed": len(series),
            "reference_quote": reference_row,
            "straddle": resolved,
            "resolved": not (isinstance(resolved, dict) and resolved.get("absent") == "true"),
            "broker_errors": errors,
        }
    finally:
        ib.disconnect()

    emit(payload, REPORTS / "task3" / "straddle.json")
    return 0 if payload["resolved"] else 1


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

    emit(payload, REPORTS / "task4" / "known_answer.json")
    return 0 if payload.get("agrees") is True else 1
