"""The Stage B entrypoint: one CLI invocation, behind the latch.

    python -m npl.stageb.cli hash   # record the B.1 read-surface hashes
    python -m npl.stageb.cli read   # the single registered read

The latch is written before the reader runs, so a crash after the latch
spends the read; recovery works from partial artifacts under an amendment,
never a silent re-run. The Amendment 3 table is applied mechanically to
the three co-primaries at central costs; secondaries never move a row.
This module is the registered sole importer of npl.stageb.reader.
"""

from __future__ import annotations

import json
import os
import sys
from dataclasses import asdict, replace
from pathlib import Path
from typing import Any

from npl.absence import Absent
from npl.census import CensusLedger, CensusRow
from npl.clock import iso_z, now_utc, utc_ms
from npl.config import CONFIG, Config
from npl.ledger.append_only import AppendOnlyLedger
from npl.paths import OUTCOMES_DIR, PAIRS_LEDGER, REPORTS
from npl.stageb.preconditions import (
    HASHES_B0_JSON,
    MIN_N_P1,
    MIN_N_P2,
    MIN_N_P3,
    READ_SURFACE,
    REGISTERED_EVENT_N,
    REGISTERED_PAIR_N,
    RETRO_PLAN,
    STAGE_B_LATCH,
    FundingTimes,
    PreconditionFailure,
    module_hashes,
    reconstruct_cohort,
    run_preconditions,
)
from npl.stageb.reader import CohortRead, FundingRates, read_cohort
from npl.verdict import (
    BinomialTest,
    EventNet,
    p1_profitability,
    p2_magnitude,
    p3_contrast,
    run_verdict,
)

READ_JSON = REPORTS / "stage_b" / "read.json"
HASHES_B1_JSON = REPORTS / "stage_b" / "hashes_b1.json"
B1_SURFACE: tuple[str, ...] = (*READ_SURFACE, "stageb/reader.py", "stageb/cli.py")

# Amendment 3 rule 4 sanctions exactly one diff against the B.0 hashes: the
# stageb package marker gaining the registered allowlist constant.
SANCTIONED_B1_DIFFS: frozenset[str] = frozenset({"stageb/__init__.py"})


class ReadAlreadySpent(RuntimeError):
    """The latch exists: the single registered read is spent."""


class ReadAuthorizationVoided(RuntimeError):
    """A read-surface module differs from its recorded hash."""


