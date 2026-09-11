# AiTrader — Direction A draft findings, part p2-return (RETURN.md)

Repository: AiTrader, anchored SHA `705e0ed128b7e184be6c1a23dcd06750c524c525` (main, 2026-08-24).
Primary document read in full: `AiTrader/RETURN.md`, 7,991 lines, 141 `## Prompt:` entries,
newest at top, spanning 2026-07-02 to 2026-07-29. All line numbers are SNAP line numbers,
identical to `git show 705e0ed:RETURN.md`.

Direction: A throughout. The thesis under test is that this program closed hypotheses earlier or
harder than its own evidence supports. RETURN.md is, on the whole, an unusually disciplined record:
pre-registration before looking, holdouts touched once, mutation-tested guards, and negatives
reported as headlines. The findings below are the places where a closure outran its evidence, and
the "What I checked and found sound" section is long on purpose.

---

### DRAFT-p2-return-1
- **Repository / SHA:** AiTrader / 705e0ed128b7e184be6c1a23dcd06750c524c525
- **Hypothesis or artifact:** H-B, daily time-series momentum long-short (pre-registered 2026-07-26, `255279b`), and its inclusion in the "six/seven families resolved against buy and hold" tally
- **Direction:** A
- **Class:** OVER_CLOSED
- **Severity:** S2
- **Label:** DERIVED
- **Claim challenged (verbatim quote):** "2. Nothing else measured this session earns a follow-up. H-C is closed negative. H-B could only be re-examined on a survivorship-free universe, which this database cannot provide." — AiTrader/RETURN.md:3485
- **Evidence:**
  - H-B's own verdict is NOT a negative. It is an inability to decide: "H-B daily TSMOM long-short | 5 sessions | n fit 1,848 | ... | n hold 1,146 | hold net +22.87 [-11.17, +56.90] | hold z +1.32 | cannot be distinguished from no edge" — AiTrader/RETURN.md:3472. The registered bar was |z| >= 2.39 (AiTrader/RETURN.md:3447).
  - The session names the exact and only remedy it would accept, quoted above, and declares the remedy unavailable in this database — AiTrader/RETURN.md:3485. The database in question is the 8-symbol, 2026-selected deep-history load whose selection bias the same session states: "the 2026-chosen universe overweights past uptrends, biasing the long side up and the short side down" — AiTrader/RETURN.md:3451.
  - **The stated blocker expired the same day, eighteen hours later.** `git -C AiTrader log`: `4ec2933 2026-07-26 00:32:09 -0700 Pre-registered hypothesis research against deep history` (the H-A/H-B/H-C session) precedes `a2f7c94 2026-07-26 18:43:03 -0700 Load a broad hindsight-free equity universe into the analysis database with survivorship and corporate-action handling`. Read 2026-09-05, read-only `git log`.
  - What the breadth load delivered is precisely the named remedy: "25,547,678 daily bars across 19,744 US equity tickers ... and 6,648 of those tickers are DEAD, each with an explicit end marker ... raised member deaths in 2023 and 2024 from ZERO to 35 and 31, and realised universe attrition from 1.12 to 2.17 percent per year" — AiTrader/RETURN.md:2985.
  - The very next round (`00c2d17`/`a0a9ef6`, 2026-07-26 19:14/19:26) used that universe for four NEW cross-sectional hypotheses (H-F..H-I) and did not re-run H-B; H-B is a time-series family, structurally distinct from all four (AiTrader/RETURN.md:2798-2804).
  - H-B is nonetheless counted as closed twice afterwards: "Six families are now resolved against buy and hold: the default stack, H-A, H-B, H-C, H-D, H-E" — AiTrader/RETURN.md:3234; and "**Seven families are now resolved against buy and hold with zero survivors**: the default stack, H-A, H-B, H-C, H-D, H-E, and now the cross-sectional family in four variants" — AiTrader/RETURN.md:2968.
  - The strongest signal in H-B sits exactly where the disclosed bias predicts, which is why the survivorship-free re-run matters rather than being a formality: "Holdout long side +55.8 net (z=2.56, secondary), short side -18.7 (z=-0.67)" — AiTrader/RETURN.md:3477.
- **Recomputation (if any):** none required; the finding is an ordering and coverage fact, not an arithmetic one. Inputs: RETURN.md:3472 (z 1.32, n 1,146), RETURN.md:3485 (the blocker), git commit timestamps of `4ec2933` and `a2f7c94`.
- **What would resolve it:** either re-run H-B's specification unchanged against `universe_membership` under the corrected `U-LIQ-500-stk-w60-m40-p5` rule with a fresh pre-registration and a holdout that has not been read for this hypothesis, or amend the tally at RETURN.md:2968/3234 to read "five resolved, H-B undecided pending a survivorship-free re-run". Either resolves it; nothing else does.
- **Confidence:** HIGH — the blocker is quoted verbatim, its expiry is a git object, and no later RETURN.md entry re-tests H-B.
- **Invalidated by later commits?:** no — every commit after 2026-07-29T20:18 on this branch is a collection-log append (`f819b68` is the last code session; `8a49239`, `f1fb308`, `b5c2236`, `705e0ed` are log-only), so no later session could have re-run H-B.
- **Disclosed by authors?:** no — the report discloses H-B's selection bias and states the remedy, but nothing anywhere records that the remedy arrived and was not used, and both later tallies count H-B as resolved without qualification.

---

