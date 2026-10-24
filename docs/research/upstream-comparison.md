# Upstream workflow comparison

**Status:** completed source research, with the composition corrected after the user's clarification. Use actual upstream skills: Matt plans/specifies/tickets, original pstack poteto-mode implements/tests/prepares PRs, and Addy's original skills provide cross-cutting lifecycle coverage. The replacement-skill proposal is withdrawn. No combined-workflow behavioral efficacy has been measured yet.

## Summary

Use **Matt's planning and durable domain knowledge**, **pstack's design/build/runtime-evidence and PR practices**, and **Addy's operational breadth**. Reconcile their conflicting defaults rather than installing three competing workflow controllers.

This is a best-fit design for the confirmed requirements, not a claim that one universally optimal workflow exists. More agents, longer specs, more tests, or stricter ceremony do not automatically produce better engineering.

| Source | Strongest contribution | Principal limitation for this project |
|---|---|---|
| Matt Pocock | Decision interviews, shared vocabulary, ADRs, spec synthesis, dependency-aware vertical tickets, deep-module design, handoffs | Limited production release/operations coverage; some hard-coded harness assumptions; inconsistent side-effect gates; experimental/frozen skills need separation |
| pstack | Caller-first architecture alternatives, ownership/isolation, real-surface verification, measurement discipline, concise reviewable PRs, pause/resume | Code-first/autonomous defaults conflict with explicit planning gates; compulsory delegation can overfit small work; Cursor/tool/model assumptions; PR-stack shipping is not production deployment |
| Addy Osmani | Broad lifecycle coverage: requirements, quality constraints, security, browser/runtime checks, CI/CD, observability, migrations, release readiness | Larger/overlapping guidance; generic thresholds and examples need contextualization; shared-reference installation gap; workflow/tool availability must not be assumed |

## Research scope and method

The [complete inventory](skill-inventory.md) accounts for **121 canonical skill files**, once each:

| Source | Pinned revision | Skill files | Status |
|---|---|---:|---|
| `mattpocock/skills` | `5beb35b040e3de97e54fa9e386d7e42d15c295c2` | 38 | 27 promoted, 7 in-progress, 4 frozen/misc |
| `cursor/plugins/pstack` | `9580c23696ac8d7abed0c166f2f9918800afb819` | 58 | 34 non-principle + 24 principle skills; no invented experimental labels |
| `addyosmani/agent-skills` | `aeac41d4d005999432bb7312f7ff06383a91d59d` | 25 | One documented catalog |

All skill bodies, all 23 pstack playbooks, and selected supporting docs, references, agents, fixtures and scripts were supplied to isolated, tool-disabled research runs using `openai-codex/gpt-6-luna` with high reasoning. The parent review checked source paths/counts, read critical instructions directly, and reconciled report errors. Upstream instructions were treated as data, never executed. Local tooling was used to inspect and validate sources, not to run upstream hooks or setup commands.

A generated report is not an authority. In particular:

- Preliminary report inventories omitted Matt's setup skill and pstack's swarm; both are included in the corrected inventory.
- A preliminary pstack table mixed playbooks with skills and repeated principles; the published inventory enumerates canonical paths instead.
- Matt's `dependency-cruiser.config.cjs`, pstack's decision-log TSV, and pstack's watcher wrapper **exist**. Their absence from a selected audit input did not demonstrate an upstream defect.
- Static instructions, tests and eval fixtures show intended behavior and coverage, not proof that agents follow them reliably.
- Research observed source-design tradeoffs. It did not benchmark the three workflows on real projects.

## 1. Matt Pocock

### Strengths

