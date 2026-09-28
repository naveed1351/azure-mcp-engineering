"""Demo: the `compute` namespace -- virtual machines."""
import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.mcp_client import connect

async def main() -> None:
    async with connect(namespaces=["compute"], read_only=True) as client:
        result = await client.call_tool("azmcp_compute_vm_get", {})
        print("Virtual machines:")
        print(result.content)

if __name__ == "__main__":
    asyncio.run(main())
