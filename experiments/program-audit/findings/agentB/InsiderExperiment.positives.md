# Agent B positives ledger — InsiderExperiment @ 12d9fd36cf055cb10ea67a3fc737e404217bc95a

Repository: InsiderExperiment, anchored SHA `12d9fd36cf055cb10ea67a3fc737e404217bc95a` (master, 2026-08-25).
Consolidated from `_drafts/InsiderExperiment/all.positives.md`, which was written as a single part.
No duplicate rows existed to merge; every draft row is carried forward and every reference to a
draft finding has been rewritten to its consolidated ID. Companion to `InsiderExperiment.md` in
this directory. Sources: `SNAP/InsiderExperiment/` for every file:line below; `InsiderExperiment.md`
for the findings, for its "What Agent B checked and found sound" section (cited as *sound item n*)
and for its git and live-tree recomputations. This ledger opened no live repository.

**This ledger is factual, not advocacy.** It records every registered hypothesis, sub-test, shipped
artifact, open item and thresholded negative in the repository, whether or not `InsiderExperiment.md`
found fault with it, so the cross-repository pass can compare what was earned against what was framed.

**Two standing facts that apply to almost every row, stated once.**

*Registration timing.* REGISTRATION.md:5-9 says "Registered 2026-08-25, Stage A.1. Every parameter in
this document is fixed before any measurement runs. Section 0 is committed before Task 4 computes
anything". Per AUDIT-B-InsiderExperiment-5 and sound items 11-12 (git, read-only, live repo), the
commit order on 2026-08-25 local (UTC-07:00) was: `fbfc74e` 18:34:56 Section 0 -> `398755b` 18:38:50
Sections 1-16 -> `ccc9b13` 18:47:16 corpus built, CORPUS-GO fired -> `cb17046` / `672b343` 19:11:45 ->
`d8b81f1` 19:11:55 Sections 15-16 written -> `12d9fd3` 23:24:15 closure. So every Section 0-16 bar was
registered before data existed. Sound item 12 verifies `mde_go_ceiling_bp`, `mde_degraded_ceiling_bp`,
`corpus_event_floor`, `corpus_coverage_floor`, `t_critical`, `newey_west_lags` and
`decayed_gross_band_bp` byte-identical from `fbfc74e` to the anchor.

*Amendments.* Section 16 (REGISTRATION.md:798-800) reads "None in force. Section 0 fired BLOCKED, so no
amendment can authorize Stage B." No numbered amendment exists anywhere in the repository.
AUDIT-B-InsiderExperiment-5 identifies **two undeclared post-data changes** at `672b343` (19:11:45,
i.e. after the corpus existed at 18:47): the deletion of the registered `Config.benchmark_id` field,
and the reordering of `corpus/routine.py:classify`. Both are flagged in the rows they touch.

*No README.* The snapshot carries no README.md. The framing column therefore cites the documents that
serve that role: REGISTRATION.md Sections 15 and 17 (the results and closure report), progress.md,
DECISIONS.md and CLAUDE.md.

---

## A. Registered gates, verdicts and the verdict table

**A1. CORPUS-GO on the qualifying-event floor.**
- Kind: **positive**
- Deciding figures (n): 4,585 qualifying events against a floor of 1,000, from an intake of 2,876,095 non-derivative in-span transactions (n = 2,876,095 charged; 4,585 retained, 0.16 %)
- file:line: REGISTRATION.md:594; reports/stage_a1/corpus.json:2, :175-176; intake table REGISTRATION.md:618-628
- Bar + registration date: "**1,000 qualifying events** over the bar span, counted after every ex-ante filter in Section 3" — REGISTRATION.md:70-71; `corpus_event_floor=1_000` at src/insider/config.py:145. Registered in the Section 0 commit `fbfc74e`, 2026-08-25 18:34 local, 13 minutes before the corpus was built.
- Amendments touching the bar: none (REGISTRATION.md:798-800); floor byte-identical from first commit (sound item 12). Data existed? No — bar predates the corpus.
- Corrections applied: **ADR-013** (DECISIONS.md:400-416) — the build's composite natural key silently merged 43 duplicate purchase lines, so the build reported 4,585 while the table held 4,542; the store moved to a surrogate key and the build now raises on divergence. `InsiderExperiment.md` AUDIT-B-InsiderExperiment-6 (S3, STALE_FIGURE) finds the Section 15.1 by-year table at REGISTRATION.md:601-608 still sums to the pre-correction 4,542 beside the corrected 4,585 headline.
- Framing: "**The corpus did not fail.** A later reader will see BLOCKED and assume the data was thin. It was not." — REGISTRATION.md:818-825; repeated progress.md:20-27, DECISIONS.md:294-298. `InsiderExperiment.md` AUDIT-B-InsiderExperiment-4 (S3, UNSUPPORTED_POSITIVE) accepts the count but challenges the floor's derivation, not the verdict.

**A2. CORPUS-GO on the session-coverage floor.**
- Kind: **positive**
- Deciding figures (n): session coverage 0.9954110898661568 (99.5 %) against a floor of 80 %; n = 2,615 in-span sessions, 12 with an empty book
- file:line: reports/stage_a1/corpus.json:173; REGISTRATION.md:594-596; denominator reports/stage_a1/port.json:2; empty-book count reports/stage_a1/power.json:115
- Bar + registration date: "**80 percent of in-span sessions carrying a non-empty book** at the primary six-month hold" — REGISTRATION.md:72-73; `corpus_coverage_floor=0.80` at src/insider/config.py:146. Registered `fbfc74e`, 18:34 local.
- Amendments touching the bar: none. Data existed? No.
- Corrections applied: none.
- Framing: REGISTRATION.md:822-825 table ("Session coverage | 99.5 percent | 80 percent"), progress.md:22-23, :236. `InsiderExperiment.md` sound item 6 reproduces 1 − 12/2,615 = 0.9954111 exactly and confirms the floor is applied to book non-emptiness, which is what Section 0.3 registers.

