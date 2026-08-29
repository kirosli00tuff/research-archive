# CLAUDE.md — operating rules for PMExperiment

Read `README.md`, `REGISTRATION.md`, `DECISIONS.md` and `progress.md` before
doing anything in this repository.

## What this project is

A measurement-only test of whether prediction-market prices are mis-calibrated
by enough to survive the costs a Canadian retail participant actually pays.

**It never trades.** No account, no credential, no order, no position, no
execution path, in this stage or any planned one. Kalshi market data and
settlement history are public and are read without an account.

**A documented negative is a valid and expected outcome. So is BLOCKED.**

## Standing rules

1. **Every prompt states a measured ETA per task**, derived from probes or from
   comparable measured work, before the work starts.
2. **Pre-register before results.** Section 0 is committed before the first
   request. Registered values change only by a numbered amendment in Section 17
   carrying its own evidence. Nothing edits in place.
3. **No first moment before the gate.** No statistic relating a price to an
   outcome is computed until the power gate has fired. The gate reads counts
   and dispersion only.
4. **Measured behaviour beats documentation.** Probe and measure. Record the
   figure and its date. A documented rate limit is a claim, not a measurement.
5. **Refusals fail closed.** A source that cannot be read is reported as
   unavailable, never as empty. Absent data is not measured absence.
6. **Report on access rather than pretending to report on the hypothesis.** If
   the data cannot be reached, Section 0 says so and the stage ends there, as a
   valid outcome.
7. **Union time intervals before summing.** Never trust append order across
   processes.
8. **A gate that has never failed is not a gate.** Every guard carries a test
   that fails when the guard is removed.
9. **Do not tune a filter to increase a sample.** Register it, then report what
   it yields.
10. **Ambiguity is a first-class category.** A contract that cannot be
    unambiguously classified is counted as ambiguous and attributed to nothing.

## The precedent this repository is built on

NPDExperiment closed at *unresolved-at-achievable-power*: realized minimum
detectable contrast **0.0512** against an effect band of **0.01 to 0.05**,
discovered after **415 days** of collection in the same session that read the
result. Its ADR-007 had registered the risk in advance and the arithmetic still
landed too late.

InsiderExperiment registered its power gate in Section 0 explicitly because of
that, and fired **BLOCKED at 49.35 bp before spending**.

**Follow Insider.** Compute the minimum detectable effect from dispersion and
sample size alone, commit the gate before the measurement it judges, and treat
BLOCKED as cheap and legitimate.

## Development

- Python with `uv`, `ruff`, `mypy --strict`, `pytest`, `pre-commit`.
- `make lint`, `make typecheck`, `make test` must be green before any push.
- No credential-shaped string in any tracked file or anywhere in git history.
- `.env` and `*.session` stay gitignored and untracked.

## Scope guard

Canadians cannot trade on Kalshi directly. The permitted-subset filter is a
**registered analysis step**, never a trading plan. Nothing in this repository
is trading advice or a suggestion to trade, and no output may be framed as one.
