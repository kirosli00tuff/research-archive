# NPLExperiment — Agent C VERIFY

- Repository: `NPLExperiment`
- Anchored SHA: `8f1fef83be0f76cbd671c2ce0fbfe8b1c4a5ea2c` (main, 2026-09-02)
- Snapshot read: `/home/kiros-li/.cache/program-audit/scratchpad/snap/NPLExperiment/` (all tracked citations are SNAP paths, identical to `git show 8f1fef8:<path>`)
- Live repo touched read-only for: git objects (`log`, `show`, `rev-parse`, `cat-file`) and the gitignored `data/` tree. Everything read from `data/` is **UNANCHORED**; read times are given below.
- Recomputation scripts: `/home/kiros-li/.cache/program-audit/scratchpad/work/agentC-npl/` (`recompute_h1.py`, `c1_recompute.py`, `c1_2144.py`, `c1_snap2.py`, `c2_pool.py`, `h2.py`, `cull.py`, `ledger28.py`, `ledger28b.py`, `accrual2.py`, `hashes.py`, `rest.py`, `c3.py`, `c7_quant.py`)
- Python: `/home/kiros-li/.cache/program-audit/scratchpad/venv/bin/python` (numpy/scipy used only as an independent cross-check against the repository's own log-space formulas)
- Agent C has read nothing under `findings/agentA` or `findings/agentB`.

**Headline.** The H1 closure arithmetic, the H2 two-look design, the register cull, the H5 fired row, and every H5 spend figure reproduce **exactly** — most to machine precision — from the repository's own artifacts, code and request ledger. One block does not: the H5 **live/delisted stratum table** (`report.md:657-660`, `docs/H5_ACCESS.md:191-197`, `HYPOTHESES.md:129`, `DECISIONS.md:496-499`) and the live touch-spread figure (`report.md:643`) were computed from an **earlier census pass (`h5-census-2026-08-28T21:44:11Z`) that exists nowhere in git**, and its headline number — "**0.0 %**" of live instruments over the 54 bp VIABLE bar, "**Every observation above the bar lived in dead markets**" — is contradicted by the repository's own tracked census artifact (1 of 94), by the second forward pass (2 of 94), and by the **fired** `reports/h5/verdict.json`, which records `share_over_viable = 0.015957` (3 of 188) three lines away from the "0.0 %" cell in `HYPOTHESES.md`.

---

## 1. Claims table

`tol` = the tolerance at which agreement was judged. "exact" means agreement to the last stored digit (typically 1e-15 relative). Recomputations against the repository's own formulas were additionally cross-checked against `scipy.stats` where a closed form exists.

### 1a. MUST-VERIFY claims

| # | claim (short) | file:line | stated | source of truth used | recomputed | tol | status |
|---|---|---|---|---|---|---|---|
| C1a | live stratum median abs basis | `docs/H5_ACCESS.md:193`, `report.md:659` | **3.72 bp** (n = 94) | `reports/h5/census.rows.json` (tracked, snapshot `…21:51:54Z`), recomputed with `src/npl/h5/stats.py:17-42` | **4.2137 bp** | 0.01 bp | **CONTRADICTED** |
| C1b | live stratum share over the 54 bp VIABLE bar | `docs/H5_ACCESS.md:193`, `report.md:659`, `HYPOTHESES.md:129`, `DECISIONS.md:497-498` | **0.0 %** | `reports/h5/census.rows.json`; cross-check `reports/h5/verdict.json:inputs.by_session_tag.extended` | **1.064 %** (1/94, `xyz:URNM` at 55.641 bp); 2.128 % (2/94) in the 22:00:14Z pass; **1.596 %** (3/188) in the fired verdict | exact | **CONTRADICTED** |
| C1c | "Every observation above the 54 bp VIABLE bar lives in the delisted stratum" | `docs/H5_ACCESS.md:197-198`; `report.md:652`; `HYPOTHESES.md:129`; `DECISIONS.md:498-499` | universal | same | false on the tracked artifact (1 live observation over the bar) and on the fired verdict (3 of 188) | exact | **CONTRADICTED** |
| C1d | live stratum max | `docs/H5_ACCESS.md:193`, `report.md:659` | **51.4 bp** | `reports/h5/census.rows.json` | **55.641 bp** (51.408 is the *second* largest) | 0.1 bp | **CONTRADICTED** |
| C1e | live stratum share over the 18 bp floor | `docs/H5_ACCESS.md:193`, `report.md:659` | **8.5 %** (= 8/94) | `reports/h5/census.rows.json` | **7.447 %** (7/94) | exact | **CONTRADICTED** |
| C1f | live stratum IQR | `docs/H5_ACCESS.md:193`, `report.md:659` | **0.73 – 7.31** | `reports/h5/census.rows.json` + `h5/stats.py:quantile` (linear) | **0.7412 – 9.0865** | 0.01 bp | **CONTRADICTED** |
| C1g | delisted stratum row | `docs/H5_ACCESS.md:194`, `report.md:660` | 57 / 30.52 / 0.00–210.79 / 2,481 / 54.4 % / 45.6 % | `reports/h5/census.rows.json` | 57 / 30.5174 / 0.0000–210.7909 / 2,480.97 / 54.386 % / 45.614 % | 0.01 | **VERIFIED** |
| C1h | all-resolved stratum row | `docs/H5_ACCESS.md:195` | 151 / 4.14 / 0.00–18.13 / 2,481 / 25.8 % / 17.2 % | `reports/h5/census.rows.json` | **4.6310 / 0.0000–19.2452 / 25.17 % / 17.88 %** | 0.01 | **CONTRADICTED** |
| C1* | **where the printed table does reproduce** | — | — | untracked `data/h5/census.jsonl`, snapshot `h5-census-2026-08-28T21:44:11Z` (read 2026-09-12T12:36Z) | live n = 94, median **3.7227**, q1 **0.7294** / q3 **7.3111** (nearest-order-statistic), max **51.3919**, >18 bp **8/94 = 8.511 %**, >54 bp **0/94 = 0.000 %**; delisted and all-resolved rows likewise (all-resolved q3 18.1248 against the printed 18.13) | 0.01 | source identified — **not in git** |
| C2a | live instruments carrying a served reference | `report.md:673`, `HYPOTHESES.md:126`, `registrations/H5/REGISTRATION.md:567` | **94**, bar **20**, clears | `reports/h5/census.rows.json` (94 rows `resolved`+`live`, all `reference_served`, all `reference_field = oraclePx`); bar from `src/npl/config.py:248` | 94; bar 20 | exact | **VERIFIED** |
| C2b | funding served on those instruments | `report.md:674`, `registrations/H5/REGISTRATION.md:569` | **94 of 94, share 1.000**, bar 0.500 | `reports/h5/census.rows.json` (`funding_history_state = stored` on 94/94); bar `config.py:250` | 94/94 = 1.000; bar 0.5 | exact | **VERIFIED** |
| C2c | instruments at 30 days of coverage | `report.md:675` | **0**, bar 20 | `reports/h5/verdict.json:inputs.covered_days_max = 1`; `scripts/h5_fire.py:76` | 0 | exact | **VERIFIED** |
| C2d | median abs basis, `extended`, n = 188 | `report.md:676`, `HYPOTHESES.md:126`, `registrations/H5/REGISTRATION.md:573` | **4.14 bp**, IQR 0.71–9.15 | pooled `reports/h5/census.rows.json` (94 live) + `data/h5/snapshots.jsonl` snapshot `…22:00:14Z` (94 live), recomputed with `h5/stats.py:summarize` | median **4.14463090419424**, q1 **0.70947242299609**, q3 **9.145925118703394** | exact (0.0e+00) | **VERIFIED** |
| C2e | share over floor / bar at n = 188 | `registrations/H5/REGISTRATION.md:574`, `HYPOTHESES.md:126` | **9.57 % / 1.60 %** | same | 0.09574468085106383 (18/188) / 0.015957446808510637 (**3**/188) | exact | **VERIFIED** |
| C2f | floor / bar = 18.00 / 54.00 = 3 × 18 | `registrations/H5/REGISTRATION.md:576` | 18 / 54 | `src/npl/config.py:181,251`; `src/npl/h5/outcome.py:70-77` | `hip3_round_trip_bp[1]` = 18.0; × `h5_viable_basis_multiple` 3.0 = 54.0 | exact | **VERIFIED** |
| C3a | passes still needed | `HYPOTHESES.md:122`, `report.md:685`, `registrations/H5/REGISTRATION.md:587` | **29** | `src/npl/h5/outcome.py:200-217` (`max(0, h5_min_coverage_days − binding)`), `reports/h5/verdict.json:census_window.covered_days_binding_instrument = 1` | 30 − 1 = **29** | exact | **VERIFIED** |
| C3b | projected fire date | same | **2026-09-26** | `src/npl/h5/outcome.py:220-222` (`today + timedelta(days=passes_needed)`) | 2026-08-28 + 29 d = **2026-09-26** | exact | **VERIFIED** (arithmetic). The *assumption* — one covered day per calendar day — is falsified after the anchor: `data/h5/snapshots.jsonl` (read 2026-09-12T12:41Z) has 12 full passes in the 15 days 2026-08-29…2026-09-12 (**0.80/day**; 2026-09-05 and 2026-09-06 absent, 2026-09-03 only 4 rows). The authors recorded this themselves in post-anchor HEAD `dff1663` ("measured 0.77 passes/day"). |
| C4a | P1 197/312, exact lower bound at alpha_adj | `HYPOTHESES.md:52`, `report.md:222`, `REGISTRATION.md:556` | **0.5707** (stored 0.5706880326738533), bar 0.60, FAIL | `reports/stage_b/read.json`; `src/npl/verdict.py:67-82` re-implemented; independent closed form `scipy.stats.beta.ppf(alpha, s, n−s+1)` | bisection **0.5706880326738533**; closed form 0.5706880326738536 | 1e-15 | **VERIFIED** |
| C4b | P1 cost bands (198 / 197 / 194 of 312) | `REGISTRATION.md:566`, `report.md:230-231` | 0.5740 / 0.5707 / 0.5609 | same | 0.5739630116873008 / 0.5706880326738533 / 0.5608793225336948 | 1e-15 | **VERIFIED** |
| C4c | P2 111/312, exact sign test | `HYPOTHESES.md:52`, `report.md:223` | **p = 1.000** (stored 0.9999998937952859) | `reports/stage_b/read.json`; `src/npl/power.py:35-42` re-implemented; `scipy.stats.binom.sf` | 0.9999998937952859 (scipy 0.9999998937952682) | 1e-13 | **VERIFIED** |
| C4d | P3 114/175, exact sign test | `HYPOTHESES.md:52`, `report.md:224` | **p = 3.767e-05** (stored 3.766632285793312e-05) | same | 3.766632285793312e-05 (scipy 3.766632285793268e-05) | 1e-16 | **VERIFIED** |
| C4e | 90-day secondaries (P1 208, P2 159, P3 111) | `REGISTRATION.md:571`, `report.md:233,235` | 0.6069 / 0.3886 / 2.36e-04 | same | 0.6068655579748216 / 0.3885886631267041 / 0.00023604632892074097 | 1e-15 | **VERIFIED** |
| C5a | H2 minimum N (E1 42/84/76; E2@0.625 59/117/111; E2@0.600 92/184/169; 2× floor single-look 169) | `HYPOTHESES.md:73`, `registrations/H2/REGISTRATION.md:673-676` | as stated | `src/npl/register/sequential.py:124-152` + `power.py:69-83` re-implemented; cross-check `reports/stage_a_h2/ktable_amended.json:minimum_n` | 42/84/76, 59/117/111, 92/184/169, 169 — all exact | exact | **VERIFIED** |
| C5b | boundary k₁/k₂ at the three scenarios | `registrations/H2/REGISTRATION.md:695-697`, `report.md:546-548` | 22/37, **38/69**, 43/79 | `sequential.py:63-113` re-implemented | 22/37, 38/69, 43/79 | exact | **VERIFIED** |
| C5c | total alpha spends | same | 0.0373 / **0.0422** / 0.0403 | same | 0.037268 / 0.042197 / 0.040343 | 5e-5 | **VERIFIED** |
| C5d | printed **component** spends at look-1 min N | `registrations/H2/REGISTRATION.md:695` | "**0.0173 + 0.0200** = 0.0373" | `reports/stage_a_h2/ktable_amended.json:boundaries.at_look1_min_n` and `sequential.py:111-112` re-implemented | **0.008062 + 0.029206** = 0.037268 | 5e-5 | **CONTRADICTED** (total right, components wrong; 0.0173 and 0.0200 occur nowhere in the artifact) |
| C5e | printed **component** spends at the deadline | `registrations/H2/REGISTRATION.md:697` | "**0.0176 + 0.0227** = 0.0403" | same | **0.019230 + 0.021113** = 0.040343 | 5e-5 | **CONTRADICTED** (total right, components wrong) |
| C5f | two-look powers | `registrations/H2/REGISTRATION.md:695-697`, `report.md:546-548,565` | 0.7031/0.5529, 0.9322/0.8237, 0.9552/**0.8629** | `sequential.py:116-121` re-implemented | 0.703083/0.552854, 0.932234/0.823731, 0.955244/0.862922 | 5e-5 | **VERIFIED** |
| C5g | look-1 futility f₁ | `registrations/H2/REGISTRATION.md:714-715`, `report.md:555` | E1 **31**, E2 **27** at n₁ = 59 | `sequential.py:155-173` re-implemented at n₂ = 84 and 117 | 31 and 27 | exact | **VERIFIED** |
| C5h | projected look dates | `report.md:561-563`, `registrations/H2/REGISTRATION.md:723-730` | look 1 **2026-11-26**, look 2 **2027-03-01** | `reports/stage_a_h2/ktable_amended.json:projected_look_dates` + `projection_by_month`; projection re-derived from `scripts/ktable_amended.py:48-54` | forward pairs 18/37/54/73 at the four month-ends reproduce exactly from ACCRUAL 18.57, DAYS_PER_MONTH 30.44, 94-day lag; deadline total 62+73 = **135** | exact | **VERIFIED** *given* the accrual constant — see C11b |
| C6a | E2 true share 0.625 by linear interpolation | `HYPOTHESES.md:74`, `src/npl/config.py:212-217` | 0.625 | arithmetic: midpoint of 0.65 (multiple 0) and 0.60 (multiple 2) at multiple 1 | (0.65 + 0.60)/2 = **0.625** | exact | **VERIFIED** (and correctly labelled "a choice, not a measurement") |
| C6b | at the unchanged 0.60 E2 needs 92/184 and "does not reach 0.80 by the deadline" | `HYPOTHESES.md:74`, `registrations/H2/REGISTRATION.md:675,683-684` | 92/184; below 0.80 | `sequential.py` + `power.py` re-implemented at the projected deadline N = 135 | min N 92/184 exact; two-look power at n₂ = 135 = **0.692372**; single-look at N = 135 = **0.731814** — both < 0.80 | 5e-5 | **VERIFIED** |
| C6c | Section 0 gate recomputation | `reports/stage_a_h2/ktable_amended.json:section0_gate_recomputed`, `report.md:565` | single-look **0.8886**, two-look **0.8629** | `power.py:crit/upper_tail` re-implemented at N = 135, alpha_h = 0.05 | k* = 78; power@0.625 = **0.888596**, @0.600 = 0.731814; two-look 0.862922 | 5e-6 | **VERIFIED** |
| C7 | live median touch spread | `report.md:643`, `docs/H5_ACCESS.md` §"Is there a book?" | **4.18 bp** (IQR 1.31–10.78), n = 94 | `reports/h5/census.rows.json:touch_spread_bp` (94 present, all `resolved`+`live`) | **3.1586 bp**, IQR 1.2270–10.4125 | 0.01 bp | **CONTRADICTED** vs the tracked artifact. Reproduces exactly from the untracked `…21:44:11Z` pass (median **4.1838**; q1/q3 **1.3062 / 10.7832** under the nearest-order-statistic convention) |

### 1b. The rest

| # | claim (short) | file:line | stated | source of truth | recomputed | status |
|---|---|---|---|---|---|---|
| C8 | cull fixed point: pass 1 (k = 3) H2 0.5771 / H3 0.0000 / H4 0.0140; pass 2 (k = 1) H2 0.7604 | `report.md:362-365` | as stated | `reports/stage_a_h2/ktable_cull.json`; `src/npl/register/cull.py:62-144`, `power.py` re-implemented | 0.577117 / 0.000000 / 0.013958 / 0.760372 — all exact to 1e-6; alpha_h k=1/2/3 = 0.05 / 0.0253206 / 0.0169524 exact | **VERIFIED** |
| C9 | H3: main-dex accrual 0.5/month (n = 3/182 d), P1 min-N 262, deadline N = 5, ~0 power | `HYPOTHESES.md:89` | as stated | `data/census/census.jsonl` (read 2026-09-12T12:44Z, unanchored); `cull.py:72` spec (p0 = `p1_bar` 0.60, p_true 0.677) | 3 main-dex listings in the trailing 182 d → 3/182 × 30.4375 = **0.5017**/month; min N at alpha 0.05 = **262**; power at n = 5 = **0.0** | **VERIFIED** |
| C10 | H4 conditioning rates 0.177/0.129/0.081 (n = 62); best-cell deadline power 0.014 (0.711 at the declined 0.85) | `HYPOTHESES.md:106`, `report.md:354-357` | as stated | `ktable_cull.json:inputs`; `cull.py:82-93,109-124`; `conditioning.py:sidak_within` | 11/62 = 0.177419, 8/62 = 0.129032, 5/62 = 0.080645; alpha_cell = 1−(1−0.016952)^(1/3) = **0.005683**; power(30, 0.60, 0.631, 0.005683) = **0.013958**; at 0.85 = **0.710576** | **VERIFIED** |
| C10b | "median trailing entry funding +31.6 %/yr (min −132.4)" | `report.md:355-356`, `registrations/H4/REGISTRATION.md:211-221` | +31.6 %/yr | — | no artifact in `reports/` stores the per-event trailing funding series; recomputing it would require re-deriving 168-hour trailing means from `data/funding/` under the blindness gate | **UNVERIFIABLE** — figure not stored in any committed artifact |
| C11a | "n = 113 listings/182d" | `report.md:340-341` | 113 in 182 d | `data/census/census.jsonl` (unanchored, read 2026-09-12T12:44Z), `first_1d_open_ms` in [2026-08-27 − 182 d, 2026-08-27) | **113** | **VERIFIED** |
| C11b | "Accrual re-measured at **18.57 events/month**" | `report.md:340`; hard-coded `scripts/ktable_amended.py:49` | 18.57 | the claim's own stated inputs with the script's own `DAYS_PER_MONTH = 30.44` (`scripts/ktable_amended.py:50`) | 113/182 × 30.44 = **18.899**; at a 30-day month **18.626**. 18.57 corresponds to **n ≈ 111.0**, i.e. the 113 listings less the two the same paragraph excludes (`io:EWY` delisted at birth, the `xyz:XBI` relist) | **CONTRADICTED** (immaterial and conservative — see finding DRAFT-V-5) |
| C12a | backfill: 24 of 24, zero exclusions, 19 distinct controls, none skipped for coverage | `report.md:509-511` | as stated | `reports/stage_a_h2/backfill_fallback.json` | `assigned_n` 24, `distinct_controls` 19, `candidates_skipped_low_coverage` = 0 on all 24 rows | **VERIFIED** |
| C12b | "**174 candidates** considered per event" | `report.md:510` | 174, per event | `backfill_fallback.json:assigned[*].candidates_considered` | per-event values are **172 (×3), 173 (×12), 174 (×9)**; `candidate_universe_n` = **175** | **CONTRADICTED** (the printed figure is the maximum, not a per-event constant) |
| C12c | pairs ledger 62 rows = 38 `same_dex` + 24 `cross_dex` | `report.md:511-512` | 62 = 38 + 24 | `backfill_fallback.json:pairs_ledger_by_tag`; `data/controls/h2_pairs.jsonl` (unanchored, read 2026-09-12T12:45Z) | artifact 38 + 24 = 62 exact. The live file now holds **63** rows; the 63rd was appended 2026-09-02T02:01:32Z (a later `same_dex` main-dex pair), consistent with the anchor | **VERIFIED** |
| C13a | H8 decomposition (n = 312): funding +1.33 %, price +1.00 % | `report.md:240-241` | as stated | `reports/stage_b/read.json:secondaries.h8_decomposition_30d` | 0.013316691275 (1.3317 %), 0.009990294691442582 (0.9990 %) | **VERIFIED** |
| C13b | "the average short earned about **+2.2 % net**" | `report.md:241-242` | ≈ +2.2 % | `src/npl/outcome.py:22-27,30-37,47,60-62` (`net = price + funding − cost`), `config.py:180-181`, strata n from `read.json` | gross 1.3317 + 0.9990 = **2.3307 %**; registered central round trip is 18 bp on 154 `hip3` events and 9 bp on the other 158 → mean cost 13.442 bp = 0.1344 % → net **2.196 %** ≈ +2.2 % | **VERIFIED** |
| C13c | paired (n = 175): funding differential +0.88, price differential +6.43 | `report.md:242-244` | as stated | `read.json:secondaries.h8_paired_30d` | 0.008815909155428573 → +0.8816 pts; 0.06426309349214424 → +6.4263 pts | **VERIFIED** |
| C14a | 273 → 151 resolved (118 equity / 15 ETF / 18 index), 80 + 42 excluded, → 94 live, 57 delisted, 0 conflicting | `HYPOTHESES.md:127`, `report.md:649-655` | as stated | `reports/h5/census.json`, `reports/h5/census.rows.json` | 273; 151 (118/15/18); 80 + 42; 94; 57; all 57 carry `is_delisted` **and** `open_interest == 0` **and** `day_notional_volume == 0`; **0** of the 94 live carry any of the three | **VERIFIED** |
| C14b | "The live family is **two dexs**: `xyz` 73, `para` 16" | `HYPOTHESES.md:127` | two dexs | `reports/h5/census.json:by_dex_live` | **four** dexs: `xyz` 73, `para` 16, `mkts` 3, `io` 2 = 94. `docs/H5_ACCESS.md:152-155` states the same split **correctly** ("hold 89 of the 94 live instruments; `mkts` holds 3 and `io` 2") | **CONTRADICTED** |
| C15 | retrospective: 27 of 151 eligible, 124 quarantined, 39 observations, 2 instruments, 0 at the 30-day bar; `io:NBIS` n = 8 / 1 day, `xyz:XBI` n = 31 / 2 days | `report.md:691-695`, `HYPOTHESES.md:128` | as stated | `reports/h5/retro.json` | 27, 124, 39, 2 with any observation, 0 meeting coverage; per-instrument 8/1 and 31/2; per-instrument observation counts sum to **39** | **VERIFIED** |
| C16 | 32 of 57 delisted still served an unbroken hourly funding series, 168 rows each, latest 2026-08-28T21:00Z | `report.md:705-707`, `HYPOTHESES.md:129` | as stated | `reports/h5/census.rows.json` (`funding_history_rows`, `funding_last_time_ms`) | exactly **32** rows at 168 and 25 at 0; all 32 carry `funding_last_time_ms` = 1787950800058 = **2026-08-28T21:00:00Z** | **VERIFIED** |
| C17a | forward collector 209 requests = **1.05 %** of the daily cap | `report.md:686` | 209; 1.05 % | `data/ledgers/requests.jsonl` (unanchored, read 2026-09-12T12:38Z), charge positions 3627–3835 on 2026-08-28; `reports/h5/collector.json` (`ledger_day_before` 3626 → `after` 3835) | 209 charges (1 perpDexs + 10 meta + 10 metaAndAssetCtxs + 94 fundingHistory + 94 l2Book); 209/20 000 = **1.045 %** | **VERIFIED** |
| C17b | `census.json` forward plan 115 requests / share 0.00575 | `reports/h5/census.json` | 115; 0.00575 | the artifact's own arithmetic string: "1 perpDexs + 10 meta + 10 metaAndAssetCtxs + 94 l2Book (+94 fundingHistory service probes)" | 1+10+10+94 = **115**; 115/20 000 = **0.00575**. The +94 probes make the measured pass 209 | **VERIFIED** (plan-excluding-probes vs measured; disclosed inside the artifact) |
| C18 | H5 total spend **888** = 6 + 323 + 323 + 27 + 209; 4.44 % of cap; day total **3,847** (19.2 %) | `progress.md:1502-1516` | as stated | `data/ledgers/requests.jsonl`, 2026-08-28 `kind = charge` rows, ordered by `ts` | recon 6 (21:39:45–48Z, positions 2948–2953); census pass 1 **323** (21:44:11Z, 2954–3276); census pass 2 **323** (21:51:54Z, 3277–3599); retrospective **27** fundingHistory (21:56:05–40Z, 3600–3626); forward **209** (22:00:14Z, 3627–3835). Sum 2948→3835 = **888**. 888/20 000 = **4.44 %**. Charges on 2026-08-28 up to 22:10:08Z = **3,847**; 3847/20 000 = **19.235 %** | **VERIFIED** |
| C19 | "Two full census passes, 323 requests each, plus a 6-request reconnaissance probe" | `report.md:635-636` | 323 + 323 + 6 | same ledger | exact: both passes are 1 + 10 + 10 + 151 + 151 = 323 | **VERIFIED** (the two passes are `…21:44:11Z` and `…21:51:54Z`; only the second is in git) |
| C20 | served premium −0.0003482613 = (77501.0 − 77528.0)/77528.0 | `report.md:645` | identity | one-line arithmetic | −0.0003482612733464039 | **VERIFIED** |
| C21a | effective N 312 / 312 / 175 against registered minimums 34 / 103 / 60 | `report.md:146-147` | as stated | `reports/stage_b/read.json:preconditions` | `effective_n_p1/p2/p3` = 312/312/175; `min_n` = [34, 103, 60]; `shortfalls` = [] | **VERIFIED** |
| C21b | "224,633 funding rows summed inside the 30-day windows" | `report.md:216` | 224,633 | `reports/stage_b/read.json:funding_rows_30_total` | the artifact records exactly 224633 | **VERIFIED as recorded**; not re-derived from the 462 archive directories in `data/funding/` (see §6) |
| C22a | "The census refresh found 504 instruments"; `reports/h5/preconditions.json` counts 505 census rows | `report.md:338-339`; `reports/h5/preconditions.json` | 504 / 505 | `data/census/census.jsonl` (unanchored) | 505 ledger rows, **504 distinct (dex, coin)** — `xyz:XBI` appears twice (the relist the same sentence names). Both figures are right | **VERIFIED** (no inconsistency) |
| C22b | "156 pages, 60,010 funding hours, 0 unrecoverable hours" | `report.md:336-337` | as stated | — | no committed artifact records page or hour totals for the A.1 rebuild | **UNVERIFIABLE** — no stored primitive |
| C23 | gate figures: 249 / 217 / 172 / 159 tests passed; `mypy --strict` on 71 / 67 files | `report.md:581-582,292,148`; `reports/h5/preconditions.json`, `reports/stage_a_h2/amend_preconditions.json` | as stated | artifacts record the strings `"pytest": "249 passed"`, `"mypy_strict": "71 source files, no issues"` etc. | not reproducible by reading; a test run is forbidden inside an audited tree and the repo's own venv cannot be built read-only | **UNVERIFIABLE** — stated reason: execution is forbidden by the audit rules |
| C24 | latch/artifact hashes: `reports/stage_b/read.json` sha256 `4455489675c…be840c` | `HYPOTHESES.md:54` | as stated | sha256 of the SNAP file | `4455489675c3774f05c977cb7edb9d8b26928f851400077b31263f5826be840c` — **identical** | **VERIFIED** |
| C25 | "The B.1 re-hash (21 modules): exactly one diff against B.0 … every other read-surface module is byte-identical" | `report.md:200-206` | one diff | `reports/stage_b/hashes_b0.json` vs `hashes_b1.json` | B.0 = 19 modules, B.1 = 21; added `stageb/cli.py`, `stageb/reader.py`; **changed: `stageb/__init__.py` only**; 18 unchanged | **VERIFIED** |
| C26 | the 21 module hashes inside `read.json` pin the read surface | `HYPOTHESES.md:54`, `report.md:210-211` | 21 hashes | `git show 32b3f9e:src/npl/<module>` piped to sha256 (live repo, read-only) | **all 21 match the git objects at `32b3f9e`** (the read-time commit, 2026-08-27T20:00:42-07:00 = 2026-08-28T03:00:42Z, 26 s before `read_at`). Five (`power`, `config`, `coverage`, `blindness`, `paths`) differ from the **anchor** tree, as expected from later H5 work | **VERIFIED** |
| C27 | "the preconditions … PASS at **07:51:10Z** on the project clock" | `report.md:446` | 07:51:10Z | `reports/stage_a_h2/amend_preconditions.json:checked_at` | **06:51:10Z**. The amendment commit `f31f7a3` is 2026-08-28T07:01:06Z, so the artifact's time precedes the commit by 10 min while the printed time would follow it by 50 min, inverting the ordering the same paragraph asserts | **CONTRADICTED** |
| C28 | H5 row "fired 2026-08-28T**22:20Z**" | `HYPOTHESES.md:122`, `report.md:667`, `registrations/H5/REGISTRATION.md:555` | 22:20Z | `reports/h5/verdict.json:fired_at` | **22:04:30Z** | **CONTRADICTED**, but **disclosed by the authors** at `registrations/H5/REGISTRATION.md:632-639` ("That figure was typed by the assistant as an estimate … The map actually fired at 2026-08-28T22:04:30Z"). Two of the three sites were not corrected at the anchor |

---

## 2. Derived quantities table

Every figure below was recomputed from stored primitives (counts, sums, per-unit rows, registered constants) and compared with what the documents print.

| derived quantity | stated | primitives used | recomputed | status |
|---|---|---|---|---|
| `alpha_adj` = 1 − 0.95^(1/3) | 0.016952 (0.0170) | `src/npl/config.py:19` | **0.016952427508441503** (matches `read.json:alpha_adj`) | VERIFIED |
| `alpha_h` = 1 − 0.95^(1/k) at k = 1, 2, 3 | 0.05 / — / 0.016952 | `register/cull.py:42-46` | 0.05 / 0.025320565519103666 / 0.016952427508441503 — all three match `ktable_cull.json` | VERIFIED |
| H4 within-hypothesis Šidák `alpha_cell` = 1 − (1 − alpha_h)^(1/3) | 0.00568 | `register/conditioning.py:sidak_within`, `registrations/H4/REGISTRATION.md:79-80` | 0.005683 at alpha_h 0.016952; 0.016952 at alpha_h 0.05 — both match `ktable_cull.json:alpha_effective` | VERIFIED |
| P1 point share 197/312 | 63.14 % | `read.json:co_primaries.p1` | 0.6314102564102564 (= `secondaries.forward_vs_retro_30d.retro.share_positive`) | VERIFIED |
| P2 point share 111/312 | 35.58 % | same | 0.3557692307692308 | VERIFIED |
| P3 point share 114/175 | 65.14 % | same | 0.6514285714285715 | VERIFIED |
| 90-day share positive 208/312 | 66.7 % | `read.json:secondaries.horizon_90d` | 0.6666666666666666 | VERIFIED |
| per-type strata shares (vanilla 0.670 n 112; hyperp 0.696 n 46; hip3 0.584 n 154) | as stated | `read.json:secondaries.per_type_strata_30d` | 0.6696428571428571 / 0.6956521739130435 / 0.5844155844155844; n sum 112+46+154 = **312** | VERIFIED |
| mean registered round-trip cost across the 312 events | implied by "+2.2 % net" | `config.py:180-181`, strata n | (154 × 18 + 158 × 9)/312 = **13.442 bp**; 2.3307 % − 0.1344 % = **2.196 %** | VERIFIED |
| H4 conditioning rates from counts | 0.1774 / 0.1290 / 0.0806 | `ktable_cull.json:inputs.achieved.cells` (11, 8, 5 of 62) | 0.177419 / 0.129032 / 0.080645 | VERIFIED |
| H3 main-dex accrual from counts | 0.5/month (n = 3/182 d) | `data/census/census.jsonl` | 3/182 × 30.4375 = **0.5017** | VERIFIED |
| total accrual from counts | **18.57**/month (n = 113/182 d) | same + `scripts/ktable_amended.py:50` (`DAYS_PER_MONTH = 30.44`) | **18.899** (30.44-day month) / 18.626 (30-day month) | **CONTRADICTED** |
| H2 pair projection (forward pairs readable by month) | 18 / 37 / 54 / 73; totals 80 / 99 / 116 / **135** | ACCRUAL 18.57, DAYS_PER_MONTH 30.44, 94-day forward lag, backfill 62 | floor(18.57 × d/30.44) for d = 31, 62, 90, 121 = 18, 37, 54, 73; totals 80, 99, 116, 135 | VERIFIED (given the constant) |
| effect of the accrual error on the look dates | — | re-running the projection at 18.899 | deadline total becomes **137** (not 135) and look 2 moves ~2 days **earlier** (2027-02-27); look 1 is reached from the 62 backfill pairs and does not move | conservative — the stated dates are later, not earlier |
| VIABLE bar = 3 × 18 bp | 54 bp | `config.py:181,251`; `h5/outcome.py:70-77` | 54.0 | VERIFIED |
| passes needed = `h5_min_coverage_days` − binding coverage | 29 | `h5/outcome.py:200-217` | 30 − 1 = 29 | VERIFIED |
| projected fire date = today + passes | 2026-09-26 | `h5/outcome.py:220-222` | 2026-08-28 + 29 d = 2026-09-26 | VERIFIED |
| realized census passes per day, post-anchor | (assumed 1.0) | `data/h5/snapshots.jsonl`, read 2026-09-12T12:41Z, **UNANCHORED** | 12 full passes in 15 days = **0.80**/day (2026-09-05, 2026-09-06 missing; 2026-09-03 = 4 rows) | assumption falsified post-anchor, self-corrected by the authors in `dff1663` |
| H5 spend shares | 4.44 % / 1.05 % / 19.2 % / 0.00575 | request ledger + `config.py:159` (cap 20 000) | 888/20000 = 4.440 %; 209/20000 = 1.045 %; 3847/20000 = 19.235 %; 115/20000 = 0.00575 | VERIFIED |
| H5 live share over the 54 bp bar, pooled n = 188 | (printed as 1.60 % at `HYPOTHESES.md:126`; as **0.0 %** at `HYPOTHESES.md:129`) | tracked `census.rows.json` + untracked `…22:00:14Z` snapshot | **3/188 = 1.5957 %** — identical to `verdict.json:share_over_viable` | the two cells of the same table disagree — see DRAFT-V-1 |
| all-resolved median abs basis **including** the delisted stratum, at the fired snapshots | implied by "the amendment deleted this entry's only route to VIABLE" (`report.md:663`, `DECISIONS.md:511`) | `census.rows.json`; `data/h5/census.jsonl`; `data/h5/snapshots.jsonl` | 4.1402 bp (21:44:11Z) / **4.6310 bp** (21:51:54Z) / 5.0726 bp (22:00:14Z); the delisted stratum alone has median 30.52 bp. `h5/outcome.py:165-185` fires VIABLE only when a tag **median** exceeds 54 bp, so no contemporaneous reading of the pre-amendment universe was within an order of magnitude of VIABLE | **UNVERIFIABLE** — the claim is a counterfactual about a future 30-day census (delisted marks freeze while oracles move, so their basis widens); recorded here with the numbers rather than adjudicated |

---

## 3. Intervals table

No two-sided confidence interval appears anywhere in this repository. Every "interval" is either a **one-sided exact (Clopper–Pearson) lower confidence bound** or an **IQR**, which is a dispersion summary and not an interval estimate. There is no asymptotic statistic, no bootstrap, no regression and no variance estimator in `src/npl`.

| # | interval | file:line | estimator actually used (from code) | independence assumed | data structure — is that doubtful? | reproduces? | status |
|---|---|---|---|---|---|---|---|
| I1 | P1 lower bound 0.5707 (197/312) at alpha_adj, bar 0.60 | `REGISTRATION.md:556`, `HYPOTHESES.md:52`, `report.md:222` | Exact Clopper–Pearson one-sided lower bound by 200-step bisection on `P(X ≥ s \| p)`, `src/npl/verdict.py:67-82` | **Yes** — one Bernoulli per event, i.i.d. assumed | 312 listing events on one venue over ~18 months, one draw per instrument-event. Events are **not** repeated within instrument (each coin contributes one 30-day window), but they share calendar time: a market-wide regime in the 30-day windows would induce cross-sectional dependence. No clustering by dex or by month is applied. The registration does not claim independence explicitly; the estimator assumes it | **Yes, exactly** — bisection 0.5706880326738533 = stored; closed form `beta.ppf(alpha, 197, 116)` = 0.5706880326738536 | **VERIFIED** (estimator correctly identified and reproduced) |
| I2 | P1 cost-band bounds 0.5740 / 0.5707 / 0.5609 (198/197/194 of 312) | `REGISTRATION.md:566`, `report.md:230-231` | same | Yes | same; the three bands are three deterministic re-scorings of the **same** 312 events, so the three bounds are perfectly dependent and are correctly presented as a sensitivity, not as three tests | Yes, exactly (all three to 1e-15) | **VERIFIED** |
| I3 | P1 at 90 days 0.6069 (208/312), descriptive only | `REGISTRATION.md:571`, `report.md:233` | same | Yes | the 90-day window nests the 30-day window on the same 312 events — heavily dependent on I1 and correctly labelled a **named secondary, never verdict-bearing** (`REGISTRATION.md:223-226`; `verdict.py:150-189`) | Yes, exactly | **VERIFIED** |
| I4 | the registered levels themselves: alpha_adj = 1 − 0.95^(1/3) = 0.016952; alpha_h = 1 − 0.95^(1/k) | `REGISTRATION.md:200-201`; `register/cull.py:42-46` | Šidák | n/a | n/a | Yes, exactly | **VERIFIED** as arithmetic; see the Tests table, T0, for whether the correction matches the rule it feeds |
| I5 | every IQR printed in H5 (live 0.73–7.31; delisted 0.00–210.79; all-resolved 0.00–18.13; n = 188 0.71–9.15; retro pooled; touch spread 1.31–10.78) | `docs/H5_ACCESS.md:193-195`, `report.md:659-660,643`, `registrations/H5/REGISTRATION.md:573,601` | `src/npl/h5/stats.py:29-42` — linear-interpolated quantiles ("the numpy default, written out") | n/a — a dispersion summary, **not** an interval estimate, and correctly never used as one | the n = 188 sample is **94 instruments × 2 snapshots taken 8 minutes apart**, so it is 94 units repeated twice, not 188 independent draws. The repository discloses this (`registrations/H5/REGISTRATION.md:572` "**188** (94 instruments × 2)") and, critically, computes **no test statistic, no p-value and no confidence interval** on it — so the repeated-measure structure feeds no inference | n = 188 row: **yes, exactly**. The H5 stratum IQRs at `docs/H5_ACCESS.md:193,195`: **no** — see DRAFT-V-1/DRAFT-V-2; they also use a **nearest-order-statistic** convention rather than the repository's own linear-interpolated `h5/stats.py:quantile` | mixed — see findings |

---

## 4. Tests table

| # | test | file:line | estimator | tail — one- vs two-sided against the registered direction | dof / exact distribution | multiplicity correction applied | decision rule it feeds | correction matches rule? | reproduces? | status |
|---|---|---|---|---|---|---|---|---|---|---|
| T0 | the H1 family as a whole | `REGISTRATION.md:200-202`; `src/npl/verdict.py:192-203` | three exact binomial tests, each at alpha_adj | — | exact | **Šidák, 1 − 0.95^(1/3) = 0.016952, applied per co-primary** | `all_co_primaries_pass = p1 and p2 and p3` (`verdict.py:201`) — an **all-must-pass conjunction** (intersection-union) | **NO.** A union-type correction on an all-must-pass rule is a mismatch: an IUT controls the type-I error of the conjunction at the maximum per-component level, so no correction is needed. The same program applies the correct reasoning to H2/H3 in `register/cull.py:18-20,135-144` ("every co-primary … the weakest governs", no within-hypothesis split) | the applied arithmetic reproduces exactly | **CONTRADICTED** as a correction/rule pairing — see DRAFT-V-4. Recomputation: at an uncorrected alpha = 0.05 the P1 bound rises 0.5707 → **0.5841**, still under the 0.60 bar, and P2's p stays 1.000, so **the H1 FAIL does not move** |
| T1 | P2 magnitude, 111/312 | `REGISTRATION.md:208-212`, `report.md:223` | exact one-sided sign test, p₀ = 0.5, success = `net_short(30) ≥ +0.15` (`verdict.py:110-121`) | **one-sided, greater** — matches the registered direction ("that share **exceeds** one half") | exact binomial, n = 312, no dof | alpha_adj 0.016952 (see T0) | component of the conjunction | see T0 | `upper_tail(312, 111, 0.5)` = **0.9999998937952859** = stored; scipy sf 0.9999998937952682 | **VERIFIED** |
| T2 | P3 listing-age contrast, 114/175 | `REGISTRATION.md:213-222`, `report.md:224` | exact one-sided sign test on paired indicators, p₀ = 0.5, success = young `net_short` > control's (`verdict.py:124-141`) | **one-sided, greater** — the registration states the direction twice, in both sign conventions, "so no sign error can creep in" | exact binomial, n = 175 pairs | alpha_adj | component of the conjunction | see T0 | `upper_tail(175, 114, 0.5)` = **3.766632285793312e-05** = stored | **VERIFIED** |
| T3 | P2 at 90 days, 159/312 | `REGISTRATION.md:571`, `report.md:235` | same as T1 | one-sided, greater | exact, n = 312 | descriptive secondary — none needed | none (never verdict-bearing) | n/a | 0.3885886631267041 = stored | **VERIFIED** |
| T4 | P3 at 90 days, 111/175 | same | same as T2 | one-sided, greater | exact, n = 175 | descriptive secondary | none | n/a | 0.00023604632892074097 = stored | **VERIFIED** |
| T5 | H2 two-look exact binomial boundary | `registrations/H2/REGISTRATION.md:691-701`, `report.md:546-548` | k₁ = min{k : P(Bin(n₁,½) ≥ k) ≤ alpha₁}; k₂ = min{k : Σ_{s<k₁} P(Bin(n₁,½)=s)·P(Bin(n₂−n₁,½) ≥ k−s) ≤ alpha₂} (`sequential.py:63-113`) | one-sided, greater | exact binomial; the look-2 spend is exact over the **independent increment** Bin(n₂−n₁, ½), not an asymptotic spending function | alpha split 0.02 + 0.03 = alpha_h = 0.05 — an **alpha-spending split across looks**, which is the correct device for a sequential rule; **no** Šidák across E1 and E2 | E1 **and** E2 both required (`cull.py:39` `"H2": "all"`) — an IUT, so no cross-co-primary correction is needed | **YES** — the split is across looks, not across co-primaries, and none is applied across E1/E2 | k₁/k₂ = 22/37, 38/69, 43/79 and totals 0.037268 / 0.042197 / 0.040343 all reproduce exactly; **two of the three printed component pairs do not** (see C5d/C5e) | **VERIFIED** on boundaries, totals and powers; **CONTRADICTED** on the printed components |
| T6 | H2 look-1 futility boundary | `registrations/H2/REGISTRATION.md:712-718` | f₁ = largest s with `P(Bin(n₂−n₁, p_true) ≥ k₂−s) < 0.10` (`sequential.py:155-173`) | one-sided conditional power, same direction | exact binomial | none (a futility rule spends no alpha) | stop-for-futility, single | n/a — correctly no correction | E1 f₁ = **31** (n₁ 59, n₂ 84), E2 f₁ = **27** (n₁ 59, n₂ 117) | **VERIFIED** |
| T7 | H2 power figures | `report.md:565`, `registrations/H2/REGISTRATION.md:695-697` | exact binomial power, `power.py:69-72` and `sequential.py:116-121` | one-sided | exact | alpha_h = 0.05 | Section 0 DEGRADED/GO map | n/a | single-look **0.888596**, two-look **0.862922**, E1 0.955244, E2@0.60 0.731814 — all exact | **VERIFIED** |
| T8 | alpha-split materiality screen (6 candidates) | `registrations/H2/REGISTRATION.md:654-661` | two-clause screen: power gain ≥ 0.01 **and** interim stop-loss ≤ 0.05, evaluated at n₂ = 135 | n/a | n/a | n/a — a design screen, not an inference | conjunction of two clauses; decision "no candidate passes both" | n/a | the printed row for 0.01/0.04 (power 0.8900, +0.0270; P(interim) 0.3112, −0.1930) matches `ktable_amended.json:alpha_split_evaluation` exactly; all six rows match | **VERIFIED** |
| T9 | H4 within-hypothesis Šidák | `registrations/H4/REGISTRATION.md:79-80,207`; `register/conditioning.py` | alpha_cell = 1 − (1 − alpha_h)^(1/3) | one-sided, greater (p₀ = `p1_bar` 0.60) | exact binomial per cell | **Šidák across 3 threshold cells** | `"H4": "any"` — the **best cell** governs (`cull.py:39,142-143`), a **union** rule | **YES** — a union rule is exactly what a Šidák correction is for | 0.005683 at alpha_h 0.016952 and 0.016952 at alpha_h 0.05, matching every `alpha_effective` in `ktable_cull.json` | **VERIFIED** |
| T10 | the cull's power screen to its fixed point | `report.md:362-365`; `register/cull.py` | exact binomial power vs the 0.50 BLOCKED floor at the achievable N by the deadline | one-sided | exact | alpha_h = 1 − 0.95^(1/k) across the **k surviving hypotheses**, recomputed at each pass | "any hypothesis may fire its own row" — a **union** across hypotheses | **YES** | pass 1 (k = 3): H2 0.577117, H3 0.000000, H4 best cell 0.013958; pass 2 (k = 1): H2 0.760372 — all exact. (H2's E2 figures use the pre-Amendment-H2-3 share 0.60, correct for a cull run at 05:41:32Z, before the 07:01:06Z amendment) | **VERIFIED** |
| T11 | H5 primary summary, n = 188 | `report.md:676`, `registrations/H5/REGISTRATION.md:573-574` | median, linear-interpolated quartiles, exceedance shares (`h5/stats.py:64-88`). **No test statistic and no p-value is computed anywhere in H5** | n/a | n/a | none | the Section 6 map is a **threshold map on the median**, not a test (`h5/outcome.py:89-193`); a single deterministic comparison | n/a — correctly none, and correctly no inference drawn from a repeated-measures sample | median 4.14463090419424, q1 0.70947242299609, q3 9.145925118703394, shares 0.09574468085106383 / 0.015957446808510637 — **all exact** | **VERIFIED** |
| T12 | H5 stratum summaries (live / delisted / all-resolved) | `docs/H5_ACCESS.md:193-195`, `report.md:659-660` | same summarizer, but the **printed quartiles use a nearest-order-statistic convention**, not `h5/stats.py`'s linear interpolation | n/a | n/a | none | descriptive; feeds the Amendment H5-2 rationale | n/a | **delisted row exact**; **live and all-resolved rows do not reproduce from the tracked artifact**, only from the untracked `…21:44:11Z` pass | **CONTRADICTED** — DRAFT-V-1, DRAFT-V-2 |
| T13 | H5 retrospective pooled summaries | `registrations/H5/REGISTRATION.md:601`, `reports/h5/retro.json` | same summarizer | n/a | n/a | none | reported as a shortfall, fires nothing | n/a | regular median 14.169534 (n 17), extended 14.120973 (n 14), closed_weekday 20.599501 (n 8); 17+14+8 = **39** = `observations_served`; per-instrument counts sum to 39 | **VERIFIED**. Note the 39 observations come from **2 instruments**, so the "n" of each pooled tag is repeated hourly measurements of one or two names — the registration says so and fires nothing on them |
| T14 | H5 touch-spread summary | `report.md:643` | same summarizer, nearest-order-statistic quartiles | n/a | n/a | none | descriptive | n/a | does not reproduce from the tracked artifact (3.1586 / 1.2270–10.4125); reproduces from the untracked `…21:44:11Z` pass | **CONTRADICTED** — DRAFT-V-2 |

