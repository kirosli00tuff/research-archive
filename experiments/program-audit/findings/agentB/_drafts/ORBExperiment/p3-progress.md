# Agent B draft findings — ORBExperiment, part p3-progress

**Repository / SHA:** ORBExperiment / f2aa675a80fc06b74979040b3028154d1add5ec0 (live HEAD confirmed identical, 2026-09-12).
**Documents read completely:** `progress.md` (3,737 lines, all), every JSON/CSV/MD under `reports/` (33 JSON + 6 markdown/log), `tools/` (31 modules, the decision-bearing ones read in full). `src/orb/`, `REGISTRATION.md`, `DECISIONS.md`, `README.md`, `HYPOTHESES.md` and `tests/` were grepped and read where a claim pointed into them.
**Direction:** B — this program claimed more than it earned.

A note on the shape of this repository before the findings. It is unusually
self-critical: it records deviations, falsified planning figures, an ordering
breach in Entry 0a, a re-drawn sample, a mutation that stopped binding, and it
pre-committed the rescue criterion in a pushed commit (`4ae14dc`) before the
measurement that decided it — verified in the live `git log`. The findings below
are therefore mostly not about concealment. They are about **four places where a
number is carried further than its method supports**, and about **two shipped
artefacts whose framing exceeds their construction**.

---

### DRAFT-p3-progress-1
- **Repository / SHA:** ORBExperiment / f2aa675a80fc06b74979040b3028154d1add5ec0
- **Hypothesis or artifact:** H1 co-primary E1; the reported E1 power figures (0.832450 at the registered 1.40 assumption on n = 875) and Amendment 18's headline finding
- **Direction:** B
- **Class:** STATISTICAL
- **Severity:** S1
- **Label:** DERIVED
- **Claim challenged (verbatim quote):** "**E1 crosses its 80 percent bar at the registered assumption for the first time. The minimum session count falls from 1,006 to 795 against 875 achievable: a shortfall of 131 becomes a surplus of 80.**" — ORBExperiment/progress.md:3157-3159 (identical text at ORBExperiment/REGISTRATION.md:3088-3092; carried to README.md:49 as "**E1 remains powered at 0.832450**")
- **Evidence:**
  - The registered E1 decision rule is a **threshold on a statistic, not a p-value test**: "**Bar: deflated Sharpe at or above 1.00.**" — ORBExperiment/REGISTRATION.md:444. Implemented as `e1_passes=e1 >= CONFIG.deflated_sharpe_bar` where `e1 = annualize(sharpe(returns) - sr0_per_observation)` — ORBExperiment/src/orb/verdict.py:269 and :146-155; `deflated_sharpe_bar=1.00` at ORBExperiment/src/orb/config.py:258.
  - The reported power is computed by `power_one_sided`, whose null is **zero Sharpe**: "Power of the one-sided Sharpe test at ``alpha``. Under the alternative the t statistic is approximately normal with mean ``daily_sharpe * sqrt(n)`` and unit variance, so power is ``Phi(mean - z_{1-alpha})``" — ORBExperiment/src/orb/power.py:55-62. The function takes no bar and no deflation benchmark; `deflated_sharpe_bar` is read **nowhere** in `power.py` (grep across `src/` and `tools/` returns only `config.py:148,258` and `verdict.py:269`).
  - Consequently `alpha` — the quantity Amendment 18 corrected from 0.02532057 to 0.05 — **plays no part in E1's registered pass/fail at all**, yet the entire "inference repair" headline is an E1 power figure at the corrected alpha. Amendment 18 itself states "**It changes no bar, no threshold and no gate.** The deflated-Sharpe bar stays at **1.00**" (ORBExperiment/REGISTRATION.md:3068-3070) without noting that the bar, not the alpha, is what E1 must clear.
  - The deflation benchmark `sr0` scales with the **dispersion of Sharpes across the 8 registered trials**, a quantity `expected_max_sharpe` refuses to invent: "Where that dispersion has not been measured this returns a recorded absence rather than assuming one" — ORBExperiment/src/orb/power.py is not the site; it is ORBExperiment/src/orb/verdict.py:110-126. **That dispersion has never been measured in this repository**, so the effective E1 bar (1.00 + annualised SR0) is not merely 1.00 — it is 1.00 plus an unmeasured positive quantity.
  - Reported figures challenged: E1 @ 0.05, n = 875, S = 1.40 → **0.832450**; min n for 80 percent → **795** — ORBExperiment/reports/stage_a2repair/task1_alpha.json (rows, `e1_power_at_corrected_alpha_0_05`, `min_sessions_for_80_at_corrected`) and ORBExperiment/reports/stage_a3rescue/task5_section0.json (`e1_power_at_registered_1_40`: 0.8324500493878693, `e1_min_n_for_80_at_registered`: 795).
- **Recomputation (if any):**
  - Inputs: annual Sharpe 1.40 (`CONFIG.registered_sharpe_assumption`, ORBExperiment/src/orb/config.py:262); n = 875 holdout sessions (ORBExperiment/progress.md:613-621); bar 1.00 (ORBExperiment/src/orb/config.py:258); 252 trading days (`trading_days_per_year`).
  - Method: the E1 statistic is the annualised sample Sharpe net of `sr0`. Under iid returns SE(daily sample Sharpe) ≈ sqrt((1 + SR_d²/2)/n) (Lo 2002); annualised SE = that × √252. Power against the registered bar = 1 − Φ((bar + SR0 − S)/SE_annual). Script: /home/kiros-li/.cache/program-audit/scratchpad/work/agentB-ORB-p3/recompute.py.
  - Result, **most generous case, zero deflation (SR0 = 0)**: SE_annual = 0.537699; **E1 power = 0.771535** at n = 875 — **below the 0.80 floor**. **Minimum n for 80 percent power = 1,120**, against 875 achievable: the 131-session shortfall does not become a surplus of 80; it becomes a **shortfall of 245**.
  - With deflation: the Bailey–López de Prado expected-max multiplier at 8 trials is 1.459014, so SR0 = 1.459014 × (trial-Sharpe sd). At an annualised trial-Sharpe sd of 0.10 / 0.20 / 0.30 the effective bar is 1.1459 / 1.2918 / 1.4377 and E1 power falls to **0.6817 / 0.5797 / 0.4720**.
  - Reproduction of the repository's own figures, to show the recomputation is not a different arithmetic: `power_one_sided(1.40, 875, 0.05)` reproduces **0.832450** exactly, and all six rows of `task1_alpha.json` reproduce to 6 dp.
- **What would resolve it:** either (a) a power computation whose null is the registered E1 rule — P(annualised deflated Sharpe ≥ 1.00 | true annual Sharpe = S) — reported at all three assumptions with the trial-Sharpe dispersion measured or explicitly recorded `Absent`, or (b) an amendment stating that "E1 power" in every document means the power of a test of Sharpe > 0, that this is not the registered E1 rule, and that the Section 0 GO floor and Section 10 latch clause are therefore not evaluated on the registered test.
- **Confidence:** HIGH — the power module contains no reference to the bar or to SR0, and the two quantities differ by a factor large enough to move E1 across the 0.80 floor in the opposite direction.
- **Invalidated by later commits?:** no — f2aa675 is the live HEAD as of 2026-09-12 and the repository is closed on H1; any later commit would have to change `power.py` or `verdict.py`.
- **Disclosed by authors?:** no — greps for "null of zero", "Sharpe > 0", "against zero", "bar of 1.00" across all markdown and Python return nothing reconciling the two; Amendment 18 §3 asserts the bar is untouched but never states that the reported power is not the power of clearing it.

