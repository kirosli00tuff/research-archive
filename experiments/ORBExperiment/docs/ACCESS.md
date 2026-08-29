# ACCESS.md — vendor access, measured

**STAGE A.1 TASK 1, run 2026-08-29.** Every figure below is **measured live**
unless it is labelled **carried**. Under standing rule 4 a tier limit printed on
a vendor's pricing page is **documented, never measured**, and the measured
limit wins.

**Standing rule 12 was executed first: `robots.txt` was recorded verbatim for
every vendor host before any repeated fetch**, and the access verdict is routed
from what those files say. **n = 15 hosts fetched for `robots.txt`; n = 7 live
API probes sent, to the 5 vendors whose recorded terms permit it.**

---

## The headline finding

> **No vendor serves 1-minute regular-session US equity bars to this repository
> today. n = 9 vendors, 0 usable.**
>
> The nine split cleanly, and the split is the finding:
>
> - **2 vendors serve keyless data and both prohibit automated collection
>   outright** — `stooq.com` and `query1.finance.yahoo.com` each publish
>   `User-agent: * / Disallow: /`.
> - **2 more prohibit the specific API path this repository would fetch** —
>   `eodhd.com` disallows `/api/`, `data.nasdaq.com` disallows `/api/*.json*`
>   and `/api/*.csv*`.
> - **5 permit collection by their published terms and every one of them
>   refused without a credential** — measured, with the refusal payload
>   recorded verbatim below. **n = 7 probes, 0 served a bar.**

**This falsifies a planning assumption carried in the operator prompt**, which
states that `.env.example` is empty on purpose because **"no key is needed for
any Stage A source."** **Measurement says otherwise.** The assumption is
recorded as falsified rather than quietly worked around — the NPLExperiment
correction, where a planning figure near 9.4 events per month was falsified at
**0.5, n = 3 over 182 days** (carried, C-20), and the hypothesis died on a
figure rather than on the world.

**Consequence, stated plainly.** `A.1 TASK 3` (bar revision rate) and
`A.1 TASK 4` (cross-vendor agreement and delisted coverage) are **the two tasks
this repository turns on**, and **neither can be executed without at least two
credentialed vendors** — a primary and a secondary. This is an **open operator
item**, recorded in `progress.md`, `report.md` and `docs/HANDOVER.md`, and it is
registered by **Amendment 1**.

---

## Terms of service, recorded verbatim, before any repeated fetch

Raw files are stored at `data/access/robots/<host>.txt`.

| host | robots.txt | what it says about `User-agent: *` | verdict for this repo |
|---|---|---|---|
| `stooq.com` | **200**, 96 B | `User-agent: Bingbot → Allow: /`; `User-agent: Googlebot → Allow: /`; **`User-agent: * → Disallow: /`** | **REFUSED_BY_TERMS** |
| `stooq.pl` | **200**, 96 B | identical to `stooq.com` | **REFUSED_BY_TERMS** |
| `query1.finance.yahoo.com` | **200**, 26 B | **`User-agent: * → Disallow: /`** — the entire host | **REFUSED_BY_TERMS** |
| `finance.yahoo.com` | **200**, 2,539 B | a named-bot group carrying `Disallow: /` lists **`ClaudeBot`, `anthropic-ai`, `Claude-Web`, `GPTBot`, `CCBot`, `Scrapy`** and 30 others; the `*` group disallows specific paths | **REFUSED_BY_TERMS** |
| `eodhd.com` | **200**, 380 B | **`Disallow: /api/`** — precisely the path a collector needs | **REFUSED_BY_TERMS** |
| `data.nasdaq.com` | **200**, 358 B | **`disallow: /api/*.json*`**, `/api/*.csv*`, `/api/*.xml*`, `/api/*.xls*`, `/api/v3/databases/*/data` | **REFUSED_BY_TERMS** |
| `databento.com` | **200**, 89 B | `Disallow: /portal` only | permitted |
| `hist.databento.com` | **404**, 22 B | no robots.txt served on the API host | no prohibition stated |
| `api.polygon.io` | **404**, 18 B (`404 page not found`) | no robots.txt served on the API host | no prohibition stated |
| `polygon.io` | **301 → `massive.com`**, 147 B | **`User-agent: *` with no directives beneath it** | permitted |
| `api.tiingo.com` | **301 → `www.tiingo.com`**, 188 B | `Disallow: /admin` only | permitted |
| `data.alpaca.markets` | **401**, 172 B | the whole host, `robots.txt` included, sits behind auth | no prohibition stated |
| `alpaca.markets` | **200**, 81,041 B — **an HTML 404 page, not a robots file** | none served | no prohibition stated |
| `www.alphavantage.co` | **404**, 179 B | no robots.txt served | no prohibition stated |

