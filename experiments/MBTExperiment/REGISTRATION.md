# REGISTRATION — MBTExperiment Stage B

**Written before any figure was measured.** Section 0 was committed before the
harness read a single quote, and Sections 1 onward before any quote was stored.
The commit hashes are the evidence, and `progress.md` carries the stage prompt
verbatim as it was received.

**What this registration authorizes: nothing.** It fixes what will be measured,
how, and what each result will mean, so that none of those can be chosen after a
number is seen.

---

## Section 0 — The outcome map, the gates, and the premium basis

### 0.1 Three terminal states, not two

This stage builds a harness. It does not settle the question, and it registers a
state that says so rather than borrowing one that overclaims.

| state | fires when |
|---|---|
| **HARNESS-READY** | the harness builds; **all five guards fire under mutation**; the **known-answer test reproduces an independently checkable margin**; and the census is **armed with its projected completion date** |
| **HARNESS-BLOCKED** | **any** of those fails, or account permission is absent |
| *(neither)* | — |

**This stage can never reach HARVESTABLE-CONFIRMED or VENUE_BLOCKED.** Both
require the MARGIN gate to fire, and the MARGIN gate requires a U-prefixed
session that the paper-only clause forecloses. A stage that cannot reach a
verdict must not register one as available, because a registered-but-unreachable
outcome is an invitation to reach for it.

**HARNESS-BLOCKED is an expected outcome and a fully acceptable one.** It is not
a failure of the stage. VRPExperiment reached a qualified block by refusing to
open an account rather than by estimating what an account would have shown, and
this stage holds the same line everywhere the account it has cannot answer.

### 0.2 The two gates, with thresholds quoted from VRPExperiment's handover

Both thresholds are **quoted**, not re-derived. Their source is
`docs/HANDOVER.md` in VRPExperiment, read across the read-only boundary and
hashed before and after.

#### Gate MARGIN

> **PASSES when the initial margin on a short MBT option sits at or below 12.80%
> of the $7,812.46 notional, being $1,000 per contract.**

Quoted reason: *"Below this a $1,000 sleeve holds fewer than one position and the
route is capital-blocked."*

#### Gate COST

> **PASSES when the absent legs at the pessimistic (90th-percentile) end — being
> the option bid-ask, the future bid-ask, and the CME exchange and regulatory
> fees — sit at or below the registered ceiling of Section 0.6.**

VRPExperiment's handover states the ceiling as **49.61 bps of notional**. Section
0.6 registers a **different** ceiling, on a stated basis, and registers both so
the choice stays visible.

**Both PASS gives HARVESTABLE-CONFIRMED. Either FAIL gives VENUE_BLOCKED,
unqualified, and the question is finished.** Neither happens in this stage.

### 0.3 The MARGIN gate is registered `Absent(no_live_session)` for this stage

**It is not fired, not estimated, and not softened into a pass.**

A margin is a property of the **account**. Reading one requires a session on a
U-prefixed account, and no live Gateway session runs in this repository. Two
operator constraints are recorded rather than worked around:

1. **The machine's internal fans are not functioning**, so concurrent live and
   paper sessions are not run.
2. **No separate live profile exists for this project yet.**

**An absent gate is a recorded state carrying its reason.** It is never an
unfired gate quietly omitted from a verdict table, and never a paper figure
promoted to stand in for a live one. `mbt.gates.fire` handed an `Absent` returns
`GateOutcome.ABSENT` carrying the reason, and `mbt.gates.require_admissible`
raises `PaperFigureInadmissibleError` on any paper-tagged margin. Both are pinned
by test and demonstrated as artifacts under `reports/guards/`.

### 0.4 The three provenance kinds, registered separately

They are registered separately because **they are not equally blocked**, and
merging them is exactly how a paper margin gets promoted into a live verdict.

