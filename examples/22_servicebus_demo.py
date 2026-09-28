"""Demo: the `servicebus` namespace -- runtime details for a Service Bus queue.

Replace the placeholder 'namespace' (the Service Bus namespace, not
an MCP namespace) and 'queue' arguments below before running."""
import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.mcp_client import connect

async def main() -> None:
    async with connect(namespaces=["servicebus"], read_only=True) as client:
        result = await client.call_tool(
            "azmcp_servicebus_queue_details",
            {
                "namespace": "<service-bus-namespace>",
                "queue": "<queue-name>",
            },
        )
        print("Service Bus queue details:")
        print(result.content)

if __name__ == "__main__":
    asyncio.run(main())
