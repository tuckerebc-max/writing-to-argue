#!/usr/bin/env python3
"""Evaluate the standalone skill repository's representative artifact."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def get_path(value: Any, path: str) -> Any:
    current = value
    for part in path.split("."):
        if isinstance(current, dict) and part in current:
            current = current[part]
        else:
            raise KeyError(path)
    return current


def nonempty(value: Any) -> bool:
    if value is None:
        return False
    if isinstance(value, str):
        return bool(value.strip())
    if isinstance(value, (list, dict)):
        return bool(value)
    return True


def run_check(record: dict[str, Any], check: dict[str, Any]) -> dict[str, Any]:
    check_id = check["check_id"]
    check_type = check["type"]
    failure_status = check.get("failure_status", "NEEDS_REVIEW")
    try:
        if check_type in {"required_paths", "present_paths"}:
            missing = []
            for path in check["paths"]:
                try:
                    value = get_path(record, path)
                except KeyError:
                    missing.append(path)
                    continue
                if check_type == "required_paths" and not nonempty(value):
                    missing.append(path)
            if missing:
                return {"check_id": check_id, "status": "FAIL", "failure_status": failure_status, "evidence": f"missing or empty: {missing}", "message": check.get("message", "")}
            return {"check_id": check_id, "status": "PASS", "evidence": f"{len(check['paths'])} paths present"}
        if check_type == "all_items_have":
            items = get_path(record, check["path"])
            if not isinstance(items, list) or not items:
                return {"check_id": check_id, "status": "FAIL", "failure_status": failure_status, "evidence": f"{check['path']} is empty or not a list", "message": check.get("message", "")}
            failures = []
            for index, item in enumerate(items):
                if not isinstance(item, dict):
                    failures.append(f"{index}: not an object")
                    continue
                absent = [field for field in check["fields"] if field not in item or not nonempty(item[field])]
                if absent:
                    failures.append(f"{index}: {absent}")
            if failures:
                return {"check_id": check_id, "status": "FAIL", "failure_status": failure_status, "evidence": f"item failures: {failures}", "message": check.get("message", "")}
            return {"check_id": check_id, "status": "PASS", "evidence": f"{len(items)} items contain required fields"}
        if check_type == "unique_values":
            values = get_path(record, check["path"])
            if not isinstance(values, list) or not values:
                return {"check_id": check_id, "status": "FAIL", "failure_status": failure_status, "evidence": f"{check['path']} is empty or not a list", "message": check.get("message", "")}
            if len(values) != len(set(values)):
                return {"check_id": check_id, "status": "FAIL", "failure_status": failure_status, "evidence": f"duplicate values in {check['path']}", "message": check.get("message", "")}
            return {"check_id": check_id, "status": "PASS", "evidence": f"{len(values)} unique values"}
        if check_type == "manual_review":
            return {"check_id": check_id, "status": "CONDITIONAL", "evidence": check["condition"], "topic": check.get("topic", "")}
        return {"check_id": check_id, "status": "FAIL", "failure_status": "EVALUATOR_SPEC_ERROR", "evidence": f"unsupported check type: {check_type}"}
    except KeyError as exc:
        return {"check_id": check_id, "status": "FAIL", "failure_status": failure_status, "evidence": f"path not found: {exc.args[0]}", "message": check.get("message", "")}


def evaluate(repo_root: Path, record_path: Path) -> dict[str, Any]:
    spec = load_json(repo_root / "references" / "evaluator-spec.json")
    record = load_json(record_path)
    errors = []
    if record.get("skill_id") != spec.get("skill_id"):
        errors.append(f"record skill_id {record.get('skill_id')!r} does not match {spec.get('skill_id')!r}")
    checks = [run_check(record, check) for check in spec.get("checks", [])]
    failed = [check for check in checks if check["status"] == "FAIL"]
    conditional = [check for check in checks if check["status"] == "CONDITIONAL"]
    status = "FAIL" if failed or errors else ("CONDITIONAL" if conditional else "PASS")
    return {"evaluator_id": spec.get("evaluator_id"), "skill_id": spec.get("skill_id"), "competency_id": spec.get("competency_id"), "record_path": record_path.as_posix(), "status": status, "errors": errors, "checks": checks}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--record", type=Path)
    args = parser.parse_args()
    root = args.repo_root.resolve()
    record = (args.record or (root / "tests" / "fixtures" / "representative-record.json")).resolve()
    try:
        result = evaluate(root, record)
    except Exception as exc:
        print(json.dumps({"status": "FAIL", "errors": [str(exc)]}, indent=2))
        return 1
    print(json.dumps(result, indent=2))
    return 1 if result["status"] == "FAIL" else 0


if __name__ == "__main__":
    sys.exit(main())
