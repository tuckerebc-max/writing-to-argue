#!/usr/bin/env python3
"""Build or verify the repository SHA-256 manifest."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path


def files_for_manifest(root: Path):
    excluded = {Path("catalog/checksums.json")}
    for path in sorted(root.rglob("*")):
        if not path.is_file() or ".git" in path.parts:
            continue
        relative = path.relative_to(root)
        if relative in excluded or relative.name in {"checksums.local.json", "release-manifest.local.json"}:
            continue
        yield relative


def digest(path: Path) -> str:
    hasher = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            hasher.update(chunk)
    return hasher.hexdigest()


def build(root: Path) -> dict:
    files = [{"path": path.as_posix(), "sha256": digest(root / path), "bytes": (root / path).stat().st_size} for path in files_for_manifest(root)]
    return {"algorithm": "sha256", "status": "generated", "generated_at": datetime.now(timezone.utc).isoformat(), "file_count": len(files), "files": files}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    root = args.repo_root.resolve()
    target = root / "catalog" / "checksums.json"
    current = build(root)
    if args.check:
        try:
            recorded = json.loads(target.read_text(encoding="utf-8"))
        except Exception as exc:
            print(f"ERROR cannot read {target}: {exc}")
            return 1
        recorded_files = {item.get("path"): item for item in recorded.get("files", [])}
        current_files = {item["path"]: item for item in current["files"]}
        errors = []
        if recorded.get("status") != "generated":
            errors.append("checksums.json is not marked generated")
        if set(recorded_files) != set(current_files):
            errors.append("checksums file list does not match repository files")
        for path, item in current_files.items():
            if recorded_files.get(path, {}).get("sha256") != item["sha256"]:
                errors.append(f"checksum mismatch: {path}")
        if errors:
            for error in errors:
                print(f"ERROR {error}")
            return 1
        print(f"PASS release checksum manifest: {len(current_files)} files")
        return 0
    target.write_text(json.dumps(current, indent=2) + "\n", encoding="utf-8")
    print(f"PASS generated {target}: {current['file_count']} files")
    return 0


if __name__ == "__main__":
    sys.exit(main())
