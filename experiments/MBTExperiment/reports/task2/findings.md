# Task 2 — the known-answer test, which is the condition that blocked the stage

**It did not run, and the reason is sharper than last time.**

Stage B could not run it because no Gateway session existed. A session now
exists, the venue answers in 0.24 to 0.26 seconds over n = 7 previews, and the
known-answer test still did not run. **The binding reason moved from the
environment into this harness.**

## The outcome, over-determined at n = 2 independent blockers

| blocker | state | clearing it alone would |
|---|---|---|
| **the venue returns no OrderState** for any what-if this package builds | measured, n = 4 of 4 products | leave the test with nothing to compare against |
| **no operator-supplied expected margin** | `Absent(not_yet_measured)`, n = 0 supplied | leave the test with nothing to compare to |

**Both must clear.** `reports/task4/known_answer.json` records `agrees: false`
with both blockers named, so the verdict reads the over-determination rather
than the first reason encountered.

## Blocker one: the venue rejects every what-if this package can construct

**IBKR error 321, at n = 4 of 4 products tried: "What-If order should have
transmit flag set to TRUE."** Raised on SPY, on the ES front future, on the MBT
front future and on an MBT option. The request is then never resolved, so the
package's preview call does not fail, it **hangs**. The Task 1 probe bounds the
wait at 20 seconds and records a typed absence, because waiting forever is not a
measurement.

`build_short_option_order` sets `transmit=False`, and `what_if_order` **refuses**
an order carrying `transmit=True`. So the package cannot construct a what-if the
venue will process, on any product, in any environment.

> **Stage B's stated reasoning was that "a preview never needs it".** The venue's
> own validation says a preview is *required* to carry it. This is the standing
> rule working exactly as intended: measured behaviour beats documentation, and
> the documentation here was this repository's own.

A second defect sits behind it and would bind next. **With `transmit=True` but no
explicit TIF, IBKR warns 10349, "Order TIF was set to DAY based on order preset",
and ends the request with no OrderState at all.** Isolated at n = 4 combinations:
TIF unset gives nothing whether or not the account is set, and `tif="DAY"` gives
an OrderState whether or not the account is set. **TIF is load-bearing and the
account field is not.**

## Blocker two: no independently checkable expected margin was supplied

**`Absent(not_yet_measured)` at n = 0 operator values supplied.** The expected
figure is an operator input read by a person, because CME refused automated
access to its schedule under its own Data Terms of Use and this repository obeys
that refusal. It is not scraped, not inferred from a third party, and not carried
from another repository. `MBT_KNOWN_ANSWER_MARGIN_USD` is the slot and it is
empty.

**An absence here is not a pass.** The check records it and the MBT output stays
untrusted.

## What was deliberately not done

**The package was not changed to set `transmit=True`.**

Flipping it would clear blocker one, and with an operator margin supplied the
stage would reach HARNESS-READY. That is precisely why it was not done here. The
change would weaken the single flag whose purpose is preventing order
transmission, in reaction to what the venue turned out to demand, and the
resulting HARNESS-READY would rest on a safety property rewritten after the fact.

The change is one line and the evidence for it is complete and recorded. **It is
an operator decision, not an autonomous one.** See ADR-010.
