# Maks Agentic Workflow

A focused way to combine **original Matt Pocock, pstack, and Addy Osmani agent skills** without installing three competing workflows or advertising every helper to your agent.

**Matt plans. Original pstack `poteto-mode` implements and verifies tickets. Relevant Addy skills add quality, security, runtime, release, and maintenance checks.** One explicit setup skill configures the project once.

## Install into a project

The repository is private. Authenticate with GitHub CLI and repository access, then run this inside the project you want to configure. The command retrieves a temporary bootstrap, installs the curated selection, then removes temporary source files.

```bash
gh auth login
python -c "import base64,subprocess; exec(compile(base64.b64decode(subprocess.check_output(['gh','api','repos/MakCoder-2004/maks-agentic-workflow/contents/install.py','--jq','.content'])),'<github-install>','exec'))" --project . --host pi
```

Choose `pi`, `codex`, `cursor`, or `claude-code`. Python 3.10+, GitHub CLI access, and network access are required. No permanent clone, package manager, or global install is needed. Only you and invited collaborators can access the private repository and its issues. Preview with `--dry-run`:

```bash
gh auth login
python -c "import base64,subprocess; exec(compile(base64.b64decode(subprocess.check_output(['gh','api','repos/MakCoder-2004/maks-agentic-workflow/contents/install.py','--jq','.content'])),'<github-install>','exec'))" --project . --host pi --dry-run
```

The installer exposes **22 entries**: 21 original skills and the combined setup skill. Another **53 selected original helpers** remain outside skill discovery and load only when needed. It does not install the full Matt, pstack, or Addy catalogs. See the [install guide](docs/guide/install.md) for files, updates, safety behavior, and host limits.

## Set up once

After installing, reload the agent and invoke the single setup skill:

| Host | Invocation |
|---|---|
| Pi | `/skill:setup-agentic-workflow` |
| Claude Code or Cursor | `/setup-agentic-workflow` |
| Codex | `$setup-agentic-workflow` |

It coordinates Matt's tracker and domain-doc setup, pstack's supported model/budget configuration, and Addy's project constraints and context guidance. It creates the standard **`AGENTS.md`** if missing, or updates it without discarding existing user rules. It reuses discovered facts, asks only for unresolved choices, and presents one setup plan. Global model rules, tool installation, CI changes, external labels, and other external actions still need their own approval.

Addy has no standalone upstream setup skill. The combined setup uses Addy's actual `constraint-driven-development` and `context-engineering` instructions. The standalone Matt and pstack setup skills are not installed; their original instructions are retained as on-demand references inside the combined setup.

## How the workflow works

```text
SETUP ONCE
  setup-agentic-workflow
  -> inspect the project, configure docs and constraints, preserve AGENTS.md

PLAN AND DESIGN: MATT LEADS
  research -> grill-with-docs -> architecture/prototype when useful
  -> to-spec -> to-tickets
  -> approve scope, design, acceptance criteria, and ticket dependencies

BUILD AND TEST: POTETO-MODE OWNS EXECUTION
  ready ticket -> implement one slice -> test and verify it
  -> relevant Addy checks -> fix and retest -> next ready ticket
  -> focused PR using pstack's original workflow

ADDY: CROSS-CUTTING ENGINEERING CHECKS
  requirements and constraints before building
  security, contracts, tests, and browser/runtime checks per change
  CI/CD, migrations, observability, release, and maintenance as relevant
```

The ownership boundary prevents duplicate plans and competing implementations:

- **Matt owns the source of truth for decisions.** `to-spec` captures the agreed behavior. `to-tickets` makes independently verifiable slices and blocking relationships.
- **pstack `poteto-mode` owns implementation.** It consumes the approved spec and tickets, verifies each slice before dependent work, and prepares PRs.
- **Addy skills supply checks where they apply.** They strengthen planning, security, testing, browser/runtime verification, CI/CD, migrations, observability, documentation, and launch readiness. They do not create a second spec or build controller.

Approve the spec and ticket plan before production implementation. Publishing, merging, deploying, global configuration, and destructive actions need their own authorization. A missing check or unavailable host feature is reported as a gap, not a pass.

## Six development phases

| Phase | Owner and purpose | Main handoff |
|---|---|---|
| **Plan** | Matt clarifies the problem, domain, acceptance criteria, and dependencies. Addy constraints shape the quality bar. | Approved spec and ready tickets |
| **Design** | Matt's codebase-design/prototype and pstack's architecture helpers resolve important structural or behavioral uncertainty. Use the actual UI design dependencies for interface work. | Agreed design, glossary, and ADRs |
| **Build** | Original pstack `poteto-mode` implements one approved ticket/slice at a time. | Verified change for one ticket |
| **Test** | Test each slice. Add relevant security, browser/runtime, performance, and code-review checks before starting dependent work. | Evidence linked to the ticket and current patch |
| **Deploy** | Prepare the PR, then use Addy's CI/CD, migration, observability, and launch skills as relevant. | Separately approved publication, merge, or release |
| **Maintain** | Triage issues/incidents, update docs and constraints, monitor operations, and return follow-ups to Matt's ticket flow. | Prioritized tickets and maintained project knowledge |

The phases can loop. A prototype may send a feature back to planning. A failed test returns the slice to build. A production incident re-enters diagnosis and planning. The only fixed ownership rule is that Matt's approved spec/tickets remain authoritative and poteto-mode owns implementation.

## Skills included after filtering

The installer advertises exactly these entry skills:

### One-time setup

- `setup-agentic-workflow`: coordinates the original Matt/pstack setup instructions, Addy's constraints/context setup, and `AGENTS.md` creation or preservation.

### Matt: planning and domain knowledge

