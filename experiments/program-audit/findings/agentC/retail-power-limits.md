# retail-power-limits — Agent C (referee / verifier), consolidated findings

Repository: retail-power-limits
Anchored SHA: `dda39b2f148569a6fe9be956a979471b2330611d` (main, 2026-08-29; also live `HEAD`)
Sources consolidated: `findings/agentC/verification/retail-power-limits.inventory.md` / `.json`,
`findings/agentC/verification/retail-power-limits.verification.md` / `.claims.json`,
`findings/agentC/provenance/retail-power-limits.md` / `.json`.
Every quote and every figure in this file was re-checked against
`SNAP/retail-power-limits` and the sibling snapshots before publication. Prepared 2026-09-04 UTC.
An independent citation-check pass then re-located every quote, re-confirmed every cited figure at its
cited line and re-ran every recomputation; its result is recorded as a **Citation check** bullet on each
finding. Eight findings entered that pass, eight leave it: seven verified unchanged, one corrected
(AUDIT-C-retail-power-limits-3, whose disclosure answer moves from No to Partially), none dropped.

## Summary

This repository computes nothing: it is a note plus a typed registry of quoted figures, so almost
every claim in it is a transcription claim and verification means going to the sibling repository
at the commit the registry names. Done that way, the transcription is overwhelmingly accurate —
all four deciding numbers (NPD 0.0512, Insider 49.35 bp/month, ETF 163-vs-300, HF z 1.668)
reproduce from the siblings' own stored primitives, all 24 citations resolve, every cited file is
byte-identical between the cited commit and its sibling's anchored SHA, all eight quoted commit
subjects and all four "Closure language, exact." blocks are verbatim, and the single figure the
repository declares its own arithmetic (411 minutes) sums correctly with a correct exclusion note.
The provenance spine verifies in its strongest form: InsiderExperiment's power gate and its 20/40 bp
bars are genuinely in that repository's first commit, Section 0 is byte-identical from first commit
to closure, and no registered parameter anywhere in the four power cases moved without a dated
amendment.
What does not verify is one substantive figure and a handful of counts and characterisations: the
NPD "Sample achieved" line pairs 404 evaluable days with 125.6 independent-equivalent days when the
achieved figure is 201.2 (and 125.6 belongs to the pre-collection 427-day base), the same confusion
recurs as "lost 70 percent" where the realized loss was 50 percent, "seven source repositories"
appears in five places where the registry cites eight, solclear's two survivorship gaps are labelled
to the wrong horizons, the cost table carries one of two competing time figures the sibling
explicitly declines to choose between, "a powered null" is applied to solattn on a record that
contains no detectability figure, and the self-reported test count is 111 against 112 collected.
What could not be checked is the internal correctness of the four sibling power cases themselves,
the tail convention behind InsiderExperiment's registered t = 2.0, ETFExperiment's alpha, and
AiTrader's z 1.668 / 1.455 as numbers rather than as quotations — none of which is a claim this
repository makes about itself.
No thesis is asserted either way: the corrections found are as likely to run in the note's favour as
against it, and two of them (the unpublished-repository disclosure and the eight-versus-seven count)
correct the note in the direction of *more* checkability, not less.

## Verification scoreboard

### Claims

| status | count |
|---|---|
| VERIFIED | 37 |
| CONTRADICTED | 6 |
| UNVERIFIABLE | 1 |
| **total claim rows audited** | **44** |

Counting convention: 44 is the granular row count (`retail-power-limits.claims.json`,
`kind == "claim"`), which splits compound inventory claims into independently checkable parts
(C-01b/c/d, C-02b, C-03b, C-28a/b, C-29a/b), adds C-31 for the separately quoted "lost 70 percent"
sentence, and carries six provenance claims (P-08, P-10, P-11, P-13, P-16, P-18) that are also
counted in the provenance block below. Rolled up to the 31 inventory-numbered claims, the same
result reads 25 VERIFIED / 6 CONTRADICTED, with the "about ninety figures" half of C-29
UNVERIFIABLE for want of any stated counting rule. Alongside these, 30 derived quantities (D-01 to
D-30) were recomputed by me from stored primitives and taken from no document; 26 agree, 2 disagree
(D-16/D-17 and D-27), and 2 (D-28, D-29) are sibling-side artefacts explicitly not charged to this
repository.

### MUST-VERIFY claims (inventory rank 1–8)

| claim | subject | status |
|---|---|---|
| C-01 | NPDExperiment's deciding number, realized MDE 0.0512 | **VERIFIED** — `2.0 × 0.02562 = 0.05124 → 0.0512` from `NPDExperiment/reports/stage_b2/evaluation.md:81` through `src/npd/eval/evaluator.py:544` with `t_critical=2.0` (`src/npd/config.py:119`); the band, the 0.026–0.047 projection and the 0.36339-vs-0.2626 pair all verify too |
| C-02 | InsiderExperiment's deciding number 49.35 bp/month and its 40 bp BLOCKED floor | **VERIFIED** — TE 9.993 %/√12 = 288.47 bp/month, N_eff months 2,869.9/21 = 136.66, SE 24.676 bp, ×2.0 = **49.353**, matching `InsiderExperiment/REGISTRATION.md:712,717-719`; the 20/40 bars and the inclusive-boundary convention are at `:41-46` in that repository's first commit |
| C-03 | ETFExperiment's closure comparison, 163 projected vs 300 governing | **VERIFIED** — `ETFExperiment/REGISTRATION.md:984` states the 163 and `:1014-1015`/`HYPOTHESES.md:70` the governing 300; the note's own re-scoping (that 845 / above-1,200 / ~302 are Amendment 6's numbers, not the closure's) is correct |
| C-04 | HFExperiment's inherited resolution, z 1.668 against a 2.50 bar | **VERIFIED** — all five figures verbatim at `AiTrader/RETURN.md@f819b68:2857,2899`; delivered 27.99 × 252 = **70.53 %/yr**, needed 66.4 × 2.50/√2.55 = **103.95 → 104.0**, shortfall 1.475 → 1.5× |
| C-05 | The progression clock, the note's stated "transferable output" | **VERIFIED** — commit timestamps give a gap of **5 h 07 m 58 s** ("five hours and eight minutes", a 2-second round-up) and a total of **9 h 57 m 17 s** ("under ten hours"); `fbfc74e` is genuinely InsiderExperiment's first commit |
| C-06 | The one figure the repository computes itself, 411 minutes | **VERIFIED** — 22+34+68+52+194+41 = **411**, every addend present in `NPDExperiment/progress.md`, the six stages are the complete timed set, and the Z.1 exclusion note is correct |
| C-07 | NPDExperiment's effective-sample base, 404 paired with 125.6 | **CONTRADICTED** → AUDIT-C-retail-power-limits-1 (the achieved figure is 201.2; 125.6 belongs to the 427 base) |
| C-08 | HFExperiment's width-widening arithmetic, 66.4→31.7 / 27.99→10.04 / z 1.668→1.455 | **VERIFIED** as transcription — all four figures identical at `AiTrader/RETURN.md@f819b68:2872,2880`. The z pair is Newey-West at 21 lags, not an iid TE ratio (which would give 1.696 / 1.274); that is a standard-error convention, recorded and not raised as a finding |

### Intervals audited

| metric | value |
|---|---|
| intervals audited | 5 (I-01 to I-05) |
| independence doubtful | 1 |
| recomputed | 2 |
| conclusion moved by recomputation | 0 |

