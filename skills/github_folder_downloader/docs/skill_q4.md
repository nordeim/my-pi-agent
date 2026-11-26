# Plan + Deliverable — `SKILL.md` for q4 (`github_folder_downloader.py` v3.1.0)

**Mode:** generation (documentation/packaging). **Workflow:** analyze → plan → validate → implement → verify → deliver.
**Evidence posture:** no runner in this session. Everything below is **Reasoned** (static cross-check against the q4 source you supplied) or **Unverifiable** until the gates in §5 are observed. q4's own "Verified" labels remain *author claims*. The script is packaged **verbatim** — no fixes bundled (audit findings stay separate commits, per your no-unrequested-rewrites rule).

---

## 1. Meticulous plan

| Phase | Tasks | Exit criterion |
|---|---|---|
| **Analyze** | Extract q4's exact contract: URL forms, `--ref`/`--path` semantics (D-9: tail = path, no prefix-strip), exit codes (0/1/2/3/130 + `--json error_class`), all 27 CLI flags + defaults, tiers, safety model, JSON summary fields, limitations. Cross-check every SKILL.md statement against source. | Zero doc/code drift; no overclaiming (e.g., LFS payloads **not** fetched; cert-retry guard contested in prior audit → not advertised). |
| **Plan** | Resolve spec decisions (§2); choose progressive-disclosure layout: one concise SKILL.md (<500 lines) + `scripts/` asset; `--help`/`--self-test` are the authoritative runtime references. | Decisions disclosed; structure matches your request. |
| **Validate** | Spec-compliance checklist (§3); packaging integrity: extract code block from `q4.md`, normalize the one-space indent artifact visible in the attachment, `py_compile`, `--self-test`, frontmatter lint, skill-discovery check. | All gates observed green before delivery is claimed. |
| **Implement** | Write `SKILL.md` (§4); place script verbatim at `scripts/github_folder_downloader.py` (§5 extractor). | Files exist; script unmodified except disclosed whitespace normalization. |
| **Verify** | §5 gates + live smoke (`--dry-run --json` on a real folder). | Each claim promoted Reasoned→Verified only on observed exit 0. |
| **Deliver** | Atomic Conventional Commit `feat(skills): add github_folder_downloader skill (q4 v3.1.0)`; push via your SSH wrapper when the environment supports it; handoff with ledger + deferred debt. | One commit; no guardrails weakened. |

### 2. Decisions requiring your sign-off (not silently resolved)

| # | Decision | Recommendation | Tradeoff |
|---|---|---|---|
| D1 | **Naming conflict:** your folder uses underscores (`github_folder_downloader`); the Agent Skills spec requires `name` to be lowercase letters/digits/hyphens only, and loaders commonly expect `name` == directory name. | Set `name: github-folder-downloader`. **Preferred:** rename dir to `skills/github-folder-downloader/` (`mv`). **If you keep the underscore dir:** the hyphenated `name` is still spec-valid, but discovery must be verified (§5 gate 6); if your loader enforces equality, rename. | Honoring your exact path vs. guaranteed loader compatibility. I keep your path in the tree below and flag the risk rather than silently renaming. |
| D2 | Optional `allowed-tools` (Claude Code-specific least-privilege hint). | Include `allowed-tools: Bash, Read`. Other surfaces ignore it; remove if your validator rejects unknown fields. | Security-positive vs. maximal cross-surface minimalism. |
| D3 | `license` frontmatter. | **Omit** — q4 ships no license text; do not fabricate one. | Add later when you choose a license. |
| D4 | Extra frontmatter (`metadata`, `version`). | Omit; version lives in the body and `--version` (3.1.0). | Avoids strict-validator rejection. |
| D5 | Whitespace artifact in `q4.md` (uniform single-space indent after the shebang). | Strip exactly one leading space **only if uniformly present**, then prove semantics unchanged via `py_compile` + `--self-test`. If gates fail: stop and triage; never edit code to pass. | Packaging hygiene, disclosed — not a code change. |

### 3. Spec-compliance checklist (Agent Skills / SKILL.md)

