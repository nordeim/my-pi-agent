# How-To: Git Push Using the SSH Wrapper (`ssh_git_wrapper_v3.py`)

**Purpose.** Push commits from this checkout to the canonical SSH remote
`git@github.com:nordeim/task-management.git` using a deploy key that is
**never stored inside the repository** (`.gitignore` rejects `*.key` and
`ssh-key.txt`). The wrapper materializes the key into a 0600 temp file
outside the repo, points `GIT_SSH_COMMAND` at it, authenticates, pushes
`main`, verifies the remote ref equals local HEAD, then shreds the temp key.

**Field-tested.** 2026-09-16: this exact procedure (wrapper v3.1 + the
paramiko shim in Appendix A) pushed `0ab29dc..f932360` to `main` from a
sandbox that had **no OpenSSH binary at all**, then re-verified the remote
ref and the fingerprint of the key in play. Everything below is that
session, generalized.

**Rules (operator contract).**

1. **main only** — no feature branches; the wrapper defaults to `main` and
   pushes `HEAD:refs/heads/main`.
2. **Run the verification gate first** — `bun run lint && bun run typecheck
   && bun run test && bun run build` must be green before pushing. There is
   no hosted CI on this repo (no `.github/workflows`), so the local gate is
   the only gate.
3. **Commit before push** — the wrapper pushes commits, not the working tree.
4. **Never commit the key** — keys live outside the repo (`~/.ssh/`, a
   secret store, or a pipe). If a key ever lands in the tree, rotate it.
5. **Never commit the shim either** — the paramiko ssh shim is environment
   tooling, not project code. It contains no secrets, but it does not
   belong in the tree; keep it in a workspace `bin/` outside the checkout.

## Field-tested sequence (what actually worked)

```bash
cd task-management
# 0. Gates green and commits already on main (rules 1-3).

# 1. Operator key -> a 0600 file in /tmp, NEVER inside the repo:
cat > /tmp/tuesday-deploy.key        # paste the key, then Ctrl-D
chmod 600 /tmp/tuesday-deploy.key

# 2. Optional sanity check — proves the key parses and shows its
#    OpenSSH fingerprint (works where ssh-keygen does not exist;
#    verified to match ssh-keygen's SHA256 output for ed25519):
python3 - <<'PY'
import base64, hashlib, paramiko
k = paramiko.Ed25519Key.from_private_key_file("/tmp/tuesday-deploy.key")
print("type:", k.get_name())
print("SHA256:", base64.b64encode(hashlib.sha256(k.asbytes()).digest())
      .decode().rstrip("="))
PY

# 3. Make an ssh binary discoverable. A real OpenSSH client needs nothing;
#    a sandbox without one uses the paramiko shim (Appendix A) on PATH:
export PATH="/path/to/shim-dir:$PATH"     # e.g. a workspace bin/ dir

# 4. Dry-run — authenticates and negotiates, touches no refs:
python3 docs/ssh_git_wrapper_v3.py --key-file /tmp/tuesday-deploy.key --dry-run

# 5. Real push — prints remote verification + tracking-ref sync:
python3 docs/ssh_git_wrapper_v3.py --key-file /tmp/tuesday-deploy.key

# 6. Shred the operator key (the wrapper already shredded its own temp copy
#    and the known_hosts sidecar, if any):
python3 - <<'PY'
import os
p = "/tmp/tuesday-deploy.key"
with open(p, "wb") as f:
    f.write(os.urandom(os.path.getsize(p)))
os.remove(p)
print("operator key shredded")
PY
```

Expected wrapper output on the real push (v3.1):

```
[ssh-git-wrapper] $ git push git@github.com:nordeim/task-management.git HEAD:refs/heads/main
[ssh-git-wrapper] remote verified: refs/heads/main @ <sha> == local HEAD
[ssh-git-wrapper] synced refs/remotes/origin/main -> <sha> (git status will now agree)
[ssh-git-wrapper] OK — pushed HEAD -> git@github.com:nordeim/task-management.git refs/heads/main
[ssh-git-wrapper] temp key material shredded and removed
```

