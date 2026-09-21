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

    @property
    def has_azure_openai(self) -> bool:
        """True if enough configuration is present to build an Azure OpenAI client."""
        return bool(self.azure_openai_endpoint)
