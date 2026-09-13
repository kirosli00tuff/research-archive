# POSITIVES LEDGER — retail-power-limits @ dda39b2f148569a6fe9be956a979471b2330611d

Factual, not advocacy. Feeds the cross-repository pass.

**Structural note that governs every row.** This repository measured nothing. It holds no
market data, opens no data source and computes no statistic (README.md:53-54). It therefore
has no hypothesis register, no registered bar of its own over data, and no verdict rows. Its
"positives" are (a) one asserted cross-experiment conclusion, (b) shipped artifacts, and
(c) transcribed figures whose bars were registered in *sibling* repositories. Rows of type
(c) carry the sibling's bar and registration date as this repository reports them; verifying
those against the sibling is the cross-repository pass's job, not mine — I read only
`snap/retail-power-limits/` plus this repository's live git history.

**Registration dates available in this repository.** The repository has three commits, all on
2026-08-29 between 00:19:47 and 00:21:28 −07:00 (`git log`, live repo, read 2026-09-03).
All six ADRs are dated "Accepted, 2026-08-29" (DECISIONS.md:10, 58, 89, 123, 154, 179). There
is no amendment log, no bar that pre-dates any data, and no data. **No amendment in this
repository touches any bar** — the only content amendment (`710093d`) changes "Three limits"
to "Four limits" in a scope lead-in, which strengthens rather than relaxes a caveat.

---

## A. The asserted conclusion (the repository's one positive claim)

| # | claim as stated | kind | deciding figures (n) | file:line | bar + registration date | amendments touching the bar | corrections applied | framing in README / note |
|---|---|---|---|---|---|---|---|---|
| A1 | "Across four independent pre-registered experiments, the binding constraint was not whether a published effect exists but whether an achievable sample could detect an effect of the reported size." | **positive (asserted conclusion)** | n = 4 cases, selected from 7 supplied repositories (8 with AiTrader); contrast set n = 3 repositories carrying ≥11 closed hypotheses | README.md:3-5; docs/the-power-limit.md:11-13 | **No bar.** No registered inclusion rule, no significance threshold, no pre-specified count. The case set was supplied: "The governing instruction named seven repositories to read in full" (progress.md:22-24); "The note was commissioned against seven repositories" (tests/test_sources.py:42). Roles assigned in progress.md:38-45. | none (repo has no amendment log) | **No multiplicity, selection, survivorship or clustering correction of any kind.** Four qualitative scope limits are stated instead (docs/the-power-limit.md:32-60) and the counter-hypothesis is volunteered (:393-401). | README leads with it in bold; note repeats it as "The claim" (:9-19). Scope-limit sentence pinned in both by tests/test_honesty.py:53-70. |
| A2 | "Each closed at *unresolved at achievable power*, at *untestable at achievable power*, or *BLOCKED* on a power gate — never on a measured null." | **positive (asserted conclusion)** | n = 4; but HFExperiment's own verdict label is a fourth category, "resolved on statistical power, not absent signal" (README.md:23) | README.md:5-7; docs/the-power-limit.md:15-17 | no bar | none | Corrected in the note and ADR-004 ("**HFExperiment did not fire a power gate.**", docs/the-power-limit.md:141-146; DECISIONS.md:121-148) — **not** in the README (grep: "AiTrader" 0, "inherit" 0, "broker" 0, "IBKR" 0 in README.md). | README states the categorical form uncorrected. |
| A3 | "That progression from expensive discovery to cheap refusal is the transferable output, and it matters more than any individual closure." | **positive (asserted conclusion)** | 6.9378 USD / 411 min / one-shot store spent vs 0 USD / ~71 min / store intact (n = 2 experiments) | README.md:37-39; docs/the-power-limit.md:155-160, table :236-243 | no bar | none | Self-limited: "The dollars are not the story; under seven dollars is not an expensive mistake" (docs/the-power-limit.md:245); prior art conceded at :262-272 (solclear fired an underpowered rule 11 days earlier). | README carries "fired BLOCKED at zero dollars" without the note's dollars-are-not-the-story caveat. |
| A4 | "They were not sampled from a population of hypotheses; they are the hypotheses one operator happened to run in a five-week window." | **positive (scope assertion)** | n = 7 supplied repositories; MLCryptoEngine alone contributes "Eleven hypotheses, nine tested and closed" counted as one contrast case (SOURCES.md:168) | docs/the-power-limit.md:39-41 | no bar; population never enumerated | none | none | Presented as a limitation, i.e. as a concession; challenged in DRAFT-all-4. |

