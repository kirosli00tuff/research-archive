"""The historical listing census. Blind by construction.

Enumerates every perp on the main dex and every HIP-3 dex, and for each
records the first served 1d candle timestamp as the inferred listing date —
parsing the t field, the T field, and the row count only, through
npl.blindness. Rows land in an append-only ledger. No price or volume field
exists on this path.
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import asdict, dataclass
from datetime import datetime
from pathlib import Path

from npl.blindness import candle_times, funding_rows
from npl.callstate import CallState
from npl.clock import MS_PER_DAY, iso_z, now_utc, utc_ms
from npl.ledger.append_only import AppendOnlyLedger
from npl.paths import CENSUS_LEDGER
from npl.venue import PerpInfo, Venue

EVENT_VANILLA = "vanilla"
EVENT_HYPERP_CONVERSION = "hyperp_conversion"
EVENT_HIP3 = "hip3"


@dataclass(frozen=True, slots=True)
class CensusRow:
    """One instrument's census record. Timestamps and counts only."""

    coin: str
    dex: str
    event_type: str
    hyperp_source: str
    is_delisted: bool
    sz_decimals: int
    max_leverage: int
    state: str
    first_1d_open_ms: int | None
    last_1d_close_ms: int | None
    candle_rows: int
    # Amendment 1: the first archived funding row, the listing cross-check.
    funding_state: str
    first_funding_time_ms: int | None
    funding_page_rows: int
    recorded_at: str


def event_type_of(coin: str, dex: str, hyperp_documented: dict[str, str]) -> tuple[str, str]:
    """The registered tag rule: hip3 by dex, hyperp by documentation, else vanilla."""
    if dex:
        return EVENT_HIP3, ""
    if coin in hyperp_documented:
        return EVENT_HYPERP_CONVERSION, hyperp_documented[coin]
    return EVENT_VANILLA, ""


def census_instrument(
    venue: Venue,
    perp: PerpInfo,
    dex: str,
    hyperp_documented: dict[str, str],
    now: datetime | None = None,
) -> CensusRow:
    """Fetch one instrument's full 1d span and reduce it to times and count."""
    at = now or now_utc()
    end_ms = utc_ms(at) + MS_PER_DAY
    event_type, hyperp_source = event_type_of(perp.name, dex, hyperp_documented)
    outcome = venue.candles(perp.name, "1d", 0, end_ms)
    first_open: int | None = None
    last_close: int | None = None
    rows = 0
    if outcome.state is CallState.STORED and outcome.body is not None:
        times = candle_times(outcome.body)
        rows = times.row_count
        if rows > 0:
            first_open = times.open_ms[0]
            last_close = times.close_ms[-1]
            state = CallState.STORED
        else:
            state = CallState.NO_DATA
    else:
        state = outcome.state

    funding_outcome = venue.funding(perp.name, 0)
    first_funding: int | None = None
    funding_page_rows = 0
    if funding_outcome.state is CallState.STORED and funding_outcome.body is not None:
        frows = funding_rows(funding_outcome.body, entry_ms=None)
        funding_page_rows = len(frows)
        if frows:
            first_funding = frows[0].time_ms
            funding_state = CallState.STORED
        else:
            funding_state = CallState.NO_DATA
    else:
        funding_state = funding_outcome.state
    return CensusRow(
        coin=perp.name,
        dex=dex,
        event_type=event_type,
        hyperp_source=hyperp_source,
        is_delisted=perp.is_delisted,
        sz_decimals=perp.sz_decimals,
        max_leverage=perp.max_leverage,
        state=state.value,
        first_1d_open_ms=first_open,
        last_1d_close_ms=last_close,
        candle_rows=rows,
        funding_state=funding_state.value,
        first_funding_time_ms=first_funding,
        funding_page_rows=funding_page_rows,
        recorded_at=iso_z(at),
    )


