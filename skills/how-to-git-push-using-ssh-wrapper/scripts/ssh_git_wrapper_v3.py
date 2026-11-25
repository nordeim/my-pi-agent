#!/usr/bin/env python3
"""
ssh_git_wrapper_v3.py — push to GitHub over SSH with an externally-supplied key.

Revision: v3.1 (2026-09-16) — field-tested hardening after a real push cycle
in a sandbox that had no OpenSSH binary on PATH. New in v3.1: an ssh-binary
preflight, post-push remote verification, best-effort origin tracking-ref
sync, and captured plumbing output (fixes --set-url idempotence). CLI and
exit-code semantics of v3 are otherwise unchanged.

Why this exists
---------------
The repo's canonical remote for pushes is the SSH URL
(`git@github.com:nordeim/task-management.git`), but cloning happens over
HTTPS and sandbox/CI environments rarely have a resident `~/.ssh` identity.
This wrapper lets an operator push without permanently installing a key:

  1. Take an OpenSSH private key from a file, stdin, or the `SSH_KEY` env var
     (NEVER from a file committed inside the repo — the .gitignore already
     rejects `*.key` / `ssh-key.txt` for exactly this reason). Keys pasted
     through chat transcripts sometimes arrive with the first line redacted
     to `[REDACTED:ssh_private_key]`; the wrapper normalizes that back to a
     real OpenSSH BEGIN line before use.
  2. Materialize it into a 0600 temp file OUTSIDE the repo.
  3. Point `GIT_SSH_COMMAND` at it (IdentitiesOnly, accept-new host keys).
  4. Push `main` (or the requested ref) to the SSH remote.
  5. Verify the remote ref now equals the pushed commit.
  6. Shred and remove the temp key.

Usage
-----
  # key from a file (recommended — file lives outside the repo):
  python3 docs/ssh_git_wrapper_v3.py --key-file /secure/path/to/id_ed25519

  # key piped on stdin:
  cat /secure/id_ed25519 | python3 docs/ssh_git_wrapper_v3.py --key-stdin

  # key from an environment variable:
  SSH_KEY="$(cat /secure/id_ed25519)" python3 docs/ssh_git_wrapper_v3.py

Options
-------
  --remote <url>    SSH remote to push to
                    (default git@github.com:nordeim/task-management.git)
  --branch <name>   Branch to push (default: main — the operator contract for
                    this repo is main-only, no feature branches)
  --set-url         Also persist the SSH URL as origin's push URL in .git/config
  --dry-run         Run `git push --dry-run` (key handling still exercised;
                    post-push verification is skipped — the remote must not move)
  -h / --help       This message

Exit codes: 0 success · 1 usage error or missing ssh binary · 2 key
materialization error · 3 git error · 4 push rejected/failed or post-push
verification mismatch.

Field-tested notes (2026-09-16, the session that shipped 0ab29dc..f932360)
---------------------------------------------------------------------------
- The validating sandbox had NO OpenSSH client: no `ssh`, no `ssh-keygen`.
  git executes GIT_SSH_COMMAND through PATH, so this version preflights
  `shutil.which("ssh")` and exits 1 with a pointer to the runbook's shim
  recipe instead of failing inside git with a cryptic shell error. What
  worked there: a paramiko-backed `ssh` shim (pure Python, outside the
  repo) placed on PATH; it only needs to parse `-i KEY`, `-o OPT`, `-p
  PORT`, `[user@]host` plus a trailing command, bridge stdio for the git
  pack protocol, and propagate the remote exit status. Full recipe:
  docs/how-to-git-push-using-ssh-wrapper_SKILL.md.
- The working operator sequence was: gates green → commits on main → key
  into a 0600 file in /tmp (never inside the repo) → optional paramiko
  parse/fingerprint check → `--dry-run` → real push → the remote
  verification this script prints → shred the operator key. Every step
  exited 0 and the remote ended at the local HEAD.
- A URL-based push (`git push <url> HEAD:refs/heads/main`) does NOT update
  origin's remote-tracking ref, so `git status` can keep saying "ahead of
  origin/main by N" after a perfectly successful push. When the pushed
  remote is the same GitHub repository as `origin` (URLs normalized), this
  wrapper now best-effort syncs `refs/remotes/origin/<branch>` so local
  status tells the truth; otherwise it just leaves verification output.
- Agent-operator caveat: some tool-output layers redact the OpenSSH BEGIN
  delimiter when DISPLAYING file contents, which makes this script's
  OPENSSH_BEGIN constant look corrupted in a transcript. The on-disk bytes
  are the source of truth — verify with a byte-level/base64 read before
  "repairing" the literal, and never trust a redacted display when editing.
- With the paramiko shim, no known_hosts sidecar file is created; cleanup
  tolerates its absence.
- `--set-url` in v3 compared against uncaptured subprocess output and so
  re-set the URL on every run (harmless but wrong); plumbing output is now
  captured wherever it is parsed, making the check idempotent.

See docs/how-to-git-push-using-ssh-wrapper_SKILL.md for the operator runbook.
"""

