# Agent A findings. NPDExperiment

Repository NPDExperiment at anchored SHA `2d3d0aebf977fb2821ec78c25b370c84ec055920` (main, 2026-08-25). Direction A: the program closed the hypothesis too early or too hard. Tracked content read from SNAP/NPDExperiment. Untracked data (`var/npd.db`, `var/npd_sealed.db`, `ledgers/evidence.jsonl`, `ledgers/spend.jsonl`) was read read-only from the live working tree; those reads are UNANCHORED, read times are given per figure, and the files may have changed after the anchor.

## Summary. The strongest case for the thesis in this repository

The primary verdict is not the weak point and I do not challenge it: at the registered floor the model did not beat a coin, and the authors themselves label the result an "underpowered unresolved, not a tight null" (evaluation.md:139-141) and say the question is "closed **by operator decision, not by evidence**" (REGISTRATION.md:709-710). The weak point is the *causal story* the closure tells about why the design was underpowered. Four documents state as measured fact that the model was "leaning systematically against" momentum; recomputation from the stored rankings and sealed returns gives corr(model, mom_12_1) = **+0.1182** (n = 404), not a correlation near minus one — the contrast sd of 0.36339 comes from per-series dispersion 35 to 58 percent above the assumed null sd, i.e. from a registration-stage modelling assumption, not from model behaviour. Around that error sit three closures that hold less firmly than they read: a registered descriptive split that was never delivered while the report claims completeness, a registered reopen schedule whose 221-day trigger the closure's own 1,700-day sizing has made stale, and a closure cost section that prices exactly one route to a powered result and calls it unavailable while omitting the ~16 to 21 USD variant the registration itself named, with 3.0622 USD unspent under the cap.

The whole B.2 computation reproduces exactly from stored primitives (every figure in `reports/stage_b2/evaluation.md`, to four decimals), so the disagreements below are about interpretation and completeness, never about arithmetic in the pipeline.

Recomputation scripts and outputs: `scratchpad/work/agentA/recompute.py`, `recompute.out`, `supp.py`, `supp.out` (under the work directory named in COMMON_RULES).

---

## Findings

### AUDIT-A-NPDExperiment-1

- **ID:** AUDIT-A-NPDExperiment-1
- **Repository / SHA:** NPDExperiment / `2d3d0aebf977fb2821ec78c25b370c84ec055920`
- **Hypothesis or artifact:** The Closure's causal diagnosis of the realized under-power, and the ADR-014 "dormant observation" that the model leaned against momentum (REGISTRATION.md Closure, DECISIONS.md ADR-014, progress.md Z.1, evaluation.md Appendix)
- **Direction:** A
- **Class:** ARITHMETIC
- **Severity:** S1
- **Label:** DERIVED
- **Claim challenged (verbatim, with file:line):**
  - "The cause is recorded. The realized daily contrast standard deviation came in at **0.36339** against a registered assumption of at most **0.2626**, driven by a strong negative correlation between the model and momentum daily ICs that fell outside the range the registration contemplated." — NPDExperiment/REGISTRATION.md:699-702
  - "**ADR-007 registered this failure mode as a risk before collection. It was not discovered afterwards.**" — NPDExperiment/REGISTRATION.md:704-705
  - "**The observation.** Across the evaluable window the model daily rank IC and the momentum daily rank IC were strongly negatively correlated. The model was not producing noise around momentum. It was leaning systematically against it." — NPDExperiment/REGISTRATION.md:727-729
  - "**The measured basis.** The realized daily contrast standard deviation of 0.36339 sits at 98 percent of the theoretical maximum of 0.3714, which is reached only at correlation minus one." — NPDExperiment/REGISTRATION.md:731-733
  - "**The realized 0.36339 sits at 98 percent of that maximum.** The model daily rank IC and the momentum daily rank IC are therefore strongly negatively correlated across this window, far outside the 0.0 to 0.7 range the registration contemplated." — NPDExperiment/reports/stage_b2/evaluation.md:229-232
  - Same claim restated at NPDExperiment/DECISIONS.md:272-276 and NPDExperiment/progress.md:41-45 and :70-73.
