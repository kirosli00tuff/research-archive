# InsiderExperiment — REOPEN LEDGER (Agent A, consolidated)

Repository `InsiderExperiment`, anchored SHA `12d9fd36cf055cb10ea67a3fc737e404217bc95a` (master, 2026-08-25).

Factual, not advocacy. Live HEAD equalled the anchor at read time (2026-09-03T06:35:25Z); no commits followed the
closure commit. The repository holds one hypothesis, two gates, three registered secondaries, one unwritten stage,
and one reserved operator slot. There is no explicit "reopen if" list anywhere in it; the reopen conditions below are
the "what would overturn it" clauses of the ADRs, the ADR-011 boundary, and the Section 17 amendment clause.

Closure dates are from the commit clock, which carries a -07:00 offset (see finding AUDIT-A-InsiderExperiment-7):
Section 0 `fbfc74e` 2026-08-25T18:34:56-07:00; Sections 1-16 `398755b` 18:38:50; corpus `ccc9b13` 18:47:16;
power gate `cb17046` 19:11:45; docs `d8b81f1` 19:11:55; closure `12d9fd3` 23:24:15.

## Summary table

| # | Entry | Status | Closure kind | Closure date | Deciding figure (n) | Cross-repo? |
|---|---|---|---|---|---|---|
| 1 | H1 Section 1 hypothesis: net-of-cost survival of Form 4 opportunistic/cluster purchases, liquid-500 | closed, untested (verdict row V7) | untestable-at-achievable-power (power gate BLOCKED) | 2026-08-25 (`cb17046`; closure `12d9fd3`) | MDE 49.35 bp/mo vs bar 40; n 2,581 sessions, N_eff 2,869.9, TE 9.993%, sd 62.95 bp | yes (rows 12, 18, 19) |
| 2 | Corpus gate (Section 0.3) | closed GO | gate cleared | 2026-08-25 (`ccc9b13`) | 4,585 events vs floor 1,000; coverage 99.5% vs 80% | no |
| 3 | Power gate, primary 126-session "value-weighted" (median-dollar-volume) book | closed BLOCKED | gate failed | 2026-08-25 (`cb17046`) | as row 1 | no |
| 4 | Secondary hold, 21 sessions VW | reported, non-verdict-bearing | none | 2026-08-25 | MDE 81.48 (n 2,513) | no |
| 5 | Secondary hold, 63 sessions VW | reported, non-verdict-bearing | none | 2026-08-25 | MDE 57.34 (n 2,563) | no |
| 6 | Secondary weighting, 126 sessions equal-weighted | reported, non-verdict-bearing, "would have fired DEGRADED", not promoted | none (declined) | 2026-08-25 | MDE 34.29 (n 2,581, N_eff 2,798.1, TE 6.856%) | possibly |
| 7 | Newey-West lag grid on the primary | reported | none | 2026-08-25 | 50.19 / 49.35 / 49.11 / 49.53 at lags 5/21/63/126 | no |
| 8 | Stage B: Carhart four-factor net alpha at the 100 bp round trip | never written; blocked | blocked by rows 3 and 9 | n/a | none (alpha sealed, unread) | no |
| 9 | Section 12 operator prior | open, outstanding | none | n/a | slot empty; assistant's 0.12 recorded beside it | yes (calibration ledger) |
| 10 | Section 14.3 Carhart-residual MDE | not measured; "will not measure" here | deferred to a different repository | 2026-08-25 | unmeasured; bounded above by 49.35 | possibly |
| 11 | ADR-007 market-capitalization weighting (registered basis of Section 7) | not run; proxy substituted | registered deviation | 2026-08-25 (`398755b`) | none measured | possibly |
| 12 | Section 4 universe narrowing / "a different universe" | scope decision, standing; alternative named, not run | registered narrowing | 2026-08-25 | 148,883 outside_universe vs 9,160 in; 5.8% | yes |
| 13 | Section 2 / ADR-003 alternative regimes (13F, congressional) | rejected ex ante | registered rejection | 2026-08-25 | 45-day lag | yes |
| 14 | ADR-009 survivorship leak (names dropped on leaving the universe mid-hold) | open limitation; must be fixed before any Stage B | recorded, not fixed | 2026-08-25 | 13,750 name-sessions, ~7.4% | no |
| 15 | ADR-008, ADR-013 implementation defects | closed (fixed) | corrected | 2026-08-25 | 1 label moved; 43 events un-merged | no |
| 16 | ADR-012 residual: config guard cannot tell enforce from display | open, deferred to next scaffold | recorded | 2026-08-25 | n/a | yes (any successor scaffold) |
| 17 | Corpus cache pruning | open, discretionary | none | n/a | 2,783,280,665 bytes | no |
| 18 | "Family record": eight families, zero positives | cross-repo claim, standing | none | 2026-08-25 | H-F z 1.668 vs 2.50; NPD MDE 0.0512 vs band 0.01-0.05 | yes |
| 19 | AiTrader news-drift experiment pointer | untouched, running elsewhere | none | n/a | verdict due at 60 clusters | yes |
| 20 | Entry-rule mismatch: registration vs code | open, undisclosed; must be fixed before any Stage B first moment | not recorded by the authors | n/a | ~1.8 entry-day names per session in a 67-name book | no |