| Requirement | Status in deliverable |
|---|---|
| YAML frontmatter with required `name` (≤64 chars, `[a-z0-9-]`, no leading/trailing/consecutive hyphens) | `github-folder-downloader` (24 chars) ✓ |
| Required `description` ≤1024 chars, third person, states **what** + **when** (trigger terms) | ~700 chars, includes "download/mirror/sync GitHub folder/subdirectory… without cloning… tree/REF/PATH" ✓ |
| Body: concise Markdown, <500 lines recommended; progressive disclosure to bundled assets | ~300 lines; heavy detail delegated to `--help` / `--self-test` ✓ |
| Bundled resources referenced by **relative** paths; executable asset in `scripts/` | `scripts/github_folder_downloader.py` ✓ |
| Optional fields used sparingly (`allowed-tools`); no invented license | ✓ (D2/D3) |
| No time-sensitive claims; consistent terminology; honest limitations | ✓ |
| Directory/name match | **Flagged (D1)** — verify discovery or rename |

---

## 4. The skill file

Save as `skills/github_folder_downloader/SKILL.md` (see D1 for the hyphenated-directory alternative):

````markdown
---
name: github-folder-downloader
description: Download and mirror a single GitHub repository folder (subdirectory) to a local path without cloning the whole repository. Uses a targeted GitHub API/raw tier with ZIP and TAR.GZ archive fallback, atomic commits, and rollback. Use when the user asks to fetch, download, sync, mirror, or update a specific GitHub folder, directory, subfolder, or skills folder, or provides a URL like https://github.com/OWNER/REPO/tree/REF/PATH and wants only that path. Supports ref/commit pinning, slash-branch disambiguation, dry-run planning, JSON summaries, size/file/depth limits, symlink/LFS policies, and an offline self-test. Requires Python 3.10+; standard library only.
allowed-tools: Bash, Read
---

# GitHub Folder Downloader

Fetch one folder from a GitHub repository — not the whole repo, not a clone.
Bundled script: `scripts/github_folder_downloader.py` (v3.1.0, single file, stdlib only).

All commands below assume the working directory is this skill's folder
(`skills/github_folder_downloader/`). From elsewhere, prefix the script path accordingly.

## When to use this skill

- "Download just the `skills/…` folder from this repo."
- "Mirror `https://github.com/OWNER/REPO/tree/REF/PATH` into a local directory."
- "Sync/update a GitHub subdirectory without a full clone or sparse checkout."
- "Fetch a folder at a specific branch, tag, or commit, reproducibly."

## When NOT to use it

- The user needs full Git history, multiple folders, or the entire repo → use `git clone`.
- The user needs **Git LFS file payloads** or **submodule contents** → this script materializes LFS pointers only and skips submodules; use `git`/`git-lfs`.
- Non-`github.com` hosts, `blob/…` URLs, or URLs with query/fragment/credentials → rejected by design.

## Requirements

- Python **3.10+**, standard library only (no installs).
- HTTPS access to `github.com`, `api.github.com`, `raw.githubusercontent.com`, `codeload.github.com`.
- Optional: a GitHub token in an environment variable (default `GITHUB_TOKEN`) for private repos and higher rate limits. **Never pass tokens as CLI arguments or print them.**

## Quick start

```bash
# 1) Offline gate (no network): expect "Ran 5 tests ... OK", exit 0
python3 scripts/github_folder_downloader.py --self-test

# 2) Plan only — resolves the ref and reports counts; writes nothing
python3 scripts/github_folder_downloader.py \
  "https://github.com/nordeim/my-pi-agent/tree/main/skills/solving-a-level-exam-papers" \
  /tmp/skill --dry-run --json

# 3) Execute
python3 scripts/github_folder_downloader.py \
  "https://github.com/nordeim/my-pi-agent/tree/main/skills/solving-a-level-exam-papers" \
  /tmp/skill --json
```

## How it works (summary)

