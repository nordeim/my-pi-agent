---
name: how-to-git-push-using-ssh-wrapper
description: |
  Push commits to a GitHub remote via a Paramiko-based SSH wrapper when OpenSSH (`ssh`) is not installed. Use this skill when `git push` fails with "git@github.com: Permission denied (publickey)" or when the environment lacks `openssh-client` (minimal containers, distroless images, restricted sandboxes, or Python-only environments).

  Prerequisites: Python 3.10+, a GitHub SSH private key file, and the `paramiko` Python package.

  Triggers: "git push", "push to github", "ssh wrapper", "paramiko git", "no openssh", "GIT_SSH_COMMAND", "permission denied publickey", "git push without ssh".
---

# How to Git Push Using an SSH Wrapper

Push commits to GitHub (or any Git-over-SSH remote) when the environment does **not** have OpenSSH's `ssh` client installed. This skill uses a self-contained Python script (`ssh_git_wrapper_v3.py`) backed by Paramiko as Git's SSH transport.

---

## When to Use This Skill

Use this skill when ALL of the following are true:

1. You need to `git push` (or `git fetch`, `git clone`, `git pull`) to a remote that uses SSH URLs (e.g. `git@github.com:user/repo.git`).
2. The environment does **not** have `openssh-client` installed (i.e. `which ssh` fails or returns nothing).
3. Python 3.10+ is available.
4. You have a GitHub SSH private key file (Ed25519, ECDSA, or RSA).

**Do NOT use this skill if** `ssh` is already installed — just use `git push` directly with your normal SSH key setup. This wrapper is a fallback for environments where OpenSSH cannot be installed.

---

## Prerequisites

### 1. Python 3.10+

```bash
python3 --version  # Must be >= 3.10
```

### 2. Paramiko package

Paramiko is the SSH library the wrapper script uses. Install it in the **same Python environment** that will run the wrapper:

```bash
# If python3 is a system Python:
pip install paramiko

# If python3 is a venv (e.g. /home/user/.venv/bin/python3):
/home/user/.venv/bin/python3 -m pip install paramiko

# If pip is blocked by PEP 668 (externally-managed-environment):
pip install --break-system-packages paramiko
```

**⚠️ Critical gotcha:** The `python3` on `PATH` may be a virtualenv that is DIFFERENT from the system Python that `pip` installs into. Always verify with:

```bash
python3 -c "import paramiko; print(paramiko.__version__)"
```

If this fails with `ModuleNotFoundError`, you installed paramiko into the wrong Python. Find the venv pip:

```bash
which python3           # e.g. /home/user/.venv/bin/python3
ls /home/user/.venv/bin/pip*  # e.g. pip3, pip3.12
# Use the venv's pip:
/home/user/.venv/bin/python3 -m pip install paramiko
```

### 3. SSH private key

You need a GitHub SSH private key file in OpenSSH format (starts with `-----BEGIN OPENSSH PRIVATE KEY-----`). Place it at a known path with restrictive permissions:

```bash
mkdir -p ~/.ssh
cp /path/to/uploaded_key.txt ~/.ssh/id_github
chmod 600 ~/.ssh/id_github
```

**Why chmod 600?** SSH libraries (including Paramiko) reject private keys that are readable by group/other. If you skip this, you'll get a cryptic "invalid key" or "permission denied" error.

### 4. The wrapper script

The wrapper script is included in this skill at:
```
skills/how-to-git-push-using-ssh-wrapper/scripts/ssh_git_wrapper_v3.py
```

A canonical copy also lives at:
```
docs/ssh_git_wrapper_v3.py
```

Both copies are identical. Make the script executable:

```bash
chmod +x skills/how-to-git-push-using-ssh-wrapper/scripts/ssh_git_wrapper_v3.py
```

---

## Step-by-Step Procedure

### Step 1: Verify all prerequisites

```bash
python3 --version                                    # >= 3.10
python3 -c "import paramiko; print('OK', paramiko.__version__)"  # Must print OK
ls -la ~/.ssh/id_github                              # Must exist, mode 600
chmod +x /path/to/ssh_git_wrapper_v3.py              # Must be executable
```

### Step 2: Set the remote URL to SSH format

If the remote is currently HTTPS, change it to SSH:

```bash
cd /path/to/repo
git remote -v
# If origin is https://github.com/user/repo.git:
git remote set-url origin git@github.com:user/repo.git
git remote -v  # Verify: origin git@github.com:user/repo.git
```

### Step 3: Verify there are commits to push

```bash
git branch --show-current          # e.g. main
git log --oneline origin/main..HEAD  # Lists commits ahead of remote
```

If `origin/main` doesn't exist yet (first push), use `git log --oneline -5` to see your commits.

### Step 4: Push using the wrapper

```bash
GIT_SSH_COMMAND="/path/to/ssh_git_wrapper_v3.py -i ~/.ssh/id_github -o StrictHostKeyChecking=accept-new" git push origin main
```

**Expected output on success:**
```
To github.com:user/repo.git
   abc1234..def5678  main -> main
```

### Step 5: Verify the push

```bash
git status -sb
# Should show: ## main...origin/main  (no "ahead" or "behind")
```

---

## The `GIT_SSH_COMMAND` variable explained

Git uses `GIT_SSH_COMMAND` to find the SSH program. The wrapper script is called by Git with arguments like:

```
ssh_git_wrapper_v3.py -i ~/.ssh/id_github -o StrictHostKeyChecking=accept-new git@github.com "git-receive-pack 'user/repo.git'"
```

The wrapper:
1. Parses SSH flags (`-i`, `-o`, `-p`, `-l`, `-v`, etc.)
2. Extracts the host (`git@github.com`) and the remote command (`git-receive-pack 'user/repo.git'`)
3. Connects to GitHub via Paramiko using the specified key
4. Executes the remote command
5. Streams stdin/stdout/stderr bidirectionally

### Key flags

| Flag | Purpose |
|---|---|
| `-i ~/.ssh/id_github` | Path to the SSH private key (supports `~` expansion) |
| `-o StrictHostKeyChecking=accept-new` | Auto-accept new host keys, reject changed keys (MITM protection) |
| `-o StrictHostKeyChecking=no` | Accept any host key (less secure, use only for testing) |
| `-v` / `-vv` / `-vvv` | Increase verbosity (WARNING / INFO / DEBUG) |

---

## Troubleshooting

### Problem 1: `ModuleNotFoundError: No module named 'paramiko'`

**Cause:** The `python3` that runs the wrapper (determined by the `#!/usr/bin/env python3` shebang) cannot find paramiko. This happens when `pip install` installs to a different Python than the one on `PATH`.

**Fix:**

```bash
# Find which python3 is on PATH:
which python3
# e.g. /home/user/.venv/bin/python3

# Install paramiko INTO THAT python:
/home/user/.venv/bin/python3 -m pip install paramiko

# Verify:
python3 -c "import paramiko; print('OK')"
```

If `pip install` fails with `externally-managed-environment`:

```bash
pip install --break-system-packages paramiko
# OR use a venv:
python3 -m venv ~/.venv
source ~/.venv/bin/activate
pip install paramiko
```

### Problem 2: `Invalid command: 'git-receive-pack '"'"'user/repo.git'"'"''`

**Cause:** This is the **most common bug** when using the wrapper for the first time. Git passes the remote command as a single string argument (e.g. `"git-receive-pack 'user/repo.git'"`). The wrapper's original code used `shlex.join(args[i+1:])` on a single-element list, which re-quotes the entire string, producing `'git-receive-pack '"'"'user/repo.git'"'"''` — a malformed command that GitHub's git-shell rejects.

**Fix (already applied in the included `ssh_git_wrapper_v3.py`):**

The wrapper must normalize the command via `shlex.split()` → `shlex.join()` when it arrives as a single argument. This strips unnecessary quotes while preserving paths that genuinely contain spaces.

The fix in the script (around line 270):

```python
if i + 1 < len(args):
    raw_cmd = args[i + 1 :]
    if len(raw_cmd) == 1:
        # Single string — split then re-join to normalise quotes
        config["command"] = shlex.join(shlex.split(raw_cmd[0]))
    else:
        config["command"] = shlex.join(raw_cmd)
    break
```

**If you encounter this error with an older version of the wrapper**, apply this fix or use the version included in this skill at `scripts/ssh_git_wrapper_v3.py`.

### Problem 3: `Permission denied (publickey)`

**Cause:** The SSH key is not being found, or GitHub doesn't recognize it.

**Fixes:**