## Detail

### 1. H1 — Section 1 hypothesis
- **Statement:** "Opportunistic and cluster insider purchases, disclosed on Form 4, predict positive abnormal returns that survive the operator's measured cost band at achievable size." REGISTRATION.md:165-167.
- **Status:** closed without the hypothesis being tested. "Verdict row **V7** fired, not V3." REGISTRATION.md:890-891; "It is not a null on the hypothesis." :771.
- **Closure kind:** untestable-at-achievable-power (Section 0 power gate fired BLOCKED). REGISTRATION.md:708, :812-816; DECISIONS.md:288-292; progress.md:14-18.
- **Closure date:** 2026-08-25 (`cb17046` 19:11:45-07:00 fired; `12d9fd3` 23:24:15-07:00 closed).
- **Deciding figure (n):** MDE 49.3543 bp per month against a BLOCKED floor of 40; daily excess-return SD 62.9519 bp; n = 2,581 sessions; VIF 0.8993; N_eff 2,869.9; TE 9.9933%; SE 24.6771 bp. REGISTRATION.md:712, :717-719; reports/stage_a1/power.json:6-12, :132-136.
- **Blockers:**
  (a) BLOCKED is terminal by registration: "Stage B is never written and the repo closes on the finding." REGISTRATION.md:43, :443.
  (b) "None in force. Section 0 fired BLOCKED, so no amendment can authorize Stage B." REGISTRATION.md:800.
  (c) Operator prior empty; blocks Stage B by code. REGISTRATION.md:508-511; src/insider/registration_check.py:56-64; src/insider/eval/evaluator.py:41.
  (d) The measured cost band applies only to the liquid band, so the universe cannot be widened at those costs. REGISTRATION.md:319-324; DECISIONS.md:127-130.
  (e) ADR-009 leak must be fixed before any first moment is read. DECISIONS.md:278-280.
  (f) Entry-rule mismatch (row 20) would also need correction before a first moment is read.
- **Reopen conditions:**
  (a) Amendment clause: "Changing a registered value after that commit requires a numbered amendment in Section 17 carrying its own evidence." REGISTRATION.md:8-9 — foreclosed inside this repository by :800.
  (b) ADR-010: "**What would overturn it.** Nothing inside this repository." DECISIONS.md:308-310.
  (c) ADR-011 boundary for equal-weight-as-primary in a fresh registration: it must "state in its own Section 0 that its primary weighting was selected after seeing a secondary result from InsiderExperiment A.1, and it must carry a correspondingly higher bar." REGISTRATION.md:865-870; DECISIONS.md:328-333.
  (d) "The honest alternative is a different universe or a different disclosure regime, neither of which inherits the seen number." REGISTRATION.md:872-874; DECISIONS.md:335-338.
  (e) A Carhart-residual revisit "must register the change as a numbered amendment, formed before measurement, in a repository that is not this one." REGISTRATION.md:794-796.
  (f) Successor work "goes in a NEW repository that reads this one across a read-only boundary" — untracked marker `_CLOSED_DO_NOT_RUN_HERE`, UNANCHORED, read 2026-09-03T06:32:15Z.
