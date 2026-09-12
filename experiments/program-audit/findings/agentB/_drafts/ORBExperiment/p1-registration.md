# Agent B draft findings — ORBExperiment, part p1-registration

**Repository:** ORBExperiment · **Anchored SHA:** `f2aa675a80fc06b74979040b3028154d1add5ec0` (main, 2026-08-29)
**Primary documents read in full:** `REGISTRATION.md` (4,193 lines), `HYPOTHESES.md` (175), `report.md` (1,080).
**Supporting reads:** `README.md`, `progress.md`, `DECISIONS.md`, `src/orb/power.py`, `src/orb/dispersion.py`,
`src/orb/vendors.py`, `tools/slippage_band.py`, every JSON under `reports/`, and the live repository's git history
(read-only: `log`, `show`, `ls-tree`, `-S`).

**Direction:** B — the thesis under test is that conclusions outran evidence.
**Standing caveat:** this repository is unusually disciplined. Most of what I checked held. The findings below are
the places where it did not, and several of them do not change the final verdict; where that is so I say it.

---

### DRAFT-p1-registration-1
- **Repository / SHA:** ORBExperiment / f2aa675a80fc06b74979040b3028154d1add5ec0
- **Hypothesis or artifact:** H1 / Amendment 21 — "E2 power collapses at the registered assumption, and joint power with it"
- **Direction:** B
- **Class:** STATISTICAL
- **Severity:** S2
- **Label:** DERIVED
- **Claim challenged (verbatim quote):** "**The pessimistic-cost mean is −0.001068 USD per share. It is negative.**" — ORBExperiment/REGISTRATION.md:3360 (repeated at report.md:736, README.md:118, HYPOTHESES.md:82), and "the registered effect assumption sits about two and a half percent below the Sharpe at which the design's own pessimistic cost band breaks even ... **The design was registered just on the wrong side of its own cost band**" — ORBExperiment/REGISTRATION.md:3426-3429
- **Evidence:**
  - The sign of the pessimistic-cost mean is a deterministic function of one measured scalar. `shift(p) = 0.020 + p·0.040 + (1−p)·0.010`, with `p` the **measured stop-exit share of 0.381818, n = 550 triggered trades with a resolved exit — 210 stop, 340 close** (ORBExperiment/REGISTRATION.md:3274; `reports/stage_a2repair/task3_execution_mix.json` fields `stop_exit_share`, `stop_exits`, `close_exits`, `sessions_used: 28`).
  - The registration computes and prints the break-even value of that same scalar: "**break-even stop-exit share** at 1.40 | **0.346206**" and "the measured stop share exceeds it by | **0.035612**" — ORBExperiment/REGISTRATION.md:3423-3424.
  - **No interval, standard error or cluster adjustment is attached to 0.381818 anywhere in REGISTRATION.md, HYPOTHESES.md, report.md or README.md.** The margin (0.035612) is smaller than the scalar's own binomial standard error times 1.96.
  - The repository applies the opposite standard to the *other* scalar measured in the same amendment: "**A zero count is reported with its uncertainty, not as a certainty.** By the **rule of three**, a one-sided 95 percent upper bound on a rate observed zero times in `n = 560` is **3/560 ≈ 0.0054**" — ORBExperiment/REGISTRATION.md:3312-3314.
  - The 550 trades are clustered in 28 sessions (19.64 per session, ORBExperiment/REGISTRATION.md:3374), and Section 8 registers clustering for exactly this reason: "by **permutation on session labels with trades clustered by session date**, so that **a single strong session cannot masquerade as many independent observations**" — ORBExperiment/REGISTRATION.md:448-451.
