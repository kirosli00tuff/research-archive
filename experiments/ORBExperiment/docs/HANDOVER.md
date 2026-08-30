# HANDOVER.md — for a fresh session

**Read this before touching anything.**

> ## There are now TWO binding constraints, and only one of them is a calendar.
> ## **1. The earliest eligible re-pull is 2026-09-12.**
> ## **2. JOINT power is 0.043277 at the registered assumption, and no session count reaches 80 percent. That one does not wait for anything.**
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

**Section 0 re-fired `PENDING_REVISION` on 2026-08-29 for the third time that
day** — the inference-repair pass, **Amendment 23**. **Nothing is armed. Nothing
is closed. H1 is OPEN.**

**Twenty-three amendments stand. Thirty-five ADRs. Read amendments 18 through 23
and ADRs 032 through 035 first — they change what the experiment can conclude.**

### The inference, repaired and then found unpowered

| finding | figure | n |
|---|---|---|
| **alpha per co-primary** | **0.05** — superseded **0.02532057** (Amendment 18) | — |
| **E1 power at the registered 1.40** | **0.832450** — was 0.743521 | **875** |
| E1 power at 2.81 / 0.70, holdout | 0.999835 / 0.366747 | 875 |
| E1 power at 1.40 / 2.81 / 0.70, in-sample | 0.980162 / 1.000000 / 0.581652 | 1,762 |
| **E1 minimum n for 80 percent** | **795** — was 1,006, against **875 achievable** | — |
| **measured stop-exit share** | **0.381818** — 210 stop, 340 close | **550** |
| **measured ambiguous rate** | **0.000000**, rule-of-three bound **0.005357** | **560** |
| **measured pessimistic shift** | **0.041455 USD/share** — bounds 0.030 / 0.060 | 550 |
| E2 central mean at 1.40 | **+0.040386 USD/share** | — |
| **E2 pessimistic-cost mean at 1.40** | **−0.001068 USD/share — NEGATIVE** | — |
| **E2 power at 1.40, holdout** | **0.043277** — below the 0.05 size of the test | 875 |
| E2 power at 2.81 / 0.70, holdout | 0.819524 / 0.001271 | 875 |
| **E2 minimum n for 80 percent at 1.40** | **Absent — unreachable at any n** | — |
| **JOINT POWER at 1.40, holdout** | **0.043277**, binding component **E2** | **875** |
| JOINT power at 2.81, holdout | 0.819524, binding component E2 | 875 |
| **JOINT minimum n for 80 percent at 1.40** | **Absent — unreachable at any n** | — |
| JOINT minimum n for 80 percent at 2.81 | **827** | — |
| **break-even Sharpe** | **1.437035** — the registered 1.40 sits **2.577 percent** below it | — |
| break-even stop share at 1.40 | **0.346206** against a measured 0.381818 | — |
| **measured trigger rate** | **0.982143** — the breakout is a **direction rule** | 560 |
| E2 dispersion input | **2.029585 USD/share** | 550 |

### Access and integrity, unchanged by this pass

| finding | figure | n |
|---|---|---|
| **credentials authenticating** | **2 of 2** | 2 |
| **primary vendor** | **Alpaca** — 2016-01-04, 1,762/1,762 in-sample, 875/875 holdout | 16 probes |
| **reference vendor** | **Massive** — 2024-08-29, 0/1,762 in-sample, 459/875 holdout | 16 probes |
| **tape, Massive vs Alpaca-SIP** | **`SAME_TAPE`**, median **1.005197** | 100 pairs |
| **sealed slice feed** | **`CONFIRMED_CONSOLIDATED`** — `sip`, measured not assumed | 7 chunks |
| **delisted names with intraday history** | **203** — **`PASS`** | 229 |
| **Alpaca burst allowance** | **384 admitted in 55.96 s**, the 385th refused `429` | 391 |
| **Alpaca sustained ceiling** | **NOT reached** — 250 of 250 at **199.73/min** | 250 |
| **Alpaca operating pace / daily cap** | **98.36/min** at 0.61 s / **3,000** | — |
| **bar revision rate** | **`Absent(not_yet_measured)`** — eligible **2026-09-12** | 0 |
| **cross-vendor agreement share** | **`Absent(not_yet_measured)`** | 0 |
| operator prior | **0.30, `INDEPENDENT`** (Amendment 5) | — |
| tests / mypy / mutations | **410 passing** / **clean over 56 files** / **16 mutations, 0 harness failures** | — |
| dollars spent | **0** | — |

