# NPDExperiment

A replication. The AiTrader LLM council was fed price-derived numbers and
measured to a properly powered negative on 2026-07-27. This repository reruns
the numeric question under two changed conditions, frontier capability and
sane formulation.

## The load-bearing rule

Collection is not evaluation.

B.1 may call the model hundreds of times and store every ranking. B.1 may not
compute one rank IC, join one output to one forward return, or read any
statistic relating outputs to outcomes. B.2 fires once, later, after the
operator appends his registered prior as Amendment 0. The empty Amendment 0
slot blocks B.2.

`tests/test_guards.py` enforces this structurally. The forward-returns store
has exactly one permitted reader, `npd.eval.evaluator`. Any other module that
names it fails the seal guard.

## Standing rules

1. Absence is a recorded state, never a synthesized value. Seven historical
   fabrications in the predecessor were each a plausible value produced from
   absent input. `npd.absence` makes absence a type that refuses coercion to a
   number.
2. Every config field has an enforcement site. Six config keys in the
   predecessor were enforced nowhere. `tests/test_guards.py` fails when a
   field in `npd.config.Config` is referenced by no other module.
3. The five call states are never merged. `stored`, `no_data`, `model_failed`,
   `excluded_pre_cutoff`, `source_failed`. `model_failed` is operational
   health. `excluded_pre_cutoff` is sample composition.
4. Per-model inference is primary. Pooled numbers are descriptive and never
   touch a verdict.
5. No confidence field exists in version one. The ranking is the entire output.

## Boundaries

- The gate model is `gpt-5-2025-08-07`, the dated snapshot. Never the bare
  `gpt-5` alias. An alias silently repoints when a successor ships.
- Read-only source paths, and only these two:
  `~/Documents/GitHub/AiTrader/analysis_bars.db` and
  `~/Documents/GitHub/AiTrader/backtest/universe.py`.
  Opened through a SQLite immutable read-only URI in `npd.data.source`.
- `news_experiment.db` is never opened. The news-drift collection runs nightly
  at 22:30 UTC and must not be disturbed.
- HFExperiment is closed and read-only. Borrow its patterns by copying, never
  by importing.
- Nothing is pushed to any public remote.
- `.env` holds the API key at mode 600. The value is never printed, logged,
  committed, or echoed.

## Layout

    src/npd/
      absence.py      recorded absence, refuses coercion
      callstate.py    the five states
      config.py       frozen registered parameters
      window.py       derive the window from the verified cutoff
      power.py        minimum detectable rank IC
      section0.py     the coverage verdict
      ledger/         append-only spend and evidence ledgers
      data/           source boundary, ported universe, panels, features
      baselines/      the three local baselines
      collect/        the collector and its adapters
      eval/           B.2 only. The sole reader of forward returns.

## Writing

Clear, spartan, active voice. No em dashes. No semicolons. No filler
adjectives.

## Commands

    make install    create the venv and install
    make all        lint, type, test
    make guards     the structural guards alone
    make b0         build the data layer
    make b0b        the collector mock scenarios
    make b1         the live gate collection
    make status     collection status without calling anything
