# MLCryptoEngine — verification (Agent C, VERIFY)

**Repository:** MLCryptoEngine · **Anchored SHA:** `5359a11fc753cdcd2606aea991dae826293d0307` (main, 2026-08-22)
**Snapshot read:** `/home/kiros-li/.cache/program-audit/scratchpad/snap/MLCryptoEngine/` · **Live repo (read-only):** `/home/kiros-li/Documents/GitHub/MLCryptoEngine/`
**Agent:** C — referee and verifier. No thesis. **Task:** VERIFY the claims located in `MLCryptoEngine.inventory.md`.
**Work dir:** `/home/kiros-li/.cache/program-audit/scratchpad/work/agentC-MLCryptoEngine/` · **Python:** scratchpad venv (numpy 2.5.2 / scipy 1.18.1 / pandas 3.0.5)
**Verification window (UTC):** 2026-09-12T22:32:09Z – 22:51:16Z

**Headline of this pass.** Nineteen of twenty ranked claims were taken to their source. The project is, on the
whole, unusually verifiable: the D.1d headline (`−4.81 / −4.35`), the whole corrected headline table, the
latency grid, the A2/A4/A5/A13 corrections, the C.27 census table, the D.1c inventory and 300/900 s tables,
H1's `3.31 / 80.00 / 0.596 / −76.69`, H4's deflated Sharpe `0.026` (reproduced from the estimator, not merely
read back), H5, H8, H9, H11, D1's `0.984 @ 0.538`, the three-venue 2026-08-03 validation figures and H10's
"zero identifiable liquidations" all reproduce from stored primitives or from my own sweep of the raw capture.
Pre-registration also verifies from git objects: every line of all six `progress.md` registration blocks
survives verbatim into the anchored tree, and every registered result postdates its registration commit.

Three things do not hold, and one of them is load-bearing. **The day-clustered lower bounds the report quotes
for the A3 correction (`+3.59 / +1.73 / −0.070`) are not what the repository's own corrected code, nor its own
tracked audit artifact, produces (`+3.739 / +2.698 / +0.028`).** The quoted figures require a *two-sided*
t(6) = 2.4469 critical value; both `research/microstructure/registered.py:189` and `audit/census_ci.py:126`
apply the *one-sided* t(6) = 1.943 the registered bar calls for. GMX's demotion from "survivor" to
"unresolved" — the only category change in the whole audit — is produced entirely by that substitution, and is
reversed by the repository's own A6 correction stated eight lines below it.

---

## 1. Claims table

Tolerance convention: a figure quoted to *k* decimals verifies if it agrees to within half a unit in the last
printed place, unless a tighter tolerance is stated. "SNAP" = anchored snapshot; "LIVE" = gitignored working
tree, **UNANCHORED**, read 2026-09-12 (times in the access log).

