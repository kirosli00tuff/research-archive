# HFExperiment — verification (Agent C, VERIFY)

Repository: HFExperiment
Anchored SHA: 82e77a021256d917c665ff6d4304c25b08f35451 (main, 2026-08-28)
Content read from SNAP/HFExperiment unless marked UNANCHORED. Line numbers are identical to
`git show 82e77a0:<path>`. Recomputation was done under
`.../scratchpad/work/agentC-verify-HF/recompute.py` with the audit venv, reading only from SNAP.
Prepared 2026-09-04 UTC. Inputs: my own `HFExperiment.inventory.md` / `.json`.

**Headline.** Of the 24 numeric claims, **16 VERIFIED, 4 CONTRADICTED, 4 UNVERIFIABLE**. The
repository's *computational* spine is exact: the 4.07 bp/day cost hurdle, the 213.84 bp round
trip, the 28.76 / 56.84 annual drag, the frozen rho 0.071641, the day-2061 / day-2852 projection,
the two-point power law and every one of its interpolated cells, the churn means, all 21
median-share-price cells, the price-reconciliation ratios and every C.1 ledger count reproduce
from stored primitives to the last printed digit. The Section 0 BLOCKED closure is fully
supported by its own evidence ledger.

What does **not** verify falls in two places. First, the *stated arithmetic* that closes the
DEGRADED branch (REGISTRATION.md Section 6) is contradicted by the very formations file it
cites — though only in the direction that makes the closure stronger. Second, and structurally
more important, **the single number the whole hypothesis rests on — 27.99 bp/day — has no
artifact anywhere in this repository, and no n, no window and no standard error is stated for it
anywhere.** That is UNVERIFIABLE here, not contradicted; it is verifiable only across the
AiTrader boundary, which this task does not cross.

There is **no realized confidence interval, no test statistic and no p-value in this repository**.
The shadow series produced zero observations, so nothing was ever evaluated on data. The Intervals
and Tests tables below therefore record *constructions and levels*, and say so.

---

## 1. Claims table

Tolerance convention: "printed" = agreement to the precision the document prints; the repository's
own pinning test (`tests/test_registered.py:63-67`) uses `abs=0.005` on the hurdle, and I use the
same band where a two-decimal figure is compared.

