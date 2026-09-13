# Agent A draft findings — ORBExperiment, part p1-registration

**Repository:** ORBExperiment · **anchored SHA:** `f2aa675a80fc06b74979040b3028154d1add5ec0` (main, 2026-08-29 20:46:22 -0700)
**Assigned documents:** `REGISTRATION.md` (4,193 lines, read in full), `HYPOTHESES.md` (175 lines, read in full), `report.md` (1,080 lines, read in full).
**Supporting reads (context, not primary):** `docs/HANDOVER.md`, `DECISIONS.md` ADR-038, `src/orb/dispersion.py`, `src/orb/signal.py`, `src/orb/universe.py`, `src/orb/costs.py`, `src/orb/sessionclock.py`, `src/orb/calendar.py`, `tools/slippage_band.py`, `reports/stage_a3rescue/*.json`.
**Recomputation script:** `/home/kiros-li/.cache/program-audit/scratchpad/work/agentA-ORB-p1/final.py` (venv python, numpy not required).

**Reproduction check before any finding.** Every published deciding figure was
recomputed from the repository's own stated primitives and agrees to five or six
decimal places: measured shift **0.467065** (repo 0.467065), carried-band shift
**0.041455** (repo 0.041455), E2 power at the registered 1.40 under the carried
band **0.043279** (repo 0.043277), E2 power at the published 2.81 under the
carried band **0.819517** (repo 0.819524), central mean at 1.40 **0.040386**
(repo 0.040386), break-even stop-exit share **0.346206** (repo 0.346206). **The
arithmetic in this repository is not in dispute. What is in dispute is what two
of the six measured band ends actually measure.**

The E2 power function recovered from the repository's own numbers is
`E2 = Phi(m * sqrt(17188) / 2.029585 − 1.6448536)`, where `m` is the
pessimistic-cost mean per share; it reproduces 0.043277 at m = −0.001068 and
0.819524 at m = +0.039606, so every recomputation below uses the repository's own
estimator, not a substitute.

---

### DRAFT-p1-registration-1
- **Repository / SHA:** ORBExperiment / f2aa675a80fc06b74979040b3028154d1add5ec0
- **Hypothesis or artifact:** H1 (H-ORB) — the closure `cost-bound`, Amendment 28; specifically the **close-exit leg** of the measured slippage band, Amendment 26 §3
- **Direction:** A
- **Class:** ARITHMETIC
- **Severity:** S1
- **Label:** DERIVED
- **Claim challenged (verbatim quote):** "| **close** | official print against the 15:59 close | 0.099324 | **0.040000** | **0.261000** | **340**, 0 without an official print |" — ORBExperiment/REGISTRATION.md:3996
- **Evidence:** The close-exit "slippage" is computed as `close_slippage.append(abs(row.official_close_c - row.last_exit_window_close_c) / CENT)` — ORBExperiment/src/orb/dispersion.py:943-945. `last_exit_window_close_c` is `close_exit_c(inside, (exit_start_ms, exit_end_ms))` — ORBExperiment/src/orb/dispersion.py:388 — which returns "The close of the last bar inside the registered exit window" — ORBExperiment/src/orb/signal.py:176, over the half-open window `[start, end)` — ORBExperiment/src/orb/signal.py:179. The window is `CLOSE_EXIT_START = time(15, 55, 0)` to `CLOSE_EXIT_END = time(15, 59, 0)` — ORBExperiment/src/orb/sessionclock.py:39,42 — so this is the close of the **15:58** minute bar, and it **is the registered exit price**: "**Exit.** The **session close**, modeled in the window **15:55:00 to 15:59:00 Eastern**" — ORBExperiment/REGISTRATION.md:314-315. `official_close_c` is the close of the **earliest** bar in `[exit_end_ms, exit_end_ms + 120_000)` — ORBExperiment/src/orb/dispersion.py:389-394 — i.e. the **15:59** minute bar, not the 16:00:00 closing-auction print. **So the quantity charged as the close-exit transaction cost is the absolute value of a one-minute price change between two consecutive bar closes (15:58 close to 15:59 close), for a leg whose registered fill price is the 15:58 close.** The code states the substitution as fact: "A real market-on-close order fills at the official closing print, and the gap between them is the close leg's realized slippage" — ORBExperiment/src/orb/dispersion.py:385-387 — but Section 3 registers no market-on-close order, and the value taken is not the closing print either. Two consequences: (a) the registered exit pays no such gap, and (b) `abs()` converts a roughly zero-mean price change into a strictly positive charge, which is not defensible on a book that is **47.5 percent short** (long-only trigger rate 0.525, n = 560 — ORBExperiment/REGISTRATION.md:2643): for a given sign of the last-minute move, half the positions gain what the other half lose. n = 340 close exits (ORBExperiment/REGISTRATION.md:3996). Contribution to the deciding shift: **0.136618 USD/share, 29.3 percent** — ORBExperiment/REGISTRATION.md:4026.
- **Recomputation (if any):** Inputs: measured close band (0.040000, 0.261000) — REGISTRATION.md:3979-3980; stop-exit share 0.381818, n = 550 — REGISTRATION.md:3274; measured stop **half spread** median 0.031934 / p90 0.182336, n = 210 served, 0 refused — REGISTRATION.md:3994. Method: replace the close leg's benchmark-difference band with the only genuine transaction-cost band the pass measured (the stop leg's time-weighted quoted half spread), recompute `shift = (e_p−e_c) + s(s_p−s_c) + (1−s)(c_p−c_c)`, then `E2 = Phi(m·sqrt(17188)/2.029585 − 1.6448536)`. Result: **shift falls 0.467065 → 0.423423** (variant B, final.py). The tier does **not** flip on this correction alone (0.423423 is still far above 0.040386), but the published figure overstates the deciding number by **0.043642 USD/share, 9.3 percent**, and the mis-measurement is of kind, not of degree.
- **What would resolve it:** Re-measure the close leg as a transaction cost — the time-weighted quoted half spread over the registered 15:55–15:59 exit window (the same instrument the pass already used for the entry and stop legs, at 760 quote minutes served and 0 refused), or the signed (not absolute) deviation of the auction print from the registered exit price, taken with the position's side. The quotes endpoint is already entitled and the sealed bars are already on disk; the re-measurement costs one pull of exit-window quote minutes.
- **Confidence:** HIGH — the formula, the window constants and the registered exit price are all read directly from source, and the arithmetic consequence is reproduced.
- **Invalidated by later commits?:** no — the live repository's HEAD is the anchored SHA `f2aa675` with a clean working tree (checked 2026-09-04; see access log), so no later commit exists.
- **Disclosed by authors?:** no — Amendment 26 §3 names the row "official print against the 15:59 close" (REGISTRATION.md:3996) but never states that the value is an absolute price difference between two bar closes, that the later of the two is not the auction print, or that the registered exit is the earlier one. Amendment 26 §7's disclosed limitation is a different one (intrabar overshoot as a lower bound, REGISTRATION.md:4042-4046) and points the other way.

