# InsiderExperiment — REOPEN LEDGER (part "all")

Repository InsiderExperiment at anchored SHA `12d9fd36cf055cb10ea67a3fc737e404217bc95a` (master, 2026-08-25). Factual, not advocacy. One line per entry, then detail. Live HEAD equalled the anchor at read time (2026-09-03T06:35:25Z); no commits after the closure commit. The repository has one hypothesis, two gates, three registered secondaries, one unwritten stage, and one reserved operator slot. There is no explicit "reopen if" list; reopen conditions below are the "what would overturn it" clauses of the ADRs, the ADR-011 boundary, and the amendment clause.

Closure dates are from the commit clock (-07:00): Section 0 `fbfc74e` 2026-08-25T18:34:56-07:00; Sections 1-16 `398755b` 18:38:50; corpus `ccc9b13` 18:47:16; power gate `cb17046` 19:11:45; docs `d8b81f1` 19:11:55; closure `12d9fd3` 23:24:15.

## Summary table

| # | Entry | Status | Closure kind | Closure date | Deciding figure (n) | Cross-repo? |
|---|---|---|---|---|---|---|
| 1 | H1 Section 1 hypothesis: net-of-cost survival of Form 4 opportunistic/cluster purchases, liquid-500 | closed, untested (verdict row V7) | untestable-at-achievable-power (power gate BLOCKED) | 2026-08-25 (`cb17046`; closure `12d9fd3`) | MDE 49.35 bp/mo vs bar 40; n 2,581 sessions, N_eff 2,869.9, TE 9.993%, sd 62.95 bp | yes (see 12, 18, 19) |
| 2 | Corpus gate (Section 0.3) | closed GO | gate cleared | 2026-08-25 (`ccc9b13`) | 4,585 events vs floor 1,000; coverage 99.5% vs 80% | no |
| 3 | Power gate, primary 126-session "value-weighted" (median-dollar-volume) book | closed BLOCKED | gate failed | 2026-08-25 (`cb17046`) | as row 1 | no |
| 4 | Secondary hold, 21 sessions VW | reported, non-verdict-bearing | none | 2026-08-25 | MDE 81.48 (n 2,513) | no |
| 5 | Secondary hold, 63 sessions VW | reported, non-verdict-bearing | none | 2026-08-25 | MDE 57.34 (n 2,563) | no |
| 6 | Secondary weighting, 126 sessions equal-weighted | reported, non-verdict-bearing, "would have fired DEGRADED", not promoted | none (declined) | 2026-08-25 | MDE 34.29 (n 2,581, N_eff 2,798.1, TE 6.856%) | no |
| 7 | Newey-West lag grid on the primary | reported | none | 2026-08-25 | 50.19 / 49.35 / 49.11 / 49.53 at lags 5/21/63/126 | no |
| 8 | Stage B: Carhart four-factor net alpha at the 100 bp round trip | never written; blocked | blocked by row 3 and row 9 | n/a | none (alpha sealed, unread) | no |
| 9 | Section 12 operator prior | open, outstanding | none | n/a | slot empty; assistant's 0.12 beside it | yes (calibration ledger, NPDExperiment) |
| 10 | Section 14.3 Carhart-residual MDE | not measured; "will not measure" here | deferred to a different repository | 2026-08-25 | unmeasured; bounded above by 49.35 | possibly |
| 11 | ADR-007 market-capitalization weighting (registered basis of Section 7) | not run; proxy substituted | registered deviation | 2026-08-25 (`398755b`) | none | possibly |
| 12 | Section 4 universe narrowing / "a different universe" | scope decision, standing; alternative named, not run | registered narrowing | 2026-08-25 | 148,883 outside_universe vs 9,160 in; 5.8% | yes |
| 13 | Section 2 / ADR-003 alternative regimes (13F, congressional) | rejected ex-ante | registered rejection | 2026-08-25 | 45-day lag | yes |
| 14 | ADR-009 survivorship leak (names dropped on leaving the universe mid-hold) | open limitation; must be fixed before any Stage B | recorded, not fixed | 2026-08-25 | 13,750 name-sessions, 7.4% | no |
| 15 | ADR-008, ADR-013 implementation defects | closed (fixed) | corrected | 2026-08-25 | 1 label moved; 43 events un-merged | no |
| 16 | ADR-012 residual: config guard cannot tell enforce from display | open, deferred to next scaffold | recorded | 2026-08-25 | n/a | yes (any successor scaffold) |
| 17 | Corpus cache pruning | open, discretionary | none | n/a | 2,783,280,665 bytes | no |
| 18 | "Family record": eight families, zero positives | cross-repo claim, standing | none | 2026-08-25 | H-F z 1.668 vs 2.50; NPD MDE 0.0512 vs band 0.01-0.05 | yes |
| 19 | AiTrader news-drift experiment pointer | untouched, running elsewhere | none | n/a | verdict due at 60 clusters | yes |

