# MLCryptoEngine — verification inventory (Agent C, LOCATE)

**Repository:** MLCryptoEngine · **Anchored SHA:** `5359a11fc753cdcd2606aea991dae826293d0307` (main, 2026-08-22)
**Snapshot read:** `/home/kiros-li/.cache/program-audit/scratchpad/snap/MLCryptoEngine/` · **Live repo (read-only):** `/home/kiros-li/Documents/GitHub/MLCryptoEngine/`
**Agent:** C — referee and verifier. No thesis. **Task:** LOCATE only; nothing below is a finding, a verdict, or a challenge. Where an artifact and a document already agree on a read, that is recorded as plainly as where they do not.
**Generated:** 2026-09-12T18:10Z · **Live read window:** 2026-09-12T18:00:50Z – 18:16:13Z

At the moment of this inventory the live working tree is **clean** and `HEAD` equals the anchored SHA, so tracked content in the live repo and in the snapshot are the same bytes. Everything under `data/` and `logs/` is gitignored and therefore **unanchored**: it is the working state of 2026-09-12 and may have changed since 2026-08-22.

Orientation, because this repository is unusual: there is **no `REGISTRATION.md`, no `registrations/`, no `FINDINGS.md` and no `reports/*.md`**. Registrations live in `progress.md` (2,977 lines) and in the pre-registration sections of `report.md` (5,190 lines); the verdict register is `HYPOTHESES.md` (572 lines); decisions are `DECISIONS.md` (2,701 lines, 66 ADRs); and the repository carries its own **adversarial audit** as `AUDIT.md` (647 lines, 13 findings against commit `ed786ce`), with the audit's evidence artifacts committed under `audit/`. A large share of what an outside verifier would want to check, this project has already checked against itself and published — including two findings it accepted as showing that a headline claim was *not earned*.

---

## 1. Artifacts

**40 artifact groups: 21 tracked (anchored), 19 untracked (unanchored).**

The decisive split in this repository: **the audit's own evidence is tracked; the results it audits are not.** `audit/census_ci.json` and `audit/variants_{base,m5,p5}.json` are in git at the anchor and can be checked byte-for-byte. The D.1d run summaries that carry the closure's deciding number (`logs/d1d_summary.json`) and the shipped `PerformanceReport` files live only in the gitignored working tree.

### 1a. Tracked (anchored at 5359a11)

**`MLCryptoEngine/audit/census_ci.json`** — *measured artifact (JSON)*
- Holds: Per-instrument C.27 census interval re-derivation for all ten scored thin perps (ARB DOT GMX HYPE LINK MERL NOT PUMP SOL TNSR): worst_horizon_ms, n, net_mean_bps, reported_ci95_lower_bps, reported_halfwidth_bps, iid_se, sd_of_nets, overlap_lag_trades, trades_per_sec, newey_west_se, nw_over_iid, nw_ci95_lower_bps, block_bootstrap_ci90_lower_bps, day_cluster_se, day_cluster_ci95_lower_bps, n_days=7, day_means_bps, p_one_sided_iid
- Backs: report.md:4047-4057 C.27 census table (net and CI95 lower per instrument); report.md:5140-5155 audit finding A3 correction; HYPOTHESES.md:198 'intervals ... 2-17x too narrow', 'halfwidth*sqrt(n)/sd = 1.9600', 'GMX ... +0.288 IID -> -0.070 day-clustered'; AUDIT.md A3
- Note: Directly recomputable. Its day_cluster_ci95_lower_bps uses 1.96 (PUMP 3.7391, MERL 2.6981, GMX +0.0281); report.md's quoted -0.070/+3.59/+1.73 reproduce only under a TWO-SIDED student-t(6) bound (verified by recomputation from day_cluster_se: PUMP 3.5935, MERL 1.7250, GMX -0.0695).

**`MLCryptoEngine/audit/census_ci.py`** — *analysis code (153 lines)*
- Holds: The script that produced census_ci.json: IID, Newey-West, day-cluster and block-bootstrap intervals over per-print census rows
- Backs: A3 finding; the census CI correction

**`MLCryptoEngine/audit/variants_base.json`** — *measured artifact (JSON)*
- Holds: D.1d replay variant set at trade_shift_ms=0.0 over records=28,658,883, with funding, elapsed_s and per-variant nets for PUMP/MERL
- Backs: report.md:4885-4900 A13 correction ('net is robust to feed interleaving'); AUDIT.md A13; HYPOTHESES.md:196 mechanism withdrawal

**`MLCryptoEngine/audit/variants_m5.json`** — *measured artifact (JSON)*
- Holds: Same replay at trade_shift_ms = -5.0 (28,658,883 records)
- Backs: The A13 sign-flip claim: 'PUMP's realized edge from -1.01 to +0.45 ... inventory moves -2.24 -> -4.08' (report.md:4890-4896; HYPOTHESES.md:196)
- Note: The single decisive artifact for the withdrawn-mechanism claim.

**`MLCryptoEngine/audit/variants_p5.json`** — *measured artifact (JSON)*
- Holds: Same replay at trade_shift_ms = +5.0 (28,658,883 records)
- Backs: A13 'negative under every ordering tested, with the published figure the least negative of the three' (AUDIT.md:E verdict; report.md:4897-4900)

**`MLCryptoEngine/audit/replay_variants.py`** — *analysis code (178 lines)*
- Holds: Subclasses BoundedQuoteSim to re-run the D.1d replay under feed-shift and rule variants
- Backs: A13; AUDIT.md 'the single check that would settle it fastest'

**`MLCryptoEngine/audit/probe_fill_replay.py`** — *analysis code (297 lines)*
- Holds: 10/2 pass/fail probe suite over fill_replay (probes 1a-2a encode an expectation the author states was wrong)
- Backs: AUDIT.md A1, A4, A5, and section B verified negatives

**`MLCryptoEngine/audit/probe2.py`** — *analysis code (156 lines)*
- Holds: 18/8 pass/fail second probe suite, corrects probe_fill_replay's sweep expectation
- Backs: AUDIT.md A4 (sweep credits min(print, order), not the full order)

**`MLCryptoEngine/research/experiments.jsonl`** — *stored ledger (JSONL, 19 runs, 192,499 bytes)*
- Holds: Append-only experiment log: run_id, logged_at, git_sha, dates, sampling, feature_count, horizons_ms, tb_config, cost_summary, signing_methods, leakage_tests and a full results block per run. Runs 0-3 Phase B / C.8 (AUC, calibration, capture per horizon); 4-8 C.10 pairs (pairs_traded, executable, deflation); 9-12 C.11 carry; 13-14 C.13 cross-sectional; 15-16 C.14 diagnostics/deep; 17 C.16 momentum (git_sha 88b69d8d); 18 C.17 medium-horizon (git_sha 370ba414)
- Backs: H1 (AUC 0.596, 3.31 bps, EV -76.69), H2 (AUC 0.501, 0.22 bps), H4 (0 of 180, DSR 0.026), H5, H8, H9 (DSR 0.446, alpha t 1.01), H11 (0 of 40, DSR 0.499, alpha t 1.35); the h1 note's whole per-horizon table
- Note: The only anchored artifact for the eight unaudited Phase-B / archive closures. Each row carries the git_sha it ran at, so run 17's sha 88b69d8d and run 18's 370ba414 are directly checkable against the pre-registration commits those stages name.

**`MLCryptoEngine/research/microstructure/registered.py`** — *analysis code (426 lines)*
- Holds: The C.27 registered census: per-horizon stats, BH q=0.10, capacity tier, category assignment. Post-audit it emits ci95_lower_bps (one-sided t, A6), ci95_lower_bps_as_scored (two-sided 1.96, as published), ci95_lower_bps_day_clustered, se_day_clustered_bps, day_clusters
- Backs: Every C.27 figure; the A3/A6/A8 corrections at report.md:5140-5170
- Note: Uses scipy student_t.ppf(CONFIDENCE, clusters-1) for the day-clustered bound (line 189), confirming the t(6) convention.

**`MLCryptoEngine/research/microstructure/fill_replay.py`** — *analysis code (496 lines)*
- Holds: BoundedQuoteSim: the D.1d order-lifecycle replay (placement/cancel latency, ALO rejection, always-last queue, sweep/through/crossing fill rules, inventory cap, MTM ledger)
- Backs: Every D.1d number, published and corrected
- Note: The code path A1 says the known-answer gate never executed.

**`MLCryptoEngine/research/microstructure/d1d.py`** — *analysis code (344 lines)*
- Holds: D.1d stage driver: variant construction (known_answer, base, as_published, a4_only, a4_only_cancels, a5_only, cap_5x, cap_10x, latency grid, MERL improved), summary emission to logs/d1d_summary.json
- Backs: report.md sections D.1d 1-5 and D.1d corrections 1-8

**`MLCryptoEngine/research/microstructure/reference_replay.py`** — *analysis code (259 lines)*
- Holds: Second implementation of the registered D.1d policy with a per-order lifecycle and blotter-recomputed ledger, sharing no code with fill_replay
- Backs: report.md:5085-5105 (A1 replacement gate); ADR-063
- Note: The repo itself states both implementations are the same author's reading of the same policy.

**`MLCryptoEngine/research/microstructure/fees.py`** — *analysis code / sourced constant (42 lines)*
- Holds: HYPERLIQUID_MAKER_BPS = 1.5, TAKER 4.5, FEE_SCHEDULE_RECORDED = '2026-08-12', ROUND_TRIP derived as 2x MAKER
- Backs: Every C.27 / D.1c / D.1d net (the 3.0 bps round trip and the 1.5 bps/leg fee); A10
- Note: Docstring says 'Recorded here 2026-08-12 from the Hyperliquid published fee schedule'; config/venues.yaml:182-190 cites a third-party explainer (hiperwire.io) as the 2026-08-01 verification source. Two different provenances for the same number.

**`MLCryptoEngine/research/microstructure/{census,spread,adverse,horizons,tick,inventory,d1c,blind_universe}.py`** — *analysis code (144/142/110/150/137/202/287/135 lines)*
- Holds: Census scoring, spread state, adverse-selection queues, 300/900 s horizons, tick geometry, inventory sim, D.1c driver, D.1b blind-universe band rule
- Backs: C.9, C.27, D.1a, D.1c figures; the D.1b blind selection
- Note: report.md:5185-5190 discloses that spread.py and adverse.py 'still have no direct test of their own'.

**`MLCryptoEngine/research/{pairs,carry,cross,momentum,medium,deep,detection,models,validation,labels,sampling,features}/`** — *analysis code (~7,900 lines across 60 modules)*
- Holds: H4 cointegration+deflation, H5 funding carry, H8 cross-sectional carry, H9 momentum grid, H11 medium-horizon ridge walk-forward, C.14 deep models and leakage suite, D1/D2 detection scorer and behaviour, purged k-fold and walk-forward validation
- Backs: Every Phase B / archive / detection closure (H1, H2, H4, H5, H8-H11, D1, D2)
- Note: report.md:5183 states these closures 'remain unaudited ... their inputs were not present in the audit clone'.

**`MLCryptoEngine/config/venues.yaml`** — *config / fee source (437 lines)*
- Holds: Per-venue fee ladders with retrieval dates and URLs: Kraken base 25/40 bps (retrieved 2026-08-08), Coinbase base 40/60, Hyperliquid base 1.5/4.5 (verified 2026-08-01 via hiperwire.io explainer), CME $2.02/side per contract (explicitly NOT verified against cmegroup.com); venue kinds incl. 'retired' for kraken/coinbase
- Backs: H1's 80 bps, H3's cost column, the 3.0 bps Hyperliquid round trip, the CME cost-bps table in HYPOTHESES.md:454-462, ADR-055, ADR-060

**`MLCryptoEngine/backtest/reporting/performance_report.schema.json`** — *schema*
- Holds: JSON Schema for PerformanceReport (mode, venue, symbol, cost, equity_curve, drawdown, trades, expectancy_bps_net, hit_rate, slippage, latency)
- Backs: The D.1d Task 5 shipped artifact claim; desktop/src/lib/generated/performance-report.ts drift test

**`MLCryptoEngine/tests/ (55 files)`** — *test code*
- Holds: test_note_honesty.py pins the h1 note's figures to HYPOTHESES.md/report.md character-for-character; test_registered_census.py, test_fill_replay_gate.py (the A1 replacement differential gate + coverage assertion), test_d1c.py, test_d1d.py, test_leakage.py, test_blind_universe.py
- Backs: ADR-065 (note figures pinned by test); ADR-063 (gate encoded as a test)

**`MLCryptoEngine/docs/notes/h1-predictability-without-capturability.md`** — *document (313 lines)*
- Holds: Standalone H1/H2 write-up with a per-horizon AUC/capture/rho/top-decile table and a Sources table mapping every figure to a report.md section and a commit
- Backs: README.md:78 Findings link; H1 and H2 register entries
- Note: Its Sources table (lines 297-311) is itself a provenance artifact naming 12 commits.

