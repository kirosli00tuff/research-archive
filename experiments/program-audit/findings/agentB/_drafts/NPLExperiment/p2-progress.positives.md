# POSITIVES LEDGER — NPLExperiment, part p2-progress

**Repository / SHA:** NPLExperiment / 8f1fef83be0f76cbd671c2ce0fbfe8b1c4a5ea2c (main, 2026-09-02)
**Scope:** entries whose deciding figures are carried by my assigned documents — DECISIONS.md, progress.md, docs/ (ACCESS, H5_ACCESS, PAIR_FEASIBILITY, STAGES, SUBSTRATE) and reports/. Registration text is cited as supporting provenance where it fixes a bar or a date.
**This ledger is factual, not advocacy.** Where a figure is drawn from the live working tree it is marked UNANCHORED with the read time (2026-09-12T12:40–12:48Z).
**Kinds used:** positive · qualified positive · shipped · open · thresholded negative.

---

## 1. P3 — the control contrast (the only PASS in the repository)

- **Claim as stated:** "**P3** 114/175 pairs young-below-control (65.14%), p = **3.767e-05** — PASS" — HYPOTHESES.md:52; in my documents: "P3 114/175, p = 3.767e-05 PASS" — progress.md:480-481, and "P3 114/175, p = 3.767e-05; effective N 312/312/175 vs minimums 34/103/60" — progress.md:503.
- **Kind:** positive.
- **Deciding figures (n):** successes 114, n = 175 pairs, exact paired sign-test p = 3.766632285793312e-05 against alpha_adj = 0.016952427508441503; `n_underpowered = 137` (events with no Section 6 control, dropped from P3 only) — reports/stage_b/read.json `co_primaries/p3`. Share 0.651429.
- **File:line:** progress.md:480-481, progress.md:503; artifact reports/stage_b/read.json.
- **Bar + registration date:** "P3, control contrast: exact sign test on paired differentials, young net minus matched net, bar: negative. Registered assumption: true share negative 0.70" — progress.md:62 (operator prompt, Stage A.0 Task 4, logged 2026-08-27T00:31:45Z); alpha_adj = 1 − 0.95^(1/3) registered at the same time (progress.md:59). Control rule fixed by ADR-002, 2026-08-27, "before any pair existed" (DECISIONS.md:17-28).
- **Amendments touching the bar:** none. Amendment 3 (2026-08-28, commit 6399d63, pushed before the read) registered the verdict *table* and the reading rules, stating that only counts, timestamps and coverage existed at write time (progress.md:402, 462-464). The P3 bar itself was never moved.
- **Corrections applied:** familywise alpha_adj 0.016952 (three co-primaries); exact rather than asymptotic test; cost-band sensitivity computed (P3 identical at all three bands — reports/stage_b/read.json `secondaries/cost_band_sensitivity`, which is structurally guaranteed for a paired differential); one control excluded underpowered (NEIROETH, delisted at the event entry — progress.md:449-450) taking 176 → 175. **Not applied:** any correction for the same-dex 180-day control screen that selected the 175 (P3 cohort is 88.6 % main-dex against 50.6 % in the P1/P2 cohort — data/controls/pairs.jsonl, UNANCHORED, read 2026-09-12T12:42Z); any correction for with-replacement control reuse (82 distinct controls over 176 pairs, effective 1/Σp² ≈ 41, top control serves 15) or for entry-window overlap (mean 12.6 other pairs within ±30 days); no by-stratum P3 figure exists.
- **Framing in README / report / register:** README.md:7-9 "its listing-age contrast passed (114/175, p = 3.8e-05)"; HYPOTHESES.md:56 "a **real listing-age effect** (+6.43 price points paired differential, n = 175, generating-sample figure) too thin per event for the naive short"; docs/STAGES.md:70 "P3 114/175, p = 3.8e-05 (PASS)". The 137 dropped events are counted at progress.md:322-323 but their composition is never stated.

## 2. H1 — the Stage B row: FAIL (a negative decided on two thresholds)

