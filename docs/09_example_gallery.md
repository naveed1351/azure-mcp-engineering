# 09 — Example Gallery

The [`examples/`](../examples) folder has grown from the original 10
step-by-step tutorial scripts into a much larger gallery covering almost
every Azure MCP Server namespace listed in
[06_available_tools_catalog.md](06_available_tools_catalog.md). This page is
a quick-reference index so you can jump straight to the namespace you care
about instead of reading every script in order.

Every script follows the same shape:

```python
async with connect(namespaces=["<namespace>"], read_only=True) as client:
    result = await client.call_tool("azmcp_<tool>", {...})
    print(result.content)
```

Run any of them with `python examples/<file>.py` after `az login`. Scripts
whose tool needs more than a subscription (a resource group, account name,
vault, endpoint, etc.) say so in their module docstring and use obvious
`<placeholder>` argument values — edit those before running.

## Getting started (01-10)

| Script | What it shows |
| --- | --- |
| [01_list_tools.py](../examples/01_list_tools.py) | Enumerate every tool the server exposes |
| [02_call_tool_directly.py](../examples/02_call_tool_directly.py) | Call a tool without an LLM in the loop |
| [03_chat_with_tools.py](../examples/03_chat_with_tools.py) | One-shot Azure OpenAI function-calling round trip |
| [04_resource_groups_demo.py](../examples/04_resource_groups_demo.py) | `subscription` / `group` namespaces |
| [05_storage_demo.py](../examples/05_storage_demo.py) | `storage` namespace |
| [06_keyvault_demo.py](../examples/06_keyvault_demo.py) | `keyvault` namespace |
| [07_cosmos_demo.py](../examples/07_cosmos_demo.py) | `cosmos` namespace |
| [08_monitor_kusto_demo.py](../examples/08_monitor_kusto_demo.py) | `monitor` / `kusto` namespaces |
| [09_learn_mode_discovery.py](../examples/09_learn_mode_discovery.py) | Discover parameters with `learn` mode |
| [10_multi_turn_agent_cli.py](../examples/10_multi_turn_agent_cli.py) | Full interactive multi-turn agent |

## Resource, identity & cost governance

| Script | Namespace | Tool called |
| --- | --- | --- |
| [41_rbac_demo.py](../examples/41_rbac_demo.py) | `role` | `azmcp_role_assignment_list` |
| [39_policy_demo.py](../examples/39_policy_demo.py) | `policy` | `azmcp_policy_assignment_list` |
| [38_quota_demo.py](../examples/38_quota_demo.py) | `quota` | `azmcp_quota_region_availability_list` |
| [51_advisor_demo.py](../examples/51_advisor_demo.py) | `advisor` | `azmcp_advisor_recommendation_list` |
| [42_resourcehealth_demo.py](../examples/42_resourcehealth_demo.py) | `resourcehealth` | `azmcp_resourcehealth_health-events_list` |
| [40_pricing_demo.py](../examples/40_pricing_demo.py) | `pricing` | `azmcp_pricing_get` (no Azure sign-in needed) |
| [52_resiliency_demo.py](../examples/52_resiliency_demo.py) | `resiliency` | `azmcp_resiliency_usageplan_get` |
| [53_well_architected_demo.py](../examples/53_well_architected_demo.py) | `wellarchitectedframework` | `azmcp_wellarchitectedframework_serviceguide_get` |

## Storage & databases

| Script | Namespace | Tool called |
| --- | --- | --- |
| [26_mysql_demo.py](../examples/26_mysql_demo.py) | `mysql` | `azmcp_mysql_list` |
| [27_postgres_demo.py](../examples/27_postgres_demo.py) | `postgres` | `azmcp_postgres_list` |
| [28_redis_demo.py](../examples/28_redis_demo.py) | `redis` | `azmcp_redis_list` |
| [29_sql_demo.py](../examples/29_sql_demo.py) | `sql` | `azmcp_sql_server_get` |
| [30_fileshares_demo.py](../examples/30_fileshares_demo.py) | `fileshares` | `azmcp_fileshares_fileshare_get` |
| [49_storagesync_demo.py](../examples/49_storagesync_demo.py) | `storagesync` | `azmcp_storagesync_service_get` |
| [50_azurebackup_demo.py](../examples/50_azurebackup_demo.py) | `azurebackup` | `azmcp_azurebackup_vault_get` |

## Monitoring & analytics

| Script | Namespace | Tool called |
| --- | --- | --- |
| [12_applicationinsights_demo.py](../examples/12_applicationinsights_demo.py) | `applicationinsights` | `azmcp_applicationinsights_recommendation_list` |
| [33_grafana_demo.py](../examples/33_grafana_demo.py) | `grafana` | `azmcp_grafana_list` |
| [48_workbooks_demo.py](../examples/48_workbooks_demo.py) | `workbooks` | `azmcp_workbooks_list` |
| [37_datadog_demo.py](../examples/37_datadog_demo.py) | `datadog` | `azmcp_datadog_monitoredresources_list` |

