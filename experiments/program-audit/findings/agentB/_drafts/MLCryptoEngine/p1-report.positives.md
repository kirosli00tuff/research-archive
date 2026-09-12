# POSITIVES LEDGER — MLCryptoEngine, part p1-report (report.md + README.md)

Repository: MLCryptoEngine @ `5359a11fc753cdcd2606aea991dae826293d0307` (main, 2026-08-22).
Factual, not advocacy. Every entry whose primary evidence lies in `report.md` or `README.md`:
positives, qualified positives, shipped artifacts, open items, and negatives whose verdict rested
on a threshold. Registration dates are the commit dates of the `docs: pre-register …` commits in
the live repository's git log (read-only). "Framing" is how the result is presented in
report.md / README.md; register wording (HYPOTHESES.md) is noted where it differs and is marked
as outside my assigned document set.

---

## 1. Phase A venue-day **PASS** — thresholded positive

- **Claim:** "Phase A is accepted when **all** of the following hold, measured by the validation harness over recorded data" (report.md:10) → "### coinbase — 2026-07-31 — **PASS**" (report.md:457), "### kraken — 2026-07-31 — **PASS**" (report.md:491), 16 PASS verdicts in total.
- **Kind:** thresholded positive (a pass/fail label).
- **Deciding figures (n):** coverage outside gaps 100.00–100.02% against a 99.9% threshold (`FULL_DAY_THRESHOLD = 0.999`, data/validate/replay.py:81); 0 unexplained crossed books, 0 unexplained seq gaps, 17,361,554 CRC32 checksums verified on kraken 2026-07-31 (report.md:466), 3,408,568 sequence numbers on coinbase (report.md:465).
- **Bar + registration date:** criteria 1–4 at report.md:13-22, written 2026-07-30 08:04 in the repository's first commit `bde3082`, before any data existed.
- **Amendments touching the bar:** criterion 4 (top-of-book vs venue snapshots) demoted to "informational, not a pass/fail criterion" in progress.md:227-230, commit `301ea12`, 2026-07-31 — **after** the data existed (the same commit records the PASS and the 7-of-12 / 9-of-15 mismatch counts). Criterion 2 ("attributable to a gap recorded in the recorder's `gaps.jsonl` sidecar") was effectively widened on 2026-08-01 (`2f94b53`) to also excuse session-marker-derived `downtime` and `unclean` gaps; report.md's criteria text was never updated. Criterion 2's "every second of the day" is implemented as ≥ 99.9%.
- **Corrections applied:** warm start so books are live at midnight (state only, nothing pre-day scored); gap unioning and clamping to the recorded span; per-venue integrity mechanism scored ("zero checksum failures is not evidence of integrity" when none ran, data/validate/replay.py:718-721); snapshot-silence failure for snapshot-stream venues.
- **Framing:** report.md prints PASS with no annotation of the criterion-4 mismatches; README.md:79 still calls Phase A "*(current)*"; progress.md:231-232 leaves the Phase A checkbox unchecked as "the operator's call".
- **Audit note:** DRAFT-p1-report-1.

## 2. H1 — short-horizon directional prediction (AUC 0.94) — qualified positive, closed cost-bound; shipped as a note

- **Claim:** "AUC 0.94 at 100 ms is real and it reproduces across days to within 0.0044. It is also **magnitude-blind**" (report.md:2467-2469); README.md:75 links it as "a short-horizon model scored AUC 0.94 on the recorded book and captured ~0.03 bps per trade".
- **Kind:** qualified positive (a real measurement with no economic content) + shipped artifact (`docs/notes/h1-predictability-without-capturability.md`, 313 lines, commit `ae03bf6`, 2026-08-22).
- **Deciding figures (n):** AUC 0.9432 at 100 ms on 165,075 Kraken samples over 6 days; gross capture 0.0291 bps; Spearman rho −0.3175; best top-confidence decile 5.00 bps against an 80 bps round trip (report.md:2288-2295, :2329). Four-day AUC range 0.0044; four-day 900 s capture range −2.44 to +3.05 bps (report.md:2364-2382).
- **Bar + registration date:** C.14 task bars committed in `a2d7466`, 2026-08-04 23:47, before any C.14 figure (report.md:2260-2268); economic filter bar "top-decile capture ≥ 80 bps".
- **Amendments touching the bar:** none to the bar. One *code* fix to match the registered text (`5430eba`, rho sign gate) — the report reads the outcome as **INCONCLUSIVE** under the bar as written (report.md:2312-2318) rather than rewriting the bar. Separately, the Kraken cost input moved 25 → 40 → 25 bps/side (`2299c7f` 2026-08-01; ADR-055 via `81e456e` 2026-08-07), and the 80 bps round-trip comparator used in C.8/C.10/C.14 was never restated (conservative direction).
- **Corrections applied:** purged k-fold CV with embargo; leakage suite with a planted-future canary verified to fire at AUC 0.9714 and a label-shift control at 0.5268 (report.md:2444-2452); single-day headline withdrawn on six-day reproduction; two degraded days named rather than averaged.
- **Framing:** report.md closes H1 harder on the withdrawal; the note discloses the single-day origin, the one-regime scope, the not-run ETH pair and the external audit's "unaudited, not clean" label for this closure. README.md's one-line summary is accurate.
- **Audit note:** sound; the Kraken cost staleness is DRAFT-p1-report-14.

