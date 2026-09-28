"""Demo: the `servicefabric` namespace -- Service Fabric managed cluster nodes.

Replace the placeholder 'resource-group' and 'cluster' arguments
below with a real Service Fabric managed cluster before running."""
import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.mcp_client import connect

async def main() -> None:
    async with connect(namespaces=["servicefabric"], read_only=True) as client:
        result = await client.call_tool(
            "azmcp_servicefabric_managedcluster_node_get",
            {
                "resource-group": "<resource-group>",
                "cluster": "<cluster-name>",
            },
        )
        print("Service Fabric managed cluster nodes:")
        print(result.content)

if __name__ == "__main__":
    asyncio.run(main())
