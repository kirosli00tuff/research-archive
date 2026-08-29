# progress.md — ORBExperiment session log

Append-only. One entry per sub-stage. Every entry states the ETA given before
the task was armed and the actual elapsed against it, per standing rule 2.
Every figure travels with its n in the same sentence, per standing rule 13.

---

## Entry 0 — the operator prompt, logged verbatim before any other work

**Recorded 2026-08-29T01:57:20Z.** Standing rule 1 requires this file to exist
with the prompt reproduced verbatim before any other work. At the moment this
file was written, this repository had **sent no request to any vendor
endpoint**, held no bar, no price, no volume, no census row and no ledger. The
only files present were the placeholder scaffold of commit `840de7c`
(`README.md`, `.gitignore`, `.env.example`) and the operator prompt itself at
`docs/STAGE_A_PROMPT.md`, commit `3c8d836`.

**One ordering note, recorded rather than smoothed.** STAGE A.-1 TASK 1 says
"before any other file exists" and STAGE A.-1 TASK 0 precedes it, requiring
`docs/DUPLICATION.md`. The two cannot both be first. Resolution: TASK 0 was
executed as **read-only work only** — git preconditions, the duplication greps,
and the eight prior-art reads — with **no file written**, and this file is the
first file this session creates. `docs/DUPLICATION.md` follows immediately
after, in the same sub-stage. Nothing was written before this line.