---

### DRAFT-p1-registration-2
- **Repository / SHA:** ORBExperiment / f2aa675a80fc06b74979040b3028154d1add5ec0
- **Hypothesis or artifact:** H1 (H-ORB) — the **entry leg** of the measured slippage band, Amendment 26 §2–§3, and its inconsistency with the registered Section 3 entry order
- **Direction:** A
- **Class:** INTERNAL_INCONSISTENCY
- **Severity:** S2
- **Label:** DERIVED
- **Claim challenged (verbatim quote):** "| entry, pessimistic | 0.0400 | **0.354645** | **8.87×** | **UNDERSTATED** |" — ORBExperiment/REGISTRATION.md:3976
- **Evidence:** Section 3 registers the entry as a **price-capped limit order**: "Modeled as a **marketable limit at the range boundary plus 0.05 percent of price** (5 basis points), in the direction of the break." — ORBExperiment/REGISTRATION.md:302-304. It is implemented as such: `entry_offset_fraction=0.0005` — ORBExperiment/src/orb/config.py:245, documented "0.0005. Marketable limit at the range boundary plus 5 bp of price." — ORBExperiment/src/orb/config.py:90 — and applied as `offset = boundary_c * CONFIG.entry_offset_fraction; return boundary_c + max(1, int(offset + 0.9999999))` — ORBExperiment/src/orb/signal.py:93-96. **A limit order cannot fill worse than its limit**, so entry slippage relative to the boundary is bounded above by `max(0.01, 0.0005 × price)` USD/share by construction of the registered rule. The band tool nevertheless charges `overshoot + the full time-weighted quoted half spread across the whole trigger minute` — `entry_slippage.append(overshoot + half)` — ORBExperiment/src/orb/dispersion.py:902, with `half` from `_time_weighted_half_spread(payload, row.trigger_ms, row.trigger_ms + 60_000)` — ORBExperiment/src/orb/dispersion.py:889-896 — i.e. the cost of an **unbounded market order**, averaged over sixty seconds rather than taken at the fill instant. The registered universe filter is only "session open | **above 5.00 USD**" — ORBExperiment/REGISTRATION.md:273. Contribution to the deciding shift: **0.267626 USD/share, 57.3 percent** — ORBExperiment/REGISTRATION.md:4024.
- **Recomputation (if any):** Inputs: entry offset fraction 0.0005 (src/orb/config.py:245), measured entry total slippage median 0.087019 and p90 0.354645, n = 550 (REGISTRATION.md:3992). Method: solve for the share price at which the registered limit's own cap equals each measured end. Result: the registered marketable limit permits an entry slippage of **0.087019 USD/share only on a name priced at or above 174.04 USD**, and of **0.354645 USD/share only at or above 709.29 USD**; for comparison the *registered* entry pessimistic of 0.040 corresponds to 80.00 USD. Capping the entry leg at the registered limit (which collapses both ends to the cap, and therefore the entry shift to zero, for any name priced at or below 174.04 USD) moves the deciding shift **0.467065 → 0.199440** (variant C, final.py). As with finding 1 the tier does not flip on this correction alone; the point is that **57.3 percent of the deciding number is a cost the registered order type cannot incur.**
- **What would resolve it:** Either (a) re-measure the entry leg as the registered order actually behaves — the realized fill price against the boundary, capped at boundary + 5 bp, with unfilled triggers recorded as missed trades rather than as costed ones (this needs the trade tape, see finding 9); or (b) register an amendment replacing the Section 3 marketable limit with a plain market order, and re-derive Section 6's band and the rescue criterion against it.
- **Confidence:** HIGH on the inconsistency (both sides read from source and registration); MEDIUM on its size, because the share of selected name-sessions priced below 174.04 USD is not reported anywhere and the missed-fill counterfactual is not free — an unfilled limit is a missed trade, not a zero-cost trade, and this repository has never measured how often the price traded back through the limit.
- **Invalidated by later commits?:** no — HEAD is the anchored SHA with a clean tree.
- **Disclosed by authors?:** no — Amendment 24 §2 describes the entry as "a marketable order" and treats the full quoted spread as a floor on its cost ("The lower bound on entry slippage alone — the quoted spread a marketable order crosses — is of the order of one cent on a liquid single name", ORBExperiment/REGISTRATION.md:3704-3706), which is precisely the substitution at issue; the 5 bp limit is not mentioned anywhere in Amendments 24, 26 or 28.

---