---

### DRAFT-p3-progress-2
- **Repository / SHA:** ORBExperiment / f2aa675a80fc06b74979040b3028154d1add5ec0
- **Hypothesis or artifact:** H1 co-primary E2 (amended, Amendment 19/21); the inference-repair pass's stated collapse
- **Direction:** B
- **Class:** STATISTICAL
- **Severity:** S1
- **Label:** DERIVED
- **Claim challenged (verbatim quote):** "**The measured pessimistic shift of 0.041455 USD/share EXCEEDS the implied central mean of 0.040386 at the registered 1.40 assumption.**" / "**The pessimistic-cost mean is −0.001068. It is NEGATIVE.**" — ORBExperiment/progress.md:3244-3245 (carried to README.md as "**E2 power is 0.043277, below the 0.05 size of the test, and JOINT power collapses with it. No session count reaches 80 percent.**")
- **Evidence:**
  - The "implied central mean" is not measured. It is derived as `implied_mean = dispersion * daily / math.sqrt(k)` — ORBExperiment/tools/dispersion_compute.py:194 — where `daily = annual_sharpe / sqrt(252)` and `k` is trades per session. `k = 550/28 = 19.642857` (550 triggered trades over 28 evaluable sessions, ORBExperiment/reports/stage_a2repair/task3_execution_mix.json and progress.md:3206-3211); dispersion = 2.029585 USD/share on n = 550 priced trades (progress.md:2698).
  - The `/sqrt(k)` step is exactly the assumption that **trades within a session are independent**: it takes session PnL variance to be k·σ². The registration denies that assumption in the same section that defines the power method: "**the trades inside a session are not independent, they share the session's market factor, and E2's permutation clusters on session date precisely because of that**" — ORBExperiment/REGISTRATION.md:534-536. E2's own test statistic is a **session-clustered** permutation (ORBExperiment/src/orb/verdict.py:166-180).
  - The deciding margin is 0.040386 − 0.041455 = **−0.001068 USD/share**, i.e. **2.6 percent of the central mean**. The repository itself records the fragility in the neighbouring sentence — "break-even Sharpe 1.437035, and the registered 1.40 sits 2.577 percent below it" (progress.md:3266-3267) — but treats both inputs as exact.
- **Recomputation (if any):**
  - Inputs as above, all with file:line given. Method: under equicorrelation ρ among a session's k trades, session dispersion is σ·sqrt(k(1+(k−1)ρ)), so the mean per trade implied by a given daily Sharpe is `implied_mean × sqrt(1+(k−1)ρ)`. Script as above.
  - Result: the repository's ρ = 0 gives 0.040386 (reproduced to 6 dp, confirming the identity). **ρ = 0.002876 — under three thousandths — makes the pessimistic-cost mean exactly zero.** At ρ = 0.01 the implied central mean is 0.043990 and the pessimistic-cost mean is **+0.002535**, i.e. positive, and E2 is no longer inside its own null. At ρ = 0.20 it is +0.046366.
  - **Stated against my own thesis, because it is true:** the *final* closure is robust to this. On the measured band (shift 0.467065) the correlation needed to flip the sign is ρ = 7.12, which is impossible; even at ρ = 1 the pessimistic-cost mean is −0.288. The finding therefore bears on the **inference-repair pass's stated conclusion** (Amendment 21, progress.md Entries 31–32, and the README's third re-fire block), not on the `cost-bound` closure.
- **What would resolve it:** report the implied central mean with the within-session correlation stated as an explicit registered assumption and a sensitivity band, or derive it from a session-level dispersion measured directly (the writer already reads sessions, so σ_session is computable inside the same sealed writer without a new blindness exception).
- **Confidence:** HIGH — the identity is one line of code and the registration's own sentence contradicts it; the sensitivity is arithmetic.
- **Invalidated by later commits?:** no — the anchored SHA is live HEAD, and Amendment 21's text is append-only.
- **Disclosed by authors?:** no — the repository discloses the *dispersion*'s regime caveat and the break-even margin, but nowhere states that the implied central mean assumes within-session independence, and Section 9 asserts the opposite.

---

### DRAFT-p3-progress-3
- **Repository / SHA:** ORBExperiment / f2aa675a80fc06b74979040b3028154d1add5ec0
- **Hypothesis or artifact:** the shipped "measured slippage band" (Amendment 26 / ADR-038), close-exit leg
- **Direction:** B
- **Class:** INTERNAL_INCONSISTENCY
- **Severity:** S2
- **Label:** DERIVED
- **Claim challenged (verbatim quote):** "| close, pessimistic | 0.0200 | **0.261000** | **13.05×** | **UNDERSTATED** |" — ORBExperiment/progress.md:3590 (identical rows at README.md:296 and REGISTRATION.md Amendment 26); and ADR-038's summary claim "**The overshoot distributions are therefore LOWER BOUNDS, the measured band is a lower bound, and any power computed on it is an UPPER bound on power.**" — ORBExperiment/DECISIONS.md (ADR-038 consequences block)
- **Evidence:**
  - The close-exit leg is computed as an **unsigned difference between two candidate exit prices**: `close_slippage.append(abs(row.official_close_c - row.last_exit_window_close_c) / CENT)` — ORBExperiment/src/orb/dispersion.py:943-945.
  - Those two prices are the close of the last bar inside the registered 15:55–15:59 exit window and the close of the first bar at or after 15:59 — ORBExperiment/src/orb/dispersion.py:388-394. So the quantity is **the absolute one-minute price change at the end of the session**, in dollars per share.
  - The source states the interpretation being challenged in its own comment: "A real market-on-close order fills at the official closing print, and the gap between them is the close leg's realized slippage" — ORBExperiment/src/orb/dispersion.py:385-386.
  - Three problems, each checkable: (i) the quantity is **unsigned**, so a favourable last-minute move is charged as a cost; if the difference is symmetric its expected signed cost is ≈ 0 while the median magnitude charged is 0.040 and the p90 charged is 0.261; (ii) it is a **difference between two modelling choices**, not an execution cost — the model's own exit price is the window close (`exit_price = close_exit_c(...)`, ORBExperiment/src/orb/dispersion.py:381), so nothing in the model pays this difference; (iii) unlike the entry and stop legs it contains **no spread component at all** (compare `entry_slippage.append(overshoot + half)` at ORBExperiment/src/orb/dispersion.py:902), so three legs presented in one "measured band" table are built from two different constructs.
  - Consequence for the deciding number: the close leg supplies **0.136618 of the 0.467065 shift = 29.3 percent**, and it is one of the two ratios the README's closure block names by name.
  - It also contradicts ADR-038's "the measured band is a lower bound": the overshoot components are bounded below, but an unsigned deviation charged as a cost is biased **upward**, so the band as a whole is not a lower bound.
- **Recomputation (if any):**
  - Inputs: measured band ends from ORBExperiment/reports/stage_a3rescue/task2_slippage_band.json (`measured_band`), stop share 0.3818181818 (same file).
  - Method: shift = (entry_p − entry_c) + s·(stop_p − stop_c) + (1−s)·(close_p − close_c).
  - Result: **0.467065203**, reproducing the reported `measured_shift_usd_per_share` exactly. Leg contributions: entry **0.267626 (57.3 %)**, stop **0.062821 (13.5 %)**, close **0.136618 (29.3 %)**.
  - **Stated against my thesis:** removing the close leg entirely leaves a shift of **0.330447**, still 8.2× the central mean of 0.040386, so `NOT_RESCUED` and the `cost-bound` closure survive. The finding is about the shipped band artefact and the "13.05×" figure, not about the closure's direction.