- **Evidence (figures with n, each with file:line or data path + read time):**
  - The correlation was never measured. It was *inferred* from the contrast sd under the assumption that both daily IC series carry the null sd 0.185695. The assumption is stated at NPDExperiment/reports/stage_b2/evaluation.md:224-227 ("which is the value at correlation zero when each daily IC carries the null standard deviation of 0.185695") and encoded in the power module: "Both have the null / standard deviation for the panel size, so the difference has standard / deviation sqrt(2 * (1 - corr)) times that value." — NPDExperiment/src/npd/power.py:107-109. Null sd 1/sqrt(29) = 0.185695 at NPDExperiment/REGISTRATION.md:203-204.
  - Recomputed from the 404 evaluable primary-horizon days (live `var/npd.db` `model_ranking` and `baseline_ranking` joined to live `var/npd_sealed.db` `forward_return` at horizon 5; read 2026-09-03T06:32:54Z, UNANCHORED): **corr(model daily IC, mom_12_1 daily IC) = +0.1182, n = 404**.
  - Realized per-series daily IC sds on the same 404 days: model **0.25159**, mom_12_1 **0.29364**, logistic 0.29276, sign_last 0.25597 — every series 35 to 58 percent above the assumed 0.185695.
  - The identity sqrt(0.25159² + 0.29364² − 2 × 0.1182 × 0.25159 × 0.29364) = **0.363389** reproduces the published 0.36339 (NPDExperiment/reports/stage_b2/evaluation.md:82) exactly. The inflation is entirely per-series dispersion at a mildly *positive* correlation.
  - The registered risk was a different one. ADR-007 registers a correlation-range risk: "the minimum detectable contrast / lands between 0.026 and 0.047 depending on how correlated the model and the / best baseline turn out to be" — NPDExperiment/DECISIONS.md:126-128, grid `correlations=(0.0, 0.3, 0.5, 0.7)` at NPDExperiment/src/npd/power.py:103. Dispersion of each series above the null sd is not in that grid, so "ADR-007 registered this failure mode" (REGISTRATION.md:704-705) is false as stated.
  - The registered overlap penalty was in fact *over*-estimated, not under: realized effective n 201.2 on 404 days (NPDExperiment/reports/stage_b2/evaluation.md:92) implies a realized VIF of 2.0 against the registered "VIF = 1 + 2 * sum_{k=1..4} (1 - k/5)^2 = 3.4" (NPDExperiment/REGISTRATION.md:225).
- **Recomputation:** Inputs: `model_ranking` (415 days) and `baseline_ranking` (3 × 432 days) from live `var/npd.db`; `forward_return` horizon 5 from live `var/npd_sealed.db`; evaluable-day rule and `daily_ic` copied from NPDExperiment/src/npd/eval/evaluator.py:96-133 and :482-506; null sd from REGISTRATION.md:203-204. Method: daily Spearman IC per series, sample sd (ddof 1), Pearson correlation between the model and momentum series, and the difference-of-series identity. Result: corr = +0.1182 (n 404); sd_model = 0.25159; sd_mom = 0.29364; sd_contrast = 0.363389. Counterfactual: had the registered grid used the realized correlation with null sds, the projected MDC would have been 2 × sqrt(2 × (1 − 0.1182)) × 0.185695 / sqrt(125.6) = 0.0440 (0.0348 at the realized effective n of 201.2); the realized 0.0512 is explained by the per-series sd, not by correlation. Script `scratchpad/work/agentA/recompute.py`, output `recompute.out`.
- **What would resolve it:** Replace the inferred correlation in the Closure, ADR-014, progress.md Z.1 and the evaluation Appendix with the measured value (+0.118, n 404) and the measured per-series sds; restate the cause of the under-power as a registration-stage modelling assumption (null-sd daily ICs for real cross-sectional returns) rather than a model behaviour; correct "ADR-007 registered this failure mode" to say the registered risk was correlation, not dispersion; withdraw or re-base the dormant observation. Note that the per-series dispersion of the three mechanical baselines was measurable before any spend, on the 711-day fit period whose forward returns sit unsealed in `var/npd_fit.db` (NPDExperiment/reports/stage_b0/build.md:75-79, 85-88), subject to registering a reader for that store.
- **Confidence:** HIGH — the correlation and the sds are direct computations on the stored rankings and sealed returns, and they reproduce every published figure to four decimals.
- **Could later commits invalidate this?:** no — HEAD of the live repository equals the anchored SHA; the only post-anchor artefact is an untracked closure marker dated 2026-09-02 that changes no result.
- **Disclosed by authors?:** no. The authors disclose the *assumption* (evaluation.md:224-227) but present the inferred negative correlation as "The measured basis" (REGISTRATION.md:731) and as fact in four documents. Direction note for the orchestrator: this finding also reads as Direction B against ADR-014's dormant observation; it is filed under A because the closure narrative ("leaning systematically against" momentum, "registered as a risk before collection") is what makes the closure read as final and as a model failure rather than a registration error. The primary verdict is unaffected.

