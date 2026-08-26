"""Build the Form 4 corpus, apply the frozen rule, and fire the CORPUS gate.

One streaming pass over the cached structured data sets accumulates two things:
every insider's look-back trade months, and every candidate transaction that
survives the filters deciding on one transaction alone. Clustering and the
Cohen-Malloy-Pomorski classification run afterward, because both need the whole
stream before either can label anything.

Nothing here reads a return.
"""

from __future__ import annotations

import datetime as dt
import json
import sqlite3
import sys
from collections import Counter, defaultdict
from dataclasses import dataclass

from insider.absence import FLAG_NOT_REPORTED, Absent
from insider.callstate import ATTRITION_ORDER, CallState
from insider.config import CONFIG, Config
from insider.corpus import store
from insider.corpus.classify import (
    code_verdict,
    normalize_roles,
    programmatic_verdict,
    role_verdict,
)
from insider.corpus.cluster import Buy, ClusterReport, find_clusters
from insider.corpus.records import Transaction
from insider.corpus.routine import RoutineClass, TradeHistory, classify
from insider.edgar import bulk
from insider.edgar.client import reachable
from insider.ledger.evidence import record
from insider.market import store as market_store
from insider.paths import REPORTS, ensure_dirs
from insider.portfolio.membership import Event, entry_session_for
from insider.portfolio.membership import build as build_membership
from insider.section0 import fire_corpus_gate


@dataclass
class Funnel:
    """Every transaction is charged to exactly one state and one sub-reason."""

    counts: Counter[tuple[str, str]]

    def charge(self, state: CallState, reason: str, n: int = 1) -> None:
        self.counts[(state.value, reason)] += n

    def total_for(self, state: CallState) -> int:
        return sum(n for (s, _), n in self.counts.items() if s == state.value)

    def grand_total(self) -> int:
        return sum(self.counts.values())


class UniverseIndex:
    """Point-in-time membership. A symbol qualifies at the governing formation."""

    def __init__(self, con: sqlite3.Connection) -> None:
        self.formations = market_store.formation_dates(con)
        self.members = {f: set(market_store.members_at(con, f)) for f in self.formations}
        self.weights = {f: market_store.members_at(con, f) for f in self.formations}

    def governing(self, date: str) -> str | None:
        lo, hi, found = 0, len(self.formations) - 1, None
        while lo <= hi:
            mid = (lo + hi) // 2
            if self.formations[mid] <= date:
                found, lo = self.formations[mid], mid + 1
            else:
                hi = mid - 1
        return found

    def is_member(self, symbol: str, date: str) -> bool:
        formation = self.governing(date)
        return formation is not None and symbol in self.members[formation]


def _flag(raw: str) -> bool | Absent:
    text = (raw or "").strip()
    if text == "":
        return FLAG_NOT_REPORTED
    return text in {"1", "true", "TRUE", "Y"}


def _positive_float(raw: str) -> float | None:
    try:
        value = float(raw)
    except (TypeError, ValueError):
        return None
    return value if value > 0 and value == value and value != float("inf") else None