- **Recomputation (if any):**
  - Inputs: `p̂ = 0.38181818181818183` (210/550), `n = 550` (REGISTRATION.md:3274); `central_mean = 0.04038617169045801` (REGISTRATION.md:3381 / 3622); band legs 0.020/0.040/0.010 (REGISTRATION.md:3171-3173).
  - Method: `shift(p) = 0.030 + 0.030p`; break-even `p* = (0.040386 − 0.030)/0.030`; Wald and Wilson 95% intervals on `p̂`; design effect `1 + (m−1)ρ` with `m = 19.64` for the session clustering the repository itself registers.
  - Result (venv python, `/home/kiros-li/.cache/program-audit/scratchpad/work/agentB-ORB-p1`): `p* = 0.346206` (reproduces the repository's figure exactly). Binomial SE = **0.020716**. **Wald 95% CI = [0.341216, 0.422421]; Wilson 95% CI = [0.342168, 0.423108]. The break-even 0.346206 lies inside both.** z = (0.381818 − 0.346206)/SE = **1.719** with no clustering; **1.467** at ρ = 0.02, **1.237** at ρ = 0.05, **1.016** at ρ = 0.10.
  - Propagated to the quantity claimed: the pessimistic-cost mean at the CI ends is **+0.000150** (lower end) and **−0.002286** (upper end) — the interval **straddles zero**. The point estimate −0.001068 reproduces exactly, as does E2 power 0.043277 at 17,188 trades.
  - This uses only the stop-share's sampling error; the dispersion (2.029585, n = 550) and the trades-per-session (19.64, n = 28) carry their own, so the interval above is a floor.
- **What would resolve it:** a clustered (by session) interval on the stop-exit share, or a bootstrap over the 28 sessions, reported beside 0.381818 — and the Amendment 21 headline restated as "not distinguishable from break-even at 95 percent on n = 550 clustered in 28 sessions" rather than as "It is negative". If the interval is computed and still excludes break-even, the finding is void.
- **Confidence:** HIGH — the arithmetic is the repository's own, reproduced to the digit, and the break-even it prints falls inside the 95% interval of the estimate it prints beside it.
- **Invalidated by later commits?:** no — the anchored SHA is the last commit on main and the figures are fixed in Amendments 20 and 21. The *consequence* is already blunted inside the anchor: Amendment 26's measured band puts the shift 11.57× above the central mean, where sampling error cannot flip the sign. This finding therefore attacks Amendment 21's stated finding and the "registered just on the wrong side" framing, **not** the final closure.
- **Disclosed by authors?:** no — the stop-exit share is reported as a point estimate everywhere it appears, and Amendment 21 §4 presents the 0.035612 margin as a measured distance rather than as a distance within one sampling error. The authors do disclose uncertainty for the neighbouring ambiguous-rate scalar (REGISTRATION.md:3312-3314), which is what makes the omission legible.

---

### DRAFT-p1-registration-2
- **Repository / SHA:** ORBExperiment / f2aa675a80fc06b74979040b3028154d1add5ec0
- **Hypothesis or artifact:** H1 closure kind in the house hypothesis register
- **Direction:** B
- **Class:** INTERNAL_INCONSISTENCY
- **Severity:** S2
- **Label:** READ
- **Claim challenged (verbatim quote):** "### H1 — H-ORB, the opening-range breakout on relative-volume-selected names · **CLOSED, `cost-bound`, 2026-08-30**" — ORBExperiment/HYPOTHESES.md:50, whose registered meaning in the same file is "| **cost-bound** | The effect may be real; it does not survive the modeled cost. | MLCryptoEngine H6 — per-fill positive, negative under an order-lifecycle fill model |" — ORBExperiment/HYPOTHESES.md:36
- **Evidence:**
  - Nothing about the effect was measured. "**No in-sample or holdout bar has been read**" — ORBExperiment/REGISTRATION.md:4075; "**nothing in this repository measured whether the directional edge is real** — no in-sample or holdout bar was ever read, and both latches remain absent" — ORBExperiment/HYPOTHESES.md:63.
  - The deciding numbers are power figures, not cost-versus-return figures: "**E2 power 0.000000. JOINT power 0.000000. Minimum n jointly: Absent — unreachable at any sample size.**" — ORBExperiment/HYPOTHESES.md:59; "No session count reaches 80 percent at any assumption" — ORBExperiment/REGISTRATION.md:4085-4086.
  - The registered kind that describes that is the fourth one, and **the registration named it for this exact ground one day before the closure**: "3. **Close H1 as `untestable-at-achievable-power` under its own registered cost assumptions.** This is a **legitimate documented closure** and it is the **fourth closure kind already named in `HYPOTHESES.md`**. It would record that the design, as registered, cannot detect the effect it was built to detect at the sample size it can reach" — ORBExperiment/REGISTRATION.md:3468-3474 (Amendment 21 §6 route 3, dated 2026-08-29). The registered definition of that kind is "The design's own arithmetic blocks it before any data exists" — ORBExperiment/HYPOTHESES.md:39.
  - The closing amendment itself states the `untestable-at-achievable-power` proposition in its own words while recording the other kind: "**The registered outcome is that the design could not reach the test**" — ORBExperiment/REGISTRATION.md:4178; "**It is a finding that this design cannot clear its own registered cost band**, which is a statement about the design" — ORBExperiment/REGISTRATION.md:4162-4163.
  - The kind was fixed by Amendment 24 §4 before the measurement: "**On `NOT_RESCUED`, H1 closes as `cost-bound`** — an **existing** closure kind in `HYPOTHESES.md`, precedent MLCryptoEngine H6" — ORBExperiment/REGISTRATION.md:3724. Pre-commitment fixes the ordering; it does not make the kind fit.
  - Why the label carries weight rather than being cosmetic: the register's stated job is "to prevent retrying a settled question because the number that closed it is buried ... A closed entry carries the figure that closed it" and "**A closure is typed** with one of the five kinds above" so that "the *kind* of the answer survives even when the details are skimmed" — ORBExperiment/HYPOTHESES.md:6-8, 30-32, 173. A skimming reader of the house record takes `cost-bound` + "precedent MLCryptoEngine H6 — per-fill positive" to mean a measured edge was eaten by costs. Here no edge was measured at all.
- **Recomputation (if any):** none required; this is a document-against-document comparison.
- **What would resolve it:** retyping the closure as `untestable-at-achievable-power`, or adding to the H1 register row an explicit note that `cost-bound` is used here of an **assumed** effect size (annualized net Sharpe 1.40) rather than of a measured one, and that Amendment 21 §6 route 3 named the other kind for this ground.
- **Confidence:** HIGH — both kinds and both definitions are in the same file, and the registration names the competing kind for this ground itself.
- **Invalidated by later commits?:** no — the closure and both definitions are at the anchor; a later amendment could retype it.
- **Disclosed by authors?:** partly, and the part that is disclosed is the substance, not the label. "What the closure is NOT ... nothing here measures whether the directional edge is real" (ORBExperiment/REGISTRATION.md:4159-4161, report.md:1017-1022) discloses every fact I rely on. What is nowhere acknowledged is that those facts sit badly with the kind recorded, and the kind is what the register is built to be skimmed for.

---

### DRAFT-p1-registration-3
- **Repository / SHA:** ORBExperiment / f2aa675a80fc06b74979040b3028154d1add5ec0
- **Hypothesis or artifact:** H1b (`REGISTERED_NOT_OPEN`) — Amendment 27, the price-floor feasibility scan; shipped table `reports/stage_a3rescue/task4_floor_scan.json`
- **Direction:** B
- **Class:** UNSUPPORTED_POSITIVE
- **Severity:** S2
- **Label:** DERIVED
- **Claim challenged (verbatim quote):** "### 2. The registered mechanism is confirmed, and so is the competing effect" / "**It rises monotonically: 0.9742 → 0.9983 → 1.1415 → 1.4767 → 2.1424.**" — ORBExperiment/REGISTRATION.md:3879, 3885; and "**The scan confirmed both halves of the registered mechanism**, which is the most interesting thing in it." — ORBExperiment/report.md:1045
- **Evidence:**
  - The mechanism has two halves: "**Per-share slippage is approximately invariant to price** ... **Per-share dispersion and per-share edge both scale with price**" — ORBExperiment/REGISTRATION.md:3800-3804 (Amendment 25 §3).
  - **The edge half is not measured anywhere in the scan.** The scan's edge column is `central mean at 1.40`, and that column is an identity in the *dispersion* column and the *registered Sharpe assumption*: `central_mean = (1.40/√252)·σ/√k`, where `k` is trades per session. Nothing in the scan measures a return. The repository states this in its own words elsewhere: "nothing in this repository measured whether the directional edge is real" — ORBExperiment/report.md:1019-1020.
  - **The headline ratio's rise is driven in large part by the sample thinning the same amendment disqualifies.** §3 of the same amendment says: "> **The \"sessions filling 20\" column measures the SCAN SAMPLE, not the registered universe, and it must not be read as one.** ... A floor that fails to fill 20 names *in a 1-in-26 subsample* says **nothing** about the registered universe, which is **26.6 times larger**." — ORBExperiment/REGISTRATION.md:3903-3909. The same thinning cuts `k` from 19.64 to 10.86 across the scan (`triggered_trades` 550 → 304 on 28 sessions, `reports/stage_a3rescue/task4_floor_scan.json`), and `k` enters the ratio as `1/√k`. §2 does not mention it.
  - **The "competing effect" series is non-monotone and the claim truncates it.** "**The mean relative volume of the selection falls 2.0652 → 1.4103** as the floor rises from 5 to 50 USD" — ORBExperiment/REGISTRATION.md:3890-3891. The full five-row series in the same table is 2.0652, 1.8216, 1.6190, 1.4103, **1.4381** (REGISTRATION.md:3873-3877): it reverses at the 100 USD floor, the row §3 says the scan cannot speak to.
  - Amendment 25 §5 already states the rule this scan breaks: "**H1's power figures do not transfer**: the dispersion, the trades per session and the trigger rate all change with the universe." — ORBExperiment/REGISTRATION.md:3835-3836. Holding the *portfolio* Sharpe fixed at 1.40 while `k` falls is precisely transferring an H1 power input across universes.
- **Recomputation (if any):**
  - Inputs, all from `reports/stage_a3rescue/task4_floor_scan.json` (rows keyed `price_floor_usd` 5/10/20/50/100): `dispersion_usd_per_share` = 2.029585 / 2.096180 / 2.382112 / 2.709331 / 3.199162; `triggered_trades` = 550 / 550 / 551 / 439 / 304; `sessions_evaluated` = 28 on every row; `shift_usd_per_share` = 0.041455 / 0.041782 / 0.041488 / 0.040866 / 0.039967; `central_mean_usd_per_share_at_1_40` = 0.040386 / 0.041711 / 0.047358 / 0.060344 / 0.085626. Sharpe 1.40 from REGISTRATION.md:479.
  - Method: recompute `central_mean = (1.40/√252)·σ/√(triggered_trades/28)` per row and compare with the stored column; then decompose the reported ratio rise into its three factors; then recompute the ratio holding `k` at the 5 USD floor's 19.64.
  - Result: the identity reproduces **all five** stored central-mean values to six decimal places (0.040386, 0.041711, 0.047358, 0.060344, 0.085626). The reported rise 0.9742 → 2.1424 is **×2.1991**, and factorises **exactly** as σ ×1.5763 · (1/√k) ×1.3451 · (1/shift) ×1.0372 = ×2.1991. Holding `k` at 19.64 the series becomes **0.9742, 0.9983, 1.1425, 1.3193, 1.5928** — still monotone, but the top of the range is **26 percent lower** and the 50 USD row falls from 1.4767 to 1.3193.
- **What would resolve it:** stating in §2 that the edge column is imputed from the registered Sharpe assumption and the measured dispersion, not measured; reporting the `k`-held-fixed series beside the raw one; and either dropping the 50 and 100 USD rows from the "confirmed" claim on the same grounds §3 drops them from the fill claim, or noting the relative-volume reversal at 100 USD.
- **Confidence:** HIGH — the identity reproduces every stored value to six decimals and the factorisation is exact.
- **Invalidated by later commits?:** no — the scan is frozen at the anchor and H1b is `REGISTERED_NOT_OPEN`, so nothing downstream has yet consumed it. That is also why the severity is S2 and not S1: no verdict rests on it. Amendment 27 §5 and Amendment 24 §6 are explicit that the scan cannot touch H1's outcome, and it does not.
- **Disclosed by authors?:** partly. §3 discloses the subsample and disqualifies one column on it (REGISTRATION.md:3901-3918), and §4 discloses that the entry-overshoot column "supports the price-invariance claim only weakly" (REGISTRATION.md:3929-3930). Nothing discloses that the ratio column is affected by the same thinning, that the edge half is an assumption rather than a measurement, or that the relative-volume series reverses.

---

### DRAFT-p1-registration-4
- **Repository / SHA:** ORBExperiment / f2aa675a80fc06b74979040b3028154d1add5ec0
- **Hypothesis or artifact:** Amendment 26 — the measured slippage band; shipped table `reports/stage_a3rescue/task2_slippage_band.json`; the close-exit leg
- **Direction:** B
- **Class:** STATISTICAL
- **Severity:** S3
- **Label:** DERIVED
- **Claim challenged (verbatim quote):** "| close exit, pessimistic | 0.0200 | **0.261000** | **13.05×** | **UNDERSTATED** |" — ORBExperiment/REGISTRATION.md:3980, and the row that defines the leg: "| **close** | official print against the 15:59 close | 0.099324 | **0.040000** | **0.261000** | **340**, 0 without an official print |" — ORBExperiment/REGISTRATION.md:3996
- **Evidence:**
  - The close leg is computed as a **two-sided price difference taken in absolute value**: `close_slippage.append(abs(row.official_close_c - row.last_exit_window_close_c) / CENT)` — ORBExperiment/src/orb/dispersion.py:943-944. A price that moves *in the trade's favour* between the exit window and the print is charged as a cost exactly like one that moves against it.
  - The entry and stop legs are computed **one-sided**, adverse only: `through = opened > boundary if row.side is Side.LONG else opened < boundary` … `overshoot = abs(opened - boundary) / CENT if through else 0.0` — ORBExperiment/src/orb/dispersion.py:881-882 (entry) and 913-916 (stop). Those two legs also add a **measured time-weighted half spread** (dispersion.py:889-902, 923-936); the close leg adds no spread term at all.
  - The "official print" is a proxy: `official = [b for b in bars if exit_end_ms <= b.timestamp_ms < exit_end_ms + 120_000]`, then the close of the earliest such bar — ORBExperiment/src/orb/dispersion.py:390-394. It is the close of the first one-minute bar at or after 15:59, not a closing-auction print.
  - The registered exit is a window, not the auction: "**Exit.** The **session close**, modeled in the window **15:55:00 to 15:59:00** Eastern, with **no profit target**." — ORBExperiment/REGISTRATION.md:314-315.
  - The leg is material to the number that closed H1: "| close width × 0.618182 | 0.136618 | 29.3 % |" of the measured shift — ORBExperiment/REGISTRATION.md:4026 — and it supplies the largest single carried-vs-measured ratio quoted in the README headline ("the close pessimistic end by **13.05×**", ORBExperiment/README.md:41).
- **Recomputation (if any):**
  - Inputs: measured band legs from `reports/stage_a3rescue/task2_slippage_band.json` (`measured_band`), stop-exit share 0.381818 (REGISTRATION.md:3274), carried close band 0.010/0.020 (REGISTRATION.md:392).
  - Method: recompute `shift = (entry_p − entry_c) + p·(stop_p − stop_c) + (1−p)·(close_p − close_c)`, then substitute the carried close width of 0.010 for the measured 0.221.
  - Result: the repository's `0.467065203` reproduces exactly. With the carried close width the measured shift is **0.336629**; the entry width alone is **0.267626**. Against the central mean of 0.040386 both are still 8.3× and 6.6× above the RESCUED_DEGRADED bar, so **`NOT_RESCUED` survives the correction and the closure is not overturned.** What does not survive is the magnitude: the "**11.27 times larger**" (HYPOTHESES.md:59) and the "13.05×" close-leg ratio both depend on charging a symmetric price move as a one-directional cost.
- **What would resolve it:** recomputing the close leg one-sided (charging only the adverse half, as the entry and stop legs are charged) with a quoted-spread term, and naming the "official print" as the close of the first minute bar at or after 15:59 wherever the table appears.
- **Confidence:** HIGH on the construction (it is four lines of the repository's own code); MEDIUM on the size of the correction, because the per-trade close distribution is not in the snapshot and I can only bound it structurally (under a symmetric Δ, charging the adverse half alone moves the leg's median from 0.040 toward 0.000 and halves its mean from 0.099324).
- **Invalidated by later commits?:** no — `dispersion.py` at the anchor is the code that produced the shipped band.
- **Disclosed by authors?:** no. The table row label "official print against the 15:59 close" (REGISTRATION.md:3996, README.md:303) describes the difference but not the absolute value, not the proxy, and not the asymmetry with the other two legs. The repository is otherwise scrupulous about this class of thing — it discloses the intrabar lower bound loudly and correctly (REGISTRATION.md:4040-4051).

---

### DRAFT-p1-registration-5
- **Repository / SHA:** ORBExperiment / f2aa675a80fc06b74979040b3028154d1add5ec0
- **Hypothesis or artifact:** the access verdict input `SERVING_FULL_REACH` and the reach figures carried into every Section 0 firing (Amendment 8, Amendment 10, Amendment 16, Amendment 23)
- **Direction:** B
- **Class:** UNSUPPORTED_POSITIVE
- **Severity:** S3
- **Label:** DERIVED
- **Claim challenged (verbatim quote):** "| **Alpaca** | **2016-01-04** | **16** | **1,762 of 1,762 — shortfall 0** | **875 of 875 — shortfall 0** |" — ORBExperiment/REGISTRATION.md:1598; and "**Monotonicity was checked rather than assumed.**" — ORBExperiment/REGISTRATION.md:1601
- **Evidence:**
  - The bisection was run on **one ticker**. `reports/stage_a1r/task5_reach.json` records `"ticker": "AAPL"`, `vendors.alpaca.probes: 16`, `vendors.alpaca.sessions_served: 2657`, and a `verification` list of exactly three sessions (2015-12-31 not served, 2016-01-04 and 2016-01-05 served).
  - **The single-ticker basis appears nowhere in REGISTRATION.md, HYPOTHESES.md, report.md, README.md or progress.md.** `grep -n AAPL` across all five returns only the rate-ceiling endpoint path `/v2/stocks/AAPL/bars` (REGISTRATION.md:1754, progress.md:1752) and unrelated probe rows — not the reach measurement.
  - What "monotonicity was checked" actually covers is three sessions either side of one boundary on that one ticker (REGISTRATION.md:1604-1607). It does not cover the 2,657 sessions the artifact reports as served, and it does not cover any other name.
  - Per-name coverage is **measured, in the same pass, at less than 1**: "**203 delisted names with intraday history, measured** ... `n = 229` in-window names checked on Alpaca ... share 0.8865" — ORBExperiment/progress.md:1648-1651; and the carve-out pull records "**`199` of 200 served at least one bar**" — ORBExperiment/REGISTRATION.md:2573. So 26 of 229 in-window delisted names and 1 of 200 active names served nothing, on the same vendor over the same windows.
  - The figure is load-bearing: it is the input that keeps `PENDING_SPEND` from firing ("It did not fire today, and the reason is the measurement: Alpaca reaches **1,762 of 1,762 in-sample and 875 of 875 holdout sessions**" — ORBExperiment/REGISTRATION.md:1856-1858) and it is the basis of "The primary reaches **every registered session**" in the README (ORBExperiment/README.md:63-65).
- **Recomputation (if any):** none needed. The arithmetic 2,657 = 1,762 + 875 + 20 is a session count from `orb.calendar`; my point is about what 16 probes on one symbol can establish, not about the count.
- **What would resolve it:** stating the ticker and the single-symbol basis in the amendment table, and either (a) restating the claim as "the vendor's tier serves from 2016-01-04 on the probed symbol, so no registered session is excluded by tier depth" — which is what was measured — or (b) probing a sample of names per year to turn the per-name coverage claim into a measurement. Note the repository already measures per-name coverage for delisted names and reports it honestly; the gap is that the reach row is written as if it were a coverage figure.
- **Confidence:** HIGH on the fact (the artifact names the ticker and the probe count); MEDIUM on materiality, because the quantity the reach bisection was designed to measure — tier depth — is genuinely a per-vendor property and is correctly measured.
- **Invalidated by later commits?:** no — the artifact and the amendment are both at the anchor.
- **Disclosed by authors?:** partly. The probe count `n = 16` is disclosed everywhere the figure appears, including the README (ORBExperiment/README.md:65), and the delisted share 0.8865 is disclosed. The single-ticker basis, and the fact that "1,762 of 1,762" is an inference from a boundary rather than a per-session or per-name measurement, are not.

---

### DRAFT-p1-registration-6
- **Repository / SHA:** ORBExperiment / f2aa675a80fc06b74979040b3028154d1add5ec0
- **Hypothesis or artifact:** the amendment log's own ordering claims (Section 14 rules 1 and 4; Amendment 26's numbering note), tested against the live repository's git history
- **Direction:** B
- **Class:** PROVENANCE
- **Severity:** S3
- **Label:** DERIVED
- **Claim challenged (verbatim quote):** "**This amendment is numbered 26 and appears in this file after Amendment 27.** Amendment 27 was appended while this amendment's measurement was still running, and `src/orb/dispersion.py` and ADR-038 already referred to this one as 26 **in text that is committed and pushed.** **The number is kept so every existing reference stays valid, the file order is the true chronology of appends**" — ORBExperiment/REGISTRATION.md:3950-3956
- **Evidence (live repository, read-only; `git -C /home/kiros-li/Documents/GitHub/ORBExperiment log|show|ls-tree|-S`, read 2026-09-12T18:14-18:20Z; working tree clean before and after, HEAD = the anchored SHA):**
  - `git log -S '## Amendment 26 — the slippage band' -- REGISTRATION.md` → **5899e1b** (2026-08-29T20:41:12-07:00, "feat: A.3 TASK 2 — the slippage band measured").
  - `git log -S '## Amendment 27 — the H1b price-floor' -- REGISTRATION.md` → **5899e1b**, the same commit.
  - `git log -S 'Amendment 26' -- src/orb/dispersion.py` → **5899e1b**. `git log -S 'ADR-038' -- DECISIONS.md` → **5899e1b**. So at the moment Amendment 26 was written, **no committed-and-pushed text referred to it as 26**; every reference it cites as already committed entered history in the same commit as the amendment itself. The claim is true of the working tree at most, and it says "committed and pushed".
  - The two amendments' own "what data existed" statements are **mutually circular**: Amendment 26 says "Everything held at Amendments 11 through 25 **and 27**" (REGISTRATION.md:3958-3959); Amendment 27 says "Everything held at Amendments 11 through **26**" (REGISTRATION.md:3857-3858). Section 14 rule 4 requires "**Stating exactly what data existed when the amendment was made**" (REGISTRATION.md:862-864). Both statements cannot be exact.
  - The task-by-task commit sequence the documents describe is not the sequence in the tree. `git show --stat 5899e1b` (labelled "A.3 TASK 2") already contains `reports/stage_a3rescue/task3_rescue_verdict.json`, `reports/stage_a3rescue/task4_floor_scan.json`, `tools/rescue_verdict.py`, `tools/floor_scan.py` and `tools/refire_section0_rescue.py`. The commit labelled "A.3 TASK 3 — NOT_RESCUED" (**7edeea7**) contains only REGISTRATION.md; the commit labelled "A.3 TASK 4 — H1b price-floor feasibility scan" (**68a1c65**) contains only `reports/stage_a3rescue/task3_execution_mix.json`.
  - This matters because the repository twice invites the check: "**the ordering is checkable in `git log` by anyone who doubts it**" — ORBExperiment/REGISTRATION.md:3728-3729 and report.md:882.