### AUDIT-A-NPDExperiment-2

- **ID:** AUDIT-A-NPDExperiment-2
- **Repository / SHA:** NPDExperiment / `2d3d0aebf977fb2821ec78c25b370c84ec055920`
- **Hypothesis or artifact:** Amendment 3's registered descriptive — the B.2 outcome split by realized reasoning effort
- **Direction:** A
- **Class:** PROCESS
- **Severity:** S3
- **Label:** DERIVED
- **Claim challenged (verbatim, with file:line):**
  - "The realized effort is stored per day for exactly this reason, and B.2 reports the outcome split by realized effort alongside the primary contrast. The split is descriptive. It does not become a verdict, under Clause 1." — NPDExperiment/REGISTRATION.md:534-536
  - "B.2 reports the outcome split by realized effort beside the primary contrast, as a descriptive split that never becomes a verdict, under Clause 1." — NPDExperiment/reports/session_a1_b1.md:269-270
  - The completeness claim it collides with: "It added no horizon, no baseline, no model, and no robustness variant that the registration does not already name." — NPDExperiment/reports/stage_b2/evaluation.md:199-200
- **Evidence (figures with n, each with file:line or data path + read time):**
  - The split appears nowhere in NPDExperiment/reports/stage_b2/evaluation.md; its only mention of effort is the carried-forward limitation at :204-207.
  - The code could not have produced it: the result type `B2Result` (NPDExperiment/src/npd/eval/evaluator.py:556-572) carries no effort field, `run_b2` (:575-703) never reads the evidence ledger, and `write_report` (NPDExperiment/src/npd/eval/report.py:29-298) renders no split. `grep -rn effort src/npd/eval/` matches only the limitation prose at NPDExperiment/src/npd/eval/report.py:292-293.
  - The realized effort per stored day was available: 813 `minimal` and 70 `low` attempts, and "days whose stored answer came from `low` after an escalation: **53**" — NPDExperiment/reports/stage_b1/collection.md:72-75. Live `ledgers/evidence.jsonl` (read 2026-09-03T06:32:54Z, UNANCHORED) gives the same counts and 362 `minimal` / 53 `low` stored days under the in-force prompt digest `7e6f3d68...` (REGISTRATION.md:594).
  - Recomputed split (descriptive only, UNANCHORED). Primary horizon (5 sessions): `minimal` **n = 353**, model mean daily rank IC **−0.0004** (sd 0.2481, naive SE 0.0132); `low` **n = 51**, model mean daily rank IC **+0.0509** (sd 0.2728, naive SE 0.0382, SE 0.0704 at the registered VIF 3.4). On those 51 days mom_12_1 read −0.0001 and the model-minus-momentum contrast +0.0510. Secondary horizon (1 session): `minimal` n = 360 → −0.0207; `low` n = 52 → −0.0171; no difference.
  - The `low` days are spread across 18 of the 21 window months, at most 5 in any month (`supp.out`), so the primary-horizon difference is not a first-half artefact. At n = 51 it is roughly 0.7 to 1.3 standard errors, and the subsample is the non-random one Amendment 3 itself warned about: "Days that needed `low` are days / where `minimal` could not hold the format. If that difficulty correlates with / anything about the panel, the sample mixes two configurations in a way that is / not random." — NPDExperiment/REGISTRATION.md:531-534.
