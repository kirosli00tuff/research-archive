# Agent A draft findings — ETFExperiment (part: all)

**Repository:** ETFExperiment · **Anchored SHA:** `4d110027674e7b4cd2861cf4e0e74f975111daf1` (master, 2026-08-28)
**Read from:** `SNAP/ETFExperiment/` for every tracked file; live repo used read-only for `git log`,
`git status`, and three untracked data files (see the access log at the bottom).
**Direction:** A — the case that work was closed earlier or harder than the evidence supports.

The repository is unusually disciplined: the pre-registration was committed before the first
network call, the append-only amendment rule was honoured through six amendments, a figure of its
own was falsified by its own measurement and recorded as falsified, and no outcome value was ever
read. Nothing below disputes any of that. The findings concern the **closure decision** taken at
Amendment 5 and Amendment 6 on 2026-08-28, roughly fifteen hours after the pre-registration was
committed, and whether the registered map actually supported it.

---

### DRAFT-all-1
- **Repository / SHA:** ETFExperiment / 4d110027674e7b4cd2861cf4e0e74f975111daf1
- **Hypothesis or artifact:** H1 (H-ETF) — the Section 0 closure and the disarming of all collectors
- **Direction:** A
- **Class:** OVER_CLOSED
- **Severity:** S1
- **Label:** DERIVED
- **Claim challenged (verbatim quote):** "**DEGRADED and BLOCKED differ in label and not in operational consequence here.**" — ETFExperiment/REGISTRATION.md:1038
- **Evidence:**
  - The registered decision function, committed at A.0 before any network call and pinned by test, makes exactly this distinction operational. `Section0Gate` carries a `collectors_armed: bool` field (ETFExperiment/src/etf/section0.py:49). Every BLOCKED return sets `collectors_armed=False` (ETFExperiment/src/etf/section0.py:110, :122, :134); the DEGRADED return sets `collectors_armed=True` (ETFExperiment/src/etf/section0.py:182), as does GO (:149).
  - The registration says the same in words: DEGRADED — "Collection proceeds." (ETFExperiment/REGISTRATION.md:41); BLOCKED — "Nothing armed beyond the census." (ETFExperiment/REGISTRATION.md:51).
  - The tests pin it: `assert gate.collectors_armed` under the registered-expectation DEGRADED shape (ETFExperiment/tests/test_section0.py:61) and `assert not gate.collectors_armed` under observability FAIL → BLOCKED (ETFExperiment/tests/test_section0.py:75).
  - The unmeasured leg is precisely what selects between them. Amendment 3 states it: PARTIAL → DEGRADED, FAIL → BLOCKED (ETFExperiment/REGISTRATION.md:876-881).
  - The measured inputs put the case squarely in the registered DEGRADED residual band. E1 at the published magnitude at the achievable count is **0.6105 (n = 163)** against a 0.50 BLOCKED floor (ETFExperiment/reports/stage_a2/power.json:62,64; ETFExperiment/REGISTRATION.md:851). The unstable-as-printed share is **0 of 11** (ETFExperiment/reports/stage_a1/retro_revision.json:3-4), far under the 0.50 majority trigger (ETFExperiment/src/etf/section0.py:25,113). The test fixture for the residual band, written at A.0, uses `e1_reg=0.20, e2_reg=0.15, e1_pub=0.62, e2_pub=0.40` (ETFExperiment/tests/test_section0.py:87) against the measured 0.2015 / 0.1700 / 0.6105 / 0.5225 — the map's own worked example of the case that landed.
  - The repository nonetheless ended in the BLOCKED collection state: "**`etf-snap` is disarmed.** `etf-daily` was disarmed at Amendment 5." and "**The repository holds no armed collector and no running process.**" (ETFExperiment/REGISTRATION.md:1157-1159).
- **Recomputation (if any):** Reproduced the power inputs independently with numpy/scipy at the registered model (Gaussian copula, `rho_p = 2 sin(pi rho_s / 6)`, ETFExperiment/src/etf/power.py:47-55; permutation critical value, :70-83) at alpha_adj = 1 − 0.95^(1/2) = 0.0253205655 (ETFExperiment/src/etf/config.py:25). E1 at n = 163, rho = 0.18: **0.638** (3,000 sims) against the repository's 0.6105 (2,000 sims, SE ≈ 0.011) — same side of the 0.50 floor by a wide margin. E1 at n = 163, rho = 0.09: **0.209** vs the repository's 0.2015. E1 at n = 152: **0.602** vs 0.6000. Script: `SCRATCH/work/agentA-ETF/power_recompute.py`.
- **What would resolve it:** Either (a) an amendment stating that the operator closure deliberately took the BLOCKED collection consequence without the BLOCKED trigger, and why that is not the "fitting the rule to the sample" the registration exists to prevent; or (b) reinstating the DEGRADED consequence the registered fire function returns on the measured inputs. Running `fire_section0` on the measured inputs and recording its output — the function is never called by any script or test other than `tests/test_section0.py` (grep across `src/` and `scripts/` returns no caller) — would settle it in one line.
- **Confidence:** HIGH — the distinction the amendment calls non-operational is a boolean field in the registered decision function, set differently on the two branches, and asserted differently by two tests committed before any data existed.
- **Invalidated by later commits?:** no — 4d11002 is the last commit on master and the repository carries an untracked `_CLOSED_DO_NOT_RUN_HERE` marker dated 2026-09-02 declaring it closed.
- **Disclosed by authors?:** no — the amendment asserts the opposite. Amendment 5 §2 (ETFExperiment/REGISTRATION.md:1034-1041) argues mootness from the deadline alone and does not mention `collectors_armed`.

