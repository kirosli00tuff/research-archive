# The collection substrate — one of each, views on top

Registered 2026-08-28 (register Stage A.0 Task 3), before any successor
measurement. The register's three hypotheses share **one** collection
substrate; nothing is duplicated per hypothesis, and nothing per-hypothesis
touches a payload. The H1 collectors are the substrate — they were built,
measured, and mutation-tested in H1's Stage A and carry over unchanged in
role:

| substrate piece | module | role, unchanged | per-hypothesis extension |
|---|---|---|---|
| **One census** | `npl.census` | enumerate every dex, first-candle + first-funding timestamps, tags, delisted flags — blind by construction | none; views read census rows |
| **One watcher** | `npl.watcher` | hourly poll, birth rows, seals, loud refusals | A.3 Task 2: on each birth, the entry-anchor pass assigns the H2 control (trailing-only) and takes the two-leg l2Book snapshot |
| **One funding recorder** | `npl.archive` | per-instrument sealed raw pages, cursor-resumable, daily advance under the soft budget | A.3 Task 3: the fresh plan (`data/state/fresh_plan.jsonl`) queues every fresh event and assigned control |
| **One checkpoint scheduler** | `npl.checkpoints` | +2 / +32 / +92, catch-up window, loud expired records | A.3 Task 4: pair legs checkpoint alongside their events; coverage viewed per hypothesis |

**Per-hypothesis eligibility views on top** (`npl.register.views`): pure
functions from fresh events plus registered pre-entry inputs to eligibility
decisions with exclusion reasons counted —

- `h2_pairable_view` — fresh events with at least one Section 6 candidate
  on their dex (census dates; coverage enforced at assignment).
- `h3_main_dex_view` — the mechanical instrument-class rule; reads the dex
  field only.
- `h4_conditioned_view` — one view per registered threshold cell over the
  signed trailing 168-hour mean hourly funding at entry (pre-entry feature,
  standing rule 13).

**Every view refuses the generating sample first** (`npl.register.
generating_sample`, `data/state/generating_sample.json`, 312 IDs): the H1
retro events are usable for power assumptions and never admissible to a
successor statistic. The refusal is produced by test.

**The config guard extends to the new keys** (`npl.config` + the parse-tree
guard in `tests/test_guards.py`): every register key — the familywise
budget, the per-hypothesis true shares, the H4 grid, the register assistant
priors — has an enforcement site or a named PENDING entry that must burn
down by the end of A.3 (currently exactly one: `h2_cost_floor_multiple`,
consumed by the A.3 Task 5 dark reader).

**Per-hypothesis latches and readers come later and dark** (A.3 Task 5,
survivors only): one reader per surviving statistic against synthetic
fixtures with known answers to the digit, one latch per hypothesis, never
pointed at real sealed data before that hypothesis's own registered Stage
B — pinned by test, exactly as H1's verdict machinery was.

**Quarantine, standing (Amendment 4, standing rule 12):** the spent H1
read surface (`reports/stage_b/`, the latch, `npl.stageb.*`) is reachable
from no successor module — AST string pin plus import isolation in
`tests/test_guards.py`, refusals produced on synthetic offenders.
