# Contribute to Maks Agentic Workflow

The repository is public. Anyone can open an issue or submit a pull request. Only the repository owner merges changes to `main`.

## Report a problem or propose an idea

Open an issue with the affected workflow, host, expected behavior, and relevant output. Do not include credentials, private prompts, customer data, or unredacted session logs.

## Submit a change

1. Fork the repository and create a focused branch.
2. Make a small change. Preserve original upstream skill content and licenses unless the change explicitly updates a pinned source version.
3. Run the relevant checks:

   ```bash
   python -m unittest discover -s tests -v
   git diff --check
   ```

4. Open a pull request against `main`. Explain the problem, scope, and checks you ran. Link any related issue.
5. Wait for the repository owner to review and merge. Contributors cannot push directly to `main` or merge pull requests.

Use **Create a merge commit** or **Rebase and merge** to preserve individual commit authorship in the repository history. Squash merging is disabled so GitHub retains each contribution as a separate commit. GitHub can credit each author when the commit email is linked to that author's account. Merge and rebase methods retain the source commits; the merge commit itself is not the contributor credit.

The `main` ruleset requires a pull request, an owner/code-owner review, and resolved review threads. Only repository admins can update `main`, and the only configured bypass is PR-only. The owner is the only current administrator. Do not add required CI checks until this repository has a configured workflow that reports them.

## Update upstream skill material

Keep the upstream source under `upstream/` and the filtered project installation separate. Pin the source revision, preserve license notices, update the curated copies and checksums together, and test both the collection and consumer installer. Do not add an entire upstream catalog to the installed discovery set without updating and reviewing `workflow/selection.json`.
