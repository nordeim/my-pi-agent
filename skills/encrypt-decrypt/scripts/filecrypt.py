#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "cryptography>=43.0.0",
# ]
# ///
"""
filecrypt.py

Encrypt and decrypt files and folders from the command line.

Usage examples:
  uv run filecrypt.py encrypt report.pdf
  uv run filecrypt.py encrypt projects --recursive
  uv run filecrypt.py decrypt report.pdf.enc
  uv run filecrypt.py decrypt projects.enc --recursive

Security notes:
  - Encryption is password-based. If the password is lost, data cannot be recovered.
  - File contents are encrypted. File names and directory structure remain visible.
  - Defaults are non-destructive: originals are not modified.
  - Existing outputs are not overwritten unless --overwrite is supplied.
"""

from __future__ import annotations

import argparse
import getpass
import hashlib
import os
import secrets
import struct
import sys
import tempfile
from collections.abc import Callable, Iterable, Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import BinaryIO, Optional

from cryptography.exceptions import InvalidTag
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt


MAGIC = b"FCRYPT01"
FORMAT_VERSION = 1
KDF_SCRYPT = 1

# Scrypt cost parameters.
# N=2**14 is a practical default for a local CLI tool.
# Increase N for stronger but slower key derivation.
SCRYPT_N = 2**14
SCRYPT_R = 8
SCRYPT_P = 1

SALT_SIZE = 16
BASE_NONCE_SIZE = 8
TAG_SIZE = 16

DEFAULT_CHUNK_SIZE = 1024 * 1024
MAX_CHUNK_SIZE = 16 * 1024 * 1024

# 8-byte base nonce + 4-byte chunk counter => max chunk index is uint32.
CHUNK_INDEX_MAX = 0xFFFFFFFF

# Allow decrypting files created with reasonable Scrypt costs.
ALLOWED_SCRYPT_N = frozenset(2**exponent for exponent in range(10, 18))

HEADER_STRUCT = struct.Struct("<8sBBIBB16s8sI")
RECORD_STRUCT = struct.Struct("<BI")

ENC_SUFFIX = ".enc"
DECRYPTED_SUFFIX = ".decrypted"

MODE_ENCRYPT = "encrypt"
MODE_DECRYPT = "decrypt"

OUTPUT_FILE_MODE = 0o600
OUTPUT_DIR_MODE = 0o700


class FileCryptError(Exception):
    exit_code = 1


class UsageError(FileCryptError):
    exit_code = 2


class OperationalError(FileCryptError):
    pass


class CryptoError(OperationalError):
    pass


@dataclass(frozen=True)
class HeaderParams:
    n: int
    r: int
    p: int
    salt: bytes
    base_nonce: bytes
    chunk_size: int


@dataclass
class Stats:
    processed: int = 0
    skipped: int = 0


def warn(message: str) -> None:
    print(f"Warning: {message}", file=sys.stderr)


def _chmod_best_effort(path: Path, mode: int) -> None:
    try:
        os.chmod(path, mode)
    except OSError:
        pass


def _read_full_chunk(stream: BinaryIO, size: int) -> bytes:
    data = bytearray()
    while len(data) < size:
        chunk = stream.read(size - len(data))
        if not chunk:
            break
        data.extend(chunk)
    return bytes(data)


def _read_exact(stream: BinaryIO, size: int, what: str) -> bytes:
    data = bytearray()
    while len(data) < size:
        chunk = stream.read(size - len(data))
        if not chunk:
            raise CryptoError(f"Unexpected end of file while reading {what}.")
        data.extend(chunk)
    return bytes(data)


def _build_header(params: HeaderParams) -> bytes:
    return HEADER_STRUCT.pack(
        MAGIC,
        FORMAT_VERSION,
        KDF_SCRYPT,
        params.n,
        params.r,
        params.p,
        params.salt,
        params.base_nonce,
        params.chunk_size,
    )