- **Recomputation:** Inputs: stored-day effort from live `ledgers/evidence.jsonl` rows with state `stored` and prompt_digest `7e6f3d68...`; daily ICs as in AUDIT-A-NPDExperiment-1. Method: partition the 404 evaluable primary days (and 412 secondary days) by the effort recorded on the stored row; means, sds, naive SE and SE at VIF 3.4 (REGISTRATION.md:225). Results as above. Script `scratchpad/work/agentA/recompute.py`, output `recompute.out` (section "stored days by realized effort").
- **What would resolve it:** Append the registered split to the B.2 record as the descriptive it was registered to be, with its n and standard error, and note in the closure that the "at minimal reasoning effort" qualifier (REGISTRATION.md:483-486; evaluation.md:204-207) is the one dimension on which the sample carried in-window evidence, and that this evidence was not reported. Nothing here changes the verdict row.
- **Confidence:** HIGH — the omission is verifiable by inspection of the report, the evaluator and the report writer; the recomputed split is descriptive and its imprecision is stated.
- **Could later commits invalidate this?:** no — no commits after the anchor.
- **Disclosed by authors?:** no — the evaluation asserts completeness against the registration (evaluation.md:199-200) and nowhere says the registered split was dropped.

### AUDIT-A-NPDExperiment-3

- **ID:** AUDIT-A-NPDExperiment-3
- **Repository / SHA:** NPDExperiment / `2d3d0aebf977fb2821ec78c25b370c84ec055920`
- **Hypothesis or artifact:** Section 14 B.3 replay schedule (the registered reopen path for Kimi K3, Qwen 3.8 Max, GLM-5.2) and the power floor the code enforces
- **Direction:** A
- **Class:** INTERNAL_INCONSISTENCY
- **Severity:** S3
- **Label:** DERIVED
- **Claim challenged (verbatim, with file:line):**
  - "Each model replays when the calendar grows its clean window past the registered power floor, detectable IC 0.025 at 30 names, which needs roughly 221 trading days after its own guard band." — NPDExperiment/REGISTRATION.md:377-379
  - "| Kimi K3 | 2026 vintage, verify before computing the window | replays roughly mid 2027 |" — NPDExperiment/REGISTRATION.md:383
  - "| GLM-5.2 | 2026 vintage, verify before computing the window | replays roughly mid 2027 |" — NPDExperiment/REGISTRATION.md:385
  - Against the closure's own re-sizing: "Sizing against the measured 0.36339 rather than the registered assumption requires roughly **four times the evaluable days**, landing near **1,700 trading days** of post-cutoff window." — NPDExperiment/REGISTRATION.md:716-718
- **Evidence (figures with n, each with file:line or data path + read time):**
  - The 221-day trigger is 2.0 × 0.185695 / sqrt(221) = 0.0250, i.e. the null sd with no overlap adjustment — the Section 9.1 definition "It is a one-sample test of the model's own daily rank IC against zero, at t / 2.0, with no overlap adjustment." (NPDExperiment/REGISTRATION.md:209-210) and the code `registered_floor_mde` at NPDExperiment/src/npd/power.py:129-131.
  - The closure re-sizes the design on realized dispersion to "near **1,700 trading days**" (REGISTRATION.md:716-718) but leaves Section 14 unamended, so the registered reopen trigger and the closure's own sizing differ by a factor of about eight.
  - On the realized model daily-IC sd of 0.25159 (n 404, AUDIT-A-NPDExperiment-1) the same 0.025 floor needs (2 × 0.25159 / 0.025)² = **405** days with no overlap adjustment, and about **1,377** days at the registered VIF 3.4 (REGISTRATION.md:225). On the realized coin-test bootstrap half-width of 0.0337 at 404 days ("The model-against-a-coin test is somewhat better resolved, at a half-width of / 0.0337", evaluation.md:250-251; test row at evaluation.md:133) the replay window would need about **734** days. No reading of the realized data supports 221.
  - Hygiene, folded in: the floor the code actually enforces is a day count, `clears_power_floor=len(inside) >= cfg.min_trading_days` (NPDExperiment/src/npd/window.py:76) with `min_trading_days=200` (NPDExperiment/src/npd/config.py:80), and Section 0 fires BLOCKED on that count (NPDExperiment/src/npd/section0.py:56-61). 200 days gives 2.0 × 0.185695 / sqrt(200) = **0.02626 > 0.025**, so the code's floor does not equal the registration's floor even on the registration's own arithmetic.
  - The closure names no revised replay date, and the post-anchor marker `_CLOSED_DO_NOT_RUN_HERE` (untracked, excluded via `.git/info/exclude`, dated 2026-09-02, read 2026-09-03T06:30:46Z, UNANCHORED) directs successor work to a new repository, so the registered reopen path has neither a valid trigger nor an owner.