The prompt as supplied, reproduced without alteration:

    BEGIN PROMPT

    ORBExperiment, Stage A. Effort: high. Run autonomously. Commit at every task boundary and push to origin/main immediately after every commit. The remote already exists and main already tracks origin/main. Never force-push, never rewrite a pushed commit, never amend a pushed commit.

    Purpose. Stand up a measurement-only experiment repo at /home/kiros-li/Documents/GitHub/ORBExperiment testing one hypothesis: among US common stocks with elevated opening relative volume, a breakout of the first 5-minute regular-session range predicts continuation to the session close, by enough to clear modeled commissions, fees, borrow and slippage, out of sample from 2023-01-03 forward. Stage A registers the design, verifies vendor access, measures bar revision rate and cross-vendor agreement and delisted-name coverage, freezes a cost model, fires a power verdict, and arms collectors. Stage A never trades, never touches capital, and never reads an outcome value.

    The measurement that decides this repository is not the return. It is bar integrity. Treat STAGE A.1 : TASK 3 and STAGE A.1 : TASK 4 as the experiment. Two precedents force this. MLCryptoEngine H11 died on a measured 75-day publication lag in a free flow source with whole-file regeneration that revised past rows, and the lag was discovered rather than registered. Concretum Research ran identical opening-range code against four vendors with identical dates, parameters and starting capital and reported final portfolio values from 226,000 to 726,000 USD, a threefold spread from vendor choice alone. If bar integrity fails here, no model in this repo can mean anything, and BLOCKED is the correct and cheap answer.

    Standing rules, in force for every task.

    1. Log this prompt verbatim to progress.md before any other work.
    2. State an ETA before arming each task. Record actual against ETA after.
    3. Commit at every task boundary. Push to origin/main after every commit. A task is not complete until its commit is on the remote.
    4. Measured beats documented. Verify every external figure live before relying on it. A tier limit printed on a vendor's pricing page is documented, never measured, and the measured limit wins. The MLCryptoEngine ADR-055 fee re-verification pattern applies to every vendor and broker figure in this repo.
    5. Absence is a recorded state, never a synthesized value. A refusal is loud, never a silent skip. (orb.absence)
    6. Ledgers are append-only and fsynced. A truncated line is reported, never repaired. (orb.ledger)
    7. Operational health and sample composition never merge. Call states: stored, no_data, source_failed, rate_limited, excluded_ineligible, expired, halted.
    8. Outcome blindness, stated exactly in the section below. Stage A parses row counts, timestamps, ticker symbols and exchange codes only. No price value, no volume value, and nothing derived from either leaves a sealed writer until the registered Stage C latch opens.
    9. The pre-period carve-out is the one exception, stated in full below.
    10. Union time intervals before summing. Order multi-process logs by clock, never by file position.
    11. Spend nothing without an explicit operator instruction in this prompt. Free and trial tiers only in Stage A. A request ledger with a per-vendor daily cap charges before sending.
    12. Terms of service bind. Record robots.txt and the published terms verbatim for every vendor before the first repeated fetch. If automated collection is disallowed, record it loudly and route the access verdict accordingly. Do not proceed against a stated prohibition. The HFExperiment Wealthsimple finding is the precedent.
    13. Every figure travels with its n in the same sentence.
    14. Session times are stated in US Eastern with the UTC offset named, because the experiment is anchored to a cash-session clock that shifts twice a year. Never store a naive timestamp.

    The blindness field lists, stated exactly.

    Readable outside the sealed writers, in Stage A: ticker symbol, exchange code, listing and delisting dates, bar timestamp, bar count per session, session date, and the vendor response status code. Nothing else.
    Never readable outside the sealed writers, in Stage A: open, high, low, close, volume, vwap, trade count, bid, ask, or any function of them, under any spelling, in any module. Pinned repo-wide by tests/test_guards.py::test_no_module_reads_a_priced_bar_field_anywhere, which walks the parse tree rather than the text.
    The sealed comparator is the single exception and it is a sealed writer. It reads price and volume values from two vendors, emits only aggregate mismatch counts and rates, and returns no bar value to any caller. Pinned by tests/test_guards.py::test_comparator_returns_no_bar_value.
    The universe module, the signal module and the verdict module are built dark in Stage A against synthetic fixtures with known answers, and are never pointed at real bars before the Stage C latch. Pinned by test.

    The pre-period carve-out.

    Power inputs may read US equity bars stamped strictly before 2016-01-04. Every other bar read is sealed. The rationale: 2016-01-04 is the first session of the registered in-sample window, so the window before it sits outside both the in-sample and the holdout samples and reading it cannot leak a single observation any verdict will be computed on. The E2 economic-power computation needs a per-trade dispersion figure to size a net edge against a modeled cost, and taking that from the test window would be reading the outcome to plan the test of the outcome, while inventing it would register a number this repository did not measure. The enforcement site is orb.preperiod.require_pre_period and orb.preperiod.gate_pre_period, the boundary is CONFIG.pre_period_end_ms at 2016-01-04T14:30:00.000Z exclusive, and the pin is exercised by tests/test_preperiod.py with fixtures sitting exactly on the boundary: one millisecond before it passes, the instant itself is refused.

    Prior art to read before TASK 0, for patterns not text.

    /home/kiros-li/Documents/GitHub/ETFExperiment/CLAUDE.md and REGISTRATION.md, for the operating-manual shape, the blindness field lists, the carve-out paragraph and the Section 0 fire function.
    /home/kiros-li/Documents/GitHub/ETFExperiment/DECISIONS.md, ADR-001, for the provisional-parameter-with-one-permitted-amendment shape.
    /home/kiros-li/Documents/GitHub/NPLExperiment/REGISTRATION.md and HYPOTHESES.md, for the register style, the latch protocol, the quarantine and the closure shape.
    /home/kiros-li/Documents/GitHub/NPLExperiment/progress.md, for how a falsified planning figure gets recorded rather than quietly corrected, and for the Section 0 cull firing on measured rates.
    /home/kiros-li/Documents/GitHub/NPLExperiment/docs/STAGES.md, for the stage-ladder table shape with entry gate, exit gate and capital columns.
    /home/kiros-li/Documents/GitHub/MLCryptoEngine/HYPOTHESES.md entry H11, and DECISIONS.md ADR-055, for the source-integrity death and the fee re-verification pattern.
    /home/kiros-li/Documents/GitHub/solattn/DECISIONS.md, ADR-019 and ADR-021, for seal discipline and per-endpoint pacing.
    /home/kiros-li/Documents/GitHub/InsiderExperiment/progress.md, for the power-gate closure shape and the boundary-fixture mutation lesson.

    Figures carried into the registration, sources named there, none of them measured by me. Label every one of these carried.

    Source study one. Zarattini and Aziz, Can Day Trading Really Be Profitable, SSRN abstract_id 4416622. QQQ and TQQQ, January 2016 to February 2023. A 5-minute opening-range rule with a 10R target, stop at the first candle's opposite extreme, 1 percent planned loss, 4x leverage cap, 25,000 USD start, commission 0.0005 USD per share, and explicitly zero slippage assumed. Reported QQQ 1,484 percent against 169 percent buy-and-hold, annualized alpha near 33 percent. Note the label caveat in the registration: the rule enters at 09:35 on the first candle's direction and does not require a later break of the range, so it is early-momentum with an opening-range stop rather than a breakout.

    Source study two, the one this repo tests. Zarattini, Barbon and Aziz, A Profitable Day Trading Strategy For The U.S. Equity Market, SSRN abstract_id 4729284, Swiss Finance Institute 24-98. More than 7,000 US stocks, 2016 to 2023, delisted names included. Filters: open above 5 USD, 14-day average volume above 1,000,000 shares, 14-day ATR above 0.50 USD. A plain broad-universe 5-minute ORB returned 3.2 percent annually at 6.6 percent annualized volatility, Sharpe 0.48, below passive. Restricting to the top 20 stocks in play by opening relative volume returned more than 1,600 percent net at Sharpe 2.81 and annualized alpha 36 percent, against 198 percent for the S and P 500 over the same window. The 15-minute variant returned 272 percent at Sharpe 1.43. The selection by relative volume, not the breakout, did almost all the work. This is a single, unreplicated, in-sample result produced by authors who sell day-trading education. Record that sentence in the registration.

    The independent replication, and the most important figure in this prompt. giovannibrusco/zarattini-2023-orb-qqq on GitHub reproduced the QQQ result within noise at 1,775 trades against the paper's 1,795 and gross Sharpe 1.06, then showed the edge sits inside the spread. Gross edge 0.070 USD per share. Net PnL crosses zero at roughly 0.022 USD per share of entry slippage, against a QQQ spread near 0.01 USD. A 09:25 NQ futures agreement filter lifted per-trade edge to 0.125 USD per share at t 2.05, but strategy Sharpe 0.77 barely beat buy-and-hold at 0.72 with overlapping bootstrap intervals, 0.05 to 1.41 against minus 0.03 to 1.47. 76 percent of the filtered PnL came from 2022 alone, and the filter lost money in 2017, 2020 and early 2023.

    Further decay evidence. A 2026 arXiv falsification study on MNQ micro futures tested ORB long, short and pullback variants and found all failed after 2-point friction, with the best long variant at t 1.50. Year by year, 2022 negative, 2023 near zero, 2024 strongly positive. The same one-good-year signature.

    Multiple-testing context. Harvey, Liu and Zhu argue a new claim should clear a t near 3.0 rather than 2.0. Bailey and Lopez de Prado, SSRN abstract_id 2460551, deflate a reported Sharpe for the number of trials plus skewness and kurtosis. McLean and Pontiff, Journal of Finance 71 pages 5 to 32, found published predictor returns fall 26 percent out of sample and 58 percent after publication across 97 predictors from 80 studies.

    Cost figures carried. Interactive Brokers Canada tiered US stock commission 0.0035 USD per share, minimum 0.35 USD per order, plus pass-through exchange, SEC and FINRA fees. FINRA trading activity fee near 0.000166 USD per share sold. IBKR FX conversion near 0.2 basis points above interbank with a 2.00 USD per order minimum. Every one of these is carried and must be re-verified live under standing rule 4 before the cost model freezes.

    In-house constraint carried. IBKR refuses fractional-sized orders through the API with error 10243, HFExperiment reports/stage_a1b/a1b_report.md line 52. Share-count sizing is therefore integer-only and the registration states it as a design constraint rather than discovering it at execution.

    Assistant prior, recorded 2026-08-28 in chat: 0.15 on a real capturable edge surviving the registered cost model out of sample. Nothing in the repos or on the web has moved it. The NPDExperiment Amendment 0 lesson applies. An adopted prior corrupts the calibration ledger. The operator prior slot stays empty. Do not fill it.

    The correction that governs this repo. In NPLExperiment a main-dex accrual figure near 9.4 events per month entered a registration as a planning number and measurement falsified it at 0.5, n equals 3 over 182 days, killing H3 on a figure rather than on the world. No vendor coverage, revision, agreement, delisting, trigger-rate or slippage figure in this repo is registered before it is measured. Every such figure below is named as an A.1 or A.2 measurement target, never as an input.

    STAGE A.-1 : TASK 0. Preconditions and the duplication screen.

    Confirm the working tree is /home/kiros-li/Documents/GitHub/ORBExperiment, that main tracks origin/main, and that git push --dry-run succeeds. Record the result.
    Run the duplication screen before writing a single line of design. Grep every repo under /home/kiros-li/Documents/GitHub, excluding .git, .venv and caches, for: opening range, ORB, opening candle, relative volume, 09:30, 9:30, intraday breakout, stocks in play. Record the full output in docs/DUPLICATION.md with the command used and the hit count per repo. A substantive hit halts Stage A and reports. Incidental prose hits are recorded and cleared with a one-line reason each.
    The expected result is CLEAR: MLCryptoEngine, MLCryptoTrader, NPLExperiment, NPDExperiment, HFExperiment, InsiderExperiment, ETFExperiment, solattn, solclear and AiTrader are crypto, on-chain, filings or news-LLM, and none covers intraday US equity price structure. Verify rather than assume.
    Read the eight prior-art files listed above.

    STAGE A.-1 : TASK 1. Prompt log.

    Write progress.md with this prompt reproduced verbatim between BEGIN PROMPT and END PROMPT as Entry 0, before any other file exists. Commit. Push.

    STAGE A.0 : TASK 2. Scaffold.

    uv project, package orb, src layout, Python 3.13 or newer. ruff, mypy strict, pytest, pre-commit. Makefile with install, lint, fmt, typecheck, test, all, guards, mutations. .env.example empty on purpose, no key is needed for any Stage A source. .gitignore covering .env, data/, .venv, caches and egg-info, already present, verify it.
    Port the standing guards by copying shape, not text, from ETFExperiment and InsiderExperiment.
    Guard 1, recorded absence (orb.absence): a type refusing float, int, indexing and addition. A missing bar where a number will later stand is not a zero.
    Guard 2, parse-tree config enforcement: every field of orb.config.Config must be read by a module outside config.py or sit on PENDING_ENFORCEMENT with its task named. Walk the AST, never the text.
    Guard 3, append-only fsynced ledger (orb.ledger): a truncated line is reported, never repaired.
    Guard 4, the seven call states above as an enum, with operational health and sample composition structurally unable to merge.
    Guard 5, specific to this repo: the priced-bar blindness pin, refusing any read of open, high, low, close, volume, vwap, trade count, bid or ask outside a sealed writer.
    Guard 6, specific to this repo: the pre-period date pin at 2016-01-04T14:30:00.000Z exclusive.
    Guard 7, specific to this repo: a session-clock guard refusing any naive datetime and refusing any Eastern time computed without a DST-aware zone. The opening range is anchored to 09:30 Eastern, which is 13:30 UTC in summer and 14:30 UTC in winter, and a fixed UTC offset silently mis-slices roughly a third of the sample.
    make all must pass green on the empty tree. Commit. Push.

    STAGE A.0 : TASK 3. CLAUDE.md.

    The standing rules above, the blindness field lists stated exactly, the carve-out in one paragraph with its rationale and enforcement site, the coding standards, and the commands. Follow the ETFExperiment CLAUDE.md shape. State in the opening block, permanently, that Stage A never trades, never touches capital, and never reads an outcome value, and that a documented negative is a valid and expected outcome. Commit. Push.

    STAGE A.0 : TASK 4. REGISTRATION.md Section 0, the outcome map, committed before any network call.

    The outcome map judges collection feasibility, source integrity and detectability, never returns.
    GO: both co-primaries of Section 8 reach at least 80 percent power at alpha_adj under the registered effect assumption of Section 9 at the achievable session count, and the bar-integrity verdict of A.1 TASK 3 and A.1 TASK 4 passes in full, and delisted-name coverage passes.
    DEGRADED: E1 reaches at least 80 percent power at the published-magnitude assumption but under 80 percent at the registered assumption, or bar integrity passes partially, or delisted coverage is present but thin. Collection proceeds. The verdict scope narrows and the registration states the narrowing in plain words before any data exists: under DEGRADED a later FAIL establishes that the effect is not present at its published magnitude and cannot distinguish a decayed effect from no effect at all.
    BLOCKED: E1 under 50 percent power at the published-magnitude assumption, or bar integrity FAIL, or zero delisted names served across the window, or a measured cross-vendor disagreement rate high enough that the top-20 selection is not reproducible.
    Enforced by a fire function with tests, boundary fixtures sitting exactly on each threshold.
    Registered expectation, stated now so the verdict reads as a documented answer rather than a disappointment. The arithmetic in Section 9 and the decay evidence above point to DEGRADED. Say so in the registration.

    STAGE A.0 : TASK 5. REGISTRATION.md Sections 1 through 12, committed before any network call.

    Section 1, hypothesis. Among US common stocks with elevated opening relative volume, a breakout of the first 5-minute regular-session range predicts continuation to the session close, net of modeled costs, out of sample from 2023-01-03. State it as a joint claim about the selection and about the breakout, and state the three structural doubts as part of the hypothesis rather than as caveats. Publication: the signal was published openly in 2024 and popularized commercially. Cost: the index version's entire gross edge measured smaller than a realistic slippage assumption. Regime: 76 percent of the replication's filtered profit came from one calendar year.

    Section 2, universe and event rule. US common stocks and no ETFs, evaluated at 09:35:00 Eastern each regular session. Opening relative volume equals first-5-minute share volume divided by trailing 14-session median first-5-minute share volume. Rank descending, take the top 20. Filters: session open above 5.00 USD, 14-session average volume above 1,000,000 shares, 14-session ATR above 0.50 USD. Exclude a name with no locate or a borrow rate above 25 percent annualized on the short side. Delisted tickers are included for every historical session in which they traded. Sessions are never filtered on any return quantity. Half sessions are excluded and counted.

    Section 3, the signal, the entry and the exit. This is the section the repo turns on.
    Opening range: the high and low of 09:30:00.000 to 09:34:59.999 Eastern.
    Entry: the first trade through the range high goes long, the first trade through the range low goes short, as a marketable limit at the range boundary plus 0.05 percent of price. One entry per name per session. No re-entry after a stop. If both sides trigger inside the same bar, the session is recorded ambiguous and excluded, and the ambiguous rate is a measured figure.
    Stop: the opposite extreme of the opening range, held as a resting stop.
    Exit: the session close, 15:55:00 to 15:59:00 Eastern, with no profit target. The 10R target of the source study fills on 2 to 3 percent of trades and is a mined parameter. Record as an ADR.
    The entry rule is registered as a true breakout and not the source study's immediate first-candle directional entry. Record as an ADR with the reason: the immediate entry is not a breakout, and registering the paper's rule under the paper's name would carry the paper's label onto a different claim.

    Section 4, sizing. Equal risk, 0.25 percent of equity per trade, risk defined as the entry-to-stop distance. Integer share counts only, IBKR error 10243. Maximum 20 concurrent positions, gross notional capped at 1.0x equity, no leverage, no compounding, constant equity base. Each named as a Stage-scope simplification.

    Section 5, outcome definition. Net PnL per trade equals the signed price difference from the modeled entry fill to the modeled exit fill, times shares, minus commissions, minus regulatory fees, minus borrow accrued on short positions, with slippage applied at the registered per-leg figures. The portfolio daily net return is the sum of that session's trade PnL over the constant equity base. State the sign convention explicitly.

    Section 6, costs and the modeled fill. Commission 0.0035 USD per share with a 0.35 USD order minimum. FINRA TAF 0.000166 USD per share sold. SEC fee on sells at the rate in force on the session date, recorded per date, never a single constant. Entry slippage 0.020 USD per share central, band 0.010 and 0.040. Stop-exit slippage 0.040 USD per share central, band 0.020 and 0.080, wider because a stop is marketable and gap-prone. Close-exit slippage 0.010 USD per share central, band 0.005 and 0.020. Borrow accrued daily at the measured rate where served, and where not served the name is excluded on the short side and counted, never assumed cheap. The optimistic end of every band is reported as an upper bound of optimism, never as the central case. The QQQ replication's 0.022 USD per share break-even is recorded beside the central 0.020 assumption as the reason this band is the whole experiment.

    Section 7, horizons and windows. In-sample 2016-01-04 to 2022-12-30. Holdout 2023-01-03 to 2026-06-30, pinned. Session-close exit only. No overnight horizon is verdict-bearing.

    Section 8, inference. Two co-primaries, one-sided, alpha_adj equal to one minus 0.95 to the one-half power, 0.0253 each, and both must pass.
    E1, risk-adjusted. Deflated Sharpe ratio of the daily net portfolio return series over the holdout, computed by the Bailey and Lopez de Prado method, with the trial count registered at 8, being four opening-range lengths of 5, 15, 30 and 60 minutes crossed with two entry rules of immediate-direction and true-breakout, and with skewness and kurtosis taken from the realized series. Bar: deflated Sharpe at or above 1.00.
    E2, economic. Mean net PnL per trade, one-sided lower bound above zero at alpha_adj, by permutation on session labels with trades clustered by session date so that a single strong session cannot masquerade as many independent observations.
    Two structural gates applied alongside, both registered as pass-fail and not as tests: no single holdout calendar year contributes more than 50 percent of holdout net PnL, and holdout net PnL is positive in at least 3 of the 4 holdout calendar years. The concentration gate exists because 76 percent of the replication's filtered profit came from 2022 alone. Record as an ADR.
    Named secondaries, descriptive and never verdict-bearing: the 15, 30 and 60-minute range lengths, the immediate-direction entry, the long-only and short-only legs separately, the top-10 and top-40 selection widths, performance conditioned on the VIX close against its trailing 252-session median, the ambiguous-trigger subset, and the gap-size decile profile.

    Section 9, power method and the registered effect assumption. Registered assumption: annualized net Sharpe 1.40, being half the published 2.81. The rationale is registered with it and is not discretionary: McLean and Pontiff measured a 58 percent post-publication decay across 97 predictors, the source result is unreplicated and commercially motivated, and the one independent replication of the sibling index strategy found the edge inside the spread.
    The arithmetic, to be reproduced in code and recorded, not taken from this prompt: daily Sharpe equals 1.40 divided by the square root of 252, which is 0.0882. The t statistic over n sessions equals 0.0882 times the square root of n. Clearing t equal to 2.0 needs 514 sessions, roughly 2.04 years. Clearing t equal to 3.0 needs 1,157 sessions, roughly 4.59 years. The in-sample window holds roughly 1,760 sessions and is powered for t equal to 3.0. The holdout holds roughly 880 sessions and yields t equal to 2.62 at the registered assumption, which is below 3.0.
    Register that shortfall openly as an ADR rather than discovering it at the read. The holdout gate is therefore set at a per-trade t of 2.50 with the deflated-Sharpe bar carrying the multiple-testing correction, and the registration states in plain words that the holdout alone cannot clear a factor-zoo hurdle at the discounted effect size.
    Powers at the undecayed 2.81 and at a quartered 0.70 are computed and reported beside as the honest range, the NPLExperiment H3 pattern. Minimum-N statements for each co-primary at each of the three assumptions.
    Per-trade power is computed and reported as non-binding: at 20 names per session and an assumed trigger rate to be measured rather than assumed, the holdout carries thousands of trades and clearing t equal to 3.0 needs a per-trade information ratio near 0.031. The portfolio-day series is the binding constraint and the registration says so.
    Dispersion inputs to the E2 power computation come from the pre-period carve-out only, strictly before 2016-01-04.

    Section 10, the Stage C latch. Both co-primaries at or above 80 percent power at achievable N under the assumption Section 0 fired on, the operator prior slot filled and labelled independent or adopted, and explicit operator instruction. Stage C opens the sealed in-sample read exactly once, behind a latch written first, recording module hashes. Stage D opens the holdout exactly once, behind its own latch. A second read of either window voids the hypothesis. Every value inside a read is quarantined from any successor code path by AST pin and by test.

    Section 11, epistemic boundary. A positive supports the claim that the registered rule would have cleared its bars on this sample under this cost model from this vendor. It is never a forward return prediction. It is never evidence about any range length or entry rule other than the registered one. It is never evidence that the source study's reported figures are correct, because the entry rule registered here differs from theirs by design.

    Section 12, spend and pacing. Zero dollars in Stage A. Free and trial tiers only. A request ledger with a per-vendor daily cap set from the A.1 TASK 2 measurement and recorded by amendment if it moves. Pacing respects the recorded terms of service. Any paid tier requires an explicit operator instruction and its own ADR, and the registration names the expected monthly figure as carried, not measured: Polygon Starter near 29 USD per month, Databento consumption-based near 125 USD per month for a medium universe.

    STAGE A.0 : TASK 6. Section 13, priors.

    Record the assistant prior of 0.15 with its date and the adoption warning. Reserve the operator slot empty. The empty slot blocks the Stage C latch structurally.

    STAGE A.0 : TASK 7. Section 14, the amendment log, and HYPOTHESES.md.

    Open the amendment log empty with its rules: append-only, dated, reasoned, stating exactly what data existed when the amendment was made, and nothing above an amendment line is ever edited.
    Create HYPOTHESES.md with one entry, H1, seeded OPEN, carrying the claim, the registration pointer, the registered bars, the power assumption with its rationale, the assistant prior and an empty operator prior slot. Write the purpose paragraph in the MLCryptoEngine voice: this file exists to prevent retrying a settled question because the number that closed it is buried. State the four closure kinds already in the house record so a future closure can be typed correctly: cost-bound, signal-absent, unmeasurable-on-available-data, and untestable-at-achievable-power. Add the fifth this repo may produce: source-integrity-blocked, the Concretum shape.
    Also record in HYPOTHESES.md, as closed-before-opening entries with one-line reasons, the ten candidates culled at registration: index-ETF ORB, CME Bitcoin weekend gap fill, S and P index addition and Russell reconstitution, turn-of-the-month, short-term reversal, post-earnings announcement drift, prediction-market mispricing, perpetual funding carry, new Hyperliquid listing drift, and spot Bitcoin ETF flow. The last two are DUPLICATE against NPLExperiment and ETFExperiment and must be labelled as such. Record H2, pre-FOMC drift, and H3, VIX term-structure roll yield, as PARKED with the reason that no second repo opens while H1 is unresolved.
    Commit STAGE A.0. Push.

    STAGE A.1 : TASK 1. Access verification, docs/ACCESS.md.

    Verify live, with verbatim response fragments and status codes, and record robots.txt and the published terms for each vendor before the first repeated fetch.
    Vendors to probe: Polygon, also branded Massive; Alpaca market data; Databento; Tiingo; EODHD; Alpha Vantage; Nasdaq Data Link; Stooq; and yfinance as a floor case. For each record, with its n: whether a free or trial tier serves 1-minute regular-session bars, how far back that tier reaches measured by bisection rather than taken from the pricing page, whether the tier serves delisted tickers, whether a corporate-actions or split-adjustment endpoint exists and whether adjustment is applied retroactively to already-served bars, the served timezone and whether it is DST-aware, the rate ceiling shape, and the exact refusal payload when a limit is hit.
    Record the documented tier limits verbatim and label them documented, never measured. Under standing rule 4 the measured limit wins and any disagreement is recorded as a finding rather than reconciled.
    Two questions decide vendor selection and both are integrity questions, not price questions: does the tier serve delisted names, and does it retroactively rewrite already-served bars on a split or a correction. A vendor that rewrites history silently is the H11 hazard in a different costume.

    STAGE A.1 : TASK 2. Rate ceilings measured per endpoint.

    The solattn ADR-021 lesson: ceilings are per endpoint, never per host, and measured never assumed. Probe each endpoint under the request ledger with a short escalation protocol. Record the refusal shape verbatim, the sustained admitted rate, and a chosen operating pace at half the measured ceiling, reduced further wherever the recorded terms ask for it. Record the daily cap per vendor and wire it into the ledger so the cap charges before sending.

    STAGE A.1 : TASK 3. Bar revision rate. The first of the two tasks this repo turns on.

    Select a primary vendor and a secondary vendor from TASK 1 on integrity grounds, recording the selection reasoning in an ADR.
    Pull a probe slice from the primary: 60 consecutive regular sessions ending at least 30 calendar days before today, across a fixed list of 40 tickers drawn without reference to any price, being the 40 alphabetically-first symbols meeting a liquidity screen evaluated by the sealed writer. Record the ticker list, the session list, and a SHA-256 per stored file in the append-only ledger. Parse nothing outside the readable field list.
    Arm a re-pull unit that repeats the identical request set after a registered wait of at least 14 calendar days. This wait is why Stage A cannot finish today, and the repo should say so plainly in progress.md.
    On the second pull, the sealed comparator measures and reports, each with its n: the share of bars whose stored bytes changed, the share of session-ticker pairs whose bar count changed, the share where a timestamp appeared or disappeared, and whether any change correlates with a corporate action on that ticker in that window.
    Verdict shape. PASS means the changed-bar share is at or below 0.5 percent. PARTIAL means above 0.5 and at or below 2.0 percent, recorded as a registered scope limitation carried into every downstream figure. FAIL means above 2.0 percent and fires BLOCKED.

    STAGE A.1 : TASK 4. Cross-vendor agreement and delisted-name coverage. The second of the two.

    Two measurements, both first-class.
    Agreement. Pull the identical 60-session, 40-ticker slice from the secondary vendor. The sealed comparator reports, each with its n: the share of bars present in both, the share whose OHLC agree to the cent, the distribution of absolute disagreement in cents, and the share of session-ticker pairs where the two vendors disagree on the first-5-minute high or low, which is the only disagreement that changes an entry price. It returns no bar value to any caller. The Concretum finding of a threefold spread in final equity across four vendors on identical code is the reason this is first-class rather than a footnote.
    Delisted coverage. Enumerate tickers the primary vendor serves that have a delisting date inside 2016-01-04 to 2026-06-30. Report the count, the count per year, and whether intraday bars are served for sessions before each delisting. A survivor-only universe would inflate every downstream figure and is unrecoverable after the fact.
    Verdict shape. PASS means first-5-minute high-or-low agreement at or above 95 percent of session-ticker pairs and at least 100 delisted names served with intraday history. PARTIAL means agreement between 85 and 95 percent, or between 20 and 100 delisted names, demoting the selection reproducibility to a recorded scope limitation. FAIL means agreement below 85 percent or fewer than 20 delisted names, and fires BLOCKED.
    Commit STAGE A.1. Push.

    STAGE A.2 : TASK 1. Session calendar and the corporate-actions substrate.

    Build the US equity regular-session calendar for 2016-01-04 to 2026-06-30 from a recorded source, including half sessions and unscheduled closures, with the DST-aware Eastern anchor for every session. Report the session count per year and the half-session count. Cross-check the total against a second source and record any disagreement rather than reconciling it.
    Build the corporate-actions substrate for the ticker universe: splits, reverse splits, symbol changes and delistings, with dates. Report counts with their n. This is a symbol-and-date substrate. It reads no price.

    STAGE A.2 : TASK 2. Cost model, built and frozen.

    Implement Section 6 exactly. Unit tests pin each component against a hand-computed example, including the 0.35 USD order minimum binding on a small share count and the SEC fee changing across a rate-change date.
    Re-verify live, under standing rule 4 and the ADR-055 pattern, every carried broker figure: IBKR tiered per-share commission, the order minimum, the current FINRA TAF rate, the current SEC fee rate, and the FX conversion cost. Record measured against carried, in the same sentence with its date. Any deviation is written as an amendment before Stage A.2 TASK 4, never silently absorbed.
    Freeze the model, hash it, latch it, and record the hash in the ledger. Cost parameters cannot change after this point without a dated amendment naming what data existed when it was made.

    STAGE A.2 : TASK 3. Universe, signal and verdict machinery, built dark.

    Implement the Section 2 selection, the Section 3 entry, stop and exit, and the Section 8 statistics, all against synthetic fixtures with known answers. Include a planted-signal fixture the canary must fire on, a fixture where both sides trigger inside the same bar to exercise the ambiguous path, a fixture where the stop and the range boundary coincide to the cent, and a fixture on a half session.
    Never point any of it at real bars. Pinned by test. Stage C calls it exactly once.
    Hand-compute, by hand and not by the code under test, the opening range, breakout price, stop and close exit for 10 named ticker-sessions drawn from the pre-period carve-out window, and pin them as known-answer tests matching to the cent.

    STAGE A.2 : TASK 4. Power gate.

    Simulation power for E1 and E2 at alpha 0.0253 one-sided, at the registered 1.40 Sharpe assumption, at the undecayed 2.81, and at the quartered 0.70, using the achieved session count, the projected count to 2026-12-31, and the projected count to 2027-06-30. E2 power uses pre-period dispersion only. Report minimum N clearing 80 percent for each co-primary at each assumption. Reproduce the Section 9 arithmetic in code and record any disagreement with the figures stated in this prompt, with the computation winning. Compute nothing else. Read no outcome value.

    STAGE A.2 : TASK 5. Fire Section 0.

    Record the verdict in the registration amendment log, in HYPOTHESES.md and in progress.md, with every input figure beside it and its n. On BLOCKED, stop after the documentation stage and arm nothing. On DEGRADED, record the narrowed verdict scope in the registration and in the register entry, in the plain words Section 0 requires.
    Commit STAGE A.2. Push.

    STAGE A.3, armed only on GO or DEGRADED.

    STAGE A.3 : TASK 1. Production bar collector.
    Promote the TASK 3 probe to a durable collector pulling the prior session's regular-session 1-minute bars for the registered universe each evening. Diff each pull against the last sealed manifest. On a changed bar for a closed session, append a revision row with both hashes and both pull timestamps. A 429 or 5xx writes a loud error marker and is never read as no-data. Seal the prior session's manifest at the daily pass, the solattn ADR-019 shape, and never seal the open session.

    STAGE A.3 : TASK 2. Corporate-actions watcher.
    A daily pass recording new splits, symbol changes and delistings against the universe, appending to the substrate ledger. A split landing on a stored session is the event most likely to trigger a silent vendor rewrite, so it is watched rather than discovered.

    STAGE A.3 : TASK 3. systemd.
    User units orb-daily.service on a timer at 22:15 UTC and orb-actions.service on a timer at 22:45 UTC, both Persistent true, MemoryMax 2G. Verify no unit-name collision: npl-daily, npl-watch, etf-snap, etf-daily, solattn-daily and news-collect are in use and must be left untouched. Confirm each still shows its expected next-elapse after arming. Add the manual-run guard refusing while units are active, the ADR-018 shape, with a named override env var. A gap in a forward-recorded bar ledger cannot be backfilled from a vendor that rewrites history, which is exactly the dependency this repo is measuring, so durability is not optional.

    STAGE A.3 : TASK 4. Latch machinery.
    Write the Stage C and Stage D latch files, the module-hash recorder, and the AST quarantine pin that prevents any value from a spent read reaching a successor code path. Test that a second read attempt refuses loudly.
    Commit STAGE A.3. Push.

    STAGE A.4 : TASK 1. Gates.
    make lint, typecheck and test green under ruff and mypy strict, every guard exercised, including the priced-bar blindness pin, the pre-period date pin and the session-clock guard.

    STAGE A.4 : TASK 2. Mutations.
    At least eight applied to real source, each caught, source restored green, bytecode purged before every run.
    Delete a blindness pin and confirm a priced-bar read is then reachable.
    Coerce a recorded absence to zero.
    Merge rate_limited into no_data.
    Move a boundary fixture off the registered 09:35:00.000 Eastern boundary and confirm the test stops binding.
    Replace the DST-aware Eastern anchor with a fixed UTC offset and confirm the session-clock guard fires.
    Read a bar stamped on or after 2016-01-04 through the pre-period carve-out.
    Make the sealed comparator return a bar value to a caller.
    Point the verdict module at real bars before the latch.
    Evidence in reports/stage_a4.

    STAGE A.5 : TASK 1. Docs.
    README.md at one page in the ETFExperiment shape, with a what-is-measured-so-far table carrying every figure with its n. ACCESS.md finalized. DUPLICATION.md finalized. DECISIONS.md with numbered ADRs for every choice above, at minimum: the true-breakout entry against the source study's immediate entry, the removal of the profit target, the registered half-effect assumption, the t equal to 2.50 holdout gate and the openly registered power shortfall, the concentration gate, the vendor selection on integrity grounds, the cost bands and the optimism labelling, the blindness field lists, the pre-period carve-out, the session-clock guard, the integer-share constraint from IBKR error 10243, the pacing figures, the seal target, and the exclusion of the index-ETF variant with the replication figures that forced it.
    docs/STAGES.md with the full ladder as a table carrying entry gate, exit gate and capital columns, in the NPLExperiment shape, covering Stage A through the capital gate, and stating that the forward shadow is a parallel monitor rather than a gate and that live entry sits behind the software-correctness gates rather than behind the out-of-sample read.
    report.md, stage-sectioned in the MLCryptoEngine shape, one section per sub-stage, each written for the moment it landed. Sections for A.1 access, A.1 revision, A.1 agreement and delisted coverage, A.2 calendar and actions, A.2 cost verification, A.2 power, and the Section 0 verdict with its inputs. Reserve empty Stage C and Stage D sections with a one-line note that each is written once and only after its latch.

    STAGE A.5 : TASK 2. Close-out.
    progress.md entries per sub-stage with ETA against actual. Update the HYPOTHESES.md H1 entry with the Section 0 verdict and every measured figure with its n. Final commit. Push.
    Print an end-state summary: the Section 0 verdict with its inputs, the measured bar revision rate, the measured cross-vendor first-5-minute agreement rate, the delisted-name count, the measured broker figures against the carried ones, achieved and projected session counts, the earliest Stage C date given the 14-day revision wait, and the open operator items, which should be the prior slot and nothing else.

    STAGE A.5 : TASK 3. Handover.
    Write docs/HANDOVER.md as a structured overview for a fresh chat session: what this repo tests, what Stage A measured, what is armed, what the next decision is and when it arrives, and what a fresh session must read before touching anything. Commit. Push.

    END PROMPT