1. **Resolve** the ref/path. Slash-containing refs are tried at every split; multiple valid interpretations → exit 3 with candidates (never guesses).
2. **Tier 1:** targeted API tree + raw blob download (only the requested subtree), streamed to a temp stage, size + Git-blob-hash verified.
3. **Tier 2/3 fallback:** whole-repo ZIP, then TAR.GZ from codeload, selectively extracting the requested path. The archive itself must fit `--max-download-size`.
4. **Commit:** atomic per-file replace into the destination with backup + rollback on any interruption. Destination conflicts never trigger archive fallback.

Safety model: HTTPS only; credentials stripped on cross-origin redirects; symlinks/hardlinks skipped (or `--symlink-policy fail`); submodules skipped; destination writes never follow symlinks (POSIX `dir_fd`/`O_NOFOLLOW`, lstat fallback elsewhere); POSIX backslash filenames preserved; executable bits honored (0755/0644); empty Git dirs recreated; case/NFC collisions fail closed; every byte bounded (per-file, aggregate, entries, dirs, depth, decompression work, global deadline). **Nothing downloaded is ever executed.**

## CLI reference

```text
python3 scripts/github_folder_downloader.py URL DESTINATION [options]
python3 scripts/github_folder_downloader.py --self-test | --version
```

URL forms: `https://github.com/OWNER/REPO` (default branch, root) · `…/tree/REF` (whole repo at REF) · `…/tree/REF/PATH` (folder). `.git` suffix is stripped.

| Option | Default | Meaning |
|---|---|---|
| `--ref REF` | — | Pin branch/tag/commit. **The URL tail is then the folder path** (no prefix stripping). |
| `--path P` | — | Explicit folder path; **requires `--ref`**; `''` = repo root. |
| `--token-env VAR` | `GITHUB_TOKEN` | Env var holding the token. |
| `--timeout S` | 30 | Per-request timeout (seconds). |
| `--deadline S` | 900 | Global wall-clock budget for the run. |
| `--retries N` | 3 | Retries **after** the first attempt (0–10; 0 = single attempt). |
| `--backoff-base S` | 0.5 | Jittered exponential backoff base (cap 8 s). |
| `--max-download-size M` | 100 | Per-response/per-file/archive cap (MiB). |
| `--max-extracted-size M` | 250 | Aggregate reconstructed content cap (MiB). |
| `--max-files N` | 5000 | Max regular files materialized. |
| `--max-dirs N` | 20000 | Max directories materialized. |
| `--max-depth N` | 100 | Max path depth. |
| `--max-archive-entries N` | 0 | Whole-archive entry cap (0 = derive: clamp(10×files, 20000, 500000)). |
| `--max-compression-ratio N` | 1000 | **Advisory** ZIP ratio warning (0 disables). |
| `--symlink-policy skip\|fail` | skip | Symlink/hardlink handling, identical in all tiers. |
| `--lfs warn\|fail` | warn | LFS pointers: warn + materialize, or fail. Payloads never fetched. |
| `--keep-archive` | off | Retain archive in `<dest>/.ghfd-archives/` (mode 0600). |
| `--no-overwrite` | off | Refuse to overwrite existing destination files. |
| `--allow-destination-symlink` | off | Permit a symlinked destination **root** (internal links still refused). |
| `--fsync` | off | fsync each committed file (slower, power-loss durable). |
| `--dry-run` | off | Resolve + report only; writes nothing (still uses network). |
| `--json` | off | Machine-readable summary on stdout. |
| `--log-format text\|json` | text | stderr log format. |
| `--verbose` / `--quiet` | — | Debug / warnings-only logging. |

### Exit codes (stable contract)

| Code | Meaning |
|---|---|
| 0 | Success |
| 1 | Failure — inspect `error_class` in `--json` (e.g. `URLParseError`, `ResolutionError`, `RetrievalError`, `IntegrityError`, `LimitExceeded`, `DeadlineExceeded`, `CommitError`) |
| 2 | Usage/destination error (also argparse errors) |
| 3 | Ambiguous ref — re-run with `--ref` |
| 130 | Interrupted |

### JSON summary fields

