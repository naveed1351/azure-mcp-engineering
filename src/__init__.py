"""
azure_mcp_course
=================

Reusable helper modules for the Azure MCP Server learning notebooks and
examples in this repository. Nothing in this package talks to Azure at
*import* time -- every network/subprocess call happens lazily, inside a
function or an ``async with`` block, so importing ``src`` is always safe.
"""

__version__ = "0.1.0"

import logging

# Library code should never configure logging for the whole application;
# it should only attach a NullHandler so that notebooks/examples/CLIs can
# opt in to logging via `logging.basicConfig(...)` themselves.
logging.getLogger(__name__).addHandler(logging.NullHandler())

__all__ = ["__version__"]
