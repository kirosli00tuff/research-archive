# REOPEN LEDGER — PMExperiment, part p1-register

Repository: PMExperiment / anchored SHA `03d16e71dbf25a86c529884662d02136f8e82334` (main, 2026-09-02, closed project).
Coverage: entries whose primary record lives in `REGISTRATION.md`, `HYPOTHESES.md`, `DECISIONS.md`, `report.md`, `README.md`.
Evidence for `docs/ACCESS.md`, `docs/BAND.md`, `docs/LICENCES.md`, `progress.md`, `CLAUDE.md`, the package and the tests is another reader's; where I cite them it is marked *(other reader)*.
This ledger is factual, not advocacy. Every figure carries its n where the repository records one; where it records none, the ledger says so.

**Repository-level fact that governs every row:** the power gate never fired, on any venue, over any region, and no statistic relating a price to an outcome exists (PMExperiment/REGISTRATION.md:588-591; PMExperiment/README.md:13-14). Only two gates ever fired: the Kalshi access gate and the fee-versus-edge band gate. The terminal state is not the registered closure — Section 16's conditions were **never met** (PMExperiment/REGISTRATION.md:636-641, 605-612).

---

## 1. H1 — calibration net of Canadian retail cost

- **Status:** CLOSED — terminal, 2026-09-02. Register wording: "H1 is unmeasurable at this house's standard. Not disproven, not unlikely, unmeasurable." (PMExperiment/HYPOTHESES.md:256-257; PMExperiment/REGISTRATION.md:575-578).
- **Closure kind:** terminal access-and-standing finding. Explicitly **not** the registered closure: "H1 therefore does not close under Section 16 at all." (PMExperiment/REGISTRATION.md:609). Filed as "a terminal access finding", not "a result about H1" (PMExperiment/DECISIONS.md:701-705).
- **Closure date:** 2026-09-02 (Section 15.5, Amendment 8, ADR-018).
- **Deciding figure (n):** **none exists.** There is no realized MDE, no bucket count, no dispersion — "There is no realized MDE, because there is no enumeration to compute one from." (PMExperiment/REGISTRATION.md:608-609). Totals: five stages, 0 dollars, 0 contracts enumerated, 0 market-data requests to Polymarket, 0 requests in Stage E (PMExperiment/REGISTRATION.md:628-630).
- **File:line:** PMExperiment/REGISTRATION.md:573-630 (Section 15.5); PMExperiment/HYPOTHESES.md:254-325; PMExperiment/DECISIONS.md:684-744 (ADR-018); PMExperiment/report.md:345-487.
- **Blockers (file:line):**
  - Kalshi Data Terms — systematic retrieval and AI-mediated use prohibited absent written authorization: PMExperiment/REGISTRATION.md:382, 597; PMExperiment/DECISIONS.md:89-98.
  - Kalshi API Developer Agreement unreadable (HTTP 429 bot challenge to every automated read): PMExperiment/REGISTRATION.md:382; PMExperiment/HYPOTHESES.md:173.
  - Keyless Kalshi settled-history depth reaching only 2024-01-01→2024-05-31, n = 6 bracketing probes: PMExperiment/REGISTRATION.md:389-393. **Later shown to be a property of the keyless surface only** — 2021 depth exists on the Internal Use licence through historical endpoints: PMExperiment/REGISTRATION.md:538; PMExperiment/DECISIONS.md:565-568, 621-626.
  - Polymarket Terms of Use effective 2026-08-11 — data-mining/robots/crawlers prohibition, no entity-type qualification: PMExperiment/REGISTRATION.md:934-947, 598.
  - Kalshi Internal Use requires **an established legal entity** with formation documents and beneficial-owner verification; operator is "an individual undergraduate. **No such entity is held**": PMExperiment/REGISTRATION.md:536-537.
  - Internal Use fee **UNMEASURED**; publication permission **UNRESOLVED**; AI/ML written consent **UNRESOLVED**: PMExperiment/REGISTRATION.md:541-543, 1088-1091.
  - Operator declines both entity paths (university sponsorship not achievable in time; personal entity disproportionate) — recorded as a cost decision, not evidence: PMExperiment/REGISTRATION.md:1043-1046; PMExperiment/DECISIONS.md:633-654.
  - **Expired blocker, not revisited:** ADR-002's no-account rule, which Section 15.1 names as the obstacle to the third Kalshi reopening path (PMExperiment/REGISTRATION.md:395-398), was lifted by Amendment 3 on 2026-08-30 — "The operator has stated that account creation is acceptable." (PMExperiment/REGISTRATION.md:756-757; PMExperiment/DECISIONS.md:182-183). No later document revisits it. See DRAFT-p1-register-4.
