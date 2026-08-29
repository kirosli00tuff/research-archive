# HANDOVER.md — for a fresh session

**Read this before touching anything.**

> ## The binding constraint is a calendar.
> ## **The earliest eligible re-pull is 2026-09-12.**
> Nothing in this repository can produce a bar-integrity verdict before that
> date, and no amount of further work moves it. `tools/repull_probe.py` refuses
> every earlier attempt with exit **78**, naming the date, having sent nothing.

## What this repository tests

**One hypothesis, H1.** Among US common stocks with **elevated opening relative
volume**, a **breakout of the first 5-minute regular-session range** predicts
continuation to the session close, **net of modeled costs**, out of sample from
**2023-01-03**.

It is a **joint claim about the selection and about the breakout**, and it can
fail on either half while the other is real. In the source study the **selection
by relative volume, not the breakout, did almost all the work**: the plain
broad-universe rule returned **3.2 percent annually at Sharpe 0.48 — below
passive** — while the top-20-by-relative-volume restriction returned **more than
1,600 percent at Sharpe 2.81** (both carried, unreplicated, in-sample, from
authors who sell day-trading education).

**Stage A never trades, never touches capital, and never reads an outcome
value.** A documented negative is a valid and expected outcome.

**Precise on credentials:** the two market-data credentials are **Alpaca
paper-account keys**. The **live trading host refuses them** — `401`,
`{"code":40110000,"message":"request is not authorized"}`, measured. **No live
broker credential exists and none is planned.**

## Where it stands

**Section 0 re-fired `PENDING_REVISION` on 2026-08-29** (Amendment 10),
superseding the `PENDING_ACCESS` of Amendment 4. **Nothing is armed. Nothing is
closed. H1 is OPEN.**

| finding | figure | n |
|---|---|---|
| **credentials authenticating** | **2 of 2** | 2 |
| **primary vendor** | **Alpaca** — bar vendor, ADR-023 | — |
| **reference vendor** | **Massive** — the only source of delisting dates | — |
| **Alpaca earliest served session** | **2016-01-04** — 1,762/1,762 in-sample, 875/875 holdout | 16 probes |
| **Massive earliest served session** | **2024-08-29** — 0/1,762 in-sample, 459/875 holdout | 16 probes |
| **tape, Massive vs Alpaca-SIP** | **`SAME_TAPE`**, median **1.005197**, IQR [1.003096, 1.007726] | **100 pairs** |
| tape control, Alpaca-SIP vs Alpaca-IEX | `DIFFERENT_TAPE`, median **0.027761** | 100 pairs |
| **delisted names with intraday history** | **203** — **`PASS`**, share 0.8865 | **229 checked** |
| delisted names enumerated in window | **4,731** of 6,421 served | 7 pages |
| **Massive rate ceiling** | **5.00/min**, first refusal at request 6 of 8, both endpoints | 16 |
| **Alpaca rate ceiling** | **not reached** — 25 admitted at 134.05/min | 25 |
| **probe slice sealed** | 60 sessions × 40 tickers = **2,400 pairs**, 480 files, **737,507 bars** | — |
| **bar revision rate** | **`Absent(not_yet_measured)`** — eligible **2026-09-12** | 0 |
| **cross-vendor agreement share** | **`Absent(not_yet_measured)`** | 0 |
| E1 power at the registered 1.40 | **0.7435** — below the 0.80 GO floor | 875 |
| E1 power at the published 2.81 | **0.9995** | 875 |
| E2 power | **`Absent(not_served)`** — neither credential serves the carve-out | 2 credentials |
| operator prior | **0.30, `INDEPENDENT`**, 2026-08-29 (Amendment 5) | — |
| tests / mypy / mutations | **356 passing** / **clean over 54 files** / **12 mutations, 0 harness failures** | — |
| dollars spent | **0** | — |

## What happens next, in order

1. **On or after 2026-09-12, run `tools/repull_probe.py`.** It re-sends the
   identical request set from `reports/stage_a1r/task9_probe_manifest.json`,
   seals the bytes into `data/access/sealed_repull/`, and hands both pulls to
   `orb.comparator.SealedComparator.compare_pulls`. It writes
   `reports/stage_a1r/task3_revision.json`. **Registered thresholds:** `PASS` at
   a changed-bar share **at or below 0.005**; `PARTIAL` above that and at or
   below **0.020**; **`FAIL` above 0.020, which fires BLOCKED-2.**
2. **Then measure the cross-vendor agreement share** — the registered
   first-5-minute high-or-low agreement, **not** the tape ratio, which is a
   different measurement. **It can only be run over the 459 holdout sessions on
   or after 2024-08-29**, and its scope limit is registered (Amendment 8).
3. **Then re-fire Section 0** with both integrity inputs present. Only then are
   `GO` and `DEGRADED` reachable at all.

## Rules that bind whatever the task is

- **`REGISTRATION.md` is append-only.** Nothing above an amendment line is ever
  edited. **Ten amendments** stand; read all of them.
- **Never point `orb.verdict`, `orb.signal` or `orb.universe` at a real bar
  before the Stage C latch.** A guard walks every import and fails if a Stage A
  module reaches one.
- **A second read of either window voids the hypothesis.** The latch refuses it.
- **Measured beats documented**, always. **This resumption is the demonstration:**
  a vendor recommended on documented grounds serves **0 of 1,762** in-sample
  sessions, and a ceiling measured against a 401 overstated the real one by
  **17.7×**.
- **Absence is a recorded state.** `Absent` refuses to become a number.
- **Every figure travels with its n in the same sentence.**
- **Terms of service bind.** `stooq.com` and `query1.finance.yahoo.com` publish
  `Disallow: /`. **Do not fetch them.**
