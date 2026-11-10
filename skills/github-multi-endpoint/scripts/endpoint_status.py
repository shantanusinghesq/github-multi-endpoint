"""Read-only endpoint status report for a Git repository; standard library only.

Prints the facts a handoff record needs: branch, commit, upstream, ahead/behind,
uncommitted work, stashes, and other local branches with unpublished commits.

Nothing is written: no fetch, no index refresh, no configuration change. Ahead and
behind counts therefore reflect the last fetch on this endpoint. Pass --remote to
ask the remote for its current branch tip (network read, still writes nothing).

Exit codes: 0 handoff-ready, 1 attention needed, 2 not a usable repository.
"""
import argparse
import datetime
import os
import platform
import re
import subprocess
import sys


def git(cwd, *args, timeout=60):
    """Run a git command without optional locks; return (exit code, stdout)."""
    env = dict(os.environ, GIT_OPTIONAL_LOCKS="0", GIT_TERMINAL_PROMPT="0", LC_ALL="C")
    try:
        done = subprocess.run(
            ["git", *args], cwd=cwd, env=env, timeout=timeout,
            stdout=subprocess.PIPE, stderr=subprocess.DEVNULL,
            encoding="utf-8", errors="replace",
        )
    except FileNotFoundError:
        print("git executable not found")
        sys.exit(2)
    except subprocess.TimeoutExpired:
        return 124, ""
    return done.returncode, done.stdout.rstrip()


def redact(url):
    """Drop any user:password@ part so credentials never reach the report."""
    return re.sub(r"(?<=://)[^/@\s]+@", "", url)


