"""The ex-ante classification rule, frozen in REGISTRATION.md Section 3.

Nothing here reads a return, a price move after the filing, or any realized
outcome. Every filter decides on the transaction's own reported fields.
"""

from __future__ import annotations

import re

from insider.absence import Absent
from insider.callstate import CallState
from insider.config import CONFIG, Config
from insider.corpus.records import PASSED, Transaction, Verdict

_ROLE_SPLIT = re.compile(r"[^a-z]+")


def normalize_roles(raw: str) -> frozenset[str]:
    """DERA writes relationships as a delimited string. Normalize to tokens.

    Unrecognized text yields an empty set, which the role filter rejects. An
    unreadable relationship is an absence of evidence that the filer is an
    officer or a director, not evidence that she is one.
    """
    tokens = {t for t in _ROLE_SPLIT.split((raw or "").lower()) if t}
    out: set[str] = set()
    if "director" in tokens:
        out.add("director")
    if "officer" in tokens:
        out.add("officer")
    if "tenpercentowner" in tokens or {"ten", "percent", "owner"} <= tokens:
        out.add("tenpercentowner")
    if "other" in tokens:
        out.add("other")
    return frozenset(out)


def code_verdict(txn: Transaction, cfg: Config = CONFIG) -> Verdict | None:
    """Purchases only. Transaction code P and nothing else.

    A grants, M option exercises and F tax withholding are not discretionary
    open-market purchases. S sales carry diversification and liquidity motives
    and no study finds signal in them.
    """
    if txn.code not in cfg.allowed_transaction_codes:
        return Verdict(CallState.FILTERED_CODE, f"code_{txn.code or 'blank'}")
    return None


def role_verdict(txn: Transaction, cfg: Config = CONFIG) -> Verdict | None:
    """Officers and directors only. Ten percent beneficial owners are excluded.

    The exclusion is on the flag, not on the filer's other roles. A filer who is
    both an officer and a ten percent owner is excluded, because the hazard the
    exclusion targets is the large strategic-investor closing and that hazard
    does not go away when the investor also holds a title. Section 3 records the
    count this strict reading costs.
    """
    if any(role in txn.roles for role in cfg.excluded_roles):
        also_titled = any(role in txn.roles for role in cfg.allowed_roles)
        return Verdict(
            CallState.FILTERED_ROLE,
            "tenpercentowner_also_titled" if also_titled else "tenpercentowner",
        )
    if not any(role in txn.roles for role in cfg.allowed_roles):
        return Verdict(CallState.FILTERED_ROLE, f"roles_{'_'.join(sorted(txn.roles)) or 'none'}")
    return None


def programmatic_verdict(txn: Transaction, cfg: Config = CONFIG) -> Verdict | None:
    """The per-transaction half of the programmatic-event filter.

    A 10b5-1 trade is a pre-committed plan execution, so it carries no
    information about what the insider believes today. An unreported flag is a
    recorded absence and admits the transaction, because before the 2023 cover
    page the box did not exist and treating its absence as a False would read a
    decade of filings as affirmatively not 10b5-1.
    """
    if cfg.exclude_10b5_1 and txn.aff10b5one is True:
        return Verdict(CallState.FILTERED_PROGRAMMATIC, "flagged_10b5_1")
    if txn.value_usd < cfg.min_transaction_usd:
        return Verdict(CallState.FILTERED_PROGRAMMATIC, "below_dollar_floor")
    return None


def flag_is_absent(txn: Transaction) -> bool:
    """Whether the 10b5-1 box was not reported at all. Counted, never imputed."""
    return isinstance(txn.aff10b5one, Absent)


def prefilter(txn: Transaction, cfg: Config = CONFIG) -> Verdict:
    """The filters that decide on one transaction alone, in registered order."""
    for check in (code_verdict, role_verdict, programmatic_verdict):
        verdict = check(txn, cfg)
        if verdict is not None:
            return verdict
    return PASSED