## Detail

### 1. H1 — Section 1 hypothesis
- **Statement:** "Opportunistic and cluster insider purchases, disclosed on Form 4, predict positive abnormal returns that survive the operator's measured cost band at achievable size." REGISTRATION.md:165-167.
- **Status:** closed without the hypothesis being tested. "Verdict row **V7** fired, not V3." REGISTRATION.md:890-891; "It is not a null on the hypothesis." :771.
- **Closure kind:** untestable-at-achievable-power (Section 0 power gate BLOCKED). REGISTRATION.md:708, :812-816; DECISIONS.md:288-292; progress.md:14-18.
- **Closure date:** 2026-08-25 (`cb17046` 19:11:45-07:00 fired; `12d9fd3` 23:24:15-07:00 closed).
- **Deciding figure (n):** MDE 49.35 bp per month against BLOCKED floor 40; daily excess-return SD 62.95 bp; n 2,581 sessions; VIF 0.899; N_eff 2,869.9; TE 9.993%; SE 24.68 bp. REGISTRATION.md:712, :717-719; reports/stage_a1/power.json:6-12, :132-136.
- **Blockers:** (a) power gate BLOCKED is terminal by registration: "Stage B is never written and the repo closes on the finding." REGISTRATION.md:43, :443; (b) "None in force. Section 0 fired BLOCKED, so no amendment can authorize Stage B." :800; (c) operator prior empty, blocks Stage B by code: REGISTRATION.md:508-511; src/insider/registration_check.py:56-64; src/insider/eval/evaluator.py:41; (d) cost band applies only to the liquid band, so the universe cannot be widened at the measured costs: REGISTRATION.md:319-324; DECISIONS.md:127-130; (e) ADR-009 leak must be fixed before any first moment: DECISIONS.md:278-280.
- **Reopen conditions:** (a) amendment clause: "Changing a registered value after that commit requires a numbered amendment in Section 17 carrying its own evidence." REGISTRATION.md:8-9 (foreclosed by :800); (b) ADR-010: "**What would overturn it.** Nothing inside this repository." DECISIONS.md:308-310; (c) ADR-011 boundary for equal-weight-as-primary in a fresh registration: must "state in its own Section 0 that its primary weighting was selected after seeing a secondary result from InsiderExperiment A.1, and it must carry a correspondingly higher bar." REGISTRATION.md:865-870; DECISIONS.md:328-333; (d) "The honest alternative is a different universe or a different disclosure regime, neither of which inherits the seen number." REGISTRATION.md:872-874; DECISIONS.md:335-338; (e) Carhart-residual revisit "must register the change as a numbered amendment, formed before measurement, in a repository that is not this one." REGISTRATION.md:794-796; (f) successor work "goes in a NEW repository that reads this one across a read-only boundary" (untracked marker `_CLOSED_DO_NOT_RUN_HERE`, unanchored, read 2026-09-03T06:32:15Z).
- **Possibly met by other repo?:** yes, to check in the cross-repo pass: any repository that (i) runs a Form 4 or other insider design on a different universe (e.g. beyond the liquid-500) or a different disclosure regime, or (ii) registers an equal-weighted or cap-weighted calendar-time book with the ADR-011 disclosure. None is named in this repository.

### 2. Corpus gate
- **Status:** CORPUS-GO. REGISTRATION.md:594-596; corpus.json:160-161.
- **Closure kind / date:** gate cleared, 2026-08-25 (`ccc9b13`; evidence ledger corpus_gate 2026-08-26T01:42:24Z, unanchored).
- **Deciding figure (n):** 4,585 qualifying events vs floor 1,000; 99.5% session coverage vs 80%; mean book width 71.9. REGISTRATION.md:594-596, :822-826; corpus.json:2, :158-159.
- **Blockers:** none.
- **Reopen conditions:** ADR-002 "What would overturn it. A disagreement in the XML sample, or a full-index ratio that moved across quarters" DECISIONS.md:72-74 — not met: 25 agree / 0 disagree (DECISIONS.md:64-65; validation.json), ratio 2.047-2.108.
- **Cross-repo?:** no.

