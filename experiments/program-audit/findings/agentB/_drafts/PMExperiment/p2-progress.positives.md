# PMExperiment — POSITIVES LEDGER (part p2-progress)

Repository: PMExperiment, anchored SHA `03d16e71dbf25a86c529884662d02136f8e82334`
(main, 2026-09-02, closed project). Scope: entries whose primary evidence lies in
`progress.md`, `docs/ACCESS.md`, `docs/BAND.md`, `docs/LICENCES.md`,
`pmexperiment/` and `data/`. Bars and framings living in `REGISTRATION.md`,
`HYPOTHESES.md`, `README.md` and `report.md` are cited where they set or restate
the entry. Factual, not advocacy.

Commit dates below are from the live repository's git log, converted from the
recorded −07:00 offset to UTC.

---

## 1. BAND-OPEN — the repository's only positive verdict

| field | value |
|---|---|
| **Kind** | qualified positive |
| **Claim as stated** | "**BAND-OPEN.** A surviving region exists inside the permitted subset: at entry prices 91–99c held to resolution, an effect in the upper part of the registered band clears the registered cost, requiring **5.85 points** of underpricing at the registered FX turnover against a band whose top is **8.00 points**." — PMExperiment/docs/BAND.md:15-18; verdict sentence PMExperiment/progress.md:362-368; register PMExperiment/REGISTRATION.md:402-412 |
| **Deciding figures (n)** | R_H(0.950) = **0.0585** required vs registered band top **0.0800**; margin 0.0215 (PMExperiment/docs/BAND.md:210, :257-259). Survival count **10 of 10** deciles on both routes at k = 1, 12, →∞ (PMExperiment/docs/BAND.md:233, PMExperiment/REGISTRATION.md:416). Band bottom 0.0200 unreachable everywhere: fee + half-spread = **0.0300** (PMExperiment/docs/BAND.md:241-243). Magnitudes actually cited at 91–99c: **0.020** (n = 313,972 prices / 46,282 contracts / 12,403 events) and **0.030** (same n) — **both fail** (PMExperiment/docs/BAND.md:153-154, :247-252). Band top's source: Krause 0.077, **n not recorded** (PMExperiment/docs/BAND.md:155, :335-336) |
| **file:line** | PMExperiment/docs/BAND.md:13-25, :298-338; PMExperiment/progress.md:360-368, :476-489; PMExperiment/REGISTRATION.md:402-446 |
| **Bar + registration date** | Amendment 2's three verdict rows, PMExperiment/REGISTRATION.md:736-742. Stated made-date **2026-08-30**; actual commit `f686036` **2026-08-29T18:05:26Z**. Verdict fired in commit `32dc10a` **2026-08-29T19:24:06Z** — 79 minutes after the bar. The band top 0.08 and bottom 0.02 were registered earlier still, in Section 3, commit `9080186` **2026-08-29T07:37:33Z** |
| **Amendments touching the bar (date, data existed?)** | **Amendment 4** (FX turnover k = 1 binds), stated "Made 2026-08-29", commit `4d75f66` 2026-08-29T19:17:21Z — registered **during** Stage B, after `9b4bd4f` (19:15:55Z) had already committed the band arithmetic; the lag is disclosed at PMExperiment/progress.md:515-518. It fixes k = 1, the treatment that biases toward BAND-EMPTY, so it does not help H1. **Amendment 5** (volume floor ≥ $1,000), stated "Made 2026-08-30", commit `f789079` 2026-08-30T03:34:00Z — registered **after** the verdict that recorded the floor as absent; never exercised (PMExperiment/progress.md:706-718). No amendment altered a cost component or a band edge: Sections 2 and 3 are byte-identical from `9080186` to the anchor |
| **Corrections applied** | Unit determination (probability points, not returns) — PMExperiment/docs/BAND.md:120-143. Direction correction (exploitable side is the complement; every registered magnitude sits at 0.883–0.95) — :145-159. Both FX turnover readings reported, k = 1 binding — :163-187. Two FX-base simplifications quantified at 0.00195 and 0.00135 and used to exclude route X — :181-187, :261-265. Both quantifier readings reported — :229-237. **Not applied:** no multiplicity, survivorship, look-ahead, clustering or fill correction — none applies to an arithmetic-only gate, and no data existed to correct |
| **Framing in README/report/register** | README:137-149 "**The one number this repository produced, and what it is not** … **It is a cost finding computed from registered constants with no calibration measurement behind it. It must not be written anywhere as evidence that an edge exists.**" report.md:113-121 "**So BAND-OPEN is a thin verdict, and it is reported as one.**" REGISTRATION.md:431-446 carries three qualifications "registered with the verdict and not separable from it". HYPOTHESES.md:147 "**What this verdict is not.** BAND-OPEN is **not** evidence that a tradeable edge exists." The caveat travels intact into every document |
| **Audit notes** | See DRAFT-p2-progress-1 (95–99c of the fired region is arithmetically empty; the 0.950 midpoint at which every headline figure is quoted has a ceiling of 0.0500 against a requirement of 0.0585), -3 (the 10/10 count applies the band where the band is not registered; 2/2 inside the registered cell), -4 (BAND-NARROW excluded by resolving an unevaluable clause permissively), -8 (the band top's only source sits at 0.883, outside the fired cell, with no n) |

## 2. `pmexperiment/band.py` + `docs/BAND.md` — the band arithmetic as a shipped artifact

| field | value |
|---|---|
| **Kind** | shipped |
| **Claim as stated** | "Every figure is computed by `pmexperiment.band` and pinned by `tests/test_band.py`, so nothing here is hand arithmetic." — PMExperiment/docs/BAND.md:8-9 |
| **Deciding figures (n)** | Ten-decile table at three turnovers, two routes (PMExperiment/docs/BAND.md:199-210); cross-check that the round-trip route at k = 1 reproduces `power.cost_floor` and Section 11's C(0.95) = 0.0785 / C(0.05) = 0.0515 (PMExperiment/progress.md:493-497, PMExperiment/tests/test_band.py:30-42). 63 tests green at the stage's close, 9 new honesty tests, 5 verified by mutation (PMExperiment/progress.md:502-507) |
| **file:line** | PMExperiment/pmexperiment/band.py:1-135; PMExperiment/tests/test_band.py:1-184 |
| **Bar + registration date** | Constants from `registry.py:269-283`, pinned to REGISTRATION.md Sections 2 and 11 by `tests/test_registry.py`; registered `9080186` 2026-08-29T07:37:33Z |
| **Amendments touching the bar** | Amendment 4 adds `FX_TURNOVER_REGISTERED = 1.0` (registry.py:283), committed one commit before the amendment text it cites — disclosed, PMExperiment/progress.md:515-518 |
| **Corrections applied** | Written test-first ("`tests/test_band.py`, which existed first and failed on import before the module did", PMExperiment/progress.md:493-494); BAND-NARROW and BAND-OPEN deliberately **not** derived in code because they turn on a count the stage may not read (PMExperiment/pmexperiment/band.py:128-133) |
| **Framing in README/report/register** | README:222 "`pmexperiment/` | the package: registered constants, the band, the power arithmetic, ADR-012 as code" |
| **Audit notes** | Reproduces exactly, cell for cell (see "found sound"). Two defects: the exit-before-resolution route is charged one half-spread on both routes (`band.py:80`, pinned at `tests/test_band.py:44-53`) — DRAFT-p2-progress-2; and `surviving_buckets` iterates all ten deciles rather than `TAIL_BUCKETS_CENTS` — DRAFT-p2-progress-3 |

## 3. `pmexperiment/power.py` and the registered planning counts — a shipped power limit

| field | value |
|---|---|
| **Kind** | shipped (a power limit) |
| **Claim as stated** | "inverting MDE = 2·sqrt(v̄/n) at each bar gives the required tail count: | GO, MDE ≤ 0.02 | ≥ 475 | | stay out of BLOCKED, MDE ≤ 0.08 | ≥ 30 |" — PMExperiment/REGISTRATION.md:122-129 |
| **Deciding figures (n)** | z = 2.0 two-sided; planning dispersion v̄ = 0.0475; **n_T ≥ 475** for GO, **n_T ≥ 30** to avoid BLOCKED. Never fired: "The power gate never fired, on any venue, over any region." (PMExperiment/README.md:13-14); "Both passes are **absent, not zero**." (PMExperiment/progress.md:759) |
| **file:line** | PMExperiment/pmexperiment/power.py:172-206; PMExperiment/pmexperiment/registry.py:225-228; PMExperiment/REGISTRATION.md:97-137, :299-308; PMExperiment/tests/test_power.py:24-68 |
| **Bar + registration date** | Section 0.3 / 0.4 / 9, commit `9080186` **2026-08-29T07:37:33Z**, before the first request at ~07:44Z (PMExperiment/progress.md:56-58) |
| **Amendments touching the bar** | None. Amendment 2 ordered the band gate ahead of it (REGISTRATION.md:705-708); Amendment 5 added a volume floor to the permitted filter the gate consumes, "It biases every count the gate consumes toward BLOCKED" (registry.py:265-266) |
| **Corrections applied** | Sampling of the unrestricted universe uses the Wilson 95 % **lower** bound of the tail share, the conservative direction (REGISTRATION.md:88-95). Tail cell 91–99 rather than 90–99 "can only shrink the tail count — the conservative direction" (:70-73). **Not applied:** no power term (β), no clustering unit, no multiplicity across the two verdict cells — Section 8 defers "the clustering unit, and the trial grid with its multiplicity correction" to after the gate (REGISTRATION.md:291-295) |
| **Framing in README/report/register** | README:177-192 "**The measurement that was supposed to decide this repository. Not the calibration error. The power to detect one inside the Canadian filter.** It was never reached. … **This repository followed Insider, not NPD**". CLAUDE.md:63-65 "**Follow Insider.**" progress.md:1556-1562 "If an authorization arrived tomorrow the power question would still be unanswered." |
| **Audit notes** | DRAFT-p2-progress-5: z = 2.0 with no z_β is a 95 %-interval half-width, i.e. 50 % power; at 80 % power the same bars are **933** and **59**, and n_T = 30 becomes BLOCKED (MDE 0.1115 > 0.08). Clustering unregistered while the benchmark reports 46,282 contracts across 12,403 events |

## 4. `pmexperiment/admissibility.py` (ADR-012 as code) — the repository's headline contribution

| field | value |
|---|---|
| **Kind** | shipped |
| **Claim as stated** | "A statement about what a source permits carries **a quoted clause, the document's effective date, and the date it was fetched** — or it is recorded **UNMEASURED** and the work proceeds as if permission were absent." — PMExperiment/README.md:35-38 |
| **Deciding figures (n)** | Three required elements (`REQUIRED_ELEMENTS`, admissibility.py:54); client-rendered-shell bar `MIN_DOCUMENT_TEXT_RATIO = 0.05` (:49). Five source-level mutations, all load-bearing, 89 tests green (PMExperiment/progress.md:982-989); thirteen mutations at 95 tests (:1202-1214); fourteen at 108 (:1517-1527); 111 at the final append (:1648) |
| **file:line** | PMExperiment/pmexperiment/admissibility.py:1-190; PMExperiment/progress.md:967-1013; PMExperiment/docs/LICENCES.md:8-13 |
| **Bar + registration date** | ADR-012, recorded **2026-08-30** (admissibility.py:3); module committed `b67fc84` **2026-08-30T04:28:05Z** |
| **Amendments touching the bar** | None. The stage was forbidden to soften it ("**do not soften ADR-012 to admit a candidate**", PMExperiment/progress.md:884) and did not; a version-identity amendment is left as a future, pre-registered option (PMExperiment/docs/LICENCES.md:499-503) |
| **Corrections applied** | Fired over the repository's own three claims first; convicted Stage A's Kalshi finding at **two elements of three** (`Effective` 0 occurrences, `Last Updated` 0) — PMExperiment/progress.md:999-1013. Text-ratio bar found method-dependent (18.05 % vs 67.98 % on the same Dune body) and recorded as a limitation — PMExperiment/docs/LICENCES.md:76-83 |
| **Framing in README/report/register** | README:29-49 "**This is the contribution, and it is the reason the repository is public.** … **It has a known blind spot, found by firing it on correspondence at closure:** the check tests that a clause is non-empty and **cannot tell a quotation from a paraphrase**. Recorded, not repaired" |
| **Audit notes** | Blind spot disclosed by the authors (README:47-49, docs/ACCESS.md:291-300). DRAFT-p2-progress-7: the module's own rule (`admit()` returns UNMEASURED for a claim missing an effective date, "including a claim that permission is absent") was not applied to candidate 3, published PROHIBITED on a "Last updated on" label, while the same page refuses a `dateModified` as an effective date and candidate 2's would-be-permissive verdict fails on exactly that element |

## 5. Amendment 5 — the $1,000 volume floor

| field | value |
|---|---|
| **Kind** | shipped (a registered filter), never exercised |
| **Claim as stated** | "Registered as **Amendment 5**: total traded volume **≥ $1,000** per contract, imported verbatim from the benchmark study whose magnitudes set the registered effect band … **a floor chosen by someone else, before this repository existed, cannot have been tuned to a sample this repository had not yet seen**" — PMExperiment/progress.md:706-712 |
| **Deciding figures (n)** | Threshold $1,000; **cost in sample: not measured, n = 0 contracts enumerated** (PMExperiment/progress.md:714-715) |
| **file:line** | PMExperiment/progress.md:704-718; PMExperiment/pmexperiment/registry.py:261-267; PMExperiment/REGISTRATION.md:853-855 (Amendment 5) |
| **Bar + registration date** | Stated "Made 2026-08-30"; commit `f789079` **2026-08-30T03:34:00Z** — after Stage B's verdict of 2026-08-29 had already recorded the floor as absent |
| **Amendments touching the bar** | It *is* the amendment; the companion spread filter from the same benchmark was deliberately not adopted "because a filter whose sample cost cannot be measured is worse than no filter" (PMExperiment/progress.md:716-718) |
| **Corrections applied** | Provenance-based justification (imported, not chosen); direction of bias named ("biases every count the gate consumes toward BLOCKED", registry.py:265) |
| **Framing in README/report/register** | docs/LICENCES.md:750-755 "Amendment 5's volume floor of $1,000 is registered and **never exercised** — its cost in sample is unmeasured, reported absent rather than as zero" |
| **Audit notes** | Its absence at Stage B is one of the two legs on which BAND-NARROW was excluded — DRAFT-p2-progress-4 |

## 6. Kalshi access gate, fired 2026-08-29 — PENDING_ACCESS

| field | value |
|---|---|
| **Kind** | thresholded negative |
| **Claim as stated** | "**PENDING_ACCESS** (REGISTRATION.md Section 0.5). Conditions 1 and 2 pass; conditions 3 and 4 fail closed as unmeasured or undemonstrated; condition 5 fails closed on the recorded terms." — PMExperiment/docs/ACCESS.md:9-12 |
| **Deciding figures (n)** | Condition 1 PASS: HTTP 200 in 127.6 ms, **2 records** returned. Condition 2 PASS: `result` present, verified on **2 records** against a registered cap of 5. Condition 3 threshold **≥ 1,000 settled markets** — NOT MEASURED, "a single page of 20 returned with a continuation cursor, so the count is > 20 and otherwise unknown". Condition 4 threshold **30 days of price history** — NOT DEMONSTRATED on **n = 1** market ≥ 30 days old (`NASDAQ100-24OCT25-T21499.99`, **0 daily candles** over T−40d..T), "ambiguous, counted as ambiguous". Condition 5 FAIL on terms. Total **13 outbound requests**, 11 API reads. Depth: earliest retrievable close between 2024-01-01 and 2024-05-31, **n = 6 bracketing probes** |
| **file:line** | PMExperiment/docs/ACCESS.md:14-22, :67-89; PMExperiment/progress.md:37-53 |
| **Bar + registration date** | Section 0.5's five conditions with `ACCESS_MIN_SETTLED_MARKETS = 1000` and `ACCESS_OUTCOME_PRESENCE_MAX_RECORDS = 5` (PMExperiment/pmexperiment/registry.py:252-254); registered `9080186` **2026-08-29T07:37:33Z**, before the first request at ~07:44Z |
| **Amendments touching the bar** | None. Amendment 1 moved the venue rather than relitigating the verdict (PMExperiment/progress.md:211-213) |
| **Corrections applied** | All ambiguous readings counted ambiguous (standing rule 15); rate limit **withheld** rather than measured, under ADR-007, because the governing agreement could not be read (docs/ACCESS.md:76). Stage E later found the Kalshi finding met **two ADR-012 elements of three** and recorded it against itself |
| **Framing in README/report/register** | README:115 "Kalshi, keyless | **PENDING_ACCESS** | terms do not sanction keyless systematic retrieval or AI-mediated use without written authorization | 2026-08-29". README:101-106 records that two settled records carrying `last_price_dollars` and `result` **were** received, "rather than rounded to 'no market price was ever read'" |
| **Audit notes** | Sound. Conditions 3 and 4 fail **closed** on n = 20 and n = 1 respectively; the depth claim is phrased as a property of the keyless surface and survived the Kalshi reply (docs/ACCESS.md:317-326) |

## 7. Polymarket access gate, fired 2026-08-30 — PENDING_ACCESS

| field | value |
|---|---|
| **Kind** | negative (on terms, not on a threshold) |
| **Claim as stated** | "**PENDING_ACCESS** — Polymarket's Terms of Use, effective 2026-08-11 and read in full before any repeated fetch, prohibit 'data mining tools, robots, crawlers, or similar data gathering and extraction tools' with no entity-type qualification" — PMExperiment/progress.md:672-678 |
| **Deciding figures (n)** | Terms **59,617 bytes** (Stage C) / **58,830 characters, 14 chunks, zero gaps** (Stage D re-extraction); robots.txt **HTTP 200, 35.7 ms, 73 bytes, no `Disallow`**; **7 requests** to Polymarket hosts, **0 market-data requests**; `artificial intelligence` **0**, `machine learning` **0** in the Terms |
| **file:line** | PMExperiment/docs/ACCESS.md:93-216; PMExperiment/progress.md:670-800; PMExperiment/docs/LICENCES.md:61-74 |
| **Bar + registration date** | Standing rule 12 (terms bind, recorded before any repeated fetch), CLAUDE.md:42-43, registered at scaffold |
| **Amendments touching the bar** | **Amendment 6** retracts Amendment 1's premise — this is a falsification of the repository's own earlier claim, recorded as one, not a rescue (PMExperiment/progress.md:783-796) |
| **Corrections applied** | The strongest counterargument (the crawlers bullet is scoped to "the Site, any other Interface, or Features", and the Terms are not posted at `gamma-api`) is set out in full and rejected on ADR-015 (PMExperiment/progress.md:747-755). The Data clause is recorded as **conditional on entity type** and expressly **not** used as the ground |
| **Framing in README/report/register** | README:116 "Polymarket | **PENDING_ACCESS** | Terms effective 2026-08-11 prohibit the data-gathering tool class, expressly including on-chain | 2026-08-30" |
| **Audit notes** | Sound; the counterargument is recorded against the verdict rather than only for it |

## 8. The three licence candidates, 2026-08-30

| field | value |
|---|---|
| **Kind** | negatives resting on the ADR-012 three-element threshold |
| **Claim as stated** | "**No candidate returns PERMITTED.**" — PMExperiment/docs/LICENCES.md:19; "the calibration question is unmeasurable at this house's standard until an authorization is granted" — :706-707 |
| **Deciding figures (n)** | Candidate 1 **PROHIBITED**: `Notices` **0**, `authorization` **0** across **58,830 characters**; six published addresses, none addressed to this asker. Candidate 2 **UNMEASURED**: CC BY 4.0 stated 3 times, all four gate inputs documented over **1,201,580,990 rows**, 2022-11-21→2026-04-28; fails elements (1) and (2). Candidate 3 **PROHIBITED** (Dune) on a **172,750-byte** body, `aggregat`/`derived`/`redistribut`/`republish`/`resell` **0 occurrences each**; **UNMEASURED** for four other platforms, no document retrieved. Verification: **9 lenses / 3 candidates, 3/3 each**; 13 agents, ~2.1 M subagent tokens, 454 tool uses, 4 died on a session limit |
| **file:line** | PMExperiment/docs/LICENCES.md:17-31, :119-628; PMExperiment/progress.md:1015-1065 |
| **Bar + registration date** | ADR-012's three elements, **2026-08-30**, coded in `admissibility.py` and fired at the repository's own claims first (commit `b67fc84` 2026-08-30T04:28:05Z, one hour before the candidate read `7b5a751` 2026-08-30T06:22:49Z) |
| **Amendments touching the bar** | None; softening was refused (PMExperiment/docs/LICENCES.md:493-503) |
| **Corrections applied** | Adversarial verification overturned candidate 3's central factual claim with one HTTP header; caught two selective quotations; refuted candidate 2 on element (1); deleted a leg of candidate 1's rebuttal; closed the AI/ML axis at a measured null. "**Every correction narrowed or weakened the record, and none changed a verdict**" (PMExperiment/progress.md:1070-1072). Completeness pass recorded nine unread document classes and named the bias direction (PMExperiment/docs/LICENCES.md:665-688) |
| **Framing in README/report/register** | README:117-119 records the three rows and marks candidate 1 "**PROHIBITED** (baseline)". README:130-135 records that Stage D's terminal "there is none" was falsified within two days and that "**The caveat was load-bearing within the week**" |
| **Audit notes** | DRAFT-p2-progress-7 (asymmetric dating standard between candidates 2 and 3). The completeness limits and the two-day falsification are disclosed by the authors, prominently |

## 9. Kalshi Internal Use route, recorded 2026-09-01 — EXISTS-AND-UNTRAVELLED

| field | value |
|---|---|
| **Kind** | open (a route, not a measurement) |
| **Claim as stated** | "**EXISTS-AND-UNTRAVELLED.** A route exists and was **not declined on the merits**; it is gated on an established legal entity, and **nothing was applied for, so nothing was granted and nothing was refused**." — PMExperiment/docs/ACCESS.md:224-226 |
| **Deciding figures (n)** | Three findings, all **as reported by the operator**, none verified against a published instrument; received **2026-09-01**; fee **UNMEASURED**; publishing rights **UNRESOLVED**; AI/ML consent **UNRESOLVED**; historical depth "available" but "**UNMEASURED — never requested**" |
| **file:line** | PMExperiment/docs/ACCESS.md:220-333; PMExperiment/progress.md:1410-1456; PMExperiment/docs/LICENCES.md:793-846 |
| **Bar + registration date** | ADR-012 (2026-08-30) applied to correspondence; returns **UNMEASURED on element (2)** and, in substance, on element (1) |
| **Amendments touching the bar** | The argument that a received date *is* the effective date is recorded "at full strength and **not adopted**" (PMExperiment/progress.md:1426-1432); Amendments 7 and 8 record the prior and the closure, made 2026-09-02 |
| **Corrections applied** | The received date "was not in the prompt and was not synthesized … it was asked for and supplied" (PMExperiment/progress.md:1419-1420). The asymmetry with ADR-014 is stated rather than claimed as credit (:1430-1432) |
| **Framing in README/report/register** | README:120-128 "**The last two rows are the ones a reader should not blur.** … A project that closes on access and a project whose operator stopped paying look identical from outside, and only one of them is a finding." |
| **Audit notes** | Sound. The strongest available temptation — writing an unrefused route as evidence — is explicitly refused |

## 10. H1, H1t, H2, H3 — the hypothesis register

| field | value |
|---|---|
| **Kind** | open |
| **Claim as stated** | "**H1 is unmeasurable at this house's standard. Not disproven, not unlikely, unmeasurable.**" — PMExperiment/README.md:6-8; "**H1t remains UNTESTED** on three grounds including MLCryptoEngine's H2 at **AUC 0.501**" — PMExperiment/progress.md:1553-1554 |
| **Deciding figures (n)** | **Zero** contracts enumerated, **zero** price buckets, **zero** dispersions, **zero** statistics relating a price to an outcome, across five stages (PMExperiment/progress.md:1547-1549). H1t's three grounds: a Kalshi bias reported not to replicate on Polymarket; the largest Polymarket study reporting no general longshot bias; MLCryptoEngine H2 at **AUC 0.501** — the first two carry no citation and no n in `docs/LICENCES.md:653-656` |
| **file:line** | PMExperiment/HYPOTHESES.md:28-30, :97-102, :73-74, :323-324; PMExperiment/progress.md:1487-1490 |
| **Bar + registration date** | Section 16's closure conditions, registered `9080186` 2026-08-29 |
| **Amendments touching the bar** | Six HYPOTHESES amendments (2026-08-29 → 2026-09-02); Amendment 9 adds a fourth reopening condition after closure |
| **Corrections applied** | "**The registered closure conditions were never met.** Section 16 provides for H1 to close when both verdict cells fire BLOCKED with realized MDEs beside them. **Neither fired; no MDE exists.** H1 does **not** close under Section 16 at all." (PMExperiment/progress.md:1487-1490) |
| **Framing in README/report/register** | README:6-14 leads with the unmeasurable verdict and with "The power gate never fired, on any venue, over any region." |
| **Audit notes** | H2 is carried at closure on a rationale that is not its registered one: it was parked as depending on "intraday price history being retrievable at usable depth, **which Stage A measures**" (HYPOTHESES.md:73), and Stage A measured that condition NOT DEMONSTRATED on n = 1; the closure says instead "**H2 and H3 stay PARKED** … Both depended on H1's gate clearing" (HYPOTHESES.md:323-324). Drift in the stated reason, in the direction of leaving a hypothesis open rather than of claiming anything — recorded, not raised as a finding |

## 11. The Stage B direction correction — README contribution #4

| field | value |
|---|---|
| **Kind** | shipped (a finding offered as transferable output) |
| **Claim as stated** | "**The registered FX is proportional to entry price, so every exploitable expression of the band is charged FX at 88–95c rather than at 5–12c** — near the maximum rather than near the minimum." — PMExperiment/README.md:90-92 |
| **Deciding figures (n)** | Bürgi 5c/3 % → NO at **0.950**, underpricing **0.020**, n = 313,972 prices / 46,282 contracts / 12,403 events; Bürgi 95c/98 % → YES at **0.950**, **0.030**, same n; Krause sub-30c/4.0 % → NO at **0.883**, **0.077**, n **not recorded** |
| **file:line** | PMExperiment/docs/BAND.md:145-159; PMExperiment/progress.md:409-414; PMExperiment/README.md:76-95 |
| **Bar + registration date** | Stage B Task 2's registered instruction to establish the unit before computing (prompt logged verbatim, PMExperiment/progress.md:274-285, commit `e2d8f10` 2026-08-29T19:07:37Z, before the arithmetic at 19:15:55Z) |
| **Amendments touching the bar** | None |
| **Corrections applied** | Each magnitude reconstructed both as a gap and as a return and checked against the numbers the registration prints; the post-fee "lose over 60 %" figure explicitly excluded as unusable because "using it against a cost model would charge the fee twice" (PMExperiment/docs/BAND.md:139-143) |
| **Framing in README/report/register** | README:76-95, presented as one of four transferable outputs |
| **Audit notes** | Reproduces exactly in every cell; it is a correction that made the repository's own case worse and was published at the top of the README. Its unacknowledged consequence is that it moves the band top's own source (Krause, 0.883) outside the cell the band is registered for — DRAFT-p2-progress-8 |

## 12. ADR-015 (symmetry of convenience) and the self-audit — README contributions #2 and #3

| field | value |
|---|---|
| **Kind** | shipped |
| **Claim as stated** | "A venue may not be held to a **looser** reading than another because its verdict would be more convenient — and **the rule runs both ways.**" — PMExperiment/README.md:53-54; "ADR-012 stated that 'Stage A's Kalshi finding met that bar.' Fired against itself, it did not: **the Kalshi Data Terms of Use print no date at all** — `Effective` 0 occurrences, `Last Updated` 0" — PMExperiment/README.md:66-69 |
| **Deciding figures (n)** | Dune: bare `curl` **403**, same `curl` with a browser `User-Agent` **HTTP 200**; in-force body **172,750 bytes**. Kalshi PDF: `Effective` **0**, `Last Updated` **0**; `@` **0**, `contact` **0** |
| **file:line** | PMExperiment/docs/LICENCES.md:512-544; PMExperiment/progress.md:1050-1065, :999-1013 |
| **Bar + registration date** | ADR-012 (2026-08-30) and ADR-015 (2026-08-30, `baa2bf3` 2026-08-30T06:35:19Z) |
| **Amendments touching the bar** | None |
| **Corrections applied** | The self-audit is recorded although "**This changes no verdict**" (PMExperiment/progress.md:1006-1010) |
| **Framing in README/report/register** | README:51-74, the second and third of four transferable outputs |
| **Audit notes** | DRAFT-p2-progress-7 finds the symmetry rule not applied to the repository's own dating standard across candidates 2 and 3 |

## 13. The operator prior, 5–8 per cent

| field | value |
|---|---|
| **Kind** | qualified positive framing input (a stated, not registered, prior) |
| **Claim as stated** | "The operator's prior is **5 to 8 percent**, given **2026-09-02 at closure**. Section 13 of `REGISTRATION.md` … **it was never filled, and it is left empty permanently.** The figure is therefore **stated, not pre-registered**" — PMExperiment/README.md:170-175 |
| **Deciding figures (n)** | 5–8 %, given 2026-09-02; Section 13 empty since 2026-08-29 |
| **file:line** | PMExperiment/progress.md:1344-1352, :1478-1485; PMExperiment/REGISTRATION.md:349-353 |
| **Bar + registration date** | Section 13, registered empty `9080186` 2026-08-29T07:37:33Z; a test now fails if it is filled |
| **Amendments touching the bar** | Amendment 7, made 2026-09-02, records the prior as arriving at closure "after the band gate fired on 2026-08-29 and after both access gates" (REGISTRATION.md:1011) |
| **Corrections applied** | The prompt's phrase "a registered prior" was refused and the refusal recorded **before** any document was written about it (PMExperiment/progress.md:1344-1352) |
| **Framing in README/report/register** | README:168-175, and README:20-23 "**a null was the modal expected outcome** … What follows is the method working, not a disappointment" |
| **Audit notes** | Sound, and the strongest single piece of evidence against the thesis that this repository backfills to flatter itself. The one thing to note for the cross-repository pass is that the "null was the modal expected outcome" framing at README:20-23 is carried by a figure the same README says is not pre-registered |

## 14. Thresholds and figures used as bars elsewhere in my documents

| threshold / figure | value | file:line | note |
|---|---|---|---|
| client-rendered-shell bar | text/body ratio **< 0.05** | PMExperiment/pmexperiment/admissibility.py:49 | disclosed as method-dependent: 18.05 % vs 67.98 % on the same body — PMExperiment/docs/LICENCES.md:76-83 |
| outcome-presence cap | **5 records** (2 used) | PMExperiment/pmexperiment/registry.py:254; PMExperiment/docs/ACCESS.md:19 | pre-registered exception to outcome blindness |
| settled-market floor | **≥ 1,000** | PMExperiment/pmexperiment/registry.py:253 | never measured; fails closed |
| maturity rule | **30 days** | PMExperiment/pmexperiment/registry.py:259 | never applied to a real enumeration |
| unrestricted sample | **m = 2,000**, seed **20260829**, Wilson z **1.96** | PMExperiment/pmexperiment/registry.py:248-250 | never drawn |
| mutation counts | 9 → 5 → 6 → 13 → 14 mutations; 34 → 39 → 63 → 72 → 89 → 95 → 108 → **111** tests | PMExperiment/progress.md:190, :233-235, :502-507, :806-813, :1202-1214, :1517-1527, :1648 | three harness faults found and recorded (Entries 7.1, 9.1, 12); "a mutation that does not mutate is not evidence" |
| whole-history credential audit | **32 commits, 189 objects, zero credential-shaped strings** | PMExperiment/progress.md:1537-1543 | git log at the anchor shows 36 commits, 4 of them after the audit ran |
