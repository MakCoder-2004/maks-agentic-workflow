# Scenario recipes using the original skills

Run `setup-agentic-workflow` once when configuring a project; it combines the original setup responsibilities and initializes/preserves AGENTS.md. The other names identify existing upstream skills. Use [host-correct invocation](setup.md), including native namespaces where installed. Follow [the shared workflow](README.md) for approval, evidence and ownership; do not mechanically run every skill below.

## 1. Start a new project

**Goal:** settle what matters before generating an application.

1. Matt `research` + `grill-with-docs`: audience, problem, outcomes, non-goals, constraints, domain language and uncertain decisions. Use `wayfinder` only for genuinely large uncertainty.
2. Addy `idea-refine`/`spec-driven-development` as relevant requirements checks, and `constraint-driven-development` for the quality bar. Keep Matt's planning authoritative.
3. Matt `codebase-design`/`prototype` and pstack `architect with checkpoint` for meaningful architecture alternatives. For UI, use actual frontend-design + ui-ux-pro-max.
4. Matt `to-spec`, then `to-tickets`; approve the resulting behavior, design, test seams and blocker graph.
5. Handoff to actual poteto-mode. Build a small vertical capability first, test it, apply relevant Addy checks, and continue through ready tickets. Pstack prepares focused PRs; Addy covers real release readiness.

Start prompt:

> Use grill-with-docs to define [idea] for [users]. Research facts yourself, ask me the product decisions, and document vocabulary and consequential decisions. Use Addy's requirements and quality-constraint skills where they add missing coverage, without creating another spec. No production scaffolding yet. After any needed architecture/prototype work, use to-spec and to-tickets for approval.

**Artifacts:** original configured glossary/ADRs, approved spec, ready tickets, project constraints, working vertical slice and verification evidence. **Recovery:** if a prototype invalidates a premise, return to the decision/spec before issuing speculative implementation tickets.

## 2. Add a feature to an existing project

1. Read actual source/history/tests with pstack `how`/`why`; Matt `research` can capture primary-source/API facts.
2. Matt `grill-with-docs` resolves behavioral changes, existing compatibility, permissions and non-goals. Reuse existing vocabulary/architecture rather than redesigning automatically.
3. Apply relevant Addy `api-and-interface-design`, security and constraints. Explore architecture/UI only where needed, with a checkpoint.
4. Matt `to-spec` -> `to-tickets`. Each slice is independently demonstrable/verifiable, not merely "database layer" then "UI layer".
5. Poteto-mode implements the ready frontier with per-ticket checks. Use Addy TDD/runtime/browser/security where relevant. Update affected docs, review, then prepare PRs.

Handoff prompt:

> Use poteto-mode for spec [ref] and tickets [refs]. Their approved decisions and blocking edges are authoritative. Keep existing architecture and public behavior outside this scope. Implement one ready slice, test the changed behavior on its real surface, apply the relevant Addy checks, and fix/retest before proceeding. Prepare PRs after current evidence; do not publish or merge without the corresponding grant.

**Completion:** acceptance criteria and required checks are evidenced, not just code present. **Recovery:** material new requirements go back to Matt's spec/tickets; ordinary implementation details stay with pstack.

## 3. Fix a bug or issue

A small clear bug needs a concise expected/actual/repro/acceptance note, not a manufactured extensive product spec.

1. Matt `triage` for an unclear incoming report; Matt `diagnosing-bugs` is useful when focused diagnosis must precede implementation. Pstack `how` and its bug/forensics playbooks can investigate within the requested scope.
2. Establish intended behavior, affected surface and a red-capable minimal reproduction. Separate an observed fact from a hypothesis.
3. Clarify non-obvious requirements with Matt; create/refine the original tracker ticket. Approve the bounded fix scope.
4. Poteto-mode owns the fix. Its original `tdd` fits cheap bug-regression paths; Addy's test/debugging/runtime skills supplement the actual surface.
5. Demonstrate failing-before/passing-after where practical, run nearby regressions, inspect blast radius and prepare a focused PR. Do not opportunistically refactor the system.

Prompt:

