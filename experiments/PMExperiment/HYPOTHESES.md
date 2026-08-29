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
