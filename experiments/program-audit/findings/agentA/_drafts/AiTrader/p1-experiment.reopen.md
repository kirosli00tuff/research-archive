# REOPEN LEDGER — AiTrader, part p1-experiment

Repository: AiTrader, anchored SHA `705e0ed128b7e184be6c1a23dcd06750c524c525` (main, 2026-08-24).
Covers entries whose primary evidence lies in `EXPERIMENT.md`, `AUDIT.md`, `AUDIT-2026-07-29.md`,
`DATA_AUDIT.md`, `LIVE_READINESS.md`, `COLLECTION_LOG.md`, `WEEKLOG.md`, `docs/`.
This ledger is factual, not advocacy. All paths are `AiTrader/<path>:<line>`.

**Repository-wide fact bearing on every "later entry" column:** the last substantive session commit
is `f819b68`, 2026-07-29. The four commits from there to the anchor (`8a49239` 2026-08-04,
`f1fb308` 2026-08-06, `b5c2236` 2026-08-18, `705e0ed` 2026-08-24) change only `COLLECTION_LOG.md`
and two `.gitignore` lines. `PROGRESS.md` has no session entry dated 2026-08. So no reopen condition
in this repository has been *evaluated* since 2026-07-29, while 18 collection days accrued
(10,113 symbol-day rows, 2,320 model calls, $1.2809) — COLLECTION_LOG.md:117-277.

---

## A. The news-drift experiment (EXPERIMENT.md)

| entry | status | closure kind | closure date | deciding figure (n) | file:line |
|---|---|---|---|---|---|
| Primary hypothesis: an LLM's three-way headline judgment predicts next-session excess return, ADV 2.07M-65.3M | **OPEN — collecting** | none yet | — | none; no headline has been scored against a price | EXPERIMENT.md:704-710; status header EXPERIMENT.md:3-4 |
| Stage 0 (the specification) | **SHIPPED / CLOSED** | accepted, binding | 2026-07-28 | n/a | EXPERIMENT.md:3-15 |
| Stage 1 (feasibility) | **CLOSED, partial** | cleared on every stop condition it was designed to test | 2026-07-28 | see per-task rows | EXPERIMENT.md:2696-2732 |
| Stage 2 (collector build) | **SHIPPED** | built, demonstrated, standalone | 2026-07-28 | 33 directional demo rows, n=33 | EXPERIMENT.md:2889-2898 |
| Stage 3 (collection) | **RUNNING** | started 2026-07-29T22:54:53Z | — | 18 of the registered 60 day clusters | COLLECTION_LOG.md:2-3, :270-277 |

**Blockers on the experiment (all stated in EXPERIMENT.md):**

| blocker | file:line | state at anchor |
|---|---|---|
| Tick multiple "unmeasurable without paid quote data" (AMENDMENT 2) | EXPERIMENT.md:2400-2401, :2841-2843 | **LIFTED** 2026-07-29 via historical SIP endpoint — EXPERIMENT.md:2565-2579 |
| RTH scheduling for the tick measurement | EXPERIMENT.md:2459-2478 | **LIFTED** — historical query bounds time by construction, EXPERIMENT.md:2572-2577 |
| IEX-only feed (not the consolidated tape) | EXPERIMENT.md:2521-2529 | **LIFTED** — SIP historical, venue-diversity check passes 97.9 %, EXPERIMENT.md:2621-2625 |
| Model comparison unresolved; DeepSeek has no credential; Opus arm lost to a `temperature` request bug; Gemini exhausted after 2 calls | EXPERIMENT.md:2428-2446, :2721-2724, :2730-2732 | **NOT LIFTED. Both causes have expired** (Opus quirk is now a hard rule, EXPERIMENT.md:2138-2140; the experiment holds a separate Anthropic credential, COLLECTION_LOG.md:26-27) and no redo is recorded. See DRAFT-p1-experiment-6 |
| Stage 3 blocked pending an operator amendment decision after the cost measurement | EXPERIMENT.md:2688-2694 | **LIFTED** by AMENDMENT 5, EXPERIMENT.md:247-259 |
| Borrow cost on the short side unmodelled (no borrow term in the fee model) | EXPERIMENT.md:2222-2224, :2836-2837 | **OPEN** |
| `--i-have-read-the-preconditions` is an attestation, not a verifier; three of five named checks are not start-time checks | EXPERIMENT.md:660-682 | **OPEN, reported not fixed** |
| Anthropic credential shared with the council (AMENDMENT 3, OQ 9) | EXPERIMENT.md:2240-2250 | **LIFTED in practice** — separate experiment key + latch, COLLECTION_LOG.md:26-27, `credential_shared: false`, `latch_separate: true` at COLLECTION_LOG.md:76-77 |

