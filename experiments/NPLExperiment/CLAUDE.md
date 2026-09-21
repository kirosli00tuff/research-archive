# CLAUDE.md — NPLExperiment operating manual

Read this file at the start of every coding session. It is the contract for
how work happens in this repository.

## What this project is (permanent, stated from the first commit)

> **NPLExperiment is a measurement-only test of one hypothesis family: newly
> listed Hyperliquid perpetuals drift down over 30 and 90 days by more than a
> short pays in funding and fees.**
>
> **Stage A never trades, never touches capital, and never reads an outcome
> value.** There is no wallet, no signer, no order, no venue credential, no
> position, and no stage in which one is planned. The output is a registered
> design, a census, a power verdict, armed collectors, and eventually a
> documented verdict either way. A documented negative is a valid and expected
> outcome.

## Standing rules, in force for every task

1. **Log the operator prompt verbatim to progress.md before any other work.**
2. **State an ETA before arming each task. Record actual against ETA after.**
3. **Measured beats documented.** Verify every external figure live before
   relying on it.
4. **Absence is a recorded state, never a synthesized value.** A refusal is
   loud, never a silent skip. (`npl.absence`)
5. **Ledgers are append-only and fsynced.** A truncated line is reported,
   never repaired. (`npl.ledger`)
6. **Operational health and sample composition never merge.** Call states:
   `stored`, `no_data`, `source_failed`, `rate_limited`,
   `excluded_ineligible`, `expired`. (`npl.callstate`)
7. **Outcome blindness.** Outside the sealed writers, no code path parses a
   candle open, high, low, close, or volume, and no code path reads a funding
   rate stamped after its event entry, until the registered Stage B read.
   Coverage modules count rows and timestamps only. Tests pin every one of
   these absences. (`npl.blindness`, `tests/test_blindness.py`,
   `tests/test_guards.py`)
8. **Union time intervals before summing.** Order multi-process logs by
   clock, never by file position. (`npl.intervals`)
9. **Zero dollars. Keyless public endpoints only.** A request ledger with a
   daily cap charges before sending. (`npl.ledger.requests`)
10. **Every figure travels with its n in the same sentence.**

## The blindness field lists, stated exactly

- **Candle payload fields readable outside sealed writers: `t`, `T`, and row
  count.** Nothing else. Not `o`, not `h`, not `l`, not `c`, not `v`, under
  any spelling, in any module, until the registered Stage B read.
- **fundingHistory fields readable: `time` always, `fundingRate` only where
  `time` is at or before the referencing event entry timestamp.** A row
  stamped after its event entry carries a recorded absence
  (`Absent(blindness_gated)`), which refuses numeric coercion.
- The l2Book touch state (`px`, `sz` at the top levels) is a registered
  descriptive cost input (Section 5 of REGISTRATION.md), readable only in
  `spread.py`, and is not an outcome field.
- The sealed writers under `data/outcomes/` and `data/funding/` write raw
  response bytes and parse nothing.

## Non-negotiable rules

1. **Pre-register before results.** REGISTRATION.md is append-only; an
   amendment is dated, reasoned, and states what data existed when it was
   made. Nothing above an amendment line is ever edited.
2. **Secrets never enter the repo — and none are needed.** `.env.example` is
   empty on purpose. No API key exists anywhere in this project.
3. **The operator prior slot (REGISTRATION.md Section 13) is filled only by
   the operator.** The assistant priors recorded beside it are not the
   operator's number. The empty slot blocks Stage B structurally
   (`npl.registration_check`).
4. **Stage B opens the sealed outcomes exactly once**, on the registered
   trigger of Section 10, and `verdict.py` is never pointed at real sealed
   data before that.

## Coding standards

- Python 3.13+; type hints on all signatures; `ruff format`, `ruff check`,
  and `mypy --strict` pass clean. `make all` is the gate.
- Anything with logic gets a pytest test. Real tests, not smoke tests, with
  boundary fixtures ON the registered boundary — a fixture comfortably inside
  its boundary lets a moved threshold pass unnoticed (InsiderExperiment
  mutation lesson).
- Frozen dataclasses, pure functions over records, many small modules.
- Errors handled explicitly; an error never quietly becomes a data condition.
- The mutation harness purges bytecode before every run; a harness that can
  report on absent source is worse than no harness.

## Commands

    make install     create the venv and install
    make all         lint, typecheck, test
    make guards      the structural guards alone
    make mutations   apply the registered mutations and restore (Stage A.4)

## Git commit conventions

Conventional commits: `<type>: <description>`, type in
`feat, fix, refactor, docs, test, chore, perf, ci`. Imperative mood, lower
case, no trailing period. Commit at each sub-stage boundary. **Push nothing.**

## Read these first

- `REGISTRATION.md` — the pre-registration. Nothing in it may be revised to
  fit a result.
- `progress.md` — where the project is right now, with ETA against actual.
- `DECISIONS.md` — append-only ADR log; read before revisiting a settled
  question.
- `docs/ACCESS.md` — the measured access table, with dates.