**A3. The power gate: BLOCKED on the registered primary, firing verdict row V7.**
- Kind: **thresholded negative**
- Deciding figures (n): MDE 49.3543 bp per month against a BLOCKED floor of 40.0; n = 2,581 sessions, VIF 0.8993, N_eff 2,869.9, daily excess-return sd 62.9519 bp, annualized TE 9.9933 %, monthly SE 24.6771 bp, t 2.0
- file:line: reports/stage_a1/power.json:6-12, :132-136; REGISTRATION.md:708-719; V7 row REGISTRATION.md:443
- Bar + registration date: "**BLOCKED** | MDE above 40 bp per month | The design cannot detect an effect anywhere in the range the literature reports." — REGISTRATION.md:43; `mde_degraded_ceiling_bp=40.0` at src/insider/config.py:144. Registered `fbfc74e`, 18:34 local, before the corpus and before the power run at 19:11.
- Amendments touching the bar: none; bar byte-identical from first commit (sound item 12). Data existed? No.
- Corrections applied: none to the figure. `InsiderExperiment.md` sound item 1 reproduces the entire power chain from `var/insider_dispersion.db` to the last published digit, including the lag grid.
- Framing: the fixed closure language, REGISTRATION.md:812-816, identical at DECISIONS.md:288-292 and progress.md:14-18, declared at progress.md:174-179 "not to be softened or strengthened". Four `InsiderExperiment.md` findings bear on it and **all four leave BLOCKED standing or make it more secure**: AUDIT-B-InsiderExperiment-1 (S2, the GO/DEGRADED bars carry no haircut for the repository's own 70-80 % dissipation figure — defect is in the unfired branches), AUDIT-B-InsiderExperiment-8 (S3, 82 bp × 60-70 % decay gives 24.6-32.8 bp, not the registered 30-40 bp band — a lower band fires BLOCKED a fortiori), AUDIT-B-InsiderExperiment-3 (S3, the MDE is a 50 %-power quantity; at 80 % power the primary is 69.14 bp), AUDIT-B-InsiderExperiment-12 (S3, OVER_CLOSED, the fixed language omits the disclosed Section 14.3 upward bias; bounding the beta channel still gives 47.15 bp, above the bar).

**A4. Power gate, 21-session value-weighted secondary hold.**
- Kind: **thresholded negative** (non-verdict-bearing)
- Deciding figures (n): MDE 81.4849 bp per month; n = 2,513 sessions, VIF 0.9667, N_eff 2,599.7, TE 15.7032 %
- file:line: reports/stage_a1/power.json:24-44 (MDE at :33) and the results table REGISTRATION.md:713
- Bar + registration date: "**One month (21 sessions) and three months (63 sessions) as registered secondaries.** Labelled, reported, and non-verdict-bearing." — REGISTRATION.md:368-369; `secondary_hold_sessions=(21, 63)` at src/insider/config.py:132. Registered `398755b`, 18:38 local.
- Amendments touching the bar: none. Data existed? No.
- Corrections applied: none.
- Framing: reported in the Section 15.5 table (REGISTRATION.md:710-715) and nowhere used to fire a verdict; Section 10 (REGISTRATION.md:474-476) labels it non-verdict-bearing before measurement.

**A5. Power gate, 63-session value-weighted secondary hold.**
- Kind: **thresholded negative** (non-verdict-bearing)
- Deciding figures (n): MDE 57.3398 bp per month; n = 2,563 sessions, VIF 0.8606, N_eff 2,978.2, TE 11.8273 %
- file:line: reports/stage_a1/power.json:45-65 (MDE at :54) and REGISTRATION.md:714
- Bar + registration date: as A4 — REGISTRATION.md:368-369, src/insider/config.py:132, `398755b` 18:38 local.
- Amendments touching the bar: none. Data existed? No.
- Corrections applied: none.
- Framing: as A4.

**A6. Power gate, 126-session equal-weighted secondary weighting — the DEGRADED number that was not promoted.**
- Kind: **qualified positive**
- Deciding figures (n): MDE 34.2897 bp per month, inside the registered DEGRADED band 20-40; n = 2,581 sessions, VIF 0.9224, N_eff 2,798.1, sd 43.1862 bp, TE 6.8556 %, effective names 66.9 against the primary's 29.7
- file:line: reports/stage_a1/power.json:66-86 (MDE at :75); REGISTRATION.md:715, :764, :850-854; DECISIONS.md:314-343; progress.md:40-45
- Bar + registration date: DEGRADED row "MDE between 20 and 40 bp per month" — REGISTRATION.md:42; equal weighting registered as **secondary** at REGISTRATION.md:387 (`398755b`, 18:38) and as non-verdict-bearing at REGISTRATION.md:474-476, both before the corpus was built at 18:47 and before the gate ran at 19:11.
- Amendments touching the bar: none. Data existed? No.
- Corrections applied: none.
- Framing: "**The equal-weighted secondary would have fired DEGRADED at 34.29 bp.** It was registered as non-verdict-bearing in Section 10 before measurement and it is not promoted." (REGISTRATION.md:764-767); the reopening boundary at REGISTRATION.md:865-874 and ADR-011 (DECISIONS.md:314-343); progress.md:51-55. `InsiderExperiment.md` sound item 11 confirms from source that `insider.power.report._plan` fires the gate on `cfg.primary_weighting` only (src/insider/power/report.py:23-28, 73-74, 106) and calls ADR-011 "a stronger disclosure than I expected to find". `InsiderExperiment.md` AUDIT-B-InsiderExperiment-3 notes that at 80 % power this secondary would have been BLOCKED too (48.03 bp), which weakens the DEGRADED narrative rather than the verdict.

**A7. Newey-West bandwidth sensitivity, the registered lag grid.**
- Kind: **shipped** (registered sub-test)
- Deciding figures (n): MDE 50.1903 / 49.3543 / 49.1057 / 49.5319 bp at lags 5 / 21 / 63 / 126 on the primary series (n = 2,581 sessions each)
- file:line: reports/stage_a1/power.json:88-113; REGISTRATION.md:721-723
- Bar + registration date: registered lag 21 with the grid 5, 21, 63, 126 reported beside it — REGISTRATION.md:457-465; `newey_west_lags=21`, `newey_west_lag_grid=(5, 21, 63, 126)` at src/insider/config.py:150-151. Registered `398755b`, 18:38 local.
- Amendments touching the bar: none. Data existed? No.
- Corrections applied: none.
- Framing: "The verdict does not turn on the bandwidth choice." (REGISTRATION.md:722-723). `InsiderExperiment.md` sound item 1 reproduces the whole grid from the stored primitives and states the claim is correct.

**A8. Verdict rows V1-V6 and V8: registered, never fired.**
- Kind: **open**
- Deciding figures (n): none — no abnormal return was computed; the realized alpha stays sealed in `var/insider_sealed.db`
- file:line: REGISTRATION.md:435-444 (V1 :437, V2 :438, V3 :439, V4 :440, V5 :441, V6 :442, V8 :444); "V3 and V7 are different findings and are never reported as the same one" REGISTRATION.md:446-448
- Bar + registration date: the whole table "Written now, before any measurement. Every row is a registered outcome." — REGISTRATION.md:433. Registered `398755b`, 18:38 local.
- Amendments touching the bar: none. Data existed? No.
- Corrections applied: none.
- Framing: "**It is not a null on the hypothesis.** … Verdict row V3, a measured null, is not what fired. Row V7 fired" (REGISTRATION.md:771-774, restated REGISTRATION.md:889-891). `InsiderExperiment.md` sound item 16 looked specifically for the V3/V7 merge and reports it is not there, including in progress.md's family record (progress.md:108-113).

---

## B. Registered classification rules (Section 3) and Section 4, with their measured costs

**B1. Section 3.1, purchases only.**
- Kind: **shipped**
- Deciding figures (n): charged inside `filtered_code` (see B2); no separate acquisitions tally is published
- file:line: REGISTRATION.md:222-223
- Bar + registration date: "The rule admits acquisitions and nothing else." REGISTRATION.md:223; registered `398755b`, 18:38 local.
- Amendments: none. Data existed? No.
- Corrections applied: none. A registered mutation ("a sale is admitted past the purchases-only filter") was produced and the guard fired — reports/stage_a1/mutations.json:21-29.
- Framing: not separately framed in the report; carried by the Section 15.2 funnel.

**B2. Section 3.2, transaction code P only.**
- Kind: **shipped**
- Deciding figures (n): `filtered_code` 2,578,217 of 2,876,095 intake (89.64 %), split across 17 sub-codes (largest: S 840,589; A 605,688; F 471,031; M 439,744)
- file:line: REGISTRATION.md:622; reports/stage_a1/corpus.json:17-33
- Bar + registration date: REGISTRATION.md:225-228; registered `398755b`, 18:38 local.
- Amendments: none. Data existed? No.
- Corrections applied: none.
- Framing: Section 15.2 funnel, REGISTRATION.md:613-628. `InsiderExperiment.md` sound item 4 verifies the 17 sub-codes sum exactly to 2,578,217 and the whole funnel sums to the stated intake.

**B3. Section 3.3, officers and directors only — the strict ten-percent-owner reading.**
- Kind: **shipped**
- Deciding figures (n): `filtered_role` 131,222 total (4.56 %), of which `tenpercentowner_also_titled` **46,706** — 51 % of role rejections and roughly ten times the surviving corpus; `tenpercentowner` 46,958; `roles_other` 32,536; `roles_none` 5,022
- file:line: REGISTRATION.md:623, :636-639, :652-654; reports/stage_a1/corpus.json:37-40
- Bar + registration date: "A filer who is both an officer and a ten percent owner is excluded … This is the strict reading and it is the more costly one. The count it removes is reported separately … so a reader can see what the strict reading cost without a second verdict path existing." REGISTRATION.md:234-240; registered `398755b`, 18:38 local, before any count existed.
- Amendments: none. Data existed? No.
- Corrections applied: none.
- Framing: "**Three facts this table settles**" REGISTRATION.md:650-654 — the cost is stated at its full size rather than minimised. No `InsiderExperiment.md` finding.

**B4. Section 3.4, the Cohen-Malloy-Pomorski routine/opportunistic rule.**
- Kind: **shipped**
- Deciding figures (n): `filtered_routine/routine` 156 charged in the funnel; `routine_labels` over all classified transactions: opportunistic 4,167, routine 160, insufficient_history 2,471
- file:line: REGISTRATION.md:644; reports/stage_a1/corpus.json:42, :57-61
- Bar + registration date: "An insider is **routine** if she traded in the same calendar month for at least three consecutive prior years." REGISTRATION.md:245-247; "Computed purely look-back." REGISTRATION.md:249-251; `398755b`, 18:38 local.
- Amendments touching the bar: **none declared**, but the rule's implementation changed after data existed. `InsiderExperiment.md` AUDIT-B-InsiderExperiment-5 (S3, PROCESS) shows `git diff cb17046 672b343 -- src/insider/corpus/routine.py` reordering `classify` so the routine pattern is tested before the history gate, at 2026-08-25 19:11:45 local — **data existed (corpus built 18:47)** — with no Section 17 amendment, and REGISTRATION.md:258-260 left describing the superseded rule.
- Corrections applied: **ADR-008** (DECISIONS.md:226-254) records the reordering, its cause (a slack guard fixture) and its impact: "One transaction moved from `insufficient_history` to `routine`. The qualifying set is unchanged at 4,585 … and the minimum detectable effect is unchanged at 49.35".
- Framing: progress.md:68-73 and :275-283 present the reordering as a defect found and fixed; ADR-012 (DECISIONS.md:376-384) records how. `InsiderExperiment.md` sound item 3 independently checked for look-ahead in this rule and found none (`src/insider/corpus/routine.py:75-78`, guarded at tests/test_guards.py:397).

**B5. Section 3.4, `insufficient_history` as a third recorded state.**
- Kind: **shipped**
- Deciding figures (n): `filtered_routine/insufficient_history` 2,057 of 2,876,095; front-truncation series by year 2016 449, 2017 257, 2018 256, 2019 188, 2020 174, 2021 110, 2022 296, 2023 84, 2024 95, 2025 96, 2026 38 (sums to 2,057)
- file:line: REGISTRATION.md:643, :699-704; reports/stage_a1/corpus.json:41, :62-78
- Bar + registration date: "**Three years of trading history is required to classify at all.** … It is not routine and it is not opportunistic, and it is recorded as its own sub-reason inside `filtered_routine` so the two are never merged in the data." REGISTRATION.md:258-266; registered `398755b`, 18:38 local. The truncation was predicted in advance: "That truncates the usable window at the front and the count is reported in Task 4." REGISTRATION.md:266.
- Amendments: see B4 (the ordering change moved one transaction into `routine`).
- Corrections applied: ADR-008's one-transaction move; the artifact carries the corrected 2018 value 256.
- Framing: Section 15.4 REGISTRATION.md:699-704. `InsiderExperiment.md` AUDIT-B-InsiderExperiment-11 (S3, INTERNAL_INCONSISTENCY) finds the prose quotes 257 for 2018 where the artifact says 256, and quotes the only four years for which the series falls monotonically (2022 is 296, above both 2017 and 2018).

**B6. Section 3.5, cluster buys.**
- Kind: **shipped**
- Deciding figures (n): 773 clusters found (`clusters_found`), 106 distinct issuers behind them per `InsiderExperiment.md` AUDIT-B-InsiderExperiment-2
- file:line: REGISTRATION.md:268-270; reports/stage_a1/corpus.json:171
- Bar + registration date: "Three or more distinct filer CIKs making P-code purchases at the same issuer within a rolling five-day window, counted in calendar days as the closed interval from the anchor date to the anchor date plus four." REGISTRATION.md:268-270; `398755b`, 18:38 local.
- Amendments: none. Data existed? No.
- Corrections applied: none.
- Framing: Section 15.4 REGISTRATION.md:693. `InsiderExperiment.md` AUDIT-B-InsiderExperiment-2 (S2) establishes from `src/insider/corpus/cluster.py:76-95` that the 773 are **anchored windows**, not distinct cluster events, and that the 209 rejections merge to 36 distinct events at 10 issuers.

**B7. Section 3.6, the Johnsen programmatic-event filter and the 10,000 USD floor.**
- Kind: **shipped** (a registered refusal, demonstrated by producing it)
- Deciding figures (n): 209 of 773 clusters rejected; `filtered_programmatic/johnsen_same_date_price` 274 transactions charged; `below_dollar_floor` 2,023; `flagged_10b5_1` 65; `filtered_programmatic` total 2,362 (0.08 %)
- file:line: REGISTRATION.md:641, :625, :693-697; reports/stage_a1/corpus.json:34-36, :171-172; the produced artifact reports/stage_a1/refusals.md:6-21 (the Darden cluster, 12 filers, every buy at 58.50, modal fraction 1.00 against a 0.80 threshold)
- Bar + registration date: "A cluster is rejected when a single date-and-price pair accounts for eighty percent or more of the contributing buys." REGISTRATION.md:272-274; `398755b`, 18:38 local. Standing guard 4, "Refusals are demonstrated by producing them, never asserted" — CLAUDE.md:44-46.
- Amendments: none. Data existed? No.
- Corrections applied: none.
- Framing: Section 15.4 "The refusals, produced rather than asserted" REGISTRATION.md:688-697. `InsiderExperiment.md` AUDIT-B-InsiderExperiment-2 (S2, INTERNAL_INCONSISTENCY) challenges the "209 of 773 clusters" phrasing (anchored windows, not events; 74 % of the rejections are one issuer, SPG) and notes the registered rule is stated per cluster while the implementation charges a buy only if it appears in no surviving window (`cluster.py:103`, consumed at `corpus/build.py:376-378`).

**B8. Section 3.7, 10b5-1 exclusion with absence as a recorded state.**
- Kind: **shipped**
- Deciding figures (n): 65 transactions charged as 10b5-1 flagged; the box is **absent for 3,350 of the 4,585** qualifying events (73.1 %); the XML sample shows the flag not reported in 19 of 25 documents
- file:line: REGISTRATION.md:642, :662-666; reports/stage_a1/corpus.json:35, :169; reports/stage_a1/validation.json:474-477
- Bar + registration date: "An **unreported** 10b5-1 box is a recorded absence and admits the transaction. … Treating its absence before then as an affirmative 'not 10b5-1' would read a decade of filings as carrying a fact they do not carry." REGISTRATION.md:284-288; `398755b`, 18:38 local. Standing guard 1, CLAUDE.md:34-36.
- Amendments: none. Data existed? No.
- Corrections applied: none.
- Framing: "Reading those 3,350 as affirmatively not-10b5-1 would have been a fabrication across a decade of filings." REGISTRATION.md:665-666. `InsiderExperiment.md` sound item 18 verifies the handling in `src/insider/corpus/classify.py:80-89` and `src/insider/absence.py` and reports it sound.

**B9. Section 3.8, what qualifies — the opportunistic-or-surviving-cluster disjunction.**
- Kind: **shipped**
- Deciding figures (n): 4,585 qualifying events = 4,167 opportunistic + 418 routine/insufficient-history buys rescued by surviving cluster membership (sound item 18, from the live store, UNANCHORED)
- file:line: REGISTRATION.md:290-293; reports/stage_a1/corpus.json:2, :57-61
- Bar + registration date: "A transaction is a qualifying event when it clears 3.1 through 3.3, sits at a universe issuer, clears 3.6 and 3.7, and is **either** placed by an opportunistic insider **or** belongs to a cluster that survives the Johnsen filter." REGISTRATION.md:290-293; `398755b`, 18:38 local.
- Amendments: none. Data existed? No.
- Corrections applied: ADR-013's surrogate key (A1) governs the count.
- Framing: Section 15.1 REGISTRATION.md:592-596. `InsiderExperiment.md` sound item 18 checks the composition and reports it consistent.

**B10. Section 4, the registered narrowing to the liquid-500 universe.**
- Kind: **shipped**
- Deciding figures (n): `outside_universe` 148,883 rejected against 9,160 that reached the universe filter and passed — **only 5.8 %** of qualifying-shaped insider purchases happen at a liquid-500 name; 94.2 % happen outside
- file:line: REGISTRATION.md:624, :656-660; reports/stage_a1/corpus.json:43; DECISIONS.md:120-125
- Bar + registration date: "**This is a registered narrowing of scope, not an oversight.** … It deliberately excludes the small and microcap names where the literature reports the insider effect concentrates" REGISTRATION.md:312-317; universe `U-LIQ-500-stk-w60-m40-p5` at REGISTRATION.md:303-306; `398755b`, 18:38 local, before any count existed.
- Amendments: none. Data existed? No.
- Corrections applied: none.
- Framing: "The consequence is stated plainly: **a negative here does not refute the literature.**" REGISTRATION.md:326-329, restated at closure REGISTRATION.md:776-781 and :893-896, and in ADR-004 (DECISIONS.md:132-135). `InsiderExperiment.md` sound item 17 records this as "the opposite of the failure I was looking for": registered in advance, cost measured rather than estimated, correct conclusion drawn.

---

## C. Registered design choices and their measured outcomes

**C1. Section 5, calendar-time portfolio and the universe benchmark.**
- Kind: **positive** (a registered design choice vindicated by the measurement)
- Deciding figures (n): realized variance inflation 0.8993 on the primary series — **below one**, so N_eff 2,869.9 exceeds the 2,581 raw sessions, against NPDExperiment's 427 evaluable days cut to 125.6 effective
- file:line: reports/stage_a1/power.json:7-8; REGISTRATION.md:725-729; DECISIONS.md:158-161
- Bar + registration date: "**Calendar-time portfolio.** One portfolio return per day" REGISTRATION.md:335-336, with the event-time BHAR alternative rejected in advance at REGISTRATION.md:344-349; `398755b`, 18:38 local.
- Amendments touching the bar: **none declared**, but `InsiderExperiment.md` AUDIT-B-InsiderExperiment-5 shows the registered `Config.benchmark_id="U-LIQ-500-VW"` field deleted at `672b343`, 2026-08-25 19:11:45 local — **data existed** — with no numbered amendment, against src/insider/config.py:8-9's own rule. Impact on results recorded by the draft as nil (the field had no enforcement site, which is why the standing guard forced its removal).
- Corrections applied: none to the figure.
- Framing: "The calendar-time structure did what Section 5 chose it to do." REGISTRATION.md:729; ADR-005 "Measured outcome" DECISIONS.md:158-161. `InsiderExperiment.md` sound item 1 reproduces the VIF and N_eff exactly.

**C2. Section 6, the six-month primary hold and the entry rule.**
- Kind: **shipped**
- Deciding figures (n): 126 sessions primary, entry at the close of the first session strictly after the filing date; realized filing lag over n = 4,585 events: p50 1 day, 73.0 % within two calendar days, 95.9 % within four, 91 events beyond ten days, max 1,988, mean 9.52
- file:line: REGISTRATION.md:363-381, :672-686; src/insider/config.py:131, :135; reports/stage_a1/corpus.json:79-168
- Bar + registration date: "**Six months primary**, implemented as 126 trading sessions." REGISTRATION.md:363; `398755b`, 18:38 local.
- Amendments: none. Data existed? No.
- Corrections applied: none.
- Framing: the tension is disclosed rather than resolved — "**a longer hold cuts cost drag and dilutes signal.** … Six months is registered before any number is seen precisely because that trade-off cannot be settled by looking." REGISTRATION.md:371-375; "Entry is driven by the filing date, so a late filing produces a late entry rather than a look-ahead." REGISTRATION.md:685-686. `InsiderExperiment.md` sound item 5 reconstructs every published lag statistic from `corpus.json` and matches all but p99 (228 by nearest rank against the published 230).

**C3. Section 7, value-weighted primary and equal-weighted secondary.**
- Kind: **shipped**
- Deciding figures (n): primary book 71.909 mean names / 29.731282 effective names / top-1 weight 14.9323 % / top-5 33.7911 % / correlation to benchmark 0.903981; equal-weighted 66.9 effective / top-1 1.9 % / top-5 8.5 % / correlation 0.953
- file:line: reports/stage_a1/portfolio.json:7, :19-28; REGISTRATION.md:747-750, :839-842; progress.md:31-34
- Bar + registration date: "**Value-weighted primary. Equal-weighted secondary.** Wide book, not concentrated." REGISTRATION.md:387-391; `primary_weighting="value_weighted"` at src/insider/config.py:136-137; `398755b`, 18:38 local, before any number was visible.
- Amendments: none. Data existed? No.
- Corrections applied: none.
- Framing: the registration records the irony against itself — "The primary chosen to avoid concentration was concentrated by its weighting rather than by its name count." REGISTRATION.md:860-863, DECISIONS.md:340-343, progress.md:47-49. `InsiderExperiment.md` AUDIT-B-InsiderExperiment-7 (S3, INTERNAL_INCONSISTENCY) finds the "71.9 names" quoted in the closure verdict is the pre-membership-filter figure from `MembershipSeries.mean_width()` (src/insider/portfolio/membership.py:46-54) while the book that produced the 49.35 bp averages **66.93** (power.json:16), a 7.0 % difference matching ADR-009's own 7.4 % drop.

**C4. Section 8, the operator's measured cost model.**
- Kind: **shipped**
- Deciding figures (n): one-way spread 15.8 / 50.0 bp, round trip 32 / 100 bp, amortized over 6.0 trading months to 5.3333 / 16.6667 bp per month; net band 13.3333 to 34.6667 bp per month
- file:line: REGISTRATION.md:404-421; src/insider/config.py:139-142; reports/stage_a1/power.json:124-131
- Bar + registration date: "**The pessimistic 100 bp round trip is the primary bar. The optimistic 32 bp is a registered secondary.**" REGISTRATION.md:409-411; `398755b`, 18:38 local.
- Amendments: none. Data existed? No.
- Corrections applied: none.
- Framing: "`insider.cost` computes this rather than asserting it." REGISTRATION.md:421-422. `InsiderExperiment.md` sound item 8 verifies the arithmetic and adds that `insider/cost.py:48-57` states plainly that the low end is the number a verdict is read against, "so the appearance of the optimistic bar in the band's upper end is registered rather than smuggled".

**C5. Section 10, inference: t 2.0, day clustering, one primary contrast.**
- Kind: **shipped**
- Deciding figures (n): critical value 2.0; a single pre-registered primary contrast, so no family correction; secondaries labelled non-verdict-bearing before computation
- file:line: REGISTRATION.md:454-479 (secondaries :474-476, critical value :478-479); src/insider/config.py:147
- Bar + registration date: "**Critical value 2.0.** Registered, two-sided, applied identically to the power computation in Stage A.1 and to the inference in Stage B." REGISTRATION.md:478-479; `398755b`, 18:38 local.
- Amendments: none. Data existed? No.
- Corrections applied: none.
- Framing: "the secondaries are labelled non-verdict-bearing before any of them is computed, so they cannot be promoted to the primary after the fact." REGISTRATION.md:470-472. `InsiderExperiment.md` AUDIT-B-InsiderExperiment-3 (S3, STATISTICAL) records that no power level (β, 1−β) is registered anywhere, so `t_critical * se` is a 50 %-power quantity and every "can/cannot detect" statement inherits that.

**C6. Section 0.4, the derivation of the 1,000-event floor.**
- Kind: **qualified positive**
- Deciding figures (n): planning N 2,520, VIF 1.5, N_eff 1,680; inverted bars 19.52 bp / 3.10 % and 39.04 bp / 6.20 %; required book width 23.4 and 93.7 names at σ = 30 %; 468 / 1,000 / 1,875 events at H × λ with H = 126; expected TE 4.24 % and MDE ≈ 27 bp at the floor; coverage penalty 11.8 % = √1.25
- file:line: REGISTRATION.md:82-146 (the three reasons at :126-140)
- Bar + registration date: "**The floor is set at 1,000 qualifying events**, which is a book of about 50 names." REGISTRATION.md:125-126; `fbfc74e`, 18:34 local.
- Amendments: none. Data existed? No.
- Corrections applied: none.
- Framing: partially self-disclosed at REGISTRATION.md:754-757 ("the realized book carries 29.7 with residuals that are not independent, because insider buying clusters by sector during stress"). `InsiderExperiment.md` sound item 7 confirms **the section's own arithmetic is internally correct at every step**; AUDIT-B-InsiderExperiment-4 (S3, UNSUPPORTED_POSITIVE) records that both models were falsified by the same run — H × λ over-predicted book width by 3.43× (229.2 predicted against 66.93 realized) and σ/√k under-predicted tracking error by ~1.85× — so CORPUS-GO carries no information about whether the design could be measured. Added at consolidation: REGISTRATION.md:128-131 discloses the distinct-issuer risk in advance and says "The margin absorbs that", but the registered margin was 1,000/468 = 2.14x against a realized 3.43x shortfall, and at the realized event-to-width ratio the registered 1,000-event floor would have produced a **14.6-name book** against the **23.4 names** Section 0.4's own table (REGISTRATION.md:112) gives as the BLOCKED floor.

**C7. Section 14, the three deviations recorded at registration.**
- Kind: **shipped**
- Deciding figures (n): 14.1 — the per-filing-XML route would need >69 hours of wall clock at 8 req/s over ~2 M documents, so 53 quarterly data sets carry the corpus; 14.2 — value weighting by point-in-time median dollar volume, direction stated as moving the MDE toward BLOCKED; 14.3 — Stage A.1 dispersion measured against the universe benchmark, an upper bound on the Stage B figure
- file:line: REGISTRATION.md:556-565, :567-576, :578-583; DECISIONS.md:40-74 (ADR-002), :197-222 (ADR-007), :29-32 (ADR-001 cost)
- Bar + registration date: "Recorded before measurement, each with the arithmetic that forced it." REGISTRATION.md:554; `398755b`, 18:38 local.
- Amendments: none. Data existed? No.
- Corrections applied: none.
- Framing: "**It is conservative in three registered directions.**" REGISTRATION.md:783-788, with "The Section 14.3 conservatism is the only one large enough to matter" at :790-796. `InsiderExperiment.md` AUDIT-B-InsiderExperiment-12 (S3) records that this disclosure is clear and defensible but absent from the four places the fixed verdict language appears, and bounds the beta channel at 47.15 bp — still above the 40 bp bar. `InsiderExperiment.md` AUDIT-B-InsiderExperiment-10 (S3) records that ADR-002's XML validation sample is drawn only from survivors.

**C8. ADR-009, dropping a name that leaves the universe mid-hold.**
- Kind: **shipped**
- Deciding figures (n): 13,750 name-sessions removed from the primary series, about 7.4 % of held name-sessions
- file:line: DECISIONS.md:258-280 (figure at :264-265); reports/stage_a1/power.json:118 and portfolio.json:17 (`"not_priced": 13750`); src/insider/portfolio/returns.py:189-210
- Bar + registration date: "**Status.** Accepted with a recorded limitation, Stage A.1, 2026-08-25." DECISIONS.md:260. Not a registered bar; an ADR recorded during A.1.
- Amendments: none. Data existed? The ADR is written against the realized figure, so yes — but it changes no registered bar.
- Corrections applied: none.
- Framing: the limitation is volunteered — "That is a survivorship leak in the first moment. … dropping crashed names reduces dispersion, which lowers the minimum detectable effect and moves the verdict toward GO. The gate fired BLOCKED, so the leak makes the finding conservative rather than fragile." DECISIONS.md:270-280. `InsiderExperiment.md` AUDIT-B-InsiderExperiment-7 uses the same 7.4 % to explain the 71.9 vs 66.9 gap and notes nothing says the verdict narrative's 71.9 is the pre-drop figure.

---

## D. Shipped artifacts

**D1. `reports/stage_a1/corpus.json`** — the corpus gate artifact.
- Kind: **shipped**
- Deciding figures (n): 4,585 qualifying events; by-year 2016-2026 (263, 409, 531, 462, 728, 298, 504, 508, 418, 365, 99); the full 28-row attrition map; 7 prefunnel rows; routine labels; unclassifiable by year; lag distribution; `flag_absent_events` 3,350; `clusters_found` 773; `clusters_rejected` 209; `session_coverage` 0.99541; `mean_book_width` 71.909; verdict CORPUS-GO
- file:line: reports/stage_a1/corpus.json:1-177
- Bar + registration date: fired by `insider.section0.fire_corpus_gate` (REGISTRATION.md:150-153), bars registered `fbfc74e` 18:34 local.
- Amendments: none.
- Corrections applied: ADR-013's surrogate key; per `InsiderExperiment.md` AUDIT-B-InsiderExperiment-6 the artifact carries the **corrected** by-year table (sums to 4,585) while REGISTRATION.md:601-608 carries the pre-correction one (4,542).
- Framing: Section 15.1-15.4 transcribes it, REGISTRATION.md:592-704.

**D2. `reports/stage_a1/port.json`** — the AiTrader read-only boundary record.
- Kind: **shipped**
- Deciding figures (n): 2,615 sessions, 124 formations, 1,218 distinct symbols, 2,713,496 bars copied; `analysis_bars.db` sha256 `d599ccf0…e924` identical before and after; `backtest/universe.py` sha256 `8188eea0…5529` identical before and after; `unchanged: true`
- file:line: reports/stage_a1/port.json:1-12
- Bar + registration date: "Read-only source paths, and only these two … hashed before and after." CLAUDE.md:53-56; registered in the scaffold commit `fbfc74e`.
- Amendments: none. Data existed? No.
- Corrections applied: none.
- Framing: progress.md:308-315 "Boundaries held", re-verified at closure progress.md:135-138. `InsiderExperiment.md` sound item 15 confirms `port.json` records both source hashes unchanged across the read.

**D3. `reports/stage_a1/portfolio.json`** — the calendar-time book diagnostics for all four series.
- Kind: **shipped**
- Deciding figures (n): per series, sessions with a return, membership coverage, book-width mean and percentiles, drop reasons, and the diagnostics block (sd_portfolio_daily 0.014065, sd_benchmark_daily 0.014575, corr 0.903981, top-1 0.149323, top-5 0.337911, effective names 29.731282 for the primary)
- file:line: reports/stage_a1/portfolio.json:1-113 (primary block :2-29)
- Bar + registration date: no bar; a reported artifact required by Section 15.6.
- Amendments: none.
- Corrections applied: none.
- Framing: Section 15.6 table REGISTRATION.md:747-750 and Section 17.3 REGISTRATION.md:839-842. `InsiderExperiment.md` AUDIT-B-InsiderExperiment-7 notes the artifact publishes the raw-membership mean (71.909) beside priced-series percentiles (p50 67, p90 89) without labelling the difference (portfolio.json:7-12, built at src/insider/portfolio/build.py:52-64).

**D4. `reports/stage_a1/power.json`** — the power gate artifact.
- Kind: **shipped**
- Deciding figures (n): four series with n, VIF, N_eff, sd, TE, SE and MDE; the four-point Newey-West grid; `dropped_primary` (empty_book 12, no_benchmark 0, no_finite_member_return 22, not_priced 13750); the registered bands; verdict BLOCKED; `stage_b_authorized: false`
- file:line: reports/stage_a1/power.json:1-137
- Bar + registration date: fired by `insider.section0.fire_power_gate` (REGISTRATION.md:150-153); bars `fbfc74e` 18:34 local.
- Amendments: none.
- Corrections applied: none.
- Framing: Section 15.5 REGISTRATION.md:706-738. `InsiderExperiment.md` sound item 1 reproduces every published digit from `var/insider_dispersion.db`; sound item 2 verifies the stored series are centred (`math.fsum` ≈ 1e−16) and that `insider.power` imports only `config`, `paths` and stdlib.

**D5. `reports/stage_a1/validation.json`** — the three-route SEC validation.
- Kind: **shipped**
- Deciding figures (n): 53 quarters of index-vs-dataset ratios, 2.043 to 2.140 (n = 5,077,629 index rows against 2,440,873 dataset documents, per `InsiderExperiment.md` AUDIT-B-InsiderExperiment-10); 25 per-filing XML field checks, `xml_tally` agrees 25, `flag_not_reported_in_xml` 19; 25 submissions ticker checks, 21 symbols present
- file:line: reports/stage_a1/validation.json:2-321 (index), :322-473 (XML checks), :474-477 (tally), :478-692 (ticker check)
- Bar + registration date: "**What would overturn it.** A disagreement in the XML sample, or a full-index ratio that moved across quarters" — ADR-002, DECISIONS.md:72-74, Stage A.1 2026-08-25.
- Amendments: none.
- Corrections applied: none.
- Framing: ADR-002 DECISIONS.md:56-70 and Section 14.1 REGISTRATION.md:556-565. `InsiderExperiment.md` sound item 10 confirms every figure is real and that the 21-of-25 ticker result is the evidence ADR-007 cites for rejecting the XBRL weighting route. `InsiderExperiment.md` AUDIT-B-InsiderExperiment-10 (S3, STATISTICAL) records that the 25-document sample is drawn only from the 4,585 survivors (src/insider/corpus/validate.py:115-123), so it cannot detect a purchase the SEC parse dropped, and puts an 11.29 % one-sided 95 % bound on the residual disagreement rate; DECISIONS.md:69-70 discloses the sampling but not the selection on survival. `InsiderExperiment.md` AUDIT-B-InsiderExperiment-9 records ADR-002's "53 files totalling about 750 MB" (DECISIONS.md:58) against a measured 570 MB.

**D6. `reports/stage_a1/refusals.md`** — refusals produced rather than asserted.
- Kind: **shipped**
- Deciding figures (n): two serialized refusal blocks — a Johnsen-rejected cluster (DRI, 2020-04-23 to 2020-04-27, size 12, 12 distinct filers, modal date-price fraction 1.0 against threshold 0.8) and an `insufficient_history` insider with zero years of look-back
- file:line: reports/stage_a1/refusals.md:1-236 (Johnsen block :6-21; second block :113-121)
- Bar + registration date: standing guard 4, "Refusals are demonstrated by producing them, never asserted" — CLAUDE.md:44-46; scaffold commit `fbfc74e`.
- Amendments: none.
- Corrections applied: none.
- Framing: Section 15.4 REGISTRATION.md:688-704. `InsiderExperiment.md` AUDIT-B-InsiderExperiment-2 uses the artifact itself as evidence that the two shipped Johnsen blocks are the same underlying Darden event under two anchors (cluster_id 369 size 12 and 370 size 11, identical window).

**D7. `reports/stage_a1/mutations.json`** — five registered mutations against real source.
- Kind: **shipped**
- Deciding figures (n): 5 mutations, each with `guard_failed_when_mutated: true` and `guard_green_when_restored: true` and a named failing test — power module returns a mean; non-evaluator reads the sealed store; a sale admitted past purchases-only; a routine insider admitted past the three-year rule; the EDGAR throttle loses its enforcement site
- file:line: reports/stage_a1/mutations.json:1-50 (`final_suite` at :49)
- Bar + registration date: standing guards 1-5 at CLAUDE.md:32-49; `make guards` at CLAUDE.md:100.
- Amendments: none.
- Corrections applied: ADR-012 defects 1 and 3 (see E3, E4) both surfaced here.
- Framing: progress.md:57-82 calls this "the three defects, the most reusable finding". `InsiderExperiment.md` sound item 14 confirms the harness edits real source, restores it and asserts byte equality (`scripts/mutations.py:143-155`). `InsiderExperiment.md` AUDIT-B-InsiderExperiment-13 (S4, PROVENANCE) records that `final_suite` stores a 33-dot pytest progress line, not a result line, so the shipped artifact does not evidence the "106 tests" claim.

**D8. The four standing guards and the eight recorded call states.**
- Kind: **shipped**
- Deciding figures (n): 4 guards (CLAUDE.md lists 5 including the call-state rule); 8 call states; `tests/test_guards.py` fails if any config field has no enforcement site, if any power dataclass grows a first-moment field, or if any module outside `insider.eval.evaluator` names the sealed store
- file:line: CLAUDE.md:32-49; REGISTRATION.md:524-548 (the eight states, table at :529-538); REGISTRATION.md:490-493
- Bar + registration date: scaffold commit `fbfc74e`, 2026-08-25 18:34 local; ported by copying per progress.md:219-222.
- Amendments: none. Data existed? No.
- Corrections applied: guard 2 rewritten to walk the parse tree (E3).
- Framing: progress.md:219-222; the funnel and sub-reason tables at REGISTRATION.md:618-644 are the states in use. `InsiderExperiment.md` sound item 4 verifies the whole funnel is internally exact (8,613 + 2,578,217 + 131,222 + 148,883 + 2,362 + 2,213 + 0 + 4,585 = 2,876,095), every sub-reason sums to its parent and every published share rounds correctly.

**D9. ADR-006, the seal architecture.**
- Kind: **shipped**
- Deciding figures (n): two stores; `read_sealed_returns` defined once; four enforcing guards; `insider.portfolio.returns` writes both and reads neither
- file:line: DECISIONS.md:165-193; REGISTRATION.md:155-159, :490-493; CLAUDE.md:20-24; src/insider/eval/evaluator.py:33
- Bar + registration date: Accepted Stage A.1, 2026-08-25 (DECISIONS.md:167); the load-bearing rule at CLAUDE.md:10-24.
- Amendments: none.
- Corrections applied: none.
- Framing: the limits are stated rather than overclaimed — "It is not cryptographic. … The seal prevents the accident, not the intent, and that is the failure mode that actually occurred in the predecessor." DECISIONS.md:188-193. `InsiderExperiment.md` sound item 2 verifies the architecture in code and states the auditor did not open `var/insider_sealed.db`; two of the five registered mutations exercise it (mutations.json:3-20).

**D10. The fetch campaign: 214 wire requests, 2.78 GB, zero non-200, zero dollars.**
- Kind: **shipped**
- Deciding figures (n): 53 quarterly data sets covering 2013q1-2026q1; 214 wire requests; 2,783,280,665 bytes on the wire and the same on disk; 0 non-200 responses; 8 req/s throttle against the SEC's stated 10; ledger `ledgers/fetch.jsonl` 684 rows (untracked, UNANCHORED, read 2026-09-04T05:39Z per `InsiderExperiment.md`)
- file:line: REGISTRATION.md:827-833; progress.md:23-27, :225-227; client behaviour at src/insider/edgar/client.py:76-90
- Bar + registration date: "SEC access only. Zero paid APIs. … throttled to 8 requests per second against the SEC's stated 10 per second ceiling, with a local cache so a re-run never re-fetches." CLAUDE.md:61-64; scaffold commit `fbfc74e`.
- Amendments: none. Data existed? No.
- Corrections applied: none.
- Framing: Section 17.2 REGISTRATION.md:827-833, progress.md:23-27. `InsiderExperiment.md` sound item 9 confirms all 684 rows are status 200, that the client records a row **before** it inspects the status (so a non-200 would appear), that 214 wire requests hit 214 distinct URLs, and that wire bytes equal `du -sb cache/` to the byte. `InsiderExperiment.md` AUDIT-B-InsiderExperiment-9 (S3, STALE_FIGURE) records that the 214/2.78 GB are the whole campaign, not the 53 data sets: 570,492,991 bytes (20.5 %) are the data sets and 2,207,515,405 (79.3 %) the full-index archives.

**D11. `make all`: ruff, ruff format, mypy strict on 56 files, 106 tests.**
- Kind: **shipped**
- Deciding figures (n): 56 source files; **106 tests claimed**; the shipped artifact records only `".................................  [100%]"` — 33 dots, no pass count. The pass count is **not located** in any shipped artifact.
- file:line: progress.md:216-218; reports/stage_a1/mutations.json:49; harness `scripts/mutations.py:118-122, :178-179`; `pyproject.toml:62-68`
- Bar + registration date: "make all lint, type, test" CLAUDE.md:98-100; scaffold commit `fbfc74e`.
- Amendments: none.
- Corrections applied: none.
- Framing: progress.md:217-218 and the commit title of `672b343` ("test: 106 tests green, and five registered mutations that fail the right guard"). `InsiderExperiment.md` AUDIT-B-InsiderExperiment-13 (S4, PROVENANCE) records that the harness did check the return code, so the run was green, but the artifact does not evidence it; the draft's own static count is 96 test functions expanding to ~105.

**D12. The universe port, verified rather than asserted.**
- Kind: **shipped**
- Deciding figures (n): 500 of 500 members reproduced exactly at three formation dates spanning the corpus (2016-04-01, 2021-04-01, 2026-07-01), rank by rank
- file:line: DECISIONS.md:109-112; tests/test_universe_port.py:85-91; pyproject.toml:62-68
- Bar + registration date: "ported by copy from `AiTrader/backtest/universe.py` and verified against the source's own stored membership at three formation dates" DECISIONS.md:109-112, Stage A.1 2026-08-25; boundary rule at CLAUDE.md:53-56.
- Amendments: none.
- Corrections applied: none.
- Framing: ADR-004 DECISIONS.md:105-112. `InsiderExperiment.md` sound item 15 confirms the test re-derives membership from the source bars and that `addopts = "-q --strict-markers"` carries no `-m "not slow"` deselection, so the slow test actually runs in `make test`.

**D13. The Section 0.2 power gate itself, as a transferable artifact.**
- Kind: **shipped**
- Deciding figures (n): three verdict rows with bars at 20 and 40 bp per month, inclusive at the lower edge; fired on `MDE = t · M · s_d / √N_eff`
- file:line: REGISTRATION.md:34-59 (table :39-43, inclusivity :45-46, bar placement :57-59); src/insider/config.py:143-144, :147, :152; src/insider/power/mde.py:54, :66, :70-82
- Bar + registration date: `fbfc74e`, 2026-08-25 18:34 local, before Task 4 computed anything.
- Amendments: none; bars byte-identical from first commit (sound item 12).
- Corrections applied: none.
- Framing: presented as the repository's reusable answer to NPDExperiment's late power finding — REGISTRATION.md:19-32, CLAUDE.md:3-18, ADR-001 DECISIONS.md:8-36. `InsiderExperiment.md` AUDIT-B-InsiderExperiment-1 (S2, STATISTICAL) is the ledger's largest qualification on this artifact: the GO and DEGRADED bars are calibrated against a gross band the same section says is 70-80 % dissipated before this design's registered entry point, and carry no haircut for it, so the defect sits in the branches that did **not** fire. `InsiderExperiment.md` AUDIT-B-InsiderExperiment-3 (S3) adds that the bars are 50 %-power thresholds with no registered power level.

**D14. ADR-012, "a guard that has never failed is not a guard".**
- Kind: **shipped**
- Deciding figures (n): three defects, two of them guards passing vacuously across the entire A.1 suite; the mutation task was the only one to run over its ETA (30 min stated, 32 actual)
- file:line: DECISIONS.md:347-396; progress.md:57-82, :204, :265-290
- Bar + registration date: Accepted Stage Z.1, 2026-08-25 (DECISIONS.md:349); named "the most reusable finding this repository produced".
- Amendments: none.
- Corrections applied: see E3 and E4.
- Framing: the ADR corrects the stage brief against itself and volunteers an unsolved residual — "It catches decoration, not misuse. … this repository did not solve it." DECISIONS.md:365-374. `InsiderExperiment.md` sound item 13 records: "ADR-012's self-correction is exemplary. … I looked for the softer version of that claim and did not find one."

---

## E. Corrections applied

**E1. ADR-008 — the routine pattern is tested before the history gate.**
- Kind: **shipped** (correction)
- Deciding figures (n): one transaction moved from `insufficient_history` to `routine`; qualifying set unchanged at 4,585; MDE unchanged at 49.35 bp
- file:line: DECISIONS.md:226-254 (impact at :245-249); progress.md:275-283; src/insider/corpus/routine.py:74-83
- Bar + registration date: the rule at REGISTRATION.md:245-266, registered `398755b` 18:38 local.
- Amendments touching the bar: **none declared.** The code change landed at `672b343`, 2026-08-25 19:11:45 local — **data existed** (corpus built 18:47) — and REGISTRATION.md:258-260 still describes the superseded ordering (`InsiderExperiment.md` AUDIT-B-InsiderExperiment-5, S3, PROCESS).
- Corrections applied: this row is the correction.
- Framing: disclosed in full in ADR-008 and progress.md, including that the defect was in the reported composition, not the sample.

**E2. ADR-013 — the surrogate key, after a silent merge of 43 events.**
- Kind: **shipped** (correction)
- Deciding figures (n): 43 duplicate purchase lines merged by the composite natural key; build reported 4,585 while the table held 4,542; the build now raises when offered and stored counts diverge
- file:line: DECISIONS.md:400-416 (figures at :404-410); progress.md:84-91, :292-298
- Bar + registration date: not a registered bar; the standing rule it belongs to is guard 1, CLAUDE.md:34-36.
- Amendments: none required.
- Corrections applied: this row is the correction; the artifact `corpus.json:3-15` carries the corrected by-year table.
- Framing: "A silent merge is a synthesized agreement: the count and the store disagreed, and nothing in the pipeline said so." DECISIONS.md:412-416. `InsiderExperiment.md` AUDIT-B-InsiderExperiment-6 (S3) records that REGISTRATION.md:601-608 was never regenerated and still carries the 4,542-summing breakdown beside the 4,585 headline.

**E3. ADR-012 defect 1 — the config-enforcement guard now walks the parse tree.**
- Kind: **shipped** (correction)
- Deciding figures (n): one registered mutation (throttle rate replaced by a literal, key left in a trailing comment) that the text-scanning guard failed to catch; the ported original had six AiTrader Level 1 keys parsed, validated, printed and enforced nowhere
- file:line: DECISIONS.md:356-374; progress.md:62-67, :269-273; reports/stage_a1/mutations.json:39-47
- Bar + registration date: standing guard 2, CLAUDE.md:37-40; scaffold commit `fbfc74e`.
- Amendments: none.
- Corrections applied: this row is the correction; the residual is recorded as unsolved (F6).
- Framing: DECISIONS.md:365-374 corrects the Z.1 brief's framing against the repository's own interest.

**E4. ADR-012 defect 3 — the mutation harness purges bytecode before every run.**
- Kind: **shipped** (correction)
- Deciding figures (n): `routine_consecutive_years=3,` and `=4,` are the same byte length, so a restore inside the same second left mutated bytecode valid under CPython's mtime-and-size check
- file:line: DECISIONS.md:386-390; progress.md:74-77, :285-290; scripts/mutations.py:143-155
- Bar + registration date: not a registered bar; harness discipline.
- Amendments: none.
- Corrections applied: this row is the correction.
- Framing: "A harness that can report on absent source is worse than no harness." DECISIONS.md:392-396. `InsiderExperiment.md` sound item 14 verifies the fix in source.

**E5. Three corrections to the stage briefs, recorded against the repository's own interest.**
- Kind: **shipped** (self-disclosure)
- Deciding figures (n): (i) Task 4's ETA was never stated, against a brief that required one per task; (ii) the brief's "2.78 GB on a 14 GB machine" is wrong on the host — `/home` sits on 466 GB with 328 GB available, 26 % used, so pruning is a preference not a need; (iii) the Z.1 brief records five hours where the commit record shows ~51 minutes for A.1 and ~20 for Z.1
- file:line: progress.md:207-208; progress.md:144-149; progress.md:115-120
- Bar + registration date: no bar; recorded at Stage Z.1, 2026-08-25.
- Amendments: none.
- Corrections applied: these rows are the corrections.
- Framing: "Recorded rather than smoothed over." progress.md:208; "Both are recorded rather than one being picked." progress.md:118-119. `InsiderExperiment.md` AUDIT-B-InsiderExperiment-14 (S4, PROVENANCE) records that the timing table's stated "18:20 UTC" session start is local time, not UTC (commit timestamps are UTC−07:00), and calls it immaterial to every result.

---

## F. Open items

**F1. Section 12, the operator prior — reserved and empty.**
- Kind: **open**
- Deciding figures (n): the slot is empty; the assistant's prior of 0.12 is recorded beside it and never inside it (`assistant_prior=0.12`, src/insider/config.py:153)
- file:line: REGISTRATION.md:497-520 (the empty marker :506, the block rule :508-511, the 0.12 and its four inputs :513-520); REGISTRATION.md:876-885; progress.md:93-99, :300-306; src/insider/registration_check.py
- Bar + registration date: "**This slot blocks Stage B while it is empty.** `insider.registration_check.require_operator_prior` raises `OperatorPriorMissing` rather than warning." REGISTRATION.md:508-511; registered `398755b`, 18:38 local.
- Amendments: none.
- Corrections applied: none.
- Framing: "It blocks Stage B structurally, and Stage B is blocked independently by the power gate, so nothing waited on it operationally. It remains outstanding for the calibration ledger." REGISTRATION.md:878-881, progress.md:142-143.

**F2. The calibration ledger holds zero independently formed entries.**
- Kind: **open**
- Deciding figures (n): zero
- file:line: REGISTRATION.md:882-885; progress.md:97-99
- Bar + registration date: no bar; a standing programme-level obligation stated at REGISTRATION.md:499-501.
- Amendments: none.
- Corrections applied: none.
- Framing: "NPDExperiment's prior was adopted rather than formed, so **the calibration ledger still holds zero independently formed entries.**" REGISTRATION.md:882-885 — a cross-repository claim the consolidator should carry forward.

**F3. Corpus pruning, discretionary.**
- Kind: **open**
- Deciding figures (n): 2,783,280,665 bytes (2.78 GB) of cache; host `/home` 466 GB with 328 GB available, 26 % used
- file:line: progress.md:144-149; REGISTRATION.md:832-833
- Bar + registration date: no bar; "**Nothing is deleted.** Every file, ledger, report and the 2.78 GB corpus cache stays in place. A closure that destroys its own inputs cannot be audited." ADR-010, DECISIONS.md:300-301.
- Amendments: none.
- Corrections applied: the brief's disk-pressure claim corrected (E5 ii).
- Framing: "pruning is a preference and not a need." progress.md:149. `InsiderExperiment.md` AUDIT-B-InsiderExperiment-9 records that 79.3 % of the cache is full-index archives rather than the corpus data sets, which bears on what pruning would cost.

**F4. Section 14.3, the unmeasured Carhart residual.**
- Kind: **open**
- Deciding figures (n): "the residual MDE would be lower than 49.35 by an amount this stage did not measure and will not measure"; `InsiderExperiment.md` bounds the market-beta channel alone at 47.15 bp, and computes that reaching the 40 bp bar would need a total factor R² of 34.31 %
- file:line: REGISTRATION.md:578-583, :790-796; DECISIONS.md:29-32
- Bar + registration date: recorded as a deviation at registration, `398755b` 18:38 local, before measurement.
- Amendments: none. "Any future attempt to revisit it must register the change as a numbered amendment, formed before measurement, in a repository that is not this one." REGISTRATION.md:794-796.
- Corrections applied: none.
- Framing: disclosed clearly and with a stated reason for not measuring ("measuring it after seeing BLOCKED is choosing a method by its answer"). `InsiderExperiment.md` AUDIT-B-InsiderExperiment-12 (S3, OVER_CLOSED) records the finding as: the disclosure is sound, but the fixed verdict sentence repeated in four documents carries none of it.

**F5. ADR-009's survivorship leak in the first moment.**
- Kind: **open**
- Deciding figures (n): 13,750 name-sessions, ~7.4 % of held name-sessions
- file:line: DECISIONS.md:270-280
- Bar + registration date: no bar; recorded limitation, Stage A.1 2026-08-25.
- Amendments: none.
- Corrections applied: none. "The leak would have to be fixed before any Stage B first moment, and Stage B is not authorized." DECISIONS.md:279-280.
- Framing: disclosed with its direction (reduces dispersion, moves the verdict toward GO, so conservative given BLOCKED fired).

**F6. ADR-012's residual: the parse-tree guard catches decoration, not misuse.**
- Kind: **open**
- Deciding figures (n): none — a stated structural limit
- file:line: DECISIONS.md:365-374; progress.md:62-67
- Bar + registration date: no bar; standing guard 2, CLAUDE.md:37-40.
- Amendments: none.
- Corrections applied: the text-scanning version was replaced (E3); the residual is explicitly not solved.
- Framing: "A future scaffold that wants the stronger property has to express it differently, and this repository did not solve it." DECISIONS.md:373-374. `InsiderExperiment.md` sound item 13 records this as exemplary self-correction.

**F7. ADR-011's reopening boundary for any equal-weighted successor.**
- Kind: **open**
- Deciding figures (n): the seen secondary, 34.29 bp per month
- file:line: DECISIONS.md:314-343 (the boundary :328-333, the assessment :335-338); REGISTRATION.md:865-874; progress.md:51-55
- Bar + registration date: Accepted Stage Z.1, 2026-08-25; imposes a condition on a repository that does not yet exist.
- Amendments: none.
- Corrections applied: none.
- Framing: "**Assessment.** Borderline at best. A disclosed selection is better than a hidden one, but the disclosure does not undo the information." DECISIONS.md:335-338. `InsiderExperiment.md` AUDIT-B-InsiderExperiment-3 records that at conventional 80 % power the secondary would itself have been BLOCKED (48.03 bp), so the boundary is built on a 50 %-power figure that is nowhere labelled as such — a point the cross-repository pass should carry, since ADR-011 is written for a future repository to act on.

---

## Counts by kind

| Kind | Entries |
|---|---|
| positive | 3 (A1, A2, C1) |
| qualified positive | 2 (A6, C6) |
| thresholded negative | 3 (A3, A4, A5) |
| shipped | 36 (A7, B1-B10, C2-C5, C7, C8, D1-D14, E1-E5) |
| open | 8 (A8, F1-F7) |
| **Total** | **52** |

Figures reported as **not located**: the pytest pass count behind the "106 tests" claim (D11) — no shipped
artifact records it; `mutations.json:49` stores a progress line only.

---

*Provenance of this ledger.* The draft ledger was written after the draft findings by a follow-up
agent, because the reader that produced the draft findings was interrupted by an account limit
before it could write the companion positives ledger. This consolidation carried every row forward,
rewrote each draft reference to its consolidated finding ID, and added one figure (the 14.6-name
book at the registered floor, row C6) computed at consolidation from figures already in the ledger.
No row was deleted and no row was merged, because the draft was written as a single part and carried
no duplicates.

---

## Leads for the cross-repository pass

Everything below is a claim, artifact or standard in **this** repository that reaches outside it.
Each is stated with its file:line here and with the comparison repository this agent would check
next. None of these is itself a finding; they are the handles a cross-repository pass needs.

### L1. The NPDExperiment power figures are quoted verbatim in three places and propagate further
"NPDExperiment closed at unresolved-at-achievable-power. Its realized minimum\ndetectable contrast
came in at 0.0512 against a realistic effect band of 0.01 to\n0.05 … That was discovered after 415
days of collection and 6.9378\nUSD of spend, in the same session that read the result."
(REGISTRATION.md:21-26, identical at DECISIONS.md:12-16, restated at progress.md:111-113). Four
figures — **0.0512**, the band **0.01 to 0.05**, **415 days**, **6.9378 USD** — carry the entire
motivation for Section 0, which is this repository's headline transferable artifact. The same
`0.0512` string is pinned inside another repository's honesty test (Agent B's
`AUDIT-B-retail-power-limits-1` records `assert "0.0512" in text` at
retail-power-limits/tests/test_honesty.py:139-147), so the figure has already travelled at least
two hops from its source. **Comparison repositories: NPDExperiment (does its anchor carry these four
figures, and is 0.0512 an MDE at the same convention?), then retail-power-limits.**

