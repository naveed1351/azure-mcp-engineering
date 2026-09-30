# Azure API Management Policy Recipes: Plain APIM vs AI Gateway

This folder is a hands-on companion to
[docs/11_apim_vs_ai_gateway_decision_guide.md](../../docs/11_apim_vs_ai_gateway_decision_guide.md)
and notebook
[23_choosing_apim_vs_ai_gateway.ipynb](../../notebooks/23_choosing_apim_vs_ai_gateway.ipynb).
Each file is a small, self-contained policy (or backend/Bicep) recipe you
can paste into the Azure portal's policy editor (or an IaC template) with
minimal edits. Every file starts with a comment block explaining the
scenario, when to reach for it, its prerequisites, and -- where relevant --
the decision point between plain API Management and AI Gateway.

## `plain/` — ordinary API Management, no AI awareness

These policies work identically whether the backend is a database-backed
REST API, an MCP server's tools, or anything else. If everything you need
is in this list, you don't need any AI Gateway-specific feature.

| File | Policy | What it does |
| --- | --- | --- |
| [01_rate_limit_by_key.xml](plain/01_rate_limit_by_key.xml) | `rate-limit-by-key` | Limit calls per time window, by a custom key |
| [02_rate_limit_by_subscription.xml](plain/02_rate_limit_by_subscription.xml) | `rate-limit` | Limit calls per time window, by subscription |
| [03_quota_by_key.xml](plain/03_quota_by_key.xml) | `quota-by-key` | Longer-window call/bandwidth budget, by a custom key |
| [04_quota_by_subscription.xml](plain/04_quota_by_subscription.xml) | `quota` | Longer-window call/bandwidth budget, by subscription |
| [05_limit_concurrency.xml](plain/05_limit_concurrency.xml) | `limit-concurrency` | Cap simultaneous in-flight requests |
| [06_cache_lookup_and_store.xml](plain/06_cache_lookup_and_store.xml) | `cache-lookup` / `cache-store` | Exact-match HTTP response caching |
| [07_ip_filter.xml](plain/07_ip_filter.xml) | `ip-filter` | Allow/deny by client IP address range |
| [08_validate_jwt.xml](plain/08_validate_jwt.xml) | `validate-jwt` | Validate a JWT from any OpenID Connect provider |
| [09_validate_azure_ad_token.xml](plain/09_validate_azure_ad_token.xml) | `validate-azure-ad-token` | Validate a Microsoft Entra ID token |
| [10_validate_client_certificate.xml](plain/10_validate_client_certificate.xml) | `validate-client-certificate` | Require an mTLS client certificate |
| [11_authentication_managed_identity_backend.xml](plain/11_authentication_managed_identity_backend.xml) | `authentication-managed-identity` | Authenticate to the backend with APIM's own identity |
| [12_retry_backend_call.xml](plain/12_retry_backend_call.xml) | `retry` | Retry a transient backend failure |
| [13_trace_and_emit_metric.xml](plain/13_trace_and_emit_metric.xml) | `trace` / `emit-metric` | Generic custom tracing and metrics |

## `ai_gateway/` — AI Gateway capabilities for LLM and MCP traffic

These policies (and backend resources) are specific to, or specially
designed for, LLM/MCP workloads -- token-aware limits instead of call
counts, semantic caching instead of exact-match caching, content-safety
screening, and backend resiliency tuned for model deployments.

| File | Policy / resource | What it does |
| --- | --- | --- |
| [01_llm_token_limit.xml](ai_gateway/01_llm_token_limit.xml) | `llm-token-limit` | Token-aware rate/quota limiting, any supported LLM provider |
| [02_azure_openai_token_limit.xml](ai_gateway/02_azure_openai_token_limit.xml) | `azure-openai-token-limit` | Same, Azure OpenAI-specific policy name |
| [03_llm_token_limit_by_product.xml](ai_gateway/03_llm_token_limit_by_product.xml) | `llm-token-limit` | Token budget scoped to a product/tier |
| [04_llm_emit_token_metric.xml](ai_gateway/04_llm_emit_token_metric.xml) | `llm-emit-token-metric` | Per-consumer token usage metrics, any provider |
| [05_azure_openai_emit_token_metric.xml](ai_gateway/05_azure_openai_emit_token_metric.xml) | `azure-openai-emit-token-metric` | Same, Azure OpenAI-specific policy name |
| [06_llm_semantic_cache_lookup_and_store.xml](ai_gateway/06_llm_semantic_cache_lookup_and_store.xml) | `llm-semantic-cache-lookup` / `-store` | Similarity-based response caching, any provider |
| [07_azure_openai_semantic_cache_lookup_and_store.xml](ai_gateway/07_azure_openai_semantic_cache_lookup_and_store.xml) | `azure-openai-semantic-cache-lookup` / `-store` | Same, Azure OpenAI-specific policy names |
| [08_semantic_cache_embeddings_backend.bicep](ai_gateway/08_semantic_cache_embeddings_backend.bicep) | `backends` (Bicep) | The embeddings backend semantic caching depends on |
| [09_llm_content_safety.xml](ai_gateway/09_llm_content_safety.xml) | `llm-content-safety` | Screen prompts/completions with Azure AI Content Safety |
| [10_content_safety_plus_token_limit_pipeline.xml](ai_gateway/10_content_safety_plus_token_limit_pipeline.xml) | combined | Safety → token limit → metrics, a realistic pipeline |
| [11_backend_load_balancing_round_robin.bicep](ai_gateway/11_backend_load_balancing_round_robin.bicep) | `backends` pool (Bicep) | Even traffic split across equivalent deployments |
| [12_backend_load_balancing_weighted.bicep](ai_gateway/12_backend_load_balancing_weighted.bicep) | `backends` pool (Bicep) | Weighted traffic split (for example, 80/20 canary) |
| [13_backend_load_balancing_priority_ptu.bicep](ai_gateway/13_backend_load_balancing_priority_ptu.bicep) | `backends` pool (Bicep) | Prefer a PTU deployment, fall back to pay-as-you-go |
| [14_backend_load_balancing_session_aware.bicep](ai_gateway/14_backend_load_balancing_session_aware.bicep) | `backends` pool (Bicep) | Sticky-session routing for stateful model backends |
| [15_backend_circuit_breaker_llm.bicep](ai_gateway/15_backend_circuit_breaker_llm.bicep) | `backends` circuit breaker (Bicep) | Stop calling an unhealthy LLM deployment automatically |
| [16_mcp_server_rate_limit_and_trace.xml](ai_gateway/16_mcp_server_rate_limit_and_trace.xml) | `rate-limit-by-key` / `trace` | Governance for MCP tool calls (reuses plain policies) |
| [17_combined_mcp_and_llm_gateway.xml](ai_gateway/17_combined_mcp_and_llm_gateway.xml) | (illustrative) | One APIM instance fronting both an MCP server and an LLM API |

## Validating a recipe

Run [validate_policies.py](validate_policies.py) to check that every
`.xml` file in this folder is well-formed before you paste it into the
portal's policy editor:

```powershell
python examples/apim_policies/validate_policies.py
```
