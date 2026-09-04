# Agent B draft findings — InsiderExperiment (part "all")

Repository: InsiderExperiment, anchored SHA `12d9fd36cf055cb10ea67a3fc737e404217bc95a` (master, 2026-08-25).
Snapshot read: `SNAP/InsiderExperiment/`. Live repo touched read-only for git history and for
untracked `var/`, `ledgers/`, `cache/` (all gitignored). Every live-tree figure below is UNANCHORED
and was read at **2026-09-04T05:39Z**.

I deliberately did **not** open `var/insider_sealed.db`. Nothing in this audit reads the realized
alpha, and the seal is intact as far as this agent is concerned.

---

### DRAFT-all-1
- **Repository / SHA:** InsiderExperiment / 12d9fd36cf055cb10ea67a3fc737e404217bc95a
- **Hypothesis or artifact:** The Section 0.2 power gate (the repository's headline transferable artifact: GO ≤ 20 bp, DEGRADED 20–40 bp, BLOCKED > 40 bp per month)
- **Direction:** B
- **Class:** STATISTICAL
- **Severity:** S2
- **Label:** DERIVED
- **Claim challenged (verbatim quote):** "The 20 bp GO bar sits below the bottom of the decayed gross band, so a GO design resolves the whole band. The 40 bp BLOCKED bar sits at the top of it, so a design above 40 bp cannot resolve any part of the band." — InsiderExperiment/REGISTRATION.md:57-59
- **Evidence:** Both bars are calibrated against a gross band the same section says is mostly gone before this design can enter. REGISTRATION.md:51-55 states "Ozlen and Batumoglu (SSRN 5966834, December 2025, Russell 2000 Form 4) report 70 to 80 percent of total alpha dissipating between the transaction date and the following trading day, before a public filer can act". REGISTRATION.md:377-381 fixes entry as "the close of the first session strictly after the filing date", i.e. strictly after the point at which the cited dissipation has already occurred, and DECISIONS.md:99-101 says so explicitly: "But Ozlen and Batumoglu report 70 to 80 percent of total alpha dissipating between the transaction date and the following trading day, which is inside even that lag." The bars in `insider.config.CONFIG` are `mde_go_ceiling_bp=20.0`, `mde_degraded_ceiling_bp=40.0`, `decayed_gross_band_bp=(30.0, 40.0)` (InsiderExperiment/src/insider/config.py:143-144, 152) and carry no haircut for that dissipation. `insider.power.mde.band_position` compares the realized MDE to `cfg.decayed_gross_band_bp` unadjusted (InsiderExperiment/src/insider/power/mde.py:70-82), and `power.json` records `"decayed_gross_band_bp": [30.0, 40.0]` (InsiderExperiment/reports/stage_a1/power.json:120-123). n for the fired verdict: one primary series, 2,581 sessions, MDE 49.35 bp (power.json:6-12).
- **Recomputation (if any):** Inputs: gross band (30.0, 40.0) from REGISTRATION.md:50-51 and config.py:152; dissipation 70–80 % from REGISTRATION.md:52-53; drags 16.667 / 5.333 bp per month from power.json:128-131 and `insider/cost.py:40-45`. Method: apply the repository's own dissipation range to its own registered band, then subtract its own amortized round trip. Result: reachable gross band 30×0.20 = **6.0** to 40×0.30 = **12.0** bp per month; net at the registered primary 100 bp round trip **−10.7 to −4.7** bp per month; net at the registered optimistic 32 bp round trip **+0.7 to +6.7** bp per month. The registered GO ceiling of 20 bp is 1.7× the *top* of the reachable gross band and 3× the top of the reachable net band, so a design that fires GO — "The design can resolve the decayed effect band with margin. Stage B is authorized." (REGISTRATION.md:41) — could not resolve the effect this design is able to reach. Script and outputs: `/tmp/claude-1000/-home-kiros-li-Documents-GitHub-program-audit/5ca157a0-1746-4eb9-a1b8-f3732ea42bf4/scratchpad/work/agentB-insider/recompute.txt`.
- **What would resolve it:** Either a registered statement that the 30–40 bp band is already measured from a filing-date / next-close entry (in which case the Ozlen–Batumoglu haircut is not additive and should be said so, since the registration currently presents both as applying), or a re-derivation of the GO and DEGRADED bars against the post-entry reachable band. One of the two is required; the document supports neither reading over the other.
- **Confidence:** MEDIUM — the arithmetic uses only figures the repository states, but the registration never says at which entry point its 30–40 bp band is measured, so the double-count reading cannot be excluded either.
- **Invalidated by later commits?:** no — the repository is closed and the anchored SHA is its last commit; `_CLOSED_DO_NOT_RUN_HERE` in the live tree forbids further work.
- **Disclosed by authors?:** no — both inputs are stated (REGISTRATION.md:51-55, DECISIONS.md:99-101) but the contradiction between them and the bar derivation at REGISTRATION.md:57-59 is nowhere reconciled, and the closure language (REGISTRATION.md:812-816) presents 30–40 bp gross as the relevant target without qualification. Note the direction: this makes the BLOCKED verdict that actually fired *more* secure, not less; the defect is in the GO/DEGRADED branches of a gate the repository ships as reusable.

---

### DRAFT-all-2
- **Repository / SHA:** InsiderExperiment / 12d9fd36cf055cb10ea67a3fc737e404217bc95a
- **Hypothesis or artifact:** The decayed literature band that sets both registered power bars
- **Direction:** B
- **Class:** ARITHMETIC
- **Severity:** S3
- **Label:** DERIVED
- **Claim challenged (verbatim quote):** "Cohen, Malloy and Pomorski report 82 bp per month value-weighted on opportunistic purchases over 1989 to 2007. That replicates at roughly 30 to 40 bp per month on 2008 to 2024 data, a 60 to 70 percent decay." — InsiderExperiment/REGISTRATION.md:48-51
- **Evidence:** The two halves of the sentence are not consistent. The same pairing is repeated at REGISTRATION.md:181-184 (Section 1), REGISTRATION.md:515-516 (Section 12, where "The 60 to 70 percent decay" is one of the four inputs to the assistant's 0.12 prior), and the band alone is hard-coded as `decayed_gross_band_bp=(30.0, 40.0)` at InsiderExperiment/src/insider/config.py:152. The "roughly 30 to 40 bp per month on 2008 to 2024 data" figure carries no citation anywhere in the repository (grep for "2008 to 2024" returns only REGISTRATION.md:50-51 and 182-183); the 82 bp figure is attributed to Cohen–Malloy–Pomorski and the 70–80 % intraday dissipation to Ozlen–Batumoglu, but the number that fixes both bars is attributed to no one.
- **Recomputation (if any):** Inputs: 82 bp (REGISTRATION.md:49-50), decay 60–70 % (REGISTRATION.md:51). Method: 82 × (1 − d). Result: **24.60 to 32.80 bp per month**, not 30 to 40. Inverting: a band of 30 bp implies a **63.41 %** decay and 40 bp implies a **51.22 %** decay, so the stated range 60–70 % is wrong at both ends and the stated band is 22 % (low end) to 52 % (high end) above what the stated decay produces.
- **What would resolve it:** A citation for the 30–40 bp replication, or a correction of one of the two halves of the sentence. If the band were the arithmetically implied 24.6–32.8 bp, the BLOCKED bar at "the top of it" would be ≈33 bp rather than 40 bp.
- **Confidence:** HIGH — pure arithmetic on two figures in one sentence of the shipped registration.
- **Invalidated by later commits?:** no — REGISTRATION.md lines 1-157 are byte-identical to the first commit `fbfc74ed9c8b0b2b237da5a8cd0a2b4730ba456d` (verified with `git diff fbfc74e 12d9fd3 -- REGISTRATION.md`, which shows only additions after line 157), and the repository is closed.
- **Disclosed by authors?:** no — the sentence is presented as a derivation. Direction is conservative for the verdict that fired: a lower band would have set a lower BLOCKED bar and fired BLOCKED a fortiori (49.35 > 33).

---

### DRAFT-all-3
- **Repository / SHA:** InsiderExperiment / 12d9fd36cf055cb10ea67a3fc737e404217bc95a
- **Hypothesis or artifact:** CORPUS-GO, Section 15.1 results table (the shipped by-year composition of the 4,585 qualifying events)
- **Direction:** B
- **Class:** STALE_FIGURE
- **Severity:** S3
- **Label:** DERIVED
- **Claim challenged (verbatim quote):** "Qualifying events by entry year. 2016 opens on 2016-04-01 and 2026 closes on 2026-03-31, so both are partial." — InsiderExperiment/REGISTRATION.md:598-599, followed by the table at REGISTRATION.md:601-608
- **Evidence:** The table (2016 262, 2017 406, 2018 524, 2019 457, 2020 717, 2021 297, 2022 502, 2023 505, 2024 410, 2025 363, 2026 99) sums to **4,542**, while the headline three lines above reads "**CORPUS-GO.** 4,585 qualifying events against a registered floor of 1,000" (REGISTRATION.md:594). The shipped artifact `reports/stage_a1/corpus.json:3-15` carries a different table (263, 409, 531, 462, 728, 298, 504, 508, 418, 365, 99) which sums to 4,585, and the live store agrees: `SELECT substr(entry_session,1,4), COUNT(*) FROM event GROUP BY 1` on `var/insider_corpus.db` returns exactly the corpus.json figures and `SELECT COUNT(*) FROM event` returns 4,585 (read 2026-09-04T05:39Z, UNANCHORED). Both tables are the same quantity: `store.events_per_year` is `SELECT substr(entry_session,1,4), COUNT(*) FROM event` (InsiderExperiment/src/insider/corpus/store.py:151-157). The difference is exactly **43**, which is the number ADR-013 says the old composite key silently merged: "the key silently merged 43 of them. The build reported 4,585 qualifying events while the table held 4,542." (InsiderExperiment/DECISIONS.md:404-407).
- **Recomputation (if any):** Inputs: the eleven cells at REGISTRATION.md:603-607 and the eleven at corpus.json:4-14. Method: sum each. Result: 4,542 and 4,585; difference 43, matching DECISIONS.md:406-407 exactly. Git dating: `git diff ccc9b13 cb17046 -- reports/stage_a1/corpus.json` shows the by-year cells changing from the 4,542-summing set to the 4,585-summing set at commit `cb17046308ca81ef63357541f4ad1fec84fe66c2` (2026-08-25T19:11:45-07:00); REGISTRATION.md Section 15 was written ten seconds later at `d8b81f1ef50729a12dd90b8e452f56dde706ff7a` (19:11:55-07:00) and transcribed the pre-correction table. It was never revised, including at the closure commit `12d9fd3`.
- **What would resolve it:** Regenerating REGISTRATION.md Section 15.1 from `corpus.json` / the store, or a note saying the table predates ADR-013.
- **Confidence:** HIGH — three independent sources (registration, shipped JSON, live SQLite store) and a git diff that dates the correction.
- **Invalidated by later commits?:** no — `12d9fd3` is the last commit and did not touch Section 15.
- **Disclosed by authors?:** no — ADR-013 (DECISIONS.md:400-416) records the defect and states it was corrected, but nothing says the registration's own results table still carries the uncorrected breakdown next to the corrected headline.

---

### DRAFT-all-4
- **Repository / SHA:** InsiderExperiment / 12d9fd36cf055cb10ea67a3fc737e404217bc95a
- **Hypothesis or artifact:** Section 15.4, the front-truncation narrative attached to the `insufficient_history` refusal
- **Direction:** B
- **Class:** INTERNAL_INCONSISTENCY
- **Severity:** S3
- **Label:** DERIVED
- **Claim challenged (verbatim quote):** "The front truncation it causes is visible in the by-year counts: 449 unclassifiable in 2016, 257 in 2017, 257 in 2018, falling to 84 by 2023 as the look-back window fills." — InsiderExperiment/REGISTRATION.md:701-704
- **Evidence:** The artifact behind the sentence is `reports/stage_a1/corpus.json:62-78`, `unclassifiable_by_year`: 2008 1, 2012 1, 2014 1, 2015 11, **2016 449, 2017 257, 2018 256**, 2019 188, 2020 174, 2021 110, **2022 296**, 2023 84, 2024 95, 2025 96, 2026 38 (n = 2,057, which matches `filtered_routine/insufficient_history` at corpus.json:41 and REGISTRATION.md:643). Two problems. (a) The sentence says 257 for 2018; the artifact says 256. 257 was the pre-ADR-008 value: `git diff ccc9b13 cb17046 -- reports/stage_a1/corpus.json` shows `"2018": 257` becoming `"2018": 256` in the same commit that moved one transaction from `insufficient_history` to `routine` (DECISIONS.md:245-249). (b) The four years quoted are the only four for which the series falls monotonically. 2022 is 296, above both 2017 (257) and 2018 (256), and 2024 (95) and 2025 (96) are above 2023 (84). The series does not "fall … as the look-back window fills"; it falls to 2021, spikes in 2022, and then rises again.
- **Recomputation (if any):** Inputs: corpus.json:62-78. Method: sum and inspect monotonicity. Result: sum 2,057; the sequence 2016→2026 is 449, 257, 256, 188, 174, 110, 296, 84, 95, 96, 38 — not monotone after 2021.
- **What would resolve it:** Quoting the whole series, or correcting 2018 to 256 and stating the 2022 exception.
- **Confidence:** HIGH — the artifact is in the repository and the git diff dates the 257→256 change.
- **Invalidated by later commits?:** no — closed repository.
- **Disclosed by authors?:** no.

---

### DRAFT-all-5
- **Repository / SHA:** InsiderExperiment / 12d9fd36cf055cb10ea67a3fc737e404217bc95a
- **Hypothesis or artifact:** The Johnsen programmatic-event filter and the refusal record shipped as `reports/stage_a1/refusals.md` (Standing guard 4, "Refusals are demonstrated by producing them, never asserted", CLAUDE.md:44-46)
- **Direction:** B
- **Class:** INTERNAL_INCONSISTENCY
- **Severity:** S2
- **Label:** DERIVED
- **Claim challenged (verbatim quote):** "The Johnsen filter rejected 209 of 773 clusters." — InsiderExperiment/REGISTRATION.md:693
- **Evidence:** `find_clusters` opens a new cluster at **every buy in the stream** and keeps the forward window from that anchor: `for i, anchor in enumerate(group): … window = [b for b in group[i:] if b.transaction_date <= end]` (InsiderExperiment/src/insider/corpus/cluster.py:76-95). One underlying cluster event of size s therefore produces up to s−2 rows. The stored `cluster` table in the live `var/insider_corpus.db` (read 2026-09-04T05:39Z, UNANCHORED) holds 773 rows of which 209 are `rejected=1`, and those 209 rows come from **10 distinct issuers**: SPG 155, HES 32, DRI 10, MSTR 6, and one each for WPX, CSX, MRVL, CAG, LIN, KDP. Merging overlapping windows within each issuer gives **36 distinct rejected cluster events** (SPG 23, HES 4, MSTR 2, and one each for the other seven), out of **201 distinct cluster events overall** (773 rows, 106 distinct issuers). A second, independent count agrees: exactly 34 of the 209 rejected rows have size 3, and under the nesting the code produces the number of size-3 windows equals the number of rejected events. The shipped `refusals.md` shows this directly: its two Johnsen blocks are the *same* Darden event, cluster_id 369 (size 12) and 370 (size 11, the same buys minus the lowest CIK), both with `"window": ["2020-04-23","2020-04-27"]` (InsiderExperiment/reports/stage_a1/refusals.md:13-21 and 113-121). Secondly, the registered rule is stated per cluster — "A cluster is rejected when a single date-and-price pair accounts for eighty percent or more of the contributing buys" (REGISTRATION.md:272-274) — but the implementation charges a buy only if it appears in **no** surviving window: `johnsen_rejected_only=frozenset(clustered - surviving)` (cluster.py:103) consumed at `src/insider/corpus/build.py:376-378`. A buy inside a programmatic cluster is admitted whenever some sub-window containing it falls under the 0.80 threshold.
- **Recomputation (if any):** Inputs: `var/insider_corpus.db` table `cluster` (773 rows), `attrition` row `filtered_programmatic/johnsen_same_date_price = 274`. Method: (i) group rejected rows by symbol, merge overlapping [window_start, window_end] intervals; (ii) count rejected rows of size 3. Results: 36 merged rejected events / 34 size-3 rows; 201 merged events overall. Under the nesting model the implied number of member buys is 209 + 2×34 = **277** against **274** actually charged, so roughly 3 buys that sat inside a Johnsen-rejected window were nonetheless admitted because they also fell inside a surviving window; the interval-merge count of 36 events implies up to 7. Either way the effect is small; the count inflation is not.
- **What would resolve it:** Reporting distinct cluster events rather than anchored windows (36 of 201, at 10 issuers of 106), or restating the sentence as "209 of 773 anchored five-day windows".
- **Confidence:** HIGH — the count is reproduced from the repository's own stored table and the mechanism is visible in twelve lines of its own source.
- **Invalidated by later commits?:** no — closed repository; the store has not been rewritten since 2026-08-25 19:05 local.
- **Disclosed by authors?:** no — neither REGISTRATION.md Section 15.4 nor DECISIONS.md says the cluster count is per anchor, and nothing records that 74 % of the rejections are one issuer (SPG).

---

### DRAFT-all-6
- **Repository / SHA:** InsiderExperiment / 12d9fd36cf055cb10ea67a3fc737e404217bc95a
- **Hypothesis or artifact:** The "minimum detectable effect" itself, and the ADR-011 reopening boundary built on the equal-weighted secondary
- **Direction:** B
- **Class:** STATISTICAL
- **Severity:** S3
- **Label:** DERIVED
- **Claim challenged (verbatim quote):** "**The equal-weighted secondary would have fired DEGRADED at 34.29 bp.**" — InsiderExperiment/REGISTRATION.md:764 (repeated at REGISTRATION.md:853-854, DECISIONS.md:318-319 and progress.md:42-45)
- **Evidence:** The MDE is defined as `cfg.t_critical * se` with `t_critical=2.0` (InsiderExperiment/src/insider/power/mde.py:66, src/insider/config.py:147), i.e. the effect size that would produce a t-statistic of exactly 2 — a **50 % power** quantity. No power level, β, or 1−β is stated anywhere in the repository: grepping the whole tree for "80 percent power", "type II", "statistical power", "power of the test", "50 percent power" returns nothing. Section 10 registers the critical value only: "**Critical value 2.0.** Registered, two-sided, applied identically to the power computation in Stage A.1 and to the inference in Stage B." (REGISTRATION.md:478-479). Every conclusion the repository draws about what the design "can" and "cannot" detect is therefore a statement about 50 % power. n: primary 2,581 sessions, sd 62.9519 bp, N_eff 2,869.9 (reports/stage_a1/power.json:6-12); secondary 2,581 sessions, sd 43.1862 bp, N_eff 2,798.1 (power.json:69-75).
- **Recomputation (if any):** Inputs: MDE 49.3543 and 34.2897 bp (power.json:12 and 75), t_critical 2.0 (config.py:147), BLOCKED bar 40.0 (config.py:144). Method: multiply by (z_0.975 + z_0.80)/2.0 = (1.959964 + 0.841621)/2.0 = 1.4008 to convert a 50 %-power threshold to a conventional 80 %-power one. Result: primary **69.14** bp per month; equal-weighted secondary **48.03** bp per month, which is **above the 40 bp BLOCKED bar**. At conventional power the secondary would have been BLOCKED too, and the "temptation", the Section 17.4 reopening boundary and ADR-011 in its entirety would not exist. The GO branch survives the same conversion only just: a design at the 20 bp GO boundary has an 80 %-power MDE of 28.0 bp, marginally below the 30 bp bottom of the registered band.
- **What would resolve it:** Registering a power level and reporting the MDE at it, or labelling 49.35 / 34.29 as 50 %-power thresholds wherever they appear, especially in ADR-011 which is written for a future repository to act on.
- **Confidence:** HIGH — the convention is unambiguous in the source and the conversion is standard.
- **Invalidated by later commits?:** no — closed repository.
- **Disclosed by authors?:** no — the repository states the critical value but never a power level, and `mde.py`'s own docstring ("the smallest monthly alpha the design could call significant", src/insider/power/mde.py:54) is accurate while the prose derived from it ("The design cannot detect an effect anywhere in the range the literature reports", REGISTRATION.md:43) is a power statement. Direction: this makes the BLOCKED verdict *more* secure and the DEGRADED-secondary narrative *less* supported.

---

### DRAFT-all-7
- **Repository / SHA:** InsiderExperiment / 12d9fd36cf055cb10ea67a3fc737e404217bc95a
- **Hypothesis or artifact:** CORPUS-GO, the only affirmative verdict this repository fired, and the 1,000-event floor it was fired against
- **Direction:** B
- **Class:** UNSUPPORTED_POSITIVE
- **Severity:** S3
- **Label:** DERIVED
- **Claim challenged (verbatim quote):** "Third, at 1,000 events the expected tracking error is about 4.24 percent and the expected MDE about 27 bp per month, which sits inside DEGRADED with room on both sides. A floor placed at the BLOCKED boundary would admit corpora whose verdict was decided by rounding." — InsiderExperiment/REGISTRATION.md:137-140
- **Evidence:** The floor of 1,000 qualifying events is the bar CORPUS-GO was fired against (REGISTRATION.md:70-71, `corpus_event_floor=1_000` at src/insider/config.py:145), and its derivation rests on two modelling steps that the same run falsified. Step one, book width: "At a hold of H sessions and a steady arrival of lambda qualifying events per session, expected book width is H times lambda when no two events name the same issuer." (REGISTRATION.md:115-117). Step two, tracking error: "For a book of k names with average idiosyncratic volatility sigma and residuals close to independent, tracking error is about sigma over sqrt(k). Taking sigma at 30 percent annualized" (REGISTRATION.md:105-108). Realized figures: 4,585 qualifying events over 2,615 in-span sessions (reports/stage_a1/corpus.json:2, reports/stage_a1/port.json:2), mean priced book 66.93 names and 29.73 effective names (reports/stage_a1/power.json:16, reports/stage_a1/portfolio.json:27), realized tracking error 9.9933 % value-weighted and 6.8556 % equal-weighted (power.json:10 and 73), only 496 distinct issuers behind the 4,585 events (`SELECT COUNT(DISTINCT symbol) FROM event` on `var/insider_corpus.db`, read 2026-09-04T05:39Z, UNANCHORED).
- **Recomputation (if any):** Inputs as listed. Method: evaluate the two registered models at the realized corpus. Results. (a) H×λ: λ = 4585/2520 = 1.8194 events per session, H = 126 → predicted book **229.2** names against a realized priced book of **66.93**, an over-prediction of **3.43×**. (b) σ/√k at σ = 30 %: at the realized 29.73 effective names it predicts 5.502 % against a realized 9.993 %, a factor of **1.816**; at the equal-weighted 66.93 effective names it predicts 3.667 % against a realized 6.856 %, a factor of **1.869**. (c) The floor's own third justification checks out arithmetically on its own terms (30/√50 = 4.243 %; MDE = 2 × 21 × 4.243 %/√252 / √1680 = 27.4 bp) but is falsified in fact: the realized corpus was **4.6×** the floor and the design fired BLOCKED at 49.35 bp, i.e. 1.83× the 27 bp the floor was chosen to deliver. The corpus floor therefore guaranteed none of the property it was registered to guarantee, and CORPUS-GO carries no information about whether the design could be measured.
- **What would resolve it:** A closure note recording that the Section 0.4 dispersion model under-predicted realized tracking error by ~1.85× and over-predicted book width by ~3.4×, so that a successor scaffold does not re-use the σ = 30 %/independent-residuals calibration to set a corpus floor.
- **Confidence:** HIGH for the arithmetic; MEDIUM for the framing, because the σ/√k model is an idiosyncratic-risk model and the realized figure is a tracking error against a differently-weighted benchmark, so part of the 1.85× is systematic mismatch rather than a wrong σ — which is itself the point, since Section 0.4 used the two interchangeably.
- **Invalidated by later commits?:** no — closed repository.
- **Disclosed by authors?:** partly, at REGISTRATION.md:754-757: "Section 0.4 computed that staying out of BLOCKED needs about 23 effective names at 30 percent idiosyncratic volatility, and the realized book carries 29.7 with residuals that are not independent, because insider buying clusters by sector during stress." That discloses the independence failure qualitatively. It does not quantify it, does not mention the 3.43× book-width over-prediction, and Section 17.2's framing — "**The corpus did not fail.** A later reader will see BLOCKED and assume the data was thin. It was not." (REGISTRATION.md:818-820) — presents CORPUS-GO as a clean pass without saying that its floor's justification was wrong by a factor of 1.8 in the same run.

---

### DRAFT-all-8
- **Repository / SHA:** InsiderExperiment / 12d9fd36cf055cb10ea67a3fc737e404217bc95a
- **Hypothesis or artifact:** The book-width figure "71.9 names", used in the closure verdict's explanation of what failed
- **Direction:** B
- **Class:** INTERNAL_INCONSISTENCY
- **Severity:** S3
- **Label:** DERIVED
- **Claim challenged (verbatim quote):** "The value-weighted book holds a mean of **71.9 names and behaves like 29.7 effective names**, because the heaviest name carries **14.9 percent** of the book and the heaviest five carry **33.8 percent**." — InsiderExperiment/REGISTRATION.md:839-842 (also progress.md:31-34, DECISIONS.md:296-298, REGISTRATION.md:249-250 and the Section 15.6 table at REGISTRATION.md:747-750)
- **Evidence:** The book that produced the 49.35 bp verdict is not 71.9 names wide. `reports/stage_a1/power.json:16` records `"book_width_mean": 66.93` for the primary series, and the dispersion store gives the same: mean of the `book_width` column over the 2,581 primary rows is **66.925** (recomputed from `var/insider_dispersion.db`, read 2026-09-04T05:39Z, UNANCHORED). 71.909 is a different quantity: `MembershipSeries.mean_width()` averages the raw post-filing book over non-empty sessions *before* the universe-membership filter (InsiderExperiment/src/insider/portfolio/membership.py:46-54), whereas the series that reaches the power module carries `len(priced)` after 13,750 name-sessions are dropped for not being universe members at the governing formation (src/insider/portfolio/returns.py:189-210, ADR-009 at DECISIONS.md:262-266). `reports/stage_a1/portfolio.json` publishes the two side by side without saying so: `"book_width_mean": 71.909` from the raw membership series next to `"book_width_p10": 46, "book_width_p50": 67, "book_width_p90": 89, "book_width_max": 103` taken from the priced series (portfolio.json:7-12, built at src/insider/portfolio/build.py:52-64). A mean of 71.909 sitting above a p50 of 67 and a p90 of 89 in a roughly symmetric distribution is the visible symptom.
- **Recomputation (if any):** Inputs: `centered_excess.book_width` for (126, value_weighted) in `var/insider_dispersion.db`; portfolio.json:7 and power.json:16. Method: arithmetic mean of the stored widths. Result: **66.925**, matching power.json's 66.93 and differing from the published 71.909 by **7.0 %**. Cross-check: 13,750 dropped name-sessions / (2,581 × 66.925 + 13,750) = **7.37 %**, which is ADR-009's own "about 7.4 percent of held name-sessions" (DECISIONS.md:265-266). Note the identity that makes the discrepancy easy to miss: for the equal-weighted book, effective names equals priced names, so the "66.9" that appears in Section 15.6 as the equal-weighted *effective* names is the same number as the primary's true mean width.
- **What would resolve it:** Reporting the priced book width (66.9) wherever the measured book is described, and labelling 71.9 as pre-membership-filter.
- **Confidence:** HIGH — reproduced from the stored series and traced to two lines of source.
- **Invalidated by later commits?:** no — closed repository.
- **Disclosed by authors?:** no — ADR-009 discloses the 7.4 % drop but nothing says the 71.9 in the verdict narrative is the pre-drop figure while the dispersion behind 49.35 bp used 66.9.

---

### DRAFT-all-9
- **Repository / SHA:** InsiderExperiment / 12d9fd36cf055cb10ea67a3fc737e404217bc95a
- **Hypothesis or artifact:** The registration's own amendment discipline, and Section 16 "Amendments"
- **Direction:** B
- **Class:** PROCESS
- **Severity:** S3
- **Label:** DERIVED
- **Claim challenged (verbatim quote):** "Changing a registered value after that commit requires a numbered amendment in Section 17 carrying its own evidence." — InsiderExperiment/REGISTRATION.md:8-9; and "None in force. Section 0 fired BLOCKED, so no amendment can authorize Stage B." — InsiderExperiment/REGISTRATION.md:800
- **Evidence:** Two registered items changed after data existed, neither by numbered amendment. (a) A registered `Config` field was deleted. `git show fbfc74e:src/insider/config.py` carries `benchmark_id: str` and `benchmark_id="U-LIQ-500-VW"`; `git diff cb17046 672b343 -- src/insider/config.py` shows both lines removed at commit `672b343e1a9c9697b578a02a98dd77c6e73f0603` (2026-08-25T19:11:45-07:00), which is after the corpus was built and CORPUS-GO fired at `ccc9b13a2dd6626f3e2b8e6374b2069c155ec11e` (18:47:16-07:00) and after the power gate ran. `src/insider/config.py:8-9` states the rule in the file itself: "Values here are registered in REGISTRATION.md and frozen before Task 4 computes anything. Changing one after the corpus is built requires a numbered amendment." (b) The registered Section 3 classification rule changed. `git diff cb17046 672b343 -- src/insider/corpus/routine.py` shows `classify` reordered so the routine pattern is tested before the history gate, in the same post-corpus commit. The registration's own Section 3.4 text was never updated and still reads "**Three years of trading history is required to classify at all.** An insider whose first observed trade falls less than three years before the candidate transaction is `insufficient_history`." (REGISTRATION.md:258-260), which the shipped code now contradicts: an insider who traded the candidate month in the three prior years is returned `ROUTINE` even when her earliest observed trade is under three calendar years old (src/insider/corpus/routine.py:74-83). Section 16 was written at the later commit `d8b81f1` and says "None in force."
- **Recomputation (if any):** Git only. Commands run read-only against the live repository: `git log --format='%H|%ad|%cd|%s' --date=iso-strict`, `git show --stat <sha>`, `git diff <a> <b> -- <path>`. Commit ordering: fbfc74e 18:34:56 → 398755b 18:38:50 → ccc9b13 18:47:16 → cb17046 19:11:45 → 672b343 19:11:45 → d8b81f1 19:11:55 → 12d9fd3 23:24:15, all 2026-08-25 at UTC−07:00.
- **What would resolve it:** A Section 17 amendment recording the `benchmark_id` removal and the Section 3.4 reordering, or a correction of Section 3.4's text to match the shipped rule.
- **Confidence:** HIGH — both changes are in the git record with timestamps against the corpus build.
- **Invalidated by later commits?:** no — `12d9fd3` is the last commit and added Section 17 without an amendment entry.
- **Disclosed by authors?:** partly — ADR-008 (DECISIONS.md:226-255) records the ordering change and its one-transaction impact, and ADR-012 (DECISIONS.md:356-374) records how it was found. Neither says the registered Section 3.4 text was left describing the superseded rule, and nothing anywhere records the `benchmark_id` deletion. Impact on results: nil (`benchmark_id` had no enforcement site, which is why the guard forced its removal; the reordering moved one transaction between two excluded labels).

---

### DRAFT-all-10
- **Repository / SHA:** InsiderExperiment / 12d9fd36cf055cb10ea67a3fc737e404217bc95a
- **Hypothesis or artifact:** ADR-002's validation of the SEC structured data sets, shipped as `reports/stage_a1/validation.json`
- **Direction:** B
- **Class:** STATISTICAL
- **Severity:** S3
- **Label:** DERIVED
- **Claim challenged (verbatim quote):** "**Cost.** The corpus depends on the SEC's parse rather than on this repository's. The sample validation is what bounds that risk, and it is a sample, not a census." — InsiderExperiment/DECISIONS.md:68-70, with the sample described at DECISIONS.md:64-65: "**Per-filing XML.** Field-by-field validation on a 25-document sample spread across the whole corpus by entry session. 25 agree, 0 disagree."
- **Evidence:** The sample is drawn only from the survivors. `sample_xml` selects from `SELECT accession, symbol, transaction_date, value_usd, issuer_cik FROM event ORDER BY entry_session, accession` (InsiderExperiment/src/insider/corpus/validate.py:115-123), and the `event` table holds only the 4,585 qualifying events (src/insider/corpus/store.py:12-25, written at src/insider/corpus/build.py:412-420). The comparison it performs — symbol match, officer-or-director, not ten-percent owner, a P transaction on the recorded date with a matching value, 10b5-1 flag not True (validate.py:68-105) — can therefore detect only a wrongly *admitted* event. It cannot detect the failure ADR-002 names as the risk: a purchase the DERA parse dropped, or one it mis-coded into a state the funnel charges earlier (the funnel charges 2,578,217 transactions to `filtered_code` and 8,613 to `unparseable` — REGISTRATION.md:622 and 621 — and none of those is sampled). The complementary coverage check is at document level only ("The ratio of index rows to data set documents is 2.04 to 2.14 and stable across all 53 quarters, so no quarter is short", DECISIONS.md:61-63; verified: 53 quarters, ratios 2.043 to 2.140, 5,077,629 index rows against 2,440,873 dataset documents, `reports/stage_a1/validation.json`).
- **Recomputation (if any):** Inputs: `validation.json` `xml_tally` = `{"agrees": 25, "flag_not_reported_in_xml": 19}`, 25 field checks, 0 disagreements; corpus size 4,585 (corpus.json:2). Method: exact one-sided binomial bound with 0 failures in 25 draws. Result: 1 − 0.05^(1/25) = **11.29 %** upper 95 % bound on the field-disagreement rate among *retained* events (rule of three gives 12 %). The sample is 0.55 % of the corpus and is conditioned on the outcome of every filter it is meant to validate.
- **What would resolve it:** A second sample drawn from the transactions the funnel *rejected* — in particular from `filtered_code` and `unparseable` — checked against the per-filing XML, which is the only draw that can find a missing or mis-coded purchase.
- **Confidence:** MEDIUM — the one-sidedness is certain from the source; its practical importance is low here because the corpus cleared its floor 4.6-fold and the verdict turns on tracking error rather than count.
- **Invalidated by later commits?:** no — closed repository.
- **Disclosed by authors?:** partly — DECISIONS.md:69-70 says "it is a sample, not a census", which discloses the sampling but not the selection on survival, and does not put a bound on the residual rate.

---

### DRAFT-all-11
- **Repository / SHA:** InsiderExperiment / 12d9fd36cf055cb10ea67a3fc737e404217bc95a
- **Hypothesis or artifact:** The closure note's account of what was fetched and what the 2.78 GB cache contains
- **Direction:** B
- **Class:** STALE_FIGURE
- **Severity:** S3
- **Label:** DERIVED
- **Claim challenged (verbatim quote):** "53 quarterly SEC structured Form 345 data sets covering 2013q1 to 2026q1, retrieved in **214 wire requests** totalling **2.78 GB** with **zero non-200 responses** under an 8 per second throttle against the SEC's stated 10 per second ceiling." — InsiderExperiment/REGISTRATION.md:827-830 (same sentence at progress.md:23-27)
- **Evidence:** The fetch ledger (`ledgers/fetch.jsonl`, untracked, 684 rows, read 2026-09-04T05:39Z, UNANCHORED) shows 214 wire requests and 470 cache hits, all status 200, wire bytes **2,783,280,665** — which is exactly the claimed 2.78 GB and exactly the `du -sb cache/` figure of 2,783,280,665 bytes, so the "cache equals the wire total byte for byte" claim (REGISTRATION.md:832-833) holds precisely. But the 214 requests and the 2.78 GB are the whole campaign, not the data sets: by URL family the wire requests are 53 `*_form345.zip`, 53 full-index files, 41 per-filing XML, 41 filing `index.json`, 25 `data.sec.gov/submissions` and 1 `company_tickers.json`, and the bytes are **570,492,991 for the 53 data sets (20.5 %)**, **2,207,515,405 for the full-index archives (79.3 %)**, 4,018,868 for submissions, 818,524 for the index.json lookups and 434,877 for the XML. The full-index archives are the cross-check ADR-002 describes as "An independent per-quarter Form 4 count" (DECISIONS.md:60-61), so four fifths of the "2.78 GB corpus cache" that Section 17.2 and progress.md:143-149 discuss pruning is not the corpus. Separately, ADR-002 states the data sets are "53 files totalling about 750 MB" (DECISIONS.md:58) against a measured 570 MB, a 32 % overstatement.
- **Recomputation (if any):** Inputs: `ledgers/fetch.jsonl` (684 JSON rows). Method: group by `served_from`, `status` and URL family; sum `bytes_read`. Results as above; wire request count 214 with 214 distinct URLs and zero URLs fetched twice on the wire, which independently confirms "nothing was fetched twice". Statuses: `Counter({200: 684})`, and `insider.edgar.client.fetch` records a row *before* it tests the status code (src/insider/edgar/client.py:76-90), so the "zero non-200 responses" claim is falsifiable from the artifact and holds.
- **What would resolve it:** Attributing the 214 requests and 2.78 GB to the campaign rather than to the 53 data sets, and correcting ADR-002's 750 MB.
- **Confidence:** HIGH — reproduced from the repository's own append-only ledger, which is the artifact the claim cites.
- **Invalidated by later commits?:** no — closed repository; the ledger has not been appended to since 2026-08-25 19:06 local.
- **Disclosed by authors?:** no.

---

### DRAFT-all-12
- **Repository / SHA:** InsiderExperiment / 12d9fd36cf055cb10ea67a3fc737e404217bc95a
- **Hypothesis or artifact:** The fixed closure verdict language (Section 17.1, ADR-010, progress.md, CLAUDE.md)
- **Direction:** B
- **Class:** OVER_CLOSED
- **Severity:** S3
- **Label:** DERIVED
- **Claim challenged (verbatim quote):** "**The registered primary design cannot resolve the effect at achievable power. The minimum detectable effect is 49.35 bp per month against a registered BLOCKED floor of 40 and against a decayed literature band of 30 to 40 bp per month gross and 13 to 35 bp per month net at the six-month hold. Stage B is never written. The repo closes on the finding.**" — InsiderExperiment/REGISTRATION.md:812-816 (identical at DECISIONS.md:288-292 and progress.md:15-18; progress.md:174 declares it "The fixed verdict language, not to be softened or strengthened")
- **Evidence:** The repository states that the number the verdict is read against is an upper bound of unmeasured size. REGISTRATION.md:790-796: "The Section 14.3 conservatism is the only one large enough to matter. A Carhart regression would absorb the persistent size tilt between a mid-cap book and a mega-cap-weighted benchmark, and the residual MDE would be lower than 49.35 by an amount this stage did not measure and will not measure, because measuring it after seeing BLOCKED is choosing a method by its answer." Section 14.3 says the same structurally: "The gate can therefore fire BLOCKED on a design Stage B would have found marginally better" (REGISTRATION.md:581-582), with "marginally" unquantified. The margin is 23 %: 49.35 against a bar of 40. None of the four places the fixed verdict language appears carries that qualification.
- **Recomputation (if any):** Inputs: `sd_portfolio_daily = 0.014065`, `corr_portfolio_benchmark = 0.903981` (reports/stage_a1/portfolio.json:20 and 22), `sd_daily_excess_bp = 62.9519`, MDE 49.3543 (power.json:9 and 12), bar 40.0 (config.py:144). Method: the Stage A.1 excess return imposes a market beta of 1 against the universe benchmark; a regression frees it, so bound the beta channel by `sd_p·√(1−ρ²)` and scale the MDE by the ratio. Result: freeing the market beta alone gives a residual sd of **60.138 bp** against 62.9519, i.e. an MDE of **47.15 bp — still above the 40 bp bar**. To reach 40 bp the excess series would need a total factor R² of **34.31 %**, and after the market channel the remaining three Carhart factors would have to explain a further **28.02 %** of the residual variance. So the disclosed conservatism does *not* overturn BLOCKED through the only channel I can bound from the stored primitives, and the honest statement of the gap is that it is one unmeasured size/value/momentum term wide, not that the verdict is wrong.
- **What would resolve it:** Adding the bound above (or any bound) to the closure language, so a later reader knows the 49.35 is an upper bound and how far above the bar it sits after the one correction that can be computed without opening the seal.
- **Confidence:** MEDIUM — the recomputation is exact for the beta channel but says nothing about SMB/HML/UMD, which the repository deliberately did not measure.
- **Invalidated by later commits?:** no — closed repository.
- **Disclosed by authors?:** yes (REGISTRATION.md:578-583 and 790-796, DECISIONS.md:29-32). The authors disclose the upward bias clearly and give a defensible reason for not measuring it. The finding is only that the verdict sentence that is fixed against softening, and repeated in four documents, omits a limitation the registration itself calls "the only one large enough to matter".

---

### DRAFT-all-13
- **Repository / SHA:** InsiderExperiment / 12d9fd36cf055cb10ea67a3fc737e404217bc95a
- **Hypothesis or artifact:** `reports/stage_a1/mutations.json`, the artifact backing "106 tests green"
- **Direction:** B
- **Class:** PROVENANCE
- **Severity:** S4
- **Label:** DERIVED
- **Claim challenged (verbatim quote):** "`make all` runs clean: ruff, ruff format, mypy strict on 56 files, 106 tests." — InsiderExperiment/progress.md:216-218 (commit `672b343` is titled "test: 106 tests green, and five registered mutations that fail the right guard")
- **Evidence:** The only stored record of the full suite is `"final_suite": "................................. [100%]"` (InsiderExperiment/reports/stage_a1/mutations.json:49). That is a pytest progress line, not a result line: it carries 33 dots, no pass count and no status. `scripts/mutations.py:118-122` picks the last line containing "passed", "failed" or "error" and otherwise falls back to `output.splitlines()[-1]`; the stored value shows the fallback was taken, so no summary line was captured. The harness did check the return code (`if code != 0: failures += 1`, scripts/mutations.py:178-179), so the run was green — but the shipped artifact does not evidence it. Collected-test count: the ten test modules define 96 `test_` functions and expand under `@pytest.mark.parametrize` to 105 by my count, which is what a 72 + 33 two-line progress bar at pytest's default 80-column non-tty width implies.
- **Recomputation (if any):** Inputs: `tests/test_*.py` (96 `def test_` definitions), `mutations.json:49`. Method: count definitions and parametrize expansions; count dots in the stored progress line. Result: 96 definitions, ~105 collected, 33 dots on the final progress line.
- **What would resolve it:** Storing the pytest summary line (or `--junitxml`) rather than whatever line happens to be last.
- **Confidence:** MEDIUM — the absence of a summary in the artifact is certain; my 105 collection count is an estimate from static parsing and may be one off the claimed 106.
- **Invalidated by later commits?:** no — closed repository.
- **Disclosed by authors?:** no.

---

### DRAFT-all-14
- **Repository / SHA:** InsiderExperiment / 12d9fd36cf055cb10ea67a3fc737e404217bc95a
- **Hypothesis or artifact:** The measured-cost and timing record in the Stage A.1 progress entry
- **Direction:** B
- **Class:** PROVENANCE
- **Severity:** S4
- **Label:** DERIVED
- **Claim challenged (verbatim quote):** "Timings are wall clock, session start 18:20 UTC, boundaries taken from commit timestamps where one exists." — InsiderExperiment/progress.md:193-194
- **Evidence:** The commit timestamps it cites are local, not UTC. `git log --date=iso-strict` gives `fbfc74e 2026-08-25T18:34:56-07:00` … `12d9fd3 2026-08-25T23:24:15-07:00`, i.e. 2026-08-26T01:34:56Z to 2026-08-26T06:24:15Z. The untracked fetch ledger corroborates: its first wire row is `"recorded_at": "2026-08-26T01:35:18+00:00"` (`ledgers/fetch.jsonl` line 1, read 2026-09-04T05:39Z, UNANCHORED), 22 seconds after the 18:34:56 commit. REGISTRATION.md:589-590 inherits the same offset: "Empty at the time Section 0 was committed at 18:34 on 2026-08-25." The stated session start of "18:20 UTC" is 2026-08-26T01:20Z.
- **Recomputation (if any):** None beyond the offset conversion (−07:00).
- **What would resolve it:** Dropping "UTC" or converting the times.
- **Confidence:** HIGH — two independent clocks in the repository's own artifacts.
- **Invalidated by later commits?:** no — closed repository.
- **Disclosed by authors?:** no. Immaterial to every result; recorded because the progress entry presents the commit record as the auditable cost measurement ("**Cost, measured rather than asserted.**", progress.md:115).

---

## What I checked and found sound

Everything below was checked with the thesis in hand and did not support it.

1. **The whole power chain reproduces exactly from the stored primitives.** I recomputed sample sd, the Newey–West Bartlett variance inflation, effective periods, annualized tracking error, the monthly standard error and the MDE for all four series directly from `var/insider_dispersion.db` (read 2026-09-04T05:39Z). Every figure in `reports/stage_a1/power.json` matches to the last published digit: 126 VW n = 2,581, sd 62.9519 bp, TE 9.9933 %, VIF 0.8993, N_eff 2,869.9, SE 24.6771 bp, MDE 49.3543; 21 VW 81.4849; 63 VW 57.3398; 126 EW 34.2897. The lag grid reproduces too (50.1903 / 49.3543 / 49.1057 / 49.5319 at lags 5/21/63/126), so REGISTRATION.md:721-723's "The verdict does not turn on the bandwidth choice" is correct.
2. **The dispersion store really is centred and carries no first moment.** `math.fsum` of the stored series is −1.4e−16, 1.7e−16, −2.9e−16 and −7.5e−17 for the four series. The seal architecture (ADR-006) is as described in code: `read_sealed_returns` is defined once (`src/insider/eval/evaluator.py:33`) and refuses before opening the file while Section 12 is empty; the power package imports only `config`, `paths` and stdlib. I did not open `var/insider_sealed.db`.
3. **No look-ahead in the routine/opportunistic rule.** I suspected one: `TradeHistory` is accumulated over the entire 2013q1–2026q1 stream and `classify` is called after the scan (`src/insider/corpus/build.py:156-158, 380`). But the routine predicate only queries calendar months `(when.year − 1..3, when.month)`, all strictly prior (`src/insider/corpus/routine.py:75-78`), and `first_trade` is a minimum, which later trades cannot raise. Both predicates are invariant to trades after the candidate date. `tests/test_guards.py:397` guards it.
4. **The attrition funnel is internally exact.** 8,613 + 2,578,217 + 131,222 + 148,883 + 2,362 + 2,213 + 0 + 4,585 = 2,876,095 = the stated intake; every sub-reason sums to its parent; the 17 `filtered_code` sub-codes sum to 2,578,217; every published share rounds correctly. 9,160 reached the universe filter and passed, 148,883 did not, giving the published 5.8 % / 94.2 %.
5. **The filing-lag statistics.** Reconstructed from `corpus.json` `lag_distribution` (n = 4,585): 51.32 % within one calendar day (DECISIONS.md:98-99 says 51.3), 73.00 % within two (REGISTRATION.md:683 says 73.0), 95.86 % within four (says 95.9), 91 events beyond ten days (says 91), max 1,988 (says 1,988), mean 9.5154 (says 9.52). Only p99 differs trivially (228 by nearest rank against the published 230).
6. **Session coverage.** 1 − 12/2,615 = 0.9954111, exactly the published `session_coverage`, and the denominator is the in-span session count in `port.json`. The coverage floor is applied to book non-emptiness, which is what Section 0.3 registers.
7. **Section 0.4's own arithmetic is internally correct** even where its model is wrong: 19.52 bp / 3.10 % and 39.04 bp / 6.20 % invert correctly at N_eff = 1,680; 23.4 and 93.7 names follow from σ/√k at σ = 30 %; 468 / 1,000 / 1,875 events follow from H × λ at H = 126 and 2,520 sessions; the 11.8 % coverage penalty is √1.25.
8. **The cost model.** 32/6 = 5.333 and 100/6 = 16.667 bp per month; the net band 13.33 to 34.67 follows from the registered pairing, and `insider/cost.py:48-57` states plainly that the low end is the number a verdict is read against, so the appearance of the optimistic bar in the band's upper end is registered rather than smuggled.
9. **"Zero dollars, zero non-200, nothing fetched twice."** All 684 ledger rows are status 200; the client records a row before it inspects the status, so a non-200 would appear; 214 wire requests against 214 distinct wire URLs; wire bytes equal `du -sb cache/` to the byte. No paid API appears anywhere in the ledger.
10. **The XML and full-index validation figures are real.** `validation.json` holds 25 field checks, 25 agree, 0 disagree, 19 of 25 with the 10b5-1 box absent (against 73.06 % corpus-wide), 53 quarters with ratios 2.043–2.140 (none outside the published 2.04–2.14), 21 of 25 issuer symbols present in the SEC's current ticker list (which is the evidence ADR-007 cites for rejecting the XBRL weighting route).
11. **The equal-weighted secondary is genuinely not promoted.** It is registered as the secondary weighting at REGISTRATION.md:387 and as non-verdict-bearing at REGISTRATION.md:474-476, both in commits `398755b` (18:38) — before the corpus was built at 18:47 and before the power gate ran at 19:11. `insider.power.report._plan` fires the gate on `cfg.primary_weighting` only (`src/insider/power/report.py:23-28, 73-74, 106`). ADR-011's reopening boundary is a stronger disclosure than I expected to find.
12. **The Section 0 bars were never moved.** `git diff fbfc74e 12d9fd3 -- REGISTRATION.md` shows only additions after line 157; `git diff fbfc74e 12d9fd3 -- src/insider/config.py` shows a single change, the `benchmark_id` deletion (DRAFT-all-9). `mde_go_ceiling_bp`, `mde_degraded_ceiling_bp`, `corpus_event_floor`, `corpus_coverage_floor`, `t_critical`, `newey_west_lags` and `decayed_gross_band_bp` are byte-identical from the first commit, which is the single most important thing an audit of a pre-registration can check, and it passes.
13. **ADR-012's self-correction is exemplary.** DECISIONS.md:365-374 volunteers that the parse-tree config guard "catches decoration, not misuse" and that the repository did not solve the residual. I looked for the softer version of that claim and did not find one.
14. **The mutation harness edits real source.** `scripts/mutations.py:143-155` writes, runs, restores and asserts byte equality, and purges `__pycache__` first for the reason ADR-012 gives. The five mutations are on real registered values, not fixtures.
15. **The universe port is verified, not asserted.** `tests/test_universe_port.py:85-91` re-derives membership from the AiTrader source bars at 2016-04-01, 2021-04-01 and 2026-07-01 and asserts 500 of 500 with rank-by-rank comparison; `pyproject.toml:62-68` sets `addopts = "-q --strict-markers"` with no `-m "not slow"` deselection, so the slow test runs in `make test`. `port.json` records both source hashes unchanged across the read.
16. **The V3/V7 distinction is maintained where it matters.** REGISTRATION.md:446-448 and 771-774 insist a power closure is not a measured null, and progress.md's family record does qualify its headline immediately: "Two closed on power rather than on absent signal … This one closed on power alone and closed before measurement." (progress.md:108-113). I looked for the merge and it is not there.
17. **Section 4's narrowing is registered in advance and its cost is measured, not estimated.** REGISTRATION.md:312-329 states the exclusion, ADR-004 puts 148,883 against 9,160 on it, and REGISTRATION.md:326-328 draws the correct conclusion ("a negative here does not refute the literature"). This is the opposite of the failure I was looking for.
18. **The 10b5-1 absence is handled as a recorded state, not imputed** (`src/insider/corpus/classify.py:80-89`, `src/insider/absence.py`), with the 3,350 of 4,585 (73.06 %) absent count published. The composition of the qualifying set is also consistent: 4,167 opportunistic plus 418 routine/insufficient-history events rescued by surviving cluster membership under the registered Section 3.8 disjunction (`SELECT routine_class, COUNT(*) FROM event` returns 4,167 / 414 / 4).

## Live-repo access log

`git -C /home/kiros-li/Documents/GitHub/InsiderExperiment status --porcelain`

Before (first live access, 2026-09-04T05:2xZ): *(empty — no output)*

After (last live access, 2026-09-04T05:39:01Z): *(empty — no output)*

The working tree was clean before and after. Live-repo actions were limited to: `git status --porcelain`, `git log`, `git show --stat`, `git show <sha>:<path>`, `git diff <a> <b> -- <path>`; read-only reads of `.gitignore`, `_CLOSED_DO_NOT_RUN_HERE`, `ledgers/fetch.jsonl`, `ledgers/evidence.jsonl`, `du -sb cache/ var/`, and read-only SQLite URI connections (`mode=ro`) to `var/insider_corpus.db` and `var/insider_dispersion.db`. `var/insider_sealed.db` was not opened. `.env` was not opened. Nothing was written anywhere under the audited repository; all scratch output went to `/tmp/claude-1000/-home-kiros-li-Documents-GitHub-program-audit/5ca157a0-1746-4eb9-a1b8-f3732ea42bf4/scratchpad/work/agentB-insider/`.
