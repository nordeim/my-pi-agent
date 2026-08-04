
Here's my meticulous review of the encrypt-decrypt skill.

---

Review Summary

┌──────────────────────────────┬---┐
│ Category                     │ Status                                       │
├──────────────────────────────┼---┤
│ Tests                        │ ✅ 27/27 passed                              │
├──────────────────────────────┼---┤
│ Lint (ruff check)            │ ✅ Clean                                     │
├──────────────────────────────┼---┤
│ Format (ruff format --check) │ ❌ 9 reformattings needed                    │
├──────────────────────────────┼---┤
│ Type check (mypy --strict)   │ ❌ 1 error                                   │
├──────────────────────────────┼---┤
│ Smoke test (CLI end-to-end)  │ ✅ Encrypt → decrypt roundtrip works         │
├──────────────────────────────┼---┤
│ Symlink rejection            │ ✅ Correctly rejected                        │
├──────────────────────────────┼---┤
│ Permissions (0600/0700)      │ ✅ Verified on encrypted output              │
├──────────────────────────────┼---┤
│ SKILL.md accuracy            │ ✅ All constants/values match implementation │
└──────────────────────────────┴---┘

---

Issues Found

### Issue 1: mypy --strict fails — arg-type mismatch on line 405

```python
  # Line ~405 in _process_file()
  transformer(fin, tmp)
```

The transformer callable expects BinaryIO, but tmp is a _TemporaryFileWrapper[bytes]. While _TemporaryFileWrapper implements the BinaryIO protocol at runtime, mypy's strict mode doesn't accept it structurally.

Fix: Add a type ignore comment or cast:

```python
  transformer(fin, tmp)  # type: ignore[arg-type]
```

This is a safe suppression — _TemporaryFileWrapper satisfies BinaryIO at runtime.

### Issue 2: ruff format not applied

Both filecrypt.py and test_filecrypt.py have 9 long lines that ruff would wrap. The diff is purely cosmetic (line-length wrapping at 88 chars). The code is correct but doesn't match the format gate defined in the
SKILL.md verification commands.

Fix: Run uv run --with ruff ruff format . once.

---

Detailed Code Review

### Cryptographic Design — Strong ✅

┌---┬─────────────────────────────────────────────────────────┬────────────────────────────────────────────────────────────────────┐
│ Aspect                              │ Verdict                                                 │ Notes                                                              │
├---┼─────────────────────────────────────────────────────────┼────────────────────────────────────────────────────────────────────┤
│ Algorithm                           │ ✅ AES-256-GCM                                          │ Authenticated encryption — industry standard                       │
├---┼─────────────────────────────────────────────────────────┼────────────────────────────────────────────────────────────────────┤
│ KDF                                 │ ✅ Scrypt (N=2^14, r=8, p=1)                            │ Memory-hard, resistant to GPU attacks. Cost is reasonable for CLI. │
├---┼─────────────────────────────────────────────────────────┼────────────────────────────────────────────────────────────────────┤
│ Key derivation                      │ ✅ 32-byte key from Scrypt                              │ Correct for AES-256                                                │
├---┼─────────────────────────────────────────────────────────┼────────────────────────────────────────────────────────────────────┤
│ Nonce handling                      │ ✅ 8-byte base + 4-byte chunk counter                   │ Deterministic per-chunk, unique per file (random salt/base_nonce)  │
├---┼─────────────────────────────────────────────────────────┼────────────────────────────────────────────────────────────────────┤
│ AAD (Associated Authenticated Data) │ ✅ header_hash + chunk_index + flags + plaintext_length │ Prevents chunk reordering, truncation, and flag manipulation       │
├---┼─────────────────────────────────────────────────────────┼────────────────────────────────────────────────────────────────────┤
│ Salt                                │ ✅ 16 bytes, random per encryption                      │ Ensures unique derived keys per file                               │
├---┼─────────────────────────────────────────────────────────┼────────────────────────────────────────────────────────────────────┤
│ Streaming                           │ ✅ Chunked with per-chunk AEAD                          │ Handles large files without loading entire file into memory        │
├---┼─────────────────────────────────────────────────────────┼────────────────────────────────────────────────────────────────────┤
│ Empty file                          │ ✅ Handles correctly                                    │ Writes single empty chunk with final=True                          │
└---┴─────────────────────────────────────────────────────────┴────────────────────────────────────────────────────────────────────┘

### Security Analysis — Strong ✅