---
## Entry 0a — a recorded deviation: three network calls preceded this file

**Recorded 2026-08-29T01:57:20Z, before the first commit of this session.**

STAGE A.0 TASK 4 and TASK 5 require REGISTRATION.md to be committed **before any
network call**. Three network calls were sent **before** this file existed, at
approximately 2026-08-29T01:52Z, while establishing whether outbound network
access existed at all in order to state a defensible ETA table. They are
recorded here rather than reconciled, per the NPLExperiment precedent that a
falsified or breached planning assumption is recorded, never quietly corrected.

The three calls, in full, n = 3:

| endpoint | method | status | body handling |
|---|---|---|---|
| `https://api.polygon.io/v1/marketstatus/now` | GET | **401** | discarded to `/dev/null` |
| `https://stooq.com/q/d/l/?s=aapl.us&i=d` | GET | **200** | discarded to `/dev/null` |
| `https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=IBM&interval=5min&apikey=demo` | GET | **200** | discarded to `/dev/null` |

Every one was issued as `curl -s -o /dev/null -w '%{http_code}'`. **No response
body was read, parsed, stored, or entered any file or any reasoning step. No
open, high, low, close, volume or any function of one was observed.** What was
observed is exactly three integers — 401, 200, 200 — plus three elapsed times,
all of which are inside the readable field list of the blindness section
(vendor response status code).

