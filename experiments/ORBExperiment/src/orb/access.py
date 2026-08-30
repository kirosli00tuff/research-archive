"""Recorded terms of service, and the access verdict they force.

Standing rule 12: terms of service bind. `robots.txt` and the published terms
are recorded **verbatim** for every vendor before the first repeated fetch. **If
automated collection is disallowed, it is recorded loudly and the access verdict
is routed accordingly. This repository does not proceed against a stated
prohibition.** The HFExperiment Wealthsimple finding is the precedent.

The `robots.txt` matcher here is deliberately **conservative**: where a rule is
ambiguous it refuses. A vendor wrongly refused costs this repository one
vendor; a vendor wrongly permitted costs it the right to use anything it
collected.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum, unique
from typing import final


@unique
class AccessVerdict(StrEnum):
    """Where a vendor sits after its terms are read and its tier is measured."""

    PERMITTED = "PERMITTED"
    """No stated prohibition on the path this repository would fetch."""

    REFUSED_BY_TERMS = "REFUSED_BY_TERMS"
    """Automated collection of the needed path is disallowed. Do not proceed."""

    REQUIRES_CREDENTIAL = "REQUIRES_CREDENTIAL"
    """Permitted by terms, but the tier serves nothing without a key."""

    NO_TERMS_PUBLISHED = "NO_TERMS_PUBLISHED"
    """No robots.txt is served on the API host. Recorded as its own state."""


@final
@dataclass(frozen=True, slots=True)
class RobotsRule:
    """One directive, recorded verbatim as served."""

    user_agent: str
    directive: str
    path: str


@final
@dataclass(frozen=True, slots=True)
class RobotsRecord:
    """A vendor host's robots.txt as served, with the verdict it forces."""

    host: str
    status_code: int
    raw: str
    fetched_at: str

    def rules(self) -> list[RobotsRule]:
        """Parse directives. Blank user-agent groups are ignored."""
        out: list[RobotsRule] = []
        agents: list[str] = []
        pending_agents = True
        for line in self.raw.splitlines():
            stripped = line.split("#", 1)[0].strip()
            if not stripped or ":" not in stripped:
                continue
            key, _, value = stripped.partition(":")
            key = key.strip().lower()
            value = value.strip()
            if key == "user-agent":
                if not pending_agents:
                    agents = []
                    pending_agents = True
                agents.append(value)
            elif key in {"disallow", "allow"}:
                pending_agents = False
                for agent in agents:
                    out.append(RobotsRule(agent, key, value))
        return out

    def disallows_everything_for_wildcard(self) -> bool:
        """True when ``User-agent: *`` carries a bare ``Disallow: /``."""
        return any(
            r.user_agent == "*" and r.directive == "disallow" and r.path == "/"
            for r in self.rules()
        )

    def disallowed_paths_for_wildcard(self) -> list[str]:
        return [
            r.path
            for r in self.rules()
            if r.user_agent == "*" and r.directive == "disallow" and r.path
        ]

    def path_is_disallowed(self, path: str) -> bool:
        """Conservative prefix match against the wildcard group.

        A trailing ``*`` is treated as a prefix wildcard. Where a rule is
        ambiguous this returns True: the cost of a false refusal is one vendor,
        and the cost of a false permission is the whole collection.
        """
        for rule in self.disallowed_paths_for_wildcard():
            pattern = rule.rstrip("$")
            if pattern == "/":
                return True
            prefix = pattern.split("*", 1)[0]
            if prefix and path.startswith(prefix):
                return True
        return False


@final
@dataclass(frozen=True, slots=True)
class VendorAccess:
    """One vendor's finished access record. Every figure carries its n."""

    vendor: str
    api_host: str
    probe_path: str
    verdict: AccessVerdict
    reason: str
    robots_status: int
    serves_1m_regular_session_bars: bool | None
    history_reach_measured: str | None
    serves_delisted: bool | None
    corporate_actions_endpoint: bool | None
    retroactive_adjustment: bool | None
    served_timezone: str | None
    timezone_is_dst_aware: bool | None
    refusal_payload_verbatim: str
    probes_sent: int

    def is_usable(self) -> bool:
        return self.verdict is AccessVerdict.PERMITTED


@unique
class CollectionAccess(StrEnum):
    """Whether a credentialed vendor serves the registered windows.

    Registered by **Amendment 10**. This is the **operational verdict** Section 0
    was always permitted to read — *"every input is a count-derived power, a
    measured share, a measured count, or an operational verdict"* — and it is
    what separates three states that would otherwise look identical from inside
    the map: **no bar exists to measure**, **bars exist but not across the
    registered windows**, and **bars exist and the clock has not run yet**.
    """

    NO_VENDOR_SERVES = "NO_VENDOR_SERVES"
    """No credentialed vendor serves a bar. The 2026-08-29 state: `n = 9`
    vendors, `0` usable. Fires `PENDING_ACCESS` when an integrity input is
    absent."""

    SERVING_REACH_SHORT = "SERVING_REACH_SHORT"
    """A vendor serves, and its **measured** reach does not cover the registered
    windows. Fires `PENDING_SPEND`: the question is a costed operator decision,
    not a design question."""

    SERVING_FULL_REACH = "SERVING_FULL_REACH"
    """A vendor serves and its measured reach covers the registered windows.
    Measured 2026-08-29: **Alpaca, earliest served session 2016-01-04,
    1,762/1,762 in-sample and 875/875 holdout, n = 16 probes.**"""
