"""List every tool the Azure MCP Server exposes, grouped by namespace."""
import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.mcp_client import connect
from src.tool_catalog import group_tools_by_namespace
