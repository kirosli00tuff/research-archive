# Stage C.1: the refusals, produced

Generated 2026-08-25T02:40:23Z. Mode paper, pinned account [paper account ID removed], route SMART.

Formation: the real 2026-08-03 width-20 book, computed fresh through the registered rule into C.1's own store, because the B.1 store records formations only from the 2026-09-01 series start. Quotes: mock, entry close plus and minus half the A.2 measured 12.77 bp median spread. Demo notional 45.00 USD, the A.2 GO candidate, labelled DEMO because the registered per-name notional stays DEFERRED. Refusals 1, 2, 5 and 6 run under demonstration-resolved parameters (broker minimum 1.00 DEMO, per-name 45.00 DEMO) so each check is reachable. Nothing here resolves Amendment 1.

Book: SNDK, AXTI, WOLF, MU, WDC, BE, MXL, TE, LITE, INTC, AAOI, STX, TSEM, DOCN, HUT, PL, CIEN, NBIS, RVMD, WULF

Held book empty, diff produces 20 buy intents. Formation hash 0b28a5cfda7516fa, reproduced hash 0b28a5cfda7516fa, match: True.

## Refusal 7: deferred_parameter_unresolved, the steady state

Condition: the registered inputs as they stand today. Amendment 1 has not landed, per_name_notional_usd has no value, and the gate refuses the entire book.

Refusal produced: `deferred_parameter_unresolved`

Arithmetic: per_name_notional_usd awaits Amendment 1: the billing regime of a mixed integer-plus-fraction order decides it and only a paper fill measures that

All 20 of 20 intents refused. The first ledger record written:

```json
{
 "arithmetic": "per_name_notional_usd awaits Amendment 1: the billing regime of a mixed integer-plus-fraction order decides it and only a paper fill measures that",
 "kind": "refusal",
 "reason": "deferred_parameter_unresolved",
 "run_utc": "2026-08-25T02:40:23Z",
 "subject": "SNDK"
}
```

## Refusal 1: insufficient_settled_cash

Condition constructed: settled cash 30.00 USD against a 45.00 USD buy of SNDK, parameters DEMO-resolved.

Refusal produced: `insufficient_settled_cash`

Arithmetic: notional 45.00 > settled cash 30.00

Ledger record written:

```json
{
 "arithmetic": "notional 45.00 > settled cash 30.00",
 "kind": "refusal",
 "reason": "insufficient_settled_cash",
 "run_utc": "2026-08-25T02:40:23Z",
 "subject": "SNDK"
}
```

## Refusal 2: below_broker_minimum

Condition constructed: a 0.50 USD intent against the DEMO broker minimum of 1.00 USD.

Refusal produced: `below_broker_minimum`

Arithmetic: notional 0.50 < broker minimum 1.00

Ledger record written:

```json
{
 "arithmetic": "notional 0.50 < broker minimum 1.00",
 "kind": "refusal",
 "reason": "below_broker_minimum",
 "run_utc": "2026-08-25T02:40:23Z",
 "subject": "AXTI"
}
```

## Refusal 3: non_fractionable_symbol

Condition constructed: the eligibility snapshot marks WOLF not fractionable. Absence fails closed.

Refusal produced: `non_fractionable_symbol`

Arithmetic: WOLF is not fractionable and whole-share sizing is closed at this stake

Ledger record written:

```json
{
 "arithmetic": "WOLF is not fractionable and whole-share sizing is closed at this stake",
 "kind": "refusal",
 "reason": "non_fractionable_symbol",
 "run_utc": "2026-08-25T02:40:23Z",
 "subject": "WOLF"
}
```

## Refusal 4: formation_reproduction_failed

Condition constructed: the intent carries formation hash 0000deadbeef0000 while the store reproduces 0b28a5cfda7516fa.

Refusal produced: `formation_reproduction_failed`

Arithmetic: the formation feeding this order did not reproduce from the price store

Ledger record written:

```json
{
 "arithmetic": "the formation feeding this order did not reproduce from the price store",
 "kind": "refusal",
 "reason": "formation_reproduction_failed",
 "run_utc": "2026-08-25T02:40:23Z",
 "subject": "MU"
}
```

## Refusal 6: not_smart_routed

Condition constructed: route DIRECTED:ARCA. Directed API orders forfeit Tiered pricing in IBKR's own words.

Refusal produced: `not_smart_routed`

Arithmetic: directed API orders forfeit Tiered pricing in IBKR's own words, docs/ACCESS.md

Ledger record written:

```json
{
 "arithmetic": "directed API orders forfeit Tiered pricing in IBKR's own words, docs/ACCESS.md",
 "kind": "refusal",
 "reason": "not_smart_routed",
 "run_utc": "2026-08-25T02:40:23Z",
 "subject": "WDC"
}
```

## Refusal 5: spend_cap_reached

Condition constructed: a demonstration spend ledger seeded with 60.00 USD on 2026-05-11 and 40.01 USD on 2026-08-20, plus 25.00 USD on 2025-08-10 which sits outside the rolling 365 days and must not count. The rolling-year query reads only the ledger.

rolling_year_spend(2026-08-25) = 100.01 USD, the 2025-08-10 record excluded.

Refusal produced: `spend_cap_reached`

Arithmetic: spend 100.01 >= registered cap 100.00 per rolling 365 days

Ledger record written:

```json
{
 "arithmetic": "spend 100.01 >= registered cap 100.00 per rolling 365 days",
 "kind": "refusal",
 "reason": "spend_cap_reached",
 "run_utc": "2026-08-25T02:40:23Z",
 "subject": "BE"
}
```

## Refusal 8: the account pin, four ways

