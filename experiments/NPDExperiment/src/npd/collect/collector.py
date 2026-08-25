"""The collector. Idempotent on date, retried by taxonomy, capped by ledger.

Resume is keyed on the session date. A date that already carries a terminal
state is never called again, so a crash or a reboot cannot double-charge. The
evidence ledger is the source of truth for that, because it is appended and
fsynced before the store is touched.

This module stores rankings. It joins nothing to any outcome and computes no
statistic. That boundary is the point of the whole repository.
"""

from __future__ import annotations

import datetime as dt
import sqlite3
import time
from collections.abc import Callable, Sequence
from dataclasses import dataclass, field
from pathlib import Path

from npd.callstate import CallState
from npd.collect import prompt as prompt_mod
from npd.collect.adapter import (
    Adapter,
    Answer,
    AuthFault,
    QuotaExhausted,
    TransientFault,
    UnparseableResponse,
    UnsupportedParameter,
    parse_ranking,
)
from npd.config import CONFIG, Config
from npd.data.store import open_store, record_day_state
from npd.ledger.evidence import EvidenceLedger
from npd.ledger.spend import SpendLedger, SpendRefused, cost_of
from npd.paths import STORE_DB

TERMINAL_STATES = frozenset(
    {CallState.STORED, CallState.NO_DATA, CallState.EXCLUDED_PRE_CUTOFF, CallState.MODEL_FAILED}
)


class CollectionStopped(RuntimeError):
    """A clean stop. The run ends and Section 0 fires on achieved coverage."""


@dataclass(slots=True)
class DayPayload:
    date: str
    labels: tuple[str, ...]
    z_by_label: dict[str, dict[str, float]]
    label_to_symbol: dict[str, str]


@dataclass(slots=True)
class CollectionResult:
    counts: dict[CallState, int] = field(default_factory=dict)
    calls_sent: int = 0
    reconciled: int = 0
    spend_usd: float = 0.0
    stopped_early: str = ""
    prompt_digest: str = ""

    def bump(self, state: CallState) -> None:
        self.counts[state] = self.counts.get(state, 0) + 1


def load_day(con: sqlite3.Connection, date: str, cfg: Config = CONFIG) -> DayPayload | None:
    """Assemble one day from the local store, or None when it cannot be served.

    None is a source fault, not a model fault. The caller records it as such.
    """
    anon = con.execute("SELECT label, symbol FROM anonymization WHERE date = ?", (date,)).fetchall()
    if len(anon) != cfg.panel_size:
        return None
    label_to_symbol = {r[0]: r[1] for r in anon}

    rows = con.execute("SELECT symbol, name, z FROM feature WHERE date = ?", (date,)).fetchall()
    if not rows:
        return None
    z_by_symbol: dict[str, dict[str, float]] = {}
    for sym, name, z in rows:
        if z is None:
            return None
        z_by_symbol.setdefault(sym, {})[name] = float(z)
    if len(z_by_symbol) != cfg.panel_size:
        return None
    if any(len(b) != len(cfg.feature_names) for b in z_by_symbol.values()):
        return None

    z_by_label = {lab: z_by_symbol[sym] for lab, sym in label_to_symbol.items()}
    # Presentation order is the stored label order, which anonymize shuffled.
    labels = tuple(lab for lab, _ in anon)
    return DayPayload(
        date=date, labels=labels, z_by_label=z_by_label, label_to_symbol=label_to_symbol
    )


def _sleep_backoff(attempt: int, cfg: Config, sleeper: Callable[[float], None]) -> None:
    delay = min(cfg.backoff_max_seconds, cfg.backoff_base_seconds * (2 ** (attempt - 1)))
    sleeper(delay)


