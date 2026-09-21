# 01 — What Is the Model Context Protocol (MCP)?

The [Model Context Protocol (MCP)](https://modelcontextprotocol.io/) is an
open protocol that standardizes how AI applications (hosts) give language
models access to external tools, data, and context in a safe, structured,
and stateful way. Before MCP, every AI app that wanted to call a "tool" (say,
list Azure storage accounts) had to hand-roll its own integration. MCP gives
that integration a common shape so any MCP-compatible client can talk to any
MCP-compatible server.
## The three roles

MCP defines a client-server architecture with three components:

- **Host** — the application the user interacts with (for example, Visual
  Studio Code, or a custom Python app you write). The host embeds one or more
  MCP clients.
- **Client** — a component, owned by the host, that manages a single
  connection to one MCP server: it negotiates capabilities, requests the list
  of tools, and forwards tool-call requests/results.
- **Server** — a program that exposes *tools* (actions), *resources* (data),
  and *prompts* (reusable instructions) over the protocol. The Azure MCP
  Server is one such server — it exposes tools for interacting with Azure.

```text
+------------------------ Host (e.g. VS Code, your Python app) ------------------------+
|                                                                                       |
|   +------------------+        JSON-RPC over stdio/HTTP        +------------------+   |
|   |   MCP Client      | <-------------------------------------> |   MCP Server    |   |
|   | (session/transport)|                                        | (Azure MCP Server)|  |
|   +------------------+                                          +------------------+   |
|            ^                                                                            |
|            | tool schemas / tool-call results                                           |
|            v                                                                            |
|   +------------------+                                                                  |
|   |  LLM (e.g. GPT-4o)|  <-- decides which tool to call based on the user's prompt       |
|   +------------------+                                                                  |
+---------------------------------------------------------------------------------------+
```
## Lifecycle of a tool call

1. The client connects to the server (over stdio, HTTP, or another
   transport) and calls `initialize()` to negotiate protocol version and
   capabilities.
2. The client calls `list_tools()`. The server responds with each tool's
   name, description, and JSON Schema for its input parameters.
3. The host passes those tool definitions to the LLM alongside the user's
   prompt (for example, using OpenAI's `tools=` parameter for function
   calling).
4. If the model decides a tool is needed, it returns a *tool call* (a tool
   name plus JSON arguments) instead of, or alongside, plain text.
5. The client calls `call_tool(name, arguments)` on the MCP server, which
   performs the real work (e.g., an Azure Resource Manager call) and returns
   a result.
6. The result is appended back into the conversation, and the LLM produces
   a final natural-language answer.

This request/response loop is exactly what you'll implement by hand in
[`notebooks/06_azure_openai_function_calling.ipynb`](../notebooks/06_azure_openai_function_calling.ipynb).
## Why MCP for Azure?

Without MCP, building an "Azure copilot" means writing bespoke code for every
Azure SDK you want to expose to an LLM, plus your own auth, retry, and
error-handling layer for each one. The Azure MCP Server does that work once,
exposing a consistent set of tools (see
[docs/06_available_tools_catalog.md](06_available_tools_catalog.md)) that any
MCP client — GitHub Copilot agent mode, the OpenAI Agents SDK, Semantic
Kernel, or your own Python script — can call the same way.

Because the protocol is transport-agnostic and language-agnostic, the same
server can be driven from VS Code's chat UI *and* from a headless Python
automation script, which is exactly what this repository demonstrates.
## Further reading

- [Model Context Protocol specification](https://modelcontextprotocol.io/)
- [What Is the Azure MCP Server? (Microsoft Learn)](https://learn.microsoft.com/en-us/azure/developer/azure-mcp-server/overview)
- Next: [02_azure_mcp_server_overview.md](02_azure_mcp_server_overview.md)
