"""Task 5 of H2 Amendment Stage 2: power and look dates under the tiered rule.

Exact binomial arithmetic over counts, rates, and registered probabilities.
Nothing here opens a sealed store, parses a payload, or reads an outcome
value: the only measured inputs are the v2 pair ledger's row count, tiers,
class pairs, and entry timestamps, the A.1 accrual rate, and the registered
constants.

Every figure is reported **beside the Amendment H2-4 projection it
supersedes**, so the cost of the tightening is legible in one table. The
H2-4 figures are quoted from the recorded artifact
`reports/stage_a_h2/ktable_amended.json` rather than recomputed: a
recomputed "superseded" number would not be the number the amendment
recorded.

It produces `reports/stage_a_h2/ktable_tiered.json`.
"""

from __future__ import annotations

import json
from datetime import date

from npl.clock import iso_z, now_utc
from npl.config import CONFIG
from npl.ledger.append_only import AppendOnlyLedger
from npl.paths import H2_PAIRS_LEDGER, H2_PAIRS_V2_LEDGER, REPORTS
from npl.power import min_n_for_power
from npl.register.cull import fire_hypothesis_section0, register_specs, spec_power
from npl.register.projection import (
    first_date_reaching,
    month_ends,
    projected_pairs,
    readable_days,
)
from npl.register.sequential import (
    futility_boundary,
    look1_stop_probability,
    min_n2_for_power,
    planned_n1,
    two_look_design,
    two_look_power,
)
from npl.register.tiered import assigned_rows, class_pair_of_row, tier_of_row
from npl.tier import REGISTERED_TIERS, TIER_NAMES

REPORT = REPORTS / "stage_a_h2" / "ktable_tiered.json"
SUPERSEDED_REPORT = REPORTS / "stage_a_h2" / "ktable_amended.json"

ALPHA_H = 0.05  # k = 1, fixed by the A.2 cull and never revisited
POWER_TARGET = CONFIG.power_go_floor  # 0.80
N_MAX = 400

# A.1 measured accrual, trailing 182 days, n = 113 events. Unchanged by this
# amendment: the taxonomy changes which events pair, never how many are born.
ACCRUAL_PER_MONTH = 18.57


def _int(value: object) -> int:
    assert isinstance(value, int)
    return value