- **Reopen conditions (file:line):** Amendment 8 declares them "stated precisely and exhaustively" (PMExperiment/REGISTRATION.md:1082):
  1. an established legal entity applying for Internal Use — necessary, not sufficient — PMExperiment/REGISTRATION.md:1085-1091; PMExperiment/HYPOTHESES.md:308-311; PMExperiment/README.md:156-158.
  2. an academic tier offered by Kalshi, if one is — a question is **pending and unanswered** as of 2026-09-02, existence UNMEASURED — PMExperiment/REGISTRATION.md:1092-1094; PMExperiment/HYPOTHESES.md:312-314.
  3. a licensed dataset whose licensor held authority to license (chain of title) — PMExperiment/REGISTRATION.md:1095-1098; PMExperiment/HYPOTHESES.md:315-316.
  4. a Polymarket data licence or written authorization; Canadian trading access is neither necessary nor sufficient — PMExperiment/REGISTRATION.md:1161-1167; PMExperiment/HYPOTHESES.md:352-358.
  - **Explicit non-reopeners:** a reply to the pending academic-tier question ("a one-line register update … nothing more", PMExperiment/REGISTRATION.md:1100-1102); a change in Polymarket's Canadian regulatory status (PMExperiment/HYPOTHESES.md:333-338; PMExperiment/REGISTRATION.md:1120-1143); any fourth venue (PMExperiment/REGISTRATION.md:1113-1116; PMExperiment/HYPOTHESES.md:229-231).
  - **Scope limit on any reopening:** the band may not be recomputed and no bucket added; the reopened power gate fires over 91–99c "and no other region" (PMExperiment/REGISTRATION.md:1106-1111).
  - **Dropped without a recorded reason:** Section 15.1's third path, "an operator decision to register an account" (PMExperiment/REGISTRATION.md:398), appears in none of the four.
- **Possibly met by another repository?** **YES — flag for the cross-repo pass.** Conditions 1 and 2 turn on Kalshi standing: if any other repository in the program holds a Kalshi data licence, an institutional/academic Kalshi relationship, or an established legal entity, condition 1 or 2 may already be satisfiable. Nothing in PMExperiment answers this. Condition 3 turns on a licensed dataset with chain of title — check whether any sibling repository has licensed prediction-market settlement data.

---

## 2. H1t — transfer (a calibration result on Polymarket holds on a Canadian-tradeable venue)

- **Status:** **UNTESTED**, carried forward unchanged to closure. "May not be assumed at any point." (PMExperiment/HYPOTHESES.md:101-102, 299-301; PMExperiment/REGISTRATION.md:624-626).
- **Closure kind:** not closed — never opened for measurement. "There was never anything to transfer." (PMExperiment/HYPOTHESES.md:301).
- **Closure date:** n/a; last restated 2026-09-02.
- **Deciding figure (n):** the three registered grounds carry one figure: **MLCryptoEngine H2, cross-venue transfer at AUC 0.501** — **n not recorded in this repository** (PMExperiment/HYPOTHESES.md:103; PMExperiment/REGISTRATION.md:692-693, 1150-1151). The other two grounds are qualitative (a Kalshi bias reported not to replicate on Polymarket; the largest Polymarket study reporting no general longshot bias) with no n and no citation line in this repository.
- **File:line:** PMExperiment/HYPOTHESES.md:97-104, 188-191, 299-301; PMExperiment/REGISTRATION.md:688-694, 624-626; PMExperiment/DECISIONS.md:148-154.
- **Blockers (file:line):** measurement must be made on the venue where the trade would be placed, which requires written Kalshi authorization (PMExperiment/HYPOTHESES.md:104).
- **Reopen conditions (file:line):** "what would close it | measurement on the venue where the trade would be placed" (PMExperiment/HYPOTHESES.md:104). Separately, Amendment 9 records that Polymarket becoming Canadian-available "would **collapse H1t**" by removing the venue gap (PMExperiment/REGISTRATION.md:1148-1151; PMExperiment/HYPOTHESES.md:344-347).
- **Possibly met by another repository?** **YES — flag.** The sole quantitative ground (AUC 0.501) is imported from MLCryptoEngine H2. Whether that measurement concerns a comparable transfer question, and whether it still stands at MLCryptoEngine's anchor, must be checked cross-repo.

---

## 3. H2 — time-decay and convergence structure within a contract's life

