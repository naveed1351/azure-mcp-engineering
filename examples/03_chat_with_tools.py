"""One-shot Azure OpenAI + Azure MCP Server function-calling round trip.

Usage: python examples/03_chat_with_tools.py "List my resource groups"
"""
import asyncio
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.azure_openai_helper import apply_tool_result, chat_with_tools, get_azure_openai_client
from src.config import get_settings
from src.mcp_client import connect

async def main(prompt: str) -> None:
    settings = get_settings()
    openai_client = get_azure_openai_client(settings)

    async with connect(read_only=True) as mcp_client:
        tools = await mcp_client.tools_as_openai_functions()
        messages = [{"role": "user", "content": prompt}]

        response = chat_with_tools(openai_client, settings.azure_openai_model, messages, tools)
        message = response.choices[0].message
        messages.append(message)

        if message.tool_calls:
            for call in message.tool_calls:
                args = json.loads(call.function.arguments or "{}")
                result = await mcp_client.call_tool(call.function.name, args)
                apply_tool_result(messages, call, result.content)

        final = chat_with_tools(openai_client, settings.azure_openai_model, messages, tools)
        print(final.choices[0].message.content)

if __name__ == "__main__":
    user_prompt = " ".join(sys.argv[1:]) or "List my resource groups"
    asyncio.run(main(user_prompt))