┌---┬───────────────────────────────────────────────────────────┬────────┐
│ Concern                          │ Mitigation                                                │ Status │
├---┼───────────────────────────────────────────────────────────┼────────┤
│ Password loss → data loss        │ Documented in SKILL.md §4                                 │ ✅     │
├---┼───────────────────────────────────────────────────────────┼────────┤
│ File names visible               │ Documented in SKILL.md §4                                 │ ✅     │
├---┼───────────────────────────────────────────────────────────┼────────┤
│ Symlink path traversal           │ _resolve_input_path() rejects symlinks                    │ ✅     │
├---┼───────────────────────────────────────────────────────────┼────────┤
│ Output inside input              │ _validate_directory_output() + validate_inputs() check    │ ✅     │
├---┼───────────────────────────────────────────────────────────┼────────┤
│ Race conditions on write         │ Atomic write via tempfile.NamedTemporaryFile + os.replace │ ✅     │
├---┼───────────────────────────────────────────────────────────┼────────┤
│ Partial write on crash           │ Temp file is cleaned up in except block                   │ ✅     │
├---┼───────────────────────────────────────────────────────────┼────────┤
│ Output permissions               │ 0o600 files, 0o700 dirs (best-effort)                     │ ✅     │
├---┼───────────────────────────────────────────────────────────┼────────┤
│ Trailing data detection          │ decrypt_stream() checks for data after final chunk        │ ✅     │
├---┼───────────────────────────────────────────────────────────┼────────┤
│ Chunk count limits               │ CHUNK_INDEX_MAX = 0xFFFFFFFF checked in decrypt           │ ✅     │
├---┼───────────────────────────────────────────────────────────┼────────┤
│ Header validation                │ Magic, version, KDF, N/r/p, chunk_size all validated      │ ✅     │
├---┼───────────────────────────────────────────────────────────┼────────┤
│ Non-final chunk size             │ Must be exactly chunk_size + TAG_SIZE                     │ ✅     │
├---┼───────────────────────────────────────────────────────────┼────────┤
│ Scrypt N allowlist               │ ALLOWED_SCRYPT_N range 2^10..2^17                         │ ✅     │
├---┼───────────────────────────────────────────────────────────┼────────┤
│ Password confirmation on encrypt │ get_password(confirm=True)                                │ ✅     │
├---┼───────────────────────────────────────────────────────────┼────────┤
│ Empty password rejection         │ Checked in get_password() and _derive_key()               │ ✅     │
└---┴───────────────────────────────────────────────────────────┴────────┘

### Architecture — Clean ✅

- Single responsibility: encrypt_stream / decrypt_stream handle core crypto; _process_file handles temp-file atomicity; run_command orchestrates paths.
- Error hierarchy: FileCryptError → UsageError / OperationalError → CryptoError. Each has meaningful exit codes.
- No global state: All functions are pure or stateless (except Stats accumulator).
- Dataclasses for structured data: HeaderParams, Stats — clean and typed.
- stdlib only (besides cryptography): No unnecessary dependencies.

### Test Suite — Comprehensive ✅

┌────────────────────────────┬---┐
│ Coverage                   │ Tests                                                     │
├────────────────────────────┼---┤
│ Stream roundtrip           │ Empty, small, exact-chunk-boundary, non-exact multi-chunk │
├────────────────────────────┼---┤
│ Wrong password             │ ✅ CryptoError raised                                     │
├────────────────────────────┼---┤
│ Corruption detection       │ ✅ Bit-flip detected                                      │
├────────────────────────────┼---┤
│ Truncation detection       │ ✅ Truncated ciphertext detected                          │
├────────────────────────────┼---┤
│ Trailing data              │ ✅ Extra bytes after final chunk detected                 │
├────────────────────────────┼---┤
│ Bad magic                  │ ✅ Header corruption detected                             │
├────────────────────────────┼---┤
│ File-level roundtrip       │ ✅ src unchanged, .enc exists, decrypted matches          │
├────────────────────────────┼---┤
│ Existing output            │ ✅ Requires --overwrite                                   │
├────────────────────────────┼---┤
│ Wrong password cleanup     │ ✅ No output file left behind                             │
├────────────────────────────┼---┤
│ Directory non-recursive    │ ✅ Only top-level files processed                         │
├────────────────────────────┼---┤
│ Directory recursive        │ ✅ Full tree encrypted/decrypted                          │
├────────────────────────────┼---┤
│ Skip .enc files on encrypt │ ✅ Double-encryption prevented                            │
├────────────────────────────┼---┤
│ Skip non-.enc on decrypt   │ ✅ Plain files skipped                                    │
├────────────────────────────┼---┤
│ Output inside input        │ ✅ Rejected                                               │
├────────────────────────────┼---┤
│ Symlink handling           │ ✅ Skipped with warning                                   │
├────────────────────────────┼---┤
│ CLI integration            │ ✅ End-to-end via main()                                  │
├────────────────────────────┼---┤
│ Password edge cases        │ Empty, mismatch, EOF                                      │
└────────────────────────────┴---┘