**Two notes recorded rather than smoothed.**

1. **`polygon.io` 301-redirects to `massive.com`.** The operator prompt names
   the vendor as "Polygon, also branded Massive". **Measured, not assumed:** the
   marketing domain now resolves to `massive.com`, whose `robots.txt` carries a
   `User-agent: *` group **with no directives at all**. The API host
   `api.polygon.io` still answers and still returns Polygon-shaped JSON errors.
2. **`alpaca.markets/robots.txt` returns HTTP 200 with 81 KB of HTML** — a
   styled 404 page, not a robots file. **A 200 is not a robots.txt.** Recorded
   as "no robots.txt served", not as "permitted by a served file".

### The prohibition that binds, stated loudly

**`stooq.com` and `query1.finance.yahoo.com` — the only two hosts in the probe
set that serve US equity data without a credential — both publish a blanket
`Disallow: /` for every agent this repository could present.** Standing rule 12
is not advisory: *"Do not proceed against a stated prohibition."* **This
repository sends no further request to either host.** The HFExperiment
Wealthsimple finding is the precedent.

**One earlier request is on the record and is not excused by this section.** The
connectivity probe of `progress.md` Entry 0a sent **one** GET to
`stooq.com/q/d/l/?s=aapl.us&i=d` at ~2026-08-29T01:52Z — **before** any
`robots.txt` had been recorded, which is exactly the ordering standing rule 12
exists to prevent. Its body was discarded to `/dev/null` unread. **It is
recorded, it is not repeated, and it is why the rule is ordered the way it is.**

---

## Live API probes — the 5 vendors whose terms permit collection

Sent by `tools/probe_access.py` through `orb.http.PacedClient`, which **charges
the request ledger before it sends** and **parses no response body**. Raw bytes
are sealed to `data/access/sealed/` with a SHA-256 per file recorded in
`data/access/seals.jsonl`. **n = 7 probes, 5 vendors, 0 dollars spent.**

| vendor | endpoint probed | status | bytes | refusal payload, verbatim |
|---|---|---:|---:|---|
| **Polygon / Massive** | `/v2/aggs/ticker/AAPL/range/1/minute/…` | **401** | 101 | `{"status":"ERROR","request_id":"ad01522f…","error":"API Key was not provided"}` |
| **Polygon / Massive** | `/v3/reference/tickers?limit=1` | **401** | 101 | `{"status":"ERROR","request_id":"98920b53…","error":"API Key was not provided"}` |
| **Alpaca** | `/v2/stocks/AAPL/bars?timeframe=1Min&…` | **401** | 172 | `<html><head><title>401 Authorization Required</title></head>…<center>nginx</center>` |
| **Databento** | `/v0/metadata.list_datasets` | **401** | 30 | `{"detail":"Not authenticated"}` |
| **Tiingo** | `/iex/AAPL/prices?resampleFreq=1min` | **403** | 34 | `{"detail":"Please supply a token"}` |
| **Alpha Vantage** | `TIME_SERIES_INTRADAY`, `interval=1min`, `apikey=demo` | **200** | 220 | `{"Information": "The **demo** API key is for demo purposes only. Please claim your free API key at (https://www.alphavantage.co/support/#api-key) to explore our full API offerings…"}` |
| **Alpha Vantage** | `LISTING_STATUS&state=delisted&apikey=demo` | **200** | **2** | `{}` |

### The Alpha Vantage finding — a refusal served as HTTP 200

**Alpha Vantage refuses with status 200.** The `demo` key returns a
`200 OK` carrying an `Information` string and **no time series**; the delisted
`LISTING_STATUS` query returns a **2-byte body, `{}`**, also at **200**.

**This is precisely the hazard Guard 4 exists to prevent.** A collector that
classifies health from the status code alone records `stored` for both rows and
then counts a session with **zero bars** — merging an operational refusal into
the sample as a composition fact. Under standing rule 7 those are different
families and must never merge.

**It caught this repository's own client, and that is recorded rather than
smoothed.** `orb.http.PacedClient` classifies `HealthState.STORED` on any 200
with a non-empty body, so it labelled the Alpha Vantage refusal `stored`. **The
classifier is insufficient for this vendor** and a per-vendor refusal detector
is required before any Alpha Vantage response is admitted to a census. Recorded
as a finding here and as **ADR-008**; the fix is scoped to A.3 TASK 1 because no
Alpha Vantage data is admitted to anything before then.

---

## The two questions that decide vendor selection, and their answers

The operator prompt names them, and both are **integrity questions, not price
questions**:

1. **Does the tier serve delisted names?**
2. **Does it retroactively rewrite already-served bars on a split or a
   correction?** *"A vendor that rewrites history silently is the H11 hazard in
   a different costume."*

