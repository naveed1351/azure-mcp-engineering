"""
azure_mcp_course
=================

Reusable helper modules for the Azure MCP Server learning notebooks and
examples in this repository. Nothing in this package talks to Azure at
*import* time -- every network/subprocess call happens lazily, inside a
function or an ``async with`` block, so importing ``src`` is always safe.
"""

__version__ = "0.1.0"
