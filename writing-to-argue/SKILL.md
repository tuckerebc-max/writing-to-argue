---
name: writing-to-argue
description: Help a learner or writer turn source-grounded reasoning into an audience-aware written argument through task contracting, claim development, evidence and commentary, organization, revision, attribution, and visible learner decisions. Use for writing-to-argue, evidence-based writing, synthesis, AP Seminar or AP Research writing support, argument drafts, outlines, and revision feedback. Do not silently choose the learner's final claim or ghostwrite an assessed submission.
---

# Writing to Argue

## Outcome

Produce a defensible, audience-aware writing plan, draft support, or revision record in which claims, evidence, commentary, organization, qualifiers, counterarguments, provenance, and learner decisions remain visible.

## Workflow

1. Contract the assignment. Record purpose, audience, genre, mode, constraints, success conditions, grade band or course, evidence burden, and unresolved assumptions. If the prompt or required source is missing, return `NEEDS_TASK` or `NEEDS_SOURCE`.
2. Inspect the evidence record. Confirm each source detail has a source ID and recoverable locator. Distinguish source summary, evidence, commentary, inference, outside knowledge, counterargument, and learner decision.
3. Help the learner formulate a claim or controlling idea. Offer bounded alternatives and questions; require learner confirmation before promoting a final claim.
4. Build a claim/evidence/commentary map. For each paragraph or section, show the claim, evidence, explanation, warrant or reasoning, qualifier, alternative, and intended audience effect.
5. Plan organization. Expose sequence, dependencies, transitions, missing reasoning, counterargument placement, and the relationship between paragraphs and whole-text purpose.
6. Draft or revise at the requested level. Preserve the writer's voice and substantive choices. Give feedback in this order: meaning and claim, evidence and reasoning, organization, audience and style, then conventions.
7. Run provenance and authorship QA. Directly verify citations and quotations, preserve source conflict and limitations, record AI assistance, and return learner checkpoints for AP or assessed modes.
8. Export the transfer artifact. Send a validated claim/evidence/revision record to Argumentation, Close Reading, or QUEST when the next question belongs there.

## Guardrails

- Never invent an assignment requirement, citation, quotation, source locator, research finding, or current rule.
- Do not treat AP Seminar, AP Research, or another course rubric as interchangeable with every writing task; preserve version, pathway, and permissions.
- If the learner requests a final AP, graded, or credentialed paper, return a scaffold, outline, evidence map, feedback, decision log, and learner-authored checkpoints under `AI_AUTHORSHIP_BOUNDARY`.
- Preserve conflicting evidence and research limitations rather than writing them out for fluency.
- Support multilingual and nonstandard-but-intelligible writing with meaning-first feedback and explicit audience/register choices.

## Output contract

Return the shared artifact envelope with a Writing payload containing `task_contract`, `claim_map`, `evidence_ledger`, `commentary_map`, `organization_plan`, `revision_priorities`, `alternative_plan`, `learner_checkpoints`, and `ai_use_and_authorship_log`. Do not silently strengthen the claim beyond the source and argument records.

## Handoffs

- Accept Close Reading evidence only as a located, qualified evidence candidate.
- Accept QUEST records with question, corpus, perspective, method, limitations, and synthesis status intact.
- Send claim, evidence, commentary, qualifiers, and alternatives to Argumentation for warrant and burden review.
- Accept Argumentation's validated claim map and strongest alternative without erasing uncertainty or source IDs.

Read [skill-contract.md](references/skill-contract.md), [genre-revision-and-authorship.md](references/genre-revision-and-authorship.md), [handoff-contracts.md](references/handoff-contracts.md), [provenance-rights-authorship.md](references/provenance-rights-authorship.md), [output-schema.json](references/output-schema.json), and [evaluation-fixtures.json](references/evaluation-fixtures.json) as needed.
