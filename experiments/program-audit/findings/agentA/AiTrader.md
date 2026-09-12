# Agent A — consolidated findings, AiTrader

Repository: AiTrader, anchored SHA `705e0ed128b7e184be6c1a23dcd06750c524c525` (main, 2026-08-24).
Direction A throughout: the case that a hypothesis, capability or blocker was closed on weaker
grounds than its label implies. All paths cite `AiTrader/<path>:<line>` and are identical in
`/home/kiros-li/.cache/program-audit/scratchpad/snap/AiTrader/` and in
`git -C <live AiTrader> show 705e0ed:<path>`.

Consolidated from three drafts covering `EXPERIMENT.md` / `AUDIT*.md` / `DATA_AUDIT.md` /
`LIVE_READINESS.md` / `WEEKLOG.md` (p1), `RETURN.md` (p2), and `PROGRESS.md` / `CONTEXT.md` /
`news_experiment/` / `research_satellite/` (p3). 22 draft entries merged to 18 findings.

## The strongest case for the thesis in this repository

This is not a repository that faked negatives — the measurement discipline is unusually good, and
the "found sound" section below is long on purpose. The failure mode that is actually present is
narrower: **a governing number moved and the closures leaning on it were never re-read.** On
2026-07-27 Level 1 per-position notional quadrupled (100–500 USD → 400–2,000 USD,
PROGRESS.md:191, replay-verified "exactly 4x" at PROGRESS.md:522) while the 2,500 USD/yr capacity
floor stayed put, dividing the net edge any hypothesis must clear by four. Twelve hypotheses had
been rejected 27 hours earlier on precisely that arithmetic, the council's closure boundary rests
on it, and the standing research gate still states the superseded 20 bp figure. Alongside it sit
three registered reopen paths that the shipped collector forecloses rather than keeps open as the
specification claims, a factor declared "unmeasurable" on an emptiness the repository's own passing
test says is by design, and two hypothesis families counted inside "seven families resolved with
zero survivors" while the exact remedies their own reports demanded landed in this repository hours
later and went unused.

---

### AUDIT-A-AiTrader-1
- **Repository / SHA:** AiTrader / 705e0ed128b7e184be6c1a23dcd06750c524c525
- **Hypothesis or artifact:** the price-only hypothesis programme against `analysis_bars.db`, closed 2026-07-26 as exhausted, together with the twelve candidates rejected on capacity arithmetic before any code ran
- **Direction:** A
- **Class:** OVER_CLOSED
- **Severity:** S1
- **Label:** DERIVED
- **Claim challenged (verbatim quote):** "Recorded implication: further price-only hypothesis rounds against this 8-symbol database at Level 1 sizing are not worth running, and the calculus changes only with a new information axis, maker execution (rescues nothing here), or a sizing change that is not on the table." — AiTrader/PROGRESS.md:849
- **Evidence:**
  - The registered reopen condition is "a sizing change", and a sizing change was applied the following day: `default_risk_per_trade_pct` 0.005 → **0.02**, `max_open_positions_total` 5 → 10, `max_open_positions_per_venue` 2 → 10, `max_total_open_risk_pct` 0.03 → 0.25 — AiTrader/PROGRESS.md:503-507, commit `82e8e72` 2026-07-27T21:25:16-07:00 (`git -C <live> log --date=iso-strict -- PROGRESS.md`, read 2026-09-05, read-only).
  - The twelve rejections and their capacity figures, all "at Level 1 sizing" against the unchanged 2,500 USD/yr floor: "12 of 14 candidates rejected before any code, on arithmetic (SEC EDGAR 13F following at 600 USD per year, turn-of-month at 480, FOMC drift at 392, crypto-to-equity spillover at 1,200, equity-to-crypto spillover net-negative against the 50 bp fee, intraday first-half-hour at 1,764, equity cross-section at 500 to 1,000 and NVDA-poisoned, crypto weekend net-negative, monthly crypto cross-section eaten by taker fees)" — AiTrader/PROGRESS.md:849 (n = 12 rejected candidates of 14).
  - Enforced per-position notional after the change: "position range \"100 to 500 USD\" to 400 to 2,000" — AiTrader/PROGRESS.md:191; replay-verified "notional per position | 100.00 | **400.00** (exactly 4x)" — AiTrader/PROGRESS.md:522 (n = 4 replay runs).
  - The floor itself did not move: "Accurate and untouched: trades 10/day, the 2,500 USD/year floor." — AiTrader/PROGRESS.md:191.
  - The crypto-leg objections in the same list ("net-negative against the 50 bp fee", "eaten by taker fees") were independently overtaken on 2026-07-27 when scope narrowed to US equities and the traded tier's measured round trip became 0.5–0.9 bp — AiTrader/PROGRESS.md:576; AiTrader/CONTEXT.md:84; AiTrader/PROGRESS.md:211.
  - No later entry revisits the closure. The last research round in the log is 2026-07-27 (AiTrader/PROGRESS.md:771); every session after the sizing change (AiTrader/PROGRESS.md:141-473) is news-experiment or hygiene work, and the four commits between 2026-07-30 and the anchor touch only `COLLECTION_LOG.md` and two `.gitignore` lines.
  - The second registered reopen leg, "a new information axis", was also met internally (breadth universe load 2026-07-26, AiTrader/PROGRESS.md:836) and honoured — see "found sound" item 8. It is the sizing leg that fired and was never read.
- **Recomputation:**
  - Inputs: capacity USD/yr figures at AiTrader/PROGRESS.md:849; floor 2,500 USD/yr at AiTrader/PROGRESS.md:854 and AiTrader/CONTEXT.md:108; notional multiplier 4x from AiTrader/PROGRESS.md:191 and :522 (a replay measurement, not a printed estimate).
  - Method: capacity is linear in per-position notional at fixed edge and fixed trade rate, so each rejected candidate's USD/yr figure scales by the notional multiplier. Multiply by 4, compare against the unchanged floor. Script `/home/kiros-li/.cache/program-audit/scratchpad/work/agentA-aitrader-p3/recompute.py`.
  - Result: intraday first-half-hour 1,764 → **7,056 USD/yr (2.82x the floor)**; crypto-to-equity spillover 1,200 → **4,800 (1.92x)**; equity cross-section upper bound 1,000 → **4,000 (1.60x)**. Still below: SEC EDGAR 13F 600 → 2,400 (0.96x), turn-of-month 480 → 1,920, FOMC drift 392 → 1,568, equity cross-section lower bound 500 → 2,000. **At least two, arguably three, of the twelve pre-code rejections invert at the sizing enforced one day later**, and the two that invert most are the two testable on the equity side of this database.
  - Cross-check: the cross-sectional round's holdout capacities scale identically (H-F 17,634 → 70,536, H-G 2,044 → 8,176, H-I 1,477 → 5,908 USD/yr, AiTrader/PROGRESS.md:827), but those three failed on significance rather than capacity, so this arithmetic does not reopen them.
- **What would resolve it:** re-run the capacity gate on the twelve rejected candidates at the enforced sizing and either record that the two or three survivors now warrant a pre-registered round, or record a non-capacity reason for keeping them closed; alternatively amend AiTrader/PROGRESS.md:849 to state that the reopen condition fired and the closure is retained on other grounds.
- **Confidence:** HIGH — the reopen trigger is registered in the closure's own sentence, the trigger fired 27 hours later in the same repository, the multiplier is measured by the project's own replay, and capacity is linear in notional.
- **Invalidated by later commits?:** no — no commit after 2026-07-29 touches PROGRESS.md, CONTEXT.md or any research artifact up to the anchor.
- **Disclosed by authors?:** no — the reopen condition is registered at AiTrader/PROGRESS.md:849, but the session that changed sizing (AiTrader/PROGRESS.md:491-532) does not mention the research capacity gate or the closed hypothesis families, and no later entry revisits them.

---

### AUDIT-A-AiTrader-2
- **Repository / SHA:** AiTrader / 705e0ed128b7e184be6c1a23dcd06750c524c525
- **Hypothesis or artifact:** the `whale_signal` advisory factor (SEC EDGAR 13F / Form 4), declared a fabricated and unmeasurable input by the 2026-07-27 data audit and deactivated to zero weight
- **Direction:** A
- **Class:** OVER_CLOSED
- **Severity:** S1
- **Label:** DERIVED
- **Claim challenged (verbatim quote):** "INFERRED. A factor with no source table and no history table cannot have been reading whale data, so those 2,162 confidences were produced without an input. That makes `whale_signal` a fabricated input which nonetheless carried 0.10 of the ensemble weight and sat inside the weight-normalised mean that decides the Level 1 confidence floor. The 2026-07-27 deactivation was better justified than the session that performed it knew: it treated `whale_signal` as unmeasured, and the data says it was unmeasurable." — AiTrader/DATA_AUDIT.md:22-28
- **Evidence:**
  - The inference rests on two tables being empty: "`whale_activity` holds **0 rows**. `whale_signal_history` holds **0 rows**." — AiTrader/DATA_AUDIT.md:17-18, tabulated at AiTrader/DATA_AUDIT.md:72-73. Deciding figures: 0 rows in each of two tables against **2,162 `whale_signal` rows** at mean confidence 0.5466 (n = 2,162 factor outputs, 2026-06-30 to 2026-07-26, AiTrader/DATA_AUDIT.md:19-20).
  - **Neither table is written on the live or paper path, by design, and the repository says so in two places written before this audit.** "HONEST ABOUT THE ACTIVITY COUNT. `whale_activity` holds RAW per-fetch rows, and nothing in the live path writes it: the engine asks the bridge for a SCORED signal and never persists the activity behind it (ops/demo.py is the only writer)." — AiTrader/api_server/store.py:617-619. Pinned by a passing test: "whale_activity (raw per-fetch rows) is empty by design: the engine asks the bridge for a scored signal and never persists the activity behind it." — AiTrader/tests/test_api_server.py:2709-2711 (`test_whale_feeds_labels_the_activity_count_honestly`).
  - Writer enumeration over the whole tree: the only `INSERT` into either table is the offline demo seeder — AiTrader/ops/demo.py:113 (`whale_activity`) and AiTrader/ops/demo.py:116 (`whale_signal_history`), whose own docstring reads "Fill whale_activity + whale_signal_history via the offline whale service." (AiTrader/ops/demo.py:80). Every other reference in `ui/`, `api_server/` and `tests/` is a SELECT or a fixture.
  - So both tables read 0 in production **whether or not the whale feed was live**; the emptiness carries no information about the input. The audit's own Task 1 conflates reference with writer: "**WRITTEN BY NOTHING:** none. Every table has at least one source reference." — AiTrader/DATA_AUDIT.md:87, against a table listing `whale_activity` at 19 src refs and `whale_signal_history` at 11 (AiTrader/DATA_AUDIT.md:72-73).
  - The feed was configured ON and its source is free and keyless: `sec_edgar_enabled: true` / `whale_live_enabled: true` — AiTrader/config/default_config.yaml:693-694, under the comment "SEC EDGAR is the free, keyless, active whale feed" (AiTrader/config/default_config.yaml:685-686, dated 2026-07-13), exported to the bridge at AiTrader/scripts/start_paper_trading.sh:87. The adapter is live-capable: "EDGAR is keyless and always available -> always attempt live." — AiTrader/whale_signal/adapters.py:285, live fetch at :296. Thirteen of the 2,162 outputs' days post-date the 2026-07-13 activation.
  - What the code genuinely leaves unknown is **attribution, not measurability**: `except Exception:` / `return self._mock(symbol)` — AiTrader/whale_signal/adapters.py:297-298 — silently degrades a live fetch to mock and records no per-output source. The honest statement is "the 2,162 outputs are unattributed between EDGAR and mock", a one-column fix rather than an unmeasurable hypothesis.
  - The narrower ground actually recorded in config stands and does not need the escalation: "The whale layer has never been scored against outcomes at all." — AiTrader/config/default_config.yaml:755-756, with `whale_signal_factor_weight: 0.0    # was 0.10` at :758.
- **Recomputation:** none required — this is a code-path check. Writers of `whale_activity` and `whale_signal_history` enumerated by `grep -rn` over `*.cpp`, `*.hpp`, `*.py`, `*.sql` across the snapshot: exactly one writer each, both in `ops/demo.py`, neither reachable from the engine, bridge or paper loop.
- **What would resolve it:** run the whale chain once with `SEC_EDGAR_ENABLED=1` over the five equity symbols in the declared universe, record the per-output source (live vs mock) alongside the confidence, and score those outputs against subsequent closed-trade outcomes. Both steps are free (EDGAR is keyless) and neither touches a Level 1 value. Until then the correct label is "never scored", not "unmeasurable".
- **Confidence:** HIGH — the empty-table inference is contradicted by an explicit code comment and a passing test in the same repository, and the writer enumeration is exhaustive.
- **Invalidated by later commits?:** no — every commit after 2026-07-29 up to the anchor touches only `COLLECTION_LOG.md` and `.gitignore` (`git show --stat` on 8a49239, f1fb308, b5c2236, 705e0ed), so neither the tables, the adapter, nor the audit text moved.
- **Disclosed by authors?:** no — DATA_AUDIT.md presents the empty tables as its lead finding ("THE FINDING THAT CHANGES A CONCLUSION", AiTrader/DATA_AUDIT.md:13-15) and nowhere records that both tables are unwritten on the live path, even though the project's own `api_server/store.py` and test suite say so.

