# robots.txt and published terms, recorded verbatim before any repeated fetch

Standing rule 5. Every domain this repository fetched more than once appears
below with its `robots.txt` recorded, its status, and its SHA-256. **Where a
venue published a refusal, the refusal is recorded verbatim and obeyed.**

| domain | HTTP | bytes | SHA-256 | relevant directives |
|---|---|---|---|---|
| `www.deribit.com` | **404** | 25,049 (HTML error page) | `0e8faa387add9dbe723a29670b6f4774e625f9f3f14dcd161978596efb81b284` | **No robots.txt is served.** The path returns Deribit's HTML "Page Not Found". No crawl directives are published at this path. |
| `support.deribit.com` | 200 | 2,445 | `35782374b6422d264528c0d810a5f912779cbb89718ef33fad05d47c509eb53f` | Disallows `/hc/*/search`, `/hc/requests/`, `/hc/*/signin`, `/hc/activity`, account and ticket paths. **Does not disallow `/hc/en-us/articles/`.** |
| `www.interactivebrokers.ca` | 200 | 265 | `b69c27ba2b18a7ed1e8c84df2148aa274f694feef37ad523931d39fc1c2c7b1f` | `User-agent: *` · Disallow `/smf/`, `/fluxbb/`, `/insights/ibtr_alerts.php`, `/search/`, `/referral/`. **No page fetched by this repository is disallowed.** |
| `app.hyperliquid.xyz` | 200 | 335 | `95f06b47879296b2b7b3abb66c0de8cc226831cac83b20a5aeeac8d1c8f87bcb` | Disallows `/explorer/*`, `/vaults/`, **`/join/`**, `/leaderboard/`; `Allow: /` otherwise. `/join/` is the onboarding path and **was not fetched** — this repository does not register at any venue. |
| `www.cmegroup.com` | **000 / 403** | 0 | — | **robots.txt could not be retrieved.** Two attempts: HTTP/2 returned `INTERNAL_ERROR (err 2)`; HTTP/1.1 timed out at 25 s; a third attempt with a browser user-agent returned **403**. See the refusal below. |
| `www.purposeinvest.com` | 200 | 489 | `80ba816b586df71b89cae3e68214b7a1c88786a3ae237024486c9af69c174f66` | Explicitly `Allow: /` for `ClaudeBot` and `anthropic-ai` among others; `User-agent: *` disallows `/documents/*`, `/opt-out`, `/download/*`. |
| `www.3iq.ca` → `www.3iq.io` | 200 | 176 | `1961863b767218a15883e51f17ff039f740a53090c506e25d81b7982c931d3a7` | Disallows `/style-guide`, `/thank-you` only. |
| `www.ciro.ca` | 200 | 2,103 | `3a4e0a7eacd2b79e8f7304655208b1d112fd341fa468b2ad627ce2f32de09b63` | Standard Drupal directives; disallows `/core/`, `/profiles/`, `README.md`. |

## CME Group — the refusal, recorded verbatim and obeyed

Retrieved 2026-08-30T05:27Z from
`https://www.cmegroup.com/CmeWS/mvc/Margins/Outrights?exchange=CME&pageNumber=1`.
**HTTP 403**, 602 bytes, SHA-256
`eecde3fafbde4090c30e610a7ed4b8d877f8351c0490e4189574890e8a5a4f7e`.

```json
{"message": "This IP address is blocked due to suspected web scraping activity associated with it on this CMEgroup.com page. Use of scripts, software, spiders, robots, avatars, agents, tools or other scraping mechanisms is strictly prohibited by CME Group's website Data Terms of Use. If you are attempting to access data or content from the website via automated means or for commercial purposes, CME has numerous other methods to deliver the content you require. Please contact CME Group's Global Command Center (GCC) at gcc@cmegroup.com and your inquiry will be directed to the appropriate team."}
```

**Action taken: all fetching of cmegroup.com stopped immediately on receipt of
this message, and no further request was made to that domain.** Terms of service
bind. The consequence is recorded in `reports/task3/venue_table.md` as
`Absent(not_served)` for every CME-sourced figure, and **no CME margin value is
synthesized, estimated, or carried from any third party.**

**What was NOT done, stated explicitly:** no user-agent rotation beyond the two
already attempted before the message was seen, no proxy, no VPN, no delay-and-retry
loop, no third-party mirror of CME margin data substituted for the primary source.
A figure obtained by working around this refusal would not be a measurement of
CME's schedule; it would be a measurement of someone's copy of it.