**Neither is answerable today, on any vendor, and the answer is a recorded
absence rather than an estimate.**

| vendor | serves 1-min RTH bars | history reach (bisected) | serves delisted | corp-actions endpoint | retroactive rewrite | served timezone | DST-aware |
|---|---|---|---|---|---|---|---|
| Polygon / Massive | `Absent(not_served)` | `Absent(not_served)` | `Absent(not_served)` | `Absent(not_served)` | `Absent(not_served)` | `Absent(not_served)` | `Absent(not_served)` |
| Alpaca | `Absent(not_served)` | `Absent(not_served)` | `Absent(not_served)` | `Absent(not_served)` | `Absent(not_served)` | `Absent(not_served)` | `Absent(not_served)` |
| Databento | `Absent(not_served)` | `Absent(not_served)` | `Absent(not_served)` | `Absent(not_served)` | `Absent(not_served)` | `Absent(not_served)` | `Absent(not_served)` |
| Tiingo | `Absent(not_served)` | `Absent(not_served)` | `Absent(not_served)` | `Absent(not_served)` | `Absent(not_served)` | `Absent(not_served)` | `Absent(not_served)` |
| Alpha Vantage | `Absent(not_served)` | `Absent(not_served)` | `Absent(not_served)` | `Absent(not_served)` | `Absent(not_served)` | `Absent(not_served)` | `Absent(not_served)` |
| EODHD | **not probed** — `Disallow: /api/` | — | — | — | — | — | — |
| Nasdaq Data Link | **not probed** — `disallow: /api/*.json*` | — | — | — | — | — | — |
| Stooq | **not probed** — `Disallow: /` | — | — | — | — | — | — |
| yfinance | **not probed** — `Disallow: /` | — | — | — | — | — | — |

**Every cell above is `Absent`, never zero and never a guess.** `orb.absence.Absent`
refuses `float()`, `int()`, addition in both directions, ordering, indexing and
truth-testing, so **not one of these cells can be summed into a coverage figure
by accident.** That is standing rule 5 doing its job: *absence is a recorded
state, never a synthesized value.*

**The bisection that would measure history reach was not run**, on any vendor,
because a 401 carries no history to bisect. Recording a reach here from a
pricing page would be recording a **documented** figure as though it were
**measured**, which standing rule 4 forbids by name.

---

## Documented tier limits — carried, never measured

Recorded and labelled per standing rule 4. **None of these was verified, because
verification requires a credential and this repository holds none. The measured
limit wins wherever the two ever disagree, and today there is no measured limit
to compare against.**

| vendor | documented figure | source | measured |
|---|---|---|---|
| Polygon Starter | near **29 USD per month** | vendor pricing page (carried, C-18) | **not measured** |
| Databento | consumption-based, near **125 USD per month** for a medium universe | vendor pricing page (carried, C-18) | **not measured** |
| Alpha Vantage free | rate-limited free tier, key required | measured refusal payload names the free key | **not measured** |
| Alpaca, Tiingo, EODHD, Nasdaq Data Link | free tiers documented | vendor pages | **not measured** |

---

## Access verdicts

| vendor | verdict | reason |
|---|---|---|
| **Polygon / Massive** | `REQUIRES_CREDENTIAL` | terms permit; **401 `"API Key was not provided"`**, n = 2 probes |
| **Alpaca** | `REQUIRES_CREDENTIAL` | no terms served; **401 Authorization Required**, n = 1 probe |
| **Databento** | `REQUIRES_CREDENTIAL` | terms permit (`/portal` only); **401 `"Not authenticated"`**, n = 1 probe |
| **Tiingo** | `REQUIRES_CREDENTIAL` | terms permit (`/admin` only); **403 `"Please supply a token"`**, n = 1 probe |
| **Alpha Vantage** | `REQUIRES_CREDENTIAL` | no terms served; **200 carrying a refusal**, n = 2 probes |
| **EODHD** | **`REFUSED_BY_TERMS`** | `Disallow: /api/` |
| **Nasdaq Data Link** | **`REFUSED_BY_TERMS`** | `disallow: /api/*.json*`, `/api/*.csv*` |
| **Stooq** | **`REFUSED_BY_TERMS`** | `User-agent: * → Disallow: /` |
| **yfinance** | **`REFUSED_BY_TERMS`** | `query1.finance.yahoo.com`: `User-agent: * → Disallow: /` |

**PERMITTED and usable today: 0 of 9.**

---

## What unblocks this, precisely

**Two free-tier credentials, from two different vendors**, so that A.1 TASK 4's
cross-vendor comparison has two vendors to compare. **This is an operator
action** — it requires creating accounts, which this repository will not do on
the operator's behalf.