- **Claim as stated:** "**THE ROW FIRED: FAIL** … P1 197/312, lower bound 0.5707 < 0.60 FAIL; P2 111/312, p = 1.000 FAIL; P3 114/175, p = 3.767e-05 PASS; the Amendment 3 table fires FAIL mechanically." — progress.md:471, 478-481.
- **Kind:** thresholded negative.
- **Deciding figures (n):** P1 197/312 (63.14 %), Clopper-Pearson one-sided lower bound 0.5706880326738533 against the 0.60 bar; P2 111/312 (35.58 %), sign-test p = 0.9999998937952859 against the one-half bar; both at alpha_adj 0.016952427508441503. Cost bands: P1 lb 0.5739630116873008 / 0.5706880326738533 / 0.5608793225336948, n = 312 each.
- **File:line:** progress.md:478-482, progress.md:501-505; artifact reports/stage_b/read.json.
- **Bar + registration date:** P1 "bar at or above 0.60", P2 "bar: the share exceeds one half" — progress.md:60-61, registered 2026-08-27T00:31:45Z, before any network call (progress.md:51, 179-183).
- **Amendments touching the bar:** none. Amendment 1 (2026-08-27) changed the event-date rule and epoch censoring, not the bars, and was made when "no census, no eligibility, no power number, no outcome value existed" (progress.md:234-235). Amendment 3 (2026-08-28) registered the consequence table before the read.
- **Corrections applied:** three-way multiplicity; exact binomial; cost-band sensitivity across the registered 3/9/18 and 6/18/36 bands; truncated-by-delisting events retained with their count (10) and their own secondary (n = 10, share_positive 0.5); coverage precondition with effective-N floors 34/103/60 checked before the read; a single write-once latch with 21 module hashes.
- **Framing:** README.md:6-8 "fired FAIL on its sealed read — profitable in 63.1% of 312 events, lower bound 0.5707 under the 0.60 bar, magnitude leg far under". Framing matches the figures. **I found nothing that lowers this negative's bar, and the direction of the one survivorship channel I did find (53 unreachable delisted HIP-3 instruments, DRAFT-p2-progress-3) is conservative for this row.**

## 3. H1 — Section 0: GO (the gate that armed collection)

- **Claim as stated:** "**The verdict: GO, retro plus forward, collectors armed.**" — progress.md:270; "**Section 0 verdict: GO** (fired 05:28:09Z)" — progress.md:348-353.
- **Kind:** qualified positive (a feasibility gate, not a result).
- **Deciding figures (n):** census 503; retro-eligible N = 312 (112 vanilla / 46 hyperp_conversion / 154 hip3; 10 truncated retained); match 176/312 = 56.4 %; delisting observability PASS 6/6; powers at achieved N 1.000 / 0.9993 / 0.9995 against minimum-N 34 / 103 / 60; combined N 430 by 2026-12-31 and 485 by 2027-03-31 at 18.5 events/month.
- **File:line:** progress.md:270-279, progress.md:348-353.
- **Bar + registration date:** "GO: all three co-primaries of Section 8 reach at least 80 percent power at alpha_adj … and the delisting-observability test of A.1 Task 4 passes in full" — progress.md:46, registered 2026-08-27 before any network call.
- **Amendments touching the bar:** none.
- **Corrections applied:** powers computed at the *registered* effect assumptions (P1 true share 0.85, P2 0.65, P3 −0.70 — progress.md:60-62), not at anything measured. Those assumptions were later falsified by the read itself (measured 0.631 / 0.356 / 0.651), which is normal pre-registration practice and is not a defect; it does mean the "powers 1.000 / 0.9993 / 0.9995" figures describe the design's sensitivity to the assumed effect and not to the observed one. Delisting observability probed on n = 6 main-dex delisted perps, zero HIP-3 (see DRAFT-p2-progress-3).
- **Framing:** docs/STAGES.md:69 "**GO** fired 2026-08-27: retro N 312, delisting PASS 6/6, powers 1.000 / 0.9993 / 0.9995 against min-N 34 / 103 / 60".

## 4. Delisting observability — PASS 6/6