from __future__ import annotations

import argparse
import os
import shutil
import stat
import subprocess
import sys
import tempfile

DEFAULT_REMOTE = "git@github.com:nordeim/task-management.git"
DEFAULT_BRANCH = "main"
OPENSSH_BEGIN = "-----BEGIN OPENSSH PRIVATE KEY-----"
OPENSSH_END = "-----END OPENSSH PRIVATE KEY-----"
# Keys pasted through chat/issue transcripts sometimes arrive with the BEGIN
# line replaced by this redaction placeholder; it is normalized back below.
REDACTED_MARKER = "[REDACTED:ssh_private_key]"
RUNBOOK = "docs/how-to-git-push-using-ssh-wrapper_SKILL.md"


def die(code: int, message: str) -> None:
    print(f"[ssh-git-wrapper] ERROR: {message}", file=sys.stderr)
    sys.exit(code)


def read_key(args: argparse.Namespace) -> str:
    """Collect the private key from whichever source was requested."""
    key = ""
    if args.key_file:
        try:
            with open(os.path.abspath(args.key_file), "r", encoding="utf-8") as handle:
                key = handle.read()
        except OSError as exc:
            die(2, f"cannot read --key-file {args.key_file}: {exc}")
    elif args.key_stdin:
        if sys.stdin.isatty():
            die(1, "--key-stdin given but stdin is a terminal — pipe the key in")
        key = sys.stdin.read()
    elif os.environ.get("SSH_KEY"):
        key = os.environ["SSH_KEY"]
    else:
        die(1, "no key source: pass --key-file PATH, --key-stdin, or set $SSH_KEY")

    key = key.strip() + "\n"
    # Normalize: restore a redacted BEGIN line, then require proper delimiters.
    key = key.replace(REDACTED_MARKER, OPENSSH_BEGIN)
    if OPENSSH_BEGIN not in key or OPENSSH_END not in key:
        die(
            2,
            "key does not look like an OpenSSH private key "
            f"(missing {OPENSSH_BEGIN} / {OPENSSH_END} markers)",
        )
    return key


def materialize_key(key: str) -> str:
    """Write the key to a 0600 temp file outside the repository."""
    file_descriptor, path = tempfile.mkstemp(prefix="dbs-push-", suffix=".key", dir="/tmp")
    try:
        with os.fdopen(file_descriptor, "w", encoding="utf-8") as handle:
            handle.write(key)
        os.chmod(path, stat.S_IRUSR | stat.S_IWUSR)  # 0600 — ssh refuses wider
    except OSError as exc:
        die(2, f"cannot materialize temp key file: {exc}")
    return path


def normalize_repo_id(url: str) -> str:
    """Reduce git@host:owner/repo.git, ssh://host/owner/repo.git and
    https://host/owner/repo.git to the comparable id `owner/repo`."""
    cleaned = url.strip().lower()
    if "://" in cleaned:
        cleaned = cleaned.split("://", 1)[1]
        cleaned = cleaned.split("/", 1)[1] if "/" in cleaned else cleaned
    elif ":" in cleaned:  # scp-like syntax: git@github.com:owner/repo.git
        cleaned = cleaned.split(":", 1)[1]
    if cleaned.endswith(".git"):
        cleaned = cleaned[: -len(".git")]
    return cleaned.strip("/")


def run(
    command: list[str],
    env: dict[str, str],
    capture: bool = False,
) -> subprocess.CompletedProcess[str]:
    printable = " ".join(command)
    print(f"[ssh-git-wrapper] $ {printable}")
    return subprocess.run(command, env=env, text=True, capture_output=capture)


def preflight_ssh() -> None:
    """git runs GIT_SSH_COMMAND through PATH; without an ssh binary every
    push dies inside git with a shell error. Field-tested failure mode —
    fail fast here with an actionable message instead."""
    if shutil.which("ssh") is None:
        die(
            1,
            "no ssh binary on PATH — git cannot execute GIT_SSH_COMMAND. "
            "Install an OpenSSH client, or place a paramiko-backed ssh shim "
            f"on PATH (recipe: {RUNBOOK}, section 'Sandbox without an "
            "OpenSSH binary')",
        )


def remote_branch_sha(remote: str, branch: str, env: dict[str, str]) -> str | None:
    """Current sha of refs/heads/<branch> on the remote; None if the query
    failed or the ref is absent."""
    query = run(["git", "ls-remote", "--heads", remote, branch], env, capture=True)
    if query.returncode != 0:
        if query.stderr:
            print(query.stderr, file=sys.stderr, end="")
        return None
    lines = (query.stdout or "").strip().splitlines()
    return lines[0].split()[0] if lines and lines[0].split() else None


