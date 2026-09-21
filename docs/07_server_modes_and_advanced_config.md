# 07 — Server Modes and Advanced Configuration

The `azmcp` server supports several **modes** that control how many tools it
exposes and how they're grouped, set via the `Mode` start parameter:

| Mode | Behavior |
| --- | --- |
| `namespace` (default) | Groups tools under one entry point per namespace (e.g. one `storage` tool that dispatches sub-commands). Keeps the tool list small, which is friendlier to models with limited context or tool-count limits. |
| `consolidated` | Merges tools more aggressively across namespaces into fewer, broader entry points. |
| `all` | Exposes every individual tool (e.g. `azmcp_storage_account_get`) as its own top-level MCP tool. Most granular, largest tool list. |
| `single` | Exposes exactly one tool, selected via the `Tool` parameter. Useful for the most constrained or specialized integrations. |
## Scoping by namespace

Rather than changing modes, you can restrict *which* namespaces are loaded at
all using the `Namespace` parameter, e.g. only `storage` and `keyvault`. This
is the fastest way to keep a tool list small and predictable for a
special-purpose agent (for example, a "storage housekeeping bot" that should
never see SQL or Cosmos DB tools).

```python
from mcp import StdioServerParameters

server_params = StdioServerParameters(
    command="npx",
    args=["-y", "@azure/mcp@latest", "server", "start",
          "--namespace", "storage", "--namespace", "keyvault"],
)
```
