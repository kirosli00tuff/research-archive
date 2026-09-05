# VRPExperiment — verification (VERIFY)

**Agent C (referee/verifier). No thesis.** This document reports what the numbers, the code, the
stored data and the git objects actually support. A verified claim is recorded as plainly as a
contradicted one, and "unverifiable" is recorded as itself rather than guessed at.

| | |
|---|---|
| Repository | `VRPExperiment` |
| Anchored SHA | `d37cf6d190dfdaef8e613daf099a507fe1a77dcf` (main, 2026-08-30) |
| Snapshot read | `/home/kiros-li/.cache/program-audit/scratchpad/snap/VRPExperiment/` |
| Live repo touched | `/home/kiros-li/Documents/GitHub/VRPExperiment/` — git objects and untracked `data/` only, read-only |
| Work dir | `/home/kiros-li/.cache/program-audit/scratchpad/work/agentC-vrp-verify/` |
| Verified | 2026-09-05, 03:57Z–04:09Z |
| Inventory used | `findings/agentC/verification/VRPExperiment.inventory.{md,json}` (this agent's own) |

## Result in one line

**101 items checked: 93 VERIFIED, 4 CONTRADICTED, 4 UNVERIFIABLE.** Every number that decides
the closure reproduces — exactly, to every stored decimal, from the raw series through an
independently written implementation of the registered estimators. The four contradictions are a
misstated re-check interval, a misstated measurement window, a units label wrong by 100×, and the
characterisation (not the arithmetic) of the ETH point-estimate comparison. **None of them moves
the verdict.**

### The strongest thing I can say about this repository

The chain from raw data to closure is closed and it holds.

* `reports/task6/task6.latch.2.json` records the SHA-256 of all eleven participating modules.
  **All eleven match the snapshot at the anchored SHA byte for byte** — the code I read is the code
  that ran.
* Running my own implementation of the registered estimators (numpy + scipy's Student-t, not the
  repository's own incomplete-beta) over the four raw series reproduces **every figure in
  `real_attempt2_result.json` to its full stored precision** for both assets: the means to 6 dp,
  the HAC standard errors to 6 dp, the t statistics to 4 dp, the one-sided p-values to **11
  significant figures**, the CI lower bounds, the positive shares, all eight quarterly rows, both
  non-overlapping rows, and all six rebalance distributions including min, median, mean, p90, max
  and the median max-drift.
* The deciding cost arithmetic — 32.570638 + 11 × 8.142659 = **122.139891 bps**, and
  2 × (32.570638 + 16 × 8.142659) = **325.706376 bps** — reproduces exactly from the stored USD
  rates and notionals, and the notionals reproduce from the two measured spot prices.
* Every quoted byte count and both quoted SHA-256 digests of the TASK 3 captures match the files
  on disk (`deribit_restricted_jurisdictions.html`, 63,433 B, `ec5a39b737030785…`;
  `cme_refusal.json`, 602 B, `eecde3fafbde4090…`).
* The attempt-1 → attempt-2 diff is exactly what Amendment 1 says it is: `"3600"` → `"60"` on one
  endpoint, plus attempt plumbing, and **no file under `src/vrp/` is touched**.

The raw series are gitignored and therefore unanchored, but a 2-asset × ~40-figure exact match
against the tracked result JSON authenticates them for practical purposes.

---

## 1. Claims table

`SoT` = source of truth. Tolerances are stated per row. Full machine-readable rows, with every
field the brief asks for, are in `VRPExperiment.claims.json`.

### 1.1 The eight MUST-VERIFY claims

| # | claim (abridged) | file:line | stated | SoT | recomputed | tol | status |
|---|---|---|---|---|---|---|---|
| **MV1** | "The ether premium's point estimate is **119.05 bps**. The central, commission-only, lower-bound cost is **122.14 bps**. The premium does not cover the commission." | `docs/ARTIFACT.md:212-213` | 119.05 vs 122.14 | `task6/real_attempt2_result.json:141`; `task5/commission_bps.json:53,5`; median 11 at `:163`; raw series | premium **119.0521**; cost **122.139891** = 32.570638 + 11 × 8.142659; gap **3.0878 bps** | ±0.001 bps | **VERIFIED** (arithmetic). See DRAFT-V-1 on the characterisation |
| **MV2** | "Required for HARVESTABLE: **2.0 × 162.853 = 325.706 bps. FAILS BY 8.57×.**" | `HYPOTHESES.md:21` | 162.853 / 325.706 / 8.57× | `commission_bps.json`; p90 16 at `:167`; ETH CI lower 38.0124 at `:136`; `REGISTRATION.md:312-316` | **162.853188**; **325.706376**; **8.5684×** | ±0.001 bps, ±0.01× | **VERIFIED** |
| **MV3** | BTC "mean 0.086607 … = **198.111 bps**, n = 1,955, HAC bw 30, SE 0.014709, **t = 5.888**, p = **2.297 × 10⁻⁹**, CI lower **142.740 bps**, positive **73.86%**" | `HYPOTHESES.md:19` | as quoted | `real_attempt2_result.json:12-24` + full recomputation from `data/raw/task6/*_BTC_daily.json` | mean 0.0866070, SE 0.0147090, t 5.8879, p 2.2965959114e-09, CI 0.0624010 = 142.7401 bps, pos 0.738619, n 1955 | exact to every stored decimal | **VERIFIED** |
| **MV4** | ETH "mean 0.052045 = **119.052 bps**, n = 1,955, SE 0.021528, **t = 2.418**, p = **7.859 × 10⁻³**, CI lower **38.012 bps**, positive **64.55%**" | `HYPOTHESES.md:19` | as quoted | `real_attempt2_result.json:135-147` + full recomputation | mean 0.0520450, SE 0.0215280, t 2.4175, p 7.8585401067e-03, CI 0.0166180 = 38.0124 bps, pos 0.645524, n 1955 | exact | **VERIFIED** |
| **MV5** | "rebalances, registered ±0.10 band … **median 11, p90 16** (BTC max 20, ETH max 22) … 1,955 paths per asset" | `README.md:61` | as quoted | `real_attempt2_result.json:36-45, 159-168`; `sealed_read.py:350-405`; `task6_sealed_run.py:237-267` | BTC 2/11/10.8077/16/20; ETH 2/11/10.9913/16/22; n 1955 each; `days_evaluated = 29` on every path | exact integers | **VERIFIED** |
| **MV6** | "MET option $245.62 $0.20 **8.143** **16.285**"; "MET 4 × $0.20 = $0.80 **32.571**"; "MBT 4 × $0.85 **4.352**" | `docs/COSTS.md:78, 88-89` | as quoted | `task5/commission_bps.json` | 8.142659 / 16.285319 / 32.570638 / 4.352022 / 1.088006 | ±0.0005 bps | **VERIFIED** |
| **MV7** | "Micro Ether option **$245.62** **4.07×** **407.1%** … Micro Bitcoin option **$7,812.46** **0.128×** **12.80%**" | `docs/ARTIFACT.md:142-143` | as quoted | `reports/task3/venue_table.md:11-12, 79-82` | 245.6205 / 7812.4575 / 390622.875 / 122810.25; 4.0713× (407.1%); 0.128001 (12.80%); 390.62×; 122.81%; 0.256%; 0.814% | ±0.01 | **VERIFIED** |
| **MV8** | "clears the registered 2× hurdle by **3.28×**, and would still clear it at the maximum possible **29** rebalances … must total **≤ 49.61 bps**" | `docs/ARTIFACT.md:222-231` | 3.28× / 29 / 49.61 | `real_attempt2_result.json:13`; `commission_bps.json`; loop bound `sealed_read.py:382-384` | 142.7401/43.520223 = **3.2799×**; at 29 rebalances 35.904184 bps, 2× = 71.808368 ≤ 142.7401 (still clears, by 1.99×); 142.7401/2 − 21.760111 = **49.6099 bps**; `days_evaluated = 29` empirically on all 3,910 paths | ±0.01 | **VERIFIED** |

### 1.2 Claims 9–26 (inventory ranks), plus five added rows

| claim (abridged) | file:line | recomputed | status |
|---|---|---|---|
| "1 volatility point = **22.875 bps**" | `README.md:50` | √(2/π)·√(30/365)·10⁴ = 2287.4639 per decimal unit = **22.8746** per vol point; 22.875 is that rounded | **VERIFIED** |
| "1,985 daily observations … 1,992 … 30 dropped … **n = 1,955**" | `HYPOTHESES.md:22` | 1985 / 1985 / 1992 / 1992, dropped 30, n 1955, span 2021-03-24 → 2026-07-30, all four series exact | **VERIFIED** |
| "**47,696** hourly DVOL rows … **47,858** hourly perpetual rows" | `HYPOTHESES.md:22` | stdout-only; stored in no artifact | **UNVERIFIABLE** |
| BTC non-overlapping n = 66: 220.872 bps, t 4.568, p 1.128e-5, CI 140.188 | `HYPOTHESES.md:20` | 0.096558 / 220.8720 / SE 0.021138 / t 4.5679 / p 1.1279134941e-05 / CI 140.1876 / pos 0.742424 | **VERIFIED** |
| ETH non-overlapping n = 66: 132.793 bps, t 2.088, p 0.0203, CI 26.688 | `HYPOTHESES.md:20` | 0.058053 / 132.7930 / SE 0.027798 / t 2.0883 / p 2.0344672901e-02 / CI 26.6879 / pos 0.666667 | **VERIFIED** |
| BTC "decays monotonically: 284.53 → 250.59 → 145.13 → 112.72 bps, a **60.4%** fall" | `HYPOTHESES.md:23` | 284.530 / 250.587 / 145.132 / 112.719; 1 − 112.719/284.53 = **0.60384**; n 488/488/488/491 | **VERIFIED** |
| ETH "Q3 −18.56 bps, NEGATIVE, p = 0.597; only one of four quarters is individually significant" | `HYPOTHESES.md:23` | 146.270 (p 0.1458288) / 291.212 (3.1428e-5) / −18.556 (0.5969522) / 57.659 (0.2110850); exactly one below α = 0.05 | **VERIFIED** |
| "**BTC 22.50 bps, ETH 25.00 bps** at the medians … 24 windows per leg, 96 observations, zero unquoted" | `docs/ARTIFACT.md:196-198` | 12.5 + 10.0 = 22.5; 10.0 + 15.0 = 25.0; 4 × 24 = 96; `windows_unquoted` 0 on every leg; the tabulated full distributions at `COSTS.md:224-227` reproduce the stored means exactly | **VERIFIED** |
| "all six fixed windows byte-identical after **≈ 70 minutes**" | `README.md:91` | identity **verified** (6/6 digests and row counts equal); the gap is **37.23–37.24 minutes** on every window | **CONTRADICTED** — DRAFT-V-2 |
| "DVOL history depth, bisected \| **1,992 days** … 22 probes/asset" | `README.md:87` | 22 stored probes per asset, deepest 1992, first empty 1993, earliest 2021-03-17T06:23:58Z / 06:24:06Z | **VERIFIED** |
| "no rate refusal at or below **126.76 req/s** … **n = 126** requests each" | `README.md:89` | 2+4+8+16+32+64 = 126 per endpoint; 0 non-200 across 12 steps; peaks 126.76 and 120.45; the whole per-step table at `ACCESS.md:128-133` matches | **VERIFIED** |
| "**1,026** BTC and **876** ETH option instruments … 9 of 9 valid \| 11 probes" | `docs/ACCESS.md:41-49` | 11 endpoint rows, 9 × HTTP 200 and 2 deliberate 400s with verbatim refusal payloads; row counts 1026 / 876 | **VERIFIED** |
| "**232 perpetual instruments and zero options**" | `docs/ARTIFACT.md:132` | `hl_meta.json` universe length **232**, zero option-shaped names; file is 17,495 B as quoted (**unanchored**) | **VERIFIED** |
| "32.571 bps … already exceeds the entire quoted spread cost … (22.50 / 25.00 bps)" | `docs/ARTIFACT.md:203-205` | 32.570638 > 25.0 > 22.5; and no Deribit spread appears anywhere in the verdict arithmetic (ADR-008 respected) | **VERIFIED** |
| "**7.48×** more expensive … notional is **31.8×** smaller" | `docs/COSTS.md:100-102` | 7.4840 and 31.8071 | **VERIFIED** |
| "BTCY MER **1.28%**, ETHY MER **1.29%**" | `README.md:79` | no artifact holds these; the fund pages were not captured under `data/raw/` | **UNVERIFIABLE** |
| Sharpe/power arithmetic: 119.4 / 477.5 weeks, 6.19/d², d ≈ 0.508 | `REGISTRATION.md:412-433` | 119.375 / 477.502 / 6.18517 / 0.50786; 1.016 = 2 × 0.508; 6.19/1.016² = 5.997 | **VERIFIED** (components; see note) |
| "**50 tests**", "mypy strict clean on 17 source files" | `README.md:122`, `docs/HANDOVER.md:112` | 28 + 22 = **50** `def test_`; 10 + 5 + 2 = **17** source files | **VERIFIED** |
| "mypy strict clean, ruff clean" (the pass/fail itself) | `README.md:122` | not run — read-only rule | **UNVERIFIABLE** |
| CDD "**1,986 daily rows**" vs "all **1,985** historical rows" | `docs/ACCESS.md:219` / `progress.md:824` | 1,988 lines = 1 provenance + 1 header + **1,986** data rows; byte counts 76,979 / 78,058 match exactly. Not a discrepancy: 1,985 excludes the current-day row the file regenerates (**unanchored**) | **VERIFIED** |
| carried notionals "$6,505 → $7,812.46 (**+20.1%**)"; "$191 → $245.62 (**+28.6%**)" | `reports/task3/venue_table.md:95-96` | +20.099% and +28.597% | **VERIFIED** |
| carried ORB figures "0.076572 … p90 0.333662, n = 550 … **11.27 times**" | `reports/task3/venue_table.md:97` | cross-repository; nothing in VRPExperiment stores them | **UNVERIFIABLE** |
| "**Measured 2026-08-30, 04:32Z–05:35Z.**" | `reports/task3/venue_table.md:3` | no TASK 3 artifact has an mtime inside that window; captures run 06:13:56Z–06:17:54Z; taken literally the window starts 15 min before the registration commit | **CONTRADICTED** — DRAFT-V-3 |
| "0.086607 vol points = 198.111 bps" read against "1 volatility point = 22.875 bps" | `README.md:36` and `:50` | 0.086607 × 22.875 = **1.981 bps**, not 198.111; the mean is decimal volatility (8.6607 vol points) | **CONTRADICTED** — DRAFT-V-4 |

---

## 2. Derived quantities table

Every figure below was recomputed by me from stored primitives (USD rates, notionals, counts,
per-observation rows, spot prices) rather than copied from a document. Tolerance ±0.001 bps on
basis points and ±0.01 on ratios and percentages unless noted.

| derived quantity | stated | where | method | recomputed | status |
|---|---|---|---|---|---|
| MET straddle round trip | 32.571 bps | `docs/COSTS.md:88` | 0.80/245.62 × 10⁴ | 32.570638 | ✅ |
| MET per-rebalance fill | 8.143 bps | `docs/COSTS.md:95` | 0.20/245.62 × 10⁴ | 8.142659 | ✅ |
| MET hedge, central (11) | 89.57 bps | `docs/ARTIFACT.md:168` | 11 × 8.142659 | 89.569251 | ✅ |
| MET hedge, pessimistic (16) | 130.28 bps | `docs/ARTIFACT.md:169` | 16 × 8.142659 | 130.282546 | ✅ |
| **MET total, central** | **122.140 bps** | `docs/ARTIFACT.md:170` | sum | **122.139891** | ✅ |
| **MET total, pessimistic** | **162.853 bps** | `docs/ARTIFACT.md:171` | sum | **162.853188** | ✅ |
| MBT straddle round trip | 4.352 bps | `docs/COSTS.md:89` | 3.40/7812.46 × 10⁴ | 4.352022 | ✅ |
| MBT per-rebalance fill | 1.088 bps | `docs/COSTS.md:96` | 0.85/7812.46 × 10⁴ | 1.088006 | ✅ |
| MBT total, central / pessimistic | 16.320 / 21.760 bps | `docs/ARTIFACT.md:170-171` | sums | 16.320084 / 21.760111 | ✅ |
| HARVESTABLE requirement, MET / MBT | 325.706 / 43.520 bps | `progress.md:784` | 2.0 × pessimistic | 325.706376 / 43.520223 | ✅ |
| **MET failure factor** | **8.57×** | `HYPOTHESES.md:21` | 325.706376/38.0124 | **8.5684** | ✅ |
| **MBT clearance factor** | **3.28×** | `docs/ARTIFACT.md:222` | 142.7401/43.520223 | **3.2799** | ✅ |
| **Room for the absent MBT legs** | **49.61 bps** | `docs/ARTIFACT.md:230` | 142.7401/2 − 21.760111 | **49.6099** | ✅ |
| MBT cost at 29 rebalances | 35.904 bps, 2× = 71.81 | `progress.md:796` | 4.352022 + 29 × 1.088006 | 35.904184 / 71.808368 (still clears) | ✅ |
| BTC quarterly decay | 60.4% | `HYPOTHESES.md:23` | 1 − 112.719/284.53 | 0.60384 | ✅ |
| MET/MBT commission ratio; notional ratio | 7.48× / 31.8× | `docs/COSTS.md:100-102` | ratios | 7.4840 / 31.8071 | ✅ |
| Notionals from spot | 245.62 / 7,812.46 / 390,622.88 / 122,810.25 | `docs/ARTIFACT.md:142`, `venue_table.md:64` | 0.10/5/50 × spot | 245.6205 / 7812.4575 / 390622.875 / 122810.25 | ✅ |
| Spot cross-source disagreement | 1.16 / 3.24 bps | `venue_table.md:11-12` | (Coinbase−Kraken)/Coinbase × 10⁴ | 1.1616 / 3.2367 | ✅ |
| Margin thresholds (full-size BTC / ETH) | 0.26% / 0.81% | `venue_table.md:81-82` | 1000/notional | 0.2560% / 0.8143% | ✅ |
| Deribit straddle round-trip spreads | 22.50 / 25.00 bps | `docs/COSTS.md:253-254` | call + put round-trip medians | 22.50 / 25.00 | ✅ |
| Half-spread means from the stated distributions | 6.3542 / 5.5208 / 5.9375 / 7.1875 | `docs/COSTS.md:224-227` | weighted means of the tabulated counts | 6.35417 / 5.52083 / 5.93750 / 7.18750 (identical to the JSON means) | ✅ |
| Concurrent-escalation request count | 126 per endpoint | `docs/ACCESS.md:135` | 2+4+8+16+32+64 | 126 | ✅ |
| Carried-notional drifts | +20.1% / +28.6% | `venue_table.md:95-96` | ratios − 1 | +20.099% / +28.597% | ✅ |
| Power constants | 119.4 / 477.5 wk, 6.19, d 0.508 | `REGISTRATION.md:412-433` | closed form | 119.375 / 477.502 / 6.18517 / 0.50786 | ✅ |
| bps per unit of decimal volatility | 2,287.5 | `REGISTRATION.md:165` | √(2/π)·√(30/365)·10⁴ | 2287.4639 | ✅ |
| **ETH premium HAC SE in bps** | *not stated anywhere* | derived from `HYPOTHESES.md:19` | 0.021528 × 2287.4639 | **49.2445 bps** | ✅ |
| **Gap between the ETH premium and the MET central cost, in SEs** | *not stated anywhere* | derived from `docs/ARTIFACT.md:212-213` | 3.0878/49.2445 | **0.0627 SE** (two-sided p 0.95 against H₀: true mean = 122.14) | ✅ — feeds DRAFT-V-1 |
| **MET central cost if the rebalance count were 10, not the registered median 11** | *not stated* | sensitivity on `docs/ARTIFACT.md:168` | 32.570638 + 10 × 8.142659 | **113.997 bps — below the 119.052 bps premium** | ✅ — feeds DRAFT-V-1 |
| **Revision re-check interval** | **≈ 70 minutes** | `revision_recheck.json` `gap`; `README.md:91` | recheck_taken_at − taken_at, six windows | **37.23–37.24 minutes** | ❌ **CONTRADICTED** |

---

## 3. Intervals table

All four reported intervals are **one-sided 95% lower bounds**,
`mean − t_crit(n−1, 0.05) · SE` (`src/vrp/sealed_read.py:287-288`). All four reproduce exactly.

| # | interval | file:line | estimator actually used | independence assumed? | data structure — is that assumption doubtful? | reproduces? | status |
|---|---|---|---|---|---|---|---|
| 1 | BTC primary, **142.740 bps** (0.062401) | `HYPOTHESES.md:19`; JSON `:13-14` | Newey–West Bartlett HAC, **bw 30**, autocovariance divisor `n`; Student-t crit at dof 1954 | **No** — the HAC is the registered remedy | Overlapping 30-day forward windows on daily sampling. Measured ρ₁ = 0.952, falling below 0.05 at lag **25**; ρ is essentially zero beyond lag 30. Bandwidth 30 is well matched to the actual correlation length. | **Yes**, to 4 dp in bps and 6 dp in vol points | **VERIFIED** |
| 2 | ETH primary, **38.012 bps** (0.016618) | `HYPOTHESES.md:19`; JSON `:136-137` | same | **No** | Same. Measured ρ₁ = 0.960, falling below 0.05 at lag **30** — right at the bandwidth, so ETH is the marginal case. | **Yes** | **VERIFIED** |
| 3 | BTC non-overlapping, **140.188 bps** | `HYPOTHESES.md:20`; JSON `:58-59` | same routine at **bw 0** (population SE, divisor `n`); dof 65 | **Yes** ("IID by construction") | `premium[::30]`, n = 66. **Ljung–Box(5) = 1.232, p = 0.94** — no detectable residual serial correlation, so the assumption holds empirically. | **Yes** | **VERIFIED** |
| 4 | ETH non-overlapping, **26.688 bps** | `HYPOTHESES.md:20`; JSON `:181-182` | same | **Yes** | `premium[::30]`, n = 66. **Ljung–Box(5) = 2.467, p = 0.78.** | **Yes** | **VERIFIED** |

### 3.1 What I did to attack the independence assumption, and what happened

The brief asks whether any interval's independence assumption is violated *in a way that changes a
stated comparison*. I ran the two obvious attacks on the primary intervals. **Neither changes any
stated comparison.**

**Bandwidth sensitivity** (my own HAC, same Bartlett kernel, wider truncation):

| bandwidth | BTC SE | BTC CI lower | ETH SE | ETH t | ETH one-sided p | ETH CI lower |
|---|---|---|---|---|---|---|
| 0 (IID) | 0.003513 | 184.89 | 0.004919 | 10.581 | 8.8e-26 | 100.54 |
| **30 (registered)** | **0.014709** | **142.74** | **0.021528** | **2.418** | **7.86e-3** | **38.01** |
| 45 | 0.015534 | 139.64 | 0.023202 | 2.243 | 1.25e-2 | 31.71 |
| 60 | 0.015919 | 138.19 | 0.024075 | 2.162 | 1.54e-2 | 28.43 |
| 90 | 0.016403 | 136.37 | 0.025341 | 2.054 | 2.01e-2 | 23.66 |
| 120 | 0.016755 | 135.04 | 0.026372 | 1.974 | 2.43e-2 | 19.78 |
| 180 | 0.017346 | 132.82 | 0.027933 | 1.863 | 3.13e-2 | 13.90 |

**Moving-block bootstrap**, 4,000 draws: BTC SE 0.0147 (L=30) / 0.0170 (L=90) / 0.0179 (L=180);
ETH SE 0.0215 / 0.0256 / 0.0288. The registered bandwidth-30 SE sits at the low end of the
plausible range but not outside it.

Consequences for the two stated comparisons:

* **MBT (the open route).** "Clears the registered 2× hurdle by 3.28×." At bw = 180 the BTC lower
  bound falls to 132.82 bps and the factor becomes **3.05×** — still clears, comfortably. The
  comparison does not move.
* **MET (the closure).** "Fails by 8.57×." A wider bandwidth *lowers* the ETH bound, so the failure
  factor **grows** (325.706/13.90 = 23.4× at bw 180). The comparison moves only in the direction
  that strengthens the repository's conclusion.
* **SIGNAL_ABSENT.** ETH's one-sided p stays below 0.05 at every bandwidth I tried (worst 0.0313 at
  bw 180), so the branch that fires does not change either.

Two smaller estimator notes, neither raised as a finding because neither moves a figure that
decides anything:

* `newey_west_se` divides autocovariances by `n`, so at bandwidth 0 it returns the *population*
  standard error. At n = 66 that is 0.77% smaller than the `ddof=1` sample SE
  (0.021138 vs 0.021300 BTC; 0.027798 vs 0.028011 ETH) and moves the robustness lower bounds by
  0.6–0.8 bps. At n = 1,955 the effect is invisible.
* The critical value uses `dof = n − 1 = 1954` alongside a HAC standard error. A fixed-bandwidth
  HAC has a much smaller effective sample (~65 independent windows); using dof 65 would raise
  t_crit from 1.6456 to 1.6686 and lower the ETH bound by 1.1 bps to 36.9. Nothing turns on it.

---

## 4. Tests table

Every test in this repository is the same one: the single registered one-sided t-test of
**H₀: mean(VRP) ≤ 0** at α = 0.05 (`REGISTRATION.md:360-366`), with the p-value from the
repository's own incomplete-beta Student-t survival function (`sealed_read.py:192-215`) rather than
scipy. **That own implementation agrees with `scipy.stats.t.sf` to 11 significant figures** on
every reported p-value.

| # | test | file:line | stated | recomputed | tail | dof | correction | rule type | correction matches rule? | status |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | BTC primary | `HYPOTHESES.md:19` | t 5.888, p 2.297e-9 | t **5.8879**, p **2.2965959114e-09** | upper (matches registered H₁) | 1954 | none | conjunction | **yes** | ✅ |
| 2 | ETH primary | `HYPOTHESES.md:19` | t 2.418, p 7.859e-3 | t **2.4175**, p **7.8585401067e-03** | upper | 1954 | none | conjunction | **yes** | ✅ |
| 3 | BTC non-overlapping | `HYPOTHESES.md:20` | t 4.568, p 1.128e-5 | t 4.5679, p 1.1279134941e-05 | upper | 65 | none | conjunction | yes | ✅ |
| 4 | ETH non-overlapping | `HYPOTHESES.md:20` | t 2.088, p 0.0203 | t 2.0883, p 2.0344672901e-02 | upper | 65 | none | conjunction | yes | ✅ |
| 5 | BTC Q1 | `docs/ARTIFACT.md:91` | t 3.498, p 2.556e-4 | identical (n 488) | upper | 487 | none | single (descriptive) | yes | ✅ |
| 6 | BTC Q2 | `:92` | t 3.845, p 6.821e-5 | identical (n 488) | upper | 487 | none | single | yes | ✅ |
| 7 | BTC Q3 | `:93` | t 2.619, p 4.552e-3 | identical (n 488) | upper | 487 | none | single | yes | ✅ |
| 8 | BTC Q4 | `:94` | t 2.098, p 0.0182 | identical (n 491) | upper | 490 | none | single | yes | ✅ |
| 9 | ETH Q1 | `:91` | t 1.056, p 0.1458 (n.s.) | identical (n 488) | upper | 487 | none | single | yes | ✅ |
| 10 | ETH Q2 | `:92` | t 4.037, p 3.143e-5 | identical (n 488) | upper | 487 | none | single | yes | ✅ |
| 11 | ETH Q3 | `:93` | t −0.246, p 0.5970 | identical (n 488) | upper (correctly gives p > 0.5 for a negative t) | 487 | none | single | yes | ✅ |
| 12 | ETH Q4 | `:94` | t 0.803, p 0.2111 (n.s.) | identical (n 491) | upper | 490 | none | single | yes | ✅ |
| 13–14 | BTC / ETH fixture | `reports/task6/fixture_result.json` | t 4.2725 p 1.342e-5; t 7.4162 p 7.882e-13; n 270 | not re-executed; internally consistent, and the bps conversion checks out | upper | 269 | none | single | yes | ✅ (see note) |
| 15–18 | Deribit half-spread distributions, 4 legs | `docs/COSTS.md:224-227` | medians 6.25 / 5.00 / 5.00 / 7.50; p90 7.50 / 7.50 / 7.50 / 10.00; n 24 each | all exact; the tabulated full distributions reproduce the stored means exactly | — (order statistics, not a test) | — | none | — | — | ✅ |
| 19–30 | rebalance-count distributions, 2 assets × 3 bands | `README.md:61-62`; JSON `:25-56, 148-179` | 17/21, 11/16, 5/9 (BTC); 17/22, 11/16, 5/9 (ETH); n 1955 each | every min, median, mean, p90, max and median max-drift reproduces exactly | — (order statistics) | — | none | — | — | ✅ |
| 31 | spot cross-source disagreement | `venue_table.md:11-12` | 1.16 / 3.24 bps, n = 2 sources | 1.1616 / 3.2367 | — | — | none | — | — | ✅ |
| 32 | the multiplicity rule itself | `REGISTRATION.md:381-393` | "No multiplicity correction applies to a single endpoint … Berger (1982) gives an intersection-union test the full nominal level per component" | Both assets must reject for the premium conjunct to hold, and both do. An IUT of a conjunction is level-α without adjustment. | upper on each component | 1954 | **none (Berger 1982 IUT)** | **conjunction** | **yes — correct pairing; a Bonferroni/Šidák here would be the error** | ✅ |

### 4.1 Notes on the tests

* **Tail.** Every reported p is upper-tail, matching the registered one-sided H₁ (`mean(VRP) > 0`).
  The ETH Q3 row is the useful check: a negative t correctly yields p = 0.597, not 0.403.
* **Degrees of freedom.** `dof = n − 1` throughout, as the code sets it (`sealed_read.py:285`).
  Generous under HAC (see §3.1), immaterial at these sample sizes.
* **Multiplicity, and where a correction would have been wrong.** The registered endpoint is a
  conjunction — a premium exists **and** a venue is reachable — and the two-asset premium component
  is itself an all-must-reject conjunction. An intersection-union test takes the full nominal α per
  component; the registration says so, cites Berger (1982) for it, and applies no correction. **The
  correction applied matches the decision rule it feeds.** A union-type correction here would have
  lowered the level below nominal and made SIGNAL_ABSENT easier to reach, which is the mismatch the
  registration explicitly names and avoids.
* **The four-quarter split carries no correction and needs none.** The quarters are used to weaken
  the ETH claim, not to fire a branch; a correction would leave even fewer significant and would
  therefore *strengthen* the stated limitation. Disclosed at `HYPOTHESES.md:23` and
  `docs/ARTIFACT.md:100-102`.
* **The fixture.** Planted premium 0.08 decimal (= 183.0 bps); recovered 0.094653 (BTC) and
  0.094101 (ETH), i.e. **+18.3%**. No document states a recovery tolerance, so this is recorded as
  an artifact fact and not as a failed claim. The overshoot is 0.66 fixture standard errors and is
  partly the known downward (Jensen) bias of a 30-observation sample standard deviation on the
  realized leg, which inflates the measured premium by roughly 0.9%.
* **The registration's power sentence.** Each figure reproduces (0.508, 1.016 = 2 × 0.508,
  6.19/1.016² = 6.0), but the sentence joining them —
  *"at the halved effect size the same design detects `d ≈ 1.016` only with `n ≈ 6`"*
  (`REGISTRATION.md:430-433`) — is internally garbled: halving an effect raises the required n from
  24 to ≈ 96, and n ≈ 6 is what a *doubled* effect needs. It is a design-stage note that decides
  nothing (the achieved n of 1,955 is 2.7× the registered depth), so it is recorded here rather
  than raised as a finding.

