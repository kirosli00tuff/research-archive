# Stage ladder — the register architecture

Status at 2026-08-28: **H1 closed (FAIL, 2026-08-28). Register Stage A in
progress for the successor entries H2, H3, H4.** The single-hypothesis
ladder that carried H1 from registration to closure is archived below the
register ladder; its C and D rows never bound and are void with H1's
closure. In the register architecture every hypothesis climbs its own
ladder, all of them over **one shared collection substrate**
(docs/SUBSTRATE.md), under **one familywise error budget** (alpha_h =
1 − 0.95^(1/k), k fixed by the outcome-blind cull), on **fresh data only**
(the generating-sample quarantine, HYPOTHESES.md rule 1). One
verdict-bearing read per registration. Secondaries never move a row.

## The register ladder, per hypothesis

| stage | question it answers | entry gate | exit gate | capital |
|---|---|---|---|---|
| **Register A — restructure, registration, cull** (in progress) | Which of the co-registered designs is measurable at power on fresh data by 2027-03-31? | Operator register prompt; quarantine pins built and tested before any registration; all three registrations committed before any new network call | Per-hypothesis Section 0 verdicts fired by the A.2 outcome-blind cull: any required co-primary under 50 percent power at achievable N fires BLOCKED; k = survivors; alpha_h fixed and recorded by amendment | none |
| **Register A.3 — arming** (survivors only) | Are the collectors accruing the fresh cohort correctly? | A survivor exists; the re-arm amendment is dated and recorded | Collectors re-armed and verified; watcher assigns pairs at entry; funding recorder and checkpoints running; dark readers reproduce known answers to the digit | none |
| **Per-hypothesis B — the sealed read** (dark until triggered) | Did the registered design clear its bars on its fresh cohort? | That hypothesis's registered trigger: required co-primaries at or above 80 percent power at achieved eligible N; **its own operator prior slot filled**; explicit operator instruction | That hypothesis's registered verdict table, one row fires, applied mechanically at central costs; consequence executed as registered | none |
| **C / D — execution stages** (unregistered) | — | A successor B fires its positive row; operator authorization; a new registration of its own | — | none until a future registration says otherwise |

## The path, dated

- **A.0–A.2** run in this session (2026-08-28): restructure, quarantine,
  three registrations, gap recovery, census refresh, per-hypothesis
  eligibility and power, the cull, the verdicts.
- **A.3** arms only survivors, same session, under a dated amendment.
- **Each surviving hypothesis's earliest Stage B date** is set by its own
  minimum-N against measured accrual and is recorded in the A.4 close-out;
  no successor B runs before its cohort matures and its operator slot fills.
- **Operator-only at every rung:** the priors (one reserved empty slot per
  hypothesis — the assistant never fills any), each Stage B instruction,
  and any authorization beyond measurement.

---

## Archived: the H1 single-hypothesis ladder (closed 2026-08-28)

| stage | question it answered | exit | capital |
|---|---|---|---|
| **A — registration and census** | Is the design measurable at power on this venue? | **GO** fired 2026-08-27: retro N 312, delisting PASS 6/6, powers 1.000 / 0.9993 / 0.9995 against min-N 34 / 103 / 60 | none |
| **B — the sealed read** | Did the registered short clear its bars on the retro cohort? | **FAIL** fired 2026-08-28: P1 lower bound 0.5707 < 0.60; P2 111/312, p = 1.000; P3 114/175, p = 3.8e-05 (PASS). Hypothesis closed, collectors disarmed | none |
| **C — software on paper** (was sketch) | — | Void with the FAIL row; never bound | none |
| **D — live-half** (was sketch) | — | Void with the FAIL row; never bound | none |

The H1 ladder's standing note survives it: equities stay closed at this
stake regardless (HFExperiment A.1b measured IBKR refusing fractional
orders, error 10243).
