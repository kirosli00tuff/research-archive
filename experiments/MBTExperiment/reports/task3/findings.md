# Task 3 — the paper margin read

**The registered straddle was refused, so no registered MBT margin was read. A
margin profile was measured across listed strikes instead, and it is an
indication only.**

## The registered straddle resolution was attempted and refused

`reports/task3/straddle.json`, recorded from a live paper session against the
live chain.

| registered rule | applied | outcome |
|---|---|---|
| 3.1 the ATM reference is the MBT front future's touch midpoint | yes | **`Absent(unquoted_leg)`** |
| 3.1 if the future's quote is refused, the whole straddle is refused | yes | **straddle refused** |
| 3.2 nearest strike, ties to the LOWER | not reached | no reference price to measure against |
| 3.3 nearest expiry to 30 days by settlement instant, ties LONGER | enumerated | 11 series listed across 4 underlying futures |

**The front future served no real-time touch, so there is no at-the-money
reference, so there is no strike, so there is no straddle.** The rule says one is
never substituted, and none was. This is the registration working, not failing.

**The chain itself is healthy at n = 11 listed series.** The expiry nearest the
registered 30-day tenor is `W1E:20261002`, settling `2026-10-02T15:00:00Z`, on
underlying MBTV6, with 150 listed strikes. The settlement instant was read from
the contract (`lastTradeTime 10:00:00` in `US/Central`) rather than assumed, so
rule 3.3 measured to the settlement instant and not to midnight.

## The margin profile, INDICATION ONLY

Measured outside the package, because the package's own preview path cannot
obtain a margin at all. **No reference price was used**, so no registered rule
was exercised or bypassed: margins are reported across listed strikes, and the
profile needs no at-the-money determination.

| figure | value | n |
|---|---|---|
| initial margin, short MBT option, minimum | **3,441.42 USD/contract** | n = 18 previews |
| initial margin, maximum | **4,599.07 USD/contract** | n = 18 previews |
| initial margin, median | **3,930.96 USD/contract** | n = 18 previews |
| registered ceiling | 1,000.00 USD/contract | quoted, not re-derived |
| ratio to ceiling | **3.44x to 4.60x** | n = 18 previews, 9 strikes, both rights |
| previews below the ceiling | **0** | of 18 |

**Not one of the 18 previews sat below the registered ceiling.**

> **A paper margin model is not the live one, and the MARGIN gate remains
> `Absent(no_live_session)`.** IBKR's paper environment approximates margin and
> does not reproduce the live SPAN calculation, so these figures measure the
> simulator rather than the account that would hold the position. **Nothing above
> is a gate result and nothing above is verdict-bearing.**

`tests/test_paper_margin.py` pins the refusal against these measured figures
rather than a synthetic one, at n = 5 values and 12 test cases. **The danger this
guards is specific: every measured paper margin sits far above the ceiling, so a
promoted paper figure would produce a confident FAIL that might point the same
way the live answer does. A verdict that is right by accident is not a result.**

## Does the what-if commission estimate include exchange and regulatory fees?

**No, and more precisely: the response cannot distinguish them. Stage B's
expectation is CONFIRMED against a live session rather than contradicted.**

**`OrderState` carries 17 fields and zero exchange or regulatory fee fields, at
n = 3 previews against a live paper session.** The field list is `commission`,
`commissionCurrency`, `completedStatus`, `completedTime`, `equityWithLoanAfter`,
`equityWithLoanBefore`, `equityWithLoanChange`, `initMarginAfter`,
`initMarginBefore`, `initMarginChange`, `maintMarginAfter`, `maintMarginBefore`,
`maintMarginChange`, `maxCommission`, `minCommission`, `status`, `warningText`.

**One observation, recorded with its inference explicitly refused.** The what-if
commission scalar was **2.01 USD per contract at n = 18 previews**, against the
registered IBKR Canada figure of **0.85 USD per contract** measured on the live
schedule on 2026-08-30. The difference is 1.16 USD.

**That difference is not attributed to fees.** A paper commission report is
synthetic, so the excess is equally consistent with the simulator's own model,
and the response carries no breakdown that could separate the two. **The absence
of a field is not the absence of the fee from the scalar, and the presence of an
excess is not evidence of one either.** The leg stays `Absent(not_served)`.
