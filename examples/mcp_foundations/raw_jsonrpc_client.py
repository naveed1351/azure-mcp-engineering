"""A hand-rolled MCP client using nothing but the standard library, to show
exactly what bytes flow over stdio -- no `mcp` SDK involved.

This exists purely to teach notebook 24 (JSON-RPC anatomy); every other
notebook/example in this course uses the real SDK (src/mcp_client.py or the
ClientSession pattern in notebooks 25-27) the way you actually would.

Run it directly:

    python examples/mcp_foundations/raw_jsonrpc_client.py
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

SERVER_SCRIPT = str(Path(__file__).resolve().parent / "custom_server.py")


def send(proc: subprocess.Popen, message: dict) -> None:
    """Write one newline-delimited JSON-RPC message to the server's stdin.

    Per the MCP stdio transport spec, messages are delimited by newlines
    and must not contain embedded newlines -- json.dumps with no
    indentation guarantees that.
    """
    line = json.dumps(message) + "\n"
    proc.stdin.write(line.encode("utf-8"))
    proc.stdin.flush()


def receive(proc: subprocess.Popen) -> dict:
    """Read one newline-delimited JSON-RPC message from the server's stdout."""
    line = proc.stdout.readline()
    return json.loads(line)


def main() -> None:
    proc = subprocess.Popen(
        [sys.executable, SERVER_SCRIPT],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
    )
    try:
        # 1. initialize -- the client MUST send this first (MCP lifecycle
        #    spec). Note there is no "initialized" response here; the
        #    server replies to this specific request, then the client
        #    still owes it an "initialized" *notification* below.
        send(
            proc,
            {
                "jsonrpc": "2.0",
                "id": 1,
                "method": "initialize",
                "params": {
                    "protocolVersion": "2025-06-18",
                    "capabilities": {},
                    "clientInfo": {"name": "raw-jsonrpc-demo", "version": "1.0.0"},
                },
            },
        )
        print("initialize response:")
        print(json.dumps(receive(proc), indent=2))

        # 2. initialized -- a *notification*: no "id" field, and the server
        #    sends no response at all.
        send(proc, {"jsonrpc": "2.0", "method": "notifications/initialized"})

        # 3. tools/list -- now normal ("operation phase") requests are allowed.
        send(proc, {"jsonrpc": "2.0", "id": 2, "method": "tools/list", "params": {}})
        print("\ntools/list response:")
        print(json.dumps(receive(proc), indent=2))

        # 4. tools/call -- invoke the "add" tool defined in custom_server.py.
        send(
            proc,
            {
                "jsonrpc": "2.0",
                "id": 3,
                "method": "tools/call",
                "params": {"name": "add", "arguments": {"a": 2, "b": 3}},
            },
        )
        print("\ntools/call response:")
        print(json.dumps(receive(proc), indent=2))
    finally:
        proc.terminate()


if __name__ == "__main__":
    main()