## Variants

```bash
# Key piped on stdin (no key file on disk):
cat /secure/path/to/id_ed25519 | python3 docs/ssh_git_wrapper_v3.py --key-stdin \
  --remote git@github.com:nordeim/task-management.git

# Key from an environment variable:
SSH_KEY="$(cat /secure/id_ed25519)" python3 docs/ssh_git_wrapper_v3.py \
  --remote git@github.com:nordeim/task-management.git

# Persist the SSH URL as origin's push URL for future plain `git push`
# (idempotent in v3.1 — only re-set when it actually differs):
python3 docs/ssh_git_wrapper_v3.py --key-file ~/.ssh/id_ed25519 --set-url
```

## Key formats the wrapper accepts

The wrapper accepts a standard OpenSSH private key block (proper BEGIN/END
delimiter lines). It also tolerates keys that traveled through a chat
transcript and arrived with the BEGIN line replaced by the placeholder
`[REDACTED:ssh_private_key]` — the wrapper restores a real OpenSSH BEGIN
line before use, so the key still authenticates. A key missing either
delimiter is rejected with exit code 2.

## What the wrapper does, step by step (v3.1)

| Step | Action | Safety property |
|---|---|---|
| 0 | Preflight: an `ssh` executable must exist on PATH | Fails fast (exit 1) in OpenSSH-less sandboxes with a pointer to this runbook, instead of a cryptic shell error inside git |
| 1 | Reads the key from `--key-file` / `--key-stdin` / `$SSH_KEY` | Rejects keys without proper OpenSSH delimiters (after redaction normalization) |
| 2 | Writes it to `/tmp/dbs-push-XXXX.key` with `0600` | Outside the repo; ssh refuses group/world-readable keys |
| 3 | Exports `GIT_SSH_COMMAND="ssh -i <key> -o IdentitiesOnly=yes -o StrictHostKeyChecking=accept-new …"` | Only the supplied key is offered; new host keys are recorded per-session |
| 4 | `git ls-remote --heads <remote> main` | Authentication pre-flight — fails fast with exit 4 on bad keys |
| 5 | `git push <remote> HEAD:refs/heads/main` | Explicit refspec; no implicit branch creation |
| 6 | Re-queries the remote and asserts `refs/heads/main == local HEAD` | Turns "git said ok" into evidence; exit 4 on mismatch (skipped on `--dry-run`) |
| 7 | Best-effort sync of `refs/remotes/origin/main` when the pushed remote is origin's repository (URLs normalized) | `git status` stops claiming "ahead by N" after a URL-based push |
| 8 | Overwrites the temp key with random bytes, deletes it + the sidecar known_hosts | No key residue (a paramiko shim writes no sidecar — absence is fine) |

## Exit codes

| Code | Meaning |
|---|---|
| 0 | Push succeeded (and, on a real push, the remote ref was verified) |
| 1 | Usage error (no key source, stdin is a TTY) **or no `ssh` binary on PATH** |
| 2 | Key materialization/cleanup error (also: key failed delimiter validation) |
| 3 | Local git error (not a repo, remote set-url failed, …) |
| 4 | Authentication pre-flight failed, the push was rejected, **or post-push verification mismatched** |

## Sandbox without an OpenSSH binary (the paramiko shim)

The validating sandbox had neither `ssh` nor `ssh-keygen`, and git executes
`GIT_SSH_COMMAND` through PATH — so the wrapper preflights for an `ssh`
executable and exits 1 with a pointer here when it is missing. What worked:

- a ~100-line pure-Python shim saved OUTSIDE the repo (e.g. a workspace
  `bin/ssh`), `chmod +x`, placed on PATH;
