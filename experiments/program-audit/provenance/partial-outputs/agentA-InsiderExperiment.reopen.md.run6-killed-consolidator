# InsiderExperiment — REOPEN LEDGER (consolidated)

Repository **InsiderExperiment** at anchored SHA `12d9fd36cf055cb10ea67a3fc737e404217bc95a` (master, 2026-08-25).
Factual, not advocacy. One line per entry in the table, then detail. Live HEAD equalled the anchor at consolidation
time (2026-09-03T06:47:49Z) and no commit followed the closure commit.

The repository has one hypothesis, two gates, three registered secondaries, one unwritten stage, and one reserved
operator slot. There is no explicit "reopen if" list; the reopen conditions below are the "what would overturn it"
clauses of the ADRs, the ADR-011 boundary, and the Section 17 amendment clause.

Closure timestamps are from the commit clock, which carries a **-07:00** offset (see AUDIT-A-InsiderExperiment-7;
progress.md:193-194 labels these times "UTC"): Section 0 `fbfc74e` 2026-08-25T18:34:56-07:00; Sections 1-16
`398755b` 18:38:50; corpus `ccc9b13` 18:47:16; power gate `cb17046` and tests `672b343` 19:11:45; docs `d8b81f1`
19:11:55; closure `12d9fd3` 23:24:15.

## Summary table

| # | Entry | Status | Closure kind | Closure date | Deciding figure (n) | Cross-repo? |
|---|---|---|---|---|---|---|
| 1 | H1 Section 1 hypothesis: net-of-cost survival of Form 4 opportunistic/cluster purchases, liquid-500 | closed, untested (verdict row V7) | untestable-at-achievable-power (power gate BLOCKED) | 2026-08-25 (`cb17046`; closure `12d9fd3`) | MDE 49.35 bp/mo vs bar 40; n 2,581 sessions, N_eff 2,869.9, TE 9.993%, sd 62.95 bp | yes (rows 12, 18, 19) |
| 2 | Corpus gate (Section 0.3) | closed GO | gate cleared | 2026-08-25 (`ccc9b13`) | 4,585 events vs floor 1,000; coverage 99.5% vs 80% | no |
| 3 | Power gate, primary 126-session "value-weighted" (median-dollar-volume) book | closed BLOCKED | gate failed | 2026-08-25 (`cb17046`) | as row 1 | no |
| 4 | Secondary hold, 21 sessions VW | reported, non-verdict-bearing | none | 2026-08-25 | MDE 81.48 (n 2,513) | no |
| 5 | Secondary hold, 63 sessions VW | reported, non-verdict-bearing | none | 2026-08-25 | MDE 57.34 (n 2,563) | no |
| 6 | Secondary weighting, 126 sessions equal-weighted | reported, non-verdict-bearing, "would have fired DEGRADED", not promoted | none (declined) | 2026-08-25 | MDE 34.29 (n 2,581, N_eff 2,798.1, TE 6.856%) | possibly |
| 7 | Newey-West lag grid on the primary | reported | none | 2026-08-25 | 50.19 / 49.35 / 49.11 / 49.53 at lags 5/21/63/126 (n 2,581) | no |
| 8 | Stage B: Carhart four-factor net alpha at the 100 bp round trip | never written; blocked | blocked by rows 3 and 9 | n/a | none (alpha sealed, unread) | no |
| 9 | Section 12 operator prior | open, outstanding | none | n/a | slot empty; assistant's 0.12 beside it | yes (calibration ledger, NPDExperiment) |
| 10 | Section 14.3 Carhart-residual MDE | not measured; "will not measure" here | deferred to a different repository | 2026-08-25 | unmeasured; bounded above by 49.35 (n 2,581) | possibly |
| 11 | ADR-007 market-capitalization weighting (registered basis of Section 7) | not run; proxy substituted | registered deviation | 2026-08-25 (`398755b`) | none measured; brackets 34.29-49.35 | possibly |
| 12 | Section 4 universe narrowing / "a different universe" | scope decision, standing; alternative named, not run | registered narrowing | 2026-08-25 | 148,883 outside_universe vs 9,160 in; 5.8% | yes |
| 13 | Section 2 / ADR-003 alternative regimes (13F, congressional) | rejected ex-ante | registered rejection | 2026-08-25 | 45-day lag | yes |
| 14 | ADR-009 survivorship leak (names dropped on leaving the universe mid-hold) | open limitation; must be fixed before any Stage B | recorded, not fixed | 2026-08-25 | 13,750 name-sessions, ~7.4% | no |
| 15 | Entry rule: registration vs code | open, unrecorded by the authors | not recognised | n/a | ~1.8 entry-day names per session in a 67-name book | no |
| 16 | ADR-008, ADR-013 implementation defects | closed (fixed in code); published table still stale | corrected | 2026-08-25 | 1 label moved; 43 events un-merged | no |
| 17 | ADR-012 residual: config guard cannot tell enforce from display | open, deferred to next scaffold | recorded | 2026-08-25 | n/a | yes (any successor scaffold) |
| 18 | Corpus cache pruning | open, discretionary | none | n/a | 2,783,280,665 bytes | no |
| 19 | "Family record": eight families, zero positives | cross-repo claim, standing | none | 2026-08-25 | H-F z 1.668 vs 2.50; NPD MDE 0.0512 vs band 0.01-0.05 | yes |
| 20 | AiTrader news-drift experiment pointer | untouched, running elsewhere | none | n/a | verdict due at 60 clusters | yes |

