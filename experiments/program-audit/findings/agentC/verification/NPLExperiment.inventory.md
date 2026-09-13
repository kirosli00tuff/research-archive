# NPLExperiment — Agent C LOCATE inventory

- Repository: `NPLExperiment`
- Anchored SHA: `8f1fef83be0f76cbd671c2ce0fbfe8b1c4a5ea2c` (main, 2026-09-02)
- Snapshot read: `/home/kiros-li/.cache/program-audit/scratchpad/snap/NPLExperiment/`
- Live repo touched read-only for: git history/provenance and untracked `data/`
- Live HEAD at read time: `dff16632eca6eea05b290ade5464339f44c75744` (2026-09-09T21:46:02-07:00) — **four commits ahead of the anchor**, and one of them (the HEAD commit itself) is `docs: Amendment H5-3 - fire date recomputed at measured 0.77 passes/day; no bar moved, projection was falsified by three lost collection days`. Every claim below is a claim about the anchored SHA; the H5 fire-date claims are known to have been amended by the authors after it.
- Agent C has read nothing under `findings/agentA` or `findings/agentB`.

Counts: **38 artifacts** inventoried (20 tracked under `reports/`, 18 untracked data stores/trees), **101 code files** (62 `src/npl/*.py`, 13 `scripts/`, 26 `tests/`), **23 numeric claims** listed, **7 marked MUST-VERIFY**, **20 provenance claims**.

---

## 1. Artifacts

### 1a. Tracked (ANCHORED) — `reports/`

| # | path | holds | document figures it backs | anchored? |
|---|---|---|---|---|
| A1 | `reports/stage_b/read.json` (8,853 B) | the single spent H1 Stage B read: `co_primaries.p1/p2/p3` (n, successes, statistic, passes), `alpha_adj` 0.016952427508441503, `funding_rows_30_total` 224633, `pending_30/90` 0, `row_fired` "FAIL", `read_at` 2026-08-28T03:01:08Z, 21 module hashes, `secondaries` (cost bands, 90d, strata, truncated, H8) | H1 closure deciding numbers everywhere: HYPOTHESES.md:52, report.md:222-244, REGISTRATION.md:556-571, README.md:6-9, docs/STAGES.md:70 | tracked. sha256 **4455489675c3774f05c977cb7edb9d8b26928f851400077b31263f5826be840c** — matches the value claimed at HYPOTHESES.md:54 exactly (recomputed this session) |
| A2 | `reports/stage_b/preconditions.json` (315,594 B) | per-event/per-control precondition and coverage rows for the 312+176 windows | report.md:120-153 preconditions block; REGISTRATION.md:550 | tracked |
| A3 | `reports/stage_b/hashes_b0.json` (1,651 B) | 19-module read-surface hash set at B.0 | report.md:149-151 | tracked |
| A4 | `reports/stage_b/hashes_b1.json` (1,828 B) | 21-module read-surface hash set at B.1 | report.md:200-206 ("exactly one diff against B.0") | tracked |
| A5 | `reports/stage_b/mutations.md` (1,320 B) | 3 Stage B mutations, all CAUGHT | report.md:280-291 | tracked |
| A6 | `reports/stage_a_h2/ktable_amended.json` (17,687 B) | H2 two-look boundary record: `minimum_n` (E1 42/84/76; E2@0.625 59/117/111; E2@0.600 92/184/169; 2× floor single-look 169), `boundaries` (k1,k2,alpha_spent_look1/look2, power, futility f1), `look1_futility` (E1 31, E2 27), `projected_look_dates` (2026-11-26 / 2027-03-01), `projection_by_month`, `alpha_split_evaluation` (6 candidates), `section0_gate_recomputed` (single 0.888596, two-look 0.862922), `outcome_values_read` 0, `computed_at` 2026-08-28T07:44:41Z | HYPOTHESES.md:70,73,74; report.md:530-566; registrations/H2/REGISTRATION.md:648-760 | tracked |
| A7 | `reports/stage_a_h2/ktable_cull.json` (19,551 B) | the outcome-blind cull k-table: achieved/interim/deadline scenarios, by-dex vs flat pair projections, H4 conditioning rates, powers at k=1,2,3; `computed_at` 2026-08-28T05:41:32Z | report.md:358-376; HYPOTHESES.md:89,106; H3 REGISTRATION:159-185; H4 REGISTRATION:207-221 | tracked |
| A8 | `reports/stage_a_h2/backfill_fallback.json` (10,510 B) | fallback-control backfill: `assigned_n` 24, `distinct_controls` 19, `candidate_universe_n` **175**, `pairs_ledger_total` 62 (`same_dex` 38 / `cross_dex` 24), `fresh_plan_rows` 124, `requests_spent_this_run` 1080, `trail_pages_sealed` 724, `control_leg_spread_states` {expired: 24}, `outcome_values_read` 0 | report.md:506-522; registrations/H2:638-641 | tracked |
| A9 | `reports/stage_a_h2/amend_preconditions.json` (1,683 B) | H2 amendment preconditions: `checked_at` **2026-08-28T06:51:10Z**, gates (ruff clean, mypy 67 files, pytest 217 passed), `h2_read_json_absent` true, `h2_registered_latch_absent` true, `h2_outcome_artifacts_found` [] , `reports_scan_n` 8, `head`/`origin_main` e89b187…, `tree_clean` true, verdict PASS | report.md:445-453 (which states **07:51:10Z**) | tracked |
| A10 | `reports/stage_a_h2/mutations.md` (2,307 B) | register Stage A.4 mutation evidence | report.md:416-424 (6/6 CAUGHT) | tracked |
| A11 | `reports/stage_a_h2/mutations_amend.md` (2,624 B) | Amendment H2-3 mutation evidence, "6 of 6 CAUGHT" | report.md:581-592 | tracked |
| A12 | `reports/stage_a4/mutations.md` (1,782 B) | H1 Stage A.4 mutation evidence | report.md Stage A narrative | tracked |
| A13 | `reports/h5/census.json` (2,490 B) | H5 census pass-1 summary: `instruments_total` 273, `resolved` 151, `live` 94, `by_resolution_state`, `by_dex_live` {io 2, mkts 3, para 16, xyz 73}, `excluded_delisted` 57, `listing_conflicting` 0, `reference_field_used` {oraclePx: 151}, `reference_unserved_live` 0, `requests_charged` 323, `forward_daily_pass_requests` **115**, `forward_share_of_daily_cap` **0.00575**, `snapshot_id` h5-census-2026-08-28T21:51:54Z | report.md:636-655,673-675; HYPOTHESES.md:126-127; registrations/H5:564-570 | tracked |
| A14 | `reports/h5/census.rows.json` (330,621 B, 273 rows) | **the only tracked source of per-instrument basis values**: `basis_bp`, `touch_spread_bp`, `listing_status`, `resolution_state`, `quarantined`, `served_fields`, `session_tag`, all at snapshot `h5-census-2026-08-28T21:51:54Z` | the H5 stratum tables at docs/H5_ACCESS.md:191-195, report.md:657-660, DECISIONS.md:496-499 | tracked |
| A15 | `reports/h5/collector.json` (1,150 B) | the one verified forward pass: `pass_id` h5-census-2026-08-28T22:00:14Z, coverage states (ctx stored 273; funding stored 94 / excluded_ineligible 57; l2 stored 94), `requests_charged` **209**, `ran_at` 2026-08-28T22:02:40Z | report.md:685-687 ("209 requests — 1.05 percent of the daily cap") | tracked |
| A16 | `reports/h5/retro.json` (11,771 B) | the retrospective named secondary: `instruments_eligible` 27, `instruments_excluded_quarantined` 124, `observations_served` 39, `instruments_with_any_observation` 2, `instruments_meeting_30d_coverage` 0, `pooled_by_session_tag` (regular 14.169534 n=17; extended 14.120973 n=14; closed_weekday 20.599501 n=8), 27 `per_instrument` rows, `requests_charged` 27 | report.md:689-701; HYPOTHESES.md:128; registrations/H5:591-616 | tracked |
| A17 | `reports/h5/verdict.json` (3,919 B) | **the fired H5 row**: `fired_at` 2026-08-28T22:04:30Z, `primary_registered_basis` state PENDING with `max_median_abs_bp` 4.14463090419424, `funding_share` 1.0, `instruments_with_reference` 94, `instruments_meeting_coverage` 0, `floor_bp` 18.0 / `viable_bp` 54.0; `inputs.by_session_tag.extended` {n 188, n_absent 0, median 4.14463090419424, q1 0.70947242299609, q3 9.145925118703394, share_over_floor 0.09574468085106383, **share_over_viable 0.015957**}; `census_window` {covered_days_binding_instrument 1, passes_needed 29, projected_fire_date 2026-09-26} | report.md:667-687; HYPOTHESES.md:122,126,132; registrations/H5:555-589 | tracked |
| A18 | `reports/h5/preconditions.json` (4,071 B) | H5 preconditions: `checked_at` 2026-08-28T21:24:00Z, `counts` {census_rows 505, eligibility_h2_rows 62, fresh_plan_rows 124, h2_pairs_rows 62}, gates (mypy 71 files, pytest **249 passed**, ruff clean), 11 H2 store sha256s, three H2 latches absent, `head` fc639c77…, carried context (HFExperiment ADR-026 IBKR figures, 3/9 bp HIP-3 fee measurement) | report.md:581-582; registrations/H5; HYPOTHESES.md:130 | tracked |
| A19 | `reports/h5/h2_verification.json` (4,744 B) | the quarantine proof: 11 H2 store sha256 before/after with `unchanged` true, `h2_pair_count_now` 62 = precondition 62, three latches `absent_now` true; plus a self-disclosed timestamp correction (first write carried a typed 22:36:00Z estimate; actual window 22:07:26Z–22:10:08Z) | HYPOTHESES.md:130; report.md H5 quarantine text | tracked |
| A20 | `reports/h5/mutations.md` (3,234 B) | "Result: 7 of 7 CAUGHT" on the H5 surface | README.md:76; report.md H5 close-out | tracked |

