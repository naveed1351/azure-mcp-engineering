"""Demo: the `monitor` (Log Analytics/KQL) and `kusto` (Data Explorer)
namespaces."""
import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.mcp_client import connect

async def main() -> None:
    async with connect(namespaces=["monitor", "kusto"], read_only=True) as client:
        # Example KQL: errors logged in the last hour across a workspace.
        query = "AppExceptions | where TimeGenerated > ago(1h) | take 20"
        result = await client.call_tool(
            "azmcp_monitor_log_query",
            {"query": query},
        )
        print("Query results:")
        print(result.content)