| kind | it is a property of | provenance it carries | admissible from paper |
|---|---|---|---|
| **margin** | the **ACCOUNT** | the account prefix read back from the session | **no.** Needs a U-prefixed session |
| **quote** | the **MARKET DATA FEED** | the subscription state and the tick delay status | **yes, if real-time.** See 0.5 |
| **commission report** | the **FILL** | the commission report itself | **no.** Paper fills are simulated and their reports synthetic |

The three are `ProvenanceKind.MARGIN`, `ProvenanceKind.QUOTE` and
`ProvenanceKind.COMMISSION_REPORT` in `src/mbt/provenance.py`, and
`mbt.gates.require_admissible` branches on the kind rather than on the
environment alone.

### 0.5 The admissibility of a paper-sourced quote is an ASSUMPTION, not a measurement

**The claim.** A quote taken on a paper session is admissible to the COST gate,
provided the tick is real-time, because **IBKR routes market data by subscription
rather than by account type**. The subscription attaches to the user, and the
paper and live sessions of one user see the same feed.

**What would falsify it.** Any one of:

- a paper session serving a delayed tick on an instrument the live session serves
  in real time;
- a paper session serving a quote whose touch differs from the live session's at
  the same instant on the same instrument;
- IBKR documenting or serving a distinct paper market-data routing.

**How it is treated until then.** Every census figure is labelled
**DOCUMENTED, NOT MEASURED** wherever it is reported. `mbt.gates` attaches that
label to the result of every paper-sourced quote it admits, in the
`admissibility_note` field, so the label travels with the number rather than
living only in this document.

**It is re-verified against a live session whenever one becomes available.** The
standing rule is that measured beats documented. This one is currently
documented, and it is recorded as such rather than quietly promoted.

### 0.6 The premium basis, fixed here, before any spread is measured

**This is the load-bearing decision of the stage.**

#### The two candidate bases

| basis | premium figure | statistic | half of it | less p90 commission | **ceiling** |
|---|---|---|---|---|---|
| **A. full sample** | 142.740 bps, n = 1,955 | one-sided **95% lower bound** | 71.370 | − 21.760 | **49.610 bps** |
| **B. most recent quarter** | 112.72 bps, n = 491 | **point estimate**, p = 0.018 | 56.360 | − 21.760 | **34.600 bps** |

**Both ceilings are registered so the choice stays visible to any reader.** The
arithmetic is pinned in `src/mbt/registry.py` and checked by test, so a mistyped
digit breaks the build.

#### The decision

> **Basis B is fixed. The registered COST ceiling is 34.600 bps of notional.**

#### The reasoning, in mechanism terms

**A short variance seller collects the premium in force over the tenor they
hold, not the average of the sample's history.** The registered hedging rule
holds a 30-day tenor, so the quantity the ceiling must leave room inside is the
premium prevailing over the next 30 days.

The mechanism that disqualifies the full-sample figure is that **the sample is
non-stationary by its own measurement**. VRPExperiment measured BTC decaying
**monotonically across all four quarters — 284.53, 250.59, 145.13, 112.72 bps, a
60.4% fall — with n = 488, 488, 488 and 491.** A monotone decline across every
partition is a trend, not noise around a stable mean. **The mean of a trending
series describes its history rather than estimating its next value**, so using
the full-sample figure as the premium a future seller collects assumes a
stationarity the same sample refutes. VRPExperiment's own handover says so
directly: *"Do not read the BTC premium as stationary."*

This reasoning is stated in mechanism terms and not in expected-result terms. It
does not rest on any belief about how wide the MBT spread will turn out to be,
and it would be the same argument if the spread were known to be one basis point.

#### The qualification, stated rather than buried

**The two bases are not like for like, and the asymmetry runs against the
choice made.** 142.740 bps is a **one-sided 95% lower bound** and already carries
a confidence haircut. 112.72 bps is a **point estimate** and carries none.
Swapping one for the other changes the level and the confidence treatment
together, so basis B is more conservative in level and **less** conservative in
confidence.

