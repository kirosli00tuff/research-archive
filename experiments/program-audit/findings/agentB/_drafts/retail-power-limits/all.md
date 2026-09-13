# Agent B draft findings — retail-power-limits @ dda39b2f148569a6fe9be956a979471b2330611d

Direction B: the program claimed more than it earned. Eight draft findings.

Scope note. This repository is a *secondary source*: it holds no data and computes no
statistic. Every finding below is therefore about (a) its own claims about itself, (b) the
machinery it ships as a guarantee, or (c) an inference it draws that its own transcribed
figures do not support. I did **not** read the sibling snapshots (assignment restricts me to
`snap/retail-power-limits/` plus this repository's live git history), so no finding here
asserts that a transcribed figure is wrong; where a claim depends on a sibling's contents I
say so and flag it for the cross-repository pass.

---

### DRAFT-all-1
- **Repository / SHA:** retail-power-limits / dda39b2f148569a6fe9be956a979471b2330611d
- **Hypothesis or artifact:** The headline conclusion — that in all four cases the binding constraint was achievable sample size — as applied to InsiderExperiment.
- **Direction:** B
- **Class:** UNSUPPORTED_POSITIVE
- **Severity:** S2
- **Label:** DERIVED
- **Claim challenged (verbatim quote):** "**Across four independent pre-registered experiments, the binding constraint was\nnot whether a published effect exists but whether an achievable sample could\ndetect an effect of the reported size.**" — retail-power-limits/README.md:3-5 (same claim, reworded, at retail-power-limits/docs/the-power-limit.md:11-13: "Across four independent pre-registered experiments, the binding constraint was not whether a published effect exists. It was whether a sample an individual could actually assemble could detect an effect of the size that was reported.")
- **Evidence:**
  - Every sample-size input for InsiderExperiment cleared its registered bar, by the repository's own record: "4,585 qualifying events against a registered floor of 1,000; 2,581 sessions at 99.5 percent coverage against a floor of 80 percent; 2,869.9 effective independent periods, which exceeds the raw session count because the variance inflation of 0.899 is below one" — retail-power-limits/SOURCES.md:74 (n = 4,585 events; n = 2,581 sessions; N_eff = 2,869.9), identical string at retail-power-limits/rplimits/cases.py:152-154.
  - The repository states outright that sample size was not the binding term: "**Sample required.** Not a sample requirement." — retail-power-limits/SOURCES.md:78 (also rplimits/cases.py:158). The same field attributes the whole result to concentration: "The 9.993 percent annualized tracking error is the whole of the 49.35" — retail-power-limits/SOURCES.md:78.
  - A pre-registered variant on the *identical* sample would have cleared the bar: "The equal-weighted secondary, on the identical 71.9 names, would have landed at 34.29 bp and fired DEGRADED." — retail-power-limits/docs/the-power-limit.md:227-229 (n = 71.9 names, the same book).
  - 34.29 sits below the registered BLOCKED floor of 40 (retail-power-limits/SOURCES.md:70), inside the decayed gross band 30–40, and below the top of the net band 13.3–34.7 (retail-power-limits/SOURCES.md:66). So on the identical achievable sample, a weighting choice moves the design from "resolves none of the band" to "resolves the top of both bands".
  - The note itself names the mechanism in a later section: "InsiderExperiment is the clearest instance: its verdict turned entirely on tracking error, and its own equal-weighted secondary on the identical names would have landed at 34.29 bp instead of 49.35." — retail-power-limits/docs/the-power-limit.md:386-389.
  - The closing commit subject the repository cites for this case says the same: "Close at BLOCKED on the power gate, weight concentration not corpus, artifacts preserved" — retail-power-limits/rplimits/sources.py:100 / SOURCES.md:222.
- **Recomputation (if any):** Inputs: 4,585 events and floor 1,000 (SOURCES.md:74); 34.29 bp (docs/the-power-limit.md:228); BLOCKED floor 40 and bands 30–40 / 13.3–34.7 (SOURCES.md:66, :70). Method: direct comparison. Result: 4585/1000 = 4.585x over the corpus floor; 2,869.9 > 2,581 raw sessions (variance *deflation*, VIF 0.899 < 1 — recomputed implied VIF 2581/2869.9 = 0.89933, consistent with the stated 0.899); 34.29 < 40 (BLOCKED floor), 34.29 < 34.7 (top of net band), 34.29 inside 30–40 (gross band). No sample-size quantity in this case failed any bar.
- **What would resolve it:** Either (a) restating the headline as three cases plus one portfolio-construction closure, or (b) evidence from InsiderExperiment's REGISTRATION.md that the value-weighted primary was itself forced by an achievable-sample constraint rather than chosen. (b) requires the sibling repository and belongs to the cross-repository pass.
- **Confidence:** HIGH — every figure is quoted from this repository's own generated evidence block, and the comparison is arithmetic, not judgement.
- **Invalidated by later commits?:** no — dda39b2 is the tip; the repository has three commits total and no later work exists.
- **Disclosed by authors?:** partly — the mechanism is disclosed at retail-power-limits/docs/the-power-limit.md:386-389 and SOURCES.md:78 ("Not a sample requirement"), but neither the README's headline (README.md:3-5) nor the note's claim section (docs/the-power-limit.md:11-19) carries it, and "Not a sample requirement" appears nowhere in README.md (grep count 0). The finding is that the conclusion does not carry a fact the repository elsewhere records.

---

### DRAFT-all-2
- **Repository / SHA:** retail-power-limits / dda39b2f148569a6fe9be956a979471b2330611d
- **Hypothesis or artifact:** The shipped honesty-test machinery (`tests/test_honesty.py`), offered as the guarantee that the scope limit and headline figures cannot be softened.
- **Direction:** B
- **Class:** INTERNAL_INCONSISTENCY
- **Severity:** S2
- **Label:** DERIVED
- **Claim challenged (verbatim quote):** "A separate test scans every tracked\nfile for credential-shaped strings, and each detector has a canary asserting it\nactually fires. A future session cannot quietly soften the scope limit or drop\nan inconvenient number." — retail-power-limits/README.md:80-83 (same claim at retail-power-limits/tests/test_honesty.py:16-18: "Each detector carries a canary asserting it actually fires. A guard that has never been shown to fail is not a guard"; and at retail-power-limits/DECISIONS.md:164-166)
- **Evidence:**
  - Neither canary reads either pin table or calls either detector. `test_presence_checker_fires` (retail-power-limits/tests/test_honesty.py:133-136) asserts only that a synthetic string is absent; `test_figure_pin_detector_fires` (tests/test_honesty.py:139-147) asserts `"0.0512" in text` and that a longer phrase not used by any pin is absent. The detectors are `test_scope_limit_is_present` (tests/test_honesty.py:73-81) and `test_headline_figures_are_present` (tests/test_honesty.py:122-130), whose form is `missing = [... ]; assert missing == []`.
  - Both detectors pass vacuously on an empty pin list, and no guard forbids one: grep over `tests/` and `rplimits/` returns non-emptiness assertions only at tests/test_honesty.py:185 (`assert len(tracked_files()) > 10`) and tests/test_render.py:28 (`assert CASES, "no generated blocks found; the drift check would pass vacuously"`) — neither touches `SCOPE_PINNED` (tests/test_honesty.py:59) or `FIGURES_PINNED` (tests/test_honesty.py:90).
  - Emptying the dicts entirely makes `@pytest.mark.parametrize("name", sorted(SCOPE_PINNED))` (tests/test_honesty.py:73) collect zero cases. `[tool.pytest.ini_options]` at retail-power-limits/pyproject.toml:49-52 sets only `testpaths`, `pythonpath` and `addopts = "-q"` — `empty_parameter_set_mark` is unset, so pytest's default (`skip`) applies and the suite stays green.
  - This is the exact defect the repository found and fixed elsewhere in the same build: "An empty list made the parametrized drift test collect zero cases and report a **skip**, not a failure." — retail-power-limits/progress.md:85-87; and "the scan was green over an empty list for the entire build, which is indistinguishable from a clean scan" — progress.md:89-92. Both were repaired with a non-emptiness assertion. The flagship pins were not.
  - One detector has **no** canary at all: `test_the_note_never_claims_the_anomalies_are_absent` (retail-power-limits/tests/test_honesty.py:150-159). Nothing in the file exercises it against a synthetic overclaim. It also reads `document(NOTE)` only (tests/test_honesty.py:152), so README.md has no overclaim detector, although README.md:77-83 describes the honesty tests as covering "this file or ... the note".
  - Its four forbidden strings ("the effect does not exist", "these anomalies do not exist", "we have shown the effect is absent", "proves there is no effect" — tests/test_honesty.py:153-158) do not include the phrasing the document itself names as the risk: the pinned scope sentence is "This is not evidence that those anomalies are absent" (tests/test_honesty.py:53-57), and "those anomalies are absent" is not in the forbidden set.
- **Recomputation (if any):** Inputs: the two detector bodies verbatim (tests/test_honesty.py:73-81, 122-130), the two canary bodies verbatim (tests/test_honesty.py:133-136, 139-147), `SCOPE_PINNED` (tests/test_honesty.py:59-70) and `FIGURES_PINNED` (tests/test_honesty.py:90-119). Method: re-implemented the four test bodies byte-for-byte against the snapshot's own documents in `/tmp/claude-1000/.../scratchpad/work/agentB-rpl/vacuity.py`, run under three pin-table states. Result — (A) as shipped: 4 detector instances PASS, 2 canaries PASS; (B) inner lists emptied, keys kept: 4 detector instances **still PASS**, 2 canaries PASS; (C) dicts emptied: both detectors **collect zero cases** (pytest default = skip, suite green), 2 canaries **still PASS**. The canaries are insensitive to the state of the thing they certify.
- **What would resolve it:** Add `assert SCOPE_PINNED and all(SCOPE_PINNED.values())` and the same for `FIGURES_PINNED` (the pattern already used at tests/test_honesty.py:185 and tests/test_render.py:28); make each canary call the detector function on a synthetic document and assert it raises; add a canary and README coverage for the overclaim detector.
- **Confidence:** HIGH — demonstrated by executing the test bodies verbatim; the mechanism (empty-list comprehension, unset `empty_parameter_set_mark`) is fully determined by files in the snapshot.
- **Invalidated by later commits?:** no — dda39b2 is the tip and is itself the commit that added the *other* vacuity guard, so this is the repository's final state.
- **Disclosed by authors?:** no — the opposite is asserted. progress.md:108-109 names the failure shape ("**a check that cannot fail passes, and reads exactly like a check that passed**") and the repository claims to have applied the lesson to every detector (README.md:80-82, tests/test_honesty.py:16-18, DECISIONS.md:164-166).

---

### DRAFT-all-3
- **Repository / SHA:** retail-power-limits / dda39b2f148569a6fe9be956a979471b2330611d
- **Hypothesis or artifact:** The README's four-cases table, and ADR-002's guarantee that prose and data cannot diverge.
- **Direction:** B
- **Class:** INTERNAL_INCONSISTENCY
- **Severity:** S2
- **Label:** DERIVED
- **Claim challenged (verbatim quote):** "The tables and per-case records in the documents are **generated** from that\n   data between markers, and `tests/test_render.py` re-renders each block and\n   compares it to the file. Prose and data cannot diverge silently." — retail-power-limits/DECISIONS.md:74-76 (and the same guarantee at retail-power-limits/SOURCES.md:16-17: "A figure edited in the prose but not in the data — or the reverse — fails the build.")
- **Evidence:**
  - README.md carries **no** generated block. `DOCUMENTS = (ROOT / "SOURCES.md", ROOT / "docs" / "the-power-limit.md")` — retail-power-limits/rplimits/docsync.py:77. A grep for `GENERATED` across the repository returns markers only in docs/the-power-limit.md (1 block) and SOURCES.md (3 blocks). So the README's table is hand-maintained and untested.
  - It has already diverged. The generated table renders the ETF row as "| **ETFExperiment** | rank correlation 0.09 registered, 0.18 published | needs **N = 300** governing; **163** projected at the deadline | untestable at achievable power |" — retail-power-limits/docs/the-power-limit.md:74. The README's row for the same case is "| ETFExperiment | **163** admissible days projected at its deadline | a governing minimum of **300**; **845** for E1 and **above 1,200** for E2 at the registered assumption, against about **302** reachable by 2027-10-31 | untestable at achievable power |" — retail-power-limits/README.md:22, under the column header "against" (README.md:18). The effect band (0.09 / 0.18) is replaced by required-N figures; the HF row (README.md:23) drops its effect band (27.99 bp/day vs ~418 bp/day of noise, docs/the-power-limit.md:75) entirely. Under one header, "against" means an effect band for two rows, a required sample for one and a required excess return for one.
  - The substituted triple is the one the repository's own correction retracts: "**ETFExperiment's 845 / above-1,200 / about-302 triple is real but belongs to\n   a different question than the closure.**" and "The closure\n   itself fired on a different comparison — 163 projected against 300 governing\n   at the 2027-03-31 deadline." — retail-power-limits/docs/the-power-limit.md:132-139; same correction at DECISIONS.md:101-104. The README's table presents exactly the retracted comparison as the closure's evidence, and never states that 302 belongs to a *different deadline* (2027-10-31 vs the registered 2027-03-31).
  - The honesty test *requires* those three figures in the README: `FIGURES_PINNED["README.md"]` contains `"845"`, `"above 1,200"` and `"302"` — retail-power-limits/tests/test_honesty.py:95-97 — with a comment that acknowledges the hazard: "the ETF sample figures are the ones most\n#: easily mis-scoped, and the note corrects them explicitly" (tests/test_honesty.py:87-88). The pin forces the figures into the README; nothing forces the correction in with them. The word "correction" does not appear in README.md (grep count 0; README.md:32 says only "four figures corrected against the record", without saying which).
  - Coverage measured over the anchored tree: README.md has 0 numeric tokens inside generated blocks and 37 outside; docs/the-power-limit.md has 18 inside and 187 outside.
- **Recomputation (if any):** Inputs: `docsync.DOCUMENTS` (rplimits/docsync.py:77), `blocks_in` over each document, and a numeric-token regex over each file, in `/tmp/claude-1000/.../scratchpad/work/agentB-rpl/coverage.py`. Method: split each document at the BEGIN/END GENERATED markers and count numeric tokens on each side. Result: generated blocks = 4 (SOURCES.md: power-records, contrast-records, source-registry; the-power-limit.md: headline-table). Numeric tokens inside/outside: SOURCES.md 278/7; docs/the-power-limit.md 18/187 (8.8 % of the note's numbers are drift-tested); README.md 0/37 (0 %).
- **What would resolve it:** Put the README's four-cases table inside a generated block rendered from `HEADLINES` (the renderer already exists at rplimits/render.py:23-30), or carry the ETF correction and the second deadline in the README beside the pinned figures.
- **Confidence:** HIGH — the divergence is between two tables in the snapshot, and the exclusion of README.md from the drift machinery is a single line of source.
- **Invalidated by later commits?:** no — dda39b2 is the tip.
- **Disclosed by authors?:** no — DECISIONS.md:78-80 discloses only the *cost* of the mechanism ("an editor who reflows a generated table by hand will fail the build"), which presumes coverage. Neither the exclusion of README.md nor the existing divergence is stated anywhere.

---

### DRAFT-all-4
- **Repository / SHA:** retail-power-limits / dda39b2f148569a6fe9be956a979471b2330611d
- **Hypothesis or artifact:** The scope disclaimer that the four cases are not a sample, and the absence of any selection correction on the cross-experiment conclusion.
- **Direction:** B
- **Class:** STATISTICAL
- **Severity:** S2
- **Label:** DERIVED
- **Claim challenged (verbatim quote):** "2. **Four cases are four cases.** They were not sampled from a population of\n   hypotheses; they are the hypotheses one operator happened to run in a\n   five-week window." — retail-power-limits/docs/the-power-limit.md:39-41
- **Evidence:**
  - The case set was supplied, not enumerated: "The governing instruction\nnamed seven repositories to read in full and read-only, five tasks, and a\nstanding rule" — retail-power-limits/progress.md:22-24. The test suite records the same: "The note was commissioned against seven repositories. All seven are cited." — retail-power-limits/tests/test_sources.py:42. Nothing in the repository establishes that those seven (eight with AiTrader, nine counting this repository) are all the hypotheses run in the window; the note asserts the population, it does not exhibit it.
  - Within the supplied seven, the four were selected *by closure type* — the property the conclusion is about. progress.md's reading table assigns the roles: NPDExperiment / InsiderExperiment / ETFExperiment "power case", HFExperiment "power case, inherited", MLCryptoEngine / solattn / solclear "contrast case" — retail-power-limits/progress.md:38-45. Selecting on the outcome variable is what "sampled from a population" means.
  - The unit of analysis changes between numerator and denominator. Each power case is one repository; MLCryptoEngine as a single contrast case carries "Eleven hypotheses, nine tested and closed, and not one closed on power" — retail-power-limits/SOURCES.md:168 (n = 9 closed hypotheses, none on power). Counted per hypothesis rather than per repository, the program's closures are 4 power against at least 11 non-power, not 4 against 3.
  - The count is then frozen by a test: "assert len(POWER_CASES) == 4" with the docstring "Four cases are four cases. A fifth would change the claim, not extend it." — retail-power-limits/tests/test_cases.py:31-32. Presented as a drift guard, it also makes the denominator unamendable by the build.
  - **The standard asymmetry.** The one negative in this corpus whose verdict rested on a threshold received a multiplicity correction: "z 1.668 against a corrected bar of 2.50" — retail-power-limits/SOURCES.md:134 / rplimits/cases.py:257. The cross-experiment conclusion drawn over a set selected on its own outcome receives no correction of any kind — no multiplicity, no selection, no correction for the shared operator, scaffold and method that the note itself flags at docs/the-power-limit.md:54-60.
- **Recomputation (if any):** Inputs: z bar 2.50 (SOURCES.md:134), z realized 1.668 (SOURCES.md:134). Method: two-sided normal tail; compare against Bonferroni critical values. Result: two-sided p at z = 2.50 is 0.01242, i.e. α ≈ 0.05/4.03; the Bonferroni m = 4 critical value at α = 0.05 is z = 2.4977 — the "corrected bar of 2.50" is consistent with a family of four to two decimal places. (For completeness: z = 1.668 gives two-sided p = 0.09532, so this negative also fails an uncorrected 1.96 bar; the correction did not decide it.) The inference drawn is about the *standard applied*, not about that verdict.
- **What would resolve it:** An enumeration in the repository of the hypotheses run in the stated five-week window, with the inclusion rule for the four stated before the closure types were known; or a restatement of item 2 as "four cases selected from seven supplied repositories because they closed on power".
- **Confidence:** MEDIUM — the selection is documented inside this repository, but whether further hypotheses existed in the window can only be settled against the other repositories in the program; that half belongs to the cross-repository pass. The Bonferroni identification of the 2.50 bar is an inference from arithmetic, not a quotation.
- **Invalidated by later commits?:** no for this repository (dda39b2 is the tip); the population question could be re-opened by evidence from sibling repositories, which is why confidence is MEDIUM.
- **Disclosed by authors?:** partly — the note discloses the *consequences* fully and well (docs/the-power-limit.md:39-42 on base rates, :54-60 on shared method, :393-401: "Four cases run by one person under one scaffold cannot distinguish 'retail-scale replication is power-bound' from 'these four designs were underpowered'"). What is not disclosed, and is contradicted by progress.md:22-24 and :38-45, is the specific sentence "They were not sampled from a population of hypotheses".

---

### DRAFT-all-5
- **Repository / SHA:** retail-power-limits / dda39b2f148569a6fe9be956a979471b2330611d
- **Hypothesis or artifact:** ADR-006, "The one derived figure is flagged as derived", and the repository-wide claim that it computes nothing.
- **Direction:** B
- **Class:** INTERNAL_INCONSISTENCY
- **Severity:** S3
- **Label:** DERIVED
- **Claim challenged (verbatim quote):** "The 411 minutes is stated as this note's arithmetic over six\nquoted addends — A.1 22, A.2 34, B.0 68, B.0b 52, B.1 194, B.2 41 — and\n`SOURCES.md` carries a dedicated section saying so, including what the total\nexcludes. Every other number in the repository is quoted rather than computed." — retail-power-limits/DECISIONS.md:184-187 (reinforced at SOURCES.md:300: "Every other number in this repository is quoted, not computed." and at README.md:53-54 / rplimits/cases.py:3: "Nothing here is computed.")
- **Evidence:**
  - Two intervals in the note's spine are this repository's arithmetic across commit timestamps from **two different** sibling repositories, so no single cited source can contain them: "NPDExperiment's closing commit is stamped\n2026-08-25 13:26:58. InsiderExperiment's first commit — the one carrying the\ngate — is stamped 18:34:56 the same day, five hours and eight minutes later. Its\nown closure came at 23:24:15. The whole distance from paying for the lesson to\nspending nothing on the next one is under ten hours" — retail-power-limits/docs/the-power-limit.md:211-216. Neither timestamp nor interval is a `Figure`, carries a source key, or sits inside a generated block; the passage is introduced as "The clock is the part worth keeping" (docs/the-power-limit.md:211), so it is load-bearing for the progression the README calls "the transferable output" (README.md:37-39).
  - Arithmetic presented inside a `Figure` and cited as a quotation: "The\nshortfall at the deadline is 137 days against the governing figure, and 74 days against\nE1's 237, the most favourable figure anywhere on the record." — retail-power-limits/rplimits/cases.py:214-216, rendered at SOURCES.md:110 under "*Source: ETFExperiment/REGISTRATION.md @ 4d11002 (2026-08-28).*" (SOURCES.md:112). Both numbers are differences of two other figures in the same field, and "the most favourable figure anywhere on the record" is this repository's judgement, not a quotation.
  - Further computed values carried as quotations: "it cleared its floor by a factor of four and a\nhalf" — rplimits/cases.py:178-179 (= 4,585 / 1,000, from SOURCES.md:74); "a shortfall of 1.5x" — rplimits/cases.py:259 (= 104.0 / 70.5, same field); "NPDExperiment lost 70 percent of its sample to overlapping five-session horizons" — docs/the-power-limit.md:379 (= 1 − 125.6/427, from SOURCES.md:42).
- **Recomputation (if any):** Inputs: the three timestamps at docs/the-power-limit.md:211-214; 300, 237 and 163 at rplimits/cases.py:201-215; 4,585 and 1,000 at SOURCES.md:74; 104.0 and 70.5 at rplimits/cases.py:258-259; 125.6 and 427 at SOURCES.md:42 and docs/the-power-limit.md:166. Method: direct arithmetic in `/tmp/claude-1000/.../scratchpad/work/agentB-rpl/recompute.py`. Results — 13:26:58 → 18:34:56 = **5 h 07 m 58 s** (note: "five hours and eight minutes", correct to the minute); 13:26:58 → 23:24:15 = **9 h 57 m 17 s** ("under ten hours", correct); 300 − 163 = **137**, 237 − 163 = **74** (both correct); 4585/1000 = **4.585** ("four and a half", correct); 104.0/70.5 = **1.4752** ("1.5x", correct); 1 − 125.6/427 = **70.59 %** ("70 percent", correct). Also verified the flagged figure: 22+34+68+52+194+41 = **411**, exactly as SOURCES.md:296-297 states. Every computation in the repository is arithmetically right; the claim that there is only one of them is what fails.
- **What would resolve it:** Widen the ADR-006 disclosure to list the derived figures, or move the two intervals and the two shortfalls into `rplimits/cases.py` with a `derived` marker so the existing `Figure` discipline covers them.
- **Confidence:** HIGH — the two intervals span two repositories and cannot be a quotation from either; the four other values are exact functions of figures printed in the same field.
- **Invalidated by later commits?:** no — dda39b2 is the tip.
- **Disclosed by authors?:** no — DECISIONS.md:187 and SOURCES.md:300 assert the exact opposite, and SOURCES.md:292-300 is a section built to make the single exception conspicuous.

---

### DRAFT-all-6
- **Repository / SHA:** retail-power-limits / dda39b2f148569a6fe9be956a979471b2330611d
- **Hypothesis or artifact:** SOURCES.md as the shipped artifact that maps every figure in the note to a repository, file and commit.
- **Direction:** B
- **Class:** PROVENANCE
- **Severity:** S3
- **Label:** DERIVED
- **Claim challenged (verbatim quote):** "Every figure in [the note](docs/the-power-limit.md) was measured somewhere else.\nThis file maps each one to the repository, the file and the commit it came from,\nso a reader can check the note against the primary record without asking this\nrepository to vouch for itself." — retail-power-limits/SOURCES.md:3-6 (and README.md:55: "It is a note plus the machinery that keeps the note's figures pinned to their sources.")
- **Evidence:**
  - At least 22 distinct numbers appear only in the note's hand-written prose, with no counterpart anywhere in `rplimits/` and no entry in SOURCES.md. Verified absent from both by grep: **34.29** (docs/the-power-limit.md:228 and :389 — zero hits in SOURCES.md and rplimits/), **90.3** and **19.7** (docs/the-power-limit.md:111-112, HF raw outperformance against its benchmark), **20.00** (docs/the-power-limit.md:223, the GO boundary convention that the practice section holds up as the model of a written-down bar), **3.30** and **333** (docs/the-power-limit.md:103, ETF archive capture density), **124,764** (docs/the-power-limit.md:309, solclear's stale estimate).
  - 34.29 is the most load-bearing of them: it carries the note's "The refusal was also honest about what it forwent" paragraph (docs/the-power-limit.md:227-233) and one of the three shapes in "What would change the conclusion" (docs/the-power-limit.md:386-391). It is also the deciding figure in DRAFT-all-1. It has no source key, no `Figure`, no citation, and no drift test.
  - The `Figure` discipline the repository relies on (rplimits/cases.py:29-33; DECISIONS.md:67-69: "A figure cannot be added without a citation, because the constructor refuses") applies only to values that are *put into* `cases.py`. Prose figures bypass it entirely; nothing in the build detects one.
  - Separately, "resolve" in ADR-002 means resolve to a dictionary key, not to a git object: `Figure.__post_init__` checks `self.source not in SOURCES` (rplimits/cases.py:30) and `tests/test_sources.py` checks only that fields are non-empty (:35-39), that the commit matches `^[0-9a-f]{7}$` (:44-47) and that the date matches `^2026-\d{2}-\d{2}$` (:52). No test opens a sibling repository, resolves a commit, or checks that a quoted string appears at the cited location — including for the four siblings that SOURCES.md:264-267 records as public and clonable, where verification was available.
- **Recomputation (if any):** Inputs: the numeric-token split of docs/the-power-limit.md at the GENERATED markers, against the pool of numbers present in `rplimits/cases.py` (`POWER_CASES`, `CONTRAST_CASES`, `HEADLINES`), in `/tmp/claude-1000/.../scratchpad/work/agentB-rpl/coverage.py`; test counts from `/tmp/claude-1000/.../scratchpad/work/agentB-rpl/count.py`. Method: token extraction and set difference; static enumeration of parametrized test instances. Result: 187 numeric tokens in the note's hand-written prose, of which 22 distinct values have no counterpart in `rplimits/`. Test composition: 112 collected tests, of which 74 (66 %) are the three parametrized field-format assertions over the 24-entry hand-typed source registry (24 x 3 + 2), and 0 verify any citation against any sibling repository.
- **What would resolve it:** Either narrow the SOURCES.md claim to "every figure in the generated blocks", or lift the remaining prose figures into `cases.py` where the constructor enforces a citation. For the four public siblings, a test that runs `git -C ../<repo> show <commit>:<file>` and greps for the quoted string would convert "resolves to a key" into "resolves to a source".
- **Confidence:** HIGH — the absent figures were confirmed by grep across README.md, SOURCES.md, docs/ and rplimits/; the test composition was enumerated from the snapshot's own data structures.
- **Invalidated by later commits?:** no — dda39b2 is the tip.
- **Disclosed by authors?:** partly — SOURCES.md:284-288 discloses that the four *unpublished* siblings "rest on this note's transcription" and that "The mechanisms in ADR-002 protect against drift *within* this repository; they cannot attest to a repository the reader cannot open." That disclosure is scoped to the unreachable four and does not cover either the unsourced prose figures or the four reachable repositories, and DECISIONS.md:82-83 says of ADR-002 "What would overturn it. Nothing available."

---

### DRAFT-all-7
- **Repository / SHA:** retail-power-limits / dda39b2f148569a6fe9be956a979471b2330611d
- **Hypothesis or artifact:** The stated gate evidence in progress.md — the test count reported as proof the build ran green.
- **Direction:** B
- **Class:** STALE_FIGURE
- **Severity:** S3
- **Label:** DERIVED
- **Claim challenged (verbatim quote):** "`make lint`, `make typecheck` and `make test` all green. Ruff format and check\nclean, mypy strict clean over 11 source files, 111 tests passing." — retail-power-limits/progress.md:67-68 (also progress.md:59: "`tests/`, 111 tests: source-registry integrity, case integrity, drift between prose and data, the honesty pins, and a credential scan.")
- **Evidence:**
  - The anchored commit is `dda39b2`, and its own message ends "make lint, typecheck and test green by exit status. **112 tests.**" — `git -C /home/kiros-li/Documents/GitHub/retail-power-limits show dda39b2` (read 2026-09-03, live repository, read-only).
  - The same commit added a test — `test_the_credential_scan_has_something_to_scan` (retail-power-limits/tests/test_honesty.py:177-185) — and rewrote the surrounding progress entry from "Two defects" to "Three defects" (diff of progress.md in `dda39b2`), while leaving both "111" figures untouched.
  - Static enumeration of the anchored tree gives 112: test_sources.py 24x3 + 2 = 74; test_cases.py 2 + 7 + 1 + 4 + 3 + 2 = 19; test_render.py 2 + 4 + 3 = 9; test_honesty.py 2 + 2 + 6 = 10.
  - The entry carrying the stale count is the repository's record that the gates passed, in the same document that describes the previous commit as having "went out red" because a `make test | tail` pipeline masked a failure (progress.md:100-106).
- **Recomputation (if any):** Inputs: `SOURCES` (24 entries, rplimits/sources.py:38-207), `POWER_CASES` (4) and `CONTRAST_CASES` (3) (rplimits/cases.py:297, :377), `blocks_in` over `DOCUMENTS` (4 blocks), and the parametrize decorators in each test file. Method: enumerate collected test instances per file in `/tmp/claude-1000/.../scratchpad/work/agentB-rpl/count.py`. Result: **112** collected tests, matching the commit message and contradicting progress.md:59 and :68. (pytest is not installed in the audit venv, so this is a static count of parametrized instances, not an executed run.)
- **What would resolve it:** Updating both figures in progress.md to 112, or an executed `pytest --collect-only` against the anchored tree.
- **Confidence:** HIGH — the number is fixed by the data structures in the snapshot and independently corroborated by the anchoring commit's own message.
- **Invalidated by later commits?:** no — dda39b2 is the tip, so the stale figure is the repository's final state.
- **Disclosed by authors?:** no — progress.md is append-only and states 111 twice as current fact.

---

### DRAFT-all-8
- **Repository / SHA:** retail-power-limits / dda39b2f148569a6fe9be956a979471b2330611d
- **Hypothesis or artifact:** HFExperiment as the fourth power case, and the README's categorical statement of how all four closed.
- **Direction:** B
- **Class:** PROCESS
- **Severity:** S3
- **Label:** READ
- **Claim challenged (verbatim quote):** "Each closed at *unresolved at\nachievable power*, at *untestable at achievable power*, or *BLOCKED* on a power\ngate — never on a measured null." — retail-power-limits/README.md:5-7
- **Evidence:**
  - HFExperiment closed at none of the three. The repository's own correction: "**HFExperiment did not fire a power gate.** It is a power case by\n   inheritance. Its own Section 0 fired BLOCKED on the *broker* — IBKR refused\n   fractional quantities through the API, errors 10243 and 10244 — and the\n   repository then closed by operator decision on 2026-08-26 with the shadow\n   series never started." — retail-power-limits/docs/the-power-limit.md:141-146; same at SOURCES.md:154 and DECISIONS.md:125-128. The README's own table gives it a fourth verdict label not in the enumerated three: "resolved on statistical power, not absent signal" (README.md:23).
  - Its deciding figure is sourced to a fifth repository. `realized_mde` for HF cites `"aitrader-return"` — retail-power-limits/rplimits/cases.py:262 — and the headline row does the same, `source="aitrader-return"` (rplimits/cases.py:428), resolving to AiTrader/RETURN.md @ f819b68, 2026-07-29 (rplimits/sources.py:158-164). AiTrader is neither one of the four cases nor one of the three contrast cases; progress.md:47-50 records it was not even on the reading list.
  - None of this reaches the README. Grep counts over README.md: "AiTrader" 0, "inherit" 0, "broker" 0, "IBKR" 0 (against note/SOURCES/DECISIONS counts of 3/8/4, 1/1/3, 1/2/1, 1/1/1 respectively).
  - ADR-004's own remedy does not name the README: "**Decision.** Include it, and label the inheritance in the case record, in the\nnote's correction section, and in the caveat field the tests require every case\nto carry. A reader must not come away thinking four power gates fired." — retail-power-limits/DECISIONS.md:138-140. The README is the document a reader meets first, and it is the only document of the four that carries the enumeration without the correction.
  - The caveat the tests "require" is enforced only by length: `assert len(case.caveat) > 80` — retail-power-limits/tests/test_cases.py:44. No test asserts the inheritance is stated anywhere, and the honesty pins (tests/test_honesty.py:90-119) pin HF's `z 1.668` and `2.50` into the README without pinning the caveat that scopes them.
- **What would resolve it:** One clause in README.md:5-7 and in the README's HF table row saying the power resolution is inherited from the AiTrader round of 2026-07-26 and that HFExperiment's own BLOCKED fired on the broker.
- **Confidence:** HIGH — the correction is quoted from the repository itself; the only claim I add is that it is absent from README.md, which grep settles.
- **Invalidated by later commits?:** no — dda39b2 is the tip.
- **Disclosed by authors?:** **yes** — fully and prominently, at retail-power-limits/docs/the-power-limit.md:141-146, SOURCES.md:154 and DECISIONS.md:121-148 (a whole ADR). This is therefore a READ finding capped at S3: the limitation is the authors' own, disclosed in three places, and the finding is only that the fourth document — the README — states the categorical form without it.

---

## What I checked and found sound

The thesis did **not** hold in the following places. Several of them are places where I expected it to hold and it did not.

**All arithmetic in the repository is correct.** I recomputed every derivable figure I could find (`/tmp/claude-1000/.../scratchpad/work/agentB-rpl/recompute.py`) and found no arithmetic error:
- The flagged derived figure: 22 + 34 + 68 + 52 + 194 + 41 = **411**, exactly as SOURCES.md:296-297 and DECISIONS.md:184-186 state, and the exclusion of the untimed Z.1 stage is declared.
- 300 − 163 = 137 and 237 − 163 = 74 (SOURCES.md:110); 4,585/1,000 = 4.585 ("four and a half", cases.py:178-179); 104.0/70.5 = 1.4752 ("1.5x", cases.py:259); 1 − 125.6/427 = 70.6 % ("70 percent", docs/the-power-limit.md:379); 427/3.4 = 125.59 ("125.6", SOURCES.md:42); 11/333 = 3.303 % ("3.30 percent", docs/the-power-limit.md:103); 50/0.0291 = 1,718 ("roughly 1,700x") and 3/0.0291 = 103 ("roughly 100x") at docs/the-power-limit.md:148-153; 550/3 = 183 ("100 to 180x", SOURCES.md:172).
- The ETF census reconciles: 53 + 243 + 25 + 3 + 1 = 325 disposition rows + 11 admissible = **336**, matching the stated "336-row census" (SOURCES.md:106).
- The InsiderExperiment effective-N figure reconciles: 2,581/2,869.9 = 0.89933, consistent with the stated variance inflation of 0.899 (SOURCES.md:74). The counter-intuitive claim that effective periods *exceed* raw sessions is arithmetically correct given a VIF below one, and the record says so explicitly rather than hiding it.

**The scope limit is genuinely strong, and it is placed before the evidence rather than after.** docs/the-power-limit.md:21-60 states four limits — that nothing refutes the literature (:32-37), that four cases are four cases (:39-42), that four of seven sources are unpublished (:44-52), and that "independent" means independent hypotheses only (:54-60) — before the case table at :67. The final section (:393-401) volunteers the strongest available counter-hypothesis against the note's own thesis ("Four cases run by one person under one scaffold cannot distinguish 'retail-scale replication is power-bound' from 'these four designs were underpowered'") and calls its own contrast-case evidence "weak evidence ... offered as weak evidence". I looked for a softened or trimmed scope limit and found the opposite.

**The awkward direction is disclosed unprompted and not repaired by rhetoric.** progress.md:111-127 and SOURCES.md:257-288 both state that the four repositories the claim *rests on* are unpublished while the three that *bound* it are public — "That is the awkward direction" — and say plainly "neither is a repair" and "A reader should discount the four accordingly." I expected this to be buried in a footnote or absent from the README; the README carries it as scope item 3 by reference and the note carries it in the body.

**No amendment rescued a verdict.** The repository has three commits (`0974f96`, `710093d`, `dda39b2`, all 2026-08-29 00:19–00:21 −07:00). I read all three diffs. `710093d` changes one word — "Three limits" to "Four limits" — to fix a lead-in that undercounted its own list, and the commit message explains that the fourth limit (the unpublished-sources one) was *inserted* and the count corrected "rather than by dropping the item", i.e. the amendment preserved a caveat rather than removing one. `dda39b2` records a real defect against the repository's own interest. There is no post-hoc bar change, no widened threshold, and no data that could have existed before a bar was set — this repository holds no data at all.

**The three defects in progress.md:70-109 are self-reported against interest, including one that made a commit go out red.** The `make test | tail` exit-status defect (progress.md:100-106) is a failure of the author's own verification that nothing external would have surfaced. I checked it against git: `710093d` did go out with a failing suite and `dda39b2` fixed it, exactly as described.

**The credential scan and the drift test carry real, non-vacuous canaries.** `test_credential_detector_fires` (tests/test_honesty.py:200-218) constructs synthetic positives at runtime, asserts each regex matches them, and asserts both reject a benign string — that is a genuine canary. `test_the_credential_scan_has_something_to_scan` (:177-185) and `test_documents_carry_generated_blocks` (tests/test_render.py:27-28) both close the vacuous-pass hole for their detectors. My DRAFT-all-2 is that this discipline was applied to three detectors and not to the two flagship ones — not that it is absent.

**The drift test does work where it is applied.** SOURCES.md carries 278 of its 285 numeric tokens inside generated blocks, and I re-rendered all four blocks from `rplimits/` and compared them to the documents on disk: all four match byte-for-byte. No stale generated block exists at the anchor.

**"BLOCKED as a legitimate outcome" is not self-serving here.** I checked whether the note treats a BLOCKED verdict as evidence *for* anything. It does not: docs/the-power-limit.md:32-37 states "A design that cannot resolve an effect returns no information about whether the effect is there", and the closure language quoted for ETFExperiment includes "The signal was never read and this closure is not evidence about it" (SOURCES.md:118).

**NPDExperiment's "not a measured null" framing survives scrutiny.** I tested the sceptical reading that NPD, having read its outcome and found "zero positives" (SOURCES.md:54), is really a measured null relabelled as a power closure. The note pre-empts it in terms: "The verdict\nrow fired as registered; the honest reading beside it is an underpowered\nunresolved, not a tight null" (docs/the-power-limit.md:87-88), and with a realized MDE of 0.0512 above the whole 0.01–0.05 band, "zero positives" genuinely carries no information about the band. The framing is defensible.

**No credentials, no secrets, no data.** The repository is what it says it is: markdown plus 5 small source files with `dependencies = []` (pyproject.toml:9), no network code, no data files, no execution path.

## Live-repo access log

I accessed the live repository `/home/kiros-li/Documents/GitHub/retail-power-limits` read-only, for git history only (`git status --porcelain`, `git log`, `git show`, `git ls-tree`). No untracked or gitignored data was read; there is none. No file in any audited repository was opened for writing.

**`git -C /home/kiros-li/Documents/GitHub/retail-power-limits status --porcelain` BEFORE first access:**

```
```
(empty — clean working tree)

**`git -C /home/kiros-li/Documents/GitHub/retail-power-limits status --porcelain` AFTER last access:**

```
```
(empty — clean working tree, unchanged)

Read time for the live git history: 2026-09-03, approximately 20:00 UTC. Git history at the
anchor is three commits and does not move; the anchored SHA `dda39b2` is the branch tip, so
nothing read here is unanchored.

All other reading was from
`/tmp/claude-1000/-home-kiros-li-Documents-GitHub-program-audit/5ca157a0-1746-4eb9-a1b8-f3732ea42bf4/scratchpad/snap/retail-power-limits/`.
Scratch scripts and a working copy of the snapshot (for static analysis only; no repository
script was executed in place) are under
`/tmp/claude-1000/-home-kiros-li-Documents-GitHub-program-audit/5ca157a0-1746-4eb9-a1b8-f3732ea42bf4/scratchpad/work/agentB-rpl/`.