## 3. C.8 — CME transfer — thresholded negative

- **Claim:** "**This is a different negative result from Phase B's** … there is no edge left to capture" (report.md:987-993).
- **Kind:** thresholded negative (the verdict rests on "indistinguishable from zero at the EV column's ±0.005 rounding precision", report.md:1012-1014).
- **Deciding figures (n):** AUC 0.501 and gross capture +0.215 bps at 900 s on 1,109,072 samples, net EV −5.11 maker / −7.04 taker (report.md:1002-1009); 53 days, one instrument.
- **Bar + registration date:** no pre-registered numeric bar for C.8; the deciding standard is "never crosses zero at any horizon in either cost mode".
- **Amendments:** none.
- **Corrections applied:** the one apparent positive (+0.215) was re-tested on an independent subset rather than reported — stride-1 control on 10 April days (896,018 samples, run_id `464f8937`) returns −0.785 bps and AUC 0.490 (report.md:1028-1035); the bar-width confound was separately controlled (report.md:1039-1049); walk-forward honestly counted as **one** clean fold, not three (report.md:1071-1077); the auto-generated "~10 volatility regimes" header corrected to "genuinely covered: one" (report.md:966-972).
- **Framing:** consistent across report.md; "Nothing here says CME micro bitcoin has no exploitable structure" (report.md:1081).
- **Audit note:** sound — this is the model of how a positive inside a corpus of negatives should be treated.

## 4. C.9 — spread-to-cost survey — thresholded negative, with a reserved open tail

- **Claim:** "**Every instrument measured fails, and none is close.**" (report.md:1217); "**Recommendation: do not build the fill simulation against any of these**" (report.md:1231).
- **Kind:** thresholded negative (spread − adverse − cost < 0) + an explicitly reserved open item (the thin tail).
- **Deciding figures (n):** Hyperliquid BTC −3.05, ETH −2.75, CME MBT −4.25 bps (report.md:1210-1216), measured over 53.13 quoted hours / 2,151,124 bbo updates / 342,965 trade messages; adverse selection on 491,982 / 278,835 / 148,768 trades (report.md:1202-1206); 28 instruments surveyed, "**Not one exceeds 1.0**" on spread/cost (report.md:1179).
- **Bar + registration date:** no pre-registered bar; the decision rule ("ratio < 1 means spread < cost, so the net is negative before adverse selection is charged at all") is stated in the section.
- **Amendments:** none.
- **Corrections applied:** spread measured **time-weighted**, not update-weighted; failed measurements (2YY/5YY, mids of 1.4e9) reported as failed rather than as data; SIL/MHG's favourable ratios flagged as untradeable books; the upper-bound caveat stated explicitly ("**This assumes a fill, which no part of this pipeline models**", report.md:1225).
- **Framing:** the reserved tail is stated as the condition for the next stage: "If the thin end survives spread − adverse − cost there, that is the first positive result this project has produced" (report.md:1248-1251).
- **Audit note:** sound; the selection of the 12 subscribed coins is the step later audited at D.1c (see entry 18).

## 5. C.10 — cointegration pairs — thresholded negative

- **Claim:** "**No executable pair survives at Hyperliquid cost with enough trades to be statistically meaningful. Not one.**" (report.md:1607-1608).
- **Kind:** thresholded negative.
- **Deciding figures (n):** 1,653 pairs screened, 432 raw hits against 82.7 expected, 180 BH survivors in formation, **0** in holdout (report.md:1457-1466); persistence 18 of 175 uncorrected, 0 under BH, base rate 5.9%; deflated Sharpe **0.026** against an expected-max-under-null per-bar Sharpe of 0.1058 on 1,095 observations (report.md:1586-1592); executable recent window 36 pairs, 1 raw hit against 1.8 expected (report.md:1553-1562).
- **Bar + registration date:** BH q = 0.05; power floor ≥ 20 trades and ≥ 250 scored bars (report.md:1490-1491); signal parameters "fixed a priori and never searched" (report.md:1488).
- **Amendments:** none.
- **Corrections applied:** survivorship-free universe built on the sample's first month (12 of 60 died in-sample, 20%); splice/ticker-reuse detector (LUNA, BTT excluded); multiple testing (BH); deflation for 1,653 trials; power floor; out-of-sample scoring beginning the day the formation window ends.
- **Framing:** "the structural response was correct and the thing it was applied to was not there" (report.md:1628-1630).
- **Audit note:** sound; DSR arithmetic independently reproduced (Φ(−1.943) = 0.0260).