**The like-for-like figure is `Absent(not_recorded)`.** VRPExperiment records
p-values for the four quarters and no confidence bounds, so the most recent
quarter's own one-sided 95% lower bound does not exist in the closed repository.
Computing it here would require re-reading a spent 1,955-day sample, which this
repository does not do.

**The direction the gap runs is nonetheless known, and it is the safe one.** A
one-sided lower bound is never above its point estimate. The most recent
quarter's lower bound is therefore **at or below 112.72 bps**, so a like-for-like
basis would give a ceiling **at or below 34.600 bps**. **The registered ceiling
is an upper bound on the like-for-like ceiling: it is, if anything, too generous,
and it cannot be too strict.** A COST gate that PASSES against 34.600 bps might
not pass against the unmeasured like-for-like figure; one that FAILS against
34.600 bps would fail against it too.

#### What this forecloses

**Selecting a basis after seeing a spread measurement voids this registration.**
Not weakens it: voids it. Choosing after seeing the number is the exact move a
registration exists to foreclose, and the two ceilings differ by 15.010 bps,
which is a wide enough gap that a post-hoc choice could decide the gate on its
own.

`REGISTERED_PREMIUM_BASIS` in `src/mbt/registry.py` names basis B, and
`tests/test_registration.py` pins both it and the two ceilings against this
document.

---

## Section 1 — VRPExperiment Sections 4.1, 4.2 and 4.3, transcribed verbatim

**Transcribed rather than paraphrased.** A paraphrase of a sampling rule is a new
sampling rule. The text below is quoted from
`~/Documents/GitHub/VRPExperiment/REGISTRATION.md`, read across the read-only
boundary and hashed before and after this stage.

### 1.1 VRPExperiment 4.1 — What must be measured, never carried

> Only for venues classified **PERMITTED** in TASK 3:
>
> 1. **Quoted bid-ask on the specific option series that would be traded** —
>    the ATM series at the 30-day tenor, not a proxy instrument — sampled across
>    **at least 20 distinct observation windows**, reported as **median, 90th
>    percentile, and the full distribution, each with its `n`**.
> 2. **Exchange and broker commission**, verified against the **live** schedule on
>    the retrieval date, recorded verbatim with its URL.
> 3. **The cost of the delta hedge** on the reachable futures contract, measured
>    **the same way** — bid-ask across ≥ 20 windows plus commission.
> 4. **The number of rebalances a registered hedging rule would require, with the
>    cost of each.** The hedging rule is registered in 4.3 below, before any data.

### 1.2 VRPExperiment 4.2 — How cost is reported

> All-in round-trip cost is reported **as a fraction of notional** and **as a
> fraction of premium collected**, at **both a central and a pessimistic end**,
> with **the statistic assigned to each end registered here, before anything
> downstream is computed**:
>
> | end | option leg | hedge leg | commission | rebalance count |
> |---|---|---|---|---|
> | **central** | **median** half-spread | **median** half-spread | live schedule | the registered rule's **median** count |
> | **pessimistic** | **90th percentile** half-spread | **90th percentile** half-spread | live schedule | the registered rule's **90th percentile** count |
>
> **This is the ORB lesson, named.** ORBExperiment carried a slippage band from a
> different instrument (QQQ) onto US single names; when the band was finally
> measured on the traded instrument, **five of six legs were understated**, the
> resulting shift was **0.467065 USD/share against a carried 0.041455 — 11.27
> times larger** — and the closure flipped. One leg (the central stop exit,
> 0.033529 measured against 0.040 carried) was **overstated**, and ORB recorded it
> because a measurement is not a reduction. **This registration carries no cost
> figure from anywhere.**

**The central and pessimistic assignment is fixed upstream and is not reopened
here.** Central takes the median, pessimistic takes the 90th percentile. This
stage inherits the assignment and does not re-derive it, re-argue it, or sweep it.

### 1.3 VRPExperiment 4.3 — The registered hedging rule

