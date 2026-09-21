# 05 — Tools Reference

## `azmcp` server start parameters

| Option | Required? | Description |
| --- | --- | --- |
| **Debug** | Optional | Enable debug mode with verbose logging to `stderr`. Default: `false`. |
| **Enable insecure transports** | Optional | Enable insecure transport. Default: `false`. |
| **Disable user confirmation** | Optional (not recommended) | Skips elicitation before high-risk commands (e.g., returning Key Vault secrets). Only for trusted, automated environments. Default: `false`. |
| **Mode** | Optional | `namespace` (default), `consolidated`, `all`, or `single`. See [07_server_modes_and_advanced_config.md](07_server_modes_and_advanced_config.md). |
| **Namespace** | Optional | Which Azure service namespaces to expose (e.g. `storage`, `keyvault`, `cosmos`). Default: all namespaces. |
| **Read only** | Optional | If `true`, no write operations are allowed. Default: `false`. |
| **Tool** | Optional | Expose specific tools by name (e.g. `azmcp_storage_account_get`); switches to `all` mode automatically. |
| **Transport** | Optional | Transport mechanism. Default: `stdio`. |
## Global tool parameters

Beyond subscription/tenant/auth method (see
[04_authentication.md](04_authentication.md)), every tool also accepts retry
and diagnostics parameters:

| Parameter | Description | Default |
| --- | --- | --- |
| **Maximum retries** | Retry attempts before giving up | 3 |
| **Retry delay** | Initial delay (seconds) between retries | 2 |
| **Retry delay maximum** | Cap on delay between retries | 10 |
| **Retry mode** | `fixed` or `exponential` backoff | `exponential` |
| **Retry network timeout** | Per-operation timeout (seconds) | 100 |
| **Learn mode** | Discover commands/parameters without executing them | disabled |

These map naturally onto conversational prompts, e.g. "Set maximum retries to
5 with a 3-second delay" or "Use learn mode to discover available parameters
for this tool".
## Tool annotations

[Tool annotations](https://modelcontextprotocol.io/specification/2025-06-18/schema#toolannotations)
are metadata hints describing a tool's behavior:

| Annotation | Meaning |
| --- | --- |
| **Destructive** | Can delete or modify existing resources if `true`. |
| **Idempotent** | Repeated calls with the same arguments have no additional side effects. |
| **Open world** | Interacts with an unpredictable/dynamic set of entities (e.g. web search) vs. a closed, well-defined domain. |
| **Read only** | Performs only read operations; never changes state. |
| **Secret** | Response may contain sensitive data (secrets, keys) that should be sanitized before logging or forwarding to an LLM. |
| **Local required** | Only available when the server runs locally over stdio, not in remote server modes. |

You'll inspect these programmatically in
[`notebooks/14_security_elicitation_rbac.ipynb`](../notebooks/14_security_elicitation_rbac.ipynb).
