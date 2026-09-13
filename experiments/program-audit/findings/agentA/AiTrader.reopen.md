# REOPEN LEDGER — AiTrader (Agent A, consolidated)

Repository: AiTrader, anchored SHA `705e0ed128b7e184be6c1a23dcd06750c524c525` (main, 2026-08-24).
Merged and de-duplicated from three part-ledgers covering `EXPERIMENT.md` / `AUDIT*.md` /
`DATA_AUDIT.md` / `LIVE_READINESS.md` / `WEEKLOG.md` (p1), `RETURN.md` (p2), and `PROGRESS.md` /
`CONTEXT.md` / `news_experiment/` / `research_satellite/` / `COLLECTION_LOG.md` (p3).

**This ledger is factual, not advocacy.** "Status" is the state at the anchored SHA. "Deciding
figure" is the number the closure rests on, with its n. A blank cell means the document records
nothing of that kind. All paths are `AiTrader/<path>:<line>`. Where a row is challenged by a
finding, the finding ID is named.

**Repository-wide fact bearing on every "later entry" column.** The last substantive session commit
is `f819b68`, 2026-07-29 20:18 PDT. The four commits from there to the anchor (`8a49239` 2026-08-04,
`f1fb308` 2026-08-06, `b5c2236` 2026-08-18, `705e0ed` 2026-08-24) change only `COLLECTION_LOG.md`
and two `.gitignore` lines; `PROGRESS.md` has no session entry dated 2026-08. **So no reopen
condition in this repository has been evaluated since 2026-07-29**, while 18 collection days accrued
(10,113 symbol-day rows, 2,320 model calls, $1.2809) — COLLECTION_LOG.md:117-277.

---

## A. News-drift experiment — stages

| entry | status | closure kind | closure date | deciding figure (n) | file:line |
|---|---|---|---|---|---|
| Primary hypothesis: an LLM's three-way headline judgment predicts next-session excess return, ADV 2.07M–65.3M | **OPEN — collecting** | none yet | — | none; no headline has been scored against a price | EXPERIMENT.md:704-710; status header EXPERIMENT.md:3-4 |
| Stage 0, the specification | **SHIPPED / ACCEPTED and BINDING** | accepted before any collection | 2026-07-28 | capacity gate: required net edge 4.96 bp/round trip at the 2,000 USD sizer, 2,520 trades/yr, vs a 2,500 USD/yr floor | EXPERIMENT.md:3-15; RETURN.md:433, :113; PROGRESS.md:540 |
| Stage 1, feasibility | **CLOSED, partial** | cleared on every stop condition it was designed to test | 2026-07-28 | per-task rows below | EXPERIMENT.md:2696-2732; RETURN.md:560-572 |
| Stage 2, collector build | **SHIPPED** | every state demonstrated by producing it | 2026-07-28 | 33 directional demo rows (n=33); 49 rows across all states | EXPERIMENT.md:2889-2898; PROGRESS.md:335 |
| Stage 3, collection | **RUNNING at the anchor** | not closed | started 2026-07-29T22:54:53Z | 18–19 collected sessions, 10,113 rows, 2,320 calls, $1.2809; first run 427 rows over a 1,558-member band | COLLECTION_LOG.md:2-3, :33, :117, :270-277 |
| Stage 4, holdout | **NOT STARTED** | evaluated ONCE, by design | — | — | RETURN.md:22; CONTEXT.md:46 |

Stage-3 stop rule: 1,000 scored observations across ≥ 60 day clusters, 120-session hard stop
(RETURN.md:1279; PROGRESS.md:551). Collection is unrecoverable per session: a missed session cannot
be filled without querying historical news (RETURN.md:70).

## A1. Stage 1 task verdicts

| task | verdict | deciding figure (n) | file:line |
|---|---|---|---|
| 1 coverage | PASS, stop condition not met | 98.0 / 80.0 / 72.0 / 64.0 % any-news by stratum, n = 50 each, 1,538 headlines; residual "18 of 50 S4 symbols silent, effective sample ~2/3 nominal" | EXPERIMENT.md:2318-2330; PROGRESS.md:391 |
| 2 arrival rate | PASS, 6.5x margin claimed | 0.359 headlines/symbol-day vs 0.10 assumed, n = 200 symbols | EXPERIMENT.md:2341-2354; PROGRESS.md:393. **Margin challenged: AUDIT-A-AiTrader-11** |
| 3 ETB / short side | PASS, worry mostly cleared | 83.3 / 93.3 / 80.0 / 62.1 %, n = 30/30/30/29; `shortable` and `easy_to_borrow` agreed on every symbol | EXPERIMENT.md:2364-2375; RETURN.md:580 |
| 4 latency | PASS, 20-min delay not reduced | news API median 0.17 s / p95 0.49 s; scoring median 1.04 s / p95 1.91 s; p95 ~2.4 s total | EXPERIMENT.md:2384-2396; PROGRESS.md:397 |
| 5 tick multiple, attempt 1 | UNMEASURED (after hours) | S1 870.5 vs S4 303.5 ticks, n = 10 each — ordering backwards | EXPERIMENT.md:2409-2420 |
| 5 attempt 2 | BLOCKED (market closed) | no data | EXPERIMENT.md:2459-2470 |
| 5 attempt 3 | MEASURED AND UNUSABLE | ladder 39.0 / 72.0 / 104.5 / 62.5, n = 402 rows; 42.1 % of the sample were funds | EXPERIMENT.md:2501-2549 |
| 5 attempt 4 | **MEASURED AND USABLE** | ladder 7.0 / 8.0 / 6.5 / 12.0 ticks, n = 1,402 rows / 157 symbols / 3 sessions; strict monotonicity FAILS, judged near-monotone | EXPERIMENT.md:2588-2619; RETURN.md:249; PROGRESS.md:266-272 |
| 6 model comparison | **INCONCLUSIVE, never redone** | haiku 21/21 parsed; opus 0 of 21 reached (request bug); gemini n = 2 then latched; DeepSeek n = 0, no credential | EXPERIMENT.md:2422-2458, :2734-2742; RETURN.md:596-604; PROGRESS.md:400. **AUDIT-A-AiTrader-14** |

## A2. Experiment blockers

| blocker | file:line | state at anchor |
|---|---|---|
| Tick multiple "unmeasurable without paid quote data" (AMENDMENT 2) | EXPERIMENT.md:2400-2401, :2841-2843; RETURN.md:1637, :308, :418 | **LIFTED** 2026-07-28 (`e60232a`, no RETURN.md entry — AUDIT-A-AiTrader-17), measured 2026-07-29 via the historical SIP endpoint — EXPERIMENT.md:2565-2579; RETURN.md:249 |
| RTH scheduling for the tick measurement | EXPERIMENT.md:2459-2478 | **LIFTED** — historical query bounds time by construction, EXPERIMENT.md:2572-2577 |
| IEX-only feed, not the consolidated tape | EXPERIMENT.md:2521-2529 | **LIFTED** — SIP historical; venue-diversity check passes 97.9 % — EXPERIMENT.md:2621-2625 |
| Exchange calendar stale at 2026-07-24 | RETURN.md:365, :437 | **LIFTED** 2026-07-28, populated to 2027-07-28 (+253 sessions) — RETURN.md:274 |
| Operator's separate Anthropic experiment key not created | RETURN.md:435 | **LIFTED** 2026-07-28 — RETURN.md:357; `credential_shared: false`, `latch_separate: true` at COLLECTION_LOG.md:76-77 |
| Model comparison unresolved; DeepSeek has no credential; Opus arm lost to a `temperature` request bug; Gemini exhausted after 2 calls | EXPERIMENT.md:2428-2446, :2721-2724, :2730-2732 | **NOT LIFTED. Both reachable causes have expired** (Opus quirk is now a hard rule, EXPERIMENT.md:2138-2140, RETURN.md:539; separate funded credential, COLLECTION_LOG.md:26-27) and no redo is recorded. **AUDIT-A-AiTrader-14** |
| Stage 3 blocked pending an operator amendment decision after the cost measurement | EXPERIMENT.md:2688-2694 | **LIFTED** by AMENDMENT 5 — EXPERIMENT.md:247-259; PROGRESS.md:258 |
| Borrow cost on the short side unmodelled (the fee model has no borrow term) | EXPERIMENT.md:2222-2224, :2836-2837; RETURN.md:677; PROGRESS.md:555 | **OPEN** — cross-repo lead 4 |
| `--i-have-read-the-preconditions` is an attestation, not a verifier; three of five named checks are not start-time checks | EXPERIMENT.md:660-682; RETURN.md:121 | **OPEN, reported not fixed** |
| Anthropic credential shared with the council (AMENDMENT 3, OQ 9) | EXPERIMENT.md:2240-2250 | **LIFTED in practice** — separate experiment key + latch, COLLECTION_LOG.md:26-27 |
| Market capitalisation not computable: "`analysis_bars.db` holds no shares outstanding and no market capitalisation" | EXPERIMENT.md:858-863, :2861-2863; RETURN.md:655, :688 | **OPEN** — cross-repo lead 3 |
| Historical ETB / shortability at a past formation not recoverable from this endpoint | EXPERIMENT.md:2377-2380; RETURN.md:580 | **OPEN** — cross-repo lead 5 |
| Stale start blockers still stated in `CONTEXT.md:54`, `:60` and printed by `news_experiment/collect.py:7-9`, `:731-735` | CONTEXT.md:54, :60 | **STALE** — measured and unblocked 2026-07-29 while the text stands. **AUDIT-A-AiTrader-12** |

