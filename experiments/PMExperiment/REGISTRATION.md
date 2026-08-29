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

*Written only after the gate fires. Empty until then.*

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

*(empty)*
