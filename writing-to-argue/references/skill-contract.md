# Writing to Argue package contract

**Registry ID:** `SKILL-WR`  
**Package version:** `0.1.0`  
**Source domain:** `DOM-WR`  
**Current status:** `READY_WITH_CONDITIONS`

## Required inputs

Supply an assignment or rhetorical situation, purpose, audience, genre, mode, constraints, evidence burden, grade band or course, and any supplied sources or draft. A missing assignment or source stops the run.

## Core payload

The package produces `task_contract`, `claim_map`, `evidence_ledger`, `commentary_map`, `organization_plan`, `revision_priorities`, `alternative_plan`, `learner_checkpoints`, and `ai_use_and_authorship_log` inside the shared artifact envelope.

## Quality conditions

Claims, source details, commentary, inference, outside knowledge, counterargument, qualifiers, organization, revision decisions, source locators, and learner authorship remain distinct. Feedback prioritizes meaning and reasoning before conventions.

## Canonical source paths

See `catalog/source-manifest.json` for the portable mapping to the prompt, corpus crosswalk, competency design specification, technical specification, and textbook architecture. The source validation IDs are `TST-WR-001` through `TST-WR-011`, plus `TST-INT-004` and `TST-INT-005`.
