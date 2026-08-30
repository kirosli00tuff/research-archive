# REGISTRATION — VRPExperiment Stage A

**Registered 2026-08-30, before any network call.** Commit `8bcc5bf` is the last
commit before this file; no probe, fetch or measurement precedes it.

This repository runs **one stage**, produces **one artifact**, and **closes**. It
is not a ladder. No capital is deployed, no order is placed, no venue is joined.

---

## Section 0 — The outcome map

Three branches. Each is judged on **reachability and cost**, and **never on
returns**. No sleeve is simulated anywhere in this repository, so no branch can
be reached by a return figure.

### HARVESTABLE

The measured premium is **positive at the registered significance** (Section 6),
**and** its magnitude exceeds the **measured all-in round-trip cost** on at least
one **lawfully reachable** venue (Section 3) by the **registered margin**
(Section 5).

Consequence: a successor sleeve becomes worth registering — **in its own
repository, on its own registration**. **This repository still closes.** Nothing
here becomes a deployment.

### VENUE_BLOCKED

The premium is **positive and material**, **and** no lawfully reachable venue
clears the cost hurdle at the sleeve size — whether because every venue offering
the instrument **prohibits** Canadian residents, because every permitted venue is
**capital-blocked** at roughly $1,000, because every permitted venue lists **no
option product**, or because the measured cost on every permitted venue exceeds
the premium.

Consequence: **a documented answer and a citable artifact.** This is a real
result, not a failure to get one. The distinction between *prohibited*,
*capital-blocked*, *no product* and *cost-exceeded* is recorded, because they are
four different findings and only the first is a jurisdiction fact.

### SIGNAL_ABSENT

The premium is **not distinguishable from zero** at the registered significance,
**or is negative**.

Consequence: the cost side becomes irrelevant and is reported anyway, because it
was measured and a measurement is not a reduction.

### Precedence

If the premium fails Section 6, **SIGNAL_ABSENT fires regardless of the venue
finding.** The premium is the endpoint; reachability qualifies it. If the premium
passes, the branch is decided by Section 3 and Section 5 jointly.

---

## Section 1 — The hypothesis

> **A variance risk premium exists in BTC and ETH at a 30-day tenor, is positive
> and material, and at least one venue lawfully reachable by a British Columbia
> resident permits harvesting it at an all-in round-trip cost below that premium
> by the margin registered in Section 5.**

This is a **joint claim**, and both conjuncts must hold for HARVESTABLE. It is
registered as a conjunction deliberately: a premium that exists but cannot be
reached is the *expected* outcome (see Section 9), and the point of registering
the conjunction is that its failure mode is informative rather than null.

**Registered expectation: VENUE_BLOCKED.**

---

## Section 2 — The measured quantity

Every element below is fixed **before any data is read**. Changing one after
TASK 6 voids the hypothesis.

### 2.1 Tenor

**30 calendar days.** One tenor, both assets, no sweep. Chosen because it is the
horizon at which a model-free implied volatility index is published for both BTC
and ETH, which makes the implied leg an *observed* series rather than one this
repository constructs; and because a 30-day window is short enough that a
$1,000 sleeve's holding period is a plausible object and long enough that the
realized leg has 30 daily returns in it.

### 2.2 The implied-volatility estimator

**Primary: the exchange-published 30-day model-free implied volatility index
(Deribit DVOL) for BTC and for ETH, sampled from the public API.** DVOL is a
constant-30-day, model-free implied volatility computed by the exchange from its
own option book, quoted in **annualised volatility points** (percent).

**Fallback, registered now so it is not chosen later:** if and only if the index
is not served with the depth registered in Section 2.5, the implied leg is
constructed from **option-level mark implied volatility** at the two expiries
bracketing 30 days, interpolated **linearly in total variance against
time-to-expiry**, taken at the **at-the-money-forward** strike. The fallback is
recorded as used or not used; it is never blended with the primary.

### 2.3 The realized-volatility estimator

