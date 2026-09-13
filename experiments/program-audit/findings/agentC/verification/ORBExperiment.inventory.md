# ORBExperiment — verification inventory (LOCATE)

**Agent C (referee/verifier). No thesis. This document locates what can be verified; it
adjudicates nothing. Nothing here is a finding.**

| | |
|---|---|
| Repository | `ORBExperiment` |
| Anchored SHA | `f2aa675a80fc06b74979040b3028154d1add5ec0` (main, 2026-08-29) |
| Snapshot read | `/home/kiros-li/.cache/program-audit/scratchpad/snap/ORBExperiment/` |
| Live repo touched | `/home/kiros-li/Documents/GitHub/ORBExperiment/` — git objects (log, show, ls-tree, reflog, rev-parse, status) and untracked `data/` only, read-only |
| Compiled | 2026-09-12, 18:01Z–18:20Z |
| Documents read | `README.md`, `REGISTRATION.md` (4,193 lines), `HYPOTHESES.md`, `DECISIONS.md` (38 ADRs), `report.md`, `CLAUDE.md`, `docs/HANDOVER.md`, `docs/STAGES.md`, `docs/DUPLICATION.md`, `docs/STAGE_A_PROMPT.md`, `docs/ACCESS.md` (partial), `reports/**` |
| Not present | **There is no `FINDINGS.md`** and **no `registrations/` directory** — registration is the single `REGISTRATION.md` with 28 numbered amendments. `progress.md` (3,737 lines) is the session log and was read only by targeted grep. |

**Counts: 67 artifact entries** (53 tracked/anchored, 14 untracked/unanchored),
**30 numeric claims** ranked with **7 marked MUST-VERIFY**, **7 interval entries** and
**14 test / power-statistic entries**, **22 provenance claims**.

**A structural fact that governs sections 3 and 4.** **No in-sample or holdout bar has
ever been read in this repository.** Both co-primaries (E1 deflated Sharpe, E2 permutation)
are **unrun**. Consequently **there is no p-value anywhere in the repository and no test
statistic computed from outcome data.** Every "t", "power" and "statistic" below is a
*planning* quantity computed from a registered Sharpe assumption and a session count, not
an estimate from a sample. The one exception — the slippage band, the dispersion, the stop
share and the trigger rate — are descriptive measurements on a **post-holdout carve-out**
(2026-07-01 to 2026-08-28) that is outside both registered windows.

---

## 1. Artifacts — every place a number could be verified

### 1.1 Analysis code (tracked, anchored at `f2aa675`)

| path | what it holds | which document figures it appears to back | anchored? |
|---|---|---|---|
| `src/orb/power.py` (244 lines) | **The whole power arithmetic, small enough to recompute by hand.** `daily_sharpe = annual/√252`; `t_statistic = daily·√n`; `power_one_sided = Φ(t − z(1−α))`; `sessions_for_power = ⌈((z(1−α)+z(β))/daily)²⌉`; `e2_pessimistic_mean = central − shift`; `e2_power_pessimistic = Φ((pess/σ)·√trades − z(1−α))` **with no clamping at zero**; `trades_for_e2_power` returns `Absent` when the pessimistic mean ≤ 0; `joint_power` = `min(E1,E2)` with a Fréchet lower bound `max(0, p₁+p₂−1)` | **every** E1 power, E2 power, joint power and min-n figure in README, HYPOTHESES, report, HANDOVER and every `reports/**` JSON | YES |
| `src/orb/dispersion.py` (44,896 B) | **The sealed carve-out writer.** Produces the dispersion scalar, the execution mix (stop share, ambiguous rate, shift), the **measured slippage band** (per-leg overshoot + time-weighted half spread), and the H1b floor scan. `central_mean = dispersion · (annual/√252) / √trades_per_session` at lines ~1140–1142 | dispersion 2.029585; stop share 0.381818; shift 0.041455; the six measured band ends; the floor-scan ratios | YES |
| `tools/slippage_band.py` (299 lines) | TASK 2 producer — writes `reports/stage_a3rescue/task2_slippage_band.json`. **First appears in commit `5899e1b`**, 27 min 48 s after the criterion commit `4ae14dc` | the measured band, the 0.467065 shift | YES |
| `tools/rescue_verdict.py` (195 lines) | TASK 3 producer — applies the Amendment 24 criterion, writes `task3_rescue_verdict.json` | `NOT_RESCUED`, E2 0.000000, joint 0.000000, pess mean −0.426679 | YES |
| `tools/floor_scan.py` (193 lines) | TASK 4 producer — the H1b price-floor feasibility scan | the five-floor table | YES |
| `tools/joint_power.py` (8,547 B) | The E2+joint power writer. **Reads `mean_per_unit_sharpe` off the stored dispersion table rather than re-deriving it** (lines 62–72) — so the two records cannot drift, but also cannot cross-check each other | 0.040386, −0.001068, E2 0.043277, joint 0.043277 | YES |
| `tools/power_gate.py` (4,564 B) | A.2 power table producer at `alpha_adj` | `reports/stage_a2/power.{json,md,txt}` | YES |
| `tools/execution_mix.py` (9,134 B) | Stop/close mix, ambiguous rate, shift | 210/340, 0.381818, 0.041455 | YES |
| `tools/dispersion_compute.py`, `tools/dispersion_pull.py` | Carve-out pull and dispersion computation | 2.029585, trigger rate 0.982143 | YES |
| `src/orb/costs.py` + `src/orb/costs_registered.py` | The Section 6 cost model, frozen and hashed; **refuses to price when the SEC Section 31 effective date is absent** | the round-trip 0.0386/0.0686; the 550-of-550 refusal; `Absent` under the frozen model | YES |
| `src/orb/calendar.py` (7,354 B) | NYSE rules encoded, not downloaded | 2,637 sessions, 21 half, 1,762 in-sample, 875 holdout | YES |
| `src/orb/section0.py` + `src/orb/verdict.py` | The Section 0 outcome map and its clause ordering | every `PENDING_ACCESS` / `PENDING_REVISION` firing | YES |
| `src/orb/comparator.py` (16,137 B) | The sealed comparator — **built, armed, never run**: the bar-revision and cross-vendor-agreement measurements do not exist | the two `Absent(not_yet_measured)` integrity rows | YES |
| `src/orb/config.py` (10,601 B) | **The registered constants.** `entry_slippage_usd=(0.010,0.020,0.040)`, `stop_slippage_usd=(0.020,0.040,0.080)`, `close_slippage_usd=(0.005,0.010,0.020)`, `per_test_alpha=0.05`, `alpha_adj` superseded, `trial_count=8`, `registered_sharpe_assumption=1.40`, `published=2.81`, `quartered=0.70`, `trading_days_per_year=252`, `min_session_open_usd=5.00`, `relvol_lookback_sessions=14`, `pre_period_end_ms=1_451_917_800_000`, `post_holdout_start_ms=1_782_878_400_000` | the "registered band is NOT moved" claim; every assumption | YES |
| `src/orb/absence.py`, `latch.py`, `ledger.py`, `seal.py`, `redact.py`, `callstate.py`, `sessionclock.py`, `preperiod.py`, `fields.py`, `integrity.py` | Guards 1–8 | the guard and mutation claims | YES |
| `tools/reach_bisect.py`, `reach_power.py` | Vendor reach bisection and its power consequences | 2016-01-04 / 2024-08-29, 16 probes each | YES |
| `tools/tape_identify.py` (9,766 B) | The tape verdict and its two controls | `SAME_TAPE` 1.005197, controls ≈0.0278 | YES |
| `tools/delisted_coverage.py`, `delisted_supplement.py` | Delisted enumeration and intraday-history checks | 203 / 229, 4,731 of 6,421 | YES |
| `tools/alpaca_ceiling.py`, `alpaca_sustained.py`, `probe_ceilings.py`, `ceilings_credentialed.py` | Rate-ceiling escalations | 384 in 55.96 s; 250 at 199.73/min; Massive 5.00/min | YES |
| `tools/probe_pull.py`, `repull_probe.py`, `confirm_feed.py` | The sealed probe slice, the 14-day refusal (exit 78), the feed confirmation | 480 files / 737,507 bars; `CONFIRMED_CONSOLIDATED` | YES |
| `tools/refire_section0.py`, `_amend.py`, `_repair.py`, `_rescue.py`, `fire_section0.py` | The five Section 0 firings | `reports/**/task*_section0.json` | YES |
| `tools/mutate.py` (17,272 B) | The mutation harness (17 mutations) | "17 mutations, 0 harness failures" | YES |
| `tools/freeze_costs.py`, `tools/_a1r.py`, `tools/probe_access.py`, `tools/probe_credentialed{,_b}.py` | Cost freeze; A.1 helpers; access probes | the frozen sha256; the 9-vendor table | YES |
| `tests/` — 24 files (23 `test_*.py` + `tools_freeze.py`) | **419 tests** | "419 passing", every guard/mutation pin | YES |

