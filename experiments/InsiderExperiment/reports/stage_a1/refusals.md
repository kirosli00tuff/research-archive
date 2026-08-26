# Refusals produced by the Stage A.1 corpus build

A refusal asserted in prose is a claim. Each block below was serialized by
the run that produced it, from `var/insider_corpus.db` table `refusal`.

## The Johnsen programmatic-event filter rejecting a cluster

A cluster is rejected when a single date-and-price pair accounts for eighty
percent or more of the contributing buys. Insiders who all bought at one price
on one day were filled by one mechanism, not by three independent judgements.

```json
{
  "symbol": "DRI",
  "window": [
    "2020-04-23",
    "2020-04-27"
  ],
  "size": 12,
  "distinct_filers": 12,
  "modal_date_price_fraction": 1.0,
  "threshold": 0.8,
  "buys": [
    {
      "filer_cik": 1186383,
      "transaction_date": "2020-04-23",
      "price_per_share": 58.5,
      "shares": 12820.0,
      "value_usd": 749970.0
    },
    {
      "filer_cik": 1189669,
      "transaction_date": "2020-04-23",
      "price_per_share": 58.5,
      "shares": 3418.0,
      "value_usd": 199953.0
    },
    {
      "filer_cik": 1200753,
      "transaction_date": "2020-04-23",
      "price_per_share": 58.5,
      "shares": 17094.0,
      "value_usd": 999999.0
    },
    {
      "filer_cik": 1224818,
      "transaction_date": "2020-04-23",
      "price_per_share": 58.5,
      "shares": 4273.0,
      "value_usd": 249970.5
    },
    {
      "filer_cik": 1242843,
      "transaction_date": "2020-04-23",
      "price_per_share": 58.5,
      "shares": 25641.0,
      "value_usd": 1499998.5
    },
    {
      "filer_cik": 1242844,
      "transaction_date": "2020-04-23",
      "price_per_share": 58.5,
      "shares": 4273.0,
      "value_usd": 249970.5
    },
    {
      "filer_cik": 1260096,
      "transaction_date": "2020-04-23",
      "price_per_share": 58.5,
      "shares": 1282.0,
      "value_usd": 74997.0
    },
    {
      "filer_cik": 1518780,
      "transaction_date": "2020-04-23",
      "price_per_share": 58.5,
      "shares": 427.0,
      "value_usd": 24979.5
    },
    {
      "filer_cik": 1579551,
      "transaction_date": "2020-04-23",
      "price_per_share": 58.5,
      "shares": 2564.0,
      "value_usd": 149994.0
    },
    {
      "filer_cik": 1653795,
      "transaction_date": "2020-04-23",
      "price_per_share": 58.5,
      "shares": 2991.0,
      "value_usd": 174973.5
    },
    {
      "filer_cik": 1700587,
      "transaction_date": "2020-04-23",
      "price_per_share": 58.5,
      "shares": 1025.0,
      "value_usd": 59962.5
    },
    {
      "filer_cik": 1718143,
      "transaction_date": "2020-04-23",
      "price_per_share": 58.5,
      "shares": 2000.0,
      "value_usd": 117000.0
    }
  ]
}
```

```json
{
  "symbol": "DRI",
  "window": [
    "2020-04-23",
    "2020-04-27"
  ],
  "size": 11,
  "distinct_filers": 11,
  "modal_date_price_fraction": 1.0,
  "threshold": 0.8,
  "buys": [
    {
      "filer_cik": 1189669,
      "transaction_date": "2020-04-23",
      "price_per_share": 58.5,
      "shares": 3418.0,
      "value_usd": 199953.0
    },
    {
      "filer_cik": 1200753,
      "transaction_date": "2020-04-23",
      "price_per_share": 58.5,
      "shares": 17094.0,
      "value_usd": 999999.0
    },
    {
      "filer_cik": 1224818,
      "transaction_date": "2020-04-23",
      "price_per_share": 58.5,
      "shares": 4273.0,
      "value_usd": 249970.5
    },
    {
      "filer_cik": 1242843,
      "transaction_date": "2020-04-23",
      "price_per_share": 58.5,
      "shares": 25641.0,
      "value_usd": 1499998.5
    },
    {
      "filer_cik": 1242844,
      "transaction_date": "2020-04-23",
      "price_per_share": 58.5,
      "shares": 4273.0,
      "value_usd": 249970.5
    },
    {
      "filer_cik": 1260096,
      "transaction_date": "2020-04-23",
      "price_per_share": 58.5,
      "shares": 1282.0,
      "value_usd": 74997.0
    },
    {
      "filer_cik": 1518780,
      "transaction_date": "2020-04-23",
      "price_per_share": 58.5,
      "shares": 427.0,
      "value_usd": 24979.5
    },
    {
      "filer_cik": 1579551,
      "transaction_date": "2020-04-23",
      "price_per_share": 58.5,
      "shares": 2564.0,
      "value_usd": 149994.0
    },
    {
      "filer_cik": 1653795,
      "transaction_date": "2020-04-23",
      "price_per_share": 58.5,
      "shares": 2991.0,
      "value_usd": 174973.5
    },
    {
      "filer_cik": 1700587,
      "transaction_date": "2020-04-23",
      "price_per_share": 58.5,
      "shares": 1025.0,
      "value_usd": 59962.5
    },
    {
      "filer_cik": 1718143,
      "transaction_date": "2020-04-23",
      "price_per_share": 58.5,
      "shares": 2000.0,
      "value_usd": 117000.0
    }
  ]
}
```

## An insider who cannot be classified for want of three years of history

The Cohen-Malloy-Pomorski rule needs three years of look-back. An insider whose
first observed trade falls less than three years before the candidate is neither
routine nor opportunistic. She is `insufficient_history`, which is a third state
and is recorded as one.

```json
{
  "filer_cik": 1178565,
  "symbol": "QEP",
  "transaction_date": "2016-06-30",
  "first_observed_trade": "2016-06-30",
  "years_of_history_required": 3,
  "years_of_history_observed": 0.0,
  "look_back_window_opens": "2013-01-01",
  "months_traded_observed": 2
}
```

```json
{
  "filer_cik": 1673282,
  "symbol": "RH",
  "transaction_date": "2016-06-28",
  "first_observed_trade": "2016-06-28",
  "years_of_history_required": 3,
  "years_of_history_observed": 0.0,
  "look_back_window_opens": "2013-01-01",
  "months_traded_observed": 10
}
```
