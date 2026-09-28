"""Demo: the `pricing` namespace -- Azure retail pricing (a public data tool -- no Azure sign-in needed)."""
import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.mcp_client import connect

async def main() -> None:
    async with connect(namespaces=["pricing"], read_only=True) as client:
        result = await client.call_tool(
            "azmcp_pricing_get",
            {
                "service": "Virtual Machines",
            },
        )
        print("Retail pricing for Virtual Machines:")
        print(result.content)

if __name__ == "__main__":
    asyncio.run(main())
