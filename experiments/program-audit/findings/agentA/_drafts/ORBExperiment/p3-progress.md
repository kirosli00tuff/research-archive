# Agent A draft findings — ORBExperiment, part p3-progress

**Repository / anchored SHA:** ORBExperiment / `f2aa675a80fc06b74979040b3028154d1add5ec0` (main, 2026-08-29)
**Documents read completely:** `progress.md` (3,737 lines, all 36 entries), every file under `reports/`
(`stage_a1r`, `stage_a1amend`, `stage_a2`, `stage_a2repair`, `stage_a3rescue`, `stage_a4`), `tools/`
inventory plus `tools/slippage_band.py` in full. Read for context: `HYPOTHESES.md`, `DECISIONS.md`
ADR-038, `REGISTRATION.md` Sections 3, 8, 9, 11, `docs/HANDOVER.md`, `docs/STAGES.md`,
`src/orb/{signal,costs,costs_registered,config,dispersion,power}.py`.

**Direction A summary in one sentence.** This repository closed H1 as `cost-bound` on 2026-08-30 on a
single number — a measured pessimistic-minus-central slippage shift of **0.467065 USD/share** against
a threshold of **0.040386** — and that number reproduces exactly from the published artifacts, but
**29.3 percent of it is a term that is not a cost**, **57.3 percent of it is a fill price the
registered entry order cannot produce**, and **all three of its deciding percentiles rest on 28
session-days with no interval placed on any of them**. The closure's *outcome* at the registered
1.40 assumption survives every correction I could construct; the closure's *strongest sentence* —
that it also holds at the source study's undecayed 2.81 with "no sample size" reaching the target —
does not.

Recomputation script and its full output: `/home/kiros-li/.cache/program-audit/scratchpad/work/agentA-ORB-p3/recompute.py`
(run 2026-09-04, venv at `scratchpad/venv/bin/python`).

---