Estimator / independence summary. **This repository states no estimator, no level and no tail for
any interval it carries**; every one is defined in a sibling, and I-04 and I-05 are not intervals at
all but a pre-registered sensitivity grid and a set of literature effect bands, correctly labelled
as such wherever they appear. I-01 (solattn's `[−3.3354, +0.0204]` around −1.0779) is a 95 %
day-clustered bootstrap and is the one place where independence is doubtful in a way that matters:
the clustering is on **three** birth days, so the resample admits only ten distinct day-multisets, a
resolution floor solattn states about its own estimator at `solattn/FINDINGS.md:213-218` and which
does not reach `retail-power-limits`. That thinness does not move the stated comparison — the kill
criterion K1 is "the interval includes zero" and it does — but it does undercut the *word* the note
attaches to it (AUDIT-C-retail-power-limits-3). I-02 (AiTrader's `[−4.9, +60.9]`) is day-clustered
with a Newey-West SE at 21 lags, so dependence is handled at source; I-03 (HFExperiment's day-2,061
/ day-2,852 schedule) is an anytime-valid confidence sequence for which peeking is permitted by
construction and which was never evaluated on data (n = 0 realized). Two intervals were re-derived
rather than merely compared: I-04's grid cells reproduce exactly (2.0 × 0.2626/√125.6 = **0.0469**;
2.0 × 0.1438/√125.6 = **0.0257**), and I-01's width and multiset count reproduce (**3.3558** on a
point of 1.0779, a ratio of 3.11; C(5,3) = **10** multisets). The remaining three are transcription
checks: their draws are not stored in a form I can redraw.

### Tests audited

| metric | value |
|---|---|
| tests / decision rules audited | 8 (T-01 to T-08) |
| tail mismatches | 0 |
| dof issues | 0 |
| correction mismatches | 0 |