---

## 5. Draft findings

### DRAFT-V-1
- **Repository / SHA:** NPLExperiment / `8f1fef83be0f76cbd671c2ce0fbfe8b1c4a5ea2c`
- **Hypothesis or artifact:** H5, the HIP-3 equity-style basis feasibility entry — the live/delisted stratum table and the Amendment H5-2 rationale it carries
- **Direction:** A
- **Class:** INTERNAL_INCONSISTENCY
- **Severity:** S1
- **Label:** DERIVED
- **Claim challenged (verbatim quote):** "**Every observation above the 54 bp VIABLE bar lives in the delisted stratum.**" — NPLExperiment/docs/H5_ACCESS.md:197-198; and "| **live** | **94** | **3.72 bp** | 0.73 – 7.31 | 51.4 bp | 8.5 % | **0.0 %** |" — NPLExperiment/docs/H5_ACCESS.md:193 and NPLExperiment/report.md:659; and "the delisted stratum is where **every** observation above the 54 bp bar lived: median 30.5 bp with 45.6 % over the bar, against 3.72 bp and **0.0 %** for live instruments in the same snapshot" — NPLExperiment/HYPOTHESES.md:129; and "**Every observation above the bar lived in dead markets.**" — NPLExperiment/DECISIONS.md:498-499
- **Evidence:**
  - The repository's only tracked per-instrument basis artifact, `reports/h5/census.rows.json` (273 rows, all stamped `snapshot_id = h5-census-2026-08-28T21:51:54Z`), gives for the 94 `resolved` + `live` instruments: median **4.2137 bp**, q1/q3 **0.7412 / 9.0865**, max **55.641 bp**, **7/94 = 7.447 %** over 18 bp, and **1/94 = 1.064 %** over 54 bp. The observation over the bar is `xyz:URNM` at **−55.641 bp**, `listing_status = live`, `is_delisted = false`. — NPLExperiment/reports/h5/census.rows.json (SNAP, anchored)
  - The repository's **fired** artifact records the same thing on the post-Amendment-H5-2 live universe: `inputs.by_session_tag.extended.share_over_viable` = **0.015957446808510637** = 3 of 188. — NPLExperiment/reports/h5/verdict.json
  - `HYPOTHESES.md:126` prints that same figure — "**1.60 %** over the 54 bp bar" (n = 188) — **three lines above** the "0.0 %" cell at `HYPOTHESES.md:129`. `registrations/H5/REGISTRATION.md:574` likewise prints "9.57 % / **1.60 %**".
  - The second census pass in the working tree (`data/h5/snapshots.jsonl`, snapshot `h5-census-2026-08-28T22:00:14Z`, read 2026-09-12T12:36Z, UNANCHORED) gives live median 4.1404 bp, max **63.29 bp**, **2/94 = 2.128 %** over the bar.
  - The printed table **does** reproduce, to the last printed digit, from a **third** census pass that is in no git object: `h5-census-2026-08-28T21:44:11Z`, present only in the gitignored `data/h5/census.jsonl` (read 2026-09-12T12:36Z). That pass gives live n = 94, median **3.7227**, max **51.3919**, **8/94 = 8.511 %** over 18 bp, **0/94 = 0.000 %** over 54 bp. The request ledger confirms it was a full 323-request census pass (charge positions 2954–3276 on 2026-08-28, 21:44:11–21:47:56Z), 8 minutes before the pass the tracked artifact records.
  - The delisted row of the same table (57 / 30.5174 / 0.0000–210.7909 / 2 480.97 / 54.386 % / 45.614 %) reproduces **exactly** from both passes — dead markets' marks are frozen, so their basis does not move between passes. Only the live row moves, and it moves across the bar.