**`MLCryptoEngine/tests/fixtures/{coinbase,hyperliquid,kraken}_messages.ndjson`** — *test fixture*
- Holds: Recorded venue message samples used by parser and book-builder tests
- Backs: Phase A validation code paths

### 1b. Untracked / unanchored (live working tree, read 2026-09-12)

**`/home/kiros-li/Documents/GitHub/MLCryptoEngine/logs/d1d_summary.json`** — *measured artifact (JSON), UNTRACKED*
- Holds: The corrected D.1d run: records 28,658,883, elapsed_s 166.2, zero_crossing_ms {PUMP: null, MERL: null}, funding {applied 163, skipped 5} per symbol, and 14-15 variants per instrument (known_answer, base, as_published, a4_only, a4_only_cancels, a5_only, cap_5x, cap_10x, lat_+50..+800ms, latency_grid, MERL improved), each with fills, filled_notional_usd, edge_bps, inventory_bps, funding_bps, fees_bps, net_bps
- Backs: report.md:5122-5130 corrected headline table (-4.81 / -4.35); report.md:5050-5052 A4 table; report.md:5075 a5_only 'none to every digit'; report.md:5031-5033 as_published reproduction table; HYPOTHESES.md:196
- Size: 43024 bytes · mtime 2026-08-12 21:35
- Read (UTC): 2026-09-12T18:03Z
- Note: UNANCHORED: read from the live working tree 2026-09-12; may have changed since the 2026-08-22 anchor. Read values: PUMP base net_bps -4.8086852205937705 (31,875 fills, $14,055,243 notional); MERL base -4.345949946241689 (2,536 fills, $1,105,002); MERL improved -6.3503192401302595 (14,085 fills); PUMP as_published -4.750295040717393 (32,018); MERL as_published -4.231438891792402 (4,270).

**`/home/kiros-li/Documents/GitHub/MLCryptoEngine/logs/d1d_summary_published_2026-08-12.json`** — *measured artifact (JSON), UNTRACKED*
- Holds: The pre-correction D.1d run: records 28,658,883, elapsed_s 140.0, 10-11 variants per instrument, no a4/a5/as_published entries
- Backs: report.md:4864 published net table (-4.75 / -4.23 / -6.35); report.md:4943-4944 published latency grid
- Size: 29678 bytes · mtime 2026-08-12 21:27
- Read (UTC): 2026-09-12T18:03Z
- Note: UNANCHORED. Its elapsed_s is 140.0 while report.md:4809 says the published pass took '130 s wall'; its mtime (21:27) is 8 minutes before the corrected run's (21:35), so this file may be a regeneration rather than the original 2026-08-12 output.

**`/home/kiros-li/Documents/GitHub/MLCryptoEngine/logs/d1c_summary.json`** — *measured artifact (JSON), UNTRACKED*
- Holds: D.1c: records 28,705,383; tick_geometry for 12 instruments (sz_decimals, quoted_hours, tick_bps_time_weighted_mean, median_spread_ticks, frac_le_1_tick...); horizons for the 10 census instruments (trades, trades_without_quote, per_horizon 60000/300000/900000); inventory; funding_sources
- Backs: report.md:4345-4500 (D.1c results): PUMP one tick 85.5% of the week, the 300/900 s CI table at report.md:4483-4485, inventory -33.07 vs +5.82, funding agreement on 28 overlap hours; HYPOTHESES.md:204
- Size: 22881 bytes · mtime 2026-08-11 19:52
- Read (UTC): 2026-09-12T18:04Z
- Note: UNANCHORED. Read values: per-instrument 'trades' reconcile the C.27 table exactly (PUMP 499,944, MERL 25,378, GMX 25,868, HYPE 1,150,528...) with trades_without_quote = 30 each, which is why audit/census_ci.json's scored n runs 30-54 lower.

**`/home/kiros-li/Documents/GitHub/MLCryptoEngine/data/processed/reports/d1d_PUMP_base.json`** — *shipped artifact (PerformanceReport JSON), UNTRACKED*
- Holds: run_id d1d-PUMP-base-2026-08-12, mode backtest, venue hyperliquid, 164 equity/drawdown points, 31,875 trade records, expectancy_bps_net -4.8086852205937705, slippage expected +2.7553 vs realized -1.2271, latency p50/p95/p99 = 162.0 ms, cost fee_bps_per_leg 1.5
- Backs: report.md:4957-4966 D.1d Task 5 'the project's first PerformanceReport files'; the A13 correction note that 'the regenerated reports carry the corrected engine's values'
- Size: 6211754 bytes · mtime 2026-08-12 21:35
- Read (UTC): 2026-09-12T18:05Z
- Note: UNANCHORED. Holds the CORRECTED values (31,875 records / -4.8087), while report.md:4959 describes this file as carrying 32,018 leg records.

**`/home/kiros-li/Documents/GitHub/MLCryptoEngine/data/processed/reports/d1d_MERL_base.json`** — *shipped artifact (PerformanceReport JSON), UNTRACKED*
- Holds: 2,536 trade records, expectancy_bps_net -4.345949946241689, slippage expected +2.7776 vs realized -2.7419
- Backs: report.md:4957-4966 (described there as 4,270 records)
- Size: 518234 bytes · mtime 2026-08-12 21:35
- Read (UTC): 2026-09-12T18:05Z
- Note: UNANCHORED. Corrected values.

**`/home/kiros-li/Documents/GitHub/MLCryptoEngine/data/processed/reports/d1d_MERL_improved.json`** — *shipped artifact (PerformanceReport JSON), UNTRACKED*
- Holds: 14,085 trade records, expectancy_bps_net -6.3503192401302595, slippage expected +1.7498 vs realized -2.3857
- Backs: report.md:4864 MERL improved -6.35 and report.md:5124 corrected -6.35
- Size: 2750333 bytes · mtime 2026-08-12 21:35
- Read (UTC): 2026-09-12T18:05Z
- Note: UNANCHORED. Published and corrected values are BIT-IDENTICAL for this variant (-6.350319, 14,085 fills) in both summary files - the A4 own_level correction does not touch a first-in-queue price-improved quote.

**`/home/kiros-li/Documents/GitHub/MLCryptoEngine/logs/validation_summary.json`** — *measured artifact (JSON), UNTRACKED*
- Holds: generated_at 2026-08-05T08:54:58Z, one run block: venue, date, msgs_total, channel_counts, feed/downtime/unclean gap accounting, arrival, integrity, symbols, passed, failure_reasons
- Backs: HYPOTHESES.md:473-479 infrastructure PASS claims; report.md validation-run sections
- Size: 3687 bytes · mtime 2026-08-05 01:54
- Read (UTC): 2026-09-12T18:03Z
- Note: UNANCHORED. Holds only ONE run (latest), not the three-venue 2026-08-03 set the register cites; the per-venue PASS figures live in report.md's validation-run sections.

**`/home/kiros-li/Documents/GitHub/MLCryptoEngine/logs/telemetry_latest.json`** — *measured artifact (JSON), UNTRACKED*
- Holds: generated_at 2026-08-13T05:02:48Z; per-venue last_ms/p50/p95/p99/samples plus a rolling history array. Hyperliquid at read: p50 157.402 ms, p95 410.865, p99 772.308, samples 303
- Backs: The D.1b 162 ms proxy floor (report.md:4632) and D.1d's L = 162 ms each direction (report.md:4741); the 'measured distributions instead of guessed constants' claim in README.md:33
- Size: 60080 bytes · mtime 2026-08-12 22:02
- Read (UTC): 2026-09-12T18:05Z
- Note: UNANCHORED, mode 0600. Structure read only. The registered floor rests on n = 7 (report.md:4632); this file's 303 samples postdate it.

**`/home/kiros-li/Documents/GitHub/MLCryptoEngine/data/vendor/archive/manifest.jsonl`** — *stored ledger (JSONL), UNTRACKED*
- Holds: Per-file archive provenance: source, venue, dataset, symbol, interval, period, url, path, sha256, retrieved_at, size_bytes. At read: 14,191 rows / 13,543 unique paths; sources binance_spot_klines 4,067, hyperliquid_info 9,876, binance_futures_archive 229, coinmetrics_community 2, defillama_stablecoins 1, solrpds_github 5, rugcheck_api 5, dexscreener_api 1, goplus_api 2, arxiv_abstracts 2, helius_api 1
- Backs: HYPOTHESES.md:486 'Free-archive acquisition with per-file provenance - 4,970 files, each with source, URL, sha256 and retrieval date'; ADR-031, ADR-037
- mtime: 2026-08-06
- Read (UTC): 2026-09-12T18:06Z
- Note: UNANCHORED. 14,191 rows against a claimed 4,970 files; non-hyperliquid sources sum to 4,315. The claim is either scoped to a subset or stale relative to a manifest that grew.

**`/home/kiros-li/Documents/GitHub/MLCryptoEngine/data/vendor/spend_ledger.jsonl`** — *stored ledger (JSONL), UNTRACKED*
- Holds: 29 rows, append-only Databento spend: ts, dataset, symbol, schema, date, usd, billable_bytes, note (first two flagged 'backfilled: downloaded before the gate existed')
- Backs: HYPOTHESES.md:484 'Vendor purchasing with a cost gate and an append-only ledger, which caught a real error before it spent money'; the $0.7763 CME survey cost (HYPOTHESES.md:88); progress.md:678 '$3.2054 spent ungated'; ADR-046
- Size: 5575 bytes · mtime 2026-08-03 22:37
- Read (UTC): 2026-09-12T18:06Z
- Note: UNANCHORED.

**`/home/kiros-li/Documents/GitHub/MLCryptoEngine/data/vendor/helius_credit_ledger.jsonl`** — *stored ledger (JSONL), UNTRACKED*
- Holds: 24,025 rows: ts, kind, n, weighted, cumulative, note - the Helius credit meter for the detection track
- Backs: D2's '~125k weighted (~2x the cap)' unaffordability measurement (HYPOTHESES.md:253, 257); C.26 cost arithmetic; ADR-046/047
- Size: 2643735 bytes · mtime 2026-08-07 16:07
- Read (UTC): 2026-09-12T18:06Z
- Note: UNANCHORED.

**`/home/kiros-li/Documents/GitHub/MLCryptoEngine/data/processed/detection/{features_c23.csv,behavior_c24.csv,behavior_c25.csv,labels_v0.csv,hard_rug_scorer.txt,hard_rug_scorer.meta.json}`** — *measured artifacts (CSV + LightGBM model), UNTRACKED*
- Holds: features_c23.csv 282 lines (281 pools + header - matches 'reached to T0'); behavior_c24.csv 232 lines; behavior_c25.csv 423 lines; labels_v0.csv 116,309 lines (12.7 MB); hard_rug_scorer.txt 80,150 B LightGBM dump + meta
- Backs: D1 'precision 0.984 at recall 0.538 ... 281 reached to T0, 194 in the 2024 test fold' (HYPOTHESES.md:239, 241); D2 lifts +0.097/+0.047/+0.032 (HYPOTHESES.md:253); report.md C.23-C.26
- mtime: 2026-08-06/07
- Read (UTC): 2026-09-12T18:06Z
- Note: UNANCHORED. Only artifact set for the detection-track closures.