> Registered before any data so the rebalance count is not a free parameter:
>
> > **Delta-hedge the short ATM straddle on the reachable futures contract, resized
> > whenever the position delta moves more than ±0.10 from flat, evaluated once per
> > calendar day at the fixed UTC instant of Section 2.5, over the 30-day tenor.**
>
> The ±0.10 band and the daily evaluation are both **registered choices, not
> optima**. Per MLCryptoEngine ADR-034, a rebalancing band is a **trade-off between
> bounded capital and bounded trading cost** and is therefore **swept and reported,
> never chosen**: the count is additionally reported at **±0.05 and ±0.20** as a
> sensitivity, with the ±0.10 figure as the registered primary.

### 1.4 The measured rebalance counts, carried

Measured by VRPExperiment TASK 6 inside the sealed read, **n = 1,955 paths per
asset**. Carried here as measurements, never recomputed.

| quantity | value | n |
|---|---|---|
| rebalances at the registered ±0.10 band, median | **11** | 1,955 paths |
| rebalances at the registered ±0.10 band, 90th percentile | **16** | 1,955 paths |
| **BTC maximum** | **20** | 1,955 paths |
| ETH maximum, recorded for completeness | 22 | 1,955 paths |
| rebalances at the swept ±0.05 band, median | 17 | 1,955 paths |
| rebalances at the swept ±0.20 band, median | 5 | 1,955 paths |
| structural maximum a daily rule can reach over 30 days | 29 | a property of the rule, not a path |

**This repository measures no ETH figure.** The ETH maximum is recorded because
omitting it from a table that carries the BTC one would misrepresent the source.

---

## Section 2 — The commission figures, ported as measured

**Measured by VRPExperiment against the live IBKR Canada schedule on
2026-08-30**, lowest volume tier (≤ 1,000 contracts per month), where Tiered and
Fixed rates coincide. Ported here as measurements. **Nothing below is
recomputed**, and no figure is carried from any other repository.

| figure | value |
|---|---|
| commission per MBT contract, lowest volume tier | **USD 0.85** |
| straddle round trip, four contract fills, 4 × $0.85 = $3.40 | **4.352 bps of notional** |
| one rebalance fill on the MBT micro future | **1.088 bps of notional** |
| **all-in on commission alone, central** (straddle + 11 rebalances) | **16.320 bps** |
| **all-in on commission alone, pessimistic** (straddle + 16 rebalances) | **21.760 bps** |

Both all-in figures are pinned by identity in `tests/test_registration.py`:
`4.352 + 11 × 1.088 = 16.320` and `4.352 + 16 × 1.088 = 21.760`.

**The commission is not the all-in cost, and IBKR's own schedule says so**, in
the text VRPExperiment recorded verbatim: *"non-member exchange and regulatory
fees are applied, unless a client is pre-qualified by IBKR."* That leg is the
subject of Task 6 and is `Absent(not_served)`.

---

## Section 3 — What Sections 4.1 to 4.3 leave to an implementer, fixed here

**Each of these is a place where a quiet wrong answer produces a valid-looking
straddle either way.** None is a detail. All are fixed before any chain was
enumerated and any quote stored.

### 3.1 The reference price that "at the money" is measured against

> **The at-the-money reference is the midpoint of the MBT front future's touch at
> the observation instant.** Not an index level, not the option's own underlying
> field, and not a spot price from a third party.

**Mechanism.** The straddle is delta-hedged with that future. A strike chosen
against any other reference is not delta-neutral against the instrument that
actually hedges it, so the registered hedging rule would begin from a non-zero
delta and its rebalance count would no longer be the count that was measured.

**If the future's quote is refused for any reason in 3.4, the whole straddle is
refused.** No reference price means no at-the-money strike, and one is never
substituted.

### 3.2 The at-the-money strike selection rule

> **The listed strike minimising the absolute distance from the reference price.
> At a tie, the LOWER strike.**

