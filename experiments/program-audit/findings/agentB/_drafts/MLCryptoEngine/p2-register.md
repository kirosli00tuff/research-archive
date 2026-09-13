# Agent B draft findings — MLCryptoEngine, part p2-register

**Repository / SHA:** MLCryptoEngine / `5359a11fc753cdcd2606aea991dae826293d0307` (main, 2026-08-22)
**Assigned documents (read in full):** `HYPOTHESES.md` (572 lines), `DECISIONS.md` (2,701 lines), `AUDIT.md` (647 lines), `docs/notes/h1-predictability-without-capturability.md` (313 lines), `audit/` (census_ci.py, census_ci.json, probe2.py, probe_fill_replay.py, replay_variants.py, variants_*.json).
**Read for context:** `README.md`, `CLAUDE.md`, `config/venues.yaml`, `research/microstructure/{registered,horizons,d1c,fill_replay,census}.py`, `research/detection/{scorer,train_scorer}.py`, and the specific `report.md` / `progress.md` sections the register cites.
**Unanchored reads (live working tree, read-only):** `data/processed/detection/hard_rug_scorer.meta.json`, `data/processed/detection/features_c23.csv`, `data/raw/venue=hyperliquid/date=2026-08-0{4,5}/` directory listing and mtimes — all read **2026-09-12 ~18:14–18:20 UTC**. These are untracked/gitignored and may have changed since the anchor.

Direction B throughout: the thesis under test is that conclusions outran evidence.
Where the repository disclosed the limitation I am raising, I say so and where.

---

### DRAFT-p2-register-1
- **Repository / SHA:** MLCryptoEngine / 5359a11fc753cdcd2606aea991dae826293d0307
- **Hypothesis or artifact:** H1 — "Short-horizon directional prediction on crypto spot", specifically its **registered reopening condition**, which is quoted character-for-character into the shipped README-linked note `docs/notes/h1-predictability-without-capturability.md` and pinned there by test (ADR-065, DECISIONS.md:2617-2626).
- **Direction:** B
- **Class:** UNSUPPORTED_POSITIVE
- **Severity:** S1
- **Label:** DERIVED
- **Claim challenged (verbatim quote):** "A round-trip cost below roughly **3 bps**, i.e. under 1.5 bps per side. On Coinbase that is the 0 bps maker tier requiring **$250M trailing 30-day volume**; on Kraken, the 0 bps maker tier at **$10M**. Neither is reachable at this project's capital. **Reopens on cost, not on modelling** — AUC 0.596 says there is signal there" — MLCryptoEngine/HYPOTHESES.md:54 (restated verbatim at MLCryptoEngine/docs/notes/h1-predictability-without-capturability.md:261 and endorsed again at :265-268: "AUC 0.596 says there is something there").
- **Evidence:**
  - The 3 bps threshold is the cost level at which the **superseded** headline would have paid. The register's own deciding-number cell says so: "**3.31 bps** gross capture at the 900 s horizon against **80.00 bps** round-trip maker cost … **Superseded by C.14 (2026-08-05): that 3.31 bps came from a single day. Across four full days the same measurement ranges −2.44 to +3.05 bps** — a draw from a distribution centred near zero, not a small positive edge" (MLCryptoEngine/HYPOTHESES.md:50). The reopening cell was not restated when the figure it is derived from was superseded.
  - On the measurement that replaced it — six validated days, Kraken BTC/USD, n = 165,075 — **no all-sample gross capture at any horizon reaches 3 bps**: 0.0291 / 0.0576 / 0.0850 / 0.3053 / **0.7237** / 0.2093 bps at 100 ms / 500 ms / 1 s / 5 s / 30 s / 900 s (MLCryptoEngine/report.md:2293-2298; same table at MLCryptoEngine/docs/notes/…:54-59). The maximum is **0.7237 bps at 30 s**, 4.1× short of the registered 3 bps threshold.
  - The note itself states the same thing for the reproducing horizon: "Against the cheapest venue reachable from this operator's jurisdiction at all — Hyperliquid at **3 bps** — it still misses by roughly **100×**" (MLCryptoEngine/docs/notes/…:82-85). So the document that quotes the reopening condition also prints the arithmetic showing the condition would not reopen anything.
  - Coinbase's 900 s AUC — the only number the condition offers as evidence that "there is signal there" — **does not reproduce**: across the four full days it ranges **0.3612 to 0.5931** (n = 4 days; MLCryptoEngine/report.md:2366), i.e. every daily value lies below the 0.596 the closure quotes, and the low end is below 0.5 (reversed discrimination). The 0.596 is the single day 2026-07-31 (MLCryptoEngine/report.md:2377).
  - Conversely, the one figure in the study that *does* exceed 3 bps is the **900 s top-confidence decile at 5.0020 bps** (MLCryptoEngine/report.md:2298). At the 3 bps round trip the condition names, that filter clears by 1.7×, which contradicts the note's flat statement two lines later: "There is no selection filter hiding in the predictions" (MLCryptoEngine/docs/notes/…:101). The register makes the same claim: "There is no hidden selection filter" (MLCryptoEngine/HYPOTHESES.md:54).
- **Recomputation (if any):**
  - Inputs: capture-by-horizon row, MLCryptoEngine/report.md:2293-2298 (0.0291, 0.0576, 0.0850, 0.3053, 0.7237, 0.2093 bps); top-decile 900 s 5.0020 bps, MLCryptoEngine/report.md:2298; threshold 3.0 bps, MLCryptoEngine/HYPOTHESES.md:54.
  - Method: divide the registered threshold by each measured capture.
  - Result: 3 / 0.7237 = **4.14×** short at the best horizon; 3 / 0.0291 = **103.1×** short at the horizon whose AUC reproduces to 0.0044. And 5.0020 / 3 = **1.67× above** the threshold for the top decile. Script: `/home/kiros-li/.cache/program-audit/scratchpad/work/agentB-MLCryptoEngine-p2/` (inline).
- **What would resolve it:** Restate H1's reopening condition against a figure that reproduces — e.g. "a round-trip cost below the measured six-day capture at the horizon that reproduces (0.03 bps at 100 ms), which no reachable venue approaches" — or, if the 3 bps threshold is retained, state which measured quantity is expected to clear it and reconcile it with the "no selection filter" claim, since the 900 s top decile does clear 3 bps.
- **Confidence:** HIGH — the arithmetic uses only figures printed in the repository's own tables, and the register itself labels the figure the threshold derives from as superseded.
- **Invalidated by later commits?:** no — the note and the register are the anchored SHA's final state; recording ended 2026-08-13 (DECISIONS.md:2583) and no later measurement exists.
- **Disclosed by authors?:** Partly. The supersession of the 3.31 bps figure is disclosed at MLCryptoEngine/HYPOTHESES.md:50 and in the note's §6 (docs/notes/…:123-137), and the 100×-at-3 bps arithmetic is printed at docs/notes/…:82-85. What is **not** disclosed anywhere is that those disclosures falsify the reopening threshold the same documents carry, and the note re-endorses the superseded AUC as evidence of signal at docs/notes/…:265-268.

---

