# 12 — Azure MCP Server Authentication Patterns: A Guide

This guide expands on [04_authentication.md](04_authentication.md) with a
practical, side-by-side look at the three authentication patterns you'll
actually choose between when running the Azure MCP Server and the Python
helpers in this repository: interactive developer sign-in via the **Azure
CLI**, **managed identity** for workloads already running in Azure, and
**service principal** credentials for CI/CD and other unattended automation.

It pairs with four runnable scripts in [`examples/`](../examples/README.md)
(55-58) that exercise each pattern directly with the `azure-identity`
library, independent of any specific Azure MCP tool call.

## Why this matters beyond `az login`

Every example in notebooks 01-15 and 24-28 assumes you've already signed in
once with `az login` and moves on. That's the right default for learning,
but it hides an important fact: **the Azure MCP Server and this repo's
Python helpers (`src/azure_openai_helper.py`, `src/apim_mcp_client.py`) each
resolve credentials independently**, through their own instance of a
credential chain. Understanding what's actually in that chain — and in what
order — is what lets you reason about:

- Why a tool call authenticates as a different identity than you expect.
- How to run the same code unattended in a pipeline or inside an Azure
  resource, with no human available to run `az login`.
- Which failure (`CredentialUnavailableError`, `ClientAuthenticationError`,
  an RBAC `403`) points at *which* layer of the chain.

## At a glance

| Pattern | Typical use | Who/what it authenticates as | Needs a human present? |
| --- | --- | --- | --- |
| Azure CLI sign-in | Local development, this course's notebooks | Your own Entra ID user | Yes, once per session |
| Managed identity | Code already running inside Azure (VM, Container App, Function, AKS pod) | An identity Azure itself manages — no stored secret | No |
| Service principal (client secret) | CI/CD pipelines, scheduled jobs, anything outside Azure that can't use managed identity | An app registration you created and control | No, but a secret must be stored safely |

Each is covered in its own section below, including the exact commands to
set it up and the corresponding Python credential class.

## Table of contents

1. [Pattern 1 — Developer sign-in with the Azure CLI](#pattern-1--developer-sign-in-with-the-azure-cli)
2. [Pattern 2 — Managed identity](#pattern-2--managed-identity)
3. [Pattern 3 — Service principal (client secret)](#pattern-3--service-principal-client-secret)
4. [Choosing the right pattern](#choosing-the-right-pattern)
5. [Troubleshooting credential chain issues](#troubleshooting-credential-chain-issues)
6. [Further resources](#further-resources)

## Pattern 1 — Developer sign-in with the Azure CLI

This is the pattern every notebook in this course uses. You sign in once
per machine/session, and both the Azure MCP Server (via its credential
chain mode) and this repo's Python helpers (via `DefaultAzureCredential`)
pick up that session automatically through `AzureCliCredential`.

```powershell
# Sign in interactively (opens a browser)
az login

# If your organization has multiple tenants, be explicit:
az login --tenant "<your-tenant-id>"

# Pick the subscription everything should default to
az account set --subscription "<your-subscription-id>"

# Confirm what Azure CLI (and therefore AzureCliCredential) will report
az account show --query "{subscription:id, tenant:tenantId, user:user.name}" --output table
```

`AzureCliCredential` works by shelling out to `az account get-access-token`
behind the scenes — it does not read any stored password. That's why
signing out of the CLI (`az logout`) or switching the active subscription
with `az account set` immediately changes what every Python script and the
Azure MCP Server itself authenticate as, with no code changes required.

**When to use it:** local development, this course's notebooks, and any
interactive terminal session where a person is present to approve the
sign-in. It is the first pattern to reach for and the one this repository
assumes by default.

**What it is not for:** anything that needs to run unattended (a scheduled
job, a CI pipeline, a server process with nobody watching) — `az login`
needs either a browser or a device code a human must complete.

## Pattern 2 — Managed identity

If this repo's code (or the Azure MCP Server itself) runs *inside* Azure —
on a VM, in a Container App, as an Azure Function, or on an AKS pod with
workload identity configured — use a **managed identity** instead of any
stored credential at all. Azure creates and rotates the underlying secret
for you; your code never sees it.

There are two flavors:

| Flavor | Lifecycle | Typical use |
| --- | --- | --- |
| System-assigned | Created with and tied to one specific resource; deleted when the resource is deleted | A single Container App or Function that only ever needs its own identity |
| User-assigned | Created independently, then attached to one or more resources | Sharing one identity across several resources, or needing the identity to outlive any one resource |

Create a user-assigned identity and attach it (example: a Container App):

```powershell
az identity create --name "id-azure-mcp-demo" --resource-group "<your-resource-group>"
az containerapp identity assign \
  --name "<your-container-app>" \
  --resource-group "<your-resource-group>" \
  --user-assigned "<user-assigned-identity-resource-id>"
```

Then grant that identity whatever RBAC role it needs on the target
resource (for example **Storage Blob Data Reader** on a storage account),
the same way you would for your own user in [04_authentication.md](04_authentication.md#rbac-what-determines-what-you-can-do).

In Python, request a token with `ManagedIdentityCredential` directly, or
let `DefaultAzureCredential` find it automatically:

```python
from azure.identity import DefaultAzureCredential, ManagedIdentityCredential

# System-assigned identity: no extra argument needed.
credential = ManagedIdentityCredential()

# User-assigned identity: pass its client ID explicitly.
credential = ManagedIdentityCredential(client_id="<user-assigned-identity-client-id>")

# Or let DefaultAzureCredential try managed identity as part of its chain,
# the same chain src/azure_openai_helper.py and src/apim_mcp_client.py use.
credential = DefaultAzureCredential(managed_identity_client_id="<user-assigned-identity-client-id>")
```

**When to use it:** any production-like Azure-hosted workload. It is
strictly more secure than a service principal secret because there is no
secret to leak, rotate, or expire.

**What it is not for:** your own laptop, or anything outside Azure (GitHub
Actions runners, on-premises servers, another cloud) — `ManagedIdentityCredential`
only works on infrastructure Azure itself is managing.