**Registered reopen / reversal conditions:**

| condition | file:line | trigger met? |
|---|---|---|
| AMENDMENT 1 (rank→ADV) reverses on "evidence that the effect tracks rank better than ADV ... by scoring the same observations under both memberships" | EXPERIMENT.md:2304-2306; field note EXPERIMENT.md:2078 | **NO, and partly unreachable** — 446 of 3,501 rank-band members at the 2026 formation lie outside the ADV band and are never queried (EXPERIMENT.md:957; `reject("outside_adv_band")` at news_experiment/universe.py:191; 2,419 such rejections at COLLECTION_LOG.md:30). See DRAFT-p1-experiment-5 |
| AMENDMENT 2 (5.00→10.00 floor) reverses on "evidence that the effect is concentrated in 5 to 10 USD names ... by scoring the excluded 5-to-10 band separately" | EXPERIMENT.md:1091-1095 | **NO, and unreachable from this collection** — sub-10.00 symbols are rejected before sampling (news_experiment/universe.py:163-164; `MIN_MEDIAN_CLOSE = 10.00` at news_experiment/spec.py:39; 3,042 rejections at COLLECTION_LOG.md:30). See DRAFT-p1-experiment-3 |
| AMENDMENT 2 residual: "If a later reading decides the mechanism matters more than the dispersion, the correct response is to lower the floor and accept the worse hurdle" | EXPERIMENT.md:885-890 | **Arguably met** — the price-floor lever is recorded as exhausted after the tick measurement (EXPERIMENT.md:266-267, :2674-2678), which is the "later reading" the clause anticipates. Not revisited |
| AMENDMENT 3 (Haiku) reverses only if all three hold: a DeepSeek credential exists; a head-to-head shows DeepSeek is not worse; the cost gap becomes decision-relevant | EXPERIMENT.md:2749-2761 | **NO** — none of the three has changed |
| AMENDMENT 5 (band kept in full) reverses if "the thin strata cannot meet the 30-cluster per-stratum floor", or if the gross signal concentrates entirely in S1/S2 | EXPERIMENT.md:353-356 | **NOT YET EVALUABLE** — 18 of 60 day clusters collected, no scoring session has run |
| Primary abstention trigger: permutation null UNINFORMATIVE if pooled minority directional share < 10 % or fewer than 30 mixed day clusters | EXPERIMENT.md:530-540, :2272-2281 | **NOT YET EVALUATED** — demonstration first look was 21 % minority on n=33 (EXPERIMENT.md:429-435) |
| NEUTRAL rate above 80 % is a reportable failure of the design | EXPERIMENT.md:1615-1618 | **NOT EVALUATED**; the one recorded coverage block shows 106 judged / 67 scored directional, i.e. ~37 % NEUTRAL (COLLECTION_LOG.md:60-74) |
| Story-group re-run trigger: >10 % of observations sharing a `story_group_id` | EXPERIMENT.md:1658-1663, :470-473 | **NOT EVALUATED** |
| rho and residual volatility "must be recomputed before the stop rule fires"; if realised rho > 0.05 the required n is recomputed and collection continues | EXPERIMENT.md:1806-1810, :2176-2178 | **NOT DONE** — 10,113 rows available since 2026-08; see DRAFT-p1-experiment-7 |
| Strength scale revisited on DEGENERATE USE (>80 % on one value, or fewer than three of five values occur) or SATURATED USE | EXPERIMENT.md:2790-2802 | **NOT MET on the one recorded look** — `distinct_values: 3, degenerate: false`, histogram {2:23, 3:28, 4:16} (COLLECTION_LOG.md:66-75) — but three of five values is exactly the boundary, and no later day's histogram is recorded |
| Strength anchors revisited on SKEW (median strength 1 or 5) or TYPE DOMINANCE | EXPERIMENT.md:2804-2815 | **NOT MET** on the one recorded look (median 3) |
| Maker execution is the named resolution path for a gross-positive net-negative result; forbidden to rely on before fill probability, time-to-fill, adverse selection and venue mechanics are measured | EXPERIMENT.md:377-399, :2263-2270 | **NOT TRIGGERED** — no outcome exists |
| Powered-negative definition: at ≥60 clusters, the pooled gross interval's upper bound below 30 bp with no primary clearing 2.50 | EXPERIMENT.md:1818-1823 | **NOT TRIGGERED** — 18 clusters |
| A day whose `source_failed` rate exceeds 20 % is excluded from the cluster count; >5 % emits a CRITICAL event | EXPERIMENT.md:2054-2059 | **NOT TRIGGERED** — `source_failed: 0`, `source_failed_fraction: 0.0` (COLLECTION_LOG.md:63-65) |

