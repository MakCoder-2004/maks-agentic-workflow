# bug: collection

Model: openai-codex/gpt-6-luna, high. Tools: read only. Scope: routing/permission explanation, not application implementation. Exit code: 0.

**Ownership**  
Original pstack `poteto-mode` owns implementation and per-ticket verification. Matt owns planning and the approved ticket remains authoritative. Work only if its blockers are done.

**Next steps**  
Read the ticket and relevant project constraints, source, tests, and test commands. Reproduce “cached records remain stale after expiration” on the affected surface. Add a focused behavior check that fails before the fix, where practical. Diagnose from evidence rather than assuming a root cause. Implement the bounded fix, verify the check passes, run nearby regressions and relevant build/runtime checks, then apply applicable Addy checks. Fix findings and rerun affected checks before recording evidence or moving to another ready ticket.

**Gates**  
Stop if the symptom cannot be reproduced, requirements are ambiguous, or safe resolution needs broader scope. Preserve the evidence and report the blocker. Failed, missing, or inconclusive checks are not passes. Publication and deployment require separate authorization.

**Evidence limits**  
This probe read the repository workflow and original testing/debugging guidance only. No application source or reproduction was supplied, so the cause is unknown. No tests or runtime checks were run, and no changes, publication, or deployment occurred.
