# PMExperiment — Agent A draft findings, part p2-progress

**Reader assignment:** `progress.md`, `docs/ACCESS.md`, `docs/BAND.md`,
`docs/LICENCES.md`, `pmexperiment/`, `data/`. All four primary documents were read
line by line in full (progress.md 1,651 lines; ACCESS.md 333; BAND.md 341;
LICENCES.md 846) plus all five package modules; `REGISTRATION.md`,
`HYPOTHESES.md`, `DECISIONS.md`, `README.md`, `report.md` and `tests/` were read
or grepped for context and are another reader's primary set.

**Repository / SHA:** PMExperiment / `03d16e71dbf25a86c529884662d02136f8e82334`
(main, 2026-09-02, closed project). Snapshot read at
`SNAP/PMExperiment/`; live repo touched read-only once (see the access log).

**Standing caveat.** This repository closed on 2026-09-02 and the anchored SHA is
its last commit; the live repo carries an untracked `_CLOSED_DO_NOT_RUN_HERE`
marker (read 2026-09-04T00:24Z, unanchored) saying no further session may run
there. So *later commits invalidating a finding* is very unlikely for every
finding below, and each says so.

**Direction A framing, stated honestly up front.** This repository is unusually
self-critical: it convicts its own Stage A finding, retracts its own Amendment 1,
overturns its own Dune verdict, and publishes a "what this stage did not read"
table. Several of the items below are limitations the authors themselves wrote
down. Where that is so, the finding is labelled READ, capped at S3, and says
plainly where the disclosure is. What is being challenged in those cases is not
the discovery of the limitation but the fact that **the closure label was never
revisited after the limitation was recorded, and in three cases the limitation
was then written out of the terminal reopening set.**

---

### DRAFT-p2-progress-1
- **Repository / SHA:** PMExperiment / 03d16e71dbf25a86c529884662d02136f8e82334
- **Hypothesis or artifact:** H1 / the Polymarket access closure (Stage C
  PENDING_ACCESS) and the terminal reopening conditions