- **Recomputation (if any):** not arithmetic. The commands and their outputs are listed above and in the access log at the foot of this file.
- **What would resolve it:** a correction amendment recording that Amendments 26 and 27 entered history in one commit, that the references cited as "committed and pushed" were committed in that same commit, and that the A.3 commit titles do not track the task boundaries.
- **Confidence:** HIGH — five independent `git log -S` results and two `git show --stat` listings, all from the live repository at the anchored SHA.
- **Invalidated by later commits?:** no — the anchored SHA is HEAD and there are no later commits.
- **Disclosed by authors?:** no. Amendment 26's note discloses the out-of-order numbering and gives a reason; the reason is the part the history does not support. **The one ordering claim that actually carries weight is verified and holds** — see "What I checked and found sound" below.

---

### DRAFT-p1-registration-7
- **Repository / SHA:** ORBExperiment / f2aa675a80fc06b74979040b3028154d1add5ec0
- **Hypothesis or artifact:** H1 register entry, the deciding-numbers row
- **Direction:** B
- **Class:** ARITHMETIC
- **Severity:** S4
- **Label:** DERIVED
- **Claim challenged (verbatim quote):** "**Pessimistic-cost mean: −0.426679 — negative by 11.56 times the central mean.**" — ORBExperiment/HYPOTHESES.md:59
- **Evidence:** the central mean is 0.040386 (same line; REGISTRATION.md:4082). `0.426679 / 0.040386 = 10.565`, not 11.56. The figure 11.565 is `shift / central mean` — which is what Amendment 28 §1 and report.md:974 correctly say it is: "**The shift exceeds it by 11.56 times.**" (REGISTRATION.md:4082) and "It rose to **0.467065**, **11.56 times** the central mean." (report.md:974). The register's row applies that multiple to a different quantity.
- **Recomputation (if any):** inputs `pessimistic_cost_mean = −0.42667903118744377` and `central_mean = 0.04038617169045801`, both from `reports/stage_a3rescue/task3_rescue_verdict.json` (`deciding_numbers`) and REGISTRATION.md:4082. Ratio of magnitudes = **10.5650**; `measured_shift / central_mean` = **11.5650**. Verified in the venv python.
- **What would resolve it:** "negative by 10.57 times the central mean", or restating the row as "the shift exceeds the central mean by 11.56 times".
- **Confidence:** HIGH — one division.
- **Invalidated by later commits?:** no.
- **Disclosed by authors?:** no — but the correct multiple for the correct quantity is stated twice elsewhere in the same repository, so this is a transcription slip in the register row rather than a claim the repository defends.

