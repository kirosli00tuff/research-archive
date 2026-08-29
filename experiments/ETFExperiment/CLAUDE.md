# CLAUDE.md — ETFExperiment operating manual

Read this file at the start of every coding session. It is the contract for how
work happens in this repository.

## What this project is (permanent, stated from the first commit)

> **ETFExperiment is a measurement-only test of one hypothesis: US spot Bitcoin
> ETF net flow prints predict the next day's BTC return, out of sample, by
> enough to clear a round trip on Hyperliquid perps.**
>
> **Stage A never trades, never touches capital, and never reads an outcome
> value.** There is no wallet, no signer, no order, no venue credential, no
> position, and no stage in which one is planned. The output is a registered
> design, a measured publication lag, a measured revision rate, a census, a
> power verdict, armed collectors, and eventually a documented verdict either
> way. A documented negative is a valid and expected outcome.

**The measurement that decides this repository is not the return. It is the
publication lag and the revision rate.** Stage A.1 Tasks 3 and 4 are the
experiment. The MLCryptoEngine H11 precedent is why: a free flow source with a
**measured 75-day publication lag** and whole-file regeneration that revised
past rows killed the last flow hypothesis this project ran, and the lag was
discovered rather than registered. Here it is registered as the first-class
measurement, before any model exists.

## Standing rules, in force for every task

1. **Log the operator prompt verbatim to progress.md before any other work.**
2. **State an ETA before arming each task. Record actual against ETA after.**
3. **Measured beats documented.** Verify every external figure live before
   relying on it. A publication convention printed on a source's own page is
   documented, never measured, and the measured lag wins.
4. **Absence is a recorded state, never a synthesized value.** A refusal is
   loud, never a silent skip. (`etf.absence`)
5. **Ledgers are append-only and fsynced.** A truncated line is reported, never
   repaired. (`etf.ledger`)
6. **Operational health and sample composition never merge.** Call states:
   `stored`, `no_data`, `source_failed`, `rate_limited`,
   `excluded_ineligible`, `expired`. (`etf.callstate`)
7. **Outcome blindness.** Outside the sealed writers, no code path parses a BTC
   price, open, high, low, close, volume, or any return derived from one, and
   no code path reads a funding rate stamped inside a hold window, until the
   registered Stage B read. **Flow values are signal, not outcome, and are
   readable.** Coverage modules count rows and timestamps only. Tests pin every
   one of these absences. (`etf.blindness`, `tests/test_blindness.py`,
   `tests/test_guards.py`)
8. **The pre-period carve-out is the one exception**, stated in full below.
9. **Union time intervals before summing.** Order multi-process logs by clock,
   never by file position.
10. **Zero dollars. Keyless public endpoints only.** A request ledger with a
    daily cap charges before sending. (`etf.ledger.requests`)
11. **Terms of service bind.** Record `robots.txt` and the published terms
    verbatim for every source before the first automated fetch. If automated
    collection is disallowed, record it loudly and route the access verdict
    accordingly. Do not proceed against a stated prohibition. The HFExperiment
    Wealthsimple finding is the precedent.
12. **Every figure travels with its n in the same sentence.**

## The blindness field lists, stated exactly

- **Flow payload fields readable outside the sealed writers: every field,
  including the flow values themselves, plus the capture timestamp this
  repository stamps on the capture. Flow is signal.** No gate applies to flow.
  (`etf.flow`)
- **Price payload fields readable outside the sealed writers: `t`, `T`, and row
  count only. Never `o`, `h`, `l`, `c`, `v`**, under any spelling, in any
  module, until the registered Stage B read. (`etf.blindness.candle_times`,
  pinned repo-wide by `tests/test_guards.py::test_no_module_reads_a_priced_candle_field_anywhere`)