### 1b. Untracked (UNANCHORED) — live working tree, `/home/kiros-li/Documents/GitHub/NPLExperiment/data/` (gitignored by `.gitignore:data/`; `git status --porcelain` is empty)

All read `ls -la` only, plus two JSONL line/field scans, on **2026-09-12 07:50–07:56 UTC**. Anything here may have changed after the anchor — `data/` mtimes run to 2026-09-12.

| # | path | size / mtime | holds | figures it would back |
|---|---|---|---|---|
| U1 | `data/h5/snapshots.jsonl` | 3,719,818 B, 2026-09-11 18:56 | 3,639 rows; **14 distinct `snapshot_id` values** (h5-census-2026-08-28T22:00:14Z … 2026-09-12T01:54:07Z) plus 13 rows with no `snapshot_id`. Contains the **second** of the two 2026-08-28 census snapshots (273 rows) | the 188-observation H5 verdict (one of its two snapshots is here, not in git); the "29 passes / 2026-09-26" projection |
| U2 | `data/h5/census.jsonl` | 547,294 B, 2026-08-28 14:55 | the first census snapshot on disk | H5 census figures |
| U3 | `data/h5/retro.jsonl` | 9,999 B, 2026-08-28 14:56 | retrospective observation rows | retro.json pooled medians |
| U4 | `data/ledgers/requests.jsonl` | 6,636,084 B, 2026-09-12 00:06 | the request ledger (every charge) | every spend claim: 888 H5 requests, 323/pass, 209/day, 1,080 backfill, 846/897 A.1 probe ledger positions, "zero charges by Stage B" |
| U5 | `data/state/stage_b_read.json` | 1,932 B, 2026-08-27 20:01 | **the spent H1 read latch** (claimed sha256 `2d204ccb…438f67e`, 21 module hashes) | HYPOTHESES.md:54; report.md:210-211 |
| U6 | `data/state/generating_sample.json` | 9,720 B, 2026-08-27 20:47 | the 312 quarantined retro event IDs | report.md:322-324; HYPOTHESES.md:138-140 |
| U7 | `data/state/fresh_plan.jsonl` | 20,610 B, 2026-09-09 21:36 | the fresh plan (claimed 124 rows at the amendment) | report.md:513; backfill_fallback.json |
| U8 | `data/state/retro_plan.jsonl` | 105,886 B, 2026-08-27 02:12 | the retro plan (546 rows claimed at progress.md:318) | Stage A/B cohort reconstruction |
| U9 | `data/state/checkpoints.jsonl` | 2,919 B, 2026-09-10 18:40 | +2/+32/+92 checkpoint scheduler state | ADR-007, ADR-019 |
| U10 | `data/state/watcher.jsonl` | 38,156 B, 2026-09-12 00:06 | hourly watcher passes | ADR-012; the "watcher explains moving hashes" note in reports/h5/preconditions.json |
| U11 | `data/controls/h2_pairs.jsonl` | 18,606 B, 2026-09-01 19:01 | the H2 pairs ledger (claimed 62 rows, 38 same_dex + 24 cross_dex) | HYPOTHESES.md:70; report.md:511; h2_verification.json hash `6f2bc967…` |
| U12 | `data/controls/pairs.jsonl` | 47,446 B, 2026-08-27 02:10 | the H1 pairs ledger (claimed 176 rows) | REGISTRATION.md:619 |
| U13 | `data/census/census.jsonl` | 174,131 B, 2026-08-27 22:12 | the H1/H2 census (claimed 505 rows) | reports/h5/preconditions.json counts; report.md:338 (504/505) |
| U14 | `data/eligibility/{h2,h3,h4}.jsonl` | 15,390 / 14,936 / 50,133 B, 2026-08-27 22:24 | per-hypothesis eligibility views (h2 claimed 62 rows) | the cull inputs |
| U15 | `data/spreads/pair_spreads.jsonl`, `spreads.jsonl` | 33,786 B (2026-09-01) / 6,555 B (2026-09-10) | entry-anchor touch-spread snapshots | ADR-008; report.md:354 "both legs' touch spreads snapshotted" |
| U16 | `data/births/` | 24 files (12 `.jsonl` + 12 `.sha256`), 2026-08-27 → 2026-09-11 | daily births manifests, sealed. Dates present: 08-27, 08-28, 08-29, 08-31, 09-02, 09-04, 09-05, 09-06, 09-07, 09-08, 09-09, 09-11 | the accrual figure 18.57 events/month; the forward cohort |
| U17 | `data/outcomes/` | 373 per-instrument directories, 2026-08-26 → 2026-09-10 | sealed raw candle windows (claimed 312 event + 176 control) | the H1 P1/P2/P3 recomputation from primitives |
| U18 | `data/funding/` | 462 per-instrument directories, 2026-08-27 → 2026-09-11 | sealed raw funding pages (claimed 386 archives, 224,633 rows inside the 30d windows) | H8 decomposition; H4 conditioning rates |

