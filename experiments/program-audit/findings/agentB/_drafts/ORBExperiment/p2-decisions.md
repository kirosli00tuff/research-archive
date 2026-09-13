# Agent B draft findings — ORBExperiment, part p2-decisions

**Repository / SHA:** ORBExperiment / f2aa675a80fc06b74979040b3028154d1add5ec0 (main, 2026-08-29 local / 2026-08-30 UTC)
**Assigned documents:** `DECISIONS.md`, `README.md`, `docs/ACCESS.md`, `docs/DUPLICATION.md`, `docs/HANDOVER.md`, `docs/STAGES.md`, `docs/STAGE_A_PROMPT.md`, `reports/*.md`
**Read from:** `/home/kiros-li/.cache/program-audit/scratchpad/snap/ORBExperiment/` plus the live repository's git history (read-only) and the gitignored `data/` working tree (read-only, UNANCHORED, read 2026-09-12 ~18:09Z).
**Recomputation environment:** `/home/kiros-li/.cache/program-audit/scratchpad/venv/bin/python`, scripts under `/home/kiros-li/.cache/program-audit/scratchpad/work/agentB-ORB-p2/`.

Note on dates: every commit in this repository is dated in **UTC** in the documents and in **local (−07:00)** in `git log`. "2026-08-30" in the documents is the UTC date of commits made on the evening of 2026-08-29 local. Findings below use the document convention unless a commit is quoted.

---

### DRAFT-p2-decisions-1
- **Repository / SHA:** ORBExperiment / f2aa675a80fc06b74979040b3028154d1add5ec0
- **Hypothesis or artifact:** H1 co-primary E1 — the power figure 0.832450 and the claim that E1 clears its 80 percent bar (Amendment 18 / ADR-032, carried into the closure framing)
- **Direction:** B
- **Class:** STATISTICAL
- **Severity:** S1
- **Label:** DERIVED
- **Claim challenged (verbatim quote):** "**E1 clears its 80 percent bar at the registered assumption for the first time.\nThe design does not.**" — ORBExperiment/README.md:407-408; and "**E1 at the registered 1.40 Sharpe assumption on the achievable\nholdout moves 0.743521 → 0.832450, and the minimum n for 80 percent power falls\n1,006 → 795 against 875 achievable — a shortfall of 131 becomes a surplus of\n80.**" — ORBExperiment/DECISIONS.md:1170-1174
- **Evidence:**
  - The registered E1 decision rule is a **threshold on a statistic, not a significance test**: "**Bar: deflated Sharpe at or above 1.00.**" — ORBExperiment/REGISTRATION.md:444; ADR-004 fixes the statistic as "the **annualized Sharpe net of the deflation benchmark**, `annualize(SR_hat − SR0)`" — ORBExperiment/DECISIONS.md:99-100.
  - The shipped verdict function implements exactly that threshold and uses **no alpha for E1**: `e1_passes=e1 >= CONFIG.deflated_sharpe_bar` — ORBExperiment/src/orb/verdict.py:269, with `deflated_sharpe_bar=1.00` at ORBExperiment/src/orb/config.py:258.
  - The power figure is produced by `power_one_sided`, whose documented model is the power of a **one-sided test of a zero null** at alpha: "Power of the one-sided Sharpe test at ``alpha``. … power is ``Phi(mean - z_{1-alpha})``" — ORBExperiment/src/orb/power.py:55-61. Amendment 18 names it as the source of the table: "**One-sided, from `orb.power.power_one_sided`**" — ORBExperiment/REGISTRATION.md:3073.
  - The entire movement 0.743521 → 0.832450 is a change in **alpha** (0.02532057 → 0.05) — ORBExperiment/REGISTRATION.md:3076-3082. Amendment 18 states in the same section that it "**does not touch the deflated Sharpe's own correction**" and that "**The deflated-Sharpe bar stays at 1.00**" — ORBExperiment/REGISTRATION.md:3062-3069. An alpha that does not enter E1's pass rule cannot move E1's probability of passing.
  - `SR0`, the deflation benchmark the registered bar is measured against, is an **unmeasured quantity in this repository**: "Where that dispersion is unmeasured, `expected_max_sharpe` returns `Absent` and **E1 refuses rather than deflating by an invented amount**. That is its state today." — ORBExperiment/DECISIONS.md:110-112; code at ORBExperiment/src/orb/verdict.py:110-126.
  - No document states that the E1 power figure is computed against a zero null rather than against the registered 1.00 bar (searched README.md, DECISIONS.md, docs/, REGISTRATION.md, progress.md, report.md).
