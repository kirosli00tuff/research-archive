# InsiderExperiment — Agent A findings (Direction A: closed too early or too hard)

Repository `InsiderExperiment`, anchored SHA `12d9fd36cf055cb10ea67a3fc737e404217bc95a` (master, 2026-08-25).
Agent A, consolidated from the `_drafts/InsiderExperiment/all.md` pass. 7 findings: one S2, three S3, three S4.

## Summary — the strongest case for the thesis in this repository

InsiderExperiment closed a hypothesis without ever testing it, on one number: a minimum detectable effect of
49.35 bp per month against a BLOCKED bar of 40 (n = 2,581 sessions). The arithmetic is right — I reproduced all
four series and the full Newey-West grid from the centered store to four decimals. The Direction A case is about
what that number was computed on and what it was compared against. The bar rests on an uncited 30-to-40 bp
"decayed gross band" while the closure sentence borrows the authority of "the range the literature reports"; the
registered value-weighted primary was never run (a median-dollar-volume proxy was, with a bias the authors
themselves stated as pointing toward BLOCKED); the registered Stage B inference, the Carhart residual, was never
measured because measuring it would be "choosing a method by its answer", though the store the power path reads
is already centered and makes the residual SD obtainable without ever producing an intercept; and on the identical
names the registered equal-weighted secondary fired DEGRADED at 34.29 and was refused promotion on that same
ground — a ground the registration's own Section 0.1 contradicts, since it defines the answer as a first moment
and 34.29 is a second. Three refusals, one root: a rule against seeing the answer, applied to numbers this design
defines as safe to see and to fire on.

---

### AUDIT-A-InsiderExperiment-1
- **Repository / anchored SHA:** InsiderExperiment / `12d9fd36cf055cb10ea67a3fc737e404217bc95a`
- **Hypothesis or artifact concerned:** Section 1 hypothesis (net-of-cost survival of Form 4 opportunistic and cluster purchases in the liquid-500 universe); the closure decision "Stage B is never written" and the ADR-011 reopening boundary, as they treat the registered equal-weighted secondary (MDE 34.29 bp per month, DEGRADED).
- **Direction:** A
- **Class:** INTERNAL_INCONSISTENCY
- **Severity:** S2 — a label ("selecting by its answer") contradicts its own evidence, and a permanent no-amendment clause rests on it.
- **Label:** READ — the contradiction is entirely between two passages of the same registration; the code and data citations below only confirm what the document already asserts.
- **Claim challenged (verbatim, file:line):**
  > "Promoting it now would be selecting a weighting scheme after seeing which one survived, which is the exact move Section 1's governing rule forbids."
  — InsiderExperiment/REGISTRATION.md:766-767. Same ground: "promoting it now would be selecting a weighting scheme by its answer." — InsiderExperiment/DECISIONS.md:325-326. Consequence: "None in force. Section 0 fired BLOCKED, so no amendment can authorize Stage B." — InsiderExperiment/REGISTRATION.md:800.
- **Evidence (figures with n, file:line):**
  - The registration's own load-bearing separation says a second moment is not the answer: "The separation that makes an earlier answer possible: alpha is a first moment, detectability is a second moment." (REGISTRATION.md:29-30); "Two gates fire in Stage A.1. Neither reads a first moment." (REGISTRATION.md:15); "**It is not a null on the hypothesis.** No abnormal return was computed." (REGISTRATION.md:771). The equal-weighted MDE was produced by the same power path from the centered store (src/insider/power/dispersion.py:65-78, :163-192; src/insider/power/mde.py:53-67), which by construction carries no first moment (src/insider/portfolio/returns.py:292-301). The alpha of either book remains sealed and unread (REGISTRATION.md:772-773). What was seen when the secondary was declined is a detectability figure, which this design defines as safe to see and to fire on.
  - Deciding figures, with n. Primary 126-session dollar-volume-weighted book: MDE 49.35 bp/month, n = 2,581 sessions, VIF 0.8993, N_eff 2,869.9, TE 9.9933%, SE 24.6771 bp (REGISTRATION.md:712, :717-719; reports/stage_a1/power.json:6-12). Equal-weighted secondary on the identical names: MDE 34.29 bp/month, n = 2,581 sessions, VIF 0.9224, N_eff 2,798.1, TE 6.8556%, SE 17.1449 bp (REGISTRATION.md:715; reports/stage_a1/power.json:69-75). Bar: DEGRADED is 20 to 40 bp and authorizes Stage B once the V2 sentence is on record (REGISTRATION.md:42, :442); that sentence is already on record, written before the gate fired (REGISTRATION.md:438).
  - The registered purpose of the primary weighting was diversification, not the weighting scheme as such: "**Value-weighted primary. Equal-weighted secondary.** … Wide book, not concentrated. Concentrated books are what killed H-F at 42 to 66 percent tracking error" (REGISTRATION.md:387-391). The authors record that the primary violated that purpose and the secondary met it: "The primary chosen to avoid concentration was concentrated by its weighting rather than by its name count." (REGISTRATION.md:862-863; DECISIONS.md:340-343); effective names 29.73 versus 66.93 (reports/stage_a1/portfolio.json:27, :111).
  - The registration supplies its own instrument for revisiting a registered value on evidence: "Changing a registered value after that commit requires a numbered amendment in Section 17 carrying its own evidence." (REGISTRATION.md:8-9). Section 16 forecloses it categorically (REGISTRATION.md:800) and ADR-010 states "**What would overturn it.** Nothing inside this repository." (DECISIONS.md:308). The evidence such an amendment would carry — 34.29, a second moment — is exactly the kind of evidence Section 0 was built to act on (DECISIONS.md:20-22).
  - Honest limits, stated because they are load-bearing against my own case. DEGRADED is not GO. At the equal-weighted SE of 17.1449 bp the design's power against the decayed gross band is 40% at 30 bp and 63% at 40 bp, and 51% at 34.7 bp, the top of the net band (recomputation below). The equal-weighted book also changes the replication target: Cohen-Malloy-Pomorski's 82 bp headline is value-weighted (REGISTRATION.md:49-50). ADR-011 does leave a disclosed path open in a successor repository with a higher bar (DECISIONS.md:328-333). The finding is narrower than "promote the secondary": it is that the stated ground for refusal, selection "by its answer", is contradicted by the document's own definition of the answer, and that the permanent no-amendment clause rests on that ground.
  - Related: findings -3 and -4 attack two further refusals resting on the same root ("choosing a method by its answer", REGISTRATION.md:793-794). They are separate findings with separate quotes, evidence and resolutions; they should not be double-counted as three instances of one error, nor collapsed into one.