**Code totals: 32 `src/orb` + 31 `tools` + 24 `tests` = 87 Python files.**

### 1.2 Stored result artifacts (tracked, anchored) — 49 files under `reports/`

| path | what it holds | which document figures it backs | anchored? |
|---|---|---|---|
| `reports/stage_a3rescue/task2_slippage_band.json` (4,260 B) | **The deciding artifact of the closure.** `measured_shift_usd_per_share = 0.46706520287790176`; `measured_band` (6 ends); `measured_against_carried` (6 ratios + verdict strings); `per_leg_statistics` with mean/median/p90/n for entry overshoot (n=550, 457 intrabar, 93 gapped), entry half spread (550 served, 0 refused), entry total (550), stop overshoot (210, 195/15), stop half spread (210), stop total (210), close slippage (340, 0 without an official print); `assignment_fixed_before_computation`; `quote_requests_sent = 759`; `bars_read = 1927156`; `sessions_used = 28`; `tickers_with_bars = 199`; `stop_exit_share_used = 0.3818181818181818`; `measured_at = "2026-08-29"` | README.md:289–315; HANDOVER.md:53–65; HYPOTHESES.md:59; report.md:945–970; REGISTRATION.md Amendment 26 §2–§5 | YES |
| `reports/stage_a3rescue/task3_rescue_verdict.json` (6,786 B) | `outcome = "NOT_RESCUED"`; `criterion_commit = "4ae14dc"`; `criterion_precommitted_before_the_measurement = true`; `criterion_precommitted_on = "2026-08-30"`; `computed_at = "2026-08-29"`; `deciding_numbers` (central 0.04038617169045801, shift 0.46706520287790176, pess −0.42667903118744377, E2 power 0.0); 6 rows × (E1 power, E2 power, joint, min-n, trades_implied 17188/34611); `shift_before_and_after.ratio_measured_over_carried = 11.266923753633597` | README.md:28; HYPOTHESES.md:59–62; report.md:974–976; REGISTRATION.md Amendment 28 §1–§2 | YES |
| `reports/stage_a3rescue/task4_floor_scan.json` (4,565 B) | H1b scan, 5 rows: floor / eligible / selected / sessions_with_a_full_top20_selection / mean_relvol / dispersion / central mean / shift / ratio; `hypothesis_status = REGISTERED_NOT_OPEN`; `requests_sent = 0` | README.md:323–347; report.md:1045–1056; REGISTRATION.md Amendment 27 | YES |
| `reports/stage_a3rescue/task3_execution_mix.json` (1,651 B) | stop_exit_share 0.38181818181818183 (210 stop / 340 close of 550 triggered of 560 evaluated); ambiguous_rate 0.0; `mean_pessimistic_shift_usd_per_share = 0.04145454545454545`; bounds 0.030/0.060; long-only sensitivity (294 triggered, 0.3843537); `requests_sent = 0` | README.md:260–262; ADR-035; Amendment 20 | YES |
| `reports/stage_a3rescue/task5_section0.json` (5,219 B) | The fourth `PENDING_REVISION`, `fired_at 2026-08-30T03:42:21+00:00`, with every input incl. the measured band and `rescue_outcome = NOT_RESCUED`. **Byte-identical to `reports/stage_a1r/task5_section0.json`**, which was created in the same commit `34a91b3` | README.md:58–78; HYPOTHESES.md:65,68 | YES |
| `reports/stage_a3rescue/gates.log` (693 B) | `56 files already formatted` · `no issues found in 56 source files` · **`419 passed in 2.63s`** | "419 passing", "mypy strict clean, 56 source files" | YES |
| `reports/stage_a3rescue/mutations.md` + `mutations_run.log` | 17 mutations, `harness failures: 0`, each with its failing test | "17 mutations applied to real source, 0 harness failures" | YES |
| `reports/stage_a2repair/task1_alpha.json` (3,080 B) | `corrected_alpha 0.05` vs `superseded_alpha 0.025320565519103666`; 6 rows with E1 power at both alphas, deltas, min-n at both (198/795/3180 vs 250/1006/4021) | README.md:255–259, 401–405; HYPOTHESES.md:82; Amendment 18 | YES |
| `reports/stage_a2repair/task4_joint_power.json` (9,433 B) | `central_mean_per_unit_of_annual_sharpe = 0.028847265493184292`; `pessimistic_shift 0.04145454545454545`; 6 rows with E2 power at 0.05, joint power (upper bound / Fréchet / nested), binding component, min-n | README.md:263–271; ADR-034; Amendment 21 | YES |
| `reports/stage_a2repair/task6_section0.json` (5,228 B) | The third `PENDING_REVISION`, `fired_at 2026-08-29T19:31:11Z`. **Byte-identical to `reports/stage_a1r/task6c_section0.json`** | README.md:102–134 | YES |
| `reports/stage_a2repair/{gates.log,mutations.md,mutations_run.log}` | 16 mutations at that pass | — | YES |
| `reports/stage_a1amend/task5c_dispersion_e2.json` (14,385 B) | `dispersion_usd_per_share 2.029585030455633`; bracket low `2.0294139223208143`, relative width `8.430695548655339e-05`; 6 E2 power rows at `alpha_adj`; `net_edge_rows`; `measured_trigger_rate 0.9821428571428571` (n=560); `trades_per_session_measured 19.642857142857142`; 4 named runs incl. `frozen_section_6_model` with `trades_refused_by_cost_model = 550`; `reference_pool_size 5317`, `universe_stride 26`, `tickers_sampled 200`, `sessions_pulled 42`, `sessions_evaluable_after_trailing_window 28` | README.md:217–238, 417–421; HYPOTHESES.md:66–67; ADR-031 | YES |
| `reports/stage_a1amend/task5b_post_holdout_pull.json` (124,755 B) | The carve-out pull manifest (42 sessions × 200 tickers) | "42 / 28, 200 tickers, 1,927,156 bars" | YES |
| `reports/stage_a1amend/task3b_feed_confirmation.json` (6,778 B) | `CONFIRMED_CONSOLIDATED`, 7 discriminating chunks of 8 | README.md:234 | YES |
| `reports/stage_a1amend/task4b_alpaca_ceiling.json` (5,952 B) | Burst 384 in 55.96 s, 385th `429`, 391 sent; sustained 250/250 at 199.73/min | README.md:230–232; ADR-030 | YES |
| `reports/stage_a1amend/task6b_section0.json` (6,031 B) | The second `PENDING_REVISION`, `fired_at 2026-08-29T18:43:38Z`. **Byte-identical to `reports/stage_a1r/task6b_section0.json`** | README.md:89–100 | YES |
| `reports/stage_a1r/task9_probe_manifest.json` (268,049 B) | `files_stored 480`, `bars_stored 737507`, `session_ticker_pairs 2400`, `session_count 60`, `ticker_count 40`, `feed "sip"`, `pulled_at "2026-08-29"`, `registered_wait_days 14`, `earliest_eligible_repull "2026-09-12"`, `chunks_needing_more_than_one_page 0` | README.md:71–77, 200–201; report.md:362 | YES |
| `reports/stage_a1r/task5_reach.json` (14,489 B) + `task5_reach_power.json` (1,793 B) | 32 bisection attempts on AAPL; per-vendor earliest served session, reachable/registered session counts, shortfalls, E1 power on the reachable holdout; `cross_vendor_overlap` 459 holdout / 0 in-sample from 2024-08-29 | README.md:189–190, 199; HYPOTHESES.md:70,79–80 | YES |
| `reports/stage_a1r/task4_tape.json` (19,683 B) | 3 comparisons × (median, IQR low/high, min, max, 100 pairs, verdict); 60 calls; 5 sessions × 20 tickers | README.md:191–193; ADR-021, ADR-022 | YES |
| `reports/stage_a1r/task6_delisted.json` (584,119 B) + `task6b_delisted_in_window.json` (46,040 B) | `enumerated_delisted_names 6421` over 7 pages; `enumerated_inside_window 4731`; `delisted_names_with_intraday_history 203`; `combined_in_window_checks 229` (89 first pass + 140 supplementary); `served_share 0.8864628820960698`; `registered_verdict "PASS"` | README.md:194–196; HYPOTHESES.md:70 | YES |
| `reports/stage_a1r/task7_ceilings.json` (6,153 B) | 4 escalations with achieved rate, admitted, first refusal, verbatim redacted refusal payloads | README.md:197–198; ADR-026 | YES |
| `reports/stage_a1r/task3_auth.json` (7,247 B) | 11 credential/auth probes incl. the live-trading `401` | README.md:14–18 | YES |
| `reports/stage_a1r/task10_section0.json` (2,787 B) | The **first** `PENDING_REVISION`, `fired_at 2026-08-29T07:47:54Z` | README.md:58–78 | YES |
| `reports/stage_a1r/task3_execution_mix.json`, `task3b_…`, `task4b_…`, `task5b_…`, `task5c_…`, `task5_section0.json`, `task6b_section0.json`, `task6c_section0.json` | **All byte-identical duplicates** of the same-named files in `stage_a1amend`, `stage_a2repair` or `stage_a3rescue` | — | YES |
| `reports/stage_a1r/mutations.md`, `mutations_run.log` | earlier mutation passes | — | YES |
| `reports/stage_a2/power.json` (2,877 B), `power.md` (5,034 B), `power.txt` (2,009 B) | 9 rows at `alpha_adj = 0.025320565519103666`, each with `t`, E1 power, min-n, `e2_power: "Absent"`; the 515/514 and 1,158/1,157 disagreements; the 1,003-session knife-edge | README.md:387–394; report.md:175–207 | YES |
| `reports/stage_a2/calendar.md` (7,428 B) | Per-year sessions and half sessions; the 1,762 (+2) and 875 (−5) deltas against the registration's approximations; the 2018 hand check `261 − 10 = 251` | README.md:359–366; report.md:109–133 | YES |
| `reports/stage_a2/section0.json` (1,223 B) | `PENDING_ACCESS`, `fired_at 2026-08-29T02:43:20Z`, with the `DEGRADED` counterfactual recorded inside it | README.md:83–87; report.md:211–231 | YES |
| `reports/stage_a4/gates.md` (2,833 B) | **STALE.** Says `46 files already formatted`, `no issues found in 46 source files`, **`270 passed`** — superseded by `stage_a3rescue/gates.log` (56 files, 419 passed) and **not refreshed**. The companion `stage_a4/mutations.md` *was* refreshed to 17 mutations in `f2aa675` | the guard table is still cited; the 46/270 figures are contradicted by README.md:438–439 | YES (stale content) |
| `reports/stage_a4/mutations.md` (4,665 B) | 17 mutations, 2 marked *GUARD STOPPED BINDING* | README.md:440–441 | YES |