- **Possibly met by other repository?:** Yes, to check in the cross-repository pass — any repository that (i) runs a Form 4 or other insider design on a different universe (beyond the liquid-500) or a different disclosure regime, or (ii) registers an equal-weighted or cap-weighted calendar-time book with the ADR-011 disclosure. None is named anywhere in this repository.
- **Agent A finding against this row:** AUDIT-A-InsiderExperiment-1, -2, -3, -4.

### 2. Corpus gate (Section 0.3)
- **Status:** CORPUS-GO. REGISTRATION.md:594-596; reports/stage_a1/corpus.json:175.
- **Closure kind / date:** gate cleared, 2026-08-25 (`ccc9b13`; evidence ledger `corpus_gate` at 2026-08-26T01:42:24Z, UNANCHORED).
- **Deciding figure (n):** 4,585 qualifying events vs a floor of 1,000; 99.5411% of in-span sessions carrying a non-empty book vs a floor of 80%; mean book width 71.9090. REGISTRATION.md:594-596, :822-826; corpus.json:2, :173-174.
- **Blockers:** none.
- **Reopen conditions:** ADR-002 — "What would overturn it. A disagreement in the XML sample, or a full-index ratio that moved across quarters" DECISIONS.md:72-74. Not met: 25 agree / 0 disagree (DECISIONS.md:64-65; validation.json); index-to-dataset ratio 2.047-2.108 across quarters.
- **Cross-repo?:** no.

### 3. Power gate, primary series
- As row 1. Additional detail: weight concentration is named as the cause (REGISTRATION.md:745-757, :837-848); effective names 29.7313 of 71.909 held (portfolio.json:27, :7); top-1 weight 14.93%, top-5 33.79% (portfolio.json:23-24). The weighting basis actually run is median dollar volume, a registered deviation from value (capitalization) weighting: REGISTRATION.md:393-395, :566-576; DECISIONS.md:197-222; src/insider/portfolio/returns.py:102-103; src/insider/market/store.py:100-108.
- **Reopen conditions:** as row 1 (a)-(e). Also Section 14.3: the A.1 figure is registered as an upper bound on the Stage B figure, REGISTRATION.md:578-583.
- **Agent A finding against this row:** AUDIT-A-InsiderExperiment-2, -3, -4.

### 4-5. Secondary holds, 21 and 63 sessions
- **Status:** reported, non-verdict-bearing by registration. REGISTRATION.md:368-369, :474-476.
- **Deciding figures (n):** 21 sessions — MDE 81.4849, n = 2,513 sessions, TE 15.7032%, book 15.4 names (power.json:24-43; REGISTRATION.md:713). 63 sessions — MDE 57.3398, n = 2,563 sessions, TE 11.8273% (power.json:45-64; REGISTRATION.md:714).
- **Blockers / reopen conditions:** none registered.
- **Cross-repo?:** no.

### 6. Secondary weighting, 126 sessions equal-weighted
- **Status:** reported; "would have fired DEGRADED at 34.29 bp"; "**It is not promoted.**" REGISTRATION.md:764-767, :850-858; DECISIONS.md:318-327; progress.md:40-45.
- **Deciding figure (n):** MDE 34.2897 bp per month; n = 2,581 sessions; VIF 0.9224; N_eff 2,798.1; TE 6.8556%; SE 17.1449 bp; effective names 66.9252. REGISTRATION.md:715; power.json:69-75; portfolio.json:111.
- **Blockers:** registered as secondary before measurement (REGISTRATION.md:387, :474-476); promotion refused on the "by its answer" ground (:766-767; DECISIONS.md:325-326).
- **Reopen conditions:** the ADR-011 boundary (row 1 (c)); the authors' own assessment that such a registration is "borderline at best" (REGISTRATION.md:872; DECISIONS.md:335).
- **Cross-repo?:** possibly — any successor registration naming equal weight as primary must cite this repository (DECISIONS.md:330-333).
- **Agent A finding against this row:** AUDIT-A-InsiderExperiment-1.

### 7. Newey-West lag grid
- **Status:** reported. REGISTRATION.md:721-723; power.json:88-113. Verdict "does not turn on the bandwidth choice": 50.1903 / 49.3543 / 49.1057 / 49.5319 at lags 5 / 21 / 63 / 126, all above 40.
- **Blockers / reopen conditions:** none.
- **Cross-repo?:** no.