### DRAFT-p1-registration-3
- **Repository / SHA:** ORBExperiment / f2aa675a80fc06b74979040b3028154d1add5ec0
- **Hypothesis or artifact:** H1 (H-ORB) — the rescue criterion of Amendment 24 §3 applied to a band whose *shape* is not the shape the criterion's threshold was derived against
- **Direction:** A
- **Class:** OVER_CLOSED
- **Severity:** S2
- **Label:** DERIVED
- **Claim challenged (verbatim quote):** "**`RESCUED_DEGRADED`** — the TASK 2 measured shift falls **strictly below** **0.040386**" — ORBExperiment/REGISTRATION.md:3711-3712
- **Evidence:** The threshold 0.040386 is the implied central mean per share at the registered 1.40 Sharpe assumption (REGISTRATION.md:3694). The quantity compared against it — the "shift" — is by definition the *width* of the cost band, `pessimistic − central`, mixed on the stop-exit share (`orb.costs.CostModel.mean_slippage_shift_per_share`, REGISTRATION.md:3175-3182). **Section 6's registered band has a pessimistic end that is exactly 2× its central end on every leg**: entry 0.020/0.040, stop 0.040/0.080, close 0.010/0.020 — ORBExperiment/REGISTRATION.md:388-392, restated unmoved at REGISTRATION.md:4055-4056. **The measured band replaces that 2× scenario with an empirical p90-over-median mapping whose ratios are 4.075 (entry), 5.907 (stop) and 6.525 (close)** — computed from REGISTRATION.md:3975-3980. The mapping was pre-committed ("median → central, 90th percentile → pessimistic", REGISTRATION.md:3998-3999, ADR-038 at DECISIONS.md:1439-1444), so it is not a post-hoc choice; but it silently changes what "pessimistic" *means* by a factor of 2 to 3.3, while the pass/fail threshold it is compared against was fixed against the 2× shape. It also converts a bounded robustness scenario into a joint tail: every one of 17,188 trades is charged the 90th percentile of its leg's distribution simultaneously.
- **Recomputation (if any):** Inputs: measured **central** levels entry 0.087019 / stop 0.033529 / close 0.040000 (REGISTRATION.md:3975,3977,3979); registered band shape pessimistic = 2 × central (REGISTRATION.md:388-392); stop share 0.381818 (REGISTRATION.md:3274); dispersion 2.029585, 19.642857 trades/session, 875 sessions → 17,188 trades (REGISTRATION.md:3373-3375); alpha 0.05 one-sided (REGISTRATION.md:3043). Method as in the header. Results (final.py): **E** measured central levels with the registered 2× shape → shift **0.124549**, still NOT_RESCUED. **F** = E plus the entry leg capped at the registered 5 bp limit (finding 2) → shift **0.037529 < 0.040386**, pessimistic-cost mean **+0.002857**, **E2 power 0.072103 at 1.40 and 0.878417 at 2.81 — the tier flips to `RESCUED_DEGRADED`**. **G** = F with the close leg also taken as a half-spread (finding 1) → shift **0.032543**, E2 power **0.127517** at 1.40 and **0.931784** at 2.81, again `RESCUED_DEGRADED`. **So NOT_RESCUED survives each of the three objections taken singly and does not survive them taken together.** The same two corrections also break Amendment 28 §3's strengthening claim: at the published 2.81 the pessimistic-cost mean is **+0.043532** under F rather than −0.386004, and E2 power is **0.878417** rather than 0.000000.
- **What would resolve it:** Report the deciding shift under both band shapes side by side — the discipline this repository applies to E1 (every figure beside its predecessor, REGISTRATION.md:3077-3084) and to the 2.81 row of Amendment 28 §3 (REGISTRATION.md:4110-4113) — and state which shape the pre-committed threshold was derived against. If the p90/median mapping is kept, re-derive the RESCUED_DEGRADED threshold for a band of that shape rather than reusing the one calibrated on a 2× band.
- **Confidence:** MEDIUM — variants F and G each require two simultaneous corrections, and one of them (finding 2's entry cap) has an unmeasured counterfactual (missed fills). The single-correction result — that NOT_RESCUED survives each objection alone — is HIGH confidence and is reported here as such.
- **Invalidated by later commits?:** no — HEAD is the anchored SHA with a clean tree.
- **Disclosed by authors?:** partly — Amendment 26 §8 discloses that the registered band is not moved (REGISTRATION.md:4055-4058) and Amendment 28 §3 reports the carried-band figure beside the measured one **at 2.81 only** (REGISTRATION.md:4110-4113). Nowhere is the change in the band's pessimistic-to-central *ratio* named, and nowhere is the carried-band figure reported beside the measured one at the registered 1.40 assumption, which is the row the criterion is evaluated on.

---

### DRAFT-p1-registration-4
- **Repository / SHA:** ORBExperiment / f2aa675a80fc06b74979040b3028154d1add5ec0
- **Hypothesis or artifact:** H1 (H-ORB) — the headline "E2 power 0.000000, JOINT power 0.000000" of Amendment 28
- **Direction:** A
- **Class:** INTERNAL_INCONSISTENCY
- **Severity:** S2
- **Label:** DERIVED
- **Claim challenged (verbatim quote):** "**The pessimistic-cost mean is −0.426679 USD per share. E2 power is 0.000000. Joint power is 0.000000. No session count reaches 80 percent at any assumption.**" — ORBExperiment/REGISTRATION.md:4084-4086
- **Evidence:** E2 is defined by amendment against the *registered* band: "**E2 tests whether mean net PnL per trade remains above zero when every slippage leg is set to the pessimistic end of the band registered in Section 6.**" — ORBExperiment/REGISTRATION.md:3158-3159. The same rescue pass then declines to re-register the band: "**`CONFIG.entry_slippage`, `stop_slippage` and `close_slippage` are unchanged** at (0.010, 0.020, 0.040), (0.020, 0.040, 0.080) and (0.005, 0.010, 0.020). **This amendment records a measurement beside them; it does not re-register them.**" — ORBExperiment/REGISTRATION.md:4055-4058. **So the E2 power of 0.000000 and the joint power of 0.000000 are computed against a band that is not the band E2 is registered on.** Under the band E2 *is* registered on, the figures are those of Amendment 21 and they are unchanged: pessimistic-cost mean **−0.001068 USD/share**, **E2 power 0.043277**, joint power 0.043277, and the design sits **2.577 percent** below its own break-even Sharpe of 1.437035 — ORBExperiment/REGISTRATION.md:3360-3365, 3419-3422. The difference between the two is the difference between a design that missed by a hair and one that missed by 400 times the margin, and the second is what is carried forward as the repository's headline: "| **E2 power** at 1.40 / 2.81 / 0.70 | **0.000000 / 0.000000 / 0.000000** | 875 |" — ORBExperiment/docs/HANDOVER.md:63 (primary evidence outside my assignment), and "**E2 power 0.000000. JOINT power 0.000000.**" — ORBExperiment/HYPOTHESES.md:59.
- **Recomputation (if any):** Inputs as above. Method: evaluate the repository's own E2 estimator at both bands. Result (final.py, variants A and H): registered band → shift 0.041455, m = −0.001068, **E2 = 0.043277**; measured band → shift 0.467065, m = −0.426679, **E2 = 0.000000**. Both reproduce the repository's published values, which is the point: **both are the repository's own numbers and only one of them is E2 as registered.**
- **What would resolve it:** Report the registered-band E2 power (0.043277) beside the measured-band figure at every assumption in Amendment 28 §2, exactly as Amendment 28 §3 already does at 2.81 alone; or amend E2's definition to name the measured band, which would require moving the band that Amendment 26 §8 declines to move.
- **Confidence:** HIGH — both definitions are quoted verbatim from the same document and the two numbers are the repository's own.
- **Invalidated by later commits?:** no — HEAD is the anchored SHA with a clean tree.
- **Disclosed by authors?:** partly — Amendment 28 §5 lists both "the registered Section 6 cost model and its pessimistic band" and "a slippage band measured on 42 post-holdout sessions" as things the closure rests on (REGISTRATION.md:4145-4152), and Amendment 26 §8 says the registered band is unmoved. But the consequence — that the published E2 and joint powers are not the registered E2's — is never stated, and the registered-band figure at 1.40 is not carried into the closure record.

---

### DRAFT-p1-registration-5
- **Repository / SHA:** ORBExperiment / f2aa675a80fc06b74979040b3028154d1add5ec0
- **Hypothesis or artifact:** H1 (H-ORB) — the closure **kind** `cost-bound`
- **Direction:** A
- **Class:** OVER_CLOSED
- **Severity:** S2
- **Label:** READ
- **Claim challenged (verbatim quote):** "**H1 closes as `cost-bound`: the effect may be real; it does not survive the modeled cost.**" — ORBExperiment/REGISTRATION.md:4142-4143
- **Evidence:** `cost-bound` is defined in the register as "The effect may be real; it does not survive the modeled cost." with precedent "MLCryptoEngine H6 — per-fill positive, negative under an order-lifecycle fill model" — ORBExperiment/HYPOTHESES.md:36. That precedent is a **measured PnL** that changed sign under a fill model. **This repository has no PnL of any kind.** Its own closing text says so twice: "**No in-sample or holdout bar was ever read. Both latches remain absent.** **Nothing in this repository measured whether the directional edge is real.**" — ORBExperiment/report.md:1018-1020 — and "**It is a finding that this design cannot clear its own registered cost band**, which is a statement about the design." — ORBExperiment/REGISTRATION.md:4162-4163. The register already carries the kind that describes exactly that: "**untestable-at-achievable-power** | The design's own arithmetic blocks it before any data exists." — ORBExperiment/HYPOTHESES.md:39 — and Amendment 21 offered it as a named route: "**Close H1 as `untestable-at-achievable-power` under its own registered cost assumptions.** This is a **legitimate documented closure** and it is the **fourth closure kind already named in `HYPOTHESES.md`**." — ORBExperiment/REGISTRATION.md:3468-3470. The deciding quantity is a **power** (E2 power 0.000000, joint 0.000000, "no session count reaches 80 percent") and not a return; the closure is therefore a statement about detectability, which is the fourth kind, not the first.
- **Recomputation (if any):** none needed — the deciding quantity is a power figure by inspection of Amendment 28 §1-§2 (REGISTRATION.md:4079-4100); no realized net PnL exists anywhere in the repository (`data/state/` holds no `stage_c_read.json` and no `stage_d_read.json`, REGISTRATION.md:4074-4075).
- **What would resolve it:** Re-type the closure as `untestable-at-achievable-power` (or record explicitly why `cost-bound` is preferred despite no outcome value existing), and carry the difference into the reopen condition: the fourth kind names a route back (more power, or a narrower measured band), the first reads as a settled fact about returns.
- **Confidence:** HIGH — the mismatch is between two definitions quoted from the repository's own register, and the repository states the underlying fact itself.
- **Invalidated by later commits?:** no — HEAD is the anchored SHA with a clean tree.
- **Disclosed by authors?:** partly — the repository states plainly that no bar was read and that the finding is about the design (report.md:1017-1022; REGISTRATION.md:4159-4163), and Amendment 21 route 3 named the alternative kind. It does not record why the kind actually applied is `cost-bound` rather than the one its own sentence describes. Under the common rules this makes the finding READ and capped at S3 on the disclosure of the *fact*; it is filed S2 because the mismatch between the applied label and the disclosed fact is itself undisclosed.

---

### DRAFT-p1-registration-6
- **Repository / SHA:** ORBExperiment / f2aa675a80fc06b74979040b3028154d1add5ec0
- **Hypothesis or artifact:** H1 (H-ORB) — the absence of a registered reopen condition on a closed entry
- **Direction:** A
- **Class:** PROCESS
- **Severity:** S3
- **Label:** READ
- **Claim challenged (verbatim quote):** "A closed entry carries the figure that closed it, with its n, and states what would reopen it — or states that nothing would." — ORBExperiment/HYPOTHESES.md:7-9
- **Evidence:** H1's register entry runs 30 table rows — ORBExperiment/HYPOTHESES.md:56-87 — and **none of them is a reopen condition**. The rows are: Status, deciding numbers, pre-committed criterion, "does NOT rest on the halving heuristic", "what the closure rests on", "what the closure is NOT", calibration ledger, superseded status, two Section 0 verdict rows, measured trigger rate, superseded verdict, what this resumption measured, power, cost model, registration, joint claim, registered bars, power assumption, registered shortfall, what decides this repository, registered scope limits, SL-3, restatement, inference repair, priors, calibration eligibility, latch, working. The nearest thing to a reopen route is prose inside the "what the closure rests on" row — "**The honest attack is (2): real execution evidence could narrow the band.**" (HYPOTHESES.md:62) — which names an attack, not a trigger, and is not phrased as a condition that would reopen anything. The only place a reopen route is stated as such is `docs/HANDOVER.md`:272-275, outside the register: "**(d) Pursue Amendment 21 route (b)** — narrow the registered cost band on **real execution evidence**. ... It is the only route that could reopen a cost-bound closure" (primary evidence outside my assignment). The register's own rules section adds no reopen rule either — "**A closure is typed** with one of the five kinds above." — ORBExperiment/HYPOTHESES.md:173.
- **Recomputation (if any):** none.
- **What would resolve it:** Add a reopen-condition row to H1 in `HYPOTHESES.md` with a threshold and a trigger — e.g. "reopens if a measured effective-spread band on the registered universe puts the pessimistic-cost mean at 1.40 above zero" — or the register's explicit alternative, a row stating that nothing would reopen it.
- **Confidence:** HIGH — the rule and the entry are in the same 175-line file and the row is simply absent.
- **Invalidated by later commits?:** no — HEAD is the anchored SHA with a clean tree.
- **Disclosed by authors?:** no — the file states the rule it does not follow for its own only closed entry.

---

### DRAFT-p1-registration-7
- **Repository / SHA:** ORBExperiment / f2aa675a80fc06b74979040b3028154d1add5ec0
- **Hypothesis or artifact:** H1 (H-ORB) — a registered variant family (the 15, 30 and 60-minute opening-range lengths and the immediate-direction entry) never computed at any stage, though its multiplicity is already paid
- **Direction:** A
- **Class:** OVER_CLOSED
- **Severity:** S3
- **Label:** DERIVED
- **Claim challenged (verbatim quote):** "**Registered here, before TASK 1 runs.** Stage A.3 applies **one** lever to H1 — a measurement of the slippage band on the instruments actually traded — and **no further rescue lever is applied afterwards.**" — ORBExperiment/REGISTRATION.md:3679-3681
- **Evidence:** The registration names the alternative range lengths and already prices them: "The 15, 30 and 60-minute range lengths; the immediate-direction entry; ... **None of these moves a verdict row**, and the registered trial count of 8 already prices the range-length and entry-rule crossings into E1's deflation." — ORBExperiment/REGISTRATION.md:465-471; the trial count is "**four opening-range lengths (5, 15, 30 and 60 minutes) crossed with two entry rules**" — ORBExperiment/REGISTRATION.md:439-441. **Six of those eight registered cells were never computed at any stage of this repository** — no amendment, report section or `reports/` artefact carries a figure for a 15, 30 or 60-minute range or for the immediate-direction entry. Two facts make the omission material. **(a) Cost.** The floor scan re-read the identical sealed slice for a different parameterisation at **zero request cost**: "**Zero dollars spent, zero requests sent by this scan** — the bytes were sealed on 2026-08-29 and re-reading a stored file is not a vendor call." — ORBExperiment/REGISTRATION.md:3858-3860. A range-length scan is the same operation on the same bytes. **(b) Direction.** Under the carried band the deciding quantity is one step from passing on a variable the range length mechanically moves: "| **break-even stop-exit share** at 1.40 | **0.346206** |" against a measured 0.381818, "| the measured stop share exceeds it by | **0.035612** |" — ORBExperiment/REGISTRATION.md:3423-3424. A 15/30/60-minute opening range gives a wider entry-to-stop distance and therefore fewer stop-outs; the registration never measures how many. Meanwhile the pass **did** pay a fresh multiplicity cost to scan a variant that is *not* registered: "**H1b increments the Section 8 deflated-Sharpe trial count from 8 to 9**" — ORBExperiment/REGISTRATION.md:3818-3819. **A variant already paid for was not run; a variant not paid for was scanned.**
- **Recomputation (if any):** Inputs: carried band (REGISTRATION.md:388-392), central mean at 1.40 = 0.040386 (REGISTRATION.md:3694). Method: under the carried band `shift(s) = 0.030 + 0.030·s`, so the pessimistic-cost mean is positive for any stop-exit share `s < (0.040386 − 0.030)/0.030 = 0.346206` — reproducing the repository's own break-even stop share exactly. Under the **measured** band the same algebra gives `shift(s) = 0.488626 − 0.056468·s`, which is above 0.040386 for every `s` in [0,1], so **on the measured band a lower stop share does not help** and this route only bites if findings 1–3 are also right. That is stated here rather than hidden.
- **What would resolve it:** Run the range-length scan on the sealed 42-session slice at zero request cost and report the stop-exit share, the trigger rate and the entry half spread at 5, 15, 30 and 60 minutes — or record explicitly that the six unrun cells of the registered trial count of 8 are abandoned and why.
- **Confidence:** MEDIUM — the omission and its zero cost are certain; whether the variant would change the outcome depends on findings 1–3, and this is stated in the recomputation.
- **Invalidated by later commits?:** no — HEAD is the anchored SHA with a clean tree.
- **Disclosed by authors?:** no — Amendment 24 §1 registers that exactly one lever will be applied but does not name the range-length family as a lever considered and rejected, and no document records that six of the eight registered trials were never computed.

---

### DRAFT-p1-registration-8
- **Repository / SHA:** ORBExperiment / f2aa675a80fc06b74979040b3028154d1add5ec0
- **Hypothesis or artifact:** H1 (H-ORB) — every deciding number was measured on a selection whose relative-volume extremity is not the registered selection's, and the sample-artefact caveat was applied to one column and explicitly withheld from the rest
- **Direction:** A
- **Class:** STATISTICAL
- **Severity:** S2
- **Label:** DERIVED
- **Claim challenged (verbatim quote):** "**The 5, 10 and 20 USD rows are not affected**: all three fill 20 names on all 28 sessions **within the sample**, which is a sufficient condition, not a necessary one." — ORBExperiment/REGISTRATION.md:3916-3918
- **Evidence:** Every figure the closure rests on — dispersion 2.029585 (n = 550), stop-exit share 0.381818 (n = 550), trigger rate 0.982143 (n = 560), trades per session 19.642857, and all six band ends (n = 550/210/340) — comes from a top-20 selection drawn from "a **200-name systematic sample** of a 5,317-name active US common-stock listing ... **every 26th ticker**" — ORBExperiment/REGISTRATION.md:2570-2573, 3906-3907. The registered selection is the top 20 of the whole universe. **The registration's own hypothesis is that this selection is what does the work**: "the plain broad-universe 5-min ORB returned **3.2 percent annually at Sharpe 0.48, below passive** (carried, C-2), while the top-20-by-relative-volume restriction returned **more than 1,600 percent at Sharpe 2.81**" — ORBExperiment/REGISTRATION.md:3548-3551; "**The selection did almost all the work there too.**" — REGISTRATION.md:3551-3552. **The measured extremity of the sampled selection is reported and never compared to the registered one**: "| **5** | 560 | 28 | **28** | **2.0652** | ..." — mean relative volume of the selection **2.0652** — ORBExperiment/REGISTRATION.md:3873. Taking the top 20 of 200 names is the top **10 percent** of the sample; taking the top 20 of 5,317 is the top **0.38 percent**. The repository raises the 1-in-26 sampling as a caveat for exactly one column — "**The 'sessions filling 20' column measures the SCAN SAMPLE, not the registered universe**" — REGISTRATION.md:3903-3904 — and then explicitly clears the others (line quoted above). The same sampling changes the **selection itself**, and the selection is the deciding population for the band, the dispersion and the stop share alike.
- **Recomputation (if any):** Selection ratios: 20/200 = 0.100 of the sample vs 20/5,317 = 0.00376 of the registered listing, a factor of **26.6** in tail depth — the repository's own "26.6 times larger" figure (REGISTRATION.md:3909) applied to the selection rather than to the fill count. No recomputation of the band is possible without the full-universe pull the pass did not authorise (REGISTRATION.md:3913-3914). Direction of the bias is **not bounded anywhere in the repository**: Amendment 26 §4's own reasoning ("**The selection rule and the wide-spread population are the same population**", REGISTRATION.md:4011-4012) implies the true selection's spreads are wider, which would worsen the cost; but the same names carry higher per-share dispersion, and the central mean the shift is compared against is proportional to that dispersion (`mu = (S/sqrt(252)) · sigma / sqrt(k)`, verified: 0.088192 × 2.029585 / 4.432031 = 0.040387, reproducing the repository's 0.040386). The floor scan shows both moving together — dispersion 2.0296 → 3.1992 while the central mean goes 0.040386 → 0.085626 (REGISTRATION.md:3873,3877) — so the net direction is genuinely unknown, and no document says so.
- **What would resolve it:** Attach the same caveat to every column the scan and the band share, and either bound the bias (a full-universe pull at the registered filter on a handful of sessions would price it) or record it as an unbounded scope limitation in the manner of SL-3.
- **Confidence:** MEDIUM — the mismatch between the sampled and registered selection is certain and quotable; its effect on the deciding number is unbounded in either direction, and the finding is that the unboundedness is undisclosed, not that the closure is wrong.
- **Invalidated by later commits?:** no — HEAD is the anchored SHA with a clean tree.
- **Disclosed by authors?:** partly — the 200-name systematic sample is disclosed repeatedly (REGISTRATION.md:2570-2573, 2654-2659, 3906-3909), and the trigger rate is stated narrowly with it. The specific point — that the caveat is raised for one column and explicitly cleared for the rest, while the sampling changes the relative-volume extremity of the selection itself — is not disclosed.

