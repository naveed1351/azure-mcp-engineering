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
## Read-only mode

Setting `Read only=true` blocks every tool that would create, modify, or
delete a resource, regardless of namespace. This is the single most
important safety switch for any agent you don't fully trust yet — turn it on
while you're still testing prompts, and only relax it once you understand
exactly which destructive tools a workflow needs.

```python
args=["-y", "@azure/mcp@latest", "server", "start", "--read-only"]
```
## Exposing a single tool

For the tightest possible integration surface, use `Mode=single` with
`Tool=<tool-name>` to expose exactly one operation, e.g.
`azmcp_storage_account_get`. This is useful when embedding Azure MCP Server
capability inside another, narrowly scoped automation and you want to
guarantee the model can't accidentally call anything else.
## Retry, timeout, and learn mode configuration

Retry behavior (`Maximum retries`, `Retry delay`, `Retry delay maximum`,
`Retry mode`, `Retry network timeout`) and `Learn mode` are per-call
parameters rather than server start flags — they can be set conversationally
("Use exponential retry mode with a maximum of 4 retries and a 2-second
delay") or programmatically as tool arguments. `Learn mode` is particularly
useful during development: it makes a tool return its own command/parameter
metadata instead of performing the real operation, so you can explore an
unfamiliar namespace with zero risk. See
[`notebooks/12_server_modes_namespaces.ipynb`](../notebooks/12_server_modes_namespaces.ipynb)
and [`notebooks/13_error_handling_and_retries.ipynb`](../notebooks/13_error_handling_and_retries.ipynb).

Next: [08_security_and_best_practices.md](08_security_and_best_practices.md)