def _parse_header(header: bytes) -> HeaderParams:
    if len(header) != HEADER_STRUCT.size:
        raise CryptoError("Invalid encrypted file: header length mismatch.")

    (
        magic,
        version,
        kdf_id,
        n,
        r,
        p,
        salt,
        base_nonce,
        chunk_size,
    ) = HEADER_STRUCT.unpack(header)

    if magic != MAGIC:
        raise CryptoError("Invalid encrypted file: bad magic.")
    if version != FORMAT_VERSION:
        raise CryptoError("Unsupported encrypted file format version.")
    if kdf_id != KDF_SCRYPT:
        raise CryptoError("Unsupported key derivation function.")
    if n not in ALLOWED_SCRYPT_N:
        raise CryptoError("Unsupported Scrypt cost parameter.")
    if not 1 <= r <= 32 or not 1 <= p <= 16:
        raise CryptoError("Unsupported Scrypt parameter.")
    if not 1 <= chunk_size <= MAX_CHUNK_SIZE:
        raise CryptoError("Unsupported chunk size.")

    return HeaderParams(
        n=n,
        r=r,
        p=p,
        salt=salt,
        base_nonce=base_nonce,
        chunk_size=chunk_size,
    )


def _derive_key(password: bytes, params: HeaderParams) -> bytes:
    if not password:
        raise UsageError("Password must not be empty.")

    try:
        kdf = Scrypt(
            salt=params.salt,
            length=32,
            n=params.n,
            r=params.r,
            p=params.p,
        )
        return kdf.derive(password)
    except ValueError as exc:
        raise CryptoError("Invalid key derivation parameters.") from exc


def _chunk_aad(
    header_hash: bytes,
    chunk_index: int,
    flags: int,
    plaintext_length: int,
) -> bytes:
    return header_hash + struct.pack("<QBI", chunk_index, flags, plaintext_length)


def _chunk_nonce(base_nonce: bytes, chunk_index: int) -> bytes:
    return base_nonce + struct.pack("<I", chunk_index)


def _write_chunk(
    fout: BinaryIO,
    aes: AESGCM,
    base_nonce: bytes,
    header_hash: bytes,
    chunk_index: int,
    plaintext: bytes,
    final: bool,
) -> None:
    if chunk_index > CHUNK_INDEX_MAX:
        raise OperationalError("File is too large for this format.")

    flags = 1 if final else 0
    plaintext_length = len(plaintext)
    aad = _chunk_aad(header_hash, chunk_index, flags, plaintext_length)
    nonce = _chunk_nonce(base_nonce, chunk_index)

    ciphertext = aes.encrypt(nonce, plaintext, aad)

    fout.write(RECORD_STRUCT.pack(flags, len(ciphertext)))
    fout.write(ciphertext)


def encrypt_stream(fin: BinaryIO, fout: BinaryIO, password: bytes) -> None:
    if not password:
        raise UsageError("Password must not be empty.")

    salt = secrets.token_bytes(SALT_SIZE)
    base_nonce = secrets.token_bytes(BASE_NONCE_SIZE)

    params = HeaderParams(
        n=SCRYPT_N,
        r=SCRYPT_R,
        p=SCRYPT_P,
        salt=salt,
        base_nonce=base_nonce,
        chunk_size=DEFAULT_CHUNK_SIZE,
    )

    header = _build_header(params)
    key = _derive_key(password, params)
    aes = AESGCM(key)
    header_hash = hashlib.sha256(header).digest()

    fout.write(header)

    chunk_index = 0
    pending = _read_full_chunk(fin, params.chunk_size)

    if pending == b"":
        _write_chunk(
            fout=fout,
            aes=aes,
            base_nonce=base_nonce,
            header_hash=header_hash,
            chunk_index=chunk_index,
            plaintext=b"",
            final=True,
        )
        return

    while True:
        next_chunk = _read_full_chunk(fin, params.chunk_size)
        final = len(next_chunk) == 0

        _write_chunk(
            fout=fout,
            aes=aes,
            base_nonce=base_nonce,
            header_hash=header_hash,
            chunk_index=chunk_index,
            plaintext=pending,
            final=final,
        )

        if final:
            break

        chunk_index += 1
        pending = next_chunk