| # | claim (abridged) | file:line | stated | source of truth | recomputed | tol | status |
|---|---|---|---|---|---|---|---|
| C1 | Section 0 verdict BLOCKED: fractional refused however phrased, 10243 on decimal across two names and two order types, 10244 on cashQty, whole-share control accepted | REGISTRATION.md:299-304 | 5 orders (cap 10), 2 symbols, 2 order types, 20 contracts | reports/stage_a1b/evidence.jsonl, 51 rows | 5 `order_request` / 5 `order_outcome`; 3× code 10243 (decimal-mkt-MU, decimal-lmt-MU, decimal-mkt-TE); 1× code 10244 (cashqty-mkt, MU); control-whole-share TE qty 1 → PreSubmitted then Cancelled; 20 `contract_details` all MinSize/SizeIncrement "0.0001"; `fills: []`; `final_positions` `[]` twice | exact | **VERIFIED** |
| C2 | "the measured cost hurdle of 4.07 bp per day" | REGISTRATION.md:249-250; registered.py:78 | 4.07 | book_spreads.json per-name medians + costmodel.py:135-223 + commission.py:103-113 | **4.073081** bp/day (w5 spread 13.0752, w5 mid 201.9075, RT 213.8367 bp) | 0.005 | **VERIFIED** |
| C3 | "the effect, measured at 27.99 bp per day on the already-spent holdout"; "highest recorded information ratio, 1.062"; width table 66.40/27.99/1.062 and 31.70/10.04/0.798 | REGISTRATION.md:52-56, 92-93, 113-118 | 27.99 / 66.40 / 1.062 / 10.04 / 31.70 / 0.798 | **none in this repository** — literals only at scripts/cost_table_a2.py:31-34 and registered.py:104-105 | n/a | n/a | **UNVERIFIABLE** — no artifact in HFExperiment holds these; **n is stated nowhere**; no window, no SE. Provenance declared as the AiTrader cross-sectional round of 2026-07-26 (README.md:3-5, benchmark.py:5-9), outside this task's scope. Their mutual consistency does verify: see D5, D6 |
| C4a | "144 USD at the last two formations" | REGISTRATION.md:150 | 144 | formations.json `median_price` | 143.80 (2026-06-01), 143.89 (2026-07-01), both reproduced from stored `last_close` | printed | **VERIFIED** |
| C4b | "up from 36 in March and April" | REGISTRATION.md:150-151 | 36, 36 | formations.json `median_price` | March 36.47, **April 40.59** | printed | **CONTRADICTED** (April) → DRAFT-V-1 |
| C4c | "20 names at one share each already cost about 2,880 USD" | REGISTRATION.md:152-153 | ~2,880 | formations.json 2026-07-01 width-20 `last_close`, n=20 | **7,890.47 USD** (2,880 = 20 × the median, not the book) | — | **CONTRADICTED** → DRAFT-V-1 |
| C4d | "A 5-name book gets one share per name, 720 of 900 deployed" | REGISTRATION.md:153 | 720 of 900 | formations.json 2026-07-01 width-5 `last_close`, n=5 | **3,554.82 USD**; SNDK alone 2,273.73 > 900 | — | **CONTRADICTED** → DRAFT-V-1 |
| C4e | "per-name prices from 22 to 1,595 USD" | REGISTRATION.md:154 | 22 … 1,595 | formations.json closes; book_spreads.json mids | No stored price set has min ≈22. 1,595.19 = SNDK A.2 median mid, 22.305 = PL A.2 median mid, but the same 20-name set's minimum is ONDS 8.745 (WULF 15.71, CIFR 15.845 also below 22); the width-5 book's own minimum mid is WOLF 26.355 and its July close minimum is 48.25 | — | **CONTRADICTED** → DRAFT-V-1 |
| C5 | "The floor is 500 USD of total account equity, a 400 USD loss on 900 deployed after the 100 buffer, 1.31 sigma of the width-20 tracking error, driftless touch probability near 19 percent" | REGISTRATION.md:216-218 | 400 USD loss = 1.31σ = 19 % | TE(20) 42.54 %/yr (C12) → σ = 900 × 0.4254 = **382.90 USD**; reflection tail 2Φ(−k) | a **400 USD** loss is k = 1.045σ → **29.6 %**; 1.31σ / 19.2 % requires a **500 USD** loss (1000 − 500) | 0.01σ / 0.5 pt | **CONTRADICTED** → DRAFT-V-2 |
| C5b | "600 touches near 30 percent … 400 buys only 7 more points" | REGISTRATION.md:219-221; DECISIONS.md:173-179 | 30 %, 7 pts | as above, loss = 1000 − floor | 600 → 1.045σ → 29.6 %; 400 → 1.567σ → 11.7 %; 19.2 − 11.7 = **7.5 pts** | 0.5 pt | **VERIFIED** (on the 1000-equity basis, which is what ADR-011 uses throughout) |
| C6 | "Gateway 127.0.0.1:4002, server version 187, account [paper account ID removed]" (A.1b session) | a1b_report.md:3-4; DECISIONS.md:408, :439; ACCESS.md:178; progress.md:235; refusals.md:332 | 187 | evidence.jsonl row 2 | `{"kind":"connected","managed":["[paper account ID removed]"],"server_version": **178**}` | exact | **CONTRADICTED** → DRAFT-V-3 (the C.1 probe, a separate later connection, does record 187 at refusals.md:332) |
| C7 | "median 12.77 bp, p75 17.2, p90 20.7, max 27.4"; "inherited 15.8 to 50 bp band" | REGISTRATION.md:172-173; cost_table.md:3; costmodel.py:46 | 12.77 / 17.2 / 20.7 / 27.4 | book_spreads.json 20 per-name medians, 9 cells each = 180 cells | median 12.77318, p75 17.23247, p90 20.73058, max 27.43237, min 2.14133, p25 6.36740 — all reproduce **exactly** under the lower-order-statistic quantile convention (numpy `method="lower"`); discarded crossed 6 / locked 88, rest 0 | exact | **VERIFIED** |
| C8 | "All 124 recorded formation dates identical. Universe exact at all 10 checked dates, all 500 rows each." | progress.md:207-208 | 124; 10 × 500 | reproduce_log.txt:1,21; universe_check.json | reproduce_log.txt:1 states `reproduced 124, recorded 124, identical=True`; universe_check.json is a 10-element list, every element `recorded_rows` = `reproduced_rows` = 500, all four mismatch arrays empty, `exact_match` true | exact | **VERIFIED against the stored artifacts.** The reproduction *itself* is UNVERIFIABLE here: it ran against `/home/kiros-li/Documents/GitHub/AiTrader/analysis_bars.db` (dbaccess.py:13), outside this task's scope. ADR-006 (DECISIONS.md:106-110) already discloses that "identical" covers universe membership and formation dates, not the recorded books at widths 5 and 50 |
| C9 | "rho … frozen at 0.071641 … the lower bound clears zero at day 2,061 and clears the hurdle at day 2,852" | REGISTRATION.md:248, 260-262 | 0.071641; 2061; 2852 | verdict.py:26-66, 119-133 (formula and search), re-implemented independently | golden-section reproduction **0.071641330**; independent fine-grid argmin **0.0716407**; first_crossing_day(27.99, 418, rho, 0) = **2061**; (…, 4.07) = **2852**; identical with the frozen constant 0.071641 | 1e-6 / exact | **VERIFIED** |
| C10 | "28.76 USD per year under whole-share Tiered, 56.84 under fractional" | REGISTRATION.md:184-186 | 28.76 / 56.84 | costmodel.py:178-206 over book median mid 103.2525 | Tiered 28.08 + 0.68 = **28.76**; Fixed and fractional 56.16 + 0.68 = **56.84**; width-5 rows 17.13 / 48.33 / 86.73 also reproduce | 0.01 | **VERIFIED** |
| C11 | "10.4 fills per month against 4.0 at width 5, which reaches … 200 fills … in about 19 months instead of 50" | REGISTRATION.md:101-104 | 5.2, 2.0, 10.4, 4.0, 19, 50 | formations.json `churn`, 6 formations | width 20: 8+6+5+5+2+5 = 31, /6 = **5.1667 → 5.2**; width 5: 4+3+1+1+2+1 = 12, /6 = **2.0**; 200/10.4 = **19.23**; 200/4.0 = **50** | printed | **VERIFIED** |
| C12 | "TE exponent -0.321 and excess exponent -0.445 … IR 0.894 against width 5's 1.062 … giving 1.41" | DECISIONS.md:143-147; REGISTRATION.md:110-118 | −0.321, −0.445, 53.15, 42.54, 20.56, 15.10, 0.975, 0.894, 1.41 | two recorded points (5, 50) from C3 | exponents **−0.32113 / −0.44528**; TE(10) **53.15**, TE(20) **42.54**; excess(10) **20.56**, excess(20) **15.10**; IR 0.975 / 0.894; (IR₅/IR₂₀)² = **1.4109** | printed | **VERIFIED** — but the IR column needs the annualisation IR = excess × 252 / (TE × 100), which no document in the repository states (see D6). n = 2 points, zero residual dof, disclosed at REGISTRATION.md:116-117 and DECISIONS.md:157-158 |
| C13 | "The ratio of medians is 0.7176, a 28.2 percent gap … MXL at 0.518 and WOLF at 0.546" | price_reconciliation.md:10-11, 48-50; progress.md:111-116 | 0.7176, 28.2 %, 0.518, 0.546 | formations.json 2026-07-01 width-20 closes vs book_spreads.json mids, n = 20 | 103.2525 / 143.895 = **0.717554** → 28.24 %; MXL 66.27/128.03 = **0.51761**; WOLF 26.355/48.25 = **0.54622**; full per-name ratio range **0.5176 – 1.0613** ("run continuously from 0.52 to 1.06", :65) | printed | **VERIFIED** |
| C13b | "No name in the book split in 2026. No name went ex-dividend between 2026-07-24 and 2026-08-24." | price_reconciliation.md:29-30 | 0 splits, 0 ex-dates | stockanalysis.com, retrieved 2026-08-24 (external) | — | — | **UNVERIFIABLE** — a single external public source, no stored capture of the pages. The internal cross-check (:41-50, stored closes inside current-basis 52-week ranges) is a document assertion, not a stored artifact |
| C14 | "the registered cap of 100 USD per rolling 365 days, about 1.75 times the worst-case fractional projection"; demonstrated at 100.01 | REGISTRATION.md:196-198; refusals.md:131-151 | 1.75; 100.01 | registered.py:59; demo_spend_ledger.jsonl, 3 rows | 100 / 56.84 = **1.7593**; ledger 60.00 (2026-05-11) + 40.01 (2026-08-20) = **100.01**, the 25.00 at 2025-08-10 correctly outside 365 days of 2026-08-25 | printed | **VERIFIED** |
| C15 | "Tiered cap 0.5 pct, min 0.35. Fixed cap 1 pct, min 1.00 … cap equals minimum at 70 USD Tiered and 100 USD Fixed" | ACCESS.md:65-67 | 70, 100 | commission.py:43-54, 116-121 | 0.35 / 0.005 = **70.0**; 1.00 / 0.01 = **100.0**; every row of the ACCESS.md:127-141 table reproduces (spot-checked 30/tiered 0.1500 cap, 3.54 bp reg, 103.5 bp RT; 180/fractional 1.8000, 200.8 bp RT) | exact | **VERIFIED** (the derivation). The *published schedules* themselves are external quotes with URLs and retrieval date 2026-08-23 — **UNVERIFIABLE** here, no web access used |
| C16 | "SEC Section 31 at 20.60 per million … FINRA TAF at 0.000195 … The assumed one cent TAF floor is confirmed nowhere"; "gap is 0 to 2.2 bp at 45 USD" | progress.md:202-205; ACCESS.md:98-102 | 0.0000206, 0.000195, 0–2.2 bp | commission.py:18-27 | code carries exactly those rates; 0.01 / 45 × 1e4 = **2.222 bp**, exact TAF on one share 0.0433 bp → gap **0 to 2.2 bp** | printed | **VERIFIED** (the arithmetic). Rates themselves external → UNVERIFIABLE here. The floor is explicitly disclosed UNMEASURED |
| C17 | "Median book share price at width 20 ranged 36 to 144 USD over the last 6 months" | progress.md:209-211 | 36 – 144 | formations.json `formations` `last_close` | **all 21 median_price cells reproduce, 0 mismatches**; width-20 over the last 6 formations 36.47 … 143.89 | 0.005 | **VERIFIED** |
| C18 | "The eligibility layer advertises 0.0001 increments on all 20 book names" | DECISIONS.md:422-425 | 20/20 | evidence.jsonl, 20 `contract_details` rows | all 20 carry `min_size` "0.0001" and `size_increment` "0.0001" | exact | **VERIFIED** |
| C19 | "daily bars past the recorded round's pull end of 2026-07-24 for exactly 1,535 symbols" | DECISIONS.md:89-90 | 1,535 | — | — | — | **UNVERIFIABLE** — no artifact in HFExperiment records this count; it is a property of AiTrader's `analysis_bars.db` |
| C20 | "{'intent': 20, 'refusal': 34, 'would_submit': 1} … plus 3 spend records" | refusals.md:339 | 20/34/1; 3 | demo_ledger.jsonl, demo_spend_ledger.jsonl | parsed counts **exactly** {intent: 20, refusal: 34, would_submit: 1} over 55 rows; 3 spend rows | exact | **VERIFIED** |
| C21 | "158 tests green"; 123, 76, 27; "All four required mutations … each caught" | progress.md:92-96, 141, 179, 218 | 158/123/76/27; 3+2+3+4 | tests/ at HEAD; the four mutation_tests.txt | HEAD carries **exactly 158** `def test_` functions across 27 test files; A.2 file internally consistent (5+71 = 76, 2+74 = 76); C.1 file ends "158 passed"; 12 mutations recorded CAUGHT | exact | **VERIFIED**. Note: the C.1 pytest paste shows 72 + 14 dots against "[ 91%]"/"[100%]" — one 72-dot line was dropped in transcription (72+72+14 = 158, 144/158 = 91.1 %). Transcription artifact, not a count error |
| C22 | "the operator's probability that the sleeve ever clears its verdict at 0.15" | REGISTRATION.md:276-278, :289 | 0.15 | — | a stated prior, not a measurement; recorded before the series started and confirmed unchanged at acceptance (ADR-014) | n/a | **VERIFIED as recorded** (no numeric content to check) |
| C23 | "The live track was never funded … The shadow series was disarmed before its first accrual … The verdict was never computed." | REGISTRATION.md:308-313 | 0 capital, 0 observations | reports/monitor/verdict.txt:5,14,23 (`observations: 0`, `bounds: none`); health.txt:8 (`last run: never`); live untracked state per inventory §1.3 | verdict.txt and health.txt corroborate at the anchored SHA. The inventory's live reads (`data/bars.db` all tables 0 rows, `data/ledger/` empty, timer `disabled`/`inactive`, absent from `list-timers`, read 2026-09-03T23:58–23:59Z) corroborate **UNANCHORED** | — | **VERIFIED** |
| C24 | "the `account_not_pinned` refusal is demonstrated against DU999999" | ACCESS.md:213 | DU999999 | refusals.md:197,203; demo_c1.py:310; test_gatewire.py:117; test_brokerconfig.py:61,64 | every producing site and the evidence file use **DU9999999** (one more 9) | exact | **CONTRADICTED** → DRAFT-V-4 |

