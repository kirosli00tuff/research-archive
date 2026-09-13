# Agent B positives ledger — NPDExperiment

Repository: **NPDExperiment**, anchored SHA `2d3d0aebf977fb2821ec78c25b370c84ec055920` (main, 2026-08-25).
Merged and de-duplicated from `_drafts/NPDExperiment/all.positives.md`; finding references are updated
to the consolidated IDs in `findings/agentB/NPDExperiment.md`.

Factual, not advocacy. Every entry records a registered hypothesis, sub-test, shipped artifact, open
item or thresholded negative as the repository states it, with the deciding figures and their n, the
bar and its registration date, any amendment touching that bar, the corrections the repository
applied, and the framing carried in the top-level document / the reports / the shipped page. Entries
appear whether or not the audit found fault with them; where it did, the row names the finding rather
than restating it.

**Sources.** Everything below is cited from `SNAP/NPDExperiment/` at the anchored SHA. Commit-level
timestamps and the unanchored ledger/store figures are carried from the draft, which obtained them by
read-only live access on 2026-09-04 between 05:20 and 05:40 UTC; such figures are marked *(live,
unanchored)*. This ledger and the consolidation pass touched no live repository.

**Repository-level facts that condition every row:**

- **There is no positive result in this repository.** Verdict row three fired — "does not beat coin"
  (reports/stage_b2/evaluation.md:123-127; REGISTRATION.md:274) — and the conditional phase C.1 was
  never authorized (REGISTRATION.md:658-659; progress.md:138). The positives below are measurement
  verdicts, build verifications, shipped artifacts and disciplines, not findings about the model.
- **There is no README.md.** `CLAUDE.md` is the top-level operating document, `progress.md` the
  running narrative, `reports/session_record.html` the shipped page. The "framing" column uses those.
- **Every registration date is 2026-08-25.** REGISTRATION.md:3 "Written 2026-08-25, before the first
  call."; ADR-001 through ADR-014 each read "Accepted, 2026-08-25" (DECISIONS.md:8, :28, :41, :56,
  :74, :104, :120, :143, :168, :187, :210, :233, :251, :270), with ADR-010/011 marked "at B.2" and
  ADR-012/013/014 "at Z.1". The whole project — scaffold, registration, collection, evaluation and
  closure — ran inside one day; eleven commits, all 2026-08-25 *(live, unanchored)*.
- **No amendment ever moved a statistical bar.** Amendments 1 through 5 change the call procedure
  (temperature, reasoning effort, the retry ladder, the output schema, ledger accounting). Amendments
  6 and 7 are post-read and carry no force. The coverage floors, the power floor, the t-critical, the
  resample counts, the realistic effect band and the Section 10 verdict table are unchanged from
  their first commit *(live, unanchored: `config.py` dates from `64b7d41` 09:39, last touched at
  `250bc8f` 10:35 for Amendment 4; the only registration change at the B.2 commit `2c6d683` is
  Section 13)*. This is the strongest single fact in the repository's favour and the audit confirms
  it independently.

---

## Part 1. The registered hypothesis, its sub-tests and its verdicts

### 1. The primary hypothesis and the fired verdict row

| field | content |
|---|---|
| Claim as stated | "**Given anonymized per-name numeric feature blocks, a frontier LLM ranks next-window cross-sectional returns better than cheap mechanical baselines.**" — REGISTRATION.md:31-32. Fired: "\| does **not** beat coin \| the replication confirms the council negative under frontier capability and sane formulation. Closed. \|" — REGISTRATION.md:274, printed at reports/stage_b2/evaluation.md:123-127 |
| Kind | thresholded negative (the registered row that fired) |
| Deciding figures (n) | model mean daily rank IC **+0.0061**, interval **−0.0276 to +0.0397**, "beats a coin: **False**" — evaluation.md:59, :133, :191-193. n = **404 evaluable days**, 6 dropped for a missing realized return, out of 415 stored, 30 names per day — evaluation.md:51-53 |
| Bar + registration date | "beats coin" is operationalized as the bootstrap interval's lower bound above zero: `beats_coin=model_iv.low > 0.0` — src/npd/eval/evaluator.py:546. Verdict table "Written now, before any output exists." — REGISTRATION.md:266-268, registered 2026-08-25 |
| Amendments touching the bar | none. Amendment 2 (calibration data only, no gate data and no outcome data) narrows the *scope* of any verdict to "gpt-5-2025-08-07 **at minimal reasoning effort**" (REGISTRATION.md:483-486) without changing the bar. Amendments 6 and 7 are POST-READ and change nothing (REGISTRATION.md:624-635, :661-674) |
| Corrections applied | day-clustered moving-block bootstrap, block 10 = twice the primary horizon, 10,000 resamples, two-sided at t 2.0 (REGISTRATION.md:144-145, :181-186; config.py:117-119); overlap variance inflation 3.4 registered in advance (REGISTRATION.md:225); single pre-registered contrast so no family correction (REGISTRATION.md:188-190) |
| Corrections NOT applied | the verdict sentence's "under frontier capability" is not reconciled with the realized minimal-effort configuration (AUDIT-B-NPDExperiment-9); the sample is conditioned on parse success, which is day-dependent (-10) |
| Framing | CLAUDE.md:3-6 states the premise ("frontier capability and sane formulation"). progress.md:136-138 "**Verdict row fired: does not beat coin.** … **C.1 is not authorized.**". Closure: "Two serious attempts have produced zero positives." (REGISTRATION.md:680-681). The shipped page predates B.2 and carries no verdict (session_record.html:204 "Evaluated / 0") |

### 2. The primary contrast (Task 3)

| field | content |
|---|---|
| Claim as stated | "\| **primary contrast** \| **-0.0161** \| … \| interval \| -0.0673 to +0.0351 \| … \| excludes zero \| **False** \|" — reports/stage_b2/evaluation.md:76-82 |
| Kind | thresholded negative |
| Deciding figures (n) | contrast −0.0161; bootstrap se 0.02562; daily contrast sd 0.36339; effective sample **201.2** independent-equivalent days; realized MDE **0.0512** — evaluation.md:78-82, :90-93. n = 404 days × 30 names. Per-series means: model +0.0061, `mom_12_1` +0.0222, `logistic` −0.0058, `sign_last` −0.0255 — evaluation.md:57-62 |
| Bar + registration date | "Mean daily rank IC of the model minus mean daily rank IC of the best baseline", two-sided at t 2.0, `beats_best_baseline=contrast_iv.low > 0.0` — REGISTRATION.md:181-186; evaluator.py:547. Registered 2026-08-25 |
| Amendments touching the bar | none |
| Corrections applied | best baseline designated after the fact as the *hardest* of the three (entry 9); realized power printed beside the projection before the verdict is read (entry 10); the report states the achieved interval rather than only its sign, as Section 9.3 required (REGISTRATION.md:260-262) |
| Corrections NOT applied | the registered by-effort split was not printed (entry 13) |
| Framing | evaluation.md:96-97 "The result is read against the power that existed, not the power that was hoped for." progress.md:145-151. Closure repeats the three numbers (REGISTRATION.md:689-691) |

### 3. The within-day permutation null (Task 4)