**Close-to-close annualised realized volatility.** Named explicitly:

> For each observation date `t`, take the 30 daily log returns
> `r_i = ln(P_i / P_{i-1})` over the 30 calendar days **following** `t`, compute
> the sample standard deviation with `ddof = 1`, and annualise by `sqrt(365)`.
> Crypto trades every calendar day, so the annualisation factor is 365 and not
> 252, and the daily closes are taken at the **same UTC instant** as the implied
> observation.

This is the plain close-to-close estimator, not Parkinson, not Garman-Klass, not
Yang-Zhang, and not a realized-variance sum over intraday returns. The choice is
registered because the estimator changes the number: high-low estimators are
more efficient but read differently in a market with venue-specific wicks, and
picking the efficient one after seeing the answer would be a free parameter.

**The realized leg is strictly forward-looking from the implied observation.**
Realized volatility over the 30 days *preceding* `t` is a different quantity and
is not the subtrahend. This is the single most common way the measurement is got
wrong, and it is pinned here.

### 2.4 Sign convention

> **`VRP_t = IV_t − RV_{t→t+30}`, in annualised volatility points.**

**A positive VRP means the option market charged more volatility than the
underlying subsequently delivered — a seller of variance was paid.** A negative
VRP means the seller was not paid. The sign is stated in words as well as symbols
because a sign error here inverts the verdict.

**Secondary, in variance units:** `VRP²_t = IV_t² − RV²_{t→t+30}`, reported
alongside, because the literature's "variance risk premium" is more often stated
in variance units and a reader outside this program will want the comparison.
**The primary endpoint is the volatility-points form**, because it is the form
that converts to a cost in basis points without a second modelling step.

### 2.5 Sampling frequency and window

- **Implied leg:** one observation per calendar day, at a **fixed UTC instant**,
  recorded with its timezone. The instant is fixed at the first read and never
  moved.
- **Realized leg:** daily closes at the same fixed UTC instant.
- **Registered minimum depth:** **730 daily observations per asset** (two years)
  for the primary analysis. If served depth is shorter, the analysis runs on what
  is served, `n` is reported in the same sentence as every figure, and the
  shortfall is recorded as a limitation rather than padded.
- **Registered minimum for any reported figure:** **60 observations.** Below
  that, `Absent(insufficient_sample)` is recorded and no number is printed.

### 2.6 The conversion to basis points, registered before any number exists

The premium is in volatility points and the cost is in basis points of notional.
They are made comparable by **one registered conversion**, stated here so it
cannot be chosen later:

> For an at-the-money straddle of tenor `T` years, the Black-Scholes price is
> approximately `sqrt(2/π) · S · σ · sqrt(T)`. A delta-hedged short straddle held
> to expiry therefore earns approximately
> **`edge_bps = sqrt(2/π) · sqrt(T) · (IV − RV) · 10,000`**
> basis points of underlying notional.
>
> At `T = 30/365 = 0.082192`, `sqrt(T) = 0.286691` and `sqrt(2/π) = 0.797885`, so
> **`edge_bps = 2,287.5 × (IV − RV)`** with `(IV − RV)` in decimal volatility
> points. **One volatility point of premium is 22.875 bps of notional.**

Three properties of this conversion are registered as limitations, not
discovered later. It **assumes continuous delta hedging** and so overstates a
discretely hedged position. It **assumes an at-the-money straddle** and does not
describe any other structure. It is a **first-order approximation** and drifts
for large `(IV − RV)`. It is used for **comparability only**; the premium itself
is reported in volatility points, which is the measured quantity.

---

## Section 3 — Venue set and reachability criterion

> **POPULATED BY TASK 3. NOT BEFORE.**
> **This section registers the criterion. It registers no venue and no figure.**

### 3.1 The reachability criterion

A venue is **PERMITTED** only if **all** of the following hold, each evidenced by
**published text recorded verbatim with its URL and its date**:

1. The venue's published restricted-jurisdictions policy does **not** exclude
   Canadian residents, **and** does not exclude British Columbia specifically.