## Detail

### 1. H1 — Section 1 hypothesis
- **Statement:** "Opportunistic and cluster insider purchases, disclosed on Form 4, predict positive abnormal returns that survive the operator's measured cost band at achievable size." REGISTRATION.md:165-167.
- **Status:** closed without the hypothesis being tested. "Verdict row **V7** fired, not V3." REGISTRATION.md:890-891; "**It is not a null on the hypothesis.**" :771.
- **Closure kind:** untestable-at-achievable-power (Section 0 power gate BLOCKED). REGISTRATION.md:708, :812-816; DECISIONS.md:288-292; progress.md:14-18.
- **Closure date:** 2026-08-25 (`cb17046` 19:11:45-07:00 fired; `12d9fd3` 23:24:15-07:00 closed).
- **Deciding figure (n):** MDE 49.35 bp per month against BLOCKED floor 40; daily excess-return SD 62.95 bp; n 2,581 sessions; VIF 0.899; N_eff 2,869.9; TE 9.993%; SE 24.68 bp. REGISTRATION.md:712, :717-719; reports/stage_a1/power.json:3-12, :132-136.
- **Blockers:** (a) power gate BLOCKED is terminal by registration — "Stage B is never written and the repo closes on the finding." REGISTRATION.md:43, :443; (b) "None in force. Section 0 fired BLOCKED, so no amendment can authorize Stage B." :800; (c) operator prior empty, blocks Stage B by code: REGISTRATION.md:506-511; src/insider/registration_check.py:56-64; src/insider/eval/evaluator.py:41; (d) the cost band applies only to the liquid band, so the universe cannot be widened at the measured costs: REGISTRATION.md:319-324; DECISIONS.md:118-125; (e) ADR-009 leak must be fixed before any first moment: DECISIONS.md:275-280; (f) the entry-rule mismatch (row 15) would also need correcting before a first moment is read.
- **Reopen conditions:** (a) amendment clause — "Changing a registered value after that commit requires a numbered amendment in Section 17 carrying its own evidence." REGISTRATION.md:8-9 (foreclosed by :800); (b) ADR-010 — "**What would overturn it.** Nothing inside this repository." DECISIONS.md:308-310; (c) ADR-011 boundary for equal-weight-as-primary in a fresh registration: it "must state in its own Section 0 that its primary weighting was selected after seeing a secondary result from InsiderExperiment A.1, and it must carry a correspondingly higher bar." REGISTRATION.md:865-870; DECISIONS.md:328-333; (d) "The honest alternative is a different universe or a different disclosure regime, neither of which inherits the seen number." REGISTRATION.md:872-874; DECISIONS.md:335-338; (e) a Carhart-residual revisit "must register the change as a numbered amendment, formed before measurement, in a repository that is not this one." REGISTRATION.md:794-796; (f) successor work "goes in a NEW repository that reads this one across a read-only boundary" (untracked marker `_CLOSED_DO_NOT_RUN_HERE`, unanchored, read 2026-09-03T06:32:15Z).
- **Audit note:** AUDIT-A-InsiderExperiment-1 challenges the ground under (b) and the refusal in row 6; AUDIT-A-InsiderExperiment-2 and -3 identify two measurements the record never made that could move the deciding figure; AUDIT-A-InsiderExperiment-4 challenges the provenance of the bar it was measured against.
- **Possibly met by other repo?:** yes — see the cross-repository leads, items 1-3.

