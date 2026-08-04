This is a meticulously designed, highly readable, and exceptionally well-structured Python script. It utilizes modern Python features (type hinting, dataclasses), delegates cryptographic heavy lifting to standard/vetted libraries (`cryptography`), and safely handles file operations with atomic replacements. 

However, when performing a deep technical and cryptographic review, several systemic trade-offs, edge cases, and areas for improvement emerge. 

Below is a detailed critique categorized by Cryptography, Architecture, Usability, and Code Quality.

---

### 1. Cryptographic & Security Analysis

#### A. The Scrypt Performance vs. Security Trade-off (Critical Flaw for Batch Processing)
You have hardcoded `SCRYPT_N = 2**14` (16,384). You correctly noted this as a "practical default for a local CLI tool." 
* **The Problem:** In 2026, $2^{14}$ is heavily susceptible to GPU/ASIC cracking if the password is weak. OWASP generally recommends $2^{17}$ or higher for file encryption.
* **The Root Cause:** Your architecture forces a new `salt` generation and a **new Scrypt derivation for every single file**. If a user recursively encrypts a directory with 10,000 files, the script calculates Scrypt 10,000 times. To make this directory traversal finish in a reasonable time, you were forced to lower the Scrypt parameters, weakening the security of *all* files.
* **The Fix:** Implement a **Key Encryption Key (KEK)** and **Data Encryption Key (DEK)** architecture. 
  1. Generate a random 32-byte DEK per file.
  2. Encrypt the file data with the DEK.
  3. Derive a KEK from the user's password *once per batch execution* using a highly secure Scrypt parameter (e.g., $N=2^{19}$).
  4. Encrypt the DEK with the KEK and store the encrypted DEK in the file header.
  *(Alternatively, you can keep the current architecture but derive the KEK once and reuse the same salt for all files in that batch, though this comes with nonce-collision risks discussed below).*

#### B. Nonce Sizing and Collision Risk
Your nonce is constructed as `base_nonce (8 bytes) + chunk_index (4 bytes)`. 
* **Current State:** Because each file generates a new random salt, the encryption key is entirely unique per file. Therefore, an 8-byte random base nonce is perfectly safe here.
* **Risk:** If you ever optimize the script to share a master key across multiple files (to solve the Scrypt performance issue), an 8-byte random nonce becomes dangerous. The Birthday Bound for 8 bytes (64 bits) means you have a high risk of nonce collision after $2^{32}$ files. If you ever move to batch-key sharing, you must increase the base nonce to 12 bytes (and use a different AEAD construction like XChaCha20-Poly1305, which supports 24-byte nonces, because AES-GCM is strictly tied to 12-byte total nonces).

#### C. Implicit vs. Explicit Header Authentication
You authenticate the header by hashing it (`header_hash = hashlib.sha256(header).digest()`) and including it in the Additional Authenticated Data (AAD) for every chunk.
* **The Good:** This safely binds every chunk to the exact file header. An attacker cannot swap chunks between files.
* **The Critique:** Because the header itself is not directly MAC'd (Message Authentication Code), the script will fully parse the header, allocate memory, run the expensive Scrypt function, and attempt to decrypt the first chunk before it realizes the header was tampered with. This opens the tool to a **CPU Exhaustion / Denial of Service attack** if fed corrupted files.

#### D. Password Normalization
You encode the password directly using `.encode("utf-8")`. If a user types the same password on a Mac and a Windows machine, Unicode composition differences (e.g., `é` as one character vs `e` + `´`) will result in different bytes, causing decryption to fail mysteriously. 
* **The Fix:** Apply `unicodedata.normalize('NFKC', password_string)` before converting to bytes.

---

### 2. Architecture & Implementation Critique

