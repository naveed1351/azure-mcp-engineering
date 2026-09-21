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
## Quick start

```powershell
# 1. Clone and enter the repo
git clone https://github.com/naveed1351/azure-mcp-engineering.git
cd azure-mcp-engineering

# 2. Create and activate a virtual environment
python -m venv venv
venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Sign in to Azure (the MCP server uses your Azure CLI credential by default)
az login

# 5. Copy the environment template and fill in your Azure OpenAI values
copy .env.example .env

# 6. Launch Jupyter and start with notebooks/01_introduction_to_mcp.ipynb
jupyter notebook notebooks/
```

You don't need to separately install the Azure MCP Server binary: the
notebooks and examples launch it on demand via `npx -y @azure/mcp@latest`.
## Learning path

| # | Notebook | Topic | Related doc |
| - | -------- | ----- | ------------ |
| 1 | [01_introduction_to_mcp.ipynb](notebooks/01_introduction_to_mcp.ipynb) | MCP fundamentals: hosts, clients, servers | [docs/01_what_is_mcp.md](docs/01_what_is_mcp.md) |
| 2 | [02_setting_up_azure_mcp_server.ipynb](notebooks/02_setting_up_azure_mcp_server.ipynb) | Installing & signing in | [docs/03_installation_and_setup.md](docs/03_installation_and_setup.md) |
| 3 | [03_first_mcp_client_connection.ipynb](notebooks/03_first_mcp_client_connection.ipynb) | Your first stdio MCP client | [docs/04_authentication.md](docs/04_authentication.md) |
| 4 | [04_exploring_available_tools.ipynb](notebooks/04_exploring_available_tools.ipynb) | Discovering tools | [docs/06_available_tools_catalog.md](docs/06_available_tools_catalog.md) |
| 5 | [05_calling_tools_directly.ipynb](notebooks/05_calling_tools_directly.ipynb) | Calling tools without an LLM | [docs/05_tools_reference.md](docs/05_tools_reference.md) |
| 6 | [06_azure_openai_function_calling.ipynb](notebooks/06_azure_openai_function_calling.ipynb) | Azure OpenAI function calling | [docs/02_azure_mcp_server_overview.md](docs/02_azure_mcp_server_overview.md) |
| 7 | [07_building_a_conversational_agent.ipynb](notebooks/07_building_a_conversational_agent.ipynb) | A full conversational agent loop | — |
| 8 | [08_storage_and_keyvault_tools.ipynb](notebooks/08_storage_and_keyvault_tools.ipynb) | Storage + Key Vault namespaces | [docs/06_available_tools_catalog.md](docs/06_available_tools_catalog.md) |
| 9 | [09_resource_management_tools.ipynb](notebooks/09_resource_management_tools.ipynb) | Subscriptions, RBAC, compute, AKS | [docs/06_available_tools_catalog.md](docs/06_available_tools_catalog.md) |
| 10 | [10_data_and_analytics_tools.ipynb](notebooks/10_data_and_analytics_tools.ipynb) | Cosmos DB, SQL, Kusto, Monitor | [docs/06_available_tools_catalog.md](docs/06_available_tools_catalog.md) |
| 11 | [11_devops_and_deployment_tools.ipynb](notebooks/11_devops_and_deployment_tools.ipynb) | azd, Bicep, Terraform, deploy | [docs/06_available_tools_catalog.md](docs/06_available_tools_catalog.md) |
| 12 | [12_server_modes_namespaces.ipynb](notebooks/12_server_modes_namespaces.ipynb) | Server modes & namespaces | [docs/07_server_modes_and_advanced_config.md](docs/07_server_modes_and_advanced_config.md) |
| 13 | [13_error_handling_and_retries.ipynb](notebooks/13_error_handling_and_retries.ipynb) | Retries, timeouts, resiliency | [docs/07_server_modes_and_advanced_config.md](docs/07_server_modes_and_advanced_config.md) |
| 14 | [14_security_elicitation_rbac.ipynb](notebooks/14_security_elicitation_rbac.ipynb) | Security, elicitation, RBAC | [docs/08_security_and_best_practices.md](docs/08_security_and_best_practices.md) |
| 15 | [15_advanced_multi_agent_workflows.ipynb](notebooks/15_advanced_multi_agent_workflows.ipynb) | Advanced multi-tool/multi-server workflows | [docs/08_security_and_best_practices.md](docs/08_security_and_best_practices.md) |

Start at `01` and work down — later notebooks assume you understand the
client/tool-calling patterns introduced earlier.
