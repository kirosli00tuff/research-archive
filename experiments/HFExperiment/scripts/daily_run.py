#!/usr/bin/env python
"""The 23:30 UTC daily run. Collect fresh, accrue, verdict, render.

The systemd timer hfexperiment-bars.timer calls this Mon to Fri at
23:30 UTC, after the US close, staggered from AiTrader's 22:30 so two
collectors never share a rate window. Re-runs are idempotent: computed
days are never recomputed, exclusions are retried, the verdict engine
appends only on new information.

Without credentials the run fails loudly with BLOCKED-ON-OPERATOR and
exit code 2. With --render-only it renders both monitor views from
local state and touches no network, which is the pre-start state the
stage evidence records.
"""
from __future__ import annotations

import datetime
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

from hfexperiment import universe  # noqa: E402
from hfexperiment.accrual import (  # noqa: E402
    WIDTHS,
    Ledgers,
    benchmark_returns,
    book_inits,
    chain_pointers,
    open_ledgers,
    panel_inits,
    process_pending,
    record_formation_states,
)
from hfexperiment.alpaca_source import AlpacaSource, SourceError  # noqa: E402
from hfexperiment.barstore import BarStore  # noqa: E402
from hfexperiment.envfile import (  # noqa: E402
    MissingCredentialsError,
    load_credentials,
)
from hfexperiment.formationrun import (  # noqa: E402
    CALENDAR_LOOKBACK_DAYS,
    FormationError,
    run_formation,
)
from hfexperiment.monitor import (  # noqa: E402
    HealthData,
    health_view,
    verdict_view,
)
from hfexperiment.registered import SHADOW_SERIES_START  # noqa: E402
from hfexperiment.verdictengine import recompute_and_append  # noqa: E402

DATA_DIR = ROOT / "data"
LEDGER_DIR = DATA_DIR / "ledger"
MONITOR_DIR = ROOT / "reports" / "monitor"
CALENDAR_FUTURE_DAYS = 40
TIMER_UNIT = "hfexperiment-bars.timer"


class StoreBarView:
    """The BarView protocol over the store's latest rows for one run."""

    def __init__(
        self,
        store: BarStore,
        symbols: list[str],
        span_sessions: list[str],
        active_today: set[str],
    ) -> None:
        self._sessions = span_sessions
        self._active = active_today
        if symbols and span_sessions:
            self._closes = store.latest_closes(
                symbols, span_sessions[0], span_sessions[-1]
            )
        else:
            self._closes = {}

    def close(self, symbol: str, session: str) -> float | None:
        return self._closes.get((symbol, session))

    def asset_active(self, symbol: str) -> bool:
        return symbol in self._active

    def bar_exists_later(self, symbol: str, session: str) -> bool:
        return any(
            s > session and (symbol, s) in self._closes
            for s in self._sessions
        )

    def absent_streak(self, symbol: str, session: str) -> int:
        streak = 0
        for s in reversed([x for x in self._sessions if x <= session]):
            if (symbol, s) in self._closes:
                break
            streak += 1
        return streak


def _utc_now() -> datetime.datetime:
    return datetime.datetime.now(datetime.UTC)