---

### DRAFT-p1-registration-9
- **Repository / SHA:** ORBExperiment / f2aa675a80fc06b74979040b3028154d1add5ec0
- **Hypothesis or artifact:** H1 (H-ORB) — the blocker stated on the only route that could reopen the closure
- **Direction:** A
- **Class:** OVER_CLOSED
- **Severity:** S3
- **Label:** DERIVED
- **Claim challenged (verbatim quote):** "**The honest attack on this closure is the second item**, and it is the one Amendment 21 route (b) names: **real execution evidence could narrow the band.** **This repository holds none, has no broker credential, and none is planned.**" — ORBExperiment/REGISTRATION.md:4154-4156
- **Evidence:** The blocker is stated as absolute, and the repository already holds the entitlement that produces the standard non-broker execution-cost estimate. The tier serves historical NBBO quotes: "The tier **serves historical NBBO quotes** — probed and confirmed before the tool was written — so **the quoted spread is measured, not assumed**: **760 quote minutes served, 0 refused.**" — ORBExperiment/REGISTRATION.md:3967-3969; the request is built at `f"{ALPACA_DATA_HOST}/v2/stocks/{ticker}/quotes?"` — ORBExperiment/src/orb/vendors.py:526, alongside the bars request on the same host and version prefix (`/v2/stocks/{ticker}/bars`, ORBExperiment/REGISTRATION.md:1754). **The vendor's Market Data v2 API exposes a trade-print endpoint at the same host and prefix, `GET /v2/stocks/{symbol}/trades`, with the same auth headers and the same `feed` parameter as the bars and quotes endpoints this repository already calls.** No module, tool, ADR or amendment in this repository names, probes or refuses that endpoint (`grep` over `src/orb`, `tools`, `docs`, `REGISTRATION.md`, `DECISIONS.md`, `report.md` returns no trade endpoint). Two things it would settle, both currently recorded as unresolvable: (a) the stated resolution limit — "**457 of 550 entry triggers and 195 of 210 stop triggers crossed their boundary INTRABAR**, and one-minute data cannot locate the first trade through a boundary inside a bar" — ORBExperiment/REGISTRATION.md:4042-4044 — is a limit of *minute bars*, not of the entitlement: the trade tape locates the first print through a boundary exactly; (b) signing trades against the prevailing NBBO gives an **effective spread**, the standard measured execution cost, which requires no broker account and no fills of one's own. The repository has established elsewhere that probing an endpoint is within scope and costs one request (the quotes endpoint was "probed and confirmed before the tool was written"), and it holds 1,121 unspent requests of a 3,000 daily Alpaca cap on the day in question (`n = 759` quote requests sent, REGISTRATION.md:3961-3962).
- **Recomputation (if any):** none — this is a blocker-scope finding, not an arithmetic one.
- **What would resolve it:** One probe of `/v2/stocks/{ticker}/trades` on the held credential, recorded with its status code and refusal payload verbatim in the manner of every other access measurement in this repository. If it serves, the entry leg becomes measurable as the registered order actually behaves (finding 2) and the intrabar limitation disappears; if it refuses, the blocker becomes measured rather than asserted, which is this repository's own standing rule 4.
- **Confidence:** MEDIUM — that the endpoint was never probed is certain from the repository; that it is served on this tier is stated from my own knowledge of the vendor's v2 API and is not verified here (I did not send a request to any vendor). The finding stands either way as "an endpoint on the held tier was never probed before the blocker was called absolute".
- **Invalidated by later commits?:** no — HEAD is the anchored SHA with a clean tree.
- **Disclosed by authors?:** no — the blocker is stated as "holds none, has no broker credential, and none is planned" with no mention of any non-broker measurement of execution cost, and no amendment records the trade endpoint as considered.