### DRAFT-p2-register-2
- **Repository / SHA:** MLCryptoEngine / 5359a11fc753cdcd2606aea991dae826293d0307
- **Hypothesis or artifact:** D1 — the **shipped** hard-rug clearance scorer (`research/detection/scorer.py`, model `data/processed/detection/hard_rug_scorer.txt`), the only artifact in the register declared unreopenable.
- **Direction:** B
- **Class:** UNSUPPORTED_POSITIVE
- **Severity:** S2
- **Label:** DERIVED
- **Claim challenged (verbatim quote):** "Nothing reopens the *result* — it works." — MLCryptoEngine/HYPOTHESES.md:243; deciding number: "**Honest-clearance precision 0.984 at recall 0.538** on the 2024 test fold (train ≤ 2023), from 30-minute launch-window features." — MLCryptoEngine/HYPOTHESES.md:239.
- **Evidence:**
  - **The headline is 63 correct clearances and one error.** The shipped model's own sidecar records `test_n: 194`, `test_hard_rug: 77` (so 117 non-hard-rug), and `clearance_point_pos_honest_recall_ge_0.5: {precision 0.9844, recall 0.5385, threshold 0.5963}` — `/home/kiros-li/Documents/GitHub/MLCryptoEngine/data/processed/detection/hard_rug_scorer.meta.json`, read 2026-09-12 18:14 UTC (untracked; may have changed since the anchor). 0.5385 × 117 = 63 true positives; 63/0.9844 = 64 predictions, so **FP = 1**.
  - **The training fold is 87 pools.** Same sidecar: `train_n: 87`, `train_hard_rug: 42`. Independently confirmed by counting the feature matrix: 281 rows, 87 with `year != 2024` (45 `honest_candidate` / 42 `hard_rug`), 194 with `year == 2024` (117 / 77) — `/home/kiros-li/Documents/GitHub/MLCryptoEngine/data/processed/detection/features_c23.csv`, read 2026-09-12 18:18 UTC. The register's Sample row gives "281 reached to T0, 194 in the 2024 test fold" (MLCryptoEngine/HYPOTHESES.md:240) and never states that the model ships from an 87-pool fit.
  - **The operating point is chosen on the fold it is scored on.** `pr_at_recall` computes `i = argmax(precision)` over every cut point with `recall ≥ 0.5` and returns that precision, recall and threshold (MLCryptoEngine/research/detection/train_scorer.py:50-62); it is called on the test fold only — `p = model.predict_proba(x[te])`, then `clear = pr_at_recall(1 - y[te], 1.0 - p)` (MLCryptoEngine/research/detection/train_scorer.py:72-76). The argmax ranges over every cut point at which `tp ≥ 59` (recall ≥ 0.5 of 117), i.e. up to ~136 candidates on a 194-row fold. No validation fold, no nested selection, no held-out re-estimation exists.
  - **No interval accompanies the figure anywhere** — not in the register (HYPOTHESES.md:239), not in the shipped scope note (`research/detection/scorer.py:112-121`, which hard-codes the same maximised precision into the text an end user reads), not in report.md:3351 or :3969.
  - **The standard the same repository applied to its negatives.** H6's census bar required a "**95% CI lower bound above zero at the worst of the three horizons**" plus Benjamini–Hochberg at q = 0.10 and a both-halves robustness test (MLCryptoEngine/HYPOTHESES.md:201); H9 and H11 were closed on deflated Sharpe against registered trial counts (DSR 0.446 vs a 0.95 bar, HYPOTHESES.md:147; 0 of 40 cells, best DSR 0.499, HYPOTHESES.md:181); H4 on Benjamini–Hochberg over 1,653 pairs plus a deflated Sharpe (HYPOTHESES.md:98); ADR-030 makes "raw hits, expected-by-chance, and corrected hits — always all three" a standing rule (DECISIONS.md:1310-1333). The shipped positive received none of these, and the mechanism by which it escaped them is explicit: ADR-044 places the detection track "outside the closed alpha register" (DECISIONS.md:1929-1964).
- **Recomputation (if any):**
  - Inputs: `test_n = 194`, `test_hard_rug = 77`, `precision = 0.9844`, `recall = 0.5385` (hard_rug_scorer.meta.json, read 2026-09-12 18:14 UTC); base rate 0.603 (report.md:3351).
  - Method: back out the confusion counts, then Clopper–Pearson and Wilson 95% intervals on the clearance precision.
  - Result: TP = 63, FP = 1, precision = 63/64 = 0.9844. **Clopper–Pearson 95% lower bound = 0.9160**; Wilson 95% interval = **[0.9167, 0.9972]**. Against the fold base rate 0.603 the lift is +0.381 with a lower bound of +0.313 — a real effect, but the point estimate quoted as the artifact's operating precision is the maximum of ~136 fold-selected cut points and turns on a single misclassification.
- **What would resolve it:** Publish the clearance precision with an interval and with the operating threshold fixed before the test fold is scored (e.g. chosen by cross-validation inside the 87-pool training fold), and replace "Nothing reopens the *result* — it works" with a reopening condition of the kind every other register entry carries.
- **Confidence:** HIGH — the confusion counts follow arithmetically from the artifact's own sidecar, and the fold-selected threshold is visible in the shipped source.
- **Invalidated by later commits?:** no — `train_scorer.py` and `scorer.py` are unchanged at the anchor and the detection track concluded at C.26 (ADR-054, DECISIONS.md:2228).
- **Disclosed by authors?:** Partly. `report.md`'s table column is literally headed "max precision @ recall ≥ 0.5" (MLCryptoEngine/report.md:3349), so the statistic's definition is visible, and the scope note discloses the alarm weakness (0.464) and the ~99% wild base rate. What is not disclosed anywhere: n = 64 predictions with one error, the 87-pool training fold, any interval, or that the operating threshold was selected on the scoring fold.

---

### DRAFT-p2-register-3
- **Repository / SHA:** MLCryptoEngine / 5359a11fc753cdcd2606aea991dae826293d0307
- **Hypothesis or artifact:** D1 — the shipped clearance scorer, and the selection correction its sibling result received and it did not.
- **Direction:** B
- **Class:** UNSUPPORTED_POSITIVE
- **Severity:** S2
- **Label:** READ
- **Claim challenged (verbatim quote):** "| **Limitations** | Detects **hard rugs only** — the blatant case. Says nothing about soft/slow rugs (that is D2). In the wild ~99% of launches are scam-adjacent, so it filters a small honest minority, not a general classifier — read a score against that base rate. |" — MLCryptoEngine/HYPOTHESES.md:241.
- **Evidence:**
  - The pool set D1 is measured on is the **reachability-selected** C.23 set. The project measured that selection: "`getSignaturesForAddress` paginates backward from *now*, so reaching a 2024 launch costs O(the pool's full history). Hard rugs are shallow … and honest survivors are deep … **Reconstruction cost therefore correlates with the label** — the affordable honest sample is biased toward *faded* pools and depleted of thriving survivors" (MLCryptoEngine/DECISIONS.md:2127-2134, ADR-051). It measured the magnitude: "C.25 Task 2 measured that exclusion at **57% of the honest class**" (MLCryptoEngine/DECISIONS.md:2172-2174, ADR-053), confirmed at MLCryptoEngine/report.md:3762-3764 (8 of 14 randomly drawn honest pools deep or unreached).
  - On the sibling result the same correction **halved the effect**: "On the corrected sample the C.24 lift **halved** (6h v0 +0.115 → +0.047): half of it was the reachability bias" and "the **high-activity extreme lift collapsing (+0.156 → +0.015)** — the stratum that carried C.24's headline was a selection artifact" (MLCryptoEngine/DECISIONS.md:2192-2195). D2's register entry carries this: "The C.24 magnitude was **reachability-inflated** — half the lift was the excluded 57% of deep honest pools" (MLCryptoEngine/HYPOTHESES.md:255). **D1's entry (HYPOTHESES.md:241) does not mention it at all.**
  - D1 was never re-measured on the corrected sample, although the project states the correction is now cheap and the sample exists: "**Method B lifts the from-now pagination wall**, so an unbiased Solana launch-window sample is affordable for the first time, at ~33 credits/pool" (MLCryptoEngine/report.md:3842-3844); the corrected sample reached 258 honest pools (report.md:3774, 3923). C.25's and C.26's result tables carry only behavioural rows on the corrected sample (report.md:3795-3799, 3941-3945); the C.23 launch-window figures are re-quoted, not re-run, in the track's closing inventory ("hard rugs separate cleanly there (0.984)", MLCryptoEngine/report.md:3982).
  - The asymmetry matters because the shipped artifact is the one an outside party would act on, and it is the one carrying the uncorrected number.