**What this does and does not damage.** It does not damage outcome blindness:
no bar value was seen. It does not damage the pre-registration of the
*hypothesis*, the *bars*, or the *cost model*, none of which existed or could
have been informed by three status codes. It **does** breach the literal
ordering clause of TASK 4 and TASK 5, and the correct response under standing
rule 5 is to record it loudly at the top of the log rather than to argue it
away. It is carried into DECISIONS.md as **ADR-001** and is named again in the
Section 0 disclosure block, so that a reader of the registration meets it there
rather than only here.

**What was not done.** The calls were not repeated, no `robots.txt` had yet been
recorded for any of the three hosts, and no further request of any kind was sent
until STAGE A.1 TASK 1 recorded terms and `robots.txt` first, as standing rule
12 requires.

---
## Entry 1 — STAGE A.-1 TASK 0 and TASK 1, and STAGE A.0 TASK 2

**2026-08-29.** ETA stated before arming, actual recorded after, per standing
rule 2.

| task | ETA | actual | verdict |
|---|---|---|---|
| A.-1 TASK 0 — preconditions and duplication screen | 8 min | 9 min | PASS, CLEAR |
| A.-1 TASK 1 — prompt log | 4 min | 5 min | done |
| A.0 TASK 2 — scaffold and the seven guards | 45 min | 41 min | `make all` green |