### 8. Stage B
- **Status:** never written. REGISTRATION.md:443, :800, :815-816; DECISIONS.md:291-292.
- **Blockers:** power gate BLOCKED (row 1 (a), (b)); operator prior empty (row 9); ADR-009 leak (row 14); entry-rule mismatch (row 20).
- **Reopen conditions:** none inside this repository (DECISIONS.md:308-310); a successor repository only (REGISTRATION.md:794-796; marker file).
- **Cross-repo?:** no — but see rows 1 and 10 for where a successor could live.

### 9. Section 12 operator prior
- **Status:** open, outstanding. "[ EMPTY. The operator writes a number here himself, before Stage B runs. ]" REGISTRATION.md:506; closes unfilled at :876-885; progress.md:93-99, :140-143.
- **Deciding figure:** none. The assistant's prior of 0.12 is recorded beside the empty slot (REGISTRATION.md:513; src/insider/config.py:153).
- **Blockers:** none technical — it awaits operator action.
- **Reopen conditions:** the slot is itself a Stage B precondition, enforced in code (registration_check.py:56-64).
- **Cross-repo?:** yes — "the calibration ledger still holds zero independently formed entries" (REGISTRATION.md:884-885; progress.md:97-99) refers to a calibration ledger that does not live in this repository.

### 10. Section 14.3 Carhart-residual MDE
- **Status:** not measured; "an amount this stage did not measure and will not measure". REGISTRATION.md:790-796; DECISIONS.md:29-32.
- **Deciding figure:** none. Bounded above by 49.3543 (REGISTRATION.md:579-583).
- **Blockers, as stated:** "measuring it after seeing BLOCKED is choosing a method by its answer" (REGISTRATION.md:793-794); ADR-001, "a factor regression on uncentered data produces an intercept and the intercept is the alpha" (DECISIONS.md:30-31); and the factor data are not an SEC source (CLAUDE.md:61, "SEC access only. Zero paid APIs.").
- **Reopen conditions:** "must register the change as a numbered amendment, formed before measurement, in a repository that is not this one." REGISTRATION.md:794-796.
- **Cross-repo?:** possibly — any successor that regresses this repository's centered series on Carhart factors.
- **Agent A finding against this row:** AUDIT-A-InsiderExperiment-3 (the second blocker does not hold on the already-centered store; Frisch-Waugh-Lovell yields the residual SD without producing the intercept, so the seal is not breached).

### 11. ADR-007 market-capitalization weighting
- **Status:** the route was "verified working" and not taken. DECISIONS.md:204-212; REGISTRATION.md:566-576.
- **Blockers, as stated:** `company_tickers.json` lists only current registrants (21 of 25 sampled issuers present), DECISIONS.md:207-210; shares outstanding are not split-adjusted against bars carrying adjustment `all`, :210-212.
- **Reopen conditions:** none stated. The amendment clause (REGISTRATION.md:8-9) applies in principle and is foreclosed by :800.
- **Cross-repo?:** possibly — a successor carrying a point-in-time capitalization weight, or holding a symbol↔CIK map or shares-outstanding panel.
- **Agent A finding against this row:** AUDIT-A-InsiderExperiment-4 (a free SEC route exists that neither blocker rules out: Form-4-derived `ISSUERCIK`/`ISSUERTRADINGSYMBOL` at src/insider/corpus/build.py:120, :123, plus DERA Financial Statement Data Sets).

### 12. Section 4 universe narrowing
- **Status:** standing scope decision; the alternative is named and was not run. REGISTRATION.md:303-329; DECISIONS.md:105-135.
- **Deciding figure (n):** 148,883 events filtered as `outside_universe/not_a_member_at_entry` versus 9,160 reaching and passing the universe filter; 5.8%. REGISTRATION.md:656-660; DECISIONS.md:120-125; corpus.json:43.
- **Blockers:** "the operator cannot trade the illiquid tail at his cost band" (REGISTRATION.md:319-324); the spread band of 15.8-50.0 bp is a large-cap measurement (:404-407).
- **Reopen conditions:** "The honest alternative is a different universe" REGISTRATION.md:872-874; DECISIONS.md:336-338. A measured cost band for the next liquidity tier is the precondition.
- **Cross-repo?:** yes — any repository holding a measured spread for smaller names, or bars for a wider universe (the source `analysis_bars.db` is 7.3 GB, port.json:10, against 1,218 symbols copied, :5).

