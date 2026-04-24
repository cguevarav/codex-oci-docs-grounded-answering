#!/usr/bin/env python3
"""Validate evidence coverage for OCI grounded answers.

Input: JSON array of objects with keys:
  - claim_text
  - source_url
  - support_strength (strong|moderate|weak)
"""

from __future__ import annotations

import json
import sys
from typing import Any


ALLOWED_STRENGTH = {"strong", "moderate", "weak"}


def _die(msg: str, code: int = 2) -> None:
    print(f"ERROR: {msg}", file=sys.stderr)
    raise SystemExit(code)


def _load(path: str) -> list[dict[str, Any]]:
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        _die(f"file not found: {path}")
    except json.JSONDecodeError as exc:
        _die(f"invalid JSON: {exc}")

    if not isinstance(data, list):
        _die("top-level JSON value must be an array")

    rows: list[dict[str, Any]] = []
    for i, item in enumerate(data):
        if not isinstance(item, dict):
            _die(f"entry {i} is not an object")
        rows.append(item)
    return rows


def main() -> None:
    if len(sys.argv) != 2:
        _die("usage: check_evidence_coverage.py <evidence.json>")

    rows = _load(sys.argv[1])
    total = len(rows)
    supported = 0

    for i, row in enumerate(rows):
        claim = str(row.get("claim_text", "")).strip()
        src = str(row.get("source_url", "")).strip()
        strength = str(row.get("support_strength", "")).strip().lower()

        if not claim:
            _die(f"entry {i} missing claim_text")
        if not src:
            _die(f"entry {i} missing source_url")
        if strength not in ALLOWED_STRENGTH:
            _die(f"entry {i} has invalid support_strength: {strength}")

        if strength in {"strong", "moderate"}:
            supported += 1

    print(f"supported_claims={supported}")
    print(f"total_claims={total}")
    if total == 0:
        print("coverage=0/0")
    else:
        print(f"coverage={supported}/{total}")

    if supported < total:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
