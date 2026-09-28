"""Demo: the `sql` namespace -- Azure SQL servers.

Replace the placeholder 'resource-group' argument below with a real
resource group before running."""
import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.mcp_client import connect

async def main() -> None:
    async with connect(namespaces=["sql"], read_only=True) as client:
        result = await client.call_tool(
            "azmcp_sql_server_get",
            {
                "resource-group": "<resource-group>",
            },
        )
        print("SQL servers:")
        print(result.content)

if __name__ == "__main__":
    asyncio.run(main())