def decrypt_stream(fin: BinaryIO, fout: BinaryIO, password: bytes) -> None:
    if not password:
        raise UsageError("Password must not be empty.")

    header = _read_exact(fin, HEADER_STRUCT.size, "header")
    params = _parse_header(header)

    key = _derive_key(password, params)
    aes = AESGCM(key)
    header_hash = hashlib.sha256(header).digest()

    chunk_index = 0

    while True:
        if chunk_index > CHUNK_INDEX_MAX:
            raise CryptoError("File contains too many chunks.")

        record = _read_exact(fin, RECORD_STRUCT.size, "chunk record")
        flags, length = RECORD_STRUCT.unpack(record)

        if flags not in (0, 1):
            raise CryptoError("Invalid chunk flags.")

        if length < TAG_SIZE or length > params.chunk_size + TAG_SIZE:
            raise CryptoError("Invalid chunk length.")

        if flags == 0 and length != params.chunk_size + TAG_SIZE:
            raise CryptoError("Invalid non-final chunk length.")

        ciphertext = _read_exact(fin, length, "chunk data")
        plaintext_length = length - TAG_SIZE

        aad = _chunk_aad(header_hash, chunk_index, flags, plaintext_length)
        nonce = _chunk_nonce(params.base_nonce, chunk_index)

        try:
            plaintext = aes.decrypt(nonce, ciphertext, aad)
        except InvalidTag as exc:
            raise CryptoError(
                "Decryption failed. The password may be incorrect or the file may be corrupted."
            ) from exc
        except ValueError as exc:
            raise CryptoError("Decryption failed due to invalid ciphertext.") from exc

        fout.write(plaintext)

        if flags == 1:
            break

        chunk_index += 1

    trailing = fin.read(1)
    if trailing:
        raise CryptoError("Encrypted file contains trailing data after final chunk.")


def _process_file(
    src: Path,
    dest: Path,
    transformer: Callable[[BinaryIO, BinaryIO], None],
    overwrite: bool,
) -> None:
    if src.is_symlink():
        raise UsageError(f"Symlink input is not supported: {src}")
    if not src.is_file():
        raise UsageError(f"Input is not a regular file: {src}")

    if dest.is_symlink():
        raise OperationalError(f"Output path is a symlink: {dest}")
    if dest.is_dir():
        raise OperationalError(f"Output path is a directory: {dest}")
    if dest.exists() and not overwrite:
        raise OperationalError(
            f"Output file already exists: {dest}. Use --overwrite to replace it."
        )

    try:
        dest.parent.mkdir(parents=True, exist_ok=True)
    except OSError as exc:
        raise OperationalError(
            f"Cannot create output directory: {dest.parent}"
        ) from exc

    tmp_path: Optional[Path] = None

    try:
        with tempfile.NamedTemporaryFile(
            delete=False,
            dir=dest.parent,
            prefix=".filecrypt-",
            suffix=".tmp",
        ) as tmp:
            tmp_path = Path(tmp.name)
            _chmod_best_effort(tmp_path, OUTPUT_FILE_MODE)

            with open(src, "rb") as fin:
                transformer(fin, tmp)  # type: ignore[arg-type]
                tmp.flush()
                os.fsync(tmp.fileno())

        os.replace(tmp_path, dest)
        tmp_path = None
        _chmod_best_effort(dest, OUTPUT_FILE_MODE)

    except (OSError, FileCryptError) as exc:
        if tmp_path is not None and tmp_path.exists():
            tmp_path.unlink(missing_ok=True)

        if isinstance(exc, FileCryptError):
            raise

        raise OperationalError(f"File operation failed: {exc}") from exc


