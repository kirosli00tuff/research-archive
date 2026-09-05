# Agent A draft findings — ORBExperiment, part p2-decisions

**Repository / anchored SHA:** ORBExperiment / `f2aa675a80fc06b74979040b3028154d1add5ec0` (main, 2026-08-29 local / the rescue pass is dated 2026-08-30 UTC).
**Assigned documents (read completely):** `DECISIONS.md` (1,476 lines, ADR-001…ADR-038), `README.md` (544), `docs/ACCESS.md` (577), `docs/DUPLICATION.md` (128), `docs/HANDOVER.md` (403), `docs/STAGES.md` (60), `docs/STAGE_A_PROMPT.md` (255, skimmed for named-but-unrun variants), `reports/**/*.md` (5 files).
**Read for context only** (other readers' primary documents): `REGISTRATION.md`, `HYPOTHESES.md`, `reports/stage_a3rescue/*.json`. Findings whose primary evidence sits there are marked.

**Headline.** This repository is unusually disciplined. Its power arithmetic reproduces exactly, its
pre-commitment ordering is verifiable in `git log`, and its central closure survives every
sensitivity I could run against it. The findings below are therefore **not** an attack on the
`cost-bound` arithmetic — I could not break it. They are about **what the closure foreclosed**: two
registered, zero-dollar, zero-alpha routes that the repository itself had recorded as available and
then dropped without evaluating, one affirmative claim of confirmation the underlying artifact
cannot support, one cull whose stated ground its own later measurement inverts, and four hygiene
items on stale or mis-derived figures.

---

### DRAFT-p2-decisions-1
- **Repository / SHA:** ORBExperiment / f2aa675a80fc06b74979040b3028154d1add5ec0
- **Hypothesis or artifact:** H1 (H-ORB) closure as `cost-bound`, 2026-08-30 — ADR-036/ADR-038, Amendment 28
- **Direction:** A
- **Class:** OVER_CLOSED
- **Severity:** S2
- **Label:** DERIVED
- **Claim challenged (verbatim quote):** "**`NOT_RESCUED`** otherwise, **with H1 closing as `cost-bound`** and **no further rescue lever applied**." — ORBExperiment/DECISIONS.md:1350-1351
- **Evidence:**
  - The registration prices **eight** specifications into E1's deflation: "**trial count registered at 8**, being **four opening-range lengths (5, 15, 30 and 60 minutes) crossed with two entry rules (immediate-direction and true-breakout)**" — ORBExperiment/REGISTRATION.md:439-441 (context read; other reader's document).
  - Seven of those eight are **already registered as named secondaries carrying no additional alpha**: "The 15, 30 and 60-minute range lengths; the immediate-direction entry … **the registered trial count of 8 already prices the range-length and entry-rule crossings into E1's deflation.**" — ORBExperiment/REGISTRATION.md:465-471, repeated at 606-608.
  - The deciding cost input was measured **once**, on the registered 5-minute true-breakout rule only: `first_session` 2026-07-01, `last_closed_session` 2026-08-28, `sessions_used` 28, `tickers_with_bars` 199, `quote_requests_sent` 759 — ORBExperiment/reports/stage_a3rescue/task2_slippage_band.json:11,13,115,116,118. Cost of that measurement: **0 dollars** — ORBExperiment/README.md:285.
  - The deciding shift is dominated by a quantity that is a property of the **entry minute and the name**, not of the breakout rule: entry half-spread median 0.076572, p90 0.333662, n = 550 minutes, 0 refused — ORBExperiment/README.md:300; task2_slippage_band.json:72-78. Recomputed, the half-spread's p90−median alone supplies **0.257090 of the 0.467065 shift = 55.04 percent**.
  - The mechanism that moves the *other* side of the deciding ratio is one the repository itself measured, on these same 28 sessions, at **0 requests**: raising the price floor 5→100 USD lifted the implied central mean 0.040386 → 0.085626 (dispersion 2.029585 → 3.199162, priced trades 550 → 304) — ORBExperiment/reports/stage_a3rescue/task4_floor_scan.json:11,14-28,82-96; ORBExperiment/README.md:323-329. A longer opening range moves the **same two inputs** (fewer of the 20 selected names trigger inside a shorter remaining session, and the stop distance widens), and neither was scanned.
  - After the closure the repository states "**There is no ladder any more. H1 is closed, and everything below is an operator decision rather than a next step.**" — ORBExperiment/docs/HANDOVER.md:126 — and lists four routes (a)-(d) at docs/HANDOVER.md:252-275. **None of the four is "measure the band at the other three registered range lengths or the second registered entry rule."** Amendment 28 §4's list of what "was available" and was not done (REGISTRATION.md:4124-4138) also omits it.