- **Recomputation:** Power at t = 2.0 (one-sided normal approximation) from SE 17.1449 bp (power.json:74): effect 13.3 bp → 0.110; 20 → 0.202; 30 → 0.401; 34.7 → 0.510; 40 → 0.630. Primary at SE 24.6771 bp (power.json:11): 30 → 0.216; 40 → 0.352; 49.35 → 0.500. Both MDE figures independently reproduced from `var/insider_dispersion.db` (live repo, untracked, UNANCHORED, read 2026-09-03T06:32:44Z): 126/equal_weighted lag 21 → 34.2897; 126/value_weighted lag 21 → 49.3543. Scratch: `scratchpad/work/agentA/InsiderExperiment/recompute_mde.py` (+ `.out`).
- **What would resolve it:** Either a numbered amendment under REGISTRATION.md:8-9 promoting the equal-weighted book on the recorded second-moment evidence with the provenance ADR-011 demands, or a successor Section 0 that does the same; then read the alpha once under the DEGRADED gate with V2 pre-registered. Alternatively, the closure states plainly that it forbids re-selection on power grounds as a matter of policy — not because a result was seen — and drops the "by its answer" ground.
- **Confidence:** MEDIUM — the logical point is clean and entirely inside the document, but reasonable pre-registration practice differs on whether a primary may be re-chosen on power grounds once data are in hand, and DEGRADED remains weak against the net band.
- **Could later commits invalidate this?:** No. Live HEAD equalled the anchored SHA at read time (2026-09-03T06:35:25Z) and the working tree carries an untracked marker declaring the repository closed.
- **Disclosed by the authors?:** Partially, and the part that is disclosed is not the part challenged. REGISTRATION.md:850-874 and DECISIONS.md:314-343 disclose the DEGRADED secondary, the temptation it creates, the irony, and the reopening boundary — all of that is the authors' own and is not presented here as a discovery. What is not disclosed as a limitation is the challenged ground itself: that seeing a second moment counts as seeing "the answer". That is asserted, and the document's own Section 0.1 (REGISTRATION.md:29-30) says the opposite.

### AUDIT-A-InsiderExperiment-2
- **Repository / anchored SHA:** InsiderExperiment / `12d9fd36cf055cb10ea67a3fc737e404217bc95a`
- **Hypothesis or artifact concerned:** Section 0.2 bars. The BLOCKED bar of 40 bp per month sits at the top of a "decayed gross band" of 30 to 40 bp per month that carries no citation, and the verdict language reads the bar as "the range the literature reports".
- **Direction:** A
- **Class:** PROVENANCE
- **Severity:** S3 — the external figure that sets the deciding bar is unsourced, and the closure's strongest sentence borrows the literature's authority for it.
- **Label:** READ — established by grep over the repository's documents and configuration.
- **Claim challenged (verbatim, file:line):**
  > "That replicates at roughly 30 to 40 bp per month on 2008 to 2024 data, a 60 to 70 percent decay."
  — InsiderExperiment/REGISTRATION.md:50-51 (repeated at :182-183). And the verdict row: "| **BLOCKED** | MDE above 40 bp per month | The design cannot detect an effect anywhere in the range the literature reports. Stage B is never written and the repo closes on the finding. |" — InsiderExperiment/REGISTRATION.md:43; restated as "The design cannot resolve any effect the literature reports, gross or net." — InsiderExperiment/REGISTRATION.md:738 and reports/stage_a1/power.json:135.
- **Evidence (figures with n, file:line):**
  - The band is the deciding external figure: "The 40 bp BLOCKED bar sits at the top of it, so a design above 40 bp cannot resolve any part of the band." (REGISTRATION.md:58-59); `decayed_gross_band_bp=(30.0, 40.0)` (src/insider/config.py:152); `mde_degraded_ceiling_bp=40.0` (src/insider/config.py:144).
  - Grep of the whole repository finds no author, year, sample, weighting or venue for the 2008-2024 replication. All n = 8 occurrences of the band: REGISTRATION.md:50, :182, :420, :735, :814; DECISIONS.md:290; progress.md:16, :177; plus config.py:152. None carries a citation.
  - The only cited magnitudes are Cohen-Malloy-Pomorski's 82 bp per month value-weighted on opportunistic purchases, 1989-2007 (REGISTRATION.md:49-50), and Ozlen-Batumoglu's 70 to 80 percent transaction-day-to-next-day dissipation (REGISTRATION.md:51-55) — a statement about a window before the filing posts, which does not by itself yield a monthly figure. The SSRN reference (5966834) could not be verified at read time (HTTP 403).
  - An MDE at t = 2.0 is the effect at which power is 50%, not the effect below which detection is impossible. Against the one cited literature magnitude the registered design is well powered (recomputation, n = 2,581 sessions). The closure sentence "cannot detect an effect anywhere in the range the literature reports" is true only against the uncited band, not against the cited figure.
