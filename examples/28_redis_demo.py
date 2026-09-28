"""Demo: the `redis` namespace -- Azure Managed Redis / Azure Cache for Redis resources."""
import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.mcp_client import connect

async def main() -> None:
    async with connect(namespaces=["redis"], read_only=True) as client:
        result = await client.call_tool("azmcp_redis_list", {})
        print("Redis resources:")
        print(result.content)

if __name__ == "__main__":
    asyncio.run(main())