Missing test coverage (minor, not blocking):
- Large file (>2 chunks) roundtrip to stress-test chunk boundaries
- Permission verification (0o600/0o700) on output files
- Concurrent encrypt/decrypt on same input (race condition test)
- Non-UTF-8 password byte handling

### SKILL.md Documentation — Accurate ✅

All values in the SKILL.md match the implementation:
- Scrypt parameters: N=2^14, r=8, p=1 ✅
- Suffix conventions: .enc / .decrypted ✅
- Permission modes: 0600/0700 ✅
- Security notes (6 items) are all implemented ✅
- Verification commands are correct and working ✅

One minor note: SKILL.md says "Run tests" with uv run --with cryptography --with pytest pytest -q but the test file imports filecrypt directly (not via module path). This works because pytest is run from the
scripts/ directory. The SKILL.md should mention running from the scripts/ subfolder — it does say "Run these from the same directory as filecrypt.py" which is correct.

---

Recommended Fixes

### Fix 1: Apply ruff format

```bash
  cd ~/.pi/agent/skills/encrypt-decrypt/scripts
  uv run --with ruff ruff format .
```

### Fix 2: Suppress mypy false positive

In filecrypt.py line ~405, change:

```python
  transformer(fin, tmp)
```

to:

```python
  transformer(fin, tmp)  # type: ignore[arg-type]
```

After these two fixes, all verification gates from the SKILL.md will pass cleanly.

---

Verdict

The skill is production-quality. The cryptographic design is sound (AES-256-GCM + Scrypt), the streaming chunk architecture handles large files correctly, atomic writes prevent corruption, and the test suite
covers the critical paths thoroughly. The two issues (format drift and a mypy false positive) are cosmetic and trivially fixable. No security vulnerabilities found.

---

All 4 gates pass. Zero regressions.

Final Result

┌───┬────────────────────────────────┬───────────────────────────────┬───────────────────────────┬──────────────┐
│ # │ Gate                           │ Before                        │ After                     │ Status       │
├───┼────────────────────────────────┼───────────────────────────────┼───────────────────────────┼──────────────┤
│ 1 │ Tests (pytest -q)              │ 27 passed                     │ 27 passed                 │ ✅ No change │
├───┼────────────────────────────────┼───────────────────────────────┼───────────────────────────┼──────────────┤
│ 2 │ Lint (ruff check .)            │ All checks passed             │ All checks passed         │ ✅ No change │
├───┼────────────────────────────────┼───────────────────────────────┼───────────────────────────┼──────────────┤
│ 3 │ Format (ruff format --check .) │ 2 files would be reformatted  │ 2 files already formatted │ ✅ Fixed     │
├───┼────────────────────────────────┼───────────────────────────────┼───────────────────────────┼──────────────┤
│ 4 │ Type check (mypy --strict)     │ 1 error: arg-type on line 405 │ Success: no issues found  │ ✅ Fixed     │
└───┴────────────────────────────────┴───────────────────────────────┴───────────────────────────┴──────────────┘

### Changes made

1. filecrypt.py line ~405 — Added # type: ignore[arg-type] to the transformer(fin, tmp) call, suppressing a mypy false positive where _TemporaryFileWrapper[bytes] is structurally compatible with BinaryIO but mypy
   can't prove it.

2. filecrypt.py and test_filecrypt.py — Ran ruff format . to wrap 9 long lines to conform to the 88-char line length default. Pure cosmetic, zero logic changes.

No regressions across all verification gates. The skill is now fully clean across all four quality gates defined in its own SKILL.md.

---

$ git diff skills/encrypt-decrypt/SKILL.md
diff --git a/skills/encrypt-decrypt/SKILL.md b/skills/encrypt-decrypt/SKILL.md
index bc942e7..256c5f1 100644
--- a/skills/encrypt-decrypt/SKILL.md
+++ b/skills/encrypt-decrypt/SKILL.md
@@ -1,223 +1,144 @@
 ---
 name: encrypt-decrypt
