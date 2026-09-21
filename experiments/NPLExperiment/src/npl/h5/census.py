"""The H5 instrument resolution and access census (Task 2). No outcome field.

One pass over every HIP-3 dex: enumerate mechanically from `perpDexs` and
per-dex `meta`, apply the registered mapping, then probe each **resolved**
instrument's served state — one `metaAndAssetCtxs` per dex (which carries
every instrument on it), one `fundingHistory` page, one `l2Book`.

What is recorded per instrument is **which fields the venue serves and which
it does not**, the contemporaneous basis where both mark and reference came
from the same snapshot, the funding **service** answer, and the touch state.
No funding rate value is read, no candle is requested, and every write lands
under `data/h5/` through the containment gate.
"""

from __future__ import annotations

from collections import Counter
from collections.abc import Callable, Sequence
from dataclasses import asdict, dataclass
from pathlib import Path

from npl.absence import is_absent
from npl.api import EP_FUNDING_HISTORY, EP_L2_BOOK, EP_META_AND_CTXS, funding_history_body
from npl.blindness import funding_rows
from npl.callstate import CallState
from npl.clock import MS_PER_DAY, iso_z, now_utc, utc_ms
from npl.h5 import basis as h5basis
from npl.h5.calendar import session_tag_of_ms
from npl.h5.gate import Cohorts
from npl.h5.listing import STATUS_CONFLICTING, STATUS_DELISTED, STATUS_LIVE, listing_status
from npl.h5.resolution import Resolution, resolve
from npl.h5.stores import h5_store, read_rows
from npl.paths import H5_CENSUS
from npl.spread import parse_l2_snapshot
from npl.venue import PerpInfo, Venue, parse_meta, parse_perp_dexs

# The service probe looks at the most recent week: the live question is
# whether funding is being served now, not whether an archive once existed.
FUNDING_PROBE_DAYS = 7


@dataclass(frozen=True, slots=True)
class InstrumentRow:
    """One instrument's registered resolution and venue-served state."""

    coin: str
    dex: str
    ticker: str
    resolution_state: str
    resolution_reason: str
    underlying_symbol: str
    underlying_kind: str
    underlying_family: str
    is_delisted: bool
    listing_status: str
    sz_decimals: int
    max_leverage: int
    # --- contemporaneous context ------------------------------------------
    snapshot_id: str
    at_ms: int
    session_tag: str
    ctx_state: str
    served_fields: tuple[str, ...]
    mark_served: bool
    reference_field: str
    reference_served: bool
    basis_bp: float | None
    basis_absence: str
    open_interest: float | None
    day_notional_volume: float | None
    # --- funding service ---------------------------------------------------
    funding_field_served: bool
    funding_history_state: str
    funding_history_rows: int
    funding_first_time_ms: int | None
    funding_last_time_ms: int | None
    # --- touch state -------------------------------------------------------
    l2_state: str
    touch_spread_bp: float | None
    bid_depth5_notional: float | None
    ask_depth5_notional: float | None
    # --- quarantine --------------------------------------------------------
    cohorts: tuple[str, ...]
    quarantined: bool


def _blank_underlying(res: Resolution) -> tuple[str, str, str]:
    if res.underlying is None:
        return "", "", ""
    return res.underlying.symbol, res.underlying.kind, res.underlying.family


def enumerate_hip3(venue: Venue) -> list[tuple[PerpInfo, str]]:
    """Every instrument on every HIP-3 dex, mechanically. A gap is a refusal."""
    dex_list = venue.perp_dexs()
    if dex_list.state is not CallState.STORED or dex_list.body is None:
        raise RuntimeError(f"perpDexs unavailable ({dex_list.state.value}); H5 census refused")
    plan: list[tuple[PerpInfo, str]] = []
    for dex in parse_perp_dexs(dex_list.body):
        per_dex = venue.meta(dex.name)
        if per_dex.state is not CallState.STORED or per_dex.body is None:
            raise RuntimeError(
                f"meta for dex {dex.name} unavailable ({per_dex.state.value}); the H5 "
                f"census refused rather than silently narrowing the universe"
            )
        plan.extend((p, dex.name) for p in parse_meta(per_dex.body))
    return plan


