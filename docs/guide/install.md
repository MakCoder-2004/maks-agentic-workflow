# Install only the combined workflow

Requires Python 3.10+ and network access. No GitHub CLI, login, permanent clone, or package manager is required.

## Install directly from GitHub

Run this **inside your target project**:

```bash
python -c "import sys,urllib.request; code=urllib.request.urlopen('https://raw.githubusercontent.com/MakCoder-2004/maks-agentic-workflow/main/install.py').read(); exec(code or sys.exit('Download failed'))" --project . --host pi
```

The bootstrap downloads the public source archive, validates it, installs the selected skills, and removes temporary files. Review remote code before executing it. The installer runs in the original working directory, so `--project .` means your project.

Use `--project "/path/to/your-project"` to target another directory, and choose `pi`, `codex`, `cursor` or `claude-code`. All existing flags are forwarded: add `--dry-run`, `--list` or `--check` to the same GitHub command.

The [bootstrap](../../install.py) downloads the current main source ZIP into a temporary directory without credentials, validates the archive, and invokes the curated installer while preserving your original working directory. It removes temporary source afterward. Downloading source for selection does **not** install the three full catalogs or expose the temporary archive's skills to your project's discovery. Only the selected 21 original entries, the combined setup coordinator and their private helper/reference closure reach your project. A failed download or invalid archive does not invoke the project installer.

The command executes code from this public repository's current `main`; review the source before running and use normal user rights. Network access is required. The underlying curated installer itself remains offline. There is no claim that `npx skills add` will execute this custom selection.

## Optional local-checkout command

From a checkout of this repository:

```bash
python scripts/install.py --project "../my-project" --host pi
```

From any working directory, use the installer script's actual absolute path:

```bash
python "/path/to/maks-agentic-workflow/scripts/install.py" --project "/path/to/my-project" --host pi
```

On Windows, for example:

```powershell
python "E:/Programming/Projects/maks-agentic-workflow/scripts/install.py" --project "E:/Programming/Projects/my-project" --host pi
```

`--project` also accepts `--target`. It defaults to the current directory, but the installer refuses to install into this source/archive repository, a drive root or your home directory. A new target project directory is created only after successful preflight, never by a dry run. This command does not initialize Git or run any application command.

Choose one host for a project:

| `--host` | Public entry points | Managed instructions | Original role registration |
|---|---|---|---|
| `pi` | `.agents/skills/` | Managed block in `AGENTS.md` | Role files private; a real delegation extension is still required |
| `codex` | `.agents/skills/` | Managed block in `AGENTS.md` | Role files private; native custom-agent configuration is not changed |
| `cursor` | `.agents/skills/` | Managed block in `AGENTS.md` | Two original role files in `.cursor/agents/` |
| `claude-code` | `.claude/skills/` | Managed block in `CLAUDE.md` | Two original role files in `.claude/agents/`, no plugin namespace |

When omitted, host defaults to the existing installation's host, otherwise Pi. Host layout does not prove every native tool/model/browser is available. See [setup and compatibility](setup.md).

## Preview, list, verify

```bash
# Show the 21 original entries plus the combined setup entry, without installing.
python scripts/install.py --list

# Preflight target paths, existing files and conflicts; write nothing.
python scripts/install.py --project "../my-project" --host pi --dry-run

# Install the reviewed combination.
python scripts/install.py --project "../my-project" --host pi

# Verify its inventory, originals, discovery paths and managed instruction block.
python scripts/install.py --project "../my-project" --check
```

Repeat the install command to check/update the reviewed footprint, including retirement of the two standalone setups from either prior compact release. An unchanged install reports `ALREADY UP TO DATE` without rewriting files. There is no `--all`, full-package install mode, automatic pruning, host migration or force-overwrite switch.

## What the command selects

Selection is explicit in [workflow/selection.json](../../workflow/selection.json), not inferred by copying the three repositories.

### 22 advertised entries: 21 originals + unified setup

The user-requested **`setup-agentic-workflow`** is the single setup invocation. It coordinates the original Matt/pstack setups and Addy constraints/context, and initializes/preserves canonical AGENTS.md. Run it after installation/reload; the standalone Matt/pstack setup skills are removed. Their unchanged instructions/templates are bundled as `.txt` references so they cannot be discovered as separate skills.

| Owner | Entry points |
|---|---|
| Matt (8) | `research`, `grill-with-docs`, `codebase-design`, `prototype`, `to-spec`, `to-tickets`, `triage`, `handoff` |
| pstack (1) | `poteto-mode` |
| Addy (12) | `constraint-driven-development`, `api-and-interface-design`, `test-driven-development`, `browser-testing-with-devtools`, `security-and-hardening`, `code-review-and-quality`, `performance-optimization`, `ci-cd-and-automation`, `observability-and-instrumentation`, `deprecation-and-migration`, `shipping-and-launch`, `documentation-and-adrs` |

The 21 upstream entries retain original names and unchanged SKILL.md contents. The one explicit exception is the new user-requested setup coordinator, stored separately under the installed integration tree; it does not rewrite upstream bodies or create a replacement `maw-*` suite.

### 53 helpers, not 53 extra discovery descriptions

- **Matt (6):** the composed grilling/domain helpers plus large-work planning, retrospective, architecture-audit and diagnosis helpers used in the scenario guide.
- **pstack (39):** the 24 principle leaves that poteto-mode explicitly requires, and 15 architecture/investigation/delegation/review/TDD/writing/measurement/lesson helpers used by the selected execution path.
- **Addy (5):** context, requirements completeness, source-driven research, debugging and frontend guidance.
- **cursor-team-kit (3):** original `control-ui`, `control-cli` and `deslop`, referenced by pstack.