2. The venue lists an **option product** on BTC or ETH.
3. Access requires **no proxy, no VPN, and no misrepresentation of residence**.

A venue is **PROHIBITED** if its published policy excludes Canadian residents or
British Columbia. **This is a measured finding and is never worked around.**

A venue is **CAPITAL_BLOCKED** if it is permitted and lists the product, but a
**$1,000** sleeve supports **fewer than one position** at the venue's own
contract size and margin. Capital-blocked is **distinct from prohibited** and
both are **distinct from reachable**.

A venue is **UNCLEAR** if published policy does not resolve Canada or British
Columbia either way. **UNCLEAR is a recorded state and is never read as
permission.** An unclear venue cannot support HARVESTABLE.

A venue is **NO_PRODUCT** if it is reachable but lists no option product.

### 3.2 What TASK 3 must record for each permitted venue, each with its `n`

Contract size · minimum order increment · notional at current spot · initial
margin for a short option position · maintenance margin for the same · number of
positions a $1,000 sleeve supports.

### 3.3 Candidate venue set, registered now, findings later

Deribit · CME options on Micro Bitcoin (MBT) and Micro Ether (MET) futures
through Interactive Brokers Canada, tested for **Canadian retail permissioning**
and not merely for US listing · CME Bitcoin (BTC) and Ether (ETH) options at full
size · Canadian-listed covered-call or volatility crypto ETFs · CIRO-registered
Canadian venues offering crypto options · Hyperliquid and any other BC-reachable
perpetual venue, tested for whether an **options product has listed since
2026-07**.

The set may be **extended** by TASK 3 if a candidate is found. It may not be
**narrowed**.

### 3.4 What is registered as carried, and therefore re-verified

Two figures enter this section as **dated measurements from another repository**
and are **re-verified live in TASK 3 before use**, per ADR-055. If
re-verification disagrees, **the measurement wins** and the disagreement is
recorded.

- MLCryptoEngine ADR-034 (2026-08-04): Hyperliquid at 3.0 bps round trip is the
  cheapest BC-reachable venue and the only one offering a short; it lists
  **perpetuals, not options**.
- Deribit's restricted-jurisdictions policy **dated 2026-03-19** prohibiting
  Canadian residents. **TASK 3 verifies this policy is still current and records
  the retrieval date.**

**Neither is registered as a finding here.** They are registered as claims to be
tested.

---

## Section 4 — The cost model

> **POPULATED BY TASK 5. NOT BEFORE.**
> **No carried figure is registered in this section. None.**

### 4.1 What must be measured, never carried

Only for venues classified **PERMITTED** in TASK 3:

1. **Quoted bid-ask on the specific option series that would be traded** —
   the ATM series at the 30-day tenor, not a proxy instrument — sampled across
   **at least 20 distinct observation windows**, reported as **median, 90th
   percentile, and the full distribution, each with its `n`**.
2. **Exchange and broker commission**, verified against the **live** schedule on
   the retrieval date, recorded verbatim with its URL.
3. **The cost of the delta hedge** on the reachable futures contract, measured
   **the same way** — bid-ask across ≥ 20 windows plus commission.
4. **The number of rebalances a registered hedging rule would require, with the
   cost of each.** The hedging rule is registered in 4.3 below, before any data.

### 4.2 How cost is reported

All-in round-trip cost is reported **as a fraction of notional** and **as a
fraction of premium collected**, at **both a central and a pessimistic end**,
with **the statistic assigned to each end registered here, before anything
downstream is computed**:

| end | option leg | hedge leg | commission | rebalance count |
|---|---|---|---|---|
| **central** | **median** half-spread | **median** half-spread | live schedule | the registered rule's **median** count |
| **pessimistic** | **90th percentile** half-spread | **90th percentile** half-spread | live schedule | the registered rule's **90th percentile** count |

