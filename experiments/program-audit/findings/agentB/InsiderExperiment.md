# Agent B — InsiderExperiment @ 12d9fd36cf055cb10ea67a3fc737e404217bc95a

Direction B: the program claimed more than it earned. Fourteen findings: two S2, ten S3, two S4.
Consolidated from one draft part (`_drafts/InsiderExperiment/all.md`, 14 drafts). No two drafts
challenged the same claim on the same grounds, so no merges were performed; nothing was dropped
for a missing quote, figure or n. Two label downgrades and several citation precisions were
applied at consolidation and are recorded in each finding's **Consolidation note** and in
"## Dropped at consolidation". Every quote below was re-checked against `SNAP/InsiderExperiment/`
and every recomputation was re-run at consolidation
(`/home/kiros-li/.cache/program-audit/scratchpad/work/agentB-insider-consolidator/recheck.py`).

**Verification pass (2026-09-04).** All fourteen findings were then reviewed by two independent
verifiers — one on citation fidelity, one on disclosure and labelling — and every verdict was
re-checked against `SNAP/InsiderExperiment/` before it was applied. Both verifiers found every
challenged quote EXACT at the cited line; none was NOT_FOUND and no finding's figures were rejected
outright, so **nothing was dropped**. Six findings were corrected (1, 2, 5, 8, 9, 10) and eight
verified unchanged (3, 4, 6, 7, 11, 12, 13, 14). Each finding now carries a **Citation check** line
recording which verdict was applied and, where the two verifiers differed, which was followed and
why. No severity, class or label changed in this pass. IDs were not renumbered.

The repository is closed. `12d9fd3` is its last commit and `_CLOSED_DO_NOT_RUN_HERE` sits in the
live tree, so no finding here can be invalidated by a later commit. Figures read from the
untracked live tree (`var/*.db`, `ledgers/fetch.jsonl`, `cache/`) are marked UNANCHORED and were
read at **2026-09-04T05:39Z**. `var/insider_sealed.db` was not opened.

## Summary — the strongest case for the thesis in this repository

The arithmetic is honest and the pre-registration is real: every published power figure reproduces
from the stored primitives to the last digit, and no Section 0 bar moved between the first commit
and the anchor. The case for the thesis is narrower, and it sits in what this repository ships as
reusable rather than in the BLOCKED verdict it fired. The Section 0.2 power gate — the artifact
offered to the rest of the programme — calibrates its GO and DEGRADED bars against a 30–40 bp band
that the same section's own citation says is 70–80 % dissipated before this design's registered
entry point, and its "minimum detectable effect" is a 50 %-power quantity that no document in the
tree labels as such. The one affirmative verdict, CORPUS-GO, was fired against a floor whose two
derivation models the same run falsified: at the realized event-to-width ratio the registered
1,000 events would have produced a 14.6-name book against the 23.4 names Section 0.4's own BLOCKED
floor requires. Three shipped results tables — the by-year event composition, the unclassifiable
series, and the 71.9-name book width in the closure verdict — carry pre-correction or pre-filter
numbers beside the corrected headlines they contradict. And a registration that says "None in
force" under Amendments carries two registered items that changed after the corpus existed.

---

### AUDIT-B-InsiderExperiment-1
- **Repository / SHA:** InsiderExperiment / 12d9fd36cf055cb10ea67a3fc737e404217bc95a
- **Hypothesis or artifact:** The Section 0.2 power gate — this repository's headline transferable artifact (GO ≤ 20 bp, DEGRADED 20–40 bp, BLOCKED > 40 bp per month), presented at REGISTRATION.md:19-32 and CLAUDE.md:3-18 as the programme's answer to NPDExperiment's late power finding.
- **Direction:** B
- **Class:** STATISTICAL
- **Severity:** S2
- **Label:** DERIVED
- **Claim challenged (verbatim quote):** "The 20 bp GO bar sits below the bottom of the decayed gross band, so a GO design\nresolves the whole band. The 40 bp BLOCKED bar sits at the top of it, so a design\nabove 40 bp cannot resolve any part of the band." — InsiderExperiment/REGISTRATION.md:57-59. The verdict labels the bars carry are at REGISTRATION.md:41-42: "| **GO** | MDE at or below 20 bp per month | The design can resolve the decayed effect band with margin. Stage B is authorized. |"
- **Evidence:**
  - **Both bars are calibrated against a band the same section says is mostly gone before this design can enter.** REGISTRATION.md:51-55: "Ozlen and Batumoglu (SSRN 5966834,\nDecember 2025, Russell 2000 Form 4) report 70 to 80 percent of total alpha\ndissipating between the transaction date and the following trading day, before a\npublic filer can act, leaving a residual they describe as largely confirmatory\nrather than informative."
  - **The registered entry point is strictly after that dissipation.** REGISTRATION.md:377-381: "**Entry** is the close of the first session strictly after the filing date. … The Ozlen and Batumoglu finding is that most of the\nalpha is already gone by this point, and this entry rule is what makes the\nexperiment measure the part a public filer can actually reach." DECISIONS.md:99-101 states the same: "But Ozlen and Batumoglu report 70 to\n80 percent of total alpha dissipating between the transaction date and the\nfollowing trading day, which is inside even that lag."
  - **The bars carry no haircut for it, in the document or in the code.** `mde_go_ceiling_bp=20.0`, `mde_degraded_ceiling_bp=40.0` and `decayed_gross_band_bp=(30.0, 40.0)` are adjacent literals in the frozen config (InsiderExperiment/src/insider/config.py:143-144 and :152). `insider.power.mde.band_position` compares the realized MDE to `cfg.decayed_gross_band_bp` unadjusted (InsiderExperiment/src/insider/power/mde.py:70-82), and `power.json` records `"decayed_gross_band_bp": [30.0, 40.0]` beside the fired verdict (InsiderExperiment/reports/stage_a1/power.json:120-123, verdict at :134).
  - n for the fired verdict: one primary series, 2,581 sessions, MDE 49.3543 bp, N_eff 2,869.9 (reports/stage_a1/power.json:6-12).
