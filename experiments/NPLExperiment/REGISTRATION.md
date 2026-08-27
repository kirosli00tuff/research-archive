# REGISTRATION.md — the pre-registration

> **STATUS: REGISTERED 2026-08-27, BEFORE ANY NETWORK CALL.**
>
> At the moment this document was committed, **this repository had sent no
> request to any endpoint, enumerated no instrument, and held no data of any
> kind.** The request ledger was empty. That ordering is what makes this a
> pre-registration rather than a description.
>
> **From this point the specification is closed.** Where the specification
> and reality disagree, the session reports and stops rather than choosing.
> Changing anything here requires a **new dated amendment** appended at the
> bottom, with its reason and a statement of exactly what data existed at the
> time it was made. Nothing above an amendment line is ever edited.
>
> **Disclosure.** MLCryptoEngine (HYPOTHESES.md, H5/H8/H9), solattn
> (REGISTRATION.md, progress.md), InsiderExperiment (progress.md, guard
> sources), and the solclear findings cited below were read before this was
> written, and their measured figures are carried below with their sources.
> No NPLExperiment data of any kind existed.

---

## 0. The outcome map — it judges collection feasibility, never returns

The Section 0 verdict fires in Stage A.2 Task 5 from the census, the power
computation, and the Stage A.1 access findings. **It reads no outcome value:
every input is a count-derived power or an operational verdict.**

- **GO:** all three co-primaries of Section 8 reach **at least 80 percent
  power at alpha_adj** under the registered effect assumptions, at the
  achievable event count by **2027-03-31**, and the delisting-observability
  test of A.1 Task 4 **passes in full**.
- **DEGRADED:** any power lands between **50 and 80 percent**, or delisting
  observability **passes partially**, demoting the retrospective cohort to
  descriptive with the forward cohort carrying the verdict alone. Collection
  proceeds, recomputed power stated beside the registered target.
- **BLOCKED:** any co-primary **under 50 percent power** at the achievable
  count by 2027-03-31, or listing timestamps **not inferable to plus or minus
  one day**, or funding retention **below the per-event coverage bar**
  (Section 8 / A.2 Task 2). Nothing armed beyond the census.

Enforced by `npl.section0.fire_section0`, committed with this document and
pinned by `tests/test_section0.py`, with every boundary fixture sitting on
the registered boundary. A delisting-observability FAIL is treated as the
partial case's limit: the retrospective cohort is demoted entirely and the
forward cohort carries the verdict alone, at forward-only power.

---

## 1. The hypothesis

**H-NPL.** A short opened at the registered entry anchor (Section 3) on newly
listed Hyperliquid perpetuals earns a **positive net return over 30 and 90
days**, because listing-age drift exceeds the funding the short pays plus
costs.

This is a **joint drift-plus-funding claim**, deliberately. MLCryptoEngine H8
measured, on 231 usable Hyperliquid perps over 1,182 days (4,411,046 hourly
funding observations), **+43.68 percent per year of funding income against
−42.91 percent of price return** on negative-funding perps — near
cancellation (net +0.11 percent) — so the market prices decline into funding
*when sorted on funding alone*. The claim here is that sorting on **listing
age** instead selects decline the funding market has not fully priced. The
matched control of Section 6 is what separates listing age from generic
negative-funding compensation: if young perps merely behave like
funding-matched old perps, P3 fails and the hypothesis closes.

Carried external figures, sources named, not independently verifiable live:
Delphi Consulting, 652 CEX listings since January 2025, 12 percent
profitable, median −82 percent. Animoca Research, 773 listings January to
September 2024, median −40 to −70 percent, average −49 percent. Memento
Research, 118 TGEs in 2025, 84.7 percent below listing valuation. In-house:
MLCryptoEngine H5 measured MERL funding at −22.38 and TNSR at −32.41 percent
per year, so shorts on young perps can pay materially for the position — the
funding leg is not a rounding term, which is why the outcome is net of it.

## 2. The universe and event rule

**Every perpetual listing on the Hyperliquid main dex and on every HIP-3
builder dex**, enumerated from the venue meta endpoints (`meta`, `perpDexs`,
per-dex `meta`), **birth-ordered, with no attention or performance input** of
any kind in the enumeration.

Event types, **tagged and never filtered at collection**:

- `vanilla` — a standard perp listing on the main dex.
- `hyperp_conversion` — an instrument that traded as a hyperp (pre-launch
  market) and converted to a vanilla perp. **The hyperp pre-conversion phase
  is excluded from primaries** because hyperp funding follows the venue's
  dampened formula (funding computed against a moving average of the mark
  rather than an external index, damping the very funding signal Section 4
  sums), so its funding leg is not comparable to a vanilla perp's. The phase
  is recorded as a tag, never dropped from the record. The event date for a
  conversion is the conversion date where the venue's documentation names
  it; an instrument documented as having launched as a hyperp whose
  conversion date is not inferable to plus or minus one day is
  `excluded_ineligible` for primaries and retained in the census.
- `hip3` — a listing on a HIP-3 builder dex, tagged with its dex name.

Identification rule for the tag, fixed now: `hip3` iff the instrument is
enumerated from a builder dex. `hyperp_conversion` iff the venue's public
documentation names the instrument as having launched as a hyperp; the
identification source is recorded per instrument in the census ledger.
Otherwise `vanilla`.

## 3. Listing date and entry anchor

- **Listing day** is the UTC date of the **first served 1d candle** for retro
  events (the census parses the `t` field and row count only), or the first
  watcher sighting **cross-checked against the first candle** for forward
  events. A disagreement of more than one day between watcher sighting and
  first candle is reported, and the first candle governs.
- **Entry anchor** is the **second daily close**: the close of the candle for
  UTC date `listing day + 1`, i.e. the timestamp `00:00:00Z` of
  `listing day + 2`. Every window in Section 4 anchors here.
- **Day-1 close** (the close of listing day itself) is recorded as a
  **descriptive anchor, never verdict-bearing** — it prices the listing-pop
  the entry anchor deliberately steps over.

## 4. The outcome definition

**Net short return over horizon H** (H in days, from the entry anchor):

    net_short(H) = − price_return(entry_close → close at entry + H days)
                   + Σ hourly funding a constant-notional short receives
                     over the window (entry, entry + H]
                   − registered round-trip cost (Section 5)

- **Sign convention, stated: a positive funding rate pays the short.** The
  venue's hourly `fundingRate` is the rate longs pay shorts; the short
  receives `+rate` per hour on notional, so negative funding is a cost to
  the short and enters the sum with its sign.
- **Constant notional**: the funding leg accrues on the entry notional, not
  on the marked position. Named Stage-scope simplification.
- **No compounding**: price return and funding sum are added, not
  compounded. Named Stage-scope simplification.
- **No liquidation modelling**: the short is assumed to survive to horizon
  regardless of path. Named Stage-scope simplification, and it biases the
  measured net **in the hypothesis's favour** on instruments that rallied
  hard before falling; the H8 decomposition (Section 8 secondaries) is where
  that shows up.

## 5. Costs

Round-trip cost, charged once per event, by venue class:

| class | central | band (low, central, high) |
|---|---|---|
| vanilla main-dex | **9 bp** | 3, 9, 18 |
| HIP-3 builder dex | **18 bp** | 6, 18, 36 |

Basis, carried: venue base perp fees 1.5 bp maker and 4.5 bp taker per side
(so 9 bp taker round trip; 3 bp is the all-maker bound and 18 bp a stress
bound); HIP-3 builder markets default to double fees. To be verified live in
A.1 where the venue serves fee metadata; a disagreement is recorded by
amendment before any verdict-bearing use.

**Forward events additionally record a measured touch spread at the entry
anchor** (A.3 Task 5, one l2Book fetch), **descriptive only** — it prices the
cost band's realism and moves no bar.

## 6. The matched control

At each event entry, the control is **the perp on the same dex listed at
least 180 days earlier with funding coverage, nearest by signed trailing
168-hour mean hourly funding, with replacement.**

- "Funding coverage" for a candidate: at least 95 percent of the 168 hours in
  the trailing window have served funding rows.
- "Nearest by signed" means nearest in signed value (not absolute), so a
  young perp paying −30 percent annualized is matched to the old perp
  nearest −30, separating listing age from funding level.
- Ties are broken by earlier listing date, then by coin name ascending. Both
  tie-breaks are fixed now and neither is outcome-dependent.