- **Claim as stated:** "**Verdict: PASS in full — 6 of 6 probed delisted perps serve both their candle history (through their delisting date) and their funding history.** The retrospective cohort is not survivorship-manufactured by the venue's serving behaviour." — docs/ACCESS.md:213-216.
- **Kind:** shipped (a validity certificate carried into every downstream entry).
- **Deciding figures (n):** n = 6 (MATIC, RNDR, FTM, UNIBOT, CYBER, FRIEND), all main-dex vanilla; 1d rows 1419/535/1572/380/600/256 and one 500-row funding page each — docs/ACCESS.md:204-211.
- **File:line:** docs/ACCESS.md:198-216; carried at progress.md:229-231, progress.md:351.
- **Bar + registration date:** "For at least five, test whether candles and fundingHistory still serve their history. PASS means both serve for all probed." — progress.md:83-85, registered 2026-08-27T00:31:45Z. The bar was met exactly as written.
- **Amendments touching the bar:** none.
- **Corrections applied:** none. Not corrected for: the probe drew zero HIP-3 instruments while the cohort is 154/312 HIP-3 and the successor cohort 60/62 HIP-3; 53 census instruments — all delisted, all HIP-3 — return no candles and were excluded as `no_candles` (progress.md:275; data/census/census.jsonl UNANCHORED, read 2026-09-12T12:46Z).
- **Framing:** HYPOTHESES.md:53 drops the "by the venue's serving behaviour" hedge: "Delisting observability PASS 6/6 — the cohort is not survivorship-manufactured." **This is DRAFT-p2-progress-3.**

## 5. H2 — Section 0: DEGRADED (the surviving hypothesis), at the cull

- **Claim as stated:** "**H2: DEGRADED, collectors armed.** k = 1, alpha_h = 0.05 fixed. Deadline pairs 141 (by-dex measured model; flat-0.613 variant 106 reported beside — under which E2 sits at 0.4318 at the pass-1 alpha and the cull would fire k = 0, recorded plainly). Deadline powers E1 0.9743, E2 0.7604; min-N E1 76 / E2 169 pairs at α 0.05." — progress.md:685-690.
- **Kind:** qualified positive / open.
- **Deciding figures (n):** achieved pairs 38 of 62 (match rate 0.613); deadline projection 141 pairs (by-dex) vs 106 (flat); governing power E2 0.760372 at n = 141, alpha 0.05, true share 0.60; cull pass 1 at k = 3, alpha 0.016952: H2 0.577117 — reports/stage_a_h2/ktable_cull.json.
- **File:line:** progress.md:679, 685-690, 754-759; artifact reports/stage_a_h2/ktable_cull.json.
- **Bar + registration date:** "Any hypothesis under 50 percent power on a required co-primary at the achievable N by 2027-03-31 fires BLOCKED, at the k/alpha fixed point" — HYPOTHESES.md:143-147; registered in registrations/H2 §9 at commit 77ee522 (2026-08-27T20:53:20-07:00), before the A.1 census refresh. **Section 9 as registered did not specify whether the projection is by-dex or flat** (`git show 77ee522:registrations/H2/REGISTRATION.md` §9); the governing model is first named in Amendment H2-1, with `ktable_cull.json computed_at 2026-08-28T05:41:32Z` already in hand.
- **Amendments touching the bar:** Amendment H2-1 (2026-08-28) fixes k = 1 and alpha_h = 0.05 and records the verdict; its own "what data existed" statement is "Counts, rates, and timestamps only … No outcome value of any fresh event has been read; the H2 verdict machinery does not yet exist" (registrations/H2/REGISTRATION.md:253-259). Data existed: yes — the eligibility ledgers, the 38-row pair ledger and the k-table, all outcome-blind.
- **Corrections applied:** familywise alpha at the fixed point; simultaneous-drop semantics registered at A.0 and applied unchanged, with the disclosed sensitivity that H2 would have dropped under the flat projection (DECISIONS.md:160-164). **Not applied:** the ADR-017 rule that the pessimistic end governs, which was applied to H3 and H4 and not to H2's two projections (see DRAFT-p2-progress-6).
- **Framing:** README.md:3-5 "H2 open and amended to a two-look plan, 62/62 pairs collecting"; HYPOTHESES.md:70. The k = 0 flat variant is disclosed in HYPOTHESES.md? — no; it is disclosed in DECISIONS.md:160-164, registrations/H2:286-289 and progress.md:685-688, not in README.

## 6. H2 — the amended design: recomputed power 0.8886 / 0.8629 "above the registered 0.80 target"

