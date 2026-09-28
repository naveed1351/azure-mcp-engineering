"""Demo: the `functions` namespace -- supported Azure Functions programming languages (a metadata-only tool -- no Azure sign-in needed)."""
import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.mcp_client import connect

async def main() -> None:
    async with connect(namespaces=["functions"], read_only=True) as client:
        result = await client.call_tool("azmcp_functions_language_list", {})
        print("Supported Azure Functions languages:")
        print(result.content)

if __name__ == "__main__":
    asyncio.run(main())
