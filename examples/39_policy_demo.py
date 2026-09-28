"""Demo: the `policy` namespace -- Azure Policy assignments."""
import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.mcp_client import connect

async def main() -> None:
    async with connect(namespaces=["policy"], read_only=True) as client:
        result = await client.call_tool("azmcp_policy_assignment_list", {})
        print("Policy assignments:")
        print(result.content)

if __name__ == "__main__":
    asyncio.run(main())
