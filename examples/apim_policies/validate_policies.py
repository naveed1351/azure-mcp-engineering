"""Validate every policy XML recipe in this folder is well-formed before
you paste it into the Azure API Management portal's policy editor.

Usage: python examples/apim_policies/validate_policies.py
"""
from __future__ import annotations

import sys
import xml.etree.ElementTree as ET
from pathlib import Path


def main() -> int:
    recipes_dir = Path(__file__).resolve().parent
    xml_files = sorted(recipes_dir.rglob("*.xml"))
    if not xml_files:
        print("No .xml recipes found.")
        return 1

    failures = 0
    for path in xml_files:
        try:
            ET.parse(path)
        except ET.ParseError as exc:
            failures += 1
            print(f"INVALID  {path.relative_to(recipes_dir)}: {exc}")
        else:
            print(f"OK       {path.relative_to(recipes_dir)}")

    print(f"\n{len(xml_files)} recipe(s) checked, {failures} failure(s).")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