**TASK 0, preconditions.** Working tree `/home/kiros-li/Documents/GitHub/ORBExperiment`
confirmed; `main` tracks `origin/main`; `git push --dry-run` returned
`Everything up-to-date`. Toolchain: `uv 0.12.0`, host `python3 3.14.4`, venv
pinned to `3.13.14` by `make install` against the `requires-python = ">=3.13"`
floor. `.gitignore` verified as already covering `.env`, `data/`, `.venv/`,
`__pycache__/`, `*.pyc`, `.mypy_cache/`, `.pytest_cache/`, `.ruff_cache/` and
`*.egg-info/` — nothing added.

**TASK 0, duplication screen. Verdict CLEAR**, recorded in full at
`docs/DUPLICATION.md`. 11 repositories screened, 8 patterns, **14,002 raw hits,
0 substantive**. The five design-bearing patterns — `opening range`,
`opening candle`, `relative volume`, `intraday breakout`, `stocks in play` —
returned **zero hits in every repository, n = 11**. The 14,002 are: `9:30` as a
substring of package-index upload timestamps and stored vendor clocks, `09:30`
as a US session boundary in AiTrader's news horizon and NPLExperiment's funding
session tags, `ORB` as a Solana launchpad token symbol in 33 `solattn` manifest
rows, and one `"09:30"` market-hours string in an HFExperiment broker-calendar
fixture. Each class is cleared with its reason in DUPLICATION.md. The prompt's
expected CLEAR is **verified, with one refinement**: two repositories do reach
US equities — HFExperiment reaches an equity *broker* and is the source of the
integer-share constraint carried here, and AiTrader carries a session boundary
for a *news* horizon — and neither reads intraday price structure.

