# ETFExperiment — progress

Repo created 2026-08-28. Measurement-only. Stage A never trades, never touches capital,
never reads an outcome value.

---

## Entry 0 — 2026-08-28T07:53:57Z — Governing prompt, logged verbatim before any other work

Logged under the standing rule "Log this prompt verbatim to progress.md before any other work."
Reproduced below between the BEGIN PROMPT and END PROMPT markers exactly as received.

BEGIN PROMPT

ETFExperiment, Stage A. Effort: high. Run autonomously. Commit at each sub-stage boundary. Push nothing.

Purpose. Stand up a new measurement-only experiment repo at /home/kiros-li/Documents/GitHub/ETFExperiment testing one hypothesis: US spot Bitcoin ETF net flow prints predict the next day's BTC return, out of sample, by enough to clear a round trip on Hyperliquid perps. Stage A registers the design, verifies access, measures the publication lag and the revision rate of the flow source, censuses the admissible days, fires a power verdict, and arms collectors. Stage A never trades, never touches capital, and never reads an outcome value.

The measurement that decides this repo is not the return. It is the publication lag and the revision rate. Treat STAGE A.1 : TASK 3 and STAGE A.1 : TASK 4 as the experiment.

Standing rules, in force for every task.

Log this prompt verbatim to progress.md before any other work.
State an ETA before arming each task. Record actual against ETA after.
Measured beats documented. Verify every external figure live before relying on it.
Absence is a recorded state, never a synthesized value. A refusal is loud, never a silent skip.
Ledgers are append-only and fsynced. A truncated line is reported, never repaired.
Operational health and sample composition never merge. Call states: stored, no_data, source_failed, rate_limited, excluded_ineligible, expired.
Outcome blindness. Outside the sealed writers, no code path parses a BTC price, open, high, low, close, volume, or any return derived from one, and no code path reads a funding rate stamped inside a hold window, until the registered Stage B read. Flow values are signal, not outcome, and are readable. Coverage modules count rows and timestamps only. Tests pin every one of these absences.
Pre-period carve-out, the one exception, registered here so it is not discovered later. Power inputs may read BTC price and funding data strictly before 2025-05-01, which is inside the source study's own sample and outside this test sample. Enforced by a date pin in code and by test. Every other price read is sealed.
Union time intervals before summing. Order multi-process logs by clock, never by file position.
Zero dollars. Keyless public endpoints only. A request ledger with a daily cap charges before sending.
Terms of service bind. Record robots.txt and the published terms verbatim for every source before the first automated fetch. If automated collection is disallowed, record it loudly and route the access verdict accordingly. Do not proceed against a stated prohibition. The HFExperiment Wealthsimple finding is the precedent.
Every figure travels with its n in the same sentence.

Prior art to read before TASK 0, for patterns not text.
/home/kiros-li/Documents/GitHub/NPLExperiment/REGISTRATION.md and HYPOTHESES.md, for the register style, the latch protocol, the quarantine, and the closure shape.
/home/kiros-li/Documents/GitHub/NPLExperiment/progress.md, for how a falsified planning figure gets recorded rather than quietly corrected, and for the Section 0 cull firing on measured rates.
/home/kiros-li/Documents/GitHub/MLCryptoEngine/HYPOTHESES.md, entry H11, and report.md line 2734. This is the direct precedent. A free flow source with a measured 75-day publication lag, whole-file regeneration, past rows revise. The class died on the lag, not on the model.
/home/kiros-li/Documents/GitHub/MLCryptoEngine/DECISIONS.md, ADR-055, for the fee re-verification pattern.
/home/kiros-li/Documents/GitHub/solattn/DECISIONS.md, ADR-019, ADR-021, ADR-022, for seal discipline, per-endpoint pacing, and expiry-first ordering.
/home/kiros-li/Documents/GitHub/InsiderExperiment/progress.md, for the power-gate closure shape.

Figures carried into the registration, sources named there, none of them measured by me.

Source study. Boon Chuan Lim, The Price Impact of Spot Bitcoin ETF Flows, SSRN abstract_id 6592830, posted 2026-04-17. Five largest US spot BTC ETFs, January 2024 through April 2025, 313 trading days, Databento. Reported: 53 bp per 100M USD same-day OLS, 74 bp under instrumental variables with first-stage F 21.58, flows explaining 21 percent of daily return variation at t 8.99, next-day prediction at Newey-West t 3.12, bidirectional Granger causality beta 0.47 at t 9.75, no unconditional reversal at horizons 1 through 20 days, significant conditional reversal after controlling for future flows at t minus 2.42 to minus 3.99, total impact 96 bp per 100M at 10 days at t 4.49.

