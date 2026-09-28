"""Demo: the `appservice` namespace -- App Service web apps."""
import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.mcp_client import connect

async def main() -> None:
    async with connect(namespaces=["appservice"], read_only=True) as client:
        result = await client.call_tool("azmcp_appservice_webapp_get", {})
        print("App Service web apps:")
        print(result.content)

if __name__ == "__main__":
    asyncio.run(main())