---

### DRAFT-all-2
- **Repository / SHA:** ETFExperiment / 4d110027674e7b4cd2861cf4e0e74f975111daf1
- **Hypothesis or artifact:** H1 — ADR-019's rejection of the deadline extension
- **Direction:** A
- **Class:** INTERNAL_INCONSISTENCY
- **Severity:** S1
- **Label:** READ
- **Claim challenged (verbatim quote):** "*Amending the deadline to 2027-12-31 and continuing*: legitimate, outcome-blind, and nearly free in compute, and it was declined on what it purchases rather than on what it costs. An extension buys the **published 0.18** assumption only; at the **registered 0.09** assumption the minimum N exceeds 1,200 ... A Stage B under the extension answers only whether the effect persists at its published magnitude, and a FAIL still cannot separate decay from absence, which is the distinction the registered assumption exists to draw." — ETFExperiment/DECISIONS.md:551-558
- **Evidence:**
  - What the ADR gives as the reason for declining is the registered DEGRADED scope, verbatim: "**under DEGRADED a Stage B FAIL establishes that the effect is not present at its published magnitude, and cannot distinguish a decayed effect from no effect at all.**" (ETFExperiment/REGISTRATION.md:44-46; repeated as a frozen constant in code, ETFExperiment/src/etf/section0.py:55-58).
  - The registration pre-committed to that scope as its expected outcome and as an acceptable one: "**The Section 9 arithmetic and the decay evidence of Section 14 point to DEGRADED.**" (ETFExperiment/REGISTRATION.md:74-75) and "This is stated **before the census exists** so that the verdict, when it fires, reads as a documented answer rather than a disappointment. **A DEGRADED here narrows a question rather than abandoning it, and a BLOCKED is a documented answer, not a failure of process.**" (ETFExperiment/REGISTRATION.md:82-86).
  - So the extension was declined because it would deliver exactly the deliverable the registration registered in advance as what this design was expected to produce. The registered rationale for the 0.09 assumption (ETFExperiment/REGISTRATION.md:347-356) is a rationale for *reporting* power at 0.09 beside 0.18, not for treating a 0.18-scope answer as worthless: Section 0's GO clause is the only place 0.09 is a bar, and GO had already been eliminated on the archive-density leg (ETFExperiment/REGISTRATION.md:863-867).
  - Cost of the declined option, on the repository's own numbers: zero dollars, roughly 33 requests per day (ETFExperiment/REGISTRATION.md:1085), against a registered flow cap of 200/day (ETFExperiment/src/etf/config.py:136) and a lifetime total of 220 charged requests (ETFExperiment/REGISTRATION.md:1160).
- **Recomputation (if any):** Using the repository's own projection arithmetic (`scripts/power_gate.py:69-80`: forward days = weekdays × printed_day_rate 333/336, added to achieved 11), I reproduced its published scenarios exactly — 88 by 2026-12-31, 152 forward-only and **163** all-cohorts by 2027-03-31 (matches ETFExperiment/reports/stage_a2/power.json:114-116) — and extended them: **N = 237 (E1's minimum, the figure the closure is explicitly stated against) is reached 2027-07-14**, and N = 300 on 2027-10-12. A 2027-12-31 extension therefore clears E1's minimum with 5.5 months to spare and the governing 300 with 2.5. Script: `SCRATCH/work/agentA-ETF/power_recompute.py` (date arithmetic block).
- **What would resolve it:** An amendment reconciling ADR-019's grounds for rejection with Section 0's registered expectation and DEGRADED scope — i.e. stating whether a published-magnitude answer was, or was not, the answer this registration set out to buy.
- **Confidence:** HIGH — both texts are in the same repository, one quotes the scope the other rejects, and the registered expectation predates any data.
- **Invalidated by later commits?:** no — ADR-019 is in the final commit and ADR-020 supersedes only its collection consequence (ETFExperiment/DECISIONS.md:574).
- **Disclosed by authors?:** partly — ADR-019 discloses that the extension was "legitimate, outcome-blind, and nearly free" and that it was declined on what it purchases (ETFExperiment/DECISIONS.md:551-553). It does not disclose that what it purchases is the registration's own pre-registered expected outcome.

---

