#!/usr/bin/env bash
# Bounded wait for the network stack before a collector pass (ADR-032).
#
# The failure this closes: four watcher sweeps between 2026-08-31 and
# 2026-09-02 polled zero dexs and recorded source_failed on both meta:main
# and perpDexs with a null http_status, meaning the request never reached
# the wire. Every one sat at a boot or resume boundary and the following
# sweep recovered. The units already carry After/Wants=network-online.target,
# which is close to a no-op for --user units because that target belongs to
# the system manager, and which is not re-evaluated after a suspend anyway.
#
# Two properties this script must keep.
#
# It charges nothing. DNS resolution only, never a venue request, so the
# registered request ledger and its daily cap stay authoritative.
#
# It never suppresses a real outage. On timeout it exits 0 so the pass runs
# and records source_failed loudly, per the standing rule that a refusal is
# loud and absence is a recorded state.

set -u

HOST="${NPL_NET_HOST:-api.hyperliquid.xyz}"
DEADLINE_SECS="${NPL_NET_WAIT_SECS:-60}"
SLEEP_SECS=3

start=${SECONDS}
until getent hosts "${HOST}" >/dev/null 2>&1; do
    if (( SECONDS - start >= DEADLINE_SECS )); then
        echo "wait_for_net: ${HOST} unresolved after ${DEADLINE_SECS}s; proceeding so the pass records source_failed" >&2
        exit 0
    fi
    sleep "${SLEEP_SECS}"
done

waited=$(( SECONDS - start ))
if (( waited > 0 )); then
    echo "wait_for_net: ${HOST} resolved after ${waited}s" >&2
fi
exit 0