- **Status:** **PARKED**, and at closure "not carried forward" (PMExperiment/HYPOTHESES.md:73, 323-324).
- **Closure kind:** parked on dependency, never registered. "Depends on intraday price history being retrievable at usable depth, which Stage A measures. Not registered."
- **Closure date:** parked 2026-08-29; confirmed not carried forward 2026-09-02.
- **Deciding figure (n):** none. The dependency it waited on — Stage A's access condition 4 — was resolved "NOT DEMONSTRATED, fails closed (**0 daily candles on the one ≥ 30-day-old market tested**; recent-market candles work)", **n = 1 market** (PMExperiment/REGISTRATION.md:381).
- **File:line:** PMExperiment/HYPOTHESES.md:71-74, 323-324.
- **Blockers (file:line):** intraday/daily history depth on the keyless surface (PMExperiment/REGISTRATION.md:381); the same venue-terms blockers as H1.
- **Reopen conditions (file:line):** none written for H2 individually; HYPOTHESES.md:323-324 states both H2 and H3 "depended on H1's gate clearing, and it never fired", so H1's four conditions govern.
- **Possibly met by another repository?** Not directly. Note for the cross-repo pass only: the n = 1 evidence behind the depth blocker, and Section 15.4's later record that 2021 depth exists on the Internal Use licence (PMExperiment/REGISTRATION.md:538), together mean the stated H2 blocker is a keyless-surface property rather than an archive property.

---

## 4. H3 — cross-category calibration contrast

- **Status:** **PARKED**, not carried forward (PMExperiment/HYPOTHESES.md:74, 323-324).
- **Closure kind:** parked on dependency. "Requires H1's gate to clear first, and would add trials to an account that does not yet exist."
- **Closure date:** parked 2026-08-29; confirmed 2026-09-02.
- **Deciding figure (n):** none.
- **File:line:** PMExperiment/HYPOTHESES.md:74, 323-324.
- **Blockers (file:line):** H1's power gate never fired (PMExperiment/REGISTRATION.md:588-591).
- **Reopen conditions (file:line):** H1's, per PMExperiment/HYPOTHESES.md:323-324.
- **Possibly met by another repository?** No.

---

## 5. Closed-before-opening candidate — cross-venue arbitrage, Kalshi against Polymarket

- **Status:** CLOSED at registration, on external evidence, never measured here.
- **Closure kind:** out-of-reach-at-retail-latency (external evidence, not a measurement made here).
- **Closure date:** 2026-08-29.
- **Deciding figure (n):** none — "Documented arbitrage windows close in seconds and are dominated by sub-100 ms bots" carries **no n and no citation line** in this repository.
- **File:line:** PMExperiment/HYPOTHESES.md:63.
- **Blockers (file:line):** retail latency; Polymarket inaccessible to Canadians (PMExperiment/HYPOTHESES.md:63).
- **Reopen conditions (file:line):** "**Nothing at retail latency.**" — PMExperiment/HYPOTHESES.md:63.
- **Possibly met by another repository?** Possibly — flag for the cross-repo pass: if a sibling repository (e.g. an HFT/latency repository) has measured achievable retail latency, that measurement bears on the "sub-100 ms" premise, which this repository states without an n.

---

## 6. Closed-before-opening candidate — sports and political contract mispricing

- **Status:** CLOSED at registration.
- **Closure kind:** excluded by the registered Canadian-permitted category filter ("Measurable but not reachable").
- **Closure date:** 2026-08-29.
- **Deciding figure (n):** none; a scope rule, not a measurement.
- **File:line:** PMExperiment/HYPOTHESES.md:64.
- **Blockers (file:line):** CIRO-permitted category set (economic indicators, financial markets, climate) — PMExperiment/REGISTRATION.md:180-183; PMExperiment/README.md:195-197.
- **Reopen conditions (file:line):** "A change in CIRO-permitted categories." — PMExperiment/HYPOTHESES.md:64. Amendment 9 adds that Polymarket becoming Canadian-available "would **widen the permitted category set**" (PMExperiment/REGISTRATION.md:1152-1157; PMExperiment/HYPOTHESES.md:348-350) — note this is a *category* widening, not a data-permission change.
- **Possibly met by another repository?** No.

---

## 7. Closed-before-opening candidate — trading any measured edge

- **Status:** CLOSED by construction (scope rule).
- **Closure kind:** scope rule, not a result. "Out of scope by construction, not by result."
- **Closure date:** 2026-08-29; reaffirmed by Amendment 3 (2026-08-30), which admits a terminal *trading question* while keeping the execution ban (PMExperiment/REGISTRATION.md:758-763).
- **Deciding figure (n):** none.
- **File:line:** PMExperiment/HYPOTHESES.md:65; PMExperiment/DECISIONS.md:178-191 (ADR-008).
- **Blockers (file:line):** the CLAUDE.md scope guard (PMExperiment/REGISTRATION.md:759-761).
- **Reopen conditions (file:line):** "**Nothing.** It is a scope rule, not a finding." — PMExperiment/HYPOTHESES.md:65.
- **Possibly met by another repository?** No.

---

## 8. Gate — the Kalshi access gate (Section 15.1)

