# Maks Agentic Workflow: compose the existing skills

**Status: corrected following the user's clarification.** The former proposal to write 23 replacement skills was a misunderstanding and is withdrawn. This project combines the **actual upstream skills**, retaining their names and implementations. Our additions are workflow documentation, handoff instructions, project-level operating rules and installation/provenance information, not a replacement skill suite.

## 1. The intended combination

```text
MATT: discover -> document decisions -> spec -> dependency-aware tickets
                                |
                  approved spec/ticket handoff
                                |
PSTACK: poteto-mode -> implement one ready ticket -> test/verify
                                |                       ^
                                +-> relevant Addy checks+
                                |
                  review -> next ticket / focused PR
                                |
ADDY: release readiness -> authorized deploy -> observability/maintenance
```

**Addy's skills are cross-cutting, not merely a final phase.** Requirements and quality constraints inform planning; security informs design/build; browser/runtime checks verify each relevant slice; CI/CD, migrations, observability and release readiness cover delivery and ongoing operation.

No new branded skill names, combined replacement SKILL.md files, custom workflow engine or wrapper skill. Native package namespaces may distinguish existing skills without changing their original identity.

## 2. Who owns what

`Matt / skill-name`, `pstack / skill-name` and `Addy / skill-name` below identify the source, not literal cross-host command syntax.

| Work | Original skills used | Ownership and handoff |
|---|---|---|
| Configure project documentation/tracker | Matt `setup-matt-pocock-skills` | Use its existing tracker/domain-doc conventions; inspect and approve setup changes first |
| Investigate and clarify | Matt `research`, `grill-with-docs`, `grilling`, `domain-modeling`; `wayfinder` for large uncertain work | Matt owns planning discussion, glossary and consequential ADRs |
| Requirements and quality bar | Addy `idea-refine`, `interview-me`, `spec-driven-development`, `constraint-driven-development`, when useful | Supply questions/checklists/constraints to Matt's planning; do not create a competing authoritative spec or repeat an already settled interview |
| Architecture and prototypes | Matt `codebase-design`, `prototype`, `improve-codebase-architecture`; pstack `how`, `why`, `architect` | Use before finalizing affected spec/tickets. Ask original `architect` for its supported checkpoint and design-only scope, since its default continues into implementation |
| UI/design system | Actual `frontend-design` and `ui-ux-pro-max`; relevant Addy `frontend-ui-engineering` | Preserve existing UI dependencies and design-system decisions; no homemade substitute |
| Final spec | Matt `to-spec` | Synthesize the settled conversation/design into the authoritative spec, using the configured tracker/docs |
| Ticket breakdown | Matt `to-tickets` | Approve independently verifiable slices and true blockers, then publish under the appropriate permission |
| Implement and test tickets | pstack `poteto-mode` and its actual feature/bug/refactor playbooks and dependencies | **pstack owns execution.** Read Matt's approved artifacts, work the ready frontier, test/verify each slice, and stop on unresolved scope or required verification failures |
| Test discipline and runtime checks | pstack's existing verification/TDD path; Addy `test-driven-development`, `browser-testing-with-devtools` when relevant | Supplement per-ticket execution with the appropriate original test skill; stock pstack TDD is intentionally selective, so it must not be mistaken for a universal feature-test guarantee |
| Security | Addy `security-and-hardening`; relevant pstack adversarial review | Apply proportionately during design, implementation and review, not only after all code is written |
| Interfaces and performance | Addy `api-and-interface-design`, `performance-optimization`; pstack `benchmark-checklist` | Use when the ticket affects those concerns; feed evidence and consequential decisions back to Matt's docs |
| Review and PR | pstack `interrogate`, `blast-radius` and the Opening a PR playbook through `poteto-mode`; Addy `code-review-and-quality` as relevant | Keep pstack's implementation/PR ownership. Matt `code-review` can provide a separate spec/standards check when useful; Matt `pr` is optional, not a second PR controller |
| CI/CD and release | Addy `ci-cd-and-automation`, `git-workflow-and-versioning`, `shipping-and-launch` | PR creation is not deployment. Agree release checks, environment, rollout and rollback before authorized execution |
| Migrations | Addy `deprecation-and-migration` | Feed compatibility/expand-contract requirements into planning and execution; do not blindly inherit same-wave deletion for deployed consumers |
| Observability and incidents | Addy `observability-and-instrumentation`, `debugging-and-error-recovery` | Include telemetry/runbooks before release and use real evidence after release |
| Documentation and maintenance | Matt `domain-modeling`, `triage`, `retro`, architecture skills; Addy `documentation-and-adrs`, relevant security/migration/observability skills; pstack `correct`, verification upkeep | Keep existing documentation/tracker authoritative; updates and follow-ups go back into the same planning/execution cycle |
| Pause and resume | Matt `handoff`; pstack Pause Safely / Session Pickup playbooks; Addy `context-engineering` | Carry links to actual spec, tickets, glossary/ADRs, branch/head, checks and remaining permissions; revalidate live state |

Matt `implement`/`implement-spec` and Addy's build orchestration are **not the default execution path** in this combination. They would compete with the explicitly chosen `poteto-mode` ownership. Their presence upstream is not a reason to invoke all three implementers.