**This is the ORB lesson, named.** ORBExperiment carried a slippage band from a
different instrument (QQQ) onto US single names; when the band was finally
measured on the traded instrument, **five of six legs were understated**, the
resulting shift was **0.467065 USD/share against a carried 0.041455 — 11.27
times larger** — and the closure flipped. One leg (the central stop exit,
0.033529 measured against 0.040 carried) was **overstated**, and ORB recorded it
because a measurement is not a reduction. **This registration carries no cost
figure from anywhere.**

### 4.3 The registered hedging rule

Registered before any data so the rebalance count is not a free parameter:

> **Delta-hedge the short ATM straddle on the reachable futures contract, resized
> whenever the position delta moves more than ±0.10 from flat, evaluated once per
> calendar day at the fixed UTC instant of Section 2.5, over the 30-day tenor.**

The ±0.10 band and the daily evaluation are both **registered choices, not
optima**. Per MLCryptoEngine ADR-034, a rebalancing band is a **trade-off between
bounded capital and bounded trading cost** and is therefore **swept and reported,
never chosen**: the count is additionally reported at **±0.05 and ±0.20** as a
sensitivity, with the ±0.10 figure as the registered primary.

### 4.4 If no venue is permitted

**Record `Absent(venue_blocked)` with the TASK 3 finding, and synthesize
nothing.** No modelled spread, no assumed commission, no "representative" venue.
An unreachable venue has no cost; it does not have zero cost. Guard 1 enforces
this structurally: `Absent` refuses `float()`, `int()` and every arithmetic path.

---

## Section 5 — The margin

> **Registered before any number exists, and justified here rather than after.**

**For HARVESTABLE, the lower bound of the premium's one-sided 95% confidence
interval must exceed the PESSIMISTIC end of the all-in round-trip cost by a
factor of 2.0.**

Written out: `premium_CI_lower_bps ≥ 2.0 × cost_pessimistic_bps`.

### Why 2.0, and why against the pessimistic end

Three sources of downward error on the premium and upward error on the cost are
**known to exist and are not measured by this repository**. The margin is sized
to cover them jointly, and each is named so the margin can be attacked.

1. **Quoted spread is not effected spread.** TASK 5 measures the *quoted*
   bid-ask. A real fill also pays queue position and market impact. MLCryptoEngine
   H3 measured **adverse selection positive on every one of 28 surveyed
   instruments (+0.06 to +0.68 bps)**, and its every net was an upper bound
   "because it credits every quote with a fill that queue position has not
   earned". The same applies here and is not measured.
2. **The rebalance count is a rule, not an observed path.** Section 4.3 registers
   a hedging rule and counts what it would have required. A live book rebalances
   on gaps, halts and margin calls the rule does not model.
3. **The conversion of Section 2.6 assumes continuous hedging.** A discretely
   hedged short straddle earns **less** than `sqrt(2/π)·sqrt(T)·(IV−RV)`, by an
   amount that grows with the gap between hedges. The premium side is therefore
   an **upper bound** on what is capturable.

A factor of **2.0** is deliberately modest against ORB's measured **11.27×**
carry error, and that is the point: ORB's error was a *carry* error and this
repository carries nothing, so the residual is sampling and mechanism error
rather than instrument-substitution error. A larger margin would be unfalsifiable
theatre; a smaller one would let a premium that is entirely queue position and
discrete-hedging drag read as HARVESTABLE.

**Applying it to the pessimistic end rather than the central end** follows from
the same three items: all three push in the same direction, so the central end is
not a central estimate of what a sleeve would pay.

### The corresponding VENUE_BLOCKED condition

If the premium clears Section 6 but **no permitted venue** satisfies
`premium_CI_lower_bps ≥ 2.0 × cost_pessimistic_bps`, **VENUE_BLOCKED fires**, and
the artifact records **which of prohibited / capital-blocked / no-product /
cost-exceeded** applies to each venue separately.

---

## Section 6 — Inference

**A single one-sided test at α = 0.05, on the premium.**

