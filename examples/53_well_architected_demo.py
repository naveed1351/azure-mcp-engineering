"""Demo: the `wellarchitectedframework` namespace -- Azure Well-Architected Framework service guides."""
import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.mcp_client import connect

async def main() -> None:
    async with connect(namespaces=["wellarchitectedframework"], read_only=True) as client:
        result = await client.call_tool("azmcp_wellarchitectedframework_serviceguide_get", {})
        print("Well-Architected service guides:")
        print(result.content)

if __name__ == "__main__":
    asyncio.run(main())