### DRAFT-p3-progress-1
- **Repository / SHA:** ORBExperiment / f2aa675a80fc06b74979040b3028154d1add5ec0
- **Hypothesis or artifact:** H1 (H-ORB) closure `cost-bound`, 2026-08-30 — the close-exit leg of the measured slippage band (A.3 rescue pass TASK 2)
- **Direction:** A
- **Class:** ARITHMETIC
- **Severity:** S1
- **Label:** DERIVED
- **Claim challenged (verbatim quote):** "| close, central | 0.0100 | **0.040000** | **4.00×** | **UNDERSTATED** |
| close, pessimistic | 0.0200 | **0.261000** | **13.05×** | **UNDERSTATED** |" — ORBExperiment/progress.md:3589-3590
- **Evidence:**
  - The close-exit "slippage" is computed as an **unsigned** difference between two bar closes:
    `close_slippage.append(abs(row.official_close_c - row.last_exit_window_close_c) / CENT)` —
    ORBExperiment/src/orb/dispersion.py:943-944.
  - Its two operands are: `window_close_c = close_exit_c(inside, (exit_start_ms, exit_end_ms))`
    (ORBExperiment/src/orb/dispersion.py:388), which is "the close of the last bar inside the
    registered exit window" over the **half-open** interval `start <= ts < end`
    (ORBExperiment/src/orb/signal.py:176-182) — i.e. the **15:58 minute bar's close**; and
    `official_close_c`, the earliest bar in `[exit_end_ms, exit_end_ms + 120_000)`
    (ORBExperiment/src/orb/dispersion.py:389-393) — i.e. the **15:59 minute bar's close**.
  - So the measured quantity is `|close(15:59 bar) − close(15:58 bar)|`: **the absolute one-minute
    price change over the last minute of continuous trading**. It carries **no trade side** (the
    trade's `side` is never consulted at dispersion.py:938-945), **no quoted spread** (unlike the
    entry and stop legs, which measure `overshoot + time-weighted half spread` at
    dispersion.py:889-902 and 923-936), and **no execution**.
  - A signed, symmetric timing difference has expectation ≈ 0 and contributes to *dispersion*, not to
    *mean cost*. Dispersion is separately measured and separately used (2.029585 USD/share, n = 550,
    ORBExperiment/reports/stage_a3rescue/task3_rescue_verdict.json `dispersion_usd_per_share`). Taking
    `abs()` charges the adverse sign on every trade and double-counts a quantity already carried by σ.
  - The leg's own only description in source concedes the sign it then drops: "A real market-on-close
    order fills at the official closing print, and the gap between them is the close leg's realized
    slippage" — ORBExperiment/src/orb/dispersion.py:385-386.
  - Published values: `close_slippage: {mean 0.09932352941176471, median 0.04, p90 0.26100000000000023,
    n 340, without_an_official_print 0}` —
    ORBExperiment/reports/stage_a3rescue/task2_slippage_band.json (`per_leg_statistics.close_slippage`).
  - `ADR-038`, the ADR that registers the band's method, describes the entry and stop legs
    ("the **time-weighted quoted half spread** across each entry and stop minute is measured and added
    to the overshoot", ORBExperiment/DECISIONS.md:1446-1451) and **never describes the close leg at
    all** (ORBExperiment/DECISIONS.md:1424-1476, read in full).
- **Recomputation (if any):**
  - Inputs, all from ORBExperiment/reports/stage_a3rescue/task2_slippage_band.json: entry central
    0.08701938620876422 / pessimistic 0.35464495116577943; stop 0.03352891210212913 /
    0.19806129713302226; close 0.04 / 0.26100000000000023; `stop_exit_share_used` 0.3818181818181818.
  - Method: reproduce `shift = (entry_p − entry_c) + s·(stop_p − stop_c) + (1 − s)·(close_p − close_c)`
    exactly as `orb.dispersion.measure_carve_out_slippage_band` computes it
    (ORBExperiment/src/orb/dispersion.py:953-960), then decompose it.
  - Result: recomputed shift **0.46706520287790176**, identical to the published
    `measured_shift_usd_per_share` to the last digit (difference +0.00e+00). Decomposition:
    entry **0.267626 (57.3 %)**, stop **0.062821 (13.5 %)**, **close 0.136618 (29.3 %)**.
  - The close component alone is **3.383×** the entire `RESCUED_DEGRADED` threshold of 0.040386
    (ORBExperiment/progress.md:3613).
  - **What survives the correction, stated so the finding is not over-read.** Setting the close-leg
    shift to zero gives shift 0.330447, pessimistic-cost mean −0.290061 at the registered 1.40 and
    −0.249386 at the published 2.81, E2 power 0.000000 in both. **The `NOT_RESCUED` outcome and the
    `cost-bound` closure survive this correction on their own.** What does not survive is the stated
    conclusion quoted above — the carried 0.020 close-exit *slippage* assumption is not shown to be
    "UNDERSTATED by 13.05×", because 0.261 is a one-minute absolute price change and not a slippage
    figure of the same kind — and the close leg's 29.3 percent contribution to the deciding number.
- **What would resolve it:** re-run `orb.dispersion.measure_carve_out_slippage_band` with the close
  leg computed as a **signed** difference against the traded side (or, better, as the time-weighted
  quoted half spread across the exit minute, which is the definition the other two legs already use
  and which the tier serves — 760 quote minutes served, 0 refused, ORBExperiment/progress.md:3576-3577),
  and re-state the band table and the `measured_against_carried` verdicts against a like-for-like
  carried figure.
- **Confidence:** HIGH — the operand definitions are read directly from source and the decomposition
  reproduces the published deciding number to the last digit.
- **Invalidated by later commits?:** no — the live repository's HEAD is the anchored SHA
  `f2aa675a80fc06b74979040b3028154d1add5ec0` with a clean working tree as of 2026-09-04, so no commit
  after the anchor exists to change it.
- **Disclosed by authors?:** no — ADR-038 (ORBExperiment/DECISIONS.md:1424-1476), Amendment 26, the
  A.3 TASK 2 entry (ORBExperiment/progress.md:3573-3610) and the H1 closure row
  (ORBExperiment/HYPOTHESES.md:59) all present the six band ends as one homogeneous "measured
  slippage band"; none records that the close leg is measured on a different quantity from the other
  two, and none records that it is unsigned.

---

### DRAFT-p3-progress-2
- **Repository / SHA:** ORBExperiment / f2aa675a80fc06b74979040b3028154d1add5ec0
- **Hypothesis or artifact:** H1 closure `cost-bound` — the entry leg of the deciding band against the registered entry order type
- **Direction:** A
- **Class:** INTERNAL_INCONSISTENCY
- **Severity:** S2
- **Label:** DERIVED
- **Claim challenged (verbatim quote):** "**Under the MEASURED
band it is 0.000000 there too**, with a pessimistic-cost mean of **−0.386004**.
**The closure holds at the source study's own undecayed magnitude, which makes it
stronger than expected, not weaker.**" — ORBExperiment/progress.md:3623-3626
- **Evidence:**
  - The registered entry is a **marketable limit**: "Modeled as a **marketable limit at the range
    boundary plus 0.05 percent of price** (5 basis points), in the direction of the break" —
    ORBExperiment/REGISTRATION.md:302-304; identically in the operator prompt logged in my primary
    document at ORBExperiment/progress.md:141.
  - The cap is implemented and pinned: `offset = boundary_c * CONFIG.entry_offset_fraction; return
    boundary_c + max(1, int(offset + 0.9999999))` — ORBExperiment/src/orb/signal.py:87-96, with
    `entry_offset_fraction=0.0005` at ORBExperiment/src/orb/config.py:245, and a one-cent floor
    exercised by `test_the_entry_offset_floor_of_one_cent_binds_on_a_cheap_name`
    (ORBExperiment/tests/test_known_answers.py:320-323). So the **maximum modeled entry fill under
    the registered order is `boundary + max(0.01, 0.0005·P)`**.
  - The Section 6 slippage is charged **on top of** that already-capped fill:
    `slippage = shares * (self.slippage_per_share(Leg.ENTRY, band) + self.slippage_per_share(exit_leg, band))`
    — ORBExperiment/src/orb/costs.py:222-226, applied to a trade whose entry price is
    `entry_price_c`. The model therefore prices a fill strictly worse than the limit price of the
    order it registered.
  - The measured entry figures are **central 0.087019 and pessimistic 0.354645, n = 550**
    (ORBExperiment/reports/stage_a3rescue/task2_slippage_band.json,
    `per_leg_statistics.entry_slippage_total`), of which the dominant term is the quoted half spread —
    "**The driver is the entry half spread: median 0.076572, p90 0.333662, `n = 550`.**" —
    ORBExperiment/progress.md:3595. A marketable limit is precisely an order that **declines to pay**
    more than its offset; a quote 0.35 USD through the boundary produces a **non-fill**, not a worse
    fill.
  - The cap binds on the bulk of the deciding sample. `max(0.01, 0.0005·P) < 0.087019` for every name
    priced below **174.04 USD**; the H1b floor scan on the same 28 sessions records
    `eligible_name_sessions` of 560 at a 5 USD floor, **446 at 50 USD and 310 at 100 USD**
    (ORBExperiment/reports/stage_a3rescue/task4_floor_scan.json), so at least 250 of 560 selected
    name-sessions sit below 100 USD and every one of the 560 sits below the 174 USD indifference
    price on the published evidence.
  - Nothing in ADR-038 (ORBExperiment/DECISIONS.md:1424-1476), Amendment 26, `tools/slippage_band.py`
    (read in full, 299 lines) or `orb.dispersion.measure_carve_out_slippage_band` mentions the limit,
    the offset, `entry_price_c`, or fill probability. `grep -rn "marketable limit"` over the snapshot
    returns hits only in `src/orb/signal.py:8,88`, `REGISTRATION.md:302`, `docs/STAGE_A_PROMPT.md:117`
    and `progress.md:141` — none of them in the rescue pass.
- **Recomputation (if any):**
  - Inputs as in DRAFT-1, plus σ = 2.029585030455633, trades-per-session 19.642857142857142
    (ORBExperiment/reports/stage_a2repair/task3_execution_mix.json), α = 0.05
    (ORBExperiment/src/orb/config.py:256), central mean per unit of annual Sharpe 0.028847265
    (ORBExperiment/reports/stage_a2repair/task4_joint_power.json
    `central_mean_per_unit_of_annual_sharpe`), and `orb.power.e2_power_pessimistic`'s formula
    `Φ((central − shift)/σ · √trades − z(1−α))` (ORBExperiment/src/orb/power.py:113-140).
  - Method: under a marketable limit both band ends truncate at the same cap whenever the cap is
    below the measured median (true for every name under 174.04 USD), so the **entry contribution to
    the shift is 0**. Combined with DRAFT-1's correction of the close leg, recompute the shift and
    re-run E2, joint power and the minimum sample.
  - Result, holdout n = 875: shift falls **0.467065 → 0.062821**; pessimistic-cost mean at the
    published **2.81** goes **−0.386004 → +0.018239**; **E2 power 0.000000 → 0.320370**; joint power
    **0.000000 → 0.320370**; and the minimum sample stops being an absence — **76,554 trades =
    3,897 sessions** clears E2 at 80 percent, against the published "unreachable at any sample size".
  - **At the registered 1.40 assumption the closure survives every reading I constructed**
    (pessimistic mean −0.022435, E2 power 0.000987), and I say so plainly. The claim that fails is
    the quoted one: the closure does **not** demonstrably hold at the source study's undecayed
    magnitude once the deciding number is made consistent with the order type the registration fixed.
  - Two further readings of the same measured data, for calibration: applying the **registered 2×
    pessimistic multiple** to the measured central figures gives shift 0.124549 and break-even Sharpe
    4.318; using the **distribution means** rather than percentiles gives shift 0.113393 and
    break-even Sharpe 3.931. Both leave the closure standing at 1.40 and at 2.81. The published band
    implies a break-even Sharpe of **16.191**; these readings imply 2.178 to 4.318.
- **What would resolve it:** state in the band ADR whether the registered marketable limit caps the
  modeled entry fill or not; if it does, cap the entry band at `max(0.01, 0.0005·P)` per name and
  carry the non-fill rate as a measured reduction in the trigger rate; if it does not, record the
  amendment that converts the registered entry to a market order and re-derive the trigger rate.
  Either way re-run TASK 3's criterion evaluation.
- **Confidence:** MEDIUM — the internal inconsistency (a charged fill worse than the registered limit)
  is HIGH-confidence and read from source; the size of the correction depends on the per-name price
  distribution, which the published artifacts do not give directly and which I bounded from the floor
  scan rather than measured.
- **Invalidated by later commits?:** no — live HEAD equals the anchored SHA with a clean tree at
  2026-09-04.
- **Disclosed by authors?:** no — the rescue pass, ADR-038 and the closure record never mention the
  registered limit offset, and `progress.md` Entry 35 presents the entry band as a straight
  measurement against the carried QQQ figure.

---

### DRAFT-p3-progress-3
- **Repository / SHA:** ORBExperiment / f2aa675a80fc06b74979040b3028154d1add5ec0
- **Hypothesis or artifact:** H1 closure — the sampling precision of the three deciding percentiles
- **Direction:** A
- **Class:** STATISTICAL
- **Severity:** S2
- **Label:** DERIVED
- **Claim challenged (verbatim quote):** "> **Pessimistic-cost mean −0.426679. E2 0.000000. JOINT 0.000000. Minimum n jointly: unreachable at any sample size, at every assumption.**" — ORBExperiment/progress.md:3615
- **Evidence:**
  - The deciding band is three sample 90th percentiles and three sample medians, taken once:
    `sessions_used: 28`, `name_sessions_evaluated: 560`, `tickers_with_bars: 199`, entry n = 550,
    stop n = 210, close n = 340 — ORBExperiment/reports/stage_a3rescue/task2_slippage_band.json.
  - The 28 sessions are all of the evaluable post-holdout sessions that existed on the closure date:
    42 pulled, 28 evaluable after the registered 14-session lookback —
    ORBExperiment/reports/stage_a2repair/task3_execution_mix.json (`sessions_pulled: 42`,
    `sessions_used: 28`).
  - The 199 tickers are a 1-in-26 systematic sample: "the reference listing walked in full by cursor,
    **`n = 5,317` active US common stocks over 6 pages**, **every 26th ticker** taken, **`n = 200`,
    A to WSM**, of which **199 served at least one bar**" — ORBExperiment/progress.md:2668-2670.
  - **No interval, standard error, bootstrap or sensitivity is attached to any of the six band ends**
    anywhere in `task2_slippage_band.json`, `task3_rescue_verdict.json`, ADR-038, Amendment 26, or
    ORBExperiment/progress.md Entry 35 (3573-3610). The three per-trade distributions themselves are
    not published — only mean, median and p90 — so no later reader can construct one.
  - The repository registered, before the closure, that the sample this figure comes from **grows for
    free**: "State explicitly in the amendment that the post-holdout region grows as real time
    advances" — ORBExperiment/progress.md:2211. And the measurement is cheap: the whole band cost
    `n = 759` quote requests (ORBExperiment/progress.md:3735) against an Alpaca daily cap of 3,000 of
    which 1,879 were spent in a single earlier day (ORBExperiment/progress.md:2909), at **0 dollars**.
  - The closure nonetheless pre-registered that no further measurement would be taken: "**H1 closes as
    cost-bound … and no further rescue lever is applied.**" — ORBExperiment/progress.md:3430.
  - The repository elsewhere applies exactly the discipline missing here: it bounded a zero count with
    the rule of three ("a one-sided 95 percent upper bound on 0 events in `n = 560` is **3/560 ≈
    0.0054**", ORBExperiment/progress.md:3223-3224) and refused to report an unreached ceiling as a
    number (ADR-026, ORBExperiment/progress.md:1782-1785).
- **Recomputation (if any):**
  - Method: binomial order-statistic interval for a population 90th percentile. Under i.i.d.
    sampling the 95 percent interval spans sample order statistics `k` with
    `Binom(n, 0.90).ppf(0.025) ≤ k ≤ Binom(n, 0.90).ppf(0.975)`.
  - Result at the published n: entry p90 (n = 550) spans sample percentiles **0.875–0.924**; stop p90
    (n = 210) spans **0.857–0.938**; close p90 (n = 340) spans **0.868–0.929**. These are the
    *floor* of the uncertainty, because up to 20 of the observations share a session date and
    intraday spread and closing-drift are strongly correlated within a session.
  - At the other extreme — treating the **28 session-days** as the independent unit, which is the same
    clustering E2's own permutation uses ("permutation on session labels with trades clustered by
    session date", ORBExperiment/progress.md:156, 3052-3053) — the same interval spans sample
    percentiles **0.786–1.000**: at the effective sample the deciding p90 is **not statistically
    distinguishable from the sample maximum**, which is the statistic ADR-038 explicitly rejected as
    "one session's news gap" (ORBExperiment/DECISIONS.md:1442-1444).
  - The true effective n lies between 28 and the published n and cannot be computed from the released
    artifacts. That is the finding: a permanent closure whose headline is "unreachable at any sample
    size" rests on three point estimates whose own sampling interval was never computed and cannot be
    reconstructed by a reader.
- **What would resolve it:** publish the three per-trade slippage distributions (or a cluster
  bootstrap over the 28 session dates) with a 95 percent interval on each band end, and re-evaluate
  the Amendment 24 criterion at the favourable end of those intervals; and/or re-measure the band on
  the post-holdout sessions that have accrued since 2026-08-28, which the registration already says
  grow with real time and which cost 0 dollars.
- **Confidence:** MEDIUM — the arithmetic of the interval is exact, but the effective n under
  clustering is bounded rather than measured, so the width of the true interval is a range, not a
  number.
- **Invalidated by later commits?:** no — live HEAD equals the anchored SHA with a clean tree at
  2026-09-04. It would be *resolved* rather than invalidated by any later re-measurement.
- **Disclosed by authors?:** partially — the closure discloses two *directional* limits of the band
  (post-holdout regime, and lower-bound overshoot at one-minute resolution;
  ORBExperiment/HYPOTHESES.md:62, ORBExperiment/progress.md:3604-3607) and both run in the direction
  that strengthens the closure. Neither is a sampling interval, and no sampling uncertainty on the
  deciding percentiles is disclosed anywhere.

---

### DRAFT-p3-progress-4
- **Repository / SHA:** ORBExperiment / f2aa675a80fc06b74979040b3028154d1add5ec0
- **Hypothesis or artifact:** H1 closure `cost-bound` — the 15, 30 and 60-minute opening-range lengths and the immediate-direction entry, 6 of the 8 registered trials
- **Direction:** A
- **Class:** OVER_CLOSED
- **Severity:** S3
- **Label:** DERIVED
- **Claim challenged (verbatim quote):** "> # **H1 is CLOSED — `cost-bound` — 2026-08-30.**" — ORBExperiment/progress.md:3659, together with "says plainly that **there is no ladder any more.**" — ORBExperiment/progress.md:3691
- **Evidence:**
  - The registration prices **eight** parameterisations into the co-primary itself: "with the trial
    count registered at 8, being four opening-range lengths of 5, 15, 30 and 60 minutes crossed with
    two entry rules of immediate-direction and true-breakout" — ORBExperiment/progress.md:155
    (mirrored at ORBExperiment/REGISTRATION.md:439). The other three lengths and the other entry rule
    are registered named secondaries — ORBExperiment/progress.md:158,
    ORBExperiment/REGISTRATION.md:465.
  - Only the 5-minute length was ever instantiated: `opening_range_minutes=5` with the docstring
    "5. The registered range length. 15/30/60 are named secondaries." —
    ORBExperiment/src/orb/config.py:238 and :67-68. No report artifact under `reports/` computes any
    figure at 15, 30 or 60 minutes (full inventory of `reports/` read).
  - The cost that closed H1 was measured at the **09:35 trigger minute only**:
    `load_quotes(ticker, row.trigger_ms, row.trigger_ms + 60_000)` —
    ORBExperiment/src/orb/dispersion.py:889, where `row.trigger_ms` is the first bar after the
    5-minute range. The entry leg supplies **57.3 percent** of the deciding shift (recomputed in
    DRAFT-1) and is **88 percent quoted half spread** (median half spread 0.076572 of a median total
    0.087019, ORBExperiment/reports/stage_a3rescue/task2_slippage_band.json). The quoted spread at
    09:35 is the widest minute of the regular session, and the range length is the one registered
    knob that moves the entry minute.
  - The rescue pass had the entitlement, the tooling and the bars to vary it and did not: NBBO quotes
    are served ("**The tier serves NBBO quotes** … **760 quote minutes served, 0 refused**, `n = 759`
    requests", ORBExperiment/progress.md:3575-3577); 1,927,156 bars over 42 sessions were already
    sealed on disk and re-reading them costs nothing ("**0 requests sent** — the bytes were sealed on
    2026-08-29 and re-reading a stored file is not a vendor call",
    ORBExperiment/progress.md:3204). The pass instead scanned the **price floor** (H1b), whose own
    registered mechanism is that "**per-share slippage is approximately invariant to price**"
    (ORBExperiment/HYPOTHESES.md, H1b motivation row) — i.e. the pass varied the parameter its own
    mechanism says does **not** move the cost, and did not vary the one that does.
- **Recomputation (if any):**
  - Inputs and method as in DRAFT-1. Result, stated against my own thesis: **zeroing the entry leg
    entirely leaves a shift of 0.199440**, still 4.94× the 0.040386 threshold, so a range-length
    change **cannot on its own** reverse `NOT_RESCUED` on the published numbers. The claim this
    finding supports is narrower and is about scope, not sign: the closure is stated as a closure of
    H1, and H1's own registered trial space contains six parameterisations whose deciding cost term
    was never measured, at zero marginal cost and with no blocker.
  - The entry leg only stops mattering below a shift of 0.018240 (the value at which the published
    2.81 case turns positive once DRAFT-1's close-leg correction is applied), so the untested lengths
    are the lever that interacts with the two corrections above rather than an independent one.
- **What would resolve it:** re-run `orb.dispersion.measure_carve_out_slippage_band` with
  `CONFIG.opening_range_minutes` at 15, 30 and 60 on the already-sealed post-holdout bars, requesting
  quotes for the corresponding trigger minutes, and record the entry half spread and resulting shift
  per length beside the 5-minute figures; or state in the closure that H1's `cost-bound` verdict is
  scoped to the 5-minute length and that the other three registered lengths remain unmeasured.
- **Confidence:** MEDIUM — the "never run" fact is HIGH-confidence (config plus a complete `reports/`
  inventory), but the direction and size of the spread's dependence on minutes-since-open is
  mechanistic reasoning I could not measure from the anchored artifacts.
- **Invalidated by later commits?:** no — live HEAD equals the anchored SHA with a clean tree at
  2026-09-04.
- **Disclosed by authors?:** partially, and in a form that covers a positive rather than a negative.
  REGISTRATION.md:601-607 states "**A positive verdict** supports **exactly one** claim … **It is
  never evidence about any range length or entry rule other than the registered one.**" The symmetric
  statement for a *negative* — that the `cost-bound` closure is likewise not evidence about the other
  three lengths — is not stated there, and is not stated in the H1 closure rows of HYPOTHESES.md, in
  ORBExperiment/progress.md Entry 36, or in docs/HANDOVER.md's "there is no ladder any more".

---

### DRAFT-p3-progress-5
- **Repository / SHA:** ORBExperiment / f2aa675a80fc06b74979040b3028154d1add5ec0
- **Hypothesis or artifact:** H1's single registered reopen route, and the collector gating that makes it unreachable
- **Direction:** A
- **Class:** PROCESS
- **Severity:** S3
- **Label:** READ
- **Claim challenged (verbatim quote):** "**(d) Pursue Amendment 21 route (b)** — narrow the registered cost band on **real execution evidence**. **This repository holds none and has no broker credential.** It is the only route that could reopen a cost-bound closure, and **the measurement in hand points the other way by 11.27×.**" — ORBExperiment/docs/HANDOVER.md:272-275 *(primary evidence for the quoted claim lies outside my assignment; every supporting figure below is in mine)*
- **Evidence:**
  - The repository does hold a broker credential — a paper one, and it authenticates: "`200` on
    `paper-api/v2/account`, 960 B; `200` on `paper-api/v2/assets?status=inactive`, 8,112,164 B,
    **19,189 rows**" on the same key family, with the live host refusing at 401 —
    ORBExperiment/progress.md:1314, and "**These are paper-account keys**"
    ORBExperiment/progress.md:1339. Paper fills are simulated and are genuinely not "real execution
    evidence"; the stated blocker is nevertheless broader than the repository's own measurement.
  - The quantity that actually decided the closure is not execution evidence at all. It is the
    **quoted half spread**, which supplies 88 percent of the entry leg and 57.3 percent of the shift
    (DRAFT-1, DRAFT-4), and the vendor **serves it free**: "760 quote minutes served, 0 refused,
    `n = 759` requests", 0 dollars — ORBExperiment/progress.md:3575-3577, 3735.
  - That free quantity could accrue forever. The carve-out region was registered to grow: "the
    post-holdout region grows as real time advances" — ORBExperiment/progress.md:2211. The machinery
    that would accrue it is built, tested and inert: the production collector, the actions watcher and
    the systemd units were all delivered at A.3 and left unarmed because "A.3 is registered as armed
    *only on GO or DEGRADED*, and `PENDING_ACCESS` is neither" —
    ORBExperiment/progress.md:781-782; confirmed still inert at the closure,
    "`systemctl --user list-timers` shows **0 `orb-` units**" —
    ORBExperiment/progress.md:1979-1982.
  - The gate is now permanently unsatisfiable by the closure's own arithmetic: `GO` and `DEGRADED`
    both require the co-primaries at power, and "**joint power is 0.000000**"
    (ORBExperiment/docs/HANDOVER.md:149-151, echoing ORBExperiment/progress.md:3615). So the only
    condition that would arm the collectors is one the closure makes unreachable, and the only route
    named to reopen the closure is declared unavailable. **The closure is self-sealing.**
- **Recomputation (if any):** none — this is a reading of stated conditions against stated measurements.
- **What would resolve it:** either (a) record explicitly that additional post-holdout quoted-spread
  sessions are a second reopen route and that they cost 0 dollars and require no new credential, or
  (b) record why re-measuring the band on a larger post-holdout sample is *not* a route, given the
  registration says the region grows; and correct "has no broker credential" to name the paper
  credential the repository measured itself holding.
- **Confidence:** HIGH for the facts (all quoted with file and line); MEDIUM for the characterisation
  "self-sealing", which is an inference from the conjunction of the gate and the closure.
- **Invalidated by later commits?:** no — live HEAD equals the anchored SHA with a clean tree at
  2026-09-04.
- **Disclosed by authors?:** partially — HANDOVER.md:266-269 does record option "(b) Run the
  2026-09-12 re-pull anyway", but that is the bar-integrity measurement, which the same page says
  "**would measure bar integrity; it would not reopen H1**"
  (ORBExperiment/docs/HANDOVER.md:151). No document names further post-holdout spread measurement as
  a route.

---

### DRAFT-p3-progress-6
- **Repository / SHA:** ORBExperiment / f2aa675a80fc06b74979040b3028154d1add5ec0
- **Hypothesis or artifact:** the frozen Section 6 cost model — `Absent(sec_section_31_effective_date_not_measured)`
- **Direction:** A
- **Class:** OVER_CLOSED
- **Severity:** S3
- **Label:** DERIVED
- **Claim challenged (verbatim quote):** "**It was attempted again.** `sec.gov` returned **HTTP 403 "Request Rate Threshold
Exceeded"** on `n = 2` further attempts, **`n = 4` across two sessions**. The stored IBKR page carries
the rate and **no effective date anywhere**, so it is not recoverable offline either." — ORBExperiment/progress.md:2679-2683
- **Evidence:**
  - The consequence is not small: "**`REGISTERED_COST_MODEL` refused 550 of 550 trades.**" —
    ORBExperiment/progress.md:2674. The frozen, hashed, latched Section 6 model
    (sha256 `3789221b…`, ORBExperiment/progress.md:666) has **never priced a single trade** in this
    repository, and every downstream figure runs on a bracket instead
    (ORBExperiment/progress.md:2685-2698).
  - The refusal is a **rate** refusal, which is the exact class this repository built machinery for
    and cites a precedent for: solattn ADR-021, "**ceilings are per endpoint, never per host** —
    measured never assumed" (ORBExperiment/progress.md:370-372), a per-endpoint request ledger that
    "charges before sending" (ORBExperiment/progress.md:1803-1805), a measured 24.0 s pace on Massive
    after a 429 (ORBExperiment/progress.md:1791), and a two-phase escalation with a 75 s cooldown on
    Alpaca (ORBExperiment/progress.md:2594-2606).
  - **None of it was applied to sec.gov.** The repository records the omission itself without drawing
    the conclusion: "| `sec.gov` attempts, **uncharged** (unregistered vendor, no cap exists) |
    **2**, both `403` |" — ORBExperiment/progress.md:2910. Four unpaced requests across two sessions,
    two of them 20 seconds apart (ORBExperiment/progress.md:651-652), is the "documented beats
    measured" failure standing rule 4 exists to prevent, run against the repository's own blocker.
  - An alternative source exists and is named nowhere in the repository: SEC Section 31 fee rate
    changes are published as **dated SEC Fee Rate Advisories** and the fee-rate orders themselves are
    published in the **Federal Register** (federalregister.gov, a different host with a public
    documented JSON API), each carrying the rate **and** its effective date — which is precisely the
    field the repository declared unmeasurable. `grep -rn "federalregister\|Federal Register"` over
    the snapshot returns **0 hits**.
- **Recomputation (if any):** none required — the finding is that a blocker was declared final after
  n = 4 unpaced requests to one host while the repository's own pacing machinery and a second
  publisher of the same datum were untried.
- **What would resolve it:** register `sec.gov` (or `federalregister.gov`) as a vendor in
  `orb.vendors` with a measured pace and a daily cap, re-attempt under the ledger, and populate
  `sec_fee_schedule` with dated entries; then unfreeze the bracket and let the frozen model price the
  550 trades it currently refuses.
- **Confidence:** HIGH that the blocker was declared on four unpaced requests to a single host and
  that no alternative publisher is named anywhere in the repository; MEDIUM that a paced retry or the
  Federal Register would in fact serve the effective dates, which I did not attempt (the audit is
  read-only and sends no requests).
- **Invalidated by later commits?:** no — live HEAD equals the anchored SHA with a clean tree at
  2026-09-04.
- **Disclosed by authors?:** partially — the repository discloses loudly that the schedule is empty on
  purpose and that the model refuses rather than mis-price
  (ORBExperiment/progress.md:649-655), which is the correct behaviour. It does **not** disclose that
  the host was never paced or registered, and it states the datum is "not recoverable offline either"
  without naming a second publisher. **This finding does not affect the H1 closure**: the bracket
  spanning SEC rate 0 to 0.0000206 is 8.43 × 10⁻⁵ wide in relative terms
  (ORBExperiment/progress.md:2690-2698), so the missing date moves no deciding figure.

---

### DRAFT-p3-progress-7
- **Repository / SHA:** ORBExperiment / f2aa675a80fc06b74979040b3028154d1add5ec0
- **Hypothesis or artifact:** the choice of closure kind for H1 — `cost-bound` against the registered `untestable-at-achievable-power`
- **Direction:** A
- **Class:** OVER_CLOSED
- **Severity:** S3
- **Label:** READ
- **Claim challenged (verbatim quote):** "Register the consequence of NOT_RESCUED now, before the number exists: H1 closes as cost-bound, which is an existing closure kind in HYPOTHESES.md, and no further rescue lever is applied." — ORBExperiment/progress.md:3430
- **Evidence:**
  - Both kinds were on the table for the same underlying fact and only one was evaluated. At the
    prior pass the repository handed the operator "**Three routes handed over, none chosen: a narrower
    verdict scope with E2 demoted to a named secondary; a cost band narrowed on execution evidence
    this repository does not hold; or closure as `untestable-at-achievable-power`, the fourth closure
    kind already in the house record. None depends on 2026-09-12.**" —
    ORBExperiment/progress.md:3277-3280. The rescue prompt then collapsed the three into a two-valued
    criterion whose NOT_RESCUED branch names `cost-bound` only
    (ORBExperiment/progress.md:3426-3430). **No document records a comparison of the two kinds or a
    reason for preferring one.**
  - The house definitions distinguish them exactly on the point at issue: `cost-bound` = "The effect
    may be real; it does not survive the modeled cost"; `untestable-at-achievable-power` = "**The
    design's own arithmetic blocks it before any data exists**" —
    ORBExperiment/HYPOTHESES.md:36-40. What actually happened is the second by its own description:
    E2's verdict is a deterministic function of (assumed Sharpe, measured dispersion, measured shift)
    computed with **no bar of either registered window ever read**
    (`orb.power.e2_power_pessimistic`, ORBExperiment/src/orb/power.py:113-140; both latches absent,
    ORBExperiment/progress.md:3390-3391).
  - Route 1 — demote E2 to a named secondary and continue on E1 — was never revisited after
    ORBExperiment/progress.md:3277, and E1 was **powered** at the moment of closure:
    "| **REGISTERED 1.40** | **holdout** | **875** | 0.743521 | **0.832450** | +0.088929 | 1,006 |
    **795** |" — ORBExperiment/progress.md:3152, i.e. minimum 795 sessions against 875 reachable, on
    a holdout the repository measured as fully served at zero cost ("Alpaca … **1,762 / 1,762 —
    shortfall 0** … **875 / 875 — shortfall 0**", ORBExperiment/progress.md:1540).
  - The register's own rule for a closed entry — "A closed entry carries the figure that closed it,
    with its n, and states what would reopen it — or states that nothing would" —
    ORBExperiment/HYPOTHESES.md:7-9 — is not met by the H1 entry: no row of H1 states a reopen
    condition. The only reopen route in the repository lives in `docs/HANDOVER.md:272-275`, which is
    not the register.
- **Recomputation (if any):** none — this is a label and process finding. The arithmetic behind it is
  in DRAFT-2's table: the published band implies a break-even annual Sharpe of **16.191**, i.e. E2's
  outcome is fixed for every effect size any party to this registration has ever proposed, before any
  observation is read.
- **What would resolve it:** record in HYPOTHESES.md H1 either a reopen condition or the statement
  that nothing would reopen it, as the file's own rule requires; and record why `cost-bound` was
  preferred to `untestable-at-achievable-power` when the deciding quantity is a property of the
  inference design rather than of any read.
- **Confidence:** MEDIUM — the facts are certain and quoted; whether `cost-bound` is the wrong kind is
  a judgement, and the repository's own reasoning for it (a modeled cost, registered before any data,
  defeats an assumed edge) is defensible.
- **Invalidated by later commits?:** no — live HEAD equals the anchored SHA with a clean tree at
  2026-09-04.
- **Disclosed by authors?:** yes, in substance and generously — ORBExperiment/HYPOTHESES.md:63 states
  "**E1 remains powered at 0.832450** … **nothing in this repository measured whether the directional
  edge is real** … **It is a finding that this design cannot clear its own registered cost band.**
  That is a statement about the design." That disclosure is why this finding is READ and capped at
  S3. What is **not** disclosed is the absence of a registered reopen condition in the register
  entry, and the absence of any recorded comparison between the two candidate closure kinds.

---

## What I checked and found sound

The thesis did **not** hold on any of the following, and several of them are places where I expected
it to.

1. **The deciding number reproduces exactly.** `shift = (entry_p − entry_c) + s·(stop_p − stop_c) +
   (1 − s)·(close_p − close_c)` from the published band and stop share gives
   **0.46706520287790176**, byte-identical to `measured_shift_usd_per_share` in
   ORBExperiment/reports/stage_a3rescue/task2_slippage_band.json. So does the E2 power chain: at the
   carried band, `Φ((0.040386 − 0.041455)/2.029585 · √17188 − z(0.95)) = 0.043277`, matching
   ORBExperiment/progress.md:3251 to six decimals.
2. **The closure survives every correction I could construct at its own registered 1.40 assumption.**
   Six readings of the same measured data — as published; close leg dropped; entry capped at the
   registered limit; both; the registered 2× pessimistic multiple on the measured central figures;
   distribution means instead of percentiles — give pessimistic-cost means of −0.426679, −0.290061,
   −0.159053, −0.022435, −0.084162 and −0.073007. All negative. **`NOT_RESCUED` at 1.40 is robust.**
3. **The pre-commitment ordering is real and checkable.** `git log` on the live repository shows
   `4ae14dc "docs: A.-1 TASK 0 — the rescue-pass success criterion, pre-committed"` **before**
   `5899e1b "feat: A.3 TASK 2 — the slippage band measured…"`. The claim at
   ORBExperiment/progress.md:3526-3531 is exactly true.
4. **The statistic assignment was fixed before the measurement and was not selected afterwards.**
   median→central, p90→pessimistic appears in the tool's module docstring
   (ORBExperiment/tools/slippage_band.py:11-19), in ADR-038 (DECISIONS.md:1439-1445) and in
   `assignment_fixed_before_computation` in the report JSON. `inputs_not_adjusted` in
   task3_rescue_verdict.json lists five things that were held fixed, and I could find no artifact
   contradicting any of them.
5. **The one leg where the measurement went against the repository's interest is reported.** "stop,
   central | 0.0400 | **0.033529** | 0.84× | *overstated*" — ORBExperiment/progress.md:3587, and
   again in the JSON verdict field. A pass hunting for a favourable answer would not have kept it.
6. **The multiplicity correction (Berger 1982, intersection-union) is right, and it was applied in
   the direction that helps the hypothesis.** `1 − 0.95^(1/2)` is a Šidák correction for a union
   rule; Section 8's rule is a conjunction; each component may run at nominal α
   (ORBExperiment/progress.md:3129-3140). The repository found an error that had been costing it
   power since the first commit and fixed it against its own null, taking E1 from 0.743521 to
   0.832450.
7. **The E2 ≡ E1 discovery (Amendment 15) is correct and correctly acted on.** With session-clustered
   permutation, a session of k trades has mean kμ and dispersion σ√k, so the session ratio is
   √k·(μ/σ) and σ cancels (ORBExperiment/progress.md:2739-2746). E2 as originally registered was a
   rescale of E1 and constrained nothing. Replacing rather than repairing it was the right call.
8. **`GO` and `DEGRADED` were structurally unreachable and the code, not the prose, enforces it.**
   `test_neither_go_nor_degraded_is_reachable_while_an_input_is_absent`, and
   `tools/refire_section0*.py` exiting 78 if the map ever hands one over
   (ORBExperiment/progress.md:2079-2083, 2800-2804).
9. **The tape identification is a genuine measurement with a genuine control.** SAME_TAPE on
   Massive vs Alpaca-SIP at median 1.005197, n = 100, with Alpaca-SIP vs Alpaca-IEX — same vendor,
   same host, one parameter changed — separating at 0.0278 with 100/100 pairs below threshold
   (ORBExperiment/progress.md:1441-1443, 1475-1482). The shared-upstream limitation was registered
   *before* the agreement figure exists (ORBExperiment/progress.md:1504-1518).
10. **The reach shortfall was not worked around.** Massive was removed as primary on a measurement
    (0 of 1,762 in-sample sessions) rather than shrinking the registered windows to fit it —
    ORBExperiment/progress.md:1576-1585. This is the single most common Direction-A failure mode in
    this program and it does not occur here.
11. **The ambiguous-rate zero is bounded rather than asserted.** Rule of three: 3/560 ≈ 0.0054 —
    ORBExperiment/progress.md:3223-3224. The operator's 10 percent materiality threshold was
    evaluated and reported as not crossed, and the exclusion rule was left unchanged.
12. **The trigger-rate falsification (0.982143 against an assumed 0.55, n = 560) was recorded, not
    absorbed**, and Section 1 was restated to match it rather than the measurement being quietly
    accommodated (ORBExperiment/progress.md:2700-2722, 3284-3301).
13. **Section 0 was never re-scoped to fit a result.** `src/orb/section0.py` is recorded as
    byte-identical across the pass in which BLOCKED-1 would have fired on a different definition, and
    the observation is recorded and deliberately not acted on
    (ORBExperiment/progress.md:3323-3328). I checked the branch thresholds against the JSON verdicts
    in `stage_a1r/task10_section0.json`, `stage_a1amend/task6b_section0.json`,
    `stage_a2repair/task6_section0.json` and `stage_a3rescue/task5_section0.json` and found no
    threshold movement.
14. **The mutation harness caught its own stale mutation rather than hiding it.** Mutation 13 changed
    category when `orb.dispersion` added a second independent fixture on the same boundary instant,
    and the harness reported a failure that was "the harness being right"
    (ORBExperiment/progress.md:2853-2865, 2947-2952).
15. **The H1b floor scan does not overstate itself.** I checked whether its `central_mean_to_shift_ratio`
    column (0.9742 → 2.1424 across floors) used the falsified carried band, which it does — and the
    JSON says so in `comparison_figure_note` before a reader can be misled, and
    ORBExperiment/docs/HANDOVER.md:266-271 records that H1b "inherits the closure's problem". Under
    the measured band the same ratios run 0.086 → 0.183 and H1b fails at every floor; the repository
    does not claim otherwise.
16. **Storing is not reading.** The probe slice overlaps the holdout 2026-05-05 to 2026-06-30, and the
    argument that this is collection rather than a spent read is supported by the sealed writer
    storing raw bytes, the latch files being absent, and `orb.comparator.count_bars` being the only
    module that turns vendor bytes into anything (ORBExperiment/progress.md:1957-1970, 2838-2847).
    I checked `data/state/` is named as holding neither latch and found no contradicting artifact.
17. **Priors were not scored on an unresolved event.** The calibration ledger records both priors and
    records that neither is scored, because H1 closed before any out-of-sample read
    (ORBExperiment/progress.md:3667-3672). That is the conservative and correct treatment.
18. **Every figure I sampled travels with its n**, as standing rule 13 requires, including the ones
    that hurt: 550, 560, 340, 210, 229, 203, 100, 42, 28, 16.

**What I expected to find and did not.** I looked specifically for: a threshold moved after a number
was seen (none — Section 0's source is recorded byte-identical across the deciding pass); a band
narrowed to rescue a figure (none — `inputs_not_adjusted` holds, and the one leg that moved in the
repository's favour is reported as overstated); a statistic chosen after the fact (none — the
assignment is in the tool docstring, the ADR and the pre-commit); a window shrunk to fit a vendor
(none — Massive was dropped instead); a power figure presented as changed when it was not (the
verdict record carries `e1_unchanged_by_this_pass: true` as a field); and a stale external figure
carried into a verdict (the FINRA TAF was re-verified and found stale at 0.000166 against a measured
0.000195, and that was recorded as an amendment before the power gate, ORBExperiment/progress.md:640).

---

## Live-repo access log

**Before** (`git -C /home/kiros-li/Documents/GitHub/ORBExperiment status --porcelain`, 2026-09-04):

```
```
(empty — zero lines)

Read-only commands run against the live repository: `git status --porcelain`, `git log --oneline -12`,
`git rev-parse HEAD`. No file under the live repository was opened for writing; no untracked data
directory was read; no repository script was executed.

`git rev-parse HEAD` returned `f2aa675a80fc06b74979040b3028154d1add5ec0` — **identical to the anchored
SHA**, so no commit exists after the anchor and no finding above can be invalidated by a later commit
as of this reading.

**After** (`git -C /home/kiros-li/Documents/GitHub/ORBExperiment status --porcelain`, 2026-09-04):

```
```
(empty — zero lines)

No modification of any kind was made to the audited repository.