`ok`, `exit_code`, `error_class`, `message`, `version`, `dry_run`, `destination`, `owner`, `repo`, `ref`, `path`, `commit`, `tier` (`dry-run`/`api`/`zip`/`tar.gz`), `files`, `directories`, `bytes`, `skipped_symlinks`, `skipped_submodules`, `lfs_pointers`, `deduplicated`, `retained_archive`, `duration_seconds`; `interpretations` on ambiguity.

## Scenarios

### 1. First-time folder download (plan, then execute)
```bash
python3 scripts/github_folder_downloader.py \
  "https://github.com/nordeim/my-pi-agent/tree/main/skills/solving-a-level-exam-papers" \
  /tmp/skill --dry-run --json
python3 scripts/github_folder_downloader.py \
  "https://github.com/nordeim/my-pi-agent/tree/main/skills/solving-a-level-exam-papers" \
  /tmp/skill --json
```
Report `tier`, `files`, `bytes`, and any `skipped_*`/`lfs_pointers` to the user.

### 2. Private repo or rate limits (token via env only)
```bash
export GITHUB_TOKEN="…"          # set in the shell; never echo or log it
python3 scripts/github_folder_downloader.py \
  "https://github.com/ORG/PRIVATE/tree/main/docs" ./docs --json
# custom env var:
GH_TOKEN_ALT="…" python3 scripts/github_folder_downloader.py URL ./out --token-env GH_TOKEN_ALT
```

### 3. Slash-branch ambiguity (exit 3) → pin the ref
```bash
# URL …/tree/feature/x/docs may mean ref feature/x + path docs, or ref feature + path x/docs
python3 scripts/github_folder_downloader.py \
  "https://github.com/o/r/tree/feature/x/docs" ./out --json   # exit 3, lists interpretations
# Canonical disambiguation: root URL + --ref + --path
python3 scripts/github_folder_downloader.py \
  "https://github.com/o/r" ./out --ref feature/x --path docs --json
```
With `--ref`, the URL tail (if any) is treated as the path — it is **not** stripped as a ref prefix.

### 4. Reproducible pin to a commit
```bash
python3 scripts/github_folder_downloader.py \
  "https://github.com/o/r" ./snapshot --ref 0123456789abcdef0123456789abcdef01234567 \
  --path skills/example --json
```

### 5. Whole repository at a ref (limits still apply)
```bash
python3 scripts/github_folder_downloader.py "https://github.com/o/r/tree/main" ./repo --json
# or default branch:
python3 scripts/github_folder_downloader.py "https://github.com/o/r" ./repo --json
```
Expect a `whole_repository_requested` warning; raise limits explicitly if needed (Scenario 7).

### 6. Updating an existing mirror / protecting existing files
```bash
# Default: overwrite atomically with rollback on interruption
python3 scripts/github_folder_downloader.py URL ./mirror --json
# Refuse any clobber:
python3 scripts/github_folder_downloader.py URL ./mirror --no-overwrite --json
```

### 7. Large or deep folder (disclose every limit change)
```bash
python3 scripts/github_folder_downloader.py URL ./big \
  --max-files 20000 --max-extracted-size 1024 --max-download-size 300 \
  --deadline 1800 --json
```
If Tier 1 fails, fallback downloads the **whole-repo archive**: it must fit `--max-download-size`. Prefer narrowing `--path` over raising caps.

### 8. Repos with Git LFS
```bash
python3 scripts/github_folder_downloader.py URL ./out --lfs fail --json   # refuse pointers
```
Default `warn` materializes pointer files and counts them in `lfs_pointers`. Payloads are never fetched — tell the user when real content is required.

### 9. Symlinks and destination safety
```bash
python3 scripts/github_folder_downloader.py URL ./out --symlink-policy fail --json
```
A symlinked destination root is refused unless `--allow-destination-symlink` is given; internal symlink components are always refused. Case/NFC collisions on macOS/Windows fail closed.

### 10. CI / audit trail
```bash
python3 scripts/github_folder_downloader.py URL ./out \
  --keep-archive --no-overwrite --json --quiet --log-format json > result.json
echo "exit=$?"
python3 -c "import json;d=json.load(open('result.json'));print(d['ok'],d['tier'],d['files'],d['error_class'])"
```
Retained archives live in `<dest>/.ghfd-archives/` (0600) and never fail a successful commit.

