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

def search_tools(tools: Iterable[Any], keyword: str) -> list[ToolInfo]:
    """Case-insensitive search over tool names and descriptions.

    Handy when a namespace (e.g. ``storage``) exposes dozens of tools and you
    just want the ones mentioning, say, "blob" or "container".
    """
    keyword = keyword.lower()
    matches = []
    for tool in tools:
        info = ToolInfo.from_mcp_tool(tool)
        haystack = f"{info.name} {info.description}".lower()
        if keyword in haystack:
            matches.append(info)
    return matches

def export_catalog_to_json(tools: Iterable[Any], path: str | Path) -> Path:
    """Write the full tool catalog to a JSON file for offline reference /
    diffing between Azure MCP Server versions."""
    path = Path(path)
    catalog = [asdict(ToolInfo.from_mcp_tool(tool)) for tool in tools]
    path.write_text(json.dumps(catalog, indent=2), encoding="utf-8")
    return path