### L2. The 50 %-power convention is a family-wide question, not a local one
AUDIT-B-InsiderExperiment-3 establishes that this repository's "minimum detectable effect" is
`t_critical * se` with `t_critical=2.0` (src/insider/power/mde.py:66, src/insider/config.py:147) and
that no power level is registered anywhere in the tree. If NPDExperiment's 0.0512 and HFExperiment's
figures are computed the same way, then every "unresolved at achievable power" closure in the family
is a 50 %-power statement and the meta-repository that collects them compares like with like but
labels none of them. **Comparison repositories: NPDExperiment and HFExperiment for the convention;
retail-power-limits, which aggregates the closures, for the labelling.** This is the single highest-
value cross-repository check this ledger can offer.

### L3. The HFExperiment figures are quoted four times as the reason for a registered design choice
"Concentrated books are what killed H-F at 42 to 66\npercent tracking error." (REGISTRATION.md:389,
repeated at :760-762 and :861; DECISIONS.md:341; progress.md:48, :257) and "H-F at z 1.668 against a
2.50\nbar" (progress.md:107). The 42-66 % tracking error band is the stated justification for
registering a value-weighted primary — the choice that Section 17.3 then records as having backfired.
**Comparison repository: HFExperiment (Agent B has already consolidated 18 findings there; the 42-66 %
band and the z 1.668 / 2.50 pair should be checked against its anchor).**