1. **Discovery is a real activity.** `grilling` separates facts an agent should investigate from decisions only the user owns, works through prerequisite-aware rounds, and waits for shared understanding. `grill-with-docs` composes questioning with domain modeling. This directly supports the requested planning process.
2. **Knowledge artifacts have distinct jobs.** A glossary establishes project language; ADRs record consequential decisions; a spec captures agreed behavior; tickets define execution slices. These are more useful than continually enlarging a generic agent rules file.
3. **Specs and tickets are not the same artifact.** [To Spec][matt-spec] synthesizes the conversation instead of conducting another interview. [To Tickets][matt-tickets] turns settled work into independently verifiable vertical slices, records blockers, and explicitly asks for approval of the breakdown.
4. **Architecture focuses on leverage, not a universal layer diagram.** `codebase-design` frames deep modules as capability behind a small understandable interface. Interface alternatives and seam selection can expose a poor design before implementation.
5. **Testing targets external behavior.** `tdd` rejects tautological expected values and implementation-coupled tests. `diagnosing-bugs` demands a reproduction that can actually fail, hypothesis testing, and regression evidence.
6. **Continuity is deliberate.** `handoff`, phase-boundary guidance and agent-facing writing techniques support fresh-context tickets without losing decisions.

### Weaknesses and integration risks

- **The PR skill is not deployment.** A PR-body format and human-only setup wizard do not supply staged release, monitoring, rollback, incident command, or a complete dependency-maintenance loop.
- **Spec verbosity is not traceability.** [The spec template][matt-spec] requests a long, extensive user-story list. That can be useful for product behavior, but is an awkward universal form for a rename, incident, migration, or architecture-only task. Prefer explicit requirements with acceptance criteria and non-goals; use user stories where they add meaning.
- **Review can miss the intended work.** [Code Review][matt-review] reviews `git diff <fixed-point>...HEAD`, while `implement` calls review before committing. That combination can exclude uncommitted changes. The new review contract must pin the base and exact head, include staged/unstaged/untracked in-scope changes when relevant, and invalidate an old verdict after patch changes.
- **Approvals are not consistent across the catalog.** Some skills ask before publication, while implementers can commit and orchestrators can transition issues/PRs. Our explicit action-grant policy must override those defaults.
- **Harness vocabulary is not portable by itself.** Literal Skill-tool calls, Claude-specific agent invocation, and setup's preference for editing an existing `CLAUDE.md` need host-neutral adaptation.
- **Strong heuristics can become dogma.** Exact terminology bans, always-approved test seams, a single test-surface ideal, or automatic deepening should not replace project context. Preserve useful rationale comments and public compatibility contracts.
- **Do not adopt the whole repository indiscriminately.** The in-progress writing/coordinator skills and frozen repo-specific utilities are inventoried but are not maintained production dependencies for this suite. The frozen Git hook is not a general security boundary.

### Contribution

Use Matt's actual `grill-with-docs`, `domain-modeling`, `to-spec`, `to-tickets` and supporting planning/documentation skills. Their outputs are the authoritative planning handoff to original `poteto-mode`. Do not rewrite these as new branded skills or use Matt's implementers as a second execution controller.

## 2. pstack

### Strengths

1. **Design begins with real callers and data.** [Architect][pstack-architect] grounds the surrounding system, writes usage before signatures, compares structurally different candidates, and carries rationale into implementation. This complements Matt's deep-module vocabulary.
2. **Implementation ownership is explicit.** [The feature playbook][pstack-feature] names the data shape, scope, success criteria and independent workstreams. Isolation of writable state is directly useful for task-owned branches/worktrees and centralized integration.
3. **It distinguishes evidence from proxies.** Actual app/CLI/browser behavior matters; compilation alone is not correctness. Reproducing a bug and verifying the fix on the same surface reduces false confidence.
4. **Performance claims receive scrutiny.** `benchmark-checklist` and `explain-the-number` ask whether the measured work happened, what limits it, and whether repeatability/end-to-end relevance support the claim.
5. **PRs are reviewer-oriented.** [Opening a PR][pstack-pr] structures the briefing around why, changes, scope, tradeoffs, blast radius and verification. Evidence is concise in the body, with larger artifacts linked separately.
6. **Pause/resume is operationally concrete.** The pickup/pause playbooks distinguish inherited claims from revalidated state, describe ongoing work, and preserve a cold-start handoff.
7. **Repeated mistakes can become checks.** `correct` and `encode-lessons-in-structure` favor structural safeguards over endlessly appending instructions.

### Weaknesses and integration risks

