"""
Validate every docs/it/**/*.fsm.yaml against schema/fsm.schema.json.

Usage:
    uv run python scripts/validate_fsm.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator

REPO_ROOT = Path(__file__).parent.parent
SCHEMA_PATH = REPO_ROOT / "schema" / "fsm.schema.json"
DOCS_IT = REPO_ROOT / "docs" / "it"


def main() -> None:
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    validator = Draft202012Validator(schema)

    paths = sorted(DOCS_IT.glob("**/*.fsm.yaml"))
    if not paths:
        print("no *.fsm.yaml files found under docs/it/")
        return

    failed = False
    for path in paths:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
        errors = sorted(validator.iter_errors(data), key=lambda e: list(e.path))
        rel = path.relative_to(REPO_ROOT)
        if errors:
            failed = True
            print(f"INVALID: {rel}")
            for error in errors:
                location = "/".join(str(p) for p in error.path) or "<root>"
                print(f"  {location}: {error.message}")
        else:
            print(f"OK: {rel}")

    if failed:
        sys.exit(1)


if __name__ == "__main__":
    main()
