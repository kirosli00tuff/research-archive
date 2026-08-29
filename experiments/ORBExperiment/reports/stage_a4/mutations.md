# A.4 TASK 2 — the mutation harness

**Run 2026-08-29. n = 10 mutations applied to real source, each restored green afterwards. Bytecode is purged before every run.**

Two mutations are of a different kind and are marked *GUARD STOPPED BINDING*: the point is to show a guard **failing to catch** something, which is how a boundary fixture placed comfortably inside its boundary goes unnoticed.

| # | mutation | what it would have cost | expected | detected | suite |
|---|---|---|---|---|---|
| 1 | delete the blindness pin | with the pin deleted a priced-bar read is reachable and nothing complains | GUARD STOPPED BINDING | yes | `` |
| 2 | coerce a recorded absence to zero | a missing bar becomes a measured zero and every coverage figure inflates | CAUGHT | yes | `FAILED tests/test_absence.py::test_absent_refuses_float_and_int - Failed: DID...` |
| 3 | merge rate_limited into no_data | a vendor refusal is counted as an empty session and the denominator inflates | CAUGHT | yes | `` |
| 4 | move a boundary fixture off the registered 09:35:00.000 boundary | a fixture inside its boundary lets a moved threshold pass unnoticed | GUARD STOPPED BINDING | yes | `` |
| 5 | replace the DST-aware Eastern anchor with a fixed UTC offset | the opening range is taken from the wrong five minutes on a third of the sample | CAUGHT | yes | `` |
| 6 | read a bar stamped on or after 2016-01-04 through the carve-out | a verdict-window observation leaks into the power computation that plans the verdict | CAUGHT | yes | `FAILED tests/test_preperiod.py::test_the_boundary_instant_itself_is_refused` |
| 7 | make the sealed comparator return a bar value to a caller | the single blindness exception becomes a hole; price leaves the seal | CAUGHT | yes | `FAILED tests/test_guards.py::test_comparator_returns_no_bar_value - Assertion...` |
| 8 | point the verdict module at real bars before the latch | the dark strategy becomes reachable from a Stage A collection path | CAUGHT | yes | `FAILED tests/test_guards.py::test_no_stage_a_module_imports_a_latched_module` |
| 9 | let a manifest seal attest the open session | the seal describes a partial file and teaches readers to expect mismatches | CAUGHT | yes | `FAILED tests/test_collector.py::test_the_open_session_is_never_sealed - Faile...` |
| 10 | allow a second read of a spent window | the hypothesis is voided and nothing says so | CAUGHT | yes | `FAILED tests/test_latch.py::test_a_second_read_of_the_same_window_is_refused` |

---

## What each mutation would have cost, and what caught it

| # | caught by |
|---|---|
| 2 | `test_absence.py::test_absent_refuses_float_and_int` |
| 3 | the `CallStateTally` family split — `rate_limited` and `no_data` collapse to one enum member |
| 5 | `test_guards.py::test_no_module_builds_eastern_from_a_fixed_offset` and the whole DST suite |
| 6 | `test_preperiod.py::test_the_boundary_instant_itself_is_refused` |
| 7 | `test_guards.py::test_comparator_returns_no_bar_value` |
| 8 | `test_guards.py::test_no_stage_a_module_imports_a_latched_module` |
| 9 | `test_collector.py::test_the_open_session_is_never_sealed` |
| 10 | `test_latch.py::test_a_second_read_of_the_same_window_is_refused` |

## The two that were supposed to go green, and why

**Mutation 1 — delete the blindness pin.** With `violations` emptied in the
guard, a module reading `bar["close"] + bar["volume"]` was added to
`orb/calendar.py` and **the suite stayed green**. That is the demonstration: the
blindness property lives entirely in that one assertion, and nothing else in the
repository would notice a priced-bar read appearing in a collection module.

**Mutation 4 — move the boundary fixture off the boundary.** This one produced a
finding the harness was not looking for.

**The first attempt failed, and the failure was informative.** Disabling the four
`test_preperiod.py` boundary fixtures and shifting
`CONFIG.pre_period_end_ms` by a day **did not** make the suite green: it was
caught by `test_dark.py::test_a_pre_period_bar_must_actually_be_pre_period`,
which pins the same boundary **independently**, through `Bar.__post_init__`
rather than through `preperiod.py`. A third site then caught it — the
`test_known_answers.py` assertion that every one of the ten hand-computed
fixtures is stamped strictly before the boundary.

**The carve-out boundary is defended in three independent places**, and it took
**seven edits across three test modules plus the source** before the guard
stopped binding. That is the opposite of the InsiderExperiment failure mode, and
it is recorded because it was measured rather than intended: the redundancy was
not designed in, it was discovered by trying to defeat it.

Once all three sites were disabled the suite went green with the boundary moved
a full day — which is the lesson the mutation exists to show. **A fixture
comfortably inside its boundary lets a moved threshold pass unnoticed**; the only
reason it could not pass unnoticed here is that three separate fixtures sit
**on** the boundary rather than near it.

## Method

- Every mutation is applied to **real source** (or, for the two
  guard-stops-binding cases, to real source and the real tests), never to a copy.
- **Bytecode is purged before every run** — `__pycache__` is removed under the
  repository, excluding `.venv`. A harness that can report on absent source is
  worse than no harness, because a stale `.pyc` reports success from code that
  no longer exists.
- After each mutation the source is **restored and the suite re-run**, and a
  failure to return green is itself counted as a harness failure. **n = 10
  mutations, 0 harness failures, 0 tests left red.**
