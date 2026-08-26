# InsiderExperiment

A net-of-cost survival test on Form 4 insider purchases. NPDExperiment closed
at unresolved-at-achievable-power: its realized minimum detectable contrast came
in at 0.0512 against a realistic effect band of 0.01 to 0.05, so the design
could not have detected an effect anywhere in the range the literature reports.
That was discovered after 415 days of collection and 6.9378 USD of spend, in the
same session that read the result.

## The load-bearing rule

The power question is answered before the alpha question.

Alpha is a first moment. Detectability is a second moment. The minimum
detectable effect depends on the portfolio's tracking error and its effective
number of independent periods, and neither requires knowing the mean. Stage A.1
computes the variance side, fires a registered verdict on it, and leaves the
mean sealed.

`insider.power` is structurally incapable of emitting a mean. It reads
`var/insider_dispersion.db`, which holds daily portfolio excess returns already
centered on their own mean, and the mean itself is never written there. The raw
series lives in `var/insider_sealed.db` and `insider.eval.evaluator` is its only
permitted reader. `tests/test_guards.py` fails when any other module names it.

## The governing rule

A negative is the expected outcome and a fully acceptable one. Do not soften a
specification to keep this alive. Do not substitute a friendlier cost
assumption, a narrower universe, or a longer hold after seeing a number.

## Standing guards

1. Absence is a recorded state, never a synthesized value. AiTrader Level 4
   computed whale scores from two empty tables and emitted plausible numbers.
   `insider.absence` makes absence a type that refuses coercion to a number.
2. Every config field has an enforcement site. Six Level 1 keys were once
   parsed, validated, printed at startup, and enforced nowhere.
   `tests/test_guards.py` fails when a field in `insider.config.Config` is
   referenced by no other module.
3. Append-only ledgers surviving restart, never mutated. `ledger/append_only.py`
   fsyncs before returning and reports a truncated final line rather than
   repairing it.
4. Refusals are demonstrated by producing them, never asserted. The Johnsen
   rejection and the unclassifiable insider are shown as produced artifacts in
   `reports/stage_a1/refusals.md`.
5. The eight recorded call states are never merged. Operational health
   (`unparseable`, `no_bar`) and sample composition (`filtered_*`,
   `outside_universe`) never share a representation.

## Boundaries

- Read-only source paths, and only these two:
  `~/Documents/GitHub/AiTrader/analysis_bars.db` and
  `~/Documents/GitHub/AiTrader/backtest/universe.py`. Opened through a SQLite
  immutable read-only URI in `insider.market.source`, hashed before and after.
- `news_experiment.db` is never opened. The news-drift collection runs nightly
  at 22:30 UTC and must not be disturbed.
- HFExperiment and NPDExperiment are closed and read-only. Borrow their patterns
  by copying, never by importing.
- SEC access only. Zero paid APIs. A User-Agent naming the requester with a
  contact email is mandatory, throttled to 8 requests per second against the
  SEC's stated 10 per second ceiling, with a local cache so a re-run never
  re-fetches.
- Nothing is pushed to any public remote.

## What Stage A.1 does not do

It reads no alpha, computes no abnormal return, fires no hypothesis verdict,
places no order, and spends no money. It answers whether the question is
answerable, and it answers that before anyone can see what the answer would
have been.

## Layout

    src/insider/
      absence.py            recorded absence, refuses coercion
      callstate.py          the eight states, never merged
      config.py             frozen registered parameters
      cost.py               the operator's measured cost band
      paths.py              every path, one place
      section0.py           the corpus gate and the power gate
      registration_check.py the operator prior gate
      ledger/               append-only fetch and evidence ledgers
      edgar/                throttle, client, bulk sets, full index, XML
      corpus/               classification, CMP routine rule, clusters
      market/               the read-only boundary, ported universe, local store
      portfolio/            calendar-time membership and daily returns
      power/                dispersion only. No first moment leaves here.
      eval/                 Stage B. The sole reader of the sealed store.

## Writing

Clear, spartan, active voice. No em dashes. No semicolons. No filler adjectives.

## Commands

    make install     create the venv and install
    make all         lint, type, test
    make guards      the structural guards alone
    make a1-market   copy the market data across the read-only boundary
    make a1-corpus   build the Form 4 corpus and fire the CORPUS gate
    make a1-power    compute the MDE and fire the power gate
    make mutations   apply the five registered mutations and restore
