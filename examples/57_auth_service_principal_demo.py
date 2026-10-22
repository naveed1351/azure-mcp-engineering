"""Pattern 3: Service principal (client secret).

Acquires a token using ``ClientSecretCredential`` -- the credential for
CI/CD pipelines and other unattended automation running *outside* Azure,
where managed identity (Pattern 2) is not available. The identity is an
app registration you created yourself with ``az ad sp create-for-rbac``;
see docs/12_authentication_patterns_guide.md (Pattern 3) for the exact
command and the RBAC role to grant it.

This script reads the three standard environment variable names
``azure-identity`` itself recognizes (the same ones ``EnvironmentCredential``
and ``DefaultAzureCredential`` read automatically) so it never hardcodes a
secret. Never commit real values for these -- store them in your CI
system's secret manager or in a local, gitignored ``.env`` file.

Run with:

    $env:AZURE_TENANT_ID = "<tenant-id>"
    $env:AZURE_CLIENT_ID = "<app-id>"
    $env:AZURE_CLIENT_SECRET = "<client-secret>"
    python examples/57_auth_service_principal_demo.py
"""
import os

from azure.core.exceptions import ClientAuthenticationError
from azure.identity import ClientSecretCredential

_ARM_SCOPE = "https://management.azure.com/.default"
_REQUIRED_ENV_VARS = ("AZURE_TENANT_ID", "AZURE_CLIENT_ID", "AZURE_CLIENT_SECRET")


def main() -> None:
    missing = [name for name in _REQUIRED_ENV_VARS if not os.getenv(name)]
    if missing:
        raise SystemExit(
            f"Missing environment variable(s): {', '.join(missing)}. Set "
            "AZURE_TENANT_ID, AZURE_CLIENT_ID, and AZURE_CLIENT_SECRET to "
            "the values from 'az ad sp create-for-rbac' before running "
            "this script -- see docs/12_authentication_patterns_guide.md."
        )

    credential = ClientSecretCredential(
        tenant_id=os.environ["AZURE_TENANT_ID"],
        client_id=os.environ["AZURE_CLIENT_ID"],
        client_secret=os.environ["AZURE_CLIENT_SECRET"],
    )

    try:
        token = credential.get_token(_ARM_SCOPE)
    except ClientAuthenticationError as exc:
        raise SystemExit(
            "ClientSecretCredential could not get a token. Check that the "
            "client secret hasn't expired (az ad sp credential reset) and "
            f"that the tenant/client IDs match. Original error: {exc}"
        ) from exc

    print("Authenticated via ClientSecretCredential (service principal).")
    print("Token acquired for scope:", _ARM_SCOPE)
    print(
        "Never print or log the client secret or token value itself -- "
        "only metadata like scope, as shown above."
    )


if __name__ == "__main__":
    main()