**Open Questions, status as the document records them (EXPERIMENT.md:2161-2281):**

| # | subject | status recorded | file:line |
|---|---|---|---|
| 1 | thin-end news coverage | ANSWERED by Stage 1; residual: 18 of 50 S4 symbols silent, effective S4 sample ~2/3 nominal | EXPERIMENT.md:2165-2172, :2332-2337 |
| 2 | arrival rate | ANSWERED — measured 0.359/symbol-day against an assumed 0.10, n=200 symbols / 1,538 headlines | EXPERIMENT.md:2174, :2318-2324 |
| 3 | 180 bp residual volatility and rho = 0.05 | **OPEN, recompute registered and not done** | EXPERIMENT.md:2176-2178 |
| 4 | rank drift / cost dispersion | RESOLVED by AMENDMENT 1 + 2 + the 2026-07-29 tick measurement | EXPERIMENT.md:2180-2195 |
| 5 | DeepSeek credential / hard-rule conflict | CLOSED by AMENDMENT 3, by removing the conflict | EXPERIMENT.md:2197-2204 |
| 6 | DeepSeek provider error semantics | LARGELY CLOSED; residual: the `model_failed` vs `source_failed` split "remains a design claim rather than an exercised one" | EXPERIMENT.md:2206-2219 |
| 7 | short-side feasibility | LARGELY ANSWERED — ETB 62.1-93.3 % by stratum, n=30/30/30/29; borrow COST still unmodelled | EXPERIMENT.md:2221-2227, :2364-2380 |
| 8 | benchmark's own cost | ADDRESSED for the primary by AMENDMENT 5 | EXPERIMENT.md:2229-2238 |
| 9 | shared Anthropic credential | OPEN as written; **superseded in practice** by the separate experiment key | EXPERIMENT.md:2240-2250 vs COLLECTION_LOG.md:26-27 |
| 10 | strength distribution unknown | OPEN | EXPERIMENT.md:2252-2261 |
| 11 | maker execution named and unmeasured | OPEN | EXPERIMENT.md:2263-2270 |
| 12 | realised directional balance unknown | OPEN | EXPERIMENT.md:2272-2281 |

**Stage 1 task verdicts (EXPERIMENT.md:2308-2495):**

