# Validation and honest limits

## Current setup cleanup

Only `setup-agentic-workflow` is installed as setup. Both standalone Matt/pstack setups are removed; their pinned instructions/templates are non-skill `.txt` references bundled with the coordinator. The current profile has 22 entries (21 original + combined setup), 53 on-demand helpers and 74 original skills. Known prior compact installs safely retire unchanged owned copies. [Retirement checks and scope](../../validation/setup-retirement.md).

The earlier counts and runs below are historical validation of the preceding profiles.

## What the local collection checks

Run:

```bash
python -m unittest discover -s tests -v
```

The read-only tests verify:

- 1,084 recorded source/discovery/resource file hashes and Git-index blob identity, so line-ending filters cannot silently change the preserved originals.
- 27 original executable flags, including their matching discovery copies, preserved in the Git index.
- Five pinned source-package snapshots, original licenses and recorded source-symlink handling.
- 105 unique active skill names, unchanged original metadata/content/resources, and the exact curated source mapping.
- Complete pstack skill/principle/playbook inclusion, its original agent definitions on disk, and Matt's composed planning dependencies.
- One shared-view `tdd` owner (pstack) and the distinct original Addy feature-testing supplement.
- Addy's original root-shared reference layout and the supplied control-ui/control-cli/deslop dependencies.
- Presence of the actual Matt, Addy and upstream-generated pstack Claude loader manifests; cursor-team-kit is correctly identified as Cursor-native rather than advertised as a fourth Claude plugin.
- Links and whitespace in this repository's own guide/research/planning documents.

This proves collection integrity/layout, not that an app works, an agent is registered, a host is authenticated, a browser is installed or a deployment is safe. No upstream setup hooks, automations, watchers, dependency installers, PR publishing or deployment commands are run by these tests.

## Compact installer

The consuming-project command is now `python scripts/install.py --project <project> --host pi`; it does not copy the 105-entry source/archive view. It advertises 22 original entry points and retains 54 used/required original helpers privately, on demand. [Installation instructions](install.md) document selection and safety.

The full regression passed **49 tests**, followed by **3 targeted final checks** including the added filesystem-boundary test. A real read-only Pi run successfully loaded original grill-with-docs and its grilling/domain-modeling helpers from the private canonical tree, with zero tool errors and unchanged installed checksums. [Detailed installer evidence and limits](../../validation/compact-installer.md).

## Public GitHub bootstrap

The repository is now public at the user's request. The [root bootstrap](../../install.py) supports the direct GitHub URL command in [installation instructions](install.md), using only Python and a temporary download, with no permanent clone or GitHub credentials. It delegates to the same curated installer and preserves caller-relative target paths.

The latest full regression passed **63 tests**, including public-download failure handling, archive traversal/link/size checks, cleanup, argument/CWD forwarding and refusal to install into another source/archive checkout. Unit network responses are mocked; the published URL is smoke-tested after the first main push. Downloading temporary source does not install all three catalogs into the project.

## Unified setup update

The user-requested `setup-agentic-workflow` adds one coordinator to the unchanged 22 original entries (23 total; 54 original helpers still on demand). It combines Matt/pstack setup and Addy constraints/context, including canonical AGENTS.md initialization and preservation. Existing 22-entry installs support the exact non-destructive additive update by rerunning the same installer.

The full suite passed **73 tests**, followed by **3 packaging/upgrade checks** after adding explicit-only Codex metadata. Two live read/write/edit fixture runs read all four original component files, created/preserved AGENTS.md, configured local docs/constraints, preserved original skill files/managed blocks and left globals unchanged. Model configuration/enforcement limitations were reported as pending. The older baseline left AGENTS.md absent when CLAUDE.md existed. These are limited controlled cases, not universal host guarantees. [Unified setup evidence](../../validation/unified-setup.md).

## Host coverage