def collect(
    dates: Sequence[str],
    adapter: Adapter,
    *,
    cfg: Config = CONFIG,
    spend: SpendLedger | None = None,
    evidence: EvidenceLedger | None = None,
    projected_cost_per_call: float | None = None,
    sleeper: Callable[[float], None] = time.sleep,
    pass_date_to_adapter: bool = False,
    store_path: Path = STORE_DB,
    retry_failed: bool = False,
    progress: Callable[[str, CallState, int, int], None] | None = None,
) -> CollectionResult:
    """Run the collection over the given dates. Resumes, retries, and refuses."""
    spend = spend or SpendLedger(cfg=cfg)
    evidence = evidence or EvidenceLedger()
    result = CollectionResult()

    terminal = TERMINAL_STATES - ({CallState.MODEL_FAILED} if retry_failed else frozenset())
    done = {
        d: CallState(row["state"])
        for d, row in evidence.last_row_by_date().items()
        if CallState(row["state"]) in terminal and _procedure_is_current(row, cfg)
    }
    for d, s in done.items():
        if d in set(dates):
            result.bump(s)

    todo = [d for d in dates if d not in done]
    batch_estimate = projected_cost_per_call
    if batch_estimate is None:
        measured = spend.mean_cost_per_call("gate")
        batch_estimate = measured if measured is not None else _registered_estimate(cfg)

    with open_store(store_path) as con:
        result.reconciled = reconcile(con, evidence, dates, cfg)
        for offset in range(0, len(todo), cfg.batch_size):
            batch = todo[offset : offset + cfg.batch_size]
            measured = spend.mean_cost_per_call("gate")
            per_call = measured if measured is not None else batch_estimate
            try:
                spend.refuse_if_projection_crosses_cap(
                    calls_in_batch=len(batch), projected_cost_per_call=per_call
                )
            except SpendRefused as exc:
                result.stopped_early = f"spend_refused: {exc}"
                return result

            for date in batch:
                payload = load_day(con, date)
                if payload is None:
                    evidence.record(
                        date=date,
                        state=CallState.SOURCE_FAILED,
                        model=cfg.gate_model,
                        attempt=0,
                        detail="the local store could not serve a complete panel",
                    )
                    record_day_state(con, date, CallState.SOURCE_FAILED.value, "incomplete panel")
                    result.bump(CallState.SOURCE_FAILED)
                    if progress is not None:
                        progress(date, CallState.SOURCE_FAILED, result.calls_sent, len(todo))
                    continue

                built = prompt_mod.build(payload.labels, payload.z_by_label, cfg)
                result.prompt_digest = result.prompt_digest or prompt_mod.template_digest(cfg)

                state, answer, detail = _call_with_retries(
                    adapter, built, date, cfg, evidence, spend, sleeper, pass_date_to_adapter
                )
                if state is None:
                    result.stopped_early = detail
                    con.commit()
                    return result

                if state is CallState.STORED and answer is not None:
                    con.executemany(
                        "INSERT OR REPLACE INTO model_ranking(date, rank, label, symbol) "
                        "VALUES(?,?,?,?)",
                        [
                            (date, i + 1, lab, payload.label_to_symbol[lab])
                            for i, lab in enumerate(answer.ranking)
                        ],
                    )
                record_day_state(con, date, state.value, detail)
                con.commit()
                result.bump(state)
                result.calls_sent += 1
                if progress is not None:
                    progress(date, state, result.calls_sent, len(todo))

    result.spend_usd = spend.total_usd()
    return result


def _procedure_is_current(row: dict[str, object], cfg: Config = CONFIG) -> bool:
    """Whether a stored day was produced by the procedure now in force.

    The test is the prompt template digest. A day whose stored answer came from a
    different prompt belongs to a different experiment, so it is recollected
    rather than mixed into a sample whose other days answered a different
    question. This generalizes what Amendment 3 needed and what Amendment 4
    needed, and it will catch the next one without further code.

    The superseded rows stay in the ledger. A ledger is history and history is
    not edited.
    """
    if CallState(str(row["state"])) is not CallState.STORED:
        return True
    return str(row.get("prompt_digest", "")) == prompt_mod.template_digest(cfg)


def reconcile(
    con: sqlite3.Connection,
    evidence: EvidenceLedger,
    dates: Sequence[str],
    cfg: Config = CONFIG,
) -> int:
    """Rebuild any ranking the ledger recorded but the store never committed.

    A process killed between the ledger append and the store commit leaves a
    date the ledger calls stored and the store cannot show. Resume must not call
    that date again, because the call was already paid for. It rebuilds the
    ranking from the raw response the ledger kept verbatim, which is the reason
    the raw response is kept at all.
    """
    wanted = set(dates)
    stored_in_ledger: dict[str, str] = {}
    for row in evidence.rows():
        if row.get("date") not in wanted or row.get("state") != CallState.STORED.value:
            continue
        if not _procedure_is_current(row, cfg):
            # Superseded by an amendment. The day is recollected, not rebuilt.
            stored_in_ledger.pop(str(row["date"]), None)
            continue
        stored_in_ledger[str(row["date"])] = str(row.get("raw_response", ""))

    have = (
        {
            r[0]
            for r in con.execute(
                "SELECT DISTINCT date FROM model_ranking WHERE date IN "
                f"({','.join('?' * len(stored_in_ledger))})",
                tuple(stored_in_ledger),
            )
        }
        if stored_in_ledger
        else set()
    )

    repaired = 0
    for date, raw in stored_in_ledger.items():
        if date in have:
            continue
        payload = load_day(con, date)
        if payload is None:
            continue
        try:
            ranking = parse_ranking(raw, payload.labels)
        except UnparseableResponse:
            # The ledger kept a response this panel cannot be rebuilt from. Left
            # for the collector to call again rather than repaired by a guess.
            continue
        con.executemany(
            "INSERT OR REPLACE INTO model_ranking(date, rank, label, symbol) VALUES(?,?,?,?)",
            [(date, i + 1, lab, payload.label_to_symbol[lab]) for i, lab in enumerate(ranking)],
        )
        record_day_state(con, date, CallState.STORED.value, "rebuilt from the evidence ledger")
        repaired += 1
    con.commit()
    return repaired


