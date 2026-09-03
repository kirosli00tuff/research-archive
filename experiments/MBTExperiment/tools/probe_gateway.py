#!/usr/bin/env python3
"""Measure IB Gateway reachability on the configured host and port.

Standalone and stdlib-only, so it runs before `uv sync` and needs nothing from
the package it sits beside. It opens a TCP connection and closes it. It sends no
API handshake, names no account and reads no market data, because a reachability
probe that logs in is not a reachability probe.

Every figure it prints is measured. An unreachable gateway is recorded as a
measured refusal with its errno, never as a retry that eventually succeeded and
never as an assumption that the operator will start one.
"""

from __future__ import annotations

import argparse
import errno
import json
import os
import socket
import time
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]


def load_env(path: Path) -> dict[str, str]:
    """Read KEY=VALUE lines from a .env file. Values are never printed."""
    values: dict[str, str] = {}
    if not path.exists():
        return values
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        values[key.strip()] = value.strip()
    return values


def probe_once(host: str, port: int, timeout: float) -> dict[str, object]:
    """One TCP connect attempt, timed. Records the errno on refusal."""
    started = time.perf_counter()
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(timeout)
    try:
        sock.connect((host, port))
    except OSError as exc:
        elapsed = time.perf_counter() - started
        return {
            "reachable": False,
            "elapsed_ms": round(elapsed * 1000, 3),
            "errno": exc.errno,
            "errno_name": errno.errorcode.get(exc.errno or 0, "UNKNOWN"),
            "message": str(exc),
        }
    else:
        elapsed = time.perf_counter() - started
        return {
            "reachable": True,
            "elapsed_ms": round(elapsed * 1000, 3),
            "errno": None,
            "errno_name": None,
            "message": "tcp connect succeeded; no API handshake was sent",
        }
    finally:
        sock.close()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--attempts", type=int, default=5)
    parser.add_argument("--timeout", type=float, default=5.0)
    parser.add_argument("--out", default="reports/task0/gateway_reachability.json")
    args = parser.parse_args()

    env = {**load_env(REPO / ".env"), **os.environ}
    host = env.get("MBT_IB_HOST", "")
    port_text = env.get("MBT_IB_PAPER_PORT", "")
    missing = [name for name, value in (("MBT_IB_HOST", host), ("MBT_IB_PAPER_PORT", port_text)) if not value]
    if missing:
        print(f"REFUSED: missing required environment variables: {', '.join(missing)}")
        return 2
    port = int(port_text)

    attempts = [probe_once(host, port, args.timeout) for _ in range(args.attempts)]
    reachable = [a for a in attempts if a["reachable"]]

    # The account number is a credential-shaped identifier and never leaves the
    # environment. Only its prefix and length are recorded, which is all the
    # provenance guard needs and all a reader needs to check the shape.
    account = env.get("MBT_IB_PAPER_ACCOUNT", "")
    account_shape = {
        "configured": bool(account),
        "prefix": account[:1] if account else None,
        "length": len(account) if account else 0,
        "note": "the number itself never enters an artifact; the prefix is the provenance signal",
    }

    payload = {
        "probe": "ib_gateway_tcp_reachability",
        "taken_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "host": host,
        "port": port,
        "port_role": "paper",
        "attempts": attempts,
        "attempts_total": len(attempts),
        "attempts_reachable": len(reachable),
        "verdict": "REACHABLE" if reachable else "UNREACHABLE",
        "configured_client_id_present": bool(env.get("MBT_IB_PAPER_CLIENT_ID", "")),
        "paper_account_shape": account_shape,
        "what_this_does_not_establish": (
            "A TCP connect proves a listener, not a session. Account list, futures "
            "options permission on CME crypto products, chain enumeration and market "
            "data subscription state each need an API handshake and are recorded "
            "Absent until one succeeds."
        ),
    }

    out = REPO / args.out
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0 if reachable else 1


if __name__ == "__main__":
    raise SystemExit(main())
