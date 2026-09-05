# NPDExperiment — Agent C findings (referee and verifier)

Repository: `NPDExperiment`
Anchored SHA: `2d3d0aebf977fb2821ec78c25b370c84ec055920` (main, 2026-08-25) — also the live `HEAD`,
so the anchor is the last commit and the repository is closed (`_CLOSED_DO_NOT_RUN_HERE`, 2026-09-02).
Agent: **C** (referee; no thesis). Consolidated 2026-09-04.

Inputs merged: `findings/agentC/verification/NPDExperiment.inventory.md` and `.inventory.json`;
`findings/agentC/verification/NPDExperiment.verification.md` and `.claims.json`;
`findings/agentC/provenance/NPDExperiment.md` and `.json`.
Snapshot re-read for this pass: `SNAP/NPDExperiment/` (tracked, anchored) — every quote below was
re-located in the snapshot at the line cited. Live git objects and the untracked stores and ledgers
were re-read read-only on 2026-09-04 23:06–23:07 UTC for the three load-bearing recomputations; see
§Live-repo access log.
An independent citation-check pass then re-located every quote at its cited line, re-confirmed every
cited figure and re-ran every recomputation; its result is recorded as a **Citation check** bullet on
each finding. Nine findings entered that pass and nine leave it: **four verified unchanged, five
corrected** (AUDIT-C-NPDExperiment-**1**, **-2**, **-3**, **-4** and **-9**, each a citation, count or
wording repair that leaves the finding's substance, class and severity unchanged), **none dropped**.

**Anchoring caveat that governs every outcome figure.** Nothing under `var/` or `ledgers/` is tracked.
`var/npd.db`, `var/npd_sealed.db`, `var/npd_fit.db`, `ledgers/spend.jsonl` and `ledgers/evidence.jsonl`
exist only in the working tree. Every B.1 and B.2 number in this report verifies against those files as
read 2026-09-04; none of them verifies against `2d3d0ae` itself, because `2d3d0ae` contains no ranking,
no forward return and no ledger row. Their mtimes (2026-08-25) and the exact agreement of every derived
count with a tracked figure make post-anchor mutation implausible, but that is inference, not proof.

---

## Summary

The machinery reproduces. The block bootstrap, the permutation null, the negative-control gate, the
verdict rule, the registered power grid, the spend ledger and the Section 0 coverage gate all recompute
from the repository's own stored primitives, most of them exactly to the printed digit, and the closure's
deciding numbers — realized MDE 0.0512, verdict row 3, coverage 96.1 percent GO, spend 6.9378 USD under
a 10 USD cap — are correct. The pre-registration ordering holds under git: the binding registration was
committed 31 minutes before the first billed call, and the outcome map, power floor, verdict table,
horizons, baselines and spend cap are byte-identical from that commit to the anchor.

Nine findings survive consolidation. One is S1: the closure's causal account of why its own power fell
short rests on a "strong negative correlation" between the model and momentum daily ICs, and the measured
correlation is **+0.1182** — weakly positive. The remaining eight do not move the verdict: a registered
B.2 deliverable that was never produced, three records of mid-run amendments whose counts do not match the
ledgers they describe, a threshold called "registered" that appears in no version of the registration, and
three hygiene items. What could not be checked is stated as such and not guessed at: two Amendment 4
projections and one Amendment 5 figure rest on inputs the ledger discarded, the predecessor AiTrader
figures carried into the registration are external, and no hash of the sealed store was ever recorded.

---

## Verification scoreboard

### Claims

| Status | Count |
|---|---|
| VERIFIED | **20** |
| CONTRADICTED | **6** |
| UNVERIFIABLE | **4** |
| **Total claims audited** | **30** |

Two of the four UNVERIFIABLE rows are unverifiable only in part: `reports/session_record.html:192`
verifies on modules (38) and lines (4,699) and is unverifiable on "113 tests" (`def test_` counts 107 at
`433dabe`; establishing pytest's collected count would require running the suite, which the audit rules
forbid); `REGISTRATION.md:612` verifies on "recorded 0.3494" (0.349374, exact) and on "46 percent"
(45.65 %) and is unverifiable on "actual 0.6429". The two wholly unverifiable rows are Amendment 4's
latency and spend projections (finding **-3**). Separately, §B of the verification pass recomputed **18**
derived quantities from stored primitives; all 18 reproduce, and four of them (D6, D7, D11, D12) are
quantities the documents never state and which carry findings **-1** and **-2**.

**MUST-VERIFY claims (the 13 marked `[MV]` in the inventory), with status:**

| Rank | Claim | Status |
|---|---|---|
| 1 | "**The realized 0.36339 sits at 98 percent of that maximum.** The model daily rank IC and the momentum daily rank IC are therefore strongly negatively correlated across this window" (`reports/stage_b2/evaluation.md:229-233`) | **CONTRADICTED** — measured ρ = **+0.1182** on n = 404 (finding **-1**). The "98 percent" arithmetic itself verifies (0.36339 / 0.3714 = 0.9785) |
| 2 | "\| realized minimum detectable contrast \| **0.0512** \|" (`reports/stage_b2/evaluation.md:93`) | **VERIFIED** — recomputed 0.0512418 |
| 3 | "\| does not beat coin \| **YES** \|" and the Closed verdict row (`reports/stage_b2/evaluation.md:123,127`) | **VERIFIED** — model interval −0.027575…+0.039729, low < 0, so row 3 fires under `evaluator.py:686-706` |
| 4 | "coverage: **96.1%**" / "## Section 0 verdict: **GO**" (`reports/stage_b1/collection.md:33,41`) | **VERIFIED** — 415 stored / 432 eligible = 0.960648, ≥ 0.90 ⇒ GO |
| 5 | "total spent: **6.9378 USD** of a 10.00 USD cap" / "gate calls billed: **920**" / "0.007508 USD" (`reports/stage_b1/collection.md:47-51`) | **VERIFIED** — Σ = 6.9377835 over 922 rows; 920 gate rows, mean 0.00750789; 10 − Σ = 3.062216 |
| 6 | "\| **two-sided p** \| **0.5174** \|" (`reports/stage_b2/evaluation.md:113`) | **VERIFIED** — 0.5174483, 5,174 hits in 10,000 draws at seed 20260845 |
| 7 | "\| shuffled mean daily rank IC \| **+0.0001** \|" … "**Gate verdict: PASS.**" (`reports/stage_b2/evaluation.md:36,42`) | **VERIFIED** — +0.00011025 against a tolerance of 0.02 and a null sd of 0.0092549 (the word "registered" attached to that tolerance is finding **-6**) |
| 8 | "MDE = 2.0 * 0.185695 / sqrt(432) = 0.01787" and "VIF … = 3.4 … 427 evaluable days to **125.6**" (`REGISTRATION.md:212,225-227`) | **VERIFIED** — 0.18569534, 0.0178685, 3.4, 125.588, and all 16 grid cells reproduce |
| 9 | "The 26 superseded attempts stay in the ledger and their 0.0286 USD still counts against the cap." (`reports/session_a1_b1.md:254-255`) | **CONTRADICTED** — the ledger holds **74** superseded attempts costing **0.318852 USD** (finding **-5**) |
| 10 | "Every stored ranking carries `7e6f3d6801506bd7…`" / "**zero** of the 415 stored rankings" from the superseded template (`REGISTRATION.md:780-781`) | **VERIFIED** — all 883 current-procedure rows carry that one digest, no second digest appears, and the 415 stored days are drawn from those rows |
| 14 | "requires roughly **four times the evaluable days**, landing near **1,700 trading days**" (`REGISTRATION.md:716-718`) | **VERIFIED** — 4 × 427 = 1,708; MDE at 4× days = 0.02562, at the 0.026 floor of the registered projection |
| 16 | "B.2 reports the outcome split by realized effort alongside the primary contrast." (`REGISTRATION.md:534-536`) | **CONTRADICTED** — no effort split exists in the 260-line B.2 report, and neither `evaluator.py` nor `report.py` contains an effort term (finding **-2**) |
| 18 | "The evaluable counts are 427 at the five-session horizon and 431 at the one-session horizon." (`REGISTRATION.md:92-93`) | **VERIFIED** — 5 dates all-null at h = 5 ⇒ 427; 1 all-null at h = 1 ⇒ 431 |

10 VERIFIED, 3 CONTRADICTED, 0 UNVERIFIABLE.

### Intervals

| Metric | Count |
|---|---|
| Intervals audited | **11** |
| Independence doubtful | **1** |
| Recomputed | **10** |
| Conclusion moved | **0** |

Every interval in this repository that bears on a conclusion is the same object:
`block_bootstrap_interval` (`src/npd/eval/evaluator.py:160-190`) — a moving-block bootstrap, 10,000
resamples, block length `2 × primary_horizon_sessions` = 10, formed as `point ± 2.0 × sd(bootstrap
means)`. It is a **normal-approximation interval on the bootstrap SE, not a percentile interval**, and
`t_critical = 2.0` is a registered constant, not a t-quantile at any dof. Both facts are stated in advance
at `REGISTRATION.md:184-185`. The data are one scalar Spearman rank IC per trading day over a 30-name
panel; at the primary horizon consecutive days share four fifths of their forward window, so a block of 10
spans the whole dependence range. The realized variance inflation implied by the bootstrap is **2.01**
(n_eff 201.2 on 404 days), i.e. *below* the registered assumption of 3.4 — the overlap penalty the authors
budgeted for was larger than the one they paid.

**Independence doubtful (1):** the secondary-horizon interval (`evaluation.md:170`). `evaluator.py:508`
sets the block from `2 × primary_horizon_sessions` regardless of the horizon being evaluated, so a block
of 10 is applied at a one-session horizon where consecutive days share nothing. The registration fixes the
block only for the primary (`REGISTRATION.md:143-146`), so this is an unregistered code choice made in the
same commit as the run. **It is conservative in fact and it moves nothing.** Recomputed at block 1 the
interval is *wider* (−0.069963…+0.009967, SE 0.019982) than the reported block-10 one
(−0.067690…+0.007694, SE 0.018846); "excludes zero: False" holds under both, and the secondary is
explicitly barred from changing the verdict (`evaluation.md:153-154`). Recorded, not raised as a finding.

**Not recomputed (1):** the predecessor council interval −22.5 to +21.4 bp on 274 calls / 80 clusters
(`REGISTRATION.md:38-39`), carried in as text from AiTrader. No input, estimator or code for it exists in
this repository.

**Recorded, not raised.** The registered projection band "0.026 to 0.047" (`evaluation.md:94`,
`REGISTRATION.md:231-245`) is an analytic grid that holds *both* daily IC series at the null sd 0.185695.
The realized sds were 0.2516 and 0.2936 — 35 % and 58 % above it. The band is a pre-registration
projection, so this is a limitation of the projection rather than an error in it; it is nevertheless the
actual reason the realized MDE (0.0512) exceeded the projection, and the documents attribute that to
correlation instead. That attribution is finding **-1**.

### Tests

| Metric | Count |
|---|---|
| Test-statistic-shaped quantities audited | **11** |
| Tail mismatch | **0** |
| Degrees-of-freedom issue | **0** |
| Multiplicity-correction mismatch | **0** |

Nothing in this repository applies a multiplicity correction, and nothing in it needs one. The place a
correction would have been *wrong* is handled correctly: verdict row 1 fires on
`beats_coin AND beats_best_baseline` (`evaluator.py:686-706`), an intersection-union rule, and row 2 on
`beats_coin` alone, so the union {row 1, row 2} fires only if `beats_coin` and the global type-I rate is
bounded by that single test. The report states "No family correction applies" (`evaluation.md:84`) and the
reason was registered in advance at `REGISTRATION.md:188-190`. Applying a Bonferroni or Šidák there would
have been the mismatch.

Two conventions are recorded rather than raised, because each is conservative and each was fixed before
the data existed. (i) `beats_coin` is `model_interval.low > 0.0` — a **one-sided** read of a two-sided
±2·SE interval, α ≈ 0.025 in the registered direction. The hypothesis is directional (the model *beats*
the baseline), so the one-sided read of a two-sided bound is the harder bar, not the easier one.
(ii) `t_critical = 2.0` is a constant, not a t-quantile; at n_eff ≈ 201 the two-sided 95 % t-quantile is
1.972, so 2.0 is marginally wider than a dof-correct value would be. Neither can flatter the result.

One labelling mismatch is recorded: `REGISTRATION.md:186` lists the permutation null under the heading
"Primary contrast", while `evaluator.py:663-668` tests the **model mean daily rank IC** against zero. The
report labels its own statistic correctly (`evaluation.md:109`), the p is descriptive, and no verdict row
reads it, so no conclusion turns on it.

Three of the eleven rows (T8, T9, T10) are predecessor AiTrader statistics carried into the registration
as text — z −0.046 on 274 calls, the pooled confidence Spearman, the 71.7 % `consolidat` cell. They are
UNVERIFIABLE here and belong to the AiTrader audit.

### Provenance

| Status | Count |
|---|---|
| SUPPORTED | **15** |
| NOT_SUPPORTED | **3** |
| PARTIAL | **10** |
| UNVERIFIABLE | **2** |
| **Total provenance rows audited** | **30** (17 registration claims R1…R17, 13 post-data parameter changes C1…C13) |

Registration claims (R1–R17): SUPPORTED 9, NOT_SUPPORTED 3, PARTIAL 3, UNVERIFIABLE 2.
Parameter changes (C1–C13): SUPPORTED 6, PARTIAL 7.

**NOT_SUPPORTED (3):** R12, the "registered tolerance" of 0.02 that appears in no version of
`REGISTRATION.md` (finding **-6**); R13, the closure's "26 superseded attempts" against a ledger holding
74 (finding **-5**); R14, "every attempt" / "every billed call" against the eight strict-schema calls that
have no row in either ledger (finding **-3**).

**PARTIAL (10):** R7 (the B.0b prompt-freeze artifact was overwritten in place 22 minutes after the first
live call — amended, and the change is recorded in Amendment 4); R15 (the sealed store's mtime supports
"unchanged", but no pre-image hash was ever recorded); R16 (a before-hash exists for `universe.py` and not
for `analysis_bars.db`); C3 and C4 (Amendments 3 and 4, findings **-4** and **-3**); C7 (the stale
`CLAUDE.md`, finding **-9**); C8 (the tolerance's word "registered", finding **-6**); and C9, C11, C12 —
three post-data changes with no dated amendment, counted PARTIAL here on provenance grounds although the
provenance pass raised none of them: the h = 1 block length (conservative, above), the Amendment-0 guard
being *strengthened* from "the empty marker is absent" to "a number in [0,1] is present", and the mutation
set growing from five guards to six. All three add or tighten a constraint; none relaxes one.

**UNVERIFIABLE (2):** R6, whether the operator's Section 13 prior was recorded before the sealed store was
read — the fill and every B.2 artifact land in one commit and git cannot order events inside a working
tree; the only in-repo mechanism is `require_amendment_zero()`, which existed before the first call and
refuses to run on the empty marker. R17, whether the GitHub remote the repository was pushed to on
2026-08-29 (four days after the anchor) is public; no network read was attempted.

**The structural fact the provenance pass rests on.** `git diff -U0 64b7d41 2d3d0ae -- REGISTRATION.md`
deletes exactly two things across the whole history: the Section 13 Amendment-0 placeholder and the line
"None yet. Amendment 0 is reserved in Section 13 and is empty." Everything else is an append. `DECISIONS.md`
and `progress.md` have **zero** deleted lines. Sections 0, 1, 5, 6, 8, 9, 10 and 11 are byte-identical from
the pre-call commit `64b7d41` (16:39:00Z) to the anchor. The first billed call is 17:10:48.475Z. No bar,
threshold, horizon, universe, alpha, n target or cost figure was edited after data existed; every parameter
that did change after 17:10:48Z changed in the model-call layer only, and each of those five carries a
dated amendment.

### Merge and de-duplication record

Eleven draft findings entered consolidation: six from the verification pass (DRAFT-V-1…V-6) and five from
the provenance pass (DRAFT-P-1…P-5). Two merges were made and **no draft was dropped** — every one carries
a verbatim quote that was re-located in `SNAP/NPDExperiment/` at the cited line, and at least one figure
with its n or its source object.

- DRAFT-V-4 + DRAFT-P-1 → **-4**. Same quoted passage (`REGISTRATION.md:504-509`, `:538-539`), same ledger
  walk, same conclusion. Merged; class taken as PROVENANCE; both evidence strands kept (the attempt-14 vs
  attempt-16 vs attempt-26 prefix walk, and the non-reproducing 0.0286 USD).
- DRAFT-V-3 + DRAFT-P-4 → **-5**. Same quoted closure sentence (`REGISTRATION.md:779-780`) and the same
  74-vs-26 count. Merged; class taken as INTERNAL_INCONSISTENCY, because the decisive evidence is the
  repository's own B.1 report printing the correct 74 at `reports/stage_b1/collection.md:73`.

Drops for want of a locatable quote or figure: **0**.

---

## Findings

### AUDIT-C-NPDExperiment-1
- **Repository / SHA:** NPDExperiment / `2d3d0aebf977fb2821ec78c25b370c84ec055920`
- **Hypothesis or artifact:** the closure's causal account of why the realized power fell short — the
  "dormant observation" that the model leaned against momentum (`reports/stage_b2/evaluation.md` Appendix;
  ADR-014; the Closure block)
- **Direction:** B (claimed too much — a measured fact is asserted with the wrong sign)
- **Class:** STATISTICAL
- **Severity:** S1
- **Label:** DERIVED
- **Claim challenged (verbatim):** "**The realized 0.36339 sits at 98 percent of that maximum.** The model
  daily rank IC and the momentum daily rank IC are therefore strongly negatively correlated across this
  window, far outside the 0.0 to 0.7 range the registration contemplated." —
  NPDExperiment/reports/stage_b2/evaluation.md:229-233. Restated as the recorded cause of the closure at
  NPDExperiment/REGISTRATION.md:699-702 ("driven by a strong negative correlation between the model and
  momentum daily ICs that fell outside the range the registration contemplated"), as the named observation
  at NPDExperiment/REGISTRATION.md:727-729 ("The model was not producing noise around momentum. It was
  leaning systematically against it."), as ADR-014 at NPDExperiment/DECISIONS.md:272-276, and at
  NPDExperiment/progress.md:41-45, 70-73, 158-161.
- **Evidence:**
  - The Pearson correlation between the 404-day model daily rank IC series and the 404-day `mom_12_1` daily
    rank IC series is **+0.1182418** — weakly *positive*. n = 404. Data:
    `/home/kiros-li/Documents/GitHub/NPDExperiment/var/npd.db` tables `model_ranking` and
    `baseline_ranking`, and `/home/kiros-li/Documents/GitHub/NPDExperiment/var/npd_sealed.db` table
    `forward_return`, read read-only 2026-09-04T23:06Z (untracked, unanchored).
  - The realized per-series daily IC standard deviations are **0.251585** (model) and **0.293645**
    (momentum), n = 404 each — 35 % and 58 % above the null value 0.185695 the power model assumes
    (NPDExperiment/src/npd/power.py:34-42, NPDExperiment/REGISTRATION.md:203-204).
  - √(0.251585² + 0.293645² − 2 · 0.1182418 · 0.251585 · 0.293645) = **0.3633892**, equal to the sd of
    the difference series computed directly (0.3633892) and matching every digit the report prints for
    the daily contrast sd, 0.36339 (NPDExperiment/reports/stage_b2/evaluation.md:82) — **with a positive
    correlation**.
  - At zero correlation and the *realized* per-series sds the contrast sd would be
    √(0.251585² + 0.293645²) = **0.3866812**, which is *larger* than the observed 0.3633892. An observed
    contrast sd below the independent-series value can only arise from a positive correlation. This
    forecloses any negative ρ.
  - The "theoretical maximum of 0.3714" (NPDExperiment/REGISTRATION.md:731-735) is 2 × 0.185695, i.e. a
    maximum **conditional on both series carrying the null sd**. Given the realized sds the maximum is
    0.251585 + 0.293645 = 0.545230, and 0.3633892 is 66.6 % of it, not 98 %.
  - Correlation with the other two baselines is also positive: `logistic` **+0.0642262**, `sign_last`
    **+0.4114189** (n = 404 each). No baseline in this repository is negatively correlated with the model.
  - The claim is hand-written prose, not code output. `src/npd/eval/report.py` ends at the line "model at
    its best." (NPDExperiment/src/npd/eval/report.py:291-294), which is
    `reports/stage_b2/evaluation.md:207`. Everything from line 210 on — the whole appendix containing this
    claim — was written by hand and committed with the machine-generated report in `2c6d683`.
- **Recomputation:** inputs `var/npd.db:model_ranking`, `var/npd.db:baseline_ranking`,
  `var/npd_sealed.db:forward_return` (horizon 5, `ret IS NOT NULL`), joined exactly as
  NPDExperiment/src/npd/eval/evaluator.py:481-497 joins them, and scored with the repository's own
  `daily_ic` / `spearman` convention (NPDExperiment/src/npd/eval/evaluator.py:96-133). This reproduces the
  same 404 evaluable days, model mean IC **+0.0060772** against the printed +0.0061, `mom_12_1` mean IC
  **+0.0221820** against the printed +0.0222, and primary contrast **−0.0161048** against the printed
  −0.0161. Method: Pearson correlation on the two 404-length series; sample sd with ddof = 1; the variance
  identity above. Result ρ = **+0.1182418**, σ_diff = **0.3633892**, equal to the sd of the difference
  series computed directly (0.3633892) and matching every digit the report prints at
  NPDExperiment/reports/stage_b2/evaluation.md:82 (0.36339). Nothing in the repository prints the figure
  to seven places.
  Inverting the registration's own formula σ_diff = √(2(1 − ρ)) · 0.185695
  (NPDExperiment/src/npd/power.py:116) at σ_diff = 0.36339 returns ρ = **−0.914757** — that is the number
  the documents are describing, and it is an artefact of holding both series at the null sd rather than at
  their realized sds. Run twice independently: once in the verification pass
  (`work/agentC/npd_verify/verify.py`) and once in this consolidation
  (`work/agentC/npd_consol/spot_corr.py`), agreeing to every printed digit.
- **What would resolve it:** compute `corr(model daily IC, mom_12_1 daily IC)` on the 404 evaluable days
  from the same two stores the evaluator reads, and replace the causal sentence. The correct diagnosis is
  available from the same data and is arguably more interesting: the registered power model assumed each
  daily IC carried the null sd 0.185695; the realized sds were 0.2516 and 0.2936, and that alone raises the
  contrast sd from the 0.2466 the registered formula gives at ρ = +0.1182 to the observed 0.36339. If
  ADR-014 is to survive as a dormant observation it has to be restated with its sign reversed, or withdrawn.
- **Confidence:** HIGH — the identity σ_diff² = σm² + σb² − 2ρσmσb reproduces the repository's own printed
  0.36339 only at ρ = +0.1182, and the observed sd lies below the zero-correlation value,
  which forecloses a negative ρ independently of any tie or ranking convention.
- **Invalidated by later commits?:** no — HEAD equals the anchored SHA, there is no commit after it, the
  repository carries a `_CLOSED_DO_NOT_RUN_HERE` marker dated 2026-09-02, and the claim is present verbatim
  in four tracked documents at the anchor. The one exposure is the untracked data: if `var/npd.db` or
  `var/npd_sealed.db` changed after 2026-08-25 the recomputation would describe a different sample — but
  the same stores reproduce every printed B.2 figure exactly, which makes that implausible.
- **Disclosed by the authors?:** no. The authors disclose that the observation "is not a finding" and may
  only be promoted by a future pre-registered test (NPDExperiment/REGISTRATION.md:737-742,
  NPDExperiment/DECISIONS.md:278-289). That disclosure is about the observation's evidential *status*, not
  its sign. The documents state the correlation as measured fact — "**The measured basis.**"
  (NPDExperiment/REGISTRATION.md:731) — and use it as the recorded cause of the power shortfall in the
  Closure block.
- **Citation check:** corrected — a wording repair in the evidence, recomputation and confidence blocks, no change of substance. The first two read "σ_diff from the identity = 0.3633892 against the printed 0.3633892" and the third claimed agreement "to seven digits"; nothing in the repository prints 0.3633892. `reports/stage_b2/evaluation.md:82` prints `| daily contrast sd | 0.36339 |`, and a repo-wide grep for `0.3633` over `SNAP/NPDExperiment` returns only the five-decimal 0.36339 (`evaluation.md:82`, `:224`, `:229`; `REGISTRATION.md:700`, `:716`, `:732`; `progress.md:42`, `:51`, `:159`; `DECISIONS.md:272`). The text now says that 0.3633892 equals the sd of the difference series computed directly and matches every digit the report prints. Everything else re-verified independently in the citation-check pass, which re-implemented the evaluator join and the `daily_ic`/`spearman` convention from scratch: quote EXACT at `reports/stage_b2/evaluation.md:229-232` (cited 229-233; line 233 completes the paragraph); ρ(model, `mom_12_1`) = **+0.1182418**; sd 0.251585 and 0.293645; n = 404; σ_diff 0.3633892 both from the identity and from the difference series, identically; σ_diff at ρ = 0 equal to 0.3866812, above the observed, which forecloses a negative ρ; maximum at the realized sds 0.545230 with 0.36339 at 66.65 % of it; ρ(`logistic`) = +0.0642262 and ρ(`sign_last`) = +0.4114189; and the control means +0.0060772 / +0.0221820 / −0.0161048 against the printed +0.0061 (`evaluation.md:59`), +0.0222 (`:60`) and −0.0161 (`:78`), with 404 evaluable and 6 dropped (`:51-53`). The registered formula at ρ = +0.1182 gives 0.246599 (the finding's 0.2466); inverting it at 0.36339 gives −0.914758 against the finding's −0.914757, display rounding only; and 0.36339 / 0.371391 = 97.85 %, so the report's own "98 percent" arithmetic is right and only its causal reading is wrong. Provenance re-verified against the live object store: `src/npd/eval/report.py:294` ends the generated report at `evaluation.md:207`, the appendix from `:210` on is hand-written, and `git diff 2c6d683 HEAD -- reports/stage_b2/evaluation.md` is empty. Class STATISTICAL, severity S1, label DERIVED and the non-disclosure answer all confirmed and unchanged.

### AUDIT-C-NPDExperiment-2
- **Repository / SHA:** NPDExperiment / `2d3d0aebf977fb2821ec78c25b370c84ec055920`
- **Hypothesis or artifact:** the registered B.2 deliverable that was to address the Amendment 3 /
  Amendment 4 effort confound
- **Direction:** A (a registered analysis was not run before the project closed)
- **Class:** PROCESS
- **Severity:** S3
- **Label:** DERIVED
- **Claim challenged (verbatim):** "The realized effort is stored per day for exactly this reason, and B.2
  reports the outcome split by realized effort alongside the primary contrast. The split is descriptive. It
  does not become a verdict, under Clause 1." — NPDExperiment/REGISTRATION.md:534-536. Repeated at
  NPDExperiment/reports/session_a1_b1.md:269-270 ("B.2 reports the outcome split by realized effort beside
  the primary contrast, as a descriptive split that never becomes a verdict, under Clause 1.").
- **Evidence:**
  - `reports/stage_b2/evaluation.md` is 260 lines and contains no split by realized reasoning effort. The
    only effort text in it is the Amendment 2 limitation prose at
    NPDExperiment/reports/stage_b2/evaluation.md:204-207.
  - The renderer contains no effort term: the only match for "effort" in
    NPDExperiment/src/npd/eval/report.py is that same limitation prose at lines 292-293. There is no match
    at all in NPDExperiment/src/npd/eval/evaluator.py.
  - The inputs exist and were stored for this purpose. 53 days' stored answers came from `low` after an
    escalation (NPDExperiment/reports/stage_b1/collection.md:75, reproduced from `ledgers/evidence.jsonl`),
    of which 51 fall inside the 404 evaluable days.
  - The commitment was live going into B.2. The promise at
    NPDExperiment/reports/session_a1_b1.md:269-270 first enters git at `02b8560`
    (2026-08-25T12:48:04 −0700), *after* Amendment 4 superseded Amendment 3's ladder. (The file itself
    was created earlier, at `3164c88`, 10:42:05 −0700; `02b8560` extended it, and
    `git log -S 'B.2 reports the outcome split by realized effort beside'` returns `02b8560` alone.)
    Amendment 4 (NPDExperiment/REGISTRATION.md:550-603) re-tunes the ladder but never withdraws the
    reporting commitment, and the closure does not list it as outstanding.
- **Recomputation:** inputs `ledgers/evidence.jsonl` (the stored-state row per day carries
  `reasoning_effort`), `var/npd.db:model_ranking`, `var/npd.db:baseline_ranking`,
  `var/npd_sealed.db:forward_return`; read 2026-09-04T18:26Z. Method: partition the 404 evaluable days by
  the effort of the attempt that produced the stored ranking, then take the mean daily rank IC and the mean
  contrast against `mom_12_1` in each cell. Result: `minimal` n = 353, model mean IC **−0.00040**, contrast
  **−0.02580**; `low` n = 51, model mean IC **+0.05092**, contrast **+0.05098**. The i.i.d. standard error
  on the `low` contrast is 0.0465; inflated by the registered VIF 3.4 it is 0.086, so +0.0510 is about
  0.6 SE — a large descriptive gap that is **not** significant, and a post-hoc subgroup besides. Tolerance:
  means to 1e-5.
- **What would resolve it:** produce the registered split as a descriptive table in the B.2 report, or
  record an amendment stating that the deliverable was dropped and why. Either resolves it; neither exists
  at the anchor. Note that the split, had it been produced, would not have changed the verdict — it is
  barred from doing so by the same sentence that registers it — so this is a process finding, not a
  suppressed result.
- **Confidence:** HIGH — the deliverable is registered in one sentence, the artifact is 260 lines and does
  not contain it, and neither module that could have produced it references effort.
- **Invalidated by later commits?:** no — HEAD equals the anchored SHA and the project is closed.
- **Disclosed by the authors?:** partly. The B.2 report carries the Amendment 2 limitation that "the gate
  ran at `minimal` reasoning effort on the large majority of attempts"
  (NPDExperiment/reports/stage_b2/evaluation.md:204-207), which is the honest general caveat and is why this
  is S3 rather than higher. It does not disclose that the specific registered split was not produced, and
  the closure does not list it as an outstanding item.
- **Citation check:** corrected — two provenance repairs, neither touching the conclusion. (a) The evidence read that `reports/session_a1_b1.md` "was committed at `02b8560`"; the file was **first** committed at `3164c88` (2026-08-25T10:42:05 −0700) and `02b8560` (12:48:04 −0700) extended it. The load-bearing half survives exactly: `git log -S 'B.2 reports the outcome split by realized effort beside' -- reports/session_a1_b1.md` returns `02b8560` alone, so the promise itself does first enter git after Amendment 4 (`250bc8f`, 10:35:37 −0700). (b) The promise sentence is at `reports/session_a1_b1.md:269-270`, not 268 — line 268 carries only its lead-in, "The realized effort is stored per day for exactly" — so both the quote citation and the in-text pin move to 269-270. Everything else re-verified: the registered quote EXACT at `REGISTRATION.md:534-536`; the absence confirmed mechanically (`evaluation.md` is 260 lines and `grep -i effort` returns only :205-206; `grep -i effort src/npd/eval/evaluator.py` returns nothing at all; the only match in `src/npd/eval/report.py` is that same prose at :292-293); Amendment 4 (`REGISTRATION.md:550-603`) read in full and it never withdraws the reporting commitment; and the split reproduced independently — 415 stored days mapped to the `reasoning_effort` of their stored attempt give 362 `minimal` / 53 `low`, matching `reports/stage_b1/collection.md:75` (EXACT), and inside the 404 evaluable days `minimal` n = 353 mean IC −0.00040 contrast −0.02580, `low` n = 51 mean IC +0.05092 contrast +0.05098, i.i.d. SE 0.04653, VIF-3.4-inflated 0.08579, so +0.0510 is 0.594 SE. Class PROCESS, label DERIVED and the S3 cap (set by the disclosed Amendment 2 caveat) unchanged; the taxonomy fit is loose, since an unproduced registered deliverable is not literally "a blocker or external figure is stale", but S1 is barred by the same registered sentence that forbids the split becoming a verdict.

### AUDIT-C-NPDExperiment-3
- **Repository / SHA:** NPDExperiment / `2d3d0aebf977fb2821ec78c25b370c84ec055920`
- **Hypothesis or artifact:** Amendment 4's justifying measurement, and the closure's artifact table
  asserting the completeness of the two ledgers
- **Direction:** B (the audit trail is claimed complete and is not)
- **Class:** PROVENANCE
- **Severity:** S3
- **Label:** DERIVED
- **Claim challenged (verbatim):** "| evidence ledger | every attempt, with the raw response verbatim |" and
  "| spend ledger | every billed call |" — NPDExperiment/REGISTRATION.md:772-773, read against
  "**Measured on 8 held-out window days at `minimal`:**" and the table it heads — "| first-attempt
  compliance | 17 of 29, 59 percent | 7 of 8, 88 percent |", "| mean latency | 16.3 s per attempt | 2.3 s |",
  "| projected total over 432 days | 9.12 USD | **2.86 USD** |" — NPDExperiment/REGISTRATION.md:573-579.
- **Evidence:**
  - The strict JSON schema and the digest `7e6f3d68…` first exist in git at `250bc8f`, author date
    2026-08-25T17:35:37Z (`git show 250bc8f -- src/npd/collect/prompt.py reports/stage_b0b/mock_run.md`).
    The eight strict-schema calls behind the "7 of 8", "2.3 s" and "2.86 USD" column must therefore predate
    17:35:37Z.
  - In `ledgers/evidence.jsonl` the last row before that commit is **17:30:37.688731Z** and the next row is
    **17:35:44.085369Z** — a **306.4-second gap containing no evidence row**. The spend ledger has the same
    hole: its last pre-commit gate row is 17:30:35.843538Z and its next is 17:35:44.075258Z. Read read-only
    2026-09-04T23:06Z (untracked, unanchored).
  - There is no room for the eight calls anywhere else either. The 74 pre-Amendment-4 evidence rows carry
    Σ`cost_usd` = **0.318852 USD** and the 37 gate rows in the spend ledger before 17:35:37Z sum to exactly
    **0.318852 USD**, so every billed row in that window is accounted for by a recorded attempt.
  - At the observed strict-schema first-attempt price (0.006586–0.006684 USD per call, `ledgers/spend.jsonl`
    rows at 17:35:44–17:35:47) the unrecorded spend is roughly **0.05–0.06 USD** against a ledger-enforced
    10.00 USD cap (NPDExperiment/REGISTRATION.md:290). The cap is not threatened; the completeness claim is.
  - Nothing outside the amendment text and its own commit message records the measurement: no ledger row,
    no data file, and no artifact among the **ten** files changed at `250bc8f` — `REGISTRATION.md` (the
    amendment itself, +74 lines), `reports/stage_b0b/mock_run.md`, the adapter, the collector, the mock,
    the prompt, the config, the evidence ledger and two test files — carries the eight calls or names the
    eight days. The commit message of `250bc8f` restates the same three figures ("lifts first-attempt
    compliance from 59 to 88 percent, cuts latency from 16.3s to 2.3s, and drops the projection from 9.12
    to 2.86 USD"), but that is the amendment's own assertion travelling with it, not an independent
    record of the measurement.
  - "Held-out" itself has no support in any record: no artifact names the eight days, and every window day
    was subsequently recollected into the final 415.
- **Recomputation:** inputs `ledgers/evidence.jsonl` (959 rows) and `ledgers/spend.jsonl` (922 rows), both
  read-only line parses; `git log`/`git show` for the commit dates. Method: window scan on `ts` between
  17:28:00Z and 17:37:00Z; Σ`cost_usd` over the 74 evidence rows lacking `prompt_digest` versus Σ over
  spend gate rows with `ts < 17:35:37Z`. Result: 0.318852 = 0.318852, exact to 1e-6; gap 306.396638 s;
  23 spend rows in the surrounding nine minutes, none inside the gap. Re-run in this consolidation
  (`work/agentC/npd_consol/spot_ledger.py`) and agreeing with the provenance pass exactly.
- **What would resolve it:** the eight held-out calls' ledger rows, or a note in Amendment 4 stating that
  the schema was measured with a harness outside the ledgers, naming the eight dates and their cost. Absent
  that, the measurement that re-froze the prompt and re-tuned the ladder mid-run cannot be checked, and the
  reported 6.9378 USD total understates true spend by those calls. This is also why claims C27 and C28
  (the 16.3 s / 2.3 s latencies and the 9.12 / 2.86 USD projections) are UNVERIFIABLE.
- **Confidence:** HIGH for the absence of the rows and for the timing (git object dates plus append-only
  ledgers whose sums close exactly); MEDIUM for the imputed 0.05–0.06 USD, which is an estimate from
  observed per-call prices rather than a recorded figure.
- **Invalidated by later commits?:** no — `250bc8f` is an ancestor of the anchor and the artifact table is
  at HEAD.
- **Disclosed by the authors?:** partly. Amendment 5 discloses an unrecoverable undercount of 0.2936 USD
  but attributes it to "the superseded attempts" whose usage was discarded
  (NPDExperiment/REGISTRATION.md:617-622); it does not mention the held-out strict-schema calls, which are a
  separate set made after that undercount was measured. The partial disclosure is why this is S3.
- **Citation check:** corrected — one over-broad sentence narrowed in two places, neither touching the conclusion. (a) The evidence listed eight files changed at `250bc8f`; `git show --stat 250bc8f` lists **ten**, also `REGISTRATION.md` (the amendment itself, +74 lines) and `reports/stage_b0b/mock_run.md` (regenerated: its timestamp and digest lines). (b) "No script, report or artifact in any commit records the measurement" overlooked the commit message of `250bc8f`, which restates the same three figures ("lifts first-attempt compliance from 59 to 88 percent, cuts latency from 16.3s to 2.3s, and drops the projection from 9.12 to 2.86 USD") — the amendment's own assertion travelling with it, not an independent record. The bullet now reads that nothing outside the amendment text and its own commit message records it. Everything else re-verified, most of it first-hand at apply: quote EXACT at `REGISTRATION.md:772-773`, and Amendment 4's "**Measured on 8 held-out window days at `minimal`:**" EXACT at `:573` with its table at `:575-579`; 959 evidence rows and 922 spend rows re-parsed; digest `7e6f3d68` first entering git at `250bc8f` (author date 2026-08-25T10:35:37 −0700 = 17:35:37Z); the evidence gap 17:30:37.688731Z → 17:35:44.085369Z = **306.396638 s** containing no row, with the same hole in the spend ledger (17:30:35.843538Z → 17:35:44.075258Z); 23 spend rows in the surrounding nine minutes, none inside the gap; 37 gate spend rows before 17:35:37Z summing to **0.318852 USD**, exactly the 74 no-digest evidence rows' 0.318852 USD, so every billed row in the window is accounted for by a recorded attempt; observed strict-schema first-attempt prices 0.006635, 0.00658625 and 0.00668375, bracketing the stated 0.006586–0.006684 range; and the 10.00 USD cap at `REGISTRATION.md:290`. One corroboration the finding does not use, which sharpens rather than weakens it: Amendment 4's free-form column **is** reconstructible from the ledger — the 48 Amendment-3-era rows split 29 `minimal` / 19 `low`, exactly the table at `REGISTRATION.md:557-560`, reproduced first-hand at apply — while the strict column (7 of 8, 2.3 s, 2.86 USD) is not. Class PROVENANCE, severity S3 and the partial-disclosure answer unchanged.

### AUDIT-C-NPDExperiment-4
- **Repository / SHA:** NPDExperiment / `2d3d0aebf977fb2821ec78c25b370c84ec055920`
- **Hypothesis or artifact:** Amendment 3's record of the live failure that triggered it, and the
  stop-and-amend discipline it asserts
- **Direction:** B (more mid-run discipline is claimed than the ledger records)
- **Class:** PROVENANCE
- **Severity:** S3
- **Label:** DERIVED
- **Claim challenged (verbatim):** "**Raised 2026-08-25, 14 gate calls into B.1. The run was stopped to
  record this before it went further.**" and "Across the first 14 live attempts the model failed to return a
  usable permutation of the 30 labels on 9 of them" — NPDExperiment/REGISTRATION.md:504-509; and
  "**Days already collected are recollected.** The 7 days stored before this amendment followed the
  superseded procedure." — NPDExperiment/REGISTRATION.md:538-539; and "The 9 superseded attempts cost
  0.0286 USD and that spend still counts against the cap." — NPDExperiment/REGISTRATION.md:543-544.
- **Evidence:**
  - `git log` gives `c4da18c` (Amendment 3) author date **2026-08-25T17:17:32Z**. The pre-Amendment-3 slice
    of `ledgers/evidence.jsonl` — rows with no `prompt_digest` and no `reasoning_effort` — is **26 attempts
    across 13 dates**, timestamped 17:12:52.134001Z through 17:14:59.939605Z, with **10 days stored** and
    **16 model_failed**. The Amendment-3-era rows (which carry `reasoning_effort`) begin at 17:17:38.640202Z.
    Read read-only 2026-09-04T23:06Z (untracked, unanchored).
  - Walking that slice in timestamp order: at attempt 14 the cumulative failure count is **7**, not 9. The
    amendment's own failure table — "| ranking omitted or duplicated a label | 5 |" and "| ranking had 31,
    32, 35, or 37 entries instead of 30 | 4 |" (NPDExperiment/REGISTRATION.md:516-517) — is the cumulative
    state at attempt **16** (17:13:59.708055Z), where the counts are exactly 5 and 4 and 9 in total.
  - "7 days stored" is the state at attempts 14 through 18. By the end of the superseded slice **10** days
    were stored (2024-10-31, 11-01, 11-04, 11-05, 11-06, 11-07, 11-08, 11-13, 11-14, 11-15).
  - The 2.5-minute gap between 17:14:59.939605Z (last superseded attempt) and 17:17:38.640202Z (first
    Amendment-3-era attempt) is the actual stop. It sits after attempt **26**, not after attempt 14 or 16 —
    so collection continued for ten more attempts and three more stored days after the snapshot the
    amendment describes, which is what "the run was stopped … before it went further" denies.
  - The companion cost sentence does not reproduce either. Every one of the 16 pre-Amendment-3 failures
    carries `cost_usd = 0.0` — precisely the defect Amendment 5 documents two amendments later — so the
    9 attempts the sentence names have **zero** recorded cost, and the full 26-attempt slice costs
    **0.026807 USD**. No prefix of the slice sums to 0.0286: attempt 26 reaches 0.026807 and the next gate
    row (17:17:38Z) is already past the commit. "0.0286" against a ledger reading 0.0268 is consistent with
    a digit transposition.
- **Recomputation:** inputs `/home/kiros-li/Documents/GitHub/NPDExperiment/ledgers/evidence.jsonl` (959
  rows) and `ledgers/spend.jsonl` (922 rows). Method: filter to gate rows (`date != "calibration"`) with no
  `prompt_digest`, split on presence of `reasoning_effort`, sort by `ts`, and walk the prefix accumulating
  state, failure count and cost; cut both ledgers at the commit author date. Result: the cumulative
  (fails, stored-days, cost) vector reaches (7, 7, 0.018936) at attempt 14, (9, 7, 0.018936) at attempt 16,
  and (16, 10, 0.026807) at attempt 26. Tolerance: exact on counts, 1e-6 on cost. Run independently in the
  verification pass, the provenance pass and this consolidation, with identical results.
- **What would resolve it:** restate the amendment against the ledger — 26 attempts across 13 dates, 16
  failures, 10 days recollected, 0.0268 USD — or state that the counts are a snapshot taken at attempt 16
  while collection continued to attempt 26, which is the honest reading but contradicts "the run was
  stopped … before it went further". The mechanism the amendment relies on is independently **VERIFIED**:
  rows with no `reasoning_effort` are treated as not-yet-collected and recollected, and all 415 stored days
  come from the 883 rows carrying the re-frozen digest, so no superseded day contaminates the sample.
- **Confidence:** MEDIUM on intent — the "9 failures / 5 + 4 / 7 stored" figures match a real prefix of the
  ledger exactly at attempt 16, so the amendment describes a genuine mid-run snapshot rather than inventing
  numbers. HIGH on the counts themselves, which are a direct walk of an append-only ledger timestamped to
  the microsecond against a git author date.
- **Invalidated by later commits?:** no — `c4da18c` is an ancestor of the anchor and Amendment 3's text is
  unchanged at HEAD; Amendment 4 supersedes the *ladder* but not this account of the data.
- **Disclosed by the authors?:** no. Amendment 4 states that Amendment 3 was "the wrong diagnosis, correctly
  recorded" (NPDExperiment/REGISTRATION.md:563-564), which concedes the diagnosis but not the counts.
  Amendment 5 discloses that rejected attempts were unbilled (NPDExperiment/REGISTRATION.md:609-615), which
  explains the zero costs, but nothing discloses that the superseded procedure ran to 26 attempts and 10
  stored days rather than 14 and 7.
- **Citation check:** corrected — one citation line. Amendment 4's concession "Amendment 3 was the wrong diagnosis, correctly recorded" is at `REGISTRATION.md:563-564`, not the `:565-567` the finding cited (line 565 is blank and 566 opens "**The fix.**"); `grep -n 'wrong diagnosis' REGISTRATION.md` returns 563 alone. Fixed here and in the JSON's disclosure reference and evidence list. Everything else re-verified: all three quotes EXACT at `REGISTRATION.md:504-505` + `:508-509`, `:538-539` and `:543-544`; `c4da18c` author date 2026-08-25T10:17:32 −0700 = 17:17:32Z; the pre-Amendment-3 slice re-walked from the ledger — 26 attempts across 13 dates, 17:12:52.134001Z to 17:14:59.939605Z, 10 stored / 16 `model_failed`, 0.026807 USD (re-derived first-hand at apply), with the Amendment-3-era rows beginning 17:17:38.640202Z — and the cumulative vector reproducing to the digit: (7, 7, 0.018936) at attempt 14, (9, 7, 0.018936) at attempt 16, (16, 10, 0.026807) at attempt 26, with all 16 pre-Amendment-3 failures carrying `cost_usd = 0.0` and the stored dates matching the finding's list of ten exactly. **Stronger than the finding claims:** the nine failures at attempt 16 split 5 label-mismatch and 4 wrong-length (31, 37, 35, 32 entries), matching `REGISTRATION.md:516-517` cell for cell, so the amendment's table is provably an attempt-16 snapshot. Two corroborations not previously used: at the moment of the Amendment 3 commit the spend ledger held exactly 10 gate rows summing to 0.026807 USD (plus two calibration rows, 0.030522), so 0.0286 had no source in the ledger the author was reading; and the unit-ambiguity defence fails too, since reading "14 gate calls" as days does not rescue the sentence when the slice spans only 13 distinct dates. Confidence MEDIUM on intent / HIGH on counts, class PROVENANCE, severity S3 and label DERIVED unchanged.

### AUDIT-C-NPDExperiment-5
- **Repository / SHA:** NPDExperiment / `2d3d0aebf977fb2821ec78c25b370c84ec055920`
- **Hypothesis or artifact:** the closure's correction to the closing instruction, and the B.1 session
  narrative — the accounting of what the superseded prompt template produced
- **Direction:** neutral (it understates discarded work; no verdict figure moves)
- **Class:** INTERNAL_INCONSISTENCY
- **Severity:** S3
- **Label:** DERIVED
- **Claim challenged (verbatim):** "It produced the two calibration calls and the 26 superseded attempts,
  and **zero** of the 415 stored rankings." — NPDExperiment/REGISTRATION.md:779-780. And: "The 26 superseded
  attempts stay in the ledger and their 0.0286 USD still counts against the cap." —
  NPDExperiment/reports/session_a1_b1.md:254-255.
- **Evidence:**
  - `ledgers/evidence.jsonl` holds 959 rows: 883 carrying `prompt_digest = 7e6f3d68…`, 2 calibration rows,
    and **74** gate attempts carrying no digest. Read read-only 2026-09-04T23:06Z (untracked, unanchored).
  - Those 74 rows cost **0.318852 USD**, of which 37 carry `cost_usd = 0` because their usage was discarded
    (the Amendment 5 defect). The 26 pre-Amendment-3 rows alone cost **0.026807 USD**; the 48
    Amendment-3-era rows cost 0.292045 USD.
  - The repository's own B.1 report gets it right: "superseded attempts, kept in the ledger and excluded
    from these counts: **74**" — NPDExperiment/reports/stage_b1/collection.md:73.
  - The same registration reasons over 74 in one amendment and calls them 26 in the closure. Amendment 5's
    "recorded 0.3494 USD" (NPDExperiment/REGISTRATION.md:612) is exactly 0.318852 (74 superseded rows) +
    0.030522 (2 calibration rows) = **0.349374**.
  - The 26/74 split is the pre- versus post-Amendment-3 boundary: 26 rows carry no `reasoning_effort` field,
    48 do. Amendment 4 re-froze the template *after* both groups, and `src/npd/collect/prompt.py` is
    untouched between `943ba05` and `250bc8f`, so all 74 came from the one superseded template.
  - Neither figure reproduces: no prefix of the superseded slice sums to 0.0286 (attempt 26 reaches
    0.026807 and attempt 27 is already past the Amendment 3 commit).
  - Three different counts for "superseded attempts" appear in the tracked documents: 9
    (`REGISTRATION.md:543`), 26 (`REGISTRATION.md:779`, `reports/session_a1_b1.md:254`) and 74
    (`reports/stage_b1/collection.md:73`). The last is the correct one.
  - `reports/session_a1_b1.md:254` first enters git at `02b8560` (2026-08-25T12:48 −0700), the same commit
    as `collection.md` with its 74, so the two were written together.
- **Recomputation:** inputs `/home/kiros-li/Documents/GitHub/NPDExperiment/ledgers/evidence.jsonl` (959
  lines) and `ledgers/spend.jsonl` (922 lines). Method: partition evidence rows on presence of
  `prompt_digest` and of `reasoning_effort`, sum `cost_usd` per partition, and cross-check the gate rows in
  the spend ledger (920 = 883 current + 37 superseded that were billed). Result: superseded 74 rows /
  0.318852 USD; pre-Amendment-3 26 rows across 13 dates / 0.026807 USD. Tolerance 1e-6 USD. Re-run in this
  consolidation with identical results.
- **What would resolve it:** correct the closure sentence to "the 74 superseded attempts" and 0.3189 USD —
  or to "the 26 attempts made before Amendment 3 and the 48 made under it" — and fix 0.0286 to 0.0268. The
  substantive half of the claim, that **zero** of the 415 stored rankings came from the superseded digest,
  is independently **VERIFIED** and is unaffected.
- **Confidence:** HIGH — a direct count of two append-only ledgers, cross-checked against the repository's
  own B.1 report, which states 74.
- **Invalidated by later commits?:** no — HEAD equals the anchored SHA and the closure commit *is* the
  anchor. The ledgers are untracked and could in principle have changed after the anchor; their mtime is
  2026-08-25 12:46 and every row count derived from them matches a tracked B.1 figure exactly, which makes
  post-anchor mutation implausible.
- **Disclosed by the authors?:** partly, and that is why the severity is S3. The correct number is printed
  elsewhere in the repository (`reports/stage_b1/collection.md:73`), and the authors disclose the
  *unrecoverable* portion of the superseded spend (NPDExperiment/REGISTRATION.md:617-622). Neither
  disclosure says that the closure's attempt count is a third of what the ledger holds, and the closure
  paragraph is what a future replicator reads.
- **Citation check:** verified (quote EXACT at `REGISTRATION.md:779-780`; figures exact; recomputation reproduced). Re-run first-hand at apply against the live untracked ledgers and stores, read-only: 959 evidence rows = 883 carrying `prompt_digest 7e6f3d68` (exactly **one** distinct digest among them) + 2 calibration + **74** no-digest gate attempts; superseded cost **0.318852 USD** with 37 of those rows at `cost_usd = 0`; pre-Amendment-3 26 rows / 13 dates / 0.026807 USD; Amendment-3-era 48 rows / 29 dates / 0.292045 USD; calibration 0.030522 USD; 0.318852 + 0.030522 = **0.349374**, matching Amendment 5's "recorded 0.3494 USD" (`REGISTRATION.md:612`, EXACT) to 1e-6; spend ledger 920 gate rows + 2 calibration = 883 current + 37 billed superseded + 2; whole-ledger total **6.937784 USD** against the reported 6.9378 (`reports/stage_b1/collection.md:49`, EXACT); and no prefix of the superseded slice sums to 0.0286. All three competing counts located EXACT — 9 at `REGISTRATION.md:543`, 26 at `REGISTRATION.md:779` and `reports/session_a1_b1.md:254`, 74 at `reports/stage_b1/collection.md:73`. The provenance claim verifies precisely: `git log -S 'The 26 superseded attempts stay in the ledger'` returns `02b8560` as the earliest introduction, the same commit that created `collection.md` with its 74, so "written together" is exact; and `src/npd/collect/prompt.py` has exactly two commits (`943ba05`, `250bc8f`), so it is untouched between them and all 74 came from the one superseded template. The finding's separation of the verified half (zero of the 415 stored rankings came from the superseded digest) from the contradicted count is confirmed. Kept unchanged.

### AUDIT-C-NPDExperiment-6
- **Repository / SHA:** NPDExperiment / `2d3d0aebf977fb2821ec78c25b370c84ec055920`
- **Hypothesis or artifact:** the B.2 pipeline validity gate, Task 2 of `reports/stage_b2/evaluation.md`
- **Direction:** B (a provenance overclaim; the gate itself passes by three orders of magnitude either way)
- **Class:** PROVENANCE
- **Severity:** S3
- **Label:** DERIVED
- **Claim challenged (verbatim):** "| registered tolerance | 0.02 |" —
  NPDExperiment/reports/stage_b2/evaluation.md:40; and "**Gate verdict: PASS.** The shuffled mean sits
  inside the registered tolerance of zero." — NPDExperiment/reports/stage_b2/evaluation.md:42-43; and the
  source comment "# The registered tolerance for the pipeline validity gate." —
  NPDExperiment/src/npd/eval/evaluator.py:551.
- **Evidence:**
  - `REGISTRATION.md` contains no occurrence of "toleran" and no bare `0.02` at any commit. `grep -n -iE
    'toleran' REGISTRATION.md` is empty at `64b7d41` and at HEAD; `grep -n '0\.02' REGISTRATION.md` returns
    only 0.025 (the B.3 replay floor), the power-grid cells, 0.027271/0.0222 and the 0.0286 of finding
    **-4** — no 0.02.
  - What Section 7 registers is qualitative: "**Negative-control leakage audit at B.2.** Shuffle stored
    rankings within day. The rank IC must collapse toward zero. A non-zero result stops everything." —
    NPDExperiment/REGISTRATION.md:173-175, unchanged from `64b7d41`.
  - The figure 0.02 first enters git at `943ba05` (2026-08-25T17:06:55Z) as the default argument of
    `assert_control_collapsed(verdict, tolerance: float = 0.02)`. `git log -S 'tolerance: float = 0.02' --
    src/npd/eval/evaluator.py` returns that commit only. The module constant `CONTROL_TOLERANCE = 0.02`
    used by `run_b2` (NPDExperiment/src/npd/eval/evaluator.py:553) was added at `2c6d683` (20:13:28Z), the
    evaluation commit, carrying the "registered" comment.
  - The threshold genuinely predates every call it gates (17:06:55Z against a first billed call at
    17:10:48Z), and its value never changed. Only the word "registered" is unsupported.
- **Recomputation:** none required — this is a grep over every committed version of the registration plus
  two `git log -S` queries. For scale: the realized gate mean is +0.00011025 against a null sd of
  0.0092549, so any tolerance above roughly 0.001 passes. The gate's substance is not in question.
- **What would resolve it:** call it the *code-fixed* tolerance, adopted at `943ba05` before the first call;
  or add an amendment recording that 0.02 was adopted then and why. Either removes the overclaim without
  touching the gate.
- **Confidence:** HIGH — a grep over every committed version of `REGISTRATION.md`, and the two commits that
  introduce the value are identified by `git log -S`.
- **Invalidated by later commits?:** no — the anchor is the last commit.
- **Disclosed by the authors?:** no. `progress.md:142` says "inside the 0.02 tolerance" without claiming
  registration; only `evaluation.md` and the source comment call it registered.
- **Citation check:** verified (quote EXACT at `reports/stage_b2/evaluation.md:40`, prose repeat EXACT at `:42-43`; figures exact; no recomputation required, as the finding states). Verified more broadly than the finding claims: `toleran` was grepped at **every one of the eleven commits in the repository** — `64b7d41`, `943ba05`, `3c2a152`, `c4da18c`, `f8304d9`, `250bc8f`, `3164c88`, `02b8560`, `433dabe`, `2c6d683`, `2d3d0ae`, spanning six distinct blobs of `REGISTRATION.md` — with **zero hits in each**, so the claim holds at every point in the repository's history and not only at `64b7d41` and HEAD. `grep -n '0\.02' REGISTRATION.md` at the anchor returns exactly what the finding says (0.025 at :208, :214, :378, :490; the power-grid cells at :236 and :242-244; 0.027271 at :473; 0.0286 at :543; 0.0222 / 0.0161 at :691) and no bare 0.02. Section 7's qualitative registration is EXACT at `REGISTRATION.md:173-175`. `git log -S 'tolerance: float = 0.02' -- src/npd/eval/evaluator.py` returns `943ba05` alone and `git log -S CONTROL_TOLERANCE` returns `2c6d683` alone; the ordering holds to the microsecond, `943ba05` at 2026-08-25T10:06:55 −0700 = 17:06:55Z against the first billed call at 17:10:48.475880Z. The "for scale" figure checks without rerunning the Monte Carlo: the analytic null sd of a mean of 404 daily ICs at panel 30 is 0.185695/√404 = 0.0092387, agreeing with the report's printed 0.00925 (`evaluation.md:38`) and with the finding's 0.0092549, so any tolerance above roughly 0.001 passes and the gate's substance is genuinely not in question. One strengthening worth recording, not an error: the table cell and the prose are **both** emitted by code, at `src/npd/eval/report.py:82` and `:85-86` from `CONTROL_TOLERANCE_TEXT = "0.02"` (`report.py:301`), so the overclaim traces to the generator rather than to a stray hand-written line. Kept unchanged.

### AUDIT-C-NPDExperiment-7
- **Repository / SHA:** NPDExperiment / `2d3d0aebf977fb2821ec78c25b370c84ec055920`
- **Hypothesis or artifact:** the B.2 report's accounting of how 415 collected days became 404 evaluated days
- **Direction:** neutral (an incomplete reconciliation; no figure moves)
- **Class:** INTERNAL_INCONSISTENCY
- **Severity:** S4
- **Label:** DERIVED
- **Claim challenged (verbatim):** "Primary horizon, next-5-session return. **404 evaluable days.** 6 days
  dropped because a name in the panel carried no realized return. The absence is recorded and the day is
  dropped, never filled." — NPDExperiment/reports/stage_b2/evaluation.md:51-53. Read against
  "| evaluable days | 404 of 415 stored |" — NPDExperiment/progress.md:147.
- **Evidence:**
  - 415 days carry a stored ranking (`var/npd.db:day_status`, `stored` 415 / `model_failed` 17). 404 are
    evaluated. The gap is **11**, of which the report explains 6.
  - Of the 415, exactly **6** fall on dates with a partially missing forward-return panel (2024-11-21,
    2025-03-26, 2025-09-09, 2026-03-12, 2026-05-20, 2026-06-22). These are the 6 the `dropped` counter
    reports.
  - A further **5** fall on the last five sessions of the window (2026-07-20 … 2026-07-24), whose entire
    5-session forward window runs past the end of the sealed store. All 30 names on those dates carry
    `ret IS NULL`, so `read_sealed_returns` (NPDExperiment/src/npd/eval/evaluator.py:81-93, which filters
    `ret IS NOT NULL`) removes the dates entirely and they never reach the `dropped` counter at
    NPDExperiment/src/npd/eval/evaluator.py:482-492.
  - The same structure at the secondary horizon gives 415 − 1 tail − 2 partial = 412, matching
    NPDExperiment/reports/stage_b2/evaluation.md:167.
- **Recomputation:** inputs `/home/kiros-li/Documents/GitHub/NPDExperiment/var/npd.db:model_ranking` (415
  distinct dates) and `/home/kiros-li/Documents/GitHub/NPDExperiment/var/npd_sealed.db:forward_return`
  (432 dates × 30 names × 2 horizons = 25,920 rows; 156 NULLs at h = 5, 32 at h = 1), read
  2026-09-04T23:06Z. Method: classify each stored date as all-null, partially null, or complete at each
  horizon. Result: h = 5 → 5 all-null, 6 partial, 404 complete; h = 1 → 1 all-null, 2 partial, 412 complete.
  Exact. Confirmed twice: the verification pass and this consolidation both report 415 stored, 410
  candidate dates with any return, 404 evaluable and 6 dropped by the counter.
- **What would resolve it:** one sentence in the B.2 report reconciling 415 to 404 — "5 further days have
  no five-session forward window inside the store" — which is the mechanism the registration already
  anticipated.
- **Confidence:** HIGH — the classification is a direct count and reproduces the report's own 404 and 412
  exactly.
- **Invalidated by later commits?:** no — HEAD equals the anchored SHA.
- **Disclosed by the authors?:** partly, and this is why the severity is S4. The mechanism is registered in
  advance: "Days whose forward return lands past the end of the store are still collected. Their forward
  return is absent, recorded as absent, and never filled." — NPDExperiment/REGISTRATION.md:90-91, and the
  registered evaluable counts 427/431 at NPDExperiment/REGISTRATION.md:92-93 embody it. What is missing is
  the arithmetic tying that registered mechanism to the 5 missing days in the B.2 report, which presents
  "6 days dropped" as the whole of the gap.
- **Citation check:** verified (quote EXACT at `reports/stage_b2/evaluation.md:51-53`; figures exact; recomputation reproduced). Re-run first-hand at apply: `var/npd.db` `day_status` holds 415 `stored` / 17 `model_failed` and `model_ranking` covers 415 distinct dates; `var/npd_sealed.db` `forward_return` holds 25,920 rows over 432 dates and 2 horizons, with 156 NULL `ret` at h = 5 and 32 at h = 1; classifying the 415 stored dates gives h = 5 → **5 all-null, 6 partial, 404 complete** and h = 1 → **1 all-null, 2 partial, 412 complete**, matching `evaluation.md:51` (404), `:167` (412, EXACT) and `progress.md:147` (EXACT). The five all-null dates are exactly 2026-07-20 through 07-24 and the six partial dates exactly 2024-11-21, 2025-03-26, 2025-09-09, 2026-03-12, 2026-05-20 and 2026-06-22, as listed. Additionally confirmed: **zero** complete-return days are dropped for a missing baseline at either horizon, so the counter's 6 is entirely the partial-panel cause the report names, and the 5 tail days are removed upstream by `read_sealed_returns` (`src/npd/eval/evaluator.py:81-93`, `ret IS NOT NULL`) before reaching the counter, whose loop is at `:484-492` inside the `:482-492` range cited — exactly the mechanism the finding describes. Severity S4 confirmed: the gap is fully explained by a mechanism registered in advance and the report's only fault is not doing the 415 = 404 + 6 + 5 arithmetic out loud. Kept unchanged.

### AUDIT-C-NPDExperiment-8
- **Repository / SHA:** NPDExperiment / `2d3d0aebf977fb2821ec78c25b370c84ec055920`
- **Hypothesis or artifact:** the mutation-harness report, which is the repository's evidence that its
  guards actually bite
- **Direction:** neutral (a stale count that understates the work done)
- **Class:** STALE_FIGURE
- **Severity:** S4
- **Label:** DERIVED
- **Claim challenged (verbatim):** "**All five caught and restored: True**" —
  NPDExperiment/reports/mutations.md:14
- **Evidence:**
  - The table immediately above that line lists **six** mutations, numbered 1, 2, 3, 4, 6, 5 —
    NPDExperiment/reports/mutations.md:7-12.
  - `reports/mutations.json` holds **six** objects, in the same 1, 2, 3, 4, 6, 5 order, each with
    `"guard_failed_as_required": true` and `"restored_green": true`.
  - The committed generator cannot produce the word "five": at the anchor it emits
    `f"**All {len(results)} caught and restored: {every}**"` — NPDExperiment/scripts/mutations.py:214 —
    which for six results prints "All 6". The literal `"All five"` existed only in the previous revision of
    that line (`git show 3c2a152:scripts/mutations.py`, line 203), changed in the same commit `2c6d683`
    that added mutation 6 and committed this report.
  - `progress.md:176` says "Six mutations run, all caught and restored".
    `reports/session_a1_b1.md:155` says "### Five mutations, all caught" over a five-row table — correct
    for its own commit `02b8560`, which predates mutation 6.
- **Recomputation:** inputs `reports/mutations.json` (6 objects), `scripts/mutations.py:195-220` (the
  writer), and `git show 3c2a152:scripts/mutations.py` (the previous writer). Method: compare the committed
  artifact against the string the committed generator would emit for `len(results) = 6`. Result: the
  artifact's summary line is not producible by the code committed beside it. Re-checked against
  `SNAP/NPDExperiment/` in this consolidation.
- **What would resolve it:** re-run the harness at the anchored code, or correct the line to "All 6". The
  substance — six mutations, each caught by the named guard and each restored green — is unaffected and is
  carried correctly in the json, in the table above the line, and in `progress.md`.
- **Confidence:** HIGH — the generator source at the anchor formats an integer where the artifact carries a
  word.
- **Invalidated by later commits?:** no — HEAD equals the anchored SHA.
- **Disclosed by the authors?:** no.
- **Citation check:** verified (quote EXACT at `reports/mutations.md:14`; figures exact; recomputation reproduced). Re-checked first-hand at apply: the table immediately above the line lists six mutations in the order 1, 2, 3, 4, 6, 5 at `:7-12`; `reports/mutations.json` is a list of **six** objects in that same order, and every one carries `guard_failed_as_required: true` **and** `restored_green: true`, so the trailing `True` is correct and only the word "five" is stale. The anchored generator at `scripts/mutations.py:214` emits `f"**All {len(results)} caught and restored: {every}**"`, which for six results prints "All 6", so the committed artifact is not producible by the code committed beside it; `git show 3c2a152:scripts/mutations.py` line 203 is the previous writer carrying the literal `**All five caught and restored: {every}**`, at exactly the line the finding cites. Commit dates confirmed: `3c2a152` 2026-08-25T10:12:23 −0700, `02b8560` 12:48:04, `2c6d683` 13:13:28. `reports/session_a1_b1.md:155` ("### Five mutations, all caught") is EXACT and correct for its own commit, which predates mutation 6. S4 confirmed: the substance is carried correctly by the json, the table and `progress.md:176`. Kept unchanged.

### AUDIT-C-NPDExperiment-9
- **Repository / SHA:** NPDExperiment / `2d3d0aebf977fb2821ec78c25b370c84ec055920`
- **Hypothesis or artifact:** `CLAUDE.md`, the standing-rules file, against the frozen config and the
  registration at the same SHA
- **Direction:** neutral (hygiene; nothing operational turned on the stale text)
- **Class:** PROVENANCE
- **Severity:** S4
- **Label:** DERIVED
- **Claim challenged (verbatim):** "Three amendments are in force and REGISTRATION.md Section 17 carries the
  evidence for each. … A parse failure escalates that day to `low` and it stays there, because at `minimal`
  the model often cannot hold a 30 label permutation." — NPDExperiment/CLAUDE.md:42-47
- **Evidence:**
  - `git log -- CLAUDE.md` returns exactly two commits, `64b7d41` and `f8304d9`
    (2026-08-25T17:19:11Z). The file was never touched again.
  - At the anchor **five** amendments are in force (1 through 5), not three. Section 17
    (`REGISTRATION.md:442-675`) carries seven amendment entries, of which Amendment 6 is recorded as
    intent carrying "**no pre-registration force**" (NPDExperiment/REGISTRATION.md:628) and Amendment 7
    is headed "VOID" and "is not applied" (NPDExperiment/REGISTRATION.md:661, 668).
  - At the anchor `src/npd/config.py:102-105` holds
    `reasoning_effort_ladder=("minimal", "minimal", "minimal", "minimal", "low")`, set by Amendment 4 at
    `250bc8f` (17:35:37Z) — not "escalates that day to `low` and it stays there", which is Amendment 3's
    superseded ladder.
- **Recomputation:** none. Both files are tracked and anchored; the comparison is a read of
  `SNAP/NPDExperiment/CLAUDE.md` against `SNAP/NPDExperiment/src/npd/config.py` and
  `SNAP/NPDExperiment/REGISTRATION.md` at the same SHA, plus one `git log`.
- **What would resolve it:** one line in `CLAUDE.md` updating the amendment count and the ladder, or a
  pointer stating that Section 17 governs and this file is a snapshot.
- **Confidence:** HIGH — both files are tracked and anchored, and the contradiction is between two files at
  the same commit.
- **Invalidated by later commits?:** no — the anchor is the last commit.
- **Disclosed by the authors?:** no, though the authoritative statement is in Amendment 4 and the config is
  the enforced artifact, so nothing operational turned on the stale text.
- **Citation check:** corrected — one count restated. The evidence read "At the anchor `REGISTRATION.md:442-675` carries **seven** amendments, not three", which mismatches the predicate of the sentence it rebuts: `CLAUDE.md:42` says three amendments are in **force**. Section 17 carries seven amendment *entries*, but Amendment 6 states it carries "no pre-registration force" (`REGISTRATION.md:628`) and Amendment 7 is headed "VOID" and "is not applied" (`:661`, `:668`), so the number in force at the anchor is **five** (Amendments 1 through 5). Restated here and in the JSON. Everything else re-verified first-hand at apply: quote EXACT at `CLAUDE.md:42-47`; `git log -- CLAUDE.md` returns exactly two commits and no more, `64b7d41` (2026-08-25T09:39:00 −0700) and `f8304d9` (10:19:11 −0700 = 17:19:11Z), so the file froze two minutes after the Amendment 3 commit `c4da18c` (17:17:32Z) and was never touched again; the ladder contradiction confirmed at the same SHA, `src/npd/config.py:105` holding `reasoning_effort_ladder=("minimal", "minimal", "minimal", "minimal", "low")` under an Amendment 4 comment at `:102-104` and set at `250bc8f` (17:35:37Z), against `CLAUDE.md`'s Amendment-3 ladder "escalates that day to `low` and it stays there"; and Section 17 does span `REGISTRATION.md:442-675`, the next `##` header (Closure) being at `:678`. The finding correctly declares that no recomputation was needed. Class PROVENANCE, severity S4, label DERIVED and the non-disclosure answer unchanged.


---

## Sound

What verified cleanly, listed so that a reader can see what a negative result was checked against. If the
thesis "this program closed too early or claimed too much" held in the numbers, it would have shown up
here; on twenty of the twenty-six claims with a definite verdict, it did not.

**The deciding numbers.** Every figure the closure turns on reproduces from the repository's own stored
primitives:
- realized minimum detectable contrast **0.0512** (recomputed 0.0512418), and the effective sample size
  201.2 behind it (201.166);
- the verdict itself — model interval −0.027575…+0.039729 with `low < 0`, so `beats_coin` is False, so
  verdict row 3 fires (`evaluator.py:546-547,686-706`), exactly as printed;
- Section 0 coverage **96.1 %** and the GO branch — 415 stored / 432 eligible = 0.960648 against a
  registered ≥ 0.90 bar;
- total spend **6.9378 USD** against a 10.00 USD cap (Σ = 6.9377835 over 922 ledger rows), 920 gate calls,
  0.007508 USD per call, 3.0622 remaining;
- permutation two-sided p **0.5174** (0.5174483, 5,174 hits in 10,000 draws at seed 20260845);
- the negative-control gate: shuffled mean **+0.0001** (+0.00011025), MC band −0.0001…+0.0003, null sd
  0.00925, percentiles −0.0179…+0.0181, PASS.

**The inference machinery.** All eleven interval-shaped and eleven test-shaped objects behave as their code
says and as the registration says. Every one of the ten recomputable intervals reproduces to the printed
digit, including the primary contrast (−0.0673466…+0.0351370), its bootstrap SE (0.0256209), the model mean
IC interval (−0.0275751…+0.0397294) and the secondary-horizon interval. The verdict rule is an
intersection-union conjunction and is correctly left uncorrected, for a reason registered in advance. The
resampling seed 20260825 was fixed at `943ba05`, before any model output existed, so it cannot have been
chosen against the result.

**The registered power arithmetic.** 0.185695, MDE 0.0178685, VIF 3.4, 427 evaluable days → 125.588
effective days, and all sixteen cells of the projection grid reproduce from `src/npd/power.py:33-126`. The
4× sizing statement (1,708 days, MDE 0.02562) is arithmetically correct. So is the "98 percent" ratio
0.36339 / 0.3714 = 0.9785 — it is the *inference* drawn from that ratio, not the ratio, that is finding
**-1**.

**The B.0 and B.1 counts.** 15,474,106 bars; 18,474 symbols; 55 formations at exactly 500 members each;
308,610 features; 432 anonymization days; 432 days per baseline; 12,450 model ranking rows = 415 × 30;
883 attempts across 432 days at 2.04 per day; 175 multi-attempt days; {minimal 813, low 70}; 74 superseded;
53 escalated; 3,514,278 input tokens; 361,641 output of which 217,728 reasoning. All exact. The logistic
fit sample (711 days, 21,322 non-null rows at h = 5, 2022-01-03…2024-10-30) is exact once the eight NULL
rows are accounted for. The registered evaluable counts 427 and 431 are exact.

**The amendment arithmetic that does reproduce.** Amendment 2's calibration projections (11.7812, 1.4045,
safety budget 7.9756, 0.0194 against a 0.025 floor); Amendment 4's compliance table (29 minimal / 12 failed
= 41 %, 19 low / 9 failed = 47 %, 17 of 29 first-attempt = 59 %, 7 of 8 = 88 %); Amendment 5's recorded
0.3494 USD (0.349374, exact) and its 46 % undercount (45.65 %); Section 12.1's pre-spend arithmetic
(5.832 and 10.152).

**The supersession mechanism.** All 883 current-procedure evidence rows carry the one re-frozen digest
`7e6f3d68…`; no second digest appears on any row that has the field; all 415 stored days are drawn from
those rows. The claim that **zero** of the 415 stored rankings came from the superseded template is true.
No superseded day contaminates the sample, which is the substantive point the mis-stated counts in findings
**-4** and **-5** sit next to.

**The pre-registration ordering, under git.** The binding registration `64b7d41` (16:39:00Z) precedes the
first billed call (17:10:48Z) by 31 minutes and the sealed-store write (16:54:33Z) by 15 minutes. Sections
0, 1, 5, 6, 8, 9, 10 and 11 are byte-identical from that commit to the anchor. `DECISIONS.md` and
`progress.md` have zero deleted lines across all eleven commits. Every post-data parameter change is
confined to the model-call layer and each carries a dated amendment. The two post-read amendments are
labelled POST-READ and VOID and the git order confirms both labels; the voided one (10- and 20-session
descriptive horizons) is verifiably not applied — `config.py:85-86` holds only 5 and 1, and no other
horizon appears anywhere in the code or the reports. ADR-010 labels the best-baseline designation
post-hoc, in the commit that made it.

**A cross-repository check.** `backtest/universe.py` in AiTrader hashes to
`8188eea0aef8a4d737e220095b9081071e26e4b4d30cceafb5082d7bfe525529`, matching the digest
`reports/stage_b0/build.md:9-12` records — verified against the live AiTrader working tree (unanchored).

**Two things the referee looked for and did not find.** No multiplicity correction is applied anywhere, and
none is needed anywhere — including the one place where applying one would have been the error. And no
interval or test convention in this repository is anti-conservative: the one-sided `beats_coin` read of a
two-sided bound, the `t_critical = 2.0` constant, and the block length 10 carried to the secondary horizon
all make the authors' own case *harder*, not easier.

---

## Could not be checked and why

| item | why |
|---|---|
| Amendment 4's "16.3 s" and "2.3 s" mean latencies (`REGISTRATION.md:578`) | `latency_s` is recorded as `0.0` on every rejected attempt — the same discard defect Amendment 5 documents for usage — so no mean over the retained ledger is the quantity the amendment measured, and the 8 held-out strict-schema probe calls are not identifiable in `evidence.jsonl` (finding **-3**). Recorded for the reader: the 17 successful free-form `minimal` attempts average 2.031 s, the 10 successful free-form `low` attempts 30.63 s, and the per-day total across the 29 superseded days 12.469 s. None is 16.3 s. |
| Amendment 4's "9.12 USD" / "2.86 USD" 432-day projections (`REGISTRATION.md:579`) | the same 8 probe calls, not isolable in either ledger (finding **-3**). For context, realized current-procedure gate spend was 6.58841 USD over 432 days, 2.3× the 2.86 projection; the 10 USD cap held regardless. The 9.12 figure is internally consistent with Amendment 5: 432 × (0.6429 − 0.030522) / 29 = 9.122. |
| Amendment 5's "actual 0.6429 USD" (`REGISTRATION.md:612`) | the usage behind the 37 unbilled attempts was discarded before it was recorded. **The authors state this themselves** at `REGISTRATION.md:619-622`. Only the "recorded 0.3494" half reconstructs (0.349374, exact), and the 46 % undercount follows from it. |
| "113 tests" in the HTML masthead (`reports/session_record.html:192`) | `def test_` counts **107** at `433dabe`. 113 is plausibly pytest's collected count under parametrization, but establishing that would require running the repository's suite, which the audit rules forbid. Modules (38) and lines (4,699) verify exactly. Not raised as a finding, because the discrepancy has an innocent and likely explanation that cannot be tested here. |
| The predecessor AiTrader figures carried into the registration — the council interval −22.5 to +21.4 bp on 274 calls / 80 clusters (`REGISTRATION.md:38-39`), z −0.046 (`:36`), the pooled confidence Spearman (`:418-420`), the 71.7 % `consolidat` cell (`:434-437`) | external to this repository. No input, estimator or code for any of them exists under `NPDExperiment/`. They are carried in as text and are a matter for the AiTrader audit, not this one. |
| Whether the operator's Section 13 prior was recorded before the sealed store was read (`REGISTRATION.md:343-344`) | the Section 13 fill and every B.2 artifact land in one commit, `2c6d683`, two and a half minutes after the run's own timestamp at `evaluation.md:3`. Git cannot order events inside a working tree. The only in-repo mechanism is `require_amendment_zero()`, which existed at `943ba05` before the first call and refuses to run on the empty marker — a code-enforced ordering, not a recorded one. Not guessed at. No finding: the authors disclose the prior was adopted rather than independent, and that the experiment yields no calibration evidence (`REGISTRATION.md:351-360`). |
| Whether B.2 ran exactly once (`evaluation.md:3`, "Run … Once.") | nothing in git or in the untracked stores records a second run or its absence; the sealed store was opened read-only, so its mtime cannot distinguish one read from five. |
| The pre-image hash of `var/npd_sealed.db` claimed unchanged at B.2 (`progress.md:168-169`) and the hash of `analysis_bars.db` on either side of the B.0 extract (`reports/stage_b0/build.md:9-12`) | neither was ever recorded, so the "unchanged" claims cannot be verified from the repository. The mtime half of the first does check: `2026-08-25 09:54:33 −0700`, before the B.1 collection (12:46) and before the B.2 run (13:10). Only `var/source_hashes_before.txt` survives, for `universe.py` alone. |
| "This repository never installed a systemd unit, a timer, or a cron entry. Verified at closure" (`progress.md:87-90`) | a host-state claim, not a repository claim. Verifying it means enumerating the operator's units and crontabs, which is outside the audit's read scope. |
| Whether `github.com/kirosli00tuff/NPDExperiment` is public, against "Nothing is pushed to any public remote." (`CLAUDE.md:56`) | `origin/main` equals the anchored SHA and `.git/refs/remotes/origin/main` was written 2026-08-29T18:45:18Z, **four days after the anchor**. Whether that repository is public cannot be determined without a network read, and none was attempted. A post-anchor event; recorded, not raised. |
| The `9a174e01…` superseded digest as the producer of the 74 no-digest rows | those rows predate the field that records the digest, so the attribution rests on the ordering of the amendments and on `collect/prompt.py` being untouched between `943ba05` and `250bc8f`, rather than on a stored value. The complementary claim — that all 883 current rows carry `7e6f3d68…` and that the 415 stored days come from them — is directly VERIFIED. |
| **Every B.1 and B.2 figure, as a claim about the anchored commit** | none of the four data files is tracked. The figures verify against the working tree read 2026-09-04; they do not verify against `2d3d0ae` itself, because `2d3d0ae` contains no ranking, no forward return and no ledger row. A reader who clones the repository at the anchor can re-derive none of them. This is the largest single limitation of this audit and it applies to findings **-1**, **-2**, **-3**, **-4**, **-5** and **-7** as well as to the sound results. |

---

## Live-repo access log

`/home/kiros-li/Documents/GitHub/NPDExperiment` — read-only throughout, across all three passes. No write,
no checkout, no branch operation, no stash, no reset, and no repository script executed in place. `.env`
was **not** opened at any point.

`git rev-parse HEAD` = `2d3d0aebf977fb2821ec78c25b370c84ec055920` = the anchored SHA, at the start and end
of every pass.

**Provenance pass** — `git -C /home/kiros-li/Documents/GitHub/NPDExperiment status --porcelain`
BEFORE first access (2026-09-04T18:21:05Z):

```
```
(empty — clean)

AFTER last access (2026-09-04T18:38:54Z):

```
```
(empty — clean)

**Verification pass** — BEFORE first access (2026-09-04T18:21:17Z):

```
```
(empty — clean)

AFTER last access (2026-09-04T18:44:17Z):

```
```
(empty — clean)

**Consolidation pass (this document)** — BEFORE first access (2026-09-04T23:06:07Z):

```
```
(empty — clean)

AFTER last access (2026-09-04T23:07:16Z):

```
```
(empty — clean)

**Citation-check apply pass** — BEFORE first access (2026-09-04T23:26Z):

```
```
(empty — clean)

AFTER last access (2026-09-04T23:38:01Z):

```
```
(empty — clean)

`git rev-parse HEAD` re-read at 23:38:01Z = `2d3d0aebf977fb2821ec78c25b370c84ec055920`, still the anchor.
Reads in this pass: `git log`, `git log -S`, `git show`, `git show --stat`, `git diff`, `git rev-parse`
(including `git show <c>:REGISTRATION.md` at all eleven commits), plus a read-only line parse of
`ledgers/evidence.jsonl` and `ledgers/spend.jsonl` and read-only sqlite against `var/npd.db` and
`var/npd_sealed.db` to re-derive the counts in findings **-3**, **-4**, **-5** and **-7** first-hand.
No write, no checkout, no script executed in place.

Reads performed against `NPDExperiment` across the three passes:
- `git log`, `git show`, `git diff`, `git log -S`, `git log --follow`, `git ls-tree`, `git rev-parse`,
  `git rev-list --count`, `git branch -a`, `git tag`, `git remote -v`
- `ls -la --time-style=full-iso` on `var/`, `ledgers/`, `.git/refs/remotes/origin/`
- read-only sqlite (`file:…?mode=ro&immutable=1`) against `var/npd.db`, `var/npd_sealed.db`,
  `var/npd_fit.db`
- read-only line parse of `ledgers/spend.jsonl` (922 rows) and `ledgers/evidence.jsonl` (959 rows)
- `cat` of `var/source_hashes_before.txt`

Cross-repo read for the `universe.py` source-integrity hash (`AiTrader`, an audited repository, read-only):

**`git -C /home/kiros-li/Documents/GitHub/AiTrader status --porcelain` BEFORE and AFTER
(2026-09-04T18:31:48Z):**

```
 M COLLECTION_LOG.md
```

` M COLLECTION_LOG.md` is the pre-existing dirt named in the audit rules (a collector appends to it) and is
not caused by this audit. The only operation performed was `sha256sum backtest/universe.py`.

**Pre-existing dirt not caused by this audit:** none in `NPDExperiment` — the tree was clean before and
after every pass; ` M COLLECTION_LOG.md` in `AiTrader`, as the rules anticipate. Nothing else was observed
and nothing was modified.

Scratch scripts and outputs live under
`~/.cache/program-audit/scratchpad/work/agentC/npd_verify/` (verification pass: `verify.py`, `ledger.py`,
`acct.py`, `amend.py`, `a3b.py`, `a4.py`, `a5.py`, `b1.py`, `lat.py`, `lat2.py`, `split.py`, `out.json`),
`~/.cache/program-audit/scratchpad/work/agentC-prov-npd/` (provenance pass), and
`~/.cache/program-audit/scratchpad/work/agentC/npd_consol/` (consolidation pass: `spot_corr.py`,
`spot_ledger.py`, `chk.py`, `led.py`, `walk.py`), and
`~/.cache/program-audit/scratchpad/work/agentC-applier-npd/` (citation-check apply pass: `check.py`,
`apply_md.py`, `apply_bullets.py`, `apply_json.py`, `fix_f1.py`, `log.py`).
Nothing was written anywhere inside an audited repository.

**Unanchored caveat, restated once more.** Everything under `var/` and `ledgers/` is untracked. It was read
2026-09-04 between 18:21Z and 23:07Z and may have changed after the 2026-08-25 anchor. Every row count and
every derived figure matches a tracked figure exactly, which makes post-anchor mutation implausible — but
that is inference, not proof.
