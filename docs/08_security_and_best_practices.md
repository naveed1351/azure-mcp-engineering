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
## Best practices checklist

- ✅ Start every new agent/workflow with `--read-only` until you've verified
  its prompts and tool choices behave as expected.
- ✅ Scope namespaces (`--namespace storage --namespace monitor`, etc.) to the
  minimum set a given workflow actually needs.
- ✅ Prefer least-privilege RBAC roles (e.g. **Reader**, **Storage Blob Data
  Reader**) over broad roles like **Contributor** or **Owner** for the
  identity the agent runs as.
- ✅ Leave elicitation enabled for anything touching secrets.
- ✅ Log tool calls and their arguments (not their secret-bearing results) for
  auditability.
- ✅ Treat the local MCP server as a developer tool, not a production
  service — don't expose it to untrusted callers or external users.
