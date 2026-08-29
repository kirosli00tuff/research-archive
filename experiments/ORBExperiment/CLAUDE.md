# CLAUDE.md — ORBExperiment operating manual

Read this file at the start of every coding session. It is the contract for how
work happens in this repository.

## What this project is (permanent, stated from the first commit)

> **ORBExperiment is a measurement-only test of one hypothesis: among US common
> stocks with elevated opening relative volume, a breakout of the first
> 5-minute regular-session range predicts continuation to the session close, by
> enough to clear modeled commissions, fees, borrow and slippage, out of sample
> from 2023-01-03 forward.**
>
> **Stage A never trades, never touches capital, and never reads an outcome
> value.** There is no broker credential, no order, no position, no signer, and
> no stage in which one is planned. The output is a registered design, a
> measured bar revision rate, a measured cross-vendor agreement rate, a
> measured delisted-name count, a frozen cost model, a power verdict, armed
> collectors, and eventually a documented verdict either way. **A documented
> negative is a valid and expected outcome.**

**The measurement that decides this repository is not the return. It is bar
integrity.** `STAGE A.1 TASK 3` and `STAGE A.1 TASK 4` are the experiment. Two
precedents force this:

- **MLCryptoEngine H11** died on a **measured 75-day publication lag** in a free
  flow source with whole-file regeneration that revised past rows — and the lag
  was **discovered rather than registered**.
- **Concretum Research** ran identical opening-range code against four vendors
  with identical dates, parameters and starting capital and reported final
  portfolio values from **226,000 to 726,000 USD** — a threefold spread from
  vendor choice alone.

If bar integrity fails here, no model in this repo can mean anything, and
**BLOCKED is the correct and cheap answer**.

## Standing rules, in force for every task

1. **Log the operator prompt verbatim to progress.md before any other work.**
2. **State an ETA before arming each task. Record actual against ETA after.**
3. **Commit at every task boundary. Push to `origin/main` after every commit.**
   A task is not complete until its commit is on the remote. Never force-push,
   never rewrite a pushed commit, never amend a pushed commit.
4. **Measured beats documented.** Verify every external figure live before
   relying on it. A tier limit printed on a vendor's pricing page is
   **documented, never measured**, and the measured limit wins. The
   MLCryptoEngine ADR-055 fee re-verification pattern applies to every vendor
   and broker figure in this repo.
5. **Absence is a recorded state, never a synthesized value.** A refusal is
   loud, never a silent skip. (`orb.absence`)
6. **Ledgers are append-only and fsynced.** A truncated line is reported, never
   repaired. (`orb.ledger`)
7. **Operational health and sample composition never merge.** Call states:
   `stored`, `no_data`, `source_failed`, `rate_limited`, `excluded_ineligible`,
   `expired`, `halted`. (`orb.callstate` — two disjoint enums, no supertype)
8. **Outcome blindness**, stated exactly in the section below. Stage A parses
   row counts, timestamps, ticker symbols and exchange codes only. **No price
   value, no volume value, and nothing derived from either leaves a sealed
   writer until the registered Stage C latch opens.**
9. **The pre-period carve-out is the one exception**, stated in full below.
10. **Union time intervals before summing.** Order multi-process logs by clock,
    never by file position.
11. **Spend nothing** without an explicit operator instruction. Free and trial
    tiers only in Stage A. A request ledger with a per-vendor daily cap
    **charges before sending**. (`orb.ledger.RequestLedger`)
12. **Terms of service bind.** Record `robots.txt` and the published terms
    verbatim for every vendor **before the first repeated fetch**. If automated
    collection is disallowed, record it loudly and route the access verdict
    accordingly. **Do not proceed against a stated prohibition.** The
    HFExperiment Wealthsimple finding is the precedent.
13. **Every figure travels with its n in the same sentence.**
14. **Session times are stated in US Eastern with the UTC offset named**,
    because the experiment is anchored to a cash-session clock that shifts
    twice a year. **Never store a naive timestamp.** (`orb.sessionclock`)