- **H₀:** `mean(VRP) ≤ 0` — the option market did not charge above subsequent
  realization.
- **H₁:** `mean(VRP) > 0`.
- **Test:** one-sided t-test on the mean of the daily `VRP_t` series, per asset.
- **Standard errors:** **Newey–West HAC with bandwidth 30**, because the realized
  leg uses **overlapping** 30-day forward windows on daily sampling, which
  induces serial correlation by construction. Using an IID standard error here
  would be the exact defect ORBExperiment's audit A3 found in its own census
  intervals, where independence assumptions made intervals **2–17× too narrow**.
  **Registered before any data, not after an audit.**
- **Robustness, registered now:** the same test on **non-overlapping** 30-day
  windows, which is IID by construction at the cost of `n/30` observations. Both
  are reported with their own `n`. **If they disagree in sign or significance,
  the disagreement is the finding and neither is suppressed.**
- **Two assets, and why that is still one endpoint:** BTC and ETH are reported
  separately, each against α = 0.05. The **hypothesis endpoint is "a variance
  risk premium exists in BTC and ETH"**, and Section 0 fires on it as a single
  claim.

### The Berger 1982 note, recorded

> **No multiplicity correction applies to a single endpoint.** Section 1 is a
> **conjunction** — a premium exists **and** a venue is reachable — and Berger
> (1982) gives an intersection-union test **the full nominal level per
> component**: to reject the null of the conjunction, *every* component must
> reject, so the test is conservative at level α without any adjustment. This is
> the same correction ORBExperiment made in its Amendments 18–21, where a union
> correction had been applied to a conjunction and was wrong.
>
> Applying a Bonferroni or Benjamini-Hochberg correction here would **lower**
> the level below nominal for no inferential reason and would make a
> SIGNAL_ABSENT verdict easier to reach than the design intends.

---

## Section 7 — Power

### 7.1 Effect sizes are halved

Per **McLean and Pontiff (2016)**, published anomaly returns decay by roughly
half post-publication — 26% attributable to publication itself and the remainder
to statistical bias. **Every effect size in this section is reported at both the
published magnitude and half of it, and the halved figure is the one the design
is judged against.**

### 7.2 Why the endpoint is the premium and not a strategy return

Recorded explicitly, because it is the reason this repository measures what it
measures:

> A **strategy-Sharpe endpoint of 1.32 annualised** would need **roughly 119
> weekly observations to reach t = 2** — from `t ≈ SR·√(years)`, so
> `years = (2/1.32)² = 2.296`, and `2.296 × 52 = 119.4` weeks. **At the halved
> 0.66 it would need roughly 478** — `years = (2/0.66)² = 9.183`, and
> `9.183 × 52 = 477.5` weeks, **more than nine years**.
>
> Nine years of weekly observations on an instrument whose venue may not be
> reachable at all is not a measurement this repository can make. **The premium
> is a per-observation quantity with daily sampling and a two-year registered
> depth; a strategy Sharpe is a per-period quantity needing a decade.** That is
> the whole reason the endpoint is the premium.

### 7.3 Power on the registered endpoint

At the registered depth of **730 daily observations per asset** with **Newey–West
bandwidth 30**, the effective independent sample is approximately
`730/30 ≈ 24` non-overlapping windows. Against a one-sided α = 0.05, detecting a
premium of `d` standard deviations needs `n ≈ (1.645 + 0.842)² / d² = 6.19/d²`
independent observations for 80% power. **At 24 effective observations the
detectable standardised effect is `d ≈ 0.508`; at the halved effect size the
same design detects `d ≈ 1.016` only with `n ≈ 6` — that is, the halved-effect
design is powered only if the premium is large.**

**This is registered as a known limitation of the design, before any data.** If
the measured premium is small relative to its dispersion, **SIGNAL_ABSENT is the
correct verdict and will be reported as such**, and the artifact will state that
a null here is a statement about this sample's power as much as about the world.

---

## Section 8 — Epistemic boundary