## A3. Experiment amendments and their registered reversal conditions

| amendment / condition | file:line | trigger met at the anchor? |
|---|---|---|
| AMENDMENT 1 (rank → absolute ADV) reverses on "evidence that the effect tracks rank better than ADV ... by scoring the same observations under both memberships" | EXPERIMENT.md:2304-2306; field note EXPERIMENT.md:2078; PROGRESS.md:448; RETURN.md:800 | **NO, and partly unreachable** — 446 of 3,501 rank-band members at the 2026 formation lie outside the ADV band and are never queried (EXPERIMENT.md:957; `reject("outside_adv_band")` at news_experiment/universe.py:189-191; 2,419 such rejections at COLLECTION_LOG.md:30). **AUDIT-A-AiTrader-13** |
| AMENDMENT 2 (5.00 → 10.00 floor) reverses on "evidence that the effect is concentrated in 5 to 10 USD names ... by scoring the excluded 5-to-10 band separately" | EXPERIMENT.md:1091-1095; PROGRESS.md:425; RETURN.md:694 | **NO, and unreachable from this collection** — sub-10.00 symbols are rejected before sampling (news_experiment/universe.py:163-164; `MIN_MEDIAN_CLOSE = 10.00` at news_experiment/spec.py:39; 3,042 rejections at COLLECTION_LOG.md:30). **AUDIT-A-AiTrader-7** |
| AMENDMENT 2 residual: "If a later reading decides the mechanism matters more than the dispersion, the correct response is to lower the floor and accept the worse hurdle" | EXPERIMENT.md:885-890 | **Arguably met** — the price-floor lever is recorded as exhausted after the tick measurement (EXPERIMENT.md:266-267, :2674-2678; PROGRESS.md:272), which is the "later reading" the clause anticipates. Not revisited |
| AMENDMENT 2 alternate: "If shares outstanding become available, the removal analysis should be redone against actual market cap" | EXPERIMENT.md:858-863; RETURN.md:688 | **NO** — cross-repo lead 3 |
| AMENDMENT 3 (Haiku) reverses only if all three hold: a DeepSeek credential exists; a head-to-head shows DeepSeek is not worse; the cost gap becomes decision-relevant | EXPERIMENT.md:2749-2761; RETURN.md:508 | **NO** — none of the three has changed |
| AMENDMENT 4 (fifth state `excluded_pre_call`) | PROGRESS.md:302; EXPERIMENT.md:211-226 | shipped; no reversal registered |
| AMENDMENT 5 (band kept in full) reverses if "the thin strata cannot meet the 30-cluster per-stratum floor", or if the gross signal concentrates entirely in S1/S2 | EXPERIMENT.md:353-356; PROGRESS.md:252; RETURN.md:207 | **NOT YET EVALUABLE** — 18 of 60 day clusters collected, no scoring session has run |
| AMENDMENT 5 residual: maker execution is the named resolution path for a gross-positive net-negative result, forbidden to rely on before fill probability, time-to-fill, adverse selection and venue mechanics are measured | EXPERIMENT.md:377-399, :2263-2270; PROGRESS.md:254; RETURN.md:211 | **NOT TRIGGERED** — no outcome exists. Cross-repo lead 5 |
| AMENDMENT 6 (within-day permutation null): "An uninformative null makes the affected primary an abstention, never a negative" | EXPERIMENT.md:530-545; PROGRESS.md:221-223; RETURN.md:163-165 | shipped; the uninformative-null rule is itself the registered abstention condition |
| AMENDMENT 7 (stale Level 1 figures) | PROGRESS.md:189-197; RETURN.md:113-121 | shipped, figures only; three start-precondition gaps reported rather than added (RETURN.md:121) |
| Primary abstention trigger: permutation null UNINFORMATIVE if pooled minority directional share < 10 % or fewer than 30 mixed day clusters | EXPERIMENT.md:530-540, :2272-2281 | **NOT YET EVALUATED** — demonstration first look was 21 % minority on n = 33 (EXPERIMENT.md:429-435) |
| NEUTRAL rate above 80 % is a reportable failure of the design | EXPERIMENT.md:1615-1618 | **NOT EVALUATED**; the one recorded coverage block shows 106 judged / 67 scored directional, i.e. ~37 % NEUTRAL (COLLECTION_LOG.md:60-74) |
| Story-group re-run trigger: > 10 % of observations sharing a `story_group_id` | EXPERIMENT.md:1658-1663, :470-473 | **NOT EVALUATED** |
| rho and residual volatility "must be recomputed before the stop rule fires"; if realised rho > 0.05 the required n is recomputed and collection continues | EXPERIMENT.md:1806-1810, :2176-2178 | **NOT DONE** — 10,113 rows available since 2026-08. **AUDIT-A-AiTrader-11** |
| Strength scale revisited on DEGENERATE USE (> 80 % on one value, or fewer than three of five values occur) or SATURATED USE | EXPERIMENT.md:2790-2802; RETURN.md:453, :463 | **NOT MET on the one recorded look** — `distinct_values: 3, degenerate: false`, histogram {2:23, 3:28, 4:16} (COLLECTION_LOG.md:66-75); three of five values is exactly the boundary and no later day's histogram is recorded |
| Strength anchors revisited on SKEW (median strength 1 or 5) or TYPE DOMINANCE | EXPERIMENT.md:2804-2815 | **NOT MET** on the one recorded look (median 3) |
| Powered-negative definition: at ≥ 60 clusters, the pooled gross interval's upper bound below 30 bp with no primary clearing 2.50 | EXPERIMENT.md:1818-1823 | **NOT TRIGGERED** — 18 clusters |
| A day whose `source_failed` rate exceeds 20 % is excluded from the cluster count; > 5 % emits a CRITICAL event | EXPERIMENT.md:2054-2059 | **NOT TRIGGERED** — `source_failed: 0`, `source_failed_fraction: 0.0` (COLLECTION_LOG.md:63-65) |
| Fee-model tiers 1, 2, 5, 6 remain "1.0 floors marked UNMEASURED" | RETURN.md:251; PROGRESS.md:270 | **OPEN** — an explicit un-run variant; the same script measures them |
| Claim boundary (OQ 12): a gross positive supports "the pipeline predicts", never "the model understands"; the comparator is "recorded without being added" | EXPERIMENT.md:556-566; RETURN.md:167; AUDIT-2026-07-29.md:208-216 | **OPEN** — cross-repo lead 6 |

## A4. Experiment Open Questions, as the documents record them

| # | subject | status recorded | file:line |
|---|---|---|---|
| 1 | thin-end news coverage | ANSWERED by Stage 1; residual: 18 of 50 S4 symbols silent, effective S4 sample ~2/3 nominal | EXPERIMENT.md:2165-2172, :2332-2337 |
| 2 | arrival rate | ANSWERED — 0.359/symbol-day against an assumed 0.10, n = 200 symbols / 1,538 headlines | EXPERIMENT.md:2174, :2318-2324 |
| 3 | 180 bp residual volatility and rho = 0.05 | **OPEN, recompute registered and not done** | EXPERIMENT.md:2176-2178; RETURN.md:1313. **AUDIT-A-AiTrader-11** |
| 4 | rank drift / cost dispersion | RESOLVED by AMENDMENT 1 + 2 + the 2026-07-29 tick measurement | EXPERIMENT.md:2180-2195 |
| 5 | DeepSeek credential / hard-rule conflict | CLOSED by AMENDMENT 3, by removing the conflict | EXPERIMENT.md:2197-2204 |
| 6 | DeepSeek provider error semantics | LARGELY CLOSED; residual: the `model_failed` vs `source_failed` split "remains a design claim rather than an exercised one" | EXPERIMENT.md:2206-2219 |
| 7 | short-side feasibility | LARGELY ANSWERED — ETB 62.1–93.3 % by stratum, n = 30/30/30/29; **borrow COST still unmodelled** | EXPERIMENT.md:2221-2227, :2364-2380; PROGRESS.md:555 |
| 8 | the benchmark's own cost | ADDRESSED for the primary by AMENDMENT 5 | EXPERIMENT.md:2229-2238; RETURN.md:1318 |
| 9 | shared Anthropic credential | OPEN as written; **superseded in practice** by the separate experiment key | EXPERIMENT.md:2240-2250 vs COLLECTION_LOG.md:26-27 |
| 10 | strength distribution unknown | OPEN, first look taken: 3 of 5 values used, 60.6 % modal against an 80 % degeneracy bar, n = 33 | EXPERIMENT.md:2252-2261; RETURN.md:453 |
| 11 | maker execution named and unmeasured | OPEN — "not designed, not implemented"; three named pre-reliance measurements | EXPERIMENT.md:2263-2270; PROGRESS.md:254 |
| 12 | realised directional balance unknown | OPEN | EXPERIMENT.md:2272-2281 |

