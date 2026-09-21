"""One-shot Azure OpenAI + Azure MCP Server function-calling round trip.

Usage: python examples/03_chat_with_tools.py "List my resource groups"
"""
import asyncio
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.azure_openai_helper import apply_tool_result, chat_with_tools, get_azure_openai_client
from src.config import get_settings
from src.mcp_client import connect
