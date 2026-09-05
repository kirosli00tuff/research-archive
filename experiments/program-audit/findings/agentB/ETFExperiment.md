# Agent B — ETFExperiment

Repository: **ETFExperiment** · anchored SHA `4d110027674e7b4cd2861cf4e0e74f975111daf1` (master, 2026-08-28).
Snapshot read: `/home/kiros-li/.cache/program-audit/scratchpad/snap/ETFExperiment/`.
Live repository touched read-only for git history and for the untracked `data/` tree (access log at the end).
Recomputation scratch: `/home/kiros-li/.cache/program-audit/scratchpad/work/agentB-etf/`.
Direction B throughout: the question asked of every entry is whether the conclusion outran the evidence.

## Summary — the strongest case for the thesis in this repository

This repository shipped no positive result, no verdict and no tradeable artifact, so the thesis has to
be made against the *inputs to a negative* — and there it holds twice. One of the two registered
co-primaries, E2, is implemented so that the round-trip cost, the measured funding and the pre-period
volatility all cancel algebraically: `run_e2` returns `p = 0.000250, passes = True` on a strategy losing
**8.9 percent net per trade** (n = 200 days, 153 trades), and every E2 power figure — including the
governing minimum N of 300 that decides the closure — comes from a test that never charges a cost.
The second: the accrual rate called "measured" in five documents is the source's *printed-day* rate
(333/336), not an admissible-day rate; measured forward admissibility is **0** (n = 336 rows), and the
substitution is what keeps the Section 0 BLOCKED power trigger from firing. Two further figures shipped
on the front page describe a series the design never reads (315 of 333) or a distribution that is not the
one named (mean 47.42M). Against that, the pre-registration is genuinely prior, no bar moved after data
existed, and the one convenient figure available was refused — the list of what survived is long.

**Findings: 9.** Two S1, two S2, one S3, four S4.

---