### 13. Section 2 / ADR-003 alternative disclosure regimes
- **Status:** rejected ex ante. REGISTRATION.md:196-213; DECISIONS.md:78-101.
- **Blockers (as stated reasons):** 13F — 45-day lag and ex-post manager selection (:198-204); congressional — 45-day lag and public competition (:206-209).
- **Reopen conditions:** "a different disclosure regime" is named as the honest alternative (REGISTRATION.md:873); no specific trigger is registered.
- **Cross-repo?:** yes — any repository testing 13F cloning or congressional disclosure.

### 14. ADR-009 survivorship leak
- **Status:** recorded limitation, not fixed. DECISIONS.md:258-280.
- **Deciding figure (n):** 13,750 name-sessions dropped, ~7.4% of held name-sessions. DECISIONS.md:264-265; power.json:118; portfolio.json:16 (`"not_priced": 13750`).
- **Blockers:** none — for the second moment the direction is toward GO (DECISIONS.md:275-278), so it cannot have caused BLOCKED.
- **Reopen conditions:** "would have to be fixed before any Stage B first moment" DECISIONS.md:279-280.
- **Cross-repo?:** no.

### 15. ADR-008 and ADR-013 implementation defects
- **Status:** closed, corrected. DECISIONS.md:226-255, :400-416. One label moved (`insufficient_history` → `routine`); 43 merged events restored; the qualifying set stayed at 4,585 and the MDE at 49.35 (:245-249).
- **Residual:** the published Section 15.1 by-year table still carries the pre-fix merged counts summing to 4,542 — see AUDIT-A-InsiderExperiment-5.
- **Cross-repo?:** no.

### 16. ADR-012 residual
- **Status:** open, deferred. "A future scaffold that wants the stronger property has to express it differently, and this repository did not solve it." DECISIONS.md:365-374; progress.md:62-67.
- **Cross-repo?:** yes — any scaffold ported from this one inherits the same config-guard weakness (DECISIONS.md:392-396).

### 17. Corpus cache pruning
- **Status:** discretionary, open. progress.md:144-149. 2,783,280,665 bytes cached; host has 328 GB free; "pruning is a preference and not a need."
- **Cross-repo?:** no.

### 18. Family record (cross-repository claim)
- **Statement:** "Eight price-based and signal-based hypothesis families have now been tested across AiTrader, HFExperiment, NPDExperiment and InsiderExperiment. **Zero have produced a positive result that survived its own registered bar.**" progress.md:103-106. And: "Two closed on power rather than on absent signal: H-F at z 1.668 against a 2.50 bar, and NPD at unresolved-at-achievable-power." :107-108. NPD figures quoted here: MDE 0.0512 against a band of 0.01-0.05, 415 days, 6.9378 USD (REGISTRATION.md:21-25).
- **Cross-repo?:** yes — the eight-family count, and the characterization of HFExperiment's H-F closure (z 1.668 vs 2.50) as a power closure rather than an absent-signal closure, are claims about other repositories.

### 19. AiTrader news-drift pointer
- "The running AiTrader news-drift experiment is untouched and unaffected. Its verdict remains due at 60 clusters." progress.md:122-123.
- **Cross-repo?:** yes — a pointer only; nothing in this repository depends on it.