- **Recomputation:** Primary SE 24.6771 bp per month (power.json:11), n = 2,581 sessions. Power at t = 2.0 (one-sided normal): effect 82 bp → 0.907; 60 → 0.667; 49.35 → 0.500; 40 → 0.352; 34.7 → 0.276; 30 → 0.216; 13.3 → 0.072. So the registered design detects the cited Cohen-Malloy-Pomorski magnitude with 91% power and the top of the uncited band with 35%. Scratch: `recompute_mde.out`.
- **What would resolve it:** Cite the 2008-2024 replication(s) behind 30 to 40 bp (author, year, sample, weighting, universe). If no such published replication exists, the bar rests on the assistant's estimate, and the closure language should read "the range this registration assumed" rather than "the range the literature reports". Report the power curve beside the MDE in Section 15.5 either way.
- **Confidence:** MEDIUM — the absence of any citation is certain; I do not claim the band is wrong, only that the closure's strongest sentence borrows the literature's authority for an uncited number.
- **Could later commits invalidate this?:** No. HEAD equalled the anchored SHA at read time.
- **Disclosed by the authors?:** No. The band is stated as fact in the same paragraph that cites Cohen-Malloy-Pomorski and Ozlen-Batumoglu by name, which is what makes it read as sourced.

### AUDIT-A-InsiderExperiment-3
- **Repository / anchored SHA:** InsiderExperiment / `12d9fd36cf055cb10ea67a3fc737e404217bc95a`
- **Hypothesis or artifact concerned:** Section 14.3 / ADR-001. The power gate fired on raw excess-return dispersion against the dollar-volume-weighted universe, not on the residual dispersion of the registered Stage B inference (Carhart four-factor alpha), and the document says the latter "will not [be] measure[d]" for a reason that does not hold on the store the power path actually reads.
- **Direction:** A
- **Class:** OVER_CLOSED
- **Severity:** S3 — capped at S3 because the underlying conservatism is disclosed (see below); the undisclosed part is that the quantity was measurable.
- **Label:** READ — the challenged reason is a documentary assertion; the code citations show which store the power path reads, but the claim stands on the document.
- **Claim challenged (verbatim, file:line):**
  > "the residual MDE would be lower than 49.35 by an amount this stage did not measure and will not measure, because measuring it after seeing BLOCKED is choosing a method by its answer."
  — InsiderExperiment/REGISTRATION.md:792-794. Supporting premise: "The Stage A.1 number is measured against the universe benchmark rather than the Carhart residual, because a factor regression on uncentered data produces an intercept and the intercept is the alpha." — InsiderExperiment/DECISIONS.md:29-31.
- **Evidence (figures with n, file:line):**
  - Carhart is not a method chosen after the answer; it is the registered inference. "Carhart four-factor alpha on the resulting daily series, in Stage B." (REGISTRATION.md:336-337); "Stage B replaces this with the Carhart four-factor residual." (REGISTRATION.md:353-354); primary contrast at :467-468. It was committed in `398755b` at 2026-08-25T18:38:50-07:00, before the corpus (`ccc9b13`, 18:47:16) and before the power gate (`cb17046`, 19:11:45) — git log, live repo, read-only.
  - The stated obstacle does not apply to the store the power path reads. The dispersion store holds the series already centered on its own mean (src/insider/portfolio/returns.py:292-301; src/insider/power/dispersion.py:39-62, where `CenteredSeries` refuses an uncentered series). Regressing a centered series on centered factor returns without an intercept yields the same residuals as the intercept regression on raw data (Frisch-Waugh-Lovell); the residual standard deviation, which is the only dispersion the MDE consumes (src/insider/power/mde.py:50, :66), is therefore obtainable without ever producing the intercept. The seal is not breached.
  - The authors identify this as the one unmeasured conservatism that matters: "The Section 14.3 conservatism is the only one large enough to matter. A Carhart regression would absorb the persistent size tilt between a mid-cap book and a mega-cap-weighted benchmark" (REGISTRATION.md:790-792). The benchmark is itself concentrated — top-1 weight 7.02%, top-5 19.84% (portfolio.json:25-26) — so part of the measured "tracking error" is the benchmark's own idiosyncratic variance, which a diversified market factor would not carry.
  - Daily Fama-French three factors and the momentum factor are published free by the Kenneth R. French Data Library (no API, no fee). They are not an SEC source, so use would need a registered note against CLAUDE.md:61 ("SEC access only. Zero paid APIs."), not a new budget.
