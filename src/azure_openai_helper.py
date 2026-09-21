"""Azure OpenAI client + function-calling helpers used by the agent notebooks."""
from __future__ import annotations

import json
from typing import Any

from azure.identity import DefaultAzureCredential, get_bearer_token_provider
from openai import AzureOpenAI

from .config import Settings, require_azure_openai

_COGNITIVE_SERVICES_SCOPE = "https://cognitiveservices.azure.com/.default"

def get_azure_openai_client(settings: Settings | None = None) -> AzureOpenAI:
    """Build an ``AzureOpenAI`` client authenticated via Entra ID (no API keys).

    Uses :class:`~azure.identity.DefaultAzureCredential`, which tries
    environment variables, managed identity, the Azure CLI, and other
    credential sources in turn -- the same chain the Azure MCP Server itself
    uses (see ``docs/04_authentication.md``).
    """
    settings = require_azure_openai(settings)
    token_provider = get_bearer_token_provider(DefaultAzureCredential(), _COGNITIVE_SERVICES_SCOPE)
    return AzureOpenAI(
        azure_endpoint=settings.azure_openai_endpoint,
        api_version="2024-04-01-preview",
        azure_ad_token_provider=token_provider,
    )

def chat_with_tools(
    client: AzureOpenAI,
    model: str,
    messages: list[dict[str, Any]],
    tools: list[dict[str, Any]],
):
    """Call the chat completions API with a tool/function schema attached.

    This is a thin wrapper so notebooks can call one function instead of
    repeating the same ``client.chat.completions.create(...)`` boilerplate
    on every turn.
    """
    return client.chat.completions.create(model=model, messages=messages, tools=tools)

def apply_tool_result(
    messages: list[dict[str, Any]],
    tool_call: Any,
    result_content: Any,
) -> None:
    """Append a tool's result back onto the running message history in the
    shape the chat completions API expects for a ``role: tool`` message.

    ``result_content`` is typically ``CallToolResult.content`` from the MCP
    SDK; it is stringified defensively since MCP content can be structured.
    """
    if not isinstance(result_content, str):
        result_content = json.dumps(result_content, default=str)
    messages.append(
        {
            "tool_call_id": tool_call.id,
            "role": "tool",
            "name": tool_call.function.name,
            "content": result_content,
        }
    )
