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
## Signing in for local development

Pick whichever tool you already use:

| Tool | Command |
| --- | --- |
| VS Code | Command Palette (`Ctrl+Shift+P`) → **Azure: Sign In** |
| Visual Studio | **File > Account Settings > Add an account** |
| Azure CLI | `az login` |
| Azure PowerShell | `Connect-AzAccount` |
| Azure Developer CLI | `azd auth login` |

After signing in, the Azure MCP Server can authenticate and run operations
based on your permissions — there's no separate "MCP login" step.
## RBAC: what determines what you can do

The Azure MCP Server (and every tool it exposes) uses your Azure user
credentials or managed identity, and access is enforced through Azure
Role-Based Access Control (RBAC). If a tool call fails with an authorization
error, the fix is almost always to grant your account the appropriate role
(e.g., **Storage Blob Data Reader** to list blobs, **Key Vault Secrets User**
to read secrets) rather than anything MCP-specific.

> The local MCP server is intended strictly for developer use within your
> organization. Don't use it for external applications or production
> scenarios outside an approved development environment.
## Global authentication parameters

Every tool call accepts these optional parameters (in addition to its own):

| Parameter | Description |
| --- | --- |
| **Subscription** | Azure subscription ID or name. Defaults to the Azure CLI profile's default subscription, or the `AZURE_SUBSCRIPTION_ID` env var. |
| **Tenant Id** | Microsoft Entra tenant ID or display name. Defaults to your default tenant. |
| **Authentication method** | `credential` (default, Azure CLI/managed identity), `key`, or `connectionString`. |

Example prompts a client might translate into these parameters:

- "Use subscription 'my-subscription-id' for all operations"
- "Authenticate using tenant ID 'my-tenant-id'"
- "Use 'credential' authentication for this session"
## Troubleshooting

- **`DefaultAzureCredential` fails locally** — run `az login` again; make
  sure you selected the right tenant with `az login --tenant <tenant-id>`.
- **Tool returns "not authorized"** — check RBAC role assignments with the
  `role` (Azure RBAC) tool, covered in
  [`notebooks/09_resource_management_tools.ipynb`](../notebooks/09_resource_management_tools.ipynb).
- **Wrong subscription used** — run `az account set --subscription <id>` or
  pass an explicit subscription parameter/prompt.

Next: [05_tools_reference.md](05_tools_reference.md)
