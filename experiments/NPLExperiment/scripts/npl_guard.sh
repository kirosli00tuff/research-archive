#!/usr/bin/env bash
# The manual-run guard, the solattn ADR-018 shape. A declaration is not a
# mechanism: this script refuses to run a collector while the systemd units
# are active, because two clients against one measured ceiling is a doubled
# request rate the pacing was never measured for. Override, deliberately
# named and explicit: NPL_ALLOW_ALONGSIDE_SYSTEMD=1.
set -euo pipefail

COMMAND="${1:-}"
if [[ -z "${COMMAND}" ]]; then
    echo "usage: scripts/npl_guard.sh {verify|watch|daily}" >&2
    exit 2
fi

if [[ "${NPL_ALLOW_ALONGSIDE_SYSTEMD:-0}" != "1" ]] && command -v systemctl >/dev/null 2>&1; then
    for unit in npl-watch.service npl-daily.service npl-watch.timer npl-daily.timer; do
        if systemctl --user is-active --quiet "${unit}" 2>/dev/null; then
            echo "refusing: ${unit} is active. Two clients against one measured" >&2
            echo "per-endpoint ceiling doubles the request rate the registered" >&2
            echo "pacing (npl/pacing.py) was measured for. Nothing was started" >&2
            echo "and nothing was written." >&2
            echo "stop the units first:  systemctl --user stop npl-watch.timer npl-daily.timer" >&2
            echo "or override explicitly: NPL_ALLOW_ALONGSIDE_SYSTEMD=1 $0 ${COMMAND}" >&2
            exit 3
        fi
    done
fi

cd "$(dirname "$0")/.."
exec uv run python -m npl.cli "${COMMAND}"