def scan(cfg: Config = CONFIG) -> tuple[TradeHistory, list[Transaction], Funnel, Counter[str]]:
    """One pass over every cached quarter."""
    history = TradeHistory()
    candidates: list[Transaction] = []
    funnel = Funnel(Counter())
    prefunnel: Counter[str] = Counter()

    for quarter in bulk.quarters(cfg):
        archive = bulk.fetch_quarter(quarter, cfg)

        submissions: dict[str, tuple[dt.date, int, str, bool | Absent]] = {}
        for row in bulk.iter_table(archive, bulk.SUBMISSION):
            accession = row["ACCESSION_NUMBER"]
            doc_type = (row.get("DOCUMENT_TYPE") or "").strip()
            if doc_type != "4":
                prefunnel[f"document_type_{doc_type or 'blank'}"] += 1
                continue
            filed = bulk.parse_dera_date(row.get("FILING_DATE", ""))
            if filed is None:
                prefunnel["submission_unparseable_filing_date"] += 1
                continue
            try:
                issuer_cik = int(row.get("ISSUERCIK") or 0)
            except ValueError:
                issuer_cik = 0
            symbol = (row.get("ISSUERTRADINGSYMBOL") or "").strip().upper()
            submissions[accession] = (filed, issuer_cik, symbol, _flag(row.get("AFF10B5ONE", "")))

        owners: dict[str, list[tuple[int, frozenset[str]]]] = defaultdict(list)
        for row in bulk.iter_table(archive, bulk.REPORTING_OWNER):
            try:
                cik = int(row.get("RPTOWNERCIK") or 0)
            except ValueError:
                continue
            if cik:
                owners[row["ACCESSION_NUMBER"]].append(
                    (cik, normalize_roles(row.get("RPTOWNER_RELATIONSHIP", "")))
                )

        for row in bulk.iter_table(archive, bulk.NONDERIV_TRANS):
            accession = row["ACCESSION_NUMBER"]
            submission = submissions.get(accession)
            if submission is None:
                continue
            if (row.get("TRANS_FORM_TYPE") or "").strip() != "4":
                prefunnel["transaction_on_form_5"] += 1
                continue

            filed, issuer_cik, symbol, flag = submission
            code = (row.get("TRANS_CODE") or "").strip().upper()
            when = bulk.parse_dera_date(row.get("TRANS_DATE", ""))
            shares = _positive_float(row.get("TRANS_SHARES", ""))
            price = _positive_float(row.get("TRANS_PRICEPERSHARE", ""))
            acquired = (row.get("TRANS_ACQUIRED_DISP_CD") or "").strip().upper()
            filers = owners.get(accession, [])

            # The look-back history takes every discretionary open-market trade
            # by every reporting owner, at every issuer, universe or not.
            if code in cfg.lookback_trade_codes and when is not None:
                for cik, _ in filers:
                    history.add(cik, when)

            in_span = cfg.event_span_start <= filed.isoformat() <= cfg.event_span_end
            if not in_span:
                continue

            if when is None or not code or not filers:
                funnel.charge(CallState.UNPARSEABLE, "missing_date_code_or_filer")
                continue
            if when > filed:
                funnel.charge(CallState.UNPARSEABLE, "transaction_after_filing")
                continue
            if code in cfg.allowed_transaction_codes and (
                shares is None or price is None or acquired != "A"
            ):
                funnel.charge(CallState.UNPARSEABLE, "purchase_missing_shares_price_or_acq")
                continue
            if shares is None or price is None:
                funnel.charge(CallState.FILTERED_CODE, f"code_{code}")
                continue

            # The event's filer identity is the lowest reporting-owner CIK, so a
            # joint filing counts as one filer and cannot manufacture a cluster
            # on its own. Roles are checked across every owner on the filing.
            primary = min(cik for cik, _ in filers)
            roles: frozenset[str] = frozenset().union(*(r for _, r in filers))
            if len(filers) > 1:
                prefunnel["multi_owner_filing_transaction"] += 1

            txn = Transaction(
                accession=accession,
                issuer_cik=issuer_cik,
                symbol=symbol,
                filer_cik=primary,
                roles=roles,
                transaction_date=when,
                filing_date=filed,
                code=code,
                shares=shares,
                price_per_share=price,
                aff10b5one=flag,
            )

            # Registered funnel order: code, role, universe, programmatic.
            for check in (code_verdict, role_verdict):
                verdict = check(txn, cfg)
                if verdict is not None:
                    funnel.charge(verdict.state, verdict.reason)
                    break
            else:
                if not _in_universe(txn):
                    funnel.charge(CallState.OUTSIDE_UNIVERSE, "not_a_member_at_entry")
                    continue
                verdict = programmatic_verdict(txn, cfg)
                if verdict is not None:
                    funnel.charge(verdict.state, verdict.reason)
                    continue
                candidates.append(txn)

    return history, candidates, funnel, prefunnel


_UNIVERSE: UniverseIndex | None = None
_SESSIONS: list[str] = []


def _in_universe(txn: Transaction) -> bool:
    assert _UNIVERSE is not None
    entry = entry_session_for(_SESSIONS, txn.filing_date.isoformat())
    return entry is not None and _UNIVERSE.is_member(txn.symbol, entry)