- **Recomputation:** inputs `reports/h5/census.rows.json` (273 rows) and `reports/h5/verdict.json:inputs`; method — the repository's own `src/npl/h5/stats.py:64-88` `summarize` re-implemented verbatim (median, linear-interpolated quartiles, `sum(m > bar)/n`) over `abs(basis_bp)` for the stratum `resolution_state == "resolved" AND listing_status == "live"`; script `/home/kiros-li/.cache/program-audit/scratchpad/work/agentC-npl/c1_recompute.py`. Result: n = 94, median 4.2137, share_over_viable **0.010638**, max 55.6406. Tolerance: exact (integer counts). Pooled with the second snapshot the shares reproduce `verdict.json` to 0.0e+00.
- **What would resolve it:** committing the `h5-census-2026-08-28T21:44:11Z` rows and stating in `docs/H5_ACCESS.md` and `report.md` which pass each stratum figure is computed from; and replacing the universal "every observation above the bar lives in the delisted stratum" with a snapshot-scoped statement, or re-deriving the table from the census artifact of record, in which case the live cell reads 1.06 % (or 1.60 % pooled), not 0.0 %.
- **Confidence:** HIGH — the contradicting figure is in the repository's own fired artifact and is printed three lines away in the same document table.
- **Invalidated by later commits?:** no — the tracked artifact and both document tables are unchanged from the anchor to live HEAD `dff1663`; nothing in the four post-anchor commits touches the stratum table.
- **Disclosed by authors?:** no. `report.md:635-636` asserts the two census passes returned "**identical** counts" — which is true of counts — and presents the stratum table immediately afterwards without saying which pass produced it; no document names the `21:44:11Z` pass at all.