---

### DRAFT-p1-registration-8
- **Repository / SHA:** ORBExperiment / f2aa675a80fc06b74979040b3028154d1add5ec0
- **Hypothesis or artifact:** `HYPOTHESES.md` status header
- **Direction:** B
- **Class:** STALE_FIGURE
- **Severity:** S4
- **Label:** READ
- **Claim challenged (verbatim quote):** "**Status at 2026-08-29: H1 OPEN, registered, Stage A in progress. Ten candidates closed before opening at registration. H2 and H3 PARKED.**" — ORBExperiment/HYPOTHESES.md:15-16
- **Evidence:** the register entry 35 lines below reads "**CLOSED, `cost-bound`, 2026-08-30**" (ORBExperiment/HYPOTHESES.md:50) and the Parked section reads "**H1 closed `cost-bound` on 2026-08-30** (Amendment 28), so the condition that parked these two no longer holds" (ORBExperiment/HYPOTHESES.md:140-141). The status line is the first assertion in a file whose stated purpose is to be skimmed: "**This file exists to prevent retrying a settled question because the number that closed it is buried.**" (ORBExperiment/HYPOTHESES.md:6-7). Unlike REGISTRATION.md, HYPOTHESES.md is not an append-only log — the same commit that closed H1 (34a91b3, HYPOTHESES.md +21/−4) edited the entry in place but left the header.
- **Recomputation (if any):** none.
- **What would resolve it:** updating the status line to 2026-08-30 / H1 CLOSED, or dating it explicitly as a superseded header the way the H1 row dates its own "Superseded status".
- **Confidence:** HIGH.
- **Invalidated by later commits?:** no — one commit later would fix it; there are none after the anchor.
- **Disclosed by authors?:** no. The line carries its own date ("Status at 2026-08-29"), which is a partial defence, but it is presented as the file's current status block and H2/H3's parking condition it asserts is contradicted 125 lines later.

