# The combined workflow

This is a **usage guide for the originals**, not a new skill. [Install the compact combination](install.md) into a project with `python scripts/install.py --project ../my-project --host pi`; it advertises 21 selected originals plus combined setup and keeps 53 helpers on demand, not three full catalogs. [Setup](setup.md) explains discovery and host syntax; [scenarios](scenarios.md) explain entry points and recovery; [validation](validation.md) states what has actually been checked.

## The ownership rule

| Responsibility | Owner |
|---|---|
| What should we build? What does the domain mean? What was decided? | Matt's planning/domain/documentation skills |
| What are the approved spec, acceptance criteria, tickets and blockers? | Matt `to-spec` -> `to-tickets` |
| How do we implement, verify and prepare a reviewable PR? | Original pstack `poteto-mode` and its dependencies/playbooks |
| What quality/security/runtime/operational disciplines apply? | Relevant original Addy skills, before/during/after implementation |

Do not ask Matt implement-spec, poteto-mode and Addy's build controller to independently run the same feature. Do not let a helper create a second authoritative spec or silently replace the ticket graph.

## 0. Configure once per project

Invoke **`setup-agentic-workflow`** once: `/skill:setup-agentic-workflow` in Pi, `/setup-agentic-workflow` in Claude Code/Cursor, or `$setup-agentic-workflow` in Codex. It reads the bundled non-skill Matt/pstack setup references and Addy's actual constraints/context guidance through one shared intake and approved plan. There is no standalone upstream Addy setup skill.

It creates canonical AGENTS.md if missing, preserves existing rules and installer-owned blocks, configures Matt's existing tracker/domain conventions, validates supported pstack model/budget choices, and records Addy's actual commands/quality requirements. Existing answers are reused rather than starting three setup interviews. Global rules, external labels, new tooling and CI changes still need their separate explicit grants; unverified enforcement or unavailable native capabilities remain pending.