def _record_refusals(
    ccon: sqlite3.Connection,
    clusters: object,
    candidates: list[Transaction],
    history: TradeHistory,
    cfg: Config,
) -> None:
    """Write the refusals this run actually produced, with the evidence attached.

    A refusal asserted in prose is a claim. A refusal serialized from the run
    that produced it is a fact, and these are the two the stage brief names.
    """
    assert isinstance(clusters, ClusterReport)
    rejected = [c for c in clusters.clusters if c.rejected]
    rejected.sort(key=lambda c: (-c.size, c.symbol, c.window_start))
    for ordinal, cluster in enumerate(rejected[:5]):
        members = [candidates[i] for i in cluster.member_indexes]
        store.write_refusal(
            ccon,
            "johnsen_rejected_cluster",
            ordinal,
            json.dumps(
                {
                    "symbol": cluster.symbol,
                    "window": [cluster.window_start.isoformat(), cluster.window_end.isoformat()],
                    "size": cluster.size,
                    "distinct_filers": cluster.distinct_filers,
                    "modal_date_price_fraction": round(cluster.modal_date_price_fraction, 4),
                    "threshold": cfg.johnsen_same_date_price_fraction,
                    "buys": [
                        {
                            "filer_cik": m.filer_cik,
                            "transaction_date": m.transaction_date.isoformat(),
                            "price_per_share": m.price_per_share,
                            "shares": m.shares,
                            "value_usd": round(m.value_usd, 2),
                        }
                        for m in members
                    ],
                },
                indent=2,
            ),
        )

    shown = 0
    for txn in candidates:
        if shown >= 5:
            break
        if classify(history, txn.filer_cik, txn.transaction_date, cfg) is not (
            RoutineClass.INSUFFICIENT_HISTORY
        ):
            continue
        first = history.first_trade.get(txn.filer_cik)
        store.write_refusal(
            ccon,
            "insider_unclassifiable_for_want_of_history",
            shown,
            json.dumps(
                {
                    "filer_cik": txn.filer_cik,
                    "symbol": txn.symbol,
                    "transaction_date": txn.transaction_date.isoformat(),
                    "first_observed_trade": first.isoformat() if first else None,
                    "years_of_history_required": cfg.min_history_years,
                    "years_of_history_observed": (
                        round((txn.transaction_date - first).days / 365.25, 2) if first else 0.0
                    ),
                    "look_back_window_opens": cfg.lookback_start,
                    "months_traded_observed": len(history.months_traded.get(txn.filer_cik, ())),
                },
                indent=2,
            ),
        )
        shown += 1


