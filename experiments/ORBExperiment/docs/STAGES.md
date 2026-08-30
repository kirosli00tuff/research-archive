# Stage ladder

**Status at 2026-08-29: Stage A complete except for the two integrity
measurements. Section 0 fired `PENDING_ACCESS`. H1 is OPEN. Nothing is armed and
nothing is closed.**

Every rung states what it answers, what lets it start, what ends it, and how much
capital it authorizes. **The capital column reads `none` at every rung of this
ladder, including the last one Stage A can reach.**

## The ladder

| stage | question it answers | entry gate | exit gate | capital |
|---|---|---|---|---|
| **A.-1 — preconditions and duplication** *(complete)* | Is this question already open somewhere in the house? | Operator prompt; a clean tree tracking `origin/main` | **CLEAR**: n = 11 repositories, 8 patterns, 14,002 raw hits, **0 substantive**; the five design-bearing patterns return **zero** everywhere | none |
| **A.0 — registration** *(complete)* | What exactly is being claimed, and what would refute it? | Duplication CLEAR; prior art read | Sections 0–14 committed **before any vendor data request**; `make all` green on the guards | none |
| **A.1 — access and integrity** *(TASK 1–2 complete; TASK 3–4 blocked)* | Can a vendor be reached, and are its bars stable enough for any verdict to mean anything? | Registration committed; `robots.txt` and terms recorded **before the first repeated fetch** | **TASK 1–2: measured, 0 of 9 vendors usable.** **TASK 3–4: `Absent(not_yet_measured)`** — machinery built, armed, and waiting on a credential | none |
| **A.2 — substrate, cost, power, verdict** *(complete)* | Is the design measurable at power, and what does it cost to trade? | A.1 findings recorded | Calendar 2,637 sessions / 21 half; cost model frozen `3789221b…`; **E1 power 0.7435 at the registered assumption, 0.9995 at the published**; **Section 0 fired PENDING_ACCESS** | none |
| **A.3 — arming** *(built, inert)* | Are the collectors accruing correctly? | **GO or DEGRADED**, which `PENDING_ACCESS` is not | Collector, watcher, systemd units and latch machinery written and tested; **no timer enabled** | none |
| **A.4 — gates and mutations** *(complete)* | Do the guards actually bind? | A.3 code exists | `make all` green; **n = 10 mutations, 0 harness failures**, each restored green, bytecode purged before every run | none |
| **A.5 — documentation and handover** *(complete)* | Can a fresh session pick this up? | A.4 green | README, ACCESS, DUPLICATION, DECISIONS, STAGES, report.md, HANDOVER.md committed and pushed | none |
| **A.1 TASK 3–4 re-run** *(next; blocked on an operator item)* | What is the bar revision rate, the cross-vendor agreement rate, and the delisted-name count? | **Two free-tier credentials, two different vendors.** An operator action | The three measured figures, each with its n, and their PASS/PARTIAL/FAIL verdicts | none |
| **A.2 TASK 5 re-fire** | Does the design proceed, narrow, or stop? | The three integrity figures exist | **GO**, **DEGRADED** (expected — the counterfactual already computes to it), or **BLOCKED** | none |
| **A.3 arming** | — | A DEGRADED-or-better Section 0 | Timers enabled; probe pull 1 taken | none |
| **the 14-day wait** | Does this vendor rewrite already-served bars? | Probe pull 1 sealed | **≥ 14 calendar days**, then the identical re-pull and the revision verdict | none |
| **B — Stage C latch and the in-sample read** *(dark)* | Did the registered rule clear its bars in-sample? | **All three of**: both co-primaries ≥ 80% power at achievable N under the assumption Section 0 fired on; **the operator prior slot filled and labelled**; **explicit operator instruction** | One read, exactly once, behind a latch written first recording module hashes. **A second read voids the hypothesis** | none |
| **C — Stage D latch and the holdout read** *(dark)* | Did it clear its bars out of sample? | Stage C's latch **present**, Stage D's **absent**; its own operator instruction | E1 ≥ 1.00 **and** E2 lower bound > 0 at alpha_adj **and** concentration **and** persistence — **all four** | none |
| **D — software on paper** *(unregistered)* | Is the implementation correct enough to trust with an order? | A Stage D pass; operator authorization; **a new registration of its own** | — | **none** |
| **the capital gate** *(unregistered)* | — | Everything above, plus an explicit operator decision this registration does not anticipate | — | **none until a future registration says otherwise** |

## Two things the ladder says on purpose

**The forward shadow is a parallel monitor, not a gate.** Once collectors are
armed they accrue forward sessions continuously. That stream is **never** a rung:
it does not gate a read, it does not extend a window, and a favourable shadow
does not advance the ladder. It exists so that a divergence between forward and
historical behaviour is **visible** rather than discovered at the read.

**Live entry sits behind the software-correctness gates, not behind the
out-of-sample read.** A Stage D pass is a statement about a **modelled** rule on
**historical** bars from **one vendor**. It says nothing about whether the code
that would place an order is correct. Those are different questions and this
ladder keeps them apart: **stage D answers "was there an effect", stage D+ answers
"can this software be trusted with an order", and the second is not implied by
the first.**

## The dates

- **2026-08-29** — Stage A registered, measured, and documented in one session.
  Section 0 fired **PENDING_ACCESS**.
- **Blocked on an operator item** — two free-tier vendor credentials. Until then
  A.1 TASK 3 and TASK 4 cannot run, and **the 14-day revision wait has not
  started.**
- **Earliest possible Stage C** — **credential date + ~1 day (probe pull) + 14
  calendar days (the registered wait) + the re-pull and verdict.** With a
  credential on day 0, that is **day 15 at the earliest**, and only if the
  revision verdict passes, the power gate is satisfied under the assumption
  Section 0 fires on, **and the operator prior slot is filled.**
- **The operator prior slot is the other open item, and it is the only one
  besides the credential.**
