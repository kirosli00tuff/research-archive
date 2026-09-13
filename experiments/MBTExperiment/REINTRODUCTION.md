# REINTRODUCTION — the conditions under which this question reopens

**Written at closure, 2026-09-03, before any reopening was attempted.** Fixing
the conditions now rather than when the question feels attractive again is the
point of writing this file today.

---

## What is final and does not reopen

**The MARGIN gate FAILED at a $1,000 sleeve.** 20.837% of notional against a
registered 12.80% ceiling, exceedance 1.628x, measured against a threshold fixed
before the measurement existed. That result stands as written. **It is never
replaced by a friendlier number, revised to fit a larger sleeve, or dropped from
a verdict table.**

A different capital constraint is a **different question** and gets its own
registration in a **new repository**, exactly as solcopy got one rather than
becoming a stage appended to solattn.

## The sequencing trap, named now because it already happened once

On 2026-09-03 the operator learned the margin figure and then named $7,000 as a
tolerable sleeve. **The motivation was honest and the sequence was still
backwards.** A capital ceiling chosen after seeing what the margin looked like is
reverse-engineered, whatever the intent.

**A reopening must register its headroom rule on risk grounds, before any
measurement, and state that the sequence above occurred.** A reader who is not
told cannot discount it.

## The headroom rule a reopening must carry

Register the gate as **peak margin across a full hedged cycle at or below a fixed
fraction of the sleeve**, never as "does required margin fit". The remainder is
variation-margin cover for a short-gamma position that moves against you roughly
26% of the time and is hedged a median of 11 times per cycle.

**Fix the fraction before any trial.** A figure near half the sleeve is
defensible on risk grounds at this cadence. The number belongs to the operator;
the discipline is that it exists first.

## The arithmetic at a $7,000 sleeve, so a reopening starts informed

| | figure |
|---|---|
| notional per straddle | **$8,177.75** |
| leverage at a $7,000 sleeve | **1.17x** (against 8.18x at $1,000) |
| CME maintenance, hedge leg alone | **$1,704**, being **24.3%** of the sleeve |
| paper median, ONE short option | **$3,930.96**, being **56.2%** of the sleeve |
| paper median, BOTH short legs, before SPAN netting | **$7,861.92**, being **112.3%** of the sleeve |

**The entire $7,000 question is whether SPAN nets a short straddle enough to
fit.** Before netting, the two short legs alone exceed the sleeve. SPAN computes
portfolio risk rather than summing legs, and a straddle's two sides cannot both
lose, so the netted figure will be materially lower. **How much lower is the only
open question, and it is measurable on paper for free.**

## The economics a reopening would be buying

At the registered premium basis, the decayed most-recent quarter of **112.72 bps**:

| | per 30-day cycle |
|---|---|
| premium on $8,177.75 notional | **$92.18** |
| cost at ceiling (21.76 commission + 34.60 absent legs = 56.36 bps) | **$46.09** |
| **net at ceiling** | **$46.09** |
| twelve cycles on a $7,000 sleeve | **~$553, or 7.9% a year** |

**That is payment for bearing crash risk**, on a position needing eleven hedge
adjustments per cycle, where VRPExperiment measured the payment and states
plainly that it never measured the liability. A 5.4-year sample contains no crash
of the size a variance seller ultimately pays for. **Judge the 7.9% against
that**, not against a savings rate.

## What paper can and cannot prove, registered in advance

**Paper CAN prove margin**, because IBKR computes it. **Paper CAN prove quoted
spreads**, because market data is subscription-routed rather than
account-routed. **Paper CAN prove hedge cadence**, because the delta band is
arithmetic on real quotes.

**Paper CANNOT prove fills.** Paper executions are simulated, so realized
slippage against the quoted touch is unmeasurable there. **The entire cost model
rests on that gap.** A reopening registers this as a known unmeasurable at the
outset and never lets a clean paper cycle imply the cost band was validated.

## The order of operations, so nothing is bought before it is needed

1. **Fix the transmit invariant** (ADR-010). Free. The new rule is *stricter*
   than the old one: any order carrying `transmit=True` must carry `whatIf=True`
   as a literal, and no path may construct an order with `whatIf=False`. A sixth
   mutation follows from it.
2. **Take a paper margin read across a full hedged cycle.** Free, no
   subscription, no live session. If peak margin breaks the headroom rule, the
   route closes there and nothing is bought.
3. **Only then**, the CME crypto real-time market data subscription, which is the
   only paid step and which the census needs.

**Step 3 never precedes step 2.** Paying to price a position that cannot be held
is the error this closure exists to prevent.

## The live margin figure remains unmeasured

Every margin figure here is either CME exchange-minimum or IBKR **paper**. **No
U-prefixed session was ever opened**, so IBKR's live initial margin on a short
MBT option is unmeasured, and paper is not a substitute for it. A reopening at
any sleeve size will need that read.