---

## 5. Draft findings

Four. Temporary IDs; the consolidator assigns final ones. **None of them changes the registered
verdict**, and each says so explicitly.

### DRAFT-V-1
- **Repository / SHA:** VRPExperiment / `d37cf6d190dfdaef8e613daf099a507fe1a77dcf`
- **Hypothesis or artifact:** H1 closure, MET (Micro Ether) route — the "margin-free" leg of the
  cost comparison in `docs/ARTIFACT.md` and `HYPOTHESES.md`
- **Direction:** A
- **Class:** STATISTICAL
- **Severity:** S2
- **Label:** DERIVED
- **Claim challenged (verbatim quote):**
  "**Micro Ether — decided, and not by a close margin.** / The ether premium's point estimate is
  **119.05 bps**. The **central, commission-only, lower-bound cost is 122.14 bps**. **The premium
  does not cover the commission.**" — VRPExperiment/docs/ARTIFACT.md:211-214; and
  "And the failure does not depend on the margin at all: **the ETH premium's point estimate,
  119.052 bps, is below the central commission-only cost of 122.140 bps.**" —
  VRPExperiment/HYPOTHESES.md:21
- **Evidence:**
  - The arithmetic is right. ETH `mean_bps` = 119.0521, n = 1,955
    (VRPExperiment/reports/task6/real_attempt2_result.json:141); central cost
    = 0.80/245.62 × 10⁴ + 11 × 0.20/245.62 × 10⁴ = **122.139891 bps**
    (VRPExperiment/reports/task5/commission_bps.json:53 and :5; median rebalance count 11 at
    real_attempt2_result.json:163). The gap is **3.0878 bps**, 2.53% of the cost.
  - The repository's own standard error on that mean is 0.021528 vol
    (VRPExperiment/HYPOTHESES.md:19; real_attempt2_result.json:139), which at the registered
    conversion of 2,287.4639 bps per unit (VRPExperiment/src/vrp/sealed_read.py:43-51) is
    **49.2445 bps**. The 3.0878 bps gap is **0.063 of one standard error**. Testing the stated
    conclusion directly: H₀ *true mean = 122.14 bps* gives a two-sided p of **0.95** at n = 1,955,
    dof 1,954. The data are as consistent with the premium exactly covering the commission as with
    any other value in a very wide band.
  - The comparison also turns on a single integer. The central cost uses the registered median
    rebalance count of 11. Recomputed from the raw paths, **44.8% of the 1,955 ETH paths need ≤ 10
    rebalances and 53.4% need ≤ 11** — the median sits just over the 10/11 boundary. At a count of
    10 the central cost is **113.997 bps**, *below* the 119.052 bps premium, and the quoted sentence
    reverses.
  - The registration itself supplies the honest framing that the artifact drops: the premium's
    reported figure is a **one-sided 95% lower bound of 38.012 bps** (HYPOTHESES.md:19), and
    the registered decision rule compares that bound, not the point estimate
    (VRPExperiment/REGISTRATION.md:312-316).
