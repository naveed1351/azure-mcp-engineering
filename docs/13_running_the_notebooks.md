# Running the notebooks

This is the practical runbook for all 28 notebooks in this learning
repository. Use it for installation, choosing a kernel, preparing cloud
resources, and deciding which cells are safe to run. The
[learning path](../README.md#learning-path) and the conceptual notes in
[docs](./) explain the topics in more depth.

## Choose a route

| Route | Notebooks | What you need |
| --- | --- | --- |
| Understand MCP without Azure | 24-28 | Python and the repository dependencies; no Azure login, Node.js, or LLM deployment |
| Learn the local Azure MCP Server | 01-05, then 08-15 | Python, Node.js LTS, Azure CLI, an Azure identity, and permissions for the services you query |
| Add an LLM | 06-07 | The local-server setup plus an Azure OpenAI deployment and inference permissions |
| Put APIs and models behind a gateway | 16-23 | Python; live exercises additionally need API Management, reachable backends, and the authentication described in each notebook |

For a first cloud-backed run, follow 01-05 before adding an LLM or gateway.
For a first Azure-free run, start at 24 and continue through 28. Notebook
15's sample workflow is not itself an LLM loop; adding one is an exercise.
Reading notebook text does not require cloud resources.

## Before running any cells

- Use a learning subscription and non-sensitive sample data. Inspect each
  tool and policy before running it against a shared environment.
- Cloud resources must already exist unless you explicitly follow a
  provisioning exercise. Installing Python packages does not deploy Azure.
- Tool catalogs and model responses vary by server version, configuration,
  permissions, and subscription contents. An empty resource list can be a
  valid result; an error response is not a successful empty list.
- Read each notebook's markdown and code before using **Run All**. Some
  examples deliberately trigger errors or contain resource placeholders.
- Do not commit credentials, access tokens, or notebook outputs containing
  private resource details. The real environment file is ignored by Git.

The commands in this guide use Windows PowerShell. Run terminal commands
from the repository root unless a step explicitly says otherwise; run
Python cells in the notebook kernel.
