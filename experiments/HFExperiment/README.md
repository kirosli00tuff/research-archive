# HFExperiment

H-F is 12-1 cross-sectional momentum, tested once in the AiTrader
cross-sectional round of 2026-07-26 and resolved on statistical power
rather than absent signal.

This repository runs two series.

The SHADOW series is the signal instrument. The registered book computed
daily from price data alone. No fills. No commissions. It accumulates the
statistics the verdict reads.

The LIVE series is the execution instrument. Actual fills at a real broker
at micro size. It measures what the shadow series cannot.

The difference between the two is the execution cost, measured directly.

Binding documents: REGISTRATION.md, DECISIONS.md, progress.md.
Broker measurement: docs/ACCESS.md.

## Layout

    src/hfexperiment/   the package
    scripts/            stage drivers
    tests/              pytest suite with mutation checks
    docs/               measured broker access
    reports/            stage evidence