---

## B. Price-only and cross-sectional research hypotheses

| entry | status | closure kind | closure date | deciding figure (n) | file:line | blockers | registered reopen conditions |
|---|---|---|---|---|---|---|---|
| Default stack (RSI-2 reversion + dual-MA momentum, `active_quant`) | closed | powered negative, net | 2026-07-25 | pooled net −1.97 bp/trade, 95 % CI [−2.68, −1.27] (n = 19,648 trades over 3.3M 5-min bars, 8 symbols); re-costed pooled −30.28 bp (crypto −48.78, equity −2.73) | RETURN.md:3564; PROGRESS.md:879, :864; CONTEXT.md:113 | live IEX volume not comparable to SIP history (RETURN.md:3576) | "any future pre-registered run on new out-of-sample tape showing a pooled interval excluding zero on the positive side would overturn this. Nothing else would." (RETURN.md:3599); a 15m-native or signal-augmented run (RETURN.md:3601) |
| H-A equity overnight premium | closed | disqualified by its own secondaries, then re-run properly and cannot-be-distinguished | 2026-07-26 | first pass holdout +6.19 bp, z 2.91 → night-clustered z 1.73; QUEUE 002 holdout +5.41 bp/night, 95 % CI [−0.27, +11.08], z 1.87 vs a raised bar of 2.24 (n = 640 nights) | RETURN.md:3341, :3471; PROGRESS.md:869, :859 | holdout already read for this hypothesis by P28, so no untouched period exists (RETURN.md:3323) | none remaining; "Hypothesis generation should resume elsewhere" (RETURN.md:3354). **The registered confirming observable was run and reported** |
| H-B daily time-series momentum, long-short | **closed, with an unmet reopen condition** | cannot be distinguished from no edge | 2026-07-26 | holdout net +22.87 bp/round trip, 95 % CI [−11.17, +56.90], z 1.32 vs bar 2.39 (n = 1,146 holdout trades); re-costed +1.85, z 0.11 | RETURN.md:3472, :3417; PROGRESS.md:869 | "the 2026-chosen universe overweights past uptrends" (RETURN.md:3451) | **"H-B could only be re-examined on a survivorship-free universe, which this database cannot provide." (RETURN.md:3485) — MET INSIDE THIS REPOSITORY 18 h later (`a2f7c94`, RETURN.md:2985); never re-run, yet counted as resolved at RETURN.md:3234 and :2968. AUDIT-A-AiTrader-4** |
| H-C crypto US-session drift | closed | clean negative (sign flipped out of sample) | 2026-07-26 | holdout net −8.21 bp, 95 % CI [−17.34, +0.91], z −1.76 (n = 2,530 holdout trades); re-costed −56.21, z −12.07 | RETURN.md:3473, :3418 | — | "H-C is closed negative" (RETURN.md:3485) |
| H-D majors-to-SOL convergence | closed | falsified (interval spans zero, negative point, capacity below floor, mechanism contradicted) | 2026-07-26 | holdout −12.48 bp/day, 95 % CI [−36.48, +11.51], z −1.02 vs bar 2.24; capacity −1,695 USD/yr (n = 697 holdout days, 57 trades) | RETURN.md:3219, :3230; PROGRESS.md:849 | shorts not executable on Alpaca crypto (RETURN.md:3186); SOL 417-day data hole 2023-07-06..2024-08-26 (RETURN.md:3190) | none registered |
| H-E ETH-BTC rotation spread | closed | falsified | 2026-07-26 | holdout −8.22 bp/day, 95 % CI [−27.04, +10.60], z −0.86; capacity −190 USD/yr; gross +3.2 %/yr against a 30 %/yr claim (n = 936 holdout days) | RETURN.md:3221, :3227, :3231 | — | none registered |
| H-F 12-1 cross-sectional momentum | closed | cannot be distinguished from buy and hold (significance leg only; capacity leg cleared) | 2026-07-26 | holdout excess +27.99 bp/day, 95 % CI [−4.9, +60.9], z 1.668 vs bar 2.50; capacity 17,634 USD/yr (n = 31 holdout months, 2.55 yrs, 5-name book) | RETURN.md:2857, :2921; PROGRESS.md:824-827 | "**THE TRADEABLE-SIZE TEST IS UNDERPOWERED BY CONSTRUCTION**" at the Level 1 5-position width (RETURN.md:2779); realised holdout TE 66.4 %/yr needs 104 %/yr excess (RETURN.md:2899) | "The position limit, not the fee model and not the data, is what blocks this family" (RETURN.md:2966); "Any future round uses the corrected universe from a fresh pre-registration" (RETURN.md:2729). **The position-limit blocker expired 2026-07-27 (5 → 10, RETURN.md:1137); recomputed implied z at n=10 is 1.44–1.53, i.e. no higher, so the verdict SURVIVES** |
| H-G 1-month short-term reversal | closed | fails (interval spans zero, capacity below floor) | 2026-07-26 | holdout excess +3.25 bp/day, 95 % CI [−16.2, +22.7], z 0.328; capacity 2,044 USD/yr vs a 2,500 floor (n = 31 holdout months) | RETURN.md:2859, :2922; PROGRESS.md:827 | 1 of 124 books contaminated by RSX (RETURN.md:2932); capacity computed at superseded sizing | "Any future round uses the corrected universe from a fresh pre-registration" (RETURN.md:2729). Corrected universe exists (RETURN.md:2706); never re-run. Capacity rescales to 8,176 USD/yr at the enforced sizer but z is unchanged |
| H-H low idiosyncratic volatility | **closed AND separately disqualified** | fails, "and is separately DISQUALIFIED by a disclosed defect" | 2026-07-26 | holdout excess −0.25 bp/day, 95 % CI [−5.9, +5.4], z −0.086; capacity −157 USD/yr (n = 31 holdout months); **51 of 124 formation books contain SPLG** | RETURN.md:2861, :2923, :2932; PROGRESS.md:827, :831 | universe recovery path admitted funds with empty name/exchange; "NOT FIXED HERE, because the fix belongs to the universe classifier" (RETURN.md:2932) | "Any future round uses the corrected universe from a fresh pre-registration" (RETURN.md:2729). **Enabling condition MET the same evening (`d6ad37a`, 1,218 names, 0 funds, RETURN.md:2706-2709); never re-run, yet counted in "seven families ... zero survivors". AUDIT-A-AiTrader-5** |
| H-I 52-week high proximity | closed | fails (interval spans zero, capacity below floor, sign flips between periods) | 2026-07-26 | holdout excess +2.35 bp/day, 95 % CI [−7.9, +12.5], z 0.451; capacity 1,477 USD/yr (n = 31 holdout months) | RETURN.md:2863, :2924; PROGRESS.md:827 | 0 of 115 books contaminated | "Any future round uses the corrected universe from a fresh pre-registration" (RETURN.md:2729); corrected universe exists; never re-run |
| Candidates rejected before testing (14 in the capacity round, 8 in the cross-sectional round) | closed pre-test | arithmetic (below the 2,500 USD/yr floor), untestable (missing data), or structural duplicate | 2026-07-26 | per-candidate annual USD at Level 1 sizing: 13F 600, turn-of-month 480, FOMC drift 392, crypto→equity 1,200, intraday first-half-hour 1,764, equity cross-section 500–1,000 (n = 12 of 14 rejected) | PROGRESS.md:849; RETURN.md:3167-3178, :2785-2792 | "No fundamentals", "No earnings dates", "**No sector classification**", "No shares outstanding", "no options data", "`whale_activity` ... has zero rows" | the capacity floor itself and the named data gaps. **The sizing-change trigger fired 2026-07-27 (PROGRESS.md:503, :191): AUDIT-A-AiTrader-1. The sector gap is answerable inside this repository: AUDIT-A-AiTrader-9** |
| Price-only hypothesis programme (family level) | closed | exhausted | 2026-07-26 | "Six families now resolved" (PROGRESS.md:849), later "Seven families ... with zero survivors" (RETURN.md:2968) | PROGRESS.md:849; RETURN.md:3234, :2968 | 8-symbol database; Level 1 sizing | "the calculus changes only with a new information axis, maker execution (rescues nothing here), or a sizing change that is not on the table" (PROGRESS.md:849). **New information axis: MET 2026-07-26 and honoured (breadth load, PROGRESS.md:836; the news experiment). Sizing change: MET 2026-07-27 and NOT read — AUDIT-A-AiTrader-1. Maker execution: still unbuilt (OQ 11)** |
| Buy and hold after costs, as the standing bar | shipped (standing rule) | measurement | 2026-07-26 | SPY +17.7 %/yr Sharpe 1.13; BTC +16.1 %/yr Sharpe 0.55, both after the fee model | PROGRESS.md:854; CONTEXT.md:106; RETURN.md:3288 | — | none |
| Capacity floor as a permanent research gate | shipped (standing rule) | gate | 2026-07-26 | 2,500 USD/yr = "roughly 20 bp net at 10 trades per day at Level 1 sizing" (500 USD notional) | PROGRESS.md:854; CONTEXT.md:108 | — | **none registered — and the sizing it is expressed in was superseded 2026-07-27; the same quantity is 4.96 bp at the enforced sizer (PROGRESS.md:189). AUDIT-A-AiTrader-3** |

