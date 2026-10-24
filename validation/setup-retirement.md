# Standalone setup retirement

At the user's request, `setup-matt-pocock-skills` and `setup-pstack` are no longer installed or registered skills. `setup-agentic-workflow` is the only setup entry.

## References, not separate skills

The combined setup bundles the unchanged original setup instructions as `references/matt/SETUP.txt` and `references/pstack/SETUP.txt`, with Matt's necessary templates and both upstream licenses. These are deliberately not SKILL.md files or legacy Markdown skill entries. Their bytes are verified against the pinned upstream originals. Addy's constraints/context components remain the existing original skills.

Pinned upstream snapshots remain read-only provenance; their standalone setup files are not copied as skills into projects. Both old setup copies were also removed from this repository's discovery view, now 103 original archive entries.

The current consumer profile is **22 entries: 21 original skills plus combined setup**, **53 on-demand helpers**, and **74 original skills**. No extra global skill/plugin removal is attempted.

## Safe existing-project update

The installer recognizes the exact two previously published compact profiles. It removes only their unchanged installer-owned public Matt setup and private Matt/pstack setup files while adding the bundled references. It validates the prior inventory, provenance, original checksums and ownership before any write. A missing helper, changed file, unowned copy, conflicting coordinator or altered inventory blocks migration.

Only empty retired directories are cleaned up. User-added files and instruction text survive. If a later write fails, the removed files are restored as part of rollback; concurrent changes remain protected. There is no general arbitrary pruning or force-delete option. Retired setup commands suggested by upstream texts are redirected to the combined setup in the managed project instructions.

## Checks

- Sixteen targeted retirement/packaging/source checks passed during implementation, including both old profiles and Pi/Claude layouts.
- Coverage includes absence from registry/discovery, original reference bytes/templates, idempotence, local edits/unowned files, user extras, rollback after deletion, corrupt/missing records and a reintroduced standalone setup detected by --check.
- Full regression passed **78 tests** in 169.993 seconds.
- The installed Pi 1.4.0 native skill loader discovered exactly **22 entries**, with **setup-agentic-workflow as the only setup skill** and zero diagnostics. Bundled references were not registered as skills.
- A real public GitHub upgrade from the prior `a19e23f` release removed 16 unchanged owned standalone-setup files, preserved a custom user instruction, retained the combined references and passed remote `--check`.
- Git index validation also covers bundled reference bytes; source attributes preserve their original line endings in published archives.