The same author, later and longer. SSRN abstract_id 6567058, 563 days January 2024 through April 2026, Farside data, causal IV impact 0.20 percent per 100M at t 2.65, against the earlier 0.41 percent OLS. The author's own estimate roughly halves on the extended sample. This is the single most important figure in this prompt.

The claimed external replication does not replicate the tradable leg. Citi's note of 2026-07-01 cut its twelve-month BTC target to 82,000 USD and cut assumed twelve-month net ETF inflows to zero. Reporting shows Citi cited an external academic study rather than running its own regression, and the dataset description is Lim's. Citi's own quantified claim, from analyst Alex Saunders, is that flows explain roughly 45 percent of weekly BTC moves. Weekly and contemporaneous, not next-day and predictive. Record it in the registration as FAILED TO CONFIRM, not as corroboration.

Contradicting evidence. HashKey senior researcher Tim Sun, August 2026: single-day ETF flows alone yield very limited predictive power for the next trading day, long-term correlation coefficient below 0.5, roughly 0.4 percent per 100M, a lagging trend-confirmation indicator rather than a leading one. CoinDesk, 2026-05-14, using SoSoValue data: the 90-day rolling coefficient between daily BTC return and daily change in cumulative net inflows stands at 0.16, indistinguishable from zero, down from a February peak of 0.68.

Regime. June 2026 net outflows reached 4.06 billion USD, the worst month since launch in January 2024, inside a 13-day consecutive outflow streak totalling roughly 4.4 billion.

In-house, from the repos. Hyperliquid base perp fees 1.5 bp maker and 4.5 bp taker per side. Kraken Pro base tier 0.25 percent maker and 0.40 percent taker, ADR-055, verified live 2026-08-08. Coinbase base tier 0.40 maker and 0.60 taker, ADR-055, already correct and not in dispute. IBKR refuses fractional-sized orders through the API with error 10243, HFExperiment reports/stage_a1b/a1b_report.md line 52, so no equity-side implementation exists.

Assistant prior, recorded 2026-08-27 in chat: 0.10 on a real capturable edge existing here. Nothing found in the repos or on the web since has moved it. The NPD Amendment 0 lesson applies. An adopted prior corrupts the calibration ledger. The operator prior slot stays empty. Do not fill it.

The correction that governs this repo. In NPLExperiment a main-dex accrual figure near 9.4 events per month entered a registration as a planning number and measurement falsified it at 0.5, n equals 3 over 182 days, killing H3 on a figure rather than on the world. No accrual, coverage, lag, retention, revision, or capture-density figure in this repo is registered before it is measured. Every such figure below is named as an A.1 or A.2 measurement target, never as an input.

STAGE A.0 : TASK 0. Repo init and prompt log.
Create the repo, git init, write progress.md with this prompt verbatim as its first entry, read the six prior-art files.

STAGE A.0 : TASK 1. Scaffold.
uv project, package etf. ruff, mypy strict, pytest, pre-commit, Makefile with lint, typecheck, test, all. .env.example empty on purpose, no keys needed. .gitignore covering .env, data/, .venv. Port the four standing guards by copying shape from NPLExperiment and InsiderExperiment: a recorded-absence type refusing numeric coercion, the parse-tree config-enforcement guard, the append-only fsynced ledger primitive, the call-state enum with the six states above. Add a fifth guard specific to this repo: a pre-period date pin that refuses any price or funding read stamped on or after 2025-05-01 outside the sealed writers.

STAGE A.0 : TASK 2. CLAUDE.md.
The standing rules above, plus the blindness field lists stated exactly.
Flow payload fields readable outside sealed writers: every field, including the flow values themselves, plus the capture timestamp. Flow is signal.
Price payload fields readable outside sealed writers: t, T, and row count only. Never o, h, l, c, v.
Funding fields readable outside sealed writers: time always, fundingRate only where time is strictly before 2025-05-01 under the pre-period carve-out.
State the carve-out in one paragraph with its rationale and its enforcement site.