| field | content |
|---|---|
| Claim as stated | "\| observed model mean daily rank IC \| **+0.0061** \| … \| **two-sided p** \| **0.5174** \|" — reports/stage_b2/evaluation.md:107-113 |
| Kind | thresholded negative |
| Deciding figures (n) | null mean −0.0002, null sd 0.00926, null 2.5-97.5 percentile −0.0184 to +0.0177, p 0.5174 — evaluation.md:110-113. n = 10,000 resamples over 404 days |
| Bar + registration date | "Within-day permutation null at 10,000." — REGISTRATION.md:186; `permutation_resamples=10_000` config.py:118, registered 2026-08-25 |
| Amendments touching the bar | none |
| Corrections applied | drawn independently of the Task 2 gate "so the two questions do not share a sample" (evaluation.md:103-105); the null sd 0.00926 equals 0.185695/sqrt(404), the correct null for independent daily shuffles — the audit checked this test for anti-conservatism under the five-session overlap and reports it **valid** |
| Framing | reported inside Task 4 with no interpretive gloss; carried into the closure as "permutation p **0.5174**" (REGISTRATION.md:691; progress.md:36) |

### 4. The registered secondary horizon (one session)

| field | content |
|---|---|
| Claim as stated | "\| model, SECONDARY \| -0.0203 \| … \| contrast \| -0.0300 \| interval \| -0.0677 to +0.0077 \| excludes zero \| False \|" — reports/stage_b2/evaluation.md:158-172 |
| Kind | thresholded negative (registered secondary, correctly kept subordinate) |
| Deciding figures (n) | n = **412 evaluable days**; best secondary baseline `logistic` +0.0097; realized MDE 0.0377 — evaluation.md:161-173 |
| Bar + registration date | "**Secondary.** Next-session return." REGISTRATION.md:143; `secondary_horizon_sessions=1` config.py:86. Registered 2026-08-25 |
| Amendments touching the bar | Amendment 7 would have added 10- and 20-session horizons; **void, not applied** (REGISTRATION.md:661-674; ADR-013 DECISIONS.md:249-266). Data existed: yes — drafted after the read, which is the stated reason it is void |
| Corrections applied | the secondary is better powered (0.014 to 0.025, ADR-007 DECISIONS.md:130-133) and was **not** promoted after the result was seen — the registration names that move in advance as the one it exists to prevent (REGISTRATION.md:256-258) |
| Framing | evaluation.md:153-154 "**Everything in this section is subordinate. None of it changed the verdict above and none of it may be read as changing it.**" The secondary is absent from the closure and from progress.md's Z.1 summary |

### 5. Task 2, the pipeline validity gate (registered negative control, Section 7 clause 3)

| field | content |
|---|---|
| Claim as stated | "**Gate verdict: PASS.** The shuffled mean sits inside the registered tolerance of zero. The scorer, the join, and the label mapping behave as a valid pipeline must under randomization" — reports/stage_b2/evaluation.md:42-45 |
| Kind | positive (a registered control that fired PASS) — **qualified**: the audit shows the statistic has no power against the defects it names |
| Deciding figures (n) | shuffled mean daily rank IC **+0.0001**, Monte-Carlo 95 % interval −0.0001 to +0.0003, null sd 0.00925, registered tolerance 0.02 — evaluation.md:36-40. n = 10,000 within-day shuffles over 404 days |
| Bar + registration date | "Shuffle stored rankings within day. The rank IC must collapse toward zero. A non-zero result stops everything." — REGISTRATION.md:173-175 (Section 7, clause 3), registered 2026-08-25. Tolerance coded as `CONTROL_TOLERANCE = 0.02` — evaluator.py:551-553; gate at evaluator.py:627 |
| Amendments touching the bar | none. The tolerance predates collection *(live, unanchored: `assert_control_collapsed(..., tolerance: float = 0.02)` present at `943ba05`, 10:06)* |
| Corrections applied | the report itself narrows the claim: "**This detects pipeline defects, not model contamination.** … It is not a contamination clearance and a later reader must not read it as one." — evaluation.md:29-32 |
| Corrections NOT applied | the statistic has expectation zero for every possible input, and the audit demonstrates that a pipeline joined to pure noise and a scrambled label mapping both PASS (AUDIT-B-NPDExperiment-3) |
| Framing | counted as one of three contamination defenses (REGISTRATION.md:167-175); progress.md:142 "pipeline validity gate, shuffled mean +0.0001, inside the 0.02 tolerance. PASS" |

### 6. Section 0 coverage verdict: GO

| field | content |
|---|---|
| Claim as stated | "**Section 0 verdict: GO.** 96.1% of eligible days carry a stored, parseable ranking, at or above the 90% bar." — reports/stage_b1/collection.md:41-43 |
| Kind | positive (measurement verdict; it authorized B.2) |
| Deciding figures (n) | 415 `stored`, 17 `model_failed`, 0 `no_data`, 0 `excluded_pre_cutoff`, 0 `source_failed`, total **432** — collection.md:19-26; coverage 415/432 = **96.1 %** (0.9606, collection.json). n = 432 eligible days |
| Bar + registration date | "\| GO \| at least 90 percent of eligible days carry a stored, parseable ranking \|" — REGISTRATION.md:16; `coverage_go_floor=0.90` config.py:115; enforced at src/npd/section0.py:62-67. Registered 2026-08-25, "Committed before any call goes out. Coverage decides this verdict and nothing else does." REGISTRATION.md:11-12 |
| Amendments touching the bar | **none touched the bar itself.** Amendment 4 (raised 29 gate days into B.1; data existing = 48 free-form attempts plus an 8-day strict-schema pilot, no outcome data) changed the *procedure* that produced coverage and forced a full recollection (REGISTRATION.md:588-603) |
| Corrections applied | `excluded_pre_cutoff` excluded from the denominator by rule, `model_failed` **kept in** it — "a day the model could not answer is a day the sample does not have" (REGISTRATION.md:20-23; section0.py:34-44). The verdict is explicitly fired on coverage alone with no output-to-outcome statistic (collection.md:100-105) |
| Corrections NOT applied | the free-form arm's own realized coverage is never stated, so the "heading for BLOCKED" claim is unsupported (AUDIT-B-NPDExperiment-5); the 17 `model_failed` days are treated as operational health rather than a selected subset (-10) |
| Framing | progress.md:190-191 "**Section 0 verdict: GO.** 415 of 432 eligible days … Coverage 96.1 percent against a 90 percent bar." Shipped page: "Section 0 verdict / **GO** / fired on coverage alone" and "Coverage / 96.1% / 415 of 432 eligible days" — session_record.html:199-200 |

### 7. The registered power floor, and the authorization to collect