---

## B. Shipped artifacts

| # | artifact | kind | deciding figures (n) | file:line | bar + registration date | amendments | corrections applied | framing |
|---|---|---|---|---|---|---|---|---|
| B1 | The note, `docs/the-power-limit.md` — "a detectability result about retail-scale replication" | **shipped** | 407 lines; ~90 figures claimed (DECISIONS.md:35); 18 of 205 numeric tokens (8.8 %) inside drift-tested generated blocks | docs/the-power-limit.md:1-407 | ADR-001, accepted 2026-08-29 (DECISIONS.md:8-52) | none | four figure corrections in the body rather than a footnote (docs/the-power-limit.md:118-153; ADR-003) | README.md:14 "Read the note"; pyproject.toml:4 description. |
| B2 | `SOURCES.md` — "maps each one to the repository, the file and the commit it came from" | **shipped** | 24 source entries; 285 numeric tokens, 278 inside generated blocks; **0 citations verified against any sibling repository by any test** | SOURCES.md:3-6 | ADR-002, accepted 2026-08-29 (DECISIONS.md:56-83) | none | 4 of 7 siblings disclosed as unpublished and uncheckable (SOURCES.md:257-288) | README.md:25-26 "Full extraction, every figure with its repository, file and commit". Challenged in DRAFT-all-6. |
| B3 | The honesty tests, `tests/test_honesty.py` — "A future session cannot quietly soften the scope limit or drop an inconvenient number." | **shipped** | 10 of 112 collected tests; 2 pin detectors, 2 canaries, 1 overclaim detector with **no** canary, 2 credential tests + 1 genuine canary | README.md:80-83; tests/test_honesty.py:1-19; DECISIONS.md:152-173 | ADR-005, accepted 2026-08-29 | `dda39b2` added `test_the_credential_scan_has_something_to_scan` (vacuity guard for the credential scan only) | non-emptiness guards added for the credential scan (tests/test_honesty.py:185) and the drift test (tests/test_render.py:28); **not** for `SCOPE_PINNED` or `FIGURES_PINNED` | README.md:75-83 "The honesty tests". Challenged in DRAFT-all-2 (pins pass vacuously in both hollowing modes; canaries pass in all three states). |
| B4 | The drift machinery, `rplimits/render.py` + `docsync.py` — "Prose and data cannot diverge silently." | **shipped** | 4 generated blocks; all 4 verified byte-identical to their rendered form at the anchor; README.md excluded (`DOCUMENTS`, docsync.py:77) — 0 of its 37 numeric tokens covered | DECISIONS.md:74-76; SOURCES.md:16-17 | ADR-002, accepted 2026-08-29 | none | two build-time defects in this machinery found and fixed (progress.md:72-88) | README.md:64-65 "the renderers for the generated blocks in the documents". Challenged in DRAFT-all-3 (README's table already diverges from the generated one). |
| B5 | The 411-minute derived figure, flagged as derived | **shipped (flagged derivation)** | 22 + 34 + 68 + 52 + 194 + 41 = 411 min, n = 6 stages; excludes untimed Z.1 | SOURCES.md:292-300; DECISIONS.md:177-193 | ADR-006, accepted 2026-08-29 | none | recomputed by me: **411, correct** | "Every other number in this repository is quoted, not computed" (SOURCES.md:300). Challenged in DRAFT-all-5 (at least 6 further computed numbers). |
| B6 | `tests/` — "111 tests" as the recorded gate evidence | **shipped (stale)** | stated 111 (progress.md:59, :68); actual **112** (static enumeration; commit `dda39b2`'s own message says "112 tests") | progress.md:67-68 | gate = `make check` (Makefile:193) | `dda39b2` added the 112th test and did not update the figure | none | progress.md states 111 twice as current fact. Challenged in DRAFT-all-7. |
| B7 | `test_there_are_exactly_four_power_cases` — "A fifth would change the claim, not extend it." | **shipped (pinned denominator)** | `assert len(POWER_CASES) == 4` | tests/test_cases.py:31-32 | ADR-005 discipline, 2026-08-29 | none | none | Framed as a drift guard; also makes the case count unamendable by the build. Noted in DRAFT-all-4. |

---

## C. The four power cases (transcribed positives-of-a-negative-kind; each rests on a sibling's threshold)

Every row below is a **thresholded closure**: a verdict that turned on a comparison against a
bar. The bar, its registration date and its amendment history live in the sibling repository;
what follows is what *this* repository reports about them. All four sibling repositories are
recorded as unpublished (SOURCES.md:268-271).

| # | claim as stated | kind | deciding figures (n) | file:line | bar + registration date (as reported here) | amendments touching the bar (date, data existed?) | corrections applied | framing in README / note |
|---|---|---|---|---|---|---|---|---|
| C1 | "0.0512 minimum detectable contrast, above the entire 0.01 to 0.05 band, against a pre-registered projection of 0.026 to 0.047." → "The numeric-LLM question is unresolved at achievable power." | **thresholded negative** | MDE 0.0512 vs band 0.01–0.05; realized contrast sd 0.36339 vs registered ≤0.2626; n = 415 stored rankings of 432 eligible days (96.1 %), 404 evaluable, **125.6 independent-equivalent** after VIF 3.4; 920 billed calls | SOURCES.md:38, :42, :54 | Effect band 0.01–0.05 "registered in Section 9.2 **before any call went out**" (SOURCES.md:34); closing commit `2d3d0ae`, 2026-08-25 | **A post-hoc amendment was voided**: "When a post-hoc amendment proposed scoring the same data at two more horizons, the registration voided it: *scoring spent data against new horizons is a second look however it is labelled*" (docs/the-power-limit.md:250-252) — i.e. an amendment was refused **after** the data existed. Reported here as a refusal, not a rescue. | Overlap/variance-inflation correction applied (3.4x, 427→125.6 effective days). Registered risk in ADR-007 acknowledged as non-binding: "a risk is a note and a gate is a decision" (docs/the-power-limit.md:356-359). | README.md:20 table row; docs/the-power-limit.md:72, :81-88, :161-178. Correction #1 (the "415 days" scope) at :124-130. |
| C2 | "49.35 bp per month, above the whole gross band and the whole net band, against a registered BLOCKED floor of 40 bp committed before the measurement existed." → "The registered primary design cannot resolve the effect at achievable power ... Stage B is never written." | **thresholded negative** | MDE **49.35** bp/mo vs BLOCKED floor **40**, gross band 30–40, net band 13.3–34.7; n = **4,585** events vs floor 1,000; 2,581 sessions at 99.5 % vs floor 80 %; **N_eff 2,869.9** (VIF 0.899 < 1); book 71.9 names behaving as **29.7**; TE 9.993 % | SOURCES.md:66, :70, :74, :78, :86 | Bars **20 bp GO / 40 bp BLOCKED**, derived from the decayed literature band, committed in the repository's **first commit** `fbfc74e`, 2026-08-25, "before the corpus existed, before the portfolio existed" (docs/the-power-limit.md:218-225); boundary convention written down ("An MDE of exactly 20.00 bp is GO", :223-224) | **none reported.** Gate fired as registered at commit `cb17046` (sources.py:88-94). | Newey-West bandwidth robustness reported (50.19 at lag 5, 49.11 at lag 63, 49.53 at lag 126 — SOURCES.md:70). Universe scope disclosed: "94.2 percent of qualifying-shaped insider purchases happen outside the liquid-500 band this design could trade" (SOURCES.md:90). **Not corrected for the design choice that produced the number**: the equal-weighted secondary on the identical names lands at **34.29** bp, below the 40 floor and below the top of both bands (docs/the-power-limit.md:228, :386-389) — registered as non-verdict-bearing and correctly not promoted. | README.md:21; docs/the-power-limit.md:73, :90-97, :180-232. **"Sample required. Not a sample requirement."** (SOURCES.md:78) appears nowhere in README.md. Challenged in DRAFT-all-1. |
| C3 | "H1 closes at untestable-at-achievable-power. The registered design cannot resolve the effect at the sample size reachable by the registered deadline of 2027-03-31. The signal was never read and this closure is not evidence about it." | **thresholded negative** | **11** admissible days at closure from a **336**-row census; **163** projected at the 2027-03-31 deadline at 20.8 admissible days/month; vs governing minimum **300** (E1 237, E2 300 at published 0.18; E1 845, E2 >1,200 at registered 0.09); archive capture density 11/333 = **3.30 %** vs a registered **60 %** bar | SOURCES.md:102, :106, :110, :118; docs/the-power-limit.md:99-105 | Registered effect 0.09 vs published 0.18; "Section 10 requires both co-primaries, so the governing minimum is 300" (SOURCES.md:102); registered deadline 2027-03-31; closing commit `3f5d629`, 2026-08-28 | **Amendment 6 exists and post-dates the data** (the census was measured): it prices a 14-month extension at "about 302 admissible days by 2027-10-31, which clears the governing 300 at the published 0.18 by two days and clears nothing at the registered 0.09" (SOURCES.md:122). Reported here as belonging to a *different question* than the closure — i.e. it did not rescue the verdict. **Also amended:** `etf-disarm` commit `4d11002`, 2026-08-28, "correct the reopen-path mislabel in Amendment 5 and ADR-019" (sources.py:123-129) — a correction against interest. | Powers reported at three magnitudes (0.18 published, 0.09 registered, 0.045 quartered — SOURCES.md:98). Correction #2 separates Amendment 6's triple from the closure (docs/the-power-limit.md:132-139). | README.md:22 — **carries the Amendment-6 triple (845 / above 1,200 / 302 by 2027-10-31) in the "against" column of the closure table**, i.e. the retracted comparison, with no correction and without stating the second deadline. tests/test_honesty.py:95-97 pins those three figures into the README. Challenged in DRAFT-all-3. |
| C4 | "H-F is 12-1 cross-sectional momentum, tested once in the AiTrader cross-sectional round of 2026-07-26 and resolved on statistical power rather than absent signal." | **thresholded negative (inherited)** | **z 1.668** vs **corrected bar 2.50**; excess 27.99 bp/day vs ~418 bp/day noise (TE 66.4 %/yr); needed **104.0 %/yr**, delivered **70.5**; interval −4.9 to +60.9; n = one 2.55-year holdout, **touched once**; **zero** forward shadow observations; forward verdict priced at 2,061 days to clear zero, 2,852 to clear the 4.07 bp/day cost hurdle | SOURCES.md:130, :134, :138, :142, :150 | Bar **2.50**, described only as "a corrected bar" — the correction's basis and date are **not stated in this repository**. My recomputation: two-sided p at z = 2.50 is 0.01242 ≈ 0.05/4, and Bonferroni m = 4 at α = 0.05 gives z = 2.4977 — consistent with a family of four. Section 11 verdict schedule registered 2026-08-23 (docs/the-power-limit.md:266-268). | none reported. HFExperiment closed **by operator decision** 2026-08-26 with the shadow series never started (SOURCES.md:154). | Width robustness reported (5→50 names: TE 66.4→31.7 %, excess 27.99→10.04 bp/day, z 1.668→1.455; SOURCES.md:134). Correction #3: "HFExperiment did not fire a power gate ... Its own Section 0 fired BLOCKED on the *broker*" (docs/the-power-limit.md:141-146). Deciding figure sourced to a **fifth repository**, AiTrader/RETURN.md @ f819b68 2026-07-29 (cases.py:262, :428; sources.py:158-164). | README.md:23 presents "z 1.668 against a corrected bar of 2.50" as HFExperiment's own measured detectability. README contains no mention of AiTrader, inheritance, the broker or IBKR. Challenged in DRAFT-all-8. |

---

## D. The three contrast cases (transcribed; carried to bound the claim)

| # | claim as stated | kind | deciding figures (n) | file:line | bar + registration date (as reported here) | amendments | corrections applied | framing |
|---|---|---|---|---|---|---|---|---|
| D1 | MLCryptoEngine: "Eleven hypotheses, nine tested and closed, and not one closed on power." | **thresholded negative (cost-bound / signal-absent)** | AUC **0.9432** at 100 ms, capture **0.0291** bps/trade vs Kraken 50 bps round trip (**~1,700x**) and vs Hyperliquid 3 bps (**~100x**); H4 break-even costs 300–550 bps vs 3 bps actual (**100–180x**); n = 11 hypotheses, 9 closed | SOURCES.md:168, :172 | register's own two-way split cost-bound vs signal-absent; HYPOTHESES.md @ `d2a0f05`, 2026-08-12; h1 note @ `ae03bf6`, 2026-08-22 | none reported | Correction #4: the 0.03 bps miss is against 50 bps, not 3 (docs/the-power-limit.md:148-153; DECISIONS.md:108-110). H6 closed "under an order-lifecycle fill model" (SOURCES.md:168) — a fill-model correction. Recomputed: 50/0.0291 = 1,718; 3/0.0291 = 103; 550/3 = 183. All as stated. | README.md:40-42; docs/the-power-limit.md:280-293. Repository **is public** (SOURCES.md:264). |
| D2 | solattn: "A powered null. Kill criterion K1 fired at 100.0 percent outcome coverage on every analysed cohort, and all 120 computable cells carry a negative point lift with none positive at any significance level." | **thresholded negative (powered null)** | lift **−1.0779** net of a 450 bps cost band; **day-clustered** 95 % bootstrap interval [−3.3354, +0.0204]; n = **12,798** pools over 3 birth days, 2,107 measurable at d0+2, Q5 cell n = **412**; 120 computable cells | SOURCES.md:180, :184 | kill criterion K1, registered; FINDINGS.md @ `b3f5062`, 2026-08-28 | Amendment 7 "records the Stage B readout and the horizon never analysed" (sources.py:186-192) — an amendment recording an untested horizon, not rescuing a verdict | **Clustering correction applied** (day-clustered bootstrap); cost band applied (450 bps); coverage 100.0 % | README.md:40-42; docs/the-power-limit.md:295-302. Repository **is public**. The most fully corrected negative anywhere in this ledger. |
| D3 | solclear: "the earliest power-shaped refusal in the program ... 18 cleared against a floor of 20 at 30 days, and 4 at 90 days — so no significance was claimed in either direction" | **thresholded negative (registered underpowered rule)** | **18** cleared vs floor **20** at 30 d; **4** at 90 d; all 18 realized −100 % net; share ever above entry **0 %** of 18; confirmation re-priced at **4,695,489** weighted credits, **37.6x** the stale 124,764 | SOURCES.md:192, :196 | registered underpowered rule, floor 20, "registered before the measurement and fired on 2026-08-14" (SOURCES.md:200); FINDINGS.md @ `c692032`, 2026-08-22 | none reported | **Survivorship correction is the headline finding**: "archived-page sampling manufactures survivorship by 60 points at 30 days and 79 at 90, 97.5 percent death on 40 birth-ordered pools against 18.75 percent on 16 attention-crawled ones" (SOURCES.md:196) | README.md:40-42; docs/the-power-limit.md:304-312. Repository **is public**. Used to date the shift; the note concedes it fired 11 days before NPDExperiment. |

---

## E. Open hypotheses

**None.** This repository registers no hypothesis and opens none. All seven cited siblings are
reported closed (SOURCES.md:8: "The sibling repositories are closed."). progress.md:138-141:
"### Outstanding — None inside the repository. The four sibling experiments remain closed and
were not touched." There is therefore **no open hypothesis that should already have closed on
its own registered rule** in this repository.

The one thing left open is not a hypothesis but an operator action, and it is disclosed:
publishing the four unpublished sibling repositories, "an operator decision, and it is outside
this repository's boundary" (progress.md:126-127).

---

## F. Cross-repository flags

Items this repository asserts that only the siblings can settle. Listed for the cross-repository
pass; **not** claimed as findings here.

1. **Every C-row figure is a transcription.** No test in this repository resolves a commit,
   opens a sibling file, or checks that a quoted string appears at the cited location
   (tests/test_sources.py checks only field non-emptiness, a `^[0-9a-f]{7}$` hash shape, and a
   `^2026-\d{2}-\d{2}$` date). 74 of 112 collected tests are these format assertions over a
   24-entry hand-typed registry.
2. **C4's "corrected bar of 2.50"** — the correction's basis, size and date are not stated in
   this repository. Whether it was set before or after z 1.668 was known is answerable only in
   AiTrader/HFExperiment.
3. **C2's registered BLOCKED floor of 40** and the claim it was committed in InsiderExperiment's
   first commit `fbfc74e` before the corpus existed — checkable only there.
4. **C3's Amendment 6** — whether it responded to an observed outcome (the ETF closure states
   no outcome value was ever read, SOURCES.md:114) is checkable only in ETFExperiment.
5. **C1's voided post-hoc amendment** (two extra horizons on spent data) — checkable only in
   NPDExperiment.
6. **The population question behind A4** — whether the seven supplied repositories are all the
   hypotheses the operator ran in the stated five-week window. The program contains further
   repositories not cited here.
7. **The unit mismatch in A1/A4** — 4 power *repositories* against 3 contrast *repositories*
   carrying ≥11 closed hypotheses (MLCryptoEngine 9, solattn 1, solclear ≥1).