**Mechanism for the tie rule.** Two equidistant strikes are equally
at-the-money, so the choice between them is **arbitrary by construction**. What
matters is not which is chosen but that it is chosen **before any chain is
enumerated**, so it cannot be made after seeing which of the two quotes tighter.
Registering the arbitrary choice is the whole function of registering it.

The artifact records whether the tie rule fired, so a reader can see it was
exercised rather than merely present.

### 3.3 The 30-day tenor resolution rule

> **The listed expiry minimising the absolute distance from 30 days, measured
> from the observation instant to the expiry's SETTLEMENT INSTANT, not to
> midnight. At a tie, the LONGER tenor. An expiry already past is excluded.**

**Mechanism for measuring to the settlement instant.** CME crypto options settle
at a contract-specific time, not at midnight UTC. Two expiries on the same
calendar day have different tenors, and calendar-day arithmetic reports them as
identical. `tests/test_chain.py` contains a case constructed so the two rules
**disagree** — 29.75 days against 30.458 days on one calendar date — so the test
fails if the implementation ever reverts to calendar days.

**Mechanism for the tie rule.** The registered hedging rule evaluates delta once
per calendar day **over a 30-day tenor**, and the rebalance counts carried in 1.4
were measured over exactly that path. A tenor shorter than 30 days truncates the
path and offers fewer evaluation points than the rule those counts came from. At
a tie the longer tenor is the one the registered 30-day path fits inside.

**Rounding direction, stated plainly:** the rule rounds to **nearest**, and only
at an exact tie does it round **up**.

### 3.4 The refusal conditions

> **A leg is refused, and with it the whole window, when any of the following
> holds. Each is a typed absence carrying its reason, never a number.**

| condition | test | typed reason |
|---|---|---|
| **unquoted leg** | bid or ask absent at the observation instant | `Absent(unquoted_leg)` |
| **crossed book** | bid strictly greater than ask | `Absent(crossed_book)` |
| **zero bid** | bid at or below zero | `Absent(zero_bid)` |
| **stale timestamp** | venue stamp trails local capture by more than **5.0 seconds** | `Absent(stale_timestamp)` |
| **delayed tick** | IBKR market data type 3, or any unreported status | `Absent(delayed_tick)` |
| **frozen tick** | IBKR market data type 2 or 4 | `Absent(frozen_tick)` |

**The order of the checks is registered and is not incidental.** Structure is
checked before staleness, and staleness before delay. A crossed book on a delayed
feed is reported as **crossed**, because the book being broken is the more
specific fact and the one a reader needs first. Reporting it as merely delayed
would hide that the venue served something impossible.

**An unreported tick status is treated as inadmissible, never as real-time.**
IBKR silently downgrades to delayed data when no subscription covers an
instrument, so "no status" and "delayed" fail the same way by design.

**A refused window is recorded with its reason and is never dropped.** Dropping
refusals to reach 20 would turn the count into a selection, and the selection
would be on exactly the book states the refusal conditions identify as unusual.

**No gap is ever filled by widening a figure from another venue.** See Section 4.

### 3.5 What makes two observation windows distinct, in clock terms

> **Two observation windows are distinct if and only if their local capture
> instants differ by at least 60 MINUTES, and at most 4 windows are drawn from
> any one UTC CALENDAR DAY.**

Stated in clock terms rather than in count terms, as required.

**Mechanism for the 60 minutes.** An option book's touch persists over minutes.
Two samples inside an hour re-measure one book state, inflating `n` without
adding information, and an inflated `n` makes a 90th percentile look better
determined than it is.

**Mechanism for the 4-per-day cap.** Without it, 20 windows could all be drawn
from one afternoon, and the 90th percentile would describe the tail of a single
session rather than the tail across sessions. The cap forces the sample across at
least **five collection days**.

**The consequence, which is why Task 5 is clock-bound.** 20 windows at 4 per day
is **5 collection days minimum**. The census cannot be compressed below that by
any amount of effort, and the projected completion date follows from the first
day a session exists, not from the day the harness was built.