- **What would resolve it:** report the close leg signed (mean and distribution of `official_close − window_close` in the trade's own direction), or drop it and state that the registered close-exit slippage was not measured, with the reason.
- **Confidence:** HIGH — one line of code, and the two price definitions are read at named lines.
- **Invalidated by later commits?:** no — anchored SHA is live HEAD.
- **Disclosed by authors?:** no — ADR-038 discloses the one-minute *overshoot* resolution limit in detail and says nothing about the close leg's construction; the JSON's `one_minute_resolution_caveat` covers only the overshoot.

---

### DRAFT-p3-progress-4
- **Repository / SHA:** ORBExperiment / f2aa675a80fc06b74979040b3028154d1add5ec0
- **Hypothesis or artifact:** the H1 closure kind `cost-bound`; the measured entry slippage leg
- **Direction:** B
- **Class:** INTERNAL_INCONSISTENCY
- **Severity:** S2
- **Label:** DERIVED
- **Claim challenged (verbatim quote):** "| entry, pessimistic | 0.0400 | **0.354645** | **8.87×** | **UNDERSTATED** |" — ORBExperiment/progress.md:3586; and the closure it feeds, "**The registered rule cannot clear its own registered cost band.**" — ORBExperiment/README.md:28 (primary evidence for the band is in my documents; the closure sentence is README framing)
- **Evidence:**
  - The registered entry is a **limit order with a registered maximum price**: "Modeled as a **marketable limit at the range boundary plus 0.05 percent of price** (5 basis points), in the direction of the break" — ORBExperiment/REGISTRATION.md:302-303; `entry_offset_fraction=0.0005` at ORBExperiment/src/orb/config.py:245, with a one-cent floor exercised at ORBExperiment/tests/test_known_answers.py:320-323.
  - Section 6 draws the distinction itself, for the *stop* leg: "**The stop band is widest because a stop is marketable and gap-prone**; a stop is not a limit and does not get the limit's price." — ORBExperiment/REGISTRATION.md:394-395. The entry, by that same sentence, **does** get the limit's price.
  - The measured entry slippage applies **no limit cap**: `entry_slippage.append(overshoot + half)` — ORBExperiment/src/orb/dispersion.py:902 — where `half` is the time-weighted NBBO half spread (median 0.076572, p90 0.333662, n = 550 quote minutes served, 0 refused; ORBExperiment/reports/stage_a3rescue/task2_slippage_band.json → `per_leg_statistics.entry_half_spread`).
  - The registered universe's only price constraint is a **5.00 USD floor** (Section 2, ORBExperiment/REGISTRATION.md Section 2; also progress.md:137).
- **Recomputation (if any):**
  - Inputs: entry central 0.08701938620876422 and entry pessimistic 0.35464495116577943 (ORBExperiment/reports/stage_a3rescue/task2_slippage_band.json, `measured_band`); offset fraction 0.0005 (ORBExperiment/src/orb/config.py:245).
  - Method: the maximum price a marketable limit at boundary + 5 bp can pay above the boundary is 0.0005 × price (floored at one cent). Solve for the price at which that equals the modeled slippage.
  - Result: the **central** modeled entry fill requires a share price of **≥ 174.04 USD** before the registered order could legally pay it; the **pessimistic** end requires **≥ 709.29 USD**. Below those prices the registered order does not fill worse — **it does not fill**. The registered universe floor is 5.00 USD.
  - Consequence for the closure *kind*: the honest reading of a half spread wider than the registered limit offset is a **fill-rate** finding (which fraction of registered entries never execute), not a cost. The repository holds no fill model, and its own named precedent for `cost-bound` is "MLCryptoEngine H6 — per-fill positive, negative under an **order-lifecycle fill model**" (ORBExperiment/HYPOTHESES.md, closure-kinds table).
- **What would resolve it:** either apply the registered limit cap to the entry leg and report the resulting **non-fill rate** with its n, or amend Section 3 to a market order and record what that changes; either way state which of `cost-bound` and `untestable-at-achievable-power` the measurement supports.
- **Confidence:** MEDIUM — the arithmetic and the two registered clauses are certain; what is uncertain is the price distribution of the traded names, which the repository does not record (it is a sealed field), so I state the required price rather than assert the share of trades affected.
- **Invalidated by later commits?:** no — anchored SHA is live HEAD.
- **Disclosed by authors?:** no — ADR-038 lists four rejected alternatives and none is the limit cap; no grep for "limit's price", "fill", "unfilled" outside Section 6's stop sentence returns a treatment of this.

---

### DRAFT-p3-progress-5
- **Repository / SHA:** ORBExperiment / f2aa675a80fc06b74979040b3028154d1add5ec0
- **Hypothesis or artifact:** H1b (open, `REGISTERED_NOT_OPEN`); the shipped price-floor feasibility table handed to the operator
- **Direction:** B
- **Class:** UNSUPPORTED_POSITIVE
- **Severity:** S2
- **Label:** DERIVED
- **Claim challenged (verbatim quote):** "**Both halves of the registered mechanism are confirmed and they run in opposite directions.** The ratio **rises monotonically** while the shift stays inside a **4 percent band** — the price-invariance H1b asserted before the scan." — ORBExperiment/progress.md:3642-3645 (mirrored at REGISTRATION.md:3885-3889 and README.md:331-333)
- **Evidence:**
  - The "shift" column of the scan is **not measured**. It is the registered Section 6 constant band re-weighted by each floor's stop share: `shift = 0.020 + s·0.040 + (1−s)·0.010 = 0.03 + 0.03s`. The JSON says so in its own note — "The shift here is the **registered Section 6 band shift** at each floor's own measured stop-exit share" — ORBExperiment/reports/stage_a3rescue/task4_floor_scan.json (`comparison_figure_note`).
  - So the per-share band is **price-invariant by construction**: the registered constants do not depend on price. "The shift stays inside a 4 percent band … the price-invariance H1b asserted before the scan" restates an input as a result.
  - The one measured quantity offered as the independent check on invariance is `entry_overshoot_median_usd_per_share`, and it is **0.0 at every one of the five floors** (ORBExperiment/reports/stage_a3rescue/task4_floor_scan.json, all rows) — degenerate, because 457 of 550 entry crosses are intrabar and recorded as 0.0 (progress.md:3604-3607).
  - The same pass had already measured, one task earlier, that per-share entry slippage is **not** price-invariant in the relevant sense: the measured entry half spread is 0.076572 median / 0.333662 p90 (ORBExperiment/reports/stage_a3rescue/task2_slippage_band.json), and that measurement was **not re-run per floor** — the only measurement that could have tested the invariance claim.
  - The "ratio rises monotonically" half is likewise mechanical: `central_mean = dispersion × daily_sharpe / sqrt(k)`, so `central ÷ shift` is per-share dispersion divided by a near-constant. Per-share dollar dispersion rising with a price floor is arithmetic, not evidence about edge.
- **Recomputation (if any):**
  - Inputs: all five rows of ORBExperiment/reports/stage_a3rescue/task4_floor_scan.json; the identity at ORBExperiment/tools/dispersion_compute.py:194.
  - Result table (floor | dispersion | central | shift | ratio | implied stop share | central÷dispersion):
    5 | 2.029585 | 0.040386 | 0.041455 | 0.9742 | 0.381818 | 0.01989873
    10 | 2.096180 | 0.041711 | 0.041782 | 0.9983 | 0.392727 | 0.01989873
    20 | 2.382112 | 0.047358 | 0.041488 | 1.1415 | 0.382940 | 0.01988067
    50 | 2.709331 | 0.060344 | 0.040866 | 1.4767 | 0.362187 | 0.02227278
    100 | 3.199162 | 0.085626 | 0.039967 | 2.1424 | 0.332237 | 0.02676517
  - Every shift row satisfies `0.03 + 0.03s` to 9 dp, confirming that the column moves **only** through the stop share. `central ÷ dispersion` is constant at 0.0198987 across floors 5–20, confirming that the ratio column is dispersion up to a constant.
  - Secondary: the stated "4 percent band" is **4.54 percent** (0.039967 to 0.041782) — REGISTRATION.md:3887 quotes both endpoints, so the arithmetic is checkable from the repository's own text.
- **What would resolve it:** re-run `measure_carve_out_slippage_band` at each floor and report the measured per-leg band per floor beside the ratio; until then, label the invariance half of the mechanism **unmeasured** rather than confirmed.
- **Confidence:** HIGH — the identity reproduces every row of the shipped table to 9 dp.
- **Invalidated by later commits?:** no — anchored SHA is live HEAD and H1b is not opened.
- **Disclosed by authors?:** partially — the JSON note names the shift as the registered band, and one column (`filling 20`) is explicitly labelled a sample artefact (progress.md:3648-3651); the prose conclusion "both halves of the registered mechanism are confirmed" is not qualified anywhere.

---

### DRAFT-p3-progress-6
- **Repository / SHA:** ORBExperiment / f2aa675a80fc06b74979040b3028154d1add5ec0
- **Hypothesis or artifact:** the delisted-name coverage verdict `PASS` (A.1 TASK 6), a Section 0 BLOCKED-5 input
- **Direction:** B
- **Class:** UNSUPPORTED_POSITIVE
- **Severity:** S2
- **Label:** DERIVED
- **Claim challenged (verbatim quote):** "**`PASS`** — **203 delisted names with intraday history, measured** … The registered bar is **100 or more for `PASS`**, 20 to 99 for `PARTIAL`, below 20 for `FAIL` firing BLOCKED. **203 clears it by measurement, not by extrapolation.**" — ORBExperiment/progress.md:1648-1653
- **Evidence:**
  - The registered bar is a **count of names the analyst chooses to check**, and the analyst controls the sample size. The repository chose to enlarge the sample after the first in-window draw fell short: "inside the registered window | **89** | **81** | **0.910**" — ORBExperiment/progress.md:1688. **81 is below the 100 PASS bar**; on that sample the verdict is `PARTIAL`.
  - The enlargement is recorded: "**So the sample was re-drawn inside the window and enlarged** … **`n = 140` supplementary names**, combined with the 89 in-window names from the first pass: **`n = 229` checked, `203` served.**" — ORBExperiment/progress.md:1696-1699.
  - The repository explicitly refuses the alternative that would make the bar sample-size-independent: "**a rate measured on 20 names and multiplied by 4,731 is a synthesized value** — standing rule 5 forbids one" — ORBExperiment/progress.md:1701-1703. That refusal is defensible; its consequence — that the verdict is then a function of how many names were checked — is not recorded.
  - The population is 4,731 in-window delisted names (ORBExperiment/progress.md:1657-1659; ORBExperiment/reports/stage_a1r/task6b_delisted_in_window.json), of which **229 (4.84 percent)** were checked.
- **Recomputation (if any):**
  - Inputs: 89 checked / 81 served and 229 checked / 203 served (ORBExperiment/progress.md:1686-1699); bar = 100 (Section 0, registered 2026-08-28 at A.0 TASK 4, progress.md:127-129).
  - Result: served share 0.9101 on the first in-window draw and 0.8865 on the combined draw. At the realised share, the **number of names that must be checked to reach the count bar is 113**. The verdict is therefore determined by the stopping rule of the sampling, not by the vendor's coverage: checking 89 gives PARTIAL, checking 113 gives PASS, checking 229 gives PASS with a larger number. The bar is a count and the sample size is discretionary.
- **What would resolve it:** state the sample size beside the count in every place the PASS is reported, and record either (a) the exact binomial lower bound on the *population* count implied by 203/229 of 4,731, or (b) an amendment converting the registered bar to a share with its own threshold. Both are computable from figures the repository already holds.
- **Confidence:** MEDIUM-HIGH — the arithmetic is certain; what is arguable is whether the registered wording ("at least 100 delisted names served with intraday history") was meant as a population count or a sample count, and the repository chose the reading under which it controls the answer.
- **Invalidated by later commits?:** no — anchored SHA is live HEAD; the verdict is frozen in `reports/stage_a1r/task6b_section0.json`.
- **Disclosed by authors?:** partially — the re-draw and the enlargement are recorded in full at progress.md:1667-1705, with the honest reason (a silently-ignored vendor filter); what is not recorded anywhere is that the threshold is one the sample size can reach at will, or that the first in-window sample stood below it.

---

### DRAFT-p3-progress-7
- **Repository / SHA:** ORBExperiment / f2aa675a80fc06b74979040b3028154d1add5ec0
- **Hypothesis or artifact:** the shipped reach figures "1,762 of 1,762 in-sample / 875 of 875 holdout"; a Section 0 `SERVING_FULL_REACH` input
- **Direction:** B
- **Class:** PROVENANCE
- **Severity:** S2
- **Label:** DERIVED
- **Claim challenged (verbatim quote):** "| **Alpaca** | **2016-01-04** | **16** | **1,762 / 1,762 — shortfall 0** | **875 / 875 — shortfall 0** |" — ORBExperiment/progress.md:1540; the same figures are re-stated as a Section 0 input at progress.md:2015 and in ORBExperiment/reports/stage_a1r/task10_section0.json, and framed in README.md:63-65 as "The primary reaches **every registered session**".
- **Evidence:**
  - The bisection was run on **one ticker**: `"ticker": "AAPL"` — ORBExperiment/reports/stage_a1r/task5_reach.json (top-level key), with `probes: 16` per credential and `candidate_session_count: 5934`.
  - The per-window counts are **calendar arithmetic from a single boundary date**, not per-session measurements: the JSON reports `sessions_served: 2657` for Alpaca, which is the count of calendar sessions from the earliest served date to today, and the 1,762 / 875 split comes from `orb.calendar`. Three sessions were verified directly (`2015-12-31` false, `2016-01-04` true, `2016-01-05` true).
  - The repository's own later measurements contradict the coverage reading of the figure: **203 of 229** in-window delisted names served intraday bars, share **0.8865** (progress.md:1650-1652), and **199 of 200** sampled tickers served at least one bar on the post-holdout pull (progress.md:2669-2670). Per-name coverage is measurably not 1.0.
  - AAPL is the single name least likely to expose a gap: continuously listed mega-cap. The registered universe is news-driven single names **including delisted tickers for every session in which they traded** (REGISTRATION.md Section 2).
- **Recomputation (if any):** none required beyond reading the artefact: the JSON carries the ticker, the probe count and the three verification rows, and carries no per-session coverage measurement of any kind.
- **What would resolve it:** rename the figure (the progress table's own header says "**reachable**", which is correct; the Section 0 input field and the README's "reaches every registered session" are not), or measure served-session coverage on a price-blind sample of the registered universe across both windows and report it with its n.
- **Confidence:** HIGH — the artefact names its own single ticker.
- **Invalidated by later commits?:** no — anchored SHA is live HEAD.
- **Disclosed by authors?:** partially — progress.md uses the word "reachable" and records the zero-margin coincidence honestly ("**The in-sample window is covered with zero margin** … **This is not a comfortable pass. It is an exact one**", progress.md:1553-1558); it does not record that the bisection used one ticker, and the README's framing drops "reachable" for "reaches every registered session".

---

### DRAFT-p3-progress-8
- **Repository / SHA:** ORBExperiment / f2aa675a80fc06b74979040b3028154d1add5ec0
- **Hypothesis or artifact:** the deciding post-holdout measurements (dispersion, trigger rate, stop share, slippage band) and the universe they were measured on
- **Direction:** B
- **Class:** STATISTICAL
- **Severity:** S2
- **Label:** DERIVED
- **Claim challenged (verbatim quote):** "**The carried band came from QQQ, an ETF with a ~1-cent spread**; the registered universe selects **news-driven single names by elevated opening relative volume** — the population whose spreads are widest at exactly the moment the rule trades them." — ORBExperiment/README.md:38-41 (the explanatory claim); the measurement it explains is "the slippage band, measured on the instruments actually traded" — ORBExperiment/tools/slippage_band.py:1 and ORBExperiment/src/orb/dispersion.py:816-821
- **Evidence:**
  - Every deciding post-holdout figure was measured on a **1-in-26 systematic subsample**, not on the registered universe: "the reference listing walked in full by cursor, **`n = 5,317` active US common stocks over 6 pages**, **every 26th ticker** taken, **`n = 200`, A to WSM**, of which **199 served at least one bar**" — ORBExperiment/progress.md:2666-2670.
  - The slippage band reads its ticker list from that same pull (`MANIFEST = REPORTS / "task5b_post_holdout_pull.json"`, ORBExperiment/tools/slippage_band.py:56-79; `tickers_with_bars: 199` in ORBExperiment/reports/stage_a3rescue/task2_slippage_band.json).
  - The registered Section 2 selection is the **top 20 by opening relative volume out of the eligible universe**. Applied to 200 names it is a **top-decile** selection; applied to the registered ~5,317 it is a **top-0.38-percent** selection. The measured extremity is recorded: `mean_relative_volume_of_selection: 2.0651704796524437` at the 5 USD floor — ORBExperiment/reports/stage_a3rescue/task4_floor_scan.json.
  - So the population whose spreads were measured is **not** the population the README's explanatory sentence describes, and the repository knows the subsample matters: it labels exactly one column of one table with the caveat — "**A floor that fails to fill 20 names in a 1-in-26 subsample says nothing about a universe 26.6 times larger**" (progress.md:3648-3651) — and attaches it nowhere else.
  - The direction of the bias is unmeasured: a genuinely top-0.38-percent relative-volume selection could have wider spreads (supporting the closure) or narrower (higher absolute volume). The repository asserts the first in prose and measures neither.
- **Recomputation (if any):** none beyond the ratio 5,317 / 200 = 26.6 and the recorded mean relative volume of 2.0652, both read from the artefacts named above.
- **What would resolve it:** state the subsample and its selection extremity beside every figure derived from it — dispersion 2.029585, trigger rate 0.982143, stop share 0.381818, and all six band ends — on the same terms standing rule 13 attaches an n; or re-run the selection against the full reference listing.
- **Confidence:** HIGH — the sampling stride is recorded by the repository and the mean relative volume of the selection is in a shipped artefact.
- **Invalidated by later commits?:** no — anchored SHA is live HEAD.
- **Disclosed by authors?:** partially — the stride and the 200/5,317 figures are recorded at progress.md:2666-2670 and in the manifest; the caveat is attached to one floor-scan column only, and to none of the four deciding figures.

---

### DRAFT-p3-progress-9
- **Repository / SHA:** ORBExperiment / f2aa675a80fc06b74979040b3028154d1add5ec0
- **Hypothesis or artifact:** Section 1 restatement (§1.1, Amendment 22) and the §11.2 epistemic consequence
- **Direction:** B
- **Class:** OVER_CLOSED
- **Severity:** S3
- **Label:** READ
- **Claim challenged (verbatim quote):** "At a measured **0.982143** trigger rate, `n = 560`, over roughly **385 minutes** after a five-minute range, **the condition selects on almost nothing.**" — ORBExperiment/progress.md:3286-3287, followed by the registered restatement of Section 1 at progress.md:3289-3291
- **Evidence:**
  - The same repository states the opposite constraint on the figure four hundred lines earlier, in the entry that measured it: "**Stated narrowly so it is not over-read:** this is the realized share of registered top-20 selections producing a registered entry, on **28 post-holdout sessions**, over a **200-name sample of 5,317**, in a **post-holdout regime**. **It is not the in-sample trigger rate.**" — ORBExperiment/progress.md:2714-2717.
  - The restatement it was then used for is unconditioned on window: Section 1 governs the whole registered claim, 2016-01-04 to 2026-06-30, and §11.2 registers the consequence for "a later `PASS`" — i.e. for the holdout read (progress.md:3293-3295).
  - n for the restatement is 560 name-sessions = 28 sessions × 20 names, on 28 of 42 pulled post-holdout sessions (progress.md:3206-3211).
- **Recomputation (if any):** none — this is a scope question, not an arithmetic one.
- **What would resolve it:** attach the same "not the in-sample trigger rate" sentence to §1.1 and §11.2, or measure the trigger rate inside the in-sample window (which the Stage C latch governs and which has not been opened).
- **Confidence:** HIGH — both sentences are in the same file and are directly contradictory in scope.
- **Invalidated by later commits?:** no — anchored SHA is live HEAD; §1.1 and §11.2 are append-only.
- **Disclosed by authors?:** yes, in one place (ORBExperiment/progress.md:2714-2717) and not in the amendment that acts on it. Per the common rules this makes the finding READ and capped at S3.

---

### DRAFT-p3-progress-10
- **Repository / SHA:** ORBExperiment / f2aa675a80fc06b74979040b3028154d1add5ec0
- **Hypothesis or artifact:** the shipped verdict machinery `orb.verdict.fire_verdict` — the function Stage C/D would call
- **Direction:** B
- **Class:** INTERNAL_INCONSISTENCY
- **Severity:** S3
- **Label:** DERIVED
- **Claim challenged (verbatim quote):** "**SUPERSEDED by Amendment 18 as the per-co-primary level.** … **It is the right correction for a union rule and the wrong one for Section 8's conjunction.** Use :func:`per_test_alpha` for the co-primaries." — ORBExperiment/src/orb/verdict.py:40-46
- **Evidence:**
  - Two lines below its own instruction, the registered verdict function still uses the superseded level for E2: `e2_passes=p_value < alpha_adj()` — ORBExperiment/src/orb/verdict.py:270. `per_test_alpha()` is read only by tools (`tools/rescue_verdict.py:57`, `tools/joint_power.py:74`, `tools/refire_section0_rescue.py:54`) and by `tests/test_verdict.py`; grep across `src/orb` shows no call site in the verdict path.
  - `fire_verdict` also still implements the **superseded E2 null**. Amendment 19 replaced "mean net PnL per trade above zero at central costs" with "mean net PnL per trade above zero **at the pessimistic end of the Section 6 band**" (progress.md:3183-3186). `fire_verdict` calls `permutation_lower_bound`, which tests the observed mean against zero (ORBExperiment/src/orb/verdict.py:166-197) and takes no shift parameter; nothing in `verdict.py` references `e2_pessimistic_mean` or a slippage shift.
  - So the two amendments that produced the inference-repair pass's headline figures are registered in prose and wired into the *reporting* tools, and are not wired into the artefact that would fire the verdict.
- **Recomputation (if any):** none — this is a code read; the grep output is reproducible with `grep -rn "per_test_alpha\|alpha_adj" src/orb`.
- **What would resolve it:** either wire `per_test_alpha()` and the pessimistic-cost null into `fire_verdict`, or record an amendment stating that `verdict.py` is deliberately frozen at its pre-Amendment-18 form because H1 is closed and Stage C will not open, so a later reader does not take the module as the registered inference.
- **Confidence:** HIGH — two named lines in one file.
- **Invalidated by later commits?:** no — anchored SHA is live HEAD.
- **Disclosed by authors?:** no — Amendment 18 §2 says `alpha_adj` "is not removed and not made wrong" but does not say the verdict function still uses it; no ADR records `verdict.py` as frozen.

---

### DRAFT-p3-progress-11
- **Repository / SHA:** ORBExperiment / f2aa675a80fc06b74979040b3028154d1add5ec0
- **Hypothesis or artifact:** Guard 2 (parse-tree config enforcement) and the registered constants it exempts — including the Section 6 slippage band, the DSR trial count of 8 and the per-trade t gate of 2.50
- **Direction:** B
- **Class:** PROCESS
- **Severity:** S3
- **Label:** DERIVED
- **Claim challenged (verbatim quote):** "Config fields not yet read outside ``config.py``, each with its task named. **A field sits here only while the task that will read it is still ahead.** The guard below fails if a field is neither read nor listed, and fails again if a listed field has since been read — a stale entry hides the next real gap." — ORBExperiment/tests/test_guards.py:252-257 (docstring of `PENDING_ENFORCEMENT`, declared at :234)
- **Evidence:**
  - At the anchored SHA — after A.0 through A.5, the A.1 resumption, the amendment pass, the inference-repair pass and the rescue pass have all **closed** — the exemption list still carries 14 fields, every one naming a task that has completed (ORBExperiment/tests/test_guards.py:234-249):
    `in_sample_end`, `holdout_start` → "A.2 TASK 1 — session calendar" (closed 2026-08-28, progress.md Entry 4);
    `commission_per_share_usd`, `commission_order_minimum_usd`, `finra_taf_per_share_sold_usd`, **`entry_slippage_usd`, `stop_slippage_usd`, `close_slippage_usd`** → "A.2 TASK 2 — cost model" (closed, model frozen and hashed, progress.md:666-668);
    **`trial_count`**, `quartered_sharpe_assumption` → "A.2 TASK 4 — power gate" (closed, progress.md Entry 5);
    **`holdout_per_trade_t_gate`** → "A.2 TASK 3 — verdict built dark" (closed, progress.md Entry 4);
    `probe_sessions`, `probe_tickers`, `probe_min_age_days` → "A.1 TASK 3" (the probe slice was pulled at A.1 TASK 9, progress.md Entry 17).
  - The guard cannot detect this, because it only fails when a listed field **has since been read**; it has no completed-task check. So the escape hatch is permanent by construction, and the stated purpose — "A registered constant nobody reads is an unimplemented intention" (ORBExperiment/tests/test_guards.py:273) — is not enforced for these 14.
  - Three of the exemptions are consequential:
    1. **`holdout_per_trade_t_gate = 2.50`** (ORBExperiment/src/orb/config.py:151-152, 259). The registration states "**The holdout gate is therefore set at a per-trade t of 2.50**" — ORBExperiment/REGISTRATION.md:509. No module reads it; `fire_verdict` applies E1, E2, concentration and persistence and no t gate (ORBExperiment/src/orb/verdict.py:267-275). **A registered gate that exists nowhere in the decision path.**
    2. **`trial_count = 8`** (ORBExperiment/src/orb/config.py:257). Section 8 registers the DSR deflation "with the trial count registered at 8" (REGISTRATION.md:436-440); Amendment 25 pays a multiplicity cost by incrementing it to 9 for H1b. Nothing passes it to `expected_max_sharpe(n_trials, ...)` (ORBExperiment/src/orb/verdict.py:110).
    3. **The three slippage triples** are duplicated as literals in the frozen model — `entry_slippage=(0.010, 0.020, 0.040)` etc. at ORBExperiment/src/orb/costs_registered.py:52-54 — rather than read from `CONFIG`. The values agree today. Amendment 26's reassurance that "The registered band was NOT moved. `CONFIG`'s slippage tuples are unchanged" (progress.md:3609-3610) is therefore a statement about fields the cost model does not consume.
- **Recomputation (if any):** none — reproducible with `grep -rn "entry_slippage\|trial_count\|holdout_per_trade_t_gate" src tools`, which returns only the declarations in `config.py` plus the duplicated literals in `costs_registered.py`.
- **What would resolve it:** add a completion check to Guard 2 (a listed field whose named task has closed is a failure), and either implement or formally withdraw the t = 2.50 gate and the `trial_count` wiring.
- **Confidence:** HIGH — the list and the greps are exact.
- **Invalidated by later commits?:** no — anchored SHA is live HEAD.
- **Disclosed by authors?:** no — the guard's docstring asserts the opposite of the state it is in, and no ADR or amendment records that the t = 2.50 gate is unimplemented.

---

### DRAFT-p3-progress-12
- **Repository / SHA:** ORBExperiment / f2aa675a80fc06b74979040b3028154d1add5ec0
- **Hypothesis or artifact:** the mutation harness — the shipped "n = 17 mutations, 0 harness failures" claim and its mutation 4
- **Direction:** B
- **Class:** PROCESS
- **Severity:** S3
- **Label:** DERIVED
- **Claim challenged (verbatim quote):** "| 4 | move a boundary fixture off the registered 09:35:00.000 boundary | a fixture inside its boundary lets a moved threshold pass unnoticed | GUARD STOPPED BINDING | yes | |" — ORBExperiment/reports/stage_a3rescue/mutations.md (row 4; identical rows in `reports/stage_a1amend/mutations.md`, `reports/stage_a1r/mutations.md`, `reports/stage_a4/mutations.md`)
- **Evidence:**
  - The registered mutation, from the operator prompt logged verbatim in my primary document: "Move a boundary fixture off the registered 09:35:00.000 Eastern boundary and confirm the test stops binding." — ORBExperiment/progress.md:260.
  - Mutation 4 as implemented touches **no 09:35 boundary**. Its nine edits move `ONE_MS_BEFORE` by a day, disable five `tests/test_preperiod.py` tests by renaming them, disable `tests/test_dark.py::test_a_pre_period_bar_must_actually_be_pre_period`, blank an assertion in `tests/test_known_answers.py`, and shift `src/orb/preperiod.py`'s comparison by 86,400,000 ms — i.e. it moves the **2016-01-04T14:30:00.000Z carve-out boundary** (ORBExperiment/tools/mutate.py:92-146). Grep for "09:35" across `tools/mutate.py` returns **only the label on line 94**.
  - Its `expect_green=True` (ORBExperiment/tools/mutate.py:145) means the harness scores it a success when the suite stays green — but the mutation **disables the eight assertions that would catch it** as part of itself. "GUARD STOPPED BINDING — detected: yes" therefore records that deleting the tests stops the tests firing. Mutation 1 has the same shape: it inserts `violations = []` into the guard test before planting the leak (ORBExperiment/tools/mutate.py:48-66).
  - The harness's treatment of the same situation is inconsistent in the direction that preserves a green result. When a second, independent pin appeared on mutation 13's boundary, the repository correctly re-marked it `expect_green=False` and recorded "the failure was the harness being right" (progress.md:2860-2865). When a second pin appeared on mutation 4's boundary, the mutation was **extended to disable that pin too**: "mutation 4's, which needed the new sealed-window sweep disabled to keep going green" — ORBExperiment/progress.md:2366-2367 (the corresponding edit is `_disabled_sealed_window_sweep` at ORBExperiment/tools/mutate.py:124-129).
  - Separately, ORBExperiment/progress.md:834-841 describes mutation 4 as being about the carve-out and as **caught** — "Disabling the four `test_preperiod.py` boundary fixtures and shifting the carve-out boundary by a day **did not** make the suite green" — while `reports/stage_a4/mutations.md` from the same run records it as `GUARD STOPPED BINDING`. Both cannot describe the same mutation's outcome.
- **Recomputation (if any):** none — the mutation's edit list, its `expect_green` flag and the harness's scoring rule (`caught = (not suite_green) if not mutation.expect_green else suite_green`, ORBExperiment/tools/mutate.py:408) are read directly.
- **What would resolve it:** implement the registered 09:35:00.000 mutation (a fixture on the opening-range end boundary exists and is exercised — progress.md:688-691); re-mark mutation 4 `expect_green=False` now that the boundary is pinned in three places, as was done for mutation 13; and reconcile progress.md Entry 6 with `reports/stage_a4/mutations.md`.
- **Confidence:** HIGH — the mutation's own source lists every edit and the label does not match them.
- **Invalidated by later commits?:** no — anchored SHA is live HEAD.
- **Disclosed by authors?:** partially — the harness openly marks two mutations as "of a different kind … the point is to show a guard **failing to catch** something" (reports/stage_a3rescue/mutations.md, preamble), and Entry 21 records the extension of mutation 4 in one clause. What is not disclosed is that mutation 4 does not perform the registered mutation, and that its green result is produced by disabling its own detectors.

---

### DRAFT-p3-progress-13
- **Repository / SHA:** ORBExperiment / f2aa675a80fc06b74979040b3028154d1add5ec0
- **Hypothesis or artifact:** the Amendment 11 regime caveat and its scope; the H1 `cost-bound` closure
- **Direction:** B
- **Class:** INTERNAL_INCONSISTENCY
- **Severity:** S3
- **Label:** DERIVED
- **Claim challenged (verbatim quote):** "Amendment 11: the **dispersion input** comes from a POST-HOLDOUT regime (2026-07-01 to 2026-08-28), later than the sample it is applied to, and may misstate in-sample dispersion in either direction by an amount this repository has not measured and does not claim to bound." — ORBExperiment/reports/stage_a3rescue/task5_section0.json (`inputs.carve_out_caveat`); the amendment's own instruction was "**Attach the TASK 1 caveat to every E2 figure produced**" — ORBExperiment/progress.md:2259
- **Evidence:**
  - By the rescue pass the figure that decides E2 is no longer the dispersion. It is the **measured slippage band**, and that was measured on **the same post-holdout window**: `"first_session": "2026-07-01"`, `"last_closed_session": "2026-08-28"`, `sessions_used: 28` — ORBExperiment/reports/stage_a3rescue/task2_slippage_band.json.
  - The caveat carried into the final verdict record names only the dispersion input. The band carries a different caveat — the one-minute resolution limit — and **no regime caveat at all** (same file, `one_minute_resolution_caveat`). ADR-038's consequences block lists the resolution limit and four rejected alternatives and does not mention the regime (ORBExperiment/DECISIONS.md, ADR-038).
  - The registered window the band is applied to is 2016-01-04 to 2026-06-30. A July–August 2026 quoted-spread distribution applied to a decade of sessions is precisely the extrapolation Amendment 11 said it "does not claim to bound", and the closure's headline sentence carries no such qualification (ORBExperiment/progress.md:3613-3615; README.md:28).
- **Recomputation (if any):** none — the two date ranges and the two caveat texts are read from one artefact.
- **What would resolve it:** extend the Amendment 11 caveat by amendment to every figure drawn from the post-holdout carve-out, the slippage band included, and attach it to the closure sentence on the same terms standing rule 13 attaches an n.
- **Confidence:** MEDIUM-HIGH — the scope gap is plain; what is arguable is how much a spread regime moves over a decade, which nobody here has measured.
- **Invalidated by later commits?:** no — anchored SHA is live HEAD and H1 is closed.
- **Disclosed by authors?:** partially — Amendment 11 discloses the regime problem in full and in advance for the dispersion (progress.md:2331-2338); it is the *scope* of that disclosure, not its existence, that this finding challenges.

---

### DRAFT-p3-progress-14
- **Repository / SHA:** ORBExperiment / f2aa675a80fc06b74979040b3028154d1add5ec0
- **Hypothesis or artifact:** Section 0's `GO` clause after Amendment 21 restated the Section 10 latch as a joint condition
- **Direction:** B
- **Class:** INTERNAL_INCONSISTENCY
- **Severity:** S4
- **Label:** DERIVED
- **Claim challenged (verbatim quote):** "**Clause 1, restated: JOINT power — the probability that both co-primaries reject — at or above 80 percent at achievable N** … So **a reader may never take the larger component power, or either component power, as the design's power**" — ORBExperiment/REGISTRATION.md:3578-3590 (§10.1, Amendment 21)
- **Evidence:**
  - Section 0's GO clause is still evaluated on the two **component** powers: `powers_pass = (power.e1_power_at_registered >= CONFIG.target_power and power.e2_power_at_registered >= CONFIG.target_power)` — ORBExperiment/src/orb/section0.py:255-258.
  - Two components at 0.80 each are jointly anywhere from 0.60 to 0.80 — the registration says so itself at §10.1 — so Section 0 can fire `GO` on a design whose joint power is 0.60 while Section 10 clause 1 refuses the latch.
  - The repository checked the analogous question for one other branch and recorded the answer: "**Had BLOCKED-1 been defined on JOINT power at the registered assumption it would fire, at 0.043277.** **The branch was not changed**, and `src/orb/section0.py` is byte-identical to its state before this pass." — ORBExperiment/progress.md:3323-3328. GO is not examined.
- **Recomputation (if any):** none — the clause is three lines of code.
- **What would resolve it:** an amendment stating whether Section 0's GO floor is intentionally a per-component condition while the latch is joint, and if so why.
- **Confidence:** HIGH — the code and the amendment are both explicit.
- **Invalidated by later commits?:** no — anchored SHA is live HEAD; GO never fired and H1 is closed, which is why this is S4 rather than higher.
- **Disclosed by authors?:** partially — the BLOCKED-1 analogue is disclosed at progress.md:3323-3328; the GO clause is not mentioned.

---

## What I checked and found sound

These are the places where I went looking for the B-thesis and it did not hold. Each is listed because a reader of the findings above is entitled to know the repository was not only searched for faults.

1. **The pre-committed rescue criterion is genuinely pre-committed.** `4ae14dc` ("docs: A.-1 TASK 0 — the rescue-pass success criterion, pre-committed", 2026-08-29 20:13:26 −0700) precedes `5899e1b` ("feat: A.3 TASK 2 — the slippage band measured", 20:41:12) in the live `git log`. The claim at ORBExperiment/progress.md:3526-3531 and README.md:30-32 is true and checkable, exactly as the repository says it is.
2. **The measured-band arithmetic reproduces exactly.** `shift = (entry_p − entry_c) + s·(stop_p − stop_c) + (1−s)·(close_p − close_c)` gives **0.467065203**, matching `measured_shift_usd_per_share` to 9 dp; the carried shift 0.04145454545 also reproduces. No arithmetic error anywhere in the rescue pass.
3. **The `NOT_RESCUED` outcome is robust to every alternative construction I tried.** Using **mean** rather than p90/median slippage gives a shift of 0.113393 — still 2.8× the central mean. Removing the close leg entirely gives 0.330447. The **central** band alone already gives a per-share net of −0.084162 at the registered assumption. The measured band would need a 246.7-fold reduction to reach the 0.001893 the criterion required. The closure direction is not fragile.
4. **The "21.89-fold" figure in the closure block is correctly scoped.** 0.041455 / 0.001893 = 21.90, and it is stated as of commit `4ae14dc`, before the band was measured — not as a claim about the measured band.
5. **`joint_power` is correct and correctly framed.** `min(e1, e2)` as an unconditional upper bound, a Fréchet lower bound, and a named binding component (ORBExperiment/src/orb/power.py, `JointPower`) — with the registration forbidding a reader from quoting a component power as the design's power. This is better practice than the program's other repositories.
6. **The Berger (1982) intersection-union argument is correct.** Requiring every component of an IUT to reject does bound the overall size by the per-component level; `1 − 0.95^(1/k)` is the Šidák correction for a union rule and was the wrong instrument. Amendment 18's statistics are right. My finding 1 is not that the correction is wrong — it is that the quantity it was applied to is not E1's registered decision rule.
7. **`trades_for_e2_power` returns a recorded absence rather than a large number** when the alternative lies inside the null (ORBExperiment/src/orb/power.py), and `e2_power_pessimistic` refuses to clamp a sub-alpha power. Both are the right behaviour and both are pinned.
8. **The tape identification is a real measurement with a real control.** Alpaca-SIP against Alpaca-IEX — same vendor, same host, one parameter changed — separates at median 0.027761 with 100 of 100 pairs below the 0.20 threshold (ORBExperiment/reports/stage_a1r/task4_tape.json). The thresholds were registered and pinned by ULP-boundary fixtures before the tool ran, and mutation 12 is caught by the boundary fixture rather than the headline case.
9. **The shared-upstream limitation is registered before the number it would have flattered.** "**The cross-vendor agreement measurement on this pair scores a redistribution pipeline, not two independent feeds** … **it is not the Concretum test**" (ORBExperiment/progress.md:1506-1510) is written before any agreement share exists. I looked for this being softened later and it is not; SL-1, SL-2 and SL-3 all carry it forward.
10. **The feed-confirmation `NOT_CONFIRMED` first run is recorded, and the classifier was fixed rather than the verdict.** A chunk serving 0 bars on both feeds had been counted as a match to the single-venue feed; it is now excluded as uninformative and the sample widened from 4 to 8 (ORBExperiment/progress.md:2493-2518). I checked that the widening did not change the discriminating chunks' answers: 7 of 7 match the consolidated count, 0 of 7 the single-venue count.
11. **The cost model's refusal is real and was not weakened to produce a number.** `REGISTERED_COST_MODEL` refuses all 550 trades because the SEC Section 31 effective date is `Absent`; the repository bracketed the one unmeasured component at both ends rather than inventing a date, and the bracket is 8.43 × 10⁻⁵ wide relative (ORBExperiment/progress.md:2686-2698). That is the correct move and it is correctly reported.
12. **The 14-day re-pull wait was not shortened, and the same-day feed-confirmation counts are explicitly refused as a revision measurement**: "The same-day counts matching **exactly** … is **not** a revision measurement — a vendor that regenerates history nightly has not yet had a chance to" (ORBExperiment/progress.md:2529-2533). `tools/repull_probe.py` refuses before 2026-09-12 and exits 78.
13. **The ambiguous-rate zero is reported with its bound.** Rule of three: 3/560 ≈ 0.0054 one-sided 95 percent upper bound on 0 events (ORBExperiment/progress.md:3222-3228). The operator's 10 percent threshold was genuinely not crossed and no scope limitation was manufactured.
14. **The 0.982143 trigger rate falsifying the 0.55 assumption is reported as a falsification, not absorbed**, and the "coincidence" that the long-only rate 0.525 sits near 0.55 is recorded "without a claim attached" (ORBExperiment/progress.md:2719-2722). That is the right handling.
15. **Every ETA table reconciles.** I summed the three pass tables: 621 vs 658, 435 vs 438, 380 vs 401, 352 vs 346, 370 vs 348 — all match the stated overall percentages to the rounding shown.
16. **The two self-corrections in Entry 27 are real corrections against the instrument**, not cosmetic: 979 charged requests rather than 954, 1,879 Alpaca rather than 1,980, counted from the append-only ledger, with the amendment's own §2 superseded rather than edited (ORBExperiment/progress.md:2889-2911). Likewise the 336→335 test-count correction at progress.md:1821-1824.
17. **E2 = E1 to five decimal places was diagnosed correctly**, and the cause (`implied_mean / annual_sharpe` a constant, so E2 was a linear rescale) is arithmetically right; replacing rather than repairing E2 was the correct response and Amendment 19 was committed (`421113d`, 12:21:19) **before** the shift was measured (`db92b18`, 12:26:19). I checked that ordering in the live git log specifically because the finding depends on it.
18. **The probe slice's holdout overlap does not spend the Stage D read.** 39 of 60 sessions lie inside the holdout, the bytes were stored by a sealed writer that parses nothing, and the dispersion computation reads only sessions from 2026-07-01, enforced per bar with `Provenance.POST_HOLDOUT` validated at construction. Both latch files are absent (`data/state/` holds neither), verified in the repository's own precondition tables at three separate passes.
19. **Amendment 25's multiplicity cost for H1b is paid rather than avoided**: the DSR trial count goes 8 → 9 for H1b "because the change was proposed after seeing a null", and H1's count is left at 8. The floor itself is deliberately not registered, "because choosing one from the scan that motivated it would fit a parameter to its own evidence" (ORBExperiment/progress.md:3555-3564). That is the correct handling of a post-hoc filter change, and it is rarer than it should be.
20. **The calendar disagreements with the prompt are recorded, not reconciled**: 1,762 against ~1,760 and 875 against ~880, with t moving 2.616 → 2.609 and no verdict row moving (ORBExperiment/progress.md:613-621). Same for minimum-N 515-not-514 and 1,158-not-1,157.

## Live-repo access log

Read-only git access to `/home/kiros-li/Documents/GitHub/ORBExperiment` was used for commit dating only (`git status --porcelain`, `git log`, `git rev-parse`). No untracked or gitignored data was read.

- **Before** — `git -C /home/kiros-li/Documents/GitHub/ORBExperiment status --porcelain`:
```
```
(empty — zero lines of output, exit 0)

- **After** — `git -C /home/kiros-li/Documents/GitHub/ORBExperiment status --porcelain`:
```
```
(empty — zero lines of output, exit 0)

`git rev-parse HEAD` returned `f2aa675a80fc06b74979040b3028154d1add5ec0`, identical to the anchored SHA. Nothing was modified.