---

### DRAFT-p1-registration-10
- **Repository / SHA:** ORBExperiment / f2aa675a80fc06b74979040b3028154d1add5ec0
- **Hypothesis or artifact:** H1 status statements across the register and the handover
- **Direction:** A
- **Class:** INTERNAL_INCONSISTENCY
- **Severity:** S4
- **Label:** READ
- **Claim challenged (verbatim quote):** "**Status at 2026-08-29: H1 OPEN, registered, Stage A in progress. Ten candidates closed before opening at registration. H2 and H3 PARKED.**" — ORBExperiment/HYPOTHESES.md:15-16
- **Evidence:** The same file's H1 entry, 35 lines later, reads "**CLOSED — `cost-bound`** · closed **2026-08-30**" — ORBExperiment/HYPOTHESES.md:58. The file's stated discipline is that a closed entry is findable ("**This file exists to prevent retrying a settled question because the number that closed it is buried.**", HYPOTHESES.md:6-7), and the first status line a reader meets says OPEN. The same stale-status pattern recurs outside my assignment: "H1 remains **OPEN**, and closing it as `untestable-at-achievable-power` is **one of three routes**, not a conclusion this pass reached." — ORBExperiment/docs/HANDOVER.md:381-383 (primary evidence outside my assignment), in a file whose first line is "# H1 IS CLOSED." (HANDOVER.md:5); and the same file gives three different amendment counts and two ADR counts — "**Twenty-eight amendments stand. Thirty-eight ADRs.**" (HANDOVER.md:43), "**Ten amendments** stand; read all of them." (HANDOVER.md:156), "**and all twenty-three amendments**" (HANDOVER.md:312), "**35 ADRs**" (HANDOVER.md:319). The true counts are **28 amendments** and **38 ADRs**, so the line at HANDOVER.md:43 is right and the three later lines are stale by 18, 5 and 3 respectively.
- **Recomputation (if any):** Headings counted from the anchored files: `grep -c '^## Amendment ' REGISTRATION.md` = **28** (numbers 1–28, with Amendment 26 appended *after* Amendment 27 — an anomaly the repository itself records at REGISTRATION.md:3950-3956); `grep -c '^## ADR-' DECISIONS.md` = **38**.
- **What would resolve it:** One dated line at the head of `HYPOTHESES.md` restating the status as of the closure, in the append-only style the register already uses; and one reconciliation of the amendment and ADR counts in the handover.
- **Confidence:** HIGH — all statements are quoted from the anchored files.
- **Invalidated by later commits?:** no — HEAD is the anchored SHA with a clean tree.
- **Disclosed by authors?:** no — the 2026-08-29 header carries an "Updated 2026-08-29, A.1 resumption" note (HYPOTHESES.md:18) but was not updated at the 2026-08-30 closure.