1. **Verify the key file exists and has correct permissions:**
   ```bash
   ls -la ~/.ssh/id_github
   # Must show: -rw------- (mode 600)
   chmod 600 ~/.ssh/id_github
   ```

2. **Verify the key is in OpenSSH format:**
   ```bash
   head -1 ~/.ssh/id_github
   # Must show: -----BEGIN OPENSSH PRIVATE KEY-----
   tail -1 ~/.ssh/id_github
   # Must show: -----END OPENSSH PRIVATE KEY-----
   ```

3. **Verify the public key is added to GitHub:** The corresponding public key must be registered at https://github.com/settings/keys. Check with:
   ```bash
   ssh-keygen -y -f ~/.ssh/id_github  # Extracts public key from private
   # Compare with what's registered on GitHub
   ```

4. **Explicitly pass the key with `-i`:**
   ```bash
   GIT_SSH_COMMAND="/path/to/wrapper.py -i ~/.ssh/id_github" git push origin main
   ```

### Problem 4: `git@github.com: Permission denied` with a key that works elsewhere

**Cause:** The key may require a passphrase, or the SSH agent isn't running.

**Fix:**

```bash
# Start ssh-agent and add the key:
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_github
# Enter passphrase if prompted

# Then push (wrapper auto-detects agent keys):
GIT_SSH_COMMAND="/path/to/wrapper.py" git push origin main
```

**Note:** If `ssh-agent` is not installed (minimal environments), you must use an unencrypted key (no passphrase).

### Problem 5: `Could not read from remote repository`

**Cause:** Wrong remote URL, or network issue.

**Fix:**

```bash
# Verify remote URL is SSH (not HTTPS):
git remote -v
# Must show: origin git@github.com:user/repo.git

# If it shows https://, change it:
git remote set-url origin git@github.com:user/repo.git

# Test connectivity:
python3 -c "
import paramiko, socket
s = socket.create_connection(('github.com', 22), timeout=10)
print('Port 22 reachable')
s.close()
"
```

### Problem 6: `HOST KEY VERIFICATION FAILED`

**Cause:** GitHub's host key has changed (or was previously recorded differently in `~/.ssh/known_hosts`).

**Fix:**

```bash
# Remove the old GitHub host key:
ssh-keygen -R github.com 2>/dev/null || true
# Or manually delete the github.com line from ~/.ssh/known_hosts

# Then push with accept-new to re-accept:
GIT_SSH_COMMAND="/path/to/wrapper.py -i ~/.ssh/id_github -o StrictHostKeyChecking=accept-new" git push origin main
```

### Problem 7: Wrapper crashes with `Fatal Python error: _enter_buffered_busy`

**Cause:** A race condition during interpreter shutdown when the SSH channel closes before the exit status is received. This is a known issue in the wrapper's I/O drain logic.

**Fix:** This is typically transient. Retry the push. If it persists, add a small delay before the channel close or upgrade the wrapper script.

---

## Complete Working Example

Here is the exact sequence that successfully pushed 5 commits to `nordeim/stillwater` in July 2026:

```bash
# 1. Install paramiko into the correct Python
/home/z/.venv/bin/python3 -m pip install paramiko

# 2. Set up the SSH key
mkdir -p ~/.ssh
cp /home/z/my-project/upload/ssh_key.txt ~/.ssh/id_stillwater
chmod 600 ~/.ssh/id_stillwater

# 3. Make the wrapper executable
chmod +x /home/z/my-project/stillwater/docs/ssh_git_wrapper_v3.py

# 4. Change remote from HTTPS to SSH
cd /home/z/my-project/stillwater
git remote set-url origin git@github.com:nordeim/stillwater.git

# 5. Verify there are commits to push
git log --oneline origin/main..HEAD
# (Should list the commits)

# 6. Push
GIT_SSH_COMMAND="/home/z/my-project/stillwater/docs/ssh_git_wrapper_v3.py -i ~/.ssh/id_stillwater -o StrictHostKeyChecking=accept-new" git push origin main

# 7. Verify
git status -sb
# Should show: ## main...origin/main
```

---

## Lessons Learned (From Real-World Usage)

### Lesson 1: Always verify `python3` and `pip` are the same Python

In restricted environments, `python3` on `PATH` is often a virtualenv, while `pip` installs to system Python. The wrapper's `#!/usr/bin/env python3` shebang uses whichever `python3` is on `PATH` — so paramiko MUST be installed into that specific Python.

