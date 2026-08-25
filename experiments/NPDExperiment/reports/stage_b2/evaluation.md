# Stage B.2. The one-shot evaluation

Run 2026-08-25T20:10:48.471253+00:00. Once.

Gate model `gpt-5-2025-08-07`. Sealed store read one time, by one module.

---

## Amendment 0, recorded before any outcome was read

Operator prior: **0.05**

The operator adopted the assistant prior of 0.05 rather than forming an
independent one. The calibration ledger shows it as **adopted, not
independent**, because an adopted prior carries no information about the
operator own judgment and would corrupt the calibration record if logged as
his.

**This experiment yields no evidence about the operator calibration.** One
prior was recorded, not two.

---

## Task 2. The pipeline validity gate

The registered negative control. Stored rankings shuffled within each day,
10,000 draws, scored against the sealed forward returns.

**This detects pipeline defects, not model contamination.** A non-zero
shuffled IC means the scorer, the join, or the label mapping is wrong, and
every downstream number would be an artifact. It is not a contamination
clearance and a later reader must not read it as one.

| quantity | value |
|---|---|
| shuffled mean daily rank IC | **+0.0001** |
| Monte Carlo 95 percent interval on that mean | -0.0001 to +0.0003 |
| spread of the null distribution, sd | 0.00925 |
| null distribution 2.5 to 97.5 percentile | -0.0179 to +0.0181 |
| registered tolerance | 0.02 |

**Gate verdict: PASS.** The shuffled mean sits inside the registered
tolerance of zero. The scorer, the join, and the label mapping behave as a
valid pipeline must under randomization, so the numbers below are
computed on a pipeline that has been shown to produce zero when it should.

---

## Task 3. The primary contrast

Primary horizon, next-5-session return. **404 evaluable days.**
6 days dropped because a name in the panel carried no
realized return. The absence is recorded and the day is dropped, never filled.

### Mean daily rank IC

| series | mean daily rank IC |
|---|---|
| **model**, `gpt-5-2025-08-07` | **+0.0061** |
| baseline `mom_12_1` | +0.0222 &larr; best |
| baseline `logistic` | -0.0058 |
| baseline `sign_last` | -0.0255 |

**Best baseline: `mom_12_1`.** It was designated after the fact, as
the baseline with the highest mean daily rank IC in the window. Selecting it
this way is **conservative**, because it picks the hardest of the three
baselines for the model to clear rather than the easiest. It raises the bar,
it never lowers it. Recorded as ADR-010.

### The contrast

Model mean daily rank IC minus best-baseline mean daily rank IC.
Day-clustered moving-block bootstrap, 10,000 resamples,
block length 10, two-sided at t 2.0.

| quantity | value |
|---|---|
| **primary contrast** | **-0.0161** |
| interval | -0.0673 to +0.0351 |
| excludes zero | **False** |
| bootstrap standard error | 0.02562 |
| daily contrast sd | 0.36339 |

No family correction applies. This is one pre-registered contrast on one
pre-registered model, and the registration states why: the hypothesis was not
selected from a sweep. It was written before any output existed.

### Power that actually existed

| quantity | value |
|---|---|
| achieved effective sample size | **201.2** independent-equivalent days |
| realized minimum detectable contrast | **0.0512** |
| registered projection | 0.026 to 0.047 |

The result is read against the power that existed, not the power that was
hoped for.

---

## Task 4. The permutation null

Within-day permutation of the model outputs, 10,000 resamples, drawn
independently of the gate in Task 2 so the two questions do not share a
sample.

| quantity | value |
|---|---|
| observed model mean daily rank IC | **+0.0061** |
| null mean | -0.0002 |
| null sd | 0.00926 |
| null 2.5 to 97.5 percentile | -0.0184 to +0.0177 |
| **two-sided p** | **0.5174** |

---

## Task 6. The verdict, fired once

| registered row | fired |
|---|---|
| beats coin and beats every baseline | no |
| beats coin, does not beat the baselines | no |
| does not beat coin | **YES** |

### Verdict: does not beat coin

**the replication confirms the council negative under frontier capability and sane formulation. Closed.**

Supporting tests:

| test | result |
|---|---|
| model IC above zero | +0.0061, interval -0.0276 to +0.0397, significant: **False** |
| contrast above zero | -0.0161, interval -0.0673 to +0.0351, significant: **False** |