- **Recomputation:** Beta-only adjustment from reported diagnostics (portfolio.json:20-22: sd_portfolio 0.014065, sd_benchmark 0.014575, corr 0.903981), n = 2,581 sessions. Excess sd = sqrt(sp² + sb² − 2ρ·sp·sb) = 62.95 bp, matching power.json:9. Residual sd after a single beta = sp·sqrt(1 − ρ²) = 60.14 bp. MDE_beta = 2 × 21 × 60.14 bp / sqrt(2,869.9) = 47.15 bp per month (N_eff held at power.json:8). So beta alone explains 8.7% of excess variance and leaves the verdict at BLOCKED. To reach DEGRADED the factor residual must be ≤ 51.02 bp daily (TE 8.10%), so size, value and momentum together would need to explain a further ~25.6 percentage points (34.3% cumulative) of excess-return variance. That is plausible for a mid-cap-tilted book against a mega-volume benchmark and is measured nowhere in the record. Scratch: `recompute_mde.out`.
- **What would resolve it:** Regress the centered primary series (and the centered equal-weighted series) on centered daily Carhart factors with no intercept; report residual SD, VIF at the registered lag 21, and the resulting MDE beside 49.35 and 34.29. This is a second-moment computation the existing guards permit. If the primary residual MDE lands at or below 40, the gate applied to the registered inference fires DEGRADED, not BLOCKED.
- **Confidence:** MEDIUM — that the residual dispersion is computable without the first moment is certain; whether it crosses 40 is unknown, and the beta-only step does not.
- **Could later commits invalidate this?:** No. HEAD equalled the anchored SHA at read time.
- **Disclosed by the authors?:** Yes, in part, and severity is capped at S3 for that reason. The authors disclose the conservatism at REGISTRATION.md:578-583 ("The gate can therefore fire BLOCKED on a design Stage B would have found marginally better"), at :785-796, and at DECISIONS.md:29-32. That disclosure is theirs and is not claimed here as a discovery. What is not disclosed — and what this finding rests on — is that the residual MDE was measurable from the already-centered store without producing an intercept; the document asserts the contrary at DECISIONS.md:29-31.

### AUDIT-A-InsiderExperiment-4
- **Repository / anchored SHA:** InsiderExperiment / `12d9fd36cf055cb10ea67a3fc737e404217bc95a`
- **Hypothesis or artifact concerned:** The Section 0 power gate, primary series. The registered primary weighting (value-weighted, Section 7) was never run; a median-dollar-volume proxy was run in its place, with a direction of error the authors themselves stated ex ante as pointing toward BLOCKED. The closure then attributes the failure to "the registered primary".
- **Direction:** A
- **Class:** OVER_CLOSED
- **Severity:** S3 — capped at S3 because the substitution is disclosed as a registered deviation (see below).
- **Label:** READ — the substitution and its stated direction are documentary; the code confirms no market-capitalization weighting exists, which corroborates rather than carries the finding.
- **Claim challenged (verbatim, file:line):**
  > "**Weight concentration in the registered primary.**"
  — InsiderExperiment/REGISTRATION.md:837. And: "The value-weighted book is concentrated by construction, and value-weighted was registered as primary before any number was visible." — InsiderExperiment/REGISTRATION.md:759-761.
- **Evidence (figures with n, file:line):**
  - What was registered: "**Value-weighted primary.**" (REGISTRATION.md:387), replicating Cohen-Malloy-Pomorski's value-weighted figure (REGISTRATION.md:49-50). What was run: "value weighting is implemented as point-in-time median dollar volume from the formation window" (REGISTRATION.md:393-395; Section 14.2 at :566-576). Code: `primary_weighting="value_weighted"` (src/insider/config.py:136); weights are `members.get(n, 0.0)` (src/insider/portfolio/returns.py:102-103) where `members_at` returns `median_dollar_volume` (src/insider/market/store.py:100-108). No market-capitalization weight exists anywhere in the source.
  - The authors stated the proxy's bias before measurement: "It is more dispersed than market capitalization, so the book is slightly less concentrated and the tracking error slightly higher, which moves the minimum detectable effect toward BLOCKED rather than away from it." (REGISTRATION.md:574-576); "The substitution cannot flatter the design." (DECISIONS.md:222). For a gate whose BLOCKED outcome is terminal — "Stage B is never written and the repo closes on the finding" (REGISTRATION.md:43) — a substitution biased toward BLOCKED is the opposite of conservative with respect to the closure decision.
  - The ex-ante direction sentence is internally contradictory, and the measurement resolved it against the "slightly": "more dispersed … so the book is slightly less concentrated and the tracking error slightly higher" (REGISTRATION.md:574-575; DECISIONS.md:220-221) — a less concentrated book has lower, not higher, idiosyncratic tracking error. Measured, n = 2,581 sessions: the 71.909-name book behaves like 29.73 effective names, top-1 weight 14.93%, top-5 33.79% (portfolio.json:7, :23-24, :27; REGISTRATION.md:749, :752-754: "Median dollar volume is heavily skewed, so weighting by it collapses a 72-name book into one that behaves like 30").
  - The route to the registered basis was named and not taken: `dei:EntityCommonStockSharesOutstanding` "was verified working" and was rejected because `company_tickers.json` "lists only current registrants" (21 of 25 sampled issuers present) and shares are not split-adjusted (DECISIONS.md:204-212). A cheaper route exists inside data the corpus already holds: every Form 4 row carries `ISSUERCIK` and `ISSUERTRADINGSYMBOL` (src/insider/corpus/build.py:120, :123), giving a point-in-time symbol-to-CIK map from the filing stream with no survivorship; and the SEC's own DERA Financial Statement Data Sets (free, quarterly since 2009q1; `sub.txt` keyed by adsh and cik, `num.txt` carrying the `EntityCommonStockSharesOutstanding` cover fact) supply shares outstanding by CIK without `company_tickers.json`. Both are SEC sources, inside the CLAUDE.md:61 boundary.
  - Bracketing, n = 2,581 sessions on identical names: the most concentrated registered weighting gives MDE 49.3543 and the least concentrated gives 34.2897 (power.json:12, :75). The BLOCKED bar of 40 lies between them. The registered primary weighting's MDE is unmeasured, and the closure attributes the failure to "the registered primary" (REGISTRATION.md:837, :759-761, :860-863; DECISIONS.md:296-298) when the concentration is a property of the proxy that stood in for it.