- **Recomputation (if any):** none — this is a comparison of what was corrected against what was shipped.
- **What would resolve it:** Re-score the launch-window scorer on the Method-B depth-independent sample (the T0…T0+30 min slice is a subset of the 6 h window already retrieved for C.25/C.26) and publish the corrected clearance precision, or add the 57%-of-the-honest-class selection to D1's Limitations row as D2's row carries it.
- **Confidence:** MEDIUM-HIGH — that the bias exists and was measured is certain and quoted; the *direction* of its effect on a launch-window (rather than behavioural) classifier is not established by the repository, which is itself the point: it was not measured.
- **Invalidated by later commits?:** no — the detection track concluded at C.26/ADR-054 and nothing after the anchor re-measures it.
- **Disclosed by authors?:** The bias is disclosed prominently for **D2** (HYPOTHESES.md:255, ADR-051, ADR-053) and in C.24's verdict prose ("the measured sample is conservatively biased toward faded-honest pools", MLCryptoEngine/report.md:3673). It is **absent from D1's register entry, from D1's shipped scope note, and from the track's closing inventory of D1**.

---

### DRAFT-p2-register-4
- **Repository / SHA:** MLCryptoEngine / 5359a11fc753cdcd2606aea991dae826293d0307
- **Hypothesis or artifact:** D2 — "Honest-versus-slow-rug separation", carried in the register as a qualified positive and counted as one of "the project's first two substantive positives".
- **Direction:** B
- **Class:** UNSUPPORTED_POSITIVE
- **Severity:** S2
- **Label:** DERIVED
- **Claim challenged (verbatim quote):** "**Concluded, not closed-absent** — the signal is real in direction but small and its confirmation is priced out." — MLCryptoEngine/HYPOTHESES.md:257; and "It has produced the project's first two substantive positives." — MLCryptoEngine/HYPOTHESES.md:228-229.
- **Evidence:**
  - The deciding figure at the anchor is the C.26 mid-stratum lift: "**+90 more pools moved the mid-stratum estimate DOWN to +0.032 (SE 0.039, 95% CI [−0.045, +0.109])**" at n = 103 (MLCryptoEngine/HYPOTHESES.md:253; source MLCryptoEngine/report.md:3944-3949). That is **0.82 SE from zero**, one-sided p ≈ 0.21.
  - The report adds an operating-point qualifier the register drops: the +0.032 is measured "at recall 0.939 (**near base-rate operating point**)" (MLCryptoEngine/report.md:3949) — i.e. at a threshold that clears almost everything, not the registered selective recall ≥ 0.50 point.
  - The registered test was not the test that ran. C.25 Task 0 rule 2 reads: "The C.24 positive is recorded as **surviving** the unbiased sample iff, at the 6h cutoff on the depth-corrected sample, **behavioural decon lift** over base is **> 0.02** *and* precision clears **0.60 at recall ≥ 0.50**" (MLCryptoEngine/report.md:3700-3706). The delivered test substituted the **v0 (un-decontaminated)** labels — "the corrected-sample bar runs on **v0 labels**" (MLCryptoEngine/report.md:3783-3785) — which the project's own ADR-048 identifies as the label version that mis-scores the target class ("The honest_candidate class is an upper bound; a model punished for correctly flagging an unlabeled soft rug is being scored against wrong ground truth", MLCryptoEngine/DECISIONS.md:2031-2033). On the anchored feature matrix, decontamination reclassifies **20 of the 117** v0-honest test-fold pools (17.1%) as `soft_rug` (`data/processed/detection/features_c23.csv`, read 2026-09-12 18:18 UTC).
  - The bar the positive is judged against contains **no significance requirement at all**: "genuine discrimination requires the mid lift **> 0.02 and ≥ half the overall lift**" (MLCryptoEngine/DECISIONS.md:2186-2187; report.md:3723-3726). Because the clause is relative to the *overall* lift, each correction that shrank the overall effect made the mid-stratum clause easier: at C.24's biased overall lift of +0.115 the mid lift of +0.045 would have failed "≥ half the overall"; at C.26's overall +0.043 the mid lift of +0.032 passes.
  - **18 cells were scored with no multiplicity correction**: "18 cells were scored (3 cutoffs × 3 sets × 2 labels)" (MLCryptoEngine/report.md:3639-3640). The same repository corrects 1,653 pairs with Benjamini–Hochberg (H4, HYPOTHESES.md:98-99), 12 momentum cells with a deflated Sharpe (H9, HYPOTHESES.md:147), 40 medium-horizon cells likewise (H11, HYPOTHESES.md:181), and makes the three-number reporting rule standing policy in ADR-030 (DECISIONS.md:1322-1327). The detection track's exemption is structural, not evidential: ADR-044 (DECISIONS.md:1929-1964).
  - The trend across corrections points at zero, not at a real effect: overall 6 h v0 lift +0.115 (biased) → +0.047 (depth-unbiased) → +0.043 (firmed); mid stratum +0.045 → +0.051 → +0.032 (MLCryptoEngine/report.md:3806-3810, 3941-3945).
- **Recomputation (if any):**
  - Inputs: lift +0.032, SE 0.039, n = 103 (MLCryptoEngine/HYPOTHESES.md:253, report.md:3944-3948); overall firmed lift +0.043 (report.md:3938).
  - Method: z = lift/SE; normal one-sided tail; the registered "≥ half the overall" margin in SE units.
  - Result: **z = 0.821, one-sided p = 0.206, 95% CI [−0.0444, +0.1084]** — matching the published interval. The registered clause is cleared by 0.032 − 0.0215 = **0.0105, i.e. 0.27 SE**. The C.25 figure it replaced was z = 0.80 (p = 0.212).
- **What would resolve it:** State the D2 register verdict in the terms the evidence supports — an effect estimate of +0.032 ± 0.039 that is not distinguishable from zero, on contaminated labels, from a 18-cell scan without correction — rather than "the signal is real in direction", and drop or qualify the count of "two substantive positives".
- **Confidence:** HIGH — every input is quoted from the repository and the arithmetic reproduces the published interval.
- **Invalidated by later commits?:** no — D2 concluded at C.26 (ADR-054) and no later measurement exists at or after the anchor.
- **Disclosed by authors?:** Yes for the uncertainty, and generously: "a confidence interval including zero" (HYPOTHESES.md:253 and report.md:3948), "statistically indistinguishable from zero" (report.md:3953-3954), "measured on **v0**, not decon" (HYPOTHESES.md:255), and the 18 cells (report.md:3639). The finding is not the undisclosed limitation but the **verdict label placed on top of it** — "real in direction", "substantive positive" — and the fact that the register's Limitations row (HYPOTHESES.md:255) carries the CI and the label substitution but not the 18-cell scan or the near-base-rate operating point.

---

