# Agent A draft findings — HFExperiment (part: all)

Repository: HFExperiment, anchored SHA 82e77a021256d917c665ff6d4304c25b08f35451 (main, 2026-08-28).
Read from SNAP/HFExperiment. Live repo touched read-only for git history and untracked data (log below).
Thesis argued: closed too early / too hard (Direction A). Recomputations in
scratchpad/work/agentA-HFExperiment/recompute.py and recompute.out.

Context in one paragraph. HFExperiment re-registered the H-F 12-1 momentum hypothesis
(README.md:3-5: "tested once in the AiTrader cross-sectional round of 2026-07-26 and
resolved on statistical power rather than absent signal") as a two-series design: a
free SHADOW series to answer the signal question and a micro-size LIVE series to
measure execution. Timeline in UTC from git: Section 0 registered 2026-08-23T22:23Z
(c4e9817); A.1b fired BLOCKED on the broker 2026-08-25T03:09Z (669eb5c); the whole
experiment was closed "terminal" 2026-08-25T07:45Z (f13e1d3, text dated 2026-08-26);
a record-hygiene ADR-026 landed 2026-08-28 (82e77a0). The shadow series never
produced an observation.

---

### DRAFT-all-1
- **Repository / SHA:** HFExperiment / 82e77a021256d917c665ff6d4304c25b08f35451
- **Hypothesis or artifact:** H-F 12-1 cross-sectional momentum, REGISTRATION.md Section 1; the shadow-series signal verdict (Sections 2, 11); the 2026-08-26 closure entry.
- **Direction:** A
- **Class:** OVER_CLOSED
- **Severity:** S2
- **Label:** READ
- **Claim challenged (verbatim quote):** "Experiment closed by operator decision, instruction dated 2026-08-26. The live track was never funded and zero capital was deployed. The shadow series was disarmed before its first accrual" — HFExperiment/REGISTRATION.md:308-310; and "Closure is terminal." — HFExperiment/REGISTRATION.md:313
- **Evidence:**
  - The registration fixed, before any measurement, what a BLOCKED broker verdict means: "Consequence: phases C and D stop. Phase B proceeds unchanged, because the shadow series needs no broker, no account, and no money. The signal question still gets answered." — HFExperiment/REGISTRATION.md:37-39.
  - ADR-002 made the decoupling unamendable: "If the broker question resolves BLOCKED, phase B still runs and still answers the signal question. Only phases C and D die. This property is the reason the two-series design was chosen. Changes it: nothing. A later stage that couples the shadow series to a broker dependency violates this ADR." — HFExperiment/DECISIONS.md:24-29.
  - The BLOCKED entry itself re-affirmed it four and a half hours before the closure: "Per Section 0 phases C and D stop and phase B proceeds unchanged. No parameter changes." — HFExperiment/REGISTRATION.md:303-304; "The shadow series carries the experiment alone and answers the signal question, which was the design's point." — HFExperiment/progress.md:42-44; same at HFExperiment/reports/stage_a1b/a1b_report.md:113-115.
  - The closure gives no reason and no evidence: deciding figure n = 0 shadow observations ("zero shadow observations, because the series never started" — HFExperiment/REGISTRATION.md:315). It is the only decision in the repository without an ADR: DECISIONS.md requires that "Each records the decision, the reason, and what would change it" (HFExperiment/DECISIONS.md:3-4); the closure commit f13e1d3 touched only REGISTRATION.md and progress.md (git show --stat), and DECISIONS.md jumps from ADR-022 to ADR-026 with no ADR-023..025 anywhere in history (git log --all -S"ADR-023" empty). So no reopen condition exists for the closure.
  - Cost of the abandoned path: nil by the authors' own words (":38 needs no broker, no account, and no money"); the only money figure in the registration for a documented negative, "roughly 30 to 60 USD a year at the traded width" (HFExperiment/REGISTRATION.md:278-280), is the LIVE drag, not shadow cost. The operator's registered prior that the sleeve ever clears was 0.15 (HFExperiment/REGISTRATION.md:287-289), i.e. the design was accepted expecting a likely negative.
  - The closure is reversible today without spending any pre-registration integrity: "Daily bars backfill freely, so the honest guarantee is the registration timestamp and not the collection start." — HFExperiment/REGISTRATION.md:72-74. The daily runner computes every missed formation on resume: `due = [f for f in universe.formation_dates(sessions, params) if SHADOW_SERIES_START <= f <= last_complete and f not in recorded]` — HFExperiment/scripts/daily_run.py:141-144 — so the 2026-09-01 formation-aligned start (ADR-015, DECISIONS.md:244-256) is still reachable by backfill. One known pre-start defect remains: the B.1 trade endpoint pin ("B.1 pinned api.alpaca.markets, which 401s on /v2/assets" — HFExperiment/DECISIONS.md:379-380; fix cancelled "as moot", HFExperiment/progress.md:18-19).
  - Live state (UNANCHORED, read-only, 2026-09-03T00:56-00:57Z, may have changed after the anchor): `systemctl --user is-enabled hfexperiment-bars.timer` → disabled, `is-active` → inactive; /home/kiros-li/Documents/GitHub/HFExperiment/data/bars.db has 0 rows in all six tables (bars, sessions, assets, universe, formations, fetch_log); data/ledger/ is empty. Timeline: BLOCKED commit 669eb5c 2026-08-25T03:09:06Z; closure commit f13e1d3 2026-08-25T07:45:29Z (4 h 36 m later); first scheduled shadow run 2026-08-25T23:30Z (HFExperiment/reports/monitor/health.txt:7 "Tue 2026-08-25 16:30:00 PDT"), i.e. the series was disarmed about 16 hours before its first collection and about 57 hours after Section 0 was registered.
- **Recomputation (if any):** Registered verdict clock reproduced exactly (inputs REGISTRATION.md:247-248 rho 0.071641, :255-262 mean 27.99 bp, sigma 418 bp, hurdle 4.07, alpha 0.05): tuned rho 0.071641; lower bound clears zero at day 2061 and the hurdle at day 2852 (recompute.out section A). The crossing day is insensitive to the pre-registered tuning target (t* 200..3000 gives clear-zero days 2385..2055, section B), so the 8-11 year horizon is intrinsic to the signal-to-noise, not to a tuning choice. This does not shorten the clock; it confirms the authors' arithmetic and that the shadow series was the only instrument that could ever move the H-F hypothesis off the AiTrader power-closure.
- **What would resolve it:** Either (a) an appended ADR for the closure stating the reason and a "Changes it" clause, re-labelling the H-F entry from "terminal" to "parked, zero observations, resumable by backfill"; or (b) re-arming hfexperiment-bars.timer after the one-line TRADE_BASE fix (scripts/fetch_c1_formation.py:30 shows the override), which backfills the 2026-09-01 formation and starts the registered sequence at no cost.
- **Confidence:** HIGH — every element is textual in the anchored documents; the contradiction between the closure and Section 0 / ADR-002 does not depend on any external fact.
- **Invalidated by later commits?:** no — the closure is at the anchor; a later re-arm or a closure ADR would resolve, not invalidate, the finding.
- **Disclosed by authors?:** partially — the closure entry discloses that the decision was operator-made and that zero observations exist (REGISTRATION.md:306-315; progress.md:5-21), but nowhere acknowledges that it overrides Section 0:37-39 and ADR-002:28-29 or states a reason; the contradiction itself is not disclosed.

### DRAFT-all-2
- **Repository / SHA:** HFExperiment / 82e77a021256d917c665ff6d4304c25b08f35451
- **Hypothesis or artifact:** Section 0 broker outcome map; the 2026-08-25 BLOCKED verdict; ADR-022's reopen clause.
- **Direction:** A
- **Class:** OVER_CLOSED
- **Severity:** S2
- **Label:** READ
- **Claim challenged (verbatim quote):** "BLOCKED. The IBKR TWS API refused fractional quantities however phrased on paper account [paper account ID removed]" — HFExperiment/REGISTRATION.md:299-300; where BLOCKED is defined as "No reachable broker clears the bars." — HFExperiment/REGISTRATION.md:35
- **Evidence:**
  - The GO bar is channel-agnostic: "exposes an API that places orders and reads fills programmatically, and accepts fractional quantities through that API at 45 USD per name." — HFExperiment/REGISTRATION.md:14-16.
  - The repository's own access survey names two order-placing APIs at the one reachable broker: "| IBKR Canada | yes [1] | yes [1] | yes, TWS API and Web API [1] | UNVERIFIED, settled by test in Task 3 |" — HFExperiment/docs/ACCESS.md:11.
  - The survey also records a report that the Web API accepts cash-quantity orders (with rounding): "an Elite Trader thread reported cashQty rounding down to whole shares through the Web API" — HFExperiment/docs/ACCESS.md:220-221. The sentence that follows, "Both routes refuse." (ACCESS.md:223), refers to decimal and cashQty on the TWS socket, not to the Web API, which was never exercised.
  - A.1b exercised only the TWS socket through ib_async against the Gateway: `from ib_async import IB, LimitOrder, MarketOrder, Order, Stock` — HFExperiment/scripts/a1b_capability_test.py:29; `self.ib.connect(self.env.host, self.env.port, ...)` — :151-155; "No live account, no live endpoint, no strategy." — :8. All five orders in reports/stage_a1b/evidence.jsonl:28,32,38,42,48 went through that socket. n = 5 orders (3 decimal, 1 cashQty, 1 whole-share control), 2 symbols, 2 order types.
  - The refusal text itself points at a channel restriction rather than an instrument or account restriction: "Fractional-sized order cannot be placed via API. Please use desktop version to place this order." — HFExperiment/reports/stage_a1b/a1b_report.md:68-69; the authors agree the instruments are eligible ("the refusal is the API channel itself" — HFExperiment/DECISIONS.md:424).
  - The reopen condition was then written for the channel tested, not the bar registered: "Changes it: IBKR shipping fractional support in the TWS API, or an Alpaca Canadian launch per ADR-003." — HFExperiment/DECISIONS.md:427-428. A Section 0 BLOCKED ("No reachable broker clears the bars") therefore rests on one of two named channels at the one reachable broker.
- **Recomputation (if any):** none (no arithmetic; a capability question).
- **What would resolve it:** Repeat the A.1b five-order validation pattern through the IBKR Client Portal Web API on the same paper account (place-order with quantity 0.0498 MU and with cashQty 45, outside RTH, cancel before open, positions verified flat). A refusal makes BLOCKED complete against Section 0's bar; an acceptance moves the verdict to GO on that channel and reopens phases C and D. I could not verify IBKR's current Web API documentation myself (interactivebrokers.com returned HTTP 403 to my fetch on 2026-09-03), so I make no claim about the outcome, only that the variant the registration's own survey names was not run.
- **Confidence:** MEDIUM — that the Web API was named and never tested is certain from the record; whether it accepts fractional quantities is not established by anything in the repository or by me.
- **Invalidated by later commits?:** no — no commit after A.1b adds a Web API test; ADR-026 (2026-08-28) explicitly leaves "the fractional closure ... unchanged" (DECISIONS.md:459).
- **Disclosed by authors?:** no — ACCESS.md:11 names the Web API but no document records it as untested or explains why it was excluded from Task 3; the ACCESS.md:220-221 Web API report was cited only as a documentation conflict about cashQty, not as an untested route.

### DRAFT-all-3
- **Repository / SHA:** HFExperiment / 82e77a021256d917c665ff6d4304c25b08f35451
- **Hypothesis or artifact:** A.1b fractional verdict carried from the paper venue to the live account; ADR-026.
- **Direction:** A
- **Class:** OVER_CLOSED
- **Severity:** S3
- **Label:** READ
- **Claim challenged (verbatim quote):** "The fractional closure stands unchanged. It rested on error 10243 and error 10244 against an accepted whole-share control, which is measurement, not an inference from missing access." — HFExperiment/DECISIONS.md:459-461
- **Evidence:**
  - The measurement was taken on paper account [paper account ID removed] through the paper Gateway port 4002 (HFExperiment/reports/stage_a1b/a1b_report.md:3-5; `DECLARED_MODE = "paper"`, `MODE_PORTS = {"paper": 4002, "live": 4001}` — HFExperiment/src/hfexperiment/brokerconfig.py:23-25; "No live account, no live endpoint" — scripts/a1b_capability_test.py:8).
  - The bridge from paper to live is an uncited assumption written during A.1 and later struck for a different reason: "~~... with the Trade in Fractions permission enabled in Client Portal, because a paper account inherits the live account's permissions.~~" — HFExperiment/docs/ACCESS.md:184-187. No source is given for the inheritance claim, and no document records whether the Trade in Fractions permission was enabled on the live account at the time of A.1b.
  - The live account exists and is reachable: "the operator ... stated he holds a funded live IBKR account and a paper account reachable through a running Gateway" — HFExperiment/DECISIONS.md:445-447 (2026-08-28). ADR-026 lists what that unblocks and names only the billing-plan sub-test ("One sub-test is genuinely unblocked and worth running" — DECISIONS.md:466-468), not a live-channel repeat of the deciding fractional test.
  - A zero-exposure live test pattern already exists in the repository: the whole-share control was accepted, queued for the open and cancelled unfilled (HFExperiment/reports/stage_a1b/a1b_report.md:86-93); the same pattern with a 0.0498-share order on port 4001 would settle whether error 10243 is a paper-server behaviour or a channel behaviour, at no fill risk if cancelled before 09:30 ET.
- **Recomputation (if any):** none.
- **What would resolve it:** A cited IBKR statement that paper and live servers validate fractional API orders identically, or one validation-only order on the live account under the ADR-018 pin (account must equal the pinned U-prefixed id, port 4001 asserted, cancelled before the open). Either closes the venue gap; the second also costs nothing.
- **Confidence:** LOW — I cannot show that the live server behaves differently; the finding is that the paper-to-live bridge is uncited, the means to test it appeared on 2026-08-28, and the closure label was not revisited.
- **Invalidated by later commits?:** no — ADR-026 is the last commit and leaves the verdict untouched.
- **Disclosed by authors?:** no — the inheritance assumption is stated, not flagged as unverified; ADR-026 describes the closure as "measurement, not an inference from missing access" without noting the venue.

### DRAFT-all-4
- **Repository / SHA:** HFExperiment / 82e77a021256d917c665ff6d4304c25b08f35451
- **Hypothesis or artifact:** The Alpaca-Canada blocker in docs/ACCESS.md; ADR-003's reopen condition "An Alpaca Canadian launch would reopen the table."
- **Direction:** A
- **Class:** STALE_FIGURE
- **Severity:** S3
- **Label:** READ
- **Claim challenged (verbatim quote):** "Alpaca excludes Canadian residents today. Its careers page advertises a Canadian broker-dealer controller role, so the exclusion may lift. Recheck at stage C if Task 3 resolves badly." — HFExperiment/docs/ACCESS.md:17-20; source quoted as "Residents of Canada are not currently eligible" — HFExperiment/docs/ACCESS.md:32
- **Evidence:**
  - The recheck was a registered follow-up with an explicit trigger. The trigger fired: Task 3 resolved BLOCKED on 2026-08-25 (REGISTRATION.md:297-304). No later entry performs the recheck: progress.md after 2026-08-25 mentions Alpaca only for data keys (progress.md:99-100) and the ADR-021 endpoint note; the A.1b report and progress entry merely restate the clause ("an Alpaca Canadian launch or IBKR shipping API fractional support reopens the table as a new measurement" — HFExperiment/progress.md:44-46; a1b_report.md:115-116). ADR-003's own "Changes it" names it (DECISIONS.md:65-66).
  - The cited source no longer verifies the blocker. Fetched 2026-09-03T00:5xZ (external, unanchored): https://alpaca.markets/support/countries-alpaca-is-available now contains no country list and no mention of Canada, only "Please contact support at [email protected] for more information regarding whether your country is supported", with a page date of "February 2026". Either the page changed after the 2026-08-23 retrieval or the quoted sentence was not on this page at retrieval; in both cases the blocker as recorded cannot be re-verified from its citation, and the eligibility status is unknown rather than known-negative.
  - Consequence for the closure: BLOCKED's "No reachable broker" (REGISTRATION.md:35) rests on the broker table's single reachable row (ACCESS.md:16-17), whose exclusion of Alpaca is the figure at issue.
- **Recomputation (if any):** none.
- **What would resolve it:** Perform the registered recheck (support enquiry or the account-opening flow), record the answer with date and source under the amendment log, and re-date the reopen condition.
- **Confidence:** MEDIUM — the omission of the recheck is certain from the record; the current eligibility status is unknown (my fetch shows the page neither excludes nor admits Canada), and the fetch is a summarised read of a live page.
- **Invalidated by later commits?:** no — nothing after 2026-08-25 touches the Alpaca eligibility question.
- **Disclosed by authors?:** partially — the recheck instruction is the authors' own (ACCESS.md:19-20) and the reopen clause is recorded (DECISIONS.md:65-66); that the recheck was never carried out, and that the cited page no longer carries the quoted text, are not disclosed.

### DRAFT-all-5
- **Repository / SHA:** HFExperiment / 82e77a021256d917c665ff6d4304c25b08f35451
- **Hypothesis or artifact:** The closure record's date.
- **Direction:** A
- **Class:** PROVENANCE
- **Severity:** S4
- **Label:** DERIVED
- **Claim challenged (verbatim quote):** "### 2026-08-26: Closure" and "Experiment closed by operator decision, instruction dated 2026-08-26." — HFExperiment/REGISTRATION.md:306-308; repeated at HFExperiment/progress.md:5-8
- **Evidence:**
  - Commit f13e1d3 ("docs: terminal closure, shadow timer disarmed, closure recorded in amendment log and progress") carries author and committer date 2026-08-25T00:45:29-07:00 = 2026-08-25T07:45:29Z (git -C /home/kiros-li/Documents/GitHub/HFExperiment log --format='%ad %cd' --date=iso-strict f13e1d3). The closure text is dated one calendar day after the commit that introduced it, in both UTC and the author's local zone.
  - The BLOCKED commit 669eb5c is dated 2026-08-24T20:09:06-07:00 = 2026-08-25T03:09:06Z; the closure therefore followed the broker verdict by 4 h 36 m, not by a day of deliberation as the "2026-08-26" date suggests, and preceded the first scheduled shadow collection (2026-08-25T23:30Z, reports/monitor/health.txt:7) by about 16 hours.
- **Recomputation (if any):** time differences from the two commit timestamps above.
- **What would resolve it:** An appended note correcting the closure date to 2026-08-25 (UTC) or explaining the discrepancy (e.g. an instruction pre-dated for a later calendar day).
- **Confidence:** HIGH — commit metadata is unambiguous; a wrong system clock is possible but would itself be a provenance defect.
- **Invalidated by later commits?:** no — the anchored text and commit dates are fixed.
- **Disclosed by authors?:** no.

### DRAFT-all-6
- **Repository / SHA:** HFExperiment / 82e77a021256d917c665ff6d4304c25b08f35451
- **Hypothesis or artifact:** Section 6 / ADR-012, closure of the DEGRADED (whole-share) live branch.
- **Direction:** A
- **Class:** INTERNAL_INCONSISTENCY
- **Severity:** S4
- **Label:** DERIVED
- **Claim challenged (verbatim quote):** "At 144, whole-share sizing on 900 USD cannot fill a 20-name book at all, because 20 names at one share each already cost about 2,880 USD. A 5-name book gets one share per name, 720 of 900 deployed, with equal weighting destroyed by per-name prices from 22 to 1,595 USD." — HFExperiment/REGISTRATION.md:151-154 (same arithmetic at DECISIONS.md:195-198)
- **Evidence:**
  - The figures are median proxies, not the book. From HFExperiment/reports/stage_a1/formations.json (2026-07-01, last_close): width-5 book WOLF 48.25, AXTI 72.08, SNDK 2273.73, BE 302.7, LITE 858.06 — one share each sums to 3,554.82 USD, not 720 (720 = 5 x 144). SNDK alone exceeds the 900 USD deployable, so a whole-share 5-name book cannot be filled at all; the sentence "gets one share per name, 720 of 900 deployed" is false in the direction that flatters the branch. Width-20 one share each sums to 7,890.47 USD (closes) or 6,239.89 USD (A.2 mids, reports/stage_a2/book_spreads.json), not "about 2,880". The quoted range "22 to 1,595 USD" is PL's A.2 median mid 22.305 and SNDK's 1595.19 — both from the width-20 set; PL is not in the width-5 book.
  - The "equal weighting destroyed" rationale is inconsistent with the repository's own ADR-008, which holds that the live book serves fill count only and "never feeds the verdict, so nothing the live book does can confound it" (HFExperiment/DECISIONS.md:130-133; REGISTRATION.md:104-107). Equal weighting is a property of the verdict book, which is the shadow book.
  - What the closure actually rests on is the 1,000 USD stake, and the whole-share API channel was confirmed open by A.1b ("Whole-share through the API stays open; only slicing is closed" — HFExperiment/docs/ACCESS.md:197; progress.md:258-259). At that stake a price-filtered whole-share execution sleeve was arithmetically possible: the 11 cheapest names of the 2026-07-01 width-20 book cost 789.91 USD at one share each (closes ONDS 8.24 ... HUT 115.445 ... DOCN 157.03; cumulative from formations.json), 792.90 USD for 11 names on 2026-06-01. Such a sleeve would measure slippage on a lower-priced, wider-spread subset and was not considered anywhere in the record. I flag it as a path not named by the authors, not as one they rejected.
- **Recomputation (if any):** recompute.out section G; inputs formations.json 2026-07-01 blocks "5" and "20" (last_close), formation_2026-08-03.json width20_entry_closes (sum 5,936.07, median 152.51), book_spreads.json per_name.median_mid (sum 6,239.89, median 103.25); method: plain sums and cumulative affordability at 900 USD.
- **What would resolve it:** Restate Section 6 on the actual book (the conclusion "no full-width whole-share book at this stake" survives, more strongly), drop or justify the equal-weighting rationale against ADR-008, and record whether a partial whole-share execution sleeve was considered and why it was rejected.
- **Confidence:** HIGH on the arithmetic; LOW that a corrected statement changes the decision at the registered stake.
- **Invalidated by later commits?:** no — Section 6 and ADR-012 are unchanged through the anchor.
- **Disclosed by authors?:** no — the reopen condition "a materially larger stake, which is a new registration" (DECISIONS.md:201-203) is disclosed; the proxy arithmetic and the ADR-008 tension are not.

---

## What I checked and found sound

Where the Direction-A thesis did not hold, or where a limitation was already disclosed and is therefore not a finding:

- **Verdict schedule arithmetic (Section 11, cost_table.md:40, registered.py:91-107).** Reproduced exactly: tuned rho 0.071641 at t* 1600, clear-zero day 2061, clear-hurdle day 2852 at mean 27.99 bp / sigma 418 bp / alpha 0.05; pointwise z=1.645 needs 603 days ("about 600", REGISTRATION.md:257); 418 bp follows from 66.4 %/yr (418.3). The crossing day is insensitive to t* (2055-2385 across t* 200-3000), so the "eight to eleven years" is intrinsic and not a design artefact. No better-signal endpoint exists within the design: width 5 already carries the highest IR (1.062) of the three registered widths (REGISTRATION.md:113-118), and the width table's two-point power law reproduces (exponents -0.321 / -0.445; IR 0.975 / 0.894 interpolated; ratio (1.062/0.894)^2 = 1.411).
- **Cost hurdle and drag tables (REGISTRATION.md:184-186, :249-251; cost_table.md).** 2.0/5 x 213.84/21 = 4.073 bp/day; drag rows follow from costmodel.py; A.2 spread medians recomputed from book_spreads.json: book 12.77 bp, width-5 13.08 bp at median mid 201.91 (n = 20 names x 9 cells, none unmeasured).
- **A.1 reproduction (reports/stage_a1/reproduce_log.txt:1,21; universe_check.json).** 124/124 formation dates identical; universe exact at 10 dates x 500 rows. ADR-005's horizon pin to the 2026-07-24 pull end is disclosed with its reopen condition (DECISIONS.md:89-95).
- **B.1 price reconciliation (reports/stage_b1/price_reconciliation.md).** 28.2 % median gap explained as market movement with zero corporate actions in window; per-name ratios 0.52-1.06 continuous; consistent with the A.2 mids I re-read.
- **A.1b evidence for the TWS-channel refusal itself (reports/stage_a1b/evidence.jsonl:28-49).** Three decimal orders refused with 10243 (two names, MKT and LMT, outsideRth both ways), one cashQty refused with 10244, one whole-share control PreSubmitted then cancelled; positions flat twice. Within the channel tested the BLOCKED reading is correct. (Aside, hygiene only: evidence.jsonl:2 records `"server_version":178` while a1b_report.md:4 and refusals.md:332 say 187; ib_async's negotiated version versus the Gateway's, presumably, but the report should say which.)
- **Section 12 amendment discipline.** The closure did not respond to an observed shadow outcome (there were none), so the ":273 No amendment may respond to an observed shadow outcome" rule was not breached.
- **The runnable billing-plan sub-test left unscheduled (ACCESS.md:199; DECISIONS.md:466-468; progress.md:268-271).** A stated blocker (no account) that expired on 2026-08-25/28 with the item still unrun — but the authors disclose exactly this ("runnable and unscheduled", progress.md:268) and it resolves a moot Amendment 1 parameter; recorded in the reopen ledger, not raised as a finding.
- **DEGRADED reopen condition (DECISIONS.md:201-203).** "A collapse in book share prices does not reopen it, because the branch decision must not track the thing it sizes" — disclosed and principled; the 2026-08-24 median close of 97.45 (price_reconciliation.md:58) therefore does not reopen the branch, and I do not claim it does.
- **B.1a endpoint fix cancelled as moot (progress.md:18-19; DECISIONS.md:378-387).** Consistent with the closure; noted only as a precondition for any resume in DRAFT-all-1.
- **Asides for the Direction-B pass (not Direction-A findings, recorded so they are not lost):** (i) Kill-floor sentence REGISTRATION.md:216-217 says "500 USD of total account equity, a 400 USD loss on 900 deployed ... 1.31 sigma"; at 42.54 % TE on 900 USD (sigma 382.9 USD) a 400 USD loss is 1.04 sigma and 1.31 sigma is a 500 USD loss (recompute.out section D) — the sigma and touch figures in ADR-011 are consistent with loss = 1000 - floor, the "400 USD loss" phrase is not; moot since no live sleeve exists. (ii) The futility bar (upper bound below 10 bp/day) is first reachable at day 18,650 if the true mean is 0 bp/day and never if it is +5 (recompute.out section C), so "A documented negative is a valid outcome" (REGISTRATION.md:278) could not have arrived through the registered futility rule on any practical horizon; the design was one-sided in practice. (iii) progress.md:18 says "B.2 registered and unrun" but no B.2 registration exists anywhere in the repository or its history.

## Live-repo access log

Live repository: /home/kiros-li/Documents/GitHub/HFExperiment (read-only: git log/show/rev-parse/branch; ls; sqlite3 opened with mode=ro on data/bars.db and data/c1_formation.db; `systemctl --user` state queries; no .env read).

BEFORE (2026-09-03T00:52:55Z), `git -C /home/kiros-li/Documents/GitHub/HFExperiment status --porcelain`:
```
?? Accept:
?? GET
?? Host:
?? User-Agent:
```
AFTER (2026-09-03T01:00:55Z), same command:
```
?? Accept:
?? GET
?? Host:
?? User-Agent:
```
HEAD before and after: 82e77a021256d917c665ff6d4304c25b08f35451. The four untracked entries are the owner's pre-existing stray files listed in COMMON_RULES; no other entry appeared.
