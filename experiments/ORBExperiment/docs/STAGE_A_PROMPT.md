# ORBExperiment Stage A operator prompt

Paste everything between BEGIN PROMPT and END PROMPT into the coding CLI.

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