### 1c. Analysis code (all tracked / anchored) — 101 files

- **Statistics, where every figure is produced**: `src/npl/power.py` (115 L — exact binomial `pmf`/`upper_tail`/`critical_k`/`exact_power`/`min_n_for_power`, log-space); `src/npl/verdict.py` (203 L — `clopper_pearson_lower` by 200-step bisection on `upper_tail`, `p1_profitability`, `p2_magnitude`, `p3_contrast`, `named_secondaries`, tie rules stated in the docstring); `src/npl/register/sequential.py` (184 L — `look2_spend`, `look2_critical`, `two_look_design`, `two_look_power`, `planned_n1`, `min_n2_for_power`, `futility_boundary`, `look1_stop_probability`); `src/npl/register/cull.py` (291 L — the familywise fixed-point cull); `src/npl/section0.py` (150 L — the outcome map gate); `src/npl/h5/stats.py` (88 L — `median`, linear-interpolated `quantile`, `summarize` returning median/q1/q3/share_over_floor/share_over_viable with n); `src/npl/h5/outcome.py` (222 L — the H5 map); `src/npl/h5/basis.py` (212 L — same-snapshot basis in bp); `src/npl/intervals.py` (30 L — `merge_windows` before any interval sum).
- **Readers and gates**: `src/npl/stageb/{reader.py,cli.py,preconditions.py,__init__.py}`; `src/npl/register/{pairs.py,latches.py,views.py,fresh.py,forward.py,fallback.py,priors.py,generating_sample.py,conditioning.py}`; `src/npl/h5/{gate.py,stores.py,listing.py,coverage.py,census.py,collector.py,resolution.py,calendar.py,retro.py,spend.py,priors.py}`.
- **Collection/substrate**: `census.py`, `eligibility.py`, `controls.py`, `coverage.py`, `archive.py`, `checkpoints.py`, `watcher.py`, `spread.py`, `venue.py`, `pacing.py`, `pairtype.py`, `outcome.py`, `seals.py`, `absence.py`, `blindness.py`, `callstate.py`, `clock.py`, `config.py` (the registered constants), `http.py`, `api.py`, `paths.py`, `registration_check.py`, `cli.py`, `ledger/{append_only.py,__init__.py}`.
- **Scripts that wrote the artifacts**: `scripts/ktable_amended.py` (428 L → A6), `scripts/backfill_fallback.py` (262 L → A8), `scripts/h5_census.py` (→ A13/A14), `scripts/h5_retro.py` (→ A16), `scripts/h5_fire.py` (→ A17), `scripts/h5_pass.py` (→ A15), `scripts/mutations*.py` (5 files → A5/A10/A11/A12/A20), `scripts/{npl_guard.sh,wait_for_net.sh}`.
- **Tests**: 26 files, 583 L in `tests/test_amend.py` alone; `tests/test_guards.py` (283 L) carries the AST pins the quarantine claims rest on. The claimed gate figures (249 passed / mypy 71 files) are **not verifiable by reading**; they would need a copy-out-and-run, and no test run may happen inside the audited tree.

---

## 2. Numeric claims, ranked (MUST-VERIFY marked)

Rank 1 is the number a registered amendment rests on and that the repo's own fired artifact appears to contradict; ranks 2–7 are the other deciding numbers of a fired row or a registered boundary.

### **[MUST-VERIFY] C1 — the H5 live stratum has "0.0 %" over the 54 bp VIABLE bar (and median 3.72 bp)**

> "| **live** | **94** | **3.72 bp** | 0.73 – 7.31 | 51.4 bp | 8.5 % | **0.0 %** |"
> — `NPLExperiment/docs/H5_ACCESS.md:193` (identically `report.md:659`)

> "**Every observation above the 54 bp VIABLE bar lives in the delisted stratum.**" — `NPLExperiment/docs/H5_ACCESS.md:197`

> "the delisted stratum is where **every** observation above the 54 bp bar lived: median 30.5 bp with 45.6 % over the bar, against 3.72 bp and **0.0 %** for live instruments in the same snapshot." — `NPLExperiment/HYPOTHESES.md:129`

> "the delisted stratum's median absolute basis is **30.5 bp with 45.6 percent over the 54 bp bar**, against **3.72 bp and 0.0 percent** for live instruments in the same snapshot. **Every observation above the bar lived in dead markets.**" — `NPLExperiment/DECISIONS.md:496-499`

