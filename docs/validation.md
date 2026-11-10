# Initial scenario review

These are manual reviews of the instructions, not executions against real user endpoints.

| Scenario | Instruction outcome reviewed |
|---|---|
| Empty local repository | Detect unborn branch; publish intended history without unrelated starter commits |
| Existing history | Preserve Git database, layout, branch names, and history |
| Dirty or unpushed work | Preserve and inspect before handoff; do not claim remote completeness |
| Divergent branches | Stop automatic fast-forward synchronization and inspect ancestry |
| Inaccessible second endpoint | Mark validation pending and give evidence requirements |
| Three or more endpoints | Independent clones and one active endpoint per branch |
| Private repository on Free plan | Check actual feature eligibility; disclose unavailable enforcement |
| Account differs from intended owner | Verify ownership permission separately before publishing |

The status script was exercised on Linux against local repositories in these states: unborn branch, clean and published, uncommitted and stashed work, ahead, remote moved since last fetch, divergent, detached HEAD, and outside a repository. Each produced the expected report and exit code, and no file in the Git directory changed (compared by modification time and size) across runs with and without `--remote`. CI runs it once on Windows and macOS as a smoke test only.

All scenarios are covered by the package instructions. Structural validation and isolated copy checks establish package integrity only. CI on Windows and macOS validates package structure and links; it does not validate physical endpoint authentication or prove model behavior under every prompt.
