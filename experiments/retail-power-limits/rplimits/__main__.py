"""``python -m rplimits`` prints the generated blocks; ``--write`` rewrites them."""

from __future__ import annotations

import sys

from rplimits.docsync import DOCUMENTS, write_blocks
from rplimits.render import BLOCKS


def main(argv: list[str]) -> int:
    if "--write" in argv:
        for document in DOCUMENTS:
            names = write_blocks(document)
            print(f"{document.name}: rewrote {', '.join(names)}")
        return 0
    for name, build in BLOCKS.items():
        print(f"--- {name} ---\n{build()}\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