| field | content |
|---|---|
| Claim as stated | "    MDE = 2.0 * 0.185695 / sqrt(432) = 0.01787" / "**0.01787 is below 0.025. The window clears the registered power floor.** Collection is authorized." — REGISTRATION.md:212-215 |
| Kind | positive (the gate that authorized spending) — **qualified**, see below |
| Deciding figures (n) | null daily rank IC sd at 30 names = 1/sqrt(29) = **0.185695** (REGISTRATION.md:203-204; src/npd/power.py:34-42); n = **432 trading days** (REGISTRATION.md:83); floor MDE **0.01787** against a floor of 0.025 — REGISTRATION.md:212, reproduced at reports/stage_b0/build.md:97 |
| Bar + registration date | "detectable IC 0.025 at 30 names … a one-sample test of the model's own daily rank IC against zero, at t 2.0, with no overlap adjustment" — REGISTRATION.md:208-210; `registered_floor_mde` power.py:129-131. Registered 2026-08-25, before any spend ("These numbers are produced before a cent is spent" REGISTRATION.md:200-201) |
| Amendments touching the bar | none |
| Corrections applied | the registration discloses in the same breath that the floor carries no overlap adjustment (REGISTRATION.md:208-210) and registers the contrast's weaker power beside it (Section 9.2-9.3, ADR-007 DECISIONS.md:118-139) |
| Corrections NOT applied | the realized one-sample half-width was 0.0337 (evaluation.md:250-251), 35 % above the 0.025 floor, and this is nowhere stated; the Section 14 replay figure of 221 days inherits the same no-overlap arithmetic (AUDIT-B-NPDExperiment-6). The coded BLOCKED condition is a 200-day count, not the stated MDE (`min_trading_days=200` config.py:80; section0.py:58-61; -17) |
| Framing | progress.md:317-318 "**Power.** Registered floor MDE 0.01787 against a floor of 0.025, so the window is authorized." Shipped page: "Derived window / **432** / trading days, floor 200" — session_record.html:202 |

### 8. The registered power *limitation* (Section 9.3 / ADR-007)

| field | content |
|---|---|
| Claim as stated | "The primary contrast detects effects in the **upper half** of the realistic band and is **underpowered for the lower half**." — REGISTRATION.md:251-252; ADR-007 "Recorded before collection rather than discovered after." DECISIONS.md:136-137 |
| Kind | positive (a disclosed limitation registered in advance, at a cost) |
| Deciding figures (n) | VIF = 1 + 2·Σ(1−k/5)² = **3.4**, taking 427 evaluable days to **125.6** effective (REGISTRATION.md:225-227; power.py:45-58, :61-63); grid 0.0469 / 0.0392 / 0.0331 / 0.0257 at correlations 0.0 / 0.3 / 0.5 / 0.7 (REGISTRATION.md:231-236); realistic band 0.01 to 0.05 (REGISTRATION.md:247; `realistic_effect_band=(0.01, 0.05)` config.py:120) |
| Bar + registration date | registered 2026-08-25 as a limitation rather than repaired by swapping the primary (REGISTRATION.md:256-258) |
| Amendments touching the bar | none |
| Corrections applied | the better-powered secondary was **not** promoted (entry 4); ADR-007's cost is paid explicitly |
| Corrections NOT applied | the grid derives every cell from the *null* per-series sd (power.py:107-116), an assumption the realized data break in the same direction for all four series; the closure nonetheless credits ADR-007 with having registered the failure mode that materialized (AUDIT-B-NPDExperiment-2) |
| Framing | reports/session_a1_b1.md:63-69; build.md:107 "At the middle cell the primary contrast covers the upper part of the registered band 0.01 to 0.05, from 0.0331." |

### 9. ADR-010, the best baseline designated after the fact

| field | content |
|---|---|
| Claim as stated | "Choosing after the fact is **conservative in this direction and only this direction.** It picks the hardest of the three for the model to clear, so it raises the bar rather than lowering it." — DECISIONS.md:198-200 |
| Kind | positive (a methodological claim the audit **confirmed**) |
| Deciding figures (n) | `mom_12_1` +0.0222 beat `logistic` −0.0058 and `sign_last` −0.0255 on n = 404 days — DECISIONS.md:193-196; evaluation.md:57-62 |
| Bar + registration date | the registration names three baselines and defines the contrast against "the best baseline" without naming which (REGISTRATION.md:149-158, :181-182), registered 2026-08-25; ADR-010 accepted 2026-08-25 **at B.2**, i.e. with the outcome visible (DECISIONS.md:187) |
| Amendments touching the bar | none |
| Corrections applied | the ADR states the falsifiable check ("A reader checking this can confirm it from the per-baseline table") and declines to offer an alternative specification (DECISIONS.md:201-206) |
| Audit result | **confirmed and costed.** Recomputed: the model beats `sign_last` by +0.0316 with an interval of +0.0009 to +0.0623 — the only interval in the repository excluding zero — and the chosen baseline also yields the largest realized MDE (0.0512 against 0.0307). Selecting the hardest baseline turned a nominal positive into a null |
| Framing | evaluation.md:64-68 "Selecting it this way is **conservative** … It raises the bar, it never lowers it." No document claims credit for the +0.0316 that was given up |

### 10. ADR-011, the realized power read before the null ("underpowered unresolved")

| field | content |
|---|---|
| Claim as stated | "This is an **underpowered unresolved**, not a tight null. The realized minimum detectable contrast is 0.0512, so effects below that magnitude were never distinguishable from zero by this design." — reports/stage_b2/evaluation.md:139-141; ADR-011 DECISIONS.md:220-225 |
| Kind | positive (an honest self-limitation, printed before the verdict row is reached) — **qualified**: its stated *cause* is contradicted |
| Deciding figures (n) | realized MDE **0.0512** against a registered projection of 0.026 to 0.047 (evaluation.md:93-94); realized daily contrast sd **0.36339** against a registered maximum of 0.2626 (evaluation.md:82, :224); band table "contrast effects from 0.01 to 0.05 — **not detectable**" (evaluation.md:241-244). n = 404 days |
| Bar + registration date | ADR-011 accepted 2026-08-25 at B.2; the requirement to state the achieved interval rather than only its sign was registered in advance at REGISTRATION.md:260-262 |
| Amendments touching the bar | none |
| Corrections applied | the realized number is printed beside the projection and before the verdict row (DECISIONS.md:217-218); the appendix is explicitly labelled "arithmetic on the numbers already printed above … adds no test" (evaluation.md:214-215) |
| Corrections NOT applied | the attributed cause — "a strong negative correlation between the model and momentum daily ICs" (REGISTRATION.md:699-702) — is contradicted by the data; the overshoot comes from per-series dispersion, and the realized correlation moved the number favourably (AUDIT-B-NPDExperiment-1, -2) |
| Framing | carried verbatim into progress.md:155-161 and into the closure (REGISTRATION.md:693-705). It is the repository's own headline qualifier and it travels with every restatement of the result |

### 11. ADR-014, the dormant observation ("the model leaned against momentum")

| field | content |
|---|---|
| Claim as stated | "**The observation.** Across the evaluable window the model daily rank IC and the momentum daily rank IC were strongly negatively correlated. The model was not producing noise around momentum. It was leaning systematically against it." — REGISTRATION.md:727-729 (also DECISIONS.md:274-276; progress.md:70-72; evaluation.md:229-233) |
| Kind | recorded as a **dormant named observation, explicitly not a finding** — the audit grades the underlying figure unsupported |
| Deciding figures (n) | the only figure offered is the inference "The realized daily contrast standard deviation of 0.36339 sits at 98 percent of the theoretical maximum of 0.3714" — REGISTRATION.md:731-733; evaluation.md:223-229. **No correlation figure exists anywhere in the snapshot**: `run_b2` computes and stores none (evaluator.py:526-528, :556-573; :575-722) and `write_report` prints none |
| Bar + registration date | none. "No registered test asks about the correlation between the model and a baseline." — REGISTRATION.md:737-738. ADR-014 accepted 2026-08-25 at Z.1, with the outcome fully visible |
| Amendments touching the bar | none. It is placed in the shape Section 16 clause 4 reserved for the AiTrader `consolidat` cell (REGISTRATION.md:433-438) |
| Corrections applied | four containment sentences: "This is not a finding." / "It surfaced as a power diagnostic" / "It may only be promoted by a future test that names it in advance." / "Nothing further is claimed." (REGISTRATION.md:737-742); ADR-014 adds "Claiming it now is what would make that test worthless." (DECISIONS.md:288-289) |
| Corrections NOT applied | the sign and magnitude were never measured; measured on the same 404 days the correlation is **+0.1182**, inside the registered 0.0-to-0.7 grid, and 0.36339 is 66.6 % of the true attainable maximum (AUDIT-B-NPDExperiment-1) *(live, unanchored)* |
| Framing | the containment is exemplary and the underlying number is wrong. The closure heads it "Dormant observation. The model leaned against momentum" (REGISTRATION.md:723) and progress.md:68-73 repeats it under the same heading — the form most likely to be retold as a result |

