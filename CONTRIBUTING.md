# Contribute to Maks Agentic Workflow

Issues and pull requests are welcome. Only the repository owner merges changes to `main`.

## Report a problem or propose an idea

Open an issue with the affected workflow, host, expected behavior, and relevant output. Do not include credentials, private prompts, customer data, or unredacted session logs.

## Submit a change

1. Fork the public repository and create a focused branch.
2. Make a small change. Preserve original upstream skill content and licenses unless the change explicitly updates a pinned source version.
3. Run the relevant checks:

   ```bash
   python -m unittest discover -s tests -v
   git diff --check
   ```

4. Open a pull request against `main`. Explain the problem, scope, and checks you ran. Link any related issue.
5. Wait for the repository owner to review and merge. Contributors cannot push directly to `main` or merge their own pull requests.

The `main` branch requires a pull request, an owner/code-owner review, and resolved review threads. Do not add required CI checks until this repository has a configured workflow that reports them.

## Update upstream skill material

Keep the upstream source under `upstream/` and the filtered project installation separate. Pin the source revision, preserve license notices, update the curated copies and checksums together, and test both the collection and consumer installer. Do not add an entire upstream catalog to the installed discovery set without updating and reviewing `workflow/selection.json`.
