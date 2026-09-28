"""Demo: the `functionapp` namespace -- Azure Functions apps."""
import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.mcp_client import connect

async def main() -> None:
    async with connect(namespaces=["functionapp"], read_only=True) as client:
        result = await client.call_tool("azmcp_functionapp_get", {})
        print("Function apps:")
        print(result.content)

if __name__ == "__main__":
    asyncio.run(main())
