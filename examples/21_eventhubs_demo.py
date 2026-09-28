"""Demo: the `eventhubs` namespace -- Event Hubs namespaces."""
import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.mcp_client import connect

async def main() -> None:
    async with connect(namespaces=["eventhubs"], read_only=True) as client:
        result = await client.call_tool("azmcp_eventhubs_namespace_get", {})
        print("Event Hubs namespaces:")
        print(result.content)

if __name__ == "__main__":
    asyncio.run(main())
