# 12 — MCP Protocol Foundations

This page is the conceptual companion to notebooks 24-28 (Part 3 of this
course). Parts 1 and 2 taught you to *use* MCP through Azure-specific
lenses — the Azure MCP Server and Azure API Management's AI gateway. This
page, and the notebooks it pairs with, step back to the protocol itself:
no Azure subscription, `az login`, or Node.js required for any of it.

## Why a third part, and why now

By the end of Part 2 you can consume and govern MCP servers fluently, but
nothing in Parts 1-2 required you to know what an MCP server actually *is*
under the hood, or what the Azure MCP Server (or an API Management-exposed
server) chooses not to expose and why. Part 3 fills that gap using the
[official MCP specification](https://modelcontextprotocol.io/specification/2025-06-18)
and the [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk)
directly.

## Map of notebooks 24-28

| Notebook | Topic |
| --- | --- |
| [24_mcp_lifecycle_and_jsonrpc.ipynb](../notebooks/24_mcp_lifecycle_and_jsonrpc.ipynb) | JSON-RPC 2.0 message shapes, the initialize/initialized handshake, version negotiation, error codes |
| [25_building_a_custom_mcp_server.ipynb](../notebooks/25_building_a_custom_mcp_server.ipynb) | Build a minimal MCP server from scratch with `FastMCP`; connect with the real SDK client |
| [26_mcp_resources_and_prompts.ipynb](../notebooks/26_mcp_resources_and_prompts.ipynb) | The two primitives the Azure MCP Server barely uses: resources and prompts |
| [27_mcp_sampling_and_roots.ipynb](../notebooks/27_mcp_sampling_and_roots.ipynb) | Server-initiated LLM sampling and client-exposed filesystem roots |
| [28_mcp_transports_and_capability_recap.ipynb](../notebooks/28_mcp_transports_and_capability_recap.ipynb) | stdio vs. Streamable HTTP, and a capability-negotiation recap across the whole course |

## The five primitives, at a glance

| Primitive | Direction | Who decides to use it | Covered |
| --- | --- | --- | --- |
| Tool | Client → Server | The model (function calling) | Parts 1-2 (everything), notebook 25 |
| Resource | Client → Server | The host application | Notebook 26 |
| Prompt | Client → Server | The user, explicitly | Notebook 26 |
| Sampling | Server → Client | The server, with mandatory human-in-the-loop review | Notebook 27 |
| Roots | Server → Client | The server asks; the client answers within its own boundaries | Notebook 27 |

Elicitation (a server requesting structured input mid-tool-call) is a
sixth primitive, already covered conceptually in
[08_security_and_best_practices.md](08_security_and_best_practices.md);
`examples/mcp_foundations/custom_server.py`'s `book_table` tool implements
it so you can see the server-side code for real.

## Runnable artifacts

[examples/mcp_foundations/](../examples/mcp_foundations/README.md) holds
two scripts with no Azure dependency:

- `custom_server.py` — a complete `FastMCP` server exposing a tool, a
  sampling-using tool, an elicitation-using tool, two resources (one
  templated), and a prompt.
- `raw_jsonrpc_client.py` — a hand-rolled client using only `json` and
  `subprocess`, showing the exact newline-delimited JSON-RPC bytes a real
  MCP handshake produces, with no SDK involved.

## Why this matters even if you only ever use the Azure MCP Server

- You can read *any* MCP server's source and immediately know which
  primitives it implements and why.
- You can tell the difference between "this platform doesn't expose
  resources" (a deliberate design choice, like the Azure MCP Server) and
  "this gateway doesn't support resources yet" (a platform limitation, like
  API Management's REST-API-backed MCP servers in notebook 17).
- You can prototype or wrap an internal tool as an MCP server in minutes
  (notebook 25) long before it's worth standing up Azure API Management in
  front of it (notebook 17).

## Further resources

- [Model Context Protocol specification](https://modelcontextprotocol.io/specification/2025-06-18)
- [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk) —
  `docs/server.md`, `docs/client.md`, `docs/protocol.md`
- [docs/01_what_is_mcp.md](01_what_is_mcp.md) — the original, Azure-framed
  introduction this page extends

This is the last conceptual doc in the series so far. Work through
notebooks 24-28 in order if you're new to the protocol; jump directly to
whichever one matches what you're building otherwise.
