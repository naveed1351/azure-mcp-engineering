# 02 — Azure MCP Server Overview

The Azure MCP Server is Microsoft's MCP server implementation for Azure. It
enables AI agents and MCP clients to interact with Azure resources using
natural language, by exposing Azure operations as MCP tools.
## Key features

- **MCP support** — implements the Model Context Protocol, so it works with
  any compliant client: GitHub Copilot agent mode, the OpenAI Agents SDK,
  Semantic Kernel, and custom clients like the ones in this repo.
- **Entra ID authentication** — authenticates via the Azure Identity library,
  following Azure authentication best practices (see
  [04_authentication.md](04_authentication.md)).
- **Service and tool integration** — supports the Azure CLI, Azure Developer
  CLI (azd), and a broad set of Azure resources (storage, databases,
  Kubernetes, monitoring, and more).
- **Azure Skills Plugin** — the [Azure Skills Plugin](https://github.com/microsoft/azure-skills)
  packages 26+ reusable Azure skills (`azure-prepare`, `azure-validate`,
  `azure-deploy`, `azure-diagnostics`, `azure-cost`, ...) that layer
  structured workflows and guardrails on top of the raw MCP tools.
## Prerequisites

Azure MCP Server tools are **disabled by default** in supported hosts. To use
them you need:

- A GitHub Copilot subscription (if using a Copilot-based host)
- An Azure account with appropriate subscription permissions (RBAC)

Tool *availability* reflects your Azure subscription permissions — the
server won't show you tools/data you don't have RBAC access to. Once you
enable the tools in a host, they stay enabled across sessions.