**A missed window is a gap in a discrete sample and is recorded as one, never
backfilled.** Because the machine's internal fans are not functioning, the census
runs as **discrete sampling with the session closed between windows**, never as a
resident collector.

### 3.6 What is deliberately NOT fixed here

Recorded so that a later reader does not mistake an absence for an oversight.

- **The central and pessimistic assignment.** Fixed upstream in VRPExperiment 4.2
  and inherited. Not reopened.
- **The ±0.10 delta band.** A registered choice, not an optimum. Swept at ±0.05
  and ±0.20 and reported alongside, never selected between.
- **The exchange and regulatory fee.** `Absent(not_served)`. Task 6 determines it
  or records it absent, and does not estimate it.

### 3.7 The trial grid, counted, and its deflation

**A registration that does not count its own degrees of freedom has not
constrained them.**

| degree of freedom | choices available |
|---|---|
| premium basis | 2 — full sample, most recent quarter |
| delta band as primary | 3 — ±0.05, ±0.10, ±0.20 |
| central/pessimistic assignment | 2 — median/p90, or swapped |
| at-the-money strike tie rule | 2 — lower, higher |
| 30-day tenor tie rule | 2 — shorter, longer |

**Discrete combinations: 2 × 3 × 2 × 2 × 2 = 48.** Three further tolerances are
continuous rather than discrete: the staleness tolerance, the window spacing, and
the windows-per-day cap.

> **Deflation: every one of the 48 is fixed above, before any quote is stored,
> and each of the three continuous tolerances is pinned to a single registered
> value. The grid deflates to 1. Nothing is left selectable.**

The sweeps at ±0.05 and ±0.20 are **not** a re-expansion of the grid: they are
reported alongside the registered primary as a sensitivity, and no result is read
off them.

---

## Section 4 — Deribit is REFERENCE ONLY and is never substituted

> **Deribit's measured BTC straddle round-trip quoted spread of 22.50 bps
> (medians, n = 24 observation windows per leg, 96 observations, zero unquoted)
> is REFERENCE ONLY. It may never be substituted for a CME spread, and no gate
> in this repository reads it.**

**Deribit prohibits Canadian residents.** Its restricted-jurisdictions page,
stamped `2026-03-19T16:49:36Z`, lists "Canada" bare, with none of the narrowing
qualifiers five other entries carry. **A venue a British Columbia resident may
not use has no cost in this experiment; it does not have a cheap cost.**

**This rests on VRPExperiment ADR-008**, quoted:

> **Decision.** Measure it, label it **REFERENCE ONLY, not a cost input**, and let
> no verdict read it.
>
> **Consequence.** This is the ORBExperiment lesson applied in advance rather than
> in hindsight: a band carried from a different instrument understated **five of
> six legs** and produced a shift **11.27× too small**, while *over*stating a
> sixth — so "assume worse" would not have rescued it either.

**The sixth leg is the part that matters most and is the easiest to forget.**
Because one leg was *over*stated, a reader cannot rescue a carried band by
assuming the carried figure is merely optimistic. A carried band is wrong in both
directions at once, which is why it is refused rather than adjusted.

**What this forecloses in this stage, concretely.** If the census falls short of
20 windows, or if legs are refused, the shortfall is reported as a shortfall. It
is never topped up from Deribit, from MLCryptoEngine's futures measurements, from
tick-size modelling, or from a comparable instrument.

---

## Section 5 — The operator prior

> **RESERVED — EMPTY.**

This slot exists for the calibration ledger and blocks nothing in this stage. If
the operator records a prior before the census completes, it is scored alongside
the assistant's; if not, **the absence is recorded as an absence rather than
backfilled.**

VRPExperiment's handover notes that its own assistant prior *"resolved in favour
of the branch it weighted — but for a partly wrong reason"*, and that **a prior
which gets the branch right through a wrong mechanism should not be scored as a
clean hit.** That note is carried here as the standard this slot would be scored
against.