- **With replacement**: one old perp may serve as control for many events.
- Pairs are written to an append-only ledger **at assignment time**, with the
  event entry timestamp, the control's trailing mean, and the candidate count.
- **Matching reads no row stamped after the event entry, pinned by test**
  (`npl.blindness.funding_rows` gates the rate by the entry timestamp, and
  the matcher refuses a post-entry row loudly).

An event with no eligible candidate is recorded `no_control_candidate`,
stays in P1 and P2, and drops from P3 only, counted.

## 7. Horizons and deaths

- **30 days primary, 90 days secondary.**
- **A delisting before horizon values the event at its last served close**,
  flags it `truncated_by_delisting`, **retains it in the primaries**, and the
  count is reported beside every figure it enters. Rationale: delisting is
  disproportionately the fate of the instruments the hypothesis is about, and
  dropping them manufactures survivorship — solclear Finding 2 measured that
  mechanism at 60 points of death-rate gap.
- **Events younger than their horizon at read time are `pending`, never
  partially filled.** A pending event enters no figure.

## 8. Inference

Three co-primaries, distribution-free, one-sided, at
**alpha_adj = 1 − 0.95^(1/3) = 0.016952 (0.0170)** each. **All three must
pass for the Stage B GO row.**

- **P1, profitability share.** Exact binomial (Clopper–Pearson) lower
  confidence bound at level alpha_adj on the share of events with **positive
  30-day net short return**; the bar is the bound **at or above 0.60**.
  Registered power assumption: true share **0.85**.
- **P2, magnitude.** Exact one-sided sign test on the share of events whose
  30-day outcome sits **at or below −15 percent net** on the asset side —
  the position moved at least 15 points net in the short's favour,
  equivalently `net_short(30) ≥ +15 percent`; the bar: that share **exceeds
  one half** at alpha_adj. Registered assumption: true share **0.65**.