def verify_remote(remote: str, branch: str, env: dict[str, str]) -> str:
    """Post-push evidence: the remote ref must now equal local HEAD."""
    local = run(["git", "rev-parse", "HEAD"], {**os.environ}, capture=True)
    if local.returncode != 0:
        die(3, "git rev-parse HEAD failed")
    local_sha = (local.stdout or "").strip()
    remote_sha = remote_branch_sha(remote, branch, env)
    if not remote_sha:
        die(4, f"post-push verification failed — could not query refs/heads/{branch} on {remote}")
    if remote_sha != local_sha:
        die(
            4,
            f"post-push verification failed — remote {remote_sha[:7]} "
            f"!= local HEAD {local_sha[:7]}",
        )
    print(
        f"[ssh-git-wrapper] remote verified: refs/heads/{branch} @ "
        f"{remote_sha[:7]} == local HEAD"
    )
    return local_sha


def sync_origin_tracking_ref(remote: str, branch: str, sha: str) -> None:
    """A URL-based push never updates refs/remotes/origin/*, so `git status`
    keeps claiming 'ahead of N' after a successful push. If origin points at
    the same repository as the pushed remote, sync the tracking ref (exactly
    what `git push origin` would have done). Best-effort: never fatal."""
    configured = run(["git", "remote", "get-url", "origin"], {**os.environ}, capture=True)
    if configured.returncode != 0:
        return
    origin_url = (configured.stdout or "").strip()
    if not origin_url or normalize_repo_id(origin_url) != normalize_repo_id(remote):
        return
    ref = f"refs/remotes/origin/{branch}"
    update = run(["git", "update-ref", ref, sha], {**os.environ})
    if update.returncode == 0:
        print(f"[ssh-git-wrapper] synced {ref} -> {sha[:7]} (git status will now agree)")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Push to the GitHub SSH remote using an externally-supplied deploy key.",
        epilog="revision v3.1 (2026-09-16) — runbook: " + RUNBOOK,
    )
    parser.add_argument("--key-file", help="path to an OpenSSH private key (outside the repo)")
    parser.add_argument("--key-stdin", action="store_true", help="read the key from stdin")
    parser.add_argument("--remote", default=DEFAULT_REMOTE, help=f"SSH remote (default {DEFAULT_REMOTE})")
    parser.add_argument("--branch", default=DEFAULT_BRANCH, help=f"branch to push (default {DEFAULT_BRANCH})")
    parser.add_argument("--set-url", action="store_true", help="persist the SSH URL as origin push URL")
    parser.add_argument("--dry-run", action="store_true", help="git push --dry-run")
    args = parser.parse_args()

    repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if not os.path.isdir(os.path.join(repo_root, ".git")):
        die(3, f"{repo_root} does not look like a git repository (run from the repo checkout)")

    preflight_ssh()

    key = read_key(args)
    key_path = materialize_key(key)
    ssh_command = (
        f"ssh -i {key_path} -o IdentitiesOnly=yes "
        f"-o StrictHostKeyChecking=accept-new -o UserKnownHostsFile={key_path}.known_hosts"
    )
    env = {**os.environ, "GIT_SSH_COMMAND": ssh_command}

    try:
        if args.set_url:
            configured = run(
                ["git", "remote", "get-url", "--push", "origin"],
                {**os.environ},
                capture=True,
            )
            if args.remote not in (configured.stdout or ""):
                result = run(
                    ["git", "remote", "set-url", "--push", "origin", args.remote],
                    {**os.environ},
                )
                if result.returncode != 0:
                    die(3, "git remote set-url failed")

        push_args = ["git", "push", args.remote, f"HEAD:refs/heads/{args.branch}"]
        if args.dry_run:
            push_args.insert(2, "--dry-run")

        # Pre-flight: prove the key authenticates before attempting the push.
        ls_remote = run(
            ["git", "ls-remote", "--heads", args.remote, args.branch],
            env,
        )
        if ls_remote.returncode != 0:
            die(4, "authentication pre-flight failed (git ls-remote) — check the key and remote")

        push = run(push_args, env)
        if push.returncode != 0:
            die(4, f"git push failed (exit {push.returncode})")

        if args.dry_run:
            print(
                f"[ssh-git-wrapper] OK — dry-run push to {args.remote} "
                f"refs/heads/{args.branch} (remote untouched; post-push "
                "verification skipped)"
            )
        else:
            pushed_sha = verify_remote(args.remote, args.branch, env)
            sync_origin_tracking_ref(args.remote, args.branch, pushed_sha)
            print(
                f"[ssh-git-wrapper] OK — pushed HEAD -> {args.remote} refs/heads/{args.branch}"
            )
    finally:
        # Shred-then-remove: best-effort overwrite before unlink, and clean
        # the sidecar known_hosts the SSH command created (a paramiko shim
        # creates none — absence is fine).
        try:
            size = os.path.getsize(key_path)
            with open(key_path, "wb") as handle:
                handle.write(os.urandom(size))
            os.remove(key_path)
            known_hosts = f"{key_path}.known_hosts"
            if os.path.exists(known_hosts):
                os.remove(known_hosts)
            print("[ssh-git-wrapper] temp key material shredded and removed")
        except OSError:
            die(2, f"failed to clean up {key_path} — remove it manually")


if __name__ == "__main__":
    main()