Tail / dof / correction summary. **There is no p-value anywhere in `retail-power-limits`, and no
alpha, target power or critical value is stated for any figure it carries**; each test below is
named as its sibling defines it. Every correction that exists matches the shape of the rule it
serves. T-01 (AiTrader's z 1.668 against a "corrected bar of 2.50") applies **Bonferroni** across a
closed list of four primary hypotheses — a union over a disjunction, which is the right family;
`z(1 − 0.0125/2) = 2.4977 → 2.50` recomputes exactly, and the within-hypothesis conjunction
correctly takes no further split. T-03 (NPD's 0.0512) and T-02 (Insider's 49.35) are single
pre-registered primaries and correctly take no correction, NPD's registration saying so in terms
(`evaluation.md:84-86`). T-04 (ETF's required N) is an intersection-union conjunction over two
co-primaries where the governing minimum is the larger, 300; no per-component correction is needed
and none is applied — a Bonferroni split here would have been the mismatch. T-05 (solattn) applies
**Šidák** at α_adj = 0.000321 on the **registered 160-cell** grid, which recomputes exactly
(`1 − 0.95^(1/160)`); using the 120 computable cells would have given the less conservative 0.000427,
and the registered denominator is what was used. T-06 is a suppression rule, T-07 a discrimination
statistic on which no test is run, and T-08 an identity — all correctly not dressed as tests. One
tail is **UNVERIFIABLE** rather than mismatched: neither repository states whether
InsiderExperiment's registered `t = 2.0` is one- or two-sided, leaving the implied α ambiguous
between ≈0.023 and ≈0.046. It does not move the verdict — even at t = 1.645 the MDE is 40.6 bp,
still above the 40 bp BLOCKED floor. ETFExperiment's significance level is stated in neither
repository; its 0.80 target power is stated in the sibling only.

### Provenance

| status | count |
|---|---|
| SUPPORTED | 32 |
| NOT_SUPPORTED | 1 |
| PARTIAL | 2 |
| UNVERIFIABLE | 0 |
| **total** | **35** |

Composition: 22 registration claims (19 SUPPORTED, 2 PARTIAL, 1 NOT_SUPPORTED) and 13
parameter-change rows across the four power cases plus this repository itself (13 SUPPORTED —
**every changed registered figure carries a dated amendment, and there are no undated changes at
all**). The single NOT_SUPPORTED is P-14, the four-of-seven publication disclosure, which was true
at the anchored SHA and became false 11 h 23 m later the same day
(AUDIT-C-retail-power-limits-7). The two PARTIALs are P-01 — HFExperiment's Section 0 fired BLOCKED
on the *broker*, not on a power gate, which the authors disclose in three places
(`docs/the-power-limit.md:141-146`, `DECISIONS.md:125-129`, `rplimits/cases.py:286-294`) — and
P-17's second half, InsiderExperiment's "the alpha is still sealed", which rests on strong
structural code evidence plus the repository's own statement but on no read-audit artifact.

---

## Findings

### AUDIT-C-retail-power-limits-1
- **Repository / SHA:** retail-power-limits / `dda39b2f148569a6fe9be956a979471b2330611d`
- **Hypothesis or artifact:** The NPDExperiment `PowerCase`'s `sample_achieved` Figure — the "Sample achieved" line of the generated `power-records` block.
- **Direction:** B (claimed too much)
- **Class:** INTERNAL_INCONSISTENCY
- **Severity:** S2
- **Label:** DERIVED
- **Claim challenged (verbatim):**
  > "**Sample achieved.** 415 stored daily rankings of 432 eligible window days, 96.1 percent coverage against a 90 percent bar; 404 evaluable days; 125.6 independent-equivalent days after the 3.4 variance inflation the five-session horizon induces."

  — `retail-power-limits/SOURCES.md:42`, generated from `retail-power-limits/rplimits/cases.py:100-104`, sourced to `NPDExperiment/progress.md @ 2d3d0ae`.
- **Evidence:**
  - The cited source never pairs 404 with 125.6. 125.6 is the **pre-collection projection off a 427-day base**: `NPDExperiment/REGISTRATION.md:227` — "which takes 427 evaluable days to **125.6** independent-equivalent days" — and `:229` "D = 427, effective D = 125.6".
  - The **achieved** figure is 201.2. `NPDExperiment/reports/stage_b2/evaluation.md:92`: "| achieved effective sample size | **201.2** independent-equivalent days |", under the heading "Power that actually existed", on n = 404 evaluable days (`evaluation.md:51`, "**404 evaluable days.**").
  - The code defines it from the bootstrap, not the theoretical VIF: `NPDExperiment/src/npd/eval/evaluator.py:529`, `effective_n = (sd_daily / se) ** 2`.
  - The two Figures inside the same `PowerCase` are mutually inconsistent. `realized_mde` (`retail-power-limits/rplimits/cases.py:94-99`) carries 0.0512; at N_eff = 125.6 with sd 0.36339 the MDE would be 0.0648 — a factor of 1.27.
  - 125.6 is not reachable from 404 by the note's own stated route: 404/3.4 = **118.8**.
  - The repository's own prose gets this right elsewhere: `retail-power-limits/docs/the-power-limit.md:164-165` says "the effective day count fell from 427 to 125.6" inside the ADR-007 paragraph, correctly attributing it to the registration before collection.
- **Recomputation:** inputs `bootstrap standard error 0.02562` and `daily contrast sd 0.36339` (`NPDExperiment/reports/stage_b2/evaluation.md:81-82`), `t_critical=2.0` (`NPDExperiment/src/npd/config.py:119`); method `(sd/se)²` per `evaluator.py:529` and `t·se` per `evaluator.py:544`. Results: N_eff = **201.181 → 201.2**; MDE = 2.0 × 0.02562 = **0.05124 → 0.0512**. Cross-checks: 2.0 × 0.36339/√125.6 = **0.06485**; 427/3.4 = **125.588**; 404/3.4 = **118.824**. Tolerance 4 dp on the MDE, 1 dp on N_eff.
- **What would resolve it:** replacing "125.6 independent-equivalent days" with the achieved 201.2, or re-labelling the 125.6 as the pre-registration projection over the 427-day base — which the note's own prose already does correctly at `docs/the-power-limit.md:164-165`.
- **Confidence:** HIGH — the sibling states the achieved figure explicitly under a heading that names it as achieved, the code that computes it is present and unambiguous, and the stated pairing is arithmetically impossible under the note's own variance inflation.
- **Could later commits invalidate this?** No. `NPDExperiment` is closed at `2d3d0ae`, which is both the cited commit and the audit anchor, and `retail-power-limits` has had no commit since `dda39b2`.
- **Disclosed by the authors?** No. `DECISIONS.md` ADR-003 lists four corrections the note makes against the record it was handed; this is not among them, and `SOURCES.md:42` presents the figure under the heading **Sample achieved**.
- **Effect on the verdict:** none. The MDE 0.0512 is correct and still sits above the whole 0.01–0.05 band. The error makes NPDExperiment look about 38 % more underpowered than it was.
- **Citation check:** verified (quote EXACT and byte-for-byte at `SOURCES.md:42`, and identical in the generating Figure at `rplimits/cases.py:100-104`; figures all confirmed at their cited lines — `NPDExperiment/REGISTRATION.md:227,229`, `reports/stage_b2/evaluation.md:51,81,82,88,92`, `src/npd/eval/evaluator.py:529,544`, `src/npd/config.py:119`; recomputation reproduced independently in the audit venv from the stated primitives — N_eff = (0.36339/0.02562)² = 201.1813 → 201.2, MDE = 2.0×0.02562 = 0.05124 → 0.0512, MDE at N_eff 125.6 = 0.064850 (ratio 1.2656, so "a factor of 1.27" holds), 427/3.4 = 125.588, 404/3.4 = 118.824; severity S2 and label DERIVED confirmed; non-disclosure confirmed — ADR-003 at `DECISIONS.md:87-110` lists exactly four handed-over corrections and this is not among them, and 125.6 / 201.2 / 404 occur repo-wide only at `SOURCES.md:42`, `docs/the-power-limit.md:165` and `rplimits/cases.py:102`, none a disclosure). Corroborating detail found on re-check: within the single cited file `NPDExperiment/progress.md`, 404 appears only in the achieved-results table at `:147` and 125.6 only in the pre-collection A.0 power paragraph at `:319-320`, so the splice is visible inside the source the Figure names. Kept unchanged.

### AUDIT-C-retail-power-limits-2
- **Repository / SHA:** retail-power-limits / `dda39b2f148569a6fe9be956a979471b2330611d`
- **Hypothesis or artifact:** The "cheaper independent observation" bullet of §What would change the conclusion. Same root confusion as finding 1, different locus and a separate quote.
- **Direction:** B
- **Class:** INTERNAL_INCONSISTENCY
- **Severity:** S3
- **Label:** DERIVED
- **Claim challenged (verbatim):**
  > "NPDExperiment lost 70 percent of its sample to overlapping five-session horizons."

  — `retail-power-limits/docs/the-power-limit.md:379-380`.
- **Evidence:** The realized loss was **50.2 %**: 404 evaluable days (`NPDExperiment/reports/stage_b2/evaluation.md:51`) against an achieved effective sample of 201.2 (`evaluation.md:92`). The 70 % figure is the *registered projection*, 1 − 125.6/427, from `NPDExperiment/REGISTRATION.md:227`. The sentence is written in the past tense about what happened, inside a paragraph arguing that the count of independent periods was the binding constraint. It sits outside the four marker-delimited generated blocks and so is not covered by the repository's own drift test (`retail-power-limits/tests/test_render.py`).
- **Recomputation:** 1 − 201.2/404 = **0.5020**; 1 − 125.6/427 = **0.7059**. Tolerance 1 pp.
- **What would resolve it:** "NPDExperiment's registration projected a 70 percent loss to overlapping five-session horizons; the realized loss was 50 percent" — or simply the realized figure.
- **Confidence:** HIGH — both numbers are stated in the sibling and the arithmetic is one division.
- **Could later commits invalidate this?** No — same reasoning as finding 1.
- **Disclosed by the authors?** No.
- **Citation check:** verified (quote EXACT, ending at `docs/the-power-limit.md:380` as cited; figures re-confirmed at `NPDExperiment/reports/stage_b2/evaluation.md:51` and `:92`; recomputation reproduced — 1 − 201.2/404 = 0.50198 → 50.2 %, 1 − 125.6/427 = 0.70585 → 70.6 %; the subsidiary drift-test claim also verifies — the four generated blocks are `SOURCES.md` 27-155, 165-201 and 209-236 and `docs/the-power-limit.md` 69-76, `BLOCK_NAME` matches BEGIN markers only (`rplimits/docsync.py:33`), so line 379 lies outside every block and `tests/test_render.py` cannot pin it). One identity worth recording: 70 % is also exactly 1 − 1/3.4 = 0.7059, so the sentence restates the registered variance inflation in the past tense rather than reporting an independently formed figure. Kept unchanged.

### AUDIT-C-retail-power-limits-3
- **Repository / SHA:** retail-power-limits / `dda39b2f148569a6fe9be956a979471b2330611d`
- **Hypothesis or artifact:** The solattn `ContrastCase` — the note's own scope limit, offered as proof that not every closure in the program was a power closure.
- **Direction:** B
- **Class:** STATISTICAL
- **Severity:** S3
- **Label:** DERIVED
- **Claim challenged (verbatim):**
  > "**solattn** returned a powered null. … That is what a closure looks like when detectability is not the binding term: the design measured what it set out to measure, at full coverage, and the answer was no."

  — `retail-power-limits/docs/the-power-limit.md:295,300-302`; the same characterisation at `retail-power-limits/rplimits/cases.py:331` ("A powered null.") and `:342-347`.
- **Evidence:**
  - **No detectability figure exists for solattn anywhere.** The note's own practice rule (`retail-power-limits/docs/the-power-limit.md:322-324`) is that an MDE must be computed from dispersion and sample size; for the one case it labels "powered" it supplies none, and neither does solattn.
  - The interval it does supply spans zero and is wide relative to the point: lift −1.0779 with a 95 % interval **[−3.3354, +0.0204]** (`solattn/FINDINGS.md:98-99`), a width of 3.3558 on a point of 1.0779. solattn's own `p_raw` for that primary trial is 0.3054 (`FINDINGS.md:99`).
  - The clustering is on **three** birth days, 2026-08-16..18 (`solattn/FINDINGS.md:101-102`). solattn states the consequence for its own estimator: "With 3 day-clusters, `p_raw = 0.0000` carries almost no information. It means only that all **ten distinct day-multisets** share a sign — the resolution floor of the registered day-clustered bootstrap" (`solattn/FINDINGS.md:213-218`). The resolution-floor caveat does not reach `retail-power-limits`.
  - The word "powered" is `retail-power-limits`'s own. `solattn/FINDINGS.md` never uses it; its only use of the root is the **`underpowered` floor** at `:107-108`, and what clears that floor is the Q5 cell's 412 measurable pools — a cell-size rule, not a statement about the primary contrast's detectability.
  - solattn's registered justification for the kill is **outcome coverage** (100.0 % on every analysed cohort, `FINDINGS.md:104-105`) plus the Q5 floor. Both are real, and both are correctly transcribed. Neither is a detectability figure.
- **Recomputation:** interval width 3.3354 + 0.0204 = **3.3558**, ratio to |point| = **3.11**. Distinct multisets from resampling 3 clusters with replacement, C(5,3) = **10**, matching solattn's own figure. No further recomputation is possible: solattn's resample draws are not stored.
- **What would resolve it:** either a detectability figure for solattn's primary contrast — an MDE on the same 450 bps-net scale as the −1.0779 — or dropping "powered" for what the record supports: a fully covered null whose registered kill criterion fired, on three day-clusters.
- **Confidence:** MEDIUM — the label is a characterisation rather than a number, so it is not falsified the way a figure is; what is established is that no detectability evidence exists for it and that the cited interval's structure argues the other way.
- **Could later commits invalidate this?** No. `solattn/FINDINGS.md` is byte-identical between the cited `b3f5062` and solattn's anchored SHA, which are the same commit.
- **Disclosed by the authors?** Partially. The note carries both the interval and the three birth days (`retail-power-limits/SOURCES.md:184`, `retail-power-limits/docs/the-power-limit.md:299`), so a careful reader can see that the interval spans zero on three clusters; what is not carried is solattn's own resolution-floor consequence — that three clusters admit only ten distinct day-multisets (`solattn/FINDINGS.md:213-218`). Per the disclosure rule the finding is capped at S3, which is where it already sits.
- **Note on direction:** this cuts against the note's own scope limit rather than for it. If solattn is not securely a non-power closure, the note's disclaimer that not every closure in this program was a power closure rests on two contrast cases rather than three — which makes the note's headline *more* universal, not less. It is recorded as B because the note claims more about solattn than solattn's record supports.
- **Citation check:** corrected — the "Disclosed by the authors?" answer moves from **No** to **Partially**, and the evidence bullet's "None of this reaches `retail-power-limits`" becomes "The resolution-floor caveat does not reach `retail-power-limits`". The draft asserted that the three-cluster structure is not carried across; it is, twice and verbatim — `SOURCES.md:184` ("n = 12,798 amm pools over three birth days") and `docs/the-power-limit.md:299-300` ("on 12,798 pools over three birth days"). What genuinely does not cross is solattn's resolution-floor consequence: `grep -rn "multiset\|resolution floor"` over `SNAP/retail-power-limits` returns zero hits. Everything else verified: quotes EXACT at `docs/the-power-limit.md:295` and `:300-302` and at `rplimits/cases.py:331,342-347`; recomputation reproduced — width 3.3354 + 0.0204 = 3.3558, ratio to |−1.0779| = 3.113 → 3.11, and C(5,3) = 10 matching `solattn/FINDINGS.md:216` `distinct_day_multisets = 10`; the "no detectability figure anywhere" claim confirmed mechanically — grep of `solattn/FINDINGS.md` for `mde|minimum detectable|detectab` returns zero hits and the file's only use of the "power" root is "clear the 20-pool `underpowered` floor" at `:108`. Severity stays S3 (the disclosure rule caps it there; the finding's own MEDIUM confidence makes S3 a conservative rung rather than a wrong one).

### AUDIT-C-retail-power-limits-4
- **Repository / SHA:** retail-power-limits / `dda39b2f148569a6fe9be956a979471b2330611d`
- **Hypothesis or artifact:** The repository's count of its own evidence base, in five places.
- **Direction:** neutral
- **Class:** INTERNAL_INCONSISTENCY
- **Severity:** S3
- **Label:** READ
- **Claim challenged (verbatim):**
  > "The note quotes about ninety figures from seven repositories."

  — `retail-power-limits/DECISIONS.md:35-36`. Repeated as "It reads all seven sibling repositories and writes to none of them" (`retail-power-limits/DECISIONS.md:42-43`), "**Four of the seven source repositories are not published.**" (`retail-power-limits/docs/the-power-limit.md:44`), "**four of the seven source repositories have no remote.**" (`retail-power-limits/progress.md:113-114`), and "for four of the seven that promise is currently **conditional**" (`retail-power-limits/SOURCES.md:260`).
- **Evidence:**
  - `retail-power-limits/rplimits/sources.py` holds 24 `Source` entries citing **eight** distinct repositories: NPDExperiment (4), InsiderExperiment (5), ETFExperiment (4), HFExperiment (4), **AiTrader (2)**, MLCryptoEngine (2), solattn (2), solclear (1).
  - The repository's own publication table has **eight rows**, AiTrader among them: `retail-power-limits/SOURCES.md:262-271`.
  - Two of the five sentences enumerate eight in their own next clause. `docs/the-power-limit.md:46-47`: "The three contrast cases **and AiTrader** are public." `progress.md:115-116`: "The three contrast cases **and AiTrader** are public on GitHub." Four local-only plus three contrast cases plus AiTrader is eight.
  - AiTrader is not incidental: it is the sole source for the fourth power case's deciding number — the `aitrader-return` key backs the HFExperiment record at `retail-power-limits/rplimits/cases.py:256-262` and the fourth row of the headline table (z 1.668, the 2.50 bar, 104.0 needed, 70.5 delivered).
  - The test that would catch it cannot: `retail-power-limits/tests/test_sources.py:41-52` asserts `expected <= {source.repo for source in SOURCES.values()}` over a seven-element set that omits AiTrader — a subset assertion, so an eighth repository passes silently.
  - Origin, recorded in fairness: the count is inherited from the commissioning instruction. `retail-power-limits/progress.md:22-23` records that "The governing instruction named seven repositories to read in full and read-only", and the test's own docstring at `tests/test_sources.py:42` repeats it. That sentence about the instruction is not challenged here; the five sentences that use "seven" to count the note's *sources* are.
- **Recomputation:** distinct `Source.repo` values in `rplimits/sources.py` = **8** over **24** entries; rows in the `SOURCES.md` publication table = **8**.
- **What would resolve it:** "eight repositories", and "four of the eight are not published". The correction moves against the note's own interest: 4/8 = 50 % unpublished rather than the 57 % the text implies.
- **Confidence:** HIGH — the eighth repository is listed in the repository's own table and enumerated in two of the sentences that miscount it.
- **Could later commits invalidate this?** No — `retail-power-limits` has had no commit since `dda39b2`.
- **Disclosed by the authors?** Partially — AiTrader is named and its publication status given at `retail-power-limits/SOURCES.md:267`, so a reader can see the eighth. The count sentence is what is wrong, in five places. Per the disclosure rule the finding is READ and capped at S3, which is where it sits.
- **Citation check:** verified (all five loci quote-exact at their cited lines — `DECISIONS.md:36`, `DECISIONS.md:43`, `docs/the-power-limit.md:44`, `progress.md:114`, `SOURCES.md:260`; recount reproduced independently — `rplimits/sources.py` holds 24 `Source` entries over 8 distinct repositories with exactly the per-repo split stated (NPD 4, Insider 5, ETF 4, HF 4, AiTrader 2, MLCryptoEngine 2, solattn 2, solclear 1), and the `SOURCES.md` publication table has 8 data rows at `:264-271`; `tests/test_sources.py:41-52` re-read and confirmed to be a subset assertion over a hard-coded seven-element set omitting AiTrader, so an eighth repository passes silently; AiTrader's load-bearing role confirmed at `rplimits/cases.py:256-262`; inherited-count context confirmed at `progress.md:22-23` and `tests/test_sources.py:42`; label READ and the S3 cap confirmed — AiTrader is the fourth row of the publication table at `SOURCES.md:267` and two of the five sentences enumerate the eighth in their next clause). **Emphasis added:** the bold on "**and AiTrader**" in the evidence bullet is this audit's, not the sources' — `docs/the-power-limit.md:46-47` and `progress.md:115-116` carry no emphasis there. Kept unchanged otherwise.

### AUDIT-C-retail-power-limits-5
- **Repository / SHA:** retail-power-limits / `dda39b2f148569a6fe9be956a979471b2330611d`
- **Hypothesis or artifact:** The time row of the cost-asymmetry table, and the InsiderExperiment `cost` Figure it renders from.
- **Direction:** B
- **Class:** CROSS_REPO_INCONSISTENCY
- **Severity:** S3
- **Label:** READ
- **Claim challenged (verbatim):**
  > "| time | **411 minutes** of recorded stage time across six stages, of which collection alone was 194 | about **51 minutes** for Stage A.1 and 20 for the closure |"

  — `retail-power-limits/docs/the-power-limit.md:241`; the Figure it renders from is `retail-power-limits/rplimits/cases.py:164-168`.
- **Evidence:**
  - `InsiderExperiment/progress.md:115-119` records **two** figures and refuses to choose between them: "The commit record puts Stage A.1 at about 51 minutes of session wall clock, 18:20 to 19:11, and Stage Z.1 at about 20 minutes. **The Z.1 brief records five hours.** The commit record cannot confirm that figure, which presumably counts operator time between stages that this repository does not observe. **Both are recorded rather than one being picked.**"
  - `retail-power-limits` carries only the smaller pair. The table cell at `docs/the-power-limit.md:241` drops even the provenance qualifier; the `cost` Figure at `rplimits/cases.py:166` keeps "by the commit record" but names no alternative.
  - The magnitude matters to the row's own point: 51 + 20 = 71 minutes against NPDExperiment's 411 is a **5.8×** asymmetry; 51 + 300 = 351 against 411 is **1.2×**.
- **Recomputation:** 411/71 = **5.79**; 411/351 = **1.17**. Both figures are quoted, not derived; no further recomputation applies.
- **What would resolve it:** carrying both figures, as the sibling does — "about 51 minutes for Stage A.1 and either 20 minutes or five hours for the closure, depending on which of the two records the sibling itself declines to choose between".
- **Confidence:** HIGH — the competing figure and the instruction not to pick one are in the same paragraph of the cited file.
- **Could later commits invalidate this?** No. `InsiderExperiment` is closed at `12d9fd3`, the cited and anchored commit.
- **Disclosed by the authors?** Partially — `rplimits/cases.py:166` says "by the commit record", which signals the provenance without naming the alternative; the note's own table drops that qualifier entirely. Per the disclosure rule this is READ and capped at S3, which is where it sits.
- **Citation check:** verified (quote EXACT at `docs/the-power-limit.md:241`, the whole table row character for character including its bolds; the generating Figure confirmed at `rplimits/cases.py:164-168` with "by the commit record" at `:166`; the sibling passage verbatim at `InsiderExperiment/progress.md:115-119` including "The Z.1 brief records five hours." and "Both are recorded rather than one being picked."; recomputation reproduced — 411/71 = 5.7887 → 5.79×, 411/351 = 1.1709 → 1.17×, and the 411 itself re-verified as 22+34+68+52+194+41 = 411; label READ and the S3 cap confirmed). **Emphasis added:** the bold on those two sibling sentences in the evidence bullet is this audit's — `InsiderExperiment/progress.md:117,119` carries none. Kept unchanged otherwise.

### AUDIT-C-retail-power-limits-6
- **Repository / SHA:** retail-power-limits / `dda39b2f148569a6fe9be956a979471b2330611d`
- **Hypothesis or artifact:** The solclear `ContrastCase` deciding number — the survivorship result the note calls solclear's most transferable finding.
- **Direction:** neutral
- **Class:** ARITHMETIC
- **Severity:** S4
- **Label:** DERIVED
- **Claim challenged (verbatim):**
  > "archived-page sampling manufactures survivorship by 60 points at 30 days and 79 at 90, 97.5 percent death on 40 birth-ordered pools against 18.75 percent on 16 attention-crawled ones"

  — `retail-power-limits/SOURCES.md:196`, generated from `retail-power-limits/rplimits/cases.py:361-366`; restated at `retail-power-limits/docs/the-power-limit.md:310-312`.
- **Evidence:** `solclear/FINDINGS.md@c692032:120-123` gives the table: birth-ordered n = 40 (20 at 90 d), **dead at 30 d 97.5 %**, **dead at 90 d 100 %**; attention-crawled n = 16 (15 at 90 d), **dead at 30 d 18.75 %**, **dead at 90 d 40 %**. So the 30-day gap is 78.75 points and the 90-day gap is 60.0 — the reverse of the labels. The same `retail-power-limits` sentence supplies the 30-day pair (97.5 vs 18.75) as support for a "60 points at 30 days" claim that this very pair contradicts.
- **Recomputation:** 97.5 − 18.75 = **78.75** (30 d); 100 − 40 = **60.0** (90 d). Exact.
- **What would resolve it:** swapping the two horizon labels — "79 points at 30 days and 60 at 90".
- **Confidence:** HIGH — the source table is explicit and the subtraction is exact.
- **Could later commits invalidate this?** No. `solclear/FINDINGS.md` is byte-identical between the cited `c692032` and solclear's anchored `d298576`, so no later commit repairs it.
- **Disclosed by the authors?** No — but the error **originates in solclear**, whose own prose at `solclear/FINDINGS.md@c692032:125-126` reads "A 60-point gap at 30 days and a 79-point gap at 90 days" against its own table two lines above. `retail-power-limits` transcribed solclear's prose faithfully; the finding is that it repeated an error it also carries the data to catch. This is a contrast-case figure and nothing in the note's argument rests on which horizon carries which gap.
- **Citation check:** verified (quote EXACT at `SOURCES.md:196`, identical in the generating Figure at `rplimits/cases.py:361-366` and restated at `docs/the-power-limit.md:310-312`; the source table confirmed at `solclear/FINDINGS.md:120-123` — birth-ordered n = 40 (20 at 90 d), dead at 30 d 97.5 %, dead at 90 d 100 %; attention-crawled n = 16 (15 at 90 d), dead at 30 d 18.75 %, dead at 90 d 40 % — and its contradicting prose at `:125-126`; recomputation reproduced exactly — 97.5 − 18.75 = 78.75 at 30 d, 100 − 40 = 60.0 at 90 d; the byte-identity claim re-verified independently, `git -C solclear show c692032:FINDINGS.md` returning the same table at the same lines and `git diff c692032 d298576 -- FINDINGS.md` returning empty, so no later commit repairs it). Severity note: S4 is a conservative rung — labels contradicting a table quoted inside the same sentence reads as S2 — but the finding records its own reasons (a contrast-case figure, sibling origin, nothing in the argument resting on it), so it is left as written. Kept unchanged.

### AUDIT-C-retail-power-limits-7
- **Repository / SHA:** retail-power-limits / `dda39b2f148569a6fe9be956a979471b2330611d`
- **Hypothesis or artifact:** The publication disclosure (provenance claim P-14) — the repository's own statement of how checkable its citations are.
- **Direction:** neutral (pure hygiene; the error runs *against* the note's interest, telling readers to discount evidence that is in fact now checkable)
- **Class:** STALE_FIGURE
- **Severity:** S4
- **Label:** DERIVED (git remotes, push reflogs, `.git/config` mtimes)
- **Claim challenged (verbatim):**
  > "**Four of the seven source repositories are not published.** The four power cases — NPDExperiment, InsiderExperiment, ETFExperiment and HFExperiment — exist only on the operator's machine and have no remote."

  — `retail-power-limits/docs/the-power-limit.md:44-46`; tabulated as "**no — local only, no remote** | requires the operator's working copy" four times at `retail-power-limits/SOURCES.md:268-271`, and recorded as a discovery at `retail-power-limits/progress.md:113-116`.
- **Evidence:**
  - All four repositories now carry a GitHub remote. `git -C <repo> remote -v`, read **2026-09-04T00:10:56Z** and again at **00:18:21Z** (UNANCHORED, live working tree): each returns `origin https://github.com/kirosli00tuff/<repo>.git`.
  - The remotes were added **after** the note. `git reflog show <remote branch>` gives a single "update by push" entry each: ETFExperiment `origin/master` 2026-08-29T11:45:06−07:00, HFExperiment `origin/main` 11:45:10, InsiderExperiment `origin/master` 11:45:14, NPDExperiment `origin/main` 11:45:18. The four `.git/config` mtimes match those times to the second, and each `.git/refs/remotes/origin/` was created in the same minute.
  - `retail-power-limits`' last commit is `dda39b2`, 2026-08-29T00:21:28−07:00. The gap is **11 h 23 m 38 s**.
  - So the claim was **true when written and committed**, and became false the same day.
- **Recomputation:** none beyond the timestamp comparison — `dda39b2` author date 2026-08-29T00:21:28−07:00 against the earliest push reflog entry 2026-08-29T11:45:06−07:00.
- **What would resolve it:** recording in `SOURCES.md:262-271`, `docs/the-power-limit.md:44-52` and `progress.md:113-123` that the four were published on 2026-08-29 and that every citation in the registry now resolves against a public remote — exactly the outcome `SOURCES.md:279-282` anticipated. No figure changes; only the checkability disclosure does.
- **Confidence:** HIGH — remotes, reflog entries and config mtimes are unambiguous and mutually corroborating, and the direction of the gap is not close.
- **Could later commits invalidate this?** No. `retail-power-limits` has had no commit since `dda39b2`, so the stale text still stands; a later commit updating the disclosure would *resolve* the finding, not invalidate it. The underlying fact is unanchored — remotes are not versioned and could change again after the read times above.
- **Disclosed by the authors?** Partly, and honestly. The note anticipated exactly this change and built for it: "every citation carries the commit hash that will resolve against them if they ever are" (`docs/the-power-limit.md:49-51`) and "**if any of the four is published later, every citation in this file resolves against it without amendment**" (`SOURCES.md:279-281`); `progress.md:113` also records that the fact was "Checked at push time rather than assumed". What is not disclosed is that the publication then happened. That anticipation is why this is S4 and not higher.
- **Citation check:** verified (quote EXACT at `docs/the-power-limit.md:44-46`, em dashes and all; the four table rows verbatim at `SOURCES.md:268-271` and the `progress.md` restatement at `:113-116`; the anticipation passages verbatim at `docs/the-power-limit.md:49-51`, `SOURCES.md:279-282` and `progress.md:113`; the live-repo evidence re-run independently about five hours after the original pass and reproducing exactly — reads at **2026-09-04T05:14:41Z–05:14:50Z**, UNANCHORED, since remotes, reflogs and mtimes are not versioned and may change again: `git remote -v` returns `origin https://github.com/kirosli00tuff/<repo>.git` for all four power cases; one "update by push" reflog entry each — ETFExperiment `origin/master` 2026-08-29 11:45:06 −0700, HFExperiment `origin/main` 11:45:10, InsiderExperiment `origin/master` 11:45:14, NPDExperiment `origin/main` 11:45:18 — with `.git/config` mtimes matching to the second, against `retail-power-limits` HEAD `dda39b2` authored 2026-08-29 00:21:28 −0700, a gap of 11 h 23 m 38 s as stated). Kept unchanged.

### AUDIT-C-retail-power-limits-8
- **Repository / SHA:** retail-power-limits / `dda39b2f148569a6fe9be956a979471b2330611d`
- **Hypothesis or artifact:** The repository's own gate self-report.
- **Direction:** neutral
- **Class:** INTERNAL_INCONSISTENCY
- **Severity:** S4
- **Label:** DERIVED
- **Claim challenged (verbatim):**
  > "Ruff format and check clean, mypy strict clean over 11 source files, 111 tests passing."

  — `retail-power-limits/progress.md:67-68`; restated as "`tests/`, 111 tests" at `retail-power-limits/progress.md:59`.
- **Evidence:** The anchored tree collects **112** tests, not 111: `tests/test_sources.py` 74, `tests/test_cases.py` 19, `tests/test_honesty.py` 10, `tests/test_render.py` 9. The "11 source files" half is **correct** — 6 `.py` files under `rplimits/` and 5 under `tests/`, which is exactly mypy's configured scope (`retail-power-limits/pyproject.toml:41-46`, `files = ["rplimits", "tests"]`).
- **Recomputation:** the anchored tree was copied to the audit work directory and collected with the repository's own pinned pytest; `112 tests collected in 0.04s`. Nothing was executed inside the audited repository. The one test that fails in the copy, `test_the_credential_scan_has_something_to_scan`, calls `git ls-files` and cannot pass outside a work tree — an artefact of the copy, not a repository defect.
- **What would resolve it:** "112 tests passing".
- **Confidence:** MEDIUM — collection counts can move with a pytest version, and the repository's own interpreter was used to minimise that risk, but it cannot be ruled out that the author counted at a moment when the suite held one test fewer.
- **Could later commits invalidate this?** No — there has been no commit since `dda39b2`.
- **Disclosed by the authors?** No. Nothing in the note rests on it; this is hygiene only.
- **Citation check:** verified (both quotes EXACT — `progress.md:67-68` and `progress.md:59`; the 112 reproduced by a second, independent method needing no pytest at all, static enumeration of the four test modules and their parametrize sources: `test_sources.py` 3 tests × 24 `SOURCES` keys + 2 plain = 74; `test_cases.py` (7 + 4 + 3) parametrized + 5 plain = 19; `test_honesty.py` (2 + 2) parametrized + 6 plain = 10; `test_render.py` (3 + 1) blocks + 5 plain = 9; total 74+19+10+9 = **112**, matching the pytest collection exactly; the "11 source files" half re-confirmed as 6 `.py` under `rplimits/` and 5 under `tests/`). One citation-range repair: the mypy scope line is `pyproject.toml:46`, not inside the `:41-45` range the draft gave, so the reference is widened to `:41-46` — the range now contains the `files = ["rplimits", "tests"]` line it is cited for. The stated reason for MEDIUM confidence — that a pytest version could move the collection count — is closed off by the static count, since every parametrize argument is frozen data in the tree (24 sources, 4 + 3 cases, 4 BEGIN markers, 2 + 2 pinned documents); the confidence is left at MEDIUM as written rather than raised, and the finding is otherwise kept unchanged.

### Consolidation record

Nine drafts entered consolidation: DRAFT-V-1 through DRAFT-V-8 from the verification pass and
DRAFT-P-1 from the provenance pass. **One de-duplication:** DRAFT-V-3 and DRAFT-P-1 are the same
finding — the four-of-seven publication disclosure — and are merged as
AUDIT-C-retail-power-limits-7, keeping the provenance pass's stronger evidence (the push reflog
entries) alongside the verification pass's mtime bracket. **No draft was dropped**: every one
carries a verbatim quote with a file and line that were re-located in `SNAP/retail-power-limits`
during consolidation, and a figure or figures re-derived here. DRAFT-V-1 and DRAFT-V-8 share a root
cause (the 427-vs-404 base for 125.6) but were kept separate because they challenge different
sentences in different files at different severities and admit different repairs; each is
cross-referenced to the other. Finding 4 gained a fifth locus during consolidation
(`DECISIONS.md:42-43`, "It reads all seven sibling repositories"), which the draft did not list, and
gained the note that the seven-count is inherited from the commissioning instruction
(`progress.md:22-23`, `tests/test_sources.py:42`).

---

## Sound

Recorded because a sound result is a result. Everything below was checked and verified.

**The four deciding numbers, from the siblings' own primitives.** NPD's realized MDE 0.0512
(`2.0 × 0.02562`, `evaluation.md:81` → `evaluator.py:544`); Insider's 49.35 bp/month (TE 9.993 %/√12
= 288.47 bp, N_eff months 2,869.9/21 = 136.66, SE 24.676, ×2.0 = **49.353**); ETF's 163-vs-300 at
the 2027-03-31 deadline; HF's z 1.668 with delivered 27.99 × 252 = **70.53 %/yr**, needed
66.4 × 2.50/√2.55 = **103.95 → 104.0**, shortfall **1.475 → 1.5×**.

**Transcription fidelity.** All 24 citations resolve, `rev-parse --disambiguate` returning exactly
one object for each short hash; every claimed date equals the actual author date; every named path
exists at its commit; **every cited file is byte-identical between the cited commit and its
sibling's anchored SHA** — the drift ADR-001 warns about has not occurred anywhere. All eight quoted
commit subjects are verbatim, and all four "Closure language, exact." blocks are verbatim.

**The one derived figure, and the claim that it is the only one.** 22+34+68+52+194+41 = **411**,
each addend present in `NPDExperiment/progress.md`, the six timed stages the complete set, the Z.1
exclusion note correct. Every other ratio a verifier would suspect the note of forming itself —
137 and 74, 37.6×, 1,700×, 100×, 100–180×, 1.5×, "eight to eleven years", 418 bp, 96.1 %, 302 — is
stated verbatim by the sibling that owns it, not formed here.

**The provenance spine, in its strongest available form.** `fbfc74e` is genuinely
InsiderExperiment's first commit; its Section 0 carries the 20/40 bp bars and the inclusive-boundary
convention ("An MDE of exactly 20.00 bp is GO"); its tree contains no corpus and an empty
`portfolio/`; and Section 0 lines 1–159 are **byte-identical from that first commit to the closing
commit `12d9fd3`**, across the corpus build, the power measurement and the closure. The four bar
constants in `src/insider/config.py` were set in the first commit and never touched.

**No undated parameter change anywhere.** Thirteen parameter-change rows across the four power
cases: every one carries a dated amendment recording what data existed when it was made. NPD's
power floor, effect band and five-session primary horizon never moved; ETF's 2027-03-31 deadline
never moved and its one governing-N change (237 → 300) moved the bar *against* the experiment and
carried Amendment 4; HFExperiment's registration is append-only in fact, its single deletion in the
whole history being a placeholder line.

**Arithmetic and census.** The 336-row ETF census sums; 415/432 = **96.065 % → 96.1**;
11/333 = **3.3033 % → 3.30**; 300−163 = **137** and 237−163 = **74**; 4,695,489/124,764 =
**37.635 → 37.6×**; the progression clock's two gaps; NPD's grid cells at corr 0 and corr 0.7;
NPD's sd at **97.85 % → 98** of the corr −1 theoretical maximum 0.37139; the Šidák level
`1 − 0.95^(1/160) = 0.000321`; the Bonferroni bar `z(1 − 0.0125/2) = 2.4977 → 2.50`.

**The repository's own drift guarantee.** `Figure.__post_init__` (`rplimits/cases.py:29-33`) raises
on an unresolvable source or an empty value; the four generated blocks are re-rendered and compared
by `tests/test_render.py`; all render and drift tests pass on a scratch copy of the anchored tree.
`rplimits/` imports only `dataclasses`, `pathlib`, `re` and its own modules — no `subprocess`, no
network, no path outside `ROOT` — and no sibling has any commit dated 2026-08-29, so the claim that
this repository wrote to nothing holds.

**What I would have expected to find if the thesis were that this note's numbers or provenance were
loose, and did not find:** a figure that does not exist at its cited commit; a deciding number that
does not reproduce; a paraphrased commit subject; an inexact "Closure language, exact." block; a
derived figure smuggled in as a quotation; a bar edited without an amendment; a hash that does not
resolve; a "registered before" that postdates its data. None of these occurred.

## Could not be checked and why

1. **The four power-case repositories' internal correctness.** This audit verified that
   `retail-power-limits` transcribes them accurately. Whether NPDExperiment's bootstrap, or
   InsiderExperiment's tracking-error estimate, or ETFExperiment's simulation is itself right is a
   question about those repositories, not this one.
2. **The tail of InsiderExperiment's registered `t = 2.0`.** Neither repository states whether it is
   one- or two-sided, so the implied α is ambiguous between ≈0.023 and ≈0.046. **UNVERIFIABLE.** It
   does not move the verdict: at t = 1.645 the MDE would be 40.6 bp, still above the 40 bp floor.
3. **ETFExperiment's significance level.** The 0.80 target power is stated in
   `ETFExperiment/REGISTRATION.md:1017-1021`; the alpha is stated in **neither** repository.
   **UNVERIFIABLE.**
4. **AiTrader's z 1.668 and 1.455 as numbers.** They are Newey-West-at-21-lags bootstrap figures and
   the daily series is not stored in a form I can redraw. The iid TE-ratio approximation gives 1.696
   and 1.274, bracketing the first and not the second; that is a difference between two
   standard-error conventions, not a discrepancy adjudicable without AiTrader's holdout series.
   **UNVERIFIABLE** as re-derivation; **VERIFIED** as transcription.
5. **"the largest raw outperformance this project has ever measured."** Verified to be AiTrader's own
   sentence at `RETURN.md@f819b68:2844`; AiTrader's whole hypothesis register was not enumerated to
   test the superlative. **UNVERIFIABLE** as a fact, **VERIFIED** as a quotation.
6. **"No later AiTrader commit re-scores that holdout for H-F."** The `a0a9ef6` subject was verified
   verbatim and `RETURN.md` is unchanged between `f819b68` and AiTrader's anchor `705e0ed`;
   AiTrader's full subsequent history was not walked for a re-scoring elsewhere. **UNVERIFIABLE**
   without a full-history sweep of a repository outside this task's scope.
7. **"about ninety figures."** No counting convention is stated anywhere. The note carries 115
   distinct numeric tokens and `cases.py` Figures carry 133, so the claim is an undercount rather
   than an overstatement, but there is no rule against which to call it right or wrong.
   **UNVERIFIABLE.** (The "seven repositories" half of the same sentence *is* checkable and is
   finding 4.)
8. **ETFExperiment's 163 as a derivation.** Projecting 20.8 admissible days/month from this note's
   own date to the deadline and adding the 11 held gives 157.2, not 163. The gap is explained inside
   ETFExperiment — 163 is its "all cohorts" projection (`progress.md:486`) while the 291-plus-11 that
   yields 302 is "forward-only" (`REGISTRATION.md:1129-1130`) — but the accrual start date for the
   all-cohorts series is stated nowhere, so the 163 cannot be re-derived. **UNVERIFIABLE** as a
   derivation; **VERIFIED** as a transcription, which is all `retail-power-limits` claims for it.
9. **Whether InsiderExperiment's sealed store was ever actually opened** (provenance P-17, second
   half). The structural evidence is strong: `read_sealed_returns` is defined exactly once
   (`src/insider/eval/evaluator.py:33`), no module in `src/` calls it, the only call site anywhere is
   a guard test asserting that the call *raises*, and `tests/test_guards.py:160-167` fails the build
   if a second definition or a non-evaluator caller appears. But no read-audit artifact exists, so
   "never read" rests on that plus the repository's own statement. **PARTIAL, not contradicted.**