class CensusLedger:
    """Append-only census store. One row per instrument per census pass."""

    def __init__(self, path: Path = CENSUS_LEDGER) -> None:
        self._ledger = AppendOnlyLedger(path)

    def append(self, row: CensusRow) -> None:
        self._ledger.append(asdict(row))

    def rows(self) -> list[CensusRow]:
        out: list[CensusRow] = []
        for raw in self._ledger.require_intact():
            out.append(
                CensusRow(
                    coin=str(raw["coin"]),
                    dex=str(raw["dex"]),
                    event_type=str(raw["event_type"]),
                    hyperp_source=str(raw.get("hyperp_source", "")),
                    is_delisted=bool(raw["is_delisted"]),
                    sz_decimals=int(raw["sz_decimals"]),
                    max_leverage=int(raw["max_leverage"]),
                    state=str(raw["state"]),
                    first_1d_open_ms=(
                        int(raw["first_1d_open_ms"])
                        if raw["first_1d_open_ms"] is not None
                        else None
                    ),
                    last_1d_close_ms=(
                        int(raw["last_1d_close_ms"])
                        if raw["last_1d_close_ms"] is not None
                        else None
                    ),
                    candle_rows=int(raw["candle_rows"]),
                    funding_state=str(raw["funding_state"]),
                    first_funding_time_ms=(
                        int(raw["first_funding_time_ms"])
                        if raw["first_funding_time_ms"] is not None
                        else None
                    ),
                    funding_page_rows=int(raw["funding_page_rows"]),
                    recorded_at=str(raw["recorded_at"]),
                )
            )
        return out


def quarter_of_ms(ms: int) -> str:
    from npl.clock import ms_to_utc

    moment = ms_to_utc(ms)
    quarter = (moment.month - 1) // 3 + 1
    return f"{moment.year}Q{quarter}"


def listings_per_quarter(rows: list[CensusRow]) -> dict[str, dict[str, int]]:
    """Quarter -> event_type -> count, over rows with an inferred listing date."""
    out: dict[str, dict[str, int]] = {}
    for row in rows:
        if row.first_1d_open_ms is None:
            continue
        quarter = quarter_of_ms(row.first_1d_open_ms)
        bucket = out.setdefault(quarter, {})
        bucket[row.event_type] = bucket.get(row.event_type, 0) + 1
    return out


def trailing_rate_per_quarter(
    rows: list[CensusRow], now_ms: int, quarters: int = 2
) -> dict[str, float]:
    """Listings per quarter over the trailing N quarters (91-day quarters), by type."""
    window_ms = quarters * 91 * MS_PER_DAY
    counts: dict[str, int] = {}
    for row in rows:
        if row.first_1d_open_ms is None:
            continue
        if row.first_1d_open_ms >= now_ms - window_ms:
            counts[row.event_type] = counts.get(row.event_type, 0) + 1
    return {etype: n / quarters for etype, n in counts.items()}


def run_census(
    venue: Venue,
    hyperp_documented: dict[str, str],
    ledger: CensusLedger | None = None,
    progress: Callable[[str], None] = lambda _: None,
) -> list[CensusRow]:
    """Enumerate main dex and every HIP-3 dex, census each instrument, append rows."""
    from npl.venue import parse_meta, parse_perp_dexs

    store = ledger or CensusLedger()
    rows: list[CensusRow] = []

    main = venue.meta()
    if main.state is not CallState.STORED or main.body is None:
        raise RuntimeError(f"main-dex meta unavailable ({main.state.value}); census refused")
    dex_list = venue.perp_dexs()
    if dex_list.state is not CallState.STORED or dex_list.body is None:
        raise RuntimeError(f"perpDexs unavailable ({dex_list.state.value}); census refused")

    plan: list[tuple[PerpInfo, str]] = [(p, "") for p in parse_meta(main.body)]
    for dex in parse_perp_dexs(dex_list.body):
        per_dex = venue.meta(dex.name)
        if per_dex.state is not CallState.STORED or per_dex.body is None:
            raise RuntimeError(
                f"meta for dex {dex.name} unavailable ({per_dex.state.value}); census refused "
                f"rather than silently narrowing the universe"
            )
        plan.extend((p, dex.name) for p in parse_meta(per_dex.body))

    for i, (perp, dex_name) in enumerate(plan):
        row = census_instrument(venue, perp, dex_name, hyperp_documented)
        store.append(row)
        rows.append(row)
        if i % 25 == 0:
            progress(f"census {i + 1}/{len(plan)}: {perp.name} [{row.state}]")
    return rows
