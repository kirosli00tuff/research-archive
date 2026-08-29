# BAND.md — the fee-versus-edge band

Written by Stage B on 2026-08-29. **No venue was read.** No contract, price,
order book or resolution was requested from Polymarket, Kalshi or anywhere
else; every figure below is arithmetic over constants already registered, so
this document violates neither Section 4 nor Section 10. Zero dollars spent.

Every figure is computed by `pmexperiment.band` and pinned by
`tests/test_band.py`, so nothing here is hand arithmetic.

---

## Verdict

**BAND-OPEN.** A surviving region exists inside the permitted subset: at entry
prices 91–99c held to resolution, an effect in the upper part of the registered
band clears the registered cost, requiring **5.85 points** of underpricing at
the registered FX turnover against a band whose top is **8.00 points**.

The qualifier travels with it and is not separable: **that surviving region is
the top 2.15 points of a 6-point band, and no cited source places a magnitude
there at that price bucket.** The two magnitudes cited at 91–99c — Bürgi's 2.0
and 3.0 points — both fail. The only cited magnitude large enough to survive is
Krause's 7.7 points, whose exploitable entry price is 88.3c, outside the
registered tail cell, and whose n appears nowhere in the registration.

---

## Task 1 — the registered inputs, quoted verbatim

### The effect band, REGISTRATION.md Section 3

> **Registered band: 0.02 to 0.08 absolute probability points of miscalibration
> in the tail cell** (snapshot prices 1–10c and 91–99c), fixed here before any
> measurement, from the published favourite-longshot magnitudes:
>
> - Bürgi, Deng and Whelan, *Makers and Takers: The Economics of the Kalshi
>   Prediction Market*, University College Dublin, January 2026. 313,972
>   Yes-and-No contract prices on 46,282 contracts across 12,403 events, Kalshi
>   2021 through April 2025, total staked ≥ $1,000, final spread ≤ 20c, open at
>   least 24 hours. Buyers of contracts under 10c lose over 60 % of their money
>   after fees; a 5c contract that wins 3 % of the time — a **2-point** gap —
>   returns −40 % before fees; a 95c contract winning 98 % — a **3-point** gap
>   — returns +3.1 % before fees; the average pre-fee return across all
>   contracts is −20 %. Two-thirds of all recorded prices sit in the 1–10c and
>   90–99c bands.
> - Krause, *Market Efficiency and the Favorite-Longshot Bias in Unemployment
>   Prediction Markets*, 2026: longshots priced below 30c settled YES 4.0 % of
>   the time, a bias of **−0.077** — about 7.7 points — inside a
>   permitted-category (economic-indicator) series. The companion CPI study
>   (*Zero-Price Contracts and the Favorite-Longshot Bias in CPI Prediction
>   Markets*, SSRN 7087538, 95 contracts over 12 months) finds **no** classic
>   favourite-longshot bias — registered here as evidence that the effect
>   inside the permitted categories is heterogeneous and may be absent in some
>   series.
> - Page and Clemen, *Do Prediction Markets Produce Well-Calibrated Probability
>   Forecasts?*, Economic Journal 123(568):491–513, 2013: calibration is good
>   near expiry and deteriorates with time to expiration, in the
>   favourite-longshot direction. Consistent with that, the Kalshi benchmark's
>   mean absolute error roughly triples between the closing day and ten days
>   out. The 30-day maturity rule therefore pushes the permitted subset toward
>   the horizon where the published bias is larger — and where prices are
>   noisier.
>
> The band's bottom, 0.02, is the smallest well-established tail gap on the
> platform itself. Its top, 0.08, rounds the largest single-category published
> figure, Krause's 7.7 points. The gate (Section 0.3) is judged against this
> band and nothing else.

### The cost model, REGISTRATION.md Section 2

