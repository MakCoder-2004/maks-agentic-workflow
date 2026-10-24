# Compact installer validation

The [installer](../scripts/install.py) is for the agreed original-skill combination, not three whole upstream installations. [Selection](../workflow/selection.json) and [usage/safety](../docs/guide/install.md) are explicit.

## Target footprint

- **22 advertised original entry points:** Matt 9, original poteto-mode 1, selected Addy lifecycle skills 12.
- **54 on-demand original helpers:** including pstack's required 24 principle leaves, outside all installed skill-discovery roots.
- **76 distinct original skills available**, not 76 startup descriptions. Public entry copies/resources and their private canonical originals remain byte-identical to pinned source files.
- No full source archives, competing implementation controllers, plugin catalogs, auto hooks, automation packs, global setup, credentials or replacement SKILL.md files are installed.
- Original poteto-mode's own embedded playbooks/resources remain intact; this is not a claim that its unchanged body or every optional feature consumes no context.

## Deterministic tests

Initial installer coverage passed 36 tests. A fresh-context, tool-disabled review identified permission/concurrent-rollback and incomplete-manifest risks. Those were repaired and targeted regression tests passed, alongside the existing rollback/update cases.

The final full-suite result is recorded below after integration. Tests cover compact discovery, four host file layouts, original bytes, bundled/shared resource paths, native role files, command execution from an unrelated working directory, paths with spaces, dry-run/check/idempotence, preservation of existing instructions/user skills, duplicate identities, unowned/edited files, malformed/incomplete state, source provenance, POSIX permission intent, Git normalization, Windows junction refusal, transaction rollback and detected concurrent edits. File-layout tests do not prove all four native clients execute the workflow.

## Live Pi helper-loading smoke

A fresh temporary consuming project was installed for Pi. The real CLI ran with `openai-codex/gpt-6-luna`, high reasoning, read tool only, fresh in-memory context, no extensions/MCP/global skill discovery, and only the target's public entry directory explicitly selected. The generated project coordination block was supplied as context.

The request was planning-only: use original grill-with-docs and its original grilling/domain-modeling helpers; do not write files or claim application implementation/testing.

Recorded tool-execution events showed exactly these reads, relative to the target:

1. `.maks-agentic-workflow/WORKFLOW.md`
2. `.maks-agentic-workflow/registry.json`
3. `.maks-agentic-workflow/originals/matt/skills/engineering/grill-with-docs/SKILL.md`
4. `.maks-agentic-workflow/originals/matt/skills/productivity/grilling/SKILL.md`
5. `.maks-agentic-workflow/originals/matt/skills/engineering/domain-modeling/SKILL.md`

The final reply correctly distinguished the two private helper files from advertised skill entries, described Matt -> poteto-mode -> Addy ownership and asked an initial user-problem question. No unrelated helper bodies were read. There were **zero tool errors**, a successful settled event and a normal final assistant stop. All installed checksums/instructions still verified afterward. The discovery directory contained **22** SKILL.md files, not the 105-entry source repository view.

Raw JSONL/diagnostics are retained locally under ignored `validation/raw/compact-installer/`, not required by the installed workflow. These receipts establish the tested read-only original-helper loading path. They do **not** establish production implementation, native delegation, full independent review, real browser testing, deployment, every optional pstack feature or full Claude/Codex/Cursor runtime compatibility.

## Review boundary

The fresh-context review was static, not execution. Its concrete findings were handled as follows:

- Compare content **and permissions** with preflight state before replacing a file.
- During rollback, preserve a concurrently changed/inaccessible path and report incomplete cleanup rather than restoring over a user's edit; continue rolling back other files.
- Validate complete expected inventory, source provenance, permissions and the required managed instruction record, so deleting a hidden helper plus its manifest record cannot falsely pass `--check`.
- Describe host output as documented file layout, not a proof of native runtime support.
- Explicitly treat install.json as trusted local bookkeeping, **not a signed or independently protected ownership boundary**. A coordinated attacker who can fabricate both project files and their ownership records is not authenticated by checksums. No misleading tamper-proof claim is made.

A follow-up review found no other functional blocker within the documented trusted, idle-project scope. It highlighted that pathname checks are not race-proof against an adversarial directory swap between check and write. This limit is explicit in code/docs, and a disposable-fixture test demonstrates it rather than claiming a security sandbox. Do not run elevated against an adversarial/concurrently manipulated filesystem.

The command does not delete obsolete installs, force overwrite local changes, migrate hosts or modify the consuming project's Git index. Existing global skills/plugins and their context cost are not controlled by this project-local install.

## Final integration result

- Full regression: **49 tests passed** in 117.570 seconds before the final documentation-only safety clarification and its added boundary test.
- Final quick check: **3 targeted tests passed**, including the added boundary demonstration, exact compact selection and document links; authored changes passed `git diff --check`.
- Current-code live Pi recheck: successful normal stop/settled event, five canonical/runbook/index reads listed above, zero tool errors, and installed integrity still valid afterward.
- During those checks no consuming user project, global configuration, Git commit/push, PR or deployment was changed; installations used disposable test projects.
- Subsequent public-GitHub bootstrap integration passed **63 tests** in 100.629 seconds. The user then authorized publication of all work to main and made the repository public. The new command fetches temporary public source and delegates to this same curated selection, not three whole target installations.