### 12. Descriptive: window halves (the residual-knowledge diagnostic)

| field | content |
|---|---|
| Claim as stated | "**The observed difference is about one third of one standard error.** It is not a decay signal. It is recorded because the registration asked for the diagnostic, and it flags nothing." — reports/stage_b2/evaluation.md:258-260 |
| Kind | descriptive, reported and correctly not promoted |
| Deciding figures (n) | first half n = 202 days, +0.0123; second half n = 202 days, −0.0001; difference +0.0124 against a standard error near 0.035 — evaluation.md:181-185, :255-258 |
| Bar + registration date | no bar. Registered as a diagnostic: "Residual knowledge just past a cutoff would show as early-window strength decaying later. **This is a diagnostic and not a verdict input.** A difference here is a flag for a future registered test, never a finding." — evaluation.md:177-179 |
| Amendments touching the bar | none |
| Corrections applied | the standard error is computed with the registered overlap inflation of 3.4 rather than naively (evaluation.md:256-258) |
| Framing | inside Task 5, under the subordination banner (evaluation.md:153-154). Absent from progress.md and from the closure |

### 13. Descriptive: the outcome split by realized reasoning effort — REGISTERED AND NOT PRODUCED

| field | content |
|---|---|
| Claim as stated | "The realized effort is stored per day for exactly this reason, and B.2 reports the outcome split by realized effort alongside the primary contrast." — REGISTRATION.md:534-535 |
| Kind | **open** (a registered B.2 deliverable that does not exist at the anchor) |
| Deciding figures (n) | **not located in the snapshot.** `reports/stage_b2/` mentions effort only at evaluation.md:205-206 (the Amendment-2 qualifier); `B2Result` carries no effort field (evaluator.py:556-573); `write_report` emits secondary horizon, window halves and model-versus-coin under Task 5 and nothing else. The realized split, recomputed from the live ledger, is `minimal` n = 353 mean −0.0004 versus `low` n = 51 mean +0.0509 *(live, unanchored; AUDIT-B-NPDExperiment-7)* |
| Bar + registration date | Amendment 3, 2026-08-25, raised 14 gate calls into B.1 (data existing: 14 attempts, no outcomes). The split is registered as descriptive and explicitly barred from becoming a verdict under Clause 1 (REGISTRATION.md:536) |
| Amendments touching the bar | Amendment 4 superseded Amendment 3's ladder but not its reporting commitment (REGISTRATION.md:562-564) |
| Corrections applied | the confound itself is disclosed plainly in advance: "Days that needed `low` are days where `minimal` could not hold the format. If that difficulty correlates with anything about the panel, the sample mixes two configurations in a way that is not random." — REGISTRATION.md:531-534 |
| Corrections NOT applied | the split was never printed and no document records the omission; the same report asserts scope completeness at evaluation.md:199-200 (AUDIT-B-NPDExperiment-7) |
| Framing | carried forward as a firm commitment in both shipped documents: reports/session_a1_b1.md:268-270 and session_record.html:434 "B.2 reports the split descriptively, and under Clause 1 it never becomes a verdict." |

---

## Part 2. Shipped build and verification artifacts

Each row is a claim the repository ships as verified. Every figure is located in the snapshot unless
marked. None of these is a result about the model; they are the substrate the result stands on.