## Compute & containers

| Script | Namespace | Tool called |
| --- | --- | --- |
| [14_aks_demo.py](../examples/14_aks_demo.py) | `aks` | `azmcp_aks_cluster_get` |
| [13_container_registry_demo.py](../examples/13_container_registry_demo.py) | `acr` | `azmcp_acr_registry_list` |
| [16_compute_demo.py](../examples/16_compute_demo.py) | `compute` | `azmcp_compute_vm_get` |
| [18_containerapps_demo.py](../examples/18_containerapps_demo.py) | `containerapps` | `azmcp_containerapps_list` |
| [15_appservice_demo.py](../examples/15_appservice_demo.py) | `appservice` | `azmcp_appservice_webapp_get` |
| [31_functionapp_demo.py](../examples/31_functionapp_demo.py) | `functionapp` | `azmcp_functionapp_get` |
| [32_functions_demo.py](../examples/32_functions_demo.py) | `functions` | `azmcp_functions_language_list` (no Azure sign-in needed) |
| [17_servicefabric_demo.py](../examples/17_servicefabric_demo.py) | `servicefabric` | `azmcp_servicefabric_managedcluster_node_get` |

## Messaging, IoT & integration

| Script | Namespace | Tool called |
| --- | --- | --- |
| [20_eventgrid_demo.py](../examples/20_eventgrid_demo.py) | `eventgrid` | `azmcp_eventgrid_topic_list` |
| [21_eventhubs_demo.py](../examples/21_eventhubs_demo.py) | `eventhubs` | `azmcp_eventhubs_namespace_get` |
| [22_servicebus_demo.py](../examples/22_servicebus_demo.py) | `servicebus` | `azmcp_servicebus_queue_details` |
| [23_deviceregistry_demo.py](../examples/23_deviceregistry_demo.py) | `deviceregistry` | `azmcp_deviceregistry_namespace_list` |
| [24_iothub_demo.py](../examples/24_iothub_demo.py) | `iothub` | `azmcp_iothub_hub_get` |
| [25_iotoperations_demo.py](../examples/25_iotoperations_demo.py) | `iotoperations` | `azmcp_iotoperations_instance_list` |
| [45_signalr_demo.py](../examples/45_signalr_demo.py) | `signalr` | `azmcp_signalr_runtime_get` |

## AI, search & architecture assistants

| Script | Namespace | Tool called |
| --- | --- | --- |
| [43_ai_search_demo.py](../examples/43_ai_search_demo.py) | `search` | `azmcp_search_service_list` |
| [44_speech_demo.py](../examples/44_speech_demo.py) | `speech` | `azmcp_speech_stt_recognize` (local-required tool) |
| [54_cloudarchitect_demo.py](../examples/54_cloudarchitect_demo.py) | `cloudarchitect` | `azmcp_cloudarchitect_design` |

## Developer tools, testing & misc

| Script | Namespace | Tool called |
| --- | --- | --- |
| [11_appconfig_demo.py](../examples/11_appconfig_demo.py) | `appconfig` | `azmcp_appconfig_account_list` |
| [34_loadtesting_demo.py](../examples/34_loadtesting_demo.py) | `loadtesting` | `azmcp_loadtesting_testresource_list` |
| [35_managedlustre_demo.py](../examples/35_managedlustre_demo.py) | `managedlustre` | `azmcp_managedlustre_fs_list` |
| [36_marketplace_demo.py](../examples/36_marketplace_demo.py) | `marketplace` | `azmcp_marketplace_product_list` |
| [46_sreagent_demo.py](../examples/46_sreagent_demo.py) | `sreagent` | `azmcp_sreagent_agents_list` |
| [47_virtualdesktop_demo.py](../examples/47_virtualdesktop_demo.py) | `virtualdesktop` | `azmcp_virtualdesktop_hostpool_list` |
| [19_confidentialledger_demo.py](../examples/19_confidentialledger_demo.py) | `confidentialledger` | `azmcp_confidentialledger_entries_get` |

## Notes on tool names and arguments

- Tool names mirror the `azmcp` CLI command path with spaces replaced by
  underscores (hyphens inside a command segment, like `health-events`, are
  preserved) -- see
  [microsoft/mcp's command reference](https://github.com/microsoft/mcp/blob/main/servers/Azure.Mcp.Server/docs/azmcp-commands.md)
  for the authoritative list.
- Tool arguments use the same names as the CLI flags, minus the leading
  `--` (for example `--resource-group` becomes the `"resource-group"` key).
- Every demo defaults to `read_only=True` and calls only non-destructive
  `get`/`list` tools, so they're safe to run repeatedly against a real
  subscription.

Next: there is no `10_` sequel to this page -- it's a living index. As the
Azure MCP Server adds namespaces, add a matching `examples/NN_<name>_demo.py`
script and a row here.
