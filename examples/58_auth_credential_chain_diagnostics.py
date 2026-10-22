"""Diagnostic: show which credential in the chain actually succeeds.

``DefaultAzureCredential`` tries several credentials in order and only
raises once *all* of them fail -- which makes it easy to authenticate
successfully as the *wrong* identity without realizing it (see the
"wrong identity" entry in docs/12_authentication_patterns_guide.md's
troubleshooting section). This script tries each credential individually,
in the same relative order ``DefaultAzureCredential`` does, and reports
which ones are usable in the current environment instead of hiding that
behind a single pass/fail result.

Run with:

    python examples/58_auth_credential_chain_diagnostics.py
"""
import os

from azure.core.credentials import TokenCredential
from azure.core.exceptions import ClientAuthenticationError
from azure.identity import AzureCliCredential, EnvironmentCredential, ManagedIdentityCredential

_ARM_SCOPE = "https://management.azure.com/.default"


def _try_credential(name: str, credential: TokenCredential) -> bool:
    try:
        credential.get_token(_ARM_SCOPE)
    except ClientAuthenticationError as exc:
        print(f"  [ ] {name}: unavailable ({exc.__class__.__name__})")
        return False
    print(f"  [x] {name}: succeeded")
    return True


def main() -> None:
    print("Checking each credential in isolation (ARM scope):\n")

    env_var_names = ("AZURE_TENANT_ID", "AZURE_CLIENT_ID", "AZURE_CLIENT_SECRET")
    if all(os.getenv(name) for name in env_var_names):
        env_ok = _try_credential("EnvironmentCredential (service principal)", EnvironmentCredential())
    else:
        env_ok = False
        print("  [ ] EnvironmentCredential (service principal): skipped, env vars not set")

    managed_identity_client_id = os.getenv("AZURE_MANAGED_IDENTITY_CLIENT_ID")
    managed_ok = _try_credential(
        "ManagedIdentityCredential",
        ManagedIdentityCredential(client_id=managed_identity_client_id),
    )

    cli_ok = _try_credential("AzureCliCredential", AzureCliCredential())

    print("\nSummary:")
    results = [
        ("EnvironmentCredential (service principal)", env_ok),
        ("ManagedIdentityCredential", managed_ok),
        ("AzureCliCredential", cli_ok),
    ]
    succeeded = [name for name, ok in results if ok]
    if not succeeded:
        print(
            "  No credential in this chain succeeded. Follow Pattern 1, 2, "
            "or 3 in docs/12_authentication_patterns_guide.md to configure "
            "at least one before relying on DefaultAzureCredential."
        )
    else:
        print(f"  DefaultAzureCredential would use: {succeeded[0]}")
        if len(succeeded) > 1:
            print(
                "  Note: more than one credential succeeded. "
                "DefaultAzureCredential always picks the first usable one "
                "in its fixed order, which may not be the identity you "
                "expect -- this is a common source of 'wrong identity' bugs."
            )


if __name__ == "__main__":
    main()
