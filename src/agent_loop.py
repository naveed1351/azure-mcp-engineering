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
