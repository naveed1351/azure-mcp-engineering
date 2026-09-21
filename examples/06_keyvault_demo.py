"""Demo: the `keyvault` namespace.

Reading secrets triggers *elicitation* (user confirmation) in interactive
clients -- see docs/05_tools_reference.md. This script only lists vaults by
default to stay safe to run non-interactively.
"""
import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.mcp_client import connect

async def main() -> None:
    async with connect(namespaces=["keyvault"], read_only=True) as client:
        vaults = await client.call_tool("azmcp_keyvault_list", {})
        print("Key Vaults in the default subscription:")
        print(vaults.content)
        print(
            "\nTo read a secret, call azmcp_keyvault_secret_get with a "
            "'vault' and 'secret' name -- expect an elicitation / "
            "confirmation prompt in interactive clients."
        )

if __name__ == "__main__":
    asyncio.run(main())
