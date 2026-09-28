"""Demo: the `sreagent` namespace -- Azure SRE Agent resources."""
import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.mcp_client import connect

async def main() -> None:
    async with connect(namespaces=["sreagent"], read_only=True) as client:
        result = await client.call_tool("azmcp_sreagent_agents_list", {})
        print("SRE Agent resources:")
        print(result.content)

if __name__ == "__main__":
    asyncio.run(main())