### 2. Corpus gate
- **Status:** CORPUS-GO. REGISTRATION.md:594-596; corpus.json:175-176.
- **Closure kind / date:** gate cleared, 2026-08-25 (`ccc9b13`; evidence ledger `corpus_gate` 2026-08-26T01:42:24Z, unanchored, read 2026-09-03T06:35:07Z).
- **Deciding figure (n):** 4,585 qualifying events vs floor 1,000; 99.5% session coverage vs 80%; mean book width 71.9. REGISTRATION.md:594-596, :822-826; corpus.json:2, :173-174.
- **Blockers:** none.
- **Reopen conditions:** ADR-002 — "**What would overturn it.** A disagreement in the XML sample, or a full-index ratio that moved across quarters" DECISIONS.md:72-74. Not met: 25 agree / 0 disagree (DECISIONS.md:64-65; validation.json), ratio 2.047-2.108.
- **Cross-repo?:** no.
- **Audit note:** the gate stands; only the *published by-year table* is stale (AUDIT-A-InsiderExperiment-5), and the stale table is 43 events low, not high, so it cannot have flattered the gate.

### 3. Power gate, primary
- As row 1. Additional detail: weight concentration named as the cause, REGISTRATION.md:745-757, :837-848; effective names 29.7 against a mean 71.9 held and 66.9 priced (portfolio.json:27, :7; power.json:16); top-1 14.9%, top-5 33.8% (portfolio.json:23-24). The weighting basis is median dollar volume, a registered deviation from value (capitalization) weighting: REGISTRATION.md:393-395, :567-576; DECISIONS.md:197-222; src/insider/portfolio/returns.py:102-103; src/insider/market/store.py:100-108.
- **Reopen conditions:** as row 1 (a)-(f). Also Section 14.3: the A.1 figure is an upper bound on the Stage B (Carhart) figure, REGISTRATION.md:578-583.
- **Audit note:** AUDIT-A-InsiderExperiment-2 (the registered weighting was never run) and -6 (the 71.9/66.9 basis mix in the published concentration table).

### 4-5. Secondary holds, 21 and 63 sessions
- **Status:** reported, non-verdict-bearing by registration. REGISTRATION.md:368-369, :467-476.
- **Deciding figures (n):** 21 sessions — MDE 81.48, n 2,513, TE 15.703%, priced book 38 at the median (power.json:24-44; REGISTRATION.md:713). 63 sessions — MDE 57.34, n 2,563, TE 11.827% (power.json:45-65; REGISTRATION.md:714).
- **Blockers / reopen conditions:** none registered.

### 6. Secondary weighting, equal-weighted
- **Status:** reported; "would have fired DEGRADED at 34.29 bp"; "**It is not promoted.**" REGISTRATION.md:764-767, :850-858; DECISIONS.md:318-327; progress.md:40-45.
- **Deciding figure (n):** MDE 34.29 bp per month; n 2,581 sessions; VIF 0.922; N_eff 2,798.1; TE 6.856%; effective names 66.9. REGISTRATION.md:715; power.json:66-75; portfolio.json:111.
- **Blockers:** registered as secondary before measurement, REGISTRATION.md:387, :474-476; promotion refused on the "by its answer" ground, :766-767 and DECISIONS.md:325-326.
- **Reopen conditions:** the ADR-011 boundary (row 1 (c)); the authors' own assessment of that route is "borderline at best" REGISTRATION.md:872; DECISIONS.md:335.
- **Cross-repo?:** possibly — any successor registration naming equal weight as primary must cite this repository (DECISIONS.md:330-333).
- **Audit note:** AUDIT-A-InsiderExperiment-1 argues the refusal ground contradicts Section 0.1. Honest counterweight recorded there: at SE 17.14 bp the equal-weighted design still has only 40% power at 30 bp and 63% at 40 bp.