### 1.3 Untracked / unanchored data in the live working tree

`data/` is gitignored (`.gitignore` line 2). Everything below was observed by `ls -la`,
line counts and JSON key inspection **at 2026-09-12 18:01Z–18:05Z** and **may have changed
since the anchor of 2026-08-29**. No large binary was opened. `.env` was **never opened**.

| path | size / count | mtime | what it holds | backs | anchored? |
|---|---|---|---|---|---|
| `data/access/requests.jsonl` | 336,697 B, **2,766 rows** | 2026-08-29 20:39 | the append-only request ledger; each row `{day, endpoint, kind:"charge", recorded_at, vendor}`. Day split: 2026-08-29 → 2,005; 2026-08-30 → 761. Vendor split: alpaca 2,640, massive 102, polygon 15, alphavantage 7, databento 1, tiingo 1. Endpoint split: `alpaca:bars` 1,875, `alpaca:quotes` 761, `massive:aggs` 78, `massive:reference` 24, `polygon:aggs` 14, … | the `n = 1,026`, `n = 979` (973 Alpaca + 6 Massive), `1,879 of 3,000`, and `n = 759` request claims | **NO — unanchored** |
| `data/access/seals.jsonl` | 559,143 B, **1,978 rows** | 2026-08-29 20:39 | one SHA-256 seal row per stored file | the seal/manifest claims | NO |
| `data/access/sealed_credentialed/` | **1,957 files, 349,976,958 B** | 2026-08-29 20:15–20:39 | prefix census: `task2q_*` **759**, `task9_*` **481** (480 bar files + 1 reference pool), `task5b_*` 314, `task6_*` 147, `task6b_*` 140, `task4_*` 60 (20 massive + 20 alpaca_sip + 20 alpaca_iex), `task5_*` 27, `task3b_*` 20, `task3_*` 7, `task2_quoteprobe_*` 2 | the 480-file seal; the 759 quote requests; the 100-pair tape; the probe slice | NO |
| `data/access/carve_out_reads.jsonl` | 3,123 B, 4 rows | 2026-08-29 20:39 | the carve-out read log | the four carve-out writer runs | NO |
| `data/access/sealed/` | 7 `.raw` files, ≤ 220 B each | 2026-08-28 19:15 | the pre-credential refusal bodies | the "0 of 9 vendors serving a bar" table | NO |
| `data/access/robots/` | 21 `.txt`, 81,041 B largest | 2026-08-28 19:13–19:28 | fetched `robots.txt` per host | "15 hosts fetched", the 4 terms refusals | NO |
| `data/access/fees/` | 4 HTML, 676 KB (`ibkr_stocks.html` 584,282 B, `finra_taf.html` 88,292 B, `sec_fee.html`/`sec_fee2.html` 1,925 B each) | 2026-08-28 19:29–19:30 | the live fee-schedule bodies | "HTTP 200, 584,282 bytes"; TAF 0.000195; the 403 on `sec.gov` | NO |
| `data/access/probe_findings.json` | 3,611 B | 2026-08-28 19:15 | the 9-vendor access probe | the A.1 access table | NO |
| `data/access/ceiling_findings.json` | 2,668 B | 2026-08-28 19:19 | the pre-credential ceiling escalation | "18 requests, 0 × 429, 88.4/min, 29.1/min" | NO |
| `data/state/section0.jsonl` | 19,078 B, **5 rows** | 2026-08-29 20:42 | the five Section 0 firings: `PENDING_ACCESS` 02:43:20Z; `PENDING_REVISION` 07:47:54Z, 18:43:38Z, 19:31:11Z, and 2026-08-30T03:42:21Z | every Section 0 claim, and the "re-fired a fourth time" count | NO |
| `data/state/cost_model.jsonl` | 873 B, 1 row | 2026-08-28 19:32 | `kind: cost_model_freeze`, `canonical_bytes 359`, `recorded_at 2026-08-29T02:32:28.834Z`, `measured_against_carried` per component, `sha256 3789221b…` | the frozen-model hash, the TAF staleness, the three unmodeled components | NO |
| `data/state/cost_model_latch.json` | 113 B | 2026-08-28 19:32 | `{measured_on: "2026-08-29", sha256: "3789221b9dd3fea5a9680547dfdf8ec7b1febaf246042fe1fa70e27ca610fba3"}` | report.md:169 | NO |
| `_PARKED_CHECK_BEFORE_RUNNING` | 322 B | **2026-09-02 22:38 — four days AFTER the anchor** | *"THIS REPOSITORY IS PARKED, NOT CLOSED. H1 and H1b closed cost-bound. H2 (pre-FOMC) and H3 (VIX roll yield) are parked pending a revision measurement that becomes eligible 2026-09-12."* **Untracked, post-anchor, and it disagrees with the anchored documents on two points: H1b is `REGISTERED_NOT_OPEN` at `f2aa675`, and neither H2 nor H3 exists anywhere in the anchored `HYPOTHESES.md`** | nothing in the anchored record | NO — post-anchor |
| `.env` | 166 B | 2026-08-28 20:43 | credentials | — | **NEVER OPENED** |

