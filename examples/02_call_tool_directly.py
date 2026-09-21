"""Call an Azure MCP Server tool directly, with no LLM in the loop.

This demonstrates the lowest-level building block every other example in
this course is built on: `session.call_tool(name, arguments)`.
"""
import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.mcp_client import connect

async def main() -> None:
    async with connect(read_only=True) as client:
        # No arguments needed: the server resolves the default subscription
        # from your `az login` session unless you pass one explicitly.
        result = await client.call_tool("azmcp_subscription_list", {})
        print("Subscriptions available to your signed-in account:\n")
        print(result.content)