**Recommended pair, chosen on the two integrity questions and not on price:**

- **Primary: Polygon / Massive.** It is the only probed vendor that publishes a
  documented delisted-ticker reference endpoint (`/v3/reference/tickers` with
  `active=false`) *and* minute aggregates on one host, which makes the delisted
  question of A.1 TASK 4 answerable at all. Its terms carry no prohibition.
- **Secondary: Alpaca or Tiingo.** A genuinely independent feed is what the
  Concretum finding demands — identical code against four vendors produced
  final equity from **226,000 to 726,000 USD** (carried, C-13). Two vendors that
  resell the same consolidated tape would measure agreement with themselves.
  **Whichever is chosen, its upstream source is recorded in the selection ADR,
  and if the two share an upstream the agreement measurement is labelled as
  measuring a redistribution pipeline rather than two independent feeds.**

Keys go in `.env`, which is git-ignored. **`.env.example` stays empty of values
and gains only key *names*.** No key is ever committed.

**Until then**, everything in Stage A that does not depend on vendor bars is
built and delivered in full: the session calendar, the cost model, the universe,
signal and verdict machinery built dark against synthetic fixtures, the power
gate, the latch machinery, the guards and the mutation harness. **Only the two
integrity measurements wait**, and they wait on an operator item rather than on
a design question.

---

# A.1 TASK 2 — rate ceilings, measured per endpoint

**Run 2026-08-29.** `tools/probe_ceilings.py`, through the same paced,
ledger-charging client. **n = 18 requests across 3 endpoint-spacing cells.**

| vendor | endpoint | requested spacing | n | achieved rate | status distribution | 429s |
|---|---|---:|---:|---:|---|---:|
| Polygon / Massive | `/v3/reference/tickers` | 2.0 s | 5 | **33.2 / min** | `{401: 5}` | **0** |
| Polygon / Massive | `/v3/reference/tickers` | 0.5 s | 8 | **88.4 / min** | `{401: 8}` | **0** |
| Alpha Vantage | `TIME_SERIES_INTRADAY` demo | 2.0 s | 5 | **29.1 / min** | `{200: 5}` | **0** |

**No endpoint returned HTTP 429. n = 18, 0 refusals on a limit.**

## What this measurement is not evidence about, stated with its precedent

**It is not evidence about the endpoints this repository will actually collect
from.** solattn ADR-021 established that **ceilings are per endpoint, never per
host**: one GeckoTerminal endpoint refused **47.5 percent of n = 1,863
attempts** while a second, on the same host and the same IP, took **0 of 360**
(carried, C-21). **The corollary applies here to this repository's own
measurement.** With no credential, **the only reachable path on every permitted
vendor is the unauthenticated refusal path**, and a ceiling measured on a 401 is
**not** a ceiling on the authenticated data endpoint.

**Polygon's documented free tier is 5 requests per minute** — documented, never
measured. **The measured 88.4 per minute does not contradict it**, and recording
it as though it did would be exactly the error standing rule 4 warns about, run
backwards: treating a measurement of the wrong thing as though it beat the
documentation of the right thing.

## Registered operating pace, provisional and labelled unmeasured

Registered by **Amendment 2**. Half-the-measured-ceiling cannot be computed
because **no ceiling on a data endpoint has been measured**, so the pace falls
back to the conservative default rather than to a figure derived from the wrong
endpoint.

| parameter | value | basis |
|---|---|---|
| `DEFAULT_MIN_SPACING_S` | **6.0 s** | conservative default; **unmeasured** |
| per-vendor daily cap | set in `orb.ledger.RequestLedger`, charged **before** sending | **unmeasured** |
| unregistered vendor | **refused outright** — no cap, no send | structural |

**Every one of these is re-measured per endpoint at the first task that holds a
credential, and moved by a dated amendment if the measurement disagrees.**

## The refusal shapes, recorded verbatim

| vendor | limit-refusal shape | measured? |
|---|---|---|
| Polygon / Massive | **not observed** — no 429 reached on the reachable path | no |
| Alpha Vantage | **not observed as a 429.** Its *credential* refusal is served as **HTTP 200** carrying `{"Information": "The **demo** API key is for demo purposes only…"}`, so a limit refusal may well also arrive at 200. **A status-code-only limiter detector is unsafe on this vendor** (ADR-008). | no |
| Alpaca, Databento, Tiingo | **not observed** — refused at 401/403 before any limiter was reached | no |

**The request ledger charged every one of these probes before it sent them.**
Total charged this session: **polygon 15, alphavantage 7, alpaca 1, databento 1,
tiingo 1 — n = 25 requests, 0 dollars.**
