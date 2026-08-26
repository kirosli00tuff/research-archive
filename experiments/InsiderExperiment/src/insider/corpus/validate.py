"""Check the corpus against the two access routes it did not use for bulk.

The structured data sets carry the corpus. That choice is only defensible if it
is checked, so this module does two things. It counts Form 4 rows in the
full-index archives and sets them beside the data sets' own filing counts, and
it fetches the raw ownership XML for a sample of qualifying events and compares
every field the rule depends on.

It also writes out the refusals the corpus build produced, which is the only
form of refusal this repository accepts.
"""

from __future__ import annotations

import json
import sys
from collections import Counter
from dataclasses import dataclass

from insider.absence import Absent
from insider.config import CONFIG, Config
from insider.corpus import store
from insider.edgar import bulk, fullindex, submissions, xml_form4
from insider.edgar.client import EdgarUnavailable
from insider.ledger.evidence import record
from insider.paths import REPORTS, ensure_dirs

SAMPLE_SIZE = 25


@dataclass(frozen=True, slots=True)
class FieldCheck:
    accession: str
    symbol: str
    agrees: bool
    detail: str


def index_versus_datasets(cfg: Config = CONFIG) -> list[dict[str, object]]:
    """Form 4 rows in the full index beside Form 4 documents in the data sets.

    form.idx carries one row per filer per filing, so an ownership filing with
    an issuer and two reporting owners contributes several rows. The ratio is a
    coverage signal, not an equality check, and it is labelled that way.
    """
    out: list[dict[str, object]] = []
    for quarter in bulk.quarters(cfg):
        counted = fullindex.count_form4(quarter, cfg)
        archive = bulk.fetch_quarter(quarter, cfg)
        documents = sum(
            1
            for row in bulk.iter_table(archive, bulk.SUBMISSION)
            if (row.get("DOCUMENT_TYPE") or "").strip() == "4"
        )
        out.append(
            {
                "quarter": quarter,
                "form4_index_rows": counted.form4_index_rows,
                "dataset_form4_documents": documents,
                "rows_per_document": (
                    round(counted.form4_index_rows / documents, 3) if documents else None
                ),
            }
        )
    return out


def _compare(row: tuple[str, ...], parsed: xml_form4.XmlForm4, cfg: Config) -> FieldCheck:
    accession, symbol, transaction_date, value_usd = row[0], row[1], row[2], float(row[3])
    problems: list[str] = []

    if parsed.issuer_symbol and parsed.issuer_symbol != symbol:
        problems.append(f"symbol {parsed.issuer_symbol} != {symbol}")
    if not (parsed.is_officer or parsed.is_director):
        problems.append("filing reports neither officer nor director")
    if parsed.is_ten_percent_owner:
        problems.append("filing reports a ten percent owner")

    purchases = [
        t
        for t in parsed.transactions
        if t.transaction_code in cfg.allowed_transaction_codes
        and t.transaction_date is not None
        and t.transaction_date.isoformat() == transaction_date
    ]
    if not purchases:
        problems.append(f"no {cfg.allowed_transaction_codes[0]} transaction on {transaction_date}")
    else:
        values = [
            (t.shares or 0.0) * (t.price_per_share or 0.0)
            for t in purchases
            if t.shares and t.price_per_share
        ]
        if not any(abs(v - value_usd) <= max(1.0, 0.005 * value_usd) for v in values):
            problems.append(f"no purchase value matches {value_usd:.2f} (xml has {values})")

    if cfg.exclude_10b5_1 and parsed.aff10b5one is True:
        problems.append("filing carries the 10b5-1 flag")

    return FieldCheck(
        accession=accession,
        symbol=symbol,
        agrees=not problems,
        detail="; ".join(problems) if problems else "every checked field agrees",
    )


