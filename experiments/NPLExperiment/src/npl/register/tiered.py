"""The tiered control rule (Amendment H2-5 section 2), replacing the H2-3 fallback.

Three tiers, consulted in order; the first that yields a candidate wins:

    tier 1  same dex, exact class
    tier 2  any dex,  exact class
    tier 3  any dex,  within the equity complex — equity-complex legs only

**Cross-complex is refused at every tier**, structurally by the tier filters
and again by `assert_coherent` on the selected elder, so deleting either
refusal is caught. Within the selected tier the registered Section 6
selection is unchanged: listed at least 180 days before the entry, funding
coverage at or above the bar, nearest by signed trailing 168-hour mean hourly
funding, with replacement, ties to the earlier listing then coin ascending.

Two things this module will not do:

- **read a row stamped after the event entry.** Every trailing mean goes
  through `npl.controls.trailing_mean`, which raises
  `npl.controls.PostEntryRead`; the refusal is produced through the tiered
  path by test, never asserted in a comment.
- **write into the superseded ledger.** `data/controls/h2_pairs.jsonl` is the
  H2-3 record, retained byte-identical. `assert_not_superseded` refuses any
  assignment target that resolves to it.
"""

from __future__ import annotations

from collections.abc import Callable, Sequence
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Final

from npl.blindness import FundingRow
from npl.clock import iso_z, now_utc
from npl.config import CONFIG, Config
from npl.controls import event_trailing_mean, nearest_by_funding
from npl.ledger.append_only import AppendOnlyLedger
from npl.paths import H2_PAIRS_LEDGER, H2_PAIRS_V2_LEDGER
from npl.register.assetclass import (
    asset_class,
    class_pair,
    in_equity_complex,
    unclassifiable_reason,
)
from npl.tier import (
    REGISTERED_TIERS,
    TIER_ANY_DEX_EQUITY_COMPLEX,
    TIER_ANY_DEX_EXACT_CLASS,
    TIER_SAME_DEX_EXACT_CLASS,
)

STATE_ASSIGNED: Final = "assigned"
STATE_UNCLASSIFIABLE: Final = "excluded_unclassifiable"
STATE_NO_CLASS_ELDER: Final = "excluded_no_class_elder"


class CrossComplexControl(RuntimeError):
    """A selected elder sits outside the event's complex. Refused loudly."""


class SupersededLedgerWrite(RuntimeError):
    """An assignment tried to write into the superseded H2-3 pairs ledger."""


@dataclass(frozen=True, slots=True)
class CandidateRef:
    """One admissible elder at census level: identity, dex, class, listing date.

    Deliberately carries **no funding rows**. Tier membership is decided from
    these four fields alone, so the trailing windows of a tier nobody reaches
    are never fetched — and a fetch is a charge against the daily cap.
    """

    coin: str
    dex: str
    asset_class: str
    listing_open_ms: int


@dataclass(frozen=True, slots=True)
class ClassedCandidate:
    """A `CandidateRef` with its trailing window materialised.

    Satisfies `npl.controls.CandidateLike` structurally, so the registered
    distance, tie-break, and coverage rules run over it unchanged.
    """

    coin: str
    dex: str
    asset_class: str
    listing_open_ms: int
    rows: tuple[FundingRow, ...]


type RowProvider = Callable[[CandidateRef], tuple[FundingRow, ...]]


def rows_from(mapping: dict[str, tuple[FundingRow, ...]]) -> RowProvider:
    """A provider backed by an in-memory map. Used by tests and by replays."""
    return lambda ref: mapping.get(ref.coin, ())


def materialise(ref: CandidateRef, rows_for: RowProvider) -> ClassedCandidate:
    """Fetch (or look up) one candidate's trailing window. One call per elder."""
    return ClassedCandidate(
        coin=ref.coin,
        dex=ref.dex,
        asset_class=ref.asset_class,
        listing_open_ms=ref.listing_open_ms,
        rows=rows_for(ref),
    )


@dataclass(frozen=True, slots=True)
class TieredAssignment:
    """One tiered pair row. Written at assignment time, append-only."""

    event_coin: str
    control_coin: str
    dex: str
    control_dex: str
    entry_ms: int
    tier: int
    event_class: str
    control_class: str
    class_pair: str
    event_trailing_mean: float
    control_trailing_mean: float
    funding_distance: float
    candidates_considered: int
    candidates_skipped_low_coverage: int
    tier_pool_sizes: tuple[int, int, int]
    assigned_at: str
    state: str = STATE_ASSIGNED