- **Recomputation:** Inputs: null sd 0.185695 (REGISTRATION.md:203-204), t 2.0 (`t_critical=2.0`, NPDExperiment/src/npd/config.py:119), VIF 3.4 (REGISTRATION.md:225), realized model IC sd 0.25159 (n 404), realized coin half-width 0.0337 (evaluation.md:250-251). Method: days = (t × sd / MDE)² × VIF. Results: 220.7 (registered inputs), 750 (registered sd at VIF 3.4), 405 (realized sd, no overlap), 1,377 (realized sd at VIF 3.4), 0.02626 at 200 days. Script `scratchpad/work/agentA/recompute.py`, output `recompute.out` (final block).
- **What would resolve it:** A numbered amendment that either re-bases Section 14's trigger on the realized sd and states the revised replay dates, or withdraws the B.3 schedule explicitly; and a one-line correction aligning `min_trading_days` with the 221-day registered floor. Either current reading (replays fire underpowered in mid 2027, or the schedule has silently lapsed) is a defect; it is filed under Direction A because the closure leaves the registered reopen path without a live trigger.
- **Confidence:** MEDIUM — the arithmetic is HIGH confidence; that the schedule is orphaned rather than merely unrevised is an inference from the closure's silence and the post-anchor marker.
- **Could later commits invalidate this?:** no — no commits after the anchor; a future amendment would resolve it rather than invalidate it.
- **Disclosed by authors?:** no — the closure re-sizes the design but does not connect the new sizing to Section 14, and no document notes the 200-versus-221-day mismatch.

### AUDIT-A-NPDExperiment-4

- **ID:** AUDIT-A-NPDExperiment-4
- **Repository / SHA:** NPDExperiment / `2d3d0aebf977fb2821ec78c25b370c84ec055920`
- **Hypothesis or artifact:** The `low`-reasoning-effort variant named in Amendment 2 as a future registered variant, versus the Closure's "What a powered version would cost"
- **Direction:** A
- **Class:** OVER_CLOSED
- **Severity:** S3 (capped: the authors disclosed the variant elsewhere — see the disclosure field)
- **Label:** READ
- **Claim challenged (verbatim, with file:line):**
  - "Sizing against the measured 0.36339 rather than the registered assumption requires roughly **four times the evaluable days**, landing near **1,700 trading days** of post-cutoff window." / "**No model has one.** The window would have to accumulate from the calendar at about 21 trading days a month." — NPDExperiment/REGISTRATION.md:716-722
  - Against: "The `low` effort variant over a shortened window is recorded here as a natural candidate for a future registered variant, where it can be named in advance rather than chosen in hindsight." — NPDExperiment/REGISTRATION.md:493-496