- **Claim as stated:** "**Recomputed power beside the registered 0.80 target:** single-look governing 0.8886 (the Section 0 function returns GO), two-look governing 0.8629. Section 0's DEGRADED record is not edited and not re-fired." — progress.md:939-941.
- **Kind:** qualified positive (shipped as the README status line).
- **Deciding figures (n):** deadline projection 135 pairs; E2 power 0.888596 at true share 0.625 and **0.731814 at the registered 0.60** (reports/stage_a_h2/ktable_amended.json `single_look_k_table_extension_at_deadline`); two-look governing 0.862922; look-1 min N 59 (E1 42, E2 59), look-2 min N 117 (E1 84, E2 117); at n = 117: k₁ = 38, k₂ = 69, spend 0.0182 + 0.0240 = 0.0422 inside alpha_h = 0.05.
- **File:line:** progress.md:913-946, progress.md:1061-1077; artifact reports/stage_a_h2/ktable_amended.json.
- **Bar + registration date:** the 0.80 power target is from the H2 Section 0 map registered at A.0 (progress.md:549, commit 77ee522). The **E2 economic floor** was registered at A.0 as "at or above **two** times the pair's registered central cost" (progress.md:549) with true share 0.60.
- **Amendments touching the bar — dated, with what data existed:**
  - **Amendment H2-3 Change 2 (2026-08-28, commit f31f7a3, 07:01Z):** E2's floor 2× → 1×, and E2's true share 0.60 → 0.625 by linear interpolation. Data that existed: counts, tags, timestamps, pre-entry funding features; all three H2 latches absent; the pair reader had seen only synthetic fixtures (progress.md:831-839, 988-993). **Direction: a weakening, stated as one** — "This is a weakening, and it is recorded as one" (DECISIONS.md:300). The interpolated share is stated to be "a choice, not a measurement" and derived from a figure itself called "a judgment discount from E1's 0.651, not a measurement" (DECISIONS.md:308-313).
  - **Amendment H2-3 Change 1 (same commit):** main-dex fallback control; match rate 0.613 → 1.000 (62/62). Direction: a relaxation, stated as one (DECISIONS.md:282-286).
  - **Amendment H2-3 Change 3 / H2-4 (same day):** one look → two looks, alpha 0.02 + 0.03. Direction: buys a date at the cost of alpha; total spend 0.0422 ≤ 0.05.
  - **Amendment H2-4 §7 / ADR-025 (same day):** corrects a defect in H2-3's own look-2 wording that would have fired FAIL on strong early evidence. **This is a falsification recorded against the authors' own amendment, not a rescue** (DECISIONS.md:354-380).
- **Corrections applied:** exact binomial sequential boundary with the spend conditional on not rejecting at look 1; a two-clause materiality test for the alpha split written before it was applied, which refused the two splits that gained power (DECISIONS.md:328-337; ktable_amended.json `alpha_split_evaluation`); a registered futility boundary at a 0.10 conditional-power floor; the 2× floor retained as a named secondary at every look; every minimum N also reported at the unchanged 0.60. **Not applied:** any measurement of E2's true share from the 175 generating-sample paired differentials, which the register's own rule 1 permits.
- **Framing:** README.md:15-16 "Look-1 minimum N 59, look-2 minimum N 117; recomputed power at the deadline 0.889 single-look / 0.863 two-look" — **the 0.60 row is absent from the README**; it is present at HYPOTHESES.md:74, DECISIONS.md:313-316 and progress.md:1074-1076. **This is DRAFT-p2-progress-5.**

## 7. H2 — "62 of 62 pairs achieved" and the projected look dates