### 7. Newey-West lag grid
- **Status:** reported. REGISTRATION.md:721-723; power.json:88-113. The verdict "does not turn on the bandwidth choice"; reproduced independently (50.1903 / 49.3543 / 49.1057 / 49.5319, n 2,581). No blockers or reopen conditions.

### 8. Stage B
- **Status:** never written. REGISTRATION.md:443, :800, :812-816; DECISIONS.md:288-292.
- **Blockers:** power gate BLOCKED (row 1 (a),(b)); operator prior empty (row 9); ADR-009 leak (row 14); entry-rule mismatch (row 15).
- **Reopen conditions:** none inside this repository (DECISIONS.md:308-310); a successor repository only (REGISTRATION.md:794-796; the untracked marker file).

### 9. Section 12 operator prior
- **Status:** open, outstanding. The slot is reserved and empty (REGISTRATION.md:506); it closes unfilled at :876-885; progress.md:93-99, :140-143.
- **Deciding figure:** none; the assistant's prior 0.12 is recorded beside it, REGISTRATION.md:513, :882-883; src/insider/config.py:153.
- **Blockers:** none (operator action).
- **Reopen conditions:** the slot is itself a Stage B precondition (src/insider/registration_check.py:56-64).
- **Cross-repo?:** yes — "the calibration ledger still holds zero independently formed entries" (REGISTRATION.md:883-885; progress.md:97-99) refers to NPDExperiment's adopted prior; the ledger itself is not in this repository.

### 10. Section 14.3 Carhart-residual MDE
- **Status:** not measured; "an amount this stage did not measure and will not measure". REGISTRATION.md:790-796; DECISIONS.md:29-32.
- **Deciding figure:** none; bounded above by 49.35 (REGISTRATION.md:578-583), n 2,581 sessions.
- **Blockers as stated:** "measuring it after seeing BLOCKED is choosing a method by its answer" REGISTRATION.md:793-794; ADR-001 "a factor regression on uncentered data produces an intercept and the intercept is the alpha" DECISIONS.md:29-31; factor data are not an SEC source (CLAUDE.md:61 "SEC access only. Zero paid APIs.").
- **Reopen conditions:** "must register the change as a numbered amendment, formed before measurement, in a repository that is not this one." REGISTRATION.md:794-796.
- **Cross-repo?:** possibly — any successor that regresses this repository's centered series on Carhart factors.
- **Audit note:** AUDIT-A-InsiderExperiment-3 — the second stated blocker does not bind, because the store is already centered (returns.py:292-293; dispersion.py:53-62) and a no-intercept regression on centered data yields the residual SD without producing an intercept. A beta-only step gives MDE 47.15, still BLOCKED; the three remaining factors would have to explain a further ~25.6 points of excess variance to reach 40.

### 11. ADR-007 market-capitalization weighting
- **Status:** the registered basis was "verified working" and not taken. DECISIONS.md:204-212; REGISTRATION.md:567-576.
- **Blockers as stated:** `company_tickers.json` lists only current registrants (21 of 25 sampled issuers present), DECISIONS.md:206-210; shares outstanding are not split-adjusted while the bars carry adjustment `all`, :210-212.
- **Reopen conditions:** none stated; the amendment clause REGISTRATION.md:8-9 applies in principle and is foreclosed by :800.
- **Cross-repo?:** possibly — a successor with a point-in-time cap weight.
- **Audit note:** AUDIT-A-InsiderExperiment-2 names a free SEC route that avoids both stated blockers (Form-4-derived symbol↔CIK map, corpus/build.py:120, :123, plus the DERA Financial Statement Data Sets cover fact), and records that the unmeasured registered weighting is bracketed by 34.29 and 49.35 with the bar at 40.