**Every E2 and joint figure carries the Amendment 11 caveat**: the dispersion
input comes from a **post-holdout regime** and may misstate in-sample dispersion
in either direction by an unmeasured, unbounded amount. **Every in-sample figure
carries SL-3.** **Every statement about what a PASS would mean carries §11.2.**

### Four things a fresh reader will otherwise get wrong

1. **`0.832450` is E1's power, not the design's.** Section 10.1 makes the latch
   condition **JOINT** power, bounded above by the smaller component. **The
   design's power is 0.043277.**
2. **Correcting the multiplicity error made E1 powered and left the design
   unpowered.** Both are true. Neither may be reported without the other.
3. **The E2 collapse is a property of the registered design, not of the world.**
   The pessimistic-cost mean is negative because the registered 1.40 assumption
   sits **2.577 percent** below the break-even Sharpe of **1.437035**.
4. **The breakout is a direction rule, not a selector** (Amendment 22). At a
   measured **0.982143** trigger rate the condition selects on almost nothing.
   **The registered rule is unchanged; the description was wrong.**

### H1b — registered 2026-08-30, NOT OPENED

**`REGISTERED_NOT_OPEN`.** The H1 rule with a raised price floor replacing the
registered open-above-5.00-USD filter. **Exactly one registered parameter
changes; every other one is unchanged.** The floor itself is **deliberately not
registered** — this pass ran a feasibility scan and handed over a table.

**It increments the deflated-Sharpe trial count from 8 to 9 for H1b.** H1's count
of 8 is unchanged. **The ninth trial exists because the filter change was
proposed after seeing an H1 null**, and that is the cost of having looked.

**Opening it requires its own full registration, its own power gate computed
rather than inherited, and explicit operator instruction. None exists.**

| price floor | selected | filling 20 **in the scan sample** | mean relvol | dispersion | **central ÷ shift** |
|---:|---:|---:|---:|---:|---:|
| **5** | 560 | 28 of 28 | 2.0652 | 2.0296 | **0.9742** |
| **10** | 560 | 28 of 28 | 1.8216 | 2.0962 | **0.9983** |
| **20** | 560 | 28 of 28 | 1.6190 | 2.3821 | **1.1415** |
| 50 | 446 | 0 of 28 | 1.4103 | 2.7093 | **1.4767** |
| 100 | 310 | 0 of 28 | 1.4381 | 3.1992 | **2.1424** |

**Do not read the "filling 20" column as a fact about the registered universe.**
The scan sampled **200 names of 5,317** — every 26th ticker. A floor that thins a
1-in-26 subsample says nothing about a universe **26.6 times larger**.

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
  module reaches one. **`orb.dispersion` is the one module that runs them over
  real bars, it is latched, and it may read only the amended carve-out.**
- **The carve-out is TWO-SIDED as of Amendment 11.** Readable: strictly before
  **2016-01-04T14:30:00.000Z** (measured empty for both credentials), **or** at
  or after **2026-07-01T04:00:00.000Z** — Eastern midnight, **not** UTC midnight,
  because UTC midnight sits at 20:00 ET on 2026-06-30 and would admit that
  session's after-hours bars. **Everything between is sealed.** Four fixtures sit
  exactly on the four edges.
- **Storing bars is not reading them.** The probe slice overlaps the holdout from
  **2026-05-05 to 2026-06-30**; those bytes went through a sealed writer that
  parses nothing and reached no strategy module. **That is collection. The Stage
  D latch still governs the holdout in full and has not been written.**