- **Evidence (figures with n, each with file:line or data path + read time):**
  - The closure's cost section prices exactly one route to a powered result — calendar accumulation to about 1,700 days — and declares it unavailable. It does not mention the variant the registration itself named seven amendments earlier, nor the 3.0622 USD left under the cap ("**Spend.** Measured at **6.9378 USD** against the **10.00 USD** cap. 3.0622 USD / unspent." — NPDExperiment/REGISTRATION.md:789-790), nor what the variant would cost now that Amendment 4's strict schema is in force.
  - Ledger-measured cost of the **70** `low` attempts under the in-force digest (live `ledgers/evidence.jsonl`, read 2026-09-03T06:35:37Z, UNANCHORED): mean **0.03735 USD** per attempt, mean 3,110 reasoning tokens, **53 of 70** attempts stored (76 percent), mean latency 31.5 s. A full 432-day `low` collection therefore projects to about **16.1 USD** at one attempt per day and about **21.3 USD** at the realized 1.32 attempts per stored `low` day; the 365-day version Amendment 2 sized (REGISTRATION.md:488-490) to about **13.6 to 18.0 USD**.
  - The binding blocker is the leftover balance, not the calendar: "The 10 USD is a **leftover balance rather than a dedicated budget**, so the / effective cap is the lower of 10 USD and whatever the account actually has / left." — NPDExperiment/REGISTRATION.md:293-295.
  - Every sentence of the closure carries the effort qualifier: "The gate ran at `minimal` reasoning on 813 of 883 attempts. **A null result is a / null for gpt-5-2025-08-07 at minimal reasoning effort, not for the model at its / best.**" — NPDExperiment/reports/session_a1_b1.md:261-263; same at REGISTRATION.md:483-486. The only in-sample datum on that qualifier — the split of AUDIT-A-NPDExperiment-2 — reads +0.0509 on 51 `low` days against −0.0004 on 353 `minimal` days at the primary horizon: imprecise, but on the hypothesis side.
  - Honest limit on my own claim: the `low` variant would not repair the contrast power at 432 days (the contrast-sd problem of AUDIT-A-NPDExperiment-1 is independent of effort), so its value is confined to the effort qualifier.
- **Recomputation:** Inputs: `cost_usd`, `reasoning_tokens`, `state`, `reasoning_effort`, `prompt_digest` per row of live `ledgers/evidence.jsonl` (n = 883 attempts under the in-force digest); day count 432 (REGISTRATION.md:83). Method: mean over `low` attempts with the in-force digest; multiply by 432, and by 432 × 70/53. Result: 16.13 USD and 21.3 USD. Script `scratchpad/work/agentA/supp.py`, output `supp.out`.
- **What would resolve it:** Add to the closure's cost section the price of the named `low` variant (order 15 to 25 USD on the ledger's own rates) beside the 1,700-day route, and state whether it is declined on cost, on the operator decision recorded at REGISTRATION.md:710, or on the contrast-power argument. Then "No model has one" stops reading as "no achievable path exists".
- **Confidence:** MEDIUM — the omission and the cost are firm; whether the variant is worth running is a judgement the closure is entitled to make, but it did not make it.
- **Could later commits invalidate this?:** no — no commits after the anchor; the untracked 2026-09-02 marker says successor work belongs in a new repository, which is consistent with the variant still being open.
- **Disclosed by authors?:** **yes** — REGISTRATION.md:493-496 names the variant as a future candidate, and REGISTRATION.md:710 states the closure is by operator decision. The authors disclosed it, so this finding is READ and capped at S3. What is not disclosed is the *cost*, and the disclosure sits in Amendment 2 rather than in the closure section that prices what a powered version would cost, so a reader of the closure alone is told no path exists.

---

## What Agent A checked and found sound

Where the thesis did not hold, with the arithmetic where I ran it.

