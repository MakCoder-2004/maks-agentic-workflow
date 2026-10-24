# architecture: collection

Model: openai-codex/gpt-6-luna, high. Tools: read only. Scope: routing/permission explanation, not application implementation. Exit code: 0.

### Ownership
Matt owns planning: research, domain/glossary and ADR decisions, then the authoritative approved spec and dependency-aware tickets via `to-spec` → `to-tickets`. Original pstack `poteto-mode` owns implementation, per-ticket verification, and PR preparation. Do not run Matt’s implement-spec or Addy’s build controller as competing implementation owners.  
Source: [workflow](docs/guide/README.md).

### Next steps
After approving scope, design, spec, tickets, and execution permissions, hand poteto-mode the full references, blockers/ready frontier, glossary/ADRs, constraints, real test commands, required evidence, and action permissions. It should implement and verify one ready ticket at a time. Addy skills supplement relevant slices: requirements and constraints in planning; API/security in design or build; testing, browser/runtime, review, migration, observability, CI/CD, and launch checks as applicable. Release actions need separate authorization.

### Gates
Resolve design uncertainty and approve the final plan before production implementation. For each ticket, test the affected behavior, run relevant real-surface and Addy checks, fix and retest findings, then record evidence before dependent work. Failed, blocked, missing, or inconclusive checks are not passes. PR publication, merge, deployment, and destructive actions require their own grants.

### Evidence limits
The guide describes the pinned original packages and their intended coordination; `sources.lock.json` records provenance and active copies. These files do not prove a host actually registers every skill, provides delegation or independent models, or has browsers, services, credentials, and runtime tools. The setup guide explicitly warns that Markdown discovery is not proof of full pstack runtime compatibility. This was a read-only documentation review; no tests, runtime checks, or implementation occurred.