### L4. Two factual claims about AiTrader are asserted in six places and are the reason two guards exist
"Six Level 1 keys in AiTrader were parsed, validated, printed at startup, and\nenforced nowhere."
(src/insider/config.py:3-4, repeated at DECISIONS.md:362-369 and tests/test_guards.py:95) and
"AiTrader Level 4 computing whale scores from two empty tables and emitting\nplausible numbers"
(DECISIONS.md:414-416, repeated at CLAUDE.md:34-36 and src/insider/absence.py:3). These are factual
claims about another repository, and this repository's two strongest standing guards are justified by
them. **Comparison repository: AiTrader.**

### L5. The universe port is a three-hop chain and only the last hop is verified
"Copied from ~/Documents/GitHub/AiTrader/backtest/universe.py on\n2026-08-25, through the
intermediate copy in NPDExperiment which was taken from\nthe same file and verified against the
source's own stored membership." (src/insider/market/universe.py:3-5). This repository verifies its
own copy at three formation dates, 500 of 500 rank by rank (tests/test_universe_port.py:85-91,
sound item 15) — but the claim that the *intermediate* NPDExperiment copy was verified is asserted
here and not evidenced here. **Comparison repositories: NPDExperiment (was its copy verified, and
against what?) and AiTrader (does the source still hash to the recorded values?).**