def effort_for_attempt(attempt: int, cfg: Config) -> str:
    """Which reasoning effort this attempt uses. Amendment 3.

    Attempt one uses the registered effort. A parse failure means the model did
    not return a usable permutation of the labels, which is a format compliance
    problem rather than a judgement problem, so the next attempt climbs one rung
    of the ladder and stays there. The ladder is identical for every day, so the
    procedure is uniform even though the realized effort is not.
    """
    ladder = cfg.reasoning_effort_ladder or (cfg.reasoning_effort,)
    return ladder[min(attempt - 1, len(ladder) - 1)]


def _call_with_retries(
    adapter: Adapter,
    built: prompt_mod.Prompt,
    date: str,
    cfg: Config,
    evidence: EvidenceLedger,
    spend: SpendLedger,
    sleeper: Callable[[float], None],
    pass_date: bool,
) -> tuple[CallState | None, Answer | None, str]:
    """Return the terminal state for one day, or None to stop the whole run."""
    last_detail = ""
    digest = prompt_mod.template_digest(cfg)
    for attempt in range(1, cfg.max_retries + 1):
        effort = effort_for_attempt(attempt, cfg)
        try:
            answer = (
                adapter.rank(built, date, effort) if pass_date else adapter.rank(built, "", effort)
            )
        except QuotaExhausted as exc:
            evidence.record(
                date=date,
                state=CallState.NO_DATA,
                model=cfg.gate_model,
                attempt=attempt,
                reasoning_effort=effort,
                prompt_digest=digest,
                detail=f"insufficient_quota: {exc}",
            )
            return None, None, f"quota_exhausted: {exc}"
        except AuthFault as exc:
            evidence.record(
                date=date,
                state=CallState.MODEL_FAILED,
                model=cfg.gate_model,
                attempt=attempt,
                reasoning_effort=effort,
                prompt_digest=digest,
                detail=f"auth: {exc}",
            )
            return None, None, f"auth_fault: {exc}"
        except UnsupportedParameter as exc:
            disable = getattr(adapter, "disable_temperature", None)
            if getattr(adapter, "send_temperature", False) and callable(disable):
                disable()
                evidence.record(
                    date=date,
                    state=CallState.MODEL_FAILED,
                    model=cfg.gate_model,
                    attempt=attempt,
                    reasoning_effort=effort,
                    prompt_digest=digest,
                    detail=f"parameter rejected, retrying without it: {exc}",
                )
                continue
            return None, None, f"unsupported_parameter: {exc}"
        except (TransientFault, UnparseableResponse) as exc:
            last_detail = f"{type(exc).__name__}: {exc}"
            # A rejected answer was still billed. The ledger sees those tokens or
            # the cap is enforced against a number that is too low.
            billed = getattr(exc, "usage", None)
            rejected_raw = str(getattr(exc, "raw", ""))
            failed_cost = 0.0
            if billed is not None:
                failed_cost = cost_of(
                    billed.input_tokens, billed.cached_input_tokens, billed.output_tokens, cfg
                )
                spend.record(
                    date=date,
                    kind="gate",
                    input_tokens=billed.input_tokens,
                    cached_input_tokens=billed.cached_input_tokens,
                    output_tokens=billed.output_tokens,
                    note=f"rejected answer, reasoning_effort={effort}, attempt={attempt}",
                )
            evidence.record(
                date=date,
                state=CallState.MODEL_FAILED,
                model=cfg.gate_model,
                attempt=attempt,
                reasoning_effort=effort,
                prompt_digest=digest,
                input_tokens=billed.input_tokens if billed else 0,
                cached_input_tokens=billed.cached_input_tokens if billed else 0,
                output_tokens=billed.output_tokens if billed else 0,
                reasoning_tokens=billed.reasoning_tokens if billed else 0,
                cost_usd=failed_cost,
                raw_response=rejected_raw,
                detail=last_detail,
            )
            if attempt < cfg.max_retries:
                _sleep_backoff(attempt, cfg, sleeper)
                continue
            return CallState.MODEL_FAILED, None, last_detail

        cost = cost_of(
            answer.usage.input_tokens,
            answer.usage.cached_input_tokens,
            answer.usage.output_tokens,
            cfg,
        )
        spend.record(
            date=date,
            kind="gate",
            note=f"reasoning_effort={effort}, attempt={attempt}",
            input_tokens=answer.usage.input_tokens,
            cached_input_tokens=answer.usage.cached_input_tokens,
            output_tokens=answer.usage.output_tokens,
        )
        evidence.record(
            date=date,
            state=CallState.STORED,
            model=cfg.gate_model,
            attempt=attempt,
            reasoning_effort=effort,
            prompt_digest=digest,
            input_tokens=answer.usage.input_tokens,
            cached_input_tokens=answer.usage.cached_input_tokens,
            output_tokens=answer.usage.output_tokens,
            reasoning_tokens=answer.usage.reasoning_tokens,
            cost_usd=cost,
            latency_s=answer.latency_s,
            raw_response=answer.raw,
        )
        return CallState.STORED, answer, ""
    return CallState.MODEL_FAILED, None, last_detail


def _registered_estimate(cfg: Config) -> float:
    """The Section 12.1 per-call estimate, used before any call has run."""
    return cost_of(1600, 0, 1150, cfg)


def utc_now() -> str:
    return dt.datetime.now(dt.UTC).isoformat()