- **Recomputation:** Inputs TE 9.9933% and MDE 49.3543 (power.json:10, :12); TE 6.8556% and MDE 34.2897 (power.json:73, :75); bar 40 (config.py:144). MDE scales linearly with TE at fixed N_eff (mde.py:50, :66), so the primary reaches DEGRADED at TE ≤ 8.10% (40/49.35 × 9.9933), a 19% reduction; the equal-weighted book sits at 6.86%. Implied per-name idiosyncratic volatility from TE × sqrt(effective names): 9.9933% × sqrt(29.73) = 54.5% for the proxy book and 6.8556% × sqrt(66.93) = 56.1% for the equal-weighted book, against the 30% planning figure at REGISTRATION.md:107-108. Whether a cap-weighted book lands below 8.10% TE is not determinable from the record; cap weights among the top 500 by dollar volume are also skewed. Scratch: `recompute_mde.out`.
- **What would resolve it:** Build the 126-session book with point-in-time market-capitalization weights via the free route above (Form-4-derived symbol↔CIK map plus DERA FSDS shares outstanding, restricting the cover fact to the quarter of the formation date to handle splits), run the existing power path on it, and report its MDE beside 49.35 and 34.29. If it lands at or below 40, the registered primary as registered fires DEGRADED, not BLOCKED.
- **Confidence:** MEDIUM — the direction of the proxy's bias is the authors' own ex-ante statement and the code confirms no cap weighting was ever run; the magnitude is unmeasured and may well leave the verdict at BLOCKED.
- **Could later commits invalidate this?:** No. HEAD equalled the anchored SHA at read time and the repository is marked closed.
- **Disclosed by the authors?:** Yes, and severity is capped at S3 for that reason. The substitution and its BLOCKED-ward direction are disclosed as a registered deviation at REGISTRATION.md:566-576 and :783-784, and at DECISIONS.md:197-222. That disclosure is the authors' and is not presented here as a discovery. Two things are not disclosed: the self-contradiction inside the direction sentence (less concentrated yet higher tracking error), and the closure's attribution of the concentration to "the registered primary" when the concentration belongs to the proxy.

### AUDIT-A-InsiderExperiment-5
- **Repository / anchored SHA:** InsiderExperiment / `12d9fd36cf055cb10ea67a3fc737e404217bc95a`
- **Hypothesis or artifact concerned:** Section 15.1 qualifying-events-by-year table, and the ADR-005 year figures.
- **Direction:** A
- **Class:** STALE_FIGURE
- **Severity:** S4 — hygiene; the published table was not refreshed after the ADR-013 fix. No verdict depends on it.
- **Label:** READ — the recomputation is arithmetic over numbers printed in two files in the snapshot (a Markdown table and a JSON report). No stored database, code path or git object was read for it.
- **Claim challenged (verbatim, file:line):**
  > "| 2016 | 262 | 2022 | 502 |" … "| 2021 | 297 | | |"
  — InsiderExperiment/REGISTRATION.md:603-608, the by-year table published under "**CORPUS-GO.** 4,585 qualifying events" (REGISTRATION.md:594). And: "the corpus shows 717 qualifying events in 2020 against 297 in 2021" — InsiderExperiment/DECISIONS.md:148-149.
- **Evidence (figures with n, file:line):**
  - The published table (n = 11 year rows) sums to 4,542, not the 4,585 asserted 9 lines above it at REGISTRATION.md:594.
  - reports/stage_a1/corpus.json:4-14 carries 263, 409, 531, 462, 728, 298, 504, 508, 418, 365, 99 — sum 4,585, matching `"qualifying_events": 4585` at corpus.json:2.
  - The 43-event shortfall equals exactly the silent merge that ADR-013 records: "The build reported 4,585 qualifying events while the table held 4,542." (DECISIONS.md:407-408; progress.md:87-88). The Section 15.1 table was written from the merged store and never refreshed after the surrogate-key fix, although ADR-008 states "The qualifying set is unchanged at 4,585" (DECISIONS.md:246-248).
  - A second, smaller instance: REGISTRATION.md:702-704 gives "257 in 2018" unclassifiable where reports/stage_a1/corpus.json:69 gives 256.
