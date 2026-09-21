"""Demo: the `storage` namespace -- accounts, containers, and blobs."""
import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.mcp_client import connect

async def main() -> None:
    async with connect(namespaces=["storage"], read_only=True) as client:
        accounts = await client.call_tool("azmcp_storage_account_list", {})
        print("Storage accounts:")
        print(accounts.content)
        print(
            "\nTip: once you know an account name, try "
            "azmcp_storage_blob_container_list / azmcp_storage_blob_list "
            "with an 'account' argument."
        )
