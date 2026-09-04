# PMExperiment — REOPEN LEDGER (part p2-progress)

**Repository / SHA:** PMExperiment / `03d16e71dbf25a86c529884662d02136f8e82334`
(main, 2026-09-02 — closed project, last commit).

**Scope of this ledger.** Every entry whose primary evidence sits in my assigned
documents: `progress.md`, `docs/ACCESS.md`, `docs/BAND.md`, `docs/LICENCES.md`,
`pmexperiment/`, `data/`. Cross-references into `REGISTRATION.md`,
`HYPOTHESES.md` and `DECISIONS.md` are given where the registered reopen text
lives there (another reader's primary set) and are marked `[R]`, `[H]`, `[D]`.

**This ledger is factual, not advocacy.** Every cell is a quotation or a figure
with its file:line. Where a figure has no n, the cell says so — it is not filled
in.

---

## Index table

| # | entry | status | closure kind | closure date | deciding figure (n) | file:line |
|---|---|---|---|---|---|---|
| 1 | H1 — calibration net of Canadian retail cost | **CLOSED (terminal)** | unmeasurable-at-this-house's-standard; **not** Section 16's registered closure | 2026-09-02 | none — no MDE, no bucket count, no dispersion ever computed (n = 0 contracts) | progress.md:1363-1367; [H]:254-268; [R]:573-612 |
| 2 | Stage A — Kalshi access gate | **CLOSED** | PENDING_ACCESS (access gate, fail-closed on 3 of 5 conditions) | 2026-08-29 | conditions 3, 4, 5 fail; depth bracket 2024-01-01…2024-05-31 (n = 6 probes); reachability HTTP 200 99.9–213.8 ms (n = 11 requests) | docs/ACCESS.md:9-22, :71-72; progress.md:20-25 |
| 3 | Stage A Task 2 — the Canadian-permitted filter | **NEVER ARMED** | registered casualty of the access verdict | 2026-08-29 | none — "never armed" | progress.md:33; docs/BAND.md:113 |
| 4 | Stage A Task 3 — the power gate (U24 / P30) | **NEVER FIRED** | registered casualty of the access verdict | 2026-08-29 | none — "reported as absent, not as zero" | progress.md:34, :48-53 |
| 5 | Stage B — the fee-versus-edge band | **FIRED: BAND-OPEN** | arithmetic gate over registered constants; "computed once, never recomputed" | 2026-08-29 | required 0.0585 at p = 0.95, k = 1 vs band top 0.0800 (Bürgi n = 313,972 prices / 46,282 contracts / 12,403 events; **Krause's n not recorded anywhere**) | docs/BAND.md:15-25, :210, :330-336 |
| 6 | Stage C — Polymarket access gate | **CLOSED** | PENDING_ACCESS on the published terms | 2026-08-30 | Terms effective 2026-08-11, 59,617 bytes; crawlers bullet, no entity-type qualification; **0** market-data requests, **7** total requests | docs/ACCESS.md:97-102, :121-136, :210-216; progress.md:672-682 |
| 7 | Stage C Task 3 — the power gate over 91–99c | **NEVER FIRED** | terms closed the enumeration before it was armed | 2026-08-30 | both passes "absent, not zero"; no MDE reported against the 5.85-point requirement | progress.md:757-765 |
| 8 | Stage D candidate 1 — a Polymarket written-authorization request | **CLOSED** | PROHIBITED **(baseline, not a refusal)** | 2026-08-30 | `Notices` 0, `authorization` 0 occurrences across 58,830 characters; 6 published addresses, none for this asker | docs/LICENCES.md:121, :195-199, :303-307 |
| 9 | Stage D candidate 2 — published academic datasets | **CLOSED** | UNMEASURED (ADR-012 elements (1) and (2) both unmet) | 2026-08-30 | `TimeSeventeen/Polymarket-v1`: 1,201,580,990 rows, 2022-11-21→2026-04-28, all four gate inputs documented; **no date printed on card or on the CC BY 4.0 legal code** | docs/LICENCES.md:343-345, :379-403 |
| 10 | Stage D candidate 3 — third-party platforms | **CLOSED** | PROHIBITED (Dune) / UNMEASURED (four others) | 2026-08-30 | Dune ToS `Last updated on: June 3rd, 2026`, 172,750 bytes; `aggregat`/`derived`/`redistribut`/`republish`/`resell` **0 occurrences each**; API keys only after a paid subscription | docs/LICENCES.md:509-511, :525-532, :576-579 |
| 11 | Kalshi Internal Use route | **OPEN — EXISTS-AND-UNTRAVELLED** | not a closure: not declined on the merits; nothing applied for | received 2026-09-01 | 2021 historical depth available on the licence (no count, no coverage figure — "UNMEASURED — never requested") | docs/ACCESS.md:220-251, :302-315 |
| 12 | The entity path | **CLOSED by operator decision** | a declined cost, explicitly **not** evidence about H1 | 2026-09-02 | judged disproportionate to a stated prior of 5–8 % against a band top of 2.15 of 6.0 points at 95c | progress.md:1458-1472; [D]:633 |
| 13 | Amendment 5 — the $1,000 volume floor | **REGISTERED, NEVER EXERCISED** | not closed; cost in sample "not measured", reported absent | 2026-08-30 | floor $1,000 total traded volume per contract (n of contracts it removed: **not measured**) | progress.md:704-718; pmexperiment/registry.py:44-50 |
| 14 | Kalshi rate limit | **WITHHELD, NOT MEASURED** | deliberate deviation, ADR-007 (rule 12 outranks rule 4) | 2026-08-29 | documented claim only: 200 reads/s Basic tier — "claim, not a measurement" | docs/ACCESS.md:75-76 |
| 15 | Polymarket reachability / rate limits / history depth | **WITHHELD, NOT MEASURED** | same deviation, applied ahead of any fetch | 2026-08-30 | none — "Reported as withheld — never as zero, and never as unknown-therefore-fine" | docs/ACCESS.md:196-201 |
| 16 | The Kalshi academic-tier question | **PENDING, UNANSWERED** | not a closure; "its existence is UNMEASURED, not absent" | as of 2026-09-02 | none | [H]:312-314; [R]:1092-1094 |
| 17 | The Polygon-read question (Amendment 6 route c) | **OPEN, never analysed** | not closed and not opened; "under a legal analysis this repository has not performed" | left open 2026-08-30, **absent from the terminal list of 2026-09-02** | none | docs/LICENCES.md:320-326; progress.md:1089-1092; [R]:1001-1005, :508-513 |
| 18 | H1t — transfer to a Canadian-tradeable venue | **UNTESTED** | never opened; nothing to transfer | — | MLCryptoEngine H2 cross-venue transfer **AUC 0.501** (n not recorded in this repository) | docs/LICENCES.md:649-661; [H]:97-104 |
| 19 | H2 — time-decay / convergence structure | **PARKED** | depends on intraday depth Stage A never demonstrated | 2026-09-02 (not carried forward) | none | [H]:73, :323-324 |
| 20 | H3 — cross-category calibration contrast | **PARKED** | requires H1's gate to clear; it never fired | 2026-09-02 (not carried forward) | none | [H]:74, :323-324 |

---

## Blockers, stated per entry, with file:line

| # | blocker as stated | file:line | still standing at the anchor? |
|---|---|---|---|
| B1 | Kalshi Data Terms of Use prohibit "systematic retrieval to create collections, compilations, databases", automated navigation by "scripts, software, spiders, robots", and any AI/ML use of Kalshi Data, absent prior written authorization | docs/ACCESS.md:26-42 | yes |
| B2 | "**API Developer Agreement** … **unreadable by automated means on 2026-08-29**: curl and server-side fetch both received HTTP 429 with a Vercel bot-challenge page; a headless-browser render timed out" | docs/ACCESS.md:44-47 | yes — **never re-probed**, including after this repository discovered on 2026-08-30 that a browser `User-Agent` turned a 403 into HTTP 200 at Dune (docs/LICENCES.md:522-524). See DRAFT-p2-progress-2 |
| B3 | `kalshi.com/robots.txt` returns "HTTP 429 bot-challenge page in 0.071 s" — the website refuses automated readers before robots.txt is served | docs/ACCESS.md:56-59 | yes — never re-probed |
| B4 | Keyless settled history reaches only 2024-01-01…2024-05-31 (n = 6 bracketing probes); the 2021→Apr 2025 benchmark span "is **not reproducible keylessly**" | docs/ACCESS.md:72-73 | **superseded in part**: the 2026-09-01 reply reports 2021 depth via historical endpoints on the licence (docs/ACCESS.md:251). The repository states the original phrasing survives because it described the keyless surface, not the archive (docs/ACCESS.md:317-326) |
| B5 | Access-gate condition 3, ≥ 1,000 settled markets: "**NOT MEASURED — fails closed** … counting requires systematic pagination … a single page of 20 returned with a continuation cursor, so the count is > 20 and otherwise unknown" | docs/ACCESS.md:20 | yes — and it is a *derived* blocker: it fails because of condition 5, not independently |
| B6 | Access-gate condition 4, S30 price history: "**NOT DEMONSTRATED — fails closed** … 0 daily candles" on one market | docs/ACCESS.md:21 | yes — n = 1 market, one interval, lifetime unrecorded. See DRAFT-p2-progress-6 |
| B7 | Polymarket Terms of Use, effective 2026-08-11: "Use any data mining tools, robots, crawlers, or similar data gathering and extraction tools to scrape or otherwise remove data from the Site, any other Interface, or Features" | docs/ACCESS.md:132-136; docs/LICENCES.md:147-149 | yes |
| B8 | Polymarket restricted-jurisdiction narrowing for Alberta, British Columbia, Ontario, Quebec — permitted use narrows to the Content Features | docs/ACCESS.md:166-178 | yes (recorded "though not the ground") |
| B9 | Polymarket has no notices clause and no postal address; the closest route (`data-licensing@`) opens "If you or your clients are **Capital Markets Entities**" | docs/LICENCES.md:189, :195-199 | yes |
| B10 | The Polymarket builder-program upgrade path requires "Route orders through Polymarket and demonstrate consistent usage" — unreachable for a repository that will never trade | docs/LICENCES.md:215-219 | yes |
| B11 | CC BY 4.0 legal code and the dataset card print **no date at all**, so ADR-012 element (2) fails | docs/LICENCES.md:398-403 | yes — **and the document class that carries a date by construction (Zenodo / Dataverse / OSF / figshare) was never fetched** (docs/LICENCES.md:674). See DRAFT-p2-progress-3 |
| B12 | CC BY 4.0 Section 1 caps Licensed Rights to what "the Licensor has authority to license"; Section 5(a) disclaims title and non-infringement — chain of title unestablished | docs/LICENCES.md:427-435 | yes |
| B13 | Dune binds non-registrants, grants no right in data, and issues API keys only "After the User's subscription to a Subscription Plan" — a paid account is outside standing rule 11 | docs/LICENCES.md:557-580 | yes |
| B14 | Kalshi Internal Use requires "**an established legal entity**, with formation documents and beneficial-owner verification" | docs/ACCESS.md:250 | yes — and declined by the operator on 2026-09-02 (progress.md:1458-1472) |
| B15 | Three questions surviving the entity requirement, all unread: the **fee** (UNMEASURED), whether Internal Use permits **publishing** (UNRESOLVED), the **AI/ML written consent** (UNRESOLVED) | docs/ACCESS.md:302-315 | yes |
| B16 | Standing rule 11 — no spend without an explicit operator instruction — blocks every paid tier | docs/LICENCES.md:576-580, :784-787 | yes |
| B17 | Section 1's volume floor was never registered in Stage A, so BAND-NARROW's volume clause "cannot be evaluated" | docs/BAND.md:113, :287 | **lifted 2026-08-30** by Amendment 5 (progress.md:704-712) — but never exercised, so the clause remains unevaluated in fact |
| B18 | Raw probe responses "were **not retained** beyond this report", against Section 14's registered requirement that the gate verdict be regenerable from `data/raw/` | docs/ACCESS.md:88-89 vs [R]:359-361 | yes — `data/` holds only a 0-byte `.gitkeep` in snapshot and live tree (read 2026-09-04T00:24Z). See DRAFT-p2-progress-8 |

---

## Registered reopen conditions, with file:line, and whether the trigger is met

### Per-stage conditions, as registered when each verdict fired

| # | reopen condition, as registered | file:line | trigger met at the anchor? |
|---|---|---|---|
| R1 | Kalshi access: "written authorization from Kalshi for systematic retrieval and AI-mediated analysis, **or** a Kalshi-sanctioned bulk research channel not requiring an account, **or** an operator decision to register an account — which ADR-002 currently excludes" | [R]:395-400; [H]:33-35 | **partially, and unresolved.** The 2026-09-01 reply says the use "fits their Internal Use data licence" and was "not declined on the merits" (docs/ACCESS.md:249) — a *named route*, not a granted authorization. "Nothing was applied for, so nothing was granted and nothing was refused" (docs/ACCESS.md:306). The register keeps it **EXISTS-AND-UNTRAVELLED** and does not treat the trigger as met |
| R2 | Polymarket access, Amendment 6: (a) "prior written consent from Adventure One QSS, Inc."; (b) "enrolment in the builder program the Terms name"; (c) "a Polygon read performed through infrastructure that is not a Polymarket Interface, under a legal analysis this repository has not done" | [R]:1001-1005; [R]:508-513; [H]:199-203 | **(a) no. (b) no — answered on the merits at docs/LICENCES.md:215-225. (c) NOT ANSWERED, and its supporting argument was strengthened after registration**: "a public Polygon ledger is none of the three on its face … Amendment 6's Polygon question stays open" (docs/LICENCES.md:320-326; progress.md:1089-1092). **It is absent from the terminal reopening set.** See DRAFT-p2-progress-1 |
| R3 | Section 16 registered reopening: "the permitted subset accumulates settled contracts with the calendar, so a later session may refire the gate on a fresh enumeration as a new numbered firing — the gate reads no outcome, so refiring is not a second look" | [R]:651-654 | **trigger is calendar-based and therefore continuously met** — but inoperative, because the enumeration it refires on is the thing the access verdicts forbid. Section 16 is annotated "none of these conditions was ever met" ([R]:636-641) |
| R4 | Stage D "What would change it": "**Only these**, and each is an operator decision rather than a measurement" — (1) written authorization from Adventure One QSS or Kalshi; (2) a numbered amendment on version identity for element (2), only alongside closing element (1), chain of title and the AI-clause search; (3) a paid third-party tier | docs/LICENCES.md:771-789 | (1) partially — see R1. (2) no. (3) no. **The list omits R2(c), which the same document records as live at :324-326.** See DRAFT-p2-progress-1 |

### The terminal conditions, Amendment 8 + Amendment 9 (2026-09-02)

| # | condition, verbatim | file:line | trigger met at the anchor? |
|---|---|---|---|
| T1 | "**An established legal entity applying for Internal Use.** … **Necessary, not sufficient** — the fee is UNMEASURED, whether Internal Use permits **publishing** a calibration result is UNRESOLVED, and whether it carries the **AI/ML written consent** … is UNRESOLVED" | [R]:1085-1091; [H]:308-311; README.md:155-158 | **no.** The operator declined to form the entity on 2026-09-02 (progress.md:1458-1472) |
| T2 | "**An academic tier offered by Kalshi, if one is.** A question about one is **pending** with the institutional desk and unanswered as of 2026-09-02. Its existence is **UNMEASURED**" — with "A reply … is **a one-line register update**, not a reopening" | [R]:1092-1094, :1100-1104; [H]:312-314, :318-321 | **no — pending.** This is the one condition whose trigger could arrive without any operator action, and the register pre-commits that a reply is *not* a reopening |
| T3 | "**A licensed dataset whose licensor held authority to license.** ADR-014's chain-of-title element, which the leading candidate could not show" | [R]:1095-1098; [H]:315-316 | **no.** Chain of title unestablished (docs/LICENCES.md:427-435); element (2) also unmet, and the deposit document class that would cure it was never fetched (docs/LICENCES.md:674) |
| T4 | "**a Polymarket data licence or written authorization** — the instrument Stage C found absent, obtained. **Canadian trading access is neither necessary nor sufficient for it**" | [R]:1161-1167; [H]:352-358; progress.md:1620-1621 | **no** |
| — | Registered as **not** a reopening: a change in Polymarket's Canadian regulatory status ("a regulatory change to trading access is not evidence about data permission") | [R]:1133-1143; progress.md:1607-1612 | n/a — an explicit non-trigger |
| — | Registered as **barred**: "**And no fourth venue.**" and "no route makes BAND-OPEN evidence that an edge exists"; "A reopened measurement starts at the power gate over 91–99c held to resolution and no other region" | [R]:1106-1116 | n/a — a standing bar. Note that the region clause locks the scope discussed in DRAFT-p2-progress-5, and that the "fourth venue" bar is stated about **venues**, which does not on its face cover the unasked regulatory-disclosure route (docs/LICENCES.md:682) — DRAFT-p2-progress-7 |

---

## Named-but-never-travelled routes (registered as unread, not as absent)

These are recorded in the repository's own completeness table and are **not**
reopen conditions. Listed here because each is a route to the same records whose
status is "not read", not "read and refused" — docs/LICENCES.md:665-688,
progress.md:1094-1110.

| route | file:line | in a reopen condition? |
|---|---|---|
| Versioned repository deposits — Zenodo, Dataverse, OSF, figshare ("**the sharpest gap**") | docs/LICENCES.md:674 | no |
| The CC BY 4.0 errata page named in the legal code's own footer | docs/LICENCES.md:675, :405-411 | no |
| Manifold's Terms of Service (a prediction-market venue's ToS) | docs/LICENCES.md:676 | no |
| Six Dune addenda incorporated by reference, incl. the Data Hub Service Addendum | docs/LICENCES.md:677 | no |
| Token Terminal's Subscription Agreement | docs/LICENCES.md:678 | no |
| Kalshi's non-PDF surface — main Terms of Use, help centre, API documentation licensing | docs/LICENCES.md:679 | no |
| ICE documents (Polymarket institutional data is distributed through ICE) | docs/LICENCES.md:680 | no |
| IEM, PredictIt, Metaculus, Betfair; Kaggle, BigQuery public datasets, Snowflake Marketplace, subgraph hosts | docs/LICENCES.md:681 | no |
| **Regulatory disclosure routes** — "whether settlement history is obtainable from a **regulator** rather than a venue was never asked" | docs/LICENCES.md:682 | no — see DRAFT-p2-progress-7 |

---

## Possibly met by work in a DIFFERENT repository — for the cross-repo pass

Flagged, not asserted. Each is a dependency this repository imports from another
repository in the same programme, or a condition another repository could satisfy.

| # | item | what would meet it, elsewhere | file:line here |
|---|---|---|---|
| X1 | **H1t is UNTESTED on three grounds, one of which is another repository's number**: "this program's own MLCryptoEngine H2 measuring cross-venue transfer at **AUC 0.501**" | If MLCryptoEngine's H2 has since been superseded, re-run at different power, or found to have measured something else, **one of the three grounds for treating transfer as unassumable weakens**. The other two grounds are external-literature claims and are unaffected | docs/LICENCES.md:653-656; progress.md:776-779; [H]:103 |
| X2 | **The design premise is imported from NPDExperiment**: "realized minimum detectable contrast **0.0512** against an effect band of **0.01 to 0.05** … after **415 days**" | If NPDExperiment's realized MDE or its 415-day figure has moved, the "follow Insider, not NPD" rationale that justified stopping before collection changes its arithmetic basis | CLAUDE.md:54-58; README.md:182-188; progress.md:94-98 |
| X3 | **The gate design is imported from InsiderExperiment**: "fired **BLOCKED at 49.35 bp** before spending" | If InsiderExperiment's 49.35 bp figure or its BLOCKED label has been revised, the precedent this repository's whole method rests on is affected | CLAUDE.md:60-65; README.md:186-188 |
| X4 | **Terminal reopening condition T3, "a licensed dataset whose licensor held authority to license"** | Any repository in this programme that has obtained, licensed or documented a prediction-market dataset with a printed effective date **and** an established chain of title would satisfy T3 on its face. Worth checking ETFExperiment, HFExperiment, NPLExperiment and AiTrader for licensed-vendor data with chain-of-title documentation | [R]:1095-1098; [H]:315-316 |
| X5 | **Blocker B2/B3 (Kalshi 429 bot challenges) and the browser-`User-Agent` method** | Any repository in this programme that has successfully fetched a Vercel- or Cloudflare-challenged terms page with a header change would show whether B2 is a genuine blocker or a stale one. The method is already recorded *inside* this repository at docs/LICENCES.md:522-524 but was never applied to Kalshi | docs/ACCESS.md:44-47, :56-59 |
| X6 | **Krause's missing n**, which sets the registered band's top of 0.08 and is "not recorded" anywhere | If any other repository in this programme cites the same Krause 2026 unemployment-market study with its sample size, the band's top acquires the n that standing rule 13 requires and that this repository could not supply | docs/BAND.md:115, :155, :336; [D]:265-270 |
| X7 | **The permitted-category filter (economic indicators, financial markets, climate; 30-day minimum maturity)** was never applied to a real enumeration | Any repository holding a settled prediction-market or event-contract enumeration could supply the count that BAND-NARROW's volume clause and the P30 power cell both needed | docs/BAND.md:269-294; progress.md:714-718 |

---

## Ledger notes

1. **Nothing in this repository ever closed on a measurement of H1.** Every closure
   in the table above is an access, permission or standing verdict. The two
   verdict cells the design registered (U24 and P30) never fired, and no realized
   MDE exists — stated by the authors at [R]:605-612 and progress.md:1487-1489.
2. **Two figures are the only quantitative outputs of five stages**: BAND-OPEN's
   5.85 points required at p = 0.95, k = 1 against a band top of 8.00
   (docs/BAND.md:15-18), and the 0.0300 fee-plus-half-spread floor that already
   exceeds the band's 0.0200 bottom at every price (docs/BAND.md:241-243). Both
   are arithmetic over registered constants with no venue read behind them.
3. **Retention.** No probe artefact survives for any stage (docs/ACCESS.md:88-89;
   `data/` empty in snapshot and live tree, read 2026-09-04T00:24Z), so none of
   the deciding access figures in this ledger can be re-derived from stored state.