- **Recomputation (if any):**
  - Inputs: annual Sharpe 1.40 (REGISTRATION.md:481), trading days 252 (`CONFIG.trading_days_per_year`, src/orb/power.py:36), n = 875 holdout sessions (reports/stage_a2/calendar.md:31), bar 1.00 annualized (REGISTRATION.md:444), alpha 0.05 (src/orb/config.py:256).
  - Method (same normal, unit-variance model the repository's own module uses): reproduce the repository's figures, then compute the probability of clearing the **registered** bar, `P(annualized SR_hat − SR0 ≥ 1.00)` with `SE(annualized SR_hat) = sqrt(252/n)`.
  - Reproduced exactly: alpha 0.05 → 0.832450 / 0.999835 / 0.366747 (holdout) and 0.980162 / 1.000000 / 0.581652 (in-sample); alpha 0.02532057 → 0.743521 / 0.999484 / 0.257802; min n 795 and 1,006. Every published figure reproduces to six decimals.
  - Against the registered bar, **with the most favourable possible deflation SR0 = 0**: power = Φ((1.40 − 1.00)/sqrt(252/875)) = Φ(0.745358) = **0.771972** — below 0.80. Minimum n for 80 percent against the 1.00 bar at SR0 = 0 is **1,116**, against 875 achievable; i.e. a shortfall of **241 sessions**, not "a surplus of 80".
  - With any positive deflation the figure falls further: SR0 = 0.25 → 0.610073; SR0 = 0.50 → 0.426089; SR0 = 0.75 → 0.257140 (n = 875, true annual Sharpe 1.40).
- **What would resolve it:** either (a) a statement in the registration that "E1 power" means the power of a zero-null significance test and that the power to clear the registered 1.00 deflated bar is a different, smaller and currently uncomputed quantity; or (b) a recomputation of E1 power against `annualize(SR_hat − SR0) ≥ 1.00` with a measured or bracketed trial-Sharpe dispersion, and a restatement of Section 10 clause 1 against that figure.
- **Confidence:** HIGH — the registered bar, the code that fires it, and the code that computes the power are all in the snapshot and disagree about what E1's pass event is; the recomputation uses the repository's own distributional model.
- **Invalidated by later commits?:** no — the bar (1.00), the statistic (ADR-004) and `power_one_sided` are all pre-anchor and pushed; a later commit could only fix it by recomputing, which would confirm the finding.
- **Disclosed by authors?:** no — the repository warns readers not to read 0.832450 as *the design's* power (docs/HANDOVER.md:374-377) but never that it is the power of a test whose null the registered E1 rule does not use.

---

### DRAFT-p2-decisions-2
- **Repository / SHA:** ORBExperiment / f2aa675a80fc06b74979040b3028154d1add5ec0
- **Hypothesis or artifact:** H1b (`REGISTERED_NOT_OPEN`) — the price-floor feasibility scan and the claim that its registered mechanism is confirmed
- **Direction:** B
- **Class:** UNSUPPORTED_POSITIVE
- **Severity:** S1
- **Label:** DERIVED
- **Claim challenged (verbatim quote):** "**The registered mechanism is confirmed** — the ratio rises monotonically while\nthe shift stays inside a 4 percent band, which is the price-invariance H1b\nasserted before the scan." — ORBExperiment/README.md:331-333; and "The mechanism was **confirmed** and its **competing effect\nwas measured with it**: the central-mean-to-shift ratio rises **0.9742 → 0.9983 →\n1.1415 → 1.4767 → 2.1424** across the five floors" — ORBExperiment/DECISIONS.md:1412-1415
- **Evidence:**
  - The `shift` column of the scan is **the carried QQQ band**, not the band measured minutes earlier in the same pass. The scan's own artifact says so: "The shift here is the registered Section 6 band shift at each floor's own measured stop-exit share" — ORBExperiment/reports/stage_a3rescue/task4_floor_scan.json (`comparison_figure_note`).
  - In code the shift is `cost_model.mean_slippage_shift_per_share(stop_share, band_from=Band.CENTRAL, band_to=Band.PESSIMISTIC)` on `REGISTERED_COST_MODEL` — ORBExperiment/src/orb/dispersion.py:1129-1136 and ORBExperiment/tools/floor_scan.py:66-73, 82-88. That function is `entry_shift + exit_shift` over the **registered constants** — ORBExperiment/src/orb/costs.py:143-190 — i.e. **shift = 0.030 + 0.030 × stop_exit_share**, with no price term of any kind.
  - The same pass measured that those constants understate cost on the traded instruments by **11.27×**: `"ratio_measured_over_carried": 11.266923753633597`, `"carried_band_shift": 0.04145454545454545`, `"measured_band_shift": 0.46706520287790176` — ORBExperiment/reports/stage_a3rescue/task3_rescue_verdict.json (`shift_before_and_after`); README.md:304 records the same pair.
  - Both artifacts were committed in the **same commit**: `git show --stat 5899e1b` (2026-08-29 20:41:12 −0700) adds `reports/stage_a3rescue/task2_slippage_band.json`, `reports/stage_a3rescue/task4_floor_scan.json`, `tools/slippage_band.py` and `tools/floor_scan.py` together. The measured band was in hand when the scan was produced.
  - The only price-sensitive check offered beside the ratio is the entry overshoot, which is **0.0 at every floor** — `entry_overshoot_median_usd_per_share: 0.0` in all five rows of task4_floor_scan.json — and the repository states this is a resolution artefact, not a measurement: "**The entry-overshoot median is 0.0000 at every floor**, which is a **one-minute resolution limit and not a measurement that overshoot is zero**" — README.md:344-345. The scan therefore contains no statistic capable of falsifying price-invariance.
  - The repository did hold a price-sensitive execution measurement — the per-trade time-weighted entry half spread, median 0.076572, p90 0.333662, n = 550 minutes (README.md:300) — and it is not stratified by price anywhere.
- **Recomputation (if any):**
  - Inputs: the five scan rows (`price_floor_usd`, `shift_usd_per_share`, `central_mean_usd_per_share_at_1_40`) from ORBExperiment/reports/stage_a3rescue/task4_floor_scan.json; measured shift 0.46706520287790176 from ORBExperiment/reports/stage_a3rescue/task2_slippage_band.json.
  - Method: (a) invert the shift to its implied stop share, `(shift − 0.030)/0.030`; (b) recompute `central ÷ shift` with the measured band substituted for the carried one, which is the substitution H1b's own price-invariance premise licenses.
  - (a) implied stop shares 0.381818 / 0.392727 / 0.382940 / 0.362187 / 0.332237 — the shift column is an exact affine function of the stop-exit share, confirming it carries no price information. The "4 percent band" is the range of the stop share, and is in fact 4.34 percent of its maximum / **4.54 percent of its minimum**.
  - (b) ratios under the measured band: floor 5 → **0.0865**, 10 → **0.0893**, 20 → **0.1014**, 50 → **0.1292**, 100 → **0.1833**. The table's crossing of 1.0 at the 20 USD floor disappears; the best scanned floor leaves the implied edge **5.5× below** the measured cost shift.
- **What would resolve it:** re-run the scan with the measured band (or with the entry half spread stratified by price) and re-state whether the mechanism is confirmed; or withdraw "confirmed" and label the table what it is — a scan of the assumed cost constant against a dispersion that rises with price.
- **Confidence:** HIGH — the shift's functional form is read directly from source, and the measured band is in the sibling artifact of the same commit.
- **Invalidated by later commits?:** no — H1b is `REGISTERED_NOT_OPEN` at the anchor and the scan is the only evidence offered for it; a later pass could only replace the table.
- **Disclosed by authors?:** partially — `docs/HANDOVER.md:290-293` warns that H1b "**inherits the closure's problem**: the measured entry half spread of **0.076572 median** is what killed H1, and a raised floor improves the ratio only if the spread does not scale with price — which the scan's overshoot column **cannot** confirm at one-minute resolution." That sentence appears in one option of one open-item list; it does not appear beside the "confirmed" claim in README.md:331, in ADR-037's consequences (DECISIONS.md:1412), in the scan artifact, or in the commit subject "H1b price-floor feasibility scan, mechanism confirmed".

---

### DRAFT-p2-decisions-3
- **Repository / SHA:** ORBExperiment / f2aa675a80fc06b74979040b3028154d1add5ec0
- **Hypothesis or artifact:** A.1 TASK 6 delisted-name coverage — the `PASS` that keeps BLOCKED-3 and BLOCKED-5 from firing
- **Direction:** B
- **Class:** UNSUPPORTED_POSITIVE
- **Severity:** S2
- **Label:** DERIVED
- **Claim challenged (verbatim quote):** "> ### **Verdict: `PASS` — 203 delisted names with intraday history, `n = 229` in-window names checked on Alpaca, share 0.8865.**\n> The registered bar is **100 or more**. **203 is a count of names this\n> repository requested bars for and received them — not a rate scaled up.**" — ORBExperiment/docs/ACCESS.md:464-466; mirrored as "| **delisted names with intraday history** | **203** — **`PASS`**, share 0.8865 | **229 checked** |" — ORBExperiment/README.md:195
- **Evidence:**
  - The registered bar is a **count with no registered sample size**: "**Delisted coverage, A.1 TASK 4.** `PASS` at **100 or more** delisted names served with intraday history; `PARTIAL` at **20 to 99**; `FAIL` **below 20**." — ORBExperiment/REGISTRATION.md:118-119.
  - The first draw fired **PARTIAL** and the artifact records that label: `"alpaca": {"names_with_intraday_history": 81, "registered_verdict_on_measured_count": "PARTIAL", "sample_size": 120, "served_share": 0.675}` — ORBExperiment/reports/stage_a1r/task6_delisted.json.
  - Restricting that first draw to the registered window does not change the verdict: **81 of 89 in-window served** (progress.md:1688, DECISIONS.md:762) — 81 is still inside the 20–99 PARTIAL band.
  - The sample was then **enlarged after the fact** by 140 further names: `"first_pass_in_window_checks": 89, "supplementary_checks": 140, "combined_in_window_checks": 229, "delisted_names_with_intraday_history": 203, "registered_verdict": "PASS"` — ORBExperiment/reports/stage_a1r/task6b_delisted_in_window.json. 89 + 140 = 229 and the count crosses 100 at roughly the 110th in-window check.
  - Because the bar is a count and the serve rate is ~0.887, **the verdict is a function of how many names are probed**: any n ≥ ~113 gives PASS and any n ≤ ~110 gives PARTIAL, on the same vendor and the same population. The repository's own artifacts demonstrate this directly — the identical rule applied to the reference vendor with a 20-name sample is recorded as `"massive": {"names_with_intraday_history": 18, ... "registered_verdict_on_measured_count": "FAIL", "sample_size": 20}` (reports/stage_a1r/task6_delisted.json), a `FAIL` label that appears in no markdown file in the repository.
  - The repository blocks the obvious alternative (scaling the rate to the 4,731-name population) on principle: "**a rate measured on 20 names and multiplied by 4,731 is a synthesized value** — standing rule 5 forbids one" (progress.md:1701-1703; DECISIONS.md:766-769). That leaves the count, and the count was chosen after the first count was seen.
  - What is disclosed is the **re-draw**, and the reason given for it is the out-of-window contamination, not the shortfall: "The sample was re-drawn in-window and **enlarged to n = 229** rather than scaled up" — DECISIONS.md:765-766. `docs/ACCESS.md` presents 229/203 as a single draw (line 470) and does not mention the first pass at all.
- **Recomputation (if any):** inputs 89 first-pass in-window checks with 81 served and 140 supplementary checks with 122 served (203 − 81), from reports/stage_a1r/task6b_delisted_in_window.json and reports/stage_a1r/task6_delisted.json. At the measured in-window serve share of 203/229 = 0.8865, the count crosses the registered 100 bar at n = 113 checks; the first pass stopped at 89 and reported 81. No arithmetic in the published figures is wrong; the verdict is what depends on the stopping point.
- **What would resolve it:** a registered sample size for the delisted probe (fixed before the draw), or a verdict expressed on the measured **share** with an interval, or an explicit statement beside the PASS that the first in-window draw returned 81 and fired PARTIAL and that the sample was enlarged afterwards.
- **Confidence:** HIGH — both stopping points and both verdict labels are recorded in the repository's own stored artifacts.
- **Invalidated by later commits?:** no — both artifacts are pre-anchor and the PASS is carried unchanged into README, HANDOVER, ACCESS and HYPOTHESES.
- **Disclosed by authors?:** partially — the enlargement is disclosed at DECISIONS.md:765 and progress.md:1696-1703; the fact that the first in-window count fired PARTIAL against the registered bar, and that the PASS therefore turns on a sample size chosen afterwards, is stated nowhere.

---

### DRAFT-p2-decisions-4
- **Repository / SHA:** ORBExperiment / f2aa675a80fc06b74979040b3028154d1add5ec0
- **Hypothesis or artifact:** the shipped "measured slippage band" (A.3 TASK 2, Amendment 26, ADR-038) — specifically the close-exit leg and the six-row carried-vs-measured comparison
- **Direction:** B
- **Class:** UNSUPPORTED_POSITIVE
- **Severity:** S2
- **Label:** DERIVED
- **Claim challenged (verbatim quote):** "| close, pessimistic | 0.0200 | **0.261000** | **13.05×** | **UNDERSTATED** |" — ORBExperiment/README.md:296; and "**Five of\nsix band ends were understated by the carried figures**, the entry pessimistic\nend by **8.87×** and the close pessimistic end by **13.05×**." — ORBExperiment/README.md:39-41
- **Evidence:**
  - The close leg is computed as the **absolute price difference between two prices**, not as an execution cost: `close_slippage.append(abs(row.official_close_c - row.last_exit_window_close_c) / CENT)` — ORBExperiment/src/orb/dispersion.py:943-945, where `last_exit_window_close_c` is the close of the last bar of the registered 15:55–15:59 exit window (src/orb/dispersion.py:388) and `official_close_c` is the close of the first bar in the two minutes **after** that window (src/orb/dispersion.py:389-394).
  - The registered exit is the 15:55–15:59 window, not the closing auction: "**Exit:** the session close, 15:55 to 15:59 Eastern, **no profit target**." — ORBExperiment/src/orb/signal.py:11; ADR-003 registers the same (DECISIONS.md:75-76). The quantity charged is therefore a price move over a gap the registered rule never trades across. The code's own comment asserts the counterfactual instead: "A real market-on-close order fills at the official closing print" (src/orb/dispersion.py:385).
  - Because it is an absolute deviation, its expectation is **strictly positive under zero execution cost** and scales with the 1–5 minute volatility of the selected names — which are selected precisely for elevated opening relative volume. It cannot return zero and cannot be compared like-for-like to a carried slippage assumption.
  - The other two legs measure a different quantity: entry and stop add the **time-weighted quoted half spread** to the overshoot (src/orb/dispersion.py:920-941; ADR-038, DECISIONS.md:1451-1457). The close leg adds **no spread at all**. The README table (lines 289-296) and the HANDOVER closure table (docs/HANDOVER.md:52-58) present all six ends as one band measured against one carried band.
- **Recomputation (if any):**
  - Inputs: `measured_band` and `stop_exit_share_used` from ORBExperiment/reports/stage_a3rescue/task2_slippage_band.json; registered carried band from ORBExperiment/src/orb/costs.py (entry 0.020/0.040, stop 0.040/0.080, close 0.010/0.020).
  - Method: recompute the shift as `entry_shift + stop_share·stop_shift + (1−stop_share)·close_shift`.
  - With all three legs measured: 0.267626 + 0.381818·0.164532 + 0.618182·0.221000 = **0.467066**, reproducing the published 0.46706520 to six decimals.
  - Replacing only the close leg with the carried 0.010/0.020: 0.267626 + 0.062822 + 0.618182·0.010 = **0.336630** — still 8.3× the central mean of 0.040386, so the `NOT_RESCUED` outcome and the `cost-bound` closure **survive** the objection. What does not survive is the "five of six ends understated" framing and the 13.05× and 4.00× close-leg ratios, which compare a price-change statistic to a slippage assumption.
- **What would resolve it:** measure the close leg the way the entry and stop legs are measured (half spread across the 15:55–15:59 minutes plus any overshoot against the modelled fill price), or label the existing column as the 15:59-to-print price move and drop it from the carried-vs-measured comparison.
- **Confidence:** HIGH — the computation is four lines of source and the registered exit window is pinned in the signal module.
- **Invalidated by later commits?:** no — the band is the repository's shipped artifact at the anchor and is carried into README, HANDOVER, HYPOTHESES and the closure.
- **Disclosed by authors?:** partially — the row label "close slippage vs the official print" (README.md:303) names the referent, and ADR-038 says the half spread is added "across each entry and stop minute" (DECISIONS.md:1453), from which a reader could infer the close leg is different in kind. Neither says the quantity is an absolute price change, that it cannot be zero, or that the registered rule does not trade the print.

---

### DRAFT-p2-decisions-5
- **Repository / SHA:** ORBExperiment / f2aa675a80fc06b74979040b3028154d1add5ec0
- **Hypothesis or artifact:** Amendment 18 / ADR-032 — the claim that the corrected per-co-primary alpha is what the verdict reads
- **Direction:** B
- **Class:** INTERNAL_INCONSISTENCY
- **Severity:** S2
- **Label:** DERIVED
- **Claim challenged (verbatim quote):** "Registered as `CONFIG.per_test_alpha = 0.05`, read through\n`orb.verdict.per_test_alpha()`." — ORBExperiment/DECISIONS.md:1155-1156 (same sentence at REGISTRATION.md:3045-3046)
- **Evidence:**
  - The only function that fires the registered Section 8 verdict still applies the **superseded** union correction to E2: `e2_passes=p_value < alpha_adj(),` — ORBExperiment/src/orb/verdict.py:272, inside `fire_verdict` (src/orb/verdict.py:256-278). `alpha_adj()` returns `1 − 0.95^(1/2) = 0.02532057` (src/orb/verdict.py:37-47).
  - `per_test_alpha()`'s own docstring instructs the opposite: "Use :func:`per_test_alpha` for the co-primaries." — ORBExperiment/src/orb/verdict.py:44.
  - `per_test_alpha` has **no caller inside `src/`**: grep over `src/`, `tools/`, `tests/` finds it used only by `tools/refire_section0_repair.py:60`, `tools/refire_section0_rescue.py:54`, `tools/rescue_verdict.py:57`, `tools/joint_power.py:74`. The power tables therefore use 0.05 while the verdict would use 0.02532057.
  - The module docstring of the verdict module still states the superseded level as the registered one: "Two co-primaries, one-sided, at ``alpha_adj = 1 - 0.95 ** (1/2) = 0.02532``" — ORBExperiment/src/orb/verdict.py:3.
  - The test suite (419 passing, README.md:438) does not bind this: `tests/test_power.py:28-30` imports `alpha_adj` and sets `ALPHA = alpha_adj()`.
- **Recomputation (if any):** none needed; the discrepancy is read from source. Direction of the error: using 0.02532057 makes E2 **harder** to pass, so a future verdict would be conservative rather than inflated. What is over-claimed is the documentation of what the code does.
- **What would resolve it:** change `fire_verdict` to read `per_test_alpha()`, add a test pinning it, or amend the sentence to say the correction is registered in config and consumed by the power tools while the verdict function still carries the superseded level.
- **Confidence:** HIGH — single line of source against a single sentence of registration.
- **Invalidated by later commits?:** no at the anchor; a later commit fixing the call would remove the defect and confirm the finding.
- **Disclosed by authors?:** no — Amendment 18 §2 states the opposite ("Registered as `CONFIG.per_test_alpha = 0.05` and read through `orb.verdict.per_test_alpha()`", REGISTRATION.md:3045-3046) and lists no exception.

---

### DRAFT-p2-decisions-6
- **Repository / SHA:** ORBExperiment / f2aa675a80fc06b74979040b3028154d1add5ec0
- **Hypothesis or artifact:** the H1 closure — the robustness claim attached to the measured slippage band
- **Direction:** B
- **Class:** PROCESS
- **Severity:** S3
- **Label:** READ
- **Claim challenged (verbatim quote):** "**So the\nclosure is robust: the design failed at the most favourable honest reading of its\nown costs.**" — ORBExperiment/README.md:313-315 (repeated at docs/HANDOVER.md:70-71)
- **Evidence:**
  - The deciding band is measured on **28 evaluable sessions between 2026-07-01 and 2026-08-28**, on a 200-name systematic sample, and is applied to a 1,762-session in-sample window (2016-01-04 to 2022-12-30) and an 875-session holdout (2023-01-03 to 2026-06-30): `"first_session": "2026-07-01", "last_closed_session": "2026-08-28", "sessions_used": 28, "tickers_with_bars": 199` — ORBExperiment/reports/stage_a3rescue/task2_slippage_band.json; README.md:285-287.
  - The repository's own registered caveat for any figure from that region is unbounded in both directions: "the dispersion input comes from a POST-HOLDOUT regime (2026-07-01 to 2026-08-28), later than the sample it is applied to, and may misstate in-sample dispersion **in either direction by an amount this repository has not measured and does not claim to bound**" — ORBExperiment/reports/stage_a3rescue/task3_rescue_verdict.json (`carve_out_caveat`); registered as Amendment 11 and quoted at README.md:240-243, 278-281 and DECISIONS.md:874-882.
  - That caveat is attached, sentence by sentence, to **every E2 and dispersion figure** (README.md:240-243, 278-281, 430-432) and is **not attached to the measured band** anywhere: the rescue-pass table (README.md:289-308), ADR-038 (DECISIONS.md:1424-1476) and the HANDOVER closure table (docs/HANDOVER.md:48-71) carry the one-minute-resolution caveat and no regime caveat.
  - The robustness argument that is offered addresses a different error source — intrabar resolution, which biases the band **down** — and does not bound the regime mismatch: "457 of 550 entry triggers and 195 of 210 stop triggers crossed their boundary intrabar" (README.md:310-312).
- **Recomputation (if any):** none. The point is the scope of a caveat, not an arithmetic error. For calibration: the closure's margin is large (measured shift 0.467065 against a central mean of 0.040386, an 11.57× gap, README.md:304-305), so a regime effect would have to be an order of magnitude to reverse it — which is exactly the claim the repository says it cannot make in either direction.
- **What would resolve it:** attach the Amendment 11 sentence to the measured band wherever it appears, or bound the regime effect (e.g. by comparing quoted half spreads on the same names across earlier years once a quote-serving tier reaching them exists), or restate the closure as conditional on a 2026 H2 cost regime.
- **Confidence:** MEDIUM — the omission is factual and checkable, but the closure's margin makes it unlikely that the missing caveat changes the verdict, and the authors do disclose the regime problem for the sibling input from the same 28 sessions.
- **Invalidated by later commits?:** no — the band and the caveat scoping are both pre-anchor.
- **Disclosed by authors?:** partially — the identical caveat is disclosed for the dispersion measured on the same 28 sessions (README.md:240-243; reports/stage_a3rescue/task3_rescue_verdict.json), which makes its absence from the band a scoping omission rather than an undisclosed hazard.

---

### DRAFT-p2-decisions-7
- **Repository / SHA:** ORBExperiment / f2aa675a80fc06b74979040b3028154d1add5ec0
- **Hypothesis or artifact:** the sealed probe slice and the pending bar-revision verdict (A.1 TASK 9 → the 2026-09-12 re-pull; registered thresholds PASS ≤ 0.005, FAIL > 0.020 firing BLOCKED-2)
- **Direction:** B
- **Class:** PROCESS
- **Severity:** S3
- **Label:** DERIVED
- **Claim challenged (verbatim quote):** "**The measurement that decides this repository is not the return. It is bar\nintegrity.**" — ORBExperiment/README.md:20-21; with the slice recorded as "| **probe slice sealed** | 60 sessions × 40 tickers = **2,400 pairs**, 480 files, **737,507 bars** | — |" — ORBExperiment/README.md:200
- **Evidence:**
  - The integrity question the slice is built to answer is explicitly about corporate actions: "**does it retroactively rewrite already-served bars on a split or a correction.**" — ORBExperiment/DECISIONS.md:190-192 (ADR-007).
  - The slice is a convenience sample that is not conditioned on either: the 40 tickers are "the **alphabetically-first active US common stocks** from the reference vendor that **serve at least one bar** on a fixed reference session" — ORBExperiment/progress.md:1915-1917, listing `A, AA, AADX, AAL, … ACDC` (progress.md:1903). The universe is the **active** listing, so no delisted name — the population the repository spent A.1 TASK 6 proving matters — is in it.
  - The sessions are **already stale when first pulled**: sessions 2026-05-05 to 2026-07-30 (progress.md:1901) sealed on 2026-08-29, i.e. 30 to 116 calendar days after the session closed. Vendor revisions concentrate in the hours and days after a session; a 14-day gap between two pulls of month-old bars is not the window in which a rewrite is likely.
  - A PASS is therefore close to structurally guaranteed at a threshold of **0.005 changed-bar share** (REGISTRATION.md:108-111; docs/HANDOVER.md:140-144), while the repository frames the outcome as the thing that decides it. The repository shows it understands this failure mode in the adjacent case and applies it only there: "a re-pull sent early measures a revision rate biased toward zero, and **zero is the shape of a `PASS`**" — README.md:74-75.
  - The config docstring for the slice promised a different screen and the deviation is recorded: "`CONFIG.probe_tickers` documents *'40 alphabetically-first symbols meeting the sealed liquidity screen.'* **No sealed liquidity screen exists**" — progress.md:1920-1923.
- **Recomputation (if any):** none — no revision figure exists yet (`bar revision rate | Absent(not_yet_measured) | 0`, README.md:201). The finding is about what a PASS on this slice would license.
- **What would resolve it:** state, beside the registered thresholds, that the slice is 40 currently-listed alphabetically-first names on sessions 30–116 days old, that it contains no delisted name and is not conditioned on a split or a correction, and that a PASS therefore bounds revision behaviour only for stale bars on surviving liquid names; or add a second slice conditioned on corporate actions and on delisted names before reading the verdict.
- **Confidence:** MEDIUM — the slice composition and staleness are documented facts; the claim that they bias the verdict toward PASS is an inference from the stated mechanism (splits and corrections) rather than from a measured revision distribution.
- **Invalidated by later commits?:** yes, in one direction — the re-pull became eligible on 2026-09-12 (today), so a post-anchor run could produce a non-zero rate and blunt the finding; it could not make the slice representative.
- **Disclosed by authors?:** partially — the selection rule and the docstring deviation are disclosed at progress.md:1915-1923 and the session range at progress.md:1901; no document states the consequence for what a PASS would support, and README.md:20-22 and docs/HANDOVER.md:9-13 present the measurement as decisive without it.

---

### DRAFT-p2-decisions-8
- **Repository / SHA:** ORBExperiment / f2aa675a80fc06b74979040b3028154d1add5ec0
- **Hypothesis or artifact:** `docs/HANDOVER.md` and `docs/STAGES.md` — the two handover documents, as shipped at the anchor
- **Direction:** B
- **Class:** STALE_FIGURE
- **Severity:** S3
- **Label:** READ
- **Claim challenged (verbatim quote):** "H1 remains\n**OPEN**, and closing it as `untestable-at-achievable-power` is **one of three\nroutes**, not a conclusion this pass reached." — ORBExperiment/docs/HANDOVER.md:383-385, in the same document whose second line is "> # H1 IS CLOSED." — ORBExperiment/docs/HANDOVER.md:6
- **Evidence:**
  - `docs/HANDOVER.md` opens "**Read this before touching anything.**" (line 3) and "> # H1 IS CLOSED." (line 6), then carries four stale statements:
    - "**Ten amendments** stand; read all of them." — line 156, against "**Twenty-eight amendments stand. Thirty-eight ADRs.**" — line 43.
    - "**and all twenty-three\n   amendments** — 5 to 10 the A.1 resumption, 11 to 17 the amendment pass,\n   **18 to 23 the inference repair**." — lines 314-316.
    - "5. **`DECISIONS.md`** — **35 ADRs**; … **032 through 035 the inference repair**." — line 319, against 38 ADRs in DECISIONS.md (ADR-038 at DECISIONS.md:1424).
    - "H1 remains **OPEN**" — line 383.
  - `docs/STAGES.md` is stale in full: "**Status at 2026-08-29: Stage A complete except for the two integrity\nmeasurements. Section 0 fired `PENDING_ACCESS`. H1 is OPEN. Nothing is armed and\nnothing is closed.**" — lines 3-5; the ladder still records "TASK 3–4 blocked" and "**Blocked on an operator item** — two free-tier vendor credentials" (lines 17, 51-53) when two credentials authenticate (README.md:186), and "**n = 10 mutations**" (line 20) against 17 (README.md:440).
  - The repository's own rule is that a superseded statement is struck and left visible with its supersession recorded ("**An ADR is never edited after the fact; a reversal is a new ADR**", DECISIONS.md:5-6; the README uses strikethrough plus a supersession note at README.md:410-415). Neither stale block is marked.
- **Recomputation (if any):** count of ADR headings in DECISIONS.md = 38 (`grep -c '^## ADR' DECISIONS.md`); amendment count 28 per docs/HANDOVER.md:43 and HYPOTHESES.md:50-58.
- **What would resolve it:** strike the four stale HANDOVER statements in place with their supersession, and either stamp `docs/STAGES.md` as superseded or re-date it.
- **Confidence:** HIGH — direct contradictions inside one file.
- **Invalidated by later commits?:** yes — a documentation commit after the anchor would fix it; the anchor ships them.
- **Disclosed by authors?:** no — these are not labelled superseded, and the reading order that a fresh session is given (README.md:533-534) sends that session to `docs/HANDOVER.md`.

---

### DRAFT-p2-decisions-9
- **Repository / SHA:** ORBExperiment / f2aa675a80fc06b74979040b3028154d1add5ec0
- **Hypothesis or artifact:** the session calendar (A.2 TASK 1) — the registered second-source cross-check, and the n = 875 / n = 1,762 denominators that every power figure uses
- **Direction:** B
- **Class:** PROCESS
- **Severity:** S3
- **Label:** READ
- **Claim challenged (verbatim quote):** "| second-source cross-check | **`Absent`** — not completed, **and not fabricated** | 0 |" — ORBExperiment/README.md:366; with the stated reason "Every vendor that serves a machine-\nreadable US equity trading calendar is one of the nine measured at A.1 TASK 1,\nand **all nine are either refused by terms or refused without a credential**." — ORBExperiment/reports/stage_a2/calendar.md:86-88
- **Evidence:**
  - The registered task requires it: "Cross-check the total against a second source and record any disagreement rather than reconciling it." — ORBExperiment/docs/STAGE_A_PROMPT.md:189.
  - The stated blocker was falsified within the same 24 hours: two credentials authenticate and are used for 2,766 charged requests (README.md:182, 209-213, 285; `data/access/requests.jsonl`, read 2026-09-12 ~18:09Z, UNANCHORED). The repository's own duplication screen records that the house already reaches an Alpaca calendar endpoint: "**HFExperiment** reaches a US equity *broker* (IBKR, Alpaca calendar)" — ORBExperiment/docs/DUPLICATION.md:116-117.
  - The cross-check was never revisited in the A.1 resumption, the amendment pass, the inference-repair pass or the rescue pass: `grep -rn "second.source"` returns only the original A.2 entries (README.md:366, report.md:120, reports/stage_a2/calendar.md:80-88, progress.md:623) plus the prompt line.
  - The unverified counts are load-bearing for the one surviving positive: 875 is the denominator of E1's 0.832450 and of the claimed "surplus of 80" sessions over a minimum n of 795 (README.md:404, DECISIONS.md:1170-1174), and the registration's own approximations differ from the computed counts by +2 and −5 sessions (reports/stage_a2/calendar.md:29-31).
- **Recomputation (if any):** none attempted — a second calendar source is exactly what is missing. For scale: the E1 margin at the registered assumption is 875 − 795 = 80 sessions, i.e. an unverified session count would have to be wrong by more than 9 percent to reverse the E1 clearance; the half-session and closure handling (21 half sessions, 2 unscheduled closures, reports/stage_a2/calendar.md:22, 34-45) is the kind of detail a cross-check exists to catch.
- **What would resolve it:** run the cross-check against the now-credentialed Alpaca calendar endpoint and record the disagreement, or amend the entry to say that the blocker was removed on 2026-08-29 and the cross-check was not re-attempted.
- **Confidence:** MEDIUM — the omission and the stale reason are both documented facts; whether the calendar is actually wrong is unknown and is the point.
- **Invalidated by later commits?:** yes — one post-anchor run of the cross-check would close it.
- **Disclosed by authors?:** partially — the absence is disclosed loudly and honestly at README.md:366 and reports/stage_a2/calendar.md:80-95; what is not disclosed is that its stated cause ceased to hold on the same day and that no pass since has revisited it.

---

### DRAFT-p2-decisions-10
- **Repository / SHA:** ORBExperiment / f2aa675a80fc06b74979040b3028154d1add5ec0
- **Hypothesis or artifact:** counting and provenance hygiene in the shipped figures (three items)
- **Direction:** B
- **Class:** PROVENANCE
- **Severity:** S4
- **Label:** DERIVED
- **Claim challenged (verbatim quote):** "**`n = 759` quote requests, 0 dollars spent.**" — ORBExperiment/README.md:285
- **Evidence:**
  1. **759 vs 761 vs 760.** The append-only ledger the repository calls authoritative ("counted from the append-only request ledger, which charges before every send", README.md:210-212) records **761** `alpaca:quotes` charges on day 2026-08-30 — `data/access/requests.jsonl`, read 2026-09-12 ~18:09Z (UNANCHORED; live working tree, gitignored). The tool records `"quote_requests_sent": 759` (reports/stage_a3rescue/task2_slippage_band.json) and the README reports **760 quote minutes served, 0 refused** (README.md:287; `minutes_served` 550 + 210 in the same artifact). Three figures, no reconciliation in any document. The same ledger reproduces the other two pass counts **exactly**: 979 (973 alpaca + 6 massive) for the amendment pass and 1,879 Alpaca of the 3,000 daily cap (README.md:209-212).
  2. **15 vs 14 robots hosts.** "**n = 15 hosts fetched for `robots.txt`**" (docs/ACCESS.md:10; README.md:163; report.md:13; REGISTRATION.md:1330) against **14 rows** in the verbatim table that is the evidence for it (docs/ACCESS.md:52-65). The live `data/access/robots/` holds 21 files including three later cost-source hosts and four `-resolved` duplicates (read 2026-09-12 ~18:09Z, UNANCHORED), so the intended 15th host is not identifiable from the table.
  3. **Rescue artifacts stamped a day before the pass they belong to.** `reports/stage_a3rescue/task3_rescue_verdict.json` asserts `"criterion_precommitted_before_the_measurement": true` while carrying `"computed_at": "2026-08-29"` and `"criterion_precommitted_on": "2026-08-30"` — on its face the artifact says the criterion was committed the day **after** the computation. The cause is that the tools stamp `date.today()` (local) — `tools/rescue_verdict.py:115`, `tools/slippage_band.py:166`, `tools/floor_scan.py:125` — while the criterion date is a hardcoded UTC string (`CRITERION_DATE = "2026-08-30"`, tools/rescue_verdict.py:45) and the ledger's `day` field is UTC. Git resolves the ordering in the repository's favour (4ae14dc 2026-08-29 20:13:26 −0700 precedes 5899e1b 2026-08-29 20:41:12 −0700, which introduces `tools/slippage_band.py`), so the substantive pre-commitment claim stands; the artifact alone contradicts itself.
- **Recomputation (if any):** `json` counts over `data/access/requests.jsonl` (2,766 charges total; by UTC day 2026-08-29 → 2,005, 2026-08-30 → 761; by hour bucket 02h → 25, 06h+07h → 1,001, 18h → 979, 03h(+1d) → 761); row count of the ACCESS.md robots table via `grep -c '^| \`'`.
- **What would resolve it:** reconcile 759/760/761 in the rescue-pass text; identify the 15th robots host or correct the n to 14; stamp tool outputs in UTC so the artifact's own fields agree with its pre-commitment assertion.
- **Confidence:** HIGH for items 1 and 2 (direct counts); HIGH for item 3 as a self-contradiction of the artifact, with the underlying ordering claim verified as sound.
- **Invalidated by later commits?:** no for items 2 and 3; item 1 rests on an unanchored live file that could in principle have been appended to after the anchor — the last ledger row is 2026-08-30T03:39:19.048Z, before the anchor commit at 2026-08-30T03:46Z UTC, so it was not.
- **Disclosed by authors?:** no — each figure is presented without qualification.

---

## What I checked and found sound

- **The rescue-pass pre-commitment (ADR-036).** "Amendment 24, commit `4ae14dc`, precedes the commit containing `tools/slippage_band.py`, and **the ordering is checkable in `git log`**" (DECISIONS.md:1343-1345) — verified in the live history: `4ae14dc` 2026-08-29 20:13:26 −0700 (touching only REGISTRATION.md and progress.md) precedes `5899e1b` 2026-08-29 20:41:12 −0700, which introduces `tools/slippage_band.py`. The criterion text, the `RESCUED_DEGRADED`/`NOT_RESCUED` tiers and the arithmetic ruling out `GO` are all in the earlier commit. This is the single most important process claim in the repository and it holds. (Two caveats worth recording, neither a finding: the three rescue "tasks" all landed in commit `5899e1b` — tools, outputs and announcement text together — so the later commits `7edeea7` "A.3 TASK 3 — NOT_RESCUED" (REGISTRATION.md only) and `68a1c65` "A.3 TASK 4 — H1b price-floor feasibility scan, mechanism confirmed" (`task3_execution_mix.json` only) do not contain what their subjects name, and the standing rule "Commit at every task boundary" was not met in that pass; and a *push* time is not checkable from a local clone.)
- **Every power and cost arithmetic figure I could reproduce, reproduced.** E1 power at both alphas and all three assumptions on both horizons; min n 795 and 1,006; E2 power 0.043277 (= Φ(√(19.642857·875)·(−0.001068/2.029585) − z₀.₉₅)); the carried-band shift 0.041455 from a 0.381818 stop share; the measured shift 0.467065 from the three measured legs; the pessimistic means −0.001068, −0.426679 and −0.386004; the break-even Sharpe 1.437035 and the 2.577 percent gap; the 21.89-fold reduction `GO` would have needed; the 8.87×, 13.05×, 4.35×, 4.00×, 2.48× and 0.84× band ratios; the 11.267× measured-over-carried shift. No arithmetic error found.
- **`GO` ruled out in advance, and the alternatives-rejected list of ADR-034.** The refusal to adjust the cost band, the effect assumption, the alpha or the null after the collapse, and the refusal to clamp a power below alpha (`e2_power_pessimistic` returns the sub-alpha figure, src/orb/power.py:116-136) are all consistent with the code and the artifacts.
- **The closure's own robustness to my DRAFT-4 objection.** Removing the close leg entirely still leaves a shift of 0.336630 against a central mean of 0.040386. The `cost-bound` closure does not depend on the leg I challenge.
- **`cost-bound` is a pre-registered closure kind, not one invented for the verdict.** `git show 14d37ea:HYPOTHESES.md` (the file's first commit, 2026-08-28 19:13 −0700) already lists it with the MLCryptoEngine H6 precedent — three days before the closure.
- **The duplication screen's coverage (docs/DUPLICATION.md).** The 11-repository loop is exhaustive of what existed: VRPExperiment, PMExperiment and retail-power-limits all have first commits dated 2026-08-29, after the screen commit `c26d9ae` (2026-08-28 18:58 −0700). The universal claim at DUPLICATION.md:9-12 is supported.
- **The reach bisection's monotonicity assumption is disclosed and boundary-checked**, contrary to my initial suspicion: `tools/reach_bisect.py:19-29` states the assumption in terms, and docs/ACCESS.md:424-427 records the three adjacent-session probes for both vendors (Alpaca 2015-12-31 → 200/0 bars, 2016-01-04 → 200/718, 2016-01-05 → 200/694). The column is honestly headed "in-sample **reachable**", and the per-name coverage question is answered separately by A.1 TASK 6.
- **The `CONFIRMED_CONSOLIDATED` verdict flip is disclosed and the fix is correct.** ADR-029 (DECISIONS.md:993-998) states that the first run counted a `0 == 0` tie as a single-venue match and returned `NOT_CONFIRMED`, and that "the classifier was fixed rather than the verdict". A tie on zero bars genuinely cannot discriminate; the verdict rests on 7 informative chunks, all matching the consolidated count (`reports/stage_a1amend/task3b_feed_confirmation.json`, `discriminating_checks_n: 7`, `no_sealed_count_matches_the_single_venue_feed: true`).
- **The carve-out universe's survivorship, which cuts the other way.** The 200-name sample is drawn from the **active** listing (README.md:236), so it is survivor-only — but the measurement window is 8 weeks and survivors have *narrower* spreads, so the omission biases the measured band down and makes the closure more conservative, not less. Recorded, not raised.
- **ADR-020 (the operator prior labelled `INDEPENDENT` **and** `independent_but_not_blind`), ADR-026 (an unreached ceiling recorded as `None`), ADR-030 (a burst allowance is not a sustained rate), ADR-024 (client-side window filters), ADR-025 (refusals recorded verbatim, served payloads not), ADR-031 (the two-scalar dispersion contract and the bracketed SEC fee).** Each of these is a case where the repository declined to convert an unmeasured quantity into a number, and in each case the code matches the claim. The 0.0084-percent-wide SEC bracket at reports/stage_a1amend/task5c_dispersion_e2.json is a genuine "the unmeasured input does not matter here, measured rather than hoped".
- **Two small overstatements I checked and judged below the threshold for a finding:** "E2 equals E1 to five decimal places" (README.md:423, docs/HANDOVER.md:398) — the cell is 0.743533 against 0.743521, equal to four decimal places, and ADR-033's own "between 1e-05 and 1e-12" (DECISIONS.md:1189) is the accurate form; and "the shift stays inside a 4 percent band" (README.md:332) — the true spread is 4.34 percent of the maximum and 4.54 percent of the minimum.

---

## Live-repo access log

Live repository touched: `/home/kiros-li/Documents/GitHub/ORBExperiment` — read-only `git log/show/rev-parse` and read-only reads of the gitignored `data/` tree; plus read-only `git log` on `/home/kiros-li/Documents/GitHub/{VRPExperiment,PMExperiment,retail-power-limits}` for first-commit dates only.

Before (`git -C /home/kiros-li/Documents/GitHub/ORBExperiment status --porcelain`):

```
```
(empty — clean tree; `git rev-parse HEAD` = `f2aa675a80fc06b74979040b3028154d1add5ec0`, equal to the anchored SHA)

After (`git -C /home/kiros-li/Documents/GitHub/ORBExperiment status --porcelain`):

```
AFTER_STATUS_PLACEHOLDER
```