### DRAFT-V-2
- **Repository / SHA:** NPLExperiment / `8f1fef83be0f76cbd671c2ce0fbfe8b1c4a5ea2c`
- **Hypothesis or artifact:** H5 — the "What the venue actually serves" block and the stratum table: every descriptive figure is computed from a census pass that is not in git, while the committed census artifact is a different pass
- **Direction:** neutral
- **Class:** PROVENANCE
- **Severity:** S3
- **Label:** DERIVED
- **Claim challenged (verbatim quote):** "Two full census passes, 323 requests each, returning **identical** counts, plus a 6-request reconnaissance probe. `docs/H5_ACCESS.md` carries the verbatim fragments." — NPLExperiment/report.md:635-637; and "| Is there a book? | Two-sided on 94 of 94 live; empty on all 57 delisted. Live median touch spread **4.18 bp** (IQR 1.31–10.78). |" — NPLExperiment/report.md:643
- **Evidence:**
  - The tracked census artifacts name exactly one pass: `reports/h5/census.json:snapshot_id` = `h5-census-2026-08-28T21:51:54Z`, and all 273 rows of `reports/h5/census.rows.json` carry that same id. The `21:44:11Z` pass has no tracked artifact.
  - Touch spread from the tracked artifact (94 present values, all on `resolved`+`live` rows): median **3.1586 bp**, IQR **1.2270 – 10.4125**. From the untracked `21:44:11Z` pass: median **4.1838**, and under the nearest-order-statistic convention q1/q3 = **1.3062 / 10.7832** — i.e. exactly the printed "4.18 bp (IQR 1.31–10.78)".
  - Same for the all-resolved stratum row `docs/H5_ACCESS.md:195` ("151 | 4.14 bp | 0.00 – 18.13 | 2,481 | 25.8 % | 17.2 %"): tracked artifact gives 4.6310 / 0.0000–19.2452 / 25.17 % / 17.88 %; the `21:44:11Z` pass gives 4.1402 / 0.0000–18.10 / **25.828 %** / **17.219 %**.
  - The printed quartiles also use a different quantile convention from the repository's own `src/npl/h5/stats.py:29-42`, which is documented as "linear-interpolated … the numpy default, written out". The printed 0.73 / 7.31 / 10.78 / 18.13 are nearest-order-statistic values; the linear values are 0.7576 / 7.3007 / 10.5706 / 18.0993.
  - `docs/H5_ACCESS.md` was added in commit `13c6965` at 2026-08-28T21:59:42Z — after both census passes and before the forward pass — so the pass it summarizes was a deliberate choice, not a timing accident.