def main() -> int:
    today = now_utc().date()
    deadline = date.fromisoformat(CONFIG.projection_deadline)
    interim = date.fromisoformat(CONFIG.interim_deadline)

    all_rows = AppendOnlyLedger(H2_PAIRS_V2_LEDGER).require_intact()
    pairs = assigned_rows(all_rows)
    events_total = len(all_rows)
    superseded_rows = AppendOnlyLedger(H2_PAIRS_LEDGER).require_intact()

    tiers = {f"tier_{t}": sum(1 for r in pairs if tier_of_row(r) == t) for t in REGISTERED_TIERS}
    class_pairs: dict[str, int] = {}
    for row in pairs:
        label = class_pair_of_row(row)
        class_pairs[label] = class_pairs.get(label, 0) + 1
    exclusions: dict[str, int] = {}
    for row in all_rows:
        state = str(row["state"])
        if state != "assigned":
            exclusions[state] = exclusions.get(state, 0) + 1

    match_rate = len(pairs) / events_total if events_total else 0.0
    readable = readable_days([int(str(r["entry_ms"])) for r in pairs])

    def project(at: date) -> tuple[int, int, int]:
        return projected_pairs(readable, at, today, ACCRUAL_PER_MONTH, match_rate)

    shares = {
        "E1": CONFIG.h2_e1_true_share,
        "E2": CONFIG.h2_e2_true_share,
        "E2_at_two_times_share": CONFIG.h2_e2_true_share_two_times_floor,
    }
    deadline_n = project(deadline)[2]

    def design_row(n1: int, n2: int, p_true: float) -> dict[str, object]:
        design = two_look_design(n1, n2, CONFIG.h2_alpha_look1, CONFIG.h2_alpha_look2)
        return {
            "n1": n1,
            "n2": n2,
            "k1": design.k1,
            "k2": design.k2,
            "alpha_spent_look1": round(design.alpha_spent_1, 6),
            "alpha_spent_look2": round(design.alpha_spent_2, 6),
            "alpha_spent_total": round(design.alpha_spent_total(), 6),
            "power": round(two_look_power(design, p_true), 6),
            "p_look1_boundary_fires": round(look1_stop_probability(design, p_true), 6),
            "futility_boundary_f1": futility_boundary(design, p_true, CONFIG),
        }

    # --- minimum N per co-primary, both looks. Unchanged by this amendment:
    # the bars, the alpha split, and the true shares are all untouched, so a
    # difference here would be an arithmetic error, not a design change.
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
            "single_look_min_n_at_alpha_h": min_n_for_power(
                0.5, p_true, ALPHA_H, POWER_TARGET, N_MAX
            ),
        }

    e1_look1 = _int(min_n["E1"]["look1_min_n"])  # type: ignore[index]
    e2_look1 = _int(min_n["E2_1x_floor_share_0.625"]["look1_min_n"])  # type: ignore[index]
    e1_look2 = _int(min_n["E1"]["look2_min_n"])  # type: ignore[index]
    e2_look2 = _int(min_n["E2_1x_floor_share_0.625"]["look2_min_n"])  # type: ignore[index]
    governing_look1 = max(e1_look1, e2_look1)
    governing_look2 = max(e1_look2, e2_look2)

    months = [
        {
            "as_of": end.isoformat(),
            "backfill_pairs_readable": project(end)[0],
            "forward_pairs_readable": project(end)[1],
            "total_pairs_readable": project(end)[2],
        }
        for end in month_ends(today, deadline)
    ]

    look1_date = first_date_reaching(
        readable, governing_look1, today, deadline, ACCRUAL_PER_MONTH, match_rate
    )
    look2_reach = first_date_reaching(
        readable, governing_look2, today, deadline, ACCRUAL_PER_MONTH, match_rate
    )
    look2_date = min(x for x in (look2_reach, deadline.isoformat()) if x)

    scenarios = {
        "achieved_readable_today": project(today)[2],
        "reassigned_cohort_fully_readable": len(pairs),
        f"interim_{CONFIG.interim_deadline}": project(interim)[2],
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
            "E1": design_row(planned_n1(n), n, shares["E1"]),
            "E2": design_row(planned_n1(n), n, shares["E2"]),
            "E2_reported_beside_at_0.600": design_row(
                planned_n1(n), n, shares["E2_at_two_times_share"]
            ),
        }

    futility = {
        "n1_at_the_projected_look1": governing_look1,
        "n2_rule": (
            "the co-primary's registered look-2 minimum N, or the observed n1 where that is "
            "larger - the real n2 is not observable at look 1 (Amendment H2-4 section 4)"
        ),
        "conditional_power_floor": CONFIG.h2_futility_conditional_power,
        "E1": design_row(governing_look1, max(governing_look1, e1_look2), shares["E1"]),
        "E2": design_row(governing_look1, max(governing_look1, e2_look2), shares["E2"]),
    }

    specs = {(s.hypothesis, s.name): s for s in register_specs()}
    gate = fire_hypothesis_section0(
        "H2", [spec_power(specs[("H2", n)], deadline_n, ALPHA_H) for n in ("E1", "E2")], ALPHA_H
    )
    two_look_deadline = {
        "E1": design_row(planned_n1(deadline_n), deadline_n, shares["E1"]),
        "E2": design_row(planned_n1(deadline_n), deadline_n, shares["E2"]),
    }
    governing_power = min(float(two_look_deadline[k]["power"]) for k in ("E1", "E2"))

    # --- the superseded projection, quoted from its recorded artifact ------
    prior = json.loads(SUPERSEDED_REPORT.read_text(encoding="utf-8"))
    prior_dates = prior["projected_look_dates"]
    prior_deadline_n = next(
        m["total_pairs_readable"]
        for m in prior["projection_by_month"]
        if m["as_of"] == CONFIG.projection_deadline
    )
    prior_power = prior["section0_gate_recomputed"]["governing_two_look_power_at_deadline"]

    payload: dict[str, object] = {
        "computed_at": iso_z(now_utc()),
        "amendment": "H2-5 (the tiered control rule); this record is Amendment H2-6",
        "outcome_values_read": 0,
        "inputs": {
            "k": 1,
            "alpha_h": ALPHA_H,
            "alpha_1": CONFIG.h2_alpha_look1,
            "alpha_2": CONFIG.h2_alpha_look2,
            "true_shares": shares,
            "events_in_the_reassigned_cohort": events_total,
            "pairs_assigned": len(pairs),
            "pairs_by_tier": tiers,
            "tier_names": {f"tier_{t}": TIER_NAMES[t] for t in REGISTERED_TIERS},
            "pairs_by_class_pair": dict(sorted(class_pairs.items())),
            "exclusions": exclusions,
            "measured_match_rate_reassigned": round(match_rate, 4),
            "superseded_match_rate_h2_3": round(len(superseded_rows) / events_total, 4),
            "measured_accrual_events_per_month": ACCRUAL_PER_MONTH,
            "today": today.isoformat(),
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
        "against_the_superseded_projection": {
            "source": str(SUPERSEDED_REPORT),
            "note": (
                "quoted from the recorded Amendment H2-4 artifact, never recomputed: a "
                "recomputed superseded number would not be the number the amendment recorded"
            ),
            "look1": {"h2_4": prior_dates["look1"], "h2_5": look1_date},
            "look2": {"h2_4": prior_dates["look2"], "h2_5": look2_date},
            "pairs_at_the_deadline": {"h2_4": prior_deadline_n, "h2_5": deadline_n},
            "governing_two_look_power_at_the_deadline": {
                "h2_4": prior_power,
                "h2_5": round(governing_power, 6),
            },
            "match_rate": {
                "h2_4": 1.0,
                "h2_5": round(match_rate, 4),
            },
        },
        "section0_gate_recomputed": {
            "governing_two_look_power_at_deadline": round(governing_power, 6),
            "single_look_gate": {
                "verdict": gate.verdict.value,
                "governing_power": round(gate.governing_power, 6),
                "rationale": gate.rationale,
            },
            "note": (
                "the Section 0 map is stated on single-look power (Amendment H2-1); the "
                "two-look figure is what governs the amended design and is reported beside "
                "it, per the DEGRADED rule that recomputed power travels with the target"
            ),
        },
    }

    for label, row in boundaries.items():
        if "E1" not in row:
            continue
        for leg in ("E1", "E2", "E2_reported_beside_at_0.600"):
            spent = float(row[leg]["alpha_spent_total"])
            if spent > ALPHA_H + 1e-12:
                raise SystemExit(f"{label}/{leg} spends {spent} > alpha_h {ALPHA_H}; refusing")

    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(payload["inputs"], indent=2, sort_keys=True))
    print(json.dumps(payload["projected_look_dates"], indent=2, sort_keys=True))
    print(json.dumps(payload["against_the_superseded_projection"], indent=2, sort_keys=True))
    print(json.dumps(payload["projection_by_month"], indent=2))
    print(f"governing two-look power at the deadline: {governing_power:.4f}")
    print(f"report -> {REPORT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