---

### AUDIT-A-AiTrader-3
- **Repository / SHA:** AiTrader / 705e0ed128b7e184be6c1a23dcd06750c524c525
- **Hypothesis or artifact:** the permanent research capacity gate ("AN EDGE BELOW THE CAPACITY FLOOR IS NOT WORTH OPERATING REGARDLESS OF SIGNIFICANCE"), the standing pre-computation filter every research round must pass
- **Direction:** A
- **Class:** STALE_FIGURE
- **Severity:** S2
- **Label:** DERIVED
- **Claim challenged (verbatim quote):** "The floor is 2,500 USD per year at 100,000 equity, 2.5 percent, covering execution risk, infrastructure failure, and operator time. At Level 1 sizing (about 500 USD notional per trade) that requires roughly a 20 bp net edge at 10 trades per day, and the crypto gross hurdle behind such a net is 70 bp. A future hypothesis must state before testing how it clears this floor at permitted sizing." — AiTrader/CONTEXT.md:108
- **Evidence:**
  - The same gate in the session that created it: "Capacity table at Level 1 sizing (500 USD notional): a 10 bp net edge at 10 trades per day is 1,260 USD per year. CAPACITY FLOOR set as a permanent research gate: 2,500 USD per year (2.5 percent of equity), requiring roughly 20 bp net at 10 trades per day at Level 1 sizing, with the crypto gross hurdle at 70 bp behind it." — AiTrader/PROGRESS.md:854 (2026-07-26).
  - Level 1 sizing was re-derived the next day: `default_risk_per_trade_pct` "0.005 | **0.02**", derivation "capacity floor 2,500 USD/yr at an honest 10 bp edge needs 992 to 1,984 USD per position" — AiTrader/PROGRESS.md:503 (commit `82e8e72`, 2026-07-27T21:25:16-07:00, `git -C <live> log -- PROGRESS.md`, read 2026-09-05). Enforced range: "position range \"100 to 500 USD\" to 400 to 2,000" — AiTrader/PROGRESS.md:191; replay "notional per position | 100.00 | **400.00** (exactly 4x)" — AiTrader/PROGRESS.md:522 (n = 4 replay runs).
  - The repository's own recomputation of this exact quantity under the enforced sizing: "The 4.96 bp E-test comparison figure at the 2,000 USD sizer is CONFIRMED EXACT (2,500 / (2,520 x 2,000)) and does not move. At the enforced 2,500 USD ceiling the requirement is 3.97 bp." — AiTrader/PROGRESS.md:189 (Amendment 7, 2026-07-29); reaffirmed at :256 and used as the live bar at :272.
  - The 2026-07-29 stale-figure sweep that should have caught it bracket-noted CONTEXT.md's *scope* decision (AiTrader/CONTEXT.md:84) and then concluded "No other figure was found overtaken by this week's measurements." — AiTrader/PROGRESS.md:211. CONTEXT.md:108 and PROGRESS.md:854 were not touched.
  - Second leg also stale: "the crypto gross hurdle behind such a net is 70 bp" governs a system whose scope narrowed to US equities on 2026-07-27 (AiTrader/PROGRESS.md:576; AiTrader/CONTEXT.md:84), where the traded tier costs "roughly 0.5 to 0.9 bp" (AiTrader/CONTEXT.md:84 bracketed correction; AiTrader/PROGRESS.md:211).