1. **The B.2 computation is exactly reproducible.** From the stored rankings and sealed returns I reproduce every figure in `reports/stage_b2/evaluation.md`: model +0.0061 (n 404), mom_12_1 +0.0222, logistic −0.0058, sign_last −0.0255 (:59-62); contrast −0.0161, interval −0.0673 to +0.0351, bootstrap SE 0.02562, daily sd 0.36339 (:78-82); effective n 201.2 and MDC 0.0512 (:92-93); coin interval −0.0276 to +0.0397 (:133); secondary model −0.0203, contrast −0.0300 [−0.0677, +0.0077], MDC 0.0377 (n 412) (:160-173). The moving-block bootstrap (evaluator.py:160-190) reproduces with the same seeds. `recompute.out`.
2. **The "does not beat coin" row is supported at the registered floor.** The Section 9.1 floor is a one-sample test against zero with the null sd and no overlap adjustment (REGISTRATION.md:208-212). The registered within-day permutation null (REGISTRATION.md:186; evaluation.md:101-113) is exactly that test: null sd 0.00926 on the mean (0.185695/sqrt(404) = 0.00924), resolution at t 2.0 of 0.0185, inside the 0.025 floor; observed +0.0061 gives p 0.5174. The block-bootstrap coin interval is wider (half-width 0.0337) because the realized model IC sd is 0.2516, and the no-overlap one-sample test on the realized sd gives MDE 0.0250 (t = +0.49). All three readings agree the model did not beat a coin. I therefore do not file the "confirms the council negative ... Closed." label (evaluation.md:127) as a finding: the authors disclose the power tension in the same document ("underpowered unresolved, not a tight null", evaluation.md:139-141; "closed by operator decision, not by evidence", REGISTRATION.md:709-710). What is underpowered is the contrast against momentum, which the authors say plainly (evaluation.md:246-248).
3. **The 1,700-day sizing is arithmetically right on its own inputs.** (0.0512/0.025)² × 404 = 1,694; (2 × 0.36339/0.033)² × 3.4 = 1,649. "Roughly four times the evaluable days" (REGISTRATION.md:717) is (0.0512/0.025)² = 4.19. "No model has one" is true for any frontier model with a post-2020 cutoff (a 2021-09 cutoff yields about 1,190 trading days to 2026-07-24); I know of no served frontier snapshot with a 2019 cutoff, so I do not file an alternative-source finding.
4. **The window-halves diagnostic is inside noise, as stated.** With sd 0.19 and VIF 3.4 the SE per half is 0.0247 and on the difference 0.0349 (evaluation.md:255-258); 0.0124/0.0349 = 0.36 SE. On the realized sd 0.2516 the difference SE is 0.046 and the ratio 0.27. Sound.
5. **Section 0 coverage.** 415 stored of 432 eligible = 96.06 percent (collection.json:8-14; collection.md:30-43); GO at the 90 percent bar; `model_failed` correctly in the denominator (section0.py:34-44). Sound.
6. **Spend arithmetic.** Evidence ledger and spend ledger both sum to 6.9377835 USD (920 gate rows, 2 calibration rows), matching 6.9378 (collection.md:49); remaining 3.0622. Amendment 5's undercount is disclosed and the superseded rows are kept. Sound.
7. **Best-baseline designation (ADR-010) is conservative in the stated direction.** The model would have looked better against either other baseline: contrast versus logistic +0.0118 [−0.0397, +0.0634]; versus sign_last +0.0316 [+0.0011, +0.0621] (UNANCHORED recomputation, block bootstrap, `recompute.out`, n 404). The sign_last contrast excludes zero, but sign_last carries a negative IC (−0.0255) and the registration fixes the contrast against the best baseline (REGISTRATION.md:181-182), so I do not file the sign_last result as a better-resolved endpoint: beating a below-coin baseline is not the hypothesis. The logistic contrast — the one most directly matched to "identical features" — is no better resolved than the momentum contrast (MDC 0.0516).
8. **Reopen conditions with triggers already met: none inside this repository.** Every dated entry is 2026-08-25; the only later artefact is the untracked closure marker of 2026-09-02, which lifts no blocker. The one stale trigger is AUDIT-A-NPDExperiment-3.
9. **Anti-contamination design.** Cutoff verified from the vendor page with the verbatim string (REGISTRATION.md:58-61), one-month guard band, per-call remapped labels, ticker-label collision fix on 52 of 432 days (session_a1_b1.md:134-138), negative control +0.0001 inside the 0.02 tolerance (evaluation.md:36-42). Sound.
10. **Amendment 0 ordering and the sealed-store single reader.** The evaluator refuses on an empty Section 13 (evaluator.py:73-78), mutation 6 proves the refusal (mutations.md:76-89), and the guard test restricts the sealed path to the evaluator (build.md:85-90). Sound.
11. **Noted for completeness, outside my direction (not filed as a finding).** Amendment 4 projected first-attempt compliance of 88 percent from 8 held-out days and "an expected failure rate near zero" over four `minimal` attempts (REGISTRATION.md:573-586). The ledger shows 362 stored of 813 `minimal` attempts under the strict schema (45 percent of attempts), 17 days in `model_failed`, and measured spend 6.94 USD against the 2.86 USD projection (REGISTRATION.md:579; progress.md:214-217 presents the projection-to-measurement move as a success). Coverage still fired GO, so no verdict rests on it. This is a Direction B item; it belongs to the B pass, not to mine.

