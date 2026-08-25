#!/usr/bin/env python
"""Stage A.1b: the fractional question, settled by paper order behaviour.

The only stage authorized to place paper orders. API capability tests,
not strategy trades. Hard rails enforced in code below: at most ten
orders, every order addressed to the pinned paper account, SmartRouted,
tif DAY, and the run ends by cancelling everything open and proving the
account flat. No live account, no live endpoint, no strategy.

Every request, response, and status transition is appended to
reports/stage_a1b/evidence.jsonl, its own evidence ledger, separate
from the spend ledger. The rendered report lands beside it.

Market-hours honesty: order ACCEPTANCE is validated by the Gateway at
submission any hour. FILLS need a session. The script records exactly
what the clock allows and never synthesizes the rest.
"""
from __future__ import annotations

import datetime
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

from ib_async import IB, LimitOrder, MarketOrder, Order, Stock  # noqa: E402

from hfexperiment.brokerconfig import (  # noqa: E402
    DECLARED_MODE,
    MODE_PORTS,
    MODE_PREFIXES,
    load_broker_env,
)
from hfexperiment.ledger import Ledger  # noqa: E402

FORMATION_JSON = ROOT / "reports" / "stage_c1" / "formation_2026-08-03.json"
EVIDENCE = ROOT / "reports" / "stage_a1b" / "evidence.jsonl"

ORDER_CAP = 10
NOTIONAL = 45.00
MOST_LIQUID = "MU"    # measured from the C.1 store, 48.3B USD/day median
LEAST_LIQUID = "TE"   # measured from the C.1 store, 0.28B USD/day median
WAIT_S = 8.0

READ_ONLY_MARKERS = ("read-only", "read only", "readonly")


class OrderCapExceededError(RuntimeError):
    pass


def now_utc() -> str:
    return datetime.datetime.now(datetime.UTC).strftime(
        "%Y-%m-%dT%H:%M:%S.%fZ"
    )


class Evidence:
    def __init__(self) -> None:
        EVIDENCE.parent.mkdir(parents=True, exist_ok=True)
        if EVIDENCE.exists():
            EVIDENCE.unlink()
        self._ledger = Ledger(EVIDENCE)

    def rec(self, kind: str, **fields: Any) -> None:
        self._ledger.append({"kind": kind, "utc": now_utc(), **fields})