### DRAFT-all-3
- **Repository / SHA:** ETFExperiment / 4d110027674e7b4cd2861cf4e0e74f975111daf1
- **Hypothesis or artifact:** H1 — the "deadline finding" that carries the closure
- **Direction:** A
- **Class:** OVER_CLOSED
- **Severity:** S2
- **Label:** DERIVED
- **Claim challenged (verbatim quote):** "**H1 closes at `untestable-at-achievable-power`.** The registered design cannot resolve the effect at the sample size reachable by the registered deadline of 2027-03-31." — ETFExperiment/REGISTRATION.md:1004-1006
- **Evidence:**
  - The word "deadline" does not occur anywhere in the pre-registration proper. `awk 'NR<=595 && /deadline/'` over ETFExperiment/REGISTRATION.md (Sections 0–14 end at line 589; the amendment log opens at 591) returns nothing. The date 2027-03-31 occurs exactly three times before the amendments: ETFExperiment/REGISTRATION.md:36, :48 and :78 — in all three it is the horizon over which the **achievable admissible-day count** is computed inside the Section 0 map, never a date by which anything must be finished.
  - The repository's own code names it as a horizon: `projection_deadline: str` (ETFExperiment/src/etf/config.py:89), set to `"2027-03-31"` (ETFExperiment/src/etf/config.py:176), beside `interim_deadline` `"2026-12-31"` (:175). It is consumed only inside the Section 0 rationale strings (ETFExperiment/src/etf/section0.py:130,145) and by the projection in `scripts/power_gate.py:73`.
  - Section 10, the Stage B trigger, carries no date at all: "1. **both co-primaries at or above 80 percent power at achieved admissible N** (not projected) under **the assumption Section 0 fired on**; 2. the **operator prior slot ... filled and labelled** ...; 3. **explicit operator instruction.**" (ETFExperiment/REGISTRATION.md:394-398). Nothing in the registration expires.
  - The one registered decision rule that does use 2027-03-31 is the BLOCKED power trigger — "**BLOCKED:** E1 under **50 percent** power at the published-magnitude assumption at the achievable count by 2027-03-31" (ETFExperiment/REGISTRATION.md:47-48) — and it was measured at **0.6105** and did not fire (ETFExperiment/reports/stage_a2/power.json:62; ETFExperiment/REGISTRATION.md:869-871). The report says so plainly: "**Section 0's BLOCKED floor is a statement about power, and it is cleared. The registered deadline is what is not met.**" (ETFExperiment/report.md:369-370).
  - Consequence for the closure type: HYPOTHESES.md defines `untestable-at-achievable-power` as "the registered design still cannot resolve the effect at the sample size **reachable by the registered deadline**" (ETFExperiment/HYPOTHESES.md:48-49). If the deadline is a projection horizon rather than a registered stopping rule, the closure type rests on a constraint the registration did not impose on itself.
- **Recomputation (if any):** Minimum detectable rank correlation at 80 % power, alpha_adj one-sided, normal approximation to the permutation null (r·√(n−1) ~ N(ρ√(n−1), 1−ρ²)), inputs alpha_adj from ETFExperiment/src/etf/config.py:25 and N from ETFExperiment/reports/stage_a2/power.json:116: at **N = 163 the MDE is ρ = 0.218**; at N = 237, ρ = 0.181; at N = 300, ρ = 0.161. So at the projected count the design detects an effect 21 % larger than the published magnitude at 80 % power, and reaches 61 % power against the published magnitude itself — a narrowed design, not an unresolvable one, on the registration's own 0.50/0.80 scale.
- **What would resolve it:** Point to a line in Sections 0–14 registering 2027-03-31 as a termination date rather than a projection horizon; failing that, an amendment recording that the stopping rule was created at closure time and stating why that is not a post-hoc bar.
- **Confidence:** HIGH for the textual claim (the greps are exhaustive over the pre-registration); MEDIUM for the inference that the closure is therefore premature, because an operator is entitled to stop a project for reasons outside its registration — but then the closure is an operator preference, not the registered `untestable-at-achievable-power` finding it is typed as.
- **Invalidated by later commits?:** no — the amendment log is append-only and 4d11002 is final.
- **Disclosed by authors?:** partly — ADR-019 speaks of "*Amending* the deadline" (ETFExperiment/DECISIONS.md:551), which presupposes a registered deadline exists; the record never notes that Sections 0–14 contain none.

---

### DRAFT-all-4
- **Repository / SHA:** ETFExperiment / 4d110027674e7b4cd2861cf4e0e74f975111daf1
- **Hypothesis or artifact:** H1 — the data-availability finding kept as what "outlives the hypothesis", and reopen path (b)
- **Direction:** A
- **Class:** OVER_CLOSED
- **Severity:** S2
- **Label:** DERIVED
- **Claim challenged (verbatim quote):** "What is established is narrower and is a fact about data availability, not about markets: **the as-printed history required to test this design at power does not exist in any free archive**, and building it forward takes longer than the registration allowed." — ETFExperiment/REGISTRATION.md:1055-1058 (same claim at ETFExperiment/report.md:476-479)
- **Evidence:**
  - Exactly one archive was ever queried. The `robots.txt` sweep covers 8 hosts and the only archive hosts on it are `web.archive.org` (HTTP 404, no robots served) and `archive.org` (ETFExperiment/reports/stage_a1/robots_and_terms.json:39-56; ETFExperiment/docs/ACCESS.md:26-27). The two archive endpoints registered in config are both Wayback: `wayback_availability_url`, `wayback_timemap_url` (ETFExperiment/src/etf/config.py:126-127). Grep of the whole snapshot for `archive.today`, `archive.ph`, `archive.is`, `commoncrawl` returns nothing.
  - Exactly two URLs were ever measured, both on the one selected publisher: `https://farside.co.uk/btc/` and `https://farside.co.uk/bitcoin-etf-flow-all-data/` (ETFExperiment/reports/stage_a1/archive_density.json:30,60; ETFExperiment/scripts/archive_density.py:30-33). The retained cross-check source SoSoValue — keyless, server-rendered `__NEXT_DATA__`, 660 daily rows (ETFExperiment/docs/ACCESS.md:165-168) — had no timemap requested.
  - Reopen path (b) is registered over a universe wider than the one measured: "**(b)** An archive **or mirror** with **at least 60 percent** pre-anchor capture density over the test window." (ETFExperiment/HYPOTHESES.md:84). A mirror class was named as a reopen trigger and never probed.
  - The cost of probing it is essentially zero on the repository's own measurements: the archive endpoints were the fastest clean endpoints measured, 59.92/min and 21.28/min with no ceiling found (ETFExperiment/reports/stage_a1/rate_ceilings.json, `archive.availability` / `archive.timemap`; ETFExperiment/docs/ACCESS.md:336-337), the registered archive cap is 2,000/day (ETFExperiment/src/etf/config.py:137), and the whole repository spent 79 archive requests in its lifetime (ETFExperiment/REGISTRATION.md:1160 gives 220 total; ETFExperiment/progress.md:515-516 splits them 33 flow / 79 archive / 108 venue). A timemap query against a second archive is one request.
  - A concrete named alternative I can state: **archive.today** (mirrors `archive.ph` / `archive.is` / `archive.li`), an independently operated free web archive with its own crawl schedule and its own memento/timemap surface, unrelated to the Internet Archive. I have no network access in this audit and therefore make no claim about what it holds for `farside.co.uk`; the point is that the repository's universal claim was never tested against it. **Common Crawl** (monthly WARC crawls with a public index API) is a second.
