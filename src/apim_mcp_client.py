"""Helpers for connecting to Model Context Protocol (MCP) servers exposed
through Azure API Management's AI gateway.

``src/mcp_client.py`` launches a *local* Azure MCP Server process over
stdio. The helpers here instead connect to a *remote* MCP server over
Streamable HTTP -- the transport Azure API Management uses for MCP servers
it hosts (either "REST API as MCP server" or a federated existing server).
See ``docs/10_apim_ai_gateway_and_mcp.md`` for the conceptual background.
"""
from __future__ import annotations

from contextlib import asynccontextmanager
from typing import AsyncIterator

from azure.identity import DefaultAzureCredential, get_bearer_token_provider
from mcp import ClientSession
from mcp.client.streamable_http import streamablehttp_client


def get_entra_bearer_token(scope: str) -> str:
    """Fetch a Microsoft Entra ID access token for *scope*.

    Uses the same :class:`~azure.identity.DefaultAzureCredential` chain as
    :func:`src.azure_openai_helper.get_azure_openai_client` (see
    ``docs/04_authentication.md``). *scope* is typically the App ID URI of
    the Microsoft Entra application registered for the MCP server, plus
    ``/.default``, for example ``api://<app-id>/.default``.
    """
    token_provider = get_bearer_token_provider(DefaultAzureCredential(), scope)
    return token_provider()


def build_auth_headers(
    *,
    subscription_key: str | None = None,
    bearer_token: str | None = None,
) -> dict[str, str]:
    """Build the request headers Azure API Management expects for a secured
    MCP server (see ``docs/10_apim_ai_gateway_and_mcp.md``).

    - ``subscription_key`` becomes the ``Ocp-Apim-Subscription-Key`` header,
      validated whenever the MCP server is associated with an API Management
      product that requires a subscription.
    - ``bearer_token`` becomes an ``Authorization: Bearer <token>`` header,
      validated by a ``validate-azure-ad-token`` policy on the MCP server.
    """
    headers: dict[str, str] = {}
    if subscription_key:
        headers["Ocp-Apim-Subscription-Key"] = subscription_key
    if bearer_token:
        headers["Authorization"] = f"Bearer {bearer_token}"
    return headers


@asynccontextmanager
async def connect_apim_mcp(
    server_url: str,
    *,
    subscription_key: str | None = None,
    bearer_token: str | None = None,
) -> AsyncIterator[ClientSession]:
    """Async context manager for an MCP ``ClientSession`` connected over
    Streamable HTTP to an Azure API Management-hosted MCP server endpoint.

    Example
    -------
    >>> async with connect_apim_mcp(
    ...     "https://my-apim.azure-api.net/my-mcp-server/mcp",
    ...     subscription_key="<key>",
    ... ) as session:
    ...     tools = await session.list_tools()
    ...     print(tools)
    """
    headers = build_auth_headers(subscription_key=subscription_key, bearer_token=bearer_token)
    async with streamablehttp_client(server_url, headers=headers or None) as (read, write, _get_session_id):
        async with ClientSession(read, write) as session:
            await session.initialize()
            yield session