### 20. Entry-rule mismatch, registration versus code
- **Status:** open and undisclosed. Not recorded by the authors anywhere in REGISTRATION.md, DECISIONS.md or progress.md.
- **Statement in the registration:** "**Entry** is the close of the first session strictly after the filing date … entry at or before the filing date would be unreachable." REGISTRATION.md:377-379.
- **What the code does:** membership holds the name on the entry session itself (src/insider/portfolio/membership.py:81-83; tests/test_membership.py:25-28 asserts `held == ["2020-01-05", …]` for entry 2020-01-05), and the return credited on session j is close(j−1) → close(j) (src/insider/portfolio/returns.py:85-92, :196). The book therefore earns the filing-date-close to next-close move — entry at the filing date's close, which the registration calls unreachable.
- **Deciding figure (n):** about 1.8 entry-day names per session in a book averaging 66.93 priced names (n = 2,581 sessions), so the effect on the second moment is negligible and the BLOCKED verdict does not turn on it.
- **Blockers:** none; it is a defect, not a decision.
- **Reopen conditions:** it must be fixed, alongside ADR-009, before any Stage B first moment is read. It is a Direction B observation (it would overstate a claim, not close one early) and is carried here so a successor inherits it.
- **Cross-repo?:** no — but any scaffold ported from this repository (row 16) inherits the same membership code.

## Leads for the cross-repository pass

Every blocker or reopen condition above that might be satisfied, contradicted, or already answered by work in another
repository, with the best guess of which repository to look in.

1. **A registration elsewhere testing insider purchases on a wider or different universe, or a different disclosure regime** (rows 1, 12, 13). Trigger text: REGISTRATION.md:872-874; DECISIONS.md:336-338. *Best guess:* no sibling repository is named in this one; check `HFExperiment`, `ORBExperiment`, `PMExperiment` and `NPLExperiment` for any Form 4, 13F or congressional-disclosure design, and any repository holding a measured spread for a smaller-cap liquidity tier — the cost band, not the signal, is what blocks the universe widening.
2. **A registration elsewhere naming an equal-weighted or capitalization-weighted calendar-time book as primary, carrying the ADR-011 disclosure** (rows 6, 11). Trigger text: REGISTRATION.md:865-870; DECISIONS.md:328-333. *Best guess:* any post-2026-08-25 registration in the program. `NPLExperiment` (commits to 2026-09-02) and `PMExperiment` (to 2026-09-02) are the only repositories that moved after this closure, so they are where an ADR-011-conforming successor would have to appear. If one names equal weight as primary without citing InsiderExperiment A.1, that is a cross-repository provenance failure.
3. **A Carhart-residual dispersion computed elsewhere on a centered series** (row 10). Trigger text: REGISTRATION.md:794-796. *Best guess:* any repository already carrying Fama-French/momentum daily factors — check `ETFExperiment`, `VRPExperiment` and `AiTrader` for a factor-data path. If the factor panel already exists in the program, the "not an SEC source" blocker at CLAUDE.md:61 costs nothing but a registered note, and the row-10 deferral is weaker than it reads.
4. **An independently formed operator prior entering the calibration ledger** (row 9). Trigger text: REGISTRATION.md:882-885; progress.md:97-99. *Best guess:* `NPDExperiment` — the registration's own framing points at NPD's adopted prior, and the calibration ledger is not in this repository. Check whether the ledger exists at all, whether it holds any independently formed entry, and whether the "zero independently formed entries" claim was still true at that repository's anchor.
5. **The eight-family, zero-positive record and the "closed on power" characterizations** (row 18). Trigger text: progress.md:103-108; REGISTRATION.md:21-25. *Best guess:* `HFExperiment` for the H-F z 1.668 against a 2.50 bar; `NPDExperiment` for MDE 0.0512 against a 0.01-0.05 band, 415 days, 6.9378 USD; `AiTrader` for the family count and for row 19's news-drift verdict "due at 60 clusters". Check the count of eight, and check whether each closure is characterized the same way in its own repository as it is here.
6. **The uncited 30-to-40 bp decayed gross band** (AUDIT-A-InsiderExperiment-2, which sets the bar behind row 1). *Best guess:* if any other repository in the program cites a decayed insider-alpha magnitude for 2008-2024 with an author and year, that citation would source this bar; if the same uncited band appears in another registration, it is a shared-provenance failure rather than a local one. Grep the program for "30 to 40 bp", "decayed gross band" and "Cohen, Malloy".
7. **The ADR-012 config-guard residual and the membership/entry-rule defect** (rows 16, 20). Trigger text: DECISIONS.md:392-396. *Best guess:* any repository whose scaffold was ported from or to this one. If a sibling carries the same `registration_check` shape or the same membership code, it carries both defects; the entry-rule one is undisclosed and would matter wherever a first moment actually gets read.