## 3. The Matt -> poteto-mode handoff

Provide existing artifacts, not a rewritten plan:

- Approved spec reference and relevant comments/acceptance criteria.
- Ticket references, real blocking edges and the currently ready frontier.
- Domain glossary, applicable ADRs, architecture/prototype decisions and design-system references.
- Agreed test surfaces/commands, Addy's written quality constraints, required runtime/security/eval checks and known baseline failures.
- Scope/non-goals and permission boundaries for publishing, merge, deployment and destructive work.

Example execution request, using the original skill name:

> Use poteto-mode to implement the approved spec at [reference] through the tickets at [references]. Preserve Matt's spec and dependency graph; do not replace them with a new plan. Start with a ticket whose blockers are complete. For each ticket, implement the bounded slice, run its relevant tests and real runtime checks, apply the relevant Addy security/quality/browser checks, fix findings, and rerun affected checks before moving on. Update evidence and consequential docs. Stop for material scope changes or unavailable required evidence. Follow pstack's PR preparation workflow; obtain the configured permission before publishing, merging or deploying.

This is a handoff prompt/runbook, **not a new skill**. The final guide will show host-correct invocation and worked examples rather than pretending this prose alone supplies missing host tools.

## 4. Per-ticket execution loop

1. Read the original ticket, spec criteria, relevant glossary/ADRs and project constraints.
2. Confirm blockers are complete and identify the observable behavior/check for this slice.
3. Let original `poteto-mode` select and execute its appropriate playbook.
4. Use test-first/failing-before evidence where practical; include appropriate Addy tests/runtime checks for the affected surface.
5. Run relevant security, architecture, performance or compatibility checks rather than every checklist on every change.
6. Resolve verified findings and rerun affected checks. A skipped, blocked or inconclusive check is not a pass.
7. Record actual results and update affected docs/ticket state under the allowed permissions.
8. Proceed to the next ready ticket or pstack PR preparation. Do not wait until the entire spec is implemented to test its first slice.

For small bugs, the same ownership applies with a short scope/repro instead of manufacturing a full product PRD. For documentation-only requests, use the original research/architecture/documentation skills without entering an implementation playbook.

## 5. Keep the skills original; put coordination outside them

Keep upstream skill files and required references/scripts/data intact at pinned revisions, including applicable notices. Do not flatten source trees or rename `tdd` into a custom branded replacement to conceal a discovery problem.

Document project-specific scope and permission rules in a concise project instruction file and the workflow guide. In particular, reconcile pstack's default autonomy, architecture auto-implementation, comment cleanup and PR readiness with the user's agreed gates **without silently rewriting poteto-mode**. If a host cannot honor the composition as documented, report the limit rather than presenting a homemade implementation as upstream.

The installation plan must handle actual dependencies, not just copy a single poteto-mode file:

- pstack's referenced skills, principles, playbooks, agents and resources.
- Explicit external dependencies such as cursor-team-kit controls/deslop where the chosen host supports/requires them.
- Matt's composed skills and tracker/domain-doc references.
- Addy's root-shared references, which individual-folder installs can otherwise strand.
- Original `tdd` and other name collisions: use supported package namespaces or isolated discovery/explicit source selection. Do not claim `Matt:tdd` is a real command unless that host actually provides it.

Pi, Claude Code, Codex and Cursor remain the intended supported environments. Original skill readability does not guarantee that Cursor-specific subagent/model/MCP calls execute in Pi or Codex. Document and test the actual host paths/capabilities; do not promise identical automation or build a new bridge engine by default.

## 6. What this repository contains

- A quick-start README and six-phase workflow map using the original skill names.
- The complete source comparison/catalog, corrected to distinguish research from the withdrawn replacement proposal.
- A full scenario handbook: new project, feature, bug, architecture, UI/design system, documentation, migration, release, maintenance and handoff.
- Concrete handoff prompts showing Matt -> poteto-mode and where each Addy skill is used.
- Installation/source/version/license information and, if authorized, the selected actual upstream packages/resources in a namespace-safe layout.
- Validation of discovery, resources, handoffs, per-ticket checks and permission boundaries on available hosts, with truthful limitations.

No `maw-*` skill collection, custom shared workflow runtime or custom project schema. The user's subsequent request authorizes a small project-local installer, not a new orchestration framework.

## 7. Packaging confirmed: originals + guide

The user selected **Originals + guide**. Pinned original package files are now under `upstream/`, with a byte-identical `.agents/skills/` discovery view containing Matt 22, pstack 58, Addy 22 and cursor-team-kit 3. Shared Addy resources, original pstack agents/playbooks and the actual upstream-generated Claude adapter are included; names/content are not rewritten. `sources.lock.json` and checksums record provenance.

The source/audit collection is not the consumer payload. The subsequently requested [compact installation command](../guide/install.md) installs only 22 advertised originals plus 54 required/used helpers outside discovery; it never copies all three catalogs or the repository's 105-entry view.

The [full workflow](../guide/README.md), [scenario recipes](../guide/scenarios.md), [setup/host limitations](../guide/setup.md) and [validation record](../guide/validation.md) are available. Collection integrity and read-only routing probes are distinct from real application/host-runtime acceptance. No files have been committed or pushed, and no global configuration, deployment or automation was enabled.