---

## 2. Numeric claims, ranked — what the verdicts rest on

Ranked by how much rests on them. **MUST-VERIFY** marks the seven the closure cannot survive
being wrong about.

### RANK 1 — MUST-VERIFY · the closure's deciding number

> *"The registered rule cannot clear its own registered cost band. The measured slippage
> band on the traded instruments gives a pessimistic-minus-central shift of **0.467065 USD
> per share** against a central mean of **0.040386** at the registered effect assumption.
> The pessimistic-cost mean is **−0.426679**. **E2 power 0.000000. Joint power 0.000000.**"*
> — `ORBExperiment/README.md:28`

Also `HYPOTHESES.md:59`, `docs/HANDOVER.md:7`, `report.md:974-976`, `REGISTRATION.md:4081-4086`.
**Figures:** shift 0.46706520287790176; central 0.04038617169045801; pessimistic
−0.42667903118744377; E2 power 0.0; joint 0.0. **n = 875** holdout sessions,
**17,188 implied trades**, band measured on **n = 550 / 210 / 340** trades from
**28 evaluable post-holdout sessions**.
**Produced by:** `tools/slippage_band.py` → `reports/stage_a3rescue/task2_slippage_band.json`;
`tools/rescue_verdict.py` → `task3_rescue_verdict.json`;
`src/orb/power.py::e2_power_pessimistic` / `joint_power`.
**Recompute path:** `pess = 0.040386 − 0.467065 = −0.426679`;
`effect = (−0.426679 / 2.029585)·√17188 = −27.57`; `Φ(−27.57 − 1.6449) ≈ 0`. Every input is stored.

### RANK 2 — MUST-VERIFY · the criterion threshold itself

> *"the implied central mean of **0.040386** at the registered assumption"* — `README.md:118`;
> *"`RESCUED_DEGRADED` required the shift to fall **strictly below 0.040386**"* — `HYPOTHESES.md:60`

**Figure:** `central_mean_per_unit_of_annual_sharpe = 0.028847265493184292`, × 1.40 =
0.04038617169045801. **n:** derived from `dispersion = 2.029585030455633` (n = 550 priced
trades) and `trades_per_session_measured = 19.642857142857142` (n = 28 sessions).
**Produced by:** `src/orb/dispersion.py:1140-1142`
(`central_mean = dispersion · (annual/√252) / √trades_per_session`), read back verbatim by
`tools/joint_power.py:62-72`. **This single scalar sets both the `RESCUED_DEGRADED`
threshold and the sign of the pessimistic mean at every assumption**, so it carries more
weight than any other derived quantity in the repository.

### RANK 3 — MUST-VERIFY · the measured band, its ratios and its decomposition

> *"entry, central 0.0200 → **0.087019** (**4.35×**) … entry, pessimistic 0.0400 →
> **0.354645** (**8.87×**) … stop, central 0.0400 → **0.033529** (0.84×) … stop,
> pessimistic 0.0800 → **0.198061** (**2.48×**) … close, central 0.0100 → **0.040000**
> (**4.00×**) … close, pessimistic 0.0200 → **0.261000** (**13.05×**)"* — `README.md:289-296`

Also `REGISTRATION.md:3973-3980`, `report.md:945-952`, `HANDOVER.md:53-58`, `HYPOTHESES.md:59`.
**n:** entry 550, stop 210, close 340. **Decomposition** (`REGISTRATION.md:4022-4027`):
entry width 0.267626 (57.3 %) + stop width × 0.381818 = 0.062821 (13.5 %) + close width ×
0.618182 = 0.136618 (29.3 %) = **0.467065**.
**Produced by:** `tools/slippage_band.py`, `src/orb/dispersion.py`;
stored in `task2_slippage_band.json`. **Verifiable from the stored JSON alone** — every
median, p90, n and carried figure is in the file; the ratios and the decomposition are pure
arithmetic on them.

### RANK 4 — MUST-VERIFY · E1 power, the number the closure is careful to preserve

> *"**E1 remains powered at 0.832450**"* — `README.md:49`, `HYPOTHESES.md:63`, `HANDOVER.md:65,80`;
> *"E1 at the registered 1.40 Sharpe assumption moves 0.743521 → 0.832450 on the achievable
> holdout, and the minimum n for 80 percent power falls 1,006 → 795 against 875 achievable"*
> — `README.md:110-112`

**Figures:** 0.8324500493878693 at α = 0.05; 0.7435206445941073 at α = 0.025320565519103666;
min n 795 vs 1,006; **n = 875**. **Produced by:** `src/orb/power.py::power_one_sided` /
`sessions_for_power`; `tools/power_gate.py` and `reports/stage_a2repair/task1_alpha.json`.
**Recompute:** `t = 1.40/√252 · √875 = 2.608746`; `Φ(2.608746 − 1.644854) = 0.83245`.
**Why it ranks here:** it is the load-bearing number in every "what the closure is NOT"
sentence, and it is also the number that makes Amendment 21 route (a) (demote E2) survivable.

### RANK 5 — MUST-VERIFY · the pre-rescue collapse that motivated the whole pass

> *"The measured pessimistic shift of 0.041455 USD per share exceeds the implied central mean
> of 0.040386 at the registered assumption, so the pessimistic-cost mean is −0.001068 —
> negative. E2 power is 0.043277, below the 0.05 size of the test, and JOINT power collapses
> with it. No session count reaches 80 percent."* — `README.md:118`

Also `HYPOTHESES.md:82`, `HANDOVER.md:279-282`, `DECISIONS.md:1252`, Amendment 21.
**Figures:** shift 0.04145454545454545 (from stop share 0.381818, n = 550); pess mean
−0.0010683737640874436; E2 power 0.043276644872287495; joint 0.043276644872287495.
**Produced by:** `tools/execution_mix.py` → `task3_execution_mix.json`;
`tools/joint_power.py` → `task4_joint_power.json`.
**The margin is 0.001069 USD/share — about a tenth of a cent.** A 2.6 % error in the
central mean or the shift flips the sign, so this is the most precision-sensitive claim in
the repository.

### RANK 6 — MUST-VERIFY · the pre-committed arithmetic that ruled `GO` out

> *"For E2 to reach 80 percent power on 875 sessions at the registered 1.40 assumption, with
> the measured dispersion of 2.029585 USD per share and 19.642857 trades per session, the
> pessimistic-cost mean must be at least **0.038493 USD per share** — which means the shift
> must fall to **0.001893 or below**, a **21.89-fold reduction** from the measured 0.041455.
> **That is below a single tick across both legs.**"* — `report.md:884-891`

Also `README.md:32-34`, `DECISIONS.md:1353-1357`, `REGISTRATION.md:3686-3702` (table with
`z(0.95)+z(0.80) = 2.486475`). **n = 875 sessions / 17,188 trades.**
**Recompute:** `required mean = 2.486475 · 2.029585 / √17188 = 0.038493`;
`0.040386 − 0.038493 = 0.001893`; `0.041455 / 0.001893 = 21.90`.
**This claim is what makes the pass unfalsifiable-in-the-favourable-direction**; it must
hold arithmetically or the "GO was never reachable" framing fails.

### RANK 7 — MUST-VERIFY · the claim that the closure does not depend on the halving heuristic

> *"At the source study's own undecayed **2.81** the pessimistic-cost mean is **−0.386004**
> and E2 power is **zero** as well."* — `README.md:44-46`; and the carried-vs-measured
> contrast at `report.md:990-993`: **0.819524 → 0.000000**.

**Figures:** central at 2.81 = 0.08106081603584786; pess = 0.08106081603584786 − 0.467065 =
−0.3860043868420539; E2 power at 2.81 under the carried band = 0.819523804601201 (min n 827).
**n = 875.** **Produced by:** `task4_joint_power.json` (carried) and
`task3_rescue_verdict.json` (measured). **Why it matters:** without it the closure is
conditional on the McLean–Pontiff halving, which the repository itself calls a heuristic.

---

### Ranks 8–30 (not marked MUST-VERIFY)