The gate checks the pin before everything, including the deferred parameters, so a mis-addressed intent never reaches pricing. The four cases below build Intent objects directly, simulating a defect that skips construct_intent, and the gate refuses anyway. The construction wall is shown after.

### Absent field

Refusal produced: `account_not_pinned`

Arithmetic: intent.account is absent. The TWS API would route an accountless order to the default account on the full-access login. Refused before any socket.

Ledger record written:

```json
{
 "arithmetic": "intent.account is absent. The TWS API would route an accountless order to the default account on the full-access login. Refused before any socket.",
 "kind": "refusal",
 "reason": "account_not_pinned",
 "run_utc": "2026-08-25T02:40:23Z",
 "subject": "LITE"
}
```

### Empty field

Refusal produced: `account_not_pinned`

Arithmetic: intent.account is empty. The TWS API treats an empty account field as the default account, the operator's main account. Refused.

Ledger record written:

```json
{
 "arithmetic": "intent.account is empty. The TWS API treats an empty account field as the default account, the operator's main account. Refused.",
 "kind": "refusal",
 "reason": "account_not_pinned",
 "run_utc": "2026-08-25T02:40:23Z",
 "subject": "LITE"
}
```

### Wrong account

Refusal produced: `account_not_pinned`

Arithmetic: intent.account DU9999999 != pinned IBKR_ACCOUNT_ID [paper account ID removed]

Ledger record written:

```json
{
 "arithmetic": "intent.account DU9999999 != pinned IBKR_ACCOUNT_ID [paper account ID removed]",
 "kind": "refusal",
 "reason": "account_not_pinned",
 "run_utc": "2026-08-25T02:40:23Z",
 "subject": "LITE"
}
```

### Right account under wrong mode

Refusal produced: `account_mode_mismatch`

Arithmetic: account [paper account ID removed] lacks the live prefix U: right account under the wrong declared mode refuses

Ledger record written:

```json
{
 "arithmetic": "account [paper account ID removed] lacks the live prefix U: right account under the wrong declared mode refuses",
 "kind": "refusal",
 "reason": "account_mode_mismatch",
 "run_utc": "2026-08-25T02:40:23Z",
 "subject": "LITE"
}
```

## The construction wall, before the gate

### Absent account

Refusal produced: `intent_field_absent`

Arithmetic: account is absent or empty. An intent must be addressed to the pinned account before it can travel.

Ledger record written:

```json
{
 "arithmetic": "account is absent or empty. An intent must be addressed to the pinned account before it can travel.",
 "kind": "refusal",
 "reason": "intent_field_absent",
 "run_utc": "2026-08-25T02:40:23Z",
 "subject": "LITE"
}
```

### Empty account

Refusal produced: `intent_field_absent`

Arithmetic: account is absent or empty. An intent must be addressed to the pinned account before it can travel.

Ledger record written:

```json
{
 "arithmetic": "account is absent or empty. An intent must be addressed to the pinned account before it can travel.",
 "kind": "refusal",
 "reason": "intent_field_absent",
 "run_utc": "2026-08-25T02:40:23Z",
 "subject": "LITE"
}
```

### No captured quote, the arrival-mid mirror

Refusal produced: `no_arrival_mid`

Arithmetic: no quote was captured. The arrival mid anchors the execution measurement, and a fill without one is the registered termination fill_without_arrival_mid. Refused before the gate.

Ledger record written:

```json
{
 "arithmetic": "no quote was captured. The arrival mid anchors the execution measurement, and a fill without one is the registered termination fill_without_arrival_mid. Refused before the gate.",
 "kind": "refusal",
 "reason": "no_arrival_mid",
 "run_utc": "2026-08-25T02:40:23Z",
 "subject": "LITE"
}
```

## Priced-and-ready, stopped exactly at Amendment 1

Under DEMO-resolved parameters the same intent passes every check and reaches priced-and-ready. It is recorded as a would-be submission and submitted nowhere:

symbol SNDK, side buy, notional 45.00, quantity 0.037, mid 1214.8300 captured 2026-08-25T02:40:23Z, account [paper account ID removed], route SMART, settled cash after 955.00

Under the registered inputs the identical intent stops at the deferred parameter, which is exactly where D.1 begins:

Refusal produced: `deferred_parameter_unresolved`

Arithmetic: per_name_notional_usd awaits Amendment 1: the billing regime of a mixed integer-plus-fraction order decides it and only a paper fill measures that

Ledger record written:

```json
{
 "arithmetic": "per_name_notional_usd awaits Amendment 1: the billing regime of a mixed integer-plus-fraction order decides it and only a paper fill measures that",
 "kind": "refusal",
 "reason": "deferred_parameter_unresolved",
 "run_utc": "2026-08-25T02:40:23Z",
 "subject": "SNDK"
}
```

## The reconciliation stub, D.1's registered task shape

```json
{
 "ledger_total_cents": 10001,
 "period_end": "2026-08-25",
 "period_start": "2026-01-01",
 "statement_total_cents": null,
 "status": "awaiting_broker_statement"
}
```

## The connectivity probe, read-only twice over

Declared mode paper, .env port 4002, host 127.0.0.1, pinned [paper account ID removed].

```json
{
 "detail": "account [paper account ID removed] verified in managed list of 1, disconnected",
 "managed_accounts": [
  "[paper account ID removed]"
 ],
 "server_time_epoch": 1787625630,
 "server_version": 187,
 "state": "ok"
}
```

## The demonstration ledger, counted

{'intent': 20, 'refusal': 34, 'would_submit': 1} in demo_ledger.jsonl, plus 3 spend records in demo_spend_ledger.jsonl. Append-only, fsynced, one record per event.