| task | verdict | deciding figure (n) | file:line |
|---|---|---|---|
| 1 coverage | PASS, stop condition not met | 98.0/80.0/72.0/64.0 % any-news by stratum, n=50 each, 1,538 headlines | EXPERIMENT.md:2318-2330 |
| 2 arrival rate | PASS, 6.5x margin claimed | 0.359/symbol-day, n=200 | EXPERIMENT.md:2341-2354 |
| 3 ETB | PASS | 83.3/93.3/80.0/62.1 %, n=30/30/30/29 | EXPERIMENT.md:2364-2375 |
| 4 latency | PASS, delay left at 20 min | p95 ~2.4 s total | EXPERIMENT.md:2384-2396 |
| 5 tick multiple, attempt 1 | UNMEASURED (after hours) | S1 870.5 vs S4 303.5 ticks, n=10 each — ordering backwards | EXPERIMENT.md:2409-2420 |
| 5 attempt 2 | BLOCKED (market closed) | no data | EXPERIMENT.md:2459-2470 |
| 5 attempt 3 | MEASURED AND UNUSABLE | ladder 39.0/72.0/104.5/62.5, n=402 rows; 42.1 % of the sample were funds | EXPERIMENT.md:2501-2549 |
| 5 attempt 4 | MEASURED AND USABLE | ladder 7.0/8.0/6.5/12.0 ticks, n=1,402 rows / 157 symbols; strict monotonicity FAILS, judged near-monotone | EXPERIMENT.md:2588-2619 |
| 6 model comparison | **INCONCLUSIVE, never redone** | haiku 21/21 parsed; opus 0/21 reached (request bug); gemini n=2 | EXPERIMENT.md:2422-2458, :2734-2742 |

---

## B. AUDIT.md (2026-07-27) — recommendations and findings