- **The consolidated tape is `CONFIG.consolidated_feed`, not a default.** Every
  bar request names its feed; the only non-consolidated path is
  `alpaca_minute_bars_on_feed`, which **demands a stated reason**. The measured
  cost of the wrong branch is a feed carrying **median 0.027761** of consolidated
  volume, `n = 100` pairs — real bars, all wrong, invisible downstream.
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
| **`alpaca:bars`** | **0.61 s** | **98.36** | **measured** — half of a **199.73/min sustained** rate, `n = 250`, 0 refusals over 75.10 s. Burst allowance **384 in 55.96 s** is looser and does not bind. |
| `alpaca:multibars`, `:account`, `:assets` | **1.0 s** | **60.0** | **unmeasured endpoints** — pacing is per endpoint, never per host, so a measurement on `alpaca:bars` licenses no change here |

**Daily caps, charged before sending: Massive 600, Alpaca 3,000** (Amendment 14). Neither is
derived from a daily allowance, **because none was measured on either vendor**.
They are circuit breakers, not throughput targets.

## Open operator items — four, and the fourth does not wait for anything

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

4. **Choose a route for the collapsed E2. THIS IS THE ONE THAT DOES NOT WAIT.**
   **`REGISTRATION.md` Amendment 21, ADR-034.** The measured pessimistic shift of
   **0.041455 USD/share** exceeds the implied central mean of **0.040386** at the
   registered 1.40 assumption, so the **pessimistic-cost mean is −0.001068**,
   **E2 power is 0.043277** and **JOINT power collapses with it — no session
   count reaches 80 percent at any n.** **Three routes, none chosen and none
   recommended here:**
   - **(a) A narrower verdict scope conditional on central costs alone**, with
     **E2 demoted to a named secondary**. E1 is powered at **0.832450**. The
     verdict would then support only *the rule cleared its bar under **central**
     cost assumptions* — and **that is exactly what Section 1's structural doubt
     2 says matters most**, so the registration would have to say so where the
     verdict is stated.
   - **(b) Narrow the registered cost band on measured execution evidence.** The
     pessimistic entry figure of **0.040 USD/share is carried and registered,
     never measured**. Real fill data would let it narrow on evidence. **This
     repository holds none, has no broker credential, and none is planned.**
   - **(c) Close H1 as `untestable-at-achievable-power`** under its own
     registered cost assumptions — **the fourth closure kind already in the house
     record**, a **legitimate documented negative about the design rather than
     about the world**.

   **None of the three depends on 2026-09-12.** **This decision can be taken
   today, and items 1 to 3 cannot resolve it.**

## What a fresh session must read before touching anything

1. **`CLAUDE.md`** — the operating manual. Standing rules 1–14, the blindness
   field lists stated exactly, **the carve-out as amended two-sided on
   2026-08-29** with the falsified original struck through and left visible, and
   **rule 3 as amended** with its falsified original quoted in place.
2. **`REGISTRATION.md` §0** (the outcome map and its fixed precedence), **§1.1**
   (the hypothesis restated), **§8–10 and §10.1** (the co-primaries, the power
   method, and the latch on **joint** power)
   (the co-primaries, the power method, the latch), **§11.1** (the scope
   limitations, SL-1 to SL-3), **§13.1** (the operator prior), **and all twenty-three
   amendments** — 5 to 10 the A.1 resumption, 11 to 17 the amendment pass,
   **18 to 23 the inference repair**.
3. **`HYPOTHESES.md`** — H1's state, the five closure kinds, the ten culls, the
   two parked entries, and **the three registered scope limits, SL-3 included**.
4. **`docs/ACCESS.md`** — the uncredentialed findings **and** the credentialed
   section below them, kept apart on purpose so the falsifications are visible.
5. **`DECISIONS.md`** — **35 ADRs**; 019–026 the A.1 resumption, 027–031 the amendment pass, **032 through 035 the inference repair**.
6. **`progress.md`, last entry** — where the session stopped.

## The inference-repair pass — what changed and what a quoted figure now means

**Read this before quoting any power figure written before 2026-08-29's third
firing.**

1. **`alpha` per co-primary is 0.05, not 0.02532057.** Section 8 is a
   **conjunction** and carried a **union** correction. Berger (1982) gives an
   intersection-union test the full nominal level per component. **Amendment 18.**
