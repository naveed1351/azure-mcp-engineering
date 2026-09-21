"""Demo: subscription + resource group tools (the `subscription` / `group`
namespaces)."""
import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.mcp_client import connect

async def main() -> None:
    async with connect(namespaces=["subscription", "group"], read_only=True) as client:
        subs = await client.call_tool("azmcp_subscription_list", {})
        print("Subscriptions:")
        print(subs.content)

        groups = await client.call_tool("azmcp_group_list", {})
        print("\nResource groups in the default subscription:")
        print(groups.content)