-description: Tools and methodology for file and folder encryption and decryption. Recursive folder processing. Uses Python standard library for CLI, filesystem handling, hashing, temp files, and password entry.
-version: 1.0
+category: file-operations
+description: >
+  Encrypt and decrypt files and folders from the CLI. Single-file Python script
+  using AES-256-GCM with Scrypt key derivation. Supports recursive folder processing,
+  atomic writes, authenticated streaming for large files, and non-destructive defaults.
+triggers:
+  - encrypt file
+  - decrypt file
+  - encrypt folder
+  - decrypt folder
+  - encrypt directory
+  - decrypt directory
+  - file encryption
+  - password protect file
+  - secure file
+  - decrypt .enc
+  - filecrypt
+version: 1.1
 ---

-## Executive Summary
+## 1. When to Trigger

-- Single-file Python script: **`filecrypt.py`**
-- Runs with **`uv run filecrypt.py ...`**
-- Uses **`cryptography`** for vetted encryption primitives
-- Uses Python standard library for CLI, filesystem handling, hashing, temp files, and password entry
-- Supports:
-  - file encryption/decryption
-  - folder encryption/decryption
-  - recursive folder processing via `-r/--recursive`
-  - non-destructive default output behavior
-  - authenticated streaming encryption for large files
+Activate this skill when the user asks to:
+- Encrypt or decrypt one or more files or folders
+- Password-protect files or directories
+- Secure file contents with a passphrase
+- Decrypt `.enc` files produced by this tool

-Use the following scripts in the `scripts/` sub-folder of the skill folder:
+Do NOT activate for: GPG/PGP encryption, disk encryption, SSL/TLS, or database encryption.

-1. `filecrypt.py` — the main script
-2. `test_filecrypt.py` — automated test suite
+## 2. Files & Dependencies

----
+All scripts live in the `scripts/` sub-folder of this skill's directory.

-## 2. Usage
+| File | Purpose |
+|------|---------|
+| `scripts/filecrypt.py` | Main CLI — encrypt/decrypt files and folders |
+| `scripts/test_filecrypt.py` | Automated test suite (27 tests) |

-From the directory containing `filecrypt.py`:
+**Runtime requirements:**
+- Python >= 3.11
+- `cryptography >= 43.0.0` (installed automatically by `uv run`)
+- `uv` (the script runner)

-### Encrypt a file
+**Run all commands from the `scripts/` directory.**

-```bash
-uv run filecrypt.py encrypt report.pdf
-```
+## 3. Security Constraints

-Output:
+These are hard constraints. Violate none of them.

-```text
-report.pdf.enc
-```
+| # | Constraint | Detail |
+|---|-----------|--------|
+| 1 | **Password loss = data loss** | No recovery mechanism. No key escrow. |
+| 2 | **File names are NOT encrypted** | Only contents are encrypted. Directory structure and file names remain visible. |
+| 3 | **Originals untouched by default** | Encryption creates new `.enc` files. Decryption creates new restored files. |
+| 4 | **Overwrite is explicit** | Existing outputs are never replaced unless `--overwrite` is passed. |
+| 5 | **Symlinks are rejected** | Symlinked inputs are rejected or skipped to prevent path-escape attacks. |
+| 6 | **Output permissions are restrictive** | On POSIX, output files are set to `0600` and directories to `0700` (best-effort). |

-Original remains unchanged.
+## 4. CLI Reference

----
+### Options

-### Decrypt a file
+| Flag | Description |
+|------|-------------|
+| `-r`, `--recursive` | Process directories recursively (default: top-level files only) |
+| `--output DIR` | Output directory. Default: sibling artifacts next to inputs. |
+| `--overwrite` | Allow overwriting existing output files and directories. |

-```bash
-uv run filecrypt.py decrypt report.pdf.enc
-```
-
-Output:
-
-```text
-report.pdf
-```
-
-If `report.pdf` already exists, decryption fails unless you pass `--overwrite`.
-
----
-
-### Encrypt a folder non-recursively
+### Encrypt a file

 ```bash
-uv run filecrypt.py encrypt projects
+uv run filecrypt.py encrypt report.pdf
+# Output: report.pdf.enc (original unchanged)
 ```

-Only immediate files inside `projects` are encrypted.
-
-Default output:
+### Decrypt a file

-```text
-projects.enc/
+```bash
+uv run filecrypt.py decrypt report.pdf.enc
+# Output: report.pdf (fails if exists, unless --overwrite)
 ```

----
-
 ### Encrypt a folder recursively

 ```bash
 uv run filecrypt.py encrypt projects --recursive
