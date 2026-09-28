# Changelog

Notable changes to this learning repository. This project doesn't ship
versioned releases; entries are grouped by topic instead of a version
number.

## Example gallery expansion

- Added 44 new standalone demo scripts (`examples/11_*` through
  `examples/54_*`), one per additional Azure MCP Server namespace not
  already covered by the original 10 tutorial scripts -- including
  `appconfig`, `acr`, `aks`, `appservice`, `compute`, `sql`, `mysql`,
  `postgres`, `redis`, `servicebus`, `eventgrid`, `eventhubs`, `iothub`,
  `role` (RBAC), `pricing`, `search`, `speech`, `cloudarchitect`, and more.
- Added [docs/09_example_gallery.md](docs/09_example_gallery.md), an index
  mapping every example script to its namespace and the specific
  `azmcp_*` tool it calls.
- Cross-linked the new gallery from the README, the tools catalog
  ([docs/06_available_tools_catalog.md](docs/06_available_tools_catalog.md)),
  and the closing section of
  [docs/08_security_and_best_practices.md](docs/08_security_and_best_practices.md).
- All new scripts default to `read_only=True` and call only non-destructive
  `get`/`list` tools, so they're safe to run repeatedly against a real
  Azure subscription.