def encrypt_file(
    src: Path,
    dest: Path,
    password: bytes,
    overwrite: bool = False,
) -> None:
    _process_file(
        src=src,
        dest=dest,
        transformer=lambda fin, fout: encrypt_stream(fin, fout, password),
        overwrite=overwrite,
    )


def decrypt_file(
    src: Path,
    dest: Path,
    password: bytes,
    overwrite: bool = False,
) -> None:
    _process_file(
        src=src,
        dest=dest,
        transformer=lambda fin, fout: decrypt_stream(fin, fout, password),
        overwrite=overwrite,
    )


def _file_output_path(
    input_path: Path,
    output_root: Optional[Path],
    mode: str,
) -> Path:
    name = input_path.name

    if mode == MODE_ENCRYPT:
        output_name = name + ENC_SUFFIX
    else:
        if not name.endswith(ENC_SUFFIX):
            raise UsageError(
                f"Decryption input must have '{ENC_SUFFIX}' suffix: {input_path}"
            )

        output_name = name[: -len(ENC_SUFFIX)]
        if not output_name:
            raise UsageError(f"Cannot derive decrypted filename for: {input_path}")

    base = output_root if output_root is not None else input_path.parent
    return base / output_name


def _directory_output_path(
    input_dir: Path,
    output_root: Optional[Path],
    mode: str,
) -> Path:
    name = input_dir.name or "directory"

    if mode == MODE_ENCRYPT:
        output_name = name + ENC_SUFFIX
    else:
        if name.endswith(ENC_SUFFIX):
            base_name = name[: -len(ENC_SUFFIX)]
        else:
            base_name = name

        if not base_name:
            base_name = "decrypted"

        output_name = base_name + DECRYPTED_SUFFIX

    base = output_root if output_root is not None else input_dir.parent
    return base / output_name


def _prepare_output_root(output: Path) -> Path:
    if output.is_symlink():
        raise UsageError(f"Output path is a symlink: {output}")

    existed = output.exists()

    if existed and not output.is_dir():
        raise UsageError(f"Output path is not a directory: {output}")

    try:
        output.mkdir(parents=True, exist_ok=True)
    except OSError as exc:
        raise OperationalError(f"Cannot create output directory: {output}") from exc

    if not existed:
        _chmod_best_effort(output, OUTPUT_DIR_MODE)

    return output.resolve(strict=False)


def _ensure_output_directory(output_dir: Path, overwrite: bool) -> None:
    if output_dir.is_symlink():
        raise OperationalError(f"Output directory is a symlink: {output_dir}")

    if output_dir.exists():
        if not output_dir.is_dir():
            raise OperationalError(f"Output path is not a directory: {output_dir}")

        try:
            is_empty = next(output_dir.iterdir(), None) is None
        except OSError as exc:
            raise OperationalError(
                f"Cannot read output directory: {output_dir}"
            ) from exc

        if not is_empty and not overwrite:
            raise OperationalError(
                f"Output directory already exists and is not empty: {output_dir}. "
                "Use --overwrite to allow writing into it."
            )
    else:
        try:
            output_dir.mkdir(parents=True, exist_ok=True)
        except OSError as exc:
            raise OperationalError(
                f"Cannot create output directory: {output_dir}"
            ) from exc

        _chmod_best_effort(output_dir, OUTPUT_DIR_MODE)


def _validate_directory_output(input_dir: Path, output_dir: Path) -> None:
    try:
        input_real = input_dir.resolve(strict=True)
        output_real = output_dir.resolve(strict=False)
    except OSError as exc:
        raise OperationalError("Cannot resolve input/output paths.") from exc

    if output_real == input_real or output_real.is_relative_to(input_real):
        raise UsageError("Output directory cannot be inside the input directory.")


def _walk_error(error: OSError) -> None:
    raise OperationalError(f"Directory traversal failed: {error}") from error


