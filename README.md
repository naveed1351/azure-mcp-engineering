# Azure MCP Server — A Learning Repository

> 📚 **This repository is for learning purposes only.** It is a hands-on,
> self-paced course that teaches the [Azure MCP Server](https://learn.microsoft.com/azure/developer/azure-mcp-server/overview)
> from first principles (what the Model Context Protocol is) up through
> advanced, multi-tool agent workflows. It is not an official Microsoft
> product and is not intended for production use.

The Azure MCP Server lets AI agents and MCP-compatible clients interact with
Azure resources using natural language, by implementing the open
[Model Context Protocol (MCP)](https://modelcontextprotocol.io/). This repo
walks through that story step by step using runnable Python scripts and
Jupyter notebooks.
## What you will learn

- The fundamentals of the Model Context Protocol: hosts, clients, servers, and tools.
- What the Azure MCP Server is, why it exists, and how it authenticates with Entra ID.
- How to install and run the Azure MCP Server locally (npm, NuGet, PyPI, Docker).
- How to write a Python MCP client that connects to the server over stdio.
- How to list, inspect, and call Azure MCP Server tools directly.
- How to wire the server into an Azure OpenAI function-calling loop to build a
  natural-language Azure agent.
- How to work with tools across Storage, Key Vault, Cosmos DB, SQL/MySQL/Postgres,
  Monitor/Kusto, App Service, AKS, DevOps/deployment, and identity/RBAC namespaces.
- Server modes (`namespace`, `consolidated`, `all`, `single`), read-only mode,
  retries/timeouts, and "learn mode" tool discovery.
- Security concepts: RBAC, elicitation (user confirmation for secrets), and tool
  annotations (destructive / idempotent / read-only / secret / local-required).
- Advanced patterns: multi-server MCP clients and composing custom workflows.

### Prerequisites

- An [Azure account](https://azure.microsoft.com/pricing/purchase-options/azure-account) with an active subscription (only needed to actually *run* the examples against real Azure resources; you can read the notebooks without one).
- [Python 3.9+](https://www.python.org/downloads/)
- [Node.js LTS](https://nodejs.org/) (used to launch the Azure MCP Server via `npx @azure/mcp@latest`)
- The [Azure CLI](https://learn.microsoft.com/cli/azure/install-azure-cli) for `az login`
- An Azure OpenAI resource (only needed for the function-calling notebooks)
## Repository structure

```text
azure-mcp-engineering/
├── docs/                Conceptual reference notes, mirroring Microsoft Learn
├── notebooks/           15 Jupyter notebooks, fundamentals -> advanced
├── src/                 Reusable Python helper modules imported by the notebooks/examples
├── examples/            Small, focused standalone scripts (run with `python examples/xx_name.py`)
├── requirements.txt     Python dependencies for the whole course
├── .env.example         Template for the environment variables the code expects
└── README.md            You are here
```

Each notebook and example is self-contained but builds on the helpers in
[`src/`](./src). Read `docs/` alongside the notebooks for the "why", and use
the notebooks/examples for the "how".