- **Recomputation:**
  - Inputs: floor 2,500 USD/yr (AiTrader/CONTEXT.md:108); 10 trades/day × 252 = 2,520 entries/yr (AiTrader/PROGRESS.md:189, :511); per-position notional 500 USD old convention (AiTrader/CONTEXT.md:108, AiTrader/PROGRESS.md:854) and 2,000 USD enforced (AiTrader/PROGRESS.md:189, :191).
  - Method: required net edge = floor / (entries_per_year × notional).
  - Result: old 2,500/(2,520 × 500) = **19.84 bp** (the document's "roughly 20 bp"); enforced 2,500/(2,520 × 2,000) = **4.96 bp**; at the enforced 0.025 ceiling 2,500/(2,520 × 2,500) = **3.97 bp**. **The gate as written is 4.0x stricter than the same arithmetic on the enforced sizing.** The multiplier is convention-independent: the notional range moved 100→400 at the low end and 500→2,000 at the high end (AiTrader/PROGRESS.md:191), replay-measured "exactly 4x" (:522). Honest caveat: comparing the enforced range's LOW end (400 USD) against the old convention's HIGH end (500 USD) raises the requirement to 24.80 bp — but that mixes conventions, and Amendment 7 fixes the convention at 2,000 USD.
- **What would resolve it:** amend AiTrader/CONTEXT.md:108 and AiTrader/PROGRESS.md:854 to the enforced sizing (4.96 bp at the 2,000 USD sizer, 3.97 bp at the ceiling) and to the US-equity cost hurdle, exactly as Amendment 7 did for the news experiment; or state explicitly that the research gate deliberately keeps the superseded 500 USD convention, and why.
- **Confidence:** HIGH — both the stale figure and its corrected replacement are stated verbatim in this repository three days apart, and the arithmetic is one division.
- **Invalidated by later commits?:** no — the four commits after 2026-07-29 up to the anchor touch only `COLLECTION_LOG.md` and `.gitignore` (`git -C <live> log 705e0ed --since=2026-07-30`, read 2026-09-05).
- **Disclosed by authors?:** no — AiTrader/PROGRESS.md:211 ran a sweep for exactly this class of staleness and concluded no other figure was overtaken.

---

### AUDIT-A-AiTrader-4
- **Repository / SHA:** AiTrader / 705e0ed128b7e184be6c1a23dcd06750c524c525
- **Hypothesis or artifact:** H-B, daily time-series momentum long-short (pre-registered 2026-07-26, `255279b`), and its inclusion in the "six/seven families resolved against buy and hold" tally
- **Direction:** A
- **Class:** OVER_CLOSED
- **Severity:** S2
- **Label:** DERIVED
- **Claim challenged (verbatim quote):** "2. Nothing else measured this session earns a follow-up. H-C is closed negative. H-B could only be re-examined on a survivorship-free universe, which this database cannot provide." — AiTrader/RETURN.md:3485
- **Evidence:**
  - H-B's own verdict is not a negative but an inability to decide: "| H-B daily TSMOM long-short | 5 sessions | 1,848 | +35.38 | +33.38 [-0.12, +66.88] | 1,146 | +24.87 | +22.87 [-11.17, +56.90] | +1.32 | cannot be distinguished from no edge |" — AiTrader/RETURN.md:3472. n = 1,146 holdout trades (1,848 fit); registered bar |z| ≥ 2.39 (AiTrader/RETURN.md:3447).
  - The session names its only accepted remedy and declares it unavailable in this database — AiTrader/RETURN.md:3485 — where the database is the 8-symbol, 2026-selected deep-history load whose selection bias the same session states: "the 2026-chosen universe overweights past uptrends, biasing the long side up and the short side down" — AiTrader/RETURN.md:3451.
  - **The stated blocker expired the same day, eighteen hours later.** `git -C <live AiTrader> log`: `4ec2933 2026-07-26 00:32:09 -0700 Pre-registered hypothesis research against deep history` (the H-A/H-B/H-C session) precedes `a2f7c94 2026-07-26 18:43:03 -0700 Load a broad hindsight-free equity universe into the analysis database with survivorship and corporate-action handling`. Read 2026-09-05, read-only `git log`.
  - What the breadth load delivered is precisely the named remedy: "25,547,678 daily bars across 19,744 US equity tickers ... and 6,648 of those tickers are DEAD, each with an explicit end marker ... raised member deaths in 2023 and 2024 from ZERO to 35 and 31, and realised universe attrition from 1.12 to 2.17 percent per year" — AiTrader/RETURN.md:2985 (n = 19,744 tickers, 6,648 dead).
  - The very next round (`00c2d17`/`a0a9ef6`, 2026-07-26 19:14/19:26) used that universe for four NEW cross-sectional hypotheses (H-F..H-I) and did not re-run H-B; H-B is a time-series family, structurally distinct from all four (AiTrader/RETURN.md:2798-2804).
  - H-B is nonetheless counted as closed twice afterwards: "Six families are now resolved against buy and hold: the default stack, H-A, H-B, H-C, H-D, H-E" — AiTrader/RETURN.md:3234; and "**Seven families are now resolved against buy and hold with zero survivors**" — AiTrader/RETURN.md:2968.
  - The strongest signal in H-B sits exactly where the disclosed bias predicts, which is why the survivorship-free re-run matters rather than being a formality: "Holdout long side +55.8 net (z=2.56, secondary), short side -18.7 (z=-0.67)" — AiTrader/RETURN.md:3477.
- **Recomputation:** none required; the finding is an ordering and coverage fact, not an arithmetic one. Inputs: AiTrader/RETURN.md:3472 (z 1.32, n 1,146), AiTrader/RETURN.md:3485 (the blocker), git commit timestamps of `4ec2933` and `a2f7c94`.
- **What would resolve it:** re-run H-B's specification unchanged against `universe_membership` under the corrected `U-LIQ-500-stk-w60-m40-p5` rule with a fresh pre-registration and a holdout not previously read for this hypothesis; or amend the tally at AiTrader/RETURN.md:2968 and :3234 to read "five resolved, H-B undecided pending a survivorship-free re-run".
- **Confidence:** HIGH — the blocker is quoted verbatim, its expiry is a git object, and no later RETURN.md entry re-tests H-B.
- **Invalidated by later commits?:** no — every commit after 2026-07-29T20:18 on this branch is a collection-log append (`f819b68` is the last code session), so no later session could have re-run H-B.
- **Disclosed by authors?:** no — the report discloses H-B's selection bias and states the remedy, but nothing anywhere records that the remedy arrived and was not used, and both later tallies count H-B as resolved without qualification.

---

### AUDIT-A-AiTrader-5
- **Repository / SHA:** AiTrader / 705e0ed128b7e184be6c1a23dcd06750c524c525
- **Hypothesis or artifact:** H-H, low idiosyncratic volatility (cross-sectional round, 2026-07-26, `a0a9ef6`) — disqualified by its own report and still counted as a resolved family
- **Direction:** A
- **Class:** INTERNAL_INCONSISTENCY
- **Severity:** S2
- **Label:** READ
- **Claim challenged (verbatim quote):** "3. **Seven families are now resolved against buy and hold with zero survivors**: the default stack, H-A, H-B, H-C, H-D, H-E, and now the cross-sectional family in four variants." — AiTrader/RETURN.md:2968
- **Evidence:**
  - The same document disqualifies one of those four variants in its verdict list: "**H-H, low idiosyncratic volatility: FAILS, and is separately DISQUALIFIED by a disclosed defect.** Holdout point estimate is negative at z equals -0.086 with capacity -157 USD per year. See the disclosure below: 51 of its 124 books contain an S&P 500 index ETF." — AiTrader/RETURN.md:2923.
  - The mechanism is definitional, not incidental: "SPLG, an S&P 500 index ETF, appears in **51 of H-H's 124 five-name books** and in 57 of its wide books. An index fund has near-zero idiosyncratic volatility against SPY BY CONSTRUCTION, so a low-IVOL ranking selects it almost by definition." — AiTrader/RETURN.md:2932. Contamination by hypothesis: H-F 0 of 115 books, H-I 0 of 115, H-G 1 of 124, **H-H 51 of 124**. Deciding figure: holdout excess −0.25 bp/day, 95 % CI [−5.9, +5.4], z −0.086, n = 31 holdout months / 2.55 years (AiTrader/RETURN.md:2861).
  - The universe classifier was corrected the same day, so the enabling condition for a valid re-test exists in the anchored tree: "distinct names | 1,187 | **1,218** ... funds remaining in membership | 6 vehicles, 150 months | **0** ... unclassified in membership | admitted silently | **0**" — AiTrader/RETURN.md:2706-2709 (`d6ad37a`, 2026-07-26 20:58, 92 minutes after `a0a9ef6`).
  - The correction session registers the reopen condition explicitly and no round is ever run under it: "4. **Any future round uses the corrected universe from a fresh pre-registration.** Prior and future results are not comparable across the correction and must not be pooled." — AiTrader/RETURN.md:2729. RETURN.md contains no later hypothesis round of any kind.
  - The correction session also refuses to re-score, correctly, and hands the obligation forward: "**No hypothesis result was recomputed.** ... Re-scoring H-F, H-G, H-H or H-I against a universe corrected after their outcome was seen is precisely the contamination that round's discipline prevented" — AiTrader/RETURN.md:2723.
- **Recomputation:** contamination share from AiTrader/RETURN.md:2923 and :2932 — 51 of 124 five-name books contain SPLG = **41.1 %** of H-H's formation books; at equal weight that is **8.2 %** of all H-H book-months held in an S&P 500 tracker. Inputs are figures printed in the document, so this finding is labelled READ. Script `/home/kiros-li/.cache/program-audit/scratchpad/work/agentA-AiTrader-p2/recompute.py`.
- **What would resolve it:** run H-H's unchanged specification once against the corrected `universe_membership` under a fresh pre-registration, as AiTrader/RETURN.md:2729 already requires; or amend the tally at AiTrader/RETURN.md:2968 to exclude a hypothesis its own verdict list calls disqualified.
- **Confidence:** HIGH — both quotes are in one document, and the corrected universe exists at the anchor.
- **Invalidated by later commits?:** no — no later commit runs a hypothesis round.
- **Disclosed by authors?:** partly, and stated plainly. The contamination and the disqualification are fully disclosed at AiTrader/RETURN.md:2923 and :2932, and the reopen condition is registered at :2729. What is not disclosed anywhere is that a hypothesis the same report labels DISQUALIFIED is then counted inside "seven families ... resolved ... with zero survivors" (AiTrader/RETURN.md:2968), and that the enabling correction landed the same evening and was never used.

---

### AUDIT-A-AiTrader-6
- **Repository / SHA:** AiTrader / 705e0ed128b7e184be6c1a23dcd06750c524c525
- **Hypothesis or artifact:** council confidence calibration (Task 2 of "Ask the recorded council calls what else they knew", 2026-07-27, `958cfcb`) — declared not practically settleable
- **Direction:** A
- **Class:** OVER_CLOSED
- **Severity:** S2
- **Label:** READ
- **Claim challenged (verbatim quote):** "WHAT WOULD SETTLE IT: with a bootstrap standard deviation of 0.0541 at 80 clusters, reaching the corrected bar at the observed rho needs **1,149 clusters, 14.4 times the current sample**. There are not 1,149 liquid instruments this system can evaluate, so the question is not practically settleable at this effect size." — AiTrader/RETURN.md:2221
- **Evidence:**
  - Deciding figures: pooled Spearman rho +0.0357, cluster-bootstrap interval [−0.067, +0.145], z 0.660, n = 274 scorable directional calls across 80 symbol clusters — AiTrader/RETURN.md:2217, :2187.
  - The instrument-count premise is contradicted by this repository's own universe tables, loaded the previous day: "25,547,678 daily bars across **19,744** US equity tickers" — AiTrader/RETURN.md:2985; membership "124 formation dates, **1,187** distinct names" (AiTrader/RETURN.md:2808), corrected to "**1,218**" distinct names across 3,076 member-months (AiTrader/RETURN.md:2706); eligible pool at the 2026-01-02 formation "**9,999**" (AiTrader/RETURN.md:744).
  - The successor experiment, specified two days later, draws its band from the same store: "band 1,558 members from a 9,613-symbol eligible pool" (AiTrader/RETURN.md:439) and, at the derived 10.00 price floor, "2,769" members at 2026-01-02 (AiTrader/RETURN.md:643). Every one of these counts exceeds 1,149.
  - The wide run had already demonstrated that scaling clusters is mechanical: it went from 9 clusters to "**distinct symbol clusters evaluated | 90** (21 crypto, 69 equity)" by rank-stratifying the top-500 book, at a realised spend of "**Real spend 10.87 USD against the 120 USD ceiling**" — AiTrader/RETURN.md:2406, :2397.
  - The same programme's own settling arithmetic prices clusters, not instruments: "establish a 50 bp effect | 66 clusters | 272 directional calls | ... | **509** evaluations | **85.39 USD**" — AiTrader/RETURN.md:2618, and it says explicitly "**THE MONEY IS NOT THE CONSTRAINT.** ... The binding constraint is SYMBOL DIVERSITY" — AiTrader/RETURN.md:2622.
- **Recomputation:**
  - Inputs: rho = 0.0357 and bootstrap SD = 0.0541 at g = 80 clusters (AiTrader/RETURN.md:2221, :2217); bar |z| ≥ 2.50 (AiTrader/RETURN.md:2155); scaling 509 evaluations per 66 clusters and 85.39 USD (AiTrader/RETURN.md:2618); realised 389 evaluations for 10.87 USD (AiTrader/RETURN.md:2403, :2397). All inputs are figures printed in the document, so the finding is labelled READ.
  - Method: SD(g) = 0.0541 × sqrt(80/g); solve rho/SD(g) = 2.50. Script `/home/kiros-li/.cache/program-audit/scratchpad/work/agentA-AiTrader-p2/recompute.py`.
  - Result: **g = 1,148 clusters** — the repository's 1,149 is arithmetically correct and is not disputed. Implied evaluations 1,148 × (509/66) = **8,855**. Cost at the session's own planned rate (85.39/509 = 0.1678 USD/eval) = **1,486 USD**; at the rate actually realised in the wide run (10.87/389 = 0.0279 USD/eval) = **247 USD**. So the recorded blocker ("there are not 1,149 liquid instruments") is false against this repository's own data, and the true blocker is a 250–1,500 USD spend plus a wider 5-minute bar pull — materially weaker than "not practically settleable".
- **What would resolve it:** restate the limitation as what it is (a spend and bar-coverage cost, quantified), or run the confidence-ordering test at the width the universe tables already support.
- **Confidence:** HIGH — the cluster arithmetic reproduces exactly, and the contradicting instrument counts are in the same repository one day earlier and two days later.
- **Invalidated by later commits?:** no — the universe tables and the news-experiment band both post-date the claim and are present at the anchor; nothing after 2026-07-29 is a code session.
- **Disclosed by authors?:** no. The session discloses the sample's other limits at length ("80 clusters over two days in one market regime, with GPT-5.5 absent from the entire equity half, cannot exclude a small effect" — AiTrader/RETURN.md:2274) but the instrument-count claim is stated as a fact and is not qualified anywhere.

---

### AUDIT-A-AiTrader-7
- **Repository / SHA:** AiTrader / 705e0ed128b7e184be6c1a23dcd06750c524c525
- **Hypothesis or artifact:** AMENDMENT 2's supersession of the 5.00 USD eligibility price floor by 10.00 USD, and the registered reversal condition that is supposed to keep it checkable
- **Direction:** A
- **Class:** OVER_CLOSED
- **Severity:** S2
- **Label:** DERIVED
- **Claim challenged (verbatim quote):** "**What would make 5.00 correct again:** evidence that the effect is concentrated in 5 to 10 USD names strongly enough to outweigh a doubled tick cost. That is measurable once data exists, by scoring the excluded 5-to-10 band separately, and `median_close_at_formation` is recorded so the check stays available." — AiTrader/EXPERIMENT.md:1091-1095
- **Evidence:**
  - The collector rejects every sub-10.00 symbol **before the band is formed and before any query is issued**: `if med_close < spec.MIN_MEDIAN_CLOSE:` / `reject("below_price_floor")` — AiTrader/news_experiment/universe.py:163-164, with `MIN_MEDIAN_CLOSE = 10.00        # AMENDMENT 2, derived from the tick's cost` at AiTrader/news_experiment/spec.py:39. Rejected symbols never reach `members`, so they are never sampled (AiTrader/news_experiment/universe.py:187-196) and never queried.
  - The magnitude at the operative formation: "rejections {'fund': 5387, 'below_price_floor': **3042**, 'thin_window': 724, 'unclassified': 33, 'listing_segment_break_in_window': 8, 'outside_adv_band': 2419}" — AiTrader/COLLECTION_LOG.md:30 (formation 2026-07-01; n = 12,613 symbols enumerated, summing the six rejection buckets plus the 1,558 members). Those 3,042 symbols produce zero rows, and `median_close_at_formation` on every row that does exist is ≥ 10.00 by construction. The excluded 5-to-10 band is therefore not scoreable separately from the collected data; it is scoreable only from a second collection under a different rule — which is exactly what "the check stays available" is written to deny.
  - Collection has been running against this rule since 2026-07-29 and has accrued 18 collection days, 10,113 symbol-day rows and 2,320 model calls (summed from AiTrader/COLLECTION_LOG.md:117-277), so the closed reopen path is not hypothetical: roughly a third of the day-cluster floor has already been collected under it.
  - The closure this reopen condition guards is one the document itself flags as costly and non-random: "its removals are **concentrated in exactly the population the hypothesis is about**" — AiTrader/EXPERIMENT.md:98-99; "At 10.00 the removal is 15.8 percent of S4 against 5.2 percent of S1." — AiTrader/EXPERIMENT.md:875-876; "**THE HONEST RESIDUAL:** ... **If a later reading decides the mechanism matters more than the dispersion, the correct response is to lower the floor and accept the worse hurdle**" — AiTrader/EXPERIMENT.md:885-890. That "later reading" is precisely the reading the recorded data cannot support.
  - The lever the amendment traded the population away for is now recorded as spent: "the price-floor lever is exhausted, since measured bp spread is roughly flat across the band's prices" — AiTrader/EXPERIMENT.md:266-267 and :2674-2678. So the floor's justification weakened after the tick measurement while the reversal path stayed closed.
- **Recomputation:** none needed beyond the code path; the claim is falsified by construction. Recorded for scale: 3,042 of the 12,613 symbols enumerated at the 2026-07-01 formation are rejected on the price floor (AiTrader/COLLECTION_LOG.md:30), i.e. **24.1 % of the enumerated pool is placed permanently out of reach of the registered check** (n = 12,613).
- **What would resolve it:** strike the sentence and record that reversing Amendment 2 requires a new collection under its own pre-registration; or extend the collector to *record* (not score) a control sample of 5-to-10 USD symbols with `state` and `median_close_at_formation` written, which keeps the check literally available at the cost of a few dollars of model calls at the measured $0.000465 per call (AiTrader/EXPERIMENT.md:1224).
- **Confidence:** HIGH — the rejection precedes sampling in the shipped collector and the rejection count is in the collection log.
- **Invalidated by later commits?:** no — `news_experiment/universe.py` and `EXPERIMENT.md` are unchanged after 2026-07-29; the only post-2026-07-29 commits are `COLLECTION_LOG.md` appends and two `.gitignore` lines.
- **Disclosed by authors?:** no — EXPERIMENT.md states the opposite, that the check "stays available", and no amendment, open question or audit entry records that the universe rule forecloses it.

---

### AUDIT-A-AiTrader-8
- **Repository / SHA:** AiTrader / 705e0ed128b7e184be6c1a23dcd06750c524c525
- **Hypothesis or artifact:** the `discovery` funnel / watchlist layer, recorded as dormant with a known structural blocker (the conviction floor)
- **Direction:** A
- **Class:** STATISTICAL
- **Severity:** S2
- **Label:** DERIVED
- **Claim challenged (verbatim quote):** "**`discovery` funnel. Do not remove, but stop carrying it as if it works. Confidence medium.** The conviction floor sits above what the pipeline produces, so the watchlist has never gained a member on merit (PROGRESS.md:103). It is dormant with a known blocker, not sound-and-waiting." — AiTrader/AUDIT.md:90
  (The same closure is stated with its n at AiTrader/PROGRESS.md:103: "**The discovery conviction floor sits above what the pipeline produces, and it blocks the whole layer.** `discovery/evaluate.py` passes `council_min_confidence` (0.60, the TRADING gate's threshold) as `conviction_floor`. Seven real council verdicts across two days measure 0.5265 to 0.5938. None cleared it. ... Nothing downstream of Stage C can work until this is decided. No dependencies.")
- **Evidence:**
  - The deciding sample is n = 7: "Seven real council verdicts across two days measure 0.5265 to 0.5938. None cleared it." — AiTrader/PROGRESS.md:103. The observed maximum misses the floor by 0.0062, i.e. **1.03 % of the floor**.
  - The floor is not a discovery-derived value; it is the trading gate's council threshold re-used verbatim: `conviction_floor: float = 0.60,` — AiTrader/discovery/evaluate.py:72; passed at AiTrader/discovery/evaluate.py:339 as `conviction_floor=council_min_confidence(cfg_path)`; the value is `council_min_confidence: 0.6` at AiTrader/config/default_config.yaml:281. The repository records the mismatch as unresolved, not as evidence: "the discovery layer's separate floor mismatch (0.60 passed as a conviction floor against measured council confidences of 0.53 to 0.59) is a recorded open flag, not a precedent" — AiTrader/EXPERIMENT.md:653-655.
  - **One candidate did exceed the floor on the council's own number and was pushed below it by an untrained factor:** "ADA/USD had council confidence 0.6026, above the floor, and the advisory adjustment of -0.066 pushed it to 0.5366. An untrained advisory factor should not be able to veto." — AiTrader/PROGRESS.md:104, where `dnn_bias` measured −0.31 to −0.34 "on all 12 symbols ever evaluated and never once positive" (n = 12 symbols). So the blocking mechanism recorded as "the floor sits above what the pipeline produces" is at least partly a synthetic DNN veto, which the same flag says must be settled after the floor, not before.
  - The blocker has been live in code for 37 days at the anchor, recorded reported-not-fixed on 2026-07-18 ("Reported, deliberately NOT fixed (that session was diagnosis only)" — AiTrader/PROGRESS.md:101) and, unlike five sibling flags in the same block, never struck through or annotated CLEARED (compare AiTrader/PROGRESS.md:105-:108).
  - The funnel's own volume shows the decision matters: Stage A 5,605, Stage B 1,929, **Stage C 394** (AiTrader/DATA_AUDIT.md:191), against only 7 candidates that ever reached a council verdict.
  - Corroboration from a larger, independent sample that the floor is high relative to the distribution: "No council verdict in the record reaches conviction 0.65, which is the 0.60 discovery floor problem seen from the other side." — AiTrader/PROGRESS.md:800 (75 evaluations).
- **Recomputation:**
  - Inputs: k = 0 clears of n = 7 verdicts; observed range 0.5265 to 0.5938; floor 0.60 (all AiTrader/PROGRESS.md:103). Stage-C volume 394 (AiTrader/DATA_AUDIT.md:191). Floor provenance read from code (AiTrader/discovery/evaluate.py:72, :339; AiTrader/config/default_config.yaml:281), which is why this finding is DERIVED rather than READ.
  - Method: Clopper-Pearson exact 95 % interval on a 0/7 binomial; and a normal fit using the range-based dispersion estimate for n = 7 (d2 = 2.704) with the midrange as location, giving P(verdict ≥ 0.60). Script `/home/kiros-li/.cache/program-audit/scratchpad/work/agentA-AiTrader-p1/discovery.py`.
  - Result: **Clopper-Pearson 95 % CI on the pass rate = [0, 0.410].** Range-based σ̂ = 0.0249, midrange 0.5601, z-to-floor 1.60, **implied pass rate 5.5 %**; the probability of observing 0 of 7 at that rate is **0.675**, i.e. entirely unsurprising. At a 5.5 % rate the 394 recorded Stage-C candidates would have yielded about **22 watchlist members**; at the interval's upper bound, 161. The sample cannot distinguish "the floor sits above what the pipeline produces" from "about one verdict in eighteen clears it".
- **What would resolve it:** score a further ~30 Stage-C candidates through the council under the existing 12-calls/day discovery budget (AiTrader/WEEKLOG.md:58) and report the realised distribution of conviction against the 0.60 floor; or state the floor's provenance in AUDIT.md and downgrade "known blocker" to "an inherited threshold missed by 1 percent on seven observations". Either is the one-line, dependency-free decision the flag itself calls for.
- **Confidence:** HIGH — the shortfall, the n and the floor's provenance are quoted from the record and read from code, and the binomial and range-based recomputations agree that 0/7 carries almost no information at this margin.
- **Invalidated by later commits?:** no — `discovery/evaluate.py`, the config value and AUDIT.md are unchanged after 2026-07-29.
- **Disclosed by authors?:** partially. The *mismatch* is disclosed as "a recorded open flag, not a precedent" (AiTrader/EXPERIMENT.md:653-655), the n is given at AiTrader/PROGRESS.md:103, and the DNN veto is flagged at :104. What is not disclosed anywhere is that 0 of 7 at a 1.03 % shortfall does not support a *structural* blocker; AiTrader/AUDIT.md:90 states the structural version without the n.

---

### AUDIT-A-AiTrader-9
- **Repository / SHA:** AiTrader / 705e0ed128b7e184be6c1a23dcd06750c524c525
- **Hypothesis or artifact:** industry/sector momentum, rejected before testing in the cross-sectional round's pre-registration (2026-07-26, `00c2d17`); and the same blocker as it constrains the wide council run's independence design
- **Direction:** A
- **Class:** OVER_CLOSED
- **Severity:** S2
- **Label:** DERIVED
- **Claim challenged (verbatim quote):** "| Industry or sector momentum | UNTESTABLE. No sector classification in the database. |" — AiTrader/RETURN.md:2787
- **Evidence:**
  - The rejection is a data-availability closure taken before any computation, in a table headed "REJECTED BEFORE TESTING, for missing data or missing mechanism, recorded per the rule" — AiTrader/RETURN.md:2781 (n = 8 pre-test rejections in this round).
  - The same blocker is carried into the wide council run's design two days later: "The database carries NO sector classification (recorded by the cross-sectional round), so cross-sector independence is approximated by stratifying the full liquidity distribution rather than claimed from a sector table." — AiTrader/RETURN.md:2353; repeated as disclosure 7 at AiTrader/RETURN.md:2488.
  - **An alternative source was already integrated in this repository and is demonstrated resolving sector two days later:** "`universe_asset` has **no sector column** so sector comes from Finnhub with `sector_source` recording absence (44/47 resolved, 3 `unresolved`)." — AiTrader/RETURN.md:437 (n = 47 symbols, 44 resolved = 93.6 %).
  - The implementation is eighteen lines and uses an endpoint the repo's Finnhub client already exposes: `def fetch_sector(client, symbol: str) -> tuple[str | None, str]:` calling `client._get("stock/profile2", {"symbol": symbol})` and reading `finnhubIndustry`, returning `(None, "unresolved")` or `(None, "absent_in_source")` rather than guessing — AiTrader/news_experiment/collect.py:163-180; persisted as `sector`/`sector_source` at AiTrader/news_experiment/store.py:62-63.
  - Finnhub was integrated in this repository since 2026-07-15/16, well before the rejection: the discovery client is described as "quotes, company news, pre-computed news sentiment, basic fundamentals, analyst ratings, and the earnings calendar" (AiTrader/discovery/finnhub_source.py:4), the key has a Settings field and a keystore credential (AiTrader/RETURN.md:6816), and a live health check confirmed it working at 107.8 ms (AiTrader/RETURN.md:6631).
  - The cost is bounded and measured in the repo's own terms: "~400 symbol-day queries per trading day, which is under 7 minutes against the integrated Finnhub 60/min free tier" — AiTrader/RETURN.md:1225. A one-off sector pull for the 1,218 distinct universe members is a fraction of that.
- **Recomputation:** none. The claim is that a named-in-repo alternative source existed; the evidence is the shipped code path.
- **What would resolve it:** resolve `finnhubIndustry` once for the 1,218 distinct `universe_membership` names (or state why an issuer-level, largely time-invariant classification cannot be used point-in-time when a fund classification already is, AiTrader/RETURN.md:3001), then either run the sector-momentum hypothesis under a fresh pre-registration or record the rejection on a mechanism ground rather than a data ground.
- **Confidence:** HIGH — the blocker quote and the working code path are both in the anchored tree, and the code path post-dates the blocker by two days in the same repository.
- **Invalidated by later commits?:** no — `news_experiment/collect.py` is present at the anchor and no later commit removes it; every post-2026-07-29 commit is a collection-log append.
- **Disclosed by authors?:** no — the sector gap is disclosed repeatedly (AiTrader/RETURN.md:2353, :2488, :2787), but nowhere is it recorded that the repository's own Finnhub client answers it, and the sector rejection was never revisited after `fetch_sector` shipped.
- **Scope note, so this is not read wider than it is:** the same table also rejects Value and Size for "No fundamentals" / "No shares outstanding" (AiTrader/RETURN.md:2785-2789). Finnhub `stock/metric` fundamentals are likewise integrated (AiTrader/discovery/finnhub_source.py:80, :335). Those two are **not** raised, because a free-tier fundamentals snapshot is a present-day value and a 2016-2026 cross-sectional backtest needs point-in-time fundamentals; that objection is real even though the repository did not state it. Sector is different: `finnhubIndustry` is an issuer property the repository already treats as time-invariant for the analogous fund classification.

---

### AUDIT-A-AiTrader-10
- **Repository / SHA:** AiTrader / 705e0ed128b7e184be6c1a23dcd06750c524c525
- **Hypothesis or artifact:** "the council predicts price", closed 2026-07-27 by the wide council run (274 scorable directional calls, 80 symbol clusters), and the boundary clause the closure is stated with
- **Direction:** A
- **Class:** OVER_CLOSED
- **Severity:** S2
- **Label:** DERIVED
- **Claim challenged (verbatim quote):** "**WHAT IS AND IS NOT CLOSED.** The interval admits roughly plus or minus 22 bp, and 22 bp survives neither the 50 bp crypto round trip nor the 2,500 USD capacity floor at Level 1 sizing. So the question is closed for anything this system could trade, and open only for effects too small to matter." — AiTrader/PROGRESS.md:788
  (Carried forward without its scope clause into the audit's headline recommendation: "Seven hypothesis families are dead against buy-and-hold-after-costs, the council does not predict price at any size this system could trade, and the honest boundary is drawn: an effect small enough to survive the intervals would clear neither the 50 bp crypto round trip nor the 2,500 USD capacity floor (PROGRESS.md:206, CONTEXT.md:58-60)." — AiTrader/AUDIT.md:154, which then recommends "Continuing to test price-based hypotheses at Level-1 sizing is not worth doing".)
- **Evidence:**
  - The deciding figures: "274 scorable directional calls across 80 symbol clusters, clearing the pre-registered floor of 272 calls and 66 clusters. Pooled excess over the unconditional move is -0.5 bp per call at z equals -0.046, interval [-22.5, +21.4], hit rate 50.0 percent to one decimal place. The interval EXCLUDES the 50 bp effect the design was powered to detect." — AiTrader/PROGRESS.md:775 (n = 274 calls / 80 clusters); the same figures at AiTrader/AUDIT.md:16.
  - **Leg 1 (the 50 bp crypto round trip) was superseded the same day**: scope narrowed to US equities at the universe layer (AiTrader/PROGRESS.md:576; AiTrader/CONTEXT.md:84), and the traded tier's measured round trip is "roughly 0.5 to 0.9 bp" (AiTrader/CONTEXT.md:84 bracketed correction 2026-07-29; AiTrader/PROGRESS.md:211, :235; AiTrader/AUDIT-2026-07-29.md:33). Commit ordering from git objects: council run `959a295` 2026-07-27T12:41:21-07:00; scope narrowing `8fd9fbf` 2026-07-27T18:55:32-07:00 (`git -C <live> log --date=iso-strict -- PROGRESS.md`, read 2026-09-05).
  - **Leg 2 (the capacity floor "at Level 1 sizing") was superseded 8 h 44 m later the same day** by commit `82e8e72` (AiTrader/PROGRESS.md:503, :191) and recomputed by this repository at 4.96 bp (AiTrader/PROGRESS.md:189, :256, :272). The capacity requirement the sentence invokes is stated twice in the specification: "at the sizer, 2,000 USD: 2,500 / (2,520 x 2,000) = **4.96 bp**" and "at the ceiling, 2,500 USD: ... = 3.97 bp" (AiTrader/EXPERIMENT.md:1870-1871), against "required net edge = 2,500 / 1,260,000 = **19.8 bp** per trade" in force when the council session ran (AiTrader/EXPERIMENT.md:1876).
  - **The originating session scoped the claim correctly and the audit dropped the scope:** "Does the evidence now show the council predicts subsequent price movement? **NO, at the scale this session was designed to detect.**" — AiTrader/RETURN.md:2472. AUDIT.md:154 restates it without the scope clause.
  - The expansion that would power the negative against the bar actually in force was affordable inside the ceiling that session already held: real spend 10.87 USD against a hard 120 USD ceiling (AiTrader/PROGRESS.md:773; AiTrader/RETURN.md:2397).
- **Recomputation:**
  - Inputs: interval [−22.5, +21.4] around point −0.5 at z −0.046, 80 clusters / 274 calls (AiTrader/PROGRESS.md:775; AiTrader/AUDIT.md:16); bars 50 bp, 19.8 bp, 4.96 bp, 3.97 bp (AiTrader/EXPERIMENT.md:1870-1871, :1876); tier-1 equity round trip 0.5–0.9 bp (AiTrader/AUDIT-2026-07-29.md:33; AiTrader/CONTEXT.md:84). Two independent SE routes were used as a cross-check. Scripts `/home/kiros-li/.cache/program-audit/scratchpad/work/agentA-AiTrader-p1/recompute.py` and `/home/kiros-li/.cache/program-audit/scratchpad/work/agentA-aitrader-p3/recompute.py`.
  - Method: (a) SE from the interval half-width / 1.95996, and independently from |point/z|; (b) subtract the equity cost hurdle from the interval's upper bound and compare against the enforced requirement and the 2,500 USD/yr floor; (c) minimum detectable effect at 80 % power, two-sided α = 0.05; (d) clusters required for each bar as 80·(SE/SE_needed)².
  - Result: half-width route **SE = 11.20 bp/call**; point/z route **SE = 10.87 bp/call** (normal-theory CI [−21.8, +20.8], matching the reported [−22.5, +21.4] to rounding). **MDE = 30.5 to 31.4 bp.** 50 bp lies outside the interval and needs only 32 clusters — that claim is sound. 19.8 bp lies **inside** the interval and needs **201 clusters (2.5x)**; 4.96 bp lies inside and needs **3,201 clusters (40x)**. Upper bound net of the tier-1 equity round trip = 21.4 − 0.5 = **20.90 bp** (20.50 bp at 0.9 bp cost), i.e. **4.2x the enforced 4.96 bp requirement**; in dollars at the enforced sizer, (21.4 − 0.7)/1e4 × 2,520 × 2,000 = **10,433 USD/yr against a 2,500 USD/yr floor (4.17x)**. The design cannot exclude anything between ~5 bp and ~30 bp, a range that is now economically material rather than "too small to matter". Narrowing it to a 10 bp MDE needs ~9.3x clusters ≈ 742 clusters / ~2,542 calls ≈ 101 USD at the run's realised 0.0397 USD/call — inside the run's own unspent 120 USD ceiling.
- **What would resolve it:** restate the closure's boundary against the enforced sizing and the US-equity cost hurdle — the honest form is "the point estimate is null and the interval excludes 50 bp; effects between ~5 and ~30 bp remain untested and are now economically material" — or run the cluster extension the same session's own scaling rule prices at roughly 100 USD. Restricting the negative to the crypto leg, where the 50 bp round trip does dominate the interval, would also resolve it.
- **Confidence:** MEDIUM — the point estimate is genuinely null and the pre-registered floor was met, so the *negative* stands; what is overstated is the boundary clause. The one load-bearing assumption is that one scored council call maps onto one hypothetical round trip over the same window; that is how the design was constructed, but it is stated here as an assumption rather than a verified equivalence.
- **Invalidated by later commits?:** no — no session commit landed after 2026-07-29, so neither AUDIT.md, PROGRESS.md nor the council figures moved before the anchor.
- **Disclosed by authors?:** partially. The originating session recorded "What this does NOT establish: that no effect of any size exists. The interval admits roughly plus or minus 22 bp" (AiTrader/RETURN.md:2474) and AiTrader/PROGRESS.md:755 lists the sample limits. But the same sentences dismiss such an effect on the superseded capacity arithmetic, AiTrader/AUDIT.md:154 carries the claim forward without the scope clause, and AiTrader/PROGRESS.md:211's stale-figure sweep declares no other figure overtaken. No document anywhere states that the interval's upper end sits above the enforced capacity requirement.

---

### AUDIT-A-AiTrader-11
- **Repository / SHA:** AiTrader / 705e0ed128b7e184be6c1a23dcd06750c524c525
- **Hypothesis or artifact:** the news-drift experiment's registered stop rule, its stated power margin, and Open Question 3's obligation to recompute rho and the residual volatility from collected data
- **Direction:** A
- **Class:** STATISTICAL
- **Severity:** S3
- **Label:** DERIVED
- **Claim challenged (verbatim quote):** "60 days x 107.7 = ~6,460 observations, 6.5x the requirement" — AiTrader/EXPERIMENT.md:2348
- **Evidence:**
  - The registered requirement is not 1,000 raw observations; it is 402 independent observations inflated by the day-clustering design effect: "Design effect for day clustering, k = 40 obs/day, rho = 0.05 post-benchmark: / DE = 1 + (k-1) * rho = 1 + 39*0.05 = 2.95 / n_required = 402 * 2.95 = 1,186" — AiTrader/EXPERIMENT.md:1798-1800.
  - Stage 1 superseded that k in the same document: "400 symbols x 0.359 x 0.75 surviving filters = **107.7 scorable/day**" — AiTrader/EXPERIMENT.md:2345-2346 (n = 200 symbols / 1,538 headlines behind the 0.359 arrival rate). The design effect scales with cluster size, so the requirement moves with it, and "6.5x" is computed against the raw 1,000 rather than the DE-corrected n.
  - The recomputation obligation is registered and unmet: "**The 180 bp residual volatility and the rho = 0.05 intra-day correlation are assumptions.** Both feed the required sample size. Both are computable from the collected data and both must be recomputed before the stop rule fires." — AiTrader/EXPERIMENT.md:2176-2178; and "**The realised `rho` is computed from the collected data and reported, and if it exceeds 0.05 the required n is recomputed and collection continues.** The stop rule is 'both thresholds met AND realised power adequate at the realised rho', never '1,000 reached'." — AiTrader/EXPERIMENT.md:1806-1810.
  - Data to do it with exists and has for weeks: 18 collected sessions, 10,113 symbol-day rows and 2,320 model calls between 2026-07-29 and 2026-08-21 (AiTrader/COLLECTION_LOG.md:117-277).
  - **No session has looked at any of it.** Verified against the live repository's git objects (read-only): the last substantive commit is `f819b68` 2026-07-29; every commit to the anchor — `8a49239` 2026-08-04, `f1fb308` 2026-08-06, `b5c2236` 2026-08-18, `705e0ed` 2026-08-24 — changes only `COLLECTION_LOG.md` (and two `.gitignore` lines in the last). `grep -n "^### 2026-08" PROGRESS.md` returns nothing.
  - Why this is Direction A rather than bookkeeping: the pre-registered powered-negative definition fires on the pooled interval at the 60-cluster floor (AiTrader/EXPERIMENT.md:1818-1823). Whether that negative deserves the word "powered" depends entirely on the realised rho, and the one margin figure in the document that would reassure a reader is overstated 2.6x.
- **Recomputation:**
  - Inputs: z_α/2 = 2.50, z_β = 0.84, σ = 180 bp, δ = 30 bp, rho = 0.05 (AiTrader/EXPERIMENT.md:1793-1801); k = 40 registered vs k = 107.7 measured (AiTrader/EXPERIMENT.md:1798, :2346). The "not done" leg rests on git objects, which is why the label is DERIVED.
  - Method: n_independent = (z_α/2 + z_β)²·(σ/δ)²; DE = 1 + (k−1)·rho; n_required = n_independent · DE; margin = 60·107.7 / n_required.
  - Result: n_independent = **402** (reproduces the document). At k = 40, DE = 2.950, n_required = **1,185** (reproduces the document's 1,186). At the measured k = 107.7, DE = **6.335**, n_required = **2,544** — 2.1x the registered figure. 60 clusters × 107.7 = 6,462 observations, so the true margin over the DE-corrected requirement is **2.54x, not 6.5x**. The design does still clear at 400 symbols, by 2.5x; the document's own suggestion that "the sample could fall to about 150 and still clear" (AiTrader/EXPERIMENT.md:2352-2354) leaves roughly 2.0x, not the headroom "6.5x" implies. Direction of the error: it overstates power, which is the direction that makes a future null easier to label "powered".
- **What would resolve it:** compute the realised rho and residual dispersion from the 10,113 rows already collected, report them beside the registered 0.05 and 180 bp, and restate the margin against the DE-corrected requirement rather than against the raw 1,000.
- **Confidence:** HIGH — the formula, its inputs and the measured k are quoted from the same document, and the arithmetic reproduces the document's own intermediate figures exactly.
- **Invalidated by later commits?:** no, and the silence is itself part of the evidence: the four commits between 2026-07-29 and the anchor touch nothing but the collection log. A session after the anchor could of course perform the recompute.
- **Disclosed by authors?:** partially — the obligation to recompute rho is disclosed (AiTrader/EXPERIMENT.md:1806-1810, :2176-2178). The specific arithmetic point, that "6.5x the requirement" is measured against the raw 1,000 rather than against the design-effect requirement the same document derives, is not disclosed anywhere.

---

### AUDIT-A-AiTrader-12
- **Repository / SHA:** AiTrader / 705e0ed128b7e184be6c1a23dcd06750c524c525
- **Hypothesis or artifact:** the news-drift experiment's start blocker — "the tick multiple is unmeasured" and "stage 3 stays blocked" — still stated in CONTEXT.md and still printed by the collector 26 days after the blocker was lifted and while collection has been running daily
- **Direction:** A
- **Class:** STALE_FIGURE
- **Severity:** S3
- **Label:** DERIVED
- **Claim challenged (verbatim quote):** "**It also refuses to start collecting**: `--run-kind collection` needs an explicit `--i-have-read-the-preconditions`, since the tick multiple is still unmeasured and its result may amend the cost model or the band." — AiTrader/CONTEXT.md:60
- **Evidence:**
  - Second stale blocker in the same document: "Consequence reported, not applied: the accepted news-drift specification survives at the median only in its liquid half (S1/S2), and stage 3 stays blocked on that operator decision." — AiTrader/CONTEXT.md:54.
  - The tick multiple was measured on 2026-07-29: "tier 3 = 8.0 and tier 4 = 9.0, MEASURED" over "1,402 rows kept of 1,440 cells over 157 symbols" across three sessions — AiTrader/PROGRESS.md:266, :270 (n = 1,402 symbol-session-window rows, 157 symbols).
  - Stage 3 was unblocked the same day: "**STAGE 3 IS NOW UNBLOCKED.** The tick multiple is measured, the amendment decision the measurement forced is made and recorded, and the specification no longer pre-condemns half its sample." — AiTrader/PROGRESS.md:258; reaffirmed "**STAGE 3 REMAINS UNBLOCKED.**" — AiTrader/PROGRESS.md:229, and "Collection still waits only on the operator's start command" — AiTrader/PROGRESS.md:197.
  - The collector still carries the expired reason in two places at the anchored SHA: module docstring "`--run-kind collection` is refused unless `--i-have-read-the-preconditions` is also passed, because the tick multiple is still unmeasured and its result may amend the cost model or the band" — AiTrader/news_experiment/collect.py:7-9; runtime refusal "REFUSING: collection has not been cleared to start. The tick multiple is unmeasured and its result may amend the cost model or the band (EXPERIMENT.md, Stage 1 verdict)." — AiTrader/news_experiment/collect.py:731-735.
  - Collection has in fact been running since 2026-07-29 and is running at the anchor: "start_utc: 2026-07-29T22:54:53Z" (AiTrader/COLLECTION_LOG.md:2), then 19 `action: collected` daily runs from "=== DAILY RUN 2026-07-30T22:30:45Z ===" (AiTrader/COLLECTION_LOG.md:117) to "=== DAILY RUN 2026-08-24T22:31:49Z ===" (AiTrader/COLLECTION_LOG.md:270), the last writing 433 rows for target session 2026-08-21 (AiTrader/COLLECTION_LOG.md:275). First collection wrote 427 rows over a 1,558-member band (AiTrader/COLLECTION_LOG.md:33, :36).
  - The status documents were never updated: `PROGRESS.md` "Current State" (AiTrader/PROGRESS.md:7) and its Session Log both stop at 2026-07-29, and every entry in the last week states "Collection has not started" / "NO COLLECTION DATA EXISTED" (AiTrader/PROGRESS.md:187, :217, :248, :276, :289). The four commits between 2026-07-30 and the anchor touch only `COLLECTION_LOG.md` and `.gitignore`.
- **Recomputation:** none required — this is a document-versus-record comparison. Counted 19 `action: collected` blocks in AiTrader/COLLECTION_LOG.md between lines 117 and 277 (read from the anchored snapshot; the live file carries one further uncommitted collector append, not read for content).
- **What would resolve it:** update AiTrader/CONTEXT.md:54 and :60 to record that the tick multiple was measured on 2026-07-29 and that stage 3 unblocked; rewrite the collector's refusal message to the current reason (an operator attestation), which AiTrader/PROGRESS.md:195 already recommends; and refresh PROGRESS.md "Current State" to reflect ~19 collected sessions.
- **Confidence:** HIGH — the measurement, the unblocking, the still-stale text and the running collection are each stated verbatim in files at the anchored SHA.
- **Invalidated by later commits?:** no — the only post-anchor motion is the collector appending to `COLLECTION_LOG.md`, which strengthens rather than weakens the finding.
- **Disclosed by authors?:** partially — AiTrader/PROGRESS.md:195 discloses the collector's stale message ("its refusal message still cites the tick multiple as unmeasured, stale since the 2026-07-29 measurement, reported not changed"). The two stale blockers in CONTEXT.md and the four-week gap between the running collection and the status documents are not disclosed anywhere.

---

### AUDIT-A-AiTrader-13
- **Repository / SHA:** AiTrader / 705e0ed128b7e184be6c1a23dcd06750c524c525
- **Hypothesis or artifact:** AMENDMENT 1's supersession of the liquidity-rank universe rule by the absolute ADV band, and the robustness check registered to keep the superseded rule scoreable
- **Direction:** A
- **Class:** OVER_CLOSED
- **Severity:** S3
- **Label:** DERIVED
- **Claim challenged (verbatim quote):** "| `liquidity_rank` | INTEGER | rank at formation. Recorded but NOT the band variable, so the superseded rank rule stays scoreable as a pre-registered robustness check. |" — AiTrader/EXPERIMENT.md:2078
  (The same claim is written into the collector: "`liquidity_rank` means what the superseded rank rule meant and that rule / stays scoreable as a pre-registered robustness check (Task 8)." — AiTrader/news_experiment/universe.py:183-184.)
- **Evidence:**
  - The rank is indeed computed over the whole eligible pool before the band filter (AiTrader/news_experiment/universe.py:182-185), but the **band filter still removes every out-of-band symbol from `members` before sampling**: `stratum = spec.stratum_for(adv)` / `if stratum is None:` / `reject("outside_adv_band")` — AiTrader/news_experiment/universe.py:188-191. Only `members` are sampled and queried (AiTrader/news_experiment/universe.py:192-196 and the stratified draw below it).
  - At the operative formation the collector rejected **2,419** symbols as `outside_adv_band` — AiTrader/COLLECTION_LOG.md:30. None of them will ever carry an observation row.
  - The document's own overlap figures show how much of the rank rule that removes: "| **rank band members** | 3,501 | 3,501 | 3,501 |" and "| overlap, % of rank band | 53.4 | 67.2 | **87.3** |" — AiTrader/EXPERIMENT.md:941, :947; and "only 68 ADV-only symbols against **446 rank-only**" — AiTrader/EXPERIMENT.md:957 (n = 3,501 rank-band members).
  - The missing names are not a random slice: they are exactly the symbols on which rank and absolute ADV disagree, which is the entire content of the comparison the check is registered to make.
  - The same unreachability applies to the amendment's own reversal condition: "**What would reverse the amendment:** evidence that the effect tracks rank better than ADV. That is measurable once data exists, by scoring the same observations under both memberships" — AiTrader/EXPERIMENT.md:2304-2306. Scoring the same rows under two labels is possible; scoring the *rank rule* is not.
- **Recomputation:**
  - Inputs: rank band 3,501 members; overlap as a percentage of the rank band 53.4 / 67.2 / 87.3 at the 2020 / 2023 / 2026 formations (AiTrader/EXPERIMENT.md:941, :947). Code path read from AiTrader/news_experiment/universe.py.
  - Method: rank-band members never queried = 3,501 × (1 − overlap).
  - Result: **2026 formation: 3,056 queriable, 445 never queried (12.7 %)** — consistent with the document's own count of 446 rank-only symbols. 2023: 1,148 never queried (32.8 %). 2020: **1,631 never queried (46.6 %)**. The registered robustness check can examine at most 87.3 % of the superseded rule at the one formation in use, and would be blind to nearly half of it at an earlier formation.
- **What would resolve it:** restate the field note to what it supports ("`liquidity_rank` allows the rank *label* to be tested as an organising variable within the ADV band; the rank rule itself is not scoreable from this collection"), or extend the sample to the rank band's 446 exclusive members at the operative formation, which at the measured 0.359 headlines/symbol/day and $0.000465 per call costs a few dollars.
- **Confidence:** HIGH — the band rejection precedes sampling in the shipped collector, and the shortfall is computed from the document's own overlap table.
- **Invalidated by later commits?:** no — `news_experiment/universe.py` and EXPERIMENT.md are unchanged after 2026-07-29.
- **Disclosed by authors?:** no — the claim is asserted in EXPERIMENT.md Task 8 and repeated as a comment in the collector, and no amendment or open question records the limitation.

---

### AUDIT-A-AiTrader-14
- **Repository / SHA:** AiTrader / 705e0ed128b7e184be6c1a23dcd06750c524c525
- **Hypothesis or artifact:** Stage 1 Task 6, the model-capability comparison (`claude-haiku-4-5`, `claude-opus-4-8`, `gemini-3.1-pro-preview`, DeepSeek V4 Flash), and the two-condition collection-clearance precondition built on it
- **Direction:** A
- **Class:** PROCESS
- **Severity:** S3 (capped: the limitation is disclosed by the authors — see below)
- **Label:** READ
- **Claim challenged (verbatim quote):** "**The experiment is not cleared to collect, because the model comparison is unresolved and the tick multiple is unmeasured, and both are cheap to finish.**" — AiTrader/EXPERIMENT.md:2730-2732
  (The identical two-condition gate is stated in both other tracking documents: "**The experiment is NOT cleared to collect**, because the model comparison is unresolved and the tick multiple unmeasured. Both are cheap to finish: one RTH-timed script and one corrected comparison." — AiTrader/PROGRESS.md:401; and "**NOT answered:** whether capability matters, which must be redone before the cheap-tier decision." — AiTrader/RETURN.md:612.)
- **Evidence:**
  - Three of the four arms produced no usable data. n by arm: Haiku **21 of 21 parsed**, 52.4 % directional, $0.000403/call; Opus **0 scorable of 21** (100 % parse-fail); Gemini **n = 2** then latched EXHAUSTED; DeepSeek **n = 0**, no credential — AiTrader/EXPERIMENT.md:2422-2446; AiTrader/PROGRESS.md:400; AiTrader/RETURN.md:596-600.
  - Both failures are blockers, not model verdicts: "**THE OPUS RESULT IS MY BUG, NOT A MODEL FAILURE** ... Every call returned `HTTP 400: temperature is deprecated for this model`. My request sent `temperature: 0`. **Opus 4.8 was never tested.**" — AiTrader/EXPERIMENT.md:2438-2443. "**Gemini latched EXHAUSTED after 2 calls** on HTTP 429 with quota language" — AiTrader/EXPERIMENT.md:2445-2446.
  - **Both blockers expired inside this repository.** The Opus fix is now a recorded hard rule: "That is now a hard rule in CLAUDE.md so a later session does not lose calls to it." — AiTrader/EXPERIMENT.md:2138-2140; diagnosed at AiTrader/PROGRESS.md:384 and AiTrader/RETURN.md:539. The Gemini latch is a balance condition that had lifted once before ("**GEMINI HAS RECOVERED**" — AiTrader/RETURN.md:5360), and the experiment now runs on its own separately funded credential: "[credential] OWN KEY: resolved anthropic_experiment_key (source experiment), latch label 'anthropic_experiment'. Independent of the council balance." — AiTrader/COLLECTION_LOG.md:26-27; AiTrader/CONTEXT.md:62.
  - **Only one of the two clearance conditions was ever met.** "The named blocker, the tick multiple unmeasured, is CLEARED." — AiTrader/EXPERIMENT.md:2688-2689; the remaining block was then resolved as a *cost decision* by AMENDMENT 5 (AiTrader/PROGRESS.md:258), and the model comparison is mentioned in neither unblocking record. AMENDMENT 7's "START PRECONDITIONS, DOCUMENTED AS THEY ARE" (AiTrader/EXPERIMENT.md:657-682) enumerates five checks and the comparison is not among them.
  - Collection began anyway and ran to the anchor: start anchor 2026-07-29T22:54:53Z (AiTrader/COLLECTION_LOG.md:2), 18 collected sessions through target 2026-08-21, 10,113 symbol-day rows, 2,320 model calls, $1.2809 spent (summed from AiTrader/COLLECTION_LOG.md:117-277). No document records the precondition being waived, met or reconsidered.
- **Recomputation:**
  - Inputs: 21 headlines per arm (AiTrader/EXPERIMENT.md:2425); measured per-call costs haiku $0.000403, gemini $0.000559 (AiTrader/EXPERIMENT.md:2434-2436); Anthropic `claude-opus-4-8` published pricing $5.00/M input, $25.00/M output (AiTrader/RETURN.md:2385) against the document's own 290-input / 35-output token estimate (AiTrader/EXPERIMENT.md:1216-1218). All inputs are figures printed in the documents, consistent with the READ label.
  - Method: per-call cost × 21 per arm, summed.
  - Result: opus $0.002325/call; **the two missing-but-reachable arms cost $0.061 to run, all three arms $0.069.** The comparison the record calls "cheap to finish" is a seven-cent job that has stood undone for 27 days while $1.28 of collection ran past it (Stage 1's whole ceiling was 15.00 USD, of which 0.0096 USD was spent — AiTrader/PROGRESS.md:389).
- **What would resolve it:** re-run the fixed comparison set on the 21 recorded headlines with the `temperature` field omitted for Opus and Gemini on a funded key, report parse rate, directional rate and agreement with a multiple-comparison correction, and either record the precondition as met or amend it away explicitly so that "not cleared to collect" is not silently satisfied by meeting one of its two named conditions.
- **Confidence:** HIGH on the facts — the precondition, the expiry of both blockers and the collection start dates are all quoted from the record, and the cost is derived from the document's own measured rates. The practical stakes are bounded: the specification's verdict table already forbids reading a gross positive as "the model understands" (AiTrader/RETURN.md:167), so an untested Opus arm does not invalidate the primary.
- **Invalidated by later commits?:** no — no post-anchor commit re-runs the comparison; the collector is fixed on `claude-haiku-4-5` and the specification is binding.
- **Disclosed by authors?:** **yes, squarely and in all three documents**, which is why this finding is READ and capped at S3: AiTrader/EXPERIMENT.md:2721-2724 and :2734-2742; "**NO CLAIM IS MADE THAT HAIKU IS BETTER.** Stage 1 produced one usable arm out of four, so the capability question stays open and is recorded as open." (AiTrader/PROGRESS.md:359, repeated at :243); AiTrader/RETURN.md:480 and :506; and AiTrader/AUDIT-2026-07-29.md:176-179 ("nothing in the specification forces it closed"). What the record does not state is that both causes of the missing arms have since been removed inside this repository, that the remaining cost is seven cents, and that a two-condition clearance test was satisfied on one condition.

---

### AUDIT-A-AiTrader-15
- **Repository / SHA:** AiTrader / 705e0ed128b7e184be6c1a23dcd06750c524c525
- **Hypothesis or artifact:** the crypto removal from all trading paths (2026-07-27, `8fd9fbf`), and the cost comparison that justified it
- **Direction:** A
- **Class:** STALE_FIGURE
- **Severity:** S3
- **Label:** READ
- **Claim challenged (verbatim quote):** "Crypto round trips cost 50 bp against equity's 1.14 to 4.87 bp in the tradeable bands" — AiTrader/RETURN.md:1431
- **Evidence:**
  - That ratio is the lead justification for a scope decision that closed nine separate code paths and made crypto ineligible for entry at the universe layer (AiTrader/RETURN.md:1443-1467). It rests on the fee model's spread component, which at the time carried an explicitly unmeasured tick multiple: "`alpaca_equity_spread_tick_usd: 0.01` and `alpaca_equity_spread_tick_multiple: 1.0` ... **The multiple ships at 1.0, which is the floor, and the config says in writing that the model therefore understates small-cap spread by construction.**" — AiTrader/RETURN.md:1647.
  - Two days later the multiple was measured on consolidated SIP quotes and the equity side moved by roughly an order of magnitude in the band the successor experiment trades: "Round-trip hurdle (spread + 0.3 bp fixed): S1 16.1 med / 64.2 p90, S2 21.4 / 95.4, S3 30.9 / 121.4, S4 50.3 / 211.9. The one-tick floor said 2.4-5.1 bp: **understated 6.7x-9.9x**." — AiTrader/RETURN.md:249. Applied to the fee model as `tier3 = 8.0`, `tier4 = 9.0` — AiTrader/RETURN.md:251. n = 1,402 quote cells kept of 1,440, 157 of 160 symbols, 3 sessions (AiTrader/RETURN.md:234).
  - The repository notices the consequence and files it as a note rather than reopening the decision: "CLAUDE.md scope note corrected: 0.5 to 0.9 bp for the tier-1 names the engine trades, the superseded 1.14 to 4.87 recorded as the one-tick floor, **tier 4's measured 41.2 bp noted within 20 percent of crypto's 50**, conclusion stands on tier 1 with the reasoning recorded as narrowed." — AiTrader/RETURN.md:144.
  - The fee model already carries a crypto maker rate that was never used to re-cost the comparison: "Round trips the model returns: crypto taker 50.0 bp, **crypto maker 30.0 bp**, equity 1.3 bp." — AiTrader/RETURN.md:3394. Maker execution is named elsewhere as a live resolution path (AiTrader/RETURN.md:211).
  - The band that matters is the news experiment's: ADV 2.07M–65.3M (AiTrader/RETURN.md:715), i.e. exactly fee tiers 3 and 4.
- **Recomputation:**
  - Inputs: crypto taker RT 50.0 bp and maker RT 30.0 bp (AiTrader/RETURN.md:3394); equity band floors 3.15 and 4.87 bp (AiTrader/RETURN.md:1613-1614); measured equity tier 3 17.8 bp and tier 4 41.2 bp (AiTrader/RETURN.md:144, :251). All inputs are figures printed in the document, hence READ.
  - Method: ratio of crypto to equity round trip, per tier, before and after the measurement.
  - Result: the gap the removal cited collapses from **15.9x (tier 3) / 10.3x (tier 4)** to **2.8x / 1.2x**. Against the crypto **maker** rate the measured tier-4 equity round trip is **1.37x more expensive than crypto**. The removal's cost argument survives only for tier-1 mega caps (0.5–0.9 bp), which is the population the engine traded then and not the population the successor experiment is built on.
- **What would resolve it:** measure the tick multiple for tiers 1/2/5/6 with the same script (they remain "1.0 floors marked UNMEASURED" — AiTrader/RETURN.md:251) and re-state the crypto comparison per tier; or record explicitly in CLAUDE.md/CONTEXT.md that the crypto exclusion is now a tier-1 conclusion and carries no cost argument in the ADV 2.07M–65.3M band.
- **Confidence:** MEDIUM — the arithmetic is unambiguous, but the crypto removal had three independent legs (cost; the P26 split at −48.78 bp crypto vs −2.73 equity; council abstention 87–94 % on crypto vs 43–47 % on equity — AiTrader/RETURN.md:1431), and only the cost leg is affected.
- **Invalidated by later commits?:** no — the tick measurement and the CLAUDE.md correction both precede the anchor and no later commit revisits the scope decision.
- **Disclosed by authors?:** partly. The proximity of tier 4 to crypto is disclosed at AiTrader/RETURN.md:144 and AiTrader/PROGRESS.md:211, and the narrowing of the conclusion to tier 1 is recorded there. What is not recorded anywhere is that the deciding ratio moved by roughly an order of magnitude, that the crypto maker rate inverts it at tier 4, and that the band the successor experiment trades is precisely the affected one.

---

### AUDIT-A-AiTrader-16
- **Repository / SHA:** AiTrader / 705e0ed128b7e184be6c1a23dcd06750c524c525
- **Hypothesis or artifact:** the LLM council layer's remaining justification, closed 2026-07-27 (`958cfcb`)
- **Direction:** A
- **Class:** OVER_CLOSED
- **Severity:** S3 (capped: the coverage gap is disclosed by the authors — see below)
- **Label:** READ
- **Claim challenged (verbatim quote):** "Across three sessions the layer has now been measured on direction, on calibration, on abstention, on rejection, and on asset class, and nothing has been demonstrated on any axis. ... **No measured justification for the layer remains on this evidence.**" — AiTrader/RETURN.md:2274
- **Evidence:**
  - One of three providers contributed nothing at all to the equity half, which since the crypto removal the following day is the entire tradeable universe: "| gpt-5.5 | equity | 244 | **244** | not measurable | 0 | not measurable | not measurable |" — AiTrader/RETURN.md:2254; "all 244 calls errored on the quota exhaustion disclosed in the wide run" — AiTrader/RETURN.md:2256 (n = 244 calls, 244 failures).
  - The absent provider is the one the earlier record identifies as the only voice the council ever had: "**THE COUNCIL IS GPT-5.5.** All 22 evaluations carrying a directional council verdict had GPT-5.5 directional, and there are ZERO evaluations where GPT-5.5 was flat and the council was not." — AiTrader/RETURN.md:2531 (n = 22 directional verdicts). In the wide run its whole contribution is 19 scorable calls across 11 clusters, every one crypto — AiTrader/RETURN.md:2440, :2253.
  - The blocker is a funding state, not a technical one, and the repository says so: "This is **billing exhaustion on the operator's accounts**, not model behaviour" — AiTrader/RETURN.md:2419; the exhaustion latch "is process state and deliberately not persisted: **an account stays dry until it is funded**" — AiTrader/RETURN.md:2311.
  - The programme's own price for settling the direction question is small: "**THE MONEY IS NOT THE CONSTRAINT. Settling this costs between 8 and 85 dollars.**" — AiTrader/RETURN.md:2622; the wide run itself spent 10.87 USD (AiTrader/RETURN.md:2397).
  - The two providers that did answer the equity half disagree in sign at a magnitude the interval cannot separate: Opus −13.3 bp [−39.5, +12.9] (n = 148 calls, 72 clusters) against Gemini +18.6 bp [−7.3, +44.5] (n = 107 calls, 65 clusters) — AiTrader/RETURN.md:2438-2439.
- **Recomputation:** none. The finding is coverage, not arithmetic: the pooled primary (−0.5 bp, z −0.046, n = 274, 80 clusters — AiTrader/RETURN.md:2437) does not depend on GPT-5.5, but the per-provider and council-versus-member results do, and equity is now the whole universe.
- **What would resolve it:** fund the OpenAI account and re-run the equity half of the wide design (69 rank-stratified names, 4 rounds each, ~$30 at the realised rate), or restate the layer's verdict as "no measured justification on two of three providers in equity, the third structurally absent".
- **Confidence:** MEDIUM — the closure is hedged carefully by its own authors ("That is a statement about what has been measured, not a proposal" — AiTrader/RETURN.md:2274), and the pooled result is genuinely powered; the gap is real but narrower than the headline sentence suggests.
- **Invalidated by later commits?:** no — no later commit runs a council evaluation; the layer's weights were zeroed on 2026-07-27 (`deb51b7`) and the panels removed on 2026-07-29 (`f819b68`), both post-dating the closure.
- **Disclosed by authors?:** **yes, explicitly and prominently**, which caps this at S3: "(3) **GPT-5.5 is absent from the equity half entirely, so every figure involving it rests on crypto alone.**" (AiTrader/RETURN.md:2278) and "GPT-5.5's equity column is not measurable at all" (AiTrader/RETURN.md:2256), repeated at AiTrader/PROGRESS.md:753 and :755. What is added here is only that the blocker is a funding state the repository itself prices at $8–85, and that the asset class in which the provider is absent became the only tradeable class the following day.

---

### AUDIT-A-AiTrader-17
- **Repository / SHA:** AiTrader / 705e0ed128b7e184be6c1a23dcd06750c524c525
- **Hypothesis or artifact:** RETURN.md's own completeness rule, for the session that overturned the tick-multiple blocker (commit `e60232a`, 2026-07-28)
- **Direction:** A
- **Class:** PROCESS
- **Severity:** S4
- **Label:** DERIVED
- **Claim challenged (verbatim quote):** "Log every user prompt to RETURN.md before starting work, newest at top, recording the prompt, model, changes, and commit message." — AiTrader/CLAUDE.md:9
- **Evidence:**
  - `git -C <live AiTrader> log`: `e60232a 2026-07-28 14:39:07 -0700 Find a free consolidated quote source on the existing credential, correcting the paid-subscription conclusion, no amendment made`. `git show --stat e60232a` touches **PROGRESS.md only, 13 insertions**. Read 2026-09-05, read-only.
  - RETURN.md at the anchor contains no `## Prompt:` entry for that session; `grep -n "free consolidated quote\|paid-subscription\|delayed_sip"` over RETURN.md returns nothing matching it, against a file holding **141** `## Prompt:` entries (n = 141 logged sessions, 0 matching).
  - The session it omits is the one that lifted the programme's longest-standing blocker. The prior state was recorded as terminal: "**THE POSITION IS WORSE THAN BEFORE, STATED PLAINLY.** The multiple moved from 'unmeasured and one script away' to 'unmeasured and behind a paid data subscription'." — AiTrader/RETURN.md:418; "Establishing the tick multiple needs quote data, which needs a paid subscription" — AiTrader/RETURN.md:1637; "**The tick multiple remains the binding blocker** and is behind a SIP-entitled market-data subscription" — AiTrader/RETURN.md:308.
  - The `e60232a` commit message and its PROGRESS.md entry state the correction: "It is unmeasured and reachable for free ... an error message was read as broader than its wording, and one unprobed parameter separated a blocked question from an open one."
  - The finding does survive into RETURN.md indirectly, inside the next session's prompt summary at AiTrader/RETURN.md:224, which is why this is hygiene rather than a lost result.
- **Recomputation:** none.
- **What would resolve it:** add the missing `## Prompt:` entry for `e60232a` to RETURN.md, or amend AiTrader/CLAUDE.md:9 to say that a findings-only session may record to PROGRESS.md alone.
- **Confidence:** HIGH — the commit exists, its stat is one file, and RETURN.md has no matching entry.
- **Invalidated by later commits?:** no — no post-anchor commit adds the entry.
- **Disclosed by authors?:** no — nothing in RETURN.md or PROGRESS.md notes the missing entry.

---

### AUDIT-A-AiTrader-18
- **Repository / SHA:** AiTrader / 705e0ed128b7e184be6c1a23dcd06750c524c525
- **Hypothesis or artifact:** two entries in PROGRESS.md "Known Issues and Caveats" / "Open Flags" that describe limits lifted on 2026-07-27 and were never struck through
- **Direction:** A
- **Class:** STALE_FIGURE
- **Severity:** S4
- **Label:** READ
- **Claim challenged (verbatim quote):** "Remaining synthetic-mock cap: the RiskGate `required_model_agreement_count` gate (the momentum-biased mock advisory factors disagree with mean-reversion entries), a mock-data artifact a real council would not have, not the tuner." — AiTrader/PROGRESS.md:78
- **Evidence:**
  - The named artifact was removed on 2026-07-27: "`MockCatalystProvider` hashed the symbol string into a catalyst score and importance... The hash gave each symbol a fixed pseudo-random directional pull, so the mock advisory factors disagreed with mean-reversion entries in a way no real council would, and the disagreement count blocked entries." — AiTrader/CONTEXT.md:82; session record "The dead news mock was suppressing trades: removing it fixed tuner_floor, and ctest is 33 of 33 for the first time" — AiTrader/PROGRESS.md:557 (n = 33 ctest cases at that point).
  - The companion flag is stale in the same way: "**ctest `tuner_floor` FAILS at `3e4a684` and is not caused by the provenance change.** ... Until then the suite is 30 of 31 and the plateau claim in Known Issues above is not currently demonstrable by the test that pins it." — AiTrader/PROGRESS.md:122. `3e4a684` is 2026-07-27T16:41:25-07:00 and the fix `74f5636` is 2026-07-27T19:32:30-07:00, under three hours later (`git -C <live> log --date=iso-strict -- PROGRESS.md`, read 2026-09-05); ctest is **34 of 34** at the anchor (AiTrader/PROGRESS.md:7, :209).
- **Recomputation:** none.
- **What would resolve it:** strike both entries through with their resolution dates, as the same document does for every other cleared flag (e.g. AiTrader/PROGRESS.md:86, :87, :88, :105-:108).
- **Confidence:** HIGH — the resolutions are recorded in the same two files.
- **Invalidated by later commits?:** no.
- **Disclosed by authors?:** no — both entries sit in the un-struck part of "Known Issues" and "Open Flags", where every other resolved item carries a strike-through or a CLEARED annotation.

---

## What Agent A checked and found sound

This repository's measurement discipline is, on the whole, better than the thesis predicts. What
follows is where Direction A was hunted and did not hold, with what would have been expected if the
thesis held and what was found instead.

**Pre-registration and verdict discipline**

1. **AMENDMENT 5's refusal to restrict the band to the tier-3 floor** (AiTrader/EXPERIMENT.md:337-356; AiTrader/PROGRESS.md:246-256). This is the exact shape the thesis hunts — a thin, expensive stratum cut after a cost measurement — and the document goes the other way for three recorded reasons, keeps S3 and S4 in full, and pre-registers what would reverse it. The reasoning ("cost is a function of account size and execution quality, both of which can change, while the existence of a signal cannot") is correct, and the independent audit flagged the permissive direction of the call in writing (AiTrader/PROGRESS.md:237).
2. **The pre-registered verdict table** (AiTrader/EXPERIMENT.md:363-375), including the row that writes down the awkward likely outcome before any number exists. No verdict pre-commits to killing a hypothesis on a narrow miss; the abstention rows are generous rather than harsh.
3. **AMENDMENT 6's permutation confirmation** (AiTrader/EXPERIMENT.md:408-545). Checked specifically whether the added conjunctive bar could convert a real effect into a *negative*: it cannot. "The confirmation intercepts positives only" (:543-545), and an uninformative null produces an abstention (:536-540).
4. **The powered-negative definition** (AiTrader/EXPERIMENT.md:1818-1831). It requires the interval's upper bound to sit below the assumed effect *and* no primary to clear, and records "An interval that includes both zero and 30 bp gross at the cluster floor is an abstention, not a negative and not a finding." That is stricter than the council closure challenged in AUDIT-A-AiTrader-10, and it is the right rule.
5. **"TOO THIN TO TELL" was never blurred into "no effect".** The council scoring session declares the distinction in advance (AiTrader/RETURN.md:2520), lands on 9 clusters, refuses the negative ("It does NOT show the council fails to predict", AiTrader/RETURN.md:2630; AiTrader/PROGRESS.md:794), prices the confirmatory run at 25–85 USD, and the next session re-powers it to 80 clusters. Exemplary.
6. **Every pre-registered negative that could be checked was reached on its own registered rule**, with the deciding number and its n stated: H-D (−12.48 bp/day, z −1.02, 697 days), H-E (−8.22, z −0.86, 936 days) at AiTrader/RETURN.md:3219-3221; the 54-cell threshold grid with "**Zero positive cells out of 108 cell-periods**" (AiTrader/RETURN.md:3581); the default stack at −1.97 bp [−2.68, −1.27] over 19,648 trades (AiTrader/RETURN.md:3564). No bar was moved after seeing a result, and two bars were **raised** after the fact for holdout reuse (AiTrader/RETURN.md:3323, :2834).
7. **H-A, the equity overnight premium.** The session that passed its own written bar (holdout +6.19 bp, z 2.91) immediately disclosed two defects in its own registration, computed the corrected clustered estimate (z 1.73, interval spanning zero), registered a confirming observable, and Queue 002 then ran exactly that spec and reported 1.87 (AiTrader/RETURN.md:3471, :3484, :3341). Reopened as registered and re-closed on evidence.

**Blockers chased rather than parked**

8. **The tick-multiple blocker, attempts 1 to 4** (AiTrader/EXPERIMENT.md:2398-2694; AiTrader/PROGRESS.md:274-285). A textbook expired blocker that the project found and corrected itself, in writing, before this audit: "an error message was read as broader than its wording, and one unprobed parameter separated a blocked question from an open one" (AiTrader/PROGRESS.md:282). The near-monotone judgment is disclosed as a judgment with the strict flag left false, and the fee model was updated per tier. (Only the missing RETURN.md entry for that session is raised, as AUDIT-A-AiTrader-17.)
9. **The three "unmeasurable from stored data" diagnostics** (volume filter AiTrader/RETURN.md:4715, ATR band :4963, RSI-2 entry depth :4805). Each named its prerequisite; the prerequisite was built two days later (entry_decision instrumentation :4435, harness :4089) and all three questions were re-run (:4063-4065, :3573-3581). Reopened as registered.
10. **"FURTHER HYPOTHESIS ROUNDS AGAINST THIS DATABASE ARE NOT WORTH RUNNING"** (AiTrader/RETURN.md:3234) on its *information-axis* leg. The same sentence names what would change the calculus — "a new information axis the bars do not carry" — and the breadth universe was loaded the next day and used the same evening (AiTrader/RETURN.md:2985, :2844); the news-drift experiment is the text axis. That leg was honoured. (The *sizing* leg of the same closure was not — AUDIT-A-AiTrader-1.)
11. **The cross-sectional family's width closure survives its blocker's expiry.** H-F failed at holdout z 1.668 against a bar of 2.50 because a 5-name book carries 66.4 %/yr tracking error; `max_open_positions_total` then moved 5 → 10, which looks like the registered reopen. Interpolating the two widths the session itself measured (n=5: TE 66.4 %, excess 27.99 bp/d; n=50: TE 31.7 %, excess 10.04 bp/d — AiTrader/RETURN.md:2857, :2899, AiTrader/PROGRESS.md:827-828) gives at n=10 an implied z of **1.44 to 1.53 — no higher than at n=5**. Widening does not rescue the family, exactly as the session predicted. Closure stands.
12. **"The test cannot be won at this width" and more history.** Pooling fit and holdout inverse-variance (illegitimate, computed only as an upper bound: fit +12.88 bp/day at z 1.737 over 93 months, holdout +27.99 at z 1.668 over 31 months, AiTrader/RETURN.md:2856-2857) gives +15.35 bp/day, SE 6.78, **z 2.263 < 2.50**. Even the whole 10.3-year database would not clear the corrected bar. Sound.

**Refusals and self-blocking**

13. **The three-layer removal was blocked by its own gate.** The prompt asked for a removal; the replay showed 386 of 716 evaluations would newly clear the Level 1 floor, all permissive, and the session stopped and removed nothing (AiTrader/RETURN.md:2083; AiTrader/PROGRESS.md:719-740; AiTrader/CONTEXT.md:94). A closure that refused itself on evidence.
14. **AMENDMENT 4's refusal to exclude delay-rolled headlines** (AiTrader/EXPERIMENT.md:211-226) and the five-state absent-input rule (:1963-1993). Both widen rather than narrow the sample.
15. **The crypto scope narrowing as a scope decision** (AiTrader/PROGRESS.md:576-606; AiTrader/CONTEXT.md:84). Retention rather than deletion, restoration priced at "one class in `mal::scope`", the measured consequence stated at 11,978 changed decisions. Reversible by construction. (Only its cost *argument* is challenged, in AUDIT-A-AiTrader-15.)
16. **The global-session equity rotation blocker** (AiTrader/LIVE_READINESS.md:14-45). Checked whether the IBKR blocker had expired: it has not. IBKR is still "wired as the live-only venue ... but stays DISABLED" (AiTrader/AUDIT.md:36), regional whitelists are still empty placeholders (AiTrader/LIVE_READINESS.md:35-38), and the refusal is enforced rather than documented.
17. **The `rl_advisory` real-fill gate.** AUDIT.md's lead finding 3 is superseded at the anchor by a correction that moved the count in the *conservative* direction (243 of 500 → 9 of 500 after provenance confirmation — AiTrader/AUDIT-2026-07-29.md:91; AiTrader/RETURN.md:2043). No Direction-A finding.
18. **The capacity-floor correction inside the news experiment (Amendment 7, AiTrader/PROGRESS.md:185-197).** The 4.96 bp figure is arithmetically exact and the session verified the trade-cap mechanism in the engine rather than accepting the prior claim. Where the correction was applied, it was applied well — which is precisely what makes AUDIT-A-AiTrader-3 and -1 findings rather than noise.
19. **AUDIT-2026-07-29.md's own lead finding 3** (:59-72) was acted on within the same day by AMENDMENT 6. Audit-to-amendment latency of hours is the opposite of premature closure.
20. **Disclosure discipline generally.** Uncomfortable corrections are stated in the direction that hurts: the 48-bar benchmark defect whose pre-fix z was 4.974 against the corrected 2.66 (AiTrader/RETURN.md:2189); the warmup fix that **improved** two hypotheses (:2930); the spend figure inflated sevenfold and corrected downward (:2484); the OOM incident reported first (:3529).
21. **The `news_experiment/` collector state machine.** The `no_news` vs `source_failed` separation, the fifth `excluded_pre_call` state, the `calendar_exhausted` split, and the immutability of a resolved outcome are implemented as described and each is guarded by a mutation-tested case (AiTrader/CONTEXT.md:48, :56, :64, :66; AiTrader/EXPERIMENT.md:2011-2015). No state carries a closure label harsher than the evidence behind it.
22. **`research_satellite/` and `README.md`.** No hypothesis closure, blocker or reopen condition is registered in either; they are implementation and architecture surfaces.
23. **WEEKLOG pre-flight success criteria** (AiTrader/WEEKLOG.md:61-71), whose paragraph 2 explicitly forbids reading a low trade count as a verdict on either of two opposing changes — the anti-premature-closure discipline working.

**Where the thesis was expected to hold and did not.** Searched specifically for (a) a "signal-absent"
or "falsified" label sitting on a positive point estimate with a wide interval, (b) hypothesis
families closed without a registered reopen condition, and (c) thin-sample nulls presented as
refutations. Found the opposite on all three. The one candidate for (a) is H-F (holdout +27.99 bp/day,
z 1.668, AiTrader/RETURN.md:2857), and it is **not** labelled falsified — it is labelled "**CANNOT BE
DISTINGUISHED from buy and hold**" with the shortfall quantified and the power deficit declared before
the run (:2921, :2779). That is the correct label for that number. The failure mode that is actually
present is the narrower one the findings above describe: **a governing number moved and the closures
leaning on it were never re-read**, and **documents were not swept forward after the blocker they cite
expired**.

## Dropped at consolidation

**Merged, not dropped** (22 draft entries → 18 findings):
- DRAFT-p1-experiment-6 + DRAFT-p2-return-5 + DRAFT-p3-progress-5 → **AUDIT-A-AiTrader-14**. All three challenge the same closure (Stage 1 Task 6 / the two-condition collection-clearance precondition) on the same grounds (three of four arms un-run, both reachable blockers expired, collection started anyway). The merged entry keeps the strongest quote from each document, the per-arm n from all three, and both cost recomputations.
- DRAFT-p1-experiment-2 + DRAFT-p3-progress-3 → **AUDIT-A-AiTrader-10**. Same closure ("the council does not predict price at any size this system could trade") attacked on the same grounds (both deciding hurdles superseded). Kept both verbatim quotes (AUDIT.md:154 and PROGRESS.md:788), both SE routes (half-width 11.20 bp and point/z 10.87 bp, which agree), and the dollar restatement.
- DRAFT-p1-experiment-4 + DRAFT-p3-progress-6 → **AUDIT-A-AiTrader-8**. Same artifact and same closure (the discovery conviction floor as a structural blocker). Kept the Clopper-Pearson and range-based recomputations from p1, the 37-day un-actioned code state and the PROGRESS.md:104 DNN-veto evidence from p3.

**Dropped for want of a locatable quote, a figure, or an n** — none. Every draft entry carried a
verbatim quote with file:line, a deciding figure and an n, and each was re-verified against
SNAP/AiTrader during consolidation.

**Withdrawn from the "found sound" lists, because another draft's code check contradicts them:**
- p3-progress "sound" item 3 asserted that Amendment 2 "preserves the superseded 5.00 floor **with a registered reversal condition and the field needed to test it**". The shipped collector rejects sub-10.00 symbols before sampling (AiTrader/news_experiment/universe.py:163-164), so the field is present and the check is not. Withdrawn; the correct reading is AUDIT-A-AiTrader-7.
- p3-progress "sound" item 4 asserted that Amendment 1 "keeps `liquidity_rank` recorded so the superseded rule stays scoreable". The band filter removes 2,419 out-of-band symbols before sampling (AiTrader/news_experiment/universe.py:189-191). Withdrawn; the correct reading is AUDIT-A-AiTrader-13. The rest of item 4 (the amendment records that it "does not fix the dispersion it was hoped to") stands and is retained above.

**Considered and deliberately not raised:**
- **Value and Size rejected pre-test for "No fundamentals" / "No shares outstanding"** (AiTrader/RETURN.md:2785-2789), even though Finnhub `stock/metric` fundamentals are integrated (AiTrader/discovery/finnhub_source.py:80, :335). A free-tier fundamentals snapshot is a present-day value and a 2016-2026 cross-sectional backtest needs point-in-time fundamentals. The objection is real, the repository merely did not state it. Not a finding.
- **AUDIT.md's line citations into PROGRESS.md and CONTEXT.md are stale** at the anchor (e.g. AiTrader/AUDIT.md:16 cites PROGRESS.md:193 for a result now at PROGRESS.md:775). Natural consequence of an append-only tracking file; below the S4 threshold.
- **README.md:736 still mentions "prediction markets" trading around the clock** after Polymarket's removal on 2026-07-06 (AiTrader/CONTEXT.md:185). Cosmetic, below the S4 threshold.
- **AMENDMENT 6's power cost is named but never quantified** (AiTrader/EXPERIMENT.md:501-509). No closure rests on it yet, so it is recorded here rather than raised.
- **The adaptive react layer's first graduation rung is arguably triggered** — both named prerequisites (a working Finnhub key and a working Anthropic key) are now demonstrated at production scale by the collector (AiTrader/COLLECTION_LOG.md:26, :117-277) and the observe rung costs ~$0.40/day and moves no position (AiTrader/LIVE_READINESS.md:124-126). Recorded in the reopen ledger as a met condition, not raised as a finding: no document labels the layer *closed*; it is off, and "off" is a defensible state for an unmeasured layer.
- **H-F's reported capacity of 17,634 USD/yr was computed on 25,000 USD deployed against an enforced 1,000 USD at the time** (AiTrader/RETURN.md:2857 vs :1046-1048). This runs in the Direction-B direction (a claim that overstates) rather than Direction A, so it is handed to whoever audits Direction B rather than raised here.

**Labels adjusted from the drafts during consolidation**, applying the rule that a recomputation
from numbers printed in a document is READ unless an input came from stored data, code or a git
object:
- DRAFT-p2-return-3 (→ AUDIT-A-AiTrader-6) DERIVED → **READ**: every input is a RETURN.md figure.
- DRAFT-p2-return-6 (→ AUDIT-A-AiTrader-15) DERIVED → **READ**: same.
- DRAFT-p1-experiment-2, whose inputs were all document figures, would have been READ standing alone; merged with DRAFT-p3-progress-3, whose commit-ordering evidence comes from git objects and is load-bearing, **AUDIT-A-AiTrader-10 is DERIVED**.
- AUDIT-A-AiTrader-8 is **DERIVED** because the floor's provenance (`conviction_floor=council_min_confidence`) is read from code, not from a document.
All other labels are carried over unchanged.

## Live-repo access log

Merged from the three drafts. The live repository `/home/kiros-li/Documents/GitHub/AiTrader` was
touched read-only on **2026-09-05 (UTC session date)** for two purposes only, both permitted:
git history/provenance (`git status --porcelain`, `git log --date=iso-strict`, `git log -- PROGRESS.md`,
`git show --stat <sha>`, `git show e60232a -- PROGRESS.md`, `git log 705e0ed --since=2026-07-30`).
No checkout, stash, reset, branch, write, script execution, or untracked/gitignored data read.
No `.env`, keystore, session or credential file was opened.

`git -C /home/kiros-li/Documents/GitHub/AiTrader status --porcelain` **before** first access
(identical in all three drafts):

```
 M COLLECTION_LOG.md
```

`git -C /home/kiros-li/Documents/GitHub/AiTrader status --porcelain` **after** last access
(identical in all three drafts):

```
 M COLLECTION_LOG.md
```

Identical before and after, and the single entry is the pre-existing dirt documented in
COMMON_RULES.md for this repository (a collector appends to `COLLECTION_LOG.md`). No other entry
appeared. **Nothing was modified by this audit.**

**Unanchored data read:** none. Everything except the git-history facts above comes from
`SNAP/AiTrader` at the anchored SHA. The git-history facts used in findings are immutable git
objects at or before the anchor: commit timestamps and ordering (`4ec2933`, `a2f7c94`, `959a295`,
`8fd9fbf`, `82e8e72`, `3e4a684`, `74f5636`), the existence and file-stat of `e60232a`, and the
file-stat of the four post-2026-07-29 commits (`8a49239`, `f1fb308`, `b5c2236`, `705e0ed`).
The live `COLLECTION_LOG.md` carries one uncommitted collector append beyond the anchor; it was
**not** read for content, and every collection figure quoted above is from the anchored snapshot.

**Scratch computation** (outside both the audited repository and the program-audit tree):
`/home/kiros-li/.cache/program-audit/scratchpad/work/agentA-AiTrader-p1/recompute.py` and `discovery.py`,
`/home/kiros-li/.cache/program-audit/scratchpad/work/agentA-AiTrader-p2/recompute.py`,
`/home/kiros-li/.cache/program-audit/scratchpad/work/agentA-aitrader-p3/recompute.py`.