def _iter_files(root: Path, recursive: bool) -> Iterable[Path]:
    if recursive:
        for dirpath, dirnames, filenames in os.walk(
            root,
            onerror=_walk_error,
            followlinks=False,
        ):
            current = Path(dirpath)

            kept_dirs = []
            for directory in sorted(dirnames):
                dir_path = current / directory
                if dir_path.is_symlink():
                    warn(f"Skipping symlink directory: {dir_path}")
                else:
                    kept_dirs.append(directory)

            dirnames[:] = kept_dirs

            for filename in sorted(filenames):
                file_path = current / filename

                if file_path.is_symlink():
                    warn(f"Skipping symlink: {file_path}")
                    continue

                if file_path.is_file():
                    yield file_path
                else:
                    warn(f"Skipping non-regular file: {file_path}")
    else:
        try:
            entries = sorted(root.iterdir(), key=lambda path: path.name)
        except OSError as exc:
            raise OperationalError(f"Cannot read directory: {root}") from exc

        for entry in entries:
            if entry.is_symlink():
                warn(f"Skipping symlink: {entry}")
                continue

            if entry.is_file():
                yield entry
            elif entry.is_dir():
                continue
            else:
                warn(f"Skipping non-regular file: {entry}")


def _process_single_file(
    path: Path,
    output_root: Optional[Path],
    mode: str,
    password: bytes,
    overwrite: bool,
    stats: Stats,
) -> None:
    dest = _file_output_path(path, output_root, mode)

    if mode == MODE_ENCRYPT:
        encrypt_file(path, dest, password, overwrite)
    else:
        decrypt_file(path, dest, password, overwrite)

    stats.processed += 1


def _process_directory(
    input_dir: Path,
    output_root: Optional[Path],
    mode: str,
    recursive: bool,
    password: bytes,
    overwrite: bool,
    stats: Stats,
) -> None:
    output_dir = _directory_output_path(input_dir, output_root, mode)

    _validate_directory_output(input_dir, output_dir)
    _ensure_output_directory(output_dir, overwrite)

    for src_file in _iter_files(input_dir, recursive):
        rel = src_file.relative_to(input_dir)

        if mode == MODE_ENCRYPT:
            if src_file.name.endswith(ENC_SUFFIX):
                warn(
                    f"Skipping file that already has '{ENC_SUFFIX}' suffix: {src_file}"
                )
                stats.skipped += 1
                continue

            dest = output_dir / rel.with_name(src_file.name + ENC_SUFFIX)
            encrypt_file(src_file, dest, password, overwrite)
        else:
            if not src_file.name.endswith(ENC_SUFFIX):
                warn(f"Skipping file without '{ENC_SUFFIX}' suffix: {src_file}")
                stats.skipped += 1
                continue

            decrypted_name = src_file.name[: -len(ENC_SUFFIX)]
            if not decrypted_name:
                raise OperationalError(
                    f"Cannot derive decrypted filename for: {src_file}"
                )

            dest = output_dir / rel.with_name(decrypted_name)
            decrypt_file(src_file, dest, password, overwrite)

        stats.processed += 1


def _resolve_input_path(raw: Path) -> Path:
    path = Path(raw).expanduser()

    if path.is_symlink():
        raise UsageError(f"Symlink input is not supported: {path}")

    if not path.exists():
        raise UsageError(f"Input path does not exist: {path}")

    try:
        resolved = path.resolve(strict=True)
    except OSError as exc:
        raise UsageError(f"Cannot resolve input path: {path}") from exc

    if resolved.is_symlink():
        raise UsageError(f"Symlink input is not supported: {resolved}")

    if not (resolved.is_file() or resolved.is_dir()):
        raise UsageError(f"Unsupported input path: {resolved}")

    if resolved.is_dir() and resolved.name == "":
        raise UsageError("Cannot process filesystem root.")

    return resolved