### DRAFT-p2-register-5
- **Repository / SHA:** MLCryptoEngine / 5359a11fc753cdcd2606aea991dae826293d0307
- **Hypothesis or artifact:** H6 census (C.27) — the audit A3 clustering correction and the GMX membership decision it drove; the committed evidence artifact `audit/census_ci.json`.
- **Direction:** B
- **Class:** INTERNAL_INCONSISTENCY
- **Severity:** S2
- **Label:** DERIVED
- **Claim challenged (verbatim quote):** "**GMX does not** (+0.288 IID → **−0.070** day-clustered) and should be read as **unresolved, not a survivor**." — MLCryptoEngine/HYPOTHESES.md:198 (same figure at MLCryptoEngine/AUDIT.md:194-195 and MLCryptoEngine/report.md:5149-5152).
- **Evidence:**
  - The committed evidence artifact the claim cites records the **opposite sign** for that statistic: `"GMX": {"net_mean_bps": 0.40443…, "day_cluster_se": 0.19369…, "day_cluster_ci95_lower_bps": 0.028088…, "block_bootstrap_ci90_lower_bps": 0.10088…, "n_days": 7}` — MLCryptoEngine/audit/census_ci.json (GMX block). The audit's own file is `audit/census_ci.py`, and AUDIT.md:7-10 names both as the evidence for A3.
  - The divergence is a tail convention applied in two places at once. `census_ci.py:126` computes `day_cluster_ci95_lower_bps = mean − 1.943 × day_se`, and 1.943 is the **one-sided** t at 6 df. AUDIT.md's table instead reports day-clustered half-widths of 0.7069 (PUMP), 4.7254 (MERL), 0.4740 (GMX), 0.1539 (SOL), 0.2533 (HYPE) (MLCryptoEngine/AUDIT.md:181-185) — all of which equal `2.4469 × day_se`, the **two-sided** t at 6 df.
  - The repository, in the same corrections section, adopts the one-sided convention as the correct reading of this bar: "**A6 — a one-sided bar was judged with a two-sided critical value.** C.27 used `t(0.975)` = 1.96 where a one-sided 95% bound needs 1.645" (MLCryptoEngine/report.md:5155-5157), and the corrected code now uses it: `one_sided = float(student_t.ppf(CONFIDENCE, n - 1)); lower = mean - one_sided * se` and `day_lower = mean - student_t.ppf(CONFIDENCE, clusters - 1) * day_se` (MLCryptoEngine/research/microstructure/registered.py:183-192). Under the convention the repository itself adopts, **GMX's day-clustered lower bound is +0.028 and GMX does not flip**.
  - A second defect inside the same artifact: `census_ci.py:99` back-solves the IID standard error as `(mean − ci95_lower) / 1.6449`, while `registered.py` built that half-width with the two-sided ≈1.9600 (AUDIT.md:166-168 measures `halfwidth·√n/sd = 1.9600` for all ten instruments). The stored `iid_se` is therefore 1.96/1.6449 = **19.16% too large**, and the stored `nw_over_iid` correspondingly too small: the JSON records GMX 1.2761, HYPE 2.3665, PUMP 1.7063 where AUDIT.md's published "NW/IID" column reads 1.5×, 2.8×, 2.0×. The published column is the defensible one (a half-width ratio); the committed artifact's field is not, and the two do not agree.
- **Recomputation (if any):**
  - Inputs: `net_mean_bps`, `day_cluster_se`, `n_days`, `reported_halfwidth_bps`, `newey_west_se`, `iid_se`, `nw_over_iid` per instrument from MLCryptoEngine/audit/census_ci.json; critical values from `scipy.stats.t`.
  - Method: recompute the day-clustered lower bound under both tail conventions; recompute `iid_se` from the reported half-width under 1.96 and under 1.6449; recompute the NW/IID half-width ratio.
  - Result: GMX day-clustered lower bound = **−0.0695** two-sided (the published −0.070) vs **+0.0281** one-sided (the stored field). PUMP +3.5935 / +3.7391; MERL +1.7250 / +2.6981 — PUMP and MERL stay positive under either convention, so **only GMX's verdict turns on the choice**. `iid_se` inflation factor 1.1916 exactly; e.g. PUMP stored 0.019884 vs 0.016687 true; stored `nw_over_iid` 1.7063 vs published half-width ratio 2.0332 (= 1.7063 × 1.1916). Script inline in `/home/kiros-li/.cache/program-audit/scratchpad/work/agentB-MLCryptoEngine-p2/`.
- **What would resolve it:** Recompute the day-clustered bounds with the same critical value as the bar they are compared against, state which tail is intended, and regenerate `audit/census_ci.json` so the committed evidence matches the published table — or record explicitly that GMX's demotion holds only under the two-sided reading that A6 says is wrong for this bar.
- **Confidence:** HIGH — both numbers are in the repository and the constants that produce them are in the committed source (`census_ci.py:99,126`).
- **Invalidated by later commits?:** no — AUDIT.md is frozen by its own statement ("This file is the frozen audit record as delivered against commit `ed786ce`", MLCryptoEngine/AUDIT.md:18-20), and the anchor is the last commit.
- **Disclosed by authors?:** no — no document notes that the day-clustered figures use a different tail than the A6-corrected bar, and no document notes the disagreement between `audit/census_ci.json` and AUDIT.md's table. The A6 correction itself is disclosed at report.md:5155-5160 and AUDIT.md:264-278.

---

### DRAFT-p2-register-6
- **Repository / SHA:** MLCryptoEngine / 5359a11fc753cdcd2606aea991dae826293d0307
- **Hypothesis or artifact:** H1 — the "no hidden selection filter" leg of the closure, as carried in the register and in the shipped README-linked note.
- **Direction:** B
- **Class:** STALE_FIGURE
- **Severity:** S3
- **Label:** DERIVED
- **Claim challenged (verbatim quote):** "**The best top-confidence decile anywhere in the study captures 5.00 bps, against an 80 bps round trip — missing the economic bar by 16×.**" — MLCryptoEngine/docs/notes/h1-predictability-without-capturability.md:99-101; identically at MLCryptoEngine/HYPOTHESES.md:54 ("the best decile in the study captures **5.00 bps against 80 bps** — missing the economic bar by 16×") and MLCryptoEngine/report.md:2328-2330, :2471.
- **Evidence:**
  - The 5.0020 bps figure is the **Kraken** BTC/USD 900 s top decile: it sits in the table headed "**Kraken BTC/USD, 6 days, 165,075 samples**" (MLCryptoEngine/report.md:2289-2298, value at :2298), and the note reproduces the same Kraken table with the same value (MLCryptoEngine/docs/notes/…:52-59). The note's own sources table attributes "top-decile 0.0720 → 5.0020 bps" to that Kraken per-horizon table (docs/notes/…:301).
  - ADR-055 corrected Kraken's base tier on 2026-08-08: "The Kraken maker round trip falls **80 → 50 bps**" (MLCryptoEngine/DECISIONS.md:2258), and the register's cost table now reads "Kraken spot, base tier | 25 bps | **50 bps** | 2026-08-08" (MLCryptoEngine/HYPOTHESES.md:305). ADR-055 also states where the correction was propagated — "`venues.yaml`, the HYPOTHESES venue-cost table, and the external-corroboration section" (DECISIONS.md:2263-2266) — a list that does not include the C.14 decile framing.
  - The shipped note therefore contradicts itself within twenty lines: §3 prints "Kraken spot, base tier | 25 bps | **50 bps**" (docs/notes/…:77) and uses it correctly for the 100 ms figure ("misses its own venue's floor by roughly **1,700×**", :81-82 — 50/0.0291 = 1,718); §4 then charges the same venue's decile against 80 bps.
  - ADR-065's pinning test (`tests/test_note_honesty.py`) asserts the note's figures match the register in both directions (DECISIONS.md:2617-2622), so the stale "80 bps / 16×" pair is now pinned by test into the project's only outside-reader artifact.