**Verification command:**
```bash
python3 -c "import paramiko; print('OK', paramiko.__version__)"
```

If this fails, find the venv's pip:
```bash
which python3                          # Find the python3 path
ls $(dirname $(which python3))/pip*    # Find the venv's pip
$(which python3) -m pip install paramiko  # Install into the right Python
```

### Lesson 2: The `shlex.join()` bug is the #1 blocker

The original wrapper script (and the `v3_readme.md` documentation) does NOT account for Git passing the remote command as a single string. The `shlex.join()` call on a single-element list produces a re-quoted string that GitHub's git-shell rejects with "Invalid command".

**Always check for this bug first** when you see:
```
Invalid command: 'git-receive-pack '"'"'user/repo.git'"'"''
```

The fix is to normalize via `shlex.split()` → `shlex.join()` for single-argument commands. This fix is already applied in the version of the script included in this skill (`scripts/ssh_git_wrapper_v3.py`).

### Lesson 3: SSH key permissions are non-negotiable

Paramiko (like OpenSSH) refuses to use private keys that are readable by group or other. Always:
```bash
chmod 600 ~/.ssh/id_github
```

If you copy a key file and forget this step, you'll get "Permission denied (publickey)" with no clear indication that the key permissions are the problem.

### Lesson 4: `StrictHostKeyChecking=accept-new` is the right default

- `yes` — rejects new hosts entirely (first push fails)
- `accept-new` — auto-accepts new hosts, rejects changed keys (MITM-safe) ✅
- `no` — accepts everything (insecure)

For first-time pushes to GitHub, `accept-new` is the correct choice. It writes the host key to `~/.ssh/known_hosts` on first contact and validates it on subsequent connections.

### Lesson 5: Change remote URL from HTTPS to SSH

Many repos are cloned via HTTPS. The wrapper only works with SSH URLs. Always check and convert:
```bash
git remote -v
# If HTTPS: https://github.com/user/repo.git
# Change to SSH:
git remote set-url origin git@github.com:user/repo.git
```

### Lesson 6: The wrapper supports `-o Key=Value` (not space-separated)

Per the wrapper's known limitations, always use `-o StrictHostKeyChecking=accept-new` (with `=`), never `-o StrictHostKeyChecking accept-new` (with space). The space form breaks argument parsing.

### Lesson 7: Commit the wrapper script fix

If you had to apply the `shlex.join()` fix to the wrapper, commit and push it so future agents don't hit the same bug. In the Stillwater project, this was commit `39298e4`:
```
fix(ssh-wrapper): normalise Git remote command quoting for GitHub
```

---

## Quick Reference Card

```bash
# One-liner push (after prerequisites are met):
GIT_SSH_COMMAND="/path/to/ssh_git_wrapper_v3.py -i ~/.ssh/id_github -o StrictHostKeyChecking=accept-new" git push origin main

# Debug mode (verbose):
GIT_SSH_COMMAND="/path/to/ssh_git_wrapper_v3.py -i ~/.ssh/id_github -o StrictHostKeyChecking=accept-new -vvv" git push origin main

# Fetch:
GIT_SSH_COMMAND="/path/to/ssh_git_wrapper_v3.py -i ~/.ssh/id_github -o StrictHostKeyChecking=accept-new" git fetch origin

# Clone:
GIT_SSH_COMMAND="/path/to/ssh_git_wrapper_v3.py -i ~/.ssh/id_github -o StrictHostKeyChecking=accept-new" git clone git@github.com:user/repo.git
```

---

## Files in This Skill

| File | Purpose |
|---|---|
| `SKILL.md` | This document — instructions for performing `git push` via the SSH wrapper |
| `scripts/ssh_git_wrapper_v3.py` | The wrapper script (executable, with the `shlex.join()` fix applied) |

## Canonical Source

The canonical copy of the wrapper script lives at `docs/ssh_git_wrapper_v3.py` in the Stillwater repo. The copy in `scripts/` is for skill self-containment. If they diverge, the `docs/` version is authoritative (it's the one actually tested in production).

## See Also

- `docs/ssh_git_wrapper_v3_readme.md` — Original wrapper documentation (does NOT include the `shlex.join()` fix — see Lesson 2 above)
