# VRPExperiment — verification inventory (LOCATE)

**Agent C (referee/verifier). No thesis. This document locates what can be verified; it
adjudicates nothing.**

| | |
|---|---|
| Repository | `VRPExperiment` |
| Anchored SHA | `d37cf6d190dfdaef8e613daf099a507fe1a77dcf` (main, 2026-08-30) |
| Snapshot read | `/home/kiros-li/.cache/program-audit/scratchpad/snap/VRPExperiment/` |
| Live repo touched | `/home/kiros-li/Documents/GitHub/VRPExperiment/` — git objects + untracked `data/` only, read-only |
| Compiled | 2026-09-05, 03:41Z–03:48Z |
| Documents read | `README.md`, `REGISTRATION.md`, `HYPOTHESES.md`, `DECISIONS.md`, `progress.md`, `docs/ARTIFACT.md`, `docs/ACCESS.md`, `docs/COSTS.md`, `docs/HANDOVER.md`, `docs/VENUE_TABLE_UPDATE.md`, `docs/DUPLICATION.md`, `reports/task3/*.md` |
| Not present | There is no `report.md` and no `FINDINGS.md` in this repository; `docs/ARTIFACT.md` is the deliverable and `HYPOTHESES.md` carries the verdict. There is no `registrations/` directory; registration is the single `REGISTRATION.md`. |

Counts: **37 artifact entries** (30 tracked/anchored, 7 untracked/unanchored groups),
**26 numeric claims** ranked with **8 marked MUST-VERIFY**, **4 confidence intervals** and
**31 test / distribution / power entries**, **23 provenance claims**.

---

## 1. Artifacts — every place a number could be verified

### 1.1 Analysis and measurement code (tracked, anchored at `d37cf6d`)

| path | what it holds | which document figures it backs | anchored? |
|---|---|---|---|
| `src/vrp/sealed_read.py` (405 lines) | **The estimator.** `realized_volatility` (close-to-close, `ddof=1`, ×√365); `newey_west_se` (Bartlett kernel, divisor `n`, bandwidth 30); `incomplete_beta`/`student_t_sf`/`student_t_critical` (own implementation, no scipy); `estimate_premium` (mean, t, one-sided p, one-sided CI lower, bps scaling, positive share); `non_overlapping` (stride 30); `bps_per_volatility_point` (√(2/π)·√(30/365)·10⁴); `straddle_delta` (2N(d₁)−1); `count_rebalances` (loop bound gives a **daily maximum of 29** evaluations over a 30-day tenor) | every premium statistic, every CI, every p-value, the 22.875 conversion, the rebalance counts, the "29 maximum" claim | YES |
| `tools/task6_sealed_run.py` (444 lines) | **The driver.** hourly chunking at 40 days; `at_observation_hour` (08:00 UTC filter); `build` (31 closes → 30 returns, forward window, drop rule); `stability` (4 equal parts, default bandwidth 30 on each); `rebalance_distribution` (`median = ordered[n//2]`, `p90 = ordered[round(0.90·(n−1))]`); latch write; fixture mode with planted 0.08 | n construction (1,985 → 1,955), the quarterly split, median/p90 rebalance definitions, the fixture claim | YES |
| `tools/measure_spreads.py` (211 lines) | Deribit ATM straddle bid/ask sampler; emits **differences only** (spread, half-spread, half-spread/notional) | `docs/COSTS.md` §4 reference spreads | YES |
| `tools/probe_deribit.py` (368 lines) | TASK 4 probe: endpoint status, byte/row counts, history bisection, pass-1 rate burst, 5-second revision A/B | `docs/ACCESS.md` §1.1–1.7 | YES |
| `tools/probe_rate_and_revision.py` (229 lines) | Corrected probes: concurrent rate escalation, data-only revision digests | `docs/ACCESS.md` §1.6–1.7 | YES |
| `tools/env_report.py` (57 lines) | Toolchain provenance writer | `reports/env_report.json` | YES |
| `src/vrp/absence.py` (174) | Guard 1 — `Absent` refusing `float()`/`int()`/indexing | every `Absent(not_served)` claim; the "a branch conditioned on a measured cost cannot fire on an absent one" argument | YES |
| `src/vrp/tzguard.py` (114) | Guard 2 — naive datetimes refused | ADR-005 timestamp handling | YES |
| `src/vrp/ledger.py` (122) | Guard 3 — append-only `O_APPEND`+`fsync` ledger | ADR-002 (the guard that fired on `ledger.py:74`) | YES |
| `src/vrp/callstate.py` (125) | Guard 4 — venue states vs health states, `combined_total()` raises | ADR-004, the five venue classifications | YES |
| `src/vrp/fields.py` (148) + `src/vrp/seal.py` (121) | Guard 5 — 38 blind / 40 readable field names, asserted disjoint | ADR-001, ADR-006, the blindness argument for deferring the rebalance count | YES |
| `src/vrp/latch.py` (165) | The latch: module SHA-256 record, `LatchAlreadySpentError` | "the latch is spent and is not re-runnable" | YES |
| `src/vrp/redact.py` (69) | Credential redaction in ledger rows | — | YES |
| `tests/test_guards.py` (28 test functions) + `tests/test_estimators.py` (22) = **50 tests** | Guard canaries and estimator unit tests | the "**50 tests**, mypy strict clean, ruff clean" claim in `README.md:122` and `docs/HANDOVER.md:112` | YES |

### 1.2 Stored result artifacts (tracked, anchored)

