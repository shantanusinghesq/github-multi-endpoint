# Contributing

Keep changes focused on personal GitHub workflows across independent endpoint clones. Preserve existing history, distinguish local work from published work, and report inaccessible endpoints honestly.

Use topic branches for changes and run `python scripts/validate_skill.py` before submitting a pull request. Include relevant scenario reasoning from `docs/validation.md`. The solo maintainer can integrate reviewed changes without an independent approving reviewer; passing CI is required on main.

Use synthetic examples. Do not submit credentials, personal machine paths, private project documents, or actual customer repositories. Validators must remain read-only. Changes to supported workflows should explain their authorization boundaries and failure behavior.
