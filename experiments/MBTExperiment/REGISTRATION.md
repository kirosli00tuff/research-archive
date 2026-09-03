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