### DRAFT-p2-return-2
- **Repository / SHA:** AiTrader / 705e0ed128b7e184be6c1a23dcd06750c524c525
- **Hypothesis or artifact:** Industry/sector momentum, rejected before testing in the cross-sectional round's pre-registration (2026-07-26, `00c2d17`); and the same blocker as it constrains the wide council run's independence design
- **Direction:** A
- **Class:** OVER_CLOSED
- **Severity:** S2
- **Label:** DERIVED
- **Claim challenged (verbatim quote):** "| Industry or sector momentum | UNTESTABLE. No sector classification in the database. |" — AiTrader/RETURN.md:2787
- **Evidence:**
  - The rejection is a data-availability closure taken before any computation, in a table headed "REJECTED BEFORE TESTING, for missing data or missing mechanism, recorded per the rule" — AiTrader/RETURN.md:2781.
  - The same blocker is carried into the wide council run's design two days later: "The database carries NO sector classification (recorded by the cross-sectional round), so cross-sector independence is approximated by stratifying the full liquidity distribution rather than claimed from a sector table. Stated as a limitation up front." — AiTrader/RETURN.md:2353; repeated as disclosure 7, "**No sector classification exists in the database**, so equity independence rests on liquidity-rank stratification across the full top-500 rather than on a sector table." — AiTrader/RETURN.md:2488.
  - **An alternative source was already integrated in this repository and is demonstrated resolving sector two days later.** RETURN.md:437: "`universe_asset` has **no sector column** so sector comes from Finnhub with `sector_source` recording absence (44/47 resolved, 3 `unresolved`)."
  - The implementation is thirty lines and uses an endpoint the repo's Finnhub client already exposes: `news_experiment/collect.py:163-180`, `fetch_sector(client, symbol)` calls `client._get("stock/profile2", {"symbol": symbol})` and reads `finnhubIndustry`, returning `(None, "unresolved")` or `(None, "absent_in_source")` rather than guessing. Persisted as `sector`/`sector_source` at `news_experiment/store.py:62-63`.
  - Finnhub was integrated in this repository since 2026-07-15/16, well before the rejection: the discovery client is described as "quotes, company news, pre-computed news sentiment, basic fundamentals, analyst ratings, and the earnings calendar" (`discovery/finnhub_source.py:4`), the key has a Settings field and a keystore credential (AiTrader/RETURN.md:6816), and a live health check confirmed the key working at 107.8 ms (AiTrader/RETURN.md:6631).
  - The cost is bounded and was measured in the repo's own terms: "~400 symbol-day queries per trading day, which is under 7 minutes against the integrated Finnhub 60/min free tier" — AiTrader/RETURN.md:1225. A one-off sector pull for the 1,187 distinct universe members is a fraction of that.
- **Recomputation (if any):** none. The claim is that a named-in-repo alternative source existed; the evidence is the shipped code path.
- **What would resolve it:** resolve `finnhubIndustry` once for the 1,218 distinct `universe_membership` names (or state why an issuer-level, largely time-invariant classification cannot be used point-in-time when a fund classification already is, AiTrader/RETURN.md:3001), then either run the sector-momentum hypothesis under a fresh pre-registration or record the rejection on a mechanism ground rather than a data ground.
- **Confidence:** HIGH — the blocker quote and the working code path are both in the anchored tree, and the code path post-dates the blocker by two days in the same repository.
- **Invalidated by later commits?:** no — `news_experiment/collect.py` is present at the anchor and no later commit removes it; every post-2026-07-29 commit is a collection-log append.
- **Disclosed by authors?:** no — the sector gap is disclosed repeatedly (RETURN.md:2353, 2488, 2787), but nowhere is it recorded that the repository's own Finnhub client answers it, and the sector rejection was never revisited after `fetch_sector` shipped.
- **Note, stated so this finding is not read wider than it is:** the same table also rejects Value and Size for "No fundamentals" / "No shares outstanding" (AiTrader/RETURN.md:2785-2789). Finnhub `stock/metric` fundamentals are likewise integrated (`discovery/finnhub_source.py:80,335`) and the long-term sleeve already consumes "quality, roe, margin, growth, pe, 52-week range" (AiTrader/RETURN.md:5557). I am **not** raising those two, because a free-tier fundamentals snapshot is a present-day value and a 2016-2026 cross-sectional backtest needs point-in-time fundamentals; that objection is real and the repository did not state it. Sector is different: `finnhubIndustry` is an issuer property that the repository already treats as time-invariant for the analogous fund classification.

---