---

## What I checked and found sound

**The arithmetic.** Every deciding figure I could reconstruct from the repository's stated primitives reproduces: the measured shift 0.467065, the carried shift 0.041455, the central mean at 1.40 (0.040386, from `mu = (S/sqrt(252))·sigma/sqrt(k)` = 0.088192 × 2.029585 / 4.432031), E2 power 0.043277 at the carried band and 0.819524 at 2.81, the break-even stop share 0.346206, the required shift of 0.001893 for 80 percent power (2.486475 × 2.029585 / sqrt(17188) = 0.038491 required pessimistic mean; 0.040386 − 0.038493 = 0.001893), and the 21.89-fold required reduction. REGISTRATION.md:3690-3698, 3377-3384, 3419-3424.

**Amendment 18's multiplicity correction is right.** Section 8 is an intersection-union test ("both must pass", REGISTRATION.md:429) and `1 − 0.95^(1/2)` is the Šidák correction for a union. Berger (1982) is applied correctly and the one-line subset argument at REGISTRATION.md:3034-3037 is valid. The correction moves E1 the right way and the repository says loudly that it does not make the design powered (REGISTRATION.md:3104-3107). I looked for a self-serving alpha loosening and did not find one: 0.05 was fixed before the table that it flatters (REGISTRATION.md:3443-3445), and the commit order supports it.