- **Direction:** A
- **Class:** OVER_CLOSED
- **Severity:** S2
- **Label:** READ
- **Claim challenged (verbatim quote):** "Only these, and each is an operator decision rather than a measurement:" — PMExperiment/docs/LICENCES.md:773 (the list that follows runs to :787 and contains three items: written authorization, a numbered amendment on element (2), a paid third-party tier). The same exhaustiveness is asserted at closure: "**The reopening conditions, stated precisely and exhaustively.**" — PMExperiment/REGISTRATION.md:1082.
- **Evidence:**
  - The repository registered **three** Polymarket reopening routes on 2026-08-30,
    not one: "prior written consent from Adventure One QSS, Inc.; or enrolment in
    the builder program the Terms name; **or a Polygon read performed through
    infrastructure that is not a Polymarket Interface, under a legal analysis this
    repository has not done.** The third is recorded as an open question, **not**
    as a workaround adopted now." — PMExperiment/REGISTRATION.md:1001-1005.
  - The same route is carried in the hypothesis register on the same date: "— for
    Polymarket only, and unanswered — a Polygon read through infrastructure that
    is not a Polymarket Interface" — PMExperiment/HYPOTHESES.md:199-203.
  - My own primary document then **strengthens** that route rather than closing
    it: "The on-chain path is narrower than the licence read claimed. … The
    bullet is scoped to 'the Site, any other Interface, or Features', and **a
    public Polygon ledger is none of the three on its face**. Amendment 6 already
    records the Polygon question as a live reopening path 'under a legal analysis
    this repository has not performed', and that remains its status — neither
    closed here nor opened here." — PMExperiment/docs/LICENCES.md:320-326; the
    same finding in the stage log at PMExperiment/progress.md:1089-1092 ("Amendment
    6's Polygon question stays **open**, neither closed nor opened here").
  - The terminal reopening set omits it. Amendment 8's three conditions
    (PMExperiment/REGISTRATION.md:1085-1098) are an entity applying for Kalshi
    Internal Use, a Kalshi academic tier, and a licensed dataset. Amendment 9 adds
    a fourth — "a Polymarket data licence or written authorization"
    (PMExperiment/REGISTRATION.md:1163-1167) — which is Amendment 6's route (a),
    not route (c). Route (b), builder-program enrolment, is separately answered on
    the merits at PMExperiment/docs/LICENCES.md:215-225 ("Route orders through
    Polymarket and demonstrate consistent usage" — closed to a repository that
    will never trade). **Route (c) is answered nowhere and appears in no terminal
    list.**
  - The omission propagates to every closing summary a cold reader would meet:
    PMExperiment/README.md:151-166 lists three; PMExperiment/HYPOTHESES.md:305-321
    lists three, and the amendment at :352-358 adds the same fourth as Amendment 9.
  - Cost of the omitted route: it is explicitly **not** a data request. It is "a
    legal analysis this repository has not performed"
    (PMExperiment/REGISTRATION.md:1004) — document work of the same class Stage D
    ran for 111 minutes (PMExperiment/progress.md:942), inside a stage that spent
    zero dollars and sent zero market-data requests.
- **Recomputation (if any):** none — this is a document-to-document comparison, not
  arithmetic.
- **What would resolve it:** either (a) a numbered amendment recording the Polygon
  route as closed, with the legal analysis Amendment 6 says was never performed, or
  (b) restoring it to the exhaustive reopening list as condition 5 with its status
  ("open, requires a legal analysis not performed"). Either is a one-paragraph
  document change requiring no venue, no request and no dollar.
- **Confidence:** HIGH — the route is registered verbatim at REGISTRATION.md:1001-1005,
  strengthened at LICENCES.md:320-326, and absent from every terminal list; all five
  documents are in the anchored snapshot.
- **Invalidated by later commits?:** no — 03d16e71 is the repository's last commit
  and the live tree is clean at that SHA (`git -C … status --porcelain` empty,
  2026-09-04T00:24Z), with a marker file forbidding further sessions.
- **Disclosed by authors?:** no — the *openness* of the Polygon question is
  disclosed (LICENCES.md:324-326, progress.md:1089-1092, REGISTRATION.md:1001-1005),
  but nowhere does any document note that it was dropped from the reopening set that
  Amendment 8 calls exhaustive, and no document explains why.

---

### DRAFT-p2-progress-2
- **Repository / SHA:** PMExperiment / 03d16e71dbf25a86c529884662d02136f8e82334
- **Hypothesis or artifact:** Stage A / the Kalshi access gate, condition 5 —
  "the API Developer Agreement is unreadable by automated means"
- **Direction:** A
- **Class:** OVER_CLOSED
- **Severity:** S3
- **Label:** READ
- **Claim challenged (verbatim quote):** "**API Developer Agreement** — `https://kalshi.com/developer-agreement`, **unreadable by automated means on 2026-08-29**: curl and server-side fetch both received HTTP 429 with a Vercel bot-challenge page; a headless-browser render timed out at the same checkpoint." — PMExperiment/docs/ACCESS.md:44-47
- **Evidence:**
  - That unreadability is load-bearing in the closure record, not incidental. It is
    a named ground of the Stage A verdict sentence — "the governing API Developer
    Agreement is unreadable by automated means" (PMExperiment/progress.md:22-23) —
    of the access table row (PMExperiment/progress.md:46), of the fired gate row
    ("condition 5 … the API Developer Agreement is unreadable by automated means",
    PMExperiment/REGISTRATION.md:382), and of the register line
    (PMExperiment/HYPOTHESES.md:173).
  - **One day later, in this same repository, the identical blocker class was
    dissolved by one header.** "Bare `curl` returns 403; the same `curl` with
    nothing added but a browser `User-Agent` returns **HTTP 200**. The in-force
    instruments were one header away." — PMExperiment/docs/LICENCES.md:522-524
    (Stage D, 2026-08-30; the same finding at PMExperiment/progress.md:1054-1056).
  - The repository generalised that discovery into a rule — "**PROHIBITED on an
    unread instrument is a synthesized value** … **ADR-012 has no
    direction-of-travel exemption**" (PMExperiment/docs/LICENCES.md:534-538) and
    "a venue may not be held to a **looser** reading than another because its
    verdict would be more convenient — and **the rule runs both ways**"
    (PMExperiment/README.md:52-54) — and then applied it to Dune only.
  - A grep of the whole snapshot finds `User-Agent` in exactly five places, all of
    them the Dune correction (README.md:58, DECISIONS.md:528, report.md:271,
    progress.md:1055, docs/LICENCES.md:523). **The method was never turned back on
    the Kalshi 429**, and the Kalshi surface is itself listed as unread: "**Kalshi's
    non-PDF surface** — main Terms of Use, help centre, API documentation licensing
    | one 3-page Data Terms PDF was the whole of the Kalshi reading in this stage"
    — PMExperiment/docs/LICENCES.md:679.
  - The same unretried blocker also sits under `kalshi.com/robots.txt`: "HTTP 429
    bot-challenge page in 0.071 s (the Website refuses unauthenticated automated
    readers before robots.txt is even served)" —
    PMExperiment/docs/ACCESS.md:56-59 — so a second recorded input to standing
    rule 12 rests on a challenge that was never re-probed.
- **Recomputation (if any):** none. No request was sent by this audit; re-probing
  a third-party host is outside the audit's read-only scope.
- **What would resolve it:** one single-shot fetch of
  `https://kalshi.com/developer-agreement` with a browser `User-Agent`, recorded in
  the ADR-012 shape (clause, effective date, fetch date). Either it returns the
  instrument — in which case a leg of the Stage A verdict must be rewritten from
  "unreadable" to whatever it says — or it returns 429 again, in which case the
  blocker is confirmed measured rather than assumed. The verdict itself would very
  likely survive either way, because the Data Terms of Use prohibition
  (PMExperiment/docs/ACCESS.md:26-42) is independent of it.
- **Confidence:** MEDIUM — the asymmetry of treatment is documented beyond doubt,
  but a Vercel 429 bot challenge is not the same mechanism as the Cloudflare 403 the
  header defeated at Dune, so the blocker may well be genuine; what is certain is
  that it was never re-measured after the method existed.
- **Invalidated by later commits?:** no — 03d16e71 is the final commit; nothing in
  the repository after 2026-08-30 re-probes any Kalshi host.
- **Disclosed by authors?:** partially (PMExperiment/docs/LICENCES.md:679 records
  Kalshi's non-PDF surface as unread) — but no document connects the
  browser-`User-Agent` discovery of 2026-08-30 to the Kalshi 429 of 2026-08-29, and
  the "unreadable" ground is repeated unqualified in the closure record.

---

### DRAFT-p2-progress-3
- **Repository / SHA:** PMExperiment / 03d16e71dbf25a86c529884662d02136f8e82334
- **Hypothesis or artifact:** Stage D candidate 2 — published academic datasets,
  closed UNMEASURED on ADR-012 element (2)
- **Direction:** A
- **Class:** OVER_CLOSED
- **Severity:** S3
- **Label:** READ
- **Claim challenged (verbatim quote):** "**Element (2) fails.** The dataset card prints no effective, last-updated or revision label; its only years are data-coverage bounds and a BibTeX citation year, neither of which may be promoted." — PMExperiment/docs/LICENCES.md:398-400
- **Evidence:**
  - The deciding element was never sought in the document class that carries it by
    construction, and the repository says so itself: "**Versioned repository
    deposits — Zenodo, Dataverse, OSF, figshare** | **the sharpest gap.** A DOI
    landing page prints a licence, a publication date and a version *by
    construction* — the one document class that routinely satisfies all three
    ADR-012 elements. Candidate 2 reached UNMEASURED on element (2) **without
    fetching a single deposit landing page**, recording only a search-result
    absence." — PMExperiment/docs/LICENCES.md:674.
  - A second, named, unfetched document bearing on the same element: "the **CC BY
    4.0 errata page**, named in the legal code's own footer | bears directly on
    element (2), the element candidate 2 fails" —
    PMExperiment/docs/LICENCES.md:675; and at :405-411, "**There is one, it is
    named on the face of the legal code, and it was not read** — the footer points
    to an errata page carrying 'the date of change'."
  - Such a fetch is inside the stage's own permitted scope and costs nothing:
    "Licence, terms, acceptable-use, contact, pricing and dataset-documentation
    pages **only**" — PMExperiment/docs/LICENCES.md:39-40 — a class of which
    candidate 1 alone fetched **11** (PMExperiment/docs/LICENCES.md:125-131). The
    dataset's own paper is a versioned deposit with a dated landing page:
    "`TimeSeventeen/Polymarket-v1` (Boka Qin, Rui Yang; paper arXiv:2606.04217)"
    — PMExperiment/docs/LICENCES.md:348.
  - The verdict was then **frozen at closure without re-asking**: "**And one thing
    this addendum does not do: it does not reopen Stage D's other two verdicts.**
    Polymarket and the three licence candidates are where Stage D left them. One
    route answered; the rest were not re-asked." —
    PMExperiment/docs/LICENCES.md:844-846. That freeze was written on 2026-09-02,
    i.e. *after* the same document's completeness caveat had already been proven
    load-bearing once — "**A route surfaced two days later.** The caveat cost one
    paragraph and was load-bearing inside a week" (PMExperiment/progress.md:1445-1447).
  - The register carries the candidate forward as the surviving reopening condition
    3, "a licensed dataset whose licensor held authority to license"
    (PMExperiment/REGISTRATION.md:1095-1098), i.e. as an operator decision — even
    though the element that actually failed (a printed date) was never sought where
    it lives.
- **Recomputation (if any):** none — this is a document-availability argument.
- **What would resolve it:** fetching one DOI landing page for the corpus (Zenodo,
  Dataverse, OSF, figshare, or the arXiv:2606.04217 record) and the CC BY 4.0
  errata page, then re-firing `pmexperiment.admissibility` on the claim. The
  repository itself states this would still leave element (1), chain of title and
  the AI-clause search open (PMExperiment/docs/LICENCES.md:499-503) — so the
  resolution here is a *label*, not necessarily a PERMITTED.
- **Confidence:** HIGH — the gap and its sharpness are stated in the repository's
  own words at LICENCES.md:674, and the freeze at :844-846 is equally explicit.
- **Invalidated by later commits?:** no — 03d16e71 is the last commit and the
  addendum at LICENCES.md:793-846 is the final word on this candidate.
- **Disclosed by authors?:** yes (PMExperiment/docs/LICENCES.md:674, :675,
  :405-411; PMExperiment/progress.md:1097-1110; PMExperiment/HYPOTHESES.md:233-238)
  — the authors disclose the gap, name it "the sharpest", and name the direction of
  bias. What is not disclosed is that the closure was nevertheless frozen at Stage E
  without acting on a one-document, zero-cost cure to the very element that decided
  it.

---

### DRAFT-p2-progress-4
- **Repository / SHA:** PMExperiment / 03d16e71dbf25a86c529884662d02136f8e82334
- **Hypothesis or artifact:** the registered effect band, Section 3 — the CPI
  companion study registered as evidence against the effect inside the
  Canadian-permitted categories
- **Direction:** A
- **Class:** STATISTICAL
- **Severity:** S3
- **Label:** DERIVED
- **Claim challenged (verbatim quote):** "The companion CPI study (*Zero-Price Contracts and the Favorite-Longshot Bias in CPI Prediction Markets*, SSRN 7087538, 95 contracts over 12 months) finds **no** classic favourite-longshot bias — registered here as evidence that the effect inside the permitted categories is heterogeneous and may be absent in some series." — PMExperiment/docs/BAND.md:50-55 (Section 3 quoted verbatim into BAND.md; carried into the Pass-2 input table as an "against" row at PMExperiment/docs/BAND.md:285 and into the stage log at PMExperiment/progress.md:468-470)
- **Evidence:**
  - The n travels with the figure (standing rule 13) but **no minimum detectable
    effect is ever computed for it**, in a repository whose founding premise is
    that an underpowered null is not a null: "NPDExperiment closed at
    *unresolved-at-achievable-power*: realized minimum detectable contrast
    **0.0512** against an effect band of **0.01 to 0.05**" —
    PMExperiment/CLAUDE.md:54-58. Grepping the snapshot, the n = 95 figure appears at
    REGISTRATION.md:240, docs/BAND.md:52, docs/BAND.md:285, progress.md:468-469
    and DECISIONS.md:270-271 (hard-wrapped across the line break), and **no power
    figure accompanies any occurrence**.
  - The repository supplies every input needed to compute it: the MDE formula
    `MDE = z · sqrt(v̄ / n_T)` with z = 2.0 (PMExperiment/REGISTRATION.md:99-101 and
    PMExperiment/pmexperiment/power.py:37-45), the tail-cell planning dispersion
    "prices near 5c or 95c give p(1−p) ≈ 0.0475"
    (PMExperiment/REGISTRATION.md:122-123), and Krause's implied mean bucket price
    of 0.117 for a comparable "below 30c" bucket
    (PMExperiment/docs/BAND.md:132; PMExperiment/DECISIONS.md:225).
  - The verdict map this repository would apply to its own gate at that MDE is
    **DEGRADED at best, never GO** (PMExperiment/REGISTRATION.md:108-112) — i.e.
    the CPI study could not have detected an effect anywhere in the lower half of
    the very band it is registered against.
  - Direction of the error is against H1: the CPI null is one of only two "against"
    inputs in the Canadian-filter pass (PMExperiment/docs/BAND.md:285) and part of
    "the Canadian doubt, registered before any measurement and never tested"
    (PMExperiment/README.md:194-199).
- **Recomputation (if any):** inputs — n = 95 (docs/BAND.md:52); z = 2.0
  (REGISTRATION.md:99-101, registry.py:9); v̄ = 0.0475 (REGISTRATION.md:122-123),
  v̄ = 0.117 × 0.883 = 0.10331 (docs/BAND.md:132), v̄ = 0.04 × 0.96 = 0.0384
  (the study's own comparator settle rate, docs/BAND.md:51). Method: the
  repository's own `pmexperiment.power.minimum_detectable_effect`, plus a Wilson
  interval for illustration. Results
  (`scratchpad/work/agentA-PMExperiment-p2/recompute.py`, run 2026-09-04):
  - MDE(n = 95, v̄ = 0.0475) = **0.0447** = 4.47 points → DEGRADED; n needed for
    GO (MDE ≤ 0.02) = **475**.
  - MDE(n = 95, v̄ = 0.10331) = **0.0660** = 6.60 points → DEGRADED, reaching only
    the top **23.4 %** of the registered 2–8 point band; n needed for GO = **1,033**.
  - MDE(n = 95, v̄ = 0.0384) = **0.0402** = 4.02 points → DEGRADED.
  - At a conventional 80 % power (two-sided α = 0.05) the same n = 95 gives
    **6.26** points (v̄ = 0.0475) and **9.24** points (v̄ = 0.10331) — the second
    lying entirely **above** the registered band top of 8.00.
  - Illustrative interval: 4 of 95 settling YES (Krause's 4.0 % rate, the figure
    the registration prints beside it at docs/BAND.md:51) gives a Wilson 95 %
    interval of **[0.0165, 0.1033]**, **8.68 points wide — wider than the whole
    6-point registered band**. n = 95 is contracts *in total over 12 months*, so
    the longshot-bucket n is at most 95 and the true interval is at least this
    wide.
- **What would resolve it:** one sentence in Section 3 or docs/BAND.md recording
  the CPI study's MDE beside its n, and restating the registered inference from
  "the effect … may be absent in some series" to "that series is uninformative
  below roughly 4–6.6 points". Zero-cost, document-only, and exactly the arithmetic
  Section 0.4 already performs for this repository's own cells.
- **Confidence:** HIGH for the arithmetic (it uses the repository's own formula,
  constants and cited figures); MEDIUM for its weight, because the dispersion of
  the CPI study's own price bucket is not published in this repository and three
  plausible values were carried rather than one.
- **Invalidated by later commits?:** no — Section 3 is registered and
  Amendment 2 fixes the band as computed once (PMExperiment/HYPOTHESES.md:153-157);
  nothing after 2026-08-29 alters these inputs.
- **Disclosed by authors?:** no — the n is disclosed everywhere the figure appears
  (standing rule 13 working as designed), and DECISIONS.md:271-272 notes that "The
  band's bottom travels with a large n; its top travels with none.", but no document
  computes or states what n = 95 could detect.

---

### DRAFT-p2-progress-5
- **Repository / SHA:** PMExperiment / 03d16e71dbf25a86c529884662d02136f8e82334
- **Hypothesis or artifact:** Stage B BAND-OPEN — the surviving region fixed at
  91–99c, and the power-gate scope locked to it in Amendment 8
- **Direction:** A
- **Class:** OVER_CLOSED
- **Severity:** S3
- **Label:** READ
- **Claim challenged (verbatim quote):** "| the eight non-tail deciles | **no effect magnitude is registered outside the tail cell.** Supplying one would violate standing rule 5. |" — PMExperiment/docs/BAND.md:325
- **Evidence:**
  - The same document, three rows earlier in its own results table, places a
    magnitude outside the tail cell and marks it **clearing on every treatment**:
    "| Krause, sub-30c/4.0 % → NO at 88.3c | 0.883 | 0.077 | 0.0565 **clears** |
    0.0765 **clears** | 0.0300 **clears** |" — PMExperiment/docs/BAND.md:253; and
    in the bucket table, "| 81–90 | 0.855 | 0.0556 | … | not registered — though
    Krause's exploitable complement lands here at 0.883 |" —
    PMExperiment/docs/BAND.md:209.
  - **The two magnitudes inside the fired region both fail**: "| Bürgi, 5c/3 % → NO
    at 95c | 0.950 | 0.020 | 0.0585 **fail** … | Bürgi, 95c/98 % → YES at 95c |
    0.950 | 0.030 | 0.0585 **fail** …" — PMExperiment/docs/BAND.md:251-252. So the
    gate's region contains no cited magnitude that clears, and the excluded
    neighbouring decile contains the only one that does.
  - **The verdict's own discrimination relies on the excluded bucket.** BAND-OPEN
    rather than BAND-NARROW is chosen because "its category clause is contradicted
    by Krause's permitted-category attribution" —
    PMExperiment/docs/BAND.md:307-309 and PMExperiment/progress.md:478-481. Krause
    is the 88.3c figure. The magnitude is in scope when it defeats BAND-NARROW and
    out of scope when it would widen the region the power gate fires over.
  - The exclusion was then made permanent for any future work: "A reopened
    measurement starts at the power gate over 91–99c held to resolution and no
    other region, exactly where Stage C left it." —
    PMExperiment/REGISTRATION.md:1110-1111; and the Stage C prompt had already
    frozen it, "Do not widen the region to improve the count"
    (PMExperiment/progress.md:562-563).
  - The region was fixed **before** Stage B's own direction correction moved every
    exploitable price to 0.883–0.95 ("Restated that way every registered magnitude
    sits at a **high** entry price — 0.883 to 0.95", PMExperiment/progress.md:412-414).
    That correction produced *two* coupled consequences in the same task; one was
    registered as a numbered amendment before use (the FX turnover, Amendment 4,
    PMExperiment/docs/BAND.md:165) and the other was recorded as an unrepaired
    "scope mismatch" (PMExperiment/DECISIONS.md:259-264).
- **Recomputation (if any):** inputs — fee $0.02/side, half-spread $0.01, FX
  1.5 % × 2 directions (PMExperiment/pmexperiment/registry.py:53-57), turnover
  k = 1 (registry.py:66), band 0.02–0.08 (registry.py:10-11). Method:
  `R(p) = fee·sides + 0.01 + 0.03·p/k`, i.e. `pmexperiment.band.required_underpricing`
  re-implemented. Results (`scratchpad/work/agentA-PMExperiment-p2/recompute.py`),
  all reproducing docs/BAND.md exactly:
  - p = 0.883: R_H = **0.0565**, Krause's 0.077 clears by **+0.0205** (2.05 points);
    R_X = 0.0765, clears by +0.0005.
  - p = 0.950: R_H = **0.0585**; Bürgi's 0.030 fails by −0.0285 and 0.020 by −0.0385.
  - Band-top survival margin, held route: **0.0244 at the 81–90 decile** versus
    **0.0215 at the 91–99 decile** — the excluded bucket has the *larger* margin as
    well as the only clearing citation.
- **What would resolve it:** a numbered amendment recording, before any reopened
  measurement, either (a) that the power gate fires over 81–99c because the
  direction correction of ADR-009 moved the exploitable prices across the
  registered cell edge, or (b) that it fires over 91–99c only and that the region
  therefore contains no cited magnitude that clears the registered cost floor —
  which is a materially different sentence from the one Amendment 8 now carries.
- **Confidence:** MEDIUM — the arithmetic is certain and reproduces the
  repository's own table, but the exclusion is *registration-compliant*: Section 3
  registers the band in the tail cell (1–10c and 91–99c) before any measurement,
  and DECISIONS.md:261-263 gives a principled reason for not moving it after the
  fact ("narrowing a registered band after seeing the arithmetic is precisely what
  Section 3 forbids").
- **Invalidated by later commits?:** no — Amendment 2 fixes the band as computed
  once and forbids adding a bucket afterwards
  (PMExperiment/REGISTRATION.md:1107-1109); 03d16e71 is the last commit.
- **Disclosed by authors?:** yes, for the scope mismatch —
  PMExperiment/DECISIONS.md:259-264 ("**A scope mismatch.** … Krause's exploitable
  complement at 88.3c lands in the 81–90 decile, outside that cell"),
  PMExperiment/docs/BAND.md:330-334, PMExperiment/HYPOTHESES.md:144. Not disclosed:
  that the same excluded magnitude is what defeats BAND-NARROW, and that the
  exclusion is carried into Amendment 8 as the permanent scope of any reopened
  measurement.

---

### DRAFT-p2-progress-6
- **Repository / SHA:** PMExperiment / 03d16e71dbf25a86c529884662d02136f8e82334
- **Hypothesis or artifact:** Stage A access gate, condition 4 — price history
  retrievable to 30 days before close (the S30 snapshot's feasibility)
- **Direction:** A
- **Class:** OVER_CLOSED
- **Severity:** S3
- **Label:** READ
- **Claim challenged (verbatim quote):** "| 4 | price history retrievable to 30 days before close | **NOT DEMONSTRATED — fails closed** | … the one ≥ 30-day-old settled market tested (`NASDAQ100-24OCT25-T21499.99`, closed 2024-10-25) returned HTTP 200 and **0 daily candles** over T−40d..T; ambiguous, counted as ambiguous, attributed to nothing |" — PMExperiment/docs/ACCESS.md:21
- **Evidence:**
  - **n = 1 market, one interval.** The whole evidence for the failing side of
    condition 4 is a single ticker at a single `daily` granularity; the request log
    records "3 candlestick reads (2 returned zero candles, 1 returned one candle)"
    — PMExperiment/docs/ACCESS.md:84-85 — inside a total probe budget of 13
    requests (PMExperiment/progress.md:59). No second market, no second series, no
    hourly or minute interval, and no second date range was tried.
  - **The condition's own precondition is unrecorded.** The registered condition
    reads "Price history is retrievable back to 30 days before close **for markets
    whose lifetime reaches that far**, so S30 is computable" —
    PMExperiment/REGISTRATION.md:151-152. The tested market's open time or lifetime
    appears nowhere: grepping the snapshot, `NASDAQ100` occurs exactly once, at
    docs/ACCESS.md:21, and no other document records an open date for it. "≥ 30-day-old"
    in that row means *closed ≥ 30 days before the probe*, which is a different
    property from *open for ≥ 30 days*. A zero-candle response over T−40d..T is the
    expected result for a market that did not exist 40 days before its close, in
    which case the probe cannot bear on the condition either way.
  - The row's own label is internally split: the cell says "ambiguous, counted as
    ambiguous, attributed to nothing" (docs/ACCESS.md:21) and
    PMExperiment/progress.md:44 repeats "ambiguous, counted ambiguous" — while the
    verdict paragraph converts it into a failing condition, "conditions 3 and 4 fail
    closed as unmeasured or undemonstrated" (PMExperiment/docs/ACCESS.md:9-12), and
    the fired gate row states it as a finding: "NOT DEMONSTRATED, fails closed
    (0 daily candles on the one ≥ 30-day-old market tested; recent-market candles
    work)" (PMExperiment/REGISTRATION.md:381).
  - Consequence is bounded and must be said: condition 5 fails independently on the
    recorded terms (PMExperiment/docs/ACCESS.md:22, :26-42), so PENDING_ACCESS
    stands whatever condition 4 does. What changes is the *number of independent
    grounds* the closure claims, and whether S30 — the snapshot the entire Canadian
    question rests on (PMExperiment/REGISTRATION.md:63-67) — is on record as
    infeasible.
- **Recomputation (if any):** none — there is no arithmetic to redo; the point is
  that the deciding sample is n = 1 and its qualifying property is unrecorded.
- **What would resolve it:** recording the tested market's open time beside its
  close time, and either (a) a second probe on a market whose lifetime demonstrably
  exceeds 30 days, or (b) restating condition 4 as **NOT MEASURED** rather than
  **NOT DEMONSTRATED**, since a probe whose precondition is unverified measures
  nothing. Both cost one line of document or one request inside the existing budget.
- **Confidence:** MEDIUM — that the record is silent on the tested market's
  lifetime is certain and checkable by grep; that the market in fact had a short
  lifetime is an inference from the ticker's form (a dated strike on an index-close
  series) and is *not* established by anything in the repository.
- **Invalidated by later commits?:** no — Stage A's probe budget was spent on
  2026-08-29 and no later stage sent a Kalshi request
  (PMExperiment/docs/ACCESS.md:231-234).
- **Disclosed by authors?:** partially — the ambiguity and the n = 1 are stated in
  the same cell (docs/ACCESS.md:21) and repeated at progress.md:44. Not disclosed:
  that the registered condition is conditional on the tested market's lifetime and
  that this property was never recorded.

---

### DRAFT-p2-progress-7
- **Repository / SHA:** PMExperiment / 03d16e71dbf25a86c529884662d02136f8e82334
- **Hypothesis or artifact:** the terminal data-availability closure — "the
  calibration question is unmeasurable at this house's standard"
- **Direction:** A
- **Class:** OVER_CLOSED
- **Severity:** S3
- **Label:** READ
- **Claim challenged (verbatim quote):** "**The consequence, stated plainly: the calibration question is unmeasurable at this house's standard until an authorization is granted.** Not unmeasurable in principle, and not unmeasured because the arithmetic came out badly … Unmeasurable because every route to the records either prohibits the reading or cannot show it is permitted" — PMExperiment/docs/LICENCES.md:706-712
- **Evidence:**
  - A whole class of route to the same records was named and never asked:
    "| **regulatory disclosure routes** | Kalshi is a CFTC-designated contract
    market with public reporting obligations; whether settlement history is
    obtainable from a **regulator** rather than a venue was never asked |" —
    PMExperiment/docs/LICENCES.md:682 (same item at PMExperiment/progress.md:1104-1105).
  - The bar the repository uses to stop searching does not, on its own words, reach
    this route: "**No fourth venue is proposed.** … proposing a new venue after
    three routes close is how a measurement-only project turns into a search for a
    venue that will say yes" — PMExperiment/docs/LICENCES.md:759-763, repeated at
    PMExperiment/REGISTRATION.md:1113-1116. A regulator is not a venue and holds no
    terms of use over a market participant's reading; the objection stated is about
    venues.
  - The route bears on the *deciding* element, permission: a regulator's public
    disclosure file is published under a statutory obligation, i.e. exactly the
    document class most likely to satisfy ADR-012 with a printed effective date —
    the element on which candidate 2 failed (PMExperiment/docs/LICENCES.md:398-403).
  - It appears in none of the four terminal reopening conditions
    (PMExperiment/REGISTRATION.md:1085-1098 and :1163-1167;
    PMExperiment/HYPOTHESES.md:305-321 and :352-358;
    PMExperiment/README.md:151-166), and Stage E did not re-ask it: "the rest were
    not re-asked" (PMExperiment/docs/LICENCES.md:846).
  - The repository's own record shows that asking outside the read set is what
    produced its only new information in five stages: the Kalshi institutional
    desk reply of 2026-09-01 came from a route Stage D had not read
    (PMExperiment/docs/ACCESS.md:236-240, PMExperiment/progress.md:1442-1449).
- **Recomputation (if any):** none.
- **What would resolve it:** one document fetch of a CFTC / DCM public reporting
  page for Kalshi, recorded in the ADR-012 shape, and either a PERMITTED /
  PROHIBITED / UNMEASURED verdict on it or an explicit register line saying the
  route is out of scope and why. Zero dollars, no account, and inside the licence-
  document scope Stage D already used.
- **Confidence:** MEDIUM — the route's existence and its non-asking are recorded
  verbatim in the repository; whether a regulator actually publishes contract-level
  settlement history at the depth the gate needs is unknown to this audit and is
  not asserted.
- **Invalidated by later commits?:** no — 03d16e71 is the last commit; the closure
  addendum explicitly declines to re-ask.
- **Disclosed by authors?:** yes (PMExperiment/docs/LICENCES.md:682 and
  PMExperiment/progress.md:1104-1105 list it among what was not read, and
  :684-688 names the direction of bias). Not disclosed: that the "no fourth venue"
  bar, which is what stops the search, is stated about **venues** and does not on
  its face cover a regulator.

---

### DRAFT-p2-progress-8
- **Repository / SHA:** PMExperiment / 03d16e71dbf25a86c529884662d02136f8e82334
- **Hypothesis or artifact:** Section 14 reproducibility, applied to the Stage A
  access-gate figures
- **Direction:** A
- **Class:** PROVENANCE
- **Severity:** S4
- **Label:** DERIVED
- **Claim challenged (verbatim quote):** "The gate verdict must be regenerable from: the stored raw enumeration and candlestick responses under `data/raw/`, the registered constants in `pmexperiment.registry`, and the registered seed 20260829. A rerun may depend on no other state." — PMExperiment/REGISTRATION.md:359-361 (primary evidence partly outside my assignment; the countervailing record is in my documents)
- **Evidence:**
  - The probe artefacts were not kept: "the raw probe responses were **not retained
    beyond this report** and the two tickers named above" —
    PMExperiment/docs/ACCESS.md:88-89.
  - `data/` is empty in the snapshot (`data/.gitkeep`, 0 bytes, the only entry) and
    empty in the live tree: `data/` contains only `.gitkeep` (0 bytes, mtime
    2026-08-29), no `data/raw/` directory exists, and `git status --porcelain
    --ignored` lists no data artefact — read from
    `/home/kiros-li/Documents/GitHub/PMExperiment` at **2026-09-04T00:24Z**
    (unanchored; may have changed after the anchor, though the tree is clean at
    03d16e71 and carries a marker forbidding further sessions).
  - The consequence for the closure: the deciding figures of the Stage A gate —
    "earliest retrievable settled close sits between 2024-01-01 (empty page) and
    2024-05-31 (present) … n = 6 bracketing probes" (PMExperiment/docs/ACCESS.md:72),
    the 11-request latency range 99.9–213.8 ms (:71), the 0-daily-candles reading
    (:21) — cannot be re-derived by anyone, including a later operator, from
    anything in the repository. They are re-obtainable only by re-probing a venue
    the repository has closed itself off from.
  - This is the reverse of the failure mode the repository names elsewhere: Stage E
    audited "**32 commits, 189 reachable objects, every blob decompressed**"
    for credentials (PMExperiment/progress.md:1537-1539), so whole-history rigour
    was available and was applied to secrets but not to the gate's own inputs.
- **Recomputation (if any):** none; a directory listing and a `git status` are the
  whole evidence.
- **What would resolve it:** a one-line amendment to Section 14 recording that the
  Stage A probe responses were not retained and that the access-gate figures are
  therefore reproducible only by re-probing — i.e. bringing Section 14 into line
  with docs/ACCESS.md:88-89, rather than leaving a registered reproducibility
  requirement standing unmet.
- **Confidence:** HIGH — the non-retention is stated by the authors and the empty
  `data/` is directly observed in both snapshot and live tree.
- **Invalidated by later commits?:** no — no commit after 2026-08-29 adds a data
  artefact; the live tree at 03d16e71 is clean.
- **Disclosed by authors?:** partially — the non-retention is disclosed at
  PMExperiment/docs/ACCESS.md:88-89. Not disclosed: that this leaves
  REGISTRATION.md Section 14's registered requirement unmet for the only gate that
  ever fired on measured inputs. This is hygiene, not a wrong conclusion, hence S4.

---

## What I checked and found sound

Listed with what I would have expected to find if my thesis held there, and did not.

1. **The zero-measurement claims are true in the artefact record.** "No price
   bucket was built, no dispersion computed, and no statistic relating a price to
   an outcome exists in this repository" (progress.md:681-682, :1370-1372) is
   consistent with `data/` holding only a 0-byte `.gitkeep` in both the snapshot
   and the live tree (read 2026-09-04T00:24Z), with `pmexperiment/` containing no
   I/O, no network call and no outcome field, and with `power.py` never being
   invoked on real inputs anywhere in the package or tests. I expected to find a
   retained probe dump or a stray CSV contradicting "zero enumerated"; there is none.

2. **The band arithmetic reproduces exactly.** Every figure in docs/BAND.md's
   Pass-1 table, the crossing points (p = −0.3333, +1.6667, −1.0000, +1.0000), the
   0.0300 fee+spread floor, the 0.0015 route-X margin, the 0.00195 FX-base
   understatement and the 0.00135 held-route counterpart all reproduce from
   registry.py's constants under `R(p) = fee·sides + 0.01 + 0.03p/k`
   (my recompute.py). C(0.95) = 0.0785 and C(0.05) = 0.0515 match
   REGISTRATION.md:338. No arithmetic error found.

3. **The FX treatment is chosen against H1 and the verdict is invariant to it.**
   k = 1 binds and biases toward BAND-EMPTY (docs/BAND.md:175-179, ADR-010);
   k = 12 and k → ∞ are reported beside it and never substituted. I checked
   `band.fx_cost` and `registry.FX_TURNOVER_REGISTERED = 1.0` and found no path
   by which a favourable k enters a verdict.

4. **The direction correction (ADR-009) is right and is the opposite of
   self-serving.** Restating the published longshot overpricing as its exploitable
   complement moves every magnitude to 0.883–0.95, where the price-proportional FX
   is largest — a correction that made the repository's own case *harder*, not
   easier. I verified `return = gap ÷ price` reproduces −40.0 % at 5c and +3.16 %
   at 95c, and that the return reading of Krause's −0.077 would imply a mean price
   of 0.043 and make the largest cited figure the smallest.

5. **The z = 2.0 gate convention is permissive, not restrictive.** `MDE = 2·sqrt(v̄/n)`
   (power.py:45) is a detection threshold at roughly 50 % power; an 80 %-power MDE
   would be 1.4× larger and the required n 1.96× larger. This makes the gate
   *easier* to pass, so it cuts against my thesis rather than for it, and I record
   it here rather than as a finding.

6. **The Stage-A/Stage-E depth question was handled correctly.** Stage A's phrasing
   "the 2021→Apr 2025 span … is **not reproducible keylessly**"
   (docs/ACCESS.md:73) survived the 2026-09-01 discovery that the archive exists
   behind a licence, and the repository says so without claiming credit it does not
   have (docs/ACCESS.md:317-333). I expected to find a stale blocker here and found
   a correctly scoped one.

7. **The Kalshi reply was not promoted beyond what it is.** It is recorded
   UNMEASURED under the repository's own procedure, with the strongest argument for
   admitting it stated at full strength and refused (docs/ACCESS.md:261-283), and
   the label stays EXISTS-AND-UNTRAVELLED rather than "declined"
   (docs/ACCESS.md:224-229). The three questions that survive the entity
   requirement — fee, publishing rights, AI/ML consent — are recorded absent rather
   than as zero (docs/ACCESS.md:302-315). No over-closure here.

8. **The Dune self-correction is real and complete.** The "unreadable" claim was
   overturned by the repository's own verification, the archived-instrument
   quotation was replaced by the in-force text, and ADR-015 generalises the lesson
   symmetrically (docs/LICENCES.md:512-544). I checked for the same failure
   surviving anywhere else in the licence read and found only the Kalshi 429 case
   raised as DRAFT-p2-progress-2.

9. **The mutation harness faults are recorded, not hidden.** Three separate
   hard-wrap faults (Entry 1, Entry 7.1, Entry 9.1) and one destroyed-work incident
   (progress.md:1216-1230) are written up as faults with their fixes, and Stage E
   reports "zero harness faults" against fourteen mutations
   (progress.md:1529-1535). I looked for a mutation reported green that had not
   mutated and found the repository had already caught every instance itself.

10. **ETA discipline is honest against itself.** Every stage records actuals
    against stated ETAs including the one stage that overran by 5.5×
    (progress.md:947-965), and Entry 11 concludes that flagging an estimate as weak
    "is a guess wearing a warning label" (progress.md:1402-1408). No ETA cell was
    filled retrospectively with a fictional number; Stage C's 2b cell is left
    "never stated, never armed" (progress.md:691).

11. **One inconsistency I judged too weak to raise as a finding, recorded here.**
    "**If an authorization arrived tomorrow the power question would still be
    unanswered**" (progress.md:1560, README.md:190-192) sits beside
    REGISTRATION.md:132-134, which already reasons from the published benchmark's
    two-thirds tail share that "the unrestricted universe reaching 475 tail
    contracts is expected". The unrestricted cell's power is therefore partly
    pre-answered from published figures, and only the permitted-subset cell is
    genuinely open. This cuts against the closure being as complete as stated, but
    it is a Direction-B nuance on a self-critical sentence, the registered gate
    requires measured v̄ and n_T rather than published estimates, and standing rule
    5 forbids synthesizing them — so I do not raise it.

12. **Amendment 9 is not a rationalisation.** I checked whether "a regulatory
    change to trading access is not evidence about data permission"
    (progress.md:1607-1612) was being used to bar a real reopening. It is not: the
    data terms it cites carry no entity-type qualification
    (docs/ACCESS.md:132-136), and the amendment adds a reopening condition rather
    than only removing one.

---

## Live-repo access log

Purpose: (1) git history/provenance, (2) untracked or gitignored working-tree data
under `data/` and `scripts/`. No file was opened for writing; no git command other
than `status`, `rev-parse` and `log` was run.

**BEFORE** — `git -C /home/kiros-li/Documents/GitHub/PMExperiment status --porcelain`
(2026-09-04T00:23Z):

```
```

(empty — clean working tree; `git rev-parse HEAD` = `03d16e71dbf25a86c529884662d02136f8e82334`, identical to the anchored SHA)

**AFTER** — `git -C /home/kiros-li/Documents/GitHub/PMExperiment status --porcelain`
(2026-09-04T00:34Z):

```
```

(empty — unchanged; nothing was modified by this audit)

**Ignored entries observed** (`git status --porcelain --ignored`, 2026-09-04T00:24Z),
recorded because one of them is not tooling dirt:

```
!! .mypy_cache/
!! .pytest_cache/
!! .ruff_cache/
!! .venv/
!! _CLOSED_DO_NOT_RUN_HERE
!! pmexperiment/__pycache__/
!! tests/__pycache__/
```

`_CLOSED_DO_NOT_RUN_HERE` (747 bytes, mtime 2026-09-02 22:38, untracked and
excluded via `.git/info/exclude`) is an operator closure marker reading in part
"THIS REPOSITORY IS CLOSED. DO NOT RUN A CODING SESSION HERE. … Marker written
2026-09-02 after a session was opened here by mistake." It is **not** repository
dirt caused by this audit and it is not tracked at the anchored SHA. Read
2026-09-04T00:24Z; unanchored.

`data/` and `scripts/` each contain exactly one 0-byte `.gitkeep` and nothing else
(read 2026-09-04T00:24Z). No untracked or gitignored data artefact of any kind
exists in this repository.
