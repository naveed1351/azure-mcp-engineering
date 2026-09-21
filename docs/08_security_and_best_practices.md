# 08 — Security and Best Practices

## The security model in one paragraph

The Azure MCP Server never has its own identity or permissions — it always
acts as *you* (your Entra ID user) or as a managed identity you've
configured. Every tool call is authorized through Azure RBAC exactly as if
you'd run the equivalent Azure CLI/SDK call yourself. That means the server
can never do more than your account is already allowed to do, but it also
means a poorly-scoped account (e.g. Owner on a whole subscription) makes an
agent built on top of it just as risky as that role would be for you
personally.
## Elicitation, revisited

Elicitation (see [05_tools_reference.md](05_tools_reference.md)) is your last
line of defense against an LLM silently exfiltrating a Key Vault secret or
connection string into a chat transcript or log file. Treat
`Disable user confirmation=true` the same way you'd treat disabling a
production approval gate: only acceptable in fully automated, fully trusted
pipelines where a human could never have intervened anyway.