| path | what it holds | which document figures it backs | anchored? |
|---|---|---|---|
| `reports/task6/real_attempt2_result.json` (8,547 B) | **The deciding artifact.** Per asset: `n`, `days_paired`, `dropped_incomplete_forward_window`, implied/underlying spans and day counts, `primary_overlapping_hac` (mean vol pts, mean bps, HAC SE, bw, t, one-sided p, CI lower vol pts and bps, positive share), `robustness_non_overlapping_iid` (n=66), `stability_quarters` (4 rows × mean/t/p/positive share), `rebalances` (3 bands × min/median/mean/p90/max/max_abs_drift_median), plus `bps_per_volatility_point = 22.874639`, `attempt: 2`, latch record, `started_at 2026-08-30T06:58:05Z`, `finished_at 06:59:48Z` | **every premium figure** in `README.md:36-49`, `docs/ARTIFACT.md:67-94`, `HYPOTHESES.md:19-23`, `progress.md:718-754` | YES |
| `reports/task6/task6.latch.json` (1,697 B) | Attempt-1 latch, 11 module SHA-256, `written_at 2026-08-30T06:55:35.492Z`, note "TASK 6 single sealed read of Deribit DVOL" | ADR-007, Amendment 1 | YES |
| `reports/task6/task6.latch.2.json` (1,804 B) | Attempt-2 latch, `written_at 06:58:05.858Z`. **All ten `src/vrp` hashes identical to latch 1; only `tools/task6_sealed_run.py` differs** (`baeb131d…` → `47ee85a3…`) | Amendment 1's "only change is one string literal" claim | YES |
| `reports/task6/fixture_result.json` (6,036 B) | Fixture run, `days_requested 300`, planted premium 0.08 vol pts, n=270/asset, recovered means 0.094653 (BTC) and 0.094101 (ETH) | "the identical pipeline against synthetic data with a known planted premium" (`README.md:125`) | YES |
| `reports/task5/commission_bps.json` (1,469 B) | Commission in bps for MET/MBT/BRR/full-ETH options and futures, plus both straddle round trips (`MET 32.5706`, `MBT 4.352`); notionals as 245.62 / 7812.46 | `docs/COSTS.md` §1.2, `docs/ARTIFACT.md:154-171`, the whole cost table | YES |
| `reports/task5/ibkr_ca_commissions.json` (2,590 B) | Parsed IBKR Canada schedule bands per product. *Note for the verifier: several product keys hold six rows where three belong to the futures line and three to the options line, and `MET → ">20,000" → fixed_usd: 5.0` is anomalous — a parse artefact, not used downstream* | `docs/COSTS.md` §1 table | YES |
| `reports/task5/reference_spreads_deribit.json` (40,476 B) | 24 windows × 4 legs; per-leg half-spread and round-trip **full sorted distributions**, median, p90, min, max, mean, quoted/unquoted counts; series metadata (expiry `2026-09-25T08:00:00Z`, days to expiry 26.06, strikes 78,000/2,500, index 78,178.25/2,457.21, 13 expiries, 65/64 strikes); `status: "REFERENCE ONLY"` | `docs/COSTS.md` §4.1–4.4, `docs/ARTIFACT.md:195-205`, ADR-008 | YES |
| `reports/task4/deribit_probe.json` (47,372 B) | 11 endpoint probes (status, bytes, row counts); `history_depth` (22 probes/asset, `deepest_served_days_back 1992`, `first_empty_days_back 1993`, `approx_earliest_served_utc 2021-03-17T06:23:58Z`); pass-1 rate burst (60 sequential, 3.64 req/s, no refusal); revision A/B 5 s apart with `digests_identical: false`, `row_counts_identical: true` | `docs/ACCESS.md` §1.1–1.5, `README.md:86-91` | YES |
| `reports/task4/rate_and_revision_baseline.json` (8,541 B) | Concurrent escalation, 6 steps × 2 endpoints (2+4+8+16+32+64 = **126 requests each**, peaks 126.76 and 120.45 req/s, zero non-200); six revision baselines with data-only SHA-256 and 169 rows each; `retrieved_at 2026-08-30T06:25:49.532Z` | `docs/ACCESS.md` §1.6–1.7 | YES |
| `reports/task4/revision_recheck.json` (4,400 B) | Six windows re-checked, `all_identical: true`, `gap: "≈70 minutes"`, baseline `taken_at ≈06:26:08Z`, `recheck_taken_at ≈07:03:22Z` | `README.md:91`, `docs/ARTIFACT.md:278-281`, ADR-009, `progress.md:818-821` | YES |
| `reports/task3/venue_table.md` (13,009 B) | Spot from two sources, the 8-row venue table, contract specs, sleeve arithmetic, carried-figure re-verification, recorded CME absences | `docs/ARTIFACT.md:111-143`, `HYPOTHESES.md:54-62` | YES |
| `reports/task3/deribit_restricted_jurisdictions_verbatim.md` (3,248 B) | Policy text verbatim, page `<time datetime="2026-03-19T16:49:36Z">`, retrieved `05:13Z`, HTML SHA-256 `ec5a39b7…`, 63,433 bytes, the full jurisdiction list with qualifiers | the **PROHIBITED** classification and the "Canada carries none [of the qualifiers]" claim | YES |
| `reports/task3/robots_and_terms.md` (3,986 B) | 7 robots.txt rows with HTTP/bytes/SHA-256; the CME **HTTP 403** refusal verbatim, 602 bytes, SHA-256 `eecde3fa…`, retrieved `05:27Z` | ADR-003 and every `Absent(not_served)` sourced to CME | YES |
| `reports/env_report.json` (526 B) | `git_head ba5059660423…`, `git_status_porcelain` showing README modified + 5 untracked at generation time, Python 3.13.14, ruff 0.16.5, mypy 2.3.1, pytest 9.1.1 | `docs/HANDOVER.md:112-114` toolchain provenance | YES |

### 1.3 Untracked / gitignored data in the live working tree — **UNANCHORED**

`data/` is gitignored (`.gitignore:1`). Everything below was read from the live tree on
**2026-09-05 at 03:44–03:46Z** by `ls -la`/`stat` and, for the four small JSON series,
by counting keys. It may have changed after the anchor; no large binary was opened.

