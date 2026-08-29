# A.2 TASK 4 — the power gate, computed

**Run 2026-08-29.** `alpha_adj = 0.02532057`, one-sided, per co-primary.
**Session counts come from `orb.calendar`, not from the prompt.** Every figure
below is reproduced in code; **where the computation disagrees with the prompt,
the computation wins**, as Section 9 requires.

## The table

| assumption | annual Sharpe | horizon | n | t | **E1 power** | min N for 80% | E2 power |
|---|---:|---|---:|---:|---:|---:|---|
| published (undecayed) | 2.81 | holdout to 2026-06-30 | 875 | 5.2361 | **0.9995** | 250 | `Absent` |
| published (undecayed) | 2.81 | projected to 2026-12-31 | 1,003 | 5.6060 | **0.9999** | 250 | `Absent` |
| published (undecayed) | 2.81 | projected to 2027-06-30 | 1,126 | 5.9398 | **1.0000** | 250 | `Absent` |
| **REGISTERED (half)** | **1.40** | **holdout to 2026-06-30** | **875** | **2.6087** | **0.7435** | **1,006** | `Absent` |
| **REGISTERED (half)** | **1.40** | projected to 2026-12-31 | 1,003 | 2.7930 | **0.7991** | 1,006 | `Absent` |
| **REGISTERED (half)** | **1.40** | projected to 2027-06-30 | 1,126 | 2.9594 | **0.8425** | 1,006 | `Absent` |
| quartered | 0.70 | holdout to 2026-06-30 | 875 | 1.3044 | **0.2578** | 4,021 | `Absent` |
| quartered | 0.70 | projected to 2026-12-31 | 1,003 | 1.3965 | **0.2884** | 4,021 | `Absent` |
| quartered | 0.70 | projected to 2027-06-30 | 1,126 | 1.4797 | **0.3175** | 4,021 | `Absent` |

## What the table says

**The registered expectation of DEGRADED is confirmed by computation.** Section 0
registered, before any measurement existed, that the arithmetic pointed to
DEGRADED. It does, and the two clauses fire exactly:

- **E1 power at the published magnitude is 0.9995**, comfortably above the 0.80
  GO floor and far above the 0.50 BLOCKED floor;
- **E1 power at the registered assumption is 0.7435**, below the 0.80 GO floor.

That is the DEGRADED clause word for word: *"E1 reaches at least 80 percent power
at the published-magnitude assumption but under 80 percent at the registered
assumption."*

**The shortfall is 131 sessions.** The registered assumption needs **1,006**
sessions for 80 percent power; the holdout holds **875**.

**And a knife-edge worth recording exactly.** Extending the holdout to
**2026-12-31** gives **1,003 sessions and power 0.7991** — short of 0.80 by
**0.0009**, and short of the required 1,006 by **three sessions**. Extending to
**2027-06-30** gives 1,126 sessions and **0.8425**, which clears. **Three trading
days separate a design that reaches its registered power target from one that
does not**, and that is now recorded before anyone is holding a result that
would make the extension tempting.

**At the quartered assumption nothing works at any horizon** — 0.2578 rising only
to 0.3175 by mid-2027, all far below the 0.50 BLOCKED floor. If the true effect
is a quarter of the published one, this design cannot detect it on any sample
this repository can reach.

## Two disagreements with the prompt, the computation winning

| quantity | prompt | **computed** | why |
|---|---:|---:|---|
| sessions to clear t = 2.0 at Sharpe 1.40 | 514 | **515** | at n = 514 the statistic is **1.9994**, which does not clear 2.0 |
| sessions to clear t = 3.0 at Sharpe 1.40 | 1,157 | **1,158** | at n = 1,157 the statistic is **2.9998**, which does not clear 3.0 |
| holdout t at the registered assumption | 2.62 (at n = 880) | **2.6087** (at n = **875**) | the session count is computed from the calendar |

**The prompt's figures are floors; a minimum-N is a ceiling.** The disagreement
is one session in each case, in the conservative direction. **No verdict row
moves**: 2.6087 still sits above the 2.50 holdout gate and below the 3.0
factor-zoo hurdle, which is the openly registered shortfall of ADR-005.

## E2 power — a recorded absence, not a number

**`Absent(not_yet_measured)` at every assumption and every horizon.** Section 9
restricts the E2 dispersion input to the **pre-period carve-out**, and A.1 TASK 1
measured **0 of 9 vendors serving a bar to this repository**. A dispersion is not
invented here; the absence refuses coercion to a number, so it cannot be summed
into a power figure by accident.

## Per-trade power, non-binding — and what the prompt's figure hides

At 20 names per session over 875 holdout sessions:

| trigger rate | trades | IR needed for t = 3.0 |
|---:|---:|---:|
| 1.000 | 17,500 | **0.0227** |
| 0.750 | 13,125 | 0.0262 |
| **0.535** | **9,362** | **0.0310** ← matches the prompt's stated 0.031 |
| 0.500 | 8,750 | 0.0321 |
| 0.250 | 4,375 | 0.0454 |

**The prompt's "per-trade information ratio near 0.031" embeds an unmeasured
trigger rate of roughly 53.5 percent** — and the prompt itself says the trigger
rate is *"to be measured rather than assumed."* The figure is reported here with
the assumption it contains made explicit. **The portfolio-day series remains the
binding constraint**, as Section 9 states: trades inside a session share that
session's market factor, which is why E2 permutes on session labels.