- **Recomputation (if any):** I reproduced the repository's archive measurement from the raw untracked timemaps to confirm the method before criticising the universe. Inputs: live `data/access/timemap-recent.txt` and `timemap-all_data.txt` (untracked, read 2026-09-03T19:40Z), and live `data/access/farside_all_parsed.json` (untracked, same read). Method mirrors ETFExperiment/src/etf/archive.py:90-127. Results, all matching the repository exactly: **336** out-of-sample date rows, **333** with a complete five-fund print, **451** union mementos, **37** timemap-admissible days at the 08:00 anchor (share 0.1111), **53** capture-too-late, unbounded-window ceiling **112/333 = 0.3363**, out-of-sample crawl rate **0.316 mementos/day** (153 mementos over 484.3 calendar days). Script: `SCRATCH/work/agentA-ETF/anchor_sensitivity.py`. The measurement is sound; the generalisation from it is what is not.
- **What would resolve it:** One timemap request per candidate archive per flow URL — four requests would test archive.today against both Farside pages — with the result recorded. Until then the sentence should read "does not exist in the Internet Archive's captures of the two Farside pages (n = 1 archive, n = 2 URLs)".
- **Confidence:** HIGH that the claim is universal and the measurement is not; MEDIUM that a second archive would change the number, since a crawl rate of 0.316/day on a mid-sized publisher is not obviously atypical and the bar is 0.60.
- **Invalidated by later commits?:** no — 4d11002 is final and no later measurement exists.
- **Disclosed by authors?:** no — the record repeatedly attaches "any free archive" (ETFExperiment/REGISTRATION.md:1057, ETFExperiment/report.md:477) and "path (b) turns on someone else's archive existing" (ETFExperiment/DECISIONS.md:585-586) to a measurement whose n over archives is 1, without stating that n.

---

### DRAFT-all-5
- **Repository / SHA:** ETFExperiment / 4d110027674e7b4cd2861cf4e0e74f975111daf1
- **Hypothesis or artifact:** H1 — reopen path (a), and the measurement dropped at Amendment 6
- **Direction:** A
- **Class:** INTERNAL_INCONSISTENCY
- **Severity:** S2
- **Label:** READ
- **Claim challenged (verbatim quote):** "**(a)** A flow source serving a **per-row publication timestamp**. Measured: **0 of 2** surviving sources serve one, and none documents a publication time. This removes the dependence on this repository's own capture cadence entirely and would make the full **333-day** out-of-sample series admissible in a single pass, clearing every minimum on the record at once." — ETFExperiment/HYPOTHESES.md:84
- **Evidence:**
  - A per-row publication timestamp establishes *when* a row was published. It does not establish *what value stood* at that time, and the registered admissibility rule turns on the second: "**The as-printed value for US trading day D is the aggregate net flow for D as served by the flow source in a capture strictly before the entry anchor. The value taken is the one in that capture.** A later value for the same day, however authoritative, **is never substituted**" (ETFExperiment/REGISTRATION.md:155-160; ADR-002, ETFExperiment/DECISIONS.md:57-61). Reading today's value for a past row, with a timestamp attesting the row's age, is exactly the substitution the rule forbids — unless the source's revision rate is known to leave the sign and threshold intact.
  - That revision rate is the measurement Amendment 6 dropped: "**The forward revision-integrity leg will never complete.** ... **It is dropped by decision, not by oversight.**" (ETFExperiment/REGISTRATION.md:1141, :1149) — and the same amendment forbids using the only substitute: "Any future flow hypothesis in this house **must measure it from scratch** and may not cite the n = 11 figure as evidence of anything." (ETFExperiment/REGISTRATION.md:1152-1153; identically ETFExperiment/DECISIONS.md:608-611).
  - So reopen path (a), described as clearing "every minimum on the record at once", cannot in fact be exercised without redoing, from scratch, the 15-trading-day measurement the closure declined to finish — and the closure's own §2 valuation table records path (a) as "**Does not need `etf-snap`.**" (ETFExperiment/REGISTRATION.md:1125), which is true of the collector and false of the measurement.
  - The retro corroboration that would have carried the point stands at 0 revised / 0 sign flips / 0 threshold crosses on **n = 11**, below the registered minimum of 30 (ETFExperiment/reports/stage_a1/retro_revision.json:3-8), and is correctly refused as evidence (ETFExperiment/REGISTRATION.md:889-895).