### 12. Section 4 universe narrowing
- **Status:** standing scope decision; the alternative is named, not run. REGISTRATION.md:303-329; DECISIONS.md:105-135.
- **Deciding figure (n):** 148,883 `outside_universe` against 9,160 that reached and passed the universe filter; 5.8%. REGISTRATION.md:656-658; DECISIONS.md:120-125; corpus.json:43.
- **Blockers:** "the operator cannot trade the illiquid tail at his cost band" REGISTRATION.md:319-324; the spread band 15.8-50.0 bp is a large-cap measurement, :404-407; config.py:139-140.
- **Reopen conditions:** "The honest alternative is a different universe" REGISTRATION.md:872-874; DECISIONS.md:336-338. A cost measurement for the next liquidity band is the precondition.
- **Cross-repo?:** yes — any repository holding a measured spread for smaller names, or bars for a wider universe (the source `analysis_bars.db` is 7,320,629,248 bytes, reports/stage_a1/port.json:10, against 1,218 distinct symbols copied, :4).

### 13. Section 2 / ADR-003 alternative regimes
- **Status:** rejected ex-ante. REGISTRATION.md:196-213; DECISIONS.md:78-101.
- **Blockers (as reasons):** 13F 45-day lag and ex-post manager selection, REGISTRATION.md:198-204; congressional 45-day lag and public competition, :206-209.
- **Reopen conditions:** "a different disclosure regime" is named as an honest alternative (REGISTRATION.md:873); no specific trigger is registered.
- **Cross-repo?:** yes — any repository testing 13F cloning or congressional disclosure.

### 14. ADR-009 survivorship leak
- **Status:** recorded limitation, not fixed. DECISIONS.md:258-280.
- **Deciding figure (n):** 13,750 name-sessions dropped, ~7.4% of held name-sessions (DECISIONS.md:264-265; power.json:118; src/insider/portfolio/returns.py:189-190).
- **Blockers:** none; the direction is toward GO for the second moment (DECISIONS.md:275-278), so it cannot have caused BLOCKED.
- **Reopen conditions:** "would have to be fixed before any Stage B first moment" DECISIONS.md:279-280.

### 15. Entry rule: registration versus code
- **Status:** open and unrecognised by the authors. Registration: "**Entry** is the close of the first session strictly after the filing date. A public filer reads the filing after it posts, so entry at or before the filing date would be unreachable." REGISTRATION.md:377-379. Code: membership holds the name on the entry session itself (src/insider/portfolio/membership.py:81-83; tests/test_membership.py:25-28) and the return credited on session j is close(j−1) → close(j) (src/insider/portfolio/returns.py:85-92, :196), so the book earns the filing-date-close to next-close move.
- **Deciding figure (n):** about 1.8 entry-day names per session in a mean 66.9-name priced book, n 2,581 sessions.
- **Blockers / direction:** none for this repository's verdict — the effect on a second moment is negligible and no first moment was read. It is a Direction B item (it would overstate reachable alpha), carried here because it is a Stage B precondition alongside ADR-009.
- **Reopen conditions:** must be reconciled — either the code or the registered sentence — before any successor reads a first moment.

### 16. ADR-008 and ADR-013 defects
- **Status:** closed and corrected in code. DECISIONS.md:226-255, :400-416. One label moved (`insufficient_history` → `routine`); the 43 silently merged events restored; the qualifying set stands at 4,585 and the MDE at 49.35 unchanged (DECISIONS.md:245-249).
- **Residue:** the Section 15.1 by-year table still carries the pre-fix merged counts, summing to 4,542 (AUDIT-A-InsiderExperiment-5; REGISTRATION.md:603-608 against corpus.json:4-14).

### 17. ADR-012 residual
- **Status:** open, deferred. "A future scaffold that wants the stronger property has to express it differently, and this repository did not solve it." DECISIONS.md:365-374; progress.md:62-67.
- **Cross-repo?:** yes — any scaffold ported from this one (DECISIONS.md:392-396).

### 18. Corpus cache pruning
- **Status:** discretionary, open. progress.md:144-149. 2,783,280,665 bytes on disk (REGISTRATION.md:832-833); the host has 328 GB free; "pruning is a preference and not a need."

### 19. Family record (cross-repo claim)
- **Statement:** "Eight price-based and signal-based hypothesis families have now been tested across AiTrader, HFExperiment, NPDExperiment and InsiderExperiment. **Zero have produced a positive result that survived its own registered bar.**" progress.md:103-105. "Two closed on power rather than on absent signal: H-F at z 1.668 against a 2.50 bar, and NPD at unresolved-at-achievable-power." progress.md:107-108. NPD figures as recited here: MDE 0.0512 against a realistic band of 0.01 to 0.05, 415 days, 6.9378 USD (REGISTRATION.md:21-25).
- **Cross-repo?:** yes — the eight-family count and the characterisation of HFExperiment's H-F closure are claims about other repositories.

