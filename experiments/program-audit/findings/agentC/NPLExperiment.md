# NPLExperiment — Agent C findings (referee and verifier)

Repository: `NPLExperiment`
Anchored SHA: `8f1fef83be0f76cbd671c2ce0fbfe8b1c4a5ea2c` (main, 2026-09-02T09:24:43Z)
Live `HEAD` at consolidation: `dff16632eca6eea05b290ade5464339f44c75744` — **exactly one commit ahead of
the anchor**, touching `progress.md` and `registrations/H5/REGISTRATION.md` only.
Agent: **C** (referee; no thesis). Consolidated 2026-09-12.

Inputs merged: `findings/agentC/verification/NPLExperiment.inventory.md`;
`findings/agentC/verification/NPLExperiment.verification.md` and `.claims.json`;
`findings/agentC/provenance/NPLExperiment.md` and `.json`.
Snapshot re-read for this pass: `SNAP/NPLExperiment/` — **every quote below was re-located in the
snapshot at the line cited during consolidation**, and every load-bearing figure was recomputed
first-hand from the tracked artifacts. Live git objects were re-read read-only on
2026-09-12T13:06Z for the post-anchor diff and for the commit dates and file lists of `2d2edc1`,
`f31f7a3`, `f8e54d8`, `546b2e3`, `449ff1e`, `13c6965`, `98e7e01`, `c7bdf64` and `e89b187`; see
**§ Live-repo access log**. Each finding carries a **Consolidation check** line recording what that
re-check found. **Twelve draft findings entered consolidation, one pair merged, none dropped,
eleven leave it.**

Agent C has read nothing under `findings/agentA` or `findings/agentB`.

**One correction to my own earlier passes, recorded before anything else.** The verification pass
wrote that live `HEAD` was "four commits ahead of the anchor"; the provenance pass wrote "one".
`git log --format='%h %cI %s' 8f1fef8..HEAD` (re-read 2026-09-12T13:06:23Z) returns **one commit**,
`dff1663` (2026-09-09T21:46:02−07:00), and `git diff --name-status 8f1fef8 dff1663` returns
`M progress.md` and `M registrations/H5/REGISTRATION.md` — 79 insertions, 0 deletions. The
provenance figure was right. Every "invalidated by later commits?" answer below is re-grounded on
that single diff rather than on either earlier count.

---

## Summary

The deciding machinery of this repository reproduces to the digit. The H1 closure's three
co-primary statistics recompute to 1e-15 from the counts alone, by the repository's own bisection
and independently by `scipy`; the H2 two-look design — minimum N, boundaries, total alpha spends,
powers, futility — is exact; the register cull reproduces to its fixed point; every H5 spend figure
matches the request ledger charge-for-charge (888 = 6 + 323 + 323 + 27 + 209); the 21-module
read-surface hash chain matches the git objects at the read-time commit; and both stored sha256
latch values reproduce byte-for-byte. One block does not. The H5 live/delisted stratum table and
the live touch-spread figure were computed from a census pass (`h5-census-2026-08-28T21:44:11Z`)
that exists in **no git object**, and that table's headline cell — "**0.0 %**" of live instruments
over the 54 bp VIABLE bar, "Every observation above the bar lived in dead markets" — is
contradicted by the repository's own tracked census artifact (1 of 94), by the second forward pass
(2 of 94), and by the **fired** `reports/h5/verdict.json` (3 of 188), which is printed as "1.60 %"
three lines above the "0.0 %" cell in the same document. That sentence is the whole stated
justification for Amendment H5-2, the amendment the program presents as its credibility exhibit.
On provenance, 37 of 43 rows are SUPPORTED, including the registration-before-first-request
ordering (2 min 11 s), the Amendment 3 registration before the reader existed (11 m 23 s), the
`f31f7a3` → `f8e54d8` register-then-implement gap (39 m 20 s) and the never-read H2 latches; two
rows are NOT_SUPPORTED and four PARTIAL. Four figures could not be checked at all, each for a
stated structural reason — the test and `mypy` gate counts (execution is forbidden inside an
audited tree), the A.1 page/hour totals, the H4 trailing-funding median, and one forward
counterfactual about a 30-day census that no data at the anchor can settle. **Eleven findings
leave consolidation: one S1, two S3, eight S4. The S1 is the H5 stratum table; nothing else moves
a verdict, a bar, an alpha, an N target or a cost band.**

---

## Verification scoreboard

### Claims

| Status | Count |
|---|---|
| VERIFIED | **56** |
| CONTRADICTED | **17** |
| UNVERIFIABLE | **4** |
| **Total claim + derived rows audited** | **77** |

Split by kind: **65 claim rows** (47 VERIFIED, 15 CONTRADICTED, 3 UNVERIFIABLE) and **12 derived
quantities** (9 VERIFIED, 2 CONTRADICTED, 1 UNVERIFIABLE). Counted separately below and not in that
table: **5 intervals** (4 VERIFIED, 1 CONTRADICTED) and **15 test-statistic-shaped quantities** (11
VERIFIED, 4 CONTRADICTED). Across all four kinds: **97 items, 71 VERIFIED, 22 CONTRADICTED, 4
UNVERIFIABLE.**

The 22 CONTRADICTED rows resolve into **eight distinct defects**, not twenty-two. Thirteen of them
(C1a, C1b, C1c, C1d, C1e, C1f, C1h, C7, D10, I5, T12, T14, and the live half of the stratum table)
are the **single** H5 census-pass defect counted once per printed cell — finding **-1**, with its
provenance half **-2**. The remaining nine map one-to-one: C5d/C5e/T5 → **-6**; T0/T1/T2 → **-4**;
C11b + the derived accrual row → **-5**; C12b → **-8**; C14b → **-7**; C27 → **-9**; C28 → **-10**.
One CONTRADICTED derived row, **D12** (realized census passes per day after the anchor, 0.80/day
against an assumed 1.00), is **not** a finding: it is post-anchor and the authors falsified and
corrected it themselves in the single post-anchor commit.

**MUST-VERIFY claims (the 7 marked in the inventory), with status:**

| # | Claim | Status |
|---|---|---|
| C1 | the H5 live stratum has "**0.0 %**" over the 54 bp VIABLE bar (median **3.72 bp**, IQR 0.73–7.31, max 51.4 bp, 8.5 % over the floor), and "Every observation above the 54 bp VIABLE bar lives in the delisted stratum." (`docs/H5_ACCESS.md:193,197-198`; `report.md:659`; `HYPOTHESES.md:129`; `DECISIONS.md:497-499`) | **CONTRADICTED** — the tracked `reports/h5/census.rows.json` gives median **4.2137**, IQR 0.7412–9.0865, max **55.6406**, **7/94 = 7.447 %** over the floor and **1/94 = 1.064 %** over the bar (`xyz:URNM` at −55.641 bp, `listing_status = live`); the fired `verdict.json` records `share_over_viable = 0.015957` (3 of 188). The printed row reproduces only from the untracked `…21:44:11Z` pass. Findings **-1** (S1) and **-2** (S3). The **delisted** row of the same table reproduces exactly |
| C2 | the fired H5 PENDING row's deciding figures: **94** with a served reference (bar 20), funding **94 of 94** = 1.000 (bar 0.500), **0** at 30 days of coverage, median absolute basis **4.14 bp** (IQR 0.71–9.15, 9.57 % / 1.60 %) at n = 188 (`report.md:673-676`; `HYPOTHESES.md:126`; `registrations/H5/REGISTRATION.md:567-575`) | **VERIFIED** — all six components exact. 94/94 carry `reference_served` with `reference_field = oraclePx`; `funding_history_state = stored` on 94/94; `covered_days_max = 1`, so 0 meet the 30-day bar; pooled n = 188 gives median 4.14463090419424, q1 0.70947242299609, q3 9.145925118703394, shares 0.09574468085106383 / 0.015957446808510637 — identical to `verdict.json` at 0.0e+00. Bars from `config.py:248-251`; 54 = 3 × `hip3_round_trip_bp[1]` = 3 × 18 |
| C3 | "**29 daily passes needed; projected fire date 2026-09-26.**" (`HYPOTHESES.md:122`; `report.md:685`; `registrations/H5/REGISTRATION.md:587`) | **VERIFIED as arithmetic** — `h5/outcome.py:200-222` gives max(0, 30 − 1) = **29** and 2026-08-28 + 29 d = **2026-09-26** exactly from `covered_days_binding_instrument = 1`. The one-pass-per-day **assumption** is falsified after the anchor (0.80/day over 2026-08-29…09-12, UNANCHORED) and **the authors falsified and corrected it themselves** in `dff1663` (Amendment H5-3, measured 0.77/day, projection → ~2026-10-05, no bar moved). **Not a finding** |
| C4 | the H1 closure: **P1** 197/312 lb **0.5707** vs the 0.60 bar — FAIL; **P2** 111/312 p = **1.000** — FAIL; **P3** 114/175 p = **3.767e-05** — PASS; bands 0.5740 / 0.5707 / 0.5609 (`HYPOTHESES.md:52`; `report.md:222-224`; `REGISTRATION.md:556-568`) | **VERIFIED** — every stored statistic reproduces to 1e-15 from the counts alone, by the repository's own bisection and by an independent closed form: 0.5706880326738533 (`beta.ppf` …36), 0.9999998937952859, 3.766632285793312e-05; bands and the four 90-day secondaries likewise. A separate correction/rule mismatch is recorded at **-4** (S4) and does not move the verdict |
| C5 | H2's governing minimum N, two-look spends, boundaries, powers, futility and look dates (`HYPOTHESES.md:73`; `registrations/H2/REGISTRATION.md:673-730`; `report.md:546-563`) | **SPLIT** — minimum N (42/84/76, 59/117/111, 92/184/169, 169), k₁/k₂ (22/37, 38/69, 43/79), **total** spends (0.037268 / 0.042197 / 0.040343), powers, futility f₁ (31, 27) and the look dates 2026-11-26 / 2027-03-01 all **VERIFIED** exactly; two of the three printed **component** pairs **CONTRADICTED** (finding **-6**). The look dates are verified *given* the accrual constant, itself contradicted at **-5** in the conservative direction |
| C6 | E2's **0.625** true share by linear interpolation, and that at the unchanged 0.60 E2 needs **92/184** and "does not reach 0.80 by the deadline" (`HYPOTHESES.md:74`; `registrations/H2/REGISTRATION.md:675,683-684`) | **VERIFIED** — (0.65 + 0.60)/2 = 0.625 exactly, correctly labelled "a choice, not a measurement"; 92/184 exact; two-look power at n₂ = 135 is **0.692372** and single-look **0.731814**, both under 0.80; the Section 0 gate recomputation (0.888596 / 0.862922) matches to 5e-6 |
| C7 | "Live median touch spread **4.18 bp** (IQR 1.31–10.78)." at n = 94 (`report.md:643`) | **CONTRADICTED** — the tracked artifact's `touch_spread_bp` over the same 94 rows gives median **3.1586 bp**, IQR **1.2270–10.4125**. The printed figures reproduce exactly from the untracked `…21:44:11Z` pass (4.1838; 1.3062/10.7832 nearest-order-statistic). Finding **-2**. Descriptive only — fires nothing |