def sample_xml(cfg: Config = CONFIG) -> tuple[list[FieldCheck], Counter[str]]:
    """Fetch the raw ownership XML for a spread of qualifying events and compare.

    The sample is taken by ordering on entry session and stepping through it,
    so it spans the whole corpus rather than one quarter of it, and it is chosen
    without reference to any outcome.
    """
    with store.connect() as con:
        rows = con.execute(
            "SELECT accession, symbol, transaction_date, value_usd, issuer_cik "
            "FROM event ORDER BY entry_session, accession"
        ).fetchall()
    if not rows:
        return [], Counter()
    step = max(1, len(rows) // SAMPLE_SIZE)
    picked = rows[::step][:SAMPLE_SIZE]

    checks: list[FieldCheck] = []
    tally: Counter[str] = Counter()
    for accession, symbol, transaction_date, value_usd, issuer_cik in picked:
        try:
            parsed = xml_form4.fetch_and_parse(int(issuer_cik), accession, cfg)
        except (EdgarUnavailable, ValueError) as exc:
            checks.append(FieldCheck(accession, symbol, False, f"fetch or parse failed: {exc}"))
            tally["unreachable"] += 1
            continue
        check = _compare((accession, symbol, transaction_date, str(value_usd)), parsed, cfg)
        checks.append(check)
        tally["agrees" if check.agrees else "disagrees"] += 1
        if isinstance(parsed.aff10b5one, Absent):
            tally["flag_not_reported_in_xml"] += 1
    return checks, tally


def sample_ticker_map(cfg: Config = CONFIG) -> list[dict[str, object]]:
    """Ask the submissions API whether each sampled issuer CIK carries its symbol."""
    with store.connect() as con:
        rows = con.execute(
            "SELECT DISTINCT issuer_cik, symbol FROM event ORDER BY issuer_cik"
        ).fetchall()
    step = max(1, len(rows) // SAMPLE_SIZE)
    out: list[dict[str, object]] = []
    for issuer_cik, symbol in rows[::step][:SAMPLE_SIZE]:
        try:
            tickers = submissions.tickers_for(int(issuer_cik), cfg)
        except EdgarUnavailable as exc:
            out.append({"cik": issuer_cik, "symbol": symbol, "tickers": None, "error": str(exc)})
            continue
        out.append(
            {
                "cik": issuer_cik,
                "symbol": symbol,
                "tickers": list(tickers),
                "symbol_present": symbol in tickers,
            }
        )
    return out


def write_refusals_report() -> str:
    with store.connect() as con:
        johnsen = store.refusals(con, "johnsen_rejected_cluster")
        unclassifiable = store.refusals(con, "insider_unclassifiable_for_want_of_history")

    lines = [
        "# Refusals produced by the Stage A.1 corpus build",
        "",
        "A refusal asserted in prose is a claim. Each block below was serialized by",
        "the run that produced it, from `var/insider_corpus.db` table `refusal`.",
        "",
        "## The Johnsen programmatic-event filter rejecting a cluster",
        "",
        "A cluster is rejected when a single date-and-price pair accounts for eighty",
        "percent or more of the contributing buys. Insiders who all bought at one price",
        "on one day were filled by one mechanism, not by three independent judgements.",
        "",
    ]
    for block in johnsen[:2]:
        lines += ["```json", block, "```", ""]
    lines += [
        "## An insider who cannot be classified for want of three years of history",
        "",
        "The Cohen-Malloy-Pomorski rule needs three years of look-back. An insider whose",
        "first observed trade falls less than three years before the candidate is neither",
        "routine nor opportunistic. She is `insufficient_history`, which is a third state",
        "and is recorded as one.",
        "",
    ]
    for block in unclassifiable[:2]:
        lines += ["```json", block, "```", ""]
    return "\n".join(lines)


def main() -> int:
    ensure_dirs()
    cfg = CONFIG
    out = REPORTS / "stage_a1"
    out.mkdir(parents=True, exist_ok=True)

    print("counting the full-index archives against the structured data sets")
    coverage = index_versus_datasets(cfg)
    ratios = [c["rows_per_document"] for c in coverage if c["rows_per_document"] is not None]
    print(f"  {len(coverage)} quarters, rows per document {min(ratios):.2f} to {max(ratios):.2f}")

    print(f"fetching {SAMPLE_SIZE} ownership documents and comparing every rule field")
    checks, tally = sample_xml(cfg)
    for check in checks:
        if not check.agrees:
            print(f"  {check.accession} {check.symbol}: {check.detail}")
    print(f"  {tally['agrees']} agree, {tally['disagrees']} disagree, {tally['unreachable']} unreachable")
    print(f"  10b5-1 box absent in the XML for {tally['flag_not_reported_in_xml']} of the sample")

    print(f"asking the submissions API about {SAMPLE_SIZE} issuer CIKs")
    tickers = sample_ticker_map(cfg)
    present = sum(1 for t in tickers if t.get("symbol_present"))
    print(f"  symbol present in the SEC's current ticker list for {present} of {len(tickers)}")

    payload = {
        "index_versus_datasets": coverage,
        "xml_field_checks": [
            {"accession": c.accession, "symbol": c.symbol, "agrees": c.agrees, "detail": c.detail}
            for c in checks
        ],
        "xml_tally": dict(tally),
        "submissions_ticker_check": tickers,
    }
    (out / "validation.json").write_text(json.dumps(payload, indent=2), encoding="utf-8")
    (out / "refusals.md").write_text(write_refusals_report(), encoding="utf-8")
    record("corpus_validation", agrees=tally["agrees"], disagrees=tally["disagrees"], unreachable=tally["unreachable"])
    print("wrote reports/stage_a1/validation.json and reports/stage_a1/refusals.md")
    return 0 if tally["disagrees"] == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
