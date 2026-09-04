# Agent B — HFExperiment

Repository: **HFExperiment**, anchored SHA **82e77a021256d917c665ff6d4304c25b08f35451** (main, 2026-08-28).
Direction B: the program claimed more than it earned. All tracked content read from SNAP/HFExperiment;
the live repository was used read-only for git history and for the untracked `data/` working tree
(marked UNANCHORED where used). 18 findings: 1 × S1, 6 × S2, 9 × S3, 2 × S4.

## The strongest case for the thesis in this repository

This experiment shipped **no result**: zero shadow observations, zero fills, no verdict, no capital deployed.
What it shipped is one measurement verdict and a set of numeric artifacts, and the case for the thesis is that
those carry more warrant in their wording than in their evidence. The causal control that converts "three
fractional orders were refused" into "Read-Only is off and the refusal is specific to fractional sizing" was
placed by code that exists in no commit, into a ledger the committed script deletes at the start of every run.
The registered success bar, "the measured cost hurdle of 4.07 bp per day", is 93.5 % an unbilled commission
projection under a billing regime the same repository measured as unavailable four days later and then left
unchanged. The session identity of that headline run is quoted as server version 187 in five documents where
the run's own ledger records 178. The record-hygiene ADR that promises "Nothing is rewritten to look as though
it was always right" added a seventh, already-passing sub-test to a registered set of six, deleted the
precondition column rather than striking it, and rewrote a paragraph in place. And the front door still says
the execution cost was "measured directly".

---

### AUDIT-B-HFExperiment-1
- **Repository / SHA:** HFExperiment / 82e77a021256d917c665ff6d4304c25b08f35451
- **Hypothesis or artifact:** Stage A.1b whole-share control order — the evidence that converts "three fractional orders were refused" into "the refusal is specific to fractional sizing" and into "Read-Only API verified off by behaviour", and which the binding BLOCKED amendment cites
- **Direction:** B
- **Class:** PROVENANCE
- **Severity:** S1
- **Label:** DERIVED
- **Claim challenged (verbatim quote):** "One whole share of TE was ACCEPTED and queued for the 09:30 ET open, then cancelled. The channel works, Read-Only is off, and the fractional refusals are specific to fractional sizing." — HFExperiment/reports/stage_a1b/a1b_report.md:91-93. Also "Read-Only API verified off by behaviour: the whole-share control order was accepted and queued, so orders were validated on their merits." — HFExperiment/reports/stage_a1b/a1b_report.md:7-8, and "while a whole-share control order was accepted" in the binding amendment — HFExperiment/REGISTRATION.md:302.
- **Evidence:**
  - The committed stage script places exactly four orders and no control: `decimal-mkt-MU`, `decimal-lmt-MU`, `decimal-mkt-TE`, `cashqty-mkt` (HFExperiment/scripts/a1b_capability_test.py:278, 296, 310, 321, inside `main()` at :247-353). There is no whole-share order anywhere in the file.
  - **No revision of the script contains the word "control" at all.** Checked every blob in the file's history (`git -C <live> show <c>:scripts/a1b_capability_test.py | grep -in control` for c = 669eb5c and 23b7791, the only two commits that touch it): no match in either. The single hit from `git log -p --all -- scripts/a1b_capability_test.py` is in the *commit message* of 669eb5c ("while a whole-share control was accepted"), not in code. 23b7791 (2026-08-25T03:09:55Z) is a lint rename.
  - The evidence ledger records the control anyway: `{"account":"[paper account ID removed]","action":"BUY","kind":"order_request","label":"control-whole-share","order_number":5,"order_type":"MKT","purpose":"control: a whole share must accept, proving the channel works and only fractional is refused","route":"SMART","symbol":"TE","tif":"DAY","total_quantity":"1","utc":"2026-08-25T03:07:06.141398Z"}` — HFExperiment/reports/stage_a1b/evidence.jsonl:48.
  - That record cannot have been written by the committed emitter. `place()` emits a fixed keyword set — label, symbol, order_type, action, total_quantity, cash_qty, lmt_price, outside_rth, tif, account, route, order_number (HFExperiment/scripts/a1b_capability_test.py:106-115) — with no `**extra`. Record 48 **carries** a `purpose` field the emitter never writes and **lacks** `cash_qty`, `lmt_price` and `outside_rth`, which it always writes (compare evidence.jsonl:30, the decimal-mkt-MU request, which carries all three).
  - The outcome record is likewise foreign: `record_trade()` always emits order_id, status, filled, **remaining**, **avg_fill_price**, log (HFExperiment/scripts/a1b_capability_test.py:129-137); evidence.jsonl:49 has order_id, status, filled and log only.
  - Ordering: the committed script wrote `{"cap":10,"count":4,"kind":"orders_placed_total","utc":"2026-08-25T03:06:14.859168Z"}` (evidence.jsonl:47) and a `final_positions` record at 03:06:14.850255Z (evidence.jsonl:46) from its `finally:` block (script :347-351), i.e. the committed run had already ended. The control request is stamped 03:07:06.141398Z, 51 s later.
  - The control ran on a different connection: its warning is "reqId 3" and its `order_id` is 3 (evidence.jsonl:49), while the four committed orders used reqIds 25, 26, 29, 30 (evidence.jsonl:30, 33, 40, 43).
  - n: 1 control order, 0 fills, produced by 0 lines of committed code, in a file of 51 records.
- **Recomputation (if any):** none needed; the finding is a field-set comparison between the committed emitter (scripts/a1b_capability_test.py:106-115 and :129-137) and evidence.jsonl:48-49, plus a git-object check of every revision of the script.
- **What would resolve it:** the code that placed the control order, committed, with its own run log; or a re-run of a committed control under the same rails. Failing that, an explicit note in a1b_report.md that the control was placed by hand outside the rail-guarded script.
- **Confidence:** HIGH that the provenance is not established — the emitted field sets differ in both directions and no revision of the script can place a control order; LOW that the control is factually wrong, since the IBKR Warning 399 text in record 49 is not the kind of thing this repository fabricates elsewhere. The severity is S1 because the stated conclusion is *unsupported by any reproducible record*, not because it is shown false.
- **Invalidated by later commits?:** no — 82e77a0 is the tip and touched only DECISIONS.md, docs/ACCESS.md and progress.md (`--numstat`: 60/0, 47/19, 48/0).
- **Disclosed by authors?:** no. The report presents the control inside the same run as the refusals ("Five orders of the ten-order cap used", a1b_report.md:5) and the script's docstring claims "The only stage authorized to place paper orders. Hard rails enforced in code below: at most ten orders" (scripts/a1b_capability_test.py:4-6); the fifth order was placed outside that rail, whose counter is per-process (`self.orders_placed`, :89, 95-98) and had already stopped at 4.

---

### AUDIT-B-HFExperiment-2
- **Repository / SHA:** HFExperiment / 82e77a021256d917c665ff6d4304c25b08f35451
- **Hypothesis or artifact:** the registered success bar, "the measured cost hurdle of 4.07 bp per day" — the repository's single most quotable shipped number
- **Direction:** B
- **Class:** UNSUPPORTED_POSITIVE
- **Severity:** S2
- **Label:** DERIVED
- **Claim challenged (verbatim quote):** "Success when the lower bound clears the measured cost hurdle of 4.07 bp per day, computed at the primary width under the worst-case fractional regime with the measured width-5 spread." — HFExperiment/REGISTRATION.md:249-251
- **Evidence:**
  - Composition, from HFExperiment/reports/stage_a2/cost_table.md:36 and HFExperiment/src/hfexperiment/registered.py:71-78: round trip 213.84 bp = **200.00 bp commission** (fractional schedule, 1 % of value per side, docs/ACCESS.md:141) + **13.08 bp measured spread** + **0.76 bp regulatory** (docs/ACCESS.md:139). Recomputed: 200 + 13.075182298214278 + 0.0137/180×10⁴ = 213.836 bp; hurdle = (2.0/5) × 213.836 / 21 = **4.0731** bp/day. The registered 4.07 reproduces exactly.
  - **93.5 %** of the bar (200.00/213.84) is a commission projection read off a published web page and never billed: "No order filled, so no commission was observed. Nothing exists to label INDICATIVE-ONLY and nothing migrates into the cost model." (HFExperiment/reports/stage_a1b/a1b_report.md:96-98). Another **0.36 %** (0.76 bp, driven by the one-cent TAF floor) is a bound the repository itself calls unverifiable: "The one cent TAF floor the settled design assumed is CONFIRMED NOWHERE." (HFExperiment/docs/ACCESS.md:98). Only **6.1 %** (13.08/213.84) is measured, and that measurement is itself n=5 names over 9 near-instantaneous cells (see AUDIT-B-HFExperiment-9).
  - The regime it is computed under was subsequently measured **unavailable through the API** by this same repository: "error 10243 on decimal totalQuantity across two book names and two order types, error 10244 on cashQty" (HFExperiment/REGISTRATION.md:299-302). The same amendment closes with "No parameter changes." (REGISTRATION.md:304), so the success bar was left standing on a falsified billing regime.
  - Under the only regime the broker does offer at this stake, whole-share Tiered, the identical arithmetic gives a hurdle of **1.00 bp/day** (round trip 2×19.4 + 13.08 + 0.76 = 52.64 bp; 0.4 × 52.64 / 21 = 1.0026). The registered bar is 4.06× the achievable one.
  - The bar is still live in code and in the shipped monitor: `cost_hurdle_bp_per_day: float = 4.07` (registered.py:78), "success bar: lower bound above 4.07 bp/day" (HFExperiment/reports/monitor/verdict.txt:8, 17, 26).
  - n: 0 fills, 0 broker statements, 1 published fee page, 20 names × 9 cells of quotes behind the one measured term.