def _collect_and_accrue(
    store: BarStore, ledgers: Ledgers, source: AlpacaSource,
    run_utc: str, today: str,
) -> int:
    start = (
        datetime.date.fromisoformat(today)
        - datetime.timedelta(days=CALENDAR_LOOKBACK_DAYS)
    ).isoformat()
    end = (
        datetime.date.fromisoformat(today)
        + datetime.timedelta(days=CALENDAR_FUTURE_DAYS)
    ).isoformat()
    try:
        calendar = source.calendar(start, end)
    except SourceError as err:
        store.append_fetch(run_utc, err.endpoint, False, err.detail)
        print(f"SOURCE FAILED: {err}", file=sys.stderr)
        return 1
    store.append_sessions(calendar, run_utc)
    store.append_fetch(run_utc, "calendar", True, f"{len(calendar)} sessions")
    sessions = store.session_dates(start, end)
    complete = [s for s in sessions if s <= today]
    if not complete:
        print("SOURCE FAILED: calendar served no complete sessions",
              file=sys.stderr)
        return 1
    last_complete = complete[-1]
    if last_complete < SHADOW_SERIES_START:
        print(f"Series starts at the {SHADOW_SERIES_START} formation. "
              "Nothing to accrue yet.")
        return 0

    params = universe.RuleParams()
    recorded = set(store.recorded_formation_dates())
    due = [
        f for f in universe.formation_dates(sessions, params)
        if SHADOW_SERIES_START <= f <= last_complete and f not in recorded
    ]
    for fdate in due:
        try:
            result = run_formation(
                store, source, sessions, fdate, list(WIDTHS), run_utc
            )
            store.append_fetch(
                run_utc, "formation", True,
                f"{fdate}: {result.n_candidates} members, "
                f"{result.n_measurable} measurable",
            )
        except (FormationError, SourceError) as err:
            store.append_fetch(run_utc, "formation", False, f"{fdate}: {err}")
            print(f"FORMATION FAILED {fdate}: {err}", file=sys.stderr)
            return 1

    formed = store.recorded_formation_dates()
    if not formed:
        return 0
    symbols: set[str] = set()
    for fdate in formed:
        symbols.update(store.universe_members(fdate))
        for names in store.formation_books(fdate).values():
            symbols.update(names)
    pointers = chain_pointers(ledgers)
    span_start = min(pointers.values(), default=formed[0])
    span_sessions = [s for s in sessions if span_start <= s <= last_complete]

    fetch_ok = True
    active_today: set[str] = set()
    try:
        assets = source.active_assets()
        store.append_assets(assets, run_utc)
        active_today = {a[0] for a in assets}
        bars = source.daily_bars(sorted(symbols), span_start, last_complete)
        store.append_bars(
            [
                (sym, ses, o, h, lo, c, v)
                for sym, rows in bars.items()
                for ses, o, h, lo, c, v in rows
            ],
            "all",
            run_utc,
        )
        store.append_fetch(
            run_utc, "daily_bars", True,
            f"{len(symbols)} symbols {span_start}..{last_complete}",
        )
    except SourceError as err:
        store.append_fetch(run_utc, err.endpoint, False, err.detail)
        print(f"SOURCE FAILED: {err}", file=sys.stderr)
        fetch_ok = False

    if fetch_ok:
        have_inits = {p.formation_date for p in panel_inits(ledgers)}
        for fdate in formed:
            if fdate < SHADOW_SERIES_START or fdate in have_inits:
                continue
            members = store.universe_members(fdate)
            books = store.formation_books(fdate)
            needed = set(members).union(*books.values())
            entry = {}
            for sym in needed:
                close = store.last_close_at_or_before(sym, fdate)
                if close is not None:
                    entry[sym] = close
            missing = sorted(needed - set(entry))
            if missing:
                print(f"FORMATION {fdate}: no close at or before formation "
                      f"for {missing}", file=sys.stderr)
                return 1
            record_formation_states(
                ledgers, fdate, members, books, entry, run_utc
            )

    first_inits = panel_inits(ledgers)
    if first_inits:
        chain_sessions = [
            s for s in sessions
            if first_inits[0].formation_date <= s <= last_complete
        ]
        counts = process_pending(
            ledgers, StoreBarView(
                store, sorted(symbols), span_sessions, active_today
            ),
            chain_sessions, fetch_ok, run_utc,
        )
        print(f"accrual: {counts}")
        appended = recompute_and_append(ledgers, run_utc)
        print(f"verdict records appended: {len(appended)}")
    return 0 if fetch_ok else 1


def _timer_lines() -> list[str]:
    lines: list[str] = []
    for args in (
        ["systemctl", "--user", "is-enabled", TIMER_UNIT],
        ["systemctl", "--user", "is-active", TIMER_UNIT],
        [
            "systemctl", "--user", "list-timers", TIMER_UNIT,
            "--no-pager", "--no-legend",
        ],
    ):
        try:
            proc = subprocess.run(
                args, capture_output=True, text=True, timeout=10
            )
            text = (proc.stdout or proc.stderr).strip()
            lines.append(f"{args[2]}: {text or 'no output'}")
        except Exception as err:  # noqa: BLE001 - health must render anyway
            lines.append(f"{args[2]}: unavailable ({err})")
    return lines


def _aggregate_state_counts(ledgers: Ledgers) -> dict[str, int]:
    counts: dict[str, int] = {}

    def add(mapping: dict[str, int]) -> None:
        for key, value in mapping.items():
            counts[key] = counts.get(key, 0) + value

    for r in ledgers.benchmark.read_all():
        add(r.get("state_counts") or {})
        add(r.get("excluding_state_counts") or {})
    for r in ledgers.accrual.read_all():
        if r["status"] == "computed":
            states: dict[str, int] = {}
            for value in r["name_states"].values():
                states[value] = states.get(value, 0) + 1
            add(states)
        else:
            add(r.get("excluding_state_counts") or {})
    return counts


