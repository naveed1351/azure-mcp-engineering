# 06 — Available Tools Catalog

The Azure MCP Server groups tools into namespaces, one per Azure service or
capability area. This page mirrors the
[official tools index](https://learn.microsoft.com/en-us/azure/developer/azure-mcp-server/tools/)
so you have an offline reference while working through the notebooks.

## Best practices

| Product/tool | Namespace | Description |
| --- | --- | --- |
| Azure best practices | `get_azure_bestpractices` (`get`) | Guidance on Azure Functions development, deployment, and Azure SDK usage. |
| Azure AI best practices for app development | `get_azure_bestpractices` (`ai app`) | Recommendations for building AI apps, agents, chatbots, and Foundry code generation. |
| Terraform best practices for Azure | `azureterraformbestpractices` | Best practices for Azure Terraform usage. |

## AI and Machine Learning

| Product/tool | Namespace | Description |
| --- | --- | --- |
| Microsoft Foundry | `foundry` | Work with Foundry models, deployments, and endpoints. |
| Azure AI Search | `search` | Manage search services, indexes, and queries. |
| Azure Speech in Foundry Tools | `speech` | Speech-to-text / text-to-speech resources. |
| Azure SRE Agent | `sreagent` | Agents, skills, connectors, incidents, workflows. |
## Analytics

| Product/tool | Namespace | Description |
| --- | --- | --- |
| Azure App Lens | `applens` | Diagnose and analyze application performance issues. |
| Azure Data Explorer | `kusto` | Clusters, databases, tables, and KQL queries. |
| Azure Event Hubs | `eventhubs` | Namespaces and event hubs. |

## Compute

| Product/tool | Namespace | Description |
| --- | --- | --- |
| Azure App Service | `appservice` | Web apps, DB connections, diagnostics, deployments, settings. |
| Azure Functions | `functionapp` | List Azure Functions. |
| Azure Kubernetes Service | `aks` | List AKS clusters. |
| Azure Service Fabric | `servicefabric` | Managed clusters, node details, restarts. |
| Azure Compute | `compute` | VMs, VM scale sets, managed disks. |

## Containers

| Product/tool | Namespace | Description |
| --- | --- | --- |
| Azure Container Registry | `acr` | List ACR instances. |
| Azure Functions | `functionapp` | List Azure Functions. |
| Azure Kubernetes Service | `aks` | List AKS clusters. |
| Azure Service Fabric | `servicefabric` | Managed clusters, node details, restarts. |
## Databases

| Product/tool | Namespace | Description |
| --- | --- | --- |
| Azure Cosmos DB | `cosmos` | Accounts, databases, containers, documents. |
| Azure Database for MySQL | `mysql` | Servers, databases, tables. |
| Azure Database for PostgreSQL | `postgres` | Servers, databases, tables. |
| Azure Redis | `redis` | Managed Redis and Cache for Redis. |
| Azure SQL | `sql` | Servers, databases, firewall rules, elastic pools. |

## Developer tools

| Product/tool | Namespace | Description |
| --- | --- | --- |
| Azure App Configuration | `appconfig` | Centralized settings and feature flags. |
| Azure Application Insights | `applicationinsights` | List Application Insights resources. |
| Azure CLI | `extension` | Find CLI commands and install instructions. |
| Azure Developer CLI (azd) | `extension` | azd install instructions, deployment usage, azd MCP tools. |
| Azure Load Testing | `loadtesting` | Create, run, and view load tests. |
## DevOps

| Product/tool | Namespace | Description |
| --- | --- | --- |
| Azure Bicep schema | `bicepschema` | Bicep schemas for IaC templates. |
| Azure Deploy | `deploy` | Deploy and manage resources via templates/scripts. |
| Azure Developer CLI | `extension` | azd usage for deployment scenarios. |
| Azure Managed Grafana | `grafana` | List Grafana workspaces. |
| Azure Monitor | `monitor` | Query logs and metrics. |
| Azure Terraform | `azureterraform` | Provider docs, Azure Verified Modules, export-to-Terraform, policy validation. |
| Azure Workbooks | `workbooks` | Create/manage/update Workbooks for visualization. |

## Identity

| Product/tool | Namespace | Description |
| --- | --- | --- |
| Azure RBAC | `role` | View and manage role-based access control assignments. |

## Integration

| Product/tool | Namespace | Description |
| --- | --- | --- |
| Azure Event Grid | `eventgrid` | Topics and subscriptions. |
| Azure Native ISV (Datadog) | `datadog` | Monitoring/observability integration. |
| Azure Service Bus | `servicebus` | Queues, topics, peek at messages. |
## IoT and hybrid/multicloud

| Product/tool | Namespace | Description |
| --- | --- | --- |
| Azure Cosmos DB | `cosmos` | Accounts, databases, containers, documents. |
| Azure Device Registry | `deviceregistry` | Namespaces for organizing IoT device assets. |
| Azure Event Grid | `eventgrid` | Topics and subscriptions. |
| Azure Functions | `functionapp` | List Azure Functions. |
| Azure IoT Hub | `iothub` | List devices/hubs. |
| Azure Database for PostgreSQL | `postgres` | Also usable in hybrid/multicloud scenarios. |
| Azure SQL | `sql` | Also usable in hybrid/multicloud scenarios. |

> This catalog is not exhaustive — the server adds namespaces over time. Use
> `learn mode` (see [05_tools_reference.md](05_tools_reference.md)) or
> [`notebooks/04_exploring_available_tools.ipynb`](../notebooks/04_exploring_available_tools.ipynb)
> to list what your installed version actually exposes.

Next: [07_server_modes_and_advanced_config.md](07_server_modes_and_advanced_config.md)