- **Recomputation:** inputs `data/h5/census.jsonl` (546 lines; two snapshot ids, read 2026-09-12T12:36Z, UNANCHORED) and `reports/h5/census.rows.json`; method — `h5/stats.py`'s summarizer plus all 13 `numpy.quantile` methods; script `/home/kiros-li/.cache/program-audit/scratchpad/work/agentC-npl/c1_2144.py` and `c7_quant.py`. Result as above. Tolerance 0.01 bp.
- **What would resolve it:** commit the `21:44:11Z` rows (or re-derive the block from `census.rows.json`), and state the quantile convention used in the documents so it matches `h5/stats.py`.
- **Confidence:** HIGH — the source pass is identified positively and every printed figure of the block matches it to the last digit.
- **Invalidated by later commits?:** no — unchanged through live HEAD `dff1663`.
- **Disclosed by authors?:** no.

### DRAFT-V-3
- **Repository / SHA:** NPLExperiment / `8f1fef83be0f76cbd671c2ce0fbfe8b1c4a5ea2c`
- **Hypothesis or artifact:** H2 — Amendment H2-4 boundary table, `registrations/H2/REGISTRATION.md` §3
- **Direction:** neutral
- **Class:** INTERNAL_INCONSISTENCY
- **Severity:** S4
- **Label:** DERIVED
- **Claim challenged (verbatim quote):** "| at look-1 min N | 59 | 30 | 22 | 37 | 0.0173 + 0.0200 = 0.0373 | 0.7031 | 0.5529 |" — NPLExperiment/registrations/H2/REGISTRATION.md:695; and "| at the deadline | 135 | 68 | 43 | 79 | 0.0176 + 0.0227 = 0.0403 | 0.9552 | **0.8629** |" — NPLExperiment/registrations/H2/REGISTRATION.md:697
- **Evidence:**
  - The registration names its own full record two sections earlier: "Full record: `reports/stage_a_h2/ktable_amended.json`." — NPLExperiment/registrations/H2/REGISTRATION.md:646.
  - That artifact records, at look-1 min N: `alpha_spent_look1` **0.008062**, `alpha_spent_look2` **0.029206**, total 0.037268; and at the deadline: `alpha_spent_look1` **0.019230**, `alpha_spent_look2` **0.021113**, total 0.040343.
  - The values 0.0173, 0.0200, 0.0176 and 0.0227 occur nowhere in `ktable_amended.json` (searched every float in the file to ±0.0006).
  - The middle row, "at look-2 min N … 0.0182 + 0.0240 = **0.0422**" (REGISTRATION.md:696), **does** match the artifact exactly (0.018172 + 0.024025).
  - Only the components are wrong: both printed **totals** are right, and the totals are what the section's claim rests on ("Every total spend sits **inside** alpha_h = 0.05", REGISTRATION.md:699-701). k₁, k₂ and both powers in the affected rows are also right.