### L6. The AiTrader boundary hashes are directly checkable from the other side
`reports/stage_a1/port.json` records `analysis_bars.db` sha256 `d599ccf0…e924` and
`backtest/universe.py` sha256 `8188eea0…5529`, identical before and after the read, with
`"unchanged": true` (port.json:1-12, row D2), re-verified at closure (progress.md:135-138). Two
hashes, both recomputable against AiTrader's own anchor. **Comparison repository: AiTrader.**

### L7. The family record is a cross-repository claim with a count
"Eight price-based and signal-based hypothesis families have now been tested\nacross AiTrader,
HFExperiment, NPDExperiment and InsiderExperiment. **Zero have\nproduced a positive result that
survived its own registered bar.**" (progress.md:103-105). Eight families, four repositories, zero
survivors. Agent B's own retail-power-limits consolidation records that the meta-repository "asserts
a population of hypotheses it never enumerates" and compares four power repositories against three
contrast repositories carrying at least eleven closed hypotheses. The two population counts are not
obviously reconcilable, and neither document enumerates its families. **Comparison repository:
retail-power-limits first, then AiTrader, HFExperiment and NPDExperiment for the enumeration.**
This is a candidate CROSS_REPO_INCONSISTENCY rather than a lead only.

### L8. ADR-012 is cited by name in another repository, and was applied there only in part
"A guard that has never failed is not a guard" (DECISIONS.md:347-396, row D14, named by this
repository as "the most reusable finding this repository produced"). retail-power-limits/DECISIONS.md:164-166
cites it explicitly as "the InsiderExperiment ADR-012 lesson", and Agent B's
`AUDIT-B-retail-power-limits-1` finds that in that repository one detector has no canary at all and
neither flagship canary calls the detector it certifies. **Comparison repository: retail-power-limits.**
The lesson's own residual is disclosed here and unsolved — "It catches decoration, not misuse. …
this repository did not solve it." (DECISIONS.md:373-374, row F6) — so the interesting question is
whether any downstream repository claims to have solved it.

