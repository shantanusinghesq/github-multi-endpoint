# Repository-agnostic readiness and handoff checklist

## 1. Establish scope and authority

- [ ] Identify the actual repository root (the current directory may be inside `.git`), applicable project instructions, local default branch, intended GitHub owner/repository, visibility, transport, and endpoint inventory.
- [ ] Distinguish source-document instructions and historical approvals from the current user's authorization. Resolve material ownership or visibility ambiguity before publishing.
- [ ] Identify authoritative specifications and reference renderings; preserve their distinction. Do not invent missing product inputs or start unrelated application implementation.
- [ ] Define GitHub main as the integrated publication baseline and independent endpoint clones as working copies. Preserve an existing default branch name unless renaming is requested.

## 2. Inspect before changing

- [ ] Inspect worktree status, current branch, commits, remotes, upstream tracking, worktrees, and repository-local settings. Preserve existing `.git`, files, and history; do not reinitialize an existing repository.
- [ ] Verify authenticated GitHub identity and access to the intended owner separately. Authentication to one account does not establish permission to create repositories under another.
- [ ] Fetch the intended remote before comparing ancestry. Classify local branches as equal, ahead, behind, divergent, or unrelated; handle an unborn branch separately.
- [ ] Preserve uncommitted and unpushed work. Do not reset, clean, overwrite, force-push, auto-stash, or combine unrelated histories as a shortcut. Resolve divergence through an explicit history-preserving plan within authorization.

## 3. Establish portable repository policy

- [ ] Preserve the project's existing structure; create only purposeful files needed for this repository. Bootstrap does not imply a Python package, test hierarchy, or empty directory scaffold.
- [ ] Define appropriate tracked text normalization in `.gitattributes`, including binary exceptions, and editing conventions where useful. Review normalization changes separately in existing repositories.
- [ ] Check relevant portability hazards: case-only path collisions, OS-specific filenames, executable bits, symlinks, hard-coded machine paths, and platform-specific scripts.
- [ ] Keep credentials, local environments, caches, generated outputs, and restricted datasets out of tracked content. Tailor ignores to actual project needs and use sanitized examples where helpful.
- [ ] Inspect already tracked and staged files: ignore rules do not untrack files or remove secrets from history. If a secret is found, avoid printing it, address exposure and credential rotation, and treat history rewriting as a separate coordinated action.
- [ ] Choose size limits and artifact storage based on actual needs. Use LFS only for an agreed tracked-binary use case; confirm access on every endpoint if used.
- [ ] Configure fast-forward-only pulls locally where agreed. Keep identity and credentials endpoint-specific; do not alter global settings unnecessarily.
- [ ] Document setup, validation, artifact policy, and endpoint handoff. Run appropriate read-only checks; fixes remain reviewable edits. Distinguish expected dirty state before committing from a required clean handoff state.

## 4. Publish or reconcile the central remote

- [ ] Reuse and verify an existing remote where suitable. Create a personal GitHub repository only within authorized scope and confirmed ownership/visibility; avoid an independently initialized remote when publishing existing local history.
- [ ] Review the staged diff and relevant checks before committing. Respect existing signing conventions without assuming signing is configured.
- [ ] Push the intended branch and set upstream tracking. Fetch and verify the local commit matches the intended remote branch after publication; do not infer success from a local commit alone.
- [ ] Keep main stable and use short-lived topic branches for substantive work. Integrate finished work to GitHub main before claiming that it is in the central baseline. A topic-branch push alone does not update main.
- [ ] Check the actual personal plan and visibility before applying branch protections or rulesets. If available and requested, prevent force-push and deletion on main; require only checks that actually exist and can run. Avoid review requirements a sole owner cannot satisfy.
- [ ] When protections are unavailable, record that fact and document no-force-push, no-delete, review, and check conventions. Local checks are bypassable and are not server protection. Do not change visibility or purchase a plan to obtain enforcement without authorization.

## 5. Validate every endpoint

- [ ] Clone independently into a deliberate location outside live file-sync management of `.git`; never use a shared or cloud-synchronized `.git` directory as transport.
- [ ] Verify authentication, expected remote, branch/upstream, and commit identity on each accessible endpoint. Use separate local environments and locally supplied secrets.
- [ ] Run the project's relevant setup and checks on each OS in scope. Identify legitimate platform differences; compare normalized Git content or commit identity rather than raw checkout hashes when line endings differ.
- [ ] Verify read access by fetch/clone and write access through an authorized disposable topic branch. Never alter main merely to test permissions. Track any test branch cleanup within the authorized scope.
- [ ] A fresh disposable clone can validate published completeness, but cannot prove that an inaccessible computer works. Mark inaccessible endpoint checks PENDING with exact instructions and evidence required.
- [ ] Delete a disposable clone only after confirming its resolved path, task ownership, and absence of needed work. Keep existing user checkouts.

## 6. Repeat at each handoff

- [ ] Sending endpoint: inspect changes, run relevant checks, review and commit intended files, push the active branch, and verify publication. Record repository, branch, commit, validation, outstanding work, and receiving endpoint.
- [ ] Integrate completed work to main through the agreed process and update local tracking state. Clearly label unfinished work handed off on a topic branch.
- [ ] Receiving endpoint: inspect and preserve local work first, fetch, select the recorded branch, and update with `git pull --ff-only` when tracking is configured. Verify the expected commit before editing.
- [ ] If fast-forward fails or local work conflicts, stop automatic synchronization and inspect divergence. Do not force convergence or silently create a merge.
- [ ] Assign one active endpoint per branch at a time. Concurrent work uses separate branches and explicit integration. Repeat these rules for every additional endpoint.
- [ ] Offline work remains local until pushed; do not represent it as available on GitHub. Record any excluded local-only materials needed to reproduce the work separately.

## Completion report

Report the remote/default branch and verified commit, endpoint results, portability and checks, enforcement limitations, outstanding unpublished work, and any pending endpoint validation. Include exact handoff commands with resolved values when known; label template values clearly and never embed credentials.

## Official references

Consult these when relevant; feature availability must be rechecked when executing:

- [GitHub protected branches and plan availability](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches)
- [Git pull and fast-forward behavior](https://git-scm.com/docs/git-pull)
- [GitHub line-ending policy](https://docs.github.com/en/get-started/git-basics/configuring-git-to-handle-line-endings)
