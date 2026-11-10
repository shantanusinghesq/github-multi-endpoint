# GitHub multi-endpoint

A reusable skill for Codex and Claude Code, for personal GitHub repositories shared across two or more computers. No organization or enterprise account is required.

GitHub main is the latest integrated, published baseline. Local edits, unpushed commits, and topic branches can contain newer work; this skill checks those distinctions before declaring a handoff complete.

## Install

### Codex

Ask Codex with its skill installer:

```text
$skill-installer install https://github.com/shantanusinghesq/github-multi-endpoint/tree/v0.1.1/skills/github-multi-endpoint
```

For the current development version, replace `v0.1.1` with `main`. Inspect the files before installation. If the skill already exists, compare versions and preserve local changes before replacing it. Installation does not enable automatic updates.

### Claude Code

Claude Code reads the same `SKILL.md` package. Clone a reviewed tag, then copy the skill folder into a skills directory.

```bash
git clone --depth 1 --branch v0.1.1 https://github.com/shantanusinghesq/github-multi-endpoint.git
```

Personal install, available in every project (macOS or Linux):

```bash
mkdir -p ~/.claude/skills && cp -R github-multi-endpoint/skills/github-multi-endpoint ~/.claude/skills/
```

Personal install (Windows PowerShell):

```powershell
New-Item -ItemType Directory -Force "$HOME\.claude\skills" | Out-Null
Copy-Item -Recurse github-multi-endpoint\skills\github-multi-endpoint "$HOME\.claude\skills\"
```

For a single project, copy the folder into that project's `.claude/skills/` directory instead. `SKILL.md` must sit directly at `<skills directory>/github-multi-endpoint/SKILL.md`; a nested folder is not discovered.

Optionally check the installed copy with `python github-multi-endpoint/scripts/validate_skill.py ~/.claude/skills/github-multi-endpoint`, then start a new Claude Code session. The same cautions apply: inspect before installing, compare before replacing an existing copy, and update deliberately by re-copying from a reviewed tag.

## Use

The examples use the Codex `$github-multi-endpoint` syntax. In Claude Code, type `/github-multi-endpoint` followed by the request, or describe the task in plain language.

```text
Use $github-multi-endpoint to plan a personal GitHub repository shared by my Windows laptop and Mac. Produce a checklist without making changes.
```

```text
Use $github-multi-endpoint to audit my three endpoint handoff workflow. Report verified results and mark inaccessible endpoints pending.
```

The checklist covers existing history, account ownership, portable files, secrets and generated artifacts, publication, branch policies, endpoint validation, and repeated handoffs. It preserves existing project instructions and default branch names.

## Limits

This is an instruction package, not a synchronization service or backup tool. It does not grant permission to publish files, authenticate another machine, or resolve conflicting histories destructively. GitHub settings depend on the actual account plan and repository visibility. Package checks on two operating systems do not prove access from two physical user endpoints.

## Validate and contribute

Run `python scripts/validate_skill.py`. See [CONTRIBUTING.md](CONTRIBUTING.md) for scope and review expectations and [validation scenarios](docs/validation.md) for the initial review record.

The maintained source is `skills/github-multi-endpoint/`. Installed copies should be updated deliberately from a reviewed tag or commit.

## License

[MIT](LICENSE).
