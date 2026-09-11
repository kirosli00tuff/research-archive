# Agent A draft findings — AiTrader, part p1-experiment

Repository: AiTrader, anchored SHA `705e0ed128b7e184be6c1a23dcd06750c524c525` (main, 2026-08-24).
Read from `/home/kiros-li/.cache/program-audit/scratchpad/snap/AiTrader/` unless a line says otherwise.
Assigned documents read in full: `EXPERIMENT.md` (2,906 lines), `AUDIT.md` (174), `AUDIT-2026-07-29.md` (263),
`DATA_AUDIT.md` (229), `LIVE_READINESS.md` (161), `COLLECTION_LOG.md` (277), `WEEKLOG.md` (71), `docs/`.
Source, config and test files were read for corroboration; `PROGRESS.md`, `RETURN.md`, `CONTEXT.md` were
read only where an assigned document cites them, and those citations are flagged.

Direction A throughout: the case that a hypothesis or capability was closed on weaker grounds than its
label implies. Recomputation scripts:
`/home/kiros-li/.cache/program-audit/scratchpad/work/agentA-AiTrader-p1/recompute.py` and `discovery.py`.

---

### DRAFT-p1-experiment-1
- **Repository / SHA:** AiTrader / 705e0ed128b7e184be6c1a23dcd06750c524c525
- **Hypothesis or artifact:** the `whale_signal` advisory factor (SEC EDGAR 13F / Form 4), deactivated to zero weight on 2026-07-27
- **Direction:** A
- **Class:** OVER_CLOSED
- **Severity:** S1
- **Label:** DERIVED
- **Claim challenged (verbatim quote):** "INFERRED. A factor with no source table and no history table cannot have been reading whale data, so those 2,162 confidences were produced without an input. That makes `whale_signal` a fabricated input which nonetheless carried 0.10 of the ensemble weight and sat inside the weight-normalised mean that decides the Level 1 confidence floor. The 2026-07-27 deactivation was better justified than the session that performed it knew: it treated `whale_signal` as unmeasured, and the data says it was unmeasurable." — AiTrader/DATA_AUDIT.md:22-28
- **Evidence:**
  - The inference rests on two tables being empty: "`whale_activity` holds **0 rows**. `whale_signal_history` holds **0 rows**." — AiTrader/DATA_AUDIT.md:17-19, tabulated at AiTrader/DATA_AUDIT.md:72-73.
  - **Neither table is written on the live or paper path, by design, and the repository says so in two places written before this audit.** "HONEST ABOUT THE ACTIVITY COUNT. `whale_activity` holds RAW per-fetch rows, and nothing in the live path writes it: the engine asks the bridge for a SCORED signal and never persists the activity behind it (ops/demo.py is the only writer)." — AiTrader/api_server/store.py:617-619. Pinned by test: "whale_activity (raw per-fetch rows) is empty by design: the engine asks the bridge for a scored signal and never persists the activity behind it." — AiTrader/tests/test_api_server.py:2709-2711 (test `test_whale_feeds_labels_the_activity_count_honestly`).
  - Verified across the whole tree: the only `INSERT` into either table is the offline demo seeder — AiTrader/ops/demo.py:113 (`whale_activity`) and AiTrader/ops/demo.py:116 (`whale_signal_history`); its own docstring reads "Fill whale_activity + whale_signal_history via the offline whale service." — AiTrader/ops/demo.py:80. Every other reference in `ui/`, `api_server/` and `tests/` is a SELECT or a fixture.
  - So both tables read 0 in production **whether or not the whale feed was live**. The emptiness carries no information about the input, and the audit's own Task 1 conflates reference with writer: "**WRITTEN BY NOTHING:** none. Every table has at least one source reference." — AiTrader/DATA_AUDIT.md:87, against a table listing `whale_activity` at 19 src refs and `whale_signal_history` at 11 (AiTrader/DATA_AUDIT.md:72-73).
  - The feed was configured ON, and its source is free and keyless: `sec_edgar_enabled: true` and `whale_live_enabled: true` — AiTrader/config/default_config.yaml:693-694, with the block comment "SEC EDGAR is the free, keyless, active whale feed" (AiTrader/config/default_config.yaml:685-686) dated 2026-07-13, exported to the bridge by AiTrader/scripts/start_paper_trading.sh:87. The adapter is fully implemented and live-capable: "EDGAR is keyless and always available -> always attempt live." — AiTrader/whale_signal/adapters.py:285; live fetch at AiTrader/whale_signal/adapters.py:296.
  - The `whale_signal` outputs span 2026-06-30 to 2026-07-26 (AiTrader/DATA_AUDIT.md:20), i.e. thirteen days of them post-date the 2026-07-13 activation.
  - What the code does leave genuinely unknown is **attribution, not measurability**: `except Exception: return self._mock(symbol)` — AiTrader/whale_signal/adapters.py:297-298 — silently degrades a live fetch to mock, and no per-output source is recorded. The honest statement is "the 2,162 outputs are unattributed between EDGAR and mock", which is a one-column fix, not an unmeasurable hypothesis.
  - The deactivation the finding was used to justify: `whale_signal_factor_weight: 0.0    # was 0.10` — AiTrader/config/default_config.yaml:758, on the recorded grounds "The whale layer has never been scored against outcomes at all." (AiTrader/config/default_config.yaml:755-756). That narrower ground stands; the DATA_AUDIT escalation to "fabricated input" and "unmeasurable" does not.