class A1b:
    def __init__(self) -> None:
        self.env = load_broker_env(ROOT / ".env")
        prefix = MODE_PREFIXES[DECLARED_MODE]
        if self.env.port != MODE_PORTS[DECLARED_MODE]:
            raise SystemExit(
                f"REFUSING: declared mode {DECLARED_MODE} requires port "
                f"{MODE_PORTS[DECLARED_MODE]}, .env has {self.env.port}"
            )
        if not self.env.account_id.startswith(prefix):
            raise SystemExit(
                f"REFUSING: {self.env.account_id} lacks the "
                f"{DECLARED_MODE} prefix {prefix}"
            )
        self.account = self.env.account_id
        self.ev = Evidence()
        self.ib = IB()
        self.orders_placed = 0
        self.trades: list[Any] = []
        self.read_only_detected: str | None = None

    # -- rails -----------------------------------------------------

    def _order_rails(self, order: Order) -> Order:
        self.orders_placed += 1
        if self.orders_placed > ORDER_CAP:
            raise OrderCapExceededError(f"order cap {ORDER_CAP} reached")
        order.account = self.account
        order.tif = "DAY"
        return order

    def place(self, symbol: str, order: Order, label: str) -> Any:
        contract = Stock(symbol, "SMART", "USD")
        order = self._order_rails(order)
        self.ev.rec(
            "order_request", label=label, symbol=symbol,
            order_type=order.orderType, action=order.action,
            total_quantity=str(order.totalQuantity),
            cash_qty=str(getattr(order, "cashQty", "")),
            lmt_price=str(getattr(order, "lmtPrice", "")),
            outside_rth=bool(order.outsideRth), tif=order.tif,
            account=order.account, route=contract.exchange,
            order_number=self.orders_placed,
        )
        trade = self.ib.placeOrder(contract, order)
        self.trades.append((label, trade))
        return trade

    def record_trade(self, label: str, trade: Any) -> list[str]:
        log_lines = []
        for entry in trade.log:
            line = (f"{entry.time:%H:%M:%S.%f} status={entry.status} "
                    f"{entry.message}".strip())
            log_lines.append(line)
            lowered = entry.message.lower()
            if any(m in lowered for m in READ_ONLY_MARKERS):
                self.read_only_detected = entry.message
        self.ev.rec(
            "order_outcome", label=label,
            order_id=trade.order.orderId,
            status=trade.orderStatus.status,
            filled=str(trade.orderStatus.filled),
            remaining=str(trade.orderStatus.remaining),
            avg_fill_price=trade.orderStatus.avgFillPrice,
            log=log_lines,
        )
        return log_lines

    def cancel_if_open(self, label: str, trade: Any) -> None:
        if not trade.isDone():
            self.ib.cancelOrder(trade.order)
            self.ib.sleep(2.0)
            self.ev.rec("cancel", label=label,
                        order_id=trade.order.orderId,
                        status=trade.orderStatus.status)

    # -- tasks -----------------------------------------------------

    def connect(self) -> None:
        self.ib.connect(
            self.env.host, self.env.port,
            clientId=self.env.client_id + 10, timeout=15,
            readonly=False,
        )
        managed = self.ib.managedAccounts()
        self.ev.rec("connected",
                    server_version=self.ib.client.serverVersion(),
                    managed=managed)
        if self.account not in managed:
            raise SystemExit(
                f"REFUSING: pinned {self.account} not in managed {managed}"
            )
        self.ib.errorEvent += self._on_error

    def _on_error(self, req_id: int, code: int, msg: str,
                  *args: Any) -> None:
        self.ev.rec("api_error", req_id=req_id, code=code, message=msg)
        lowered = msg.lower()
        if any(m in lowered for m in READ_ONLY_MARKERS):
            self.read_only_detected = f"error {code}: {msg}"

    def eligibility(self, book: list[str]) -> dict[str, dict[str, Any]]:
        out: dict[str, dict[str, Any]] = {}
        for symbol in book:
            details = self.ib.reqContractDetails(
                Stock(symbol, "SMART", "USD")
            )
            if not details:
                out[symbol] = {"error": "no contract details"}
                self.ev.rec("contract_details", symbol=symbol,
                            error="no contract details")
                continue
            d = details[0]
            row = {
                "con_id": d.contract.conId,
                "min_size": str(d.minSize),
                "size_increment": str(d.sizeIncrement),
                "suggested_size_increment": str(d.suggestedSizeIncrement),
                "long_name": d.longName,
            }
            out[symbol] = row
            self.ev.rec("contract_details", symbol=symbol, **row)
        return out

    def quote(self, symbol: str) -> dict[str, Any]:
        self.ib.reqMarketDataType(3)  # delayed is fine for a capability test
        contract = Stock(symbol, "SMART", "USD")
        self.ib.qualifyContracts(contract)
        ticker = self.ib.reqMktData(contract, "", snapshot=True)
        self.ib.sleep(4.0)
        snap = {
            "symbol": symbol,
            "bid": ticker.bid, "ask": ticker.ask, "last": ticker.last,
            "close": ticker.close, "captured_utc": now_utc(),
            "market_data_type": ticker.marketDataType,
        }
        self.ev.rec("quote_snapshot", **snap)
        self.ib.cancelMktData(contract)
        return snap

    def flatten_all(self) -> list[dict[str, Any]]:
        """Cancel everything open, then sell any position to zero."""
        for label, trade in self.trades:
            self.cancel_if_open(label, trade)
        self.ib.sleep(2.0)
        positions = [
            p for p in self.ib.positions(self.account)
            if p.position != 0
        ]
        for p in positions:
            qty = abs(p.position)
            action = "SELL" if p.position > 0 else "BUY"
            order = LimitOrder(
                action, qty,
                round(p.avgCost * (0.97 if action == "SELL" else 1.03), 2),
            )
            order.outsideRth = True
            self.ev.rec("flatten_request", symbol=p.contract.symbol,
                        action=action, qty=str(qty))
            trade = self.place(p.contract.symbol, order,
                               f"flatten-{p.contract.symbol}")
            self.ib.sleep(WAIT_S)
            self.record_trade(f"flatten-{p.contract.symbol}", trade)
            self.cancel_if_open(f"flatten-{p.contract.symbol}", trade)
        final = [
            {"symbol": p.contract.symbol, "position": str(p.position),
             "avg_cost": p.avgCost}
            for p in self.ib.positions(self.account)
            if p.position != 0
        ]
        self.ev.rec("final_positions", account=self.account,
                    open_positions=final)
        return final


