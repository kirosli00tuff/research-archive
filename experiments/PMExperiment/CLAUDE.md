# CLAUDE.md — operating rules for PMExperiment

Read `README.md`, `REGISTRATION.md`, `HYPOTHESES.md`, `DECISIONS.md`,
`progress.md` and `report.md` before doing anything in this repository.

## What this project is

A measurement-only test of whether prediction-market prices are mis-calibrated
by enough to survive the costs a Canadian retail participant actually pays.

**It never trades.** No account, no credential, no order, no position, no
execution path, in this stage or any planned one. Kalshi market data and
settlement history are public and are read without an account.

**A documented negative is a valid and expected outcome. So is BLOCKED.**

## Standing rules, in force for every task

1. **Log the operator prompt verbatim to `progress.md` before any other work.**
   Entry 0 exists before the first request.
2. **State a measured ETA before arming each task** — derived from a probe or
   from comparable measured work, never guessed — **and record actual against
   it** in the entry that reports the task.
3. **Commit at every task boundary. Push to `origin/main`** after each stage.
4. **Measured beats documented.** Verify every external figure live. A
   documented rate limit is a claim, not a measurement.
5. **Absence is a recorded state, never a synthesized value.** A source that
   cannot be read is reported unavailable, never as empty.
6. **Ledgers are append-only and fsynced.** A truncated line is reported, not
   repaired.
7. **Operational health and sample composition never merge.** Coverage and
   filtering are separate reported quantities.
8. **No first moment before the gate.** No statistic relating a price to an
   outcome is computed until the power gate has fired. The gate reads bucket
   counts and dispersion only.
9. **Do not tune a filter to increase a sample.** Register it, then report what
   it yields. The sample it costs is a first-class output.
10. **Union time intervals before summing.** Never trust append order across
    processes.
11. **Spend nothing** without an explicit operator instruction. Stage A is
    zero-cost by design; every source is a keyless public endpoint.
12. **Terms of service bind.** Record `robots.txt` and the published terms
    before any repeated fetch, and report what they permit.
13. **Every figure travels with its n in the same sentence.**
14. **A gate that has never failed is not a gate.** Every guard carries a test
    that fails when the guard is removed, verified by mutation.
15. **Ambiguity is a first-class category.** A contract that cannot be
    unambiguously classified is counted ambiguous and attributed to nothing.
16. **Report on access rather than pretending to report on the hypothesis.** If
    the data cannot be reached, Section 0 says so and the stage ends there.

## The precedent this repository is built on

NPDExperiment closed at *unresolved-at-achievable-power*: realized minimum
detectable contrast **0.0512** against an effect band of **0.01 to 0.05**,
discovered after **415 days** of collection in the same session that read the
result. Its ADR-007 had registered the risk in advance and the arithmetic still
landed too late.

InsiderExperiment registered its power gate in Section 0 explicitly because of
that, and fired **BLOCKED at 49.35 bp before spending**.

**Follow Insider.** Compute the minimum detectable effect from dispersion and
bucket counts alone, commit the gate before the measurement it judges, and
treat BLOCKED as cheap and legitimate.

## Development

- Python with `uv`, `ruff`, `mypy --strict`, `pytest`, `pre-commit`.
- `make lint`, `make typecheck`, `make test` green before any push.
- No credential-shaped string in any tracked file or anywhere in git history.
- `.env` and `*.session` stay gitignored and untracked.

## Scope guard

Canadians cannot trade on Kalshi directly. The permitted-subset filter is a
**registered analysis step**, never a trading plan. Nothing in this repository
is trading advice or a suggestion to trade, and no output may be framed as one.