- **Status:** FIRED **PENDING_ACCESS**, 2026-08-29; never re-fired.
- **Closure kind:** access verdict on five registered conditions, three failing closed.
- **Closure date:** 2026-08-29.
- **Deciding figures with n:**
  - condition 1 PASS — HTTP 200 keyless, 127.6 ms (PMExperiment/REGISTRATION.md:378); probe budget 11 keyless market requests, 13 total (PMExperiment/DECISIONS.md:100-102, 131-134).
  - condition 2 PASS — `result` present, **2 of 5** permitted records inspected (PMExperiment/REGISTRATION.md:379).
  - condition 3 **NOT MEASURED**, fails closed — the registered bar is ≥ 1,000 settled markets (PMExperiment/REGISTRATION.md:380, 148-150).
  - condition 4 **NOT DEMONSTRATED**, fails closed — **0 daily candles on the one ≥ 30-day-old market tested, n = 1** (PMExperiment/REGISTRATION.md:381).
  - condition 5 **FAIL** — the decisive one (PMExperiment/REGISTRATION.md:382; PMExperiment/DECISIONS.md:89-90).
  - depth finding travelling with the verdict: earliest keyless settled close between 2024-01-01 and 2024-05-31, **n = 6 bracketing probes** (PMExperiment/REGISTRATION.md:389-393).
- **File:line:** PMExperiment/REGISTRATION.md:371-400; PMExperiment/DECISIONS.md:85-114 (ADR-006, 2026-08-29); PMExperiment/report.md:25-55.
- **Blockers (file:line):** Data Terms prohibition (PMExperiment/REGISTRATION.md:382); Developer Agreement HTTP 429 (PMExperiment/HYPOTHESES.md:173); rate-limit measurement withheld under ADR-007 (PMExperiment/DECISIONS.md:118-134); keyless depth (PMExperiment/REGISTRATION.md:389-393) — **superseded 2026-09-01**, 2021 depth exists on licence (PMExperiment/REGISTRATION.md:538).
- **Reopen conditions (file:line):** PMExperiment/REGISTRATION.md:395-399 — (a) written authorization from Kalshi for systematic retrieval and AI-mediated analysis; (b) a Kalshi-sanctioned bulk research channel not requiring an account; (c) **an operator decision to register an account — "which ADR-002 currently excludes"**. Restated PMExperiment/HYPOTHESES.md:33-35; PMExperiment/DECISIONS.md:111-114.
- **Trigger status:** condition (c)'s stated obstacle **expired 2026-08-30** (PMExperiment/REGISTRATION.md:756-757; PMExperiment/DECISIONS.md:182-183) and was never revisited; the path is also the one the benchmark study used (PMExperiment/DECISIONS.md:97-98). Amendment 8's "exhaustive" list omits it.
- **Possibly met by another repository?** **YES — flag.** (a) and (b) are satisfied by any Kalshi written authorization or sanctioned bulk/academic channel held elsewhere in the program.

---

## 9. Gate — the fee-versus-edge band (Section 15.2)

- **Status:** FIRED **BAND-OPEN**, 2026-08-29. Registered as **not recomputable** (PMExperiment/HYPOTHESES.md:153-157; PMExperiment/REGISTRATION.md:744-745, 1107-1108).
- **Closure kind:** cost verdict computed from registered constants; no venue read. Explicitly "**not** evidence that an edge exists" (PMExperiment/REGISTRATION.md:614-618).
- **Closure date:** 2026-08-29.
- **Deciding figures with n:**
  - required underpricing, 91–99c held to resolution, k = 1: **0.0585** at 95c (5.73 at 91c → 5.97 at 99c) — PMExperiment/REGISTRATION.md:422-424.
  - registered band **0.02–0.08**, top **8.00** points — PMExperiment/REGISTRATION.md:221, 253-256.
  - fee + half-spread alone, held route, before FX: **0.0300** vs band bottom 0.0200 — PMExperiment/HYPOTHESES.md:140; PMExperiment/REGISTRATION.md:457-459.
  - surviving share: top **2.15 of 6.0** points at 95c — PMExperiment/HYPOTHESES.md:146; PMExperiment/REGISTRATION.md:1049-1050.
  - magnitudes cited at 91–99c: Bürgi's **0.020** and **0.030**, both fail; **n = 313,972 contract prices on 46,282 contracts across 12,403 events** — PMExperiment/HYPOTHESES.md:143; PMExperiment/REGISTRATION.md:227-228, 440-443.
  - the only cited magnitude that clears: Krause's **0.077** at exploitable entry price **0.883** — **n not recorded anywhere** — PMExperiment/HYPOTHESES.md:144; PMExperiment/DECISIONS.md:250, 266-270.
  - BAND-NARROW could not be evaluated: the volume clause needed a floor that was unregistered at the time — PMExperiment/REGISTRATION.md:417. (Floor later registered at **$1,000** by Amendment 5, 2026-08-30 — PMExperiment/REGISTRATION.md:862; its cost in sample **never measured**, reported absent not zero — PMExperiment/REGISTRATION.md:485.)
