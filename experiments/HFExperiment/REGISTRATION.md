# HFExperiment Registration

This document is the binding pre-registration for the H-F live execution experiment.
Sections beyond Section 0 land in Stage A.2. Amendments append. Nothing edits in place.

## Section 0: Broker outcome map

Registered 2026-08-23, before any broker measurement was taken. The three outcomes
below are fixed now so the broker answer cannot be read against a bar its own
measurement could see.

### GO

A broker accepts a Canadian resident individual account, serves US equities,
exposes an API that places orders and reads fills programmatically, and accepts
fractional quantities through that API at 45 USD per name.

Consequence: the settled configuration runs as recorded. 20 names at 45 USD.
900 deployed. 100 held as settlement and fee buffer.

### DEGRADED

A broker clears every bar except fractional-through-the-API.

Consequence, registered now: per-name notional rises to whole-share size. Book
width falls to what 900 USD supports at that size. Amendment 1 records that the
parameters were forced by execution mechanics rather than chosen, and states the
arithmetic. Whole-share sizing makes book width a function of share price. No
registered rule may inherit that property by accident. Task 4 of Stage A.1
measures the median share price of the top-20 book, which is the input that
decides whether this path is survivable at all.

### BLOCKED

No reachable broker clears the bars.

Consequence: phases C and D stop. Phase B proceeds unchanged, because the shadow
series needs no broker, no account, and no money. The signal question still gets
answered.

### Scope note

One week of live trading is enough to measure execution. One week is nowhere near
enough to measure signal. The verdict on the signal reads the shadow series and
only the shadow series.

## Amendment log

Append-only. No entries yet.