def fetch_contexts(
    venue: Venue, dexs: list[str], snapshot_id: str, at_ms: int
) -> tuple[dict[str, h5basis.AssetContext], dict[str, str]]:
    """One metaAndAssetCtxs per dex. Returns contexts by coin and per-dex states."""
    contexts: dict[str, h5basis.AssetContext] = {}
    states: dict[str, str] = {}
    for dex in dexs:
        outcome = venue.request({"type": "metaAndAssetCtxs", "dex": dex}, EP_META_AND_CTXS)
        states[dex] = outcome.state.value
        if outcome.state is not CallState.STORED or outcome.body is None:
            continue
        for ctx in h5basis.parse_asset_contexts(outcome.body, dex, snapshot_id, at_ms):
            contexts[ctx.coin] = ctx
    return contexts, states


def probe_funding_service(
    venue: Venue, coin: str, now_ms: int
) -> tuple[str, int, int | None, int | None]:
    """Is funding served for this instrument now? Rows and times only, no rate."""
    start = now_ms - FUNDING_PROBE_DAYS * MS_PER_DAY
    outcome = venue.request(funding_history_body(coin, start), EP_FUNDING_HISTORY)
    if outcome.state is not CallState.STORED or outcome.body is None:
        return outcome.state.value, 0, None, None
    rows = funding_rows(outcome.body, entry_ms=None)
    if not rows:
        return CallState.NO_DATA.value, 0, None, None
    return CallState.STORED.value, len(rows), rows[0].time_ms, rows[-1].time_ms


def probe_touch(venue: Venue, coin: str) -> tuple[str, float | None, float | None, float | None]:
    """One l2Book fetch. The touch state is read by the registered l2 reader."""
    outcome = venue.request({"type": "l2Book", "coin": coin}, EP_L2_BOOK)
    if outcome.state is not CallState.STORED or outcome.body is None:
        return outcome.state.value, None, None, None
    try:
        snapshot = parse_l2_snapshot(coin, 0, outcome.body, iso_z(now_utc()))
    except (ValueError, KeyError, IndexError):
        return CallState.NO_DATA.value, None, None, None
    return (
        CallState.STORED.value,
        snapshot.touch_spread_bp,
        snapshot.bid_depth5_notional,
        snapshot.ask_depth5_notional,
    )