## The blindness field lists, stated exactly

**Readable outside the sealed writers, in Stage A:** ticker symbol, exchange
code, listing and delisting dates, bar timestamp, bar count per session,
session date, and the vendor response status code. **Nothing else.**
(`orb.seal.READABLE_FIELDS`)

**Never readable outside the sealed writers, in Stage A:** `open`, `high`,
`low`, `close`, `volume`, `vwap`, trade count, `bid`, `ask`, **or any function
of them, under any spelling, in any module.** Pinned repo-wide by
`tests/test_guards.py::test_no_module_reads_a_priced_bar_field_anywhere`, which
**walks the parse tree rather than the text** and catches the attribute, the
subscript and the `.get`/`.pop`/`.setdefault` forms alike.
(`orb.seal.PRICED_BAR_FIELDS`)

**The sealed comparator is the single exception and it is a sealed writer.** It
reads price and volume values from two vendors, emits **only aggregate mismatch
counts and rates**, and **returns no bar value to any caller**. Pinned by
`tests/test_guards.py::test_comparator_returns_no_bar_value`.

**The universe module, the signal module and the verdict module are built dark
in Stage A** against synthetic fixtures with known answers, and are **never
pointed at real bars before the Stage C latch**. Pinned by test.

## The pre-period carve-out

**Power inputs may read US equity bars stamped strictly before
2016-01-04T14:30:00.000Z. Every other bar read is sealed.** The rationale:
2016-01-04 is the first session of the registered in-sample window, so the
window before it sits **outside both the in-sample and the holdout samples**,
and reading it cannot leak a single observation any verdict will be computed
on. The E2 economic-power computation needs a per-trade dispersion figure to
size a net edge against a modeled cost; taking that from the test window would
be **reading the outcome to plan the test of the outcome**, and inventing it
would register a number this repository did not measure. **The enforcement site
is `orb.preperiod.require_pre_period` and `orb.preperiod.gate_pre_period`, the
boundary is `CONFIG.pre_period_end_ms` (2016-01-04T14:30:00.000Z, exclusive),
and the pin is exercised by `tests/test_preperiod.py` with fixtures sitting
exactly on the boundary — one millisecond before it passes, the instant itself
is refused.** Two structural guards hold it there: no module outside
`config.py` may hardcode the literal, and no module outside `preperiod.py` may
read it from config.

## Non-negotiable rules

1. **Pre-register before results.** `REGISTRATION.md` is append-only; an
   amendment is dated, reasoned, and states exactly what data existed when it
   was made. **Nothing above an amendment line is ever edited.**
2. **No coverage, revision, agreement, delisting, trigger-rate or slippage
   figure is registered before it is measured.** The NPLExperiment correction
   governs this repo: a main-dex accrual figure near 9.4 events per month
   entered a registration as a planning number and measurement falsified it at
   **0.5, n = 3 over 182 days**, killing H3 on a figure rather than on the
   world. Every such figure here is named as an A.1 or A.2 **measurement
   target**, never as an input.
3. **Secrets never enter the repo — and credentials are required.**
   **AMENDED 2026-08-29.** The original rule read, and is preserved here
   unedited so the correction is auditable:

   > ~~**Secrets never enter the repo — and none are needed.** `.env.example` is
   > empty on purpose. No API key exists anywhere in this project.~~

   **The second half was falsified by measurement**, not by preference.
   `docs/ACCESS.md`, A.1 TASK 1, 2026-08-29: **`n = 9` vendors, `0` usable
   without a credential.** The two that serve keylessly both publish
   `User-agent: * / Disallow: /`; two more disallow the exact API path a
   collector needs; **the five whose terms permit collection all refused
   without a key**, refusal payloads recorded verbatim. This is the
   NPLExperiment shape — a planning number entering a rule and measurement
   falsifying it — and it is amended rather than contradicted silently.

   **The amended rule, in force:**
   - **Credentials are required.** Measurement established this; the line is
     `docs/ACCESS.md` → *"PERMITTED and usable today: 0 of 9."*
   - **Keys live in `.env`, which is git-ignored** and confirmed so by
     `git check-ignore` before any credentialed request is sent.
   - **`.env.example` carries names only and never values.**
   - **Guard 8 enforces redaction at the recording boundary** — the sealed
     writer, the append-only ledger and the HTTP response object — because a
     credentialed endpoint can return the key inside its own error body and
     `docs/ACCESS.md` records refusal payloads verbatim. Redaction is
     **deterministic**, so the byte-level revision comparison survives it.
   - **What may be recorded about a credential:** its variable name, whether it
     is present, and its character length. **What may not:** the value, any
     prefix, any suffix, and **any hash** — a hash of a 32-character key is a
     confirmation oracle for a guess.
   - **No key is ever committed**, and the first half of the original rule —
     *secrets never enter the repo* — **stands unchanged and unweakened.**
