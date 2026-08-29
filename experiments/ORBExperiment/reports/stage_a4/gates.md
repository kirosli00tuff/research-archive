# A.4 TASK 1 — the gates

**Run 2026-08-29.** `make all` is the gate: `ruff format --check`, `ruff check`,
`mypy --strict`, `pytest`.

| gate | result |
|---|---|
| `ruff format --check src tests` | **46 files already formatted** |
| `ruff check src tests` | **All checks passed** |
| `mypy` (strict, `warn_unreachable`) | **Success: no issues found in 46 source files** |
| `pytest` | **270 passed** |

## Every guard, exercised

| guard | pin | exercised by |
|---|---|---|
| 1 — recorded absence | `orb.absence.Absent` | refuses `float`, `int`, `index`, `+` both ways, `-`, `*`, `/`, ordering, `bool`, indexing, iteration, `len` — and mutation 2 |
| 2 — parse-tree config enforcement | `test_every_config_field_is_read_or_pending_with_its_task_named` | fired **four times** this session as fields came into use; a stale entry also fails |
| 3 — append-only fsynced ledger | `test_a_truncated_line_is_reported_never_repaired` | the damaged line survives on disk after reading |
| 4 — the seven call states | two disjoint enums, `combined_total()` raises | mutation 3 |
| **5 — priced-bar blindness** | `test_no_module_reads_a_priced_bar_field_anywhere` | mutation 1, plus **two real catches in this repository's own source** |
| **6 — the pre-period date pin** | `test_preperiod.py`, fixtures **on** the boundary | mutations 4 and 6 |
| **7 — the session clock** | `test_no_module_builds_eastern_from_a_fixed_offset` | mutation 5 |
| the sealed comparator's limit | `test_comparator_returns_no_bar_value` | mutation 7 |
| the latched modules' unreachability | `test_no_stage_a_module_imports_a_latched_module` | mutation 8 |
| the seal target | `test_the_open_session_is_never_sealed` | mutation 9 |
| the read latch | `test_a_second_read_of_the_same_window_is_refused` | mutation 10 |

## Guard 5's two real catches, recorded because they were not fixtures

1. **`Path.open` in `orb/ledger.py`**, on the guard's first run against real
   source at A.0 TASK 2. `open` is a bar field in every vendor dialect. **The
   source was changed, not the guard**: `iter_rows` now reads via `read_text`.
2. **The guard's own blindness to variable-alias access**, at A.1 TASK 3. The
   sealed comparator reads OHLC through `for alias in ("o", "open"): bar[alias]`,
   which a constant-subscript walk cannot see — **the guard reported zero reads
   from a module that reads every priced field on every bar.** A fourth detection
   form was added (a bare string constant naming a priced field), the field
   registry was moved to `orb/fields.py` so the declaration site does not flag
   itself, and findings are deduplicated by `(line, field)`.

**A guard that has never been shown to catch anything is an assertion about
nothing.** These two were caught in this repository's own source, on the days the
guards were written.
