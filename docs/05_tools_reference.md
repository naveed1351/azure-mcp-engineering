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
