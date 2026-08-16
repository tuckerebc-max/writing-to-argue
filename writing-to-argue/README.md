# Writing to Argue

Standalone GitHub repository for the Main textbook skill `SKILL-WR` and competency `COMP-WR-ARGUE`.

Upload this folder as the repository root. It includes `SKILL.md`, Codex UI metadata, competency and assessment codification, evaluator specification, output schema, handoff contract, provenance and authorship guidance, source manifest, shared schemas, fixtures, validation scripts, CI, release metadata, and checksums.

## Canonical design trace

`SPEC-WR-001` · `ANRI-DOM-WR-001` · `ARCH-WR-001` · `CORP-WR-001`

This package is finalized as a private draft. Its evaluator retains human-review conditions for authorship, AP/assessed work, currentness, rights, and transfer. It does not invent assignments, citations, quotations, source locators, or findings.

## Validate locally

```text
python scripts/validate_repository.py
python scripts/validate_repository.py --check
python scripts/evaluate_package.py
python scripts/build_release_manifest.py --check
```

The canonical textbook source files remain external and are mapped, not copied, in `catalog/source-manifest.json`.