10. **Whether untracked data existed in InsiderExperiment's working tree at 18:34:56**
    (provenance P-02, sub-condition d). Git cannot answer this. Filesystem mtimes read
    2026-09-04T00:17:57Z (UNANCHORED) put `var/insider_market.db` at 18:36 and the other three stores
    at 19:05, all after the gate commit, and the `fbfc74e` tree contains no data file at all — the
    claim is supported on every available piece of evidence, but the negative is not provable from
    git alone.
11. **The exact wall-clock time of NPDExperiment's first billed API call.**
    `reports/stage_b1/calibration.json` carries no timestamp field, so the bound used is the commit
    that introduced the artifact (`3c2a152`, 10:12:23). Either bound leaves ADR-007 and Section 9.2
    (root `64b7d41`, 09:39:00) comfortably earlier, so tightening it would not change the verdict.
12. **Two sibling-side quirks, recorded and explicitly not charged to this repository.**
    NPDExperiment's per-call price (920 × 0.007508 = 6.907 against the stated 6.9378, a 0.4 % gap) is
    a rounding artefact inside `NPDExperiment/progress.md:201-202`, faithfully transcribed here.
    HFExperiment's closing commit `f13e1d3` is stamped 2026-08-25T00:45 yet records an instruction
    dated 2026-08-26; `retail-power-limits` transcribes HFExperiment's own stated date correctly.
    Also recorded and not raised: `sources.py:125` labels `etf-disarm` (`4d11002`) a "(closing
    commit)" though its subject is a post-closure correction — the note's own `progress.md:40` says
    it read ETFExperiment's "both closing commits", so the usage is internally consistent and
    disclosed. Whether solclear's "2026-08-14" is a UTC or local convention is solclear's question,
    not this repository's; the transcription is faithful either way.

