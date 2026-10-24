# Attribution and source integrity

This repository coordinates existing upstream skills. The explicitly requested `setup-agentic-workflow` is one authored integration skill that reads/coordinates the unchanged upstream setup, constraints and context instructions; it is not presented as an upstream Matt/pstack/Addy skill. It does not claim their authorship, rename them into a new suite, or imply upstream endorsement.

| Included source | Copyright / license | Original notice |
|---|---|---|
| Matt Pocock skills | Matt Pocock, MIT | [LICENSE](upstream/matt/LICENSE) |
| pstack and its upstream-generated Claude adapter | Lauren Tan, MIT | [pstack LICENSE](upstream/pstack/LICENSE), [adapter LICENSE](upstream/pstack-claude-code/LICENSE) |
| Addy Osmani agent-skills | Addy Osmani, MIT | [LICENSE](upstream/addy/LICENSE) |
| cursor-team-kit dependencies | Cursor, MIT | [LICENSE](upstream/cursor-team-kit/LICENSE) |

Matt's original PR skill additionally preserves [credit to Dex Horthy's show-me skill](upstream/matt/skills/engineering/pr/CREDITS.md). All additional upstream attribution remains with the original files.

The exact repository URLs, revisions, included subdirectories, active original-skill selection and omitted source-symlink records are in [sources.lock.json](sources.lock.json). Original regular-file and active-copy hashes are in [upstream/checksums.json](upstream/checksums.json). Active copies preserve original metadata, names, instructions and resources. The lock also records 27 original executable paths, preserved in the Git index; tests verify the staged/checked-out blobs are byte-identical to the recorded originals. Coordination and host limitations are documented separately.

Source symlinks are recorded rather than instantiated for Windows portability: Matt's root AGENTS.md link targets its included CLAUDE.md; Addy's OpenCode skill-directory link targets its included canonical skills. Neither is a missing dependency of the shared project discovery view. No source Git history, credentials or node_modules are included.

The frontend-design and ui-ux-pro-max skills are not redistributed in this collection. They remain explicit external dependencies with their own provenance, versions and license terms.

Upstream license grants apply to their material. No single blanket copyright claim is made over third-party content. The repository is public at the user's explicit request. Publishing this collection does not authorize deployment, PR publication or other operations in projects that install it.