### L9. The seal architecture names an unspecified predecessor's actual failure
"The seal prevents the accident, not the intent, and that is the failure mode\nthat actually
occurred in the predecessor." (DECISIONS.md:188-193, row D9), and "Each guard exists because a
predecessor system" failed (tests/test_guards.py:3). The predecessor is never named.
**Comparison repositories: HFExperiment and NPDExperiment** — identifying which one had the
accidental early read would let the cross-repository pass check whether the guard is aimed at the
right failure.

### L10. The calibration ledger is a standing programme-level obligation reported at zero
"NPDExperiment's prior was adopted rather than formed, so **the calibration ledger still holds zero
independently formed entries.**" (REGISTRATION.md:882-885, row F2; the mechanism at
src/insider/registration_check.py). Section 12 here is registered and left empty by design
(row F1), and this repository's own assistant prior of 0.12 is recorded beside the slot and never
inside it. **Comparison repositories: every repository in the family that records an operator prior —
NPDExperiment first, since its prior is the one named as adopted rather than formed.**

### L11. ADR-011 imposes a condition on a repository that does not yet exist
"Assessment. Borderline at best. A disclosed selection is better than a hidden one, but the
disclosure does not undo the information." (DECISIONS.md:335-338, row F7; the boundary at
DECISIONS.md:328-333 and REGISTRATION.md:865-874). The boundary is stated against the seen
equal-weighted secondary of 34.29 bp — which AUDIT-B-InsiderExperiment-3 shows is a 50 %-power
figure that would have been BLOCKED at 80 % power. **Comparison repository: any future
equal-weighted insider successor; today, the cross-repository pass should simply record that the
boundary's threshold inherits an unlabelled power convention.**