- **Recomputation:** Sum of REGISTRATION.md:603-608 = 4,542 (n = 11 rows); sum of corpus.json:4-14 = 4,585 (n = 11 rows); per-year differences 1, 3, 7, 5, 11, 1, 2, 3, 8, 2, 0, totalling 43. Scratch: `verify_tables.py` (+ `.out`).
- **What would resolve it:** Regenerate the Section 15.1 table and the ADR-005 sentence from corpus.json, and correct the 2018 unclassifiable count at REGISTRATION.md:703-704.
- **Confidence:** HIGH — arithmetic on two files in the anchored snapshot, reproducible by anyone with the snapshot.
- **Could later commits invalidate this?:** No. HEAD equalled the anchored SHA at read time.
- **Disclosed by the authors?:** No. ADR-013 discloses the merge and its correction; it does not disclose that the published Section 15.1 table still carries the pre-fix merged counts.

### AUDIT-A-InsiderExperiment-6
- **Repository / anchored SHA:** InsiderExperiment / `12d9fd36cf055cb10ea67a3fc737e404217bc95a`
- **Hypothesis or artifact concerned:** Sections 15.6, 17.3 and 17.4 — the "holds 71.9 names and behaves like N" comparison mixes two different bases.
- **Direction:** A
- **Class:** INTERNAL_INCONSISTENCY
- **Severity:** S4 — hygiene; it overstates the primary's concentration ratio and mislabels an equal-weighted count as a concentration statistic, but does not move the verdict.
- **Label:** DERIVED — established by reading the two code paths that produce the two numbers, then confirmed against both JSON reports.
- **Claim challenged (verbatim, file:line):**
  > "On the identical names, the equal-weighted book holds **71.9 and behaves like 66.9**"
  — InsiderExperiment/REGISTRATION.md:852-853. And: "Both books hold 71.9 names." — InsiderExperiment/REGISTRATION.md:863.
- **Evidence (figures with n, file:line):**
  - 71.909 is the membership mean width *before* the ADR-009 drop (portfolio.json:7, :91), computed by `series.mean_width()` at src/insider/portfolio/build.py:59, over n = 2,581 sessions.
  - Effective names are computed on the *priced* book *after* the drop (src/insider/portfolio/returns.py:189-190, :195, :217), and the priced book averages 66.93 names (power.json:16, :79, from `widths.append(len(priced))` at returns.py:210), same n = 2,581 sessions.
  - For an equal-weighted book the inverse Herfindahl equals the name count, so "behaves like 66.9" is simply the priced width, not a concentration statistic. The equal-weighted book is not behaving like fewer names than it holds; the entire 71.9 → 66.9 gap is the ADR-009 drop of 13,750 name-sessions (power.json:118).
  - For the primary, the like-for-like ratio is 29.73 of 66.93 = 44%, not 29.73 of 71.9 = 41%.
- **Recomputation:** book_effective_names 66.925223 (portfolio.json:111) versus book_width_mean 66.93 (power.json:79) — equal to rounding, as an equal-weighted book requires; 29.731282 / 66.93 = 0.4442; 29.731282 / 71.909 = 0.4134.
- **What would resolve it:** State the priced width (66.9) as the "names held" basis in Sections 15.6, 17.3 and 17.4, and reserve "behaves like" for the value-weighted book, where inverse Herfindahl genuinely differs from the count.
- **Confidence:** HIGH — read directly from the two code paths and both JSON reports in the snapshot.
- **Could later commits invalidate this?:** No. HEAD equalled the anchored SHA at read time.
- **Disclosed by the authors?:** No.

### AUDIT-A-InsiderExperiment-7
- **Repository / anchored SHA:** InsiderExperiment / `12d9fd36cf055cb10ea67a3fc737e404217bc95a`
- **Hypothesis or artifact concerned:** The pre-registration provenance record — progress.md timings and the "committed at 18:34" statements that establish the ordering of Section 0 against the gates.
- **Direction:** A
- **Class:** PROCESS
- **Severity:** S4 — hygiene; the substantive ordering claim survives in both clocks, so nothing about the pre-registration is impeached.
- **Label:** DERIVED — obtained from git objects (commit timestamps) and an untracked ledger file, not from the documents.
- **Claim challenged (verbatim, file:line):**
  > "Timings are wall clock, session start 18:20 UTC, boundaries taken from commit timestamps where one exists."
  — InsiderExperiment/progress.md:193-194. And: "Empty at the time Section 0 was committed at 18:34 on 2026-08-25." — InsiderExperiment/REGISTRATION.md:589-590.
- **Evidence (figures with n, file:line):**
  - The commit timestamps carry a -07:00 offset, n = 5 commits: `fbfc74e` (Section 0) 2026-08-25T18:34:56-07:00 = 2026-08-26T01:34:56Z; `398755b` (Sections 1-16) 18:38:50-07:00; `ccc9b13` (corpus, CORPUS-GO) 18:47:16-07:00; `cb17046` (power gate, BLOCKED) 19:11:45-07:00; `12d9fd3` (closure) 23:24:15-07:00. Source: `git log`, live repo, read-only, read 2026-09-03T06:30:19Z.
  - The untracked evidence ledger `ledgers/evidence.jsonl` (live repo, UNANCHORED, read 2026-09-03T06:35:07Z) records the corpus gate at 2026-08-26T01:42:24+00:00 and the first power gate at 2026-08-26T01:51:14+00:00, with n = 3 power-gate records, all carrying 49.3543 and BLOCKED. The ledger's own UTC stamps agree with the commit clock once the -07:00 offset is applied; the "UTC" label in progress.md:193-194 is off by seven hours.
  - The substantive claim survives in both clocks: Section 0 (01:34:56Z) precedes the first corpus-gate record (01:42:24Z) and the first power-gate record (01:51:14Z). The pre-registration ordering is not impeached; only its labelling is.
