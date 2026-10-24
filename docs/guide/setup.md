# Setup the compact original-skill workflow

## Install into a consuming project

Use [the curated installer](install.md), not three full plugin installations or a copy of this source repository's 103-entry audit view:

Run inside the target project:

```bash
python -c "import sys,urllib.request; code=urllib.request.urlopen('https://raw.githubusercontent.com/MakCoder-2004/maks-agentic-workflow/main/install.py').read(); exec(code or sys.exit('Download failed'))" --project . --host pi
```

Choose `pi`, `codex`, `cursor` or `claude-code`; add `--dry-run` to preview. Python 3.10+ and network access are required. No GitHub login, GitHub CLI, permanent clone, or package installation is needed. The underlying curated installer remains usable from a local checkout.

The selection is **22 entries: 21 original skills plus the combined setup coordinator, with 53 original on-demand helpers**. Helpers live outside host discovery roots and do not contribute another 53 startup skill descriptions. The [selection file](../../workflow/selection.json) records exactly which originals are included. The full archived sources under `upstream/` and legacy `.agents/skills/` view in this repository are source/audit material, **not the target payload**.

## Installed project layout

- Pi/Codex/Cursor: 22 selected entries under `.agents/skills/`.
- Claude Code: 22 selected entries under `.claude/skills/`, with no plugin namespace.
- Canonical selected originals/helpers/resources, source map and runbook: `.maks-agentic-workflow/`.
- Addy's shared references: both the canonical original tree and the matching public `../../references` location.
- Managed coordination block: `AGENTS.md`, or `CLAUDE.md` for Claude Code. Existing text outside the block is preserved.
- Original pstack `poteto-agent` and `comment-sicko` role files: private for all hosts; additionally in `.cursor/agents/` or `.claude/agents/` for those hosts.

Original names/content are unchanged. The only added integration is the explicitly requested `setup-agentic-workflow`, which coordinates the original setups; it does not replace/rewrite their bodies. Before resolving a hidden helper or upstream relative resource path, the agent reads the canonical original indicated by `.maks-agentic-workflow/registry.json`. A private helper is an on-demand file, not a falsely registered slash command; read its original body when a direct Skill-tool invocation is unavailable.

Only the two needed native role descriptions are added for Cursor/Claude. There is no new scheduler or orchestration service. Agent role registration by itself does not prove the actual tool, model or independent execution is available.

## One setup invocation

Reload/restart the host and invoke **one** skill:

| Host | Command |
|---|---|
| Pi | `/skill:setup-agentic-workflow` |
| Claude Code / Cursor | `/setup-agentic-workflow` |
| Codex | `$setup-agentic-workflow` |

It reads the bundled non-skill references `references/matt/SETUP.txt` and `references/pstack/SETUP.txt`, plus Addy's original `constraint-driven-development` / `context-engineering` skills. Addy has no separate upstream setup skill. The coordinator audits once, reuses existing answers, asks only missing decisions, and presents one setup plan rather than running three independent interviews.

The approved project setup covers:

- Matt's authoritative tracker, labels, glossary/ADR layout and `docs/agents/` pointers.
- Pstack's actual available models, reasoning budget, role choices and supported configuration path. Global rules require a separate explicit grant; unknown native capabilities remain pending, not magically configured.
- Addy's actual commands, quality floor, agreed checks/baselines/budgets, context and handoff conventions. A written constraint is not falsely described as installed/enforced/passing.
- Canonical **AGENTS.md** (plural): create it when missing, preserve its user-written rules when present, and keep setup additions outside the installer-owned marker block. Existing CLAUDE.md is preserved and gets a minimal pointer/import only when needed and approved. A legacy singular AGENT.md is not silently renamed or deleted.

It does not implement application code, install tools, create secrets, change CI, generate more skills, modify globals, publish tracker data or deploy merely because you invoked setup. Those operations need their applicable approval. Optional or unavailable prerequisites are reported honestly. Re-running unchanged setup should not duplicate sections, labels or interviews.

Both standalone Matt/pstack setup skills are removed from discovery and the installed skill registry. Their instructions/templates remain reference data inside the combined setup, not separate commands. After setup, continue with `grill-with-docs` -> `to-spec` -> `to-tickets` -> `poteto-mode`. Verify the actual external frontend-design and ui-ux-pro-max when UI work is relevant.

To update either earlier compact release, rerun the same GitHub command. It removes only the exact unchanged installer-owned standalone setup copies, preserves user rules and extra files, and refuses edited, unowned or incomplete inventories. No other automatic pruning is enabled.

The selected source revision and target paths are stored in the installed registry; file ownership/integrity is recorded in install.json. Verify with `python /path/to/scripts/install.py --project /path/to/project --check`.