- **Recomputation:** inputs `src/npl/register/sequential.py:63-121` and `src/npl/power.py:20-42` re-implemented in `/home/kiros-li/.cache/program-audit/scratchpad/work/agentC-npl/h2.py`; method — `alpha_spent_1 = P(Bin(n₁,½) ≥ k₁)`, `alpha_spent_2 = Σ_{s<k₁} P(Bin(n₁,½)=s)·P(Bin(n₂−n₁,½) ≥ k₂−s)`. Result: (59,30) → 0.008062 + 0.029206 = 0.037268; (117,59) → 0.018172 + 0.024025 = 0.042197; (135,68) → 0.019230 + 0.021113 = 0.040343. Tolerance 5e-5.
- **What would resolve it:** correcting the two printed component pairs to the artifact's values.
- **Confidence:** HIGH — recomputed from the module the registration names, and cross-checked against the artifact.
- **Invalidated by later commits?:** no — `registrations/H2/REGISTRATION.md` is unchanged in the four post-anchor commits.
- **Disclosed by authors?:** no.

### DRAFT-V-4
- **Repository / SHA:** NPLExperiment / `8f1fef83be0f76cbd671c2ce0fbfe8b1c4a5ea2c`
- **Hypothesis or artifact:** H1 — Section 8 inference, the multiplicity correction and the decision rule it feeds
- **Direction:** A
- **Class:** STATISTICAL
- **Severity:** S4
- **Label:** DERIVED
- **Claim challenged (verbatim quote):** "Three co-primaries, distribution-free, one-sided, at **alpha_adj = 1 − 0.95^(1/3) = 0.016952 (0.0170)** each. **All three must pass for the Stage B GO row.**" — NPLExperiment/REGISTRATION.md:200-202
- **Evidence:**
  - The decision rule is implemented as a conjunction: `all_co_primaries_pass=p1.passes and p2.passes and p3.passes` — NPLExperiment/src/npl/verdict.py:201.
  - A Šidák correction is a **union**-type adjustment: it controls the probability that *at least one* of several tests rejects. Under an all-must-pass (intersection-union) rule the GO decision rejects only when every component rejects, so its type-I error under any configuration in which at least one component null is true is bounded by the **largest** per-component level; no correction is required. Applying Šidák makes each component strictly harder and the GO strictly harder than the registered family-wise budget requires.
  - The same repository applies the correct reasoning to its successor hypotheses: "H2 and H3 require every co-primary (the weakest governs); H4's grid is disjunctive within the hypothesis (Sidak-corrected), so its best cell governs" — NPLExperiment/src/npl/register/cull.py:18-20, implemented at `cull.py:135-144`. No within-hypothesis correction is applied to H2's two required co-primaries; Šidák is applied only to H4's union of three cells (`conditioning.py:sidak_within`, `registrations/H4/REGISTRATION.md:79-80`). H1 is the only place where a union correction is attached to a conjunction.
  - Direction: the correction makes the conjunction harder to pass, i.e. makes the **FAIL** that H1 fired easier to reach. The H1 row is `row_fired = "FAIL"` (`reports/stage_b/read.json`).
