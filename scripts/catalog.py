#!/usr/bin/env python3
"""Validate discovery metadata and maintain the README catalog; never run kits."""

import argparse
import html
import json
import re
import sys
import tomllib
from pathlib import Path

from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parents[1]
BEGIN = "<!-- BEGIN CATALOG -->"
END = "<!-- END CATALOG -->"
GROUPS = (
    ("software-product-development", "Software & Product Development"),
    ("science", "Science"),
)


def validate_registry(path):
    with path.open("rb") as source:
        registry = tomllib.load(source)
    schema = json.loads((ROOT / "schema/registry.schema.json").read_text(encoding="utf-8"))
    validator = Draft202012Validator(schema)
    errors = list(validator.iter_errors(registry))
    if errors:
        details = [f"{'.'.join(map(str, error.absolute_path)) or 'registry'}: {error.message}"
                   for error in errors]
        raise ValueError("\n".join(details))

    ids = set()
    repositories = set()
    for entry in registry["kits"] + registry.get("related_tools", []):
        if entry["id"] in ids:
            raise ValueError(f"Duplicate id: {entry['id']}")
        ids.add(entry["id"])
        key = (entry["repository"].casefold(), entry.get("kit", ""))
        if key in repositories:
            raise ValueError(f"Duplicate repository/kit: {entry['repository']} {entry.get('kit', '')}".strip())
        repositories.add(key)
        for field in ("name", "description", "publisher"):
            if entry[field] != entry[field].strip():
                raise ValueError(f"{entry['id']}.{field}: must not have surrounding whitespace")
    return registry


def markdown_text(value):
    """Publisher text is text, never HTML or Markdown markup."""
    return re.sub(r"([\\`*_{}\[\]()#!|])", r"\\\1", html.escape(value, quote=False))


def render_catalog(registry):
    lines = []
    for category, heading in GROUPS:
        kits = [entry for entry in registry["kits"] if category in entry["categories"]]
        tools = [entry for entry in registry.get("related_tools", []) if category in entry["categories"]]
        if not kits and not tools:
            continue
        lines += [f"## {heading}", ""]
        for index, entry in enumerate(kits + tools, 1):
            name, description = [markdown_text(entry[field]) for field in ("name", "description")]
            repository = entry["repository"]
            suffix = " · **Related tool**" if index > len(kits) else ""
            lines += [f"{index}. [**{name}**](https://github.com/{repository}) — {description} [`{repository}`](https://github.com/{repository}){suffix}"]
        lines += [""]
    return "\n".join(lines).rstrip() + "\n"


def updated_readme(readme, catalog):
    if readme.count(BEGIN) != 1 or readme.count(END) != 1:
        raise ValueError("README must contain exactly one BEGIN CATALOG and END CATALOG marker")
    start = readme.index(BEGIN) + len(BEGIN)
    finish = readme.index(END)
    if finish < start:
        raise ValueError("README catalog markers are in the wrong order")
    return readme[:start] + "\n\n" + catalog + "\n" + readme[finish:]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--registry", type=Path, default=ROOT / "registry.toml")
    parser.add_argument("--readme", type=Path, default=ROOT / "README.md")
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--write", action="store_true", help="Regenerate only the marked README catalog")
    mode.add_argument("--check", action="store_true", help="Fail if README differs from registry")
    args = parser.parse_args()
    try:
        registry = validate_registry(args.registry)
        if args.write or args.check:
            readme = args.readme.read_text(encoding="utf-8")
            updated = updated_readme(readme, render_catalog(registry))
            if args.check and updated != readme:
                raise ValueError("README catalog is out of date. Run: python scripts/catalog.py --write")
            if args.write:
                args.readme.write_text(updated, encoding="utf-8")
        print(f"Valid registry: {len(registry['kits'])} kits, {len(registry.get('related_tools', []))} related tools.")
        return 0
    except (OSError, ValueError) as error:
        print(f"Catalog validation failed: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
