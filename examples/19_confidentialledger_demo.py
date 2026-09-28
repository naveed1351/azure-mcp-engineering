"""Demo: the `confidentialledger` namespace -- tamper-proof Confidential Ledger entries.

Replace the placeholder 'ledger' and 'transaction-id' arguments
below with a real ledger and transaction ID before running."""
import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.mcp_client import connect

async def main() -> None:
    async with connect(namespaces=["confidentialledger"], read_only=True) as client:
        result = await client.call_tool(
            "azmcp_confidentialledger_entries_get",
            {
                "ledger": "<ledger-name>",
                "transaction-id": "<transaction-id>",
            },
        )
        print("Confidential Ledger entry:")
        print(result.content)

if __name__ == "__main__":
    asyncio.run(main())
