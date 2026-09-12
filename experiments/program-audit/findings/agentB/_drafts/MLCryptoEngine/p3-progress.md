# Agent B draft findings — MLCryptoEngine, part p3-progress

Repository: MLCryptoEngine @ `5359a11fc753cdcd2606aea991dae826293d0307` (main, 2026-08-22)
Assigned documents read completely: `progress.md` (2977 lines), `research/` (all 60 modules +
`research/experiments.jsonl`), `backtest/` (all 6 files). Other documents (`report.md`,
`HYPOTHESES.md`, `AUDIT.md`, `DECISIONS.md`, `README.md`, `docs/notes/`, `config/`, `audit/`) read
for corroboration only; where a finding's primary evidence sits in one of those it is marked.

Unanchored reads (live working tree, read-only, **2026-09-12T18:17Z**):
`data/processed/detection/hard_rug_scorer.meta.json`, `data/processed/detection/features_c23.csv`,
`data/processed/reports/d1d_*.json`, directory listings of `logs/` and `data/processed/`. These are
gitignored artifacts and may have changed after the anchor.

---

### DRAFT-p3-progress-1
- **Repository / SHA:** MLCryptoEngine / 5359a11fc753cdcd2606aea991dae826293d0307
- **Hypothesis or artifact:** D1 — the shipped hard-rug clearance scorer (`research/detection/scorer.py`, `train_scorer.py`, `data/processed/detection/hard_rug_scorer.txt`)
- **Direction:** B
- **Class:** UNSUPPORTED_POSITIVE
- **Severity:** S2
- **Label:** DERIVED
- **Claim challenged (verbatim quote):** "the **hard-rug clearance scorer** (0.984 clearance precision, weak alarm 0.464)" — MLCryptoEngine/progress.md:2470. Register form: "**Honest-clearance precision 0.984 at recall 0.538** on the 2024 test fold (train ≤ 2023), from 30-minute launch-window features." — MLCryptoEngine/HYPOTHESES.md:239; sample stated as "281 reached to T0, 194 in the 2024 test fold" — MLCryptoEngine/HYPOTHESES.md:240.
- **Evidence:**
  - The shipped model's own metadata sidecar gives the operating point exactly: `"clearance_point_pos_honest_recall_ge_0.5": {"precision": 0.9844, "recall": 0.5385, "threshold": 0.5963}`, `"train_n": 87`, `"train_hard_rug": 42`, `"test_n": 194`, `"test_hard_rug": 77` — `data/processed/detection/hard_rug_scorer.meta.json` (live tree, read 2026-09-12T18:17Z, UNANCHORED).
  - The training matrix confirms the split: `data/processed/detection/features_c23.csv` has 281 rows; by (year, cls): 2021 14 hard_rug / 15 honest, 2022 13/15, 2023 15/15, 2024 **77 hard_rug / 117 honest** (read 2026-09-12T18:17Z, UNANCHORED). `train_scorer.py:67-68` splits on `yr != "2024"`, so the model is fitted on **87 pools**.
  - The operating point is therefore **63 true clearances against 1 false one (63/64 = 0.984375)** and the recall 0.5385 = 63/117. Neither `64`, `63`, `87`, nor any interval appears in `progress.md`, `report.md:3646-3658`, `report.md:3968-3972`, `HYPOTHESES.md:236-243`, the module docstring (`research/detection/scorer.py:1-31`), or the generated scope string (`research/detection/scorer.py:106-121`). The register's **Sample** cell (HYPOTHESES.md:240) states 281 and 194 — 3×–4× the n the deciding figure actually rests on.
  - Precision is base-rate dependent and the 2024 fold's honest share (117/194 = 0.603) is a property of the **stratified sampling design** registered in C.21 ("540-token class×year stratified sample (240 train-era, 300 test-era)", progress.md:2311-2313), not of the population. The labelled population is 75,996 hard_rug / 34,791 honest (progress.md:2276-2278), i.e. 0.314 honest; the deployment base rate the scorer's own scope note names is ~0.013 honest ("in the wild ~99% of launches are scam-adjacent", `research/detection/scorer.py:118-119`).
  - The register's forward statement is unconditional: "Nothing reopens the *result* — it works." — MLCryptoEngine/HYPOTHESES.md:243.