### DRAFT-p2-return-3
- **Repository / SHA:** AiTrader / 705e0ed128b7e184be6c1a23dcd06750c524c525
- **Hypothesis or artifact:** Council confidence calibration (Task 2 of "Ask the recorded council calls what else they knew", 2026-07-27, `958cfcb`) — declared not practically settleable
- **Direction:** A
- **Class:** OVER_CLOSED
- **Severity:** S2
- **Label:** DERIVED
- **Claim challenged (verbatim quote):** "WHAT WOULD SETTLE IT: with a bootstrap standard deviation of 0.0541 at 80 clusters, reaching the corrected bar at the observed rho needs **1,149 clusters, 14.4 times the current sample**. There are not 1,149 liquid instruments this system can evaluate, so the question is not practically settleable at this effect size." — AiTrader/RETURN.md:2221
- **Evidence:**
  - The deciding figures: pooled Spearman rho +0.0357, cluster-bootstrap interval [-0.067, +0.145], z 0.660, n 274 scorable directional calls across 80 symbol clusters — AiTrader/RETURN.md:2217, 2187.
  - The instrument-count premise is contradicted by this repository's own universe tables, loaded the previous day: "25,547,678 daily bars across **19,744** US equity tickers" — AiTrader/RETURN.md:2985; membership "124 formation dates, **1,187** distinct names" (AiTrader/RETURN.md:2808), corrected to "**1,218**" distinct names across 3,076 member-months (AiTrader/RETURN.md:2706); eligible pool at the 2026-01-02 formation "**9,999**" (AiTrader/RETURN.md:744).
  - The successor experiment, specified two days later, draws its band from the same store: "band 1,558 members from a 9,613-symbol eligible pool" (AiTrader/RETURN.md:439) and, at the derived 10.00 price floor, "2,769" members at 2026-01-02 (AiTrader/RETURN.md:643). Every one of these counts exceeds 1,149.
  - The wide run had already demonstrated that scaling clusters is mechanical, not exotic: it went from 9 clusters to "**distinct symbol clusters evaluated | 90** (21 crypto, 69 equity)" by rank-stratifying the top-500 book, at a realised spend of "**Real spend 10.87 USD against the 120 USD ceiling**" — AiTrader/RETURN.md:2406, 2397.
  - The same programme's own settling arithmetic prices clusters, not instruments: "establish a 50 bp effect | 66 clusters | 272 directional calls | ... | **509** evaluations | **85.39 USD**" — AiTrader/RETURN.md:2618, and it says explicitly "**THE MONEY IS NOT THE CONSTRAINT.** ... The binding constraint is SYMBOL DIVERSITY" — AiTrader/RETURN.md:2622.
- **Recomputation (if any):**
  - Inputs: rho = 0.0357 and bootstrap SD = 0.0541 at g = 80 clusters (AiTrader/RETURN.md:2221, 2217); bar |z| >= 2.50 (AiTrader/RETURN.md:2155); scaling 509 evaluations per 66 clusters and 85.39 USD (AiTrader/RETURN.md:2618); realised 389 evaluations for 10.87 USD (AiTrader/RETURN.md:2403, 2397).
  - Method: SD(g) = 0.0541 * sqrt(80/g); solve rho/SD(g) = 2.50. Script `/home/kiros-li/.cache/program-audit/scratchpad/work/agentA-AiTrader-p2/recompute.py`.
  - Result: **g = 1,148** clusters — the repository's 1,149 is arithmetically correct and I do not dispute it. Implied evaluations 1,148 * (509/66) = **8,855**. Cost at the session's own planned rate (85.39/509 = 0.1678 USD/eval) = **1,486 USD**; at the rate actually realised in the wide run (10.87/389 = 0.0279 USD/eval) = **247 USD**.
  - So the recorded blocker ("there are not 1,149 liquid instruments") is false against this repository's own data, and the true blocker is a $250-$1,500 spend plus a wider 5-minute bar pull — a materially different and much weaker statement than "not practically settleable".
- **What would resolve it:** restate the limitation as what it is (a spend and bar-coverage cost, quantified), or run the confidence-ordering test at the width the universe tables already support. Either removes the false premise.
- **Confidence:** HIGH — the cluster arithmetic reproduces exactly, and the contradicting instrument counts are in the same repository one day earlier and two days later.
- **Invalidated by later commits?:** no — the universe tables and the news-experiment band both post-date the claim and are present at the anchor; nothing after 2026-07-29 is a code session.
- **Disclosed by authors?:** no. The session discloses the sample's other limits at length ("80 clusters over two days in one market regime, with GPT-5.5 absent from the entire equity half, cannot exclude a small effect" — AiTrader/RETURN.md:2274) but the instrument-count claim is stated as a fact and is not qualified anywhere.

---

### DRAFT-p2-return-4
- **Repository / SHA:** AiTrader / 705e0ed128b7e184be6c1a23dcd06750c524c525
- **Hypothesis or artifact:** H-H, low idiosyncratic volatility (cross-sectional round, 2026-07-26, `a0a9ef6`) — disqualified by its own report and still counted as a resolved family
- **Direction:** A
- **Class:** INTERNAL_INCONSISTENCY
- **Severity:** S2
- **Label:** READ
- **Claim challenged (verbatim quote):** "3. **Seven families are now resolved against buy and hold with zero survivors**: the default stack, H-A, H-B, H-C, H-D, H-E, and now the cross-sectional family in four variants." — AiTrader/RETURN.md:2968
- **Evidence:**
  - The same document disqualifies one of those four variants in its verdict list: "**H-H, low idiosyncratic volatility: FAILS, and is separately DISQUALIFIED by a disclosed defect.** Holdout point estimate is negative at z equals -0.086 with capacity -157 USD per year. See the disclosure below: 51 of its 124 books contain an S&P 500 index ETF." — AiTrader/RETURN.md:2923.
  - The mechanism is definitional, not incidental: "An index fund has near-zero idiosyncratic volatility against SPY BY CONSTRUCTION, so a low-IVOL ranking selects it almost by definition ... Contamination by hypothesis: H-F 0 of 115 books, H-I 0 of 115, H-G 1 of 124 (RSX in 2022-03), **H-H 51 of 124**." — AiTrader/RETURN.md:2932. Deciding figure: holdout excess -0.25 bp/day, 95% CI [-5.9, +5.4], z -0.086, over 31 holdout months / 2.55 years — AiTrader/RETURN.md:2861.
  - The universe classifier was corrected the same day, so the enabling condition for a valid re-test exists in the anchored tree: "distinct names | 1,187 | **1,218** ... funds remaining in membership | 6 vehicles, 150 months | **0** ... unclassified in membership | admitted silently | **0**" — AiTrader/RETURN.md:2706-2709 (`d6ad37a`, 2026-07-26 20:58, i.e. 92 minutes after `a0a9ef6`).
  - The correction session registers the reopen condition explicitly and then no round is ever run under it: "4. **Any future round uses the corrected universe from a fresh pre-registration.** Prior and future results are not comparable across the correction and must not be pooled." — AiTrader/RETURN.md:2729. RETURN.md contains no later hypothesis round of any kind.
  - The correction session also refuses to re-score, correctly, and hands the obligation forward: "**No hypothesis result was recomputed.** ... Re-scoring H-F, H-G, H-H or H-I against a universe corrected after their outcome was seen is precisely the contamination that round's discipline prevented" — AiTrader/RETURN.md:2723.
