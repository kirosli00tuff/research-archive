# POSITIVES LEDGER — PMExperiment (Agent B, consolidated)

**Repository:** PMExperiment / `03d16e71dbf25a86c529884662d02136f8e82334` (main, 2026-09-02,
closed project). Snapshot: `/home/kiros-li/.cache/program-audit/scratchpad/snap/PMExperiment/`.
Merged and de-duplicated from the two draft ledgers (`p1-register`, `p2-progress`). Commit dates
are from the live repository's git log, converted from the recorded −07:00 offset to UTC.
**This ledger is factual, not advocacy.**

**The fact that frames every row:** the power gate never fired, on any venue, over any region;
no contract was enumerated; no price bucket, no dispersion and no statistic relating a price to
an outcome exists (PMExperiment/README.md:13-14; PMExperiment/REGISTRATION.md:588-591;
PMExperiment/progress.md:1547-1549). There is therefore **one** substantive quantitative verdict
in this repository (BAND-OPEN); everything else is an access or licence state, a shipped
procedure, or a closure label.

---

## 1. Positives and qualified positives

### 1.1 BAND-OPEN — the only positive verdict

| field | content |
|---|---|
| **kind** | qualified positive |
| **claim as stated** | "**In one sentence: BAND-OPEN — a surviving region exists that the permitted subset admits, at entry prices 91–99c held to resolution, requiring 5.85 points of underpricing at the registered FX turnover against a registered band whose top is 8.00 points.**" — REGISTRATION.md:409-412. Evidence-document form at docs/BAND.md:15-18; verdict sentence progress.md:362-368; carried at report.md:61-65, README.md:139-141, HYPOTHESES.md:130-133 |
| **deciding figures (n)** | R_H(0.950) = **0.0585** required vs registered band top **0.0800**; surviving margin **0.0215** = "the top 2.15 of a 6-point band". Range over the region 0.0573 at 91c → 0.0597 at 99c. Survival count **10 of 10** deciles on both routes at k = 1, 12, →∞ (docs/BAND.md:233, REGISTRATION.md:416). Band bottom 0.0200 unreachable everywhere: fee + half-spread alone = **0.0300** (docs/BAND.md:241-246). Magnitudes actually cited at 91–99c: **0.020** and **0.030**, n = 313,972 contract prices on 46,282 contracts across 12,403 events (Bürgi) — **both fail** (docs/BAND.md:247-252). Band top's source: Krause **0.077**, **n not recorded** (docs/BAND.md:155, :335-336) |
| **file:line** | REGISTRATION.md:402-459; docs/BAND.md:13-25, :298-338; progress.md:360-368, :476-489; report.md:59-137; HYPOTHESES.md:119-160; README.md:137-149 |
| **bar + registration date** | Effect band **0.02–0.08** registered in Section 3 (REGISTRATION.md:221-256), committed `9080186` **2026-08-29T07:37:33Z**, before any request. Cost model Sections 2 and 11 in the same commit. Verdict rows registered in **Amendment 2** (REGISTRATION.md:736-745), stamped "Made 2026-08-30" but committed `f686036` **2026-08-29T18:05:26Z** — 79 minutes before the verdict fired (`32dc10a` 19:24:06Z) |
| **amendments touching the bar (date, data existed?)** | **Amendment 2** (verdict rows + the two exit routes) — committed 2026-08-29T18:05Z; **no data existed; no venue had been read and none ever was**. **Amendment 4** (FX turnover k; `FX(p)=0.03·p/k`) — `4d75f66` 2026-08-29T19:17:21Z, 7 minutes before the verdict; binds k = 1, the treatment that biases *toward* BAND-EMPTY. **Amendment 5** (volume floor ≥ $1,000) — `f789079` 2026-08-30T03:34:00Z, after the verdict, never exercised. Sections 0–14 are **byte-identical** from `9080186` to the anchor (diff exit 0, 367 lines), so no registered value was edited in place |
| **corrections applied** | Unit determination checked both ways against the register's own printed numbers (ADR-009, DECISIONS.md:208-271; docs/BAND.md:120-143). Direction correction — every registered magnitude restated at its exploitable entry price, 0.883–0.950 (docs/BAND.md:145-159). Both FX turnover readings reported with k = 1 binding and never substituted (Amendment 4 / ADR-010). Two FX-base simplifications quantified at 0.0015 + 0.00045 = **0.00195** and used to exclude route X (docs/BAND.md:181-187, :261-265). Both quantifier readings reported in the working document (docs/BAND.md:229-237). **Not applied:** multiplicity (one verdict), clustering (Section 8 defers it, REGISTRATION.md:293-295), any live verification of an effect-band source (standing rule 4, CLAUDE.md:25-26) |
| **framing in README / report / register** | README.md:143-145 "**It is a cost finding computed from registered constants with no calibration measurement behind it. It must not be written anywhere as evidence that an edge exists.**"; report.md:113 "**So BAND-OPEN is a thin verdict, and it is reported as one.**"; REGISTRATION.md:431-446 three qualifications "not separable from it"; HYPOTHESES.md:147-151 the same refusal, pinned by tests/test_honesty.py:226-232. The caveat travels intact into every conclusion-bearing document |
| **audit flags** | AUDIT-B-PMExperiment-1 (95–99c of the fired region is arithmetically empty; at the 0.950 midpoint the ceiling is 0.0500 against a requirement of 0.0585); -3 (the 10/10 count applies the band at eight deciles where the same page says supplying a magnitude would violate standing rule 5; 2/2 inside the registered cell); -5 (BAND-NARROW excluded by resolving an unevaluable clause permissively and by importing a category attribution from an excluded bucket); -8 (the band top has no n and its source's exploitable price is 0.883, outside the fired cell); -10 (the strict quantifier reading, BAND-EMPTY at 0/10, never travels into the four conclusion documents); -13 (5.85 carried forward as the region-wide requirement) |

### 1.2 "Stage D was wrong in the exact way Stage D said it might be" — a methodological positive

| field | content |
|---|---|
| **kind** | qualified positive (a methodological claim, not a measurement) |
| **claim as stated** | "**The caveat was load-bearing within the week**, and that is the best argument this repository can offer for writing completeness limits at all." — README.md:134-135; DECISIONS.md:577-579 |
| **deciding figures (n)** | Stage D closed "there is none" 2026-08-30; the Kalshi reply arrived **2026-09-01**. n = 1 vindication, over 3 candidate routes read and 4 document classes (Zenodo / Dataverse / OSF / figshare) admittedly not read; the completeness pass recorded **9 unread document classes** with the bias direction named (docs/LICENCES.md:665-688) |
| **file:line** | REGISTRATION.md:558-564; report.md:361-379; DECISIONS.md:570-579; HYPOTHESES.md:281-288; docs/ACCESS.md:317-326 |
| **bar + registration date** | the caveat itself, written into the Stage D material of 2026-08-30 UTC (`7b5a751` 2026-08-30T06:22:49Z, `baa2bf3` 06:35:19Z) — before the event that vindicated it. No bar was moved |
| **amendments touching the bar** | none |
| **corrections applied** | the register records that the vindication does **not** make the route usable: nothing applied for, nothing granted, nothing refused; fee UNMEASURED; publication right UNRESOLVED; AI/ML consent UNRESOLVED (REGISTRATION.md:533-544, :566-569) |
| **framing** | README.md:130-135; report.md:373-379 ("the most interesting sentence in this report"); consistent across all three documents |
| **audit flags** | none |

---

## 2. Shipped artifacts

| artifact | claim as stated (file:line) | deciding figures (n) | bar + registration date | amendments touching the bar | corrections applied | framing | audit flags |
|---|---|---|---|---|---|---|---|
| **The power gate** (`pmexperiment/power.py`; Sections 0.3, 0.4, 9) | "\| **GO** \| MDE ≤ 0.02 \| the design resolves the entire published band" — REGISTRATION.md:110 | MDE = z·√(v̄/n_T), z = 2.0 two-sided (:99-101; registry.py:9); planning v̄ = 0.0475 (:122-123); required n_T ≥ **475** (GO), ≥ **30** (out of BLOCKED) (:128-129). **n actually gated: 0 — the gate never fired** (README.md:13-14; progress.md:759 "Both passes are **absent, not zero**") | Section 0.3 / 0.4 / 9, commit `9080186` **2026-08-29T07:37:33Z**, before the first request at ~07:44Z | none — Sections 0–14 byte-identical to the anchor. Amendment 2 ordered the band gate ahead of it; Amendment 5 added a filter that "biases every count the gate consumes toward BLOCKED" (registry.py:47-48) | Unrestricted sampling uses the Wilson 95 % **lower** bound, the conservative direction (REGISTRATION.md:88-95); the tail cell is 91–99 rather than 90–99, which "can only shrink the tail count — the conservative direction" (:70-73). **Not applied:** no power term, no clustering unit, no multiplicity across the two verdict cells (Section 8 defers all three past the gate, :293-295) | README.md:177-192 "**The measurement that was supposed to decide this repository. Not the calibration error. The power to detect one inside the Canadian filter.** … **This repository followed Insider, not NPD**"; CLAUDE.md:63-65 "**Follow Insider.**" | AUDIT-B-PMExperiment-2 (no power level stated anywhere; z = 2.0 gives 0.5160 power at the GO bar; 80 % power needs n_T ≈ 932.05 → 933 and 58.25 → 59, not 475 and 30; n_T = 30 becomes BLOCKED at MDE 0.11148; clustering unregistered while the benchmark reports 46,282 contracts across 12,403 events; direction of bias unnamed against the register's own preamble at :13-14). AUDIT-B-PMExperiment-12 (planning v̄ is the point value at the cell's centre, not the registered cell mean 0.049105 over 19 prices; 475/30 never restated for the halved 91–99c region) |
| **`pmexperiment/band.py` + `docs/BAND.md`** — the band arithmetic | "Every figure is computed by `pmexperiment.band` and pinned by `tests/test_band.py`, so nothing here is hand arithmetic." — docs/BAND.md:8-9 | Ten-decile table at three turnovers on two routes (docs/BAND.md:199-210); cross-check that the round-trip route at k = 1 reproduces `power.cost_floor` and Section 11's C(0.95) = 0.0785 / C(0.05) = 0.0515; **63 tests green** at the stage's close, 9 new honesty tests, 5 verified by mutation (progress.md:493-507) | Constants from registry.py:52-66, pinned to Sections 2 and 11 by tests/test_registry.py; registered `9080186` 2026-08-29T07:37:33Z | Amendment 4 adds `FX_TURNOVER_REGISTERED = 1.0` (registry.py:66), committed one commit before the amendment text that cites it — **disclosed** (DECISIONS.md:304-307; progress.md:515-518) | Written test-first (progress.md:493-494); BAND-NARROW and BAND-OPEN deliberately **not** derived in code because they turn on a count the stage may not read (band.py:128-133) | README.md:222 "`pmexperiment/` \| the package: registered constants, the band, the power arithmetic, ADR-012 as code" | Reproduces exactly, cell for cell (see "found sound" 2). AUDIT-B-PMExperiment-4 (one half-spread charged on both routes, `band.py:80`, pinned at tests/test_band.py:44-53); AUDIT-B-PMExperiment-3 (`surviving_buckets` iterates `BUCKET_EDGES_CENTS`, band.py:114-122, while `TAIL_BUCKETS_CENTS` sits at registry.py:26) |
| **`pmexperiment/admissibility.py`** (ADR-012 as code) — the README's headline contribution | "A statement about what a source permits carries **a quoted clause, the document's effective date, and the date it was fetched** — or it is recorded **UNMEASURED** and the work proceeds as if permission were absent." — README.md:35-37 | Three required elements (`REQUIRED_ELEMENTS`, admissibility.py:54); client-rendered-shell bar `MIN_DOCUMENT_TEXT_RATIO = 0.05` (:49). Fired over **4 claims**: Amendment 1 inadmissible 3/3, Stage C admissible 3/3, Stage A admissible **2/3**, the Kalshi reply UNMEASURED on element (2). Mutation counts 5 → 13 → 14, all load-bearing; **111 tests** at closure (progress.md:982-989, :1202-1214, :1517-1527, :1648) | ADR-012 accepted **2026-08-30** (DECISIONS.md:346); module committed `b67fc84` **2026-08-30T04:28:05Z**, one hour before the candidate read `7b5a751` 06:22:49Z | none. Softening was forbidden by the stage prompt ("**do not soften ADR-012 to admit a candidate**", progress.md:884) and was refused (docs/LICENCES.md:493-503) | Fired over the repository's own claims first; convicted the ADR's own sentence "Stage A's Kalshi finding met that bar" at DECISIONS.md:434-440. Text-ratio bar found method-dependent (18.05 % vs 67.98 % on the same Dune body) and recorded as a limitation (docs/LICENCES.md:76-83). Blind spot recorded and deliberately not repaired (README.md:47-49; docs/ACCESS.md:291-300) | README.md:29-49 as contribution #1, "portable to any project that has to decide what it is allowed to read" | AUDIT-B-PMExperiment-11 (the module's own rule — `admit()` returns UNMEASURED for a claim missing an effective date, "**including a claim that permission is absent**" — was not applied to candidate 3, published PROHIBITED on a "Last updated on" label). **Not raised:** the disclosed quotation blind spot; `_is_iso_date` and the fail-closed treatment of a claimed PROHIBITED are both **stronger** than ADR-012 requires; `MIN_DOCUMENT_TEXT_RATIO` rests on one measured observation and says so with its direction of error (admissibility.py:39-49) |
| **The cost model / cost floor** (Sections 2 and 11; `power.py:74-82`) | "C(p) = 0.04 + 0.01 + 0.03·p … At the favourite tail, p = 0.95, the floor is **0.0785**" — REGISTRATION.md:203-212; restated ":334-339" as "Fixed before any measurement; not revisable after a result is seen" | 0.0785 at 95c round trip; 0.0585 at 95c held; fee + spread alone **0.0300** vs band bottom **0.0200** | Sections 2 and 11, `9080186` 2026-08-29T07:37:33Z | **Amendment 2** adds the held-to-resolution route (one fee side); **Amendment 4** names k and binds k = 1 | every component carries a named direction of bias (:199-201); two registered simplifications leaning toward H1 quantified at 0.00195 (:841-849) | REGISTRATION.md:456-459 "**The decisive figure, for a reader who reads one number**"; README.md:90-95 | AUDIT-B-PMExperiment-4 (a spread component justified by "**A settlement exit crosses no spread**" was carried unamended onto the non-settlement route). The held-route fee halving itself is **not** a finding: numbered, pre-verdict, consistent with Section 2's own note, reported beside the round-trip figure throughout, and BAND-OPEN does not depend on it |
| **The honesty test suite** (`tests/`, 111 passing at closure) | "**A gate that has never failed is not a gate** — every guard here carries a test that fails when the guard is removed, verified by mutation." — README.md:230-232 (standing rule 14, CLAUDE.md:45-46) | 14 mutations at closure, all load-bearing (DECISIONS.md:706-718); 13 at Stage D, 5 at Stage C; test counts 34 → 39 → 63 → 72 → 89 → 95 → 108 → **111** | rule 14 registered in CLAUDE.md at scaffold, 2026-08-29 | ADR-020 and ADR-021 (2026-09-02) fix the harness after false greens | three recorded harness faults (Entry 7.1, Entry 9.1, ADR-021), affected mutations re-run (progress.md:1229); `tests/test_guards.py:139-150` asserts the mutation baseline first — "a mutation that does not mutate is not evidence" | README.md:230-232 | none raised — the faults are recorded as ADRs rather than hidden |
| **Amendment 5 — the $1,000 volume floor** | "a floor chosen by someone else, before this repository existed, **cannot have been tuned to a sample this repository had not yet seen**" — progress.md:709-712 | threshold **$1,000**; **cost in sample: not measured, n = 0 contracts enumerated** (progress.md:714-715) | stated "Made 2026-08-30"; commit `f789079` **2026-08-30T03:34:00Z** — after Stage B's verdict had already recorded the floor as absent | it *is* the amendment; the benchmark's companion spread filter was deliberately not adopted "because a filter whose sample cost cannot be measured is worse than no filter" (progress.md:716-718) | provenance-based justification; direction of bias named ("biases every count the gate consumes toward BLOCKED", registry.py:47-48) | docs/LICENCES.md:750-755 "registered and **never exercised** — its cost in sample is unmeasured, reported absent rather than as zero" | its absence at Stage B is one of the two legs on which BAND-NARROW was excluded — AUDIT-B-PMExperiment-5 |
| **The route ledger** (README's public summary table) | "\| route \| verdict \| on what \| date \|" — README.md:113-121, mirrored REGISTRATION.md:595-603 | **7 rows**; 0 contracts, 0 dollars, 0 market-data requests to the measurement venue | each row's verdict registered in Sections 15.1–15.5 as it fired | Amendment 9 (2026-09-02) adds a fourth reopening condition | "PROHIBITED is the baseline, not a rejection"; "EXISTS-AND-UNTRAVELLED" defended precisely (README.md:120-128) | README.md:111-128 | AUDIT-B-PMExperiment-14 (README's reopening list carries 3 conditions; the register carries 4 after Amendment 9, committed 14 minutes after the README rewrite) |
| **The Stage B direction correction** — README contribution #4 | "**The registered FX is proportional to entry price, so every exploitable expression of the band is charged FX at 88–95c rather than at 5–12c**" — README.md:90-92 | Bürgi 5c/3 % → NO at **0.950**, 0.020, n = 313,972 prices / 46,282 contracts / 12,403 events; Bürgi 95c/98 % → YES at **0.950**, 0.030, same n; Krause sub-30c/4.0 % → NO at **0.883**, 0.077, n **not recorded** | Stage B Task 2's registered instruction to establish the unit before computing, logged verbatim at progress.md:274-285, commit `e2d8f10` 2026-08-29T19:07:37Z, before the arithmetic at 19:15:55Z | none | each magnitude reconstructed both as a gap and as a return and checked against the register's printed numbers; the post-fee "lose over 60 %" figure excluded as unusable because using it against a cost model "would charge the fee twice" (docs/BAND.md:139-143) | README.md:76-95, one of four transferable outputs | Reproduces exactly in every cell; a correction that made the repository's own case **worse** and was published at the top of the README. Its unacknowledged consequence — that it moves the band top's own source outside the cell the band is registered for — is AUDIT-B-PMExperiment-8 |
| **ADR-015 (symmetry of convenience) and the self-audit** — contributions #2 and #3 | "A venue may not be held to a **looser** reading than another because its verdict would be more convenient — and **the rule runs both ways.**" — README.md:53-54 | Dune: bare `curl` **403**, the same `curl` with a browser `User-Agent` **HTTP 200**; in-force body **172,750 bytes**. Kalshi PDF: `Effective` **0**, `Last Updated` **0** → the finding met **2 of 3** elements | ADR-012 (2026-08-30) and ADR-015 (`baa2bf3` 2026-08-30T06:35:19Z) | none | the self-audit is recorded although "**This changes no verdict**" (DECISIONS.md:437-440) | README.md:51-74 | AUDIT-B-PMExperiment-11 finds the symmetry rule not applied to the repository's own dating standard across candidates 2 and 3; AUDIT-B-PMExperiment-7 finds it not applied to the effect-band sources at all |

---

## 3. Open hypotheses

| entry | claim as stated (file:line) | kind | deciding figures (n) | bar + registration date | amendments | corrections | framing |
|---|---|---|---|---|---|---|---|
| **H1** — "Prediction-market prices are mis-calibrated by enough to survive the costs a Canadian retail participant actually pays" | "**Status: OPEN. Registered 2026-08-29; the access gate fired PENDING_ACCESS the same day**" — HYPOTHESES.md:30-31; terminal line "**TERMINAL: H1 is unmeasurable at this house's standard. Not disproven, not unlikely, unmeasurable.**" — :14-15 | open (terminal-unmeasurable; does **not** close) | **none.** "no figure exists for or against H1" (HYPOTHESES.md:32); no MDE, no bucket count, no dispersion; **0** contracts, **0** price buckets, **0** statistics across five stages (progress.md:1547-1549) | Section 16's closure conditions registered 2026-08-29 (`9080186`): H1 closes only if **both** verdict cells fire BLOCKED with realized MDEs and their n | Amendment 8 (2026-09-02) ends the project with three reopening conditions; Amendment 9 adds a fourth. Section 16 annotated, body unedited (verified by diff) | "**The registered closure conditions were never met.** … **Neither cell ever fired.** … **H1 therefore does not close under Section 16 at all.**" — REGISTRATION.md:605-609 | README.md:6-8; report.md:458-462; consistent |
| **H1t** — transfer: "a calibration result measured on Polymarket holds on a Canadian-tradeable venue" | "**UNTESTED. May not be assumed at any point.**" — HYPOTHESES.md:101-102 | open, untested | three registered grounds, one quantitative: MLCryptoEngine's H2 cross-venue transfer at **AUC 0.501** (HYPOTHESES.md:103; report.md:456) — **n for that AUC not recorded in this repository**. The other two grounds carry no citation and no n (docs/LICENCES.md:653-656) | registered in the 2026-08-30 HYPOTHESES amendment (:97-104), i.e. with Amendment 1 | none | the ground survived Amendment 6's retraction of Amendment 1's premise and is restated at every stage | REGISTRATION.md:624-626; report.md:455-456 |
| **H2**, **H3** | "PARKED. Depends on intraday price history being retrievable at usable depth" / "Requires H1's gate to clear first" — HYPOTHESES.md:73-74; "**H2 and H3 stay PARKED and are not carried forward.**" — :323 | parked | none | HYPOTHESES.md:69-75, 2026-08-29 | none | **Recorded, not raised:** H2's stated parking reason drifts — it was parked on depth "which Stage A measures" (:73), Stage A measured that NOT DEMONSTRATED on n = 1, and the closure says instead "Both depended on H1's gate clearing" (:323-324). The drift runs toward leaving a hypothesis open, not toward claiming anything | consistent |

---

## 4. Negatives whose verdict rested on a threshold

| verdict | claim as stated (file:line) | the threshold | deciding figures (n) | bar + registration date | amendments | corrections | framing / audit note |
|---|---|---|---|---|---|---|---|
| **Kalshi keyless — PENDING_ACCESS**, 2026-08-29 | "**PENDING_ACCESS** (REGISTRATION.md Section 0.5). Conditions 1 and 2 pass; conditions 3 and 4 fail closed as unmeasured or undemonstrated; condition 5 fails closed on the recorded terms." — docs/ACCESS.md:9-12 | Section 0.5's five ACCESS-OK conditions, incl. `ACCESS_MIN_SETTLED_MARKETS = 1000` (registry.py:36) and 30 days of price history | Condition 1 PASS: HTTP 200 in **127.6 ms**, 2 records. Condition 2 PASS: `result` present on **2 records** against a registered cap of 5 (registry.py:37). Condition 3 NOT MEASURED — "a single page of 20 returned with a continuation cursor". Condition 4 NOT DEMONSTRATED on **n = 1** market ≥ 30 days old, **0 daily candles**. Condition 5 FAIL on terms. **13 outbound requests, 11 API reads.** Depth: earliest keyless settled close between 2024-01-01 and 2024-05-31, **n = 6 bracketing probes** | Section 0.5, `9080186` **2026-08-29T07:37:33Z**, before the first request at ~07:44Z | none. Amendment 1 moved the venue rather than relitigating the verdict | all ambiguous readings counted ambiguous (standing rule 15); the rate limit **withheld** rather than measured under ADR-007 because the governing agreement could not be read; Stage E later convicted the finding at 2 ADR-012 elements of 3 | **Sound.** Conditions 3 and 4 fail **closed** on n = 20 and n = 1; the depth claim was phrased as a property of the keyless surface and survived the Kalshi reply (docs/ACCESS.md:317-326) |
| **Polymarket — PENDING_ACCESS**, 2026-08-30 | "Terms of Use, effective 2026-08-11 and read in full before any repeated fetch, prohibit 'data mining tools, robots, crawlers, or similar data gathering and extraction tools'" — progress.md:672-678 | ADR-012's three elements | Terms **59,617 bytes** (Stage C) / **58,830 characters, 14 chunks, zero gaps** (Stage D re-extraction); robots.txt HTTP 200, 35.7 ms, **73 bytes, no `Disallow`**; **7 requests** to Polymarket hosts, **0 market-data requests**; `artificial intelligence` **0**, `machine learning` **0** | standing rule 12 (CLAUDE.md:42-43), registered at scaffold; ADR-012 registered 2026-08-30 from this stage's own failure | **Amendment 6** retracts Amendment 1's premise — a falsification of the repository's own earlier claim, recorded as one | the strongest counterargument (the crawlers bullet is scoped to "the Site, any other Interface, or Features") is set out at full strength with three reasons it is not taken; robots.txt's permissiveness and the conditional Data clause are recorded **against** the verdict | **Sound.** REGISTRATION.md:461-513; report.md:141-232 |
| **Academic datasets — UNMEASURED**, 2026-08-30 | "**Decision: UNMEASURED, on ADR-012 elements (1) and (2).**" — DECISIONS.md:460 | ADR-012 element (2): the document must print an effective date | `TimeSeventeen/Polymarket-v1`: CC BY 4.0 stated **3×**, all four gate inputs documented over **1,201,580,990 rows** (2022-11-21 → 2026-04-28); **no date printed on the card or in the CC BY 4.0 legal code** | ADR-012, 2026-08-30, applied without amendment | none — the argument that the standard is unmeetable for any CC licence is recorded at full strength and **not acted on** (DECISIONS.md:470-480) | three further gaps recorded as surviving a cured date: chain of title, the grant's Section 1 authority cap, an unrun AI-clause search | the tension is stated, escalated and left closed. **Comparison point for AUDIT-B-PMExperiment-11 and -7** |
| **Dune — PROHIBITED**, 2026-08-30 | "**Decision: PROHIBITED for Dune, the one in-scope platform measured; UNMEASURED for Flipside, Allium, Nansen and Sim, whose governing documents were not retrieved.**" — DECISIONS.md:503-505 | ADR-012 + standing rule 5 | Terms label `Last updated on: June 3rd, 2026`, body **172,750 bytes**; affirmative-permission search **0 occurrences each** for 9 terms; pricing page text ratio **0.14–0.40 %** → tier price UNMEASURED | ADR-015, 2026-08-30 | none | the verification overturned the licence read's central factual claim: bare `curl` **403** vs the same `curl` with a browser User-Agent **HTTP 200**; "PROHIBITED on an instrument that was never read is a synthesized value" | README.md:51-63 as contribution #2; the self-conviction is the headline, not a footnote. **AUDIT-B-PMExperiment-11**: the effective-date element was met by substitution here and refused elsewhere |
| **Kalshi Internal Use — EXISTS-AND-UNTRAVELLED**, received 2026-09-01 | "**EXISTS-AND-UNTRAVELLED.** A route exists and was **not declined on the merits**; it is gated on an established legal entity, and **nothing was applied for, so nothing was granted and nothing was refused**." — docs/ACCESS.md:224-226 | ADR-012 elements (1) and (2), applied to correspondence for the first time | returns **UNMEASURED on element (2)**; element (1) unmet in substance (an operator paraphrase, not the reply's text — "no sentence of the correspondence is quoted anywhere in this repository", docs/ACCESS.md:288-289); licence granted **none**; fee **UNMEASURED**; requests sent **0** | ADR-012, 2026-08-30 | the standard was **not** amended at closure to admit it (REGISTRATION.md:546-556); the argument that a received date *is* an effective date is recorded "at full strength and **not adopted**" (progress.md:1426-1432) | the register records the honest asymmetry: "**Here holding it costs nothing** … Applying a rule when it is free is not evidence that the rule is being applied" (DECISIONS.md:592-596); the procedure's blind spot recorded and deliberately not repaired | **Sound.** The strongest available temptation — writing an unrefused route as evidence — is explicitly refused (README.md:120-128) |
| **The entity path — declined by the operator**, 2026-09-02 | "**This is the operator declining a cost. It is not a discovery, and it is not evidence about H1.**" — report.md:422-423 | no threshold; a cost judgement against a **stated** prior of 5 to 8 percent and a band recorded as thin | surviving region "the top **2.15 of 6.0 points**" at 95c; **5.85** required at k = 1 vs band top **8.00**; Bürgi's **2.0** and **3.0** both fail the **0.0300** floor (REGISTRATION.md:1048-1054) | Section 13 registered 2026-08-29 as "*to be filled by the operator before the gate fires*" and **never filled**; the prior arrives 2026-09-02 in Amendment 7 | **Amendment 7** (2026-09-02) records the prior **after** the band gate and both access gates fired — all the data that ever existed already existed; the register forbids reading any verdict against it as pre-registered (:1027-1029) | filed in its own category so it is never collapsed with the access verdicts (ADR-017, DECISIONS.md:648-664) | README.md:168-175 discloses it correctly; **README.md:20-23 and report.md:443-445 project it backwards** — AUDIT-B-PMExperiment-6 |
| **Terminal — H1 unmeasurable**, 2026-09-02 | "**H1 is unmeasurable at this house's standard — not disproven, not unlikely, unmeasurable**" — REGISTRATION.md:575-578 | Section 16's registered closure conditions, **recorded as never met** rather than substituted | both verdict cells: never fired. Realized MDE: none. Contracts **0**; dollars **0** | Section 16 registered 2026-08-29 | Amendment 8 (2026-09-02) ends the project; Section 16 annotated, body unedited (verified by diff; REGISTRATION.md:640-641) | the two words the verdict is **not** are enumerated with reasons (:582-586) | **Sound.** README.md:6-14; report.md:458-462; HYPOTHESES.md:254-268; pinned by mutation-verified tests |

---

## 5. Thresholds and figures used as bars

| threshold / figure | value | file:line | note |
|---|---|---|---|
| effect band | **0.02 – 0.08** probability points, tail cell only | REGISTRATION.md:221-222; registry.py:10-11 | bottom from Bürgi (n = 313,972 prices); **top from Krause, n absent** |
| registered cost floor | C(p) = 0.05 + 0.03p; C(0.95) = **0.0785** | REGISTRATION.md:334-339; power.py:74-82 | every component carries a named direction of bias |
| FX turnover | **k = 1** binding; k = 12 and k → ∞ reported beside it | REGISTRATION.md:783-849; registry.py:59-66 | binds in the direction that does **not** help H1 |
| power gate z | **z = 2.0** two-sided, no β | registry.py:9; power.py:45 | AUDIT-B-PMExperiment-2 |
| planning dispersion | v̄ = **0.0475** | REGISTRATION.md:122-123; tests/test_power.py:21 | the cell mean over 19 integer cents is 0.049105 — AUDIT-B-PMExperiment-12 |
| required tail counts | **≥ 475** (GO), **≥ 30** (out of BLOCKED) | REGISTRATION.md:128-129 | never restated for the halved 91–99c region |
| client-rendered-shell bar | text/body ratio **< 0.05** | admissibility.py:49 | disclosed as method-dependent: 18.05 % vs 67.98 % on the same body (docs/LICENCES.md:76-83) |
| outcome-presence cap | **5 records** (2 used) | registry.py:37; docs/ACCESS.md:19 | pre-registered exception to outcome blindness |
| settled-market floor | **≥ 1,000** | registry.py:36 | never measured; fails closed |
| maturity rule | **30 days** | registry.py:42 | never applied to a real enumeration |
| volume floor | **≥ $1,000** | registry.py:50; REGISTRATION.md:853-855 | imported from the benchmark; never exercised |
| unrestricted sample | m = **2,000**, seed **20260829**, Wilson z **1.96** | registry.py:31-33 | never drawn |
| mutation / test counts | 5 → 13 → 14 mutations; 34 → … → **111** tests | progress.md:502-507, :1202-1214, :1517-1527, :1648 | three harness faults found and recorded |
| whole-history credential audit | **32 commits, 189 objects, zero credential-shaped strings** | progress.md:1537-1543 | git log at the anchor shows **36 commits**, 4 of them made after the audit ran |

---

## Leads for the cross-repository pass

**A. Figures this repository imports from other repositories and relies on.** None carries its
own n inside PMExperiment; each is load-bearing here, so if any is itself in question, a
conclusion here moves with it.

1. **NPDExperiment** — "a realized minimum detectable contrast of **0.0512** against an effect
   band of **0.01 to 0.05** … discovered after **415 days** of collection, in the same session
   that read the result" (README.md:182-186; CLAUDE.md:54-58; REGISTRATION.md:29-44). This is the
   negative example the whole power-gate framing is built against ("This repository followed
   Insider, not NPD", README.md:190). **Comparison repository: NPDExperiment.** Check that
   0.0512, the 0.01–0.05 band and the 415 days are what NPDExperiment actually records, and note
   that PMExperiment's own gate is a 2-SE bar (AUDIT-B-PMExperiment-2) — if NPD's 0.0512 was
   computed at a different z, the two are not comparable in the way this README implies.
2. **InsiderExperiment** — "registered its gate in advance and fired **BLOCKED at 49.35 bp**
   before spending" (README.md:186-188; CLAUDE.md:60-61; REGISTRATION.md:46-47). This is the
   positive example, and PMExperiment's Section 0.3 inherits Insider's inclusive-lower-edge
   boundary convention verbatim ("following Insider", REGISTRATION.md:105-106; power.py:53-54).
   **Comparison repository: InsiderExperiment.** Worth checking whether Insider's gate carries a
   power term that PMExperiment's dropped.
3. **MLCryptoEngine** — "H2 cross-venue transfer at **AUC 0.501**" (HYPOTHESES.md:103;
   report.md:456; carried in six places). This is the single quantitative ground for H1t being
   UNTESTED, and H1t is the reason no measured Polymarket result could have been claimed for
   Kalshi. **The n behind that AUC is not recorded in this repository.** **Comparison repository:
   MLCryptoEngine.** Also: "Eleven MLCryptoEngine hypotheses closed on cost rather than on
   signal, several after data had been collected" (REGISTRATION.md:710-711) is the stated reason
   Amendment 2 ordered the band gate first — the count 11 should be checkable there.
4. **ORBExperiment** — "align the document set to the ORBExperiment house shape" (commit
   `180c235`, 2026-08-29T07:17:04Z). The five-document shape (REGISTRATION / HYPOTHESES /
   DECISIONS / progress / report) and several standing rules are inherited. **Comparison
   repository: ORBExperiment.**

**B. Artifacts here that another repository could rely on.**

5. **ADR-012 as code** (`pmexperiment/admissibility.py`, 190 lines) is offered explicitly as
   portable — "portable to any project that has to decide what it is allowed to read"
   (README.md:30-31). If any other repository has adopted it, AUDIT-B-PMExperiment-11 (the
   effective-date element satisfied by a last-updated label) travels with it, as does the
   disclosed quotation blind spot.
6. **The band arithmetic** (`band.py`) and the direction correction (every exploitable expression
   of a favourite-longshot band sits at 88–95c, so proportional FX is charged near its maximum)
   are offered as transferable outputs (README.md:76-95). The feasibility bound this audit found
   missing (AUDIT-B-PMExperiment-1: the edge cannot exceed 1 − p) applies to **any** repository
   that models a probability edge against a per-contract cost at a stated entry price. Worth
   grepping for in ETFExperiment, VRPExperiment and ORBExperiment.

**C. Standards applied here that look laxer or stricter than the house norm.**

7. **Stricter than the house norm, on permission:** ADR-012's three conjunctive elements, with
   UNMEASURED treated exactly as PROHIBITED, refused a CC BY 4.0 dataset of 1,201,580,990 rows
   for want of a printed date and convicted the repository's own Stage A finding. I know of no
   other repository in this program that refuses an input on a missing date alone. **Comparison
   repositories: ETFExperiment and VRPExperiment** (both consume third-party data whose licence
   and provenance state is recorded) — if either admits a dataset that would fail ADR-012, the
   house standard is not uniform, and this repository's terminal verdict is stricter than its
   siblings' by construction rather than by evidence.
8. **Laxer than the house norm, on literature figures:** standing rule 4 ("Verify every external
   figure live", CLAUDE.md:25-26) and standing rule 13 ("Every figure travels with its n",
   :44) were applied to every permission document and to none of the three effect-band sources.
   The deciding source (Krause 2026) carries no n, no DOI/SSRN/URL — 32 mentions, 0 identifiers —
   and no fetch record, while its own companion study in the same bullet carries "SSRN 7087538,
   95 contracts over 12 months". **AUDIT-B-PMExperiment-7.** Worth checking in every sibling
   repository whether externally-sourced effect bands carry retrievable identifiers and n:
   **comparison repositories: NPDExperiment (the 0.01–0.05 band) and InsiderExperiment (the
   49.35 bp bar)** are the obvious first two, since PMExperiment cites both.
9. **A dating convention that is wrong in a checkable direction.** Amendments 1–3 and the
   ADR-006(2)/ADR-007(2)/ADR-008 trio carry "2026-08-30" while the commit that made them is
   `f686036` 2026-08-29T18:05:26Z, and the register consequently carries an amendment dated
   08-29 *after* three dated 08-30 (AUDIT-B-PMExperiment-9). **Any cross-repository timeline
   built from this repository's document stamps rather than its commits will be wrong by a day
   for those six entries.** If the same author habit shows up in NPLExperiment or ORBExperiment
   (both moved in the same window), the correction is systemic rather than local.
10. **A closure-framing pattern.** A post-hoc operator prior is recorded honestly in its own
    section and then used retrospectively in the README's opening block and the report's closure
    ("a null was the modal expected outcome **before any of this began**",
    AUDIT-B-PMExperiment-6). The prompt that produced it is logged verbatim
    (progress.md:1310), so the same instruction — "State the registered prior and that a null was
    the modal expected outcome" — may have been issued to sibling projects closing in the same
    window. **Comparison repositories: NPLExperiment and ORBExperiment**; grep their closure
    documents for "modal expected outcome".