- **Recomputation (if any):**
  - Inputs: precision 0.9844, recall 0.5385 (`hard_rug_scorer.meta.json`, unanchored), honest test n = 117 and hard-rug test n = 77 (`features_c23.csv`, unanchored; 194 total also at HYPOTHESES.md:240). Method: solve TP = recall × 117, FP = TP/precision − TP.
    Result: **TP = 63, FP = 1, operating-point n = 64.** Wilson 95% CI on 63/64 = **[0.917, 0.997]**; Clopper–Pearson 95% = [0.916, 0.9996]. The alarm point is 39/84 = 0.4643, Wilson 95% [0.362, 0.570].
  - Base-rate transport, same TPR = 63/117 = 0.5385 and FPR = 1/77 = 0.01299, precision = TPR·π / (TPR·π + FPR·(1−π)):
    π = 0.603 (the fold) → **0.984** (reproduces the published figure exactly, confirming the decomposition);
    π = 0.314 (labelled population, progress.md:2276-2278) → **0.950**;
    π = 0.013 (the wild rate the scorer's scope note names, scorer.py:118) → **0.353**.
  - Script and output: /home/kiros-li/.cache/program-audit/scratchpad/work/agentB-mlcrypto-p3/ (inline heredoc, re-runnable).
- **What would resolve it:** Publish the operating-point n (64 predictions, 1 error) and the training n (87) beside the 0.984 in the register, the report and `scope_note()`, with an interval; and state the clearance precision recomputed at the population and wild base rates the same artifact names, rather than at the stratified-design base rate only.
- **Confidence:** HIGH — the 63/1 decomposition reproduces the published 0.984/0.538 pair to four decimals from the shipped artifact's own metadata, and the absent n is verifiable by grep across every document.
- **Invalidated by later commits?:** no — `research/detection/scorer.py` and `train_scorer.py` have exactly one commit each (`9294da1`, 2026-08-07) and the register text is unchanged through the anchor; only a future re-measurement would invalidate it.
- **Disclosed by authors?:** partly — the base-rate dependence is stated qualitatively ("read a score against that base rate", HYPOTHESES.md:241; scorer.py:22-25), but the operating-point sample size, the single false clearance, the 87-row training fold and any interval or recomputed base-rate figure are absent from every field.

---

### DRAFT-p3-progress-2
- **Repository / SHA:** MLCryptoEngine / 5359a11fc753cdcd2606aea991dae826293d0307
- **Hypothesis or artifact:** D1 — the hard-rug clearance scorer's sample, versus the depth-selection correction the same repository applied to its sibling result (D2)
- **Direction:** B
- **Class:** STATISTICAL
- **Severity:** S2
- **Label:** DERIVED
- **Claim challenged (verbatim quote):** "This bias is **conservative** for the bar attempt: a faded honest pool looks rug-like behaviourally, so it depresses, never inflates, measured separation." — MLCryptoEngine/report.md:3572-3574 (primary evidence for this quote is in another reader's document; the consequences below are in mine). Carried forward unqualified as "the **hard-rug clearance scorer** (0.984 clearance precision, weak alarm 0.464)" — MLCryptoEngine/progress.md:2470 and MLCryptoEngine/report.md:3968-3970.
- **Evidence:**
  - The C.23 sample that produced the scorer was selected by reachability under a page-capped backward pagination: "Sweep: 360 designed, T0 reached 281 (78.1% …)" — MLCryptoEngine/progress.md:2360-2361. The same sweep and its cap are what C.24 inherited: "That inherits C.23's 40-page reachability selection — the same conservative faded-honest skew, stated not hidden." — MLCryptoEngine/report.md:3578-3579.
  - C.25 then **measured** that the selection removes the majority of the honest class: "Task 2 measured **57% of honest pools deep** (>40 pages); the 40-page selection excluded the majority." — MLCryptoEngine/progress.md:2426-2428.
  - And C.25 measured the *direction* of the resulting bias, which is the opposite of the one asserted at report.md:3572-3574: "random-draw Method-B corrected sample (+120 honest, 96 reached), 6h v0 lift **+0.047** vs C.24's biased v0 +0.115" — MLCryptoEngine/progress.md:2430-2431; "The corrected v0 lift (**+0.047**) is roughly **half** C.24's v0 lift (+0.115)" — MLCryptoEngine/report.md:3801. Removing the selection **halved** the measured separation; the selection had inflated it, not depressed it.
  - The scorer was never re-measured on an unbiased sample. `git -C <live> log -- research/detection/scorer.py research/detection/train_scorer.py` returns a single commit, `9294da1` (2026-08-07, "C.24 … ship the hard-rug scorer"). `git show --stat 41e6275` (C.25) and `git show --stat 2403a8e` (C.26) each touch only `DECISIONS.md`, `HYPOTHESES.md`, `progress.md`, `report.md` — no code and no feature matrix. `train_scorer.py:27` still reads `data/processed/detection/features_c23.csv`, the pre-correction matrix.
  - The limitation is absent from the artifact's own framing and from the register entry: `research/detection/scorer.py:9-31` lists four scope limits (hard rugs only, clearance not alarm, no soft/slow rugs, base rate) and no sampling limit; `scope_note()` (scorer.py:106-121) likewise; HYPOTHESES.md:241 **Limitations** likewise. The D2 entry immediately below it does carry the correction ("The C.24 magnitude was **reachability-inflated**", HYPOTHESES.md:255).
  - The track-closing deliverables list restates the uncorrected figure one bullet above the corrected sibling: "clears a pool as not-a-hard-rug at 0.984 precision / 0.538 recall" (report.md:3968-3969) sits directly above "survived depth-unbiasing at half its C.24 magnitude" (report.md:3973-3976).
- **Recomputation (if any):** none required — the two figures that establish the bias direction (+0.115 biased vs +0.047 unbiased, a factor of 2.45) are the repository's own, at progress.md:2430-2431 and report.md:3801.
- **What would resolve it:** Either re-measure the clearance operating point on a Method-B (depth-independent) honest sample, as C.25 did for the behavioural lift, or add the 40-page reachability selection to the scorer's scope note and to the D1 register **Limitations** cell and withdraw "Nothing reopens the *result* — it works" (HYPOTHESES.md:243) until it has been.
- **Confidence:** HIGH — the selection, its measured magnitude, its measured direction on a sibling estimate built from the *same* sample family, and the absence of any re-measurement are all established by the repository's own text and its own git history.
- **Invalidated by later commits?:** no — the anchor is the last commit touching any detection file; a later re-measurement would resolve it.
- **Disclosed by authors?:** partly — the existence of the skew is disclosed for the C.24 behavioural sample (report.md:3578-3579, progress.md:2395), and its measured magnitude at progress.md:2426-2428; but the assertion that it can only depress (report.md:3572-3574) is never withdrawn, the scorer is never re-measured, and no disclosure attaches to D1's deciding number, its register entry or the shipped module.

---

### DRAFT-p3-progress-3
- **Repository / SHA:** MLCryptoEngine / 5359a11fc753cdcd2606aea991dae826293d0307
- **Hypothesis or artifact:** H6 — the registered thin-perp census (`research/microstructure/registered.py`), its survivor rule and its multiplicity correction
- **Direction:** B
- **Class:** STATISTICAL
- **Severity:** S2
- **Label:** DERIVED
- **Claim challenged (verbatim quote):** "**A3/A6/A8** — census intervals assume independence and are 2–17× too narrow (`halfwidth·√n/sd = 1.9600` for all ten instruments). PUMP and MERL survive HAC, day-clustered and block-bootstrap; **GMX flips** (+0.288 → −0.070 day-clustered) and is now recorded as unresolved rather than a survivor." — MLCryptoEngine/progress.md:2741-2745
- **Evidence:**
  - The survivor rule was **not** changed. `research/microstructure/registered.py:292-298` selects survivors on `float(r["ci95_lower_bps_worst"]) > 0` — the IID bound — and `:285-290` feeds Benjamini–Hochberg `p_values = [float(r["p_one_sided_worst"]) …]`, which `:187` computes as `student_t.sf(mean / se, n - 1)` with `se = math.sqrt(var / n)` (`:182`), the same IID standard error the audit finding declares invalid. `:299-310` assigns every category from the same IID bound.
  - The day-clustered correction exists only as a reported diagnostic: `_day_clustered_se` (`registered.py:146-163`) and `ci95_lower_bps_day_clustered` (`:204`, surfaced at `:268`) are computed and never consulted by `assemble()`.
  - `git -C <live> show d2a0f05 -- research/microstructure/registered.py` (the commit whose message states the A3/A6/A8 remediation) adds `_day_clustered_se`, the extra reported fields, the one-sided critical value and the `recorded_ns` parameter, and **contains no hunk touching `assemble()`**.
  - Consequence: running the shipped `run_registered_census` on the census week still classifies GMX as `survivor_tradeable_capacity` (GMX: `p_one_sided_iid = 4.88e-12`, `reported_ci95_lower_bps = +0.288`, and C.27 reported it clearing both-halves and capacity). The published verdict "GMX … is now recorded as unresolved rather than a survivor" (progress.md:2743-2745) is a prose edit that the code does not reproduce.
  - The GMX demotion itself is computed with the critical value the same audit round declares wrong. `audit/census_ci.json` (tracked artifact) gives GMX `net_mean_bps = 0.40443`, `day_cluster_se = 0.193692`, `day_cluster_ci95_lower_bps = **+0.028**`; the quoted −0.070 is the **two-sided** bound, while the paired A6 correction in the very same bullet reads "One-sided bar no longer judged with a two-sided critical value" (progress.md:2745-2746) and `registered.py:183,188-192` now uses the one-sided value everywhere else.
  - What the corrected intervals are worth on the two survivors that were carried forward: PUMP `day_cluster_se = 0.28889` on **7** day clusters, MERL `1.93109` on 7 (`audit/census_ci.json`). MERL's seven daily means run **+0.90, +1.62, +1.82, +2.94, +6.82, +8.35, +15.02 bps** — a monotone sixteen-fold spread across one week, on which a 6-degree-of-freedom t interval is the whole robustness evidence.
- **Recomputation (if any):**
  - Inputs: `audit/census_ci.json` GMX `net_mean_bps = 0.40443149568754866`, `day_cluster_se = 0.19369186624939855`, `n_days = 7`. Method: `mean − t_crit · se`, `t(0.95, 6) = 1.9432`, `t(0.975, 6) = 2.4469`.
    Result: one-sided lower bound **+0.0281**; two-sided **−0.0695**. The published −0.070 is the two-sided figure; under the convention the same commit adopted, GMX does **not** flip.
  - Script: /home/kiros-li/.cache/program-audit/scratchpad/work/agentB-mlcrypto-p3/ (inline, re-runnable).
- **What would resolve it:** Either move the survivor gate and the BH input in `assemble()` onto the clustered (or HAC/bootstrap) statistic and re-run the census, or state in the register and in `registered.py` that the shipped decision rule is the uncorrected IID one and that the published survivor set was selected under it; and reconcile the GMX demotion with the one-sided convention adopted in the same commit.
- **Confidence:** HIGH — the code path, the unchanged `assemble()`, the diff, and the two critical values are all directly checkable; the arithmetic reproduces both quoted bounds exactly.
- **Invalidated by later commits?:** no — `d2a0f05` is the last commit touching `registered.py` before the anchor. The consequence for the project's conclusions is bounded because H6 later closed at D.1d, but the census result is still carried in the register as "the project's first bar-clearing positive" (progress.md:2527).
- **Disclosed by authors?:** partly — AUDIT.md §A3 and progress.md:2741-2746 disclose that the intervals are 2–17× too narrow and that no clustering correction exists; neither discloses that the survivor rule and the BH inputs were left on the uncorrected statistic, nor that the GMX demotion uses the critical value the adjacent A6 correction rejects.

---

### DRAFT-p3-progress-4
- **Repository / SHA:** MLCryptoEngine / 5359a11fc753cdcd2606aea991dae826293d0307
- **Hypothesis or artifact:** the three shipped `PerformanceReport` artifacts (`data/processed/reports/d1d_{PUMP_base,MERL_base,MERL_improved}.json`) and the A13 remediation claimed for them
- **Direction:** B
- **Class:** INTERNAL_INCONSISTENCY
- **Severity:** S2
- **Label:** DERIVED
- **Claim challenged (verbatim quote):** "Fill-instant attribution withdrawn from report.md, H6 and the shipped `PerformanceReport`; H6's reopening condition rewritten, since it had been scoped to a mechanism the data cannot pin down." — MLCryptoEngine/progress.md:2735-2737
- **Evidence:**
  - The audit located the defect as a published field in the shipped artifact: "consumed by `report.md` §D.1d.2 and published as `SlippageStats(expected_bps=2.74, realized_bps=−1.01)` in `data/processed/reports/d1d_PUMP_base.json` via `d1d.py:242-245`" — MLCryptoEngine/AUDIT.md:414-421 (another reader's document; the code and artifact below are in mine).
  - At the anchored SHA the field is still emitted: `research/microstructure/d1d.py:295-298` builds `slippage=SlippageStats(expected_bps=float(summary["expected_edge_bps"] or 0.0), realized_bps=float(summary["edge_bps"]))`, i.e. the fill-instant realized edge. `d1d.py:262-270` additionally writes a per-leg `gross_pnl=round(edge, 8)` into every `TradeRecord`.
  - The schema keeps the field and its interpretive label: `backtest/reporting/schema.py:63-67` — `class SlippageStats` / `"""Realized fill quality against what the simulation assumed."""` with `expected_bps` and `realized_bps` both required; there is no notes, caveat or provenance field anywhere in `PerformanceReport` (`backtest/reporting/schema.py:78-95`). The generated consumer type exposes it verbatim: `desktop/src/lib/generated/performance-report.ts:35` `realized_bps: number;`, `:57` `slippage: SlippageStats;`.
  - The regenerated artifacts carry the withdrawn quantity, post-correction: `d1d_PUMP_base.json` `slippage.expected_bps = 2.7553`, `slippage.realized_bps = **−1.2271**`; `d1d_MERL_base.json` `2.7776 / **−2.7419**`; `d1d_MERL_improved.json` `1.7498 / **−2.3857**` (live tree, read 2026-09-12T18:17Z, UNANCHORED; file mtimes 2026-08-12 21:35, i.e. regenerated by the corrected engine 14 minutes before commit `d2a0f05`, and the net figures `−4.8087 / −4.3459 / −6.3503` match the corrected headline at report.md:5121-5125).
  - The quantity is exactly the one the audit shows is not identified by this data: "PUMP's realized edge swings from **−1.01 to +0.45 — a sign flip**" under a ±5 ms feed shift, "so moving the instant at which a fill is marked merely relocates P&L between the two buckets" — MLCryptoEngine/AUDIT.md:451-459.
- **Recomputation (if any):** none needed — the claim is that a field was withdrawn from an artifact; the field is present in the schema (`backtest/reporting/schema.py:63-67`), in the generator (`research/microstructure/d1d.py:295-298`), in the emitted files, and in the desktop type.
- **What would resolve it:** Either drop `SlippageStats` (and the per-leg `gross_pnl` attribution) from the D.1d reports, or add an explicit non-identified marker — the schema currently has no field that could carry one — and restate progress.md:2735-2737 as "withdrawn from the prose, retained unlabelled in the artifact".
- **Confidence:** HIGH — the generator line, the schema, the TypeScript type and the emitted values are all directly inspectable; the only judgement call is whether "withdrawn from the shipped `PerformanceReport`" means the field or only the interpretation, and the audit's own "Where" line names the field and the file.
- **Invalidated by later commits?:** no — `d2a0f05` is the last commit touching `d1d.py`; the reports' mtimes predate it and nothing regenerates them afterwards.
- **Disclosed by authors?:** no — progress.md:2735-2737, report.md:5108-5116 and the D.1d caveat list all state the attribution was withdrawn from the shipped report; none says the field remains.

---

### DRAFT-p3-progress-5
- **Repository / SHA:** MLCryptoEngine / 5359a11fc753cdcd2606aea991dae826293d0307
- **Hypothesis or artifact:** H5 — funding-rate carry; the per-instrument net-on-capital table and the "5 of 10 clear cash" verdict (`research/carry/__main__.py`, `research/carry/trade.py`)
- **Direction:** B
- **Class:** STATISTICAL
- **Severity:** S2
- **Label:** DERIVED
- **Claim challenged (verbatim quote):** "**Verdict.** Against a 4% risk-free rate, **5 of 10 clear it** historically by 1.6–4.1 points." — MLCryptoEngine/progress.md:1522-1523; the table it rests on: "**Return on deployed capital, per instrument at its best band:** ETH **8.07%**, BTC **8.00%**, LINK 7.43%, SOL 5.86%, ARB 5.57%, DOT 3.48%, PUMP 3.26%, NOT 1.68%, GMX 1.28%, TNSR **−10.45%**." — MLCryptoEngine/progress.md:1500-1503.
- **Evidence:**
  - Every figure in that table is a **maximum over a five-point parameter sweep**, selected on the outcome, with a different parameter chosen per instrument. `research/carry/__main__.py:55` `REBALANCE_BANDS = (0.02, 0.05, 0.10, 0.25, 0.50)`; `:161-172` runs `tr.simulate` once per band; `:183` `entry["best_band"] = max(sweep, key=lambda r: r["net_pct_of_capital_pa"])`. The published table's `band` column is 10% for ETH and BTC and 25% for six others (report.md:1762-1772), i.e. the parameter varies per instrument.
  - The module states the opposite intent in its own comment: "The rebalancing band is the whole design trade-off, so it is swept rather than chosen … **Picking one band would present a preference as a result.**" — `research/carry/__main__.py:51-54`; echoed as "The band is swept, never chosen." — MLCryptoEngine/progress.md:1499.
  - No multiplicity or deflation correction is applied anywhere in `research/carry/`. `grep -rn "deflat\|n_trials" research/carry/` returns nothing; `research/carry/__main__.py` never imports `research.pairs.validation`. The same repository registers trial-count deflation for exactly this situation in three other stages: "The deflated Sharpe uses C.10's estimator … with **n_trials = 12**" (progress.md:1737-1740, C.16), "**n_trials for deflation = the full registered cell count** — every cell computed counts, and no cell may be dropped from the denominator" (progress.md:1976-1978, C.17), and C.13's own verdict on a sweep: "**The parameter surface is noise.** Net swings from −10.15% to +51.61% across the sweep with no stable optimum … A result that moves 60 points on the choice of rebalance interval is fitted." (progress.md:1610-1616).
  - The code's own aggregate counter does not agree with the published verdict either: `research/carry/__main__.py:193` computes `beats_cash` from `results`, which holds only the **default** 2% band run (`:155` `tr.simulate(coin, times, spots, perps, rates, config)` with `config = tr.CarryConfig()`, default `DEFAULT_BAND = 0.02`, `trade.py:45`). The "5 of 10 … by 1.6–4.1 points" sentence is arithmetic on the best-band column, not on that counter.
  - Only one instrument's sweep is published (BTC, report.md:1750-1756); the two marginal instruments that make the count 5 rather than 3 — SOL at +1.86 and ARB at +1.57 points over the benchmark — have no published sweep, so their margins cannot be checked against band choice at all.
- **Recomputation (if any):**
  - Inputs: the BTC band sweep at MLCryptoEngine/report.md:1750-1756 — 2% 6.84, 5% 7.97, 10% **8.00**, 25% 7.59, never-resize 6.43 (net % on capital p.a.). Method: compare the reported maximum with the sweep's own spread and mean.
    Result: max−min = **1.57 points**; max − mean(5 cells) = **0.63 points**. The published 8.00% is the top of a 1.57-point range, all of whose cells happen to clear 4% for BTC.
  - Inputs: the best-band column (progress.md:1500-1503) minus the 4% benchmark (`research/carry/__main__.py:50` `RISK_FREE_PCT = 4.0`). Method: subtraction.
    Result: ETH +4.07, BTC +4.00, LINK +3.43, SOL +1.86, ARB **+1.57**, DOT −0.52 — reproducing the quoted "1.6–4.1 points" exactly and confirming the verdict is computed from the maxima. A band-induced swing of the BTC size (1.57 points) applied to ARB's +1.57 margin would take it to the benchmark.
  - Script: /home/kiros-li/.cache/program-audit/scratchpad/work/agentB-mlcrypto-p3/ (inline, re-runnable).
- **What would resolve it:** Publish the full per-instrument band sweep (the payload already computes it, `__main__.py:161-181`), report the table at a single pre-declared band with the sweep as a range, and state the count of instruments clearing cash at the *worst* as well as the best band — or apply the trial-count deflation the sibling stages register.
- **Confidence:** HIGH — the selection is one line of code (`__main__.py:183`), the verdict's arithmetic reproduces the published margins to 0.01, and the absence of any correction is a grep.
- **Invalidated by later commits?:** no — `research/carry/` has a single commit (`2382aca`, 2026-08-04) and the register entry is unchanged through the anchor.
- **Disclosed by authors?:** partly — report.md:1760 labels the table "**Per instrument, at each one's best band**" and report.md:1757-1758 calls BTC's optimum "a shallow optimum"; neither the register's deciding-number cell (HYPOTHESES.md:114) nor progress.md's verdict (progress.md:1522-1523) carries the qualifier, and no document anywhere discusses correcting for the five-point selection.

---

### DRAFT-p3-progress-6
- **Repository / SHA:** MLCryptoEngine / 5359a11fc753cdcd2606aea991dae826293d0307
- **Hypothesis or artifact:** the shipped standalone note `docs/notes/h1-predictability-without-capturability.md` and the H1 register paragraph it quotes — the top-decile economic-bar comparison
- **Direction:** B
- **Class:** STALE_FIGURE
- **Severity:** S3
- **Label:** DERIVED
- **Claim challenged (verbatim quote):** "**Top-confidence deciles capture 2–24× the all-sample mean** through accuracy rather than magnitude, and the best decile in the study takes **5.00 bps against 80 bps** — missing the economic bar by **16×**." — MLCryptoEngine/progress.md:2826-2829 (identical text shipped at docs/notes/h1-predictability-without-capturability.md:99-101 and HYPOTHESES.md:54).
- **Evidence:**
  - The 5.00 bps decile is a **Kraken** measurement: report.md:2296 gives the Kraken BTC/USD row `| 900 s | 0.5401 | 0.2093 | +0.0606 | 5.0020 | 23.9× |` under the heading "**Kraken BTC/USD, 6 days, 165,075 samples**" (report.md:2288), and report.md:2320 states "the best top-decile capture across both venues and all horizons is **5.00 bps against an 80 bps round trip**".
  - Kraken's round trip is **50 bps**, not 80, as of ADR-055: "**Kraken fee reconciled (Task 3, ADR-055):** base tier corrected 0.40/0.80 → **0.25/0.40** (live schedule, retrieved 2026-08-08) … Round-trip maker 80→50 bps." — MLCryptoEngine/progress.md:1385-1388. The corrected value is in `config/venues.yaml:60` (`maker_bps: 25`), in the register's cost table (HYPOTHESES.md:305), and in the note's own cost table (docs/notes/…:77).
  - The same shipped note uses 50 bps for Kraken eleven lines earlier: "Against Kraken's own 50 bps round trip that is a miss of roughly **1,700×**" — MLCryptoEngine/progress.md:2823-2825 and docs/notes/…:81-82. So one document applies two different Kraken round trips to two figures from the same Kraken table.
  - The register performed this reconciliation for the *other* H1 figure and not for this one: "even at 0.25 maker (round trip 50 bps) H1's 3.31 bps gross capture fails by ~15×" — HYPOTHESES.md:445. `git show 81e456e -- HYPOTHESES.md` shows the cost-table row changed `40 bps | **80 bps**` → `25 bps | **50 bps**` and the ~15× sentence added, with the C.14 decile paragraph untouched.
  - The framing was re-published into a **new** shipped artifact 15 days after the correction: `git log -S "5.00 bps against 80 bps"` returns `ddf525d` (2026-08-05, before the fee correction) and `ae03bf6` (**2026-08-22T17:38**, the note), against `81e456e` (2026-08-07T17:33, the correction).
  - Both halves of the stale comparison are locked in place by the note's own honesty suite, which requires them to appear in the note *and* in the register: `tests/test_note_honesty.py:137` `"5.00 bps"`, `:139` `"16×"`, `:169` `"| Coinbase Advanced spot, base tier | 40 bps | **80 bps** |"` — while `:168` simultaneously pins `"| Kraken spot, base tier | 25 bps | **50 bps** |"`, and `:174` pins `"5.0020"` against report.md. Correcting the comparison in one document alone fails the build.
- **Recomputation (if any):**
  - Inputs: top-decile capture 5.0020 bps (MLCryptoEngine/report.md:2296, Kraken BTC/USD, 900 s), Kraken base-tier maker round trip 50 bps (MLCryptoEngine/progress.md:1386-1388; config/venues.yaml:60). Method: cost ÷ capture.
    Result: **10.00×**, not 16×. With the pre-ADR-055 80 bps the quotient is 15.99× ("16×"), confirming which cost figure was used.
  - Script: /home/kiros-li/.cache/program-audit/scratchpad/work/agentB-mlcrypto-p3/ (inline, re-runnable).
- **What would resolve it:** State which venue's decile the 5.00 bps is (Kraken), compare it against Kraken's corrected 50 bps round trip (10×), and update the C.14 registered "economic" threshold — registered as a single `>= 80.0 bps` for both venues at progress.md:1631-1633 — to the per-venue floors the cost table now carries; then re-pin the honesty tests to the corrected pair.
- **Confidence:** HIGH — the decile's venue, the corrected fee, the two different round trips inside one shipped document, and the publication date relative to the correction are all directly checkable; the arithmetic is one division.
- **Invalidated by later commits?:** no — `ae03bf6` and `5359a11` are the last two commits in the repository and neither revisits the comparison.
- **Disclosed by authors?:** no — the note's scope section (progress.md:2833-2841 summarising it) names six limits and does not mention that its economic-bar multiple uses a superseded venue cost; the direction of the error makes the closure look stronger than the corrected figure supports.

---

### DRAFT-p3-progress-7
- **Repository / SHA:** MLCryptoEngine / 5359a11fc753cdcd2606aea991dae826293d0307
- **Hypothesis or artifact:** the C.5 backfill recommendation and the C.6 purchase options — the walk-forward fold arithmetic that sized a $81 data purchase and the C.8 experiment
- **Direction:** B
- **Class:** ARITHMETIC
- **Severity:** S3
- **Label:** DERIVED
- **Claim challenged (verbatim quote):** "**Contiguous months needed: 6 minimum, 12 preferred.** Walk-forward with a 3-month train and 1-month test window yields 3 folds at 6 months and 9 at 12; fewer than ~6 folds cannot distinguish a real pattern from one regime." — MLCryptoEngine/progress.md:878-881. And: "4 months (2026-04..07) prices at **$97.08** and fits the current cap with $16.69 to spare, giving 2 walk-forward folds at 3-month train / 1-month test rather than 3." — MLCryptoEngine/progress.md:956-958.
- **Evidence:**
  - The stated scheme is a 3-month training window with a 1-month test window advancing one month at a time, so the number of folds is `months − 3`. The repository's own two data points confirm that rule exactly: 6 months → 3 folds and 12 months → 9 folds (progress.md:879-880).
  - Applying the same rule to the sentence's own recommended minimum: **6 months yields 3 folds**, which is half the "~6 folds" the same sentence declares necessary to "distinguish a real pattern from one regime". The recommended minimum fails the criterion stated beside it; only the 12-month "preferred" option meets it (9 folds).
  - Applying the same rule to the C.6 option actually costed and offered: **4 months yields 1 fold**, not the 2 claimed at progress.md:957-958.
  - The "~6 folds" threshold itself is asserted with no source, derivation or power calculation anywhere in `progress.md`, `report.md`, `DECISIONS.md` or `research/validation/`; `grep -rn "6 folds\|fold" research/validation/` shows `walk_forward` carries only a `MIN_FOLD_BARS = 60` guard (`research/pairs/validation.py:37`), no fold-count requirement.
  - The consequence is recorded two stages later, when the purchase that was actually made produced fewer folds than either figure: "**Walk-forward: one clean fold, not three (ADR-024).** 42/14-day windows over a 61-day span yield 2 folds, the second truncated 5 days past the data (43,340 samples vs 252,596)." — MLCryptoEngine/progress.md:1150-1153.
- **Recomputation (if any):**
  - Inputs: the scheme at MLCryptoEngine/progress.md:879-880 (3-month train, 1-month test, advancing monthly). Method: enumerate folds — fold *k* trains on months *k*…*k+2* and tests month *k+3*, so folds = months − 3.
    Result: 4 months → **1** fold (repo says 2); 6 months → **3** folds (repo's own figure, and below its own "~6" requirement); 12 months → 9 folds.
  - Script: /home/kiros-li/.cache/program-audit/scratchpad/work/agentB-mlcrypto-p3/ (inline, re-runnable).
- **What would resolve it:** Correct the 4-month fold count to 1, and either raise the stated minimum to 9 months (6 folds) or drop the "~6 folds" criterion and say what statistical requirement actually governs; give the ~6-fold threshold a derivation or a citation.
- **Confidence:** HIGH — the fold count follows deterministically from the scheme the same sentence states, and the repository's own 6→3 and 12→9 figures fix the rule.
- **Invalidated by later commits?:** no — both sentences are unchanged at the anchor; the purchase they sized was already made and stopped at two months (progress.md:960-966).
- **Disclosed by authors?:** no — neither the internal contradiction ("6 minimum" giving 3 folds against a "~6 folds" requirement) nor the 4-month miscount is noted anywhere; C.8's "one clean fold, not three" (progress.md:1150) reports the shortfall against the 6-month figure without revisiting the arithmetic.

---

### DRAFT-p3-progress-8
- **Repository / SHA:** MLCryptoEngine / 5359a11fc753cdcd2606aea991dae826293d0307
- **Hypothesis or artifact:** D2 — the post-launch behavioural "qualified positive", and the evidentiary standard applied to it versus the standard the same repository registered for its alpha hypotheses
- **Direction:** B
- **Class:** UNSUPPORTED_POSITIVE
- **Severity:** S3
- **Label:** READ
- **Claim challenged (verbatim quote):** "the **behavioural finding** (real but small and unconfirmed, mid-stratum +0.032 CI-includes-zero)" — MLCryptoEngine/progress.md:2471-2472; register form: "It has produced the project's first two substantive positives." — MLCryptoEngine/HYPOTHESES.md:229.
- **Evidence:**
  - The final deciding number and its interval are given in the same breath: "the **mid-stratum lift moved DOWN +0.051 → +0.032** (SE 0.039, 95% CI [−0.045, +0.109], still includes zero). The added data **weakened rather than confirmed**" — MLCryptoEngine/progress.md:2465-2468.
  - The bar it is said to meet is a bare point-estimate threshold with no uncertainty control: "the **mid-activity stratum holds (+0.051)**, meeting the pre-registered genuine-discrimination bar (>0.02 and ≥ half overall)" — MLCryptoEngine/progress.md:2433-2435. At C.26's final numbers (+0.032 mid-stratum against +0.043 overall) the bar is still nominally met, by a margin (0.012 over the 0.02 floor) roughly one third of the estimate's own standard error (0.039).
  - No multiplicity correction is applied across the grid that was searched: "18 cells were scored (3 cutoffs × 3 sets × 2 labels)" — MLCryptoEngine/report.md:3640-3642; the response is an argument from coherence, not a correction. C.25 adds a further stratum decomposition (high/mid/low activity) and C.26 a re-estimate, none of them counted.
  - The same repository registered materially stricter standards for every alpha positive: H6's census required "**95% confidence interval lower bound above zero at the worst of the three horizons**", "**Benjamini–Hochberg across the ten thin instruments at q = 0.10**", "**Sample floor: ≥ 300 aggressor trades**", "**Robustness: the effect must hold in both halves of the window independently**" and a capacity tier (progress.md:2128-2153); H9 and H11 required "deflated Sharpe probability **≥ 0.95**" (progress.md:1751-1753, 2002-2004).
  - The label survives the weakening: the deliverables list still calls it "a **real but small and unconfirmed** post-launch behavioural signal" (report.md:3987-3990) and the register keeps D2's status as "*(qualified positive, open for confirmation)*" (HYPOTHESES.md:245) while its "What would reopen it" cell asserts "the signal is real in direction but small" (HYPOTHESES.md:257).
- **Recomputation (if any):** none — the CI is the authors'; the comparison is between the standard applied here (point-estimate lift > 0.02, 18 uncorrected cells) and the standards the same repository registered for H6, H9 and H11 at the lines cited.
- **What would resolve it:** State D2's status against the standard the repository uses elsewhere — an interval that excludes zero after correction for the cells searched — and replace "real but small" with the CI, which is the only measured statement available; or register, in advance, why the detection track is judged on an uncorrected point estimate.
- **Confidence:** MEDIUM — the numbers and the multiplicity are the authors' own and are disclosed; what is contested is the label "real"/"substantive positive" attached to an estimate whose disclosed interval includes zero, which is a judgement about framing rather than about a computation.
- **Invalidated by later commits?:** no — C.26 (`2403a8e`) is the last commit touching the D2 entry and the anchor carries it unchanged.
- **Disclosed by authors?:** yes (MLCryptoEngine/progress.md:2465-2468; MLCryptoEngine/HYPOTHESES.md:255; MLCryptoEngine/report.md:3640-3642) — the CI including zero, the ~0.8 SE margin and the 18 scored cells are all stated plainly; presenting them as a discovery would be a process failure, so this finding is confined to the label the same documents place on top of them.

---

### DRAFT-p3-progress-9
- **Repository / SHA:** MLCryptoEngine / 5359a11fc753cdcd2606aea991dae826293d0307
- **Hypothesis or artifact:** `research/experiments.jsonl` and `research/validation/experiment_log.py` — the append-only trial registry that exists so multiple-testing corrections can be computed
- **Direction:** B
- **Class:** PROVENANCE
- **Severity:** S3
- **Label:** DERIVED
- **Claim challenged (verbatim quote):** "Append-only experiment log: every training run, from the first one. A deflated Sharpe ratio — or any honest multiple-testing correction — is only computable if the number and shape of trials is known, and that only works if the log exists from the first experiment rather than being retrofitted after the survivors are chosen." — MLCryptoEngine/research/validation/experiment_log.py:1-6
- **Evidence:**
  - The log contains **19 entries** covering only stages C.10, C.11, C.13, C.14, C.16 and C.17 (`research/experiments.jsonl`, entries 1–19; stage field present from entry 5, `git_sha` and `logged_at` on all).
  - `grep -rn "log_experiment" --include=*.py .` shows callers in `research/__main__.py:222`, `research/carry/__main__.py:238`, `research/momentum/__main__.py:264`, `research/medium/__main__.py:198`, `research/deep/__main__.py:172`, `research/pairs/__main__.py:311`, `research/cross/__main__.py:146`, `research/diagnostics/__main__.py:357` — and in **no module under `research/microstructure/` or `research/detection/`**.
  - The uncovered tracks are exactly the ones that produced the repository's positives: the C.9 spread-to-cost survey (`research/microstructure/census.py`), the C.18/C.27 registered census that produced "the project's first bar-clearing positive" (progress.md:2527; `research/microstructure/registered.py`), the D.1a/D.1c/D.1d fill-simulation chain (`research/microstructure/{horizons,inventory,tick,fill_replay,d1c,d1d}.py`) and the whole detection track C.20–C.26 including the shipped scorer and D2 (`research/detection/*`).
  - The gap matters for exactly the reason the docstring gives. The census's BH ran "across at most ten p-values, and the screen that chose those ten was spread-motivated" (AUDIT.md:288-290); D2's grid was "18 cells … (3 cutoffs × 3 sets × 2 labels)" (report.md:3640-3642) plus C.25's stratum decomposition and C.26's re-estimate — none of these trial counts is in the registry that exists to hold them.
  - The same absence is acknowledged from the other side by the audit's scope note: "**Explicitly still unaudited:** H1, H2, H4, H5, H8–H11" (progress.md:2758-2760).
- **Recomputation (if any):** none — the claim is a coverage claim; the 19 entries and the caller set are enumerable directly.
- **What would resolve it:** Either log the microstructure and detection runs (the modules already have `main()` entry points that would take one call each), or restate the docstring's scope as "Phase B and the daily-bar studies" so the registry is not read as the project's complete trial record.
- **Confidence:** HIGH — the entry list and the caller grep are exhaustive and the docstring's claim is verbatim.
- **Invalidated by later commits?:** no — `research/experiments.jsonl` last gains an entry at `370ba41` (C.17, 2026-08-06) and no later commit adds a logging call.
- **Disclosed by authors?:** no — no document states that the census, the fill replays or the detection track are outside the experiment log; progress.md:298-303 introduces the log as part of the Phase B deliverable without a scope limit.

---

### DRAFT-p3-progress-10
- **Repository / SHA:** MLCryptoEngine / 5359a11fc753cdcd2606aea991dae826293d0307
- **Hypothesis or artifact:** the two documents the project nominates as a future reader's entry points (`HYPOTHESES.md`, `README.md`) versus the terminal state recorded in `progress.md`
- **Direction:** B
- **Class:** STALE_FIGURE
- **Severity:** S3
- **Label:** DERIVED
- **Claim challenged (verbatim quote):** "Two clocks still read out for the record: the Hyperliquid latency distribution (2026-08-19, moot for the sign) and the blind-universe scoring window (2026-09-09, now a selection-bias check)." — MLCryptoEngine/HYPOTHESES.md:263-266 (primary evidence for the contradiction is progress.md, which is mine).
- **Evidence:**
  - Recording and telemetry were stopped and disabled nine days before either clock could read out: "**Recording stopped 2026-08-13T05:02:49Z.** `mlce-recorder` and `mlce-telemetry` were stopped and disabled through systemd … No recorder or telemetry process remains." — MLCryptoEngine/progress.md:2765-2769.
  - The blind window is explicitly declared unusable in the same entry: "The 27-instrument blind universe subscribed on 2026-08-12 is therefore left with 1 day of capture and is **not** a scoreable window; it should not be treated as one." — MLCryptoEngine/progress.md:2782-2784.
  - The commit that recorded this touched nothing else: `git -C <live> show --stat aeabff6` → `progress.md | 44 ++++++++++`, one file changed. `HYPOTHESES.md`, `README.md`, `report.md` and `CLAUDE.md` were not updated, and the two later commits (`ae03bf6`, `5359a11`) do not revisit them.
  - The same entry tells a future reader to start from the un-updated document: "**What a future reader should start from.** `HYPOTHESES.md` for the register and every reopening condition" — MLCryptoEngine/progress.md:2798-2800.
  - `README.md` is stale in the same direction and more broadly: it presents the project as an in-flight recording pipeline — "**Stage 1 (this codebase) records and validates public market data only.**" (README.md:8-10), "The recorder is meant to run continuously — Phase B needs many days across different volatility regimes" (README.md:61-64), "**Phase A** — data pipeline, storage, order book reconstruction validated *(current)*" (README.md:79) — with a venue table listing Kraken, Coinbase and CME (README.md:14-18) when Kraken and Coinbase were retired at D.1b (progress.md:2660-2663) and Hyperliquid, the venue every positive was measured on, does not appear at all.
  - The anchor date (2026-08-22) is already past the first clock and the audit read date (2026-09-12) is past the second, so neither statement can still come true.
- **Recomputation (if any):** none — the contradiction is between dated statements in two files and one git `--stat`.
- **What would resolve it:** Update the register's project-wide-open-items paragraph and the README to the state progress.md records: recording ended 2026-08-13, both clocks are dead, Kraken and Coinbase retired, Hyperliquid the only venue with a positive, and the alpha search concluded by decision.
- **Confidence:** HIGH — dates, the single-file commit and the contradictory sentences are all directly checkable.
- **Invalidated by later commits?:** no — `5359a11` is the anchor and the tip; nothing after `aeabff6` touches either file.
- **Disclosed by authors?:** no — progress.md states the terminal facts, but neither the register nor the README acknowledges them, and the register is the document progress.md itself directs a future reader to.

---

### DRAFT-p3-progress-11
- **Repository / SHA:** MLCryptoEngine / 5359a11fc753cdcd2606aea991dae826293d0307
- **Hypothesis or artifact:** the A10 fee-centralisation remediation (`research/microstructure/fees.py`) and the fee constants that survived it
- **Direction:** B
- **Class:** INTERNAL_INCONSISTENCY
- **Severity:** S4
- **Label:** DERIVED
- **Claim challenged (verbatim quote):** "**A10/A11/A12** — fee centralised into `research/microstructure/fees.py` with a source, a date, and `ROUND_TRIP = 2 × MAKER` derived" — MLCryptoEngine/progress.md:2747-2749; the module's own claim: "The one place the Hyperliquid fee schedule is stated (audit finding A10)." — MLCryptoEngine/research/microstructure/fees.py:1.
- **Evidence:**
  - `research/microstructure/horizons.py:27` still declares `ROUND_TRIP_BPS = 3.0` as an undated, unsourced literal, used at `:99` to compute every D.1c long-horizon net (`net = armed.spread_bps - adverse - ROUND_TRIP_BPS`). Those are the figures quoted as "PUMP +4.17 (CI +4.04) / +4.49 (CI +4.28), MERL +6.06 (CI +5.45) / +6.08 (CI +5.21)" at MLCryptoEngine/progress.md:2612-2614. `git -C <live> show --stat d2a0f05` lists twelve changed files and `research/microstructure/horizons.py` is not among them.
  - `research/microstructure/reference_replay.py:77` carries a second literal `maker_fee_bps: float = 1.5`, created in the same commit that created `fees.py`.
  - `research/carry/trade.py:42-44` hardcodes `SPOT_COST_BPS_PER_SIDE = 40.0` under the comment "`# Kraken base-tier spot maker, per side, as corrected 2026-08-01 in # config/venues.yaml. Coinbase's base tier is the same 40 bps.`" That attribution was reversed on 2026-08-08: "base tier corrected 0.40/0.80 → **0.25/0.40** … the old figure was the non-Pro retail fees" (MLCryptoEngine/progress.md:1385-1388), and `config/venues.yaml:60` now reads `maker_bps: 25`. `git log -- research/carry/trade.py` returns a single commit, `2382aca` (2026-08-04), four days before the correction. The number remains correct for Coinbase, so the C.11 result is unaffected in direction (a 25 bps Kraken leg would raise, not lower, the reported carry), but the provenance comment is false at the anchor.
  - This is the exact defect class the repository made a standing rule about: "Every fee schedule in this project has been found stale at least once (ADR-012)" — MLCryptoEngine/HYPOTHESES.md:297-298 — and the one `fees.py` was written to eliminate: "Three independently maintained restatements of one fact, with nothing enforcing `ROUND_TRIP == 2 x MAKER`, is the same exposure." (fees.py:7-10).
- **Recomputation (if any):** none — the constants are identical in value today (1.5 / 3.0), so no published number changes; the finding is that the claimed single source of truth is three sources.
- **What would resolve it:** Import `HYPERLIQUID_MAKER_ROUND_TRIP_BPS` in `horizons.py` (and decide explicitly whether `reference_replay.py`'s independence is intended, saying so), and either point `research/carry/trade.py` at `config/venues.yaml` or correct its comment to name Coinbase.
- **Confidence:** HIGH — three greppable literals and one git `--stat`.
- **Invalidated by later commits?:** no — `d2a0f05` is the last commit touching `research/microstructure/`, and `research/carry/` has not been touched since 2026-08-04.
- **Disclosed by authors?:** no — progress.md:2747-2749 and fees.py:1 both assert the centralisation is complete; no document lists the surviving literals.

---

### DRAFT-p3-progress-12
- **Repository / SHA:** MLCryptoEngine / 5359a11fc753cdcd2606aea991dae826293d0307
- **Hypothesis or artifact:** the A8 capacity-divisor correction in the registered census (`research/microstructure/registered.py`)
- **Direction:** B
- **Class:** INTERNAL_INCONSISTENCY
- **Severity:** S4
- **Label:** DERIVED
- **Claim challenged (verbatim quote):** "capacity tier now divides by the recorded span, not 7 calendar days." — MLCryptoEngine/progress.md:2745-2746
- **Evidence:**
  - The correction was implemented as a default parameter set to the uncorrected value: `research/microstructure/registered.py:212-213` — `def instrument_report(inst: RegisteredInstrument, recorded_ns: int = SCORED_END_NS - SCORED_START_NS)` — where `SCORED_END_NS - SCORED_START_NS` is exactly the **7 calendar days** of the scored window (`:50-51`).
  - The only production caller passes nothing: `registered.py:390` — `reports = [instrument_report(instruments[coin]) for coin in sorted(instruments)]`. `grep -rn "instrument_report" --include=*.py .` finds no other non-test caller.
  - The docstring beside it describes the behaviour the call path does not produce: "A8: divide by the span actually recorded. The window is 7 calendar days but a ~5.75 h recorder hole on 08-04 means 96.4% of it was captured, and crediting the missing hours understates every instrument's rate." (`registered.py:257-259`).
  - The hole is real and reported elsewhere: "**08-04 at 76.3%** (a ~5.75 h recorder downtime, first half)" — MLCryptoEngine/progress.md:2519-2521.
  - Direction: the uncorrected divisor **understates** trades/day by ~3.6%, so the capacity bar is harder, not easier; no instrument's verdict turns on it (PUMP ≈ 73,900 trades/day and GMX ≈ 3,820 against a 150/day floor, from `audit/census_ci.json` `trades_per_sec` 0.8555 and 0.04423). The finding is that a stated remediation is inert in the shipped path, not that a number is wrong.
- **Recomputation (if any):**
  - Inputs: `SCORED_START_NS = 1_785_801_600_000_000_000`, `SCORED_END_NS = 1_786_406_400_000_000_000` (`registered.py:50-51`), recorded coverage 96.4% (progress.md:2519-2521). Method: compare the default divisor with the recorded span.
    Result: default divisor = **7.000 days**; recorded span ≈ 6.748 days; `trades_per_day` as shipped is **3.6% lower** than the A8-corrected value.
- **What would resolve it:** Pass the measured recorded span at `registered.py:390` (or default the parameter to it), or correct progress.md:2745-2746 to say the corrected divisor is available but not applied in the scored run.
- **Confidence:** HIGH — the default value, the single caller and the docstring are three adjacent lines in one file.
- **Invalidated by later commits?:** no — `d2a0f05` is the last commit touching the file.
- **Disclosed by authors?:** no — progress.md:2745-2746 and the commit message for `d2a0f05` both state the correction is applied.

---

## What I checked and found sound

Listed with the file references I checked, and what I would have expected to find if my thesis held there.

- **Pre-registration ordering is genuinely clean.** I checked every registration commit against the commit that produced its results with `git log --date=iso-strict`: C.14 bars `a2d7466` 2026-08-04T23:47 precede `17df5ad` 00:11 and `ddf525d` 03:46; C.16 `88b69d8` 2026-08-05T22:09 precedes `022a059`; C.17 `370ba41` 2026-08-06T07:02 precedes `4f1b030`; C.18 `6025f5c` 2026-08-06T12:18 precedes both the machinery `287fc10` and the census run `deb041b` 2026-08-10T23:56; D.1a `513d2c1`, D.1c `4b8bc1f`, D.1d `6a17edf` each precede their result commits by 20–40 minutes. I found no bar edited after its data existed. The one code-versus-text divergence (`rho >= 0.10` signed versus `max|rho|`) was fixed toward the registered text in `5430eba` and reported as INCONCLUSIVE rather than rewritten (progress.md:1690-1699, report.md:2318-2325).
- **The C.18 census guard is a real guard, not a comment.** `research/microstructure/registered.py:336-343` raises before `SCORED_END_NS`, `run_registered_census:385` calls it first, and `run_census`'s `coins` allowlist (`research/microstructure/census.py:93-98, 116, 135`) excludes the thin population at parse level so the known-answer validation cannot touch it.
- **The known-answer gates reproduce.** `known_answer` (`registered.py:394-426`) recomputes C.9's own measure on C.9's own window and the published deltas are −0.001 / −0.0033 bps (progress.md:2160-2163). D.1d's gate reproduces D.1c to the digit (progress.md:2699-2703). I checked the arithmetic of C.9's nets from the published components: 0.164 − 0.215 − 3.0 = −3.051, 0.545 − 0.298 − 3.0 = −2.753, and report.md:1214's 2.640 − 0.678 − 6.211 = −4.249, all matching.
- **The census net formula is right, not double- or half-counting.** I checked whether `net = spread − adverse − round_trip` (registered.py:21-22, 177) should charge two adverse legs against a full spread. It should not: over one passive round trip (buy at bid at mid *M₁*, sell at ask at mid *M₂ = M₁ − adverse*) the P&L is `S − adverse`, and the sell fill's own adverse move accrues to the next round trip's entry level rather than to this one. One adverse term against a full spread and two maker legs is the correct accounting.
- **Spread is time-weighted, not update-weighted, and crossed quotes are excluded rather than folded in.** `research/microstructure/spread.py:213-247` credits elapsed time to the *previous* spread and routes `bps <= 0` to a separate counter. That is the conservative choice and the docstring says why (spread.py:145-162).
- **Adverse-selection resolution never reads the future.** `research/microstructure/adverse.py:347-364` and the identical semantics in `registered.py:105-124` and `horizons.py:83-104` resolve a deadline strictly before a quote against the *previous* mid. I looked specifically for an off-by-one that would resolve against a later mid and did not find one.
- **The deflated-Sharpe implementation is correct.** `research/pairs/validation.py:99-135` matches Bailey & López de Prado: `E[max SR]` uses the standard two-term approximation and the DSR denominator is `1 − γ₃·SR + ((γ₄−1)/4)·SR²`. `sharpe_dispersion` (`:166-184`) measures σ̂(SR) from the study's own trials rather than assuming it.
- **The cost model refuses rather than guesses on per-contract venues.** `research/labels/costs.py:60-78` raises when a per-contract fee has no price to convert against, and `cost_model_from_config:112-120` raises when a contract multiplier is undeclared. Its maker branch (`:80-100`) explicitly pays no spread and says so — an assumption that flatters the maker EV, which makes the negative H1/H2 verdicts a-fortiori rather than fragile.
- **The capability matrix is closed by default and enforced in code.** `research/features/capabilities.py:1-45` documents the measured cadences that govern it, `SUB_100MS_FEATURES` exists because 100 ms bins against a 123 ms median are not measurable, undeclared venues raise, and `assert_stream_supports` reads the parser's own emitted channels rather than a hand-kept list.
- **The leakage discipline is real and its probes are shown capable of firing.** `research/deep/leakage.py:47-58` trains probes harder than the models they police (ADR-040), and `research/detection/behavior.py:129-153` refuses a pool whose label event is at or before the cutoff instead of clamping it in. C.14's canary fired at AUC 0.9714 with the label-shift control at 0.5268 (progress.md:1720-1724).
- **The C.10 look-ahead bug is self-reported and the fix is the conservative one.** progress.md:1454-1461 — the highest-ranked result in the study was the bug, `start` is now indexed by date, and the pair was excluded rather than truncated. I checked `research/pairs/` for a surviving offset-based start and found the `searchsorted` form.
- **Survivorship handling in C.10/C.13/C.16 is genuinely unusual and correct.** Binance monthly dumps retain delisted directories, selection is by the *first* month's volume (progress.md:1414-1421), ticker reuse (LUNA, BTT) is excluded entirely rather than spliced, and C.16 reuses the cached universe verbatim with a rebuild treated as an error (progress.md:1795-1801).
- **Budget arithmetic reconciles.** I recomputed every ledger step: C.3 components 2.5686+0.5698+0.0652+0.0018 = **3.2054**; C.4 3.0288 ≈ the stated 3.0289; cumulative 6.2343; C.7 6.2343+21.1582+18.4347+35.5144 = **81.3416**; remaining 38.6584; June-only retry leaving 38.6584−35.5144 = **3.14**; reversal restoring 38.6584+35.5144 = **74.17**; four months then leaving 74.1728−57.4835 = **16.69**; C.9 81.3416+0.7763 = **82.1179** with **37.8821** left. Every published figure matches. The single blemish is progress.md:713 quoting "$3.2053" where its own components sum to $3.2054 and every later figure uses $3.2054 — a one-hundredth-of-a-cent transcription slip, not a finding.
- **Other published arithmetic I recomputed and found correct:** C.8's −76.69 and −5.11 EVs; C.2's 3.9 and 3.3 bps gaps from the cost floor; C.3's $791/yr and $17/yr and C.4's $190/yr and $573/yr extrapolations and their 3× ratio; C.10's 82.7 expected hits from 1,653 pairs at α=0.05, the 1.74× lift from 18/175 against 5.9%, the 36 pairs from 9 instruments and 1.8 expected hits; C.11's 102 bps on MET's $191 notional; C.13's 43.68 − 42.91 − 0.66 = +0.11; D.1d's −5.98 / −10.90 falls from D.1c; E.1's 1,700×, 100× and 16× (the last against the superseded cost — see DRAFT-p3-progress-6).
- **The shipped D.1d reports carry the *corrected* numbers, not the published-then-superseded ones.** I checked the live artifacts against the A4 correction: `expectancy_bps_net` is −4.8087 (PUMP), −4.3459 (MERL base), −6.3503 (MERL improved), matching report.md:5121-5125 rather than the pre-correction −4.75/−4.23. I expected to find stale artifacts here and did not.
- **The engineering self-corrections are honest about direction.** The gap-accounting chain (Stage 1.5/1.6/C.3/C.6/C.8, five instances of the same interval defect), the coverage numerator that "became a 34-point lie on 2026-08-01" (progress.md:262-268), the C.3→C.4 withdrawal of the MBT sparsity finding as "wrong by an order of magnitude" with ADR-016 left unedited as the record, and the E.2 finding that the memory guard was measuring pytest (progress.md:2944-2977) are all cases where a comfortable number was retracted. I looked for a self-correction that moved a verdict toward the author's preference and did not find one; every retraction I traced moved against it.

## Live-repo access log

Live repository touched: `/home/kiros-li/Documents/GitHub/MLCryptoEngine`, read-only, for (1) `git log|show|show --stat` provenance and (2) reading untracked/gitignored artifacts under `logs/` and `data/processed/`. No write, checkout, or script execution.

`git -C /home/kiros-li/Documents/GitHub/MLCryptoEngine status --porcelain` **before** first access:

```
```
(empty — clean working tree)

`git -C /home/kiros-li/Documents/GitHub/MLCryptoEngine status --porcelain` **after** last access:

```
```
(empty — clean working tree; unchanged)
