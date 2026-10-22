"""A minimal, from-scratch MCP server used by the Part 3 (MCP protocol
foundations) notebooks 24-28.

Unlike the Azure MCP Server used throughout the rest of this course, this
server has no Azure dependency at all -- it only demonstrates the protocol
primitives themselves (tools, resources, prompts, sampling, elicitation)
using the official MCP Python SDK's high-level `FastMCP` API. You don't
need an Azure subscription, `az login`, or Node.js to run anything in
notebooks 24-28.

Run directly for a quick smoke test (it waits on stdio -- Ctrl+C to exit):

    python examples/mcp_foundations/custom_server.py

The notebooks instead launch it as a subprocess over stdio, the same way
src/mcp_client.py launches the Azure MCP Server elsewhere in this course --
see notebook 25.
"""
from __future__ import annotations

from pydantic import BaseModel, Field

from mcp.server.fastmcp import Context, FastMCP
from mcp.server.session import ServerSession
from mcp.types import SamplingMessage, TextContent

mcp = FastMCP("Foundations Demo Server")


# --- Tools: actions the client can invoke -----------------------------------

@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers together."""
    return a + b


@mcp.tool()
async def generate_poem(topic: str, ctx: Context[ServerSession, None]) -> str:
    """Generate a short poem by asking the CLIENT's LLM via MCP sampling.

    This tool never calls an LLM API directly -- it sends a
    sampling/createMessage request back through the client (see
    notebook 27), which is why no API key is configured anywhere in this
    file.
    """
    result = await ctx.session.create_message(
        messages=[
            SamplingMessage(
                role="user",
                content=TextContent(type="text", text=f"Write a short, two-line poem about {topic}"),
            )
        ],
        max_tokens=100,
    )
    if result.content.type == "text":
        return result.content.text
    return str(result.content)


class TableBookingPreferences(BaseModel):
    """Schema the client renders as a form when the requested date is full."""

    try_alternative: bool = Field(description="Would you like to try a different date?")
    alternative_date: str = Field(default="2025-01-02", description="Alternative date (YYYY-MM-DD)")


@mcp.tool()
async def book_table(date: str, party_size: int, ctx: Context[ServerSession, None]) -> str:
    """Book a table, demonstrating elicitation when the requested date is
    unavailable. See notebook 27 for the client-side half of this exchange.
    """
    if date == "2025-01-01":
        result = await ctx.elicit(
            message=f"No tables for {party_size} on {date}. Try another date?",
            schema=TableBookingPreferences,
        )
        if result.action == "accept" and result.data and result.data.try_alternative:
            return f"Booked for {result.data.alternative_date}"
        return "No booking made"
    return f"Booked for {date}, party of {party_size}"


# --- Resources: readable data, addressed by URI ------------------------------

@mcp.resource("greeting://{name}")
def get_greeting(name: str) -> str:
    """A parameterized (templated) resource -- notebook 26 reads this by URI."""
    return f"Hello, {name}! This text came from an MCP *resource*, not a tool."


@mcp.resource("config://server-info")
def get_server_info() -> str:
    """A fixed (non-templated) resource."""
    return "Foundations Demo Server v1.0 -- see notebooks 24-28."


# --- Prompts: reusable, user-triggered message templates ---------------------

@mcp.prompt()
def greet_user(name: str, style: str = "friendly") -> str:
    """Generate a greeting prompt -- notebook 26 fetches this by name."""
    styles = {
        "friendly": "Please write a warm, friendly greeting",
        "formal": "Please write a formal, professional greeting",
    }
    return f"{styles.get(style, styles['friendly'])} for someone named {name}."


if __name__ == "__main__":
    # Defaults to the stdio transport, matching how src/mcp_client.py
    # launches the Azure MCP Server elsewhere in this course.
    mcp.run()
