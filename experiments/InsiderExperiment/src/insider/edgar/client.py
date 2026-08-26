"""The single door to sec.gov and data.sec.gov.

Mandatory User-Agent naming the requester with a contact email, because
requests without one return 403. Exponential backoff on the registered retry
statuses. A local cache keyed on the URL, so a re-run never re-fetches and the
SEC is asked for each byte exactly once.

Nothing else in this repository opens a socket.
"""

from __future__ import annotations

import hashlib
import os
import time
from pathlib import Path

import httpx

from insider.config import CONFIG, Config
from insider.edgar.throttle import THROTTLE
from insider.ledger.fetch import record_fetch
from insider.paths import EDGAR_CACHE


class EdgarUnavailable(RuntimeError):
    """The SEC could not be reached or refused every attempt. CORPUS-BLOCKED."""


class UserAgentMissing(RuntimeError):
    """No contact User-Agent configured. The SEC returns 403 without one."""


def user_agent(cfg: Config = CONFIG) -> str:
    """The contact header. Read from the environment, never committed."""
    value = os.environ.get(cfg.sec_user_agent_env, "").strip()
    if not value or "@" not in value:
        raise UserAgentMissing(
            f"set {cfg.sec_user_agent_env} to a string naming the requester with a "
            f"contact email. The SEC returns 403 without one."
        )
    return value


def _cache_path(url: str) -> Path:
    digest = hashlib.sha256(url.encode("utf-8")).hexdigest()
    suffix = ".zip" if url.endswith(".zip") else ".json" if url.endswith(".json") else ".txt"
    return EDGAR_CACHE / digest[:2] / f"{digest}{suffix}"


def fetch(url: str, *, cfg: Config = CONFIG) -> bytes:
    """Fetch one URL through the throttle, the cache, and the backoff ladder."""
    cached = _cache_path(url)
    if cached.exists():
        payload = cached.read_bytes()
        record_fetch(url, status=200, served_from="cache", waited_seconds=0.0, bytes_read=len(payload))
        return payload

    cached.parent.mkdir(parents=True, exist_ok=True)
    headers = {"User-Agent": user_agent(cfg), "Accept-Encoding": "gzip, deflate"}
    last_status: int | None = None
    last_error: str | None = None

    for attempt in range(cfg.sec_max_retries + 1):
        waited = THROTTLE.wait()
        try:
            response = httpx.get(
                url, headers=headers, timeout=cfg.sec_request_timeout_seconds, follow_redirects=True
            )
        except httpx.HTTPError as exc:
            last_error = f"{type(exc).__name__}: {exc}"
            record_fetch(url, status=None, served_from="wire", waited_seconds=waited, bytes_read=0)
        else:
            last_status = response.status_code
            record_fetch(
                url,
                status=response.status_code,
                served_from="wire",
                waited_seconds=waited,
                bytes_read=len(response.content),
            )
            if response.status_code == 200:
                cached.write_bytes(response.content)
                return response.content
            if response.status_code == 404:
                raise EdgarUnavailable(f"404 for {url}")
            if response.status_code not in cfg.sec_retry_status_codes:
                raise EdgarUnavailable(f"{response.status_code} for {url}")

        if attempt < cfg.sec_max_retries:
            delay = min(cfg.sec_backoff_base_seconds * (2**attempt), cfg.sec_backoff_max_seconds)
            time.sleep(delay)

    raise EdgarUnavailable(
        f"gave up on {url} after {cfg.sec_max_retries + 1} attempts "
        f"(last status {last_status}, last error {last_error})"
    )


def reachable(cfg: Config = CONFIG) -> bool:
    """Whether the SEC answers at all. Feeds the CORPUS gate, never a verdict."""
    try:
        fetch("https://www.sec.gov/files/company_tickers.json", cfg=cfg)
    except (EdgarUnavailable, UserAgentMissing):
        return False
    return True