- **File:line:** PMExperiment/REGISTRATION.md:402-459; PMExperiment/HYPOTHESES.md:119-160; PMExperiment/DECISIONS.md:208-308 (ADR-009, ADR-010); PMExperiment/report.md:59-137; evidence in `docs/BAND.md` *(other reader)*.
- **Blockers (file:line):** none — the gate needed no access ("No venue was read", PMExperiment/REGISTRATION.md:404-407).
- **Reopen conditions (file:line):** **none, by registration.** "Amendment 2 fixes the band as computed once: it is not recomputed after a calibration result is seen, and no bucket may be added to it afterwards. A different verdict requires a revised cost component entering by numbered amendment with its own evidence" — PMExperiment/HYPOTHESES.md:153-157; reinforced at closure, "no route permits recomputing the fee-versus-edge band … no bucket may be added to it afterwards" — PMExperiment/REGISTRATION.md:1107-1108.
- **Possibly met by another repository?** No — the band depends on no external state. Cross-repo note only: the FX and fee assumptions are Canadian-retail constants that a sibling repository may have measured; a measured turnover k would require its own numbered amendment (PMExperiment/DECISIONS.md:295-296).

---

## 10. Gate — the Polymarket access gate (Section 15.3)

- **Status:** FIRED **PENDING_ACCESS**, 2026-08-30.
- **Closure kind:** access verdict on published terms; **zero market-data requests sent**.
- **Closure date:** 2026-08-30.
- **Deciding figures with n:** Terms of Use **59,617 bytes**, effective **2026-08-11**, read in full (PMExperiment/REGISTRATION.md:479); `robots.txt` HTTP 200 in 35.7 ms, 73 bytes, **no `Disallow` of any kind** (PMExperiment/REGISTRATION.md:477); API-host `robots.txt` HTTP 404 ×3 (PMExperiment/REGISTRATION.md:478); request log **7 requests**, none for a contract, price, order book or resolution (PMExperiment/REGISTRATION.md:502-506); **contracts enumerated 0** (PMExperiment/REGISTRATION.md:484); reachability/rate limits/history depth **WITHHELD — not measured** (PMExperiment/REGISTRATION.md:483, 487-493).
- **File:line:** PMExperiment/REGISTRATION.md:461-513; Amendment 6 at :912-1005; PMExperiment/DECISIONS.md:344-389 (ADR-012); PMExperiment/HYPOTHESES.md:164-203; PMExperiment/report.md:141-232.
- **Blockers (file:line):** the crawlers bullet (PMExperiment/REGISTRATION.md:938-940); binding notice reaching "CONNECTING VIA AN API" (PMExperiment/REGISTRATION.md:949-952); Restricted-Jurisdiction narrowing for AB/BC/ON/QC (PMExperiment/REGISTRATION.md:988-994); no developer licence granting what the Terms withhold (PMExperiment/REGISTRATION.md:996-999).
  - **Recorded as NOT binding:** the Data clause (the one naming on-chain) is conditional on entity type and "is **not** the ground of this finding" (PMExperiment/REGISTRATION.md:967-972). The binding crawlers bullet is scoped to "the Site, any other Interface, or Features", and "**a public Polygon ledger is none of the three on its face**" (PMExperiment/DECISIONS.md:426-428). See DRAFT-p1-register-3.
- **Reopen conditions (file:line):** PMExperiment/REGISTRATION.md:1001-1005 and :508-512 — (a) prior written consent from Adventure One QSS, Inc.; (b) enrolment in the builder program the Terms name; (c) **a Polygon read through infrastructure that is not a Polymarket Interface, "under a legal analysis this repository has not done" — recorded as an open question**. Amendment 9 adds condition 4 to H1 (a Polymarket data licence) at PMExperiment/REGISTRATION.md:1161-1167.
- **Trigger status:** (c) is **open and unanswered** at closure; ADR-013's verification pass found the binding bullet does not on its face reach a public ledger (PMExperiment/DECISIONS.md:426-428), and no document performs the analysis. (b)'s published upgrade path is gated on "Route orders through Polymarket", which this repository cannot pass (PMExperiment/DECISIONS.md:404-405).
- **Possibly met by another repository?** **Possibly — flag.** If a sibling repository has performed a Polygon/on-chain read through non-Polymarket infrastructure, or holds a legal analysis of that route, it bears directly on reopening path (c).

---

## 11. Route — a Polymarket written-authorization request (Stage D candidate 1)