## 6. C.11 — funding-rate carry — **qualified positive**, then withdrawn against the current regime

- **Claim:** "**This is the first stage that has not produced a clean negative, and that makes it the most dangerous one.** The carry existed and paid. The measured 8% is real." (report.md:1846-1849).
- **Kind:** qualified positive.
- **Deciding figures (n):** 5 of 10 modelled instruments clear a 4% risk-free benchmark — ETH 8.07%, BTC 8.00%, LINK 7.43%, SOL 5.86%, ARB 5.57% on capital, margin 1.6–4.1 points (report.md:1831-1836); 27,761 hourly funding observations for BTC over 3.23 years.
- **Bar + registration date:** the benchmark is stated in-section ("Against the honest benchmark, which is cash and not zero"); no pre-registration commit for C.11.
- **Amendments:** none.
- **Corrections applied:** funding annualised by **elapsed time** rather than a fixed intervals-per-year constant, correcting an 8× hazard at the venue's 8-hourly→hourly boundary (report.md:1672-1682); return reported on **deployed capital** (1.6–3.0× notional), not notional; the missing bear market stated; unmeasurable risks enumerated rather than omitted.
- **Framing:** the positive is immediately qualified — "At 2026 funding levels … **the trade does not clear cash at all**" and "the **yield decay is the finding**" (report.md:1842-1845, :1861-1863).
- **Audit note:** sound; the qualification is in the same section and in the verdict, not a footnote.

## 7. C.13 — cross-sectional funding carry — thresholded negative

- **Claim:** "**Against cash at 4%, not against zero: the strategy returns +0.11% and fails to clear the benchmark by 3.89 points.**" (report.md:2223-2224).
- **Kind:** thresholded negative.
- **Deciding figures (n):** funding +43.68%, price −42.91%, cost −0.66%, net **+0.11%**/yr on 1.18× capital; max drawdown −75.85%; 232 perps, 231 usable, 55 delisted, 4,411,046 funding observations, 1,182 days (report.md:2074-2076, :2117-2124, :2205-2212).
- **Bar + registration date:** 4% risk-free benchmark, stated in-section; a dispersion gate answered before construction.
- **Amendments:** none.
- **Corrections applied:** the three terms kept apart by standing rule (ADR-036); a fixed-cohort control that reverses the naive dispersion reading (241.50% → 53.45%, report.md:2050-2053); survivorship handled by the venue's positional index scheme with the residual bias stated; the parameter sweep reported as noise ("A result that swings 60 points on the choice of rebalance interval is being fitted to the sample", report.md:2197-2199).
- **Framing:** consistent.
- **Audit note:** sound; break-even 1.76 bps/side independently reproduced as 1.75.

## 8. C.16 — time-series momentum — thresholded negative

- **Claim:** "**FAIL against the registered bars**" (report.md:2613).
- **Kind:** thresholded negative.
- **Deciding figures (n):** primary L90/H30 net Sharpe 0.302 vs BTC 0.183, DSR 0.446 (bar 0.95), alpha t = 1.01 (bar 2), 7 of 12 specs positive (bar 8); executable subset (27 of 58 symbols) net Sharpe **0.013** (report.md:2536-2549, :2601-2607); 1,736 days.
- **Bar + registration date:** four simultaneous conditions, commit `88b69d8`, 2026-08-05 22:09, before any result (report.md:2512-2518).
- **Amendments:** none.
- **Corrections applied:** deflated Sharpe over 12 trials; beta control (measured book is net short, beta negative in every cell); survivorship-free universe reused verbatim from C.10 with 12 in-sample deaths as forced exits; statistical-vs-executable split.
- **Framing:** consistent; the regime caveat is stated to cut both ways.
- **Audit note:** sound.

## 9. C.15 — liquidation aftermath — negative on data availability, no bar registered

- **Claim:** "**Identifiable liquidations in the recorded data: zero.**" (report.md:2679).
- **Kind:** thresholded negative (a floor of zero), reached before the hypothesis.
- **Deciding figures (n):** 2,639,510 fills across 116 hour files, twelve instruments, one key-set, no flag; zero occurrences of `liquidat` in any channel; 18.0% zero-hash fills explained by ground truth against `userFillsByTime` (report.md:2645-2668).
- **Bar:** the Task 2 bar was deliberately **never registered** — "registering a bar for an impossible test would be ceremony rather than discipline" (report.md:2686-2688).
- **Amendments:** none.
- **Corrections applied:** the check was run against recorded bytes rather than documentation; proxying liquidations with large trades was declined per the stage's own instruction.
- **Framing:** consistent; the matched-control design is preserved in the register for a future data source.
- **Audit note:** sound.

## 10. C.17 — medium-horizon prediction — thresholded negative that ended the alpha search

