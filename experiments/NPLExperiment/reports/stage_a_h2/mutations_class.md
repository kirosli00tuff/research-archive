# Amendment H2-5 mutation evidence

Each mutation edits real source on the taxonomy and tiered-rule surface;
the suite must go red; the source is restored byte-for-byte; the suite
must go green. Bytecode is purged before every run. **No H2 look has been
read** — all three H2 latches are absent and the pair reader has only ever
seen synthetic fixtures — so no mutation could touch a live verdict.

**Result: 8 of 8 CAUGHT.**

Baseline: suite green before any mutation.

## MC1: admit a cross-complex elder at any tier

- file: `src/npl/register/tiered.py`
- expected catch: tests/test_tiered.py — the tier-2 filter stops naming the class, so a commodity elder wins an equity leg on funding proximity, which is exactly the H2-3 defect this amendment exists to refuse
- suite red under mutation: **True**
- source restored byte-for-byte: **True**
- suite green after restore: **True**
- verdict: **CAUGHT**

## MC2: let tier 3 accept an fx, rates, commodity, or vol leg

- file: `src/npl/register/tiered.py`
- expected catch: tests/test_tiered.py — a rates leg would be rescued into the equity complex, and `para:10Y` would pair with an equity instead of being excluded
- suite red under mutation: **True**
- source restored byte-for-byte: **True**
- suite green after restore: **True**
- verdict: **CAUGHT**

## MC3: read a post-entry funding row inside tiered selection

- file: `src/npl/controls.py`
- expected catch: tests/test_tiered.py — PostEntryRead is produced through the tiered path; silently dropping the offending row would let a rate from the event's own future reach the matcher without a refusal
- suite red under mutation: **True**
- source restored byte-for-byte: **True**
- suite green after restore: **True**
- verdict: **CAUGHT**

## MC4: write into the superseded h2_pairs.jsonl

- file: `src/npl/register/tiered.py`
- expected catch: tests/test_tiered.py — the superseded Amendment H2-3 assignment would become writable, and the record this stage promises to retain byte-identical could be appended to
- suite red under mutation: **True**
- source restored byte-for-byte: **True**
- suite green after restore: **True**
- verdict: **CAUGHT**

## MC5: silently classify an unmapped ticker as equity

- file: `src/npl/register/assetclass.py`
- expected catch: tests/test_assetclass.py — the six tickers whose refusal is the whole measured cost of the class test (QNT, BOT, SHAZ, LYTE, NCLD, ANSEM) would silently become equity, and `excluded_unclassifiable` would never be recorded
- suite red under mutation: **True**
- source restored byte-for-byte: **True**
- suite green after restore: **True**
- verdict: **CAUGHT**

## MC6: let a lower tier win over a higher one

- file: `src/npl/register/tiered.py`
- expected catch: tests/test_tiered.py - tier order is the rule; reversing it makes the loosest tier win, so an exact-class same-dex elder loses to an equity-complex one
- suite red under mutation: **True**
- source restored byte-for-byte: **True**
- suite green after restore: **True**
- verdict: **CAUGHT**

## MC7: impute a missing tier on a ledger row instead of refusing

- file: `src/npl/register/tiered.py`
- expected catch: tests/test_tiered.py — an absent tier would read as tier 1 rather than as the defect it is, which is the H2-3 `pair_type` imputation mistake repeated
- suite red under mutation: **True**
- source restored byte-for-byte: **True**
- suite green after restore: **True**
- verdict: **CAUGHT**

## MC8: drop the crypto dex rule

- file: `src/npl/register/assetclass.py`
- expected catch: tests/test_assetclass.py — every main-dex instrument would fall through to the builder-dex table, where BTC and ETH are registered as `crypto_reference_on_builder_dex` and most crypto tickers appear at all
- suite red under mutation: **True**
- source restored byte-for-byte: **True**
- suite green after restore: **True**
- verdict: **CAUGHT**