**Amendment 19's replacement of E2 is right and was pre-committed.** The old E2 was a linear rescale of E1 and constrained nothing (REGISTRATION.md:3137-3149); the amended null was fixed *before* the stop-share measurement that feeds it (REGISTRATION.md:3128-3131), and Amendment 19 §6 pre-registered what a collapse would mean (REGISTRATION.md:3233-3246). This is the opposite of the failure mode I was hunting for.

**The pre-commitment ordering holds.** `git log` on the live repository confirms `4ae14dc` ("docs: A.-1 TASK 0 — the rescue-pass success criterion, pre-committed", 2026-08-29 20:13:26 −0700) precedes `5899e1b` ("feat: A.3 TASK 2 — the slippage band measured", 20:41:12 −0700) and `7edeea7` (the verdict, 20:41:59). The criterion was committed 28 minutes before the measuring tool, not days, but the ordering claim at REGISTRATION.md:3675 and 4068-4069 is factually correct.

**The measurement went against the hypothesis.** Amendment 26 §6's own control (REGISTRATION.md:4031-4038) is a real one: a rescue pass whose one lever came back eleven times worse is not a search for a favourable number. Findings 1–3 are about what two of the six band ends measure, not about a thumb on the scale.

**NOT_RESCUED survives each single objection.** Recomputed: correcting the close leg alone leaves shift 0.423423; capping the entry at the registered limit alone leaves 0.199440; adopting the registered 2× band shape alone leaves 0.124549. All three are far above the 0.040386 threshold. Only the *combination* of the entry cap with the registered band shape flips the tier. I report that plainly rather than presenting the flip as the single reading.

