"""Pattern 1: Developer sign-in with the Azure CLI.

Acquires a real Azure Resource Manager token using only ``AzureCliCredential``
-- the credential the Azure MCP Server and every other example in this
course fall back on after you run ``az login``. This script does not call
any Azure MCP Server tool; it isolates just the authentication step so you
can see exactly what identity and tenant an ``az login`` session resolves
to in Python.

See docs/12_authentication_patterns_guide.md (Pattern 1) for the full
explanation.

Run with:

    az login
    python examples/55_auth_cli_credential_demo.py
"""
import time

from azure.identity import AzureCliCredential
from azure.core.exceptions import ClientAuthenticationError

_ARM_SCOPE = "https://management.azure.com/.default"


def main() -> None:
    credential = AzureCliCredential()
    try:
        token = credential.get_token(_ARM_SCOPE)
    except ClientAuthenticationError as exc:
        raise SystemExit(
            "AzureCliCredential could not get a token -- run 'az login' "
            f"first. Original error: {exc}"
        ) from exc

    expires_in_minutes = round((token.expires_on - time.time()) / 60)
    print("Authenticated via AzureCliCredential (Pattern 1).")
    print("Token acquired for scope:", _ARM_SCOPE)
    print(f"Token expires in approximately {expires_in_minutes} minute(s).")
    print(
        "Never print or log the token value itself -- only metadata like "
        "scope and expiry, as shown above."
    )


if __name__ == "__main__":
    main()
