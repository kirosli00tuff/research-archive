"""The structured Form 4 XML inside one filing.

This is the primary-source route. It is exercised on a sample to check the
structured data sets field by field, which is what lets the corpus claim its
transaction codes, roles, prices and 10b5-1 flags came from the filing rather
than from a convenience layer nobody verified.

ADR-002 records why the sample is a sample.
"""

from __future__ import annotations

import datetime as dt
import json
from dataclasses import dataclass
from xml.etree import ElementTree

from insider.absence import FLAG_NOT_REPORTED, Absent
from insider.config import CONFIG, Config
from insider.edgar.client import EdgarUnavailable, fetch

ARCHIVE = "https://www.sec.gov/Archives/edgar/data/{cik}/{accession}"


@dataclass(frozen=True, slots=True)
class XmlTransaction:
    """One non-derivative transaction as the filing itself reports it."""

    transaction_date: dt.date | None
    transaction_code: str
    shares: float | None
    price_per_share: float | None
    acquired_disposed: str


@dataclass(frozen=True, slots=True)
class XmlForm4:
    accession: str
    issuer_cik: int
    issuer_symbol: str
    is_director: bool
    is_officer: bool
    is_ten_percent_owner: bool
    aff10b5one: bool | Absent
    transactions: tuple[XmlTransaction, ...]


def _text(node: ElementTree.Element | None, path: str) -> str:
    if node is None:
        return ""
    found = node.find(path)
    return (found.text or "").strip() if found is not None and found.text else ""


def _value(node: ElementTree.Element | None, path: str) -> str:
    """Form 4 wraps most leaves in a <value> child. Read through it."""
    if node is None:
        return ""
    found = node.find(path)
    if found is None:
        return ""
    inner = found.find("value")
    target = inner if inner is not None else found
    return (target.text or "").strip() if target.text else ""


def _float_or_none(raw: str) -> float | None:
    try:
        return float(raw)
    except (TypeError, ValueError):
        return None


def document_url(cik: int, accession: str, cfg: Config = CONFIG) -> str:
    """Locate the ownership XML inside a filing directory.

    The directory listing carries an XSL-rendered copy beside the raw document.
    The raw one is taken, because the rendered one is a presentation artifact.
    """
    plain = accession.replace("-", "")
    listing = json.loads(fetch(f"{ARCHIVE.format(cik=cik, accession=plain)}/index.json", cfg=cfg))
    names = [
        item["name"]
        for item in listing.get("directory", {}).get("item", [])
        if str(item.get("name", "")).lower().endswith(".xml")
        and not str(item.get("name", "")).lower().startswith("xsl")
    ]
    if not names:
        raise EdgarUnavailable(f"no ownership XML in {accession}")
    return f"{ARCHIVE.format(cik=cik, accession=plain)}/{names[0]}"


def parse(payload: bytes, accession: str) -> XmlForm4:
    """Parse one ownership document. Raises on anything that is not one."""
    root = ElementTree.fromstring(payload)
    if root.tag != "ownershipDocument":
        raise ValueError(f"{accession} is not an ownership document, root is {root.tag!r}")

    issuer = root.find("issuer")
    owner = root.find("reportingOwner")
    relationship = owner.find("reportingOwnerRelationship") if owner is not None else None

    raw_flag = _text(root, "aff10b5One")
    flag: bool | Absent = FLAG_NOT_REPORTED if raw_flag == "" else raw_flag in {"1", "true"}

    transactions: list[XmlTransaction] = []
    for node in root.findall("nonDerivativeTable/nonDerivativeTransaction"):
        amounts = node.find("transactionAmounts")
        raw_date = _value(node, "transactionDate")
        parsed_date: dt.date | None
        try:
            parsed_date = dt.date.fromisoformat(raw_date) if raw_date else None
        except ValueError:
            parsed_date = None
        transactions.append(
            XmlTransaction(
                transaction_date=parsed_date,
                transaction_code=_value(node, "transactionCoding/transactionCode"),
                shares=_float_or_none(_value(amounts, "transactionShares")),
                price_per_share=_float_or_none(_value(amounts, "transactionPricePerShare")),
                acquired_disposed=_value(amounts, "transactionAcquiredDisposedCode"),
            )
        )

    return XmlForm4(
        accession=accession,
        issuer_cik=int(_text(issuer, "issuerCik") or 0),
        issuer_symbol=_text(issuer, "issuerTradingSymbol").upper(),
        is_director=_text(relationship, "isDirector") in {"1", "true"},
        is_officer=_text(relationship, "isOfficer") in {"1", "true"},
        is_ten_percent_owner=_text(relationship, "isTenPercentOwner") in {"1", "true"},
        aff10b5one=flag,
        transactions=tuple(transactions),
    )


def fetch_and_parse(cik: int, accession: str, cfg: Config = CONFIG) -> XmlForm4:
    return parse(fetch(document_url(cik, accession, cfg=cfg), cfg=cfg), accession)