### 3. Power gate, primary
- As row 1. Additional detail: weight concentration named as cause, REGISTRATION.md:745-757, :837-848; effective names 29.7 of 71.9 held (portfolio.json:27, :7); top-1 14.9%, top-5 33.8% (portfolio.json:23-24). Weighting basis is median dollar volume, a registered deviation from value (cap) weighting: REGISTRATION.md:393-395, :566-576; DECISIONS.md:197-222; src/insider/portfolio/returns.py:102-103; src/insider/market/store.py:100-108.
- **Reopen conditions:** see row 1 (a)-(e). Also Section 14.3: the A.1 figure is an upper bound on the Stage B (Carhart) figure, REGISTRATION.md:578-583.

### 4-5. Secondary holds 21 and 63 sessions
- **Status:** reported, non-verdict-bearing by registration. REGISTRATION.md:368-369, :474-476.
- **Deciding figures (n):** 21 sessions: MDE 81.48, n 2,513, TE 15.70%, book 15.4 names (power.json:24-43; REGISTRATION.md:713). 63 sessions: MDE 57.34, n 2,563, TE 11.83% (power.json:45-64; REGISTRATION.md:714).
- **Blockers / reopen:** none registered.

### 6. Secondary weighting, equal-weighted
- **Status:** reported; "would have fired DEGRADED at 34.29 bp"; "It is not promoted." REGISTRATION.md:764-767, :850-858; DECISIONS.md:318-327; progress.md:40-45.
- **Deciding figure (n):** MDE 34.29 bp per month; n 2,581; VIF 0.922; N_eff 2,798.1; TE 6.856%; effective names 66.9. REGISTRATION.md:715; power.json:66-75; portfolio.json:111.
- **Blockers:** registered as secondary before measurement, REGISTRATION.md:387, :474-476; promotion refused on the "by its answer" ground, :766-767, DECISIONS.md:325-326.
- **Reopen conditions:** ADR-011 boundary (row 1 (c)); assessment "borderline at best" REGISTRATION.md:872; DECISIONS.md:335.
- **Cross-repo?:** possibly — any successor registration naming equal weight as primary must cite this repository (DECISIONS.md:330-333).

### 7. Newey-West lag grid
- **Status:** reported. REGISTRATION.md:721-723; power.json:88-113. Verdict "does not turn on the bandwidth choice." No blockers or reopen conditions.

### 8. Stage B
- **Status:** never written. REGISTRATION.md:443, :800, :815-816; DECISIONS.md:291-292.
- **Blockers:** power gate BLOCKED (row 1 (a),(b)); operator prior empty (row 9); ADR-009 leak (row 14); entry-rule mismatch noted in all.md "What I checked" (registration vs code) would also need correction before a first moment is read.
- **Reopen conditions:** none inside this repository (DECISIONS.md:308-310); successor repository only (REGISTRATION.md:794-796; marker file).

### 9. Section 12 operator prior
- **Status:** open, outstanding. "[ EMPTY. The operator writes a number here himself, before Stage B runs. ]" REGISTRATION.md:506; closes unfilled :876-885; progress.md:93-99, :140-143.
- **Deciding figure:** none; assistant's prior 0.12 recorded beside it, REGISTRATION.md:513; config.py:153.
- **Blockers:** none (operator action).
- **Reopen conditions:** the slot is itself a Stage B precondition (registration_check.py:56-64).
- **Cross-repo?:** yes — "the calibration ledger still holds zero independently formed entries" (REGISTRATION.md:884-885; progress.md:97-99) references NPDExperiment's adopted prior; the ledger itself is not in this repository.

### 10. Section 14.3 Carhart-residual MDE
- **Status:** not measured; "an amount this stage did not measure and will not measure". REGISTRATION.md:790-796; DECISIONS.md:29-32.
- **Deciding figure:** none; bounded above by 49.35 (REGISTRATION.md:579-583).
- **Blockers:** stated: "measuring it after seeing BLOCKED is choosing a method by its answer" :793-794; ADR-001 "a factor regression on uncentered data produces an intercept and the intercept is the alpha" DECISIONS.md:30-31; factor data are not an SEC source (CLAUDE.md:61 "SEC access only").
- **Reopen conditions:** "must register the change as a numbered amendment, formed before measurement, in a repository that is not this one." REGISTRATION.md:794-796.
- **Cross-repo?:** possibly — any successor that regresses the centered series on Carhart factors.

### 11. ADR-007 market-capitalization weighting
- **Status:** route "verified working" and not taken. DECISIONS.md:204-212; REGISTRATION.md:566-576.
- **Blockers:** `company_tickers.json` lists only current registrants (21 of 25 sampled issuers present), DECISIONS.md:207-210; shares outstanding not split-adjusted vs bars with adjustment `all`, :210-212.
- **Reopen conditions:** none stated; amendment clause REGISTRATION.md:8-9 applies in principle, foreclosed by :800.
- **Cross-repo?:** possibly — a successor with a point-in-time cap weight.

