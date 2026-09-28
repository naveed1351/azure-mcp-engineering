"""Demo: the `marketplace` namespace -- Azure Marketplace products available to the subscription."""
import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.mcp_client import connect

async def main() -> None:
    async with connect(namespaces=["marketplace"], read_only=True) as client:
        result = await client.call_tool("azmcp_marketplace_product_list", {})
        print("Marketplace products:")
        print(result.content)

if __name__ == "__main__":
    asyncio.run(main())
