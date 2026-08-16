#!/usr/bin/env python3
"""Validate one standalone textbook-skill GitHub repository."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from datetime import date
from pathlib import Path
from typing import Any


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--source-root", type=Path)
    parser.add_argument("--check", action="store_true", help="Validate without rewriting finalization report")
    args = parser.parse_args()
    root = args.repo_root.resolve()
    errors: list[str] = []
    required = [
        "SKILL.md", "agents/openai.yaml", "references/competency-codification.md", "references/evaluator-spec.json",
        "references/output-schema.json", "references/handoff-contracts.md", "references/provenance-rights-authorship.md",
        "references/evaluation-fixtures.json", "catalog/skill-catalog.json", "catalog/source-manifest.json",
        "catalog/handoff-route-registry.json", "catalog/release-manifest.json", "shared/schemas/interoperability-artifact-envelope.schema.json",
        "shared/fixtures/interoperability-handoff-fixtures.json", "tests/fixtures/representative-record.json",
    ]
    for relative in required:
        if not (root / relative).exists():
            errors.append(f"missing required file: {relative}")
    try:
        catalog = load_json(root / "catalog" / "skill-catalog.json")
        entries = catalog.get("skills", [])
        if len(entries) != 1:
            errors.append("standalone catalog must contain exactly one skill")
        entry = entries[0] if entries else {}
        evaluator = load_json(root / "references" / "evaluator-spec.json")
        fixtures = load_json(root / "references" / "evaluation-fixtures.json")
        source_manifest = load_json(root / "catalog" / "source-manifest.json")
        handoffs = load_json(root / "catalog" / "handoff-route-registry.json")
    except Exception as exc:
        errors.append(f"invalid required JSON: {exc}")
        entry, evaluator, fixtures, source_manifest, handoffs = {}, {}, {}, {}, {}

    skill_id = entry.get("skill_id")
    package_name = entry.get("package_name")
    if skill_id and evaluator.get("skill_id") != skill_id:
        errors.append("evaluator skill_id does not match catalog")
    if skill_id and evaluator.get("competency_id") != entry.get("competency_id"):
        errors.append("evaluator competency_id does not match catalog")
    skill_text = (root / "SKILL.md").read_text(encoding="utf-8") if (root / "SKILL.md").exists() else ""
    frontmatter = re.search(r"\A---\n(.*?)\n---", skill_text, re.DOTALL)
    if not frontmatter:
        errors.append("SKILL.md has no valid frontmatter")
    elif f"name: {package_name}" not in frontmatter.group(1):
        errors.append("SKILL.md name does not match catalog package_name")
    for link in re.findall(r"\]\((references/[^)]+)\)", skill_text):
        if not (root / link).exists():
            errors.append(f"broken SKILL.md reference: {link}")
    check_ids = [check.get("check_id") for check in evaluator.get("checks", [])]
    if len(check_ids) != len(set(check_ids)):
        errors.append("evaluator check IDs are not unique")
    if evaluator.get("required_test_ids"):
        fixture_tests = {fixture.get("source_test_id") for fixture in fixtures.get("fixtures", [])}
        missing_tests = set(evaluator["required_test_ids"]) - fixture_tests
        shared_tests = {test for test in missing_tests if str(test).startswith(("TST-INT-", "TST-MSS-"))}
        if missing_tests - shared_tests:
            errors.append(f"evaluator tests without domain fixtures: {sorted(missing_tests - shared_tests)}")
    if source_manifest.get("records") and skill_id not in {record.get("skill_id") for record in source_manifest["records"]}:
        errors.append("source manifest has no domain record for this skill")
    route_ids = {route.get("handoff_id") for route in handoffs.get("routes", [])}
    if set(entry.get("handoff_ids", [])) - route_ids:
        errors.append("catalog handoff IDs are absent from the route registry")

    evaluator_process = subprocess.run([sys.executable, str(root / "scripts" / "evaluate_package.py"), "--repo-root", str(root)], cwd=root, capture_output=True, text=True, encoding="utf-8")
    try:
        evaluator_result = json.loads(evaluator_process.stdout)
        if evaluator_result.get("status") not in {"PASS", "CONDITIONAL"}:
            errors.append(f"representative evaluator returned {evaluator_result.get('status')!r}")
    except Exception as exc:
        errors.append(f"representative evaluator did not return JSON: {exc}")

    report_path = root / "catalog" / "finalization-report.json"
    report = {
        "finalization_id": f"{skill_id}-standalone-finalization",
        "checked_at": date.today().isoformat(),
        "status": "FINALIZED_PRIVATE_DRAFT" if not errors else "BLOCKED",
        "repository_visibility": "private",
        "skill_id": skill_id,
        "package_name": package_name,
        "source_fidelity": {"status": "VERIFIED_WITH_LOCAL_SOURCE_ROOT" if args.source_root else "PORTABLE_SOURCE_MANIFEST", "source_root_hint": args.source_root.name if args.source_root else "AI-Native-ELA-Reasoning-Inquiry-Textbooks-2026-08-08"},
        "evaluator_status": evaluator_result.get("status") if 'evaluator_result' in locals() and isinstance(evaluator_result, dict) else "FAIL",
        "errors": errors,
        "remaining_conditions": ["Fresh-context/model-based forward testing remains a human/reviewer gate.", "Official/current assessment, standards, and rights confirmation remains required before public production release.", "AP and assessed-mode assistance remains scaffold-first and learner-authored."]
    }
    if args.check:
        try:
            committed = load_json(report_path)
            if committed.get("status") != "FINALIZED_PRIVATE_DRAFT":
                errors.append("committed finalization report is not FINALIZED_PRIVATE_DRAFT")
        except Exception as exc:
            errors.append(f"cannot read committed finalization report: {exc}")
        if errors:
            print("FAIL standalone repository validation")
            for error in errors:
                print(f"- {error}")
            return 1
    else:
        report["status"] = "FINALIZED_PRIVATE_DRAFT" if not errors else "BLOCKED"
        report["errors"] = errors
        report_path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    if errors:
        print("FAIL standalone repository validation")
        for error in errors:
            print(f"- {error}")
        return 1
    print(f"PASS standalone repository: {package_name} ({skill_id}); evaluator {report['evaluator_status']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