- **Recomputation (if any):** contamination share, from AiTrader/RETURN.md:2923 and 2932. 51 of 124 five-name books contain SPLG = **41.1 %** of H-H's formation books; at equal weight that is **8.2 %** of all H-H book-months held in an S&P 500 tracker. Script as above.
- **What would resolve it:** run H-H's unchanged specification once against the corrected `universe_membership` under a fresh pre-registration, as RETURN.md:2729 already requires; or amend the tally at RETURN.md:2968 to exclude a hypothesis its own verdict list calls disqualified.
- **Confidence:** HIGH — both quotes are in one document, and the corrected universe exists at the anchor.
- **Invalidated by later commits?:** no — no later commit runs a hypothesis round.
- **Disclosed by authors?:** partly, and I say so plainly. The contamination and the disqualification are fully disclosed by the authors at AiTrader/RETURN.md:2923 and 2932, and the reopen condition is registered at 2729. What is not disclosed anywhere is that a hypothesis the same report labels DISQUALIFIED is then counted inside "seven families ... resolved ... with zero survivors" (RETURN.md:2968), and that the enabling correction landed the same evening and was never used.

---

### DRAFT-p2-return-5
- **Repository / SHA:** AiTrader / 705e0ed128b7e184be6c1a23dcd06750c524c525
- **Hypothesis or artifact:** Stage 1 Task 6, the model comparison that decides the scoring model for the news-drift experiment; and Amendment 3's selection of `claude-haiku-4-5`
- **Direction:** A
- **Class:** OVER_CLOSED
- **Severity:** S3
- **Label:** READ
- **Claim challenged (verbatim quote):** "**NOT answered:** whether capability matters, which must be redone before the cheap-tier decision. OQ3, 6 and 8 were out of scope." — AiTrader/RETURN.md:612
- **Evidence:**
  - The comparison produced one usable arm of four: "| claude-haiku-4-5 | 21 | **0.0%** | 52.4% | $0.000403 | $0.0085 | / | claude-opus-4-8 | 21 | **100%** | n/a | $0 | $0 | / | gemini-3.1-pro-preview | 2 | 0.0% | 50.0% | $0.000559 | $0.0011 |" — AiTrader/RETURN.md:596-598. DeepSeek V4 Flash "has NO CREDENTIAL and could not be tested at all" — AiTrader/RETURN.md:600.
  - Both failures are blockers, not model verdicts, and both were named as such: "**The Opus 100 percent is MY BUG, not a model failure** ... Every call returned `HTTP 400: temperature is deprecated for this model`. **Opus was never tested.**" — AiTrader/RETURN.md:602. "**Gemini latched EXHAUSTED** on HTTP 429 with quota language after 2 calls, per the recorded rule, and was not retried." — AiTrader/RETURN.md:604.
  - **Both blockers expired inside this repository.** The Opus one was diagnosed and recorded the next day: "CLAUDE.md now records that `claude-opus-4-8` rejects `temperature` with `HTTP 400 invalid_request_error` ... **That is why Stage 1's Opus column read 100 percent parse-fail: the model was never reached.**" — AiTrader/RETURN.md:539. The Gemini one had already lifted once before: "**GEMINI HAS RECOVERED**: it was HTTP 429 account-quota-exhausted through the 2026-07-20 sessions and now answers, slowly." — AiTrader/RETURN.md:5360.
  - Removing `temperature` is a one-line change on the same seam the repository had already used for GPT-5: "OpenAIProvider now sends max_completion_tokens (not max_tokens) and omits temperature (GPT-5 family allows only the default)" — AiTrader/RETURN.md:7353. Re-running the arm costs the same order as the original: 21 headlines at $0.000403 to $0.000559 per call, i.e. cents.
  - The decision was taken anyway and collection now runs on it: Amendment 3 selects `claude-haiku-4-5` (AiTrader/RETURN.md:480), Stage 2 builds the collector to it (AiTrader/RETURN.md:433), and the pre-registration was ACCEPTED and closed on 2026-07-28 (AiTrader/RETURN.md:433), with collection running daily through 2026-08-21 at the anchor (AiTrader/COLLECTION_LOG.md, tail).