### 11. Offline verification / version
```bash
python3 scripts/github_folder_downloader.py --self-test   # no network; exit 0 expected
python3 scripts/github_folder_downloader.py --version     # 3.1.0
```

## Agent workflow (follow in order)

1. Confirm the URL is a supported form and the destination is acceptable to the user.
2. Run `--dry-run --json` first. Inspect `files`, `bytes`, `directories`, `skipped_*`, `lfs_pointers` against the limits.
3. Surface skips/pointers/ambiguity to the user **before** executing; choose `--ref`/`--path`, `--lfs`, `--symlink-policy`, `--no-overwrite` accordingly.
4. Execute with `--json`. Check the exit code and `ok`.
5. Report `tier`, `files`, `bytes`, `commit`, skips, and `retained_archive`. On failure, map `error_class` via Troubleshooting and propose a remedy.

**Hard rules:** never execute downloaded content; never print or log tokens; never disable or weaken guards to make a run pass; never raise limits silently — state the change and why; prefer narrowing the path over loosening caps; do not edit the bundled script to fix runtime failures (report and triage instead).

## Troubleshooting

| Symptom | Likely cause | Remedy |
|---|---|---|
| Exit 3, `interpretations` | Slash ref ambiguous | Re-run with `--ref` (+ `--path`) |
| Exit 2 | Bad flags, `--path` without `--ref`, destination not a dir / is a symlink | Fix usage; or `--allow-destination-symlink` explicitly |
| `URLParseError` | Non-github host, `blob/…`, query/fragment/credentials, encoded separators | Use a supported URL form |
| `ResolutionError` / HTTP 404 | Wrong ref/path, or private repo without token | Verify path; set `GITHUB_TOKEN` |
| HTTP 403 rate limit | Unauthenticated quota / secondary limit | Token via `--token-env`; retry later |
| `LimitExceeded` | File/aggregate/entry/dir/depth cap | Narrow path or raise the specific cap (disclose) |
| `DeadlineExceeded` | Global budget exhausted | Raise `--deadline` or narrow scope |
| `IntegrityError` | Size/blob-hash mismatch | Re-run; treat as untrusted content, do not bypass |
| `CommitError` | Existing file vs dir, `--no-overwrite`, symlink, case/NFC collision | Resolve destination conflict; rename or choose a clean dir |
| "TRUNCATED listing" | GitHub returned an incomplete directory listing | Narrow the path or retry later (never mirrors partial data) |
| Archive fallback fails on size | Whole-repo archive > `--max-download-size` | Raise that cap or use Tier 1 successfully (narrow path) |
| `lfs_pointers > 0` | LFS payloads not fetched | Use `git lfs` if real content is needed |

## Limitations (documented, not hidden)

- LFS payloads and submodule contents are never fetched; symlinks/hardlinks are not materialized.
- Sequential downloads; no resume/Range support; no directory-level locking.
- Committed files are 0644/0755; retained archives 0600; `.ghfd-archives/` is extra content inside the destination.
- Non-POSIX commit uses lstat checks (a theoretical symlink-swap race remains); Windows illegal/reserved names are rejected.
- Live GitHub behavior, Windows/macOS runners, and the author's full 78-test suite are not reproduced by the embedded 5-test smoke suite.

## Verification & integrity

```bash
python3 -m py_compile scripts/github_folder_downloader.py
python3 scripts/github_folder_downloader.py --self-test     # expect exit 0
python3 scripts/github_folder_downloader.py --version       # expect 3.1.0
sha256sum scripts/github_folder_downloader.py               # record the FULL hash as your baseline
```
The q4 delivery ledger reports 2121 lines / 94305 bytes and a truncated SHA-256; recompute and record the full hash locally rather than matching the truncated value. Treat "passes" claims as unverified until observed.

## Files in this skill

```text
skills/github_folder_downloader/
├── SKILL.md
└── scripts/
    └── github_folder_downloader.py   # q4 v3.1.0, verbatim, stdlib only
```
````

