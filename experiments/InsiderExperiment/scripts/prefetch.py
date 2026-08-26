"""Warm the SEC cache. Every byte the corpus needs, fetched once, through the throttle.

Separated from the corpus build so a slow network cannot be mistaken for a slow
pipeline, and so a re-run of the build costs nothing.
"""

from __future__ import annotations

import sys
import time

from insider.config import CONFIG
from insider.edgar import bulk, fullindex
from insider.edgar.client import EdgarUnavailable
from insider.paths import ensure_dirs


def main() -> int:
    ensure_dirs()
    quarters = bulk.quarters(CONFIG)
    started = time.monotonic()
    failures: list[str] = []

    print(f"warming {len(quarters)} structured data sets, {quarters[0]} to {quarters[-1]}")
    for i, quarter in enumerate(quarters, start=1):
        try:
            bulk.fetch_quarter(quarter, CONFIG)
        except EdgarUnavailable as exc:
            failures.append(f"{quarter}: {exc}")
            print(f"  {quarter} FAILED {exc}")
            continue
        if i % 10 == 0 or i == len(quarters):
            print(f"  {i}/{len(quarters)} at {time.monotonic() - started:.0f}s", flush=True)

    print(f"warming {len(quarters)} full indexes")
    for i, quarter in enumerate(quarters, start=1):
        try:
            fullindex.count_form4(quarter, CONFIG)
        except EdgarUnavailable as exc:
            failures.append(f"form.idx {quarter}: {exc}")
            print(f"  form.idx {quarter} FAILED {exc}")
            continue
        if i % 10 == 0 or i == len(quarters):
            print(f"  {i}/{len(quarters)} at {time.monotonic() - started:.0f}s", flush=True)

    print(f"done in {time.monotonic() - started:.0f}s, {len(failures)} failures")
    for line in failures:
        print(f"  {line}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
