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

## 7. Prepare and run the API Management route (16-23)

These notebooks mix explanatory text, portal instructions, XML/Bicep
examples, and live Python requests. Reading a policy or parsing XML locally
does not apply it to a gateway. You can study the route without provisioning
anything; live cells require the infrastructure and authentication below.

### Prepare the gateway before live requests

1. Use a lab API Management instance with current support for the features
   you intend to test. Check
   [MCP server support](https://learn.microsoft.com/azure/api-management/mcp-server-overview)
   and the [AI gateway overview](https://learn.microsoft.com/azure/api-management/genai-gateway-capabilities)
   for tier and feature limitations.
2. For 17, import a suitable REST API and expose selected operations as an
   MCP server using the notebook's portal instructions. For 20's federation
   route, first have a reachable existing MCP backend instead. A local
   stdio subprocess is not a public HTTP backend.
3. Choose inbound authentication, associate any required product, configure
   backend authentication separately, and copy the real MCP endpoint to
   `.env`. A subscription key and an Entra bearer token serve different
   purposes; some configurations require both.
4. For 21-22, configure an OpenAI-compatible API route and model backend in
   the gateway, with the intended deployment name and backend permissions.
   Set `APIM_GATEWAY_ENDPOINT` to this route, not to `/mcp`.
5. Restart the kernel after updating configuration. Verify MCP discovery
   before enabling tool calls, then verify the model route separately
   before combining them.

The remote helper uses Streamable HTTP and opens the configured gateway
endpoint; it does not start the Azure MCP npm server.

| Notebook | Run instructions and expected evidence |
| --- | --- |
| [16: Gateway fundamentals](../notebooks/16_apim_ai_gateway_fundamentals.ipynb) | Read the architecture/tier guidance and inspect constructed URLs. The sample `my-apim-instance`/`weather-mcp` values are not deployed services. |
| [17: REST API as MCP](../notebooks/17_exposing_rest_apis_as_mcp_servers.ipynb) | Complete portal setup, then list tools through the real endpoint. **Inspect `first.inputSchema` and the operation's effects before the `call_first_tool` cell**: it sends `{}` to the first returned tool and is not generically safe or valid. Supply required arguments or skip it. |
| [18: Entra security](../notebooks/18_securing_mcp_servers_with_entra_id.ipynb) | Configure the Entra app, allowed audience/tenant, and policy first; set the actual scope. Token acquisition and gateway token validation must both succeed. Add a subscription key to the connection if your product also requires one. |
| [19: Governance](../notebooks/19_mcp_server_policies_and_governance.ipynb) | Run the local XML example, then adapt and apply policies deliberately in the lab portal. Local XML parsing is not gateway policy validation. Confirm enforcement with controlled requests. |
| [20: Federation and discovery](../notebooks/20_federating_existing_mcp_servers_and_discovery.ipynb) | Follow portal/backend setup and replace `<subscription-id>`, `<resource-group>`, and `<apim-service-name>` in the ARM example; `.env` does not replace these code literals. The management call needs ARM permissions, independently of MCP endpoint access. |
| [21: LLM resiliency](../notebooks/21_ai_gateway_llm_backends_and_resiliency.ipynb) | Configure the gateway model route before sending chat requests. Load balancing, caching, and token policies require their described backends/services; a single successful chat request does not prove failover. |
| [22: Gateway capstone](../notebooks/22_end_to_end_agent_over_apim_gateway.ipynb) | Verify both endpoint values, model deployment, and required credentials before running the live cells. Expect discovered tools and a final chat answer; the initial missing-config message is informational and does not prevent later cells from running. |
| [23: Policy choice](../notebooks/23_choosing_apim_vs_ai_gateway.ipynb) | Run the local decision/recipe exploration. Use the companion recipes to choose policies; applying them and provisioning optional services is a separate step. |

### Match each API's authentication

The sample calls in 17 and 22 pass `APIM_SUBSCRIPTION_KEY` to the MCP
connection. Notebook 18 demonstrates passing a bearer token instead.
If your MCP API requires Entra authentication, acquire the appropriate
MCP-scope token and pass `bearer_token` through the existing
`connect_apim_mcp(...)` parameter on **every** relevant connection, including
discovery and tool execution. Add the key too if required. Merely setting
`APIM_MCP_SCOPE` does not change 17 or 22's connection arguments.

The model route in 21-22 supplies a Cognitive Services bearer token.
If the gateway model API also requires a subscription key, adapt the
`AzureOpenAI` client headers to include `Ocp-Apim-Subscription-Key`;
configuring the key for MCP calls does not automatically add it to chat
requests. Never print either credential while diagnosing 401/403 errors.

For policy recipes, correlation-header adaptation, and background, see
[the APIM companion](10_apim_ai_gateway_and_mcp.md),
[the policy decision guide](11_apim_vs_ai_gateway_decision_guide.md), and
[the recipe index](../examples/apim_policies/README.md). The current remote
helper accepts subscription/token credentials, not an arbitrary `headers`
argument; the capstone's correlation-ID discussion requires explicit
helper adaptation before those headers can be forwarded.

## 8. Run the Azure-free protocol route (24-28)

Complete the Python installation and kernel setup in sections 1-3, then
skip Azure login and `.env` configuration. After installing dependencies,
these exercises communicate with local Python subprocesses and do not need
an Azure subscription, Node.js, API Management, or a real model endpoint.

Keep the full checkout: the notebooks launch
[custom_server.py](../examples/mcp_foundations/custom_server.py) and
[raw_jsonrpc_client.py](../examples/mcp_foundations/raw_jsonrpc_client.py).
Downloading only the notebook files will not work. The server is launched
using `sys.executable`, so it inherits the notebook's selected Python.

| Notebook | Expected evidence |
| --- | --- |
| [24: Lifecycle and JSON-RPC](../notebooks/24_mcp_lifecycle_and_jsonrpc.ipynb) | The raw client shows initialize, discovery, and a tool-call exchange. If the captured output is blank, check the subprocess return code and stderr instead of assuming success. |
| [25: Custom server](../notebooks/25_building_a_custom_mcp_server.ipynb) | Discovery includes `add`, `generate_poem`, and `book_table`, the fixed server-info resource, and the `greet_user` prompt. Calling `add(5, 7)` returns text representing `12`. |
| [26: Resources and prompts](../notebooks/26_mcp_resources_and_prompts.ipynb) | Resource reads return greeting/server-info text; getting `greet_user` returns prompt messages, not a model-generated greeting. A templated resource is distinct from a fixed resource entry. |
| [27: Sampling and roots](../notebooks/27_mcp_sampling_and_roots.ipynb) | The sampling callback prints the server's request and returns the fixed stand-in poem. Roots capability is advertised; the sample server does not actually request a roots listing. |
| [28: Transports recap](../notebooks/28_mcp_transports_and_capability_recap.ipynb) | Read the transport/capability comparison. This is a conceptual recap, not a command to launch a remote HTTP service. |

For a terminal-only preflight, run from the repository root:

```powershell
.\.venv\Scripts\python.exe .\examples\mcp_foundations\raw_jsonrpc_client.py
```

Expect a completed JSON-RPC conversation and process exit, not a waiting
server prompt. If you launch `custom_server.py` directly instead, waiting
silently on stdin is normal: it needs an MCP client, not typed Python
commands. Stop that manually launched process with **Ctrl+C**; the
notebooks create their own server processes.

Notebook 27's roots callback uses `file:///tmp/project` as illustrative
metadata, not as a directory you must create on Windows. For a real root,
use a directory you intend to expose and convert its absolute path with
`Path(...).resolve().as_uri()`. Advertising roots is not an operating-system
sandbox and does not grant or enforce filesystem permissions by itself.

The stand-in sampling callback makes this route free of LLM API charges.
Replacing it with a real model call is an optional code exercise with its
own authentication, cost, and consent requirements. Likewise, the custom
server's elicitation tool needs an elicitation-capable client to handle
the confirmation path; listing the tool is not proof that a callback has
been implemented.

See [protocol foundations](12_mcp_protocol_foundations.md) and the
[standalone script instructions](../examples/mcp_foundations/README.md)
for further context.