---

### DRAFT-p1-registration-9
- **Repository / SHA:** ORBExperiment / f2aa675a80fc06b74979040b3028154d1add5ec0
- **Hypothesis or artifact:** shipped artifact `orb.vendors.MEASURED_CEILING_PER_MINUTE` and Amendment 9's "Massive's measured ceiling is 5 requests per minute"
- **Direction:** B
- **Class:** INTERNAL_INCONSISTENCY
- **Severity:** S4
- **Label:** DERIVED
- **Claim challenged (verbatim quote):** "**1. Massive's measured ceiling is 5 requests per minute, on both endpoints.** First refusal at request **6 of 8** in both `n = 8` cells." — ORBExperiment/REGISTRATION.md:1769-1770; and the shipped dict's docstring "Measured **sustained** per-minute ceilings per endpoint" — ORBExperiment/src/orb/vendors.py:67
- **Evidence:**
  - The dict records `"massive:grouped": 5.0` — ORBExperiment/src/orb/vendors.py:60 — for an endpoint that was **never probed**. `reports/stage_a1r/task7_ceilings.json` contains cells for `massive:reference` and `massive:aggs` only (plus Alpaca). Amendment 9's own pace table labels that endpoint "**unmeasured endpoint**; carries its vendor's measured figure" — ORBExperiment/REGISTRATION.md:1800. The value is inherited, the dict is named and documented as measured. The repository cites the rule against exactly this: "a measurement of one endpoint is not evidence about another, even on the same host" (solattn ADR-021, quoted at ORBExperiment/REGISTRATION.md:970-972).
  - The two Massive cells that were probed ran **15.76 s and 16.74 s** (`reports/stage_a1r/task7_ceilings.json`, `elapsed_s`), i.e. entirely inside one rolling minute, admitting 5 then refusing 3. That is the same observation shape the repository refuses to call a ceiling five amendments later: "**The whole escalation fit inside one rolling minute** — 55.96 s. So the observation is: *384 requests were admitted within one minute and the 385th was refused.* **A token bucket of capacity near 400 refilling at the documented 200 per minute produces exactly that observation** ... recording **411.72 per minute** as *the ceiling* would be the ADR-026 error running in reverse" — ORBExperiment/REGISTRATION.md:2453-2461. Amendment 14 never revisits Massive's figure.
- **Recomputation (if any):** none beyond reading `elapsed_s` and the cell list out of the stored artifact.
- **What would resolve it:** recording `massive:grouped` as `None` (unmeasured) in the ceiling dict while keeping its conservative pace, and adding to Amendment 14 the note that Massive's 5.0 is a burst-shaped observation within one rolling minute that happens to agree with the vendor's documented figure.
- **Confidence:** HIGH on both facts; the consequence is benign.
- **Invalidated by later commits?:** no.
- **Disclosed by authors?:** partly — the pace table discloses that `massive:grouped` is unmeasured (REGISTRATION.md:1800) and Amendment 9 §2 discloses that documentation and measurement agree at 5/min, which is the real support for the figure. What is not disclosed is that the *ceiling dict itself* carries an inherited value under a "measured" label, or that the Massive observation never exceeded one rolling minute. **Direction of the error runs against the repository's own interest** — a too-low ceiling paces collection more slowly — so this is hygiene, not an over-claim that buys anything.

---