## Live-repo access log

Merged from the two passes that touched live repositories. **The consolidation pass itself made no
live-repo access**: every quote and figure re-checked here was read from
`SNAP/retail-power-limits/` and the sibling snapshots at their anchored SHAs. All access below was
read-only, for the two permitted purposes — git history/provenance, and confirming the working tree
matched the anchor. **No file in any audited repository was opened for writing.** No `.env`,
keystore, session or credential file was read.

**Provenance pass window:** 2026-09-04T00:10:56Z – 00:20:01Z.
**Verification pass window:** 2026-09-04T00:13:58Z – 00:25:30Z.

`git status --porcelain` was taken over all nine repositories before the first access and after the
last access of each pass. **All four captures are identical**, verbatim:

```
retail-power-limits   (clean)
InsiderExperiment     (clean)
NPDExperiment         (clean)
ETFExperiment         (clean)
HFExperiment          ?? Accept:
                      ?? GET
                      ?? Host:
                      ?? User-Agent:
AiTrader               M COLLECTION_LOG.md
MLCryptoEngine        (clean)
solclear              (clean)
solattn               (clean)
```

The only entries are the two pre-existing conditions the common rules name as not the auditor's:
HFExperiment's four stray files (`Accept:`, `GET`, `Host:`, `User-Agent:`) and AiTrader's
` M COLLECTION_LOG.md`, which a collector appends to. **Nothing was modified by this audit.**