- **Claim as stated:** "**Pairs achieved, by tag: 62 of 62 — 38 `same_dex`, 24 `cross_dex`.** … The backfillable cohort's match rate: **0.613 → 1.000**." and "**Projected look-1 date: 2026-11-26.** … **Projected look-2 date: 2027-03-01**, one month inside the registered 2027-03-31 deadline. At the deadline the projection is 135 pairs." — progress.md:1057-1065.
- **Kind:** shipped (a dated schedule carried into README and docs/STAGES.md).
- **Deciding figures (n):** 24 of 24 previously unpairable events assigned, 0 exclusions, 19 distinct main-dex elders, 174 candidates considered per fallback event, 0 skipped for coverage, 24/24 control-leg l2Book windows recorded `expired` loudly (progress.md:877-892); accrual 18.57 events/month (n = 113 listings / 182 d, progress.md:664); `readable_lag_days_backfill` 92, `readable_lag_days_forward` 94 (ktable_amended.json `inputs`).
- **File:line:** progress.md:877-892, progress.md:936-946, progress.md:1057-1065; docs/STAGES.md:24, :55.
- **Bar + registration date:** look-1/look-2 minimum N registered by Amendment H2-3 Change 3 and computed in Amendment H2-4 (2026-08-28), before any outcome value existed.
- **Amendments touching the bar:** as in row 6.
- **Corrections applied:** the by-dex and flat projection models coincide under the fallback (match rate 1.000), and the withdrawal sensitivity is recorded — "at the pre-amendment 0.613 the deadline count would be 82 instead of 135" (progress.md:946). **Not applied:** any sensitivity on the *accrual* rate itself. UNANCHORED check (data/controls/h2_pairs.jsonl, read 2026-09-12T12:42Z): 63 rows — 62 assigned 2026-08-28, **one** assigned since (2026-09-02), against a projection needing ~18.6 new pairs per month. **This is DRAFT-p2-progress-8.** Look 1 does not depend on forward accrual (`projection_by_month` shows `forward_pairs_readable: 0` through 2026-11-30); look 2 does.
- **Framing:** README.md:3-5 "62/62 pairs collecting, look 1 due 2026-11-26 and look 2 due 2027-03-01"; docs/STAGES.md:55 "**For H2 those dates are 2026-11-26 (look 1) and 2027-03-01 (look 2).**"

## 8. H3 — BLOCKED (a negative decided on a power threshold)

- **Claim as stated:** "**H3: BLOCKED.** Measured main-dex accrual 0.5/month (n = 3/182d) against the falsified ~9.4 planning figure; deadline N = 5 vs P1 min-N 262; powers 0.0000 / 0.0057 (0.1160 at the optimistic 0.65, beside)." — progress.md:692-693.
- **Kind:** thresholded negative.
- **Deciding figures (n):** main-dex accrual 0.5/month, n = 3 listings in 182 days (progress.md:664-666, docs/ACCESS.md:265-267); deadline N = 5; P1 min-N 262 at k = 1; magnitude leg min-N `None` — "governing true share at or below the null: no n reaches 0.80" (ktable_cull.json `min_n_for_080/H3/MAG`).
- **File:line:** progress.md:692-693, progress.md:760-762; artifact reports/stage_a_h2/ktable_cull.json.
- **Bar + registration date:** the 50 %-power cull floor, registered in each successor's Section 9 at A.0 (2026-08-28, commit 77ee522) before the A.1 measurement. The registration also pre-registered the expectation of BLOCKED (progress.md:552).
- **Amendments touching the bar:** Amendment H3-1 (2026-08-28) records the verdict; no bar moved.
- **Corrections applied:** the honest-range rule (ADR-017): power computed at both the optimistic 0.65 and the generating-sample-derived 0.356, with the **pessimistic end governing** (DECISIONS.md:202-211). Re-checked at the relaxed k = 1 alpha 0.05: still BLOCKED (min-N 262 against N = 5).
- **Framing:** HYPOTHESES.md:89 "A documented answer. Reopens only on an order-of-magnitude higher main-dex listing rate"; README.md:17 "H3 and H4 fired BLOCKED on measured rates — documented answers." **This negative was not reached by a process that would have produced a positive on noise: the governing figure is a measured listing count, not an assumption.**

## 9. H4 — BLOCKED (a negative decided on a power threshold)