### DRAFT-p1-registration-10
- **Repository / SHA:** ORBExperiment / f2aa675a80fc06b74979040b3028154d1add5ec0
- **Hypothesis or artifact:** the delisted-coverage `PASS`, an input to every Section 0 firing from Amendment 10 onward
- **Direction:** B
- **Class:** UNSUPPORTED_POSITIVE
- **Severity:** S3
- **Label:** DERIVED
- **Claim challenged (verbatim quote):** "| **delisted names with intraday history** | **203**, `n = 229` checked — **`PASS`** |" — ORBExperiment/REGISTRATION.md:1961; and "**203 clears it by measurement, not by extrapolation.**" — ORBExperiment/progress.md:1653
- **Evidence:**
  - The registered bar is a **scale-free count**, not a share: "**Delisted coverage, A.1 TASK 4.** `PASS` at **100 or more** delisted names served with intraday history; `PARTIAL` at **20 to 99**; `FAIL` **below 20**." — ORBExperiment/REGISTRATION.md:118-119, registered 2026-08-29 before any vendor data request (REGISTRATION.md:3-8). BLOCKED-3 (`== 0`) and BLOCKED-5 (`< 20`) are counts too (REGISTRATION.md:100, 102). Every one of them is monotone in how many names are probed, so at any non-zero serving rate the verdict is a function of the sample size chosen by the measurer.
  - The sample size was chosen **after** a shortfall. First draw: 120 names, 81 served, `"registered_verdict_on_measured_count": "PARTIAL"` — `reports/stage_a1r/task6_delisted.json` (`alpaca` block: `names_with_intraday_history: 81`, `sample_size: 120`, `served_share: 0.675`). Second draw: "**So the sample was re-drawn inside the window and enlarged** ... **`n = 140` supplementary names**, combined with the 89 in-window names from the first pass: **`n = 229` checked, `203` served.**" — ORBExperiment/progress.md:1696-1699. At the in-window serving rate of 0.910 the enlargement guaranteed crossing 100.
  - What the gate was registered to protect against is a **share**, and the measured share is below 1: "**The combined A.1 TASK 4 verdict is the worst of the two**, because perfect cross-vendor agreement does not offset a survivor-only universe: a universe missing its delisted names inflates every downstream figure and is unrecoverable after the fact." — ORBExperiment/REGISTRATION.md:121-124. The measured in-window share is **0.8865** (`reports/stage_a1r/task6b_delisted_in_window.json`, `served_share`), i.e. about **11.35 percent of 4,731 in-window delisted names — on the order of 537 names — are expected to serve nothing**, and no registered threshold fires on that.
  - The reference vendor's own coverage of the same question is FAIL on the registered count (`reports/stage_a1r/task6_delisted.json`, `massive`: `names_with_intraday_history: 18`, `registered_verdict_on_measured_count: "FAIL"`), and its in-window answerable pool is 1,171 of 4,731 (DECISIONS.md:687). Neither figure appears in REGISTRATION.md, report.md or README.md.
- **Recomputation (if any):** 81/120 = 0.675 and 203/229 = 0.88646 reproduce the stored `served_share` values; 0.8865 × 4,731 = 4,194, leaving ≈537 in-window delisted names expected to serve nothing.
- **What would resolve it:** reporting the served **share** against a registered share bar, or recording in the Section 0 firing that the delisted verdict is a count bar whose crossing is a function of the number of names probed, with the residual 11.35 percent named as the survivorship exposure that remains after a PASS.
- **Confidence:** MEDIUM-HIGH. The facts are certain; the judgement that a count bar is the wrong instrument is mine, and the repository's stated reason for a count — "a rate measured on 20 names and multiplied by 4,731 is a synthesized value — standing rule 5 forbids one" (ORBExperiment/progress.md:1701-1703) — is a real and principled counter-argument. It explains why the *count* is reported; it does not explain why the *threshold* is a count.
- **Invalidated by later commits?:** no.
- **Disclosed by authors?:** substantially, which is why this is S3 and not higher. The re-draw is disclosed in full with its reason, and the reason is good — 31 of the first 120 sat outside the vendor's measured reach and 0 of those 31 served, aligning with the independently measured boundary (ORBExperiment/progress.md:1680-1694). The share 0.8865 is disclosed in README.md:195 and HYPOTHESES.md:70. Not disclosed: the first-pass PARTIAL and the Massive FAIL (both only in the JSON), and the scale-freeness of the bar.

---

### DRAFT-p1-registration-11
- **Repository / SHA:** ORBExperiment / f2aa675a80fc06b74979040b3028154d1add5ec0
- **Hypothesis or artifact:** Amendment 7 — the `SAME_TAPE` verdict, the branch that licenses the registered agreement thresholds to fire; and SL-1
- **Direction:** B
- **Class:** UNSUPPORTED_POSITIVE
- **Severity:** S3
- **Label:** DERIVED
- **Claim challenged (verbatim quote):** "**The verdict on the pair this experiment would use is `SAME_TAPE`. The registered agreement thresholds apply as written, and nothing in Section 0 is disapplied.**" — ORBExperiment/REGISTRATION.md:1491-1493
- **Evidence:**
  - The measurement is 20 tickers × 5 consecutive sessions: "**`n = 20` tickers × `5` sessions = `100` session-ticker pairs per comparison**" — ORBExperiment/REGISTRATION.md:1479-1481; sessions 2026-07-01 to 07-08 (REGISTRATION.md:1458-1459). The ticker list is in `reports/stage_a1r/task4_tape.json`: `AAPL, MSFT, NVDA, AMZN, GOOGL, META, TSLA, JPM, V, UNH, XOM, JNJ, WMT, PG, MA, HD, CVX, ABBV, KO, PEP` — the twenty largest US mega-caps.
  - The registered universe is not that population, and the repository argues the point forcefully when it suits the cost case: "The registered universe selects the top 20 names by **elevated opening relative volume** — that is, **the names with the most unusual activity in the first five minutes of the session**, which is precisely the population whose spreads are blown out at that moment. **The selection rule and the wide-spread population are the same population.** ... **The carried figure was an ETF's spread applied to news-driven single names at the one moment of the day they are least like an ETF.**" — ORBExperiment/REGISTRATION.md:4008-4015. A tape-agreement figure measured on twenty mega-caps is open to the same objection in the same words.
  - `n = 100` is 5 session clusters and 20 name clusters, not 100 independent observations. The repository registers that trades inside a session are not independent and builds E2's permutation on it (REGISTRATION.md:448-451, 534-536). The same standard is not applied to the 100 pairs.
  - The inference drawn from those same 100 clustered pairs is consequential and has no registered threshold: "**The two feeds appear to redistribute a common upstream, and the evidence is the tightness rather than the level.** The interquartile range ... is **[1.003096, 1.007726] — 0.46 percentage points wide, over 100 session-ticker pairs.** Two independently constructed consolidations of US equity activity would not agree to within half a percent with that consistency" — ORBExperiment/REGISTRATION.md:1543-1549. No null distribution for "how tightly two independent consolidations would agree" is computed or cited.
  - Consequence: `SAME_TAPE` is a gate-enabler — it is what allows `PASS ≥ 0.95 / PARTIAL ≥ 0.85 / FAIL` and BLOCKED-4 to fire on the pair at all (REGISTRATION.md:1433-1437).
