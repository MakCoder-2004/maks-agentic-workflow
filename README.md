# Maks Agentic Workflow

A curated set of existing engineering skills with a clear handoff between planning and implementation. Matt Pocock's skills define the work, pstack's `poteto-mode` builds and verifies it, and Addy Osmani's skills provide the relevant quality and release checks. You don't have to install all three catalogs or run three competing workflows.

The repository is public. Anyone can read it, open an issue, or submit a pull request; only the owner can merge to `main`.

## Get started

You need Python 3.10+ and network access. No GitHub login or GitHub CLI is required.

1. From your **target project's directory**, install the skills. Change `pi` to `codex`, `cursor`, or `claude-code` as needed:

   ```bash
   python -c "import sys,urllib.request; code=urllib.request.urlopen('https://raw.githubusercontent.com/MakCoder-2004/maks-agentic-workflow/main/install.py').read(); exec(code or sys.exit('Download failed'))" --project . --host pi
   ```

   Already have a checkout? From this repository, run `python scripts/install.py --project /path/to/your-project --host pi` instead. Add `--dry-run` to preview changes. The installer preserves existing project instructions and refuses to overwrite modified skills.

2. Reload your agent and run setup **once**:

   | Host | Setup command |
   |---|---|
   | Pi | `/skill:setup-agentic-workflow` |
   | Codex | `$setup-agentic-workflow` |
   | Cursor or Claude Code | `/setup-agentic-workflow` |

   Setup detects the project before asking questions. It configures Matt's tracker and domain docs, checks pstack's model options, and records Addy's quality constraints. It creates `AGENTS.md` if missing and keeps existing rules. Global configuration, tool installs, and external changes still need your approval.

3. Start with the appropriate planning skill. For an unclear feature, use `grill-with-docs`. Once decisions are settled, run `to-spec` and `to-tickets`. Approve the design and tickets before handing them to `poteto-mode`.

For flags, updates, and host-specific limitations, see the [installation guide](docs/guide/install.md) and [setup guide](docs/guide/setup.md).

## Who does what

```text
Matt:   research / grill / design -> approved spec -> dependency-aware tickets
                                                      |
                                                      v
pstack:                         poteto-mode -> one ticket -> test -> next ticket -> PR
                                                      ^          |
Addy:                    relevant constraints, security, runtime and review checks

After the PR: Addy covers CI/CD, migrations, observability and release readiness.
Issues and maintenance findings can feed back into Matt's planning flow.
```

**Matt owns the specification.** `grill-with-docs` brings together requirements and domain vocabulary; `to-spec` writes the agreed behavior; `to-tickets` breaks it into verifiable work with real blockers. Design and prototypes are used when uncertainty warrants them, not for every small change.

**`poteto-mode` owns execution.** Give it the approved spec, ready tickets, acceptance criteria, glossary or ADRs, test commands, and constraints. It implements and verifies a ticket before moving to dependent work. It prepares a reviewable PR; opening a PR is not merging or deploying.

**Addy supplies checks throughout the cycle.** Apply the relevant constraints, interface, test, browser, security, performance, CI/CD, observability, migration, documentation, and shipping skills at the point they matter. Addy does not write a second authoritative spec or take over implementation.

A useful handoff after ticket approval:

> Use `poteto-mode` to implement the approved spec at [link] through tickets [links]. Keep Matt's requirements and blocking relationships authoritative. Start with an unblocked ticket, implement and test that slice, apply the relevant Addy checks, fix and retest, then record the evidence before moving on. Stop if the scope changes or required verification is unavailable. Prepare a focused PR; ask separately before publishing, merging, or deploying.

For a bug with an agreed expected behavior, start with reproduction and a focused ticket; you do not need to write a full product spec. See the [scenario recipes](docs/guide/scenarios.md) for features, bugs, architecture, UI, documentation, releases, and maintenance.

## What gets installed

**22 skills appear in the project's skill picker:** 21 original upstream entry points and the one combined setup skill.

| Role | Entry skills |
|---|---|
| Setup | `setup-agentic-workflow` |
| Matt: planning and handoff | `research`, `grill-with-docs`, `codebase-design`, `prototype`, `to-spec`, `to-tickets`, `triage`, `handoff` |
| pstack: build and verify | `poteto-mode` |
| Addy: lifecycle checks | `constraint-driven-development`, `api-and-interface-design`, `test-driven-development`, `browser-testing-with-devtools`, `security-and-hardening`, `code-review-and-quality`, `performance-optimization`, `ci-cd-and-automation`, `observability-and-instrumentation`, `deprecation-and-migration`, `shipping-and-launch`, `documentation-and-adrs` |

Another **53 original helper skills** are stored outside normal skill discovery. `poteto-mode` can read its principles, playbooks, and review helpers when needed without advertising them all up front. The exact filter is in [`workflow/selection.json`](workflow/selection.json).

The standalone Matt and pstack setup skills are **not** installed. Their unchanged setup instructions and templates are included as references inside `setup-agentic-workflow`. Other selected upstream skill bodies keep their original names and content. The full snapshots under `upstream/` are for provenance and research; the installer does not copy those catalogs into your project.

For UI work, `frontend-design` and `ui-ux-pro-max` are separate dependencies. Check that they are installed in your agent environment; this installer does not bundle them or create substitutes. Browsers, models, subagents, and deployment tools also need their own working setup. [Compatibility and verification notes](docs/guide/validation.md) distinguish installed files from tested runtime capabilities.

## Project files and permissions

The installer adds a small managed block to `AGENTS.md`, or to `CLAUDE.md` for a Claude Code install, without replacing your rules. `.maks-agentic-workflow/` holds the usage guide, pinned selected originals, private helpers, and a registry so the agent can find them on demand. The installer does not install global packages or enable hooks and automations.

Approve the spec and ticket plan before production implementation. Publishing issues or PRs, merging, deploying, changing global configuration, and destructive operations require separate authorization. A missing or inconclusive test is not a pass.

## Contribute and learn more

The repository is public. Anyone can open issues or submit PRs. The owner reviews and merges changes to `main`. Merge commits and rebase merges preserve contributors' individual commits; squash merges are disabled. See [CONTRIBUTING.md](CONTRIBUTING.md).

- [Full workflow](docs/guide/README.md) and [scenario recipes](docs/guide/scenarios.md)
- [Install and upgrade details](docs/guide/install.md)
- [Why these skills were chosen](docs/research/upstream-comparison.md) and [upstream inventory](docs/research/skill-inventory.md)
- [Source attribution and licenses](NOTICE.md)

Run `python -m unittest discover -s tests -v` in this repository to check the curated collection and installer. Those checks do not replace the tests for a project that uses the workflow.
