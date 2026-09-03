# CLAUDE.md — MBTExperiment operating manual

Read this file at the start of every coding session. It is the contract for how
work happens in this repository.

## What this project is (permanent, stated from the first commit)

> **MBTExperiment measures two venue facts and nothing else: the initial margin
> on a short MBT option, and the all-in bid-ask plus exchange and regulatory
> fees on the MBT straddle and its hedge leg.**
>
> **It does not measure a premium.** VRPExperiment measured that, closed on
> 2026-08-30, and is not reopened here. Its 1,955-day sample is spent and no
> figure in it is recomputed, extended, or re-read.
>
> **It transmits no order.** Every broker interaction is a `whatIf` preview or a
> market-data read. There is no path in this package that places, modifies, or
> cancels a live order, and `tests/test_guards.py` proves it by walking the parse
> tree rather than by grepping text.
>
> **It authorizes no capital.** A PASS on both gates authorizes exactly one
> thing: writing a sleeve registration in a **third** repository. It never
> authorizes a position.

## Why this repository exists rather than an edit to VRPExperiment

VRPExperiment is CLOSED with verdict VENUE_BLOCKED, qualified. Its
`docs/HANDOVER.md` names two figures as the only open items that change a
verdict, and states that settling them makes a successor worth registering in
its own repository. Editing a closed repository to add its own missing evidence
is the failure its closure discipline exists to prevent.

## The two gates, quoted from the closure

| figure | threshold | why |
|---|---|---|
| initial margin, short MBT option | **≤ 12.80% of $7,812.46 notional, i.e. ≤ $1,000/contract** | below this a $1,000 sleeve holds fewer than one position |
| absent cost legs, at p90 | **≤ 49.610 bps of notional** | half the premium's one-sided 95% lower bound (71.370) less measured p90 commission (21.760) |

Both PASS gives **HARVESTABLE-CONFIRMED**. Either FAIL gives **VENUE_BLOCKED,
unqualified**, and the question is finished.

## Paper-only, from 2026-09-02, and what it forecloses

**No live Gateway session runs in this repository until the operator lifts this
clause.** Two operator constraints, both recorded rather than worked around:
the machine's internal fans are not functioning, so concurrent live and paper
sessions are not run; and no separate live profile exists for this project yet.

The two provenance kinds are therefore separated, because they are not equally
blocked:

| figure kind | provenance carried | admissible from paper |
|---|---|---|
| **margin** — a property of the ACCOUNT | the account prefix read back from the session | **no.** Needs a U-prefixed session |
| **quote** — a property of the MARKET DATA FEED | the subscription state and tick delay status | **yes, if real-time.** IBKR routes market data by subscription, not by account type |
| **exchange and regulatory fees** | the commission report | **no.** Paper fills are simulated and their reports synthetic |

**The MARGIN gate cannot fire in a paper-only stage and is not fired.** It is
recorded `Absent(no_live_session)` with that reason, never estimated from a
paper figure and never softened into a pass.

**The COST gate's spread legs are collectible now.** Its fee leg stays
`Absent(not_served)` regardless of environment.

**The admissibility of a paper-sourced quote is a CLAIM, not a measurement.**
It rests on the feed being subscription-routed. Record it as an assumption with
that reasoning, and re-verify it against a live session whenever one becomes
available. Per the standing rule, measured beats documented, and this one is
currently documented.


## The decision Section 0 must settle before any collection

The 142.740 bps lower bound behind the 49.610 threshold is a **full-sample**
figure, and the sample decays monotonically across its four quarters:
**284.53 → 250.59 → 145.13 → 112.72 bps, a 60.4% fall.** The most recent quarter
does not support the number the bar rests on.

**Section 0 fixes the basis before any spread is measured**, records both
resulting thresholds so the choice is visible, and states its reasoning. Against
the decayed figure the room is 56.360 less 21.760, leaving **34.600 bps**.
Choosing after seeing a spread measurement is the exact move a registration
exists to foreclose.

## Non-negotiable rules