- **Recomputation (if any):** inputs — ETH premium series rebuilt from
  `data/raw/task6/dvol_ETH_daily.json` and `underlying_ETH_daily.json` (live untracked, read
  2026-09-05T03:57Z) through my own implementation of VRPExperiment/src/vrp/sealed_read.py:54-301;
  cost inputs from VRPExperiment/reports/task5/commission_bps.json. Method — reproduce the mean and
  HAC SE (they match the stored artifact to 6 dp), convert the SE to bps, express the stated gap in
  SE units, and re-run the rebalance count at ±0.10 to get the full count distribution. Result —
  SE 49.2445 bps; gap 0.0627 SE; 53.4% of ETH paths at ≤ 11 rebalances; cost at 10 rebalances
  113.997 bps. Tolerance ±0.001 bps.
- **What would resolve it:** one sentence in `docs/ARTIFACT.md` and `HYPOTHESES.md` stating that
  the point-estimate comparison is within 0.06 standard errors and is therefore illustrative rather
  than decisive, with the decisive statement left where it belongs — the registered
  CI-lower-vs-2×-pessimistic test, which fails by 8.57× and is robust to every bandwidth and
  bootstrap I tried.
- **Confidence:** MEDIUM — the arithmetic verifies exactly and two disclosed asymmetries push the
  comparison the repository's way (three cost legs are `Absent` and non-negative, so the true cost
  exceeds 122.14 bps — HYPOTHESES.md:24; and REGISTRATION.md:333-336 registers that discrete
  hedging earns less than the conversion implies, so the premium side is an upper bound). What is
  not supported is the *stated certainty* of a comparison the repository's own estimator cannot
  separate from a tie.
