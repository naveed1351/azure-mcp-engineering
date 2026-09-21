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

class AzureMcpClient:
    """Async context manager wrapping an MCP ``ClientSession`` connected to
    a locally-launched Azure MCP Server process.

    Example
    -------
    >>> async with AzureMcpClient() as client:
    ...     tools = await client.list_tools()
    ...     result = await client.call_tool("azmcp_subscription_list", {})
    """

    def __init__(self, server_params: StdioServerParameters | None = None):
        self.server_params = server_params or build_server_params()
        self._stdio_ctx = None
        self._session_ctx = None
        self.session: ClientSession | None = None

    async def __aenter__(self) -> "AzureMcpClient":
        self._stdio_ctx = stdio_client(self.server_params)
        read, write = await self._stdio_ctx.__aenter__()
        self._session_ctx = ClientSession(read, write)
        self.session = await self._session_ctx.__aenter__()
        await self.session.initialize()
        return self

    async def __aexit__(self, exc_type, exc, tb) -> None:
        if self._session_ctx is not None:
            await self._session_ctx.__aexit__(exc_type, exc, tb)
        if self._stdio_ctx is not None:
            await self._stdio_ctx.__aexit__(exc_type, exc, tb)