- **Claim:** "**FAIL.** No cell passes all six registered bars; no cell passes the two statistical ones individually." (report.md:2840-2841); "**the alpha search of this project ends by decision, dated 2026-08-06**" (report.md:2847-2848).
- **Kind:** thresholded negative + a pre-registered decision.
- **Deciding figures (n):** 40 cells; best DSR 0.499 against a 0.95 bar, best alpha t 1.35 against 2 (report.md:2795-2797); class D's apparent 0.89–1.62 Sharpes rest on 45–59 scored weeks in a window where buy-and-hold BTC scores 1.16–2.06.
- **Bar + registration date:** six simultaneous bars and the end condition, commit `370ba41`, 2026-08-06 07:02, before any data (report.md:2717-2728).
- **Amendments:** none. Artifact patterns were named in advance and each apparent success matched one.
- **Corrections applied:** measured data-lag (+75 days on Coin Metrics) applied per the registration; deflated Sharpe over 40 trials; beta control; long-short variant as the beta-cancelling control; planted-future canary and prefix-invariance probes green.
- **Framing:** consistent, including "recorded as a choice made before the result rather than a reaction to it".
- **Audit note:** sound.

## 11. C.19 — Solana rug-detection availability audit — **GO** (a positive gate decision)

- **Claim:** "Against the registered floor of 5,000: **the hard-rug class alone provides ~76,000 labeled pools free, 15× the floor** — the audit is a **GO**." (report.md:3026-3027).
- **Kind:** positive (a gate opened).
- **Deciding figures (n):** 75,996 of 116,308 SolRPDS pools with ≥ 99% liquidity removal (report.md:3011-3013); known-answer spot-check **1 hit / 3 indeterminate / 0 missed** on four documented rugs (report.md:2983); vendor `rugged` flag recovered 0 of 4 and was disqualified.
- **Bar + registration date:** "**GO requires ≥ 5,000 labeled tokens obtainable free with pre-event feature coverage**; a heuristic scheme that misses documented rugs fails the audit" — commit `35e3466`, 2026-08-06 12:47, before any probe (report.md:2939-2942).
- **Amendments touching the bar:** none written; at evaluation, "misses documented rugs" was operationalised as *provably absent* pre-event signal, under which 1-of-4 detection passes (report.md:2983-2985).
- **Corrections applied:** every source probed against measured reality rather than documentation (pump.fun HTTP 530, Bitquery/Dune/Birdeye 401, MELT data link unverified); the leakage trap named for the domain; the base-rate rule fixed in advance ("judged on minority-class (honest-token) precision, never accuracy", report.md:3008-3009).
- **Framing:** the economics caveat is stated first and unhedged (report.md:2929-2937) — no trading strategy is waiting at the end of this track.
- **Audit note:** DRAFT-p1-report-12.

## 12. C.20 — viability gate ("avoidance is viable") — positive

- **Claim:** "**The mass does not sit in the first minutes. ~96% of the hard-rug class outlives any plausible score-and-act latency**, so avoidance tooling is viable for this class" (report.md:3067-3069).
- **Kind:** positive (a gate), carried forward as the justification for the Helius key.
- **Deciding figures (n):** 75,996 hard-rug pools; removed within 5 minutes 3.93%, within 1 hour 18.8%, within 24 hours 41.5%; median 2.55 days (report.md:3055-3064).
- **Bar + registration date:** no numeric bar for the gate itself; the first-model bar (honest precision ≥ 0.60 at recall ≥ 0.50, time-split holdout, pre-event features only) is registered in commit `902d2e6`, 2026-08-06 19:05, before any model (report.md:3132-3143).
- **Amendments touching the bar:** the 0.60 @ 0.50 bar is carried unchanged through C.21, C.22, C.23 and C.24 ("**Honest-class bar — unchanged from 902d2e6**", report.md:3487-3490).
- **Corrections applied:** the removal-time proxy is stated with its validating observation (96.8% trailing swaps); the scope limit (post-graduation stratum only, bonding-curve deaths outside the data) is stated rather than softened.
- **Framing:** the 96% figure is restated at report.md:3077 and never revisited after the working cutoffs moved to T0+30min / 6h / 24h.
- **Audit note:** DRAFT-p1-report-10.

## 13. C.21 / C.22 / C.23 — the honest bar, attempted and **not cleared** — thresholded negatives

