"""Task 3 of the H2 amendment stage: power and boundaries under Amendment H2-3.

Exact binomial arithmetic over counts, rates, and registered probabilities.
Nothing here opens a sealed store, parses a payload, or reads an outcome
value: the only measured inputs are the pair ledger's row count, pair tags,
and entry timestamps, the A.1 accrual rate, and the registered constants.

It produces `reports/stage_a_h2/ktable_amended.json`:

  - the alpha-split materiality evaluation (Amendment H2-3 Change 3),
  - look-1 and look-2 minimum N per co-primary, each reported at the
    amended 0.625 true share **and** at the unchanged 0.60, beside the
    single-look figures under the old 2x floor and the new 1x floor,
  - the exact boundary table (k1, k2, both spends, power, the probability
    the look-1 boundary fires, and the futility boundary) at every scenario,
  - the readable-pair projection by month and the projected look dates,
  - the Section 0 gate recomputed under the amended design.
"""

from __future__ import annotations

import json
from datetime import UTC, date, datetime, timedelta

from npl.clock import MS_PER_DAY, iso_z, now_utc
from npl.config import CONFIG
from npl.controls import pair_type_of_row
from npl.ledger.append_only import AppendOnlyLedger
from npl.paths import H2_PAIRS_LEDGER, REPORTS
from npl.power import min_n_for_power
from npl.register.cull import fire_hypothesis_section0, register_specs, spec_power
from npl.register.sequential import (
    futility_boundary,
    look1_stop_probability,
    min_n2_for_power,
    planned_n1,
    two_look_design,
    two_look_power,
)

REPORT = REPORTS / "stage_a_h2" / "ktable_amended.json"

ALPHA_H = 0.05  # k = 1, fixed by the A.2 cull and never revisited
POWER_TARGET = CONFIG.power_go_floor  # 0.80
N_MAX = 400
BACKFILL_COHORT = 62  # the fresh pending-at-closure cohort

# A.1 measured accrual, trailing 182 days, n = 113 events.
ACCRUAL_PER_MONTH = 18.57
DAYS_PER_MONTH = 30.44
PRE_AMENDMENT_MATCH_RATE = 0.613
# ADR-019: a fresh pair's candle window seals once, at entry + 92 days, so
# that is the date its 30-day primary becomes readable. Entry is listing + 2.
READABLE_LAG_DAYS = 92
FORWARD_READABLE_LAG_DAYS = 94

SPLITS: tuple[tuple[float, float], ...] = (
    (0.02, 0.03),
    (0.025, 0.025),
    (0.015, 0.035),
    (0.01, 0.04),
    (0.005, 0.045),
    (0.03, 0.02),
)
# Amendment H2-3 Change 3, the materiality test, stated before it is applied.
MATERIAL_POWER_GAIN = 0.01
MATERIAL_MAX_STOP_LOSS = 0.05


def _ms(day: date) -> int:
    return int(datetime(day.year, day.month, day.day, tzinfo=UTC).timestamp() * 1000)


def readable_schedule() -> tuple[list[int], dict[str, int]]:
    """Backfill pairs by the date each becomes readable, plus the tag counts."""
    rows = AppendOnlyLedger(H2_PAIRS_LEDGER).read().rows
    tags: dict[str, int] = {}
    for row in rows:
        tag = pair_type_of_row(row)
        tags[tag] = tags.get(tag, 0) + 1
    readable = sorted(int(r["entry_ms"]) + READABLE_LAG_DAYS * MS_PER_DAY for r in rows)
    return readable, tags


def projected_pairs(readable: list[int], at: date, today: date) -> tuple[int, int, int]:
    """(backfill readable, forward readable, total) at a date. Counts only."""
    cut = _ms(at)
    backfill = sum(1 for ms in readable if ms <= cut)
    horizon_days = (at - today).days - FORWARD_READABLE_LAG_DAYS
    forward = max(0, int(ACCRUAL_PER_MONTH * horizon_days / DAYS_PER_MONTH))
    return backfill, forward, backfill + forward


def first_date_reaching(readable: list[int], target: int, today: date, limit: date) -> str | None:
    """The earliest day at which total readable pairs reaches the target."""
    day = today
    while day <= limit:
        if projected_pairs(readable, day, today)[2] >= target:
            return day.isoformat()
        day += timedelta(days=1)
    return None