### AUDIT-B-ETFExperiment-1
- **Repository / SHA:** ETFExperiment / `4d110027674e7b4cd2861cf4e0e74f975111daf1`
- **Hypothesis or artifact:** H1 co-primary **E2** (the "economic" test), its power figures, the governing minimum N of 300, and the shipped dark verdict engine `src/etf/verdict.py`
- **Direction:** B
- **Class:** STATISTICAL
- **Severity:** S1
- **Label:** DERIVED (obtained by running the repository's own `power.py` and `verdict.py` modules and by reading `src/etf/power.py` / `src/etf/verdict.py`)
- **Claim challenged (verbatim quote):**
  "**Mean net return per trade under the Section 4 rule at T = 100 million USD;
  exact one-sided lower bound above zero at alpha_adj by permutation**, at the
  **9 bp central cost band with measured funding**, and **reported at 3 and 18 bp
  beside**." — **ETFExperiment/REGISTRATION.md:302-305**
  (same substance at HYPOTHESES.md:73, "exact one-sided lower bound above zero by permutation, at the **9 bp central cost band** with **measured** funding, reported at 3 and 18 bp beside", and in the governing prompt at progress.md:105)
- **Evidence:**
  - The implemented E2 statistic subtracts the round-trip cost from **both** the observed value and every permutation replicate: `observed = sum(edge) / traded - inputs.round_trip_cost` (ETFExperiment/src/etf/power.py:154) against `if perm_edge / traded - inputs.round_trip_cost >= observed` (ETFExperiment/src/etf/power.py:162). The same construction stands in the shipped verdict engine: `observed = statistics.fmean(edges) - cost * BP` (ETFExperiment/src/etf/verdict.py:126) against `if perm and statistics.fmean(perm) - cost * BP >= observed` (ETFExperiment/src/etf/verdict.py:138). The cost term is identical on both sides and cancels exactly, so the p-value cannot depend on it. The number of non-flat positions is preserved by a shuffle, so the denominator is constant too.
  - The funding term cancels for the same reason one step further: `perm_edge = Σ p_shuffled·(r − F) = Σ p_shuffled·r − F·Σ p_shuffled`, and `Σ p` is invariant under a shuffle. The docstring stops one term short of noticing this: "`|p|` is preserved by a shuffle, so the cost term is constant under the null and the test is on the mean of `p * (r - F)`" (ETFExperiment/src/etf/power.py:137-138).
  - The scale of the return series cancels as well, so the pre-period volatility input is inert.
  - **Consequence for the shipped verdict engine (n = 200 days, 153 trades):** on a synthetic sample, `run_e2` returns `p = 0.000250, passes = True` at **every** cost band — 0, 3, 9, 18, 100 and **1000 bp** — while `mean_net` falls from **+1.109%** to **−8.891%** per trade. A strategy losing 8.9 percent net per trade "passes" a test registered as an "exact one-sided lower bound above zero".
  - **A realistic-scale case (n = 400 days, 294 trades, daily sd 0.20%, true rank correlation 0.30):** at the registered 9 bp band `run_e2` gives `mean_net = −2.73 bp`, `p = 0.00025`, `passes = True`; at 18 bp, `mean_net = −11.73 bp`, `p = 0.00025`, `passes = True`.
  - **Consequence for the closure's governing figure:** `e2_power(300, 0.18, …, draws=1200, simulations=300)` returns **0.8000** at round trips of 3.0, 9.0, 18.0 and 1000.0 bp; **0.8000** at funding sums of 0.0, the measured 0.000534 and 0.01; and **0.8000** at daily sd of 0.001, the measured 0.027431 and 0.5. Every E2 power figure in Amendment 3 (ETFExperiment/REGISTRATION.md:846-851, the `E2 @ 0.18` and `E2 @ 0.09` columns, n = 4 cohort rows) and Amendment 4 (ETFExperiment/REGISTRATION.md:961-964, the E2 grid over n = 200…1200), and therefore the E2 minimum N of **300** that Amendment 4 makes governing ("**The governing minimum N is therefore 300, not 237.**", ETFExperiment/REGISTRATION.md:974), is a number produced by a test that never charges a cost.
  - The three "economic inputs" reported beside those figures with their n — "daily sd **0.027431** (n = 475 returns, 2024-01-11 to 2025-04-30); 24-hour funding sum **0.000534** from a mean hourly rate of 0.00002226 (n = 11,423 hours); round trip **9 bp**" (ETFExperiment/REGISTRATION.md:853-856; the same values in `reports/stage_a2/power.json` → `economic_inputs`) — provably do not move any reported output. The entire pre-period carve-out apparatus that supplies two of them (ADR-007, ETFExperiment/DECISIONS.md:207-215, with four structural guards and a live demonstration of 72 of 72 readable pre-boundary rows and 500 of 500 gated post-boundary rows) exists, per its own rationale, because "The E2 economic-power computation needs a volatility and a funding level to size a net return against a 9 bp round trip" (ETFExperiment/DECISIONS.md:211-212). As implemented it sizes nothing.
  - The test suite does not catch it: `test_a_higher_cost_band_never_improves_the_mean_net` asserts only on `mean_net`, never on `p_value` or `passes` (ETFExperiment/tests/test_verdict.py:185-190, n = 3 cost bands asserted).
- **Recomputation:** Inputs — `src/etf/power.py:119-166` (`e2_power`), `src/etf/verdict.py:106-148` (`run_e2`), `src/etf/config.py:154` (`hyperliquid_round_trip_bp=(3.0, 9.0, 18.0)`), `reports/stage_a2/preperiod_inputs.json` (`daily_sd` 0.027430504889517645, `daily_funding_sum` 0.0005343574667950626), `reports/stage_a2/census.json` → `signal_distribution_live_descriptive.trade_share` 0.7567567567567568. Method: the repository's own package was copied unmodified to `/home/kiros-li/.cache/program-audit/scratchpad/work/agentB-etf/etf/` and called with the cost, funding and volatility inputs varied one at a time (`check_e2.py`, `check_e2b.py`, `check_more.py`); nothing was executed inside the audited repository. Results: `run_e2` p-value and `passes` constant across 0–1000 bp (re-run at consolidation, 2026-09-04: `+0.011089 / +0.010789 / +0.010189 / +0.009289 / +0.001089 / −0.088911` mean_net, `p = 0.000250, passes = True, n_trades = 153` at all six); `e2_power(300, 0.18)` = 0.8000 across all cost, funding and volatility settings tried. **Control:** `e2_power(300, 0.18, draws=1200, simulations=300)` reproduces Amendment 4's published 0.8000 exactly, and the grid points the repository's script never evaluated give 0.8633 at n = 350 and 0.9500 at n = 400 — so the minimum of 300 is right *for the test that was run*.
- **What would resolve it:** Either (a) re-register E2 as what it is — a permutation test of association between the thresholded position and the realised return, with the cost band reported as a descriptive statistic only — or (b) implement the registered test: compare the observed mean net return against zero by a method whose null is centred at zero (a studentised bootstrap, or a permutation of return signs), which would make the 3/9/18 bp band bind and would change every E2 power figure and the governing minimum N. Until one of the two happens, no E2 figure in the record describes the registered bar.
- **Confidence:** HIGH — the cancellation is algebraic, it is reproduced numerically in the repository's own code at six cost levels, three funding levels and three volatility levels, and it stands identically in the power module and in the verdict module.
- **Invalidated by later commits?:** No. The anchored SHA is the final commit of a closed repository; `power.py` and `verdict.py` are unchanged since 5fa460a / f53c44f (2026-08-28 13:27 / 13:30 −0700, verified by `git log --follow` on the live repository).
- **Disclosed by authors?:** **Partly, and only in code, and only for one of the three terms.** `src/etf/power.py:137-138` states that the cost term is constant under the null. No document states it, and the code states it as a *justification* of the null's validity rather than as a statement that the registered cost band does not enter the decision; the funding and volatility invariance, and the consequence for the power figures and for the governing minimum N, are disclosed nowhere. For that reason I have not treated this as an authorial disclosure of the limitation raised and have not capped the severity at S3 — a reader who judges power.py:137-138 to be the disclosure should read this as S3. REGISTRATION.md, HYPOTHESES.md, report.md and DECISIONS.md all present E2 as a net-of-cost test at a named band with the funding measured, and report.md:301-304 draws a substantive conclusion — "costs are not the binding term here" — beside power figures that could not have shown otherwise.

---

### AUDIT-B-ETFExperiment-2
- **Repository / SHA:** ETFExperiment / `4d110027674e7b4cd2861cf4e0e74f975111daf1`
- **Hypothesis or artifact:** the projected admissible N of 163, the Section 0 finding "BLOCKED does not fire on power", the deadline finding, and shipped reopen threshold (c)
- **Direction:** B
- **Class:** STATISTICAL
- **Severity:** S1
- **Label:** DERIVED (obtained from `scripts/power_gate.py`, from the stored `reports/stage_a2/*.json` artifacts, and by running the repository's own `e1_power`)
- **Claim challenged (verbatim quote):**
  "**Projected achieved N at the registered 2027-03-31 deadline: 163**, at a measured forward accrual of **20.8 admissible days per month**." — **ETFExperiment/HYPOTHESES.md:70**
  (also "At the measured forward accrual rate of 20.8 admissible days per month" REGISTRATION.md:981-982; "Measured forward accrual is **20.8 admissible days per month**" report.md:447-448; "the measured accrual rate of 20.8 admissible days per month" progress.md:493; "forward accrual sustained at the measured 20.8 admissible days per month" HYPOTHESES.md:84)
- **Evidence:**
  - **No forward admissible day exists.** `reports/stage_a2/census.json` records `"admissible_forward_capture": 0` and `"admissible_retro_archive": 11` over `"rows": 336`; HYPOTHESES.md:70 itself says "Achieved N on the closing date: **11**, all retro-archive, forward-capture 0."
  - **The projection is not a measurement of admissibility.** `scripts/power_gate.py:71` sets `printed_rate = 333 / 336` and `scripts/power_gate.py:78-80` builds the scenarios as `achieved_forward + round(to_interim * printed_rate)` and `achieved + round(to_deadline * printed_rate)`. With `weekdays_to_deadline = 153` (`reports/stage_a2/power.json`) this gives `round(153 × 0.9910714285714286) = 152` and `11 + 152 = 163` (`reports/stage_a2/power.json` → `scenarios.all_cohorts_by_deadline` = 163). The projection therefore assumes that **every** future weekday on which the source prints a value yields an admissible day — a forward-capture admissibility rate of 100 percent.
  - **20.8 is the source's print rate per month, not an admissible-day rate:** 333 printed days over the 16 months of `census.json.by_month` (2025-05 … 2026-08) = **20.8125**; the same 16 months hold 336 weekday rows = 21.0/month. The **measured** admissible-day rate over those same 16 months is **11 admissible days**, i.e. **0.69 per month** (`census.json.by_month` admissible counts: 1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 5, 2; n = 16 months, 336 weekday rows).
  - **The registration named this exact figure as a measurement target and forbade its use before measurement:** "**Therefore: no accrual, coverage, lag, retention, revision, or capture-density figure in this repository is registered before it is measured.**" (ETFExperiment/REGISTRATION.md:571-572) with the table row "| admissible days per month and the trailing rate | **A.2 Task 1** |" (ETFExperiment/REGISTRATION.md:584). A.2 Task 1 produced `by_month` and no trailing rate; the number carried into the closure came from `power_gate.py`, not from A.2 Task 1.
  - **The one measurement that would have converted the assumption into a figure was abandoned.** A.1 Task 3's registered deliverables include "the count of days where no value exists before the provisional 08:00 UTC anchor" (ETFExperiment/progress.md:143; ETFExperiment/REGISTRATION.md:580, "| days with no value before the provisional anchor | **A.1 Task 3** |"). It never ran: "**2 captures exist**" against a registered minimum of 15 US trading days (ETFExperiment/progress.md:452-455), and Amendment 6 drops it permanently (ETFExperiment/REGISTRATION.md:1141-1147).
  - **The repository's own retro evidence does not establish that the assumption holds.** Of the 11 archived captures that served a value, one sits at **+07:59:43** past midnight UTC on D+1 — 17 seconds inside the 08:00 anchor — and captures still showing a dash run as late as **+04:29** (recomputed from `reports/stage_a1/retro_revision.json`, n = 11 served and n = 23 still-dashed; the repository quotes the same range at docs/ACCESS.md:413-415 and rounds the last served capture to "+08:00"). A print landing inside the last cadence interval before the anchor produces an inadmissible forward day, and the rate at which that happens is exactly the unmeasured quantity.
  - **What turns on it:** Section 0's BLOCKED trigger is "E1 under **50 percent** power at the published-magnitude assumption at the achievable count by 2027-03-31" (ETFExperiment/REGISTRATION.md:47-48). At the projected N = 163, E1 = **0.6105** and the trigger is not met (ETFExperiment/REGISTRATION.md:869-871). At the only *measured* pre-anchor served-value rate this repository holds (11 of 336 = **3.27 percent**), the achievable count by the deadline is `11 + round(153 × 0.0327)` = **16**, at which `e1_power(16, 0.18)` = **0.0955** — BLOCKED fires. The two rates on the record bracket the verdict, and the registration used neither the measured one nor a stated assumption.
  - **It also carries the shipped reopen threshold.** Amendment 6 §2: "Forward-only accrual at the measured **20.8 admissible days per month** reaches roughly **291** by 2027-10-31, plus the **11** already admissible, for about **302**. That clears the governing 300 by two days" (ETFExperiment/REGISTRATION.md:1129-1132). A margin of two days out of 300 is **0.67 percent**; any forward admissibility below 99.3 percent of printed days inverts that sentence, and no evidence in the repository bounds it.
- **Recomputation:** Inputs — `scripts/power_gate.py:71,78-80`; `reports/stage_a2/power.json` (`weekdays_to_deadline` 153, `printed_day_rate` 0.9910714285714286, `scenarios`); `reports/stage_a2/census.json` (`admissible` 11, `admissible_forward_capture` 0, `rows` 336, `by_month`). Method: arithmetic reproduction plus `e1_power` from the repository's own module, run from the work dir. Results: `round(153 × 333/336) = 152`; `11 + 152 = 163` ✓ matches the published figure; `333/16 = 20.8125` ✓ matches the published 20.8; measured admissible rate `11/16 = 0.6875` per month; `e1_power(16, 0.18) = 0.0955`, `e1_power(30, 0.18) = 0.1395`. **Control:** `e1_power(163, 0.18) = 0.6105`, `e1_power(163, 0.09) = 0.2015`, `e1_power(11, 0.18) = 0.0815`, `e1_power(152, 0.18) = 0.6000` — all four reproduce `reports/stage_a2/power.json` exactly, so the power engine itself is sound and only its input N is in question.
- **What would resolve it:** Relabel the figure as a projection at an assumed 100 percent forward admissibility, state the assumption where the number is used (README, HYPOTHESES, report, Amendments 3-6), and either bound it from the 15-trading-day A.1 Task 3 measurement or record that the Section 0 power leg was decided on an unmeasured input. A single sentence — "this projection assumes every printed forward day is captured before the anchor; that rate was never measured" — would settle it.
- **Confidence:** HIGH on the facts (the code, the census and the arithmetic are unambiguous); MEDIUM on how much it should move the verdict, because a 20-minute forward cadence is structurally far denser than a third party's 0.316 crawls per day and the assumption is plausible — but plausible is not measured, and the registration's own Section 14.7 exists to forbid exactly this substitution.
- **Invalidated by later commits?:** No. The anchor is the final commit; `power_gate.py` and `census.json` are unchanged since 5fa460a (2026-08-28) and the repository is closed with no armed collector.
- **Disclosed by authors?:** **No.** The code comes closest and still gets it wrong in the other direction: `scripts/power_gate.py:5-6` says the projection uses "achieved admissible N and projected N by the two registered deadlines from the measured forward admissible rate", which is 0 over 0 days. The honest half is the `trading_days_between` docstring, "The projection uses the MEASURED printed-day rate rather than a calendar assumption" (ETFExperiment/scripts/power_gate.py:34-35), and no document repeats it. Every document says "measured forward accrual … admissible days per month".

---

### AUDIT-B-ETFExperiment-3
- **Repository / SHA:** ETFExperiment / `4d110027674e7b4cd2861cf4e0e74f975111daf1`
- **Hypothesis or artifact:** the shipped "independent cross-check" figure (README table row, HYPOTHESES measured-figures row, report A.1 Task 1, Amendment 1 §1)
- **Direction:** B
- **Class:** UNSUPPORTED_POSITIVE
- **Severity:** S2
- **Label:** DERIVED (recomputed from the two stored payloads in the live `data/access/` tree, with the universe rule read from `src/etf/config.py`)
- **Claim challenged (verbatim quote):**
  "| Independent cross-check | **315 of 333** out-of-sample days agree within 2% between Farside and SoSoValue |" — **ETFExperiment/README.md:29**
  (also "The cross-check passes: **315 of 333 out-of-sample days agree within 2 percent**." REGISTRATION.md:624; "**The cross-check passes: 315 of 333 out-of-sample days agree within 2 percent between two independently operated sources (n = 333).**" report.md:69-70; "Independent cross-check **315 of 333** within 2%." HYPOTHESES.md:80)
- **Evidence:**
  - **The comparison is not on the registered signal.** The one document that says what was compared says it is "between Farside's all-fund `Total` and SoSoValue's `totalNetInflow`" (ETFExperiment/docs/ACCESS.md:179-181). Farside's `Total` column is the one the registration forbids consuming: "the source's `Total` column is **never** consumed" (ETFExperiment/DECISIONS.md:333-334), "it is the wrong universe anyway" (ETFExperiment/DECISIONS.md:348-349), and A.1 Task 1's Finding 2 is that reading it would have fabricated the whole lag measurement — "**The `Total` column prints `0.0` on a day where every per-fund cell is a dash: 3 of 3 such rows over n = 336.**" (ETFExperiment/report.md:90-91).
  - **Recomputed from the same stored payloads:** comparing Farside's `Total` with SoSoValue's `totalNetInflow` over the 333 printed out-of-sample days reproduces the published figure exactly — **315 of 333** within 2 percent (relative to |a|, |b| or the mean; 316 under a max-denominator). The document's named worst day also reproduces: 2026-08-11, Farside `Total` = 7.8M against SoSoValue 4.886M (docs/ACCESS.md:182, "worst: 2026-08-11, 7.8M against 4.89M").
  - **The same 2 percent test applied to the registered five-fund aggregate** — the actual signal, `flow_universe_tickers=("IBIT", "FBTC", "GBTC", "ARKB", "BITB")` (ETFExperiment/src/etf/config.py:141) — against SoSoValue passes on **110 of 333** days (109 under the |a| or mean denominators). That figure appears nowhere in the repository.
  - So the registered signal has no independent cross-check on the record: the two sources agree on a series the design never reads, and disagree by more than 2 percent on **223 of 333** days (67.0 percent) on the series it does read.
- **Recomputation:** Inputs — `data/access/farside_all_parsed.json` (untracked, live repo, read-only, 2026-09-04 ~19:1x UTC; header and 676 date rows), `data/access/sosovalue-btc.html` (untracked, live repo, same read; `__NEXT_DATA__` → `props.pageProps.historyData.list`, 660 rows), universe rule from `src/etf/config.py:141` and `scripts/archive_density.py:43-47`, out-of-sample start `2025-05-01` from `src/etf/config.py:148`. Method: parse both series, restrict to the 333 out-of-sample days on which all five registered funds print, and count `|a − b| / den ≤ 0.02` (`verify_flow.py`, `verify2.py` in the work dir). Results: 676 date rows, 336 out-of-sample, 333 printed — all three reproduce the published counts exactly; Farside `Total` vs SoSoValue **315/333**; registered five-fund aggregate vs SoSoValue **110/333**.
- **What would resolve it:** Say in the README, the register entry, the report and Amendment 1 what docs/ACCESS.md already says — that the 315 of 333 is an agreement between two all-fund totals — and publish the corresponding figure for the registered five-fund signal, or drop the row.
- **Confidence:** HIGH — the published number is reproduced exactly on the stated comparison, and the alternative comparison is reproduced from the same two files by the same parser.
- **Invalidated by later commits?:** No. The payloads are the ones stored at the anchor and the repository is closed. The untracked data could in principle have changed since 2026-08-28, but both files carry the collection timestamps of that day and every derived count matches a published one exactly.
- **Disclosed by authors?:** **Partly, and not the part that decides it.** docs/ACCESS.md:179-181 states the comparison basis plainly, and that is the only place it appears. README.md:29, HYPOTHESES.md:80, report.md:69-70 and REGISTRATION.md:624 all present the figure as an agreement "between Farside and SoSoValue" — three of them within a line or two of the universe mismatch — which reads as a cross-check of the signal. The deciding figure of this finding, **110 of 333 for the registered signal**, is derived here and is disclosed nowhere, so the S3 disclosure cap does not apply and the severity stands at S2.

---

### AUDIT-B-ETFExperiment-4
- **Repository / SHA:** ETFExperiment / `4d110027674e7b4cd2861cf4e0e74f975111daf1`
- **Hypothesis or artifact:** the figure deciding "SoSoValue is never the signal" and "the source's `Total` column is never read", published identically in four documents
- **Direction:** B
- **Class:** ARITHMETIC
- **Severity:** S2
- **Label:** DERIVED (recomputed from the two stored payloads in the live `data/access/` tree)
- **Claim challenged (verbatim quote):**
  "**SoSoValue is retained as a cross-check and is never the signal**: its
  `totalNetInflow` spans all US spot BTC ETFs rather than the registered five,
  and the two differ by **a mean of 47.42M USD (median 27.20M, range −903.20M to
  +1,205.20M, n = 333)** — large against the registered 100M threshold." — **ETFExperiment/REGISTRATION.md:620-623**
  (same figures at report.md:65, at docs/ACCESS.md:172-176 "the registered five-fund aggregate differs from the all-fund total by a mean of 47.42M USD (median 27.20M, range −903.20M to +1,205.20M, n = 333)", and at DECISIONS.md:349-351, where they are attributed to Farside's own `Total` column spanning "12 funds against the registered 5")
- **Evidence:**
  - **Recomputed over the same 333 days, the *difference* between the registered five-fund aggregate and SoSoValue's all-fund total is mean −7.15M, median −2.89M, range −150.43M to +366.16M (n = 333).** Against Farside's own `Total` column it is mean **−7.44M**, median **−3.00M**, range **−363.00M to +150.40M** (n = 333). Mean absolute difference is 17.9M (SoSoValue) and 17.6M (Farside `Total`).
  - **The published figures are instead the *level* statistics of SoSoValue's own series** over those same 333 days: mean **47.13M**, median **27.29M**, min **−903.11M**, max **+1,205.18M** — against the published "mean of 47.42M USD (median 27.20M, range −903.20M to +1,205.20M, n = 333)". The min, max and median agree to within the source's own 0.1M display rounding; the mean differs by 0.6 percent. Every alternative day-set tried (all 336 out-of-sample rows, SoSoValue's own rows from 2025-05-01, its last 333 rows, values rounded to 0.1M) gives the same four statistics.
  - **For contrast, the registered five-fund series' own level statistics** are mean 39.98M, median 27.40M, min −860.90M, max +1,142.40M — which is exactly `reports/stage_a2/census.json` → `signal_distribution_live_descriptive` (`mean` 39980780.78078078, `median` 27400000.0, `min` −860900000.0, `max` 1142400000.0, `n` 333). The two level distributions were computed side by side; one of them was then written down as a difference.
  - **What the true difference implies for the stated conclusion:** |five-fund − SoSoValue| exceeds the registered 100M USD threshold (`signal_threshold_usd=100_000_000.0`, src/etf/config.py:150) on **7 of 333** days (2.1 percent), and the Section 4 position (long above +100M, short below −100M, flat inside) differs between the two series on **10 of 333** days (3.0 percent). The conclusion "the two are not interchangeable" survives — 3 percent of days changing the traded position is a real objection — but not on the figure given, which overstates the mean discrepancy by a factor of about 6.6 and the median by about 9.4.
- **Recomputation:** Inputs — `data/access/farside_all_parsed.json` and `data/access/sosovalue-btc.html` (untracked, live repo, read-only, 2026-09-04; see access log), universe `("IBIT","FBTC","GBTC","ARKB","BITB")` from `src/etf/config.py:141`, out-of-sample start `2025-05-01` from `src/etf/config.py:148`. Method: parse both series, restrict to the 333 printed out-of-sample days, compute the difference distribution and each series' level distribution (`verify_flow.py`, `verify2.py`, `verify3.py`, `verify4.py` in the work dir). Results as above. **Control:** the same parse reproduces the published 315-of-333 cross-check exactly and the published 676 / 336 / 333 row counts exactly.
- **What would resolve it:** Recompute the difference distribution between the registered five-fund aggregate and the all-fund total, and record the correction as an amendment, as Amendment 2 did for the density figure. The right supporting figures for the same conclusion are already available and are stronger where it matters: 7 of 333 days differ by more than the registered threshold and 10 of 333 change the traded position.
- **Confidence:** HIGH — the published min, max and median match SoSoValue's own level distribution to display rounding, and the true difference distribution is an order of magnitude away on three of the four statistics.
- **Invalidated by later commits?:** No. The repository is closed at this SHA and the figure is repeated identically in four files, two of them amendments that may not be edited.
- **Disclosed by authors?:** **No.** All four sites state the figures as a measured difference between two series; DECISIONS.md:349-351 additionally attributes them to a third pairing (Farside `Total`, "12 funds against the registered 5").

---

### AUDIT-B-ETFExperiment-5
- **Repository / SHA:** ETFExperiment / `4d110027674e7b4cd2861cf4e0e74f975111daf1`
- **Hypothesis or artifact:** the README's front-page summary of what this repository measured
- **Direction:** B
- **Class:** PROCESS
- **Severity:** S3 (capped: the authors disclose the underlying absences — see the disclosure field)
- **Label:** READ (document-to-document comparison; no data, code or git object was needed)
- **Claim challenged (verbatim quote):**
  "## What is measured so far, each figure with its n" — **ETFExperiment/README.md:21**, the 13-row table at README.md:23-37, read against README.md:14, "**Not the return. The publication lag and the revision rate.**"
- **Evidence:**
  - The README declares that the publication lag and the revision rate are the two measurements that decide the repository (ETFExperiment/README.md:14-19; the same declaration is the governing prompt's at progress.md:19 and CLAUDE.md:19-25).
  - **Neither was measured, and neither appears in the table.** Of the **13 rows** at README.md:25-37, **0** describe the publication lag and **0** describe the forward revision rate; there is no row saying either was not measured. The nearest row is "Retro revision rate" (README.md:33), which is a different measurement on a different cohort.
  - The absences are recorded plainly elsewhere: "**No lag figure is quoted in this section.** The registration requires at least **15 US trading days** of forward capture before any is, and one day exists." (ETFExperiment/report.md:176-177); "**Not quoted.** The registration requires **15 US trading days** of forward capture before any lag figure is; **2 captures exist**" (ETFExperiment/progress.md:452-454); "**The forward revision-integrity leg will never complete.**" (ETFExperiment/REGISTRATION.md:1141).
  - The one row that does describe the revision hazard reports a figure the repository itself says carries no verdict and may not be cited later — "| Retro revision rate | **0 of 11 revised**, 0 sign flips, 0 threshold crosses — the H11 hazard does **not** reproduce here, at an n below the registered minimum of 30 |" (ETFExperiment/README.md:33, n = 11) — while Amendment 6 rules that "its n = 11 retro corroboration may not be cited by anything later as evidence of source stability" (ETFExperiment/report.md:518-519; the register's wording at REGISTRATION.md:1151-1153 is "may not cite the n = 11 figure as evidence of anything"). The README states the reassuring half in bold and the disqualifier in a trailing clause.
- **Recomputation:** None. This is a document-to-document comparison; the only figures are row counts (13 table rows, 0 of them the lag or the forward revision rate) and the repository's own n = 11 / 2 captures / 15 trading days.
- **What would resolve it:** One row in the README table reading "Publication lag — **not measured**; registered minimum 15 US trading days, 2 captures exist" and one reading "Forward revision rate — **not measured**, dropped by Amendment 6". The repository's own standing rule 4, "**Absence is a recorded state, never a synthesized value.**" (ETFExperiment/CLAUDE.md:34), asks for exactly that on the page most people will read.
- **Confidence:** HIGH on the fact; MEDIUM on severity, because the report, the registration and progress.md all state the absences without hedging and the omission is confined to the one-page summary.
- **Invalidated by later commits?:** No — README.md is unchanged since fe60a22 and the repository is closed.
- **Disclosed by authors?:** **Yes — the authors disclose both absences, and this finding is therefore capped at S3.** report.md:176-179, progress.md:450-456 and REGISTRATION.md:1139-1147 all state that neither forward measurement completed, without hedging. The finding is only that the disclosure does not reach the README, which is the artifact a reader meets first; it is not a discovery of an undisclosed limitation.

---

### AUDIT-B-ETFExperiment-6
- **Repository / SHA:** ETFExperiment / `4d110027674e7b4cd2861cf4e0e74f975111daf1`
- **Hypothesis or artifact:** the four bars that decide A.1 Task 4 and Section 0 — archive density 0.60, revision integrity 0.90, retro revision minimum sample 30, lag minimum 15 trading days — and the register's citation of them
- **Direction:** B
- **Class:** PROVENANCE
- **Severity:** S4
- **Label:** DERIVED (grep over the snapshot document, plus live git objects 815f888 / 0cd8572 / 97da329 and `src/etf/config.py`)
- **Claim challenged (verbatim quote):**
  "**This is below the registered minimum sample of 30** (Section 12 / A.1 Task 4)," — **ETFExperiment/REGISTRATION.md:767**
  (and "**and n = 11 is below the registered minimum sample of 30, which the registration set before any of it was visible.**" REGISTRATION.md:891-893)
- **Evidence:**
  - **Sections 0-14 of REGISTRATION.md — the pre-registration proper, lines 1-589 — contain none of the four numbers in this sense.** A grep of those 589 lines for `0\.60|60 percent|0\.90|90 percent|15 US|15 trading|thirty| 30` returns exactly **2 hits out of 589 lines**: line 70, "`tests/test_observability.py` with fixtures exactly on the 0.60 and 0.90 bars", which names two of the bars without stating what they measure, and line 561, Coinbase's fee tier ("**0.40 maker / 0.60 taker**"). The numbers 30 and 15 do not occur at all.
  - **Section 12 (REGISTRATION.md:423-450), the section cited for the minimum sample of 30 and for the 15 trading days, contains neither number** — its only bars are the sealed coverage bars, "`MIN_OUTCOME_COVERAGE` **0.95** for candles and **0.95** for funding hours".
  - **The bars do exist, in code:** `lag_min_trading_days=15` (src/etf/config.py:183), `archive_density_pass_share=0.60` (:185), `revision_intact_pass_share=0.90` (:186), `retro_revision_sample_min=30` (:187), with their meaning in the module docstring — "Bar: at least 60 percent." (src/etf/observability.py:9) and "Bar: at least 90 percent." (src/etf/observability.py:12).
  - **Git confirms the substance of the pre-registration claim.** `git show 815f888:src/etf/config.py` already carries all four values at commit 815f888 (2026-08-28 01:05:56 −0700), and the first network activity is commit 97da329 at 13:04:41 −0700 the same day — twelve hours later. `git diff 815f888 0cd8572 -- src/etf/config.py` shows the only post-network change to config.py is the addition of the three Farside URL fields, which Amendment 1 §1 registers. **No bar moved after data existed.**
  - So the defect is one of citation and of where the record lives, not of bar-fitting: a document that says nothing above an amendment line is ever edited, and that is meant to be the registration, does not itself state four of the numbers it later calls registered, and points at a section that does not contain them.
- **Recomputation:** Inputs — `REGISTRATION.md:1-589` (grep, run against the snapshot), `src/etf/config.py:183-187`, `src/etf/observability.py:9,12`, live git objects 815f888, 0cd8572, 97da329. Method: grep of the pre-amendment portion of the registration; `git show` / `git diff` / `git log --date=iso` on the live repository, read-only. Result: **0 of 4** bars stated in the pre-amendment registration prose (2 named without meaning at line 70), all 4 present in code from the first scaffold commit and unchanged thereafter.
- **What would resolve it:** State the four numbers in the registration prose, or correct the citation from "Section 12" to `src/etf/config.py` / `src/etf/observability.py`.
- **Confidence:** HIGH — the grep and the git objects are unambiguous.
- **Invalidated by later commits?:** No — the repository is closed at this SHA.
- **Disclosed by authors?:** **Partly** — REGISTRATION.md:65-70 points at the enforcing modules and their boundary fixtures, so a reader is told where the bars are enforced; it is the four numbers themselves and the Section 12 citation that are wrong. Severity is S4 regardless of how that partial disclosure is read.

---

### AUDIT-B-ETFExperiment-7
- **Repository / SHA:** ETFExperiment / `4d110027674e7b4cd2861cf4e0e74f975111daf1`
- **Hypothesis or artifact:** the E1 minimum-N figures 237 / 845 / 3,776 and the simulation budgets stated for them
- **Direction:** B
- **Class:** PROVENANCE
- **Severity:** S4
- **Label:** DERIVED (read from the call site in `scripts/power_gate.py` and the defaults in `src/etf/power.py`, and re-run with the repository's own module)
- **Claim challenged (verbatim quote):**
  "| E1 minimum N at the published 0.18 | **237** | 1,200 draws, 300 sims/cell |" — **ETFExperiment/REGISTRATION.md:1011**
  (read against "Simulation budget stated: E1 at 20,000 permutation draws and 2,000 simulations; E2 at 1,500 draws and 400 simulations" REGISTRATION.md:856-857)
- **Evidence:**
  - The E1 minimum-N figures come from `minimum_n(rho, TARGET)` called with **no budget arguments** (ETFExperiment/scripts/power_gate.py:104-106), so they use that function's defaults, `draws: int = 4_000, simulations: int = 600` (ETFExperiment/src/etf/power.py:232-233). They were computed at **neither** of the two budgets the record states: not the 20,000/2,000 of Amendment 3 (which is CONFIG's `permutation_draws` at src/etf/config.py:162 and `power_simulations` at :172, used for the power *table*), and not the 1,200/300 that Amendment 5's closing table attributes to them — that is E2's grid budget (`e2_power(n, rho, inputs, draws=1200, simulations=300)`, ETFExperiment/scripts/e2_minimum.py:42). Three budgets are in play and the one printed beside the number is the wrong one for **3 of the 3** E1 rows.
  - `minimum_n` bisects: "The smallest n whose E1 power reaches the target. None when hi does not." (src/etf/power.py:236) with `if power >= target: high = mid else: low = mid + 1` (src/etf/power.py:248-251). Bisection presupposes monotonicity in n; the function it bisects is a 600-simulation Monte-Carlo estimate whose non-monotonicity the repository documents elsewhere for the same class of grid — "**That non-monotonicity is simulation noise, not a property of the test**" (ETFExperiment/REGISTRATION.md:969-970).
  - **The figure nevertheless survives.** Recomputed: `minimum_n(0.18, 0.80)` returns **237**, reproducing the published value at the code's own defaults; and at the higher budget the record claims (20,000 draws, 2,000 simulations) power is 0.7570 at n = 220, 0.7955 at n = 230, 0.8150 at n = 237, 0.8135 at n = 245 and 0.8235 at n = 255 (n = 5 grid points) — so the true minimum sits near 232-237 and 237 is not misleading. The defect is the stated budget, not the number.
- **Recomputation:** Inputs — `src/etf/power.py:225-252` (`minimum_n`), `scripts/power_gate.py:104-106`, `src/etf/config.py:162,172`, `scripts/e2_minimum.py:42`. Method: the repository's own `power.py` run unmodified from the work dir (`check_e1.py`). Results: `minimum_n(0.18, 0.80) = 237` in 19 s; `e1_power` at 20,000/2,000 gives the five values above. **Control:** `e1_power(163, 0.18) = 0.6105`, `(163, 0.09) = 0.2015`, `(11, 0.18) = 0.0815`, `(152, 0.18) = 0.6000`, each reproducing `reports/stage_a2/power.json` exactly.
- **What would resolve it:** Correct the n column of Amendment 5 §1 to "4,000 draws, 600 simulations, by bisection", and state that the bisection assumes a monotonicity the estimator does not have.
- **Confidence:** HIGH on the budget misattribution (it is readable from the call site and the defaults); HIGH that the figure itself survives a higher-budget check.
- **Invalidated by later commits?:** No — the repository is closed at this SHA.
- **Disclosed by authors?:** **No** for the misattribution; **yes** for the general point that simulated power grids are noisy (REGISTRATION.md:965-972, report.md:364-367). The misattribution is the finding and it is not disclosed.

---

### AUDIT-B-ETFExperiment-8
- **Repository / SHA:** ETFExperiment / `4d110027674e7b4cd2861cf4e0e74f975111daf1`
- **Hypothesis or artifact:** the registered rationale for E1's form
- **Direction:** B
- **Class:** STATISTICAL
- **Severity:** S4
- **Label:** DERIVED (the comparison is simulated under the generating model and the alpha the repository's own code registers — `src/etf/power.py:47-55`, `src/etf/config.py:160,167-169`)
- **Claim challenged (verbatim quote):**
  "**The threshold-free form is registered deliberately: it uses every admissible
  day and is the highest-powered distribution-free test available on this
  sample.**" — **ETFExperiment/REGISTRATION.md:295-297**
  (repeated at DECISIONS.md:91-92, "It is the highest-powered distribution-free test available on this sample.")
- **Evidence:**
  - **The superlative carries no computation anywhere in the repository.** `reports/stage_a2/power.json` reports E1's power at 3 assumptions × 5 cohort sizes and compares it with no alternative test.
  - **A permutation test on the Pearson correlation is equally distribution-free** — the null is the same label-shuffle null, exact for any marginals — **and under the generating model the registration itself adopts it is more powerful.** The model is stated in the repository's own code: "Exact for a bivariate normal, which is the generating model the power simulation registers" (ETFExperiment/src/etf/power.py:50-51). Simulated at `alpha_adj = 0.0253205655`, one-sided, 2,000 permutation draws and 800 simulations per cell: at n = 163 and a true rank correlation of 0.18, the registered Spearman permutation test reaches **0.6238** against the Pearson permutation test's **0.6575**; at n = 237, **0.8087** against **0.8250**; at n = 300, **0.8625** against **0.8950** (n = 3 cells, 800 simulations each). This is the textbook 0.912 asymptotic relative efficiency of Spearman to Pearson under normality, showing up where the registration's own model puts it.
  - The claim matters a little because E1's minimum N of 237 is the figure the closure is deliberately rested on — "the most favourable figure anywhere on the record" (ETFExperiment/HYPOTHESES.md:70) — and a more efficient distribution-free primary would have lowered it.
- **Recomputation:** Inputs — `src/etf/power.py:47-55` (the generating model), `src/etf/config.py:160` (`alpha_adj=ALPHA_ADJ` = 0.0253205655), `src/etf/config.py:167-169` (the three rho assumptions). Method: an independent numpy implementation of both permutation tests against the same bivariate-normal draws (`pearson_fast.py` in the work dir), 800 simulations × 2,000 permutations per cell; the repository's own code was not modified and was not run for this item. Results as above.
- **What would resolve it:** Either drop the superlative to "the highest-powered distribution-free test considered here, chosen for robustness to the fat-tailed flow distribution", or publish the comparison that justifies it.
- **Confidence:** MEDIUM — the simulation is unambiguous under the registration's own Gaussian model, but the defence the repository does not make is a good one: real flow and return marginals are fat-tailed and asymmetric (the measured signal runs −860.9M to +1,142.4M with median 27.4M, n = 333, `census.json.signal_distribution_live_descriptive`), where a rank test would likely regain the difference. The claim is an unsupported superlative either way.
- **Invalidated by later commits?:** No — the repository is closed at this SHA.
- **Disclosed by authors?:** **No** — the claim is stated flatly in the registration and in the ADR, with no comparison behind it.

---

### AUDIT-B-ETFExperiment-9
- **Repository / SHA:** ETFExperiment / `4d110027674e7b4cd2861cf4e0e74f975111daf1`
- **Hypothesis or artifact:** the shipped per-endpoint pacing table (Amendment 1 §2, report.md A.1 Task 2, ADR-008, docs/ACCESS.md)
- **Direction:** B
- **Class:** INTERNAL_INCONSISTENCY
- **Severity:** S4
- **Label:** DERIVED (recomputed from the stored telemetry artifact `reports/stage_a1/rate_ceilings.json`)
- **Claim challenged (verbatim quote):**
  "Operating paces are therefore set at **twice the fastest verified-clean
  spacing**, the NPLExperiment pattern for an endpoint whose ceiling was not
  found — half the highest verified-clean *rate*, because there is no ceiling to
  halve." — **ETFExperiment/REGISTRATION.md:635-638**
  (same at report.md:150-151 and DECISIONS.md:255-256)
- **Evidence:**
  - **The two formulations are asserted as equivalent and are not**, because observed rate is not monotone in probe spacing when the endpoint's own latency dominates. For `archive.timemap` the ladder recorded **5.78/min at 5.0 s spacing, 21.28/min at 2.0 s, and 12.29/min at 1.0 s** (`reports/stage_a1/rate_ceilings.json`, `archive.timemap` rungs, 6 requests per rung, n = 18, all HTTP 200). "Twice the fastest verified-clean spacing" (1.0 s probed) gives 2.0 s, which is the operating figure. "Half the highest verified-clean *rate*" gives 10.64/min, i.e. a spacing of **5.64 s**.
  - The published table states both the rate and the pace side by side — "| `archive.timemap` | 21.28/min (n = 18) | **2.0 s** |" (ETFExperiment/REGISTRATION.md:645; report.md:145) — so the collector's registered pace permits up to 30/min against a highest-ever-verified-clean 21.28/min for that endpoint, where the stated rule promises half of it.
  - **The other five endpoints are consistent under both readings** (half-rate spacing against the published operating spacing): flow.table 12.17/min → 9.86 s vs 10.0 s; archive.availability 59.92/min → 2.00 s vs 2.0 s; venue.candleSnapshot 59.90 → 2.00 s vs 2.0 s; venue.fundingHistory 59.91 → 2.00 s vs 2.0 s; kraken.ohlc 58.73 → 2.04 s vs 2.0 s. **1 of 6 endpoints disagrees**, by 3.6 s.
- **Recomputation:** Inputs — `reports/stage_a1/rate_ceilings.json` (`highest_verified_clean_rate_per_min`, `operating_min_spacing_s`, and per-rung `spacing_s` / `observed_rate_per_min` / `all_200` for all six endpoints; 96 requests total, all 200, reproducing the published count). Method: arithmetic, `60 / (rate/2)` against the published operating spacing (re-run at consolidation, 2026-09-04). Result: five of six agree to 0.05 s; `archive.timemap` disagrees by 3.6 s, the operating pace being 2.8× faster than "half the highest verified-clean rate".
- **What would resolve it:** State the rule as the spacing rule alone ("twice the fastest spacing probed clean"), and note that for `archive.timemap` the observed rate fell at 1.0 s because the endpoint's own latency, not a server limit, bounded throughput.
- **Confidence:** HIGH on the arithmetic; the practical risk is small, since 2.0 s is still slower than the fastest spacing verified clean and every one of the 96 probes returned 200.
- **Invalidated by later commits?:** No — the repository is closed at this SHA.
- **Disclosed by authors?:** **Partly** — the record does say "**The figures are bounded by what was probed, not by what the server would refuse**" (report.md:155-156; REGISTRATION.md:638-639), which covers the ceiling question but not the disagreement between the two stated forms of the pacing rule. Severity is S4 regardless.

---

## What Agent B checked and found sound

The thesis did not hold on any of the following, several of which I expected to break.

1. **The pre-registration really is prior to the data.** `git log --date=iso` on the live repository: scaffold and all five guards at 815f888 (2026-08-28 01:05:56 −0700), Section 0 plus `section0.py` and `observability.py` at 44567f6 (01:07:59), Sections 1-12 at e33b03c (01:09:26), Sections 13-14 and HYPOTHESES.md at 38b9397 (01:11:17); the first network-derived artefact lands at 97da329 (13:04:41), twelve hours later. `git log --follow` confirms `section0.py` and `observability.py` first appear in the Section 0 commit, as REGISTRATION.md:65-66 claims.
2. **No registered bar moved after data existed.** `git diff 815f888 0cd8572 -- src/etf/config.py` shows the sole post-network change to the frozen config is the addition of the three Farside URL fields, which Amendment 1 §1 registers. All power floors, cost bands, effect assumptions, coverage bars, observability bars and sample minima are byte-identical from the first scaffold commit to the anchor.
3. **The amendments record falsifications rather than rescue verdicts.** Amendment 2 falsifies Amendment 1's own 0.1111 density and moves it against the repository's interest to 0.0330 (REGISTRATION.md:711-738). Amendment 4 corrects Amendment 3's governing minimum N *upward* from 237 to 300, enlarging the shortfall (REGISTRATION.md:947-986). Amendment 6 corrects Amendment 5's reopen-path label in the direction that removes the argument for keeping a collector alive (REGISTRATION.md:1096-1137). I looked specifically for an amendment that widened a bar or re-specified a definition after seeing a number; there is none.
4. **The favourable figure was not promoted.** The retro revision rate of 0 revised / 0 sign flips / 0 threshold crosses on n = 11 would have cleared the 0.90 revision-integrity bar and completed Section 0 as DEGRADED. It is refused on the pre-registered n ≥ 30 rule at REGISTRATION.md:889-895, at report.md:222-226, and again at Amendment 6 (REGISTRATION.md:1149-1153), where future citation of it is forbidden. This is the single most obvious place a positive could have been manufactured and it was not.
5. **Every E1 power figure reproduces exactly.** Running the repository's own `power.py` unmodified: 0.6105 at n = 163 ρ 0.18; 0.2015 at n = 163 ρ 0.09; 0.0815 at n = 11; 0.6000 at n = 152 — identical to `reports/stage_a2/power.json` to four decimals.
6. **The E2 minimum N of 300 is right for the test that was run, and the disclosed caveat is conservative.** `scripts/e2_minimum.py:45-47` breaks at the first grid point clearing 0.80, so 350 and 400 were never evaluated at the published assumption. I evaluated them: 0.8633 at n = 350 and 0.9500 at n = 400, so 300 is the crossing, and Amendment 5's warning that "the true E2 minimum could be 350 or 400" (REGISTRATION.md:1020-1021) errs against the repository.
7. **Every archive figure reproduces exactly from the stored timemaps.** 451 union mementos, 153 out-of-sample, 0.3161 mementos per calendar day over 484 days, 37/333 = 0.1111 under the registered window, 74/153 = 48.37 percent of mementos inside 20:00-08:00 UTC, and 112/333 = 0.3363 under an unbounded D-or-D+1 window. The published 0.3363 is a capture ceiling quoted beside a served-value density of 0.0330 — two different measures in one sentence — but as an *upper bound* on what any window-widening could yield it is valid, and the conclusion "widening the window is foreclosed as an explanation" holds.
8. **The flow-source counts reproduce exactly:** 676 date rows, 336 on or after 2025-05-01, 333 printing all five registered funds, from `data/access/farside_all_parsed.json`. SoSoValue's 660 rows reproduce too.
9. **The retro print-window figures reproduce.** Recomputed from `reports/stage_a1/retro_revision.json`: served-value captures at +04:04.6 to +07:59.7 past midnight D+1 (n = 11) and still-dashed captures at −03:37.7 to +04:29.0 (n = 23), matching docs/ACCESS.md:413-415 to the minute. The retro cohort of 8 days is the correct intersection of the 11 served days with the 2026-02-01 candle window, and the eight dates listed at REGISTRATION.md:744-745 are exactly the ones I derive.
10. **The census adds up and separates instrument fault from cohort.** 11 admissible + 53 capture-too-late + 243 no-capture + 25 capture-served-no-value + 3 no-printed-value + 1 archive-fetch-failed = 336 (`census.json.exclusion_reasons`); the HTTP 403 day is `source_failed` with admissibility unknown rather than an exclusion (Amendment 2 §5, REGISTRATION.md:806-810), which is the correct handling and was a self-caught defect.
11. **Outcome blindness holds where I could check it.** `verdict.py` is imported by nothing (pinned at tests/test_verdict.py:94-99), refuses sealed paths in code (src/etf/verdict.py:36-45), and contains no statistic outside Section 8's list. The pre-period pin is enforced on the parse tree with a one-file allowlist (ADR-007) and was demonstrated on live payloads (72 of 72 readable pre-boundary, 500 of 500 gated post-boundary).
12. **The closure is typed conservatively.** `untestable-at-achievable-power` rather than `signal-absent` is the right type given that no outcome value was read, and the register states the difference and forbids the mistyping (REGISTRATION.md:1050-1058, DECISIONS.md:559-561). The epistemic boundary — that nothing here is evidence about whether ETF flows predict BTC returns — is stated in four places without hedging.
13. **The self-reported defects are real and were found by the repository, not by me:** the process-local rate limiter that paced nothing across systemd invocations (ADR-014), the unbounded `capture_too_late` test reporting 296 against 53, the failed fetch filed as an exclusion, and two mutation-harness anchors broken by `ruff format`. All four are recorded with the wrong number left visible.
14. **The Citi note is recorded as FAILED TO CONFIRM rather than corroboration** (ADR-012, REGISTRATION.md:518-533), which is the harder and the correct call, and the contradicting evidence of Section 14.4 is carried into the registration rather than omitted.
15. **The E2 grid non-monotonicity is disclosed rather than smoothed** (REGISTRATION.md:965-972), and the stated standard errors (0.0289 at 300 simulations, 0.0231 at the 0.80 bar) are correct binomial figures.

Where I expected the thesis to hold and it did not: I looked for a positive inside the corpus of negatives and there is none — the repository shipped no positive result, no tradeable artifact, and no verdict. The two S1 findings are both about *inputs to a negative*: a co-primary whose registered content is not implemented, and a projection labelled measured. Both matter because a negative reached by a process that would also have produced a positive on noise is a claim that outran its evidence, and AUDIT-B-ETFExperiment-1 is precisely that — the E2 engine as built passes a strategy losing 8.9 percent per trade.

## Dropped at consolidation

The drafting pass produced one part ("all") with nine draft findings; **no draft finding was dropped for want of a locatable quote, a figure or an n**, and **no two drafts challenged the same claim on the same grounds**, so nothing was merged away. What happened instead is recorded here in full.

**Considered and not raised as findings** (each fails rule 4 — no figure with an n — or is already the repository's own disclosure):

1. **The operator-prior inconsistency.** README.md:80-83 says "**REGISTRATION.md Section 13 reserves an operator prior and it is empty.** The empty slot blocks Stage B structurally", while progress.md:558 says "**Open operator items: none.**" Two shipped documents at the same SHA disagree on whether the item is open. Dropped as a finding because it has no figure and no n — it is a one-item disagreement about a label, not a claim about evidence. Recorded in the positives ledger at D1 instead.
2. **The 112/333 capture ceiling quoted beside the 0.0330 served-value density** (HYPOTHESES.md:84, REGISTRATION.md:1062-1064). Two different measures appear in one sentence, but the 0.3363 is used only as an upper bound on what widening the window could yield, and in that use it is valid. Recorded in the sound list (item 7) and in the ledger at B3.
3. **The selection of the n = 11 retro sample** (these are the days a third party's crawler happened to capture after the print and before 08:00 UTC, which plausibly over-samples early-printing days). The repository does not make this argument, but it also refuses the figure any verdict at three separate sites, so there is no claim left to challenge. Recorded in the ledger at B4.
4. **Amendment 5 §2's "moot rather than resolved" PARTIAL/FAIL choice** (report.md:465-470). This is the one place a label was chosen without its registered input, and the repository says so in those words — a disclosed limitation, S3 at most, and better recorded as a ledger entry (A4) than as a discovery.

**Corrections applied to draft line citations during consolidation** (every quote in this file was re-verified character-by-character against `SNAP/ETFExperiment`; eight cites were off by one or two lines and are corrected here):

| draft cite | corrected cite | text |
|---|---|---|
| scripts/power_gate.py:35 | **scripts/power_gate.py:34-35** | "The projection uses the MEASURED printed-day rate rather than a calendar assumption" |
| DECISIONS.md:92-93 | **DECISIONS.md:91-92** | "It is the highest-powered distribution-free test available on this sample." |
| REGISTRATION.md:635-639 | **REGISTRATION.md:635-638** | the pacing rule sentence |
| report.md:144 | **report.md:145** | the `archive.timemap` table row |
| report.md:150-153 | **report.md:150-151** | the pacing rule sentence in the report |
| src/etf/power.py:232-234 | **src/etf/power.py:232-233** | `draws: int = 4_000, simulations: int = 600` |
| REGISTRATION.md:1021-1022 | **REGISTRATION.md:1020-1021** | "the true E2 minimum could be 350 or 400" |
| REGISTRATION.md:856-858 | **REGISTRATION.md:856-857** | "Simulation budget stated: E1 at 20,000 permutation draws and 2,000 simulations" |
| DECISIONS.md:347-350 | **DECISIONS.md:348-349, 349-351** | "it is the wrong universe anyway" / the 47.42M attribution |
| DECISIONS.md:211-213 | **DECISIONS.md:211-212** | "The E2 economic-power computation needs a volatility and a funding level…" |
| REGISTRATION.md:571-573 | **REGISTRATION.md:571-572** | "Therefore: no accrual, coverage, lag… figure … is registered before it is measured." |
| REGISTRATION.md:1152-1153 (for the verbatim) | **report.md:518-519** | "may not be cited by anything later as evidence of source stability" (the register's own wording at REGISTRATION.md:1151-1153 differs) |

**One draft attribution checked and confirmed correct:** `trade_share` 0.7567567567567568 is indeed in `reports/stage_a2/census.json` (under `signal_distribution_live_descriptive`) as well as in `reports/stage_a2/power.json` → `economic_inputs`.

**One recomputation re-run at consolidation rather than taken on trust:** the E2 cost-invariance of `run_e2` (AUDIT-B-ETFExperiment-1) was re-executed on 2026-09-04 from the copied package in the work dir and reproduced the draft's figures exactly (`p = 0.000250, passes = True` at 0/3/9/18/100/1000 bp; `mean_net` +0.011089 → −0.088911; n = 200 days, 153 trades). The `archive.timemap` pacing arithmetic (AUDIT-B-ETFExperiment-9) and the REGISTRATION.md:1-589 grep (AUDIT-B-ETFExperiment-6) were likewise re-run.

## Live-repo access log

Before (first live access, `git -C /home/kiros-li/Documents/GitHub/ETFExperiment status --porcelain`):

```
```
(empty — clean tree; `git rev-parse HEAD` = `4d110027674e7b4cd2861cf4e0e74f975111daf1`, matching the anchored SHA)

Live-repo operations, all read-only: `git status --porcelain`, `git rev-parse HEAD`, `git log --oneline --all`, `git log --reverse --pretty=format:"%h %ad %s" --date=iso`, `git log --follow` on five paths, `git show 815f888:src/etf/config.py`, `git show --stat 815f888`, `git diff 815f888 0cd8572 -- src/etf/config.py`, and read-only reads of the untracked files `data/access/farside_all_parsed.json`, `data/access/sosovalue-btc.html`, `data/access/timemap-recent.txt`, `data/access/timemap-all_data.txt`, plus `ls` of `data/`. All untracked reads were made on 2026-09-04 (UTC) and are **UNANCHORED**: they may have changed after the 2026-08-28 anchor, though every count derived from them reproduces a figure published at the anchor. No `.env`, credential, token or session file was opened; none exists in the tree (`.env.example` is empty by design).

The consolidation pass (2026-09-04, ~21:1x UTC) touched the **live repository not at all**: it read only `SNAP/ETFExperiment/` and re-ran scripts in `/home/kiros-li/.cache/program-audit/scratchpad/work/agentB-etf/`, whose copy of the `etf` package was made during the drafting pass.

After (`git -C /home/kiros-li/Documents/GitHub/ETFExperiment status --porcelain`):

```
```
(empty — clean tree, unchanged; `git rev-parse HEAD` = `4d110027674e7b4cd2861cf4e0e74f975111daf1`. Nothing in the audited repository was modified, created or deleted. No pre-existing dirt was present before or after, and none of the entries listed in COMMON_RULES as expected dirt applies to this repository.)