## Dropped at consolidation

Nothing was dropped for want of a locatable quote, a figure or an n: all four draft findings carried a verbatim quote with file:line, figures, and their n, and all quotes were re-verified against SNAP/NPDExperiment during consolidation. Merges and demotions were as follows.

- **No duplicate findings to merge.** NPDExperiment produced a single draft part ("all"), so no two drafts challenged the same claim or attacked the same closure on the same grounds. AUDIT-A-NPDExperiment-2 and -4 both touch the `minimal`-effort qualifier but attack different closures on different grounds (a registered descriptive never delivered against evaluation.md's completeness claim, versus the closure's cost section omitting a named variant), so they are kept separate and cross-referenced rather than merged.
- **Demoted and folded, not filed separately:** the S4 hygiene mismatch between the code's enforced floor (`min_trading_days=200`, config.py:80, giving MDE 0.02626) and the registration's 221-day floor (giving 0.025). It is evidence inside AUDIT-A-NPDExperiment-3 rather than its own finding, because on its own it changes nothing: the realized window of 432 days clears both.
- **Not filed (out of direction):** the Amendment 4 compliance-and-cost projection versus its realized figures (item 11 above). It is a Direction B claim — the document claiming more than it measured — and no verdict rests on it, so filing it under Direction A would be padding.
- **Not filed (evidence points the other way):** the model-minus-sign_last contrast of +0.0316 [+0.0011, +0.0621], which excludes zero. It is not a suppressed positive: sign_last carries a negative IC and the registration fixes the contrast against the *best* baseline before any output existed (REGISTRATION.md:181-182). Reporting it as an under-closed positive would be exactly the hindsight move the registration was built to prevent.
- **Not filed (adequately resolved and disclosed):** the "does not beat coin" verdict label itself (evaluation.md:127). Three independent readings agree, and the authors disclose the power tension in the same document; see item 2 above.

## Live-repo access log

Live repository: `/home/kiros-li/Documents/GitHub/NPDExperiment`. Read-only access only: `git status --porcelain`, `git rev-parse HEAD`, `git log`, `git branch -a`, `git status --porcelain --ignored`, `ls`, `find`, `cat` of `.gitignore` and of the untracked marker `_CLOSED_DO_NOT_RUN_HERE`, SQLite opens of `var/npd.db`, `var/npd_sealed.db` and `var/npd_fit.db` with `mode=ro&immutable=1`, and plain reads of `ledgers/evidence.jsonl` and `ledgers/spend.jsonl`. `.env` was not opened. No script was executed inside the repository; all recomputation ran from the work directory against read-only inputs.

BEFORE (2026-09-03T06:30:18Z), `git -C /home/kiros-li/Documents/GitHub/NPDExperiment status --porcelain`:

```
(empty output)
```

AFTER (2026-09-03T06:35:37Z), same command:

```
(empty output)
```

HEAD at both times: `2d3d0aebf977fb2821ec78c25b370c84ec055920`, equal to the anchored SHA. Reported loudly per the rules: `git status --porcelain --ignored` lists `!! _CLOSED_DO_NOT_RUN_HERE`, an untracked file dated 2026-09-02 excluded through `.git/info/exclude` (its own text says so). It is pre-existing and not mine. Other ignored entries are `.env`, caches, `.venv/`, `ledgers/`, `var/`, `__pycache__/`. No modification to the repository was made or observed.
