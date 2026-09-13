#!/usr/bin/env bash
# Recreates the legacy /tmp scratchpad symlinks (cleared on every reboot) for each session id listed in
# provenance/launch-args/SESSIONS.txt. Idempotent. Run at login by the systemd user unit
# program-audit-tmp-links.service, and again by tools/resume.py.
set -u
PROJ=/tmp/claude-1000/-home-kiros-li-Documents-GitHub-program-audit
TARGET=/home/kiros-li/.cache/program-audit/scratchpad
HERE=$(dirname "$(readlink -f "$0")")
mkdir -p -m 700 /tmp/claude-1000
mkdir -p -m 700 "$PROJ"
while read -r sid; do
  [ -z "$sid" ] && continue
  case "$sid" in \#*) continue;; esac
  d="$PROJ/$sid"; mkdir -p "$d"
  if [ -d "$d/scratchpad" ] && [ ! -L "$d/scratchpad" ]; then
    rmdir "$d/scratchpad" 2>/dev/null || { echo "WARN: $d/scratchpad is a non-empty real directory; left alone"; continue; }
  fi
  [ -L "$d/scratchpad" ] || ln -s "$TARGET" "$d/scratchpad"
  echo "ok $d/scratchpad -> $(readlink "$d/scratchpad")"
done < "$HERE/../provenance/launch-args/SESSIONS.txt"
