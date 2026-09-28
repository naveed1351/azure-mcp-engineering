"""Demo: the `appconfig` namespace -- centralized settings and feature flags."""
import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.mcp_client import connect

async def main() -> None:
    async with connect(namespaces=["appconfig"], read_only=True) as client:
        result = await client.call_tool("azmcp_appconfig_account_list", {})
        print("App Configuration stores:")
        print(result.content)

if __name__ == "__main__":
    asyncio.run(main())
