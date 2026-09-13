# Agent A draft findings — retail-power-limits (part: all)

Repository: retail-power-limits @ dda39b2f148569a6fe9be956a979471b2330611d (main, 2026-08-29).
Read: SNAP/retail-power-limits in full (README.md, progress.md, DECISIONS.md, SOURCES.md,
docs/the-power-limit.md, rplimits/*.py, tests/*.py, Makefile, pyproject.toml, .gitignore), plus the
live repository's git history (three commits, read-only). Recomputation script and output:
scratchpad/work/agentA-rpl/recompute.py (all inputs are figures quoted in this repository; the
line references below point at where each input is quoted).

Framing note. This repository closes no hypothesis of its own. It is a secondary-source note that
*carries* seven sibling closures and argues that four of them were power closures and nothing more.
Direction-A findings here are therefore about (a) places where the note's own quoted figures show a
closure it carries resting on weaker grounds than the label the note adopts, and (b) the note's
own reopen condition ("What would change the conclusion"), which is stated more narrowly than the
note's own evidence supports. Every figure below is the note's; nothing was read from a sibling
repository. Items that need a sibling read are marked for the cross-repo pass.

---

### DRAFT-all-1
- **Repository / SHA:** retail-power-limits / dda39b2f148569a6fe9be956a979471b2330611d
- **Hypothesis or artifact:** HFExperiment H-F (12-1 cross-sectional momentum, forward shadow series) as carried by the note; the "eight to eleven years" horizon used to make it a power case.
- **Direction:** A
- **Class:** STATISTICAL
- **Severity:** S2
- **Label:** DERIVED
- **Claim challenged (verbatim quote):** "Its own registration priced the forward version at 2,061 trading days to clear zero and 2,852 to clear the cost hurdle. Eight to eleven years." — retail-power-limits/docs/the-power-limit.md:114-116; and the horizon is then attributed to the domain rather than the procedure: "the arithmetic that closed them is the arithmetic that would close a better model just as fast." — retail-power-limits/docs/the-power-limit.md:365-366
- **Evidence:** The 2,061/2,852-day figures are explicitly conditional on a *confidence sequence*: "Under the frozen confidence sequence, with the sample mean holding at 27.99 bp per day, the lower bound clears zero at day 2,061 and clears the measured 4.07 bp per day cost hurdle at day 2,852." (retail-power-limits/SOURCES.md:142; rplimits/cases.py:269-273). The note's own inputs: excess 27.99 bp/day (SOURCES.md:130), tracking error 66.4 % annualised, "daily noise near 418 bp" (SOURCES.md:130), holdout 2.55 years (SOURCES.md:134), z 1.668 on that holdout (SOURCES.md:134). Backing the multiplier out of the CS figures: 27.99·√2061/418.3 = 3.04 and (27.99−4.07)·√2852/418.3 = 3.05 — i.e. the frozen sequence's boundary at N≈2,000–2,900 is ≈3.05 standard errors wide. A fixed-N one-sided 5 % test is 1.645 SE wide; a two-sided 5 % test 1.96 SE. The same series under the same "mean holds" convention therefore clears zero at 604 days (2.4 y) one-sided or 858 days (3.4 y) two-sided, and clears the 4.07 bp hurdle at 827 days (3.3 y) or 1,175 days (4.7 y). The CS costs a factor of 3.4 in sample relative to a one-sided fixed-N test. (Even at 80 % power rather than "mean holds", a one-sided fixed-N design needs 1,381 / 1,891 days = 5.5 / 7.5 y — still below 2,061 / 2,852.) The 2.50 bar the AiTrader round used is exactly the one-sided Bonferroni bar for eight hypotheses (Φ⁻¹(1−0.05/8) = 2.498); a single pre-registered forward hypothesis does not carry that correction, and z 1.668 already clears the uncorrected one-sided 5 % bar (p = 0.048).
- **Recomputation (if any):** Inputs: mean 27.99 bp/day (SOURCES.md:130), hurdle 4.07 bp/day (SOURCES.md:142), TE 0.664 → daily sd 0.664/√252 = 418.3 bp (SOURCES.md:130), CS crossing days 2,061 and 2,852 (SOURCES.md:142). Method: N = (z·sd/μ)² for fixed-N; implied CS multiplier = μ√N/sd. Results: implied CS multiplier 3.04–3.05; fixed-N one-sided 5 %: 604 d (zero) / 827 d (hurdle); two-sided 5 %: 858 / 1,175 d; at the corrected 2.50 bar: 1,396 / 1,911 d. Script: scratchpad/work/agentA-rpl/recompute.py §3.
- **What would resolve it:** Read HFExperiment REGISTRATION.md Section 11 (cross-repo) for the confidence-sequence family and α, and for whether a fixed-horizon alternative was considered and rejected. If the CS was chosen for anytime-validity, the note should attribute "eight to eleven years" to that choice, not to the domain, and its "not a better estimator" sentence should be qualified.
- **Confidence:** MEDIUM — the fixed-N arithmetic reproduces the note's own z 1.668 (1.70 at 643 days) and the CS multiplier is backed out from two independent crossing figures that agree (3.04 vs 3.05), but the CS's exact parameters are not in this repository.
- **Invalidated by later commits?:** no — the repository has three commits, all on 2026-08-29, and no later commit touches these figures; HFExperiment is closed.
- **Disclosed by authors?:** no — the note discloses that the figures come from a confidence sequence (SOURCES.md:142) but nowhere states that the procedure, rather than the domain, accounts for roughly a factor of three of the horizon; the conclusion section says the opposite (docs/the-power-limit.md:363-366).

### DRAFT-all-2
- **Repository / SHA:** retail-power-limits / dda39b2f148569a6fe9be956a979471b2330611d
- **Hypothesis or artifact:** NPDExperiment (numeric-LLM cross-sectional ranking) as carried; the "above the whole band" reading of MDE 0.0512.
- **Direction:** A
- **Class:** STATISTICAL
- **Severity:** S2
- **Label:** DERIVED
- **Claim challenged (verbatim quote):** "found that the realized minimum detectable contrast was 0.0512 against a realistic effect band of 0.01 to 0.05. The design could not have detected an effect anywhere in the range the literature reports." — retail-power-limits/docs/the-power-limit.md:84-86 (the same sentence is re-quoted from InsiderExperiment at docs/the-power-limit.md:186-188 and carried as "above the whole band" in the headline table, docs/the-power-limit.md:72).
- **Evidence:** A minimum detectable effect is the effect at which a test reaches its design power; it is not a detection cliff. With MDE 0.0512 and band top 0.05, the margin is 0.0012 (2.4 %). Inputs quoted in this repository: realized contrast sd 0.36339 (SOURCES.md:38), 404 evaluable days and 125.6 independent-equivalent days after 3.4× inflation (SOURCES.md:42), accrual "about 21 trading days a month" (SOURCES.md:46). None of the standard conventions reproduces 0.0512 exactly from (0.36339, 125.6) — the implied multiplier is 1.58 on N_eff = 125.6, 2.83 on N = 404 un-inflated, 1.54 on 404 inflated — so the convention cannot be recovered here; but under every convention the design had substantial power at the top of the band: at true contrast 0.05, power is 48 % (critical-value convention, two-sided), 68 % (80 %-power one-sided) or 78 % (80 %-power two-sided); at 0.04, 33–59 %; at 0.03, 21–38 %. "Could not have detected an effect anywhere in the range" is therefore not what the number says; "could not resolve the lower half of the band and was roughly a coin-flip to 80 % at its top" is. Separately, (0.0512/0.05)² − 1 = 4.9 %, i.e. about 20 more evaluable days — one month of the quoted accrual — would put the realized MDE inside the band. The note's own honest reading at docs/the-power-limit.md:87-88 ("an underpowered unresolved, not a tight null") is correct; the sentence at 85-86 is stronger than that reading and stronger than the arithmetic.
- **Recomputation (if any):** Inputs: MDE 0.0512 (SOURCES.md:38), band 0.01–0.05 (SOURCES.md:34), sd 0.36339 and N_eff 125.6 / N 404 (SOURCES.md:38,42). Method: SE = MDE/m for m ∈ {1.96, 2.487, 2.802}; power = 1−Φ(z_α − effect/SE) (+ lower tail for two-sided). Results as in Evidence; script scratchpad/work/agentA-rpl/recompute.py §1.
- **What would resolve it:** Cross-repo: NPDExperiment REGISTRATION.md Section 9 for the MDE convention (power target, sidedness, which N) and progress.md B.2 for the realized point contrast and its interval. If the point estimate sits on the hypothesis side with a wide interval, the note's "above the whole band" headline should be softened to the note's own line 87-88 wording.
- **Confidence:** MEDIUM — the power curve is convention-dependent, but the conclusion (non-trivial power at the band top; a 5 % sample shortfall against the band edge) holds under all three conventions tried.
- **Invalidated by later commits?:** no — no later commit in this repository; NPDExperiment is closed and its store was opened once.
- **Disclosed by authors?:** partially — docs/the-power-limit.md:87-88 gives the correct softer reading ("underpowered unresolved, not a tight null"), but the stronger sentence at 85-86 and the headline "above the whole band" (docs:72, README.md:20) remain and the honesty test pins the headline figures, not the softer reading.

### DRAFT-all-3
- **Repository / SHA:** retail-power-limits / dda39b2f148569a6fe9be956a979471b2330611d
- **Hypothesis or artifact:** NPDExperiment — the better-powered shorter-horizon secondary named in ADR-007 and the two further horizons proposed post hoc, neither run on the already-collected 415 rankings.
- **Direction:** A
- **Class:** OVER_CLOSED
- **Severity:** S3
- **Label:** READ
- **Claim challenged (verbatim quote):** "The registration said so, in writing, before a cent was spent, and chose not to repair it by promoting the better-powered secondary — because promoting a secondary after seeing a result is the move the repository existed to prevent." — retail-power-limits/docs/the-power-limit.md:165-168; and "When a post-hoc amendment proposed scoring the same data at two more horizons, the registration voided it: *scoring spent data against new horizons is a second look however it is labelled*." — retail-power-limits/docs/the-power-limit.md:249-252
- **Evidence:** The note states that the power defect was known "before collection began" and "before a cent was spent" (docs/the-power-limit.md:161-166): a five-session horizon in which consecutive days share four fifths of their window, inflating variance 3.4× and cutting effective days 427 → 125.6. The stated reason for not promoting the better-powered secondary — that promotion "after seeing a result" is forbidden — does not apply at the moment the note says the decision was taken, because no result had yet been seen. The effect band is stated as "daily rank IC 0.01 to 0.05" (SOURCES.md:34; cases.py:90), which is a one-session quantity, while the primary was scored at a five-session horizon. On the note's own figures, removing the overlap inflation on the same collected data (N_eff 125.6 → 404, same contrast sd) gives an MDE of 0.0512·√(125.6/404) = 0.0285 — inside the band, resolving roughly its upper 45 %. The data cost nothing further to score ("the spent data" already exists; rerun of a *fresh* window is priced at about 7 USD, docs:243). The closure "unresolved at achievable power" is right for the registered primary; the repository-level closure with the one-session scoring never run leaves a named, zero-dollar variant untested.
- **Recomputation (if any):** MDE_1-session ≈ 0.0512 × √(125.6/404) = 0.0285 (inputs SOURCES.md:38,42; assumes the one-session contrast sd equals the five-session sd, which under the null is approximately true for rank IC). Script §1.
- **What would resolve it:** Cross-repo: NPDExperiment REGISTRATION.md Section 9 / DECISIONS.md ADR-007 — was the secondary's power registered, and does the registration permit a non-verdict-bearing exploratory scoring of the stored rankings at the one-session horizon (labelled as a second look)? If yes, running it costs nothing and bounds the question the primary could not.
- **Confidence:** MEDIUM — the timing inconsistency is in the note's own sentence; the 0.0285 rests on an equal-sd assumption and on the note's characterisation of the secondary as "better-powered".
- **Invalidated by later commits?:** no — no later commits here; NPDExperiment's amendment log is described as sealed.
- **Disclosed by authors?:** yes (docs/the-power-limit.md:161-168, 249-253) — the note discloses that the secondary was not promoted and that the post-hoc horizons were voided, and endorses both; what it does not address is that the promotion decision predates any result, or that the band is a daily quantity.

### DRAFT-all-4
- **Repository / SHA:** retail-power-limits / dda39b2f148569a6fe9be956a979471b2330611d
- **Hypothesis or artifact:** ETFExperiment H1 (spot-BTC ETF flow prints → next-day BTC return) as carried; the "untestable at achievable power" label and the "no budget shortens it" reading.
- **Direction:** A
- **Class:** OVER_CLOSED
- **Severity:** S3
- **Label:** READ
- **Claim challenged (verbatim quote):** "ETFExperiment could not buy history at any price, because the as-printed record was never archived — its binding constraint was calendar time, and no budget shortens it." — retail-power-limits/docs/the-power-limit.md:380-382; carried as "untestable at achievable power" at docs/the-power-limit.md:74 and README.md:22.
- **Evidence:** The note's own Amendment-6 figures: "roughly 302 admissible days by 2027-10-31, which clears the governing 300 at the *published* 0.18 magnitude by two days" (docs/the-power-limit.md:134-136; SOURCES.md:122). Forward accrual is 20.8 admissible days per month (SOURCES.md:106) at "Zero dollars, no capital and no credential at any point" (SOURCES.md:114). So the calendar path to the governing N at the published magnitude was known, finite (≈14 months from 2026-08-28), and free; the closure fired on the registered deadline of 2027-03-31 (163 vs 300) and the collector was then disarmed ("Disarm etf-snap", SOURCES.md:215; rplimits/sources.py:123-129). Disarming a zero-cost forward collector is what converts "not by the registered deadline" into "not at achievable power"; every month disarmed pushes the 300-day crossing back one-for-one. Under the *registered* 0.09 assumption the closure is sound on the note's figures (845 → ≈40 months; >1,200 → ≈57 months). The label merges the two cases; the README carries only the label.
- **Recomputation (if any):** Inputs: 11 admissible days at closure 2026-08-28 (SOURCES.md:106), accrual 20.8/month (SOURCES.md:106), N targets 237/300/845/1,200 (SOURCES.md:102). Method: months = (N−11)/20.8. Results: N=300 reached ≈13.9 months → ≈2027-10-24; N=237 (E1 at 0.18) ≈10.9 months → ≈2027-07; N=845 ≈40 months → ≈2029-12; N>1,200 ≈57 months → ≈2031-06. Sensitivity: at 20.5/month the 2027-10-31 figure is exactly 300; at 21.1/month, 308 — the two-day margin is inside the accrual-rate uncertainty. Script §4.
- **What would resolve it:** Cross-repo: ETFExperiment REGISTRATION.md Amendments 5–6 and ADR-019 (the "reopen-path" the disarm commit says it corrected, SOURCES.md:215): does the registration forbid extending the deadline, and what does the reopen path require? If the reopen path is "re-arm and wait", the honest label for the published-magnitude case is "parked until ≈2027-11", not "untestable".
- **Confidence:** MEDIUM — the calendar arithmetic uses only the note's figures and reproduces its 163 and 302; whether a deadline extension was permissible is not readable here.
- **Invalidated by later commits?:** no — the anchored repository has no later commits; the sibling is described as closed and disarmed.
- **Disclosed by authors?:** partially — the 302/300 figure and its date are disclosed as a *correction of a handed-over figure* (docs/the-power-limit.md:132-139; SOURCES.md:122; DECISIONS.md:101-104), but the note treats it as "a different question than the closure" and does not reconcile it with "no budget shortens it" or with disarming the collector.

### DRAFT-all-5
- **Repository / SHA:** retail-power-limits / dda39b2f148569a6fe9be956a979471b2330611d
- **Hypothesis or artifact:** ETFExperiment H1 — the data-availability half of the closure (as-printed flow history).
- **Direction:** A
- **Class:** OVER_CLOSED
- **Severity:** S3
- **Label:** READ
- **Claim challenged (verbatim quote):** "The as-printed flow history needed to test the design does not exist in any free archive: archive capture density measured 11 of 333 days, 3.30 percent, against a registered 60 percent bar." — retail-power-limits/docs/the-power-limit.md:101-103
- **Evidence:** The unavailability is of *as-printed* captures (Wayback-style snapshots of the print page: 11 of 333 days). As-revised daily net-flow histories for the US spot-BTC ETFs from launch (2024-01-11) are, to my knowledge, published without charge by Farside Investors (farside.co.uk/btc/, the table the "prints" are usually read from), The Block's data dashboard, CoinGlass (ETF flow page) and SoSoValue; and the primitive the flows are computed from — daily shares outstanding and NAV per fund — is published by each issuer (e.g. iShares IBIT, Fidelity FBTC, Grayscale GBTC daily fund pages). None of these is named in this repository, and none is as-printed; the design's as-printed requirement exists to exclude revision look-ahead. Whether that exclusion is worth the whole closure is measurable: the 11 captured as-printed days, and every forward day the collector captured, can be compared with the later-revised value to bound the revision magnitude. If revisions are small relative to the flow's cross-day dispersion, a registered amendment using the revised history would supply the ≈500 trading days since launch at once, against a requirement of 300 at the published magnitude (SOURCES.md:102). The note's stronger phrasing "could not buy history at any price" (docs:380-381) also overlooks that point-in-time fund-flow fields exist on paid terminals; that is outside retail scope but is not "any price".
- **Recomputation (if any):** none beyond 11/333 = 3.30 % (confirmed) and 2024-01-11 → 2026-08-28 ≈ 660 trading days available in an as-revised history.
- **What would resolve it:** Cross-repo: ETFExperiment REGISTRATION.md Section 0/9 and Amendments 3–6 — was an as-revised source considered and rejected, and on what measured revision size? If not measured, the closure rests on an untested assumption that revisions are material.
- **Confidence:** LOW — the alternative sources are from my own knowledge, not from any file in this repository, and the design may have rejected them for a registered reason I cannot read here.
- **Invalidated by later commits?:** no — no later commits here.
- **Disclosed by authors?:** no — the note names no alternative source and states the record "does not exist in any free archive" without qualifying that this is the as-printed record only; the as-printed requirement is stated (docs:101-102) but not its cost.

### DRAFT-all-6
- **Repository / SHA:** retail-power-limits / dda39b2f148569a6fe9be956a979471b2330611d
- **Hypothesis or artifact:** solattn (contrast case) — the "powered null / measured what it set out to measure" characterisation against a registered horizon the note's own registry says was never analysed.
- **Direction:** A
- **Class:** INTERNAL_INCONSISTENCY
- **Severity:** S3
- **Label:** READ
- **Claim challenged (verbatim quote):** "That is what a closure looks like when detectability is not the binding term: the design measured what it set out to measure, at full coverage, and the answer was no." — retail-power-limits/docs/the-power-limit.md:300-302
- **Evidence:** The repository's own source registry describes the solattn registration citation as "Amendment 7, which records the Stage B readout and the horizon never analysed" (SOURCES.md:234; rplimits/sources.py:186-192). The note's body never mentions that horizon; its figures are scoped to "every analysed cohort" (docs:296; SOURCES.md:180) and "all 120 computable cells" (docs:296-297). A design with a registered horizon that was never analysed did not, in full, "measure what it set out to measure". The contrast case is load-bearing: it is the note's chief evidence that the operator's method is not itself the constraint (docs:398-401). Whether the un-analysed horizon was dropped under a registered rule (e.g. kill criterion K1 firing first) is not stated here.
- **Recomputation (if any):** none.
- **What would resolve it:** Cross-repo: solattn REGISTRATION.md Amendment 7 — which horizon, why it was not analysed, and whether the registration made K1's firing sufficient to skip it. If so, the note should say so beside the "measured what it set out to measure" sentence.
- **Confidence:** LOW — the tension is between two sentences in this repository; its weight depends entirely on what Amendment 7 says.
- **Invalidated by later commits?:** no — no later commits here; solattn is anchored at the same b3f5062 the note cites.
- **Disclosed by authors?:** partially (SOURCES.md:234 names the un-analysed horizon; docs/the-power-limit.md:296 scopes the kill criterion to "every analysed cohort") — but the body sentence at 300-302 is unqualified.

### DRAFT-all-7
- **Repository / SHA:** retail-power-limits / dda39b2f148569a6fe9be956a979471b2330611d
- **Hypothesis or artifact:** The note's own reopen condition — "What would change the conclusion".
- **Direction:** A
- **Class:** INTERNAL_INCONSISTENCY
- **Severity:** S3
- **Label:** READ
- **Claim challenged (verbatim quote):** "Not a better estimator on the same samples. The four designs were not badly built; all four ran their pipelines against mutation-tested guards, and the arithmetic that closed them is the arithmetic that would close a better model just as fast." — retail-power-limits/docs/the-power-limit.md:363-366
- **Evidence:** The same section's third bullet says the opposite for one of the four: "InsiderExperiment is the clearest instance: its verdict turned entirely on tracking error, and its own equal-weighted secondary on the identical names would have landed at 34.29 bp instead of 49.35 ... the denominator is often the cheaper term to attack" (docs/the-power-limit.md:386-391). A 30 % lower MDE on the identical sample from a different weighting is a better estimator on the same sample. DRAFT-all-1 shows the same for HFExperiment (a fixed-N test on the same forward series is ≈3.4× shorter than the frozen confidence sequence), and DRAFT-all-3 for NPDExperiment (one-session scoring of the same stored rankings: 0.0512 → ≈0.0285). The reopen condition as written ("a domain whose effects are large relative to achievable samples, not a better estimator on the same ones", docs:370-371; README.md:48-49) excludes the route the note's own evidence says is cheapest.
- **Recomputation (if any):** 34.29/49.35 = 0.695 (inputs docs:388-389). Implied tracking error of the equal-weight book = 34.29/2/21·√2869.9·√252 = 6.94 % vs 9.993 % value-weighted (inputs SOURCES.md:74,78; convention t=2 reproduced in the "checked" section below).
- **What would resolve it:** Reword the reopen condition to include estimator/denominator changes on the same samples, or state why a 30 % MDE reduction does not count.
- **Confidence:** HIGH — both statements are in the same section of the same document.
- **Invalidated by later commits?:** no.
- **Disclosed by authors?:** partially — the counter-example is the note's own (docs:386-391); the contradiction with line 363 is not acknowledged.

### DRAFT-all-8
- **Repository / SHA:** retail-power-limits / dda39b2f148569a6fe9be956a979471b2330611d
- **Hypothesis or artifact:** The headline claim that each of the four closed at one of three power labels.
- **Direction:** A
- **Class:** INTERNAL_INCONSISTENCY
- **Severity:** S4
- **Label:** READ
- **Claim challenged (verbatim quote):** "Each closed at *unresolved at achievable power*, at *untestable at achievable power*, or *BLOCKED* on a power gate — never on a measured null." — retail-power-limits/README.md:5-7 (same sentence at docs/the-power-limit.md:15-16)
- **Evidence:** The note's own correction 3: "HFExperiment did not fire a power gate. It is a power case by inheritance. Its own Section 0 fired BLOCKED on the *broker* ... and the repository then closed by operator decision on 2026-08-26" (docs/the-power-limit.md:141-146; SOURCES.md:154; DECISIONS.md:125-128). ADR-004 says "A reader must not come away thinking four power gates fired" (DECISIONS.md:140), yet the first paragraph of the README says exactly that, and the README carries no correction. HFExperiment's own closure is "BLOCKED on the broker + operator decision", which is none of the three listed labels.
- **Recomputation (if any):** none.
- **What would resolve it:** Amend the README/note lead sentence to "three closed at ... and the fourth inherits its power resolution", as ADR-004 already requires of the case record.
- **Confidence:** HIGH — verbatim contradiction within the repository.
- **Invalidated by later commits?:** no.
- **Disclosed by authors?:** yes (docs/the-power-limit.md:141-146; DECISIONS.md:121-149) — disclosed in the body and the ADR, not in the README sentence a first reader sees.

### DRAFT-all-9
- **Repository / SHA:** retail-power-limits / dda39b2f148569a6fe9be956a979471b2330611d
- **Hypothesis or artifact:** HFExperiment / AiTrader width table — the 5-name vs 50-name z comparison.
- **Direction:** A
- **Class:** ARITHMETIC
- **Severity:** S4
- **Label:** READ
- **Claim challenged (verbatim quote):** "Widening 5 names to 50 halves tracking error (66.4 to 31.7 percent) and cuts excess proportionally (27.99 to 10.04 bp per day), so z moves only 1.668 to 1.455 and neither width clears." — retail-power-limits/SOURCES.md:134 (rplimits/cases.py:259-261)
- **Evidence:** The three quoted ratios are not mutually consistent under z = mean/(sd/√N) on a common holdout: excess falls to 10.04/27.99 = 0.359 while tracking error falls to 31.7/66.4 = 0.477 — not "proportionally" — so z should move to 1.668 × 0.359/0.477 = 1.25, not 1.455. For 1.455 to hold with excess 10.04, the 50-name tracking error would have to be ≈27.3 %, or with TE 31.7 % the excess ≈11.65 bp/day. The conclusion ("neither width clears" 2.50) is unchanged under either figure.
- **Recomputation (if any):** 1.668 × (10.04/27.99)/(31.7/66.4) = 1.253 (inputs SOURCES.md:134). Script §3.
- **What would resolve it:** Cross-repo: AiTrader RETURN.md @ f819b68 — the width table's actual z for 50 names and how its SE is computed (realised daily sd over a possibly different N).
- **Confidence:** MEDIUM — the inconsistency is arithmetic on the quoted figures; the source may define z differently.
- **Invalidated by later commits?:** no.
- **Disclosed by authors?:** no.

### DRAFT-all-10
- **Repository / SHA:** retail-power-limits / dda39b2f148569a6fe9be956a979471b2330611d
- **Hypothesis or artifact:** progress.md build record.
- **Direction:** A
- **Class:** STALE_FIGURE
- **Severity:** S4
- **Label:** DERIVED
- **Claim challenged (verbatim quote):** "`tests/`, 111 tests: source-registry integrity, case integrity, drift between prose and data, the honesty pins, and a credential scan." — retail-power-limits/progress.md:59-60; and "mypy strict clean over 11 source files, 111 tests passing." — retail-power-limits/progress.md:68
- **Evidence:** Counting the anchored test files: test_sources.py 3×24 sources + 2 = 74; test_cases.py 19; test_render.py 2 + 4 blocks + 3 = 9; test_honesty.py 10 (2+2 parametrised, 6 plain) = 112. The commit dda39b2 message says "112 tests" and its diff adds `test_the_credential_scan_has_something_to_scan` to test_honesty.py while leaving progress.md:59 and :68 at 111 (git -C live diff 0974f96 dda39b2 -- progress.md shows only the defects section changed). pytest is not installed in the audit venv, so the count is by enumeration of parametrisations from the data (24 sources, 7 cases, 4 generated blocks), not by collection.
- **Recomputation (if any):** scratchpad/work/agentA-rpl/recompute.py §0: 74 + 19 + 9 + 10 = 112 at dda39b2; 111 at 0974f96.
- **What would resolve it:** Update progress.md to 112, or note the count is as of 0974f96.
- **Confidence:** HIGH — enumeration plus the commit message agree.
- **Invalidated by later commits?:** no — dda39b2 is the anchored HEAD.
- **Disclosed by authors?:** no.

### DRAFT-all-11
- **Repository / SHA:** retail-power-limits / dda39b2f148569a6fe9be956a979471b2330611d
- **Hypothesis or artifact:** The note's subtitle date range.
- **Direction:** A
- **Class:** INTERNAL_INCONSISTENCY
- **Severity:** S4
- **Label:** READ
- **Claim challenged (verbatim quote):** "Four pre-registered experiments, closed between 2026-07-26 and 2026-08-28, that ended on detectability rather than on a measured null." — retail-power-limits/docs/the-power-limit.md:3-5
- **Evidence:** The four closure dates the repository records are 2026-08-25 (NPD, cases.py:83), 2026-08-25 (Insider, cases.py:133), 2026-08-28 (ETF, cases.py:188) and 2026-08-26 (HF, cases.py:243). 2026-07-26 is the AiTrader round (SOURCES.md:213), which is not one of the four pre-registered experiments; HFExperiment's own README is dated 2026-08-23 and its registration 2026-08-25 (SOURCES.md:218-221), so it did not exist on 2026-07-26. The four actually closed within four days (2026-08-25 to 2026-08-28). Related: HF's recorded closure date 2026-08-26 (cases.py:243) sits one day after its cited terminal-closure commit f13e1d3 dated 2026-08-25 (sources.py:151-156) — possibly a timezone artefact, not checked.
- **Recomputation (if any):** none.
- **What would resolve it:** Change the subtitle to "resolved between 2026-07-26 and 2026-08-28" (if the AiTrader round is meant) or "closed between 2026-08-25 and 2026-08-28".
- **Confidence:** HIGH — dates are all in this repository.
- **Invalidated by later commits?:** no.
- **Disclosed by authors?:** no.

---

## What I checked and found sound

- **InsiderExperiment's 49.35 bp/month MDE reproduces exactly from the note's primitives.** Tracking error 9.993 % (SOURCES.md:78) → daily sd 62.95 bp; N_eff 2,869.9 (SOURCES.md:74) → SE of the daily mean 1.175 bp; × 21 sessions = 24.68 bp/month; 49.35/24.68 = 1.9999, i.e. MDE = 2·SE (Section 0's `t·M·sd/√N_eff` with t = 2, M = 21). Under that convention the design's one-sided 5 % power at the band top of 40 bp is 49 %, at 34.7 bp (net top) 41 %, at 30 bp 33 %. The BLOCKED floor of 40 fires when power at the top of the band is below one half — a defensible bar, committed before the measurement (docs:218-225). Label matches evidence. (Script §2.)
- **The equal-weight secondary was correctly not promoted for the registered verdict.** 34.29 bp sits inside the gross band 30–40 and just under the net top 34.7 (docs:227-232); DEGRADED, not GO. The note records the temptation and the disclosure a future equal-weight registration would owe (docs:230-232). Reopen path exists (ADR-011, SOURCES.md:223) — recorded in the ledger, not a finding.
- **ETFExperiment's closure figures are internally consistent.** 11 + 20.8 × 7.06 months = 158 ≈ 163; 11 + 20.8 × 14.09 = 304 ≈ 302; 300 − 163 = 137; 237 − 163 = 74; 11/333 = 3.30 % (SOURCES.md:102-110). Under the registered 0.09 assumption the closure is sound (≈40–57 months of accrual).
- **HFExperiment's inherited figures are consistent with each other.** 0.664/√252 = 418 bp/day; 27.99 × 252 = 70.5 %/yr; 90.3 − 19.7 = 70.6; 2.50/1.668 = 1.50 ≈ 104.0/70.5 = 1.48 (compounding); z at 27.99 over 643 days = 1.70 ≈ 1.668; 2,061/252 = 8.2 y, 2,852/252 = 11.3 y — "eight to eleven years" is a correct reading of the CS figures (the finding is about attribution, not arithmetic). The label "resolved on statistical power, not absent signal" (SOURCES.md:150) is the right label for a point estimate on the hypothesis side with interval −4.9 to +60.9 (SOURCES.md:134); the note does not call it signal-absent.
- **NPDExperiment's derived and quoted figures check.** 22+34+68+52+194+41 = 411 (SOURCES.md:294-298; ADR-006); 427/3.4 = 125.6; 1 − 1/3.4 = 70.6 % ("lost 70 percent", docs:379); 404 × 4 ≈ 1,616 ("near 1,700" for MDE ≈ 0.0256); the 13:26:58 → 18:34:56 gap is 5 h 08 m and → 23:24:15 is 9 h 57 m (docs:211-216).
- **The refusal to promote NPD's secondary *after* the result** (the voided post-hoc amendment, docs:249-252) is correct protocol; DRAFT-all-3 concerns the pre-collection decision and the never-run zero-cost variant, not the post-hoc void.
- **MLCryptoEngine contrast arithmetic.** 50/0.0291 = 1,718 ("roughly 1,700x"); 3/0.0291 = 103 ("roughly 100x"); correction 4 (ADR-003 item 4) is right and the cost-bound/signal-absent split with its reopen field is faithfully carried (docs:280-293; SOURCES.md:172-176).
- **solclear's underpowered rule is a registered pre-commitment and honouring it is protocol.** For the record, the arithmetic runs the other way from the Direction-A thesis: 0 of 18 pools ever above entry gives P = 2⁻¹⁸ = 3.8 × 10⁻⁶ under p = 0.5 and an exact 95 % upper bound on p of 15.3 % (SOURCES.md:196); the n = 18 sample is decisive against the positive hypothesis, so "no significance claimed in either direction" understates a negative rather than closing a live hypothesis early. Not a Direction-A finding; noted so the cross-repo pass does not re-derive it. 4,695,489/124,764 = 37.6 ✓.
- **solattn's interval** [−3.3354, +0.0204] on n = 12,798 (SOURCES.md:184) does include zero; the note reports it verbatim and does not call it significant; "powered null" is carried on the 120/120 negative cells and full coverage. Sound as stated, subject to DRAFT-all-6.
- **The honesty tests do what they say** (tests/test_honesty.py:53-159): the scope sentence and headline figures are pinned in both documents, four overclaiming phrasings are forbidden, and each detector has a canary. Drift tests re-render all four generated blocks (test_render.py:19-37) and the blocks in SOURCES.md and the note are current against cases.py at the anchor (verified by reading; the renderer output matches the block text line-for-line).
- **Source registry is complete and well-formed**: 24 sources, every Figure key resolves, every commit a 7-hex short hash, all seven repositories represented (test_sources.py; verified by import in scratchpad/work/agentA-rpl/recompute.py §0).
- **Live repository provenance.** Three commits, all 2026-08-29 00:19–00:21 -07:00; HEAD = dda39b2 = origin/main; remote https://github.com/kirosli00tuff/retail-power-limits.git — consistent with progress.md:113-116 (this note is public; the four power-case siblings are said not to be). No untracked files; only ignored caches and .venv in the working tree.
- **What I would have expected to find if the thesis held strongly and did not:** a case where the note's own deciding number sits inside the effect band while the label says outside (none: 0.0512 > 0.05, 49.35 > 40, 163 < 300, 1.668 < 2.50 all hold as stated); a blocker stated in an early file and lifted in a later dated entry of this repository (none: the repository has a single dated day of entries); a reopen condition met by a later entry here (none: nothing postdates 2026-08-29).

## Cross-repo items for the orchestrator (not verified here, by lane)

1. Whether NPDExperiment, InsiderExperiment, ETFExperiment or HFExperiment now has a remote (progress.md:113-116; SOURCES.md:262-275; docs:44-52 say "no remote" as of 2026-08-29 push time). If any is now public, the note's "A reader should discount the four accordingly" (docs:51-52) is a stated blocker that has expired.
2. NPDExperiment: realized point contrast and interval at B.2; MDE convention (Section 9); registered power of the one-session secondary (ADR-007) — DRAFT-all-2, -3.
3. ETFExperiment: Amendment 5 / ADR-019 reopen path; whether the registered deadline may be extended; whether an as-revised source was considered — DRAFT-all-4, -5.
4. HFExperiment: Section 11 confidence-sequence family and α; whether a fixed-horizon alternative was registered — DRAFT-all-1.
5. AiTrader RETURN.md width table: z for 50 names and its SE definition — DRAFT-all-9.
6. solattn Amendment 7: the un-analysed horizon and why — DRAFT-all-6.
7. InsiderExperiment ADR-011 reopening boundary: its text is not carried here; the ledger records only that it exists.

## Live-repo access log

Live repository touched: /home/kiros-li/Documents/GitHub/retail-power-limits, read-only (`git status --porcelain`, `rev-parse`, `branch --format`, `remote -v`, `log`, `ls-files --others`, `diff <a> <b>`). No other live repository was opened.

Before (UTC 2026-09-03T00:35:19Z), `git -C /home/kiros-li/Documents/GitHub/retail-power-limits status --porcelain`:
```
(empty)
```
After (UTC 2026-09-03T00:48:29Z), `git -C /home/kiros-li/Documents/GitHub/retail-power-limits status --porcelain`:
```
(empty)
```
Both outputs empty: no pre-existing dirt and nothing changed by this audit. No file under the live repository was opened for writing.