- **Recomputation (if any):** none required — the finding is a code-path check. Writers of `whale_activity` and `whale_signal_history` enumerated by `grep -rn` over `*.cpp`, `*.hpp`, `*.py`, `*.sql` across the snapshot: exactly one writer each, both in `ops/demo.py`, neither reachable from the engine, bridge or paper loop.
- **What would resolve it:** run the whale chain once with `SEC_EDGAR_ENABLED=1` on the five equity symbols in the declared universe and record the per-output source (live vs mock) alongside the confidence, then score those outputs against subsequent closed-trade outcomes. Both steps are free (EDGAR is keyless) and neither touches a Level-1 value. Until then the correct label is "never scored", not "unmeasurable".
- **Confidence:** HIGH — the empty-table inference is contradicted by an explicit code comment and a passing test in the same repository, and the writer enumeration is exhaustive.
- **Invalidated by later commits?:** no — every commit after 2026-07-29 up to the anchor touches only `COLLECTION_LOG.md` and `.gitignore` (`git -C AiTrader show --stat` on 8a49239, f1fb308, b5c2236, 705e0ed), so neither the tables, the adapter, nor the audit text moved.
- **Disclosed by authors?:** no — DATA_AUDIT.md presents the empty tables as its lead finding ("THE FINDING THAT CHANGES A CONCLUSION", AiTrader/DATA_AUDIT.md:13-15) and nowhere records that both tables are unwritten on the live path, even though the project's own `api_server/store.py` and test suite say so.

---