| # | claim as stated | kind | deciding figures (n) | file:line | bar + registration date | amendments touching the bar | corrections applied | framing |
|---|---|---|---|---|---|---|---|---|
| 14 | "The verified knowledge cutoff for `gpt-5-2025-08-07` is **2024-09-30**" | positive (gating measurement) | one served page, verbatim string `Sep 30, 2024 knowledge cutoff`, retrieved 2026-08-25, reached by 301 from platform.openai.com (n = 1 source) | REGISTRATION.md:56-65; session_a1_b1.md:18-24; config.py:75-77 | ADR-001, gate on cutoff not leaderboard, 2026-08-25 (DECISIONS.md:6-24) | none | the carried chat estimate of 2024-05-31 / 515 days is discarded and named wrong (REGISTRATION.md:70-71) | progress.md:302-311 "**The carried estimate was wrong.**"; shipped page's opening claim (session_record.html:218-222) |
| 15 | Window 2024-10-31 through 2026-07-24, **432 trading days**, clears the registered minimum of 200 | positive | 432 days from the source store's own `trading_calendar`; guard band one calendar month; evaluable 427 at h=5 and 431 at h=1 | REGISTRATION.md:77-93; build.md:94-95 | `min_trading_days=200`, config.py:80, registered 2026-08-25 | none | the calendar is the exchange calendar, "not the dates any one symbol happened to trade" (REGISTRATION.md:87-88) | session_record.html:202; progress.md:313-315 |
| 16 | "The port is verified rather than asserted." 55 formations rebuilt from bars, all matching the source | positive | **55 reproduced, 55 verified, 0 failures**, 500 members each, symbol set *and* rank order, 2022-01-03 to 2026-07-01 | build.md:22-30; progress.md:272-274; session_a1_b1.md:100-104 | no registered bar; the criterion is stated as exact ("A single differing symbol or rank fails the check", build.md:24) | none | the machinery was copied, never imported across repositories (session_a1_b1.md:96-97) | progress.md:272-274; CLAUDE.md:54-55 forbids importing from HFExperiment |
| 17 | Source integrity: two read-only paths, `news_experiment.db` never opened | positive | `backtest/universe.py` sha256 identical before, after and at report time (`8188eea0…`); bar store opened through a SQLite immutable read-only URI; 15,474,106 daily bars across 18,474 symbols | build.md:5-20 | CLAUDE.md:48-53 names the only two permitted source paths | none | "a write is impossible at the driver level rather than by convention" (build.md:14); the guard is the only place `news_experiment` appears in source (session_a1_b1.md:87-88) | progress.md:269-271 |
| 18 | Panel and baseline completion | positive | 432 of 432 window days drew a full 30-name panel (100 % every month); `sign_last`, `mom_12_1`, `logistic` each ranked 432 days; 308,610 feature rows; 9 features per name | build.md:32-73 | ADR-009, eligibility decided by data availability before the draw, 2026-08-25 (DECISIONS.md:166-183) | none | eligibility "never consults an outcome, so it cannot leak", checked before the seeded draw, and no short panel is ever sent (DECISIONS.md:177-183) | progress.md:276-280 |
| 19 | Logistic baseline fitted once and frozen | shipped | **21,322 rows across 711 days**, 2022-01-03 to 2024-10-30, coefficient digest `fe6f6006…` | build.md:75-77; progress.md:279-280 | Section 6: "Fit once on data strictly before the window start, then frozen. Never refit inside the window." REGISTRATION.md:156-163, registered 2026-08-25 | none | a refit inside the window fails `tests/test_guards.py` (REGISTRATION.md:162-163) | session_a1_b1.md:115-116 |
| 20 | The seal: forward returns split by date, one permitted reader | positive (structural control) | two stores, `var/npd_fit.db` and `var/npd_sealed.db`; guard test walks every source file; sealed store read **one time by one module** at B.2 | ADR-004 DECISIONS.md:54-70; ADR-008 DECISIONS.md:141-164; build.md:81-90; evaluator.py:81-93 | registered 2026-08-25; "A convention that says 'do not look' is not a control." DECISIONS.md:58 | none | "Breaking the seal requires editing a guard test, which shows up in a diff." (DECISIONS.md:67-68). Confirmed operationally: sealed-store mtime unchanged from the B.0 build through B.2 and closure, and `read_sealed_returns` has exactly one caller *(live, unanchored)* | progress.md:168-169; CLAUDE.md:18-20. **Gap:** the absolute claim "Holds no window outcome, so reading it leaks nothing" is contradicted by 150 of 21,322 fit rows whose h=5 return realizes inside the window (AUDIT-B-NPDExperiment-14) |
| 21 | Anonymization collision defect, found and fixed before any spend | positive (self-found defect) | on **52 of the 432 window days** a drawn two-letter label equalled a ticker in the same panel; symbols struck from the label pool, all 432 mappings rebuilt, collision count **zero** | session_a1_b1.md:134-138 | Section 4 / Section 7 clause 2: per-call letter labels remapped every call (REGISTRATION.md:106, :172), registered 2026-08-25 | none | pinned by six tests in `tests/test_anonymization.py` and by mutation 5 (mutations.md:91-103) | progress.md does not carry the 52-day figure; it is shipped only in session_a1_b1.md:134-138 |
| 22 | Inverted `daily_ic` sign, found on synthetic data before any real outcome was read | positive (self-found defect) | "`daily_ic` returning minus one for a perfect ranking. The experiment would have reported the exact opposite of what it measured." (n = the synthetic end-to-end run) | session_a1_b1.md:129-132; progress.md:286-289 | no bar; the practice is ADR-004's consequence, "The full verdict pipeline is proved end to end on synthetic data with fake returns" (DECISIONS.md:68-70), 2026-08-25 | none | fixed and pinned by a test asserting the convention | progress.md:286-289 "It also caught a real defect"; session_a1_b1.md:127 heads the pair "Two defects the design caught before any spend" |
| 23 | B.0b collector, five scripted faults | shipped | clean 432/432 at 5.8320 USD; kill_resume 0 double-called dates, 3 lost commits rebuilt, 0 extra spend; model_failed 4 dates × 5 attempts terminal; source_failed 3 dates, 0 calls; spend_refused 0 calls, 0.0000 USD. **Overall PASS** | mock_run.md:13-74 | "All five scenarios must pass before Stage B.1 sends a single real call." mock_run.md:11, 2026-08-25 | Amendment 4 re-froze the prompt digest that B.0b froze (from `9a174e01…` to `7e6f3d68…`), before any outcome data (REGISTRATION.md:588-597) | the kill scenario exposed a real gap (a paid call with no stored ranking) and produced the reconciliation path, "which is the reason the raw response is kept at all" (progress.md:240-245) | progress.md:232-261; session_a1_b1.md:140-153. The registration records the mock-only gap against itself: "no mock scenario could have exposed the problem, because the mock returns a valid permutation by construction. That is a real gap in mock-only verification and it is recorded as such." (REGISTRATION.md:589-591) |
| 24 | Mutation harness | shipped, **with a provenance defect** | committed table lists **six** mutations, all "caught / restored green"; the summary line reads "**All five caught and restored: True**" | mutations.md:5-14; mutations.json (six objects) | no registered bar; B.2 prompt Task 7 asks for "tests and two mutations" (progress.md:129) | none | mutations applied to real source, not a copy, with byte restore and a full re-run to prove it (mutations.md:3) | progress.md:176-178 claims "Six mutations run, all caught and restored, including the two this stage required". The audit shows the committed file matches no possible output of the committed generator — the f-string emits a digit, never "five" (scripts/mutations.py:214) — and that only mutation 6 was newly executed at B.2 (AUDIT-B-NPDExperiment-13); session_a1_b1.md:160-166 correctly lists five at its own date |
| 25 | Stored ranking integrity | positive | **415 / 415** on each of five structural checks: a ranking in the store, ranks exactly 1 to 30, labels match that day's mapping, symbols match that day's panel, label-to-symbol consistent | collection.md:55-66; collection.json `integrity` | structural only, "No forward return was read and no output was joined to any outcome." collection.md:56-58 | none | the check runs inside B.1, which is barred from computing any statistic relating an output to an outcome (CLAUDE.md:12-14) | progress.md:205-207; session_record.html:428 |
| 26 | Spend against the ledger-enforced cap | shipped | **6.9378 USD of a 10.00 USD cap**, 920 gate calls billed plus 2 calibration, 0.007508 USD per call, input 3,514,278 / output 361,641 / reasoning 217,728 tokens; batch refusal never fired, no quota error | collection.md:45-53; REGISTRATION.md:789-790; progress.md:201-203 | "**Cap: 10.00 USD, ledger-enforced.** The collector refuses a batch before sending it whenever completing that batch would cross the cap." REGISTRATION.md:290-291; `spend_cap_usd=10.0`, `batch_size=50` config.py:110-111. Registered 2026-08-25 | **Amendment 5**, same stop as Amendment 4 (data existing: the first 29 gate days). It repaired the mechanism, not the bar (REGISTRATION.md:605-622) | the cap is enforced against *measured* cost per batch, so it holds regardless of the projection (REGISTRATION.md:546-548) | closure states 6.9378 USD with "3.0622 USD unspent" (REGISTRATION.md:789-790). The headline was never adjusted for Amendment 5's own measured 0.2936 USD undercount, giving ≈7.23 USD actual (AUDIT-B-NPDExperiment-12), and "gate calls billed: 920" counts calls *recorded* |
| 27 | Artifacts preserved, and the frozen prompt digest in force | shipped | 415 stored rankings; evidence ledger with every attempt and its raw response; spend ledger; sealed returns "unchanged, read once"; digest `7e6f3d6801506bd7…` | REGISTRATION.md:764-783; progress.md:92-99 | Amendment 4 re-froze the prompt and made supersession key on the digest, so "every B.3 replay uses these bytes" (REGISTRATION.md:588-603) | Amendment 4 only | the closure corrects the closing instruction's superseded digest `9a174e01…` and states plainly that a replication starting from it "would replay a different experiment" (REGISTRATION.md:777-783). The claim "**zero** of the 415 stored rankings" came from the superseded template is **correct** | progress.md:96-99. The same paragraph's count of superseded attempts (26, cost 0.0286 USD) contradicts the repository's own generated figure of **74** at collection.md:73 (AUDIT-B-NPDExperiment-11) |