- **Guard 8 redacts at the recording boundary.** Recordable about a credential:
  name, presence, character length. **Not recordable: the value, any prefix, any
  suffix, and any hash** — a hash of a 32-character key is a confirmation oracle
  for a guess.
- **`make all` is the gate.** Commit at every task boundary and push.

## The registered pace, and why it is not negotiable upward

| endpoint | spacing | per minute | basis |
|---|---:|---:|---|
| `massive:aggs`, `massive:reference` | **24.0 s** | **2.50** | **measured** — half of a measured 5.0/min 429 boundary |
| `alpaca:*` | **1.0 s** | **60.0** | **unmeasured ceiling** — half of a 134.05/min *observed admitted rate* |

**Daily caps, charged before sending: Massive 600, Alpaca 2,000.** Neither is
derived from a daily allowance, **because none was measured on either vendor**.
They are circuit breakers, not throughput targets.

## Open operator items — three, and none blocks the ladder

**Both earlier items are discharged.** The credentials exist and authenticate;
the Section 13 prior is filled at **0.30, `INDEPENDENT`**, satisfying **Section
10 clause 2**. Clauses 1 and 3 remain unsatisfied and **the Stage C latch stays
closed**.

1. **A third feed on a genuinely different upstream.** The two feeds held here
   **share an upstream**: the ratio IQR is **0.46 percentage points wide over
   `n = 100` pairs**, which two independent consolidations would not produce. A
   cross-vendor `PASS` therefore establishes that **two redistributors of one
   upstream agree**, and **it is not the Concretum test** — that spread,
   **226,000 to 726,000 USD** across four vendors, is a spread *across
   upstreams*. **ADR-022.**
2. **A costed decision on the Massive tier.** It buys back the agreement gate's
   window — **459 of 875 holdout and 0 of 1,762 in-sample sessions today** — and
   **nothing else**, since Alpaca already covers the registered windows at zero
   cost. **Near 29 USD per month, carried, never measured** (C-18). **The reach a
   paid tier actually delivers is deliberately not recorded as a number**; the
   honest way to get it is one month's spend and a second bisection.
   **Amendment 8.**

3. **Retire SL-3, or accept it.** **Registered 2026-08-29, `REGISTRATION.md`
   §11.1 under Amendment 12.** **Cross-vendor agreement covers 459 holdout
   sessions and 0 in-sample sessions**, so **all 1,762 in-sample sessions rest
   on a single unverified feed**, and **a PASS computed on the in-sample window
   is conditional on that one vendor's rendering of it being faithful — a
   condition this repository holds no measurement supporting.** This is the
   Concretum exposure — **226,000 to 726,000 USD across four vendors on
   identical code** — and it is the one this repository cannot currently retire
   for the in-sample window. **Two routes, neither chosen here, neither costed
   here:**
   - **(a) a reference credential whose tier reaches 2016-01-04**, which retires
     SL-3 **on measurement**. It costs money, needs an explicit operator
     instruction and its own ADR, and the reach a paid tier actually delivers is
     **deliberately not recorded as a number** — the honest way to get it is a
     month's spend and a second bisection. Note this is **item 2 widened**: item
     2 buys back the *holdout* overlap, and route (a) is the version of that
     purchase that also reaches the in-sample window, which only a tier serving
     2016-01-04 can do.
   - **(b) explicit operator acceptance that the in-sample window is
     single-sourced**, which retires **nothing by measurement**. It records that
     the operator has read SL-3 and accepts the conditional. **A decision, not a
     finding**, and it would be recorded with its date.

   **Neither route blocks the ladder, and neither is a precondition for the
   2026-09-12 re-pull.** SL-3 changes what a verdict *means*, never when one
   fires.

## What a fresh session must read before touching anything

1. **`CLAUDE.md`** — the operating manual. Standing rules 1–14, the blindness
   field lists stated exactly, the carve-out with its enforcement site, and
   **rule 3 as amended 2026-08-29** with the falsified original quoted in place.
2. **`REGISTRATION.md` §0** (the outcome map and its fixed precedence), **§8–10**
   (the co-primaries, the power method, the latch), **§13.1** (the operator
   prior), **and all ten amendments** — 5 through 10 are this resumption.
3. **`HYPOTHESES.md`** — H1's state, the five closure kinds, the ten culls, the
   two parked entries, and the two registered scope limits.
4. **`docs/ACCESS.md`** — the uncredentialed findings **and** the credentialed
   section below them, kept apart on purpose so the falsifications are visible.
5. **`DECISIONS.md`** — 26 ADRs; **019 through 026** are this resumption.
6. **`progress.md`, last entry** — where the session stopped.

## The thing most likely to go wrong next

**Running the re-pull early, or treating the tape ratio as the agreement
measurement.**

**The first manufactures a pass.** A re-pull sent before 2026-09-12 measures a
revision rate **biased toward zero**, and **zero is the shape of a `PASS`**. The
refusal in `orb.repull.require_due` exists for exactly that, and its message says
so rather than merely refusing.

**The second is a category error that would look like progress.** A.1 TASK 4
measured the **tape** — the ratio of first-5-minute *volume* between two feeds —
and returned `SAME_TAPE`. **That is not the registered cross-vendor agreement
share**, which is the fraction of session-ticker pairs agreeing on the
first-5-minute **high or low**. The tape verdict is the **gate that decides
whether the agreement thresholds may fire at all**. Recording one as the other
would fill an `Absent` with a number that measures something else.
