"""Demo: the `role` namespace -- RBAC role assignments.

Replace the placeholder 'scope' argument below with a real subscription, resource group, or resource ID before running."""
import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.mcp_client import connect

async def main() -> None:
    async with connect(namespaces=["role"], read_only=True) as client:
        result = await client.call_tool(
            "azmcp_role_assignment_list",
            {
                "scope": "/subscriptions/<subscription-id>",
            },
        )
        print("RBAC role assignments:")
        print(result.content)

if __name__ == "__main__":
    asyncio.run(main())