| # | claim (abbreviated, verbatim in the JSON) | file:line | figures | n | produced by |
|---:|---|---|---|---|---|
| 8 | break-even Sharpe **1.437035**; the registered 1.40 sits **2.577 percent** below it; break-even stop share **0.346206** against a measured 0.381818 | `README.md:272-274`; `DECISIONS.md:1274-1276`; `report.md:773` | 1.437035 / 2.577 % / 0.346206 | 875 | `tools/joint_power.py`, Amendment 21 §4 |
| 9 | E2 dispersion input **2.029585 USD/share**, bracket relative width **8.43 × 10⁻⁵**; under the frozen Section 6 model **`Absent` — 550 of 550 trades refused** | `README.md:221-223`; `report.md:548` | 2.029585030455633 / 2.0294139223208143 | 550 priced trades, 28 sessions | `src/orb/dispersion.py`, `task5c_dispersion_e2.json` |
| 10 | measured **stop-exit share 0.381818** — 210 stop, 340 close; **ambiguous rate 0.000000**, rule-of-three upper bound **0.005357** | `README.md:260-261`; `DECISIONS.md:1299-1301` | 0.38181818181818183 / 0.0 / 0.005357 | 550 / 560 | `tools/execution_mix.py`, ADR-035 |
| 11 | measured **trigger rate 0.982143** against an assumption of **0.55**; long-only **0.525**; **19.64** trades per session of a registered 20 | `README.md:217-220`; `HYPOTHESES.md:67,81` | 0.9821428571428571 / 0.525 / 19.642857142857142 | 560 name-sessions, 28 sessions | `task5c_dispersion_e2.json`, Amendment 15/22 |
| 12 | calendar: **2,637 sessions, 21 half**, in-sample **1,762** (registration said ~1,760), holdout **875** (said ~880); 2 unscheduled closures | `README.md:359-366`; `reports/stage_a2/calendar.md` | 2637 / 21 / 1762 / 875 | 11 calendar years | `src/orb/calendar.py` |
| 13 | E1 power at the superseded `alpha_adj = 0.02532057`: **0.9995 / 0.7435 / 0.2578**, min N **250 / 1,006 / 4,021**, `t = 2.6087` | `README.md:387-394`; `reports/stage_a2/power.md` | see left | 875 | `tools/power_gate.py` |
| 14 | the knife-edge: **1,003 sessions → power 0.7991**, short of 0.80 by **0.0009** and of 1,006 by **three trading days**; 2027-06-30 gives 1,126 and **0.8425** | `report.md:191-195`; `reports/stage_a2/power.md` | 0.799135859539906 / 0.0009 / 0.8425144846005717 | 1,003 / 1,126 | `power.json` |
| 15 | two min-N disagreements with the prompt: **515 not 514** (t = 1.9994 at 514); **1,158 not 1,157** (t = 2.9998 at 1,157) | `report.md:198-200` | 515 / 1,158 | — | `src/orb/power.py::sessions_for_t` |
| 16 | Alpaca earliest served session **2016-01-04** — **1,762/1,762** in-sample and **875/875** holdout; Massive **2024-08-29** — **0/1,762** and **459/875** | `README.md:189-190,199` | — | **16 bisection probes each** | `tools/reach_bisect.py`, `task5_reach.json` |
| 17 | tape verdict **`SAME_TAPE`**, median first-5-minute volume ratio **1.005197**, IQR **[1.003096, 1.007726]**; controls **0.027856** and **0.027761** `DIFFERENT_TAPE` | `README.md:191-193`; `DECISIONS.md:619` | see left | **100 session-ticker pairs** each | `tools/tape_identify.py`, `task4_tape.json` |
| 18 | delisted coverage **`PASS`**: **203** names with intraday history of **229** checked, share **0.8865**; **4,731** of **6,421** enumerated inside the window over 7 pages | `README.md:194-196` | 203 / 229 / 0.8864628820960698 / 4731 / 6421 | 229 checked (89 + 140) | `tools/delisted_coverage.py`, `task6b_delisted_in_window.json` |
| 19 | probe slice sealed: **60 sessions × 40 tickers = 2,400 pairs, 480 files, 737,507 bars**; registered **14-calendar-day wait** → earliest eligible re-pull **2026-09-12** | `README.md:71-77,200-201`; `report.md:362` | 480 / 737507 / 2400 | — | `tools/probe_pull.py`, `task9_probe_manifest.json` |
| 20 | cost model: FINRA TAF carried **0.000166** vs measured **0.000195** — **14.9 % low**; three components not previously modeled (1 % cap, CAT 0.000003, clearing 0.00020); round trip on a 50 USD name **≈ 0.0386** close / **≈ 0.0686** stop against a carried gross edge of **0.070** = **55 %** and **98 %**; slippage **78 %** of the close-exit total; frozen `3789221b…` | `README.md:370-383`; `report.md:146-170`; `HYPOTHESES.md:72` | see left | — | `src/orb/costs.py`, `data/state/cost_model.jsonl` (untracked) |
| 21 | request ledger: **n = 1,026** charged on the credentialed pass; **n = 979** further (973 Alpaca, 6 Massive); **1,879 Alpaca of a 3,000 daily cap**; **n = 759** quote requests in the rescue pass; **0 dollars** throughout | `README.md:182,209-213,285` | 1026 / 979 / 1879 / 759 / 0 | — | `data/access/requests.jsonl` (untracked; **2,766 rows observed 2026-09-12**: 2,005 on 08-29 + 761 on 08-30; 1,026 + 979 = 2,005 ✓; 761 − 2 quote probes = 759 ✓) |
| 22 | Alpaca ceiling: **384 requests admitted in 55.96 s, 385th refused `429`** (391 sent); **sustained not reached** — 250 of 250 at **199.73/min** over 75.10 s; operating pace **98.36/min** at 0.61 s spacing; daily cap **3,000** is a circuit breaker from **no** measured allowance | `README.md:230-233` | see left | 391 / 250 / 25 | `tools/alpaca_ceiling.py`, `alpaca_sustained.py` |
| 23 | Massive measured ceiling **5.00/min**, first refusal at **request 6 of 8**, **both endpoints** | `README.md:197` | 5.00/min | 16 | `task7_ceilings.json` — *note the stored rows record `achieved_rate_per_min` 30.45 and 28.67 with 5 admitted; "5.00/min" is a re-expression of "5 admitted before refusal", not the achieved rate* |
| 24 | sealed slice feed **`CONFIRMED_CONSOLIDATED`** — every sealed bar count equals the consolidated count, none equals the single-venue count | `README.md:234` | — | **7 discriminating chunks of 8** | `tools/confirm_feed.py`, `task3b_feed_confirmation.json` |
| 25 | H1b floor scan: ratio rises **0.9742 → 0.9983 → 1.1415 → 1.4767 → 2.1424** while the shift stays inside a **4 percent band**; mean relvol falls **2.0652 → 1.4103**; the scan is a **200-name systematic sample (every 26th) of a 5,317-name listing**, a universe **26.6 times larger** | `README.md:323-342`; `report.md:1045-1056` | see left | 560 / 446 / 310 name-sessions; 28 sessions | `tools/floor_scan.py`, `task4_floor_scan.json` |
| 26 | software: **419 tests passing**; **mypy strict clean, 56 source files**; **17 mutations, 0 harness failures** | `README.md:438-441`; `HANDOVER.md:67` | 419 / 56 / 17 | — | `reports/stage_a3rescue/gates.log`, `mutations_run.log`. **`reports/stage_a4/gates.md` still reads 46 files / 270 passed and was not refreshed** |
| 27 | net edge per share at 1.40: **−0.003756** close exit, **−0.033756** stop exit; at 2.81: **+0.031369** / **+0.001369** | `README.md:237-238` | see left | modeled | `task5c_dispersion_e2.json::net_edge_rows` |
| 28 | carve-out: **42 sessions read / 28 evaluated**, 2026-07-01 to 2026-08-28, **200 tickers, 1,927,156 bars**, 199 with bars; universe = every **26th** of a **5,317**-name listing over 6 reference pages | `README.md:235-236` | see left | 42 / 28 / 200 | `task5b_post_holdout_pull.json` |
| 29 | duplication screen: **14,002 raw hits across 11 repositories, 0 substantive**, the five design-carrying patterns return **zero** everywhere | `docs/DUPLICATION.md:9-12,51,66-68` | 14002 / 0 / 11 | 11 repos | a shell `grep` recorded verbatim at `docs/DUPLICATION.md:16-28`; **no stored artifact** — the hit counts are not reproducible from anything in the repository |
| 30 | carried structural doubts: **58 percent post-publication decay across 97 predictors from 80 studies**; Concretum **226,000 to 726,000 USD** across four vendors; **76 percent of the replication's filtered profit from 2022 alone**; plain ORB **3.2 percent / Sharpe 0.48** vs top-20-relvol **> 1,600 percent / Sharpe 2.81** | `README.md:447-455`; `HYPOTHESES.md:40,74,76` | see left | — | **all carried, none measured here**; labelled C-2, C-3, C-6, C-10, C-12, C-13 |

