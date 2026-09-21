"""Demo: subscription + resource group tools (the `subscription` / `group`
namespaces)."""
import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.mcp_client import connect