- **Claim as stated:** "**H4: BLOCKED.** Conditioning rates 0.1774/0.1290/0.0806 (n = 62); deadline cell Ns 30/22/13; best-cell power 0.0140 governing (0.7106 at the declined optimistic 0.85, beside). The registered expectation confirmed." — progress.md:694-697.
- **Kind:** thresholded negative.
- **Deciding figures (n):** conditioning rates 0.1774 / 0.1290 / 0.0806 measured on n = 62 fresh events, 0 absent; median trailing entry funding +31.6 %/yr; best-cell deadline power 0.013958 (ktable_cull.json `cull_bydex/passes`).
- **File:line:** progress.md:677, 694-697, 763-766; artifact reports/stage_a_h2/ktable_cull.json.
- **Bar + registration date:** as row 8; requirement mode `any` (best cell) registered at A.0 (ktable_cull.json `inputs/requirement_modes/H4`), with Sidak correction within the hypothesis over the three registered thresholds (progress.md:555).
- **Amendments touching the bar:** Amendment H4-1 (recorded **before any conditioning value existed**) resolved the absence rule for the conditioning feature — "the H1 event-side partial-window mean governs; the 0.95 bar applies to control candidates only" (progress.md:699-701). Amendment H4-2 records the verdict.
- **Corrections applied:** ADR-017's honest range with the pessimistic end governing (0.0140 governs, 0.7106 at the declined optimistic 0.85 reported beside); within-hypothesis Sidak; measured rates rather than assumed.
- **Framing:** HYPOTHESES.md:106; README.md:17. As with H3, the deciding figure is measured.

## 10. H5 — PENDING, the census window, and its two cleared structural clauses

- **Claim as stated:** "**The row: PENDING. The census window closes 2026-09-26.**" — progress.md:1388; clause table at progress.md:1393-1401: "instruments carrying a served reference | **94** | ≥ 20 | **clears**"; "funding served on those instruments | **94 of 94, share 1.000** | ≥ 0.500 | **clears**"; "instruments at 30 days of coverage | **0** | ≥ 20 | **window open**"; "median absolute basis, `extended`, n = 188 | **4.14 bp** (IQR 0.71–9.15)"; "share over 18 bp / over 54 bp | **9.57 % / 1.60 %**"; "passes needed / projected fire | **29** / **2026-09-26**".
- **Kind:** open (with two positives inside it: the two cleared structural clauses).
- **Deciding figures (n):** 273 HIP-3 instruments enumerated over 10 dexs → 151 resolved (118 equity, 15 ETF, 18 index) → **94 live** after the three-field delisted rule (57 excluded, 0 conflicting); reference served 94/94, funding served 94/94; basis pool n = 188 = 94 instruments × 2 snapshots **8 m 20 s apart** (reports/h5/verdict.json `inputs.snapshots_counted`); covered days max 1.
- **File:line:** progress.md:1269-1281, progress.md:1386-1405; artifacts reports/h5/verdict.json, reports/h5/census.json, reports/h5/retro.json.
- **Bar + registration date:** Section 6 outcome map registered at H5 Task 1 (2026-08-28, commit 98e7e01, 21:38:58Z) **before any H5 network call** (progress.md:1186-1192): VIABLE needs ≥ 20 instruments with a served reference **and** ≥ 30 days coverage each **and** median absolute basis > 54 bp in at least one session tag **and** funding served on at least half; CLOSED on median < 18 bp in every tag, or < 20 reference-carrying instruments, or funding on fewer than half. The 54 bp bar is arithmetic on the registered HIP-3 cost band (ADR-029, DECISIONS.md:464-481) and is derived in code, not written as a literal.
- **Amendments touching the bar — dated, with what data existed:**
  - **Amendment H5-1 (2026-08-28, during Task 2, commit 13c6965):** the CLOSED floor clause waits for the coverage bars, "because a single cross-section lands in one session tag and 'under 18 bp in every tag' would have been satisfied vacuously. **Makes CLOSED strictly harder**; it cost this entry the same-day close" (progress.md:1304-1307). Data existed: the census counts and one cross-section. Direction: harder. **The gate it added is the coverage-day count, not tag population** (npl/h5/outcome.py:145), so the vacuity it names is deferred, not removed — see DRAFT-p2-progress-2.
  - **Amendment H5-2 (same commit):** delisted instruments excluded on a conjunctive three-field rule. Data existed: the full census including the delisted stratum's basis distribution (30.5 bp median, 45.6 % over the bar). Direction: "it makes VIABLE **strictly harder** and deleted this entry's only route to it" (DECISIONS.md:510-511). **This is a bar re-specified after data existed, disclosed as such by the authors** ("The amendment was made with the census in hand, which is disclosed in full in its own text", DECISIONS.md:509-510). Its supporting claim "Every observation above the bar lived in dead markets" (DECISIONS.md:498-499) is contradicted by the repository's own fired verdict — **DRAFT-p2-progress-1**.
