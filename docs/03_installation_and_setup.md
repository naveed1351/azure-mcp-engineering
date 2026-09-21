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
## Docker

For easy deployment and isolation you can run the Azure MCP server as a
Docker container instead of via `npx`/`dotnet`/`pip`. See
[Run Azure MCP Server in Docker](https://github.com/microsoft/mcp/blob/main/servers/Azure.Mcp.Server/README.md#docker)
for the exact image and flags.
## IDE quick links

- [Visual Studio Code](https://learn.microsoft.com/en-us/azure/developer/azure-mcp-server/get-started/tools/visual-studio-code)
- [Visual Studio](https://learn.microsoft.com/en-us/azure/developer/azure-mcp-server/get-started/tools/visual-studio) — bundled with the Azure workload in 17.14.30+, no extra extension needed.
- [Cursor](https://learn.microsoft.com/en-us/azure/developer/azure-mcp-server/get-started/tools/cursor)
- [Windsurf](https://learn.microsoft.com/en-us/azure/developer/azure-mcp-server/get-started/tools/windsurf)
- [Cline](https://learn.microsoft.com/en-us/azure/developer/azure-mcp-server/get-started/tools/cline)
- [IntelliJ](https://learn.microsoft.com/en-us/azure/developer/azure-mcp-server/get-started/tools/jet-brains)
- [Eclipse](https://learn.microsoft.com/en-us/azure/developer/azure-mcp-server/get-started/tools/eclipse)

This repo doesn't require any of these — it talks to the server directly
from Python — but they're the fastest way to try the tools conversationally
before writing code.
