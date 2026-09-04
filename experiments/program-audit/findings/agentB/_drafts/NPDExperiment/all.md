# Agent B draft findings — NPDExperiment (part "all")

Repository: NPDExperiment, anchored SHA `2d3d0aebf977fb2821ec78c25b370c84ec055920` (main, 2026-08-25).
Snapshot read: `SNAP/NPDExperiment/`. Live repository touched read-only for git history and for
untracked data under `var/` and `ledgers/` (UNANCHORED; read 2026-09-04 between 05:20 and 05:40 UTC;
those files may have changed after the anchor, though their mtimes are 2026-08-25).

Recomputation environment: the audit venv, scripts under
`.../scratchpad/work/agentB-NPD/` (`repro.py`, `gate_effort.py`, `ev.py`, `epochs.py`, `fit.py`,
`misc.py`). No repository script was executed in place. Every database was opened with
`file:...?immutable=1`.

Twenty findings follow, ordered by severity.

---

### DRAFT-all-1
- **Repository / SHA:** NPDExperiment / 2d3d0aebf977fb2821ec78c25b370c84ec055920
- **Hypothesis or artifact:** The Z.1 "dormant observation" that the model leaned against momentum (ADR-014, closure section of REGISTRATION.md, progress.md Z.1, the B.2 appendix)
- **Direction:** B
- **Class:** UNSUPPORTED_POSITIVE
- **Severity:** S1
- **Label:** DERIVED
- **Claim challenged (verbatim quote):** "**The observation.** Across the evaluable window the model daily rank IC and the momentum daily rank IC were strongly negatively correlated. The model was not producing noise around momentum. It was leaning systematically against it." — NPDExperiment/REGISTRATION.md:727-729 (repeated at NPDExperiment/DECISIONS.md:274-276, NPDExperiment/progress.md:70-72, NPDExperiment/reports/stage_b2/evaluation.md:229-233)
- **Evidence:**
  - The correlation was never measured. `run_b2` (NPDExperiment/src/npd/eval/evaluator.py:575-722) computes `contrast_sd_daily` (line 526-528) and never computes or stores the correlation between the model and any baseline daily IC series; `write_report` (NPDExperiment/src/npd/eval/report.py:29-298) never prints one. The figure was inferred from `sd_diff` alone.
  - The inference assumes both daily IC series carry the null standard deviation. NPDExperiment/reports/stage_b2/evaluation.md:224-227: "The registered grid assumed a daily contrast sd of at most 0.2626, which is the value at correlation zero when each daily IC carries the null standard deviation of 0.185695. The theoretical maximum, reached only at correlation minus one, is 2 times 0.185695, or 0.3714." The same assumption is coded at NPDExperiment/src/npd/power.py:108-116 ("Both have the null standard deviation for the panel size").
  - Measured on the same 404 evaluable days used by B.2 (live `var/npd.db` `model_ranking`/`baseline_ranking`, `var/npd_sealed.db` `forward_return` horizon 5, read 2026-09-04 ~05:30 UTC; n = 404 days, 30 names per day):
    - model daily rank IC: mean +0.0061, **sd 0.25159**
    - `mom_12_1` daily rank IC: mean +0.0222, **sd 0.29364**
    - `logistic`: mean −0.0058, sd 0.29276; `sign_last`: mean −0.0255, sd 0.25597
    - **corr(model, mom_12_1) = +0.1182** — positive and weak, and inside the 0.0-to-0.7 grid the registration says it fell outside of.
  - Every published B.2 figure reproduces exactly from the same data (contrast −0.0161, interval −0.0673 to +0.0351, daily contrast sd 0.36339, bootstrap se 0.02562, realized MDE 0.0512, effective n 201.2, model interval −0.0276 to +0.0397), so the reproduction is of the same object the report describes.
- **Recomputation (if any):**
  - Inputs: model and baseline orders from live `var/npd.db`; sealed returns horizon 5 from live `var/npd_sealed.db`; scorer transcribed from NPDExperiment/src/npd/eval/evaluator.py:96-133 and :471-548; block bootstrap from :160-190 with block 10 and seed 20260825+10 (config at NPDExperiment/src/npd/config.py:105-119).
  - Method: recompute each daily IC series, then Pearson correlation of the model and momentum series, and the identity sd_diff = sqrt(sd_m² + sd_b² − 2·ρ·sd_m·sd_b).
  - Result: sqrt(0.25159² + 0.29364² − 2·0.1182·0.25159·0.29364) = **0.36340**, against the published daily contrast sd of 0.36339 (NPDExperiment/reports/stage_b2/evaluation.md:82). The realized dispersion is fully explained by ρ = **+0.1182**. Solving the repository's own null-sd formula instead gives ρ = 1 − 0.36339²/(2·0.185695²) = **−0.9148**, which is the number the documents describe in words and which the data contradict. The true bound at ρ = −1 is sd_m + sd_b = **0.54523**, so 0.36339 is **66.6 %** of the attainable maximum, not "98 percent". At ρ = 0 with the measured sds the contrast sd would have been **0.38668**, i.e. *larger* than what was realized: the realized correlation reduced the contrast variance rather than inflating it.
- **What would resolve it:** Print corr(model, best baseline) and the two per-series daily IC standard deviations from the stored rankings and the sealed store, and withdraw or restate ADR-014, the closure "Dormant observation" section, progress.md:70-73 and evaluation.md:229-233 against the measured value.
- **Confidence:** HIGH — the claimed correlation is recomputed from the same stored artifacts that reproduce every other published B.2 number to the printed precision.
- **Invalidated by later commits?:** no — the anchor is the closure commit and the repository is marked closed (`_CLOSED_DO_NOT_RUN_HERE`, written 2026-09-02); no later commit exists.
- **Disclosed by authors?:** no — the documents present the correlation as measured ("**The measured basis.**", REGISTRATION.md:731) and only disclaim its *status* ("This is not a finding"), never its derivation or its sign.

---

### DRAFT-all-2
- **Repository / SHA:** NPDExperiment / 2d3d0aebf977fb2821ec78c25b370c84ec055920
- **Hypothesis or artifact:** The stated cause of the power shortfall, and the credit given to ADR-007 for registering it in advance (ADR-011, closure)
- **Direction:** B
- **Class:** STATISTICAL
- **Severity:** S1
- **Label:** DERIVED
- **Claim challenged (verbatim quote):** "The cause is recorded. The realized daily contrast standard deviation came in at **0.36339** against a registered assumption of at most **0.2626**, driven by a strong negative correlation between the model and momentum daily ICs that fell outside the range the registration contemplated.\n\n**ADR-007 registered this failure mode as a risk before collection. It was not discovered afterwards.**" — NPDExperiment/REGISTRATION.md:699-705 (repeated at NPDExperiment/progress.md:159-164 and NPDExperiment/DECISIONS.md:227-229)
- **Evidence:**
  - The registered grid derives every cell from the null daily IC sd. NPDExperiment/src/npd/power.py:112-116: `sd_one = null_ic_sd(n_names)` then `sd_diff = math.sqrt(2.0 * (1.0 - corr)) * sd_one`; docstring at :108-110 "Both have the null standard deviation for the panel size". The grid is printed at NPDExperiment/REGISTRATION.md:231-237.
  - ADR-007 (NPDExperiment/DECISIONS.md:118-139) registers exactly one uncertainty: "the minimum detectable contrast lands between 0.026 and 0.047 **depending on how correlated the model and the best baseline turn out to be**". It contemplates no uncertainty in the per-series standard deviation.
  - Measured (n = 404 evaluable days, live stores, 2026-09-04 ~05:30 UTC): model daily IC sd **0.25159** (+35.5 % over the assumed 0.185695); `mom_12_1` **0.29364** (+58.1 %); `logistic` **0.29276**; `sign_last` **0.25597**. All four series violate the assumption in the same direction.
  - Measured corr(model, `mom_12_1`) = **+0.1182**, which lies inside the registered grid's 0.0-to-0.7 range (NPDExperiment/REGISTRATION.md:231-237), not outside it.