**Emphasis inside the seven quotes above is this audit's, added to mark the figure under test,
except where the source itself bolds it** (`docs/H5_ACCESS.md:193` and `report.md:659` bold the
`live`, `94`, `3.72 bp` and `0.0 %` cells; `HYPOTHESES.md:122` bolds the passes-and-date sentence;
`report.md:643` bolds "4.18 bp"). No figure or line reference changes either way.

**4 VERIFIED, 2 CONTRADICTED, 1 SPLIT.** The two contradicted MUST-VERIFY claims are the same
defect seen on two sets of cells of the same untracked census pass.

### Intervals

| Metric | Count |
|---|---|
| Intervals audited | **5** |
| Independence doubtful | **1** |
| Recomputed | **5** |
| Conclusion moved | **0** |

**No two-sided confidence interval appears anywhere in this repository.** Every "interval" is
either a one-sided **exact Clopper–Pearson lower bound** or an **IQR**, which is a dispersion
summary and not an interval estimate. There is no asymptotic statistic, no bootstrap, no
regression and no variance estimator in `src/npl`.

- **I1** — P1 lower bound 0.5707 (197/312) at `alpha_adj`, bar 0.60. Estimator read from code:
  exact Clopper–Pearson one-sided lower bound by 200-step bisection on P(X ≥ s | p),
  `src/npl/verdict.py:67-82`. **Independence assumed** (one Bernoulli per event).
  **Independence doubtful: yes, and this is the one row so counted** — the 312 listing events are
  one draw per instrument-event and are *not* repeated within instrument, but they share calendar
  time, so a market-wide regime inside the 30-day windows would induce cross-sectional dependence;
  no clustering by dex or by month is applied. Reproduces exactly (bisection 0.5706880326738533 =
  stored; `beta.ppf(alpha, 197, 116)` = 0.5706880326738536). **VERIFIED.**
- **I2** — the three cost-band bounds (198/197/194 of 312). Three deterministic re-scorings of the
  *same* 312 events, so perfectly dependent — and correctly presented as a sensitivity, not as
  three tests. All three reproduce to 1e-15. **VERIFIED.**
- **I3** — P1 at 90 days, 0.6069 (208/312). Nests the 30-day window on the same events, so heavily
  dependent on I1, and correctly labelled a named secondary that is never verdict-bearing
  (`REGISTRATION.md:223-226`; `verdict.py:150-189`). Reproduces exactly. **VERIFIED.**
- **I4** — the registered levels themselves (Šidák `alpha_adj` = 1 − 0.95^(1/3) = 0.016952247…,
  `alpha_h` = 1 − 0.95^(1/k)). Arithmetic; reproduces exactly. **VERIFIED** as arithmetic — whether
  the correction matches the rule it feeds is a *tests* question, answered at T0.
- **I5** — every IQR printed in H5. Not an interval estimate and correctly never used as one. The
  n = 188 sample is **94 instruments × 2 snapshots taken 8 minutes apart**, which the repository
  discloses in the same line that reports it ("**188** (94 instruments × 2)",
  `registrations/H5/REGISTRATION.md:572`) and on which it computes **no test statistic, no p-value
  and no confidence interval** — so the repeated-measure structure feeds no inference and is not
  counted as doubtful independence. The n = 188 IQR reproduces exactly; the stratum IQRs at
  `docs/H5_ACCESS.md:193,195` do not (findings **-1**, **-2**), and they also use a
  nearest-order-statistic convention rather than the repository's own linear-interpolated
  `h5/stats.py:29-42`. **CONTRADICTED.**

"Recomputed" = 5 means all five were re-derived first-hand from the stored counts. **No interval
was recomputed under an alternative dependence structure**, and the reason is stated rather than
elided: for I1 a within-unit clustered bound is undefined (no instrument contributes two events)
and a calendar-block bootstrap would need per-event entry dates, which no tracked artifact holds —
see **§ Could not be checked**. **Conclusion moved: 0** — and for I1 the direction is knowable
anyway: a block correction widens the bound away from the 0.60 bar it already fails.

### Tests

| Metric | Count |
|---|---|
| Tests audited | **15** |
| Tail mismatch | **0** |
| Dof issue | **0** |
| Correction mismatch | **3 rows, 1 distinct defect** |

**Tails.** Every test in the repository is one-sided in the direction its registration states, and
the registrations state the direction explicitly — P3's twice, in both sign conventions, "so no
sign error can creep in" (`REGISTRATION.md:213-222`). **No tail mismatch anywhere.**

**Dof.** Every test is an **exact binomial**; none has a degrees-of-freedom parameter, and the H2
look-2 spend is computed exactly over the independent increment Bin(n₂ − n₁, ½) rather than by an
asymptotic spending function. **No dof issue is possible, and none was found.**

**Corrections.** Nine of the fifteen rows carry a correction and eight of the nine match the rule
they feed: the H2 alpha split 0.02 + 0.03 = `alpha_h` is **across looks**, which is the correct
device for a sequential rule, with no Šidák across the two required co-primaries (`cull.py:39`
`"H2": "all"`); H4's Šidák across three threshold cells feeds `"H4": "any"`, a **union** rule,
which is exactly what Šidák is for; and the cull's `alpha_h` = 1 − 0.95^(1/k) across the k
surviving hypotheses feeds a union across hypotheses. The mismatch is **T0/T1/T2 — one defect
counted on three rows**: a Šidák (union-type) correction attached to
`all_co_primaries_pass = p1 and p2 and p3` (`verdict.py:201`), an all-must-pass
intersection-union rule that needs no correction at all. Finding **-4**; recomputed at an
uncorrected 0.05 the H1 FAIL does not move. Four rows are CONTRADICTED on their *values* rather
than their correction: T5 on the printed component spends (**-6**), T12 and T14 on the H5 stratum
and touch-spread summaries (**-1**, **-2**).

### Provenance

| Status | Count |
|---|---|
| SUPPORTED | **37** |
| NOT_SUPPORTED | **2** |
| PARTIAL | **4** |
| UNVERIFIABLE | **5** |

43 rows were dispositioned: **23 registration claims** (19 SUPPORTED, 3 PARTIAL, 1 NOT_SUPPORTED)
and **20 parameter/rule changes** (18 SUPPORTED, 1 PARTIAL, 1 NOT_SUPPORTED). The 5 UNVERIFIABLE
are the items in **§ Could not be checked** that are provenance questions rather than claim rows;
a sixth entry in that section of the provenance pass ("anything under `findings/agentA` or
`findings/agentB`") is a scope note, not a claim, and is not counted here.

**NOT_SUPPORTED (2):** the operator-prior slot fill (finding **-3**) and `report.md:446`'s
07:51:10Z precondition timestamp (finding **-9**).

**PARTIAL (4):** the 22:20Z fire time, corrected by the authors but not propagated to two summary
documents (**-10**); the reconnaissance probe's 21:41Z charge time against a ledger that stamps it
21:39:45–48Z (**-11**); Amendment H5-1's "no census had been run" (corroborated by the
`listing_status` field boundary between the two passes and by `rows_skipped_pre_amendment = 273`,
but pinned only to the commit at 21:59:42Z — **not a finding**, nothing contradicts it); and
PC-15, the same amendment's firing-order change (dated, reasoned, restrictive direction verified —
**not a finding**).

**What SUPPORTED means here, in the load-bearing cases.** The registration precedes the first
network call by 2 m 11 s (`cd640b6` at 00:54:38Z; first ledger charge 00:56:49Z). Amendment 3, the
Stage B verdict table, was committed 11 m 23 s before `stageb/reader.py` first existed and 11 m
49 s before the single read. Amendment H2-3 was committed at `f31f7a3` with **no source file in
the commit** and implemented 39 m 20 s later at `f8e54d8` — git proves register-then-implement
outright. The H5 registration, the 198-entry exact-string mapping and the session calendar were
committed with **zero H5 requests sent** (last charge before 21:38:58Z is 21:05:53Z; first H5
charge 21:39:45Z), and `git log --follow` on `resolution.py` and `calendar.py` returns that one
commit each — byte-frozen through the anchor. The latch and artifact sha256 values at
`HYPOTHESES.md:54` reproduce digit-for-digit, the latch holds 21 module hashes, and all 21 match
`git show 32b3f9e:src/npl/<mod>` and `844f7c2:<mod>`. `family_confidence = 0.95` enters at
`77ee522` and is never touched again. Every registration file is **pure insertion** (deletions = 0)
with exactly two mechanical exceptions, one of which is the prior-slot fill itself.

### Merge and de-duplication record

| Draft | Origin | Disposition |
|---|---|---|
| DRAFT-V-1 | verification §5 | → **AUDIT-C-NPLExperiment-1**, unchanged |
| DRAFT-V-2 | verification §5 | → **-2**, unchanged |
| DRAFT-P-1 | provenance §5 | → **-3**, unchanged |
| DRAFT-V-4 | verification §5 | → **-4**, unchanged |
| DRAFT-V-5 | verification §5 | → **-5**, unchanged |
| DRAFT-V-3 | verification §5 | → **-6**, unchanged |
| DRAFT-V-6 | verification §5 | → **-7**, disclosure field re-graded (see below) |
| DRAFT-V-7 | verification §5 | → **-8**, unchanged |
| DRAFT-V-8 | verification §5 | **merged** with DRAFT-P-2 → **-9**; its second half (the 22:20Z parallel case) routed to **-10** |
| DRAFT-P-2 | provenance §5 | **merged** with DRAFT-V-8 → **-9** |
| DRAFT-P-3 | provenance §5 | → **-10**, label re-graded DERIVED → **READ** (see below) |
| DRAFT-P-4 | provenance §5 | → **-11**, unchanged |

**Twelve drafts in, one merge, eleven findings out. Nothing was dropped.** All twelve carry a
verbatim quote that re-locates in `SNAP/NPLExperiment/` at the line cited, and all twelve carry a
figure that recomputed here — so the "drop any without a locatable quote and figure" rule removed
nothing, and **no drop is recorded because none was warranted**.

Four reconciliations were required.

1. **The merge.** DRAFT-V-8 and DRAFT-P-2 challenge the same sentence, `report.md:445-447`. They
   agreed on severity (S4), direction (neutral) and label (DERIVED) and differed on class —
   V-8 said `INTERNAL_INCONSISTENCY`, P-2 said `PROVENANCE`. Resolved to **PROVENANCE**: the
   defect is a timestamp on a provenance record whose only function is to establish an ordering.
   The provenance draft's evidence is the fuller of the two (four sources, plus the timezone
   argument) and is carried whole; V-8's second half, the 22:20Z parallel case, was already its own
   provenance draft and becomes **-10** rather than being duplicated inside **-9**.