---

## C. LLM council layer

| entry | status | closure kind | closure date | deciding figure (n) | file:line | blockers | registered reopen conditions |
|---|---|---|---|---|---|---|---|
| Council predicts price at 4h, first pass | **parked** | thin-sample abstention, explicitly NOT a refutation | 2026-07-26 | pooled +92.3 bp/call, z 1.706, interval spans zero (n = 37 calls / 9 clusters vs a floor of 10 clusters) | PROGRESS.md:794; RETURN.md:2630 | symbol diversity: "66 independent symbols are needed and the record has 9" (PROGRESS.md:803) | "Confirming the observed effect needs 20 clusters, 150 evaluations, about 25 USD. Establishing a 50 bp effect needs 66 clusters, 509 evaluations, about 85 USD" — **MET by the 2026-07-27 wide run** |
| Council predicts price at 4h, wide run | closed | powered negative | 2026-07-27 | pooled −0.5 bp/call, z −0.046, interval [−22.5, +21.4], hit rate 50.0 % (n = 274 calls / 80 clusters vs a pre-registered floor of 272 calls / 66 clusters) | PROGRESS.md:775; RETURN.md:2437, :2393; AUDIT.md:16 | GPT-5.5 and Gemini billing exhaustion mid-run (315 of 389 and 73 of 389 calls failed) — PROGRESS.md:780; RETURN.md:2419 | "What this does NOT establish: that no effect of any size exists. The interval admits roughly plus or minus 22 bp" (RETURN.md:2474). **The boundary clause's two hurdles were both superseded the same day: AUDIT-A-AiTrader-10** |
| Council 1-hour secondary horizon | closed | negative after fees | 2026-07-27 | 55.5 % hit rate, nets −0.7 bp after fees (n within the 274) | PROGRESS.md:783 | — | none registered |
| Is the stated confidence calibrated? | closed | "not practically settleable at this effect size" | 2026-07-27 | pooled Spearman rho +0.0357, bootstrap CI [−0.067, +0.145], z 0.660 (n = 274 calls / 80 clusters); every individual provider negative (Opus −0.0996, Gemini −0.1156, GPT-5.5 −0.2724); bucket hit rates monotone 42.3/49.1/50.6/54.1 % | RETURN.md:2217-2223; PROGRESS.md:784, :751 | **"There are not 1,149 liquid instruments this system can evaluate" (RETURN.md:2221)** | "reaching the corrected bar at the observed rho needs 1,149 clusters, 14.4 times the current sample". **Premise contradicted inside this repository (19,744 tickers; 1,218 U-LIQ-500 members; 2,769–3,123 news-band members): AUDIT-A-AiTrader-6.** Cross-repo lead 7 |
| Is abstention informative? | closed | no effect demonstrated (pooled crossed the bar, dissolved on class decomposition) | 2026-07-27 | +23.2 bp [+6.1, +40.4], z 2.660 pooled; within crypto z 0.787, within equity z 1.534 (n = 503 abstained / 274 directional, 80 clusters) | RETURN.md:2197-2206; PROGRESS.md:750 | "CLUSTERING ON SYMBOL DOES NOT ABSORB AN ASSET-CLASS MIX EFFECT" (PROGRESS.md:747) | "Recorded as a methodological lesson for any future split of this record" |
| Is rejection a filter? | closed | no effect demonstrated (same asset-mix artifact) | 2026-07-27 | −26.4 bp [−46.5, −6.4], z −2.581 pooled; decomposed z −0.554 crypto / −0.907 equity (n = 187 endorsed / 202 declined) | RETURN.md:2231, :2241; PROGRESS.md:752 | as above | none registered |
| Does predictive quality differ by asset class? | closed | clean null | 2026-07-27 | pooled crypto-minus-equity excess −0.2 bp, 95 % CI [−64.0, +63.7], z −0.005 | RETURN.md:2245; PROGRESS.md:753 | **GPT-5.5's equity column "not measurable at all: all 244 calls errored on the quota exhaustion"** (RETURN.md:2254-2256) | none registered; the latch "is process state and deliberately not persisted: an account stays dry until it is funded" (RETURN.md:2311) |
| Is the council its best member? / "THE COUNCIL IS GPT-5.5" | shipped as a structural finding | survives as a tendency (~82 %), not an identity | 2026-07-27 | on the 73 fully-answered evaluations: 22 directional council verdicts, GPT-5.5 also directional in 18, council-only in 4, zero sign disagreements | RETURN.md:2464-2466, :2531; PROGRESS.md:786 | only wave C1 produced full three-provider data (RETURN.md:2482); "the full-sample comparison was destroyed by the outage and is not reported as an answer" | implicit: a funded three-provider run |
| Council rationale phrases (Task 5) | parked | exploratory throughout | 2026-07-27 | 3 of 23 phrases cross \|z\| 2, "which is what chance produces uncorrected"; "consolidat" 71.7 % hit on 53 calls | PROGRESS.md:754 | — | "recorded only so a future pre-registered test could name it in advance" |
| Council agreement inversion | closed | did not replicate | 2026-07-27 | 52.2 / 49.3 / 33.3 % vs a recorded 100 / 80 / 25; top cell n = 3 | PROGRESS.md:785, :801 | — | none registered |
| The council layer as a whole | closed / deactivated | "No measured justification for the layer remains on this evidence"; weights zeroed 2026-07-27, GUI panels removed 2026-07-29 | 2026-07-27 | five axes measured, nothing demonstrated on any; zero trades in the whole recorded history carry a council decision id; the two non-GPT providers are 78.4 % of spend and changed 18 % of directional verdicts | RETURN.md:2274, :2468; PROGRESS.md:755 | GPT-5.5 absent from the entire equity half (RETURN.md:2278); 80 clusters over two days in one market regime | "Whether a layer with no demonstrated value and a known cost stays in the system is an operator's decision against this evidence, not a conclusion this session is entitled to draw." (RETURN.md:2276). **The absent provider's blocker is a funding state this repository prices at $8–85: AUDIT-A-AiTrader-16** |
| `min_directional_votes: 1` | **open** | evaluation-period choice | 2026-07-18 | none | PROGRESS.md:94 | — | "Revisit with outcome data once single-voter verdicts accumulate. 2 is the conservative setting." — **outcome data now exists (the 2026-07-26/27 scoring rounds) and it was not revisited** |

---

## D. Engine layers, factors, controls and scope decisions