STAGE A.0 : TASK 3. REGISTRATION.md Section 0, committed before any network call.
The outcome map judges collection feasibility and detectability, never returns.
GO: both co-primaries of Section 8 reach at least 80 percent power at alpha_adj under the registered effect assumption of Section 9, at the achievable admissible-day count by 2027-03-31, and the as-printed observability test of A.1 TASK 4 passes in full.
DEGRADED: E1 reaches at least 80 percent power at the published-magnitude assumption but under 80 percent at the registered assumption, or as-printed observability passes partially. Collection proceeds. The verdict scope narrows, and the registration states the narrowing in plain words before any data exists: under DEGRADED a Stage B FAIL establishes that the effect is not present at its published magnitude, and cannot distinguish a decayed effect from no effect at all. Recomputed power stated beside the registered target.
BLOCKED: E1 under 50 percent power at the published-magnitude assumption at the achievable count by 2027-03-31, or as-printed observability FAIL, or a measured revision rate high enough that no stable as-printed value exists before the entry anchor on a majority of days. Nothing armed beyond the census.
Enforced by a fire function with tests.

Registered expectation, stated now so the verdict reads as a documented answer rather than a disappointment. The arithmetic in Section 9 and the decay evidence above point to DEGRADED. Say so in the registration. A DEGRADED here narrows a question rather than abandoning it, and a BLOCKED is a documented answer, not a failure of process.

STAGE A.0 : TASK 4. REGISTRATION.md Sections 1 through 12, committed before any network call.

Section 1, hypothesis. A daily rule that takes a directional Hyperliquid BTC perp position after a US spot Bitcoin ETF net flow print, using only the value published and timestamped before the entry anchor, earns a positive return net of costs over the out-of-sample period. State it as a joint claim about the signal and about information timing, and state the two structural doubts as part of the hypothesis rather than as caveats. Publication timing: the signal was published openly in April 2026 and the author's own estimate halved on a longer sample. Information timing: the flow print lands after the US close the return is measured against, so the same-day leg is untradable by construction and only the next-day leg is testable here.

Section 2, universe and event rule. One instrument, Hyperliquid BTC perp. One event per US trading day on which an admissible as-printed flow value exists. Days are never filtered on any price or return quantity. The five largest US spot BTC ETFs by assets are the flow universe, named explicitly in the registration by ticker, with the aggregate net flow as the signal and per-fund values retained as descriptive.

Section 3, the print, the anchor, and admissibility. This is the section the repo turns on.
The as-printed value for US trading day D is the aggregate net flow for D as served by the flow source in a capture strictly before the entry anchor. The value taken is the one in that capture. A later value for the same day, however authoritative, is never substituted, and where the two differ the day is flagged revised and the difference recorded.
The entry anchor is registered provisionally at 08:00 UTC on day D plus 1. A.1 TASK 3 measures the distribution of first-print times. If the measured 95th percentile first-print time falls later than 07:00 UTC, the anchor moves to the next whole hour after that percentile, recorded by amendment before any outcome read and before any admissibility count is final. No other input moves the anchor.
A retro day is admissible only if an archive capture strictly before the entry anchor serves a flow value for that day. A forward day is admissible only if the repo's own timestamped capture strictly before the entry anchor serves one. Days failing this are excluded_ineligible and counted, never imputed.

Section 4, signal and position. The signal is the admissible as-printed aggregate net flow in USD. The primary position rule is symmetric: long one unit of BTC perp when the signal exceeds plus T, short one unit when it falls below minus T, flat otherwise, entered at the anchor and exited at the same clock time 24 hours later. T is registered at 100 million USD, matching the source study's unit. Constant notional, no compounding, no leverage beyond one, no liquidation modelling, each named as a Stage-scope simplification. The long-only variant of the handover sketch is a named secondary, never verdict-bearing.

Section 5, outcome definition. Net return for a day equals the signed price return of the Hyperliquid BTC perp from the anchor to the anchor plus 24 hours, plus the signed sum of hourly funding accruing to the position over that window, minus the registered round-trip cost. State the sign convention explicitly: a positive funding rate pays the short.

Section 6, costs. Hyperliquid central 9 bp round trip, taker both legs, band 3, 9, 18. The 3 bp end is maker both legs and is reported as an upper-bound-of-optimism, never as the central case, because a daily signal must fill. Funding over the hold is measured, never assumed. Kraken spot at 50 bp maker and 80 bp taker round trip is reported beside every economic figure to show the venue dependence, descriptive only. IBKR carries no band because error 10243 closes it.

