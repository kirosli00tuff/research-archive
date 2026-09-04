# HFExperiment — Agent C (referee / verifier), consolidated findings

Repository: HFExperiment
Anchored SHA: `82e77a021256d917c665ff6d4304c25b08f35451` (main, 2026-08-28; also live `HEAD`)
Sources consolidated: `findings/agentC/verification/HFExperiment.inventory.md` / `.json`,
`findings/agentC/verification/HFExperiment.verification.md` / `.claims.json`,
`findings/agentC/provenance/HFExperiment.md` / `.json`.
Every quote and every figure in this file was re-checked against
SNAP/HFExperiment before publication. Prepared 2026-09-04 UTC.

## Summary

The computational spine of this repository verifies exactly: the 4.07 bp/day cost hurdle, the
213.84 bp round trip, the 28.76 / 56.84 annual drag, the frozen rho 0.071641, the day-2061 /
day-2852 projection, the two-point power law and every interpolated cell, all 21 median-share-price
cells, the spread quantiles, the price-reconciliation ratios, the churn means and every C.1 ledger
count reproduce from stored primitives to the last printed digit, and the Section 0 BLOCKED closure
is fully supported by its own evidence ledger.
What does not verify is stated arithmetic and record-keeping, never a result: four figures in the
sentence that closes the DEGRADED branch are contradicted by the formations file the same paragraph
cites (all in the direction that makes the closure *stronger*), the kill-floor loss figure cannot be
reconciled with its own sigma, and the Gateway server version in five prose retellings of the
deciding session is 187 where that session's ledger says 178.
What could not be checked is the largest dependency in the repository: 27.99 bp/day, 66.40 %/yr and
IR 1.062 exist here only as literals, with no n, no window and no standard error stated anywhere,
and are verifiable only across the AiTrader boundary this task does not cross.
No thesis is asserted either way: there is no realized interval, no test statistic and no p-value in
this repository, because the shadow series produced zero observations and the repository says so in
its own monitor output.

## Verification scoreboard

### Claims

| status | count |
|---|---|
| VERIFIED | 20 |
| CONTRADICTED | 7 |
| UNVERIFIABLE | 3 |
| **total claim rows audited** | **30** |

Counting convention: 30 is the granular row count (`HFExperiment.claims.json`, `kind == "claim"`),
in which the compound claims C4 and C5 are split into their independently checkable parts. Rolled up
to the 24 inventory claim numbers C1–C24, the same result reads 16 VERIFIED / 4 CONTRADICTED /
4 UNVERIFIABLE. Alongside these, 23 derived quantities (19 agree, 4 disagree) were recomputed by me
from stored primitives and taken from no document.

### MUST-VERIFY claims (inventory rank 1–7)

