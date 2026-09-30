# 11 — APIM vs AI Gateway: A Decision Guide

This page is the conceptual companion to
[notebook 23](../notebooks/23_choosing_apim_vs_ai_gateway.ipynb) and the
recipe folder [examples/apim_policies/](../examples/apim_policies/README.md).
It exists to answer one recurring question directly: **when do you need an
AI Gateway policy, and when is a plain Azure API Management policy
enough?**

## AI Gateway is a policy category, not a separate product

Every Azure API Management instance already runs an API gateway. **AI
Gateway** is Microsoft's name for one category of policies in that same
gateway — [listed right alongside `rate-limit` and `cache-lookup` in the
official policy reference](https://learn.microsoft.com/en-us/azure/api-management/api-management-policies#ai-gateway):

- `llm-token-limit` / `azure-openai-token-limit`
- `llm-emit-token-metric` / `azure-openai-emit-token-metric`
- `llm-semantic-cache-lookup` / `-store` (and the `azure-openai-*` equivalents)
- `llm-content-safety`

There's no separate resource to provision and no toggle to flip. You add
these policies to a specific API (or MCP server) exactly the way you'd add
`rate-limit-by-key` — because you decided that API's traffic needs
token-aware, semantics-aware, or harm-aware governance, not because the
project is "an AI project."

## The decision, in one table

| Governs by... | Plain API Management | AI Gateway |
| --- | --- | --- |
| Request volume | `rate-limit-by-key`, `quota-by-key` | — |
| LLM token volume | — | `llm-token-limit` / `azure-openai-token-limit` |
| Exact-match responses | `cache-lookup` / `cache-store` | — |
| Semantically similar prompts | — | `llm-semantic-cache-lookup` / `-store` |
| Generic usage metrics | `emit-metric` | `llm-emit-token-metric` / `azure-openai-emit-token-metric` |
| Harmful prompt/response content | — | `llm-content-safety` |
| Caller identity | `validate-azure-ad-token`, `validate-jwt` | *(identical — not AI-specific)* |
| Backend health/load | Backends, load balancer, circuit breaker | *(same mechanism; especially valuable for LLM backends — notebook 21)* |

The last two rows matter: authentication and backend resiliency aren't
split into "plain" and "AI" versions. They're the same policies whether the
backend is a REST API, an MCP server's tools, or an LLM.

## A five-question decision tree

1. **Does the backend consume or produce natural-language tokens?**
   (chat/completions, embeddings, or an MCP tool whose result feeds an
   LLM) — if no, stop: plain API Management policies are enough.
2. **Do you need per-caller cost/quota control finer than "N calls"?** →
   token-limit policies.
3. **Do near-duplicate prompts recur often enough that caching by meaning
   would help?** → semantic-cache policies.
4. **Could a prompt or response contain content you must block?** →
   `llm-content-safety`.
5. **Do you have (or want) more than one model deployment?** → a backend
   pool with load balancing and a circuit breaker.

Notebook 23 turns this into a runnable Python helper
(`recommend_policies(...)`) and works through two full worked examples.

## Prerequisites you take on by choosing AI Gateway policies

AI Gateway policies aren't free to enable:

| Policy | Extra prerequisite |
| --- | --- |
| `llm-semantic-cache-lookup` / `-store` | An embeddings deployment registered as a backend, plus an external cache |
| `llm-content-safety` | An Azure AI Content Safety resource, with API Management's managed identity granted the Cognitive Services User role |
| `llm-token-limit`, `llm-emit-token-metric`, `llm-semantic-cache-store` | **Not available on the Consumption tier** — check the tier columns on each policy reference page |

Weigh these against the governance gap you're actually trying to close.
Adding infrastructure for a capability you don't need yet is its own kind
of complexity cost.

## Recipes to try

All policy/backend snippets referenced above live in
[examples/apim_policies/](../examples/apim_policies/README.md), split into
`plain/` (13 recipes) and `ai_gateway/` (17 recipes), each with a comment
block explaining its scenario and decision rationale. Validate any edits
with:

```powershell
python examples/apim_policies/validate_policies.py
```

## Further resources

- [Azure API Management policy reference — AI gateway category](https://learn.microsoft.com/en-us/azure/api-management/api-management-policies#ai-gateway)
- [AI gateway capabilities in Azure API Management](https://learn.microsoft.com/en-us/azure/api-management/genai-gateway-capabilities)
- [docs/10_apim_ai_gateway_and_mcp.md](10_apim_ai_gateway_and_mcp.md) — how to expose, secure, and govern MCP servers and LLM backends through the gateway
- [Azure-Samples/AI-Gateway](https://github.com/Azure-Samples/AI-Gateway) — hands-on labs for both plain and AI Gateway policies

This is the last conceptual doc in the series. Pair it with notebook 23 and
the recipes folder for the hands-on side.
