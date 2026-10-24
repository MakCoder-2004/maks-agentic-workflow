---
name: setup-agentic-workflow
description: Set up the combined Matt Pocock, pstack and Addy workflow once per project. Use when explicitly asked to initialize or configure the whole workflow, its tracker/domain docs, model roles, quality constraints or AGENTS.md. Coordinate the existing setup instructions rather than running three separate interviews.
disable-model-invocation: true
---

# Set up the combined workflow

One invocation, one shared intake, one approved setup plan. Configure the existing skills; do not implement application features, rewrite upstream skills or install three full catalogs.

This integration skill was explicitly requested by the user. Matt remains the planning/spec/ticket owner, original poteto-mode the implementation/test/PR owner, and Addy's relevant skills the lifecycle/quality support.

## 1. Read the original instructions once

Find this project's `.maks-agentic-workflow/registry.json`, using its project root rather than assuming the current directory is the root. Read this coordinator's canonical file first. The standalone Matt/pstack setup skills have been removed; their unchanged instructions/templates are bundled as non-skill references next to this file. Read these four components in full:

| Component | Original instruction source | Purpose |
|---|---|---|
| Matt | `references/matt/SETUP.txt` (original setup-matt-pocock-skills instructions) | Tracker, triage vocabulary, domain/glossary/ADR layout and their consumer rules |
| pstack | `references/pstack/SETUP.txt` (original setup-pstack instructions) | Available model detection, reasoning budget, role/panel choices, validation and supported configuration path |
| Addy | `constraint-driven-development` | Project quality floor, chosen dimensions, actual check commands, baselines/budgets and enforcement placement |
| Addy | `context-engineering` | Compact durable project context, actual commands/conventions/boundaries, relevant docs and restartable handoff |

**Addy has no dedicated upstream setup skill.** Use the two existing skills above; do not claim a fictional setup-addy skill exists.

Resolve Matt/pstack reference paths relative to this coordinator's canonical directory (also recorded in `registry.setup_references`); they are data files, not callable skills. Resolve the two Addy components through their original `registry.skills[*].canonical_path`. In this source repository, the same bundled references are present; Addy's originals are under `upstream/addy/skills/`. Do not invoke the retired standalone setups or search unrelated user-home projects. If required original resources are unavailable, report the missing component instead of inventing replacement instructions.

Read Matt's tracker/domain templates from `references/matt/` only when that choice applies. For Claude Code read the installed original pstack Claude adapter and use the actual tool/model schema and project agent names, not an assumed plugin namespace.

Apply the sources inside **this single setup conversation**. Reuse discovered facts and accepted answers rather than launching each original interview from the beginning. This coordinator's explicit AGENTS.md/preservation/approval rules resolve differences in upstream setup defaults without editing their bodies.

## 2. Audit the existing state before asking

Read only what is relevant:

- Existing `AGENTS.md` and `CLAUDE.md`, including any installer-owned `<!-- maks-agentic-workflow:start -->` block and existing `## Agent skills` section.
- Matt's `docs/agents/issue-tracker.md`, `domain.md`, `triage-labels.md`; configured glossary/ADR paths and monorepo signals.
- Actual Git remote, tracker tooling and existing labels, without publishing or changing them.
- Existing `CONSTRAINTS.md`, project manifest, test/build/lint/typecheck scripts, CI and available runtime/browser/verification harness.
- Host/capabilities from the installed registry and actual tool schemas; pstack's existing supported model rule if present, its budget and role choices. Enumerate only models actually available to the host. Never invent a model slug or treat Cursor slugs as portable provider IDs.
- Actual frontend-design/ui-ux-pro-max availability if UI work is relevant; do not install, replace or copy private global skill directories.

Never ask a fact that can be inspected. Do not run a full/expensive test suite, start services or access sensitive production data merely to discover setup facts. Propose baseline measurements and their cost when execution needs approval. Do not read secrets or dump global transcripts.

## 3. One shared intake

Summarize existing configuration and missing choices briefly. Preserve usable existing settings; ask only unresolved decisions, in small rounds using the host's question tool or plain text if absent:

- **Matt:** authoritative tracker, needed triage-label overrides and single-/multi-context domain layout. Reuse existing labels/docs and Matt's seed templates. Do not invent a second tracker.
- **pstack:** reasoning budget and confirmed per-role/panel models or supported inherit-parent/auto aliases. Follow the original budget/role validation. Ask separately before creating or replacing a global rule, and show the exact path and effect on other projects.
- **Addy:** relevant quality dimensions, block/warn policy, actual baseline or agreed thresholds, and acceptable check cost/placement. Reuse unchanged constraints rather than interviewing again. Do not impose example numbers or web-only checks on an unrelated stack.

