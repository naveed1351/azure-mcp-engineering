# Changelog

Notable changes to this learning repository. This project doesn't ship
versioned releases; entries are grouped by topic instead of a version
number.

## Example gallery expansion

- Added 44 new standalone demo scripts (`examples/11_*` through
  `examples/54_*`), one per additional Azure MCP Server namespace not
  already covered by the original 10 tutorial scripts -- including
  `appconfig`, `acr`, `aks`, `appservice`, `compute`, `sql`, `mysql`,
  `postgres`, `redis`, `servicebus`, `eventgrid`, `eventhubs`, `iothub`,
  `role` (RBAC), `pricing`, `search`, `speech`, `cloudarchitect`, and more.
- Added [docs/09_example_gallery.md](docs/09_example_gallery.md), an index
  mapping every example script to its namespace and the specific
  `azmcp_*` tool it calls.
- Cross-linked the new gallery from the README, the tools catalog
  ([docs/06_available_tools_catalog.md](docs/06_available_tools_catalog.md)),
  and the closing section of
  [docs/08_security_and_best_practices.md](docs/08_security_and_best_practices.md).
- All new scripts default to `read_only=True` and call only non-destructive
  `get`/`list` tools, so they're safe to run repeatedly against a real
  Azure subscription.

## Part 2: Azure API Management AI gateway and MCP

- Added 7 new notebooks (`notebooks/16_*` through `notebooks/22_*`) covering
  Azure API Management's AI gateway: exposing REST APIs and existing
  servers as MCP servers, securing them with Microsoft Entra ID and
  credential manager, governance policies (rate limiting, caching,
  tracing), federation and discovery via Azure API Center, and resiliency/
  token-governance policies for LLM backends, ending in a capstone agent
  that calls both a chat model and MCP tools through the gateway.
- Added `src/apim_mcp_client.py`, a Streamable HTTP MCP client helper for
  connecting to Azure API Management-hosted MCP servers, plus matching
  `APIM_*` settings in `src/config.py` and `.env.example`.
- Pinned `mcp<2.0.0` in `requirements.txt`: the MCP Python SDK's v2 rewrite
  changes the Streamable HTTP client API these notebooks depend on.
- Added [docs/10_apim_ai_gateway_and_mcp.md](docs/10_apim_ai_gateway_and_mcp.md),
  the conceptual companion to notebooks 16-22, and linked it from the
  README's learning path table.

## APIM vs AI Gateway decision guide

- Added notebook `23_choosing_apim_vs_ai_gateway.ipynb`: a decision table,
  a five-question decision tree, a runnable `recommend_policies(...)`
  helper, and two worked examples for deciding when a scenario needs
  AI Gateway-specific policies versus plain API Management policies.
- Added `examples/apim_policies/`, 30 ready-to-adapt policy/backend
  recipes split into `plain/` (13 recipes: rate limiting, quotas,
  concurrency, caching, IP filtering, JWT/Entra ID/certificate auth,
  managed-identity backend auth, retries, tracing) and `ai_gateway/`
  (17 recipes: `llm-token-limit`, `llm-emit-token-metric`,
  `llm-semantic-cache-lookup`/`-store` and their `azure-openai-*`
  equivalents, `llm-content-safety`, backend load-balancing/circuit-breaker
  Bicep snippets, and combined MCP + LLM governance pipelines), plus a
  `validate_policies.py` XML well-formedness checker and a README index.
- Added [docs/11_apim_vs_ai_gateway_decision_guide.md](docs/11_apim_vs_ai_gateway_decision_guide.md),
  the conceptual companion to notebook 23, cross-linked from the README,
  docs/06, docs/09, and docs/10.

## Part 3: MCP protocol foundations

- Added 5 new notebooks (`notebooks/24_*` through `notebooks/28_*`), the
  first part of this course with **no Azure dependency** at all: JSON-RPC
  2.0 message anatomy and the connection lifecycle, building a minimal MCP
  server from scratch with the official SDK's `FastMCP` API, the
  resources and prompts primitives the Azure MCP Server doesn't use,
  server-initiated sampling and client-exposed roots, and a transports/
  capability-negotiation recap tying Parts 1-3 together.
- Added `examples/mcp_foundations/`: `custom_server.py` (a complete
  `FastMCP` server exposing a tool, a sampling-using tool, an
  elicitation-using tool, two resources, and a prompt) and
  `raw_jsonrpc_client.py` (a hand-rolled, SDK-free client showing the exact
  newline-delimited JSON-RPC bytes an MCP handshake produces), plus a
  README index. Both scripts were run and verified end to end while
  authoring these notebooks.
- Added [docs/12_mcp_protocol_foundations.md](docs/12_mcp_protocol_foundations.md),
  the conceptual companion to notebooks 24-28, and linked it from the
  README's learning path table, structure, and resources.