- **Claims:** "**Model vs the bar (902d2e6): NOT CLEARED, on either label version.**" (report.md:3237); "**The bar is not cleared.**" (report.md:3321); "**The honest bar is not cleared, and C.23 identifies why**" (report.md:3452-3453).
- **Kind:** thresholded negatives.
- **Deciding figures (n):** C.21 n = 80, 5 honest in test, precision undefined (0/0); C.22 n = 171, test honest 36, precision **0.411** (v0) / **0.294** (decon) at recall 0.639/0.500 (report.md:3307-3308); C.23 one test fold n = 194, decon precision **0.574** at a 0.500 base rate against v0's 0.984 (report.md:3345-3349).
- **Bar + registration date:** honest precision ≥ 0.60 at recall ≥ 0.50, `902d2e6`, 2026-08-06.
- **Amendments touching the bar:** none. The budget cap was raised once, 30,000 → 60,000, "deliberately and only after the method was proven" (report.md:3283-3287), and held through C.23–C.26.
- **Corrections applied:** window-leak refusal (`WindowLeakError`, never clamped); decontamination reported alongside v0 at every stage; creator-history leakage guard wired and tested before the first creator feature; the v0/decon control used as the clinching evidence that the limitation is signal, not sample.
- **Framing:** consistent, and C.23 narrows the claim rather than widening it ("the narrower, sharper claim C.22 declined to make, now earned").
- **Audit note:** sound. The C.22 "3–4× the 0.013 external base rate" multiple is arithmetically wrong (DRAFT-p1-report-13).

## 14. C.24 — "post-launch behaviour is a **qualified positive** at 6h+" — the track's first substantive positive

- **Claim:** "**A cutoff cleared the honest bar above the noise floor (6h: 0.654 ≥ 0.60, lift +0.097 > 0.02), so the registered negative branch does not fire.**" (report.md:3661-3662).
- **Kind:** qualified positive.
- **Deciding figures (n):** 6h behavioural decon precision **0.654** at recall 0.53, base 0.557, lift **+0.097**; 24h 0.731 / base 0.630 (flagged base-rate-inflated); n_test honest 97; 18 cells scored (report.md:3608-3615, :3636-3640). Survivor-conditioned populations 276 / 256 / 231 with 5 / 25 / 50 excluded (report.md:3590-3592).
- **Bar + registration date:** honest precision ≥ 0.60 at recall ≥ 0.50 (`902d2e6`, 2026-08-06); cutoffs, survivor-conditioning, unanswerable floor of 30, 0.02 noise floor and the end condition registered in commit `c1b469e`, 2026-08-07 02:45, before the results commit `9294da1` at 03:57 (report.md:3485-3545). The persisted matrix `behavior_c24.csv` has mtime 2026-08-07 03:43, between the two.
- **Amendments touching the bar:** none to the numeric bar. The report itself records that survivor conditioning partly compromised it: "The absolute bar, registered before this was visible, is partly compromised by conditioning — a limitation of the pre-registration, recorded as such" (report.md:3598-3600).
- **Corrections applied:** survivor conditioning with per-cutoff non-comparability (ADR-051); matched-population behaviour-vs-launch comparison; cutoff leakage rule with canary/prefix suites run before the first feature; the reachability bias identified and argued to be conservative. **Not applied:** any multiplicity correction over the 18 scored cells, and no confidence interval on the deciding precision.
- **Framing:** "a **qualified** positive, and the qualifications travel with it" (report.md:3665-3673); the register calls it "**qualified positive, open for confirmation**" (HYPOTHESES.md:245, outside my assignment).
- **Audit note:** DRAFT-p1-report-2, DRAFT-p1-report-3, DRAFT-p1-report-6.

## 15. C.24 Task 5 — the **hard-rug clearance scorer** — shipped artifact

- **Claim:** "a *low* score **clears** a pool as not-a-hard-rug at **0.984 precision, covering 0.538 of honest pools**" (report.md:3652-3653), restated at report.md:3968-3970.
- **Kind:** shipped (`research/detection/scorer.py`, `train_scorer.py`, model at `data/processed/detection/hard_rug_scorer.txt`).
- **Deciding figures (n):** test fold n = 194 (117 honest / 77 hard-rug), clearance precision 0.9844 at recall 0.5385, threshold 0.5963; the complementary hard-rug **alarm** is 0.4643 at recall 0.5065 (`hard_rug_scorer.meta.json`, live tree, read 2026-09-12 ~20:00 UTC, UNANCHORED). Those figures imply 63 true and **1** false clearance.
- **Bar + registration date:** no separate bar for the artifact; its figures are C.23's, measured against the `902d2e6` bar.
- **Amendments touching the bar:** the **direction** was corrected on measurement — C.23's headline was re-read as the honest-clearance direction, not a hard-rug alarm (report.md:3646-3658). That is a correction against the artifact's interest.
- **Corrections applied:** creator-history features deliberately excluded as out-of-sample-inert; missing features encoded with a distinguishable sentinel; the scope string ships with the artifact. **Not applied:** re-expression of the precision at the deployment base rate, or an interval on a figure resting on one false positive.
- **Framing:** report.md and the artifact both state the ~99%-scam wild base rate qualitatively; the register goes further in the other direction — "Nothing reopens the *result* — it works" (HYPOTHESES.md:243, outside my assignment).
- **Audit note:** DRAFT-p1-report-4.