- **Recomputation (if any):** none — this is a reading of the registered admissibility rule against the reopen condition.
- **What would resolve it:** Restate reopen (a) as a conjunction — a per-row publication timestamp **and** a revision-integrity measurement at the registered n ≥ 30 — or record that (a) implicitly assumes the revision rate the repository chose not to measure.
- **Confidence:** MEDIUM — a source that served both a publication timestamp *and* an as-printed value history would satisfy (a) as written; but no such source is named, and the two surviving sources serve neither (ETFExperiment/docs/ACCESS.md:104,169).
- **Invalidated by later commits?:** no — Amendment 6 is the final amendment.
- **Disclosed by authors?:** no — the register presents (a) as a self-sufficient threshold that "clear[s] every minimum on the record at once".

---

### DRAFT-all-6
- **Repository / SHA:** ETFExperiment / 4d110027674e7b4cd2861cf4e0e74f975111daf1
- **Hypothesis or artifact:** H1 — the forward accrual rate, the deciding input to the deadline finding
- **Direction:** A
- **Class:** PROVENANCE
- **Severity:** S2
- **Label:** DERIVED
- **Claim challenged (verbatim quote):** "**Projected achieved N at the registered 2027-03-31 deadline: 163**, at a measured forward accrual of **20.8 admissible days per month**." — ETFExperiment/HYPOTHESES.md:70 (the same "measured" label at ETFExperiment/HYPOTHESES.md:82,84; ETFExperiment/report.md:360,447,506; ETFExperiment/REGISTRATION.md:982,1010,1129)
- **Evidence:**
  - The accrual is a calendar count times one measured ratio, with the admissibility factor assumed rather than measured. `scripts/power_gate.py:71` sets `printed_rate = 333 / 336`; `:78-80` sets every forward scenario to `achieved_forward + round(weekdays × printed_rate)`. The comment above it says what was measured: "the census measured 333 printed days in 336 weekday rows over the window" (ETFExperiment/scripts/power_gate.py:69-70). What is *not* measured is the probability that this repository's own capture serves that day's value strictly before the anchor — the only thing that makes a forward day admissible under Section 3.3 (ETFExperiment/REGISTRATION.md:194-196). It is set implicitly to 1.0.
  - Zero forward days were admissible when the figure was computed: `"admissible_forward_capture": 0` (ETFExperiment/reports/stage_a2/census.json:3), echoed in `power.json` as `"achieved_forward_only": 0` (ETFExperiment/reports/stage_a2/power.json:114). Two forward captures existed, both recording the open day as absent (ETFExperiment/progress.md:453-454).
  - The measurement that would have supplied the missing factor is the one that never ran: A.1 Task 3 measures "the count of days where no value exists before the provisional 08:00 UTC anchor" (governing prompt, ETFExperiment/progress.md:143) and is named as an A.1 measurement target in the very table that forbids planning numbers (ETFExperiment/REGISTRATION.md:580, "days with no value before the provisional anchor | **A.1 Task 3**").
  - The registration's governing correction forbids this class of figure by name: "**Therefore: no accrual, coverage, lag, retention, revision, or capture-density figure in this repository is registered before it is measured.**" (ETFExperiment/REGISTRATION.md:571-573), citing NPLExperiment's 9.4/month planning figure falsified at 0.5 (ETFExperiment/REGISTRATION.md:566-569).
  - Direction of the error is not the point; the label is. But note the direction is optimistic, and the closure is the one place an optimistic accrual helps: a lower true accrual would make the shortfall larger, so the closure's own robustness argument does not cover the figure it is built on.
- **Recomputation (if any):** Inputs: `weekdays_to_deadline = 153` (ETFExperiment/reports/stage_a2/power.json:121), `printed_day_rate = 0.9910714…` (:112), achieved 11 (ETFExperiment/reports/stage_a2/census.json:2). I re-ran the same arithmetic independently: weekdays from 2026-08-28 to 2027-03-31 = **153**, forward = round(153 × 0.99107) = **152**, all cohorts = **163** — exact matches to power.json:114-116, confirming the code. The prose figure 20.8/month is not emitted by the code; it reconstructs as 21 weekdays/month × 0.99107 = **20.81**, i.e. a round calendar constant times the one measured ratio. (My own calendar-months division of the same 152 days gives 21.5/month, so 20.8 is the conservative reading of an unmeasured quantity, not a measurement.) Script: `SCRATCH/work/agentA-ETF/power_recompute.py`.
- **What would resolve it:** Relabel as "projected forward accrual of 20.8 printed days per month, at an assumed forward admissibility of 1.0 (unmeasured; A.1 Task 3 incomplete)", or measure the factor — which is the 15-trading-day run that was dropped.
- **Confidence:** HIGH — the code path is three lines and the census records forward admissible days as zero.
- **Invalidated by later commits?:** no.
- **Disclosed by authors?:** partly — the record repeatedly says achieved forward capture is 0 (ETFExperiment/HYPOTHESES.md:70, ETFExperiment/report.md:264) and `power_gate.py`'s docstring at :30-36 explains the approximation. It is never reconciled with the word "measured" attached to the accrual rate in eight places, nor with Section 14.7.

