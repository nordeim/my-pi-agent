---
name: encrypt-decrypt
category: file-operations
platform: ["linux", "macos", "windows"]
dependencies: ["cryptography>=43.0.0", "uv", "python>=3.11"]
description: >
  Encrypt and decrypt files and folders from the CLI. Single-file Python script
  using AES-256-GCM with Scrypt key derivation. Supports recursive folder processing,
  atomic writes, authenticated streaming for large files, and non-destructive defaults.
triggers:
  - encrypt file
  - decrypt file
  - encrypt folder
  - decrypt folder
  - encrypt directory
  - decrypt directory
  - file encryption
  - password protect file
  - secure file
  - decrypt .enc
  - filecrypt
version: 1.2
---

## 1. When to Trigger

Activate this skill when the user asks to:
- Encrypt or decrypt one or more files or folders
- Password-protect files or directories
- Secure file contents with a passphrase
- Decrypt `.enc` files produced by this tool

Do NOT activate for: GPG/PGP encryption, disk encryption, SSL/TLS, or database encryption.

## 2. Files & Dependencies

All scripts live in the `scripts/` sub-folder of this skill's directory.

| File | Purpose |
|------|---------|
| `scripts/filecrypt.py` | Main CLI — encrypt/decrypt files and folders |
| `scripts/test_filecrypt.py` | Automated test suite (27 tests) |

**Runtime requirements:**
- Python >= 3.11
- `cryptography >= 43.0.0` (installed automatically by `uv run`)
- `uv` (the script runner)

**Working directory: `scripts/` for all commands below.**

## 3. Security Constraints

These are hard constraints. Violate none of them.

| # | Constraint | Detail |
|---|-----------|--------|
| 1 | **Password loss = data loss** | No recovery mechanism. No key escrow. |
| 2 | **File names are NOT encrypted** | Only contents are encrypted. Directory structure and file names remain visible. |
| 3 | **Originals untouched by default** | Encryption creates new `.enc` files. Decryption creates new restored files. |
| 4 | **Overwrite is explicit** | Existing outputs are never replaced unless `--overwrite` is passed. |
| 5 | **Symlinks are rejected** | Symlinked inputs are rejected or skipped to prevent path-escape attacks. |
| 6 | **Output permissions are restrictive** | On POSIX, output files are set to `0600` and directories to `0700` (best-effort). |

## 4. CLI Reference

### Options

| Flag | Description |
|------|-------------|
| `-r`, `--recursive` | Process directories recursively (default: top-level files only) |
| `--output DIR` | Output directory. Default: sibling artifacts next to inputs. |
| `--overwrite` | Allow overwriting existing output files and directories. |

### Encrypt a file

```bash
uv run filecrypt.py encrypt report.pdf
# Output: report.pdf.enc (original unchanged)
```

### Decrypt a file

```bash
uv run filecrypt.py decrypt report.pdf.enc
# Output: report.pdf (fails if exists, unless --overwrite)
```

### Encrypt a folder recursively

```bash
uv run filecrypt.py encrypt projects --recursive
# Output: projects.enc/ (full tree with .enc suffixes)
```

### Decrypt a folder recursively

```bash
uv run filecrypt.py decrypt projects.enc --recursive
# Output: projects.decrypted/
```

### Decrypt a folder non-recursively

```bash
uv run filecrypt.py decrypt projects.enc
# Output: projects.decrypted/ (top-level .enc files only)
```

### Custom output directory

```bash
uv run filecrypt.py encrypt projects --recursive --output encrypted
# Output: encrypted/projects.enc/...
```

### Overwrite existing output

```bash
uv run filecrypt.py encrypt report.pdf --overwrite
```

## 5. Verification

Run all commands from the `scripts/` directory. All four gates must pass before delivering.

| # | Gate | Command | Expected |
|---|------|---------|----------|
| 1 | Tests | `uv run --with cryptography --with pytest pytest -q` | 27 passed |
| 2 | Lint | `uv run --with ruff ruff check .` | All checks passed |
| 3 | Format | `uv run --with ruff ruff format --check .` | No changes needed |
| 4 | Type check | `uv run --with cryptography --with mypy mypy --strict filecrypt.py` | Success: no issues found |

**If format check fails**, fix with:

```bash
uv run --with ruff ruff format .
```

**Smoke test** (safe, non-critical data):

```bash
uv run filecrypt.py encrypt some-test-file.txt
uv run filecrypt.py decrypt some-test-file.enc --output restored
```

**Cryptographic details** (for audit):
- Algorithm: AES-256-GCM (authenticated encryption)
- KDF: Scrypt (N=2^14, r=8, p=1)
- Salt: 16 bytes random per encryption
- Nonce: 8-byte base + 4-byte chunk counter (unique per file, unique per chunk)
- Chunk size: 1 MiB default, up to 16 MiB
- AAD: SHA-256(header) + chunk_index + flags + plaintext_length
- File format: `FCRYPT01` magic, version 1, little-endian binary header (`<8sBBIBB16s8sI`)