- **Status:** CLOSED **PROHIBITED (baseline)**, 2026-08-30. Label deliberately precise: "Nothing was requested, so nothing was refused." (PMExperiment/DECISIONS.md:419-421).
- **Closure kind:** licence/permission verdict on the in-force Terms.
- **Closure date:** 2026-08-30.
- **Deciding figures with n:** six published contact addresses, **none designated for this asker**; `Notices` **0 occurrences**, `authorization` **0 occurrences** across **58,830 characters**; Terms read in full as 14 contiguous chunks (PMExperiment/HYPOTHESES.md:217; PMExperiment/DECISIONS.md:398-416).
- **File:line:** PMExperiment/HYPOTHESES.md:217; PMExperiment/DECISIONS.md:393-445 (ADR-013); PMExperiment/REGISTRATION.md:599; PMExperiment/report.md:278-285.
- **Blockers (file:line):** `data-licensing@polymarket.com` scoped to "Capital Markets Entities"; builder upgrade gated on routing orders; Contact Us scoped to Features; no notices clause, no postal address (PMExperiment/DECISIONS.md:400-409).
- **Reopen conditions (file:line):** written authorization obtained — H1 reopening condition 4 (PMExperiment/REGISTRATION.md:1163-1167); `docs/LICENCES.md` *(other reader)*.
- **Recorded counter-evidence:** the AI/ML axis is measured as a null — `artificial intelligence` **0**, `machine learning` **0** across the Polymarket Terms; "Polymarket has no AI clause where Kalshi has one" (PMExperiment/DECISIONS.md:428-432).
- **Possibly met by another repository?** Possibly — a Polymarket data licence held elsewhere in the program would satisfy H1 reopening condition 4.

---

## 12. Route — published academic datasets (Stage D candidate 2)

- **Status:** CLOSED **UNMEASURED**, 2026-08-30, on ADR-012 elements (1) and (2).
- **Closure kind:** evidence-standard verdict (admissibility), not a merits refusal. "UNMEASURED is not a synonym for PROHIBITED" (PMExperiment/README.md:43-45).
- **Closure date:** 2026-08-30.
- **Deciding figures with n:** `TimeSeventeen/Polymarket-v1` states CC BY 4.0 three times and documents all four gate inputs over **1,201,580,990 rows** spanning 2022-11-21 → 2026-04-28; **no date printed on the card or in the CC BY 4.0 legal code** (element 2 fails); the grant was quoted without Section 1's cap to rights "the Licensor has authority to license" (element 1 fails as an effective grant) — PMExperiment/HYPOTHESES.md:218; PMExperiment/DECISIONS.md:452-468.
- **File:line:** PMExperiment/DECISIONS.md:448-495 (ADR-014); PMExperiment/HYPOTHESES.md:218; PMExperiment/REGISTRATION.md:600; PMExperiment/report.md:286-292.
- **Blockers (file:line):** no printed date on the card or the CC legal code (PMExperiment/DECISIONS.md:462-464); chain of title unestablished (PMExperiment/DECISIONS.md:482-486); AI/ML clause search **unrun** on dataset LICENSE bodies (PMExperiment/DECISIONS.md:485-487); whether a venue's terms reach a downstream on-chain-derived corpus is **UNRESOLVED** (PMExperiment/DECISIONS.md:487-491).
- **Stated limit on the search itself:** "the candidate space was **sampled, not enumerated** — versioned repository deposits (Zenodo, Dataverse, OSF, figshare) were never fetched, and that is the one document class carrying a licence, a date and a version by construction" — PMExperiment/HYPOTHESES.md:233-238; PMExperiment/report.md:306-314; `docs/LICENCES.md:674` calls it "the sharpest gap" *(other reader)*. **Never acted on before closure.** See DRAFT-p1-register-7.
- **Reopen conditions (file:line):** H1 condition 3, "a licensed dataset whose licensor held authority to license" (PMExperiment/REGISTRATION.md:1095-1098); and, for this candidate specifically, "a numbered amendment on version-identity-in-place-of-date, registered *before* the measurement it governs and only alongside closing element (1), the chain of title, and the AI-clause search" (PMExperiment/DECISIONS.md:493-495).
- **Possibly met by another repository?** **Possibly — flag.** Any sibling repository holding a licensed prediction-market corpus with a datable, chain-of-title-clean licence would satisfy H1 condition 3.

---

## 13. Route — third-party platforms (Stage D candidate 3)