| entry | status | closure kind | closure date | deciding figure (n) | file:line | reopen condition |
|---|---|---|---|---|---|---|
| Price-only research programme | **CLOSED — "finished"** | powered negative + seven dead families | 2026-07-27 | council pooled excess −0.5 bp, interval [−22.5, +21.4], n=274 calls / 80 clusters | AUDIT.md:16, :154 | "Open a genuinely new information axis ... should start from a pre-registration against the corrected universe" — AUDIT.md:160. Challenged: DRAFT-p1-experiment-2 |
| `news_ingestion` mock catalyst | **REMOVED** | remove, confidence high | recommended 2026-07-27, executed by 2026-07-29 | hash constant, no consumer | AUDIT.md:88; removal confirmed AUDIT-2026-07-29.md:87 | none registered |
| `research_satellite` | **PARKED** (remove-or-shelve, confidence medium) | every recorded pass screens out at conviction 0.0 | 2026-07-27 | 31 theses, every one `flat` (n=31) | AUDIT.md:89; DATA_AUDIT.md:176-178 | "confirm the 70/30 sleeve machinery does not assume a live satellite" — AUDIT.md:89. Note `research_conviction_threshold: 0.70` at config/default_config.yaml:407, never varied |
| `discovery` funnel | **PARKED — "dormant with a known blocker"** | conviction floor above pipeline output | 2026-07-27 | 7 council verdicts, 0.5265-0.5938 vs floor 0.60 (n=7) | AUDIT.md:90; figure at PROGRESS.md:103 (other reader's document); floor at discovery/evaluate.py:72,:339 and config/default_config.yaml:281 | "the one place a future information axis could plug in" — AUDIT.md:90; mismatch flagged open at EXPERIMENT.md:654-655. Challenged: DRAFT-p1-experiment-4 |
| `rl_advisory` | **PARKED, inert** | keep in tree, correct the gate, do not enable | 2026-07-27 | zero recorded evaluations; removal replays neutral | AUDIT.md:91 | gate `rl_min_real_fills` 500; counter read 243 of 500 against 6 real-path lifetime exits — WEEKLOG.md:55. Gate corrected by 2026-07-29 (AUDIT-2026-07-29.md:91) |
| Dash UI (`ui/`) | **OPEN flag, no call** | consider removing, confidence low | 2026-07-27 | 2,958 + 8,620 lines of two UIs | AUDIT.md:92 | "confirm no operator workflow depends on Dash-only panels" — AUDIT.md:92 |
| `whale_signal` | **DEACTIVATED (weight 0.0), kept in tree** | no demonstrated skill, drags the gate | 2026-07-27 | 2,162 outputs, mean confidence 0.5466, weight 0.10 | AUDIT.md:94; DATA_AUDIT.md:15-28; config/default_config.yaml:754-758 | "restoring a weight reactivates the layer with no other change" — config/default_config.yaml:747-748. Challenged: DRAFT-p1-experiment-1 |
| 4.1 RL real-fill gate counts synthetic fills | **CLOSED** | corrected | by 2026-07-29 | 243 counted vs 6 real | AUDIT.md:102; AUDIT-2026-07-29.md:91 | none outstanding |
| 4.2 base-check gate fails open toward spending | **OPEN** | flagged, not fixed | — | `proceed=True` on any exception / missing key | AUDIT.md:104 | "Decide the base-check gate's fail direction deliberately" — AUDIT.md:164. **Not done as of the anchor** |
| 4.3 `KillSwitch::trip` silent no-op when disabled | **OPEN flag** | "a flag to check, not a confirmed defect" | — | risk/risk_gate.cpp:99-105 | AUDIT.md:106 | "I did not confirm the engine always enables it" — AUDIT.md:106 |
| 4.4 RiskGate check-count 14 vs 18 | **CLOSED** | corrected 2026-07-29 | 2026-07-29 | 18 `fail(` sites | AUDIT.md:108; AUDIT-2026-07-29.md:84 | none |
| 4.5 three ctest failures from an uncommitted config edit | **CLOSED** | control-file lever added; ctest 34/34 at 2026-07-29 | 2026-07-29 | 24/27 or 25/28 historically | AUDIT.md:110; AUDIT-2026-07-29.md:85 | none |
| 4.6 absence-as-evidence, RL gate the surviving instance | **CLOSED** with 4.1 | — | 2026-07-29 | — | AUDIT.md:112 | none |
| 4B composition rule: weight-normalised mean is the wrong gate rule | **OPEN** | analysed, not changed | — | 716 evaluations replayed, 386 flipped across the 0.65 floor, all permissive (n=716) | AUDIT.md:18, :124 | "Reconsider the composition rule so unskilled factors do not gate trades" — AUDIT.md:164. Partially mitigated by zeroing two weights (config/default_config.yaml:757-758); the mean rule itself is unchanged |
| Task 5 thin spot 1: symbol clustering could not absorb an asset-class mix effect | **CLOSED, self-caught** | lesson recorded, crossings not reported | 2026-07-27 | abstention z 2.66, rejection z −2.581, both dissolved on decomposition | AUDIT.md:140 | none |
| Task 5 thin spot 2: per-trade SE treated correlated trades as independent | **CLOSED, self-caught** | hypothesis disqualified on the clustered reading | — | z 2.91 as registered → z 1.73 clustered, 5 correlated same-night trades | AUDIT.md:142 | none |
| Task 5 thin spot 3: benchmark implementation corrected after seeing data | **DISCLOSED, not reopened** | change moved the result the uncomfortable way | — | pooled z 4.974 → 2.66 | AUDIT.md:144 | none |

---

## C. AUDIT-2026-07-29.md — findings

| entry | status | closure kind | closure date | deciding figure (n) | file:line | reopen condition |
|---|---|---|---|---|---|---|
| Lead 1: CLAUDE.md cites cost figures the fee model no longer produces | **CLOSED** | corrected same day | 2026-07-29 | 1.14-4.87 bp cited vs ~17.8 / ~41.2 bp measured; tier-1 unchanged at 0.5-0.9 bp | AUDIT-2026-07-29.md:27-41 | crypto-exclusion conclusion stands on tier 1; "tier 4's 41.2 bp sits within 20 percent of crypto's 50 bp, which weakens the rhetorical gap" — AUDIT-2026-07-29.md:33-35 |
| Lead 2: the direction of error moved permissive | **OPEN, named as a pattern** | no action taken | — | tick ladder 7.0/8.0/6.5/12.0 with `usable: false`; AMENDMENT 5's net→gross move | AUDIT-2026-07-29.md:43-57, :163-175 | "any future softening of 'a gross-positive net-negative result licenses no trade' should be read as the failure mode this finding warns about" — AUDIT-2026-07-29.md:55-57 |
| Lead 3: judgment-imbalance confound uncontrolled | **CLOSED** | AMENDMENT 6 added the permutation null the same day | 2026-07-29 | 37 next-open anchors vs 12 same-close; 26 POSITIVE / 7 NEGATIVE on n=33 | AUDIT-2026-07-29.md:59-72; EXPERIMENT.md:408-421 | uninformative-null thresholds, EXPERIMENT.md:530-540 |
| Task A: `trades.origin` documentation gap (`reconciliation`) | **OPEN** | recorded in DATA_AUDIT and nowhere else | — | 3 rows, 2026-07-24 | AUDIT-2026-07-29.md:96-97; DATA_AUDIT.md:93-95 | none registered |
| Task B: yaml-vs-fallback default equality unpinned by test | **OPEN, named rather than fixed** | low risk | — | defaults agree today (1.0/1.0/8.0/9.0/1.0/1.0) | AUDIT-2026-07-29.md:108-115 | "a caller loading a DIFFERENT yaml ... falls to defaults silently" — AUDIT-2026-07-29.md:111-113 |
| Task C: three latent fabrication candidates | **CLOSED** | all three closed 2026-07-29 with 12 new tests | 2026-07-29 | no realized instance found | AUDIT-2026-07-29.md:128-159; closure at PROGRESS.md (2026-07-29 Fable 5 entry) | none |
| Task D3: Stage 1 model comparison unresolved, chosen model never compared | **OPEN** | "nothing in the specification forces it closed" | — | one usable arm of four | AUDIT-2026-07-29.md:176-179 | see DRAFT-p1-experiment-6 |
| Task D5: mutation tests not re-run; a value-pinning test would not catch a shared formula error | **OPEN** | scope constraint | — | — | AUDIT-2026-07-29.md:188-191 | none |
| Task E2: a gross positive does not distinguish the model from a trivial reader | **DISCLOSED, comparator not added** | recorded without being added | 2026-07-29 | no baseline arm exists | AUDIT-2026-07-29.md:208-216; EXPERIMENT.md:556-566 | "a new hypothesis and needs its own pre-registration" — EXPERIMENT.md:563-566 |
| Task E4: the 20-minute delay untested against quote reality | **OPEN** | "Adequate for gross, optimistic for net" | — | S4 50 bp median spread | AUDIT-2026-07-29.md:225-228 | none registered |

---

## D. DATA_AUDIT.md (2026-07-27) — findings

| entry | status | closure kind | closure date | deciding figure (n) | file:line | reopen condition |
|---|---|---|---|---|---|---|
| `whale_signal` produced 2,162 outputs "from zero whale data" | **CLOSED as unmeasurable** | inference from two empty tables | 2026-07-27 | `whale_activity` 0 rows, `whale_signal_history` 0 rows, `model_outputs` 2,162 whale rows at mean 0.5466 | DATA_AUDIT.md:15-28, :72-73 | none registered. **Challenged: DRAFT-p1-experiment-1** — both tables are written only by `ops/demo.py` (ops/demo.py:113, :116) and are empty by design on the live path (api_server/store.py:617-619; tests/test_api_server.py:2709-2711) |
| `model_registry` empty while documents describe it as populated | **OPEN, NOT RESOLVED** | stated open rather than guessed | 2026-07-27 | 0 rows | DATA_AUDIT.md:165-172, :213-214 | "either promotion never ran against this database, or the registry is file-based under `ml_factor/models/`, which I did not verify" — DATA_AUDIT.md:169-171 |
| `trades.origin` enum wrong in both directions | **OPEN** | documented, not fixed | 2026-07-27 | `strategy` 262, `reconciliation` 3; `adaptive_react` and `rebalance` never occurred | DATA_AUDIT.md:93-104, :161-163 | none |
| `research_thesis`: 31 theses, all `flat` | **OPEN observation** | recorded | 2026-07-27 | n=31 | DATA_AUDIT.md:176-178 | none registered; feeds the AUDIT.md:89 shelve recommendation |
| 12 blank `entry_decision.first_reject` rows | **OPEN, NOT RESOLVED** | uncertain | 2026-07-27 | n=12 | DATA_AUDIT.md:115-116, :212 | none |
| 108 `watchdog_restart` events in one-second bursts | **CLOSED — known test contamination, deliberately left** | append-only journal | 2026-07-27 | 108 rows on 2026-07-24 | DATA_AUDIT.md:197-201 | "it would corrupt any restart-frequency or stability metric computed from `events`" — DATA_AUDIT.md:200-201 |
| 3,411 `real_feed` bars with `volume_source = fabricated_zeroed` | **CLOSED — internally consistent two-axis provenance** | explained | 2026-07-27 | n=3,411 | DATA_AUDIT.md:203-206 | none |
| Three undocumented empty tables (`adaptive_event`, `adaptive_interpretation`, `adaptive_poll`) | **OPEN hygiene** | recorded | 2026-07-27 | 0 rows each | DATA_AUDIT.md:74-76, :78-81 | none |

---

## E. LIVE_READINESS.md — gated capabilities

| entry | status | closure kind | closure date | deciding figure (n) | file:line | blockers | reopen condition |
|---|---|---|---|---|---|---|---|
| Global-session equity rotation | **SCAFFOLDED, DISABLED** | venue capability | — | Alpaca is US-only | LIVE_READINESS.md:14-16 | IBKR not connected; per-region whitelists empty placeholders; rotation flag off — LIVE_READINESS.md:32-40 | all three conditions at LIVE_READINESS.md:32-40. **Not met at the anchor** |
| Adaptive react layer, flag 1 `adaptive_news_feed_enabled` (observe) | **BUILT, SHIPS DISABLED** | deliberate, not a closure | 2026-07-16 | 12,000-step run behaviourally identical with flags off; 272 trades / 136 closed | LIVE_READINESS.md:55-62 | needs a Finnhub key and an Anthropic key; Finnhub "Verified working 2026-07-16 (`one quote ok`, about 108ms)" — LIVE_READINESS.md:103-112 | Prerequisites at LIVE_READINESS.md:114-129. **TRIGGER ARGUABLY MET**: both credentials are now demonstrated at production scale by the collector (COLLECTION_LOG.md:26, :117-277); the observe rung costs ~$0.40/day and moves no position (LIVE_READINESS.md:124-126). Not revisited |
| Adaptive flag 2 `adaptive_watchlist_shaping_enabled` | **DISABLED** | requires flag 1 | — | — | LIVE_READINESS.md:131-136 | requires the feed and a healthy discovery funnel | discovery funnel health — see section B, `discovery` row |
| Adaptive flag 3 `adaptive_react_defensive_enabled` | **DISABLED** | requires flag 1 | — | — | LIVE_READINESS.md:138-150 | requires observe-mode evidence on names actually held | LIVE_READINESS.md:141-150 |
| Aggressive event path | **REFUSED AS A DESIGN, not deferred** | permanent | — | enforced in three places, two languages | LIVE_READINESS.md:83-95, :154 | n/a | none, deliberately |

---

## F. WEEKLOG.md — the paper-trading validation week

| entry | status | closure kind | closure date | deciding figure (n) | file:line | reopen condition |
|---|---|---|---|---|---|---|
| Validation-week PASS criteria (stability, trade/signal rate, spend, data) | **REGISTERED, no completion entry** | pre-flight baseline written 2026-07-24 | — | baseline: 247 closed rows lifetime, +$420.87 realized; 6 real-path native exits lifetime; RL counter 243 of 500 | WEEKLOG.md:46-66 | "A LOW TRADE COUNT IS NOT ATTRIBUTABLE to either change individually and must not be read as a verdict on either" — WEEKLOG.md:64. **No week-summary section exists at the anchor**; the last digest is 2026-07-16 (WEEKLOG.md:5) |
| Run-ending conditions (unattributable stop, fabrication trip, stranded position, DB corruption, spend breach) | **REGISTERED** | — | — | — | WEEKLOG.md:70 | "DOES NOT END THE RUN: a Level 1 halt doing its job" — WEEKLOG.md:71 |
| 4 `risk_block` events with empty payload | **OPEN anomaly** | recorded | 2026-07-16 | n=4 | WEEKLOG.md:44 | none |

---

## G. Possibly met by work in a DIFFERENT repository — for the cross-repo pass

Listed for the cross-repository pass only. I have not read any other repository; these are flagged
because the condition names a capability, data source, or measurement another repository in this
programme is likely to hold.

| condition | file:line | what another repository might supply |
|---|---|---|
| "Whether capability matters is UNANSWERED ... must be redone before the cheap-tier decision" — the model-capability comparison | EXPERIMENT.md:2454-2458, :2721-2724 | Any repository that has run a head-to-head of `claude-opus-4-8` / `gemini-3.1-pro-preview` / a cheap tier on an identical scored task, or that records the corrected Opus request shape in practice |
| Borrow availability and cost on the short side in the ADV 2.07M-65.3M band, "modelled nowhere in this repository, and the fee model has no borrow term" | EXPERIMENT.md:2222-2224, :2836-2837 | A repository holding a short-borrow cost model or an ETB/borrow-rate history for US small and mid caps |
| Market capitalisation for the price-floor removal analysis: "`analysis_bars.db` holds no shares outstanding and no market capitalisation ... If shares outstanding become available, the removal analysis should be redone against actual market cap" | EXPERIMENT.md:858-863, :2861-2863 | Any repository holding a shares-outstanding or market-cap panel for US equities |
| Maker-execution feasibility: fill probability at the touch, time-to-fill, post-fill drift conditional on filling, venue order-type mechanics | EXPERIMENT.md:393-399, :2263-2270 | A repository that has measured limit-order fill rates or queue position on a US equity venue |
| Historical ETB / shortability at a past formation: "ETB status at a past formation is not recoverable from this endpoint" | EXPERIMENT.md:2377-2380 | A repository holding a point-in-time borrow or shortability panel |
| A baseline comparator for "the pipeline predicts" vs "the model understands": a keyword-sentiment reader over the same headlines, universe, windows, benchmark and bars | EXPERIMENT.md:556-566 | A repository holding a non-LLM news-sentiment or keyword scorer that could be run over the same headline set |
| Consolidated-tape (SIP) quote access beyond the Alpaca historical window, for the >15-minute-recency constraint | EXPERIMENT.md:2572-2577 | A repository with a paid market-data subscription or a stored NBBO history |
| "Open a genuinely new information axis (fundamentals, alternative data, a different holding period, or a capacity model that does not fight the position limit)" | AUDIT.md:160 | Any repository in this programme testing a non-price axis on US equities or crypto |
| `model_registry` empty: "either promotion never ran against this database, or the registry is file-based under `ml_factor/models/`" | DATA_AUDIT.md:169-171 | Not cross-repo; resolvable in place. Listed only because a sibling ML repository may share the registry convention |