---

## 3. Intervals and test statistics

### 3.1 The governing fact

**No confidence interval is reported on any estimate of the hypothesis, and no p-value
appears anywhere in the repository**, because **no in-sample or holdout bar has been read**
and both co-primaries are unrun. The intervals below are (a) percentile/IQR summaries of
descriptive distributions, (b) arithmetic bounds, or (c) one carried range. The "test
statistics" in §3.3 are **planning quantities** — a `t` implied by an assumed Sharpe and a
session count — not statistics computed from a sample.

### 3.2 Every interval reported anywhere

| # | interval | file:line | stated estimator | n | data structure |
|---:|---|---|---|---:|---|
| I1 | **IQR [1.003096, 1.007726]** around a median ratio of 1.005197, described at `HYPOTHESES.md:79` as *"the ratio IQR is 0.46 percentage points wide"* | `README.md:191`; `DECISIONS.md:619`; `task4_tape.json` | **interquartile range, not a confidence interval** — sample quartiles of the per-pair first-5-minute volume ratio | **100** session-ticker pairs (5 sessions × 20 tickers) | paired volume ratios across two redistributors; ADR-022 argues the narrowness itself proves a shared upstream |
| I2 | **rule-of-three one-sided 95 percent upper bound 0.005357** on an ambiguous rate observed **0.000000** | `README.md:261`; `DECISIONS.md:1300-1301` | rule of three, `3/n` | **560** selected name-sessions, 0 events | binary per name-session; the only genuine interval estimate in the repository |
| I3 | **dispersion bracket [2.0294139223208143, 2.029585030455633]**, absolute width 0.000171, **relative width 8.430695548655339e-05** | `README.md:222`; `task5c_dispersion_e2.json` | **a sensitivity bracket over the unmeasured SEC Section 31 rate** (rate = 0 vs rate = measured), not a sampling interval | 550 priced trades | two full re-runs of the same writer |
| I4 | **shift hard bounds 0.030 (all-close) to 0.060 (all-stop)** around a measured 0.041455 | `README.md:262`; `task3_execution_mix.json` | **arithmetic bounds** from the two extreme stop shares, not an interval estimate | 550 | deterministic |
| I5 | **the measured band itself: median → central end, 90th percentile → pessimistic end**, per leg | `REGISTRATION.md:3998-4000`; `DECISIONS.md:1439-1444` | **percentile summary with the assignment fixed in advance**; explicitly *not* mean and *not* maximum | 550 entry / 210 stop / 340 close | per-trade slippage distributions; **lower-bounded** because 457/550 and 195/210 crossings are intrabar and recorded as 0.0 overshoot |
| I6 | entry half spread **median 0.076572, p90 0.333662**; stop **0.031934 / 0.182336**; close **0.040000 / 0.261000**; means 0.131842 / 0.076879 / 0.099324 | `REGISTRATION.md:3988-3996`; `task2_slippage_band.json` | time-weighted quoted half spread per minute; percentile summary | 550 / 210 / 340 minutes, **0 refused** | minute-level NBBO quotes, weighted by time held |
| I7 | **Concretum 226,000 to 726,000 USD** final portfolio value across four vendors | `HYPOTHESES.md:40,80` | **carried range, not measured here**; a spread across vendors, not a CI | 4 vendors | carried, C-13 |

### 3.3 Every test statistic / power quantity reported

| # | quantity | file:line | stated estimator or test | value | n | data structure |
|---:|---|---|---|---:|---:|---|
| T1 | E1 `t` at the registered 1.40 on the computed holdout | `reports/stage_a2/power.md`; `README.md:387-394` | `t = (S/√252)·√n`, one-sided normal approximation | **2.6087459737497545** | 875 | **assumed** Sharpe × session count — not a sample statistic |
| T2 | E1 `t` at 2.81 / 0.70 | `power.json` | same | 5.236126 / 1.304373 | 875 | same |
| T3 | E1 power at α = 0.02532057 | `power.json`; `README.md:393` | `Φ(t − z(1−α))` | 0.9994839 / **0.7435206** / 0.2578024 | 875 | same |
| T4 | E1 power at α = 0.05 | `task1_alpha.json`; `README.md:403-405` | same | 0.9998355 / **0.8324500** / 0.3667473 (holdout); 1.0000000 / 0.9801616 / 0.5816522 (in-sample) | 875 / 1,762 | same |
| T5 | E2 power under the **carried** band | `task4_joint_power.json`; `README.md:265-266` | `Φ((central−shift)/σ·√trades − z(1−α))` | 0.819523805 (2.81) / **0.043276645** (1.40) / 0.001271161 (0.70) | 875 (17,188 trades) | per-trade; **σ cancels in E1 but not here** |
| T6 | E2 power under the **measured** band | `task3_rescue_verdict.json`; `README.md:306` | same | **0.0 / 0.0 / 0.0** | 875 | same |
| T7 | E2 power at `alpha_adj`, pre-replacement (the old rescale-of-E1 E2) | `task5c_dispersion_e2.json`; `README.md:417-421` | `Φ(μ/σ·√trades − z(1−α))` | 0.999484 / **0.743533** / 0.257809 (holdout); 0.959721 / 1.000000 / 0.458773 (in-sample) | 875 / 1,762 | **equals E1 to 5 dp — Amendment 15 records this as a falsified premise of Section 9, not a copy** |
| T8 | JOINT power | `task4_joint_power.json`, `task3_rescue_verdict.json` | `min(E1, E2)`; Fréchet lower bound `max(0, p₁+p₂−1)`; nested-rejection exact | 0.819524 → **0.043277** (carried) → **0.000000** (measured) | 875 | conjunction of two co-primaries; ADR-034 makes this the latch condition |
| T9 | required effect for 80 percent power | `REGISTRATION.md:3692` | `z(0.95) + z(0.80)` | **2.486475** | — | — |
| T10 | minimum n for 80 percent power, E1 | `task1_alpha.json`; `README.md:259` | `⌈((z(1−α)+z(β))/(S/√252))²⌉` | **795** (α = 0.05) vs **1,006** (α = 0.02532057); 198 / 3,180 at 2.81 / 0.70 | — | ceiling, never round |
| T11 | minimum n, E2 and JOINT | `task4_joint_power.json`, `task3_rescue_verdict.json` | `trades_for_e2_power`, returning `Absent` when the pessimistic mean ≤ 0 | **827** at 2.81 carried; **Absent — unreachable at any n** at 1.40 and under the measured band | — | recorded as an absence, not a large number (ADR-026 rule) |
| T12 | the two superseded/corrected alphas | `src/orb/config.py:123-135`; `README.md:255` | `alpha_adj = 1 − 0.95^(1/2) = 0.025320565519103666` (**union**, superseded); `per_test_alpha = 0.05` (**intersection-union test, Berger 1982**) | — | — | ADR-032, Amendment 18 |
| T13 | the **registered but unrun** E1 statistic | `HYPOTHESES.md:75`; `config.py:145-151` | deflated Sharpe **≥ 1.00** on the daily net portfolio return series, **trial count 8** (9 for H1b), skew and kurtosis from the realized series; holdout per-trade `t` gate **2.50** | — | 875 planned | **never computed — no holdout bar read** |
| T14 | the **registered but unrun** E2 statistic | `HYPOTHESES.md:75`; `DECISIONS.md:1202` | mean net PnL per trade, one-sided lower bound > 0 **by permutation on session labels clustered by session date** | — | 17,188 planned | **never computed**; the clustering is why per-trade σ cancels (Amendment 15) |

---

## 4. Provenance claims