---

## Part 3. The amendments as registered claims

| # | amendment | date + what data existed | claim as stated | kind | deciding figures (n) | file:line | corrections applied | framing |
|---|---|---|---|---|---|---|---|---|
| 28 | **Amendment 0** — the operator's registered prior | "Recorded 2026-08-25, before any module touched the sealed store" (REGISTRATION.md:343-344). Data existing: none claimed | "0.05, ADOPTED FROM THE ASSISTANT. NOT INDEPENDENT." | shipped (a discipline claim, not a result) | one prior, not two; n = 1 operator, 1 assistant | REGISTRATION.md:341-368; evaluation.md:9-20 | the adoption is stated rather than hidden: "**Calibration status: one prior, not two. This experiment yields no evidence about the operator's calibration.**" (REGISTRATION.md:367-368). The empty slot is a runtime refusal, not a reminder — `require_amendment_zero` (evaluator.py:73-78) is called at :590, **before** the single sealed read at :597-598, and mutation 6 proves it fires (mutations.md:76-89) | progress.md:169-172; session_record.html:443-449 makes it the single outstanding operator action. **The ordering claim is mechanically enforced**, which is why the drafted provenance finding was dropped at consolidation; the disclosed adoption removes any residual stake |
| 29 | **Amendment 1** — temperature omitted | 2026-08-25, raised by the calibration call **before B.1 started**. Data existing: 1 calibration call | "The endpoint refused it verbatim: `Unsupported value: 'temperature' does not support 0.0 with this model.`" | shipped (procedure change forced by the endpoint) | n = 1 call; `"temperature_accepted": false` recorded in both calibration files | REGISTRATION.md:446-462; reports/stage_b1/calibration.json; config.py:98-99 | Section 12.2 registered this exact contingency in advance (REGISTRATION.md:334-337); the registration withdraws its own determinism claim rather than keeping it (REGISTRATION.md:461-462) | CLAUDE.md:43-44; session_a1_b1.md:243; session_record.html:421 |
| 30 | **Amendment 2** — `reasoning_effort` = `minimal` | 2026-08-25, calibration call, **before B.1 started**. Data existing: 2 calibration calls, no gate data | "The registered rule reads: reasoning_effort takes the highest value … **The rule selects `minimal`.**" | positive (a registered decision rule applied against the analyst's interest) | `low`: 1,753 in / 2,508 out / 2,432 reasoning, 0.027271 USD per call, **11.7812 USD** projected; `minimal`: 106 out, 0 reasoning, 0.003251 USD, **1.4045 USD**; safety budget 7.9756 USD. n = 2 calls | REGISTRATION.md:464-500; calibration.json; calibration_minimal.json | the limitation is stated plainly and repeated everywhere: "A null result is a null for gpt-5-2025-08-07 **at minimal reasoning effort**, not for the model at its best. Every sentence written about the outcome carries that qualifier." (REGISTRATION.md:483-486). The tempting post-hoc option (a `low` run over 365 of 432 days, still clearing the floor at 0.0194) is declined and the reason given (REGISTRATION.md:488-496). The audit confirms the rule's outcome is unchanged under the realized costs | evaluation.md:204-207 carries the qualifier into B.2; session_a1_b1.md:259-263; session_record.html:432-433. **But** the fired verdict sentence still reads "under frontier capability" (AUDIT-B-NPDExperiment-9) |
| 31 | **Amendment 3** — the reasoning-effort ladder `("minimal", "low")` | 2026-08-25, raised 14 gate calls into B.1; the run was stopped to record it. Data existing: 14 attempts, no outcomes | "9 of them" failed; ladder registered; "Days already collected are recollected." | shipped, **later refuted and kept** | 9 of 14 attempts failed; 5 label omissions/duplications, 4 wrong-length rankings; 1 day exhausted five retries; 7 days recollected; 9 superseded attempts costing 0.0286 USD | REGISTRATION.md:502-548 | classified as an operational fix touching no design element (REGISTRATION.md:525-529); the confound it creates is disclosed in the same amendment (REGISTRATION.md:531-536); superseded rows stay in the ledger — "A ledger is history and history is not edited." (REGISTRATION.md:541-542) | kept rather than deleted after being refuted: "Amendment 3 was the wrong diagnosis, correctly recorded, and it is superseded here rather than quietly dropped." (REGISTRATION.md:563-564); session_record.html:424 flags it in the table as "**This diagnosis was wrong.**" The keeping is the harder choice, made |
| 32 | **Amendment 4** — strict output schema and re-tuned ladder | 2026-08-25, raised 29 gate days into B.1. Data existing: 48 free-form attempts plus an 8-day strict-schema pilot; no outcome data | "**The ladder is re-tuned.** … Retries are independent samples, and at 88 percent per attempt four cheap attempts leave an expected failure rate near zero." | **qualified positive**: the diagnosis (format, not budget) is supported; the projections it shipped are not | diagnosis: `minimal` 12/29 = 41 % failure, `low` 9/19 = 47 % (n = 48 attempts). Re-tuning basis: **7 of 8** held-out days at first attempt (n = 8), latency 2.3 s, projected 2.86 USD over 432 days | REGISTRATION.md:550-603; config.py:100-105 | the schema fix is targeted at "eight of the nine observed failures" and the amendment states what strict mode cannot express: "Uniqueness is not expressible in strict mode, so the parser checks it and the collector retries." (REGISTRATION.md:566-571). The prompt freeze is re-established and supersession generalized to key on the digest (REGISTRATION.md:588-603) | the diagnosis is carried everywhere (progress.md:212-214; session_a1_b1.md:246; session_record.html:425). The audit finds the decisive n = 8 comparison not significant (Fisher p = 0.216), realized first-attempt compliance 59.5 % against the claimed 88 %, retries **not** independent (p = 4.1e-13), 17 terminal failures against ~0 expected, realized spend 6.59 USD against the 2.86 USD projection, and the 16.3 s latency row drawn from `low` while headed "at `minimal`" (AUDIT-B-NPDExperiment-4, -5, -16) *(live, unanchored)* |
| 33 | **Amendment 5** — rejected answers are billed, so the ledger records them | 2026-08-25, same stop as Amendment 4. Data existing: first 29 gate days | "recorded 0.3494 USD against an actual 0.6429 USD, a **46 percent undercount**" and "**A cap enforced against a number 46 percent too low is not a cap.**" | positive (a self-found defect in the mechanism the spend section leans on) | 0.3494 vs 0.6429 USD over 29 gate days; 0.2936 USD unrecoverable | REGISTRATION.md:605-622 | the defect is measured, the fix is structural (`UnparseableResponse` now carries the usage), the unrecoverable portion is stated rather than estimated away, and the superseded ledger rows "stay exactly as they were written" (REGISTRATION.md:617-622) | progress.md:219-222 "Amendment 5 mattered more than its size."; session_record.html:426-427 gives it a stop-coloured callout. The only complaint is that the closure headline was not adjusted for it (AUDIT-B-NPDExperiment-12) |
| 34 | **Amendment 6** — the terminal state, POST-READ | drafted before the B.2 evaluation ran, **arrived after it**. Data existing: the full result | "This amendment carries **no pre-registration force**. … It is preserved as **a record of intent, not as a binding clause**." | open item, correctly defused | four gates named between the experiment and the intended engine; "**The first gate was never authorized.**" | REGISTRATION.md:624-659; ADR-012 DECISIONS.md:231-247 | the ordering is stated in the first line by decision, so a reader scanning the list sees it without reading the body (DECISIONS.md:239-243) | progress.md:59-63. Nothing downstream is claimed |
| 35 | **Amendment 7** — VOID | drafted in the same batch, arrived after the read | "**It is void and it is not applied.** Scoring spent data against new horizons is a second look however it is labelled." | open item, declined | recovering the decay curve would need a fresh collection at roughly 7 USD | REGISTRATION.md:661-674; ADR-013 DECISIONS.md:249-266 | the cost is named and accepted: "The cost of this decision is a curve the operator wanted and will not get from this data. That cost is paid on purpose." (DECISIONS.md:265-266) | progress.md:65-66. Voiding rather than applying is the harder choice, made |

---

## Part 4. Open items at the anchored SHA

| item | status as stated | file:line | closed on its own rule? |
|---|---|---|---|
| Phase C.1, the frontier-trio replication | "conditional phase C.1 authorized on the frontier trio …" — conditional on the top verdict row, which did not fire | REGISTRATION.md:272; evaluation.md:121-123; REGISTRATION.md:658-659 | Yes. Row three fired, C.1 was never authorized, and nothing downstream of it is claimed (progress.md:138) |
| The B.3 replay schedule | Kimi K3 and GLM-5.2 "replays roughly mid 2027"; **Qwen 3.8 Max "undocumented in the material held. Verify before its window is computed. Never assume." — blocked on verification** | REGISTRATION.md:372-389 | Open by design, and the discipline is enforced: "No window is computed from an assumed cutoff." The threshold it ships — "roughly 221 trading days" — carries the same no-overlap arithmetic as the floor (AUDIT-B-NPDExperiment-6) |
| The `consolidat` rationale cell (Section 16 clause 4) | "the cell stays dormant, named, and applicable only if a rationale-emitting variant is ever registered" | REGISTRATION.md:433-438; DECISIONS.md:92-96 | Correctly dormant. This design emits no rationales, so the cell cannot be tested here; continuity is recorded rather than claimed |
| ADR-014's dormant observation | "It may only be promoted by a future test that names it in advance." | REGISTRATION.md:741-742 | Left open by rule. But the figure it preserves for that future test is wrong (entry 11) |
| The registered by-effort split | promised as a B.2 deliverable in two shipped documents | REGISTRATION.md:534-535; session_a1_b1.md:268-270; session_record.html:434 | **Not closed and not recorded as unclosed** (entry 13) |
| Amendment 6's four gates (cost survival, forward shadow series, broker access under HFExperiment's reopening conditions) | "Between this experiment and that engine sat four gates, each requiring its own registration" | REGISTRATION.md:648-656 | Moot: the first gate was never authorized. Broker access is explicitly deferred to HFExperiment's conditions |
| The AiTrader news-drift experiment | "**untouched and unaffected** … **Its verdict remains due at 60 clusters.**" | REGISTRATION.md:758-762; progress.md:82-83 | Outside this repository. The non-interference claim is enforced in code — `news_experiment.db` appears in source only inside the guard that forbids opening it (build.md:7; session_a1_b1.md:87-88) |
| The OpenAI key | "Revoke or retain at the operator discretion. This repository never printed, logged, or committed it." | REGISTRATION.md:787-788; progress.md:103 | Open by design, outside the repository. `.env` is gitignored and was never read |
| CLAUDE.md's Boundaries section | still describes "Three amendments … in force" and Amendment 3's superseded ladder | CLAUDE.md:42-47 | Stale at the anchor: five amendments were in force at the end of B.1 and seven exist (AUDIT-B-NPDExperiment-15) |
| Shipped-page counters | "9 ADRs · 5 amendments", "113 tests", "38 modules · 4,699 lines" | session_record.html:191-193 | Correct for the page's own date (stages A.1→B.1). At the anchor there are 14 ADRs and 7 amendments. The test, module and line counts are **not located** as a generated artifact in the snapshot |