- **Recomputation:** inputs `reports/stage_b/read.json:co_primaries` (197/312, 111/312, 114/175); method — re-run each component at an uncorrected alpha = 0.05 using `verdict.py:clopper_pearson_lower` and `power.py:upper_tail`; script `/home/kiros-li/.cache/program-audit/scratchpad/work/agentC-npl/misc.py`. Result: **P1 lower bound rises 0.570688 → 0.584086, still below the 0.60 bar → FAIL; P2 p = 1.000000 → FAIL; P3 p = 3.767e-05 → PASS. The H1 verdict does not move.** Tolerance 1e-6.
- **What would resolve it:** stating in Section 8 that alpha_adj is deliberately conservative for an intersection-union rule (and therefore that the registered family-wise budget is not binding), or testing each co-primary at 0.05 as an IUT permits. Either way the 2026-08-28 FAIL stands.
- **Confidence:** HIGH on the mismatch and on the recomputation; the practical consequence is nil at these counts, which is why this is S4.
- **Invalidated by later commits?:** no — `REGISTRATION.md` Section 8 and `verdict.py` are unchanged post-anchor, and the read is spent.
- **Disclosed by authors?:** no — no document discusses the conservatism of a union correction under an all-must-pass rule.

### DRAFT-V-5
- **Repository / SHA:** NPLExperiment / `8f1fef83be0f76cbd671c2ce0fbfe8b1c4a5ea2c`
- **Hypothesis or artifact:** H2 — the A.1-measured accrual constant that drives the pair projection and the look dates
- **Direction:** B
- **Class:** ARITHMETIC
- **Severity:** S4
- **Label:** DERIVED
- **Claim challenged (verbatim quote):** "Accrual re-measured at **18.57 events/month** (n = 113 listings/182d) — the carried 18.5 confirmed" — NPLExperiment/report.md:340-341; and "# A.1 measured accrual, trailing 182 days, n = 113 events. / ACCRUAL_PER_MONTH = 18.57" — NPLExperiment/scripts/ktable_amended.py:48-49
- **Evidence:**
  - The script that consumes the constant fixes its own month length: `DAYS_PER_MONTH = 30.44` — NPLExperiment/scripts/ktable_amended.py:50. With the claim's own stated inputs, 113/182 × 30.44 = **18.899**, not 18.57. At a 30-day month it is 18.626.
  - 18.57 corresponds to **n ≈ 111.0** over 182 days, i.e. the 113 listings less the two the same paragraph explicitly excludes: "one new: io:EWY, delisted at birth, never an event; one relist: xyz:XBI" — NPLExperiment/report.md:339-340. The label "n = 113 listings" is therefore the wrong n for the rate printed beside it.
  - The **main-dex** figure in the same sentence *does* reproduce under a 30.44-day month: 3/182 × 30.4375 = 0.5017 → "0.5/month (n = 3)" (report.md:341-342), so the two halves of the sentence use different effective n.
  - n = 113 itself is correct: counting `data/census/census.jsonl` rows whose `first_1d_open_ms` falls in the 182 days before 2026-08-27 gives exactly **113** (of which 3 are main-dex, matching the 0.5/month figure).
  - No A.1 artifact under `reports/` records the accrual measurement; the figure exists only as a hard-coded constant.
- **Recomputation:** inputs `data/census/census.jsonl` (505 rows, read 2026-09-12T12:44Z, UNANCHORED) and `scripts/ktable_amended.py:48-54`; method — count listings in the trailing window, divide by 182, multiply by the script's `DAYS_PER_MONTH`; then re-run the projection at both rates; scripts `accrual2.py` and `misc.py` in the work dir. Result: rate 18.899 vs stated 18.57; at 18.899 the projected deadline pair count becomes **137** rather than 135 and the projected look-2 date moves ~2 days **earlier** (2027-02-27 rather than 2027-03-01); the look-1 date is reached from the 62 backfill pairs and does not move. Tolerance 0.01/month.
- **What would resolve it:** relabelling the constant as n = 111 events (not 113 listings), or restating the rate as 18.90 with n = 113.
- **Confidence:** HIGH on the arithmetic; the effect on every downstream figure is small and in the conservative direction (the stated look dates are later than the measured accrual implies), which is why this is S4 and why it does not weaken the "one month inside the deadline" conclusion.
- **Invalidated by later commits?:** no.
- **Disclosed by authors?:** no.

### DRAFT-V-6
- **Repository / SHA:** NPLExperiment / `8f1fef83be0f76cbd671c2ce0fbfe8b1c4a5ea2c`
- **Hypothesis or artifact:** H5 — the Universe row of the H5 summary table
- **Direction:** neutral
- **Class:** INTERNAL_INCONSISTENCY
- **Severity:** S4
- **Label:** DERIVED
- **Claim challenged (verbatim quote):** "The live family is two dexs: `xyz` 73, `para` 16." — NPLExperiment/HYPOTHESES.md:127
- **Evidence:**
  - `reports/h5/census.json:by_dex_live` = `{"io": 2, "mkts": 3, "para": 16, "xyz": 73}` — four dexs, summing to the 94 live instruments the same table cell reports.
  - The repository's own access document states it correctly: "`xyz` (73) and `para` (16) hold **89 of the 94** live instruments; `mkts` holds 3 and `io` 2" — NPLExperiment/docs/H5_ACCESS.md:152-154.
  - The retrospective section elsewhere names `io:NBIS` as one of the two instruments with any observation (`report.md:693`), so an `io` live instrument is used by name a few pages later.
- **Recomputation:** inputs `reports/h5/census.json` and `reports/h5/census.rows.json`; method — group the 94 `resolved`+`live` rows by `dex`; result 73 / 16 / 3 / 2 = 94. Tolerance exact.
- **What would resolve it:** one word — "two dexs" → "concentrated in two dexs (89 of 94)", matching `docs/H5_ACCESS.md:152-154`.
- **Confidence:** HIGH.
- **Invalidated by later commits?:** no.
- **Disclosed by authors?:** partially — the correct split is stated in `docs/H5_ACCESS.md:152-154`, but the summary table that most readers will read is not corrected.