- **Recomputation (if any):**
  - Inputs: top decile 5.0020 bps (MLCryptoEngine/report.md:2298); Kraken round trip 50 bps (MLCryptoEngine/HYPOTHESES.md:305, DECISIONS.md:2258); the quoted 80 bps.
  - Method: divide round trip by capture.
  - Result: 80/5.0020 = **15.99×** (the published 16×); **50/5.0020 = 10.00×**. The published miss factor is overstated by **1.6×** against the venue the figure was measured on.
- **What would resolve it:** Restate the C.14 decile comparison against the venue the decile was measured on (Kraken, 50 bps round trip → 10×), or state explicitly that the 80 bps is Coinbase's and that the decile figure is Kraken's, in all three places the pair appears.
- **Confidence:** HIGH — table attribution and arithmetic are both unambiguous; the only residual risk is if an untabulated Coinbase decile also equalled 5.00 bps, which no table in the repository shows.
- **Invalidated by later commits?:** no — the note was added at 2026-08-22 (ADR-065) after ADR-055, so the staleness was carried forward rather than predating the correction.
- **Disclosed by authors?:** no — the corrected Kraken figure is disclosed (ADR-055, HYPOTHESES.md:305) but the consequence for the decile framing is nowhere noted, and ADR-055 asserts "**No closure flips**" and enumerates the places the correction landed without this one.

---

### DRAFT-p2-register-7
- **Repository / SHA:** MLCryptoEngine / 5359a11fc753cdcd2606aea991dae826293d0307
- **Hypothesis or artifact:** H6 — the D.1a / D.1c confidence intervals that remain in the permanent register after audit finding A3.
- **Direction:** B
- **Class:** STATISTICAL
- **Severity:** S3
- **Label:** DERIVED
- **Claim challenged (verbatim quote):** "**300/900 s adverse:** the sign holds — PUMP +4.17/+4.49 (CI lower +4.04/+4.28), MERL +6.06/+6.08 (CI +5.45/+5.21), both halves positive" — MLCryptoEngine/HYPOTHESES.md:204; and "the **always-last-in-queue** pessimistic net stays positive on both — **PUMP +2.15 (CI +2.00), MERL +5.42 (CI +4.88)** — a *measured* quantity" — MLCryptoEngine/HYPOTHESES.md:203.
- **Evidence:**
  - A3's diagnosis is that per-print `spread − adverse − 3.0` rows are serially dependent because consecutive trades share overlapping forward windows, so the IID standard error understates: "PUMP's reported ±0.03 bps is really ±0.07 under HAC and ±0.71 under day clustering. The stated precision is overstated by roughly an order of magnitude" (MLCryptoEngine/AUDIT.md:187-189); measured inflation factors 1.4–3.6× (NW) and 3.3–28.1× (day-clustered) across ten instruments (AUDIT.md:181-185).
  - The correction was applied to **one module**. `research/microstructure/registered.py` now computes `_day_clustered_se` and emits `ci95_lower_bps_day_clustered` and `se_day_clustered_bps` (MLCryptoEngine/research/microstructure/registered.py:155-209), and report.md:5145-5147 says so.
  - The intervals quoted at HYPOTHESES.md:204 come from a different module that was **not** corrected. `d1c.py` uses "`HorizonNet` for the 10 thin census instruments — does the census sign hold at 300 s and 900 s?" (MLCryptoEngine/research/microstructure/d1c.py:8-9), and `HorizonNet.summary` computes `se = math.sqrt(variance / w.n)` with `crit = student_t.ppf(0.5 + CONFIDENCE / 2, w.n - 1)` and returns `ci95_lower_bps = w.mean - crit * se` — MLCryptoEngine/research/microstructure/horizons.py:129-134. There is no day-clustered field, no HAC, no cluster count anywhere in that file.
  - The horizons involved are **300 s and 900 s**, five to fifteen times longer than the 5 s and 60 s windows A3 named as "textbook overlapping observations" (MLCryptoEngine/AUDIT.md:154-157), so the understatement is strictly larger there, not smaller. The corresponding table is MLCryptoEngine/report.md:4485-4486 ("PUMP | 499,914 | … **+4.17 (+4.04)** | **+4.49 (+4.28)**").
  - Neither AUDIT.md nor the D.1d corrections section extends A3 past the census: "Which result it changes. The stated precision of every C.27 number, and one membership decision" (MLCryptoEngine/AUDIT.md:191-192); "Applied to `research/microstructure/registered.py`" (MLCryptoEngine/report.md:5136).
- **Recomputation (if any):**
  - Inputs: the census day-clustered inflation factors for PUMP and MERL at the *shorter* horizons — PUMP day-clustered SE 0.2889 vs IID half-width 0.0327, MERL 1.9311 vs 0.3807 (MLCryptoEngine/audit/census_ci.json); the D.1c reported half-widths, e.g. PUMP 900 s 4.49 − 4.28 = 0.21 bps, MERL 900 s 6.08 − 5.21 = 0.87 bps (MLCryptoEngine/HYPOTHESES.md:204).
  - Method: apply the census-measured day-clustering factors (PUMP 17.3×, MERL 9.9× on the half-width; AUDIT.md:181-182) as an order-of-magnitude indication for the same instruments at longer horizons.
  - Result: PUMP's 900 s interval of ±0.21 bps would widen to roughly ±3.6 bps and MERL's ±0.87 to roughly ±8.6 bps — both still leaving a positive point estimate but no longer a lower bound "positive at both halves" in the precision the register claims. This is an indication, not a measurement: the correct figures require re-running `HorizonNet` with a clustered SE, which is why it is what would resolve the finding.
- **What would resolve it:** Add the day-clustered (or HAC) interval to `horizons.py` as was done for `registered.py`, re-run D.1c's 300/900 s pass, and restate HYPOTHESES.md:203-204 with the corrected intervals — or annotate those cells as IID intervals carrying A3's 2–28× caveat.
- **Confidence:** HIGH on the omission (the code is unambiguous); MEDIUM on the magnitude, which is extrapolated from the census factors rather than recomputed.
- **Invalidated by later commits?:** no — `horizons.py` is unchanged at the anchor, which is the final commit.
- **Disclosed by authors?:** no — AUDIT.md's coverage table lists `horizons.py` among the modules covered only by `test_d1c.py` (MLCryptoEngine/AUDIT.md:559) but nowhere states that A3's correction does not reach it, and the register's D.1c row presents the intervals without caveat. H6 closed negative, so no conclusion turns on this; the overstated precision sits in the permanent record.

---

