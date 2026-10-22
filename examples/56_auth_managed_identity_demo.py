"""Pattern 2: Managed identity.

Acquires a token using ``ManagedIdentityCredential`` -- the credential to
reach for when this code (or the Azure MCP Server itself) runs *inside*
Azure (a VM, a Container App, an Azure Function, or an AKS pod with
workload identity configured). There is no stored secret: Azure creates
and rotates the underlying credential for you.

This script only works when actually running on Azure-managed
infrastructure with an identity attached -- it is expected to fail with a
clear message when run on a developer laptop. See
docs/12_authentication_patterns_guide.md (Pattern 2) for how to create and
attach a managed identity before running this.

Run with (inside Azure, after assigning an identity to the resource):

    python examples/56_auth_managed_identity_demo.py

To target a specific user-assigned identity instead of a system-assigned
one, set its client ID first:

    $env:AZURE_MANAGED_IDENTITY_CLIENT_ID = "<user-assigned-identity-client-id>"
    python examples/56_auth_managed_identity_demo.py
"""
import os

from azure.core.exceptions import ClientAuthenticationError
from azure.identity import ManagedIdentityCredential

_ARM_SCOPE = "https://management.azure.com/.default"


def main() -> None:
    client_id = os.getenv("AZURE_MANAGED_IDENTITY_CLIENT_ID")
    credential = ManagedIdentityCredential(client_id=client_id)
    identity_kind = "user-assigned" if client_id else "system-assigned"

    try:
        token = credential.get_token(_ARM_SCOPE)
    except ClientAuthenticationError as exc:
        raise SystemExit(
            "ManagedIdentityCredential could not get a token. This is "
            "expected outside Azure-managed infrastructure (for example, "
            "on a developer laptop). Confirm a managed identity is "
            "attached to this resource and has been granted a role; see "
            f"docs/12_authentication_patterns_guide.md. Original error: {exc}"
        ) from exc

    print(f"Authenticated via ManagedIdentityCredential ({identity_kind}).")
    print("Token acquired for scope:", _ARM_SCOPE)
    print(
        "Never print or log the token value itself -- only metadata like "
        "scope and identity kind, as shown above."
    )


if __name__ == "__main__":
    main()