> | component | registered value | status and direction of bias |
> |---|---|---|
> | venue fee | **2 cents per contract per side, both sides counted: 4 cents round trip** | assumption, conservative. Kalshi's published taker schedule is $0.07·P·(1−P) per contract rounded up (≈ 1.77 % of price at 50c, ≈ 0.33c at 5c), and settlement carries no fee, so the flat 4c **overstates** the venue cost at every price, most severely at the tails. Bias: against H1 surviving costs. |
> | spread | **1 cent half-spread, paid once at entry** | assumption. A settlement exit crosses no spread. Tail books on the platform are typically 1–3c wide; illiquid extremes can be wider. Bias: likely **understates** the cost at the illiquid tails, i.e. toward H1 — carried as a named caveat wherever the cost floor is used. |
> | FX schedule | **1.5 % of committed principal per direction: CAD→USD at entry, USD→CAD at exit, 3.0 % round trip** | assumption. Sits inside the 1.0–2.5 % retail margin band Canadian banks quote over mid-market. **Overstates** low-cost channels (multi-currency brokers, Norbert's gambit ≈ 0.2–0.5 %); **understates** card-schedule FX (≈ 2.5 %+). Applied to the entry price of the side purchased. |
>
> **The cost floor, in probability points.** For a contract entered at price p
> in dollars:
>
>     C(p) = 0.04 + 0.01 + 0.03·p
>
> At the favourite tail, p = 0.95, the floor is **0.0785** — a calibration edge
> there must exceed roughly 7.9 probability points per contract to survive this
> registered retail path. That number sits at the top of the published effect
> band (Section 3), and the proximity is registered here, before measurement,
> as the central economic fact this repository exists to test.
>
> No component of this table may be revised after a result is seen; a better
> cost estimate enters only as a numbered amendment with its evidence.

### The three verdict definitions, REGISTRATION.md Amendment 2

> | verdict | condition | consequence |
> |---|---|---|
> | BAND-EMPTY | no price bucket where the registered effect band exceeds the required underpricing | the tradeable question is **closed on cost**. The phenomenon study may still proceed under Amendment 3, labelled as such. |
> | BAND-NARROW | a surviving region exists only at price buckets outside the Canadian-permitted categories or below usable volume | recorded as a **split finding**: an effect may be real, priced, and unreachable. |
> | BAND-OPEN | a surviving region exists inside the permitted subset | the power gate proceeds against that region, and only that region. |

Amendment 2 also registers the two exit routes this stage prices:

> | exit route | fee borne | required underpricing |
> |---|---|---|
> | held to resolution | one side, $0.02 | **≥ 2.0 percentage points** |
> | exited before resolution | both sides, $0.04 | **≥ 4.0 percentage points** |

### Inputs this stage needed and did not find — recorded, not supplied

Standing rule 5: absence is a recorded state, never a synthesized value.

| input | state | consequence |
|---|---|---|
| **the volume floor of Section 1** | **never registered.** Stage A Task 2 never armed (ADR-006, 2026-08-29), so the permitted filter's third axis has no value | BAND-NARROW's "below usable volume" clause **cannot be evaluated**. Recorded in Pass 2 rather than filled with a guess. |
| **an FX tier threshold** | **absent.** The Stage B prompt describes the schedule as charging "1.5 percent under $10,000 CAD"; Section 2 registers a flat 1.5 % per direction with **no** size break, and no position size is registered either | the threshold is not used. It is untriggered at the registered unit of one contract in any case. Recorded as Amendment 4. |
| **Krause's n** | **absent from the registration**, which records the 4.0 % settlement rate and the −0.077 bias but no sample size | the band's **top** carries no n. Stated wherever the top carries a conclusion (standing rule 13). |
| **the quantifier in Amendment 2's BAND-EMPTY row** | ambiguous on its face — "the registered effect band exceeds" could mean the whole band or any of it — but **disambiguated by the amendment's own rationale**, which fires BAND-EMPTY when there is "no price region where a documented effect **could** survive" | the existential reading is registered, not chosen here. Both readings are reported in Pass 1 anyway. |

---

## Task 2 — the unit determination

**The registered band is in absolute probability points, not percent realized
return. It is not ambiguous, and no conversion is needed.** Full derivation in
DECISIONS.md ADR-009; the summary is that each recorded magnitude was
reconstructed both ways and checked against the numbers the registration itself
prints, using the identity `return = gap ÷ price`:

| recorded figure | as a probability gap | as a return | reproduces the record |
|---|---|---|---|
| Bürgi's 5c contract winning 3 % | 0.03 − 0.05 = **−0.02** = the recorded "2-point gap" | −0.02/0.05 = **−40.0 %** = the recorded "−40 %" | both |
| Bürgi's 95c contract winning 98 % | 0.98 − 0.95 = **+0.03** = the recorded "3-point gap" | 0.03/0.95 = **+3.16 %** = the recorded "+3.1 %" | both |
| Krause's **−0.077** at longshots settling 4.0 % | implies a mean bucket price of **0.117**, coherent for "below 30c" | implies a mean price of **0.043**, and would make this the *smallest* figure cited | probability only |

The Krause row settles it alone: read as a return, the figure Section 3 calls
"the largest single-category published figure" would be the smallest of the
three. The fee is denominated identically — $0.02 against a $1.00 payout is
0.02 of probability — so band and cost are directly comparable.

**The magnitude that is not usable as an effect size.** Bürgi's "buyers of
contracts under 10c lose over 60 % of their money **after fees**" is a return,
and it is post-fee. Converted it is 0.030 at 5c and 0.057 at 9.5c, inside the
band, but it already contains the venue's own fee; using it against a cost model
would charge the fee twice. Section 3 set neither band edge from it.

**The consequential half: direction.** At longshot prices the documented
miscalibration is *over*pricing, so a buyer of a longshot holds a negative edge
while break-even requires *under*pricing. On a binary venue the exploitable
expression is the complement. Restated in the underpriced direction, **every
registered magnitude sits at a high entry price**:

| source figure | exploitable side | entry price | underpricing | n |
|---|---|---|---|---|
| Bürgi, 5c winning 3 % | NO | **0.950** | 0.020 | 313,972 prices / 46,282 contracts / 12,403 events |
| Bürgi, 95c winning 98 % | YES | **0.950** | 0.030 | as above |
| Krause, sub-30c settling 4.0 % | NO | **0.883** | 0.077 | **not recorded** |

Because the registered FX is proportional to entry price, every exploitable
expression of the band is charged FX at 88–95c rather than at 5–12c. **That is
what makes the FX treatment of Task 3 material rather than academic.**

---

## Task 3 — the FX treatment

Registered as **Amendment 4** before use; reasoning in DECISIONS.md ADR-010.
Both candidate models are one formula with a turnover k:

    FX(p) = 0.03 · p / k

**k = 1 binds** (Section 2's participant converts, buys one contract, holds it
to settlement, converts back). **k > 1 is reported beside it and never
substituted**, because Section 2 forbids revising a cost component in the
direction that helps H1.

| treatment | FX at p = 0.95 | biases the verdict toward | why reported |
|---|---|---|---|
| **k = 1**, per contract — **binds** | **0.0285** | **BAND-EMPTY**, i.e. against H1 | Section 2 as registered; a surviving band cannot be an artifact of it |
| k = 12, one funding year of 30-day positions | 0.0024 | BAND-OPEN, toward H1 | the most favourable plausible amortization under the registered 30-day maturity rule |
| k → ∞, FX exactly zero | 0.0000 | BAND-OPEN, toward H1 | a bound no amortization can beat; a result surviving it survives every FX argument |

**Two registered simplifications, both leaning toward H1, neither revised.**
Section 2 applies FX to the entry price, which (a) excludes the fee and
half-spread from the conversion base — understating cost by 0.03 × 0.05 =
**0.0015** on the round-trip route — and (b) values the exit conversion at the
entry price rather than at the $1.00 a winner returns — a further 0.015 × 0.03 =
**0.00045** at a 95c contract winning 98 %. Their sum is **0.00195**, and Pass 1
reports where that exceeds a survival margin.

---

## Task 4, Pass 1 — the band across price buckets, unrestricted

Required underpricing to break even, in probability points, by registered
decile. **R_H** is held to resolution (one fee); **R_X** is exited before
resolution (two). The registered effect magnitude column is populated **only in
the tail cell**, because Section 3 registers the band there and nowhere else;
elsewhere it is absent, not zero.

| bucket (c) | mid p | R_H k=1 | R_X k=1 | R_H k=12 | R_X k=12 | R_H k→∞ | R_X k→∞ | registered effect magnitude |
|---|---|---|---|---|---|---|---|---|
| 1–10 | 0.055 | 0.0316 | 0.0517 | 0.0301 | 0.0501 | 0.0300 | 0.0500 | **0.02–0.08**, but *overpriced* — a buy has the wrong sign |
| 11–20 | 0.155 | 0.0347 | 0.0547 | 0.0304 | 0.0504 | 0.0300 | 0.0500 | not registered |
| 21–30 | 0.255 | 0.0376 | 0.0576 | 0.0306 | 0.0506 | 0.0300 | 0.0500 | not registered |
| 31–40 | 0.355 | 0.0406 | 0.0607 | 0.0309 | 0.0509 | 0.0300 | 0.0500 | not registered |
| 41–50 | 0.455 | 0.0437 | 0.0636 | 0.0311 | 0.0511 | 0.0300 | 0.0500 | not registered |
| 51–60 | 0.555 | 0.0466 | 0.0667 | 0.0314 | 0.0514 | 0.0300 | 0.0500 | not registered |
| 61–70 | 0.655 | 0.0496 | 0.0697 | 0.0316 | 0.0516 | 0.0300 | 0.0500 | not registered |
| 71–80 | 0.755 | 0.0527 | 0.0727 | 0.0319 | 0.0519 | 0.0300 | 0.0500 | not registered |
| 81–90 | 0.855 | 0.0556 | 0.0756 | 0.0321 | 0.0521 | 0.0300 | 0.0500 | not registered — though Krause's exploitable complement lands here at 0.883 |
| 91–99 | 0.950 | **0.0585** | **0.0785** | 0.0324 | 0.0524 | 0.0300 | 0.0500 | **0.02–0.08**; cited at this bucket: Bürgi's **0.020** and **0.030** |

### The crossing points, stated rather than inferred

**There are no crossings inside the tradeable price range.** Solving R(p) for
each band edge at the binding k = 1:

| curve | vs band bottom 0.02 | vs band top 0.08 |
|---|---|---|
| R_H(p) = 0.03 + 0.03p | p = **−0.3333** — no crossing; the floor exceeds the band bottom at **every** price, including p → 0 | p = **+1.6667** — no crossing; the floor stays below the band top at every price |
| R_X(p) = 0.05 + 0.03p | p = **−1.0000** — no crossing; same reading | p = **+1.0000** — the curve meets the band top exactly at $1.00, a price that cannot be traded, so it stays below it across 1–99c |

The plain statement: **the registered cost floor runs entirely inside the
registered effect band at every price.** The band's bottom is below the floor
everywhere and its top is above the floor everywhere. Section 2 predicted this
in advance — "That number sits at the top of the published effect band … the
proximity is registered here, before measurement, as the central economic fact
this repository exists to test" — and the arithmetic confirms it to 0.0015.

### Both readings of Amendment 2's quantifier

| reading | surviving buckets, route H | surviving buckets, route X | verdict it implies |
|---|---|---|---|
| **existential** — could *an* effect in the band survive? (registered, per the amendment's own rationale) | **10 / 10** at k = 1, k = 12 and k → ∞ | **10 / 10** at every k | **not BAND-EMPTY** |
| strict — would *every* effect in the band survive? | **0 / 10** at every k | **0 / 10** at every k | BAND-EMPTY |

The strict reading is reported so the choice is visible, but it is not the
registered one, and it is not used.

### The decisive crossing, and the dead heat

- **The band's bottom is unreachable everywhere.** The fee and half-spread alone
  come to 0.03 on the held route, before any FX at all. The band's bottom is
  0.02. **No FX argument, no venue price and no exit route reaches it.**
- **At the FX-free limit the held route requires exactly 0.0300, and Bürgi's
  favourite-tail gap is exactly 0.0300.** A dead heat: zero expected profit,
  with FX driven to zero, at the one bucket where a magnitude is actually cited.
- With the registered k = 1, both magnitudes cited at 91–99c fail:

| exploitable figure | entry p | underpricing | R_H k=1 | R_X k=1 | R_H k→∞ |
|---|---|---|---|---|---|
| Bürgi, 5c/3 % → NO at 95c | 0.950 | 0.020 | 0.0585 **fail** | 0.0785 **fail** | 0.0300 **fail** |
| Bürgi, 95c/98 % → YES at 95c | 0.950 | 0.030 | 0.0585 **fail** | 0.0785 **fail** | 0.0300 **dead heat** |
| Krause, sub-30c/4.0 % → NO at 88.3c | 0.883 | 0.077 | 0.0565 **clears** | 0.0765 **clears** | 0.0300 **clears** |

### Margins, and where a margin is thinner than its own slack

At k = 1 against the band top, route H clears by 4.84 points at 1–10c falling to
**2.15 points** at 91–99c; route X clears by 2.83 points falling to **0.15
points** at 91–99c.

**Route X's margin at the favourite tail (0.0015) is smaller than the 0.00195 by
which Section 2's FX base understates cost at the same price.** Its survival
there is inside the slack of its own inputs, so the fired region excludes it.
Route H's margin at that bucket is 0.0215 against a comparable 0.00135 — larger
by a factor of 16 — so it survives robustly.

---

## Task 4, Pass 2 — the Canadian filter

Reported separately from Pass 1, as instructed. **The filter's registered axes
are category, maturity and volume. Price is not one of them**, so no price
bucket is excluded by the filter's construction. What the filter can do is leave
a bucket empty of contracts — and that is a **count**, which this stage may not
read (Sections 4 and 10). Section 0.4 assigns that count to the power gate in as
many words: "Whether the Canadian-permitted subset retains even 30 is precisely
the open question this gate exists to answer."

What the registration does supply, all five inputs, with direction:

| registered input | bearing on the surviving region | direction |
|---|---|---|
| Krause's 7.7 points is "inside a permitted-category (economic-indicator) series" (Section 3) | the only cited figure that both reaches the surviving part of the band and carries a category attribution — and its category is **permitted** | **toward** |
| Page-Clemen, with the benchmark's MAE roughly tripling from closing day to ten days out (Section 3) | the 30-day maturity rule pushes the permitted subset toward the horizon where the published bias is **larger** | **toward** |
| the companion CPI study, **no** classic favourite-longshot bias, n = 95 contracts over 12 months (Section 3) | the effect inside the permitted categories is heterogeneous and may be absent in some series | **against** |
| Amendment 1: Polymarket's documented mispricing "concentrates in politics and sports … exactly the categories excluded" | a real effect on the measurement venue may sit entirely outside the permitted contract set | **against** — and registered as a *risk*, not a measurement, so it is not converted into one here |
| Section 1's volume floor | **never registered** (ADR-006, 2026-08-29) | **absent** — BAND-NARROW's "below usable volume" clause cannot be evaluated |

**Pass 2 conclusion.** The surviving price region is **admissible** inside the
permitted subset: no registered rule excludes 91–99c prices from the permitted
categories or from the 30-day maturity rule, and the one cited magnitude that
reaches the surviving part of the band is attributed to a permitted category.
Whether that region is **populated** is unmeasured, and by registration it is
the power gate's question, not this one's.

---

## Task 5 — the verdict

**BAND-OPEN**, against Amendment 2's definitions as quoted in Task 1 and without
adjusting them:

- **not BAND-EMPTY** — the registered band exceeds the required underpricing at
  10 of 10 buckets on both routes under every FX treatment, so a documented
  effect *could* survive;
- **not BAND-NARROW** — its condition requires the surviving region to lie
  *only* outside the permitted categories or below usable volume; the category
  clause is contradicted by Krause's permitted-category attribution, and the
  volume clause cannot be evaluated because no floor was ever registered;
- **BAND-OPEN** — a surviving region exists that the permitted subset admits.

### The surviving region, named precisely

**Entry prices 91–99c — the favourite half of the registered tail cell — held to
resolution, on either side of the book (YES on a documented-underpriced
favourite, or NO on a documented-overpriced longshot), requiring an edge above
5.85 points at the registered turnover k = 1: 5.73 points at 91c rising to 5.97
points at 99c.**

Why nothing else is in it:

| excluded | reason |
|---|---|
| the 1–10c half of the tail cell | the registered magnitudes there are **overpricing**, so a buy has the wrong sign. The exploitable expression of that same miscalibration is a NO purchase at 90–99c, already inside the named region. |
| the eight non-tail deciles | **no effect magnitude is registered outside the tail cell.** Supplying one would violate standing rule 5. |
| the exit-before-resolution route | it clears the band top at 95c by 0.0015 while the registered FX base understates cost by 0.00195 at that price. Its margin is inside its own slack. |

### What must travel with this verdict

1. **The surviving region is the top 2.15 of the band's 6.0 points, and no cited
   source places a magnitude there at that bucket.** The magnitudes cited at
   91–99c are 2.0 and 3.0 points; both fail. The only one large enough is
   Krause's 7.7 points at an exploitable price of 88.3c — the 81–90 decile,
   outside the cell the band is registered for.
2. **The band's top has no n.** Bürgi sets the bottom with 313,972 prices;
   Krause sets the top and the registration records no sample size for it.
3. **BAND-OPEN is not a finding that an edge exists.** It is a finding that cost
   alone does not close the question, so the power gate is still worth firing.

**The power gate fires next over 91–99c held to resolution, and over no other
region.** It is not designed here.