| claim | subject | status |
|---|---|---|
| C1 | Section 0 closure verdict, BLOCKED on the A.1b order behaviour | **VERIFIED** — every element of the verdict sentence is present in `reports/stage_a1b/evidence.jsonl` (51 rows): 5 orders of a 10 cap, 3 × error 10243, 1 × error 10244, whole-share control accepted, 20 contracts at MinSize/SizeIncrement 0.0001 |
| C2 | registered cost hurdle 4.07 bp/day | **VERIFIED** — recomputed 4.073081 from `book_spreads.json` medians through `costmodel.py` + `commission.py` (tol 0.005, the repository's own pinning tolerance) |
| C3 | holdout effect 27.99 bp/day, IR 1.062, and the primary-width choice | **UNVERIFIABLE** — no artifact in this repository holds these; n, window and SE are stated nowhere; declared origin is the AiTrader round of 2026-07-26, outside this task. Their *mutual* consistency does verify exactly |
| C4 | the DEGRADED closure arithmetic (2,880 / 720 / "36 in March and April" / "22 to 1,595") | **CONTRADICTED** on four of five parts → AUDIT-C-HFExperiment-1 (C4a, the 144 USD medians, VERIFIED) |
| C5 | kill-floor sigma and touch probability | **CONTRADICTED** on the loss figure → AUDIT-C-HFExperiment-5 (C5b, the 30 % / 7-point neighbours, VERIFIED) |
| C6 | Gateway server version, prose vs ledger | **CONTRADICTED** → AUDIT-C-HFExperiment-3 |
| C7 | measured spread distribution (median 12.77, p75 17.2, p90 20.7, max 27.4) | **VERIFIED** — all four reproduce exactly from 20 per-name medians over 180 cells under the lower-order-statistic quantile convention |

### Intervals audited

| metric | value |
|---|---|
| intervals audited | 14 (I1–I14) |
| independence doubtful | 2 |
| recomputed | 8 |
| conclusion moved by recomputation | 0 |

Estimator / independence summary. **There is not one realized interval in this repository.**
`reports/monitor/verdict.txt:5-6,14-15,23-24` prints `observations: 0` and `bounds: none, the series
has not started` at all three widths, so every row is a construction or a planning projection
evaluated at n = 0. The single estimator is a studentized asymptotic confidence sequence
(`verdict.py:8-16, 26-34`), radius `σ̂_t · √( 2(tρ²+1)/(t²ρ²) · ln( √(tρ²+1)/α ) )` — the
Waudby-Smith–Ramdas boundary, cited to no source in the repository. Its independence assumption
(I1) is doubtful in structure: had it run it would face a serially correlated, volatility-clustered
daily series, and the three widths are nested by construction (the width-5 book is the first five
names of the width-20 book, `cost_table_a2.py:35-36`), so the three sequences would be heavily
mutually dependent; multiplicity is handled by a Bonferroni split rather than any dependence model.
I5, I6, I8 and I9 are rules and projections that consume I1's radius and inherit that assumption.
The second doubtful assumption is I10, which treats the width-20 *tracking error* as the
equity-drawdown σ under driftless Brownian motion — the beta approximation is **disclosed** at
REGISTRATION.md:222-224. I13 correctly notes its 180 spread cells are 3 sessions × 3 windows within
name and therefore not independent, but claims no interval on them. Because no interval was ever
evaluated on data, no independence assumption was ever *exercised*, and I make no claim that any
stated comparison would move.

### Tests audited

| metric | value |
|---|---|
| tests / decision rules audited | 6 (T1–T6) |
| tail mismatches | 0 |
| dof issues | 0 |
| correction mismatches | 0 |

Tail / dof / correction summary. **There is no hypothesis test and no p-value in this repository.**
T1 (success: lower bound > 4.07) and T2 (futility: upper bound < 10) are one-sided in the direction
the registration states ("earn **positive** daily excess return", REGISTRATION.md:47-53); the
estimator is asymptotic with no dof parameter, α entering only through `ln(√(tρ²+1)/α)`. Two things
are flagged and deliberately not raised as findings. (i) The WSR radius is normally stated as a
two-sided (1−α) sequence; used one-sidedly at the same α it is conservative, never
anti-conservative, and the repository cites no source, so the intended convention cannot be settled
from this repository alone. `verdict.py:74-77` **discloses** the two-bound reading exactly ("Each
side holds at level alpha one-sided, which is how both the success rule and the futility rule read
it"). (ii) T3's Bonferroni split (0.05 primary, 0.025 + 0.025 secondaries) is the correct family for
a union rule and is arithmetically exact for the scope the code states; the union bound over all
three widths is nevertheless 0.10. Zero alpha was ever spent. T5 and T6 are exact-equality and
pass/fail conjunctions, correctly not dressed as statistical tests and correctly uncorrected.

### Provenance

| status | count |
|---|---|
| SUPPORTED | 30 |
| NOT_SUPPORTED | 2 |
| PARTIAL | 4 |
| UNVERIFIABLE | 1 |
| **total** | **37** |

Composition: 22 registration claims (15 SUPPORTED, 4 PARTIAL, 2 NOT_SUPPORTED, 1 UNVERIFIABLE) and
15 registered parameters / bars / rules (15 SUPPORTED, none changed after data existed). The
headline provenance result is positive and worth stating plainly: **no registered bar, parameter,
outcome map, prior or decision rule in this repository was ever edited after it was committed.** A
complete deletion census over all 13 commits returns four rows in the entire history, none of them a
registered value; `src/hfexperiment/registered.py` appears in exactly two commits, both pure
additions. The Section 0 outcome map is byte-identical at the root commit `c4e9817`
(2026-08-23T22:23:16Z, no parents) and at the anchor, and the bar that fired BLOCKED was fixed 19
min 18 s before `docs/ACCESS.md` existed and two days before the deciding fractional measurement.

## Findings

9 findings, in descending severity. 10 drafts entered consolidation; 0 were dropped for want of a
locatable quote and figure; 2 were merged (see "Merges and drops" below). Direction is recorded as
"neutral" where neither A (closed too early) nor B (claimed too much) applies — Agent C carries no
thesis, and none of these findings supports one.

---

### AUDIT-C-HFExperiment-1

- **Repository / SHA:** HFExperiment / 82e77a021256d917c665ff6d4304c25b08f35451
- **Hypothesis or artifact:** REGISTRATION.md Section 6, "The DEGRADED branch, closed" — the arithmetic that closes a pre-registered Section 0 branch
- **Direction:** neutral — every error runs in the direction that makes the DEGRADED branch *less* affordable than the document states, so the registered consequence ("NO live sleeve at this stake") holds a fortiori. The defect is in the stated arithmetic of a binding registration, not in its conclusion
- **Class:** ARITHMETIC
- **Severity:** S2 — a stated figure contradicts the artifact the same paragraph cites
- **Label:** DERIVED
- **Claim challenged (verbatim):** "A.1 measured it: 144 USD at the last two formations, up from 36 in March and April. At 144, whole-share sizing on 900 USD cannot fill a 20-name book at all, because 20 names at one share each already cost about 2,880 USD. A 5-name book gets one share per name, 720 of 900 deployed, with equal weighting destroyed by per-name prices from 22 to 1,595 USD." — HFExperiment/REGISTRATION.md:149-154 (restated at HFExperiment/DECISIONS.md:194-199, ADR-012)
- **Evidence:**
  - The stored 2026-07-01 width-20 book, n = 20, `last_close` in HFExperiment/reports/stage_a1/formations.json (`formations` → `2026-07-01` → `20`): one share of each costs **7,890.47 USD**, not "about 2,880 USD". 2,880 is 20 × the median (143.89), which is not the cost of the book.
  - The stored 2026-07-01 width-5 book, n = 5 (WOLF 48.25, AXTI 72.08, SNDK 2,273.73, BE 302.70, LITE 858.06), same file: one share of each costs **3,554.82 USD**, not "720 of 900 deployed". **SNDK alone at 2,273.73 exceeds the entire 900 USD deployed**, so "one share per name" is not purchasable at this stake at all. The width-5 book's own median close is 302.70 (`median_price` → `2026-07-01` → `5`), not the 144 the sentence applies to it.
  - "up from 36 in March and April": stored width-20 medians are March **36.47** and April **40.59** (formations.json `median_price`; rendered at HFExperiment/reports/stage_a1/formations.md:24-25). April is not 36.
  - "per-name prices from 22 to 1,595 USD": no stored price set in this repository has a minimum near 22. 1,595.19 and 22.305 are SNDK's and PL's A.2 median mids (HFExperiment/reports/stage_a2/book_spreads.json:33, :51), but the minimum of that same 20-name set is ONDS at 8.745 (:75), with WULF 15.71 (:111) and CIFR 15.845 (:129) also below 22 — and PL is not in the width-5 book the sentence is about. On the July closes the width-5 range is 48.25 to 2,273.73 and the width-20 range is 8.24 to 2,273.73.
  - What does verify in the same sentence: 143.80 (2026-06-01) and 143.89 (2026-07-01) at the last two formations, and all 21 cells of the median-share-price table, reproduced from the stored `last_close` values with **0 mismatches**.
- **Recomputation:** inputs `HFExperiment/reports/stage_a1/formations.json` (`formations.2026-07-01.{5,20}[].last_close`, n = 5 and n = 20) and `HFExperiment/reports/stage_a2/book_spreads.json` (`per_name.*.median_mid`, n = 20). Method: direct sum, min, max, median with Python `statistics`, no rounding before comparison. Results: Σ width-20 = 7,890.47; Σ width-5 = 3,554.82; max width-5 close 2,273.73; min width-20 close 8.24; min width-20 mid 8.745; April width-20 median 40.59. Tolerance 0.01 USD. Re-executed independently at consolidation against SNAP with identical results.
- **What would resolve it:** restating Section 6's arithmetic on the actual per-name closes (which strengthens the closure — the 20-name book costs 2.7× and the 5-name book 4.9× what the document states), or an explicit sentence saying 2,880 and 720 are median-times-count illustrations rather than book costs; plus naming the source of the "22 to 1,595" range.
- **Confidence:** HIGH — the contradicting values are the stored per-name closes in the very file Section 6's measurement is drawn from, and the arithmetic is a sum.
- **Invalidated by later commits?:** no — the repository is closed and terminal (REGISTRATION.md:306-315), HEAD is the anchored SHA, and formations.json has not been touched since `0a0d214`/`91a1dcb`.
- **Disclosed by authors?:** no. Section 6 and ADR-012 both present the 2,880 / 720 arithmetic as measurement. The one adjacent disclosure is the same sentence's "equal weighting destroyed by per-name prices", which acknowledges dispersion without correcting the figures beside it.

---

### AUDIT-C-HFExperiment-2

- **Repository / SHA:** HFExperiment / 82e77a021256d917c665ff6d4304c25b08f35451
- **Hypothesis or artifact:** the terminal closure record — REGISTRATION.md amendment log and progress.md
- **Direction:** A
- **Class:** PROVENANCE
- **Severity:** S3
- **Label:** DERIVED
- **Claim challenged (verbatim):** "Experiment closed by operator decision, instruction dated 2026-08-26." — HFExperiment/REGISTRATION.md:308 (identically at HFExperiment/progress.md:7-8: "Closed. Experiment closed by operator decision, instruction dated / 2026-08-26.")
- **Evidence:** Both sentences, and both headings "### 2026-08-26: Closure" (REGISTRATION.md:306) and "## 2026-08-26: Closure" (progress.md:5), were introduced by exactly one commit, `f13e1d3` (`git log -S"2026-08-26: Closure" -- progress.md` and `git show f13e1d3 -- REGISTRATION.md`, each returning only `f13e1d3`). `f13e1d3`'s author date **and** committer date are both **2026-08-25T07:45:29Z** (2026-08-25T00:45:29−07:00 local). The record of an instruction dated 2026-08-26 therefore exists in the object store roughly 16 h 14 m before the earliest instant of 2026-08-26 UTC, and no timezone on earth (max UTC+14) places that commit on 2026-08-26. The repository's other amendment entries are dated consistently with their commits under one convention or the other — acceptance "2026-08-24" / `8c4c3bc` 2026-08-25T00:36:21Z (local date), verdict "2026-08-25" / `669eb5c` 2026-08-25T03:09:06Z (UTC date) — so the closure entry is the only one matching neither. `git grep -n "2026-08-26" 82e77a0` returns only these four closure lines plus an unrelated fixture at tests/test_spendledger.py:42; no operator artifact bearing that date exists in the tree. The later commit `82e77a0` (2026-08-28T21:14:08Z), a record-hygiene commit made with the operator present (DECISIONS.md:445-448), did not correct it, so the discrepancy stands at the anchor.
- **Recomputation:** none required; date arithmetic only. `f13e1d3` = 2026-08-25T07:45:29Z; stated instruction date 2026-08-26; difference ≥ 16 h 14 m in the wrong direction.
- **What would resolve it:** an operator-authored artifact dated 2026-08-26 that the closure entry records, or a corrected amendment stating the true instruction date and why the entry was written a day early. The *substance* of the closure verifies independently — the timer is disabled and inactive, and no shadow row ever existed — so only the dating is in question.
- **Confidence:** HIGH — the commit's author and committer dates agree and the introducing commit is unambiguous.
- **Invalidated by later commits?:** no — `82e77a0` is the anchor and the live HEAD, and it left the text unchanged. A future commit could add a correcting amendment.
- **Disclosed by authors?:** no — nothing in REGISTRATION.md, progress.md or DECISIONS.md mentions the gap between the entry's date and the commit that carries it.

---

### AUDIT-C-HFExperiment-3

- **Repository / SHA:** HFExperiment / 82e77a021256d917c665ff6d4304c25b08f35451
- **Hypothesis or artifact:** the Stage A.1b session descriptor — the provenance of the session that fired Section 0's BLOCKED verdict
- **Direction:** neutral — pure provenance hygiene. The BLOCKED verdict itself is fully supported (claim C1 VERIFIED); no registered number depends on the Gateway's server version
- **Class:** PROVENANCE
- **Severity:** S3
- **Label:** DERIVED
- **Claim challenged (verbatim):** "Run 2026-08-25, 02:57 to 03:07 UTC, Monday 22:57 to 23:07 ET, market closed. Gateway 127.0.0.1:4002, server version 187, account [paper account ID removed], declared mode paper." — HFExperiment/reports/stage_a1b/a1b_report.md:3-4. The server-version figure is repeated at HFExperiment/DECISIONS.md:408 (ADR-022, "A.1b resolved it by behaviour on 2026-08-25, paper account [paper account ID removed], Gateway server version 187."), HFExperiment/DECISIONS.md:441 (ADR-026), HFExperiment/docs/ACCESS.md:178 and HFExperiment/progress.md:235
- **Evidence:**
  - The A.1b session's own primary record, row 2 of HFExperiment/reports/stage_a1b/evidence.jsonl, verbatim: `{"kind":"connected","managed":["[paper account ID removed]"],"server_version":178,"utc":"2026-08-25T03:05:16.497779Z"}` — **178, not 187**. n = 1 connection record, and it is the only one in the file; I parsed all 51 rows (1 `stage_start`, 1 `connected`, 20 `contract_details`, 10 `api_error`, 2 `quote_snapshot`, 2 `quantity_computed`, 5 `order_request`, 5 `order_outcome`, 1 `fills`, 2 `final_positions`, 1 `orders_placed_total`, 1 `cancel`) and no record anywhere in the file contains 187.
  - The value is machine-captured: `HFExperiment/scripts/a1b_capability_test.py:158` writes `server_version=self.ib.client.serverVersion()`, and that script writes only the `.jsonl`; the `.md` report is hand-written prose. ADR-022 introduces 187 in the sentence immediately before it says "Observed, verbatim in reports/stage_a1b/evidence.jsonl" (DECISIONS.md:410).
  - **187 is a real observed value, but from a different session:** the C.1 read-only probe records `"server_version": 187` at HFExperiment/reports/stage_c1/refusals.md:332, in a probe record whose `server_time_epoch` 1787625630 decodes to 2026-08-25T02:40:30Z — 25 minutes earlier, committed in `b4a7a23`, one commit before A.1b. Five prose retellings therefore attribute the C.1 probe's version to the A.1b session, and the `82e77a0` correction commit propagated it into two further documents without checking it against the ledger it cites.
  - Everything else in the descriptor checks out against the ledger: account [paper account ID removed] (`stage_start`, `connected`, `final_positions`) and declared mode paper (`stage_start`).
- **Recomputation:** none required — a direct read of a stored JSONL field against five prose statements; all 51 records parsed from SNAP/HFExperiment/reports/stage_a1b/evidence.jsonl and re-checked at consolidation.
- **What would resolve it:** the raw session log showing the Gateway's reported API server version at 03:05:16Z, or an appended note in ADR-022 / the A.1b report recording that the A.1b connection reported 178 and that 187 comes from the C.1 probe — or, if the 178 is a capture bug in `scripts/a1b_capability_test.py`, a note saying so. The substantive verdict is unaffected: the same ledger corroborates 3 × error 10243 on decimal quantities, 1 × error 10244 on cashQty, and a whole-share control `PreSubmitted`.
- **Confidence:** HIGH — the ledger field is unambiguous and singular, and the divergent 187 is traceable to a different, timestamped record.
- **Invalidated by later commits?:** no — evidence.jsonl landed at `669eb5c` and the last prose repetition landed at the anchor `82e77a0`, which re-propagated the figure rather than correcting it; the repository is closed.
- **Disclosed by authors?:** no. ADR-026 (DECISIONS.md:432-454) is precisely a self-reported record-hygiene correction about A.1b's provenance, and it repeats "server version 187" at :439 without noticing the ledger says 178.

---

### AUDIT-C-HFExperiment-4

- **Repository / SHA:** HFExperiment / 82e77a021256d917c665ff6d4304c25b08f35451
- **Hypothesis or artifact:** the ADR-026 correction note in docs/ACCESS.md Task 3 — its session window and its sub-test count
- **Direction:** B
- **Class:** PROVENANCE
- **Severity:** S4
- **Label:** DERIVED
- **Claim challenged (verbatim):** "Stage A.1b connected on **2026-08-25, 02:57 to / 03:07 UTC, to Gateway 127.0.0.1:4002, server version 187, account / [paper account ID removed], declared mode paper**, and settled four of the six sub-tests by / behaviour (`reports/stage_a1b/a1b_report.md`)." — HFExperiment/docs/ACCESS.md:177-180
- **Evidence:** Two components of this sentence are contradicted by the artifacts it cites; the third (server version 187) is AUDIT-C-HFExperiment-3 and is not re-counted here.
  - **(i) Window.** `HFExperiment/reports/stage_a1b/evidence.jsonl` spans `2026-08-25T03:05:15.955248Z` (`stage_start`) to `2026-08-25T03:07:17.172526Z` (`final_positions`), n = 51 records; the sole `connected` record is at `03:05:16.497779Z`. The claimed connection window 02:57–03:07 UTC is ten minutes; the ledger's span is 2 minutes 1 second, and no record precedes 03:05:15.955Z.
  - **(ii) Count.** `git show 82e77a0 -- docs/ACCESS.md` deletes the original six-row sub-test table and adds a **seven**-row table (HFExperiment/docs/ACCESS.md:192-200). The added seventh row is `| whole-share control order | **RESOLVED — ACCEPTED** | …`, which was not among the six sub-tests the same paragraph refers to and which ADR-026 itself lists separately in "four RESOLVED, two MOOT, one RUNNABLE" (DECISIONS.md:452 — 4+2+1 = 7). Of the *original six* rows, three are RESOLVED (decimal totalQuantity, cashQty, MinSize/SizeIncrement), two MOOT and one RUNNABLE. "Four of the six" counts a row created by the correction itself among the six it corrects.
- **Recomputation:** min/max of the 51 `utc` fields in `reports/stage_a1b/evidence.jsonl`: 03:05:15.955248Z / 03:07:17.172526Z, span 121.2 s. Row census from the `82e77a0` diff and from the anchored file: 6 removed, 7 added, statuses 4 RESOLVED / 2 MOOT / 1 RUNNABLE — re-counted directly in SNAP at consolidation.
- **What would resolve it:** the session wall-clock log covering 02:57–03:05:15Z (setup, or a first connection attempt, would explain the window), and either a re-count to "three of the six, plus a control the correction adds" or a note that the table gained a row.
- **Confidence:** HIGH for the count (arithmetic on the commit's own diff and on the anchored table); MEDIUM for the window (a stage may begin before its ledger's first write, though "connected on … 02:57 to 03:07 UTC" is specifically a connection claim).
- **Invalidated by later commits?:** no — `82e77a0` is the anchor and the live HEAD.
- **Disclosed by authors?:** partly. ADR-026's own status breakdown at HFExperiment/DECISIONS.md:452 sums to seven, which discloses that the table grew; no document reconciles that with "four of the six", and nothing discloses the window discrepancy. Held at S4.

---

### AUDIT-C-HFExperiment-5

- **Repository / SHA:** HFExperiment / 82e77a021256d917c665ff6d4304c25b08f35451
- **Hypothesis or artifact:** REGISTRATION.md Section 9, the registered restart floor and its touch-probability justification
- **Direction:** neutral — hygiene inside a registered kill criterion. The registered *level* (500 USD) and its 1.31 σ / 19 % justification are correct; only the descriptive loss figure attached to them is not, and no capital was ever deployed (REGISTRATION.md:308-309)
- **Class:** ARITHMETIC
- **Severity:** S4
- **Label:** DERIVED
- **Claim challenged (verbatim):** "The floor is 500 USD of total account equity, a 400 USD loss on 900 deployed after the 100 buffer, 1.31 sigma of the width-20 tracking error, driftless touch probability near 19 percent in year one." — HFExperiment/REGISTRATION.md:216-218
- **Evidence:**
  - σ used throughout Section 9 and ADR-011 is 900 USD × TE(20). TE(20) = 42.544 %/yr from the two-point power law (REGISTRATION.md:117; exponent reproduced as −0.32113 from the recorded widths 5 and 50), giving σ = **382.90 USD** (900 × the rounded 42.54 % gives 382.86; the difference is immaterial to every figure below).
  - A **400 USD** loss is 400/382.90 = **1.045 σ**, touch 2Φ(−1.045) = **29.6 %** — not 1.31 σ and not 19 %.
  - The stated 1.31 σ and 19 % require a **500 USD** loss: 500/382.90 = **1.306 σ**, 2Φ(−1.306) = **19.16 %**. That is exactly (1000 total equity − 500 floor), the basis ADR-011 uses for all three of its numbers.
  - ADR-011 is internally consistent on that basis and never states a loss figure: "600 is 1.04 sigma … near 30 percent … 500 is 1.31 sigma, near 19 percent. 400 is 1.57 sigma, near 12 percent" (HFExperiment/DECISIONS.md:173-179). I reproduce 1.045 σ / 29.6 %, 1.306 σ / 19.16 %, 1.567 σ / 11.71 %, and the "7 more points" of REGISTRATION.md:220-221 as 19.16 − 11.71 = 7.4. n = 0 observations; these are design projections.
  - Under the alternative reading — that the 100 buffer is consumed first, so the sleeve starts at 900 and 900 → 500 is a 400 loss — the touch probability would be 29.6 %, again not the 19 % stated in the same sentence. **Neither reading makes all three of (400 loss, 1.31 σ, 19 %) true.**
- **Recomputation:** inputs TE(20) = 42.544 %/yr (from the fit at DECISIONS.md:143-147, tabulated at REGISTRATION.md:117), deployed 900 USD (REGISTRATION.md:133). Method: σ = 900 × TE; k = loss/σ; touch = 2Φ(−k) with `scipy.stats.norm`. Tolerance 0.01 σ and 0.5 percentage points. Re-executed independently at consolidation: 1.0447 / 29.62 %, 1.3058 / 19.16 %, 1.5670 / 11.71 %.
- **What would resolve it:** replacing "a 400 USD loss on 900 deployed after the 100 buffer" with "a 500 USD loss of total equity, leaving 400 in the sleeve", which is what the 1.31 σ and the 19 % already encode. Nothing else in Section 9 or ADR-011 moves.
- **Confidence:** HIGH on the arithmetic — the three figures cannot be simultaneously true under either reading. MEDIUM on materiality: this most likely reads as "down to 400" rather than "a 400 loss", and the operative registered number (500) and its justification are correct.
- **Invalidated by later commits?:** no — closed repository, HEAD is the anchored SHA, and REGISTRATION.md is append-only with the Section 9 text landed at `a8f4b0d` and never edited.
- **Disclosed by authors?:** no for the arithmetic. The authors *do* disclose the surrounding modelling limits at REGISTRATION.md:222-224 ("The figures ignore market beta, which the high-beta book makes optimistic, and ignore positive drift"), and ADR-011 offers "a measured book beta would refine the touch probabilities" (DECISIONS.md:188) — neither touches the loss figure.

---

### AUDIT-C-HFExperiment-6

- **Repository / SHA:** HFExperiment / 82e77a021256d917c665ff6d4304c25b08f35451
- **Hypothesis or artifact:** the ADR-026 record-hygiene correction, commit `82e77a0`
- **Direction:** B
- **Class:** PROVENANCE
- **Severity:** S4
- **Label:** DERIVED
- **Claim challenged (verbatim):** "Decided. ACCESS.md Task 3 is re-headed SUPERSEDED, the false sentence is / struck rather than deleted, and the sub-test table is re-statused against / the A.1b evidence: four RESOLVED, two MOOT, one RUNNABLE. ADR-003 keeps / its original text with a superseded note beneath it. Nothing is rewritten / to look as though it was always right." — HFExperiment/DECISIONS.md:450-454
- **Evidence:** `git show 82e77a0 -- docs/ACCESS.md` is `+47/−19`. The struck sentence is genuinely struck (HFExperiment/docs/ACCESS.md:184-187, `~~…~~`), and ADR-003 is genuinely additive (DECISIONS.md `+60/−0`). But the same diff **deletes without trace** the paragraph that closed Task 3 — the one containing the repository's own prediction that A.1b falsified:

  ```
  -The documentation conflict stands unresolved on purpose: IBKR staff wrote
  -in June 2026 that the API does not support cash-quantity orders outside
  -crypto, a third-party guide from March 2026 claims the opposite, and an
  -Elite Trader thread reports cashQty rounding down to whole shares through
  -the Web API. The likely resolution is that cashQty is unsupported while
  -decimal share quantities work, which the quote-first-divide-then-submit
  -path handles. Likely is not measured. The verdict waits for the test.
  ```

  It was replaced by a rewritten paragraph in resolved-past tense ("The documentation conflict, for the record, is now resolved rather than open …"). `grep -rn "quote-first-divide-then-submit\|Likely is not measured\|verdict waits for the test\|stands unresolved on purpose"` over the whole anchored tree returns **nothing**: the falsified prediction survives only in the git object store. The asymmetry is the point — the merely *stale* sentence about account access is preserved struck, while the *wrong* forecast ("decimal share quantities work", refuted by three error-10243 refusals) is removed. ADR-026's own enumeration of what it changed does not mention this deletion.
- **Recomputation:** n/a — diff and grep only.
- **What would resolve it:** restoring the deleted paragraph struck through, as the adjacent sentence was, or an amendment noting that Task 3's closing paragraph was replaced and why.
- **Confidence:** MEDIUM — the deletion is certain; whether it amounts to "rewritten to look as though it was always right" is a judgement, and the replacement text does date the resolution honestly to 2026-08-25.
- **Invalidated by later commits?:** no — `82e77a0` is the anchor and the live HEAD.
- **Disclosed by authors?:** partly — ADR-026 discloses that the table was "re-statused" (DECISIONS.md:450-452), but no document records that a paragraph containing a falsified prediction was deleted rather than struck. Held at S4.

---

### AUDIT-C-HFExperiment-7

- **Repository / SHA:** HFExperiment / 82e77a021256d917c665ff6d4304c25b08f35451
- **Hypothesis or artifact:** progress.md's stated ordering and dating discipline
- **Direction:** neutral
- **Class:** PROVENANCE
- **Severity:** S4
- **Label:** DERIVED
- **Claim challenged (verbatim):** "Append-only. One dated entry per stage, newest at top." — HFExperiment/progress.md:3
- **Evidence:** Two defects, both in the single entry added by `82e77a0`.
  - **(i) Ordering.** The file's headings run 2026-08-26 (`:5`), 2026-08-25 (`:23`), 2026-08-25 (`:56`), 2026-08-24 (`:102`), 2026-08-23 (`:152`), 2026-08-23 (`:187`) — correctly descending — and then "## 2026-08-28T22:10Z — ADR-026: the stale no-account blocker, corrected" at `:226`, the newest entry, at the **bottom**.
  - **(ii) Timestamp.** That heading's stated time, 2026-08-28T22:10Z, is **55 m 52 s after** the author and committer date of the only commit that contains it, `82e77a0` = 2026-08-28T21:14:08Z, so the entry claims to have been written after the commit that carries it.
- **Recomputation:** `git log -S"ADR-026" -- progress.md` returns `82e77a0` alone; 22:10:00Z − 21:14:08Z = +55 m 52 s. Heading order re-read from SNAP at consolidation.
- **What would resolve it:** moving the entry to the top, or a note that ADR-026 is not a stage and is appended deliberately; and a corrected timestamp.
- **Confidence:** HIGH — both are direct reads of the file and the commit object.
- **Invalidated by later commits?:** no — the repository is closed and `82e77a0` is HEAD.
- **Disclosed by authors?:** no — progress.md:228 calls the entry "Not a stage", which explains why it is not a stage entry but not why it sits below older entries under a "newest at top" rule, and says nothing about the timestamp.

---

### AUDIT-C-HFExperiment-8

- **Repository / SHA:** HFExperiment / 82e77a021256d917c665ff6d4304c25b08f35451
- **Hypothesis or artifact:** the shadow-series systemd timer unit
- **Direction:** neutral
- **Class:** PROVENANCE
- **Severity:** S4
- **Label:** DERIVED
- **Claim challenged (verbatim):** "# Installed to ~/.config/systemd/user/ by scripts/install_timer.sh." — HFExperiment/systemd/hfexperiment-bars.timer:4
- **Evidence:** `git ls-tree -r --name-only 82e77a0 -- scripts/` returns eight files, all `.py`: `a1b_capability_test.py`, `cost_table.py`, `cost_table_a2.py`, `daily_run.py`, `demo_c1.py`, `fetch_c1_formation.py`, `measure_book_spreads.py`, `reproduce_formation.py` — confirmed identical by direct listing of SNAP/HFExperiment/scripts/ at consolidation. `git log --all --oneline -- 'scripts/install_timer.sh' '*install_timer*'` returns nothing, and a scan of every added file across all refs (`git log --all --diff-filter=A --name-only`) finds **no `.sh` file has ever been tracked in this repository**; `find SNAP/HFExperiment -name '*.sh'` returns 0 files. The named installer therefore never existed at any commit, so the units were installed by some untracked means. The installation itself is real (the inventory records the installed units byte-identical to the tracked copies) and the timer is now disabled, inactive and unscheduled (live `systemctl --user`, read 2026-09-04T00:18:43Z, UNANCHORED).
- **Recomputation:** n/a.
- **What would resolve it:** committing the installer, or amending the comment to describe how the units were actually installed.
- **Confidence:** HIGH — exhaustive over all refs and over the anchored tree.
- **Invalidated by later commits?:** no — `82e77a0` is HEAD; a later commit could add the script, which would not change its absence at the anchor.
- **Disclosed by authors?:** no.

---

### AUDIT-C-HFExperiment-9

- **Repository / SHA:** HFExperiment / 82e77a021256d917c665ff6d4304c25b08f35451
- **Hypothesis or artifact:** docs/ACCESS.md's citation of the C.1 account-pin demonstration
- **Direction:** neutral — hygiene
- **Class:** INTERNAL_INCONSISTENCY
- **Severity:** S4
- **Label:** DERIVED
- **Claim challenged (verbatim):** "the `account_not_pinned` refusal is demonstrated against DU999999 in `reports/stage_c1/refusals.md`" — HFExperiment/docs/ACCESS.md:212-214
- **Evidence:** the cited artifact and every producing site use **DU9999999** (seven nines, not six): HFExperiment/reports/stage_c1/refusals.md:197 ("Arithmetic: intent.account DU9999999 != pinned IBKR_ACCOUNT_ID [paper account ID removed]") and :203 (the same string inside the written ledger record), HFExperiment/reports/stage_c1/demo_ledger.jsonl:49, HFExperiment/scripts/demo_c1.py:310, HFExperiment/tests/test_gatewire.py:117, HFExperiment/tests/test_brokerconfig.py:61 and :64. n = 7 sites against 1. A grep for `DU999999` across the anchored snapshot returns exactly these eight hits and no other; ACCESS.md:213 is the only six-nine occurrence.
- **Recomputation:** none — exhaustive string comparison across the anchored snapshot, re-run at consolidation.
- **What would resolve it:** correcting the account id in HFExperiment/docs/ACCESS.md:213 to DU9999999.
- **Confidence:** HIGH — a single-character mismatch, exhaustively enumerated.
- **Invalidated by later commits?:** no — ACCESS.md:212-215 landed at HEAD `82e77a0` and the repository is closed.
- **Disclosed by authors?:** no.

---

## Merges and drops

- **Drops: none.** All 10 draft findings (4 from verification, 6 from provenance) carry a verbatim
  quote with file and line plus at least one figure with its n or its artifact, and every quote and
  figure was re-located in SNAP/HFExperiment at consolidation. Nothing was dropped for want of
  evidence.
- **Merge 1 (2 → 1):** verification DRAFT-V-3 and provenance DRAFT-P-2 are the same finding — the
  Gateway server version 187 in prose against 178 in `reports/stage_a1b/evidence.jsonl`. DRAFT-P-2
  flagged the overlap itself. They are consolidated as **AUDIT-C-HFExperiment-3**, taking the union
  of their cited sites (a1b_report.md:3-4, DECISIONS.md:408, DECISIONS.md:441, ACCESS.md:178,
  progress.md:235) and the union of their evidence (the 51-record parse, the producing script line,
  and the C.1 probe as the traceable source of 187). Severity S3 (the higher of the two drafts).
- **Partial overlap, deliberately kept separate:** DRAFT-P-3 quotes a sentence
  (ACCESS.md:177-180) that also contains "server version 187". Its two substantive contentions —
  the 02:57–03:07 window and the "four of the six sub-tests" count — are distinct from the server
  version and rest on different artifacts, so it survives as **AUDIT-C-HFExperiment-4** with the
  server-version component explicitly excluded and cross-referenced to finding 3, so that no reader
  counts the same defect twice.
- **Recorded but not raised** (checked, real, too small or already explained): the stale
  `orders_placed_total {count: 4, cap: 10}` row written 51 s before the fifth order; the dropped
  72-dot line in the C.1 pytest paste; the "order 1,000 to 2,000 trading days" prose against the
  same paragraph's 2,061; the ADR-023/024/025 numbering gap (no claim of contiguity exists); the
  unsourced WSR formula convention (conservative either way); and the union bound of 0.10 over all
  three widths (zero alpha ever spent).

## Sound

What verified cleanly, from stored primitives, with nothing taken on the document's word:

- **The Section 0 closure.** Every element of the BLOCKED verdict sentence is present in the
  session's own 51-row evidence ledger: 5 orders of a 10 cap, 3 × error 10243 across 2 symbols and
  2 order types, 1 × error 10244 on cashQty, a whole-share control accepted, 20 contracts at
  MinSize/SizeIncrement 0.0001, `fills: []`, `final_positions: []` twice.
- **The cost model end to end.** Hurdle 4.073081 bp/day against a registered 4.07; round trip
  213.8367 bp against 213.84; annual drag 28.76 (Tiered whole-share) and 56.84 (fractional); the
  width-5 rows 17.13 / 48.33 / 86.73; the commission crossovers at exactly 70 and 100 USD; the SEC
  §31 and FINRA TAF arithmetic and the 0–2.2 bp floor gap.
- **The spread measurement.** Median 12.77318, p75 17.23247, p90 20.73058, max 27.43237, min
  2.14133, p25 6.36740 — all exact from 20 per-name medians over 180 cells (6 crossed discarded,
  88 locked), and correctly reported as a distribution rather than an interval.
- **The confidence-sequence construction.** ρ = 0.071641330 by my own golden section and 0.0716407
  by an independent 150,001-point grid; `first_crossing_day` giving day 2,061 to clear zero and day
  2,852 to clear the hurdle; the pointwise sanity check at 603.4 days; the sequential inflation
  factor 1.8452; 8.18 and 11.32 years.
- **The A.1 series.** All 21 median-share-price cells reproduce from stored `last_close` with 0
  mismatches; the churn means 5.1667 → 5.2 and 2.0; 200/10.4 = 19.23 months against 200/4.0 = 50;
  the reproduction log's 124/124 identical and the 10 × 500-row universe check exact.
- **The two-point power law and its interpolation.** Exponents −0.32113 and −0.44528; TE(10) 53.15,
  TE(20) 42.54; excess(10) 20.56, excess(20) 15.10; IR 0.975 and 0.894; (IR₅/IR₂₀)² = 1.4109 — and
  the endpoints' mutual consistency (IR = excess × 252/(TE × 100), TE 66.4 %/yr → 418.28 bp/day) is
  exact, though the 252-day annualisation it requires is stated in no document.
- **The price reconciliation.** 103.2525/143.895 = 0.717554 → a 28.24 % gap; MXL 0.51761; WOLF
  0.54622; the per-name ratio range 0.5176–1.0613.
- **The ledgers and the guards.** `{intent: 20, refusal: 34, would_submit: 1}` over 55 rows exactly;
  3 spend records summing to 100.01 with the 2025 row correctly outside the 365-day window; 158
  `def test_` functions across 27 test files; 12/12 mutations recorded CAUGHT; all 10
  `RegisteredThresholds` fields with at least one enforcement site outside `registered.py`.
- **Pre-registration integrity.** The Section 0 outcome map is byte-identical at the root commit and
  at the anchor, fixed 19 minutes before the broker documentation existed and two days before the
  deciding fractional measurement; `registered.py` has zero deletions in its history; no registered
  bar, parameter, prior or rule was ever changed after data existed; the universe code copied from
  AiTrader differs from its frozen source by exactly one typing-import line.
- **Honest reporting of emptiness.** `verdict.txt` prints `observations: 0` and `bounds: none, the
  series has not started` at all three widths; `health.txt` prints `last run: never`; the closure
  entry states zero capital and zero observations. Had the thesis "this repository over-claims its
  results" held, the place to find it would be a realized verdict, an interval or a p-value asserted
  on the shadow series. **There is none, and the repository says so in its own output.** The one
  number that would carry a real claim, the 27.99, is imported and labelled as imported ("the
  already-spent holdout", "recorded"), with the registration explicit that it was spent elsewhere and
  may not be re-spent (REGISTRATION.md:71-74).

## Could not be checked and why

1. **The holdout width figures — the largest unchecked dependency in the repository.** 27.99 bp/day,
   66.40 %/yr and IR 1.062 at width 5, and 10.04 / 31.70 / 0.798 at width 50, exist in HFExperiment
   **only as literals**: `scripts/cost_table_a2.py:31-34` (comment: "recorded in the A.2 stage
   prompt"), `src/hfexperiment/registered.py:104-105`, and the table at REGISTRATION.md:113-118.
   There is no data file, no notebook, no log and no report holding them, and **no n, no sample
   window, no standard error and no t-statistic is stated for them anywhere**. What rests on them:
   the registered hypothesis, the choice of width 5 as PRIMARY, the whole two-point power law and its
   four interpolated cells, the σ = 418 bp/day, and the day-2061 / day-2852 arithmetic. Declared
   origin is the AiTrader cross-sectional round of 2026-07-26 (README.md:3-5, `benchmark.py:5-9`),
   which this task does not cross into. **UNVERIFIABLE, not contradicted** — and their mutual
   consistency is exact.
2. **The A.1 reproduction itself.** `scripts/reproduce_formation.py` reads
   `/home/kiros-li/Documents/GitHub/AiTrader/analysis_bars.db` (`src/hfexperiment/dbaccess.py:13`).
   Its stored outputs were verified exhaustively (reproduce_log.txt, universe_check.json,
   db_hash_before/after byte-identical at `c30d3f44…`), but the 124 dates, the 10 × 500 rows, the
   19,744 segmented symbols and ADR-005's 1,535 partially-refreshed symbols cannot be re-derived
   without opening AiTrader's database. ADR-006 (DECISIONS.md:106-110) already discloses that
   "identical" covers universe membership and formation dates, not the recorded books.
3. **Every external figure.** The IBKR published schedules and their quoted disclosure text
   (ACCESS.md:52-67, :71-76, :165-167), the SEC §31 and FINRA TAF rates (:91-106), the four broker
   rows, and the stockanalysis.com corporate-actions check behind the price reconciliation
   (price_reconciliation.md:18-34). All carry URLs and retrieval dates; none has a stored capture; no
   web access was used. Their **derivations** all verify.
4. **Anything the shadow series would have produced.** Zero observations exist. There is no interval,
   no test statistic and no p-value to reproduce, and no clustered or block-bootstrap alternative to
   compute.
5. **The provenance of the confidence-sequence formula.** `verdict.py:8-16` states the radius without
   citing a source, so whether α in `ln(√(tρ²+1)/α)` is the two-sided or the one-sided level of the
   underlying construction cannot be settled from this repository. Using it one-sidedly at α = 0.05
   is conservative under the two-sided reading and exact under the one-sided one, so the ambiguity
   cannot make the success rule anti-conservative. Flagged, not raised.
6. **Whether the broker measurement was *performed* before the outcome map was fixed.** Git proves
   only that the artifact (`docs/ACCESS.md`) was committed 19 min 18 s after the root commit;
   ACCESS.md is documentation research with no capture timestamps, so a reading done earlier and
   written up later is not excluded. What *is* excluded is the contaminating case that matters: the
   deciding bar was fractional-through-the-API at 45 USD, measured only on 2026-08-25 by A.1b, two
   days and eleven commits after the bar was fixed, with the bar's text byte-identical across that
   span.
7. **Acceptance by delegation (P17).** "The act of running the B.1 stage prompt was the acceptance"
   (DECISIONS.md:230-235) — the only records are the same session's own amendment entry and commit
   `8c4c3bc`. No operator-authored artifact exists in or beside the repository. The authors state
   this plainly, so it is disclosed, not concealed. **UNVERIFIABLE by construction.**
8. **"A funded live IBKR account" (P18).** The paper account id [paper account ID removed] verifies against
   `evidence.jsonl`; "funded" and "live" rest on an operator statement of 2026-08-28, labelled as
   such. No artifact could confirm it and none should — reading a broker statement is out of scope
   and would touch credentials.
9. **The ADR numbering gap.** ADR-022 is followed by ADR-026; nothing in the tree mentions
   ADR-023/024/025 and DECISIONS.md has zero deletions in its history, so nothing was removed.
   Whether three ADRs were drafted and never committed, or the numbering simply skipped, is not
   determinable from the git objects. No claim of contiguous numbering exists, so this is not raised.
10. **Live untracked state is UNANCHORED.** `data/bars.db` (0 rows in all six tables),
    `data/c1_formation.db`, the empty `data/ledger/`, and the disabled/inactive/unscheduled timer
    were read from the live working tree at 2026-09-04T00:18:43–00:19:03Z with
    `file:…?immutable=1`. They may have changed after that read and after the 2026-08-28 anchor,
    though the repository carries a `_CLOSED_DO_NOT_RUN_HERE` marker and the timer is disarmed.

## Live-repo access log

Merged from the two upstream passes. Both accessed
`/home/kiros-li/Documents/GitHub/HFExperiment/` read-only, for git history/provenance and (in the
provenance pass) for untracked working-tree data that exists nowhere else. **No file under any
audited repository was opened for writing, no repository script was executed, `.env` was not read,
and no credential, token or session file was opened.** This consolidation step performed **no live
repository access at all**: it read only SNAP/HFExperiment and the two upstream output files, and
wrote only under `findings/agentC/`.

**Provenance pass — `git -C /home/kiros-li/Documents/GitHub/HFExperiment status --porcelain`, BEFORE first access, 2026-09-04T00:11:16Z:**

```
?? Accept:
?? GET
?? Host:
?? User-Agent:
```

**Provenance pass — same command, AFTER last access, 2026-09-04T00:26:52Z:**

```
?? Accept:
?? GET
?? Host:
?? User-Agent:
```

**Verification pass — same command, BEFORE first access, 2026-09-04T00:18:36Z:**

```
?? Accept:
?? GET
?? Host:
?? User-Agent:
```

**Verification pass — same command, AFTER last access, 2026-09-04T00:20:51Z:**

```
?? Accept:
?? GET
?? Host:
?? User-Agent:
```

All four readings are identical and are exactly the four stray files COMMON_RULES records as
pre-existing owner dirt (`?? Accept:`, `?? GET`, `?? Host:`, `?? User-Agent:`). Nothing else
appeared at any point; the verification pass's window sits inside the provenance pass's window and
the two agree. **No accidental modification occurred in HFExperiment.**

Secondary repository, read once for the universe-copy check (P11):
`git -C /home/kiros-li/Documents/GitHub/AiTrader status --porcelain` returned ` M COLLECTION_LOG.md`
— the pre-existing collector dirt COMMON_RULES names — both before those reads and again at
2026-09-04T00:26:52Z, unchanged. AiTrader was touched with `git log`, `git show` and `git status`
only.

| time (UTC) | pass | command | purpose |
|---|---|---|---|
| 00:11:16 | prov | `git status --porcelain` | pre-access baseline |
| 00:11:2x | prov | `git log --format=… --date=iso-strict --reverse`, `git log --numstat --reverse` | 13-commit timeline; complete deletion census |
| 00:12:xx | prov | `git rev-list --parents -n1 c4e9817`, `git show --stat c4e9817`, `git show c4e9817:REGISTRATION.md` | P1, P2 — root commit, Section 0 fixity |
| 00:12:xx | prov | `git log --follow -p -- REGISTRATION.md`, `git show 8c4c3bc/669eb5c/f13e1d3 -- REGISTRATION.md` | P3, P4, P8, P9, P10, finding 2 |
| 00:13:xx | prov | `diff <(git show c4e9817:REGISTRATION.md) <(git show 82e77a0:REGISTRATION.md \| head -49)` | outcome-map byte identity, root vs anchor |
| 00:13:xx | prov | `git show 6ac61d2 -- src/hfexperiment/registered.py`, `git show 82e77a0 -- DECISIONS.md`, `git show 82e77a0 -- docs/ACCESS.md` | parameter table, P14, P16, findings 4 and 6 |
| 00:14:xx | prov | `git log -S"<figure>"` for 4.07, 27.99, 1.062, 0.071641, 0.15, 418.0, 2061, 2852, 1600, 0.025, 500.0, 100.0, 5.2, 15.8, 28.76, 56.84, 1.41, 1.75 | first-introduction dates of every registered figure |
| 00:15:xx | prov | `git log --all -- 'scripts/install_timer.sh'`, `git log --all --diff-filter=A --name-only`, `git ls-tree -r --name-only 82e77a0 -- scripts/` | finding 8 |
| 00:15:xx | prov | `git grep -n` at c4e9817 / 0a0d214 / a8f4b0d / 82e77a0 | figure locations at each commit |
| 00:16:xx | prov | AiTrader: `git log -- backtest/universe.py`, `git show d6ad37a:backtest/universe.py`, `git status --porcelain` | P11, universe copy fidelity |
| 00:18:36 | verify | `git status --porcelain` | pre-access baseline |
| 00:18:3x | verify | `git rev-parse HEAD` | confirmed 82e77a021256d917c665ff6d4304c25b08f35451 |
| 00:18:3x | verify | `git log --format='%h %ad %aI %s' --date=iso-strict` | dated Sections 1-12 (`a8f4b0d`, 2026-08-24T04:40:25Z) against `book_spreads.json` `measured_utc` 2026-08-24T04:23:29Z |
| 00:18:43 | prov | `systemctl --user is-enabled/is-active hfexperiment-bars.timer`, `list-timers --all` | P10 timer state (outside the repo, read-only) — UNANCHORED |
| 00:18:48 | prov | sqlite `file:data/bars.db?immutable=1`, `file:data/c1_formation.db?immutable=1` — table list + `count(*)` | shadow-series emptiness — UNANCHORED |
| 00:19:03 | prov | `ls -la data/`, `ls -la data/ledger/` | ledger emptiness — UNANCHORED |
| 00:20:51 | verify | `git status --porcelain` | post-access baseline |
| 00:2x:xx | prov | `git rev-parse HEAD`, `git branch -a`, `TZ=UTC git log --date=iso-strict-local` | anchor confirmation, UTC dating |
| 00:26:52 | prov | `git status --porcelain` (HFExperiment and AiTrader) | post-access baseline |

All computation was performed with the audit venv at
`/tmp/claude-1000/-home-kiros-li-Documents-GitHub-program-audit/5ca157a0-1746-4eb9-a1b8-f3732ea42bf4/scratchpad/venv/bin/python`,
reading only from SNAP/HFExperiment, with scratch output confined to
`/tmp/claude-1000/-home-kiros-li-Documents-GitHub-program-audit/…/scratchpad/work/agentC-*/`.