- **Invalidated by later commits?:** no — the figures are fixed by a spent latch
  (`reports/task6/task6.latch.2.json`) and by tracked artifacts at the anchor; VRPExperiment's last
  commit is the anchor itself.
- **Disclosed by authors?:** no. `HYPOTHESES.md:23` discloses instability, absent tail risk and the
  absence of a simulated sleeve, and `HYPOTHESES.md:24` discloses that every cost figure is a lower
  bound — but nowhere does any document put a standard error, an interval or the word "within
  noise" next to the 119.052-vs-122.140 comparison. `grep` over README.md, HYPOTHESES.md,
  docs/ARTIFACT.md, docs/HANDOVER.md, DECISIONS.md and progress.md for "sampling error", "standard
  error of the premium", "3.088" and "close margin" returns only the claim itself.

### DRAFT-V-2
- **Repository / SHA:** VRPExperiment / `d37cf6d190dfdaef8e613daf099a507fe1a77dcf`
- **Hypothesis or artifact:** TASK 4 / ADR-009 — the data-revision re-check
- **Direction:** B
- **Class:** INTERNAL_INCONSISTENCY
- **Severity:** S4
- **Label:** DERIVED
- **Claim challenged (verbatim quote):**
  "| **revision** | **all six fixed windows byte-identical after ≈ 70 minutes** | 6 windows × 169
  rows |" — VRPExperiment/README.md:91; and
  "The six data-only baselines recorded at 06:05Z were re-fetched at ~07:15Z, a gap of
  **≈ 70 minutes**" — VRPExperiment/progress.md:818-820
