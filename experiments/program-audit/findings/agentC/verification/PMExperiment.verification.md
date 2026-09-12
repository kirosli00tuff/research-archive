# PMExperiment — verification (VERIFY)

**Agent C (referee/verifier). No thesis.** This document reports what the numbers, the code and
the git objects actually support. A verified claim is recorded as plainly as a contradicted one,
and "unverifiable" is recorded as itself rather than guessed at.

| | |
|---|---|
| Repository | `PMExperiment` |
| Anchored SHA | `03d16e71dbf25a86c529884662d02136f8e82334` (main, 2026-09-02, closed project) |
| Snapshot read | `/home/kiros-li/.cache/program-audit/scratchpad/snap/PMExperiment/` |
| Live repo touched | `/home/kiros-li/Documents/GitHub/PMExperiment/` — read-only git plumbing only (`status --porcelain`, `log`, `show`, `blame`, `rev-list`, `rev-parse`, `ls-tree`, `cat-file -s`) |
| Work dirs | `work/agentC-pm-verify/` (recomputation, this repository) and `/home/kiros-li/.cache/program-audit/scratchpad/work/agentC-PM-verify2/` |
| Python | `/home/kiros-li/.cache/program-audit/scratchpad/venv/bin/python` (numpy/scipy) |
| Verified | 2026-09-11 02:00Z–02:20Z (recomputation and the claim rows) and 2026-09-12 02:30Z–02:50Z (independent re-verification, the power arithmetic, and this document) |
| Inventory used | `findings/agentC/verification/PMExperiment.inventory.{md,json}` (this agent's own) |

## Result in one line

**67 items checked: 40 VERIFIED, 7 CONTRADICTED, 20 UNVERIFIABLE.** Every figure that this
repository derives for itself — the band verdict, the whole 60-cell band table, both power bars,
the cost floor in both of its written forms, the unit-determination table, the margins and their
slacks, the survival counts, the request-count sums, the text-share ratios, the closing git audit
and the eight stage-by-stage suite totals — **reproduces exactly**. The seven contradictions are
six distinct defects (one appears twice, as a claim and as a derived quantity), all of them in
figures that decide nothing, and the twenty unverifiable items are almost all HTTP measurements
whose responses the repository says it deliberately did not retain.

### The single fact that shapes this verification

**This repository contains no stored data artifact of any kind, and never has.** No `.json`,
`.csv`, `.parquet`, `.db` or `.txt` file was ever added at any commit; `data/` holds one 0-byte
`.gitkeep`. So the verifiable surface is exactly two things: **arithmetic over constants that are
themselves registered** (`pmexperiment/registry.py`, pinned line-by-line to quoted sentences of
`REGISTRATION.md` by `tests/test_registry.py`), and **the git objects**. Both were checked
exhaustively here, and both hold up. What cannot be checked — every measurement made over HTTP —
is irreproducible **by construction**, and the repository states this itself:
"the raw probe responses were not retained beyond this report" (`docs/ACCESS.md:87-89`). That is
a real limitation of the evidence, disclosed by its authors, and it is recorded below as
UNVERIFIABLE rather than treated as either confirmation or contradiction.

### What verified, stated plainly

* **MV1, the only verdict this repository ever fired.** `0.02 + 0.01 + 0.03 × 0.95 = 0.0585`
  against `EFFECT_BAND_HI = 0.08`: the "5.85 points against a band top of 8.00 points" is exact
  at four decimal places, and `band.py:96` applies the comparison the registration's own rationale
  registers (existential, at the band top).
* **The whole Pass-1 table: 60 of 60 cells match to four decimal places**, across ten registered
  deciles, two exit routes and three FX turnovers, recomputed from the registered constants alone.
* **Both power bars invert exactly**: `4 × 0.0475 / 0.0004 = 475.0` and
  `4 × 0.0475 / 0.0064 = 29.6875 → 30`, and `tests/test_power.py` fires the verdict map at
  475/474/30/29/0 and pins `MDE(100) = 0.043589` — all five boundaries reproduce.
* **The two written forms of the cost floor are algebraically identical**: `0.04 + 0.01 + 0.03p`
  and `0.05 + 0.03p` agree at every price tested, and `power.py:74-82` implements the same thing.
* **The closing git audit is exact.** "32 commits, 189 reachable objects" reproduces **at
  `1ba50aa`**, which was HEAD when Stage E Task 5 ran (`rev-list --count` = 32,
  `rev-list --objects | wc -l` = 189). At the anchor the same commands give 36 and 213.
* **`docs/BAND.md` has exactly one commit in its entire history** (`34307b6`, 2026-08-29T19:22:44Z)
  and has never been modified since — the "computed once, never recomputed after seeing a result"
  claim is verified by the object store, not by assertion.
* **The suite totals 34 → 39 → 63 → 72 → 89 → 95 → 108 → 111 all reproduce**, and the anchored
  tree holds exactly 111 `def test_` functions.

---

## 1. Claims table

`SoT` = source of truth. Tolerances are per row. The machine-readable rows, with every field the
brief asks for, are in `PMExperiment.claims.json` (67 objects).

### 1.1 The eight MUST-VERIFY claims

| # | claim (abridged) | file:line | stated | SoT | recomputed | tol | status |
|---|---|---|---|---|---|---|---|
| **MV1** | BAND-OPEN - a surviving region exists that the permitted subset admits, at entry prices 91-99c held to resolution, requiring 5.85 points of underpricing at the registered FX turnover against a registered band whose top is 8.00 po… | `REGISTRATION.md:409-412 (also README.md:139-141, docs/BAND.md:15-18, HYPOTH…` | 0.0585 required vs 0.0800 band top (5.85 vs 8.00 points) | pmexperiment/registry.py:9-66 + pmexperiment/band.py:46-80 (read from SNAP), recomputed independently in work/agentC-pm-verify/recompute.py | 0.02 + 0.01 + 0.03*0.95 = 0.058499999999999996 -> %.4f = 0.0585; EFFECT_BAND_HI = 0.08 | exact at 4 dp | VERIFIED |
| **MV2** | fee and half-spread alone total 0.0300 on the held route before any FX at all, against a registered band bottom of 0.0200. No FX treatment, no venue price and no exit route reaches the bottom of the band. | `REGISTRATION.md:456-459 (also report.md:105-108, HYPOTHESES.md:140, docs/BA…` | 0.0300 vs EFFECT_BAND_LO 0.0200 | pmexperiment/registry.py:9-66 + pmexperiment/band.py:46-80 (read from SNAP), recomputed independently in work/agentC-pm-verify/recompute.py | FEE_PER_SIDE_USD 0.02 + HALF_SPREAD_USD 0.01 = 0.03 exactly; 0.03 > 0.02. Strict reading survives at 0/10 buckets on both routes at k=1, 12, inf | exact | VERIFIED |
| **MV3** | There are no crossings inside the tradeable price range. ... R_H(p) = 0.03 + 0.03p ... p = -0.3333 ... p = +1.6667 ... R_X(p) = 0.05 + 0.03p ... p = -1.0000 ... p = +1.0000 - the curve meets the band top exactly at $1.00, a price… | `docs/BAND.md:212-227 (conclusion REGISTRATION.md:448-454)` | -0.3333, +1.6667, -1.0000, +1.0000; 'confirms it to 0.0015' | analytic solution of the same linear cost curves, recomputed in work/agentC-pm-verify/recompute.py | (0.02-0.03)/0.03 = -0.3333; (0.08-0.03)/0.03 = +1.6667; (0.02-0.05)/0.03 = -1.0000; (0.08-0.05)/0.03 = +1.0000; R_X(1.00) = 0.08 exactly; 0.08-0.0785 = 0.0015 | exact at 4 dp | VERIFIED |
| **MV4** | the Pass-1 band table: required underpricing to break even, in probability points, by registered decile, R_H and R_X at k=1, k=12 and k->infinity | `docs/BAND.md:199-210 (four rows reproduced at progress.md:435-440)` | 60 cells at 4 decimal places, 0.0300 to 0.0785 | pmexperiment/registry.py:9-66 + pmexperiment/band.py:46-80 (read from SNAP), recomputed independently in work/agentC-pm-verify/recompute.py | all 60 cells reproduced from registry constants alone; 0 mismatches at '%.4f' | string equality at '%.4f' | VERIFIED |
| **MV5** | route H clears by 4.84 points at 1-10c falling to 2.15 points at 91-99c; route X clears by 2.83 points falling to 0.15 points at 91-99c. Route X's margin at the favourite tail (0.0015) is smaller than the 0.00195 by which Section… | `docs/BAND.md:255-265 (exclusion at REGISTRATION.md:426-429)` | 4.84, 2.83, 2.15, 0.15 points; slacks 0.00195 and 0.00135; factor 16; 5.73 at 91c rising to 5.97 at 99c | pmexperiment/registry.py:9-66 + pmexperiment/band.py:46-80 (read from SNAP), recomputed independently in work/agentC-pm-verify/recompute.py; slack formula read from tests/test_band.py:134-1… | 0.08-0.03165 = 0.048350000000000004 -> '%.2f' of 100x = 4.84; 0.08-0.05165 = 0.02835 -> '%.2f' of 100x = 2.83; 0.08-0.0585 = 0.0215; 0.08-0.0785 = 0.0015; 0.03*0.05 + 0.015*0.03 = 0.0015+0.00045 = 0.00195; 0.03*0.03+0.015*0.03 = 0.00135; 0.0215/0.00135 = 15.926 -> 16; R_H(0.91)=0.0573, R_H(0.99)=0.0597 | exact at 2 dp in points | VERIFIED |
| **MV6** | Burgi's 5c contract winning 3 % \| 0.03 - 0.05 = -0.02 ... -0.02/0.05 = -40.0 % ... Burgi's 95c contract winning 98 % \| +0.03 \| +3.16 % \| Krause's -0.077 ... implies a mean bucket price of 0.117 ... implies a mean price of 0.0… | `docs/BAND.md:128-137 and 151-155 (also DECISIONS.md:221-231, 246-250, RE…` | -0.02 / -40.0 %; +0.03 / +3.16 %; 0.117 and 0.043; entry prices 0.950, 0.950, 0.883; 0.030 and 0.057 for the 60 %-loss… | hand arithmetic over figures quoted from the two publications; recomputed independently | 0.03-0.05 = -0.02, -0.02/0.05 = -40.0 %; 0.98-0.95 = +0.03, 0.03/0.95 = +3.1579 % (printed '+3.16', source's own '+3.1'); 0.04+0.077 = 0.117; 0.04/(1-0.077) = 0.043337; 1-0.117 = 0.883; 0.6*0.05 = 0.030; 0.6*0.095 = 0.057; R_H(0.883) = 0.0565, R_X(0.883) = 0.0765 | exact at the printed precision | VERIFIED |
| **MV7** | \| GO, MDE <= 0.02 \| >= 475 \| \| stay out of BLOCKED, MDE <= 0.08 \| >= 30 \| [at v-bar = 0.0475, so sqrt(v-bar) ~ 0.218] | `REGISTRATION.md:120-137` | 475, 30, 0.0475, 0.218 | pmexperiment/power.py:37-45 inverted; recomputed independently | 4*0.0475/0.02^2 = 475.0 exactly; 4*0.0475/0.08^2 = 29.6875 -> >= 30; 0.05*0.95 = 0.0475; sqrt = 0.217945 -> 0.218; MDE(475) = 0.020000 exactly, MDE(474) = 0.020021, MDE(30) = 0.079582, MDE(29) = 0.080943 | exact | VERIFIED |
| **MV8** | At the published two-thirds tail share, GO needs about 703 markets (475 / 0.676); the floor of 1,000 leaves margin for a lower realized share. | `REGISTRATION.md:148-150` | 703 markets, divisor 0.676, premise 'two-thirds' | arithmetic over the stated premise; the divisor 0.676 appears exactly once in the repository and nowhere else (grep over SNAP) | 475/0.676 = 702.66 (so '703' follows from 0.676), but 475/(2/3) = 712.5 and 475/0.667 = 712.14 | +/- 1 market | **CONTRADICTED** |
| **MV9** | C(p) = 0.04 + 0.01 + 0.03*p ... the floor is 0.0785 [Section 2]; C(p) = 0.05 + 0.03*p ... C(0.95) = 0.0785. C(0.05) = 0.0515. [Section 11] | `REGISTRATION.md:203-212 and 335-338` | 0.0785 and 0.0515, in two written forms | pmexperiment/power.py:74-82; cross-pinned by tests/test_band.py:30-41 and tests/test_power.py:76-79 | both forms give 0.0785 at p=0.95 and 0.0515 at p=0.05, and both equal power.cost_floor's expression exactly (float-identical) | exact | VERIFIED |

