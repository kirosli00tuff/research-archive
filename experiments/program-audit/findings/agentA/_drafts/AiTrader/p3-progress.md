# AiTrader — Agent A draft findings, part "p3-progress"

Repository: AiTrader, anchored SHA `705e0ed128b7e184be6c1a23dcd06750c524c525` (main, 2026-08-24).
Documents read completely: `PROGRESS.md` (1,787 lines), `CONTEXT.md` (392 lines), `COLLECTION_LOG.md`
(277 lines), `news_experiment/collect.py` (entry points and preconditions), `research_satellite/`,
`README.md` (grep + targeted reads). Snapshot root
`/home/kiros-li/.cache/program-audit/scratchpad/snap/AiTrader/`.

Recomputation script: `/home/kiros-li/.cache/program-audit/scratchpad/work/agentA-aitrader-p3/recompute.py`
(run under `/home/kiros-li/.cache/program-audit/scratchpad/venv/bin/python`).

**The single structural fact behind findings 1-3.** On 2026-07-27 at 21:25 -07:00 (commit
`82e8e72`, PROGRESS.md:491-531) the project re-derived Level 1 sizing: `default_risk_per_trade_pct`
0.005 -> 0.02 and the per-position notional range 100-500 USD -> 400-2,000 USD (PROGRESS.md:503,
:191, replay-verified 4x at :522). The **capacity floor itself did not move** (2,500 USD/yr), so the
net-edge a hypothesis must clear divided by exactly 4. Amendment 7 applied that correction inside the
news experiment (4.96 bp, PROGRESS.md:189). It was **not** applied to the research capacity gate or
to the two hypothesis closures that leaned on it, and the 2026-07-29 stale-figure sweep concluded
"No other figure was found overtaken by this week's measurements" (PROGRESS.md:211).

---

### DRAFT-p3-progress-1
- **Repository / SHA:** AiTrader / 705e0ed128b7e184be6c1a23dcd06750c524c525
- **Hypothesis or artifact:** The permanent research capacity gate ("AN EDGE BELOW THE CAPACITY FLOOR IS NOT WORTH OPERATING REGARDLESS OF SIGNIFICANCE"), the standing pre-computation filter every research round is required to pass
- **Direction:** A
- **Class:** STALE_FIGURE
- **Severity:** S2
- **Label:** DERIVED
- **Claim challenged (verbatim quote):** "The floor is 2,500 USD per year at 100,000 equity, 2.5 percent, covering execution risk, infrastructure failure, and operator time. At Level 1 sizing (about 500 USD notional per trade) that requires roughly a 20 bp net edge at 10 trades per day, and the crypto gross hurdle behind such a net is 70 bp. A future hypothesis must state before testing how it clears this floor at permitted sizing." — AiTrader/CONTEXT.md:108
- **Evidence:**
  - The same gate is stated in the session that created it: "Capacity table at Level 1 sizing (500 USD notional): a 10 bp net edge at 10 trades per day is 1,260 USD per year. CAPACITY FLOOR set as a permanent research gate: 2,500 USD per year (2.5 percent of equity), requiring roughly 20 bp net at 10 trades per day at Level 1 sizing, with the crypto gross hurdle at 70 bp behind it." — AiTrader/PROGRESS.md:854 (2026-07-26).
  - Level 1 sizing was re-derived the next day: `default_risk_per_trade_pct` "0.005 | **0.02**" with derivation "capacity floor 2,500 USD/yr at an honest 10 bp edge needs 992 to 1,984 USD per position" — AiTrader/PROGRESS.md:503 (session commit `82e8e72`, 2026-07-27T21:25:16-07:00, `git -C <live> log -- PROGRESS.md`, read 2026-09-05).
  - The enforced per-position range: "the sizer row 0.005 marked SUPERSEDED against enforced 0.02, position range \"100 to 500 USD\" to 400 to 2,000" — AiTrader/PROGRESS.md:191.
  - The repository's own recomputation of this exact quantity under the enforced sizing: "The 4.96 bp E-test comparison figure at the 2,000 USD sizer is CONFIRMED EXACT (2,500 / (2,520 x 2,000)) and does not move. At the enforced 2,500 USD ceiling the requirement is 3.97 bp. Annual at the sizer: 5.04M USD entered" — AiTrader/PROGRESS.md:189 (Amendment 7, 2026-07-29). Reaffirmed at AiTrader/PROGRESS.md:256 ("its 4.96 bp arithmetic still means exactly that") and used as the live bar at AiTrader/PROGRESS.md:272 ("both clearing the 4.96 bp capacity requirement at the 2,000 USD sizer").
  - The 2026-07-29 stale-figure sweep that should have caught it explicitly bracket-noted CONTEXT.md's *scope* decision (CONTEXT.md:84) and then concluded: "No other figure was found overtaken by this week's measurements." — AiTrader/PROGRESS.md:211. CONTEXT.md:108 and PROGRESS.md:854 were not touched.
  - Second leg also stale: "the crypto gross hurdle behind such a net is 70 bp" governs a system whose scope was narrowed to US equities on 2026-07-27 (AiTrader/PROGRESS.md:576; AiTrader/CONTEXT.md:84), where the traded tier costs "roughly 0.5 to 0.9 bp" (AiTrader/CONTEXT.md:84, bracketed correction; AiTrader/PROGRESS.md:211).