### DRAFT-p2-register-8
- **Repository / SHA:** MLCryptoEngine / 5359a11fc753cdcd2606aea991dae826293d0307
- **Hypothesis or artifact:** H6 — the "pre-registered" framing of the census positive.
- **Direction:** B
- **Class:** PROVENANCE
- **Severity:** S3
- **Label:** DERIVED
- **Claim challenged (verbatim quote):** "**The census (H6) resolved at C.27 to the project's first pre-registered-bar-clearing positive**" — MLCryptoEngine/HYPOTHESES.md:8-9; registration cell: "**Fixed in progress.md commit 6025f5c (2026-08-06), before the scored window closes**: window 2026-08-04→08-11" — MLCryptoEngine/HYPOTHESES.md:201.
- **Evidence:**
  - Registration commit: `6025f5c` — "docs: pre-register the H6 thin-perp census bars before the scored window closes", author date **2026-08-06 12:18:06 −0700 = 2026-08-06 19:18:06 UTC**; its body states "Window, economics bar, BH multiplicity, sample floor, halves robustness, capacity tiering, the upper-bound statement and the outcome-to-action map **all fixed before the data exists**" (`git -C /home/kiros-li/Documents/GitHub/MLCryptoEngine log -1 6025f5c`, read 2026-09-12 18:10 UTC). The same wording heads the registration in progress.md ("Stage C.18: thin-perp census bars, registered before the data exists", MLCryptoEngine/progress.md:2071 — primary evidence outside my assignment).
  - The scored window opens at `SCORED_START_NS = 1_785_801_600_000_000_000` = **2026-08-04T00:00:00Z** (MLCryptoEngine/research/microstructure/registered.py:50). Registration is therefore **2.80 of the 7 scored days (40.1%) after the window opened**.
  - The data for those days was on disk before registration. `data/raw/venue=hyperliquid/date=2026-08-04/` holds 24 complete hour partitions and `date=2026-08-05/` likewise, with file mtimes running from 2026-08-03 18:00 to **2026-08-05 17:00 local (= 2026-08-06 00:00 UTC)**, i.e. 19 hours before the registration commit (live working tree, read-only, read **2026-09-12 18:20 UTC**; untracked, may have changed since the anchor).
  - The instrument set was itself a spread-motivated screen taken three days earlier: "retrieved 2026-08-03, 177 live perps … PUMP rank 6 $31M/day impact 4.47 bps **first above cost**" (MLCryptoEngine/config/venues.yaml:129-139). The repository later demotes the survivors on exactly this ground: "the C.9 pick was a **spread-motivated screen** … survivors demote to **screened positives**; BH corrected the 10 tested, not the 177 screened" (MLCryptoEngine/HYPOTHESES.md:204).
  - AUDIT.md's clean finding on pre-registration tests a narrower property: "Every `docs: pre-register` commit precedes its `feat:` results commit … no registered threshold edited" (MLCryptoEngine/AUDIT.md:492). That is true and is not the same as "before the data exists".
- **Recomputation (if any):**
  - Inputs: `SCORED_START_NS` (registered.py:50) and `git log -1 --date=iso 6025f5c`.
  - Method: elapsed seconds from window open to commit, divided by window length.
  - Result: 2026-08-06T19:18:06Z − 2026-08-04T00:00:00Z = **2.8042 days of 7.0000 = 40.06%** of the scored window already recorded at registration.
- **What would resolve it:** Restate the H6 headline as "bars registered after 2.8 of 7 scored days had been recorded but before the thin instruments were read", which is what the registration body actually claims ("the ten thin instruments have not been read and stay untouched until the census runs", MLCryptoEngine/progress.md:2074-2075), and drop "before the data exists" from the commit-level claim quoted in the register's framing.
- **Confidence:** HIGH for the timing arithmetic; the narrower claim that the instruments were not *read* is unverifiable either way and I make no assertion against it.
- **Invalidated by later commits?:** no — the commit and the constant are both at or before the anchor.
- **Disclosed by authors?:** Partly. HYPOTHESES.md:201 says "before the scored window **closes**", which is honest and precise, and the registration body limits its claim to the instruments not having been read. The commit subject line's "before the data exists", the progress.md heading, and the register's unqualified "pre-registered-bar-clearing positive" framing are not so limited.

---

### DRAFT-p2-register-9
- **Repository / SHA:** MLCryptoEngine / 5359a11fc753cdcd2606aea991dae826293d0307
- **Hypothesis or artifact:** H6 / D.1d — ADR-056's binding precondition on any D.1 number, and ADR-062 which replaced it.
- **Direction:** B
- **Class:** PROCESS
- **Severity:** S4
- **Label:** DERIVED
- **Claim challenged (verbatim quote):** "Two conditions bind any D.1 number: the **Hyperliquid latency gap** must be closed first (telemetry probes only kraken/coinbase; a constant assumption overstates, ADR-003), and the **one-week** census sample must extend to **≥ 4 weeks across regimes**" — MLCryptoEngine/DECISIONS.md:2294-2297 (ADR-056, dated 2026-08-11).
- **Evidence:**
  - D.1d ran on **one week** with a **proxy** latency: "Under always-last queue with cancel/replace latency (162 ms proxy floor each way)" (MLCryptoEngine/HYPOTHESES.md:197); "Every figure rests on the single census week (2026-08-04→08-11)" (MLCryptoEngine/HYPOTHESES.md:205).
  - ADR-062 re-specifies the first precondition — "Latency enters a simulation as a **floor plus a declared sensitivity grid**" — and is explicit that the floor is not the quantity ADR-056 asked for: "a POST to the info endpoint exercises the same host/TLS/HTTP front end an order traverses but omits gateway queueing and matching, and the true path cannot be measured without placing an order. Using that floor as *the* latency would understate exactly the term ADR-003 exists to protect" (MLCryptoEngine/DECISIONS.md:2478-2487).
  - **ADR-062 first appears in the results commit itself.** `git log -S "ADR-062: Latency is a measured proxy floor" -- DECISIONS.md` returns exactly one commit: `ed786ce`, 2026-08-11 23:16:42 −0700, "feat: D.1d — the capture does not survive an order-lifecycle fill model; H6 closes" (live repo, read-only, read 2026-09-12 18:11 UTC). Its Consequences section already reports the outcome ("D.1d found **no zero-crossing exists**", DECISIONS.md:2493), so it was written with the result in hand.
  - ADR-056 is not marked superseded or amended by it, against DECISIONS.md's own rule: "Never rewrite an accepted decision; if a decision is reversed, add a new entry that supersedes it and links back" (MLCryptoEngine/DECISIONS.md:3-4). ADR-018 shows the project doing this properly ("**Supersedes:** ADR-016", DECISIONS.md:645).
  - The outstanding readout is later declared irrelevant rather than run: "the Hyperliquid latency distribution (2026-08-19, **moot for the sign**)" (MLCryptoEngine/HYPOTHESES.md:264); "The 2026-08-19 accrued distribution re-run is recorded as a for-the-record follow-up rather than a decision gate, because the sign cannot move" (DECISIONS.md:2499-2501).
  - For completeness, the *other* ADR-056 precondition was registered asymmetrically **in advance**, which I verified rather than assumed: the standing caveat "A **negative bounded D.1 closes the thin tail (and H3) completely**; a positive one is the first thing worth simulating for real capital" (HYPOTHESES.md:205) first appears in `8b6fbc7`, 2026-08-11 00:57:01 −0700 — the same commit as ADR-056 and 22 hours before the D.1d result. That asymmetry is therefore pre-registered and I raise no finding on it.
- **Recomputation (if any):** none — commit-order evidence only.
- **What would resolve it:** Record ADR-062 as amending ADR-056's precondition, with the date and the fact that it was written alongside the result it licensed; or run the 2026-08-19 distribution and report it as the precondition required.
- **Confidence:** HIGH — the commit containing ADR-062 is the results commit, verified by `git log -S`.
- **Invalidated by later commits?:** no — no commit after `ed786ce` restores or supersedes ADR-056's precondition.
- **Disclosed by authors?:** Partly — the proxy nature of the 162 ms floor is disclosed prominently (ADR-062, HYPOTHESES.md:197) and the sensitivity grid is arguably a stronger control than a point distribution. What is not disclosed is that ADR-056's stated precondition for *any* D.1 number was replaced in the same commit as the number.

---

