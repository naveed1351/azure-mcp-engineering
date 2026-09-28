"""Demo: the `speech` namespace -- speech-to-text recognition (a local-required tool that reads an audio file from disk).

Replace the placeholder 'endpoint' and 'file' arguments below with a real Azure AI Services Speech endpoint and local audio file before running."""
import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.mcp_client import connect

async def main() -> None:
    async with connect(namespaces=["speech"], read_only=True) as client:
        result = await client.call_tool(
            "azmcp_speech_stt_recognize",
            {
                "endpoint": "<speech-service-endpoint>",
                "file": "<path-to-audio.wav>",
            },
        )
        print("Speech-to-text result:")
        print(result.content)

if __name__ == "__main__":
    asyncio.run(main())