- **Recomputation (if any):** none; the ticker list and the session list are read directly out of `reports/stage_a1r/task4_tape.json` (`tickers`, `sessions`, `ticker_count: 20`, `session_count: 5`) and `comparisons[0]`.
- **What would resolve it:** repeating the tape discriminator on a draw from the population the rule actually trades — names selected by the registered top-20 relative-volume rule on those same sessions, which the repository already has the machinery to select (`orb.dispersion._selections`) — and reporting the pair count by session cluster.
- **Confidence:** MEDIUM. The separation between a consolidated tape and a single-venue feed is ~36× (1.0052 against 0.0278), so the *verdict* is very unlikely to be sample-dependent; the finding is that the evidence offered for it, and for SL-1's shared-upstream inference, is drawn from a population the repository elsewhere insists is not the traded one, on clustered observations counted as independent.
- **Invalidated by later commits?:** no.
- **Disclosed by authors?:** partly. The sessions are named in Amendment 7 with a full justification of the window (REGISTRATION.md:1444-1464); progress.md:990 records the method as "a fixed list of 20 liquid tickers across 5 sessions"; the two controls are genuinely strong and are the best part of the amendment. What is nowhere raised is that the sample is not the registered universe, or that 100 pairs are 5 session clusters.

---

### DRAFT-p1-registration-12
- **Repository / SHA:** ORBExperiment / f2aa675a80fc06b74979040b3028154d1add5ec0
- **Hypothesis or artifact:** the post-holdout carve-out sample underlying every figure that closed H1 — dispersion 2.029585, trigger rate 0.982143, stop-exit share 0.381818, the measured band and the shift 0.467065; and the Amendment 22 restatement of H-ORB built on it
- **Direction:** B
- **Class:** STATISTICAL
- **Severity:** S3
- **Label:** DERIVED
- **Claim challenged (verbatim quote):** "**The universe is a price-blind systematic sample**, not the alphabetically-first names the probe slice used. The reference vendor's active US common-stock listing was walked in full by cursor — **`n = 5,317` names over 6 pages** — and **every 26th ticker** taken, `n = 200`" — ORBExperiment/REGISTRATION.md:2568-2571; and the conclusion built on it, "**The condition selects on almost nothing. What carries whatever information exists is the direction of the first excursion**" — ORBExperiment/REGISTRATION.md:3512, 3517-3519
- **Evidence:**
  - **A rank-tail dilution of the selection, uncorrected.** Every figure above comes from applying the registered "rank descending on opening relative volume; **take the top 20**" (REGISTRATION.md:265) to a pool of at most 199 names with bars (`tickers_with_bars: 199`, `reports/stage_a1amend/task5c_dispersion_e2.json`), i.e. roughly the top 10 percent, where the registered rule selects the top 20 of a full delisted-inclusive universe — the scan's own note puts that universe at **26.6 times larger** (REGISTRATION.md:3909), so the registered selection is roughly the top 0.4 percent.
  - The registration states the mechanism and then measures it, without ever applying it to this sample: "the top-20 selection is a **rank statistic**: ranking 20 out of a smaller pool selects a **less extreme** relative-volume tail" (REGISTRATION.md:3811-3812); "**The mean relative volume of the selection falls 2.0652 → 1.4103**" (REGISTRATION.md:3890-3891). **The measured mean relative volume of the selection that produced H1's deciding numbers is 2.0652** (`reports/stage_a3rescue/task4_floor_scan.json`, 5 USD row, `mean_relative_volume_of_selection`) — barely twice a name's own median first-five-minute volume, for a rule whose selection half the repository describes as picking "the names with the most unusual activity in the first five minutes of the session" (REGISTRATION.md:4009-4010).
  - The registration also states the transfer rule it breaks: "**H1's power figures do not transfer**: the dispersion, the trades per session and the trigger rate all change with the universe." — ORBExperiment/REGISTRATION.md:3835-3836.
  - **A survivorship screen preceding the measurement, uncorrected.** The listing walked is the **active** listing as of the pull date (REGISTRATION.md:2569). Section 2 registers the opposite requirement for the experiment's universe: "**Delisted tickers are included for every historical session in which they traded.** A survivor-only universe inflates every downstream figure and is unrecoverable after the fact." — ORBExperiment/REGISTRATION.md:282-285. Over the 2026-07-01 to 2026-08-28 window the exposure is small (the repository's own per-year delisting counts, `reports/stage_a1r/task6_delisted.json` `per_year`, run 437-704 names/year against a 5,317-name active listing), but it is an uncorrected screen sitting in front of every carve-out figure and it is never named.
  - Why it bites hardest on the restatement rather than on the closure: the trigger rate 0.982143 is what moved the registration to restate H-ORB (Section 1.1, REGISTRATION.md:211-233) and to narrow what a positive verdict could ever claim (Section 11.2, REGISTRATION.md:700-717). Those are registered document changes made on a measurement of a selection that is not the registered selection.
- **Recomputation (if any):** `reference_pool_size: 5317`, `universe_stride: 26`, `tickers_sampled: 200`, `tickers_with_bars: 199`, `sessions_evaluable_after_trailing_window: 28`, `name_sessions_evaluated: 560` — all from `reports/stage_a1amend/task5c_dispersion_e2.json`. 560 = 28 × 20 exactly, so the rule filled its top 20 from a pool of ≤199 on every session; 5,317/200 = 26.6.
- **What would resolve it:** a second carve-out pull on the full active listing (or a much larger stride sample) reporting the selection's mean relative volume, and a statement of which direction each carve-out figure would move under a more extreme selection tail. On the repository's own reasoning at REGISTRATION.md:4008-4015 the slippage band and the dispersion would both rise, which would make the closure stronger — that should be said rather than left unexamined.
- **Confidence:** MEDIUM-HIGH on the facts and on the dilution's existence; LOW-MEDIUM on its size, which nobody has measured.
- **Invalidated by later commits?:** no.
- **Disclosed by authors?:** partly, and the partial disclosure is careful. The sample is named as "a **200-name systematic sample of a 5,317-name listing**, in a **post-holdout regime**. **It is not the in-sample trigger rate and this amendment does not claim it is**" (REGISTRATION.md:2657-2659), the word "active" appears in the universe description, and Amendment 11's regime caveat travels with every E2 figure. Not disclosed: that the top-20 selection drawn from 199 names is a materially less extreme relative-volume tail than the registered rule's, that the repository measures that very effect two amendments later, or that the sampling frame is survivor-only against a Section 2 requirement that it not be.

---

## What I checked and found sound

This repository survives most of the B thesis. The following are places where I expected, on the thesis,
to find an over-claim and did not.

1. **The pre-committed rescue criterion is genuine, and the git order holds.** REGISTRATION.md:3666-3675 and
   report.md:879-883 claim Amendment 24 "was written, committed and pushed as `4ae14dc` before a single line of the
   measuring tool existed". Verified read-only on the live repository: `git ls-tree -r --name-only 4ae14dc` contains no
   `slippage_band.py`, `rescue_verdict.py` or `floor_scan.py`; `git log --diff-filter=A -- tools/slippage_band.py`
   returns **5899e1b**, 27 minutes and four commits later; `git log -S 'measure_carve_out_slippage_band' -- src/orb/dispersion.py`
   returns the same commit. The criterion, the `NOT_RESCUED` consequence and the arithmetic ruling `GO` out predate the
   measurement. This is the load-bearing provenance claim in the repository and it is true.
