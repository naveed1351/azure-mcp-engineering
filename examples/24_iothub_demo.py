"""Demo: the `iothub` namespace -- IoT Hub details.

Replace the placeholder 'resource-group' and 'hub-name' arguments
below with a real IoT Hub before running."""
import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.mcp_client import connect

async def main() -> None:
    async with connect(namespaces=["iothub"], read_only=True) as client:
        result = await client.call_tool(
            "azmcp_iothub_hub_get",
            {
                "resource-group": "<resource-group>",
                "hub-name": "<iot-hub-name>",
            },
        )
        print("IoT Hub details:")
        print(result.content)

if __name__ == "__main__":
    asyncio.run(main())