Every claim below asserts that something was fixed before the measurement that used it.
"Observed during LOCATE" records only what I read off git objects or file timestamps; it is
**not** an adjudication.

| # | claim (verbatim, abbreviated) | file:line | commit named | what would have to be true | observed during LOCATE |
|---|---|---|---|---|---|
| P1 | *"**The closure was decided by a criterion committed and pushed as `4ae14dc` BEFORE the measurement that decided it**, and the commit order is checkable in `git log`."* | `README.md:30-32`; also `HYPOTHESES.md:58,60`, `DECISIONS.md:1342-1345`, `report.md:879-882`, `REGISTRATION.md:3959-3961,4069`, `HANDOVER.md:52` | `4ae14dc62328cab8a0db486622ab341cd61d2d5a` | `4ae14dc` must precede both the commit containing the measuring tool and the network calls that produced the measurement | `4ae14dc` authored & committed **2026-08-29T20:13:26-07:00**, pushed **20:13:27** (`.git/logs/refs/remotes/origin/main`). It touches **only `REGISTRATION.md` and `progress.md`** (+212 lines). `tools/slippage_band.py` first appears in `5899e1b`, pushed **20:41:14**. First `alpaca:quotes` ledger row **2026-08-30T03:15:35.818Z = 20:15:35 -07:00**, 2 min 8 s after the criterion push; last **03:39:19Z**. |
| P2 | *"Amendment 24 was written, committed and pushed as `4ae14dc` **before a single line of the measuring tool existed**."* | `report.md:879-882`; `REGISTRATION.md:3671-3673` | `4ae14dc` | no `tools/slippage_band.py`, `floor_scan.py` or `rescue_verdict.py` in the tree at `4ae14dc` | `git ls-tree 4ae14dc tools/` returns none of the three. `git log --diff-filter=A` puts all three in `5899e1b`. |
| P3 | *"**`GO` was ruled out arithmetically in that same commit**: it needed a **21.89-fold** reduction in the shift"* | `README.md:32-34`; `REGISTRATION.md:3684-3707` | `4ae14dc` | the 21.89-fold table must be inside the `4ae14dc` diff of `REGISTRATION.md`, not added later | `4ae14dc` adds 96 lines to `REGISTRATION.md`; Amendment 24 §2 (the table) sits inside that block. **Content of the diff not yet line-checked — VERIFY step.** |
| P4 | *"the **assignment of median to the central band end and 90th percentile to the pessimistic end** were all nailed down in advance … fixed in the tool's docstring before it runs"* | `report.md:894-896`; `DECISIONS.md:1369-1373`; `REGISTRATION.md:3998-4000` | (none named) | the assignment must appear in `4ae14dc`, or in some object predating `5899e1b` | The assignment is recorded **inside the result file itself** (`task2_slippage_band.json::assignment_fixed_before_computation`) and inside `tools/slippage_band.py` — **both first appearing in `5899e1b`, the same commit as the result**. So the ordering claim is **self-attested** unless the assignment also appears in `4ae14dc`'s Amendment 24 text. **VERIFY step.** |
| P5 | *"**Its counterfactual still stands: had bar integrity passed in full, the same power inputs fire `DEGRADED`** — exactly what Section 0 predicted **in writing, before any measurement existed**."* | `README.md:85-87`; `report.md:223-228` | (none) | the `DEGRADED` prediction must appear in a registration commit predating the A.2 power computation | `reports/stage_a2/section0.json` carries `counterfactual_if_integrity_passed_in_full: {verdict: "DEGRADED"}`, fired 2026-08-29T02:43:20Z. The registration text predating it is not yet located. **VERIFY step.** |
| P6 | *"the registered Section 6 cost model and its pessimistic band, **registered before any data existed**"* | `HYPOTHESES.md:62`; `report.md:1006-1008` | (none) | `entry/stop/close_slippage_usd` must appear in the first registration commit, before any vendor call | `CONFIG` at `src/orb/config.py:252-254` holds `(0.010,0.020,0.040)`, `(0.020,0.040,0.080)`, `(0.005,0.010,0.020)`. Earliest ledger row is on 2026-08-28; the registration scaffold is `840de7c`/`3c8d836` (`progress.md:15,17`). **VERIFY step.** |
| P7 | *"Frozen `3789221b9dd3fea5a9680547dfdf8ec7b1febaf246042fe1fa70e27ca610fba3`, **latched**, and pinned by a test that recomputes it."* | `report.md:169`; `docs/STAGES.md:18` | (none) | the latch file must hold that hash and a test must recompute it from the canonical bytes | `data/state/cost_model_latch.json` (untracked, read 2026-09-12T18:03Z) holds exactly that sha256 with `measured_on: "2026-08-29"`; `data/state/cost_model.jsonl` records `canonical_bytes: 359`, `recorded_at 2026-08-29T02:32:28.834Z`. |
| P8 | *"A.1 TASK 9 **sealed** the registered probe slice on 2026-08-29 — 480 files, 737,507 bars, 2,400 session-ticker pairs — and the registered **14-calendar-day wait** … runs to **2026-09-12**."* | `README.md:70-77` | (none) | 480 stored files with per-file SHA-256 in the ledger; the re-pull tool must refuse earlier dates | `task9_probe_manifest.json` records 480/737507/2400 and `earliest_eligible_repull: "2026-09-12"`. Live `data/access/sealed_credentialed/` holds **481 `task9_*` files** (480 bar files + `task9_reference_pool.raw`); `seals.jsonl` has 1,978 rows. `tools/repull_probe.py` exists and HANDOVER.md:10-11 claims exit 78. |
| P9 | *"**No vendor coverage, revision, agreement, delisting, trigger-rate or slippage figure in this repo is registered before it is measured.** Every such figure below is named as an A.1 or A.2 measurement target, never as an input."* | `docs/STAGE_A_PROMPT.md:70` | (none) | no such figure may appear as a registered constant | `CONFIG` holds no coverage/revision/agreement/trigger-rate constant. **The slippage band IS a registered constant** (`config.py:252-254`) — but it is registered as a *cost assumption*, and Amendment 26 §8 explicitly declines to move it. **VERIFY step: whether this sentence and the registered band are in tension.** |
| P10 | *"Two planning figures were falsified by measurement in this pass, both **recorded rather than quietly corrected**"* — the pre-period carve-out (0 of 2 credentials serving it) and the 0.55 trigger rate (measured 0.982143) | `README.md:138-144`; Amendments 11 and 15 | (none) | the superseded figures must still be present in the file, struck rather than deleted | `README.md:410-415` carries a struck-through `~~E2 power: Absent in all nine cells~~` with a "left standing because it was true when written" note; `reports/stage_a2/power.json` still carries `e2_power: "Absent"` in all nine rows. |
| P11 | *"**This amendment is numbered 26 and appears in this file after Amendment 27.** Amendment 27 was appended while this amendment's measurement was still running, and `src/orb/dispersion.py` and ADR-038 already referred to this one as 26 in **text that is committed and pushed**. The number is kept … the anomaly is recorded here rather than tidied away by editing pushed text."* | `REGISTRATION.md:3950-3956` | (none) | Amendment 27 must have been appended in an earlier commit than Amendment 26, and `dispersion.py`/ADR-038 must say "26" in that earlier commit | Amendment 27 is at `REGISTRATION.md:3852`, Amendment 26 at `:3944` — file order confirms the out-of-sequence numbering. **Both blocks land in `5899e1b`/`7edeea7`; the intra-commit ordering claim is not checkable from commit boundaries alone. VERIFY step.** |
| P12 | *"**H1b increments the Section 8 deflated-Sharpe trial count from 8 to 9, for H1b. H1's count of 8 is unchanged.**"* | `DECISIONS.md:1392-1394`; `HYPOTHESES.md:105` | (none) | `CONFIG.trial_count` must still read 8 at the anchor | `src/orb/config.py:257` reads `trial_count=8`. ✓ present |
| P13 | *"**No in-sample or holdout bar was ever read. Both latches remain absent.**"* | `README.md:49-50`; `HYPOTHESES.md:63`; `report.md:1018-1019` | (none) | no latch file may exist; no priced-bar read may occur outside a sealed writer | No latch artifact appears under `reports/` or `data/state/`. Guard 5 (`test_no_module_reads_a_priced_bar_field_anywhere`) is claimed to pin it, with two disclosed real catches (`reports/stage_a4/gates.md:29-38`). **VERIFY step: confirm no latch file exists under the live `data/`.** |
| P14 | *"**Storing bars is not reading them** — the probe slice overlaps the holdout from **2026-05-05 to 2026-06-30** as collection, and the Stage D latch continues to govern the holdout in full and has not been written."* | `HYPOTHESES.md:66`; `docs/HANDOVER.md:165-168` | (none) | the 480 sealed files must overlap the holdout window, and nothing outside a sealed writer may parse a price from them | The overlap is **disclosed by the authors**. 314 `task5b_*` and 481 `task9_*` files sit in the live store. |
| P15 | *"**Assistant prior 0.15**, recorded **2026-08-28** before any measurement. **Operator prior 0.30**, label `INDEPENDENT`, recorded **2026-08-29** … the assistant's 0.15 was recorded first and was **visible to the operator** before this number was formed."* | `HYPOTHESES.md:64,83-84`; `report.md:1026-1027`; ADR-020 | (none) | the 0.15 must appear in a commit dated 2026-08-28 and the 0.30 in a later one | Commits on 2026-08-28 exist (reflog: 23:48–23:59 on 08-28). **Diff not yet located. VERIFY step.** The non-blindness is **disclosed by the authors** at `HYPOTHESES.md:84`. |
| P16 | *"**A later reader can verify the ordering in `git log`**: this commit precedes the commit that contains the measuring tool."* | `REGISTRATION.md:3727-3729`; `DECISIONS.md:1345` | `4ae14dc` | same as P1/P2 | Verified in outline: see P1/P2. The `origin/main` reflog also shows the **push** order, which `git log` alone would not. |
| P17 | *"**`CONFIG.entry_slippage`, `stop_slippage` and `close_slippage` are unchanged** at (0.010, 0.020, 0.040), (0.020, 0.040, 0.080) and (0.005, 0.010, 0.020). **This amendment records a measurement beside them; it does not re-register them.**"* | `REGISTRATION.md:4053-4057` | (none) | the config values must be unchanged between the pre-rescue and post-rescue trees | `config.py:252-254` at `f2aa675` holds exactly those triples. `5899e1b` does not touch `src/orb/config.py`. ✓ |
| P18 | *"**Everything above was measured before any credential existed and is left standing.** `n = 1,026` requests charged on 2026-08-29."* | `README.md:181-182` | (none) | the 9-vendor refusal table must predate the credentials | `data/access/sealed/` and `probe_findings.json` have mtimes 2026-08-28 19:13–19:19; `sealed_credentialed/` earliest is 2026-08-29 11:xx. |
| P19 | Inside the artifacts: `criterion_precommitted_on: "2026-08-30"` beside `computed_at: "2026-08-29"` and `measured_at: "2026-08-29"` | `reports/stage_a3rescue/task3_rescue_verdict.json`; `task2_slippage_band.json` | `4ae14dc` | the two date fields must be on the same clock, or the mixture must be explained | **They are on different clocks.** The criterion was pushed 2026-08-29 20:13 **local (−07:00)** = **2026-08-30T03:13Z**; the measurement ran 20:15–20:39 local = 03:15–03:39Z. `criterion_precommitted_on` uses the **UTC** date and `measured_at`/`computed_at` use the **local** date, so the artifacts *read* as if the criterion post-dated the measurement while the underlying order is the reverse. **A reader checking dates rather than reflog times would draw the wrong conclusion. VERIFY/report step.** |
| P20 | *"Run 2026-08-29, STAGE A.-1 TASK 0, **before a single line of design was written.** … **Verdict: CLEAR.** … All 14,002 raw hits across 11 repositories are incidental"* | `docs/DUPLICATION.md:3-12` | (none) | the screen must predate the design commits, and the hit counts must be reproducible | The exact `grep` is recorded verbatim (`:16-28`). **No stored output artifact exists**, and the screened repository set includes `MLCryptoTrader` and `[personal repo, name removed]`, which are outside this audit's scope. |
| P21 | *"mutation 13 … **when this was written the edge had ONE pin and the suite went green** — the InsiderExperiment lesson. A.1 TASK 5 added a second, independent fixture … and the harness now CATCHES it."* | `reports/stage_a2repair/mutations.md:21`; `stage_a4/mutations.md` | (none) | the earlier mutations.md must show mutation 13 uncaught | `reports/stage_a1r/mutations.md` and `stage_a1amend/mutations.md` are present for comparison. **Disclosed by the authors.** |
| P22 | *"**The operator pre-committed to this on 2026-08-30, before the measurement**, and this amendment is the record of that commitment."* | `REGISTRATION.md:3726-3727` | `4ae14dc` | an operator act, not a git object — only the amendment text evidences it | The **commit** is verifiable (P1); the **operator's pre-commitment** is attested only by the amendment the operator's assistant wrote. Nothing outside the repository corroborates it. |

