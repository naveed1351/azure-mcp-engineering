"""Demo: the `cosmos` namespace -- accounts, databases, and containers."""
import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.mcp_client import connect

async def main() -> None:
    async with connect(namespaces=["cosmos"], read_only=True) as client:
        accounts = await client.call_tool("azmcp_cosmos_account_list", {})
        print("Cosmos DB accounts:")
        print(accounts.content)

if __name__ == "__main__":
    asyncio.run(main())
