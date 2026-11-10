# Handoff record template

Fill one record per handoff. Values in `<angle brackets>` are placeholders: replace every one, or write `none` or `N/A`. Keep the record where the receiving endpoint will read it (a pull request description, an issue comment, or an agreed notes location). Never include credentials, tokens, or secret values; name where a secret is supplied instead.

Most sending fields come straight from the status script, run from the repository on the sending endpoint:

```text
python <path to this skill>/scripts/endpoint_status.py --remote
```

The script is read-only. It reports `READY` only when the worktree is clean, the branch has an upstream, and the two are level. Paste its output under Evidence.

## Sending endpoint

- Date and time (UTC): `<YYYY-MM-DDTHH:MMZ>`
- Sending endpoint: `<name and operating system>`
- Receiving endpoint: `<name and operating system>`
- Repository: `<owner/repository>`
- Branch: `<branch>` (`<integrated on main | unfinished topic branch>`)
- Commit: `<full commit hash>`
- Published: `<PASS | FAIL>` (remote branch tip equals the commit above)
- Worktree clean: `<PASS | FAIL>`
- Checks run: `<command and result, or none>`

### Left behind on the sending endpoint

- Unpushed branches or commits: `<list, or none>`
- Stashes: `<count and purpose, or none>`
- Untracked or ignored files needed to reproduce the work: `<list, or none>`
- Local-only settings or secrets the receiver must supply: `<names only, or none>`

### Work state

- Done in this session: `<short summary>`
- Outstanding: `<next steps, or none>`
- Known problems: `<failing checks, open questions, or none>`

### Evidence

```text
<paste endpoint_status.py --remote output from the sending endpoint>
```

## Receiving endpoint

Complete this half on the receiving endpoint before editing anything.

- [ ] Existing local work inspected and preserved: `<PASS | FAIL | N/A>`
- [ ] Fetched, then selected the recorded branch: `<PASS | FAIL>`
- [ ] Updated with `git pull --ff-only`: `<PASS | FAIL | N/A>` (on failure, stop and inspect divergence)
- [ ] `HEAD` equals the recorded commit: `<PASS | FAIL>`
- [ ] Project setup and checks on this operating system: `<command and result, or N/A>`
- Result: `<verified | PENDING, with what remains and the evidence required>`

```text
<paste endpoint_status.py --remote output from the receiving endpoint>
```

A record whose receiving half is not filled in describes a handoff that is published, not one that is verified.