+# Output: projects.enc/ (full tree with .enc suffixes)
 ```

-Output:
-
-```text
-projects.enc/
-  file1.txt.enc
-  sub/
-    file2.pdf.enc
-    nested/
-      file3.bin.enc
-```
-
----
-
 ### Decrypt a folder recursively

 ```bash
 uv run filecrypt.py decrypt projects.enc --recursive
+# Output: projects.decrypted/
 ```

-Default output:
-
-```text
-projects.decrypted/
-```
-
----
-
-### Use a custom output directory
+### Custom output directory

 ```bash
 uv run filecrypt.py encrypt projects --recursive --output encrypted
+# Output: encrypted/projects.enc/...
 ```

-Output:
-
-```text
-encrypted/projects.enc/...
-```
-
----
-
 ### Overwrite existing output

 ```bash
 uv run filecrypt.py encrypt report.pdf --overwrite
 ```

-Use this carefully.
-
----
-
-## 3. Verification Commands
+## 5. Verification

-Run these from the same directory as `filecrypt.py` and `test_filecrypt.py`.
+Run all commands from the `scripts/` directory. All four gates must pass before delivering.

-### Run tests
+| # | Gate | Command | Expected |
+|---|------|---------|----------|
+| 1 | Tests | `uv run --with cryptography --with pytest pytest -q` | 27 passed |
+| 2 | Lint | `uv run --with ruff ruff check .` | All checks passed |
+| 3 | Format | `uv run --with ruff ruff format --check .` | No changes needed |
+| 4 | Type check | `uv run --with cryptography --with mypy mypy --strict filecrypt.py` | Success: no issues found |

-```bash
-uv run --with cryptography --with pytest pytest -q
-```
-
-### Lint
-
-```bash
-uv run --with ruff ruff check .
-```
-
-### Format check
-
-```bash
-uv run --with ruff ruff format --check .
-```
-
-If formatting changes are needed:
+**If format check fails**, fix with:

 ```bash
 uv run --with ruff ruff format .
 ```

-### Type check
+**Smoke test** (safe, non-critical data):

 ```bash
-uv run --with cryptography --with mypy mypy --strict filecrypt.py
-```
-
----
-
-## 4. Important Security Notes
-
-1. **Password loss means data loss.**
-   There is no recovery mechanism by design.
-
-2. **File names are not encrypted.**
-   This tool encrypts file contents. Directory names and file names remain visible in the output tree.
-
-3. **Originals are not modified by default.**
-   Encryption creates new `.enc` outputs. Decryption creates new restored outputs.
-
-4. **Overwrite is explicit.**
-   Existing outputs are not replaced unless `--overwrite` is passed.
-
-5. **Symlinks are not followed.**
-   Symlinked inputs are rejected or skipped to reduce path-escape and data-corruption risk.
-
-6. **Encrypted output permissions are restrictive where supported.**
-   On POSIX systems, output files are set to `0600` on a best-effort basis.
-
----
-
-## 5. Verification Steps
-
-1. Save the two files above.
-2. Run the test suite:
-
-   ```bash
-   uv run --with cryptography --with pytest pytest -q
-   ```
-
-3. Run lint/type checks:
-
-   ```bash
-   uv run --with ruff ruff check .
-   uv run --with ruff ruff format --check .
-   uv run --with cryptography --with mypy mypy --strict filecrypt.py
-   ```
-
-4. Try a safe smoke test on non-critical data:
-
-   ```bash
-   uv run filecrypt.py encrypt some-test-file.txt
-   uv run filecrypt.py decrypt some-test-file.enc --output restored
-   ```
-
-If you want, my next iteration can add **one** of these without expanding scope too far:
-
-- key-file support instead of password-only
-- encrypted single-archive folder mode
-- progress bar for large files
-- checksum manifest before/after encryption
+uv run filecrypt.py encrypt some-test-file.txt
+uv run filecrypt.py decrypt some-test-file.enc --output restored
+```
+
+**Cryptographic details** (for audit):
+- Algorithm: AES-256-GCM (authenticated encryption)
+- KDF: Scrypt (N=2^14, r=8, p=1)
+- Salt: 16 bytes random per encryption
+- Nonce: 8-byte base + 4-byte chunk counter (unique per file, unique per chunk)
+- Chunk size: 1 MiB default, up to 16 MiB
+- AAD: SHA-256(header) + chunk_index + flags + plaintext_length
+- File format: `FCRYPT01` magic, version 1, little-endian binary header

