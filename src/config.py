"""Environment/configuration loading for the course examples."""
from __future__ import annotations

import os
from dataclasses import dataclass
from functools import lru_cache

from dotenv import load_dotenv

# Load a local .env file (if present) into the process environment once,
# the first time this module is imported.
load_dotenv()

@dataclass(frozen=True)
class Settings:
    """Strongly-typed view over the environment variables this course uses."""

    azure_openai_endpoint: str | None
    azure_openai_model: str
    azure_subscription_id: str | None
    azure_tenant_id: str | None
    apim_mcp_server_url: str | None
    apim_subscription_key: str | None
    apim_mcp_scope: str | None
    apim_gateway_endpoint: str | None

    @property
    def has_azure_openai(self) -> bool:
        """True if enough configuration is present to build an Azure OpenAI client."""
        return bool(self.azure_openai_endpoint)

    @property
    def has_apim_mcp(self) -> bool:
        """True if an Azure API Management-hosted MCP server URL is configured
        (see notebooks 16-22 and ``docs/10_apim_ai_gateway_and_mcp.md``)."""
        return bool(self.apim_mcp_server_url)

@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Return the process-wide Settings, read once and cached.

    Using ``lru_cache`` means every notebook/example that calls
    ``get_settings()`` shares the same values without re-reading environment
    variables on every call.
    """
    return Settings(
        azure_openai_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        azure_openai_model=os.getenv("AZURE_OPENAI_MODEL", "gpt-4o"),
        azure_subscription_id=os.getenv("AZURE_SUBSCRIPTION_ID"),
        azure_tenant_id=os.getenv("AZURE_TENANT_ID"),
        apim_mcp_server_url=os.getenv("APIM_MCP_SERVER_URL"),
        apim_subscription_key=os.getenv("APIM_SUBSCRIPTION_KEY"),
        apim_mcp_scope=os.getenv("APIM_MCP_SCOPE"),
        apim_gateway_endpoint=os.getenv("APIM_GATEWAY_ENDPOINT"),
    )

def require_apim_mcp(settings: Settings | None = None) -> Settings:
    """Raise a friendly error if no Azure API Management MCP server is configured.

    Notebooks 16-22 that call a *remote* MCP server hosted behind Azure API
    Management should call this at the top of their setup cell instead of
    failing with an opaque connection error.
    """
    settings = settings or get_settings()
    if not settings.has_apim_mcp:
        raise RuntimeError(
            "APIM_MCP_SERVER_URL is not set. Copy .env.example to .env, expose "
            "an MCP server in Azure API Management (see "
            "docs/10_apim_ai_gateway_and_mcp.md), and fill in its endpoint "
            "before running this notebook."
        )
    return settings

def require_azure_openai(settings: Settings | None = None) -> Settings:
    """Raise a friendly error if Azure OpenAI configuration is missing.

    Notebooks that need Azure OpenAI (function-calling / agent examples)
    should call this at the top of their setup cell instead of failing with
    a raw ``KeyError`` or an opaque SDK exception.
    """
    settings = settings or get_settings()
    if not settings.has_azure_openai:
        raise RuntimeError(
            "AZURE_OPENAI_ENDPOINT is not set. Copy .env.example to .env and "
            "fill in your Azure OpenAI resource details before running this "
            "notebook/example."
        )
    return settings
