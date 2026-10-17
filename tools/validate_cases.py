#!/usr/bin/env python3
"""Validate eval-cases.jsonl against the case schema.

Usage:
    python validate_cases.py [path/to/eval-cases.jsonl]

Checks: required fields, score shapes, severity vocabulary, duplicate ids.
Exit code 0 = valid, 1 = errors found.
"""
from __future__ import annotations

import json
import sys

REQUIRED = {"id", "date", "models", "prompt", "critique", "verdict", "severity", "lang", "topic"}
SEVERITIES = {"minor", "major", "critical"}
OPTIONAL = {"scores"}


def validate(path: str) -> list[str]:
    errors: list[str] = []
    seen: set[str] = set()
    try:
        lines = open(path, encoding="utf-8").read().strip().split("\n")
    except OSError as exc:
        return [f"cannot read file: {exc}"]
    for i, line in enumerate(lines, 1):
        if not line.strip():
            continue
        try:
            rec = json.loads(line)
        except json.JSONDecodeError as exc:
            errors.append(f"line {i}: invalid JSON ({exc})")
            continue
        missing = REQUIRED - set(rec)
        if missing:
            errors.append(f"line {i} [{rec.get('id', '?')}]: missing fields {sorted(missing)}")
        unknown = set(rec) - REQUIRED - OPTIONAL
        if unknown:
            errors.append(f"line {i} [{rec.get('id', '?')}]: unknown fields {sorted(unknown)}")
        cid = rec.get("id")
        if cid in seen:
            errors.append(f"line {i}: duplicate id '{cid}'")
        seen.add(cid)
        if rec.get("severity") not in SEVERITIES:
            errors.append(f"line {i} [{cid}]: severity must be one of {sorted(SEVERITIES)}")
        models = rec.get("models")
        if not isinstance(models, list) or not models:
            errors.append(f"line {i} [{cid}]: 'models' must be a non-empty list")
        scores = rec.get("scores", {})
        if not isinstance(scores, dict):
            errors.append(f"line {i} [{cid}]: 'scores' must be an object")
        for m, s in scores.items():
            if not (isinstance(s, (int, float)) and 1 <= s <= 5) and not (
                isinstance(s, str) and s.startswith("FAIL")
            ):
                errors.append(f"line {i} [{cid}]: score for '{m}' must be 1-5 or 'FAIL (...)'")
    return errors


def main() -> None:
    path = sys.argv[1] if len(sys.argv) > 1 else "eval-cases.jsonl"
    errors = validate(path)
    if errors:
        print(f"{len(errors)} error(s) in {path}:")
        for e in errors:
            print(" -", e)
        sys.exit(1)
    print(f"OK: {path} is valid.")


if __name__ == "__main__":
    main()
