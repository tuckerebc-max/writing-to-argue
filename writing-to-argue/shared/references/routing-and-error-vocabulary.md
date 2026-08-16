# Routing and error vocabulary

Use a visible stop, repair, or handoff state when an input is incomplete or the next action belongs to another skill.

| Condition | State or diagnostic | Next action |
|---|---|---|
| Missing task, issue, audience, or purpose | `NEEDS_TASK` / `NEEDS_ISSUE` / `NEEDS_AUDIENCE` | Ask for or contract the missing condition |
| Missing source or locator | `NEEDS_SOURCE` / `NEEDS_LOCATOR` / `LOCATOR_FAILURE` | Request direct source access or a recoverable locator |
| Source disagreement | `SOURCE_CONFLICT` | Preserve both records and compare method, context, currency, and limits |
| Unsupported claim or missing bridge | `UNSUPPORTED_CLAIM` / `MISSING_WARRANT` | Narrow, qualify, test, or route for more evidence |
| Missing perspective or affected party | `PERSPECTIVE_GAP` / `RIGHTS_REVIEW` | Search for missing voices or document a safeguard |
| Method or burden mismatch | `METHOD_MISMATCH` / `BURDEN_MISMATCH` | Return to QUEST or Argumentation for repair |
| Invented or unverified citation | `PROVENANCE_AUDIT` | Directly verify before promotion |
| Assessed-product ghostwriting | `AI_AUTHORSHIP_BOUNDARY` | Return scaffold and learner checkpoints |
| Current rule or high-stakes decision | `CURRENTNESS_REVIEW` / `HIGH_STAKES_REFUSAL` | Require dated sources and accountable human authority |
| Rights, access, or privacy uncertainty | `RIGHTS_REVIEW` / `ACCESSIBILITY_REVIEW` / `PRIVACY_REVIEW` | Stop release until the condition is resolved |