- **Recomputation:** Inputs: band (30.0, 40.0) from REGISTRATION.md:50-51 and src/insider/config.py:152; dissipation 70–80 % from REGISTRATION.md:51-53; amortized round-trip drags 16.6667 / 5.3333 bp per month from reports/stage_a1/power.json:128-131. Method: apply the repository's own dissipation range to its own registered band, then subtract its own amortized round trip. Result: reachable gross band 30 × 0.20 = **6.0** to 40 × 0.30 = **12.0** bp per month; net at the registered primary 100 bp round trip **−10.67 to −4.67** bp per month; net at the registered optimistic 32 bp round trip **+0.67 to +6.67** bp per month. The registered GO ceiling of 20 bp is **1.67×** the top of the reachable gross band and **3.0×** the top of the reachable net band, so a design that fires GO — and is told "The design can resolve the decayed effect band with margin" — could not resolve the effect this entry rule is able to reach.
- **What would resolve it:** Either a registered statement that the 30–40 bp band is already measured from a filing-date / next-close entry — in which case the Ozlen–Batumoglu haircut is not additive and the registration should say so, since it currently presents both as applying to the same design — or a re-derivation of the GO and DEGRADED bars against the post-entry reachable band.
- **Confidence:** MEDIUM — the arithmetic uses only figures the repository states and the absence of a haircut is visible in the code, but the registration never says at which entry point its 30–40 bp band is measured. If the band is itself a published post-filing calendar-time alpha (which is the natural reading of a replication of Cohen–Malloy–Pomorski's value-weighted opportunistic-purchase return), the haircut is not additive and this finding falls to a documentation gap. The registration supports neither reading over the other, which is itself the defect.
- **Could later commits invalidate this?:** no — the repository is closed, `12d9fd3` is its last commit, and `_CLOSED_DO_NOT_RUN_HERE` in the live tree forbids further work.
- **Disclosed by authors?:** **partly, and in a different section — not where the bars are set.** The assistant’s prior at REGISTRATION.md:515-520 is formed from the 60–70 % decay, the Ozlen–Batumoglu 70–80 % dissipation and the 16.67 bp cost drag *together*, explicitly against "a decayed\ngross band whose bottom is 30 bp per month", and Section 1 concludes at REGISTRATION.md:187-188 that "the tradable residual is marginal at best". What is nowhere disclosed — and it is the limitation this finding raises — is that the GO and DEGRADED bars at REGISTRATION.md:41-42 and their derivation at :57-59 carry no such haircut. Both inputs are stated (REGISTRATION.md:51-55, :379-381, DECISIONS.md:99-101) and the registration even says at :379-380 that "most of the\nalpha is already gone by this point", but the bar derivation is nowhere reconciled with it, and the closure language at REGISTRATION.md:812-816 presents 30–40 bp gross as the relevant target without qualification. The compounding is acknowledged where the *prior* is formed, not where the *bars* are set, so the S3 disclosure cap does not apply: S2 and DERIVED stand, the no-haircut fact being read off config.py:143-152 and mde.py:70-82 rather than off a document. Note the direction plainly: this makes the BLOCKED verdict that actually fired **more** secure, not less. The defect is in the GO and DEGRADED branches of a gate the repository ships as reusable.
- **Consolidation note:** kept at S2 with the alternative reading stated explicitly in the confidence line, and REGISTRATION.md:379-381 promoted into the evidence because it is the strongest text against the finding as well as for it. Quote and line numbers verified against SNAP.
- **Citation check:** corrected — the disclosure field. Verifier 1 recommended KEEP (quote EXACT, figures YES, every cited line and every recomputed figure confirmed); Verifier 2 recommended CORRECT on the ground that the flat "no" was too strong. I read both passages in SNAP: REGISTRATION.md:515-520 does form the assistant's prior from the decay, the Ozlen–Batumoglu dissipation and the cost drag together, against a band "whose bottom is 30 bp per month", and REGISTRATION.md:187-188 does call the tradable residual "marginal at best". I followed Verifier 2 because those two passages exist and the flat "no" misdescribes them. Nothing else changed: the quote at REGISTRATION.md:57-59 is EXACT, figures YES, and S2 / DERIVED stand because the limitation raised — bars carrying no haircut — is disclosed nowhere, so the S3 cap does not bite.

---

### AUDIT-B-InsiderExperiment-2
- **Repository / SHA:** InsiderExperiment / 12d9fd36cf055cb10ea67a3fc737e404217bc95a
- **Hypothesis or artifact:** The Johnsen programmatic-event filter and the refusal record shipped as `reports/stage_a1/refusals.md`, under Standing guard 4 — "Refusals are demonstrated by producing them, never asserted" (CLAUDE.md:44-46).
- **Direction:** B
- **Class:** INTERNAL_INCONSISTENCY
- **Severity:** S2
- **Label:** DERIVED
- **Claim challenged (verbatim quote):** "The Johnsen filter rejected 209 of 773 clusters." — InsiderExperiment/REGISTRATION.md:693. The registered rule the count is read against is per cluster: "**3.6 The Johnsen programmatic-event filter.** A cluster is rejected when a\nsingle date-and-price pair accounts for eighty percent or more of the\ncontributing buys." — InsiderExperiment/REGISTRATION.md:272-274.
- **Evidence:**
  - **The 773 are anchored windows, not distinct cluster events.** `find_clusters` opens a new cluster at every buy in the stream and keeps the forward window from that anchor: "for i, anchor in enumerate(group):" … "window = [b for b in group[i:] if b.transaction_date <= end]" (InsiderExperiment/src/insider/corpus/cluster.py:76-78), then appends one `Cluster` per anchor that clears `cluster_min_filers` (cluster.py:80-95). One underlying cluster event of size s therefore produces up to s−2 rows.
  - **The shipped refusal artifact shows the duplication directly.** Its two Johnsen blocks are the *same* Darden event under two anchors — cluster 369 (size 12, 12 distinct filers) and cluster 370 (size 11, the same buys minus the lowest CIK), both with `"window": ["2020-04-23","2020-04-27"]` (InsiderExperiment/reports/stage_a1/refusals.md:13-21 and :113-121). The registration presents it as one refusal (REGISTRATION.md:693-697).
  - **The counts.** The shipped artifact records `"clusters_found": 773` and `"clusters_rejected": 209` (InsiderExperiment/reports/stage_a1/corpus.json:171-172). The stored `cluster` table in the live `var/insider_corpus.db` (read 2026-09-04T05:39Z, UNANCHORED) holds exactly 773 rows of which 209 carry `rejected=1`, and those 209 rows come from **10 distinct issuers**: SPG 155, HES 32, DRI 10, MSTR 6, and one each for WPX, CSX, MRVL, CAG, LIN, KDP. n = 773 rows / 106 distinct issuers overall.
  - **A buy inside a programmatic cluster is admitted whenever some sub-window containing it falls under the threshold.** The implementation charges a buy only if it appears in **no** surviving window: `johnsen_rejected_only=frozenset(clustered - surviving)` (InsiderExperiment/src/insider/corpus/cluster.py:103), consumed at `if i in clusters.johnsen_rejected_only:` (InsiderExperiment/src/insider/corpus/build.py:376-377). The registered rule at REGISTRATION.md:272-274 is stated per cluster and admits no such escape.
- **Recomputation:** Inputs: `var/insider_corpus.db` table `cluster` (773 rows, UNANCHORED, read 2026-09-04T05:39Z); `attrition` row `filtered_programmatic/johnsen_same_date_price = 274` (also at reports/stage_a1/corpus.json:34-36 and REGISTRATION.md:641). Method: (i) group rejected rows by symbol and merge overlapping `[window_start, window_end]` intervals; (ii) independently, count rejected rows of size 3, which under this nesting equals the number of distinct rejected events. Results: **36 distinct rejected cluster events** (SPG 23, HES 4, MSTR 2, one each for the other seven) against the reported 209, out of **201 distinct cluster events** against the reported 773; the size-3 count gives 34, agreeing to within two. Implied member buys under the nesting model 209 + 2 × 34 = **277** against **274** actually charged, so roughly 3 buys that sat inside a Johnsen-rejected window were nonetheless admitted because they also fell inside a surviving window; the interval-merge count of 36 events implies up to 7. The admission leak is small; the count inflation is **5.8×** on the rejections (209 anchored rows against 36 merged events; 6.1× against the size-3 estimate of 34) and **3.8×** on the denominator (773 against 201). *(3.7× as originally written was 773/209 — the found-to-rejected ratio, not an inflation.)*
- **What would resolve it:** Reporting distinct cluster events rather than anchored windows (36 of 201, at 10 issuers of 106), or restating the sentence as "209 of 773 anchored five-day windows"; and either amending the Section 3.6 rule to describe the surviving-window escape or removing it.
- **Confidence:** HIGH — the mechanism is twelve lines of the repository's own source, the counts are in its own shipped artifact, and the duplication is visible in the refusal file it publishes as evidence.
- **Could later commits invalidate this?:** no — closed repository; the live store has not been rewritten since 2026-08-25 19:05 local.
- **Disclosed by authors?:** no — neither REGISTRATION.md Section 15.4 nor DECISIONS.md says the cluster count is per anchor, and nothing records that 74 % of the rejections (155 of 209) come from a single issuer.
- **Consolidation note:** the shipped `corpus.json:171-172` counts were added so the finding does not rest on UNANCHORED live data alone; the live store is now corroboration rather than sole source. Quotes and line numbers verified against SNAP.
- **Citation check:** corrected — the rejection-inflation figure. Both verifiers independently reproduced 209 anchored rows against 36 interval-merged rejected events on the live store and both showed that "3.7×" was 773/209, the found-to-rejected ratio, not an inflation. I confirmed it inside the finding's own recomputation, which already reports 36 and 209: 209/36 = 5.81 and 773/201 = 3.85. Changed to 5.8× on the rejections (6.1× against the size-3 estimate of 34) and 3.8× on the denominator, in the recomputation and in the back-reference in "Dropped at consolidation". Quote EXACT, all other figures YES.

---

### AUDIT-B-InsiderExperiment-3
- **Repository / SHA:** InsiderExperiment / 12d9fd36cf055cb10ea67a3fc737e404217bc95a
- **Hypothesis or artifact:** The "minimum detectable effect" itself — every "can / cannot detect" statement in the repository, and the ADR-011 reopening boundary built for a successor repository on the equal-weighted secondary.
- **Direction:** B
- **Class:** STATISTICAL
- **Severity:** S3
- **Label:** DERIVED
- **Claim challenged (verbatim quote):** "**The equal-weighted secondary would have fired DEGRADED at 34.29 bp.**" — InsiderExperiment/REGISTRATION.md:764 (the same figure at REGISTRATION.md:715 and :850-854, DECISIONS.md:314-343, progress.md:40-45). The governing statement it inherits from is "| **BLOCKED** | MDE above 40 bp per month | The design cannot detect an effect anywhere in the range the literature reports. …" — InsiderExperiment/REGISTRATION.md:43.
- **Evidence:**
  - **The MDE is a 50 %-power quantity.** It is defined as `mde_bp_per_month=cfg.t_critical * se * 10_000.0` (InsiderExperiment/src/insider/power/mde.py:66) with `t_critical=2.0` (InsiderExperiment/src/insider/config.py:147) — i.e. the effect size that would produce a t-statistic of exactly 2, which a design detects half the time.
  - **No power level is registered anywhere.** Section 10 registers the critical value only: "**Critical value 2.0.** Registered, two-sided, applied identically to the power\ncomputation in Stage A.1 and to the inference in Stage B." (InsiderExperiment/REGISTRATION.md:478-479). Grepping the whole snapshot for "80 percent power", "type II", "statistical power", "power of the test" and "50 percent power" returns nothing; n = 0 occurrences across the tree.
  - **The module's own docstring is accurate; the prose derived from it is not.** `mde.py` says "The smallest monthly alpha the test could call significant at t critical." (InsiderExperiment/src/insider/power/mde.py:54) — a significance statement. REGISTRATION.md:43 turns it into "The design cannot detect an effect anywhere in the range the literature reports" — a power statement.
  - n: primary 2,581 sessions, sd 62.9519 bp, N_eff 2,869.9 (reports/stage_a1/power.json:6-12); equal-weighted secondary 2,581 sessions, sd 43.1862 bp, N_eff 2,798.1 (reports/stage_a1/power.json:69-75).
- **Recomputation:** Inputs: MDE 49.3543 and 34.2897 bp (reports/stage_a1/power.json:12 and :75), `t_critical` 2.0 (src/insider/config.py:147), bars 20.0 / 40.0 (src/insider/config.py:143-144). Method: multiply by (z₀.₉₇₅ + z₀.₈₀)/2.0 = (1.959964 + 0.841621)/2.0 = **1.4008** to convert a 50 %-power threshold to a conventional 80 %-power one. Result: primary **69.14** bp per month; equal-weighted secondary **48.03** bp per month, which is **above the 40 bp BLOCKED bar**. At conventional power the secondary would have been BLOCKED too, and the "temptation" narrative, the Section 17.4 reopening boundary and ADR-011 in its entirety would not exist. The GO branch survives the conversion only just: a design at the 20 bp GO boundary has an 80 %-power MDE of **28.02** bp, marginally below the 30 bp bottom of the registered band; a design at the 40 bp bar has one of 56.03 bp.
- **What would resolve it:** Registering a power level and reporting the MDE at it, or labelling 49.35 and 34.29 as 50 %-power thresholds wherever they appear — especially in ADR-011, which is written for a future repository to act on.
- **Confidence:** HIGH — the convention is unambiguous in two lines of the repository's own source and the conversion is standard.
- **Could later commits invalidate this?:** no — closed repository.
- **Disclosed by authors?:** no — the repository registers the critical value but never a power level, and the gap between `mde.py`'s accurate docstring and the prose derived from it is nowhere noted. Direction: this makes the BLOCKED verdict **more** secure (69.14 bp against a 40 bp bar) and the DEGRADED-secondary narrative **less** supported.
- **Consolidation note:** the grep result is now stated with its n (0 occurrences); the GO-boundary and BLOCKED-bar conversions were re-run at consolidation and match the draft.
- **Citation check:** verified (quote EXACT, figures YES). Both verifiers re-ran the zero-hit grep for "80 percent power", "type II", "statistical power", "power of the test" and "50 percent power" over the whole snapshot and both reproduced the 1.4008 conversion and its four outputs (69.14 / 48.03 / 28.02 / 56.03).

---

### AUDIT-B-InsiderExperiment-4
- **Repository / SHA:** InsiderExperiment / 12d9fd36cf055cb10ea67a3fc737e404217bc95a
- **Hypothesis or artifact:** CORPUS-GO — the only affirmative verdict this repository fired — and the 1,000-event floor it was fired against, derived in Section 0.4.
- **Direction:** B
- **Class:** UNSUPPORTED_POSITIVE
- **Severity:** S3
- **Label:** DERIVED
- **Claim challenged (verbatim quote):** "Third, at 1,000 events the expected tracking error is about 4.24 percent and the\nexpected MDE about 27 bp per month, which sits inside DEGRADED with room on both\nsides. A floor placed at the BLOCKED boundary would admit corpora whose verdict\nwas decided by rounding." — InsiderExperiment/REGISTRATION.md:137-140. The verdict fired against it: "**CORPUS-GO.** 4,585 qualifying events against a registered floor of 1,000" — InsiderExperiment/REGISTRATION.md:594.
- **Evidence:**
  - **The floor rests on two registered models.** Book width: "At a hold of H sessions and a steady\narrival of lambda qualifying events per session, expected book width is H times\nlambda when no two events name the same issuer." (InsiderExperiment/REGISTRATION.md:115-117). Tracking error: "For a book of k names with average\nidiosyncratic volatility sigma and residuals close to independent, tracking\nerror is about sigma over sqrt(k). Taking sigma at 30 percent annualized" (InsiderExperiment/REGISTRATION.md:105-108). The floor is `corpus_event_floor=1_000` at InsiderExperiment/src/insider/config.py:145, registered at REGISTRATION.md:70-71 and :125-126.
  - **Realized figures.** 4,585 qualifying events (reports/stage_a1/corpus.json:2) over 2,615 in-span sessions (reports/stage_a1/port.json:2); mean priced book 66.93 names (reports/stage_a1/power.json:16) and 29.731282 effective names (reports/stage_a1/portfolio.json:27); realized tracking error 9.9933 % value-weighted and 6.8556 % equal-weighted (reports/stage_a1/power.json:10 and :73); only 496 distinct issuers behind the 4,585 events (`SELECT COUNT(DISTINCT symbol) FROM event` on `var/insider_corpus.db`, read 2026-09-04T05:39Z, UNANCHORED). n = 4,585 events / 2,581 priced sessions.
- **Recomputation:** Inputs as listed. Method: evaluate the two registered models at the realized corpus. (a) **H × λ.** λ = 4,585/2,520 = 1.8194 events per session, H = 126 → predicted book **229.25** names against a realized priced book of **66.93**, an over-prediction of **3.43×**. (b) **σ/√k at σ = 30 %.** At the realized 29.731282 effective names it predicts 5.502 % against a realized 9.9933 %, a factor of **1.816**; at the equal-weighted book's 66.93 effective names it predicts 3.667 % against a realized 6.8556 %, a factor of **1.870**. (c) **The floor's own third justification is internally correct** (30/√50 = 4.2426 %; MDE = 2 × 21 × 4.2426 %/√252 / √1,680 = 27.4 bp) **but was falsified in fact**: the realized corpus was 4.6× the floor and the design fired BLOCKED at 49.35 bp, 1.83× the 27 bp the floor was chosen to deliver. (d) **The decisive number.** At the realized event-to-width ratio (66.93 names / 4,585 events = 0.014598 names per event), the registered floor of 1,000 events would have produced a book of **14.6 names** — below the **23.4 names** Section 0.4's own table (REGISTRATION.md:112) gives as the BLOCKED floor. The floor therefore did not guarantee the property it was registered to guarantee, and CORPUS-GO carries no information about whether the design could be measured.
- **What would resolve it:** A closure note recording that the Section 0.4 dispersion model under-predicted realized tracking error by ~1.85× and over-predicted book width by ~3.43× — enough that the registered floor would have delivered a 14.6-name book against a 23.4-name requirement — so that a successor scaffold does not reuse the σ = 30 % / independent-residuals calibration to set a corpus floor.
- **Confidence:** HIGH for the arithmetic; MEDIUM for the framing, because the σ/√k model is an idiosyncratic-risk model while the realized figure is a tracking error against a differently-weighted benchmark, so part of the 1.85× is systematic mismatch rather than a wrong σ — which is itself the point, since Section 0.4 used the two interchangeably.
- **Could later commits invalidate this?:** no — closed repository.
- **Disclosed by authors?:** **partly, and in both directions.** (i) The distinct-issuer failure is disclosed in advance with a stated remedy: "First, the H times lambda identity assumes distinct issuers. Insider purchases\ncluster in the same name … so realized distinct-issuer width is below the arrival\ncount. The margin absorbs that." (REGISTRATION.md:128-131). The registered margin was 1,000/468 = **2.14×**; the realized shortfall was **3.43×**, so the margin did not absorb it, and nothing records that. (ii) The independence failure is disclosed after the fact and qualitatively: "Section 0.4 computed that staying out of BLOCKED needs\nabout 23 effective names at 30 percent idiosyncratic volatility, and the realized\nbook carries 29.7 with residuals that are not independent, because insider\nbuying clusters by sector during stress." (REGISTRATION.md:754-757). It is not quantified, the 3.43× book-width over-prediction is not mentioned, and Section 17.2's framing — "### 17.2 The corpus did not fail" (REGISTRATION.md:818) followed by "A later reader will see BLOCKED and assume the data was thin. It was not." (REGISTRATION.md:820) — presents CORPUS-GO as a clean pass without saying its floor's justification was wrong by a factor of 1.8 in the same run. Severity is capped at S3 under the disclosure rule.
- **Consolidation note:** the draft's assembled quote "**The corpus did not fail.** A later reader will see BLOCKED and assume the data was thin. It was not." was split into the heading (REGISTRATION.md:818) and the body line (REGISTRATION.md:820), which is how the file reads. The advance disclosure at REGISTRATION.md:128-131 was found at consolidation and added; it moves the finding from "undisclosed model failure" to "disclosed risk whose registered margin was 2.14× against a realized 3.43× shortfall", and the new recomputation (d) — a 14.6-name book at the registered floor against a 23.4-name requirement — was added because it is the concrete consequence.
- **Citation check:** verified (quote EXACT, figures YES). Both verifiers reproduced every figure — 4,585/2,520 × 126 = 229.25 against 66.93 (3.43×), 30/√29.731282 = 5.502, 30/√66.93 = 3.667, 30/√50 = 4.2426, 66.93/4,585 × 1,000 = 14.6 names against 23.4, 1,000/468 = 2.14× — and Verifier 2 records the disclosure handling as a model of the rule.

---

### AUDIT-B-InsiderExperiment-5
- **Repository / SHA:** InsiderExperiment / 12d9fd36cf055cb10ea67a3fc737e404217bc95a
- **Hypothesis or artifact:** The registration's own amendment discipline — Section 16 "Amendments" and the frozen-config rule the repository states in its own source.
- **Direction:** B
- **Class:** PROCESS
- **Severity:** S3
- **Label:** DERIVED
- **Claim challenged (verbatim quote):** "Changing a registered value after that commit requires a numbered\namendment in Section 17 carrying its own evidence." — InsiderExperiment/REGISTRATION.md:8-9; and "None in force. Section 0 fired BLOCKED, so no amendment can authorize Stage B." — InsiderExperiment/REGISTRATION.md:800. The same rule in the code: "Values here are registered in REGISTRATION.md and frozen before Task 4 computes\nanything. Changing one after the corpus is built requires a numbered amendment." — InsiderExperiment/src/insider/config.py:8-9.
- **Evidence:** Two registered items changed after data existed, neither by numbered amendment. n = 2 changes across 7 commits.
  - **(a) A registered `Config` field was deleted.** `git show fbfc74e:src/insider/config.py` carries `benchmark_id: str` and `benchmark_id="U-LIQ-500-VW"`; `git diff cb17046 672b343 -- src/insider/config.py` shows both lines removed at commit `672b343e1a9c9697b578a02a98dd77c6e73f0603` (2026-08-25T19:11:45−07:00). That is after the corpus was built and CORPUS-GO fired at `ccc9b13a2dd6626f3e2b8e6374b2069c155ec11e` (18:47:16−07:00) and after the power gate ran. Section 5 still registers the benchmark in prose — "**Benchmark.** The value-weighted return of the full universe at the same\nweighting basis as the portfolio. Excess return is the portfolio return minus the\nbenchmark return on the same session." (InsiderExperiment/REGISTRATION.md:351-353, in the registered Benchmark paragraph at :351-357) — so a registered design element survives with no frozen-config field behind it. The deleted value `U-LIQ-500-VW` appears in no document at all: the universe is named `U-LIQ-500-stk-w60-m40-p5` at REGISTRATION.md:303 and DECISIONS.md:109, so the benchmark is registered in prose, never by the field’s own name.
  - **(b) The registered Section 3.4 classification rule changed.** `git diff cb17046 672b343 -- src/insider/corpus/routine.py` shows `classify` reordered so the routine pattern is tested before the history gate, in the same post-corpus commit. The registration's Section 3.4 text was never updated and still reads "**Three years of trading history is required to classify at all.** An insider\nwhose first observed trade falls less than three years before the candidate\ntransaction is `insufficient_history`." (InsiderExperiment/REGISTRATION.md:258-260). The shipped code now contradicts it: the routine predicate returns `RoutineClass.ROUTINE` before `first_trade` is ever consulted (InsiderExperiment/src/insider/corpus/routine.py:74-79, with the history gate at :81-83), so an insider who traded the candidate month in the three prior years is `ROUTINE` even when her earliest observed trade is under three calendar years old.
  - **Section 16 already said "None in force." before either change, and was revisited after both without recording them.** `git show 398755b:REGISTRATION.md` carries "## Section 16. Amendments" with "None in force." at its line 593 — written at 18:38:50−07:00, before the corpus was built. The commit `d8b81f1ef50729a12dd90b8e452f56dde706ff7a` (19:11:55−07:00), ten seconds after both changes, edited that sentence only to append the clause that now stands: "None in force. Section 0 fired BLOCKED, so no amendment can authorize Stage B." (REGISTRATION.md:800). The amendments section was therefore touched after both changes and still records none.
- **Recomputation:** Git objects only; all read-only against the live repository. Commands: `git log --format='%H|%ad|%cd|%s' --date=iso-strict`, `git show --stat <sha>`, `git show <sha>:<path>`, `git diff <a> <b> -- <path>`. Commit ordering, all 2026-08-25 at UTC−07:00: `fbfc74e` 18:34:56 → `398755b` 18:38:50 → `ccc9b13` 18:47:16 (corpus built, CORPUS-GO fired) → `cb17046` 19:11:45 → `672b343` 19:11:45 (both changes) → `d8b81f1` 19:11:55 (Section 15 written; Section 16's sentence extended, no amendment added) → `12d9fd3` 23:24:15 (closure).
- **What would resolve it:** A Section 17 amendment recording the `benchmark_id` removal and the Section 3.4 reordering, or a correction of Section 3.4's text to match the shipped rule.
- **Confidence:** HIGH — both changes are in the git record with timestamps against the corpus build, and the surviving contradiction between REGISTRATION.md:258-260 and routine.py:74-83 is readable in the snapshot alone.
- **Could later commits invalidate this?:** no — `12d9fd3` is the last commit and it added Section 17 without an amendment entry.
- **Disclosed by authors?:** **partly.** ADR-008 (DECISIONS.md:226-255) records the ordering change and its one-transaction impact, and ADR-012 (DECISIONS.md:356-374) records how it was found. Neither says the registered Section 3.4 text was left describing the superseded rule, and nothing anywhere records the `benchmark_id` deletion. Severity is capped at S3 under the disclosure rule. Impact on results: nil — `benchmark_id` had no enforcement site, which is why the standing guard forced its removal, and the reordering moved one transaction between two already-excluded labels.
- **Consolidation note:** the routine.py line citation was tightened to :74-79 (routine branch) and :81-83 (history gate) after re-reading the source; the draft's ":74-83" is retained as the enclosing range.
- **Citation check:** corrected — two evidence citations, on the same side as both verifiers. (a) "Section 5's universe benchmark, REGISTRATION.md:335-336" was wrong; I read SNAP and :335-336 is the calendar-time portfolio sentence, while the universe benchmark is registered in the "**Benchmark.**" paragraph at :351-357. Verifier 1 gave :353-354 and Verifier 2 :351-354; I followed Verifier 2's start line because that paragraph opens at :351, and cite :351-353 for the sentences actually quoted. I also confirmed that `U-LIQ-500-VW` appears in no document (the universe is named `U-LIQ-500-stk-w60-m40-p5` at REGISTRATION.md:303 and DECISIONS.md:109) and said so. (b) "Section 16 was written after both changes" was wrong: `git show 398755b:REGISTRATION.md` (read-only, live repo, 2026-09-04T23:16Z) carries Section 16 with "None in force." at its line 593, written 18:38:50−07:00, before the corpus was built; d8b81f1 edited it ten seconds after the two changes only to append the BLOCKED clause. Verifier 1 did not check the provenance of the section and Verifier 2 did; I re-ran the check across all seven commits and confirmed it. The substance survives both corrections — the section was revisited after both changes and still records no amendment. Quote EXACT, all other figures YES.

---

### AUDIT-B-InsiderExperiment-6
- **Repository / SHA:** InsiderExperiment / 12d9fd36cf055cb10ea67a3fc737e404217bc95a
- **Hypothesis or artifact:** CORPUS-GO, Section 15.1 results table — the shipped by-year composition of the 4,585 qualifying events.
- **Direction:** B
- **Class:** STALE_FIGURE
- **Severity:** S3
- **Label:** DERIVED
- **Claim challenged (verbatim quote):** "Qualifying events by entry year. 2016 opens on 2016-04-01 and 2026 closes on\n2026-03-31, so both are partial." — InsiderExperiment/REGISTRATION.md:598-599, followed by the table at InsiderExperiment/REGISTRATION.md:601-608.
- **Evidence:**
  - **The table contradicts the headline three lines above it.** The cells (2016 262, 2017 406, 2018 524, 2019 457, 2020 717, 2021 297, 2022 502, 2023 505, 2024 410, 2025 363, 2026 99) sum to **4,542**, while REGISTRATION.md:594 reads "**CORPUS-GO.** 4,585 qualifying events against a registered floor of 1,000".
  - **The shipped artifact carries a different table.** `reports/stage_a1/corpus.json:3-15` records `events_per_year` as 263, 409, 531, 462, 728, 298, 504, 508, 418, 365, 99, which sums to 4,585 and matches `"qualifying_events": 4585` at corpus.json:2.
  - **The live store agrees with the artifact, not the registration.** `SELECT substr(entry_session,1,4), COUNT(*) FROM event GROUP BY 1` on `var/insider_corpus.db` returns exactly the corpus.json figures and `SELECT COUNT(*) FROM event` returns 4,585 (read 2026-09-04T05:39Z, UNANCHORED). Both tables are the same quantity: `store.events_per_year` is `SELECT substr(entry_session,1,4), COUNT(*) FROM event` (InsiderExperiment/src/insider/corpus/store.py:151-157).
  - **The difference is exactly the number ADR-013 says the old key merged.** "Two identical purchase\nlines on one filing are two reported transactions, and the key silently merged 43\nof them. The build reported 4,585 qualifying events while the table held 4,542." — InsiderExperiment/DECISIONS.md:404-407. n = 4,585 events, difference 43.
- **Recomputation:** Inputs: the eleven cells at REGISTRATION.md:603-607 and the eleven at reports/stage_a1/corpus.json:4-14. Method: sum each. Result: **4,542** and **4,585**; difference **43**, matching DECISIONS.md:406-407 exactly. Git dating: `git diff ccc9b13 cb17046 -- reports/stage_a1/corpus.json` shows the by-year cells changing from the 4,542-summing set to the 4,585-summing set at commit `cb17046308ca81ef63357541f4ad1fec84fe66c2` (2026-08-25T19:11:45−07:00); REGISTRATION.md Section 15 was written ten seconds later at `d8b81f1ef50729a12dd90b8e452f56dde706ff7a` (19:11:55−07:00) and transcribed the pre-correction table. It was never revised, including at the closure commit `12d9fd3`.
- **What would resolve it:** Regenerating REGISTRATION.md Section 15.1 from `corpus.json` or the store, or a note saying the table predates ADR-013.
- **Confidence:** HIGH — three independent sources (registration, shipped JSON, live SQLite store) and a git diff that dates the correction.
- **Could later commits invalidate this?:** no — `12d9fd3` is the last commit and did not touch Section 15.
- **Disclosed by authors?:** no — ADR-013 (DECISIONS.md:400-416) records the defect and states it was corrected, but nothing says the registration's own results table still carries the uncorrected breakdown next to the corrected headline.
- **Consolidation note:** both sums re-run at consolidation (4,542 and 4,585, difference 43). Kept separate from AUDIT-B-InsiderExperiment-11, which challenges a different table with different figures.
- **Citation check:** verified (quote EXACT, figures YES). Both verifiers re-summed both tables (4,542 against 4,585, difference 43) and both re-ran the `git diff ccc9b13 cb17046` dating. Verifier 2 notes that the ADR-013 citation ":404-407" starts one line before the quoted sentence but is locatable and requires no correction, and offers an optional second uncorrected publication site (DECISIONS.md:148-149) that this finding does not need.

---

### AUDIT-B-InsiderExperiment-7
- **Repository / SHA:** InsiderExperiment / 12d9fd36cf055cb10ea67a3fc737e404217bc95a
- **Hypothesis or artifact:** The book-width figure "71.9 names", used in the closure verdict's explanation of what failed.
- **Direction:** B
- **Class:** INTERNAL_INCONSISTENCY
- **Severity:** S3
- **Label:** DERIVED
- **Claim challenged (verbatim quote):** "The value-weighted book holds a mean of **71.9 names and behaves like 29.7\neffective names**, because the heaviest name carries **14.9 percent** of the book\nand the heaviest five carry **33.8 percent**." — InsiderExperiment/REGISTRATION.md:839-841. The same figure at REGISTRATION.md:596 ("Mean book width 71.9 names at the six-month hold"), REGISTRATION.md:747-750, DECISIONS.md:296-298 and progress.md:31-34.
- **Evidence:**
  - **The book that produced the 49.35 bp verdict is not 71.9 names wide.** `reports/stage_a1/power.json:16` records `"book_width_mean": 66.93` for the primary series, and the dispersion store gives the same: the arithmetic mean of the `book_width` column over the 2,581 primary rows is **66.925** (recomputed from `var/insider_dispersion.db`, read 2026-09-04T05:39Z, UNANCHORED).
  - **71.909 is a different quantity.** `MembershipSeries.mean_width()` averages the raw post-filing book over non-empty sessions — "Average book width over sessions that carry a book." (InsiderExperiment/src/insider/portfolio/membership.py:46-54) — *before* the universe-membership filter, whereas the series that reaches the power module carries `len(priced)` after 13,750 name-sessions are dropped for not being universe members at the governing formation (InsiderExperiment/src/insider/portfolio/returns.py:189-210; the drop recorded as `"not_priced": 13750` at reports/stage_a1/power.json:118).
  - **The artifact publishes the two side by side without saying so.** `"book_width_mean": 71.909` (from the raw membership series) sits directly above `"book_width_p10": 46, "book_width_p50": 67, "book_width_p90": 89, "book_width_max": 103` (from the priced series) at InsiderExperiment/reports/stage_a1/portfolio.json:7-12, built at InsiderExperiment/src/insider/portfolio/build.py:52-64. A mean of 71.909 sitting above a p50 of 67 and below a p90 of 89 in a roughly symmetric distribution is the visible symptom. `corpus.json:174` publishes the same raw figure as `"mean_book_width": 71.90895121014215`.
  - n = 2,581 primary sessions; 13,750 dropped name-sessions.
- **Recomputation:** Inputs: `centered_excess.book_width` for (126, value_weighted) in `var/insider_dispersion.db`; reports/stage_a1/portfolio.json:7 and reports/stage_a1/power.json:16. Method: arithmetic mean of the stored widths. Result: **66.925**, matching power.json's 66.93 and differing from the published 71.909 by **6.92 %**. Cross-check: 13,750 / (2,581 × 66.93 + 13,750) = **7.37 %**, which is ADR-009's own figure — "This removed 13,750 name-sessions from the primary series,\nabout 7.4 percent of held name-sessions." (InsiderExperiment/DECISIONS.md:264-265). Note the identity that makes the discrepancy easy to miss: for the equal-weighted book, effective names equals priced names, so the "66.9" that appears in the Section 15.6 table as the equal-weighted *effective* names is the same number as the primary's true mean width.
- **What would resolve it:** Reporting the priced book width (66.93) wherever the measured book is described, and labelling 71.909 as pre-membership-filter.
- **Confidence:** HIGH — reproduced from the stored series, present in the shipped artifacts, and traced to two lines of source.
- **Could later commits invalidate this?:** no — closed repository.
- **Disclosed by authors?:** no — ADR-009 (DECISIONS.md:258-280) discloses the 7.4 % drop and its direction, but nothing says the 71.9 in the verdict narrative is the pre-drop figure while the dispersion behind 49.35 bp used 66.93.
- **Consolidation note:** the gap is stated as 6.92 % (exact) rather than the draft's rounded 7.0 %; `corpus.json:174` added as a third publication site of the raw figure.
- **Citation check:** verified (quote EXACT, figures YES). Both verifiers reproduced the 66.925 mean from the live dispersion store and the 13,750 / 7.4 % cross-check. Verifier 2 observed that the cited range ":839-842" ran one line past the end of the quoted sentence; I confirmed against SNAP that the quote ends at :841 and tightened the range. Verifier 2 also notes, for the record, that the Section 15.6 column heading "Names held" is the closest the repository comes to flagging the distinction.

---

### AUDIT-B-InsiderExperiment-8
- **Repository / SHA:** InsiderExperiment / 12d9fd36cf055cb10ea67a3fc737e404217bc95a
- **Hypothesis or artifact:** The decayed literature band that sets both registered power bars.
- **Direction:** B
- **Class:** ARITHMETIC
- **Severity:** S3
- **Label:** READ
- **Claim challenged (verbatim quote):** "Cohen,\nMalloy and Pomorski report 82 bp per month value-weighted on opportunistic\npurchases over 1989 to 2007. That replicates at roughly 30 to 40 bp per month on\n2008 to 2024 data, a 60 to 70 percent decay." — InsiderExperiment/REGISTRATION.md:48-51.
- **Evidence:**
  - **The two halves of the sentence are not consistent.** 82 bp decayed by 60–70 % is 24.60–32.80 bp, not 30–40 bp.
  - **The same pairing is repeated and load-bearing.** It appears again at REGISTRATION.md:181-184 (Section 1) and at REGISTRATION.md:515-516 (Section 12, where "The 60 to 70 percent decay" is one of the four inputs to the assistant's 0.12 prior), and the band alone is hard-coded as `decayed_gross_band_bp=(30.0, 40.0)` at InsiderExperiment/src/insider/config.py:152 and republished at reports/stage_a1/power.json:120-123.
  - **The number that fixes both bars is attributed to no one.** The 82 bp figure is attributed to Cohen–Malloy–Pomorski and the 70–80 % intraday dissipation to Ozlen–Batumoglu (SSRN 5966834), but grepping the snapshot for "2008 to 2024" returns only REGISTRATION.md:50-51 and :182-183 — n = 2 occurrences, 0 citations.
  - The band enters the fired gate at n = 2,581 sessions, one primary series (reports/stage_a1/power.json:6-12). The decay arithmetic itself has no sample n: it is a document-internal derivation, which is why this finding is labelled READ.
- **Recomputation:** Inputs: 82 bp (REGISTRATION.md:49-50) and decay 60–70 % (REGISTRATION.md:51), both printed in the document. Method: 82 × (1 − d), and the inverse. Result: **24.60 to 32.80 bp per month**, not 30 to 40. Inverting, a band of 30 bp implies a **63.41 %** decay — which lies *inside* the stated 60–70 % range — while 40 bp implies a **51.22 %** decay, which does not. Only the top of the band is inconsistent with the stated decay, and the two halves overlap only on **30 to 32.8 bp**. Measured against what the stated decay produces, the stated band is **uniformly 22.0 % high at both ends** (30/24.60 = 1.2195 and 40/32.80 = 1.2195).
- **What would resolve it:** A citation for the 30–40 bp replication, or a correction of one of the two halves of the sentence. If the band were the arithmetically implied 24.6–32.8 bp, the BLOCKED bar placed "at the top of it" (REGISTRATION.md:58) would be ≈33 bp rather than 40 bp.
- **Confidence:** HIGH — pure arithmetic on two figures in one sentence of the shipped registration.
- **Could later commits invalidate this?:** no — REGISTRATION.md lines 1-157 are byte-identical to the first commit `fbfc74ed9c8b0b2b237da5a8cd0a2b4730ba456d` (`git diff fbfc74e 12d9fd3 -- REGISTRATION.md` shows only additions after line 157), and the repository is closed.
- **Disclosed by authors?:** no — the sentence is presented as a derivation. Direction is conservative for the verdict that fired: a lower band would have set a lower BLOCKED bar and fired BLOCKED a fortiori (49.35 > 33).
- **Consolidation note:** **label downgraded DERIVED → READ.** Both inputs to the recomputation (82 bp, 60–70 %) are numbers printed in a document; the code site (config.py:152) only restates the band and adds no independent evidence, and the git check is an invalidation test rather than the finding's evidence. Under the consolidation rule a recomputation from document figures is READ. The n question is answered explicitly rather than by dropping the finding: a document-internal arithmetic contradiction has no sample n, and the n of the quantity it fixes is given.
- **Citation check:** corrected — two derived statements, both flagged by Verifier 2 and one of them by Verifier 1. (i) "the stated range 60–70 % is wrong at both ends" is false: 1 − 30/82 = 63.41 %, which is inside 60–70; only the top end (1 − 40/82 = 51.22 %) falls outside, so the two halves overlap on 30–32.8 bp. (ii) "22 % (low end) to 52 % (high end)" does not reproduce: 30/24.60 = 40/32.80 = 1.2195, so the band is uniformly 22.0 % high at both ends. I re-ran both on the document's own printed figures before applying. The core contradiction — 82 bp decayed by 60–70 % is 24.60–32.80 bp, not 30–40 — is untouched, so the finding stands. Quote EXACT, other figures YES; the READ label is confirmed correct by both verifiers.

---

### AUDIT-B-InsiderExperiment-9
- **Repository / SHA:** InsiderExperiment / 12d9fd36cf055cb10ea67a3fc737e404217bc95a
- **Hypothesis or artifact:** The closure note's account of what was fetched and what the 2.78 GB cache contains.
- **Direction:** B
- **Class:** STALE_FIGURE
- **Severity:** S3
- **Label:** DERIVED
- **Claim challenged (verbatim quote):** "They are the SEC's parse of the same XML documents, published free, in\n53 files totalling about 750 MB." — InsiderExperiment/DECISIONS.md:57-58. The second claim challenged is one of framing rather than of figure: "53 quarterly SEC structured Form 345 data sets covering 2013q1 to 2026q1,\nretrieved in **214 wire requests** totalling **2.78 GB** with **zero non-200\nresponses** under an 8 per second throttle against the SEC's stated 10 per second\nceiling." — InsiderExperiment/REGISTRATION.md:827-830 (same sentence at progress.md:23-27). Every figure in that sentence verifies exactly — 214 wire requests, 2,783,280,665 bytes, zero non-200 — but it attaches them to "53 quarterly SEC structured Form 345 data sets", and four fifths of both belong to a different family of files.
- **Evidence:**
  - **The claims that hold.** The fetch ledger (`ledgers/fetch.jsonl`, untracked, 684 rows, read 2026-09-04T05:39Z, UNANCHORED) shows 214 wire requests and 470 cache hits, all status 200, wire bytes **2,783,280,665** — exactly the claimed 2.78 GB and exactly the `du -sb cache/` figure, so "The cache on disk is 2,783,280,665 bytes, which\nequals the wire total exactly, so nothing was fetched twice" (REGISTRATION.md:832-833) holds to the byte.
  - **The attribution does not.** The 214 requests and the 2.78 GB are the whole campaign, not the data sets. By URL family the 214 wire requests are 53 `*_form345.zip`, 53 full-index files, 41 per-filing XML, 41 filing `index.json`, 25 `data.sec.gov/submissions` and 1 `company_tickers.json`; the bytes are **570,492,991 for the 53 data sets (20.5 %)**, **2,207,515,405 for the full-index archives (79.3 %)**, 4,018,868 for submissions, **794,966 for the single `company_tickers.json`**, **23,558 for the 41 filing `index.json` lookups** and 434,877 for the XML — six buckets summing to the 2,783,280,665 wire total exactly. n = 684 ledger rows, 214 wire rows.
  - **What that changes.** The full-index archives are the cross-check ADR-002 describes as "**Full-index archives.** An independent per-quarter Form 4 count." (InsiderExperiment/DECISIONS.md:61), so four fifths of the "2.78 GB corpus cache" that Section 17.2 (REGISTRATION.md:832-833) and progress.md:144-149 discuss pruning is not the corpus.
  - **The 750 MB is a 32 % overstatement** against the 570,492,991 bytes measured for the same 53 files.
- **Recomputation:** Inputs: `ledgers/fetch.jsonl` (684 JSON rows, UNANCHORED). Method: group by `served_from`, `status` and URL family; sum `bytes_read`. Results as above. Wire request count 214 against 214 distinct URLs with zero URLs fetched twice on the wire, which independently confirms "nothing was fetched twice". Statuses: `Counter({200: 684})`, and `insider.edgar.client.fetch` records a row *before* it tests the status code (InsiderExperiment/src/insider/edgar/client.py:76-90), so the "zero non-200 responses" claim is falsifiable from the artifact and holds.
- **What would resolve it:** Attributing the 214 requests and the 2.78 GB to the campaign rather than to the 53 data sets, and correcting ADR-002's 750 MB to the measured 570 MB.
- **Confidence:** HIGH — reproduced from the repository's own append-only ledger, which is the artifact the claim cites.
- **Could later commits invalidate this?:** no — closed repository; the ledger has not been appended to since 2026-08-25 19:06 local.
- **Disclosed by authors?:** no.
- **Consolidation note:** the DECISIONS.md 750 MB sentence was promoted into the challenged-claim field, since it is a second quoted claim this finding falsifies and the draft cited it only in the evidence. Line reference corrected to DECISIONS.md:57-58.
- **Citation check:** corrected — the byte attribution, and the challenged claim repointed. Both verifiers found that "818,524 for the index.json lookups" silently merged two families; I re-read `ledgers/fetch.jsonl` read-only (684 rows, 2026-09-04T23:17Z) and confirm 23,558 across the 41 filing `index.json` requests and 794,966 for the single `company_tickers.json`, which sum to the 818,524 that was published as one bucket. Verifier 1 additionally observed that every figure in the quoted REGISTRATION.md:827-830 sentence verifies, so the defect the finding establishes lives in DECISIONS.md:57-58 and in the framing; Verifier 2 did not address the choice of claim. I followed Verifier 1 and repointed the challenged claim to DECISIONS.md:57-58, keeping REGISTRATION.md:827-830 as the framing claim, because the finding's own evidence already concedes that sentence's figures hold. Class left at STALE_FIGURE: Verifier 2 called INTERNAL_INCONSISTENCY a better read but recorded that S3 is right either way, and neither verifier required the change. Quotes EXACT, other figures YES.

---

### AUDIT-B-InsiderExperiment-10
- **Repository / SHA:** InsiderExperiment / 12d9fd36cf055cb10ea67a3fc737e404217bc95a
- **Hypothesis or artifact:** ADR-002's validation of the SEC structured data sets, shipped as `reports/stage_a1/validation.json`.
- **Direction:** B
- **Class:** STATISTICAL
- **Severity:** S3
- **Label:** DERIVED
- **Claim challenged (verbatim quote):** "**Cost.** The corpus depends on the SEC's parse rather than on this\nrepository's. The sample validation is what bounds that risk, and it is a\nsample, not a census." — InsiderExperiment/DECISIONS.md:68-70, with the sample described at InsiderExperiment/DECISIONS.md:64-65: "**Per-filing XML.** Field-by-field validation on a 25-document sample spread\nacross the whole corpus by entry session. 25 agree, 0 disagree."
- **Evidence:**
  - **The sample is drawn only from the survivors.** `sample_xml` selects from `"SELECT accession, symbol, transaction_date, value_usd, issuer_cik "` `"FROM event ORDER BY entry_session, accession"` (InsiderExperiment/src/insider/corpus/validate.py:115-119), then takes every `step`-th row (validate.py:122-123). The `event` table holds only the 4,585 qualifying events (InsiderExperiment/src/insider/corpus/store.py:12-25, written at InsiderExperiment/src/insider/corpus/build.py:412-420).
  - **What that sample can and cannot detect.** The comparison it performs — symbol match, officer-or-director, not ten-percent owner, a P transaction on the recorded date with a matching value, 10b5-1 flag not True (InsiderExperiment/src/insider/corpus/validate.py:68-105) — can detect only a wrongly *admitted* event. It cannot detect the failure ADR-002 names as the risk: a purchase the DERA parse dropped, or one it mis-coded into a state the funnel charges earlier. The funnel charges 2,578,217 transactions to `filtered_code` and 8,613 to `unparseable` (InsiderExperiment/REGISTRATION.md:622 and :621); none of those is sampled.
  - **The complementary check is at document level only.** "The ratio of\nindex rows to data set documents is 2.04 to 2.14 and stable across all 53\nquarters, so no quarter is short." (InsiderExperiment/DECISIONS.md:61-63) — verified: 53 quarters, ratios 2.043 to 2.140, 5,077,629 index rows against 2,440,873 dataset documents (reports/stage_a1/validation.json:2-321). A document-count ratio cannot see a transaction line dropped inside a document that was counted.
  - n = 25 sampled documents against a 4,585-event corpus (0.55 %) and a 2,876,095-transaction intake.
- **Recomputation:** Inputs: `validation.json` `xml_tally` = `{"agrees": 25, "flag_not_reported_in_xml": 19}` (reports/stage_a1/validation.json:474-477), 25 field checks with 0 disagreements; corpus size 4,585 (reports/stage_a1/corpus.json:2). Method: exact one-sided binomial bound with 0 failures in 25 draws. Result: 1 − 0.05^(1/25) = **11.29 %** upper 95 % bound on the field-disagreement rate among *retained* events; the rule of three gives 12 %. The sample is 0.55 % of the corpus and is conditioned on the outcome of every filter it is meant to validate.
- **What would resolve it:** A second sample drawn from the transactions the funnel *rejected* — in particular from `filtered_code` and `unparseable` — checked against the per-filing XML, which is the only draw that can find a missing or mis-coded purchase.
- **Confidence:** MEDIUM — the one-sidedness is certain from the source; its practical importance here is low, because the corpus cleared its floor 4.6-fold and the verdict turns on tracking error rather than on count.
- **Could later commits invalidate this?:** no — closed repository.
- **Disclosed by authors?:** **partly, and only for the sampling.** DECISIONS.md:69-70 says "it is a\nsample, not a census", which discloses that the check is a sample and puts no bound on the residual rate. The selection on survival — the limitation this finding actually raises — is disclosed nowhere, and the sampler’s own docstring gives a reader the opposite impression: "The sample is taken by ordering on entry session and stepping through it,\nso it spans the whole corpus rather than one quarter of it, and it is chosen\nwithout reference to any outcome." (InsiderExperiment/src/insider/corpus/validate.py:111-113) — true of the stepping, and not of the frame, which is the surviving `event` table. Severity is capped at S3 under the disclosure rule for the sampling half; S3 is in any case where the finding sits on its own merits, since no stated conclusion turns on it.
- **Consolidation note:** the validate.py quote was split at its true line boundaries (:115-119 for the SQL, :122-123 for the step) after re-reading the source.
- **Citation check:** corrected — the disclosure field, against the finding. Verifier 1 recommended KEEP; Verifier 2 recommended CORRECT on the ground that "partly" understated the finding's own case, and I followed Verifier 2 after reading SNAP: `sample_xml`'s docstring at src/insider/corpus/validate.py:111-113 states the sample "is chosen\nwithout reference to any outcome", which is true of the stepping and false of the frame, and nothing anywhere discloses the selection on survival. The disclosure field now says plainly that only the sampling is disclosed. Severity, label and every figure are unchanged; both verifiers reproduced 1 − 0.05^(1/25) = 11.29 % and 25/4,585 = 0.55 %. Quote EXACT, figures YES.

---

### AUDIT-B-InsiderExperiment-11
- **Repository / SHA:** InsiderExperiment / 12d9fd36cf055cb10ea67a3fc737e404217bc95a
- **Hypothesis or artifact:** Section 15.4, the front-truncation narrative attached to the `insufficient_history` refusal.
- **Direction:** B
- **Class:** INTERNAL_INCONSISTENCY
- **Severity:** S3
- **Label:** DERIVED
- **Claim challenged (verbatim quote):** "The front\ntruncation it causes is visible in the by-year counts: 449 unclassifiable in\n2016, 257 in 2017, 257 in 2018, falling to 84 by 2023 as the look-back window\nfills." — InsiderExperiment/REGISTRATION.md:701-704.
- **Evidence:** The artifact behind the sentence is `unclassifiable_by_year` at InsiderExperiment/reports/stage_a1/corpus.json:62-78: 2008 1, 2012 1, 2014 1, 2015 11, **2016 449, 2017 257, 2018 256**, 2019 188, 2020 174, 2021 110, **2022 296**, 2023 84, 2024 95, 2025 96, 2026 38. n = 2,057, matching `filtered_routine/insufficient_history` at corpus.json:41 and REGISTRATION.md:643. Two problems.
  - **(a) The 2018 figure is wrong.** The sentence says 257; the artifact says 256. 257 was the pre-ADR-008 value: `git diff ccc9b13 cb17046 -- reports/stage_a1/corpus.json` shows `"2018": 257` becoming `"2018": 256` in the same commit that moved one transaction from `insufficient_history` to `routine` (InsiderExperiment/DECISIONS.md:245-249).
  - **(b) The four years quoted are the only four for which the series falls monotonically.** 2022 is 296, above both 2017 (257) and 2018 (256); 2024 (95) and 2025 (96) are above 2023 (84). The series does not "fall … as the look-back window fills": it falls to 2021, spikes in 2022, and then rises again.
- **Recomputation:** Inputs: reports/stage_a1/corpus.json:62-78. Method: sum and inspect monotonicity. Result: sum **2,057**; the 2016→2026 sequence is 449, 257, 256, 188, 174, 110, 296, 84, 95, 96, 38 — monotone decreasing only through 2021, with a 169 % rise into 2022 and a further rise into 2024-25.
- **What would resolve it:** Quoting the whole series, or correcting 2018 to 256 and stating the 2022 exception.
- **Confidence:** HIGH — the artifact is in the repository and the git diff dates the 257→256 change.
- **Could later commits invalidate this?:** no — closed repository.
- **Disclosed by authors?:** no.
- **Consolidation note:** kept separate from AUDIT-B-InsiderExperiment-6 — different claim, different table, different figures — though both are instances of Section 15 prose transcribing pre-correction artifact values.
- **Citation check:** verified (quote EXACT, figures YES). Both verifiers re-summed the fifteen `unclassifiable_by_year` cells to 2,057, both confirmed the 2018 257→256 change in `git diff ccc9b13 cb17046`, and both confirmed the monotonicity claim (falling only through 2021, +169 % into 2022, rising again into 2024-25).

---

### AUDIT-B-InsiderExperiment-12
- **Repository / SHA:** InsiderExperiment / 12d9fd36cf055cb10ea67a3fc737e404217bc95a
- **Hypothesis or artifact:** The fixed closure verdict language (Section 17.1, ADR-010, progress.md).
- **Direction:** B
- **Class:** OVER_CLOSED
- **Severity:** S3
- **Label:** READ
- **Claim challenged (verbatim quote):** "**The registered primary design cannot resolve the effect at achievable power.\nThe minimum detectable effect is 49.35 bp per month against a registered BLOCKED\nfloor of 40 and against a decayed literature band of 30 to 40 bp per month gross\nand 13 to 35 bp per month net at the six-month hold. Stage B is never written.\nThe repo closes on the finding.**" — InsiderExperiment/REGISTRATION.md:812-816 (identical at DECISIONS.md:288-292 and progress.md:14-18; progress.md:174 declares it "The fixed verdict language, not to be softened or strengthened").
- **Evidence:** The repository states, elsewhere, that the number the verdict is read against is an upper bound of unmeasured size. REGISTRATION.md:790-796: "The Section 14.3 conservatism is the only one large enough to matter. A Carhart\nregression would absorb the persistent size tilt between a mid-cap book and a\nmega-cap-weighted benchmark, and the residual MDE would be lower than 49.35 by an\namount this stage did not measure and will not measure, because measuring it\nafter seeing BLOCKED is choosing a method by its answer." Section 14.3 says the same structurally: "The gate can therefore fire BLOCKED on a\ndesign Stage B would have found marginally better" (REGISTRATION.md:581-582), with "marginally" unquantified. The margin is 23.4 %: 49.3543 against a bar of 40.0. None of the four places the fixed verdict language appears carries that qualification. n = 2,581 sessions, one primary series.
- **Recomputation:** Inputs: `sd_portfolio_daily = 0.014065` and `corr_portfolio_benchmark = 0.903981` (InsiderExperiment/reports/stage_a1/portfolio.json:20 and :22), `sd_daily_excess_bp = 62.9519` and MDE 49.3543 (reports/stage_a1/power.json:9 and :12), bar 40.0 (src/insider/config.py:144). Method: the Stage A.1 excess return imposes a market beta of 1 against the universe benchmark; a regression frees it, so bound the beta channel by sd_p·√(1−ρ²) and scale the MDE by the ratio. Result: freeing the market beta alone gives a residual sd of **60.1381 bp** against 62.9519, i.e. an MDE of **47.15 bp — still above the 40 bp bar**. To reach 40 bp the excess series would need a total factor R² of **34.31 %**, so after the market channel the remaining three Carhart factors would have to explain a further **28.02 %** of the residual variance. The disclosed conservatism therefore does *not* overturn BLOCKED through the only channel bounded from the stored primitives, and the honest statement of the gap is that it is one unmeasured size/value/momentum term wide, not that the verdict is wrong.
- **What would resolve it:** Adding this bound (or any bound) to the closure language, so a later reader knows the 49.35 is an upper bound and how far above the bar it sits after the one correction that can be computed without opening the seal.
- **Confidence:** MEDIUM — the recomputation is exact for the beta channel but says nothing about SMB/HML/UMD, which the repository deliberately did not measure.
- **Could later commits invalidate this?:** no — closed repository.
- **Disclosed by authors?:** **yes.** The authors disclose the upward bias plainly and give a defensible reason for not measuring it, at REGISTRATION.md:578-583 and :790-796, and again at DECISIONS.md:29-32. This finding is not a discovery of the limitation; it is the narrower point that the verdict sentence which is fixed against softening, and repeated in four documents, omits a limitation the registration itself calls "the only one large enough to matter". Under the disclosure rule the finding is READ and capped at S3.
- **Consolidation note:** **label downgraded DERIVED → READ** and the disclosure restated at the head of the disclosure field rather than the foot, because the limitation raised is disclosed at REGISTRATION.md:790-796. The 47.15 bp bound is a genuine derivation from stored artifacts and is not in the repository, but the finding it supports is a disclosed limitation, so the finding takes the READ label. progress.md citation corrected from :15-18 to :14-18.
- **Citation check:** verified (quote EXACT, figures YES). Both verifiers reproduced the 47.15 bp bound from the stored primitives (residual sd 60.1381 bp, R² 34.31 %, market channel 8.74 %, further residual share 28.02 %) and the 23.4 % margin, and both record the disclosure handling and the READ label with the S3 cap as correct.

---

### AUDIT-B-InsiderExperiment-13
- **Repository / SHA:** InsiderExperiment / 12d9fd36cf055cb10ea67a3fc737e404217bc95a
- **Hypothesis or artifact:** `reports/stage_a1/mutations.json`, the artifact backing the "106 tests" claim.
- **Direction:** B
- **Class:** PROVENANCE
- **Severity:** S4
- **Label:** DERIVED
- **Claim challenged (verbatim quote):** "`make all` runs clean: ruff, ruff format, mypy strict on 56 files, 106\n  tests." — InsiderExperiment/progress.md:217-218 (the bullet opens at :216). Commit `672b343` is titled "test: 106 tests green, and five registered mutations that fail the right guard".
- **Evidence:**
  - **The only stored record of the full suite is a progress line, not a result line.** `"final_suite": ".................................                                        [100%]"` (InsiderExperiment/reports/stage_a1/mutations.json:49) — 33 dots, no pass count, no status word.
  - **The harness took its fallback branch.** `scripts/mutations.py:118-122` picks the last line containing "passed", "failed" or "error" and otherwise falls back to `output.splitlines()[-1]`; the stored value shows the fallback was taken, so no summary line was captured.
  - **The run was nonetheless green.** The harness checked the return code — `if code != 0: failures += 1` (InsiderExperiment/scripts/mutations.py:178-179) — so the claim is true; it is the *artifact* that does not evidence it.
  - n: 10 test modules defining 96 `def test_` functions, expanding under `@pytest.mark.parametrize` to ~105 by static count, against 106 claimed and 33 dots on the stored line.
- **Recomputation:** Inputs: `tests/test_*.py` (96 `def test_` definitions) and mutations.json:49. Method: count definitions and parametrize expansions; count dots in the stored progress line. Result: 96 definitions, ~105 collected, exactly 33 dots — consistent with a 72 + 33 two-line progress bar at pytest's default 80-column non-tty width.
- **What would resolve it:** Storing the pytest summary line, or `--junitxml`, rather than whatever line happens to be last.
- **Confidence:** MEDIUM — the absence of a summary in the artifact is certain (the stored string is quoted above and contains no digit but "100"); the ~105 collection count is an estimate from static parsing and may be one off the claimed 106.
- **Could later commits invalidate this?:** no — closed repository.
- **Disclosed by authors?:** no.
- **Consolidation note:** the dot count was re-verified programmatically at consolidation (33 dots, 79-character string). The finding is S4 hygiene: the claim is true, the evidence for it is not shipped.
- **Citation check:** verified (quote EXACT, figures YES). Both verifiers confirmed programmatically that `mutations.json:49` is a 79-character string with 33 dots and no pass count, and both reproduced the static count (10 modules, 96 `def test_` definitions, ~105 after parametrize expansion) that the finding flags as an estimate.

---

### AUDIT-B-InsiderExperiment-14
- **Repository / SHA:** InsiderExperiment / 12d9fd36cf055cb10ea67a3fc737e404217bc95a
- **Hypothesis or artifact:** The measured-cost and timing record in the Stage A.1 progress entry, offered as the auditable cost measurement ("**Cost, measured rather than asserted.**", progress.md:115).
- **Direction:** B
- **Class:** PROVENANCE
- **Severity:** S4
- **Label:** DERIVED
- **Claim challenged (verbatim quote):** "Timings are wall clock, session start 18:20 UTC, boundaries taken from commit\ntimestamps where one exists." — InsiderExperiment/progress.md:193-194.
- **Evidence:**
  - **The commit timestamps it cites are local, not UTC.** `git log --date=iso-strict` gives `fbfc74e 2026-08-25T18:34:56-07:00` … `12d9fd3 2026-08-25T23:24:15-07:00`, i.e. 2026-08-26T01:34:56Z to 2026-08-26T06:24:15Z. n = 7 commits, all at UTC−07:00.
  - **The untracked fetch ledger corroborates with a second clock.** Its first wire row is `"recorded_at": "2026-08-26T01:35:18+00:00"` (`ledgers/fetch.jsonl` line 1, read 2026-09-04T05:39Z, UNANCHORED) — 22 seconds after the 18:34:56 commit, which is only possible if that commit is 01:34:56Z.
  - **The registration inherits the same offset.** "Empty at the time Section 0 was committed at 18:34 on 2026-08-25." — InsiderExperiment/REGISTRATION.md:589-590. The stated session start of "18:20 UTC" is 2026-08-26T01:20Z.
- **Recomputation:** None beyond the offset conversion (−07:00) between the git author/committer timestamps and the ledger's `recorded_at`.
- **What would resolve it:** Dropping "UTC" from progress.md:193, or converting the times in the table at progress.md:196 and following.
- **Confidence:** HIGH — two independent clocks in the repository's own artifacts disagree by exactly seven hours.
- **Could later commits invalidate this?:** no — closed repository.
- **Disclosed by authors?:** no. Immaterial to every result; recorded because the progress entry presents the commit record as the auditable cost measurement.
- **Consolidation note:** none; the draft is carried through unchanged apart from re-verifying progress.md:193-194 against SNAP.
- **Citation check:** verified (quote EXACT, figures YES). Both verifiers confirmed the seven commit timestamps at UTC−07:00 against the ledger's first `recorded_at` of 2026-08-26T01:35:18+00:00, 22 seconds after `fbfc74e`, and Verifier 2 confirmed by grep that nothing in the tree corrects the "UTC" label.

---

## What Agent B checked and found sound

Everything below was checked with the thesis in hand and did not support it. Where the thesis
predicted a failure and the repository did not have it, that is said.

1. **The whole power chain reproduces exactly from the stored primitives.** Sample sd, the Newey–West Bartlett variance inflation, effective periods, annualized tracking error, the monthly standard error and the MDE were recomputed for all four series directly from `var/insider_dispersion.db` (read 2026-09-04T05:39Z, UNANCHORED). Every figure in `reports/stage_a1/power.json` matches to the last published digit: 126 VW n = 2,581, sd 62.9519 bp, TE 9.9933 %, VIF 0.8993, N_eff 2,869.9, SE 24.6771 bp, MDE 49.3543; 21 VW 81.4849; 63 VW 57.3398; 126 EW 34.2897. The lag grid reproduces too (50.1903 / 49.3543 / 49.1057 / 49.5319 at lags 5/21/63/126), so REGISTRATION.md:722-723's "The verdict does not turn on the bandwidth choice." is correct.
2. **The dispersion store really is centred and carries no first moment.** `math.fsum` of the stored series is −1.4e−16, 1.7e−16, −2.9e−16 and −7.5e−17 for the four series. The seal architecture (ADR-006, DECISIONS.md:165-193) is as described in code: `read_sealed_returns` is defined once (InsiderExperiment/src/insider/eval/evaluator.py:33) and refuses before opening the file while Section 12 is empty; the `insider.power` package imports only `config`, `paths` and stdlib. `var/insider_sealed.db` was not opened by this audit.
3. **No look-ahead in the routine/opportunistic rule.** I suspected one: `TradeHistory` is accumulated over the entire 2013q1–2026q1 stream and `classify` is called after the scan (InsiderExperiment/src/insider/corpus/build.py:156-158 and :380). But the routine predicate queries only calendar months `(when.year − 1..3, when.month)`, all strictly prior (InsiderExperiment/src/insider/corpus/routine.py:74-78), and `first_trade` is a minimum, which later trades cannot raise. Both predicates are invariant to trades after the candidate date, and `tests/test_guards.py:397` guards it.
4. **The attrition funnel is internally exact.** 8,613 + 2,578,217 + 131,222 + 148,883 + 2,362 + 2,213 + 0 + 4,585 = 2,876,095 = the stated intake; every sub-reason sums to its parent; the 17 `filtered_code` sub-codes sum to 2,578,217; every published share rounds correctly. 9,160 reached the universe filter and passed, 148,883 did not, giving the published 5.8 % / 94.2 %.
5. **The filing-lag statistics.** Reconstructed from `corpus.json` `lag_distribution` (n = 4,585): 51.32 % within one calendar day (DECISIONS.md:98-99 says 51.3), 73.00 % within two (REGISTRATION.md:683 says 73.0), 95.86 % within four (says 95.9), 91 events beyond ten days (says 91), max 1,988 (says 1,988), mean 9.5154 (says 9.52). Only p99 differs trivially (228 by nearest rank against the published 230).
6. **Session coverage.** 1 − 12/2,615 = 0.9954111, exactly the published `session_coverage` (corpus.json:173), and the denominator is the in-span session count in `port.json`. The coverage floor is applied to book non-emptiness, which is what Section 0.3 registers.
7. **Section 0.4's own arithmetic is internally correct** even where its model is wrong: 19.52 bp / 3.10 % and 39.04 bp / 6.20 % invert correctly at N_eff = 1,680; 23.4 and 93.7 names follow from σ/√k at σ = 30 %; 468 / 1,000 / 1,875 events follow from H × λ at H = 126 and 2,520 sessions; the 11.8 % coverage penalty is √1.25; 30/√50 = 4.2426 %. AUDIT-B-InsiderExperiment-4 challenges the models, not this arithmetic.
8. **The cost model.** 32/6 = 5.3333 and 100/6 = 16.6667 bp per month; the net band 13.3333 to 34.6667 follows from the registered pairing; and `src/insider/cost.py:48-57` states plainly that the low end is the number a verdict is read against, so the appearance of the optimistic bar in the band's upper end is registered rather than smuggled.
9. **"Zero dollars, zero non-200, nothing fetched twice."** All 684 ledger rows are status 200; the client records a row before it inspects the status (src/insider/edgar/client.py:76-90), so a non-200 would appear; 214 wire requests against 214 distinct wire URLs; wire bytes equal `du -sb cache/` to the byte. No paid API appears anywhere in the ledger. AUDIT-B-InsiderExperiment-9 challenges only the attribution of those bytes, not their truth.
10. **The XML and full-index validation figures are real.** `validation.json` holds 25 field checks, 25 agree, 0 disagree, 19 of 25 with the 10b5-1 box absent (against 73.06 % corpus-wide), and 53 quarters with ratios 2.043–2.140 (none outside the published 2.04–2.14); 21 of 25 issuer symbols are present in the SEC's current ticker list, which is the evidence ADR-007 cites for rejecting the XBRL weighting route.
11. **The equal-weighted secondary is genuinely not promoted.** It is registered as the secondary weighting at REGISTRATION.md:387 and as non-verdict-bearing at REGISTRATION.md:474-476, both in commit `398755b` (18:38) — before the corpus was built at 18:47 and before the power gate ran at 19:11. `insider.power.report._plan` fires the gate on `cfg.primary_weighting` only (src/insider/power/report.py:23-28, :73-74, :106). ADR-011's reopening boundary is a stronger disclosure than I expected to find.
12. **The Section 0 bars were never moved.** `git diff fbfc74e 12d9fd3 -- REGISTRATION.md` shows only additions after line 157; `git diff fbfc74e 12d9fd3 -- src/insider/config.py` shows a single change, the `benchmark_id` deletion (AUDIT-B-InsiderExperiment-5). `mde_go_ceiling_bp`, `mde_degraded_ceiling_bp`, `corpus_event_floor`, `corpus_coverage_floor`, `t_critical`, `newey_west_lags` and `decayed_gross_band_bp` are byte-identical from the first commit. This is the single most important thing an audit of a pre-registration can check, and it passes.
13. **ADR-012's self-correction is exemplary.** DECISIONS.md:365-374 volunteers that the parse-tree config guard "catches decoration, not misuse" and that the repository did not solve the residual. I looked for the softer version of that claim and did not find one.
14. **The mutation harness edits real source.** `scripts/mutations.py:143-155` writes, runs, restores and asserts byte equality, and purges `__pycache__` first for the reason ADR-012 gives. The five mutations are on real registered values, not fixtures.
15. **The universe port is verified, not asserted.** `tests/test_universe_port.py:85-91` re-derives membership from the AiTrader source bars at 2016-04-01, 2021-04-01 and 2026-07-01 and asserts 500 of 500 with rank-by-rank comparison; `pyproject.toml:62-68` sets `addopts = "-q --strict-markers"` with no `-m "not slow"` deselection, so the slow test runs in `make test`. `port.json` records both source hashes unchanged across the read.
16. **The V3/V7 distinction is maintained where it matters.** REGISTRATION.md:446-448 and :771-774 insist a power closure is not a measured null, and progress.md's family record qualifies its headline immediately: "Two closed on power rather than on absent signal … This one closed on power alone and closed before measurement." (progress.md:108-113). I looked for the merge of "we could not measure it" into "there is nothing there" and it is not present.
17. **Section 4's narrowing is registered in advance and its cost is measured, not estimated.** REGISTRATION.md:312-329 states the exclusion, ADR-004 puts 148,883 against 9,160 on it, and REGISTRATION.md:326-329 draws the correct conclusion ("a negative here does not refute the literature"). This is the opposite of the failure the thesis predicted.
18. **The 10b5-1 absence is handled as a recorded state, not imputed** (src/insider/corpus/classify.py:80-89, src/insider/absence.py), with the 3,350 of 4,585 (73.06 %) absent count published (corpus.json:169). The composition of the qualifying set is also consistent: 4,167 opportunistic plus 418 routine/insufficient-history events rescued by surviving cluster membership under the registered Section 3.8 disjunction (`SELECT routine_class, COUNT(*) FROM event` returns 4,167 / 414 / 4; UNANCHORED, read 2026-09-04T05:39Z).

**What I would have expected to find if the thesis held strongly here, and did not.** A bar moved after the data was seen; a secondary promoted to primary after the fact; a power closure reported as a measured null; a corpus figure that could not be reproduced from stored primitives; a refusal asserted rather than produced; a guard that never fires. None of those is present. The findings above are all in a narrower band: bars whose *derivation* is unreconciled with the repository's own citations, results tables that were not regenerated after their artifacts were corrected, a count reported in the wrong unit, and a reusable gate whose power semantics are never stated.

## Dropped at consolidation

**Nothing was dropped for a missing quote, figure or n.** All fourteen drafts carry a verbatim
quote locatable in `SNAP/InsiderExperiment/` (each was re-checked at consolidation against the
snapshot at the cited line), a figure, and an n or an explicit statement of why no sample n
applies. There were no duplicate drafts to merge: the draft was produced as a single part, and no
two drafts challenge the same claim on the same grounds.

Recorded here instead are the changes made at consolidation, since the format requires that
nothing be quietly adjusted.

1. **AUDIT-B-InsiderExperiment-8 (was DRAFT-all-2): label downgraded DERIVED → READ.** Both inputs to the recomputation (82 bp, 60–70 % decay) are numbers printed in REGISTRATION.md. The code site `config.py:152` restates the band and adds no independent evidence; the git check is an invalidation test. Under the consolidation rule a recomputation from document figures is READ.
2. **AUDIT-B-InsiderExperiment-12 (was DRAFT-all-12): label downgraded DERIVED → READ,** because the limitation the finding raises is disclosed by the authors at REGISTRATION.md:578-583 and :790-796. The finding is retained at S3 (its cap under the disclosure rule) because it is about the *fixed verdict language*, not about the limitation, and because the 47.15 bp bound it adds is not in the repository. The disclosure is now stated first in that field rather than last.
3. **AUDIT-B-InsiderExperiment-4 (was DRAFT-all-7): an advance disclosure was found at consolidation and added against the finding.** REGISTRATION.md:128-131 discloses the distinct-issuer failure of the H × λ identity in advance and says "The margin absorbs that." The finding now states that the registered margin was 2.14× against a realized 3.43× shortfall, rather than presenting the model failure as undisclosed, and its disclosure field is marked "partly" with the severity cap noted. A new recomputation was added — a 14.6-name book at the registered 1,000-event floor against Section 0.4's own 23.4-name BLOCKED requirement — because it is the concrete consequence the draft left implicit. Its assembled quote of REGISTRATION.md:818-820 was split into the heading (:818) and the body line (:820), which is how the file actually reads.
4. **AUDIT-B-InsiderExperiment-1 (was DRAFT-all-1): the strongest text against the finding was promoted into its evidence.** REGISTRATION.md:379-381 says the entry rule "is what makes the\nexperiment measure the part a public filer can actually reach", which is the clearest sign the authors were aware of the dissipation at entry. It does not reconcile the bar derivation, so the finding stands at S2, but the alternative reading — that the 30–40 bp band is itself a post-filing published alpha, in which case the haircut is not additive — is now stated in the confidence line rather than only implied.
5. **AUDIT-B-InsiderExperiment-2 (was DRAFT-all-5): the anchored evidence was strengthened.** The draft rested the 773/209 counts on the untracked live store; the same counts are in the shipped `reports/stage_a1/corpus.json:171-172`, which is now the primary citation, with the live store as corroboration for the issuer breakdown only.
6. **Citation precisions, none load-bearing.** `progress.md:15-18` → `:14-18` (finding 12); `DECISIONS.md:58` → `:57-58` (finding 9); `validate.py:115-123` split into `:115-119` and `:122-123` (finding 10); `routine.py:74-83` split into `:74-79` and `:81-83` (finding 5); the 71.9-vs-66.93 gap stated as 6.92 % rather than 7.0 % (finding 7); `corpus.json:174` added as a third publication site of the raw book width (finding 7).
7. **One draft claim was checked and not used.** DRAFT-all-5's statement that "roughly 3 buys … were nonetheless admitted because they also fell inside a surviving window" is retained but explicitly subordinated: it rests on a nesting model rather than on a direct count, the two estimates disagree (3 against up to 7), and the finding's weight is on the count inflation, which is 5.8× on the rejections (209 anchored rows against 36 merged events, 6.1× against the size-3 estimate of 34) and 3.8× on the denominator (773 against 201).

Two items in the drafts were considered for dropping and kept, with the reason recorded:
**AUDIT-B-InsiderExperiment-8** has no sample n because it is a document-internal arithmetic
contradiction; dropping a HIGH-confidence exact contradiction on the shipped registration for
want of a sample size would be the wrong call, so the n of the quantity it fixes (2,581 sessions)
is given and the absence of a sample n is stated. **AUDIT-B-InsiderExperiment-13**'s collection
count (~105) is a static estimate that may be one off the claimed 106; the finding is not about
the count but about the artifact storing a progress line instead of a result line, which is
certain, so it is kept at S4 with the estimate flagged.

## Dropped after verification

**Nothing was dropped.** Neither verifier returned `quote_found: NOT_FOUND` or `figures_ok: NO` for
any of the fourteen findings; every challenged quote was confirmed verbatim at its cited line and
every rejected figure was a single derived number inside an otherwise-reproducing finding, which is
a correction rather than a drop. The three PARTIAL figure verdicts (findings 2, 8, 9) and the two
disclosure-field verdicts (findings 1, 10) were applied as corrections and are described in each
finding's **Citation check** line. The correction to finding 5 was to two evidence citations, not to
a figure. No ID was renumbered and no ID was removed from the JSON.

## Live-repo access log

`git -C /home/kiros-li/Documents/GitHub/InsiderExperiment status --porcelain`

Before (first live access, 2026-09-04T05:2xZ): *(empty — no output)*

After (last live access, 2026-09-04T05:39:01Z): *(empty — no output)*

The working tree was clean before and after, with no entries at all — no pre-existing dirt for this
repository and none introduced. Live-repo actions were limited to: `git status --porcelain`,
`git log`, `git show --stat`, `git show <sha>:<path>`, `git diff <a> <b> -- <path>`; read-only
reads of `.gitignore`, `_CLOSED_DO_NOT_RUN_HERE`, `ledgers/fetch.jsonl`, `ledgers/evidence.jsonl`,
`du -sb cache/ var/`, and read-only SQLite URI connections (`mode=ro`) to `var/insider_corpus.db`
and `var/insider_dispersion.db`. **`var/insider_sealed.db` was not opened** — nothing in this audit
reads the realized alpha, and the seal is intact as far as this agent is concerned. `.env` was not
opened. Nothing was written anywhere under the audited repository.

This consolidation pass opened **no** live repository. It read only
`SNAP/InsiderExperiment/` and the two draft files, and wrote only to
`/home/kiros-li/Documents/GitHub/program-audit/findings/agentB/` and to its scratch directory
`/home/kiros-li/.cache/program-audit/scratchpad/work/agentB-insider-consolidator/`.
Every UNANCHORED figure carried forward retains the draft's read time of 2026-09-04T05:39Z and may
have changed since; the repository is closed and carries `_CLOSED_DO_NOT_RUN_HERE`, so change is
unlikely but is not verified by this pass.

**Verification-application pass (this pass).** Two corrections rest on evidence that is not in the
snapshot — finding 5(b)'s provenance of Section 16, and finding 9's per-family byte split — so this
pass made read-only live accesses to check them itself rather than take a verifier's word.

`git -C /home/kiros-li/Documents/GitHub/InsiderExperiment status --porcelain`

Before (first live access, 2026-09-04T23:16:39Z): *(empty — no output, exit 0)*

After (last live access, 2026-09-04T23:17:15Z): *(empty — no output, exit 0)*

The working tree was clean before and after, with no entries at all — no pre-existing dirt and none
introduced. Live-repo actions were limited to `git status --porcelain`, `git log --format=... --date=iso-strict`
and `git show <sha>:REGISTRATION.md` for the seven commits, plus a read-only parse of the untracked
`ledgers/fetch.jsonl` (684 rows, read **2026-09-04T23:17Z**, UNANCHORED — the per-family byte figures
in finding 9 reproduced to the byte against the draft's 2026-09-04T05:39Z read). `var/insider_sealed.db`
was not opened, no `var/*.db` was opened in this pass, and `.env` was not opened. Nothing was written
anywhere under the audited repository. Everything else was checked against `SNAP/InsiderExperiment/`.
Scratch for this pass: `/home/kiros-li/Documents/GitHub/program-audit/work/agentB-applier-insider/`.
