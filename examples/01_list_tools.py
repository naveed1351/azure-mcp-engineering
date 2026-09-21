"""List every tool the Azure MCP Server exposes, grouped by namespace."""
import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.mcp_client import connect
from src.tool_catalog import group_tools_by_namespace

async def main() -> None:
    async with connect() as client:
        tools = await client.list_tools()
        grouped = group_tools_by_namespace(tools)
        print(f"Discovered {len(tools)} tools across {len(grouped)} namespaces:\n")
        for namespace, infos in grouped.items():
            print(f"[{namespace}] ({len(infos)} tools)")
            for info in infos:
                print(f"  - {info.name}: {info.description}")

if __name__ == "__main__":
    asyncio.run(main())
