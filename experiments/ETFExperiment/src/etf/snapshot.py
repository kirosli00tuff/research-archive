"""A.1 Task 3: the flow snapshotter. It stamps its own capture timestamp.

Neither selected flow source serves a per-row publication timestamp
(docs/ACCESS.md §2). **The capture timestamp this module stamps is therefore
the only print-time evidence that will ever exist**, which is why the lag
measurement is the experiment rather than a preliminary.

Two rules are load-bearing here and both were registered before the source was
fetched:

1. **The source's own `Total` column is never read.** Measured at A.1 Task 1:
   the table prints `0.0` in `Total` on a day where every per-fund cell is a
   dash, on 3 of 3 such rows over n = 336 out-of-sample rows. On the open day
   that is *every capture taken before the print lands*, so consuming `Total`
   would make every day appear to print at 00:00 UTC. The aggregate is computed
   from the five registered funds and is absent when any one of them is.
2. **A dash is never a zero.** `etf.flow.parse_cell` returns a recorded
   absence, which refuses coercion to a number.
"""

from __future__ import annotations

import hashlib
import re
from dataclasses import dataclass
from datetime import date, datetime

from etf.absence import Absent
from etf.clock import iso_z
from etf.config import CONFIG
from etf.flow import FlowCell, aggregate, parse_cell
from etf.http import PacedClient
from etf.ledger.append_only import AppendOnlyLedger
from etf.paths import SNAPSHOT_BODIES, SNAPSHOT_LEDGER
from etf.seal import seal_bytes
from etf.table import largest_table

DATE_CELL = re.compile(r"^(\d{1,2}) ([A-Z][a-z]{2}) (\d{4})$")
DATE_HEADER = "Date"
TOTAL_HEADER = "Total"


class FlowTableShape(RuntimeError):
    """The served table is not the shape the parser was registered against."""


@dataclass(frozen=True, slots=True)
class DayRow:
    """One trading day as printed in one capture."""

    trade_date: date
    per_fund: tuple[FlowCell, ...]
    signal_usd: float | Absent
    total_printed_usd: float | Absent

    def as_ledger_dict(self) -> dict[str, object]:
        funds: dict[str, object] = {}
        for cell in self.per_fund:
            funds[cell.ticker] = None if isinstance(cell.value_usd, Absent) else cell.value_usd
            if isinstance(cell.value_usd, Absent):
                funds[f"{cell.ticker}__absent"] = cell.value_usd.reason.value
        row: dict[str, object] = {"date": self.trade_date.isoformat(), "funds": funds}
        if isinstance(self.signal_usd, Absent):
            row["signal_usd"] = None
            row["signal_absent"] = self.signal_usd.reason.value
        else:
            row["signal_usd"] = self.signal_usd
        # Recorded for the A.1 Task 1 finding only. Never consumed as a signal.
        if isinstance(self.total_printed_usd, Absent):
            row["source_total_usd"] = None
            row["source_total_absent"] = self.total_printed_usd.reason.value
        else:
            row["source_total_usd"] = self.total_printed_usd
        return row


@dataclass(frozen=True, slots=True)
class Snapshot:
    captured_at: datetime
    url: str
    http_status: int
    sha256: str
    byte_count: int
    body_path: str
    days: tuple[DayRow, ...]


def _month_number(token: str) -> int:
    months = (
        "Jan",
        "Feb",
        "Mar",
        "Apr",
        "May",
        "Jun",
        "Jul",
        "Aug",
        "Sep",
        "Oct",
        "Nov",
        "Dec",
    )
    if token not in months:
        raise FlowTableShape(f"unrecognised month token {token!r}; refusing to guess a date")
    return months.index(token) + 1


def parse_flow_table(markup: str) -> tuple[DayRow, ...]:
    """Parse the served flow table into day rows, reading the registered five funds."""
    rows = largest_table(markup)
    header: list[str] | None = None
    for row in rows:
        if DATE_HEADER in row and all(t in row for t in CONFIG.flow_universe_tickers):
            header = row
            break
    if header is None:
        # The recent page omits the "Date" label and puts tickers on their own
        # row; accept a header row that carries all five registered tickers.
        for row in rows:
            if all(t in row for t in CONFIG.flow_universe_tickers):
                header = row
                break
    if header is None:
        raise FlowTableShape(
            "no header row carrying all five registered tickers "
            f"{CONFIG.flow_universe_tickers}; the served layout changed and the parser refuses "
            "to guess which column is which fund"
        )
    fund_index = {t: header.index(t) for t in CONFIG.flow_universe_tickers}
    total_index = header.index(TOTAL_HEADER) if TOTAL_HEADER in header else None

    days: list[DayRow] = []
    for row in rows:
        if not row:
            continue
        match = DATE_CELL.match(row[0])
        if match is None:
            continue
        widest = max(fund_index.values())
        if len(row) <= widest:
            raise FlowTableShape(
                f"row for {row[0]!r} has {len(row)} cells but the header needs at least "
                f"{widest + 1}; a ragged row is a recorded shape failure, never a padded row"
            )
        trade_date = date(int(match.group(3)), _month_number(match.group(2)), int(match.group(1)))
        cells = tuple(
            FlowCell(ticker=t, value_usd=parse_cell(row[fund_index[t]]))
            for t in CONFIG.flow_universe_tickers
        )
        printed = (
            parse_cell(row[total_index])
            if total_index is not None and len(row) > total_index
            else parse_cell("")
        )
        days.append(
            DayRow(
                trade_date=trade_date,
                per_fund=cells,
                signal_usd=aggregate(cells),
                total_printed_usd=printed,
            )
        )
    if not days:
        raise FlowTableShape(
            "the served table carried no date rows; refusing to record an empty capture"
        )
    return tuple(days)


def capture(
    client: PacedClient,
    *,
    now: datetime,
    url: str = CONFIG.flow_recent_url,
    ledger_path: object = None,
) -> Snapshot:
    """Fetch, seal the raw bytes, parse, and append one fsynced ledger row."""
    response = client.get(url, source="flow", endpoint="flow.table")
    stamp = iso_z(now)
    digest = hashlib.sha256(response.body).hexdigest()
    body_path = SNAPSHOT_BODIES / f"{stamp.replace(':', '')}-{digest[:12]}.html"
    seal_bytes(body_path, response.body)

    if response.status != 200:
        snapshot = Snapshot(
            captured_at=now,
            url=url,
            http_status=response.status,
            sha256=digest,
            byte_count=len(response.body),
            body_path=str(body_path),
            days=(),
        )
        _append(snapshot, state="source_failed", ledger_path=ledger_path)
        return snapshot

    days = parse_flow_table(response.body.decode("utf-8", "replace"))
    snapshot = Snapshot(
        captured_at=now,
        url=url,
        http_status=response.status,
        sha256=digest,
        byte_count=len(response.body),
        body_path=str(body_path),
        days=days,
    )
    _append(snapshot, state="stored", ledger_path=ledger_path)
    return snapshot


def _append(snapshot: Snapshot, *, state: str, ledger_path: object) -> None:
    path = SNAPSHOT_LEDGER if ledger_path is None else ledger_path
    ledger = AppendOnlyLedger(path)  # type: ignore[arg-type]
    ledger.append(
        {
            "captured_at": iso_z(snapshot.captured_at),
            "url": snapshot.url,
            "http_status": snapshot.http_status,
            "state": state,
            "sha256": snapshot.sha256,
            "byte_count": snapshot.byte_count,
            "body_path": snapshot.body_path,
            "row_count": len(snapshot.days),
            "days": [d.as_ledger_dict() for d in snapshot.days],
        }
    )