## 16. C.25 — "the positive survives unbiasing" — qualified positive, re-measured smaller

- **Claim:** "**The C.24 positive survives the unbiased sample by the registered criterion** (6h v0 clears 0.60 at recall ≥ 0.5, lift +0.047 > 0.02), and **survives in the hard middle**" (report.md:3835-3838).
- **Kind:** qualified positive.
- **Deciding figures (n):** 6h v0 corrected precision 0.822, base 0.775, lift **+0.047** (half C.24's v0 +0.115); mid-activity stratum lift **+0.051** at n = 84 (64 honest), "~0.8 SE", CI includes zero; high-activity stratum lift collapses +0.156 → +0.015 (report.md:3796-3831).
- **Bar + registration date:** commit `5504352`, 2026-08-07 14:04, before results `41e6275` at 15:09 — unanswerable floor 30, lift noise floor 0.02, depth stratification, and an interpretation rule "registered before the strata are seen" (report.md:3695-3734).
- **Amendments touching the bar:** the registered survival criterion was written on **decontaminated** labels (report.md:3700-3706); the verdict was rendered on **v0** labels because decon was measured unaffordable at unbiased scale (report.md:3780-3786). Data existed at the time of the substitution (the budget measurement is Task 2 of the same stage).
- **Corrections applied:** depth-independent Method B retrieval verified at Jaccard 1.0 against the from-now walk; random draw with no reachability or lifetime filter; per-stratum lift used as the honest metric because the base rate rose. **Not applied:** the decon labels the criterion named (verified absent for all 166 depth-corrected pools in `behavior_c25.csv`).
- **Framing:** "it survives **smaller and more honestly**"; the v0 substitution is disclosed in §3 but not carried into C.26's summary of deliverables.
- **Audit note:** DRAFT-p1-report-5.

## 17. C.26 — the detection track concludes — thresholded negative on affordability

- **Claim:** "the decontaminated unbiased test … is **measured-unaffordable at ~2× the cap**" (report.md:3987-3990); "**the detection track concludes with its current outputs**" (report.md:3985-3986).
- **Kind:** thresholded negative (a registered affordability threshold) + a track-closing decision.
- **Deciding figures (n):** priced at **≈ 124,764 weighted** against a 60,000 cap and 1,199 remaining; creator identification failed on **0 of 8** pools; the firming sweep's 92 extra pools moved the mid-stratum lift **+0.051 → +0.032**, SE ≈ 0.039, 95% CI **[−0.045, +0.109]** (report.md:3903-3956).
- **Bar + registration date:** the three-branch affordability threshold (run now ≤ 5,649; proposable raise ≤ 65,000; measured-unaffordable > 65,000) and the end condition, commit `0c62d80`, 2026-08-07 15:28, before results `2403a8e` at 16:14 (report.md:3864-3892).
- **Amendments touching the bar:** none — the cap was explicitly not raised, and the registered rule that "a narrower interval is not a stronger finding when the point estimate has not improved" was applied against the finding.
- **Corrections applied:** the firming result is reported as weakening the positive ("**C.25's +0.051 was optimistic**").
- **Framing:** "a **real but small and unconfirmed** post-launch behavioural signal whose confirmation has a known price the project chose not to pay" — except the deliverables bullet at report.md:3973-3978, which states the composite honest-vs-soft/slow claim without the v0 substitution.
- **Audit note:** DRAFT-p1-report-5.

## 18. C.27 — the thin-perp census — **the project's first bar-clearing positive**

- **Claim:** "Three thin Hyperliquid perpetuals cleared every registered bar … the project's first pre-registered-bar-clearing positive" (report.md:4003-4006).
- **Kind:** positive (upper-bound), with three sub-categories registered in advance.
- **Deciding figures (n):** worst-horizon net with 95% CI lower bound — PUMP **+4.30** (CI +4.27, 499,944 trades), MERL **+6.45** (CI +6.07, 25,378), GMX **+0.40** (CI +0.29, 25,868); failures HYPE −2.11 (1,150,528), SOL −2.61, LINK −1.77, DOT −0.60; NOT +31.15 and TNSR +35.50 sub-capacity; ARB +0.28 with both-halves "no" (report.md:4050-4061). Window coverage 96.4%, with 2026-08-04 at 76.3% (report.md:4013-4021).
- **Bar + registration date:** economics bar, BH q = 0.10 across the ten, ≥ 300-trade floor, both-halves robustness, capacity tier (≥ 150 trades/day and ≥ $100k median daily volume), an explicit upper-bound statement and a full outcome-to-action map — commit `6025f5c`, 2026-08-06 12:18, five days before the scored window closed (report.md:2874-2897).
- **Amendments touching the bar:** none before scoring. After scoring, the repository's own adversarial audit corrected the statistics against itself: A3 (intervals assume independence, 2–17× too narrow; GMX demoted from survivor to **unresolved**), A6 (a one-sided bar judged with a two-sided critical value, making the bar ~19% harder than registered), A8 (capacity divided by calendar rather than recorded days) — report.md:5139-5160, commit `d2a0f05`, 2026-08-12.
- **Corrections applied:** known-answer gate reproducing C.9's closed BTC/ETH nets to −0.001/−0.003 bps; BH q = 0.10; both-halves; capacity tier; an upper-bound discount applied to the marginal survivor (GMX discounted out); coverage validated before the result. **Applied later:** HAC, day-clustered and block-bootstrap intervals. **Not covered by the correction:** the selection step — "BH q=0.10 was corrected across the 10 tested, not the 177 screened" (report.md:4522-4525).
- **Framing:** "They are **not an edge.** They are a hypothesis for **Phase D.1**" (report.md:4098-4101).
- **Audit note:** the selection-bias resolution path is DRAFT-p1-report-8.

## 19. D.1a — feasibility **GO** — positive

- **Claim:** "PUMP and MERL stay net-positive assumed always-last, so the capture's *sign* is settled independent of the unestimable term." (report.md:4236-4239).
- **Kind:** positive (a gate opened), later overturned.
- **Deciding figures (n):** always-last net PUMP **+2.15** (CI +2.00), MERL **+5.42** (CI +4.88); the all-trades column reproduces C.27; consumption prediction fails at median absolute error 100% / p90 100% against a registered 25%/50%; 87% (PUMP) and 99% (MERL) of levels clear by cancellation (report.md:4189-4214).
- **Bar + registration date:** the go bar, the pessimistic-bound shortcut and the definition of a valid no-go, commit `513d2c1`, 2026-08-11 00:35, before probing (report.md:4116-4148).
- **Amendments touching the bar:** none.
- **Corrections applied:** the one-week caveat made specific (≥ 4 weeks spanning more than one regime, reaching viability ~2026-09-08); the Hyperliquid latency gap named as a blocker; hftbacktest ruled out on measured grounds.
- **Framing:** "a positive *range*, not a point" — superseded by D.1d without a supersession banner on this section.
- **Audit note:** DRAFT-p1-report-11.

## 20. D.1c — "H6 survives all four" — positive restated, narrowed

- **Claim:** "**PUMP**: estimate **+2.15 bps per round trip** … Carries the screened-positive demotion" (report.md:4534-4537).
- **Kind:** qualified positive, later overturned.
- **Deciding figures (n):** PUMP spread at one tick 85.5% of the week (kill condition 2 triggers); uncapped inventory **−33.07 bps** against +5.82 bps of edge, every declared cap restoring +1.19 to +1.24 bps/leg at 41–52k fills/day; 300 s and 900 s nets positive with CI lower bounds far from zero on both survivors; 28,705,383 records in one 163 s pass (report.md:4356-4499).
- **Bar + registration date:** four kill conditions, a quoting policy fixed before running, and the ETA rule — commit `4b8bc1f`, 2026-08-11 19:32, before results `8ce2838` at 19:55 (report.md:4270-4332).
- **Amendments touching the bar:** none. Kill condition 4 fired **against** the project: the selection is recorded as a spread-motivated screen and the survivors demoted to screened positives (report.md:4501-4530).
- **Corrections applied:** tick geometry from the venue's own rules; PnL-decomposition identity asserted in tests; MERL's positive inventory term declared "path luck, not a property"; the $10 minimum order value and ALO rejection recorded as replay constraints. **Over-claimed:** "two independent routes to the same number" (report.md:4473-4474) compares two figures produced under the same every-print fill credit.
- **Framing:** the section title itself carries four qualifications; the "+2.15 lower end is robust to entry" sentence (report.md:4391-4393) stands unmarked after D.1d.
- **Audit note:** DRAFT-p1-report-11.

## 21. D.1b — the blind universe rule and the two clocks — **open item at publication, abandoned in fact**

- **Claim:** "**earliest close 2026-09-09**, BH across the full blind set, PUMP/MERL as their own replication family, per the registration" (report.md:4659-4661); "the blind window closing **2026-09-09** remains the first unbiased test" (report.md:4993).
- **Kind:** open (registered, subscribed, never scored).
- **Deciding figures (n):** 25 blind picks across five volume bands from 177 live perps, seed 20260812 fixed before retrieval, plus PUMP and MERL carried over and marked not-blind; load −75% after retiring kraken and coinbase (report.md:4639-4713).
- **Bar + registration date:** the rule, the bands, the caps and the seed, commit `4bde24c`, 2026-08-11 21:43, before the ranking retrieval in `e544aa5` at 21:52; blindness pinned by a test that perturbs every price-like field.
- **Amendments touching the bar:** none. The window itself was **abandoned** at the 2026-08-13 recording stop — "left with 1 day of capture and is **not** a scoreable window" (progress.md:2782-2784, commit `aeabff6`) — which neither report.md nor the register records.
- **Corrections applied:** the rule reads exactly three fields per asset; carryover instruments explicitly excluded from the blind family.
- **Framing:** report.md (three places) and HYPOTHESES.md:197, :263-265 both still present the window as pending.
- **Audit note:** DRAFT-p1-report-8.

## 22. D.1d — H6 closes — thresholded negative

- **Claim:** "**By the registered kill condition, verbatim: the tightened net at the declared cap and the latency floor is ≤ 0 for both instruments, so H6 closes and D.2 does not follow.**" (report.md:4973-4975); corrected headline **PUMP −4.81 / MERL −4.35** (report.md:5122).
- **Kind:** thresholded negative.
- **Deciding figures (n):** PUMP −4.75 → corrected −4.81 bps on 32,018 → 31,875 fills / $14.06M notional; MERL −4.23 → −4.35 on 4,270 → 2,536 fills; negative at 5× and 10× caps, at every latency from +0 to +800 ms (no zero-crossing), and at MERL's price-improved end (−6.35); 28.7M records per pass (report.md:4849-4970, :5118-5133).
- **Bar + registration date:** policy, fill rules, latency, cap, known-answer gate tolerance (±0.10 bps) and the three-branch outcome map, commit `6a17edf`, 2026-08-11 22:46, before results `ed786ce` at 23:16 (report.md:4725-4795).
- **Amendments touching the bar:** none to the kill condition. Three published claims were **withdrawn** after the repository's own adversarial audit (A1 the known-answer gate, A2 the §2b counterfactual arithmetic, A13 the mechanism attribution), all recorded as withdrawals with the published figures retained as an `as_published` variant reproducing exactly (report.md:4799-4808, :5015-5116).
- **Corrections applied:** the A4 queue-model correction moved both instruments **more** negative; a differential test against an independently written reference replay replaced the withdrawn gate and caught a real defect on its first run; the A5 defect was reported with a measured zero effect; per-round-trip vs per-leg units marked (A11: −9.62 per round trip).
- **Framing:** caveats stated in the body, not in footnotes, including "**the D.1d replay ran once, and no second pair of eyes has checked it**" (report.md:4846-4847) and "The Phase B and detection-track closures — H1, H2, H4, H5, H8–H11 — remain unaudited" (report.md:5184-5186). One withdrawn figure pair survives in the verdict (report.md:5002-5003).
- **Audit note:** DRAFT-p1-report-7; the closure itself I found sound.

## 23. Shipped artifacts named in report.md / README.md

| artifact | framing | support |
|---|---|---|
| `research/detection/scorer.py` + `hard_rug_scorer.txt` | "clears a pool as not-a-hard-rug at 0.984 precision / 0.538 recall" (report.md:3968-3970) | 63 correct and 1 incorrect clearance on a 194-pool fold built at a 0.603 honest base rate (DRAFT-4) |
| Method B (depth-independent retrieval) | "~33 weighted/pool regardless of depth, verified at **Jaccard 1.0**" (report.md:3961-3965) | measured on 6 probe pools; the strongest-supported artifact of the detection track |
| `d1d_{PUMP_base,MERL_base,MERL_improved}.json` PerformanceReports | "First reports against the Phase B contract, `mode: backtest` stated explicitly" (report.md:4957-4960) | regenerated under the corrected engine; the expected-vs-realized slippage pair they highlight was withdrawn (A13) |
| The validation harness | README.md:33-35 "Phase A passes only when full days of Kraken and Coinbase data reconstruct with zero unexplained crossed books" | accurate as to criteria 1–3; criterion 4 is not enforced (DRAFT-1) |
| `docs/notes/h1-predictability-without-capturability.md` | README.md:75 | fully sourced to report.md sections and commits; scope section is unusually complete |
| The recorded archive and three recorders | README.md:61 "The recorder is meant to run continuously" | recording ended 2026-08-13 (DRAFT-9) |

## 24. Open items at the anchor SHA

| item | stated status in my documents | fact |
|---|---|---|
| Alpha register | "The **census (H6) is the sole remaining open item**" (report.md:2850-2851), then H6 closes at D.1d | zero open alpha items |
| D2 (honest-vs-slow-rug) | "concluded … real but small and unconfirmed" (report.md:3973-3978) | register calls it "qualified positive, open for confirmation" (HYPOTHESES.md:245, outside my assignment) |
| Hyperliquid latency distribution | "usable 2026-08-19" (report.md:4706) | telemetry stopped 2026-08-13; moot for the sign by the report's own latency grid |
| Blind four-week window | "earliest close 2026-09-09 … remains the first unbiased test" (report.md:4706, :4790, :4993) | abandoned 2026-08-13 with 1 day of capture (progress.md:2782-2784) — DRAFT-8 |
| README's forward plan | "Phase A … *(current)*", Phases B–E ahead (README.md:79-83) | Phases B, C and D.1 were run and concluded — DRAFT-9 |