- **Evidence:**
  - The artifact's own stamps: every window carries `taken_at` between
    **2026-08-30T06:26:08.230Z** and **06:26:09.144Z** and `recheck_taken_at` between
    **07:03:22Z** and **07:03:23Z** — VRPExperiment/reports/task4/revision_recheck.json:19,25 (and
    the five sibling windows). The elapsed interval is **37.23–37.24 minutes** on all six, n = 6.
  - The baselines' own file records `retrieved_at: 2026-08-30T06:25:49.532Z` —
    VRPExperiment/reports/task4/rate_and_revision_baseline.json. Neither 06:05Z nor 07:15Z appears
    anywhere in either artifact.
  - The wrong figure is written into the JSON itself: `"gap": "≈70 minutes"` —
    VRPExperiment/reports/task4/revision_recheck.json:3.
  - The substantive result **verifies**: all six `data_only_sha256` equal their
    `recheck_data_only_sha256` and all six row counts are 169 → 169.
- **Recomputation (if any):** inputs — the twelve timestamps at
  VRPExperiment/reports/task4/revision_recheck.json:19,25,40,46,… ; method — parse both stamps per
  window and difference them; result — 37.23, 37.24, 37.24, 37.24, 37.23, 37.23 minutes.
  Tolerance ±0.01 min.