| Host | Established facts | Not established by file checks |
|---|---|---|
| Pi | Agent Skills discovery format documented; executable and authenticated research model available; shared originals can be explicitly selected | Cursor Task environments/model slugs/named agents, full poteto-mode execution, all application-runtime behavior |
| Claude Code | Executable found; original native package manifests and pstack's own adapter included | Authentication, multi-plugin execution and all external dependency registration |
| Codex | Executable found; documented .agents discovery and explicit skill invocation | Authentication, original pstack tool/model compatibility and full execution |
| Cursor | Documented .agents discovery; original pstack package and dependencies included | CLI on PATH, GUI availability, cloud agents/models/native-agent registration and live execution |

Skill format compatibility is not identical automation compatibility. This collection does not re-author originals to hide missing host capabilities.

## Behavioral probe boundaries

Read-only prompt/routing probes can check whether the documented composition chooses Matt planning, poteto-mode execution and relevant Addy disciplines, respects a planning/read-only request, and admits missing capabilities. They do not implement a feature, reproduce a real app bug or verify a production deployment.

A real project acceptance run still needs:

1. An ambiguous feature planned by Matt, then an explicitly approved ticket implemented by poteto-mode with actual tests.
2. A real bug demonstrated failing before and passing after on the relevant surface.
3. A documentation/architecture task checked against source, with no unauthorized production-code changes.

Selected no-collection comparisons can reveal prompt/role differences under comparable conditions; they are not a statistically general benchmark or proof that one combination is optimal.

## Preserved upstream caveats

- Pstack defaults can continue design into implementation, take reversible external actions, remove comments or open ready PRs. The explicit project request/instructions supply the approved gates and useful-rationale policy; source bodies are unchanged.
- Matt's HEAD-based code-review diff can miss uncommitted work. Specify the actual intended patch and revalidate after changes.
- Pstack TDD is selective; include the relevant original Addy test/runtime skill when feature behavior needs it.
- Original source examples are not universal constraints, and original control-cli Unix examples are not Windows runtime evidence.
- Package files on disk do not automatically register native agents or make absent tools/accounts exist.
- Upstream relative links to author-repository maintenance documents are not all runtime dependencies. The collection tests check the known runtime resource mappings, not the claim that every upstream external/documentation link is valid forever.

## Recorded results

- **Collection suite:** `python -m unittest discover -s tests -v` passed all 8 tests, including all 1,084 recorded hashes, exact active-copy comparisons, Git-index byte identity and 27 executable modes.
- **Read-only composition probes:** four runs on `openai-codex/gpt-6-luna`, high reasoning, read tool only, exited successfully. Manual inspection confirmed the expected ownership and approval/evidence boundaries:

| Probe | Observed result | Recorded response |
|---|---|---|
| Vague feature | Matt's original planning/spec/ticket path; implementation deferred until approval; poteto-mode receives the artifacts | [Feature](../../validation/probes/feature-collection.md) |
| Approved bug explanation | poteto-mode owns the bounded fix/test/retest loop; no root cause or test result invented without source/repro | [Bug](../../validation/probes/bug-collection.md) |
| Read-only architecture/docs | Correct ownership and Addy mapping; no code mutation or claim that files prove host runtime support | [Architecture](../../validation/probes/architecture-collection.md) |

- **No-collection comparison:** [feature baseline](../../validation/probes/feature-baseline.md) used the same feature prompt, model, effort and read tool but an isolated empty workspace with no collection/guide/context discovery. Initial non-isolated baselines could read the guide and were discarded and rerun. The isolated feature baseline could not verify actual skill names; the collection run named the actual chain. Both baselines still respected broad user-specified ownership and missing-evidence limits. This is a qualitative difference, not a statistical performance claim.
- Responses and prompt/process metadata are under `validation/probes/`. Print-mode records retain final responses, not complete tool-call traces; manual checks assess those responses only and do not prove every skill was loaded or every potential side effect would be blocked.

The three **real-project** application acceptance runs listed earlier have **not** happened. No live application tests, full poteto-mode execution, other-host authentication/behavior, real independent reviewer fleet, PR publication, merge or deployment are claimed.
