# Agent A draft findings — HFExperiment (part: all)

Repository: HFExperiment, anchored SHA 82e77a021256d917c665ff6d4304c25b08f35451 (main, 2026-08-28). Read from SNAP/HFExperiment. Live repo touched read-only for git objects and a directory listing only (log at the end).

Context in one paragraph: HFExperiment registered a two-series design for hypothesis H-F (12-1 cross-sectional momentum, top-5 by width in U-LIQ-500). The SHADOW series was the signal instrument, "no broker, no account, and no money" (REGISTRATION.md:38). The LIVE series was the execution instrument. Section 0 pre-registered three broker outcomes; under BLOCKED "Phase B proceeds unchanged ... The signal question still gets answered" (REGISTRATION.md:37-39). Stage A.1b fired BLOCKED at 2026-08-25T03:07Z. The whole experiment was then closed "terminal" with the shadow timer disarmed before its first accrual, in a commit at 2026-08-25T07:45:29Z. Zero shadow observations exist. The recomputations below are in `scratchpad/work/agentA/recompute_hf.py` and `recompute_hf.out`.

---

### DRAFT-all-1
- **Repository / SHA:** HFExperiment / 82e77a021256d917c665ff6d4304c25b08f35451
- **Hypothesis or artifact:** H-F signal hypothesis (REGISTRATION.md Section 1) and the SHADOW series that was its only instrument; the 2026-08-26 "terminal" closure.
- **Direction:** A
- **Class:** OVER_CLOSED
- **Severity:** S2
- **Label:** DERIVED
- **Claim challenged (verbatim quote):** "The shadow series was disarmed before its first accrual: hfexperiment-bars.timer stopped and disabled via systemctl --user, verified that no HFExperiment unit remains scheduled. The verdict was never computed. Closure is terminal." — HFExperiment/REGISTRATION.md:310-313
- **Evidence:**
  - The registration pre-committed that the broker outcome cannot stop the signal series: "BLOCKED ... Consequence: phases C and D stop. Phase B proceeds unchanged, because the shadow series needs no broker, no account, and no money. The signal question still gets answered." — HFExperiment/REGISTRATION.md:33-39. ADR-002: "If the broker question resolves BLOCKED, phase B still runs and still answers the signal question. Only phases C and D die. This property is the reason the two-series design was chosen. Changes it: nothing. A later stage that couples the shadow series to a broker dependency violates this ADR." — HFExperiment/DECISIONS.md:24-29.
  - The A.1b stage entry, written the same night, still says so: "The shadow series carries the experiment alone and answers the signal question, which was the design's point." — HFExperiment/progress.md:42-44.
  - Timing from git objects (live repo, read-only): A.1b commit 669eb5c author/committer epoch 1787627346 = 2026-08-25T03:09:06Z; closure commit f13e1d3 epoch 1787643929 = 2026-08-25T07:45:29Z; gap 4.61 h. The closure diff touches only REGISTRATION.md (+11) and progress.md (+18). The A.1b run itself ended 03:07Z (HFExperiment/reports/stage_a1b/a1b_report.md:3).
  - State of the instrument at closure: timer "is-enabled: enabled / is-active: active", next formation 2026-09-01 (HFExperiment/reports/monitor/health.txt:4-10); "observations: 0" at every width (HFExperiment/reports/monitor/verdict.txt:5,14,23). n = 0 shadow observations (REGISTRATION.md:314-315).
  - The closure entry gives no reason beyond "operator decision" (REGISTRATION.md:308; progress.md:7-8) and registers no reopen condition for the signal question. The only reopen clauses in the repository concern the live table: "IBKR shipping fractional support in the TWS API, or an Alpaca Canadian launch" (HFExperiment/DECISIONS.md:427-428; progress.md:44-46).
  - The operator accepted the 8-to-11-year clock one day earlier with eyes open: "Eight to eleven years. The operator knows this and proceeds because the execution question is answerable now and the signal question is not." — HFExperiment/REGISTRATION.md:261-263; acceptance 2026-08-24 (REGISTRATION.md:286-295; DECISIONS.md:230-242). Between acceptance and closure the only new fact was the broker result, which the design had declared irrelevant to the shadow series.
  - The one known technical pre-start item was a one-line fix the authors themselves sized: "the 2026-09-01 formation run will fail loudly until a one-line fix lands under B.1 authorization" (HFExperiment/progress.md:87-89; DECISIONS.md:378-387). It was cancelled rather than applied: "B.1a cancelled as moot: no formation will ever call the assets endpoint." (progress.md:18-19).
  - This is the second time H-F has been closed without a signal verdict: "tested once in the AiTrader cross-sectional round of 2026-07-26 and resolved on statistical power rather than absent signal." — HFExperiment/README.md:3-5.