2. **Label of -10.** DRAFT-P-3 was labelled DERIVED. The limitation it raises — that the fire time
   printed in the two summary documents is wrong — **is disclosed by the authors verbatim**
   (`registrations/H5/REGISTRATION.md:632-639`; `progress.md:1494-1496`), so under the audit rules
   the finding is **READ**, capped at S3, and must say plainly that the authors disclosed it and
   where. It does. Severity stays S4, which is inside the cap.
3. **Disclosure field of -7.** DRAFT-V-6 recorded "disclosed: partially" because
   `docs/H5_ACCESS.md:152-154` states the dex split correctly. Re-graded to **not disclosed**: a
   second document stating the right figure is *evidence of the inconsistency*, not a disclosure of
   it — no document flags the summary-table cell as wrong. The correct statement is retained inside
   the evidence, where it belongs. Severity (S4) and label (DERIVED) unchanged.
4. **Direction vocabulary.** COMMON_RULES enumerates two directions, A and B. Findings **-2**,
   **-6**, **-7**, **-8**, **-9**, **-10** and **-11** are recorded as `neutral`, which is outside
   that enumeration. This is a deliberate, flagged deviation: each is a provenance or hygiene
   defect whose corrected reading moves the repository's position in *neither* direction, and
   forcing A or B on them would assert a direction the evidence does not support. Where a direction
   applies it is given: **-1** and **-3** are A (the corrected reading makes a closure or a gate
   weaker than labelled), **-4** is A (the correction makes the fired FAIL easier to reach), **-5**
   is B (the printed accrual overstates nothing but is labelled with the wrong n, and the
   corrected rate is *higher*, i.e. the stated look dates are conservative).

---

## Findings

Eleven. Ordered by descending severity. **-1** is the only finding that touches a stated
conclusion; the other ten say explicitly what they do not move.

### AUDIT-C-NPLExperiment-1
- **Repository / SHA:** NPLExperiment / `8f1fef83be0f76cbd671c2ce0fbfe8b1c4a5ea2c`
- **Hypothesis or artifact:** H5, the HIP-3 equity-style basis feasibility entry — the live/delisted
  stratum table and the Amendment H5-2 rationale it carries
- **Direction:** A — the corrected reading is that a live instrument *did* sit above the VIABLE bar,
  so the universe rule that removed the delisted stratum did not remove every over-bar observation
- **Class:** INTERNAL_INCONSISTENCY
- **Severity:** S1 — a stated conclusion ("every observation above the bar lived in dead markets")
  is contradicted by the repository's own tracked artifact and by its own fired verdict