Section 7, horizons. One day primary. The reversal profile at 1 through 20 days is a named secondary. No horizon other than one day is verdict-bearing.

Section 8, inference. Two co-primaries, distribution-free, one-sided, alpha_adj equal to one minus 0.95 to the one-half power, 0.0253 each, and both must pass for the Stage B GO row.
E1, directional. Exact permutation test on the rank correlation between the admissible as-printed signal for day D and the next-day return, over all admissible days, no threshold, one-sided positive. The threshold-free form is registered deliberately: it uses every admissible day and is the highest-powered distribution-free test available on this sample.
E2, economic. Mean net return per trade under the Section 4 rule at T equals 100 million, exact one-sided lower bound above zero at alpha_adj by permutation, at the 9 bp central cost band with measured funding, and reported at 3 and 18 bp beside.
Named secondaries, descriptive and never verdict-bearing: the same-day coefficient as a sanity check against the published 53 bp per 100M, the reversal profile at 1 through 20 days, threshold sensitivity over the grid 0, 50, 100, 200 million with Sidak correction inside the secondary, the out-of-sample halves split to expose decay, the long-only variant, and the revised-day subset compared against the unrevised subset.

Deliberate departure from the handover sketch, recorded here with its reason. The handover proposed a distribution-free sign test as the directional primary. Exact binomial power on roughly 330 days does not reach 80 percent at that test even under the undecayed published effect, so registering it would register a bar the sample cannot reach. The permutation test on rank correlation replaces it. Record this as an ADR.

Section 9, power method and the registered effect assumption. Exact permutation power by simulation at the registered assumptions, computed in A.2 TASK 4 from the measured admissible-day count. No number invented before the census.
The registered primary assumption is half the published next-day effect. The published next-day leg reports Newey-West t 3.12 over 313 days, implying a rank correlation near 0.18. The registered assumption is 0.09. The rationale is registered with it and is not discretionary: the author's own extended-sample IV estimate falls from 0.41 to 0.20 percent per 100M, roughly half, and the independent rolling correlation fell from 0.68 to 0.16 over the test window. Registering at the undecayed figure would register an assumption the pre-existing evidence already contradicts.
Powers at the undecayed 0.18 and at a quartered 0.045 are computed and reported beside as the honest range, the NPLExperiment H3 pattern. Minimum-N statements for each co-primary at each of the three assumptions.
Volatility and funding inputs to the E2 power computation come from the pre-period carve-out only, strictly before 2025-05-01. State this in the section.
Rough anchors for sanity, computation authoritative: E1 near 250 admissible days at the undecayed assumption and in the high hundreds to low thousands at the registered assumption. If the computation disagrees with these anchors, the computation wins and the disagreement is recorded.

Section 10, Stage B trigger. Both co-primaries at or above 80 percent power at achieved admissible N under the assumption Section 0 fired on, the operator prior slot filled and labelled independent or adopted, and explicit operator instruction. Stage B opens the sealed outcomes exactly once, behind a latch written first, recording module hashes. Every value inside the read is quarantined from any successor code path by AST pin and by test.

Section 11, epistemic boundary. A positive supports the claim that the registered rule would have cleared its bars on this sample. It is never a forward return prediction, and it is never evidence about the same-day relationship, which this design cannot test because the print lands after the close.

Section 12, spend and pacing. Zero dollars, keyless public sources only, request ledger with a daily cap set per source from the A.1 TASK 2 measurement and recorded by amendment if it moves. Pacing respects the recorded terms of service.

STAGE A.0 : TASK 5. Section 13, priors.
Record the assistant prior of 0.10 with its date and the adoption warning. Reserve the operator slot empty. The empty slot blocks Stage B structurally.

STAGE A.0 : TASK 6. HYPOTHESES.md.
Create the register with one entry, H1, seeded OPEN, carrying the claim, the registration pointer, the registered bars, the power assumption with its rationale, the assistant prior, and an empty operator prior slot. Write the file's purpose paragraph in the MLCryptoEngine voice: this file exists to prevent retrying a settled question because the number that closed it is buried. State the three closure kinds already in the house record so a future closure can be typed correctly: cost-bound, signal-absent, and unmeasurable-on-available-data. Add the fourth this repo may produce: untestable-at-achievable-power, the NPDExperiment shape. The file contains no analysis. It records what the registration and the sealed read establish.

