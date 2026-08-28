"""The connectivity probe. Read-only twice over.

This module can encode exactly two outbound API messages, START_API
(71) and REQ_CURRENT_TIME (49), and the encoder refuses every other
message id, so no order can leave here even in principle. No broker
library is imported: the module speaks the minimal v100 TWS wire
protocol itself, which is what keeps the order vocabulary out of the
import graph entirely. The Gateway's Read-Only API setting backs this
from the other side, and this stage never asks for it off.

The probe asserts the declared mode matches the port before any
connection, requests the managed-accounts list and server time,
verifies the pinned account appears with the mode-correct prefix, and
disconnects. Unreachable is a recorded state, not an error: C.1's
demonstrations run against the mock, and C.3's dry formation will call
this as its pre-flight, which also gives the operator the Sunday
reauth deadness check in software.
"""
from __future__ import annotations

import socket
import struct
import time
from dataclasses import dataclass

from hfexperiment.brokerconfig import (
    DECLARED_MODE,
    MODE_PORTS,
    MODE_PREFIXES,
    BrokerEnv,
)
from hfexperiment.gate import Refusal

# The only messages this module can send. The encoder enforces it.
START_API = 71
REQ_CURRENT_TIME = 49
OUTBOUND_MESSAGE_IDS = frozenset({START_API, REQ_CURRENT_TIME})

# Inbound ids the reader understands. Everything else is skipped.
_MANAGED_ACCTS = "15"
_CURRENT_TIME = "49"

_HANDSHAKE_VERSIONS = b"v100..187"
_MAX_FRAME_BYTES = 1 << 20


class ProbeProtocolError(RuntimeError):
    """The wire did something the minimal reader does not accept."""


@dataclass(frozen=True)
class ProbeResult:
    """One probe outcome, every state a recorded state."""

    state: str
    detail: str
    server_version: int | None = None
    server_time_epoch: int | None = None
    managed_accounts: tuple[str, ...] = ()


def assert_mode_port(mode: str, port: int) -> Refusal | None:
    """The declared mode must match the port before any connection."""
    if mode not in MODE_PORTS:
        raise ValueError(f"undeclared mode: {mode}")
    expected = MODE_PORTS[mode]
    if port != expected:
        return Refusal(
            reason="mode_port_mismatch",
            arithmetic=f"declared mode {mode} requires port {expected}, "
                       f".env has {port}. Refused before connecting.",
        )
    return None


def _frame(payload: bytes) -> bytes:
    return struct.pack(">I", len(payload)) + payload


def encode_message(msg_id: int, *fields: object) -> bytes:
    """One outbound frame. Refuses every id outside the read-only set."""
    if msg_id not in OUTBOUND_MESSAGE_IDS:
        raise ProbeProtocolError(
            f"message id {msg_id} is not in the read-only set "
            f"{sorted(OUTBOUND_MESSAGE_IDS)}: this module cannot send it"
        )
    payload = b"".join(
        str(f).encode("ascii") + b"\x00" for f in (msg_id, *fields)
    )
    return _frame(payload)


def _recv_exact(sock: socket.socket, n: int) -> bytes:
    chunks = b""
    while len(chunks) < n:
        piece = sock.recv(n - len(chunks))
        if not piece:
            raise ProbeProtocolError("connection closed mid-frame")
        chunks += piece
    return chunks


def _recv_fields(sock: socket.socket) -> list[str]:
    (length,) = struct.unpack(">I", _recv_exact(sock, 4))
    if length > _MAX_FRAME_BYTES:
        raise ProbeProtocolError(f"frame of {length} bytes refused")
    payload = _recv_exact(sock, length)
    return payload.decode("latin-1").split("\x00")[:-1]


def probe(
    env: BrokerEnv, mode: str = DECLARED_MODE, timeout_s: float = 6.0
) -> ProbeResult:
    """Connect, verify, disconnect. Every outcome recorded, none raised."""
    refusal = assert_mode_port(mode, env.port)
    if refusal is not None:
        return ProbeResult(state="mode_port_mismatch",
                           detail=refusal.arithmetic)
    try:
        sock = socket.create_connection(
            (env.host, env.port), timeout=timeout_s
        )
    except OSError as err:
        return ProbeResult(
            state="unreachable",
            detail=f"{env.host}:{env.port}: {err}. The Gateway is not "
                   "running or not listening. Recorded, not raised.",
        )
    server_version: int | None = None
    server_time: int | None = None
    managed: tuple[str, ...] = ()
    try:
        sock.settimeout(timeout_s)
        sock.sendall(b"API\x00" + _frame(_HANDSHAKE_VERSIONS))
        greeting = _recv_fields(sock)
        server_version = int(greeting[0])
        sock.sendall(encode_message(START_API, 2, env.client_id, ""))
        sock.sendall(encode_message(REQ_CURRENT_TIME, 1))
        deadline = time.monotonic() + timeout_s
        while time.monotonic() < deadline and (
            not managed or server_time is None
        ):
            fields = _recv_fields(sock)
            if not fields:
                continue
            if fields[0] == _MANAGED_ACCTS and len(fields) >= 3:
                managed = tuple(
                    a for a in fields[2].split(",") if a
                )
            elif fields[0] == _CURRENT_TIME and len(fields) >= 3:
                server_time = int(fields[2])
    except (ProbeProtocolError, OSError, ValueError, IndexError) as err:
        return ProbeResult(
            state="protocol_error",
            detail=repr(err),
            server_version=server_version,
            managed_accounts=managed,
        )
    finally:
        sock.close()
    if not managed:
        return ProbeResult(
            state="protocol_error",
            detail="no managed-accounts message arrived before the "
                   "deadline",
            server_version=server_version,
            server_time_epoch=server_time,
        )
    if env.account_id not in managed:
        return ProbeResult(
            state="account_missing",
            detail=f"pinned {env.account_id} not in managed list "
                   f"{managed}",
            server_version=server_version,
            server_time_epoch=server_time,
            managed_accounts=managed,
        )
    prefix = MODE_PREFIXES[mode]
    if not env.account_id.startswith(prefix):
        return ProbeResult(
            state="prefix_mismatch",
            detail=f"pinned {env.account_id} lacks the {mode} prefix "
                   f"{prefix}",
            server_version=server_version,
            server_time_epoch=server_time,
            managed_accounts=managed,
        )
    return ProbeResult(
        state="ok",
        detail=f"account {env.account_id} verified in managed list of "
               f"{len(managed)}, disconnected",
        server_version=server_version,
        server_time_epoch=server_time,
        managed_accounts=managed,
    )
