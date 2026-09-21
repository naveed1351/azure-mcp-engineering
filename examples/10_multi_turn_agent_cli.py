"""Full interactive multi-turn Azure MCP Server agent.

This is a thin CLI wrapper around src.agent_loop.ConversationAgent; run it
directly to chat with your Azure resources from the terminal:

    python examples/10_multi_turn_agent_cli.py --read-only --namespace storage
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.agent_loop import _main
import asyncio

# All of the actual argument parsing / connection / loop logic lives in
# src/agent_loop.py so it can be reused from notebooks too; this file is
# intentionally just an entry point.

if __name__ == "__main__":
    asyncio.run(_main())