- **P3, control contrast.** Exact one-sided sign test on **paired
  differentials, young net minus matched net, bar: negative.** The
  differential is taken on the **asset-side net** (the negative of Section
  4's net short return), so a negative differential means the young perp
  underperformed its funding-matched control net of funding and cost.
  Equivalently and exactly: the tested indicator is
  `young net_short(30) > matched net_short(30)`, and the bar is that its
  share exceeds one half at alpha_adj. Both statements are the same test;
  both are recorded so no sign error can creep in at Stage B. Registered
  assumption: the true share of negative differentials is **0.70**.
- **Named secondaries, descriptive and never verdict-bearing:** the 90-day
  versions of P1–P3; per-type strata (`vanilla`, `hyperp_conversion`,
  `hip3`); the forward-versus-retro split; and the H8 decomposition of every
  event's net into its funding term and its price term.

## 9. The power method

**Exact binomial power at the registered assumptions, computed in A.2 Task 4
from achieved and projected event counts. No number is invented before the
census.**

For each co-primary at sample size n: the rejection region is the smallest k*
with `P(X ≥ k* | p0) ≤ alpha_adj` (p0 = 0.60 for P1, 0.50 for P2 and P3),
and power is `P(X ≥ k* | p_true)` at the registered true shares (0.85, 0.65,
0.70). P1's formulation is the standard duality: the Clopper–Pearson lower
bound clears 0.60 exactly when the exact test of p0 = 0.60 rejects. P3's n
is the matched-pair count: `round(match_rate × N)` with the A.2 Task 3
measured match rate. Computed at achieved retro N, at combined N by
2026-12-31, and at combined N by 2027-03-31, with the minimum N clearing 80
percent stated for each.

## 10. The Stage B trigger

Stage B runs only when **all** of:

1. all three co-primaries at or above **80 percent power at achieved
   eligible N** (not projected),
2. the operator prior slot of Section 13 **filled and labelled** independent
   or adopted,
3. **explicit operator instruction**.

**Stage B opens the sealed outcomes exactly once.** `verdict.py` is built
dark in A.3 against synthetic fixtures and is never pointed at real sealed
data before that single registered read.

## 11. The epistemic boundary

A positive result supports the claim that **the registered short would have
cleared its bars on this sample**. It is never a forward return prediction,
never an expected-value claim about future listings, and never a trading
recommendation. Stage A produces no tradeable artifact at all.

## 12. Spend and pacing

**Zero dollars.** Keyless public endpoints only. The request ledger charges
before sending, cap **20,000 requests per UTC day**, refusals loud and
counted. Pacing figures are **deferred to A.1 measurement** (the solattn
lesson: ceilings are per endpoint, never per host, and measured never
assumed) and are recorded by amendment if they move any registered figure.

## 13. Priors

**Assistant priors, recorded 2026-08-26 in chat, before any census:**

- 0.20 that a real capturable edge exists overall.
- 0.40 that the Stage B bars clear on the registered sample.

**The adoption warning, standing:** the NPD Amendment 0 lesson applies — an
adopted prior corrupts the calibration ledger. The assistant's numbers above
are context, not the operator's number, and they must not be copied into the
slot below.

**The operator prior slot, reserved and empty:**

> Operator prior on the Stage B bars clearing: _reserved — empty. The
> operator fills this line by replacing everything after the colon with a
> probability and a label._

The accepted formats for the fill are a probability in [0, 1] followed by
`(independent)` or `(adopted)` — nothing else parses. **The empty slot blocks
Stage B structurally** (`npl.registration_check.require_operator_prior`,
exercised by `tests/test_registration_check.py`).

---

## Amendments

None yet. An amendment is dated, reasoned, states exactly what data existed
when it was made, and never edits anything above its own line.

### Amendment 1 — 2026-08-27 — the event date gains a funding cross-check, the pre-epoch era is censored, and the hyperp tag becomes mechanical

**What data existed when this amendment was made.** Stage A.1 access,
rate-ceiling, retention, and delisting telemetry only: timestamps, row
counts, HTTP statuses, and the request ledger (897 requests). **No census
row existed, no event had been enumerated, no eligibility had been
computed, no power number existed, and no outcome value of any kind had
been read** — the blindness readers served every probe, so no candle price
and no post-entry funding value has ever been parsed by this repository.
The figures behind this amendment are in docs/ACCESS.md Tasks 3 and 4.

**The measured facts that force it** (n = 12 retention instruments, 6
delisted instruments):

1. The venue serves **index-backfilled 1d candles predating its own funding
   archive epoch of 2023-05-12T00:00Z** — majors' candles begin in 2020. A
   first served 1d candle is therefore NOT a listing date for instruments
   whose candles reach the epoch.
2. For **every probed instrument listed after the epoch (7 of 7)**, the
   first 1d candle, first 1h candle, and first funding row agree on the
   same UTC day — Section 3's inference holds, but only with the funding
   cross-check attached.
3. **UNIBOT's candles begin 49 days before its first archived funding row
   and CYBER's 10 days** — a pre-vanilla phase trading without archived
   funding, mechanically visible. Section 2's documentation-based hyperp
   identification found no machine-readable source; this signature is the
   better instrument and cannot be fitted to outcomes, because it reads
   timestamps only.

**The amended rules.**

1. **Listing day (Section 3), amended:** the listing day of an event is the
   UTC date of its first served 1d candle, **cross-checked against the UTC
   date of its first archived funding row. The two must agree within the
   registered tolerance of one day** for the instrument to carry a
   `vanilla` (or `hip3`) event tag with that listing day.
2. **Epoch censoring (new):** an instrument whose first funding row lands
   exactly at the archive epoch 2023-05-12T00:00Z, or whose first candle
   predates the epoch, is **epoch-censored**: its venue listing date is not
   inferable to plus or minus one day, it is `excluded_ineligible` as an
   event (counted), and it **remains usable as a Section 6 control**, with
   its listing date treated as at-or-before its first candle (a lower
   bound suffices for the 180-day age rule).
3. **The hyperp tag (Section 2), amended to mechanical:** an instrument
   whose first funding day exceeds its first candle day by **more than one
   day** is tagged `hyperp_conversion`, its recorded pre-vanilla phase
   running from first candle to first funding row. **Its event date for
   primaries is its first funding day** — the start of the funded vanilla
   phase, which is the phase the hypothesis is about — and the entry anchor
   is the second daily close from that day. The documentation-based rule of
   Section 2 remains as a supplementary source where documentation exists;
   the mechanical signature governs.
4. **Section 12 pacing figures, recorded as measured** (docs/ACCESS.md
   Task 2): operating paces per endpoint — meta 0.8 s, metaAndAssetCtxs
   0.8 s, perpDexs 1.6 s, candleSnapshot 5.3 s, fundingHistory 1.4 s,
   l2Book 0.5 s — each at half its measured ceiling where one was found
   (perpDexs ~79/min; candleSnapshot ~23/min at 5,000 rows) and half the
   highest verified-clean rate where none was (`npl.pacing`). Funding pull
   cadence: daily, 500-row pages, ~19 days of catch-up margin.

**What is unchanged.** The universe rule, the entry anchor's second-daily-
close definition, the outcome definition, costs, the control rule, horizons
and deaths, all of Section 8's bars and assumptions, the power method, the
Stage B trigger, and the priors. The census (A.2 Task 1) now records the
first funding timestamp beside the first candle timestamp for every
instrument, reading times and counts only.

**The bias direction, stated now.** Epoch censoring removes only the
oldest instruments from the event set — instruments whose listing predates
the archive by construction cannot have a measurable funding leg, so
nothing measurable is lost. The mechanical hyperp rule moves conversion
events' anchors LATER (to the funded phase), which shortens their drift
runway and, if anything, biases the measured listing-age effect toward the
null. A negative on the conversion stratum carries that caveat; a positive
is not inflated by it.

### Section 0 verdict record — 2026-08-27, fired at Stage A.2 Task 5

**Verdict: GO. Cohort basis: retro plus forward. Collectors are armed.**

Recorded here in the amendment log as Section 0 requires, with every input
figure beside it. No outcome value was read at any point; every input is a
count, a timestamp, or a registered assumption.

- Census: **503 instruments** enumerated (232 main dex, 271 across 10 HIP-3
  dexs), 450 with served candle history, 449 with served funding, 179
  flagged delisted, 53 with no served candles.
- Retro-eligible events: **N = 312** (112 vanilla, 46 hyperp_conversion by
  the Amendment 1 mechanical tag, 154 hip3), of which 10 are
  truncated_by_delisting and retained. Pending (younger than horizon): 62.
  Excluded: 129 — epoch_censored 74, no_candles 53, no_funding_rows 1,
  died_before_entry 1. **The funding-coverage bar excluded zero measured
  events** (312 of 312 measured windows at or above 0.95).
- Delisting observability: **PASS in full** (A.1 Task 4, 6 of 6 probed
  delisted perps serve candles and funding).
- Listing dates: inferable to ±1 day via the Amendment 1 candle-funding
  cross-check (7 of 7 post-epoch probes agree same-day).
- Funding retention: 90-day retro windows servable (archive reaches the
  2023-05-12 epoch or the listing; 500-row pages).
- Control feasibility: **176 of 312 events (56.4 percent)** have at least
  one same-dex candidate aged 180+ days by census dates; the 136 unmatched
  (young HIP-3 dexs, mostly) stay in P1 and P2 and drop from P3 only.
- Projection: trailing 182-day rate **18.5 events/month** (vanilla 0.5,
  hip3 18.0); combined N **430 by 2026-12-31**, **485 by 2027-03-31**;
  forward-only N by the deadline 173.
- Exact binomial power at alpha_adj = 0.016952, registered assumptions
  (0.85 / 0.65 / 0.70):
  - achieved retro N = 312, pairs = 176: **P1 1.000, P2 0.9993, P3 0.9995**
  - combined by 2026-12-31 (430 / 243): P1 1.000, P2 0.99999, P3 0.99999
  - combined by 2027-03-31 (485 / 274): P1 1.000, P2 0.999997, P3 0.999998
  - forward-only by 2027-03-31 (173 / 98): P1 0.99999998, P2 0.9704, P3 0.9755
  - minimum N clearing 0.80: **P1 34 events, P2 103 events, P3 60 pairs.**
- Section 10 note: the achieved eligible N already clears every co-primary
  power bar, so the earliest Stage B date is bounded by the sealed-data
  backfill and the two operator conditions (the prior slot and explicit
  instruction), not by sample accrual.

Inputs produced by: docs/ACCESS.md (A.1), the census ledger
(data/census/census.jsonl, 503 rows), the A.2 eligibility assessments, and
npl.power at the registered assumptions. Fired by npl.section0.fire_section0.
