# TASK 6 — The exchange and regulatory fee leg

**Outcome: `Absent(not_served)`, for three independent reasons, and the leg
cannot be completed by this repository in either environment.** No fee is
estimated from a rule of thumb, inferred from a third party, or carried from
another repository.

---

## 6.1 The determination, which needed no session

The task asks whether the paper what-if response carries a fee breakdown. **It
does not, and this is answerable structurally rather than empirically.**

Measured against the locked `ib_async 2.1.0`, the complete `OrderState` field
list is:

```
status, initMarginBefore, maintMarginBefore, equityWithLoanBefore,
initMarginChange, maintMarginChange, equityWithLoanChange,
initMarginAfter, maintMarginAfter, equityWithLoanAfter,
commission, minCommission, maxCommission, commissionCurrency,
warningText, completedTime, completedStatus
```

**One commission triple, and no exchange or regulatory fee field of any kind.**
There is therefore **no fee breakdown to record**, with or without a session. The
response has no place to report one.

## 6.2 Three independent reasons, each sufficient on its own

Recorded separately because fixing any one leaves the leg absent.

| # | reason | consequence |
|---|---|---|
| **1** | **The API response has no fee field.** `OrderState` cannot express one. | No breakdown exists to read, in any environment. |
| **2** | **Paper fills are simulated and their commission reports synthetic.** A fee read from a paper execution measures the **simulator**, not CME. | Even a fee-bearing paper response would be a fact about the paper environment, not about the venue. |
| **3** | **CME's own schedule is `Absent(not_served)`.** CME refused automated access citing its own Data Terms of Use, verbatim: *"This IP address is blocked due to suspected web scraping activity… Use of scripts, software, spiders, robots… is strictly prohibited by CME Group's website Data Terms of Use."* | VRPExperiment obeyed that refusal rather than working around it, and this repository obeys it too. |

**A venue's own refusal binds and is obeyed rather than routed around.** That is
VRPExperiment ADR-003 and it is not relitigated here.

## 6.3 What is NOT established, stated because it is easy to overread

**The absence of a fee field does not prove the fee is absent from the scalar
`commission` value.** It proves only that the response **cannot distinguish**
them. IBKR's published schedule states plainly that *"non-member exchange and
regulatory fees are applied, unless a client is pre-qualified by IBKR"*, which
says they are additional, and IBKR separately states its fees *"are intended to
cover the costs of execution, including exchange fees"*, which cuts the other
way.

**The two statements are in tension and this repository does not resolve them.**
Resolving it would require a live fill and its commission report, which is
`Absent(no_live_session)` on top of everything above. The narrower question
"is the scalar `commission` fee-inclusive in the paper simulator?" is recorded
`Absent(gateway_unreachable)` and is, in any case, a question about the simulator.

## 6.4 The direction the bound errs, and by how much the ceiling overstates the room

**Every absent cost leg is non-negative, so the measured legs form a strict
LOWER BOUND on the true cost, and the bound errs in the PERMISSIVE direction:
the true cost is at least the bound and may be much higher.**

Stated as the task requires, with the magnitude:

> **The fee leg is `Absent(not_served)`, the resulting bound errs permissively
> because every absent leg is non-negative, and the registered 34.600 bps ceiling
> therefore overstates the room available to the measurable spread legs by
> exactly the unmeasured fee `F ≥ 0` — a quantity this repository can bound below
> at zero and CANNOT bound above by any evidence it holds.**

**"By how much" has no numeric answer here, and supplying one would be the
estimate the task forbids.** What can be stated exactly is the *form* of the
overstatement: the room available to the spread is `34.600 − F` bps, not 34.600
bps, and `F` is unmeasured.

### There is a second absent leg pushing the same way

VRPExperiment recorded, verbatim from IBKR, that the broker charges a daily
**"Exposure Fee"** and that *"Testing has indicated that short positions in low-
priced options generate the largest exposures relative to the amount of
capital."* **A short option book at this broker can attract a daily charge that
is neither commission nor spread, and the broker names short options as its
largest generator.** Its magnitude is account-specific and `Absent(not_served)`.

**So the bound errs permissively in at least two known directions, not one.**

## 6.5 The structural consequence: the COST gate becomes one-sided

This is the load-bearing consequence of the absent fee, and it is implemented
rather than described.

The COST gate compares `option_spread + future_spread + fee ≤ ceiling`. With
`fee` a recorded absence, **the sum cannot be formed at all**: `Absent` refuses
addition, and `tests/test_guards.py::test_summing_a_measured_leg_with_an_absent_one_raises`
provokes exactly that refusal and records it in `reports/guards/refusals.json`.

The measured legs still constrain the answer, as a strict lower bound.
`mbt.gates.fire_lower_bound` uses it as one:

| lower bound versus ceiling | outcome | why |
|---|---|---|
| **above** the ceiling | **FAIL** | the true cost is at least the bound, so it exceeds the ceiling too. Sound. |
| at or **below** the ceiling | **ABSENT** | nothing follows. The absent legs are non-negative and unbounded above, so they could carry the total past the ceiling. |

> **The COST gate can close the question negatively and can never close it
> positively while the fee leg is absent.** It is structurally incapable of
> returning a PASS, exactly as the MARGIN gate is structurally incapable of
> firing without a U-prefixed session.

**Both gates are therefore blocked from PASS, for different and independent
reasons.** The stage's terminal state is over-determined: even a complete
20-window census on a real-time paper feed could not produce
HARVESTABLE-CONFIRMED, because the fee leg would still be absent.

`tests/test_guards.py` pins that no lower bound at or below the ceiling ever
returns PASS, across four values including the ceiling itself.

## 6.6 What would complete this leg

Not a code change, and not obtainable by this repository:

1. **CME's published exchange and regulatory fee schedule for MBT options**, read
   by a person rather than fetched by a script, since CME's Data Terms of Use
   refusal binds automated access and is obeyed.
2. **A live fill and its commission report**, which is `Absent(no_live_session)`
   under the paper-only clause.

Either would complete the leg. Neither is available here, and neither is
approximated.