---

### DRAFT-all-7
- **Repository / SHA:** ETFExperiment / 4d110027674e7b4cd2861cf4e0e74f975111daf1
- **Hypothesis or artifact:** H1 — the entry anchor, and the finality of the admissibility count
- **Direction:** A
- **Class:** PROCESS
- **Severity:** S3
- **Label:** DERIVED
- **Claim challenged (verbatim quote):** "If the measured **95th percentile first-print time falls later than 07:00 UTC**, the anchor moves to **the next whole hour after that percentile**, recorded by amendment **before any outcome read and before any admissibility count is final**." — ETFExperiment/REGISTRATION.md:178-181 (identically ADR-001, ETFExperiment/DECISIONS.md:22-27)
- **Evidence:**
  - The measurement that may move the anchor never existed: "**Not quoted.** The registration requires **15 US trading days** of forward capture before any lag figure is; **2 captures exist**" (ETFExperiment/progress.md:452-453).
  - The admissibility count was nevertheless produced, treated as final, and used to close: census 336 rows / 11 admissible (ETFExperiment/reports/stage_a2/census.json:1-2), carried into the power gate as achieved N (ETFExperiment/scripts/power_gate.py:65), into Amendment 3's power table (ETFExperiment/REGISTRATION.md:848) and into the closing figures (ETFExperiment/REGISTRATION.md:1010-1015).
  - The rule moves the anchor in one direction only — later (ETFExperiment/src/etf/anchor.py:70-82) — and a later anchor can only admit captures that a earlier one excluded. 53 out-of-sample days are excluded as `capture_too_late` at the provisional anchor (ETFExperiment/reports/stage_a2/census.json exclusion_reasons; ETFExperiment/reports/stage_a1/archive_density.json:122).
  - The repository's own retro evidence puts the print between +04:05 and +08:00 on D+1, with served-value captures at +07:11, +07:12, +07:16 ×3 and +07:59:43 (ETFExperiment/docs/ACCESS.md:413-414; capture times in ETFExperiment/reports/stage_a1/retro_revision.json rows) — a distribution whose 95th percentile plausibly sits past the 07:00 trigger.
  - The archive-density function has no anchor parameter at all: `qualifying_window` calls `entry_anchor(trade_day)` with the config default (ETFExperiment/src/etf/archive.py:90-95), so every density and census figure in the record is conditioned on the un-amended anchor with no sensitivity stated.
- **Recomputation (if any):** Anchor sensitivity of the timemap-admissible count, recomputed from the raw untracked timemaps (live `data/access/timemap-recent.txt`, `timemap-all_data.txt`, read 2026-09-03T19:40Z) with the window `[20:00 UTC on D, anchor on D+1)` exactly as ETFExperiment/src/etf/archive.py:90-95 defines it, over the same 333-day universe:

  | anchor hour | timemap-admissible days | share | capture_too_late |
  |---|---|---|---|
  | 08:00 (as used) | 37 | 0.1111 | 53 |
  | 09:00 | 40 | 0.1201 | 52 |
  | 10:00 | 43 | 0.1291 | 52 |
  | 12:00 | 48 | 0.1441 | 50 |
  | 14:00 | 56 | 0.1682 | 48 |

  The 08:00 row reproduces the repository's published figures exactly. Script: `SCRATCH/work/agentA-ETF/anchor_sensitivity.py`. **The effect is real but bounded**: at a 09:00 anchor the timemap-admissible count rises by 3 (and the served-value conversion on those marginal late captures should be better than the 11/34 average, because the print has landed by then), so achieved N would plausibly be 13–15 rather than 11 and the projected 163 would become roughly 165–167. It cannot restore the 0.60 density bar at any anchor the rule could produce.
- **What would resolve it:** Either record the anchor amendment as forgone with a stated sensitivity band on every anchor-dependent figure, or note that the closure's admissibility count was declared final in advance of a registered step whose direction is known.
- **Confidence:** HIGH that the registered ordering was not followed; HIGH that the magnitude is small, which is why this is S3 and not higher.
- **Invalidated by later commits?:** no.
- **Disclosed by authors?:** partly — ADR-001's Consequences discloses that "the print lands between roughly 04:00 and 08:00 UTC ... and therefore that **the anchor may well move**. **It has not moved and will not move on that evidence**" (ETFExperiment/DECISIONS.md:39-42). The record does not state that a final admissibility count was nonetheless produced and used to close, nor give any sensitivity to the anchor.

---

