# 03 — Installation and Setup

You do **not** need to separately install the Azure MCP Server to use it —
most integrations (including every example in this repo) launch it on demand
via `npx -y @azure/mcp@latest`. Installing it explicitly is only useful for
CI/CD pipelines, headless environments, or when you want a pinned version.
## Package manager installation (optional)

| Package manager | Package | Typical use |
| --- | --- | --- |
| npm | [`@azure/mcp`](https://www.npmjs.com/package/@azure/mcp) | `npx -y @azure/mcp@latest server start` |
| NuGet | [`Azure.Mcp`](https://www.nuget.org/packages/Azure.Mcp) | .NET tool installs / CI |
| PyPI | [`msmcp-azure`](https://pypi.org/project/msmcp-azure/) | Python-first environments |

Package manager installation offers centralized dependency management, CI/CD
integration, support for headless environments, version pinning, and project
portability. See the [Azure MCP Server README](https://github.com/microsoft/mcp/blob/main/servers/Azure.Mcp.Server/README.md#package-manager)
for full details.