def collect(path, ask_remote):
    code, inside_git_dir = git(path, "rev-parse", "--is-inside-git-dir")
    if code != 0:
        print(f"Not a Git repository: {path}")
        sys.exit(2)
    if inside_git_dir == "true":
        print("Current directory is inside the Git directory; run from the worktree.")
        sys.exit(2)
    _, root = git(path, "rev-parse", "--show-toplevel")
    if not root:
        print("No worktree found (bare repository?).")
        sys.exit(2)

    facts, attention = [], []

    def add(label, value):
        facts.append((label, value))

    add("Endpoint", f"{platform.node() or 'unknown'} ({platform.system()})")
    add("Repository root", root)
    _, shallow = git(root, "rev-parse", "--is-shallow-repository")
    if shallow == "true":
        add("History", "shallow clone (ancestry checks are limited)")

    _, remotes = git(root, "remote", "-v")
    fetch_urls = sorted({
        f"{parts[0]} {redact(parts[1])}"
        for parts in (line.split() for line in remotes.splitlines())
        if len(parts) >= 3 and parts[2] == "(fetch)"
    })
    add("Remotes", "; ".join(fetch_urls) or "none")
    if not fetch_urls:
        attention.append("No remote is configured.")

    head_code, head = git(root, "rev-parse", "HEAD")
    _, branch = git(root, "symbolic-ref", "--short", "-q", "HEAD")
    if head_code != 0:
        add("Branch", f"{branch or 'unknown'} (unborn: no commits yet)")
        attention.append("Branch has no commits yet.")
    else:
        add("Branch", branch or "detached HEAD")
        _, summary = git(root, "log", "-1", "--format=%h %cI %s")
        add("Commit", head)
        add("Commit summary", summary)
        if not branch:
            attention.append("HEAD is detached; work here is not on a branch.")

    upstream = ""
    if branch and head_code == 0:
        up_code, upstream = git(root, "rev-parse", "--abbrev-ref", "--symbolic-full-name", "@{upstream}")
        if up_code != 0:
            upstream = ""
            add("Upstream", "none")
            attention.append(f"Branch '{branch}' has no upstream; it may never have been pushed.")
        else:
            add("Upstream", upstream)
            _, counts = git(root, "rev-list", "--left-right", "--count", "HEAD...@{upstream}")
            ahead, behind = (int(n) for n in (counts.split() + ["0", "0"])[:2])
            relation = (
                "equal" if not ahead and not behind
                else "divergent" if ahead and behind
                else "ahead" if ahead else "behind"
            )
            add("Versus upstream (as of last fetch)", f"{relation}: {ahead} ahead, {behind} behind")
            if ahead:
                attention.append(f"{ahead} local commit(s) are not pushed.")
            if behind:
                attention.append(f"{behind} upstream commit(s) are not integrated locally.")
            if relation == "divergent":
                attention.append("Histories have diverged; inspect before any pull or push.")

    _, fetch_head = git(root, "rev-parse", "--git-path", "FETCH_HEAD")
    fetch_path = fetch_head if os.path.isabs(fetch_head) else os.path.join(root, fetch_head)
    if fetch_head and os.path.isfile(fetch_path):
        stamp = datetime.datetime.fromtimestamp(os.path.getmtime(fetch_path), datetime.timezone.utc)
        add("Last fetch", stamp.strftime("%Y-%m-%dT%H:%M:%SZ"))
    else:
        add("Last fetch", "no record on this endpoint")

    _, status = git(root, "status", "--porcelain=v1", "--untracked-files=all")
    staged = unstaged = untracked = conflicted = 0
    for line in status.splitlines():
        x, y = line[0], line[1]
        if x == "?" and y == "?":
            untracked += 1
        elif "U" in (x, y) or (x == y and x in "AD"):
            conflicted += 1
        else:
            staged += x != " "
            unstaged += y != " "
    add("Worktree", f"{staged} staged, {unstaged} unstaged, {untracked} untracked, {conflicted} conflicted")
    if staged or unstaged or conflicted:
        attention.append("Uncommitted changes are present.")
    if untracked:
        attention.append(f"{untracked} untracked file(s): confirm each is ignored on purpose or belongs in a commit.")

    _, stashes = git(root, "stash", "list")
    stash_count = len(stashes.splitlines())
    add("Stashes", str(stash_count))
    if stash_count:
        attention.append(f"{stash_count} stash entry(ies) exist only on this endpoint.")

    _, refs = git(root, "for-each-ref", "--format=%(refname:short)|%(upstream:short)|%(upstream:track)", "refs/heads")
    for line in refs.splitlines():
        name, up, track = (line.split("|") + ["", ""])[:3]
        if name == branch:
            continue
        if not up:
            attention.append(f"Other branch '{name}' has no upstream.")
        elif "ahead" in track or "gone" in track:
            attention.append(f"Other branch '{name}' {track} relative to {up}.")

    if ask_remote and upstream and "/" in upstream:
        remote, remote_branch = upstream.split("/", 1)
        code, listing = git(root, "ls-remote", "--heads", remote, f"refs/heads/{remote_branch}")
        tip = listing.split()[0] if code == 0 and listing else ""
        if code != 0:
            add("Remote tip (live)", "could not reach remote")
            attention.append("Remote could not be reached; publication is unverified.")
        elif not tip:
            add("Remote tip (live)", "branch not found on remote")
            attention.append(f"Branch '{remote_branch}' does not exist on {remote}.")
        else:
            match = "matches local HEAD" if tip == head else "differs from local HEAD"
            add("Remote tip (live)", f"{tip} ({match})")
            _, tracked = git(root, "rev-parse", "@{upstream}")
            if tip != tracked:
                attention.append("Remote branch has moved since the last fetch; fetch and inspect before pushing.")
    elif not ask_remote:
        add("Remote tip (live)", "not checked (run with --remote)")

    return facts, attention


def main():
    parser = argparse.ArgumentParser(description="Read-only endpoint status for a handoff record.")
    parser.add_argument("path", nargs="?", default=".", help="path inside the repository (default: current directory)")
    parser.add_argument("--remote", action="store_true", help="also ask the remote for its current branch tip")
    options = parser.parse_args()
    if not os.path.isdir(options.path):
        print(f"Not a directory: {options.path}")
        sys.exit(2)

    facts, attention = collect(options.path, options.remote)
    width = max(len(label) for label, _ in facts)
    for label, value in facts:
        print(f"{label + ':':<{width + 2}}{value}")
    print()
    if attention:
        print("ATTENTION: not handoff-ready")
        for item in attention:
            print(f"  - {item}")
    else:
        scope = "remote tip verified live" if options.remote else "relative to the last fetch; --remote verifies live"
        print(f"READY: clean, on a branch, and level with its upstream ({scope})")
    sys.exit(1 if attention else 0)


if __name__ == "__main__":
    main()