def write_b1_hashes(
    b0_path: Path = HASHES_B0_JSON, b1_path: Path = HASHES_B1_JSON
) -> dict[str, str]:
    """The B.1 re-hash. Any unsanctioned drift from B.0 voids the authorization."""
    recorded_b0: dict[str, str] = json.loads(b0_path.read_text(encoding="utf-8"))
    current = module_hashes(B1_SURFACE)
    drifted = sorted(
        rel
        for rel, digest in recorded_b0.items()
        if current.get(rel) != digest and rel not in SANCTIONED_B1_DIFFS
    )
    if drifted:
        raise ReadAuthorizationVoided(
            f"B.0-hashed modules drifted outside the sanctioned Amendment 3 set: {drifted}; "
            f"the read authorization is void and an amendment is required"
        )
    b1_path.parent.mkdir(parents=True, exist_ok=True)
    b1_path.write_text(json.dumps(current, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return current


def verify_read_surface(recorded_path: Path = HASHES_B1_JSON) -> dict[str, str]:
    """The read runs only on byte-identical recorded modules."""
    if not recorded_path.exists():
        raise ReadAuthorizationVoided(
            f"{recorded_path} does not exist; run `python -m npl.stageb.cli hash` first"
        )
    recorded: dict[str, str] = json.loads(recorded_path.read_text(encoding="utf-8"))
    current = module_hashes(B1_SURFACE)
    diffs = sorted(rel for rel in current if recorded.get(rel) != current[rel])
    if diffs or set(recorded) != set(current):
        raise ReadAuthorizationVoided(
            f"read-surface modules differ from the recorded B.1 hashes: {diffs}; "
            f"the read authorization is void and an amendment is required"
        )
    return current


def write_latch(hashes: dict[str, str], latch_path: Path = STAGE_B_LATCH) -> None:
    """Write-once, fsynced. Existence alone spends the read."""
    latch_path.parent.mkdir(parents=True, exist_ok=True)
    payload = {"read_at": iso_z(now_utc()), "module_hashes": hashes}
    with latch_path.open("x", encoding="utf-8") as fh:
        json.dump(payload, fh, indent=2, sort_keys=True)
        fh.write("\n")
        fh.flush()
        os.fsync(fh.fileno())


def fire_row(p1: BinomialTest, p2: BinomialTest, p3: BinomialTest) -> str:
    """The Amendment 3 table, mechanically. Secondaries never move a row."""
    if p1.passes and p2.passes and p3.passes:
        return "GO"
    if p1.passes and p2.passes:
        return "PARTIAL_DRIFT"
    return "FAIL"


def _stats(events: list[EventNet], cfg: Config) -> dict[str, Any]:
    return {
        "p1": asdict(p1_profitability(events, cfg)),
        "p2": asdict(p2_magnitude(events, cfg)),
        "p3": asdict(p3_contrast(events, cfg)),
    }


def registered_secondaries(read: CohortRead, cfg: Config) -> dict[str, Any]:
    """Exactly the Amendment 3 list, descriptive. Nothing else is computed."""
    central = list(read.events_central)
    secondaries: dict[str, Any] = dict(run_verdict(central, cfg).secondaries)
    shifted = [
        replace(e, net_short_30=e.net_short_90, control_net_short_30=e.control_net_short_90)
        for e in central
    ]
    secondaries["horizon_90d_co_primaries"] = _stats(shifted, cfg)
    truncated_nets = [
        e.net_short_30
        for e in central
        if e.truncated_by_delisting and not isinstance(e.net_short_30, Absent)
    ]
    secondaries["truncated_by_delisting_30d"] = {
        "n": len(truncated_nets),
        "share_positive": (
            sum(1 for x in truncated_nets if isinstance(x, float) and x > 0.0) / len(truncated_nets)
            if truncated_nets
            else 0.0
        ),
    }
    secondaries["forward_vs_retro_note"] = (
        "zero forward events are readable yet; the placeholder strata sit in "
        "forward_vs_retro_30d and the forward cohort reads only under its own "
        "future registration"
    )
    secondaries["h8_paired_30d"] = {
        "n": read.paired_h8_n,
        "mean_funding_term_diff": read.paired_h8_mean_funding_diff,
        "mean_price_term_diff": read.paired_h8_mean_price_diff,
    }
    secondaries["cost_band_sensitivity"] = {
        "low": _stats(list(read.events_low), cfg),
        "central": _stats(central, cfg),
        "high": _stats(list(read.events_high), cfg),
    }
    return secondaries


def execute_read(
    census_rows: list[CensusRow],
    plan_rows: list[dict[str, Any]],
    pair_rows: list[dict[str, Any]],
    funding_times: FundingTimes,
    funding_rates: FundingRates,
    outcomes_root: Path = OUTCOMES_DIR,
    latch_path: Path = STAGE_B_LATCH,
    hashes_path: Path = HASHES_B1_JSON,
    now_ms: int | None = None,
    cfg: Config = CONFIG,
    registered_event_n: int = REGISTERED_EVENT_N,
    registered_pair_n: int = REGISTERED_PAIR_N,
    min_n: tuple[int, int, int] = (MIN_N_P1, MIN_N_P2, MIN_N_P3),
) -> dict[str, Any]:
    """The single read: latch first, then the reader, then the table."""
    if latch_path.exists():
        raise ReadAlreadySpent(
            f"the latch {latch_path} exists: the single registered read is spent; "
            f"recovery works from partial artifacts under an amendment, never a re-run"
        )
    precondition_report, windows = run_preconditions(
        census_rows,
        plan_rows,
        pair_rows,
        funding_times,
        outcomes_root,
        latch_path,
        cfg,
        registered_event_n,
        registered_pair_n,
        min_n,
    )
    hashes = verify_read_surface(hashes_path)
    events, controls = reconstruct_cohort(census_rows, plan_rows, pair_rows, cfg)
    write_latch(hashes, latch_path)

    at = now_ms if now_ms is not None else utc_ms(now_utc())
    read = read_cohort(events, controls, windows, at, outcomes_root, funding_rates, cfg)
    verdict = run_verdict(list(read.events_central), cfg)
    row = fire_row(verdict.p1, verdict.p2, verdict.p3)
    return {
        "read_at": iso_z(now_utc()),
        "alpha_adj": cfg.alpha_adj,
        "preconditions": asdict(precondition_report),
        "pending_30": read.pending_30,
        "pending_90": read.pending_90,
        "funding_rows_30_total": read.funding_rows_30_total,
        "co_primaries": {
            "p1": asdict(verdict.p1),
            "p2": asdict(verdict.p2),
            "p3": asdict(verdict.p3),
        },
        "all_co_primaries_pass": verdict.all_co_primaries_pass,
        "row_fired": row,
        "secondaries": registered_secondaries(read, cfg),
        "module_hashes": hashes,
    }


def main(argv: list[str]) -> int:
    if len(argv) != 2 or argv[1] not in {"hash", "read"}:
        print("usage: python -m npl.stageb.cli {hash|read}", file=sys.stderr)
        return 2
    if argv[1] == "hash":
        try:
            hashes = write_b1_hashes()
        except (ReadAuthorizationVoided, PreconditionFailure) as exc:
            print(f"HASH REFUSED: {exc}", file=sys.stderr)
            return 1
        print(f"B.1 read-surface hashes recorded: {len(hashes)} modules -> {HASHES_B1_JSON}")
        return 0

    census_rows = CensusLedger().rows()
    plan_rows = AppendOnlyLedger(RETRO_PLAN).require_intact()
    pair_rows = AppendOnlyLedger(PAIRS_LEDGER).require_intact()
    try:
        payload = execute_read(census_rows, plan_rows, pair_rows, FundingTimes(), FundingRates())
    except (ReadAlreadySpent, ReadAuthorizationVoided, PreconditionFailure) as exc:
        print(f"READ REFUSED: {exc}", file=sys.stderr)
        return 1
    READ_JSON.parent.mkdir(parents=True, exist_ok=True)
    READ_JSON.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    p1 = payload["co_primaries"]["p1"]
    p2 = payload["co_primaries"]["p2"]
    p3 = payload["co_primaries"]["p3"]
    print(
        f"row fired: {payload['row_fired']} at alpha_adj {payload['alpha_adj']:.6f}\n"
        f"P1 n={p1['n']} successes={p1['successes']} lower_bound={p1['statistic']:.6f} "
        f"passes={p1['passes']}\n"
        f"P2 n={p2['n']} successes={p2['successes']} p_value={p2['statistic']:.3e} "
        f"passes={p2['passes']}\n"
        f"P3 n={p3['n']} successes={p3['successes']} p_value={p3['statistic']:.3e} "
        f"passes={p3['passes']}\n"
        f"pending 30d={payload['pending_30']} 90d={payload['pending_90']}; "
        f"funding rows in 30d windows n={payload['funding_rows_30_total']}\n"
        f"artifact -> {READ_JSON}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