Do not run separate Matt/pstack setup passes afterward unless deliberately changing one component. Reuse existing docs rather than introducing another task database. [Setup details and invocation](setup.md#one-setup-invocation).

## 1. PLAN: Matt leads; Addy strengthens the brief

Start with Matt `research` and `grill-with-docs`. The latter composes `grilling` and `domain-modeling`: investigate facts, ask about real user decisions, develop a shared glossary, and record consequential decisions as ADRs. Use `wayfinder` only when the decision tree exceeds one manageable session.

Relevant Addy supplements:

- `idea-refine` / `interview-me`: unresolved purpose, alternatives or underlying user needs. Do not repeat a completed Matt interview just to invoke another skill.
- `spec-driven-development`: requirements/capability completeness checklist. Feed findings into Matt's spec; do not independently publish another authoritative spec.
- `constraint-driven-development`: agree enforceable project constraints and how they are checked. Coverage/performance/accessibility/security budgets are project decisions, not copied universal numbers.
- `source-driven-development`: version-aware official API/library evidence when necessary.

**First gate:** agree scope/non-goals and the boundaries of any design/prototype work. Research and draft documents do not authorize production implementation.

## 2. DESIGN: use the existing design tools before finalizing tickets

Use Matt `codebase-design` for deep-module/interface/seam reasoning and `domain-modeling` for vocabulary/ADRs. Use pstack `how` and `why` to understand the current system. For consequential alternatives, use original `architect` **with its checkpoint requested and a design-only scope**: upstream otherwise continues into implementation by default.

Use Matt `prototype` for a named uncertainty. Keep throwaway code isolated, use disposable data, state the question and observed result, and do not silently ship the prototype. Not every fix needs competing prototypes or an ADR.

Use `frontend-design` and `ui-ux-pro-max` for UI/design-system work, with Addy's `frontend-ui-engineering` / `api-and-interface-design` / `security-and-hardening` where relevant. Preserve an existing product design system and public compatibility constraints.

Return the chosen design and empirical findings to Matt's planning conversation. **Finalize specs/tickets after relevant uncertainty has been resolved**, not before a prototype reveals the actual requirement.

## 3. PLAN: finalize with Matt to-spec -> to-tickets

1. Invoke original `to-spec` to synthesize settled decisions. It is not another interview. Review expected behavior, exclusions, chosen interfaces and test seams.
2. Invoke original `to-tickets` for independently verifiable vertical slices and real blocking edges.
3. Review granularity, blockers and acceptance criteria. Publish to the configured tracker only under the appropriate grant.
4. Keep one authoritative task/status source. If using GitHub, a local index can link issues without becoming a competing live status board.

**Implementation gate:** approve the final spec/design/tickets and execution scope. An approval can cover several ready slices; it need not mean asking before every file edit or local commit. A substantial change in requirements returns to this gate.

## 4. HANDOFF: pass artifacts to original poteto-mode

Give the implementation session:

- Approved spec and ticket links/full bodies/comments.
- Blockers, ready frontier and intended delivery boundaries.
- Glossary, relevant ADRs, architecture/prototype outcomes and UI system.
- Written constraints, actual test commands/surfaces, baseline failures and required evidence.
- Scope/non-goals, applicable Addy checks and action permissions.

Copyable prompt:

> Use poteto-mode for implementation. The approved spec is [spec] and the tickets are [tickets]. Read their full bodies/comments and the glossary/ADRs at [paths]. Preserve these artifacts as the authority; do not replace Matt's plan. Work the ready frontier, one bounded verifiable ticket at a time. Use the relevant Addy skills for quality constraints, test-first behavior where practical, security and real browser/runtime checks. Verify each implemented slice before starting dependent work. Update evidence and relevant docs; stop on material ambiguity, required-check failures or missing capabilities. Prepare focused PRs with pstack's Opening a PR workflow. Publication, merge, deployment and destructive actions require their own grants.

A fresh implementation context per ticket is useful when it can be grounded cheaply. Use original `handoff` or pstack pause/pickup when continuity would otherwise be lost. Do not rely on a compacted chat to preserve unrecorded decisions.

## 5. BUILD + TEST: one pstack-owned feedback loop per ticket

```text
read approved ticket/spec/constraints
  -> understand affected system / name data shape
  -> reproduce or write a meaningful behavior check
  -> poteto-mode implements bounded change
  -> run affected tests and the relevant real surface
  -> apply relevant Addy checks / pstack review
  -> fix verified findings and rerun affected checks
  -> record result / update docs and allowed ticket state
  -> next ready ticket or focused PR
```

pstack's stock `tdd` is selective, primarily cheap bug regressions. For feature logic use Addy's original `test-driven-development` where appropriate. Prefer a good executable check over a brittle test that only proves its own mocks. Preserve failures and independently known expected results.

| Change | Original supplement to the pstack loop |
|---|---|
| UI/browser | `browser-testing-with-devtools`, `frontend-ui-engineering`; control-ui; actual UI dependencies |
| CLI/TUI | control-cli plus project-native PTY/test harness |
| Auth, permissions, secrets, untrusted data/tool output | `security-and-hardening`; relevant adversarial review |
| API/schema/contracts | `api-and-interface-design`, compatibility and integration checks |
| Performance | `performance-optimization`, pstack `benchmark-checklist`; real baseline and comparable runs |
| Database/public consumer migration | `deprecation-and-migration`; compatibility and rollback evidence |

Affected tests while iterating; broader regression/build/runtime checks at integration and before delivery. Compilation alone is not correctness. BLOCKED/NOT RUN/INCONCLUSIVE are not PASS. Do not weaken tests or thresholds to manufacture green.

Parallel work is conditional: separate task-owned branches/worktrees and disjoint write ownership, true dependency frontier, centralized integration. If the host cannot supply delegation/independent review, disclose that; do not fabricate multiple models or silently replace required review with self-review.

## 6. TEST + PR: pstack remains the delivery owner

Use pstack `interrogate` / `blast-radius` as appropriate and Addy `code-review-and-quality` for relevant axes. Matt `code-review` is optional for explicit standards/spec checking: its upstream HEAD-based diff can miss working-tree changes, so make the review target explicit and include all intended work.

Pin the reviewed base/head/patch. Recheck accepted findings against source/runtime evidence. Changes after review invalidate affected verdicts and checks.

Let poteto-mode use its original Opening a PR playbook, including its briefing structure and its real deslop/comment-review dependencies. Keep project-approved useful rationale comments; do not turn cleanup into unrequested redesign. Keep the PR small and independently verifiable where possible. Independent PRs are the default; use a stack only for genuine dependencies.

Prepare the title/body/evidence locally. Publish only with the push/PR grant. A draft versus ready PR is a deliberate project/user decision, not authority inferred from upstream's ready-by-default rule. **Opening a PR neither merges nor deploys it.**

## 7. DEPLOY: Addy covers actual release safety

Use originals as applicable:

1. `ci-cd-and-automation`: required checks and build/release path.
2. `git-workflow-and-versioning`: approved version/tag/changelog/package actions.
3. `security-and-hardening`: unresolved risks and release-relevant security evidence.
4. `deprecation-and-migration`: safe compatibility, consumer/data transitions and destructive-step boundaries.
5. `observability-and-instrumentation`: useful, privacy-safe telemetry and verified alerts/runbooks.
6. `shipping-and-launch`: staging/smoke, rollout, rollback triggers/steps and post-release evidence.

Thresholds, environments and commands must fit the project. Do not copy an example canary schedule or universal percentage blindly. Require a named deployment/release grant. Record actual results, and never run a rollback/data deletion merely because a sample command appears in a checklist; agree the operational authority first.

## 8. MAINTAIN: feed evidence back into the same cycle

- Matt `triage` makes incoming work actionable; `retro` proposes improvements.
- Addy observability/debugging supports incidents; security/deprecation/migration supports dependency and lifecycle work.
- Matt domain/ADR skills and Addy `documentation-and-adrs` keep explanations current.
- Pstack `correct` / verification upkeep can turn recurring mistakes into checks, after proposed policy/tool changes are approved.

A maintenance finding becomes a bounded Matt brief/ticket and returns to poteto-mode for implementation. A read-only audit does not silently become a refactor.

## Completion and recovery

A ticket is complete only when its requested behavior and required checks have evidence, relevant docs are updated, and unresolved gaps are disclosed. A release is complete only after its real operational verification, not just CI or merge.

When blocked, preserve the original ticket/spec, current head, repro/check output, attempted hypotheses and missing permission/tool. Use an original handoff skill/playbook. Resume by reading real files/Git state and revalidating stale evidence. Never infer a still-valid permission from a missing conversation.