---

## 2. Derived quantities table

Every row recomputed by me from stored primitives; none taken from a document.

| # | derived quantity | inputs (file:line) | method | recomputed | stated | agrees |
|---|---|---|---|---|---|---|
| D1 | width-5 book median quoted spread | book_spreads.json:19,25,31,37,43 (WOLF/AXTI/SNDK/BE/LITE `median_bp`) | median of 5 | 13.075182 bp | 13.08 (cost_table.md:36) | ✔ |
| D2 | width-5 book median mid | same rows, `median_mid` | median of 5 | 201.90750 USD | 201.91 (cost_table.md:36) | ✔ |
| D3 | width-5 fractional round trip | costmodel.py:113-132; commission.py:97-99,103-113 | 2 × max(180 × 0.01, 0.01)/180×1e4 + (180×0.0000206 + max(0.8915×0.000195, 0.01))/180×1e4 + 13.0752 | 200.0000 + 0.76156 + 13.07518 = **213.8367** bp | 213.84 | ✔ |
| D4 | book median mid / median spread (all 20) | book_spreads.json `per_name` | medians of 20 | 103.2525 USD / 12.773176 bp | 103.25 / 12.77 (cost_table.md:3) | ✔ |
| D5 | daily noise implied by TE 66.4 %/yr | REGISTRATION.md:256-257 | 0.664/√252 × 1e4 | **418.28** bp/day | 418 (registered.py:105) | ✔ |
| D6 | IR from excess and TE | REGISTRATION.md:113-118 | excess × 252 / (TE × 100) | w5 **1.0623**, w50 **0.7981**, w10 0.975, w20 0.894 | 1.062 / 0.798 / 0.975 / 0.894 | ✔ — the 252-day annualisation is required and is stated in no document |
| D7 | pointwise days to clear zero | REGISTRATION.md:255-258 | (Φ⁻¹(0.95) × 418 / 27.99)² | **603.4** days | "about 600 days" | ✔ |
| D8 | sequential inflation over pointwise | verdict.py:26-34 at t = 1600, α = 0.05 | ACS radius / pointwise radius | 0.075878 / 0.041121 = **1.8452**; 600 × 1.8452² = **2043** | day 2061 (:261) | ✔ (internally coherent) |
| D9 | projection in years | REGISTRATION.md:261-262 | 2061/252, 2852/252 | **8.18** and **11.32** years | "Eight to eleven years" | ✔ |
| D10 | spend cap multiple | REGISTRATION.md:196-198 | 100 / 56.84 | **1.7593** | "about 1.75 times" | ✔ |
| D11 | months to 200 fills | REGISTRATION.md:101-104 | 200/10.4, 200/4.0 | **19.23**, **50.0** | "about 19 months instead of 50" | ✔ |
| D12 | ADR-015 forfeited fraction | DECISIONS.md:250-252 | 5 / 2061 | **0.243 %** | "0.2 percent of a 2,061-day clock" | ✔ |
| D13 | TAF worst-case gap at 45 USD | ACCESS.md:100-102 | 0.01/45×1e4 vs 0.000195/45×1e4 | **2.222 bp** vs 0.043 bp | "0 to 2.2 bp" | ✔ |
| D14 | commission crossovers | commission.py:116-121 | min/cap | **70.0 / 100.0** | 70 / 100 | ✔ |
| D15 | A.1-to-A.2 median gap | formations.json + book_spreads.json | 103.2525/143.895 | **0.717554**, gap 28.24 % | 0.7176, 28.2 % | ✔ |
| D16 | one-share cost, 2026-07-01 width-20 book | formations.json `last_close`, n = 20 | Σ closes | **7,890.47 USD** | "about 2,880 USD" (REGISTRATION.md:152-153) | ✘ — 2,880 is 20 × the median, not the book |
| D17 | one-share cost, 2026-07-01 width-5 book | formations.json `last_close`, n = 5 | Σ closes | **3,554.82 USD** (SNDK alone 2,273.73) | "720 of 900 deployed" (REGISTRATION.md:153) | ✘ |
| D18 | kill-floor sigma and touch | REGISTRATION.md:216-222; TE(20) 42.54 | σ = 900 × 0.4254 = 382.90; 2Φ(−loss/σ) | 500 loss → 1.3059σ → **19.15 %**; 400 loss → 1.0446σ → **29.6 %**; 600 loss → 1.5670σ → **11.71 %** | "a 400 USD loss … 1.31 sigma … near 19 percent" | ✘ on the 400/1.31 pairing; ✔ on 1.31σ→19 %, on 600→30 %, and on the 7-point gap (19.15 − 11.71 = 7.4) |
| D19 | hurdle under the whole-share regimes | costmodel.py; commission.py; same width-5 inputs | round trip then daily_cost_hurdle_bp | Tiered RT 52.73 bp → **1.0043** bp/day; Fixed RT 124.95 bp → **2.3800** bp/day | registered 4.07 (fractional) | consistency note, not a discrepancy: the regime is registered explicitly at REGISTRATION.md:249-251 and the 2026-08-25 amendment says "No parameter changes" (:304). After A.1b proved fractional unavailable, the registered success bar is ~4× the bar the only reachable regime implies — a *conservative* direction, and disclosed |
| D20 | study-wide alpha across the three widths | REGISTRATION.md:97-99; verdict.py:104-116 | union bound 0.05 + 0.025 + 0.025 | **0.10** | "the family never outspends the primary" | ✔ under the code's own scope ("the secondaries split 0.05 between them", verdict.py:111-113 → 0.025+0.025 = 0.05 = the primary's 0.05); the union over all three widths is 0.10. Never spent: 0 observations |
| D21 | projection at the secondary level | verdict.py:119-133 at α = 0.025 | first_crossing_day | zero at day **2404**, hurdle at day **3321** | verdict.txt:19-20,28-29 print 2061 / 2852 inside the α = 0.025 blocks | not a discrepancy: the line is labelled "registered projection at the recorded **width-5** mean" and is the registered constant (registered.py:106-107), pinned by the monitor allowlist (monitor.py:139-142) |
| D22 | A.1b order count | evidence.jsonl | count `order_request` rows | **5** | "Five orders of the ten-order cap used" (a1b_report.md:5) | ✔ — note the ledger's own `orders_placed_total {count: 4, cap: 10}` row was written 03:06:14.859Z, 51 s *before* the control order at 03:07:06.141Z, so the counter is stale within its own file. Hygiene only |
| D23 | sequential-inflation prose vs the projection | REGISTRATION.md:258-262 | — | stated expectation "order 1,000 to 2,000 trading days"; the same paragraph then gives **2,061** | — | the realized figure sits just outside the stated band. Loose "order of" language; hygiene only |
| D24 | ACCESS.md sub-test count | ACCESS.md:179-180, :192-200; DECISIONS.md:436, :450-452 | count table rows | table has **7** rows (4 RESOLVED, 2 MOOT, 1 RUNNABLE) | "settled four of the six sub-tests"; "all six sub-tests BLOCKED-ON-OPERATOR" | ✘ on the count 6 vs 7. ACCESS.md:86-87 records that "Task 3 gains a sub-test", which plausibly explains a 6→7 growth. Hygiene only; not raised |