- **Recomputation (if any):** With the measured sds and ρ = +0.1182 the contrast sd is 0.36340 (matches the published 0.36339). Holding the registration's null-sd assumption and setting ρ = +0.1182 would have predicted sd_diff = sqrt(2·(1−0.1182))·0.185695 = **0.24657**, i.e. *below* the registered worst case of 0.2626. The entire overshoot from 0.2626 to 0.36339 is attributable to the per-series dispersion assumption, not to the correlation; the correlation moved the number in the favourable direction.
- **What would resolve it:** Restate the cause as "the daily rank IC of every series was 35 to 58 percent more dispersed than the null value the Section 9 grid assumed", and withdraw the sentence crediting ADR-007 with having registered this failure mode in advance, since ADR-007 registers only correlation uncertainty.
- **Confidence:** HIGH — the registered grid's assumption is explicit in code and prose, and the realized per-series sds are recomputed from the stored artifacts.
- **Invalidated by later commits?:** no — the anchor is the final commit.
- **Disclosed by authors?:** no — the repository asserts the opposite, that the materialized failure mode is the one ADR-007 registered.

---

### DRAFT-all-3
- **Repository / SHA:** NPDExperiment / 2d3d0aebf977fb2821ec78c25b370c84ec055920
- **Hypothesis or artifact:** Task 2, "the pipeline validity gate", the registered negative control of Section 7 clause 3
- **Direction:** B
- **Class:** UNSUPPORTED_POSITIVE
- **Severity:** S1
- **Label:** DERIVED
- **Claim challenged (verbatim quote):** "**Gate verdict: PASS.** The shuffled mean sits inside the registered tolerance of zero. The scorer, the join, and the label mapping behave as a valid pipeline must under randomization, so the numbers below are computed on a pipeline that has been shown to produce zero when it should." — NPDExperiment/reports/stage_b2/evaluation.md:42-45 (generated verbatim at NPDExperiment/src/npd/eval/report.py:85-88); the detection claim is at evaluation.md:29-31 "A non-zero shuffled IC means the scorer, the join, or the label mapping is wrong, and every downstream number would be an artifact."
- **Evidence:**
  - The gate statistic is the grand mean of the within-day permutation distribution: `gate_passed = abs(gate.grand_mean) <= CONTROL_TOLERANCE` (NPDExperiment/src/npd/eval/evaluator.py:624-627, tolerance 0.02 at :553). `within_day_null` (:368-403) shuffles each day's realized-rank row uniformly and correlates it against the fixed predicted ranks 1..n.
  - For any fixed vector of realized ranks, the expectation of Spearman rho against a uniformly random permutation is exactly zero. The statistic therefore has expectation zero **for every possible input**, and its Monte-Carlo standard error at 10,000 draws is sd/100 ≈ 0.0000925 (published sd 0.00925, evaluation.md:38). The registered tolerance of 0.02 is ~216 Monte-Carlo standard errors wide.
  - Demonstrated by substitution on the real panels (n = 404 days, live stores, 2026-09-04 ~05:35 UTC, 2,000 draws each):
    - true join: grand mean **−0.000341**, PASS
    - realized returns replaced by uniform random numbers (no relation to any outcome whatsoever): grand mean **−0.000250**, **PASS**
    - label mapping scrambled (realized ranks attached to the wrong symbol in each day): grand mean **+0.000165**, **PASS**
  - So the two defect classes the report names — a wrong join and a wrong label mapping — both pass the gate, as does a pipeline joined to pure noise.
- **Recomputation (if any):** Inputs: model orders from `var/npd.db model_ranking`; realized ranks from `var/npd_sealed.db forward_return` horizon 5; `within_day_null` transcribed from NPDExperiment/src/npd/eval/evaluator.py:368-403. Method: run the gate statistic on the true rows and on two deliberately corrupted row sets. Result above. Script: `.../work/agentB-NPD/gate_effort.py`.
- **What would resolve it:** Replace the gate with a statistic that has power against the named defects — for example the *unshuffled* mean daily IC of a deliberately mis-joined control, or a check that the null distribution's spread matches 1/sqrt(29)/sqrt(D) — and restate Section 7 clause 3, which currently counts this as one of three contamination defenses (REGISTRATION.md:167-176).
- **Confidence:** HIGH — the zero expectation is a property of the estimator, and it is confirmed empirically on corrupted inputs.
- **Invalidated by later commits?:** no — the anchor is the final commit.
- **Disclosed by authors?:** partially and in the opposite direction. The report discloses that the gate is not a contamination clearance (evaluation.md:29-32), which narrows the claim to pipeline defects; it then asserts, wrongly, that it establishes the scorer, the join and the label mapping. The narrowing disclosure does not cover this finding.

---

### DRAFT-all-4
- **Repository / SHA:** NPDExperiment / 2d3d0aebf977fb2821ec78c25b370c84ec055920
- **Hypothesis or artifact:** Amendment 4, the strict output schema and the re-tuned reasoning-effort ladder
- **Direction:** B
- **Class:** UNSUPPORTED_POSITIVE
- **Severity:** S2
- **Label:** DERIVED
- **Claim challenged (verbatim quote):** "**The ladder is re-tuned.** `(\"minimal\", \"minimal\", \"minimal\", \"minimal\", \"low\")`. Retries are independent samples, and at 88 percent per attempt four cheap attempts leave an expected failure rate near zero." — NPDExperiment/REGISTRATION.md:583-586; the 88 percent comes from "**Measured on 8 held-out window days at `minimal`:**" with "first-attempt compliance | 17 of 29, 59 percent | 7 of 8, 88 percent" — REGISTRATION.md:573-577
- **Evidence (live `ledgers/evidence.jsonl`, 959 rows, read 2026-09-04 ~05:25 UTC; 883 rows carry the in-force prompt digest `7e6f3d68…`, matching the 883 reported at NPDExperiment/reports/stage_b1/collection.md:70):**
  - Realized first-attempt compliance under the strict schema: **257 of 432 = 59.5 %**. The free-form arm the amendment replaced measured 17 of 29 = 58.6 %. The schema delivered no measurable first-attempt improvement.
  - The amendment's own decisive comparison is not significant: Fisher exact on 7/8 versus 17/29 gives **p = 0.216**; and P(X ≥ 7 | n = 8, p = 0.5949) = **0.101**, so the 7-of-8 observation is entirely consistent with the realized 59.5 % rate.
  - "Retries are independent samples" is falsified. Success by attempt index: 1 → 257/432 = 59.5 %, 2 → 57/175 = 32.6 %, 3 → 30/118 = 25.4 %, 4 → 18/88 = 20.5 %, 5 (`low`) → 53/70 = 75.7 %. First attempts versus all later minimal-rung attempts: 257/432 versus 158/451, Fisher exact **p = 4.1e-13**.
  - "expected failure rate near zero": **17 days** terminated in `model_failed` (collection.md:23). Under independence at the claimed p = 0.88 the expected count is 432·0.12⁵ = **0.01 days**; even at the realized p = 0.5949 it is 4.71, and P(X ≥ 17 | λ = 4.71) = **9.5e-06**.
  - The residual failure mode is the one strict mode cannot express. Of the 468 failed attempts under the strict schema, the modal `detail` strings are `label mismatch. missing=['XX'] extra=[]` (duplicate labels) plus 17 non-JSON responses — consistent with the amendment's own note "Uniqueness is not expressible in strict mode" (REGISTRATION.md:570-571), but not with the 88 percent figure it drew from n = 8.
  - The cost projection was also missed: "projected total over 432 days | 9.12 USD | **2.86 USD**" (REGISTRATION.md:579). Realized spend under the strict schema was **6.5884 USD** over the same 432 days (sum of `cost_usd` on the 883 in-force rows), i.e. **2.30×** the projection.
