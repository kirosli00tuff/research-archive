# REGISTRATION.md — the pre-registration

PMExperiment. A measurement-only calibration-power test on public Kalshi
settlement history, judged separately on the unrestricted universe and on the
Canadian-permitted subset.

**Section 0 registered 2026-08-29, before the first request to the measured
source.** No request had been sent to any Kalshi endpoint when the commit
carrying this section was made. Changing a registered value now requires a
numbered amendment appended to Section 17, carrying its own evidence. Nothing
edits in place.

Every number in this document is **derived, measured, or labelled an
assumption with its direction of bias named**. A section still carrying a
*to be registered* marker is registered in a later task, always before the
measurement it governs.

---

## 0. The gates

Two gates fire in Stage A, and neither reads a first moment relating a price
to an outcome. **The access gate** reads whether the public data is reachable,
deep enough, and permitted. **The power gate** reads a minimum detectable
effect, built from a bucket count and a dispersion and from nothing else.

### 0.1 Why this section exists, quoted from the record

From InsiderExperiment `REGISTRATION.md` Section 0.1, registered 2026-08-25:

> NPDExperiment closed at unresolved-at-achievable-power. Its realized minimum
> detectable contrast came in at 0.0512 against a realistic effect band of
> 0.01 to 0.05, so the design could not have detected an effect anywhere in
> the range the literature reports. That was discovered after 415 days of
> collection and 6.9378 USD of spend, in the same session that read the
> result. Its ADR-007 had registered the risk in advance and the arithmetic
> still landed too late to change anything.

From NPDExperiment `progress.md`, the closure entry of 2026-08-25:

> **The replication is an underpowered unresolved, not a tight null.** The
> realized minimum detectable contrast was 0.0512, above the entire realistic
> effect band of 0.01 to 0.05, so the design could not have detected an effect
> anywhere in the range the literature reports.

InsiderExperiment registered its power gate before spending and fired
**BLOCKED at 49.35 bp**. This repository follows Insider: the gate is
committed before the measurement it judges, so the answer cannot be read
against a threshold its own measurement could see.

### 0.2 What the gate may read, defined before anything is fetched

**The unit.** One settled Kalshi market contributes one observation: its
YES-side price at the registered snapshot, in integer cents 1 to 99.

**The snapshots.** Two, fixed here:

- **S24, the literature benchmark.** The last traded price at or before
  `close_time` minus 24 hours. A market qualifies at S24 if it was open at
  least 24 hours and traded at least once at or before that instant. This
  matches the published Kalshi benchmark (Section 3), which analyzes markets
  open at least 24 hours.
- **S30, the Canadian reality.** The last traded price at or before
  `close_time` minus 30 days. A market qualifies at S30 if it was open at
  least 30 days and traded at least once at or before that instant. S30
  exists because the permitted-subset maturity rule (Section 1) makes any
  later purchase unreachable for the participant this repository models.

**The buckets.** Ten price deciles in cents: 1–10, 11–20, 21–30, 31–40,
41–50, 51–60, 61–70, 71–80, 81–90, 91–99. **The tail cell T** is the union of
1–10 and 91–99. The published benchmark's high band is 90–99c; using 91–99
keeps the deciles even and drops 90c contracts from the tail, which can only
shrink the tail count — the conservative direction.

**The dispersion.** For a cell of n contracts with snapshot prices p_i in
dollars, the null Bernoulli dispersion is v̄, the mean of p_i(1−p_i). It is
computed from prices alone. No outcome enters it.

**The cells.** Four are computed; two carry verdicts:

| cell | universe | snapshot | role |
|---|---|---|---|
| U24 | unrestricted | S24 | **verdict cell** — comparable to the published benchmark |
| P30 | Canadian-permitted | S30 | **verdict cell** — the Canadian question |
| U30 | unrestricted | S30 | attribution — separates the horizon cost from the category cost |
| P24 | Canadian-permitted | S24 | attribution — the same split, from the other side |

**The sampling rule.** The permitted subset is measured exhaustively. The
unrestricted universe may be sampled: if the enumerated qualifying count N
exceeds m = 2,000, a uniform random sample of m markets without replacement
is drawn with seed 20260829, the tail share is estimated from the sample, and
the gate consumes n_T = N times the **Wilson 95% lower bound** of the sampled
tail share — the conservative direction, understating the tail count rather
than overstating it. If N ≤ m the universe is read exhaustively and the bound
collapses to the count itself.

### 0.3 The power gate and the outcome map

The minimum detectable effect for a cell, with z = 2.0 two-sided:

    MDE = z · sqrt(v̄ / n_T)

judged against the registered effect band of Section 3, **0.02 to 0.08**
absolute probability points in the tail cell. Fired separately for U24 and
P30. Boundaries are inclusive at the lower edge, following Insider: an MDE of
exactly 0.0200 is GO, exactly 0.0800 is DEGRADED.

| verdict | condition on the cell | consequence |
|---|---|---|
| **GO** | MDE ≤ 0.02 | the design resolves the entire published band; Stage B is authorized for that universe against the registered target |
| **DEGRADED** | 0.02 < MDE ≤ 0.08 | the design resolves the top of the band but not the bottom; Stage B proceeds only with the achieved power stated beside the registered target, and only if the registration records, before B runs, that a top-only detection is a registered verdict row |
| **BLOCKED** | MDE > 0.08, or n_T = 0 | the design cannot detect an effect anywhere in the published band; no verdict on H1 is claimed for that universe; artifacts preserved |
| **PENDING_ACCESS** | the access gate of 0.5 failed | Section 0 reports on **access**, not on the hypothesis; the stage ends as a valid outcome |

**The split verdict is registered in advance as a finding.** If U24 is GO or
DEGRADED while P30 is BLOCKED, the registered reading is: **the mispricing may
be real and simply not reachable from Canada.** That sentence is the result,
not a failure report.

### 0.4 How the bars were derived, before any request

At the tail cell's planning dispersion — prices near 5c or 95c give
p(1−p) ≈ 0.0475, so sqrt(v̄) ≈ 0.218 — inverting MDE = 2·sqrt(v̄/n) at each
bar gives the required tail count:

| bar | required n_T at v̄ = 0.0475 |
|---|---|
| GO, MDE ≤ 0.02 | ≥ 475 |
| stay out of BLOCKED, MDE ≤ 0.08 | ≥ 30 |

Both are planning figures; the realized v̄ is measured from snapshot prices
in Task 3 and reported beside them. The published benchmark (Section 3)
reports two-thirds of its 313,972 contract prices in the 1–10c and 90–99c
bands, so the unrestricted universe reaching 475 tail contracts is expected.
Whether the Canadian-permitted subset retains even 30 is precisely the open
question this gate exists to answer, and it is answerable without reading a
single outcome.

### 0.5 The access gate

ACCESS-OK requires all of the following, measured in Task 1, each with its
figure and date recorded in `docs/ACCESS.md`:

1. Settled markets are enumerable over HTTP without any credential.
2. The resolution outcome is exposed on the settled-market record, verified
   as **field presence on at most five records**, logged; no statistic is
   computed from what those fields contain.
3. At least 1,000 settled markets are enumerable in total. At the published
   two-thirds tail share, GO needs about 703 markets (475 / 0.676); the floor
   of 1,000 leaves margin for a lower realized share.
4. Price history is retrievable back to 30 days before close for markets
   whose lifetime reaches that far, so S30 is computable.
5. The published terms of service and `robots.txt`, recorded before any
   repeated fetch, do not forbid keyless automated reading of public market
   data at the measured pace.

Any failure fires PENDING_ACCESS: Section 0 then reports on access, the stage
ends there, and that is a valid outcome.

### 0.6 What fires these gates

`pmexperiment.power.fire_power_gate` computes the MDE and maps it to a
verdict; the bars live in `pmexperiment.registry` as `EFFECT_BAND_LO`,
`EFFECT_BAND_HI` and `Z_CRITICAL`. `tests/test_guards.py` fails if a bar
loses its enforcement site, and fails if the gate pipeline ever references a
resolution-outcome field; both guards are verified by mutation. Raw
enumeration responses are stored untouched (they contain result fields); the
gate consumes a projection with the outcome stripped at load time
(Section 10).

---

## 1. Universe and the permitted subset

*To be registered before any outcome is read.*

Two universes, reported separately and never pooled:

- **Unrestricted.** All resolved contracts retrievable from the public source.
- **Canadian-permitted.** The registered filter: the three permitted
  categories (economic indicators, financial markets, climate), the 30-day
  minimum maturity, and a volume floor chosen and justified **before** it is
  applied.

The filter is registered, then reported on. **It is not tuned to increase the
sample.** The sample it costs is a first-class output.

---

## 2. The cost model

Registered in full before anything is measured, so no cost can be chosen
after seeing a result. Modeled participant: a Canadian retail individual
funding in CAD, converting to USD, holding one side of one contract to
settlement, and converting back.