@dataclass(frozen=True, slots=True)
class TieredExclusion:
    """One event that forms no pair, with the reason that refused it."""

    event_coin: str
    dex: str
    entry_ms: int
    state: str
    reason: str
    event_class: str | None
    tier_pool_sizes: tuple[int, int, int]
    assigned_at: str


def assert_not_superseded(path: Path) -> Path:
    """Refuse any assignment target that resolves to the H2-3 pairs ledger."""
    resolved = (path if path.is_absolute() else Path.cwd() / path).resolve()
    if resolved == H2_PAIRS_LEDGER.resolve():
        raise SupersededLedgerWrite(
            f"refusing to write into {resolved}: it is the superseded Amendment H2-3 "
            f"assignment, retained byte-identical. The tiered assignment is "
            f"{H2_PAIRS_V2_LEDGER}."
        )
    return resolved


def assert_coherent(event_class: str, control_class: str, tier: int) -> None:
    """The registered refusal: no tier admits an elder outside the complex.

    Tiers 1 and 2 require the exact class; tier 3 requires both legs inside
    the equity complex and is unavailable to any other leg. Checked on the
    selected elder as well as in the tier filters, so deleting either is caught.
    """
    if tier in (TIER_SAME_DEX_EXACT_CLASS, TIER_ANY_DEX_EXACT_CLASS):
        if control_class != event_class:
            raise CrossComplexControl(
                f"tier {tier} selected a {control_class!r} elder for an {event_class!r} event; "
                f"tiers 1 and 2 admit the exact class only"
            )
        return
    if tier == TIER_ANY_DEX_EQUITY_COMPLEX:
        if not (in_equity_complex(event_class) and in_equity_complex(control_class)):
            raise CrossComplexControl(
                f"tier 3 selected a {control_class!r} elder for an {event_class!r} event; "
                f"tier 3 admits equity-complex legs against equity-complex elders only"
            )
        return
    raise CrossComplexControl(f"tier {tier} is not a registered tier {REGISTERED_TIERS}")


def tier_pool(
    tier: int, event_dex: str, event_class: str, candidates: Sequence[CandidateRef]
) -> list[CandidateRef]:
    """The candidate set a tier admits. Cross-complex never survives a filter."""
    if tier == TIER_SAME_DEX_EXACT_CLASS:
        return [c for c in candidates if c.dex == event_dex and c.asset_class == event_class]
    if tier == TIER_ANY_DEX_EXACT_CLASS:
        return [c for c in candidates if c.asset_class == event_class]
    if tier == TIER_ANY_DEX_EQUITY_COMPLEX:
        if not in_equity_complex(event_class):
            return []
        return [c for c in candidates if in_equity_complex(c.asset_class)]
    raise CrossComplexControl(f"tier {tier} is not a registered tier {REGISTERED_TIERS}")


