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

## 1. Check prerequisites

Use Python 3.11 or 3.12 for a straightforward starting environment.
The repository's introductory material says Python 3.9+, but the resolved
versions of the MCP SDK and other dependencies can require a newer Python.
This guide does not change the project's declared support range. Keep
the repository's `mcp<2.0.0` constraint: the remote client uses the v1 SDK's
`streamablehttp_client` API.

Install [Python](https://www.python.org/downloads/) and
[Git](https://git-scm.com/downloads). For the local Azure MCP Server route,
also install [Node.js LTS](https://nodejs.org/) and the
[Azure CLI](https://learn.microsoft.com/cli/azure/install-azure-cli).
Then open a new PowerShell terminal so PATH changes take effect.

```powershell
python --version
git --version

# Needed for the local Azure MCP Server route, not notebooks 24-28:
node --version
npx --version
az --version
```

Each applicable command should print a version, not "command not found".
Corporate proxies must allow Python package downloads and, for the local
Azure route, npm package downloads and the Azure endpoints you use.
Do not bypass certificate validation to work around proxy errors.

For cloud exercises, confirm you have:

- An active Azure subscription and the correct tenant.
- Permission to read the resources you intend to inspect. Management-plane
  Reader access does not automatically grant blob or Key Vault data access.
- For LLM notebooks, a deployed Azure OpenAI model that supports tool
  calling, its deployment name and endpoint, and an appropriate inference
  role (the notebooks use **Cognitive Services User**).
- For live gateway exercises, an API Management tier that supports the
  required MCP/AI gateway feature, permission to configure it, and accessible
  backends. Check current feature availability before provisioning.

Reference: Microsoft's
[Azure MCP Server Python quickstart](https://learn.microsoft.com/azure/developer/azure-mcp-server/get-started/languages/python)
describes local prerequisites and authentication. This repository's
[requirements](../requirements.txt) and notebook code remain the source
of truth for the client APIs used here.

## 2. Create an isolated Python environment

If you already have this repository open, skip cloning and change to its
root. Otherwise:

```powershell
git clone https://github.com/naveed1351/azure-mcp-engineering.git
Set-Location azure-mcp-engineering
```

Create a virtual environment with your chosen Python interpreter:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r .\requirements.txt
.\.venv\Scripts\python.exe -m pip check
```

Stop if installation fails. `pip check` should report
`No broken requirements found.` Explicitly using the environment's Python
avoids installing into a different interpreter and works without changing
PowerShell's script execution policy. If you prefer activation, use
`.\.venv\Scripts\Activate.ps1`, then still use `python -m pip` rather than a
potentially unrelated `pip` executable.

The manifest installs Jupyter, ipykernel, the MCP SDK, Azure Identity, and
the OpenAI client. It also includes the PyPI Azure MCP launcher, although
the local Azure examples actually launch the npm package with `npx`.
Do not replace the requirements with an unbounded `pip install mcp`.

Verify the environment without contacting Azure:

```powershell
.\.venv\Scripts\python.exe -c "import sys; from importlib.metadata import version; import mcp, azure.identity, openai, dotenv; print(sys.executable); print('mcp', version('mcp'))"
```

The executable should be inside this repository's `.venv`, and the MCP
version should be below 2.0. Save dependency-resolution errors rather than
continuing with a partially installed environment.

## 3. Launch Jupyter and select the kernel

Register a recognizable kernel, then launch Jupyter from the same terminal
that can find Node.js and Azure CLI:

```powershell
.\.venv\Scripts\python.exe -m ipykernel install --user --name azure-mcp-engineering --display-name "Python (azure-mcp-engineering)"
.\.venv\Scripts\python.exe -m notebook --notebook-dir=.\notebooks
```

Open the localhost URL printed by Jupyter; keep its access token private.
Choose a notebook and select **Python (azure-mcp-engineering)** from its
kernel menu. Leave the terminal running while working.

Alternatively, open the repository in VS Code with the Python and Jupyter
extensions, open a notebook, and use **Select Kernel > Python Environments**
to choose `.venv\Scripts\python.exe`. Selecting a terminal interpreter alone
does not guarantee the notebook uses the same kernel.

Run this temporary diagnostic cell before the notebook's setup cell:

```python
import sys
from pathlib import Path

print("Python:", sys.executable)
print("Working directory:", Path.cwd())
assert Path.cwd().name == "notebooks", "Set the kernel working directory to this repo's notebooks folder"
assert (Path.cwd().parent / "src" / "config.py").is_file()
```

Most notebook setup cells add `Path.cwd().parent` to `sys.path`, and
notebooks 24-27 locate companion scripts relative to that same parent.
The expected kernel working directory is this repository's `notebooks`
folder, not the repository root. If VS Code starts the kernel elsewhere,
set its notebook file root to `${fileDirname}` (the
`jupyter.notebookFileRoot` setting), restart the kernel, and check again.
Alternatively, explicitly change the kernel directory to the absolute
path of this repository's `notebooks` folder before running setup cells.
Do not work around an incorrect directory by copying helper modules.

Run code cells from top to bottom with **Shift+Enter**. The notebooks use
top-level `await`, supported by IPython; do not wrap those calls in
`asyncio.run()` or paste them unchanged into a plain Python REPL.
After fixing an interrupted run, restart the kernel and rerun setup rather
than relying on stale variables or an old open MCP session.

## 4. Configure Azure authentication and environment values

Skip this section for notebooks 24-28. For Azure work, sign in from a
repository-root terminal and select the intended subscription:

```powershell
az login
az account list --output table
az account set --subscription "<your-subscription-id>"
az account show --query "{subscription:id,tenant:tenantId,name:name}" --output table
```

Replace the subscription placeholder before running. For a specific tenant,
use `az login --tenant "<your-tenant-id>"`; if browser login is unavailable,
use `az login --use-device-code` where your organization's policies permit.
Never paste login codes or tokens into a notebook.

Copy the template only if you do not already have a local configuration:

```powershell
if (-not (Test-Path -LiteralPath .\.env)) {
    Copy-Item -LiteralPath .\.env.example -Destination .\.env
}
```

Edit the root `.env`, not the template:

| Variable | Set it when |
| --- | --- |
| `AZURE_OPENAI_ENDPOINT` | Running 06-07; use the real Azure OpenAI resource endpoint |
| `AZURE_OPENAI_MODEL` | Running LLM cells; this is the **deployment name**, not necessarily the model's catalog name |
| `AZURE_SUBSCRIPTION_ID`, `AZURE_TENANT_ID` | Useful configuration metadata; these fields alone do not force every helper/tool to use that subscription or tenant |
| `APIM_MCP_SERVER_URL` | Connecting to the actual gateway MCP endpoint in 17, 18, or 22, including its `/mcp` path |
| `APIM_SUBSCRIPTION_KEY` | The target gateway API/product requires a subscription key |
| `APIM_MCP_SCOPE` | Acquiring a token for the MCP API's Entra app in 18, typically `api://<app-id>/.default` |
| `APIM_GATEWAY_ENDPOINT` | Calling the OpenAI-compatible gateway API in 21-22, not the MCP endpoint |

Remove unused placeholder values or leave those variables empty. For
example, the template's nonempty fake OpenAI endpoint passes the helper's
"is configured" check but cannot serve requests. Notebooks 01-05 and
08-15 do not need an Azure OpenAI endpoint.

The [configuration helper](../src/config.py) loads `.env` at import and
caches settings. Existing process environment variables take precedence
over dotenv values. Restart the kernel after editing `.env` or changing
credentials; clearing the settings cache alone does not reload the file.
Verify presence without printing secrets:

```python
from src.config import get_settings

settings = get_settings()
print("OpenAI endpoint configured:", bool(settings.azure_openai_endpoint))
print("MCP gateway configured:", bool(settings.apim_mcp_server_url))
```

Run this after the notebook's `sys.path` setup cell.

The Python OpenAI/APIM helpers use `DefaultAzureCredential`; Azure MCP
Server has its own authentication behavior. Azure CLI login is a convenient
local credential, not a guarantee that every chain chooses it over another
available identity. If access differs from `az account show`, inspect
credential-chain diagnostics and explicit tool arguments. See
[authentication](04_authentication.md) for the background. A successful
login does not grant new RBAC permissions.

## 5. Make your first local Azure MCP connection (01-05)

Start with these notebooks in numerical order:

| Notebook | What to run and what success looks like |
| --- | --- |
| [01: Introduction](../notebooks/01_introduction_to_mcp.ipynb) | Read the host/client/server explanation and run the environment probe. Python is reported and required command paths are found for your chosen route. |
| [02: Server setup](../notebooks/02_setting_up_azure_mcp_server.ipynb) | Run version/account checks after terminal login. Confirm the active account and inspect configuration-presence checks; this does not provision resources. |
| [03: First connection](../notebooks/03_first_mcp_client_connection.ipynb) | Run setup and the async connection cell. Initialization completes and tool information is printed, then the context manager closes the session. |
| [04: Tool discovery](../notebooks/04_exploring_available_tools.ipynb) | List/group tools, inspect a schema, and export the catalog. Counts and names reflect the installed server, not a fixed expected count. |
| [05: Direct calls](../notebooks/05_calling_tools_directly.ipynb) | List resource groups and storage accounts. Inspect returned content for actual results or explicit tool errors; the `does-not-exist` example intentionally demonstrates failure handling. |

The [local client helper](../src/mcp_client.py) starts
`npx -y @azure/mcp@latest server start` as a subprocess. Do not start another
stdio server manually and wait for the notebook to connect to it: each
client launches its own process. Initial startup may take longer while
`npx` downloads the package. Standard output belongs to MCP protocol
messages; diagnostic logging must go to standard error.

You can preflight the launcher in the same terminal before starting Jupyter:

```powershell
npx -y @azure/mcp@latest --version
```

This should print a version and exit. It is not a cloud-access test.
Since `@latest` is not pinned, record the reported version when diagnosing
differences between runs.

**Discover before calling.** Notebook 05 and later examples contain
illustrative `azmcp_*` names and argument dictionaries. Compare them with
the current `tools/list` results and `inputSchema`; names, required
subscription arguments, modes, and namespace exposure can change. An
unknown tool or a missing required argument is not evidence that your
subscription has no resources. Use notebook 04 and
[server modes](07_server_modes_and_advanced_config.md) to inspect the
actual surface before adapting a call.

Notebook 04 writes `tool_catalog.json` in the kernel working directory
(normally `notebooks`). It may reveal internal names/descriptions; keep it
local unless deliberately sanitized and reviewed.

## 6. Continue with models, services, and workflows (06-15)

Complete the first-connection checks before this route. The service
notebooks do not create all the accounts, vaults, databases, clusters, or
workspaces they discuss. Replace sample identifiers in code cells with
resources you are allowed to query; leave optional example calls commented
until their inputs and permissions are ready.

| Notebook | Additional preparation and completion check |
| --- | --- |
| [06: Function calling](../notebooks/06_azure_openai_function_calling.ipynb) | Configure OpenAI endpoint/deployment and inference RBAC. Expect a chat response, any requested tool calls, and a final response incorporating results. A model can also answer without choosing a tool. |
| [07: Conversational agent](../notebooks/07_building_a_conversational_agent.ipynb) | Reuse 06's setup. Run the simulated prompts in order; conversation history persists within the agent. Review resource information before sharing responses. |
| [08: Storage and Key Vault](../notebooks/08_storage_and_keyvault_tools.ipynb) | Use existing accounts/vaults. Supply a real account when enabling container-list calls. Blob data and vault secret operations require their own data-plane roles; listing management resources is a separate permission. |
| [09: Resource management](../notebooks/09_resource_management_tools.ipynb) | Confirm subscription scope and access for subscription/group/RBAC discovery. Only enable compute/AKS/container examples for resources you own. |
| [10: Data and analytics](../notebooks/10_data_and_analytics_tools.ipynb) | Prepare the specific database or Monitor/Kusto workspace for any optional calls; replace database/workspace/query placeholders. No matching log rows can be legitimate; authorization/query errors are not. |
| [11: DevOps and deployment](../notebooks/11_devops_and_deployment_tools.ipynb) | Inspect the discovered deployment-related schemas. Bicep/Terraform/azd snippets illustrate a workflow, not a repository-wide deployment command. Install extra deployment tools only if you choose those exercises. |
| [12: Modes and namespaces](../notebooks/12_server_modes_namespaces.ipynb) | Compare generated server arguments and tool exposure. Different modes can expose different tool shapes; compare schemas as well as counts. |
| [13: Errors and retries](../notebooks/13_error_handling_and_retries.ipynb) | Expect intentional failures and retry/backoff demonstrations. Read both Python exceptions and tool-level error content; do not retry authorization or invalid-input failures indefinitely. |
| [14: Security and RBAC](../notebooks/14_security_elicitation_rbac.ipynb) | Inspect annotations and read-only settings. Do not call secret-returning tools merely to test access; these helpers are not a full interactive consent UI. |
| [15: Multi-server workflows](../notebooks/15_advanced_multi_agent_workflows.ipynb) | Register the local client and replace `rg-example` and query inputs before diagnostics. Missing access or an unavailable log tool may prevent that part of the illustrative workflow. Adding another server/agent is an exercise. |

### Model and session caveats

- The [OpenAI helper](../src/azure_openai_helper.py) uses Entra ID, not an
  OpenAI API key, and currently sets API version `2024-04-01-preview`.
  Confirm your deployment supports that API and tool calling. A deployment
  name typo commonly appears as a 404, not a Python import problem.
- Sending a very large tool catalog may exceed a model's tool-count or
  context limits. Use the existing `build_server_params(namespaces=[...],
  read_only=True)` pattern to expose only the namespaces needed for your
  exercise, and rediscover schemas after reconnecting.
- Notebooks 06, 07, and 15 open a client across cells. Always execute the
  final `__aexit__` cleanup cell. After an exception, close any open client
  if possible and restart the kernel before opening another session.
- LLM calls cost money and can send tool results to the configured model
  endpoint. Repeating a cell can repeat a charge or an operation. Read-only
  tool mode reduces mutation risk; it does not eliminate disclosure or
  billing risk.
