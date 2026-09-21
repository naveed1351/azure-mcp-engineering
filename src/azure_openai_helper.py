"""Azure OpenAI client + function-calling helpers used by the agent notebooks."""
from __future__ import annotations

import json
from typing import Any

from azure.identity import DefaultAzureCredential, get_bearer_token_provider
from openai import AzureOpenAI

from .config import Settings, require_azure_openai

_COGNITIVE_SERVICES_SCOPE = "https://cognitiveservices.azure.com/.default"