def design_row(n1: int, n2: int, a1: float, a2: float, p_true: float) -> dict[str, object]:
    design = two_look_design(n1, n2, a1, a2)
    return {
        "n1": n1,
        "n2": n2,
        "alpha_1": a1,
        "alpha_2": a2,
        "k1": design.k1,
        "k2": design.k2,
        "alpha_spent_look1": round(design.alpha_spent_1, 6),
        "alpha_spent_look2": round(design.alpha_spent_2, 6),
        "alpha_spent_total": round(design.alpha_spent_total(), 6),
        "power": round(two_look_power(design, p_true), 6),
        "p_look1_boundary_fires": round(look1_stop_probability(design, p_true), 6),
        "futility_boundary_f1": futility_boundary(design, p_true, CONFIG),
    }


def single_look_min_n(p_true: float) -> int | None:
    return min_n_for_power(0.5, p_true, ALPHA_H, POWER_TARGET, N_MAX)


def _int(value: object) -> int:
    assert isinstance(value, int)
    return value


def main() -> int:
    today = now_utc().date()
    deadline = date.fromisoformat(CONFIG.projection_deadline)
    interim = date.fromisoformat(CONFIG.interim_deadline)
    readable, tags = readable_schedule()

    shares = {
        "E1": CONFIG.h2_e1_true_share,
        "E2": CONFIG.h2_e2_true_share,
        "E2_at_two_times_share": CONFIG.h2_e2_true_share_two_times_floor,
    }
    deadline_n = projected_pairs(readable, deadline, today)[2]

    # --- the alpha split, evaluated against the registered materiality test -
    split_rows: list[dict[str, object]] = []
    for a1, a2 in SPLITS:
        row = design_row(planned_n1(deadline_n), deadline_n, a1, a2, shares["E2"])
        row["min_n2_governing"] = min_n2_for_power(a1, a2, shares["E2"], POWER_TARGET, N_MAX)
        split_rows.append(row)
    base = next(r for r in split_rows if r["alpha_1"] == CONFIG.h2_alpha_look1)
    for row in split_rows:
        gain = float(row["power"]) - float(base["power"])
        stop_loss = float(base["p_look1_boundary_fires"]) - float(row["p_look1_boundary_fires"])
        row["power_gain_vs_registered"] = round(gain, 6)
        row["look1_stop_loss_vs_registered"] = round(stop_loss, 6)
        row["clause_a_power_gain"] = gain >= MATERIAL_POWER_GAIN
        row["clause_b_stop_loss_ok"] = stop_loss <= MATERIAL_MAX_STOP_LOSS
        row["materially_better"] = bool(row["clause_a_power_gain"] and row["clause_b_stop_loss_ok"])
    replacements = [
        r for r in split_rows if r["materially_better"] and r["alpha_1"] != base["alpha_1"]
    ]

    # --- minimum N per co-primary, both looks, both E2 assumptions ----------
    min_n: dict[str, object] = {}
    for name, p_true in (
        ("E1", shares["E1"]),
        ("E2_1x_floor_share_0.625", shares["E2"]),
        ("E2_1x_floor_share_0.600_reported_beside", shares["E2_at_two_times_share"]),
    ):
        look2 = min_n2_for_power(
            CONFIG.h2_alpha_look1, CONFIG.h2_alpha_look2, p_true, POWER_TARGET, N_MAX
        )
        min_n[name] = {
            "look2_min_n": look2,
            "look1_min_n": planned_n1(look2) if look2 else None,
            "single_look_min_n_at_alpha_h": single_look_min_n(p_true),
            "boundary_at_min_n": (
                design_row(
                    planned_n1(look2), look2, CONFIG.h2_alpha_look1, CONFIG.h2_alpha_look2, p_true
                )
                if look2
                else None
            ),
        }
    min_n["E2_pre_amendment_2x_floor_share_0.600_single_look"] = {
        "single_look_min_n_at_alpha_h": single_look_min_n(shares["E2_at_two_times_share"]),
        "note": "Amendment H2-1 recorded 169; recomputed here from the same registered inputs",
    }

    e1_look1 = _int(min_n["E1"]["look1_min_n"])  # type: ignore[index]
    e2_look1 = _int(min_n["E2_1x_floor_share_0.625"]["look1_min_n"])  # type: ignore[index]
    e1_look2 = _int(min_n["E1"]["look2_min_n"])  # type: ignore[index]
    e2_look2 = _int(min_n["E2_1x_floor_share_0.625"]["look2_min_n"])  # type: ignore[index]
    governing_look1 = max(e1_look1, e2_look1)
    governing_look2 = max(e1_look2, e2_look2)

    # --- the projection and the look dates ---------------------------------
    months: list[dict[str, object]] = []
    cursor = date(today.year, today.month, 1)
    while cursor <= deadline:
        nxt = date(cursor.year + (cursor.month == 12), (cursor.month % 12) + 1, 1)
        month_end = min(nxt - timedelta(days=1), deadline)
        backfill, forward, total = projected_pairs(readable, month_end, today)
        months.append(
            {
                "as_of": month_end.isoformat(),
                "backfill_pairs_readable": backfill,
                "forward_pairs_readable": forward,
                "total_pairs_readable": total,
            }
        )
        cursor = nxt

    look1_date = first_date_reaching(readable, governing_look1, today, deadline)
    look2_reach = first_date_reaching(readable, governing_look2, today, deadline)
    look2_date = min(x for x in (look2_reach, deadline.isoformat()) if x)

    # --- scenarios ----------------------------------------------------------
    scenarios = {
        "achieved_readable_today": projected_pairs(readable, today, today)[2],
        "backfill_cohort_fully_readable_2026-11-30": projected_pairs(
            readable, date(2026, 11, 30), today
        )[2],
        f"interim_{CONFIG.interim_deadline}": projected_pairs(readable, interim, today)[2],
        f"deadline_{CONFIG.projection_deadline}": deadline_n,
        "at_look1_min_n": governing_look1,
        "at_look2_min_n": governing_look2,
    }
    boundaries: dict[str, object] = {}
    for label, n in scenarios.items():
        if n < 2:
            boundaries[label] = {"n_as_look2": n, "note": "too few pairs for a boundary"}
            continue
        boundaries[label] = {
            "n_as_look2": n,
            "E1": design_row(
                planned_n1(n), n, CONFIG.h2_alpha_look1, CONFIG.h2_alpha_look2, shares["E1"]
            ),
            "E2": design_row(
                planned_n1(n), n, CONFIG.h2_alpha_look1, CONFIG.h2_alpha_look2, shares["E2"]
            ),
            "E2_reported_beside_at_0.600": design_row(
                planned_n1(n),
                n,
                CONFIG.h2_alpha_look1,
                CONFIG.h2_alpha_look2,
                shares["E2_at_two_times_share"],
            ),
        }

    # The registered look-1 futility boundary uses n2 = the co-primary's
    # registered look-2 minimum N (or the observed n1 where that is larger).
    futility = {
        "n1_at_the_projected_look1": governing_look1,
        "n2_rule": (
            "the co-primary's registered look-2 minimum N, or the observed n1 where that is "
            "larger — the real n2 is not observable at look 1"
        ),
        "conditional_power_floor": CONFIG.h2_futility_conditional_power,
        "E1": design_row(
            governing_look1,
            max(governing_look1, e1_look2),
            CONFIG.h2_alpha_look1,
            CONFIG.h2_alpha_look2,
            shares["E1"],
        ),
        "E2": design_row(
            governing_look1,
            max(governing_look1, e2_look2),
            CONFIG.h2_alpha_look1,
            CONFIG.h2_alpha_look2,
            shares["E2"],
        ),
    }

    # --- the single-look k-table extension and the Section 0 gate ----------
    specs = {(s.hypothesis, s.name): s for s in register_specs()}
    single_look: dict[str, object] = {}
    for name in ("E1", "E2"):
        sp = spec_power(specs[("H2", name)], deadline_n, ALPHA_H)
        single_look[f"H2/{name}"] = {
            "n": deadline_n,
            "power_governing": round(sp.power_governing, 6),
            "power_reported": (None if sp.power_reported is None else round(sp.power_reported, 6)),
        }
    gate = fire_hypothesis_section0(
        "H2", [spec_power(specs[("H2", n)], deadline_n, ALPHA_H) for n in ("E1", "E2")], ALPHA_H
    )

    two_look_deadline = {
        "E1": design_row(
            planned_n1(deadline_n),
            deadline_n,
            CONFIG.h2_alpha_look1,
            CONFIG.h2_alpha_look2,
            shares["E1"],
        ),
        "E2": design_row(
            planned_n1(deadline_n),
            deadline_n,
            CONFIG.h2_alpha_look1,
            CONFIG.h2_alpha_look2,
            shares["E2"],
        ),
    }
    governing_power = min(float(two_look_deadline[k]["power"]) for k in ("E1", "E2"))

    payload: dict[str, object] = {
        "computed_at": iso_z(now_utc()),
        "amendment": "H2-3 (Changes 1-3); the boundary record is Amendment H2-4",
        "outcome_values_read": 0,
        "inputs": {
            "k": 1,
            "alpha_h": ALPHA_H,
            "alpha_1": CONFIG.h2_alpha_look1,
            "alpha_2": CONFIG.h2_alpha_look2,
            "planning_interim_fraction": CONFIG.h2_planning_interim_fraction,
            "futility_conditional_power_floor": CONFIG.h2_futility_conditional_power,
            "cost_floor_multiple": CONFIG.h2_cost_floor_multiple,
            "cost_floor_multiple_secondary": CONFIG.h2_cost_floor_multiple_secondary,
            "true_shares": shares,
            "achieved_pairs_by_tag": tags,
            "achieved_pairs_total": sum(tags.values()),
            "measured_match_rate_backfillable_cohort": round(
                sum(tags.values()) / BACKFILL_COHORT, 4
            ),
            "measured_accrual_events_per_month": ACCRUAL_PER_MONTH,
            "readable_lag_days_backfill": READABLE_LAG_DAYS,
            "readable_lag_days_forward": FORWARD_READABLE_LAG_DAYS,
            "today": today.isoformat(),
        },
        "pair_projection_models": {
            "by_dex_measured": (
                "per-dex accrual with pairability onsets — under the Amendment H2-3 fallback "
                "every dex is pairable at every entry, because the main-dex candidate universe "
                "(174 elders aged 180d+, and growing) is available to every event. Pairs = events."
            ),
            "flat": (
                "measured match rate x forward events. The measured rate is now 62/62 = 1.000, so "
                "the flat and by-dex models COINCIDE under the fallback — the divergence that "
                "made the flat variant fire k = 0 at Amendment H2-1 is gone."
            ),
            "withdrawal_sensitivity": (
                f"at the pre-amendment same-dex-only match rate of {PRE_AMENDMENT_MATCH_RATE} the "
                f"deadline pair count would be {int(PRE_AMENDMENT_MATCH_RATE * deadline_n)} "
                f"instead of {deadline_n} — the cost if the relaxation were withdrawn."
            ),
        },
        "alpha_split_evaluation": {
            "registered": [CONFIG.h2_alpha_look1, CONFIG.h2_alpha_look2],
            "materiality_test": {
                "clause_a": (
                    f"governing power gain at the projected look-2 N >= {MATERIAL_POWER_GAIN}"
                ),
                "clause_b": (
                    "reduction in the governing co-primary's probability of a look-1 GO under "
                    f"the registered alternative <= {MATERIAL_MAX_STOP_LOSS}"
                ),
            },
            "evaluated_at_n2": deadline_n,
            "governing_co_primary": "E2",
            "candidates": split_rows,
            "materially_better_splits": [[r["alpha_1"], r["alpha_2"]] for r in replacements],
            "decision": (
                "no candidate split passes both clauses; alpha_1 = 0.02 and alpha_2 = 0.03 stand "
                "as registered"
                if not replacements
                else "a materially better split exists; see materially_better_splits"
            ),
        },
        "minimum_n": min_n,
        "governing_look1_min_n": governing_look1,
        "governing_look2_min_n": governing_look2,
        "boundaries": boundaries,
        "look1_futility": futility,
        "projection_by_month": months,
        "projected_look_dates": {
            "look1": look1_date,
            "look1_condition": (
                f"both co-primaries at their look-1 minimum N (E1 {e1_look1}, E2 {e2_look1}; "
                f"governing {governing_look1} readable eligible pairs)"
            ),
            "look2": look2_date,
            "look2_condition": (
                f"the earlier of {CONFIG.projection_deadline} and the date both reach their "
                f"look-2 minimum N (E1 {e1_look2}, E2 {e2_look2}; governing {governing_look2}), "
                f"reached {look2_reach or 'not by the deadline'}"
            ),
        },
        "single_look_k_table_extension_at_deadline": single_look,
        "two_look_at_deadline": two_look_deadline,
        "section0_gate_recomputed": {
            "governing_two_look_power_at_deadline": round(governing_power, 6),
            "single_look_gate": {
                "verdict": gate.verdict.value,
                "governing_power": round(gate.governing_power, 6),
                "rationale": gate.rationale,
            },
            "note": (
                "the Section 0 map is stated on single-look power (Amendment H2-1); the two-look "
                "figure is what actually governs the amended design and is reported beside it, "
                "per the DEGRADED rule that recomputed power travels with the registered target"
            ),
        },
    }

    # A loud refusal if the arithmetic ever contradicts the registered budget.
    for label, row in boundaries.items():
        if "E1" not in row:
            continue
        for leg in ("E1", "E2", "E2_reported_beside_at_0.600"):
            spent = float(row[leg]["alpha_spent_total"])
            if spent > ALPHA_H + 1e-12:
                raise SystemExit(f"{label}/{leg} spends {spent} > alpha_h {ALPHA_H}; refusing")

    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(payload["minimum_n"], indent=2, sort_keys=True))
    print(json.dumps(payload["projected_look_dates"], indent=2, sort_keys=True))
    print(json.dumps(payload["projection_by_month"], indent=2))
    print("alpha split:", payload["alpha_split_evaluation"]["decision"])
    print(f"governing two-look power at the deadline: {governing_power:.4f}")
    print(f"report -> {REPORT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
