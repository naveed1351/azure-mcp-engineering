# 04 — Authentication

Azure MCP Server authenticates to Microsoft Entra ID using the Azure Identity
library, the same way Azure SDKs and the Azure CLI do. It supports two
authentication modes:

- **Broker mode** — uses your operating system's native authentication
  broker (for example, Windows Web Account Manager) via
  `InteractiveBrowserCredential`.
- **Credential chain mode** — tries multiple credential sources in order:
  environment variables, Visual Studio Code, Visual Studio, Azure CLI, Azure
  PowerShell, Azure Developer CLI, and finally interactive browser
  authentication.