---

## 3. Intervals table

**There is not one realized interval in this repository.** Every row below is a *construction* or a
*planning projection* evaluated at zero observations. `reports/monitor/verdict.txt:5-6,14-15,23-24`
prints `observations: 0` / `bounds: none, the series has not started` at all three widths.

| # | item | file:line | estimator actually used | independence assumed? | data structure the estimator would face | does it reproduce? | status |
|---|---|---|---|---|---|---|---|
| I1 | Studentized asymptotic confidence sequence on daily shadow excess return | REGISTRATION.md:246-248; verdict.py:8-16, 26-34 | radius = σ̂_t · √( 2(tρ²+1)/(t²ρ²) · ln( √(tρ²+1)/α ) ), σ̂_t the running sample SD. This is the Waudby-Smith–Ramdas asymptotic CS boundary. **verdict.py cites no source for the formula** | **Yes** — the asymptotic CS rests on a time-uniform CLT for i.i.d.-or-martingale-difference increments with a running variance estimate | daily book-minus-equal-weighted-universe excess returns, n = **0**. Had it run: a single daily time series per width, monthly re-formation, three widths overlapping by construction (the width-5 book is the first five names of the width-20 book, cost_table_a2.py:35-36), so the three sequences are heavily dependent on each other and each is a serially-correlated, volatility-clustered daily series | **The construction reproduces exactly** (ρ, radius, crossing days — see C9/D8). No data exists to evaluate it on | **VERIFIED as a construction; UNVERIFIABLE as an interval** — n = 0 |
| I2 | Primary level α = 0.05 one-sided, width 5 | REGISTRATION.md:97-99; registered.py:67; verdict.py:104-116 | fixed level fed to I1 | — | 3 registered widths | `alpha_for_width(5)` = 0.05, pinned by tests/test_verdict.py:60 | **VERIFIED** (level as registered) |
| I3 | Secondary levels α = 0.025, widths 20 and 50 | REGISTRATION.md:97-99; verdict.txt:13,22 | Bonferroni split of 0.05 across the two secondaries | — | 2 secondary widths, each an overlapping superset of the primary book | `alpha_for_width(20)` = `alpha_for_width(50)` = 0.025 | **VERIFIED** (level as registered). See the Tests table for the correction analysis |
| I4 | ρ frozen at 0.071641, minimising the radius at t\* = 1600 | REGISTRATION.md:248; registered.py:91; verdict.py:37-66 | golden-section on log₁₀ρ, 200 iterations, deterministic | n/a | n/a | **reproduced 0.071641330** by my own golden-section and **0.0716407** by an independent 150,001-point grid | **VERIFIED** |
| I5 | Success rule: lower bound > 4.07 bp/day | REGISTRATION.md:249-251; verdict.py:97-98 | one-sided lower bound of I1 against a fixed hurdle | as I1 | n = 0 | hurdle reproduces (C2); never evaluated | **VERIFIED as a rule; UNVERIFIABLE as a result** |
| I6 | Futility rule: upper bound < 10 bp/day | REGISTRATION.md:251-252; registered.py:70; verdict.py:99-100 | upper bound of the *same* symmetric radius, at the *same* α | as I1 | n = 0 | never evaluated | **VERIFIED as a rule** — see the Tests table on the two-tail alpha question, which verdict.py:74-77 discloses |
| I7 | Rendered bounds, all three widths | verdict.txt:5-6, 14-15, 23-24 | — | — | 0 observations | literally `observations: 0` / `bounds: none, the series has not started`; verdict CONTINUE | **VERIFIED** (the render honestly reports emptiness) |
| I8 | Planning projection, day 2061 / day 2852 | REGISTRATION.md:260-262; registered.py:106-107 | `first_crossing_day` assuming the sample mean sits at 27.99 with σ = 418 forever | as I1, plus a counterfactual constant mean | 0 (counterfactual) | **2061 and 2852 reproduce exactly** at α = 0.05 with ρ = 0.071641 | **VERIFIED as arithmetic.** Its two inputs (27.99, 418) are C3, which is UNVERIFIABLE here. verdict.py:125-128 labels it "Planning arithmetic only … which no sample does" |
| I9 | Pointwise sanity, "about 600 days" | REGISTRATION.md:255-258 | pointwise one-sided normal | i.i.d. daily | 0 | (1.645 × 418/27.99)² = **603.4** | **VERIFIED** |
| I10 | Driftless first-passage touch probabilities, ~19 % / ~30 % / ~12 % | REGISTRATION.md:218-222; DECISIONS.md:174-178 | reflection principle 2Φ(−k) over one year, σ = 900 × TE(20) = 382.90 USD | driftless Brownian motion, constant σ, **tracking error used as the equity-drawdown σ** (i.e. benchmark treated as flat) | n = 0; the σ itself is interpolated from a 2-point fit (C12), whose endpoints are C3 | 19.15 % / 29.6 % / 11.71 % reproduce; the pairing with "a 400 USD loss" does not (C5) | **CONTRADICTED on one pairing** → DRAFT-V-2. The beta approximation is **disclosed** at REGISTRATION.md:222-224 ("The figures ignore market beta, which the high-beta book makes optimistic") |
| I11 | Reproduction "checks" | universe_check.json; reproduce_log.txt:1,21 | **exact set/rank/value equality** — no statistic, no tolerance, no interval | n/a | 124 formation dates; 10 dates × 500 rows | all 10 rows exact, all mismatch arrays empty | **VERIFIED** (as an equality check, correctly not presented as a test) |
| I12 | Formation-hash check | refusals.md:9 | exact hash equality | n/a | 1 formation | — | **VERIFIED as recorded** (a stored equality assertion) |
| I13 | Spread distribution quantiles | book_spreads.json:139-147 | order statistics, no interval, no SE | per-name medians treated as 20 exchangeable draws; **the 180 underlying cells are 3 sessions × 3 windows within name**, so the cells are not independent — but no interval is claimed on them, only per-name medians | 20 names × 9 cells | every quantile reproduces exactly (lower-order-statistic convention) | **VERIFIED** — and correctly reported as a distribution, not as an interval |
| I14 | Mutation "tests" | the four mutation_tests.txt | pass/fail of named pytest cases, not a statistic | n/a | 12 source mutations | 3 + 2 + 3 + 4 = 12, each recorded CAUGHT with named failing tests | **VERIFIED** |

