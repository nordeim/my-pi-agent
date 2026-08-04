---
name: encrypt-decrypt
description: Tools and methodology for file and folder encryption and decryption. Recursive folder processing. Uses Python standard library for CLI, filesystem handling, hashing, temp files, and password entry.
version: 1.0
---

## Executive Summary

- Single-file Python script: **`filecrypt.py`**
- Runs with **`uv run filecrypt.py ...`**
- Uses **`cryptography`** for vetted encryption primitives
- Uses Python standard library for CLI, filesystem handling, hashing, temp files, and password entry
- Supports:
  - file encryption/decryption
  - folder encryption/decryption
  - recursive folder processing via `-r/--recursive`
  - non-destructive default output behavior
  - authenticated streaming encryption for large files

Use the following scripts in the `scripts/` sub-folder of the skill folder:

1. `filecrypt.py` — the main script
2. `test_filecrypt.py` — automated test suite

---

## 2. Usage

From the directory containing `filecrypt.py`:

### Encrypt a file

```bash
uv run filecrypt.py encrypt report.pdf
```

Output:

```text
report.pdf.enc
```

Original remains unchanged.

---

### Decrypt a file

```bash
uv run filecrypt.py decrypt report.pdf.enc
```

Output:

```text
report.pdf
```

If `report.pdf` already exists, decryption fails unless you pass `--overwrite`.

---

### Encrypt a folder non-recursively

```bash
uv run filecrypt.py encrypt projects
```

Only immediate files inside `projects` are encrypted.

Default output:

```text
projects.enc/
```

---

### Encrypt a folder recursively

```bash
uv run filecrypt.py encrypt projects --recursive
```

Output:

```text
projects.enc/
  file1.txt.enc
  sub/
    file2.pdf.enc
    nested/
      file3.bin.enc
```

---

### Decrypt a folder recursively

```bash
uv run filecrypt.py decrypt projects.enc --recursive
```

Default output:

```text
projects.decrypted/
```

---

### Use a custom output directory

```bash
uv run filecrypt.py encrypt projects --recursive --output encrypted
```

Output:

```text
encrypted/projects.enc/...
```

---

### Overwrite existing output

```bash
uv run filecrypt.py encrypt report.pdf --overwrite
```

Use this carefully.

---

## 3. Verification Commands

Run these from the same directory as `filecrypt.py` and `test_filecrypt.py`.

### Run tests

```bash
uv run --with cryptography --with pytest pytest -q
```

### Lint

```bash
uv run --with ruff ruff check .
```

### Format check

```bash
uv run --with ruff ruff format --check .
```

If formatting changes are needed:

```bash
uv run --with ruff ruff format .
```

### Type check

```bash
uv run --with cryptography --with mypy mypy --strict filecrypt.py
```

---

## 4. Important Security Notes

1. **Password loss means data loss.**
   There is no recovery mechanism by design.

2. **File names are not encrypted.**
   This tool encrypts file contents. Directory names and file names remain visible in the output tree.

3. **Originals are not modified by default.**
   Encryption creates new `.enc` outputs. Decryption creates new restored outputs.

4. **Overwrite is explicit.**
   Existing outputs are not replaced unless `--overwrite` is passed.

5. **Symlinks are not followed.**
   Symlinked inputs are rejected or skipped to reduce path-escape and data-corruption risk.

6. **Encrypted output permissions are restrictive where supported.**
   On POSIX systems, output files are set to `0600` on a best-effort basis.

---

## 5. Verification Steps

1. Save the two files above.
2. Run the test suite:

   ```bash
   uv run --with cryptography --with pytest pytest -q
   ```

3. Run lint/type checks:

   ```bash
   uv run --with ruff ruff check .
   uv run --with ruff ruff format --check .
   uv run --with cryptography --with mypy mypy --strict filecrypt.py
   ```

4. Try a safe smoke test on non-critical data:

   ```bash
   uv run filecrypt.py encrypt some-test-file.txt
   uv run filecrypt.py decrypt some-test-file.enc --output restored
   ```

If you want, my next iteration can add **one** of these without expanding scope too far:

- key-file support instead of password-only
- encrypted single-archive folder mode
- progress bar for large files
- checksum manifest before/after encryption