- **Default authority differs from yours.** [Poteto Mode][pstack-mode] explicitly allows reversible external actions without asking. [Architect's Agree phase][pstack-architect] proceeds to implementation unless a checkpoint was requested. Both must be overridden by approved scope/spec and design/plan gates.
- **Depth can become compulsory ceremony.** [The feature playbook][pstack-feature] mandates code delegation and sometimes arena-style alternatives. That can be sensible for consequential work but is unsuitable as a universal rule for a small fix or a host without delegation.
- **Planning is deliberately secondary.** The README says code is the best spec and planning is not the default. We want the reverse relationship for uncertain requirements: discover, prototype where useful, document the settled design, then build.
- **It has real external dependencies.** The default workflow references `cursor-team-kit` controls and `deslop`, Cursor built-ins, MCPs, configurable model slugs and subagent environments. Copying pstack's Markdown does not install those capabilities.
- **Ready PRs, stacks and resets are not universal policy.** [Opening a PR][pstack-pr] defaults to ready-not-draft PRs and contains hard-reset/recovery advice. The combined suite must preserve unrelated work, isolate task-owned changes, respect explicit publishing authority, and use independent PRs by default. No unconditional reset/clean/delete recipes.
- **Comment removal can overreach.** [No Comments][pstack-comments] and Comment Sicko can turn comment review into refactoring. Retain concise non-obvious rationale, invariants, public contracts and hazards; remove stale/redundant narration, not documentation by default.
- **PR-stack shipping is not an infrastructure release lifecycle.** Verified merge sequences do not replace environment-specific release, data-migration compatibility, rollout, monitoring and rollback.
- **Formal verification is specialized.** Statechart/model-checking workflows can help bounded races and state machines, but require tooling and faithful models. They are optional references, not claims of whole-system proof.

### Contribution

Use the actual `poteto-mode` as the implementation/testing/PR owner, with its real supporting skills, principles, playbooks, agents and resources. Invoke the appropriate original architecture/debugging/measurement skills as needed. Preserve the package rather than extracting its ideas into a replacement router; project-level instructions define the approved scope and permission boundaries.

## 3. Addy Osmani

### Strengths

1. **Operational coverage fills the largest gaps.** [Shipping][addy-ship], [Observability][addy-observability], CI/CD, security and deprecation/migration cover concerns beyond a successful local build or merged PR.
2. **Requirements and constraints precede implementation.** Spec-driven development includes scope/capability-map approval; [Constraint-Driven Development][addy-constraints] turns quality expectations into a written, enforceable contract and guards against weakening tests/checks to obtain green.
3. **Contracts include failure and compatibility.** [API and Interface Design][addy-api] contributes input boundaries, errors, idempotency and compatibility semantics rather than only type signatures.
4. **Runtime and source honesty are explicit.** Browser verification covers DOM/console/network; source-driven work checks relevant official versions and treats retrieved content as untrusted.
6. **Restartable context is well specified.** [Context Engineering][addy-context] captures scope, actual Git state, decisions, verification, risks and approvals rather than relying on conversation memory.
7. **Evaluation distinguishes structural checks from agent behavior.** Its eval documentation recognizes that fixtures, routing approximations and model-executed traces test different things. We should preserve that distinction.

### Weaknesses and integration risks

- **Broad guidance overlaps.** Multiple skills prescribe parts of planning, testing, review and delivery. Without one authority/policy model, agents can create duplicate plans or enforce inconsistent gates.
- **Generic numbers are not project requirements.** [TDD][addy-tdd] includes a test-pyramid ratio; release/performance/security examples supply thresholds and budgets. These are prompts to establish project constraints, not universal release criteria for every stack.
- **Examples are often web/TypeScript-oriented.** Guidance must discover the actual language, platform, test seam and packaging surface. A desktop packaged-runtime bug or Python data job cannot be verified by a web-only checklist.
- **Routine instructions do not grant authority.** Incremental build/commands prescribe commits and some samples show pushes/deploys. Our policy permits scoped local work after implementation approval, but requires separate permission for publishing, merge, deployment and destructive operations.
- **Individual installation can lose references.** The [getting-started guidance][addy-start] documents dependencies on root-shared `references/`. Installing one skill folder can strand those links. Our distribution must include its runtime dependency closure and validate it in a relocated install, not only in the source checkout.
- **Do not silently install specialist tools.** Chrome DevTools MCP, fresh-context reviewers, CI accounts and package tools are capabilities to detect/configure, not assumptions every project satisfies.

### Contribution

Use Addy's actual requirements/quality-constraint, security, interface/runtime/browser, CI/CD, release/rollback, observability, migration, context and documentation skills at relevant workflow points. Feed requirements into Matt's authoritative planning artifacts rather than creating competing specs; keep poteto-mode in charge of implementation.

## Conflict resolutions for the combined suite

| Conflict | Chosen resolution |
|---|---|
| Code-first autonomy vs documented planning | Research/grill and a scoped brief first; prototype/design uncertainty before the final spec/tickets; approve the final design/plan before production implementation |
| Multiple overlapping workflow controllers | Keep original skills and one documented ownership sequence: Matt planning -> poteto-mode execution/testing/PRs, with original Addy lifecycle skills used at the relevant points; no replacement router or new engine |
| Strict TDD vs no practical test path | Evidence-first TDD; failing-before/passing-after regression checks when practical, explicit alternative evidence and remaining gaps otherwise |
| Reviews over stale or incomplete diffs | Pin base and exact patch/head; cover relevant working-tree changes; revalidate findings and re-review changed evidence |
| Compulsory fan-out vs constrained hosts | Delegate useful independent work only; one writer per task-owned artifact; disclose sequential fallback and reduced independence |
| Delete comments / redesign everything | Preserve useful rationale; bounded root-cause fixes; broader redesign requires scope approval |
| Delete legacy APIs in one wave vs live consumers | Internal changes may migrate atomically when safe; public/deployed contracts and data migrations require compatibility-aware expand/migrate/contract |
| PR-ready vs deployed | Separate PR preparation/publication, merge, release deployment and post-release validation |
| Universal numerical thresholds vs project reality | Agree budgets, required checks, baselines and applicability per project; never lower the bar silently |
| Shared docs / copied references vs broken installs | Single canonical source, explicit dependency closure, relocated-install checks and manifest ownership |
| Retrospective lessons vs endless rules | Prefer architecture/types/checks where justified; retain concise rationale and approve policy changes |

## Other integration gaps

- A consistent **authority/evidence contract**, project-specific required gates, trusted-source boundaries and explicit action grants across all skills.
- Four-host installation/invocation adapters and tested, self-contained resource closure. The same Markdown does not guarantee identical runtime capabilities.
- Cohesive incident, dependency and documentation maintenance recipes; Addy's operational material is a starting point, not a complete incident-management implementation.

## Host portability findings

Official documentation was inspected, not inferred from upstream marketing:

| Host | Documented local discovery/invocation | Implication |
|---|---|---|
| Pi | Project/user `.agents/skills` and Pi skill paths; `/skill:name`; skill directory resolves bundled resources | Canonical Agent Skills works; extra delegation comes from the environment, not from the skill itself |
| Claude Code | `.claude/skills`; `/name` or plugin namespace; host-specific invocation/permission metadata | Provide a thin install/load adapter; do not imply `/skill:name` or `allowed-tools` is portable |
| Codex | `.agents/skills`; `$name` in CLI/IDE; `agents/openai.yaml` can control implicit invocation | Generate host policy metadata where necessary; discovery budgets and collisions need testing |
| Cursor | `.agents/skills`, `.cursor/skills`, plus compatibility directories; `/name`; Custom Modes optional | Avoid redundant installations across compatibility roots; do not require Custom Modes, cloud agents or Cursor built-ins |

Sources: [Claude skills](https://code.claude.com/docs/en/skills), [Codex skills](https://developers.openai.com/codex/skills), [Cursor skills](https://cursor.com/docs/skills). Pi documentation inspected from the installed 1.4.0 package: `docs/skills.md`, `docs/cli.md`, `docs/cli-integration.md`, and `docs/prompt-templates.md`.

Local observation: Pi performed the tool-disabled research runs successfully; `claude` and `codex` executables were found on PATH; `cursor`/`agent` were not found on PATH. This does **not** establish Claude/Codex authentication, prove the Cursor GUI is absent, or count as suite behavioral validation. The suite does not exist yet.

A collision-free multi-host install layout, host-specific explicit-only behavior and relocated-resource discovery are implementation acceptance cases, not facts established by this research.

## Attribution and updates

All three inspected upstream licenses are MIT: Matt Pocock, Lauren Tan (pstack), and Addy Osmani. Reused substantial material must retain copyright and license notices. Matt's PR material also records credit to Dex Horthy's show-me skill; inspect and preserve applicable downstream attribution.

Keep provenance with pinned revisions, selected original packages/resources and notices. Coordination rules live in this project's guide/instructions rather than rewritten upstream skill bodies. Review upstream changes and recheck relevant handoffs/discovery before updating.

`frontend-design` and `ui-ux-pro-max` remain **explicit dependencies**, not vendored/rebranded skills. Verify their actual local skill roots, required scripts/data, provenance and availability. Do not assume `CLAUDE_PLUGIN_ROOT` points at a globally installed skill, silently install dependencies, or substitute a homemade checklist if they are missing.

## Next gate

The user selected **Originals + guide**. Follow the [corrected original-skill workflow](../plans/workflow-design.md), [full guide](../guide/README.md) and [setup/validation notes](../guide/setup.md). Actual pinned upstream packages and a curated unchanged discovery view are included; the [corrected requirements](../plans/requirements.md) reject the former replacement-skill proposal. No publishing, merge or deployment is authorized.

[matt-spec]: https://github.com/mattpocock/skills/blob/5beb35b040e3de97e54fa9e386d7e42d15c295c2/skills/engineering/to-spec/SKILL.md
[matt-tickets]: https://github.com/mattpocock/skills/blob/5beb35b040e3de97e54fa9e386d7e42d15c295c2/skills/engineering/to-tickets/SKILL.md
[matt-review]: https://github.com/mattpocock/skills/blob/5beb35b040e3de97e54fa9e386d7e42d15c295c2/skills/engineering/code-review/SKILL.md
[pstack-mode]: https://github.com/cursor/plugins/blob/9580c23696ac8d7abed0c166f2f9918800afb819/pstack/skills/poteto-mode/SKILL.md
[pstack-architect]: https://github.com/cursor/plugins/blob/9580c23696ac8d7abed0c166f2f9918800afb819/pstack/skills/architect/SKILL.md
[pstack-feature]: https://github.com/cursor/plugins/blob/9580c23696ac8d7abed0c166f2f9918800afb819/pstack/skills/poteto-mode/playbooks/feature.md
[pstack-pr]: https://github.com/cursor/plugins/blob/9580c23696ac8d7abed0c166f2f9918800afb819/pstack/skills/poteto-mode/playbooks/opening-a-pr.md
[pstack-comments]: https://github.com/cursor/plugins/blob/9580c23696ac8d7abed0c166f2f9918800afb819/pstack/skills/no-comments/SKILL.md
[addy-start]: https://github.com/addyosmani/agent-skills/blob/aeac41d4d005999432bb7312f7ff06383a91d59d/docs/getting-started.md
[addy-tdd]: https://github.com/addyosmani/agent-skills/blob/aeac41d4d005999432bb7312f7ff06383a91d59d/skills/test-driven-development/SKILL.md
[addy-constraints]: https://github.com/addyosmani/agent-skills/blob/aeac41d4d005999432bb7312f7ff06383a91d59d/skills/constraint-driven-development/SKILL.md
[addy-api]: https://github.com/addyosmani/agent-skills/blob/aeac41d4d005999432bb7312f7ff06383a91d59d/skills/api-and-interface-design/SKILL.md
[addy-context]: https://github.com/addyosmani/agent-skills/blob/aeac41d4d005999432bb7312f7ff06383a91d59d/skills/context-engineering/SKILL.md
[addy-security]: https://github.com/addyosmani/agent-skills/blob/aeac41d4d005999432bb7312f7ff06383a91d59d/skills/security-and-hardening/SKILL.md
[addy-observability]: https://github.com/addyosmani/agent-skills/blob/aeac41d4d005999432bb7312f7ff06383a91d59d/skills/observability-and-instrumentation/SKILL.md
[addy-ship]: https://github.com/addyosmani/agent-skills/blob/aeac41d4d005999432bb7312f7ff06383a91d59d/skills/shipping-and-launch/SKILL.md
