"""Demo: the `workbooks` namespace -- Azure Monitor workbooks.

Replace the placeholder 'resource-group' argument below with a real resource group before running."""
import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.mcp_client import connect

async def main() -> None:
    async with connect(namespaces=["workbooks"], read_only=True) as client:
        result = await client.call_tool(
            "azmcp_workbooks_list",
            {
                "resource-group": "<resource-group>",
            },
        )
        print("Azure Monitor workbooks:")
        print(result.content)

if __name__ == "__main__":
    asyncio.run(main())