- **Recomputation (if any):** Reachability of the instrument that was disarmed, using the registered inputs (mean 27.99 bp/day, sigma 418 bp/day, rho 0.071641, alpha 0.05; HFExperiment/src/hfexperiment/registered.py:91,104-107; radius formula src/hfexperiment/verdict.py:26-34): lower bound clears zero at day 2061 and clears 4.07 at day 2852 — reproduces REGISTRATION.md:259-261 exactly. Pointwise fixed-n at the point estimate: 604 days; fixed-horizon 80 percent power: 1,379 days. So a positive verdict was reachable in 8-11 years at the registered effect; see DRAFT-all-3 for the negative side. Cost of continuing per the registration: none in money (REGISTRATION.md:38; DECISIONS.md:22-23); the daily run needs only Alpaca data keys, which progress.md:99-100 records as already in .env.
- **What would resolve it:** An appended amendment that (a) states the actual ground for disarming the zero-observation shadow series (a resource or clock decision is inferable from REGISTRATION.md:261-263 but is nowhere recorded), (b) acknowledges that it departs from Section 0's BLOCKED consequence and ADR-002, and (c) registers a reopen condition for the signal question itself (for example: re-arm at the next formation if any broker clears the GO bar, or if another repository produces a powered momentum test). Alternatively, re-arm the timer; the pipeline exists, is tested (158 tests green, progress.md:92), and the series is formation-aligned so any first-of-month start is registration-clean (DECISIONS.md:244-256).
- **Confidence:** HIGH — the contradiction between the registered BLOCKED consequence and the closure is textual and the timing is from git objects; that the closure was premature rather than merely unexplained is the advocacy part, and the honest counterweight is the 8-11 year clock the operator had already accepted.
- **Invalidated by later commits?:** no — the anchored SHA is the live HEAD as of 2026-09-03T04:54Z; a later amendment stating the reason or re-arming the series would change the status of the hypothesis but not the record at this SHA.
- **Disclosed by authors?:** no — the disarming itself is recorded (REGISTRATION.md:310-312; progress.md:12-15), but no entry acknowledges that it contradicts Section 0 and ADR-002, states a reason, or registers a reopen condition for the signal question.

---

