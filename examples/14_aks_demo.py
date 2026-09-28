"""Demo: the `aks` namespace -- Azure Kubernetes Service clusters."""
import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.mcp_client import connect

async def main() -> None:
    async with connect(namespaces=["aks"], read_only=True) as client:
        result = await client.call_tool("azmcp_aks_cluster_get", {})
        print("AKS clusters:")
        print(result.content)

if __name__ == "__main__":
    asyncio.run(main())