- **Recomputation:** None beyond the timestamp comparison above.
- **What would resolve it:** Relabel the progress.md times as local (-07:00), or convert them to UTC.
- **Confidence:** HIGH — the git objects and the ledger agree with each other and disagree only with the label.
- **Could later commits invalidate this?:** No. HEAD equalled the anchored SHA at read time.
- **Disclosed by the authors?:** No.

---

## What Agent A checked and found sound

The bulk of this repository is sound, and several places where the thesis predicted a premature closure turned out to be
registered scope decisions or open items carried honestly. Recorded here so a clean result is not mistaken for a thin pass.

- **The MDE arithmetic.** From `var/insider_dispersion.db` (live, untracked, UNANCHORED, read 2026-09-03T06:32:44Z) I reproduced every reported figure: 126/VW lag 21 → 49.3543 (power.json:12); 126/EW → 34.2897 (:75); 21/VW → 81.4849 (:33); 63/VW → 57.3398 (:54); and the full Newey-West grid 50.1903 / 49.3543 / 49.1057 / 49.5319 (power.json:88-113). Each series sums to zero to 1e-16, so the centering guard holds. Formula sites: src/insider/power/dispersion.py:104-120 (Bartlett VIF), :151-160 (sample SD with n−1), :179 (annualization by sqrt(252)), :182 (N_eff = n / VIF); src/insider/power/mde.py:50, :66. The gate thresholds in src/insider/section0.py:51-87 match REGISTRATION.md:39-46, including the inclusive lower edges.
- **Sensitivity that does not rescue the primary.** With VIF floored at 1.0 (no credit for negative autocorrelation) the primary is 52.04 and the equal-weighted 35.70, so the DEGRADED/BLOCKED split between the two books does not depend on the below-one VIF. The equal-weighted MDE falls to 29.98 at lag 63 and 26.47 at lag 126 (VIF 0.70, 0.55), but the registered lag is 21, so 34.29 stands as the registered figure.
- **Pre-registration ordering.** Section 0 bars (config.py:143-146) were committed in `fbfc74e` before any corpus or power computation, confirmed independently by the commit clock and by the evidence ledger (finding -7). The verdict text in power.json:134-136 matches src/insider/section0.py:77-87.
- **Corpus gate and attrition.** corpus.json: 4,585 qualifying (:2), coverage 0.9954110899 (:173), mean width 71.9089512101 (:174); attrition sums to the 2,876,095 intake (REGISTRATION.md:620); `filtered_code` 2,578,217 and `filtered_role` 131,222 reconcile (:622-623); 9,160 / (148,883 + 9,160) = 5.8% (:657-658; DECISIONS.md:122-123). Lag statistics reproduce from corpus.json:79-168: mean 9.52, p25/50/75/90/95 = 1/1/3/4/4, max 1,988, 73.0% within two days, 95.9% within four, 51.3% within one (DECISIONS.md:98), 91 events over ten days (REGISTRATION.md:673-686). p99 computes to 228 by linear interpolation against the document's 230; immaterial.
- **Fetch and cache claims.** `ledgers/fetch.jsonl` (live, untracked, UNANCHORED, read 2026-09-03T06:35:25Z): 684 records, 214 served from wire totalling 2,783,280,665 bytes, 470 from cache, all status 200, hosts `www.sec.gov` and `data.sec.gov` only. Matches REGISTRATION.md:827-833 exactly. Validation 25 agree / 0 disagree (evidence ledger; DECISIONS.md:64-65); index-to-dataset ratio 2.047-2.108 across quarters in validation.json.
- **Mutation testing.** reports/stage_a1/mutations.json: five mutations, each fails the named guard and restores green (:3-47).
- **ADR-009 direction.** Dropping names that leave the universe mid-hold (returns.py:189-190; 13,750 name-sessions, power.json:118) lowers dispersion and moves the MDE toward GO, so it cannot have caused BLOCKED. The authors say exactly this (DECISIONS.md:275-280). Sound for Direction A; it remains a Stage B blocker in the ledger.
- **Section 0.4 planning arithmetic.** The inversion at each bar reproduces (19.52 / 39.04 bp daily; 3.10 / 6.20% TE; 93.7 / 23.4 names at sigma 30%), and the planning inputs were disclosed as planning values (REGISTRATION.md:90-93). Realized per-name idiosyncratic volatility implied by the books is ~55%, not 30%, and realized VIF is 0.90, not 1.5; the two errors partly offset. This did not bind: the corpus cleared its floor by 4.6x and the authors correctly say sample size did not cause the verdict (REGISTRATION.md:742-743, :846-848).
- **The universe narrowing (Section 4, ADR-004).** Registered before measurement, disclosed at length, consistent with the cost band's scope. Not a premature closure; it is a scope decision and the record says so on every verdict (REGISTRATION.md:326-329, :776-781, :893-896). Its named alternative — "a different universe or a different disclosure regime" (:872-874) — is a reopen condition, carried in the ledger, not a finding.
- **The 13F and congressional rejections (Section 2, ADR-003).** Reasons are structural (45-day lag, ex-post manager selection, public competition) and none has expired between registration and the anchor. Sound.
- **Section 12 operator prior.** Still empty; it blocks Stage B by code (src/insider/registration_check.py:56-64; src/insider/eval/evaluator.py:41). Nothing waited on it operationally (REGISTRATION.md:878-880). Not a premature closure; an open item, carried in the ledger.
- **Claims I could not test.** The SSRN 5966834 citation returned HTTP 403 at read time; the 30-40 bp decayed band has no citation to test at all (finding -2). The sealed alpha in `var/insider_sealed.db` was deliberately not read: its mean is the realized first moment the repository sealed, and opening it would produce exactly the "seen number" the closure discipline exists to prevent.
- **Outside this thesis — recorded for the Direction B pass, not counted as a Direction A finding.** Registration versus code on the entry rule: REGISTRATION.md:377-379 registers "**Entry** is the close of the first session strictly after the filing date … entry at or before the filing date would be unreachable." The membership holds the name on the entry session itself (src/insider/portfolio/membership.py:81-83; tests/test_membership.py:25-28 asserts `held == ["2020-01-05", …]` for entry 2020-01-05), and the return credited on session j is close(j−1) → close(j) (src/insider/portfolio/returns.py:85-92, :196). So the book earns the filing-date-close to next-close move, which is entry at the filing date's close — the point the registration calls unreachable. The effect on the second moment is negligible (about 1.8 entry-day names per session in a 67-name book) and Stage B never ran, so it does not touch the BLOCKED verdict; it would overstate reachable alpha in any Stage B and must be fixed alongside ADR-009 before one runs.