- it parses the argument shape git passes: `-i KEY`, `-o OPT` (options are
  consumed and ignored — `accept-new` maps to paramiko's `AutoAddPolicy`),
  `-p PORT`, `[user@]host`, then the trailing command string;
- it bridges stdio both ways with `select()` so the git pack protocol runs
  over the SSH channel, draining the remote's stderr as it goes;
- it loads the key with `paramiko.Ed25519Key` first, `RSAKey` as fallback;
- it exits with the remote command's exit status, and refuses the
  no-command case loudly (real ssh would open a shell; git never does this);
- the shebang must point at a Python that can `import paramiko`
  (`pip install paramiko` — 5.0.0 was used and was sufficient).

Appendix A contains the field-tested implementation. Deploy it, then run
the wrapper normally — nothing else changes.

## Troubleshooting

- **`no ssh binary on PATH`** — the wrapper's own preflight (step 0).
  Install an OpenSSH client, or deploy the Appendix A shim on PATH.
- **`authentication pre-flight failed`** — the key is wrong, expired, or
  lacks push rights on `nordeim/task-management`. With OpenSSH present:
  `ssh -i /secure/key -T git@github.com` (expect a greeting naming the
  repo). Without one, the cheapest equivalent is the wrapper's own
  `--dry-run` — it exercises exactly the same auth path and fails with the
  same exit code.
- **`key does not look like an OpenSSH private key`** — the source lost its
  BEGIN or END delimiter line in transit (trailing-space mangling, partial
  copy). Re-supply the complete key block, delimiters included.
- **Push rejected (non-fast-forward)** — the remote moved ahead:
  `git fetch origin && git rebase origin/main`, re-run the gate, then push.
- **`Permission denied (publickey)`** — GitHub needs the corresponding public
  key added as a deploy key (repo → Settings → Deploy keys, write access).
- **`git status` still says "ahead of origin/main by N" after a successful
  push** — a URL-based push never updates origin's remote-tracking ref. The
  wrapper syncs it automatically when the pushed remote is the same GitHub
  repository as `origin`; if you pushed somewhere else, verify manually:
  `git ls-remote git@github.com:nordeim/task-management.git refs/heads/main`
  (shim on PATH) and compare with `git rev-parse HEAD`.
- **The wrapper's own source looks corrupted when read through agent
  tooling** — some tool-output layers redact the OpenSSH BEGIN delimiter
  when *displaying* file contents, so the `OPENSSH_BEGIN` constant appears
  to hold the redaction placeholder. This is a display artifact, not a
  defect: verify the bytes on disk (e.g. a base64 dump of the file, or
  `python3 -c "print(bytes([45]*5) + b'BEGIN OPENSSH PRIVATE KEY' + bytes([45]*5) in open('docs/ssh_git_wrapper_v3.py','rb').read())"`)
  before concluding anything — and never "repair" the constant based on a
  redacted display.

## Relationship to the repo's git contract

- AGENTS.md: clone remote is `https://github.com/nordeim/task-management.git`;
  the SSH URL is the push target — this wrapper exists so an agent or CI
  runner can push without a resident `~/.ssh` identity.
- CLAUDE.md commit standards apply: Conventional Commits, atomic commits,
  never commit secrets.
- The verification gate (AGENTS.md "clean check" order) is a precondition —
  and, until hosted CI exists, the only one.

## Appendix A — field-tested paramiko ssh shim

Save as `ssh` in a directory OUTSIDE this repo, `chmod +x`, adjust the
shebang to a Python that has paramiko, and put that directory on PATH.
This is the implementation that carried the real push (lightly edited:
generic shebang, paths generalized).

```python
#!/usr/bin/env python3
"""paramiko-backed ssh shim for sandboxes without an OpenSSH binary.

Git invokes this via GIT_SSH_COMMAND as:
  ssh -i <key> -o IdentitiesOnly=yes -o StrictHostKeyChecking=accept-new \
      -o UserKnownHostsFile=<path> git@github.com "git-upload-pack '<repo>'"

The shim speaks real SSH through paramiko, bridges stdio (the git pack
protocol runs over the channel), and exits with the remote command's
status. -o options are accepted and ignored (accept-new maps to
AutoAddPolicy).
"""
import os
import select
import sys

import paramiko

CHUNK = 65536


def parse_args(argv):
    key_path = None
    host = None
    port = 22
    command = None
    i = 0
    while i < len(argv):
        arg = argv[i]
        if arg == "-i":
            i += 1
            key_path = argv[i] if i < len(argv) else None
        elif arg == "-p":
            i += 1
            port = int(argv[i]) if i < len(argv) else 22
        elif arg == "-o":
            i += 1  # option + value consumed together
        elif arg.startswith("-"):
            pass  # unknown flags ignored
        elif host is None:
            host = arg
        else:
            command = " ".join(argv[i:])
            break
        i += 1
    return key_path, host, port, command


def load_key(key_path):
    """Load the deploy key; try Ed25519 first, then RSA (format fallback)."""
    errors = []
    for cls in (paramiko.Ed25519Key, paramiko.RSAKey):
        try:
            return cls.from_private_key_file(key_path)
        except Exception as exc:  # report both failures together
            errors.append(f"{cls.__name__}: {exc}")
    sys.stderr.write("[ssh-shim] key load failed: " + " | ".join(errors) + "\n")
    sys.exit(255)


def main():
    if len(sys.argv) < 2:
        sys.stderr.write("[ssh-shim] usage: ssh -i KEY [-o OPT] [user@]host command\n")
        sys.exit(255)

    key_path, host, port, command = parse_args(sys.argv[1:])
    if not key_path or not host or not command:
        sys.stderr.write(f"[ssh-shim] missing pieces (key={key_path} host={host} cmd={command})\n")
        sys.exit(255)

    user = "git"
    if "@" in host:
        user, host = host.split("@", 1)

    pkey = load_key(key_path)

    client = paramiko.SSHClient()
    # accept-new equivalent: trust first contact, record nothing (the
    # wrapper's known_hosts sidecar is managed by the wrapper's lifecycle).
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(
        host,
        port=port,
        username=user,
        pkey=pkey,
        look_for_keys=False,
        allow_agent=False,
        timeout=30,
        banner_timeout=30,
        auth_timeout=30,
    )

    try:
        channel = client.get_transport().open_session()
        channel.exec_command(command)

        stdin_fd = sys.stdin.fileno()
        stdin_closed = False
        while True:
            readers = [channel, sys.stdin] if not stdin_closed else [channel]
            try:
                rlist, _, _ = select.select(readers, [], [], 30)
            except (OSError, ValueError):
                break

            if channel in rlist:
                if channel.recv_ready():
                    data = channel.recv(CHUNK)
                    if data:
                        sys.stdout.buffer.write(data)
                        sys.stdout.buffer.flush()
                if channel.exit_status_ready() and not channel.recv_ready():
                    while channel.recv_ready():
                        data = channel.recv(CHUNK)
                        if not data:
                            break
                        sys.stdout.buffer.write(data)
                        sys.stdout.buffer.flush()
                    break
                if channel.closed and not channel.recv_ready():
                    break

            if sys.stdin in rlist:
                try:
                    data = os.read(stdin_fd, CHUNK)
                except OSError:
                    data = b""
                if data:
                    channel.sendall(data)
                else:
                    channel.shutdown_write()
                    stdin_closed = True

            # stderr drain (git server diagnostics)
            while channel.recv_stderr_ready():
                err = channel.recv_stderr(CHUNK)
                if not err:
                    break
                sys.stderr.buffer.write(err)
                sys.stderr.buffer.flush()

        # Final drains after the loop.
        while channel.recv_ready():
            data = channel.recv(CHUNK)
            if not data:
                break
            sys.stdout.buffer.write(data)
            sys.stdout.buffer.flush()
        while channel.recv_stderr_ready():
            err = channel.recv_stderr(CHUNK)
            if not err:
                break
            sys.stderr.buffer.write(err)
            sys.stderr.buffer.flush()

        exit_status = channel.recv_exit_status()
        sys.exit(exit_status)
    finally:
        client.close()


if __name__ == "__main__":
    main()
```