### Standards applied here that look **stricter** than the house norm

- **Config fields must have an enforcement site or the suite fails.** `tests/test_guards.py` walks
  the parse tree and fails when any `Config` field is referenced nowhere outside `config.py`
  (src/insider/config.py:3-6, row D8, E3). This repository states that AiTrader had six keys that
  would have failed this test. **Compare: AiTrader, NPDExperiment, HFExperiment.**
- **The mean is sealed behind a single named reader.** `read_sealed_returns` is defined once
  (src/insider/eval/evaluator.py:33), four guards enforce it, and the `insider.power` package imports
  only `config`, `paths` and stdlib (row D9, sound item 2). A power gate that cannot see the alpha it
  is gating is a stronger property than "we did not look". **Compare: NPDExperiment, whose power
  finding arrived "in the same session that read the result" (DECISIONS.md:16).**
- **Refusals are demonstrated by producing them.** CLAUDE.md:44-46, shipped as
  `reports/stage_a1/refusals.md` (row D6). **Compare: any repository that reports a refusal count
  without the artifact.** Note that AUDIT-B-InsiderExperiment-2 shows the produced artifact is what
  exposed the count-unit error, which is the standard working as intended.
- **No `-m "not slow"` deselection.** `pyproject.toml:62-68` sets `addopts = "-q --strict-markers"`
  only, so the slow universe-port test actually runs in `make test` (row D12, sound item 15).
  **Compare: AiTrader, HFExperiment, NPDExperiment pyproject settings.**