- **Label:** DERIVED (tracked JSON artifacts, the repository's own summarizer, and the request ledger)
- **Claim challenged (verbatim):** "**Every observation above the 54 bp VIABLE bar lives in the
  delisted / stratum.**" — NPLExperiment/docs/H5_ACCESS.md:197-198; "| **live** | **94** | **3.72
  bp** | 0.73 – 7.31 | 51.4 bp | 8.5 % | **0.0 %** |" — NPLExperiment/docs/H5_ACCESS.md:193 and
  NPLExperiment/report.md:659; "the delisted stratum is where **every** observation above the 54 bp
  bar lived: median 30.5 bp with 45.6 % over the bar, against 3.72 bp and **0.0 %** for live
  instruments in the same snapshot." — NPLExperiment/HYPOTHESES.md:129; "0.0 percent** for live
  instruments in the same snapshot. **Every observation / above the bar lived in dead markets.**" —
  NPLExperiment/DECISIONS.md:498-499
- **Evidence:**
  - The repository's only tracked per-instrument basis artifact, `reports/h5/census.rows.json`
    (273 rows, every one stamped `snapshot_id = h5-census-2026-08-28T21:51:54Z`), gives for the 94
    rows with `resolution_state = "resolved"` and `listing_status = "live"`: median **4.2137 bp**
    (printed 3.72), q1/q3 **0.7412 / 9.0865** (printed 0.73–7.31), max **55.6406 bp** (printed
    51.4), **7/94 = 7.447 %** over the 18 bp floor (printed 8.5 %) and **1/94 = 1.064 %** over the
    54 bp bar (printed **0.0 %**).
  - The single observation over the bar is `xyz:URNM` at `basis_bp = −55.6406`, with
    `listing_status = "live"` and `is_delisted = false` — a **live** instrument above the bar,
    which is precisely what the universal sentence denies.
  - The repository's own **fired** artifact records the same thing on the post-Amendment-H5-2 live
    universe: `reports/h5/verdict.json` → `inputs.by_session_tag.extended.share_over_viable =
    0.015957446808510637` = **3 of 188**.
  - That figure is printed **three lines above** the "0.0 %" cell, at `HYPOTHESES.md:126` ("**1.60
    %** over the 54 bp bar", n = 188), and again at `registrations/H5/REGISTRATION.md:574` ("9.57 %
    / **1.60 %**").
  - The second forward pass in the working tree (`data/h5/snapshots.jsonl`, snapshot
    `h5-census-2026-08-28T22:00:14Z`, UNANCHORED, read 2026-09-12T12:36Z) gives live median 4.1404
    bp, max **63.29 bp**, **2/94 = 2.128 %** over the bar.
  - The printed table **does** reproduce, to the last printed digit, from a **third** census pass
    that is in no git object: `h5-census-2026-08-28T21:44:11Z`, present only in the gitignored
    `data/h5/census.jsonl`. That pass gives live n = 94, median **3.7227**, max **51.3919**, **8/94
    = 8.511 %** over 18 bp, **0/94 = 0.000 %** over 54 bp. The request ledger confirms it was a full
    323-request census pass (charge positions 2954–3276 on 2026-08-28, 21:44:11–21:47:56Z), eight
    minutes before the pass the tracked artifact records.
  - The **delisted** row of the same table (57 / 30.5174 / 0.0000–210.7909 / 2,480.97 / 54.386 % /
    45.614 %) reproduces **exactly** from both passes — a dead market's mark is frozen, so its basis
    does not move between passes. Only the live row moves, and it moves across the bar.
  - Why it matters: the sentence is the whole stated justification for **Amendment H5-2**, which
    the program presents as its credibility exhibit ("**The amendment deleted this entry's only
    route to VIABLE**", `report.md:662-665`).
- **Recomputation:** inputs `reports/h5/census.rows.json` (273 rows) and `reports/h5/verdict.json`;
  method — the repository's own `src/npl/h5/stats.py:64-88` `summarize` re-implemented verbatim
  (median, linear-interpolated quartiles, `sum(m > bar)/n`) over `abs(basis_bp)`; scripts
  `/home/kiros-li/.cache/program-audit/scratchpad/work/agentC-npl/c1_recompute.py`, `c1_2144.py`,
  `c1_snap2.py`, `c2_pool.py`, re-run at consolidation in `…/work/agentC-npl-consol/`. Result:
  n = 94, median 4.2137, q1 0.7412, q3 9.0865, max 55.6406, `share_over_floor` 0.074468,
  `share_over_viable` **0.010638**. Pooled with the forward snapshot the shares reproduce
  `verdict.json` to **0.0e+00**. Tolerance: exact on integer counts, 0.01 bp on medians.
- **What would resolve it:** commit the `h5-census-2026-08-28T21:44:11Z` rows and state in
  `docs/H5_ACCESS.md` and `report.md` which pass each stratum figure is computed from; and replace
  the universal sentence with a snapshot-scoped one, or re-derive the table from the census artifact
  of record — in which case the live cell reads 1.06 % (or 1.60 % pooled), not 0.0 %.
- **Confidence:** HIGH — the contradicting figure is in the repository's own fired artifact and is
  printed three lines away in the same document table.
- **Invalidated by later commits?:** **no.** The single post-anchor commit `dff1663` touches
  `progress.md` and `registrations/H5/REGISTRATION.md` only; `docs/H5_ACCESS.md`, `report.md`,
  `HYPOTHESES.md`, `DECISIONS.md` and `reports/h5/*` are byte-identical at the anchor and at live
  `HEAD`.
- **Disclosed by authors?:** **no.** `report.md:635-637` asserts the two census passes returned
  "**identical** counts" — true of counts — and presents the stratum table immediately afterwards
  without saying which pass produced it. No document in the repository names the `21:44:11Z` pass.
- **Consolidation check:** re-verified first-hand from `SNAP`. All four quotes re-located at the
  lines cited (`docs/H5_ACCESS.md:193`, `:197-198`; `report.md:659`; `HYPOTHESES.md:129`;
  `DECISIONS.md:498-499`). Recomputed at consolidation: live n = 94, median 4.2137, q1 0.7412,
  q3 9.0865, max 55.6406, 7/94 over floor, 1/94 over bar, the over-bar row `xyz:URNM` at
  −55.64056196967594 with `listing_status = live`; delisted 57 / 30.5174 / 0.0000–210.7909 /
  2480.9714 / 54.386 % / 45.614 %; all-resolved 151 / 4.6310 / 19.2452 / 25.166 % / 17.881 %;
  `verdict.json` `share_over_viable` = 0.015957446808510637 and `fired_at` 22:04:30Z; every row's
  `snapshot_id` is the single value `h5-census-2026-08-28T21:51:54Z`. **No correction.**

### AUDIT-C-NPLExperiment-2
- **Repository / SHA:** NPLExperiment / `8f1fef83be0f76cbd671c2ce0fbfe8b1c4a5ea2c`
- **Hypothesis or artifact:** H5 — the "What the venue actually serves" block and the stratum table:
  the descriptive figures are computed from a census pass that is in no git object, while the
  committed census artifact is a different pass
- **Direction:** neutral — the corrected figures move the live stratum's dispersion in both
  directions at once (median down for touch spread, up for basis) and decide nothing
- **Class:** PROVENANCE
- **Severity:** S3 — the source of a published block of figures is not in the repository
- **Label:** DERIVED (tracked artifacts, the untracked census file, and a commit date)
- **Claim challenged (verbatim):** "Two full census passes, 323 requests each, returning
  **identical** counts, / plus a 6-request reconnaissance probe. `docs/H5_ACCESS.md` carries the /
  verbatim fragments." — NPLExperiment/report.md:635-637; and "| Is there a book? | Two-sided on 94
  of 94 live; empty on all 57 delisted. Live median touch spread **4.18 bp** (IQR 1.31–10.78). |" —
  NPLExperiment/report.md:643
- **Evidence:**
  - The tracked census artifacts name exactly one pass: `reports/h5/census.json:snapshot_id =
    h5-census-2026-08-28T21:51:54Z`, and all 273 rows of `reports/h5/census.rows.json` carry that
    same id (a `set()` over the rows at consolidation returns one value). The `21:44:11Z` pass has
    **no tracked artifact**.
  - Touch spread from the tracked artifact (94 present values, all on `resolved`+`live` rows):
    median **3.1586 bp**, IQR **1.2270 – 10.4125**. From the untracked `21:44:11Z` pass: median
    **4.1838**, and under a nearest-order-statistic convention q1/q3 = **1.3062 / 10.7832** — i.e.
    exactly the printed "4.18 bp (IQR 1.31–10.78)".
  - Same for the all-resolved row at `docs/H5_ACCESS.md:195` ("151 | 4.14 bp | 0.00 – 18.13 | 2,481
    bp | 25.8 % | 17.2 %"): the tracked artifact gives **4.6310 / 0.0000–19.2452 / 25.166 % /
    17.881 %** (re-verified at consolidation); the `21:44:11Z` pass gives 4.1402 / 0.0000–18.10 /
    25.828 % / 17.219 %.
  - The printed quartiles also use a different convention from the repository's own
    `src/npl/h5/stats.py:29-42`, documented there as "linear-interpolated … the numpy default,
    written out". The printed 0.73 / 7.31 / 10.78 / 18.13 are nearest-order-statistic values; the
    linear values on the same pass are 0.7576 / 7.3007 / 10.5706 / 18.0993.
  - `docs/H5_ACCESS.md` was added in commit `13c6965` at 2026-08-28T21:59:42Z — after both census
    passes and before the 22:00:14Z forward pass — so which pass it summarizes was a choice
    available to the author, not a timing accident.
  - Nothing verdict-bearing rests on this block: the fired row's own figures (n = 188 median
    4.14463090419424, shares 0.09574 / 0.01596) reproduce exactly from the tracked artifact pooled
    with the forward snapshot.
- **Recomputation:** inputs `data/h5/census.jsonl` (546 JSON lines, two snapshot ids, UNANCHORED,
  read 2026-09-12T12:36Z) and `reports/h5/census.rows.json`; method — `h5/stats.py`'s summarizer
  plus all 13 `numpy.quantile` methods, to identify the convention; scripts
  `/home/kiros-li/.cache/program-audit/scratchpad/work/agentC-npl/c1_2144.py` and `c7_quant.py`;
  touch-spread and all-resolved rows re-run at consolidation. Tolerance 0.01 bp.
- **What would resolve it:** commit the `21:44:11Z` rows (or re-derive the block from
  `census.rows.json`), and state the quantile convention in the documents so it matches
  `h5/stats.py`.
- **Confidence:** HIGH — the source pass is identified positively: every printed figure of the block
  matches it to the last digit, and no other filter or convention over the tracked artifact
  reproduces them.
- **Invalidated by later commits?:** no — `report.md` and `docs/H5_ACCESS.md` are unchanged from the
  anchor to live `HEAD`.
- **Disclosed by authors?:** **no.** The nearest statement, `report.md:635-637`, says the two passes
  returned "identical" counts and does not say which pass the figures come from.
- **Consolidation check:** re-verified first-hand. Both quotes re-located at `report.md:635-637` and
  `:643`. Recomputed at consolidation: touch-spread median 3.1586 / IQR 1.2270–10.4125 on the
  tracked artifact; all-resolved 4.6310 / 0.0000–19.2452 / 25.166 % / 17.881 %; one `snapshot_id`
  across all 273 rows; `census.json:snapshot_id` = `h5-census-2026-08-28T21:51:54Z`. **No
  correction.**

### AUDIT-C-NPLExperiment-3
- **Repository / SHA:** NPLExperiment / `8f1fef83be0f76cbd671c2ce0fbfe8b1c4a5ea2c`
- **Hypothesis or artifact:** H1 (H-NPL) Section 13 operator prior slot — the registered structural
  block on the single Stage B read
- **Direction:** A — the read that produced the CLOSED/NEGATIVE verdict is presented as gated by an
  operator condition that was in fact satisfied by the assistant, with the assistant's own number
- **Class:** PROVENANCE
- **Severity:** S3 — capped there by the authors' partial disclosure (see below)
- **Label:** DERIVED (git object `2d2edc1`, plus the verbatim-logged operator prompts)
- **Claim challenged (verbatim):** "are context, not the operator's number, and they must not be
  copied into the / slot below." — NPLExperiment/REGISTRATION.md:282-283. The slot four lines later
  reads: "> Operator prior on the Stage B bars clearing: 0.40 (adopted)" —
  NPLExperiment/REGISTRATION.md:287
- **Evidence:**
  - The assistant's own recorded prior is **0.40**: "- 0.40 that the Stage B bars clear on the
    registered sample." — NPLExperiment/REGISTRATION.md:277; and `src/npl/config.py:205` carries
    `assistant_prior_stage_b=0.40` from the init commit onward. The slot was filled with that
    identical number.
  - The Stage A.0 operator prompt, **logged verbatim** under the repository's own standing rule 1:
    "The NPD Amendment 0 lesson applies: an adopted prior corrupts the calibration ledger. **The
    operator prior slot stays empty. Do not fill it.**" — NPLExperiment/progress.md:33.
  - The Stage B.0 prompt, logged verbatim the next day, repeats it: "On an empty or malformed slot,
    stop the entire stage, report BLOCKED-ON-OPERATOR with the accepted format, push the report,
    end. **Never fill it.**" — NPLExperiment/progress.md:395.
  - `git show --name-status 2d2edc1` (committer date 2026-08-27T12:30:34−07:00 = **2026-08-27T19:30:34Z**,
    subject "docs+tests: operator prior 0.40 (adopted), written by assistant on operator instruction
    2026-08-27") touches exactly two files: `M REGISTRATION.md` and `M tests/test_registration_check.py`.
    It does **not** touch `progress.md`, and `progress.md` at the anchor has **no entry at all**
    between `## 2026-08-27T09:20Z` (line 315) and `## 2026-08-28T02:31:22Z` (line 376) — so the
    operator instruction said to authorise the fill is nowhere logged verbatim, which standing
    rule 1 requires.
  - No amendment records the departure. `REGISTRATION.md`'s amendment log runs 1, 2, 3, 4; none
    mentions the prior slot except Amendment 4 §5, which merely notes it is filled.
    `grep -c -i "prior" DECISIONS.md` returns **0** — there is no ADR on it.
  - The same commit rewrote the pin that had enforced the empty state
    (`test_the_real_registration_slot_is_still_empty_and_blocks_stage_b` →
    `test_the_real_registration_slot_is_filled_0_40_adopted`), preserving the refusal only on a
    `tmp_path` fixture.
  - The gate is load-bearing by the repository's own words: "**The empty slot blocks Stage B
    structurally**" — NPLExperiment/REGISTRATION.md:290-291; and `report.md:126-127` records it
    passing as a Stage B precondition.
- **Recomputation:** none required — the finding is an ordering and identity fact over git objects
  and quoted lines. Every component was re-read first-hand at consolidation: the commit's
  `--name-status`, the two `progress.md` prompt lines, the absence of an intervening `progress.md`
  entry, `config.py:205`, and the zero grep hit in `DECISIONS.md`.
- **What would resolve it:** the operator instruction of 2026-08-27 logged verbatim in `progress.md`
  as standing rule 1 requires, plus a numbered amendment in `REGISTRATION.md` recording that the
  Section 13 prohibition at :282-283 was set aside, by whom, on what instruction, and with what
  effect on the calibration ledger.
- **Confidence:** HIGH — the prohibition, the fill, the identity of the number, the missing prompt
  log and the absence of an amendment are each a single quoted line or a single git object.
- **Invalidated by later commits?:** no — `REGISTRATION.md` is unedited after `77ee522` and is
  untouched by the single post-anchor commit.
- **Disclosed by authors?:** **partly, and that is what caps this at S3.** The adoption and the
  assistant's authorship are stated twice — "The Section 13 prior / slot was filled 0.40 (adopted)
  on operator instruction dated 2026-08-27" (NPLExperiment/report.md:85-86) and "the Section 13 slot
  is filled — 0.40 (adopted), / written by the assistant on operator instruction 2026-08-27"
  (NPLExperiment/report.md:126-127). What is **not** disclosed anywhere is that this is the exact
  act `REGISTRATION.md:282-283` forbids, or that the authorizing instruction was never logged. The
  authors' own later practice reads as a correction: the H5 registration, written the next day,
  strengthens the wording to "must not be copied into the slot below. **The assistant never fills
  the slot.**" (NPLExperiment/registrations/H5/REGISTRATION.md:345-346) — a sentence absent from
  H2's, H3's and H4's otherwise identical paragraphs.
- **Consolidation check:** re-verified first-hand. Quotes re-located at `REGISTRATION.md:282-283`,
  `:287`, `:277`, `:290-291`; `progress.md:33`, `:395`; `report.md:85-86`, `:126-127`;
  `registrations/H5/REGISTRATION.md:345-346`. `git show --name-status 2d2edc1` re-read
  2026-09-12T13:06Z: two files, no `progress.md`. `progress.md` headings at lines 315 and 376
  confirmed adjacent. `grep -c -i prior DECISIONS.md` = 0. **One presentation correction:** the
  verification-stage draft rendered part of the `REGISTRATION.md:282` quote in bold; the source
  carries no emphasis there, and the quote is now verbatim. No figure, line or conclusion changes.

### AUDIT-C-NPLExperiment-4
- **Repository / SHA:** NPLExperiment / `8f1fef83be0f76cbd671c2ce0fbfe8b1c4a5ea2c`
- **Hypothesis or artifact:** H1 — Section 8 inference: the multiplicity correction and the decision
  rule it feeds
- **Direction:** A — the correction makes the conjunction harder to pass, i.e. makes the FAIL that
  H1 fired easier to reach
- **Class:** STATISTICAL
- **Severity:** S4 — the pairing is wrong in principle; at these counts it moves nothing
- **Label:** DERIVED (registration text against implemented code, with the consequence recomputed)
- **Claim challenged (verbatim):** "Three co-primaries, distribution-free, one-sided, at /
  **alpha_adj = 1 − 0.95^(1/3) = 0.016952 (0.0170)** each. **All three must / pass for the Stage B
  GO row.**" — NPLExperiment/REGISTRATION.md:200-202
- **Evidence:**
  - The decision rule is implemented as a conjunction:
    `all_co_primaries_pass=p1.passes and p2.passes and p3.passes` —
    NPLExperiment/src/npl/verdict.py:201.
  - A Šidák correction is a **union**-type adjustment: it controls the probability that *at least
    one* of several tests rejects. Under an all-must-pass (intersection-union) rule the GO decision
    rejects only when **every** component rejects, so its type-I error under any configuration in
    which at least one component null is true is bounded by the **largest** per-component level;
    no correction is required. Applying Šidák makes each component strictly harder, and the GO
    strictly harder, than the registered family-wise budget requires.
  - The same repository applies the correct reasoning to its successor hypotheses: "H2 and H3
    require every co-primary (the weakest governs); H4's grid is disjunctive within the hypothesis
    (Sidak-corrected), so its best cell governs" — NPLExperiment/src/npl/register/cull.py:18-20,
    implemented at `cull.py:135-144`. No within-hypothesis correction is applied to H2's two
    required co-primaries; Šidák is applied only to H4's union of three cells
    (`register/conditioning.py`, `registrations/H4/REGISTRATION.md:79-80`). **H1 is the only place
    in the program where a union correction is attached to a conjunction.**
  - The row that fired is `row_fired = "FAIL"` (`reports/stage_b/read.json`), so the conservatism
    runs toward the outcome that was recorded.
- **Recomputation:** inputs `reports/stage_b/read.json:co_primaries` (197/312, 111/312, 114/175);
  method — re-run each component at an uncorrected alpha = 0.05 using `verdict.py:clopper_pearson_lower`
  and `power.py:upper_tail`, cross-checked against `scipy.stats.beta.ppf` and `scipy.stats.binom.sf`;
  script `/home/kiros-li/.cache/program-audit/scratchpad/work/agentC-npl/misc.py`, re-run at
  consolidation. Result: **P1 lower bound rises 0.5706880326738533 → 0.5840855403520515, still below
  the 0.60 bar → FAIL; P2 p = 1.000000 → FAIL; P3 p = 3.767e-05 → PASS. The H1 verdict does not
  move.** Tolerance 1e-6 (the stored statistics themselves reproduce to 1e-15).
- **What would resolve it:** stating in Section 8 that `alpha_adj` is deliberately conservative for
  an intersection-union rule — and therefore that the registered family-wise budget is not binding —
  or testing each co-primary at 0.05 as an IUT permits. Either way the 2026-08-28 FAIL stands.
- **Confidence:** HIGH on the mismatch and on the recomputation; the practical consequence is nil at
  these counts, which is why this is S4.
- **Invalidated by later commits?:** no — `REGISTRATION.md` Section 8 and `src/npl/verdict.py` are
  unchanged post-anchor, and the single H1 read is spent and latched.
- **Disclosed by authors?:** **no** — no document discusses the conservatism of a union correction
  under an all-must-pass rule.
- **Consolidation check:** re-verified first-hand. Quote re-located at `REGISTRATION.md:200-202`;
  `verdict.py:201` re-read; `cull.py:18-20` re-read; `read.json` re-read (`row_fired = FAIL`,
  `alpha_adj = 0.016952427508441503`); the uncorrected P1 bound recomputed independently with
  `scipy.stats.beta.ppf(0.05, 197, 116) = 0.5840855403520515`. **No correction.**

### AUDIT-C-NPLExperiment-5
- **Repository / SHA:** NPLExperiment / `8f1fef83be0f76cbd671c2ce0fbfe8b1c4a5ea2c`
- **Hypothesis or artifact:** H2 — the A.1-measured accrual constant that drives the pair projection
  and the projected look dates
- **Direction:** B — a measured rate is printed with an n that does not produce it
- **Class:** ARITHMETIC
- **Severity:** S4 — immaterial, and the error runs in the conservative direction
- **Label:** DERIVED (the consuming script's own constants, plus a count over the census store)
- **Claim challenged (verbatim):** "Accrual re-measured at **18.57 events/month** (n = 113 /
  listings/182d) — the carried 18.5 confirmed" — NPLExperiment/report.md:340-341; and "# A.1 measured
  accrual, trailing 182 days, n = 113 events. / ACCRUAL_PER_MONTH = 18.57" —
  NPLExperiment/scripts/ktable_amended.py:48-49
- **Evidence:**
  - The script that consumes the constant fixes its own month length one line later:
    `DAYS_PER_MONTH = 30.44` — NPLExperiment/scripts/ktable_amended.py:50. With the claim's own
    stated inputs, 113/182 × 30.44 = **18.899**, not 18.57; at a 30-day month it is 18.626.
  - **18.57 corresponds to n ≈ 111.0** over 182 days — the 113 listings less the two the same
    paragraph explicitly excludes ("one new: io:EWY, delisted at birth, never an event; one /
    relist: xyz:XBI", NPLExperiment/report.md:339-340). The label "n = 113 listings" is therefore the
    wrong n for the rate printed beside it.
  - The **main-dex** figure in the same sentence *does* reproduce under a 30.44-day month:
    3/182 × 30.4375 = 0.5017 → "0.5/month (n = 3)" (`report.md:341-342`), so the two halves of the
    sentence use different effective n.
  - n = 113 itself is correct: counting `data/census/census.jsonl` rows whose `first_1d_open_ms`
    falls in the 182 days before 2026-08-27 gives exactly **113**, of which 3 are main-dex.
  - No artifact under `reports/` records the accrual measurement; the figure exists only as a
    hard-coded constant.
- **Recomputation:** inputs `data/census/census.jsonl` (505 rows, UNANCHORED, read
  2026-09-12T12:44Z) and `scripts/ktable_amended.py:48-54`; method — count listings in the trailing
  window, divide by 182, multiply by the script's own `DAYS_PER_MONTH`, then re-run the projection
  at both rates; scripts `accrual2.py` and `misc.py` in the work dir. Result: measured **18.899**
  against the stated 18.57 (a 1.8 % understatement); at 18.899 the projected deadline pair count
  becomes **137** rather than 135 and projected look 2 moves ~2 days **earlier** (2027-02-27 rather
  than 2027-03-01); look 1 is reached from the 62 backfill pairs and does not move. Tolerance
  0.01 events/month.
- **What would resolve it:** relabelling the constant as n = 111 events (not 113 listings), or
  restating the rate as 18.90 with n = 113.
- **Confidence:** HIGH on the arithmetic — it uses only the claim's own stated inputs and the
  consuming script's own month length; the census count that backs n = 113 reproduces exactly.
- **Invalidated by later commits?:** no — `report.md` and `scripts/ktable_amended.py` are unchanged
  post-anchor. The census store it is measured from is untracked, but the trailing window closes at
  2026-08-27 and the file has not been written since.
- **Disclosed by authors?:** **no.** The effect on every downstream figure is small and in the
  conservative direction — the stated look dates are **later** than the measured accrual implies —
  which is why this is S4 and why it does not weaken the "one month inside the deadline" conclusion.
- **Consolidation check:** re-verified first-hand. Quotes re-located at `report.md:340-341` and
  `scripts/ktable_amended.py:48-49`, with `DAYS_PER_MONTH = 30.44` confirmed at `:50`. **No
  correction.**

### AUDIT-C-NPLExperiment-6
- **Repository / SHA:** NPLExperiment / `8f1fef83be0f76cbd671c2ce0fbfe8b1c4a5ea2c`
- **Hypothesis or artifact:** H2 — Amendment H2-4 boundary table, `registrations/H2/REGISTRATION.md`
  §3
- **Direction:** neutral — the totals the section's claim rests on are right; only the addends are
  wrong
- **Class:** INTERNAL_INCONSISTENCY
- **Severity:** S4
- **Label:** DERIVED (the artifact the registration names as its own full record, plus the module
  re-implemented)
- **Claim challenged (verbatim):** "| at look-1 min N | 59 | 30 | 22 | 37 | 0.0173 + 0.0200 = 0.0373
  | 0.7031 | 0.5529 |" — NPLExperiment/registrations/H2/REGISTRATION.md:695; and "| at the deadline |
  135 | 68 | 43 | 79 | 0.0176 + 0.0227 = 0.0403 | 0.9552 | **0.8629** |" —
  NPLExperiment/registrations/H2/REGISTRATION.md:697
- **Evidence:**
  - The registration names its own full record two sections earlier: "Full record: /
    `reports/stage_a_h2/ktable_amended.json`." — NPLExperiment/registrations/H2/REGISTRATION.md:645-646.
  - That artifact records, at look-1 min N: `alpha_spent_look1` **0.008062**, `alpha_spent_look2`
    **0.029206**, total 0.037268; and at the deadline (key `deadline_2027-03-31`):
    `alpha_spent_look1` **0.019230**, `alpha_spent_look2` **0.021113**, total 0.040343 — both
    re-read first-hand at consolidation.
  - The values 0.0173, 0.0200, 0.0176 and 0.0227 occur **nowhere** in `ktable_amended.json` (every
    float in the file searched to ±0.0006).
  - The middle row, "at look-2 min N … 0.0182 + 0.0240 = **0.0422**"
    (`registrations/H2/REGISTRATION.md:696`), **does** match the artifact exactly
    (0.018172 + 0.024025).
  - Only the components are wrong: both printed **totals** are right, and the totals are what the
    section's claim rests on ("Every total spend sits **inside** alpha_h = 0.05", :699-701). k₁, k₂
    and both power figures in the affected rows are also right (22/37 with 0.703083/0.552854; 43/79
    with 0.955244/0.862922).
- **Recomputation:** inputs `src/npl/register/sequential.py:63-121` and `src/npl/power.py:20-42`
  re-implemented in `/home/kiros-li/.cache/program-audit/scratchpad/work/agentC-npl/h2.py`; method —
  `alpha_spent_1 = P(Bin(n₁,½) ≥ k₁)`, `alpha_spent_2 = Σ_{s<k₁} P(Bin(n₁,½)=s)·P(Bin(n₂−n₁,½) ≥ k₂−s)`.
  Result: (59,30) → 0.008062 + 0.029206 = 0.037268; (117,59) → 0.018172 + 0.024025 = 0.042197;
  (135,68) → 0.019230 + 0.021113 = 0.040343 — identical to the artifact in all six components.
  Tolerance 5e-5.
- **What would resolve it:** correcting the two printed component pairs to the artifact's values. No
  total, boundary, power figure or decision changes.
- **Confidence:** HIGH — recomputed from the module the registration names and cross-checked against
  the artifact the registration names as its full record.
- **Invalidated by later commits?:** no — `registrations/H2/REGISTRATION.md` is not one of the two
  files the single post-anchor commit touches.
- **Disclosed by authors?:** **no.**
- **Consolidation check:** re-verified first-hand. Both quotes re-located at
  `registrations/H2/REGISTRATION.md:695` and `:697`, and the "Full record" pointer at `:645-646`.
  `ktable_amended.json` re-read at consolidation: `at_look1_min_n` 0.008062 / 0.029206 / 0.037268
  with k₁ 22, k₂ 37, powers 0.703083 / 0.552854; `deadline_2027-03-31` 0.019230 / 0.021113 /
  0.040343 with k₁ 43, k₂ 79, powers 0.955244 / 0.862922; `at_look2_min_n` 0.018172 / 0.024025 /
  0.042197. **No correction.**

### AUDIT-C-NPLExperiment-7
- **Repository / SHA:** NPLExperiment / `8f1fef83be0f76cbd671c2ce0fbfe8b1c4a5ea2c`
- **Hypothesis or artifact:** H5 — the Universe row of the H5 summary table in the register index
- **Direction:** neutral
- **Class:** INTERNAL_INCONSISTENCY
- **Severity:** S4 — a count in a summary cell; nothing reads it
- **Label:** DERIVED (two tracked artifacts)
- **Claim challenged (verbatim):** "The live family is two dexs: `xyz` 73, `para` 16." —
  NPLExperiment/HYPOTHESES.md:127
- **Evidence:**
  - `reports/h5/census.json:by_dex_live` = `{"io": 2, "mkts": 3, "para": 16, "xyz": 73}` — **four**
    dexs, summing to the 94 live instruments the same table cell reports.
  - Grouping the 94 `resolved`+`live` rows of `reports/h5/census.rows.json` by `dex` reproduces the
    same four counts exactly (re-run at consolidation).
  - The repository's own access document states it correctly: "**The live equity-style family is
    concentrated in two dexs**: `xyz` (73) and / `para` (16) hold **89 of the 94** live instruments;
    `mkts` holds 3 and `io` / 2." — NPLExperiment/docs/H5_ACCESS.md:152-154.
  - The retrospective section names `io:NBIS` as one of the two instruments with any observation
    (`report.md:693`), so an `io` live instrument is used by name a few pages later in the same
    report.
- **Recomputation:** inputs `reports/h5/census.json` and `reports/h5/census.rows.json`; method —
  group the 94 rows with `resolution_state == "resolved"` and `listing_status == "live"` by `dex`.
  Result: `{'xyz': 73, 'para': 16, 'mkts': 3, 'io': 2}` = 94. Tolerance: exact (integer counts).
- **What would resolve it:** one clause — "two dexs" → "concentrated in two dexs (89 of 94)",
  matching `docs/H5_ACCESS.md:152-154`.
- **Confidence:** HIGH.
- **Invalidated by later commits?:** no — `HYPOTHESES.md` is not one of the two files the single
  post-anchor commit touches.
- **Disclosed by authors?:** **no** — and this is a deliberate re-grading of the verification
  draft's "partially". `docs/H5_ACCESS.md:152-154` states the correct split, but no document flags
  the summary-table cell as wrong, so the correct statement is **evidence of the inconsistency, not
  a disclosure of it**. The reader most likely to see only the register index is the one who gets
  the wrong figure.
- **Consolidation check:** re-verified first-hand. Quote re-located at `HYPOTHESES.md:127`;
  `by_dex_live` re-read; the 94 live rows re-grouped by dex at consolidation (73/16/3/2);
  `docs/H5_ACCESS.md:152-155` re-read. **One re-grading:** the disclosure field, from "partially" to
  "no", with the reason stated. Severity, class, label and direction unchanged.

### AUDIT-C-NPLExperiment-8
- **Repository / SHA:** NPLExperiment / `8f1fef83be0f76cbd671c2ce0fbfe8b1c4a5ea2c`
- **Hypothesis or artifact:** H2 — Amendment H2-3 Change 1, the fallback control backfill
- **Direction:** neutral
- **Class:** ARITHMETIC
- **Severity:** S4 — hygiene; the load-bearing half of the sentence is exact
- **Label:** DERIVED (one tracked artifact)
- **Claim challenged (verbatim):** "append-only, tagged `cross_dex`: **24 of 24, zero exclusions**,
  19 distinct / controls, 174 candidates considered per event and **none skipped for / coverage**."
  — NPLExperiment/report.md:509-511
- **Evidence:**
  - `reports/stage_a_h2/backfill_fallback.json:assigned` carries a `candidates_considered` field per
    event; tabulated over the 24 rows the values are **172 (×3), 173 (×12), 174 (×9)** — 174 is the
    maximum, not a per-event constant.
  - The same artifact records `candidate_universe_n` = **175**, not 174.
  - Everything else in the sentence verifies exactly, and was re-verified at consolidation:
    `assigned_n` 24, `distinct_controls` 19, and `candidates_skipped_low_coverage` = 0 on **all 24**
    rows; `pairs_ledger_by_tag` = `{"same_dex": 38, "cross_dex": 24}` = the 62 rows the next
    sentence claims.
- **Recomputation:** inputs `reports/stage_a_h2/backfill_fallback.json`; method — `Counter` over
  `assigned[*].candidates_considered`, and `all()` over `candidates_skipped_low_coverage`; script
  `rest.py` in the work dir, re-run at consolidation. Result `{173: 12, 172: 3, 174: 9}`, universe
  175, zero skipped. Tolerance: exact (integer counts).
- **What would resolve it:** "172–174 candidates considered per event, from a universe of 175".
- **Confidence:** HIGH.
- **Invalidated by later commits?:** no — `report.md` is unchanged post-anchor.
- **Disclosed by authors?:** **no.**
- **Consolidation check:** re-verified first-hand. Quote re-located at `report.md:509-511`; the
  artifact re-read and re-tabulated at consolidation. **No correction.**

### AUDIT-C-NPLExperiment-9
- **Repository / SHA:** NPLExperiment / `8f1fef83be0f76cbd671c2ce0fbfe8b1c4a5ea2c`
- **Hypothesis or artifact:** H2 amendment stage — the precondition scan that licenses Amendment
  H2-3, and the ordering claim it supports
- **Direction:** neutral — the artifact's true time *supports* the ordering the sentence asserts; it
  is the printed time that would break it
- **Class:** PROVENANCE *(reconciled: the verification draft filed this as INTERNAL_INCONSISTENCY;
  the provenance draft as PROVENANCE. The defect is a timestamp on a provenance record whose only
  function is to establish an ordering, so PROVENANCE governs.)*
- **Severity:** S4
- **Label:** DERIVED (the tracked artifact plus two immutable commit dates)
- **Claim challenged (verbatim):** "**The preconditions, checked and recorded before anything else**
  / (`reports/stage_a_h2/amend_preconditions.json`, PASS at 07:51:10Z on the / project clock)" —
  NPLExperiment/report.md:445-447
- **Evidence:**
  - The artifact the sentence names records `"checked_at": "2026-08-28T06:51:10Z"` (and `head =
    e89b18717ce…`) — NPLExperiment/reports/stage_a_h2/amend_preconditions.json, identical in
    `git show f31f7a3:<path>` and in the anchored tree.
  - The same figure is **06:51:10Z** in the registration itself — "PASS at 2026-08-28T06:51:10Z" —
    NPLExperiment/registrations/H2/REGISTRATION.md:377 — and in the state log,
    NPLExperiment/progress.md:831. `report.md:446` is the **only** place in the repository carrying
    07:51:10Z.
  - 07:51:10Z is not merely different, it is **impossible for the sentence it sits in**: Amendment
    H2-3 was committed at `f31f7a3`, committer date 2026-08-28T00:01:06−07:00 = **07:01:06Z**, and
    Amendment H2-4 at `546b2e3` = **07:46:42Z** — both *before* the stated check time, which would
    place the "checked and recorded before anything else" scan after the two amendments it licenses.
    The artifact's real 06:51:10Z precedes the amendment commit by 9 m 56 s, exactly as the claim
    requires.
  - No timezone reading reconciles it: the repository clock is −07:00, so 06:51:10Z is 23:51:10
    local and 07:51:10Z is 00:51:10 local, neither of which is "07:51" in any frame.
- **Recomputation:** none beyond reading one field across four sources and two git objects, all
  re-read first-hand at consolidation.
- **What would resolve it:** correcting `report.md:446` to 06:51:10Z, or an appended dated note in
  the repository's own correction style (as commit `449ff1e` did for the H5 stage timestamps).
- **Confidence:** HIGH — one field, four sources, three agreeing, and two immutable commit dates
  that make the printed time impossible for its own sentence.
- **Invalidated by later commits?:** no — `report.md` last changed at `c7bdf64`
  (2026-08-28T22:07:26Z), before the anchor, and is untouched by the single post-anchor commit.
- **Disclosed by authors?:** **no.** The `449ff1e` correction sweep ("docs: correct the H5 stage
  timestamps against the commit clock", 2026-08-28T22:11:11Z) restated the H5 stage's ETA figures
  and corrected two artifacts, but it did not reach this line and nothing in the repository flags
  it.
- **Consolidation check:** re-verified first-hand. Quote re-located at `report.md:445-447`; the
  artifact's `checked_at` re-read from the anchored tree (06:51:10Z, head `e89b187…`); `f31f7a3`
  re-read as 2026-08-28T00:01:06−07:00 with `--name-status` = `M progress.md`,
  `M registrations/H2/REGISTRATION.md`, `A reports/stage_a_h2/amend_preconditions.json` (no source
  file); `546b2e3` = 07:46:42Z; `f8e54d8` = 07:40:26Z. **Merged from DRAFT-V-8 and DRAFT-P-2**;
  class reconciled to PROVENANCE; the provenance draft's evidence carried whole; the 22:20Z half of
  DRAFT-V-8 routed to **-10** rather than duplicated here.

### AUDIT-C-NPLExperiment-10
- **Repository / SHA:** NPLExperiment / `8f1fef83be0f76cbd671c2ce0fbfe8b1c4a5ea2c`
- **Hypothesis or artifact:** H5 Section 6 verdict record — the time the outcome map fired, as
  carried in the two summary documents
- **Direction:** neutral
- **Class:** PROVENANCE
- **Severity:** S4 — inside the S3 cap that the authors' disclosure imposes; recorded at S4 because
  no computed figure depends on it
- **Label:** **READ** — the limitation raised here is disclosed by the authors in their own words,
  so under the audit rules this finding is READ and capped at S3, whatever the evidence trail. The
  non-propagation half is established from a git object and is recorded inside the evidence.
- **Claim challenged (verbatim):** "### The row, fired 2026-08-28T22:20Z" —
  NPLExperiment/report.md:667; and "| **Status** | **PENDING — the census window is open** · fired
  2026-08-28T22:20Z." — NPLExperiment/HYPOTHESES.md:122
- **Evidence:**
  - `reports/h5/verdict.json` (tracked, anchored) records `"fired_at": "2026-08-28T22:04:30Z"` — the
    artifact written by `npl.h5.outcome.fire` itself.
  - **The authors caught this themselves, 3 m 45 s after committing it**: "The verdict record above
    is headed **22:20Z**. That figure was typed by the / assistant as an estimate rather than read
    from the clock. **The map actually / fired at 2026-08-28T22:04:30Z**, recorded by the artifact
    itself / (`reports/h5/verdict.json`, field `fired_at`)." —
    NPLExperiment/registrations/H5/REGISTRATION.md:632-637, added by `449ff1e`
    (2026-08-28T22:11:11Z), with the same correction at NPLExperiment/progress.md:1494-1496.
  - What remains at the anchor is that the correction was **not propagated**:
    `git show --name-status 449ff1e` = `M progress.md`, `M registrations/H5/REGISTRATION.md`,
    `M reports/h5/h2_verification.json` — **`report.md` and `HYPOTHESES.md` are not in that list**,
    and neither file changes again before the anchor (both last touched at `c7bdf64`). A reader of
    either summary document gets 22:20Z with no cross-reference to the correction.
- **Recomputation:** none — one artifact field against two document lines and one commit's file
  list, all re-read first-hand at consolidation.
- **What would resolve it:** propagating the correction note to `report.md:667` and
  `HYPOTHESES.md:122`, or a pointer from each to `registrations/H5/REGISTRATION.md:632-639`.
- **Confidence:** HIGH.
- **Invalidated by later commits?:** no — the single post-anchor commit `dff1663` appends Amendment
  H5-3 to `registrations/H5/REGISTRATION.md` and adds a `progress.md` entry; it does not touch
  `report.md` or `HYPOTHESES.md`, so the 22:20Z lines still stand at live `HEAD`.
- **Disclosed by authors?:** **yes** — `registrations/H5/REGISTRATION.md:632-639` and
  `progress.md:1494-1496` both record the correct time and name the slip as an assistant estimate
  rather than a clock reading. **Presenting this as a discovery would itself be a process failure;
  it is recorded here only because the correction did not reach the two summary documents**, and it
  is labelled READ and capped at S3 for that reason.
- **Consolidation check:** re-verified first-hand. Both quotes re-located at `report.md:667` and
  `HYPOTHESES.md:122`; `verdict.json:fired_at` = 22:04:30Z re-read; the correction re-located at
  `registrations/H5/REGISTRATION.md:632-637` and `progress.md:1494-1496`;
  `git show --name-status 449ff1e` re-read 2026-09-12T13:06Z (three files, neither summary
  document). **One re-grading:** label DERIVED → **READ**, per the disclosed-limitation rule.
  Severity, class and direction unchanged.

### AUDIT-C-NPLExperiment-11
- **Repository / SHA:** NPLExperiment / `8f1fef83be0f76cbd671c2ce0fbfe8b1c4a5ea2c`
- **Hypothesis or artifact:** Amendment H5-1's "what data existed" record — the reconnaissance
  probe's charge time
- **Direction:** neutral
- **Class:** PROVENANCE
- **Severity:** S4
- **Label:** DERIVED — but from the **untracked, UNANCHORED** request ledger; see the confidence note
- **Claim challenged (verbatim):** "**What data existed when this amendment was made.** The Task 2 /
  reconnaissance probe had run: **six requests**, charged to the shared ledger / at
  2026-08-28T21:41Z." — NPLExperiment/registrations/H5/REGISTRATION.md:367-369
- **Evidence:**
  - `data/ledgers/requests.jsonl` (untracked, gitignored, **UNANCHORED** — mtime 2026-09-12 05:06
    local, read 2026-09-12T12:37:29Z) holds exactly six `charge` rows in that burst and six matching
    `settle` rows, all stamped **2026-08-28T21:39:45Z – 21:39:48Z**: `perpDexs` ×1 (21:39:45Z),
    `metaAndAssetCtxs` ×2 (21:39:45Z), `fundingHistory` ×2 (21:39:46Z), `l2Book` ×1 (21:39:48Z), all
    HTTP 200. **The count of six in the claim is exact**, and is corroborated by the tracked spend
    reconciliation ("6 reconnaissance", NPLExperiment/progress.md:1509).
  - There is **no ledger activity of any kind at 21:41Z**: the last charge before the burst is
    21:05:53Z (the hourly H2 watcher) and the next after it is 21:44:11Z (census pass 1).
  - The discrepancy is ~1 m 45 s and matters only because the amendment's force rests on that time
    bounding what was visible when it was written; nothing downstream reads the figure.
- **Recomputation:** inputs `data/ledgers/requests.jsonl` restricted to 2026-08-28T21:39:00Z –
  21:44:12Z; method — enumerate `charge` and `settle` rows by `ts` and `endpoint`; scripts in
  `/home/kiros-li/.cache/program-audit/scratchpad/work/agentC-npl-prov/`. Result: 6 charges, 6
  settles, all HTTP 200, 21:39:45Z–21:39:48Z; no row at any time in 21:40Z–21:43Z. Tolerance: exact
  to the second.
- **What would resolve it:** restating 21:41Z as 21:39:45–21:39:48Z in the repository's own
  correction style, or committing an append-only archive of that ledger window alongside the
  amendment.
- **Confidence:** **MEDIUM** — the ledger is append-only by design and its prefix is hash-verified
  stable across the H5 stage (`reports/h5/h2_verification.json:shared_append_only_ledgers`), but it
  is untracked and fifteen days of appends have landed since the anchor, so this asserts only what
  the file said at the read time.
- **Invalidated by later commits?:** no — no commit at or after the anchor touches this line. The
  *evidence*, however, is UNANCHORED working-tree data and is labelled as such.
- **Disclosed by authors?:** **no.** The `449ff1e` correction sweep restated the stage's ETA figures
  but did not reach this one.
- **Consolidation check:** quote re-located at `registrations/H5/REGISTRATION.md:367-369`. The
  ledger evidence was **not** re-read at consolidation (it is untracked and has continued to grow);
  it stands as recorded at 2026-09-12T12:37:29Z, and the confidence grade reflects that. The tracked
  corroboration of the count — "6 reconnaissance" at `progress.md:1509` — **was** re-read. **No
  correction.**

---

## Sound

What verified cleanly, and what would have shown up here had it not.

**The H1 closure (the founding hypothesis) is arithmetically sound end to end.** All three
co-primary statistics reproduce from the counts alone to 1e-15, by the repository's own estimator
and independently by `scipy`: the exact Clopper–Pearson lower bound 0.5706880326738533 (197/312),
the sign-test p = 0.9999998937952859 (111/312), and p = 3.766632285793312e-05 (114/175). The three
cost bands, the four 90-day secondaries, the per-type strata shares, the effective-N preconditions
(312/312/175 against registered minimums 34/103/60, zero shortfalls) and the H8 decomposition all
reproduce exactly — including the "+2.2 % net" figure, which is **not** stored anywhere and had to
be re-derived from the registered round-trip costs: 1.3317 % + 0.9990 % gross, less a mean cost of
(154 × 18 + 158 × 9)/312 = 13.442 bp, gives **2.196 %**.

**The read surface is genuinely pinned.** `sha256(reports/stage_b/read.json)` is
`4455489675c3774f05c977cb7edb9d8b26928f851400077b31263f5826be840c`, identical to `HYPOTHESES.md:54`
(recomputed again at consolidation). The latch holds 21 module hashes; all 21 match
`git show 32b3f9e:src/npl/<mod>` and `844f7c2:<mod>`. The B.0 → B.1 re-hash claim is exact: 19 → 21
modules, two added (`stageb/cli.py`, `stageb/reader.py`), **exactly one changed**
(`stageb/__init__.py`), none removed. Five modules differ from the **anchor** tree, and each first
diverges at `77ee522` or later — i.e. after the 03:01:08Z read — so the Amendment 3 rule that "any
diff in a B.0-hashed read-surface module after the B.1 re-hash voids the read authorization" is not
breached.

**The H2 sequential design is right where it matters.** Minimum N at all three scenarios and both
effects, the boundaries k₁/k₂, the **total** alpha spends, both powers per scenario, the futility
boundaries, the six-row alpha-split materiality screen, the Section 0 gate recomputation and the
projected look dates all reproduce exactly from `sequential.py` and `power.py` re-implemented. The
alpha split is **across looks**, which is the correct device; no spurious correction is applied
across E1 and E2.

**The register cull reproduces to its fixed point:** pass 1 (k = 3) H2 0.577117 / H3 0.000000 / H4
0.013958, pass 2 (k = 1) H2 0.760372, with `alpha_h` = 0.05 / 0.0253206 / 0.0169524 and H4's
within-hypothesis Šidák `alpha_cell` = 0.005683 — all exact, and the Šidák is correctly attached to
the one **union** rule in the program.

**Every H5 spend figure reconciles against the request ledger charge-for-charge:** 888 total = 6
reconnaissance (21:39:45–48Z) + 323 census pass 1 (21:44:11Z) + 323 census pass 2 (21:51:54Z) + 27
retrospective (21:56:05–40Z) + 209 forward (22:00:14Z), i.e. ledger positions 2948 → 3835 on
2026-08-28; 888/20,000 = 4.44 %; the day total 3,847 = 19.235 %; the forward pass's 209 = 1.045 %.
Both census passes are 1 + 10 + 10 + 151 + 151 = 323 exactly.

**The H5 structural counts are exact and the universe rule does what it says.** 273 → 151 resolved
(118 equity / 15 ETF / 18 index), 80 + 42 excluded, → 94 live and 57 delisted with **0**
conflicting: all 57 delisted carry `is_delisted` **and** `open_interest == 0` **and**
`day_notional_volume == 0`, and **none** of the 94 live carries any of the three. The 32-of-57
"honesty clause" figure is exact — exactly 32 delisted instruments still carry 168 unbroken hourly
funding rows, every one stamped `funding_last_time_ms` = 2026-08-28T21:00:00Z. The retrospective
shortfall (27 of 151 eligible, 124 quarantined, 39 observations, 2 instruments, 0 at the coverage
bar; `io:NBIS` 8/1 day, `xyz:XBI` 31/2 days) is exact, and the per-instrument counts sum to 39. The
pooled n = 188 summary — the figures the row actually fired on — reproduces to 0.0e+00.

**The provenance spine holds.** Registration before the first network call (2 m 11 s). Amendment 3
before the reader existed (11 m 23 s) and before the read (11 m 49 s). Amendment H2-3 registered in
a commit containing **no source file** and implemented 39 m 20 s later. The H5 registration,
mapping and calendar committed with zero H5 requests sent, and byte-frozen thereafter. `k = 1`,
`alpha_h = 0.05` and `family_confidence = 0.95` never revisited. Registration files pure-insertion
throughout. The H2 quarantine independently re-verified twice, 14 hours apart, and still holding
today: 11 store hashes unchanged, pair count 62 = 62, all three H2 latches absent.

**Amendment H5-1 does what the authors claim it does, and I recomputed it rather than took it.**
Under `98e7e01:outcome.py` the measured inputs fire **CLOSED**; under `13c6965:outcome.py` the same
inputs fire **PENDING**. So "makes CLOSED strictly harder" is exact — the post-amendment acceptance
region is a strict subset — and "it cost this entry a same-day close" is literally true. The
authors state the same fact themselves.

**What would have shown up here if the two theses held.** A program that had closed too early would
show a co-primary bound that moves across its bar under a defensible re-derivation, or a power
screen that survives at the registered assumption and dies at a measured one. Neither happens: the
H1 bound fails by 3 points of share and moves *away* from the bar under every alternative tried,
and the cull's kills reproduce exactly. A program that claimed too much would show verdict-bearing
figures that no stored primitive reproduces. Only **one** block fails that test — the H5 stratum
table (finding **-1**) — and the rest of the H5 row, the part that actually fired, reproduces
exactly.

---

## Could not be checked and why

| item | why not |
|---|---|
| Gate figures: "249 passed", "217 passed", "172 passed", "159 passed", `mypy --strict` on 71 / 67 files (`report.md:581-582,292,148`; `reports/h5/preconditions.json`; `reports/stage_a_h2/amend_preconditions.json`) | The audit rules forbid executing a repository's own scripts or test suites in place, and the figures are recorded only as free-text strings inside the artifacts. Copying the tree out and building its environment would not reproduce the *historical* runs either. **UNVERIFIABLE by construction** — neither confirmed nor contradicted. |
| "156 pages, 60,010 funding hours, **0 unrecoverable hours**" (`report.md:336-337`) | No committed artifact stores page or hour totals for the A.1 archive rebuild; re-deriving them would mean walking all 462 per-instrument directories under `data/funding/` and reconstructing the coverage rule. Not attempted. |
| "median trailing entry funding **+31.6 percent/yr** (min −132.4)" (`report.md:355-356`; `registrations/H4/REGISTRATION.md:211-221`) | The per-event 168-hour trailing means are stored in no `reports/` artifact; only the three conditioning **counts** (11 / 8 / 5 of 62) are, and those verify exactly. Re-deriving the series would require re-reading funding values under the blindness gate. |
| "224,633 funding rows summed inside the 30-day windows" (`report.md:216`) | Verified **as recorded** in `reports/stage_b/read.json:funding_rows_30_total`, but not re-derived from the sealed archives: the window arithmetic needs `src/npl/intervals.py:merge_windows` plus each event's entry anchor, and the archives are untracked. Internally consistent with `preconditions.events_covered_30 = 312`. |
| Whether Amendment H5-2 truly "deleted this entry's only route to VIABLE" (`report.md:663`; `DECISIONS.md:511`) | `src/npl/h5/outcome.py:165-185` fires VIABLE only when a session tag's **median** absolute basis exceeds 54 bp. With the delisted stratum included, the all-resolved median at the three 2026-08-28 passes is 4.14 / **4.63** / 5.07 bp, while the delisted stratum alone has a median of 30.5 bp — so **no contemporaneous reading came within an order of magnitude of VIABLE either way**. The claim is a forward statement about a 30-day census in which frozen delisted marks drift away from live oracles. It cannot be settled from the data at the anchor and is **recorded with its numbers rather than adjudicated**. |
| A clustered or block recomputation of the H1 co-primary bounds | The 312 events are one draw per instrument-event and are not repeated within instrument, so a within-unit clustered bound is **undefined**; a calendar-block bootstrap would need per-event entry dates, which no tracked artifact holds (only counts are stored). Not recomputed. The direction is knowable without it: the stated comparison (0.5707 against the 0.60 bar) already fails, and a block correction widens the bound *away* from the bar. |
| Whether Amendment H5-1 was *written* before census pass 1 (21:44:11Z) | Its text asserts it; git gives only the commit `13c6965` at 21:59:42Z, which is after both passes and which carries the census artifacts and the implementing code in the same tree. The assertion is **corroborated** — pass 1 carries no `listing_status` field and is counted as `rows_skipped_pre_amendment = 273`, pass 2 carries it, and Amendment H5-2 names pass 1 as its own census-in-hand — but corroboration is not a commit boundary. Recorded **PARTIAL, not a finding**, because nothing contradicts it. Amendment H2-3 shows the program *can* do better: registered in a commit with no source file, implemented 39 minutes later, which git proves outright. |
| Push times | The documents say "committed **and pushed**" repeatedly. Only commit times are observable from this side; `origin` was not contacted. Where a claim says "pushed", "committed" was verified and the difference noted. The repository's own push verification (`amend_preconditions.json:origin_equals_head`, `reports/h5/preconditions.json:origin_main`) is an authored record, not an independent one. |
| Whether the operator's 2026-08-27 instruction authorizing the prior fill exists | Only its **absence from `progress.md`** is checkable — it may have been given in chat. The repository's own standing rule 1 (log operator prompts verbatim) is what makes the absence checkable at all, and is the basis of finding **-3**. |
| The 21 module hashes *at the moment of the read* | Verified to reproduce against `32b3f9e` and `844f7c2` sources, which is as close as git can place them; the latch file itself is untracked and its mtime (2026-08-28T03:01Z) is consistent but not cryptographic. |
| Post-anchor state of `data/` | Everything read from `data/` may have changed after 2026-09-02: `data/ledgers/requests.jsonl` mtime 2026-09-12, `data/h5/snapshots.jsonl` mtime 2026-09-11, `data/state/fresh_plan.jsonl` now 128 lines against the 124 the amendment recorded, `data/controls/h2_pairs.jsonl` now 63 lines against 62 (the 63rd appended 2026-09-02T02:01:32Z, consistent with the anchor). **Every figure taken from `data/` is labelled UNANCHORED with its read time.** `data/h5/census.jsonl` (mtime 2026-08-28) and `data/state/generating_sample.json` (mtime 2026-08-27) have not moved since the stages that wrote them. |
| The realized census-pass rate (D12), and the 2026-09-26 projection | Checkable, and checked — 12 full passes in the 15 days 2026-08-29…2026-09-12, i.e. 0.80/day against the assumed 1.00 — but it is **post-anchor** evidence against a pre-anchor projection, and **the authors falsified and corrected it themselves** in the single post-anchor commit `dff1663` (Amendment H5-3: "measured **0.77 passes/day**", projection → ~2026-10-05, "no bar moved"). Recorded here so that no finding against the 2026-09-26 projection can be presented as undiscovered. **Not a finding.** |
| Anything under `findings/agentA` or `findings/agentB` | Not read, per the task. Not counted in the provenance UNVERIFIABLE total, because it is a scope note rather than a claim. |

---

## Live-repo access log

Live path: `/home/kiros-li/Documents/GitHub/NPLExperiment/`. All access read-only across all three
passes (LOCATE/VERIFY, PROVENANCE, and this consolidation). **No file under the audited repository
was opened for writing, no script belonging to it was executed, no working-directory command was
run inside it, and no git command other than `status`, `log`, `show`, `rev-parse` and `diff` was
issued.** No `.env`, `.keystore/`, `*.session`, credential, token or API-key file was read or
listed; `.env.example` appeared in one directory listing of the snapshot and was not opened.

### Status before and after, verbatim

**Provenance pass — pre-access `git -C /home/kiros-li/Documents/GitHub/NPLExperiment status
--porcelain`, 2026-09-12T12:31:5xZ:**

```
```

**Provenance pass — post-access, 2026-09-12T12:41:45Z:**

```
```

**Verification pass — pre-access, 2026-09-12T12:34:05Z:**

```
```

**Verification pass — post-access, 2026-09-12T12:48:25Z:**

```
```

**Consolidation pass — pre-access, 2026-09-12T13:06:23Z:**

```
```

**Consolidation pass — post-access, 2026-09-12T13:06:58Z:**

```
```

All six are **empty — a clean tree**, with no modified, staged or untracked entries (`data/` is
covered by `.gitignore:data/`). No entry outside the COMMON_RULES pre-existing-dirt list appeared,
and NPLExperiment is not on that list, so there was nothing to report. `git rev-parse HEAD` returned
`dff16632eca6eea05b290ade5464339f44c75744` at every check. **Nothing in the audited repository was
modified.**

### What was read live, and when (all UTC 2026-09-12)

| time | what |
|---|---|
| 12:31:5x–12:39 | `git status`, `rev-parse`, `log --all`, `log --follow` (on `REGISTRATION.md`, `HYPOTHESES.md`, the four successor registrations, `config.py`, `DECISIONS.md`, `report.md`, eight `src/npl/h5/*.py`), `log --follow --numstat` on the five registration files, `log -S "0.40 (adopted)" --all`, and `git show` (`--stat`, `--name-status`, path-scoped diffs, `<commit>:<path>` object reads) on `cd640b6`, `6399d63`, `32b3f9e`, `844f7c2`, `f31f7a3`, `f8e54d8`, `546b2e3`, `f72af92`, `98e7e01`, `13c6965`, `e0eab81`, `c7bdf64`, `b685d30`, `449ff1e`, `c2aaa27`, `2d2edc1`, `f1def31`, `6dfdbb1`, `8e31e78`, `77ee522`, `2b44c59` |
| 12:32:30, 12:35:19, 12:35:35, 12:37:29, 12:38 | `data/ledgers/requests.jsonl` (6,648,724 B, mtime 2026-09-12 05:06; 58,599 lines). Only `day`, `kind`, `ts`, `endpoint`, `status`, `http_status` used. **UNANCHORED** |
| 12:35:39, 12:36, 12:37:14, 12:41 | `data/h5/census.jsonl` (546 lines, two snapshot ids, mtime 2026-08-28) and `data/h5/snapshots.jsonl` (3,652 lines, 14 snapshot ids 2026-08-28…2026-09-12, mtime 2026-09-11). **UNANCHORED** |
| 12:37:06, 12:37:59, 12:38:13 | `ls -la data/h5/`, `data/state/`, `data/ledgers/`; `sha256sum data/state/stage_b_read.json`; `json.load` of `data/state/stage_b_read.json` (keys `read_at`, `module_hashes`) and `data/state/generating_sample.json` (`count`, `event_ids`). **UNANCHORED** |
| 12:38:24, 12:38:38 | module-hash comparison scripts reading `git show <commit>:src/npl/<module>` into memory and hashing; nothing written inside the repository |
| 12:44, 12:45 | `data/census/census.jsonl` (505 lines; `first_1d_open_ms`, `dex`, `coin`, `recorded_at`); `data/controls/h2_pairs.jsonl` and `pairs.jsonl` (line counts and `pair_type` tallies, 63 / 176); `data/eligibility/{h2,h3,h4}.jsonl`, `data/state/{fresh_plan,retro_plan}.jsonl`, `data/state/generating_sample.json` (counts only). **UNANCHORED** |
| 13:06:23–13:06:58 | **consolidation:** `git status --porcelain` (pre and post), `rev-parse HEAD`, `log --format 8f1fef8..HEAD`, `diff --name-status 8f1fef8 HEAD`, `diff --stat`, a path-scoped `diff` of `registrations/H5/REGISTRATION.md`, `show -s --format` on nine commits, `show --name-status` on `2d2edc1`, `449ff1e`, `f31f7a3`, and `show 8f1fef8:progress.md` piped to `sed`. **Git objects only; no working-tree data was re-read at consolidation** |

### Scratch and work directories

All computation used `/home/kiros-li/.cache/program-audit/scratchpad/venv/bin/python` (numpy/scipy
used only as an independent cross-check against the repository's own log-space formulas). All
scratch written only under `/home/kiros-li/.cache/program-audit/scratchpad/work/` — `agentC-npl/`
(verification), `agentC-npl-prov/` (provenance), `agentC-npl-consol/` (this pass). Nothing was
written into `SNAP/`, which was read only.