**TASK 0, prior art.** All eight files read for pattern, not text:
ETFExperiment `CLAUDE.md` (operating-manual shape, blindness field lists,
carve-out paragraph, Section 0 fire function), `REGISTRATION.md` (Section 0
shape including its registered residual band and fixed precedence order),
`DECISIONS.md` ADR-001 (provisional-parameter-with-one-permitted-amendment);
NPLExperiment `REGISTRATION.md`, `HYPOTHESES.md` (register style, latch,
quarantine, closure), `progress.md` (a falsified planning figure recorded
rather than corrected), `docs/STAGES.md` (ladder table with entry gate, exit
gate and capital columns); MLCryptoEngine `HYPOTHESES.md` H11 (the measured
75-day lag and whole-file regeneration that killed it) and `DECISIONS.md`
ADR-055 (fee re-verification: a carried figure is a dated measurement);
solattn `DECISIONS.md` ADR-019 (seal the closed day, never the open one; a
missing attestation is an error, never a pass) and ADR-021 (**ceilings are per
endpoint, never per host** — 47.5 percent refusals on one endpoint at n = 1,863
attempts while a second endpoint on the same host and IP took 0 of 360);
InsiderExperiment `progress.md` (power-gate closure shape, boundary-fixture
mutation lesson).

**TASK 2, scaffold.** `uv` project, package `orb`, `src` layout, Python 3.13
floor. ruff, mypy strict, pytest, pre-commit. Makefile with `install`, `lint`,
`fmt`, `typecheck`, `test`, `all`, `guards`, `mutations`. `.env.example` left
empty on purpose — **no Stage A source needs a key**. All seven guards ported
by shape, not text:

| guard | site | pinned by |
|---|---|---|
| 1 — recorded absence | `orb.absence.Absent` | refuses `float`, `int`, `index`, `+` both ways, `-`, `*`, `/`, ordering, `bool`, indexing, iteration, `len` |
| 2 — parse-tree config enforcement | `tests/test_guards.py` | every `Config` field read outside `config.py` or on `PENDING_ENFORCEMENT` with its task named; stale entries also fail |
| 3 — append-only fsynced ledger | `orb.ledger` | `O_APPEND` + `fsync`; a truncated line returns `TruncatedLedgerLine`, the file is left damaged |
| 4 — the seven call states | `orb.callstate` | two disjoint enums, no supertype; `combined_total()` raises |
| 5 — priced-bar blindness | `tests/test_guards.py::test_no_module_reads_a_priced_bar_field_anywhere` | AST walk over attribute, subscript and `.get`/`.pop`/`.setdefault` forms |
| 6 — pre-period date pin | `orb.preperiod` | boundary `2016-01-04T14:30:00.000Z` exclusive; fixtures sit **on** it |
| 7 — session clock | `orb.sessionclock` | refuses naive datetimes and fixed-offset "Eastern"; AST guard forbids `timezone(...)` and `America/New_York` outside `sessionclock.py` |

**The blindness guard caught a real read on its first run against real source,
and that is recorded rather than smoothed.** `orb/ledger.py:102` used
`self.path.open("r", ...)` — `Path.open`, an attribute named `open`, which is a
bar field in every vendor dialect. **The source was changed, not the guard.**
`iter_rows` now reads via `read_text` and splits with `keepends=True`, which
preserves the no-terminating-newline truncation detection exactly. The one
receiver allowlisted anywhere is `os`, for `os.close(fd)`, named explicitly in
`SAFE_ATTRIBUTE_RECEIVERS` with its reason; a bar is never bound to the name
`os`. **A guard that has never been shown to catch anything is an assertion
about nothing**, and this one caught something on day one.

**Boundary verified, not assumed.** `CONFIG.pre_period_end_ms = 1451917800000`
resolves to `2016-01-04T14:30:00+00:00`, and `test_preperiod.py` proves
independently that 14:30Z **is** 09:30 Eastern on that date because 2016-01-04
falls in standard time. The DST cost is measured rather than asserted:
`test_a_fixed_offset_would_mis_slice_a_third_of_the_sample` counts the calendar
days of 2016-01-04 to 2026-06-30 on which a fixed −05:00 offset resolves 09:30
Eastern to the wrong UTC instant and requires the share to exceed one third,
**n = 3,831 days**.

**`make all` green on the scaffold: ruff format and check clean, mypy strict
clean across 15 source files, 61 tests passed.**

---
## Entry 2 — STAGE A.0 complete, and STAGE A.1 TASK 1 and TASK 2

**2026-08-29.**

| task | ETA | actual | verdict |
|---|---|---|---|
| A.0 TASK 3 — CLAUDE.md | 12 min | 11 min | done |
| A.0 TASK 4 — Section 0 and its fire function | 20 min | 23 min | registered, 576-cell lattice green |
| A.0 TASK 5 — Sections 1–12 | 35 min | 32 min | registered before any vendor data request |
| A.0 TASK 6 — Section 13, priors | 5 min | 4 min | operator slot **empty** |
| A.0 TASK 7 — Section 14 and HYPOTHESES.md | 18 min | 19 min | amendment log open, H1 OPEN |
| A.1 TASK 1 — access verification | 55 min | 58 min | **0 of 9 vendors usable** |
| A.1 TASK 2 — rate ceilings | 30 min | 21 min | **no ceiling measurable on any data endpoint** |

### The finding that changes this session's shape

**Measured: 0 of 9 vendors serve 1-minute regular-session US equity bars to this
repository today.** n = 15 hosts fetched for `robots.txt`; n = 7 live API
probes; **n = 0 returned a bar.**

The nine split on **terms first**, and the split is the finding:

- **`stooq.com` and `query1.finance.yahoo.com` — the only two that serve
  keylessly — both publish `User-agent: * / Disallow: /`.** Standing rule 12:
  *do not proceed against a stated prohibition.* Neither is fetched again.
  `finance.yahoo.com` additionally names **`ClaudeBot`, `anthropic-ai`,
  `Claude-Web`, `GPTBot`, `CCBot`, `Scrapy`** and 30 others in a group carrying
  `Disallow: /`.
- **`eodhd.com` disallows `/api/`**; **`data.nasdaq.com` disallows
  `/api/*.json*` and `/api/*.csv*`** — the exact paths a collector needs.
- **The five whose terms permit it all refused without a credential**, n = 7
  probes: Polygon **401 `"API Key was not provided"`**, Alpaca **401
  Authorization Required**, Databento **401 `"Not authenticated"`**, Tiingo
  **403 `"Please supply a token"`**, Alpha Vantage **200 carrying a refusal**.

**This falsifies a planning assumption carried in the operator prompt**, which
states `.env.example` is empty on purpose because *"no key is needed for any
Stage A source."* **It is recorded as falsified, not worked around** — the
NPLExperiment correction, where a planning figure near 9.4 events per month met
measurement at **0.5, n = 3 over 182 days**, and the hypothesis died on a figure
rather than on the world.

### Two findings inside the finding

**One: Alpha Vantage refuses with HTTP 200.** The demo key returns `200` with an
`Information` string and no series; the delisted `LISTING_STATUS` query returns
a **2-byte body, `{}`**, also at `200`. **This is exactly the health/composition
merge Guard 4 exists to prevent** — a status-code-only classifier records
`stored` and then counts a session with zero bars. **It caught this
repository's own client**: `orb.http.PacedClient` labelled the refusal `stored`.
**Recorded as ADR-008 rather than smoothed**, with the fix scoped to A.3 TASK 1
because no Alpha Vantage row is admitted to anything before then.

**Two: `polygon.io` 301-redirects to `massive.com`.** The prompt's "also branded
Massive" is **measured, not assumed**. And `alpaca.markets/robots.txt` returns
**200 with 81,041 bytes of HTML** — a styled 404 page. **A 200 is not a
robots.txt**, and it is recorded as "no robots.txt served", not as "permitted".

### A.1 TASK 2, and what it is not evidence about

n = 18 requests, 3 endpoint-spacing cells, **0 refusals on a limit**. Polygon
admitted **8 of 8 at 88.4/min** (all 401); Alpha Vantage **5 of 5 at 29.1/min**
(all 200-carrying-a-refusal). **None of this licenses a pace.** solattn ADR-021's
corollary applies to this repository's own measurement: **the only reachable
path on every permitted vendor is the unauthenticated refusal path, and a
ceiling measured on a 401 is not evidence about the authenticated data
endpoint.** Polygon documents 5/min; the measured 88/min **does not contradict
it**, because they are different endpoints. Pacing is therefore registered
**provisionally and labelled unmeasured** at the conservative 6.0 s default
(Amendment 2).

### Two amendments, both made while holding zero bars