### DRAFT-all-8
- **Repository / SHA:** ETFExperiment / 4d110027674e7b4cd2861cf4e0e74f975111daf1
- **Hypothesis or artifact:** A.1 Tasks 3 and 4 — the measurement the repository declares to be its experiment
- **Direction:** A
- **Class:** PROCESS
- **Severity:** S3
- **Label:** READ
- **Claim challenged (verbatim quote):** "*Running `etf-snap` to 2026-09-22 to finish the revision leg, then disarming.* Bounded, dated, and it produces a reusable artifact rather than an option, which makes it the stronger of the two live options. Declined in favour of a clean halt matching NPDExperiment, HFExperiment and InsiderExperiment. A closed repository with a running process invites the reading that the experiment is live" — ETFExperiment/DECISIONS.md:613-618
- **Evidence:**
  - The measurement declined is the one the repository names as its whole point, in three places written before it: "The measurement that decides this repo is not the return. It is the publication lag and the revision rate. Treat STAGE A.1 : TASK 3 and STAGE A.1 : TASK 4 as the experiment." (governing prompt, ETFExperiment/progress.md:19); "Stage A.1 Tasks 3 and 4 are the experiment." (ETFExperiment/CLAUDE.md:20-21); "the class died on the lag, not on the model" (ETFExperiment/README.md:17-18).
  - The instrument was already armed and free. Armed 2026-08-28T20:17:11Z (ETFExperiment/report.md:165); cost roughly 33 requests/day and zero dollars (ETFExperiment/REGISTRATION.md:1085); the completion date was 2026-09-22, "about sixteen trading days out" (ETFExperiment/DECISIONS.md:603-604).
  - Elapsed instrument life, from the live repository's git history (read-only): armed in commit 699d4ad `feat: collectors armed…` at 2026-08-28T13:21:03-07:00 and disarmed in 4d11002 `Disarm etf-snap…` at 2026-08-28T19:43:48-07:00 — **6 hours 23 minutes against a registered minimum of 15 US trading days** (`lag_min_trading_days=15`, ETFExperiment/src/etf/config.py:183).
  - The ADR's own stated ground for declining is legibility, not evidence: "A closed repository with a running process invites the reading that the experiment is live" (ETFExperiment/DECISIONS.md:617-618).
  - The debt is transferred, not discharged: "That measurement must be made from scratch." (ETFExperiment/DECISIONS.md:611) — so the 15 trading days are still owed by whoever runs the next flow hypothesis in this house, and the retro n = 11 substitute is explicitly barred.
- **Recomputation (if any):** none beyond the git timestamps above.
- **What would resolve it:** Nothing recovers it now; the record would be improved by stating the forgone measurement as a liability carried forward with its price (15 US trading days of collection) rather than as a closed item.
- **Confidence:** HIGH — every element is quoted from the repository, and the ADR itself calls the declined option the stronger one.
- **Invalidated by later commits?:** no — 4d11002 is the disarming commit and is final.
- **Disclosed by authors?:** yes — ETFExperiment/REGISTRATION.md:1139-1153 ("The one measurement forgone, recorded as forgone rather than merely unmeasured"), ETFExperiment/DECISIONS.md:602-619, ETFExperiment/progress.md:592-599. The authors disclose this fully and at length; it is raised here only because it is the same decision as DRAFT-all-1 and DRAFT-all-2 seen from the instrument's side, and because presenting a disclosed limitation as a discovery would itself be a failure. It is capped at S3 for that reason.

---

## What I checked and found sound

Things I expected to find if the "closed too early" thesis held everywhere, and did not:

1. **The archive-density measurement itself is correct, and widening the window really is foreclosed.** I reproduced it end to end from the raw untracked timemaps: 336 out-of-sample date rows, 333 with a complete five-fund print, 451 union mementos, 37 timemap-admissible at the 08:00 anchor, 53 too-late, unbounded-window ceiling **112/333 = 0.3363**, crawl rate **0.316/day** — every figure matching ETFExperiment/reports/stage_a1/archive_density.json:118-125 and ETFExperiment/report.md:187-195. No window the registered rule could choose reaches 0.60. GO's elimination is robust.
2. **The Amendment 1 → Amendment 2 correction is exemplary.** 0.1111 from the timemap alone was falsified at 0.0330 by fetching all 37 captures, recorded as falsified rather than corrected in place (ETFExperiment/REGISTRATION.md:711-738; ETFExperiment/DECISIONS.md:440-459). The dashed-capture breakdown in retro_revision.json (23 dashed, 2 no-row, 1 HTTP 403) supports it exactly.
3. **`retro_revision.py` picks the right capture.** It takes `day.qualifying[-1]`, the last capture strictly before the anchor (ETFExperiment/scripts/retro_revision.py:57-58), which is the most favourable admissible choice; there is no understatement from picking an early dashed capture.
4. **The boundary is honoured in the data.** The latest served-value archived capture is 2025-10-23T07:59:43Z (ETFExperiment/reports/stage_a1/retro_revision.json, row for 2025-10-22) — the "+08:00" in ETFExperiment/docs/ACCESS.md:414 is that value rounded, not an admitted capture on the anchor instant.
5. **E1's minimum N of 237 is right.** My independent numpy/scipy reimplementation of the registered model gives E1 power 0.792 at n = 237 and 0.778 at n = 236, rho = 0.18, alpha_adj (ETFExperiment/reports/stage_a2/power.json:19 claims 237). The Section 9 sanity anchors ("near 250", "high hundreds to low thousands") held as reported.
6. **The E2 threshold variant the registration names does not rescue anything.** Section 8 names a threshold grid of 0/50/100/200M as a secondary (ETFExperiment/REGISTRATION.md:315-316). I powered the T = 0 case (trade share 1.0, position = sign of the signal) at rho = 0.18: E2 = 0.516 at n = 163, 0.628 at n = 237, 0.760 at n = 300 — **worse** than the registered T = 100M case (0.593 / 0.704 / 0.810). Widening the trade share lowers power here, so the unrun parameterisation would have made the shortfall larger. Script: `SCRATCH/work/agentA-ETF/e2_ts.py`.
7. **A longer horizon cannot solve an N shortfall.** Section 7 names the 1–20 day reversal profile as a secondary and the source study's 10-day total impact carries a larger t (4.49) than the next-day leg (3.12) (ETFExperiment/REGISTRATION.md:498,502). But a multi-day hold yields *fewer* independent observations, not more, so no horizon in the registered design reduces the achievable-N shortfall. Not a missed endpoint.
8. **The unpinned E2 minimum cannot rescue the hypothesis, and the record's claim about it is defensible.** Amendment 5 says "Every direction the unpinned figure could move makes the shortfall larger, never smaller" (ETFExperiment/REGISTRATION.md:1023-1024). Read as a statement about the *governing* minimum — max(E1's 237, E2's minimum) — it is correct, with a floor at 74 days. My finer E2 grid at rho = 0.18 (800 sims, 1,500 draws) reads 0.726 at n = 250, 0.743 at 260, 0.745 at 270, 0.761 at 275, 0.820 at 280, 0.810 at 300, putting the true E2 minimum near 280 rather than the 350–400 the amendment speculates — but 163 still falls short of 237 either way.
9. **Terms-of-service routing is sound.** TheBlock's rendered page was fetched and contains no server-rendered series, so the disallowed `/api/tbco` really was the only route (ETFExperiment/docs/ACCESS.md:66-69); Glassnode's data host returns 401. Neither endpoint was requested. The Farside robots.txt reading (one `Twitterbot` group, no `*` group, RFC 9309) is correct on the recorded 33 bytes.
10. **Outcome blindness held.** The pre-period pin is demonstrated on production payloads (72 readable pre-boundary, 72 of 72 and 500 of 500 gated post-boundary — ETFExperiment/reports/stage_a1/depth.json, ETFExperiment/docs/ACCESS.md:219-226), `verdict.py` is imported by nothing, and all six registered mutations were caught (ETFExperiment/report.md:409-416). Nothing suggests an outcome value was read.