| path | size | mtime (local PDT / UTC) | what it holds | backs | anchored? |
|---|---|---|---|---|---|
| `data/raw/task6/dvol_BTC_daily.json` | 41,526 B | 2026-08-29 23:58:57 / **2026-08-30T06:58:57Z** | **1,985** daily DVOL closes, 2021-03-24 → 2026-08-29 (first value 82.76) | the entire BTC implied leg | **NO** |
| `data/raw/task6/dvol_ETH_daily.json` | 41,807 B | 23:59:48 / **06:59:48Z** | **1,985** daily DVOL closes, same span (first 93.24) | the entire ETH implied leg | **NO** |
| `data/raw/task6/underlying_BTC_daily.json` | 46,030 B | 23:58:57 / **06:58:57Z** | **1,992** daily perpetual closes, 2021-03-17 → 2026-08-29 (first 55810.0) | the BTC realized leg and every rebalance path | **NO** |
| `data/raw/task6/underlying_ETH_daily.json` | 44,812 B | 23:59:48 / **06:59:48Z** | **1,992** daily perpetual closes, same span (first 1780.7) | the ETH realized leg and rebalance paths | **NO** |
| `data/raw/task5/commissions-futures.html` | **489,783 B** | 23:31 / **06:31Z** | the IBKR Canada futures commission page | `docs/COSTS.md:33` states "**HTTP 200, 489,783 bytes**" — the byte count matches exactly | **NO** |
| `data/raw/task5/commissions-home.html` | 160,443 B | 23:31 / 06:31Z | IBKR commissions landing page | — | **NO** |
| `data/raw/task3/` (14 files, 1.4 MB) | — | 23:13–23:17 / **06:13–06:17Z** | `deribit_restricted_jurisdictions.html` **63,433 B**, `ibkr_ca_mbt_met_options.html` **123,443 B**, `ibkr_ca_micro_bitcoin.html` **120,250 B**, `margin-futures-fops.ca.html` **275,624 B**, `margin-requirements.ca.html` **275,624 B**, `hl_meta.json` **17,495 B**, `cme_refusal.json` **602 B**, plus text renderings and `ibkr_us_mbt_met_options.html` (182,005 B), `margin.ca.html`, `margin-rates.ca.html`, `ibkr_ca_spot_btc_etp.html` | every byte count quoted in `reports/task3/venue_table.md` and `robots_and_terms.md` matches the file on disk | **NO** |
| `data/raw/task4/` (12 JSON, ~100 KB) + `data/raw/task4/alt/` (15 files, **205 MB**) | — | 23:23–23:27 / **06:23–06:27Z** | probe payloads and the six revision snapshots; `alt/` holds `cdd_DeriBit_volatility_OHLC_BTC.csv` **76,979 B**, `…_ETH.csv` **78,058 B**, `okx_opt_summary` **868,306 B**, `bybit_tickers_opt` **427,630 B**, `binance_eoptions` 1,068,850 B, `tardis_api` **210,602,148 B**, and the Laevitas/Amberdata/Volmex refusal bodies | `docs/ACCESS.md` §2 and §2.1 byte counts (CDD, OKX, Bybit all match) | **NO** |
| `data/raw/robots/` (8 files, 84 KB) | — | **earliest 2026-08-29 21:47:24.306 PDT = 2026-08-30T04:47:24Z** | the eight robots.txt bodies | `reports/task3/robots_and_terms.md` byte counts; **and the registration-precedence question** (see §4) | **NO** |
| `_CLOSED_DO_NOT_RUN_HERE` | 747 B | 2026-09-02 22:38 | An operator marker written **after** the anchor, excluded via `.git/info/exclude`. Not repository evidence; recorded so it is not mistaken for one. | — | **NO** |

**Recomputation reach.** The four `data/raw/task6/*.json` files are the complete primitives
of the sealed read. Every premium figure, every CI, every p-value, every quarterly split
and every rebalance distribution in this repository is fully recomputable from them plus
`src/vrp/sealed_read.py`. They are, however, **unanchored**: they are not in git and carry
mtimes, not commit hashes.

**Not stored anywhere.** The hourly row counts quoted as `47,696` DVOL and `47,858`
perpetual (`HYPOTHESES.md:22`, `progress.md:720-721`) appear in **no artifact** — the driver
writes them to stdout only (`tools/task6_sealed_run.py:137-140, 182-185`). They are
recoverable only by re-fetching, which the latch forbids.

---

## 2. Numeric claims, ranked — MUST-VERIFY marked