- `research`
- `grill-with-docs`
- `codebase-design`
- `prototype`
- `to-spec`
- `to-tickets`
- `triage`
- `handoff`

### pstack: implementation owner

- `poteto-mode`

### Addy: project-wide lifecycle checks

- `constraint-driven-development`
- `api-and-interface-design`
- `test-driven-development`
- `browser-testing-with-devtools`
- `security-and-hardening`
- `code-review-and-quality`
- `performance-optimization`
- `ci-cd-and-automation`
- `observability-and-instrumentation`
- `deprecation-and-migration`
- `shipping-and-launch`
- `documentation-and-adrs`

The installer also preserves 53 selected helper skills outside discovery. The helper files are available when an entry skill needs them, but they are not registered as additional project commands.

### Complete on-demand helper list

**Matt, 6:** `grilling`, `domain-modeling`, `wayfinder`, `retro`, `improve-codebase-architecture`, `diagnosing-bugs`.

**pstack, 39:** `how`, `why`, `architect`, `arena`, `swarm`, `interrogate`, `unslop`, `technical-writing`, `no-comments`, `tdd`, `benchmark-checklist`, `show-me-your-work`, `blast-radius`, `correct`, `figure-it-out`; plus the 24 principles `principle-attack-the-premise`, `principle-boundary-discipline`, `principle-build-the-lever`, `principle-encode-lessons-in-structure`, `principle-exhaust-the-design-space`, `principle-experience-first`, `principle-explain-the-number`, `principle-fix-root-causes`, `principle-foundational-thinking`, `principle-guard-the-context-window`, `principle-laziness-protocol`, `principle-make-operations-idempotent`, `principle-migrate-callers-then-delete-legacy-apis`, `principle-minimize-reader-load`, `principle-model-the-domain`, `principle-never-block-on-the-human`, `principle-outcome-oriented-execution`, `principle-prove-it-works`, `principle-redesign-from-first-principles`, `principle-separate-before-serializing-shared-state`, `principle-sequence-verifiable-units`, `principle-subtract-before-you-add`, `principle-test-behavior-not-implementation`, and `principle-type-system-discipline`.

**Addy, 5:** `context-engineering`, `spec-driven-development`, `source-driven-development`, `debugging-and-error-recovery`, `frontend-ui-engineering`.

**Cursor team kit, 3:** `control-ui`, `control-cli`, `deslop`.

The installer deliberately omits competing setup entries, Matt's competing implementers, Addy's competing planning/build router, and unrelated source-catalog skills. The standalone `setup-matt-pocock-skills` and `setup-pstack` skills are removed from project discovery; their original content remains as plain reference files used by the combined setup. Upstream skill bodies are otherwise unchanged.

`frontend-design` and `ui-ux-pro-max` remain **external UI dependencies**. The installer does not download, bundle, or replace them. Check that both are available in the host where UI work runs.

## The full usage guide

- [How to run the workflow](docs/guide/README.md)
- [Recipes for features, bugs, architecture, UI, releases, and maintenance](docs/guide/scenarios.md)
- [Install options and host-specific limitations](docs/guide/install.md)
- [Setup skill retirement and update behavior](validation/setup-retirement.md)
- [Source comparison and adaptation findings](docs/research/upstream-comparison.md)
- [Inventory of all 121 upstream skills](docs/research/skill-inventory.md)

## Repository structure

This repository has two different views. **Do not copy the source archive into consuming projects.**

| Path | Purpose |
|---|---|
| `.agents/skills/` | Source-repository audit view of 103 unchanged original skills after removing both standalone setup skills |
| `upstream/` | Pinned source snapshots, licenses, and full source material for comparison and provenance |
| `workflow/selection.json` | Exact filtered list of entry skills and private helpers |
| `workflow/skills/setup-agentic-workflow/` | The one user-requested coordinator plus original Matt/pstack setup instructions as non-skill references |
| `scripts/install.py` and `install.py` | Curated project installer and authenticated private GitHub bootstrap |
| `.maks-agentic-workflow/` in an installed project | Only the selected originals, required resources, registry, and usage guide |
| `sources.lock.json` and `upstream/checksums.json` | Pinned provenance and integrity checks for original upstream content |
| `docs/guide/` | Full workflow and scenario instructions |

Pstack's 24 original principle skills are included as on-demand dependencies; they are not 24 extra advertised entries. Addy's shared references and pstack's required playbooks/resources are preserved so original instructions resolve correctly.

## Verify

Run the collection and installer tests from this repository:

```bash
python -m unittest discover -s tests -v
```

This checks package integrity, filtered selection, installation and documented safety behavior. It does not prove every host provides native subagents, browser automation, model access, or application-level test infrastructure. Read the [validation record](docs/guide/validation.md) before assuming a host/runtime feature is available.

## Contribute

The repository is private. Issues and pull requests are available to you and invited collaborators. Changes to `main` must go through a pull request. The owner reviews and merges contributions; collaborator pushes and merges to `main` are blocked by the `main` ruleset. Merge commits and rebase-merges preserve contributors' individual commits, so GitHub can credit each contributor. Squash merging is disabled.

See [CONTRIBUTING.md](CONTRIBUTING.md) for access, test, review, and contributor-credit details.

## Attribution

This repository combines original skills from [Matt Pocock](https://github.com/mattpocock/skills), [Lauren Tan's pstack](https://github.com/cursor/plugins/tree/main/pstack), [Addy Osmani](https://github.com/addyosmani/agent-skills), and the required [Cursor team kit](https://github.com/cursor/plugins/tree/main/cursor-team-kit). Their original licenses and notices remain with the source files. See [NOTICE](NOTICE.md). Inclusion does not imply endorsement.
