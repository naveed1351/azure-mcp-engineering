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
