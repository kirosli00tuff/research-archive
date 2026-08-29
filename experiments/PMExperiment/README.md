# PMExperiment

**A measurement-only test of one hypothesis: prediction-market prices are
mis-calibrated by enough to survive the costs a Canadian retail participant
actually pays.**

**Stage A never trades, holds no account, places no order, and reads no
outcome value.** There is no broker credential, no venue login, no position,
and no stage in which one is planned. Kalshi market data and settlement
history are public and are read without an account. `.env.example` is empty
on purpose.

**A documented negative is a valid and expected outcome. So is BLOCKED.**

---

## Status: Section 0 registered; Stage A fired PENDING_ACCESS — 2026-08-29

Registration preceded every request: Section 0 was committed before the first
probe. The access gate then failed closed. The recorded Kalshi terms do not
sanction keyless systematic retrieval or AI-mediated analysis of Kalshi Data
without written authorization, the API Developer Agreement is unreadable by
automated means (HTTP 429 bot challenge), and the keyless settled listing
reaches back only to spring 2024 — n = 13 probe requests total, figures and
dates in `docs/ACCESS.md`. **The power gate never fired. No statistic
relating a price to an outcome exists.** The calibration question stays open,
unmeasured, with the reopening conditions recorded in `REGISTRATION.md`
Section 15.1.

---

## The measurement that decides this repository

**Not the calibration error. The power to detect one inside the Canadian
filter.**

The direct precedent is NPDExperiment, which closed at
*unresolved-at-achievable-power* with a realized minimum detectable contrast
of **0.0512** against an effect band of **0.01 to 0.05** — a design that could
not have detected an effect anywhere in the range it was testing — discovered
after **415 days** of collection, in the same session that read the result.

InsiderExperiment then registered its power gate in advance for exactly that
reason and fired **BLOCKED at 49.35 bp before spending**.

**This repository follows Insider, not NPD.** The minimum detectable effect is
computed from bucket counts and dispersion alone, before any first moment
relating price to outcome is read, and the gate is committed before the
measurement it judges.

---

## Why this domain, stated honestly

It is the one domain in this program's register whose reported effects are
large relative to achievable samples. Favourite-longshot mispricing at the
price extremes is documented in tens of percent, not basis points, so it
clears the MDE floor that closed four previous repositories.

**The doubt is the Canadian filter.** The permitted categories are economic
indicators, financial markets and climate — the well-calibrated ones — and a
30-day minimum maturity removes the fast-resolving contracts. Whether enough
extreme-priced contracts survive that filter in usable numbers is an open
question, and it is answerable **without reading a single outcome**.

A split verdict is a legitimate finding: the mispricing may be real and simply
not reachable from Canada.

---

## Scope

- Reads **public** market data and settlement history. No account, either side
  of the border.
- Canadians cannot trade on Kalshi directly. The permitted-subset filter is a
  **registered analysis step**, not a trading plan.
- Nothing here is trading advice, and nothing here is a suggestion to trade.

---

## Layout

| path | holds |
|---|---|
| `REGISTRATION.md` | the binding pre-registration; Section 0 first, amendments append |
| `DECISIONS.md` | ADRs; deliberate departures recorded with evidence |
| `progress.md` | dated stage entries, newest first, append-only |
| `docs/ACCESS.md` | measured access per source, written by `make verify` |
| `pmexperiment/` | the package |
| `tests/` | suite, including the honesty and registration tests |

Binding documents: `REGISTRATION.md`, `DECISIONS.md`, `progress.md`.

## Standing practices, inherited

Pre-register before results. Measured behaviour beats documentation. Refusals
fail closed. Union time intervals before summing. Never trust append order
across processes. A gate that has never failed is not a gate. Every prompt
states a measured ETA per task.