4. **The operator prior slot (REGISTRATION.md Section 13) is filled only by the
   operator.** The assistant prior recorded beside it is not the operator's
   number. **The empty slot blocks the Stage C latch structurally.** The
   NPDExperiment Amendment 0 lesson: an adopted prior corrupts the calibration
   ledger.
   **State as of 2026-08-29: the slot is FILLED**, by the operator, at **0.30,
   label `INDEPENDENT`** (Amendment 5). The rule above is unchanged and still
   binds — the assistant never fills it. **Section 10 clause 2 now reads
   satisfied; clauses 1 and 3 do not, and the latch stays closed.**
5. **Stage C opens the sealed in-sample read exactly once**, behind a latch
   written first, recording module hashes. **Stage D opens the holdout exactly
   once**, behind its own latch. **A second read of either window voids the
   hypothesis.** Every value inside a read is quarantined from any successor
   code path by AST pin and by test.
6. **Pacing is measured per endpoint, never per host.** solattn ADR-021: one
   endpoint refused 47.5 percent of 1,863 attempts while a second endpoint on
   the same host and the same IP took 0 of 360. **An unmeasured endpoint is not
   a licence to speed up.**

## Coding standards

- Python 3.13+; type hints on all signatures; `ruff format`, `ruff check` and
  `mypy --strict` pass clean. **`make all` is the gate.**
- Anything with logic gets a pytest test. Real tests, not smoke tests, with
  **boundary fixtures ON the registered boundary** — a fixture comfortably
  inside its boundary lets a moved threshold pass unnoticed (InsiderExperiment
  mutation lesson).
- Frozen dataclasses, pure functions over records, many small modules.
- Errors handled explicitly; **an error never quietly becomes a data
  condition** — a `rate_limited` is never a `no_data`.
- The mutation harness **purges bytecode before every run**; a harness that can
  report on absent source is worse than no harness.
- Config keys are enforced structurally: every field of `orb.config.Config`
  must be read by a module outside `config.py`, or sit on
  `PENDING_ENFORCEMENT` in `tests/test_guards.py` **with its task named**. The
  guard walks the parse tree, not the text, and a stale entry fails too.
- **Fix the source, not the guard.** Guard 5 caught `Path.open` in
  `orb/ledger.py` on its first run against real source; `iter_rows` was
  rewritten to use `read_text`. The single allowlisted receiver anywhere is
  `os`, for `os.close(fd)`, named explicitly with its reason.

## Commands

    make install     create the venv and install
    make lint        ruff format --check and ruff check
    make fmt         ruff format and ruff check --fix
    make typecheck   mypy strict
    make test        pytest
    make all         lint, typecheck, test
    make guards      the structural guards alone
    make mutations   the mutation harness

## What a fresh session reads first

`CLAUDE.md` (this file) → `REGISTRATION.md` Sections 0 and 8–10 →
`HYPOTHESES.md` → `docs/HANDOVER.md` → `progress.md` last entry. **Do not touch
`REGISTRATION.md` above an amendment line, and do not point `orb.verdict` at a
real bar under any circumstance before the Stage C latch exists.**
