# Mutation results

Each mutation was applied to real source, not to a copy. The harness restores the exact original bytes whether the run passes or fails, and reruns the full suite afterwards to prove the restore worked.

| mutation | target | guard | caught | restored green |
|---|---|---|---|---|
| 1. carry a value forward across a missing bar | `src/npd/data/features.py` | `tests/test_absence.py` | yes | yes |
| 2. merge model_failed into source_failed | `src/npd/callstate.py` | `tests/test_guards.py` | yes | yes |
| 3. let a non-evaluator module read the sealed forward returns | `src/npd/collect/collector.py` | `tests/test_guards.py` | yes | yes |
| 4. add a config field with no enforcement site | `src/npd/config.py` | `tests/test_guards.py` | yes | yes |
| 5. let a real ticker reach a prompt | `src/npd/data/anonymize.py` | `tests/test_anonymization.py` | yes | yes |

**All five caught and restored: True**

## 1. carry a value forward across a missing bar

Fill a hole in a feature span with the previous close, which is the exact shape of the seven historical fabrications.

Target `src/npd/data/features.py`. Guard `tests/test_absence.py`.

```
E       AssertionError: assert 'ret_20' in set()

tests/test_absence.py:71: AssertionError
=========================== short test summary info ============================
FAILED tests/test_absence.py::test_a_missing_bar_inside_the_span_produces_an_absence_not_a_number
FAILED tests/test_absence.py::test_every_feature_reports_the_hole - Assertion...
```

## 2. merge model_failed into source_failed

Collapse operational health into a data fault, destroying the distinction between a model that could not answer and a source that could not serve.

Target `src/npd/callstate.py`. Guard `tests/test_guards.py`.

```
E        +  and   <CallState.MODEL_FAILED: 'source_failed'> = CallState.SOURCE_FAILED

tests/test_guards.py:155: AssertionError
=========================== short test summary info ============================
FAILED tests/test_guards.py::test_five_distinct_call_states - AssertionError:...
FAILED tests/test_guards.py::test_model_failed_and_source_failed_stay_separate
```

## 3. let a non-evaluator module read the sealed forward returns

Give the collector a peek at the outcomes it is collecting against.

Target `src/npd/collect/collector.py`. Guard `tests/test_guards.py`.

```
E       assert not ['collect/collector.py']

tests/test_guards.py:98: AssertionError
=========================== short test summary info ============================
FAILED tests/test_guards.py::test_only_the_evaluator_mentions_the_sealed_store
FAILED tests/test_guards.py::test_the_forward_return_table_is_read_only_through_a_guarded_path
```

## 4. add a config field with no enforcement site

A knob that reads as registered and is enforced nowhere.

Target `src/npd/config.py`. Guard `tests/test_guards.py`.

```
E       AssertionError: config fields with no enforcement site anywhere under src/npd: ['decorative_knob']. A key enforced nowhere is decoration.
E       assert not ['decorative_knob']

tests/test_guards.py:61: AssertionError
=========================== short test summary info ============================
FAILED tests/test_guards.py::test_every_config_field_has_an_enforcement_site
```

## 5. let a real ticker reach a prompt

Label each row with its own symbol, defeating anonymization.

Target `src/npd/data/anonymize.py`. Guard `tests/test_anonymization.py`.

```
FAILED tests/test_anonymization.py::test_no_real_ticker_appears_in_the_rendered_prompt
FAILED tests/test_anonymization.py::test_labels_are_letters_only - AssertionE...
FAILED tests/test_anonymization.py::test_no_label_equals_its_symbol - Asserti...
FAILED tests/test_anonymization.py::test_the_mapping_is_remapped_every_call
FAILED tests/test_anonymization.py::test_no_label_collides_with_any_symbol_in_the_same_panel
FAILED tests/test_anonymization.py::test_a_panel_of_two_letter_tickers_still_renders_cleanly
```
