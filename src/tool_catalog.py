"""Utilities for exploring and searching the set of tools an Azure MCP Server
instance exposes -- used heavily in
``notebooks/04_exploring_available_tools.ipynb``.
"""
from __future__ import annotations

import json
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any, Iterable


@dataclass
class ToolInfo:
    """A flattened, JSON-friendly view of an MCP ``Tool``."""

    name: str
    namespace: str
    description: str
    parameters: dict[str, Any]

    @classmethod
    def from_mcp_tool(cls, tool: Any) -> "ToolInfo":
        # Azure MCP tool names look like "azmcp_storage_account_get";
        # the namespace is the segment right after the "azmcp_" prefix.
        parts = tool.name.split("_")
        namespace = parts[1] if tool.name.startswith("azmcp_") and len(parts) > 1 else "unknown"
        return cls(
            name=tool.name,
            namespace=namespace,
            description=tool.description or "",
            parameters=tool.inputSchema or {},
        )

def group_tools_by_namespace(tools: Iterable[Any]) -> dict[str, list[ToolInfo]]:
    """Group raw MCP tools into ``{namespace: [ToolInfo, ...]}``, sorted for
    stable, readable notebook output."""
    grouped: dict[str, list[ToolInfo]] = {}
    for tool in tools:
        info = ToolInfo.from_mcp_tool(tool)
        grouped.setdefault(info.namespace, []).append(info)
    for infos in grouped.values():
        infos.sort(key=lambda t: t.name)
    return dict(sorted(grouped.items()))