- **Recomputation (if any):** none needed. The precondition at RETURN.md:612 is a stated gate; the gate was not met and the decision it gates was taken.
- **What would resolve it:** re-run the fixed comparison set (`claude-haiku-4-5`, `claude-opus-4-8` without `temperature`, `gemini-3.1-pro-preview`) on the same 21 recorded headlines at temperature-default, and either confirm Haiku or record that the cheap-tier choice was made on cost and rule-compliance alone rather than on capability. The specification's own Task 5 reversal conditions (AiTrader/RETURN.md:508) already contemplate a head-to-head.
- **Confidence:** MEDIUM — the precondition and the un-run arm are unambiguous, but the practical stakes are bounded: the experiment's verdict table already forbids reading a gross positive as "the model understands" (AiTrader/RETURN.md:167), so an untested Opus arm does not invalidate the primary.
- **Invalidated by later commits?:** no — no post-anchor commit re-runs the comparison; the collector is fixed on `claude-haiku-4-5` and the specification is binding.
- **Disclosed by authors?:** yes — squarely, in two places. "**No claim is made that Haiku is better** — Stage 1 produced one usable arm out of four and the capability question stays open." (AiTrader/RETURN.md:480) and "A follow-up note was added under the Stage 1 verdict recording that **Amendment 3 does not resolve the model comparison** and does not license a best-of-four claim." (AiTrader/RETURN.md:506). What I add is only that the two blockers that produced the missing arms have since expired inside this repository, and that RETURN.md:612 states the comparison "must be redone **before** the cheap-tier decision" — a sequencing that was not honoured.

---

### DRAFT-p2-return-6
- **Repository / SHA:** AiTrader / 705e0ed128b7e184be6c1a23dcd06750c524c525
- **Hypothesis or artifact:** The crypto removal from all trading paths (2026-07-27, `8fd9fbf`), and the cost comparison that justified it
- **Direction:** A
- **Class:** STALE_FIGURE
- **Severity:** S3
- **Label:** DERIVED
- **Claim challenged (verbatim quote):** "Crypto round trips cost 50 bp against equity's 1.14 to 4.87 bp in the tradeable bands" — AiTrader/RETURN.md:1431
- **Evidence:**
  - That ratio is the lead justification for a scope decision that closed nine separate code paths and made crypto ineligible for entry at the universe layer (AiTrader/RETURN.md:1443-1467). It rests on the fee model's spread component, which at the time carried an explicitly unmeasured tick multiple: "`alpaca_equity_spread_tick_usd: 0.01` and `alpaca_equity_spread_tick_multiple: 1.0` ... **The multiple ships at 1.0, which is the floor, and the config says in writing that the model therefore understates small-cap spread by construction.**" — AiTrader/RETURN.md:1647.
  - Two days later the multiple was measured on consolidated SIP quotes and the equity side moved by roughly an order of magnitude in the band the successor experiment trades: "Round-trip hurdle (spread + 0.3 bp fixed): S1 16.1 med / 64.2 p90, S2 21.4 / 95.4, S3 30.9 / 121.4, S4 50.3 / 211.9. The one-tick floor said 2.4-5.1 bp: **understated 6.7x-9.9x**." — AiTrader/RETURN.md:249. Applied to the fee model as `tier3 = 8.0`, `tier4 = 9.0` — AiTrader/RETURN.md:251. n = 1,402 quote cells kept of 1,440, 157 of 160 symbols, 3 sessions (AiTrader/RETURN.md:234).
  - The repository notices the consequence and files it as a note rather than reopening the decision: "CLAUDE.md scope note corrected: 0.5 to 0.9 bp for the tier-1 names the engine trades, the superseded 1.14 to 4.87 recorded as the one-tick floor, **tier 4's measured 41.2 bp noted within 20 percent of crypto's 50**, conclusion stands on tier 1 with the reasoning recorded as narrowed." — AiTrader/RETURN.md:144.
  - The fee model already carries a crypto maker rate that was never used to re-cost the comparison: "Round trips the model returns: crypto taker 50.0 bp, **crypto maker 30.0 bp**, equity 1.3 bp." — AiTrader/RETURN.md:3394. Maker execution is named elsewhere as a live resolution path with its costs recorded (AiTrader/RETURN.md:211).
  - The band that matters is the news experiment's: ADV 2.07M-65.3M (AiTrader/RETURN.md:715), i.e. exactly fee tiers 3 and 4.
- **Recomputation (if any):**
  - Inputs: crypto taker RT 50.0 bp and maker RT 30.0 bp (AiTrader/RETURN.md:3394); equity band floors 3.15 and 4.87 bp (AiTrader/RETURN.md:1613-1614); measured equity tier 3 17.8 bp and tier 4 41.2 bp (AiTrader/RETURN.md:144, 251).
  - Method: ratio crypto/equity round trip, per tier, before and after the measurement. Script as above.
  - Result: the gap the removal cited collapses from **15.9x (tier 3) / 10.3x (tier 4)** to **2.8x / 1.2x**. Against the crypto **maker** rate the measured tier-4 equity round trip is **1.37x more expensive than crypto**. The removal's cost argument survives only for tier-1 mega caps (0.5-0.9 bp), which is the population the engine traded then and not the population the successor experiment is built on.
