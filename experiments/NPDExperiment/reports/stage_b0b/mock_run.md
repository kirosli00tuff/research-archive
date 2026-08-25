# Stage B.0b. Mock run evidence

Generated 2026-08-25T17:08:37.299405+00:00.

Gate model `gpt-5-2025-08-07`.

**Prompt template digest, frozen here and used by every B.3 replay:**

    9a174e0155fadfbf12906773ff26e3c13fb01d30c2a9207831520b02df54bbae

All five scenarios must pass before Stage B.1 sends a single real call.

| scenario | result |
|---|---|
| `clean` | PASS |
| `kill_resume` | PASS |
| `model_failed` | PASS |
| `source_failed` | PASS |
| `spend_refused` | PASS |

**Overall: PASS**

## clean

- `counts`: {'stored': 432, 'no_data': 0, 'model_failed': 0, 'excluded_pre_cutoff': 0, 'source_failed': 0}
- `calls_sent`: 432
- `servable_days`: 432
- `ranked_days`: 432
- `spend_usd`: 5.832

Result: **PASS**

## kill_resume

- `killed_after_calls`: 137
- `calls_before_kill`: 138
- `calls_after_resume`: 295
- `double_called_dates`: []
- `lost_commit_dates`: ['2024-10-31', '2024-11-01', '2024-11-04']
- `lost_dates_recalled`: []
- `reconciled_from_ledger`: 3
- `counts`: {'stored': 432, 'no_data': 0, 'model_failed': 0, 'excluded_pre_cutoff': 0, 'source_failed': 0}
- `ranked_days`: 432
- `spend_usd`: 5.832

Result: **PASS**

## model_failed

- `forced_dates`: ['2024-11-14', '2024-11-15', '2024-11-18', '2024-11-19']
- `attempts_per_forced_date`: {'2024-11-19': 5, '2024-11-14': 5, '2024-11-15': 5, '2024-11-18': 5}
- `final_state_per_forced_date`: {'2024-11-19': 'model_failed', '2024-11-14': 'model_failed', '2024-11-15': 'model_failed', '2024-11-18': 'model_failed'}
- `counts`: {'stored': 428, 'no_data': 0, 'model_failed': 4, 'excluded_pre_cutoff': 0, 'source_failed': 0}

Result: **PASS**

## source_failed

- `broken_dates`: ['2024-11-29', '2024-12-02', '2024-12-03']
- `calls_sent_for_broken_dates`: []
- `counts`: {'stored': 429, 'no_data': 0, 'model_failed': 0, 'excluded_pre_cutoff': 0, 'source_failed': 3}

Result: **PASS**

## spend_refused

- `cap_usd`: 0.2
- `measured_cost_per_call_usd`: 0.0135
- `calls_sent_before_refusal`: 0
- `spend_at_stop_usd`: 0
- `stopped_early`: spend_refused: batch of 50 at 0.01350 USD per call projects 0.6750 USD on top of 0.0000 already spent, crossing the 0.20 USD cap. Refused before sending.
- `counts`: {'stored': 0, 'no_data': 0, 'model_failed': 0, 'excluded_pre_cutoff': 0, 'source_failed': 0}

Result: **PASS**