**`/home/kiros-li/Documents/GitHub/MLCryptoEngine/data/processed/pairs/universe_2021-08_2026-07.json`** — *measured artifact (JSON), UNTRACKED*
- Holds: summary + members: the point-in-time survivorship-free universe (291 symbols listed at 2021-08, top 60 by that month's volume)
- Backs: H4 and H9 universe claims: '291 symbols listed at 2021-08, top 60 ... 12 (20%) died inside the sample', '58 in matrix (LUNA splice + BTT excluded)' (HYPOTHESES.md:99, 149); ADR-029
- Size: 9183 bytes · mtime 2026-08-04 03:07
- Read (UTC): 2026-09-12T18:06Z
- Note: UNANCHORED.

**`/home/kiros-li/Documents/GitHub/MLCryptoEngine/data/raw/`** — *raw capture tree (zstd NDJSON), UNTRACKED*
- Holds: 14 GB: venue=kraken 6.8 G (16 date dirs, last 2026-08-11), venue=coinbase 5.1 G (16 dirs, last 2026-08-11), venue=hyperliquid 2.2 G (15 dirs, last 2026-08-12)
- Backs: Every D.1c/D.1d/C.27 figure (the 28.7M-record replay reads this); the Phase A validation PASS rows
- mtime: 2026-08-11/12
- Read (UTC): 2026-09-12T18:02Z
- Note: UNANCHORED; ls -la only, no binary opened. Kraken/coinbase stop at 2026-08-11, consistent with the D.1b retirement (ADR-060).

**`/home/kiros-li/Documents/GitHub/MLCryptoEngine/data/processed/{book_snapshots,latency,research_samples,trades}/`** — *derived parquet trees, UNTRACKED*
- Holds: 9.3 GB total; venue=/symbol=/date= partitions for cme, coinbase, hyperliquid, kraken; latency venue trees 356K/356K/40K
- Backs: Phase B research runs, C.8 CME study, C.9/C.27 census inputs, the telemetry percentiles fed to D.1d
- mtime: 2026-08-05..2026-08-11
- Read (UTC): 2026-09-12T18:02Z
- Note: UNANCHORED; ls -la and du only.

**`/home/kiros-li/Documents/GitHub/MLCryptoEngine/data/vendor/databento/`** — *purchased vendor data, UNTRACKED*
- Holds: Part of the 7.8 GB data/vendor tree; rolls/MBT_c_0.jsonl and CME mbp-10 month files
- Backs: H2's '224,425,675 events over 989 scheduled-open hours; two validated MBT months (2026-04, 2026-05)' (HYPOTHESES.md:67)
- mtime: 2026-08-02
- Read (UTC): 2026-09-12T18:02Z
- Note: UNANCHORED; ls only.

**`/home/kiros-li/Documents/GitHub/MLCryptoEngine/logs/{recorder.log,telemetry.log,record_run.out,telemetry_run.out,d1d_rerun.log}`** — *run logs, UNTRACKED*
- Holds: recorder.log 83.8 MB (to 2026-08-12 22:02), telemetry.log 14.2 MB, record_run.out 5.7 MB, telemetry_run.out 1.4 MB, d1d_rerun.log 539 B
- Backs: The 5.75 h 2026-08-04 recorder hole; session-lifecycle and gap accounting; the D.1d correction re-run
- mtime: 2026-08-12 22:02
- Read (UTC): 2026-09-12T18:02Z
- Note: UNANCHORED; ls -la only, not opened.

**`(absent) corrected-census output`** — *MISSING artifact*
- Holds: No stored output of the A3/A6/A8-corrected research/microstructure/registered.py run exists anywhere in the snapshot, logs/ or data/processed/
- Backs: report.md:5148-5151 '+3.59 and +1.73 ... GMX ... -0.070'; HYPOTHESES.md:198 'GMX ... +0.288 IID -> -0.070 day-clustered'
- Read (UTC): 2026-09-12T18:06Z
- Note: These three figures have no artifact. They ARE reproducible from audit/census_ci.json's day_cluster_se under a two-sided t(6) bound (recomputed: PUMP 3.5935, MERL 1.7250, GMX -0.0695), but nothing in the repository stores them.

**`/home/kiros-li/Documents/GitHub/MLCryptoEngine/data/raw/venue={kraken,coinbase,hyperliquid}/{gaps.jsonl,sessions.jsonl}`** — *stored ledgers (JSONL), UNTRACKED*
- Holds: Per-venue feed-gap and recorder-session lifecycle ledgers. At read: kraken gaps 93 rows / sessions 11; coinbase gaps 88 / sessions 11; hyperliquid gaps 31 / sessions 6
- Backs: The C.27 coverage table (report.md:4016-4031: 2026-08-04 at 76.3% from a ~5.75 h logged recorder downtime; 2026-08-08 three short feed gaps; ~96.4% overall); D.1d's '5 skipped funding boundaries sit in the 08-04 recorder hole'; ADR-028 (order session markers by clock, never by position); A8 (capacity tier divided by 7 calendar days)
- mtime: kraken 2026-08-11 17:06 / 2026-08-11 21:50; coinbase 2026-08-11 13:18 / 21:50; hyperliquid 2026-08-12 19:31 / 22:02
- Read (UTC): 2026-09-12T18:08Z
- Note: UNANCHORED. These are the only artifacts that can settle the 5.75 h hole, the 96.4% coverage figure and the A8 recorded-span correction. Date partitions present: kraken and coinbase 2026-07-30 -> 2026-08-12 (14 days each); hyperliquid 2026-08-01 -> 2026-08-13 (13 days) - three-venue overlap 2026-08-01 -> 08-12 = 12 days, matching HYPOTHESES.md:504 'stopped accruing at 12 days'.

---

## 2. Numeric claims, ranked

**20 claims extracted; 8 marked MUST-VERIFY** (the brief requires at least three). Ranking is by how much rests on the number: the deciding figure of the project's terminal closure ranks first, then the chain that feeds it, then the individual register closures, then capability claims.

### 1. `MLCE-C01` — **MUST-VERIFY**

> **By the registered kill condition, verbatim: the tightened net at the declared cap and the latency floor is <= 0 for both instruments, so H6 closes and D.2 does not follow.** ... **PUMP -4.75 bps and MERL -4.23 bps** per filled notional ... Corrected headline: net at declared 2.5xQ cap, 162 ms floor (bps) | **-4.81** | **-4.35**

- **Where:** `MLCryptoEngine/report.md`:4968-4971 (verdict), 5120-5130 (corrected headline table); HYPOTHESES.md:196, 555-560
- **Figures:** PUMP -4.81 bps, MERL -4.35 bps per filled notional at the declared 2.5xQ inventory cap and the 162 ms latency floor (published -4.75 / -4.23)
- **n:** 28,658,883 replayed records over the 8-day window 2026-08-04 -> 08-12; PUMP 31,875 fills / $14.06M filled notional; MERL 2,536 fills / $1.11M
- **Believed produced by:** logs/d1d_summary.json variants.PUMP.base.net_bps = -4.8086852205937705 and variants.MERL.base.net_bps = -4.345949946241689 (UNTRACKED, read 2026-09-12T18:03Z); data/processed/reports/d1d_{PUMP,MERL}_base.json expectancy_bps_net identical; code research/microstructure/{fill_replay,d1d}.py
- **Why it ranks here:** This is the deciding number of the project's terminal closure. It closes H6, ends the only live next step on the strategy side, and is the number every 'no alpha hypothesis remains open' statement rests on.
- **Already disclosed by the authors:** report.md:4990-5006 and 5107-5112 disclose: one census week, one regime; PUMP a screened positive; latency a proxy floor; the replay ran once and no second pair of eyes has checked it; both reference implementations are the same author's reading of the same policy.

### 2. `MLCE-C02` — **MUST-VERIFY**

> | **GMX** | 25,868 | **+0.40** | +0.29 | yes | yes | **survivor @ capacity** | ... | **PUMP** | 499,944 | **+4.30** | +4.27 | ... | **MERL** | 25,378 | **+6.45** | +6.07 |

- **Where:** `MLCryptoEngine/report.md`:4047-4057; restated HYPOTHESES.md:198
- **Figures:** PUMP +4.30 (CI95 lower +4.27), MERL +6.45 (+6.07), GMX +0.40 (+0.29); failures HYPE -2.11, SOL -2.61, LINK -1.77, DOT -0.60; ARB +0.28 (+0.17); NOT +31.15 (+30.26), TNSR +35.50 (+34.91)
- **n:** Ten thin Hyperliquid perps over 2026-08-04 -> 08-11 at 96.4% coverage; trade counts 3,312 to 1,150,528
- **Believed produced by:** audit/census_ci.json (TRACKED): net_mean_bps PUMP 4.300377933683802 / MERL 6.4502060246160005 / GMX 0.40443149568754866; reported_ci95_lower_bps 4.267670482380068 / 6.069521221163282 / 0.2880788979073995. Scored n there is 499,912 / 25,348 / 25,838 against the report's trades column 499,944 / 25,378 / 25,868; logs/d1c_summary.json horizons[*].trades_without_quote = 30 reconciles most of the gap. Code research/microstructure/registered.py.
- **Why it ranks here:** The census positive is the project's only pre-registered-bar-clearing positive and the sole input to the D.1 chain; if it is wrong the whole D.1a/D.1c/D.1d arc has no subject.
- **Already disclosed by the authors:** report.md:4062-4085 states every net is an upper bound and discounts GMX to ~zero; report.md:4020-4031 reports the 5.75 h hole.

### 3. `MLCE-C03` — **MUST-VERIFY**

> **PUMP and MERL survive every correction** (day-clustered lower bounds +3.59 and +1.73; block-bootstrap +4.16 and +5.12). **GMX does not**: it moves from `ci95_lower = +0.288` (survivor) to **-0.070** day-clustered, block-bootstrap +0.101 - straddling zero.

- **Where:** `MLCryptoEngine/report.md`:5148-5153; restated HYPOTHESES.md:198
- **Figures:** Day-clustered 95% lower bounds PUMP +3.59, MERL +1.73, GMX -0.070; block-bootstrap +4.16 / +5.12 / +0.101; the diagnostic halfwidth*sqrt(n)/sd = 1.9600 for all ten; NW inflation 1.3-3.6x; day-clustering 2.2-28x
- **n:** 7 day clusters per instrument; n per instrument 3,282 to 1,150,493 prints
- **Believed produced by:** audit/census_ci.json (TRACKED): block_bootstrap_ci90_lower_bps PUMP 4.161522210384049 and MERL 5.1228180387761 and GMX 0.10088443048485143 MATCH the quoted +4.16 / +5.12 / +0.101 exactly. But its day_cluster_ci95_lower_bps are PUMP 3.7391 / MERL 2.6981 / GMX +0.0281 (normal 1.96). Recomputing from day_cluster_se with a TWO-SIDED student-t(6): PUMP 3.5935, MERL 1.7250, GMX -0.0695 - which is what the report quotes. No artifact stores the corrected registered.py output.
- **Why it ranks here:** This is the statistical correction that decides which census survivors are real. It also produces the only category change in the whole audit (GMX demoted to 'unresolved'), and GMX's demotion is quoted in the register.
- **Already disclosed by the authors:** report.md:5155-5162 (A6) states in the same section that the registered bar was ONE-sided and that the two-sided 1.96 used at scoring was ~19% harder than registered; under the one-sided convention the same artifact gives GMX a day-clustered lower bound of +0.028, i.e. still positive. The report does not reconcile A6 with the two-sided critical value used for its own A3 figures.

### 4. `MLCE-C04` — **MUST-VERIFY**

> Re-run properly (`_crossing_fills` disabled, all 8 days replayed) the answer is **PUMP -4.35, MERL -2.13**, with *more* fills than subtraction implies (24,394 vs 23,333; 3,370 vs 3,293) ... [but at report.md:5001-5003] **deleting every crossing fill still leaves both instruments negative** (-3.98 / -2.57).

- **Where:** `MLCryptoEngine/report.md`:4930-4936 (A2 correction) vs 5001-5003 (uncorrected caveat)
- **Figures:** Corrected counterfactual PUMP -4.35 / MERL -2.13 (fills 24,394 / 3,370); the superseded subtraction PUMP -3.98 / MERL -2.57 / MERL improved -3.43
- **n:** All 8 days of the replay window re-run with _crossing_fills disabled
- **Believed produced by:** No variant named 'no_crossing' exists in logs/d1d_summary.json (variants are known_answer, base, as_published, a4_only, a4_only_cancels, a5_only, cap_5x, cap_10x, lat_*, latency_grid, improved). Code: research/microstructure/fill_replay.py _crossing_fills; audit/replay_variants.py.
- **Why it ranks here:** This counterfactual is the stage's only defence that the closure does not rest on its most pessimistic fill rule; the audit's own verdict says the closure would need rebuilding if it did. The corrected figures appear in section 2b while the SAME numbers are still quoted in their superseded form in section 5's caveat list 70 lines later.
- **Already disclosed by the authors:** report.md:4804-4808 states the D.1d section is 'left exactly as published' apart from the inline correction blocks, so the -3.98/-2.57 at 5003 may be deliberate; it is nonetheless an uncorrected restatement inside a bullet that is not marked as superseded.

### 5. `MLCE-C05` — **MUST-VERIFY**

> Net is negative at **every** point including the floor itself, so the zero-crossing the stage was designed to report **does not exist - latency is not the binding constraint; fill selection is.**

- **Where:** `MLCryptoEngine/report.md`:4946-4950 (published grid at 4941-4944); corrected grid at 5125
- **Figures:** Published PUMP -4.75/-4.80/-4.83/-4.79/-4.69/-4.63 and MERL -4.23/-6.30/-7.04/-6.93/-6.40/-5.83 at +0/+50/+100/+200/+400/+800 ms; corrected PUMP -4.81/-4.92/-4.95/-4.88/-4.75/-4.66, MERL -4.35/-6.40/-6.67/-7.05/-6.35/-5.89
- **n:** 12 replays (6 latency points x 2 instruments) per engine version over 28,658,883 records
- **Believed produced by:** logs/d1d_summary.json variants.{PUMP,MERL}.latency_grid and zero_crossing_ms = {PUMP: null, MERL: null}; every grid value read from the file matches the report table to the printed digit (UNTRACKED, read 2026-09-12T18:04Z).
- **Why it ranks here:** This is what makes the 2026-08-19 latency re-run a for-the-record follow-up rather than a reopening path, i.e. it is the reason the closure is stated as final.
- **Already disclosed by the authors:** report.md:5006-5008 states latency is a proxy floor; the grid only ADDS latency above the floor and never tests below it.

### 6. `MLCE-C06` — **MUST-VERIFY**

> **3.31 bps** gross capture at the 900 s horizon against **80.00 bps** round-trip maker cost. Coinbase BTC-USD. AUC **0.596** - the signal is real and the arithmetic still fails, by 23x. Net EV **-76.69 bps**. **Superseded by C.14 (2026-08-05): that 3.31 bps came from a single day. Across four full days the same measurement ranges -2.44 to +3.05 bps**

- **Where:** `MLCryptoEngine/HYPOTHESES.md`:50
- **Figures:** 3.31 bps vs 80.00 bps, AUC 0.596, net EV -76.69 bps, 23x; C.14 range -2.44 to +3.05 bps over four full days
- **n:** Single day (2026-07-31) for the headline; six validated days 2026-07-30 -> 2026-08-04 for C.14 (165,075 Kraken / 41,780 Coinbase samples)
- **Believed produced by:** research/experiments.jsonl (TRACKED) run 1 (2026-08-02T01:05Z, git_sha e8aeac94) results['coinbase BTC-USD'] horizons; report.md:769-888 Phase B research run 2026-08-02; docs/notes/h1-*.md:297-303 pins the figures to commits 03c99f9 and ddf525d
- **Why it ranks here:** H1 is the project's headline closure and the only result written up for outside readers; 80 bps is the cost bar that all of H1's arithmetic and its reopening condition rest on.
- **Already disclosed by the authors:** HYPOTHESES.md:50 itself marks the deciding number superseded and states the four-day range straddles zero; HYPOTHESES.md:52 calls the six-day reproduction 'pipeline validation, not evidence of a durable edge'.

### 7. `MLCE-C07` — **MUST-VERIFY**

> **AUC 0.501** at every horizon, and **0.22 bps** gross capture against **5.33 bps** cost. CME MBT (micro bitcoin) via Databento. Best net EV **-5.11 bps**, and EV never crosses zero at any horizon in either cost mode. ... 224,425,675 events over 989 scheduled-open hours

- **Where:** `MLCryptoEngine/HYPOTHESES.md`:63, 67
- **Figures:** AUC 0.501; 0.22 bps capture; 5.33 bps cost; best net EV -5.11 bps; the +0.215 bps at 900 s reversing to -0.785 on a stride-1 control
- **n:** 224,425,675 events over 989 scheduled-open hours; two validated MBT months (2026-04, 2026-05), mbp-10
- **Believed produced by:** research/experiments.jsonl runs 2 and 3 (2026-08-03, git_sha a958c0d6, results['cme MBT'], 53 dates then a 10-date stride-1 control); report.md:959-1089 Stage C.8; the CME cost figure traces to config/venues.yaml:255-266, which states it was NOT verified directly against cmegroup.com
- **Why it ranks here:** H2 is the project's cleanest 'signal-absent' closure and the case that removes 'cost is the constraint' as a general explanation; the 5.33 bps figure also anchors the contrast used throughout the register.
- **Already disclosed by the authors:** HYPOTHESES.md:65 'two months of one contract ... a single instrument on a single venue'; venues.yaml declares the CME fee unverified against the exchange.

### 8. `MLCE-C08` — **MUST-VERIFY**

> **0 of 180** formation-window pairs surviving Benjamini-Hochberg remain significant out of sample. The holdout window produced **91 raw hits against 77.0 expected by chance** - fewer than noise. **BTC/ETH, the literature's headline pair, scores p = 0.1169** ... Deflated Sharpe of the best surviving pair: **0.026**, its per-bar Sharpe of 0.0514 being *less than half* the 0.1058 that screening 1,653 noise pairs would be expected to produce.

- **Where:** `MLCryptoEngine/HYPOTHESES.md`:98
- **Figures:** 0 of 180; 91 raw vs 77.0 expected; p = 0.1169 (BTC/ETH, formation) and p = 0.9275 (holdout); DSR 0.026; per-bar Sharpe 0.0514 vs expected-max 0.1058; annualised Sharpe 0.98; skew 3.78 / kurtosis 79.50; 1,095 observations
- **n:** 1,826 daily bars 2021-08-01 -> 2026-07-31; 1,653 pairs tested (formation), 1,540 (holdout), 36 (persistence); 60-member point-in-time universe, 12 died in-sample
- **Believed produced by:** research/experiments.jsonl runs 4-8 (2026-08-04, git_sha f7fb08f8, results.deflation); report.md:1386-1636 Stage C.10 (tables at 1455-1470, 1555-1600); data/processed/pairs/universe_2021-08_2026-07.json (UNTRACKED); code research/pairs/{cointegration,screening,validation,backtest}.py
- **Why it ranks here:** H4 is the load-bearing counterexample to the cost explanation ('break-even 300-550 bps against a 3 bps venue') and is cited in the cross-cutting findings as the cleanest demonstration in the project.
- **Already disclosed by the authors:** HYPOTHESES.md:101 'daily bars from a venue this project cannot trade'; report.md:1597-1604 states the deflated Sharpe rests on two of twelve folds.

### 9. `MLCE-C09`

> Primary spec (L90/H30) net-of-3bps Sharpe **0.302 vs BTC buy-and-hold 0.183** - beats the benchmark, but **deflated Sharpe 0.446** against 12 registered trials, **alpha t = 1.01**, and **7/12** specs positive. ... On the **27 executable symbols** the primary collapses to **Sharpe 0.013**.

- **Where:** `MLCryptoEngine/HYPOTHESES.md`:147
- **Figures:** Sharpe 0.302 vs 0.183; DSR 0.446 (0.223 executable); alpha t 1.01; 7/12 specs positive; executable Sharpe 0.013; best cell L30/H7 net Sharpe 0.647 deflating to 0.732; break-even 66-265 bps/side
- **n:** 58-symbol matrix, 2021-08 -> 2026-07 daily bars, 12 registered grid cells, 27 executable symbols
- **Believed produced by:** research/experiments.jsonl run 17 (2026-08-06T13:04Z, git_sha 88b69d8d - the pre-registration commit itself), results.verdict/consistency/primary/btc; report.md:2499-2630 Stage C.16 (grid table at 2537-2556, verdict at 2607-2620); code research/momentum/{engine,__main__}.py
- **Why it ranks here:** H9 is one of two closures decided purely by deflation, and its DSR 0.446 is cited in the external-corroboration section as the project's deflation discipline.
- **Already disclosed by the authors:** HYPOTHESES.md:149-150 discloses the net-short exposure and negative beta in every cell.

### 10. `MLCE-C10`

> **0 of 40 registered cells pass.** Best deflated Sharpe in the grid **0.499** vs the 0.95 bar; best alpha t **1.35** vs 2. ... Costs decided nothing: break-even 22-1,059 bps/side vs 1.5.

- **Where:** `MLCryptoEngine/HYPOTHESES.md`:181
- **Figures:** 0/40 cells; best DSR 0.499 vs 0.95; best alpha t 1.35 vs 2; class consistency A 0/8, B 7/8, C 6/8, D 8/8, E 7/8; publication lags A +1d, B +75d, C 0d, D 0d; Class D on 45-59 weeks where BTC's own Sharpe was 1.16-2.06
- **n:** Weekly 2020-08-02 -> 2026-07-26 (~310 weeks), BTC+ETH, ridge lambda=1 walk-forward, 40 registered cells
- **Believed produced by:** research/experiments.jsonl run 18 (2026-08-06T18:23Z, git_sha 370ba414 - the C.17 pre-registration commit), results.verdict/grid/lags_applied_days; report.md:2704-2863 Stage C.17 (grid table at 2754-2795, verdict at 2798-2799); code research/medium/{study,features,data}.py
- **Why it ranks here:** C.17's FAIL is the registered condition that ENDED the alpha search by decision. Everything the project says about being concluded rests on this stage failing all six bars on all forty cells.
- **Already disclosed by the authors:** HYPOTHESES.md:183-184 discloses Class D's 45-59 week window and that the netflow class is tested as freely available at 75 days stale.

### 11. `MLCE-C11`

> Funding income **+43.68%/yr on deployed capital**, price return **-42.91%**, cost -0.66% - **net +0.11%** against a 4% risk-free rate, a shortfall of 3.89 points. Max drawdown **-75.85%**. The price term's daily volatility is **10.9x the funding term's** (1.81% vs 0.166%).

- **Where:** `MLCryptoEngine/HYPOTHESES.md`:131
- **Figures:** +43.68% / -42.91% / -0.66% = +0.11%; shortfall 3.89 points; max DD -75.85%; vol ratio 10.9x; dispersion fell 77% (241.50% -> 53.45%); basket correlation -0.718; break-even 1.76 bps/side vs 1.5 modelled at 51.7x turnover
- **n:** 232 perps considered / 231 usable / 55 delisted and retained; 4,411,046 hourly funding observations; 1,182 days 2023-05-12 -> 2026-08-05
- **Believed produced by:** research/experiments.jsonl runs 13-14 (2026-08-05, git_sha fd18ba2b / a2146424, results.dispersion_gate/result/residual_price_risk/benchmark); report.md:2010-2250 Stage C.13; code research/cross/{portfolio,dispersion,universe,acquire}.py
- **Why it ranks here:** H8's arithmetic decides a closure whose three terms nearly cancel; +0.11% against a 4% bar is the smallest margin in the register and is sensitive to every input.
- **Already disclosed by the authors:** HYPOTHESES.md:133 'contains no bear market'; delisted perps assumed to liquidate at last printed price.

### 12. `MLCE-C12`

> Historically real: **8.07% (ETH) and 8.00% (BTC)** net annualised **on deployed capital** after every modelled cost, with 5 of 10 instruments clearing a 4% risk-free rate by 1.6-4.1 points. But **the yield has decayed ~85%**: Binance BTC funding annualised **30.61% in 2021 -> 11.92% in 2024 -> 5.13% in 2025 -> 1.94% in 2026**

- **Where:** `MLCryptoEngine/HYPOTHESES.md`:114
- **Figures:** 8.07% / 8.00%; 5 of 10 clearing 4% by 1.6-4.1 points; decay 30.61 -> 11.92 -> 5.13 -> 1.94 (BTC) and 37.54 -> 0.97 (ETH); MERL -22.38%/yr, TNSR -32.41%/yr; BTC pays 5.77 bps/day in uptrends vs 1.87 in downtrends; funding-trend correlation 0.5+
- **n:** Hyperliquid hourly funding 2023-05-12 -> 2026-08-04 (3.23 years, 27,761 rows for BTC), 12 perps; Binance 8-hourly 2020-01 -> 2026-07
- **Believed produced by:** research/experiments.jsonl runs 9-12 (2026-08-04, git_sha 4b521d84); report.md:1637-1865 Stage C.11; code research/carry/{funding,trade,risk}.py; data/vendor/archive/manifest.jsonl rows with source binance_futures_archive / hyperliquid_info
- **Why it ranks here:** H5 is the only entry closed as 'decayed, not disproved', so its reopening threshold (funding > ~10% sustained a quarter) is a live condition rather than a settled one.
- **Already disclosed by the authors:** HYPOTHESES.md:116 'contains no full bear market'; perp prices reconstructed as spot x (1 + premium).

### 13. `MLCE-C13`

> **Firming (C.26): +90 more pools moved the mid-stratum estimate DOWN to +0.032 (SE 0.039, 95% CI [-0.045, +0.109]) - the added data weakened rather than confirmed; C.25's +0.051 was optimistic.**

- **Where:** `MLCryptoEngine/HYPOTHESES.md`:253; report.md:3940-3960
- **Figures:** Mid-stratum lift +0.032, SE 0.039, 95% CI [-0.045, +0.109] at n=103 (C.25: +0.051 at n=84); C.24 precision 0.654 at recall 0.53 vs 0.557 base (lift +0.097); C.25 v0 lift +0.047; high-activity lift collapsing +0.156 -> +0.015; C.23 decon honest precision 0.574 vs 0.500 base; ~125k weighted credits, ~2x the cap; 0/8 pools resolved a creator
- **n:** 281 decon-labelled pools + 120 (then 166) random honest pools via Method B; mid stratum n=84 then n=103
- **Believed produced by:** data/processed/detection/{features_c23.csv (282 lines), behavior_c24.csv (232), behavior_c25.csv (423), labels_v0.csv (116,309)} - ALL UNTRACKED; data/vendor/helius_credit_ledger.jsonl (24,025 rows) for the cost measurement; code research/detection/behavior.py
- **Why it ranks here:** D2 is the only entry the project labels a positive that it then walks down across three stages; the CI including zero is the reason it is 'concluded' rather than 'shipped'.
- **Already disclosed by the authors:** HYPOTHESES.md:255 states the surviving lift is marginal, measured on v0 not decon, and that the CI includes zero at n=84.

### 14. `MLCE-C14`

> **Honest-clearance precision 0.984 at recall 0.538** on the 2024 test fold (train <= 2023), from 30-minute launch-window features. The complementary hard-rug *alarm* is weak - a high P(hard_rug) is only **0.464** precision

- **Where:** `MLCryptoEngine/HYPOTHESES.md`:239
- **Figures:** Precision 0.984 at recall 0.538; alarm precision 0.464
- **n:** 281 pools reached T0; 194 in the 2024 test fold
- **Believed produced by:** data/processed/detection/hard_rug_scorer.txt + .meta.json and features_c23.csv (UNTRACKED); code research/detection/{scorer,train_scorer}.py; report.md:3547-3682 Stage C.24
- **Why it ranks here:** D1 is the project's only SHIPPED artifact - the one claim of a working deliverable rather than a closure.
- **Already disclosed by the authors:** HYPOTHESES.md:241 'detects hard rugs only ... in the wild ~99% of launches are scam-adjacent, so it filters a small honest minority'.

### 15. `MLCE-C15`

> 2026-08-03 validates **PASS on all three venues**: Kraken 16.7M messages with 16.5M CRC32 checksums and zero failures, Coinbase 3.5M messages with zero sequence gaps, Hyperliquid 1.5M with 32,200 snapshots - 100.00% coverage outside gaps, zero crossed or locked books.

- **Where:** `MLCryptoEngine/HYPOTHESES.md`:474-479
- **Figures:** Kraken 16.7M msgs / 16.5M CRC32 / 0 failures; Coinbase 3.5M / 0 gaps; Hyperliquid 1.5M / 32,200 snapshots; 100.00% coverage outside gaps
- **n:** One UTC day (2026-08-03) across three venues
- **Believed produced by:** report.md validation-run sections (e.g. 1866-2009 for 2026-08-05 runs); logs/validation_summary.json holds only the LAST run (generated_at 2026-08-05T08:54:58Z), not the 2026-08-03 three-venue set; data/raw/ (14 GB, UNTRACKED)
- **Why it ranks here:** The infrastructure claim is what the project says survives regardless of strategy outcomes - 'the durable output'.
- **Already disclosed by the authors:** None needed; the register states the figures with their date.

### 16. `MLCE-C16`

> the **always-last-in-queue** pessimistic net stays positive on both - **PUMP +2.15 (CI +2.00), MERL +5.42 (CI +4.88)** - a *measured* quantity ... D.1 builds a *bounded* fill sim reporting the range **PUMP [+2.15, +4.30], MERL [+5.42, +6.45] bps** (both endpoints positive)

- **Where:** `MLCryptoEngine/HYPOTHESES.md`:203; report.md:4198-4213
- **Figures:** PUMP +2.15 (CI +2.00), MERL +5.42 (CI +4.88); ~4,640 and ~940 fills/day if last; consumption test median error 100%, 87-99% of levels clear by cancellation
- **n:** Sweeping trades within the census week; PUMP 499,944 / MERL 25,378 total aggressor trades
- **Believed produced by:** No D.1a summary file found in logs/ or data/processed/; code research/microstructure/{d1c,census,registered}.py; report.md:4150-4261
- **Why it ranks here:** The D.1a GO is what authorised building D.1d at all; it is also the number D.1d's -4.75 is a 'fall' from (report.md:4880), and A11 notes it is per ROUND TRIP where D.1d's is per leg.
- **Already disclosed by the authors:** report.md:4993-4999 discloses the unit mismatch and halves +2.15/+5.42 to +1.08/+2.71 for comparison; A11 at report.md:5175-5177 restates the bounded result as -9.62 per round trip.

### 17. `MLCE-C17`

> PUMP's inventory term is **-33.07 bps against +5.82 bps of edge** (-$303k on the week, position walking to $3.6M) - swamped; but **every registered cap restores ~+1.2 bps per leg** at ~300x the capacity floor, the 2.5xQ cap forgoing **74% of gross edge to avoid -$353k of inventory** (29.8% of the week spent one-sided).

- **Where:** `MLCryptoEngine/HYPOTHESES.md`:204; report.md:4425-4470
- **Figures:** -33.07 bps inventory vs +5.82 bps edge; -$303k; +1.2 bps per leg restored by the cap; 74% of gross edge forgone; -$353k avoided; 29.8% one-sided; MERL +6.7 to +12.5 bps; MERL's +3.98 uncapped inventory called path luck (price +16%)
- **n:** The single census week, $500 fixed quote size, 2.5x/5x/10x caps
- **Believed produced by:** logs/d1c_summary.json 'inventory' block (UNTRACKED, records 28,705,383); code research/microstructure/inventory.py, d1c.py
- **Why it ranks here:** The inventory cap is the declared policy parameter D.1d inherits; if the cap choice is fitted rather than declared the D.1d headline inherits that.
- **Already disclosed by the authors:** report.md:4727-4733 declares the cap 'declared, not fitted' and reports 5x/10x as sensitivity only; MERL's inventory sign is disclosed as path luck.

### 18. `MLCE-C18`

> **Free-archive acquisition with per-file provenance** - 4,970 files, each with source, URL, sha256 and retrieval date.

- **Where:** `MLCryptoEngine/HYPOTHESES.md`:486-488
- **Figures:** 4,970 files
- **n:** -
- **Believed produced by:** data/vendor/archive/manifest.jsonl (UNTRACKED, read 2026-09-12T18:06Z): 14,191 rows, 13,543 unique paths; by source binance_spot_klines 4,067 + binance_futures_archive 229 + coinmetrics 2 + defillama 1 + solrpds 5 + rugcheck 5 + dexscreener 1 + goplus 2 + arxiv 2 + helius 1 = 4,315, plus hyperliquid_info 9,876
- **Why it ranks here:** Low - a capability claim, not a closure. Included because the artifact and the figure visibly disagree and the artifact is unanchored.
- **Already disclosed by the authors:** None stated.

### 19. `MLCE-C19`

> **Zero identifiable liquidations** in 2,639,510 recorded fills (2026-08-01 -> 2026-08-06, 12 instruments). ... the one anomalous value (all-zeros hash, 18.0% of fills) ground-truths via `userFillsByTime` to **TWAP fills**

- **Where:** `MLCryptoEngine/HYPOTHESES.md`:164
- **Figures:** 0 identifiable liquidations in 2,639,510 fills; 18.0% all-zeros hash; three endpoint names returning HTTP 422; reopening floor >= 300 labeled liquidations
- **n:** 2,639,510 recorded fills over 6 days, 12 instruments, all four channels
- **Believed produced by:** data/raw/venue=hyperliquid (UNTRACKED, 2.2 GB); report.md:2631-2703 Stage C.15
- **Why it ranks here:** H10 is the register's 'third kind' of closure (data-availability). The count is a straightforward audit of recorded bytes.
- **Already disclosed by the authors:** HYPOTHESES.md:166 explicitly labels this a data-availability closure, not evidence of absence.

### 20. `MLCE-C20`

> **25 blind picks + PUMP and MERL carried over (marked not-blind) = 27 subscribed instruments** ... **earliest close 2026-09-09**, BH across the full blind set, PUMP/MERL as their own replication family, per the registration.

- **Where:** `MLCryptoEngine/report.md`:4641-4660
- **Figures:** Band memberships B0 4 / B1 7 / B2 36 / B3 107 / B4 23 of 177 live perps at >= $10k/day; caps 3/5/5/6/6; seed 20260812; session marker 1786510236894021684
- **n:** 177 live perps screened, 25 selected
- **Believed produced by:** research/microstructure/blind_universe.py (TRACKED, 135 lines, rule commit 4bde24c); data/raw/venue=hyperliquid post-2026-08-12 (UNTRACKED); tests/test_blind_universe.py
- **Why it ranks here:** The blind window is the only remaining unbiased selection test in the project; the anchor (2026-08-22) predates its 2026-09-09 readout, so nothing at the anchor can resolve it.
- **Already disclosed by the authors:** HYPOTHESES.md:196 states the window's role after the closure is a selection-bias check only.

---

## 3. Intervals and tests

### 3a. Confidence intervals

Every interval in this repository on per-print microstructure rows is an IID Welford interval on overlapping forward windows. The repository itself discloses this (audit finding A3) and quantifies the understatement at 2-17x. The A3 correction exists only for the C.27 census outputs; the D.1c 300/900 s intervals and the D.1a sweep-restricted intervals carry no clustering correction, and the report does not say whether they were re-derived.

**`MLCryptoEngine/report.md`:4047-4057** — *95% CI lower bound, ten instruments*

> | symbol | trades | worst-h net (bps) | CI95 lower | both halves | capacity | category | ... | **PUMP** | 499,944 | **+4.30** | +4.27 | ... | **MERL** | 25,378 | **+6.45** | +6.07 | ... | **GMX** | 25,868 | **+0.40** | +0.29 |

- Estimator: Welford mean +/- 1.96 * sd/sqrt(n) on per-print rows of (trade-time spread - adverse - 3.0 bps), judged at the worst of the 1/5/60 s horizons
- Value: lowers: HYPE -2.11, SOL -2.62, LINK -1.84, DOT -0.71, ARB +0.17, GMX +0.29, PUMP +4.27, MERL +6.07, NOT +30.26, TNSR +34.91
- n: 3,312 to 1,150,528 aggressor trades per instrument over 7 days
- Data structure: Per-aggressor-print rows; at the 5 s and 60 s horizons consecutive prints share overlapping forward windows, so rows are NOT independent
- Backing: audit/census_ci.json reported_ci95_lower_bps and reported_halfwidth_bps for all ten; iid_se; the diagnostic halfwidth*sqrt(n)/sd = 1.9600
- Note: The repository itself discloses at report.md:5140-5147 that these intervals assume independence and are 2-17x too narrow (A3).

**`MLCryptoEngine/report.md`:5148-5153** — *day-clustered 95% lower bound and block-bootstrap 90% lower bound*

> **PUMP and MERL survive every correction** (day-clustered lower bounds +3.59 and +1.73; block-bootstrap +4.16 and +5.12). **GMX does not**: it moves from `ci95_lower = +0.288` (survivor) to **-0.070** day-clustered, block-bootstrap +0.101

- Estimator: Cluster-robust SE over 7 day clusters with a student-t critical value on clusters-1 = 6 dof (research/microstructure/registered.py:179-190); moving-block bootstrap
- Value: day-clustered +3.59 / +1.73 / -0.070; block-bootstrap +4.16 / +5.12 / +0.101; Newey-West inflation 1.3-3.6x; day-clustering inflation 2.2-28x; PUMP's +/-0.03 bps becomes +/-0.07 (HAC) or +/-0.71 (day-clustered)
- n: 7 day clusters
- Data structure: Per-print rows grouped by UTC day; 7 clusters is a small-cluster regime
- Backing: audit/census_ci.json: block_bootstrap_ci90_lower_bps 4.1615 / 5.1228 / 0.10088 match exactly; day_cluster_ci95_lower_bps there are 3.7391 / 2.6981 / +0.0281 (normal 1.96). Recomputing from day_cluster_se with a TWO-SIDED t(6) gives 3.5935 / 1.7250 / -0.0695, matching the report.
- Note: The quoted day-clustered bounds are two-sided t(6). Under the ONE-sided convention that the same section's A6 correction says the bar actually required, the same SE gives GMX +0.028 - still positive. Whether GMX's demotion survives its own A6 correction is open.

**`MLCryptoEngine/report.md`:4483-4485** — *95% CI lower bounds at the 60 s / 300 s / 900 s adverse horizons, plus both-halves split*

> | PUMP | 499,914 | +4.56 (+4.49) | **+4.17 (+4.04)** | **+4.49 (+4.28)** | +1.72 / +2.11 / +1.79 | +4.88 / +4.15 | ... | MERL | 25,348 | +6.81 (+6.38) | **+6.06 (+5.45)** | **+6.08 (+5.21)** | -0.19 / +0.55 / +0.53 | +1.87 / +8.57 |

- Estimator: Welford mean and IID interval on the same per-print net rows, extended horizons
- Value: PUMP 60s +4.56 (+4.49), 300s +4.17 (+4.04), 900s +4.49 (+4.28); MERL 60s +6.81 (+6.38), 300s +6.06 (+5.45), 900s +6.08 (+5.21)
- n: PUMP 499,914; MERL 25,348 scored prints
- Data structure: Same overlapping-forward-window structure; the overlap is 5-15x longer at 300/900 s than at the horizons A3 was measured on
- Backing: logs/d1c_summary.json horizons[*].per_horizon keys 60000/300000/900000 (UNTRACKED, read 2026-09-12T18:04Z)
- Note: These CIs carry no clustering correction; A3's correction was applied to registered.py's C.27 outputs, and the report does not state whether the D.1c 300/900 s intervals were re-derived.

**`MLCryptoEngine/report.md`:4205-4206** — *95% CI lower bound on the sweep-restricted (always-last) net*

> | PUMP | +4.30 (CI +4.27) - reproduces C.27 | **+2.15 (CI +2.00 > 0)** | ~4,640 | | MERL | +6.45 (CI +6.07) - reproduces C.27 | **+5.42 (CI +4.88 > 0)** | ~940 |

- Estimator: Same IID Welford interval, restricted to prints whose size consumes the full visible touch
- Value: PUMP +2.15 (CI +2.00); MERL +5.42 (CI +4.88)
- n: Sweeping trades only; fills/day ~4,640 (PUMP) and ~940 (MERL)
- Data structure: A subset of the same overlapping per-print rows
- Backing: No stored D.1a artifact located; code research/microstructure/{census,registered}.py
- Note: Per round trip, not per leg (A11 at report.md:5175-5177); the registered GO bar was satisfied by this interval's sign.

**`MLCryptoEngine/report.md`:3948-3951 (restated HYPOTHESES.md:253)** — *95% confidence interval on a precision lift*

> **+0.032**, with SE ~ 0.039, a 95% interval of **[-0.045, +0.109] that still includes zero**, at recall 0.939

- Estimator: Normal interval on a difference of precisions (mid-activity stratum lift over base rate)
- Value: +0.032, SE 0.039, CI [-0.045, +0.109]
- n: n=103 mid-stratum pools (C.25 was +0.051 at n=84)
- Data structure: Pool-level cross-section, Method-B depth-independent random draw, stratified by activity
- Backing: data/processed/detection/behavior_c25.csv (423 lines, UNTRACKED); code research/detection/behavior.py
- Note: The register states the CI includes zero and calls the finding unconfirmed - disclosed, not hidden.

**`MLCryptoEngine/report.md`:4632** — *latency percentile from a very small sample*

> 162 ms / p95 208 ms** (n = 7), against kraken p50 176 / coinbase p50 115

- Estimator: p50 and p95 of measured round-trip probes
- Value: Hyperliquid p50 162 ms, p95 208 ms
- n: n = 7 probes
- Data structure: Sequential REST round-trip probes from one host
- Backing: logs/telemetry_latest.json (UNTRACKED; at read 2026-09-12 it shows hyperliquid p50 157.402 / p95 410.865 / p99 772.308 over 303 samples, generated_at 2026-08-13T05:02:48Z)
- Note: This n=7 p50 is the 162 ms floor that D.1d applies in BOTH directions to every fill (report.md:4741). The later 303-sample distribution has a p95 roughly 2x the n=7 value.

**`MLCryptoEngine/report.md`:1585-1598** — *deflated Sharpe ratio (probability the true Sharpe exceeds zero)*

> | annualised Sharpe | 0.98 | | per-bar Sharpe | 0.0514 | | **expected max per-bar Sharpe under the null, 1,653 trials** | **0.1058** | | skew / kurtosis | 3.78 / 79.50 | | observations | 1,095 | | **deflated Sharpe** | **0.026** |

- Estimator: Bailey & Lopez de Prado (2014) DSR correcting for 1,653 screened pairs, with skew and kurtosis adjustment
- Value: DSR 0.026; per-bar 0.0514 against an expected null max of 0.1058
- n: 1,095 observations, 1,653 trials
- Data structure: Daily bar returns of one selected pair; report.md:1578-1583 shows two of twelve folds carry essentially the whole return
- Backing: research/experiments.jsonl runs 4-8 results.deflation (TRACKED); code research/pairs/validation.py

**`MLCryptoEngine/report.md`:2603** — *deflated Sharpe, full universe vs executable subset*

> | deflated Sharpe | 0.446 | 0.223 |

- Estimator: DSR against 12 registered trials
- Value: 0.446 (58-symbol) and 0.223 (27 executable)
- n: 12 registered grid cells; ~1,800 daily bars
- Data structure: Daily long-short portfolio returns; the book is net short (-0.275 mean exposure)
- Backing: research/experiments.jsonl run 17 (git_sha 88b69d8d); report.md:2537-2556 grid table

**`MLCryptoEngine/report.md`:2754-2795** — *deflated Sharpe and alpha t across a 40-cell registered grid*

> | cell | weeks | net %/yr | net Sharpe | DSR | beta | alpha %/yr | alpha t | BTC Sharpe same window |

- Estimator: DSR against 40 trials; OLS alpha t against BTC
- Value: Best DSR 0.499 vs 0.95 bar; best alpha t 1.35 vs 2; Class D cells on 45-59 weeks where BTC's own Sharpe was 1.16-2.06
- n: 40 cells, weekly bars 2020-08-02 -> 2026-07-26 (Class D only 45-59 weeks)
- Data structure: Weekly ridge walk-forward with purge+embargo >= horizon
- Backing: research/experiments.jsonl run 18 (git_sha 370ba414) results.grid

### 3b. Test statistics and p-values

The project's own adversarial audit (AUDIT.md, 13 findings against commit ed786ce) is the largest single source of test statistics here. Its two structural findings - A1 (the known-answer gate executed none of the code it guarded) and A13 (the published mechanism flips sign under a 5 ms feed shift) - were both accepted and actioned by the authors, and the corresponding claims withdrawn in place. The census known-answer gate (report.md:4035-4040) has never had the A1-style trace check applied to it.

**`MLCryptoEngine/report.md`:1455-1470** — *Engle-Granger and Johansen trace cointegration tests with Benjamini-Hochberg FDR control*

> Johansen trace test. Benjamini-Hochberg at q=0.05. ... | raw hits at alpha=0.05 (Engle-Granger) | 432 | 91 | | **expected by chance at this universe size** | **82.7** | **77.0** | | **hits surviving Benjamini-Hochberg** | **180** | **0** |

- Value: Formation 432 raw hits vs 82.7 expected (5.2x), 180 surviving BH; holdout 91 vs 77.0 expected, 0 surviving; Johansen uncorrected 559 / 194; both tests 167 / 0
- n: 1,653 pairs (formation 2021-08 -> 2023-07), 1,540 pairs (holdout 2023-08 -> 2026-07), 1,826 daily bars
- Source: computed at C.10
- Data structure: Daily log-price series, survivorship-free point-in-time universe (60 members, 12 died in sample)
- Backing: research/experiments.jsonl runs 4-8; code research/pairs/{cointegration,screening}.py; data/processed/pairs/universe_2021-08_2026-07.json (UNTRACKED)

**`MLCryptoEngine/HYPOTHESES.md`:98 (report.md:1566)** — *Engle-Granger / Johansen p-values on named pairs*

> **BTC/ETH, the literature's headline pair, scores p = 0.1169** ... The single Johansen rejection, ARB/GMX (p=0.0136), **loses 8.4% a year gross**. BTC/ETH scores p=0.9275 in this window.

- Value: BTC/ETH p = 0.1169 (formation), p = 0.9275 (persistence window); ARB/GMX p = 0.0136
- n: 1,826 daily bars; persistence window 425 out-of-sample bars, 36 pairs, 1 raw hit against 1.8 expected
- Source: computed at C.10
- Data structure: Daily bars, Binance spot
- Backing: research/experiments.jsonl runs 4-8; report.md:1555-1570
- Note: p = 0.1169 appears in HYPOTHESES.md's opening paragraph (line 21) as the canonical example of a buried closing number.

**`MLCryptoEngine/report.md`:2607-2616** — *alpha t-statistic against a registered t >= 2 bar; consistency count*

> **FAIL against the registered bars**: primary beats BTC's Sharpe (0.302 vs 0.183) but fails deflation (0.446 < 0.95, and < 0.5 - the literal criterion), fails alpha significance (t = 1.01 < 2), and fails consistency (7/12 < 8/12).

- Value: alpha t = 1.01; no cell in the grid reaches t = 2; 7/12 specs positive against an 8/12 bar
- n: 12 registered specs; ~1,800 daily bars, 58 symbols
- Source: registered in commit 88b69d8, computed at C.16
- Data structure: Daily long-short returns regressed on BTC
- Backing: research/experiments.jsonl run 17 results.verdict/consistency

**`MLCryptoEngine/report.md`:2798-2799** — *alpha t and DSR against registered bars; per-class consistency*

> Class consistency (fraction of cells with positive net Sharpe): A **0/8**, B 7/8, C 6/8, D 8/8, E 7/8. **The best deflated Sharpe in the grid is 0.499 against a bar of 0.95; the best alpha t is 1.35 against a bar of 2.**

- Value: best alpha t 1.35 vs 2; best DSR 0.499 vs 0.95; A 0/8, B 7/8, C 6/8, D 8/8, E 7/8
- n: 40 registered cells; weekly 2020-08-02 -> 2026-07-26
- Source: registered in commit 370ba41 before any data, computed at C.17
- Data structure: Weekly ridge walk-forward, purge + embargo >= horizon, publication lags A +1d / B +75d / C 0d / D 0d
- Backing: research/experiments.jsonl run 18 (git_sha 370ba414) results.verdict/grid/lags_applied_days
- Note: This is the FAIL that triggered the pre-registered end condition for the whole alpha search.

**`MLCryptoEngine/report.md`:4043, 2880-2881** — *Benjamini-Hochberg FDR at q = 0.10 across ten instruments*

> with BH q=0.10 across the ten ... **Multiplicity:** Benjamini-Hochberg across the ten instruments at q = 0.10; expected false positives <= 0.1 x discoveries (<= 1 at the maximum), stated beside any survivor.

- Value: Five instruments clear BH + CI>0 + both-halves; expected false positives at q=0.10 is 0.5
- n: 10 instruments tested (out of a 177-perp screen)
- Source: registered in progress.md commit 6025f5c
- Data structure: One one-sided test per instrument on the worst-horizon net
- Backing: research/microstructure/registered.py bh_rejected; audit/census_ci.json p_one_sided_iid (PUMP and NOT and TNSR = 0.0, MERL 4.48e-237, GMX 4.88e-12, ARB 7.77e-08, DOT/HYPE/LINK/SOL = 1.0)
- Note: AUDIT.md A7 [STATIC, matches disclosure]: BH corrects the 10 tested, not the 177 screened. The p-values in census_ci.json are IID p-values on overlapping rows, so they are the quantity A3 says is 2-17x too tight.

**`MLCryptoEngine/report.md`:5155-5162** — *critical value for a one-sided registered bar*

> **A6 - a one-sided bar was judged with a two-sided critical value.** C.27 used `t(0.975)` = 1.96 where a one-sided 95% bound needs 1.645, making the bar ~19% *harder* than registered. Corrected; `ci95_lower_bps_as_scored` preserves the published figure. No instrument's category moves between the two

- Value: 1.96 used where 1.645 was registered; ~19% harder
- n: 10 instruments
- Source: registered one-sided at commit 6025f5c; scored two-sided
- Data structure: Per-print net rows
- Backing: research/microstructure/registered.py:169-190 (student_t.ppf(CONFIDENCE, n-1) one-sided, student_t.ppf(0.5 + CONFIDENCE/2, n-1) as_scored)
- Note: A6 loosens the bar while A3 tightens it; the report says 'against A3 this conservatism is swamped many times over' but the A3 day-clustered figures it quotes are themselves two-sided (see intervals entry 2).

**`MLCryptoEngine/report.md`:4809-4816, 5085-5105** — *known-answer gate, registered tolerance +/- 0.10 bps*

> The new engine, fills relaxed to D.1c's assumption, reproduces D.1c's capped results to the printed digit: **PUMP +1.23 bps, MERL +6.67 bps** ... (registered tolerance +/-0.10; measured delta ~ 0 - in fact exact to 15 significant figures). [Withdrawn 2026-08-12 (A1)] ... 106 lines, every line that distinguishes D.1d from D.1c - execute **zero times** under this gate, traced with `trace.Trace`

- Value: PUMP +1.23, MERL +6.67 reproduced to 15 significant figures; withdrawn - 106 lines executed zero times
- n: 286,378 PUMP fills / 22,077 MERL fills under the relaxed gate
- Source: registered in the D.1d pre-registration (report.md:4780-4789)
- Data structure: Same 28.7M-record event stream
- Backing: logs/d1d_summary.json variants.PUMP.known_answer.net_bps = 1.2328432875691382 and MERL 6.674559475354376 (UNTRACKED); tests/test_fill_replay_gate.py (the replacement differential gate); research/microstructure/reference_replay.py
- Note: Self-disclosed HIGH finding: the project's own audit rates A1 the most severe. The replacement gate caught one real defect on its first run (_refresh_queue shrinking queue-ahead of in-flight orders, seed 41).

**`MLCryptoEngine/report.md`:4885-4900** — *sensitivity test (perturbation of feed interleaving)*

> Shifting every `trades` timestamp by -5 ms, a perturbation 25-65x smaller than the feed's own 123-330 ms bbo cadence, moves PUMP's realized edge from **-1.01 to +0.45 - a sign flip** - while inventory moves -2.24 -> -4.08 to absorb it. That is forced: `MTM = edge + inventory` is the invariant

- Value: PUMP realized edge -1.01 -> +0.45 under a -5 ms shift; inventory -2.24 -> -4.08; net negative under all three orderings with the published figure the least negative
- n: Three full replays of 28,658,883 records each (trades -5 ms / 0 / +5 ms); crossing+through together are 80-92% of filled notional
- Source: run by the adversarial audit (A13)
- Data structure: Two independent WebSocket subscriptions (trades, bbo) ordered by local receive time
- Backing: audit/variants_m5.json, audit/variants_base.json, audit/variants_p5.json (all TRACKED, records 28,658,883 each); audit/replay_variants.py
- Note: Led to ADR-064 and the withdrawal of the published mechanism while the net closure was retained.

**`MLCryptoEngine/report.md`:5070-5082** — *isolation test of a real defect's effect (A5)*

> Effect on the scored numbers, isolated as the `a5_only` variant: **none, to every digit** - PUMP -4.750295, MERL -4.231439, identical placements (176,568 / 305,335), identical fills. ... Instrumenting a full day (2026-08-05) to count where rejections fire: **PUMP 216 on bbo, 0 on trade; MERL 82 on bbo, 0 on trade.**

- Value: Zero effect to every digit; rejection counts PUMP 216/0, MERL 82/0 on one day
- n: One instrumented day (2026-08-05) plus the full 8-day replay
- Source: computed in the D.1d corrections
- Data structure: ALO rejection events by triggering channel
- Backing: logs/d1d_summary.json variants.{PUMP,MERL}.a5_only net_bps = -4.750295040717393 / -4.231438891792402, bit-identical to as_published (UNTRACKED, read 2026-09-12T18:03Z)
- Note: Verified by direct read: a5_only and as_published agree to 15 digits and on fill counts.

**`MLCryptoEngine/report.md`:4880, 2854-2860 (canary)** — *planted-future leakage canary and prefix-invariance check*

> The leakage suite passed with a canary that demonstrably fires (AUC 0.9714 on a planted future column)

- Value: Canary AUC 0.9714; leakage suite PASS
- n: Phase B research runs and C.14/C.17
- Source: ADR-040 ('a leakage probe must be shown capable of firing')
- Data structure: A deliberately leaky future column injected into the feature matrix
- Backing: research/experiments.jsonl leakage_tests field per run; research/deep/leakage.py; tests/test_leakage.py
- Note: report.md:5185-5190 discloses the leakage suites reach NONE of the census / D.1c / D.1d modules.

**`MLCryptoEngine/report.md`:4035-4040** — *known-answer gate on the census machinery, registered tolerance 0.5 bps*

> the machinery reproduced C.9's closed BTC/ETH nets on C.9's own window and measure: **BTC net -3.051 bps** (target -3.05, delta -0.001), **ETH -2.753** (target -2.75, delta -0.003), both inside the 0.5 bps tolerance.

- Value: BTC -3.051 (delta -0.001), ETH -2.753 (delta -0.003)
- n: C.9's window (53.13 quoted hours of Hyperliquid BTC/ETH, 2,151,124 bbo updates)
- Source: registered at C.18 (commit 6025f5c), machinery in commit 287fc10
- Data structure: Per-print census rows on the earlier window
- Backing: research/microstructure/registered.py; tests/test_registered_census.py
- Note: Unlike A1's D.1d gate, this one does exercise the census code path; no equivalent audit of it is recorded.

---

## 4. Provenance claims

**16 provenance claims.** Fifteen named commit hashes appear across the documents; **all fifteen resolve in `main`** on the live read, with subjects that match what the citing text says they contain. That is a materially stronger starting position than a bare assertion, and it is recorded here as such. What resolution does *not* establish is the two things a verifier still has to open the objects for: that the registering commit's **tree** contained the bars (not merely that its message says so), and that no threshold was edited between registration and result.

| named commit | resolves to | subject |
|---|---|---|
| `370ba41` | 370ba414…4d4b, 2026-08-06 07:02:46 -0700 | docs: pre-register C.17 bars and the binding end condition before touching any data |
| `88b69d8` | 88b69d8d…d48f, 2026-08-05 22:09:05 -0700 | docs: pre-register C.16 momentum bars before computing any result |
| `6025f5c` | 6025f5c1…ce19, 2026-08-06 12:18:06 -0700 | docs: pre-register the H6 thin-perp census bars before the scored window closes |
| `a2d7466` | a2d7466a…3825, 2026-08-04 23:47:14 -0700 | docs: pre-register C.14 pass thresholds before computing any result |
| `5430eba` | 5430eba5…2702, 2026-08-05 00:17:26 -0700 | fix: verdict gates the filter branch on signed rho, matching the registered text |
| `4bde24c` | 4bde24c0…d6c5, 2026-08-11 21:43:22 -0700 | docs: pre-register the D.1b blind universe rule, seed committed before retrieval |
| `35e3466` | 35e34661…2b5e, 2026-08-06 12:47:47 -0700 | docs: register the C.19 rug-detection audit bars before probing any source |
| `902d2e6` | 902d2e6c…47d2, 2026-08-06 19:05:22 -0700 | docs: register detection baselines and the first-model bar before any model exists |
| `287fc10` | 287fc108…72a3, 2026-08-06 12:28:34 -0700 | feat: thin-perp census machinery, known-answer tested; scored population untouched |
| `ed786ce` | ed786ced…19ff, 2026-08-11 23:16:42 -0700 | feat: D.1d — the capture does not survive an order-lifecycle fill model; H6 closes |
| `fb296cb` | fb296cb7…1595, 2026-08-12 20:31:44 -0700 | docs: adversarial audit of the H6 closure chain — 13 findings, closure upheld |
| `ddf525d` | ddf525d3…fa29, 2026-08-05 03:46:17 -0700 | feat: C.14 diagnostics; both closures confirmed, H1's headline number withdrawn |
| `81e456e` | 81e456e0…61fc, 2026-08-07 17:33:42 -0700 | docs: C.27 (Tasks 2-4) — fold the external audit into the register, reconcile the Kraken fee |
| `34aebd5` | 34aebd56…5ea0, 2026-07-30 08:18:39 -0700 | feat: lossless market data recorder for kraken and coinbase public feeds |
| `ae4b734` | ae4b734d…68ff, 2026-08-01 00:32:59 -0700 | docs: record downtime gap decision, backfill, and 2026-08-01 revalidation |

**`MLCryptoEngine/HYPOTHESES.md`:5-6 (restated 541-545; report.md:2710-2717; DECISIONS.md:1903-1907 ADR-043)** — commit named: `370ba41`

> **The alpha search concluded by decision on 2026-08-06** (C.17, bars and end condition pre-registered in commit 370ba41 before any data).

- Resolves to: 370ba41420f73a8e400671d8e0c6eeafbf7f4d4b, 2026-08-06 07:02:46 -0700, 'docs: pre-register C.17 bars and the binding end condition before touching any data'
- What would have to be true: 370ba41's tree must contain the six C.17 bars and the end condition in progress.md/report.md; no C.17 result may exist in the tree at that commit; no later commit may have edited a threshold; and the C.17 computation must postdate it.
- Checkable now: Yes, entirely from git objects plus research/experiments.jsonl run 18, whose git_sha is 370ba414 - i.e. the run was logged AT the registration commit. That makes the registration and the result the same commit's code state, which should be examined: registration-before-data requires the bars to be in the tree before the run, not merely at the same sha.

**`MLCryptoEngine/HYPOTHESES.md`:150 (report.md:2512 'The bars, as registered (commit 88b69d8, before any result)')** — commit named: `88b69d8`

> | **Working** | `report.md` §"Stage C.16 — time-series momentum" (2026-08-06). ADR-041. Bars pre-registered in commit 88b69d8. |

- Resolves to: 88b69d8d6af6d01542456b639fb5d2e9a97ed48f, 2026-08-05 22:09:05 -0700, 'docs: pre-register C.16 momentum bars before computing any result'
- What would have to be true: The twelve-cell grid and the four bars must be present in 88b69d8's tree; the C.16 result must not be. research/experiments.jsonl run 17's git_sha is 88b69d8d (same sha), so again the logged run carries the registration sha.
- Checkable now: Yes, from git show 88b69d8 and the experiments ledger.

**`MLCryptoEngine/HYPOTHESES.md`:201 (report.md:2872-2900 'The bars, verbatim (progress.md, commit 6025f5c)')** — commit named: `6025f5c`

> **Fixed in progress.md commit 6025f5c (2026-08-06), before the scored window closes**: window 2026-08-04→08-11; ... Outcome-to-action map registered, from "H6 closes, zero open items" through "D.1 fill-simulation input, not a strategy".

- Resolves to: 6025f5c17392d3c8587025f66d5fcc25438ceb19, 2026-08-06 12:18:06 -0700, 'docs: pre-register the H6 thin-perp census bars before the scored window closes'
- What would have to be true: The bars, the BH level, the sample floor, the both-halves rule, the capacity tier and the full outcome-to-action map must all be in 6025f5c's progress.md, and must not differ from what C.27 applied on 2026-08-11. NOTE the claim is carefully scoped: the window opened 2026-08-04, two days BEFORE this commit, so this is registration-before-the-window-CLOSES, not registration-before-any-data. The text says exactly that.
- Checkable now: Yes: git show 6025f5c:progress.md diffed against the bars quoted at report.md:2872-2900 and against the categories registered.py actually applies.

**`MLCryptoEngine/report.md`:2868-2870** — commit named: `287fc10 (machinery, named at HYPOTHESES.md:207)`

> The ten thin instruments were not read: no figure below derives from them**, and the guard that enforces that is a raise, not a comment.

- Resolves to: 287fc108d2cd7c0fa0a554639bb95b69f68372a3, 2026-08-06 12:28:34 -0700, 'feat: thin-perp census machinery, known-answer tested; scored population untouched'
- What would have to be true: research/microstructure/registered.py at 287fc10 must contain a raise that blocks reading the ten scored instruments, and no C.18-era output may contain their figures.
- Checkable now: Yes, from git show 287fc10 and the current registered.py.

**`MLCryptoEngine/DECISIONS.md`:2382-2386 (ADR-059); report.md:4641-4643** — commit named: `4bde24c`

> **Decision.** Instrument selection for scoring is a **rule, registered before** ... (`research/microstructure/blind_universe.py`, commit 4bde24c): 24 h-notional bands (B0 >= $100M cap 3 / ...). ... The rule registered above (commit `4bde24c`) ran once against the live ranking, **after** the registration commit. ... Selection, seed 20260812

- Resolves to: 4bde24c081ae34212fd49e2658160cf78331d6c5, 2026-08-11 21:43:22 -0700, 'docs: pre-register the D.1b blind universe rule, seed committed before retrieval'
- What would have to be true: blind_universe.py and the seed 20260812 must be in 4bde24c's tree; the retrieval and band ranking must postdate that commit; the 25 picks must be reproducible by running the committed rule against the recorded ranking with that seed.
- Checkable now: Yes for the commit content and the seed; the picks are reproducible only if the retrieved ranking is stored (not located in logs/ or data/processed/).

**`MLCryptoEngine/report.md`:2940 (DECISIONS.md:1950-1951)** — commit named: `35e3466`

> Bars registered before any probe (commit 35e3466): **GO requires >= 5,000 ...

- Resolves to: 35e346617425978e7789ad8653a9b8f45eaf2b5c, 2026-08-06 12:47:47 -0700, 'docs: register the C.19 rug-detection audit bars before probing any source'
- What would have to be true: The 5,000-token floor must be in 35e3466's tree and the first Helius probe must postdate it. data/vendor/helius_credit_ledger.jsonl's first row is ts 2026-08-07T03:04:53Z ('probe DezXAZ8z'), which is after 2026-08-06 19:47 UTC - consistent.
- Checkable now: Yes; the credit ledger's first timestamp is a direct, independent check and it passes on the read taken 2026-09-12T18:06Z.

**`MLCryptoEngine/report.md`:3130** — commit named: `902d2e6`

> ### 4. Registered baselines and the first-model bar (commit 902d2e6, before any model)

- Resolves to: 902d2e6c6095a1a87c701535c3f6cc1856347e3e, 2026-08-06 19:05:22 -0700, 'docs: register detection baselines and the first-model bar before any model exists'
- What would have to be true: The baselines and bar must be in 902d2e6's tree; data/processed/detection/hard_rug_scorer.txt (mtime 2026-08-07 03:02) must postdate it.
- Checkable now: Yes; the model file's mtime (UNANCHORED, read 2026-09-12) postdates the commit.

**`MLCryptoEngine/report.md`:2261, 2316** — commit named: `a2d7466 (bars), 5430eba (rho sign-gate correction)`

> All thresholds below were committed to `progress.md` in **commit a2d7466** ... reverse (commit 5430eba), with a regression test.

- Resolves to: a2d7466a06a322fc2a043bc79f2678336bd63825, 2026-08-04 23:47:14 -0700, 'docs: pre-register C.14 pass thresholds before computing any result'; 5430eba51e0c4947ba736d901f855e5e9c9f2702, 2026-08-05 00:17:26 -0700, 'fix: verdict gates the filter branch on signed rho, matching the registered text'
- What would have to be true: The C.14 thresholds must be in a2d7466 before the C.14 run (experiments.jsonl runs 15-16 are git_sha c4497e3d, 2026-08-05T10:26Z and 10:41Z - both after). 5430eba is a correction to the VERDICT LOGIC made 30 minutes after registration and before the result: it must be shown to have changed only the gate's sign handling, not the threshold.
- Checkable now: Yes, from git diff a2d7466..5430eba and the experiments ledger timestamps.

**`MLCryptoEngine/report.md`:5017-5020 (AUDIT.md:3 'Audited commit: ed786ce')** — commit named: `fb296cb (audit record), ed786ce (audited commit)`

> An adversarial audit of this repository (`AUDIT.md`, evidence under `audit/`, commit `fb296cb`) re-derived C.27, D.1c and D.1d from the raw capture and returned 13 findings.

- Resolves to: fb296cb76ed704155c15ef10001c655527411595, 2026-08-12 20:31:44 -0700, 'docs: adversarial audit of the H6 closure chain - 13 findings, closure upheld'; ed786ced21da396c3af45b8545676d0e55de19ff, 2026-08-11 23:16:42 -0700, 'feat: D.1d - the capture does not survive an order-lifecycle fill model; H6 closes'
- What would have to be true: The audit must have run against ed786ce's tree, and the evidence artifacts under audit/ must be the outputs of the scripts committed alongside them. AUDIT.md:19-20 says the file is 'the frozen audit record as delivered against commit ed786ce; it is not updated as fixes land'.
- Checkable now: Yes for the commits; the artifacts under audit/ are anchored and re-runnable against data/raw (14 GB, unanchored).

**`MLCryptoEngine/AUDIT.md`:18-24** — commit named: `none (states 'this file is not updated as fixes land')`

> **Status, 2026-08-12: all findings have been actioned.** ... Headline change: the closure holds and tightens - **PUMP -4.75 -> -4.81, MERL -4.23 -> -4.35**.

- What would have to be true: Each of the 13 findings must have a corresponding change in the tree at or before the anchor. A1 -> tests/test_fill_replay_gate.py + reference_replay.py; A3/A6/A8 -> registered.py:146-207; A4/A5 -> fill_replay.py; A10 -> fees.py; A12 -> performance_report raise.
- Checkable now: Yes, statically, against the anchored snapshot. A2's corrected counterfactual (-4.35 / -2.13) has no stored variant in logs/d1d_summary.json.

**`MLCryptoEngine/AUDIT.md`:586-588 (§E Verdict)** — *no commit named*

> **Pre-registration is genuinely clean: every bar predates its result and no threshold was ever edited.**

- What would have to be true: For every registered bar (370ba41, 88b69d8, 6025f5c, a2d7466, 35e3466, 902d2e6, 4bde24c), git log -p on the registering file must show no later edit to any threshold value before the corresponding result commit. This is a whole-history claim and the strongest provenance statement in the repository.
- Checkable now: Yes, from git history alone (git log -p --follow progress.md over the relevant ranges), for the seven registrations the audit covers. Note the audit's own scope caveat at AUDIT.md:640-647 limits its verdict to the H6 chain.

**`MLCryptoEngine/HYPOTHESES.md`:201** — commit named: `287fc10`

> **Registered bars** ... Machinery known-answer tested: reproduces C.9's BTC -3.05 / ETH -2.75 to **-0.001 / -0.0033 bps**.

- Resolves to: 287fc108d2cd7c0fa0a554639bb95b69f68372a3, 2026-08-06 12:28:34 -0700
- What would have to be true: The known-answer test must exercise the census path (unlike A1's D.1d gate) and its targets must be C.9's published figures rather than values re-derived by the same code.
- Checkable now: Yes: tests/test_registered_census.py and research/microstructure/registered.py are anchored; a trace-based check of which lines execute would settle the A1-style question for this gate too. No such check is recorded anywhere.

**`MLCryptoEngine/research/microstructure/fees.py`:13-20 (module docstring)** — *no commit named*

> **Source.** Hyperliquid perpetuals, base tier (< $5M 14-day volume, no staking discount): **0.015% maker / 0.045% taker** -- 1.5 bps / 4.5 bps. Recorded here 2026-08-12 from the Hyperliquid published fee schedule. This is a *documented* figure, not a measured one

- What would have to be true: config/venues.yaml:182-190 records the same number as 'Perp schedule verified 2026-08-01 (hiperwire.io/explainers/hyperliquid-trading-fees-2026)' - a third-party explainer, not the venue. Two files give two different provenances for the one number every C.27/D.1c/D.1d net scales with.
- Checkable now: Yes, statically: fees.py:13-20 against config/venues.yaml:182-190. Both are anchored.

**`MLCryptoEngine/HYPOTHESES.md`:503-506** — commit named: `none (ADR-060 at DECISIONS.md:2402)`

> the kraken/coinbase feeds were retired at D.1b (2026-08-12), so that overlap stopped accruing at 12 days; reopening H7 now requires restarting those recorders first (one config flip, ADR-060).

- What would have to be true: config/venues.yaml must carry kind: retired for kraken and coinbase (it does, lines 24 and 76); the three-venue overlap must be 12 days; and the kraken/coinbase raw capture must stop at the retirement.
- Checkable now: Yes and CONSISTENT on the live read (2026-09-12T18:08Z): data/raw/venue=kraken and venue=coinbase hold date partitions 2026-07-30 -> 2026-08-12 while venue=hyperliquid holds 2026-08-01 -> 2026-08-13, so the three-venue overlap is 2026-08-01 -> 2026-08-12 = 12 days exactly as claimed. UNANCHORED read.

**`MLCryptoEngine/report.md`:4657-4660** — commit named: `4bde24c`

> The scoring window opened at the subscription restart (2026-08-12, session marker 1786510236894021684); **earliest close 2026-09-09**

- What would have to be true: A session marker with that exact nanosecond value must exist in the recorder's sessions ledger, and the 27 subscribed instruments must appear in data/raw/venue=hyperliquid from that time.
- Checkable now: Partly: the session marker lives in the unanchored recorder state (logs/recorder.log, 83.8 MB, mtime 2026-08-12 22:02). The 2026-09-09 readout postdates the 2026-08-22 anchor entirely, so no anchored evidence can settle it.

**`MLCryptoEngine/docs/notes/h1-predictability-without-capturability.md`:295-311** — commit named: `ddf525d, a2d7466, 5430eba, 03c99f9, b9c07a4, 26d2626, 16b3fa4, fd18ba2, c74257e, 81e456e, 2299c7f, fb296cb`

> Every figure above traces to a section of this project's `report.md` ... and to the commit that produced it. Commits are in `main`. [table of 9 rows naming ddf525d, a2d7466, 5430eba, 03c99f9, b9c07a4, 26d2626, 16b3fa4, fd18ba2, c74257e, 81e456e, 2299c7f, fb296cb]

- Resolves to: Spot-checked: ddf525d35aeb7eeb2c9820caa3145a121afc0029 (2026-08-05 03:46, 'feat: C.14 diagnostics; both closures confirmed, H1's headline number withdrawn'); 81e456e0c910e32563c011921415695a8ca061fc (2026-08-07 17:33). All twelve are stated to be in main.
- What would have to be true: Each named commit must exist in main and its tree must contain the figures the row claims; tests/test_note_honesty.py enforces the note-vs-register agreement but not the note-vs-commit mapping.
- Checkable now: Yes, from git rev-parse/show on all twelve.

---

## Live-repo access log

Every access below was read-only. No `checkout`, `stash`, `reset`, `clean`, `add`, `commit`, `branch`, `merge`, `rebase`, `worktree` or `gc` was run against the audited repository; no file in it was opened for writing; no repository script was executed in place; `.env` was not opened.

| time (UTC) | action | result |
|---|---|---|
| 2026-09-12T18:00:50Z | git -C <live> status --porcelain (PRE-ACCESS) | EMPTY - working tree clean, no untracked, no modified. git rev-parse HEAD = 5359a11fc753cdcd2606aea991dae826293d0307, identical to the anchored SHA. |
| 2026-09-12T18:01Z | ls -la <live> root; git status --porcelain --ignored | Ignored entries only: .env, .mypy_cache/, .pytest_cache/, .ruff_cache/, .venv/, .venv-dl/, _CLOSED_DO_NOT_RUN_HERE, __pycache__ trees, data/processed/, data/raw/, data/vendor/, desktop/dist/, desktop/node_modules/, desktop/src-tauri/{gen,target}/, logs/. .env was NOT opened. _CLOSED_DO_NOT_RUN_HERE (747 B, 2026-09-02) is an operator marker, gitignored, not opened. |
| 2026-09-12T18:02Z | ls -la and du -sh on data/raw, data/processed, data/vendor, logs; ls of date partitions | data/raw 14 G (kraken 6.8 G, coinbase 5.1 G, hyperliquid 2.2 G); data/processed 9.3 G; data/vendor 7.8 G; logs 101 M. No binary opened. |
| 2026-09-12T18:03Z | read logs/d1d_summary.json, logs/d1d_summary_published_2026-08-12.json, logs/d1c_summary.json, logs/validation_summary.json (structure + numeric fields) | Values recorded in the artifacts section. Read-only python json.load; no writes. |
| 2026-09-12T18:05Z | read data/processed/reports/d1d_{PUMP,MERL}_base.json and d1d_MERL_improved.json (top-level fields only); read logs/telemetry_latest.json keys | expectancy_bps_net and trade counts recorded. telemetry_latest.json is mode 0600 latency data, not a credential; only structure and percentiles read. |
| 2026-09-12T18:06Z | wc -l / json scan of data/vendor/archive/manifest.jsonl, data/vendor/spend_ledger.jsonl, data/vendor/helius_credit_ledger.jsonl; wc -l data/processed/detection/*.csv; read data/processed/pairs/universe_2021-08_2026-07.json keys | Counts recorded in the artifacts section. |
| 2026-09-12T18:07Z | git -C <live> log -1 on 15 named commits (370ba41 88b69d8 6025f5c a2d7466 4bde24c 35e3466 902d2e6 fb296cb ed786ce 5430eba ddf525d 287fc10 81e456e 34aebd5 ae4b734) | All 15 resolve in main; subjects and dates recorded in the provenance section. Read-only git log; no checkout, stash, reset or branch operation at any point. |
| 2026-09-12T18:08Z | ls -la and wc -l on data/raw/venue=*/gaps.jsonl and sessions.jsonl; ls date partitions | Counts and partition ranges recorded. |
| 2026-09-12T18:16:13Z | git -C <live> status --porcelain and rev-parse HEAD (POST-ACCESS, final) | EMPTY - working tree still clean; HEAD still 5359a11f…0307. Nothing was written to, created in, or deleted from the audited repository. |

**Pre-access `git -C /home/kiros-li/Documents/GitHub/MLCryptoEngine status --porcelain` (2026-09-12T18:00:50Z), verbatim:**

```
(no output — working tree clean)
```

**Post-access `git -C /home/kiros-li/Documents/GitHub/MLCryptoEngine status --porcelain` (2026-09-12T18:16:13Z), verbatim:**

```
(no output — working tree clean)
```

`git rev-parse HEAD` = `5359a11fc753cdcd2606aea991dae826293d0307`, identical before and after, and identical to the anchored SHA. No pre-existing dirt of any kind was present in this repository, and none was introduced. `git status --porcelain --ignored` lists only expected ignored paths (`.env`, caches, venvs, `data/processed/`, `data/raw/`, `data/vendor/`, `desktop/` build output, `logs/`) plus one operator marker file `_CLOSED_DO_NOT_RUN_HERE` (747 B, mtime 2026-09-02, gitignored, **not opened**) — reported here for completeness, not as dirt.

