# Shared operating contract

The five packages exchange versioned reasoning records through the same artifact envelope. A domain skill owns its own payload and does not silently perform another domain's work.

## Required envelope fields

Every generated or handed-off record preserves:

- `artifact_id`, `project_id`, `task_id`, `parent_artifact_ids`;
- `skill_id`, `skill_version`, `artifact_type`, and `status`;
- `task_contract` with question/problem, purpose, audience, context, mode, constraints, and burden/standard;
- `source_ids`, `evidence_ids`, `claim_ids`, `uncertainty_ids`, and `provenance_ids`;
- `learner_decisions`, `ai_use_log`, accessibility notes, rights/permissions, unresolved items, QA checks, and `next_action`.

Only the domain-specific `payload` changes during a handoff. A handoff creates a new versioned artifact that points to its parent; it does not overwrite the source artifact.

## Shared state vocabulary

Use `NEEDS_TASK`, `NEEDS_SOURCE`, `NEEDS_LOCATOR`, `NEEDS_LEARNER_DECISION`, `NEEDS_REVIEW`, `VALIDATED`, `READY_WITH_CONDITIONS`, `COMPLETE`, or `BLOCKED` as appropriate. Use `SOURCE_CONFLICT`, `RIGHTS_REVIEW`, `ACCESSIBILITY_REVIEW`, `AUTHORSHIP_REVIEW`, `DOMAIN_MISMATCH`, and `SCOPE_CREEP` when the reason for stopping matters.

## Routing principle

Route source meaning and evidence location to Close Reading; audience, genre, composition, and revision to Writing; question, corpus, method, perspectives, and synthesis to QUEST; claim strength, warrants, alternatives, and argument comparison to Argumentation; and public disagreement, authority, decision criteria, legitimacy, feasibility, and resolution to Public Argument Resolution.