def assign_control_tiered(
    event_coin: str,
    dex: str,
    entry_ms: int,
    event_rows: tuple[FundingRow, ...],
    candidates: Sequence[CandidateRef],
    rows_for: RowProvider,
    cfg: Config = CONFIG,
    pairs_path: Path = H2_PAIRS_V2_LEDGER,
    append: bool = True,
) -> TieredAssignment | TieredExclusion:
    """Assign one event's control under the tiered rule, or record its refusal.

    `candidates` are the elders already admitted by the registered date
    conditions (aged 180 days, still serving). The coverage condition is
    enforced here, from funding row timestamps, by `trailing_mean`.

    `rows_for` materialises one candidate's trailing window and is called
    **only for the tiers actually consulted**, so a lower tier costs nothing
    when a higher one resolves. Each elder is materialised at most once per
    event.
    """
    assert_not_superseded(pairs_path)
    at = iso_z(now_utc())
    event_class = asset_class(event_coin, dex)
    if event_class is None:
        return TieredExclusion(
            event_coin=event_coin,
            dex=dex,
            entry_ms=entry_ms,
            state=STATE_UNCLASSIFIABLE,
            reason=unclassifiable_reason(event_coin, dex),
            event_class=None,
            tier_pool_sizes=(0, 0, 0),
            assigned_at=at,
        )

    pools = tuple(len(tier_pool(t, dex, event_class, candidates)) for t in REGISTERED_TIERS)
    sizes: tuple[int, int, int] = (pools[0], pools[1], pools[2])

    event_mean = event_trailing_mean(event_rows, entry_ms, cfg)
    if not isinstance(event_mean, float):
        return TieredExclusion(
            event_coin=event_coin,
            dex=dex,
            entry_ms=entry_ms,
            state=STATE_NO_CLASS_ELDER,
            reason=f"event_trailing_mean_absent_{event_mean.reason.value}",
            event_class=event_class,
            tier_pool_sizes=sizes,
            assigned_at=at,
        )

    # The tier pools nest — tier 1 is a subset of tier 2, and both of tier 3
    # for an equity-complex leg — so the counts are over DISTINCT coins. A
    # bare counter would report one candidate two or three times.
    considered_coins: set[str] = set()
    skipped_coins: set[str] = set()
    materialised: dict[str, ClassedCandidate] = {}
    for tier in REGISTERED_TIERS:
        pool = tier_pool(tier, dex, event_class, candidates)
        if not pool:
            continue
        # The registered distance, tie-break, and coverage rules verbatim:
        # ClassedCandidate satisfies `CandidateLike` structurally.
        for ref in pool:
            if ref.coin not in materialised:
                materialised[ref.coin] = materialise(ref, rows_for)
        selection = nearest_by_funding(
            [materialised[ref.coin] for ref in pool], entry_ms, event_mean, cfg
        )
        considered_coins.update(selection.considered)
        skipped_coins.update(selection.skipped)
        best = selection.best
        if best is None:
            continue
        elder = materialised[best[2]]
        assert_coherent(event_class, elder.asset_class, tier)
        assignment = TieredAssignment(
            event_coin=event_coin,
            control_coin=elder.coin,
            dex=dex,
            control_dex=elder.dex,
            entry_ms=entry_ms,
            tier=tier,
            event_class=event_class,
            control_class=elder.asset_class,
            class_pair=class_pair(event_class, elder.asset_class),
            event_trailing_mean=event_mean,
            control_trailing_mean=best[3],
            funding_distance=abs(best[3] - event_mean),
            candidates_considered=len(considered_coins),
            candidates_skipped_low_coverage=len(skipped_coins),
            tier_pool_sizes=sizes,
            assigned_at=at,
        )
        if append:
            AppendOnlyLedger(assert_not_superseded(pairs_path)).append(asdict(assignment))
        return assignment

    return TieredExclusion(
        event_coin=event_coin,
        dex=dex,
        entry_ms=entry_ms,
        state=STATE_NO_CLASS_ELDER,
        reason=(
            f"no admissible {event_class!r} elder at any available tier "
            f"(pools {sizes}, {len(considered_coins)} considered, "
            f"{len(skipped_coins)} under the coverage bar)"
        ),
        event_class=event_class,
        tier_pool_sizes=sizes,
        assigned_at=at,
    )


def tier_of_row(row: dict[str, object]) -> int:
    """The tier of one v2 ledger row. An unregistered tier is a loud refusal."""
    tier = row.get("tier")
    if tier not in REGISTERED_TIERS:
        raise ValueError(
            f"unregistered tier {tier!r} on pair row {row.get('event_coin')!r}; "
            f"the registered tiers are {REGISTERED_TIERS}"
        )
    return int(str(tier))


def class_pair_of_row(row: dict[str, object]) -> str:
    """The class pair of one v2 ledger row. Never imputed when absent."""
    if "class_pair" not in row:
        raise ValueError(
            f"pair row {row.get('event_coin')!r} carries no class_pair; every row written "
            f"under Amendment H2-5 carries one and an absent field is a defect"
        )
    return str(row["class_pair"])


REGISTERED_STATES: Final[tuple[str, str, str]] = (
    STATE_ASSIGNED,
    STATE_UNCLASSIFIABLE,
    STATE_NO_CLASS_ELDER,
)


def assigned_rows(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    """The pair rows of a v2 ledger. Exclusion rows are not pairs.

    The v2 ledger records what happened to **every** event, so a consumer
    that wants pairs must say so. An unregistered state is a loud refusal,
    never a silently dropped row.
    """
    out: list[dict[str, object]] = []
    for row in rows:
        state = row.get("state")
        if state not in REGISTERED_STATES:
            raise ValueError(
                f"unregistered state {state!r} on pair row {row.get('event_coin')!r}; "
                f"the registered states are {REGISTERED_STATES}"
            )
        if state == STATE_ASSIGNED:
            out.append(row)
    return out


def control_dex_of_row(row: dict[str, object]) -> str:
    """The elder leg's own dex. Every v2 row carries one; an absence is a defect."""
    if "control_dex" not in row:
        raise ValueError(
            f"pair row {row.get('event_coin')!r} carries no control_dex; every row written "
            f"under Amendment H2-5 carries one and an absent field is a defect"
        )
    return str(row["control_dex"])
