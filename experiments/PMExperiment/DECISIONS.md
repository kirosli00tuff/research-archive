# DECISIONS

Architecture decision records. Each records a deliberate departure from a
default, or a choice that a later reader would otherwise have to reverse
engineer. Append only.

---

## ADR-001. This is a separate repository

**Status:** accepted, 2026-08-29.

The prediction-market hypothesis shares no universe, no venue, no cost model
and no data source with any existing repository in this program. Folding it
into one of them would mix two registers and two multiplicity accounts.

**Consequence:** its own register, its own trial accounting, its own ledger. No
result here is evidence in another repository's family, and no result there is
evidence here.

---

## ADR-002. Stage A holds no account, on either side of the border

**Status:** accepted, 2026-08-29.

Kalshi market data and settlement history are public. Canadians cannot trade
there, but nothing prevents measuring it. The measurement half of this project
therefore needs no broker, no credential and no capital.

**Consequence:** `.env.example` is empty on purpose. Zero dollars spent in
Stage A. The Canadian-permitted filter is a registered analysis step, not a
trading plan.

---

## ADR-003. The power gate is committed before the measurement it judges

**Status:** accepted, 2026-08-29.

NPDExperiment closed at unresolved-at-achievable-power, MDE 0.0512 against an
effect band of 0.01 to 0.05, discovered after 415 days in the session that read
the result. InsiderExperiment registered its gate first and fired BLOCKED at
49.35 bp before spending.

**Consequence:** no statistic relating a price to an outcome is computed until
the gate fires. The gate reads bucket counts and dispersion only.

---

## ADR-004. A split verdict is a finding, not a failure

**Status:** accepted, 2026-08-29.

The unrestricted universe and the Canadian-permitted subset are judged
separately.

**Consequence:** if the unrestricted universe clears and the permitted subset
is BLOCKED, the registered reading is "the mispricing may be real and not
reachable from Canada." That is reported as a result.

---

## ADR-005. The document set follows ORBExperiment, the current house shape

**Status:** accepted, 2026-08-29.

The scaffold was first written with five markdown files, `## Section N`
registration headers, and a progress log in stage-entry form. That diverged
from ORBExperiment, which opened the same day and is the current shape:
seven binding documents, `## N.` registration headers numbered 0 through 17
with 17 reserved for amendments, a `HYPOTHESES.md` register, a `report.md`
written per stage and never revised, and a `progress.md` session log whose
Entry 0 is the operator prompt logged verbatim before any other work.

**Consequence:** the divergence is corrected before any measurement, so no
record is rewritten later. `HYPOTHESES.md` and `report.md` are added, the
registration is renumbered to the house shape with sections 5 through 16
stubbed, `progress.md` becomes a session log with Entry 0 reserved, and
CLAUDE.md carries sixteen numbered standing rules that later entries cite by
number. Four tests pin the shape so it cannot drift back.