- **Recomputation (if any):** inputs — spread 13.075182298214278 bp (reports/stage_a2/book_spreads.json:37, median of the five width-5 names' per-name medians), notional 180 USD (900/5, REGISTRATION.md:133), churn 2.0 names/month (src/hfexperiment/registered.py:85, from reports/stage_a1/formations.md:11-16 → (4+3+1+1+2+1)/6 = 2.0), regulatory 0.0137 USD (docs/ACCESS.md:139), 21 trading days/month (src/hfexperiment/costmodel.py:213). Method: `costmodel.daily_cost_hurdle_bp` reimplemented. Results: 4.0731 bp/day; whole-Tiered variant 1.0026; whole-Fixed variant 2.3817.
- **What would resolve it:** re-labelling the bar as a projection rather than a measurement, or an amendment recomputing it under the whole-share Tiered regime that A.1b left standing ("Whole-share through the API stays open; only slicing is closed", docs/ACCESS.md:197).
- **Confidence:** HIGH — the arithmetic reproduces exactly from stored artifacts and code, and the regime falsification is the repository's own recorded verdict.
- **Invalidated by later commits?:** no — the tip commit changed no figure and touched no code.
- **Disclosed by authors?:** partially. That the hurdle uses the worst-case fractional regime is disclosed in the quoted sentence itself and at registered.py:71-78, and the unmeasured TAF floor at docs/ACCESS.md:98. What is **not** disclosed anywhere is that after 2026-08-25 the regime is known unavailable, that the bar was deliberately left unchanged, and that the word "measured" covers 6 % of the figure. Severity is not capped, because the undisclosed part is the finding.

---

### AUDIT-B-HFExperiment-3
- **Repository / SHA:** HFExperiment / 82e77a021256d917c665ff6d4304c25b08f35451
- **Hypothesis or artifact:** Stage A.1b session identity — the Gateway server version reported for the run that produced the Section 0 BLOCKED verdict
- **Direction:** B
- **Class:** INTERNAL_INCONSISTENCY
- **Severity:** S2
- **Label:** DERIVED
- **Claim challenged (verbatim quote):** "Run 2026-08-25, 02:57 to 03:07 UTC, Monday 22:57 to 23:07 ET, market closed. Gateway 127.0.0.1:4002, server version 187, account [paper account ID removed], declared mode paper." — HFExperiment/reports/stage_a1b/a1b_report.md:3-5
- **Evidence:**
  - The A.1b evidence ledger's own connection record says 178, not 187: `{"kind":"connected","managed":["[paper account ID removed]"],"server_version":178,"utc":"2026-08-25T03:05:16.497779Z"}` — HFExperiment/reports/stage_a1b/evidence.jsonl:2. The value is written straight from the client: `server_version=self.ib.client.serverVersion()` (HFExperiment/scripts/a1b_capability_test.py:157-159).
  - Four further narrative sites repeat 187 **for this run**: HFExperiment/docs/ACCESS.md:178, HFExperiment/DECISIONS.md:408 (ADR-022), HFExperiment/DECISIONS.md:439 (ADR-026), HFExperiment/progress.md:235. (progress.md:80 also says 187 but describes the C.1 probe, where it is correct; it is not counted.)
  - 187 is the number the **C.1 probe** reported 25 minutes earlier on the same Gateway: `"server_version": 187` (HFExperiment/reports/stage_c1/refusals.md:332, `server_time_epoch` 1787625630). The probe's own handshake string caps at 187: `_HANDSHAKE_VERSIONS = b"v100..187"` (HFExperiment/src/hfexperiment/ibkrprobe.py:43).
  - n: 2 connections to one Gateway, 25 minutes apart, 2 different reported versions; 5 documents quote the one that is not in the A.1b ledger.
- **Recomputation (if any):** epoch 1787625630 → 2026-08-25T02:40:30Z, confirming the probe preceded A.1b (03:05:16Z) by ~25 min.
- **What would resolve it:** correcting a1b_report.md and the four derived sites to 178, or recording explicitly that 187 is the C.1 probe's negotiated version and that A.1b negotiated 178 with a different client library.
- **Confidence:** HIGH — the ledger value is machine-written and unambiguous; the reports state 187 as a fact of the A.1b session.
- **Invalidated by later commits?:** no — ADR-026 (the tip commit) repeats 187 at DECISIONS.md:439 while citing this same evidence file.
- **Disclosed by authors?:** no. ADR-022 presents the figure as part of what is "Observed" in reports/stage_a1b/evidence.jsonl (DECISIONS.md:405-411), which is precisely where it is contradicted.

---

### AUDIT-B-HFExperiment-4
- **Repository / SHA:** HFExperiment / 82e77a021256d917c665ff6d4304c25b08f35451
- **Hypothesis or artifact:** ADR-026 (2026-08-28) — the re-statusing of the six registered Task 3 sub-tests, and its own account of the edit
- **Direction:** B
- **Class:** PROCESS
- **Severity:** S2
- **Label:** DERIVED
- **Claim challenged (verbatim quote):** "Decided. ACCESS.md Task 3 is re-headed SUPERSEDED, the false sentence is struck rather than deleted, and the sub-test table is re-statused against the A.1b evidence: four RESOLVED, two MOOT, one RUNNABLE. ADR-003 keeps its original text with a superseded note beneath it. Nothing is rewritten to look as though it was always right." — HFExperiment/DECISIONS.md:450-454
- **Evidence:** `git -C <live> show --numstat 82e77a0 -- docs/ACCESS.md` gives **47 insertions, 19 deletions**. The diff shows three things the sentence above does not describe.
  1. **A seventh, already-passing row was added.** The registered table at 82e77a0^ has exactly six sub-test rows, all BLOCKED-ON-OPERATOR (decimal totalQuantity, cashQty, routing comparison, MinSize/SizeIncrement, billing plan on a paper fill, mixed-order billing — `git show 82e77a0^:docs/ACCESS.md`, lines 180-187). The corrected table has seven: a new row "| whole-share control order | **RESOLVED — ACCEPTED** | ..." (HFExperiment/docs/ACCESS.md:197) that exists in no earlier revision. The advertised score "four RESOLVED, two MOOT, one RUNNABLE" (DECISIONS.md:452, repeated at progress.md:248-252) is therefore 4/7 against a registered set of 6, and the fourth RESOLVED is a test added at correction time, after it had passed. It carries no marker distinguishing it from the original rows.
  2. **The precondition column was deleted, not struck.** The original third column was headed "what must be true to run" and every one of the six rows carried "live account exists, **Trade in Fractions enabled**, paper gateway reachable" (or "same"). The diff removes all six cells and re-heads the column "evidence or precondition" (docs/ACCESS.md:192). Nothing anywhere records that the Trade in Fractions permission was ever confirmed.
  3. **A whole paragraph was rewritten in place, not struck.** The deleted "The documentation conflict stands unresolved on purpose ... Likely is not measured. The verdict waits for the test." is replaced by "The documentation conflict, for the record, is now resolved rather than open ... The verdict no longer waits for the test." (HFExperiment/docs/ACCESS.md:217-223). Only one sentence in the whole edit is actually struck (docs/ACCESS.md:184-186, the `~~...~~` span).
  - n: 6 registered sub-tests → 7 reported; 19 deleted lines against a claim of "struck rather than deleted"; 1 struck span.
- **Recomputation (if any):** none; the finding is the diff of the tip commit against its parent, read as a git object.
- **What would resolve it:** marking the added row as added-at-correction, restoring or explicitly retiring the precondition column, and re-stating the score against the six registered sub-tests.
- **Confidence:** HIGH — the diff is unambiguous and the ADR's own method statement is falsified by it.
- **Invalidated by later commits?:** no — this is the tip commit.
- **Disclosed by authors?:** no. ADR-026 states the opposite in the sentence quoted.

---

### AUDIT-B-HFExperiment-5
- **Repository / SHA:** HFExperiment / 82e77a021256d917c665ff6d4304c25b08f35451
- **Hypothesis or artifact:** Section 6 / ADR-012, the arithmetic offered for closing the DEGRADED branch
- **Direction:** B
- **Class:** ARITHMETIC
- **Severity:** S2
- **Label:** DERIVED
- **Claim challenged (verbatim quote):** "At 144, whole-share sizing on 900 USD cannot fill a 20-name book at all, because 20 names at one share each already cost about 2,880 USD. A 5-name book gets one share per name, 720 of 900 deployed, with equal weighting destroyed by per-name prices from 22 to 1,595 USD." — HFExperiment/REGISTRATION.md:151-154 (ADR-012 repeats "about 2,880 USD", HFExperiment/DECISIONS.md:195-196)
- **Evidence:** recomputed directly from the repository's own stored formation prices, HFExperiment/reports/stage_a1/formations.json (`last_close` per name, 2026-07-01 formation):
  - one share of each of the 20 width-20 names costs **7,890.47 USD**, not "about 2,880"; the 2,880 figure is 20 × the *median* price 143.89 (reports/stage_a1/formations.md:28), which understates the true basket by 2.74×.
  - one share of each of the 5 width-5 names (WOLF, AXTI, SNDK, BE, LITE) costs **3,554.82 USD**, so a 5-name whole-share book is unaffordable on 900 USD entirely; "720 of 900 deployed" (= 5 × 144) is not reachable from any stored price set.
  - the width-5 price range at 2026-07-01 is **48.25 to 2,273.73 USD**, not "22 to 1,595". The endpoints quoted match A.2 *quoted mids* seven weeks later for PL (22.305) and SNDK (1595.1925) — HFExperiment/reports/stage_a2/book_spreads.json:51 and :33 — and PL is not in the width-5 book at all (it is rank 6, reports/stage_a1/formations.md:68-69). A grep of the whole snapshot finds "1,595"/"1595" only at REGISTRATION.md:154 and book_spreads.json:33.
  - n: 7 formations × 3 widths in formations.json; the cited formation has n=5 and n=20 names.
- **Recomputation (if any):** inputs reports/stage_a1/formations.json (2026-07-01, widths 5 and 20 `last_close`); method: sum, min, max, median with Python `statistics`; results — width 5: sum 3,554.82 / min 48.25 / max 2,273.73 / median 302.70; width 20: sum 7,890.47 / min 8.24 / max 2,273.73 / median 143.895.
- **What would resolve it:** replacing the median-as-basket shorthand with the stored sums, and naming the source of the "22 to 1,595" range.
- **Confidence:** HIGH — three figures in one registered paragraph are unreachable from the repository's own artifact, and one of them (1,595) is traceable to a different measurement of a different name-set.
- **Invalidated by later commits?:** no.
- **Disclosed by authors?:** no. In fairness: the conclusion (no whole-share sleeve at this stake) survives *a fortiori* — the true basket costs are 2.7× and 3.9× the quoted ones — which is why this is S2 and not S1. The finding is that the registered numbers are not the repository's numbers.

---

### AUDIT-B-HFExperiment-6
- **Repository / SHA:** HFExperiment / 82e77a021256d917c665ff6d4304c25b08f35451
- **Hypothesis or artifact:** ADR-021's traced consequence of the paper-api defect — the claim that the armed shadow series would run correctly until the 2026-09-01 formation
- **Direction:** B
- **Class:** INTERNAL_INCONSISTENCY
- **Severity:** S2
- **Label:** DERIVED
- **Claim challenged (verbatim quote):** "Consequence traced: B.1's nightly runs succeed until 2026-08-31 because no formation is due and no assets call happens, and the 2026-09-01 formation run fails loudly on the 401 and retries daily until the one-line fix lands under B.1 authorization." — HFExperiment/DECISIONS.md:382-385 (repeated at HFExperiment/progress.md:86-88)
- **Evidence:**
  - The 401 is attributed to the host pin: "Alpaca serves trading-API endpoints for paper keys from paper-api.alpaca.markets, and B.1 pinned api.alpaca.markets, which 401s on /v2/assets with the keys in .env" (HFExperiment/DECISIONS.md:378-380).
  - `/v2/assets` is not the only trading-API call on that host. `TRADE_BASE = "https://api.alpaca.markets"` (HFExperiment/src/hfexperiment/alpaca_source.py:27) serves **both** `calendar()` — `url = f"{TRADE_BASE}/v2/calendar?start={start}&end={end}"` (alpaca_source.py:95) — and `active_assets()` — `url = f"{TRADE_BASE}/v2/assets?status=active&asset_class=us_equity"` (alpaca_source.py:103), with the same credentials.
  - The daily entry point calls `calendar()` **unconditionally, first, on every run**: `calendar = source.calendar(start, end)` at HFExperiment/scripts/daily_run.py:120, inside `_collect_and_accrue`, returning exit 1 on `SourceError` (daily_run.py:121-124). The formation branch and the `active_assets()` call are both downstream of it.
  - So the trace's premise — that nothing before a formation touches the failing host — is contradicted by the code it describes. Nothing in the repository establishes that `/v2/calendar` is served to these keys on `api.alpaca.markets` while `/v2/assets` is not; that endpoint was never tested.
  - Corroborating (UNANCHORED, live working tree read 2026-09-04T00:09Z): `data/bars.db` contains 0 rows in every table — bars 0, sessions 0, assets 0, universe 0, formations 0, fetch_log 0 — and `data/ledger/` is empty. The timer was disarmed before its first fire, so this is consistent with, not proof of, the calendar failure.
  - n: 1 unconditional call, on every scheduled run, to the same host and credentials the ADR records as returning 401.
- **Recomputation (if any):** none; a call-graph read of scripts/daily_run.py:107-178 against src/hfexperiment/alpaca_source.py:27, 93-116.
- **What would resolve it:** a recorded probe of `GET https://api.alpaca.markets/v2/calendar` with the paper keys. If it 401s, the trace is false and the shadow series would have failed from its first scheduled run, not from 2026-09-01.
- **Confidence:** HIGH that the claim is unsupported by the repository; MEDIUM that it is factually false, because Alpaca could in principle serve one endpoint and not the other and I could not test it read-only.
- **Invalidated by later commits?:** no — `git log -- scripts/daily_run.py src/hfexperiment/alpaca_source.py` returns one commit only, 6ac61d2 (2026-08-24), so nothing after it touched either file.
- **Disclosed by authors?:** no. The closure entry instead retires the item as "B.1a cancelled as moot: no formation will ever call the assets endpoint" (HFExperiment/progress.md:19-20), which repeats the same assets-only framing.

---

### AUDIT-B-HFExperiment-7
- **Repository / SHA:** HFExperiment / 82e77a021256d917c665ff6d4304c25b08f35451
- **Hypothesis or artifact:** the dated-record discipline itself — REGISTRATION.md's amendment log and progress.md
- **Direction:** B
- **Class:** PROVENANCE
- **Severity:** S2
- **Label:** DERIVED
- **Claim challenged (verbatim quote):** "Experiment closed by operator decision, instruction dated 2026-08-26." — HFExperiment/REGISTRATION.md:308 (under the heading "### 2026-08-26: Closure", REGISTRATION.md:306; same date at progress.md:5 and progress.md:7-8). The governing rule is "Amendments are dated, numbered, appended, and each records what data existed when it was made." — HFExperiment/REGISTRATION.md:271-272.
- **Evidence:**
  - The commit that introduced both closure entries is f13e1d3c39555d445e8f4ab21db51b99a8478f8b, author and committer date **2026-08-25T00:45:29-07:00 = 2026-08-25T07:45:29Z**, message "docs: terminal closure, shadow timer disarmed, closure recorded in amendment log and progress"; `--numstat` shows REGISTRATION.md 11/0, progress.md 18/0 and nothing else. A record dated 2026-08-26 was committed roughly 16 hours before that date, and no timezone reaches 2026-08-26 from that instant (UTC+14 gives 2026-08-25T21:45).
  - The same defect in the other direction at the tip: progress.md's ADR-026 entry is headed "## 2026-08-28T22:10Z — ADR-026: the stale no-account blocker, corrected" (HFExperiment/progress.md:226) but its commit 82e77a0 is dated **2026-08-28T14:14:08-07:00 = 2026-08-28T21:14:08Z** — the entry stamps itself 56 minutes after the commit that stores it.
  - n: 2 of the repository's ~10 dated records are inconsistent with their own commits, including the terminal closure entry and the only entry that dates an operator instruction.
- **Recomputation (if any):** timezone check on f13e1d3: 2026-08-25T07:45:29Z; the maximum civil offset (+14:00) gives 2026-08-25T21:45 local, still 2026-08-25.
- **What would resolve it:** the operator's dated closure instruction, or a correction to whichever of the two stamps is wrong.
- **Confidence:** HIGH for the arithmetic; MEDIUM for interpretation — a document may legitimately anticipate a date, but an amendment log whose authority rests on "each records what data existed when it was made" cannot carry a date its own commit predates without saying so.
- **Invalidated by later commits?:** no — f13e1d3 and 82e77a0 are both in the anchored ancestry, and the tip introduced the second instance.
- **Disclosed by authors?:** no.

---

### AUDIT-B-HFExperiment-8
- **Repository / SHA:** HFExperiment / 82e77a021256d917c665ff6d4304c25b08f35451
- **Hypothesis or artifact:** reports/stage_a1b/evidence.jsonl — the primary evidence artifact behind the Section 0 BLOCKED verdict
- **Direction:** B
- **Class:** PROCESS
- **Severity:** S3
- **Label:** DERIVED
- **Claim challenged (verbatim quote):** "Every request, response, and status transition is appended to reports/stage_a1b/evidence.jsonl, its own evidence ledger, separate from the spend ledger." — HFExperiment/scripts/a1b_capability_test.py:10-12
- **Evidence:**
  - The ledger is destroyed at the start of every run: `if EVIDENCE.exists(): EVIDENCE.unlink()` — HFExperiment/scripts/a1b_capability_test.py:63-66. Only the last run survives; an earlier attempt, including any earlier order, leaves no trace.
  - This is the one stage in the repository authorised to send orders to a broker ("The only stage authorized to place paper orders", a1b_capability_test.py:4), and its order-count rail is per-process (`self.orders_placed`, a1b_capability_test.py:89, 95-98), so the "ten-order cap" is a per-run cap that the truncated ledger cannot audit across runs. The report nonetheless states a single budget: "Five orders of the ten-order cap used" (HFExperiment/reports/stage_a1b/a1b_report.md:5).
  - The contrast with the repository's stated discipline elsewhere is explicit: "nothing is ever updated or deleted in place" (HFExperiment/src/hfexperiment/barstore.py:4-6), "Append-only" ledgers throughout (ADR-016, HFExperiment/DECISIONS.md:258-274), and the spend ledger is "Append-only, fsynced, one record per event" (reports/stage_c1/refusals.md:339).
  - Combined with AUDIT-B-HFExperiment-1, the consequence is concrete: the file we have contains records the committed script cannot write, and the committed script would have erased any earlier file, so the ledger cannot establish what else was sent to [paper account ID removed] that evening.
  - n: 1 evidence file, 51 records, unknown number of runs.
- **Recomputation (if any):** none.
- **What would resolve it:** a run-scoped evidence file (one per run, never unlinked), or a recorded statement that A.1b was executed exactly once.
- **Confidence:** HIGH — the unlink is three lines of committed code.
- **Invalidated by later commits?:** no — the script was touched only by 669eb5c and 23b7791, both before the anchor.
- **Disclosed by authors?:** no.

---

### AUDIT-B-HFExperiment-9
- **Repository / SHA:** HFExperiment / 82e77a021256d917c665ff6d4304c25b08f35451
- **Hypothesis or artifact:** the measured spread distribution — the shipped artifact that replaced the inherited 15.8–50 bp band and supplies the only measured term in the registered cost hurdle
- **Direction:** B
- **Class:** STATISTICAL
- **Severity:** S3
- **Label:** DERIVED
- **Claim challenged (verbatim quote):** "Spreads are MEASURED on the real book, not assumed from a band. All 20 names of the 2026-07-01 width-20 book were measured on the consolidated tape over sessions 2026-08-19 to 2026-08-21: median 12.77 bp, p75 17.2, p90 20.7, max 27.4. The inherited 15.8 to 50 bp band predicted the wide end and measured wrong in the favourable direction, because the book's names currently trade at large dollar volume. The measured distribution replaces the band." — HFExperiment/REGISTRATION.md:170-176
- **Evidence:**
  - **The open and the closing auction are excluded by construction.** `WINDOWS = ((14, 0), (16, 30), (19, 30))  # UTC` (HFExperiment/scripts/measure_book_spreads.py:55) with `WINDOW_SPAN_S = 300` (:56) — i.e. 10:00, 12:30 and 15:30 ET, described in the docstring as "after the open, mid, near the close". The first 30 minutes of the session, where quoted spreads on a book like this are widest, and the closing cross, contribute nothing. A monthly-rebalanced book that must trade on formation day pays exactly the part not sampled. Neither REGISTRATION.md Section 7 nor reports/stage_a2/cost_table.md mentions the windows.
  - **Each "cell" is not a 5-minute sample.** `fetch_quotes` requests `&limit={QUOTES_PER_CELL}` = 50 (measure_book_spreads.py:57, 92-110) over the 300-second window with no `sort` parameter and no pagination. The 50 quotes returned are the earliest in the window; for a name like MU (median mid 957.51) that is a fraction of a second of tape, not five minutes.
  - **The hurdle-setting figure rests on n=5 names.** The registered width-5 spread is "13.08 bp at median mid 201.91 USD" (reports/stage_a2/cost_table.md:36). Recomputed from reports/stage_a2/book_spreads.json, the five width-5 names' per-name medians are WOLF 19.604, AXTI 16.764, SNDK 7.450, BE 13.075, LITE 12.471 → median 13.075; mids 26.355/73.05/1595.19/201.91/863.91 → median 201.9075. So the number that sets the registered success bar is the median of five per-name medians, each of which is the median of nine near-instantaneous cells.
  - **Timing and universe.** The book measured is the 2026-07-01 formation, measured 2026-08-19 to 21 — seven weeks after formation, on a book the repository's own reconciliation says had fallen 28.2 % at the median in the interim (HFExperiment/reports/stage_b1/price_reconciliation.md:10-11). The names actually traded in any future month are different names.
  - **Percentile estimator is a floor index**: `return sorted_vals[int(p * (len(sorted_vals) - 1))]` (measure_book_spreads.py:153-154); at n=20 the reported p75 is the 15th of 20 and p90 the 18th of 20, both biased low. (Small; recorded for completeness.)
  - n: 20 names × 9 cells × ≤50 consecutive quotes, 3 consecutive sessions, 3 fixed intraday instants; the width-5 figure is n=5.
- **Recomputation (if any):** inputs reports/stage_a2/book_spreads.json:17-136; method: median of the five width-5 names' `median_bp` and `median_mid`; results 13.075182298214278 bp and 201.9075 USD, reproducing the registered 13.08 and 201.91 exactly. Median of all 20 `median_mid` = 103.2525, reproducing cost_table.md:3's 103.25.
- **What would resolve it:** a re-measurement including the opening 30 minutes and the closing auction, paginated across the full window, and a statement of the width-5 figure's n.
- **Confidence:** MEDIUM-HIGH — the window constants and the un-paginated limit are in the committed script; the inference that Alpaca returns the earliest 50 quotes rests on that endpoint's documented ascending order, which I could not verify offline.
- **Invalidated by later commits?:** no — measure_book_spreads.py and book_spreads.json are unchanged since a8f4b0d.
- **Disclosed by authors?:** partially, and severity is capped at S3 for it. ADR-013 discloses the route, the sessions and that "Re-measuring near each future formation would change it" (HFExperiment/DECISIONS.md:207-215), and the script docstring names the windows (measure_book_spreads.py:8-9). The exclusion of the open and close, the un-paginated 50-quote cells, and the n=5 basis of the hurdle input appear nowhere in REGISTRATION.md, cost_table.md or progress.md.

---

### AUDIT-B-HFExperiment-10
- **Repository / SHA:** HFExperiment / 82e77a021256d917c665ff6d4304c25b08f35451
- **Hypothesis or artifact:** reports/monitor/verdict.txt — the shipped verdict view's per-width projection
- **Direction:** B
- **Class:** STALE_FIGURE
- **Severity:** S3
- **Label:** DERIVED
- **Claim challenged (verbatim quote):** "width 20 (secondary, alpha 0.025 one-sided, rho 0.071641) ... registered projection at the recorded width-5 mean 27.99 bp/day: clears zero at day 2061, clears the hurdle at day 2852" — HFExperiment/reports/monitor/verdict.txt:13-20 (identical block for width 50 at :22-29)
- **Evidence:**
  - The four constants are hard-coded once and stamped into every width's record: `PROJECTION_MEAN_BP = 27.99`, `PROJECTION_SIGMA_BP = 418.0`, `PROJECTION_CLEAR_ZERO_DAY = 2061`, `PROJECTION_CLEAR_HURDLE_DAY = 2852` (HFExperiment/src/hfexperiment/registered.py:104-107), returned by `registered_projection()` and inserted into `record["projection"]` for every width (HFExperiment/src/hfexperiment/verdictengine.py:38-45, 63).
  - The secondaries' own registered figures are in the Section 4 table: width 20 excess 15.10 bp/day and TE 42.54 %/yr, width 50 excess 10.04 and TE 31.70 (HFExperiment/REGISTRATION.md:113-118), and their alphas are 0.025 (src/hfexperiment/verdict.py:104-116).
  - Recomputed under the same frozen construction with each width's own mean, sigma and alpha: width 20 clears zero at day **3,429** and the 4.07 hurdle at day **6,645**; width 50 at day **4,352** and day **13,178**. The shipped view reports 2,061 / 2,852 under all three headings — understating the secondary horizons by 1.7× and 2.1× on zero-crossing and 2.3× and 4.6× on the hurdle.
  - n: 3 width blocks, 1 projection.
- **Recomputation (if any):** inputs REGISTRATION.md:113-118 (excess and TE per width), registered.py:91 (rho 0.071641), verdict.py:104-116 (alpha per width); method: `acs_radius` and `first_crossing_day` from src/hfexperiment/verdict.py:26-34 and :119-133, reimplemented, sigma_bp = TE%/√252 × 100; results as above. Sanity check at width 5 with the registered sigma 418 reproduces 2061 and 2852 exactly; the derived sigma 66.40/√252×100 = 418.28 gives 2064 and 2856, confirming the registered 418 is the rounded derived value.
- **What would resolve it:** rendering each width's own projection, or removing the projection line from the secondary blocks.
- **Confidence:** HIGH — the constant is hard-coded and the recomputation uses the repository's own registered inputs and its own boundary function.
- **Invalidated by later commits?:** no — the tip touched no code and no report.
- **Disclosed by authors?:** partially, and capped at S3 for it — the line does say "at the recorded width-5 mean 27.99 bp/day", so an attentive reader can see the substitution. It is nonetheless labelled "registered projection" inside a block headed by a different width, and no width-20 or width-50 projection exists anywhere in the repository.

---

### AUDIT-B-HFExperiment-11
- **Repository / SHA:** HFExperiment / 82e77a021256d917c665ff6d4304c25b08f35451
- **Hypothesis or artifact:** the registered multiplicity control across the three verdict widths
- **Direction:** B
- **Class:** STATISTICAL
- **Severity:** S3
- **Label:** READ
- **Claim challenged (verbatim quote):** "Widths 20 and 50 are pre-registered secondaries. The primary spends alpha 0.05 one-sided. The secondaries spend 0.025 each, Bonferroni, so the family never outspends the primary." — HFExperiment/REGISTRATION.md:97-99
- **Evidence:**
  - Three registered one-sided success tests run simultaneously and time-uniformly: `alpha_for_width` returns 0.05 at width 5 and 0.025 at widths 20 and 50 (HFExperiment/src/hfexperiment/verdict.py:104-116), and `recompute_and_append` produces a verdict record for every width on every accrual (HFExperiment/src/hfexperiment/verdictengine.py:114-123). All three are rendered side by side as verdict-bearing blocks in the shipped monitor (HFExperiment/reports/monitor/verdict.txt:4-29).
  - The union bound over the three success tests is 0.05 + 0.025 + 0.025 = **0.10**, twice the level the primary is described as spending. The sentence's "the family" silently excludes the primary from the family it is compared against; the *secondary* family spends 0.05, equal to the primary, and the experiment-wise budget is 0.10.
  - The same narrower reading is registered in the code comment: "The primary spends alpha 0.05. The secondaries split 0.05 between them, Bonferroni, so the family never spends more than the primary." (verdict.py:108-110). No experiment-wise figure appears anywhere in the repository.
  - n: 3 registered widths, 1 primary + 2 secondaries.
- **Recomputation (if any):** union bound only: 0.05 + 0.025 + 0.025 = 0.10.
- **What would resolve it:** stating the experiment-wise level as 0.10, or splitting 0.05 across all three (e.g. 0.025 / 0.0125 / 0.0125).
- **Confidence:** MEDIUM-HIGH — the arithmetic is not in dispute; the defence would be that only width 5 may declare the verdict, but Section 4 registers the secondaries as verdict-bearing at their own alphas and the monitor renders all three with success and futility bars.
- **Invalidated by later commits?:** no.
- **Disclosed by authors?:** no. The sentence quoted is itself the claim of multiplicity control.

---

### AUDIT-B-HFExperiment-12
- **Repository / SHA:** HFExperiment / 82e77a021256d917c665ff6d4304c25b08f35451
- **Hypothesis or artifact:** the DEGRADED branch of the Section 0 broker outcome map — when its consequence was written
- **Direction:** B
- **Class:** PROCESS
- **Severity:** S3
- **Label:** DERIVED
- **Claim challenged (verbatim quote):** "The registered consequence of a DEGRADED Task 3 result is therefore NO live sleeve at this stake, not a reduced one." — HFExperiment/REGISTRATION.md:156-157
- **Evidence:**
  - What Section 0 actually registered, before measurement: "Consequence, registered now: per-name notional rises to whole-share size. Book width falls to what 900 USD supports at that size." (HFExperiment/REGISTRATION.md:25-27) — a *reduced* sleeve, explicitly. Section 0 is the part committed early: c4e98177334d31758c4c3796a216de6d620f6e89, 2026-08-23T22:23:16Z, "docs: register broker outcome map before any measurement", `--numstat` REGISTRATION.md 49/0 and nothing else.
  - The deciding input landed in the very next commit, 0a0d214b, 2026-08-23T22:42:34Z, which contains reports/stage_a1/formations.md (70/0) and formations.json (3279/0) with the median share prices.
  - The re-specified consequence landed in a8f4b0d1, **2026-08-24T04:40:25Z** — six hours after the measurement existed — as part of the Sections 1-12 append (REGISTRATION.md 235/0). So the sentence quoted describes a rule written after its own deciding measurement, while calling it "the registered consequence".
  - The re-specification is a one-way ratchet: "A collapse in book share prices does not reopen it, because the branch decision must not track the thing it sizes." (HFExperiment/DECISIONS.md:202-203). The measured input the branch closed on is itself unstable in the repository's own record — the width-20 median ran 36.47 (2026-03-02) and 40.59 (2026-04-01) before 143.80 and 143.89 (reports/stage_a1/formations.md:22-28) — and at 36.47 a 20-name whole-share basket is affordable at the 900 USD stake. High prices close the branch permanently; low prices may not reopen it.
  - n: 7 recorded formations of median book price; 2 used to close the branch ("144 USD at the last two formations", REGISTRATION.md:150).
- **Recomputation (if any):** commit-interval arithmetic from `git log --date=iso-strict`: c4e9817 → 0a0d214 = 19 min 18 s; 0a0d214 → a8f4b0d = 5 h 57 min 51 s.
- **What would resolve it:** labelling Section 6 as an amendment to Section 0's DEGRADED consequence, dated, with the data that existed — the discipline Section 12 requires of amendments (REGISTRATION.md:271-272) and which Section 6 does not follow.
- **Confidence:** HIGH on the sequence (commit timestamps are git objects); MEDIUM on materiality, since a reduced sleeve at 144 USD/share is close to no sleeve and the branch never ran.
- **Invalidated by later commits?:** no.
- **Disclosed by authors?:** partially, and capped at S3 for it — Section 6 openly says "Section 0 left DEGRADED open pending the median share price of the book. A.1 measured it" (REGISTRATION.md:149-150). What is not said is that Section 0's own registered consequence was different, and the word "registered" in the quoted sentence obscures it.

---

### AUDIT-B-HFExperiment-13
- **Repository / SHA:** HFExperiment / 82e77a021256d917c665ff6d4304c25b08f35451
- **Hypothesis or artifact:** Section 9's registered kill floor arithmetic
- **Direction:** B
- **Class:** ARITHMETIC
- **Severity:** S3
- **Label:** READ
- **Claim challenged (verbatim quote):** "The floor is 500 USD of total account equity, a 400 USD loss on 900 deployed after the 100 buffer, 1.31 sigma of the width-20 tracking error, driftless touch probability near 19 percent in year one." — HFExperiment/REGISTRATION.md:216-218
- **Evidence:**
  - The three quantities in that sentence are mutually inconsistent. A 400 USD loss on 900 deployed is 44.44 %, which at the interpolated width-20 TE of 42.54 %/yr (REGISTRATION.md:117) is **1.045 sigma**, driftless one-year touch probability **29.6 %** — not 1.31 sigma and 19 %.
  - 1.31 sigma and 19 % require a **500** USD loss: 500/900 = 55.56 %; 55.56/42.54 = 1.306 sigma; 2Φ(−1.306) = 19.2 %. That is the correct reading of a 500 USD *equity* floor on a 1,000 USD account (REGISTRATION.md:133), and it is what the code records: "500 is 1.31 sigma of the width-20 annual tracking error on 900 deployed, driftless touch probability near 19 percent in year one" (HFExperiment/src/hfexperiment/registered.py:53-55), with no "400 USD loss".
  - The figure the sentence states, 1.045 sigma / 30 %, is exactly what ADR-011 assigns to the **rejected** 600 USD floor: "at width 20's interpolated 42.54 percent tracking error, 600 is 1.04 sigma with a driftless touch probability near 30 percent" (HFExperiment/DECISIONS.md:173-176). So the binding registration's justification for the chosen floor states the loss figure of the floor it rejected.
  - n: 3 candidate floors (600/500/400), 1 sentence.
- **Recomputation (if any):** inputs REGISTRATION.md:117 (TE 42.54 %/yr) and REGISTRATION.md:133 (900 deployed, 100 buffer) — both figures printed in the document, which is why this finding is labelled READ; method: k = (1000 − floor)/900 / 0.4254, touch = 2Φ(−k) by the reflection principle for driftless Brownian motion over one year; results — floor 600 → 1.045σ, 29.61 %; floor 500 → 1.306σ, 19.16 %; floor 400 → 1.567σ, 11.71 %. These reproduce ADR-011's 1.04/30, 1.31/19 and 1.57/12 exactly, confirming both the method and that the correct loss for the 500 floor is 500, not 400.
- **What would resolve it:** correcting "a 400 USD loss" to "a 500 USD loss" in REGISTRATION.md:216-217.
- **Confidence:** MEDIUM-HIGH — the recomputation is exact and matches ADR-011's own numbers; the residual doubt is only whether "a 400 USD loss" was meant as "leaving 400 of the 900", which the words do not say. Kept at S3 rather than S2 because no figure downstream consumes it: the chosen floor, its sigma and its touch probability are all correct everywhere else.
- **Invalidated by later commits?:** no.
- **Disclosed by authors?:** no; no erratum exists.

---

### AUDIT-B-HFExperiment-14
- **Repository / SHA:** HFExperiment / 82e77a021256d917c665ff6d4304c25b08f35451
- **Hypothesis or artifact:** README.md — the repository's front door
- **Direction:** B
- **Class:** PROCESS
- **Severity:** S3
- **Label:** READ
- **Claim challenged (verbatim quote):** "This repository runs two series. / The SHADOW series is the signal instrument. The registered book computed daily from price data alone. No fills. No commissions. It accumulates the statistics the verdict reads. / The LIVE series is the execution instrument. Actual fills at a real broker at micro size. It measures what the shadow series cannot. / The difference between the two is the execution cost, measured directly." — HFExperiment/README.md:7-16
- **Evidence:**
  - Neither series exists. "The shadow series was disarmed before its first accrual ... The verdict was never computed. Closure is terminal." and "zero shadow observations, because the series never started" (HFExperiment/REGISTRATION.md:310-315). "The live track was never funded and zero capital was deployed" (REGISTRATION.md:309-310). "Section 0 fires BLOCKED ... phases C and D stop" (HFExperiment/reports/stage_a1b/a1b_report.md:107-113).
  - README.md is unchanged since 0a0d214b (2026-08-23T22:42:34Z, `--numstat` README.md 27/0; `git log -- README.md` returns that commit alone), i.e. it predates the BLOCKED verdict, the closure and ADR-026. It contains no closure line, no BLOCKED line and no "zero observations" line; a reader who reads only the README takes away a running two-series experiment with a measured execution cost.
  - "The difference between the two is the execution cost, measured directly" (README.md:16) is the strongest single claim in the repository and nothing was ever measured: 0 fills, 0 commissions observed (a1b_report.md:96-98), 0 shadow observations.
  - Corroborating (UNANCHORED, live tree read 2026-09-04T00:09Z): `data/bars.db` has 0 rows in all six tables and `data/ledger/` is empty.
  - n: 27-line README, 0 of 2 series ever run.
- **Recomputation (if any):** none.
- **What would resolve it:** a closure header on README.md pointing at REGISTRATION.md's amendment log.
- **Confidence:** HIGH — the README text and the closure text are both plain, and the git history shows the README was never revisited.
- **Invalidated by later commits?:** no — README.md is untouched at the anchor.
- **Disclosed by authors?:** yes, elsewhere — the closure is disclosed at REGISTRATION.md:306-315 and progress.md:5-21. The finding is that it is absent from the artifact most likely to be read first and quoted onward. Capped at S3 accordingly.

---

### AUDIT-B-HFExperiment-15
- **Repository / SHA:** HFExperiment / 82e77a021256d917c665ff6d4304c25b08f35451
- **Hypothesis or artifact:** ADR-026's scope claim, and the third surviving instance of the stale no-account blocker
- **Direction:** B
- **Class:** STALE_FIGURE
- **Severity:** S3
- **Label:** DERIVED
- **Claim challenged (verbatim quote):** "Two documents carried a claim the repository's own evidence had already overtaken." — HFExperiment/DECISIONS.md:434
- **Evidence:**
  - A third site carries it at the anchored SHA, in code, uncorrected: the reason string for a registered deferred parameter reads "MinSize and SizeIncrement come from reqContractDetails on a **live-permissioned account that does not exist yet**" — HFExperiment/src/hfexperiment/registered.py:119-120.
  - It is stale twice over. The account exists (docs/ACCESS.md:187-189, the ADR-026 replacement text). And the data the parameter waits on was already collected: "all 20 names of the 2026-08-03 width-20 book advertise MinSize 0.0001 and SizeIncrement 0.0001" (docs/ACCESS.md:196; the 20 `contract_details` records are reports/stage_a1b/evidence.jsonl:3-22).
  - The string is not decoration: it is the text the order gate prints on refusal, and it is quoted verbatim into the C.1 evidence ledger for the parameter that gates every intent (HFExperiment/reports/stage_c1/refusals.md:17, 23 quote the sibling `per_name_notional_usd` reason in the same shape).
  - n: 3 sites of the stale claim, 2 corrected by ADR-026, 1 left.
- **Recomputation (if any):** none; a grep of the snapshot for the phrase returns src/hfexperiment/registered.py:120 only.
- **What would resolve it:** correcting the reason string, or an ADR-026 note that the code site was deliberately left.
- **Confidence:** HIGH — the string is in the anchored source and the ADR's count is explicit.
- **Invalidated by later commits?:** no — 82e77a0 is the tip and touched no code (`--numstat`: DECISIONS.md 60/0, docs/ACCESS.md 47/19, progress.md 48/0), which is itself the point: ADR-026 describes itself as "A record-hygiene amendment ... touching two documents and no code" (progress.md:228-229).
- **Disclosed by authors?:** no.

---

### AUDIT-B-HFExperiment-16
- **Repository / SHA:** HFExperiment / 82e77a021256d917c665ff6d4304c25b08f35451
- **Hypothesis or artifact:** the inherited effect size 27.99 bp/day and everything derived from it — the primary-width choice, IR 1.062, the 2,061/2,852-day projection, the 0.15 prior, and the decision to proceed
- **Direction:** B
- **Class:** UNSUPPORTED_POSITIVE
- **Severity:** S3
- **Label:** READ
- **Claim challenged (verbatim quote):** "the effect, measured at 27.99 bp per day on the already-spent holdout, exceeds the 4.07 bp per day that round-trip costs consume at the measured 40 percent monthly churn, so a fee-paying participant keeps most of it." — HFExperiment/REGISTRATION.md:53-56. And "Universe rule U-LIQ-500-stk-w60-m40-p5, copied verbatim from the recorded round and reproduced by Stage A.1 against all 124 recorded formation dates." — HFExperiment/REGISTRATION.md:78-80.
- **Evidence:**
  - The reproduction gate never checked a book. "The recorded formation books at widths 5 and 50 are not stored in the permitted database, so the disagreement gate ran against the recorded universe membership instead" (HFExperiment/DECISIONS.md:106-108). The stored artifact confirms it: every row of reports/stage_a1/universe_check.json is a 500-row *universe* comparison at 10 dates, with no book, momentum or rank comparison anywhere; reports/stage_a1/reproduce_log.txt:4-20 shows `universe ...: exact_match=True` for 10 dates and `formation ...: N ranked` — formed, never compared.
  - The ranking itself was re-implemented from prose: "The recorded round's formation code is outside the two permitted read paths, so the 12-1 ranking is implemented from its registered description" (DECISIONS.md:99-101), with five conventions "fixed here" (anchor placement, close selection, a 20-session gap rule, one listing segment — DECISIONS.md:102-105).
  - The benchmark was likewise assumed, not verified: benchmark.py asserts its construction is "the benchmark the recorded cross-sectional round of 2026-07-26 ran and the one that produced the recorded 27.99 bp per day at width 5" (HFExperiment/src/hfexperiment/benchmark.py:6-8) and fixes it as a daily-rebalanced arithmetic mean over the 500 members (benchmark.py:8-13). Nothing in the repository verifies that the recorded round rebalanced daily rather than holding equal weights from formation; the choice is material to the level of daily excess return.
  - The primary width was selected on the maximum of the same spent holdout — "Width 5 is the PRIMARY width for the verdict. It carries the highest recorded information ratio, 1.062" (REGISTRATION.md:92-93) — and the 27.99 that carries the power projection is that maximum, with no shrinkage for having been selected over the recorded widths.
  - Widths 10 and 20 in the same table are a two-point power-law fit, i.e. two parameters through two points, zero residual degrees of freedom and no uncertainty: TE exponent −0.321 and excess exponent −0.445 (REGISTRATION.md:110-118). Recomputed from the two recorded rows: −0.3211 and −0.4453, exact. The kill floor's sigma and touch probabilities are then derived from the *interpolated* width-20 TE of 42.54 (DECISIONS.md:172-179).
  - n: 124 formation dates for the universe; 10 dates × 500 rows compared; **0** recorded books compared; 2 recorded width points behind a 4-row width table.
- **Recomputation (if any):** two-point log-log fit on (5, 66.40) and (50, 31.70) → −0.3211; on (5, 27.99) and (50, 10.04) → −0.4453; IR₅ = 27.99×252/100/66.40 = 1.0623; IR₅₀ = 0.7981; (1.062/0.894)² = 1.4112. All inputs are figures printed in REGISTRATION.md:113-118, which is why this finding is labelled READ.
- **What would resolve it:** a comparison of at least one reproduced width-5 and width-50 book against the recorded round's stored books, and a statement of the recorded round's benchmark rebalancing convention.
- **Confidence:** MEDIUM-HIGH — the arithmetic downstream of 27.99 is exact; what is unverified is that the shadow series would have measured the same strategy as the one that produced 27.99.
- **Invalidated by later commits?:** no.
- **Disclosed by authors?:** yes, in part and plainly — ADR-006 (DECISIONS.md:97-114) discloses both the unavailable formation code and the substitution of universe membership for books, and REGISTRATION.md:53 and :92-95 label the holdout "already-spent". Reported as READ and capped at S3 for that reason. What is *not* disclosed is that the benchmark convention is an assumption about the recorded round, and that the width-5 selection maximum is used un-shrunk as the power input.

---

### AUDIT-B-HFExperiment-17
- **Repository / SHA:** HFExperiment / 82e77a021256d917c665ff6d4304c25b08f35451
- **Hypothesis or artifact:** the append-only decision and progress records
- **Direction:** B
- **Class:** PROVENANCE
- **Severity:** S4
- **Label:** READ
- **Claim challenged (verbatim quote):** "Numbered ADRs, append-only. Each records the decision, the reason, and what would change it." — HFExperiment/DECISIONS.md:3-4; and "Append-only. One dated entry per stage, newest at top." — HFExperiment/progress.md:3
- **Evidence:**
  - **ADR numbering gap.** DECISIONS.md runs ADR-001 … ADR-022 (heading at :401), then jumps to ADR-026 (heading at :432). A grep of the whole snapshot for `ADR-0[0-9][0-9]` returns 23 distinct identifiers, ADR-001 through ADR-022 plus ADR-026: no ADR-023, ADR-024 or ADR-025 in any file, defined or referenced. Three numbers in a numbered append-only log are unaccounted for, with no gap note.
  - **Ordering violated at the tip.** progress.md declares "newest at top" (line 3) and its newest entry, "## 2026-08-28T22:10Z — ADR-026", sits at line 226 of 271 — below the oldest stage entry, "## 2026-08-23: Stage A.1" at progress.md:187. A reader scanning from the top sees the 2026-08-26 closure (progress.md:5) as the last word and can miss the 2026-08-28 correction entirely.
  - n: 3 missing ADR numbers out of 26; 1 of 7 progress entries out of the declared order.
- **Recomputation (if any):** none.
- **What would resolve it:** a one-line note explaining the ADR gap, and moving the ADR-026 entry to the top.
- **Confidence:** HIGH on the facts; the ADR gap may be explained outside this repository (e.g. a program-wide numbering shared with a sibling repository), which is exactly what the record should say and does not.
- **Invalidated by later commits?:** no — both were introduced by the tip commit's edits or left standing by it.
- **Disclosed by authors?:** no.

---

### AUDIT-B-HFExperiment-18
- **Repository / SHA:** HFExperiment / 82e77a021256d917c665ff6d4304c25b08f35451
- **Hypothesis or artifact:** src/hfexperiment/commission.py — the shipped commission model behind docs/ACCESS.md's and cost_table.md's tables
- **Direction:** B
- **Class:** ARITHMETIC
- **Severity:** S4
- **Label:** DERIVED
- **Claim challenged (verbatim quote):** "The cap-below-minimum branch is the load-bearing one: below the crossover notional the cap is less than the minimum and the cap is assessed. Removing that branch must fail tests/test_commission.py." — HFExperiment/src/hfexperiment/commission.py:67-69
- **Evidence:**
  - `commission()` implements `if cap < plan.min_per_order_usd: return cap; if calculated < plan.min_per_order_usd: return minimum; return calculated` (HFExperiment/src/hfexperiment/commission.py:73-79). The final branch returns the per-share amount **uncapped**. IBKR's rule as quoted in the repository's own source is a cap on every order ("the maximum per order as 1 pct of trade value for both plans", HFExperiment/docs/ACCESS.md:60-64), i.e. `min(max(calculated, minimum), cap)`.
  - The omitted branch binds when `calculated > cap ≥ min`, i.e. when `shares/value > cap_pct/per_share` = 0.005/0.0035 = 1.4286 for Tiered, that is at share prices below **0.70 USD** (Fixed: 0.01/0.005 = 2.0, below 0.50 USD).
  - Immaterial for this repository because the universe rule floors the median close at 5 USD: `MIN_MEDIAN_CLOSE = 5.0        # USD. Penny-stock floor, measured IN the window` (HFExperiment/src/hfexperiment/universe.py:42), enforced at universe.py:182-183. The minimum `last_close` across all 7 recorded formations at any width is 4.68 (OPEN, 2026-04-01; reports/stage_a1/formations.json), still 6.7× the trigger.
  - n: 15 published table rows across docs/ACCESS.md:127-141 and reports/stage_a2/cost_table.md:7-21, none of which touches the missing branch.
- **Recomputation (if any):** crossover for the missing branch: Tiered `shares × 0.0035 > value × 0.005` ⇔ price < 0.70 USD; Fixed ⇔ price < 0.50 USD. Every published row is priced at 30-180 USD notional on names above 4.68 USD, so no published row changes.
- **What would resolve it:** returning `min(calculated, cap)` on the final branch, with a test at a sub-dollar price.
- **Confidence:** HIGH on the code path; the finding is explicitly immaterial to every number the repository publishes, and is recorded because the module is a candidate for reuse in a successor repository whose universe may not carry a 5 USD floor.
- **Invalidated by later commits?:** no.
- **Disclosed by authors?:** no.

---

## What Agent B checked and found sound

Read completely: README.md, REGISTRATION.md, DECISIONS.md, progress.md, docs/ACCESS.md, all six report
markdown files, all four mutation_tests.txt, both monitor renders, all five JSON/JSONL evidence artifacts,
all six scripts, and all 24 modules under src/hfexperiment/. Where the thesis did not hold:

- **Every headline arithmetic figure reproduces exactly.** rho tuned by golden-section at 1,600 days and
  alpha 0.05 → 0.07164133 against the registered 0.071641 (src/hfexperiment/registered.py:91); clear-zero
  day 2061 and clear-hurdle day 2852 (registered.py:106-107); pointwise n = (1.645 × 418/27.99)² = 603.5
  against "about 600 days" (REGISTRATION.md:257); hurdle 4.0731 → 4.07 (reports/stage_a2/cost_table.md:36);
  round trip 213.836 → 213.84; the annual-drag rows (28.08/56.16/16.80/48.00/86.40 commission USD/yr,
  cost_table.md:27-32) all reproduce from `costmodel.annual_commission_drag`; power-law exponents
  −0.3211/−0.4453 → −0.321/−0.445; IR 1.0623 → 1.062 and 0.7981 → 0.798; time ratio 1.4112 → 1.41; churn
  (4+3+1+1+2+1)/6 = 2.0 and (8+6+5+5+2+5)/6 = 5.167 → 5.2 (reports/stage_a1/formations.md:11-16); fill rates
  4.0 and 10.4, and 200/10.4 = 19.2 months against "about 19 months" (REGISTRATION.md:101-103); touch
  probabilities 29.6/19.2/11.7 % → 30/19/12 (DECISIONS.md:173-179); median of the 20 A.2 mids = 103.2525 →
  103.25; width-5 spread 13.0752 → 13.08 and mid 201.9075 → 201.91. Nothing is rounded in a favourable
  direction anywhere I checked.
- **Test-count claims are exact.** Counting `def test_` under tests/ at each stage commit: 91a1dcb → 27,
  23d9ffa → 76, 8c4c3bc → 123, b4a7a23 → 158, matching progress.md:218, :179, :141 and :92 respectively. I
  did not run the suite (running an audited repository's own tests in place is out of bounds), so "green" is
  not independently verified, but the counts are not inflated.
- **REGISTRATION.md was never edited above the amendment log.** `git log --numstat -- REGISTRATION.md` shows
  five commits: c4e9817 (49/0, Section 0), a8f4b0d (235/0, Sections 1-12, zero deletions), 8c4c3bc (12/1,
  where the single deletion is the line "Append-only. No entries yet."), 669eb5c (9/0, the BLOCKED
  amendment), f13e1d3 (11/0, the closure amendment). The "amendments append, nothing edits in place"
  discipline holds for this file.
- **The pre-registration ordering claim holds at commit granularity.** Section 0 landed at c4e9817
  (2026-08-23T22:23:16Z) 19 min 18 s before the A.1 evidence commit 0a0d214. Progress records A.1's actual
  duration as 25 minutes (progress.md:189), so Section 0 was committed roughly four minutes into the stage —
  tight but consistent. That commit contains REGISTRATION.md and nothing else, which is what "before any
  broker measurement" requires of it.
- **The "zero shadow observations" claim is true in the data.** UNANCHORED, live tree read 2026-09-04T00:09Z:
  data/bars.db holds 0 bars, 0 sessions, 0 assets, 0 universe rows, 0 formations, 0 fetch_log rows;
  data/ledger/ is empty. Nothing was fabricated to fill the gap. data/c1_formation.db (894,420 bars, 682
  sessions, 500 universe rows, 75 formations) is a real, separately-owned store, as ADR-021 says.
- **The universe reproduction artifact says what the log says.** reports/stage_a1/reproduce_log.txt:1
  ("reproduced 124, recorded 124, identical=True"), 10 `exact_match=True` universe lines at :4-19, and
  ":21 ALL UNIVERSE CHECKS EXACT: True"; the DB hash is identical before and after
  (reports/stage_a1/db_hash_before.txt, db_hash_after.txt). The gap is what was *not* compared (books), which
  ADR-006 discloses and AUDIT-B-HFExperiment-16 records; the claim as stated about universes is sound.
- **ADR-016's fresh-adjustment design is honoured in code, not just asserted.** Every bar query carries
  `&timeframe=1Day&adjustment=all&feed=sip` (alpaca_source.py:142); the store schema carries `adjustment` and
  `queried_utc` columns and only INSERTs (barstore.py:28, 105-113); formationrun.py re-queries the full
  trailing window rather than reading stored history (formationrun.py:1-9).
- **The universe module is hindsight-clean where it matters.** Membership is decided from bars strictly
  before the formation date (universe.py:239-250), the trailing window ends the session before formation, the
  fund classifier is tri-state and fails closed on unknown instruments (universe.py:78-102, 186-194) with the
  prior failure mode documented in the docstring, and the one non-point-in-time input (present-day instrument
  name) is stated rather than hidden (universe.py:26-29).
- **The kill-criteria module enforces the restart/termination distinction it registers** (kill.py:29-47), and
  unknown stop events raise rather than defaulting.
- **The SUCCESS/FUTILITY overlap I suspected is unreachable.** `classify_verdict` checks SUCCESS before
  FUTILITY (verdict.py:97-101), so in the region `lower > 4.07 and upper < 10` it would declare SUCCESS on an
  unregistered tie-break. That region needs a radius below (10 − 4.07)/2 = 2.965 bp, and at the registered
  sigma of 418 bp the radius is still 16.9 bp at day 6,000. Not a finding.
- **The 28 % book drawdown is disclosed, and I could not turn it into evidence against the hypothesis.**
  reports/stage_b1/price_reconciliation.md:10-11 and :65-70 record that the 2026-07-01 width-20 book fell
  28.2 % at the median by 2026-08-21 and attribute it to a correlated selloff. That is a genuine
  out-of-sample observation on the registered book and the repository treats it purely as a data-hygiene
  check, but without the equal-weighted universe's return over the same window it says nothing about excess
  return, and no such benchmark figure exists in the repository. Recorded as an uncollected check, not a
  finding.
- **The spend cap, the eight refusals, the intent construction wall and the account pin** all behave as
  documented in reports/stage_c1/refusals.md, and the rolling-year query correctly excludes the 2025-08-10
  record (refusals.md:133-135). The connectivity probe genuinely cannot encode an order message
  (ibkrprobe.py, ADR-019).
- **Discard taxonomy in the spread measurement is conservative**, not favourable: locked (zero-spread) and
  crossed quotes are discarded (measure_book_spreads.py:121-127), which biases the median *up*; 88 locked and
  6 crossed out of up to 9,000 quotes (reports/stage_a2/book_spreads.json:148-156).
- **The interpolated width rows are labelled as interpolated everywhere they appear** (REGISTRATION.md:116-117,
  DECISIONS.md ADR-009), and the anomalous TE exponent is registered as a risk rather than smoothed away
  (REGISTRATION.md:124-129).

What I would have expected to find if the thesis held more strongly than it does: a shadow observation series
with cherry-picked start dates, a verdict computed and reported, a hurdle quietly lowered after the BLOCKED
verdict, or arithmetic that rounds toward the hypothesis. None of those exist. The repository's failures are
failures of *warrant in wording* and of *record hygiene*, not of fabricated results — because there are no
results.

## Dropped at consolidation

Nothing was dropped for want of a locatable quote, a figure or an n: all 18 draft findings carry a verbatim
quote with file:line, deciding figures and a stated n, and all 18 survive. Because this repository was
audited in a single draft pass ("all"), there were no cross-part duplicates to merge. What changed at
consolidation:

- **Dropped before consolidation, recorded here for completeness** (candidates that failed the evidence bar
  and are reported instead in "What Agent B checked and found sound"): the SUCCESS-before-FUTILITY tie-break
  (unreachable at the registered sigma — no failure mode exists to quote); the 28 % book drawdown as evidence
  against the signal (no benchmark return exists in the repository, so there is no figure); `universe.py`'s
  docstring pointing at a `tests/test_universe_rule.py` that does not exist here (cosmetic, verbatim copy
  from AiTrader, no claim rests on it).
- **Two severities changed from the draft.** The whole-share control order (now AUDIT-B-HFExperiment-1) was
  raised S2 → **S1**: the stated conclusions "Read-Only is off" and "the fractional refusals are specific to
  fractional sizing" have no evidence produced by any committed code, and the binding BLOCKED amendment cites
  them. The Section 6 basket arithmetic (now -5) was raised S3 → **S2** for consistency with the server-version
  finding: a registered figure that contradicts the repository's own stored artifact is a label contradicting
  its own evidence. The kill-floor slip (-13) was deliberately *kept* at S3 despite the same shape, because
  nothing downstream consumes the wrong figure.
- **Two labels corrected DERIVED → READ** under the rule that a recomputation from figures printed in a
  document is READ: the kill floor (-13, inputs TE 42.54 and 900/100 from REGISTRATION.md:117 and :133) and
  the ADR numbering/ordering finding (-17, evidence is a grep of two documents).
- **Four factual corrections to draft text**, made after re-checking git objects and the snapshot:
  (a) the draft said `git log -p` returned one "control" hit "inside a docstring/comment" — in fact **no
  revision of scripts/a1b_capability_test.py contains the string at all**, and the single hit is in the
  commit message of 669eb5c; the finding is stronger, not weaker;
  (b) the tip commit's docs/ACCESS.md change is **47 insertions / 19 deletions** (`--numstat`), not "66
  insertions, 19 deletions" as drafted (66 was the diffstat bar width);
  (c) 8c4c3bc's REGISTRATION.md change is **12/1**, not "+13/−1";
  (d) three line citations were tightened to the exact span of the quoted words: the amendment-discipline rule
  is REGISTRATION.md:271-272 (not :266-268), the kill-floor sentence is :216-218 (not :216-219), and the
  27.99 sentence is :53-56 (not :52-56). One under-statement was corrected upward: the monitor projection
  understates the width-50 zero-crossing by 2.1×, not 2.3× (4,352/2,061).
- **One draft claim narrowed.** The server-version finding said "four further narrative sites"; progress.md:80
  also prints 187 but describes the C.1 probe, where 187 is correct, so it is named and excluded rather than
  counted.

## Live-repo access log

Before first access (`git -C /home/kiros-li/Documents/GitHub/HFExperiment status --porcelain`,
2026-09-04T00:08Z, draft pass):

```
?? Accept:
?? GET
?? Host:
?? User-Agent:
```

After last access of the draft pass (same command, 2026-09-04T00:11:54Z):

```
?? Accept:
?? GET
?? Host:
?? User-Agent:
```

Before first access of the consolidation pass (same command, 2026-09-04T00:23:20Z):

```
?? Accept:
?? GET
?? Host:
?? User-Agent:
```

After last access of the consolidation pass (same command, 2026-09-04T00:26:16Z):

```
?? Accept:
?? GET
?? Host:
?? User-Agent:
```

Identical at all four readings, and identical to the pre-existing dirt the common rules record for this
repository (`?? Accept:`, `?? GET`, `?? Host:`, `?? User-Agent:` — the owner's stray files). No other entry
appeared at any point. Live-repo operations used, all read-only: `git log`, `git log -p`, `git log --numstat`,
`git show`, `git show --stat`, `git show --numstat`, `git show <sha>:<path>`, `git grep`, `git ls-tree`,
`git status --porcelain`, `ls`, `cat` of the untracked `_CLOSED_DO_NOT_RUN_HERE` marker, and read-only SQLite
(`file:...?mode=ro`) opens of `data/bars.db` and `data/c1_formation.db`. `.env` was present in the working
tree and was **not** opened. Nothing was written anywhere under the audited path. All scratch computation ran
under the scratchpad work directory against files copied or read from SNAP/HFExperiment.