### DRAFT-V-7
- **Repository / SHA:** NPLExperiment / `8f1fef83be0f76cbd671c2ce0fbfe8b1c4a5ea2c`
- **Hypothesis or artifact:** H2 — Amendment H2-3 Change 1, the fallback control backfill
- **Direction:** neutral
- **Class:** ARITHMETIC
- **Severity:** S4
- **Label:** DERIVED
- **Claim challenged (verbatim quote):** "**24 of 24, zero exclusions**, 19 distinct controls, 174 candidates considered per event and **none skipped for coverage**." — NPLExperiment/report.md:509-511
- **Evidence:**
  - `reports/stage_a_h2/backfill_fallback.json:assigned` carries a `candidates_considered` field per event: the 24 values are **172 (×3), 173 (×12), 174 (×9)** — 174 is the maximum, not a per-event constant.
  - The same artifact records `candidate_universe_n` = **175**, not 174.
  - Everything else in the sentence verifies exactly: `assigned_n` 24, `events_attempted` 24, `distinct_controls` 19, and `candidates_skipped_low_coverage` = 0 on all 24 rows.
- **Recomputation:** inputs `reports/stage_a_h2/backfill_fallback.json`; method — tabulate `candidates_considered` over the 24 assigned rows; script `rest.py` in the work dir. Tolerance exact (integer counts).
- **What would resolve it:** "172–174 candidates considered per event, from a universe of 175".
- **Confidence:** HIGH; hygiene only — the load-bearing part of the sentence ("none skipped for coverage") is exact.
- **Invalidated by later commits?:** no.
- **Disclosed by authors?:** no.

### DRAFT-V-8
- **Repository / SHA:** NPLExperiment / `8f1fef83be0f76cbd671c2ce0fbfe8b1c4a5ea2c`
- **Hypothesis or artifact:** H2 — the Amendment H2-3 precondition timestamp, and the ordering claim it supports
- **Direction:** neutral
- **Class:** INTERNAL_INCONSISTENCY
- **Severity:** S4
- **Label:** DERIVED
- **Claim challenged (verbatim quote):** "**The preconditions, checked and recorded before anything else** (`reports/stage_a_h2/amend_preconditions.json`, PASS at 07:51:10Z on the project clock)" — NPLExperiment/report.md:445-446
- **Evidence:**
  - The artifact the sentence names records `"checked_at": "2026-08-28T06:51:10Z"` — NPLExperiment/reports/stage_a_h2/amend_preconditions.json.
  - The amendment commit is `f31f7a3`, committer date 2026-08-28T00:01:06-07:00 = **2026-08-28T07:01:06Z** (live repo, `git log --format=%cI`, read 2026-09-12T12:48Z). The artifact's 06:51:10Z precedes it by 10 minutes, as the ordering claim requires; the **printed** 07:51:10Z would follow it by 50 minutes, inverting the claim.
  - A parallel, already self-disclosed case: the H5 row is headed "fired 2026-08-28T22:20Z" at `HYPOTHESES.md:122` and `report.md:667` while `reports/h5/verdict.json:fired_at` is **22:04:30Z**; the authors record the correction at `registrations/H5/REGISTRATION.md:632-639` but two of the three sites still carry 22:20Z at the anchor.
- **Recomputation:** none beyond reading the artifact and the git object.
- **What would resolve it:** correcting `report.md:446` to 06:51:10Z, and propagating the already-disclosed 22:04:30Z correction to `HYPOTHESES.md:122` and `report.md:667`.
- **Confidence:** HIGH.
- **Invalidated by later commits?:** no — none of the four post-anchor commits touches these lines.
- **Disclosed by authors?:** the 22:20Z half **yes** (`registrations/H5/REGISTRATION.md:632-639`), which caps that half at S4/S3 and is recorded here as the authors' own catch; the 07:51:10Z half **no**.

---

## 6. What could not be checked, and why

| item | why not |
|---|---|
| Gate figures "249 passed", "217 passed", "172 passed", "159 passed", `mypy --strict` on 71 / 67 files (`report.md:581-582,292,148`; `reports/h5/preconditions.json`; `reports/stage_a_h2/amend_preconditions.json`) | The audit rules forbid executing a repository's own scripts or test suites in place, and the figures are recorded only as free-text strings inside the artifacts. Copying the tree out and building its environment would not reproduce the *historical* runs either. **UNVERIFIABLE by construction.** |
| "156 pages, 60,010 funding hours, **0 unrecoverable hours**" (`report.md:336-337`) | No committed artifact stores page or hour totals for the A.1 archive rebuild; re-deriving them would mean walking all 462 per-instrument directories under `data/funding/` and reconstructing the coverage rule. Not attempted. |
| "median trailing entry funding **+31.6 percent/yr** (min −132.4)" (`report.md:355-356`, `registrations/H4/REGISTRATION.md:211-221`) | The per-event 168-hour trailing means are not stored in any `reports/` artifact; only the three conditioning **counts** (11 / 8 / 5 of 62) are, and those verify. |
| "224,633 funding rows summed inside the 30-day windows" (`report.md:216`) | Verified **as recorded** in `reports/stage_b/read.json:funding_rows_30_total`, but not re-derived from the sealed archives: the window arithmetic requires `src/npl/intervals.py:merge_windows` plus each event's entry anchor, and the archives are untracked. The figure is internally consistent with `preconditions.events_covered_30 = 312`. |
| Whether Amendment H5-2 truly "deleted this entry's only route to VIABLE" (`report.md:663`, `DECISIONS.md:511`) | `src/npl/h5/outcome.py:165-185` fires VIABLE only when a session tag's **median** absolute basis exceeds 54 bp. With the delisted stratum included, the all-resolved median at the fired snapshots is 4.14 / 4.63 / 5.07 bp, and the delisted stratum alone has a median of 30.5 bp — so no **contemporaneous** reading came near VIABLE either way. The claim is a forward statement about a 30-day census in which frozen delisted marks would drift away from live oracles; it cannot be settled from the data at the anchor. Recorded with its numbers, not adjudicated. |
| The independence of the n = 188 H5 sample | 94 instruments × 2 snapshots 8 minutes apart. No interval, test statistic or p-value is computed on it anywhere in `src/npl/h5`, so there is no estimator whose independence assumption could be violated. The repeated-measure structure is disclosed at `registrations/H5/REGISTRATION.md:572`. Nothing to recompute clustered. |
| Cross-sectional dependence in the H1 co-primaries | The 312 events are one draw per instrument-event and are not repeated within instrument, so a within-unit clustered recomputation is not defined. A calendar-block bootstrap would need per-event entry dates, which are not in any tracked artifact (only counts are). The stated comparison (P1 lower bound 0.5707 vs the 0.60 bar) fails by 3 points of share; a block correction would widen the bound and move it further from the bar, i.e. in the same direction, so the conclusion cannot move. Not recomputed. |
| Post-anchor state of `data/` | Everything read from `data/` may have changed after 2026-09-02: `data/h5/snapshots.jsonl` mtime 2026-09-11, `data/ledgers/requests.jsonl` mtime 2026-09-12, `data/state/fresh_plan.jsonl` now 128 lines against the 124 the amendment recorded, `data/controls/h2_pairs.jsonl` now 63 lines against 62 (the 63rd appended 2026-09-02T02:01:32Z). Every figure taken from `data/` is labelled UNANCHORED with its read time. |

---

## 7. Live-repo access log

Live path: `/home/kiros-li/Documents/GitHub/NPLExperiment/`. All access read-only. No file under the audited repository was opened for writing, no script was executed inside it, and no git command other than `status`, `rev-parse`, `log` and `show` was run. No `.env`, keystore, session or credential file was opened.

**Pre-access `git -C /home/kiros-li/Documents/GitHub/NPLExperiment status --porcelain`, 2026-09-12T12:34:05Z — output verbatim:**

```
```

(empty — clean; `data/` is covered by `.gitignore:data/`)

`git rev-parse HEAD` at that moment: `dff16632eca6eea05b290ade5464339f44c75744` (four commits ahead of the anchor).

Files read from the working tree (all read-only, all UNANCHORED):

| path | read (UTC) | what was read |
|---|---|---|
| `data/h5/census.jsonl` | 2026-09-12T12:36Z | 546 JSON lines; two snapshot ids (`…21:44:11Z`, `…21:51:54Z`) |
| `data/h5/snapshots.jsonl` | 2026-09-12T12:36Z, 12:41Z | 3,652 JSON lines; 14 snapshot ids 2026-08-28…2026-09-12 |
| `data/ledgers/requests.jsonl` | 2026-09-12T12:38Z | 58,599 lines (29,298 charge + 29,298 settle + 3 header-less); only `day`, `kind`, `ts`, `endpoint` fields used |
| `data/census/census.jsonl` | 2026-09-12T12:44Z | 505 lines; `first_1d_open_ms`, `dex`, `coin`, `recorded_at` |
| `data/controls/h2_pairs.jsonl`, `data/controls/pairs.jsonl` | 2026-09-12T12:45Z | line counts and `pair_type` tallies (63 / 176) |
| `data/eligibility/{h2,h3,h4}.jsonl`, `data/state/{fresh_plan,retro_plan}.jsonl`, `data/state/generating_sample.json` | 2026-09-12T12:45Z | line/entry counts only (62 / 62 / 186 / 128 / 722 / 312 event ids) |

Git objects read (read-only): `git log`/`show` on `32b3f9e`, `f31f7a3`, `13c6965`, `98e7e01`, `8f1fef8`, `dff1663`; `git show <sha>:src/npl/<module>` piped to `sha256sum` for five modules at two commits.

**Post-access `git -C /home/kiros-li/Documents/GitHub/NPLExperiment status --porcelain`, 2026-09-12T12:48:25Z — output verbatim:**

```
```

(empty — clean, unchanged; `git rev-parse HEAD` still `dff16632eca6eea05b290ade5464339f44c75744`)

Nothing in the audited repository was modified.