**The overshoot lower-bound caveat is honestly stated and points against the hypothesis.** REGISTRATION.md:4040-4051, 3920-3931, ADR-038 at DECISIONS.md:1464-1476. The repository consistently records that its own cost measurement is a floor.

**Absence discipline.** `Absent` refuses arithmetic; "none" for an unreachable minimum n is a recorded absence rather than a large number (REGISTRATION.md:3386-3388); the unreached Alpaca ceiling stays `None` (REGISTRATION.md:2478-2482); the SEC fee schedule refuses rather than take a rate from the wrong year (REGISTRATION.md:1053-1060). I looked for a synthesised zero and found none.

**Scope limitations are registered before their numbers exist, not after.** SL-1 (shared upstream, REGISTRATION.md:630-634), SL-2 (overlap from 2024-08-29, REGISTRATION.md:635-636), SL-3 (in-sample single-sourced, REGISTRATION.md:640-698). SL-3 in particular is registered with two named retirement routes and no spend authorised — exactly the shape my thesis says is usually missing.

**The trigger-rate and carve-out falsifications are recorded as falsifications, with their n, and the planning figures are left visible.** REGISTRATION.md:2635-2665, 2019-2043. This is the NPLExperiment correction working.

**The ten candidates culled at registration.** HYPOTHESES.md:120-131. Each is closed on a stated reason before any data existed, two are labelled DUPLICATE with the repository that holds them named, and none is presented as a measurement. Candidate 1 (the index-ETF variant) is closed on the replication's own figures (C-5, C-6) rather than on this repository's, and ADR-013 carries it. I found no candidate closed on a figure this repository could have measured cheaply and did not.

**H1b's registration is disciplined.** The ninth trial is paid explicitly (REGISTRATION.md:3818-3819), the floor is deliberately not chosen from the scan that motivated it (REGISTRATION.md:3793-3796), and Amendment 24 §6 forbade the scan from rescuing H1 *before* either ran (REGISTRATION.md:3740-3748). I checked whether the floor scan was quietly used to soften the closure and it was not.

**One reporting artefact I am not raising as a finding.** In `reports/stage_a3rescue/task4_floor_scan.json` the field `eligible_name_sessions` is always identical to `selected_name_sessions`, because both are incremented inside the same loop over `_selections`, which has already truncated to `CONFIG.max_concurrent_positions` — ORBExperiment/src/orb/dispersion.py:1058-1066, with the truncation at src/orb/dispersion.py:544. The field therefore carries no information about the eligible pool. It is not load-bearing for any verdict and no document quotes it, so I record it here rather than as a finding.

**What I would have expected to find if the thesis held more broadly and did not.** A closure timed to avoid a due measurement — the bar-integrity re-pull of 2026-09-12 is orthogonal to the cost closure and the repository says so and keeps the date alive (REGISTRATION.md:4192-4193, HANDOVER.md:94-96). A cost band moved after seeing a null — it was explicitly not moved (REGISTRATION.md:4055-4058, 4128). An effect assumption or alpha moved to rescue a figure — neither was (REGISTRATION.md:4128-4130). A prior scored against an event that did not resolve — the ledger explicitly refuses to (REGISTRATION.md:4175-4181). A window extended to buy power while holding a result — the temptation is named and refused while holding no result (REGISTRATION.md:1168-1174).

---

## Live-repo access log

Read-only access to `/home/kiros-li/Documents/GitHub/ORBExperiment` for git history only (`git status --porcelain`, `git log`, `git rev-parse`). No file in the live repository was opened for writing and no untracked data file was read.

**Before (2026-09-04, `git -C /home/kiros-li/Documents/GitHub/ORBExperiment status --porcelain`):**

```
```

(empty — clean working tree)

**After (same command, after the last live-repo read):**

```
```

(empty — clean working tree)

`git rev-parse HEAD` returned `f2aa675a80fc06b74979040b3028154d1add5ec0`, which is the anchored SHA; there are no commits after the anchor, so no finding in this draft can be invalidated by a later commit as of the read time.
