"""A minimal, reusable conversational agent that wires an LLM (Azure OpenAI)
together with Azure MCP Server tool calls.

This is the programmatic counterpart to
``notebooks/07_building_a_conversational_agent.ipynb`` and is also used
directly by ``examples/10_multi_turn_agent_cli.py``.
"""
from __future__ import annotations

import argparse
import asyncio
import logging

from .azure_openai_helper import apply_tool_result, chat_with_tools, get_azure_openai_client
from .config import get_settings
from .mcp_client import AzureMcpClient, build_server_params

logger = logging.getLogger(__name__)

class ConversationAgent:
    """Holds one growing message history and drives the tool-calling loop
    against a single, already-connected :class:`AzureMcpClient`."""

    def __init__(self, mcp_client: AzureMcpClient, model: str | None = None):
        self.mcp_client = mcp_client
        settings = get_settings()
        self.model = model or settings.azure_openai_model
        self.openai_client = get_azure_openai_client(settings)
        self.messages: list[dict] = []
        self._tools_schema: list[dict] | None = None

    async def run_turn(self, user_input: str) -> str:
        """Run one full user-turn: model call -> optional tool calls -> final answer."""
        if self._tools_schema is None:
            self._tools_schema = await self.mcp_client.tools_as_openai_functions()

        self.messages.append({"role": "user", "content": user_input})

        response = chat_with_tools(self.openai_client, self.model, self.messages, self._tools_schema)
        response_message = response.choices[0].message
        self.messages.append(response_message)

        if response_message.tool_calls:
            for tool_call in response_message.tool_calls:
                import json as _json

                args = _json.loads(tool_call.function.arguments or "{}")
                result = await self.mcp_client.call_tool(tool_call.function.name, args)
                apply_tool_result(self.messages, tool_call, result.content)
        else:
            logger.info("Model answered directly without calling a tool.")

        final = chat_with_tools(self.openai_client, self.model, self.messages, self._tools_schema)
        return final.choices[0].message.content or ""