**Which kind of null is this.** The verdict row is as registered. Read
descriptively against the realized power:

This is an **underpowered unresolved**, not a tight null. The realized
minimum detectable contrast is 0.0512, so effects below that
magnitude were never distinguishable from zero by this design.


### The epistemic boundary, verbatim

> A positive supports the claim the pipeline predicts, never the claim the
> model understands.

---

## Task 5. Secondaries and descriptives

**Everything in this section is subordinate. None of it changed the verdict
above and none of it may be read as changing it.**

### Secondary horizon, next-1-session return

| series (SECONDARY) | mean daily rank IC |
|---|---|
| model, SECONDARY | -0.0203 |
| baseline `logistic`, SECONDARY | +0.0097 |
| baseline `mom_12_1`, SECONDARY | +0.0089 |
| baseline `sign_last`, SECONDARY | -0.0315 |

| quantity (SECONDARY) | value |
|---|---|
| evaluable days | 412 |
| best baseline | `logistic` |
| contrast | -0.0300 |
| interval | -0.0677 to +0.0077 |
| excludes zero | False |
| model IC excludes zero | False |
| realized minimum detectable contrast | 0.0377 |

### Descriptive. Window halves

Residual knowledge just past a cutoff would show as early-window strength
decaying later. **This is a diagnostic and not a verdict input.** A difference
here is a flag for a future registered test, never a finding.

| half | days | model mean daily rank IC |
|---|---|---|
| first | 202 | +0.0123 |
| second | 202 | -0.0001 |
| difference, first minus second | | +0.0124 |

### Descriptive. Model against a coin, independent of the baselines

| quantity | value |
|---|---|
| model mean daily rank IC | +0.0061 |
| interval | -0.0276 to +0.0397 |
| beats a coin | **False** |

---

## What this evaluation did not do

It read the sealed store one time. It added no horizon, no baseline, no model,
and no robustness variant that the registration does not already name. It did
not modify the sealed store, the stored rankings, the frozen prompt digest,
the baselines, or any registered parameter.

**The limitation carried forward from Amendment 2.** The gate ran at `minimal`
reasoning effort on the large majority of attempts. Every statement above is a
statement about gpt-5-2025-08-07 at minimal reasoning effort, not about the
model at its best.


---

## Appendix. Reading the realized power

**This section is arithmetic on the numbers already printed above. It required
no further read of the sealed store and adds no test.**

### Why the realized detectable contrast exceeded the projection

The registration projected a detectable contrast of 0.026 to 0.047 across
assumed model-to-baseline correlations of 0.0 through 0.7. The realized figure
is 0.0512.

The reason is visible in the realized daily contrast standard deviation of
**0.36339**. The registered grid assumed a daily contrast sd of at most 0.2626,
which is the value at correlation zero when each daily IC carries the null
standard deviation of 0.185695. The theoretical maximum, reached only at
correlation minus one, is 2 times 0.185695, or 0.3714.

**The realized 0.36339 sits at 98 percent of that maximum.** The model daily
rank IC and the momentum daily rank IC are therefore strongly negatively
correlated across this window, far outside the 0.0 to 0.7 range the registration
contemplated. Two series that move against each other produce a difference with
a larger variance than either, which is what widened the interval.

This is stated as a power diagnostic. It is **not** a finding, no registered test
asks about the correlation between the model and a baseline, and it must not be
read as one.

### What the null does and does not establish

| band | covered by this design |
|---|---|
| contrast effects above 0.0512 | detectable, and none was found |
| contrast effects from 0.01 to 0.05 | **not detectable.** The entire realistic band sits below the realized threshold |

The verdict row is as registered. The honest reading beside it is that the
primary contrast **could not have detected an effect anywhere in the realistic
band**, so its null is not evidence of absence at those magnitudes.

The model-against-a-coin test is somewhat better resolved, at a half-width of
0.0337, but it too sits above most of the band.

### The window-halves diagnostic is inside noise

The first half read plus 0.0123 and the second read minus 0.0001, a difference
of 0.0124. With a daily rank IC standard deviation near 0.19 and the registered
overlap inflation of 3.4, the standard error on each half mean is near 0.025 and
on their difference near 0.035. **The observed difference is about one third of
one standard error.** It is not a decay signal. It is recorded because the
registration asked for the diagnostic, and it flags nothing.