### DRAFT-all-2
- **Repository / SHA:** HFExperiment / 82e77a021256d917c665ff6d4304c25b08f35451
- **Hypothesis or artifact:** Section 0 broker outcome verdict of 2026-08-25 (REGISTRATION.md amendment log) and the A.1b report.
- **Direction:** A
- **Class:** INTERNAL_INCONSISTENCY
- **Severity:** S2
- **Label:** READ
- **Claim challenged (verbatim quote):** "BLOCKED. The IBKR TWS API refused fractional quantities however phrased on paper account [paper account ID removed], error 10243 on decimal totalQuantity across two book names and two order types, error 10244 on cashQty, while a whole-share control order was accepted" — HFExperiment/REGISTRATION.md:299-303
- **Evidence:**
  - The registered definitions, fixed before measurement: "DEGRADED: A broker clears every bar except fractional-through-the-API." (HFExperiment/REGISTRATION.md:21-23); "BLOCKED: No reachable broker clears the bars." (REGISTRATION.md:33-35).
  - The measured outcome: IBKR Canada clears residency, US equities and an order-placing API (HFExperiment/docs/ACCESS.md:11,16-17); the whole-share control order was "ACCEPTED and queued" (reports/stage_a1b/a1b_report.md:91-93); only fractional-through-the-API refused (a1b_report.md:67-70, 78-82). That is the DEGRADED definition word for word; a reachable broker clears every bar but one.
  - The repository's own A.1 stage had already ruled BLOCKED out and said the test could only resolve the other two: "BLOCKED is ruled out on documented bars. The GO versus DEGRADED verdict is UNDECIDED" (HFExperiment/DECISIONS.md:39-40); "Changes it: the Task 3 test resolves GO or DEGRADED." (DECISIONS.md:65); "GO versus DEGRADED undecided pending Task 3. BLOCKED ruled out on documented bars." (HFExperiment/progress.md:222-223).
  - The A.1b report justifies BLOCKED by GO's failure alone: "Section 0 fires BLOCKED. The registered GO bar requires the API to accept fractional quantities at 45 USD per name." (a1b_report.md:107-108), and in the same paragraph applies the DEGRADED branch: "Per Section 6, DEGRADED whole-share sizing stays closed at this stake." (a1b_report.md:113-114). Both labels are applied to one outcome without noting that the taxonomy makes them exclusive. ADR-026 later reaffirms "the Section 0 BLOCKED stands exactly as recorded" (progress.md:256-257).
  - Why the label matters: the two branches carry different registered reopeners. BLOCKED's are external ("IBKR shipping fractional support in the TWS API, or an Alpaca Canadian launch", DECISIONS.md:427-428). DEGRADED's is in the operator's hands: "Changes it: a materially larger stake, which is a new registration, not an amendment." (HFExperiment/DECISIONS.md:201-202). The closure entries (REGISTRATION.md:297-315; progress.md:5-21, 39-46) carry only the BLOCKED reopeners; the larger-stake path is not mentioned in any post-A.1b entry. ACCESS.md:197 confirms the path is open: "Whole-share through the API stays open; only slicing is closed".
- **Recomputation (if any):** What "materially larger stake" means, from stored prices. 2026-08-03 width-20 book entry closes (HFExperiment/reports/stage_c1/formation_2026-08-03.json, key width20_entry_closes): one share of each of 20 names = 5,936 USD; equal-weight with one share of the priciest (SNDK 1,214.83) = 24,297 USD. Width-5 book (SNDK, AXTI, WOLF, MU, WDC; same file, books.5): one share each = 2,667 USD; equal-weight at one SNDK share = 6,074 USD. At the 2026-07-01 closes (reports/stage_a1/formations.json, formations.2026-07-01) the width-5 book is 3,555 USD one-share-each and 11,369 USD equal-weight (SNDK 2,273.73). So a whole-share DEGRADED sleeve exists at roughly 3x to 24x the registered 1,000 USD depending on width and weighting tolerance. Whether that is achievable is the operator's call; the point is that the record labels the outcome so that the question never arises.
- **What would resolve it:** An amendment re-labelling the 2026-08-25 verdict DEGRADED-with-closed-branch per Section 0 and Section 6, carrying ADR-012's larger-stake reopener into the closure record, and stating the stake at which the whole-share sleeve becomes survivable (the arithmetic above, or the authors' own).
- **Confidence:** HIGH — the definitional mismatch is verbatim and the authors' own A.1 stage says BLOCKED was already ruled out; the practical consequence at 1,000 USD is identical under either label, which is why this is S2 rather than S1.
- **Invalidated by later commits?:** no — no commit after the anchor exists; ADR-026 (the last commit) explicitly reaffirms the BLOCKED label.
- **Disclosed by authors?:** no — a1b_report.md:107-114 applies both Section 0 BLOCKED and Section 6 DEGRADED to the same outcome without acknowledging that the taxonomy makes them exclusive, and no entry revisits ADR-003:65 ("resolves GO or DEGRADED").

---

