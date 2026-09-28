"""Demo: the `fileshares` namespace -- Azure File Shares.

Replace the placeholder 'resource-group' and 'name' arguments below
with a real Azure File Share before running."""
import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.mcp_client import connect

async def main() -> None:
    async with connect(namespaces=["fileshares"], read_only=True) as client:
        result = await client.call_tool(
            "azmcp_fileshares_fileshare_get",
            {
                "resource-group": "<resource-group>",
                "name": "<file-share-name>",
            },
        )
        print("File share details:")
        print(result.content)

if __name__ == "__main__":
    asyncio.run(main())