| entry | status | closure kind | closure date | deciding figure (n) | file:line | registered reopen conditions |
|---|---|---|---|---|---|---|
| `dnn_advisory` | deactivated by zero weight, code retained | benched (synthetic-trained champion), then weight 0.15 → 0.0 | 2026-07-18 bench; 2026-07-27 zero weight | 58 of 716 recorded evaluations contained it; removing it alone flips 23 across the 0.65 floor, max delta 0.1301; challenger trained on 47,900 synthetic-regime samples, no production row | RETURN.md:2092, :2028; CONTEXT.md:90, :80; PROGRESS.md:77 | "restoring a weight reactivates the layer with no other change" (RETURN.md:2028; CONTEXT.md:90); promotion needs ≥ 200 real samples, better walk-forward Sharpe, no worse drawdown (CONTEXT.md:175); un-bench requires a real-data champion whose id matches the serving artifact (RETURN.md:6022) |
| `whale_signal` | deactivated by zero weight, code retained | "has never been scored against outcomes at all" | 2026-07-27 | 2,162 factor outputs at mean confidence 0.5466, weight 0.10 → 0.0; `whale_activity` and `whale_signal_history` hold 0 rows in both databases | AUDIT.md:94; DATA_AUDIT.md:15-28; config/default_config.yaml:754-758; CONTEXT.md:90, :94; RETURN.md:1963 | "restoring a weight reactivates the layer with no other change" (config/default_config.yaml:747-748); "a measurement against the record the ENGINE wrote" (CONTEXT.md:94). **The "unmeasurable" inference is challenged: AUDIT-A-AiTrader-2.** Cross-repo lead 8 |
| `rl_advisory` | shipped off, gated, inert | never activated; gate corrected 2026-07-27/29 | 2026-07-05 build | real-fill gate reads **9 of 500** after the provenance correction (was 243–249 of 500 counting synthetic fills) | AUDIT.md:91; AUDIT-2026-07-29.md:91; RETURN.md:2043; CONTEXT.md:92; WEEKLOG.md:55 | 500 real `strategy`-origin fills with `real_feed`/`backfill` provenance (CONTEXT.md:92; PROGRESS.md:74) |
| `dnn_rl` (legacy factor name) | dead | no code emits the name; 2,100 rows stop 2026-07-02 | 2026-07-27 | removing it alone flips 318 of 716 evaluations across the 0.65 floor | RETURN.md:2094, :1990 | none; "no key exists and none is added" (RETURN.md:2002) |
| Three-layer removal (dnn + whale + RL) | **blocked, never performed** | stopped by its own Task-2 safety gate | 2026-07-27 | 716 of 716 recorded evaluations change composed confidence; 386 cross the 0.65 floor, all newly PASSING, zero newly failing (n = 716) | RETURN.md:2083, :2098; PROGRESS.md:719-740; CONTEXT.md:94 | three options recorded, none applied: accept the loosening explicitly; compensate the denominator; remove only `rl_advisory` (RETURN.md:2124-2126). Removal permitted only if a replay shows composition equivalence (CONTEXT.md:94) |
| Composition rule (weight-normalised mean gates trades) | **OPEN** | analysed, not changed | — | 716 evaluations replayed, 386 flipped across the 0.65 floor, all permissive (n = 716) | AUDIT.md:18, :124 | "Reconsider the composition rule so unskilled factors do not gate trades" — AUDIT.md:164. Partially mitigated by zeroing two weights; the mean rule itself is unchanged |
| Crypto in all trading paths | closed / removed at the universe layer | scope decision; data path retained | 2026-07-27 | "Crypto round trips cost 50 bp against equity's 1.14 to 4.87 bp"; P26 split −48.78 bp crypto vs −2.73 equity; council abstains 87–94 % crypto vs 43–47 % equity; 11,978 changed decisions | RETURN.md:1431; PROGRESS.md:576-606; CONTEXT.md:84 | none registered; "the venue plumbing stays wired" and bars still flow; restoration priced at "one class in `mal::scope`". **The deciding cost ratio moved inside this repository: AUDIT-A-AiTrader-15** |
| Volume filter | reopened and re-closed | "DOES NOTHING in SIP terms" | 2026-07-25 | marginal rejected set −1.68 bp [−2.28, −1.09] vs accepted −1.98; removal-arm delta z −0.04 (n = 14,581 marginal) | RETURN.md:3576 | "SIP-only: this does NOT transfer to the live IEX path" — a measurement on live venue volume (RETURN.md:4741). Cross-repo lead 9 |
| ATR volatility band | reopened and re-closed | "DOES NOTHING at the bar" | 2026-07-25 | marginal rejected −1.24 bp [−1.81, −0.67], z +1.59 vs accepted; removal arm +0.49 bp, z 1.09 (n = 15,123 marginal) | RETURN.md:3575 | the one-sided (low-tail-only) band named as the most promising change; tested post hoc at n = 359 (RETURN.md:4064) but **not** on the 61x deep-history tape |
| RSI-2 entry threshold (equity 5 vs crypto 10) | reopened and re-closed | threshold tuning shows no transferable edge | 2026-07-25 | 54-cell grid, "**Zero positive cells out of 108 cell-periods**"; selected cell failed holdout confirmation, delta −0.07 bp, z −0.14 | RETURN.md:3581 | none remaining |
| `max_trade_notional_cap_pct`, `default_position_sizing_method` | closed / removed | enforced nowhere, 0 blocks in a 1,912-row record | 2026-07-27 | 23 Level 1 and sizing keys traced, 21 enforced, 2 unenforced | RETURN.md:853, :862-864 | none |
| `cooldown_minutes_after_loss_breach` | reopened and wired | harness-versus-engine divergence closed; 240 minutes derived, not chosen | 2026-07-27 | the consecutive-loss brake was 1,578 of 1,912 blocks, 82.5 % of all RiskGate refusals | RETURN.md:868, :874 | proven by a behavioural test at a tightened cap (RETURN.md:899) |
| `min_confidence_default` per strategy | parked | "deferred to the sleeve build, unresolved rather than settled" | 2026-07-27 | 0.65 global at `risk_gate.cpp:75`; 334 blocks in the record; confidence NULL on 3,614 of 3,615 rejected decisions | RETURN.md:117, :982-984; CONTEXT.md:74; PROGRESS.md:193 | "declare it on the ORDER, defaulting to current behaviour, built by the session that builds the consuming sleeve and never before it" (CONTEXT.md:74); three concrete steps at RETURN.md:905-907 |
| Per-symbol `max_consecutive_losses` | parked | "not built here because nothing consumes it yet" | 2026-07-27 | per-symbol would create "400 absorbing states instead of one" without a release | RETURN.md:876, :885 | "Per-symbol keying remains a reasonable future addition ALONGSIDE the global brake, never instead of it"; derived duration 1440 minutes if built (RETURN.md:969) |
| Base-check gate fails open toward spending (AUDIT 4.2) | **OPEN** | flagged, not fixed | — | `proceed=True` on any exception or missing key | AUDIT.md:104 | "Decide the base-check gate's fail direction deliberately" — AUDIT.md:164. **Not done as of the anchor** |
| `KillSwitch::trip` silent no-op when disabled (AUDIT 4.3) | **OPEN flag** | "a flag to check, not a confirmed defect" | — | risk/risk_gate.cpp:99-105 | AUDIT.md:106 | "I did not confirm the engine always enables it" |
| RiskGate check-count 14 vs 18 (AUDIT 4.4) | CLOSED | corrected | 2026-07-29 | 18 `fail(` sites | AUDIT.md:108; AUDIT-2026-07-29.md:84 | none |
| Three ctest failures from an uncommitted config edit (AUDIT 4.5) | CLOSED | control-file lever added; ctest 34/34 | 2026-07-29 | 24/27 or 25/28 historically → 34/34 | AUDIT.md:110; AUDIT-2026-07-29.md:85 | none |
| `news_ingestion` mock catalyst | REMOVED | remove, confidence high | recommended 2026-07-27, executed by 2026-07-29 | hash constant, no consumer | AUDIT.md:88; AUDIT-2026-07-29.md:87; CONTEXT.md:82 | none registered. **Its "Known Issues" entry was never struck: AUDIT-A-AiTrader-18** |
| `research_satellite` | **PARKED** (remove-or-shelve, confidence medium) | every recorded pass screens out at conviction 0.0 | 2026-07-27 | 31 theses, every one `flat` (n = 31) | AUDIT.md:89; DATA_AUDIT.md:176-178 | "confirm the 70/30 sleeve machinery does not assume a live satellite" — AUDIT.md:89. `research_conviction_threshold: 0.70` at config/default_config.yaml:407, never varied |
| Dash UI (`ui/`) | **OPEN flag, no call** | consider removing, confidence low | 2026-07-27 | 2,958 + 8,620 lines of two UIs | AUDIT.md:92 | "confirm no operator workflow depends on Dash-only panels" |
| Price-only research programme, as the audit's headline recommendation | **CLOSED — "finished"** | powered negative + seven dead families | 2026-07-27 | council pooled excess −0.5 bp, interval [−22.5, +21.4] (n = 274 calls / 80 clusters) | AUDIT.md:16, :154 | "Open a genuinely new information axis (fundamentals, alternative data, a different holding period, or a capacity model that does not fight the position limit) ... should start from a pre-registration against the corrected universe" — AUDIT.md:160. **AUDIT-A-AiTrader-10.** Cross-repo lead 1 |

---

## E. Capabilities built but gated, and their gate conditions