def build_row(
    perp: PerpInfo,
    dex: str,
    ctx: h5basis.AssetContext | None,
    ctx_state: str,
    snapshot_id: str,
    at_ms: int,
    cohorts: Cohorts,
    funding_probe: tuple[str, int, int | None, int | None],
    touch: tuple[str, float | None, float | None, float | None],
) -> InstrumentRow:
    """Assemble one census row. Absences are recorded, never filled."""
    res = resolve(perp.name, dex)
    symbol, kind, family = _blank_underlying(res)
    basis_value: float | None = None
    basis_absence = ""
    reference_field = ""
    reference_served = False
    mark_served = False
    served_fields: tuple[str, ...] = ()
    open_interest: float | None = None
    day_volume: float | None = None
    funding_field = False
    if ctx is not None:
        served_fields = ctx.served_fields
        mark_served = not is_absent(ctx.mark)
        reference_served = not is_absent(ctx.reference)
        reference_field = ctx.reference_field or ""
        funding_field = ctx.funding_served
        computed = h5basis.context_basis_bp(ctx)
        if is_absent(computed):
            basis_absence = str(computed).removeprefix("Absent(").removesuffix(")")
        else:
            basis_value = float(computed)
        if not is_absent(ctx.open_interest):
            open_interest = float(ctx.open_interest)
        if not is_absent(ctx.day_notional_volume):
            day_volume = float(ctx.day_notional_volume)
    else:
        basis_absence = "context_unserved"
    claims = cohorts.membership(perp.name)
    funding_state, funding_n, funding_first, funding_last = funding_probe
    l2_state, spread_bp, bid_depth, ask_depth = touch
    return InstrumentRow(
        coin=perp.name,
        dex=dex,
        ticker=res.ticker,
        resolution_state=res.state,
        resolution_reason=res.reason,
        underlying_symbol=symbol,
        underlying_kind=kind,
        underlying_family=family,
        is_delisted=perp.is_delisted,
        listing_status=listing_status(perp.is_delisted, open_interest, day_volume),
        sz_decimals=perp.sz_decimals,
        max_leverage=perp.max_leverage,
        snapshot_id=snapshot_id,
        at_ms=at_ms,
        session_tag=session_tag_of_ms(at_ms),
        ctx_state=ctx_state,
        served_fields=served_fields,
        mark_served=mark_served,
        reference_field=reference_field,
        reference_served=reference_served,
        basis_bp=basis_value,
        basis_absence=basis_absence,
        open_interest=open_interest,
        day_notional_volume=day_volume,
        funding_field_served=funding_field,
        funding_history_state=funding_state,
        funding_history_rows=funding_n,
        funding_first_time_ms=funding_first,
        funding_last_time_ms=funding_last,
        l2_state=l2_state,
        touch_spread_bp=spread_bp,
        bid_depth5_notional=bid_depth,
        ask_depth5_notional=ask_depth,
        cohorts=claims,
        quarantined=bool(claims),
    )


def run_census(
    venue: Venue,
    cohorts: Cohorts,
    ledger_path: Path = H5_CENSUS,
    progress: Callable[[str], None] = lambda _: None,
    probe_live_only: bool = False,
) -> list[InstrumentRow]:
    """One pass. Resolved instruments are probed; the rest are counted.

    `probe_live_only` is the daily collector's setting (Amendment H5-2
    Change 1): a delisted instrument is enumerated, resolved and recorded,
    but its funding and book are not re-probed every day, because it has no
    market to probe. The Task 2 access census runs with it off — probing the
    delisted stratum is how the stratum was measured in the first place.
    """
    at = now_utc()
    at_ms = utc_ms(at)
    snapshot_id = f"h5-census-{iso_z(at)}"
    plan = enumerate_hip3(venue)
    dexs = sorted({dex for _, dex in plan})
    progress(f"enumerated {len(plan)} instruments over {len(dexs)} HIP-3 dexs")
    contexts, ctx_states = fetch_contexts(venue, dexs, snapshot_id, at_ms)
    progress(f"contexts: {len(contexts)} served over {len(dexs)} dexs")

    store = h5_store(ledger_path)
    rows: list[InstrumentRow] = []
    resolved_seen = 0
    for perp, dex in plan:
        res = resolve(perp.name, dex)
        ctx = contexts.get(perp.name)
        status = (
            listing_status(perp.is_delisted, ctx.open_interest, ctx.day_notional_volume)
            if ctx is not None
            else STATUS_CONFLICTING
        )
        if res.is_resolved and (not probe_live_only or status == STATUS_LIVE):
            resolved_seen += 1
            funding_probe = probe_funding_service(venue, perp.name, at_ms)
            touch = probe_touch(venue, perp.name)
            if resolved_seen % 20 == 0:
                progress(f"probed {resolved_seen} resolved instruments (latest {perp.name})")
        else:
            funding_probe = (CallState.EXCLUDED_INELIGIBLE.value, 0, None, None)
            touch = (CallState.EXCLUDED_INELIGIBLE.value, None, None, None)
        row = build_row(
            perp,
            dex,
            ctx,
            ctx_states.get(dex, CallState.SOURCE_FAILED.value),
            snapshot_id,
            at_ms,
            cohorts,
            funding_probe,
            touch,
        )
        store.append(asdict(row))
        rows.append(row)
    return rows