| component | registered value | status and direction of bias |
|---|---|---|
| venue fee | **2 cents per contract per side, both sides counted: 4 cents round trip** | assumption, conservative. Kalshi's published taker schedule is $0.07·P·(1−P) per contract rounded up (≈ 1.77 % of price at 50c, ≈ 0.33c at 5c), and settlement carries no fee, so the flat 4c **overstates** the venue cost at every price, most severely at the tails. Bias: against H1 surviving costs. |
| spread | **1 cent half-spread, paid once at entry** | assumption. A settlement exit crosses no spread. Tail books on the platform are typically 1–3c wide; illiquid extremes can be wider. Bias: likely **understates** the cost at the illiquid tails, i.e. toward H1 — carried as a named caveat wherever the cost floor is used. |
| FX schedule | **1.5 % of committed principal per direction: CAD→USD at entry, USD→CAD at exit, 3.0 % round trip** | assumption. Sits inside the 1.0–2.5 % retail margin band Canadian banks quote over mid-market. **Overstates** low-cost channels (multi-currency brokers, Norbert's gambit ≈ 0.2–0.5 %); **understates** card-schedule FX (≈ 2.5 %+). Applied to the entry price of the side purchased. |

**The cost floor, in probability points.** For a contract entered at price p
in dollars:

    C(p) = 0.04 + 0.01 + 0.03·p

At the favourite tail, p = 0.95, the floor is **0.0785** — a calibration edge
there must exceed roughly 7.9 probability points per contract to survive this
registered retail path. That number sits at the top of the published effect
band (Section 3), and the proximity is registered here, before measurement,
as the central economic fact this repository exists to test.

No component of this table may be revised after a result is seen; a better
cost estimate enters only as a numbered amendment with its evidence.

---

## 3. The effect band under test

**Registered band: 0.02 to 0.08 absolute probability points of miscalibration
in the tail cell** (snapshot prices 1–10c and 91–99c), fixed here before any
measurement, from the published favourite-longshot magnitudes:

- Bürgi, Deng and Whelan, *Makers and Takers: The Economics of the Kalshi
  Prediction Market*, University College Dublin, January 2026. 313,972
  Yes-and-No contract prices on 46,282 contracts across 12,403 events, Kalshi
  2021 through April 2025, total staked ≥ $1,000, final spread ≤ 20c, open at
  least 24 hours. Buyers of contracts under 10c lose over 60 % of their money
  after fees; a 5c contract that wins 3 % of the time — a **2-point** gap —
  returns −40 % before fees; a 95c contract winning 98 % — a **3-point** gap
  — returns +3.1 % before fees; the average pre-fee return across all
  contracts is −20 %. Two-thirds of all recorded prices sit in the 1–10c and
  90–99c bands.
- Krause, *Market Efficiency and the Favorite-Longshot Bias in Unemployment
  Prediction Markets*, 2026: longshots priced below 30c settled YES 4.0 % of
  the time, a bias of **−0.077** — about 7.7 points — inside a
  permitted-category (economic-indicator) series. The companion CPI study
  (*Zero-Price Contracts and the Favorite-Longshot Bias in CPI Prediction
  Markets*, SSRN 7087538, 95 contracts over 12 months) finds **no** classic
  favourite-longshot bias — registered here as evidence that the effect
  inside the permitted categories is heterogeneous and may be absent in some
  series.
- Page and Clemen, *Do Prediction Markets Produce Well-Calibrated Probability
  Forecasts?*, Economic Journal 123(568):491–513, 2013: calibration is good
  near expiry and deteriorates with time to expiration, in the
  favourite-longshot direction. Consistent with that, the Kalshi benchmark's
  mean absolute error roughly triples between the closing day and ten days
  out. The 30-day maturity rule therefore pushes the permitted subset toward
  the horizon where the published bias is larger — and where prices are
  noisier.

The band's bottom, 0.02, is the smallest well-established tail gap on the
platform itself. Its top, 0.08, rounds the largest single-category published
figure, Krause's 7.7 points. The gate (Section 0.3) is judged against this
band and nothing else.

---

## 4. What is never computed before the gate

No calibration curve. No realized return by price bucket. No contract-level
outcome join. No statistic of any kind relating a price to a resolution.

The gate reads bucket counts and dispersion. Nothing else.

---

## 5. Retrieval method and its measured properties

*To be registered.* How resolved contracts are enumerated, at what measured
rate, and how deep the public history reaches. Measured, never assumed.

---

## 6. Ambiguity and classification

*To be registered.* The rule that assigns a contract to a category, and the
handling of any contract it cannot assign. Ambiguous is a first-class counted
class, attributed to nothing.

---

## 7. Coverage

*To be registered.* Enumeration coverage and resolution coverage are separate
reported quantities, each with its direction of bias named.

---

## 8. Inference

*To be registered after the gate fires.* The estimator, the interval
construction, the clustering unit, and the trial grid with its multiplicity
correction. Nothing here is computed before Section 0's gate.

---

## 9. Power method and the registered effect assumption

MDE = z · sqrt(v̄ / n_T), with z = 2.0 two-sided, v̄ the mean Bernoulli
dispersion p(1−p) over the cell's snapshot prices, and n_T the tail count —
for a sampled universe, N times the Wilson 95 % lower bound of the sampled
tail share (Section 0.2). Its inputs are a count and a dispersion, both
computable from prices alone; nothing else enters. The band it is judged
against is Section 3's 0.02 to 0.08, fixed before any measurement. Planning
values and their derivation: Section 0.4. Realized values land in Section 15
beside them.

---

## 10. Outcome blindness

Before the gate fires, the following may be read: market identifiers, series
and category fields, open and close times, volumes, order-book metadata, and
prices at any time. The following may not be computed: a calibration curve, a
realized return by price bucket, a contract-level join of a price to a
resolution, or any statistic of any kind relating a price to an outcome.

Raw enumeration responses contain result fields and are stored untouched in
`data/raw/` (gitignored, append-only). The gate pipeline consumes a
projection with the outcome stripped at load time, and `tests/test_guards.py`
fails if a gate module references an outcome field. The single registered
exception: the Task 1 access probe verifies outcome-field **presence** on at
most five settled records, logs which records, and computes nothing from
their contents (Section 0.5, condition 2).

---

## 11. Costs

In the form the inference consumes: a candidate calibration edge at entry
price p survives the registered Canadian retail path only if it exceeds

    C(p) = 0.05 + 0.03·p

probability points per contract (Section 2: 4c venue fee + 1c half-spread +
3 % FX on committed capital). C(0.95) = 0.0785. C(0.05) = 0.0515. Fixed
before any measurement; not revisable after a result is seen.

---

## 12. Reserved

*Unfilled.*

---

## 13. The operator prior

*To be filled by the operator before the gate fires, and recorded with the date
it was given.* Registered so the verdict reads against a stated expectation
rather than a remembered one.

---

## 14. Reproducibility

The gate verdict must be regenerable from: the stored raw enumeration and
candlestick responses under `data/raw/`, the registered constants in
`pmexperiment.registry`, and the registered seed 20260829. A rerun may depend
on no other state. Live endpoints may have moved on by the time of a rerun;
the stored responses are the record.

---

## 15. Results

*Written only after a gate fires.*

### 15.1 The access gate, fired 2026-08-29: PENDING_ACCESS

Fired on the five registered conditions of Section 0.5, measured in Task 1
and recorded with evidence in `docs/ACCESS.md`:

| condition | reading |
|---|---|
| 1 — enumerable without credential | PASS (HTTP 200 keyless, 127.6 ms) |
| 2 — outcome exposed on settled record | PASS (`result` present; 2 of 5 permitted records inspected; no statistic computed) |
| 3 — ≥ 1,000 settled markets enumerable | NOT MEASURED, fails closed (counting requires systematic pagination the recorded terms do not sanction) |
| 4 — price history to 30 days before close | NOT DEMONSTRATED, fails closed (0 daily candles on the one ≥ 30-day-old market tested; recent-market candles work) |
| 5 — terms permit keyless automated reading | FAIL, fails closed (recorded terms prohibit systematic retrieval and AI-mediated use without written authorization; the API Developer Agreement is unreadable by automated means) |

**Consequence, exactly as registered in Section 0.3: Section 0 reports on
access, not on the hypothesis. The power gate never fired. No price bucket
was built, no dispersion was computed, no outcome was joined to any price,
and no statistic relating a price to an outcome exists in this repository.**

A depth finding travels with the verdict, measured before the gate closed
the stage: the keyless settled listing reaches back only to between
2024-01-01 and 2024-05-31 (bracketed by single-page probes, n = 6 probes),
so the 2021→Apr 2025 span the published benchmark analyzed is not
reproducible keylessly even before the terms are considered.

**What would reopen access:** written authorization from Kalshi for
systematic retrieval and AI-mediated analysis, or a Kalshi-sanctioned bulk
research channel not requiring an account, or an operator decision to
register an account — which ADR-002 currently excludes. Any reopening is a
new numbered gate firing under Section 16; nothing here is a second look,
because no outcome was ever read.

### 15.2 The fee-versus-edge band, fired 2026-08-29: BAND-OPEN

**Fired on Amendment 2's registered definitions, over arithmetic alone. No
venue was read — no contract, price, order book or resolution was requested
from any source — so Sections 4 and 10 stand intact and zero dollars were
spent. Full table and evidence in `docs/BAND.md`.**

**In one sentence: BAND-OPEN — a surviving region exists that the permitted
subset admits, at entry prices 91–99c held to resolution, requiring 5.85 points
of underpricing at the registered FX turnover against a registered band whose
top is 8.00 points.**

| verdict row | reading |
|---|---|
| BAND-EMPTY | **does not fire.** The registered band exceeds the required underpricing at 10 of 10 registered buckets, on both exit routes, at k = 1, at k = 12 and in the k → ∞ limit. |
| BAND-NARROW | **does not fire.** Its condition requires the surviving region to lie *only* outside the permitted categories or below usable volume. The category clause is contradicted by Krause's permitted-category (economic-indicator) attribution; the volume clause cannot be evaluated, because Section 1's volume floor was never registered (ADR-006, 2026-08-29). |
| **BAND-OPEN** | **fires.** No registered rule excludes 91–99c prices from the permitted categories or from the 30-day maturity rule, and the one cited magnitude reaching the surviving part of the band is attributed to a permitted category. |

**The surviving region, registered here as the only region the power gate may
fire over:** entry prices **91–99c**, the favourite half of the registered tail
cell, **held to resolution**, on either side of the book, requiring an edge
above **5.85 points** at the binding k = 1 — 5.73 points at 91c rising to 5.97
at 99c. The 1–10c half is excluded because the documented miscalibration there
is *over*pricing, whose exploitable expression is already a purchase at 90–99c;
the eight non-tail deciles are excluded because no effect magnitude is
registered outside the tail cell; and the exit-before-resolution route is
excluded because its 0.0015 margin at 95c is thinner than the 0.00195 by which
Section 2's FX base understates cost at that same price.

**Three qualifications registered with the verdict and not separable from it:**

1. **The surviving region is the top 2.15 points of a 6-point band, and no
   cited source places a magnitude there at that bucket.** The magnitudes cited
   at 91–99c are Bürgi's 2.0 and 3.0 points; both fail at k = 1, and the 3.0
   exactly ties the fee-plus-spread floor of 0.0300 even with FX driven to zero.
   The only cited magnitude large enough to clear is Krause's 7.7 points, whose
   exploitable entry price is 88.3c — the 81–90 decile, outside the tail cell
   the band is registered for.
2. **The band's top carries no n** (standing rule 13). Bürgi sets the bottom
   with 313,972 contract prices on 46,282 contracts across 12,403 events;
   Krause sets the top, and no sample size for it appears anywhere in this
   document.
3. **BAND-OPEN is not a finding that an edge exists.** It records that cost
   alone does not close the question. What it authorizes is the power gate over
   the named region, and nothing else.

**What Section 2 predicted, now confirmed.** Section 2 registered before any
measurement that C(0.95) = 0.0785 "sits at the top of the published effect band
… the central economic fact this repository exists to test." The arithmetic
confirms it to **0.0015**: the round-trip cost curve meets the band's top
exactly at a price of $1.00, which cannot be traded. **The registered cost floor
runs entirely inside the registered effect band at every price** — below its top
everywhere, above its bottom everywhere.

**The decisive figure, for a reader who reads one number:** fee and half-spread
alone total **0.0300** on the held route before any FX at all, against a
registered band bottom of **0.0200**. **No FX treatment, no venue price and no
exit route reaches the bottom of the band.**

### 15.3 The Polymarket access gate, fired 2026-08-30: PENDING_ACCESS

**In one sentence: PENDING_ACCESS — Polymarket's published Terms of Use,
effective 2026-08-11 and read in full before any repeated fetch, prohibit the
data-gathering tool class this enumeration requires and extend expressly to API
and on-chain access, so Section 0 reports on access exactly as Section 0.3's
registered row prescribes and exactly as Stage A did for Kalshi.**

**The power gate did not fire — not over 91–99c and not over any other region.
No contract was enumerated, no price bucket was built, no dispersion was
computed, and no statistic relating a price to an outcome exists in this
repository.** Evidence and verbatim clauses in `docs/ACCESS.md`; the retraction
of Amendment 1's premise is Amendment 6.

| quantity | reading, 2026-08-30 |
|---|---|
| `robots.txt`, polymarket.com | HTTP 200 in **35.7 ms**, 73 bytes: `User-agent: *`, a sitemap line, and **no `Disallow` of any kind** |
| `robots.txt`, gamma-api / clob / data-api | HTTP **404** in 280 / 201 / 221 ms — no crawl directives published on any API host |
| Terms of Use | read in full, **59,617 bytes**, effective **2026-08-11**, Adventure One QSS, Inc. |
| the decisive clause | prohibits "data mining tools, robots, crawlers, or similar data gathering and extraction tools to scrape or otherwise remove data", with **no entity-type qualification** |
| scope of that prohibition | the binding notice reaches anyone "CONNECTING VIA AN API"; the Data clause reaches data taken "directly or through an API, or any other means, **including on-chain**" |
| developer docs | Cloudflare IP-based rate limits and builder tiers published; **no** terms, licence, acceptable-use policy or public-data grant |
| market-data reachability, rate limits, history depth | **WITHHELD — not measured.** See below. |
| contracts enumerated | **0** |
| Amendment 5's volume floor, cost in sample | **not measured** — reported absent, never as zero (standing rule 5) |

**Why reachability was withheld rather than measured, and why that is not a gap
in the record.** Standing rule 4 says measured beats documented, and the stage
prompt asked for reachability, rate limits and history depth. Every one of those
measurements requires sending market-data requests to a venue whose recorded
terms prohibit the tool class that sends them. ADR-007 settled this precedence
on 2026-08-29 for Kalshi — rule 12 outranks rule 4 when measuring would itself
be the prohibited act — and the same reasoning applies unchanged here.

**The ordering is the improvement over Stage A, and it is worth recording.**
Rule 12 requires the terms be recorded *before any repeated fetch*. Stage A read
**11 keyless market requests** before its terms position was established and
could only withhold the rate-limit burst afterwards. Stage C read `robots.txt`
and the terms **first**, and therefore sent **zero market-data requests** to
Polymarket. The rule's ordering clause did the work it was written to do.

**Request log:** 7 requests to Polymarket hosts on 2026-08-30 — 4 `robots.txt`,
2 page fetches (`/tos`, `docs.polymarket.com`), 1 rendered read of `/tos` — plus
1 fetch of the embedded terms document from `docs.google.com`. All single-shot,
spaced, no retries, no pagination. **None requested a contract, a price, an
order book or a resolution.**

**What would reopen access** is recorded in Amendment 6: prior written consent
from Adventure One QSS, Inc.; enrolment in the builder program the Terms name;
or a Polygon read through infrastructure that is not a Polymarket Interface,
under a legal analysis this repository has not performed. Any reopening is a new
numbered gate firing under Section 16. Nothing here is a second look, because no
outcome was ever read.

---

### 15.4 The Kalshi Internal Use route, recorded 2026-09-01: EXISTS-AND-UNTRAVELLED

**In one sentence: Kalshi's institutional desk replied that the use as described
fits their Internal Use data licence — so the route was not declined on the
merits — while applying requires an established legal entity with formation
documents and beneficial-owner verification, and the 2021 historical depth is
available on that licence through historical endpoints not subject to the
live-data cutoff Stage A measured at roughly spring 2024.**

**This is correspondence, not a gate firing over a measurement.** Stage E sent
**zero requests** to Kalshi or to any other host. **No contract was enumerated,
no price bucket was built, no dispersion was computed, and no statistic relating
a price to an outcome exists in this repository.** Sections 4 and 10 stand
intact. Full evidence, and the admissibility analysis this summarises, in
`docs/ACCESS.md` and DECISIONS.md ADR-016.

| quantity | reading, received 2026-09-01 |
|---|---|
| merits | **not declined.** The use as described fits the Internal Use data licence; no merits objection was raised |
| the applying requirement | **an established legal entity**, with formation documents and beneficial-owner verification |
| the operator's standing | an individual undergraduate. **No such entity is held** |
| historical depth on the licence | **2021 onward, through historical endpoints**, expressly not subject to the live-data cutoff |
| Stage A's keyless cutoff, restated | earliest keyless settled close between **2024-01-01 and 2024-05-31**, n = 6 bracketing probes — a property of the keyless surface, **not of the archive** |
| licence granted | **none. Nothing was applied for, so nothing was granted and nothing was refused** |
| fee | **UNMEASURED.** No figure reported, none assumed |
| does Internal Use permit **publishing** a calibration result? | **UNRESOLVED.** The instrument was never read, and a licence's name is not a clause |
| does it carry the AI/ML written consent Kalshi's Section I conditions separately? | **UNRESOLVED.** That clause class is what closed Kalshi in Stage A |
| contracts enumerated, requests sent, dollars spent | **0, 0, 0** |

**Admissibility under ADR-012, stated and not glossed.** Correspondence carries a
**received date, not an effective date**. Fired through
`pmexperiment.admissibility`, the claim returns **UNMEASURED on element (2)**,
and separately this repository holds **the operator's summary rather than the
reply's text**, so element (1)'s quotation requirement is unmet in substance even
though the check cannot see it. UNMEASURED here means *not checkable in the form
ADR-012 requires*; it does not mean doubted, and it is not a synonym for
PROHIBITED. The argument that a received date *is* the effective date for an
instrument that has no other is recorded at full strength in `docs/ACCESS.md`
and is not adopted, because amending the standard at closure to govern a
measurement that will never be made is worse than leaving it open.

**What this changes in the register, stated plainly.** Stage D closed on
2026-08-30 with "no candidate returns PERMITTED" and "there is none", **while
recording in the same document that the candidate space was sampled rather than
enumerated and that "there is none" is a verdict over what was read.** That
limit was correct, and was shown correct within two days. The register no longer
holds that no route exists. **It holds that one exists, that it was not refused,
and that this operator cannot stand up to it.**

**An established legal entity is a necessary step on this route, not a
sufficient one.** Three unread questions survive it: the fee, whether Internal
Use permits publication, and the AI/ML consent. None has been measured and none
is assumed.

---

## 16. Closure conditions

Written before the read. **H1 closes** if both verdict cells fire BLOCKED:
the question is then not testable at achievable power from the public
history, and the closure language is NPD's — *unresolved at achievable
power* — with the realized MDEs and their n beside it. **H1 stays open** on
any universe that fires GO or DEGRADED; Stage B for that universe is
authorized by the gate row and by nothing else. **The split verdict** — U24
clears while P30 fires BLOCKED — closes the Canadian question as *not
measurable from the permitted subset at achievable power* while leaving the
unrestricted question open, and is reported as a finding. **Reopening:** the
permitted subset accumulates settled contracts with the calendar, so a later
session may refire the gate on a fresh enumeration as a new numbered firing —
the gate reads no outcome, so refiring is not a second look.

---

## 17. Amendments

Amendments append here, numbered, each carrying its own evidence and the date
it was made. Nothing above this line is edited after Section 0 is committed.

---

### Amendment 1 — the measurement venue moves to Polymarket; Kalshi stays PENDING_ACCESS

**Made 2026-08-30, before any statistic relating a price to an outcome exists.**

**What changed.** Section 1's source moves from Kalshi to Polymarket for the
measurement universe. Kalshi's PENDING_ACCESS verdict of 2026-08-29 stands
unaltered and is not re-litigated: its Data Terms of Use prohibit systematic
retrieval and AI-mediated use without written authorization, and keyless settled
history reached only spring 2024.

**Why Polymarket is a different case, not a workaround.** Polymarket's public
read endpoints require no API key, no authentication and no wallet, and
settlement sits on Polygon, so the data is public by construction rather than by
permission. This is the opposite of Kalshi's position, where the data was
technically reachable and the terms did not sanction reaching it. Standing rule
12 is satisfied here rather than circumvented.

**What it costs, registered rather than discovered.** Canadians cannot trade
Polymarket. The measurement therefore answers *whether mispricing exists*, and
does not answer *whether it is reachable from Canada*. Those were always two
questions in this registration and they are now measured on different venues, or
in Kalshi's case not measured at all.

**Transfer is registered as UNTESTED and may not be assumed.** A calibration
result on Polymarket is not evidence about Kalshi. The evidence for treating
these as distinct: a documented Kalshi bias has been reported not to replicate on
Polymarket, the largest Polymarket study reports no general longshot bias while
other work finds one on Kalshi, and this program's own MLCryptoEngine H2 measured
cross-venue transfer at AUC 0.501. Any later claim about a Canadian-tradeable
edge requires its own measurement on the venue where it would be traded.

**Category mismatch, registered now.** Polymarket's documented mispricing
concentrates in politics and sports. Those are exactly the categories excluded
from the Canadian-permitted subset, which allows economic indicators, financial
markets and climate at a 30-day minimum maturity. So a real Polymarket effect may
sit entirely outside the contract set a Canadian could trade. This is stated
before measurement so it cannot later be offered as an explanation.

---

### Amendment 2 — the fee-versus-edge band fires before any measurement

**Made 2026-08-30.** A new gate, ordered ahead of the power gate, because it is
free and may be decisive on its own.

**Why it comes first.** Eleven MLCryptoEngine hypotheses closed on cost rather
than on signal, several after data had been collected. If the fee structure
leaves no price region where a documented effect could survive, the trading
question closes on arithmetic before a single contract is enumerated.

**The registered arithmetic.** The Canadian venue charges a flat **$0.02 per
contract per side**. A contract pays $1.00 on correct resolution and $0.00
otherwise, so the fee does not scale with price. Break-even therefore requires
the true probability to exceed the market price by:

| exit route | fee borne | required underpricing |
|---|---|---|
| held to resolution | one side, $0.02 | **≥ 2.0 percentage points** |
| exited before resolution | both sides, $0.04 | **≥ 4.0 percentage points** |

before spread and before the FX schedule of Section 2. Because the fee is flat
in cents while the exploitable edge at favourites is also small in cents, the
requirement is hardest exactly where favourite-longshot bias is documented to
live.

**What this gate computes.** Across price buckets, the minimum underpricing
required to break even net of fee, spread and FX, against the effect band
registered in Section 3. It reads published effect magnitudes and the fee
schedule. **It reads no contract, no price and no outcome from any venue**, so
it violates neither Section 4 nor Section 10.

**Registered verdicts.**

| verdict | condition | consequence |
|---|---|---|
| BAND-EMPTY | no price bucket where the registered effect band exceeds the required underpricing | the tradeable question is **closed on cost**. The phenomenon study may still proceed under Amendment 3, labelled as such. |
| BAND-NARROW | a surviving region exists only at price buckets outside the Canadian-permitted categories or below usable volume | recorded as a **split finding**: an effect may be real, priced, and unreachable. |
| BAND-OPEN | a surviving region exists inside the permitted subset | the power gate proceeds against that region, and only that region. |

The band is computed once and registered. It is **not** recomputed after seeing
a calibration result, and no bucket may be added to it afterwards.

---

### Amendment 3 — the terminal question admits a trading decision; the repository still never trades

**Made 2026-08-30.** A deliberate scope change, recorded rather than allowed to
drift.

**What changed.** The registration previously admitted only a measurement
question. It now admits a terminal question of whether a tradeable edge exists
that survives Canadian retail cost. The operator has stated that account
creation is acceptable.

**What did not change, and is not negotiable.** No stage in this repository
places an order, holds a position, connects to a broker, or stores a trading
credential. The scope guard in `CLAUDE.md` stands. A tradeable finding here is a
finding, and any execution is a separate decision taken outside this repository
with its own record.

**Ordering, registered.** The fee band of Amendment 2 fires first. The power gate
fires second, and only over a region the band left open. No calibration statistic
is computed before both have fired.

**The phenomenon study is separable.** If the band closes the tradeable question,
the Polymarket calibration measurement may still proceed as a documented
phenomenon study. It must then be labelled as one throughout, and may not be
presented as, or converted into, a strategy.

**The Kalshi authorization request is registered as the only path that reopens
measurement on a Canadian-tradeable venue.** Written authorization is what their
terms name. Sending that request is recorded here as an open action with no
assumed outcome.

---

### Amendment 4 — the FX treatment: turnover 1 binds, amortization is reported beside it

**Made 2026-08-29, before the band gate fired and while no statistic relating a
price to an outcome exists.** Registered before it is used, as Stage B Task 3
requires.

**The question.** Section 2 registers "1.5 % of committed principal per
direction … Applied to the entry price of the side purchased." That fixes the
rate and the base. It leaves implicit whether the charge recurs per contract or
is paid once per funding and shared across everything that funding buys. The
two readings differ by an order of magnitude at the favourite tail: 3 % of a
95c contract is 2.85 cents against an edge measured in single cents, while one
conversion spread across a year of positions is a fraction of a cent.

**Both readings are the same formula.** The schedule charges on currency
conversion, not on trades. If one conversion's principal is deployed into
contracts k times before it is converted back, the per-contract share is

    FX(p) = 0.03 · p / k

Section 2's registered participant — "converting to USD, holding one side of
one contract to settlement, and converting back" — is exactly k = 1. The
amortized reading is k > 1. Nothing new is introduced here; a parameter Section
2 fixed implicitly is given a name so the choice can be seen.

**Registered: k = 1 binds. k > 1 is reported beside it and never substituted
for it.** Three reasons, in order of force:

1. **Section 2 forbids the substitution.** "No component of this table may be
   revised after a result is seen; a better cost estimate enters only as a
   numbered amendment with its evidence." Moving the binding model to k > 1
   lowers the cost floor in the direction that helps H1. That is the revision
   the registration exists to prevent, and this amendment does not make it.
2. **The direction of bias runs the safe way.** k = 1 **overstates** FX for a
   participant who trades repeatedly on one funding, biasing toward
   BAND-EMPTY — against H1. k → ∞ **understates** it for a single-shot
   participant, biasing toward BAND-OPEN — toward H1. Binding the reading that
   biases against H1 means a surviving band cannot be an artifact of a generous
   assumption.
3. **It does not decide the verdict.** Computed both ways in Task 4, the band's
   top clears the required underpricing at all ten registered buckets on both
   exit routes at k = 1, at k = 12 and in the k → ∞ limit; the band's bottom
   clears at none of them under any k. The choice is therefore visible and
   non-load-bearing, which is the best position a contested assumption can hold.

**The reported alternatives, and why those values.** k = 12 is the most
favourable plausible amortization for the permitted subset, because the
registered 30-day minimum maturity caps a held-to-resolution strategy at roughly
twelve deployments per funding year, and idle time between positions lowers it.
k → ∞ sets FX to exactly zero — a bound no amortization can beat — so a result
that survives it survives every FX argument that could be made.

**An input this stage needed and did not find, recorded rather than supplied.**
The Stage B prompt describes the schedule as charging "1.5 percent under $10,000
CAD". **No tier threshold is registered anywhere in this document**: Section 2
registers a flat 1.5 % per direction with no size break, and no position size is
registered either. The threshold is therefore not used. It would change nothing
at the registered unit of one contract, but it is recorded as absent rather than
adopted from a prompt, per standing rule 5.

**Two registered simplifications, named with their direction and not revised.**
Section 2 applies FX to the entry price of the side purchased, which (a)
excludes the fee and half-spread from the conversion base, understating cost by
0.03 × 0.05 = **0.0015** on the round-trip route, and (b) values the exit
conversion at the entry price rather than at the $1.00 a winning contract
returns, understating by a further 0.015 × 0.03 = **0.00045** on a 95c contract
that wins 98 % of the time. Both lean **toward** H1. Their sum, **0.00195**, is
recorded here so Task 4 can report where a survival margin is thinner than the
slack in its own inputs.

---

### Amendment 5 — the volume floor of Section 1, registered before any enumeration

**Made 2026-08-30, before a single contract had been enumerated from any
venue.** Section 1 registered that the Canadian-permitted filter carries "a
volume floor chosen and justified **before** it is applied". Stage A's Task 2
never armed, so the floor was never filled in, and Entry 5 records that this is
exactly why Amendment 2's BAND-NARROW row could not be evaluated in Stage B. It
is filled here, ahead of Stage C's enumeration, as standing rule 9 requires.

**The registered floor: total traded volume ≥ $1,000 USD per contract.**

**Why this number, and why it is not mine.** It is the volume filter of the
benchmark study whose magnitudes set the registered effect band. Section 3
records Bürgi, Deng and Whelan analyzing contracts with "total staked ≥ $1,000,
final spread ≤ 20c, open at least 24 hours". Importing the benchmark's own floor
has three properties no self-chosen number has:

1. **It was chosen by someone else, before this repository existed, for reasons
   unrelated to this sample.** Standing rule 9 forbids tuning a filter to
   increase a sample; a floor imported from the study that defines the effect
   band cannot have been tuned to this one.
2. **It makes the sample comparable to the band it is judged against.** The
   registered band's magnitudes were measured on contracts that passed this
   filter. A looser floor would judge a different population against those
   magnitudes.
3. **It is a floor the cost model needs.** Section 2 assumes a 1-cent
   half-spread. On a contract with negligible volume there is no meaningful
   spread to cross, so the registered cost there is not merely uncertain — it is
   undefined.

**What is deliberately not adopted.** The benchmark's two companion filters are
**not** registered here. *Open at least 24 hours* is subsumed by the registered
30-day minimum maturity, which is strictly stronger. *Final spread ≤ 20c*
requires an order-book read this stage does not perform and Section 10 does not
need; adopting it would add a filter whose cost in sample could not be measured
from the fields the gate is allowed to read. Both omissions are recorded here
rather than left to be noticed later.

**Denomination, with its caveat.** Polymarket reports volume in USDC; the
benchmark's "total staked" is US dollars on Kalshi. The two are treated as
comparable at a 1:1 peg, which is an assumption. Direction: a USDC discount
would make the floor slightly loose in dollar terms and a premium slightly
tight; at the magnitudes involved the effect is far below one contract of
sample.

**Scope: the floor is part of the permitted filter, exactly where Section 1
places it**, and is not applied to the unrestricted universe, which Section 1
defines as "All resolved contracts retrievable from the public source". The
floor's cost in sample is reported on **both** universes as a first-class
output, so a reader sees what it removes and not only what it leaves.

**Direction of bias, named before application.** The floor removes thin
contracts, so it **reduces** every count the power gate consumes and biases
toward BLOCKED — against H1. It also **raises** the reliability of the prices
that remain. Neither direction is traded off against the other; both are stated
so the verdict can be read against them.

---

### Amendment 6 — Polymarket's terms are measured, and Amendment 1's premise does not survive

**Made 2026-08-30, before any contract was enumerated from Polymarket and while
no statistic relating a price to an outcome exists.** Figures, dates and
verbatim clauses in `docs/ACCESS.md`.

**What Amendment 1 claimed**, as the whole ground for moving the measurement
venue:

> Polymarket's public read endpoints require no key, no authentication and no
> wallet, and settlement sits on Polygon, so the data is public by construction
> rather than by permission. This is the opposite of Kalshi's position, where
> the data was technically reachable and the terms did not sanction reaching
> it. Standing rule 12 is satisfied here rather than circumvented.

**That claim was never measured.** It cites no terms document, no clause, no
effective date and no fetch date — where Stage A's Kalshi finding quoted its
terms verbatim with the date retrieved. Amendment 1 inferred a conclusion about
*permission* from the absence of an *authentication* requirement. Those are
different things, and substituting one for the other is exactly what standing
rule 4 exists to prevent. The substitution was made inside this registration.

**What the terms say.** POLYMARKET.COM TERMS OF USE, effective 2026-08-11,
published by Adventure One QSS, Inc., read in full on 2026-08-30. The
prohibited-conduct list includes, with no entity-type qualification:

> Use any data mining tools, robots, crawlers, or similar data gathering and
> extraction tools to scrape or otherwise remove data from the Site, any other
> Interface, or Features;

> Use any manual process to monitor or copy any of the material on the Site, any
> other Interface, or Features or for any other unauthorized purpose without our
> prior written consent;

> Harvest or otherwise collect information from the Site, any other Interface,
> or the Features for any unauthorized purpose;

**The scope reaches both paths Amendment 1 relied on.** The binding notice
covers "ACCESSING, INTERACTING WITH OR USING THE SITE, ANY FEATURE OR ANY OTHER
INTERFACE (INCLUDING BY CONNECTING VIA AN API, LINKING YOUR WALLET, OR OTHERWISE
CREATING AN IDENTIFIER ON THE SITE)", and the Data clause defines its subject as
data "contained on our Site, any Interface or Features **directly or through an
API, or any other means, including on-chain**, whether in raw, derived,
aggregated, or anonymized form". **The terms name API access and on-chain access
explicitly.** "Public by construction rather than by permission" is contradicted
by the document Amendment 1 never read.

**Registered consequence: Polymarket is the same case as Kalshi, not the
opposite one.** Both venues serve data that is technically reachable without a
credential, and both publish terms that do not sanction the systematic retrieval
this measurement needs without prior written consent. The distinction Amendment
1 drew does not exist. Amendment 1 is **not** withdrawn — the venue move stands
as the record of what was decided and why — but its stated ground is retracted
here, and no later document may cite it.

**One clause that does not bind, recorded for accuracy.** The Data restriction
is conditional on entity type: it prohibits access by "a non-retail,
professional entity that engages in capital markets activities" or by "a market
data distributor". A Canadian retail individual conducting measurement-only
research is neither, so that clause is **not** the ground of this finding. The
data-mining and crawlers prohibition carries no such condition, and it is.

**The strongest counterargument, recorded rather than suppressed, and why it is
not taken.** The crawlers bullet forbids scraping "from the Site, any other
Interface, or Features", and "Interface" is defined as Polymarket.com "and any
other site to which the Terms are posted". The Terms are not posted at
`gamma-api.polymarket.com`, so it can be argued those API hosts are not
Interfaces and that bullet does not literally reach them. Three reasons it is
not taken: the binding notice expressly extends the Terms to anyone "CONNECTING
VIA AN API"; the data those hosts serve is data "contained on our Site, any
Interface or Features", which the Data clause says may be accessed "directly or
through an API"; and reading a prohibition as narrowly as possible in order to
do the thing it names is assuming permissiveness, which standing rule 5 forbids
and which ADR-006 already refused for Kalshi. **A venue may not be held to a
looser reading than another because its verdict would be more convenient.**

**A further restriction, recorded though not the ground.** The Restricted
Jurisdictions for trading name **Alberta, British Columbia, Ontario and Quebec**
individually, and the Terms provide that a user in a Restricted Jurisdiction "is
only permitted to use the Content Features on the Site or any other Interface
and may not use the Site or any other Interface for any other purpose". For a
participant in those provinces, permitted use narrows further, to news and
information about global current events.

**No separate developer licence grants what the Terms withhold.**
`docs.polymarket.com`, measured 2026-08-30, publishes Cloudflare IP-based rate
limits and a builder program with tiers, and publishes **no** terms of use, data
licence, acceptable-use policy or public-data grant.

**What would reopen access:** prior written consent from Adventure One QSS,
Inc.; or enrolment in the builder program the Terms name; or a Polygon read
performed through infrastructure that is not a Polymarket Interface, under a
legal analysis this repository has not done. The third is recorded as an open
question, **not** as a workaround adopted now.

---

### Amendment 7 — the operator prior arrives at closure, and the entity path is declined

**Made 2026-09-02, after the band gate fired on 2026-08-29 and after both access
gates fired.** It records two operator statements. **Neither is a measurement,
and neither is evidence about H1.**

**First, the prior. Section 13 stands empty, and it is left empty
permanently.**

Section 13, `The operator prior`, reads *"To be filled by the operator before
the gate fires, and recorded with the date it was given."* It has read that
since Section 0 was committed on 2026-08-29 and **it was never filled**. The
operator's prior is now given as **5 to 8 percent** that H1 holds — supplied
**2026-09-02**, at closure, after two gates had already fired.

**It is recorded here rather than written into Section 13, and that is the
point.** Filling Section 13 now would put a post-hoc number in the slot the
registration reserved for a pre-registered one, and the empty slot is a more
honest record than a filled one. **This prior may not be described anywhere as
pre-registered, and no verdict in this repository may be read against it as
though it had been.** It is a **stated** prior, dated at closure.

**Why it is recorded at all, given that.** It is the input to the operator's
cost decision below, and a decision whose input is unrecorded is not a decision
a later reader can audit. A prior of 5 to 8 percent also makes a **null the
modal expected outcome** — which is the frame the closure should be read in, and
it is worth having on the record even arriving late.

**Second, the entity path is declined. This is a decision, not a discovery.**

Section 15.4 records that the one route which exists is gated on **an established
legal entity** with formation documents and beneficial-owner verification. Two
ways to hold one were considered and both are closed by operator decision:

| path | disposition, 2026-09-02 | the operator's stated reason |
|---|---|---|
| **institutional sponsorship** through the university | **declined — not achievable in the time available** | the university was consulted; sponsorship could not be arranged before fourth-year term starts |
| **forming a personal legal entity** | **declined — disproportionate** | the cost is out of proportion to a stated prior of 5 to 8 percent, against a band verdict already recorded as thin |

**"Thin" is a figure, not an impression, and it travels with this row.** The
surviving region is the top **2.15 of 6.0 points** of the effect band at an entry
price of 95c on the held route, requiring **5.85 points** at k = 1 against a
registered band top of **8.00**. Every magnitude any cited source places inside
that bucket — Bürgi's **2.0** and **3.0** points — **fails** the cost floor of
**0.0300**, which the 3.0 exactly ties with FX at zero. The band survives on its
top alone, set by the one source whose n the registration never recorded.

**What this amendment is not, stated so it cannot be misread later.** It is
**the operator declining a cost. It is not evidence about H1**, in either
direction. Nothing here says the effect is absent, present, small or large.
Nothing here is a measurement of any kind: **no contract was enumerated, no
bucket was built, no dispersion was computed, and no statistic relating a price
to an outcome exists in this repository.** A later reader who finds this
amendment and infers a verdict about prediction-market calibration from it has
misread it.

**And it is not a refusal by Kalshi.** The desk did not decline; **this
repository declined.** Section 15.4's label is EXISTS-AND-UNTRAVELLED and it
stays that way.