- Figures and n: live n = 94, median 3.72 bp, IQR 0.73–7.31, max 51.4 bp, 8.5 % > 18 bp, **0.0 % > 54 bp**.
- Producing artifact/code: `reports/h5/census.rows.json` (A14) + `src/npl/h5/stats.py:summarize`.
- Why it ranks first: it is the whole stated justification for **Amendment H5-2**, the amendment the program presents as its credibility exhibit ("deleted this entry's only route to VIABLE", report.md:662-665) and as the demonstration of the honesty clause.
- Already found at LOCATE (recomputed this session from A14 with `src/npl/h5/stats.py`'s own quantile rule): live-and-resolved n = 94 in that snapshot gives **median 4.2137, q1 0.7412, q3 9.0865, max 55.64, 7.45 % > 18 bp, 1.06 % > 54 bp**. The second 2026-08-28 snapshot (U1) gives median 4.1404, max 63.29, **2.13 % > 54 bp**. No filter variant tried (any-resolution live, quarantined-only, non-quarantined, l2-stored) reproduces 3.72 / 0.73–7.31 / 51.4 / 8.5 % / 0.0 %. And `reports/h5/verdict.json` itself records `share_over_viable` = **0.015957** on the pooled live n = 188. `docs/H5_ACCESS.md` was added in commit `13c6965` at 2026-08-28T21:59:42Z — after snapshot 1 (21:51:54Z), before snapshot 2 (22:00:14Z) — so snapshot 1 is the only snapshot it can be summarizing.
- The delisted row of the same table (30.52 / 0.00–210.79 / 2,481 / 54.4 % / 45.6 %) **does** reproduce exactly.

### **[MUST-VERIFY] C2 — the fired H5 PENDING row's four deciding figures**

> "| instruments carrying a served reference | **94** | ≥ 20 | **clears** | … | funding served on those instruments | **94 of 94, share 1.000** | ≥ 0.500 | **clears** | … | instruments at 30 days of coverage | **0** | ≥ 20 | **window open** | … | median absolute basis, `extended` (n = 188) | **4.14 bp** | floor 18 / bar 54 |"
> — `NPLExperiment/report.md:673-676` (also `HYPOTHESES.md:126`, `registrations/H5/REGISTRATION.md:567-575`)

- Figures and n: 94 / 94 of 94 (share 1.000) / 0 / median 4.14 bp with IQR 0.71–9.15, 9.57 % over floor, 1.60 % over bar, n = 188 across 2 snapshots.
- Producing artifact/code: `reports/h5/verdict.json` (A17) written by `scripts/h5_fire.py` over `src/npl/h5/outcome.py` + `stats.py`.
- LOCATE status: the 188-observation summary **reproduces exactly** from A14 pooled with the second snapshot in U1 — median 4.1446, q1 0.7095, q3 9.1459, share>18 0.0957, share>54 0.0160. Verify the instrument counts and the bars against `src/npl/config.py` (`h5_min_instruments_with_reference`, `h5_min_coverage_days`, `h5_funding_service_share`, `h5_viable_basis_multiple`).

### **[MUST-VERIFY] C3 — "29 daily passes needed; projected fire date 2026-09-26"**

> "**PENDING — the census window is open** · fired 2026-08-28T22:20Z. Both structural clauses **clear**; what is missing is time. **29 daily passes needed; projected fire date 2026-09-26.**" — `NPLExperiment/HYPOTHESES.md:122`
> "**29 daily passes remain.**" — `NPLExperiment/report.md:685`; "**Passes still needed: 29. Projected fire date: 2026-09-26**" — `NPLExperiment/registrations/H5/REGISTRATION.md:587`

- Figures and n: 29 passes; binding instrument at 1 covered day; 20th-best-covered instrument; bar 20 instruments at 30 covered days.
- Producing artifact/code: `reports/h5/verdict.json:census_window` + `src/npl/h5/coverage.py`.
- Why it ranks: it is the only forward commitment the H5 entry makes, and the one a closure would rest on.
- LOCATE status: the assumption is one pass per day. U1 shows **14 census snapshots between 2026-08-28 and 2026-09-12** — 2026-09-05 and 2026-09-06 absent entirely, 2026-09-03 with only 4 rows. The live repo's own post-anchor HEAD commit `dff1663` (2026-09-09) reads "fire date recomputed at measured **0.77 passes/day** … projection was falsified by three lost collection days". A finding here must say plainly it could be invalidated (indeed, was addressed) by later commits.

### **[MUST-VERIFY] C4 — the H1 closure's three co-primaries**

> "**P1** 197/312 positive (63.14%), exact lower bound **0.5707** against the 0.60 bar — FAIL; **P2** 111/312 at ≤ −15% net (35.58%), sign-test p = **1.000** — FAIL; **P3** 114/175 pairs young-below-control (65.14%), p = **3.767e-05** — PASS. Cost-insensitive across the registered bands (P1 lb 0.5740 / 0.5707 / 0.5609, n = 312 each)."
> — `NPLExperiment/HYPOTHESES.md:52` (also report.md:222-224, 297-299; REGISTRATION.md:556-568; README.md:6-9; docs/STAGES.md:70)

- Figures and n: P1 197/312, lb 0.5707 at alpha_adj 0.016952; P2 111/312, p = 1.000; P3 114/175, p = 3.767e-05; bands 198/197/194 of 312.
- Producing artifact/code: `reports/h5` n/a — `reports/stage_b/read.json` (A1) written by `src/npl/stageb/cli.py` over `src/npl/verdict.py:clopper_pearson_lower` and `src/npl/power.py:upper_tail`.
- Why it ranks: this is the number that closed the founding hypothesis. It is fully recomputable from counts alone; A1's stored statistics are 0.5706880326738533, 0.9999998937952859 and 3.766632285793312e-05.

### **[MUST-VERIFY] C5 — H2's governing minimum N, the two-look spends, and the look dates**

> "Look-1 min N **59** (E1 42, E2 59), look-2 min N **117** (E1 84, E2 117). At the look-2 minimum: k₁ = 38, k₂ = 69, exact spend 0.0182 + 0.0240 = 0.0422 inside alpha_h. Futility at n₁ = 59: E1 f₁ = 31, E2 f₁ = 27 at the 0.10 conditional-power floor."
> — `NPLExperiment/HYPOTHESES.md:73`

> "| at look-1 min N | 59 | 30 | 22 | 37 | 0.0173 + 0.0200 = 0.0373 | 0.7031 | 0.5529 | … | at the deadline | 135 | 68 | 43 | 79 | 0.0176 + 0.0227 = 0.0403 | 0.9552 | **0.8629** |"
> — `NPLExperiment/registrations/H2/REGISTRATION.md:695,697` (also report.md:546-548)

> "**Look 1 projects to 2026-11-26 and look 2 to 2027-03-01 — one month inside the registered 2027-03-31 deadline**" — `NPLExperiment/report.md:561-563`

- Figures and n: min N 42/84, 59/117, 111, 169, 184/92; k₁/k₂ 22/37, 38/69, 43/79; spends 0.0373, 0.0422, 0.0403; powers 0.7031/0.5529, 0.9322/0.8237, 0.9552/0.8629; futility 31/27; dates 2026-11-26 / 2027-03-01 at accrual 18.57/month and match rate 1.000.
- Producing artifact/code: `reports/stage_a_h2/ktable_amended.json` (A6) written by `scripts/ktable_amended.py` over `src/npl/register/sequential.py`.
- LOCATE status: the **totals** match A6 but two of the three **component** spends in the registration table do not. A6 records at look-1 min N `alpha_spent_look1` 0.008062 + `alpha_spent_look2` 0.029206 = 0.037268 (doc prints 0.0173 + 0.0200), and at the deadline 0.019230 + 0.021113 = 0.040343 (doc prints 0.0176 + 0.0227). Only the look-2-min-N row (0.018172 + 0.024025 = 0.042197) matches its printed components. Verify whether the printed components are stale or from another scenario.

### **[MUST-VERIFY] C6 — E2's 0.625 true share, and the "does not reach 0.80" alternative**

> "**E2 true share 0.625** under the 1× floor, by stated linear interpolation between multiple 0 (E1's 0.65) and multiple 2 (the registered 0.60) — a choice, not a measurement, so **every minimum N is also reported at the unchanged 0.60** (E2 then needs 92/184 and does not reach 0.80 by the deadline)."
> — `NPLExperiment/HYPOTHESES.md:74` (also report.md:476-481, 536, 544; registrations/H2/REGISTRATION.md:675,683)

- Figures and n: 0.625 interpolated; 0.60 alternative → 92/184; single-look power at the deadline N = 135 is 0.888596 at 0.625 and 0.731814 at 0.600 (A6 `single_look_k_table_extension_at_deadline`).
- Why it ranks: the entire justification for the weakened floor turns on an assumption the authors themselves label a choice; the alternative they report beside it fails the registered 0.80 target.

### **[MUST-VERIFY] C7 — the live median touch spread**

> "Live median touch spread **4.18 bp** (IQR 1.31–10.78)." — `NPLExperiment/report.md:643` (also docs/H5_ACCESS.md §"Is there a book?")

- Figures and n: n = 94 live instruments.
- Producing artifact: `reports/h5/census.rows.json:touch_spread_bp` (A14).
- LOCATE status: snapshot 1 gives median **3.1586** (IQR 1.2270–10.4125, n = 94); snapshot 2 (U1) gives median **3.8388** (IQR 0.9986–11.7339). Neither is 4.18 / 1.31–10.78. Same shape of discrepancy as C1 and on the same rows, so verifying them together is efficient.

### The rest, ranked

| # | claim (verbatim, shortened) | file:line | figures, n | believed source |
|---|---|---|---|---|
| C8 | "**Pass 1 (k = 3, alpha_h = 0.016952):** H2 required 0.5771; H3 0.0000; H4 best cell 0.0140 → **H3 and H4 fire BLOCKED.** … **Pass 2 (k = 1, alpha_h = 0.05):** H2 required 0.7604 → fixed point" | report.md:362-365 | powers 0.5771/0.0000/0.0140/0.7604; min-N 76/169; 141 projected deadline pairs; n = 38 achieved pairs | `ktable_cull.json` (A7), `register/cull.py`, `power.py` |
| C9 | "measured main-dex accrual 0.5/month (n = 3/182d) against a P1 min-N of 262; deadline N = 5; both required legs at ~0 power" | HYPOTHESES.md:89; registrations/H3/REGISTRATION.md:161,174,185 | 0.5/month, n = 3 in 182 d; min-N 262; deadline N 5 | `ktable_cull.json`, `data/census/census.jsonl` (U13) |
| C10 | "measured conditioning rates 0.177/0.129/0.081 (n = 62; median trailing entry funding +31.6%/yr…); best-cell deadline power 0.014 governing (0.711 even at the declined optimistic 0.85)" | HYPOTHESES.md:106; registrations/H4/REGISTRATION.md:211-221 | 11/62, 8/62, 5/62; median +31.6 %/yr (min −132.4); powers 0.0140/0.0037/0.0025 | `ktable_cull.json` (`conditioning_rates`), `register/conditioning.py`, `data/funding/` (U18) |
| C11 | "Accrual re-measured at **18.57 events/month** (n = 113 listings/182d) — the carried 18.5 confirmed — but **main-dex accrual measured 0.5/month (n = 3)**" | report.md:340-343 | 18.57/month, n = 113/182 d | `data/census/census.jsonl` (U13), `data/births/` (U16) |
| C12 | "**24 of 24, zero exclusions**, 19 distinct controls, 174 candidates considered per event and **none skipped for coverage**. The pairs ledger stands at **62 rows — 38 `same_dex` plus 24 `cross_dex`**" | report.md:509-512 | 24/24, 19 controls, 174 candidates, 62 rows | `backfill_fallback.json` (A8) — which records `candidate_universe_n` **175**, not 174 |
| C13 | "H8 decomposition (n = 312): mean funding term +1.33%, mean price term +1.00% per event over 30 days — the average short earned about **+2.2%** net… Paired (n = 175): funding differential +0.88 points, price differential +6.43 points" | report.md:240-244 | 0.013317, 0.009990 (sum 2.33 %), 0.008816, 0.064263 | `read.json:secondaries.h8_decomposition_30d`/`h8_paired_30d` (A1) — paired figures reproduce exactly; the "+2.2 %" is 2.33 % before costs |
| C14 | "273 HIP-3 instruments over 10 dexs → **151 resolved** (118 equity, 15 ETF, 18 index), 80 `excluded_non_equity`, 42 `excluded_unresolvable`, → **94 live** … The live family is two dexs: `xyz` 73, `para` 16." | HYPOTHESES.md:127 (also report.md:649-650) | 273/151/94; 118+15+18; 80+42; 73+16 = 89 | `census.json` (A13) — whose `by_dex_live` is {xyz 73, para 16, **mkts 3, io 2**} = 94; docs/H5_ACCESS.md:153 states the 89-of-94 split correctly |
| C15 | "The cohort gate leaves **27 of 151** … **25 return no funding rows at all** … and **2 are days-old listings** — `io:NBIS` (n = 8, 1 covered day) and `xyz:XBI` (n = 31, 2 days). **39 observations, 2 instruments, 0 meeting the 30-day bar.**" | report.md:691-695 | 27/151, 124 quarantined, 39 obs, n = 8 and n = 31 | `retro.json` (A16) |
| C16 | "**32 of the 57 delisted instruments are still being served an unbroken hourly funding series** — 168 rows each, the most recent stamped 2026-08-28T21:00Z" | report.md:705-707; HYPOTHESES.md:129 | 32 of 57, 168 rows each | `census.rows.json` funding fields (A14), `data/funding/` (U18) |
| C17 | "the collector … runs last in the 01:40Z daily pass, at 209 requests — **1.05 percent of the daily cap**" | report.md:686 | 209 / 20,000 = 1.045 % | `collector.json` (A15). `census.json` (A13) instead records `forward_daily_pass_requests` 115 and `forward_share_of_daily_cap` 0.00575 |
| C18 | "**Spend for the whole entry: 1,124 requests**" corrected to "**888** — 6 reconnaissance + 323 census pass 1 + 323 census pass 2 + 27 retrospective + 209 forward pass … **4.44 percent of the daily cap** … day total 3,847 of 20,000 (19.2 %)" | progress.md:1459, 1502-1516 | 888 = 6+323+323+27+209; 3,847 day total | `data/ledgers/requests.jsonl` (U4); commit c2aaa27 is the correction |
| C19 | "Two full census passes, 323 requests each, returning **identical** counts, plus a 6-request reconnaissance probe" | report.md:636; docs/H5_ACCESS.md:3-4 | 323 + 323 + 6 = 652 | A13/A15 + U4 |
| C20 | "served premium −0.0003482613 equals (77501.0 − 77528.0)/77528.0 exactly, where 77501.0 is the served impact ask" | report.md:645 | one arithmetic identity | recomputable in one line; `docs/H5_ACCESS.md` verbatim fragment |
| C21 | "**Effective N:** P1 312, P2 312, P3 175 — against the registered minimums 34, 103, 60. All clear." and "224,633 funding rows summed inside the 30-day windows" | report.md:146-147, 216 | 312/312/175 vs 34/103/60; 224,633 rows | `read.json:preconditions` (A1); `data/funding/` (U18) |
| C22 | "156 pages, 60,010 funding hours, **0 unrecoverable hours**" and "The census refresh found 504 instruments" | report.md:336-339 | 156, 60,010, 0; 504 (505 on disk at the H5 precondition) | `data/funding/` (U18), `data/census/census.jsonl` (U13); A18 records `census_rows` 505 |
| C23 | "`make all` green throughout: ruff, `mypy --strict` on 71 files, **249 tests**" | report.md:581-582 (also 217/67 at A9, 172/54 at report.md:292, 159/50 at report.md:148) | 249, 217, 172, 159 tests | `reports/h5/preconditions.json` (A18), `amend_preconditions.json` (A9). **Not verifiable by reading** — a test run inside the audited tree is forbidden |

---

## 3. Intervals and tests

No document reports a two-sided confidence interval anywhere. Every "interval" is either a **one-sided exact (Clopper–Pearson) lower confidence bound** or an **IQR**, which is a dispersion summary and not an interval estimate. Every test is an **exact binomial** test; there is no asymptotic statistic, no t-test, no regression, and no bootstrap in the repository.

### 3a. Confidence bounds (one-sided, exact)

| # | bound | file:line | estimator | figure | n | data structure |
|---|---|---|---|---|---|---|
| I1 | P1 lower bound at alpha_adj | REGISTRATION.md:556; HYPOTHESES.md:52; report.md:222 | Clopper–Pearson one-sided lower bound, alpha_adj = 0.016952, bar 0.60 | **0.5707** (197 successes) | 312 | one Bernoulli per event (net short 30 d > 0), `verdict.py:clopper_pearson_lower` |
| I2 | P1 cost-band bounds | REGISTRATION.md:566; report.md:230-231 | same | 0.5740 (198) / 0.5707 (197) / 0.5609 (194) | 312 each | same, three registered cost bands |
| I3 | P1 at 90 days | REGISTRATION.md:571; report.md:233 | same | **0.6069** (208) — descriptive only | 312 | same at the 90-day horizon |
| I4 | the registered bars themselves | REGISTRATION.md:201-237 | alpha_adj = 1 − 0.95^(1/3) = **0.016952**; alpha_h = 1 − 0.95^(1/k) = **0.05** at k = 1 | — | — | `src/npl/config.py:ALPHA_ADJ`, `register/cull.py` |

### 3b. Test statistics and p-values

| # | test | file:line | stated estimator | p / statistic | n | data structure |
|---|---|---|---|---|---|---|
| T1 | P2 magnitude | REGISTRATION.md:560; HYPOTHESES.md:52; report.md:223 | exact one-sided sign test, p₀ = 0.5, success = net ≤ −15 % asset-side | **p = 1.000** (stored 0.9999998937952859), 111 successes | 312 | per-event Bernoulli |
| T2 | P3 listing-age contrast | REGISTRATION.md:563; HYPOTHESES.md:52; report.md:224 | exact one-sided sign test, p₀ = 0.5, success = young net short > control | **p = 3.767e-05** (stored 3.766632285793312e-05), 114 successes | 175 pairs | paired young-vs-control, 137 of 312 events underpowered/unpaired |
| T3 | P2 at 90 days | REGISTRATION.md:571; report.md:235 | same as T1 | **p = 0.3886**, 159 successes | 312 | same |
| T4 | P3 at 90 days | REGISTRATION.md:571; report.md:235 | same as T2 | **p = 2.36e-04**, 111 successes | 175 | same |
| T5 | H2 two-look exact binomial boundary | registrations/H2/REGISTRATION.md:691-701; report.md:546-548 | exact binomial critical values k₁ (alpha_1 = 0.02) and k₂ (conditional spend over the independent increment, alpha_2 = 0.03), p₀ = 0.5 | k₁/k₂ = 22/37 (n₁=30,n₂=59), **38/69** (59,117), 43/79 (68,135); spends 0.0373 / **0.0422** / 0.0403 | 59 / 117 / 135 pairs | per-pair Bernoulli, two co-primaries E1 and E2, `register/sequential.py` |
| T6 | H2 futility boundary | registrations/H2/REGISTRATION.md:712-718; report.md:555 | conditional power floor 0.10 at n₁ | E1 **f₁ = 31**, E2 **f₁ = 27** | 59 | same |
| T7 | H2 power figures | report.md:565; HYPOTHESES.md:70 | exact binomial power at the registered true shares | single-look **0.8886**, two-look **0.8629** (0.9665 / 0.9552 for E1; 0.7318 at the 0.60 alternative) | 135 projected | `power.py:exact_power`, `sequential.py:two_look_power` |
| T8 | the alpha-split materiality screen | registrations/H2/REGISTRATION.md:654-661 | six candidate splits vs a two-clause test (gain ≥ 0.01, interim stop-loss ≤ 0.05) | e.g. 0.01/0.04 → power 0.8900 (+0.0270) but P(interim fires) 0.3112 (−0.1930) | evaluated at n₂ = 135 | `ktable_amended.json:alpha_split_evaluation` |
| T9 | H4 within-hypothesis Sidak | registrations/H4/REGISTRATION.md:79-80,207 | alpha_cell = 1 − (1 − alpha_h)^(1/3) | **0.00568** at alpha_h = 0.016952 | 3 cells | `register/conditioning.py` |
| T10 | the cull's power screen | report.md:362-365 | exact binomial power vs a 0.50 floor at the achievable N | H2 0.5771 / H3 0.0000 / H4 0.0140 at k = 3; H2 0.7604 at k = 1 | 38 achieved / 141 projected pairs; H3 n = 5; H4 best cell | `ktable_cull.json`, `register/cull.py` |
| T11 | H5 primary summary (not a test) | report.md:676; HYPOTHESES.md:126; registrations/H5:573-574 | median, linear-interpolated quartiles, exceedance shares; **no test statistic and no p-value is computed anywhere in H5** | median 4.14 bp, **IQR 0.71–9.15**, 9.57 % / 1.60 % | 188 | `h5/stats.py:summarize` |
| T12 | H5 stratum IQRs | docs/H5_ACCESS.md:193-195; report.md:659-660 | same | live IQR 0.73–7.31 (claimed); delisted 0.00–210.79; all-resolved 0.00–18.13 | 94 / 57 / 151 | `census.rows.json` (A14) |
| T13 | H5 retrospective pooled IQRs | registrations/H5:601; retro.json | same | regular 14.17 (n=17), extended 14.12 (n=14), closed_weekday 20.60 (n=8), weekend none | 39 total | `retro.json` (A16) |
| T14 | H5 touch-spread IQR | report.md:643 | same | median 4.18, IQR 1.31–10.78 | 94 | `census.rows.json:touch_spread_bp` |

---

## 4. Provenance claims

Every claim below is recorded verbatim with what would have to be true for it to hold. Commit times are converted to UTC from the repository's local `-07:00` author/commit stamps.

| # | claim (verbatim) | file:line | commit named | what would have to be true | LOCATE status |
|---|---|---|---|---|---|
| P1 | "docs: register Sections 0-13 before any network call" (commit subject) | git `cd640b6`; REGISTRATION.md is the object | `cd640b6` = **2026-08-27T00:54:38Z** | no request-ledger row earlier than 00:54:38Z | `docs/ACCESS.md:8` dates the first access verification at **2026-08-27T00:56–00:58Z**, 2 minutes after. Checkable against `data/ledgers/requests.jsonl` (U4, untracked) |
| P2 | "Amendment 3 was committed and pushed (commit 6399d63) while the only data in existence were counts, timestamps, and coverage — before the reader existed." | report.md:157-158 (also REGISTRATION.md:457) | **6399d63** | 6399d63 precedes both `stageb/reader.py` and the read | `6399d63` = 2026-08-28T02:49:19Z touching only `REGISTRATION.md`; `reader.py`+`cli.py` first appear in `32b3f9e` = 03:00:42Z; `read.json:read_at` = 03:01:08Z. Ordering confirmed by git |
| P3 | "the 312 retro event IDs are recorded in data/state/generating_sample.json, and every successor view refuses them — the refusals produced by test on synthetic offenders, never asserted" | report.md:322-325 | none | the file holds exactly 312 IDs and `register/generating_sample.py` + `views.py` refuse them | file exists untracked (U6, 9,720 B, mtime 2026-08-27 20:47). Refusal is code+test, readable in SNAP |
| P4 | "Amended the same day, before any pair outcome existed (H2-3, H2-4)" | HYPOTHESES.md:14, 70 | `f31f7a3` (H2-3), `546b2e3` (H2-4) | no H2 outcome value, latch or artifact existed at 2026-08-28T07:01:06Z / 07:46:42Z | `amend_preconditions.json` (A9) records `h2_read_json_absent`, `h2_registered_latch_absent`, `h2_outcome_artifacts_found` [] and `head` e89b187; `f31f7a3` touches only progress.md + H2 REGISTRATION + the precondition artifact |
| P5 | "**Amendment H2-3 registered three changes before a line of code moved, and was committed and pushed before any of them was implemented.**" | report.md:455-456 | `f31f7a3` | that commit contains no implementation | confirmed by `--name-status`: `progress.md`, `registrations/H2/REGISTRATION.md`, `reports/stage_a_h2/amend_preconditions.json` only. The implementation lands in `f8e54d8` 39 minutes later |
| P6 | "**Chosen before any pair outcome existed.** At the moment this line was [written]…" | registrations/H2/REGISTRATION.md:475 (also :395, :707, :773; DECISIONS.md:262, 297, 326, 365) | none | as P4 | same evidence as P4 |
| P7 | "The correction, made now, **before any outcome value exists and before the reader has seen anything but synthetic fixtures**" (the H2-4 §7 look-2 GO defect) | registrations/H2/REGISTRATION.md:773-776 | `546b2e3` | the per-look latches absent and the reader fixture-only at 07:46:42Z | report.md:594-598 asserts both latches absent at stage close; latches are untracked (`data/state/h2_look*_latch.json`) and `reports/h5/preconditions.json` (A18) independently records all three H2 latches absent at 2026-08-28T21:24Z |
| P8 | "`registrations/H5/REGISTRATION.md` was committed and pushed with **zero H5 requests sent**" | report.md:617-618 | `98e7e01` | no H5 request charged before 2026-08-28T21:38:58Z | `census.json` (A13) `snapshot_id` = h5-census-**2026-08-28T21:51:54Z**, 13 minutes later. Checkable against U4 |
| P9 | "an **exact-string mapping registered before any price was read**" (198 entries) | HYPOTHESES.md:125; report.md:620; DECISIONS.md:382; registrations/H5:92,551; docs/H5_ACCESS.md:130,179 | `98e7e01` | `src/npl/h5/resolution.py` exists at 21:38:58Z and is unchanged when prices arrive | `resolution.py` is added by `98e7e01` (git `--name-status`); whether it changed afterwards is a `git log --follow` check |
| P10 | "tagged by US market session against a calendar **registered before collection**" | HYPOTHESES.md:125; registrations/H5:209 | `98e7e01` | `src/npl/h5/calendar.py` (2024–2027, four tags) added before the first snapshot | `calendar.py` added by `98e7e01`; first snapshot 21:51:54Z |
| P11 | "the outcome map built dark with fixtures sitting exactly on 18.00 bp, 54.00 bp, 20 instruments and a 10-of-20 funding share" and "Boundary conventions, fixed before data and each with a fixture sitting exactly on it" | report.md:621-623; DECISIONS.md:483-487 | `98e7e01` | `h5/outcome.py` + its boundary fixtures predate the census | `outcome.py` added by `98e7e01`; fixtures live in `tests/test_h5_registration.py` (547 L, added in the same commit) |
| P12 | "Three consequences were registered **before** measurement, because the obvious implementation breaks all three" | report.md:626-631; DECISIONS.md:533 | `98e7e01` | the three Section 0 consequences are in the file as first committed | diffable: `git show 98e7e01:registrations/H5/REGISTRATION.md` |
| P13 | "That amendment was made before any firing and makes CLOSED **strictly harder**; it cost this entry a same-day close." (Amendment H5-1) | report.md:679-683 | `13c6965` | H5-1 committed before `verdict.json:fired_at` | `13c6965` = 2026-08-28T21:59:42Z; `fired_at` = 22:04:30Z (A17). Note H5-1 was nonetheless written **after** census pass 1 (21:51:54Z) |
| P14 | "**The amendment deleted this entry's only route to VIABLE** … it was made with the census in hand, disclosed in full in its own text, and it costs rather than buys." (Amendment H5-2) | report.md:662-665; DECISIONS.md:509-513 | `13c6965` | the amendment is post-hoc **and self-disclosed as such**, and its direction is restrictive | self-disclosed. The measurement it rests on is claim **C1**, which does not reproduce from A14 |
| P15 | "Latch `data/state/stage_b_read.json` sha256 `2d204ccb…438f67e` (21 module hashes inside); artifact `reports/stage_b/read.json` sha256 `4455489675c…be840c`. Read 2026-08-28T03:01:08Z, exactly once." | HYPOTHESES.md:54 | none (hashes) | both hashes reproduce; the latch contains 21 module hashes | **`read.json` sha256 recomputed this session = `4455489675c3774f05c977cb7edb9d8b26928f851400077b31263f5826be840c` — matches.** The latch is untracked (U5) and was not opened |
| P16 | "**The B.1 re-hash** (reports/stage_b/hashes_b1.json, 21 modules): exactly one diff against B.0 … Every other read-surface module is byte-identical to its B.0 hash." | report.md:200-206 | none | A3 vs A4 differ on `stageb/__init__.py` only, plus two additions | directly diffable between A3 and A4, and the 21 hashes inside A1 can be checked against the SNAP source files |
| P17 | "H2's collectors, ledgers, latches and stores are **read-only** to every H5 path … the cohort ledgers are read precisely so the quarantine can be honoured." | HYPOTHESES.md:130; DECISIONS.md:515-546 | none | the 11 store hashes unchanged across the H5 stage, pair count 62, three latches absent | `reports/h5/h2_verification.json` (A19) records exactly that, before/after, `unchanged` true on all 11 |
| P18 | "alpha_h = 1 − 0.95^(1/k), fixed at the cull, recorded in every surviving registration by amendment, **never revisited after any outcome exists**" | HYPOTHESES.md:143-145 (Amendment H2-1) | none | no later commit changes `family_confidence` or the recorded alpha_h | checkable with `git log -p -- src/npl/config.py` across the anchor |
| P19 | "all three registrations … were committed and pushed before any successor measurement" | report.md:327-330 | `77ee522` | A.0 precedes the A.1 measurement | `77ee522` = 2026-08-28T03:53:20Z; A.1 lands in `c4003e5` = 2026-08-28T05:21:55Z |
| P20 | Two self-disclosed timestamp corrections, one still uncorrected in two files: the H5 Section 6 record is "headed **22:20Z**. That figure was typed by the assistant as an estimate rather than read from the clock. **The map actually fired at 2026-08-28T22:04:30Z**" | registrations/H5/REGISTRATION.md:632-639 | none | the correction is recorded and the artifact carries the true time | `verdict.json:fired_at` = 22:04:30Z confirms. **But at the anchor `HYPOTHESES.md:122` and `report.md:667` still read "fired 2026-08-28T22:20Z".** A parallel case: `report.md:446` states the amendment preconditions passed "at 07:51:10Z on the project clock" where `amend_preconditions.json` records **06:51:10Z** |

### Post-anchor provenance note (anchoring caveat)

The live repository is four commits ahead of the anchor. Commit `dff16632eca6eea05b290ade5464339f44c75744` (2026-09-09T21:46:02-07:00) is titled *"docs: Amendment H5-3 - fire date recomputed at measured 0.77 passes/day; no bar moved, projection was falsified by three lost collection days"*. Any finding against claim **C3** (29 passes / 2026-09-26) must state that the authors themselves recorded the falsification after the anchored SHA, and must be framed as a claim about `8f1fef8` only.

---

## Live-repo access log

Live path: `/home/kiros-li/Documents/GitHub/NPLExperiment/`. All access read-only. No file under the audited repository was opened for writing, no script was executed inside it, and no git command other than `status`, `log`, `show`, `rev-parse` was run.

**Pre-access `git -C /home/kiros-li/Documents/GitHub/NPLExperiment status --porcelain`, 2026-09-12 07:50:43 UTC — output verbatim:**

```
```

(empty — no modified, staged or untracked entries; `data/` is covered by `.gitignore`)

**Post-access `git -C /home/kiros-li/Documents/GitHub/NPLExperiment status --porcelain`, 2026-09-12 07:56:52 UTC — output verbatim:**

```
```

(empty — unchanged; nothing was written to the audited repository)

**What was read live, and when (all UTC 2026-09-12):**

1. 07:50:43 — `git status --porcelain` (pre-access).
2. 07:50:4x — `ls -la` of the repository root and of `data/`, `data/births/`, `data/census/`, `data/controls/`, `data/eligibility/`, `data/funding/` (head), `data/h5/`, `data/ledgers/`, `data/outcomes/` (head), `data/spreads/`, `data/state/`. Sizes and mtimes only; no large binary opened.
3. 07:50:4x — `git rev-parse HEAD`, `git log -1`.
4. 07:52–07:53 — `git log --format=…` (37 commits) and `git show --stat --name-status` on 14 commits (`f6841d2`, `cd640b6`, `6399d63`, `32b3f9e`, `844f7c2`, `77ee522`, `f31f7a3`, `f8e54d8`, `546b2e3`, `98e7e01`, `13c6965`, `c7bdf64`, `c2aaa27`, `8f1fef8`). Git objects only.
5. 07:53:02–07:53:05 — read `data/h5/snapshots.jsonl` (3,719,818 B) line-by-line in a scratch script under `/home/kiros-li/.cache/program-audit/scratchpad/work/agentC-npl-locate/`, extracting only `snapshot_id` counts, then the 273 rows of snapshot `h5-census-2026-08-28T22:00:14Z` for their `basis_bp` and `touch_spread_bp` fields. **UNANCHORED**: this file's mtime is 2026-09-11 18:56, nine days after the anchor, and it may have changed after the anchored SHA.
6. 07:53:40 — the same file re-read once for the pooled recomputation in claim C1/C2/C7.
7. 07:56:52 — `git status --porcelain` (post-access).

No `.env`, `.keystore/`, `*.session`, credential, token or API-key file was read or listed. `.env.example` was seen in a directory listing and not opened.

Scratch work written only under `/home/kiros-li/.cache/program-audit/scratchpad/work/agentC-npl-locate/` (`peek.py`, `pool.py`, `hunt.py`).