def main() -> int:
    global _UNIVERSE, _SESSIONS
    ensure_dirs()
    cfg = CONFIG

    print("checking EDGAR reachability")
    edgar_up = reachable(cfg)
    print(f"  EDGAR reachable: {edgar_up}")
    if not edgar_up:
        gate = fire_corpus_gate(
            edgar_reachable=False, qualifying_events=0, session_coverage=0.0, cfg=cfg
        )
        record("corpus_gate", verdict=gate.verdict.value, rationale=gate.rationale)
        print(f"{gate.verdict.value}: {gate.rationale}")
        return 1

    with market_store.connect() as mcon:
        _SESSIONS = market_store.sessions(mcon)
        _UNIVERSE = UniverseIndex(mcon)
    print(f"  sessions {len(_SESSIONS)}, formations {len(_UNIVERSE.formations)}")

    print(f"scanning {len(bulk.quarters(cfg))} quarters")
    history, candidates, funnel, prefunnel = scan(cfg)
    print(f"  insiders with look-back history: {history.insiders()}")
    print(f"  candidates surviving the per-transaction filters: {len(candidates)}")

    print("clustering")
    buys = [
        Buy(
            index=i,
            symbol=t.symbol,
            filer_cik=t.filer_cik,
            transaction_date=t.transaction_date,
            price_per_share=t.price_per_share,
        )
        for i, t in enumerate(candidates)
    ]
    clusters = find_clusters(buys, cfg)
    print(f"  clusters found {len(clusters.clusters)}")
    print(f"  rejected by the Johnsen filter {sum(1 for c in clusters.clusters if c.rejected)}")

    print("classifying and joining to bars")
    with market_store.connect() as mcon:
        mcon.execute("CREATE TEMP TABLE want(symbol TEXT, date TEXT)")
        wanted: list[tuple[str, str]] = []
        entries: list[str | None] = []
        for txn in candidates:
            entry = entry_session_for(_SESSIONS, txn.filing_date.isoformat())
            entries.append(entry)
            if entry is not None:
                wanted.append((txn.symbol, entry))
        mcon.executemany("INSERT INTO want(symbol, date) VALUES (?,?)", wanted)
        have = {
            (r[0], r[1])
            for r in mcon.execute(
                "SELECT b.symbol, b.date FROM bar b JOIN want w "
                "ON b.symbol = w.symbol AND b.date = w.date"
            )
        }
    print(
        f"  distinct entry (symbol, session) pairs present {len(have)} of {len(set(wanted))} wanted"
    )

    rows: list[tuple[object, ...]] = []
    lags: Counter[int] = Counter()
    routine_counts: Counter[str] = Counter()
    unclassifiable_first_year: Counter[str] = Counter()
    flag_absent = 0

    for i, txn in enumerate(candidates):
        if i in clusters.johnsen_rejected_only:
            funnel.charge(CallState.FILTERED_PROGRAMMATIC, "johnsen_same_date_price")
            continue
        in_cluster = i in clusters.in_surviving_cluster
        label = classify(history, txn.filer_cik, txn.transaction_date, cfg)
        routine_counts[label.value] += 1
        if not in_cluster and label is not RoutineClass.OPPORTUNISTIC:
            funnel.charge(CallState.FILTERED_ROUTINE, label.value)
            if label is RoutineClass.INSUFFICIENT_HISTORY:
                unclassifiable_first_year[txn.transaction_date.strftime("%Y")] += 1
            continue
        entry = entries[i]
        if entry is None or (txn.symbol, entry) not in have:
            funnel.charge(CallState.NO_BAR, "no_bar_on_entry_session")
            continue

        funnel.charge(CallState.PARSED, "qualifying")
        lags[txn.filing_lag_days] += 1
        if isinstance(txn.aff10b5one, Absent):
            flag_absent += 1
        rows.append(
            (
                txn.accession,
                txn.filer_cik,
                txn.issuer_cik,
                txn.symbol,
                txn.transaction_date.isoformat(),
                txn.filing_date.isoformat(),
                entry,
                txn.value_usd,
                label.value,
                int(in_cluster),
                int(not isinstance(txn.aff10b5one, Absent)),
            )
        )

    with store.connect() as ccon:
        store.reset(ccon)
        written = store.write_events(ccon, rows)
        stored = store.event_count(ccon)
        if stored != written:
            raise RuntimeError(
                f"offered {written} events and the store holds {stored}. "
                f"A silent collapse is a fabricated count."
            )
        store.write_clusters(
            ccon,
            [
                (
                    i,
                    c.symbol,
                    c.window_start.isoformat(),
                    c.window_end.isoformat(),
                    c.size,
                    c.distinct_filers,
                    c.modal_date_price_fraction,
                    int(c.rejected),
                )
                for i, c in enumerate(clusters.clusters)
            ],
        )
        _record_refusals(ccon, clusters, candidates, history, cfg)
        store.write_attrition(ccon, dict(funnel.counts))
        store.write_lags(ccon, dict(lags))
        for key, value in (
            ("qualifying_events", str(written)),
            ("insiders_with_history", str(history.insiders())),
            ("flag_absent_events", str(flag_absent)),
            ("clusters_found", str(len(clusters.clusters))),
            ("clusters_rejected", str(sum(1 for c in clusters.clusters if c.rejected))),
        ):
            store.set_meta(ccon, key, value)
        per_year = store.events_per_year(ccon)
        event_pairs = store.events(ccon)

    series = build_membership(
        [Event(symbol=s, entry_session=e) for s, e in event_pairs],
        _SESSIONS,
        cfg.primary_hold_sessions,
    )
    coverage = series.coverage()
    gate = fire_corpus_gate(
        edgar_reachable=True,
        qualifying_events=written,
        session_coverage=coverage,
        cfg=cfg,
    )

    payload = {
        "qualifying_events": written,
        "events_per_year": per_year,
        "attrition": {f"{s}/{r}": n for (s, r), n in sorted(funnel.counts.items())},
        "prefunnel": dict(sorted(prefunnel.items())),
        "routine_labels": dict(routine_counts),
        "unclassifiable_by_year": dict(sorted(unclassifiable_first_year.items())),
        "lag_distribution": dict(sorted(lags.items())),
        "flag_absent_events": flag_absent,
        "insiders_with_history": history.insiders(),
        "clusters_found": len(clusters.clusters),
        "clusters_rejected": sum(1 for c in clusters.clusters if c.rejected),
        "session_coverage": coverage,
        "mean_book_width": series.mean_width(),
        "verdict": gate.verdict.value,
        "rationale": gate.rationale,
    }
    record("corpus_gate", **payload)
    out = REPORTS / "stage_a1"
    out.mkdir(parents=True, exist_ok=True)
    (out / "corpus.json").write_text(json.dumps(payload, indent=2), encoding="utf-8")

    print()
    print("attrition funnel")
    for state in ATTRITION_ORDER:
        total = funnel.total_for(state)
        print(f"  {state.value:<24} {total:>9,}")
        for (s, reason), n in sorted(funnel.counts.items()):
            if s == state.value:
                print(f"      {reason:<38} {n:>9,}")
    print()
    print(f"qualifying events {written:,}")
    print(f"session coverage  {coverage:.1%}")
    print(f"mean book width   {series.mean_width():.1f}")
    print()
    print(f"{gate.verdict.value}: {gate.rationale}")
    return 0 if gate.verdict.value == "CORPUS-GO" else 1


if __name__ == "__main__":
    sys.exit(main())