| command | repositories | time (UTC) | purpose |
|---|---|---|---|
| `git status --porcelain` | all 9 | 00:10:56Z (provenance before), 00:13:58Z (verification before) | mandatory before-logs |
| `git log -1 --format=…`, `git rev-list --max-parents=0` on `2d3d0ae`, `fbfc74e`, `cb17046`, `12d9fd3` | NPDExperiment, InsiderExperiment | 00:11–00:14Z | the progression clock (C-05) and the first-commit claim (P-02) |
| `git show fbfc74e:REGISTRATION.md`, `git diff fbfc74e cb17046 -- REGISTRATION.md`, `git ls-tree -r fbfc74e`, `git log -- src/insider/config.py` | InsiderExperiment | 00:12–00:14:4xZ | the 20/40 bars before the measurement, and Section 0 byte-identity (P-02, P-06, P-19) |
| `git log --format=…`, `git log -1` on `3f5d629`, `fe60a22`, `4d11002`, `97da329`, `4b9c874`, `815f888`, `44567f6`, `cf6efaf`; `git show fe60a22:README.md`; `git diff fe60a22 4d11002 -- README.md` | ETFExperiment | 00:15:22–00:15:4xZ | closure, amendments, the registered deadline (C-03, C-21, P-12, P-21) |
| `git log -1` on `f819b68`, `a0a9ef6`, `00c2d17`; `git show f819b68:RETURN.md` (grep only) | AiTrader | 00:15:35Z | the HF inherited figures (C-04, C-08, C-22, P-20) |
| `git log -1` on `f13e1d3`, `0a0d214`, `a8f4b0d`; `git show f13e1d3:REGISTRATION.md`; `git show 0a0d214:README.md`; `git log -- REGISTRATION.md` with a per-commit grep for "2,061" | HFExperiment | 00:16:11–00:16:5xZ | Section 11 and its registration date (C-23, P-10, P-13) |
| `git log -1` on `d2a0f05`, `ae03bf6`; `git show` both cited files | MLCryptoEngine | 00:18:00Z | the contrast-case margins (C-25) |
| `git log -1` on `c692032`, `8a49833`, `f0244eb`; `git show c692032:FINDINGS.md` | solclear | 00:17:32Z | the survivorship table and Stage E (C-26, P-09, finding 6) |
| `git log -1 b3f5062`; `git show b3f5062:FINDINGS.md` | solattn | 00:17–00:19Z | the primary trial and the sweep (C-24, T-05, finding 3) |
| `git remote -v`; `git reflog show <remote branch>`; `for-each-ref` | all 8 siblings | 00:10:56Z and 00:18:21Z | the publication disclosure (P-14, finding 7) — **UNANCHORED** |
| `stat .git/config`; `ls .git/refs/remotes/` | the four power cases | 00:18:32Z | dating when the remotes were added — **UNANCHORED** |
| `ls`/`stat` on `var/` | InsiderExperiment | 00:17:57Z | data-first-existed bounds (P-02) — **UNANCHORED** |
| `git rev-parse --disambiguate`, `cat-file -e`, `ls-tree`, `show` over all 24 citations | all 8 siblings | 00:19:0xZ | citation resolution (P-11) |
| `git diff <cited> <anchor> -- <path>` for the 7 cited files whose commit differs from the sibling anchor | HFExperiment, AiTrader, MLCryptoEngine, solclear, ETFExperiment | 00:19:13Z | drift check (P-11, ADR-001) |
| `git status --porcelain` | all 9 | 00:20:01Z (provenance after), 00:25:30Z (verification after) | mandatory after-logs |

**Unanchored reads.** The only unanchored facts in this report are the `git remote -v` results, the
push reflog entries, the `.git/config` mtimes and the `var/` file mtimes, read at
2026-09-04T00:10:56Z–00:18:32Z. Remotes, reflogs and mtimes are not versioned and may change again.
Everything else was read either from `SNAP/<repo>/` at the audit anchors or from git objects, which
cannot change.

**Scratch work.** All under the audit work directories
(`…/scratchpad/work/agentC-verify/` and the provenance pass's equivalent): the recomputation and
quote-check scripts, the 24-citation resolution sweep, and a copy of the anchored
`retail-power-limits` tree used only to collect and run its own test suite. No repository script was
executed in place; the only binary used from an audited tree was `retail-power-limits/.venv/bin/python`,
invoked with its working directory inside the scratch copy. The consolidation pass added only
read-only `awk`/`grep`/`sed` over `SNAP/` and one arithmetic script under
`…/scratchpad/work/`.
