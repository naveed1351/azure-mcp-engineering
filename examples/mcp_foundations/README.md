# MCP Protocol Foundations: Runnable Scripts

Companion code for notebooks 24-28 (Part 3 of this course: understanding
and building the Model Context Protocol itself, independent of Azure).
Neither script needs an Azure subscription, `az login`, or Node.js.

| Script | What it shows |
| --- | --- |
| [custom_server.py](custom_server.py) | A minimal MCP server built from scratch with the official SDK's `FastMCP` API: a tool, a sampling-using tool, an elicitation-using tool, two resources (one templated), and a prompt. |
| [raw_jsonrpc_client.py](raw_jsonrpc_client.py) | A hand-rolled client using only the standard library (`json` + `subprocess`) that speaks raw newline-delimited JSON-RPC to `custom_server.py` -- no `mcp` SDK involved. Used by notebook 24 to show exactly what bytes cross the wire. |

## Running them

```powershell
# Smoke-test the server directly (it waits on stdio; Ctrl+C to exit)
python examples/mcp_foundations/custom_server.py

# See the raw JSON-RPC initialize / tools/list / tools/call exchange
python examples/mcp_foundations/raw_jsonrpc_client.py
```

Notebooks 25-27 instead connect to `custom_server.py` with the real MCP
Python SDK (`ClientSession` + `stdio_client`), the same pattern
`src/mcp_client.py` uses to launch the Azure MCP Server elsewhere in this
course -- just pointed at `python custom_server.py` instead of
`npx @azure/mcp@latest`.