---

## Part 5. Thresholded negatives — every verdict that rested on a bar

| verdict | bar | deciding figure (n) | file:line |
|---|---|---|---|
| **Does not beat coin** (Section 10 row 3, fired) | model IC bootstrap interval lower bound above zero | +0.0061, interval −0.0276 to +0.0397 (n = 404 days × 30 names) | REGISTRATION.md:274; evaluation.md:123-133; evaluator.py:546 |
| Does not beat the best baseline | contrast interval lower bound above zero | −0.0161, interval −0.0673 to +0.0351 (n = 404) | REGISTRATION.md:181-182; evaluation.md:78-80; evaluator.py:547 |
| Permutation null not rejected | two-sided p against a within-day permutation null at 10,000 draws | p = 0.5174 (n = 404 days, 10,000 resamples) | REGISTRATION.md:186; evaluation.md:113 |
| Secondary horizon, not significant | same interval rule at h = 1 | contrast −0.0300, interval −0.0677 to +0.0077 (n = 412) | evaluation.md:167-172 |
| **GO**, not DEGRADED and not BLOCKED (Section 0) | ≥ 90 % coverage; BLOCKED under 70 % or under the power floor | 415 of 432 = 96.1 % (n = 432 eligible days) | REGISTRATION.md:16-18; collection.md:35-43; section0.py:56-67 |
| Power floor cleared, collection authorized | detectable IC 0.025 at 30 names | 0.01787 at D = 432 (n = 432 days) | REGISTRATION.md:208-215; power.py:129-131 |
| Pipeline validity gate PASS | \|shuffled grand mean\| ≤ 0.02 | +0.0001 (n = 10,000 shuffles over 404 days) | evaluation.md:36-45; evaluator.py:551-553, :627 |
| `reasoning_effort` = `minimal` | projected total ≤ 80 % of the remaining cap (7.9756 USD) | `low` 11.7812 USD fails, `minimal` 1.4045 USD clears (n = 2 calibration calls) | REGISTRATION.md:329-332, :476-481; calibration_minimal.json |
| Spend cap not crossed; batch refusal never fired | 10.00 USD ledger-enforced, refusal before sending a batch of 50 | 6.9378 USD recorded (n = 922 ledger rows); ≈7.23 USD after Amendment 5's own undercount *(live, unanchored)* | REGISTRATION.md:290-291, :789-790; collection.md:45-50 |
| B.0b: all five scripted faults pass before the first real call | all five scenarios must pass | 5 of 5 PASS (n = 5 scenarios) | mock_run.md:11-21 |
| Realized power **below** the realistic band (the negative that governs the reading) | realized MDE against the 0.01-to-0.05 band | 0.0512 against a projection of 0.026 to 0.047 (n = 404, effective 201.2) | evaluation.md:90-94, :241-244; REGISTRATION.md:695-697 |

---

## Leads for the cross-repository pass

### A. Artifacts and claims here that another repository is relied upon for, or that another repository relies on

1. **The AiTrader `consolidat` rationale cell is the template for ADR-014 — and the template now
   carries a wrong figure.** "The 2026-07-27 session preserved a rationale cell, stated reasons
   containing "consolidat", at 71.7 percent on 53 calls, explicitly not a finding." —
   REGISTRATION.md:433-438; DECISIONS.md:278-279 says the dormant observation is recorded "in the
   shape AiTrader used". NPD's copy of that shape preserves an unmeasured, wrong-signed correlation
   (finding -1). **Check in AiTrader:** whether the 71.7 %/n = 53 cell is itself measured or inferred,
   and whether the same "dormant observation" form is used elsewhere to carry an underived number.
   *Comparison repository: AiTrader.*