**One observation that runs against my own thesis, recorded because leaving it out would be selective.** The E2 statistic as implemented is **cost-inert**: `observed = sum(edge)/traded - cost` and the permutation comparison is `perm_edge/traded - cost >= observed`, so the round-trip cost cancels exactly (ETFExperiment/src/etf/power.py:154 and :162; the docstring at :137-138 states the cancellation). Section 8 registers E2 as "exact one-sided lower bound above zero" on the mean **net** return (ETFExperiment/REGISTRATION.md:302-305), which requires clearing the 9 bp cost; the coded test does not. This makes the simulated E2 easier than the registered E2, so the governing minimum of 300 is a *lower* bound on what the registered statistic would need — which enlarges, not shrinks, the shortfall the closure rests on. It is a registration-to-implementation mismatch worth someone's attention in the other direction; it does not support closing too early.

---

## Live-repo access log

Live repository touched: `/home/kiros-li/Documents/GitHub/ETFExperiment`, read-only.
Purposes: (1) `git log`, `git rev-parse`, `git status`; (2) three untracked/gitignored files under
`data/access/` — `timemap-recent.txt`, `timemap-all_data.txt`, `farside_all_parsed.json` — read at
**2026-09-03T19:40Z** and used for the recomputations in DRAFT-all-4 and DRAFT-all-7. These are
UNANCHORED: they are not in git and may have changed since the anchor, though the repository has
been declared closed and every figure I derived from them reproduces the anchored reports exactly.
No `.env`, credential, token or session file was opened; `.env.example` was not read.

**Before (2026-09-03T19:37Z):**

```
$ git -C /home/kiros-li/Documents/GitHub/ETFExperiment status --porcelain
(no output — clean)
$ git -C /home/kiros-li/Documents/GitHub/ETFExperiment rev-parse HEAD
4d110027674e7b4cd2861cf4e0e74f975111daf1
```

**After (2026-09-03T19:47:04Z):**

```
$ git -C /home/kiros-li/Documents/GitHub/ETFExperiment status --porcelain
(no output — clean)
$ git -C /home/kiros-li/Documents/GitHub/ETFExperiment rev-parse HEAD
4d110027674e7b4cd2861cf4e0e74f975111daf1
```

Identical before and after. Nothing was written to the audited repository.

**Note for the record, not a finding against this audit:** the working tree carries an untracked
marker file `_CLOSED_DO_NOT_RUN_HERE` (written 2026-09-02, excluded via `.git/info/exclude`, so it
does not appear in `git status --porcelain`) stating that a coding session was opened in the closed
repository by mistake on that date. It is pre-existing and is not mine. I did not modify it.

Scratch scripts and outputs live only under
`/tmp/claude-1000/-home-kiros-li-Documents-GitHub-program-audit/5ca157a0-1746-4eb9-a1b8-f3732ea42bf4/scratchpad/work/agentA-ETF/`
(`anchor_sensitivity.py`, `power_recompute.py`, `e2_recompute.py`, `e2_ts.py`), referred to above as
`SCRATCH/work/agentA-ETF/`. No repository script was executed in place.