**Independence verdict.** No interval was ever computed, so no independence assumption was ever
*exercised*. The one place where the structure would have mattered — I1 across three widths whose
books nest inside one another — is handled by a Bonferroni split rather than by any dependence
model; with 0 observations there is nothing to recompute clustered or blocked, and I therefore make
no claim that any stated comparison would move.

---

## 4. Tests table

**There is no hypothesis test and no p-value in this repository.** The rows below record the
decision rules, their tails, their levels and their multiplicity treatment, because those are what
a test would have consumed.

| # | test / rule | file:line | tail | dof / distribution | correction applied | decision-rule type | correction matches rule? | reproduces? | status |
|---|---|---|---|---|---|---|---|---|---|
| T1 | Success at the primary width: lower bound > 4.07 bp/day | REGISTRATION.md:249-251; verdict.py:97-98 | **one-sided, lower** — matches the registered direction ("earn **positive** daily excess return", REGISTRATION.md:47-53) | asymptotic (time-uniform CLT), no dof parameter; α enters only as ln(√(tρ²+1)/α) | none needed for the primary alone | single | n/a | boundary reproduces exactly | **VERIFIED as specified.** Note: the WSR radius is normally stated as a **two-sided** (1−α) sequence. Used one-sidedly at the same α it is conservative, never anti-conservative. The repository cites no source for the formula, so I cannot settle from this repository alone which convention the author intended — flagged, not raised |
| T2 | Futility: upper bound < 10 bp/day | REGISTRATION.md:251-252; verdict.py:99-100 | one-sided, upper | as T1 | none | single | n/a | boundary reproduces | **VERIFIED.** Both bounds use the *same* radius at the *same* α, so the two rules together read a symmetric interval whose two-sided error is at most 2α if the radius is one-sided, or α if it is two-sided. verdict.py:74-77 **discloses** this exactly: "Each side holds at level alpha one-sided, which is how both the success rule and the futility rule read it" |
| T3 | The width family: primary 0.05 + secondaries 0.025 each | REGISTRATION.md:97-99; verdict.py:104-116; DECISIONS.md:160-167 | one-sided at every width | as T1 | **Bonferroni**, 0.05 split into 0.025 + 0.025 across the two secondaries | **union / disjunction** (any width may declare SUCCESS; the *verdict* is the primary's, REGISTRATION.md:92) | **Yes** — Bonferroni is the right family for a union rule, and the split is arithmetically exact for the scope the code states ("The secondaries split 0.05 between them … so the family never spends more than the primary", verdict.py:111-113) | 0.05 / 0.025 / 0.025 reproduce from `alpha_for_width` | **VERIFIED.** For the record: the union bound over **all three** widths is 0.05 + 0.025 + 0.025 = **0.10**, twice the primary's level. The sentence at REGISTRATION.md:98-99 is true of the secondary family, which is what its own subject is and what the code documents; it is not true of the three-width family. Zero alpha was ever spent (0 observations), so nothing turns on it |
| T4 | Kill-floor touch probability | REGISTRATION.md:216-222; DECISIONS.md:171-179 | two-sided tail formula 2Φ(−k) used as a **one-sided** first-passage probability for driftless BM (correct: P(min over [0,1] < −kσ) = 2Φ(−k)) | normal, no dof | none | single | n/a | 19.15 / 29.6 / 11.71 % reproduce | **CONTRADICTED on the loss figure it is attached to** → DRAFT-V-2 |
| T5 | Reproduction agreement | universe_check.json; reproduce_log.txt | n/a — exact equality, deliberately not a test | n/a | none | conjunction (all 10 dates must match) | n/a — an exact-equality conjunction needs no correction, and none is applied | all 10 exact | **VERIFIED**, and correctly *not* dressed as a statistical test |
| T6 | Mutation checks | the four mutation_tests.txt | n/a | n/a | none | conjunction (every mutation must be caught) | n/a | 12/12 CAUGHT | **VERIFIED** |

No conjunction / all-must-pass rule in this repository carries a union-type correction, and no
intersection-union rule is over-corrected. The only multiplicity correction present (T3) sits on a
genuine union rule, which is the correct pairing.

---

## 5. Draft findings

### DRAFT-V-1
- **Repository / SHA:** HFExperiment / 82e77a021256d917c665ff6d4304c25b08f35451
- **Hypothesis or artifact:** REGISTRATION.md Section 6, "The DEGRADED branch, closed" — the arithmetic that closes a pre-registered Section 0 branch
- **Direction:** neutral — every error runs in the direction that makes the DEGRADED branch *less* affordable than the document states, so the registered consequence ("NO live sleeve at this stake") holds a fortiori. The defect is in the stated arithmetic of a binding registration, not in its conclusion
- **Class:** ARITHMETIC
- **Severity:** S2 — a stated figure contradicts the artifact the same paragraph cites
- **Label:** DERIVED
- **Claim challenged (verbatim quote):** "A.1 measured it: 144 USD at the last two formations, up from 36 in March and April. At 144, whole-share sizing on 900 USD cannot fill a 20-name book at all, because 20 names at one share each already cost about 2,880 USD. A 5-name book gets one share per name, 720 of 900 deployed, with equal weighting destroyed by per-name prices from 22 to 1,595 USD." — HFExperiment/REGISTRATION.md:149-154 (restated at HFExperiment/DECISIONS.md:194-199, ADR-012)
- **Evidence:**
  - The stored 2026-07-01 width-20 book, n = 20 names, `last_close` values in HFExperiment/reports/stage_a1/formations.json (`formations` → `2026-07-01` → `20`): one share of each costs **7,890.47 USD**, not "about 2,880 USD". 2,880 is 20 × the median (143.89), which is not the cost of the book.
  - The stored 2026-07-01 width-5 book, n = 5 (WOLF 48.25, AXTI 72.08, SNDK 2,273.73, BE 302.70, LITE 858.06), same file: one share of each costs **3,554.82 USD**, not "720 of 900 deployed". **SNDK alone at 2,273.73 exceeds the entire 900 USD deployed**, so "one share per name" is not purchasable at this stake at all. The width-5 book's own median close is 302.70 (formations.json `median_price` → `2026-07-01` → `5`), not the 144 the sentence applies to it.
  - "up from 36 in March and April": stored width-20 medians are March 36.47 and **April 40.59** (formations.json `median_price`; rendered at HFExperiment/reports/stage_a1/formations.md:24-25). April is not 36.
  - "per-name prices from 22 to 1,595 USD": no stored price set in this repository has a minimum near 22. 1,595.19 and 22.305 appear as SNDK's and PL's A.2 median mids (HFExperiment/reports/stage_a2/book_spreads.json:33, :51), but the minimum of that same 20-name set is ONDS at 8.745 (:75), with WULF 15.71 (:111) and CIFR 15.845 (:129) also below 22; and PL is not in the width-5 book the sentence is about. On the July closes the width-5 range is 48.25 to 2,273.73 and the width-20 range is 8.24 to 2,273.73.
  - The three quantities that *do* verify: 143.80 and 143.89 at the last two formations, and all 21 cells of the median-share-price table, which I reproduced from the stored `last_close` values with **0 mismatches**.
- **Recomputation:** inputs `HFExperiment/reports/stage_a1/formations.json` (`formations.2026-07-01.{5,20}[].last_close`, n = 5 and n = 20) and `HFExperiment/reports/stage_a2/book_spreads.json` (`per_name.*.median_mid`, n = 20). Method: direct sum, min, max and median with Python `statistics`, no rounding before comparison. Results: Σ width-20 = 7,890.47; Σ width-5 = 3,554.82; max width-5 close 2,273.73; min width-20 mid 8.745; April width-20 median 40.59. Tolerance: 0.01 USD. Script `.../work/agentC-verify-HF/recompute.py`.
- **What would resolve it:** either restating Section 6's arithmetic on the actual per-name closes (which strengthens the closure — the 20-name book costs 2.7× and the 5-name book 4.9× what the document states), or an explicit sentence saying the 2,880 and 720 figures are median-times-count illustrations rather than book costs; plus naming the source of the "22 to 1,595" range.
- **Confidence:** HIGH — the contradicting values are the stored per-name closes in the very file Section 6's measurement is drawn from, and the arithmetic is a sum.
- **Invalidated by later commits?:** no — the repository is closed and terminal (REGISTRATION.md:306-315), HEAD is the anchored SHA, and formations.json has not been touched since a8f4b0d/91a1dcb.
- **Disclosed by authors?:** no. Section 6 and ADR-012 both present the 2,880 / 720 arithmetic as measurement. The one adjacent disclosure is the same sentence's "equal weighting destroyed by per-name prices", which acknowledges dispersion without correcting the figures it sits beside.

### DRAFT-V-2
- **Repository / SHA:** HFExperiment / 82e77a021256d917c665ff6d4304c25b08f35451
- **Hypothesis or artifact:** REGISTRATION.md Section 9, the registered restart floor and its touch-probability justification
- **Direction:** neutral — hygiene inside a registered kill criterion. The registered *level* (500 USD) and its 1.31σ / 19 % justification are correct; only the descriptive loss figure attached to them is not, and no capital was ever deployed (REGISTRATION.md:308-309)
- **Class:** ARITHMETIC
- **Severity:** S4
- **Label:** DERIVED
- **Claim challenged (verbatim quote):** "The floor is 500 USD of total account equity, a 400 USD loss on 900 deployed after the 100 buffer, 1.31 sigma of the width-20 tracking error, driftless touch probability near 19 percent in year one." — HFExperiment/REGISTRATION.md:216-218
- **Evidence:**
  - σ used throughout Section 9 and ADR-011 is 900 USD × TE(20) = 900 × 42.54 % = **382.90 USD** (TE(20) from the interpolation at HFExperiment/REGISTRATION.md:117, reproduced in C12).
  - A **400 USD** loss is 400/382.90 = **1.045 σ**, touch 2Φ(−1.045) = **29.6 %** — not 1.31 σ and not 19 %.
  - The stated 1.31 σ and 19 % require a **500 USD** loss: 500/382.90 = **1.306 σ**, 2Φ(−1.306) = **19.15 %**. That is exactly (1000 total equity − 500 floor), the basis ADR-011 uses for all three of its numbers.
  - ADR-011 is internally consistent on that basis and never states a loss figure: "600 is 1.04 sigma … near 30 percent … 500 is 1.31 sigma, near 19 percent. 400 is 1.57 sigma, near 12 percent" (HFExperiment/DECISIONS.md:174-179). I reproduce 1.045 σ / 29.6 %, 1.306 σ / 19.15 %, 1.567 σ / 11.71 %, and the "7 more points" of REGISTRATION.md:220-221 as 19.15 − 11.71 = 7.4. n = 0 observations; these are design projections.
  - Under the alternative reading — that the 100 buffer is consumed first, so the sleeve starts at 900 and 900 → 500 is a 400 loss — the touch probability would be 29.6 %, again not the 19 % stated in the same sentence. **Neither reading makes all three of (400 loss, 1.31 σ, 19 %) true.**
- **Recomputation:** inputs TE(20) = 42.54 %/yr (REGISTRATION.md:117, itself reproduced from the two-point fit at DECISIONS.md:143-147), deployed 900 USD (REGISTRATION.md:133). Method: σ = 900 × TE; k = loss/σ; touch = 2Φ(−k) with `scipy.stats.norm`. Results as above. Tolerance: 0.01 σ and 0.5 percentage points.
- **What would resolve it:** replacing "a 400 USD loss on 900 deployed after the 100 buffer" with "a 500 USD loss of total equity, leaving 400 in the sleeve", which is what the 1.31 σ and the 19 % already encode. Nothing else in Section 9 or ADR-011 moves.
- **Confidence:** HIGH on the arithmetic — the three figures cannot be simultaneously true under either reading of the sentence. MEDIUM on materiality: this most likely reads as "down to 400" rather than "a 400 loss", and the operative registered number (500) and its justification are correct.
- **Invalidated by later commits?:** no — closed repository, HEAD is the anchored SHA, and REGISTRATION.md is append-only with the Section 9 text landed at a8f4b0d and never edited.
- **Disclosed by authors?:** no for the arithmetic. The authors *do* disclose the surrounding modelling limits at REGISTRATION.md:222-224 ("The figures ignore market beta, which the high-beta book makes optimistic, and ignore positive drift"), and ADR-011:188 offers "a measured book beta would refine the touch probabilities" — neither touches the loss figure.

### DRAFT-V-3
- **Repository / SHA:** HFExperiment / 82e77a021256d917c665ff6d4304c25b08f35451
- **Hypothesis or artifact:** the Stage A.1b session descriptor — the provenance of the session that fired Section 0's BLOCKED
- **Direction:** neutral — pure provenance hygiene. The BLOCKED verdict itself is fully supported (C1 VERIFIED); no registered number depends on the Gateway's server version
- **Class:** PROVENANCE
- **Severity:** S3
- **Label:** DERIVED
- **Claim challenged (verbatim quote):** "Run 2026-08-25, 02:57 to 03:07 UTC, Monday 22:57 to 23:07 ET, market closed. Gateway 127.0.0.1:4002, server version 187, account [paper account ID removed], declared mode paper." — HFExperiment/reports/stage_a1b/a1b_report.md:3-4. Repeated at HFExperiment/DECISIONS.md:408 (ADR-022), HFExperiment/DECISIONS.md:439 (ADR-026), HFExperiment/docs/ACCESS.md:178, HFExperiment/progress.md:235
- **Evidence:**
  - The A.1b session's own primary record, row 2 of HFExperiment/reports/stage_a1b/evidence.jsonl: `{"kind": "connected", "managed": ["[paper account ID removed]"], "server_version": 178, "utc": "2026-08-25T03:05:16.497779Z"}`. n = 1 connection record, and it is the only connection record in that file (I parsed all 51 rows: 1 `stage_start`, 1 `connected`, 20 `contract_details`, 10 `api_error`, 2 `quote_snapshot`, 2 `quantity_computed`, 5 `order_request`, 5 `order_outcome`, 1 `fills`, 2 `final_positions`, 1 `orders_placed_total`, 1 `cancel`).
  - **187 is a real observed value, but from a different session**: the C.1 read-only probe of 2026-08-25T02:40Z records `"server_version": 187` at HFExperiment/reports/stage_c1/refusals.md:332, in a probe record whose `server_time_epoch` is 1787625630. So five of the six prose retellings attribute the C.1 probe's version to the A.1b session.
  - Everything else in the descriptor checks out against the ledger: account [paper account ID removed] (`stage_start`, `connected`, `final_positions`), declared mode paper (`stage_start`), and the 03:05:15.955Z–03:07:17.172Z span.
- **Recomputation:** none required — a direct read of a stored JSONL field against five prose statements. Read from SNAP/HFExperiment/reports/stage_a1b/evidence.jsonl.
- **What would resolve it:** an appended note in ADR-022 or the A.1b report recording that the A.1b connection reported server version 178 and that 187 comes from the C.1 probe — or, if the 178 in the ledger is itself a bug in `scripts/a1b_capability_test.py`'s capture, a note saying so. Either way the ledger and the prose should agree about which number came from which connection.
- **Confidence:** HIGH — the ledger field is unambiguous and singular, and the divergent 187 is traceable to a different, timestamped record.
- **Invalidated by later commits?:** no — evidence.jsonl landed at 669eb5c (2026-08-24T20:09:06-07:00) and the last prose repetition landed at HEAD 82e77a0 (2026-08-28); the repository is closed.
- **Disclosed by authors?:** no. ADR-026 (DECISIONS.md:432-454) is precisely a self-reported record-hygiene correction about A.1b's provenance, and it repeats "server version 187" at :439 without noticing the ledger says 178.

### DRAFT-V-4
- **Repository / SHA:** HFExperiment / 82e77a021256d917c665ff6d4304c25b08f35451
- **Hypothesis or artifact:** docs/ACCESS.md's citation of the C.1 account-pin demonstration
- **Direction:** neutral — hygiene
- **Class:** INTERNAL_INCONSISTENCY
- **Severity:** S4
- **Label:** DERIVED
- **Claim challenged (verbatim quote):** "the `account_not_pinned` refusal is demonstrated against DU999999 in `reports/stage_c1/refusals.md`" — HFExperiment/docs/ACCESS.md:212-214
- **Evidence:** the cited artifact and every producing site use **DU9999999** (seven nines, not six): HFExperiment/reports/stage_c1/refusals.md:197 ("intent.account DU9999999 != pinned IBKR_ACCOUNT_ID [paper account ID removed]") and :203 (the same string inside the written ledger record); HFExperiment/scripts/demo_c1.py:310; HFExperiment/tests/test_gatewire.py:117; HFExperiment/tests/test_brokerconfig.py:61 and :64. n = 5 sites against 1. A grep for `DU999999` across the snapshot returns exactly these six hits and no other.
- **Recomputation:** none — string comparison across the snapshot.
- **What would resolve it:** correcting the account id in ACCESS.md:213 to DU9999999.
- **Confidence:** HIGH — a single-character mismatch, exhaustively enumerated.
- **Invalidated by later commits?:** no — ACCESS.md:212-215 landed at HEAD 82e77a0 and the repository is closed.
- **Disclosed by authors?:** no.

---

## 6. What could not be checked, and why

1. **The holdout width figures (C3) — the largest unchecked dependency in the repository.**
   27.99 bp/day, 66.40 %/yr and IR 1.062 at width 5, and 10.04 / 31.70 / 0.798 at width 50, exist
   in HFExperiment **only as literals**: `scripts/cost_table_a2.py:31-34` (with the comment
   "recorded in the A.2 stage prompt"), `src/hfexperiment/registered.py:104-105`, and the table
   rows at `REGISTRATION.md:113-118`. There is **no data file, no notebook, no log and no report**
   anywhere in this repository holding them, and **no n, no sample window, no standard error and no
   t-statistic is stated for them anywhere**. What rests on them: the registered hypothesis
   (REGISTRATION.md:52-56), the choice of width 5 as PRIMARY (:92-95), the entire two-point power
   law and its four interpolated cells (:110-118, ADR-009), the σ = 418 bp/day used by the
   projection, and the day-2061 / day-2852 arithmetic. The declared origin is the AiTrader
   cross-sectional round of 2026-07-26 (README.md:3-5, `src/hfexperiment/benchmark.py:5-9`), which
   this task does not cross into. What I *could* check and did: their **mutual** consistency is
   exact — IR = excess × 252/(TE × 100) gives 1.0623 and 0.7981, and TE 66.4 %/yr implies
   418.28 bp/day — so the six numbers are one coherent set under a 252-day annualisation that no
   document in the repository states. Status: **UNVERIFIABLE**, not contradicted.
2. **The A.1 reproduction itself (C8, C19).** `scripts/reproduce_formation.py` reads
   `/home/kiros-li/Documents/GitHub/AiTrader/analysis_bars.db` (`src/hfexperiment/dbaccess.py:13`).
   I verified its stored outputs exhaustively (reproduce_log.txt, universe_check.json,
   db_hash_before/after.txt byte-identical) but cannot re-derive the 124 dates, the 10 × 500 rows,
   the 19,744 segmented symbols or ADR-005's 1,535 partially-refreshed symbols without opening
   AiTrader's database, which is outside this task.
3. **Every external figure.** The IBKR published schedules and their quoted disclosure text
   (ACCESS.md:52-67, :71-76, :165-167), the SEC §31 and FINRA TAF rates (:91-106), the four broker
   rows, and the stockanalysis.com corporate-actions check behind the price reconciliation
   (price_reconciliation.md:18-34). All carry URLs and retrieval dates; none has a stored capture
   in the repository; no web access was used by this task. Their **derivations** verify (C15, C16,
   D13, D14).
4. **Anything the shadow series would have produced.** Zero observations exist. I1–I8 are
   constructions and projections; there is no interval, no test statistic and no p-value to
   reproduce, and no clustered or block-bootstrap alternative to compute.
5. **The provenance of the ACS formula.** `src/hfexperiment/verdict.py:8-16` states the radius
   without citing a source. Whether the α in `ln(√(tρ²+1)/α)` is the two-sided or the one-sided
   level of the underlying construction cannot be settled from this repository. Using it one-sidedly
   at α = 0.05 is conservative under the two-sided reading and exact under the one-sided one, so the
   ambiguity cannot make the success rule anti-conservative. Flagged in T1; not raised as a finding.
6. **The live untracked working tree** was not re-read by this task; the §1.3 rows in my inventory
   (bars.db all tables 0 rows, empty `data/ledger/`, disarmed timer) stand as UNANCHORED
   observations read 2026-09-03T23:58–23:59Z and may have changed after the 2026-08-28 anchor.
7. **Not raised, recorded for completeness** (checked, real, but too small or already explained to
   be findings): the stale `orders_placed_total {count: 4}` row written 51 s before the fifth order
   (D22); the "six sub-tests" vs the seven-row table (D24), plausibly explained by ACCESS.md:86-87's
   "Task 3 gains a sub-test"; the dropped 72-dot line in the C.1 pytest paste (C21); the
   "order 1,000 to 2,000 trading days" prose against the same paragraph's 2,061 (D23); and the
   ADR-023/024/025 numbering gap between DECISIONS.md:401 and :432.

**Where the repository is sound, plainly.** The cost model, the commission arithmetic, the spread
measurement, the churn and median-price series, the confidence-sequence construction and its
projection, the C.1 refusal demonstration and its ledgers, the test and mutation counts, and the
Section 0 BLOCKED closure all reproduce exactly from stored primitives. Had the thesis "this
repository over-claims its results" held, I would have expected to find a realized verdict, a
p-value, an interval, or a positive result asserted on the shadow series — **there is none, and the
repository says so in its own monitor output** (`verdict.txt:5-6`: "observations: 0 / bounds: none,
the series has not started"). The one number that would carry a real claim, the 27.99, is imported
and labelled as imported ("the already-spent holdout", "recorded"), and the registration is explicit
that it was spent elsewhere and may not be re-spent (REGISTRATION.md:71-74).

---

## 7. Live-repo access log

Purpose of access, per COMMON_RULES §"When you may touch a LIVE repository": (1) git
history/provenance only. No file under `/home/kiros-li/Documents/GitHub/HFExperiment/` was opened
for writing, no repository script was executed, `.env` was not read, and no untracked data file was
opened by this task.

**`git -C /home/kiros-li/Documents/GitHub/HFExperiment status --porcelain` — BEFORE first access, 2026-09-04T00:18:36Z:**

```
?? Accept:
?? GET
?? Host:
?? User-Agent:
```

**`git -C /home/kiros-li/Documents/GitHub/HFExperiment status --porcelain` — AFTER last access, 2026-09-04T00:20:51Z:**

```
?? Accept:
?? GET
?? Host:
?? User-Agent:
```

Identical, and exactly the four stray files COMMON_RULES records as pre-existing owner dirt.
Nothing else appeared. **No accidental modification occurred.**

| time (UTC) | command | purpose |
|---|---|---|
| 00:18:36 | `git status --porcelain` | pre-access baseline |
| 00:18:3x | `git rev-parse HEAD` | confirmed 82e77a021256d917c665ff6d4304c25b08f35451 |
| 00:18:3x | `git log --format='%h %ad %aI %s' --date=iso-strict` | commit timestamps, to date Sections 1-12 (a8f4b0d, 2026-08-23T21:40:25−07:00 = 2026-08-24T04:40:25Z) against `book_spreads.json` `measured_utc` 2026-08-24T04:23:29Z — the A.2 spread measurement precedes the registration commit by 17 minutes and landed in the **same** commit, which is what makes the "22 to 1,595" question in DRAFT-V-1 answerable at all |
| 00:20:51 | `git status --porcelain` | post-access baseline |

All computation was performed under
`/tmp/claude-1000/-home-kiros-li-Documents-GitHub-program-audit/2c6a58bc-6f69-48c9-a930-b20684f1e1e4/scratchpad/work/agentC-verify-HF/recompute.py`,
reading only from SNAP/HFExperiment, with the audit venv at
`/tmp/claude-1000/-home-kiros-li-Documents-GitHub-program-audit/5ca157a0-1746-4eb9-a1b8-f3732ea42bf4/scratchpad/venv/bin/python`.