def main() -> int:
    data = json.loads(FORMATION_JSON.read_text())
    book: list[str] = data["books"]["20"]
    closes: dict[str, float] = data["width20_entry_closes"]
    app = A1b()
    app.ev.rec("stage_start", account=app.account,
               declared_mode=DECLARED_MODE, order_cap=ORDER_CAP,
               most_liquid=MOST_LIQUID, least_liquid=LEAST_LIQUID)
    app.connect()
    results: dict[str, Any] = {}
    try:
        # Task 1: eligibility across the real book.
        results["eligibility"] = app.eligibility(book)

        # Task 2: decimal quantity, most liquid then least liquid.
        for symbol in (MOST_LIQUID, LEAST_LIQUID):
            snap = app.quote(symbol)
            ask = snap["ask"]
            basis = "delayed ask"
            price = ask if ask and ask > 0 else None
            if price is None:
                last = snap["last"]
                price = last if last and last > 0 else None
                basis = "delayed last"
            if price is None:
                price = closes[symbol]
                basis = "2026-08-03 store close, no delayed quote served"
            qty = round(NOTIONAL / price, 4)
            app.ev.rec("quantity_computed", symbol=symbol,
                       notional=NOTIONAL, price_basis=basis,
                       price=price, quantity=str(qty))
            trade = app.place(
                symbol, MarketOrder("BUY", qty), f"decimal-mkt-{symbol}"
            )
            app.ib.sleep(WAIT_S)
            results[f"mkt_{symbol}"] = app.record_trade(
                f"decimal-mkt-{symbol}", trade
            )
            results[f"mkt_{symbol}_status"] = trade.orderStatus.status
            results[f"mkt_{symbol}_qty"] = str(qty)
            if app.read_only_detected:
                results["read_only"] = app.read_only_detected
                return 0
            app.cancel_if_open(f"decimal-mkt-{symbol}", trade)
            if symbol == MOST_LIQUID and price is not None:
                # The overnight fill attempt: marketable limit,
                # outsideRth, SMART, DAY. Whatever happens is evidence.
                lmt = LimitOrder("BUY", qty, round(price * 1.002, 2))
                lmt.outsideRth = True
                overnight = app.place(symbol, lmt, f"decimal-lmt-{symbol}")
                app.ib.sleep(WAIT_S)
                results[f"lmt_{symbol}"] = app.record_trade(
                    f"decimal-lmt-{symbol}", overnight
                )
                results[f"lmt_{symbol}_status"] = (
                    overnight.orderStatus.status
                )
                if overnight.orderStatus.status == "Filled":
                    fill_qty = overnight.orderStatus.filled
                    sell = LimitOrder(
                        "SELL", fill_qty, round(price * 0.995, 2)
                    )
                    sell.outsideRth = True
                    flat = app.place(symbol, sell, f"flatten-lmt-{symbol}")
                    app.ib.sleep(WAIT_S)
                    results[f"flatten_{symbol}"] = app.record_trade(
                        f"flatten-lmt-{symbol}", flat
                    )
                else:
                    app.cancel_if_open(f"decimal-lmt-{symbol}", overnight)

        # Task 3: cashQty, the contradicted path.
        cash_order = MarketOrder("BUY", 0)
        cash_order.cashQty = NOTIONAL
        trade = app.place(MOST_LIQUID, cash_order, "cashqty-mkt")
        app.ib.sleep(WAIT_S)
        results["cashqty"] = app.record_trade("cashqty-mkt", trade)
        results["cashqty_status"] = trade.orderStatus.status
        app.cancel_if_open("cashqty-mkt", trade)

        # Task 4: commissions on any fills, INDICATIVE-ONLY.
        fills = app.ib.fills()
        results["fills"] = [
            {
                "symbol": f.contract.symbol,
                "side": f.execution.side,
                "shares": str(f.execution.shares),
                "price": f.execution.price,
                "commission_indicative_only":
                    f.commissionReport.commission
                    if f.commissionReport else None,
                "exec_id": f.execution.execId,
                "time": str(f.execution.time),
            }
            for f in fills
        ]
        app.ev.rec("fills", fills=results["fills"],
                   note="commissions are paper-simulated, "
                        "INDICATIVE-ONLY, settled only by D.1's live "
                        "statement reconciliation")
    finally:
        results["final_positions"] = app.flatten_all()
        app.ev.rec("orders_placed_total", count=app.orders_placed,
                   cap=ORDER_CAP)
        app.ib.disconnect()
    print(json.dumps(results, indent=1, default=str))
    return 0


if __name__ == "__main__":
    sys.exit(main())