**Amendment 1** registers a fourth Section 0 state, **`PENDING_ACCESS`**,
evaluated ahead of every BLOCKED trigger, for the case where an integrity input
is `Absent` because no vendor is reachable. Without it the map would have to
read a missing measurement as a failed one and close H1 as
`source-integrity-blocked` **on evidence that does not exist**. It arms nothing,
it is a verdict on access rather than on H1, and it is pinned as **not a
bypass**: a test walks the present-input space and requires the clause to be
inert the moment both measurements exist. GO, DEGRADED and BLOCKED are unchanged
in text, threshold and precedence.

**Amendment 2** registers pacing provisionally and labelled unmeasured.

**Both were written while this repository held zero bars, zero prices, zero
volumes and zero sessions**, which is what makes them un-fittable to a result:
there is no result.

### What this costs, stated plainly

**A.1 TASK 3 and A.1 TASK 4 are the two tasks this repository turns on, and
neither can be executed without two credentialed vendors — a primary and a
secondary.** That is now an **open operator item**, and it is the second of
exactly two; the first is the Section 13 prior slot.

**Stage A already could not finish today**, because A.1 TASK 3 registers a
**≥ 14 calendar-day wait** between the probe pull and the re-pull. **That wait
has not started, and cannot start until a credential exists.** The earliest
Stage C date moves with the credential date, not with today.

**Everything not dependent on vendor bars is still built and delivered in
full** — the session calendar, the cost model, the universe, signal and verdict
machinery built dark against synthetic fixtures, the power gate, the latch
machinery, the guards and the mutation harness. **Only the two integrity
measurements wait, and they wait on an operator item rather than on a design
question.**

---
## Entry 3 — STAGE A.1 TASK 3 and TASK 4, machinery built and armed

**2026-08-29.**

| task | ETA | actual | verdict |
|---|---|---|---|
| A.1 TASK 3 — bar revision machinery | 40 min | 36 min | **built and armed; measurement blocked on credential** |
| A.1 TASK 4 — agreement and delisted machinery | 40 min | 33 min | **built and armed; measurement blocked on credential** |

**Neither measurement was taken, and neither figure is invented.** Both findings
sit as `Absent(not_yet_measured, "no credentialed vendor")` and Section 0 fires
**PENDING_ACCESS** on them (Amendment 1). **Standing rule 5: absence is a
recorded state, never a synthesized value.** What was built is the machinery
that fires the moment two credentials exist, with its behaviour pinned against
synthetic fixtures whose answers were computed by hand.

**The sealed comparator, `orb.comparator.SealedComparator`.** It reads price and
volume from two vendors, in integer cents — **float equality on money is a
bug** — and returns **only** a `RevisionFinding` or an `AgreementFinding`, every
field of which is an `int` or a `float` count. It is pinned four ways:

- `test_comparator_returns_no_bar_value` walks the parse tree and requires every
  **public** method's return annotation to be a counts-only record or a scalar;
- `test_comparator_findings_carry_only_counts` requires every field of both
  records to be `int` or `float` and to carry no priced-field name;
- `test_the_comparator_returns_no_bar_value_at_runtime` checks the returned
  object holds neither `10.50` nor `1050` — the fixture's own opening-range high
  in dollars and in cents;
- `test_the_comparator_is_the_only_module_that_reads_a_priced_field` requires
  that `comparator.py` **does** read priced fields and that `seal.py` does not.

**Known answers, hand-computed and pinned.** One revised bar in five measures
**exactly 0.20** and fires `FAIL`; an unchanged re-pull measures **0.0** and
fires `PASS`; a one-cent disagreement **inside** the opening range breaks the
pair while a disagreement **outside** it does not; a bar stamped **exactly at
09:35:00.000** is outside the half-open range; and a clean re-pull taken at
**13 days** reports `wait_satisfied() == False`, so a re-pull taken too early is
**not evidence of a clean vendor**.

### Guard 5 had a hole, the comparator found it, and the guard was widened

**Recorded rather than smoothed.** `test_the_comparator_is_the_only_module_that_reads_a_priced_field`
failed on its first run with `assert []` — **the guard could not see the
comparator reading OHLC at all.** The reason is structural: the comparator reads
through a **variable alias**,

    for aliases in (("o", "open"), ("h", "high"), ...):
        for alias in aliases:
            if alias in bar: found = bar[alias]

and a walk that matches only **constant** subscripts, attributes and `.get`
calls is blind to it. **A guard with that hole would have passed a module that
reads every priced field on every bar.**

**The guard was widened, not the test relaxed.** A fourth detection form was
added — **a bare string constant naming a priced field, anywhere** — because
naming the field at all is the reachable signal. Two consequences were handled
rather than worked around:

1. **The declaration site would flag itself.** `PRICED_BAR_FIELDS` was moved out
   of `seal.py` into a new `orb/fields.py`, **a registry containing names and no
   logic at all**, and that one module is the guard's single structural
   exemption. `seal.py` now imports the list and reads **zero** priced fields,
   which the guard asserts directly.
2. **A constant subscript is also a string constant**, so findings are
   deduplicated by `(line, field)` keeping the more specific form. The direct
   probe still reports exactly three forms; a separate indirect probe —
   `for k in ('high',): return bar[k]` — reports `string constant`, and both are
   pinned.

**A guard that has never been shown to catch anything is an assertion about
nothing.** This one has now caught two real reads in this repository's own
source: `Path.open` in `ledger.py` at A.0 TASK 2, and its own blindness to
variable-alias access at A.1 TASK 3.

---
## Entry 4 — STAGE A.2 TASK 1, TASK 2 and TASK 3

**2026-08-29.**

| task | ETA | actual | verdict |
|---|---|---|---|
| A.2 TASK 1 — calendar and actions substrate | 30 min | 34 min | 2,637 sessions, 21 half sessions |
| A.2 TASK 2 — cost model, verified and frozen | 35 min | 38 min | **one carried figure stale, three components missing** |
| A.2 TASK 3 — universe, signal, verdict built dark | 50 min | 52 min | 10 hand-computed cases match to the cent |

### A.2 TASK 1 — the calendar

**2,637 sessions and 21 half sessions**, 2016-01-04 to 2026-06-30, built from
the NYSE holiday and early-closing rules encoded in `orb.calendar` rather than
downloaded, so it is reproducible without a vendor. **Two disagreements with the
registration, recorded not reconciled: in-sample computes 1,762 against a stated
~1,760, and the holdout computes 875 against a stated ~880.** The holdout
shortfall is carried into A.2 TASK 4 and the computation wins, as Section 9
requires. At the registered assumption, `t` moves from **2.616 at n = 880** to
**2.609 at n = 875** — **no verdict row moves**, and both sit below the 3.0
hurdle and above the 2.50 gate.

**The second-source cross-check was not completed and was not fabricated.** Every
vendor serving a machine-readable calendar is one of the nine that refused, so it
is `Absent(not_yet_measured)`. What stands in is real: the session count is
derived **twice by different arithmetic** and the two agree on all 10 complete
years, and the opening-range start of the first in-sample session equals
`CONFIG.pre_period_end_ms` **exactly** — the calendar and the carve-out boundary
computed two independent ways, from a NYSE rule set and from a registered literal.

### A.2 TASK 2 — the cost model, and the ADR-055 pattern firing as designed

Live against IBKR's published schedule (**HTTP 200, 584,282 bytes, 2026-08-29**),
terms checked first:

| component | carried | **measured** | verdict |
|---|---:|---:|---|
| commission per share | 0.0035 | **0.0035** | agrees |
| order minimum | 0.35 | **0.35** | agrees |
| FINRA TAF per share sold | 0.000166 | **0.000195** | **STALE, 14.9 percent low** |
| maximum per order | not modeled | **1 percent of trade value** | **NOT MODELED** |
| FINRA CAT | not modeled | **0.000003/share** | **NOT MODELED** |
| NSCC/DTC clearing | not modeled | **0.00020/share** | **NOT MODELED** |

**The 1 percent cap can bind below the 0.35 minimum**, and the minimum does not
survive it: 10 shares at 1.00 USD is a 10.00 USD trade whose cap is **0.10**.
Pinned.

**The SEC fee schedule is registered EMPTY on purpose.** One rate was measured
(**0.0000206 × value of aggregate sales**); **its effective date was not**, and
`sec.gov` returned **403 "Request Rate Threshold Exceeded"** on both attempts,
20 s apart. Placing the 2026 rate in the schedule would silently apply it to a
2016 session, so `rate_on` returns `Absent` for **every session in the registered
window** and the whole round-trip cost refuses. **The model will not price a
trade it cannot price honestly.** Pinned by test.