| entry | status | closure kind | closure date | deciding figure (n) | file:line | gate / blocker | reopen condition |
|---|---|---|---|---|---|---|---|
| Global-session equity rotation | **SCAFFOLDED, DISABLED** | venue capability | — | only NY reachable; London and Asia `venue_unavailable` | LIVE_READINESS.md:14-16; CONTEXT.md:193 | Alpaca is US-only; IBKR not connected; per-region whitelists are empty placeholders; rotation flag off | all three conditions at LIVE_READINESS.md:32-40. **Not met at the anchor** (checked; IBKR still DISABLED, AUDIT.md:36) |
| Adaptive react layer, flag 1 `adaptive_news_feed_enabled` (observe) | **BUILT, SHIPS DISABLED** | deliberate, not a closure | 2026-07-16 | 12,000-step run behaviourally identical with flags off; 272 trades / 136 closed; zero adaptive rows, zero API calls | LIVE_READINESS.md:55-62; PROGRESS.md:23 | needs a Finnhub key and an Anthropic key; Finnhub "Verified working 2026-07-16 (`one quote ok`, about 108 ms)" | Prerequisites at LIVE_READINESS.md:114-129. **TRIGGER ARGUABLY MET**: both credentials are now demonstrated at production scale by the collector (COLLECTION_LOG.md:26, :117-277), and the observe rung costs ~$0.40/day and moves no position (LIVE_READINESS.md:124-126). Not revisited |
| Adaptive flag 2 `adaptive_watchlist_shaping_enabled` | DISABLED | requires flag 1 | — | — | LIVE_READINESS.md:131-136 | requires the feed and a healthy discovery funnel | the discovery-funnel row below |
| Adaptive flag 3 `adaptive_react_defensive_enabled` | DISABLED | requires flag 1 | — | — | LIVE_READINESS.md:138-150 | requires observe-mode evidence on names actually held | LIVE_READINESS.md:141-150 |
| Aggressive event path | **REFUSED AS A DESIGN, not deferred** | permanent | — | enforced in three places, two languages | LIVE_READINESS.md:83-95, :154 | n/a | none, deliberately |
| `discovery` funnel → watchlist → Stage C | **BLOCKED, unresolved 37 days** | threshold borrowed from another gate | flagged 2026-07-18, never decided | 7 real council verdicts 0.5265–0.5938 vs a 0.60 floor (n = 7); Stage A 5,605 / B 1,929 / **C 394**; `dnn_bias` −0.31 to −0.34 on all 12 symbols ever evaluated | AUDIT.md:90; PROGRESS.md:103-104; DATA_AUDIT.md:191; discovery/evaluate.py:72, :339; config/default_config.yaml:281 | the 0.60 trading-gate threshold reused as `conviction_floor`; the synthetic DNN's veto | "Nothing downstream of Stage C can work until this is decided. **No dependencies.**" (PROGRESS.md:103); "Settle the floor first or this only moves the failure" (PROGRESS.md:104). **AUDIT-A-AiTrader-8** |
| Long-term sleeve / `research_satellite` | blocked, ships DISABLED | prerequisite gate | 2026-07-16 | 12,000-step run byte-identical with flags off | PROGRESS.md:25 | `long_term_sleeve_enabled` false; depends on a watchlist that has never gained a member | operator decision + the discovery blocker above |
| Live trading (`try_enable_live`) | not started, by design | deliberate | ongoing | "still never called, by design" | PROGRESS.md:34, :63-66, :128 | four-block approval gate | "turning it on is a human decision made against evidence, not a milestone to reach" |
| Two sleeves on separate accounts | blocked | structural prerequisite | 2026-07-27 | "the map key is venue, never account"; the consecutive-loss brake and trade counter are global single ints | PROGRESS.md:529; CONTEXT.md:76; RETURN.md:982, :1125 | no per-account dimension in `PortfolioState` / `trades_today_` | "Either run each as its own process with its own database, the only option today, or add an account dimension" |
| Whale live-fetch parsers | open (known limit) | partial verification | ongoing | "verified against one recorded SEC 13F payload only" (n = 1) | PROGRESS.md:127 | live off behind `WHALE_LIVE_ENABLED` / `SEC_EDGAR_ENABLED` (both `true` in config at :693-694) | verification against live responses for the other feeds |
| A real end-to-end council verdict in the live window | open | the event has not occurred | 2026-07-13 | none | PROGRESS.md:130 | "needs a fresh EMA20/100 crossover or Bollinger reentry to actually occur" | the market event |
| Validation-week PASS criteria (stability, trade/signal rate, spend, data) | **REGISTERED, no completion entry** | pre-flight baseline written 2026-07-24 | — | baseline: 247 closed rows lifetime, +$420.87 realized; 6 real-path native exits lifetime; RL counter 243 of 500 | WEEKLOG.md:46-66 | — | "A LOW TRADE COUNT IS NOT ATTRIBUTABLE to either change individually and must not be read as a verdict on either" (WEEKLOG.md:64). **No week-summary section exists at the anchor**; the last digest is 2026-07-16 (WEEKLOG.md:5) |
| Run-ending conditions (unattributable stop, fabrication trip, stranded position, DB corruption, spend breach) | REGISTERED | — | — | — | WEEKLOG.md:70 | — | "DOES NOT END THE RUN: a Level 1 halt doing its job" (WEEKLOG.md:71) |

---

## F. Audit and data-audit findings

| entry | status | closure date | deciding figure (n) | file:line | reopen condition |
|---|---|---|---|---|---|
| AUDIT 4.1 RL real-fill gate counts synthetic fills | CLOSED, corrected | 2026-07-29 | 243 counted vs 6 real | AUDIT.md:102; AUDIT-2026-07-29.md:91 | none outstanding |
| AUDIT 4.6 absence-as-evidence, RL gate the surviving instance | CLOSED with 4.1 | 2026-07-29 | — | AUDIT.md:112 | none |
| AUDIT Task 5 thin spot 1: symbol clustering could not absorb an asset-class mix effect | CLOSED, self-caught | 2026-07-27 | abstention z 2.66, rejection z −2.581, both dissolved on decomposition | AUDIT.md:140 | none |
| AUDIT Task 5 thin spot 2: per-trade SE treated correlated trades as independent | CLOSED, self-caught | — | z 2.91 as registered → z 1.73 clustered, 5 correlated same-night trades | AUDIT.md:142 | none |
| AUDIT Task 5 thin spot 3: benchmark implementation corrected after seeing data | DISCLOSED, not reopened | — | pooled z 4.974 → 2.66 | AUDIT.md:144 | none |
| Lead 1 (2026-07-29): CLAUDE.md cites cost figures the fee model no longer produces | CLOSED, corrected same day | 2026-07-29 | 1.14–4.87 bp cited vs ~17.8 / ~41.2 bp measured; tier-1 unchanged at 0.5–0.9 bp | AUDIT-2026-07-29.md:27-41 | "tier 4's 41.2 bp sits within 20 percent of crypto's 50 bp, which weakens the rhetorical gap". **AUDIT-A-AiTrader-15** |
| Lead 2: the direction of error moved permissive | **OPEN, named as a pattern** | — | tick ladder 7.0/8.0/6.5/12.0 with `usable: false`; AMENDMENT 5's net→gross move | AUDIT-2026-07-29.md:43-57, :163-175 | "any future softening of 'a gross-positive net-negative result licenses no trade' should be read as the failure mode this finding warns about" |
| Lead 3: judgment-imbalance confound uncontrolled | CLOSED — AMENDMENT 6 added the permutation null the same day | 2026-07-29 | 37 next-open anchors vs 12 same-close; 26 POSITIVE / 7 NEGATIVE on n = 33 | AUDIT-2026-07-29.md:59-72; EXPERIMENT.md:408-421 | the uninformative-null thresholds, EXPERIMENT.md:530-540 |
| Task A: `trades.origin` documentation gap (`reconciliation`) | **OPEN** | — | 3 rows, 2026-07-24 | AUDIT-2026-07-29.md:96-97; DATA_AUDIT.md:93-95 | none registered |
| Task B: yaml-vs-fallback default equality unpinned by test | **OPEN, named rather than fixed** | — | defaults agree today (1.0/1.0/8.0/9.0/1.0/1.0) | AUDIT-2026-07-29.md:108-115 | "a caller loading a DIFFERENT yaml ... falls to defaults silently" |
| Task C: three latent fabrication candidates | CLOSED — all three closed with 12 new tests | 2026-07-29 | no realized instance found | AUDIT-2026-07-29.md:128-159 | none |
| Task D3: Stage 1 model comparison unresolved, chosen model never compared | **OPEN** | — | one usable arm of four | AUDIT-2026-07-29.md:176-179 | "nothing in the specification forces it closed". **AUDIT-A-AiTrader-14** |
| Task D5: mutation tests not re-run; a value-pinning test would not catch a shared formula error | **OPEN** | — | — | AUDIT-2026-07-29.md:188-191 | none |
| Task E2: a gross positive does not distinguish the model from a trivial reader | **DISCLOSED, comparator not added** | 2026-07-29 | no baseline arm exists | AUDIT-2026-07-29.md:208-216; EXPERIMENT.md:556-566 | "a new hypothesis and needs its own pre-registration". Cross-repo lead 6 |
| Task E4: the 20-minute delay untested against quote reality | **OPEN** | — | S4 50 bp median spread | AUDIT-2026-07-29.md:225-228 | none registered |
| DATA_AUDIT: `whale_signal` produced 2,162 outputs "from zero whale data" | **CLOSED as unmeasurable** | 2026-07-27 | `whale_activity` 0 rows, `whale_signal_history` 0 rows, `model_outputs` 2,162 whale rows at mean 0.5466 | DATA_AUDIT.md:15-28, :72-73 | none registered. **CHALLENGED: AUDIT-A-AiTrader-2** — both tables are written only by `ops/demo.py` (:113, :116) and are empty by design on the live path (api_server/store.py:617-619; tests/test_api_server.py:2709-2711) |
| DATA_AUDIT: `model_registry` empty while documents describe it as populated | **OPEN, NOT RESOLVED** | 2026-07-27 | 0 rows | DATA_AUDIT.md:165-172, :213-214 | "either promotion never ran against this database, or the registry is file-based under `ml_factor/models/`, which I did not verify" |
| DATA_AUDIT: `trades.origin` enum wrong in both directions | **OPEN** | 2026-07-27 | `strategy` 262, `reconciliation` 3; `adaptive_react` and `rebalance` never occurred | DATA_AUDIT.md:93-104, :161-163 | none |
| DATA_AUDIT: `research_thesis` 31 theses, all `flat` | **OPEN observation** | 2026-07-27 | n = 31 | DATA_AUDIT.md:176-178 | none registered; feeds the AUDIT.md:89 shelve recommendation |
| DATA_AUDIT: 12 blank `entry_decision.first_reject` rows | **OPEN, NOT RESOLVED** | 2026-07-27 | n = 12 | DATA_AUDIT.md:115-116, :212 | none |
| DATA_AUDIT: 108 `watchdog_restart` events in one-second bursts | CLOSED — known test contamination, deliberately left | 2026-07-27 | 108 rows on 2026-07-24 | DATA_AUDIT.md:197-201 | "it would corrupt any restart-frequency or stability metric computed from `events`" |
| DATA_AUDIT: 3,411 `real_feed` bars with `volume_source = fabricated_zeroed` | CLOSED — internally consistent two-axis provenance | 2026-07-27 | n = 3,411 | DATA_AUDIT.md:203-206 | none |
| DATA_AUDIT: three undocumented empty tables (`adaptive_event`, `adaptive_interpretation`, `adaptive_poll`) | **OPEN hygiene** | 2026-07-27 | 0 rows each | DATA_AUDIT.md:74-76, :78-81 | none |
| WEEKLOG: 4 `risk_block` events with empty payload | **OPEN anomaly** | 2026-07-16 | n = 4 | WEEKLOG.md:44 | none |
| 2026-07-17 whale-toggle events | CLOSED — mechanism established and reproduced | 2026-07-21 | 6 events 08:39Z–08:44Z; reproduced 3 ways against a scratch control dir | PROGRESS.md:86 | "RESIDUAL, unprovable rather than open: which trigger fired at 08:39Z" |

