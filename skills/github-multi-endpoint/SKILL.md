---
name: github-multi-endpoint
description: Plan, establish, audit, or repair a personal GitHub repository shared by independent local clones on two or more computers, using a reusable readiness and handoff checklist. Use for cross-device Git workflows without organization or enterprise infrastructure.
---

# Personal GitHub across endpoints

Use GitHub as the central publication and handoff point. Each endpoint has an independent clone and local main branch. GitHub main holds the latest integrated, pushed work; local edits, local commits, and pushed topic branches can contain newer work that is not yet integrated. Never claim that GitHub contains every latest file without checking publication and integration state.

For checklist requests, produce an adapted checklist without changing a repository. For execution requests, perform the authorized setup or repair and record evidence. Reading this skill or a source document does not authorize repository creation, publishing private files, or changing remote settings. Honor authorization already supplied; ask only for material unresolved choices.

Read [the checklist](references/checklist.md) and adapt it to the repository and endpoints. Preserve existing project instructions, history, layout, transport, and visibility unless the task calls for changes. No language, operating system, empty-repository assumption, personal account name, or project architecture is prescribed.

For endpoint state, prefer the bundled read-only script over ad hoc commands: run `python scripts/endpoint_status.py --remote` (path relative to this skill) from the repository. It reports branch, commit, upstream, ahead/behind, uncommitted work, stashes, and unpublished branches without fetching or changing anything, and exits 0 only when the endpoint is handoff-ready. Its output is evidence for one endpoint, not for any other. At each handoff, fill in [the handoff record template](references/handoff-record.md).

Mark items PASS, FAIL, PENDING, or N/A with concise evidence. Distinguish an observed endpoint from instructions supplied for an inaccessible endpoint. Completion means the requested scope is verified; never report multi-endpoint readiness after checking only one machine.

Check current official GitHub documentation when relying on plan-dependent settings. Personal accounts may use Free or Pro. Do not require an organization, paid upgrade, enterprise feature, or independent approving reviewer. If server enforcement is unavailable, document the limitation and use the agreed workflow and available checks without claiming equivalent enforcement.