2. **The multiplicity correction is statistically right, and it was not used as a rescue.** Amendment 18 replaces a Šidák
   union correction with the Berger (1982) intersection-union argument (REGISTRATION.md:3028-3036). For an IUT that rejects
   only when every component rejects, size ≤ α per component is correct and no correction is owed. The change was made
   while a 131-session shortfall was on the record and it moved E1 from 0.743521 to 0.832450 across its own 0.80 floor —
   textbook grounds for suspicion — but the same pass replaced E2 with a harder null (Amendment 19), pre-registered what a
   collapse would mean *before* the shift was measured (REGISTRATION.md:3233-3246), and the net effect on the design was
   catastrophic rather than favourable (joint power 0.043277). The repository also forbids the reading that would have
   flattered it: "**A reader must not take 0.832450 as the design's power.**" (REGISTRATION.md:3106-3107).
3. **Joint power is reported as the operative figure, not a component.** Section 10.1 restates the latch clause on joint
   power (REGISTRATION.md:583) and `orb.power.joint_power` returns the unconditional upper bound with the binding
   component named (src/orb/power.py:204-220). README.md:268-271 and REGISTRATION.md:3377-3384 report E1, E2 and JOINT
   in the same table. I looked for E1's 0.832450 being quoted alone as the design's power and did not find it in
   REGISTRATION.md, HYPOTHESES.md or report.md.
4. **The intrabar lower-bound disclosure is correct and runs against the repository's interest.** 457 of 550 entry
   triggers and 195 of 210 stop triggers crossed intrabar and were recorded at 0.0 overshoot, so the measured band is a
   lower bound on cost and any power computed on it an upper bound (REGISTRATION.md:4040-4051, src/orb/dispersion.py:830-839).
   The repository states this where it hurts and draws the right conclusion from it.
5. **The E2 = E1 equality was diagnosed as a design fault, not papered over.** Amendment 15 §6 derives `σ√k` cancellation
   analytically (REGISTRATION.md:2692-2698) and Amendment 19 replaces the co-primary rather than reparameterising it. I
   recomputed the E2 power figures (0.043277 at 17,188 trades; 0.000000 under the measured band) and the break-even
   Sharpe 1.437035 and stop share 0.346206 from the stored primitives; all reproduce.
6. **The cost model refuses rather than guesses.** `SEC_FEE_SCHEDULE` is empty because the rate's effective date was not
   measured, so 550 of 550 trades are refused and the registered figure is `Absent` (REGISTRATION.md:2596-2612). The
   bracket used instead varies the one unmeasured component across both ends and comes out 0.0084 percent wide
   (REGISTRATION.md:2619-2629) — a measurement, as claimed.
7. **The registered cost band, the effect assumption, the alpha and the stop share were not moved after the null.**
   REGISTRATION.md:3434-3449 and 4124-4138 list what was available and not done; `CONFIG`'s slippage tuples are unchanged
   (REGISTRATION.md:4053-4056) and `src/orb/section0.py` is stated byte-identical across two passes (REGISTRATION.md:2920,
   3659-3660). The measured band is recorded beside the registered one rather than replacing it.
8. **H1b's multiplicity cost is paid rather than hidden**, and the scan is walled off from H1's outcome in advance
   (REGISTRATION.md:3740-3748, 3816-3828). The trial count moves 8 → 9 for H1b only, for the stated reason that the
   filter change was proposed after seeing a null.
9. **The falsified planning figures are recorded as falsified, in the direction that costs something** — the 0.55 trigger
   rate (REGISTRATION.md:2635-2652), the stale FINRA TAF rate and three unmodeled cost components, all of which make the
   model more expensive (REGISTRATION.md:1028-1032), the 88.4/min unauthenticated ceiling that overstated the real one by
   17.7× (REGISTRATION.md:1737-1745), the 134.05/min figure falsified at 223.16 (REGISTRATION.md:2445-2449), and the
   `docs/ACCESS.md` primary-vendor recommendation superseded by measurement (REGISTRATION.md:1636-1649).
10. **Two scope limitations are registered before the figures they would excuse.** SL-1 (the feeds share an upstream, so a
    cross-vendor PASS "is **not** the Concretum test") and SL-2/SL-3 (the gate covers 459 of 2,637 sessions and none of
    the in-sample window) are written before the agreement share exists (REGISTRATION.md:1551-1572, 640-698). These make
    the repository's own eventual PASS weaker, which is the opposite of the B thesis.
11. **The priors are not retro-scored.** Amendment 28 §6 declines to score either prior because "the event both priors
    were about **did not resolve**" (REGISTRATION.md:4175-4181) — the honest answer, and the one that forgoes a
    calibration win.
12. **The register's own arithmetic reproduces.** I recomputed, from stored primitives: the carried shift 0.041455 and the
    measured shift 0.467065 (both exact), the central mean 0.040386, E2 power 0.043277, the break-even Sharpe 1.437035
    and the 2.577 percent gap, the required pessimistic mean 0.038493 and the 21.89-fold reduction, and all five floor-scan
    central means. Every one matches the document to the digits given. The only arithmetic slip I found is
    DRAFT-p1-registration-7.
13. **The cross-application of the QQQ per-share gross edge (C-6, 0.070/share) to a 50 USD single name** — Amendment 3's
    "a close exit consumes **55 percent** of it and **a stop exit consumes 98 percent**" (REGISTRATION.md:1082-1083) and
    Amendment 15 §7's "uncomfortable number" table — mixes per-share quantities across instruments at very different price
    levels, which Amendment 25 §3 later says do not transfer. I checked the direction: converting properly makes the edge
    *smaller* relative to cost, so the error runs **against** the repository's own conclusion and understates the problem
    it is used to illustrate. It is labelled "a cross-application, and labelled as one" (REGISTRATION.md:2711) and the table
    is explicitly not verdict-bearing (REGISTRATION.md:2731-2733). No finding raised.
14. **Section 0's branches were never edited to fit a result.** The five verdicts, their thresholds and their precedence are
    unchanged from the first commit; the two states added (PENDING_ACCESS, PENDING_REVISION) are each pinned by a test that
    makes them inert once the measurements exist (REGISTRATION.md:942-946, 1927-1929). Amendment 23 records that
    BLOCKED-1 *would* have fired on joint power and deliberately does not change the branch to make it (REGISTRATION.md:3638-3651) —
    an observation recorded against the repository's interest.

## Live-repo access log

**Before** (`git -C /home/kiros-li/Documents/GitHub/ORBExperiment status --porcelain`, 2026-09-12T18:13:59Z):

```
```
(empty — clean working tree)

**After** (same command, 2026-09-12T18:19:48Z):

```
```
(empty — clean working tree)

`git -C /home/kiros-li/Documents/GitHub/ORBExperiment rev-parse HEAD` = `f2aa675a80fc06b74979040b3028154d1add5ec0`,
identical to the anchored SHA. Commands used, all read-only: `status --porcelain`, `rev-parse`, `log --format`,
`log -S <string> -- <path>`, `log --diff-filter=A -- <path>`, `show --stat`, `ls-tree -r --name-only`, `remote -v`,
`for-each-ref`. No checkout, stash, reset, add, commit, branch or worktree command was issued, and nothing was written
into the audited repository. Unanchored data read: none — every artifact I cite is tracked at the anchored SHA and was
read from SNAP.