- **Recomputation (if any):** Inputs: `ledgers/evidence.jsonl` fields `prompt_digest`, `attempt`, `state`, `reasoning_effort`, `cost_usd`. Method: group by date under the in-force digest; count successes by attempt index; Fisher exact and Poisson tail tests via scipy. Scripts `.../work/agentB-NPD/ev.py`, `fail.py`.
- **What would resolve it:** A note in Amendment 4 recording the realized first-attempt compliance (59.5 %), the realized per-attempt dependence, and the realized 6.59 USD against the 2.86 USD projection, so a future replay does not inherit an 88 percent per-attempt assumption drawn from eight observations.
- **Confidence:** HIGH — every figure comes from the repository's own append-only evidence ledger, and the 883/175/813/70/53/17 aggregates reproduce collection.md exactly.
- **Invalidated by later commits?:** no — the ledger is unanchored data but its mtime is 2026-08-25 12:46 and its aggregates reproduce the committed 2026-08-25 report.
- **Disclosed by authors?:** no — no document revisits the 88 percent figure or the independence assumption after collection.

---

### DRAFT-all-5
- **Repository / SHA:** NPDExperiment / 2d3d0aebf977fb2821ec78c25b370c84ec055920
- **Hypothesis or artifact:** The claim that Amendment 4 rescued the Section 0 verdict
- **Direction:** B
- **Class:** UNSUPPORTED_POSITIVE
- **Severity:** S2
- **Label:** DERIVED
- **Claim challenged (verbatim quote):** "A strict JSON schema pinning 30 enum-constrained slots cut the projected total from 9.12 USD to a measured 6.94 USD and turned a path heading for BLOCKED into one that fired GO." — NPDExperiment/progress.md:215-217 (also NPDExperiment/reports/session_a1_b1.md:255-257 and the shipped page NPDExperiment/reports/session_record.html:429)
- **Evidence:**
  - Section 0 fires BLOCKED only under 70 percent coverage (NPDExperiment/REGISTRATION.md:18; enforced at NPDExperiment/src/npd/section0.py:62-80). The free-form arm's realized day-level coverage was **27 of 29 = 93.1 %**, above the 90 percent GO bar, when it was replaced (live `ledgers/evidence.jsonl`, 74 rows without a prompt digest across 29 distinct dates, read 2026-09-04 ~05:25 UTC).
  - Of the two non-stored free-form dates, only **2024-11-19** was a terminal failure (5 attempts, all `model_failed`); **2024-12-11** carries a single attempt whose timestamp `2026-08-25T17:30:37.688731+00:00` is the last superseded row in the ledger, i.e. the run was stopped mid-retry to record the amendment. Terminal failure rate free-form 1/29 = 3.4 % versus strict schema 17/432 = 3.9 %; Fisher exact **p = 1.0**.
  - The spend route to BLOCKED is closed by the amendment's own number: the free-form projection is **9.12 USD against a 10.00 USD cap** (REGISTRATION.md:579, cap at REGISTRATION.md:290). Using the repository's own measured free-form rate — "recorded 0.3494 USD against an actual 0.6429 USD" over the first 29 gate days (REGISTRATION.md:612), i.e. 0.02217 USD per day — 432 days project to **9.58 USD**, still inside the cap, and the batch refusal (batch_size 50, NPDExperiment/src/npd/config.py:111; refusal at NPDExperiment/src/npd/ledger/spend.py:109-124) would not have fired on the final 32-day batch (8.868 + 0.709 = 9.58 < 10.00).
  - The stated saving is also a mismatched comparison: 9.12 USD is a projection for the *free-form* arm and 6.94 USD is realized spend including the calibration calls and the superseded attempts; the strict schema's own projection was 2.86 USD (REGISTRATION.md:579) and was exceeded 2.3-fold. The realized saving against the free-form projection is 28 %, not the 69 % the two projections imply.