- **A mutation harness that edits real source, restores it and asserts byte equality**
  (scripts/mutations.py:143-155, row D7, sound item 14), with five registered mutations on real
  registered values. **Compare: retail-power-limits, whose canaries do not call their detectors.**

### Standards applied here that look **laxer** than the house norm

- **The results prose is hand-transcribed from the artifacts and has no drift check.** Three of the
  fourteen findings (AUDIT-B-InsiderExperiment-6, -7 and -11) are the same defect: Section 15 or 17
  prose carrying a pre-correction or pre-filter number beside the corrected artifact. This is exactly
  the failure that a generated-block mechanism prevents, and **retail-power-limits has one** —
  BEGIN/END GENERATED markers re-rendered and compared in `tests/test_render.py`, with ADR-002 there
  claiming "Prose and data cannot diverge silently." **Comparison repository: retail-power-limits.**
  Whether that mechanism actually covers its own README is a separate question Agent B answered there
  in the negative, so the honest framing is that neither repository has the property outright: this
  one has no mechanism, that one has a mechanism with a hole.
- **No power level is registered, anywhere.** The critical value is registered
  (REGISTRATION.md:478-479, row C5); β is not. **Comparison repositories: NPDExperiment and
  HFExperiment** — if either registers a power level, this repository is laxer than the family norm
  on the axis it most advertises.
- **A validation sample drawn only from the survivors.** `sample_xml` selects from the `event` table
  (src/insider/corpus/validate.py:115-119, row D5, AUDIT-B-InsiderExperiment-10), so the check cannot
  see what the funnel dropped. **Comparison repository: any repository in the family that validates a
  parse against a rejected sample as well as a retained one.**
- **A shipped artifact that records a pytest progress line instead of a result line**
  (reports/stage_a1/mutations.json:49, row D11, AUDIT-B-InsiderExperiment-13). The pass count behind
  "106 tests" is **not located** in any shipped artifact. **Comparison repository: retail-power-limits,
  whose "111 tests" claim Agent B found false at its anchor** — the same class of claim, checked from
  the other side.
