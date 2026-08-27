# Stage ladder — entry and exit gates

Status at 2026-08-27: **A complete (GO). B armed, awaiting tonight's 01:40Z
pass and the operator paste.** Rows A and B are registered fact. **Rows C and
D are operator-revised sketch (2026-08-27)** — nothing below the B row binds
until its own registration is committed. One verdict-bearing read per
registration. Secondaries never move a row. The forward shadow was demoted
from gate to monitor by operator decision; the demotion is recorded here and
again in the C registration when written.

| stage | question it answers | entry gate | exit gate | capital |
|---|---|---|---|---|
| **A — registration and census** (complete) | Is the design measurable at power on this venue? | Operator prompt; Sections 0–13 committed before any network call | Section 0 verdict. **Fired GO 2026-08-27**: retro N 312, delisting PASS 6/6, powers 1.000 / 0.9993 / 0.9995 against min-N 34 / 103 / 60 | none |
| **B — the sealed read** (armed) | Did the registered short clear its bars on the retro cohort? | Prior slot filled, 0.40 (adopted); 312 event and 176 control windows sealed; coverage >= 0.90 candles and >= 0.95 funding hours per window; effective N >= 34 / 103 / 60; gates green; latch absent; explicit operator paste | Amendment-3 table, one row fires: **GO** (P1+P2+P3 pass at alpha_adj 0.016952, central costs). **PARTIAL_DRIFT** (P3 fails): listing-age claim closes, no C on this design. **FAIL** (P1 or P2 fails): hypothesis closes, collectors disarm | none |
| **C — software on paper** (sketch) | Is the execution stack correct? | B fired GO; operator authorization; its own registration with the gates below fixed before build | Correctness gates, not signal gates: every order-gate refusal produced with named arithmetic; account pinning shown at gate and at construction; latching kill switch as the sole interface to itself; append-only spend and position ledgers; mutation suite caught on the live-order surface; testnet or shadow fills reconciling to the model inside a stated band; line-by-line review of every order and risk path | none — simulated fills only |
| **D — live-half** (sketch) | Does live execution track the model inside tolerance? | C correctness gates green; its own registration; funded sleeve ~ $1,000; isolated margin per name with loss hard-capped at posted margin; ramp from venue-minimum notional only after live fills reconcile; kills registered: sleeve floor $500, funding-flip, three squeeze losses past the modelled tail, venue incident | Any kill fires: close and disarm. Shadow read near **late November 2026** (>= 34 matured forward events): continue-or-stop on out-of-sample evidence. Live P&L never feeds a verdict | ~ $1,000 |

## The path, dated (operator-revised 2026-08-27)

- **Paper opens at C** the day after a B GO plus authorization plus the C
  registration. Build estimate roughly two weeks, correctness-gated rather
  than calendar-gated.
- **Live opens at D** the day C's correctness gates pass — on retro evidence
  alone. The accepted risk, stated once: live entry precedes the
  out-of-sample check the shadow exists to provide.
- **The shadow runs in parallel** at zero cost, 18.5 events/month, 30-day
  maturation. Its registered read near late November 2026 is the
  continue-or-stop moment for the live sleeve.
- Operator-only at every rung: the authorization, the acceptance of each
  registration, the funding.

Equities stay closed at this stake regardless of the above: HFExperiment
A.1b measured IBKR refusing fractional orders (error 10243), and the
whole-share branch closed at the registered stake. Live means the
Hyperliquid sleeve.
