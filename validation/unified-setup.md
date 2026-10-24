# Unified setup validation

## Scope

`setup-agentic-workflow` is the one integration skill explicitly requested by the user. It coordinates unchanged Matt/pstack setup instructions and Addy's actual constraint/context skills. Addy has no dedicated upstream setup command. The default setup path is one invocation; original commands remain available for compatibility.

The installer now exposes **23 entries: 22 unchanged original entries plus the setup coordinator**. The 54 original helpers remain on demand and the 76 original skill bodies remain unchanged. Codex metadata makes the setup coordinator explicit-only, alongside the SKILL.md invocation flag used by other hosts.

## Deterministic checks

The full suite passed **73 tests** in 152.767 seconds, including the 10 new setup/compatibility cases. These cover:

- New coordinator identity, original component availability and separation from upstream originals.
- Installed canonical/public bodies and host invocation/runbook instructions.
- Exact non-destructive additive update from the prior 22-entry installation, with original files and user rules preserved.
- Refusal to hide a missing helper, altered ownership/count record, locally edited original or conflicting custom setup inside that update.
- Setup documentation appended outside installer-owned markers remains compatible with installer verification and idempotent reinstallation.
- Existing source integrity, host layouts, resource paths, safety/rollback and public bootstrap tests continue to pass.

After packaging metadata changes, **3 final targeted checks passed**, including explicit-only metadata and the safe additive-update/missing-helper regressions. No upstream snapshot files are edited.

## Live setup cases and baseline

Two controlled fixture projects ran through real Pi CLI sessions using `openai-codex/gpt-6-luna`, high reasoning, with only read/write/edit tools. Project-document changes were pre-approved; tools, global edits, shell commands and external operations were not. Test home directories were isolated, and installed originals/markers were checked afterward.

| Case | With the coordinator | Previous published workflow, without it |
|---|---|---|
| Missing AGENTS.md, existing customized CLAUDE.md | Created canonical AGENTS.md; configured local Matt docs and written-only constraints; preserved CLAUDE/user rules and globals; reported pstack/enforcement pending | Configured docs but followed the older preference for CLAUDE.md and left AGENTS.md absent |
| Existing customized AGENTS.md | Preserved exact user-rule bytes and managed block; added one setup section and local docs; kept globals unchanged and unsupported capabilities pending | Also preserved the existing AGENTS.md and configured the local docs |

Tool-call receipts confirmed both coordinator runs read all four original setup/constraint/context files. All seven artifact/scope checks passed in each coordinator run. The prior-workflow baseline passed six/seven checks in the missing-AGENTS case and seven/seven in the existing-file case. These two examples are not a statistical claim of general superiority. Missing-file audit reads/retries occurred; the final artifacts, write scope and integrity checks passed. No actual checker installation/enforcement, real user-home configuration, native model/delegation setup or production behavior is claimed.

The exact output files and tool traces are retained locally under ignored `validation/raw/setup-agentic-workflow-workspace/`. A static review viewer generated with the upstream skill-creator tooling is at `validation/raw/setup-agentic-workflow-workspace/review.html`; it is local review material, not installed context or published fixture data.

## Remaining honest boundaries

The skill can configure approved project documents across hosts, but actual model availability, native agent tooling, global pstack rule writes and quality-check installations require their real prerequisites and explicit grants. A written CONSTRAINTS.md is not called enforced or passing when its checkers are missing. AGENTS.md initialization is not permission to implement code, rewrite existing instructions or modify installer-owned marker content.