1. **No transmit, ever.** Every `placeOrder` call site must carry `whatIf=True`,
   verified by AST walk at build time. A call site without it, or with the flag
   supplied from a variable rather than a literal, fails the build. A registered
   mutation flips it to `False` and must break the suite.
2. **Environment provenance is measured, never declared.** The environment tag on
   every recorded figure is derived from the account number the session actually
   connected to, read back from the broker. A D prefix is paper, a U prefix is
   live. A session declaring `live` that connects to a D-prefixed account
   **refuses and writes nothing**. Config states an intent; the connection states
   a fact, and the fact wins.
3. **Paper figures are never verdict-bearing.** A paper margin read is
   development evidence. Any attempt to fire a gate from a figure tagged paper
   raises. Pinned by test.
4. **The deciding live reads are latched.** One spend per registered figure,
   fsynced before returning, second attempt raises `LatchAlreadySpentError`.
   Ported from VRPExperiment TASK 6.
5. **Secrets and account numbers never enter the repo.** Environment variables
   only, from `.env.example`. `config.py` raises naming the missing variable, and
   `tests/test_honesty.py` scans tracked files for both key shapes and the IBKR
   account shapes.
6. **Absence is a recorded state, never a synthesized value.** An unquoted leg, a
   crossed book, a zero bid, a missing fee line: each is a typed absence
   refusing coercion to a number.
7. **Delayed market data is inadmissible.** A delayed quote carries a stale and
   artificially wide spread. Subscription state is recorded on every observation
   and a delayed tick is refused, never widened into a cost band.
8. **Never substitute another venue's spread.** Deribit's 22.50 bps is REFERENCE
   ONLY. ORBExperiment carried a band once and understated five of six legs,
   producing a shift 11.27× too small.

## Boundaries

**First action of every session: confirm the working directory.** If the path
contains `/closed/`, or if a `_CLOSED_DO_NOT_RUN_HERE` marker sits at the root,
**stop, report the path, and take no further action.** Do not write, do not
commit, do not create a `.env`, do not run `make`. On 2026-09-02 a session was
opened in VRPExperiment by mistake and got as far as overwriting its `.env`
before stopping. Nothing was lost, and the check exists so the next one costs
even less.

Read-only source paths, hashed before and after every stage:
`~/Documents/GitHub/VRPExperiment/` in full, which relocates to
`~/Documents/GitHub/closed/VRPExperiment/` once `stage_move_closed.sh` runs.
Resolve it by locating the marker rather than by assuming either path. Nothing
in it is written, moved, renamed or deleted. Borrow its patterns by copying,
never by importing.

**Do not re-run VRPExperiment's TASK 6 read.** Its latch is spent and a second
read of that window voids its hypothesis.

**Touch no systemd unit and no timer.** AiTrader's `news-collect.timer`,
`npl-watch.timer` and `npl-daily.timer` are live and `Linger=yes` must stay
enabled. `news_experiment.db` is never opened. NPLExperiment's H2 collection is
running toward its 2026-11-26 look and is not disturbed.

**Gateway session hygiene.** A distinct client id per environment, from config.
TradingView and TWS competing for one Gateway session starve each other.

## Standing practices (defect-earned, ported by copying)

- **Measured behaviour beats documentation.** A published margin, a documented
  fee, a claimed subscription: none is believed until a probe measures it.
- **Refusals fail closed and are demonstrated, never asserted.** Every refusal is
  a produced artifact under `reports/`.
- **Known-answer tests before trusting a pipeline.** The what-if reader
  reproduces an independently checkable margin on a liquid product before its
  MBT output is believed.
- **Never trust append order across processes.** Order by the recorded clock.
- **A negative with a hidden n is not a result.** Every claim carries its sample
  size in the same sentence as its number.

## Writing

Clear, spartan, active voice. No em dashes. No semicolons. No filler adjectives.

## Git commit conventions

Conventional commits, imperative mood, lower case, no trailing period. One
deliverable per commit. Push nothing until the operator says so.

## Read these first

`REGISTRATION.md`, `README.md`, `DECISIONS.md`, `progress.md`. Every stage prompt
is logged verbatim to `progress.md` on receipt, before any file is touched.
