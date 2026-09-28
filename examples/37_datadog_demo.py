"""Demo: the `datadog` namespace -- resources monitored through the Datadog Native ISV integration."""
import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.mcp_client import connect

async def main() -> None:
    async with connect(namespaces=["datadog"], read_only=True) as client:
        result = await client.call_tool("azmcp_datadog_monitoredresources_list", {})
        print("Datadog-monitored resources:")
        print(result.content)

if __name__ == "__main__":
    asyncio.run(main())
