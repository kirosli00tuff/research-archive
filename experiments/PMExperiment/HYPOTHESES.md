# Hypothesis register

**Read this before proposing any new hypothesis on prediction-market pricing.**

**This file exists to prevent retrying a settled question because the number
that closed it is buried.** That is its whole job. A closed entry carries the
figure that closed it, with its n, and states what would reopen it — or states
that nothing would. A question answered expensively and then re-asked because
nobody could find the answer has cost this house real time before.

This file contains **no analysis**. It records what the registration and the
sealed reads established.

**Status at 2026-08-29, Stage A: H1 OPEN, registered, PENDING_ACCESS.**
Section 0 was committed before the first request; the access gate then failed
closed on the recorded terms and on keyless history depth. No calibration
statistic exists.

---

## H1 — calibration net of Canadian retail cost

**Status: OPEN. Registered 2026-08-29; the access gate fired PENDING_ACCESS
the same day** (REGISTRATION.md Section 15.1, docs/ACCESS.md). The power gate
never fired, so no figure exists for or against H1. What would reopen access
is recorded in Section 15.1: written authorization for systematic retrieval
and AI-mediated analysis, a sanctioned keyless bulk channel, or an operator
reversal of ADR-002.

Prediction-market prices are mis-calibrated by enough to survive the costs a
Canadian retail participant actually pays.

Judged on two universes, reported separately and never pooled: the unrestricted
public Kalshi history, and the Canadian-permitted subset defined by the
registered filter.

**Nothing may be claimed for H1 until `REGISTRATION.md` Section 0 is committed
and the power gate has fired.**

**Registered expectation, stated before any measurement:** the effect is
plausibly real in the unrestricted universe, where documented favourite-longshot
mispricing at the price extremes runs in tens of percent rather than basis
points. The doubt is the filter. A split verdict — unrestricted clears, permitted
subset BLOCKED — is a **legitimate registered finding**, and reads as "the
mispricing may be real and not reachable from Canada."

---

## Closed before opening

Recorded so they are not re-proposed. Each was closed at registration on
external evidence or on venue access, not on a measurement made here.

| candidate | why it is not H1 | what would reopen it |
|---|---|---|
| Cross-venue arbitrage, Kalshi against Polymarket | Documented arbitrage windows close in seconds and are dominated by sub-100 ms bots; Polymarket is inaccessible to Canadians. Not reachable at retail latency. | Nothing at retail latency. |
| Sports and political contract mispricing | Excluded from the Canadian-permitted categories. Measurable but not reachable, and measuring only the unreachable is a different project. | A change in CIRO-permitted categories. |
| Trading any measured edge | This repository has no execution path in any stage. Out of scope by construction, not by result. | Nothing. It is a scope rule, not a finding. |

---

## Parked

| candidate | status |
|---|---|
| H2 — time-decay and convergence structure within a contract's life | PARKED. Depends on intraday price history being retrievable at usable depth, which Stage A measures. Not registered. |
| H3 — cross-category calibration contrast | PARKED. Requires H1's gate to clear first, and would add trials to an account that does not yet exist. |

---

## Register discipline

A hypothesis enters this file when it is registered, not when it is imagined.
An entry closes with the figure that closed it and its n. A closed entry is
never silently reopened: reopening requires meeting the condition written in
its own row, and that condition is written before the entry closes.

---

## Amended 2026-08-30 — the venue split, and what H1 now means

H1 is now measured on **Polymarket**, whose public read endpoints need no key,
no authentication and no wallet, with settlement on Polygon. Kalshi remains
**PENDING_ACCESS** on its Data Terms of Use; that verdict stands and is not
re-litigated.

**H1 as now registered:** does mispricing exist, on the venue where the data is
public by construction, at a magnitude that would survive Canadian retail cost.

**H1t — transfer — is a separate hypothesis and is UNTESTED.**

| | |
|---|---|
| statement | a calibration result measured on Polymarket holds on a Canadian-tradeable venue |
| status | **UNTESTED. May not be assumed at any point.** |
| why it is separate | a documented Kalshi bias has been reported not to replicate on Polymarket; the largest Polymarket study reports no general longshot bias while other work finds one on Kalshi; and this program's own MLCryptoEngine H2 measured cross-venue transfer at **AUC 0.501** |
| what would close it | measurement on the venue where the trade would be placed, which currently requires written Kalshi authorization |

**Registered before measurement:** Polymarket's documented mispricing
concentrates in politics and sports, which are the categories **excluded** from
the Canadian-permitted subset. A real effect there may sit entirely outside the
contracts a Canadian could trade. Recorded now so it cannot later be offered as
an explanation.

**Gate order, registered:** the fee-versus-edge band of Amendment 2 fires
first, the power gate second and only over what the band leaves open. A
BAND-EMPTY verdict closes the tradeable question **on cost**, and the
calibration work may continue only as a labelled phenomenon study.