## Pi

Pi's documented project discovery supports `.agents/skills/`. Example explicit invocations:

```text
/skill:grill-with-docs Clarify this feature and document decisions.
/skill:to-spec Synthesize our agreed behavior/design.
/skill:to-tickets Break the approved spec into verifiable dependent slices.
/skill:poteto-mode Implement the approved spec/tickets using the handoff.
/skill:security-and-hardening Check the affected trust boundaries.
```

Some originals say to use a Skill tool; stock Pi normally loads skills by reading their files. Read the exact canonical original/helpers rather than inventing that tool or selecting a global namesake. Native subagents require an extension; raw role files do not create built-in Pi delegation. Cursor Task environments/model slugs/custom agent APIs are not automatically Pi APIs. Report missing capabilities and do not claim self-review is independent review.

A fresh read-only Pi smoke run against an actual compact installation successfully read original grill-with-docs, grilling and domain-modeling from their canonical paths. This establishes that tested helper-loading path, not full application implementation or universal host automation.

## Codex

Codex documents `.agents/skills/` project discovery. Use `/skills` or `$name`:

```text
$grill-with-docs ...
$to-spec ...
$to-tickets ...
$poteto-mode ...
$shipping-and-launch ...
```

The compact layout limits the descriptions this installer contributes. Global packages can still add context. Authentication and original pstack tool/model/agent compatibility require separate checks. Native custom-agent TOML configuration is not silently changed; role definitions are supplied privately for an actual supported facility. Do not fabricate `$pstack:...` command syntax for these plain project skills.

## Cursor

Cursor documents `.agents/skills/` project discovery. Use `/grill-with-docs`, `/to-spec`, `/to-tickets`, `/poteto-mode` and the other installed original names. Custom Mode is optional, not required by the installer.

Two original role files are also supplied in `.cursor/agents/`; models, cloud execution, MCPs and browser/control prerequisites still need real configuration. Do not additionally load whole pstack/Matt/Addy plugins for the same names unless you intentionally want duplicate discovery and extra context. The installer refuses selected names found in another project discovery root rather than relying on undocumented deduplication.

No Cursor CLI was found on PATH during the initial source inspection; this does not prove the GUI is absent. Four-host file-layout tests are not live Cursor execution tests.

## Claude Code

The compact command uses `.claude/skills/`, `.claude/agents/` and a managed block in `CLAUDE.md`. Use plain project skill names:

```text
/grill-with-docs ...
/to-spec ...
/to-tickets ...
/poteto-mode ...
/shipping-and-launch ...
```

It deliberately does **not** run `claude --plugin-dir` for three full catalogs. Read the original adapter included at `.maks-agentic-workflow/originals/pstack/docs/harness/claude-code.md` for Task -> Agent, model alias and unsupported-feature mappings. Because these are plain project files rather than a `pstack` plugin, registered role names are `poteto-agent` / `comment-sicko`, not `pstack:poteto-agent` / `pstack:comment-sicko`. Always give delegates the canonical poteto-mode absolute path.

The source repository also archives upstream's complete generated Claude plugin for research/reference. It is not copied by this installer, and its presence does not mean the compact install has run a native multi-plugin session. Authentication, native discovery and all runtime capabilities must be checked in the actual host/version.

## Existing installations

Unrelated project skills, user text and all global configurations remain untouched. Existing extra upstream/helper skill entries are reported rather than removed; the command cannot promise only 22 total descriptions if you already load additional collections elsewhere. Inspect/disable duplicates deliberately. Only the two known prior compact profiles support this exact standalone-setup retirement. It will not silently migrate a full-catalog or different-host installation.

Reinstalling unchanged files is idempotent. Edited originals, edited managed blocks, incomplete manifests, changed inventory/provenance or conflicting files stop the operation. No force overwrite, automatic pruning, uninstaller or global clean command is included; the known setup-reference migration is the sole explicitly supported inventory retirement. See [installer safety](install.md).

## UI and operational prerequisites

Actual frontend-design and ui-ux-pro-max remain external dependencies under their own provenance/licenses. Check their complete scripts/data in the active host; resolve commands from the real skill directory, not a guessed CLAUDE_PLUGIN_ROOT. The installer does not search/copy private user-home installations or download packages.

No upstream setup hooks, model credentials, browser/MCP services, automations, watchers, PRs, merges or deployments are activated. Original control-cli includes Unix PTY/tmux examples; Windows needs an actually supported harness. Original scripts are copied with executable intent and chmod applied where supported; Windows Git users should review recorded executable modes before sharing a Unix checkout, because the installer does not stage or alter the target's Git index.