Thus **74 distinct original skills plus one integration skill are available on disk; 22 entries are advertised and 53 original helpers remain on demand**. Helpers are not fake slash commands; read the canonical original on demand. Their bodies can still enter context when genuinely used, as can the principle index already inside original poteto-mode. The installer does not claim to reduce poteto-mode's own unchanged body.

The target contains selected skill folders/resources only. It does not contain the full source archives, their plugin manifests/catalogs, automatic hooks, automation packs, unrelated bots/videos/productivity skills, competing Matt/Addy implementers, frozen utilities or a new workflow engine. Original poteto-mode's own embedded playbooks/scripts remain intact as bundled resources; optional features outside this curated profile are not automatically made operational or granted authority.

## Installed layout

For Pi/Codex/Cursor (Claude uses `.claude` for the public view):

```text
AGENTS.md                                  Existing text + small managed coordination block
.agents/
  skills/<22 selected names>/              21 original entries + unified setup, with resources
  references/                              Addy's original shared checklists
.maks-agentic-workflow/
  WORKFLOW.md                              Installed scenario/handoff runbook
  registry.json                            Exact original paths, roles, source revisions and visibility
  install.json                             Owned/reused files and checksums, instruction-block checksum
  NOTICE.md                                Attribution
  integration/skills/setup-agentic-workflow/ User-requested setup coordinator
  originals/
    matt/skills/...                        Only selected planning skills/helpers
    pstack/skills/...                       poteto-mode and its selected helpers/principles
    pstack/agents/...                       Two original role definitions
    pstack/docs/harness/claude-code.md      Original upstream tool/model adapter documentation
    addy/skills/...                         Only selected lifecycle skills/helpers
    addy/references/...                     Canonical shared references
    cursor-team-kit/skills/...              Only the three real dependencies
```

Originals outside `.agents/skills` / `.claude/skills` are not normal skill-discovery roots. The managed instruction block tells the agent how to find their canonical paths through `registry.json` and resolve original sibling/resource references there. It does not import the full runbook or helper bodies into startup context. A real Pi read-only probe verified that original `grill-with-docs` loaded its original grilling/domain helpers from this private tree without registering them as commands.

Each public copy keeps its own resources. Addy's public `../../references` layout is also preserved. Scoped Git attributes preserve original bytes; executable script permissions are applied where the OS supports them. Nothing depends on symlinks back to this checkout: the installed project can move and be checked again.

## Existing projects and safety

- Existing agent instructions are preserved byte-for-byte outside one clearly marked block, including BOM/CRLF. The installer does not replace your project's rules with this source repository's AGENTS.md.
- Different existing skill contents or duplicate selected identities across host roots stop preflight before writes. An identical pre-existing file may be reused, but is recorded as user-owned and cannot be silently updated later.
- Unrelated project skills/files are preserved. Existing globally installed packages remain untouched. If your project already advertises extra upstream/helper skills, the command warns rather than deleting them. Therefore the 22-entry claim concerns this installer, not every pre-existing/global description your host may load.
- Locally edited or missing managed files, edited workflow blocks, changed provenance, incomplete inventories and incompatible selection footprints are refused. The exact known setup retirement removes only pinned, unchanged, installer-owned copies from the two prior compact profiles. It cannot be used to mask a missing helper, alter ownership or delete unrelated files; rollback restores retired files if a later write fails. User edits outside the managed instruction block are allowed. Restore/review the previous installation instead of editing manifest ownership to bypass a conflict.
- Symlinks, Windows junctions and reparse paths observed during path checks are refused. Detected changes to file content or permissions after preflight are not overwritten. These checks use ordinary pathname-based I/O, not race-proof directory handles: a hostile process replacing a directory with a link between a check and the write is outside the protection provided. Use a trusted, idle project filesystem with normal user rights; do not run elevated against an adversarial or concurrently manipulated project.
- Writes are atomic per file. Ordinary failures roll back changes already made. A file edited concurrently after the installer wrote it is preserved instead of rolled back over the user's edit; an incomplete rollback is reported and requires inspection before retrying. Run installs while other writers are idle.
- `install.json` is trusted **local bookkeeping**, not a signed security boundary. Inventory/provenance checks detect ordinary corruption; they do not authenticate an attacker who can fabricate both files and ownership/checksum records. Inspect untrusted project content before running any installer.
- No automatic global edits, packages, secrets, hooks, Git commits/pushes, PRs, watcher processes, model configuration or deployment occur.

Apart from this exact setup retirement, a different host or changed footprint requires deliberate review/cleanup. Edited or unowned standalone setup files block migration; global installations are never removed. Empty retired directories are removed only when empty, preserving user-added files. There is no automatic uninstaller in this version. Removal must use the recorded ownership and preserve reused files and all user text outside the managed block; do not recursively delete shared skill/reference directories.

## UI and host prerequisites

As agreed, actual `frontend-design` and `ui-ux-pro-max` remain external dependencies. The command does not download/rebrand them or copy private user-home installations. Verify them in the host/project where UI work runs. Browsers, MCPs, PTY tooling, model access, provider credentials and independent-agent capability also remain real prerequisites.

For Claude Code, the compact install uses original unnamespaced project skill/agent files plus the upstream tool-mapping notes; it does not launch three full native plugins. For Pi/Codex, unresolved native Cursor tool/agent requirements are documented, not disguised as full automation.

## Validation

Run the source repository's tests with:

```bash
python -m unittest discover -s tests -v
```

Installer tests exercise the selection, all four file layouts, resource paths, unchanged originals, repeated installs, preview/check commands, unrelated working directories and paths with spaces, project-text preservation, collisions, local edits, rollback/concurrent edits, manifest corruption, relocation, Git filters, and a real Windows junction where supported. [Validation notes](validation.md) separate these checks from full host/application execution.
