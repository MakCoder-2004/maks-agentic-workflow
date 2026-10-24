# Confirmed requirements

**Status:** corrected after the user clarified the intended composition. The earlier interpretation as a new 23-skill suite was rejected. Preserve the original upstream skills and coordinate their use; do not re-author or rebrand them.

## Purpose and priorities

Create Maks Agentic Workflow in this repository by combining the existing skills: Matt owns discovery, planning documentation, specs and dependency-aware tickets; pstack's actual `poteto-mode` owns implementation, per-slice testing/verification and PR preparation; Addy's actual skills supply broad lifecycle coverage before, during and after execution.

Primary priorities, in order of emphasis: **correctness and maintainability**, and **planning and traceability**. The suite should be practical and risk-scaled, not a mandatory 121-step ceremony. "Optimal" means best fit to these requirements, subject to validation, not a universal performance claim.

## Confirmed decisions

| Area | User decision |
|---|---|
| Lifecycle | Plan, Design, Build, Test, Deploy, Maintain; support iteration between phases |
| Hosts | Pi, Claude Code, Codex and Cursor from version one |
| Packaging | User selected Originals + guide: include actual upstream packages/resources and original names, plus coordinated workflow documentation; document host discovery, dependencies and limitations |
| Composition | One coordinated workflow using original skills, not new replacement skills or a homemade router. Matt plans/specifies/tickets; poteto-mode implements/tests/prepares PRs; Addy supplies lifecycle disciplines |
| Software coverage | Web/backend, desktop/mobile, CLIs, libraries and developer tools; discover the stack rather than prescribing one |
| Approval | Scope/spec and design/ticket approval before implementation; publishing, merge, deployment and destructive actions separately authorized |
| Rigor | Risk-scaled lightweight, standard and high-risk paths |
| Documentation | Linked core repo docs: brief/spec, acceptance criteria, domain glossary, consequential ADRs, architecture map, test evidence and handoff; update affected docs without duplicate truth |
| Tasks | One authoritative per-project tracker adapter, not a universally forced tracker |
| Testing | Evidence-first TDD; failing-before/passing-after regressions when practical; appropriate integration/runtime/UI checks; missing/inconclusive checks are never passes |
| Architecture | Context-driven: deep modules, explicit contracts, sound data models, minimal justified abstractions; no universal folder/layer pattern |
| UI/design | Use the actual `frontend-design` and `ui-ux-pro-max` skills |
| UI distribution | Checked explicit dependencies, not bundled or rebranded copies; do not silently install or replace them |
| Git | Independent task-owned branches/worktrees and small independently landable PRs; centralized integration; stacks only when dependencies justify them |
| Delegation | Selective independent work/review; isolated write ownership; sequential fallback with an explicit independence limitation |
| Deployment | Configurable real release path: CI, versioning, staging/smoke, migrations, rollout/rollback and post-release verification; execution needs its own authorization |
| Maintenance | Issues/incidents; architecture/dependencies/security; documentation/workflow learning |
| Onboarding | Existing-project read-only assessment first; approve proposed configuration/docs changes; no surprise application-code restructuring |
| Bug scope | Bounded root-cause fix within approval; propose wider restructuring separately; stop if a safe fix requires material scope expansion |
| Comments | Keep concise non-obvious intent, invariants, public contracts and operational hazards; remove stale/redundant narration; consequential rationale belongs in ADRs |
| Handbook | Layered quick start, lifecycle map, detailed scenario recipes, exact prompts, artifacts, gates, recovery, worked examples and upstream comparison/adaptation matrix |
| Validation | Static + behavioral checks, representative scenarios, safety/approval cases, selected no-suite comparisons; label untested hosts honestly |
| Pilot scenarios | Three: new product/feature, existing-project bug, architecture/documentation |

## Required scenario coverage

The handbook must explain how to enter, proceed, stop, recover and finish each scenario:

1. New project from an ambiguous idea.
2. New feature in an existing project.
3. Reproducible bug/issue fix and hard-bug diagnosis.
4. Read-only codebase understanding and accurate documentation.
5. Architecture/domain/API design and improvements.
6. Design-system/UI work using the two actual UI dependencies.
7. Behavior-preserving refactoring and compatibility-aware migration.
8. Release, deployment, rollback planning and post-release verification.
9. Issue triage, incidents, dependency/security work, documentation drift and retrospectives.
10. Pause/resume, handoff, fresh-context tickets and recovery from unavailable tools or failed agent work.

## Authority interpretation

- Approval has a scope and action, not merely a positive-sounding sentence. Record the approved document/version or exact task boundary and any exclusions.
- Production implementation waits for approved scope and design/plan. Research, drafts and explicitly scoped throwaway prototypes are different activities; a prototype is not permission to change production behavior.
- Once implementation is approved, local task-owned edits, tests, branches/worktrees and ordinary commits can occur within that scope. This is not a requirement to ask before each commit.
- Separate action grants cover external issue/label publication, push/PR publication, merge, release/deployment and destructive operations. A grant may cover a clearly named batch; it is not inherited from unrelated earlier work or broadened by delegation.
- Material uncertainty, scope expansion, unavailable required evidence or conflicts with repository policy are surfaced rather than silently worked around.
- A missing test tool, failed child agent, unread source or stale reviewer verdict never becomes a pass.

These operational interpretations belong in project instructions and the [original-skill workflow](workflow-design.md), not rewritten upstream skills. Matt's and Addy's alternative implementers are not the default execution controllers.

## Not included by default

- An autonomous scheduler/daemon, standing multi-agent fleet, persistent goal engine or automatic merge service.
- Cursor-only automation, transcript mining, mandatory multi-model panels or mandatory parallelism for every task.
- Automatic deployment-provider provisioning, global tool installation, credential collection, secret persistence or production mutation.
- Universal numerical test-coverage/performance/SLO thresholds or prescribed architecture layers.
- New or rebranded replacement skills, a custom workflow engine/runtime/schema, frozen utilities treated as maintained dependencies, or the two UI skills rewritten into lookalikes. The subsequently requested project-local installation command is allowed; it installs only the combination rather than all three catalogs.
- Simultaneous competing implementation controllers: use poteto-mode, not Matt implement-spec plus Addy's build orchestration for the same work.
- Claims that all four hosts have passed live tests merely because they support the Agent Skills format.

## Current repository facts

At the user's explicit request, local Git was initialized with branch `main`, and the private GitHub repository [MakCoder-2004/maks-agentic-workflow](https://github.com/MakCoder-2004/maks-agentic-workflow) was created with `origin` pointing to it. Creating this repository did not authorize pushing planning files or publishing the suite.

The replacement-skill proposal is withdrawn. Actual pinned upstream packages remain as source/audit archives. The user then explicitly requested a reusable, context-conscious installer: `scripts/install.py` installs 22 original entry points and 54 required/used helpers outside discovery, with workflow guidance and ownership/resource checks. It does not install all three catalogs. No replacement skills, global setup hooks, application code, commits or pushes are added by the installer.

## Confirmed packaging and validation boundary

The user selected **Originals + guide**. The repository now includes the original sources and 105 curated original skill entries; [setup](../guide/setup.md) records the exact selection, dependencies and host limits. [Validation](../guide/validation.md) distinguishes collection checks/read-only routing probes from unperformed application and host-runtime acceptance. Do not recreate the rejected replacement-skill proposal. Publication remains separately authorized.