- **Status:** CLOSED **PROHIBITED** (Dune) / **UNMEASURED** (Flipside, Allium, Nansen, Sim), 2026-08-30.
- **Closure kind:** licence verdict on the one in-force instrument retrieved; the other four governing documents were never fetched.
- **Closure date:** 2026-08-30.
- **Deciding figures with n:** Dune Terms `Last updated on: June 3rd, 2026`, binding non-registrants, prohibiting "bots, crawlers, scrapers", granting no right in data, API keys only "After the User's subscription to a Subscription Plan"; affirmative permission search returned **zero occurrences each** for `aggregate`, `derived`, `redistribute`, `republish`, `resell`, `commercial use`, `creative commons`, `open source`, `public domain`; tier price **UNMEASURED** (pricing page is a client-rendered shell at **0.14–0.40 % text**) — PMExperiment/HYPOTHESES.md:219; PMExperiment/DECISIONS.md:507-521.
- **File:line:** PMExperiment/DECISIONS.md:499-547 (ADR-015); PMExperiment/HYPOTHESES.md:219; PMExperiment/REGISTRATION.md:601; PMExperiment/report.md:268-277.
- **Blockers (file:line):** account + terms acceptance + payment, all outside standing rule 11 (PMExperiment/HYPOTHESES.md:225-227); four platforms' governing documents never retrieved (PMExperiment/DECISIONS.md:504-505).
- **Self-correction recorded with the verdict:** the first read declared the current Terms unreadable, quoted a superseded May 2025 archive and published PROHIBITED anyway; "bare `curl` returns 403; the same `curl` with nothing added but a browser `User-Agent` returns **HTTP 200**" — PMExperiment/DECISIONS.md:523-540; PMExperiment/README.md:51-63.
- **Reopen conditions (file:line):** "a paid platform tier, which needs an account, an acceptance of terms and a payment, all outside standing rule 11" (PMExperiment/HYPOTHESES.md:225-227). Independent of every clause: "Dune's terms nowhere establish that Dune holds redistributable rights in the third-party prediction-market data it surfaces" (PMExperiment/DECISIONS.md:542-547).
- **Possibly met by another repository?** Possibly — a sibling repository holding a paid Dune/Flipside/Allium/Nansen/Sim subscription would move the four UNMEASURED rows and the account/payment blocker.

---

## 14. Route — Kalshi Internal Use (Section 15.4)

- **Status:** **EXISTS-AND-UNTRAVELLED**, recorded 2026-09-01 on correspondence received 2026-09-01. **Not declined on the merits.** Not PERMITTED.
- **Closure kind:** correspondence recorded as an access finding; admissibility **UNMEASURED on element (2)** (received date, not effective date), with element (1) unmet in substance because the repository holds the operator's summary, not the reply's text (PMExperiment/REGISTRATION.md:546-556; PMExperiment/DECISIONS.md:581-609).
- **Closure date:** recorded 2026-09-02 (ADR-016); reply received 2026-09-01.
- **Deciding figures with n:** licence granted **none**; fee **UNMEASURED**; publication permission **UNRESOLVED**; AI/ML consent **UNRESOLVED**; contracts enumerated, requests sent, dollars spent **0, 0, 0**; historical depth **2021 onward** through historical endpoints; Stage A's keyless cutoff restated as 2024-01-01→2024-05-31, **n = 6** (PMExperiment/REGISTRATION.md:533-544).
- **File:line:** PMExperiment/REGISTRATION.md:517-569; PMExperiment/DECISIONS.md:551-629 (ADR-016); PMExperiment/report.md:361-410; PMExperiment/README.md:120.
- **Blockers (file:line):** an established legal entity with formation documents and beneficial-owner verification (PMExperiment/REGISTRATION.md:536); operator holds none (PMExperiment/REGISTRATION.md:537); both entity paths declined by the operator 2026-09-02 (PMExperiment/REGISTRATION.md:1043-1046).
- **Procedural blind spot recorded and deliberately not repaired:** `missing_elements()` "checks only that `clause` is non-empty, so it would score a paraphrase as satisfying element (1)" (PMExperiment/DECISIONS.md:598-609; PMExperiment/README.md:47-49).
- **Reopen conditions (file:line):** H1 conditions 1 and 2 (PMExperiment/REGISTRATION.md:1085-1094). Note the register's own foreclosure: a reply to the pending academic-tier question "is not a reopening" (PMExperiment/REGISTRATION.md:1100-1102), pinned by `tests/test_honesty.py:471-476` *(other reader)*. See DRAFT-p1-register-5.
- **Possibly met by another repository?** **YES — flag.** An established legal entity, or Kalshi institutional/academic standing, held anywhere else in the program.

---

## 15. Decision — the entity path declined (Amendment 7 / ADR-017)