> Use poteto-mode's bug-fix workflow for [ticket]. First reproduce [symptom] on [surface] and identify the root cause. Preserve [unrelated behavior]. Use a focused failing regression check where practical, then fix and verify on the same surface with relevant Addy runtime/security checks. Stop if the safe fix requires a material scope expansion. Report the actual before/after evidence and remaining gaps.

**Recovery:** if no reproduction exists, report what is missing and the hypotheses/evidence; do not claim a guessed guard fixes the bug. If production access is needed, obtain authorization and protect private data. Log a broader architecture issue separately.

## 4. Document an unfamiliar codebase

1. Pstack `how` maps ownership, entry points and runtime flow; `why` searches available history/docs for rationale.
2. Matt `domain-modeling` establishes terminology and consequential decision records; `research` gathers cited external evidence where needed.
3. Addy `documentation-and-adrs` and pstack `technical-writing` organize accurate maintainable docs. Use original Matt `writing-for-agents` for concise pointers rather than huge rules files.
4. Validate explanations against actual code, commands and tests. Mark unavailable history and inferred rationale. Do not invent ADR approval or claim a demo was executed when it was only read.
5. Hand proposed code improvements back as separate tickets; do not enter a feature/refactor implementation path for a documentation-only request.

Prompt:

> Use how/why to explain [subsystem], then domain-modeling and documentation-and-adrs to document the actual architecture, vocabulary, public interfaces and test/run paths. Distinguish observed code behavior, supported historical rationale and inference. Scope is documentation only; no application-code restructuring or invented architectural decisions.

**Artifacts:** navigation/architecture map, glossary and justified ADR/doc updates, source references, known gaps. **Recovery:** if a documented command cannot run, record that status and propose the missing prerequisite rather than fabricating output.

## 5. Plan architecture or a design system

### Architecture

1. Pstack `how`/`why` for current constraints; Matt `codebase-design`/`improve-codebase-architecture` for deep-module/interface opportunities.
2. Original pstack `architect with checkpoint` for caller-first alternatives. Explicitly say design only and pause before implementation.
3. Addy `api-and-interface-design`, security and migration/compatibility checks where the design crosses real boundaries.
4. Matt prototype/domain-modeling records the empirical decisions and vocabulary. Update the final spec/tickets only after the key uncertainty settles.
5. Implementation, if subsequently approved, returns to poteto-mode; an architecture report alone does not authorize a rewrite.

Prompt:

> Use architect with checkpoint for [problem], informed by codebase-design and the current source. Compare materially different interfaces/ownership shapes, compatibility and testing surfaces. Use isolated prototypes only for [approved uncertainty]. Produce the design/rationale for approval and stop; do not implement production code.

### UI/design system

1. Verify actual frontend-design and ui-ux-pro-max resources in the active host.
2. Read the existing product system, flows, tokens/components, accessibility and responsive constraints. Use the real skills for intentional direction and applicable UX/stack guidance.
3. Compare prototypes when the interaction/direction is uncertain. Preserve ui-ux-pro-max's actual master/page-override persistence rules; do not force-overwrite an existing system.
4. Feed approved decisions into Matt's spec/tickets; use poteto-mode for production implementation after approval.
5. Verify visible states and real interactions with control-ui / Addy browser checks and screenshot critique. Tests must not fabricate impossible internal UI paths.

Prompt:

> Use frontend-design and ui-ux-pro-max to design [flow] for [audience], respecting [existing system]. Show the relevant states, accessibility/responsive behavior and prototype evidence before production implementation. After approval, poteto-mode should implement Matt's tickets and verify the result visually and functionally.

## 6. Refactor or migrate

1. Pstack `how`/`why` and Matt's architecture/domain skills identify the concrete pain and current behavior. Do not restructure because a generic pattern looks fashionable.
2. Addy `deprecation-and-migration` / `api-and-interface-design` establish real consumer/data compatibility. Internal atomic change and deployed expand/migrate/contract are different cases.
3. Matt records decisions and dependency-aware tickets, including any required compatibility window and final removal gate.
4. Poteto-mode's refactoring/migration path makes bounded changes with characterization/equivalence checks. Addy's simplification/security/runtime checks are targeted, not permission for broad unrelated cleanup.
5. Verify actual callers, stored data and deployed compatibility before any authorized destructive contract/drop step.