### 1.2 The remaining claims (inventory ranks 9–26, plus added rows)

| claim (abridged) | file:line | recomputed / source of truth | status |
|---|---|---|---|
| earliest retrievable settled close sits between 2024-01-01 (empty page) and 2024-05-31 (present), bracketed by max_close_ts probes ... n = 6 probes | `docs/ACCESS.md:72 (also REGISTRATION.md:389-393, DECISIONS.md:100-105)` | not recomputable; the six probe DATES as logged (2021-08-01, 2022-01-01, 2023-01-01, 2024-01-01 empty; 2024-07-01, 2025-01-01 non-empty) bracket [2024-01-01, 2024-07-01], not [2024-01-01, 2024-05-31] | UNVERIFIABLE |
| keyless API reachability \| HTTP 200, latencies 99.9-213.8 ms across 11 requests ... 13 outbound requests total on 2026-08-29 ... 2 robots.txt fetches (429, 404) and 11 API reads - 2 settled-listing… | `docs/ACCESS.md:71 and 80-89 (also progress.md:41)` | internal arithmetic only: 2+6+3 = 11 API reads and 2+11 = 13 total, both consistent; the latencies and record counts cannot be recomputed | UNVERIFIABLE |
| robots.txt, polymarket.com \| HTTP 200 \| 35.7 ms \| 73 bytes ... 7 requests to Polymarket hosts on 2026-08-30 ... 4 robots.txt (200, 404, 404, 404), 1 /tos page, 1 docs.polymarket.com, 1 rendered re… | `docs/ACCESS.md:106-111 and 210-216` | internal arithmetic only: 4+1+1+1 = 7, consistent, plus 1 docs.google.com fetch counted separately | UNVERIFIABLE |
| Terms of Use \| read in full, 59,617 bytes [ACCESS] vs 58,830 characters / 59,061 bytes, against the 59,617 bytes Stage C recorded [LICENCES]; and 217 KB body ... 1,354 characters vs 217,045 bytes ->… | `docs/LICENCES.md:61-62 and 72-73 (against docs/ACCESS.md:122 and 126-12…` | derived shares are each coherent with their own numerator: 1405/217045 = 0.6473 % ('0.65 %') and 1354/217045 = 0.6238 % ('near 0.6 %', pmexperiment/admissibility.py:41) | UNVERIFIABLE |
| Notices - 0 occurrences, Notice - 0 ... authorization - 0 occurrences ... Searched over the full 58,830 characters; [and the Kalshi PDF] Effective 0, Last Updated 0 ... in a 6,648-char document | `docs/LICENCES.md:195-199, 261-267, 280, 332-337, 582-586` | none - no document body or PDF is stored at any commit | UNVERIFIABLE |
| TimeSeventeen/Polymarket-v1 ... OrderFilled/ 1,201,580,990 rows (~49.1 GB compressed Parquet), coverage 2022-11-21 to 2026-04-28 | `docs/LICENCES.md:348-384 and 465-473` | external dataset cards; nothing retained | UNVERIFIABLE |
| dune.com/pricing is a client-rendered shell in both the archived copy (56,756 bytes -> 81 characters, 0.14 %) and live (67,316 bytes -> 269 characters, 0.40 %) ... the verification pass measured 18.0… | `docs/LICENCES.md:78-82, 328-331, 528-532, 590-597, 601-609` | the two shell shares are internally exact: 81/56756 = 0.1427 % and 269/67316 = 0.3996 % | UNVERIFIABLE |
| 13 agents, ~2.1 M subagent tokens and 454 tool uses across two passes, four of which died on a session limit ... All 17 quoted or attributed strings ... 14 match byte-for-byte; 3 differ only in typog… | `progress.md:959-960 (also docs/LICENCES.md:97, 614-618, 91-95)` | internal arithmetic only: 14 + 3 = 17, consistent | UNVERIFIABLE |
| Restored, 111 pass, lint and typecheck clean (and 34, 39, 63, 72, 89, 95, 108 at the earlier stages) | `progress.md:1648 (also :12, :235, :507, :813, :986, :1214, :1527)` | 98ce2d4=34, f686036=39, ebdc116=63, 52d39ec=72, 80b9b9d/e6f6f3c=89, baa2bf3=95, 3aca2d1=108, 03d16e7 (HEAD)=111. Every stated total reproduces exactly at the commit it is claimed for. | VERIFIED |
| 32 commits, 189 reachable objects, every blob decompressed and scanned: zero credential-shaped strings ... .env.example, which is 294 bytes, five comment lines, and contains no '=' at all ... LICENSE… | `progress.md:1537-1543` | at 1ba50aa (HEAD when the Stage E Task 5 audit ran): rev-list --count = 32, rev-list --objects \| wc -l = 189 - both exact. .env.example = 294 bytes, 5 lines, 0 occurrences of '='. LICENSE = MIT, 'Copyright (c) 2026 kirosli00tuff', 21 physical lines / 17 non-blank. At the anchored HEAD the same com… | VERIFIED |
| Stage B total: 22.9 min against a 75-min stated ETA (19:05:53Z -> 19:28:45Z), overrun by a factor of 3.3 in the safe direction ... Stage E total: ~21.4 min against 50 min stated (09:22:59Z -> 09:44:2… | `progress.md:534-535 and 1573-1574 (also :836, :942, :1255-1261, :1…` | 19:05:53->19:28:45 = 22.87 min ('22.9'); 75/22.9 = 3.28 ('3.3'); 09:22:59->09:44:22 = 21.38 min ('21.4'); 21.4/50 = 42.8 % ('43 %'); 09:36:29->09:44:22 = 7.88 min ('7.9'); 135/55 = 2.45 ('2.5'); 111/20 = 5.55 ('5.5'); 7.8/8 = 2.5 % under ('within 3 %') | VERIFIED |
| the registered constants, each pinned to a quoted sentence of REGISTRATION.md: 0.02 to 0.08, z = 2.0 two-sided, the ten deciles and the tail cell, m = 2,000, seed 20260829, Wilson 95% lower bound, at… | `pmexperiment/registry.py:1-66 (pinned by tests/test_registry.py:22-99)` | nine test functions assert each constant against a whitespace-folded substring of REGISTRATION.md; every constant the band gate consumes is covered, and FX_TURNOVER_REGISTERED is additionally pinned at tests/test_band.py:182-184 | VERIFIED |
| realized minimum detectable contrast came in at 0.0512 against a realistic effect band of 0.01 to 0.05 ... after 415 days of collection and 6.9378 USD of spend; InsiderExperiment ... fired BLOCKED at… | `REGISTRATION.md:31-47 and 710-712 (also README.md:182-188, CLAUDE.md:5…` | other repositories in this program (NPDExperiment, InsiderExperiment, MLCryptoEngine) | UNVERIFIABLE |
| 313,972 Yes-and-No contract prices on 46,282 contracts across 12,403 events ... a 5c contract that wins 3 % of the time returns -40 % before fees; a 95c contract winning 98 % returns +3.1 % ... [Krau… | `REGISTRATION.md:225-251 (quoted at docs/BAND.md:37-63)` | external publications; no copy, PDF or extract is stored in the repository | UNVERIFIABLE |
| Five stages. Zero dollars. Zero contracts enumerated. Zero market-data requests to Polymarket. Zero requests of any kind in Stage E. No price bucket, no dispersion, and no statistic relating a price… | `report.md:476-478 (also README.md:16, REGISTRATION.md:628-630, p…` | the 'no statistic' half VERIFIES: no data-shaped file was ever added at any of the 36 commits; an independent grep over all 10 documents and 12 Python files for p-value / confidence interval / standard error / bootstrap / significan / bonferroni / multiplicity returns exactly two hits, both about m… | UNVERIFIABLE |
| The operator's prior is 5 to 8 percent, given 2026-09-02 at closure ... The figure is therefore stated, not pre-registered | `README.md:168-175 (also REGISTRATION.md:1015-1029, HYPOTHESES.md…` | Section 13 still reads 'To be filled by the operator before the gate fires' and carries no figure; the honesty suite asserts that the section body contains neither 'percent' nor '%' and that the prior is never called pre-registered | VERIFIED |
| rate limit, documented claim \| Basic tier 200 reads/s (docs.kalshi.com/getting_started/rate_limits, read 2026-08-29); tiers are defined for API-key holders \| claim, not a measurement | `docs/ACCESS.md:75 (also DECISIONS.md:132-133, progress.md:45)` | external vendor documentation; not retained | UNVERIFIABLE |
| the one >= 30-day-old settled market tested (NASDAQ100-24OCT25-T21499.99, closed 2024-10-25) returned HTTP 200 and 0 daily candles over T-40d..T; ambiguous, counted as ambiguous, attributed to nothing | `docs/ACCESS.md:21 (also progress.md:44)` | none retained | UNVERIFIABLE |
| Every figure is computed by `pmexperiment.band` and pinned by `tests/test_band.py`, so nothing here is hand arithmetic. | `docs/BAND.md:8-9` | band.py contains no solver for the crossing prices and no probability-gap/return conversion; grep over pmexperiment/ and tests/ for 0.3333, 1.6667, 3.16, 0.117, 0.883, 0.043 and -40 returns no hit outside one docstring phrase. The Task 2 unit-determination table (docs/BAND.md:128-137, 151-155) and… | **CONTRADICTED** |

## 2. Derived quantities table

Every row was recomputed by me from the stored primitives named in the middle column —
registered constants, logged counts, git objects — never copied from a document.

| derived quantity (abridged) | file:line | method / primitives | recomputed | tol | status |
|---|---|---|---|---|---|
| the surviving region is the top 2.15 points of a 6-point band | `docs/BAND.md:330 (also REGISTRATION.md:433, HYPOTHESES.md…` | registered constants | 0.08 - 0.0585 = 0.0215 (2.15 pts); 0.08 - 0.02 = 0.06 (6.0 pts) | exact | VERIFIED |
| the arithmetic confirms it to 0.0015 | `REGISTRATION.md:448-454` | registered constants | 0.08 - 0.0785 = 0.0015 (float 0.0015000000000000013) | 1e-15 | VERIFIED |
| Section 2's FX base understates cost by 0.03 x 0.05 = 0.0015 plus 0.015 x 0.03 = 0.00045, sum 0.00195 (route X) and 0.00135 (route H) | `docs/BAND.md:181-187` | tests/test_band.py:134-146 formula, recomputed independently | 0.03*(0.04+0.01) + 0.015*(0.98-0.95) = 0.0015 + 0.00045 = 0.00195; 0.03*(0.02+0.01) + 0.00045 = 0.00135 | exact | VERIFIED |
| Route H's margin ... larger by a factor of 16 | `docs/BAND.md:264-265` | registered constants | 0.0215 / 0.00135 = 15.926 | rounds to the nearest integer | VERIFIED |
| route H clears by 4.84 points at 1-10c; route X clears by 2.83 points | `docs/BAND.md:257-259` | registered constants | 100*(0.08-0.03165) = 4.835000000000001 -> '%.2f' = 4.84; 100*(0.08-0.05165) = 2.8349999999999995 -> '%.2f' = 2.83 | exact at 2 dp | VERIFIED |
| 5.73 points at 91c rising to 5.97 at 99c | `REGISTRATION.md:423-424 (also docs/BAND.md:317-318)` | registered constants | 0.03+0.03*0.91 = 0.0573; 0.03+0.03*0.99 = 0.0597 | exact at 4 dp | VERIFIED |
| Krause, sub-30c/4.0 % -> NO at 88.3c \| 0.077 \| 0.0565 clears \| 0.0765 clears | `docs/BAND.md:253` | registered constants | 0.03+0.03*0.883 = 0.05649 -> 0.0565; 0.05+0.03*0.883 = 0.07649 -> 0.0765 | exact at 4 dp | VERIFIED |
| the 3.0 exactly ties the fee-plus-spread floor of 0.0300 even with FX driven to zero | `REGISTRATION.md:433-436` | registered constants | required_underpricing(0.95, HELD, turnover=inf) = 0.03 exactly; Burgi's gap = 0.03; band.py:96 uses strict '<', so the tie does NOT survive - consistent with the document calling it a dead heat, not a clearance | exact | VERIFIED |
| existential reading 10/10 buckets at k = 1, 12 and infinity on both routes; strict reading 0/10 at every k | `docs/BAND.md:233-234` | pmexperiment/band.py:83-122 re-implemented independently | existential 10/10 for routes H and X at k = 1, 12, inf; strict 0/10 for both routes at all three k | exact | VERIFIED |
| FX at p = 0.95: k = 1 -> 0.0285; k = 12 -> 0.0024; k -> infinity -> 0.0000 | `docs/BAND.md:175-179` | pmexperiment/band.py:51-65 | 0.03*0.95 = 0.0285; 0.0285/12 = 0.002375 -> '%.4f' = 0.0024; inf -> 0.0 | exact at 4 dp | VERIFIED |
| MDE at n = 100 equals 0.043589 | `tests/test_power.py:24-34` | pmexperiment/power.py:37-45 | 2*sqrt(0.0475/100) = 0.0435890 | 1e-6 | VERIFIED |
| GO boundary inclusive at 475; 474 DEGRADED; 30 DEGRADED; 29 BLOCKED; 0 BLOCKED with mde None | `tests/test_power.py:37-68` | pmexperiment/power.py:48-71 | MDE(475) = 0.0200000 exactly (GO, lower edge inclusive); MDE(474) = 0.020021 (DEGRADED); MDE(30) = 0.079582 (DEGRADED); MDE(29) = 0.080943 (BLOCKED) | exact | VERIFIED |
| sqrt(v-bar) ~ 0.218 at the planning dispersion 0.0475 | `REGISTRATION.md:122-123` | arithmetic | 0.05*0.95 = 0.0475; sqrt(0.0475) = 0.2179449 | 3 dp | VERIFIED |
| the two written forms of the cost floor agree: 0.04 + 0.01 + 0.03p and 0.05 + 0.03p | `REGISTRATION.md:206 vs 335` | pmexperiment/power.py:74-82 | float-identical at p = 0.95 and p = 0.05, and identical to power.cost_floor and to band.required_underpricing(p, EXITED_BEFORE_RESOLUTION, 1.0) | exact | VERIFIED |
| 13 outbound requests = 2 robots.txt + 11 API reads; 11 = 2 settled-listing + 6 depth brackets + 3 candlestick | `docs/ACCESS.md:80-85` | internal arithmetic on the stated composition | 2+6+3 = 11; 2+11 = 13 | exact | VERIFIED |
| 7 requests to Polymarket hosts = 4 robots.txt + 1 /tos + 1 docs.polymarket.com + 1 rendered /tos | `docs/ACCESS.md:210-213` | internal arithmetic | 4+1+1+1 = 7, with the docs.google.com fetch counted separately as stated | exact | VERIFIED |
| earliest retrievable settled close bracketed between 2024-01-01 and 2024-05-31 by n = 6 probes | `docs/ACCESS.md:72 (restated REGISTRATION.md:391, DECISIONS.…` | the six probe dates as logged in the same table cell | the six logged probes (2021-08-01, 2022-01-01, 2023-01-01, 2024-01-01 empty; 2024-07-01, 2025-01-01 non-empty) bracket [2024-01-01, 2024-07-01]; 2024-05-31 is not among them and is not implied by them | n/a | **CONTRADICTED** |
| All 17 quoted or attributed strings ... 14 match byte-for-byte; 3 differ only in typographic apostrophes | `docs/LICENCES.md:614-618` | internal arithmetic | 14 + 3 = 17 | exact | VERIFIED |
| 217,045 bytes -> 1,405 characters, 0.65 % text; [and] a text share near 0.6 % [from 1,354 characters] | `docs/LICENCES.md:61-62 (and pmexperiment/admissibility.py:41)` | internal arithmetic on the stated counts | 1405/217045 = 0.6473 %; 1354/217045 = 0.6238 % | +/- 0.005 pp | VERIFIED |
| 56,756 bytes -> 81 characters, 0.14 %; 67,316 -> 269 characters, 0.40 % | `docs/LICENCES.md:590-597` | internal arithmetic | 81/56756 = 0.1427 %; 269/67316 = 0.3996 % | +/- 0.005 pp | VERIFIED |
| the suite totals stage by stage: 34, 39, 63, 72, 89, 95, 108, 111 | `progress.md:12, 235, 507, 813, 986, 1214, 1527, 1648` | git objects: grep -c '^def test_' over tests/*.py at each of the 36 commits (live repo, read-only) | 34 at 98ce2d4, 39 at f686036, 63 at ebdc116, 72 at 52d39ec, 89 at 80b9b9d, 95 at baa2bf3, 108 at 3aca2d1, 111 at 03d16e7 | exact | VERIFIED |
| Stage C report ... and nine honesty tests [commit subject of 52d39ec] | `git commit 52d39ec (subject line)` | git show 52d39ec -- tests/ (live repo, read-only) | exactly 8 test functions added, 0 removed; the suite moves 64 -> 72 | exact | **CONTRADICTED** |
| Made 2026-08-30 [Amendments 1, 2 and 3]; Status: accepted, 2026-08-30 [the second ADR-006 and ADR-007] | `REGISTRATION.md:667, 707, 751 (and DECISIONS.md:140, 160)` | git blame + git log on the live repo (read-only) | all five lines are owned by commit f686036, author and committer date 2026-08-29T11:05:26-07:00 = 2026-08-29T18:05:26Z - 2026-08-29 in UTC and in the committer's own local timezone alike | exact | **CONTRADICTED** |
| 32 commits, 189 reachable objects [the closing audit] | `progress.md:1537-1538` | git rev-list on the live repo (read-only) | rev-list --count 1ba50aa = 32; rev-list --objects 1ba50aa \| wc -l = 189; at the anchored HEAD 03d16e7 the same commands give 36 and 213 | exact | VERIFIED |
| no stored data artifact of any kind exists, at any commit | `REGISTRATION.md:320-321 and 359-363 (the data/raw/ reproduci…` | git log --all --diff-filter=A --name-only on the live repo; ls -laR data/ on the live tree at 2026-09-11T02:09Z | 32 distinct files ever added, none with a data extension; data/ holds a single 0-byte .gitkeep; data/raw/ does not exist | n/a | UNVERIFIABLE |
| GO \| MDE <= 0.02 \| the design resolves the entire published band; Stage B is authorized for that universe against the registered target | `REGISTRATION.md:110 (the GO row of the verdict map; bar at 1…` | pmexperiment/power.py:37-45 (the estimator as coded), REGISTRATION.md:99-106 and 120-129 (z, v-bar and the bar); power recomputed with scipy.stats.norm in work/agentC-PM-verify2/power_check… | at n_T = 475 and v-bar = 0.0475, SE = sqrt(0.0475/475) = 0.010000 exactly; a true effect of 0.02 is two-sided significant with probability 0.5000 at z = 2.0 (0.5160 at z = 1.96). A bar that resolves 0.02 at the conventional 80 % power is n_T = 959 (z = 2.0) or 933 (z = 1.96) - 2.0x the registered b… | power to 4 dp; n to 1 contract | **CONTRADICTED** |
| At the published two-thirds tail share, GO needs about 703 markets (475 / 0.676) | `REGISTRATION.md:148-150` | arithmetic over the premise stated in the same sentence and at REGISTRATION.md:132-134 | 475/0.676 = 702.66 -> 703 (the printed quotient is internally right); 475/(2/3) = 712.50; 475/0.667 = 712.14 | +/- 1 market | **CONTRADICTED** |

## 3. Intervals table

| # | interval | file:line | estimator actually used | independence assumed? | data structure — is that assumption doubtful? | reproduces? | status |
|---|---|---|---|---|---|---|---|
| I1 | no confidence interval, standard error or interval estimate is reported anywhere in this repository | `README.md:13-14 (also REGISTRATION.md:384-387, HYPOTHESES.m…` | — | — | none - no sample was ever drawn | exactly two hits, both referring to machinery that never ran: DECISIONS.md:15 ('two multiplicity accounts') and REGISTRATION.md:294 (Section 8, unfilled) | VERIFIED |
| I2 | the gate consumes n_T = N times the Wilson 95% lower bound of the sampled tail share | `REGISTRATION.md:88-95 and 303-304 (constant at pmexperiment/regis…` | Wilson score interval, lower endpoint | Yes | a uniform random sample of m = 2,000 settled markets without replacement, seed 20260829, from an enumerated universe of N; the estimand is a tail SHARE over markets | not reproducible - no universe was ever enumerated, so no sample was ever drawn and no bound was ever computed. The constant 1.96 is the z of a TWO-sided 95 % interval (equivalently a one-sided 97.5 % bound); a one-sided 95 % lower bound conventionally uses 1… | UNVERIFIABLE |
| I3 | Section 8, Inference. *To be registered after the gate fires.* The estimator, the interval construction, the clustering unit, and the trial grid with its multiplicity co… | `REGISTRATION.md:291-295` | none registered | — | would have been a panel of contracts within events within series - repeated measurement within event is the obvious clustering unit and the section names 'the clustering unit' as something still to be registered | still unfilled at HEAD | VERIFIED |


### 3.1 What "independence" would have meant here, and why it never got tested

The brief asks, for every interval, whether the data structure makes the independence assumption
doubtful and whether the interval reproduces from stored data. **No interval was ever
constructed in this repository**, so the second question has one answer everywhere: it does not
reproduce because it was never computed, and no sample exists from which to compute it. The first
question still has a real answer, and it is worth recording:

* **I2, the Wilson bound, would not have had a clustering problem.** Its sampling unit is the
  market and its estimand is a share over markets, drawn uniformly without replacement from one
  enumerated universe with a registered seed. Independence is assumed by construction and the
  construction would have supplied it. The finite-population correction is not mentioned; it
  would only have made the bound more conservative.
* **The gate the bound feeds would have had one.** `n_T` enters `MDE = z·sqrt(v̄/n_T)` as if the
  tail cell held `n_T` independent contracts. Contracts are nested in events and events in series
  — one event contributes several contracts whose outcomes resolve together — so the effective n
  is below the raw count and the MDE is optimistic by a factor of `sqrt(1 + (m̄−1)ρ)`. The
  registration knows this is a live question: Section 8 names **"the clustering unit"** as
  something still to be registered (`REGISTRATION.md:291-295`). It was never filled, because the
  gate never fired.
* **On the naming of I2.** `WILSON_Z = 1.96` is labelled "the 95% lower bound"
  (`pmexperiment/registry.py:33`). Read as the lower endpoint of the two-sided 95 % Wilson
  interval — the ordinary usage — 1.96 is exactly right; read as a one-sided 95 % bound, the
  conventional constant is 1.645 and 1.96 delivers 97.5 %. **I do not raise this**: the usage is
  standard, and the ambiguity's direction is the conservative one the registration says it wants
  ("understating the tail count rather than overstating it", `REGISTRATION.md:93-94`).

## 4. Tests table

| # | test statistic / decision rule | file:line | tail | dof / distribution | correction applied | decision-rule type | correction matches rule? | reproduces? | status |
|---|---|---|---|---|---|---|---|---|---|
| T1 | MDE = z * sqrt(v-bar / n_T), with z = 2.0 two-sided | `REGISTRATION.md:99-106 and 301-308 (pmexperiment/power.py:37…` | two-sided (z = 2.0 is a rounded 1.96; the rounding directio… | normal approximation, no dof | none | single | n/a — none owed | the formula in code is exactly z*sqrt(v/n) with z = registry.Z_CRITICAL = 2.0; it was never evaluated on any cell | UNVERIFIABLE |
| T2 | GO MDE <= 0.02; DEGRADED 0.02 < MDE <= 0.08; BLOCKED MDE > 0.08 or n_T = 0; boundaries inclusive at the lower edge | `REGISTRATION.md:105-112 (pmexperiment/power.py:48-71)` | — | — | none | single | Yes | implemented exactly as registered, including n_T = 0 -> BLOCKED with mde None; verified at n = 475/474/30/29/0 | VERIFIED |
| T3 | v-bar, the null Bernoulli dispersion, is the mean of p_i(1-p_i) over the cell's snapshot prices. It is computed from prices alone. No outcome enters… | `REGISTRATION.md:75-77` | — | — | none | — | n/a — none owed | no v-bar was ever computed; the outcome-blindness guard exists and is itself fed a violation in tests/test_guards.py | UNVERIFIABLE |
| T4 | prices near 5c or 95c give p(1-p) ~ 0.0475, so sqrt(v-bar) ~ 0.218 | `REGISTRATION.md:122-123 (tests/test_power.py:21)` | — | — | none | — | n/a — none owed | 0.05*0.95 = 0.0475; sqrt = 0.2179449 | VERIFIED |
| T5 | planning bars n_T >= 475 (GO) and n_T >= 30 (out of BLOCKED) | `REGISTRATION.md:126-129` | two-sided z = 2.0 | normal approximation | none | single | n/a — none owed | 4*0.0475/0.0004 = 475.0 exactly; 4*0.0475/0.0064 = 29.6875 -> 30 | VERIFIED |
| T6 | boundary assertions: n=475 -> MDE 0.02 GO; 474 -> DEGRADED; 30 -> DEGRADED; 29 -> BLOCKED; 0 -> BLOCKED with mde None; MDE at n=100 == 0.043589 | `tests/test_power.py:24-73` | — | — | none | single | n/a — none owed | all five verdicts and the 0.043589 figure reproduce exactly | VERIFIED |
| T7 | imported: MLCryptoEngine H2 cross-venue transfer at AUC 0.501 | `HYPOTHESES.md:103 (and 11 further occurrences across 6 fil…` | — | — | none stated here | — | n/a — none owed | — | UNVERIFIABLE |
| T8 | imported: NPD realized minimum detectable contrast 0.0512 against a band of 0.01 to 0.05, after 415 days and 6.9378 USD | `REGISTRATION.md:31-44` | — | — | none | — | n/a — none owed | — | UNVERIFIABLE |
| T9 | imported: InsiderExperiment fired BLOCKED at 49.35 bp before spending | `REGISTRATION.md:46-47` | — | — | none | — | n/a — none owed | — | UNVERIFIABLE |

### 4.1 Tails, degrees of freedom and multiplicity

* **Tail.** The only tail anywhere is `z = 2.0 two-sided` (`REGISTRATION.md:99`, `:301`,
  `registry.py:9`), and the code applies exactly that. 2.0 is a rounded 1.96, and the rounding
  enlarges the MDE — the conservative direction. There is no registered direction of effect to
  mismatch it against: H1 is registered as a two-sided calibration question, and Section 8, which
  would have registered the estimator and the trial grid, was never filled.
* **Degrees of freedom.** Nothing uses a t distribution, a chi-square or an F. Every figure is a
  normal approximation on a proportion, so no dof is owed and none is stated.
* **Multiplicity, and whether the correction matches the rule it feeds.** Two questions arise and
  both come out clean:
  1. **The power gate fires over two verdict cells** (U24 and P30) and applies **no** correction.
     The decision rule is not a family-wise claim: each cell carries its own verdict and a split
     verdict is registered *in advance* as its own reportable finding (`REGISTRATION.md:113-118`).
     Per-cell reporting owes no correction, so the absence matches the rule.
  2. **The band gate's rule is a union over ten deciles** — "a surviving region exists at any
     bucket" — which is exactly the shape where a union-type correction would be owed *if the
     comparisons were statistical*. They are not: all sixty are exact arithmetic comparisons
     between two registered constants with no sampling error, so multiplicity does not arise.
     The strict (all-must-pass) reading is reported beside the existential one rather than
     substituted for it (`docs/BAND.md:229-234`), which is the honest way to expose a quantifier.
* **No p-value, no test statistic and no standard error is reported anywhere in this
  repository** — a negative I re-verified independently by grep over all ten documents and all
  twelve Python files. The two hits are Section 8's unfilled placeholder and one sentence of
  `DECISIONS.md` about multiplicity accounts in other repositories.


---

## 5. Draft findings

Six findings, from seven CONTRADICTED rows (the `475 / 0.676` defect appears twice, once as a
claim and once as the derived quantity). **None of them moves the repository's verdict**, and I
say so in each. Temporary IDs; the consolidator assigns final ones.

### DRAFT-V-1
- **Repository / SHA:** PMExperiment / `03d16e71dbf25a86c529884662d02136f8e82334`
- **Hypothesis or artifact:** Section 0.5, the access gate — clause 3's derived market requirement
- **Direction:** B
- **Class:** ARITHMETIC
- **Severity:** S4
- **Label:** DERIVED
- **Claim challenged (verbatim quote):** "At the published two-thirds tail share, GO needs about 703 markets (475 / 0.676); the floor of 1,000 leaves margin for a lower realized share." — PMExperiment/REGISTRATION.md:148-150
- **Evidence:**
  - The premise, in the same registration: "The published benchmark (Section 3) reports **two-thirds** of its 313,972 contract prices in the 1–10c and 90–99c bands" — PMExperiment/REGISTRATION.md:132-134.
  - The numerator verifies: "| GO, MDE ≤ 0.02 | ≥ 475 |" — PMExperiment/REGISTRATION.md:128 — reproduces exactly as `2.0² × 0.0475 / 0.02² = 475.0`.
  - **`0.676` occurs exactly once in the entire snapshot** (grep over all files, n = 1 hit, that line). It is defined nowhere, attributed to nothing, and pinned by no test.
- **Recomputation (if any):** inputs `REGISTRATION.md:128` (475) and `REGISTRATION.md:132-134` (two-thirds); method: division; results `475 / 0.676 = 702.66 → 703` (so the printed quotient is internally correct), `475 / (2/3) = 712.5`, `475 / 0.667 = 712.14`. Tolerance ± 1 market. Script: `scratchpad/work/agentC-PM-verify2/power_check.py`.
- **What would resolve it:** the tail share the benchmark actually reports, to three decimals — an external figure the repository never quotes — or one sentence saying where 0.676 came from. If the benchmark really reports 67.6 %, the sentence's own word "two-thirds" is the loose half and the arithmetic is right.
- **Confidence:** HIGH — the arithmetic is unambiguous; the only open question is which of the two numbers the outside paper supports, and the repository quotes neither.
- **Invalidated by later commits?:** no — Sections 0–14 of `REGISTRATION.md` are byte-identical from `9080186` to the anchor (SHA-256 of that region is stable across all eleven later commits that touched the file), and the project closed on 2026-09-02.
- **Disclosed by authors?:** no — neither the divisor nor the discrepancy is mentioned anywhere.
- **Why it decides nothing:** the registered access floor is **1,000** markets, which exceeds both 703 and 713, and the gate never fired: Stage C recorded PENDING_ACCESS before any enumeration.

### DRAFT-V-2
- **Repository / SHA:** PMExperiment / `03d16e71dbf25a86c529884662d02136f8e82334`
- **Hypothesis or artifact:** `docs/BAND.md`, the provenance sentence that opens the band evidence
- **Direction:** neutral (pure hygiene — every figure the sentence covers recomputes exactly)
- **Class:** PROVENANCE
- **Severity:** S4
- **Label:** DERIVED
- **Claim challenged (verbatim quote):** "Every figure is computed by `pmexperiment.band` and pinned by `tests/test_band.py`, so nothing here is hand arithmetic." — PMExperiment/docs/BAND.md:8-9
- **Evidence:**
  - `pmexperiment/band.py` is 135 lines, read in full: it has **no solver for a crossing price** and **no probability-gap ↔ percent-return conversion**. Its public surface is `fee_borne`, `fx_cost`, `required_underpricing`, `band_top_exceeds_requirement`, `band_bottom_exceeds_requirement`, `bucket_midpoint`, `surviving_buckets`, `is_band_empty` — PMExperiment/pmexperiment/band.py:46-135.
  - grep over `pmexperiment/` and `tests/test_band.py` for `0.3333`, `1.6667`, `3.16`, `0.117`, `0.883`, `0.043`, `-40`, `0.077`: **zero hits**.
  - `tests/test_band.py` holds 14 test functions and **never opens `docs/BAND.md`**; the only tests that read that document are three in `tests/test_honesty.py:184-217, 242-249`, and they pin the strings `BAND-OPEN`, `0.0585`, `0.0785`, `0.0300`, `313,972` and one sentence — not the Task-2 table and not the crossing points.
  - The document contradicts the sentence twice itself: "### The crossing points, **stated rather than inferred**" — PMExperiment/docs/BAND.md:212 — and "Full derivation in DECISIONS.md ADR-009" for the unit determination — PMExperiment/docs/BAND.md:123 (ADR-009 at PMExperiment/DECISIONS.md:208).
- **Recomputation (if any):** I recomputed every hand-derived figure the sentence over-claims for: the four crossing prices (−0.3333, +1.6667, −1.0000, +1.0000), the six unit-determination cells (−0.02, −40.0 %, +0.03, +3.16 %, 0.117, 0.043), the exploitable NO entry 0.883 and its two costs (0.0565, 0.0765), and the 60-cell Pass-1 table. **All reproduce exactly** (tolerance: 4 dp on prices and costs, 2 dp on percentages). Script: `work/agentC-pm-verify/recompute.py`.
- **What would resolve it:** replacing "every figure" with the accurate scope — the band table, the margins, the slacks and the survival counts are machine-computed and machine-pinned; the crossing points and the unit-determination table are hand arithmetic, correct, and derived in ADR-009.
- **Confidence:** HIGH — the module and the test file were read in full and the grep is decisive.
- **Invalidated by later commits?:** no — `docs/BAND.md` has exactly one commit in its history (`34307b6`) and is unmodified at the anchor.
- **Disclosed by authors?:** partly — `docs/BAND.md:212` ("stated rather than inferred") and `:123` (the ADR-009 pointer) disclose the derivation route for exactly the figures the blanket sentence at `:8-9` mis-describes. The finding is that the two statements cannot both be true, not that a number is wrong.

### DRAFT-V-3
- **Repository / SHA:** PMExperiment / `03d16e71dbf25a86c529884662d02136f8e82334`
- **Hypothesis or artifact:** Stage A Task 1, the keyless settled-history depth measurement
- **Direction:** neutral (if anything it cuts against the repository's own closure, by claiming *more* retrievable history than the probes establish)
- **Class:** INTERNAL_INCONSISTENCY
- **Severity:** S4
- **Label:** READ
- **Claim challenged (verbatim quote):** "settled-history depth | earliest retrievable settled close sits **between 2024-01-01 (empty page) and 2024-05-31 (present)**, bracketed by `max_close_ts` probes at 2021-08-01, 2022-01-01, 2023-01-01, 2024-01-01 (all empty) and 2024-07-01, 2025-01-01 (both non-empty)" — PMExperiment/docs/ACCESS.md:72
- **Evidence:**
  - The six probes listed in that same cell bracket the earliest retrievable close to **[2024-01-01, 2024-07-01]**. **2024-05-31 is not one of the six probe dates and is not implied by them**; it is a full month tighter than the stated method supports.
  - The endpoint is restated four more times, each time attributed to the probe count and to nothing else: "between 2024-01-01 and 2024-05-31 (bracketed by single-page probes, **n = 6 probes**)" — PMExperiment/REGISTRATION.md:391; identically at PMExperiment/REGISTRATION.md:539, PMExperiment/report.md:34, PMExperiment/progress.md:43, PMExperiment/DECISIONS.md:103, and PMExperiment/docs/ACCESS.md:320.
  - The raw responses are gone by the repository's own statement — "the raw probe responses were not retained beyond this report" — PMExperiment/docs/ACCESS.md:87-89 — so the figure cannot be reproduced from anything stored.
- **Recomputation (if any):** interval arithmetic over the six stated probe endpoints: `max(empty) = 2024-01-01`, `min(non-empty) = 2024-07-01`; bracket = [2024-01-01, 2024-07-01]. Stated bracket [2024-01-01, 2024-05-31]. Tolerance: exact dates.
- **What would resolve it:** one sentence saying where 2024-05-31 came from. **The innocent reading is available and likely**: if the non-empty 2024-07-01 page contained a market closing 2024-05-31, then 2024-05-31 is the earliest close *observed*, which is a legitimately tighter bound — but it is then a property of the page's contents, not of "n = 6 bracketing probes", and the document says the latter five times. Retained responses would settle it; there are none.
- **Confidence:** MEDIUM — HIGH that the stated bracket does not follow from the stated probe set, LOWER that anything is actually wrong with the number itself.
- **Invalidated by later commits?:** no — `docs/ACCESS.md` is unmodified at the anchor and the project is closed.
- **Disclosed by authors?:** no for the bracket; yes for the irreproducibility (`docs/ACCESS.md:87-89`), which is why the underlying measurement is recorded UNVERIFIABLE rather than contradicted.

### DRAFT-V-4
- **Repository / SHA:** PMExperiment / `03d16e71dbf25a86c529884662d02136f8e82334`
- **Hypothesis or artifact:** the Stage C commit message, `52d39ec`
- **Direction:** neutral
- **Class:** PROVENANCE
- **Severity:** S4
- **Label:** DERIVED
- **Claim challenged (verbatim quote):** "docs: Stage C report, Entry 7, ADR-012 and **nine honesty tests**" and, in the body, "**Nine honesty tests** pin the verdict, its clause and effective date, the retraction with the retracted claim still quoted, the zero-request record, the counterargument, the floor's absent sample cost, and the transfer statement." — PMExperiment git commit `52d39ec003f9c774a4e73760e75d4798cd905839` (subject and body; live repo read 2026-09-12T02:36Z)
- **Evidence:**
  - `git show 52d39ec --stat` touches exactly one test file, `tests/test_honesty.py` (+82 lines, no deletions).
  - `def test_` count in that file: **28 before, 36 after — exactly 8 added, none removed**. The eight are `test_polymarket_access_verdict_is_recorded_with_its_clause`, `test_amendment_one_premise_is_retracted_not_quietly_dropped`, `test_stage_c_sent_no_market_data_requests`, `test_the_counterargument_to_the_access_verdict_is_recorded`, `test_the_gate_did_not_fire_and_both_passes_are_absent`, `test_the_terms_claim_practice_is_registered`, `test_transfer_statement_holds_even_with_no_polymarket_result`, `test_volume_floor_cost_in_sample_is_reported_absent_not_zero`.
  - The **same message's other count is right**: "72 tests green" — the tree at `52d39ec` holds 14 + 4 + 36 + 9 + 9 = **72** test functions, up from 64. Eight, not nine, is what closes that arithmetic.
  - The repository's convention is otherwise accurate: `ebdc116` says "nine honesty tests" and added exactly 9 (19 → 28); `baa2bf3` says "six" and added exactly 6 (37 → 43).
- **Recomputation (if any):** inputs `git show 52d39ec^:tests/test_honesty.py` and `git show 52d39ec:tests/test_honesty.py`; method `grep -c '^def test_'`; result 28 → 36; tolerance exact.
- **What would resolve it:** nothing needs resolving in the tree — the message is wrong by one and no document repeats the figure for this stage.
- **Confidence:** HIGH — counted directly from the git objects.
- **Invalidated by later commits?:** no — a commit message is immutable once written.
- **Disclosed by authors?:** no.

### DRAFT-V-5
- **Repository / SHA:** PMExperiment / `03d16e71dbf25a86c529884662d02136f8e82334`
- **Hypothesis or artifact:** the registration dates of Amendments 1, 2 and 3 and of ADR-006 and ADR-007
- **Direction:** neutral (the *ordering* claim these dates support survives intact; only the dates are wrong)
- **Class:** PROVENANCE
- **Severity:** S4
- **Label:** DERIVED
- **Claim challenged (verbatim quote):** "**Made 2026-08-30, before any statistic relating a price to an outcome exists.**" — PMExperiment/REGISTRATION.md:667 (identically "**Made 2026-08-30.**" at PMExperiment/REGISTRATION.md:707 and :751, and "**Status:** accepted, 2026-08-30." at PMExperiment/DECISIONS.md:140 and :160)
- **Evidence:**
  - All five lines are owned by one commit: `git blame` at the anchor returns `f686036a` for `REGISTRATION.md:667`, `:707`, `:751` and `DECISIONS.md:140`, `:160`.
  - `f686036` ("docs: amendments 1-3 — Polymarket measures the phenomenon, the fee band fires first") has author **and** committer date **2026-08-29T11:05:26−07:00 = 2026-08-29T18:05:26Z** — **2026-08-29 in UTC and in the committer's own local zone alike**. There is no timezone in which that commit falls on 2026-08-30.
  - The repository's own convention is UTC and is applied correctly elsewhere: Amendment 5 is dated "Made 2026-08-30" (`REGISTRATION.md:855`) and its commit `f789079` is 2026-08-29T20:34:00−07:00 = **2026-08-30T03:34Z**; Amendment 6 likewise (`REGISTRATION.md:914`, `1b3124e`, 03:40Z).
  - The internal oddity this produces: **Amendment 4, committed 72 minutes later** (`4d75f66`, 2026-08-29T19:17Z), is dated "**Made 2026-08-29**" (`REGISTRATION.md:783`) — so as the document reads, Amendment 4 was made a day *before* the Amendment 2 it operates under.
- **Recomputation (if any):** inputs `git blame -L <line>,<line> 03d16e7 -- <file>` and `git log -1 --date=iso-strict`; method: compare stated date to author/committer date in both UTC and −07:00; result: stated 2026-08-30, actual 2026-08-29 (18:05:26Z); tolerance exact to the calendar day.
- **What would resolve it:** a one-line correction, or a statement of the dating convention used. **The load-bearing claim is unaffected**: `f686036` (18:05Z) precedes the band verdict `32dc10a` (19:24:06Z), so "registered before it fired" is verified by the objects regardless of which calendar day the label carries.
- **Confidence:** HIGH — read straight from the commit objects.
- **Invalidated by later commits?:** no — the lines are unmodified at the anchor and the project is closed.
- **Disclosed by authors?:** no for these five; the repository does catch and correct one other extrapolated timestamp of its own ("Entry 6 states it was logged at 2026-08-29T19:32Z. **That figure is wrong.**" — PMExperiment/progress.md:652-658), and that correction is itself verified: `84f7b92` is dated 2026-08-30T03:31:03Z exactly as the correction says.

### DRAFT-V-6
- **Repository / SHA:** PMExperiment / `03d16e71dbf25a86c529884662d02136f8e82334`
- **Hypothesis or artifact:** Section 0.3 / Section 9, the power gate — the GO row and the tail-count bar it implies
- **Direction:** B
- **Class:** STATISTICAL
- **Severity:** S4 (it would be S2 had the gate ever fired; no verdict in this repository depends on it)
- **Label:** DERIVED
- **Claim challenged (verbatim quote):** "| **GO** | MDE ≤ 0.02 | the design **resolves the entire published band**; Stage B is authorized for that universe against the registered target |" — PMExperiment/REGISTRATION.md:110 — read against its own bar, "| GO, MDE ≤ 0.02 | **≥ 475** |" — PMExperiment/REGISTRATION.md:128
- **Evidence:**
  - The estimator, as coded: `return registry.Z_CRITICAL * math.sqrt(mean_dispersion / tail_count)` — PMExperiment/pmexperiment/power.py:45, with `Z_CRITICAL: float = 2.0` — PMExperiment/pmexperiment/registry.py:9; as registered: "MDE = z · sqrt(v̄ / n_T), with z = 2.0 two-sided" — PMExperiment/REGISTRATION.md:301.
  - **There is no power term.** grep over all ten documents and all twelve Python files for `z_beta`, `z_β`, `80 %`, `80%`, `50 %`, `power of`, `statistical power`, `1 − β`: **zero hits**. `z·SE` is the smallest effect that would reach two-sided significance when the estimate lands exactly on its own expectation — i.e. at **50 % power** — not the smallest effect a design would reliably detect, which is `(z_{α/2} + z_β)·SE`.
  - The planning inputs are stated and verified: `v̄ = 0.0475` and `sqrt(v̄) ≈ 0.218` — PMExperiment/REGISTRATION.md:120-123 (recomputed: 0.0475 and 0.2179449).
- **Recomputation (if any):** inputs `REGISTRATION.md:128` (n_T = 475), `REGISTRATION.md:122-123` (v̄ = 0.0475), `pmexperiment/power.py:45` (the estimator); method: `SE = sqrt(v̄/n)`, power `= 1 − Φ(z − δ/SE)` with `δ = 0.02`, and the inverted bar `n = (z_{α/2}+z_β)² v̄ / δ²` via `scipy.stats.norm`; results — **SE = 0.010000 exactly at n = 475**, so **power = 0.5000** at z = 2.0 (0.5160 at z = 1.96); a bar that resolves a 0.02 effect at the conventional **80 %** power is **n_T = 959** (z = 2.0) or **933** (z = 1.96), **2.0× the registered 475**; at 90 %, 1,279 / 1,248. Tolerance: power to 4 dp, n to 1 contract. Script: `scratchpad/work/agentC-PM-verify2/power_check.py`.
- **What would resolve it:** stating the power level the bar is set at — "the smallest effect that would reach significance at 50 % power" is an accurate description of what the gate computes — or raising the bar to the 80 %-power figure. Note the second-order consequence: DRAFT-V-1's market requirement (703 markets) is 475 divided by a tail share, so the same doubling would carry through to it.
- **Confidence:** HIGH on the arithmetic; MEDIUM on its importance, since no cell was ever built, no dispersion was ever measured and the gate never fired on any venue.
- **Invalidated by later commits?:** no — `power.py`, `registry.py` and Sections 0–14 of `REGISTRATION.md` are unmodified at the anchor.
- **Disclosed by authors?:** no — the registration states no power level anywhere, so it does not misstate one; what it does is attach the word "resolves" to a bar that misses a real 0.02 effect half the time. **The form is inherited**, explicitly: "This repository follows Insider: the gate is committed before the measurement it judges" — PMExperiment/REGISTRATION.md:44-49 — so the same arithmetic is worth checking in InsiderExperiment and NPDExperiment, whose MDE figures (49.35 bp, 0.0512) are quoted here as the motivating precedents.

---

## 6. What could not be checked, and why

Twenty of the sixty-seven rows are UNVERIFIABLE. They fall into exactly three kinds, and none of
them is unverifiable because something was hidden from me.

**(a) HTTP measurements whose responses were deliberately not retained — 11 rows.** Every figure
Stages A, C and D report from a network probe: the 11-request latency range 99.9–213.8 ms, the
settled-history bracket, the `robots.txt` and terms status codes and byte counts, the two
Polymarket request logs, the character counts of rendered pages, the occurrence counts inside the
Kalshi PDF, the Dune dataset row counts and coverage windows, the candlestick probe on
`NASDAQ100-24OCT25-T21499.99`. **No response body, no header, no timestamped request ledger and
no `data/raw/` directory exists at any commit** — I checked the whole history, not just the
anchor: `git log --all --diff-filter=A --name-only` adds no data-shaped file, ever. The
repository states this itself at `docs/ACCESS.md:87-89`, and Section 14's reproducibility clause
("the gate verdict must be regenerable from the stored raw enumeration and candlestick responses
under `data/raw/`", `REGISTRATION.md:359-363`) is therefore **vacuous rather than satisfied** —
consistent with the fact that no enumeration ever ran, but it means the clause was never tested.
What is missing, exactly: the response bodies and the request ledger. Nothing I could compute
would recover them.

**(b) Figures imported from outside this repository — 6 rows.** The MLCryptoEngine AUC 0.501, the
NPD minimum detectable contrast 0.0512 with its 415 days and 6.9378 USD, the Insider 49.35 bp, the
Bürgi-Deng-Whelan magnitudes (313,972 prices; −40 %; +3.1 %; "lose over 60 % after fees") and the
Krause −0.077 at a 4.0 % settlement rate. Inside PMExperiment these are **quotations with no n
attached** (the registration says so itself for the band's top: "The band's top carries no n",
`REGISTRATION.md:440`), pinned as strings by `tests/test_honesty.py` and `tests/test_registry.py`.
Their internal *use* verifies — every conversion and comparison built on them recomputes exactly —
but their *truth* is a question for MLCryptoEngine, NPDExperiment, InsiderExperiment and two
outside papers, not for this repository.

**(c) Registered machinery that never ran — 3 rows.** The MDE on a real cell, the Wilson bound on
a real sample, and `v̄` on real snapshot prices. There is nothing to reproduce because the access
gate fired PENDING_ACCESS before any universe was enumerated. Their *definitions* were checked
against the code and are exactly as registered; only their values do not exist.

**Two things I chose not to run, and why.** I did not execute the repository's test suite (the
read-only rule forbids running a repository's scripts in place, and the LOCATE pass recorded an untracked
`_CLOSED_DO_NOT_RUN_HERE` marker in the working tree, read 2026-09-05T23:28Z); every test assertion cited above was verified by reading the
test and recomputing the assertion myself. And I did not attempt any network request: the figures
that would need one are precisely the ones this repository declined to make, and reproducing them
now would measure 2026-09-12, not 2026-08-29.

---

## 7. Live-repo access log

Every access to `/home/kiros-li/Documents/GitHub/PMExperiment/` in this task was **read-only git
plumbing**: `status --porcelain`, `rev-parse`, `log`, `show` (including `show <commit>:<path>` to
stdout), `show --stat`, `blame -L`, `rev-list --count`, `rev-list --objects`, `ls-tree`,
`cat-file -s`, `count-objects -v`. **No file in the repository was opened for writing, no
repository script was executed, no commit, checkout, stash, reset, branch or worktree command was
run, and no untracked file was read in this session.** No `.env`, keystore, session, credential or
token file was opened. All document and code content was read from the anchored snapshot at
`/home/kiros-li/.cache/program-audit/scratchpad/snap/PMExperiment/`.

There are **no unanchored reads in this verification pass**. (The LOCATE pass recorded one:
`ls -la` of the working tree and of `data/`, read 2026-09-05T23:28Z, establishing that `data/`
holds a single 0-byte `.gitkeep`.)

**`git -C /home/kiros-li/Documents/GitHub/PMExperiment status --porcelain` BEFORE first access —
2026-09-12T02:36:30Z:**

```
```

(empty — exit 0, working tree clean; `HEAD` = `03d16e71dbf25a86c529884662d02136f8e82334`)

**`git -C /home/kiros-li/Documents/GitHub/PMExperiment status --porcelain` AFTER last access —
2026-09-12T02:45:25Z:**

```
```

(empty — exit 0, working tree clean; `HEAD` = `03d16e71dbf25a86c529884662d02136f8e82334`)

**No modification was made to the audited repository and none is reported.**

---

## 8. Scripts used

All written by me; none copied from the repository; none executed with a working directory inside
an audited path.

| script | what it does |
|---|---|
| `work/agentC-pm-verify/recompute.py` | The main recomputation. Types the registered constants in from `registry.py` / `REGISTRATION.md` (reading no repository file), then reproduces: the BAND-OPEN headline (0.0585 vs 0.08), the fee+spread floor against the band bottom, the four crossing prices, **all 60 cells of the Pass-1 table**, the surviving-bucket counts under both quantifiers at k = 1, 12 and ∞, the margins and slacks on both routes, the six unit-determination cells, both power bars and the MDE at n = 100, the cost floor in both written forms, and the text-share ratios of `docs/LICENCES.md`. |
| `scratchpad/work/agentC-PM-verify2/power_check.py` | The power arithmetic behind DRAFT-V-6 and DRAFT-V-1: SE and realized power at the registered bar, the 80 %- and 90 %-power bars at both z, and the three divisions of 475 by the candidate tail shares. Uses `scipy.stats.norm`. |
| `work/agentC-pm-verify/mkjson.py` | Emits `PMExperiment.claims.json` — one object per claim, derived quantity, interval and test, with the fields the brief specifies. |
| `scratchpad/work/agentC-PM-verify2/gen_tables.py` | Renders sections 1–4 of this document from that JSON, so the tables and the machine-readable rows cannot drift apart. |