### DRAFT-p1-experiment-2
- **Repository / SHA:** AiTrader / 705e0ed128b7e184be6c1a23dcd06750c524c525
- **Hypothesis or artifact:** the LLM council's price-prediction hypothesis, and the AUDIT.md Task 6 recommendation to close the price-only research programme on it
- **Direction:** A
- **Class:** OVER_CLOSED
- **Severity:** S2
- **Label:** DERIVED
- **Claim challenged (verbatim quote):** "Seven hypothesis families are dead against buy-and-hold-after-costs, the council does not predict price at any size this system could trade, and the honest boundary is drawn: an effect small enough to survive the intervals would clear neither the 50 bp crypto round trip nor the 2,500 USD capacity floor (PROGRESS.md:206, CONTEXT.md:58-60)." — AiTrader/AUDIT.md:154
- **Evidence:**
  - The deciding figure, as AUDIT.md itself states it: "274 scorable calls across 80 symbol clusters, pooled excess -0.5 bp per call, interval [-22.5, +21.4], which excludes the 50 bp effect the design was built to detect" — AiTrader/AUDIT.md:16. n = 274 calls / 80 clusters. Source figures (other reader's documents, flagged): AiTrader/PROGRESS.md:775 and AiTrader/RETURN.md:2437.
  - The capacity requirement the sentence invokes is stated in my own assigned document, twice: "at the sizer, 2,000 USD: 2,500 / (2,520 x 2,000) = **4.96 bp**" and "at the ceiling, 2,500 USD: ... = 3.97 bp" — AiTrader/EXPERIMENT.md:1870-1871; and at the sizing in force when the council session ran, "required net edge = 2,500 / 1,260,000 = **19.8 bp** per trade" — AiTrader/EXPERIMENT.md:1876.
  - The equity round-trip cost the interval would have to survive is not 50 bp. My own assigned document records the current measured figure: "the engine trades tier-1 names whose cost is unchanged at roughly **0.5 to 0.9 bp**" — AiTrader/AUDIT-2026-07-29.md:33.
  - **+21.4 bp exceeds every equity capacity bar named.** Net of the tier-1 round trip the interval's upper end is 20.5 to 20.9 bp, which is 4.1x to 4.2x the enforced 4.96 bp requirement and still 1.04x to 1.06x the superseded 19.8 bp requirement in force on 2026-07-27. The 50 bp crypto clause is correct; the "2,500 USD capacity floor" clause and the universal "at any size this system could trade" are not.
  - **The originating session scoped the claim correctly and the audit dropped the scope.** "Does the evidence now show the council predicts subsequent price movement? **NO, at the scale this session was designed to detect.**" — AiTrader/RETURN.md:2472 (flagged: other reader's document). AUDIT.md Task 6 restates it without the scope clause and uses it to recommend "Continuing to test price-based hypotheses at Level-1 sizing is not worth doing" (AiTrader/AUDIT.md:154).
  - The expansion that would have powered the negative against the bar actually in force was affordable inside the ceiling that session already held: the real spend was 10.87 USD against a hard 120 USD ceiling (AiTrader/RETURN.md, "The spend figure in the run logs is inflated roughly sevenfold; the real number is 10.87 USD", and the ceiling at AiTrader/RETURN.md:2385). 2.5x the clusters is ~27 USD.
- **Recomputation (if any):**
  - Inputs: interval `[-22.5, +21.4]` around point `-0.5`, 80 clusters, 274 calls (AiTrader/AUDIT.md:16); bars 50 bp, 19.8 bp, 4.96 bp, 3.97 bp (AiTrader/EXPERIMENT.md:1870-1871, :1876); tier-1 equity round trip 0.5-0.9 bp (AiTrader/AUDIT-2026-07-29.md:33).
  - Method: half-width / 1.95996 → SE; minimum detectable effect at 80 % power, two-sided α=0.05, as (1.95996+0.8416)·SE; clusters required for each bar as 80·(SE/SE_needed)².
  - Result: half-width 21.950 bp → **SE = 11.20 bp per call** (reproduces the reported z of −0.046 to −0.045). **MDE = 31.4 bp.** 50 bp lies outside the interval and needs only 32 clusters — that claim is sound. 19.8 bp lies **inside** the interval and needs **201 clusters (2.5x)**. 4.96 bp lies inside and needs **3,201 clusters (40x)**. 3.97 bp needs 4,997 clusters (62x). Upper bound net of cost: 21.4 − 0.9 = **20.5 bp = 4.1x the 4.96 bp requirement**.
- **What would resolve it:** either re-word the closure to the scope its own interval supports — "no effect at or above ~31 bp, on 80 clusters" — or run the 2.5x cluster expansion that powers it against the capacity floor in force. Restricting the negative to the crypto leg, where the 50 bp round trip does dominate the interval, would also resolve it.
- **Confidence:** MEDIUM — the arithmetic is unambiguous, but mapping "bp excess per council call" onto "bp net per round trip" assumes one scored call corresponds to one hypothetical round trip over the same window; that is how the design was constructed, and I state it as an assumption rather than a verified equivalence.
- **Invalidated by later commits?:** no — no session commit landed after 2026-07-29 (verified by `git log --stat`), so neither AUDIT.md nor the council figures moved before the anchor.
- **Disclosed by authors?:** partially — the originating session recorded "What this does NOT establish: that no effect of any size exists ... The question is closed for practical purposes and not for arbitrarily small effects" (AiTrader/RETURN.md, findings section, other reader's document), but it too asserts that 22 bp "does not ... clear the 2,500 USD capacity floor at Level 1 sizing", which is the arithmetic error I am raising, and AUDIT.md:154 carries it forward without the scope clause. No document anywhere states that the interval's upper end sits above the capacity requirement.

---

### DRAFT-p1-experiment-3
- **Repository / SHA:** AiTrader / 705e0ed128b7e184be6c1a23dcd06750c524c525
- **Hypothesis or artifact:** AMENDMENT 2's supersession of the 5.00 USD eligibility price floor by 10.00 USD, and its registered reversal condition
- **Direction:** A
- **Class:** OVER_CLOSED
- **Severity:** S2
- **Label:** DERIVED
- **Claim challenged (verbatim quote):** "**What would make 5.00 correct again:** evidence that the effect is concentrated in 5 to 10 USD names strongly enough to outweigh a doubled tick cost. That is measurable once data exists, by scoring the excluded 5-to-10 band separately, and `median_close_at_formation` is recorded so the check stays available." — AiTrader/EXPERIMENT.md:1091-1095
- **Evidence:**
  - The collector rejects every sub-10.00 symbol **before the band is formed and before any query is issued**: `if med_close < spec.MIN_MEDIAN_CLOSE:` / `reject("below_price_floor")` — AiTrader/news_experiment/universe.py:163-164, with `MIN_MEDIAN_CLOSE = 10.00        # AMENDMENT 2, derived from the tick's cost` at AiTrader/news_experiment/spec.py:39. Rejected symbols never reach `members`, so they are never sampled (AiTrader/news_experiment/universe.py:187-196) and never queried.
  - The magnitude at the operative formation: "rejections {'fund': 5387, 'below_price_floor': **3042**, ..." — AiTrader/COLLECTION_LOG.md:30 (formation 2026-07-01). Those 3,042 symbols produce zero rows, and `median_close_at_formation` on every row that does exist is ≥ 10.00 by construction. The excluded 5-to-10 band is therefore not scoreable separately from the collected data; it is scoreable only from a **second collection under a different rule**, which is what "the check stays available" is written to deny.
  - Collection has been running against this rule since 2026-07-29 and has accrued 18 collection days, 10,113 symbol-day rows and 2,320 model calls (summed from AiTrader/COLLECTION_LOG.md:117-277), so the closed reopen path is not hypothetical: a third of the day-cluster floor has already been collected under it.
  - The closure this reopen condition guards is one the document itself flags as costly and non-random: "its removals are **concentrated in exactly the population the hypothesis is about**" — AiTrader/EXPERIMENT.md:98-99; "At 10.00 the removal is 15.8 percent of S4 against 5.2 percent of S1." — AiTrader/EXPERIMENT.md:875-876; "**THE HONEST RESIDUAL:** even at 10.00 the study population is 15.8 percent smaller at the thin end than the mechanism would want ... **If a later reading decides the mechanism matters more than the dispersion, the correct response is to lower the floor and accept the worse hurdle**" — AiTrader/EXPERIMENT.md:885-890. That "later reading" is exactly the reading the recorded data cannot support.
  - The lever the amendment traded the population away for is now recorded as spent: "the price-floor lever is exhausted, since measured bp spread is roughly flat across the band's prices" — AiTrader/EXPERIMENT.md:266-267, and the same at AiTrader/EXPERIMENT.md:2674-2678. So the justification for the floor weakened after the tick measurement while the reversal path stayed closed.
- **Recomputation (if any):** none needed beyond the code path; the claim is falsified by construction. Recorded for scale: 3,042 of the 12,613 symbols enumerated at the 2026-07-01 formation are rejected on the price floor (AiTrader/COLLECTION_LOG.md:30, summing the six rejection buckets plus the 1,558 members), i.e. 24.1 % of the enumerated pool is placed permanently out of reach of the registered check.
- **What would resolve it:** either strike the sentence and record that reversing Amendment 2 requires a new collection under its own pre-registration, or extend the collector to *record* (not score) a control sample of 5-to-10 USD symbols with `state` and `median_close_at_formation` written, which keeps the check literally available at the cost of a few dollars in model calls at the measured $0.000465 per call (AiTrader/EXPERIMENT.md:1224).
- **Confidence:** HIGH — the rejection precedes sampling in the shipped collector and the rejection count is in the collection log.
- **Invalidated by later commits?:** no — `news_experiment/universe.py` and `EXPERIMENT.md` are unchanged after 2026-07-29; the only post-2026-07-29 commits are `COLLECTION_LOG.md` appends and two `.gitignore` lines.
- **Disclosed by authors?:** no — EXPERIMENT.md states the opposite, that the check "stays available", and no amendment, open question or audit entry records that the universe rule forecloses it.

---

### DRAFT-p1-experiment-4
- **Repository / SHA:** AiTrader / 705e0ed128b7e184be6c1a23dcd06750c524c525
- **Hypothesis or artifact:** the `discovery` funnel / watchlist layer, recorded as blocked by a conviction floor
- **Direction:** A
- **Class:** STATISTICAL
- **Severity:** S2
- **Label:** DERIVED
- **Claim challenged (verbatim quote):** "**`discovery` funnel. Do not remove, but stop carrying it as if it works. Confidence medium.** The conviction floor sits above what the pipeline produces, so the watchlist has never gained a member on merit (PROGRESS.md:103). It is dormant with a known blocker, not sound-and-waiting." — AiTrader/AUDIT.md:90
- **Evidence:**
  - The deciding sample, and it is n = 7: "Seven real council verdicts across two days measure 0.5265 to 0.5938. None cleared it." — AiTrader/PROGRESS.md:103 (other reader's document; the conclusion I challenge is in my own AUDIT.md:90 and is restated in my own EXPERIMENT.md).
  - The observed maximum misses the floor by 0.0062, i.e. **1.03 percent of the floor**. The floor is 0.60, and it is not a discovery-derived value: it is the trading gate's council threshold re-used verbatim. `conviction_floor: float = 0.60` — AiTrader/discovery/evaluate.py:72; passed at AiTrader/discovery/evaluate.py:339 as `conviction_floor=council_min_confidence(cfg_path)`; the value is `council_min_confidence: 0.6` at AiTrader/config/default_config.yaml:281.
  - My own assigned document records the mismatch as unresolved, not as evidence: "the discovery layer's separate floor mismatch (0.60 passed as a conviction floor against measured council confidences of 0.53 to 0.59) is **a recorded open flag, not a precedent**" — AiTrader/EXPERIMENT.md:654-655.
  - The variant that would settle it — the floor at any value derived from measured discovery-side conviction rather than inherited from the trading gate — is named nowhere as having been run. `discovery/evaluate.py` carries exactly one floor and one default. The source note itself says the change is free: "Nothing downstream of Stage C can work until this is decided. **No dependencies.**" — AiTrader/PROGRESS.md:103.
  - The funnel's own volume shows the decision matters: Stage A 5,605, Stage B 1,929, **Stage C 394** (AiTrader/DATA_AUDIT.md:191), against only 7 candidates that ever reached a council verdict.
- **Recomputation (if any):**
  - Inputs: k = 0 clears of n = 7 verdicts; observed range 0.5265 to 0.5938; floor 0.60 (all AiTrader/PROGRESS.md:103). Stage-C volume 394 (AiTrader/DATA_AUDIT.md:191).
  - Method: Clopper-Pearson exact 95 % interval on a 0/7 binomial; and, as a second route, a normal fit using the range-based dispersion estimate for n = 7 (d2 = 2.704) with the midrange as location, giving P(verdict ≥ 0.60).
  - Result: **Clopper-Pearson 95 % CI on the pass rate = [0, 0.410].** Range-based σ̂ = 0.0249, midrange 0.5601, z-to-floor 1.60, **implied pass rate 5.5 %**; the probability of observing 0 of 7 at that rate is **0.675**, i.e. entirely unsurprising. At a 5.5 % rate the 394 recorded Stage-C candidates would have yielded about **22 watchlist members**; at the interval's upper bound, 161. The sample cannot distinguish "the floor sits above what the pipeline produces" from "about one verdict in eighteen clears it".
- **What would resolve it:** score a further ~30 Stage-C candidates through the council under the existing 12-calls/day discovery budget (AiTrader/WEEKLOG.md:58) and report the realised distribution of conviction against the 0.60 floor; or state the floor's provenance in AUDIT.md and downgrade "known blocker" to "an inherited threshold missed by 1 percent on seven observations".
- **Confidence:** HIGH — the shortfall, the n and the floor's provenance are all quoted from the record, and the binomial and range-based recomputations agree that 0/7 carries almost no information at this margin.
- **Invalidated by later commits?:** no — `discovery/evaluate.py`, the config value and AUDIT.md are unchanged after 2026-07-29.
- **Disclosed by authors?:** partially — the *mismatch* is disclosed as "a recorded open flag, not a precedent" (AiTrader/EXPERIMENT.md:654-655) and the source note gives the n. What is not disclosed anywhere is that 0 of 7 at a 1.03 percent shortfall does not support a structural blocker, and AUDIT.md:90 states the structural version without the n.

---

### DRAFT-p1-experiment-5
- **Repository / SHA:** AiTrader / 705e0ed128b7e184be6c1a23dcd06750c524c525
- **Hypothesis or artifact:** AMENDMENT 1's supersession of the liquidity-rank universe rule (`U-NEWS-1500-5000-...`) by the absolute ADV band, and the robustness check registered to keep it checkable
- **Direction:** A
- **Class:** OVER_CLOSED
- **Severity:** S3
- **Label:** DERIVED
- **Claim challenged (verbatim quote):** "| `liquidity_rank` | INTEGER | rank at formation. Recorded but NOT the band variable, so the superseded rank rule stays scoreable as a pre-registered robustness check. |" — AiTrader/EXPERIMENT.md:2078 (the same claim is written into the collector: "`liquidity_rank` means what the superseded rank rule meant and that rule / stays scoreable as a pre-registered robustness check (Task 8)." — AiTrader/news_experiment/universe.py:183-184)
- **Evidence:**
  - The rank is indeed computed over the whole eligible pool before the band filter (AiTrader/news_experiment/universe.py:182-185), but the **band filter still removes every out-of-band symbol from `members`** before sampling: `if stratum is None:` / `reject("outside_adv_band")` — AiTrader/news_experiment/universe.py:189-191. Only `members` are sampled and queried (AiTrader/news_experiment/universe.py:192-196 and the stratified draw below it).
  - At the operative formation the collector rejected 2,419 symbols as `outside_adv_band` — AiTrader/COLLECTION_LOG.md:30. None of them will ever carry an observation row.
  - The document's own overlap figures show how much of the rank rule that removes: "rank band members 3,501 ... overlap, % of rank band | 53.4 | 67.2 | **87.3**" and "only 68 ADV-only symbols against **446 rank-only**" — AiTrader/EXPERIMENT.md:941, :947, :957.
  - The missing names are not a random slice: they are precisely the symbols on which rank and absolute ADV disagree, which is the entire content of the comparison the check is registered to make.
  - The same unreachability applies to the reversal condition registered for the amendment itself: "**What would reverse the amendment:** evidence that the effect tracks rank better than ADV. That is measurable once data exists, by scoring the same observations under both memberships" — AiTrader/EXPERIMENT.md:2304-2306. Scoring the same rows under two labels is possible; scoring the *rank rule* is not.
- **Recomputation (if any):**
  - Inputs: rank band 3,501 members; overlap as a percentage of the rank band 53.4 / 67.2 / 87.3 at the 2020 / 2023 / 2026 formations (AiTrader/EXPERIMENT.md:941, :947).
  - Method: rank-band members never queried = 3,501 × (1 − overlap).
  - Result: **2026 formation: 3,056 queriable, 445 never queried (12.7 %)** — consistent with the document's own count of 446 rank-only symbols. 2023: 1,148 never queried (32.8 %). 2020: **1,631 never queried (46.6 %)**. The registered robustness check can therefore examine at most 87.3 % of the superseded rule at the one formation in use, and would be blind to nearly half of it at an earlier formation.
- **What would resolve it:** either restate the field note to what it actually supports ("`liquidity_rank` allows the rank *label* to be tested as an organising variable within the ADV band; the rank rule itself is not scoreable from this collection"), or extend the sample to the rank band's 446 exclusive members at the operative formation, which at the measured 0.359 headlines/symbol/day and $0.000465 per call costs a few dollars.
- **Confidence:** HIGH — the band rejection precedes sampling in the shipped collector, and the shortfall is computed from the document's own overlap table.
- **Invalidated by later commits?:** no — `news_experiment/universe.py` and EXPERIMENT.md are unchanged after 2026-07-29.
- **Disclosed by authors?:** no — the claim is asserted in EXPERIMENT.md Task 8 and repeated as a comment in the collector, and no amendment or open question records the limitation.

---

### DRAFT-p1-experiment-6
- **Repository / SHA:** AiTrader / 705e0ed128b7e184be6c1a23dcd06750c524c525
- **Hypothesis or artifact:** the Stage 1 model-capability comparison (`claude-opus-4-8`, `gemini-3.1-pro-preview`, DeepSeek V4 Flash), and the collection-clearance precondition built on it
- **Direction:** A
- **Class:** PROCESS
- **Severity:** S3
- **Label:** READ
- **Claim challenged (verbatim quote):** "**The experiment is not cleared to collect, because the model comparison is unresolved and the tick multiple is unmeasured, and both are cheap to finish.**" — AiTrader/EXPERIMENT.md:2730-2732
- **Evidence:**
  - Both named blockers on the comparison have expired, on the record's own account. Opus: "**THE OPUS RESULT IS MY BUG, NOT A MODEL FAILURE** ... Every call returned `HTTP 400: temperature is deprecated for this model`. My request sent `temperature: 0`. **Opus 4.8 was never tested.**" — AiTrader/EXPERIMENT.md:2438-2443; the fix is now a recorded hard rule ("That is now a hard rule in CLAUDE.md so a later session does not lose calls to it." — AiTrader/EXPERIMENT.md:2138-2140). Gemini: "**Gemini latched EXHAUSTED after 2 calls** on HTTP 429 with quota language" — AiTrader/EXPERIMENT.md:2445-2446, a balance condition, and the experiment now runs on its own separate Anthropic credential with its own ceiling ("OWN KEY: resolved anthropic_experiment_key ... Independent of the council balance." — AiTrader/COLLECTION_LOG.md:26-27).
  - Of the two clearance conditions, **only the tick multiple was cleared**: "The named blocker, the tick multiple unmeasured, is CLEARED." — AiTrader/EXPERIMENT.md:2688-2689. The remaining block was resolved as a *cost decision* by AMENDMENT 5, and the model comparison is never mentioned again in the unblocking chain. AMENDMENT 7's "START PRECONDITIONS, DOCUMENTED AS THEY ARE" (AiTrader/EXPERIMENT.md:657-682) enumerates five checks and the comparison is not among them.
  - Collection began anyway and has run to the anchor: start anchor 2026-07-29T22:54:53Z (AiTrader/COLLECTION_LOG.md:2), then 18 collected sessions through target 2026-08-21 (AiTrader/COLLECTION_LOG.md:117-277), 10,113 symbol-day rows, 2,320 model calls, $1.2809 spent (summed from the log).
  - No document records the precondition being waived, met, or reconsidered.
- **Recomputation (if any):**
  - Inputs: 21 headlines per arm (AiTrader/EXPERIMENT.md:2425); measured per-call costs haiku $0.000403, gemini $0.000559 (AiTrader/EXPERIMENT.md:2434-2436); Anthropic `claude-opus-4-8` published pricing $5.00/M input, $25.00/M output (AiTrader/RETURN.md:2385) against the document's own 290-input / 35-output token estimate (AiTrader/EXPERIMENT.md:1216-1218).
  - Method: per-call cost × 21 per arm, summed.
  - Result: opus $0.002325/call; **the two missing arms cost $0.061 to run, all three arms $0.069.** The comparison the record calls "cheap to finish" is a seven-cent job that has now stood undone for 27 days while $1.28 of collection ran past it.
- **What would resolve it:** re-run the fixed comparison set on the 21 recorded headlines with the `temperature` field omitted for Opus, report parse rate, directional rate and agreement with a multiple-comparison correction, and either record the precondition as met or amend it away explicitly.
- **Confidence:** HIGH — the precondition, the expiry of both blockers, and the collection start dates are all quoted from my assigned documents, and the cost is derived from the document's own measured rates.
- **Invalidated by later commits?:** no — no session commit landed after 2026-07-29 (`git log --stat` on the four post-anchor commits shows only `COLLECTION_LOG.md` and `.gitignore`).
- **Disclosed by authors?:** yes — AiTrader/EXPERIMENT.md:2721-2724 ("**Does capability matter.** ... **This must be redone before the cheap-tier decision is made.**"), AiTrader/EXPERIMENT.md:2734-2742, and AiTrader/AUDIT-2026-07-29.md:176-179 ("Stage 1's model comparison remains unresolved and the chosen model was never compared to anything. Amendment 3 says so honestly. The thinness is that collection can now start (stage 3 unblocked) with the capability question still open, and nothing in the specification forces it closed."). The finding is therefore READ and capped at S3; what the record does not state is that both causes of the failure have since been removed and that the remaining cost is seven cents.

---

### DRAFT-p1-experiment-7
- **Repository / SHA:** AiTrader / 705e0ed128b7e184be6c1a23dcd06750c524c525
- **Hypothesis or artifact:** the news-drift experiment's registered stop rule, and Open Question 3's obligation to recompute rho and the residual volatility from collected data
- **Direction:** A
- **Class:** STATISTICAL
- **Severity:** S3
- **Label:** DERIVED
- **Claim challenged (verbatim quote):** "60 days x 107.7 = ~6,460 observations, 6.5x the requirement" — AiTrader/EXPERIMENT.md:2348
- **Evidence:**
  - The registered requirement is not 1,000 raw observations; it is 402 independent observations inflated by the day-clustering design effect: "DE = 1 + (k-1) * rho = 1 + 39*0.05 = 2.95 / n_required = 402 * 2.95 = 1,186" — AiTrader/EXPERIMENT.md:1798-1801, with the cluster size assumed at "k = 40 obs/day" (AiTrader/EXPERIMENT.md:1798).
  - Stage 1 superseded that k in the same document: "400 symbols x 0.359 x 0.75 surviving filters = **107.7 scorable/day**" — AiTrader/EXPERIMENT.md:2345-2346. The design effect scales with cluster size, so the requirement moves with it, and the "6.5x" margin is computed against the raw 1,000 rather than against the DE-corrected n.
  - The recomputation obligation is registered and unmet: "**The 180 bp residual volatility and the rho = 0.05 intra-day correlation are assumptions.** Both feed the required sample size. Both are computable from the collected data and both must be recomputed before the stop rule fires." — AiTrader/EXPERIMENT.md:2176-2178; and "The realised `rho` is computed from the collected data and reported, and if it exceeds 0.05 the required n is recomputed and collection continues. The stop rule is 'both thresholds met AND realised power adequate at the realised rho', never '1,000 reached'." — AiTrader/EXPERIMENT.md:1806-1810.
  - Data to do it with exists and has for weeks: 18 collected sessions, 10,113 symbol-day rows and 2,320 model calls between 2026-07-29 and 2026-08-21 (AiTrader/COLLECTION_LOG.md:117-277).
  - **No session has looked at any of it.** Verified against the live repository's git objects (read-only): the last substantive commit is `f819b68` 2026-07-29; every commit to the anchor — `8a49239` 2026-08-04, `f1fb308` 2026-08-06, `b5c2236` 2026-08-18, `705e0ed` 2026-08-24 — changes only `COLLECTION_LOG.md` (and two `.gitignore` lines in the last). `PROGRESS.md` carries no session entry after 2026-07-29 (`grep -n "^### 2026-08" PROGRESS.md` returns nothing).
  - Why this is a Direction-A matter and not bookkeeping: the pre-registered powered-negative definition fires on the pooled interval at the 60-cluster floor (AiTrader/EXPERIMENT.md:1818-1823). Whether that negative deserves the word "powered" depends entirely on the realised rho, and the one margin figure in the document that would reassure a reader is overstated 2.6x.
- **Recomputation (if any):**
  - Inputs: z_α/2 = 2.50, z_β = 0.84, σ = 180 bp, δ = 30 bp, rho = 0.05 (AiTrader/EXPERIMENT.md:1793-1801); k = 40 registered vs k = 107.7 measured (AiTrader/EXPERIMENT.md:1798, :2346).
  - Method: n_independent = (z_α/2 + z_β)²·(σ/δ)²; DE = 1 + (k−1)·rho; n_required = n_independent · DE; margin = 60·107.7 / n_required.
  - Result: n_independent = **402** (reproduces the document). At k = 40, DE = 2.950, n_required = **1,185** (reproduces the document's 1,186). At the measured k = 107.7, DE = **6.335**, n_required = **2,544** — 2.1x the registered figure. 60 clusters × 107.7 = 6,462 observations, so the true margin over the DE-corrected requirement is **2.54x, not 6.5x**. The design does still clear at 400 symbols; it clears by 2.5x, and the document's own suggestion that "the sample could fall to about 150 and still clear" (AiTrader/EXPERIMENT.md:2352-2354) leaves roughly 2.0x, not the headroom "6.5x" implies.
  - Direction of the error: it overstates the design's power, which is the direction that makes a future null easier to label "powered". That is why it belongs to this direction rather than to Direction B alone.
- **What would resolve it:** compute the realised rho and residual dispersion from the 10,113 rows already collected, report them beside the registered 0.05 and 180 bp, and restate the margin against the DE-corrected requirement rather than against the raw 1,000.
- **Confidence:** HIGH — the formula, its inputs and the measured k are all quoted from the same document, and the arithmetic reproduces the document's own intermediate figures exactly.
- **Invalidated by later commits?:** no, and the silence is itself part of the evidence: the four commits between 2026-07-29 and the anchor touch nothing but the collection log. A session after the anchor could of course perform the recompute.
- **Disclosed by authors?:** partially — the obligation to recompute rho is disclosed (AiTrader/EXPERIMENT.md:1806-1810, :2176-2178). The specific arithmetic point, that "6.5x the requirement" is measured against the raw 1,000 rather than against the design-effect requirement the same document derives, is not disclosed anywhere.

---

## What I checked and found sound

- **AMENDMENT 5's refusal to restrict the band to the tier-3 floor** (AiTrader/EXPERIMENT.md:337-356). This is the exact shape my thesis hunts — a thin, expensive stratum cut after a cost measurement — and the document goes the other way for three recorded reasons, keeps S3 and S4 in full, and pre-registers what would reverse the decision. It is anti-closure, and the reasoning ("cost is a function of account size and execution quality, both of which can change, while the existence of a signal cannot") is correct.
- **The pre-registered verdict table** (AiTrader/EXPERIMENT.md:363-375), including the row that writes down the awkward likely outcome before any number exists. I looked for a verdict that pre-commits to killing a hypothesis on a narrow miss and did not find one; the abstention rows are generous rather than harsh.
- **AMENDMENT 6's permutation confirmation** (AiTrader/EXPERIMENT.md:408-545). I checked specifically whether the added conjunctive bar could convert a real effect into a *negative*: it cannot. "The confirmation intercepts positives only. A primary whose interval and z fail on their own terms fails regardless of the null" (AiTrader/EXPERIMENT.md:543-545), and an uninformative null produces an abstention (AiTrader/EXPERIMENT.md:536-540). The stated cost is power and it is named honestly (AiTrader/EXPERIMENT.md:501-509) — though never quantified, which I note without raising as a finding since no closure rests on it yet.
- **The powered-negative definition** (AiTrader/EXPERIMENT.md:1818-1831). It requires the interval's upper bound to sit below the assumed effect *and* no primary to clear, and explicitly records "An interval that includes both zero and 30 bp gross at the cluster floor is an abstention, not a negative and not a finding." That is stricter than the council closure I challenge in DRAFT-p1-experiment-2, and it is the right rule.
- **The tick-multiple blocker, attempts 1 to 4** (AiTrader/EXPERIMENT.md:2398-2694). This is the model case of a blocker being chased until it expired: "unmeasurable without paid quote data" was falsified, then restored on evidence, then genuinely resolved through the historical SIP endpoint. The near-monotone judgment is disclosed as a judgment with the strict flag left false (AiTrader/EXPERIMENT.md:2616-2619), and AUDIT-2026-07-29.md names it as a permissive call (AiTrader/AUDIT-2026-07-29.md:163-169). I have no Direction-A complaint here.
- **AMENDMENT 4's refusal to exclude delay-rolled headlines** (AiTrader/EXPERIMENT.md:211-226) and the five-state absent-input rule (AiTrader/EXPERIMENT.md:1963-1993). Both widen rather than narrow the sample, and the reasoning against excluding near-close headlines ("a non-random slice of the sample and would bias it") is correct.
- **The global-session equity rotation blocker** (AiTrader/LIVE_READINESS.md:14-45). I checked whether the IBKR blocker had expired: it has not. IBKR is still "wired as the live-only venue ... but stays DISABLED" (AiTrader/AUDIT.md:36), the regional whitelists are still empty placeholders (AiTrader/LIVE_READINESS.md:35-38), and the refusal rule is enforced rather than documented. Sound.
- **The `rl_advisory` real-fill gate.** AUDIT.md's lead finding 3 (AiTrader/AUDIT.md:20) is superseded at the anchor: "Real-fill gate counts provenance-confirmed only ... `ml_factor/real_dataset.py` imports `REAL_SOURCES` from `market_data.tradeable` | **supported**" (AiTrader/AUDIT-2026-07-29.md:91). The fix moved the count in the conservative direction, so there is no Direction-A finding here.
- **AUDIT-2026-07-29.md's own lead finding 3** (AiTrader/AUDIT-2026-07-29.md:59-72) was acted on within the same day by AMENDMENT 6. Audit-to-amendment latency of hours is the opposite of premature closure.
- **The adaptive react layer's graduation ladder** (AiTrader/LIVE_READINESS.md:99-150). The first rung's stated prerequisites — a working Finnhub key and a working Anthropic key — are now demonstrated at scale by the collector (AiTrader/COLLECTION_LOG.md:26, :117-277), so the trigger is arguably met and the observe-only rung costs about $0.40/day and moves no position (AiTrader/LIVE_READINESS.md:124-126). I record this as a met reopen condition in the ledger rather than as a finding, because no document labels the adaptive layer closed — it is off, not closed, and "off" is a defensible state for an unmeasured layer.
- **AUDIT.md's line citations into PROGRESS.md and CONTEXT.md are stale** at the anchor (e.g. AiTrader/AUDIT.md:16 cites PROGRESS.md:193 for the council result, which now sits at PROGRESS.md:775). This is hygiene, it is a natural consequence of an append-only tracking file, and I did not raise it as a finding.
- **Checked and found nothing:** the fee model's two-language agreement (AiTrader/AUDIT-2026-07-29.md:99-126), the eighth-fabrication sweep and its three latent candidates (AiTrader/AUDIT-2026-07-29.md:128-159, all three closed the same day per AiTrader/PROGRESS.md), the `no_news` / `source_failed` separation (AiTrader/EXPERIMENT.md:2011-2015), the strength field's "recorded, never gated" rule (AiTrader/EXPERIMENT.md:1363-1378), and the WEEKLOG pre-flight success criteria (AiTrader/WEEKLOG.md:61-71), whose paragraph 2 explicitly forbids reading a low trade count as a verdict on either of two opposing changes — the anti-premature-closure discipline working.

## Live-repo access log

Purpose of access: git history only (`git status --porcelain`, `git log`, `git show --stat`). No file in the
live repository was opened for writing, and no untracked data file was read.

Before (`git -C /home/kiros-li/Documents/GitHub/AiTrader status --porcelain`):

```
 M COLLECTION_LOG.md
```

After (same command, after the last live-repo command):

```
 M COLLECTION_LOG.md
```

Both outputs match the documented pre-existing dirt for this repository (a collector appends to
`COLLECTION_LOG.md`). No other entry appeared. Nothing was modified by me.