### 20. AiTrader news-drift pointer
- "The running AiTrader news-drift experiment is untouched and unaffected. Its verdict remains due at 60 clusters." progress.md:122-123. A pointer only; nothing in this repository depends on it.

## Leads for the cross-repository pass

Every blocker or reopen condition above that a different repository might satisfy, with the repository I would look in first.

1. **A registration elsewhere that tests insider purchases on a wider or different universe, or on a different disclosure regime** (rows 1, 12, 13). Trigger text: REGISTRATION.md:872-874; DECISIONS.md:336-338. Where to look: no successor is named in this repository, so first check whether any repository in the program holds a **measured spread or cost band for a less liquid band** — that measurement is the stated precondition for widening the universe. Best guesses: **ORBExperiment** and **VRPExperiment** (equity/vol designs likely to carry their own cost assumptions), and **AiTrader** (holds the `analysis_bars.db` source behind port.json:4, :10 — 7,320,629,248 bytes against 1,218 distinct symbols copied, so a wider universe's bars may already exist there).
2. **A registration elsewhere naming an equal-weighted or cap-weighted calendar-time book as primary, carrying the ADR-011 disclosure** (rows 6, 11). Trigger text: REGISTRATION.md:865-870; DECISIONS.md:328-333. Where to look: any repository created after 2026-08-25 with a calendar-time equity book. Best guesses: **NPLExperiment** (commits on 2026-09-02, the most recent work in the program) and **ORBExperiment**; check their Section 0 / registration text for a citation back to InsiderExperiment A.1, which ADR-011 requires and whose absence would itself be a cross-repository finding.
3. **A Carhart-residual (or any factor-residual) dispersion computed elsewhere on a centered daily series** (row 10). Trigger text: REGISTRATION.md:794-796. Where to look: whichever repository already holds daily Fama-French/momentum factors, since CLAUDE.md:61 forbids non-SEC sources here. Best guesses: **HFExperiment** and **ETFExperiment** (equity factor work), then **AiTrader**. If any of them holds daily factor data, the "will not measure" blocker is satisfiable across a read-only boundary without breaching this repository's seal.
4. **An independently formed operator prior entering the calibration ledger** (row 9). Trigger text: REGISTRATION.md:882-885; progress.md:97-99. Where to look: **NPDExperiment** (named as the source of the adopted-rather-than-formed prior) and wherever the calibration ledger physically lives — it is not in this repository. Any repository with an operator-written prior would satisfy the Stage B precondition at registration_check.py:56-64 for a successor.
5. **The eight-family / zero-positive record and the "closed on power" characterisation of H-F** (row 19). Trigger text: progress.md:103-108. Where to look: **HFExperiment** (verify z 1.668 against a 2.50 bar and whether that closure was on power or on absent signal), **NPDExperiment** (verify MDE 0.0512 against the 0.01-0.05 band and 415 days / 6.9378 USD), **AiTrader** (verify the family count and that the news-drift experiment is still open at fewer than 60 clusters, row 20).
6. **ADR-012's unsolved config-guard property** (row 17), which the authors explicitly hand to "a future scaffold" (DECISIONS.md:365-374, :392-396). Where to look: any repository whose scaffold was copied from this one — check **NPLExperiment** and **ORBExperiment** first for the same `Config` guard shape, since a ported scaffold inherits the same residual.
7. **The 30-to-40 bp decayed-gross band with no citation** (AUDIT-A-InsiderExperiment-4; row 1's bar). Not a reopen condition of this repository, but a cross-repository check worth making: if any other repository in the program cites the same 2008-2024 replication with a source, the bar's provenance is recoverable; if the same uncited band appears elsewhere, it is a shared inherited assumption rather than a local one. Where to look: **HFExperiment** and **ETFExperiment** first (equity anomaly decay figures), then any repository citing Cohen-Malloy-Pomorski.