**What it costs the hypothesis, measured.** A round trip at the central band on a
50 USD name costs **≈ 0.0386 USD/share on a close exit and ≈ 0.0686 on a stop
exit**, against the replication's measured gross edge of **0.070 USD/share**
(carried, C-6). **A close exit consumes 55 percent of the edge; a stop exit
consumes 98 percent. Slippage is 78 percent of the close-exit total.** Section
6's claim that the cost band is the experiment's second axis is now a measured
number rather than an assertion, and it **strengthens the DEGRADED expectation
registered in Section 0 before any of this was measured.**

Frozen at sha256 `3789221b9dd3fea5a9680547dfdf8ec7b1febaf246042fe1fa70e27ca610fba3`,
latched, and pinned by a test that recomputes the hash from the model.
**Amendment 3** records all of it, before A.2 TASK 4.

### A.2 TASK 3 — built dark, and a stronger guarantee than blindness

An opening-range rule **is** a statement about highs and lows, so the strategy
modules cannot be blind. A stronger guarantee replaces the blindness pin:

1. **Structural — they are unreachable.** `bars.py`, `universe.py`, `signal.py`
   and `verdict.py` are `LATCHED_MODULES`, and
   `test_no_stage_a_module_imports_a_latched_module` walks **every import in the
   package** and requires that no module outside the set imports one of them.
   **Nothing on the Stage A collection path can call the strategy, whatever
   anyone later forgets.**
2. **Behavioural — they refuse at runtime.** Every bar carries a `Provenance`.
   `SEALED_VENDOR` is refused by every entry point until the Stage C latch;
   `PRE_PERIOD` is checked against the boundary rather than trusted, so a bar
   *claiming* the carve-out at the boundary instant is rejected at construction.

**The ten hand-computed ticker-sessions matched to the cent on the first run.**
Every opening range, breakout price, stop and close exit was computed on paper
first; all ten agreed. They cover **all four registered trigger states** — LONG,
SHORT, NONE and AMBIGUOUS. Named fixtures also pin: a bar stamped **exactly** at
09:35:00.000 sitting outside the half-open range; a **touch** of the boundary not
being a break; **the stop and the range boundary coinciding to the cent**, where
a touch at 950 is a hit and 951 is not; the **one-cent entry-offset floor**
binding on a 1.60 USD name where 0.05 percent is 0.08 cents; and a **half
session**, whose exit window shifts three hours.

**A recorded limitation.** The ten bars are **synthetic fixtures stamped inside
the carve-out window, not real vendor bars**, because 0 of 9 vendors serve one.
Provenance and boundary are genuinely exercised; the prices are constructed.
**When a credential exists these same ten ticker-sessions are re-run against real
pre-period bars and the hand computations redone.** Recorded as an open item and
stated in the test module's own docstring, not only here.

**The canary fires and the converse holds.** A planted edge at annualized Sharpe
3.0 over 875 sessions clears both co-primaries and both gates; **pure noise
clears neither**. And `test_all_four_conditions_are_required` shows a run that
passes E1, E2 and persistence but fails concentration **still fails overall** —
so no gate can quietly become advisory.

**Bar construction caught one of my own malformed fixtures** (`open` below
`low`) on its first run, which is the validator doing its job on the day it was
written.

**`make all` green: 224 tests, mypy strict clean over 38 files.**

---
## Entry 5 — STAGE A.2 TASK 4 and TASK 5, and STAGE A.3

**2026-08-29.**

| task | ETA | actual | verdict |
|---|---|---|---|
| A.2 TASK 4 — power gate | 30 min | 27 min | **DEGRADED expectation confirmed by computation** |
| A.2 TASK 5 — fire Section 0 | 12 min | 14 min | **PENDING_ACCESS** |
| A.3 TASK 1 — production collector | 30 min | 24 min | built, **inert** |
| A.3 TASK 2 — actions watcher | 18 min | 13 min | built, **inert** |
| A.3 TASK 3 — systemd | 22 min | 17 min | units written, **no timer enabled** |
| A.3 TASK 4 — latch machinery | 25 min | 26 min | built and pinned |

### The power gate

**The registered expectation was recorded before the evidence, and the evidence
matched it.** Section 0 stated in writing, before any measurement existed, that
the arithmetic pointed to DEGRADED. The computation — on a session count derived
from a NYSE rule set, not from the prompt — confirms it by the exact mechanism
the DEGRADED clause names:

| assumption | annual Sharpe | **E1 power at n = 875** | against the floors |
|---|---:|---:|---|
| published (undecayed) | 2.81 | **0.9995** | above the 0.80 GO floor |
| **REGISTERED (half)** | **1.40** | **0.7435** | **below the 0.80 GO floor** |
| quartered | 0.70 | **0.2578** | below the 0.50 BLOCKED floor |

**Minimum N at the registered assumption is 1,006 against 875 achieved — a
shortfall of 131 sessions.** And a knife-edge recorded precisely: extending the
holdout to **2026-12-31** gives **1,003 sessions and power 0.7991**, short of
0.80 by **0.0009** and short of the required count by **three trading days**.
2027-06-30 gives 1,126 and **0.8425**, which clears. **That is recorded now,
while this repository holds no result that would make the extension tempting.**

**Two disagreements with the prompt, the computation winning as Section 9
requires.** Minimum N to clear t = 2.0 is **515, not 514** — at n = 514 the
statistic is **1.9994**. To clear t = 3.0 it is **1,158, not 1,157** — at 1,157
it is **2.9998**. The prompt states floors; a minimum-N ceilings. One session
each, in the conservative direction, and **no verdict row moves**.

**And one figure in the prompt turns out to contain an assumption.** The stated
per-trade information ratio "near 0.031" for t = 3.0 corresponds to **9,362
trades**, i.e. a **53.5 percent trigger rate** at 20 names over 875 sessions —
and the prompt itself says the trigger rate is *"to be measured rather than
assumed."* At a 100 percent trigger rate the figure is **0.0227**. Reported with
the assumption made explicit.

**E2 power is `Absent` in all nine cells.** Section 9 restricts its dispersion
input to the pre-period carve-out; no vendor serves one. The absence refuses
coercion, so it cannot be summed into a power figure by accident.

### Section 0, fired

> **PENDING_ACCESS** · `PENDING-ACCESS Amendment 1`

**Nothing is armed. Nothing is closed. H1 remains OPEN.** It is explicitly not
the `source-integrity-blocked` closure kind — that requires a vendor whose bars
were **measured** and found unstable, and **no bar has been served to fail**.

**The counterfactual is computed and recorded: had bar integrity passed in full,
the same power inputs fire `DEGRADED`.** Recorded in Amendment 4, in
HYPOTHESES.md, and in the append-only ledger, with every input beside it.

### Stage A.3 — built, and deliberately inert

A.3 is registered as armed *only on GO or DEGRADED*, and `PENDING_ACCESS` is
neither. Everything is written, tested and committed; **no timer is enabled.**

**The CLI entry points refuse loudly and exit 78**, rather than running and
storing nothing — because *a collector that runs and stores nothing looks
identical in a log to one that ran and found nothing*, which is the
health/composition merge standing rule 7 forbids. Pinned by test.

**Unit-name collision verified against the live system, not assumed.**
`systemctl --user` shows `npl-daily`, `npl-watch`, `etf-snap`, `etf-daily`,
`solattn-daily`, `news-collect` in use as the prompt said, **and three the prompt
did not name — `hfexperiment-bars`, `solattn-collect`, `solattn-watch`.**
`orb-daily` and `orb-actions` are free. A guard pins the non-collision, the
22:15/22:45 UTC schedule, `Persistent=true` and `MemoryMax=2G`.

**The classifier now reads the body, not only the status code** (ADR-008),
because A.1 TASK 1 measured a vendor **refusing at HTTP 200**. A 429 or a 5xx
writes a loud error marker and is **never** read as no-data; an `Information`
string at 200 is `source_failed`, and an empty `{}` at 200 is `no_data`.

**The open session is never sealed** (the solattn ADR-019 shape): sealing a
session on or after today raises. A changed bar on a **closed** session appends a
revision row carrying **both hashes and both pull timestamps**, which turns the
MLCryptoEngine H11 hazard from a discovery into a measurement.

**The latch refuses every registered way.** A second read of a window raises with
*"a second read of this window voids the hypothesis"*; Stage D refuses before
Stage C's latch exists; an **empty or unlabelled operator prior slot blocks it
structurally**; and a **failed attempt leaves no file**, so a refusal never
consumes the one read the window has. The quarantine guard walks every module
for a string naming a spent-read artifact, with `latch.py` the only exemption.

**`make all` green: 270 tests, mypy strict clean over 46 files.**

---