### DRAFT-p2-register-10
- **Repository / SHA:** MLCryptoEngine / 5359a11fc753cdcd2606aea991dae826293d0307
- **Hypothesis or artifact:** ADR-061 — the standing rule on order-lifecycle evaluation, and the robustness figure it rests on.
- **Direction:** B
- **Class:** STALE_FIGURE
- **Severity:** S4
- **Label:** READ
- **Claim challenged (verbatim quote):** "A closure has to survive the removal of the rule it could most plausibly be accused of resting on; this one does." preceded by "**deleting every crossing fill outright still leaves both negative** (−3.98 / −2.57)." — MLCryptoEngine/DECISIONS.md:2469-2471.
- **Evidence:**
  - Audit A2 showed those two numbers were produced by invalid arithmetic and are wrong: "**−3.98** … **−2.57** … were obtained by subtracting the crossing rows from the totals. That is invalid twice over: the edge was recomputed on the *reduced* notional while inventory and fees were carried over from the *full* notional, and the ledger is path dependent … Re-run properly … the answer is **PUMP −4.35, MERL −2.13**" (MLCryptoEngine/report.md:4925-4932; full finding at MLCryptoEngine/AUDIT.md:99-137, which adds that the method "discredits the method that produced them").
  - The register was corrected: "**−4.35 / −2.13**; the −3.98 / −2.57 originally recorded here was arithmetic on a path-dependent ledger with mixed denominators — audit A2, re-run properly" (MLCryptoEngine/HYPOTHESES.md:197). report.md's D.1d section carries a supersession banner and an in-place correction box (report.md:4799-4807, 4925-4932).
  - `DECISIONS.md` carries no banner, no correction, and no cross-reference: ADR-061 still states the discredited pair, and the two audit-driven ADRs written the same day (ADR-063 on the gate, ADR-064 on the mechanism, DECISIONS.md:2505-2574) address A1 and A13 but not A2.
  - This matters because DECISIONS.md is the document a future session is instructed to read first: "`DECISIONS.md` — append-only architecture decision log; read before revisiting any settled question" (MLCryptoEngine/CLAUDE.md:196-197).