- **Corrections applied:** session tagging against a calendar written out by date before collection (ADR-028); same-snapshot-only basis construction with cross-snapshot refusal; absences recorded, never interpolated; the retrospective secondary gated to coins outside the generating sample, the fresh plan and both legs of every H2 pair, costing 124 of 151 instruments and kept anyway (DECISIONS.md:536-546); the secondary may fire CLOSED but never VIABLE; pre-amendment census rows skipped and counted (273) rather than assumed live; two input-wiring defects found and fixed before the recorded firing (progress.md:1414-1420). **Not applied:** any correction for the pseudo-replicated n = 188 (DRAFT-p2-progress-9); any requirement that the four registered session tags be populated (DRAFT-p2-progress-2).
- **Framing:** README.md:89-91 "The H5 row **fires on 2026-09-26 either way** — a verdict is never withheld for want of a prior"; docs/STAGES.md:40 "The map fires on **2026-09-26**, when the 20th-best-covered instrument reaches 30 covered days **at one pass per day**"; docs/STAGES.md:56-58 "its row fires on schedule". HYPOTHESES.md:132 presents all three terminal branches as live ("over 54 in at least one tag (VIABLE)") while HYPOTHESES.md:129 states the same page's amendment "deleted this entry's only route to VIABLE" — **primary evidence outside my assignment, recorded here for dedup.** The 2026-09-26 date was recomputed to ~2026-10-05 in post-anchor commit dff1663 (DRAFT-p2-progress-7).

## 11. H5 — "the venue accrues funding on dead markets" (the honesty-clause demonstration)