---

## Amended 2026-08-29 — the fee band fired BAND-OPEN; H1 stays open

**H1 remains OPEN.** The first of the two registered gates has now fired.
**The power gate has still never fired, and no statistic relating a price to an
outcome exists in this repository.** No venue was read to reach this verdict.

**The band gate, fired 2026-08-29: BAND-OPEN** (REGISTRATION.md Section 15.2,
evidence in `docs/BAND.md`). The tradeable question is **not** closed on cost.
Amendment 3's labelled-phenomenon-study route is therefore **not triggered**;
it applies only on BAND-EMPTY.

**The surviving region, and the only region the power gate may fire over:**
entry prices **91–99c** held to resolution, requiring an edge above **5.85
points** at the registered FX turnover k = 1, against a registered band top of
**8.00 points**.

**The figures that must be carried forward with it, so this is not re-asked
without them:**

| figure | value |
|---|---|
| fee + half-spread alone, held route, before any FX | **0.0300** — already above the registered band bottom of 0.0200, at every price and on every route |
| required underpricing at 95c, held to resolution, k = 1 | **0.0585** |
| required underpricing at 95c, round trip, k = 1 | **0.0785** — Section 11's registered C(0.95), meeting the band top only at an untradeable $1.00 |
| magnitudes actually cited at 91–99c | Bürgi's **0.020** and **0.030** — **both fail**; the 0.030 exactly ties the 0.0300 floor even with FX at zero |
| the only cited magnitude that clears | Krause's **0.077**, at an exploitable entry price of **0.883** — the 81–90 decile, outside the registered tail cell, **n not recorded anywhere** |
| surviving share of the band at 95c, held route | the top **2.15** of 6.0 points |

**What this verdict is not.** BAND-OPEN is **not** evidence that a tradeable
edge exists. It records only that cost alone does not close the question. Every
magnitude any cited source places *inside* the surviving bucket fails the cost
floor; the band survives on its registered top, which is set by the one source
whose n the registration never recorded.

**Registered as not recomputable.** Amendment 2 fixes the band as computed once:
it is not recomputed after a calibration result is seen, and no bucket may be
added to it afterwards. A different verdict requires a revised cost component
entering by numbered amendment with its own evidence — not a re-argument of the
same figures.

**Next gate:** the power gate, over 91–99c held to resolution and no other
region. It was not designed in Stage B.

---

## Amended 2026-08-30 — Polymarket fires PENDING_ACCESS; H1 is unmeasured on both venues

**H1 remains OPEN and is now unmeasured on every venue this repository has
examined.** The power gate has still never fired. **No statistic relating a
price to an outcome exists.** Zero contracts have ever been enumerated from
Polymarket, and zero market-data requests were sent to it.

| venue | verdict | ground | date |
|---|---|---|---|
| Kalshi | **PENDING_ACCESS** | Data Terms prohibit systematic retrieval and AI-mediated use without written authorization; Developer Agreement unreadable (HTTP 429) | 2026-08-29 |
| Polymarket | **PENDING_ACCESS** | Terms of Use, effective 2026-08-11, prohibit "data mining tools, robots, crawlers, or similar data gathering and extraction tools", scope expressly reaching API **and on-chain** access | 2026-08-30 |

**The same failure mode has now closed two venues, and the second was not
foreseen because it was not measured.** Amendment 1 moved the venue here on the
ground that Polymarket's data was "public by construction rather than by
permission" — a claim about permission inferred from the absence of an API key,
citing no clause and no date. Amendment 6 retracts that ground. **Keyless is not
the same as permitted, and this register now records the mistake twice so it is
not made a third time.**

**What this does *not* change.** The Stage B band verdict stands: BAND-OPEN over
91–99c held to resolution, on arithmetic that read no venue and needed none. It
is unaffected by access, because it never depended on it.

**H1t — transfer — is untouched and remains UNTESTED.** There is now no
Polymarket calibration result at all, so there is nothing to transfer even in
principle. The three grounds recorded above stand, including MLCryptoEngine's H2
at **AUC 0.501**.

**Registered so it is not re-proposed:** the Canadian-permitted subset's
category and maturity filter has still never been applied to any real
enumeration, and Amendment 5's volume floor of **$1,000** is registered but
**never exercised** — its cost in sample is unmeasured, reported absent rather
than as zero.

**What would reopen either venue** is recorded in REGISTRATION.md Sections 15.1
and 15.3 and in Amendment 6: written authorization from the venue, a sanctioned
bulk or builder channel, or — for Polymarket only, and unanswered — a Polygon
read through infrastructure that is not a Polymarket Interface. **None of these
is a second look, because no outcome has ever been read.**
