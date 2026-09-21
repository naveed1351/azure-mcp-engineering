"""Demo: 'learn mode' -- discover a tool's parameters without executing it.

Learn mode is safe to run against any namespace: it returns metadata about
commands/parameters instead of performing the real Azure operation.
"""
import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.mcp_client import connect