- **Claim as stated:** "**32 delisted instruments — zero open interest, zero volume, no book — are still served an unbroken hourly funding series**, latest row 2026-08-28T21:00Z." — HYPOTHESES.md:129; in my documents: progress.md:1293-1297 and docs/H5_ACCESS.md:204-210.
- **Kind:** shipped (a measurement used as the registration's own epistemic demonstration).
- **Deciding figures (n):** 32 of 57 delisted resolved instruments, 168 funding rows each; `funding_history_states_resolved: {no_data: 25, stored: 126}` (reports/h5/census.json).
- **File:line:** progress.md:1293-1297, docs/H5_ACCESS.md:204-210, DECISIONS.md:436-438.
- **Bar + registration date:** none — descriptive, no bar.
- **Amendments touching the bar:** none.
- **Corrections applied:** funding is recorded as **service** (presence, row counts, timestamps); no funding rate value is read on any H5 path, pinned by AST test (progress.md:1224-1226).
- **Framing:** used to support Section 4's honesty clause. **Checked and found sound** — the counts reproduce from reports/h5/census.json, and the authors correctly scope the companion "25 long-dead instruments return no rows" to the registered 180-day probe window (progress.md:1332).

## 12. Shipped artifacts in my documents, with the support each rests on

| artifact | file:line | deciding figures (n) | bar / registration date | corrections | framing |
|---|---|---|---|---|---|
| Measured per-endpoint rate ceilings and operating paces | docs/ACCESS.md:118-158, ADR-005 DECISIONS.md:56-68 | n = 846 ledgered probe requests; refusals on exactly 2 endpoints (perpDexs ~79/min, candleSnapshot@5000 ~23/min); refusal body verbatim `null` + HTTP 429 | "measured never assumed … half the measured ceiling", 2026-08-27 | drift re-probe 2026-08-28: 0 refusals in 60 requests, pacing unamended (docs/ACCESS.md:282-288) | "the documented 1200 weight/min budget does not describe admission" — measured beats documented, stated |
| Retention table | docs/ACCESS.md:158-196 | n = 12 instruments; funding epoch 2023-05-12T00:00Z on 5 of 5 launch-era; candle/1h/funding agree on the same UTC day for 7 of 7 post-epoch | A.1 Task 3, 2026-08-27 | epoch censoring added by Amendment 1 when no census/eligibility/power/outcome existed | carried into ADR-009; the ±1 day tolerance is claimed to hold "to well under" it on n = 7 |
| Cost bands 9 bp vanilla / 18 bp HIP-3 | ADR-003 DECISIONS.md:30-39 | venue base 1.5 maker / 4.5 taker per side; HIP-3 double | registered Section 5, 2026-08-27 | `deployerFeeScale` recorded per instrument as a live verification input; P1 cost-band sensitivity computed | used unchanged as the H5 54 bp bar's input |
| The 54 bp VIABLE bar | ADR-029 DECISIONS.md:464-481 | 3.0 × 18 bp; "neither 18 nor 54 is written as a literal anywhere in the map" | H5 Section 6, 2026-08-28, before any price read | **verified in code** — npl/h5/outcome.py:70-77 derives both from CONFIG; no literal | sound |
| The ticker→underlying mapping | ADR-026 DECISIONS.md:382-411 | 198 exact strings, three disjoint tables, disjointness checked at import; `para:IGV` born mid-stage and recorded `not_in_registered_mapping`, **not added** | committed before the first price read | fuzzy/prefix matching explicitly rejected | sound — a universe rule that refused to extend itself after the census |
| The session calendar | ADR-028 DECISIONS.md:440-462 | NYSE closures and 13:00 closes written out by date 2024–2027; 16 fixtures ON the boundaries; a year outside the table is a loud refusal | H5 Section 5, before collection | — | sound as a tagger; **the collector that feeds it can only reach 2 of its 4 tags** (DRAFT-p2-progress-2) |
| The two-look boundary table | reports/stage_a_h2/ktable_amended.json; progress.md:913-946 | look-1 min N 59, look-2 117; k₁ 38, k₂ 69, spend 0.0182 + 0.0240 = 0.0422; futility f₁ E1 31 / E2 27 | Amendments H2-3/H2-4, 2026-08-28, before any outcome | the pre-amendment 169 recomputes exactly from the same inputs and reproduces H2-1 — the arithmetic's own check (progress.md:919-920) | sound arithmetic; the *assumption* feeding it is row 6 |
| Mutation harnesses | progress.md:336 (5/5), :731 (6/6), :492 (3/3 MB), :999-1015 (6/6 MA), :1428-1441 (7/7 MH) | 27 mutations, all CAUGHT, source restored byte-for-byte, bytecode purged before every run | registered per stage in each operator prompt | the register A.4 harness re-run against the amended source still caught 6/6, so older pins did not rot | sound; the MA/MH tables name the pin that caught each |
| docs/PAIR_FEASIBILITY.md | docs/PAIR_FEASIBILITY.md:1-115 | ~2.2N capital per pair; 45-pair hard cap at $1,000; 12–14 concurrent pairs at a 0.61 match rate; n = 78 spread legs | written 2026-08-28 at A.3 Task 6 | — | **stale against the same-day Amendment H2-3** (match rate now 1.000, 24/62 pairs cross-dex) — DRAFT-p2-progress-10 |
| `scripts/wait_for_net.sh` / ADR-032 | DECISIONS.md:549-602; progress.md:1520-1556 | 4 boundary `source_failed` sweeps; direct probe 200 in 0.15 s; happy path 0.054 s, bogus host exits 0 at a 6 s deadline | not a registration amendment, by stated choice | charges nothing, never suppresses an outage, both tested | "**Data integrity was not at risk** … the daily pass catches up regardless" — true for the funding/candle substrate, false for H5's point-in-time snapshots (DRAFT-p2-progress-7) |

## 13. Open items carried at the anchor

| item | kind | state | file:line |
|---|---|---|---|
| H2 operator prior slot | open (blocks both looks structurally) | reserved, empty; the assistant fills none | progress.md:1098-1103; README.md:80-85 |
| H5 operator prior slot | open (blocks the successor draft, not the map) | reserved, empty | README.md:87-91 |
| H2 look 1 | open | dark; `h2_look1_latch.json` absent; due 2026-11-26 at 59 readable pairs | progress.md:1084-1089; docs/STAGES.md:25 |
| H2 look 2 | open | dark; cannot run before look 1's latch exists; due 2027-03-01 at 117 | docs/STAGES.md:26 |
| H5 terminal row | open | PENDING; fires when 20 instruments reach 30 covered days | progress.md:1388; docs/STAGES.md:41 |
| H3, H4 prior slots | open but moot | both hypotheses BLOCKED, neither has a Stage B to gate | README.md:83-85 |