Prompt:

> Plan [migration] with Matt's spec/ticket skills and Addy's deprecation-and-migration. Preserve [consumer/data invariants]. Then use poteto-mode to execute the approved sequence, verifying each slice before the next. Do not delete the old contract until its explicit usage/compatibility gate is satisfied and destructive action is authorized.

**Recovery:** when independent slices cannot remain green, document the real integration boundary instead of falsely marking each intermediate state verified.

## 7. Prepare a PR, release or deployment

### PR

Use poteto-mode's existing Opening a PR workflow. Provide approved intent, current patch/evidence and the permitted publication target. Use original deslop/no-comments/interrogate where relevant under project scope and useful-comment rules. Keep the briefing focused on why, what, scope, tradeoffs, blast radius and verification. Stale tests/review against an earlier head are not current evidence.

> Use poteto-mode to review and prepare the PR for [ticket/branch]. Confirm the actual diff matches the approved spec and required tests. Prepare the title/body and evidence now. [Explicitly state whether push/PR creation is authorized.] Do not infer permission to merge or deploy.

### Release

1. Addy CI/CD and Git/versioning for required checks, packaging/version/changelog path.
2. Security and migration skills for relevant release risks and compatibility.
3. Observability for useful privacy-safe telemetry, health and actionable runbooks.
4. Shipping-and-launch for staging/smoke, rollout criteria, rollback steps and post-release verification.
5. Execute only with the release/environment/action grant; record actual results and monitor agreed success signals.

> Use shipping-and-launch with ci-cd-and-automation, observability-and-instrumentation and relevant migration/security skills to assess [release]. Show readiness gaps, required checks, rollout/rollback triggers and commands. Do not deploy until [explicit authorization]. After authorized execution, verify [critical flows/metrics] and record outcomes.

**Recovery:** failed rollout signals trigger the agreed operational decision/runbook, not a blind example command. Confirm data rollback semantics; reverting application code may not restore data.

## 8. Maintain, triage and improve

- **Incoming issues:** Matt triage -> clarify/verify -> approved ticket -> poteto-mode -> per-slice Addy checks.
- **Incident:** relevant observability/debugging/runtime forensics -> evidence/recovery boundaries -> bounded fix -> regression -> documentation/postmortem/follow-up. Do not hide uncertainty or mutate production without permission.
- **Dependencies/security:** Addy security/deprecation/migration; investigate real exposure, compatibility and required checks before upgrade/removal.
- **Docs drift:** original domain/docs/ADRs and verification-upkeep skills; compare docs with current source/runtime, not old agent summaries.
- **Recurring agent mistakes:** Matt retro + pstack correct; propose the smallest useful type/check/test/tooling enforcement rather than endlessly expanding rules.

Prompt:

> Audit [area] using the relevant original maintenance skills. Keep this pass read-only, distinguish proven issues from risks, and propose prioritized bounded tickets. Do not silently install tools, upgrade dependencies or refactor application code. After approval, Matt refines the tickets and poteto-mode executes them with current verification.

## 9. Pause, resume or transfer work

Use Matt handoff, pstack Pause Safely / Session Pickup and Addy context-engineering as appropriate. The deliverable is a durable, redacted pointer to actual state, not a long unsupported narrative.

Include original spec/tickets/blockers; glossary/ADRs; branch/head and in-scope working-tree changes; exact checks/outcomes; running processes/artifacts; unresolved hypotheses; permissions and their scope/version; next ready action. Do not dump secrets or private screenshots into a repository.

> Use handoff and the relevant pstack pause/pickup procedure. Preserve the authoritative artifact links, current Git state, exact verification evidence, blockers and action permissions. On pickup, re-read live state and revalidate stale evidence; do not assume approvals survived an unrecorded scope change.

**Recovery:** missing child reports, dropped panes or absent runtime tools are gaps. Recover task-owned work carefully; never interpret silence as completion or reset unrelated work.