### DRAFT-all-3
- **Repository / SHA:** HFExperiment / 82e77a021256d917c665ff6d4304c25b08f35451
- **Hypothesis or artifact:** Section 11 verdict schedule: futility bar 10 bp/day against success hurdle 4.07 bp/day, and the claim that the shadow series can produce a documented negative.
- **Direction:** A
- **Class:** STATISTICAL
- **Severity:** S3
- **Label:** DERIVED
- **Claim challenged (verbatim quote):** "Success when the lower bound clears the measured cost hurdle of 4.07 bp per day ... Futility when the upper bound falls below 10 bp per day." — HFExperiment/REGISTRATION.md:249-252; and "A documented negative is a valid outcome at a cost of roughly 30 to 60 USD a year at the traded width" — HFExperiment/REGISTRATION.md:279-280
- **Evidence:**
  - Thresholds as code: futility_bp_per_day = 10.0 (HFExperiment/src/hfexperiment/registered.py:70), cost_hurdle_bp_per_day = 4.07 (registered.py:78); classification order success-then-futility (src/hfexperiment/verdict.py:92-101). Noise: sigma 418 bp/day (registered.py:105; REGISTRATION.md:256-257). No derivation of the 10 bp figure exists anywhere in the repository (grep "futility" over all .md: the single hit is REGISTRATION.md:251).
  - The futility bar sits ABOVE the success hurdle. Because the sequence is symmetric about the sample mean, futility fires before success whenever the true mean is below (10 + 4.07)/2 = 7.035 bp/day. A true excess of 4.07 to 7.03 bp/day (10 to 18 percent per year, net-positive after the registered costs, i.e. the economic content of Section 1's "a fee-paying participant keeps most of it", REGISTRATION.md:55-56) is classified FUTILE before it can be classified SUCCESS.
  - More importantly for the closure record: the futility bar is unreachable at any human horizon, so the design could never have produced the "documented negative" it advertises. See recomputation.
- **Recomputation (if any):** Inputs: sigma 418 bp/day (registered.py:105), rho 0.071641 (registered.py:91), alpha 0.05 (registered.py:67), radius formula verdict.py:26-34, bars registered.py:70,78. Method: first day t at which mean + radius(t) < 10 (futility) or mean - radius(t) > 4.07 (success), scanning t. Results: true mean 0.00 bp/day: futility at day 18,650 (about 74 trading years), success never. True mean 4.07: futility at day 58,309. True mean 6.00: futility at day 137,247. True mean 7.03: futility at day 261,550 vs success at 263,464 (futility first). True mean 8.00: success at day 142,605, futility never. True mean 15.10 (the interpolated width-20 excess, REGISTRATION.md:117): success at day 15,060. True mean 27.99: success at day 2,852 (matches registration). Width-50 secondary at its recorded 10.04 bp/day (REGISTRATION.md:118), sigma 199.7 bp/day from TE 31.70 percent, alpha 0.025: success at day 13,178. Cross-check: the registered clear-zero day 2,061 and clear-hurdle day 2,852 reproduce exactly.
- **What would resolve it:** Either register a derivation for the 10 bp futility bar and state plainly that the design has no achievable negative (so "the signal question still gets answered", REGISTRATION.md:39, holds only on the positive side), or re-register futility as a bound on the lower side of the economic hypothesis (for example upper bound below the cost hurdle 4.07) together with the horizon at which it becomes reachable. For the closure record: state that H-F leaves this repository untested, not falsified, because no negative verdict was ever reachable and none was computed.
- **Confidence:** HIGH — the arithmetic is a direct evaluation of the repository's own boundary function with its own constants; whether the 10 bp bar is a defect or an undocumented design choice is a judgment, hence S3.
- **Invalidated by later commits?:** no — the constants and formula are pinned by tests (tests/test_verdict.py:52-55; tests/test_verdictengine.py per registered.py:88-90,103) and no later commit exists.
- **Disclosed by authors?:** no — the registration discloses the slow positive clock (REGISTRATION.md:255-263) but nowhere states that the futility bar is above the success hurdle or that a negative is unreachable; this finding cuts both ways and the B pass may prefer to rate the "documented negative is a valid outcome" sentence as S2 under direction B.

---

### DRAFT-all-4
- **Repository / SHA:** HFExperiment / 82e77a021256d917c665ff6d4304c25b08f35451
- **Hypothesis or artifact:** Broker table verdict (docs/ACCESS.md) and its registered recheck trigger for Alpaca's Canadian exclusion.
- **Direction:** A
- **Class:** PROCESS
- **Severity:** S4
- **Label:** READ
- **Claim challenged (verbatim quote):** "Alpaca excludes Canadian residents today. Its careers page advertises a Canadian broker-dealer controller role, so the exclusion may lift. Recheck at stage C if Task 3 resolves badly." — HFExperiment/docs/ACCESS.md:17-20
- **Evidence:**
  - Task 3 resolved badly on 2026-08-25 (REGISTRATION.md:297-304). Stage C.1 ran the same night (progress.md:56-100) and A.1b after it (progress.md:23-54). Neither entry, nor the closure (progress.md:5-21), nor ADR-026 three days later (DECISIONS.md:432-479; progress.md:226-271) records a recheck of the Alpaca eligibility page. The only mentions after the trigger restate the clause as a future reopener: "an Alpaca Canadian launch would reopen the table" (reports/stage_a1b/a1b_report.md:115-116; progress.md:44-46).
  - The blocker's cited source is https://alpaca.markets/support/countries-alpaca-is-available quoting "Residents of Canada are not currently eligible" as retrieved 2026-08-23 (ACCESS.md:31-32). Fetched 2026-09-03T04:58Z (WebFetch, unanchored): the page, dated February 2026, lists no countries and says only "Please contact support ... for more information regarding whether your country is supported." A third-party page (brokerchooser.com, "Is Alpaca Trading Available to Investors in Canada?", stated last updated 2026-03-11, via WebSearch 2026-09-03) still says Canadian residents are not eligible. So the blocker probably still holds, but its cited primary source no longer states it and the registered recheck was never done.
- **Recomputation (if any):** none.
- **What would resolve it:** Perform and date the registered recheck (Alpaca eligibility for Canadian residents) and append the result to ACCESS.md; if the exclusion has lifted, the BLOCKED reopener in DECISIONS.md:427-428 is met and the live table reopens as a new measurement per ADR-022.
- **Confidence:** HIGH that the recheck is absent from the record; LOW that Alpaca's policy has actually changed.
- **Invalidated by later commits?:** no — no later commit exists; a dated recheck would close this item.
- **Disclosed by authors?:** no — the trigger is registered at ACCESS.md:19-20 but no entry acknowledges that it fired.

---

### DRAFT-all-5
- **Repository / SHA:** HFExperiment / 82e77a021256d917c665ff6d4304c25b08f35451
- **Hypothesis or artifact:** Deferred parameter broker_min_notional_usd (Amendment 1) and its stated blocker in enforced code.
- **Direction:** A
- **Class:** STALE_FIGURE
- **Severity:** S4
- **Label:** READ
- **Claim challenged (verbatim quote):** "reason=\"MinSize and SizeIncrement come from reqContractDetails on a \" \"live-permissioned account that does not exist yet\"," — HFExperiment/src/hfexperiment/registered.py:119-120
- **Evidence:**
  - A.1b measured exactly this on 2026-08-25: "All 20 names advertise fractional sizing at the contract layer" with MinSize 0.0001 and SizeIncrement 0.0001 per name (HFExperiment/reports/stage_a1b/a1b_report.md:10-35; reports/stage_a1b/evidence.jsonl:3-22). ACCESS.md re-statuses the sub-test "RESOLVED — ELIGIBLE" (docs/ACCESS.md:196).
  - The account exists: "The operator holds a funded live IBKR account and a paper account, [paper account ID removed]" (docs/ACCESS.md:187-189; DECISIONS.md:445-447).
  - ADR-026 corrected the stale blocker in two documents and deliberately not in code: "A record-hygiene amendment ... touching two documents and no code." (HFExperiment/progress.md:228-229). registered.py is the file the gate enforces (registered.py:1-11; refusal 7 in reports/stage_c1/refusals.md:11-17), so the repository's enforced blocker text still says a measured quantity is unmeasurable on an account that does not exist.
- **Recomputation (if any):** none.
- **What would resolve it:** Update the DeferredParameter reason strings in registered.py to cite the A.1b measurement (MinSize 0.0001 on all 20 names) and state what actually still blocks Amendment 1 (the whole-share-only channel at this stake), or record in ADR-026 why code was left stale.
- **Confidence:** HIGH — the measurement and the stale string are both verbatim in the anchored tree.
- **Invalidated by later commits?:** no — no later commit exists.
- **Disclosed by authors?:** no — ADR-026 discloses the ACCESS.md and ADR-003 staleness (DECISIONS.md:432-443) but states that no code was touched without noting that code carries the same stale claim.

---

### DRAFT-all-6
- **Repository / SHA:** HFExperiment / 82e77a021256d917c665ff6d4304c25b08f35451
- **Hypothesis or artifact:** Dates in the closure entry and the ADR-026 progress entry versus the git objects that record them.
- **Direction:** A
- **Class:** PROVENANCE
- **Severity:** S4
- **Label:** DERIVED
- **Claim challenged (verbatim quote):** "Experiment closed by operator decision, instruction dated 2026-08-26." — HFExperiment/REGISTRATION.md:308 (also progress.md:7-8)
- **Evidence:**
  - Commit f13e1d3c39555d445e8f4ab21db51b99a8478f8b ("docs: terminal closure, shadow timer disarmed, closure recorded in amendment log and progress") has author and committer epoch 1787643929 = 2026-08-25T07:45:29Z (00:45:29 at the recorded -0700 offset). The entry it introduces cites an instruction dated the following day. Read via `git cat-file -p` on the live repo, 2026-09-03T04:54Z.
  - Same pattern for ADR-026: progress.md:226 is headed "2026-08-28T22:10Z — ADR-026" while commit 82e77a0 has epoch 1787951648 = 2026-08-28T21:14:08Z, 56 minutes before the stated time.
  - Other stated times are consistent with their commits (A.1b run 02:57-03:07Z, commit 03:09:06Z; C.1 render 02:40:23Z, commit 02:46:28Z), so the clock is not uniformly off.
- **Recomputation (if any):** Epoch conversions above (Python datetime, UTC). Closure commit minus A.1b commit = 4.61 h.
- **What would resolve it:** Correct the instruction date in the closure entry (or explain the discrepancy), and correct the ADR-026 timestamp in progress.md. The date matters because it fixes how soon after BLOCKED the shadow series was disarmed (DRAFT-all-1).
- **Confidence:** HIGH — epochs are from the commit objects.
- **Invalidated by later commits?:** no — commit objects are immutable; a later entry could only annotate.
- **Disclosed by authors?:** no.

---

### DRAFT-all-7
- **Repository / SHA:** HFExperiment / 82e77a021256d917c665ff6d4304c25b08f35451
- **Hypothesis or artifact:** Stage B.2, described at closure as registered and unrun.
- **Direction:** A
- **Class:** INTERNAL_INCONSISTENCY
- **Severity:** S4
- **Label:** READ
- **Claim challenged (verbatim quote):** "End state. Stages A.1 through C.1 complete and green. A.1b verdict BLOCKED. B.2 registered and unrun." — HFExperiment/progress.md:17-18
- **Evidence:**
  - No registration of a stage B.2 exists anywhere in the anchored tree: grep for "B.2" over all .md, .py, Makefile and pyproject returns only progress.md:18. Over the full git history, `git log --all -p -S'B.2'` returns the same single line (closure commit f13e1d3). ADR-002 refers to "Stages A.1 through D.1 as registered in the stage prompt" (DECISIONS.md:22), so B.2 may live in an external stage prompt that the repository never copied in.
  - Consequence for the reopen ledger: the closure names an unrun registered stage whose content, purpose and reopen conditions cannot be characterised from the record. Sections 1 through 12 state that they are "the binding pre-registration" (REGISTRATION.md:3), so a registered-but-absent stage is a gap in the binding record.
- **Recomputation (if any):** none.
- **What would resolve it:** Append B.2's registration text (or a pointer to where it is recorded) to REGISTRATION.md or progress.md, with its status and reopen conditions.
- **Confidence:** HIGH that the repository does not register B.2; the stage may be defined outside the repository.
- **Invalidated by later commits?:** no — no later commit exists.
- **Disclosed by authors?:** no.

---

## What I checked and found sound

Where the direction-A thesis did NOT hold, with references.

1. **The fractional-through-API measurement itself (the deciding evidence for the broker verdict).** n = 3 decimal orders on 2 names (MU, TE) across 2 order types, 1 cashQty order, 1 whole-share control; each fractional order refused at validation with an explicit code, control accepted (reports/stage_a1b/a1b_report.md:49-93; evidence.jsonl:28-49). For a deterministic API validation rule this n is adequate; nothing here is a thin-sample dismissal. Codes 10243 and 10244 are genuine IBKR TWS API message codes with exactly the quoted text (interactivebrokers.github.io/tws-api/message_codes.html, fetched 2026-09-03).
2. **The untested Web API channel (hunt item 1).** ACCESS.md:11 names "TWS API and Web API" and only the TWS API was exercised. But the repository's own cited Elite Trader thread reports the Web API rounding cashQty "down to whole shares" (ACCESS.md:219-221), and an external source (github.com/erdewit/ib_insync/discussions/706, statement dated 2024-03-05, fetched 2026-09-03) states "IBKR has never supported fractional equity shares via the API". The untested variant would not have cleared the GO bar. No finding.
3. **The Trade-in-Fractions account permission.** The struck ACCESS.md text (docs/ACCESS.md:184-187) notes a paper account inherits the live account's permissions; A.1b never recorded the permission state and instead argued from instrument-level SizeIncrement (a1b_report.md:37-40), which is not the same thing. However, the external sources above indicate the API refuses fractional equities regardless of permission, so this gap does not reopen the verdict. Noted, not a finding.
4. **The registered verdict clock.** 2,061 and 2,852 days reproduce exactly from the registered constants (recompute section A). Pointwise 604 days and 80-percent-power 1,379 days are the fixed-horizon comparators; the sequential design costs roughly 1.5x a fixed-horizon test at matched power, which is the ordinary price of always-valid inference. The "eight to eleven years" statement (REGISTRATION.md:261) is honest.
5. **Power-law interpolation and IR arithmetic (Section 4, ADR-009).** TE exponent ln(31.70/66.40)/ln(10) = -0.321; excess exponent -0.445; width-20 TE 42.54, excess 15.10, IR 0.894; (1.062/0.894)^2 = 1.41. All reproduce.
6. **Cost hurdle 4.07 bp/day.** 2 names x 0.2 weight x 213.84 bp round trip / 21 sessions = 4.073 (cost_table.md:36). Reproduces. Note (not a finding): under whole-share Tiered at 180 USD the same arithmetic gives about 1.0 bp/day (cost_table.md:19), and the registration deliberately chose the worst-case regime (REGISTRATION.md:250-251).
7. **Kill-floor touch probabilities (ADR-011).** 1.045, 1.306 and 1.567 sigma for floors 600/500/400 give driftless one-year touch probabilities 0.296, 0.192, 0.117; the registered 30/19/12 percent reproduce.
8. **DEGRADED closure in substance (ADR-012).** The conclusion "no live sleeve at this stake" holds a fortiori: one share each of the 2026-07-01 width-20 book costs 7,890 USD at stored closes (formations.json) or 6,240 USD at A.2 mids (book_spreads.json per_name.median_mid), and the width-5 book alone costs 3,555 / 2,760 USD, because SNDK exceeds 900 USD by itself.
9. **Choice of width 5 as primary (hunt item 6).** Among recorded and interpolated widths, 5 carries the highest IR (REGISTRATION.md:113-118), so within the registered rule the highest-SNR endpoint was chosen. A beta- or sector-hedged residual endpoint is not considered anywhere (grep "beta": REGISTRATION.md:219-223 and DECISIONS.md:175-188, kill floor only) and would plausibly lower the 418 bp noise on a book the authors call "four correlated sector bets" (REGISTRATION.md:126-128), but nothing in this repository lets me quantify the gain, so I make no finding. Flagged for the cross-repository pass against the AiTrader round that produced the 27.99 bp / IR 1.062 figures.
10. **Stale "operator holds no IBKR account" blocker (hunt item 2).** Genuinely stale from 2026-08-25 to 2026-08-28 and disclosed and corrected by the authors in ADR-026 (DECISIONS.md:432-479; docs/ACCESS.md:173-190). Not presented as a finding.
11. **The runnable billing-plan sub-test.** Disclosed as "runnable and unscheduled" (progress.md:268-271; ACCESS.md:199). Not a finding; entered in the reopen ledger.
12. **Other brokers (hunt item 7).** The broker table covers IBKR Canada, Alpaca, Questrade and Wealthsimple (ACCESS.md:9-14). I cannot state a concrete citation that any other broker clears all four bars (Canadian resident, US equities, order API, fractional through the API) so I make no finding.
13. **Spread measurement.** 20 of 20 names, 3 sessions, 9 cells each, median 12.77 bp (progress.md:156-161; book_spreads.json). Not a closure input in dispute.

Observations that are NOT direction A (left for the B pass / hygiene), recorded so they are not lost:
- REGISTRATION.md:152-154 "A 5-name book gets one share per name, 720 of 900 deployed, with equal weighting destroyed by per-name prices from 22 to 1,595 USD." 720 is 5 x the 144 median, not the sum of five prices; the 22-1,595 range is the width-20 book's A.2 mids (PL 22.305, SNDK 1,595.19 in book_spreads.json), not the width-5 book's. One share each of the width-5 book costs 2,760 USD at those mids. The conclusion is unaffected (stronger, in fact); the arithmetic sentence is wrong. Likewise "20 names at one share each already cost about 2,880 USD" (REGISTRATION.md:152-153) is 20 x median; the actual sum is 6,240-7,890 USD.
- REGISTRATION.md:215-216 "The floor is 500 USD of total account equity, a 400 USD loss on 900 deployed after the 100 buffer, 1.31 sigma": 1.31 sigma of 42.54 percent on 900 USD is a 500 USD loss (equity 1,000 to 500); a 400 USD loss is 1.045 sigma, which the same paragraph assigns to the 600 floor. The touch probabilities are computed on the 500 USD loss and are right; the sentence is not.
- REGISTRATION.md:279-280 "A documented negative is a valid outcome at a cost of roughly 30 to 60 USD a year": per DRAFT-all-3 the negative is unreachable in under about 74 trading years at a true mean of zero, and the 30-60 USD is the live drag, not a shadow-series cost (the shadow series costs nothing per REGISTRATION.md:38).
- DECISIONS.md numbering jumps from ADR-022 to ADR-026; `git log --all -p -S` finds no ADR-023, -024 or -025 ever committed.

## Live-repo access log

Live path: /home/kiros-li/Documents/GitHub/HFExperiment. Operations: `git status --porcelain`, `git rev-parse HEAD`, `git log`, `git branch -a`, `git status --porcelain --ignored`, `git cat-file -p` on three commits, `git show --stat` on one commit, `git log --all -p -S` for ADR-023/024/025 and B.2; a `find -printf` listing of data/ (no file under data/ was opened); `cat .env.example` (a tracked file identical to the snapshot; .env itself was not read). No checkout, write, or script execution. Untracked data listed (UNANCHORED, read 2026-09-03T04:54:35Z, may change): data/bars.db (40,960 bytes, mtime 2026-08-24 17:34), data/c1_formation.db (105,005,056 bytes, mtime 2026-08-24 19:31), data/ledger/ (dir). Ignored entries also present: .env, .venv/, caches.

Before (2026-09-03 ~04:47Z):
```
?? Accept:
?? GET
?? Host:
?? User-Agent:
```
After (2026-09-03T05:00:42Z):
```
?? Accept:
?? GET
?? Host:
?? User-Agent:
```
Both match the pre-existing owner stray files named in COMMON_RULES.md. No other entries.