- **Recomputation (if any):** Inputs as above from `ledgers/evidence.jsonl` and REGISTRATION.md:579, :612, :290. Method: partition evidence rows into the pre-Amendment-4 (no `prompt_digest`) and in-force epochs, count dates reaching `stored`, and project the free-form cap path at the amendment's own measured per-day cost. Script `.../work/agentB-NPD/epochs.py`.
- **What would resolve it:** Replace the BLOCKED sentence with the measured comparison, or produce the coverage or spend arithmetic that put the free-form path under 70 percent coverage.
- **Confidence:** HIGH for the coverage arithmetic (it is a direct count in the repository's own ledger); MEDIUM for the counterfactual spend path, which assumes the measured per-day cost holds for the remaining 403 days.
- **Invalidated by later commits?:** no.
- **Disclosed by authors?:** no — no document states the free-form arm's realized coverage.

---

### DRAFT-all-6
- **Repository / SHA:** NPDExperiment / 2d3d0aebf977fb2821ec78c25b370c84ec055920
- **Hypothesis or artifact:** The descriptive split by realized reasoning effort, registered in Amendment 3 as a B.2 deliverable
- **Direction:** B
- **Class:** PROCESS
- **Severity:** S2
- **Label:** DERIVED
- **Claim challenged (verbatim quote):** "The realized effort is stored per day for exactly this reason, and B.2 reports the outcome split by realized effort alongside the primary contrast." — NPDExperiment/REGISTRATION.md:534-535 (repeated as a forward commitment at NPDExperiment/reports/session_a1_b1.md:268-270 and NPDExperiment/reports/session_record.html:434)
- **Evidence:**
  - The split does not exist. `grep -rn -i effort` over `reports/stage_b2/` returns only NPDExperiment/reports/stage_b2/evaluation.md:204-207, the Amendment-2 qualifier. `B2Result` (NPDExperiment/src/npd/eval/evaluator.py:556-573) carries no effort field; `run_b2` (:575-722) never reads the evidence ledger; `write_report` (NPDExperiment/src/npd/eval/report.py:236-294) emits secondary horizon, window halves and model-versus-coin and nothing else under Task 5.
  - The same report asserts completeness of scope: "It read the sealed store one time. It added no horizon, no baseline, no model, and no robustness variant that the registration does not already name." (evaluation.md:199-200). Nothing states that a registered descriptive was omitted.
  - The omission is not innocuous. Joining the 415 stored days to the realized effort recorded on each stored evidence row and scoring them with the B.2 scorer (n = 404 evaluable days): **`minimal` n = 353, mean daily rank IC −0.0004; `low` n = 51, mean daily rank IC +0.0509**. The reported headline model mean of +0.0061 is produced entirely by the 12.6 % of days that had to be escalated; the days answered at the configured effort read essentially zero. The difference of −0.0513 carries a naive standard error of 0.0404 (t = −1.27) and is **not** statistically significant, so this is a descriptive fact, exactly as Amendment 3 specified it should be — but it is the descriptive fact the registration promised and did not print.
  - Amendment 3 states the reason it registered the split: "Days that needed `low` are days where `minimal` could not hold the format. If that difficulty correlates with anything about the panel, the sample mixes two configurations in a way that is not random." (REGISTRATION.md:531-534). The non-randomness is now demonstrable — see DRAFT-all-4 on the attempt-index dependence.
- **Recomputation (if any):** Inputs: stored-row `reasoning_effort` from live `ledgers/evidence.jsonl` (415 stored days: 362 `minimal`, 53 `low`); daily ICs recomputed from `var/npd.db` and `var/npd_sealed.db` with the B.2 scorer. Method: group the 404 evaluable daily ICs by realized effort. Script `.../work/agentB-NPD/gate_effort.py`.
- **What would resolve it:** Either print the split as registered, or record in the registration that the registered descriptive was not produced and why.
- **Confidence:** HIGH — the absence is a property of the committed code and the committed report.
- **Invalidated by later commits?:** no — the anchor is the final commit and the repository is closed.
- **Disclosed by authors?:** no — the B.2 report and progress.md both describe Task 5 as delivered.

---

### DRAFT-all-7
- **Repository / SHA:** NPDExperiment / 2d3d0aebf977fb2821ec78c25b370c84ec055920
- **Hypothesis or artifact:** The registered power floor that authorized collection, and the B.3 replay schedule that ships from it (REGISTRATION.md Section 9.1 and Section 14)
- **Direction:** B
- **Class:** STATISTICAL
- **Severity:** S2
- **Label:** DERIVED
- **Claim challenged (verbatim quote):** "Each model replays when the calendar grows its clean window past the registered power floor, detectable IC 0.025 at 30 names, which needs roughly 221 trading days after its own guard band." — NPDExperiment/REGISTRATION.md:377-379; the authorization itself is "**0.01787 is below 0.025. The window clears the registered power floor.** Collection is authorized." — REGISTRATION.md:214-215
- **Evidence:**
  - The floor is computed with no overlap term: `registered_floor_mde` = `detection_mde(null_ic_sd(30), float(n_days), t)` (NPDExperiment/src/npd/power.py:129-131), stated at REGISTRATION.md:208-212 as "a one-sample test of the model's own daily rank IC against zero, at t 2.0, with no overlap adjustment".
  - The same registration registers that the overlap inflates the variance of a daily-IC mean by 3.4 at the five-session primary horizon (REGISTRATION.md:223-227; `overlap_vif`, power.py:45-58).
  - When the same one-sample test is actually run with the registered inference, it fails the floor. B.2's model-versus-coin block bootstrap gives a half-width of 0.0337 (NPDExperiment/reports/stage_b2/evaluation.md:250-251, "at a half-width of 0.0337"; interval −0.0276 to +0.0397 at :133), i.e. a realized detectable IC of **0.0337 against the 0.025 floor — 35 % above it**. Recomputed independently: bootstrap se 0.01683 on 404 days, 2·se = 0.0337.
  - The B.3 schedule's 221-day figure inherits the same omission: 2·0.185695/sqrt(D) = 0.025 gives D = 220.7. With the measured model daily IC sd of 0.25159 and the registered VIF of 3.4, the days needed for a 0.025 detectable IC are **(2·0.25159/0.025)²·3.4 ≈ 1,377**, six times the shipped figure.
  - Section 0 makes the power floor a BLOCKED condition ("under 70 percent, or the derived window falls under the power floor", REGISTRATION.md:18), so the choice of floor definition gates the whole experiment.
- **Recomputation (if any):** Inputs: null sd 1/sqrt(29) = 0.185695 (power.py:34-42); VIF 3.4 (power.py:45-58, REGISTRATION.md:225); realized model daily IC sd 0.25159 and bootstrap se 0.01683 from the live stores (n = 404). Method: evaluate the floor formula at D = 432 (0.01787, matches REGISTRATION.md:212), then evaluate the same quantity with the realized dispersion and the registered overlap term. Script `.../work/agentB-NPD/misc.py`.
- **What would resolve it:** Record beside Section 9.1 that the realized one-sample detectable IC was 0.0337 against the 0.025 floor, and re-derive the Section 14 replay threshold with the overlap term, or state explicitly that the replay threshold is defined on the overlap-free secondary horizon.
- **Confidence:** HIGH — the floor's construction is explicit in code, and the realized half-width is printed in the repository's own report.
- **Invalidated by later commits?:** no.
- **Disclosed by authors?:** partially. REGISTRATION.md:208-212 discloses that the floor carries no overlap adjustment, and Section 9.3 discloses that the *contrast* is underpowered. Neither states that the floor's own test fails the floor as realized, and Section 14's shipped 221-day figure is never qualified.

---

### DRAFT-all-8
- **Repository / SHA:** NPDExperiment / 2d3d0aebf977fb2821ec78c25b370c84ec055920
- **Hypothesis or artifact:** The shipped "what a powered version would cost" figure in the closure
- **Direction:** B
- **Class:** ARITHMETIC
- **Severity:** S2
- **Label:** DERIVED
- **Claim challenged (verbatim quote):** "Sizing against the measured 0.36339 rather than the registered assumption requires roughly **four times the evaluable days**, landing near **1,700 trading days** of post-cutoff window." — NPDExperiment/REGISTRATION.md:716-718 (repeated at NPDExperiment/progress.md:51-53), under the heading "**What a powered version would cost.** Recorded here so a future reader does not have to re-derive it." (REGISTRATION.md:712-714)
- **Evidence:**
  - The factor of four corresponds to a target detectable contrast of about 0.026: (0.0512/0.026)² = 3.88, and 427 · 3.88 = 1,656 ≈ "near 1,700". 0.026 is the optimistic end of the registered projection (REGISTRATION.md:216-247, "0.026 to 0.047").
  - The same closure states the standard the design must meet: "The realized minimum detectable contrast was **0.0512**, above the entire realistic effect band of 0.01 to 0.05. **The design could not have detected an effect anywhere in the range the literature reports.**" (REGISTRATION.md:695-697). A design at 0.026 still cannot detect anywhere in 0.010 to 0.026, i.e. the lower ~60 % of the band by width, so it is not "a powered version" by the repository's own criterion.
  - To cover the band (detectable at 0.01) requires (0.0512/0.01)² = **26.2×** the evaluable days, about **10,600 trading days**, roughly 42 calendar years at the closure's own "about 21 trading days a month".
  - The figure is also a 50-percent-power figure. The repository's own grid reports both conventions (REGISTRATION.md:231-237, "detectable at t 2.0" versus "detectable at 80 percent power", ratio 1.4208; `powered_mde`, NPDExperiment/src/npd/power.py:73-84). At 80 percent power the realized detectable contrast is 0.0512 · 1.4208 = **0.0727**, and reaching 0.026 at 80 percent power needs (0.0727/0.026)² = **7.8×**, about **3,340 days**.
- **Recomputation (if any):** Inputs: realized MDE 0.0512 and evaluable-day counts 404/427 (NPDExperiment/reports/stage_b2/evaluation.md:51, :93; REGISTRATION.md:93); band (0.01, 0.05) from NPDExperiment/src/npd/config.py:120; power convention from power.py:73-84. Method: MDE scales as 1/sqrt(D), so the required multiplier is (0.0512/target)². Script `.../work/agentB-NPD/misc.py`.
- **What would resolve it:** State the target the 1,700-day figure achieves (detectable contrast ≈0.026 at t 2.0), and give the figure for covering the registered band beside it.
- **Confidence:** HIGH — the arithmetic is elementary and the inputs are the repository's own printed numbers.
- **Invalidated by later commits?:** no.
- **Disclosed by authors?:** no — the closure names no target for the sizing and frames the result as the cost of a *powered* version.

---

### DRAFT-all-9
- **Repository / SHA:** NPDExperiment / 2d3d0aebf977fb2821ec78c25b370c84ec055920
- **Hypothesis or artifact:** The fired verdict sentence
- **Direction:** B
- **Class:** INTERNAL_INCONSISTENCY
- **Severity:** S3
- **Label:** READ
- **Claim challenged (verbatim quote):** "**the replication confirms the council negative under frontier capability and sane formulation. Closed.**" — NPDExperiment/reports/stage_b2/evaluation.md:127 (generated at NPDExperiment/src/npd/eval/evaluator.py:700-703; registered at REGISTRATION.md:274; repeated at NPDExperiment/progress.md:136-137)
- **Evidence:**
  - Amendment 2 withdrew the frontier-capability condition: "**The limitation this creates, stated plainly.** The gate runs the model with no reasoning budget. A null result is a null for gpt-5-2025-08-07 **at minimal reasoning effort**, not for the model at its best. Every sentence written about the outcome carries that qualifier." — REGISTRATION.md:483-486.
  - The realized configuration confirms it: 813 of 883 attempts at `minimal` (NPDExperiment/reports/stage_b1/collection.md:72), 362 of 415 stored days answered at `minimal` (live evidence ledger).
  - The verdict sentence carrying "under frontier capability" is nonetheless the headline in evaluation.md:127, progress.md:136, and the closure's framing "a frontier model chosen by knowledge cutoff" (REGISTRATION.md:687-688). The premise is also stated as the experiment's reason for existing at NPDExperiment/CLAUDE.md:4-6.
  - The word "confirms" additionally sits against the repository's own reading of its null: "This is an **underpowered unresolved**, not a tight null." (evaluation.md:138-141).
- **Recomputation (if any):** none.
- **What would resolve it:** Amend the verdict-row text to name the realized condition ("at minimal reasoning effort") rather than "frontier capability", or state in the closure that the fired row's registered wording overstates the realized configuration.
- **Confidence:** HIGH — both statements are verbatim in the repository.
- **Invalidated by later commits?:** no.
- **Disclosed by authors?:** yes (NPDExperiment/REGISTRATION.md:483-486 and NPDExperiment/reports/stage_b2/evaluation.md:204-207). The authors disclose the minimal-effort limitation plainly and repeatedly; what no document does is reconcile it with the verdict sentence's "under frontier capability", which is the line that travels.

---

### DRAFT-all-10
- **Repository / SHA:** NPDExperiment / 2d3d0aebf977fb2821ec78c25b370c84ec055920
- **Hypothesis or artifact:** The closure's "Correction to the closing instruction" and the preserved-artifacts accounting
- **Direction:** B
- **Class:** PROVENANCE
- **Severity:** S3
- **Label:** DERIVED
- **Claim challenged (verbatim quote):** "That is the **superseded** pre-Amendment-4 template. It produced the two calibration calls and the 26 superseded attempts, and **zero** of the 415 stored rankings." — NPDExperiment/REGISTRATION.md:778-780 (also "The 26 superseded attempts stay in the ledger and their 0.0286 USD still counts against the cap." — NPDExperiment/reports/session_a1_b1.md:254-255 and NPDExperiment/reports/session_record.html:429)
- **Evidence:**
  - Live `ledgers/evidence.jsonl` (959 rows, read 2026-09-04 ~05:25 UTC): 883 rows carry the in-force digest `7e6f3d68…`, 2 rows are calibration, and **74 rows** are pre-Amendment-4 attempts across **29 distinct dates**. Their recorded cost is **0.318852 USD**, of which 37 rows carry no cost at all (the Amendment-5 defect).
  - The repository's own machine-generated report already says 74: "superseded attempts, kept in the ledger and excluded from these counts: **74**" — NPDExperiment/reports/stage_b1/collection.md:73. The hand-written closure and the shipped HTML page carry 26.
  - 26 is the count of rows with no `reasoning_effort` field, i.e. the pre-Amendment-3 subset only; the 48 attempts made between Amendment 3 and Amendment 4 used the same superseded template and are omitted.
  - The cost figure is carried over from Amendment 3, where it described a different set: "The 9 superseded attempts cost 0.0286 USD" — REGISTRATION.md:543.
  - The claim "zero of the 415 stored rankings" is correct: all 415 stored days carry the in-force digest.
- **Recomputation (if any):** Inputs: `ledgers/evidence.jsonl` fields `prompt_digest`, `reasoning_effort`, `cost_usd`, `date`. Method: partition rows by presence of the in-force digest and sum. Script `.../work/agentB-NPD/ev.py`.
- **What would resolve it:** Correct the count to 74 attempts across 29 dates and the recorded cost to 0.3189 USD in the closure and the session record.
- **Confidence:** HIGH — the correct figure is already printed by the repository's own generator in the same repository.
- **Invalidated by later commits?:** no.
- **Disclosed by authors?:** no — the closure presents this paragraph as a correction to the record.

---

### DRAFT-all-11
- **Repository / SHA:** NPDExperiment / 2d3d0aebf977fb2821ec78c25b370c84ec055920
- **Hypothesis or artifact:** The closure's spend accounting
- **Direction:** B
- **Class:** INTERNAL_INCONSISTENCY
- **Severity:** S3
- **Label:** READ
- **Claim challenged (verbatim quote):** "- **Spend.** Measured at **6.9378 USD** against the **10.00 USD** cap. 3.0622 USD unspent." — NPDExperiment/REGISTRATION.md:789-790 (also NPDExperiment/progress.md:104, and "gate calls billed: **920**" at NPDExperiment/reports/stage_b1/collection.md:47)
- **Evidence:**
  - The live spend ledger holds exactly 922 rows totalling 6.937784 USD (920 `gate` + 2 `calibration`), matching the report.
  - The live evidence ledger records **957** non-calibration gate attempts actually sent, of which **37 carry no cost**. Those 37 calls were billed; Amendment 5 says so: "The undercounted 0.2936 USD from the superseded attempts is not recoverable, because the usage was discarded before it was seen." — REGISTRATION.md:620-622, and "recorded 0.3494 USD against an actual 0.6429 USD, a 46 percent undercount" at :612.
  - So the true spend is ≈ 7.23 USD and the unspent balance ≈ 2.77 USD, and "gate calls billed: 920" is the count of calls *recorded*, not billed.
- **Recomputation (if any):** 6.937784 (ledger) + 0.2935 (Amendment 5's own measured undercount) = **7.2313 USD**; 10.00 − 7.2313 = **2.7687 USD** unspent. Inputs: `ledgers/spend.jsonl` (922 rows), `ledgers/evidence.jsonl` (957 gate attempts, 37 uncosted), REGISTRATION.md:612.
- **What would resolve it:** Report the closure spend as "6.9378 USD recorded, ≈7.23 USD actual after the Amendment-5 undercount", and relabel "gate calls billed" as "gate calls recorded".
- **Confidence:** HIGH — the undercount is the repository's own measured figure.
- **Invalidated by later commits?:** no.
- **Disclosed by authors?:** yes (NPDExperiment/REGISTRATION.md:605-622, Amendment 5). The authors found, measured and recorded the undercount; the finding is that the closure's headline figure and the "unspent" balance were not adjusted for it.

---

### DRAFT-all-12
- **Repository / SHA:** NPDExperiment / 2d3d0aebf977fb2821ec78c25b370c84ec055920
- **Hypothesis or artifact:** Section 15's classification of `model_failed` as operational health rather than sample composition
- **Direction:** B
- **Class:** STATISTICAL
- **Severity:** S3
- **Label:** DERIVED
- **Claim challenged (verbatim quote):** "`model_failed` is operational health. `excluded_pre_cutoff` is sample composition." — NPDExperiment/REGISTRATION.md:405-406 (table at :401, "| `model_failed` | the model did not return a parseable ranking after the registered retries | **operational health** |")
- **Evidence:**
  - The evaluated sample is conditioned on the model having produced a parseable answer: 415 of 432 days entered the store, 17 did not (NPDExperiment/reports/stage_b1/collection.md:23).
  - The repository's own ledger shows that parse difficulty is a day-level property, not an i.i.d. per-attempt event: first attempts succeed at 257/432 = 59.5 %, later minimal-rung attempts at 158/451 = 35.0 % (Fisher exact p = 4.1e-13), and terminal failures number 17 against 4.71 expected under independence at the realized first-attempt rate (Poisson p = 9.5e-06). Days that fail once are materially more likely to keep failing, so the 17 excluded days are a non-random subset selected on the model's own behaviour on that panel.
  - Counting `model_failed` in the Section 0 coverage denominator (REGISTRATION.md:20-23; NPDExperiment/src/npd/section0.py:34-44) is a coverage-accounting choice; it is not a correction for the selection, and no document treats the 17 dropped days as a selection effect on the primary contrast.
  - Magnitude is small — 17 of 432 days, 3.9 % — so this is a stated-classification problem rather than a result-changing one.
- **Recomputation (if any):** Inputs and method as in DRAFT-all-4 (attempt-index success rates from `ledgers/evidence.jsonl`); scipy Fisher exact and Poisson tail. Script `.../work/agentB-NPD/fail.py`.
- **What would resolve it:** Record that the evaluated sample is conditioned on parse success and that parse success is day-dependent, or demonstrate that the 17 excluded panels do not differ from the 415 on any pre-outcome feature.
- **Confidence:** MEDIUM — the day-level dependence is demonstrated at high significance; whether it correlates with anything that would move the primary contrast is not measured here.
- **Invalidated by later commits?:** no.
- **Disclosed by authors?:** partially. Amendment 3 discloses the neighbouring confound for the effort mix (REGISTRATION.md:531-534) but the registration asserts the opposite classification for the dropped days themselves.

---

### DRAFT-all-13
- **Repository / SHA:** NPDExperiment / 2d3d0aebf977fb2821ec78c25b370c84ec055920
- **Hypothesis or artifact:** `reports/mutations.md`, the mutation-harness evidence artifact
- **Direction:** B
- **Class:** PROVENANCE
- **Severity:** S3
- **Label:** DERIVED
- **Claim challenged (verbatim quote):** "Six mutations run, all caught and restored, including the two this stage required: bypassing the Amendment 0 refusal, and letting a non-evaluator module read the sealed store." — NPDExperiment/progress.md:176-178
- **Evidence:**
  - The committed artifact lists six mutations (NPDExperiment/reports/mutations.md:7-12) under the summary line "**All five caught and restored: True**" (:14).
  - The generator writes that line as `f"**All {len(results)} caught and restored: {every}**"` (NPDExperiment/scripts/mutations.py:214, and the same fix at :191). Six results would print "All 6"; one result would print "All 1" and would emit only mutation 6. The committed file matches no output of the committed script, so it was assembled by hand.
  - Git confirms it: at the B.2 commit `2c6d683` the diff to `reports/mutations.md` is a single inserted table row and a single inserted section for mutation 6, spliced above the pre-existing mutation 5, with the "All five" line untouched (`git -C /home/kiros-li/Documents/GitHub/NPDExperiment show 2c6d683 -- reports/mutations.md`). The five earlier mutation outputs are byte-identical to their earlier version, so only mutation 6 was newly executed at B.2 — not "the two this stage required".
- **Recomputation (if any):** none beyond the git diff and the generator source.
- **What would resolve it:** Re-run `scripts/mutations.py` and commit its actual output, or state that the artifact was edited by hand.
- **Confidence:** HIGH — the summary line and the table are mutually inconsistent in the committed file, and the generator's format string decides the question.
- **Invalidated by later commits?:** no — the anchor is the final commit.
- **Disclosed by authors?:** no.

---

### DRAFT-all-14
- **Repository / SHA:** NPDExperiment / 2d3d0aebf977fb2821ec78c25b370c84ec055920
- **Hypothesis or artifact:** The ordering guarantee on Amendment 0, the project's central discipline claim
- **Direction:** B
- **Class:** PROVENANCE
- **Severity:** S3
- **Label:** DERIVED
- **Claim challenged (verbatim quote):** "**The operator's registered prior. Recorded 2026-08-25, before any module touched the sealed store.**" — NPDExperiment/REGISTRATION.md:343-344 (also "Amendment 0 was recorded before any module touched it" — NPDExperiment/progress.md:170-171)
- **Evidence:**
  - No artifact dates the prior earlier than the verdict. `git -C /home/kiros-li/Documents/GitHub/NPDExperiment log --date=iso-strict` shows eleven commits, all on 2026-08-25. Section 13 changes from "reserved / empty" to the recorded 0.05 **in the same commit that fires the verdict**: `2c6d68363ebc83a0b632d0b408a4c6e78b4d135d`, 2026-08-25T13:13:28-07:00, whose diff to REGISTRATION.md is exactly the Section 13 rewrite and nothing else.
  - The evaluation report was written at 2026-08-25T20:10:48.471253+00:00 = 13:10:48-07:00 (NPDExperiment/reports/stage_b2/evaluation.md:3), two minutes and forty seconds before that commit. The previous commit is `433dabe`, 12:48:48-07:00, in which Section 13 still reads empty.
  - The runtime mechanism cannot supply the ordering either: `require_amendment_zero` (NPDExperiment/src/npd/eval/evaluator.py:73-78) only checks that the slot holds a number at run time; it records no timestamp.
  - The substance is unaffected, because the prior was adopted rather than formed: "0.05, ADOPTED FROM THE ASSISTANT. NOT INDEPENDENT." (REGISTRATION.md:349), and the assistant's 0.05 has been in the file since the A.2 commit `64b7d41` at 09:39.
- **Recomputation (if any):** none beyond the git log and diff cited.
- **What would resolve it:** A commit, ledger row or signed file dated before the B.2 run that carries the operator's prior.
- **Confidence:** HIGH for the provenance gap; the claim may well be true, but nothing in the repository evidences it.
- **Invalidated by later commits?:** no.
- **Disclosed by authors?:** no — though the adoption disclosure (REGISTRATION.md:349-368) removes the stake, since an adopted prior could not have been steered by the result.

---

### DRAFT-all-15
- **Repository / SHA:** NPDExperiment / 2d3d0aebf977fb2821ec78c25b370c84ec055920
- **Hypothesis or artifact:** The seal architecture, ADR-008, and the logistic baseline's fit sample
- **Direction:** B
- **Class:** INTERNAL_INCONSISTENCY
- **Severity:** S3
- **Label:** DERIVED
- **Claim challenged (verbatim quote):** "    var/npd_fit.db      dates strictly before the window start. Read by the\n                        logistic baseline to fit once and freeze. **Holds no\n                        window outcome, so reading it leaks nothing.**" — NPDExperiment/src/npd/data/forward_returns.py:6-8 (also "`load_fit_targets` refuses any date after the guard band end, so the fit cannot reach a window outcome even if the two return stores were ever pointed at one file." — NPDExperiment/reports/stage_b0/build.md:79, and ADR-008 at NPDExperiment/DECISIONS.md:158-160)
- **Evidence:**
  - The routing is by the *start* date only: `(fit_rows if date < window_start else sealed_rows).append(packed)` — NPDExperiment/src/npd/data/forward_returns.py:92. A five-session forward return stored under date `t` is realized at `t+5`.
  - Live `var/npd_fit.db` (read 2026-09-04 ~05:38 UTC) holds forward returns for dates 2022-01-03 through 2024-10-30 at horizons 1 and 5, 21,330 rows each, 21,322 non-null at horizon 5 — matching "fitted once on **21322** rows across **711** days" (build.md:75).
  - From `var/npd.db session`, the window starts at 2024-10-31. The five fit dates 2024-10-24, 10-25, 10-28, 10-29 and 10-30 have `t+5` equal to 2024-10-31, 11-01, 11-04, 11-05 and 11-06 — all inside the sealed window. Counting rows: **150 of 21,322 fit rows (0.70 %)** carry a five-session return realized on or after the window start.
  - Magnitude is negligible for a frozen coefficient vector fitted on 21,322 rows, and `logistic` was not the best baseline at the primary horizon, so no published number turns on it. The finding is that three documents assert an absolute property the data contradict.
- **Recomputation (if any):** Inputs: `var/npd_fit.db forward_return` and `var/npd.db session`. Method: locate the window-start session index, list the five preceding sessions and their `t+5` dates, count fit rows at horizon 5 with date ≥ 2024-10-24. Script `.../work/agentB-NPD/fit.py`.
- **What would resolve it:** Route by realization date rather than start date, or restate the claim as "holds no forward return *keyed to* a window date" and note the horizon-length overlap.
- **Confidence:** HIGH — the routing line and the session calendar settle it, and the row count is a direct query.
- **Invalidated by later commits?:** no.
- **Disclosed by authors?:** no — the documents assert the absolute form.

---

### DRAFT-all-16
- **Repository / SHA:** NPDExperiment / 2d3d0aebf977fb2821ec78c25b370c84ec055920
- **Hypothesis or artifact:** CLAUDE.md, the repository's top-level operating document
- **Direction:** B
- **Class:** STALE_FIGURE
- **Severity:** S3
- **Label:** DERIVED
- **Claim challenged (verbatim quote):** "Three amendments are in force and REGISTRATION.md Section 17 carries the evidence for each. `temperature` is not sent, because the endpoint rejects any non-default value for this model. `reasoning_effort` starts at `minimal`, chosen by the registered spend rule against measured tokens. A parse failure escalates that day to `low` and it stays there, because at `minimal` the model often cannot hold a 30 label permutation." — NPDExperiment/CLAUDE.md:42-47
- **Evidence:**
  - Five amendments were in force at the end of B.1 and seven exist at the anchor (REGISTRATION.md:446, :464, :502, :550, :605, :624, :661).
  - The described ladder is Amendment 3's `("minimal", "low")`, superseded by Amendment 4 with `("minimal", "minimal", "minimal", "minimal", "low")` (NPDExperiment/src/npd/config.py:102-105; REGISTRATION.md:583).
  - The stated rationale is the one Amendment 4 refutes: "Amendment 3 was the wrong diagnosis, correctly recorded, and it is superseded here rather than quietly dropped." — REGISTRATION.md:563-564; "**`low` fails as often as `minimal`.** The problem is the output format, not the reasoning budget." — :562-563.
  - Git dates the staleness: `git log -- CLAUDE.md` shows its last change at `f8304d9`, 2026-08-25 10:19, while Amendments 4 and 5 land at `250bc8f`, 10:35.
- **Recomputation (if any):** none.
- **What would resolve it:** Update CLAUDE.md's Boundaries section, or mark it as a stage-B.1-era document.
- **Confidence:** HIGH.
- **Invalidated by later commits?:** no — the anchor is the final commit and no later commit touches CLAUDE.md.
- **Disclosed by authors?:** no.

---

### DRAFT-all-17
- **Repository / SHA:** NPDExperiment / 2d3d0aebf977fb2821ec78c25b370c84ec055920
- **Hypothesis or artifact:** The shipped session record page and the A.1-B.1 session report
- **Direction:** B
- **Class:** INTERNAL_INCONSISTENCY
- **Severity:** S3
- **Label:** READ
- **Claim challenged (verbatim quote):** "It computed no rank IC. It read no outcome against any output. It fired no hypothesis verdict. **It called no frontier model.** It traded nothing and touched no running system." — NPDExperiment/reports/session_record.html:452 (same list at NPDExperiment/reports/session_a1_b1.md:291-293)
- **Evidence:**
  - The session those two documents describe is the one that ran B.1, the live gate collection: 920 recorded gate calls plus 2 calibration calls to `gpt-5-2025-08-07` (NPDExperiment/reports/stage_b1/collection.md:47-48), 957 gate attempts in the live evidence ledger.
  - The repository names that model as the frontier condition of the experiment: "This repository reruns the numeric question under two changed conditions, **frontier capability** and sane formulation." — NPDExperiment/CLAUDE.md:4-6; and the fired verdict reads "under frontier capability" (evaluation.md:127).
  - A charitable reading exists: ADR-001 reserves "the frontier trio" for the C.1 replication models and calls `gpt-5-2025-08-07` "the gate model" that "is not the strongest available" (NPDExperiment/DECISIONS.md:14-24). Under that reading the sentence is true of C.1 only. Nothing in either document signals that reading, and every neighbouring clause in the same list is literally true.
- **Recomputation (if any):** none.
- **What would resolve it:** Rewrite the clause as "called none of the C.1 frontier trio", or drop it.
- **Confidence:** MEDIUM — the term-of-art reading is available in ADR-001, which is why this is not graded higher.
- **Invalidated by later commits?:** no.
- **Disclosed by authors?:** no.

---

### DRAFT-all-18
- **Repository / SHA:** NPDExperiment / 2d3d0aebf977fb2821ec78c25b370c84ec055920
- **Hypothesis or artifact:** Amendment 4's latency comparison
- **Direction:** B
- **Class:** INTERNAL_INCONSISTENCY
- **Severity:** S4
- **Label:** DERIVED
- **Claim challenged (verbatim quote):** "**Measured on 8 held-out window days at `minimal`:**\n\n| metric | free-form array | strict schema |\n|---|---|---|\n| first-attempt compliance | 17 of 29, 59 percent | 7 of 8, 88 percent |\n| mean latency | 16.3 s per attempt | 2.3 s |" — NPDExperiment/REGISTRATION.md:573-579 (repeated as "cut mean latency from 16.3 to about 3 seconds per attempt" — NPDExperiment/reports/session_a1_b1.md:256)
- **Evidence (live `ledgers/evidence.jsonl`, read 2026-09-04 ~05:25 UTC):**
  - Free-form attempts at `minimal`: 29 attempts, mean latency **1.19 s**. Free-form attempts at `low`: 19 attempts, mean latency **16.12 s**. The 16.3 s figure is the `low`-effort number, presented in a table headed "at `minimal`".
  - Realized strict-schema latency: **3.54 s** over 883 attempts, i.e. three times the free-form `minimal` figure, not one seventh of it. The calibration file records the same pattern independently: `latency_s` 31.43 at `low` and 3.19 at `minimal` (NPDExperiment/reports/stage_b1/calibration.json, calibration_minimal.json).
- **Recomputation (if any):** mean of `latency_s` grouped by `reasoning_effort` within the pre-Amendment-4 and in-force epochs. Script `.../work/agentB-NPD/epochs.py`.
- **What would resolve it:** Label the 16.3 s figure as the `low`-effort latency, and give the free-form `minimal` latency beside it.
- **Confidence:** HIGH — the ledger figures reproduce the amendment's other rows (`minimal` 17/29 stored, `low` 10/19 stored) exactly.
- **Invalidated by later commits?:** no.
- **Disclosed by authors?:** no.

---

### DRAFT-all-19
- **Repository / SHA:** NPDExperiment / 2d3d0aebf977fb2821ec78c25b370c84ec055920
- **Hypothesis or artifact:** The enforcement site for Section 0's BLOCKED-on-power condition
- **Direction:** B
- **Class:** INTERNAL_INCONSISTENCY
- **Severity:** S4
- **Label:** DERIVED
- **Claim challenged (verbatim quote):** "| BLOCKED | under 70 percent, **or the derived window falls under the power floor** | no verdict claimed |" — NPDExperiment/REGISTRATION.md:18
- **Evidence:**
  - The enforced floor is a raw day count, not the stated detectable IC: `rationale = (f"the derived window falls under the power floor of " f"{cfg.min_trading_days} trading days. No verdict claimed.")` — NPDExperiment/src/npd/section0.py:58-61, with `min_trading_days=200` at NPDExperiment/src/npd/config.py:80.
  - The stated floor is "detectable IC 0.025 at 30 names" (REGISTRATION.md:208), which needs 220.7 trading days (2·0.185695/sqrt(D) = 0.025). A 200-day window gives 2·0.185695/sqrt(200) = **0.02626**, above the floor.
  - So windows of 200 to 220 days pass the coded gate while failing the registered floor. The realized window of 432 days is not affected.
- **Recomputation (if any):** `detection_mde` (NPDExperiment/src/npd/power.py:66-70) evaluated at D = 200 and D = 221. Script `.../work/agentB-NPD/misc.py`.
- **What would resolve it:** Set `min_trading_days` to 221, or enforce the MDE directly in `section0.fire`.
- **Confidence:** HIGH.
- **Invalidated by later commits?:** no.
- **Disclosed by authors?:** no.

---

### DRAFT-all-20
- **Repository / SHA:** NPDExperiment / 2d3d0aebf977fb2821ec78c25b370c84ec055920
- **Hypothesis or artifact:** The report generator's latent "tight null" branch
- **Direction:** B
- **Class:** STATISTICAL
- **Severity:** S4
- **Label:** DERIVED
- **Claim challenged (verbatim quote):** "        tight = abs(p.model_interval.high) < 0.02 and abs(p.model_interval.low) < 0.02" ... "            a(\"most of the realistic band 0.01 to 0.05. The sample had the resolution to\")\n            a(\"find an effect of the size the literature reports and did not find one.\")" — NPDExperiment/src/npd/eval/report.py:208, :215-216
- **Evidence:**
  - The branch would print "This is a **tight null**" and the resolution claim whenever both interval bounds are inside ±0.02, while the registered realistic band's lower end is 0.01 (NPDExperiment/src/npd/config.py:120). An interval of ±0.019 does not resolve effects of 0.01 to 0.019, so the branch's own text would overstate what such a sample established.
  - The threshold and its text were written in the same commit that fired the verdict (`2c6d683`; `src/npd/eval/report.py` created there, 305 lines), i.e. with the outcome available. The branch did not fire — the report printed the "underpowered unresolved" alternative (NPDExperiment/reports/stage_b2/evaluation.md:138-141) — so no published statement rests on it.
- **Recomputation (if any):** none.
- **What would resolve it:** Tie the threshold to `cfg.realistic_effect_band[0]` rather than a literal 0.02, and soften the accompanying text.
- **Confidence:** HIGH that the branch is as described; it is latent, which is why it is S4.
- **Invalidated by later commits?:** no.
- **Disclosed by authors?:** no.

---

## What I checked and found sound

Read completely: `CLAUDE.md`, `REGISTRATION.md` (790 lines), `DECISIONS.md` (289 lines), `progress.md`
(351 lines), `reports/stage_b2/evaluation.md`, `reports/stage_b1/collection.md` + `collection.json`,
`reports/session_a1_b1.md`, `reports/session_record.html` (rendered text), `reports/stage_b0/build.md`,
`reports/stage_b0b/mock_run.md`, `reports/mutations.md` + `.json`, both calibration JSON files,
`src/npd/eval/evaluator.py`, `src/npd/eval/report.py`, `src/npd/power.py`, `src/npd/section0.py`,
`src/npd/config.py`, `src/npd/ledger/spend.py`, `src/npd/data/forward_returns.py`, the amendment-zero
guards in `tests/test_guards.py`, and `scripts/report_b1.py` / `scripts/mutations.py` / `scripts/calibrate.py`
where they generate published numbers.

Where the sceptical thesis did **not** hold:

- **Every published B.2 number reproduces exactly.** Recomputing from the live stores with the
  repository's own scorer, block length and seeds gives 404 evaluable days, 6 dropped, model mean
  +0.0061, `mom_12_1` +0.0222, `logistic` −0.0058, `sign_last` −0.0255, contrast −0.0161, interval
  −0.0673 to +0.0351, daily contrast sd 0.36339, bootstrap se 0.02562, realized MDE 0.0512, effective
  n 201.2, model interval −0.0276 to +0.0397, secondary 412 days. No arithmetic error in the reported
  statistics (`reports/stage_b2/evaluation.md:51-134`, :167-173).
- **The registered inference parameters were fixed before any data existed and never touched
  afterwards.** `git log -- src/npd/config.py` shows four commits, the last at 10:35 (Amendment 4);
  `bootstrap_resamples`, `permutation_resamples`, `t_critical`, `realistic_effect_band`,
  `coverage_go_floor`, `panel_seed`, `primary_horizon_sessions` all date from `64b7d41` at 09:39.
  Neither the B.2 commit nor the closure commit modifies `config.py`. The 0.02 control tolerance
  likewise predates collection (`assert_control_collapsed(..., tolerance: float = 0.02)` in
  `evaluator.py` at `943ba05`, 10:06). The only registration change at the B.2 commit is Section 13.
- **The after-the-fact best-baseline rule is genuinely conservative, as ADR-010 claims, and its cost
  is real.** Recomputed: the model beats `sign_last` by +0.0316 with a bootstrap interval of +0.0009
  to +0.0623 — the one interval in the whole repository that excludes zero. Selecting `mom_12_1`
  instead of the weakest baseline turned a nominal positive into a null. ADR-010's limiting clause
  ("conservative in this direction and only this direction", `DECISIONS.md:198`) is accurate: the
  chosen baseline also happens to yield the largest realized MDE (0.0512 versus 0.0307 against
  `sign_last`), which makes the underpowering narrative look worse, and the ADR does not claim
  otherwise.
- **The within-day permutation test (Task 4) is a valid exact test.** I checked whether it was
  anti-conservative under the five-session overlap; it is not — the shuffles are independent across
  days, so under the sharp exchangeability null the daily ICs are independent and the null sd of
  0.00926 (= 0.185695/sqrt(404)) is correct for that null.
- **The seal held operationally.** `var/npd_sealed.db` mtime is 2026-08-25 09:54, i.e. the B.0 build,
  unchanged through the B.2 run at 13:10 and the closure at 13:26, consistent with `progress.md:171-173`.
  `read_sealed_returns` has exactly one caller (`evaluator.py:81-93`, called at :597-598).
- **The collection ledger reproduces every operational figure in `collection.md`:** 883 in-force
  attempts, 175 multi-attempt days, 813 `minimal` / 70 `low`, 74 superseded, 53 escalated stored days,
  415 stored, 17 `model_failed`, 920 spend rows totalling 6.937784 USD, input 3,514,278 / output
  361,641 / reasoning 217,728 tokens over the in-force epoch. The one accounting seam is that the
  spend row count (920) and the token totals (883 rows) sit on different denominators in the same
  table — noted, but too small to raise separately.
- **Coverage and integrity claims check out:** 415/432 = 96.06 % ≈ 96.1 %; `model_ranking` holds
  12,450 rows = 415 × 30; `baseline_ranking` holds 38,880 = 432 × 3 × 30; the sealed store holds
  25,920 = 432 × 30 × 2. The 404-of-415 evaluable count reconciles as 415 − 5 tail days with no
  five-session return − 6 incomplete days, matching the registered 427-of-432 evaluable count
  (`REGISTRATION.md:90-93`); the report explains only the 6, which is a presentation gap rather than
  an error.
- **Amendment 2's decision rule was applied as registered**, even though its calibration projection
  (1.4045 USD) proved 4.7× optimistic against the realized 6.59 USD: `low` would still have failed the
  80-percent safety budget under the realized costs, so the rule's outcome does not change. The
  "road not taken" paragraph (`REGISTRATION.md:488-496`) declines the tempting post-hoc option and
  says why.
- **Amendment 3 is kept rather than deleted** after being refuted, and Amendment 7 is voided rather
  than applied (`DECISIONS.md:249-266`) — both are the harder choice, and both are made.
- **The C.1 gate was not authorized** and nothing downstream of it is claimed
  (`REGISTRATION.md:658-659`), which is consistent with the fired verdict row.
- Things I looked for and did **not** find: any post-hoc change to a registered threshold, any
  amendment that rescued a verdict, any second read of the sealed store, any horizon or baseline added
  after the fact, any positive promoted from a descriptive, and any `news_experiment.db` access
  (`grep -rn news_experiment src/` returns only the guard that forbids it).

## Live-repo access log

Before (first live access, 2026-09-04 ~05:22 UTC):

```
$ git -C /home/kiros-li/Documents/GitHub/NPDExperiment status --porcelain
(no output)
```

After (last live access, 2026-09-04 ~05:40 UTC):

```
$ git -C /home/kiros-li/Documents/GitHub/NPDExperiment status --porcelain
(no output)
```

The working tree was clean before and after. Note that the repository contains an untracked marker
file `_CLOSED_DO_NOT_RUN_HERE` (mtime 2026-09-02 22:38) which does not appear in `status --porcelain`
because it is excluded via `.git/info/exclude`, as that file itself states; it is not mine and I did
not create, modify or remove it. Live access was limited to `git log` / `git show`, `cat` on
`ledgers/*.jsonl`, and read-only SQLite connections opened with `file:...?immutable=1` on
`var/npd.db`, `var/npd_sealed.db` and `var/npd_fit.db`. `.env` was never opened.