- **What would resolve it:** either measure the tick multiple for tiers 1/2/5/6 with the same script (they remain "1.0 floors marked UNMEASURED" — AiTrader/RETURN.md:251) and re-state the crypto comparison per tier, or record explicitly in CLAUDE.md/CONTEXT.md that the crypto exclusion is now a tier-1 conclusion and carries no cost argument in the ADV 2.07M-65.3M band.
- **Confidence:** MEDIUM — the arithmetic is unambiguous, but the crypto removal had three independent legs (cost; the P26 split at -48.78 bp crypto vs -2.73 equity; council abstention 87-94 % on crypto vs 43-47 % on equity — AiTrader/RETURN.md:1431), and only the cost leg is affected.
- **Invalidated by later commits?:** no — the tick measurement and the CLAUDE.md correction both precede the anchor and no later commit revisits the scope decision.
- **Disclosed by authors?:** partly. The proximity of tier 4 to crypto is disclosed at AiTrader/RETURN.md:144, and the narrowing of the conclusion to tier 1 is recorded there. What is not recorded anywhere is that the deciding ratio moved by roughly an order of magnitude, that the crypto maker rate inverts it at tier 4, and that the band the successor experiment trades is precisely the affected one.

---

### DRAFT-p2-return-7
- **Repository / SHA:** AiTrader / 705e0ed128b7e184be6c1a23dcd06750c524c525
- **Hypothesis or artifact:** The LLM council layer's remaining justification, closed 2026-07-27 (`958cfcb`)
- **Direction:** A
- **Class:** OVER_CLOSED
- **Severity:** S3
- **Label:** READ
- **Claim challenged (verbatim quote):** "Across three sessions the layer has now been measured on direction, on calibration, on abstention, on rejection, and on asset class, and nothing has been demonstrated on any axis. ... **No measured justification for the layer remains on this evidence.**" — AiTrader/RETURN.md:2274
- **Evidence:**
  - One of three providers contributed nothing at all to the equity half, which since the crypto removal (`8fd9fbf`, the following day) is the entire tradeable universe: "| gpt-5.5 | equity | 244 | **244** | not measurable | 0 | not measurable | not measurable |" — AiTrader/RETURN.md:2254; "all 244 calls errored on the quota exhaustion disclosed in the wide run" — AiTrader/RETURN.md:2256.
  - The absent provider is the one the earlier record identified as the only voice the council ever had: "**THE COUNCIL IS GPT-5.5.** All 22 evaluations carrying a directional council verdict had GPT-5.5 directional, and there are ZERO evaluations where GPT-5.5 was flat and the council was not." — AiTrader/RETURN.md:2531. In the wide run its whole contribution is 19 scorable calls across 11 clusters, every one crypto — AiTrader/RETURN.md:2440, 2253.
  - The blocker is a funding state, not a technical one, and the repository says so: "This is **billing exhaustion on the operator's accounts**, not model behaviour" — AiTrader/RETURN.md:2419; the exhaustion latch "is process state and deliberately not persisted: **an account stays dry until it is funded**" — AiTrader/RETURN.md:2311.
  - The programme's own price for settling the direction question is small: "**THE MONEY IS NOT THE CONSTRAINT. Settling this costs between 8 and 85 dollars.**" — AiTrader/RETURN.md:2622; the wide run itself spent 10.87 USD (AiTrader/RETURN.md:2397).
  - The two providers that did answer the equity half disagree in sign at a magnitude the interval cannot separate: Opus -13.3 bp [-39.5, +12.9] (n 148, 72 clusters) against Gemini +18.6 bp [-7.3, +44.5] (n 107, 65 clusters) — AiTrader/RETURN.md:2438-2439.
- **Recomputation (if any):** none. The finding is coverage, not arithmetic: the pooled primary (-0.5 bp, z -0.046, n 274, 80 clusters — AiTrader/RETURN.md:2437) does not depend on GPT-5.5, but the per-provider and council-versus-member results do, and equity is now the whole universe.
- **What would resolve it:** fund the OpenAI account and re-run the equity half of the wide design (69 rank-stratified names, 4 rounds each, ~$30 at the realised rate), or restate the layer's verdict as "no measured justification on two of three providers in equity, the third structurally absent".
- **Confidence:** MEDIUM — the closure is hedged carefully by its own authors ("That is a statement about what has been measured, not a proposal" — AiTrader/RETURN.md:2274), and the pooled result is genuinely powered; the gap is real but narrower than the headline sentence suggests.
- **Invalidated by later commits?:** no — no later commit runs a council evaluation; the layer's weights were zeroed on 2026-07-27 (`deb51b7`) and the panels removed on 2026-07-29 (`f819b68`), both post-dating the closure.
- **Disclosed by authors?:** yes — explicitly and prominently: "(3) **GPT-5.5 is absent from the equity half entirely, so every figure involving it rests on crypto alone.**" (AiTrader/RETURN.md:2278) and "GPT-5.5's equity column is not measurable at all" (AiTrader/RETURN.md:2256). What I add is that the blocker is a funding state the repository prices at $8-85, and that the asset class in which the provider is absent became the only tradeable class the following day.

---

