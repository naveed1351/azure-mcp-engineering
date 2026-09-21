"""Environment/configuration loading for the course examples."""
from __future__ import annotations

import os
from dataclasses import dataclass
from functools import lru_cache

from dotenv import load_dotenv

# Load a local .env file (if present) into the process environment once,
# the first time this module is imported.
load_dotenv()