2. **The negative this repository exists to replicate.** "The AiTrader LLM council was fed
   price-derived numbers and measured to a properly powered negative on 2026-07-27." — CLAUDE.md:3-4;
   REGISTRATION.md:34. NPD's own replication was **not** powered (realized MDE 0.0512 above the whole
   0.01-0.05 band, entry 10). **Check in AiTrader:** the power arithmetic behind "properly powered",
   whether it carries an overlap term, and whether NPD's inherited premise survives.
   *Comparison repository: AiTrader.*
3. **The source-data provenance chain.** `~/Documents/GitHub/AiTrader/analysis_bars.db` and
   `~/Documents/GitHub/AiTrader/backtest/universe.py` (sha256 `8188eea0…`), 55 formations reproduced
   0 failures, 15,474,106 daily bars across 18,474 symbols, universe id `U-LIQ-500-stk-w60-m40-p5`
   (build.md:5-30; config.py:81). **Check across repositories:** any repo quoting a different
   `universe.py` digest, a different bar count, or a different formation count for the same period is
   a CROSS_REPO_INCONSISTENCY; the port is claimed verified only here.
   *Comparison repositories: AiTrader (source), HFExperiment (the repo whose patterns were copied).*
4. **Broker access is deferred to a document in another repository.** "| broker access | under the
   reopening conditions recorded in HFExperiment |" — REGISTRATION.md:656. **Check in HFExperiment:**
   whether those reopening conditions exist and say what NPD assumes. If they do not, Amendment 6's
   gate table cites a non-existent artifact.  *Comparison repository: HFExperiment.*
5. **The state taxonomy is claimed to be shared with the news experiment.** "`model_failed` is
   operational health. `excluded_pre_cutoff` is sample composition. **The news experiment drew the
   same boundary for the same reason.**" — REGISTRATION.md:405-406. **Check in AiTrader:** whether
   the news experiment really counts `model_failed` inside its coverage denominator. A divergence is
   a cross-repo inconsistency in a claim NPD makes about another repository.
   *Comparison repository: AiTrader.*
6. **A live external commitment is asserted about another repository's state.** "The running AiTrader
   news-drift experiment is **untouched and unaffected** … **Its verdict remains due at 60
   clusters.**" — REGISTRATION.md:758-762. **Check in AiTrader:** the cluster count at its own anchor
   and whether a verdict was in fact taken before 60.  *Comparison repository: AiTrader.*
7. **The verified model cutoff, and the wrong carried estimate it replaced.** "The verified knowledge
   cutoff for `gpt-5-2025-08-07` is 2024-09-30"; the discarded carried estimate was 2024-05-31 / 515
   days (REGISTRATION.md:56-71; progress.md:302-311). **Check across repositories:** any repo still
   sizing a post-cutoff window from 2024-05-31, or from a *leaderboard-chosen* model rather than a
   cutoff-chosen one, inherits a stale external figure.
   *Comparison repositories: HFExperiment, ORBExperiment, NPLExperiment, PMExperiment.*

### B. Standards applied here that look stricter than the house norm

8. **Nothing moved after the data existed.** Every inference parameter dates from the pre-data commit;
   the only registration edit at the verdict commit is the Amendment-0 slot; a refuted amendment is
   kept and a tempting one is voided (entries 31, 35). If any other repository amended a threshold,
   promoted a secondary, or added a horizon after the read, NPD is the clean control to measure it
   against.  *Comparison repositories: HFExperiment, VRPExperiment, ETFExperiment, PMExperiment.*
9. **Structural rather than conventional controls:** the two-store seal with a guard test that walks
   every source file, `read_sealed_returns` with exactly one caller, the runtime Amendment-0 refusal
   ordered before the sealed read, a mutation harness applied to real source with byte restore, and a
   ledger-enforced spend cap checked against *measured* cost per batch. "A convention that says 'do
   not look' is not a control." (DECISIONS.md:58). **Check:** which other repositories rely on
   convention where this one relies on a guard.  *Comparison repositories: HFExperiment, solclear,
   InsiderExperiment.*
10. **Power computed and published before any spend**, with the limitation registered rather than
    repaired (Section 9, ADR-007). **Check:** whether other repositories publish a pre-data MDE at
    all, and whether they state the realized MDE beside the projection before reading the verdict.
    *Comparison repositories: retail-power-limits, ETFExperiment, VRPExperiment.*

### C. Standards applied here that look laxer than the house norm

11. **A procedure change and its shipped projections rest on n = 8.** Amendment 4's 88 percent
    first-attempt figure, its 2.3 s latency and its 2.86 USD projection all come from an eight-day
    pilot (REGISTRATION.md:573-579); all three are contradicted by the realized run (finding -4).
    Elsewhere this repository refuses to read anything off small samples. **Check:** whether other
    repositories admit pilot-sized evidence into a registered procedure and then ship its projections
    as measured.  *Comparison repositories: HFExperiment, InsiderExperiment.*
12. **A "negative control" with zero power against the defects it names.** The within-day shuffle has
    expectation zero for every possible input (finding -3), and its 0.02 tolerance is ~216
    Monte-Carlo standard errors wide. This is a *pattern* likely to have been copied along with the
    rest of the harness. **Check for the same shuffle-within-day control and the same tolerance
    constant elsewhere; if present, the same defect travels.**
    *Comparison repositories: HFExperiment (patterns explicitly copied, CLAUDE.md:54-55),
    ETFExperiment, retail-power-limits.*
13. **The power vocabulary is reusable and two of its pieces are load-bearing errors.**
    `null_ic_sd = 1/sqrt(n-1)`, `overlap_vif = 1 + 2·Σ(1−k/h)²`, `detection_mde = t·sd/sqrt(n_eff)`,
    `powered_mde` with z = 0.8416 (power.py:34-84), plus the *floor* defined with no overlap term
    (power.py:129-131) and the contrast grid assuming both series carry the **null** sd
    (power.py:107-116). Findings -1, -2 and -6 are all consequences of those last two. **Check any
    repository that reuses these helpers or the constant 0.185695 / the "detectable IC 0.025 at 30
    names" replay threshold.**  *Comparison repositories: HFExperiment, ETFExperiment,
    ORBExperiment, NPLExperiment.*
14. **A shipped verification artifact that its own generator could not have produced**
    (`reports/mutations.md`, finding -13). **Check:** whether other repositories' generated reports
    are byte-consistent with their generators, which is cheap to test wherever a generator is
    committed alongside its output.  *Comparison repositories: all with `scripts/` generators —
    HFExperiment, retail-power-limits, InsiderExperiment.*
15. **A shipped page frozen at an earlier stage while the narrative moved on** (session_record.html
    counters "9 ADRs · 5 amendments" against 14 and 7 at the anchor; CLAUDE.md's "Three amendments",
    finding -15). **Check:** whether other repositories' shipped pages and top-level operating
    documents are re-generated at closure or left at the stage that produced them.
    *Comparison repositories: HFExperiment, solclear, PMExperiment.*