### DRAFT-p2-return-8
- **Repository / SHA:** AiTrader / 705e0ed128b7e184be6c1a23dcd06750c524c525
- **Hypothesis or artifact:** RETURN.md's own completeness rule, for the session that overturned the tick-multiple blocker (commit `e60232a`, 2026-07-28)
- **Direction:** A
- **Class:** PROCESS
- **Severity:** S4
- **Label:** DERIVED
- **Claim challenged (verbatim quote):** "Log every user prompt to RETURN.md before starting work, newest at top, recording the prompt, model, changes, and commit message." — AiTrader/CLAUDE.md:9
- **Evidence:**
  - `git -C AiTrader log`: `e60232a 2026-07-28 14:39:07 -0700 Find a free consolidated quote source on the existing credential, correcting the paid-subscription conclusion, no amendment made`. `git show --stat e60232a` touches **PROGRESS.md only, 13 insertions**. Read 2026-09-05, read-only.
  - RETURN.md at the anchor contains no `## Prompt:` entry for that session; `grep -n "free consolidated quote\|paid-subscription\|delayed_sip"` over RETURN.md returns nothing matching it, and the file holds 141 `## Prompt:` entries.
  - The session it omits is the one that lifted the programme's longest-standing blocker. The prior state was recorded as terminal: "**THE POSITION IS WORSE THAN BEFORE, STATED PLAINLY.** The multiple moved from 'unmeasured and one script away' to 'unmeasured and behind a paid data subscription'." — AiTrader/RETURN.md:418; and earlier, "Establishing the tick multiple needs quote data, which needs a paid subscription" — AiTrader/RETURN.md:1637; and "**The tick multiple remains the binding blocker** and is behind a SIP-entitled market-data subscription" — AiTrader/RETURN.md:308.
  - The e60232a commit message and its PROGRESS.md entry state the correction: "It is unmeasured and reachable for free ... an error message was read as broader than its wording, and one unprobed parameter separated a blocked question from an open one."
  - The finding does survive into RETURN.md indirectly, inside the next session's prompt summary at AiTrader/RETURN.md:224, which is why this is hygiene rather than a lost result.
- **Recomputation (if any):** none.
- **What would resolve it:** add the missing `## Prompt:` entry for `e60232a` to RETURN.md, or amend CLAUDE.md:9 to say that a findings-only session may record to PROGRESS.md alone.
- **Confidence:** HIGH — the commit exists, its stat is one file, and RETURN.md has no matching entry.
- **Invalidated by later commits?:** no — no post-anchor commit adds the entry.
- **Disclosed by authors?:** no — nothing in RETURN.md or PROGRESS.md notes the missing entry.

---

## What I checked and found sound

Direction A did not hold in the following places. Each is listed with what I would have expected to
find if the thesis held, and what I found instead.

