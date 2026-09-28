"""Demo: the `deviceregistry` namespace -- Device Registry namespaces for organizing IoT device assets."""
import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.mcp_client import connect

async def main() -> None:
    async with connect(namespaces=["deviceregistry"], read_only=True) as client:
        result = await client.call_tool("azmcp_deviceregistry_namespace_list", {})
        print("Device Registry namespaces:")
        print(result.content)

if __name__ == "__main__":
    asyncio.run(main())