### 12. Section 4 universe narrowing
- **Status:** standing scope decision; alternative named, not run. REGISTRATION.md:303-329; DECISIONS.md:105-135.
- **Deciding figure (n):** 148,883 `outside_universe` vs 9,160 reaching and passing the universe filter; 5.8%. REGISTRATION.md:656-660; DECISIONS.md:120-125; corpus.json:44.
- **Blockers:** "the operator cannot trade the illiquid tail at his cost band" REGISTRATION.md:319-324; spread band 15.8-50.0 bp is a large-cap measurement, :404-407.
- **Reopen conditions:** "The honest alternative is a different universe" REGISTRATION.md:872-874; DECISIONS.md:336-338. A cost measurement for the next liquidity band would be the precondition.
- **Cross-repo?:** yes — any repository holding a measured spread for smaller names, or bars for a wider universe (the source `analysis_bars.db` is 7.3 GB, port.json:10, versus 1,218 symbols copied, :5).

### 13. Section 2 / ADR-003 alternative regimes
- **Status:** rejected ex-ante. REGISTRATION.md:196-213; DECISIONS.md:78-101.
- **Blockers (as reasons):** 13F 45-day lag and ex-post manager selection, :198-204; congressional 45-day lag and public competition, :206-209.
- **Reopen conditions:** "a different disclosure regime" is named as the honest alternative (REGISTRATION.md:873); no specific trigger.
- **Cross-repo?:** yes — any repository testing 13F cloning or congressional disclosure.

### 14. ADR-009 survivorship leak
- **Status:** recorded limitation, not fixed. DECISIONS.md:258-280.
- **Deciding figure:** 13,750 name-sessions dropped, ~7.4% of held name-sessions (DECISIONS.md:264-265; power.json:118).
- **Blockers:** none; direction toward GO for the second moment (DECISIONS.md:275-278).
- **Reopen conditions:** "would have to be fixed before any Stage B first moment" DECISIONS.md:279-280.

### 15. ADR-008 and ADR-013 defects
- **Status:** closed, corrected. DECISIONS.md:226-255, :400-416. One label moved (insufficient_history → routine); 43 merged events restored; qualifying set 4,585 and MDE 49.35 unchanged (:245-249). The Section 15.1 by-year table still carries the merged 4,542 (all.md DRAFT-all-5).

### 16. ADR-012 residual
- **Status:** open, deferred. "A future scaffold that wants the stronger property has to express it differently, and this repository did not solve it." DECISIONS.md:365-374; progress.md:62-67.
- **Cross-repo?:** yes — any scaffold ported from this one (DECISIONS.md:392-396).

### 17. Corpus cache pruning
- **Status:** discretionary, open. progress.md:144-149. 2,783,280,665 bytes; host has 328 GB free; "pruning is a preference and not a need."

### 18. Family record (cross-repo claim)
- **Statement:** "Eight price-based and signal-based hypothesis families have now been tested across AiTrader, HFExperiment, NPDExperiment and InsiderExperiment. **Zero have produced a positive result that survived its own registered bar.**" progress.md:103-106. "Two closed on power rather than on absent signal: H-F at z 1.668 against a 2.50 bar, and NPD at unresolved-at-achievable-power." :107-108. NPD figures: MDE 0.0512 vs band 0.01-0.05, 415 days, 6.9378 USD (REGISTRATION.md:21-25).
- **Cross-repo?:** yes — the characterization of HFExperiment's H-F (z 1.668 vs 2.50) as a power closure and the eight-family count are claims about other repositories, for the cross-repo pass.

### 19. AiTrader news-drift pointer
- "The running AiTrader news-drift experiment is untouched and unaffected. Its verdict remains due at 60 clusters." progress.md:122-123. Cross-repo pointer only.

## Reopen conditions possibly met by work in a different repository (for the cross-repo pass)

1. A registration elsewhere that tests insider purchases on a wider or different universe, or on a different disclosure regime (rows 1, 12, 13). Trigger text: REGISTRATION.md:872-874; DECISIONS.md:336-338.
2. A registration elsewhere that names an equal-weighted or cap-weighted calendar-time book as primary with the ADR-011 disclosure (rows 6, 11). Trigger text: REGISTRATION.md:865-870; DECISIONS.md:328-333.
3. A Carhart-residual dispersion computed elsewhere on this repository's centered series (row 10). Trigger text: REGISTRATION.md:794-796.
4. An independently formed operator prior entering the calibration ledger (row 9). Trigger text: REGISTRATION.md:882-885.
5. The eight-family / zero-positive record and the H-F "closed on power" characterization (row 18) — to be checked against HFExperiment, NPDExperiment and AiTrader.