---

## 5. Packaging + verification gates (run in order; observe, don't assume)

```bash
# 1) Extract the script VERBATIM from q4.md (disclosed D5 normalization only)
python3 - <<'PY'
from pathlib import Path
import py_compile, subprocess, sys
src = Path("q4.md").read_text(encoding="utf-8")          # adjust path to your upload
start = src.index("#!/usr/bin/env python3")
end = src.rindex("sys.exit(main())") + len("sys.exit(main())")
block = src[start:end].splitlines()
body = block[1:]
if body and all((not l.strip()) or l.startswith(" ") for l in body):
    block = [block[0]] + [l[1:] if l.startswith(" ") else l for l in body]  # strip ONE uniform space
out = Path("skills/github_folder_downloader/scripts/github_folder_downloader.py")
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text("\n".join(block) + "\n", encoding="utf-8")
py_compile.compile(str(out), doraise=True)
print("extracted lines:", len(block))
PY

# 2) Offline gates (author-claimed green; must be OBSERVED here)
python3 skills/github_folder_downloader/scripts/github_folder_downloader.py --self-test
python3 skills/github_folder_downloader/scripts/github_folder_downloader.py --version   # 3.1.0
sha256sum skills/github_folder_downloader/scripts/github_folder_downloader.py            # record full hash

# 3) Frontmatter lint (stdlib)
python3 - <<'PY'
import re, pathlib
t = pathlib.Path("skills/github_folder_downloader/SKILL.md").read_text()
m = re.match(r"^---\n(.*?)\n---\n", t, re.S); assert m, "frontmatter missing"
fm = m.group(1)
name = re.search(r"^name:\s*(.+)$", fm, re.M).group(1).strip()
desc = re.search(r"^description:\s*(.+)$", fm, re.M).group(1).strip()
assert re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", name) and len(name) <= 64
assert 0 < len(desc) <= 1024
assert len(t.splitlines()) < 500
print("frontmatter OK:", name, len(desc), "chars;", len(t.splitlines()), "lines")
PY

# 4) Optional lint/type gates on the bundled script (no rule suppression)
uv pip install ruff mypy && uv run ruff check skills/github_folder_downloader/scripts/github_folder_downloader.py \
  && uv run mypy --strict skills/github_folder_downloader/scripts/github_folder_downloader.py

# 5) Live smoke (plan-only)
python3 skills/github_folder_downloader/scripts/github_folder_downloader.py \
  "https://github.com/nordeim/my-pi-agent/tree/main/skills/solving-a-level-exam-papers" \
  /tmp/skill --dry-run --json

# 6) Skill discovery check (D1): confirm the skill loads in your Claude surface.
#    If your loader enforces name == directory name:
mv skills/github_folder_downloader skills/github-folder-downloader
```

**Delivery (when repo + SSH wrapper are available):** one atomic commit —
`feat(skills): add github_folder_downloader skill (q4 v3.1.0)` — containing `SKILL.md` + verbatim script; push to `main` via your SSH wrapper. No code fixes bundled.

---

## 6. Verification ledger & handoff

| Claim | Method | Status |
|---|---|---|
| SKILL.md matches q4's actual CLI/exit codes/JSON/limits/semantics | Line-by-line cross-check vs supplied source | **Reasoned** |
| Frontmatter satisfies name/description constraints | Manual + §5 lint (to run) | **Reasoned** |
| Script compiles / self-test green / 3.1.0 | Author-claimed; §5 gates pending | **Unverifiable here** |
| Skill discovery with underscore dir + hyphenated name | Loader-dependent | **Assumed** — gate 6 |
| Extraction preserves semantics | Uniform dedent + compile + self-test | **Reasoned**, pending observation |

**Deferred debt:** D1 naming sign-off; license choice; optional `references/` split if the body grows; live slash-branch/LFS/symlink smoke; Windows/macOS runners; shipping q4's full 78-test suite; prior-audit fixes (e.g., cert-retry guard) as separate `fix:` commits — never inside this packaging commit.
