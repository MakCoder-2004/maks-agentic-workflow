# feature: baseline

Model: openai-codex/gpt-6-luna, high. Tools: read only. Scope: routing/permission explanation, not application implementation. Exit code: 0.

Baseline isolation: empty temporary workspace, no collection/guide files, no discovered skills/context, same task/model/effort/read tool.

### Ownership
Matt should own discovery and the eventual spec/tickets, matching your preference. I can’t verify the exact names of the skills installed for Matt, poteto-mode, or Addy, so I won’t guess or invent them.

### Next steps
Before selecting a skill, please share the available skill names or point me to their repository files. Then use Matt’s existing planning/spec skill to clarify:
- Who submits requests, reviews them, and acts on them?
- What problem are requests meant to solve, and what’s in or out of scope?
- What are the request states, transitions, and required information?
- What does success look like? Any permissions, notifications, integrations, or reporting needs?
- What constraints or examples should shape the first version?

### Gates
Planning only for now: no implementation, testing, PR, or lifecycle work. Once you approve the requirements and acceptance criteria, Matt can turn them into tickets. The later handoff should give poteto-mode the approved spec, scoped tickets, acceptance criteria, and relevant constraints; Addy can cover the lifecycle when that work is authorized.

### Evidence limits
I could not find readable repository files at the attempted skill/documentation paths, so I can’t confirm which actual skills are available or their exact names. No code changes or tests were performed.