## Dropped at consolidation

No draft finding was dropped in full: all seven carried a locatable verbatim quote with file:line, a figure, and an n.
What changed in consolidation is recorded here.

- **Nothing merged.** The seven drafts challenge seven distinct claims. The three that all attack the BLOCKED closure (-1, -3, -4) do so on different grounds, with different quotes, different evidence and different resolutions — the promotion refusal, the unmeasured Carhart residual, and the substituted weighting basis — so they are kept separate rather than merged. Finding -1 carries an explicit cross-reference so a reader does not count one error three times.
- **Label corrected, DRAFT-all-5 (now -5): DERIVED → READ.** Its recomputation is arithmetic over numbers printed in two files (the Markdown table at REGISTRATION.md:603-608 and the JSON report at corpus.json:4-14). Neither input is stored data, code, or a git object, so the consolidation rule makes it READ. The finding itself is unchanged and its confidence stays HIGH.
- **Citation corrected, finding -5.** The draft cited `corpus.json:34` for the 2018 unclassifiable count of 256. Line 34 of that file is `filtered_programmatic/below_dollar_floor`. The correct citation, verified in the snapshot, is `reports/stage_a1/corpus.json:69`. The sub-claim is retained with the corrected line.
- **Quote span corrected, finding -4.** The draft cited REGISTRATION.md:760-762 for "The value-weighted book is concentrated by construction…". The sentence actually spans :759-761 in the snapshot. Corrected; the quote text is unchanged and verbatim.
- **Held out of the findings deliberately.** The registration-versus-code entry-rule mismatch (see the last bullet above) is a Direction B observation — it would overstate a claim, not close one early — and is recorded in the sound section rather than issued as a Direction A finding.
- **Not pursued.** `var/insider_sealed.db` was never opened, on principle, so no finding here rests on the realized alpha. The Ozlen-Batumoglu SSRN paper could not be retrieved (HTTP 403), so no finding characterizes its contents beyond what the registration itself quotes.

## Live-repo access log

Pre-access `git -C /home/kiros-li/Documents/GitHub/InsiderExperiment status --porcelain` at 2026-09-03T06:30:19Z: (empty output).

Post-access `git -C /home/kiros-li/Documents/GitHub/InsiderExperiment status --porcelain` at 2026-09-03T06:35:25Z: (empty output).

HEAD before and after: `12d9fd36cf055cb10ea67a3fc737e404217bc95a`, equal to the anchored SHA.

Read-only operations performed on the live repository: `git log --format=… --all`, `git rev-parse HEAD`, `git status --porcelain`; `ls -la` of the repository root, `var/`, `docs/` and `reports/`; a SQLite read of `var/insider_dispersion.db` opened as `file:…?mode=ro&immutable=1` (centered series and book widths only; read 2026-09-03T06:32:44Z); reads of `ledgers/evidence.jsonl` and `ledgers/fetch.jsonl` (read 2026-09-03T06:35:07Z and 2026-09-03T06:35:25Z); `cat` of the untracked marker `_CLOSED_DO_NOT_RUN_HERE` (read 2026-09-03T06:32:15Z). Everything read this way is UNANCHORED and may have changed after the anchor. Not opened at any point: `var/insider_sealed.db`, `var/insider_corpus.db`, `var/insider_market.db`, `.env`, `cache/`, `.venv/`.

Consolidation pass (this document): reads confined to `SNAP/InsiderExperiment/` and to the two draft files under `findings/agentA/_drafts/InsiderExperiment/`. No live-repository access, and no new computation beyond re-verifying quoted line numbers in the snapshot.

**Reported loudly, as the common rules require.** The working tree carries an untracked file `_CLOSED_DO_NOT_RUN_HERE`, dated 2026-09-02 22:38 local, which does not appear in `status --porcelain` because, per its own text, it is excluded via `.git/info/exclude`. It states that "a session was opened here by mistake" on 2026-09-02 and declares the repository closed. It postdates the anchor, it is not mine, and no commit followed it — HEAD still equals the anchor. Tracked files carry mtimes no later than the closure commit (2026-08-25 23:23 local). No modification of any kind was made to this repository by this audit.
