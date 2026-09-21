# 01 — What Is the Model Context Protocol (MCP)?

The [Model Context Protocol (MCP)](https://modelcontextprotocol.io/) is an
open protocol that standardizes how AI applications (hosts) give language
models access to external tools, data, and context in a safe, structured,
and stateful way. Before MCP, every AI app that wanted to call a "tool" (say,
list Azure storage accounts) had to hand-roll its own integration. MCP gives
that integration a common shape so any MCP-compatible client can talk to any
MCP-compatible server.