> **A positive result establishes that a premium existed on this data, at this
> tenor, by these named estimators, and that it exceeded a cost measured at a
> point in time on a specific venue.**
>
> **It is never evidence that a sleeve would have been profitable, because no
> sleeve is simulated here.**

What this repository does **not** measure, listed so the artifact cannot be
misread:

- **No strategy is backtested.** No position is opened, held, or closed in any
  simulation. There is no equity curve, no drawdown, no Sharpe.
- **No fill is modelled.** The cost is a *quoted* spread plus a *scheduled*
  commission. Queue position, partial fills, and market impact are absent.
- **No margin path is simulated.** Section 3 records the initial and maintenance
  margin at a point in time; it does not simulate a margin call.
- **No tail is measured.** A short-variance position's defining risk is the move
  that does not appear in a two-year sample. **The premium is compensation for
  exactly that risk, so measuring the premium without the tail measures the
  payment and not the liability.** This is the single largest thing this
  repository does not know, and it is stated here rather than in a footnote.
- **Cost is a point-in-time measurement.** Fee schedules and margins are dated
  measurements, not constants (MLCryptoEngine ADR-012, ADR-055).
- **A venue policy is current as of its retrieval date and no longer.**

---

## Section 9 — Priors

Recorded before any measurement.

### 9.1 Assistant prior

| branch | prior |
|---|---|
| **HARVESTABLE** | **0.12** |
| **VENUE_BLOCKED** | **0.76** |
| **SIGNAL_ABSENT** | **0.12** |

**Reasoning, recorded so the prior can be scored rather than admired.** The
premium side is the easy half: an implied-minus-realized wedge in BTC and ETH is
widely reported as positive and large, and the mechanism — hedgers paying for
convexity — does not require any inefficiency, so `SIGNAL_ABSENT` gets only 0.12,
and most of that 0.12 is **power** rather than a genuinely absent premium
(Section 7.3 shows the design detects only a large effect at the halved size).
The venue side is where the mass sits: Deribit is the venue with the option book
and is believed to prohibit Canadian residents; CME lists MBT and MET options but
a **$1,000 sleeve against a $6,505 MBT notional** is unlikely to support one
short-option position at exchange margin, which points at CAPITAL_BLOCKED; and
Hyperliquid, the one venue ADR-034 records as BC-reachable and short-capable,
**lists perpetuals rather than options**. `HARVESTABLE` at 0.12 is mostly the
probability that a Canadian-listed volatility ETF or a CIRO-registered venue
turns out to offer something measurable that this program has not previously
looked for.

### 9.2 Operator prior

> **RESERVED — EMPTY.**

**This slot does not block anything in a single-stage census.** It exists for the
calibration ledger. If the operator records a prior before TASK 6, it is scored
alongside the assistant's; if not, the assistant's is scored alone and the
absence is recorded as an absence rather than backfilled.

### 9.3 The ORBExperiment calibration outcome, recorded as context

> **Assistant 0.15 and operator 0.30 both resolved against a NO on H1, and
> neither had priced the spread.**

Both priors were directionally correct and **both were correct for the wrong
reason**. Neither had priced the transaction-cost side: the closure came from a
measured entry half-spread of **0.076572 USD per share (n = 550 minutes served,
0 refused, p90 0.333662)** on the traded instrument, against a band carried from
QQQ that understated five of six legs and produced a shift **11.27 times** too
small.

**The lesson carried into this registration, explicitly:** the cost side is
registered as a **measurement obligation** (Section 4) rather than a modelling
assumption, carries **no figure from anywhere**, and the margin of Section 5 is
applied to its **pessimistic** end. The assistant's 0.76 on VENUE_BLOCKED is a
prior that has *learned this specific lesson*, which is precisely why it should
be scored strictly: a prior that is high because it finally priced the thing it
missed last time is only calibrated if the thing actually binds.

---

## Amendment log

No amendments. Any amendment is appended here with its date, its reason, and the
commit that introduced it. **No section above is edited in place.**