1. **The tick-multiple blocker.** Expected: a hard blocker ("behind a SIP-entitled market-data
   subscription", RETURN.md:308, 418) left standing while the experiment proceeded on an unmeasured
   floor. Found: the blocker was probed again on 2026-07-28 (`e60232a`), found false, and the
   measurement was run the next day (RETURN.md:230-256) with the fee model updated per tier, the
   monotonicity check applied before belief, and the specification implications reported but **not**
   applied because EXPERIMENT.md was binding (RETURN.md:253). This is the opposite of premature
   closure. (The missing RETURN.md entry for that session is DRAFT-p2-return-8, a hygiene point.)

2. **The Level 1 position limit as the cross-sectional family's binding constraint.** The round names
   it as such: "**The position limit, not the fee model and not the data, is what blocks this
   family**" (RETURN.md:2966), and the limit was raised from 5 to 10 the next day
   (`max_open_positions_total` 5 -> 10, RETURN.md:1137). I recomputed whether the closure survives
   the blocker's expiry. Fitting TE(n)^2 = a + b/n and excess(n) = c + d/n to the two measured widths
   (n=5: TE 66.4 %/yr, excess 70.5 %/yr; n=50: TE 31.7, excess 25.3 — RETURN.md:2857, 2872, 2899,
   2962) gives at n=10: TE 50.2 %/yr, excess 45.4 %/yr, needing 78.6 %/yr for z=2.50 over 2.55 years
   and delivering 45.4, i.e. **z falls from 1.668 to about 1.44**. Widening the book does not rescue
   H-F; the verdict survives its blocker's expiry. Recorded as sound.

3. **"The test cannot be won at this width" and more history.** Expected: a closure that a longer
   sample would overturn. Pooling fit and holdout inverse-variance (illegitimate, computed only as an
   upper bound: fit +12.88 bp/day at z 1.737 over 93 months, holdout +27.99 at z 1.668 over 31 months,
   RETURN.md:2856-2857) gives +15.35 bp/day, SE 6.78, **z 2.263 < 2.50**. Even the whole 10.3-year
   database would not clear the corrected bar. Sound.

4. **The capacity gate's per-position notional.** The capacity round and the cross-sectional round
   both size on "5,000 USD per position" from `max_trade_notional_cap_pct: 0.05` (RETURN.md:3161,
   2758). The next day that key was proved "**NOT ENFORCED ANYWHERE**" and the real ceiling was 500
   USD (RETURN.md:1046-1048). The error runs in the **permissive** direction, so the 12-of-14 and
   4-of-4 pre-test arithmetic rejections stand a fortiori; and after the 2026-07-27 re-derivation
   (10 positions x 2,000 USD = 20,000 deployed) the assumption became roughly true. No direction-A
   finding. Worth flagging to whoever audits direction B: H-F's reported "capacity clears the floor at
   17,634 USD per year" (RETURN.md:2857) was computed on 25,000 deployed against an enforced 1,000 at
   the time.

5. **H-A, the equity overnight premium.** Expected: a pass quietly kept. Found the opposite: the
   session that passed its own written bar (holdout +6.19 bp, z 2.91, RETURN.md:3471) immediately
   disclosed two defects in its own registration, computed the corrected clustered estimate
   (z 1.73, interval spanning zero), and registered a confirming observable
   ("night-clustered holdout z >= 2.39 on that bias-reduced spec", RETURN.md:3484). Queue 002 then ran
   exactly that spec and reported 1.87 (RETURN.md:3341). Reopened as registered and re-closed on
   evidence.

6. **The three "unmeasurable from stored data" diagnostics** (volume filter RETURN.md:4715, ATR band
   RETURN.md:4963, RSI-2 entry depth RETURN.md:4805). Each named its prerequisite (record per-entry
   filter state, or run a backtest). The prerequisite was built two days later (entry_decision
   instrumentation, RETURN.md:4435; harness, RETURN.md:4089) and every one of the three questions was
   re-run: the first backtest round (RETURN.md:4063-4065) and the deep-history H-G/H-T grid
   (RETURN.md:3573-3581). Reopened as registered.

7. **"FURTHER HYPOTHESIS ROUNDS AGAINST THIS DATABASE ARE NOT WORTH RUNNING"** (RETURN.md:3234). The
   same sentence names what would change the calculus — "a new information axis the bars do not
   carry" — and the breadth universe was loaded the next day and used the same evening
   (RETURN.md:2985, 2844); the news-drift experiment is the text axis, i.e. the same recommendation
   at RETURN.md:3601(3b). Closure with a live, honoured reopen condition.

8. **"TOO THIN TO TELL" was never blurred into "no effect".** The council scoring session declares the
   distinction in advance ("Fewer than 10 symbol clusters, or fewer than 30 scorable directional
   calls, reads as TOO THIN TO TELL ... **NOT** as evidence of absence", RETURN.md:2520), lands on 9
   clusters, refuses the negative ("It does NOT show the council fails to predict", RETURN.md:2630),
   and the next session re-powers it to 80 clusters. Exemplary.

9. **The three-layer removal was blocked by its own gate.** The prompt asked for a removal; the replay
   showed 386 of 716 evaluations would newly clear the Level 1 floor, all permissive, and the session
   stopped and removed nothing (RETURN.md:2083). Later the layers were deactivated by weight instead,
   with the permissive framing recorded in advance and the replay matching the pre-registration
   exactly (RETURN.md:2034). No premature closure.

10. **Amendment 5 widened rather than narrowed.** Faced with median hurdles of 16.1/21.4/30.9/50.3 bp
    against a 30 bp working effect, the specification separated the gross signal question from the net
    economic question and **kept the full band** rather than restricting to the survivable half, and
    recorded the counter-argument that a reader could call it a weakened standard (RETURN.md:205-207).
    The opposite of closing on a hard number.

11. **Every pre-registered negative I could check was reached on its own registered rule**, with the
    deciding number and its n stated: H-D (-12.48 bp/day, z -1.02, 697 days), H-E (-8.22, z -0.86,
    936 days) at RETURN.md:3219-3221; the 54-cell threshold grid with "**Zero positive cells out of
    108 cell-periods**" (RETURN.md:3581); the default stack at -1.97 bp [-2.68, -1.27] over 19,648
    trades (RETURN.md:3564). I found no case of a bar being moved after seeing a result, and two cases
    of a bar being **raised** after the fact for holdout reuse (RETURN.md:3323, 2834).

12. **Disclosure discipline.** Uncomfortable corrections are stated in the direction that hurts: the
    48-bar benchmark defect whose pre-fix z was 4.974 against the corrected 2.66 (RETURN.md:2189); the
    warmup fix that **improved** two hypotheses (RETURN.md:2930); the spend figure inflated sevenfold
    by the collector's own safety over-charge, corrected downward (RETURN.md:2484); the OOM incident
    that killed the validation stack, reported first (RETURN.md:3529).

Where I expected direction-A findings and did not get them: I looked specifically for a "signal-absent"
or "falsified" label sitting on a point estimate on the hypothesis side with a wide interval. The one
candidate is H-F (holdout +27.99 bp/day, z 1.668, RETURN.md:2857), and it is **not** labelled falsified —
it is labelled "**CANNOT BE DISTINGUISHED from buy and hold**" with the shortfall quantified and the
power deficit declared before the run (RETURN.md:2921, 2779). That is the correct label for that number.

## Live-repo access log

Live repository touched: `/home/kiros-li/Documents/GitHub/AiTrader`, read-only, on 2026-09-05 UTC.
Commands used: `git status --porcelain`, `git log --date=iso --pretty`, `git show --stat e60232a`,
`git show e60232a -- PROGRESS.md`. No checkout, no write, no script execution, no untracked data read.

`git -C /home/kiros-li/Documents/GitHub/AiTrader status --porcelain` **before** first access:

```
 M COLLECTION_LOG.md
```

`git -C /home/kiros-li/Documents/GitHub/AiTrader status --porcelain` **after** last access:

```
 M COLLECTION_LOG.md
```

Identical, and the single entry is the pre-existing collector dirt named in COMMON_RULES.md. Nothing
was modified by this audit.

Unanchored data read: none. Everything except the git-history facts above comes from
`SNAP/AiTrader` at the anchored SHA. The two git-history facts used in findings are commit
timestamps/ordering (DRAFT-p2-return-1) and the existence and file-stat of commit `e60232a`
(DRAFT-p2-return-8); both are immutable git objects at or before the anchor.

Scratch computation: `/home/kiros-li/.cache/program-audit/scratchpad/work/agentA-AiTrader-p2/recompute.py`.
