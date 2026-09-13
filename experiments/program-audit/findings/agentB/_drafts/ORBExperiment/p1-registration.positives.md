# POSITIVES LEDGER — ORBExperiment, part p1-registration

**Repository:** ORBExperiment · **Anchored SHA:** `f2aa675a80fc06b74979040b3028154d1add5ec0`
(main, 2026-08-29). **Snapshot:** `/home/kiros-li/.cache/program-audit/scratchpad/snap/ORBExperiment/`.

**Scope of this ledger:** every positive, qualified positive, shipped procedure, open item and
thresholded negative whose primary record sits in the p1-registration document set —
`REGISTRATION.md` (4,193 lines), `HYPOTHESES.md` (175), `report.md` (1,080). Entries whose primary
evidence sits in `README.md`, `DECISIONS.md`, `docs/`, `progress.md`, `reports/*.json`, `src/orb/`
or `tools/` are marked *(primary evidence outside my assignment)*; where those documents merely
**frame** an entry recorded here, they appear in the framing field only. Every quote below was
re-checked against the snapshot at the file and line given. Commit facts are the ones the draft
findings file established by read-only `git log` on the live repository on 2026-09-12; this ledger
touched no live repository and marks each such fact *(from the draft's git reads)*.

**This ledger is factual, not advocacy.**

---

## Repository-level facts that frame every row

**No outcome value was ever read.** "**No in-sample or holdout bar has been read**" —
REGISTRATION.md:4075; "**nothing in this repository measured whether the directional edge is
real** — no in-sample or holdout bar was ever read, and both latches remain absent" —
HYPOTHESES.md:63. Neither latch exists: "**Stage C latch** | **absent** … **Stage D latch** |
**absent**" — REGISTRATION.md:2909-2910. So **no entry in this ledger is a return, an edge or a
verdict on the hypothesis**; every one is an access state, an integrity input, a power figure, a
cost measurement, a shipped procedure or a closure label.

**Two of the three inputs the whole design turns on never existed at the anchor.** "**bar
revision rate** | **`Absent(not_yet_measured)`** — eligible **2026-09-12**" and "**cross-vendor
agreement share** | **`Absent(not_yet_measured)`**" — REGISTRATION.md:3630-3631. "**What decides
this repository** | **Not the return. Bar integrity.**" — HYPOTHESES.md:78.

**Zero dollars were spent at every firing.** "**dollars spent** | **0**" —
REGISTRATION.md:3632, :2807.

---

## 1. Positives and qualified positives

### 1.1 `SAME_TAPE` — thresholded positive (a gate-enabler)

| field | content |
|---|---|
| **claim as stated** | "**The verdict on the pair this experiment would use is `SAME_TAPE`. The registered agreement thresholds apply as written, and nothing in Section 0 is disapplied.**" — REGISTRATION.md:1491-1493 |
| **kind** | thresholded positive; it fires no verdict of its own, it licenses the registered agreement thresholds to fire at all |
| **deciding figures (n)** | median first-5-minute volume ratio **1.005197**, IQR **[1.003096, 1.007726]**, min 1.000905, max 1.034148, share below 0.20 = 0.0000, **n = 100 session-ticker pairs** (20 tickers × 5 sessions), `n = 60` requests, 200 on every one. Controls: Massive vs Alpaca-IEX **0.027856**, Alpaca-SIP vs Alpaca-IEX **0.027761**, both `n = 100` — REGISTRATION.md:1479-1489 |
| **file:line** | REGISTRATION.md:1426-1493 (branch and measurement); HYPOTHESES.md:70; report.md:296-305 |
| **bar + registration date** | `SAME_TAPE` = median ratio in **`[0.90, 1.10]`**, inclusive both ends; `DIFFERENT_TAPE` strictly below 0.50; `AMBIGUOUS` between — REGISTRATION.md:1433-1437. Registered **2026-08-29** in Amendment 7, and the registration states the ordering: "**The branch text was written before the numbers were read**, and the three verdicts, their thresholds and their consequences were fixed … **before** `tools/tape_identify.py` sent its first request" — REGISTRATION.md:1404-1408 |
| **amendments touching the bar (date, did data exist?)** | Amendment 7 itself, 2026-08-29 — data existing: "Everything Amendment 6 listed, plus the A.1 TASK 3 credentialed probes (`n = 11` …) and the A.1 TASK 4 tape pulls (`n = 60` requests …). **Zero trades, zero returns, zero PnL.**" (REGISTRATION.md:1397-1402). **The branch text predates the numbers; the amendment that carries it does not.** No later amendment moves the tape thresholds |
| **corrections applied** | two controls run alongside rather than the pair alone — one positive control (Massive vs Alpaca-IEX) and one same-vendor/same-host/one-parameter control (Alpaca-SIP vs Alpaca-IEX) "**and why they are in the amendment rather than a footnote**" (REGISTRATION.md:1495-1500); the window substituted post-holdout with the substitution's rationale stated (REGISTRATION.md:1444-1464); a systematic direction inside the PASS recorded rather than smoothed — "**Alpaca-SIP reports more first-5-minute volume than Massive in 100 of 100 pairs**, with a **minimum ratio of 1.000905 — strictly above 1.0**" (report.md:333-337). **Not applied:** any clustering of the 100 pairs into their 5 session or 20 name clusters; no null distribution for the IQR inference |
| **framing in README / report** | report.md:296-305 states the verdict and puts the controls first; README.md:191 carries it as a table row with `n = 100`. The registration **weakens its own PASS in the same amendment**: "**A cross-vendor `PASS` therefore establishes that two redistributors of one upstream agree**, and it is **not the Concretum test**" — REGISTRATION.md:630-634 (SL-1) |
| **audit flag** | DRAFT-p1-registration-11 (sample is 20 mega-caps, not the registered relative-volume universe; 100 pairs are 5 session clusters) |

### 1.2 `SERVING_FULL_REACH` — positive (the access verdict input)

| field | content |
|---|---|
| **claim as stated** | "\| **Alpaca** \| **2016-01-04** \| **16** \| **1,762 of 1,762 — shortfall 0** \| **875 of 875 — shortfall 0** \|" — REGISTRATION.md:1598; "**Monotonicity was checked rather than assumed.**" — REGISTRATION.md:1601 |
| **kind** | positive (an operational state, `SERVING_FULL_REACH`, REGISTRATION.md:1953) |
| **deciding figures (n)** | earliest served session **2016-01-04**, **`n = 16` probes** per credential, over **`n = 5,934` candidate sessions** spanning 2003-01-02 to 2026-07-29, `n = 32` probes across 2 credentials (REGISTRATION.md:1583-1584). Boundary confirmation: 2015-12-31 → 200, 0 bars; 2016-01-04 → 200, **718** bars; 2016-01-05 → 200, **694** bars (REGISTRATION.md:1606-1607) |
| **file:line** | REGISTRATION.md:1589-1634, :1953-1956; HYPOTHESES.md:68, :70; report.md:307-309, :322-331 |
| **bar + registration date** | no numeric bar; reach feeds `PENDING_SPEND`, registered **2026-08-29** in Amendment 10: "**It did not fire today**, and the reason is the measurement: Alpaca reaches **1,762 of 1,762 in-sample and 875 of 875 holdout sessions**" — REGISTRATION.md:1855-1857 |
| **amendments touching the bar (date, did data exist?)** | Amendment 8, 2026-08-29 — data existing: "Everything Amendment 7 listed, plus the A.1 TASK 5 bisection: **`n = 32` probes across 2 credentials over `n = 5,934` candidate sessions** … **Zero trades, zero returns, zero PnL**" (REGISTRATION.md:1582-1587). Amendment 10, same day, registers the `PENDING_SPEND` clause the figure keeps from firing — data existing then included the 480-file probe pull but **not** the revision measurement (REGISTRATION.md:1844-1849) |
| **corrections applied** | bisection rather than a pricing page ("**Reach was bisected, not read from a pricing page.**", REGISTRATION.md:1591); refusal and empty-set families separated by **status code plus bar count, never by count alone** (REGISTRATION.md:1615-1620); the coincidence recorded as fragile rather than as comfort — "**This is not a comfortable pass. It is an exact one.**" (REGISTRATION.md:1634); the superseded `docs/ACCESS.md` primary-vendor recommendation left standing rather than edited (REGISTRATION.md:1640-1649). **Not applied:** any per-name or per-session coverage measurement behind the "1,762 of 1,762" |
| **framing in README / report** | README.md:63-65 "The primary reaches **every registered session**"; report.md:322-331 records the zero-margin coincidence at full strength |
| **audit flag** | DRAFT-p1-registration-5 (the bisection ran on one ticker; the single-ticker basis appears in none of the five markdown documents) |

### 1.3 Delisted coverage `PASS` — thresholded positive

| field | content |
|---|---|
| **claim as stated** | "\| **delisted names with intraday history** \| **203**, `n = 229` checked — **`PASS`** \|" — REGISTRATION.md:1961 |
| **kind** | thresholded positive (a registered count bar crossed) |
| **deciding figures (n)** | **203** names served intraday bars, **n = 229** in-window names checked, share **0.8865**; **4,731** delisted names enumerated inside the registered window, of 6,421 served (REGISTRATION.md:1960-1961; HYPOTHESES.md:70) |
| **file:line** | REGISTRATION.md:1961, :1976, :2804, :3629; HYPOTHESES.md:70; report.md:311-314 |
| **bar + registration date** | "**Delisted coverage, A.1 TASK 4.** `PASS` at **100 or more** delisted names served with intraday history; `PARTIAL` at **20 to 99**; `FAIL` **below 20**." — REGISTRATION.md:118-119, registered **2026-08-29** before any vendor data request (REGISTRATION.md:3-8). BLOCKED-3 (`== 0`) and BLOCKED-5 (`< 20`) are the same scale-free count (REGISTRATION.md:100, :102) |
| **amendments touching the bar (date, did data exist?)** | **The bar itself is unmoved.** Amendment 10, 2026-08-29, changes the **route** into the map rather than the threshold: `fire_section0` gains a keyword-only `delisted_with_intraday` input so an absent agreement share cannot hide a measured count — "**Pinned on the boundary**: 20 fires `PENDING_REVISION`, **19 fires BLOCKED-5**" (REGISTRATION.md:1897-1904). Data existing then: the probe pull, **no** revision measurement (REGISTRATION.md:1844-1849) |
| **corrections applied** | the combined A.1 TASK 4 verdict registered as "**the worst of the two**" so agreement cannot offset survivorship (REGISTRATION.md:121-124); the share 0.8865 reported beside the count. **Not applied:** any share-based bar; the first-pass `PARTIAL` (81 of 120) and the re-draw to `n = 229` are recorded only in `progress.md` and `reports/stage_a1r/task6_delisted.json` *(primary evidence outside my assignment)* |
| **framing in README / report** | report.md:311-314 and report.md:405-407 ("delisted coverage passing on a measured count of 203 names"); README.md:195 adds the share 0.8865 |
| **audit flag** | DRAFT-p1-registration-10 (the registered bar is a scale-free count; the sample size was enlarged after a shortfall) |

### 1.4 E1 crosses its 80 percent bar, 0.743521 → 0.832450 — qualified positive

| field | content |
|---|---|
| **claim as stated** | "> ## **At the registered 1.40 Sharpe assumption, E1 crosses its 80 percent bar on the achievable holdout for the first time: 0.743521 → 0.832450.**" — REGISTRATION.md:3088; "**The minimum session count for 80 percent power falls from 1,006 to 795, against 875 achievable holdout sessions — a shortfall of 131 sessions becomes a surplus of 80.**" — REGISTRATION.md:3090-3092 |
| **kind** | qualified positive — qualified in the same section: "**A reader must not take 0.832450 as the design's power.**" — REGISTRATION.md:3106-3107 |
| **deciding figures (n)** | E1 at 1.40, holdout: **0.743521 → 0.832450** on **n = 875** sessions; in-sample 0.959720 → 0.980162 on **n = 1,762**; at 2.81 holdout 0.999484 → 0.999835; at 0.70 holdout 0.257802 → 0.366747; min n for 80 percent 1,006 → **795** (REGISTRATION.md:3077-3084). Session counts computed from `orb.calendar`, not the prompt |
| **file:line** | REGISTRATION.md:3000-3117; HYPOTHESES.md:82; report.md:666-695, :750 |
| **bar + registration date** | E1's bar is "**Bar: deflated Sharpe at or above 1.00**" with "**trial count registered at 8**" — REGISTRATION.md:439-444, registered 2026-08-29. The **80 percent power floor** is Section 0's GO clause (REGISTRATION.md:56-60), same date. The quantity corrected is `alpha_adj` |
| **amendments touching the bar (date, did data exist?)** | **Amendment 18, 2026-08-29** — replaces the Šidák union correction `alpha_adj = 0.02532057` with Berger (1982)'s intersection-union argument, each component at 0.05. Data existing: "Everything held at Amendments 11 through 17 … **No in-sample or holdout bar had been read; both latches remain absent** … **This amendment required no measurement at all** — it is a correction to arithmetic that was wrong from the first commit" (REGISTRATION.md:3005-3010). The deflated-Sharpe bar of 1.00 and the trial count of 8 are explicitly untouched (REGISTRATION.md:3116) |
| **corrections applied** | the correction is stated as a registration error, not a fact about the world ("**No datum changed. No vendor changed. No session was added.**", REGISTRATION.md:3094-3097); ADR-005's superseded shortfall is left unedited (REGISTRATION.md:3099-3102); **the same pass replaced E2 with a harder null (Amendment 19) and pre-registered what a collapse would mean before the shift was measured** (REGISTRATION.md:3233-3246); joint power made the latch quantity in Section 10.1 (REGISTRATION.md:583) |
| **framing in README / report** | report.md:750 and REGISTRATION.md:3603 keep the two questions in separate rows — "**Does the corrected alpha alone move E1 across its 80 percent bar?** \| **YES** … **Does JOINT power clear its 80 percent bar?** \| **NO**"; README.md:110, :256, :308 quote 0.832450 with "min n 795" beside it; HYPOTHESES.md:82 carries both halves in one sentence |
| **audit flag** | none. The draft's "found sound" items 2 and 3 record that the correction is statistically right and that E1 alone is nowhere quoted as the design's power |

### 1.5 `CONFIRMED_CONSOLIDATED` — the sealed slice's feed, qualified positive

| field | content |
|---|---|
| **claim as stated** | "**The manifest records `\"feed\": \"sip\"`, and on its own that is an assertion about a code path, not a measurement of what the vendor served.** So it was confirmed." — REGISTRATION.md:2331-2332; "\| **verdict** \| **`CONFIRMED_CONSOLIDATED`** \|" — REGISTRATION.md:2349 |
| **kind** | qualified positive (a verification of a stored artifact, price-blind) |
| **deciding figures (n)** | chunks sampled **8**, requests sent **16**, chunks that discriminate **7**, discriminating chunks matching the consolidated count **7 of 7**, matching the single-venue count **0 of 7**, median single-venue bar count as a share of consolidated **0.5245**; sealed files **480 of 480**, bars **737,507** (REGISTRATION.md:2341-2349) |
| **file:line** | REGISTRATION.md:2329-2374; report.md:569-577; REGISTRATION.md:2799 (carried into the Amendment 16 firing) |
| **bar + registration date** | no numeric bar. The rule it verifies — `CONFIG.consolidated_feed = "sip"`, keyword-only `feed` with no default, one named escape hatch requiring a stated reason — is registered in **Amendment 13, 2026-08-29** (REGISTRATION.md:2283-2307) |
| **amendments touching the bar (date, did data exist?)** | Amendment 13, 2026-08-29. Data existing: "Everything held at …" (REGISTRATION.md:2248) — the sealed slice existed; **the feed confirmation is run inside the same amendment that registers the guard**, and the amendment records that the tool's first run was wrong (below) |
| **corrections applied** | one uninformative chunk (`AADX`, 0 bars on both feeds) **excluded rather than counted**, and the sample widened from 4 to 8 so the exclusion cost no evidence — "**The first run of the confirmation tool sampled four chunks, hit this case, and returned `NOT_CONFIRMED`** … **The classifier was fixed and the verdict was not**" (REGISTRATION.md:2351-2359); two different ratios (0.027761 volume vs 0.5245 bar count) kept apart explicitly (REGISTRATION.md:2361-2366); the same-day count match declared **not** a revision measurement (REGISTRATION.md:2368-2374) |
| **framing in README / report** | report.md:569-577 records the fixed classifier as the finding; REGISTRATION.md:2799 carries the verdict with its `n = 7 discriminating chunks` |
| **audit flag** | none |

### 1.6 The dispersion bracket, 0.0084 percent wide — qualified positive

| field | content |
|---|---|
| **claim as stated** | "**The bracket is 0.0084 percent wide, so the unmeasured effective date does not matter for this figure — and that is measured rather than hoped.**" — REGISTRATION.md:2626-2627 |
| **kind** | qualified positive (a measurement delivered where the frozen model refuses) |
| **deciding figures (n)** | SEC rate **0** → dispersion **2.0294139**; SEC rate **0.0000206** → **2.0295850**; bracket width **0.000171**, relative width **8.43 × 10⁻⁵**; **n = 550 priced trades** (REGISTRATION.md:2619-2632) |
| **file:line** | REGISTRATION.md:2614-2633; report.md:542-551; REGISTRATION.md:2786-2788 |
| **bar + registration date** | Section 6's cost model, registered 2026-08-29 and frozen at hash `3789221b9dd3fea5a9680547dfdf8ec7b1febaf246042fe1fa70e27ca610fba3` in **Amendment 3, 2026-08-29** (REGISTRATION.md:1091-1097) |
| **amendments touching the bar (date, did data exist?)** | Amendment 3, 2026-08-29 — data existing: "the session calendar of A.2 TASK 1, the A.1 access findings, and the live fee pages fetched below. **Zero bars, zero prices, zero volumes, zero trades and zero returns.**" (REGISTRATION.md:998-1000). Amendment 15, 2026-08-29, computes the bracket; **the frozen model is not changed to admit the figure** |
| **corrections applied** | the one unmeasured component varied across **both** ends, the zero end justified as arithmetic rather than assumption ("a fee cannot be negative", REGISTRATION.md:2621); the registered figure under the frozen model still recorded as **`Absent`** beside the bracketed one (REGISTRATION.md:2631-2633) |
| **framing in README / report** | report.md:542-551 "**delivered as a bracket rather than as an absence or an invention** … The registered figure under the frozen model is still reported, and it is still **`Absent`**" |
| **audit flag** | none |

### 1.7 The H1b floor scan — "the registered mechanism is confirmed", qualified positive

| field | content |
|---|---|
| **claim as stated** | "### 2. The registered mechanism is confirmed, and so is the competing effect" — REGISTRATION.md:3879; "**It rises monotonically: 0.9742 → 0.9983 → 1.1415 → 1.4767 → 2.1424.**" — REGISTRATION.md:3885; "**The scan confirmed both halves of the registered mechanism**, which is the most interesting thing in it." — report.md:1045 |
| **kind** | qualified positive (feasibility evidence for a hypothesis that is registered and not opened; no verdict, no power figure, no chosen floor) |
| **deciding figures (n)** | five floors 5/10/20/50/100 USD on **n = 42 sessions, 28 evaluable, 200 tickers**; central ÷ shift **0.9742 / 0.9983 / 1.1415 / 1.4767 / 2.1424**; dispersion 2.0296 → 3.1992 USD/share; shift band 0.039967–0.041782 (a 4 percent band); mean relvol of the selection 2.0652 → 1.8216 → 1.6190 → 1.4103 → **1.4381**; selected name-sessions 560/560/560/446/310 (REGISTRATION.md:3867-3877) |
| **file:line** | REGISTRATION.md:3852-3941; HYPOTHESES.md:100-110; report.md:1045-1056 |
| **bar + registration date** | **no bar** — deliberately: "**The floor itself is NOT registered** … **Selecting a floor is part of opening H1b, not part of scanning for it**" (HYPOTHESES.md:102). The mechanism was written before the scan: "**This is a mechanism, not a result, and it is written here before the scan runs**" (HYPOTHESES.md:103), registered in **Amendment 25, 2026-08-30** (REGISTRATION.md:3798-3814) |
| **amendments touching the bar (date, did data exist?)** | Amendment 25, 2026-08-30 — data existing: "Everything held at Amendments 11 through 24 … **The Stage A.3 slippage-band measurement and the price-floor scan had not been run.**" (REGISTRATION.md:3766-3770). Amendment 27, 2026-08-30, runs the scan — data existing: "Everything held at Amendments 11 through 26 … **Zero dollars spent, zero requests sent by this scan**" (REGISTRATION.md:3857-3860). **Amendment 24 §6 walled the scan off from H1's outcome before either ran** (REGISTRATION.md:3740-3748) |
| **corrections applied** | the multiplicity cost paid explicitly — trial count **8 → 9 for H1b only**, H1's 8 unchanged, "**because the filter change was proposed AFTER seeing an H1 null**" (HYPOTHESES.md:105; REGISTRATION.md:3816-3828); one column disqualified on its own sample — "**The \"sessions filling 20\" column measures the SCAN SAMPLE, not the registered universe**" (REGISTRATION.md:3903-3909); the entry-overshoot column labelled a resolution limit that "**supports the price-invariance claim only weakly**" (REGISTRATION.md:3929-3930). **Not applied:** any correction for the trades-per-session thinning inside the ratio column; the relative-volume reversal at 100 USD is not mentioned in §2 |
| **framing in README / report** | report.md:1045-1056 repeats §2 and §3 together; README.md:329 carries the 100 USD row with "**0 of 28**" beside it |
| **audit flag** | DRAFT-p1-registration-3 |

### 1.8 Massive's rate ceiling, 5.00 per minute — positive (a measurement)

| field | content |
|---|---|
| **claim as stated** | "**1. Massive's measured ceiling is 5 requests per minute, on both endpoints.** First refusal at request **6 of 8** in both `n = 8` cells." — REGISTRATION.md:1769-1770; "**2. Documented and measured agree, and that is recorded as a finding.**" — REGISTRATION.md:1776 |
| **kind** | positive (a measurement that agrees with documentation) |
| **deciding figures (n)** | `/v3/reference/tickers` at 2.0 s: **n = 8**, 30.45/min achieved, **5 admitted**, `{200: 5, 429: 3}`, first refusal request 6; `/v2/aggs/…/1/minute/…` at 2.0 s: **n = 8**, 28.67/min, 5 admitted, first refusal request 6; at 0.5 s: n = 12, **0 admitted**, `{429: 12}` (REGISTRATION.md:1749-1753). Agreement across **`n = 2` endpoints**, measured separately |
| **file:line** | REGISTRATION.md:1747-1789; HYPOTHESES.md:70; report.md:316-318 |
| **bar + registration date** | no bar; the **pace rule** is registered: "**Half the measured ceiling, per endpoint**" — REGISTRATION.md:1793, Amendment 9, 2026-08-29, superseding Amendment 2's provisional and explicitly unmeasured 6.0 s default (REGISTRATION.md:982-990, dated 2026-08-29, data existing: `n = 18` unauthenticated requests and **zero bars**) |
| **amendments touching the bar (date, did data exist?)** | Amendment 2, 2026-08-29 (provisional, labelled unmeasured, zero bars); Amendment 9, 2026-08-29 (the measurement, on credentials). Amendment 9 is "**that task**" Amendment 2 promised, and Amendment 2 is "**left visible and unedited**" (REGISTRATION.md:1727-1730) |
| **corrections applied** | the 88.4/min unauthenticated figure refused as evidence about the data endpoint under solattn ADR-021, and the refusal vindicated — "the authenticated path refuses at 5 per minute. The unauthenticated figure overstated the real ceiling by **17.7×**" (report.md:281-283); ceiling and pace kept as separate objects, `orb.vendors.PACE_BASIS` recording which each endpoint rests on (REGISTRATION.md:1804-1810); Alpaca's unreached ceiling recorded as `None` rather than a large number (REGISTRATION.md:1784-1789) |
| **framing in README / report** | report.md:279-285 presents it as a prediction that "held in the direction that costs something rather than the direction that flatters"; HYPOTHESES.md:70 carries it with its n |
| **audit flag** | DRAFT-p1-registration-9 (`massive:grouped` carries an inherited value inside a dict documented as measured; the Massive observation never exceeded one rolling minute). The draft records the direction of that error as running against the repository's own interest |

### 1.9 Alpaca's sustained rate, at or above 199.73 per minute — qualified positive

| field | content |
|---|---|
| **claim as stated** | "**The sustained ceiling is therefore at or above 199.73 per minute and is not known exactly.** That is a **lower bound, never a ceiling**" — REGISTRATION.md:2478-2479 |
| **kind** | qualified positive (a lower bound, explicitly refused entry into the ceiling dict) |
| **deciding figures (n)** | requests sent **250**, admitted **250**, refusals **0**, elapsed **75.10 s** (longer than one rolling minute), sustained admitted rate **199.73/min** (REGISTRATION.md:2470-2476). Phase 1 burst: **384 admitted in 55.96 s**, refusal at cumulative request 385, 391 sent (REGISTRATION.md:2801, report.md:594-595) |
| **file:line** | REGISTRATION.md:2463-2510; report.md:587-614; REGISTRATION.md:2800-2803 |
| **bar + registration date** | no bar. The rule that binds it — an unreached ceiling stays `None`, and an operating pace is at most half a **measured** ceiling — is Amendment 9's, 2026-08-29 (REGISTRATION.md:1784-1810); Amendment 14, 2026-08-29, adds `MEASURED_SUSTAINED_ADMITTED_PER_MINUTE` as a separate field (REGISTRATION.md:2490-2497) |
| **amendments touching the bar (date, did data exist?)** | Amendment 14, 2026-08-29 — data existing: "Everything held at …" (REGISTRATION.md:2391); no bar, no verdict input moves |
| **corrections applied** | burst distinguished from ceiling — "**a token bucket of capacity near 400 refilling at the documented 200 per minute produces exactly that observation** … recording **411.72 per minute** as *the ceiling* would be the ADR-026 error running in reverse" (REGISTRATION.md:2453-2461); the tool's own first analysis (an operating pace of 689.37/min) corrected before registration (report.md:601-604); the falsified A.1 TASK 7 figure of 134.05/min recorded as falsified at 223.16/min, `n = 25` (report.md:612-614); the sibling-endpoint test rewritten "**from a proxy to the rule**" (REGISTRATION.md:2506-2510) |
| **framing in README / report** | report.md:606-610 states the lower bound and that the ceiling entry stays `None`; README.md:231 carries "**not reached** — 250 of 250 at **199.73/min**" |
| **audit flag** | none |

### 1.10 The measured trigger rate, 0.982143 — qualified positive (a measurement that cost the design its description)

| field | content |
|---|---|
| **claim as stated** | "\| **measured trigger rate** \| **0.982143** \|" with "\| **n** \| **560 selected name-sessions** — 28 evaluable sessions × the registered 20 \|" — REGISTRATION.md:2639-2640; "**The measurement wins and the disagreement is a recorded finding, not a quiet correction.**" — REGISTRATION.md:2648-2649 |
| **kind** | qualified positive (a measurement); its consequence is a **narrowing** of what a later positive verdict could claim |
| **deciding figures (n)** | trigger rate **0.982143**, **n = 560** selected name-sessions over **28** evaluable post-holdout sessions; assumption replaced **0.55**, disagreement **+0.432**; long-only rate **0.525**, n = 560; ambiguous triggers **0**, n = 560; trades per session **19.64** of a registered 20; stop/close exits **210 / 340** (REGISTRATION.md:2637-2646) |
| **file:line** | REGISTRATION.md:2635-2665, :211-233 (Section 1.1), :700-717 (Section 11.2); HYPOTHESES.md:67, :81; report.md:460-479, :807-839 |
| **bar + registration date** | no bar. Section 9 registered the rate as a target, not an input: "**a trigger rate that is a measurement target and never an assumption**" — REGISTRATION.md:531, registered 2026-08-29 |
| **amendments touching the bar (date, did data exist?)** | **Amendment 22, 2026-08-29** restates Section 1 on the measurement and adds Section 11.2 — data existing: "Everything held at Amendments 11 through 21 … the measured trigger rate of …" (REGISTRATION.md:3497-3498). The rule itself is not changed: "**The registered rule is unchanged and stands.** Sections 2, 3, 4, 5 and 6 are byte-for-byte as registered. **Only the description was wrong**" (report.md:820-822) |
| **corrections applied** | stated narrowly against over-reading — "**It is not the in-sample trigger rate and this amendment does not claim it is**" (REGISTRATION.md:2658-2659); the near-coincidence of the long-only 0.525 with the 0.55 assumption recorded "**without a claim attached**" and left undecided (REGISTRATION.md:2661-2665); the cost to a later positive verdict registered rather than absorbed (REGISTRATION.md:707-714). **Not applied:** any correction for the 199-name pool the top-20 rank statistic was drawn from |
| **framing in README / report** | report.md:807-839 puts the restatement and its cost together; HYPOTHESES.md:81 carries the restated hypothesis and the §11.2 consequence in one row |
| **audit flag** | DRAFT-p1-registration-12 (rank-tail dilution and a survivor-only sampling frame sit uncorrected in front of every carve-out figure, including this one) |

### 1.11 The ambiguous rate, 0.000000 on n = 560 — positive (a registered exclusion measured cheap)

| field | content |
|---|---|
| **claim as stated** | "**A zero count is reported with its uncertainty, not as a certainty.** By the **rule of three**, a one-sided 95 percent upper bound on a rate observed zero times in `n = 560` is **3/560 ≈ 0.0054, or 0.54 percent**." — REGISTRATION.md:3312-3314 |
| **kind** | positive (a measurement of a registered exclusion's cost) |
| **deciding figures (n)** | ambiguous rate **0.000000**, **n = 560** selected name-sessions, **0** events; rule-of-three upper bound **0.005357** (REGISTRATION.md:3275, :3310-3316, :3625); long-only sensitivity: ambiguous rate 0.000000 on `n = 294` triggered trades (REGISTRATION.md:3330-3332) |
| **file:line** | REGISTRATION.md:3310-3328, :3625; report.md:796-797 |
| **bar + registration date** | the operator's threshold: "**The 10 percent threshold the operator set was not crossed, so no scope limitation is raised on the ambiguous exclusion, and the exclusion rule is unchanged.**" — REGISTRATION.md:3318-3320. Section 2's ambiguous exclusion registered 2026-08-29 |
| **amendments touching the bar (date, did data exist?)** | Amendment 20, 2026-08-29 measures it — data existing: "Everything held at Amendments 11 through 19 … **including Amendment 19, which fixed E2's null before these figures existed** … **Zero dollars spent. Zero requests sent**" (REGISTRATION.md:3255-3261). "**It changes no rule.** Section 2's ambiguous exclusion stands exactly as registered." (REGISTRATION.md:3336-3337) |
| **corrections applied** | the rule of three applied to a zero count; the mechanism explained "**so a later reader does not mistake it for a bug**" (REGISTRATION.md:3322-3328); a long-only sensitivity recorded because the locate filter is unmeasured (REGISTRATION.md:3330-3332) |
| **framing in README / report** | report.md:796-797 lists it among what was deliberately not changed — "at a measured rate of **0.000000**, `n = 560`, it was not a candidate for change" |
| **audit flag** | none. The draft uses this entry as the internal standard the neighbouring stop-exit share is not held to (DRAFT-p1-registration-1) |

### 1.12 The DEGRADED counterfactual, predicted in writing and confirmed — qualified positive about the method

| field | content |
|---|---|
| **claim as stated** | "**Had bar integrity passed in full, the same power inputs would have fired `DEGRADED`, clause `DEGRADED residual`.**" — REGISTRATION.md:1139-1140; "**The prediction was recorded before the evidence, and the evidence matched it.**" — REGISTRATION.md:1150 |
| **kind** | qualified positive (a methodological claim; it moves no verdict) |
| **deciding figures (n)** | E1 **0.9995** at the published 2.81 and **0.7435** at the registered 1.40, both on **n = 875** holdout sessions computed from `orb.calendar`; min N for 80 percent **1,006**, shortfall **131**; E1 **0.2578** at 0.70 (REGISTRATION.md:1127-1131). Under the corrected alpha the counterfactual is restated on **two** computed powers: "**E1 is 0.7435 and E2 is 0.7435**" (REGISTRATION.md:2826-2830) |
| **file:line** | REGISTRATION.md:139-154 (the registered expectation), :1137-1152, :2825-2830; report.md:175-195, :223-228 |
| **bar + registration date** | the DEGRADED clause and the 0.80/0.50 floors, REGISTRATION.md:56-76, registered **2026-08-29 before any vendor data request** (REGISTRATION.md:3-8); the expectation itself written into Section 0 at the same commit (REGISTRATION.md:141-148) |
| **amendments touching the bar (date, did data exist?)** | none — the GO, DEGRADED and BLOCKED clauses are stated unchanged at every firing: "The GO, DEGRADED and BLOCKED clauses are **unchanged in text, threshold and precedence**" (REGISTRATION.md:945-946), "**`GO` and `DEGRADED` are unchanged in text, threshold and precedence**" (REGISTRATION.md:1924), "**It changes no Section 0 branch.** `src/orb/section0.py` is byte-identical" (REGISTRATION.md:3659-3660) |
| **corrections applied** | the residual band named in advance rather than discovered (REGISTRATION.md:78-86); the two disagreements with the prompt resolved in the conservative direction, one session each (report.md:197-200); the holdout shortfall against the registration's own ~880 carried into the gate with "**the computation wins**" (report.md:114-118) |
| **framing in README / report** | report.md:186-188 quotes the clause "word for word"; report.md:223-228 states it is "**the only circumstance in which a DEGRADED reads as a documented answer rather than a disappointment**" |
| **audit flag** | none |

---

## 2. Shipped procedures and artifacts

| artifact | claim as stated (file:line) | kind | deciding figures (n) | bar + registration date | amendments touching it | corrections applied | framing |
|---|---|---|---|---|---|---|---|
| **`orb.section0.fire_section0`** and its boundary suite | "A totality test walks the full 4 × 4 × 6 × 6 input lattice, **n = 576 combinations**, and requires that every one fires exactly one registered verdict and that all three verdicts are reachable." — REGISTRATION.md:134-137 | shipped | **n = 576** lattice combinations; boundary fixtures on 0.005, 0.020, 0.95, 0.85, 100, 20, 0.80, 0.50, each stepped one ULP or one count across (REGISTRATION.md:126-132) | Section 0, registered 2026-08-29 before any vendor data request (REGISTRATION.md:3-8) | Amendment 1 (2026-08-29, **no data existed at all**, REGISTRATION.md:907) adds `PENDING_ACCESS`; Amendment 10 (2026-08-29, probe pull existed, **revision measurement did not**) adds `PENDING_SPEND` and `PENDING_REVISION` and refines ordering (REGISTRATION.md:1911-1922) | both new states pinned inert once the measurements exist — `test_pending_access_is_not_reachable_when_both_inputs_are_present`, `test_pending_revision_is_not_reachable_when_both_inputs_are_present`; `test_all_five_registered_verdicts_are_reachable` requires no clause be decoration (REGISTRATION.md:942-946, :1927-1931) | report.md:375-379 defends `PENDING_REVISION` as a separate state on the ground that "**the two have completely different next actions**" |
| **`orb.absence.Absent`** | "**No figure is invented and no zero is written**: `orb.absence.Absent` refuses `float()`, `int()`, addition in both directions, ordering and truth-testing, so not one of these cells can be summed into a coverage figure by accident." — report.md:80-82 | shipped | used for **3** absent Section 0 inputs at the first firing (REGISTRATION.md:1133-1135); at the anchor still 2 (:3630-3631) | standing rule 5 ("absence is a recorded state, never a synthesized value"), quoted at REGISTRATION.md:931-932, 2026-08-29 | none | the actions substrate is "**built and unpopulated. `Absent`, no zero written: a zero that was measured and a zero that was never looked for are different facts.**" (report.md:132-133) | report.md:76-82 |
| **`orb.comparator.SealedComparator`** | "compares in **integer cents** — float equality on money is a bug — and returns **only** counts-only findings records. It is pinned four ways" — report.md:84-90 | shipped | 4 pins; known-answer fixtures: one revised bar in five = **exactly 0.20** → FAIL; unchanged re-pull = **0.0** → PASS; a clean re-pull at **13 days** reports `wait_satisfied() == False` (report.md:92-98) | the blindness field lists and the registered comparator exception, 2026-08-29 (quoted REGISTRATION.md:1468-1470) | Amendment 7 relies on it for `compare_tapes` and records that the exception is **not window-limited** (REGISTRATION.md:1466-1475) | "**Guard 5 had a hole and the comparator found it.** … The guard was widened, not the test relaxed" (report.md:100-105) | report.md:84-105 |
| **`orb.power.joint_power`** | "**Joint power is bounded above by the smaller component power, unconditionally.** … So **a reader may never take the larger component power, or either component power, as the design's power**, and `orb.power.joint_power` returns the bound with the binding component named." — REGISTRATION.md:585-590 | shipped | binding component named on every row of REGISTRATION.md:3377-3384 (E2 binds at all six cells) | Section 10.1, appended **2026-08-29 under Amendment 21**, restating clause 1 of the Stage C latch as joint power (REGISTRATION.md:567-583) | Amendment 21, 2026-08-29 — data existing: the corrected alpha, the amended E2, the measured dispersion **2.029585** and the measured shift **0.041455** (REGISTRATION.md:3349-3354) | clause 1 left standing unedited above the append "so the correction is visible" (REGISTRATION.md:569-571) | report.md:757-763 |
| **`tools/repull_probe.py` / `orb.repull.require_due`** and the sealed probe slice | "`orb.repull.require_due` refuses every earlier attempt with exit **78**, naming the date, **having sent nothing.**" — REGISTRATION.md:2932-2933 | shipped | slice: **480 files, 737,507 bars, 2,400 session-ticker pairs, `HTTP 200` on every one** (report.md:362-363; REGISTRATION.md:1845-1846, :1964) | the registered **14-calendar-day wait**, earliest eligible re-pull **2026-09-12** (REGISTRATION.md:1863-1864, :2929) | Amendment 13 adds `require_manifest_feed`, called "**before the first re-pull request is sent**", because "a re-pull sent on a different feed than the original measures a tape difference and records it as a revision rate" (REGISTRATION.md:2299-2304) | "**The wait is the measurement.** A re-pull sent early does not produce a *weaker* revision figure; it produces a **wrong** one, biased toward zero — **and zero is the shape of a `PASS`**" (report.md:367-369) | report.md:360-379; REGISTRATION.md:2925-2933 |
| **The guarded consolidated-feed config field** (Amendment 13) | "**`orb.vendors.alpaca_minute_bars` takes `feed` as a keyword-only parameter with no default**" and "**An exception with no reason recorded at its call site is a default wearing a different name.**" — REGISTRATION.md:2287-2296 | shipped | **5** parse-tree guards plus 3 runtime tests (REGISTRATION.md:2311-2323); **`n = 14` mutations, 0 harness failures**; mutation 14 flips the configured value and is caught by a **guard** (REGISTRATION.md:2325-2327) | registered 2026-08-29, Amendment 13 | none after | "**The default was correct.** … **The defect was that nothing made a call site say which tape it wanted**" (report.md:556-559); the wrong branch costed at a median **0.027761** of consolidated first-5-minute volume over `n = 100` pairs | report.md:553-567 |
| **The frozen cost model** (`REGISTERED_COST_MODEL`, hash `3789221b…`) | "The model is frozen at `orb.costs_registered.REGISTERED_COST_MODEL`, hashed **`3789221b9dd3fea5a9680547dfdf8ec7b1febaf246042fe1fa70e27ca610fba3`** … **A test recomputes the hash from the model and fails if the two diverge.**" — REGISTRATION.md:1091-1095 | shipped | commission 0.0035/share and the 0.35 order minimum agree with carried; FINRA TAF carried **0.000166** vs measured **0.000195** (14.9 percent low); **3** components not modeled at all (report.md:146-151) | Section 6 registered 2026-08-29; frozen in Amendment 3, 2026-08-29, "**written before A.2 TASK 4**" (report.md:170-171) | Amendment 26, 2026-08-30, records a **measured** band beside the carried one and explicitly does not re-register it: "**`CONFIG.entry_slippage`, `stop_slippage` and `close_slippage` are unchanged**" (REGISTRATION.md:4053-4056) | `SEC_FEE_SCHEDULE` left empty because the rate's **effective date** was not measured, so the model refuses (REGISTRATION.md:2598-2602); the 1 percent cap shown to bind below the 0.35 minimum (report.md:153-154) | report.md:137-171 |
| **`orb.dispersion` / the slippage-band tool** | "**So the overshoot distributions are LOWER BOUNDS, the measured band is a lower bound, and any power computed on it is an UPPER bound on power.**" — report.md:925-926, "written into the tool's docstring before the tool ran" — report.md:915-916 | shipped | **457 of 550** entry triggers and **195 of 210** stop triggers crossed intrabar and were recorded at 0.0 overshoot (REGISTRATION.md:4042-4044); quoted half spread measured over **550 minutes served, 0 refused** (entry) and **210 served, 0 refused** (stop) (REGISTRATION.md:3991-3995) | the median→central / p90→pessimistic assignment "**was fixed before any of this was computed**", ADR-038 (REGISTRATION.md:3998-4000) | Amendment 26, 2026-08-30 | the two intrabar cases counted separately so a reader can see how much is bounded rather than measured (report.md:927-928); "**A minute whose quotes are unusable is a refused minute, counted as such, never a zero spread.**" (report.md:939) | report.md:913-939; the draft's "found sound" item 4 records this disclosure as correct and against the repository's interest |
| **Amendment 24, the pre-committed rescue criterion** | "> ### **This amendment exists so the pass cannot be read as a search for a favourable number.** It is committed and pushed **before** TASK 2 computes anything, and the commit order is checkable in `git log`." — REGISTRATION.md:3675 | shipped (a procedure) | required pessimistic-cost mean **0.038493**, required shift **0.001893 or below**, measured shift **0.041455**, **21.89-fold** required reduction; z(0.95)+z(0.80) = **2.486475** on 17,188 trades (**19.642857** per session × 875) (REGISTRATION.md:3690-3697) | registered **2026-08-30**, commit `4ae14dc` *(from the draft's git reads: `git ls-tree -r --name-only 4ae14dc` contains no `slippage_band.py`, `rescue_verdict.py` or `floor_scan.py`; `git log --diff-filter=A -- tools/slippage_band.py` returns `5899e1b`, 27 minutes and four commits later)* | none — Amendment 28 applies it unchanged | "`GO` is unreachable and is not a tier" ruled out **arithmetically in advance** (REGISTRATION.md:3702-3707, :3720); the `NOT_RESCUED` consequence registered before the number existed (REGISTRATION.md:3722-3724); Change B walled off from H1 (REGISTRATION.md:3740-3748) | report.md:874-896; the draft's "found sound" item 1 verifies the ordering and records it as true |
| **The mutation harness** | "**Mutation 13 changed category, and the harness is what noticed.** … The next run reported **`HARNESS FAILURE`** — **and the failure was the harness being right.**" — report.md:618-628 | shipped | close-out state: **`n = 15` mutations, 0 harness failures**, bytecode purged before every run; **385 tests passing** (356 before the pass); `ruff` and `mypy --strict` clean over **55** files (REGISTRATION.md:2901-2905) | standing practice, not a numeric bar | Amendment 17 records the close-out state, 2026-08-29 | "**Nothing about the mutation changed; what changed is that the boundary is pinned twice.**" (report.md:628); one test fixture caught by the registered 0.50 USD ATR filter rather than by an assertion — "The fixture was wrong and the filter was right" (report.md:630-634) | report.md:616-634 |

---

## 3. Open items

| entry | claim as stated (file:line) | kind | deciding figures (n) | bar + registration date | amendments touching it | corrections | framing |
|---|---|---|---|---|---|---|---|
| **Bar revision rate** — the measurement the repository turns on | "**bar revision rate** \| **`Absent(not_yet_measured)`** — eligible **2026-09-12**" — REGISTRATION.md:3630 | open (a recorded absence) | **none exists.** n = 0 (REGISTRATION.md:3630). The sealed slice it will run against: 480 files, 737,507 bars | `PASS` at a changed-bar share **at or below 0.005**; `PARTIAL` above 0.005 and at or below 0.020; `FAIL` above 0.020, firing BLOCKED-2 — REGISTRATION.md:108-111, registered 2026-08-29 | none — the bar is unmoved at every firing | the 14-day wait enforced in code rather than by care (REGISTRATION.md:2931-2933) | report.md:409-411 "**Integrity is the expensive problem and it is fourteen days away.**"; REGISTRATION.md:4192-4193 records that the date now governs a repository whose primary hypothesis is closed |
| **Cross-vendor agreement share** | "**cross-vendor agreement share** \| **`Absent(not_yet_measured)`**" — REGISTRATION.md:3631 | open (a recorded absence) | **none exists.** n = 0. Measurable only over **459** holdout sessions and **0** in-sample (REGISTRATION.md:1670-1675) | `PASS ≥ 0.95`, `PARTIAL ≥ 0.85`, `FAIL` below, firing BLOCKED-4 — REGISTRATION.md:113-116, registered 2026-08-29 | **Amendment 8, 2026-08-29** narrows the **scope** and leaves threshold and precedence unchanged (REGISTRATION.md:1666-1675); data existing then: the reach bisection, **zero trades** (REGISTRATION.md:1582-1587) | the narrowing registered rather than absorbed, with the reason stated: a gate on the recent half of the holdout "is a **weaker instrument than the one registered**" (REGISTRATION.md:1677-1683) | report.md:347-358; SL-1 and SL-2 both make the eventual PASS weaker (REGISTRATION.md:630-636) |
| **H1b** | "**`REGISTERED_NOT_OPEN`** · registered **2026-08-30** (Amendment 25). **It is registered. It is not opened.** No verdict may be computed against it, and none is by this pass." — HYPOTHESES.md:100 | open (registered, not opened) | **none.** No verdict, no power figure, no chosen floor (HYPOTHESES.md:107) | opening it requires "**Its own full registration** … **its own power gate**, computed rather than inherited; and **explicit operator instruction**. **None of the three exists.**" — HYPOTHESES.md:106 | Amendment 25 (registers), Amendment 27 (scans), both 2026-08-30; Amendment 28 "**does not close H1b**" (REGISTRATION.md:4189) | the trial count moves 8 → 9 **for H1b only** (HYPOTHESES.md:105); **no prior recorded** — "A prior belongs with an opened hypothesis" (HYPOTHESES.md:109) | report.md:1036-1043; consistent |
| **H2 — pre-FOMC drift** and **H3 — VIX term-structure roll yield** | "**Status: PARKED**, 2026-08-29. Not closed, not refuted, not tested." — HYPOTHESES.md:151; "**Status: PARKED**, 2026-08-29. Same reason." — HYPOTHESES.md:161 | open (parked) | **none** | no bar; the parking condition was "**No second repository opens while H1 is unresolved.**" — HYPOTHESES.md:137 | H1's closure removes the parking condition and **does not open them**: "**They are not thereby opened**: each still needs its own registration, its own power gate and explicit operator instruction, and **none of the three exists for either.**" — HYPOTHESES.md:140-144 | the reason for parking restated at closure rather than dropped | REGISTRATION.md:4190 "**It does not close H2 or H3**, which remain parked" |
| **Stage C and Stage D latches** | "**Stage C latch** \| **absent** — `data/state/stage_c_read.json` does not exist \| **Stage D latch** \| **absent** — `data/state/stage_d_read.json` does not exist" — REGISTRATION.md:2909-2910 | open (never opened) | latch clause 1 (joint power ≥ 0.80) **UNSATISFIED** at 0.043277 and then 0.000000; clause 2 SATISFIED (operator prior 0.30, `INDEPENDENT`); clause 3 (explicit operator instruction) **UNSATISFIED** — HYPOTHESES.md:86; REGISTRATION.md:592-595 | Section 10, registered 2026-08-29; "**A second read of either window voids the hypothesis.**" — REGISTRATION.md:561 | Section 10.1, appended 2026-08-29 under Amendment 21, restates clause 1 as **joint** power (REGISTRATION.md:583) | "**Storing bars is not reading them**" registered in the verdict record, with the probe slice's holdout overlap named and the Stage D latch stated to govern the holdout in full (REGISTRATION.md:2832-2849) | report.md:235-247 leaves both stage sections reserved and empty |
| **Alpaca's sustained ceiling** | "`MEASURED_CEILING_PER_MINUTE[\"alpaca:bars\"]` **stays `None`**, pinned by `tests/test_vendors.py::test_an_unreached_ceiling_is_none_and_not_a_large_number`, which now also refuses to let a lower bound be written into the ceiling dict." — REGISTRATION.md:2480-2482 | open (deliberately unmeasured) | lower bound **199.73/min** on n = 250; burst **384 in 55.96 s** | Amendment 9's rule that an unreached ceiling is not a number (REGISTRATION.md:1784-1789), 2026-08-29 | Amendment 14, 2026-08-29 | *"The ceiling was not reached"* kept distinct from *"there is no ceiling"* (REGISTRATION.md:1788-1789) | README.md:231 carries "**not reached**" |
| **SL-3's two retirement routes; the costed Massive-tier decision** | "**Neither route is chosen here, neither is recommended here, and no spend is authorised by this subsection.**" — REGISTRATION.md:696-697 | open (operator items) | in-sample sessions with cross-vendor overlap **0** of **1,762**; holdout **459** of **875** (REGISTRATION.md:645-652). The reach a paid tier delivers: "**not measured, and not recorded here as a number**" (REGISTRATION.md:1702) | SL-3 registered **2026-08-29** under Amendment 12 (REGISTRATION.md:640-698) | Amendment 12, 2026-08-29; data existing: everything held at Amendments 11 onward (REGISTRATION.md:2186) | the carried monthly figure labelled **carried**, C-18, "**never measured by this repository**" (REGISTRATION.md:1700); "**If the operator wants that number, the honest way to get it is to buy one month and bisect again**" (REGISTRATION.md:1707-1708) | report.md:413-417 calls the agreement half "**weaker than it was designed to be**" |

---

## 4. Negatives whose verdict rested on a threshold

### 4.1 `PENDING_ACCESS`, 2026-08-29 (Amendment 4)

- **Claim:** "> ## **PENDING_ACCESS** · clause `PENDING-ACCESS Amendment 1`" — REGISTRATION.md:1113, with "*because A.1 TASK 1 measured **0 of 9 vendors serving a bar to this repository**. **Nothing is armed.***" — REGISTRATION.md:1117-1118.
- **Kind:** thresholded negative (an access state, evaluated ahead of every BLOCKED trigger).
- **Deciding figures (n):** **0 of 9** vendors serving a 1-minute RTH bar; **n = 15** robots fetches, **n = 25** API probes (REGISTRATION.md:1106-1107); `n = 7` probes had returned data **n = 0** at the time Amendment 1 was written (REGISTRATION.md:910). Session calendar **2,637** sessions and **21** half sessions; holdout **875**.
- **Bar + registration date:** the `PENDING_ACCESS` clause registered in **Amendment 1, 2026-08-29**, when "**Exactly what data existed when this amendment was made: none.**" (REGISTRATION.md:907-909).
- **Amendments touching the bar:** Amendment 10, 2026-08-29, refines the ordering — Amendment 1's clause stands unchanged when the access verdict is `NO_VENDOR_SERVES`; where a vendor serves, a BLOCKED trigger with a **measured** input fires ahead of the pending states and one with an **absent** input is skipped (REGISTRATION.md:1885-1890). Data existing: the probe pull; **the revision measurement did not and could not exist** (REGISTRATION.md:1847-1849).
- **Corrections applied:** the state registered rather than forcing GO or BLOCKED — "GO would pretend, and BLOCKED would close H1 as `source-integrity-blocked` **on evidence that does not exist**" (REGISTRATION.md:929-931); pinned as not a bypass (REGISTRATION.md:942-946); the counterfactual computed and recorded (entry 1.12).
- **Framing:** report.md:211-231; explicitly **not** a closure kind — "**no bar has been served to fail**" (report.md:219-221).
- **Audit flag:** none.

### 4.2 `PENDING_REVISION`, fired three times (Amendments 10, 16, 23)

- **Claim:** "> ## **PENDING_REVISION** · clause `PENDING-REVISION Amendment 10`" — REGISTRATION.md:1935, repeated at :2759 and :3590; "This is a **parked outcome, not a failure**, and it is **not** a source-integrity closure." — REGISTRATION.md:1940-1941.
- **Kind:** thresholded negative (a parked access/integrity state).
- **Deciding figures (n):** at the third firing — E1 **0.832450**, E2 **0.043277**, JOINT **0.043277** binding on E2, all on **n = 875**; min n E1 **795**, min n E2 **Absent — unreachable**; stop share 0.381818 on **n = 550**; ambiguous 0.000000 on **n = 560**; dispersion 2.029585 on **n = 550**; delisted 203 of **n = 229**; revision and agreement **`Absent`**, n = 0; dollars spent **0** (REGISTRATION.md:3612-3632).
- **Bar + registration date:** the clause registered in **Amendment 10, 2026-08-29** (REGISTRATION.md:1861-1872); the full ten-step clause order at REGISTRATION.md:1911-1922.
- **Amendments touching the bar:** none after Amendment 10. Each re-firing states the branch file is untouched — "**It changes no Section 0 branch.** `src/orb/section0.py` is byte-identical to its state before this pass." (REGISTRATION.md:3659-3660); "**It weakened, requalified and reworded no Section 0 branch.**" (REGISTRATION.md:2919-2920).
- **Corrections applied:** a new firing tool per firing, earlier ones left untouched, all records in one append-only ledger (REGISTRATION.md:2764-2769, :3595-3597); every tool **refuses to record `GO` or `DEGRADED` and exits 78** (REGISTRATION.md:1989-1990, :2768-2769); every E2 figure carries the Amendment 11 post-holdout-regime caveat and every in-sample figure carries SL-3 (REGISTRATION.md:2809-2815, :3634-3636).
- **Framing:** report.md:375-379; HYPOTHESES.md:68.
- **Audit flag:** none on the verdict. The reach and delisted inputs it rests on carry DRAFT-p1-registration-5 and -10.

### 4.3 E2 power collapses and joint power with it — Amendment 21, 2026-08-29

- **Claim:** "> ## **The measured pessimistic shift of 0.041455 USD per share EXCEEDS the implied central mean of 0.040386 at the registered 1.40 Sharpe assumption.**" / "> ## **The pessimistic-cost mean is −0.001068 USD per share. It is negative.**" — REGISTRATION.md:3358, :3360.
- **Kind:** thresholded negative (the alternative lies inside the null; power falls below the size of the test).
- **Deciding figures (n):** at 1.40, holdout **n = 875**: pessimistic mean **−0.001068**, E1 **0.832450**, E2 **0.043277**, JOINT **0.043277**, min n E1 795, min n E2 and JOINT **none**; at 2.81: +0.039606, E2 0.819524, min n JOINT 827; at 0.70: −0.021261, E2 0.001271 (REGISTRATION.md:3377-3384). Inputs: dispersion **2.029585** (n = 550), shift **0.041455** (derived from a stop-exit share of 0.381818, n = 550), **19.642857** trades per session (REGISTRATION.md:3373-3375). Margins: break-even Sharpe **1.437035**, the registered 1.40 below it by **2.577 percent**; break-even stop share **0.346206**, exceeded by **0.035612** (REGISTRATION.md:3417-3424).
- **Bar + registration date:** the pessimistic band **0.040 / 0.080 / 0.020**, registered in Section 6 **2026-08-29 before any data existed** (REGISTRATION.md:3169-3173, :3439-3440); E2's amended null registered in **Amendment 19, 2026-08-29** (REGISTRATION.md:3158-3164); the 0.05 alpha in Amendment 18.
- **Amendments touching the bar (date, did data exist?):** **Amendment 19, 2026-08-29** — data existing: "**The stop-versus-close exit mix and the ambiguous rate were still assumptions when this amendment was written**; they are measured at TASK 3 immediately after it, and **this amendment deliberately fixes the null before the figures that will be fed into it exist.**" (REGISTRATION.md:3128-3131). **Amendment 20, 2026-08-29** measures the mix, with Amendment 19 already fixed "**so the null cannot have been chosen to suit them**" (REGISTRATION.md:3256-3258). **Amendment 21, 2026-08-29** computes the table.
- **Corrections applied:** what a collapse would mean **pre-registered** before the shift existed, and pre-declared not to be grounds to adjust the band, the assumption, the alpha or E2 (REGISTRATION.md:3233-3246); "none" recorded as an absence rather than a large number (REGISTRATION.md:3386-3388); a negative power not clamped (report.md:795); the five things available and not done, listed so a reader can check the diff (REGISTRATION.md:3434-3449); three routes handed over, none chosen (REGISTRATION.md:3451-3479). **Not applied:** any interval, standard error or cluster adjustment on the stop-exit share 0.381818 that decides the sign.
- **Framing:** report.md:726-781 states the collapse first and the thinness second ("**A test with 0.043 power detects nothing**", report.md:767); HYPOTHESES.md:82 carries E1-powered and design-unpowered in the same sentence.
- **Audit flag:** DRAFT-p1-registration-1 (the break-even stop share 0.346206 falls inside the 95 percent interval of the 0.381818 the document prints beside it).

### 4.4 `NOT_RESCUED` and H1 CLOSED `cost-bound`, 2026-08-30 (Amendment 28)

- **Claim:** "> ## **`NOT_RESCUED`**" / "> **The measured shift is 0.467065 USD per share. The central mean at the registered 1.40 assumption is 0.040386. The shift exceeds it by 11.56 times.**" — REGISTRATION.md:4079-4082; register row: "### H1 — H-ORB, the opening-range breakout on relative-volume-selected names · **CLOSED, `cost-bound`, 2026-08-30**" — HYPOTHESES.md:50.
- **Kind:** thresholded negative + a typed closure.
- **Deciding figures (n):** measured band on **n = 42 post-holdout sessions, 28 evaluable, 200 tickers** — entry central **0.087019** / pessimistic **0.354645** (**n = 550**), stop **0.033529 / 0.198061** (**n = 210**), close **0.040000 / 0.261000** (**n = 340**) (REGISTRATION.md:3973-3984); shift **0.467065** against a carried **0.041455**, **11.27×** (REGISTRATION.md:4019-4020); pessimistic mean **−0.426679**, E2 **0.000000**, JOINT **0.000000**, min n **none** at every assumption on n = 875 and n = 1,762 (REGISTRATION.md:4093-4100); at the undecayed 2.81 the pessimistic mean is **−0.386004** and E2 power **0.000000** (REGISTRATION.md:4115-4117).
- **Bar + registration date:** "`RESCUED_DEGRADED` — the TASK 2 measured shift falls **strictly below** **0.040386**" / "`NOT_RESCUED` — the measured shift remains **at or above 0.040386**" — REGISTRATION.md:3711-3718, registered **2026-08-30** in Amendment 24, commit `4ae14dc`, **before a line of the measuring tool existed** (REGISTRATION.md:3959-3961; verified by the draft's read-only `git ls-tree`/`git log --diff-filter=A`). The closure kind `cost-bound` and its consequence were registered in the same amendment (REGISTRATION.md:3724).
- **Amendments touching the bar (date, did data exist?):** **Amendment 24, 2026-08-30** — "**The Stage A.3 slippage-band measurement had not been made and no line of the tool that makes it had been written.**" (REGISTRATION.md:3671-3673). **Amendment 26, 2026-08-30** — data existing: Amendments 11–25 and 27, **`n = 759` quote requests sent**, and Amendment 24 "**already committed and pushed as `4ae14dc`**" (REGISTRATION.md:3958-3962). **Amendment 28, 2026-08-30** — "Everything held at Amendments 11 through 27, **including the measured band of Amendment 26** … **No in-sample or holdout bar has been read.**" (REGISTRATION.md:4071-4075).
- **Corrections applied:** the measured band recorded **beside** the registered one and the registered band **not moved** (REGISTRATION.md:4053-4062); the one overstated leg recorded "**because a measurement is not a reduction**" (REGISTRATION.md:3982-3984); the lower-bound caveat stated where it hurts, with the counts (REGISTRATION.md:4040-4048); the expected halving-heuristic conditionality withdrawn rather than repeated (REGISTRATION.md:4102-4122); seven things available and not done, itemised (REGISTRATION.md:4124-4138); the closure's three supports listed "**so a later reader can attack it**" with the honest attack named (REGISTRATION.md:4140-4157); priors **not** retro-scored because "the event both priors were about **did not resolve**" (REGISTRATION.md:4175-4181).
- **Framing:** report.md:972-1022; README.md:26 and :41-49 carry the closure, the 13.05× and "**E1 remains powered at 0.832450**"; HYPOTHESES.md:58-65 is the register row.
- **Audit flags:** DRAFT-p1-registration-2 (the closure kind `cost-bound` presupposes a measured effect; none was measured, and REGISTRATION.md:3468-3474 named `untestable-at-achievable-power` for this exact ground the day before); DRAFT-p1-registration-4 (the close leg is computed as an absolute two-sided price difference with no spread term, unlike the entry and stop legs); DRAFT-p1-registration-7 (the register row's "negative by 11.56 times the central mean" applies the shift-to-mean multiple to the pessimistic mean; the ratio of magnitudes is 10.565).

### 4.5 Massive's reach shortfall — the agreement gate narrowed (Amendment 8)

- **Claim:** "**Massive's free tier cannot serve the registered windows. That is decisive, it is not worked around, and it removes Massive from consideration as the primary collection vendor.**" — REGISTRATION.md:1638-1640.
- **Kind:** thresholded negative (a reach measurement against the registered windows) + a registered scope narrowing.
- **Deciding figures (n):** earliest served session **2024-08-29**, **n = 16** probes; in-sample **0 of 1,762**, shortfall 1,762; holdout **459 of 875**, shortfall 416 (REGISTRATION.md:1599). Overlap share: in-sample **0.0 percent**, holdout **52.5 percent** (REGISTRATION.md:1661-1664). Combined with SL-1: "**two redistributors of one upstream agree, on 459 of 2,637 registered sessions**" (REGISTRATION.md:1687-1688).
- **Bar + registration date:** no numeric bar on reach; the agreement thresholds it narrows (`PASS ≥ 0.95`, `PARTIAL ≥ 0.85`, FAIL → BLOCKED-4) are Section 0's, registered 2026-08-29 and **"unchanged in threshold and in precedence"** (REGISTRATION.md:1666-1668).
- **Amendments touching the bar:** Amendment 8, 2026-08-29 — data existing: Amendment 7's data plus the bisection, **zero trades, zero returns, zero PnL** (REGISTRATION.md:1582-1586).
- **Corrections applied:** the swap of primary vendor distinguished from a work-around — "a work-around would be keeping Massive as primary and shrinking the window to fit it. **The registered windows do not move.**" (REGISTRATION.md:1646-1649); no power figure moved, and the amendment says so (REGISTRATION.md:1651-1654, :1715-1718); the carried price figure kept labelled carried and the paid tier's reach deliberately not recorded as a number (REGISTRATION.md:1700-1702).
- **Framing:** report.md:264-271 leaves the superseded `docs/ACCESS.md` recommendation standing "so a reader can see the shape of the error — **a vendor chosen on what it publishes rather than on what it serves**".
- **Audit flag:** none.

### 4.6 E2 power `Absent(not_served)` — the pre-period carve-out was never reachable (Amendment 11)

- **Claim:** "**The carve-out was never reachable.** E2 power was therefore recorded `Absent(not_served)` at Amendment 10 rather than computed, and it entered the Section 0 firing as an absence." — REGISTRATION.md:2036-2038.
- **Kind:** thresholded negative (a registered reservation falsified by measurement).
- **Deciding figures (n):** **`n = 2` credentials, 0 serving**; Alpaca earliest served session 2016-01-04 = exactly `CONFIG.in_sample_start`, sessions served before it **0**; Massive 2024-08-29, **0**; **n = 16** probes each (REGISTRATION.md:2026-2034).
- **Bar + registration date:** "**Dispersion inputs to the E2 power computation come from the pre-period carve-out only, strictly before 2016-01-04T14:30:00.000Z.**" — REGISTRATION.md:540-541, registered 2026-08-29.
- **Amendments touching the bar (date, did data exist?):** **Amendment 11, 2026-08-29** makes the carve-out two-sided — data existing: "Everything measured on …" (REGISTRATION.md:2008). The replacement region is **strictly after the holdout ends**, at Eastern rather than UTC midnight, "because UTC midnight on 2026-07-01 is **20:00 Eastern on 2026-06-30** and would have admitted the last holdout session's after-hours bars" (report.md:445-448).
- **Corrections applied:** the cost registered rather than argued away — "**A dispersion figure drawn from a post-holdout regime may misstate in-sample dispersion in either direction by an amount this repository has not measured and does not claim to bound.** It is not asserted to be conservative, it is not asserted to be small" (REGISTRATION.md:2083-2086); the caveat attached to **every** E2 figure produced, in four documents (REGISTRATION.md:2087-2088; report.md:456-458); the direction of the error explicitly unknown (REGISTRATION.md:2093-2095); four boundary fixtures sitting exactly on their edges (REGISTRATION.md:2142).
- **Framing:** report.md:434-458; HYPOTHESES.md:66 carries the caveat inside the verdict row.
- **Audit flag:** DRAFT-p1-registration-12 concerns the sample the replacement region draws from, not the amendment.

### 4.7 The frozen cost model refuses — `Absent`, 550 of 550 trades (Amendment 15 §3)

- **Claim:** "> **The registered figure, under the frozen model, is `Absent(sec_section_31_effective_date_not_measured)`, `n = 550` trades refused.**" — REGISTRATION.md:2610-2612.
- **Kind:** thresholded negative (a refusal, registered as a state rather than a value).
- **Deciding figures (n):** **550 of 550** trades refused; SEC Section 31 rate measured at **0.0000206 per dollar**, its **effective date** not; `sec.gov` HTTP 403 on **`n = 2` further attempts**, **`n = 4` across two sessions**; the stored IBKR schedule carries **no effective date anywhere on the page** (REGISTRATION.md:2598-2608).
- **Bar + registration date:** Section 6's cost model and the empty `SEC_FEE_SCHEDULE`, registered 2026-08-29 and frozen in Amendment 3 the same day.
- **Amendments touching the bar:** none. Amendment 15, 2026-08-29, records the refusal and supplies the bracket **beside** the `Absent`, not instead of it (REGISTRATION.md:2631-2633).
- **Corrections applied:** the refusal preferred to a plausible substitution — "**the model refuses to price a trade rather than take a fee from the wrong year**" (REGISTRATION.md:2601-2602); the bracket varied across both ends with the zero end justified as arithmetic (entry 1.6).
- **Framing:** report.md:156-160 "**The model will not price a trade it cannot price honestly.**"
- **Audit flag:** none; the draft's "found sound" item 6 records this as the cost model refusing rather than guessing.

### 4.8 The ten candidates closed before opening — negatives with no measurement behind them

- **Claim:** "Each was considered as an alternative to H1 and closed **before any data existed**, with a one-line reason. **None was closed on a measurement**, and none of them is reopened by anything H1 does." — HYPOTHESES.md:116-118.
- **Kind:** thresholded negatives only in two cases; the other eight are closures on reasoning, and the register says so.
- **Deciding figures (n):** candidate 1 (index-ETF ORB) rests on carried figures — "**1,775 trades against the paper's 1,795, gross Sharpe 1.06**" and "**the entire gross edge of 0.070 USD per share sits inside the spread**, with **net PnL crossing zero at ~0.022 USD/share against a QQQ spread near 0.010**" (HYPOTHESES.md:122; carried C-5, C-6, REGISTRATION.md:875-876) — **no n is recorded in this repository for the 0.070 or the 0.022**. Candidate 9 carries NPLExperiment's **197/312 positive, exact lower bound 0.5707 against a 0.60 bar** (HYPOTHESES.md:130). The other eight carry **no figure and no n**.
- **Bar + registration date:** registered 2026-08-29 with the register itself; the labelling rule is "**A DUPLICATE is labelled DUPLICATE and names the repository that holds it.**" — HYPOTHESES.md:175.
- **Amendments touching the bar:** none.
- **Corrections applied:** the closures are explicitly marked as **not** measurements (HYPOTHESES.md:117); the two duplicates name the repository that holds each (HYPOTHESES.md:130-131).
- **Framing:** HYPOTHESES.md:15 "Ten candidates closed before opening at registration."
- **Audit flag:** none raised in the draft.

### 4.9 BLOCKED-1 did not fire — an observation recorded and deliberately not acted on

- **Claim:** "**Had BLOCKED-1 been defined on JOINT power at the registered assumption, it would fire — that figure is 0.043277, an order of magnitude below the floor.**" / "**This pass does not change the branch.**" — REGISTRATION.md:3644-3647.
- **Kind:** a recorded non-firing (a negative the map did not produce), against a registered threshold.
- **Deciding figures (n):** BLOCKED-1 is E1 power at the **published** magnitude against `< 0.50`; E1 at 2.81 is **0.999835** on **n = 875**, so it does not fire; JOINT at 1.40 is **0.043277** (REGISTRATION.md:3640-3645).
- **Bar + registration date:** "\| BLOCKED-1 \| E1 power at the published magnitude \| `< 0.50` \|" — REGISTRATION.md:98, registered 2026-08-29 before any vendor data request.
- **Amendments touching the bar:** none — "**It changes no Section 0 branch.** `src/orb/section0.py` is byte-identical to its state before this pass." (REGISTRATION.md:3659-3660).
- **Corrections applied:** the observation recorded in the verdict record "because it is material to the operator's choice" and because "a reader comparing a 0.043277 joint power against a 0.50 BLOCKED floor is entitled to know the branch was evaluated on the input it was registered with rather than on the one that would have fired" (REGISTRATION.md:3647-3651).
- **Framing:** report.md:800-805, same content.
- **Audit flag:** none; the draft's "found sound" item 14 records this as an observation kept against the repository's interest.

### 4.10 The falsified planning figures — negatives recorded against the repository's own documents

- **Claim:** "The operator prompt's assumption that **\"no key is needed for any Stage A source\"** is therefore **falsified by measurement**, and is recorded as falsified rather than worked around." — REGISTRATION.md:922-924.
- **Kind:** thresholded negatives on the repository's own planning documents.
- **Deciding figures (n):** **0 of 9** vendors serve a bar, `n = 7` API probes with `n = 0` returning data (REGISTRATION.md:910-921); the carried FINRA TAF rate **0.000166** against a measured **0.000195**, and **three** components unmodeled (report.md:146-151); the unauthenticated **88.4/min** overstating the authenticated ceiling by **17.7×**, which would have refused **3 of every 8** requests (report.md:281-284); **134.05/min** falsified at **223.16/min**, `n = 25` (report.md:612-614); the **0.55** trigger rate falsified at **0.982143**, n = 560 (entry 1.10); `docs/ACCESS.md`'s primary-vendor recommendation superseded by measurement (REGISTRATION.md:1636-1649).
- **Bar + registration date:** standing rule 4 ("the measurement wins", REGISTRATION.md:1642) and the registration's own disclosure that **no** coverage, revision, agreement, delisting, trigger-rate or slippage figure is registered as an input, every one being named a measurement target (REGISTRATION.md:37-44) — 2026-08-29.
- **Amendments touching the bar:** Amendments 1, 3, 9, 14, 15 record the falsifications; none moves a threshold.
- **Corrections applied:** every falsified figure moves in the direction that **costs** something — the three unmodeled cost components "**All three make the model more expensive**" (report.md:150-151); the superseded recommendation left standing unedited.
- **Framing:** report.md:259-285 "**Three claims went in. Two came out falsified, and the third came out narrower than it went in.**"
- **Audit flag:** none; the draft's "found sound" item 9 records these as falsified in the costly direction.

### 4.11 "The uncomfortable number" — the modeled net edge per share, negative on both legs at 1.40

- **Claim:** "**At the registered assumption the modeled net edge per share is negative on both exit legs.** At the published magnitude, on a stop exit, **two percent of the gross edge survives the cost model**." — report.md:520-522; "**This is not a verdict and it is not evidence about H1.**" — report.md:524.
- **Kind:** thresholded negative, explicitly declared non-verdict-bearing.
- **Deciding figures (n):** close leg at 1.40: gross 0.034875, cost 0.038631, **net −0.003756**; stop leg at 1.40: net **−0.033756**; at 2.81 close +0.031369 and stop **+0.001369** (report.md:511-518). The gross edge is **carried** (C-6, 0.070 USD/share, from the QQQ replication) and **carries no n in this repository**; the cost figures come from the frozen model.
- **Bar + registration date:** Section 1's structural doubt 2, registered 2026-08-29: "**The entire gross edge of the index version measured smaller than a realistic slippage assumption.**" — REGISTRATION.md:190-191.
- **Amendments touching the bar:** Amendment 15 §7 computes the table, 2026-08-29; Amendment 25 §3 later records that per-share quantities do not transfer across price levels (REGISTRATION.md:3798-3804).
- **Corrections applied:** labelled a cross-application at the point of use — "**a cross-application, and labelled as one**" (report.md:509); declared recorded **before any read exists** "so it cannot be discovered later and rationalised" (report.md:526-527).
- **Framing:** report.md:505-527 and :648-653; consistent, and it is the doubt the closure eventually turned on (report.md:1070-1076).
- **Audit flag:** none raised — the draft checked the direction of the cross-application and found the error runs **against** the repository's own conclusion ("found sound" item 13).

---

## 5. Ledger notes for the cross-repository pass

- **One measured scalar carries the closure's sign.** The stop-exit share **0.381818, n = 550**
  fixes the Amendment 21 shift, and therefore whether the pessimistic-cost mean at 1.40 is
  negative. It is reported as a point estimate everywhere it appears in these three documents
  (REGISTRATION.md:3274, :3624, :3298; report.md:729-730), while the neighbouring zero-count
  scalar in the same amendment is reported with a rule-of-three bound (REGISTRATION.md:3312-3314).
  The **final** closure does not depend on it — Amendment 26's measured band puts the shift
  11.27× above the carried one — but Amendment 21's stated finding and the "registered just on
  the wrong side" framing do.
- **Every deciding figure in this repository comes from one 42-session, 200-ticker, post-holdout
  carve-out.** Dispersion 2.029585, trigger rate 0.982143, stop share 0.381818, ambiguous rate
  0.000000, the measured band and the shift 0.467065 all come from the same slice
  (REGISTRATION.md:3265-3268, :3966-3969). The repository names its regime caveat and attaches it
  to every E2 figure; it does not name the selection-tail or survivorship properties of the
  sampling frame.
- **Two closure kinds, one label.** `cost-bound` and `untestable-at-achievable-power` are both
  defined in HYPOTHESES.md:36-39, and REGISTRATION.md:3468-3474 names the second for this exact
  ground on 2026-08-29, one day before the closure recorded the first. Any cross-repository tally
  of closure kinds should carry that.
- **Figures this repository imports and relies on, none measured here:** the QQQ replication's
  gross edge **0.070 USD/share** and its **0.022** break-even (C-6), which carry no n here and
  are load-bearing for structural doubt 2, the ten-candidate cull, and the "uncomfortable number";
  Concretum's **226,000 to 726,000 USD** fourfold-vendor spread (C-13), which is the sole
  justification for bar integrity being a first-class verdict; McLean and Pontiff's **58 percent
  post-publication decay, 97 predictors, 80 studies** (C-12), which is the sole justification for
  the registered 1.40 assumption that every power figure rests on. Each is labelled **carried**
  where used (REGISTRATION.md:869-891).
- **Dates and commits.** The document stamps 2026-08-30 on Amendments 24–28 are consistent with
  the commit clock in UTC *(from the draft's git reads: `5899e1b` is 2026-08-29T20:41:12-07:00 =
  2026-08-30T03:41Z)*. Amendments 26 and 27 entered history in **one** commit, which bears on
  Amendment 26's own account of its numbering (DRAFT-p1-registration-6), not on any figure in
  this ledger.

---

## Recovery note

This ledger was written on **2026-09-12** by a follow-up recovery agent, from the draft findings
file `findings/agentB/_drafts/ORBExperiment/p1-registration.md` and from the anchored snapshot at
`/home/kiros-li/.cache/program-audit/scratchpad/snap/ORBExperiment/`, after the original Agent B
reader for this part died before writing it. **The draft was not modified.** **No live-repository
access was used** — every quote and line number above was read from the snapshot, and the handful
of commit facts reused are attributed to the draft's own read-only git reads and marked as such.
**No other file was written**; the scratch directory
`/home/kiros-li/.cache/program-audit/scratchpad/work/agentB-ORB-p1-ledger/` was created and left
empty.