Ranked by how much rests on them. Ranks 1–8 are marked **MUST-VERIFY** (the brief requires
at least three; the closure's arithmetic needs eight to be checked end to end).

### ★ MUST-VERIFY 1 — the number that decides the closure

> "**The ether premium's point estimate is 119.05 bps. The central,
> commission-only, lower-bound cost is 122.14 bps. The premium does not cover the
> commission.**"
> — `docs/ARTIFACT.md:211-213`; repeated `README.md:23-24`, `HYPOTHESES.md:21`,
> `progress.md:788-790`

Figures: 119.052 bps (ETH mean, n = 1,955) against 122.140 bps (MET straddle 32.571 +
11 × 8.143 = 89.573). Produced by: `reports/task6/real_attempt2_result.json` (ETH
`primary_overlapping_hac.mean_bps`), `reports/task5/commission_bps.json` (32.5706 and
8.1426), and the median rebalance count 11 from the same task-6 JSON. **This is the single
number the VENUE_BLOCKED verdict rests on for the only route the repository claims to have
decided.** The margin is 3.088 bps — 2.5% of the cost figure — so rounding in the notional
($245.62 vs the exact $245.6205) and in the per-rebalance bps matters.

### ★ MUST-VERIFY 2 — the registered hurdle and the "8.57×" failure

> "**Required for HARVESTABLE: 2.0 × 162.853 = 325.706 bps. FAILS BY 8.57×.**"
> — `HYPOTHESES.md:21`; as "fails by 8.6×" at `docs/ARTIFACT.md:215`; as
> "FAILS by 8.57×" at `progress.md:786`

Figures: pessimistic MET total 162.853 bps (32.571 + 16 × 8.143 = 162.859 by direct
arithmetic — the document's 162.853 differs in the third decimal), ×2.0 = 325.706, against
ETH CI lower 38.012 bps; 325.706 / 38.012 = 8.568. n = 1,955 for both the premium and the
p90 rebalance count. Backing: `commission_bps.json` + task-6 JSON + `REGISTRATION.md:312-316`.

### ★ MUST-VERIFY 3 — the BTC premium and its interval

> "**BTC: mean 0.086607 annualised volatility points = 198.111 bps of notional,
> n = 1,955 daily observations**, Newey–West HAC bandwidth 30, SE 0.014709,
> **t = 5.888, one-sided p = 2.297 × 10⁻⁹**, one-sided 95% CI lower bound
> **0.062401 vol points = 142.740 bps**, positive on **73.86%** of observations."
> — `HYPOTHESES.md:19`; same figures `README.md:36-40`, `docs/ARTIFACT.md:67-77`

Backing: `reports/task6/real_attempt2_result.json:12-24`; recomputable from
`data/raw/task6/{dvol,underlying}_BTC_daily.json` through `src/vrp/sealed_read.py`.
It carries the entire "SIGNAL_ABSENT does not fire" leg and is the premium side of the one
route left open.

### ★ MUST-VERIFY 4 — the ETH premium and its interval

> "**ETH: mean 0.052045 vol points = 119.052 bps, n = 1,955**, SE 0.021528,
> **t = 2.418, one-sided p = 7.859 × 10⁻³**, CI lower **0.016618 vol points =
> 38.012 bps**, positive on **64.55%**."
> — `HYPOTHESES.md:19`; `docs/ARTIFACT.md:72-77`

Backing: `real_attempt2_result.json:135-147`. The 38.012 CI lower is the denominator of the
8.57× claim; the 119.052 mean is MUST-VERIFY 1.

### ★ MUST-VERIFY 5 — the rebalance multiplier

> "**rebalances, registered ±0.10 band, 30-day tenor | median 11, p90 16 (BTC max 20,
> ETH max 22) | 1,955 paths per asset**"
> — `README.md:61`; used as the multiplier at `docs/ARTIFACT.md:166-171` and
> `progress.md:780-781`

Figures: median 11, p90 16, n = 1,955 per asset, both assets. Backing:
`real_attempt2_result.json:36-45` (BTC band 0.1) and `:161-168` (ETH band 0.1); computed by
`count_rebalances` (`src/vrp/sealed_read.py:350-405`) driven by
`rebalance_distribution` (`tools/task6_sealed_run.py:237-267`). **89 of the 122.14 bps —
73% of the deciding cost — is this count times 8.143.** The median/p90 index rules are
non-standard (`ordered[n//2]`, `ordered[round(0.90·(n−1))]`) and worth checking against the
registered "median" and "90th percentile" of `REGISTRATION.md:271-274`. Also worth checking:
the count holds σ (the implied at t) and the strike fixed across the whole path while
letting time-to-expiry decay.

### ★ MUST-VERIFY 6 — commission in basis points

> "| **MET option** | $245.62 | $0.20 | **8.143 bps** | **16.285 bps** |" and
> "| **MET** | 4 × $0.20 = **$0.80** | **32.571 bps** | … | **MBT** | 4 × $0.85 =
> **$3.40** | **4.352 bps** |"
> — `docs/COSTS.md:78, 88-89`; `docs/ARTIFACT.md:167`

Figures: 0.20/245.62 × 10⁴ = 8.1426; ×4 = 32.5706; 0.85/7812.46 × 10⁴ = 1.0880; ×4 = 4.352.
Backing: `reports/task5/commission_bps.json`; source rates in
`reports/task5/ibkr_ca_commissions.json` and the live file
`data/raw/task5/commissions-futures.html` (489,783 B, unanchored).

### ★ MUST-VERIFY 7 — the notionals and the two capital thresholds

> "| **Micro Ether option** | **$245.62** | **4.07×** | **407.1% of notional** … |
> **Micro Bitcoin option** | **$7,812.46** | **0.128×** | **12.80% of notional** |"
> — `docs/ARTIFACT.md:142-143`; `reports/task3/venue_table.md:79-80`

Figures: spot BTC $78,124.575, ETH $2,456.205 (Coinbase, n = 1 source used, Kraken
corroborating to 1.16 / 3.24 bps); 0.10 × spot; $1,000 ÷ notional. Backing:
`reports/task3/venue_table.md:9-16`. Every downstream bps figure and both CAPITAL_BLOCKED
determinations ($390,622.88 = 390.6×; $122,810.25 = 122.8×) descend from these two spots.

### ★ MUST-VERIFY 8 — the open route's two thresholds

> "**it clears the registered 2× hurdle by 3.28×**, and would still clear it at the
> maximum possible **29** rebalances … these must total **≤ 49.61 bps of notional**"
> — `docs/ARTIFACT.md:222-231`; `HYPOTHESES.md:26, 62`; `docs/HANDOVER.md:24`

Figures: 142.740 / (2 × 21.760 = 43.520) = 3.279; 142.740/2 − 21.760 = 49.610; the "29" is
the loop bound in `count_rebalances` (`src/vrp/sealed_read.py:382-384`), not a measured
maximum (measured maxima are 20 BTC / 22 ETH at the ±0.10 band). This is the entire content
of the qualification on the closure and of `docs/HANDOVER.md` item 1.

### Ranks 9–26 (not marked MUST-VERIFY)

| # | claim (abridged, verbatim fragments quoted) | file:line | figures / n | believed produced by |
|---|---|---|---|---|
| 9 | "**conversion, registered before any data** \| **1 volatility point = 22.875 bps of notional**"; registration writes "`edge_bps = 2,287.5 × (IV − RV)`" | `README.md:50`; `REGISTRATION.md:164-166` | 22.875 vs the code's **22.874639** | `bps_per_volatility_point`, `sealed_read.py:43-51`; `real_attempt2_result.json:251` |
| 10 | "**47,696 hourly DVOL rows → 1,985 daily observations per asset; 47,858 hourly perpetual rows → 1,992.** Paired: **1,985 days**, of which **30 dropped** … leaving **n = 1,955**" | `HYPOTHESES.md:22`; `progress.md:720-723` | 47,696 / 47,858 / 1,985 / 1,992 / 30 / 1,955 | driver stdout (**not stored**); day counts verifiable against the live `data/raw/task6/*.json` (1,985 and 1,992 confirmed on read) |
| 11 | "**BTC n = 66 non-overlapping windows: 0.096558 vol points = 220.872 bps, t = 4.568, p = 1.128 × 10⁻⁵, CI lower 140.188 bps. ETH n = 66: 0.058053 = 132.793 bps, t = 2.088, p = 0.0203, CI lower 26.688 bps.**" | `HYPOTHESES.md:20`; `docs/ARTIFACT.md:79-83` | n = 66 each | `real_attempt2_result.json:57-69, 180-192`; `non_overlapping(stride=30)` |
| 12 | "**BTC … decays monotonically: 284.53 → 250.59 → 145.13 → 112.72 bps, a 60.4% fall**" | `HYPOTHESES.md:23`; `docs/ARTIFACT.md:96-97`; `docs/HANDOVER.md:83` | 4 quarters, n = 488/488/488/491; 1 − 112.719/284.53 = 0.604 | `real_attempt2_result.json:70-115`; `stability()` |
| 13 | "**ETH … Q3 −18.56 bps, NEGATIVE, p = 0.597**; only one of four quarters is individually significant" | `HYPOTHESES.md:23`; `docs/ARTIFACT.md:93, 100-102` | n = 488 per quarter | `real_attempt2_result.json:193-238` |
| 14 | "**BTC 22.50 bps, ETH 25.00 bps** at the medians … **24 observation windows per leg, 96 observations, zero unquoted**" | `docs/ARTIFACT.md:196-198`; `docs/COSTS.md:253-254` | 4 legs × 24 | `reports/task5/reference_spreads_deribit.json` (BTC 6.25+5.00, ETH 5.00+7.50, doubled) |
| 15 | "**all six fixed windows byte-identical after ≈ 70 minutes**" | `README.md:91`; `docs/ARTIFACT.md:279-281`; `DECISIONS.md:191-192`; `progress.md:818-820` ("recorded at 06:05Z … re-fetched at ~07:15Z") | 6 windows × 169 rows | `reports/task4/revision_recheck.json` — whose own stamps are `taken_at 06:26:08Z` → `recheck_taken_at 07:03:22Z`, a gap of **≈ 37 minutes**, and whose baseline file records `retrieved_at 06:25:49Z`. The "≈70 minutes" is also written into the JSON's own `gap` field. |
| 16 | "**DVOL history depth, bisected** \| **1,992 days** (≈ 2021-03-17) \| 22 probes/asset" | `README.md:87`; `docs/ACCESS.md:89-92`; `docs/ARTIFACT.md:272` | 22 probes/asset | `deribit_probe.json.history_depth`; note the sealed read served DVOL only from **2021-03-24** (1,985 days) and `HYPOTHESES.md:22` states "Implied history begins 2021-03-24, the first date Deribit serves DVOL" |
| 17 | "**no rate refusal at or below 126.76 req/s** — an upper bound *not reached*", "`n = 126` requests each" | `README.md:89`; `docs/ACCESS.md:126-140` | 126 requests/endpoint | `rate_and_revision_baseline.json` (2+4+8+16+32+64 = 126 ✓; peaks 126.76 and 120.45) |
| 18 | "**1,026 BTC option instruments and 876 ETH option instruments**", "9 of 9 valid, HTTP 200 \| 11 probes" | `docs/ACCESS.md:41-49`; `README.md:86-88` | n = 1 enumeration each | `deribit_probe.json.endpoints` (11 rows, 9 valid all 200 ✓) |
| 19 | "**232 perpetual instruments and zero options**, and three separate options-endpoint probes each returned HTTP 422" | `docs/ARTIFACT.md:132-134`; `reports/task3/venue_table.md:27` | n = 232 | `data/raw/task3/hl_meta.json` (17,495 B, unanchored — matches the quoted byte count) |
| 20 | "**32.571 bps** … already exceeds the **entire quoted spread cost** of the same trade on Deribit (**22.50 / 25.00 bps**)" | `docs/ARTIFACT.md:203-205`; `docs/COSTS.md:256-259`; ADR-008 | — | derived from claims 6 and 14 |
| 21 | "**The MET straddle's commission is 7.48× more expensive … purely because MET's notional is 31.8× smaller**" | `docs/COSTS.md:100-102`; `DECISIONS.md:229-232` | — | 32.571/4.352 = 7.484; 7812.46/245.62 = 31.807 |
| 22 | "**BTCY MER 1.28%, ETHY MER 1.29%**" (ETHY management fee 1.10%, MER capped 1.48%) | `README.md:79`; `reports/task3/venue_table.md:28` | 2 funds | fund pages; no machine-readable artifact stores these |
| 23 | "a **strategy-Sharpe endpoint of 1.32 annualised** would need **roughly 119 weekly observations** … **at the halved 0.66 … roughly 478**"; "`730/30 ≈ 24`", "`6.19/d²`", "`d ≈ 0.508`" | `REGISTRATION.md:412-433`; `DECISIONS.md:203-206` | — | arithmetic in the registration itself, checkable in closed form |
| 24 | "**`make all` is green: 50 tests, mypy strict clean, ruff clean**", "mypy strict clean on 17 source files" | `README.md:122`; `docs/HANDOVER.md:112`; `progress.md:835` | 50 tests | `tests/*.py` contain exactly 50 `def test_` functions ✓; `reports/env_report.json` for the toolchain (its `git_head` is `ba50596`, one commit before the anchor) |
| 25 | CDD "**1,986 daily rows** spanning 2021-03-24 → 2026-08-30" vs "byte-identical, including all **1,985** historical rows" | `docs/ACCESS.md:219-220` vs `progress.md:824` | — | `data/raw/task4/alt/cdd_DeriBit_volatility_OHLC_*.csv` (76,979 / 78,058 B, unanchored — byte counts match) |
| 26 | Carried figures re-verified: "MBT … **$6,505** → **$7,812.46** (**+20.1%**)"; "MET **$191** → **$245.62** (**+28.6%**)"; ORB "**0.076572** USD per share … p90 **0.333662**, **n = 550** … **11.27 times**" | `reports/task3/venue_table.md:95-96`; `docs/VENUE_TABLE_UPDATE.md:22-29, 73-74`; `REGISTRATION.md:276-283, 514-518` | n = 550 minutes (ORB) | cross-repository; **not verifiable inside VRPExperiment** — the cited sources are `MLCryptoEngine/report.md:1164-1165`, `MLCryptoEngine/DECISIONS.md:1480`, `ORBExperiment/README.md:300`, `ORBExperiment/reports/stage_a3rescue/task2_slippage_band.json:74` |

---

## 3. Every confidence interval and every test statistic / p-value reported

All intervals are **one-sided 95% lower bounds** (`estimate_premium(..., alpha=0.05)` →
`mean − t_crit(n−1, 0.05) · SE`, `src/vrp/sealed_read.py:287-288`). All tests are the single
registered one-sided t-test of `H₀: mean(VRP) ≤ 0` (`REGISTRATION.md:360-366`), with the
p-value from an own-implementation Student-t survival function
(`sealed_read.py:209-215`), not scipy.

### 3.1 Primary — overlapping daily, Newey–West HAC bandwidth 30

| # | asset | file:line | mean | SE | t | one-sided p | CI lower | n | data structure |
|---|---|---|---|---|---|---|---|---|---|
| 1 | BTC | `HYPOTHESES.md:19`; `README.md:37-39`; `docs/ARTIFACT.md:73-76`; `real_attempt2_result.json:12-24` | 0.086607 vol pts / 198.111 bps | 0.014709 | **5.888** (JSON 5.8879) | **2.297 × 10⁻⁹** (JSON 2.2965959e-09) | 0.062401 / **142.740 bps** | 1,955 | overlapping 30-day forward windows on daily sampling — serial correlation by construction |
| 2 | ETH | same lines; `real_attempt2_result.json:135-147` | 0.052045 / 119.0521 bps | 0.021528 | **2.418** (2.4175) | **7.859 × 10⁻³** (0.0078585401) | 0.016618 / **38.012 bps** | 1,955 | same |

### 3.2 Registered robustness — non-overlapping, IID (bandwidth 0)

| # | asset | file:line | mean | SE | t | p | CI lower | n | structure |
|---|---|---|---|---|---|---|---|---|---|
| 3 | BTC | `HYPOTHESES.md:20`; `docs/ARTIFACT.md:81`; JSON `:57-69` | 0.096558 / 220.872 bps | 0.021138 | **4.568** (4.5679) | **1.128 × 10⁻⁵** | 0.061285 / **140.188 bps** | **66** | every 30th observation (`premium[::30]`), IID by construction |
| 4 | ETH | `HYPOTHESES.md:20`; `docs/ARTIFACT.md:82`; JSON `:180-192` | 0.058053 / 132.793 bps | 0.027798 | **2.088** (2.0883) | **0.0203** (0.0203446729) | 0.011667 / **26.688 bps** | **66** | same |

### 3.3 Stability quarters — same estimator, HAC bandwidth 30 on each quarter

| # | asset · quarter | file:line | mean bps | t | one-sided p | positive share | n |
|---|---|---|---|---|---|---|---|
| 5 | BTC Q1 2021-03-24→2022-07-24 | `docs/ARTIFACT.md:91`; JSON `:71-81` | +284.53 | 3.498 | 0.00025559579 | 0.7541 | 488 |
| 6 | BTC Q2 →2023-11-24 | `:92`; JSON `:82-92` | +250.587 | 3.845 | 6.8209193e-05 | 0.7561 | 488 |
| 7 | BTC Q3 →2025-03-26 | `:93`; JSON `:93-103` | +145.132 | 2.619 | 0.0045517941 | 0.7418 | 488 |
| 8 | BTC Q4 →2026-07-30 | `:94`; JSON `:104-114` | +112.719 | 2.098 | 0.0182154177 | 0.7026 | 491 |
| 9 | ETH Q1 | `:91`; JSON `:194-204` | +146.27 | 1.056 | **0.1458287911 (n.s.)** | 0.6455 | 488 |
| 10 | ETH Q2 | `:92`; JSON `:205-215` | +291.212 | 4.037 | 3.1428446e-05 | 0.7889 | 488 |
| 11 | ETH Q3 | `:93`; JSON `:216-226` | **−18.556** | **−0.246** | **0.5969522477** | 0.5369 | 488 |
| 12 | ETH Q4 | `:94`; JSON `:227-237` | +57.659 | 0.803 | **0.2110850063 (n.s.)** | 0.611 | 491 |

*(No multiplicity adjustment is applied to the four-quarter split; the registration's
Berger 1982 note at `REGISTRATION.md:381-393` addresses the conjunction endpoint, not the
stability sub-tests.)*

### 3.4 Fixture-run statistics (machinery verification, not a finding)

| # | label | file | mean bps | SE | t | p | CI lower bps | n |
|---|---|---|---|---|---|---|---|---|
| 13 | BTC fixture | `reports/task6/fixture_result.json` | 216.5144 | 0.022154 | 4.2725 | 1.3422673e-05 | 132.8716 | 270 |
| 14 | ETH fixture | same | 215.2530 | 0.012689 | 7.4162 | 7.8820688e-13 | 167.3465 | 270 |

*(planted premium 0.08 vol pts = 183.0 bps; recovered means are 0.094653 and 0.094101 vol
points. No document states a recovery tolerance, so this is recorded as an artifact fact,
not a claim.)*

### 3.5 Distributional statistics reported with an n (not tests)

| # | quantity | file:line | median | p90 | min / max | n |
|---|---|---|---|---|---|---|
| 15 | Deribit BTC call half-spread | `docs/COSTS.md:224` | 6.25 bps | 7.50 | 5.0 / 10.0 | 24 |
| 16 | Deribit BTC put half-spread | `:225` | 5.00 | 7.50 | 5.0 / 7.5 | 24 |
| 17 | Deribit ETH call half-spread | `:226` | 5.00 | 7.50 | 5.0 / 7.5 | 24 |
| 18 | Deribit ETH put half-spread | `:227` | 7.50 | 10.00 | 5.0 / 12.5 | 24 |
| 19–24 | rebalance counts, BTC at bands 0.05 / 0.10 / 0.20 | `README.md:61-62`; JSON `:25-56` | 17 / 11 / 5 | 21 / 16 / 9 | 4–26 / 2–20 / 0–14 | 1,955 each |
| 25–30 | rebalance counts, ETH at the same three bands | JSON `:148-179` | 17 / 11 / 5 | 22 / 16 / 9 | 3–26 / 2–22 / 1–16 | 1,955 each |
| 31 | spot cross-source disagreement | `reports/task3/venue_table.md:11-12` | BTC 1.16 bps, ETH 3.24 bps | — | — | 2 sources per asset |

### 3.6 Power statements (design-stage, no data)

`REGISTRATION.md:426-433`: effective independent sample `730/30 ≈ 24`;
`n ≈ (1.645 + 0.842)²/d² = 6.19/d²` for 80% power at one-sided α = 0.05;
detectable `d ≈ 0.508` at 24 effective observations, `d ≈ 1.016` needing `n ≈ 6` at the
halved effect. `REGISTRATION.md:412-416`: `years = (2/1.32)² = 2.296` → 119.4 weeks;
`(2/0.66)² = 9.183` → 477.5 weeks.

---

## 4. Provenance claims

Each row: the claim verbatim, where it is, the commit named, and what would have to be true.
Where I established a fact from a git object or a file mtime during this LOCATE pass, it is
stated; nothing here is a verdict.

| # | claim (verbatim) | file:line | commit named | what would have to be true | observed during LOCATE |
|---|---|---|---|---|---|
| P1 | "**Registered 2026-08-30, before any network call.** Commit `8bcc5bf` is the last commit before this file; no probe, fetch or measurement precedes it." | `REGISTRATION.md:3-5` | `8bcc5bf` | `REGISTRATION.md` first appears in a commit whose parent is `8bcc5bf`, and no fetched artifact predates that commit | `REGISTRATION.md` is added (533 lines) in `7827592`, parent `8bcc5bf` ✓. Commit time `2026-08-29 21:47:08 PDT` = **04:47:08Z**. Earliest artifact in `data/` is `robots/www.deribit.com.robots.txt`, mtime **04:47:24.306Z** — 16 seconds later. `data/` holds nothing older. |
| P2 | "`REGISTRATION.md`, commit `7827592`, **before any network call**." | `HYPOTHESES.md:18`; `docs/HANDOVER.md:95` | `7827592` | same as P1 | `7827592` = `78275921ca8f4cad72fd7bf2f10155dcf58cb507`, "docs: TASK 2 — REGISTRATION.md, committed before any network call" ✓ |
| P3 | "`REGISTRATION.md` \| Sections 0–9, committed **before any network call**; Amendment 1" | `README.md:102` | — | Sections 0–9 are byte-identical from `7827592` to the anchor | `git diff 7827592 ef07f19 -- REGISTRATION.md` touches **only** the Amendment-log block (a 2-line replacement plus the appended Amendment 1); no section above it changes. `REGISTRATION.md` has no other commit. |
| P4 | "Any amendment is appended here with its date, its reason, and the commit that introduced it. **No section above is edited in place.**" | `REGISTRATION.md:531-533` | — | as P3 | as P3 |
| P5 | "**Measured 2026-08-30, 04:32Z–05:35Z.** Every classification below is evidenced by published text recorded with its URL and its date." | `reports/task3/venue_table.md:3` | — | TASK 3's measurements begin at 04:32Z | This start time **precedes the registration commit at 04:47:08Z**. The earliest network artifact on disk is 04:47:24Z, and the TASK 3 page captures carry mtimes 06:13:57Z–06:17:54Z (their in-document retrieval stamps read 05:13Z / 05:15Z / 05:27Z). The header, the in-document stamps and the file mtimes disagree with one another by up to ~60 minutes. |
| P6 | "### 2.6 The conversion to basis points, **registered before any number exists** … **One volatility point is 22.875 bps of notional.**" | `REGISTRATION.md:152-166` | — | the conversion is in `7827592` and unchanged | present in `7827592`; unchanged (P3). Code emits 22.874639 (`sealed_read.py:43-51`). |
| P7 | "Registered before any data so the rebalance count is not a free parameter: … resized whenever the position delta moves more than ±0.10 … additionally reported at **±0.05 and ±0.20**" | `REGISTRATION.md:285-297` | — | §4.3 is in `7827592`; the implemented bands are exactly 0.05/0.10/0.20 with 0.10 primary | in `7827592` ✓; `tools/task6_sealed_run.py:405-408` sweeps `(0.05, 0.10, 0.20)` ✓ |
| P8 | "with **the statistic assigned to each end registered here, before anything downstream is computed**" (central = median, pessimistic = p90) | `REGISTRATION.md:266-274` | — | the central/pessimistic assignment predates any cost number | in `7827592` ✓; applied as 11 (median) / 16 (p90) in `docs/ARTIFACT.md:168-171` |
| P9 | "**For HARVESTABLE, the lower bound of the premium's one-sided 95% confidence interval must exceed the PESSIMISTIC end of the all-in round-trip cost by a factor of 2.0.** … **Registered before any number exists**" | `REGISTRATION.md:308-316` | — | the 2.0 factor predates the measurement | in `7827592` ✓ |
| P10 | "**Newey–West HAC with bandwidth 30** … **Registered before any data, not after an audit.**" | `REGISTRATION.md:366-371` | — | bandwidth 30 predates the sealed read | in `7827592` ✓; `sealed_read.py:267` defaults `bandwidth = TENOR_DAYS = 30` |
| P11 | "**Robustness, registered now:** the same test on **non-overlapping** 30-day windows … **If they disagree in sign or significance, the disagreement is the finding**" | `REGISTRATION.md:372-375` | — | the robustness rule predates the result; and the disagreement clause was correctly evaluated | in `7827592` ✓; `HYPOTHESES.md:20` asserts agreement and that the clause "is not triggered" |
| P12 | "**Fallback, registered now so it is not chosen later** … The fallback is recorded as used or not used; it is never blended with the primary." | `REGISTRATION.md:95-100` | — | the fallback is recorded as used or not used | `docs/ACCESS.md:268-270` records it **not used** ✓ |
| P13 | "> **POPULATED BY TASK 3. NOT BEFORE.** > **This section registers the criterion. It registers no venue and no figure.**" | `REGISTRATION.md:179-181` | — | §3 as committed carries no venue finding and no number | in `7827592`, §3 contains only criteria and a candidate list ✓ |
| P14 | "> **POPULATED BY TASK 5. NOT BEFORE.** > **No carried figure is registered in this section. None.**" | `REGISTRATION.md:246-247` | — | §4 as committed carries no cost figure | in `7827592`, §4 contains only obligations and the ORB precedent narrative ✓ |
| P15 | "Assistant prior 0.12 / **0.76** / 0.12 … **recorded 2026-08-30 before any network call**" | `HYPOTHESES.md:17`; `REGISTRATION.md:477-497` | `7827592` | the prior table is in `7827592` and unchanged | present in `7827592` §9.1 ✓; unchanged (P3) |
| P16 | "### 9.2 Operator prior > **RESERVED — EMPTY.** … the absence is recorded as an absence rather than backfilled" | `REGISTRATION.md:499-506`; `HYPOTHESES.md:92` | — | the slot is still empty at the anchor | empty at `d37cf6d` ✓ |
| P17 | "At 2026-08-30T06:55:35.492Z the TASK 6 latch was written to `reports/task6/task6.latch.json`, recording the SHA-256 of all ten `src/vrp` modules and of the run tool, **at commit `adac707`**." | `REGISTRATION.md:537-539` | `adac707` | the latch file's `written_at` matches; the module hashes match the blobs at `adac707` | `task6.latch.json` `written_at = 2026-08-30T06:55:35.492Z` ✓, 11 hashes present ✓. Hash-to-blob comparison not performed in this LOCATE pass. |
| P18 | "the only change between attempt 1 and attempt 2 is a **single string literal** in a request parameter — `"3600"` to `"60"` — plus the attempt-numbering that keeps the first latch. **No estimator, no window, no estimator parameter, no tenor, no sign convention and no inference rule was touched.** The diff is auditable in the commit that precedes attempt 2." | `REGISTRATION.md:578-584`; ADR-007 at `DECISIONS.md:149-155` | `ef07f19` (precedes attempt 2) | the `adac707..ef07f19` diff of the driver contains only that literal plus attempt plumbing, and `src/vrp/**` is untouched | `git diff adac707 ef07f19` touches `REGISTRATION.md`, `reports/task6/fixture_result.json`, `reports/task6/task6.latch.json`, `tools/task6_sealed_run.py` — **no `src/vrp` file**. The driver diff is: `"resolution": "3600"` → `"60"` (plus a comment), a new `latch_path(attempt)` helper, an `--attempt` argument, and the output-name suffix. The two latch files confirm all ten `src/vrp` hashes are identical and only `task6_sealed_run.py` differs. |
| P19 | "**No estimator ran.** `reports/task6/real_result.json` does not exist." | `REGISTRATION.md:560-563` | — | that path exists nowhere in history or the worktree | `git log --all --name-only` finds no `real_result.json`; the worktree's `reports/task6/` holds only `fixture_result.json`, `real_attempt2_result.json`, and the two latches ✓ |
| P20 | "**No data was written.** `data/raw/task6/` was empty after the abort." | `REGISTRATION.md:564-566` | — | the four raw series files date from attempt 2, not attempt 1 | live mtimes are 06:58:57Z (BTC pair) and 06:59:48Z (ETH pair) — after the attempt-2 latch at 06:58:05.858Z and matching `finished_at 06:59:48Z`. Consistent; unanchored. |
| P21 | "Section 2.5 registered 'one observation per calendar day, at a **fixed UTC instant** … fixed at the first read and never moved.' **The instant is fixed here, before the TASK 6 latch, at 08:00 UTC**" | `docs/ACCESS.md:275-280`; ADR-005 at `DECISIONS.md:93-111` | — | the timestamp-only probe establishing the 00:00/08:00 misalignment predates the latch, and 08:00 is Deribit's settlement instant | `docs/ACCESS.md` §6 was appended to `ACCESS.md` in `adac707` (the TASK 6 machinery commit, 23:55:29 PDT = 06:55:29Z), **26 seconds before** the attempt-1 latch at 06:55:35.492Z. The settlement claim is corroborated by `reference_spreads_deribit.json` (`expiry_utc 2026-09-25T08:00:00+00:00`). |
| P22 | "Measure it, label it **REFERENCE ONLY, not a cost input**, and let no verdict read it." | ADR-008 at `DECISIONS.md:165-167`; `docs/COSTS.md:186-192`; `reference_spreads_deribit.json.status` | — | no Deribit spread enters any verdict arithmetic | the verdict arithmetic in `HYPOTHESES.md:21` and `progress.md:777-786` uses only commission figures ✓ |
| P23 | "**The TASK 6 latch is spent and is not re-runnable.** `--mode real` raises `LatchAlreadySpentError`." | `README.md:124`; `docs/HANDOVER.md:69-72` | — | `Latch.write` refuses a second write to an existing path | `src/vrp/latch.py` (165 lines) implements it; note that `latch_path(attempt)` gives a *new* path per `--attempt`, so re-running is barred per-latch-file rather than per-repository |

**Also recorded, not a claim by the repository:** the duplication screen
(`docs/DUPLICATION.md:3`) is dated `2026-08-30T04:33Z`, before the registration commit at
04:47:08Z. Its method is `grep -rniI` over local repositories, i.e. not a network fetch, so
it does not bear on P1.

---

## Live-repo access log

Every access to `/home/kiros-li/Documents/GitHub/VRPExperiment/` in this task was
read-only: `git log`/`show`/`diff`/`rev-parse`/`branch`/`status`, `ls -la`, `stat`,
`find -printf`, `du`, and `json.load` on four ~45 KB JSON files under `data/raw/task6/`.
No file in the repository was opened for writing. No `.env`, keystore, session, credential
or token file was opened; `.env.example` is empty and tracked. No repository script was
executed. No large binary was opened (`data/raw/task4/alt/tardis_api`, 210,602,148 B, was
listed only).

**`git -C /home/kiros-li/Documents/GitHub/VRPExperiment status --porcelain`, BEFORE first
access — 2026-09-05T03:41:51Z:**

```
```

(empty — exit 0, working tree clean)

**`git -C /home/kiros-li/Documents/GitHub/VRPExperiment status --porcelain`, AFTER last
access — 2026-09-05T03:48:16Z:**

```
```

(empty — exit 0, working tree clean)

No modification was made and none is reported. `HEAD` at both checks was
`d37cf6d190dfdaef8e613daf099a507fe1a77dcf`, matching the anchored SHA.

Unanchored reads (untracked/gitignored working-tree data), all at **2026-09-05
03:44Z–03:46Z**: `data/raw/task6/*.json` (contents), and directory listings/mtimes for
`data/raw/{robots,task3,task4,task5,task6}` and the repository root. These paths are not in
git and may have changed since the 2026-08-30 anchor.
