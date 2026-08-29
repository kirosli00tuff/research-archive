# A.4 TASK 2 — the mutation harness

**Run 2026-08-29. n = 12 mutations applied to real source, each restored green afterwards. Bytecode is purged before every run.**

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
| 11 | remove the secret redactor | a credential value reaches a sealed file, a ledger row and the console | CAUGHT | yes | `FAILED tests/test_guards.py::test_no_credential_value_reaches_a_recorded_string` |
| 12 | force the tape verdict to SAME_TAPE | a single-venue feed is scored against the registered agreement bars and BLOCKED-4 fires on entitlement while recording it as integrity | CAUGHT | yes | `FAILED tests/test_tape.py::test_one_ulp_below_the_lower_same_tape_bar_is_ambiguous` |
