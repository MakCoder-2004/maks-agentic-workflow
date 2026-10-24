# feature: collection

Model: openai-codex/gpt-6-luna, high. Tools: read only. Scope: routing/permission explanation, not application implementation. Exit code: 0.

## Ownership
Matt owns discovery and the authoritative spec/tickets. Next use Matt’s `research` and `grill-with-docs` (which composes the original `grilling` and `domain-modeling` skills). Addy’s `interview-me` or `idea-refine` can help clarify intent; `spec-driven-development` and `constraint-driven-development` supplement requirements and quality gates, not create a competing plan.

## Next steps
Clarify, one question at a time: who requests work and who handles it; what problem the current process causes; the request lifecycle and exceptions; what “done” means; scope and non-goals; and relevant constraints. Start with: **Who is the primary user, and what are they trying to get done that is difficult today?** My guess is employees submitting requests, because you called this internal request tracking—but that may be wrong.

After decisions settle, Matt’s `to-spec` synthesizes them, then `to-tickets` proposes verifiable vertical slices and blockers. Review and approve both before implementation. If architecture or a prototype is needed, bound it to a specific uncertainty first.

## Gates
Approve scope/design, then the spec, then ticket granularity and dependencies. Handoff to original pstack `poteto-mode` with approved artifact references, blockers/ready tickets, glossary/ADRs, constraints, test commands, and scope/permissions. Poteto-mode implements and verifies one ready ticket at a time, applying relevant Addy checks before moving on. PR/publishing actions need their own authorization.

## Evidence limits
This is a planning-only answer based on repository workflow and skill files. No code, tests, tracker updates, independent reviewers, or runtime checks were performed.