def _accrual_tail(ledgers: Ledgers, n: int = 6) -> list[str]:
    out: list[str] = []
    for r in ledgers.accrual.read_all()[-n:]:
        if r["status"] == "computed":
            out.append(
                f"{r['session']} w{r['width']} computed "
                f"excess {r['excess_bp']:+.2f} bp"
            )
        else:
            detail = ",".join(
                f"{k}:{v}"
                for k, v in sorted(
                    (r.get("excluding_state_counts") or {}).items()
                )
            )
            out.append(f"{r['session']} w{r['width']} excluded {detail}")
    return out


def _next_formation(
    store: BarStore, today: str
) -> tuple[str | None, int | None]:
    sessions = store.session_dates("2000-01-01", "2099-12-31")
    target: str | None = None
    if sessions:
        fdates = universe.formation_dates(sessions, universe.RuleParams())
        recorded = set(store.recorded_formation_dates())
        upcoming = [
            f for f in fdates
            if f >= SHADOW_SERIES_START and f not in recorded and f >= today
        ]
        target = upcoming[0] if upcoming else None
    elif today <= SHADOW_SERIES_START:
        target = SHADOW_SERIES_START
    if target is None:
        return None, None
    days = (
        datetime.date.fromisoformat(target)
        - datetime.date.fromisoformat(today)
    ).days
    return target, days


def _find_gaps(
    ledgers: Ledgers, store: BarStore, today: str
) -> tuple[list[str], str | None]:
    sessions = store.session_dates("2000-01-01", today)
    last_complete = sessions[-1] if sessions else None
    inits = panel_inits(ledgers)
    if not inits or last_complete is None:
        return [], last_complete
    bench = benchmark_returns(ledgers)
    start = inits[0].formation_date
    gaps = [
        s for s in sessions
        if start < s <= last_complete and s not in bench
    ]
    return gaps, last_complete


def _build_health(
    store: BarStore, ledgers: Ledgers, credentials: str,
    generated_utc: str, today: str,
) -> HealthData:
    fetches = store.recent_fetches(6)
    gaps, last_complete = _find_gaps(ledgers, store, today)
    next_formation, days = _next_formation(store, today)
    books: dict[int, list[str]] = {}
    for width in WIDTHS:
        inits = book_inits(ledgers, width)
        if inits:
            books[width] = list(inits[-1].names)
    panels = panel_inits(ledgers)
    return HealthData(
        generated_utc=generated_utc,
        credentials=credentials,
        timer_lines=_timer_lines(),
        last_run=fetches[0][0] if fetches else "never",
        last_complete_session=last_complete,
        next_formation=next_formation,
        days_to_next_formation=days,
        gaps=gaps,
        state_counts=_aggregate_state_counts(ledgers),
        books=books,
        benchmark_size=len(panels[-1].names) if panels else None,
        pointers=chain_pointers(ledgers),
        accrual_tail=_accrual_tail(ledgers),
        recent_fetches=[
            f"{run} {endpoint} {'ok' if ok else 'FAILED'} {detail}"
            for run, endpoint, ok, detail in fetches
        ],
    )


def _render(
    store: BarStore, ledgers: Ledgers, credentials: str,
    generated_utc: str, today: str,
) -> None:
    MONITOR_DIR.mkdir(parents=True, exist_ok=True)
    health = health_view(
        _build_health(store, ledgers, credentials, generated_utc, today)
    )
    verdict = verdict_view(ledgers.verdict.read_all())
    (MONITOR_DIR / "health.txt").write_text(health + "\n", encoding="utf-8")
    (MONITOR_DIR / "verdict.txt").write_text(verdict + "\n", encoding="utf-8")
    print(health)
    print()
    print(verdict)


def main(argv: list[str]) -> int:
    render_only = "--render-only" in argv
    ledgers = open_ledgers(LEDGER_DIR)
    store = BarStore(DATA_DIR / "bars.db")
    now = _utc_now()
    run_utc = now.strftime("%Y-%m-%dT%H:%M:%SZ")
    today = now.strftime("%Y-%m-%d")
    try:
        credentials = load_credentials(ROOT / ".env")
        cred_note = "present"
    except MissingCredentialsError as err:
        credentials = None
        cred_note = str(err)

    exit_code = 0
    if render_only:
        pass
    elif credentials is None:
        print(f"REFUSING: {cred_note}", file=sys.stderr)
        exit_code = 2
    else:
        source = AlpacaSource(
            credentials["ALPACA_KEY_ID"], credentials["ALPACA_SECRET_KEY"]
        )
        exit_code = _collect_and_accrue(store, ledgers, source, run_utc, today)
    _render(store, ledgers, cred_note, run_utc, today)
    store.close()
    return exit_code


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
