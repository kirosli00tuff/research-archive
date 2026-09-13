# TASK 8 — The five registered mutations

**Outcome: all five behave as registered.** Each was applied to **real source**,
the check that should catch it failed, the file was restored byte for byte, the
check came back green, and the whole suite is green on the restored tree.

Machine-readable evidence: `reports/mutations/mutations.json`.

---

## 8.1 Results

| # | mutation | file | check | mutated | restored |
|---|---|---|---|---|---|
| 1 | a `whatIf` literal is flipped to `False` | `src/mbt/broker.py` | no-transmit scan | **FAILED**, rule `whatif_false_literal` | green |
| 2 | the `whatIf` flag comes from an expression, not a literal | `src/mbt/broker.py` | no-transmit scan | **FAILED**, rule `whatif_not_a_literal` | green |
| 3 | a session trusts its declared environment over the connected account | `src/mbt/provenance.py` | `tests/test_guards.py` | **FAILED** | green |
| 4 | a paper margin becomes admissible to a gate | `src/mbt/gates.py` | `tests/test_guards.py` | **FAILED** | green |
| 5 | the deciding latch's spent check is inverted | `src/mbt/latch.py` | `tests/test_guards.py` | **FAILED**, 4 tests fired | green |

**Whole suite after restore: green. Failures: 0.**

Mutation 2 is the sharpest of the five. `bool(1)` evaluates to `True`, so the
package still behaves correctly and every run-time check still passes. What is
lost is the **static** guarantee, and the guard fires on the loss alone.

Mutation 5 tripped **four** tests rather than one. A mutation that trips several
guards is stronger evidence than one that trips a single guard, so the artifact
names them all rather than printing only the last line.

## 8.2 The mutation harness found a real defect, which is the argument for having one

**Mutations 1 and 2 stayed GREEN on the first run.** Both edited the `whatIf`
flag on the package's only order construction, and the no-transmit scan did not
notice.

**Cause.** `build_short_option_order` took the order class as a **parameter**, so
the call site read `order_cls(...)`. Guard 1 matched call sites against a list of
known constructor names — `Order`, `LimitOrder`, `MarketOrder` and so on — and
`order_cls` was not among them. **The one order construction in the package was
outside the guard that exists to check it.**

**This was not caught by review, by mypy, by ruff or by 156 passing tests.** It
was caught by flipping the flag and finding that nothing broke.

**Two fixes, applied together, because they close different shapes of the hole:**

1. **The specific fix.** `broker.py` now constructs `Order` directly rather than
   through an injected class, so the site is covered by name. The class was
   injected for testability, and the test now exercises the **real** `ib_async`
   `Order` instead of a stub, which is better evidence anyway.
2. **The general fix.** The scan now holds **any** call site carrying a `whatIf`
   keyword to the literal requirement, keyed on the **argument** rather than on
   the callee name. A constructor reached through a parameter, a factory or an
   alias is now covered regardless of what it is called.

`tests/test_guards.py::test_guard_one_covers_a_call_whose_callee_is_not_a_known_constructor`
pins the general fix against three shapes of the defect.

## 8.3 Bytecode is purged before every run

**Purged first, every time**, and the purge is verified rather than assumed:
running it against a tree holding 3 `__pycache__` directories removed all 3.

The defect this prevents: CPython validates a cache entry on the source mtime in
**whole seconds** and the source size. A mutation that changes one token can
leave both identical, so a restore inside the same second can leave the
**mutated** bytecode valid, and the harness reports a result from source that is
no longer on disk. A predecessor's restore once read as still-red for exactly
this reason.

The run log shows `0 bytecode caches purged` at each step, and that is correct
rather than a failure: every subprocess runs with `PYTHONDONTWRITEBYTECODE=1` and
`-p no:cacheprovider`, so no cache is created to purge. **The purge is the second
of two defences, not the only one**, and it is kept because the environment
variable protects only processes this harness launches.

## 8.4 What the two artifacts show, and why both are needed

They are not the same claim.

| artifact | shows |
|---|---|
| `reports/guards/refusals.json` | each guard **refusing when exercised**, with the exception type and message it actually produced |
| `reports/mutations/mutations.json` | each test **detecting the guard being disabled**, on real source |

**A guard can refuse correctly while its test asserts nothing**, and only the
second catches that. Mutations 1 and 2 are the proof: the refusal artifact showed
Guard 1 refusing on synthetic sources the whole time, while the real call site
sat unchecked.