| ID | Claim (short) | Stated | Source of truth | Recomputed | Tol | Status |
|---|---|---|---|---|---|---|
| MLCE-C01 | D.1d corrected headline net at declared cap + 162 ms floor | PUMP −4.81, MERL −4.35 bps | LIVE `logs/d1d_summary.json` `variants.{PUMP,MERL}.base.net_bps`; LIVE `data/processed/reports/d1d_{PUMP,MERL}_base.json` `expectancy_bps_net` | −4.8086852205937705 / −4.345949946241689 (both files bit-identical) | ±0.005 | **VERIFIED** |
| MLCE-C01b | Rest of the corrected headline table (report.md:5124-5130) | 5×/10× cap −4.87/−4.76 and −6.53/−11.14; MERL improved −6.35; notional $14.06M/$1.11M; ALO 0.77%/0.19%; zero-crossing none | LIVE `logs/d1d_summary.json` | −4.8682/−4.7568; −6.5312/−11.1443; −6.3503; 14,055,243/1,105,002; 0.7656%/0.1881%; `zero_crossing_ms = {PUMP: null, MERL: null}` | ±0.005 / ±0.005% | **VERIFIED** (every cell) |
| MLCE-C02 | C.27 census table, ten instruments | e.g. PUMP +4.30 (CI +4.27), MERL +6.45 (+6.07), GMX +0.40 (+0.29) | SNAP `audit/census_ci.json` (**tracked**) `net_mean_bps`, `reported_ci95_lower_bps` | 4.3004/4.2677; 6.4502/6.0695; 0.4044/0.2881; all ten nets \|Δ\|≤0.0047, all ten CI lowers \|Δ\|≤0.0047 | ±0.005 | **VERIFIED** |
| MLCE-C02b | Census `trades` column vs scored n | PUMP 499,944 / MERL 25,378 / GMX 25,868 | SNAP `audit/census_ci.json` `n`; LIVE `logs/d1c_summary.json` `horizons[*].trades`, `trades_without_quote` | d1c `trades` matches the report column **exactly** for all ten; census `n` is lower by 30 (eight instruments), 32 (PUMP), 35 (HYPE), 54 (SOL) | exact | **VERIFIED** (the gap is `trades_without_quote`, 30 each, plus 2/5/24 more on PUMP/HYPE/SOL) |
| MLCE-C03 | "PUMP and MERL survive every correction (day-clustered +3.59 and +1.73) … GMX does not: … **−0.070** day-clustered" | +3.59 / +1.73 / −0.070 | SNAP `audit/census_ci.json` `day_cluster_se`, `day_cluster_ci95_lower_bps`; SNAP `research/microstructure/registered.py`:183-192; SNAP `audit/census_ci.py`:126 | Artifact and code both give **+3.7391 / +2.6981 / +0.0281** (one-sided t(6)=1.943). The quoted figures reproduce **only** under two-sided t(6)=2.4469: +3.5935 / +1.7250 / −0.0695 | ±0.005 | **CONTRADICTED** → DRAFT-V-1 |
| MLCE-C03b | Block-bootstrap 90% lower bounds | +4.16 / +5.12 / +0.101 | SNAP `audit/census_ci.json` `block_bootstrap_ci90_lower_bps` | 4.161522210384049 / 5.1228180387761 / 0.10088443048485143 | ±0.005 | **VERIFIED** |
| MLCE-C04 | A2 corrected no-crossing counterfactual | PUMP −4.35, MERL −2.13; fills 24,394 / 3,370 vs subtraction's 23,333 / 3,293 | SNAP `audit/variants_base.json` (**tracked**) `variants.*.no_crossing` | −4.351918 / −2.134605; fills 24,394 / 3,370; base fills − crossings = 32,018−8,685 = 23,333 and 4,270−977 = 3,293 | ±0.005 / exact | **VERIFIED** |
| MLCE-C04b | The same counterfactual as restated in the verdict caveats | "deleting every crossing fill still leaves both instruments negative (**−3.98 / −2.57**)" (report.md:5003) | Same artifact; report.md:4925-4937 withdraws exactly these two numbers | Superseded values still quoted 66 lines after their withdrawal | — | **CONTRADICTED (stale restatement)** → DRAFT-V-4 |
| MLCE-C05 | Latency grid; "no zero-crossing exists" | published −4.75…−4.63 / −4.23…−5.83; corrected −4.81…−4.66 / −4.35…−5.89 | LIVE `logs/d1d_summary_published_2026-08-12.json` and `logs/d1d_summary.json` `latency_grid` | Every one of the 24 grid values reproduces to the printed digit; `zero_crossing_ms` null on both instruments in both files | ±0.005 | **VERIFIED** |
| MLCE-C06 | H1 deciding number | 3.31 bps capture at 900 s vs 80.00 bps cost; AUC 0.596; net EV −76.69; "fails by 23×" | SNAP `research/experiments.jsonl` run 1 (**tracked**), `results['coinbase BTC-USD'].horizons['900000']`; SNAP `config/venues.yaml` coinbase tier 0 | AUC 0.5960; `ev_bps_net` −76.6941; capture = 80.00 − 76.6941 = **3.3059**; 76.69/3.31 = 23.17× | ±0.005 | **VERIFIED** |
| MLCE-C06b | H1 supersession by C.14 | four-day range −2.44 to +3.05 bps | SNAP `report.md`:2377-2378 (+3.05, +0.15, −2.44, +0.74) | Range reproduces from the four stated day values | exact | **VERIFIED (document-internal)** |
| MLCE-C07 | H2 "**AUC 0.501 at every horizon**" | 0.501 at every horizon | SNAP `research/experiments.jsonl` run 2; SNAP `report.md`:920 | Per-horizon AUC = 0.664 / 0.620 / 0.600 / 0.551 / 0.521 / 0.516 / 0.508 / **0.501**. 0.501 is the 900 s value only | exact | **CONTRADICTED** → DRAFT-V-3 |
| MLCE-C07b | H2 economics | 0.22 bps capture vs 5.33 bps cost; best net EV −5.11; +0.215 at 900 s reversing to −0.785 on the stride-1 control | SNAP `research/experiments.jsonl` runs 2 and 3 | run 2 900 s `ev_bps_net` −5.1094 (= −5.11); 5.33 − 0.215 = 5.115 ✓; run 3 − run 2 at 900 s vs 100 ms: Δcapture = −6.5760 − (−5.7897) = **−0.786** vs the claimed −0.785 | ±0.01 | **VERIFIED** |
| MLCE-C08 | H4 pairs closure | 0 of 180; 91 raw vs 77.0 expected; DSR 0.026; per-bar 0.0514 vs expected-max 0.1058; skew 3.78 / kurt 79.50; n=1,095; 1,653 trials | SNAP `research/experiments.jsonl` runs 5-8 `results.deflation.best_overall`, `formation`, `holdout` | formation `bh_corrected_hits` 180, holdout 0, `persisted_bh` 0; 91 / 77.0; 0.05141 / 0.10581; 3.776 / 79.496; 1,095; 1,653. DSR **recomputed from the Bailey–López de Prado formula = 0.02602** | ±0.001 | **VERIFIED** |
| MLCE-C09 | H9 momentum | primary net Sharpe 0.302 vs BTC 0.183; DSR 0.446; alpha t 1.01; 7/12; executable Sharpe 0.013 / DSR 0.223; best cell 0.647 → DSR 0.732; BE 66–265 bps | SNAP `research/experiments.jsonl` run 17 (git_sha 88b69d8d); SNAP `report.md`:2537-2603 | 0.302 / 0.183; 0.4462; 1.013; 7 of 12; 0.013 / 0.223; 0.653→0.647, DSR 0.732; BE over positive-gross-Sharpe cells = 66.7–265.0 | ±0.005 | **VERIFIED** |
| MLCE-C10 | H11 / C.17 final closure | 0 of 40 pass; best DSR 0.499 vs 0.95; best alpha t 1.35 vs 2; A 0/8 B 7/8 C 6/8 D 8/8 E 7/8; lags +1/+75/0/0 | SNAP `research/experiments.jsonl` run 18 (git_sha 370ba414); SNAP `report.md`:2756-2799 grid | `cells_passing_all_six` = []; `cells_scored` 40; max DSR in the 40-row grid = 0.499 (D/h2w/LS); max positive alpha t = 1.35 (same cell); consistency fractions 0.0/0.875/0.75/1.0/0.875; `lags_applied_days` {A:1,B:75,C:0,D:0} | exact | **VERIFIED** |
| MLCE-C11 | H8 cross-sectional carry | +43.68 / −42.91 / −0.66 = +0.11 %/yr; shortfall 3.89; maxDD −75.85; vol ratio 10.9×; corr −0.718; BE 1.76 vs 1.5 at 51.7× | SNAP `research/experiments.jsonl` run 14 `results.result`, `residual_price_risk`, `benchmark` | 43.68 − 42.91 − 0.66 = **+0.11**; `excess_over_cash_pct` −3.89; −75.85; 1.81/0.166 = **10.90**; −0.718; 1.76 / 1.5 / 51.7 | ±0.005 | **VERIFIED** |
| MLCE-C11b | H8 dispersion decay | "fell **77%**, from a 241.50% decile spread in 2023 to 53.45% in 2026" | SNAP `report.md`:2050-2053 (fixed-cohort table); `progress.md`:1704 | 1 − 53.45/241.50 = **77.87%** | ±1 pt | **VERIFIED** |
| MLCE-C12 | H5 funding carry | ETH 8.07% / BTC 8.00%; 5 of 10 clear 4% by 1.6–4.1 pts; BTC 30.61→11.92→5.13→1.94; MERL −22.38 / TNSR −32.41 | SNAP `report.md`:1709-1710, 1764-1773, 1690-1691, 1831-1835 | 8.07 / 8.00; five cells ≥4% with excesses 4.07, 4.00, 3.43, 1.86, 1.57 → 1.6–4.1 ✓; year series exact; −22.38 / −32.41 | ±0.005 | **VERIFIED** |
| MLCE-C12b | H5 "the yield has decayed **~85%**" | ~85% | Same sentence's own endpoints (30.61% in 2021 → 1.94% in 2026) | 1 − 1.94/30.61 = **93.7%**; 1 − 5.13/30.61 = 83.2%; 1 − 1.94/11.92 = 83.7% | — | **UNVERIFIABLE** — the "~85%" has no stated referent; it reproduces from 2021→2025 or 2024→2026 but not from the 2021→2026 endpoints the same sentence names |
| MLCE-C13 | D2 firming (C.26) | mid-stratum lift +0.032, SE 0.039, 95% CI [−0.045, +0.109] at n=103 (C.25 +0.051 at n=84) | SNAP `report.md`:3941-3951; LIVE `data/processed/detection/behavior_c25.csv` | 0.032 ± 1.96×0.039 = **[−0.0444, +0.1084]** ✓. Supporting artifact present with the stated shape: 422 rows, `source` c25_deep 166 ✓, honest total 328 ✓ | ±0.001 | **VERIFIED (interval arithmetic + artifact shape)**; the lift itself is not recomputable — see §6 |
| MLCE-C13b | D2 unaffordability arithmetic | "≈124,764 weighted … **~1.9× the entire 60,000 cap** … Against the **1,199 remaining** it is **~28×** over" (report.md:3926-3928) | SNAP `report.md`:3924-3928; LIVE `data/vendor/helius_credit_ledger.jsonl` (final `cumulative` = 58,801 → 1,199 remaining ✓) | 124,764/60,000 = **2.079×**; 124,764/1,199 = **104.06×**. The two ratios are also mutually impossible (60,000/1,199 = 50.0). HYPOTHESES.md:252 says "~2× the cap", which is right | ±0.1× | **CONTRADICTED** → DRAFT-V-5 |
| MLCE-C14 | D1 clearance scorer | precision 0.984 at recall 0.538 (2024 fold); alarm precision 0.464; 281 reached T0; 194 in the test fold | LIVE `data/processed/detection/hard_rug_scorer.meta.json`; LIVE `features_c23.csv` | 0.9844 / 0.5385; 0.4643; `features_c23.csv` = 281 rows of which `year=2024` is 194; meta `train_n` 87 + `test_n` 194 = 281 | ±0.001 | **VERIFIED** |
| MLCE-C15 | Infrastructure PASS, 2026-08-03, three venues | Kraken 16.7M msgs / 16.5M CRC32 / 0 failures; Coinbase 3.5M / 0 seq gaps; Hyperliquid 1.5M / 32,200 snapshots; 100.00% coverage outside gaps; 0 crossed/locked | SNAP `report.md`:1255-1339 validation transcript | Kraken 16,653,584 msgs, 16,531,192 checksums checked, 0 (0) fails; Coinbase 3,460,641, 0 (0) seq gaps; Hyperliquid 1,489,552, l2Book 32,200; every row "coverage excl. gaps" 100.00%, crossed 0 (0), locked 0 | rounding | **VERIFIED** against the document's own transcript (no machine artifact survives for that date — see §6) |
| MLCE-C16 | D.1a always-last bound | PUMP +2.15 (CI +2.00), MERL +5.42 (CI +4.88) | — | No D.1a summary exists in `logs/`, `data/processed/` or the snapshot; recomputation needs a full re-run of `registered.py`/`census.py` over the 14 GB raw tree | — | **UNVERIFIABLE — artifact absent** |
| MLCE-C16b | A11 unit reconciliation | "halve to +1.08 / +2.71"; "per round trip the bounded result is −9.62, not −4.81" | SNAP `report.md`:4980, 5177 | 2.15/2 = 1.075; 5.42/2 = 2.71; 2 × (−4.81) = −9.62 | ±0.005 | **VERIFIED (arithmetic)** |
| MLCE-C17 | D.1c inventory | PUMP inventory −33.07 vs edge +5.82; −$303k; cap restores ~+1.2 bps; 74% of gross edge forgone to avoid −$353k; 29.8% one-sided; MERL +6.7→+12.5; +3.98 uncapped | LIVE `logs/d1c_summary.json` `inventory` | −33.068 / +5.825; `net_usd` −303,013; capped nets +1.233/+1.241/+1.186; forgone 45,898 of 62,120 gross = **73.9%**; `inventory_usd` −352,651; `frac_time_at_cap` 0.2982; MERL +6.675→+12.515; +3.978 | ±0.005 | **VERIFIED** |
| MLCE-C17b | C.27 coverage | 2026-08-04 at 76.3%; window ~96.4% covered; ~5.75 h hole | LIVE `data/raw/venue=hyperliquid/sessions.jsonl` + `gaps.jsonl`; LIVE `logs/d1c_summary.json` `tick_geometry.*.quoted_hours` | Census-quoted span 162.3217 h of 168 → missing 5.6783 h = 05:40:42, exactly the 2026-08-04T05:40:40.982Z session restart. (24 − 5.6783)/24 = **76.34%**; (168 − 5.6783)/168 = 96.62%; net of the 0.113 h of in-window feed gaps, 96.55% | ±0.3 pt | **VERIFIED** (the "~96.4%" is 0.15 pt low; "three short feed gaps" on 08-08 confirmed: 229.8 s + 165.0 s + 1.0 s → 99.54% that day) |
| MLCE-C18 | "Free-archive acquisition with per-file provenance — **4,970 files**, each with source, URL, sha256 and retrieval date" | 4,970 files | LIVE `data/vendor/archive/manifest.jsonl`; `find data/vendor/archive -type f` | Manifest: **14,191 rows / 13,543 unique paths**; on disk: **13,543 files** (exact 1:1 with the manifest). Provenance completeness: **0 rows of 14,191 missing** source, url, sha256 or retrieved_at. Rows retrieved on/before the commit that wrote the claim (fd18ba2, 2026-08-04T20:03:13Z): **exactly 4,970** | exact | **CONTRADICTED (stale, not wrong when written)** → DRAFT-V-6 |
| MLCE-C19 | H10 "zero identifiable liquidations in 2,639,510 recorded fills (2026-08-01 → 2026-08-06, twelve instruments)"; one key-set; zero `liquidat` strings; 18.0% zero-hash | as stated | LIVE `data/raw/venue=hyperliquid/date=2026-08-0[1-6]` — my own streaming sweep of all 126 hour files (15,814,362 recorded messages) | **0** occurrences of `liquidat` (any case) in any channel. Fill key-set observed = exactly `(coin, hash, px, side, sz, tid, time, users)`, no `liquidation` key. Exactly **12** coins in the trades channel. Fills over the first 116 hour files (2026-08-01T18 → 2026-08-06T13) = 2,673,301, of which 2,664,891 unique `tid`; the 115-file prefix is 2,623,409, so the claimed **2,639,510 falls inside the last (partial) hour file** — exactly what a mid-hour run on 2026-08-06 produces. Zero-hash fills 477,970 = 17.9% | brackets | **VERIFIED** |
| MLCE-C20 | D.1b blind universe | bands 4/7/36/107/23 of 177; caps 3/5/5/6/6; 25 picks + 2 = 27; seed 20260812; session marker 1786510236894021684; earliest close 2026-09-09 | SNAP `research/microstructure/blind_universe.py`; SNAP `report.md`:4643-4660; LIVE `data/raw/venue=hyperliquid/sessions.jsonl` | 4+7+36+107+23 = **177** ✓; 3+5+5+6+6 = **25** ✓ and the five pick lists hold 3/5/5/6/6 names ✓; `SEED = 20260812` in the anchored rule ✓; the session marker is present verbatim as a `start` event = **2026-08-12T04:50:36.894Z**, 7 min 14 s after the registration commit 4bde24c (2026-08-12T04:43:22Z) ✓ | exact | **VERIFIED (arithmetic, seed, ordering)**; the 25 picks themselves are **UNVERIFIABLE** — the retrieved 177-perp ranking is not stored |
| MLCE-C21 | A8: "`trades_per_day` **now divides by the recorded span**" (report.md:5162-5163) | corrected | SNAP `research/microstructure/registered.py`:212-213, 260, 390 | `instrument_report(inst, recorded_ns = SCORED_END_NS − SCORED_START_NS)`; the only production call site (line 390) passes no `recorded_ns`, so the anchored code still divides by **7 calendar days** | exact | **CONTRADICTED** → DRAFT-V-2 (no category moves: PUMP 71,421/day vs 73,919/day, GMX 3,695 vs 3,825, floor 150) |
| MLCE-C22 | A5 isolation: "effect on the scored numbers … **none, to every digit**" | zero effect | LIVE `logs/d1d_summary.json` `variants.*.a5_only` vs `as_published` | PUMP −4.750295040717393 both; MERL −4.231438891792402 both; fills 32,018 / 4,270 both; placements 176,568 / 305,335 both | 15 s.f. | **VERIFIED** |
| MLCE-C23 | A4 table and its deltas | −4.7503/−4.2314 → −4.8087/−4.3459 (PUMP −0.058, MERL −0.115); cancels end −4.3944/−4.1436 (+0.356); MERL fills fall 41% | LIVE `logs/d1d_summary.json` | All six nets and four fill counts exact; −0.0584 / −0.1145; +0.3559; (4,270−2,536)/4,270 = **40.6%** | ±0.005 | **VERIFIED** |
| MLCE-C24 | A13 sign flip | PUMP realized edge −1.01 → +0.45 under a −5 ms `trades` shift; inventory −2.24 → −4.08; net negative under all three orderings with the published figure least negative | SNAP `audit/variants_{base,m5,p5}.json` (**tracked**, 28,658,883 records each) | edge −1.0115 → **+0.4464**; inventory −2.2387 → **−4.0758**; nets −4.7503 (0 ms), −5.1295 (−5 ms), −4.7578 (+5 ms) — the published 0 ms figure **is** the least negative | ±0.005 | **VERIFIED** |
| MLCE-C25 | D.1d per-rule attribution (report.md:4912-4914) | PUMP 20.1%/+1.23, 49.5%/−0.84, 30.3%/−2.77; MERL 9.5%/+1.21, 47.1%/−1.56, 43.4%/−4.91 | LIVE `logs/d1d_summary.json` `as_published.notional_by_reason`, `edge_bps_by_reason` | 20.13/49.54/30.34% and +1.2298/−0.8428/−2.7740; 9.51/47.12/43.37% and +1.2111/−1.5554/−4.9051 | ±0.005 | **VERIFIED** |
| MLCE-C26 | Task-5 PerformanceReport record counts (report.md:4957-4959) | 32,018 / 4,270 / 14,085 leg records; slippage +2.74 vs −1.01 | LIVE `data/processed/reports/d1d_*.json` | **31,875 / 2,536 / 14,085**; PUMP slippage +2.7553 vs **−1.2271** | exact | **CONTRADICTED (stale)** → DRAFT-V-8 (the correction block at 4965-4969 does say the reports were regenerated) |
| MLCE-C27 | Pre-registration: "every bar predates its result and **no threshold was ever edited**" (AUDIT.md:586-588) | clean | LIVE git objects (read-only `log`/`show`/`diff`) | All six `progress.md` registration commits (370ba41, 6025f5c, 88b69d8, a2d7466, 35e3466, 902d2e6) are **pure additions, docs-only**; **all 380 added lines survive verbatim** in `progress.md` at the anchor (0 missing); `progress.md` has 16 deletions in its whole history, all in five commits that touch no registration block. Every result postdates its registration: C.16 reg 2026-08-06T05:09:05Z → run 17 13:04:51Z; C.17 reg 14:02:46Z → run 18 18:23:31Z; C.14 reg 2026-08-05T06:47:14Z → runs 15/16 10:26/10:41Z; C.19 reg 2026-08-06T19:47:47Z → first Helius credit row 2026-08-07T03:04:53Z; D.1b reg 2026-08-12T04:43:22Z → subscription restart 04:50:36.894Z | exact | **VERIFIED** |
| MLCE-C28 | Fee provenance | `fees.py`:13-14 "Recorded here 2026-08-12 from the Hyperliquid published fee schedule"; `venues.yaml`:53-55 "verified 2026-08-01 (hiperwire.io …, supa.is …)" | SNAP both files | Same 1.5/4.5 figure, two different dates and two different kinds of source (venue vs third-party explainer); neither file references the other. The number itself is used consistently: `fees_bps` = 1.5000 in every D.1d variant, `ROUND_TRIP_BPS` = 3.0 derived | — | **VERIFIED as a value, PROVENANCE INCONSISTENT** (disclosed in part: `fees.py` calls itself "documented, not measured"; `venues.yaml` warns the CME line is unverified) |