---

## Live-repo access log

**Repository:** `/home/kiros-li/Documents/GitHub/ORBExperiment/`

| | |
|---|---|
| `git status --porcelain` **before** first access | *(empty — clean working tree)* |
| time of that check (UTC) | **2026-09-12T18:01:53Z** |
| `git status --porcelain` **after** last access | *(empty — clean working tree)* |
| time of that check (UTC) | **2026-09-12T18:04:56Z** |
| `HEAD` at both checks | `f2aa675a80fc06b74979040b3028154d1add5ec0` |

**Both status outputs were empty. No pre-existing dirt, and none introduced.**

**Read-only operations performed:**
`git rev-parse HEAD`; `git log --format=… -20`; `git show --stat` on
`4ae14dc`, `5899e1b`, `7edeea7`, `68a1c65`, `34a91b3`, `f2aa675`, `416c1f4`;
`git ls-tree --name-only 4ae14dc tools/`;
`git log --diff-filter=A -- tools/slippage_band.py tools/floor_scan.py tools/rescue_verdict.py`;
`git remote -v`; `git branch -a`; `git reflog show origin/main`;
`cat .git/logs/refs/remotes/origin/main`; `cat .git/packed-refs`;
`git status --porcelain` (twice).

**Untracked data opened read-only** (all under `data/`, plus one root file):
`ls -la` on `/`, `data/`, `data/access/`, `data/access/{fees,robots,sealed,sealed_credentialed}`,
`data/state/`; `wc -l` on `requests.jsonl`, `seals.jsonl`, `carve_out_reads.jsonl`,
`section0.jsonl`, `cost_model.jsonl`; `du -sb sealed_credentialed`;
filename census of `sealed_credentialed` (names only, no file contents);
`ls -la --time-style=full-iso` on `task2q_*.raw` and `task2_quoteprobe*` (**metadata only**);
JSON/JSONL parse of `requests.jsonl` (aggregate counts only), `section0.jsonl`,
`cost_model.jsonl`, `cost_model_latch.json`; `cat .gitignore`;
`cat _PARKED_CHECK_BEFORE_RUNNING`.

**Not opened:** `.env` (seen in `ls -la`, never read). No `.raw` payload, no HTML fee body,
no sealed bar file was opened. No `seals.jsonl` row content was read beyond the line count.

**Modifications made: none.** No file under `/home/kiros-li/Documents/GitHub/ORBExperiment/`
was created, edited, renamed or deleted; no repository script was executed; no git command
that writes was issued.

**Unanchored caveat:** everything in §1.3 was read at **2026-09-12 18:01Z–18:05Z**, fourteen
days after the anchor. `_PARKED_CHECK_BEFORE_RUNNING` is dated **2026-09-02** and postdates
the anchor; it asserts a state (H1b closed, H2 and H3 registered) that the anchored documents
do not contain, and **nothing in it may be used to adjudicate a claim about `f2aa675`.**

**Anchoring caveat:** every claim located here is a claim about `f2aa675` (2026-08-29).
ORBExperiment's last six commits all landed within 33 minutes of each other on the evening of
2026-08-29, and the repository's own binding calendar date — the earliest eligible bar-revision
re-pull — is **2026-09-12, the day this inventory was compiled.** Later commits could add the
revision measurement and change the Section 0 verdict; they could not change the cost-bound
closure, which the documents state is orthogonal to it.