- **Recomputation (if any):** none — the correct figures are the repository's own re-run (report.md:4931-4932, AUDIT.md:120-126).
- **What would resolve it:** Append a one-line ADR (or a dated amendment note in ADR-061, which the log already does elsewhere — see ADR-013's "Amended 2026-08-01 … by measurement", DECISIONS.md:409-412) recording that the −3.98 / −2.57 pair was re-run to −4.35 / −2.13.
- **Confidence:** HIGH — both figures and the correction are in the repository.
- **Invalidated by later commits?:** no — the anchor is the final commit.
- **Disclosed by authors?:** Yes, elsewhere and clearly — the correction is disclosed at HYPOTHESES.md:197, AUDIT.md:99-137 and report.md:4925-4932. Only the ADR is uncorrected and uncross-referenced. Raised as hygiene, not as a discovery.

---

### DRAFT-p2-register-11
- **Repository / SHA:** MLCryptoEngine / 5359a11fc753cdcd2606aea991dae826293d0307
- **Hypothesis or artifact:** HYPOTHESES.md's summative sections, and ADR-044's boundary rule.
- **Direction:** B
- **Class:** INTERNAL_INCONSISTENCY
- **Severity:** S4
- **Label:** READ
- **Claim challenged (verbatim quote):** "**Five strategy hypotheses have been tested to a standard that permits closing them.**" — MLCryptoEngine/HYPOTHESES.md:455-456; and "Five tests, no deployable strategy." — MLCryptoEngine/HYPOTHESES.md:525; against "this register — which documents, to a standard each entry could be closed on, why **nine strategy families** do not work" — MLCryptoEngine/HYPOTHESES.md:568-570.
- **Evidence:**
  - The "Established" section enumerates only the first five entries ("Three closed because a real cost exceeded a real edge; one closed because removing the cost constraint revealed no edge; one is a genuine but decayed income stream", HYPOTHESES.md:457-459) and the "An honest reading" section still says "two of them (H1's AUC 0.596, H5's 8% on capital) did produce measurable effects" (HYPOTHESES.md:527-528) — text written when the register held five entries and not updated as H8, H9, H11 and H6 closed.
  - The same file's own preamble and conclusion claim nine: "Eleven entries stand: nine tested and closed" (HYPOTHESES.md:7-8) and "nine hypotheses tested and closed on measured figures" (HYPOTHESES.md:543). ADR-043 acknowledges the drift in passing — "that five, then nine closures are evidence about those hypotheses" (DECISIONS.md:1924-1926) — without reconciling the register's sections.
  - The warrant does not transfer cleanly: the Established section vouches for five to "a standard that permits closing them", while the conclusion extends the same warrant to nine, including H6, whose closure rests on one census week that ADR-056 declared insufficient for any D.1 number (DECISIONS.md:2296-2297) and whose replay "has still only run once with no second pair of eyes" (DECISIONS.md:2538; same statement at report.md:5105-5106).
  - Separately, ADR-044's consequence — "HYPOTHESES.md remains the alpha register and **gains no detection entries**" (MLCryptoEngine/DECISIONS.md:1958-1959) — is contradicted by the register itself, which now carries a "Detection track (off the alpha register — ADR-044)" section with the D1 and D2 entries (HYPOTHESES.md:225-257). No superseding ADR records the reversal, against DECISIONS.md:3-4.
- **Recomputation (if any):** Counting the register: H1, H2, H3, H4, H5, H6, H8, H9, H11 = 9 closed on measured figures; H10 closed as untestable; H7 closed by decision; total 11 (HYPOTHESES.md:42-220). "Five" matches the register as it stood before H8 (2026-08-05).
- **What would resolve it:** Update the "Established" and "An honest reading" sections to the current count, and append an ADR recording that the register now carries the detection entries in a clearly separated section.
- **Confidence:** HIGH — a direct count of the file against its own prose.
- **Invalidated by later commits?:** no.
- **Disclosed by authors?:** no — neither the stale count nor the ADR-044 departure is flagged in either file; ADR-043's "five, then nine" phrasing is the closest thing to an acknowledgement.

---

### DRAFT-p2-register-12
- **Repository / SHA:** MLCryptoEngine / 5359a11fc753cdcd2606aea991dae826293d0307
- **Hypothesis or artifact:** H6 — GMX, and the registered outcome-to-action map.
- **Direction:** B
- **Class:** PROCESS
- **Severity:** S4
- **Label:** READ
- **Claim challenged (verbatim quote):** "**No alpha hypothesis remains open and no live next step exists on the strategy side.**" — MLCryptoEngine/HYPOTHESES.md:15-16 (repeated at :262-263).
- **Evidence:**
  - The registered outcome map assigns an action to exactly the bucket GMX was later moved into: "| survivors within noise of zero | **extend recording 30 days and re-run under these same bars** — no building |" (MLCryptoEngine/progress.md:2121 — primary evidence outside my assignment; the map is summarised in my documents at HYPOTHESES.md:201, "Outcome-to-action map registered, from 'H6 closes, zero open items' through 'D.1 fill-simulation input, not a strategy'").
  - GMX was moved into that bucket by the audit correction: "**GMX does not** (+0.288 IID → **−0.070** day-clustered) and should be read as **unresolved, not a survivor**" (MLCryptoEngine/HYPOTHESES.md:198).
  - The registered action was not executed. The blind re-run carries only "PUMP and MERL … never counted as blind picks" plus 25 blind picks (MLCryptoEngine/DECISIONS.md:2388-2393, ADR-059; MLCryptoEngine/config/venues.yaml:156-162), and the six pre-D.1b census instruments including GMX "leave the live subscription" (config/venues.yaml:161-162). Recording ended 2026-08-13 (DECISIONS.md:2583), so the 30-day extension is no longer possible.
  - Note the finding is narrow: H6 closed on the D.1d fill model rather than on the census bucket, so nothing in the project's verdict depends on GMX. What is unearned is the completeness claim — "zero open items" — while one registered action stands unexecuted and now unexecutable.
- **Recomputation (if any):** none.
- **What would resolve it:** Record GMX's unresolved status and the unexecuted registered action as a named open item, or state why the D.1d closure supersedes the census outcome map for an instrument that never entered D.1.
- **Confidence:** MEDIUM — the map's bucket wording is unambiguous, but a reasonable reading is that D.1d's closure of H6 discharges every census-level action.
- **Invalidated by later commits?:** no — recording ended before the anchor.
- **Disclosed by authors?:** no — the register reports "zero open items" on the strategy side without noting the unexecuted GMX action. The GMX demotion itself is disclosed at HYPOTHESES.md:198.

---

## What I checked and found sound

These are places where I expected the Direction-B thesis to hold and it did not.

- **Pre-registration order, generally.** Every `docs: pre-register` commit I checked precedes its results commit: `370ba41` (C.17 bars, 2026-08-06 07:02) before the C.17 result; `a2d7466` (C.14 thresholds, 2026-08-04 23:47) before C.14; `88b69d8` (C.16 momentum grid, 2026-08-05 22:09); `902d2e6` (detection bars, 2026-08-06 19:05) before the first detection model; `4bde24c` (blind universe rule and seed, 2026-08-11 21:43) before the 2026-08-12 retrieval; `6a17edf` (D.1d policy, 2026-08-11 22:46) before `ed786ce` (22:46 vs 23:16). AUDIT.md:492 reports the same and it reproduces.
- **A registered bar that was mis-specified was reported as mis-specified rather than rewritten.** C.14's rho gate was written as `rho ≥ 0.10` and the code tested `max|rho|`; the code was corrected to match the registered text, not the reverse (commit `5430eba`, 2026-08-05 00:17), and the outcome is reported as "INCONCLUSIVE on both venues" under the bar as written (MLCryptoEngine/report.md:2311-2322). That is the opposite of a rescued verdict.
- **The A4 correction the audit named as decisive was actually run, and it moved the number the predicted way.** AUDIT.md:620-640 nominates correcting the sweep rule and predicts the net will become more negative; the correction landed and did: PUMP −4.7503 → −4.8087, MERL −4.2314 → −4.3459, with the less-pessimistic variant also negative (MLCryptoEngine/report.md:5048-5052). The stated stop condition (net moving toward zero by more than ~1 bp) was checked and not triggered.
- **The audit's own findings were acted on rather than absorbed.** A1 produced ADR-063 and a replacement differential gate that itself caught a defect (`_refresh_queue` shrinking queue-ahead for in-flight orders, report.md:5097-5101); A13 produced ADR-064 and the withdrawal of the mechanism claim from report.md, HYPOTHESES.md and the shipped `PerformanceReport`; A12 was changed from a `0.0` coercion to a raise. A5 was measured to have literally zero effect and that measurement was published (report.md:5069-5083).
- **A10 (the unsourced maker fee) was fixed without overclaiming.** The three literals became one sourced statement with `ROUND_TRIP = 2 × MAKER` derived, and the honest label was kept: "this is a **documented** figure, not a measured one … the weakest input in the chain" (MLCryptoEngine/report.md:5169-5175).
- **"100.00% coverage outside gaps" is not a tautology.** I suspected the metric was true by construction; the same metric reads 0.03%, 4.63% and 19.39% on failing days (MLCryptoEngine/report.md:53, 383, 240), so it can and does fail.
- **The union-before-summing and clock-ordering rules are honoured where they matter,** including `data/databento/session.py:70` and `research/stream/reader.py:183` (AUDIT.md:494), and `exchange_ns` is persisted but never ordered on (AUDIT.md:495).
- **AUDIT.md's scope limit is stated, not buried.** "the Phase-B and detection-track hypotheses (H1, H2, H4, H5, H8–H11) … are **unaudited**, not clean" appears twice (MLCryptoEngine/AUDIT.md:535-539, 642-647) and is carried into the shipped note's Scope section (docs/notes/…:210-218) and into ADR-065 (DECISIONS.md:2636-2641). I looked for the verdict "No" being quoted without its scope and did not find it.
- **The D.1a "GO" decision names the branch it passed on.** ADR-056 records "GO against D.1a's registered bar via §2 (pessimistic-positive), **not** §1 (estimability, which failed)" (DECISIONS.md:2291-2292) rather than presenting a clean pass.
- **H5's and H8's positives are framed against their own favourable samples.** H5's "8.07% (ETH) and 8.00% (BTC)" is paired in the same cell with "the yield has decayed ~85%" and "**At 2026 funding levels the trade does not clear cash at all**" (HYPOTHESES.md:114), and the Limitations row leads with "**Contains no full bear market** … every Hyperliquid figure is drawn from a favourable sample" (HYPOTHESES.md:116). ADR-033 names the stage "the most dangerous kind of result the project has produced: a marginal positive" (DECISIONS.md:1473-1478). I could not find a place where the 8% figure travels without that qualifier.
- **The C.26 "firming weakened it" reading is conservative relative to its own registration.** The registered noise floor said "A change in the 6h mid-stratum lift of ≤ 0.02 is noise" (report.md:3881-3884); the observed change was −0.019, i.e. inside the floor, and the project still read it against itself ("C.25's +0.051 was optimistic", report.md:3951-3952).
- **The blind-universe rule is genuinely blind in code.** "the code reads exactly `name`, `isDelisted`, `dayNtlVlm`, pinned by a decoy-perturbation test", seed committed with the rule, PUMP and MERL explicitly excluded from the blind count (DECISIONS.md:2386-2393, config/venues.yaml:150-162).
- **Fee-schedule perishability is treated as a standing hazard, not a one-off,** and ADR-016's withdrawn MBT conclusion is left unedited as the record of how the misreading happened (DECISIONS.md:695-698) — the opposite of a rescued verdict.
- **H4's and H9's and H11's negatives were reached by processes with the corrections attached** (BH over 1,653 pairs with raw/expected/corrected all reported, ADR-030; deflated Sharpe over registered grids, ADR-041; publication lag measured rather than documented, ADR-042). I looked specifically for a negative reached by a process that would also have produced a positive on noise and did not find one in the register; the reverse asymmetry — a *positive* reached without those corrections — is DRAFT-p2-register-2 and -4.

## Live-repo access log

Live repository touched: `/home/kiros-li/Documents/GitHub/MLCryptoEngine` — read-only `git log`/`git show`/`git rev-parse`/`git status`, plus read-only reads of untracked files under `data/processed/detection/` and a directory/mtime listing under `data/raw/venue=hyperliquid/`. No writes, no checkouts, no script executed inside the repository.

Before (2026-09-12 18:09 UTC):
```
$ git -C /home/kiros-li/Documents/GitHub/MLCryptoEngine status --porcelain
(no output — clean)
$ git -C /home/kiros-li/Documents/GitHub/MLCryptoEngine rev-parse HEAD
5359a11fc753cdcd2606aea991dae826293d0307
```

After (2026-09-12 18:22 UTC):
```
$ git -C /home/kiros-li/Documents/GitHub/MLCryptoEngine status --porcelain
(no output — clean)
$ git -C /home/kiros-li/Documents/GitHub/MLCryptoEngine rev-parse HEAD
5359a11fc753cdcd2606aea991dae826293d0307
```