- **Recomputation (if any):**
  Inputs: carried band 0.020/0.040 entry, 0.040/0.080 stop, 0.010/0.020 close — DECISIONS.md:244-246; measured band 0.087019/0.354645, 0.033529/0.198061, 0.040000/0.261000 — README.md:291-296; measured stop share 0.381818 — README.md:260; entry half-spread median/p90 0.076572/0.333662 — README.md:300; implied-mean constant 0.02884727 — DECISIONS.md:1194; dispersion 2.029585 and trades/session 19.64 — README.md:220-221.
  Method: `shift = (e_p90−e_med) + s·(st_p90−st_med) + (1−s)·(cl_p90−cl_med)`; leg shares by division. Script `/home/kiros-li/.cache/program-audit/scratchpad/work/agentA-ORB-p2/recompute.py`.
  Result: measured shift **0.467066** (document 0.467065, agrees to 1e-6). Leg shares entry **0.5730**, stop **0.1345**, close **0.2925**. Entry half-spread part **0.257090** = **55.04 percent** of the whole shift; entry overshoot part only **0.010536** = 2.26 percent. So the single quantity carrying most of the closure is the quoted half spread at the entry minute of a **5-minute** range.
  Also recomputed: μ_central = SR·σ/√(252·k) reproduces every floor-scan row (floor 100: 1.40·3.1991620/√(252·10.857) = **0.085628** vs the artifact's 0.08562611), so the numerator channel is `σ` and `k` and is measurable at zero requests.
  **Materiality, stated against my own thesis:** the required reduction is `0.467065 / 0.040386 = 11.5652×`. The one lever the repository actually scanned supplied `2.1424/0.9742 = 2.199×`. I have **no** measurement showing the range-length secondaries supply the remaining 5.3×, and I do not claim they would.
- **What would resolve it:** re-run `tools/slippage_band.py` and the carve-out dispersion writer at the registered 15, 30 and 60-minute range lengths (and, separately, at the immediate-direction entry) on the same post-holdout carve-out, and record the central-mean-to-shift ratio for each. That is zero dollars, zero additional alpha (the eight trials are already deflated for) and no new registration, since all four lengths and both entry rules are already registered. If every ratio stays below 1, the closure generalises from H1's specification to the registered family and should say so; if one crosses, `cost-bound` was scoped to one of eight registered specifications and the record should say that instead.
- **Confidence:** MEDIUM — the facts (variant registered, alpha already paid, measurement never run, absent from every post-closure route) are certain; the materiality is unproven and the required 11.57× reduction is large.
- **Invalidated by later commits?:** no — the anchor is `HEAD` of the live repository (verified `git rev-parse HEAD` = f2aa675, no commits after the anchor).
- **Disclosed by authors?:** no — REGISTRATION.md:606-608 says a verdict "is never evidence about any range length or entry rule other than the registered one", which correctly scopes a *positive* verdict, but no document states that the measured cost band is likewise specific to the 5-minute true-breakout specification, and no route names re-measuring it.

---

### DRAFT-p2-decisions-2
- **Repository / SHA:** ORBExperiment / f2aa675a80fc06b74979040b3028154d1add5ec0
- **Hypothesis or artifact:** H1 closure vs Amendment 21 route (a) — the narrowed verdict scope with E2 demoted to a named secondary
- **Direction:** A
- **Class:** OVER_CLOSED
- **Severity:** S2
- **Label:** READ
- **Claim challenged (verbatim quote):** "**None of the three depends on 2026-09-12.** **This decision can be taken today, and items 1 to 3 cannot resolve it.**" — ORBExperiment/docs/HANDOVER.md:299-300 (this sentence now sits inside the block headed "**Superseded item 4 — the collapsed-E2 routes of Amendment 21.**" — docs/HANDOVER.md:277)
- **Evidence:**
  - Route (a), as the repository stated it on 2026-08-29: "**(a) A narrower verdict scope conditional on central costs alone**, with **E2 demoted to a named secondary**. E1 is powered at **0.832450**." — ORBExperiment/docs/HANDOVER.md:284-286; identical text at ORBExperiment/README.md:506-508. It needs no new data, no spend, no broker credential and no calendar.
  - The pre-committed criterion has exactly **two** tiers and never mentions it: `RESCUED_DEGRADED` / `NOT_RESCUED`, the latter "**with H1 closing as `cost-bound`** and **no further rescue lever applied**" — ORBExperiment/DECISIONS.md:1348-1351.
  - Amendment 28 §4 lists what "was available" and was deliberately not done — the cost band, the effect assumption, the alpha, the stop share, statistic selection, a weaker E2, H1b — ORBExperiment/REGISTRATION.md:4124-4138 (context read). **Route (a) is not on that list.** §5 names only route (b), "real execution evidence", as "the honest attack on this closure" — REGISTRATION.md:4154-4157.
  - The post-closure live item 4 offers four routes — (a) stop here, (b) run the 2026-09-12 re-pull anyway, (c) open H1b, (d) pursue Amendment 21 route (b) — ORBExperiment/docs/HANDOVER.md:252-275. **Amendment 21 route (a) is absent**, and route (c) of the superseded list (`untestable-at-achievable-power`) is absent too. No reason is given for either omission; the whole block is simply relabelled "Superseded item 4" (docs/HANDOVER.md:277).
  - Timing, from the live repository's own history (read-only `git log`, 2026-09-04 UTC): `4ae14dc` "the rescue-pass success criterion, pre-committed" 2026-08-29T20:13:26−0700 → `5899e1b` "the slippage band measured" 20:41:12 → `7edeea7` "NOT_RESCUED" 20:41:59 → `34a91b3` "H1 CLOSED as cost-bound" 20:43:15. **The whole pass, from writing the two-tier criterion to closing the hypothesis, spans 33 minutes**, and the closure follows the deciding measurement by 123 seconds. The pre-commitment claim itself is **sound** (see the sound list); what the timeline shows is that the decision to drop a registered alternative was taken inside a single automated pass with no deliberation step.
- **Recomputation (if any):** none needed beyond confirming E1's stated power, which reproduces exactly: at α = 0.05 one-sided, t = (1.40/√252)·√875 = 2.608746, power = 1 − Φ(1.644854 − 2.608746) = **0.832450** (document 0.832450, README.md:404); minimum n for 80 percent = ((1.644854+0.841621)/(1.40/√252))² = **794.9 → 795** (document 795, README.md:404). So route (a)'s premise — that E1 alone is powered on the achievable holdout — is arithmetically correct at the anchor.
- **What would resolve it:** a dated entry saying, in the closure amendment itself, why route (a) was not taken — most plausibly that demoting a co-primary after seeing a null re-specifies the registration and is the factor-zoo behaviour ADR-037 refused for H1b. That reason is defensible and would settle it; it simply is not written anywhere. Alternatively, restore route (a) to the live item 4 so the operator sees the option the repository said was available.
- **Confidence:** HIGH — the route is quoted verbatim from the repository's own documents, its omission from Amendment 28 §4 and from the live item 4 is checkable by grep, and no supersession reason is stated.
- **Invalidated by later commits?:** no — no commits exist after the anchor.
- **Disclosed by authors?:** partly — the superseded block is left visible at docs/HANDOVER.md:277-300, which is honest record-keeping, but nothing states that route (a) was considered and rejected, and Amendment 28 §4's explicit "what was available and was not done" list omits it.

---

### DRAFT-p2-decisions-3
- **Repository / SHA:** ORBExperiment / f2aa675a80fc06b74979040b3028154d1add5ec0
- **Hypothesis or artifact:** H1b price-floor feasibility scan, 2026-08-30 (ADR-037, Amendment 27) — the only alternative lever offered to the operator after the closure
- **Direction:** A
- **Class:** INTERNAL_INCONSISTENCY
- **Severity:** S2
- **Label:** DERIVED
- **Claim challenged (verbatim quote):** "**The registered mechanism is confirmed** — the ratio rises monotonically while the shift stays inside a 4 percent band, which is the price-invariance H1b asserted before the scan." — ORBExperiment/README.md:331-333
- **Evidence:**
  - The scan's `shift_usd_per_share` column is **not a measurement of slippage at any floor**. It is the *carried* QQQ band's shift evaluated at each floor's own stop-exit share: the artifact says so — "The shift here is the **registered Section 6 band shift** at each floor's own measured stop-exit share" — ORBExperiment/reports/stage_a3rescue/task4_floor_scan.json:5.
  - Recomputed exactly (below): with carried constants the shift is identically `0.030 + 0.030·s`, a function of the stop share **only**. It therefore cannot vary with price under any circumstances, and "stays inside a 4 percent band" is arithmetic on constants, not evidence about price-invariance.
  - The scan's own stated "independent check on the invariance half" is the entry-overshoot median (task4_floor_scan.json:5,18,35,52,69,86), which is **0.0 at every one of the five floors** — and the repository elsewhere says why that is uninformative: "**The entry-overshoot median is 0.0000 at every floor**, which is a **one-minute resolution limit and not a measurement that overshoot is zero**" — ORBExperiment/README.md:344-347.
  - The handover document states the opposite conclusion to the README: "a raised floor improves the ratio only if the spread does not scale with price — **which the scan's overshoot column cannot confirm** at one-minute resolution." — ORBExperiment/docs/HANDOVER.md:268-271.
  - The same pass, on the same 28 carve-out sessions, **did** measure real per-leg slippage (entry median 0.087019 / p90 0.354645, n = 550 — README.md:291-292) and the scan was **not** re-run on it. Under the measured shift the ratio at the registered 5 USD floor is 0.040386/0.467065 = **0.0865**, not 0.9742.
- **Recomputation (if any):**
  Inputs: the five scan rows, `shift_usd_per_share` 0.041455 / 0.041782 / 0.041488 / 0.040866 / 0.039967 — reports/stage_a3rescue/task4_floor_scan.json:25,42,59,76,93 (mirrored at README.md:325-329); carried band constants 0.020/0.040, 0.040/0.080, 0.010/0.020 — DECISIONS.md:244-246.
  Method: solve `shift = 0.020 + s·0.040 + (1−s)·0.010 = 0.030 + 0.030·s` for the implied stop share `s` at each floor.
  Result: implied `s` = **0.381833, 0.392733, 0.382933, 0.362200, 0.332233** — every row reproduces to 6 decimals from the carried constants and the stop share alone. Ratio column check: 0.040386/0.041455 = 0.9742, 0.041711/0.041782 = 0.9983, 0.047358/0.041488 = 1.1415, 0.060344/0.040866 = 1.4766, 0.085626/0.039967 = 2.1424 — all match the artifact. The **entire** movement in the ratio column comes from the numerator (dispersion 2.029585 → 3.199162 and priced trades 550 → 304, i.e. μ ∝ σ/√k); the denominator carries **no** price information at all.
- **What would resolve it:** either strike the "price-invariance … confirmed" sentence from README.md:331-333 and replace it with the handover's formulation, or re-run `tools/slippage_band.py` per price floor so the denominator is measured rather than carried. The second is zero dollars — the quote data for all 28 sessions was already pulled (759 quote requests, 0 refused, README.md:285-287).
- **Confidence:** HIGH — the functional form is exact at all five rows and the artifact itself names the shift as the registered (carried) band.
- **Disclosed by authors?:** partly — the two components are disclosed separately (the overshoot resolution limit at README.md:344-347 and docs/HANDOVER.md:270-271; the shift's provenance at task4_floor_scan.json:5). What is not disclosed is that combining them leaves **nothing** in the scan capable of testing price-invariance, and README.md:331-333 states the opposite as a confirmed result.
- **Invalidated by later commits?:** no — no commits after the anchor.

---

### DRAFT-p2-decisions-4
- **Repository / SHA:** ORBExperiment / f2aa675a80fc06b74979040b3028154d1add5ec0
- **Hypothesis or artifact:** ADR-013 — the index-ETF opening-range variant, culled 2026-08-29 (HYPOTHESES.md cull 1)
- **Direction:** A
- **Class:** OVER_CLOSED
- **Severity:** S3
- **Label:** DERIVED
- **Claim challenged (verbatim quote):** "*Testing it as a control*: it would spend sample and attention re-measuring a **settled cost problem**, and the replication already answered it more carefully than this repository could." — ORBExperiment/DECISIONS.md:365-367
- **Evidence:**
  - The cull's deciding numbers are all about the excluded variant's *cost* problem: "the **entire gross edge of 0.070 USD/share sits inside the spread**, with net PnL crossing zero at **~0.022 USD/share** against a QQQ spread near **0.010**" — ORBExperiment/DECISIONS.md:355-358, restated at DECISIONS.md:238-241 (ADR-009).
  - The retained single-name universe was measured on 2026-08-30 at an entry slippage **median 0.087019 USD/share, n = 550** — ORBExperiment/README.md:291; reports/stage_a3rescue/task2_slippage_band.json:89 — with a time-weighted quoted **half** spread median of **0.076572** on the same 550 minutes (README.md:300).
  - The repository's own closure text names this as the cause of death: "the measured entry half spread of **0.076572 median** is what killed H1" — ORBExperiment/docs/HANDOVER.md:268-269.
  - The cull was never revisited. `HYPOTHESES.md` still asserts of all ten culls "**None was closed on a measurement**, and none of them is reopened by anything H1 does." — ORBExperiment/HYPOTHESES.md:117-118 (context read; other reader's primary document). ADR-013 is not superseded by any later ADR (DECISIONS.md ends at ADR-038, and no ADR names ADR-013).
- **Recomputation (if any):**
  Inputs: 0.022 USD/share break-even entry slippage for the excluded variant (DECISIONS.md:240); QQQ spread near 0.010 (DECISIONS.md:241); measured median entry slippage on the retained universe 0.087019 (README.md:291); measured median entry half spread 0.076572 (README.md:300).
  Method: direct ratios.
  Result: the retained universe's **median** entry slippage is **3.955×** the entry-slippage level at which the excluded variant's edge was measured to die, and its median **half** spread alone is **7.657×** the QQQ spread that killed it. Whatever else separates the two variants, the retained one is not the cheaper one to execute, and the cull's stated ground — that the ETF variant is the settled *cost* problem — reads differently after 2026-08-30.
- **What would resolve it:** one dated line in `DECISIONS.md` or `HYPOTHESES.md` recording that the 2026-08-30 measurement shows the retained universe's execution costs exceed the excluded variant's by the ratios above, and stating whether cull 1's ground still holds. This is a record correction, not a re-opening; the replication genuinely did answer the ETF variant more carefully than this repository could, and that half of the ADR is untouched.
- **Confidence:** MEDIUM — the two figures are exact and both are from this repository, but they are not strictly commensurable (0.070 gross edge for the excluded variant vs a 0.040386 *implied net* mean for the retained one), so this shows the cull's ground is no longer clean rather than that it was wrong.
- **Invalidated by later commits?:** no — no commits after the anchor.
- **Disclosed by authors?:** no — no document revisits cull 1 after the band measurement, and HYPOTHESES.md:118 still says none of the culls is reopened by anything H1 does.

---

### DRAFT-p2-decisions-5
- **Repository / SHA:** ORBExperiment / f2aa675a80fc06b74979040b3028154d1add5ec0
- **Hypothesis or artifact:** the measured slippage band (ADR-038 / Amendment 26) — the n reported with the deciding figures
- **Direction:** A
- **Class:** STATISTICAL
- **Severity:** S3
- **Label:** DERIVED
- **Claim challenged (verbatim quote):** "| entry half spread, time-weighted | median **0.076572**, p90 **0.333662** | **550 minutes, 0 refused** |" — ORBExperiment/README.md:300 (same rows at docs/HANDOVER.md:59 and README.md:301-303)
- **Evidence:**
  - The registration fixes the independent unit for exactly this reason: E2 is computed "by **permutation on session labels with trades clustered by session date**, so that **a single strong session cannot masquerade as many independent observations**" — ORBExperiment/REGISTRATION.md:448-451 (context read). The repository restates it: "**The portfolio-day series remains the binding constraint**, as Section 9 states: trades inside a session share that session's market factor, which is why E2 permutes on session labels." — ORBExperiment/reports/stage_a2/power.md:88-89 (my document).
  - The band's own n's are reported per observation, not per cluster: entry n = 550 minutes, stop n = 210, close n = 340 — README.md:300-303 — drawn from **28 evaluable sessions**, `sessions_used: 28` — reports/stage_a3rescue/task2_slippage_band.json:116; "carve-out sessions read / evaluated | **42 / 28**" — README.md:235.
  - Quoted spreads are a same-day market-wide quantity in exactly the way the registration's clustering rule is written against: one volatile session widens the spread on every name in it simultaneously.
  - The deciding percentiles are read off those uncorrected distributions: entry p90 0.333662 (half spread), 0.354645 (total) — task2_slippage_band.json:77,91.
- **Recomputation (if any):**
  Inputs: n = 550 / 210 / 340 (README.md:300-303), 28 evaluable sessions (task2_slippage_band.json:116).
  Method: mean cluster size = n / sessions; design effect `deff = 1 + (m−1)·ρ`.
  Result: mean cluster size **19.64** (entry), **7.50** (stop), **12.14** (close). At an illustrative intra-session correlation of ρ = 0.3 the entry leg's effective n falls from 550 to **83**; at ρ = 1 it is **28**. ρ is **not measured here and I do not claim a value** — the point is that the effective n for every deciding percentile lies between 28 and 550, and 28 is the number of independent session-days, not 550.
  **Materiality, stated plainly:** this does **not** flip the closure. Bringing the pessimistic-cost mean to zero needs the shift to fall from 0.467065 to 0.040386, an **11.57×** reduction; no plausible interval on a p90 from 28 clusters spans that.
- **What would resolve it:** report the six band ends with a session-clustered (block-bootstrap over the 28 sessions) interval, or state the session count in the same sentence as the percentile, on the same terms standing rule 13 attaches an n.
- **Confidence:** HIGH on the inconsistency (the registration's clustering rule and the band's per-observation n are both quoted), LOW on materiality (the margin is far too wide to be closed by this).
- **Invalidated by later commits?:** no — no commits after the anchor.
- **Disclosed by authors?:** partly — the 42/28 session counts are disclosed (README.md:235,285; REGISTRATION.md:4147-4151) and the post-holdout regime caveat is attached everywhere, but no document notes that the band's n's are not the registration's own independence unit.

---

### DRAFT-p2-decisions-6
- **Repository / SHA:** ORBExperiment / f2aa675a80fc06b74979040b3028154d1add5ec0
- **Hypothesis or artifact:** `docs/STAGES.md` (the stage ladder) and `docs/ACCESS.md`'s registered operating pace
- **Direction:** A
- **Class:** STALE_FIGURE
- **Severity:** S3
- **Label:** READ
- **Claim challenged (verbatim quote):** "| **A.1 TASK 3–4 re-run** *(next; blocked on an operator item)* | … | **Two free-tier credentials, two different vendors.** An operator action | …" — ORBExperiment/docs/STAGES.md:22
- **Evidence:**
  - The credential blocker was discharged on the same day the document was written: "**Two credentials authenticate and both serve one-minute bars. `n = 2` credentials, `2` authenticating, `0` refused.**" — ORBExperiment/docs/ACCESS.md:321-322; vendor selection made in a dated ADR — ORBExperiment/DECISIONS.md:672-699 (ADR-023).
  - `docs/STAGES.md` nonetheless still states, at the anchor, "**Status at 2026-08-29: Stage A complete except for the two integrity measurements. Section 0 fired `PENDING_ACCESS`. H1 is OPEN. Nothing is armed and nothing is closed.**" — docs/STAGES.md:3-5 — against README.md:26 "**Status: H1 is CLOSED — `cost-bound` — 2026-08-30**" and docs/HANDOVER.md:5-6 "**H1 IS CLOSED.**"; and repeats the discharged blocker at docs/STAGES.md:51-53 ("**Blocked on an operator item** — two free-tier vendor credentials").
  - It also carries a superseded software figure: "**n = 10 mutations, 0 harness failures**" — docs/STAGES.md:20 — against the table row "| mutations applied to real source | **17**, **0 harness failures** |" — README.md:440.
  - Second instance, same class, different document: `docs/ACCESS.md`'s registered operating pace still reads "| `alpaca:*` | **1.0 s** | **60.0** | **unmeasured ceiling**; half of a 134.05/min *observed admitted rate* is 67/min |" and "**Per-vendor daily caps, charged before sending: Massive 600, Alpaca 2,000.**" — docs/ACCESS.md:532,534 — against the Amendment 14 figures "| **`alpaca:bars`** | **0.61 s** | **98.36** | **measured** — half of a **199.73/min sustained** rate, `n = 250` …" and "**Daily caps, charged before sending: Massive 600, Alpaca 3,000** (Amendment 14)." — docs/HANDOVER.md:196,199; DECISIONS.md:1050,1060-1062 (ADR-030). Unlike its other superseded claims, this one is **not** listed in `docs/ACCESS.md`'s own "What was falsified in the section above this line" table (docs/ACCESS.md:567-573).
- **Recomputation (if any):** none — this is a document-to-document comparison at fixed line numbers.
- **What would resolve it:** a supersession block at the top of `docs/STAGES.md` on the pattern `docs/ACCESS.md` already uses successfully (leave the stale text standing, label it), and one additional row in `docs/ACCESS.md`'s falsification table for the Amendment 14 pace and daily cap.
- **Confidence:** HIGH — every figure is quoted and the contradictions are within the same anchored tree.
- **Invalidated by later commits?:** no — no commits after the anchor.
- **Disclosed by authors?:** no — `docs/STAGES.md` carries no supersession note, and the pace change is absent from `docs/ACCESS.md`'s own falsification table. `docs/STAGES.md` is not in the README's reading order (README.md:533-534), which limits the harm but does not remove it.

---

### DRAFT-p2-decisions-7
- **Repository / SHA:** ORBExperiment / f2aa675a80fc06b74979040b3028154d1add5ec0
- **Hypothesis or artifact:** the H1 closure summary table in `docs/HANDOVER.md`
- **Direction:** A
- **Class:** ARITHMETIC
- **Severity:** S4
- **Label:** DERIVED
- **Claim challenged (verbatim quote):** "| **pessimistic-cost mean** | **−0.426679** — negative by **11.56×** | — |" — ORBExperiment/docs/HANDOVER.md:62
- **Evidence:**
  - Central mean at the registered 1.40 assumption: **0.040386** — README.md:263; reports/stage_a3rescue/task3_rescue_verdict.json:9.
  - Pessimistic-cost mean under the measured band: **−0.426679** — README.md:305; reports/stage_a3rescue/task3_rescue_verdict.json:14. (README.md:264's **−0.001068** is the *carried*-band figure and is not the one this row cites.)
  - Measured shift: **0.467065** — README.md:304; task3_rescue_verdict.json:13.
  - The figure **11.56** is correct where the registration uses it — "**The shift exceeds it by 11.56 times.**" — REGISTRATION.md:4082 (context read) — because that is `shift ÷ central mean`. `docs/HANDOVER.md:62` attaches the same number to a different quantity.
- **Recomputation (if any):**
  Inputs as above. Method: `|−0.426679| / 0.040386` and `0.467065 / 0.040386`.
  Result: **|pessimistic mean| ÷ central mean = 10.5650**; **shift ÷ central mean = 11.5650**. The two differ by exactly 1 because `|c − s|/c = s/c − 1`. `docs/HANDOVER.md:62` therefore overstates the margin against H1 by **9.5 percent** of its own value. (The same error appears at HYPOTHESES.md:59, "negative by 11.56 times the central mean" — other reader's document, noted for dedup.)
- **What would resolve it:** change `11.56×` to `10.56×` at docs/HANDOVER.md:62, or relabel the row as the shift-to-central-mean ratio.
- **Confidence:** HIGH — three-figure arithmetic on the repository's own numbers.
- **Invalidated by later commits?:** no — no commits after the anchor.
- **Disclosed by authors?:** no — the figure is presented as a derived multiple with no caveat. It does not move the closure; it is recorded because this repository's own standard is that a figure travels correctly with its quantity.

---

### DRAFT-p2-decisions-8
- **Repository / SHA:** ORBExperiment / f2aa675a80fc06b74979040b3028154d1add5ec0
- **Hypothesis or artifact:** README's "Bar integrity — A.1 TASK 3 and TASK 4, **the two that decide this repository**" table
- **Direction:** A
- **Class:** STALE_FIGURE
- **Severity:** S4
- **Label:** READ
- **Claim challenged (verbatim quote):** "| delisted names served with intraday history | **`Absent(not_yet_measured)`** | 0 |" — ORBExperiment/README.md:355
- **Evidence:**
  - The same README records the measurement 160 lines earlier: "| **delisted names with intraday history** | **203** — **`PASS`**, share 0.8865 | **229 checked** |" — ORBExperiment/README.md:195.
  - And `docs/ACCESS.md` records the verdict in full: "**Verdict: `PASS` — 203 delisted names with intraday history, `n = 229` in-window names checked on Alpaca, share 0.8865.**" — ORBExperiment/docs/ACCESS.md:464; and the handover carries it too — docs/HANDOVER.md:90.
  - The other two rows of the same table (bar revision rate, cross-vendor agreement) **are** genuinely `Absent` and eligible 2026-09-12 — README.md:353-354; docs/HANDOVER.md:91-92 — so the table as a whole reads as "three of three absent" when the correct reading is two of three.
- **Recomputation (if any):** none — a within-document contradiction at fixed line numbers.
- **What would resolve it:** replace README.md:355 with the measured row, or strike it from a table headed as the two measurements that decide the repository (delisted coverage is a third, and it passed).
- **Confidence:** HIGH — both lines are in the same file.
- **Invalidated by later commits?:** no — no commits after the anchor.
- **Disclosed by authors?:** no.

---

### DRAFT-p2-decisions-9
- **Repository / SHA:** ORBExperiment / f2aa675a80fc06b74979040b3028154d1add5ec0
- **Hypothesis or artifact:** the dating of the rescue-pass report artifacts
- **Direction:** A
- **Class:** PROVENANCE
- **Severity:** S4
- **Label:** DERIVED
- **Claim challenged (verbatim quote):** "**Run 2026-08-29. n = 17 mutations applied to real source, each restored green afterwards. Bytecode is purged before every run.**" — ORBExperiment/reports/stage_a4/mutations.md:3
- **Evidence:**
  - `reports/stage_a4/mutations.md` is **byte-identical** to `reports/stage_a3rescue/mutations.md` (verified with `diff` on the snapshot; both 25 lines), including mutation 17, whose description pins "the per-leg summary contract of **Amendment 26**" — reports/stage_a4/mutations.md:25 — and Amendment 26 / ADR-038 is dated **2026-08-30** (DECISIONS.md:1426). The A.4 report therefore carries 2026-08-30 content under a 2026-08-29 header, and `docs/STAGES.md:20` still cites "n = 10 mutations" for the same task, so three different counts (10 / 17 / 17) attach to A.4 TASK 2 across the tree.
  - Second instance, in the artifact that records the closure: `"computed_at": "2026-08-29"` and `"criterion_precommitted_on": "2026-08-30"` sit four lines apart in the same file — reports/stage_a3rescue/task3_rescue_verdict.json:3,6 — alongside `"criterion_precommitted_before_the_measurement": true` (line 5). Read literally, the deciding artifact says the criterion was committed the day **after** the measurement it decided.
  - The underlying ordering is in fact correct, and I verified it read-only against the live repository: `4ae14dc` (criterion) 2026-08-29T20:13:26−0700, `5899e1b` (band measured) 20:41:12, `7edeea7` (NOT_RESCUED) 20:41:59. The two dates are the same instants expressed in local time and UTC; nothing is wrong except the labelling.
- **Recomputation (if any):** `diff reports/stage_a4/mutations.md reports/stage_a3rescue/mutations.md` → identical; `git log --format='%h %ad %s' --date=iso` on the live repository for the four commits above.
- **What would resolve it:** stamp both report headers and both JSON date fields in one timezone (the repository's own convention elsewhere is UTC, which is why the rescue pass is dated 2026-08-30), and stop overwriting a stage's report file with a later stage's run.
- **Confidence:** HIGH — the diff and the git timestamps are mechanical.
- **Invalidated by later commits?:** no — no commits after the anchor.
- **Disclosed by authors?:** no. This is hygiene, not a substantive defect: the pre-commitment claim on which the whole closure's credibility rests is **true**, and the repository invites exactly this check ("**the ordering is checkable in `git log` by anyone who doubts it**" — DECISIONS.md:1345). The mislabelled dates make that check harder than it needs to be.

---

## Cross-repo candidates (for the cross-repository pass)

Two of this repository's registered open items ask for something a sibling repository may already
hold. I have **not** verified any of this against the sibling repositories — that is the cross-repo
pass's job. Flagged here with the ORBExperiment-side evidence only.

1. **Open item 1 — "a third feed on a genuinely different upstream"** (README.md:469-475;
   docs/HANDOVER.md:210-216). ORBExperiment holds only Alpaca-SIP and Massive, measured to share one
   upstream (IQR [1.003096, 1.007726] over n = 100 pairs — docs/ACCESS.md:382,407-410), so its
   agreement gate "**is not the Concretum test**". The item is recorded with **no candidate vendor
   named and no cost attached**, even though `docs/ACCESS.md` records Databento and Tiingo as
   terms-permitted and merely uncredentialed (docs/ACCESS.md:198-199, 560). Separately,
   `docs/DUPLICATION.md:116-118` records that **HFExperiment "reaches a US equity *broker* (IBKR,
   Alpaca calendar)"** and is the source of the integer-share constraint carried into this
   registration (error 10243, `reports/stage_a1b/a1b_report.md` line 52 — DECISIONS.md:268-270).
   **Lead:** if HFExperiment holds an IBKR market-data entitlement, that is a bar source on a
   genuinely different upstream from two SIP redistributors, and it would bear directly on this
   item at no new spend. Unverified from here.
2. **SL-3 — "all 1,762 in-sample sessions rest on a single unverified feed"**, retirable by "a
   reference credential whose tier reaches **2016-01-04**" (README.md:485-497;
   docs/HANDOVER.md:225-246; DECISIONS.md:909-951). Same lead as above, widened: any sibling
   repository holding a US-equity minute-bar credential reaching 2016 would retire SL-3 on
   measurement rather than on operator acceptance.
3. **Culls 9 and 10 are already cross-referenced by the authors** — Hyperliquid listing drift →
   NPLExperiment H1 (closed 2026-08-28, 197/312, lower bound 0.5707 against a 0.60 bar), spot
   Bitcoin ETF flow → ETFExperiment H-ETF (HYPOTHESES.md:130-131, other reader's document). Both are
   labelled DUPLICATE with the holding repository named; no action needed, listed so the cross-repo
   pass does not re-derive them.
4. **Cull 1, the index-ETF opening-range variant** (DRAFT-p2-decisions-4). If any sibling repository
   holds an ETF minute-bar substrate, the variant this repository culled on cost grounds is the
   cheaper-to-execute one by the ratios recomputed above, and the cull is worth re-examining
   house-wide rather than only here.

---

## What I checked and found sound

Everything below is where the "closed too early" thesis did **not** hold. In several of these the
repository does the opposite of premature closure.

**The power arithmetic reproduces exactly.** Using `annualize`: `t = (SR/√252)·√n`, one-sided normal
power. At α = 0.05: E1 = **0.999835 / 0.832450 / 0.366747** at 2.81 / 1.40 / 0.70 on n = 875, and
**1.000000 / 0.980162 / 0.581652** on n = 1,762 — every cell matches README.md:403-405 to six
decimals. At the superseded α = 0.02532057: **0.999484 / 0.743521 / 0.257802** — matches
README.md:392-394 and reports/stage_a2/power.md:12-20. Minimum n for 80 percent: **794.90 → 795**
and **1005.22 → 1,006** — matches README.md:404 and README.md:393. The Berger (1982)
intersection-union argument at DECISIONS.md:1146-1153 is correct as stated, and correcting it moved
E1 **up**, against the repository's own interest in a clean null.

**The E2 and joint-power collapse reproduces exactly, in both directions.** With the carried band:
pessimistic mean 0.040386 − 0.041455 = **−0.001069**, effect −5.266e−04 per share against σ =
2.029585, N = 875 × 19.64 = 17,185 trades, t = −0.069036, power **0.043275** (document 0.043277,
README.md:265). With the measured band: **−0.426679**, t = −27.56, power **0.000000**
(README.md:306). At the published 2.81 under the carried band, **0.819458** (document 0.819524,
README.md:266) — so the closure genuinely would have been conditional on the halving heuristic under
the old band and genuinely is not under the new one. Amendment 28 §3 (REGISTRATION.md:4102-4122)
records that correction against the operator's own expectation, which is the opposite of motivated
reasoning.

**The shift decomposition reproduces to 1e-6 for both bands.** Carried **0.041455**, measured
**0.467066** (documents 0.041455 and 0.467065). Break-even Sharpe from the carried shift =
0.041455/0.02884727 = **1.437051** (document 1.437035, README.md:272); the registered 1.40 sits
**2.5772 percent** below it (document 2.577, README.md:273); break-even stop share **0.346206**
(document 0.346206, README.md:274); the `GO` ruling-out multiple 0.041455/0.001893 = **21.899**
(document 21.89, DECISIONS.md:1354-1356). Rule of three 3/560 = **0.005357** (document 0.005357,
README.md:261).

**The pre-commitment claim is true and I verified it the way the repository invites.**
DECISIONS.md:1343-1345 says the criterion "precedes the commit containing `tools/slippage_band.py`,
and **the ordering is checkable in `git log` by anyone who doubts it**." It is:
`4ae14dc` 20:13:26 → `5899e1b` 20:41:12 → `7edeea7` 20:41:59 → `34a91b3` 20:43:15, all 2026-08-29
−0700. The criterion, its two tiers and the arithmetic ruling out `GO` were all fixed before the
number existed.

**I tried three ways to break the closure and could not.**
(a) *Should the measured band also raise the dispersion, and so the implied central mean?* μ ∝ σ, so
a larger σ helps H1 — but flipping the sign needs σ ≥ 0.467065·√(252·19.64)/1.40 = **23.5 USD/share**
against the measured 2.029585, an 11.6× increase. Adding an independent cost component of standard
deviation ≈ 0.2 to a PnL of σ = 2.03 moves σ by about 0.5 percent. No rescue.
(b) *Is the median the right central end for a test about a mean?* The artifact holds the means:
entry 0.145915, stop 0.080212, close 0.099324 (reports/stage_a3rescue/task2_slippage_band.json:66,
88, 94, 109). Reassigning mean→central gives shift = 0.208730 + 0.381818·0.117849 + 0.618182·0.161676
= **0.353682**, still **8.76×** the central mean. No rescue. ADR-038:1439-1445 registered the
median→central assignment before computing, and rejecting the mean because it "would be dragged by
the gap-through tail" is a defensible, pre-committed choice.
(c) *Does the "lower bound" robustness claim cover the whole band?* Strictly, no — it covers the
overshoot (457/550 entry and 195/210 stop triggers crossed intrabar and were recorded at 0.0 —
task2_slippage_band.json:80,101) and market impact, but the quoted half spread is a point estimate
from one 2-month regime carrying Amendment 11's explicit "either direction, unbounded" caveat, and
that half spread is 55.0 percent of the shift. **It does not matter**: the closure survives an
11.57× overstatement of the entire shift, so I record this as checked and not a finding.

**Decisions that were correctly revisited when their trigger was met** — the exact behaviour my
thesis looks for and does not find here. ADR-007 deferred vendor selection "when a credential
exists, in its own dated ADR" (DECISIONS.md:204) and ADR-023 delivered it (DECISIONS.md:672-732),
reversing the `docs/ACCESS.md` recommendation on measurement and leaving the falsified section
visible with a falsification table (docs/ACCESS.md:567-577). ADR-012's one-sided carve-out was
falsified by measurement (n = 2 credentials, 0 serving) and amended two-sided by ADR-027, with the
direction of the compromise registered rather than argued away (DECISIONS.md:872-880). ADR-026
recorded Alpaca's ceiling as `None` and rejected escalating; when the premise changed (Alpaca became
primary, plus an operator instruction) ADR-030 superseded **that single rejected alternative and
nothing else** (DECISIONS.md:1004-1010). ADR-030 also records that it falsified its own earlier
134.05/min figure in passing (DECISIONS.md:1058-1060).

**Refusals to close on absent evidence.** ADR-017 registered `PENDING_ACCESS` specifically so that
BLOCKED would not "record a source-integrity death this repository did not measure"
(DECISIONS.md:469-471), and README.md:79-81 keeps `PENDING_REVISION` explicitly out of the
`source-integrity-blocked` closure kind. ADR-035 reports a zero count with its rule-of-three bound
rather than as a certainty (DECISIONS.md:1299-1305). ADR-026 records an unreached ceiling as absent
rather than as a large number. `reports/stage_a2/calendar.md:80-96` records the second-source
calendar cross-check as "**not completed, and not fabricated**" rather than filling it from
recollection. `reports/stage_a2/power.md:52-63` records two one-session disagreements with the
operator prompt and lets the computation win.

**Structural gates that can genuinely fail a real effect** — ADR-006's concentration and persistence
gates, pinned by `test_all_four_conditions_are_required` so no gate can quietly become advisory
(DECISIONS.md:172-177), with the cost registered as intended rather than hidden.

**The H1b registration paid its multiplicity cost rather than avoiding it** — trial count 8 → 9 for
H1b, with the reason stated ("the ninth trial exists the moment the alternative is written down",
DECISIONS.md:1407-1409), and the floor deliberately left unchosen so it is not fitted to the scan
that motivated it. The scan's "sessions filling 20" column is correctly disclaimed as a scan-sample
artefact (README.md:337-342; docs/HANDOVER.md:120-122) — the opposite of over-reading a thin sample.

**The parked entries were handled correctly when their parking condition expired.** H2 and H3 were
parked because "no second repository opens while H1 is unresolved"; H1's closure met that trigger and
`HYPOTHESES.md:140-144` says so explicitly while refusing to treat the met condition as an opening
(other reader's primary document; recorded here for the ledger only).

**Blockers I checked for expiry and found still live at the anchor.** The 2026-09-12 re-pull date
(README.md:77; docs/HANDOVER.md:8-11) had not been reached at the anchor and had still not been
reached at my read time (2026-09-04 UTC). The SEC Section 31 effective date is genuinely unmeasured
(`sec.gov` 403 on n = 4 across two sessions, DECISIONS.md:1081-1083), but ADR-031's bracket shows it
does not move the figure it feeds — "**The bracket came out 0.0084 percent wide**"
(DECISIONS.md:1101-1103), which I confirmed is consistent with the reported relative width
8.43 × 10⁻⁵ (README.md:222). It is not a live blocker on anything.

---

## Live-repo access log

Purpose of access: (1) `git log` / `rev-parse` to verify the ADR-036 pre-commitment ordering and to
confirm no commits exist after the anchored SHA; (2) `git ls-tree` and a directory listing under
`reports/` to establish which rescue-pass artifacts are tracked. No file was opened for writing; no
`.env`, keystore, session or credential file was read (`.env` was seen only as a name in
`git status --ignored` output and was not opened).

    $ git -C /home/kiros-li/Documents/GitHub/ORBExperiment status --porcelain    # BEFORE
    (no output — clean tree)

    $ git -C /home/kiros-li/Documents/GitHub/ORBExperiment status --porcelain    # AFTER
    (no output — clean tree)

`git rev-parse HEAD` = `f2aa675a80fc06b74979040b3028154d1add5ec0` before and after, identical to the
anchored SHA; `git log f2aa675..HEAD` is empty. Unanchored reads: none — every report artifact I
opened is tracked at the anchor and was read from
`/home/kiros-li/.cache/program-audit/scratchpad/snap/ORBExperiment/`. The only live-tree read was the
directory listing of `reports/stage_a3rescue/` (2026-09-04 ~14:00 UTC), used solely to confirm
tracked status; its contents were then read from the snapshot.

Scratch work: `/home/kiros-li/.cache/program-audit/scratchpad/work/agentA-ORB-p2/recompute.py`.