- **Funding fields readable outside the sealed writers: `time` always;
  `fundingRate` only where `time` is strictly before 2025-05-01, under the
  pre-period carve-out.** A row stamped at or after that instant carries
  `Absent(pre_period_gated)`, which refuses coercion to a number.
  (`etf.blindness.funding_rows` → `etf.preperiod.gate_pre_period`)
- The sealed writers under `data/outcomes/` and `data/funding/` write raw
  response bytes and parse nothing. (`etf.seal`)

## The pre-period carve-out

**Power inputs may read BTC price and funding data stamped strictly before
2025-05-01. Every other price or funding read is sealed.** The rationale: the
window before 2025-05-01 sits inside the source study's own sample (January
2024 through April 2025) and outside this test sample, which begins
2025-05-01, so reading it cannot leak a single observation the Stage B verdict
will be computed on. The E2 economic-power computation needs a volatility and a
funding level to size a net return against a 9 bp round trip; taking those from
the test window would be reading the outcome to plan the test of the outcome,
and inventing them would register a number this repository did not measure.
**The enforcement site is `etf.preperiod.require_pre_period` and
`etf.preperiod.gate_pre_period`, the boundary is `CONFIG.pre_period_end_ms`
(2025-05-01T00:00:00.000Z, exclusive), and the pin is exercised by
`tests/test_preperiod.py` with fixtures sitting exactly on the boundary — one
millisecond before it passes, the instant itself is refused.** Three structural
guards in `tests/test_guards.py` hold it there: the funding reader must route
every rate through `gate_pre_period`, no module outside `preperiod.py` may read
the boundary from config, and no module outside `config.py` may hardcode its
literal value.

## Non-negotiable rules

1. **Pre-register before results.** REGISTRATION.md is append-only; an
   amendment is dated, reasoned, and states exactly what data existed when it
   was made. Nothing above an amendment line is ever edited.
2. **The entry anchor moves exactly once, by exactly one rule.** Section 3 of
   the registration registers it provisionally at 08:00 UTC on D+1; the A.1
   Task 3 measured 95th percentile first-print time is the only input that can
   move it, by amendment, before any admissibility count is final.
   (`etf.anchor.amended_anchor_hour`)
3. **A later value is never substituted for an as-printed one.** The value
   taken for trading day D is the one standing in a capture strictly before the
   anchor. Where a later value differs, the day is flagged `revised` and the
   difference is recorded — never corrected.
4. **Secrets never enter the repo — and none are needed.** `.env.example` is
   empty on purpose. No API key exists anywhere in this project.
5. **The operator prior slot (REGISTRATION.md Section 13) is filled only by the
   operator.** The assistant prior recorded beside it is not the operator's
   number. The empty slot blocks Stage B structurally.
6. **Stage B opens the sealed outcomes exactly once**, on the registered
   trigger of Section 10, behind a latch written first, and `verdict.py` is
   never pointed at real sealed data before that.

## Coding standards

- Python 3.13+; type hints on all signatures; `ruff format`, `ruff check`, and
  `mypy --strict` pass clean. `make all` is the gate.
- Anything with logic gets a pytest test. Real tests, not smoke tests, with
  **boundary fixtures ON the registered boundary** — a fixture comfortably
  inside its boundary lets a moved threshold pass unnoticed (InsiderExperiment
  mutation lesson).
- Frozen dataclasses, pure functions over records, many small modules.
- Errors handled explicitly; an error never quietly becomes a data condition.
- The mutation harness purges bytecode before every run; a harness that can
  report on absent source is worse than no harness.
- Config keys are enforced structurally: every field of `etf.config.Config`
  must be read by a module outside `config.py`, or sit on the
  `PENDING_ENFORCEMENT` list in `tests/test_guards.py` with its task named.
  The guard walks the parse tree, not the text.

## Commands

    make install     create the venv and install
    make lint        ruff format --check and ruff check
    make typecheck   mypy strict
    make test        pytest
    make all         lint, typecheck, test
    make guards      the structural guards alone
    make mutations   the mutation harness
