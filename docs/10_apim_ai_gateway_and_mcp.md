# 10 — Azure API Management as an AI Gateway for MCP

This page is the conceptual companion to notebooks 16-22 (Part 2 of this
course), the same way docs 01-08 pair with notebooks 01-15. It summarizes
"why", with links out to the official Microsoft Learn articles for the full
"how". Portal steps and code live in the notebooks themselves.

## Why put API Management in front of MCP servers and LLM backends?

Notebooks 01-15 ran the Azure MCP Server locally, launched over stdio by
your own machine. That's great for personal development, but it doesn't
answer the enterprise version of the same problem: how do you expose *your
own* tools and APIs as MCP servers, to many different agents and users, with
centralized authentication, rate limiting, and observability — without
every team reinventing that plumbing?

[Azure API Management (APIM)](https://learn.microsoft.com/en-us/azure/api-management/api-management-key-concepts)
already solves this for regular REST APIs. Its **AI gateway** capabilities
([overview](https://learn.microsoft.com/en-us/azure/api-management/genai-gateway-capabilities))
extend the same gateway to two additional traffic shapes:

- **MCP servers** — expose a managed REST API as an MCP server, or proxy an
  existing MCP-compatible server, so any MCP client (GitHub Copilot, Claude,
  ChatGPT, your own agent) can call its tools through one governed endpoint.
- **LLM backends** — front Azure OpenAI/Foundry model deployments with load
  balancing, circuit breakers, token quotas, and semantic caching.

Both are just the existing API gateway wearing a different hat: an MCP
server is an API Management `API` resource with `type: mcp`, and an LLM
backend is a regular API Management `backend` your policies route to.

## Map of notebooks 16-22

| Notebook | Topic |
| --- | --- |
| [16_apim_ai_gateway_fundamentals.ipynb](../notebooks/16_apim_ai_gateway_fundamentals.ipynb) | MCP architecture recap, AI gateway capability summary, service tiers |
| [17_exposing_rest_apis_as_mcp_servers.ipynb](../notebooks/17_exposing_rest_apis_as_mcp_servers.ipynb) | Turn a managed REST API into an MCP server; call it from Python and VS Code |
| [18_securing_mcp_servers_with_entra_id.ipynb](../notebooks/18_securing_mcp_servers_with_entra_id.ipynb) | Inbound (subscription keys, `validate-azure-ad-token`) and outbound (credential manager) security |
| [19_mcp_server_policies_and_governance.ipynb](../notebooks/19_mcp_server_policies_and_governance.ipynb) | Rate limiting, quotas, IP filtering, caching, tracing policies for MCP tools |
| [20_federating_existing_mcp_servers_and_discovery.ipynb](../notebooks/20_federating_existing_mcp_servers_and_discovery.ipynb) | Proxying external MCP servers, managing MCP servers as ARM resources, Azure API Center discovery |
| [21_ai_gateway_llm_backends_and_resiliency.ipynb](../notebooks/21_ai_gateway_llm_backends_and_resiliency.ipynb) | Backends, load balancing, circuit breakers, token limits, semantic caching for LLM traffic |
| [22_end_to_end_agent_over_apim_gateway.ipynb](../notebooks/22_end_to_end_agent_over_apim_gateway.ipynb) | Capstone: one agent, both chat completions and MCP tool calls through the gateway |

## Key building blocks, at a glance

| Concern | Mechanism |
| --- | --- |
| MCP transport | Streamable HTTP at `/mcp` (SSE `/sse` + `/messages` is deprecated) |
| Expose a REST API as MCP | Portal: **APIs > MCP Servers > + Create MCP server > Expose an API as an MCP server** |
| Proxy an existing MCP server | Portal: **... > Expose an existing MCP server** (base URL + transport type) |
| Inbound key auth | `Ocp-Apim-Subscription-Key` header, tied to a product/subscription |
| Inbound token auth | [`validate-azure-ad-token`](https://learn.microsoft.com/en-us/azure/api-management/validate-azure-ad-token-policy) policy |
| Outbound auth to backends | [Credential manager](https://learn.microsoft.com/en-us/azure/api-management/credentials-overview) + `get-authorization-context` |
| Rate limiting | `rate-limit-by-key`, `quota-by-key` |
| Caching | `cache-lookup` / `cache-store` (tools), `azure-openai-semantic-cache-lookup` / `-store` (LLM) |
| Token governance | `azure-openai-token-limit` / `llm-token-limit`, `azure-openai-emit-token-metric` / `llm-emit-token-metric` |
| Resiliency for LLM backends | [Backends](https://learn.microsoft.com/en-us/azure/api-management/backends): load balancer + circuit breaker |
| Programmatic management | ARM API resource `type: mcp`, REST API version `2025-09-01-preview`+ (ARM/Bicep/CLI/Terraform) |
| Discovery | [Azure API Center](https://learn.microsoft.com/en-us/azure/api-center/register-discover-mcp-server) MCP server registration |

## Local Python setup

Notebooks 16-22 reuse the same `.env`-driven configuration pattern as the
rest of the course (`src/config.py`), plus a new remote-transport client:

- `src/apim_mcp_client.py` — `connect_apim_mcp(...)`, an async context
  manager around the MCP SDK's Streamable HTTP client, plus
  `get_entra_bearer_token(...)` for acquiring Microsoft Entra ID tokens with
  `azure-identity`.
- New `.env` variables: `APIM_MCP_SERVER_URL`, `APIM_SUBSCRIPTION_KEY`,
  `APIM_MCP_SCOPE`, `APIM_GATEWAY_ENDPOINT` (see `.env.example`).

> **Version note:** `requirements.txt` pins `mcp<2.0.0`. The MCP Python SDK's
> v2 rewrite renames and reshapes the Streamable HTTP client API these
> notebooks use — install `mcp<2` (as this repo's `requirements.txt`
> already does) if you're following along outside this repo's virtual
> environment.

## Further resources

- [Overview of MCP servers in Azure API Management](https://learn.microsoft.com/en-us/azure/api-management/mcp-server-overview)
- [AI gateway capabilities in Azure API Management](https://learn.microsoft.com/en-us/azure/api-management/genai-gateway-capabilities)
- [Expose REST API as MCP server](https://learn.microsoft.com/en-us/azure/api-management/export-rest-mcp-server)
- [Connect and govern an existing MCP server](https://learn.microsoft.com/en-us/azure/api-management/expose-existing-mcp-server)
- [Secure access to MCP servers](https://learn.microsoft.com/en-us/azure/api-management/secure-mcp-servers)
- [Manage MCP servers programmatically](https://learn.microsoft.com/en-us/azure/api-management/manage-mcp-servers-rest-api)
- [Inventory and discover MCP servers in Azure API Center](https://learn.microsoft.com/en-us/azure/api-center/register-discover-mcp-server)
- [Azure-Samples/AI-Gateway](https://github.com/Azure-Samples/AI-Gateway) — hands-on labs for everything above

This is the last conceptual doc in the series. From here, work through
notebooks 16-22 in order, or jump to whichever topic matches what you're
building.
