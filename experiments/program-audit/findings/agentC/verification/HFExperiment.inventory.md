# HFExperiment — verification inventory (Agent C, LOCATE)

Repository: HFExperiment
Anchored SHA: 82e77a021256d917c665ff6d4304c25b08f35451 (main, 2026-08-28)
Snapshot read: SNAP/HFExperiment (all tracked content below is from the snapshot;
paths and line numbers are identical to `git show 82e77a0:<path>`).
Live repo touched read-only for git objects, untracked data, and systemd state only.
Prepared 2026-09-03/04 UTC.

Scope note: this repository is CLOSED. REGISTRATION.md:306-315 and progress.md:5-21
record a terminal operator closure dated 2026-08-26, with the live track never funded
and the shadow series disarmed before its first accrual. That is the single most
important structural fact for verification: **the experiment's own verdict instrument
never produced a single observation**, so almost every numeric claim in the repository
is a *design* or *cost/broker measurement* claim, not a result claim. There is no
report.md, no FINDINGS.md, no HYPOTHESES.md and no registrations/ directory in this
repository; the binding documents are REGISTRATION.md, DECISIONS.md, progress.md,
README.md, docs/ACCESS.md and reports/*.

---

## 1. Artifacts

### 1.1 Analysis and threshold code (tracked → ANCHORED)

| path | holds | backs which document figures |
|---|---|---|
| `src/hfexperiment/registered.py` (133 ln) | Every registered numeric threshold as code: `restart_floor_usd=500.0` (:56), `spend_cap_usd_per_year=100.0` (:59), `primary_width=5` / `traded_width=20` / `secondary_widths=(20,50)` (:62-64), `alpha_one_sided=0.05` / `secondary=0.025` (:67-68), `crossing_target_days=1600` (:69), `futility_bp_per_day=10.0` (:70), `cost_hurdle_bp_per_day=4.07` (:78), `CHURN_NAMES_PER_MONTH={5:2.0,20:5.2}` (:85), `RHO_FROZEN=0.071641` (:91), `SHADOW_SERIES_START="2026-09-01"` (:97), `PROJECTION_MEAN_BP=27.99` / `SIGMA=418.0` / `CLEAR_ZERO_DAY=2061` / `CLEAR_HURDLE_DAY=2852` (:104-107), and the three `DeferredParameter` objects (:110-133) | REGISTRATION.md Sections 4, 5, 8, 9, 11, 12; reports/monitor/verdict.txt |
| `src/hfexperiment/commission.py` (121 ln) | IBKR Pro Tiered (0.0035/sh, min 0.35, cap 0.5 %) and Fixed (0.005/sh, min 1.00, cap 1 %) plans; SEC §31 0.0000206; FINRA TAF 0.000195 with worst-case 0.01 floor and 9.79 cap; fractional schedule max(1 % , 0.01); `crossover_notional_usd` | docs/ACCESS.md:50-67, :89-102, :118-153 cost table |
| `src/hfexperiment/costmodel.py` (223 ln) | `round_trip`, `annual_commission_drag`, `daily_cost_hurdle_bp` (:209-223); inherited band (15.8, 50.0) with UNMEASURED carry = 50.0 | reports/stage_a2/cost_table.md, the 4.07 hurdle, the 28.76/56.84 drag |
| `src/hfexperiment/verdict.py` (133 ln) | `acs_radius`, `tuned_rho` (golden-section on log10 ρ), `confidence_bounds`, `classify_verdict`, `alpha_for_width`, `first_crossing_day` | REGISTRATION.md Section 11; day 2061 / 2852; ρ 0.071641 |
| `src/hfexperiment/verdictengine.py` (124 ln) | Wires the sequence over the shadow series; embeds the projection in every record | reports/monitor/verdict.txt |
| `src/hfexperiment/monitor.py` (237 ln) | The two views; verdict view validates each emitted line against a regex allowlist (:142 pins `clears zero at day 2061, clears the hurdle at day 2852`) | reports/monitor/{health,verdict}.txt |
| `src/hfexperiment/universe.py` (336 ln) | Rule U-LIQ-500-stk-w60-m40-p5, header states "COPIED 2026-08-23 from AiTrader backtest/universe.py" | REGISTRATION.md:78, ADR-006, reproduce_log.txt |
| `src/hfexperiment/formation.py` (149 ln) | 12-1 momentum with skip month; ADR-006 anchor conventions; MAX_ANCHOR_GAP_SESSIONS | REGISTRATION.md:80-88, formations.json |
| `src/hfexperiment/shadow.py`, `accrual.py`, `states.py`, `benchmark.py`, `barstore.py`, `alpaca_source.py`, `formationrun.py` | The shadow-series machinery. **Never executed against real data** — see §1.3 | progress.md:121-139 |
| `src/hfexperiment/gate.py`, `gatewire.py`, `brokerconfig.py`, `intents.py`, `kill.py`, `ledger.py`, `spendledger.py`, `ibkrprobe.py`, `mockbroker.py`, `envfile.py`, `config.py`, `dbaccess.py` | Order gate, eight refusals, account pin, kill classification, append-only ledger primitive, read-only TWS probe | REGISTRATION.md Sections 8, 9; reports/stage_c1/refusals.md |
| `scripts/cost_table_a2.py` (137 ln) | The generator for reports/stage_a2/cost_table.md; carries the holdout literals `PRIMARY_EXCESS_BP_PER_DAY=27.99`, `PRIMARY_SIGMA_BP_PER_DAY=418.0` (:33-34) and `WIDTH5_NAMES` (:36) | cost_table.md in full |
| `scripts/cost_table.py` (86 ln) | Generator for the docs/ACCESS.md cost table | ACCESS.md:125-141 |
| `scripts/reproduce_formation.py` (310 ln) | A.1 reproduction driver; reads AiTrader `analysis_bars.db` read-only | universe_check.json, formations.json, formations.md, reproduce_log.txt |
| `scripts/measure_book_spreads.py` (258 ln) | A.2 spread measurement; Alpaca historical SIP quotes, 3 sessions × 3 windows, discard taxonomy | book_spreads.json |
| `scripts/a1b_capability_test.py` (357 ln) | The only order-placing script; 10-order cap, pinned account, SmartRouted, DAY | evidence.jsonl, a1b_report.md |
| `scripts/demo_c1.py` (420 ln) | Produces every refusal against the real 2026-08-03 book | refusals.md, demo ledgers |
| `scripts/fetch_c1_formation.py` (91 ln) | Computes the 2026-08-03 formation into `data/c1_formation.db` | formation_2026-08-03.json |
| `scripts/daily_run.py` (420 ln) | The 23:30 UTC entry point the timer fires | health.txt, verdict.txt |
| `tests/` (27 files, **158 `def test_` functions** at HEAD) | Pins the hurdle re-derivation (test_registered.py:52-69), ρ and 2061/2852 (test_verdict.py:68-74, test_verdictengine.py:24-40), the monitor allowlist, the structural guard | progress.md test counts |

### 1.2 Stored evidence artifacts (tracked → ANCHORED)

| path | holds | backs | n |
|---|---|---|---|
| `reports/stage_a1/formations.json` (3278 ln) | `rule`, `widths`, `formations` (7 dates × widths 5/20/50, each row rank/symbol/momentum/last_close), `churn` block, `median_price` block | formations.md, the 144 USD DEGRADED closure, churn 5.2/2.0 | 7 formations; 5+20+50 rows each |
| `reports/stage_a1/formations.md` (70 ln) | Churn table (6 months × 3 widths), median-share-price table (7 × 3), full name lists | REGISTRATION.md:150-154, ADR-004, ADR-012 | as above |
| `reports/stage_a1/universe_check.json` (101 ln) | 10 formation dates, each `recorded_rows`/`reproduced_rows` 500, empty mismatch arrays, `exact_match: true` | "Universe exact at all 10 checked dates, all 500 rows each" | n=10 dates, 500 rows each |
| `reports/stage_a1/reproduce_log.txt` (21 ln) | `reproduced 124, recorded 124, identical=True`; 19744 symbols segmented; per-formation ranked counts (493-496) and exclusion dicts | REGISTRATION.md:79, progress.md:207 | 124 dates |
| `reports/stage_a1/db_hash_{before,after}.txt` | Identical sha256 `c30d3f44…` of AiTrader/analysis_bars.db | progress.md:211-212 | 1 file |
| `reports/stage_a1/mutation_tests.txt` (4 ln) | 3 mutations CAUGHT; restored line shows **27** progress dots | progress.md:218-220 | 3 mutations / 27 tests |
| `reports/stage_a2/book_spreads.json` (156 ln) | Per-name `n_cells`/`median_bp`/`median_ticks`/`median_mid` for all 20 names; `unmeasured: []`; `distribution` (min 2.141, p25 6.367, median 12.7732, p75 17.2325, p90 20.7306, max 27.4324); `discarded` (crossed 6, locked 88, rest 0); `measured_utc 2026-08-24T04:23:29Z`, feed sip | REGISTRATION.md:170-177, cost_table.md, ADR-013 | 20 names × 9 cells = 180 cells |
| `reports/stage_a2/cost_table.md` (40 ln) | 15-row round-trip table, 6-row annual-drag table, the hurdle derivation line (:36), the verdict arithmetic line (:40) | REGISTRATION.md Sections 7 and 11 | — |
| `reports/stage_a2/mutation_tests.txt` (26 ln) | 2 mutations CAUGHT with named failing tests; "76 passed" | progress.md:179-181 | 2 mutations / 76 tests |
| `reports/stage_a1b/evidence.jsonl` (51 rows) | `stage_start`, `connected` (**`server_version: 178`**, managed `["[paper account ID removed]"]`), 20 `contract_details` (MinSize/SizeIncrement 0.0001), 10 `api_error`, 2 `quote_snapshot`, 2 `quantity_computed`, **5** `order_request` / 5 `order_outcome`, `fills: []`, 2 `final_positions` (both `[]`), `orders_placed_total {count: 4, cap: 10}`, 1 `cancel` | The Section 0 BLOCKED verdict, ADR-022, ACCESS.md Task 3 re-status | 5 orders, 20 contracts, run 03:05:15Z–03:07:17Z |
| `reports/stage_a1b/a1b_report.md` (116 ln) | The rendered A.1b report; **states "server version 187"** (:4), verbatim 10243/10244 logs, the accepted whole-share control, flat positions twice | REGISTRATION.md:297-304 amendment | 5 orders |
| `reports/stage_b1/price_reconciliation.md` (84 ln) | 143.89 vs 103.25, ratio 0.7176 / 28.2 %; zero splits, zero in-window ex-dates; MU 0.15 ex 2026-07-06, WDC 0.60 ex 2026-09-08, STX 2.96 ex 2026-09-24; MXL 0.518, WOLF 0.546; third median 97.45 at 2026-08-24 | ADR-016, progress.md:111-119 | 20 names, public source |
| `reports/stage_b1/mutation_tests.txt` (41 ln) | 3 mutations CAUGHT; "123 passed"; progress dots 72+51 = 123 (consistent) | progress.md:141-145 | 3 mutations / 123 tests |
| `reports/stage_c1/refusals.md` (339 ln) | All 8 refusals with named arithmetic, the 4-way account pin, the construction wall, the priced-and-ready intent, reconciliation stub, probe result (`server_version: 187`), ledger counts `{intent:20, refusal:34, would_submit:1}` | progress.md:70-83, ADR-018/020/021 | 20 intents |
| `reports/stage_c1/demo_ledger.jsonl` (55 rows) | The demonstration ledger records | refusals.md:339 count | 55 |
| `reports/stage_c1/demo_spend_ledger.jsonl` (3 rows) | The seeded rolling-year spend records (60.00 / 40.01 / 25.00) | refusals.md:133-139 | 3 |
| `reports/stage_c1/formation_2026-08-03.json` (112 ln) | `n_members 500`, `n_measurable 494`, books at 5/20, per-name closes | refusals.md:7, ADR-021 | 500 members |
| `reports/stage_c1/mutation_tests.txt` (43 ln) | 4 mutations CAUGHT; "158 passed"; progress dots shown 72+14 = 86 (one 72-dot line missing from the paste; 72+72+14 = 158 and 144/158 = 91 % is consistent) | progress.md:92-96 | 4 mutations / 158 tests |
| `reports/monitor/health.txt` (22 ln) | Pre-start health render, generated 2026-08-25T00:34:28Z: credentials BLOCKED, timer enabled/active, "last run: never", all counts none | progress.md:134-139 | 0 observations |
| `reports/monitor/verdict.txt` (29 ln) | Pre-start verdict render: 3 widths, "observations: 0", "bounds: none", CONTINUE, bars 4.07 / 10.0, projection 2061/2852 | REGISTRATION.md Section 11/12 | 0 observations |
| `docs/ACCESS.md` (223 ln) | Broker table with 8 numbered web sources and retrieval dates; the cap-rule and routing quotes; regulatory rate table; 15-row cost table; the Task 3 SUPERSEDED block with the 7-row sub-test status table | ADR-003, ADR-007, ADR-022, ADR-026 | 4 brokers, 7 sub-tests |
| `systemd/hfexperiment-bars.{timer,service}` | OnCalendar Mon..Fri 23:30 UTC, Persistent=true, MemoryMax=2G | progress.md:134-137 | — |

### 1.3 Untracked / gitignored data in the LIVE working tree — UNANCHORED

`ls -la` and read-only SQLite (`immutable=1`) only. Read times UTC as noted.
These may have changed after the 2026-08-28 anchor; they are working-tree state, not git objects.

| path | size (B) | mtime | contents observed |
|---|---|---|---|
| `data/bars.db` | 40,960 | 2026-08-24 17:34 | The B.1 shadow store. Tables `assets, bars, fetch_log, formations, sessions, universe` — **every one 0 rows** (read 2026-09-03T23:58:33Z). Corroborates "zero shadow observations". |
| `data/c1_formation.db` | 105,005,056 | 2026-08-24 19:31 | C.1's own store: assets 14,260; bars 894,420; formations 75; sessions 682; universe 500; fetch_log 0 (read 2026-09-03T23:58:42Z). Row counts only; no bulk read. |
| `data/ledger/` | dir | 2026-08-24 17:34 | **Empty.** No `spend.jsonl` exists, corroborating ADR-021's "the real spend ledger … stays untouched". |
| `_CLOSED_DO_NOT_RUN_HERE` | 747 | 2026-09-02 22:38 | A closure marker written 2026-09-02, excluded via `.git/info/exclude`. Post-anchor artifact; not part of the audited SHA. |
| `.env` | 200 | 2026-08-24 17:52 | **NOT READ** (credentials). Its existence contradicts health.txt:3 ("`.env` does not exist"), which was rendered 2026-08-25T00:34Z, before the file was created at 17:52 local on 2026-08-24 → in fact `.env` predates the render; the render is the pre-start artifact and the file arrived later per progress.md:99-100. Note only; no read performed. |
| `Accept:`, `GET`, `Host:`, `User-Agent:` | 0 each | 2026-08-24 17:41 | The four known stray files listed in COMMON_RULES as pre-existing dirt. |
| `~/.config/systemd/user/hfexperiment-bars.{timer,service}` | 426 / 395 | 2026-08-24 17:34 | **Byte-identical** to the tracked units (diff clean). `systemctl --user is-enabled` → `disabled`; `is-active` → `inactive`; absent from `list-timers --all`. The closure's disarm claim verifies. |

### 1.4 External artifacts this repository's figures depend on but does not contain

- `/home/kiros-li/Documents/GitHub/AiTrader/analysis_bars.db` — referenced at `src/hfexperiment/dbaccess.py:13`. It is the **sole** source for the A.1 reproduction (124 dates), the universe checks, the momentum ranking, churn and median share price. Not opened by this task. Any recomputation of claims C8, C11, C12, C17 must cross the AiTrader boundary.
- The "already-spent holdout" width figures — **27.99 bp/day, 66.40 %/yr, IR 1.062 (width 5) and 10.04 bp/day, 31.70 %/yr, IR 0.798 (width 50)**. There is **no artifact anywhere in HFExperiment** holding these. They enter the repository only as literals in `scripts/cost_table_a2.py:31-34` (comment: "recorded in the A.2 stage prompt") and `src/hfexperiment/registered.py:104-105`, and as table rows at `REGISTRATION.md:115,118`. Everything downstream — the hypothesis, the primary-width choice, the power-law fit, the 2061/2852 projection — rests on them.

---

## 2. Numeric claims, ranked (MUST-VERIFY marked)

Ranked by how much rests on the number. Rank 1-7 are marked **MUST-VERIFY**.

### C1 — MUST-VERIFY — the Section 0 closure verdict
> "BLOCKED. The IBKR TWS API refused fractional quantities however phrased on paper account [paper account ID removed], error 10243 on decimal totalQuantity across two book names and two order types, error 10244 on cashQty, while a whole-share control order was accepted, evidence in reports/stage_a1b."
`REGISTRATION.md:299-304`. Also `reports/stage_a1b/a1b_report.md:107-116`, `progress.md:39-46`, `DECISIONS.md:401-429` (ADR-022).
Figures / n: 3 decimal orders (MU market, MU limit, TE market) + 1 cashQty order + 1 whole-share control = **5 orders**, cap 10; 2 symbols; 2 order types; 20 contracts checked at MinSize/SizeIncrement 0.0001.
Producer: `scripts/a1b_capability_test.py` → `reports/stage_a1b/evidence.jsonl` (51 rows).
Why first: this is the deciding number of the whole live track. Phases C and D stop on it.

### C2 — MUST-VERIFY — the registered cost hurdle
> "Success when the lower bound clears the measured cost hurdle of 4.07 bp per day, computed at the primary width under the worst-case fractional regime with the measured width-5 spread."
`REGISTRATION.md:249-251`; also `registered.py:78`, `reports/stage_a2/cost_table.md:36`, `reports/monitor/verdict.txt:8,17,26`.
Figures / n: width 5, churn 2.0 names/mo, notional 180 USD, width-5 measured spread 13.08 bp at median mid 201.91 USD, round trip 213.84 bp, 21 trading days/mo. n = 5 names (WOLF, AXTI, SNDK, BE, LITE), 9 spread cells each.
Producer: `scripts/cost_table_a2.py:96-115` over `costmodel.round_trip` + `daily_cost_hurdle_bp`, reading `reports/stage_a2/book_spreads.json`. Pinned by `tests/test_registered.py:52-69`.
Why: it is the success bar the verdict would have been read against, and the "keeps most of it" clause of the hypothesis.

### C3 — MUST-VERIFY — the holdout effect size and the primary-width choice
> "the effect, measured at 27.99 bp per day on the already-spent holdout, exceeds the 4.07 bp per day that round-trip costs consume at the measured 40 percent monthly churn, so a fee-paying participant keeps most of it"
`REGISTRATION.md:52-56`. And: "Width 5 is the PRIMARY width for the verdict. It carries the highest recorded information ratio, 1.062" `REGISTRATION.md:92-93`; table `REGISTRATION.md:113-118`.
Figures / n: width 5 → TE 66.40 %/yr, excess 27.99 bp/day, IR 1.062; width 50 → 31.70, 10.04, 0.798, both labelled "recorded"; widths 10 and 20 labelled INTERPOLATED. Underlying n is **not stated anywhere in this repository**.
Producer: none in-repo. Literals only (`cost_table_a2.py:31-34`, `registered.py:104-105`). Origin declared as the AiTrader cross-sectional round of 2026-07-26 (`README.md:3-5`, `src/hfexperiment/benchmark.py:5-9`).
Why: the largest single dependency in the repository, and the one with the weakest in-repo anchor.

### C4 — MUST-VERIFY — the DEGRADED closure arithmetic
> "A.1 measured it: 144 USD at the last two formations, up from 36 in March and April. At 144, whole-share sizing on 900 USD cannot fill a 20-name book at all, because 20 names at one share each already cost about 2,880 USD. A 5-name book gets one share per name, 720 of 900 deployed, with equal weighting destroyed by per-name prices from 22 to 1,595 USD."
`REGISTRATION.md:149-154`; ADR-012 at `DECISIONS.md:194-199`.
Figures / n: median width-20 book share price 143.80 (2026-06-01) and 143.89 (2026-07-01); March 36.47, April 40.59; 20 × 144 = 2,880; 5 × 144 = 720.
Producer: `reports/stage_a1/formations.json` `median_price` block; per-name closes in the same file. Independently reproduced by me from the stored `last_close` values (medians match to 2 dp).
Flags to check: the 2,880 and 720 figures are median × count, not the actual one-share cost. Summed one-share cost of the 2026-07-01 width-20 book from stored closes is **7,890.47 USD**, and of the width-5 book **3,554.82 USD** — so "720 of 900 deployed" is not obtainable from the book it names, and is in tension with the same sentence's "prices from 22 to 1,595 USD" (a single 1,595 share exceeds 900). Also "36 in March and April" against a stored April value of 40.59. Direction of the conclusion is unaffected (it is a fortiori), but the stated arithmetic is what closes a registered branch.

### C5 — MUST-VERIFY — the kill-floor sigma and touch probability
> "The floor is 500 USD of total account equity, a 400 USD loss on 900 deployed after the 100 buffer, 1.31 sigma of the width-20 tracking error, driftless touch probability near 19 percent in year one. Against the table: 600 touches near 30 percent … 400 buys only 7 more points of touch probability"
`REGISTRATION.md:216-222`; ADR-011 at `DECISIONS.md:171-179`; `registered.py:53-56`.
Figures / n: TE(20) = 42.54 %/yr interpolated; deployed 900; sigma = 382.86 USD.
Producer: no script; hand arithmetic in the document. I reproduce 500 → 1.306 σ → 19.2 % touch, 600 → 1.045 σ → 29.6 %, 400 → 1.567 σ → 11.7 %, and 19 − 12 = 7 points — all consistent **only if the loss is 1000 − floor**, i.e. **500 USD, not the 400 USD the sentence states**. The "400 USD loss" phrase and the "1.31 sigma" figure cannot both be right.

### C6 — MUST-VERIFY — Gateway server version, prose vs ledger
> "Gateway 127.0.0.1:4002, **server version 187**, account [paper account ID removed]"
`reports/stage_a1b/a1b_report.md:3-4`; repeated at `DECISIONS.md:408` (ADR-022), `DECISIONS.md:441` (ADR-026), `docs/ACCESS.md:178`, `progress.md:236`, `reports/stage_c1/refusals.md:332`.
Contradicting artifact: `reports/stage_a1b/evidence.jsonl` row 2, `{"kind":"connected", …, "server_version": 178, …}`.
n: one connection record. The C.1 probe (a separate, later connection) does record 187.
Why: A.1b's evidence ledger is the sole primary record of the closure session; a transposed digit in every prose retelling of it is a provenance question about which artifact was actually read.

### C7 — MUST-VERIFY — the measured spread distribution that replaces the inherited band
> "All 20 names of the 2026-07-01 width-20 book were measured on the consolidated tape over sessions 2026-08-19 to 2026-08-21: median 12.77 bp, p75 17.2, p90 20.7, max 27.4. The inherited 15.8 to 50 bp band predicted the wide end and measured wrong in the favourable direction"
`REGISTRATION.md:170-176`; `reports/stage_a2/cost_table.md:3`; ADR-013 at `DECISIONS.md:207-215`.
Figures / n: 20 names × 9 cells = 180 cells; discarded crossed 6, locked 88; median 12.7732, p75 17.2325, p90 20.7306, max 27.4324, min 2.1413, p25 6.3674.
Producer: `scripts/measure_book_spreads.py` → `reports/stage_a2/book_spreads.json`.
Why: it feeds C2 and it is the one measurement that moved a settled assumption.

### C8 — the A.1 reproduction
> "All 124 recorded formation dates identical. Universe exact at all 10 checked dates, all 500 rows each."
`progress.md:207-208`; `REGISTRATION.md:78-80`; `reports/stage_a1/reproduce_log.txt:1,21`; `reports/stage_a1/universe_check.json`.
n: 124 formation dates; 10 universe dates × 500 rows; 19,744 symbols segmented; per-formation ranked 493-496 with `no_far_anchor_bar` exclusions 4-7.
Producer: `scripts/reproduce_formation.py` against AiTrader `analysis_bars.db`. Cross-repo.

### C9 — the frozen confidence-sequence construction and its projection
> "tuning parameter rho set by minimizing the boundary at a crossing time of 1,600 trading days, frozen at 0.071641 … with the sample mean holding at 27.99, the lower bound clears zero at day 2,061 and clears the hurdle at day 2,852."
`REGISTRATION.md:246-262`; `reports/stage_a2/cost_table.md:40`; `registered.py:91,104-107`; `reports/monitor/verdict.txt:4,10-11`.
n: 0 observations (projection only). Producer: `verdict.tuned_rho` / `verdict.first_crossing_day`. I reproduce ρ = 0.071641, day 2061 and day 2852 exactly from the stated formula.

### C10 — the annual deterministic drag
> "Annual deterministic drag at the traded width and measured churn: 28.76 USD per year under whole-share Tiered, 56.84 under fractional."
`REGISTRATION.md:184-186`; `reports/stage_a2/cost_table.md:27-32`; echoed as "roughly 30 to 60 USD a year" at `REGISTRATION.md:279-280`.
n: width 20, churn 5.2/mo, 10.4 fills/mo, share price 103.25. Producer: `costmodel.annual_commission_drag`. I reproduce 28.08 + 0.68 = 28.76 and 56.16 + 0.68 = 56.84.

### C11 — measured churn and the fill-rate justification for the traded width
> "Width 20 is the TRADED width, chosen for fill rate: 10.4 fills per month against 4.0 at width 5, which reaches the roughly 200 fills the execution measurement needs in about 19 months instead of 50."
`REGISTRATION.md:101-104`; ADR-004 `DECISIONS.md:79-81`; ADR-010 `DECISIONS.md:165-166`; `registered.py:85`.
n: 6 formations (2026-02-02 … 2026-07-01). Producer: `reports/stage_a1/formations.json` `churn` block. I reproduce width-20 mean 31/6 = 5.167 → 5.2 and width-5 mean 12/6 = 2.0.

### C12 — the power-law width interpolation and the 1.41 signal-clock cost
> "Fitting a power law to the two recorded widths gives TE exponent -0.321 and excess exponent -0.445 … Width 20 carries IR 0.894 against width 5's 1.062, and time to verdict scales as one over IR squared, giving 1.41."
`DECISIONS.md:141-149` (ADR-009); table at `REGISTRATION.md:110-118`.
n: **two points**, explicitly disclosed. I reproduce every cell: exponents −0.3211/−0.4453; TE(10) 53.15, TE(20) 42.54; excess(10) 20.56, excess(20) 15.10; IR 0.975/0.894; ratio 1.4112. Note the IR figures require the annualisation 252 × bp/day, which the documents never state.

### C13 — the price reconciliation
> "The ratio of medians is 0.7176, a 28.2 percent gap … No name in the book split in 2026. No name went ex-dividend between 2026-07-24 and 2026-08-24."
`reports/stage_b1/price_reconciliation.md:11-13,27-34`; ADR-016 `DECISIONS.md:259-265`; `progress.md:111-119`.
n: 20 names, one public source (stockanalysis.com, retrieved 2026-08-24). Figures: 143.89 vs 103.25; MXL 0.518, WOLF 0.546; third median 97.45 on 19 names + MU at its 2026-08-21 mid.

### C14 — the spend cap and its 1.75× justification
> "Cumulative spend at or above the registered cap of 100 USD per rolling 365 days, about 1.75 times the worst-case fractional projection."
`REGISTRATION.md:196-198`; ADR-013 `DECISIONS.md:217-219`; `registered.py:59`. 100/56.84 = 1.759.
Demonstrated at `reports/stage_c1/refusals.md:131-151`: rolling-year spend 100.01 from records 60.00 + 40.01, with a 25.00 record at 2025-08-10 correctly excluded.

### C15 — the commission schedule and crossovers
> "Confirmed: Tiered cap 0.5 pct, min 0.35. Fixed cap 1 pct, min 1.00. Derived crossovers confirmed: cap equals minimum at 70 USD Tiered and 100 USD Fixed."
`docs/ACCESS.md:65-67`; quoted IBKR text at `:54-58,63`; `commission.py:43-54,116-121`. n: 2 published schedules, retrieved 2026-08-23, sources cited with URLs.

### C16 — regulatory rates
> "SEC Section 31 at 20.60 per million effective 2026-04-04. FINRA TAF at 0.000195 effective 2026-01-01. The assumed one cent TAF floor is confirmed nowhere and is held as a worst-case bound."
`progress.md:202-205`; `docs/ACCESS.md:91-106`; `commission.py:18-27`. Disclosed unmeasured: the TAF floor; gap stated as "0 to 2.2 bp at 45 USD" (`ACCESS.md:102`).

### C17 — median book share price series
> "Median book share price at width 20 ranged 36 to 144 USD over the last 6 months."
`progress.md:209-211`; `reports/stage_a1/formations.md:20-28`. n = 7 formations. I reproduce every cell of the median-price table from the stored `last_close` values.

### C18 — the eligibility layer contradicts the API channel
> "The eligibility layer advertises 0.0001 increments on all 20 book names, so the instruments are fractionable and the refusal is the API channel itself"
`DECISIONS.md:423-425`; table at `reports/stage_a1b/a1b_report.md:14-35`; 20 `contract_details` rows in `evidence.jsonl`. n = 20 names.

### C19 — the ADR-005 partial-refresh horizon
> "The database carries daily bars past the recorded round's pull end of 2026-07-24 for exactly 1,535 symbols, a partial refresh."
`DECISIONS.md:88-90`. n = 1,535 symbols. **No artifact in this repository records this count**; it is verifiable only against AiTrader's database.

### C20 — the C.1 demonstration counts
> "{'intent': 20, 'refusal': 34, 'would_submit': 1} in demo_ledger.jsonl, plus 3 spend records"
`reports/stage_c1/refusals.md:339`. Artifacts present: `demo_ledger.jsonl` 55 lines (20+34+1 = 55 ✔ by line count), `demo_spend_ledger.jsonl` 3 lines.

### C21 — the test and mutation counts
> "158 tests green under mypy strict and ruff … All four required mutations applied to real source, each caught"
`progress.md:92-96`; also 123 (`:141`), 76 (`:179`), 27 (`:218`). HEAD carries exactly **158** `def test_` functions. Mutation evidence files carry per-stage pytest excerpts; the C.1 excerpt shows only 86 of the 158 progress dots (one wrapped line dropped from the paste).

### C22 — the registered prior
> "this session drafts the operator's probability that the sleeve ever clears its verdict at 0.15, and the operator confirms or replaces that number at acceptance"
`REGISTRATION.md:276-278`; confirmed at `:289`; ADR-014 `DECISIONS.md:230-240`. n/a — a stated prior, not a measurement.

### C23 — the closure state
> "The live track was never funded and zero capital was deployed. The shadow series was disarmed before its first accrual … The verdict was never computed."
`REGISTRATION.md:308-313`; `progress.md:5-21`. Corroborated by live untracked state: `data/bars.db` all tables 0 rows; `data/ledger/` empty; `systemctl --user is-enabled` = disabled, `is-active` = inactive, absent from `list-timers`.

### C24 — the account pin demonstration id
> `docs/ACCESS.md:213` says the refusal "is demonstrated against **DU999999**"; `reports/stage_c1/refusals.md:197` and `scripts/demo_c1.py:310` and `tests/test_gatewire.py:117` all use **DU9999999**. One digit apart; hygiene only.

---

## 3. Intervals and tests

**There is no realized confidence interval, no test statistic and no p-value anywhere in this
repository.** The shadow series produced zero observations, so the confidence sequence was
never evaluated on data. What exists is the *construction*, its *levels*, and *planning
projections*. Listed exhaustively:

| # | item | file:line | stated estimator / test | n | data structure |
|---|---|---|---|---|---|
| I1 | Studentized asymptotic confidence sequence, one-sided, on daily shadow excess return | `REGISTRATION.md:246-248`; formula at `src/hfexperiment/verdict.py:10-12,26-34` | ACS radius `σ_t·sqrt(2(tρ²+1)/(t²ρ²)·ln(sqrt(tρ²+1)/α))`, σ_t the running sample SD | **0** | would be a daily series of book-minus-benchmark excess returns; ledger `data/bars.db` is empty |
| I2 | Primary level α = 0.05 one-sided at width 5 | `REGISTRATION.md:97-99`; `registered.py:67`; `verdict.alpha_for_width:104-116` | Bonferroni family: 0.05 primary, 0.025 each secondary, "family never outspends the primary" | 0 | 3 widths (5, 20, 50) |
| I3 | Secondary levels α = 0.025 at widths 20 and 50 | `REGISTRATION.md:97-99`; `reports/monitor/verdict.txt:13,22` | as above | 0 | — |
| I4 | Tuning parameter ρ frozen at 0.071641, minimizing the radius at t\*=1600 | `REGISTRATION.md:248`; `registered.py:91`; `verdict.tuned_rho:37-66` | golden-section search on log10 ρ, 200 iterations | n/a (deterministic) | — |
| I5 | Success rule: lower bound > 4.07 bp/day | `REGISTRATION.md:249-251`; `verdict.classify_verdict:97-98` | one-sided lower bound of I1 vs a fixed hurdle | 0 | — |
| I6 | Futility rule: upper bound < 10 bp/day | `REGISTRATION.md:251-252`; `registered.py:70` | one-sided upper bound of I1 | 0 | — |
| I7 | Rendered bounds, all three widths | `reports/monitor/verdict.txt:5-6,14-15,23-24` | literally `observations: 0` / `bounds: none, the series has not started`, verdict CONTINUE | 0 | — |
| I8 | Planning projection: lower bound clears zero at day 2061, clears 4.07 at day 2852 | `REGISTRATION.md:260-262`; `reports/stage_a2/cost_table.md:40`; `registered.py:106-107` | `verdict.first_crossing_day`, assuming the sample mean holds at 27.99 with σ 418 forever — explicitly labelled "planning arithmetic only" at `verdict.py:126-128` | 0 (counterfactual) | — |
| I9 | Pointwise sanity: "pointwise arithmetic needs about 600 days" | `REGISTRATION.md:255-258` | pointwise normal arithmetic at 27.99 vs 418 bp | 0 | — |
| I10 | Driftless first-passage touch probabilities: ~19 % at 500, ~30 % at 600, ~12 % at 400 | `REGISTRATION.md:218-222`; `DECISIONS.md:174-178` | reflection-principle tail `2Φ(−k)` on annual σ = 900 × 42.54 % | 0 | — |
| I11 | Reproduction "tests" | `reports/stage_a1/universe_check.json` (`exact_match`), `reproduce_log.txt:1,21` | **exact set/rank/value equality**, not a statistical test — no tolerance, no statistic | 124 dates / 10 × 500 rows | recorded vs reproduced membership tables |
| I12 | Formation-hash reproduction check | `reports/stage_c1/refusals.md:9` | exact hash equality `0b28a5cfda7516fa` == `0b28a5cfda7516fa` | 1 formation | — |
| I13 | Spread distribution quantiles | `reports/stage_a2/book_spreads.json:139-147` | order statistics (min, p25, median, p75, p90, max), no interval | 20 names × 9 cells | per-name median bp |
| I14 | Mutation "tests" | `reports/stage_a1/…`, `stage_a2/…`, `stage_b1/…`, `stage_c1/mutation_tests.txt` | 3 + 2 + 3 + 4 = 12 source mutations, each recorded CAUGHT by named failing pytest cases | 12 mutations | pytest output |

Nothing above is a hypothesis test on data. The two-point power-law fit (C12) has zero
residual degrees of freedom by construction and reports no uncertainty, which the
documents disclose by labelling widths 10 and 20 "INTERPOLATED from two-point fit"
(`REGISTRATION.md:116-117`) and by ADR-009's "recorded measurements at more widths would
replace the two-point fit" (`DECISIONS.md:157-158`).

---

## 4. Provenance claims

| # | claim (verbatim, abridged where marked) | file:line | commit named | what would have to be true |
|---|---|---|---|---|
| P1 | "Registered 2026-08-23, before any broker measurement was taken. The three outcomes below are fixed now so the broker answer cannot be read against a bar its own measurement could see." | `REGISTRATION.md:8-11` | — (see P2) | Section 0's text must exist in a commit that precedes any artifact of the broker measurement. |
| P2 | "REGISTRATION.md Section 0 committed at c4e9817 before any broker measurement." | `progress.md:192-193` | **c4e9817** | c4e9817 must contain Section 0 and nothing measured. *Observed in the live repo:* c4e9817 is the **root commit** (no parents), dated 2026-08-23T15:23:16−07:00, touching **only REGISTRATION.md**, +49 lines. The broker measurement (docs/ACCESS.md) first appears in 0a0d214 at 15:42:34 the same day — 19 minutes later. |
| P3 | "Sections beyond Section 0 land in Stage A.2. Amendments append. **Nothing edits in place.**" | `REGISTRATION.md:4` | — | Every later commit to REGISTRATION.md must add lines only. *Observed:* c4e9817 +49/−0, a8f4b0d +235/−0, 8c4c3bc +12/−1, 669eb5c +9/−0, f13e1d3 +11/−0. The single deletion is at 8c4c3bc, replacing the line "Append-only. No entries yet." with "Append-only." when the first amendment landed. |
| P4 | "Sections 1 through 12 registered 2026-08-23. Binding once the operator accepts them." | `REGISTRATION.md:58-59` | — | Sections 1-12 must land in a 2026-08-23 commit. *Observed:* a8f4b0d, 2026-08-23T21:40:25−07:00, +235 lines to REGISTRATION.md. |
| P5 | "Width 5 is the PRIMARY width for the verdict … it is chosen **now, before any forward data exists**, on the already-spent holdout rather than on anything the shadow series will produce." | `REGISTRATION.md:92-95`; restated `DECISIONS.md:162-163` | — | No shadow observation may exist at a8f4b0d, and none may ever have existed. *Corroborating:* `data/bars.db` holds 0 rows in every table (live, read 2026-09-03T23:58:33Z); the series was authorised to start 2026-09-01 and was disarmed 2026-08-26. |
| P6 | "The shadow series starts at the registration date and is never backfilled before it, because backfilling spends a holdout already spent." | `REGISTRATION.md:71-74` | — | `SHADOW_SERIES_START = "2026-09-01"` (`registered.py:97`) must gate every accrual, and no pre-start row may exist. Moot in fact: no row exists at all. |
| P7 | "tuning parameter rho set by minimizing the boundary at a crossing time of 1,600 trading days, **frozen at 0.071641**." | `REGISTRATION.md:248` | — | ρ must be a constant consumed, never re-tuned, and must reproduce from the stated procedure. `registered.py:87-91` states "The engine consumes this constant, never re-tunes"; `tests/test_verdictengine.py:24-26` pins both. |
| P8 | "Amendments are dated, numbered, appended, and each records what data existed when it was made. **No amendment may respond to an observed shadow outcome.**" | `REGISTRATION.md:271-274` | — | Each amendment-log entry must state the data extant. All three do (`:290-295`, `:299-304`, `:313-315`). |
| P9 | "Data existing at this entry: the A.1 reproduction against the recorded round through the 2026-07-24 pull, the A.2 spread measurement over sessions 2026-08-19 to 2026-08-21, and **zero shadow observations, because the series has not started**." | `REGISTRATION.md:290-295`; ADR-014 `DECISIONS.md:234-238` | — | Acceptance (8c4c3bc, 2026-08-24) must precede any shadow row. Corroborated as in P5. |
| P10 | "Data existing at this entry: everything recorded above, and **zero shadow observations, because the series never started**." | `REGISTRATION.md:313-315` | — | As P5. Also that the timer was disarmed: *observed live*, `is-enabled` = disabled, `is-active` = inactive, unit absent from `list-timers --all`, unit files still present and byte-identical to the tracked copies. |
| P11 | "Universe rule U-LIQ-500-stk-w60-m40-p5, **copied verbatim** from the recorded round"; and "COPIED 2026-08-23 from AiTrader backtest/universe.py, read-only source. … Do not edit the logic." | `REGISTRATION.md:78-79`; `src/hfexperiment/universe.py:1-6` | — | `universe.py` must be textually the AiTrader module. Verifiable only across the AiTrader boundary. |
| P12 | "The recorded round's formation code is outside the two permitted read paths, so the 12-1 ranking is implemented from its registered description." | `DECISIONS.md:99-101` (ADR-006) | — | The formation ranking is a **re-implementation**, not a copy — so C8's "identical" applies to universe membership and formation *dates*, and ADR-006 says so explicitly at `:106-110`: the recorded books at widths 5 and 50 "are not stored in the permitted database, so the disagreement gate ran against the recorded universe membership instead". |
| P13 | "Database hash unchanged: c30d3f4486e975a0 before and after." | `progress.md:211-212`; `reports/stage_a1/db_hash_{before,after}.txt` | — | The two recorded sha256 values must be equal (they are, byte-identical files) and must be of AiTrader's `analysis_bars.db`. A re-hash today will differ because AiTrader keeps collecting; the claim is about the A.1 window only. |
| P14 | "Numbered ADRs, **append-only**." | `DECISIONS.md:3` | — | Every commit to DECISIONS.md must be additions only. *Observed:* 91a1dcb +114/−0, 23d9ffa +104/−0, 8c4c3bc +86/−0, b4a7a23 +85/−0, 669eb5c +30/−0, 82e77a0 +60/−0. Zero deletions across the whole history. Note the numbering jumps **ADR-022 → ADR-026** (`DECISIONS.md:401`, `:432`); ADR-023/024/025 do not exist. |
| P15 | "Both were written during A.1 and were true then … Neither document was amended, so the repository advertised a blocker that no longer existed and an UNDECIDED verdict that A.1b had already resolved to BLOCKED." | `DECISIONS.md:432-443` (ADR-026); `progress.md:226-253` | 82e77a0 | The stale text must have survived from 0a0d214/91a1dcb (2026-08-23) through 669eb5c (2026-08-24, A.1b) to 82e77a0 (2026-08-28). *Observed:* docs/ACCESS.md and ADR-003 were untouched between those commits — the correction is self-reported and the git history supports the three-day gap. |
| P16 | "ADR-003 keeps its original text with a superseded note beneath it. **Nothing is rewritten to look as though it was always right.**" | `DECISIONS.md:452-454`; the note itself at `:47-55`; the struck sentence at `docs/ACCESS.md:184-189` | 82e77a0 | 82e77a0 must add, not replace. *Observed:* +60/−0 on DECISIONS.md. docs/ACCESS.md in the same commit does modify the Task 3 section, but by re-heading and striking through (`~~…~~`) rather than deleting. |
| P17 | "The operator accepted Sections 1 through 12 by delegation on 2026-08-24 … **The act of running the B.1 stage prompt was the acceptance**" | `DECISIONS.md:230-235` (ADR-014) | — | Acceptance rests on an act, not a signature. The only record is the amendment-log entry the same session wrote (`REGISTRATION.md:286-295`) plus commit 8c4c3bc. There is no operator-authored artifact. |
| P18 | "The operator holds a funded live IBKR account and a paper account, [paper account ID removed], reachable through a running Gateway on port 4002 (**operator statement, 2026-08-28**, consistent with the A.1b session log)." | `docs/ACCESS.md:187-189` | — | An operator statement, disclosed as such, corroborated by the A.1b connection record (`evidence.jsonl` `connected`, managed accounts `["[paper account ID removed]"]`). |
| P19 | "Registered numeric thresholds live in src/hfexperiment/registered.py and the structural guard test fails if any lacks an enforcement site." | `REGISTRATION.md:59-61`; `registered.py:3-6` | — | `tests/test_structural_guard.py` (2 tests) must actually enumerate the fields of `RegisteredThresholds` and `StageAConfig` and require a consumption site outside the defining module. |
| P20 | "Demo constants: notional 45.00 and broker minimum 1.00, **labelled DEMO everywhere, resolving nothing registered**." | `DECISIONS.md:392-394` (ADR-021); demonstrated at `reports/stage_c1/refusals.md:5` | — | `PER_NAME_NOTIONAL_USD` must remain a `DeferredParameter` at HEAD (it is, `registered.py:110-115`), and every DEMO use must be labelled. |
| P21 | "Append-only. One dated entry per stage, **newest at top**." | `progress.md:3` | — | Entries must descend by date. *Observed:* they do from `:5` (2026-08-26) down to `:187` (2026-08-23 A.1) — but the ADR-026 entry dated **2026-08-28T22:10Z** sits at the **bottom**, `progress.md:226`, below the 2026-08-23 A.1 entry. Ordering-discipline hygiene only. |
| P22 | The timer unit's own comment: "Installed to ~/.config/systemd/user/ by scripts/install_timer.sh." | `systemd/hfexperiment-bars.timer:4` | — | `scripts/install_timer.sh` must exist. **It does not** — `scripts/` holds eight `.py` files and nothing else at the anchored SHA. The installed units are nonetheless byte-identical to the tracked ones. |

---

## Live-repo access log

Purpose of access, per COMMON_RULES: (1) git history/provenance; (2) untracked working-tree data.
No file under `/home/kiros-li/Documents/GitHub/HFExperiment/` was opened for writing. `.env` was
not read. No repository script was executed. SQLite reads used `file:…?immutable=1`, which
cannot create `-wal`/`-shm` sidecars; `ls -la data/` after the reads shows the same two files with
unchanged sizes and mtimes.

**`git -C /home/kiros-li/Documents/GitHub/HFExperiment status --porcelain` — BEFORE first access, 2026-09-03T23:57:15Z:**

```
?? Accept:
?? GET
?? Host:
?? User-Agent:
```

**`git -C /home/kiros-li/Documents/GitHub/HFExperiment status --porcelain` — AFTER last access, 2026-09-04T00:01:25Z:**

```
?? Accept:
?? GET
?? Host:
?? User-Agent:
```

Identical, and exactly the four stray files COMMON_RULES records as pre-existing owner dirt.
Nothing else appeared. No accidental modification occurred.

Commands run against the live tree, all read-only:

| time (UTC) | command | purpose |
|---|---|---|
| 23:57:15 | `git status --porcelain` | pre-access baseline |
| 23:57:2x | `git rev-parse HEAD`, `git branch -a`, `git log --format=… --date=iso-strict`, `git tag -l` | history (13 commits, root c4e9817, HEAD 82e77a0, no tags) |
| 23:57:4x | `git show --stat c4e9817`, `git rev-list --parents -n1 c4e9817`, `git ls-tree -r --name-only c4e9817` | P2 |
| 23:58:0x | `git log --follow`, `git diff --numstat c4e9817 HEAD -- REGISTRATION.md`, `git show 8c4c3bc -- REGISTRATION.md`, `git log --numstat -- DECISIONS.md` | P3, P4, P14, P16 |
| 23:58:1x | `ls -la .`, `git status --ignored --porcelain`, `cat .git/info/exclude`, `git config --get core.excludesFile` | §1.3 inventory |
| 23:58:2x | `cat _CLOSED_DO_NOT_RUN_HERE`, `ls -laR data/` | §1.3 (747-byte text marker; sizes and mtimes) |
| 23:58:33 | sqlite `file:data/bars.db?immutable=1` — table list + `count(*)` per table | C23, P5 |
| 23:58:42 | sqlite `file:data/c1_formation.db?immutable=1` — table list + `count(*)` per table | §1.3 |
| 23:59:xx | `systemctl --user is-enabled/is-active hfexperiment-bars.timer`, `systemctl --user list-timers --all`, `ls -la ~/.config/systemd/user/`, `diff` against the tracked units | C23, P10 (outside the repo; system state, read-only) |
| 00:01:25 | `git status --porcelain` | post-access baseline |

Computation was performed only under
`/tmp/claude-1000/-home-kiros-li-Documents-GitHub-program-audit/2c6a58bc-6f69-48c9-a930-b20684f1e1e4/scratchpad/work/agentC/spotcheck.py`,
reading from SNAP.
