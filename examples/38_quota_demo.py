"""Demo: the `quota` namespace -- regional quota / capacity availability for a resource type."""
import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.mcp_client import connect

async def main() -> None:
    async with connect(namespaces=["quota"], read_only=True) as client:
        result = await client.call_tool(
            "azmcp_quota_region_availability_list",
            {
                "resource-types": "Microsoft.Compute/virtualMachines",
            },
        )
        print("Regional quota availability:")
        print(result.content)

if __name__ == "__main__":
    asyncio.run(main())