---

## G. Blockers recorded anywhere in this repository, with their state at the anchor

| blocker | recorded at | state at anchor |
|---|---|---|
| Tick multiple "behind a paid data subscription" / "SIP-entitled market-data subscription" | RETURN.md:1637, :308, :418 | **EXPIRED** 2026-07-28 (`e60232a`, no RETURN.md entry), measured 2026-07-29 — RETURN.md:249 |
| Exchange calendar stale at 2026-07-24 | RETURN.md:365, :437 | **EXPIRED** 2026-07-28 — RETURN.md:274 |
| Operator's separate Anthropic experiment key not created | RETURN.md:435 | **EXPIRED** 2026-07-28 — RETURN.md:357 |
| `claude-opus-4-8` rejects `temperature` (killed the Opus comparison arm) | RETURN.md:602; EXPERIMENT.md:2438-2443 | **EXPIRED** 2026-07-28 (diagnosed, now a CLAUDE.md hard rule); arm never re-run — RETURN.md:539; EXPERIMENT.md:2138-2140 |
| Gemini account quota exhausted (killed the Gemini arm at n = 2) | RETURN.md:604 | expired at least once (2026-07-21, RETURN.md:5360); state at anchor unknown |
| OpenAI account exhausted (killed the entire GPT-5.5 equity arm, 244/244) | RETURN.md:2254, :2419 | **OPEN** — a funding state, priced by this repository at $8–85 (RETURN.md:2622, :2311) |
| Survivorship-free universe "which this database cannot provide" | RETURN.md:3485 | **EXPIRED** 18 h later — RETURN.md:2985 |
| Fund contamination of `universe_membership` | RETURN.md:2932 | **FIXED** 2026-07-26 evening (0 funds, 0 unclassified, 1,218 names) — RETURN.md:2706-2709 |
| Level 1 five-position cap as the cross-sectional family's binding constraint | RETURN.md:2966 | **EXPIRED** 2026-07-27 (raised to 10) — RETURN.md:1137; recomputed z at n=10 is no higher, so the verdict survives |
| Level 1 500 USD per-position notional, behind the capacity gate | CONTEXT.md:108; PROGRESS.md:854 | **EXPIRED** 2026-07-27 (400–2,000 USD enforced) — PROGRESS.md:191, :503, :522 |
| "No sector classification in the database" | RETURN.md:2787, :2353, :2488 | **ANSWERABLE in-repo** via Finnhub `stock/profile2`, demonstrated 44/47 on 2026-07-28 — news_experiment/collect.py:163-180 |
| "No shares outstanding / no market capitalisation" | RETURN.md:655, :688, :2788; EXPERIMENT.md:858-863 | **OPEN** |
| "No earnings dates", "no options data" in `analysis_bars.db` | RETURN.md:2786, :3177 | **OPEN** |
| `whale_activity` holds zero rows in both databases | RETURN.md:1963, :3167; DATA_AUDIT.md:17-18 | **OPEN as a fact; not evidence of unmeasurability** — the tables are unwritten on the live path by design (api_server/store.py:617-619) |
| Live IEX volume not comparable to SIP history | RETURN.md:3576, :4019 | **OPEN** |
| No per-account / per-sleeve / per-strategy dimension in the RiskGate | RETURN.md:982, :1125; CONTEXT.md:76 | **OPEN**; blocking prerequisite for two simultaneous sleeves |
| Shorts not executable on Alpaca crypto | RETURN.md:3186 | **OPEN**; moot after the crypto removal |
| Equity borrow cost has no term in the fee model | RETURN.md:677; EXPERIMENT.md:2222-2224; PROGRESS.md:555 | **OPEN** |
| Historical ETB / shortability at a past formation | RETURN.md:580; EXPERIMENT.md:2377-2380 | **OPEN** — "no backfilled study can reconstruct it" |
| Discovery conviction floor 0.60 inherited from the trading gate | PROGRESS.md:103; discovery/evaluate.py:72 | **OPEN, live in code at the anchor, 37 days** |
| Maker execution: fill probability, time-to-fill, adverse selection, venue mechanics | EXPERIMENT.md:393-399; PROGRESS.md:254 | **OPEN, four measurements named, none run** |

---

## H. Standing figures superseded by a later dated entry in this repository