Commit STAGE A.0.

STAGE A.1 : TASK 1. Access verification, docs/ACCESS.md.
Verify live, with verbatim response fragments and status codes, and record robots.txt and published terms for each before the first repeated fetch.
Flow candidates: Farside Investors BTC ETF flow table, SoSoValue public surface, TheBlock public charts, Glassnode public charts. Record for each whether a per-row publication timestamp is served, whether a keyless structured endpoint exists, and what the served page or payload actually contains as bytes rather than as documented.
Price: Hyperliquid POST https://api.hyperliquid.xyz/info, type candleSnapshot at 1h and 1d for BTC, and type fundingHistory with startTime paging. Kraken public OHLC as a cross-check source only.
Archive: the Wayback availability and timemap endpoints for the chosen flow source.
Record the documented publication convention for each flow source verbatim and label it documented, never measured. The evening and night claim on Farside is a convention, not a measurement, and under the standing rule the measured lag wins.

STAGE A.1 : TASK 2. Rate ceilings measured per endpoint.
The solattn ADR-021 lesson: ceilings are per endpoint, never per host, and measured never assumed. Probe each endpoint under the ledger with a short escalation protocol, record the refusal shape verbatim, the sustained admitted rate, and a chosen operating pace at half the measured ceiling, further reduced wherever the recorded terms ask for it.

STAGE A.1 : TASK 3. Publication lag measured. The first of the two tasks this repo turns on.
Arm a snapshotter that captures the full flow table and writes it with its own capture timestamp to the append-only fsynced ledger. Cadence every 20 minutes across 20:00 to 14:00 UTC, which brackets the print and revision window, and every 2 hours otherwise, subject to the TASK 2 pace and the recorded terms.
Run for a registered minimum of 15 US trading days before any lag figure is quoted.
Measure and report, each with its n: the distribution of first-print times per trading day in UTC, the 50th, 90th and 95th percentiles, the rate at which the largest fund reports late, the rate at which a dash appears where a number later stands, and the count of days where no value exists before the provisional 08:00 UTC anchor.
Fire the Section 3 anchor amendment from the measured 95th percentile if the rule requires it. This is the only permitted anchor movement and it happens here, before any admissibility count is final.

STAGE A.1 : TASK 4. As-printed observability and revision rate. The retro validity test, and the second of the two.
Two measurements, both first-class.
Revision rate, forward. From the TASK 3 ledger, for every day with at least two captures, compare the first value served against the value standing 48 hours later. Report the share of days revised, the distribution of revision sizes in USD and as a share of the printed value, and the share of days where a revision changes the sign of the signal or moves it across the 100 million threshold. The sign-flip and threshold-cross rates are the figures that matter, because they are the ones that would corrupt the test toward a false positive.
Archive capture density, retro. For the out-of-sample window from 2025-05-01 forward, query the archive timemap and count, per US trading day, whether at least one capture exists strictly between the print window and the entry anchor. Report the admissible retro day count, the inadmissible count, and the reasons split by no-capture and capture-too-late. Sample at least 30 admissible retro days and compare the archived as-printed value against the current live value to produce a retro revision rate with its n.
Verdict shape. PASS means archive capture density admits at least 60 percent of out-of-sample trading days and the forward revision rate leaves the signal sign and threshold intact on at least 90 percent of days. PARTIAL means one holds and the other does not, demoting the retro cohort to descriptive with the forward cohort carrying the verdict alone. FAIL means neither holds. Record verbatim evidence.
The MLCryptoEngine H11 precedent is the reason this is first-class. A free flow source with whole-file regeneration and revising past rows killed the last flow hypothesis this project ran, and the lag was discovered rather than registered.

Commit STAGE A.1.

STAGE A.2 : TASK 1. Admissible-day census.
Enumerate every US trading day from 2025-05-01 to the census date. For each, record admissibility under Section 3, the source of the as-printed value as retro-archive or forward-capture, the capture timestamp, the revised flag, and the exclusion reason where inadmissible. Parse flow fields and timestamps only. No price field is touched. Append-only census ledger. Report admissible days per month and the trailing rate.