---

## 2. Derived quantities table

| Derived quantity | Inputs (file:line) | Method | Result | Stated | Status |
|---|---|---|---|---|---|
| IID half-width scaling | `audit/census_ci.json` `reported_halfwidth_bps`, `sd_of_nets`, `n` | `halfwidth·√n/sd` for all ten | 1.959966 – 1.960687 | "= 1.9600 to four decimals" (report.md:5142) | **VERIFIED** |
| True IID SE | same | `sd/√n` | e.g. PUMP 0.016688, GMX 0.059362 | — | — |
| Artifact `iid_se` field | `audit/census_ci.py`:99 `(mean − ci95_lower)/1.6449` | compare with `sd/√n` | **1.191562× too large, identically for all ten** (the reported bound was scored two-sided at 1.96, not one-sided) | field named `iid_se` | **CONTRADICTED (artifact-internal)** → DRAFT-V-7 |
| Newey–West inflation | `newey_west_se` ÷ true IID SE | ratio across ten | **1.312 – 3.593** | "1.3–3.6×" (report.md:5143) | **VERIFIED** (against `sd/√n`; the artifact's own `nw_over_iid` field gives 1.101–3.015, which would not support the quoted range) |
| Day-cluster inflation | `day_cluster_se` ÷ true IID SE | ratio across ten | **2.238 – 28.058** | "2.2–28×" (report.md:5144) | **VERIFIED** (same caveat; artifact-field version gives 1.878–23.547) |
| Day-cluster SE | `day_means_bps` (7 values) | `sd(dm, ddof=1)/√7` | reproduces `day_cluster_se` to 4 d.p. for all ten | — | **VERIFIED** |
| PUMP interval widths | `reported_halfwidth_bps`, `newey_west_se`, `day_cluster_se` | ×1.96 / ×1.943 / ×2.4469 | ±0.0327 → HAC ±0.0665 → day-clustered ±0.5613 (one-sided t6) / ±0.7069 (two-sided t6) | "±0.03 … ±0.07 (HAC) or **±0.71** (day-clustered)" | **±0.03 and ±0.07 VERIFIED; ±0.71 requires the two-sided t(6)** (same substitution as DRAFT-V-1) |
| `p_one_sided_iid` | `net_mean_bps`, `sd_of_nets`, `n` | `student_t.sf(mean/(sd/√n), n−1)` | ARB 7.77e-08 (stored 7.769888e-08); GMX 5.46e-09 vs stored 4.884674e-12; MERL 1.05e-168 vs stored 4.48e-237 | stored values | **ARB VERIFIED; GMX/MERL differ** — the stored p uses `sd/√n` (registered.py:187) while the JSON's own `iid_se` field does not, and extreme-tail t-survival differs by scipy version/precision. Both are ≪ any BH threshold, so no decision moves |
| Deflated Sharpe, H4 | run 5 `per_bar_sharpe` 0.05141, `expected_max…` 0.10581, `observations` 1095, skew 3.776, kurt 79.496 | Bailey & López de Prado (2014) DSR | **0.02602** | 0.026 | **VERIFIED** |
| Deflated Sharpe cross-check | run 4 `best_overall` 0.21566 / 0.11377 / 131 / 3.082 / 17.681 | same formula | **0.94485** | 0.9448 | **VERIFIED** (confirms the estimator identity) |
| Expected max Sharpe under the null | `sharpe_dispersion_per_bar` 0.03116, N = 1,653 | `σ·[(1−γ)Φ⁻¹(1−1/N) + γΦ⁻¹(1−1/(Ne))]` | **0.105801** | 0.10581 | **VERIFIED** |
| H8 net | +43.68 − 42.91 − 0.66 | sum | **+0.11** | +0.11 | **VERIFIED** |
| H8 shortfall / vol ratio | 4.00 − 0.11; 1.81 ÷ 0.166 | arithmetic | 3.89; **10.90×** | 3.89; 10.9× | **VERIFIED** |
| H1 gross capture | 80.00 + (−76.6941) | arithmetic | **3.3059** | 3.31 | **VERIFIED** |
| H1 cost hurdle | `venues.yaml` coinbase tier-0 maker 40.0 bps/leg × 2 | arithmetic | **80.0** | 80.00 | **VERIFIED** |
| H6 fee hurdle | `fees.py`:36,42 `2.0 × 1.5` | arithmetic | **3.0** | 3.0 bps round trip everywhere | **VERIFIED** |
| D.1c forgone-edge share | `inventory` PUMP uncapped `edge_bps` 5.825 × notional 106,643,036; `forgone_edge_usd` 45,898 | 45,898 / 62,120 | **73.9%** | "74%" | **VERIFIED** |
| D.1c inventory avoided | `inventory_usd` uncapped | read | **−$352,651** | "−$353k" | **VERIFIED** |
| D.1c swamp factor | 33.068 / 5.825 | ratio | **5.677×** | "5.7×" | **VERIFIED** |
| D.1d funding boundaries | `funding` {applied 163, skipped 5} | sum | 168 | "163/168 boundaries applied" | **VERIFIED** |
| Audit-variant funding | `variants_*.json` `funding` {326, 10} | ÷2 symbols | 163 / 5 | consistent with d1d_summary | **VERIFIED** |
| A8 capacity rate | 499,944 ÷ 7 d vs ÷ 6.7634 d | ratio | 71,421/day vs 73,919/day (floor 150) | "clear the floor by ~300× either way" | **VERIFIED** (PUMP is ~476–493×, MERL ~24×; "~300×" is the report's own earlier 41–52k fills/day framing, not this ratio) |
| D2 interval | 0.032 ± 1.96 × 0.039 | normal interval | **[−0.0444, +0.1084]** | [−0.045, +0.109] | **VERIFIED** |
| C.26 cost ratios | 124,764 vs 60,000 and 1,199 | ratios | **2.079× and 104.06×** | "~1.9×" and "~28×" | **CONTRADICTED** → DRAFT-V-5 |
| H5 decay | 1 − 1.94/30.61 | ratio | **93.7%** | "~85%" | **UNVERIFIABLE (referent ambiguous)** |
| Coverage | (24 − 5.6783)/24; (168 − 5.6783)/168 | arithmetic from the session restart | **76.34%**; 96.62% (96.55% net of feed gaps) | 76.3%; ~96.4% | **VERIFIED** (96.4% is 0.15 pt low) |
| Archive manifest reconciliation | `manifest.jsonl` unique `path` vs `find … -type f` | set comparison | 13,543 = 13,543 | — | **VERIFIED (exact)** |
| Blind-universe band arithmetic | report.md:4643-4652 | sums | 177 members; 25 picks; 27 subscribed | 177 / 25 / 27 | **VERIFIED** |
| H10 zero-hash share | 477,970 ÷ 2,673,301 | ratio | **17.88%** | "18.0% of fills (473,824)" | **VERIFIED** (the claim's own 473,824/2,639,510 = 17.95%) |

---

## 3. Intervals table

| Interval (file:line) | Estimator actually used | Independence assumed? | Data structure | Reproduces from stored data? | Status |
|---|---|---|---|---|---|
| C.27 census CI95 lower, ten instruments (`report.md`:4047-4057) | Welford mean − 1.96·sd/√n on per-print `spread − adverse − 3.0` at the worst of 1/5/60 s. Confirmed twice: `halfwidth·√n/sd` = 1.9600 for all ten, and `registered.py`:184-186 `ci95_lower_bps_as_scored = mean − t(0.975, n−1)·se` | **Yes** — and wrongly: at 5 s and 60 s consecutive aggressor prints share overlapping forward windows | Per-print rows within instrument within UTC day; 3,282–1,150,493 rows | **Yes**, exactly, from `audit/census_ci.json` | **VERIFIED as published; the independence assumption is violated and the repo says so (A3)** |
| A3 day-clustered CI95 lower (`report.md`:5148-5153) | *Report:* mean − 2.4469·SE_day (two-sided t(6)). *Code (`registered.py`:189):* mean − `student_t.ppf(0.95, k−1)`·SE_day = one-sided t(6) = 1.943. *Artifact (`census_ci.py`:126):* literal 1.943 | Clusters assumed independent across 7 UTC days (reasonable); rows within a day unconstrained (the point of the correction) | 7 day clusters per instrument — a small-cluster regime where the t(6) reference is the right idea | **No.** Artifact gives +3.7391 / +2.6981 / +0.0281; report quotes +3.59 / +1.73 / −0.070 | **CONTRADICTED** → DRAFT-V-1 |
| A3 block-bootstrap CI90 lower (`report.md`:5150) | Moving-block bootstrap, block = max(lag, 50), 300 reps, 5th percentile of resampled means (`census_ci.py`:54-65) | No (that is its purpose) | Same per-print series | **Yes** — +4.1615 / +5.1228 / +0.10088 exactly | **VERIFIED** |
| A3 Newey–West CI95 lower (`census_ci.json` `nw_ci95_lower_bps`) | `mean − 1.6449·NW_se`, Bartlett kernel, lag = min(tps·h/1000, n/20, 3000) (`census_ci.py`:42-51, 98, 123) | No | Same | Yes, internally consistent | **VERIFIED as computed**; note the *bound* here is one-sided 1.6449 while the published bound it is compared against is two-sided 1.96 — the two are not like-for-like |
| D.1c 300 s / 900 s CI lowers (`report.md`:4483-4486) | Same IID Welford interval, no clustering correction | **Yes** | Same overlapping structure, with a 5–15× longer forward window than the horizons A3 was measured on | **Yes** — `logs/d1c_summary.json` `per_horizon.{300000,900000}.ci95_lower_bps` match every printed digit for both survivors and for the GMX reversal (−0.245 at 300 s, −0.756 at 900 s) | **VERIFIED as published**; A3's correction was never carried to these, and the report does not say it was — see §6 |
| D.1a always-last CI lower (`report.md`:4205-4206) | Same IID Welford interval on the sweep-restricted subset | **Yes** | Subset of the same overlapping rows | **No stored artifact** | **UNVERIFIABLE — artifact absent** |
| D2 precision-lift CI (`report.md`:3948) | Normal interval on a difference of precisions, SE ≈ 0.039 | Yes (pool-level cross-section, defensible); but the base rate is estimated on the same draw, so lift and base are not independent | Pool-level, Method-B depth-independent random draw, stratified by 6 h activity | Interval arithmetic reproduces exactly; the lift and its SE are **not** recomputable (stratum cut-points and per-pool scores are not stored) | **VERIFIED (arithmetic); INPUTS UNVERIFIABLE** |
| Latency p50/p95 floor, n = 7 (`report.md`:4632) | Empirical p50/p95 of 7 sequential REST probes from one host | n/a | Sequential probes, one host, one cycle | LIVE `logs/telemetry_latest.json` (generated 2026-08-13T05:02:48Z) shows p50 157.402 / p95 410.865 / p99 772.308 over 303 samples — the p50 is close, the p95 is **~2× the n = 7 value** | **VERIFIED as a reading of its own n = 7 sample**; the report labels it a proxy floor that "reads low" and the later 303-sample distribution confirms the tail is much fatter |
| H4 deflated Sharpe 0.026 (`report.md`:1585-1598) | Bailey & López de Prado DSR with skew/kurtosis adjustment, 1,653 trials | Serial independence of daily bar returns assumed by the DSR's √(T−1) term | Daily returns of one selected pair; report.md:1578-1583 discloses that two of twelve folds carry the return | **Yes** — recomputed 0.02602 from the stored primitives | **VERIFIED** |
| H9 deflated Sharpe 0.446 / 0.223 (`report.md`:2603) | DSR over 12 registered trials | Same | Daily long-short returns, net short (−0.275 mean exposure) | Value matches the ledger's `deflated_sharpe` exactly; the per-bar Sharpe, skew and kurtosis that feed it are **not** stored, so the estimator cannot be re-executed | **VERIFIED (agreement); NOT RE-EXECUTABLE** |
| H11 deflated Sharpe grid, best 0.499 (`report.md`:2754-2795) | DSR over 40 registered trials | Same, on weekly bars | Weekly ridge walk-forward, purge + embargo ≥ horizon; Class D cells have only 45–59 weeks | Grid maximum confirmed = 0.499; inputs not stored | **VERIFIED (agreement); NOT RE-EXECUTABLE** |

---

## 4. Tests table

| Test / statistic (file:line) | Tail | dof / distribution | Decision rule | Correction applied | Correction matches rule? | Reproduces? | Status |
|---|---|---|---|---|---|---|---|
| C.27 per-instrument one-sided net test (`report.md`:4043; `registered.py`:187, 288) | One-sided, matching the registered direction ("95% CI lower bound > 0") | `student_t.sf(mean/se, n−1)`, n = 3,282–1,150,493 | **Intersection-union per instrument** (BH-rejected **and** CI>0 **and** both-halves **and** capacity), then a **union across the ten instruments** for "who is a survivor" | Benjamini–Hochberg FDR, q = 0.10, across the ten tested (`multipletests(..., method="fdr_bh")`) | **Yes.** BH is a selection/union correction and it is applied exactly where the union is (which of ten instruments is declared). The four per-instrument components are a conjunction and correctly carry no further correction | p-values reproduce for ARB from `sd/√n`; GMX/MERL differ in the extreme tail only, far below any BH threshold | **VERIFIED** (the disclosed A7 caveat — BH covers the 10 tested, not the 177 screened — stands) |
| C.27 critical value, A6 (`report.md`:5155-5162) | Registered **one-sided**; scored **two-sided** 1.96 | t(n−1) | Same | A6 corrects the scored bound to one-sided 1.645 and keeps `ci95_lower_bps_as_scored` for reproducibility | **Yes as stated for the IID bound** — but the same section's A3 day-clustered figures go the *other* way, to two-sided t(6) = 2.4469, i.e. 26% *harder* than the registered one-sided t(6) = 1.943 | Yes: `registered.py`:183-186 implements both | **Mismatch inside the section** → DRAFT-V-1 |
| C.27 known-answer gate (`report.md`:4035-4038) | n/a | n/a | Reproduce C.9's BTC −3.05 / ETH −2.75 within ±0.5 bps | n/a | n/a | Targets are hard-coded at `registered.py`:70 `C9_KNOWN_NET_BPS = {"BTC": −3.05, "ETH": −2.75}` and the gate path (`known_answer`) does exercise the census accumulators; the *measured* −3.051/−2.753 have no stored output | **UNVERIFIABLE (output absent)** — and, unlike D.1d's gate, no A1-style line-coverage trace of this gate is recorded anywhere |
| D.1d known-answer gate, A1 (`report.md`:4809-4816, 5085-5105) | n/a | n/a | ±0.10 bps tolerance; **withdrawn** | n/a | n/a | `variants.PUMP.known_answer.net_bps` = 1.2328432875691382 and MERL 6.674559475354376 reproduce the quoted +1.23 / +6.67. The A1 defect (106 lines executing zero times) cannot be re-traced without running the code | **Figures VERIFIED; the A1 trace UNVERIFIABLE by recomputation.** Replacement gate present and substantive: `tests/test_fill_replay_gate.py` runs 8 seeds × cap × latency × queue-model against an independent implementation, asserts the full ledger, and carries a defect-detection control (`detected >= 5` of 6 streams) |
| C.10 Engle–Granger / Johansen with BH (`report.md`:1455-1470) | Cointegration tests, one-sided by construction | Per-pair EG/Johansen | **Union across 1,653 (formation) / 1,540 (holdout) pairs**: "does any pair survive" | Benjamini–Hochberg, q = 0.05 (`fdr_method: "fdr_bh"` in the ledger) | **Yes** — a union over pairs, corrected by FDR over pairs | Counts reproduce exactly from the ledger: 432 raw vs 82.7 expected → 180 BH; 91 vs 77.0 → 0 BH; Johansen 559 / 194; both-tests 167 / 0 | **VERIFIED** |
| C.10 named-pair p-values (`HYPOTHESES.md`:98) | As above | As above | Illustrative, not a decision | n/a | n/a | BTC/ETH p = 0.1169 / 0.9275 and ARB/GMX p = 0.0136 appear only in `report.md`:1555-1570; the ledger stores the aggregate counts, not per-pair p-values | **UNVERIFIABLE (per-pair statistics not stored)** |
| C.16 verdict (`report.md`:2607-2616) | alpha t two-sided OLS vs BTC, bar `t ≥ 2` (i.e. a one-sided read of a two-sided statistic, conservative) | OLS on ~1,800 daily bars | **Conjunction — all four bars required for PASS** | DSR over 12 registered trials on the Sharpe bar; **no** multiplicity correction on the alpha-t bar | **Yes.** A conjunction needs no per-component correction; the DSR is there because the cell was *selected*, and the outcome is FAIL, so an uncorrected alpha bar is conservative in the direction of the result | t = 1.013, DSR 0.4462, 7/12 all reproduce from the ledger; grid max alpha t = 1.95 confirms "no cell reaches t = 2" | **VERIFIED** |
| C.17 verdict (`report.md`:2798-2799) | Same | OLS on 45–207 weekly bars per cell | **Conjunction — "ALL required for PASS, anything short is FAIL"** (registered verbatim at 370ba41), evaluated over a **union of 40 cells** | DSR over the full registered 40-cell trial count ("no cell may be dropped from the denominator" — registered); no correction on the alpha-t bar | **Yes**, for the same reason; and the registered text explicitly fixes the deflation denominator in advance, which is the part most often fudged | `cells_passing_all_six` = []; grid max DSR 0.499, max positive alpha t 1.35; class fractions exact | **VERIFIED** |
| C.14 leakage canary (`report.md`:4880, 2442-2448) | n/a | n/a | Canary must fire at AUC ≥ 0.90 on a planted future column | n/a | n/a | AUC 0.9714 stated at report.md:2442 against a ≥ 0.90 bar; the ledger carries a `leakage_tests` field per run but the canary AUC is not in it | **VERIFIED document-internally; the per-run canary value is not stored in the ledger** |
| A13 feed-shift sensitivity (`report.md`:4885-4900) | n/a — a perturbation test, not a hypothesis test | n/a | Does the sign of *edge* survive a −5 ms `trades` shift? | n/a | n/a | Yes, exactly, from three tracked 28.7M-record replays | **VERIFIED** (and the conclusion drawn — withdraw the attribution, keep the net — is the conservative one) |
| A5 isolation (`report.md`:5070-5075) | n/a | n/a | Does the ALO-rejection defect move any scored number? | n/a | n/a | `a5_only` and `as_published` agree to 15 significant figures on nets, fills and placements | **VERIFIED** |
| A2 counterfactual (`report.md`:4925-4937) | n/a | n/a | Does the closure survive deleting the crossing rule? | n/a | n/a | Yes — `no_crossing` in all three tracked variant files | **VERIFIED**; the superseded figures survive at report.md:5003 → DRAFT-V-4 |
| H10 field-inventory test (`report.md`:2644-2652) | n/a | n/a | Does any recorded message carry a liquidation mark? | n/a | n/a | **Re-run independently**: 0 `liquidat` hits in 15,814,362 messages across 126 hour files; fill key-set is exactly the eight keys claimed | **VERIFIED by direct recomputation** |

---

## 5. Draft findings

Only contradictions and estimator/provenance mismatches are listed. Temporary IDs; the consolidator assigns final IDs.

### DRAFT-V-1
- **Repository / SHA:** MLCryptoEngine / `5359a11fc753cdcd2606aea991dae826293d0307`
- **Hypothesis or artifact:** H6 / C.27 census — audit finding A3's day-clustered lower bounds, and the demotion of GMX from "survivor @ capacity" to "unresolved"
- **Direction:** A
- **Class:** STATISTICAL
- **Severity:** S1
- **Label:** DERIVED
- **Claim challenged (verbatim quote):** "**PUMP and MERL survive every correction** (day-clustered lower bounds +3.59 and +1.73; block-bootstrap +4.16 and +5.12). **GMX does not**: it moves from `ci95_lower = +0.288` (survivor) to **−0.070** day-clustered, block-bootstrap +0.101 — straddling zero. GMX was one of C.27's three survivors and was already discounted to ~zero on independent grounds; it should now be read as **unresolved, not a survivor**." — MLCryptoEngine/report.md:5148-5153 (restated MLCryptoEngine/HYPOTHESES.md:198)
- **Evidence:**
  - The repository's own tracked evidence artifact gives the opposite sign for GMX: `day_cluster_ci95_lower_bps` = **+0.0281** (GMX), **+3.7391** (PUMP), **+2.6981** (MERL) — MLCryptoEngine/audit/census_ci.json (n = 10 instruments, 7 day clusters each; tracked at the anchor, read from SNAP).
  - The script that wrote it applies a **one-sided** critical value: `"day_cluster_ci95_lower_bps": st["net_mean_bps"] - 1.943 * day_se` — MLCryptoEngine/audit/census_ci.py:126. 1.943 = `t(0.95, 6)`, the one-sided t on 6 dof.
  - The anchored, post-audit production code does the same: `mean - float(student_t.ppf(CONFIDENCE, clusters - 1)) * day_se` with `CONFIDENCE = 0.95` — MLCryptoEngine/research/microstructure/registered.py:189 and :64. `t.ppf(0.95, 6)` = 1.943180.
  - The quoted figures require `t(0.975, 6)` = **2.446912**, a two-sided critical value implemented nowhere in the repository for this quantity.
  - The same paragraph block's A6 correction states the registered bar is one-sided: "**A6 — a one-sided bar was judged with a two-sided critical value.** C.27 used `t(0.975)` = 1.96 where a one-sided 95% bound needs 1.645, making the bar ~19% *harder* than registered. Corrected" — MLCryptoEngine/report.md:5155-5157. The A3 figures published eight lines above go the other way, to a critical value 26% harder than the registered one-sided t(6).
  - The error is decisive **only** for GMX. For the two survivors it runs the conservative way (PUMP +3.59 quoted vs +3.74 computed; MERL +1.73 vs +2.70), so DRAFT-V-1 does not disturb the D.1c/D.1d chain. GMX is the one instrument whose category changes, and it changes because of the substitution.
  - No stored output of the corrected `registered.py` run exists anywhere in the snapshot, `logs/` or `data/processed/` (checked 2026-09-12T22:39Z), so `audit/census_ci.json` is the only artifact for these figures.
- **Recomputation (if any):** Inputs: `net_mean_bps` and `day_cluster_se` per instrument, MLCryptoEngine/audit/census_ci.json. Method: `mean − c·SE_day` for c ∈ {1.943180 (one-sided t6), 1.96 (normal), 2.446912 (two-sided t6)}; `SE_day` independently reproduced as `sd(day_means, ddof=1)/√7` to 4 d.p. for all ten. Results — GMX: +0.0281 / +0.0248 / **−0.0695**; PUMP: +3.7390 / +3.7342 / **+3.5935**; MERL: +2.6978 / +2.6653 / **+1.7250**. Tolerance ±0.005 bps. Only the two-sided column matches the report. The same substitution explains the quoted "±0.71" day-clustered half-width for PUMP (2.4469 × 0.28887 = 0.7069; the one-sided value is 0.5613).
- **What would resolve it:** Either (a) publish the stored output of the corrected `registered.py` run showing which critical value produced the quoted bounds, or (b) restate A3's day-clustered bounds under the one-sided convention A6 says was registered — under which GMX's day-clustered lower bound is **+0.028** and its demotion to "unresolved" does not follow from A3 (it may still follow from the independent grounds the report cites at :4062-4085 and from the 300 s / 900 s sign reversal at :4495-4497, which are separate arguments).
- **Confidence:** HIGH — the artifact and both implementations are anchored and agree with each other and disagree with the document, and the discrepancy is exactly one critical-value substitution reproduced to four decimals on all three quoted instruments.
- **Invalidated by later commits?:** no — `registered.py`, `census_ci.py` and `census_ci.json` are all tracked at the anchored SHA and the working tree is clean at HEAD = the anchor.
- **Disclosed by authors?:** Partly. A6 (report.md:5155-5162) discloses that the registered bar was one-sided and that a two-sided value was used at scoring, and says the correction "only loosens". It does not disclose that the A3 day-clustered figures printed eight lines earlier use a two-sided critical value, does not report the artifact's own one-sided value of +0.028 for GMX, and asserts "No instrument's category moves between the two" while A3's GMX demotion — the only category move in the audit — is produced by precisely that choice.

### DRAFT-V-2
- **Repository / SHA:** MLCryptoEngine / `5359a11fc753cdcd2606aea991dae826293d0307`
- **Hypothesis or artifact:** C.27 capacity tier — audit finding A8's stated code correction
- **Direction:** neutral
- **Class:** PROVENANCE
- **Severity:** S3
- **Label:** DERIVED
- **Claim challenged (verbatim quote):** "**A8 — the capacity tier divided by 7 calendar days** despite a ~5.75 h recorder hole (96.4% coverage). `trades_per_day` now divides by the recorded span, and `median_daily_usd` takes a true median rather than the upper element on an even day count." — MLCryptoEngine/report.md:5161-5164
- **Evidence:**
  - The recorded-span divisor is a *default parameter*, not a value: `def instrument_report(inst: RegisteredInstrument, recorded_ns: int = SCORED_END_NS - SCORED_START_NS)` — MLCryptoEngine/research/microstructure/registered.py:212-213. `SCORED_END_NS − SCORED_START_NS` = 604,800,000,000,000 ns = exactly 7 calendar days (constants at :50-51).
  - `trades_per_day = inst.trades / max(1.0, recorded_ns / NS_PER_DAY)` — MLCryptoEngine/research/microstructure/registered.py:260.
  - The only production call site passes no override: `reports = [instrument_report(instruments[coin]) for coin in sorted(instruments)]` — MLCryptoEngine/research/microstructure/registered.py:390. A grep of `research/`, `tests/` and `audit/` finds no other caller supplying `recorded_ns` (2 further calls, both in tests/test_registered_census.py:149-150, also omit it).
  - So the anchored code still divides by 7 calendar days — the exact behaviour A8 says was corrected. The comment immediately above the line (:257-259) describes the corrected behaviour.
  - The companion half of A8 **is** applied: the true-median branch is at :250-256.
  - Impact is nil, as the authors state: PUMP 499,944/7 = 71,421 trades/day vs 499,944/6.7634 = 73,919; GMX 25,868/7 = 3,695 vs 3,825; the floor is 150/day.
- **Recomputation (if any):** Inputs `inst.trades` from `logs/d1c_summary.json` `horizons[*].trades` (LIVE, read 2026-09-12T22:40Z) and the recorded span 162.3217 h from `tick_geometry.PUMP.quoted_hours`. Method: divide by 7.0 days and by 162.3217/24 = 6.7634 days. Result: no instrument changes side of the 150/day floor; the two divisors differ by 3.5%.
- **What would resolve it:** Pass the recorded span at the call site (or recompute it from the session ledger inside `run_registered_census`), or restate A8 as "the divisor is parameterised; the published figures still use 7 calendar days, conservatively".
- **Confidence:** HIGH — three anchored lines of code, no other call site.
- **Invalidated by later commits?:** no — the file is tracked at the anchor and HEAD equals the anchor.
- **Disclosed by authors?:** The *consequence* is disclosed ("Both errors were conservative; PUMP and MERL clear the floor by ~300× either way, so no category moves", report.md:5164-5165). The *mechanism claim* — that the code now divides by the recorded span — is not, and is contradicted by the code.

### DRAFT-V-3
- **Repository / SHA:** MLCryptoEngine / `5359a11fc753cdcd2606aea991dae826293d0307`
- **Hypothesis or artifact:** H2 — the CME MBT "signal-absent" closure, deciding-number cell
- **Direction:** A
- **Class:** INTERNAL_INCONSISTENCY
- **Severity:** S3
- **Label:** DERIVED
- **Claim challenged (verbatim quote):** "**AUC 0.501** at every horizon, and **0.22 bps** gross capture against **5.33 bps** cost." — MLCryptoEngine/HYPOTHESES.md:66
- **Evidence:**
  - The stored ledger row for the run gives AUC by horizon **0.6640 (100 ms), 0.6204 (500 ms), 0.5997 (1 s), 0.5509 (5 s), 0.5211 (30 s), 0.5158 (60 s), 0.5085 (300 s), 0.5005 (900 s)**, n = 1,101,582–1,109,068 per horizon — MLCryptoEngine/research/experiments.jsonl run 2 (`run_id` 99ad7dde, git_sha a958c0d6, 53 dates, stride 4), `results['cme MBT'].horizons[*].auc`.
  - The project's own report states the same decay in one line: "Predictability decay (AUC by horizon): 100 ms: 0.664 · 500 ms: 0.620 · 1000 ms: 0.600 · 5000 ms: 0.551 · 30000 ms: 0.521 · 60000 ms: 0.516 · 300000 ms: 0.508 · 900000 ms: 0.501" — MLCryptoEngine/report.md:920.
  - Elsewhere the report states the scope correctly: "On CME MBT AUC was 0.501 at 900 s, a coin flip" — MLCryptoEngine/report.md:2255.
  - The rest of the H2 cell verifies: 900 s `ev_bps_net` = −5.1094 (stated −5.11); 5.33 − 0.215 = 5.115; and the stride-1 control's 900 s reversal recomputes to −0.786 against the stated −0.785.
- **Recomputation (if any):** Inputs: `research/experiments.jsonl` run 2, `results['cme MBT'].horizons`. Method: read the eight `auc` values and the eight `cost_modes.maker.model_classifier.ev_bps_net` values; capture differences taken against the 100 ms row. Result: AUC ranges 0.5005–0.6640, not 0.501; capture at 900 s = ev(900 s) − ev(100 ms) = +0.2101 (stated +0.215), stride-1 control −0.7863 (stated −0.785). Tolerance ±0.005 on AUC, ±0.01 bps on capture.
- **What would resolve it:** Restate the register cell as "AUC 0.501 **at 900 s**, decaying from 0.664 at 100 ms" — which is what the report already says and what the ledger supports. Nothing about the closure changes: the economics fail at every horizon in both cost modes.
- **Confidence:** HIGH — the ledger and the report's own decay line both contradict "at every horizon".
- **Invalidated by later commits?:** no — the ledger row and report line are tracked at the anchor.
- **Disclosed by authors?:** The true per-horizon AUCs are published in the same repository (report.md:920, 1046, 2255); only the register's summary cell overstates the signal-absence. This is an internal inconsistency between register and report, not a hidden figure.

### DRAFT-V-4
- **Repository / SHA:** MLCryptoEngine / `5359a11fc753cdcd2606aea991dae826293d0307`
- **Hypothesis or artifact:** H6 / D.1d §5 caveats — the no-crossing counterfactual
- **Direction:** neutral
- **Class:** STALE_FIGURE
- **Severity:** S4
- **Label:** DERIVED
- **Claim challenged (verbatim quote):** "**deleting every crossing fill still leaves both instruments negative** (−3.98 / −2.57)." — MLCryptoEngine/report.md:5002-5003
- **Evidence:**
  - The same document withdraws exactly these numbers 66 lines earlier: "The figures originally given here (PUMP **−3.98**, MERL **−2.57**, MERL improved **−3.43**) were obtained by subtracting the crossing rows from the totals. That is invalid twice over … Re-run properly … the answer is **PUMP −4.35, MERL −2.13**" — MLCryptoEngine/report.md:4925-4932.
  - The corrected figures are in a tracked artifact: `variants.PUMP.no_crossing.net_bps` = **−4.351918**, `variants.MERL.no_crossing.net_bps` = **−2.134605**, fills 24,394 and 3,370 — MLCryptoEngine/audit/variants_base.json (28,658,883 records, trade_shift_ms 0.0).
  - The conclusion the caveat draws ("still negative") holds under both sets, and PUMP is *more* negative under the corrected run, so nothing in the verdict moves.
- **Recomputation (if any):** Inputs as above. Method: read `no_crossing` nets and fills; check the subtraction the correction rejects (32,018 − 8,685 = 23,333; 4,270 − 977 = 3,293). Result: both the corrected nets and the "more fills than subtraction implies" claim reproduce exactly. Tolerance ±0.005 bps.
- **What would resolve it:** Update the figure at report.md:5003 to −4.35 / −2.13, or mark the bullet as pre-correction text the way the surrounding blocks are marked.
- **Confidence:** HIGH — both passages are in one file and the artifact settles which is current.
- **Invalidated by later commits?:** no.
- **Disclosed by authors?:** Partly — report.md:4804-4808 states the D.1d section is "left exactly as published" apart from the inline correction blocks, so the retained text is deliberate. But the bullet at :5002-5003 sits inside the *verdict and caveats* section and carries no superseded marker, so a reader of the verdict alone gets the withdrawn numbers.

### DRAFT-V-5
- **Repository / SHA:** MLCryptoEngine / `5359a11fc753cdcd2606aea991dae826293d0307`
- **Hypothesis or artifact:** D2 / Stage C.26 — the "measured-unaffordable" price of the decon-unbiased test
- **Direction:** neutral
- **Class:** ARITHMETIC
- **Severity:** S4
- **Label:** DERIVED
- **Claim challenged (verbatim quote):** "the pool-path decontaminated test costs **≈ 124,764 weighted** … That is **~1.9× the entire 60,000 cap** and would require raising the cap to **≈ 180,000, three times its current ceiling** … Against the **1,199 remaining** it is ~28× over." — MLCryptoEngine/report.md:3924-3928
- **Evidence:**
  - 124,764 / 60,000 = **2.079×**, not ~1.9×.
  - 124,764 / 1,199 = **104.06×**, not ~28×.
  - The two ratios cannot both be right for any cost figure: 60,000 / 1,199 = 50.0, so a cost that is 1.9× the cap is necessarily ~95× the remainder.
  - The third statement in the same sentence does check out: 58,801 already spent + 124,764 = 183,565 ≈ 180,000 ≈ 3 × 60,000.
  - The 1,199 remaining is confirmed against the ledger: the last row of `data/vendor/helius_credit_ledger.jsonl` (LIVE, 24,025 rows, read 2026-09-12T22:44Z) has `cumulative` = **58,801**; 60,000 − 58,801 = 1,199.
  - The register states the ratio correctly — "~125k weighted (~2× the cap)" — MLCryptoEngine/HYPOTHESES.md:252 and :257.
- **Recomputation (if any):** Inputs 124,764 (report.md:3925), 60,000 and 1,199 (report.md:3926-3928), `cumulative` 58,801 (helius_credit_ledger.jsonl last row). Method: division. Results 2.079× and 104.06×. Tolerance ±0.1×.
- **What would resolve it:** Correct the two ratios (or state which denominators they use). The decision is unaffected: the registered end condition is "cannot be afforded within a defensible cap (the > 65,000 case)" (report.md:3886-3888) and 124,764 clears that threshold under every reading.
- **Confidence:** HIGH — arithmetic on figures stated in the same sentence, with the credit ledger confirming the denominator.
- **Invalidated by later commits?:** no — report.md is tracked at the anchor; the ledger is unanchored but its last row long predates the anchor (2026-08-07).
- **Disclosed by authors?:** no.

### DRAFT-V-6
- **Repository / SHA:** MLCryptoEngine / `5359a11fc753cdcd2606aea991dae826293d0307`
- **Hypothesis or artifact:** "What this project built" capability list — free-archive provenance
- **Direction:** neutral
- **Class:** STALE_FIGURE
- **Severity:** S4
- **Label:** DERIVED
- **Claim challenged (verbatim quote):** "**Free-archive acquisition with per-file provenance** — 4,970 files, each with source, URL, sha256 and retrieval date." — MLCryptoEngine/HYPOTHESES.md:486-487
- **Evidence:**
  - `data/vendor/archive/manifest.jsonl` (LIVE, UNANCHORED, read 2026-09-12T22:49Z) holds **14,191 rows** over **13,543 unique paths**; `find data/vendor/archive -type f` returns **13,543 files** excluding the manifest — an exact 1:1 reconciliation.
  - By source: binance_spot_klines 4,067 · hyperliquid_info 9,876 · binance_futures_archive 229 · coinmetrics_community 2 · defillama_stablecoins 1 · solrpds_github 5 · rugcheck_api 5 · dexscreener_api 1 · goplus_api 2 · arxiv_abstracts 2 · helius_api 1. No grouping sums to 4,970 (non-Hyperliquid = 4,315; binance total = 4,296).
  - The claim was written in commit `fd18ba2` (2026-08-04 13:03:13 −0700 = 2026-08-04T20:03:13Z, "docs: add HYPOTHESES.md, a register of what has been tested and closed") and the string has never been edited since (`git log -S '4,970 files' -- HYPOTHESES.md` returns that one commit).
  - **The figure was exactly right when written:** filtering the manifest to `retrieved_at ≤ 2026-08-04T20:03:13` gives **exactly 4,970 rows** (4,892 unique paths). The manifest then grew to 13,497 unique paths on 2026-08-05 and 13,543 by 2026-08-07, and the register was never refreshed.
  - The provenance half of the claim verifies outright: **0 of 14,191 rows** are missing `source`, `url`, `sha256` or `retrieved_at`.
- **Recomputation (if any):** Inputs: manifest rows and the on-disk tree. Method: count rows, unique `path`, per-source counts, missing-field counts, and the cumulative unique-path curve by `retrieved_at` day. Results: 14,191 / 13,543 / 0 missing; cumulative unique paths 4,892 (08-04) → 13,497 (08-05) → 13,541 (08-06) → 13,543 (08-07); rows on/before fd18ba2 = 4,970. Tolerance: exact.
- **What would resolve it:** Update the register to the manifest's current count, or scope the figure ("4,970 as of 2026-08-04"). The figure understates the capability, so the correction strengthens rather than weakens the claim.
- **Confidence:** MEDIUM-HIGH — the manifest is unanchored (working-tree read 2026-09-12), but its last `retrieved_at` is 2026-08-07, 15 days before the anchor, so it is very unlikely to have changed between the anchor and the read; the git evidence for when the claim was written is anchored.
- **Invalidated by later commits?:** no — HYPOTHESES.md:486 is unchanged at the anchor and the manifest stopped growing on 2026-08-07.
- **Disclosed by authors?:** no.

### DRAFT-V-7
- **Repository / SHA:** MLCryptoEngine / `5359a11fc753cdcd2606aea991dae826293d0307`
- **Hypothesis or artifact:** `audit/census_ci.json` — the tracked evidence artifact for audit finding A3
- **Direction:** neutral
- **Class:** STATISTICAL
- **Severity:** S4
- **Label:** DERIVED
- **Claim challenged (verbatim quote):** "`iid_se = (st["net_mean_bps"] - st["ci95_lower_bps"]) / 1.6449 if n > 2 else float("nan")`" — MLCryptoEngine/audit/census_ci.py:99, whose output field backs "Newey–West inflates the standard error 1.3–3.6×; day-clustering (7 clusters) 2.2–28×" — MLCryptoEngine/report.md:5143-5144
- **Evidence:**
  - The script back-derives the IID standard error by dividing the published half-width by **1.6449** (a one-sided z). But the published half-width was scored **two-sided at 1.96** — the script's own diagnostic proves it: `halfwidth·√n/sd` = 1.9600 for all ten (report.md:5142, reproduced by me as 1.959966–1.960687).
  - Consequently the stored `iid_se` field is **1.191562× the true IID SE** (= 1.96/1.6449), identically for all ten instruments, and the derived `nw_over_iid` field is 16% low.
  - Using the artifact's own `iid_se`, the inflation ratios are NW **1.101–3.015** and day-cluster **1.878–23.547** — which do **not** support the quoted "1.3–3.6×" and "2.2–28×".
  - Using the correct IID SE (`sd_of_nets/√n`, both stored in the same artifact) the ratios are NW **1.312–3.593** and day-cluster **2.238–28.058** — which match the report exactly.
  - The same file's `p_one_sided_iid` is computed from the *correct* SE (`registered.py`:187 uses `se = sqrt(var/n)`), so one artifact carries two different "IID standard errors" under one name.
- **Recomputation (if any):** Inputs: `sd_of_nets`, `n`, `reported_halfwidth_bps`, `iid_se`, `newey_west_se`, `day_cluster_se` for all ten instruments, MLCryptoEngine/audit/census_ci.json. Method: compute `sd/√n`, compare with the stored `iid_se`, and form both sets of inflation ratios. Result: constant 1.191562 discrepancy; ranges as above. Tolerance ±0.002 on the ratio.
- **What would resolve it:** Divide by 1.96 at census_ci.py:99 (or take `se_iid_bps` straight from `_horizon_stats`, which already computes it correctly), and regenerate. The report's published ranges are the correct ones and do not change.
- **Confidence:** HIGH — the divisor is a literal in an anchored file and the discrepancy is an exact constant across all ten instruments.
- **Invalidated by later commits?:** no — both files are tracked at the anchor.
- **Disclosed by authors?:** no. The report's ratios happen to be right; it is the tracked artifact cited as their evidence whose derived field does not reproduce them.

### DRAFT-V-8
- **Repository / SHA:** MLCryptoEngine / `5359a11fc753cdcd2606aea991dae826293d0307`
- **Hypothesis or artifact:** D.1d Task 5 — the shipped PerformanceReport files
- **Direction:** neutral
- **Class:** STALE_FIGURE
- **Severity:** S4
- **Label:** DERIVED
- **Claim challenged (verbatim quote):** "`d1d_PUMP_base.json` (32,018 leg records), `d1d_MERL_base.json` (4,270), `d1d_MERL_improved.json` (14,085) … slippage expected-vs-realized (+2.74 vs −1.01 on PUMP)" — MLCryptoEngine/report.md:4957-4961
- **Evidence:**
  - The shipped files hold the corrected engine's values: `d1d_PUMP_base.json` **31,875** trade records, `expectancy_bps_net` −4.8086852205937705, slippage expected **+2.7553** vs realized **−1.2271**; `d1d_MERL_base.json` **2,536** records, −4.345949946241689; `d1d_MERL_improved.json` 14,085 records, −6.3503192401302595 — LIVE `data/processed/reports/` (UNANCHORED, read 2026-09-12T22:36Z, mtime 2026-08-12 21:35).
  - These match `logs/d1d_summary.json` `variants.*.base` exactly; the quoted 32,018 / 4,270 and +2.74 / −1.01 are the `as_published` variant's values.
  - The correction block immediately below does tell the reader the files changed: "The regenerated reports carry the corrected engine's values" (report.md:4965-4967) — but it names only the −5 ms shift reading (+0.45), not the corrected engine's −1.23, and the record counts in the un-struck sentence were not updated.
- **Recomputation (if any):** Inputs: the three PerformanceReport JSONs. Method: `len(trades)` and `expectancy_bps_net` per file, cross-checked against `logs/d1d_summary.json`. Result: 31,875 / 2,536 / 14,085 and −4.8087 / −4.3459 / −6.3503, i.e. `base`, not `as_published`. Tolerance: exact on counts.
- **What would resolve it:** Update the three record counts and the slippage pair to the regenerated files' values, or state explicitly that the sentence describes the pre-correction artifacts.
- **Confidence:** MEDIUM — the shipped files are unanchored working-tree artifacts (mtime 2026-08-12, ten days before the anchor), so I am comparing an anchored document to an unanchored file; their agreement with the anchored audit variants' `base`-engine lineage makes the reading secure.
- **Invalidated by later commits?:** no — no commit after 2026-08-12 touches these paths (they are gitignored), and the anchor's report text is unchanged.
- **Disclosed by authors?:** Partly — the correction block says the reports were regenerated with corrected values; the specific counts were not refreshed.

---

## 6. What could not be checked and why

1. **MLCE-C16 — the D.1a bounded result (+2.15 / +5.42 and their CIs).** No D.1a summary exists in `logs/`, in `data/processed/`, or anywhere in the snapshot (directory listing taken 2026-09-12T22:39Z: `logs/` holds only `d1c_summary.json`, `d1d_summary.json`, `d1d_summary_published_2026-08-12.json`, `validation_summary.json`, `telemetry_latest.json` and five text logs). Reproducing it requires re-running the census machinery over the 14 GB raw capture, which the rules forbid in place and which I did not attempt in the work dir. **Missing: a stored D.1a output.** The arithmetic *around* the figure (the A11 per-leg/per-round-trip halving, and −4.81 × 2 = −9.62) does verify.
2. **The corrected `registered.py` census output.** The A3/A6/A8-corrected run has no stored output at all. The GMX/PUMP/MERL day-clustered bounds in DRAFT-V-1 therefore had to be checked against `audit/census_ci.json` and against the code, not against the run that produced the quoted numbers. **Missing: the emitted `ci95_lower_bps_day_clustered` / `se_day_clustered_bps` / `day_clusters` for the ten instruments.**
3. **The C.27 known-answer gate's measured values (BTC −3.051, ETH −2.753).** The targets (−3.05 / −2.75) are hard-coded at `registered.py`:70 and the gate path does exercise the census accumulators, but no stored gate output exists. Note also that no A1-style line-coverage trace has ever been applied to *this* gate, only to D.1d's. **Missing: a stored `known_answer()` result.**
4. **The D.1a and D.1c interval estimators' re-derivation under clustering.** The D.1c 300 s / 900 s intervals reproduce exactly as published (IID), but recomputing a day-clustered version of them would require the per-print rows, which are not stored — `d1c_summary.json` carries only `n`, `net_mean_bps`, `ci95_lower_bps`, `mean_adverse_bps` and the two half-means per horizon. So I can say the A3 correction was not carried to them; I cannot say by how much they would widen. Directionally, A3 measured 2.2–28× at 1/5/60 s on the *same* rows, and the 300/900 s windows overlap 5–15× more, so the understatement there is at least as large.
5. **H9 / H11 deflated Sharpes as *recomputations*.** `experiments.jsonl` stores the DSR outputs but not the per-bar Sharpe, skew, kurtosis or observation count that feed them (unlike C.10, where all five primitives are stored and the DSR reproduced to 5 decimals). So 0.446 / 0.223 / 0.499 are verified as *agreeing between ledger and report*, not as re-executed statistics. **Missing: the DSR inputs per cell.**
6. **Per-pair cointegration p-values (BTC/ETH 0.1169 and 0.9275, ARB/GMX 0.0136).** The ledger stores the aggregate hit counts and the FDR method, not per-pair p-values. The aggregates all reproduce. **Missing: the per-pair test output.**
7. **The D2 mid-stratum lift itself (+0.032 / +0.051) and its SE.** `behavior_c25.csv` has the right shape (422 rows, 166 `c25_deep`, 328 honest) but neither the activity-stratum cut-points nor the per-pool v0 scores are stored, so the lift cannot be recomputed — only its interval arithmetic, which is exact.
8. **The 25 blind picks.** The registered rule (`blind_universe.py`, seed 20260812, per-band `Random(f"{seed}:{band}").sample(...)`) is deterministic *given the retrieved ranking*, and the ranking of 177 live perps at retrieval is not stored anywhere I could find. The band counts, caps, pick counts, seed and the ordering of the registration commit against the subscription restart all verify; the identity of the 25 names does not.
9. **The 2026-08-03 three-venue validation as a machine artifact.** `logs/validation_summary.json` holds a single run block, `generated_at` 2026-08-05T08:54:58Z. The 2026-08-03 figures exist only as the transcript in `report.md`:1255-1339. They are internally consistent and the register summarises them correctly; there is no second source.
10. **A1's trace result (106 lines executing zero times).** Re-tracing requires executing the repository's code against the raw capture. Not attempted. The replacement gate (`tests/test_fill_replay_gate.py`) was read and is substantive.
11. **The blind window itself (earliest close 2026-09-09).** It postdates the anchor entirely. For the record, and strictly as an unanchored observation: `data/raw/venue=hyperliquid/sessions.jsonl` shows the session that opened the window (start 2026-08-12T04:50:36.894Z) **ending at 2026-08-13T05:02:49.032Z**, and the last hyperliquid date partition is `date=2026-08-13`. No anchored evidence bears on the readout.
12. **`logs/telemetry_latest.json` is mode 0600.** It is latency telemetry, not a credential; I read only the per-venue percentile fields and `generated_at`. `.env` was never opened.
13. **The "~85%" decay (MLCE-C12b) and the "~1.9× / ~28×" ratios (DRAFT-V-5)** could not be reconciled to any stated denominator; for the first I could not determine the intended referent, so it is recorded UNVERIFIABLE rather than contradicted.

**Where the thesis-free expectation was disappointed in the other direction** — i.e. things a verifier braces for and did not find here: no threshold was edited after registration (380 registered lines survive verbatim); no result predates its registration; the audit's own evidence artifacts are tracked and reproduce; the two most damaging findings against the project's own headline (A1 and A13) were raised, accepted and actioned by the authors themselves; the D.1d closure reproduces from three independent places (summary JSON, shipped PerformanceReports, and the tracked audit replays) and survives every perturbation tested.

---

## 7. Live-repo access log

Every access was read-only. No `checkout`, `stash`, `reset`, `clean`, `add`, `commit`, `branch`, `merge`, `rebase`, `worktree` or `gc` was run against the audited repository; no file in it was opened for writing; no repository script was executed, in place or elsewhere; `.env` was never opened. All scratch scripts and outputs were written to `/home/kiros-li/.cache/program-audit/scratchpad/work/agentC-MLCryptoEngine/`.

| time (UTC) | action | result |
|---|---|---|
| 2026-09-12T22:32:09Z | `git -C <live> status --porcelain` (PRE-ACCESS) + `rev-parse HEAD` | EMPTY. HEAD = `5359a11fc753cdcd2606aea991dae826293d0307` = the anchored SHA |
| 2026-09-12T22:34:27Z | `ls -la logs/*.json`; read `logs/d1d_summary.json` (structure + all variant fields) | 5 JSON files listed; 14/15 variants per instrument read |
| 2026-09-12T22:35Z | read `logs/d1d_summary_published_2026-08-12.json` (all variants) | published nets, grids, fills recorded |
| 2026-09-12T22:36Z | read `data/processed/reports/d1d_{PUMP,MERL}_base.json`, `d1d_MERL_improved.json` (top-level fields, `len(trades)`) | corrected-engine values confirmed |
| 2026-09-12T22:40Z | read `logs/d1c_summary.json` (horizons, inventory, tick_geometry) | all D.1c figures recorded |
| 2026-09-12T22:41Z | `grep` for the session marker in `logs/recorder.log` (not found) and in `data/raw/venue=*/sessions.jsonl` (found, hyperliquid); read all three `sessions.jsonl` (6/11/11 rows) and `data/raw/venue=hyperliquid/gaps.jsonl` (31 rows) | marker = `start` event at 2026-08-12T04:50:36.894Z; gap ledger read in full |
| 2026-09-12T22:42Z | `ls`/`du` of `data/raw/venue=hyperliquid/date=2026-08-0{3,4,5}/hour=*` | per-hour byte sizes; the 2026-08-04 step at hour 06 |
| 2026-09-12T22:43Z | read `data/processed/detection/hard_rug_scorer.meta.json`; `csv.DictReader` over `features_c23.csv`, `behavior_c24.csv`, `behavior_c25.csv`, `labels_v0.csv` (counts only) | 281 / 231 / 422 / 116,308 rows; fold counts confirmed |
| 2026-09-12T22:44Z | `wc -l`, `head`, `tail` on `data/vendor/helius_credit_ledger.jsonl` | 24,025 rows; final `cumulative` 58,801 |
| 2026-09-12T22:45Z | `git -C <live> log -1` / `show --stat` / `show <sha>:progress.md` / `log --numstat` on 9 named commits and on `progress.md`'s whole history; `git log -S '4,970 files'` | read-only history only; registration blocks extracted to the work dir |
| 2026-09-12T22:47Z–22:49Z | streaming read (`zstdcat`) of `data/raw/venue=hyperliquid/date=2026-08-0[1-6]/hour=*/messages.ndjson.zst` — 126 files, 862 MB compressed, 15,814,362 lines — counting `tid`, `coin`, zero-`hash` and any `liquidat` string | 0 `liquidat` hits; 12 coins; 2,673,301 fills over the first 116 hour files. Files opened for reading only; nothing written into the repo |
| 2026-09-12T22:49Z | read `data/vendor/archive/manifest.jsonl` (14,191 rows); `find data/vendor/archive -type f` | 13,543 unique paths = 13,543 files on disk |
| 2026-09-12T22:51:16Z | `git -C <live> status --porcelain` + `rev-parse HEAD` (POST-ACCESS) | EMPTY; HEAD unchanged |

**Pre-access `git -C /home/kiros-li/Documents/GitHub/MLCryptoEngine status --porcelain` (2026-09-12T22:32:09Z), verbatim:**

```
(no output — working tree clean)
```

**Post-access `git -C /home/kiros-li/Documents/GitHub/MLCryptoEngine status --porcelain` (2026-09-12T22:51:16Z), verbatim:**

```
(no output — working tree clean)
```

`git rev-parse HEAD` = `5359a11fc753cdcd2606aea991dae826293d0307` before and after, identical to the anchored SHA. No pre-existing dirt was present and none was introduced.