| figure as stated | file:line | superseding measurement | file:line | revisited? |
|---|---|---|---|---|
| "roughly a 20 bp net edge at 10 trades per day" at "about 500 USD notional per trade" | CONTEXT.md:108; PROGRESS.md:854 | 4.96 bp at the 2,000 USD sizer, 3.97 bp at the 2,500 USD ceiling | PROGRESS.md:189, :256, :272; EXPERIMENT.md:1870-1871 | **no** — AUDIT-A-AiTrader-3 |
| "the crypto gross hurdle behind such a net is 70 bp" as the standing research hurdle | CONTEXT.md:108; PROGRESS.md:854 | scope narrowed to US equities; traded tier 0.5–0.9 bp | PROGRESS.md:576, :211; CONTEXT.md:84 | **no** |
| "22 bp survives neither the 50 bp crypto round trip nor the 2,500 USD capacity floor at Level 1 sizing" | PROGRESS.md:788 | both hurdles superseded the same day | PROGRESS.md:576, :503, :189 | **no** — AUDIT-A-AiTrader-10 |
| "the council does not predict price at any size this system could trade ... would clear neither the 50 bp crypto round trip nor the 2,500 USD capacity floor" | AUDIT.md:154 | same | PROGRESS.md:189; AUDIT-2026-07-29.md:33 | **no** — AUDIT-A-AiTrader-10 |
| "an effect that small would clear neither the fee model nor the capacity floor" | PROGRESS.md:755 | same | PROGRESS.md:189, :211 | **no** |
| "Crypto round trips cost 50 bp against equity's 1.14 to 4.87 bp in the tradeable bands" | RETURN.md:1431 | measured tier 3 17.8 bp, tier 4 41.2 bp | RETURN.md:144, :251 | **partly** — bracket-noted at CONTEXT.md:84 and PROGRESS.md:211; the ratio collapse is not stated. AUDIT-A-AiTrader-15 |
| "the tick multiple is still unmeasured" | CONTEXT.md:60; news_experiment/collect.py:7-9, :731-735 | measured, tier 3 = 8.0, tier 4 = 9.0 | PROGRESS.md:266, :270 | **no** (collect.py disclosed at PROGRESS.md:195; CONTEXT.md:60 not) — AUDIT-A-AiTrader-12 |
| "stage 3 stays blocked on that operator decision" | CONTEXT.md:54 | "STAGE 3 IS NOW UNBLOCKED" | PROGRESS.md:258, :229, :197 | **no** — AUDIT-A-AiTrader-12 |
| "Collection has not started" / "NO COLLECTION DATA EXISTED"; PROGRESS "Current State" | PROGRESS.md:7, :187, :217, :248, :276 | 19 collected sessions 2026-07-30..2026-08-24 | COLLECTION_LOG.md:117-277 | **no** — AUDIT-A-AiTrader-12 |
| "60 days x 107.7 = ~6,460 observations, 6.5x the requirement" | EXPERIMENT.md:2348 | the same document's own design-effect requirement at the measured k | EXPERIMENT.md:1798-1801, :2346 | **no** — AUDIT-A-AiTrader-11 |
| "Remaining synthetic-mock cap: the RiskGate `required_model_agreement_count` gate" | PROGRESS.md:78 | mock catalyst removed; ctest 33/33 then 34/34 | PROGRESS.md:557, :209; CONTEXT.md:82 | **no** — AUDIT-A-AiTrader-18 |
| "the suite is 30 of 31 and the plateau claim ... is not currently demonstrable" | PROGRESS.md:122 | ctest 34 of 34 | PROGRESS.md:7, :209 | **no** — AUDIT-A-AiTrader-18 |
| "1.14 to 4.87 bp" equity band hurdle in the scope decision | CONTEXT.md:84 (original text) | corrected in place with a bracketed 2026-07-29 note | CONTEXT.md:84 | **yes — corrected** |
| "ctest 7/7", "RiskGate: 14 hard checks" | PROGRESS.md:7, :11 (original text) | corrected to 34/34 and 18 refusal sites | PROGRESS.md:7, :11, :211 | **yes — corrected** |
| AUDIT.md's line citations into PROGRESS.md / CONTEXT.md (e.g. PROGRESS.md:193 for the council result, now at :775) | AUDIT.md:16, :154 | append-only drift in the tracking files | PROGRESS.md:775 | **no** — hygiene, below the S4 threshold, not raised |

---

## I. Leads for the cross-repository pass

Every blocker or reopen condition below might be satisfied by work held in another repository in
this programme. **No other repository has been read.** The "best guess" column is an inference from
repository names and from the kind of data the condition needs; it is a starting point for the
cross-repo pass, not a claim. Leads whose condition can only be met inside AiTrader (the sizing
change, the discovery floor, the Amendment 1/2 reversal paths) are deliberately excluded.

| # | condition, verbatim where short | file:line | what another repository would have to hold | best guess |
|---|---|---|---|---|
| 1 | "Open a genuinely new information axis (fundamentals, alternative data, a different holding period, or a capacity model that does not fight the position limit)" — the price-only programme's own registered reopen | AUDIT.md:160; PROGRESS.md:849 | any tested non-price axis on US equities, with a pre-registration against a corrected universe | InsiderExperiment (SEC filings axis), NPDExperiment / NPLExperiment (news/text axis), VRPExperiment (options-derived axis), ETFExperiment (flow/sector axis) |
| 2 | "Whether capability matters is UNANSWERED ... must be redone before the cheap-tier decision" — the `claude-opus-4-8` / `gemini-3.1-pro-preview` / DeepSeek head-to-head, 21 recorded headlines, cost seven cents | EXPERIMENT.md:2454-2458, :2721-2724; PROGRESS.md:400-401; RETURN.md:612 | a head-to-head of these same model strings on an identical scored judgment task, or a record of the corrected Opus request shape in practice | PMExperiment (prediction-market LLM judgments) first; then NPLExperiment / NPDExperiment; MLCryptoEngine if it runs an LLM arm |
| 3 | "`analysis_bars.db` holds no shares outstanding and no market capitalisation ... If shares outstanding become available, the removal analysis should be redone against actual market cap" | EXPERIMENT.md:858-863, :2861-2863; RETURN.md:655, :688 | a shares-outstanding or market-cap panel for US equities, ideally point-in-time | InsiderExperiment (needs issuer-level filings data), ETFExperiment (holdings/weights imply caps) |
| 4 | Borrow availability and cost on the short side in the ADV 2.07M–65.3M band, "modelled nowhere in this repository, and the fee model has no borrow term" | EXPERIMENT.md:2222-2224, :2836-2837; RETURN.md:677; PROGRESS.md:555 | a short-borrow cost model or an ETB/borrow-rate history for US small and mid caps | HFExperiment (execution-cost modelling), InsiderExperiment, ORBExperiment |
| 5 | Maker-execution feasibility and historical shortability: fill probability at the touch by stratum, time-to-fill against the horizon, post-fill drift conditional on filling, venue order-type mechanics; plus "ETB status at a past formation is not recoverable from this endpoint" | EXPERIMENT.md:393-399, :2263-2270, :2377-2380; PROGRESS.md:254 | measured limit-order fill rates or queue position on a US equity venue; a point-in-time borrow or shortability panel | HFExperiment and ORBExperiment (intraday US equity execution); solclear / solattn hold fill data but on a different venue class, so transferability must be argued |
| 6 | A baseline comparator for "the pipeline predicts" vs "the model understands": "a pre-registered baseline arm, same headlines, universe, windows, benchmark, estimator and bars, a reader with no claimed understanding, plus a margin test with its own bar" | EXPERIMENT.md:556-566; RETURN.md:167; AUDIT-2026-07-29.md:208-216 | a non-LLM news-sentiment or keyword scorer that could be run over the same headline set | NPLExperiment / NPDExperiment first; PMExperiment if it holds a keyword baseline |
| 7 | Council confidence calibration needs "1,149 clusters, 14.4 times the current sample" | RETURN.md:2221; PROGRESS.md:751 | a larger scored-verdict record — any repository holding ≥ ~1,150 independent scored LLM verdicts with realised outcomes | PMExperiment (verdict-per-market records), MLCryptoEngine, NPLExperiment |
| 8 | `whale_signal` "has never been scored against outcomes at all"; `analysis_bars.db` holds zero whale rows, and the 13F-following candidate was rejected pre-code at 600 USD/yr | CONTEXT.md:90, :94; PROGRESS.md:849; DATA_AUDIT.md:15-28 | a populated 13F / Form 4 / whale store with outcomes attached | InsiderExperiment (strongest guess), NPDExperiment |
| 9 | Consolidated-tape (SIP) quote access beyond the Alpaca historical window, for the > 15-minute-recency constraint; and live venue volume comparable to SIP history | EXPERIMENT.md:2572-2577; RETURN.md:3576, :4741 | a paid market-data subscription, a stored NBBO history, or a live consolidated-volume record | HFExperiment, ORBExperiment |
| 10 | "No sector classification in the database" as it constrains the wide council run's independence design (the sector-momentum rejection itself is answerable in-repo) | RETURN.md:2353, :2488 | a sector/industry mapping for US equities usable as an independence stratifier | ETFExperiment (sector-ETF membership), InsiderExperiment |
| 11 | H-A's holdout is exhausted: "holdout already read for this hypothesis", so no untouched period exists in this database | RETURN.md:3323 | an untouched post-2024 US equity bar panel that this programme has not scored | ORBExperiment, HFExperiment, ETFExperiment |
| 12 | Pre-code rejections on missing data: "No earnings dates", "no options data" | RETURN.md:2786, :3177 | an earnings-calendar panel; an options chain or implied-vol surface | VRPExperiment (options, strongest guess for the second); NPDExperiment for earnings dates |
| 13 | `model_registry` empty: "either promotion never ran against this database, or the registry is file-based under `ml_factor/models/`, which I did not verify" | DATA_AUDIT.md:169-171 | not cross-repo — resolvable in place. Listed only because a sibling ML repository may share the registry convention | MLCryptoEngine |
