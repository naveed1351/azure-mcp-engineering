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