- **Recomputation (if any):**
  - Inputs: floor 2,500 USD/yr (CONTEXT.md:108); 10 trades/day x 252 = 2,520 entries/yr (PROGRESS.md:189, :511); per-position notional 500 USD old convention (CONTEXT.md:108, PROGRESS.md:854) and 2,000 USD enforced convention (PROGRESS.md:189, :191).
  - Method: required net edge = floor / (entries_per_year x notional).
  - Result: old 2,500/(2,520 x 500) = **19.84 bp** (the document's "roughly 20 bp"); enforced 2,500/(2,520 x 2,000) = **4.96 bp**; at the enforced 0.025 ceiling 2,500/(2,520 x 2,500) = **3.97 bp**. The gate as written is **4.0x stricter** than the same arithmetic on the enforced sizing. The 4x multiplier is convention-independent: the notional range moved 100->400 at the low end and 500->2,000 at the high end (PROGRESS.md:191), and the replay measured "notional per position | 100.00 | **400.00** (exactly 4x)" (PROGRESS.md:522). Honest caveat: if the LOW end of the enforced range (400 USD) is compared against the OLD convention's HIGH end (500 USD), the requirement rises to 24.80 bp — but that mixes conventions, and Amendment 7 fixes the convention at 2,000 USD.
- **What would resolve it:** Amend CONTEXT.md:108 and PROGRESS.md:854 to the enforced sizing (4.96 bp at the 2,000 USD sizer, 3.97 bp at the ceiling) and to the US-equity cost hurdle, exactly as Amendment 7 did for the news experiment; or state explicitly that the research gate deliberately keeps the superseded 500 USD convention and why.
- **Confidence:** HIGH — both the stale figure and its corrected replacement are stated verbatim in this repository, three days apart, and the arithmetic is one division.
- **Invalidated by later commits?:** no — the four commits after 2026-07-29 up to the anchor touch only `COLLECTION_LOG.md` and `.gitignore` (`git -C <live> log 705e0ed --since=2026-07-30`, read 2026-09-05).
- **Disclosed by authors?:** no — PROGRESS.md:211 performed a sweep for exactly this class of staleness and concluded no other figure was overtaken.

---

### DRAFT-p3-progress-2
- **Repository / SHA:** AiTrader / 705e0ed128b7e184be6c1a23dcd06750c524c525
- **Hypothesis or artifact:** The price-only hypothesis programme against `analysis_bars.db` (the 8-symbol intraday database) — closed 2026-07-26 as exhausted, together with the twelve candidates rejected on capacity arithmetic before any code ran
- **Direction:** A
- **Class:** OVER_CLOSED
- **Severity:** S1
- **Label:** DERIVED
- **Claim challenged (verbatim quote):** "Recorded implication: further price-only hypothesis rounds against this 8-symbol database at Level 1 sizing are not worth running, and the calculus changes only with a new information axis, maker execution (rescues nothing here), or a sizing change that is not on the table." — AiTrader/PROGRESS.md:849
- **Evidence:**
  - The registered reopen condition is "a sizing change", and a sizing change was applied the following day: sizer 0.005 -> 0.02, `max_open_positions_total` 5 -> 10, `max_open_positions_per_venue` 2 -> 10, `max_total_open_risk_pct` 0.03 -> 0.25 — AiTrader/PROGRESS.md:503-507, commit `82e8e72` 2026-07-27T21:25:16-07:00 (`git -C <live> log --date=iso-strict -- PROGRESS.md`, read 2026-09-05).
  - The twelve rejections and their capacity figures, all "at Level 1 sizing" and all compared against the unchanged 2,500 USD/yr floor: "12 of 14 candidates rejected before any code, on arithmetic (SEC EDGAR 13F following at 600 USD per year, turn-of-month at 480, FOMC drift at 392, crypto-to-equity spillover at 1,200, equity-to-crypto spillover net-negative against the 50 bp fee, intraday first-half-hour at 1,764, equity cross-section at 500 to 1,000 and NVDA-poisoned, crypto weekend net-negative, monthly crypto cross-section eaten by taker fees)" — AiTrader/PROGRESS.md:849.
  - Enforced per-position notional range after the change: "position range \"100 to 500 USD\" to 400 to 2,000" — AiTrader/PROGRESS.md:191; replay-verified "notional per position | 100.00 | **400.00** (exactly 4x)" — AiTrader/PROGRESS.md:522.
  - The floor itself did not move: "Accurate and untouched: trades 10/day, the 2,500 USD/year floor." — AiTrader/PROGRESS.md:191.
  - No later entry revisits the closure. The last research round in the log is 2026-07-27 (AiTrader/PROGRESS.md:771); every session after the sizing change (PROGRESS.md:141-473) is news-experiment or hygiene work, and the four commits between 2026-07-30 and the anchor touch only `COLLECTION_LOG.md` and `.gitignore`.
  - The crypto-leg objections in the same list ("net-negative against the 50 bp fee", "eaten by taker fees") were also overtaken on 2026-07-27, when scope narrowed to US equities and the traded tier's measured round trip became 0.5-0.9 bp — AiTrader/PROGRESS.md:576, AiTrader/CONTEXT.md:84, AiTrader/PROGRESS.md:211.
- **Recomputation (if any):**
  - Inputs: capacity USD/yr figures at AiTrader/PROGRESS.md:849; floor 2,500 USD/yr at AiTrader/PROGRESS.md:854 and CONTEXT.md:108; notional multiplier 4x from AiTrader/PROGRESS.md:191 and :522.
  - Method: capacity is linear in per-position notional at fixed edge and fixed trade rate, so each rejected candidate's USD/yr figure scales by the notional multiplier. Multiply by 4 and compare against the unchanged 2,500 USD/yr floor.
  - Result: intraday first-half-hour 1,764 -> **7,056 USD/yr (2.82x the floor)**; crypto-to-equity spillover 1,200 -> **4,800 (1.92x)**; equity cross-section upper bound 1,000 -> **4,000 (1.60x)**. Below the floor still: SEC EDGAR 13F 600 -> 2,400 (0.96x), turn-of-month 480 -> 1,920, FOMC drift 392 -> 1,568, equity cross-section lower bound 500 -> 2,000. So **at least two, arguably three, of the twelve pre-code rejections invert at the sizing enforced one day later**, and the two that invert most are the two testable on the equity side of this database.
  - Cross-check on the same page: the cross-sectional round's holdout capacities also scale — H-F 17,634 -> 70,536, H-G 2,044 -> 8,176, H-I 1,477 -> 5,908 USD/yr (AiTrader/PROGRESS.md:827) — though those three failed on significance, not capacity, so they are not reopened by this arithmetic (see "What I checked and found sound").
- **What would resolve it:** Re-run the capacity gate on the twelve rejected candidates at the enforced sizing and either record that the two or three survivors are now worth a pre-registered round, or record a reason (other than capacity) for keeping them closed. Alternatively, amend PROGRESS.md:849 to state that the reopen condition fired and the closure is being retained on a different ground.
- **Confidence:** HIGH — the reopen trigger is registered in the closure's own sentence, the trigger fired 27 hours later in the same repository, the multiplier is measured by the project's own replay, and capacity is linear in notional.
- **Invalidated by later commits?:** no — no commit after 2026-07-29 touches PROGRESS.md, CONTEXT.md or any research artifact up to the anchor.
- **Disclosed by authors?:** no — the reopen condition is registered at AiTrader/PROGRESS.md:849, but the session that changed sizing (AiTrader/PROGRESS.md:491-532) does not mention the research capacity gate or the closed hypothesis families, and no later entry revisits them.

---

### DRAFT-p3-progress-3
- **Repository / SHA:** AiTrader / 705e0ed128b7e184be6c1a23dcd06750c524c525
- **Hypothesis or artifact:** "the council predicts price" — closed 2026-07-27 by the wide council run (274 scorable directional calls, 80 symbol clusters)
- **Direction:** A
- **Class:** OVER_CLOSED
- **Severity:** S2
- **Label:** DERIVED
- **Claim challenged (verbatim quote):** "**WHAT IS AND IS NOT CLOSED.** The interval admits roughly plus or minus 22 bp, and 22 bp survives neither the 50 bp crypto round trip nor the 2,500 USD capacity floor at Level 1 sizing. So the question is closed for anything this system could trade, and open only for effects too small to matter." — AiTrader/PROGRESS.md:788
- **Evidence:**
  - The deciding figures of the run: "274 scorable directional calls across 80 symbol clusters... Pooled excess over the unconditional move is -0.5 bp per call at z equals -0.046, interval [-22.5, +21.4], hit rate 50.0 percent to one decimal place. The interval EXCLUDES the 50 bp effect the design was powered to detect." — AiTrader/PROGRESS.md:775 (n = 274 calls / 80 clusters).
  - The same closure repeated in the sibling session: "an effect that small would clear neither the fee model nor the capacity floor" — AiTrader/PROGRESS.md:755.
  - Leg 1 (50 bp crypto round trip) was superseded the same day: scope narrowed to US equities at the universe layer (AiTrader/PROGRESS.md:576; AiTrader/CONTEXT.md:84), and the traded tier's measured round trip is "roughly 0.5 to 0.9 bp" (AiTrader/CONTEXT.md:84 bracketed correction 2026-07-29; AiTrader/PROGRESS.md:211, :235). Commit ordering: council run `959a295` 2026-07-27T12:41:21-07:00; scope narrowing `8fd9fbf` 2026-07-27T18:55:32-07:00 (`git -C <live> log --date=iso-strict -- PROGRESS.md`, read 2026-09-05).
  - Leg 2 (the capacity floor "at Level 1 sizing") was superseded 8h44m later the same day by commit `82e8e72` (AiTrader/PROGRESS.md:503, :191) and recomputed by this repository at 4.96 bp (AiTrader/PROGRESS.md:189, :256, :272).
  - The closure is the operative one for the layer's future: "**No measured justification remains on this evidence.**" — AiTrader/PROGRESS.md:755. No later entry revisits it.
- **Recomputation (if any):**
  - Inputs: interval upper bound +21.4 bp and point -0.5 bp at z -0.046 (AiTrader/PROGRESS.md:775); tier-1 equity round trip 0.5-0.9 bp (AiTrader/CONTEXT.md:84, AiTrader/PROGRESS.md:211); enforced capacity requirement 4.96 bp = 2,500/(2,520 x 2,000) (AiTrader/PROGRESS.md:189).
  - Method: (a) recover SE from point/z and confirm the reported interval; (b) subtract the equity cost hurdle from the interval's upper bound and compare against the enforced requirement and against the 2,500 USD/yr floor; (c) compute the run's minimum detectable effect at 80% power.
  - Result: SE = |-0.5 / -0.046| = **10.87 bp**; normal-theory 95% CI = [-21.8, +20.8] bp, matching the reported [-22.5, +21.4]. Upper bound net of tier-1 equity cost = 21.4 - 0.5 = **20.90 bp** (or 20.50 bp at 0.9 bp cost), i.e. **4.2x the enforced 4.96 bp requirement**, not "too small to matter". In dollars at the enforced sizer: (21.4-0.7)/1e4 x 2,520 x 2,000 = **10,433 USD/yr against a 2,500 USD/yr floor (4.17x)**. Minimum detectable effect of the run at 80% power, two-sided 0.05 = 2.802 x 10.87 = **30.5 bp**, so the design cannot exclude anything between the 4.96 bp requirement and ~30 bp — a range that is now entirely economically material rather than "too small to matter".
  - Cost of narrowing it, using the round's own rule that power scales on clusters not calls (AiTrader/PROGRESS.md:803): to make 10 bp the MDE needs 9.3x clusters = ~742 clusters, ~2,542 calls, ~101 USD at the run's realised 0.0397 USD/call (10.87 USD / 274 calls, AiTrader/PROGRESS.md:773, :775) — inside the run's own **120 USD hard ceiling of which 10.87 USD was spent** (AiTrader/PROGRESS.md:773).
- **What would resolve it:** Restate the closure's boundary against the enforced sizing and the US-equity cost hurdle (the honest form is "the point estimate is null and the interval excludes 50 bp; effects between ~5 and ~30 bp remain untested and are now economically material"), or run the cluster extension the same session's own scaling rule prices at roughly 100 USD.
- **Confidence:** MEDIUM — the point estimate is genuinely null and the pre-registered floor was met, so the *negative* stands; what is over-stated is the boundary clause, and that clause rests on two figures this repository superseded within hours and never revisited.
- **Invalidated by later commits?:** no — no commit after 2026-07-29 touches the research documents, and the council layer's weights remain as set (AiTrader/CONTEXT.md:90).
- **Disclosed by authors?:** no for the capacity/cost legs — AiTrader/PROGRESS.md:211's stale-figure sweep declares no other figure overtaken. Partially disclosed for sample limits: AiTrader/PROGRESS.md:755 states "80 clusters, two days, one regime, GPT-5.5 absent from the whole equity half, so a small effect is not excluded" — but the same sentence dismisses such an effect on the superseded capacity arithmetic.

---

### DRAFT-p3-progress-4
- **Repository / SHA:** AiTrader / 705e0ed128b7e184be6c1a23dcd06750c524c525
- **Hypothesis or artifact:** The news-drift experiment's start blocker — "the tick multiple is unmeasured" and "stage 3 stays blocked" — still stated in CONTEXT.md and still printed by the collector, 26 days after the blocker was lifted and while collection has been running daily
- **Direction:** A
- **Class:** STALE_FIGURE
- **Severity:** S3
- **Label:** DERIVED
- **Claim challenged (verbatim quote):** "It also refuses to start collecting**: `--run-kind collection` needs an explicit `--i-have-read-the-preconditions`, since the tick multiple is still unmeasured and its result may amend the cost model or the band." — AiTrader/CONTEXT.md:60
- **Evidence:**
  - Second stale blocker in the same document: "Consequence reported, not applied: the accepted news-drift specification survives at the median only in its liquid half (S1/S2), and stage 3 stays blocked on that operator decision." — AiTrader/CONTEXT.md:54.
  - The tick multiple was measured on 2026-07-29: "tier 3 = 8.0 and tier 4 = 9.0, MEASURED" over "1,402 rows kept of 1,440 cells over 157 symbols" across three sessions — AiTrader/PROGRESS.md:266, :270 (n = 1,402 symbol-session-window rows, 157 symbols).
  - Stage 3 was unblocked the same day: "**STAGE 3 IS NOW UNBLOCKED.** The tick multiple is measured, the amendment decision the measurement forced is made and recorded, and the specification no longer pre-condemns half its sample." — AiTrader/PROGRESS.md:258 (Amendment 5); reaffirmed "**STAGE 3 REMAINS UNBLOCKED.**" — AiTrader/PROGRESS.md:229, and "**Stage 3 remains unblocked.** Collection still waits only on the operator's start command" — AiTrader/PROGRESS.md:197.
  - The collector still carries the expired reason in two places at the anchored SHA: module docstring "`--run-kind collection` is refused unless `--i-have-read-the-preconditions` is also passed, because the tick multiple is still unmeasured and its result may amend the cost model or the band" — AiTrader/news_experiment/collect.py:7-9; and the runtime refusal "REFUSING: collection has not been cleared to start. The tick multiple is unmeasured and its result may amend the cost model or the band (EXPERIMENT.md, Stage 1 verdict)." — AiTrader/news_experiment/collect.py:731-735.
  - Collection has in fact been running since 2026-07-29 and is running at the anchor: start anchor "start_utc: 2026-07-29T22:54:53Z" (AiTrader/COLLECTION_LOG.md:2), then 19 `action: collected` daily runs from "=== DAILY RUN 2026-07-30T22:30:45Z ===" (AiTrader/COLLECTION_LOG.md:117) to "=== DAILY RUN 2026-08-24T22:31:49Z ===" (AiTrader/COLLECTION_LOG.md:270), the last writing 433 rows for target session 2026-08-21 (AiTrader/COLLECTION_LOG.md:275). First collection wrote 427 rows over a 1,558-member band (AiTrader/COLLECTION_LOG.md:33, :36).
  - Meanwhile the status documents were never updated: `PROGRESS.md` "Current State" (AiTrader/PROGRESS.md:7) and its Session Log both stop at 2026-07-29, and every entry in the last week states "Collection has not started" / "NO COLLECTION DATA EXISTED" (AiTrader/PROGRESS.md:187, :217, :248, :276, :289). The four commits between 2026-07-30 and the anchor touch only `COLLECTION_LOG.md` and `.gitignore` (`git -C <live> log 705e0ed --since=2026-07-30`, read 2026-09-05).
- **Recomputation (if any):** none required — this is a document-versus-record comparison. Counted 19 `action: collected` blocks in AiTrader/COLLECTION_LOG.md between lines 117 and 277 (read from the anchored snapshot; the live file has one further uncommitted modification, the documented collector append, not read for content).
- **What would resolve it:** Update CONTEXT.md:54 and :60 to record that the tick multiple was measured on 2026-07-29 and that stage 3 unblocked; rewrite the collector's refusal message to the current reason (an operator attestation), which PROGRESS.md:195 already recommends; and refresh PROGRESS.md "Current State" to reflect ~19 collected sessions.
- **Confidence:** HIGH — the measurement, the unblocking, the still-stale text and the running collection are each stated verbatim in files at the anchored SHA.
- **Invalidated by later commits?:** no — the only post-anchor motion is the collector appending to COLLECTION_LOG.md, which strengthens rather than weakens the finding.
- **Disclosed by authors?:** partially — AiTrader/PROGRESS.md:195 discloses the collector's stale message ("its refusal message still cites the tick multiple as unmeasured, stale since the 2026-07-29 measurement, reported not changed"). The two stale blockers in CONTEXT.md and the four-week gap between the running collection and the status documents are not disclosed anywhere.

---

### DRAFT-p3-progress-5
- **Repository / SHA:** AiTrader / 705e0ed128b7e184be6c1a23dcd06750c524c525
- **Hypothesis or artifact:** Stage 1 Task 6, the model-capability comparison for the news-drift scorer — closed with three of four registered arms never actually run, and named as one of the two conditions for clearing collection
- **Direction:** A
- **Class:** OVER_CLOSED
- **Severity:** S3
- **Label:** READ
- **Claim challenged (verbatim quote):** "**VERDICT: no stop condition fired.** ... **The experiment is NOT cleared to collect**, because the model comparison is unresolved and the tick multiple unmeasured. Both are cheap to finish: one RTH-timed script and one corrected comparison." — AiTrader/PROGRESS.md:401
- **Evidence:**
  - Three of the four arms produced no usable data: "**DeepSeek V4 Flash, the candidate the whole specification names, has NO CREDENTIAL and could not be tested.** haiku: 21 of 21 parsed, 52.4 percent directional, $0.000403 per call. **opus: 100 percent \"parse fail\" was MY BUG, not the model** — every call returned `HTTP 400: temperature is deprecated for this model`, so Opus was never tested. ... gemini latched EXHAUSTED on HTTP 429 after 2 calls" — AiTrader/PROGRESS.md:400. Deciding n: Haiku n = 21 calls; Opus n = 0 scorable; Gemini n = 2 then latched; DeepSeek n = 0.
  - The Opus blocker was self-inflicted and fixed the next session: "`claude-opus-4-8` rejects `temperature` with `HTTP 400 invalid_request_error` ... That is why Stage 1's Opus column read 100 percent parse-fail: the model was never reached." — AiTrader/PROGRESS.md:384, recorded in CLAUDE.md the same day.
  - The Gemini blocker is an account-funding latch, not a capability result: AiTrader/PROGRESS.md:400, and the exhaustion mechanism at AiTrader/PROGRESS.md:766 ("Process state, not persisted: an account stays dry until funded").
  - The experiment subsequently obtained its own separately-funded credential, which removes the shared-quota coupling for the Anthropic arms: "A separate credential, `anthropic_experiment_key` / `EXPERIMENT_ANTHROPIC_API_KEY` ... Only a separate KEY gives a separate BALANCE" — AiTrader/CONTEXT.md:62; confirmed live in the run log "[credential] OWN KEY: resolved anthropic_experiment_key ... Independent of the council balance." — AiTrader/COLLECTION_LOG.md:28.
  - Only one of the two clearance conditions was ever met. The unblocking records cite the tick multiple alone: "**STAGE 3 IS NOW UNBLOCKED.** The tick multiple is measured, the amendment decision the measurement forced is made and recorded" — AiTrader/PROGRESS.md:258; "Collection still waits only on the operator's start command with the attestation flag." — AiTrader/PROGRESS.md:197. The model comparison is not mentioned in either, and was never re-run.
  - Collection then ran on the single untested arm for 19 sessions (AiTrader/COLLECTION_LOG.md:117-277), spending against the experiment's own ceiling per run (e.g. "spend: 0.108320 USD over 197 calls" — AiTrader/COLLECTION_LOG.md:123).
  - The cost of the omitted arm is trivial by the project's own figures: the whole Stage 1 measurement cost "Total spend 0.0096 USD" (AiTrader/PROGRESS.md:389) and Haiku's per-call cost is $0.000403 (AiTrader/PROGRESS.md:400), so a 21-call repeat on the two reachable arms is well under one cent.
- **Recomputation (if any):** none beyond the per-call arithmetic above; 21 calls x $0.000403 = $0.0085 per arm, so re-running the two blocked-but-reachable arms costs under two cents against a Stage 1 ceiling of 15.00 USD (AiTrader/PROGRESS.md:389).
- **What would resolve it:** Either run the corrected comparison (Opus with `temperature` omitted, Gemini on a funded key) on the same 21 headlines and record the result, or formally withdraw the model comparison as a clearance condition with a stated reason, so that "the experiment is NOT cleared to collect" is not silently satisfied by meeting one of its two named conditions.
- **Confidence:** MEDIUM — the omission is real and the arithmetic trivial, but the authors argue defensibly that Haiku is chosen on reachability and approval rather than on a capability claim, and no result is claimed for the untested arms.
- **Invalidated by later commits?:** no — no commit after 2026-07-29 touches the experiment code or the specification up to the anchor.
- **Disclosed by authors?:** yes (AiTrader/PROGRESS.md:243 "The model-capability question is still open while stage 3 is unblocked, and nothing forces it closed"; AiTrader/PROGRESS.md:359 "**NO CLAIM IS MADE THAT HAIKU IS BETTER.** Stage 1 produced one usable arm out of four, so the capability question stays open and is recorded as open."). The undisclosed part is that PROGRESS.md:401's *two-condition* clearance test was satisfied on one condition, and that collection then ran for four weeks on the untested arm.

---

### DRAFT-p3-progress-6
- **Repository / SHA:** AiTrader / 705e0ed128b7e184be6c1a23dcd06750c524c525
- **Hypothesis or artifact:** The discovery layer's Stage C output gate — blocked since 2026-07-18 by a threshold borrowed from a different gate, with the fix named, costless, dependency-free, and still unapplied at the anchor 37 days later
- **Direction:** A
- **Class:** OVER_CLOSED
- **Severity:** S3
- **Label:** READ
- **Claim challenged (verbatim quote):** "**The discovery conviction floor sits above what the pipeline produces, and it blocks the whole layer.** `discovery/evaluate.py` passes `council_min_confidence` (0.60, the TRADING gate's threshold) as `conviction_floor`. Seven real council verdicts across two days measure 0.5265 to 0.5938. None cleared it. Every verdict is therefore `avoid`, `run.py` skips `avoid` when building the watchlist, and the watchlist has never gained a member. Nothing downstream of Stage C can work until this is decided. No dependencies." — AiTrader/PROGRESS.md:103
- **Evidence:**
  - Deciding figure and n: seven real council verdicts spanning 0.5265-0.5938 against a 0.60 floor (n = 7 verdicts across two days) — AiTrader/PROGRESS.md:103.
  - The flag was recorded as reported-not-fixed on 2026-07-18 ("Found 2026-07-18 by the discovery diagnostic session (OPUS pass). Reported, deliberately NOT fixed (that session was diagnosis only). Ordered by severity and dependency:" — AiTrader/PROGRESS.md:101) and, unlike five sibling flags in the same block, was never struck through or annotated CLEARED (compare AiTrader/PROGRESS.md:105, :106, :107, :108).
  - The code still carries the borrowed constant at the anchored SHA: `conviction_floor: float = 0.60` (AiTrader/discovery/evaluate.py:72), wired as `conviction_floor=council_min_confidence(cfg_path)` (AiTrader/discovery/evaluate.py:339), against `council_min_confidence: 0.6` (AiTrader/config/default_config.yaml:281).
  - Independent corroboration that the floor is unreachable by the pipeline, from a different session and a much larger sample: "No council verdict in the record reaches conviction 0.65, which is the 0.60 discovery floor problem seen from the other side." — AiTrader/PROGRESS.md:800 (75 evaluations); and the wide run's 274 calls produced no entry contradicting it.
  - The blocked capability is not small: the discovery funnel plus dynamic watchlist plus the long-term sleeve all sit downstream (AiTrader/PROGRESS.md:25), and "the watchlist has never gained a member" (AiTrader/PROGRESS.md:103) means every downstream surface has been dead for the whole period.
  - Second, dependent flag also unresolved: "**The synthetic DNN champion is the deciding vote against every discovery candidate.** `dnn_bias` measured -0.31 to -0.34 on all 12 symbols ever evaluated and never once positive." — AiTrader/PROGRESS.md:104 (n = 12 symbols). Its stated precondition ("Settle the floor first or this only moves the failure") has never been met.
- **Recomputation (if any):** none — the gap is arithmetic on stated figures: the highest observed conviction 0.5938 falls 0.0062 short of the 0.60 floor, i.e. the layer is blocked by roughly one part in a hundred of a threshold the same document says was never chosen for it.
- **What would resolve it:** Decide the discovery conviction floor as its own number (the flag says "No dependencies"), or record explicitly that the discovery layer is retired rather than blocked. Either is a one-line change plus a test; neither has happened in 37 days.
- **Confidence:** MEDIUM — the blocker and its cause are stated by the authors; what I add is that it is still live in code at the anchor and that a second, larger sample confirms the floor is structurally unreachable.
- **Invalidated by later commits?:** no — `discovery/evaluate.py` is unchanged at the anchored SHA and no commit after 2026-07-29 touches it.
- **Disclosed by authors?:** yes (AiTrader/PROGRESS.md:103, recorded as an open flag on 2026-07-18 and left open). Presented here only as an un-actioned reopen candidate for the cross-repository pass, not as a discovery.

---

### DRAFT-p3-progress-7
- **Repository / SHA:** AiTrader / 705e0ed128b7e184be6c1a23dcd06750c524c525
- **Hypothesis or artifact:** Two entries in PROGRESS.md "Known Issues and Caveats" / "Open Flags" that describe limits lifted on 2026-07-27 and were never struck through
- **Direction:** A
- **Class:** STALE_FIGURE
- **Severity:** S4
- **Label:** READ
- **Claim challenged (verbatim quote):** "Remaining synthetic-mock cap: the RiskGate `required_model_agreement_count` gate (the momentum-biased mock advisory factors disagree with mean-reversion entries), a mock-data artifact a real council would not have, not the tuner." — AiTrader/PROGRESS.md:78
- **Evidence:**
  - The named artifact was removed on 2026-07-27: "`MockCatalystProvider` hashed the symbol string into a catalyst score and importance... The hash gave each symbol a fixed pseudo-random directional pull, so the mock advisory factors disagreed with mean-reversion entries in a way no real council would, and the disagreement count blocked entries." — AiTrader/CONTEXT.md:82; session record "The dead news mock was suppressing trades: removing it fixed tuner_floor, and ctest is 33 of 33 for the first time" — AiTrader/PROGRESS.md:557.
  - The companion flag is stale in the same way: "**ctest `tuner_floor` FAILS at `3e4a684` and is not caused by the provenance change.** ... Until then the suite is 30 of 31 and the plateau claim in Known Issues above is not currently demonstrable by the test that pins it." — AiTrader/PROGRESS.md:122. `3e4a684` is 2026-07-27T16:41:25-07:00 and the fix `74f5636` is 2026-07-27T19:32:30-07:00, under three hours later (`git -C <live> log --date=iso-strict -- PROGRESS.md`, read 2026-09-05); ctest is 34 of 34 at the anchor (AiTrader/PROGRESS.md:7, :209).
- **Recomputation (if any):** none.
- **What would resolve it:** Strike both entries through with their resolution dates, as the same document does for every other cleared flag (e.g. AiTrader/PROGRESS.md:86, :87, :88, :105-:108).
- **Confidence:** HIGH — the resolutions are recorded in the same two files.
- **Invalidated by later commits?:** no.
- **Disclosed by authors?:** no — both entries sit in the un-struck part of "Known Issues" and "Open Flags", where every other resolved item carries a strike-through or a CLEARED annotation.

---

## What I checked and found sound

Where I looked for the thesis and it did not hold. In each case the closure survives its own arithmetic
or the limitation is disclosed at the point it bites.

1. **The cross-sectional round's width closure (AiTrader/PROGRESS.md:820-832).** H-F failed at holdout
   z 1.668 against a bar of 2.50 because a 5-name book carries 66.4 percent realised tracking error
   (PROGRESS.md:824, :827). The 2026-07-27 limit change doubled `max_open_positions_total` 5 -> 10
   (PROGRESS.md:505), which looks like the registered reopen. I interpolated between the two widths the
   session itself measured (n=5: TE 66.4%, excess 27.99 bp/d; n=50: TE 31.7%, excess 10.04 bp/d,
   PROGRESS.md:827-828) on a power law and got n=10: TE 53.2%, excess 20.56 bp/d, **implied z 1.530 —
   lower than at n=5**. Widening does not rescue this family, exactly as the session predicted
   ("z barely moves and neither width clears", PROGRESS.md:828). The closure stands.
2. **The thin-sample council verdict of 2026-07-26 (AiTrader/PROGRESS.md:790-804).** 37 calls / 9 clusters,
   pooled +92.3 bp at z 1.706 with the interval spanning zero, labelled "TOO THIN TO TELL, which is a
   different finding from no predictive value, and the distinction was declared in advance so it could
   not be blurred afterwards" (PROGRESS.md:794). This is the correct label for a positive point estimate
   with a wide interval — the opposite of the failure mode I was hunting — and the session prices the
   confirmatory run at 25-85 USD rather than declaring the question closed (PROGRESS.md:803).
3. **Amendment 2, the 10.00 USD price floor (AiTrader/PROGRESS.md:403-425).** It removes 15.8 percent of
   S4 against 5.2 percent of S1 and says so (PROGRESS.md:421), rejects the stricter 15.00 floor on the
   tradeoff with both numbers stated (PROGRESS.md:419), and preserves the superseded 5.00 floor **with a
   registered reversal condition and the field needed to test it** (`median_close_at_formation`,
   PROGRESS.md:425). That is the shape a reopenable closure should have.
4. **Amendment 1, rank -> absolute ADV (AiTrader/PROGRESS.md:427-449).** Records that the amendment
   "does not fix the dispersion it was hoped to" and is "marginally worse" on max/median hurdle
   (PROGRESS.md:446), keeps `liquidity_rank` recorded so the superseded rule stays scoreable, and
   registers the reversal condition (PROGRESS.md:448). No hidden closure.
5. **Amendment 5's band decision (AiTrader/PROGRESS.md:246-256).** Faced with measured costs that eat the
   effect in S3/S4, the session kept the full band rather than restricting it, and recorded the reversal
   conditions ("thin strata failing the 30-cluster floor, or the gross signal concentrating entirely in
   S1/S2", PROGRESS.md:252). The independent audit flagged the permissive direction of this call in
   writing (PROGRESS.md:237). This is the opposite of closing too hard.
6. **The three-layer removal blocked by its own replay (AiTrader/PROGRESS.md:719-740, CONTEXT.md:94).**
   716 of 716 evaluations changed and 386 crossed the floor, so the removal was not performed. A closure
   that refused itself on evidence.
7. **The "unmeasurable without paid quote data" tick-multiple blocker (AiTrader/PROGRESS.md:274-285).**
   This is a textbook expired blocker, and the project found and corrected it itself, in writing, before
   I did: "an error message was read as broader than its wording, and one unprobed parameter separated a
   blocked question from an open one" (PROGRESS.md:282). Fully disclosed; no finding.
8. **The crypto scope narrowing (AiTrader/PROGRESS.md:576-606, CONTEXT.md:84).** Retention rather than
   deletion, restoration priced at "one class in `mal::scope`", the measured consequence stated at
   11,978 changed decisions including the 42 equity ones. Reversible by construction.
9. **The capacity-floor correction inside the news experiment (Amendment 7, AiTrader/PROGRESS.md:185-197).**
   The 4.96 bp figure is arithmetically exact (2,500/(2,520 x 2,000)) and the session verified the
   trade-cap mechanism in the engine rather than accepting the prior claim. This is the correction that
   findings 1-3 say was not carried across to the research gate; where it was applied, it was applied well.
10. **`research_satellite/` (long_term.py, research.py) and README.md.** No hypothesis closure, blocker,
    or reopen condition is registered in either; they are implementation and architecture surfaces. The
    one stale item I found in README.md is cosmetic (README.md:736 still mentions "prediction markets"
    trading around the clock after Polymarket's removal on 2026-07-06, CONTEXT.md:185) and is below the
    S4 threshold for a finding.
11. **`news_experiment/` collector state machine.** The absent-input rule (`no_news` vs `source_failed`),
    the fifth `excluded_pre_call` state, the `calendar_exhausted` split from `symbol_did_not_trade`, and
    the immutability of a resolved outcome are all implemented as described and each is guarded by a
    mutation-tested case (CONTEXT.md:48, :56, :64, :66). I found no state whose closure label is harsher
    than the evidence behind it.

If my thesis had held more widely here I would have expected: hypothesis families closed without a
registered reopen condition; "signal-absent" labels sitting on positive point estimates; and thin-sample
nulls presented as refutations. I found the opposite pattern on all three — reversal conditions are
registered as a habit, the 37-call positive was refused rather than claimed, and the thin/powered
distinction is pre-declared. The failure mode that is actually present is narrower and consistent:
**a governing number moved and the closures that leaned on it were never re-read** (findings 1-3), and
**documents were not swept forward after the blocker they cite expired** (findings 4, 7).

## Live-repo access log

Purposes: git history/provenance only (`git log` on `PROGRESS.md` and on the anchor SHA), to establish
the within-day ordering of the 2026-07-27 sessions and to confirm no commit between 2026-07-30 and the
anchor touches the research documents. No untracked or gitignored data was opened. Read time
2026-09-05 (UTC session date).

BEFORE (`git -C /home/kiros-li/Documents/GitHub/AiTrader status --porcelain`):

```
 M COLLECTION_LOG.md
```

AFTER (`git -C /home/kiros-li/Documents/GitHub/AiTrader status --porcelain`):

```
 M COLLECTION_LOG.md
```

Identical, and the single entry is the documented pre-existing dirt (a collector appends to
`COLLECTION_LOG.md`). Nothing was modified by me. No other entry appeared.