def validate_inputs(
    command: str,
    paths: Sequence[Path],
    output: Optional[Path],
) -> None:
    resolved_directories = []

    for raw in paths:
        resolved = _resolve_input_path(raw)

        if (
            command == MODE_DECRYPT
            and resolved.is_file()
            and not resolved.name.endswith(ENC_SUFFIX)
        ):
            raise UsageError(
                f"Decryption input must have '{ENC_SUFFIX}' suffix: {resolved}"
            )

        if resolved.is_dir():
            resolved_directories.append(resolved)

    if output is not None:
        out = output.expanduser()

        if out.is_symlink():
            raise UsageError(f"Output path is a symlink: {out}")

        if out.exists() and not out.is_dir():
            raise UsageError(f"Output path is not a directory: {out}")

        out_resolved = out.resolve(strict=False)

        for directory in resolved_directories:
            if out_resolved == directory or out_resolved.is_relative_to(directory):
                raise UsageError(
                    "Output directory cannot be inside an input directory."
                )


def run_command(
    command: str,
    paths: Sequence[Path],
    recursive: bool,
    output: Optional[Path],
    overwrite: bool,
    password: bytes,
) -> Stats:
    stats = Stats()

    output_root = _prepare_output_root(output) if output is not None else None

    for raw_path in paths:
        path = _resolve_input_path(raw_path)

        if path.is_file():
            _process_single_file(
                path=path,
                output_root=output_root,
                mode=command,
                password=password,
                overwrite=overwrite,
                stats=stats,
            )
        elif path.is_dir():
            _process_directory(
                input_dir=path,
                output_root=output_root,
                mode=command,
                recursive=recursive,
                password=password,
                overwrite=overwrite,
                stats=stats,
            )
        else:
            raise UsageError(f"Unsupported input path: {path}")

    return stats


def get_password(confirm: bool) -> bytes:
    prompt = "Encryption password: " if confirm else "Decryption password: "

    try:
        first = getpass.getpass(prompt)
    except EOFError as exc:
        raise UsageError("Password input is required.") from exc

    if first == "":
        raise UsageError("Password must not be empty.")

    if confirm:
        try:
            second = getpass.getpass("Confirm password: ")
        except EOFError as exc:
            raise UsageError("Password input is required.") from exc

        if first != second:
            raise UsageError("Passwords do not match.")

    return first.encode("utf-8")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="filecrypt.py",
        description="Encrypt and decrypt files or folders.",
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    commands = (
        (MODE_ENCRYPT, "Encrypt files and/or folders."),
        (MODE_DECRYPT, "Decrypt files and/or folders."),
    )

    for command, help_text in commands:
        sub = subparsers.add_parser(command, help=help_text)

        sub.add_argument(
            "paths",
            nargs="+",
            type=Path,
            help="Files and/or directories to process.",
        )
        sub.add_argument(
            "-r",
            "--recursive",
            action="store_true",
            help="Process directories recursively.",
        )
        sub.add_argument(
            "--output",
            type=Path,
            help="Output directory. Defaults to sibling artifacts next to inputs.",
        )
        sub.add_argument(
            "--overwrite",
            action="store_true",
            help="Allow overwriting existing output files/directories.",
        )

    return parser


def main(argv: Optional[list[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    try:
        validate_inputs(args.command, args.paths, args.output)

        password = get_password(args.command == MODE_ENCRYPT)

        stats = run_command(
            command=args.command,
            paths=args.paths,
            recursive=args.recursive,
            output=args.output,
            overwrite=args.overwrite,
            password=password,
        )

        print(
            f"Done. Processed {stats.processed} file(s); skipped {stats.skipped} file(s)."
        )
        return 0

    except FileCryptError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return exc.exit_code

    except KeyboardInterrupt:
        print("Interrupted.", file=sys.stderr)
        return 130


if __name__ == "__main__":
    raise SystemExit(main())
