#!/usr/bin/env bash
# Read-only cleanliness check over the thirteen audited repositories.
# Usage: tools/git_status_check.sh <label>
# Appends a labelled block to provenance/git-status-checks.log and prints it.
# Never runs anything but `git rev-parse`, `git rev-parse --abbrev-ref`, and `git status --porcelain`.
set -u
LABEL="${1:?label required}"
BASE=/home/kiros-li/Documents/GitHub
REPOS="AiTrader ETFExperiment HFExperiment InsiderExperiment MLCryptoEngine NPDExperiment NPLExperiment ORBExperiment PMExperiment VRPExperiment retail-power-limits solattn solclear"
LOG="$(dirname "$0")/../provenance/git-status-checks.log"
{
  echo "##### CHECK: $LABEL  @ $(date -u +%Y-%m-%dT%H:%M:%SZ)"
  for r in $REPOS; do
    sha=$(git -C "$BASE/$r" rev-parse HEAD 2>/dev/null || echo ERR)
    br=$(git -C "$BASE/$r" rev-parse --abbrev-ref HEAD 2>/dev/null || echo ERR)
    st=$(git -C "$BASE/$r" status --porcelain 2>/dev/null)
    n=$(printf '%s' "$st" | grep -c . || true)
    echo "=== $r  HEAD=$sha  BRANCH=$br  porcelain_entries=$n"
    if [ -n "$st" ]; then printf '%s\n' "$st" | sed 's/^/    /'; fi
  done
  echo "##### END: $LABEL"
  echo
} | tee -a "$LOG"
