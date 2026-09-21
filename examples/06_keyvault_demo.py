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
