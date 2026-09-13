# Agent A findings — HFExperiment

Repository: HFExperiment, anchored SHA `82e77a021256d917c665ff6d4304c25b08f35451` (main, 2026-08-28).
Direction A: the program closed hypotheses too early or too hard. Content read from
SNAP/HFExperiment; git objects and working-tree listings read read-only from the live repository
(log at the end). Recomputations are in
`scratchpad/work/agentA/recompute_hf.py` and `recompute_hf.out`, re-verified independently at
consolidation.

## Summary — the strongest case for the thesis in this repository

HFExperiment pre-registered a two-series design whose entire point was that the signal question
survives any broker outcome: under BLOCKED, "Phase B proceeds unchanged, because the shadow series
needs no broker, no account, and no money. The signal question still gets answered."
(REGISTRATION.md:37-39), and ADR-002 states that a later stage coupling the shadow series to a
broker dependency "violates this ADR" (DECISIONS.md:28-29).
The broker test fired BLOCKED at 2026-08-25T03:09:06Z; 4.61 hours later, commit `f13e1d3` disarmed
the shadow timer before its first accrual and declared the closure "terminal" — n = 0 observations,
no reason recorded beyond "operator decision", and no reopen condition registered for the signal
question at all.
The broker verdict that triggered it is itself mislabelled: a reachable broker cleared every
registered bar except fractional-through-the-API, which is the registered DEGRADED definition word
for word, and the two branches carry different reopeners — BLOCKED's are external, DEGRADED's ("a
materially larger stake") is in the operator's own hands.
And the instrument that was disarmed could never have produced the "documented negative" the
registration advertises: evaluating the repository's own boundary function with its own frozen
constants, the futility bar (10 bp/day, sitting *above* the 4.07 bp/day success hurdle) is first
crossed at day 18,650 — 74 trading years — at a true mean of zero.
The record states plainly that "The verdict was never computed" and that there were "zero shadow
observations, because the series never started" (REGISTRATION.md:312-315). What no entry states is
the consequence — that H-F is left untested in this repository for the second time (README.md:3-5)
rather than falsified — or any reopen condition for the signal question.

---

## AUDIT-A-HFExperiment-1

- **Repository / SHA:** HFExperiment / 82e77a021256d917c665ff6d4304c25b08f35451
- **Hypothesis or artifact:** H-F signal hypothesis (REGISTRATION.md Section 1) and the SHADOW series
  that was its only instrument; the "2026-08-26" terminal closure.
- **Direction:** A
- **Class:** OVER_CLOSED
- **Severity:** S2
- **Label:** DERIVED — commit objects (`git cat-file` / `git log --format=%at`) fix the timing, and
  the reachability recomputation evaluates constants and a formula read out of
  `src/hfexperiment/registered.py` and `src/hfexperiment/verdict.py`.
- **Claim challenged (verbatim quote):**
  "The shadow series was disarmed before its first accrual: hfexperiment-bars.timer stopped and
  disabled via systemctl --user, verified that no HFExperiment unit remains scheduled. The verdict
  was never computed. Closure is terminal." — HFExperiment/REGISTRATION.md:309-313
- **Evidence:**
  - The registration pre-committed that the broker outcome cannot stop the signal series: "BLOCKED
    ... Consequence: phases C and D stop. Phase B proceeds unchanged, because the shadow series needs
    no broker, no account, and no money. The signal question still gets answered." —
    HFExperiment/REGISTRATION.md:33-39. ADR-002: "If the broker question resolves BLOCKED, phase B
    still runs and still answers the signal question. Only phases C and D die. This property is the
    reason the two-series design was chosen. Changes it: nothing. A later stage that couples the
    shadow series to a broker dependency violates this ADR." — HFExperiment/DECISIONS.md:24-29.
  - The A.1b stage entry, written the same night, still says so: "The shadow series carries the
    experiment alone and answers the signal question, which was the design's point." —
    HFExperiment/progress.md:42-44.
  - Timing from git objects (live repo, read-only, re-verified 2026-09-03T05:08Z): A.1b commit
    `669eb5c` ("feat: A.1b paper capability test fires Section 0 BLOCKED") author/committer epoch
    1787627346 = 2026-08-25T03:09:06Z; closure commit `f13e1d3` ("docs: terminal closure, shadow
    timer disarmed ...") epoch 1787643929 = 2026-08-25T07:45:29Z. Gap 16,583 s = 4.61 h. The A.1b run
    itself ended 03:07Z (HFExperiment/reports/stage_a1b/a1b_report.md:3). The closure diff touches
    only REGISTRATION.md and progress.md.
  - State of the instrument at the last recorded health view, "generated 2026-08-25T00:34:28Z"
    (HFExperiment/reports/monitor/health.txt:1) — about seven hours before the closure commit, not at
    the moment of disarming: timer "is-enabled: enabled / is-active: active", "next formation:
    2026-09-01, in 7 days" (HFExperiment/reports/monitor/health.txt:4-10); "observations: 0" at all
    three registered widths (HFExperiment/reports/monitor/verdict.txt:5,14,23). n = 0 shadow
    observations, stated in the closure entry itself: "zero shadow observations, because the series
    never started" (REGISTRATION.md:314-315).
  - The closure entry gives no reason beyond "operator decision" (REGISTRATION.md:308;
    progress.md:7-8) and registers no reopen condition for the signal question. The only reopen
    clauses anywhere in the repository concern the *live* table: "IBKR shipping fractional support in
    the TWS API, or an Alpaca Canadian launch" (HFExperiment/DECISIONS.md:427-428; progress.md:44-46).
  - The operator had accepted the 8-to-11-year clock one day earlier with eyes open: "Eight to eleven
    years. The operator knows this and proceeds because the execution question is answerable now and
    the signal question is not." — HFExperiment/REGISTRATION.md:261-263; acceptance recorded
    2026-08-24 (REGISTRATION.md:286-295; DECISIONS.md:230-242). Between acceptance and closure the
    only new fact was the broker result, which the design had declared irrelevant to the shadow
    series.
  - The one known technical pre-start item was a one-line fix the authors themselves sized: "the
    2026-09-01 formation run will fail loudly until a one-line fix lands under B.1 authorization"
    (HFExperiment/progress.md:87-89; DECISIONS.md:378-387). It was cancelled rather than applied:
    "B.1a cancelled as moot: no formation will ever call the assets endpoint." (progress.md:18-19).
  - This is the second time H-F has been closed without a signal verdict: "tested once in the AiTrader
    cross-sectional round of 2026-07-26 and resolved on statistical power rather than absent signal."
    — HFExperiment/README.md:3-5.
- **Recomputation:** Reachability of the instrument that was disarmed, from the registered inputs
  (mean 27.99 bp/day, sigma 418 bp/day, rho 0.071641, alpha 0.05 —
  HFExperiment/src/hfexperiment/registered.py:91,104-107; radius formula
  src/hfexperiment/verdict.py:26-34): the lower bound clears zero at day 2,061 and clears 4.07 at day
  2,852, reproducing REGISTRATION.md:259-261 and registered.py:106-107 exactly (radius(2061)=27.986
  against a mean of 27.99; radius(2852)=23.919, 27.99-23.919=4.071). Fixed-horizon comparators:
  pointwise n at 1.645 sigma = 604 days; 80 percent power = 1,379 days. So a positive verdict was
  reachable in 8-11 years at the registered effect (n = 1 registered effect estimate, itself imported
  from AiTrader). Cost of continuing, per the registration: none in money (REGISTRATION.md:38;
  DECISIONS.md:22-24); the daily run needs only Alpaca data keys, which progress.md:99-100 records as
  already in `.env`.
- **What would resolve it:** An appended amendment that (a) states the actual ground for disarming a
  zero-observation shadow series (a resource or clock decision is inferable from
  REGISTRATION.md:261-263 but is nowhere recorded), (b) acknowledges that it departs from Section 0's
  BLOCKED consequence and from ADR-002, and (c) registers a reopen condition for the signal question
  itself — for example, re-arm at the next formation if any broker clears the GO bar, or if another
  repository produces a powered momentum test. Alternatively, re-arm the timer: the pipeline exists,
  is tested (158 tests green, progress.md:92), and the series is formation-aligned, so any
  first-of-month start is registration-clean (DECISIONS.md:244-256) and ADR-015's "nothing after the
  series starts" (DECISIONS.md:255-256) does not bind a series that never started.
- **Confidence:** HIGH — the contradiction between the registered BLOCKED consequence and the closure
  is textual, and the 4.61 h timing is from commit objects; the advocacy part is the judgment that
  the closure was premature rather than merely unexplained, and the honest counterweight is the
  8-11 year clock the operator had already accepted in writing.
- **Could later commits invalidate this?:** No. The anchored SHA is the live HEAD as of
  2026-09-03T05:08Z and no commit exists after it. A later amendment stating the reason or re-arming
  the series would change the status of the hypothesis but not the record at this SHA.
- **Disclosed by authors?:** No. The disarming itself is recorded, and so is its result — "The
  verdict was never computed", "zero shadow observations, because the series never started"
  (REGISTRATION.md:310-315; progress.md:12-15) — but no entry acknowledges that the closure
  contradicts Section 0 and ADR-002, states a reason, or registers a reopen condition for the signal
  question.
- **Citation check:** corrected — quote citation REGISTRATION.md:310-313 changed to 309-313, because
  the quote's opening word "The" sits at the end of line 309 (verifier 2's reading; I checked the
  snapshot and followed it over verifier 1's 310-313, which starts the quote one word late). The
  health-state bullet now says "last recorded health view, generated 2026-08-25T00:34:28Z
  (health.txt:1), about seven hours before the closure commit" instead of "at the moment it was
  disarmed", which overstated what health.txt shows (verifier 1). The no-money citation
  DECISIONS.md:22-23 becomes 22-24, since "and no money" falls on line 24 (verifier 1). The summary
  paragraph was amended to credit the authors' own statement at REGISTRATION.md:312-315 (verifier 2).
  Quote EXACT, figures YES; class, severity S2, label DERIVED and the disclosure verdict unchanged,
  both verifiers judging S2 conservative rather than high.

---

## AUDIT-A-HFExperiment-2

- **Repository / SHA:** HFExperiment / 82e77a021256d917c665ff6d4304c25b08f35451
- **Hypothesis or artifact:** The Section 0 broker outcome verdict of 2026-08-25 (REGISTRATION.md
  amendment log) and the A.1b report that produced it.
- **Direction:** A
- **Class:** INTERNAL_INCONSISTENCY
- **Severity:** S2
- **Label:** READ — the deciding evidence is the registered definitions and the A.1b report text. The
  supplementary stake arithmetic in the recomputation field is derived from stored formation JSON but
  is not load-bearing for the finding.
- **Claim challenged (verbatim quote):**
  "BLOCKED. The IBKR TWS API refused fractional quantities however phrased on paper account
  [paper account ID removed], error 10243 on decimal totalQuantity across two book names and two order types, error
  10244 on cashQty, while a whole-share control order was accepted" —
  HFExperiment/REGISTRATION.md:299-302
- **Evidence:**
  - The registered definitions, fixed before measurement: "DEGRADED: A broker clears every bar except
    fractional-through-the-API." (HFExperiment/REGISTRATION.md:21-23); "BLOCKED: No reachable broker
    clears the bars." (REGISTRATION.md:33-35).
  - The measured outcome: IBKR Canada clears residency, US equities and an order-placing API
    (HFExperiment/docs/ACCESS.md:11,16-17); the whole-share control order was "ACCEPTED and queued"
    (reports/stage_a1b/a1b_report.md:91-93; ACCESS.md:197); only fractional-through-the-API refused
    (a1b_report.md:67-70,78-82). n = 3 decimal orders on 2 names (MU, TE) across 2 order types, all
    refused with error 10243; 1 cashQty order refused with 10244; 1 whole-share control accepted.
    That is the DEGRADED definition word for word: a reachable broker clears every bar but one.
  - The repository's own A.1 stage had already ruled BLOCKED out and said the test could only resolve
    the other two: "BLOCKED is ruled out on documented bars. The GO versus DEGRADED verdict is
    UNDECIDED" (HFExperiment/DECISIONS.md:39-40); "Changes it: the Task 3 test resolves GO or
    DEGRADED." (DECISIONS.md:65-66); "GO versus DEGRADED undecided pending Task 3. BLOCKED ruled out
    on documented bars." (HFExperiment/progress.md:222-223).
  - The A.1b report justifies BLOCKED by GO's failure alone: "Section 0 fires BLOCKED. The registered
    GO bar requires the API to accept fractional quantities at 45 USD per name."
    (a1b_report.md:107-108) — and in the same paragraph applies the DEGRADED branch: "Per Section 6,
    DEGRADED whole-share sizing stays closed at this stake." (a1b_report.md:113-114). Both labels are
    applied to one outcome without noting that the taxonomy makes them exclusive. ADR-026, three days
    later, reaffirms "the Section 0 BLOCKED stands exactly as recorded" (progress.md:256-257).
  - Why the label matters for direction A: the two branches carry different registered reopeners.
    BLOCKED's are external and out of the operator's control ("IBKR shipping fractional support in
    the TWS API, or an Alpaca Canadian launch", DECISIONS.md:427-428). DEGRADED's is in the
    operator's hands: "Changes it: a materially larger stake, which is a new registration, not an
    amendment." (HFExperiment/DECISIONS.md:201-202). Every closure entry (REGISTRATION.md:297-315;
    progress.md:5-21,39-46) carries only the BLOCKED reopeners, and ADR-012's larger-stake reopener
    (DECISIONS.md:201-202) is carried into no post-A.1b entry: "larger stake" occurs exactly once in
    the whole repository, at DECISIONS.md:201. What the post-A.1b entries do record is the
    stake-conditionality itself — the branch "stays closed at this stake"
    (reports/stage_a1b/a1b_report.md:113-114; progress.md:42,54), "closed at the registered stake"
    (progress.md:269-270), and "Whole-share API trading was never closed; only slicing is"
    (progress.md:258-259), matching ACCESS.md:197: "Whole-share through the API stays open; only
    slicing is closed". So the path is signposted as technically open at a larger stake; what no
    entry does is carry ADR-012's reopener, or the DEGRADED label it belongs to, into the record.
- **Recomputation:** What "materially larger stake" would have to mean, from stored prices.
  2026-08-03 width-20 book entry closes (HFExperiment/reports/stage_c1/formation_2026-08-03.json,
  key `width20_entry_closes`, n = 20 names): one share of each = 5,936 USD; equal-weight with one
  share of the priciest (SNDK 1,214.83) = 24,297 USD. Width-5 book (SNDK, AXTI, WOLF, MU, WDC; same
  file, `books.5`, n = 5): one share each = 2,667 USD; equal-weight at one SNDK share = 6,074 USD. At
  the 2026-07-01 closes (reports/stage_a1/formations.json, `formations.2026-07-01`, n = 5) the
  width-5 book is 3,555 USD one-share-each and 11,369 USD equal-weight (SNDK 2,273.73). So a
  whole-share DEGRADED sleeve exists at roughly 3x to 24x the registered 1,000 USD stake depending on
  width and weighting tolerance. Whether that is achievable is the operator's call; the point is that
  the record's label means the question never arises.
- **What would resolve it:** An amendment re-labelling the 2026-08-25 verdict as DEGRADED with the
  branch closed at this stake, per Section 0 and Section 6; carrying ADR-012's larger-stake reopener
  into the closure record; and stating the stake at which a whole-share sleeve becomes survivable
  (the arithmetic above, or the authors' own). Alternatively, an amendment explaining why the
  whole-share control acceptance does not satisfy "clears every bar except
  fractional-through-the-API".
- **Confidence:** HIGH — the definitional mismatch is verbatim and the authors' own A.1 stage records
  that BLOCKED was already ruled out. The practical consequence at 1,000 USD is identical under
  either label, which is why this is S2 and not S1: no stated outcome is wrong, but the label
  contradicts the evidence in the same report.
- **Could later commits invalidate this?:** No. No commit exists after the anchor, and ADR-026 — the
  last commit — explicitly reaffirms the BLOCKED label.
- **Disclosed by authors?:** No for the limitation raised — the label conflict. a1b_report.md:107-114
  applies both Section 0 BLOCKED and Section 6 DEGRADED to the same outcome without acknowledging
  that the taxonomy makes them exclusive, and no entry revisits ADR-003's "the Task 3 test resolves
  GO or DEGRADED" (DECISIONS.md:65-66). Partial disclosure of the stake-conditional *consequence*,
  which is a different point: ADR-026 states "Whole-share API trading was never closed; only slicing
  is" (progress.md:258-259) and ACCESS.md:197 says the same, and the A.1b report and progress entries
  qualify the closure "at this stake" (a1b_report.md:113-114; progress.md:42,54,269-270). Severity
  stays S2 because the disclosed part is not the limitation raised.
- **Citation check:** corrected — quote range tightened from REGISTRATION.md:299-303 to 299-302,
  since the quoted text ends at "accepted," on line 302 (verifier 1; verifier 2 accepted 299-303 as
  within tolerance, and I took the tighter range after checking the snapshot). The sentence "the
  larger-stake path is not mentioned in any post-A.1b entry" was too broad (verifier 2) and is
  replaced by the precise claim, verified in the snapshot: "larger stake" occurs exactly once in the
  tree (DECISIONS.md:201) and ADR-012's reopener is carried into no post-A.1b entry, while the
  stake-conditionality itself is recorded at a1b_report.md:113-114, progress.md:42,54,269-270,
  progress.md:258-259 and ACCESS.md:197. The disclosure field now records that partial disclosure and
  the JSON carries a disclosure_ref. Quote EXACT, figures YES; severity S2 and label READ unchanged.

---

## AUDIT-A-HFExperiment-3

- **Repository / SHA:** HFExperiment / 82e77a021256d917c665ff6d4304c25b08f35451
- **Hypothesis or artifact:** Section 11 verdict schedule — futility bar 10 bp/day against a success
  hurdle of 4.07 bp/day — and the registered claim that the shadow series can produce a documented
  negative.
- **Direction:** A
- **Class:** STATISTICAL
- **Severity:** S2
- **Label:** DERIVED — the constants and the boundary function were read out of
  `src/hfexperiment/registered.py` and `src/hfexperiment/verdict.py` (code) and evaluated; this is
  not arithmetic on numbers printed in prose.
- **Claim challenged (verbatim quote):**
  "Success when the lower bound clears the measured cost hurdle of 4.07 bp per day ... Futility when
  the upper bound falls below 10 bp per day." — HFExperiment/REGISTRATION.md:249-252; and
  "A documented negative is a valid outcome at a cost of roughly 30 to 60 USD a year at the traded
  width" — HFExperiment/REGISTRATION.md:279-280
- **Evidence:**
  - The thresholds as enforced code: `futility_bp_per_day: float = 10.0`
    (HFExperiment/src/hfexperiment/registered.py:70); `cost_hurdle_bp_per_day: float = 4.07`
    (registered.py:78); classification order success-then-futility
    (src/hfexperiment/verdict.py:92-101). Noise: sigma 418 bp/day (registered.py:105;
    REGISTRATION.md:256-257). The monitor prints both bars side by side —
    "success bar: lower bound above 4.07 bp/day / futility bar: upper bound below 10.0 bp/day"
    (reports/monitor/verdict.txt:8-9).
  - No derivation of the 10 bp figure exists anywhere in the repository: `grep -rni "futility"` over
    all `.md` returns exactly n = 1 hit, REGISTRATION.md:251, which states the bar without deriving
    it (the case-sensitive form returns 0, because the word is capitalised there). The 4.07 hurdle by
    contrast carries a full derivation and a pinning test (registered.py:71-78).
  - The futility bar sits ABOVE the success hurdle. Because the sequence is symmetric about the
    sample mean, futility fires before success whenever the true mean is below (10 + 4.07)/2 = 7.035
    bp/day. A true excess of 4.07 to 7.03 bp/day — 10 to 18 percent per year, net-positive after the
    registered costs, i.e. exactly the economic content of Section 1's "a fee-paying participant
    keeps most of it" (REGISTRATION.md:55-56) — is classified FUTILE before it can be classified
    SUCCESS. That is a mechanism for closing the hypothesis too hard.
  - The claim that a negative is an attainable outcome is falsified by the same boundary function:
    the futility bar is unreachable at any human horizon. See the recomputation.
- **Recomputation:** Inputs: sigma 418 bp/day (registered.py:105), rho 0.071641 (registered.py:91),
  alpha 0.05 (registered.py:67), radius formula verdict.py:26-34, bars registered.py:70,78. Method:
  the first day t at which mean + radius(t) < 10 (futility) or mean - radius(t) > 4.07 (success),
  scanning t. Results (n = 1 boundary function, 8 hypothesised true means):
  true mean 0.00 bp/day — futility at day 18,650 (74.0 trading years), success never;
  4.07 — futility at day 58,309; 6.00 — futility at day 137,247; 7.03 — futility at day 261,550
  versus success at day 263,464 (futility first); 8.00 — success at day 142,605, with futility not
  reached until day 613,782 (about 2,436 trading years), so success first;
  15.10 (the interpolated width-20 excess, REGISTRATION.md:117) — success at day 15,060;
  27.99 — success at day 2,852 (matches the registration). Width-50 secondary at its recorded 10.04
  bp/day (REGISTRATION.md:118), sigma 199.69 bp/day (unrounded 199.6912) implied by TE 31.70 percent,
  alpha 0.025 — success at day 13,178 (the rounded 199.7 gives 13,180). Cross-check: the registered
  clear-zero day 2,061 and clear-hurdle day 2,852 reproduce exactly, so the implementation of the
  boundary is the repository's own.
- **What would resolve it:** Either register a derivation for the 10 bp futility bar and state
  plainly that the design has no achievable negative — so that "The signal question still gets
  answered" (REGISTRATION.md:39) holds only on the positive side — or re-register futility as a bound
  on the lower side of the economic hypothesis (for example, upper bound below the 4.07 cost hurdle)
  together with the horizon at which it becomes reachable. For the closure record specifically: state
  that H-F leaves this repository untested rather than falsified, because no negative verdict was
  ever reachable and none was computed.
- **Confidence:** HIGH — the arithmetic is a direct evaluation of the repository's own boundary
  function with its own frozen constants, independently reproduced at consolidation, and it
  reproduces the registration's published day numbers exactly. Rated S2 rather than S1 because the
  series never ran: no verdict was actually misclassified, so no conclusion the repository states is
  wrong *because of* this bar. Rated S2 rather than S3 because "A documented negative is a valid
  outcome" is a claim in the binding pre-registration that the repository's own constants contradict,
  not merely a stale figure.
- **Could later commits invalidate this?:** No. The constants and formula are pinned by tests
  (tests/test_verdict.py; tests/test_verdictengine.py, per registered.py:88-90,102-103) and no commit
  exists after the anchor.
- **Disclosed by authors?:** No. The registration discloses the slow *positive* clock
  (REGISTRATION.md:255-263) but nowhere states that the futility bar sits above the success hurdle or
  that a negative is unreachable. Note for the B pass: the same sentence at REGISTRATION.md:279-280
  is also a candidate direction-B finding (claiming more than the design delivers).
- **Citation check:** corrected — both verifiers found the same two defects and I reproduced both
  from the repository's own boundary function. (1) "true mean 8.00 — success at day 142,605, futility
  never" was wrong: the radius decays monotonically, so futility is first crossed at day 613,782
  (about 2,436 trading years); the row now reads "success first". The mechanism is untouched, since
  success fires 4.3x earlier at that mean. (2) The grep as written was case-sensitive and returns 0
  hits in `.md`; the single hit is "Futility" capitalised at REGISTRATION.md:251, so the command now
  reads `grep -rni` and the count n = 1 stands. Also stated the width-50 sigma as the unrounded 199.69
  (199.6912) rather than 199.7, because that is what reproduces day 13,178 (199.7 gives 13,180) —
  verifier 1's note, confirmed. Quote EXACT; figures PARTIAL as submitted, YES after correction;
  severity S2 kept, both verifiers judging the self-imposed cap conservative and the reasoning
  explicit.

---

## AUDIT-A-HFExperiment-4

- **Repository / SHA:** HFExperiment / 82e77a021256d917c665ff6d4304c25b08f35451
- **Hypothesis or artifact:** The broker table verdict (docs/ACCESS.md) and its registered recheck
  trigger for Alpaca's Canadian exclusion.
- **Direction:** A
- **Class:** PROCESS
- **Severity:** S3
- **Label:** READ — the trigger and its absence are established from documents; the corroborating web
  fetch is external and UNANCHORED.
- **Claim challenged (verbatim quote):**
  "Alpaca excludes Canadian residents today. Its careers page advertises a Canadian broker-dealer
  controller role, so the exclusion may lift. Recheck at stage C if Task 3 resolves badly." —
  HFExperiment/docs/ACCESS.md:17-20
- **Evidence:**
  - The trigger fired: Task 3 resolved badly on 2026-08-25 (REGISTRATION.md:297-304). Stage C.1 ran
    the same night (progress.md:56-100) and A.1b after it (progress.md:23-54). n = 0 recorded
    rechecks across the four post-trigger entries: neither C.1, nor A.1b, nor the closure
    (progress.md:5-21), nor ADR-026 three days later (DECISIONS.md:432-479; progress.md:226-271)
    records a recheck of the Alpaca eligibility page. The three post-trigger mentions all restate
    the clause as a *future* reopener: "an Alpaca Canadian launch would reopen the table"
    (reports/stage_a1b/a1b_report.md:115-116; progress.md:44-46; ADR-022 at DECISIONS.md:427-428).
  - The honest counterweight: the occasion the trigger names had already passed by the time its
    condition was met. Stage C.1 rendered its refusals at 2026-08-25T02:40:23Z
    (reports/stage_c1/refusals.md:3), before A.1b — the test that resolved Task 3 badly — ran 02:57
    to 03:07Z (reports/stage_a1b/a1b_report.md:3), and C.2 and D.1 were then declared "moot at this
    stake" (progress.md:53-54). So "Recheck at stage C" was arguably unexecutable as literally
    worded. What remains is that no entry records either the recheck or that fact.
  - The blocker's cited source is `https://alpaca.markets/support/countries-alpaca-is-available`
    quoting "Residents of Canada are not currently eligible", retrieved 2026-08-23
    (ACCESS.md:31-32). Fetched 2026-09-03T04:58Z (WebFetch, UNANCHORED, may have changed since): the
    page, dated February 2026, lists no countries and says only "Please contact support ... for more
    information regarding whether your country is supported." A third-party page (brokerchooser.com,
    "Is Alpaca Trading Available to Investors in Canada?", stated last updated 2026-03-11, via
    WebSearch 2026-09-03) still says Canadian residents are not eligible. So the blocker probably
    still holds, but its cited primary source no longer states it and the registered recheck was
    never performed.
- **Recomputation:** None.
- **What would resolve it:** Perform and date the registered recheck of Alpaca eligibility for
  Canadian residents and append the result to ACCESS.md. If the exclusion has lifted, the BLOCKED
  reopener at DECISIONS.md:427-428 is met and the live table reopens as a new measurement per
  ADR-022.
- **Confidence:** HIGH that the recheck is absent from the record (a complete read of every
  post-trigger entry); LOW that Alpaca's policy has actually changed.
- **Could later commits invalidate this?:** No. No commit exists after the anchor. A dated recheck in
  a future commit would close the item but would not change the record at this SHA.
- **Disclosed by authors?:** No. The trigger is registered at ACCESS.md:19-20, but no entry
  acknowledges that it fired, that it went unexecuted, or that the stage it named had already run.
- **Citation check:** corrected — added ADR-022 (DECISIONS.md:427-428) as the third post-trigger
  restatement of the clause (verifier 1's completeness note), and added verifier 2's counterweight,
  which I checked in the snapshot: C.1 rendered at 02:40:23Z (reports/stage_c1/refusals.md:3) before
  A.1b ran 02:57-03:07Z (a1b_report.md:3), and C.2/D.1 were then declared moot (progress.md:53-54),
  so the trigger's named occasion had passed when its condition was met. Quote EXACT; figures PARTIAL
  — the repo-internal figure n = 0 rechecks was reproduced by both verifiers, while the two external
  web figures were re-fetched by neither and remain labelled UNANCHORED with their read time in the
  finding. Severity S3, label READ and the split HIGH/LOW confidence unchanged.

---

## AUDIT-A-HFExperiment-5

- **Repository / SHA:** HFExperiment / 82e77a021256d917c665ff6d4304c25b08f35451
- **Hypothesis or artifact:** Deferred parameter `broker_min_notional_usd` (Amendment 1) and its
  stated blocker, as carried in enforced code.
- **Direction:** A
- **Class:** STALE_FIGURE
- **Severity:** S3 (also the cap, because the authors partially disclosed — see below)
- **Label:** DERIVED — the stale string is a literal in `src/hfexperiment/registered.py` (code) and
  the measurement that refutes it is in `reports/stage_a1b/evidence.jsonl` (stored data), not in
  prose.
- **Claim challenged (verbatim quote):**
  `reason="MinSize and SizeIncrement come from reqContractDetails on a "` /
  `"live-permissioned account that does not exist yet",` —
  HFExperiment/src/hfexperiment/registered.py:119-120
- **Evidence:**
  - A.1b measured exactly this quantity on 2026-08-25: "All 20 names advertise fractional sizing at
    the contract layer", with MinSize 0.0001 and SizeIncrement 0.0001 for every name
    (HFExperiment/reports/stage_a1b/a1b_report.md:12,14-35 — a 20-row table, n = 20; primitives in
    reports/stage_a1b/evidence.jsonl:3-22, 20 `contract_details` records each carrying
    `"min_size":"0.0001","size_increment":"0.0001"`). ACCESS.md re-statuses the sub-test
    "**RESOLVED — ELIGIBLE**" (docs/ACCESS.md:196).
  - The account exists: "The operator holds a funded live IBKR account and a paper account,
    [paper account ID removed]" (docs/ACCESS.md:187-189; DECISIONS.md:445-447).
  - ADR-026 corrected the stale blocker in two documents and deliberately not in code: "A
    record-hygiene amendment, made in chat with the operator present, touching two documents and no
    code." (HFExperiment/progress.md:228-229). `registered.py` is the file the gate enforces
    (registered.py:1-11 — "tests/test_structural_guard.py fails if any field lacks a consumption site
    outside this file"), and its DeferredParameter reason strings surface verbatim in refusal output:
    refusal 7 reproduces the sibling parameter's reason string word for word
    (reports/stage_c1/refusals.md:11-17). So the repository's enforced text still asserts that a
    quantity measured on 20 of 20 names is unmeasurable on an account that does not exist.
- **Recomputation:** None.
- **What would resolve it:** Update the DeferredParameter reason string in registered.py:116-121 to
  cite the A.1b measurement (MinSize 0.0001 on all 20 names) and state what actually still blocks
  Amendment 1 — the whole-share-only channel at this stake — or record in ADR-026 why the code was
  deliberately left stale.
- **Confidence:** HIGH — the measurement and the stale string are both verbatim in the anchored tree,
  and the 20-row measurement was re-read from `evidence.jsonl` at consolidation.
- **Could later commits invalidate this?:** No. No commit exists after the anchor.
- **Disclosed by authors?:** Yes, partially, and the severity is capped at S3 accordingly. ADR-026
  discloses the same class of staleness in ACCESS.md and ADR-003 (DECISIONS.md:432-443) and states
  plainly that the correction touched "two documents and no code" (progress.md:228-229). What no
  entry states is that the code carries the same stale claim. This is a gap the authors signposted,
  not one they hid, and it is reported as such.
- **Citation check:** verified (quote EXACT, figures YES) — both verifiers KEEP with no change. Both
  re-counted n = 20 `contract_details` records carrying `"min_size":"0.0001","size_increment":
  "0.0001"` in reports/stage_a1b/evidence.jsonl:3-22 against the 20-row table at a1b_report.md:14-35,
  and both confirmed the partial-disclosure handling, the populated disclosure_ref and the S3 cap.

---

## AUDIT-A-HFExperiment-6

- **Repository / SHA:** HFExperiment / 82e77a021256d917c665ff6d4304c25b08f35451
- **Hypothesis or artifact:** Dates in the closure entry and in the ADR-026 progress entry, against
  the git objects that record them.
- **Direction:** A
- **Class:** PROVENANCE
- **Severity:** S4
- **Label:** DERIVED — commit author/committer epochs read from git objects.
- **Claim challenged (verbatim quote):**
  "Experiment closed by operator decision, instruction dated 2026-08-26." —
  HFExperiment/REGISTRATION.md:308 (repeated at progress.md:7-8)
- **Evidence:**
  - Commit `f13e1d3c39555d445e8f4ab21db51b99a8478f8b` ("docs: terminal closure, shadow timer
    disarmed, closure recorded in amendment log and progress") has author and committer epoch
    1787643929 = 2026-08-25T07:45:29Z (00:45:29 at the recorded -0700 offset). The entry it
    introduces cites an instruction dated the *following* day. Read via `git log --format=%at` and
    `git cat-file -p` on the live repository, 2026-09-03T05:08Z.
  - The same pattern for ADR-026: progress.md:226 is headed "2026-08-28T22:10Z — ADR-026" while the
    commit that introduces it (`82e77a0`, the anchor) has epoch 1787951648 = 2026-08-28T21:14:08Z —
    56 minutes before the stated time.
  - Other stated times are consistent with their commits (A.1b run 02:57-03:07Z, commit 03:09:06Z;
    C.1 render 02:40:23Z, commit 02:46:28Z), so the clock is not uniformly offset and this is not a
    timezone artefact. n = 2 discrepant entries out of the dated entries checked.
- **Recomputation:** Epoch conversions above (Python `datetime`, UTC). Closure commit minus A.1b
  commit = 1787643929 - 1787627346 = 16,583 s = 4.61 h.
- **What would resolve it:** Correct the instruction date in the closure entry (or explain the
  discrepancy — a same-night instruction recorded under the next day's date would be an ordinary
  explanation), and correct the ADR-026 timestamp in progress.md. The date matters because it fixes
  how soon after BLOCKED the shadow series was disarmed, which is the substance of
  AUDIT-A-HFExperiment-1.
- **Confidence:** HIGH — the epochs come from the commit objects themselves.
- **Could later commits invalidate this?:** No. Commit objects are immutable; a later entry could
  only annotate the discrepancy.
- **Disclosed by authors?:** No.
- **Citation check:** verified (quote EXACT, figures YES) — both verifiers KEEP with no change. Both
  independently re-derived the epochs from the live commit objects (f13e1d3 = 2026-08-25T07:45:29Z
  against an instruction dated 2026-08-26; 82e77a0 = 2026-08-28T21:14:08Z against the
  "2026-08-28T22:10Z" heading, 56 minutes) and confirmed the control cases that rule out a uniform
  timezone offset, so n = 2 stands.

---

## AUDIT-A-HFExperiment-7

- **Repository / SHA:** HFExperiment / 82e77a021256d917c665ff6d4304c25b08f35451
- **Hypothesis or artifact:** Stage B.2, described in the closure entry as registered and unrun.
- **Direction:** A
- **Class:** INTERNAL_INCONSISTENCY
- **Severity:** S4
- **Label:** DERIVED — the decisive part of the evidence is a git-history content search
  (`git log --all -S`), not a document read.
- **Claim challenged (verbatim quote):**
  "End state. Stages A.1 through C.1 complete and green. A.1b verdict BLOCKED. B.2 registered and
  unrun." — HFExperiment/progress.md:17-18
- **Evidence:**
  - No registration of a stage B.2 exists anywhere in the anchored tree: `grep -rn "B\.2"` over all
    `.md`, `.py`, `Makefile` and `pyproject.toml` returns n = 1 hit, progress.md:18 — the claim
    itself.
  - Over the full history, `git -C <live> log --all --format='%h %aI %s' -S'B.2'` returns n = 1
    commit, `f13e1d3` (the closure commit), confirming that B.2's registration was never committed
    and later removed. Run read-only on the live repository 2026-09-03T05:08Z.
  - ADR-002 refers to "Stages A.1 through D.1 as registered in the stage prompt"
    (DECISIONS.md:22-23), so B.2 may well live in an external stage prompt that the repository never
    copied in. That is the honest alternative explanation, and it is also the defect: Sections 1
    through 12 state that they are "the binding pre-registration" (REGISTRATION.md:3), so a
    registered-but-absent stage is a gap in the binding record.
  - Consequence for direction A: the closure names an unrun registered stage whose content, purpose
    and reopen conditions cannot be characterised from the record at all, so no reader can tell what
    was given up when the experiment closed.
- **Recomputation:** None.
- **What would resolve it:** Append B.2's registration text — or a pointer to where it is recorded —
  to REGISTRATION.md or progress.md, with its status and reopen conditions.
- **Confidence:** HIGH that the repository and its history do not register B.2; the stage is probably
  defined in the external stage prompt, which this audit cannot see.
- **Could later commits invalidate this?:** No. No commit exists after the anchor.
- **Disclosed by authors?:** No. progress.md:18 asserts the registration; no entry notes that it is
  not in the repository.
- **Citation check:** verified (quote EXACT, figures YES) — both verifiers KEEP with no change. Both
  reproduced n = 1 tree hit (progress.md:18, the claim itself) and n = 1 history commit (`f13e1d3`)
  for `B.2`, and both endorse the DERIVED label and the honest alternative explanation (ADR-002's
  external stage prompt, DECISIONS.md:22-23).

---

## What Agent A checked and found sound

Where the direction-A thesis did NOT hold, with references. If the thesis held generally in this
repository, I would have expected thin-sample dismissals, untested alternatives waved away, and
closures resting on absent rather than measured evidence. Mostly I found the opposite.

1. **The fractional-through-API measurement itself — the deciding evidence for the broker verdict.**
   n = 3 decimal orders on 2 names (MU, TE) across 2 order types, 1 cashQty order, 1 whole-share
   control; each fractional order refused at validation with an explicit error code, the control
   accepted (reports/stage_a1b/a1b_report.md:49-93; evidence.jsonl:28-49). For a deterministic API
   validation rule this n is entirely adequate — nothing here is a thin-sample dismissal. Codes 10243
   and 10244 are genuine IBKR TWS API message codes carrying exactly the quoted text
   (interactivebrokers.github.io/tws-api/message_codes.html, fetched 2026-09-03, UNANCHORED).
2. **The untested Web API channel.** ACCESS.md:11 names "TWS API and Web API" and only the TWS API
   was exercised, which looked like an untested alternative. But the repository's own cited Elite
   Trader thread reports the Web API rounding cashQty "down to whole shares" (ACCESS.md:219-221), and
   an external source (github.com/erdewit/ib_insync discussion 706, statement dated 2024-03-05,
   fetched 2026-09-03) states "IBKR has never supported fractional equity shares via the API". The
   untested variant would not have cleared the GO bar. No finding.
3. **The Trade-in-Fractions account permission.** The struck ACCESS.md text (docs/ACCESS.md:184-187)
   notes that a paper account inherits the live account's permissions; A.1b never recorded the
   permission state and argued instead from instrument-level SizeIncrement (a1b_report.md:37-40),
   which is not the same thing. However, the external sources above indicate the API refuses
   fractional equities regardless of permission, so this gap does not reopen the verdict. Noted, not
   a finding.
4. **The registered verdict clock.** Days 2,061 and 2,852 reproduce exactly from the registered
   constants. Pointwise fixed-n is 604 days and 80-percent-power fixed-horizon is 1,379 days; the
   sequential design costs roughly 1.5x a fixed-horizon test at matched power, which is the ordinary
   price of always-valid inference. The "Eight to eleven years" statement (REGISTRATION.md:261-262)
   is honest, and the operator accepted it in writing before the fact.
5. **Power-law interpolation and IR arithmetic (Section 4, ADR-009).** TE exponent
   ln(31.70/66.40)/ln(10) = -0.321; excess exponent -0.445; width-20 TE 42.54, excess 15.10, IR
   0.894; (1.062/0.894)^2 = 1.41. All reproduce (n = 2 recorded widths feeding a two-point fit, which
   the authors disclose as a two-point fit at DECISIONS.md:157-158).
6. **Cost hurdle 4.07 bp/day.** 2 names x 0.2 weight x 213.84 bp round trip / 21 sessions = 4.073
   (reports/stage_a2/cost_table.md:36). Reproduces. Note, not a finding: under whole-share Tiered at
   180 USD the same arithmetic gives about 1.0 bp/day (cost_table.md:19), and the registration
   deliberately chose the worst-case regime (REGISTRATION.md:249-251) — a conservative choice against
   its own hypothesis.
7. **Kill-floor touch probabilities (ADR-011).** 1.045, 1.306 and 1.567 sigma for floors 600/500/400
   give driftless one-year touch probabilities 0.296, 0.192 and 0.117; the registered 30/19/12 percent
   reproduce (n = 3 floors).
8. **DEGRADED closure in substance (ADR-012).** Independent of the labelling dispute in
   AUDIT-A-HFExperiment-2, the conclusion "no live sleeve at this stake" holds a fortiori: one share
   each of the 2026-07-01 width-20 book costs 7,890 USD at stored closes (formations.json, n = 20) or
   6,240 USD at A.2 mids (book_spreads.json, `per_name.median_mid`), and the width-5 book alone costs
   3,555 / 2,760 USD, because SNDK exceeds 900 USD by itself. The arithmetic sentence in the
   registration is wrong (see Dropped, item D1) but the conclusion is right and understated.
9. **Choice of width 5 as the primary.** Among recorded and interpolated widths, 5 carries the
   highest IR (REGISTRATION.md:113-118), so within the registered rule the highest-SNR endpoint was
   chosen. A beta- or sector-hedged residual endpoint is considered nowhere (`grep "beta"`:
   REGISTRATION.md:219-223 and DECISIONS.md:175-190, kill floor only) and would plausibly lower the
   418 bp noise on a book the authors themselves call "four correlated sector bets"
   (REGISTRATION.md:126-128) — but nothing in this repository lets me quantify the gain, so I make no
   finding. Flagged instead for the cross-repository pass against the AiTrader round that produced
   the 27.99 bp / IR 1.062 figures.
10. **The stale "operator holds no IBKR account" blocker.** Genuinely stale from 2026-08-25 to
    2026-08-28, and disclosed and corrected by the authors themselves in ADR-026
    (DECISIONS.md:432-479; docs/ACCESS.md:173-190). Not presented as a finding; presenting an
    author-disclosed limitation as a discovery would itself be a process failure.
11. **The runnable billing-plan sub-test.** Disclosed as "runnable and unscheduled"
    (progress.md:268-271; ACCESS.md:199). Not a finding; entered in the reopen ledger as an open item.
12. **Other brokers.** The broker table covers IBKR Canada, Alpaca, Questrade and Wealthsimple
    (ACCESS.md:9-14), n = 4. I cannot cite any other broker that clears all four bars (Canadian
    resident, US equities, order-placing API, fractional through the API), so I make no finding of an
    unexamined alternative.
13. **Spread measurement.** 20 names x 9 cells over 3 sessions (2026-08-19 to 21), median 12.77 bp,
    p75 17.2, p90 20.7 (progress.md:156-161; reports/stage_a2/book_spreads.json). Adequately powered
    for its purpose and not a closure input in dispute.
14. **The gate and the refusal demonstration.** 8 refusals demonstrated against the real 2026-08-03
    width-20 book with formation hash 0b28a5cfda7516fa reproduced (reports/stage_c1/refusals.md:7-9),
    158 tests green with 4 applied mutations each caught (progress.md:92-96). The safety machinery
    does what it claims.

---

## Dropped at consolidation

**Merging.** No two drafts challenged the same claim on the same grounds, so no findings were merged.
Two near-duplicate pairs were examined and kept separate: (a) draft 1 and draft 3 both bear on
"The signal question still gets answered" (REGISTRATION.md:38-39) but attack it on independent
grounds — an administrative disarm at n = 0 versus an unreachable negative bar; (b) draft 2 and
draft 4 both concern the broker table's reopeners but on independent grounds — a definitional
mislabel versus an unexecuted recheck trigger. All seven drafts survived the quote/figure/n test and
became findings 1 through 7. Two draft severities were adjusted upward against the rubric
(draft 4: S4 to S3, and draft 5: S4 to S3, both because "a blocker or external figure is stale" is
the S3 line), one upward from S3 to S2 (draft 3, reasoned in the finding itself), and two labels were
corrected from READ to DERIVED (findings 5 and 7, because the load-bearing evidence is a code
literal plus stored JSONL in one case and a git-history search in the other).

**Dropped — not promoted to findings.** These were recorded in the drafts and are kept here so they
are not lost, but none is a direction-A finding at this SHA:

- **D1. Book-cost arithmetic in Section 6.** REGISTRATION.md:152-154: "A 5-name book gets one share
  per name, 720 of 900 deployed, with equal weighting destroyed by per-name prices from 22 to 1,595
  USD." 720 is 5 x the 144 median, not the sum of five prices; the 22-1,595 range is the *width-20*
  book's A.2 mids (PL 22.305, SNDK 1,595.19 in book_spreads.json), not the width-5 book's. One share
  each of the width-5 book costs 2,760 USD at those mids. Likewise "20 names at one share each
  already cost about 2,880 USD" (REGISTRATION.md:152-153) is 20 x the median; the actual sum is
  6,240-7,890 USD. Dropped from direction A because the error makes the conclusion *stronger*, not
  weaker — it understates the cost of the branch it closes — so it is arithmetic hygiene, or a
  direction-B item, not an over-closure.
- **D2. Kill-floor sentence.** REGISTRATION.md:215-216: "The floor is 500 USD of total account
  equity, a 400 USD loss on 900 deployed after the 100 buffer, 1.31 sigma". 1.31 sigma of 42.54
  percent TE on 900 USD is a 500 USD loss (equity 1,000 to 500); a 400 USD loss is 1.045 sigma, which
  the same paragraph assigns to the 600 floor. The touch probabilities are computed on the 500 USD
  loss and are correct (see sound-item 7); only the sentence is wrong. Dropped: hygiene, no closure
  rests on it.
- **D3. "A documented negative ... at a cost of roughly 30 to 60 USD a year."** The 30-60 USD is the
  *live* drag, not a shadow-series cost — the shadow series costs nothing (REGISTRATION.md:38).
  Dropped as a separate item and folded into AUDIT-A-HFExperiment-3, which challenges the same
  sentence on the stronger ground that the negative is unreachable.
- **D4. ADR numbering gap.** DECISIONS.md jumps from ADR-022 (line 401) to ADR-026 (line 432);
  `git log --all --oneline -S"ADR-023"` (and -024, -025) each return 0 commits, so those ADRs were
  never written. Dropped: numbering hygiene with no substantive content, and it lacks a figure that
  bears on any closure.
- **D5. `.env` credentials state at the health snapshot.** reports/monitor/health.txt:3 records
  ".env does not exist ... BLOCKED-ON-OPERATOR" at 2026-08-25T00:34Z, while progress.md:99-100
  records "Alpaca keys are in .env" later the same night. Dropped: the ordering is consistent (the
  health view predates the keys landing) and it is not an inconsistency.
- **D6. The beta- or sector-hedged residual endpoint.** Considered as an "alternative never tested"
  finding (see sound-item 9) and dropped for want of any figure in this repository that would let me
  quantify the noise reduction. Referred to the cross-repository pass instead.

---

## Live-repo access log

Live path: `/home/kiros-li/Documents/GitHub/HFExperiment`. Two read-only access windows, merged here.

**Operations across both windows:** `git status --porcelain`, `git status --porcelain --ignored`,
`git rev-parse HEAD`, `git log` (several formats), `git branch -a`, `git cat-file -p` on three
commits, `git show --stat` on one commit, `git log --all -p -S` for ADR-023/-024/-025 and for `B.2`,
`git log --all --oneline -S`; a `find -printf` listing of `data/` (no file under `data/` was opened);
`cat .env.example` (a tracked file identical to the snapshot). `.env` itself was never read, and no
credential, keystore, session or token file was opened. No checkout, write, branch operation, or
script execution of any kind.

**Untracked working-tree data listed (UNANCHORED, read 2026-09-03T04:54:35Z, may have changed
since):** `data/bars.db` (40,960 bytes, mtime 2026-08-24 17:34), `data/c1_formation.db`
(105,005,056 bytes, mtime 2026-08-24 19:31), `data/ledger/` (directory). Ignored entries also
present: `.env`, `.venv/`, caches. Contents of none of these were opened.

Window 1 — before (2026-09-03 ~04:47Z):
```
?? Accept:
?? GET
?? Host:
?? User-Agent:
```
Window 1 — after (2026-09-03T05:00:42Z):
```
?? Accept:
?? GET
?? Host:
?? User-Agent:
```
Window 2 (consolidation re-verification) — before (2026-09-03T05:08:13Z):
```
?? Accept:
?? GET
?? Host:
?? User-Agent:
```
Window 2 — after (2026-09-03T05:08:21Z):
```
?? Accept:
?? GET
?? Host:
?? User-Agent:
```

All four listings are identical and match exactly the pre-existing owner stray files named in
COMMON_RULES.md (`Accept:`, `GET`, `Host:`, `User-Agent:`). No other entry appeared at any point.
No modification was made to the audited repository. Live HEAD at consolidation
(2026-09-03T05:08Z) is `82e77a021256d917c665ff6d4304c25b08f35451`, identical to the anchored SHA.