- **What would resolve it:** replace "≈ 70 minutes" with "≈ 37 minutes" in
  `README.md:91`, `docs/ARTIFACT.md:280`, `DECISIONS.md:190`, `progress.md:819-820` and the JSON's
  own `gap` field, and correct progress.md's 06:05Z / ~07:15Z to 06:26Z / 07:03Z.
- **Confidence:** HIGH — the contradicting timestamps are in the same tracked file as the claim.
- **Invalidated by later commits?:** no — `revision_recheck.json` is added in the anchor commit
  itself and is the repository's last word on the question.
- **Disclosed by authors?:** no — the ≈70-minute figure is stated four times and in the artifact's
  own `gap` field, with no note that it is approximate in the direction of nearly double.

### DRAFT-V-3
- **Repository / SHA:** VRPExperiment / `d37cf6d190dfdaef8e613daf099a507fe1a77dcf`
- **Hypothesis or artifact:** TASK 3 venue table — the stated measurement window, and its relation
  to the pre-registration guarantee
- **Direction:** neutral
- **Class:** PROVENANCE
- **Severity:** S3
- **Label:** DERIVED
- **Claim challenged (verbatim quote):**
  "**Measured 2026-08-30, 04:32Z–05:35Z.** Every classification below is evidenced by published
  text recorded with its URL and its date." — VRPExperiment/reports/task3/venue_table.md:3
