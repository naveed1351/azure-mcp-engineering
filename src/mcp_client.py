"""A thin, reusable wrapper around the MCP Python SDK for talking to the
Azure MCP Server over stdio.

Every notebook/example in this course builds on :func:`build_server_params`
and :class:`AzureMcpClient` instead of re-implementing the stdio plumbing
each time.
"""
from __future__ import annotations

from contextlib import asynccontextmanager
from typing import Any, AsyncIterator, Sequence

from mcp import ClientSession, StdioServerParameters, types
from mcp.client.stdio import stdio_client


def build_server_params(
    namespaces: Sequence[str] | None = None,
    read_only: bool = False,
    mode: str | None = None,
    debug: bool = False,
) -> StdioServerParameters:
    """Build the ``npx @azure/mcp@latest server start`` arguments.

    Parameters mirror the ``azmcp`` start options documented in
    ``docs/05_tools_reference.md`` (Mode, Namespace, Read only, Debug).
    """
    args = ["-y", "@azure/mcp@latest", "server", "start"]
    for namespace in namespaces or []:
        args += ["--namespace", namespace]
    if read_only:
        args.append("--read-only")
    if mode:
        args += ["--mode", mode]
    if debug:
        args.append("--debug")
    return StdioServerParameters(command="npx", args=args, env=None)