#### A. Atomic Overwrites and TOCTOU
Your file output strategy is excellent: writing to a `.tmp` file in the destination directory and using `os.replace`. This guarantees atomic writes and prevents file corruption on failure.
* **Critique:** There is a minor Time-Of-Check to Time-Of-Use (TOCTOU) race condition here:
  ```python
  if dest.exists() and not overwrite:
      raise OperationalError(...)
  # ... time passes while encrypting to tmp file ...
  os.replace(tmp_path, dest)
  ```
  If `dest` is created by another process *while* the script is encrypting a massive file, `os.replace` will silently overwrite it, bypassing your safety check.

#### B. Batch Operation Fragility (Fail-Fast)
If you run `filecrypt.py encrypt my_huge_folder --recursive`, and the script encounters a single `PermissionError` on file #4,999, the script will raise `OperationalError` and abort completely. 
* **The Fix:** For batch CLI tools, it is best practice to catch file-level `OSError`s, log a warning to `sys.stderr`, increment a `stats.failed` counter, and continue processing the rest of the directory, returning a non-zero exit code at the very end.

#### C. Chunk Validation Edge Case
You validate non-final chunks cleanly:
```python
if flags == 0 and length != params.chunk_size + TAG_SIZE:
    raise CryptoError(...)
```
You rely on `if length < TAG_SIZE or length > params.chunk_size + TAG_SIZE:` to validate the final chunk. This is entirely correct and handles 0-byte plaintext chunks flawlessly (where `length == 16`). Excellent logic here.

---

### 3. Usability & CLI Experience

#### A. Automation Roadblocks
The tool strictly uses `getpass.getpass()`. While great for interactive use, this prevents the tool from being used in shell scripts, cron jobs, or CI/CD pipelines. 
* **The Fix:** Add an optional `--pass-file` argument (to read from a secure file) or check for an environment variable like `FILECRYPT_PASSWORD`.

#### B. Symlink Spam
In `_iter_files`, every symlink encountered prints a warning to `sys.stderr`. 
* **Critique:** If a user encrypts a directory like a Node.js project or an OS config directory containing hundreds of symlinks, their terminal will be flooded with warnings, drowning out real errors. 
* **The Fix:** Only warn if a verbose flag (`-v`) is set, or simply log a summary at the end: `Skipped 42 symlinks`.

#### C. Strict Decryption Naming
The script forces decryption inputs to end with `.enc`. If a user downloads an encrypted file that got renamed by a browser or email client (e.g., `report.enc.pdf` or `report_enc`), the tool will refuse to process it unless manually renamed back.
* **The Fix:** Allow the user to specify an exact output file path via `--output` for single files, bypassing the suffix check if an explicit filename is given.

---

### 4. Code Quality & Python Best Practices

The code is exceptionally clean. Type hints are perfect, exceptions are well-hierarchized, and variable names are highly descriptive.

* **Look-ahead Chunking:** Your loop in `encrypt_stream` reads `pending` and looks ahead to `next_chunk` to correctly identify the final chunk without emitting unnecessary zero-byte final chunks. This is a very elegant implementation of streaming AEAD.
* **Resource Leaks:** Your usage of `with tempfile.NamedTemporaryFile(...) as tmp:` combined with `os.replace` outside the context manager ensures cross-platform compatibility (Windows forbids replacing open files) while ensuring proper file descriptor cleanup. This is textbook-perfect.
* **Data Packing:** `struct.Struct("<8sBBIBB16s8sI")` is highly efficient.

---

### Summary of Actionable Recommendations

If you intend to iterate on this, here is the prioritized list of changes:

1. **(Critical for Security/Performance)** Implement a **KEK/DEK** system. This allows you to bump Scrypt $N$ to at least $2^{17}$ (or use Argon2id, which `cryptography` supports) without penalizing recursive directory encryption.
2. **(Batch Reliability)** Refactor `run_command` and `_process_directory` to catch `OperationalError` per file, print a warning, and continue, rather than aborting the entire directory operation.
3. **(Automation)** Add `--password-file` or allow reading the password from `STDIN` so the script can be automated.
4. **(Localization)** Add `unicodedata.normalize('NFKC', password_string)` to prevent cross-platform password mismatch bugs.
5. **(UX)** Mute symlink skipping warnings by default to prevent terminal spam.