- **Evidence:**
  - The registration commit `78275921ca8f4cad72fd7bf2f10155dcf58cb507` ("docs: TASK 2 —
    REGISTRATION.md, committed before any network call") is dated **2026-08-30T04:47:08Z**
    (`git -C /home/kiros-li/Documents/GitHub/VRPExperiment log`, read 2026-09-05T04:04Z). Taken
    literally, a TASK 3 measurement beginning at 04:32Z precedes it by 15 minutes and would
    contradict "**Registered 2026-08-30, before any network call**" —
    VRPExperiment/REGISTRATION.md:3-5.
  - **No TASK 3 artifact has an mtime inside the stated window.** From the live untracked tree
    (read 2026-09-05T04:05Z): the earliest network artifact in the entire repository is
    `data/raw/robots/www.deribit.com.robots.txt` at **04:47:24Z** — 16 seconds *after* the
    registration commit — and the TASK 3 page captures run **06:13:56Z–06:17:54Z**
    (`deribit_restricted_jurisdictions.html` 06:13:57Z, `ibkr_ca_mbt_met_options.html` 06:15:29Z,
    `hl_meta.json` 06:16:21Z, `cme_refusal.json` 06:17:54Z). The TASK 3 commit `3ad6098` is at
    06:22:23Z.
  - The in-document per-page stamps are systematically early too:
    "**Retrieved:** 2026-08-30T05:13Z" (reports/task3/deribit_restricted_jurisdictions_verbatim.md:7)
    against a file mtime of 06:13:57Z; "retrieved 2026-08-30T05:15Z"
    (reports/task3/venue_table.md:38) against 06:15:29Z; "Retrieved 2026-08-30T05:27Z"
    (reports/task3/robots_and_terms.md:20) against 06:17:54Z. TASK 5's stamp is off by 11 minutes
    in the same direction ("retrieved 2026-08-30T06:20Z", docs/COSTS.md:33, against a 06:31:21Z
    mtime).
  - **The captures themselves verify by content**, so this is a clock problem and not a fabrication
    problem: `data/raw/task3/deribit_restricted_jurisdictions.html` is **63,433 bytes** with
    SHA-256 **`ec5a39b737030785…`** and `data/raw/task3/cme_refusal.json` is **602 bytes** with
    SHA-256 **`eecde3fafbde4090…`**, exactly as quoted in
    reports/task3/deribit_restricted_jurisdictions_verbatim.md:9 and
    reports/task3/robots_and_terms.md.
- **Recomputation (if any):** inputs — `git log` on the live repository and `stat` on every file
  under `data/raw/` (both read-only, 2026-09-05T04:04–04:05Z); method — convert commit dates and
  file mtimes to UTC and order them; result — repo init 04:22:18Z → TASK 0 04:37:16Z → TASK 1
  04:43:31Z → **registration 04:47:08Z → first network artifact 04:47:24Z** → TASK 3 captures
  06:13:56–06:17:54Z → TASK 3 commit 06:22:23Z → TASK 4 06:23–06:26Z → TASK 5 06:31Z → TASK 6
  06:58–06:59Z. Monotone and consistent throughout, with only `venue_table.md:3`'s window out of
  line.
- **What would resolve it:** correct `reports/task3/venue_table.md:3` to the window the artifacts
  actually occupy (≈ 04:47Z–06:18Z, or 06:13Z–06:18Z for the page captures alone) and correct the
  three per-page retrieval stamps, which are each ~50–60 minutes early. The mtimes are unanchored
  (gitignored), so an author statement of the true clock offset would settle it definitively.
- **Confidence:** MEDIUM — the file mtimes are untracked working-tree metadata and could in
  principle have changed since the anchor; but they are internally consistent with the commit
  sequence to the minute across five separate tasks, which is hard to produce accidentally.
- **Invalidated by later commits?:** no — `venue_table.md` is unchanged since `3ad6098` and the
  anchor is the repository's last commit.
- **Disclosed by authors?:** no — no document notes any clock offset. **Stated plainly: the
  substantive pre-registration guarantee VERIFIES.** Nothing under `data/` predates the registration
  commit; the earliest capture postdates it by 16 seconds. The finding is that a stated timestamp
  contradicts the repository's own evidence in a way that, read at face value, would wrongly appear
  to break that guarantee.

### DRAFT-V-4
- **Repository / SHA:** VRPExperiment / `d37cf6d190dfdaef8e613daf099a507fe1a77dcf`
- **Hypothesis or artifact:** the premium's unit label in `README.md` and `HYPOTHESES.md`
- **Direction:** neutral
- **Class:** INTERNAL_INCONSISTENCY
- **Severity:** S4
- **Label:** READ
- **Claim challenged (verbatim quote):**
  "| BTC premium, mean | **0.086607 vol points = 198.111 bps of notional** | **1,955 daily
  observations** |" — VRPExperiment/README.md:36, read against
  "| conversion, registered before any data | **1 volatility point = 22.875 bps of notional** | — |"
  — VRPExperiment/README.md:50
- **Evidence:**
  - 0.086607 × 22.875 = **1.981 bps**, not 198.111. The two rows of the same table are inconsistent
    by a factor of 100.
  - The stored mean is **decimal** volatility, not volatility points: `mean_vol_points` = 0.086607
    (VRPExperiment/reports/task6/real_attempt2_result.json:19), and `estimate_premium` multiplies it
    by `bps_per_volatility_point()` = 2,287.4639 bps *per unit of decimal volatility*
    (VRPExperiment/src/vrp/sealed_read.py:43-51 and :286,298). In volatility points the mean is
    **8.6607**, and 8.6607 × 22.8746 = 198.111 bps.
  - The repository states it correctly elsewhere: "| **mean premium** | **8.66 volatility points** |
    **5.20 volatility points** |" — VRPExperiment/docs/ARTIFACT.md:71.
  - The same mislabel recurs at README.md:41, HYPOTHESES.md:19, and progress.md:725 and :729. `REGISTRATION.md:165-166` carries the same looseness — "`edge_bps = 2,287.5 × (IV − RV)`
    with `(IV − RV)` in decimal volatility points" immediately followed by "**One volatility point
    of premium is 22.875 bps of notional**".
- **Recomputation (if any):** inputs — README.md:36 and :50; method — multiply the stated mean by
  the stated conversion; result — 1.981 bps against a stated 198.111 bps, a factor of 100.
  Tolerance: none needed.
- **What would resolve it:** write the mean as "8.6607 volatility points (0.086607 in decimal)" in
  README.md, HYPOTHESES.md and progress.md, matching docs/ARTIFACT.md:71, and rename the code field
  `mean_vol_points` to `mean_decimal_vol`.
- **Confidence:** HIGH — a direct arithmetic contradiction between two lines of the same table.
- **Invalidated by later commits?:** no — both lines are in the anchor commit.
- **Disclosed by authors?:** no. **No computed figure is affected**: every bps figure in the
  repository is computed from the decimal value through the correct 2,287.4639 factor, and every
  one of them reproduces exactly. This is a labelling defect only.

---

## 6. What could not be checked, and why

| item | why not | consequence |
|---|---|---|
| The two hourly row counts **47,696** and **47,858** (`HYPOTHESES.md:22`, `progress.md:720-721`) | The driver writes them to stdout only (`tools/task6_sealed_run.py:137-140, 182-185`); no artifact stores them, and the spent latch (`src/vrp/latch.py`, `README.md:124`) forbids a re-fetch. | **UNVERIFIABLE.** Consistency check only: `ceil(1992/40) = 50` hourly chunks with inclusive endpoints over 1,992 days gives 1992 × 24 + 50 = **47,858**, exactly the stated perpetual figure; the 7-day-later DVOL start reconciles the 162-row difference. Consistent, but consistency is not verification. Everything else in the same sentence (1,985 / 1,992 / 30 / 1,955 / the span) is verified exactly. |
| **BTCY MER 1.28%, ETHY MER 1.29%** (`README.md:79`, `venue_table.md:28`) | No machine-readable artifact holds them and the two fund pages were never captured under `data/raw/`. | **UNVERIFIABLE.** Decides nothing: the ETF route is excluded on the registered product-type criterion 3.1(2), not on cost. |
| **"mypy strict clean, ruff clean"** (`README.md:122`) | Verifying a pass/fail requires executing the repository's own tooling, which the read-only rule forbids in place; `reports/env_report.json` records versions, not exit status. | **UNVERIFIABLE.** The counts it sits beside — **50 tests**, **17 source files** — are verified statically, and `ba50596..d37cf6d` touches no `.py`, so any clean run at `ba50596` applies to the anchored code. |
| Carried **ORBExperiment / MLCryptoEngine** figures (`venue_table.md:97`, `docs/VENUE_TABLE_UPDATE.md:73-74`) — 0.076572 / 0.333662 USD per share, n = 550, 11.27× | The cited sources are in other repositories; nothing under `VRPExperiment/` stores them. | **UNVERIFIABLE inside this repository.** They enter no VRPExperiment verdict arithmetic — they appear as narrative precedent for measuring rather than carrying cost. The two carried *notional* figures in the same table are re-derived internally and both drift percentages verify. |
| The three **HTTP 422** Hyperliquid options probes (`venue_table.md:27`) | Only the `meta` capture (`hl_meta.json`) is on disk; the three refusal responses are not stored as artifacts. | The **232 perpetuals / zero options** count is verified from the capture; the 422 statuses are recorded as stated but unbacked by a stored payload. |
| The **fixture run** (`reports/task6/fixture_result.json`) | The synthetic source seeds from the run date (`tools/task6_sealed_run.py:193-198`), so the exact stream is not reproducible today, and re-running the repository's driver is outside the read-only rule. | The stored figures are internally consistent and the bps conversion checks out; the +18.3% overshoot of the planted 0.08 is within 0.66 fixture SE and partly explained by the Jensen bias of a 30-observation sample SD. No document states a tolerance, so nothing is contradicted. |
| The **latch module hashes against the blobs at commit `adac707`** (P17) | Not needed in the end. | Better than needed: **all eleven SHA-256 hashes in `task6.latch.2.json` match the snapshot files at the anchored SHA byte for byte**, and `task6.latch.json` differs from it in exactly one file — `tools/task6_sealed_run.py` — confirming Amendment 1's claim. |
| Whether the **raw series were altered after the anchor** | `data/` is gitignored; the four files carry mtimes, not commit hashes. | Formally **unanchored**. Practically authenticated: my independent recomputation reproduces roughly forty stored figures across two assets to full precision, which altered inputs could not do. |

---

## 7. Live-repo access log

Every access to `/home/kiros-li/Documents/GitHub/VRPExperiment/` in this task was **read-only**:
`git status --porcelain`, `git rev-parse`, `git log`, `git diff --name-status`, `git diff` on one
file, `find -printf`, `stat`, `sha256sum`, `wc -l`, `head`, and `cp` of four ~45 KB JSON files out
of the repository into my work directory. **No file in the repository was opened for writing, no
repository script was executed, and no commit, checkout, stash or reset was performed.** No `.env`,
keystore, session, credential or token file was opened. No file larger than ~500 KB was read
(`data/raw/task4/alt/tardis_api`, 210,602,148 B, was not touched).

Unanchored reads (untracked / gitignored working-tree data), with UTC read times:

* `data/raw/task6/{dvol,underlying}_{BTC,ETH}_daily.json` — copied and read **2026-09-05T03:57Z**
* `data/raw/task4/alt/cdd_DeriBit_volatility_OHLC_{BTC,ETH}.csv` — line/byte counts, **04:03Z**
* `data/raw/` full mtime listing — **04:05Z**
* `data/raw/task3/*.html`, `cme_refusal.json`, `hl_meta.json`, `data/raw/task5/commissions-futures.html`
  — sizes and SHA-256 only (plus the 602-byte CME refusal body in full), **04:05Z**

These paths are not in git and may have changed since the 2026-08-30 anchor.

**`git -C /home/kiros-li/Documents/GitHub/VRPExperiment status --porcelain`, BEFORE first access —
2026-09-05T03:57:29Z:**

```
```

(empty — exit 0, working tree clean; `HEAD` = `d37cf6d190dfdaef8e613daf099a507fe1a77dcf`)

**`git -C /home/kiros-li/Documents/GitHub/VRPExperiment status --porcelain`, AFTER last access —
2026-09-05T04:08:51Z:**

```
```

(empty — exit 0, working tree clean; `HEAD` = `d37cf6d190dfdaef8e613daf099a507fe1a77dcf`)

**No modification was made to the audited repository and none is reported.**

---

## 8. Scripts used

All under `/home/kiros-li/.cache/program-audit/scratchpad/work/agentC-vrp-verify/`, all written by
me, none copied from the repository:

| script | what it does |
|---|---|
| `recompute.py` | Rebuilds both premium series from the four raw JSON files and reproduces every figure in `real_attempt2_result.json`: means, HAC SEs, t, p, CI lower bounds, positive shares, the four quarterly splits, the non-overlapping robustness, and all six rebalance distributions (including a check of the repo's index rules against numpy's median / 90th percentile). |
| `hac.py` | Autocorrelation profile of both premium series to lag 400; HAC standard errors at bandwidths 0–365; moving-block bootstrap (4,000 draws, L = 30/90/180/365). |
| `thin.py` | Ljung–Box test of the "IID by construction" claim on `premium[::30]`; HAC bw 1–3 on the thinned series. |
| `costs.py` | Reproduces every commission, notional, hurdle, ratio and threshold from the stored USD rates and spot prices. |
| `mkjson.py`, `patch.py` | Emit `VRPExperiment.claims.json`. |
