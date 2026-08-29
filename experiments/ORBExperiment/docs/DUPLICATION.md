# DUPLICATION.md — the pre-design duplication screen

**Run 2026-08-29, STAGE A.-1 TASK 0, before a single line of design was
written.** The screen exists to stop this repository from re-asking a question
another repository in this house has already opened. A substantive hit halts
Stage A and reports. An incidental prose or data hit is recorded and cleared
with a one-line reason.

**Verdict: CLEAR.** No repository under `/home/kiros-li/Documents/GitHub`
contains an opening-range, relative-volume or intraday-US-equity-price-structure
design. All 14,002 raw hits across 11 repositories are incidental and are
cleared below with reasons, n = 11 repositories screened.

---

## The command, exactly as run

    cd /home/kiros-li/Documents/GitHub
    for repo in AiTrader ETFExperiment HFExperiment InsiderExperiment \
                MLCryptoEngine MLCryptoTrader NPDExperiment NPLExperiment \
                solattn solclear [personal repo, name removed]; do
      grep -rniE 'opening range|\bORB\b|opening candle|relative volume|09:30|9:30|intraday breakout|stocks in play' \
        "$repo" \
        --exclude-dir=.git --exclude-dir=.venv --exclude-dir=__pycache__ \
        --exclude-dir=node_modules --exclude-dir=.mypy_cache \
        --exclude-dir=.pytest_cache --exclude-dir=.ruff_cache \
        --exclude-dir='*.egg-info'
    done

Eight patterns, case-insensitive, `\bORB\b` word-bounded so that `absorb`,
`orbit` and `Orbital` do not match on the token alone. `.git`, `.venv` and every
cache directory excluded, as specified.

---

## Hit count per repository

| repository | raw hits | substantive hits | classification |
|---|---:|---:|---|
| AiTrader | 47 | **0** | incidental — session-boundary prose |
| ETFExperiment | 0 | **0** | clean |
| HFExperiment | 8 | **0** | incidental — lockfile timestamps, one test fixture string |
| InsiderExperiment | 0 | **0** | clean |
| MLCryptoEngine | 943 | **0** | incidental — lockfile upload timestamps |
| MLCryptoTrader | 0 | **0** | clean |
| NPDExperiment | 0 | **0** | clean |
| NPLExperiment | 9 | **0** | incidental — US session-tag definitions |
| solattn | 12,954 | **0** | incidental — lockfile timestamps, one Solana token symbol |
| solclear | 19 | **0** | incidental — lockfile timestamps, one vendor JSON timestamp |
| [personal repo, name removed] | 0 | **0** | clean |
| **total** | **14,002** | **0** | **CLEAR** |

## Hit count per pattern, across all repositories

| pattern | total hits | verdict |
|---|---:|---|
| `opening range` | **0** | clean everywhere |
| `opening candle` | **0** | clean everywhere |
| `relative volume` | **0** | clean everywhere |
| `intraday breakout` | **0** | clean everywhere |
| `stocks in play` | **0** | clean everywhere |
| `\bORB\b` | 33 | all in `solattn`, all incidental |
| `09:30` | 3,796 | all incidental |
| `9:30` | 13,947 | all incidental, superset of the `09:30` row |

**The five patterns that carry the design — `opening range`, `opening candle`,
`relative volume`, `intraday breakout`, `stocks in play` — return zero hits in
every repository, n = 11.** That is the finding. The remaining three patterns
are substring-promiscuous by construction and were included as a deliberately
over-wide net; every one of their hits is cleared below.

---

## Every hit class, cleared with its reason

1. **`9:30` inside `uv.lock` upload timestamps** — the dominant class, e.g.
   `upload-time = "2026-07-14T16:49:30.285Z"` contains the substring `9:30` at
   the seconds boundary. Accounts for essentially all of the `solattn` 12,921
   and `MLCryptoEngine` 943. **Cleared:** a package-index upload clock is not a
   trading design.
2. **`9:30` inside stored vendor JSON timestamps** — e.g.
   `solclear/data/vendor/stage_g_decon_population.json`,
   `"first_activity": "2021-11-10 04:19:30.000"`. **Cleared:** on-chain
   first-activity clocks, not an equity session.
3. **`09:30` as a US session boundary in prose** — `AiTrader/core/util.cpp:60`
   `// 09:30-16:00 trading session`, `AiTrader/news_experiment/horizon.py:41`,
   and `NPLExperiment/DECISIONS.md:450-451` tagging `regular` as
   `09:30` to the close in `America/New_York`. **Cleared:** these define *when a
   session is*, for a news-LLM horizon and for an on-chain funding session tag
   respectively. Neither reads intraday equity price structure, neither computes
   a range, and neither ranks anything by volume.
4. **`ORB` as a Solana token symbol** — all 33 hits sit in
   `solattn/data/manifests/births-2026-08-*.jsonl`, in rows such as
   `{"name":"ORDBET AI", ... ,"symbol":"ORB","venue_class":"launchpad"}` and
   `{"name":"Orbital Wallet", ... ,"symbol":"ORB"}`. **Cleared:** a launchpad
   ticker string that collides with the acronym. Not a design.
5. **`09:30` in a test fixture string** —
   `HFExperiment/tests/test_alpaca_source.py:62`,
   `{"date": "2026-09-01", "open": "09:30", ...}`. **Cleared:** this is a
   *market-hours* payload field in a broker-calendar test, i.e. the string
   `"09:30"` as the session open **time**, not an opening price. It is the
   nearest thing in the house to an equity-intraday touch and it is a calendar
   fixture.

---

## The expectation, verified rather than assumed

The prompt states the expected result as CLEAR on the ground that MLCryptoEngine,
MLCryptoTrader, NPLExperiment, NPDExperiment, HFExperiment, InsiderExperiment,
ETFExperiment, solattn, solclear and AiTrader are crypto, on-chain, filings or
news-LLM work and none covers intraday US equity price structure. **Verified, and
one refinement recorded.** Two repositories do touch US equities, and neither
touches intraday price structure:

- **HFExperiment** reaches a US equity *broker* (IBKR, Alpaca calendar) and is
  the source of the integer-share constraint carried into this registration
  (error 10243, `reports/stage_a1b/a1b_report.md` line 52). It models
  execution mechanics, not an intraday signal.
- **AiTrader** carries a US session boundary for a *news* horizon. Its
  `news_experiment/horizon.py` maps a headline to a session, and reads no
  intraday bar.

`[personal repo, name removed]` was screened as well although the prompt does not name it, and
returned 0 hits on all eight patterns.

**No repository is testing, or has closed, a claim about the first five minutes
of the US regular session.** Stage A proceeds.