2. **E1's power figures all moved up and no datum changed.** 0.743521 →
   **0.832450** at 1.40 on 875; minimum n **1,006 → 795**.
3. **E2 is a different test now.** It asks whether the mean net PnL per trade
   survives the **pessimistic** end of the Section 6 band. The old E2 was a
   linear rescale of E1 and constrained nothing. **Amendment 19.**
4. **E2 and joint power collapsed at the registered assumption.** **0.043277**,
   with **no n reaching 80 percent**. **Amendment 21.**
5. **The latch condition is JOINT power.** **Section 10.1.** Neither component
   power alone satisfies clause 1.
6. **The breakout is a direction rule, not a selector.** Trigger rate
   **0.982143**, `n = 560`. **Amendment 22**, and the registered rule is
   unchanged.

## Three things the amendment pass measured that were previously asserted

**Read these before quoting any figure from before 2026-08-29.**

1. **The pre-period carve-out was never reachable.** `n = 2` credentials, **0
   serving** any session before 2016-01-04. It is amended two-sided
   (Amendment 11), and the second half **is not equivalent to the first** — the
   compromise runs **forward** now.
2. **The trigger rate is 0.982143, not 0.55.** `n = 560` selected name-sessions,
   post-holdout. **The 0.55 was never measured** and Section 9 said so
   (Amendment 15).
3. **Alpaca's ceiling is a burst allowance of 384 requests in 55.96 s, and its
   sustained ceiling is still unreached** at 199.73/min over 75.10 s with 0
   refusals (Amendment 14). **The old 134.05/min was that moment's latency, not a
   limiter** — the identical request shape reached 223.16/min on the same day.

**And one premise of the method was falsified: E2's power does not need a
per-trade dispersion input at all**, because its permutation clusters on session
date and the dispersion cancels. **E2 = E1** to five decimal places, and that is
arithmetic rather than a copied figure (Amendment 15).

## The thing most likely to go wrong next

**Running the re-pull early, or treating the tape ratio as the agreement
measurement.**

**The first manufactures a pass.** A re-pull sent before 2026-09-12 measures a
revision rate **biased toward zero**, and **zero is the shape of a `PASS`**. The
refusal in `orb.repull.require_due` exists for exactly that, and its message says
so rather than merely refusing.

**The first thing that will go wrong now: quoting `0.832450` as the design's
power.** It is **E1's** power. **The design's power is JOINT power, 0.043277**,
and Section 10.1 says so. A reader who takes the larger component has taken the
one number the conjunction guarantees is *not* the answer.

**The second: reading the E2 collapse as a verdict on H1.** It is not. **It is a
measured property of the registered design** — the registered 1.40 assumption
sits **2.577 percent** below the break-even Sharpe of **1.437035**. H1 remains
**OPEN**, and closing it as `untestable-at-achievable-power` is **one of three
routes**, not a conclusion this pass reached.

**A third, added by the amendment pass: quoting an E2 figure without its
caveat, or an in-sample figure without SL-3.** Every E2 number in this repository
rests on a dispersion measured in a **post-holdout regime** and **may misstate
in-sample dispersion in either direction by an unmeasured, unbounded amount**.
Every in-sample number rests on a **single unverified feed**. Both sentences
travel **in the same sentence as the figure**, per standing rule 13's own logic.

**A fourth: reading E2 = E1 as a bug or a copy.** It is neither. E2's permutation
clusters on session date, so the session is the independent unit and the
per-trade dispersion cancels. The verdict record prints both figures side by side
precisely so this can be checked rather than believed.

**The second is a category error that would look like progress.** A.1 TASK 4
measured the **tape** — the ratio of first-5-minute *volume* between two feeds —
and returned `SAME_TAPE`. **That is not the registered cross-vendor agreement
share**, which is the fraction of session-ticker pairs agreeing on the
first-5-minute **high or low**. The tape verdict is the **gate that decides
whether the agreement thresholds may fire at all**. Recording one as the other
would fill an `Absent` with a number that measures something else.