- **Status:** DECLINED by the operator, 2026-09-02. Filed as a cost decision, explicitly **not** evidence about H1.
- **Closure kind:** operator cost decision. "This one rests on a person's judgement about their own time and money" (PMExperiment/DECISIONS.md:652-654).
- **Closure date:** 2026-09-02.
- **Deciding figures with n:** the operator's stated prior **5 to 8 percent**, given 2026-09-02 at closure, **not pre-registered** (PMExperiment/REGISTRATION.md:1018-1029); the "thin" band figures — surviving region top **2.15 of 6.0** points at 95c, requiring **5.85** points at k = 1 against a band top of **8.00**, with Bürgi's **2.0** and **3.0** failing the **0.0300** floor (PMExperiment/REGISTRATION.md:1048-1054). Section 13 left permanently empty (PMExperiment/REGISTRATION.md:1015-1016).
- **File:line:** PMExperiment/REGISTRATION.md:1009-1067; PMExperiment/DECISIONS.md:633-681 (ADR-017); PMExperiment/report.md:412-432.
- **Blockers (file:line):** university sponsorship "not achievable in the time available"; personal entity "disproportionate" (PMExperiment/REGISTRATION.md:1045-1046).
- **Reopen conditions (file:line):** none written as such; the decision is reversible by the operator at any time and is not a finding (PMExperiment/DECISIONS.md:648-654).
- **Audit note:** the "thin" figure that is the stated input to this decision is challenged in DRAFT-p1-register-1 (its thinness is produced by the registered fee and FX assumptions, both of which Section 2 records as overstating cost).
- **Possibly met by another repository?** Not applicable — an operator decision, not an external condition.

---

## 16. Registered closure conditions (Section 16) — status: NEVER MET

- **Status:** **never met**, recorded as such rather than as satisfied by a substitute.
- **Registered condition:** "**H1 closes** if both verdict cells fire BLOCKED … with the realized MDEs and their n beside it" (PMExperiment/REGISTRATION.md:643-647).
- **Actual:** "**Neither cell ever fired.** There is no realized MDE because there is no enumeration to compute one from. **H1 does not close under Section 16 at all**" (PMExperiment/REGISTRATION.md:636-641; PMExperiment/DECISIONS.md:720-727).
- **Registered reopening inside Section 16:** "the permitted subset accumulates settled contracts with the calendar, so a later session may refire the gate on a fresh enumeration as a new numbered firing — the gate reads no outcome, so refiring is not a second look" (PMExperiment/REGISTRATION.md:651-654). **This calendar-accrual reopening is not carried into Amendment 8's "exhaustive" list**, and Amendment 8 restricts any reopened firing to 91–99c only (PMExperiment/REGISTRATION.md:1106-1111).
- **Possibly met by another repository?** No — it is a property of this repository's own enumeration, which never happened.

---

## Summary of trigger status across all registered reopen conditions

| # | condition | file:line | met as of anchor? | possibly met by another repo? |
|---|---|---|---|---|
| H1-1 | established legal entity applying for Internal Use | REGISTRATION.md:1085-1091 | no — declined by operator | **yes, flag** |
| H1-2 | a Kalshi academic tier, if one is offered | REGISTRATION.md:1092-1094 | **pending and unanswered**; the only instrument that could establish it is pre-declared a non-reopening (:1100-1102) | **yes, flag** |
| H1-3 | a licensed dataset whose licensor held authority to license | REGISTRATION.md:1095-1098 | no; the document class most likely to satisfy it was never fetched (report.md:306-311) | **yes, flag** |
| H1-4 | a Polymarket data licence or written authorization | REGISTRATION.md:1161-1167 | no | possibly |
| 15.1-a | written Kalshi authorization | REGISTRATION.md:395-396 | no | **yes, flag** |
| 15.1-b | Kalshi-sanctioned keyless bulk channel | REGISTRATION.md:396-397 | no | **yes, flag** |
| 15.1-c | operator decision to register an account | REGISTRATION.md:397-398 | **obstacle expired 2026-08-30** (:756-757); never revisited; dropped from Amendment 8's exhaustive list | no |
| A6-c | Polygon read through non-Polymarket infrastructure | REGISTRATION.md:1002-1005 | **open, unanswered**; DECISIONS.md:426-428 records the binding clause does not reach a public ledger on its face | possibly |
| S16 | calendar accrual in the permitted subset, refire the gate | REGISTRATION.md:651-654 | not applicable — no enumeration ever existed | no |
| H1t | measurement on the venue where the trade would be placed | HYPOTHESES.md:104 | no | **yes, flag** (MLCryptoEngine H2, AUC 0.501) |
| arb | "Nothing at retail latency" | HYPOTHESES.md:63 | no reopening exists by construction | possibly (latency measurements elsewhere) |
| sports | a change in CIRO-permitted categories | HYPOTHESES.md:64 | no | no |
| trading | "Nothing. It is a scope rule" | HYPOTHESES.md:65 | n/a | no |
| band | none — computed once, not recomputable | HYPOTHESES.md:153-157; REGISTRATION.md:1107-1108 | n/a | no |
