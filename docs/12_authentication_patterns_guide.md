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