def load_census(path: Path = H5_CENSUS) -> list[InstrumentRow]:
    """The most recent census pass only. Earlier passes stay on disk, unread.

    The store is append-only, so a second pass adds rows rather than
    replacing them; reading the latest `snapshot_id` is how a pass is
    isolated, and a missing store is a loud absence rather than an empty list
    that would read as "no instruments".
    """
    if not path.exists():
        raise FileNotFoundError(
            f"{path} does not exist: the H5 census has not run, which is not the same "
            f"as a census that found nothing."
        )
    rows = read_rows(path)
    if not rows:
        return []
    latest = max(str(r["snapshot_id"]) for r in rows)
    out: list[InstrumentRow] = []
    for raw in rows:
        if str(raw["snapshot_id"]) != latest:
            continue
        fields = dict(raw)
        fields["served_fields"] = tuple(fields.get("served_fields") or ())
        fields["cohorts"] = tuple(fields.get("cohorts") or ())
        out.append(InstrumentRow(**fields))
    return out


def census_summary(rows: Sequence[InstrumentRow]) -> dict[str, object]:
    """One pass reduced to counts. Every split reported with its n.

    The live/delisted split (Amendment H5-2 Change 1) is reported everywhere
    a primary figure appears, because the delisted stratum is descriptive and
    the live stratum is the universe.
    """
    resolved = [r for r in rows if r.resolution_state == "resolved"]
    live = [r for r in resolved if r.listing_status == STATUS_LIVE]
    dead = [r for r in resolved if r.listing_status == STATUS_DELISTED]
    conflicting = [r for r in resolved if r.listing_status == STATUS_CONFLICTING]
    with_reference = [r for r in live if r.reference_served]
    funding_live = [r for r in with_reference if r.funding_history_state == "stored"]
    return {
        "instruments_total": len(rows),
        "by_resolution_state": dict(Counter(r.resolution_state for r in rows)),
        "by_resolution_reason": dict(Counter(r.resolution_reason for r in rows)),
        "by_dex_total": dict(Counter(r.dex for r in rows)),
        "by_dex_resolved": dict(Counter(r.dex for r in resolved)),
        "by_dex_live": dict(Counter(r.dex for r in live)),
        "resolved": len(resolved),
        "resolved_by_kind": dict(Counter(r.underlying_kind for r in resolved)),
        "live": len(live),
        "live_by_kind": dict(Counter(r.underlying_kind for r in live)),
        "excluded_delisted": len(dead),
        "listing_conflicting": len(conflicting),
        "reference_served_resolved": sum(1 for r in resolved if r.reference_served),
        "reference_served_live": len(with_reference),
        "reference_unserved_live": len(live) - len(with_reference),
        "reference_field_used": dict(
            Counter(r.reference_field for r in resolved if r.reference_served)
        ),
        "funding_field_served_resolved": sum(1 for r in resolved if r.funding_field_served),
        "funding_history_states_resolved": dict(Counter(r.funding_history_state for r in resolved)),
        "funding_history_states_live": dict(Counter(r.funding_history_state for r in live)),
        "funding_served_of_live_reference_carrying": len(funding_live),
        "l2_states_resolved": dict(Counter(r.l2_state for r in resolved)),
        "l2_states_live": dict(Counter(r.l2_state for r in live)),
        "served_field_sets_resolved": {
            "|".join(fields): n for fields, n in Counter(r.served_fields for r in resolved).items()
        },
        "quarantined_resolved": sum(1 for r in resolved if r.quarantined),
        "quarantined_live": sum(1 for r in live if r.quarantined),
        "ungated_live": sum(1 for r in live if not r.quarantined),
        "session_tag": rows[0].session_tag if rows else "",
        "snapshot_id": rows[0].snapshot_id if rows else "",
        "at_ms": rows[0].at_ms if rows else 0,
    }