STAGE A.2 : TASK 2. Signal distribution, outcome-blind.
From the census, report the distribution of the admissible as-printed signal: mean, median, quantiles, the count above plus 100 million, the count below minus 100 million, and the count inside the band. This determines the trade count under Section 4 and is an input to E2 power. It reads no return.

STAGE A.2 : TASK 3. Sealed collection of the outcome substrate.
Fetch and seal, under data/outcomes/, the Hyperliquid BTC perp hourly candles and hourly funding covering every admissible day's anchor and hold window. Written by the sealed writer only. No field parsed outside the allowed lists. Coverage reported as counts, timestamps and reasons, never as values. MIN_OUTCOME_COVERAGE 0.95 for candles and 0.95 for funding hours over the hold windows. An under-covered day reports underpowered, never a return.

STAGE A.2 : TASK 4. Power gate.
Exact permutation power by simulation for E1 and E2 at alpha 0.0253 one-sided, at the registered 0.09 assumption, at the undecayed 0.18, and at the quartered 0.045, using achieved admissible N, projected N by 2026-12-31, and projected N by 2027-03-31 from the measured forward admissible rate. E2 power uses pre-period volatility and funding only. Minimum N clearing 80 percent for each co-primary at each assumption. Compute nothing else. Read no outcome value.

STAGE A.2 : TASK 5. Fire Section 0.
Record the verdict in the registration amendment log, in HYPOTHESES.md, and in progress.md, with every input figure beside it and its n. On BLOCKED, stop after STAGE A.4 documentation and arm nothing. On DEGRADED, record the narrowed verdict scope in the registration and in the register entry, in the plain words Section 0 requires.

Commit STAGE A.2.

STAGE A.3, armed only on GO or DEGRADED.

STAGE A.3 : TASK 1. Production flow snapshotter.
Promote the TASK 3 probe to a durable collector. Diff each capture against the last sealed manifest. On a changed value for a closed day, append a revision row with both values and both capture timestamps. A 429 or 5xx writes a loud error marker and is never read as end-of-print. Seal yesterday's manifest at the daily pass, the solattn ADR-019 shape, and never seal the open day.

STAGE A.3 : TASK 2. Retro backfill, only on as-printed observability PASS.
On PARTIAL, record the forward-only demotion and skip this task. Otherwise, for each admissible retro day, fetch the qualifying pre-anchor archive capture, extract the as-printed value, and write it to the sealed retro ledger with the capture timestamp and the archive URL. Never substitute a live value for a missing capture.

STAGE A.3 : TASK 3. Price and funding recorder.
Daily batch pulls covering each new admissible day's anchor and hold window, cadence set by the A.1 TASK 2 pace, coverage accounted per day, sealed writes only.

STAGE A.3 : TASK 4. systemd.
User units etf-snap.service on a 20-minute timer and etf-daily.service on a timer at 12:20 UTC, Persistent true, MemoryMax 2G. Verify no unit-name collision and confirm the AiTrader 22:30, solattn 00:40, and NPLExperiment 01:40 UTC timers are untouched, and that the npl-watch 60-minute timer is untouched. Add the manual-run guard script refusing while units are active, the ADR-018 shape, with a named override env var. A gap in a forward-recorded flow ledger cannot be backfilled except through the archive, which is exactly the dependency this repo is measuring, so durability is not optional.

STAGE A.3 : TASK 5. Verdict machinery, built dark.
verdict.py computes E1, E2 and the named secondaries against a synthetic fixture set with known answers, including a planted-signal fixture the canary must fire on. Never point it at real sealed data, pinned by test. Stage B calls it exactly once.

Commit STAGE A.3.

STAGE A.4 : TASK 1. Gates.
make lint, typecheck, test green under mypy strict and ruff, every guard exercised, including the pre-period date pin.

STAGE A.4 : TASK 2. Mutations.
At least six applied to real source, each caught, source restored green, bytecode purged before every run: delete a blindness pin, coerce an absence to zero, merge rate_limited into no_data, move a boundary fixture onto the registered anchor boundary, substitute a live flow value where an archived as-printed value is missing, and read a post-2025-05-01 price through the pre-period carve-out. Evidence in reports/stage_a4.