Carry prior accepted answers forward. One invocation may include questions and an approval checkpoint; it is not permission to guess missing requirements or bypass approval. If the original request already authorizes a concrete setup plan and choices, do not demand the same approval again.

## 4. Present one plan and get the necessary approval

List exact proposed file changes, external/global operations and checks, separated by Matt / pstack / Addy. Show the concise AGENTS.md additions and settings to preserve. Default to project-local documentation and the existing supported model configuration.

The plan must distinguish:

- **Allowed project configuration:** proposed doc/instruction updates and explicitly approved project checks.
- **Separate grants:** global model-rule edits, tool/dependency installs, MCP/server setup, external tracker labels/issues, secrets, CI edits or production operations.
- **Unavailable capabilities:** missing native delegation/model configuration, browsers or checkers. A file with an intended threshold is not proof that its check is installed/enforced.

Pstack's original setup normally writes a user-global rule. Do not silently write it, and do not pretend that a newly invented local config file is read by pstack. Use the original host-supported location only after approval, preserving unrelated settings. If no supported persistent mapping is available, record that limitation and the accepted fallback or pending action.

No code implementation, package install, PR, deployment, watcher, hook or additional skill generation is implicitly authorized. Optional verification/formal-verification generators remain opt-in and may be outside this installed selection.

## 5. Apply the approved setup, preserving existing work

### Canonical project instructions

Use the standard **`AGENTS.md`** filename (plural), not a newly invented `AGENT.MD`.

- If missing, create a short AGENTS.md with the actual project identity/stack, verified or explicitly unverified command references, workflow ownership, safety boundaries and documentation pointers.
- If present, preserve user-written rules and update only the agreed sections. Do not overwrite it with a template or append duplicate `## Agent skills` sections.
- A legacy singular AGENT.md or differently scoped instruction file is user data: read and flag it, do not silently rename/delete it or discard its rules.
- Never change content inside the installer-owned maks-agentic-workflow marker block; put setup-specific sections outside it so installer checksums remain valid.
- Preserve existing CLAUDE.md. If that host needs an import/pointer to AGENTS.md or CONSTRAINTS.md, propose one minimal non-duplicate addition. The user's request explicitly makes AGENTS.md the durable project instruction file even where Matt's upstream default would prefer an existing CLAUDE.md.
- Keep AGENTS.md compact: facts, commands, boundaries and links, not the full workflow handbook, all helper bodies or copied model-role tables.

### Matt configuration

Apply the original approved tracker/domain/triage templates, normally under `docs/agents/`. Add/update the existing `## Agent skills` pointers in AGENTS.md. Create only the labels explicitly authorized and absent from the configured tracker; local Markdown needs no external label operation. Do not create fake issues or overwrite existing glossary/ADRs merely to make setup look complete.

### Pstack configuration

Validate every real role model against detected availability. Reuse confirmed configuration and aliases supported by the actual host; respect the original budget and panel-count semantics. Write a global rule only under its separate grant. Keep the supported rule authoritative, with a path/status pointer in project docs rather than a conflicting duplicate model table in AGENTS.md. Report missing native tools/agents honestly; configuration text cannot create them.

### Addy configuration

Create or update approved `CONSTRAINTS.md` using the original skill's floor/dimensions/commands/placement approach. Every enforced requirement needs an actual checker and evidence; distinguish **written**, **measured**, **enforced**, **pending** and **not applicable**. If a tool or baseline run is unapproved/unavailable, record it as pending or measured-only, not installed, enforced or passing. Do not weaken existing thresholds to get green.

Add one concise instruction to read the actual constraints file before implementation. Record the real project commands, conventions, source/docs pointers and handoff rules using context-engineering; avoid loading the whole codebase or every skill into persistent context. Reuse existing scripts/CI; install or wire new tooling only if the plan explicitly authorized it.

## 6. Verify and summarize

- AGENTS.md exists, preserves prior rules, contains one coherent setup section and valid document pointers; installer-owned blocks are unchanged.
- Matt's configured tracker/domain/triage files match the approved choices and existing project vocabulary.
- Pstack model choices are valid and, if changed, written to the actually supported approved location; unresolved host/global limitations remain explicit.
- Constraints distinguish actual checks/results from plans, unknown baselines and inapplicable dimensions. Run only approved checks; report exact outcomes without manufacturing passes.
- Re-running with unchanged settings is a no-op: no duplicate sections, repeated label writes, global replacement or repeated interview. Do not create an application spec/PR during setup.

Finish with a compact **Matt / pstack / Addy / AGENTS.md** status table, files changed, checks actually run, pending choices/capabilities and the next command (`grill-with-docs` -> `to-spec` -> `to-tickets` -> `poteto-mode`). Never report the whole setup ready if a required component remains blocked. The user does not need to invoke the three component setup flows separately.
