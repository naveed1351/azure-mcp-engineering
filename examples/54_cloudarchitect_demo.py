"""Demo: the `cloudarchitect` namespace -- the Cloud Architect design assistant."""
import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.mcp_client import connect

async def main() -> None:
    async with connect(namespaces=["cloudarchitect"], read_only=True) as client:
        result = await client.call_tool(
            "azmcp_cloudarchitect_design",
            {
                "question": "What type of application are you building?",
            },
        )
        print("Cloud Architect design guidance:")
        print(result.content)

if __name__ == "__main__":
    asyncio.run(main())