STAGE A.4 : TASK 3. Docs.
README.md at one page. ACCESS.md finalized. DECISIONS.md with numbered ADRs for every choice above: the anchor and its amendment rule, the as-printed admissibility rule, the primary test change from sign test to permutation, the registered half-effect assumption and its rationale, the cost bands, the blindness lists, the pre-period carve-out, the pacing figures, the seal target, the snapshot cadence, and the Citi FAILED TO CONFIRM finding.
report.md, stage-sectioned in the MLCryptoEngine shape, one section per sub-stage, each written for the moment it landed. Sections for A.1 access, A.1 lag, A.1 revision and archive density, A.2 census, A.2 power, and the Section 0 verdict with its inputs. Reserve an empty Stage B section with a one-line note that it is written once and only after the latch.

STAGE A.4 : TASK 4. Close-out.
progress.md entries per sub-stage with ETA against actual. Update the HYPOTHESES.md H1 entry with the Section 0 verdict and every measured figure with its n. Final commit. Push nothing. Print an end-state summary: the Section 0 verdict with its inputs, the measured lag distribution, the measured revision and sign-flip rates, the archive capture density, achieved and projected admissible N, the earliest Stage B date, and the open operator items, which should be the prior slot and nothing else.

END PROMPT

---

## Entry 1 — 2026-08-28 — STAGE A.0, ETAs stated before arming

Session start 07:53:57Z (repo init). Standing rule 2 requires an ETA before each
task and the actual recorded after. Stated here, before A.0 Task 1 is armed.

| Task | ETA stated before starting | Actual |
|---|---|---|
| A.0 T0. Repo init, prompt log, six prior-art files | 12 min | 6 min (07:53:57Z → 07:59:5xZ) |
| A.0 T1. Scaffold and the five guards | 25 min | _pending_ |
| A.0 T2. CLAUDE.md | 8 min | _pending_ |
| A.0 T3. REGISTRATION Section 0 + fire function + tests | 20 min | _pending_ |
| A.0 T4. REGISTRATION Sections 1–12 | 30 min | _pending_ |
| A.0 T5. Section 13, priors | 5 min | _pending_ |
| A.0 T6. HYPOTHESES.md | 12 min | _pending_ |

### Prior art read at A.0 Task 0 — six files, patterns taken, no text copied

1. `NPLExperiment/REGISTRATION.md` (659 lines) — the register style, the
   dated-amendment protocol ("nothing above an amendment line is ever edited"),
   the Section 0 verdict record with every input figure beside its n, the Stage B
   latch and module-hash protocol, the quarantine, the closure shape.
2. `NPLExperiment/HYPOTHESES.md` (126 lines) — the register index voice, the
   status/deciding-numbers/sample/working/what-would-reopen-it table shape, the
   outcome-blind cull firing BLOCKED on measured rates as a documented answer.
3. `NPLExperiment/progress.md` (1,015 lines) — the falsified planning figure
   recorded rather than corrected (main-dex accrual 9.4/month registered,
   measured 0.5/month at n = 3 over 182 days, H3 killed on the figure), and the
   Section 0 cull firing on measured rates.
4. `MLCryptoEngine/HYPOTHESES.md` H11 + `report.md:2734` — **the direct
   precedent.** Free flow source (Coin Metrics community), **measured 75-day
   publication lag** where the documentation implied current, "whole-file
   regeneration; past rows revise", 0 of 40 registered cells pass. The reopening
   condition names the data threshold, not a better model: "a free exchange-flow
   source at ≤ 2-day publication lag with ≥ 3 years of history — the measured
   75-day staleness is the binding data constraint on class B". **The class died
   on the lag, not on the model.**
5. `MLCryptoEngine/DECISIONS.md` ADR-055 — fee schedules are dated
   measurements, never constants; re-verify live and record the correction with
   an explicit statement of which closures flip (none did).
6. `solattn/DECISIONS.md` ADR-019 (the daily pass seals the day that closed, and
   never the open day; a reader refuses an unattested closed day), ADR-021
   (pacing is measured **per endpoint**, never generalised across them — 6.0 s on
   one endpoint and 12.0 s on another from the same host, n = 1,863 attempts,
   47.5% refusal share), ADR-022 (expiry-soonest-first ordering decides where a
   shortfall falls).
7. `InsiderExperiment/progress.md` (315 lines) — the power-gate closure shape:
   CORPUS-GO then BLOCKED, the verdict fired before measurement, the three
   defects found only by mutation (text-scanning config guard passing vacuously,
   a fixture comfortably inside its boundary, a mutation harness reporting on
   bytecode from source no longer on disk).

