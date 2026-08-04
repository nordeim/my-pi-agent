import io
import os
from pathlib import Path

import pytest

import filecrypt


PASSWORD = b"test-password-123"


def make_tree(base: Path) -> Path:
    input_dir = base / "input"
    (input_dir / "sub" / "deep").mkdir(parents=True)

    (input_dir / "a.txt").write_bytes(b"a")
    (input_dir / "sub" / "b.txt").write_bytes(b"b")
    (input_dir / "sub" / "deep" / "c.bin").write_bytes(b"c")

    return input_dir


def stream_encrypt(data: bytes) -> bytes:
    out = io.BytesIO()
    filecrypt.encrypt_stream(io.BytesIO(data), out, PASSWORD)
    return out.getvalue()


def stream_decrypt(data: bytes, password: bytes = PASSWORD) -> bytes:
    out = io.BytesIO()
    filecrypt.decrypt_stream(io.BytesIO(data), out, password)
    return out.getvalue()


def test_stream_roundtrip_empty():
    assert stream_decrypt(stream_encrypt(b"")) == b""


def test_stream_roundtrip_small():
    data = b"hello world"
    assert stream_decrypt(stream_encrypt(data)) == data


def test_stream_roundtrip_multiple_chunks_exact(monkeypatch):
    monkeypatch.setattr(filecrypt, "DEFAULT_CHUNK_SIZE", 1024)

    data = os.urandom(2 * 1024)
    assert stream_decrypt(stream_encrypt(data)) == data


def test_stream_roundtrip_multiple_chunks_non_exact(monkeypatch):
    monkeypatch.setattr(filecrypt, "DEFAULT_CHUNK_SIZE", 1024)

    data = os.urandom(2 * 1024 + 5)
    assert stream_decrypt(stream_encrypt(data)) == data


def test_stream_wrong_password():
    token = stream_encrypt(b"data")

    with pytest.raises(filecrypt.CryptoError):
        stream_decrypt(token, b"wrong-password")


def test_stream_corruption_detected():
    token = bytearray(stream_encrypt(b"data"))
    token[-1] ^= 0xFF

    with pytest.raises(filecrypt.CryptoError):
        stream_decrypt(bytes(token))


def test_stream_truncation_detected():
    token = stream_encrypt(b"data")[:-1]

    with pytest.raises(filecrypt.CryptoError):
        stream_decrypt(token)


def test_stream_trailing_data_detected():
    token = stream_encrypt(b"data") + b"x"

    with pytest.raises(filecrypt.CryptoError):
        stream_decrypt(token)


def test_stream_bad_magic_detected():
    token = bytearray(stream_encrypt(b"data"))
    token[0] ^= 0xFF

    with pytest.raises(filecrypt.CryptoError):
        stream_decrypt(bytes(token))


def test_file_roundtrip(tmp_path):
    src = tmp_path / "hello.txt"
    src.write_bytes(b"hello")

    enc = tmp_path / "hello.txt.enc"
    dec = tmp_path / "out.txt"

    filecrypt.encrypt_file(src, enc, PASSWORD)
    filecrypt.decrypt_file(enc, dec, PASSWORD)

    assert src.read_bytes() == b"hello"
    assert enc.exists()
    assert dec.read_bytes() == b"hello"


def test_encrypt_existing_output_requires_overwrite(tmp_path):
    src = tmp_path / "file.txt"
    src.write_bytes(b"data")

    enc = tmp_path / "file.txt.enc"

    filecrypt.encrypt_file(src, enc, PASSWORD)

    with pytest.raises(filecrypt.OperationalError):
        filecrypt.encrypt_file(src, enc, PASSWORD)

    filecrypt.encrypt_file(src, enc, PASSWORD, overwrite=True)


def test_decrypt_wrong_password_leaves_no_output(tmp_path):
    src = tmp_path / "secret.txt"
    src.write_bytes(b"secret")

    enc = tmp_path / "secret.txt.enc"
    out = tmp_path / "recovered.txt"

    filecrypt.encrypt_file(src, enc, PASSWORD)

    with pytest.raises(filecrypt.CryptoError):
        filecrypt.decrypt_file(enc, out, b"bad-password")

    assert not out.exists()


def test_directory_nonrecursive(tmp_path):
    input_dir = make_tree(tmp_path)

    stats = filecrypt.run_command(
        command=filecrypt.MODE_ENCRYPT,
        paths=[input_dir],
        recursive=False,
        output=tmp_path / "out",
        overwrite=False,
        password=PASSWORD,
    )

    enc_dir = tmp_path / "out" / "input.enc"

    assert (enc_dir / "a.txt.enc").is_file()
    assert not (enc_dir / "sub").exists()
    assert stats.processed == 1
    assert stats.skipped == 0


def test_directory_recursive_encrypt_decrypt(tmp_path):
    input_dir = make_tree(tmp_path)

    encrypt_stats = filecrypt.run_command(
        command=filecrypt.MODE_ENCRYPT,
        paths=[input_dir],
        recursive=True,
        output=tmp_path / "out",
        overwrite=False,
        password=PASSWORD,
    )

    enc_dir = tmp_path / "out" / "input.enc"

    assert encrypt_stats.processed == 3
    assert (enc_dir / "a.txt.enc").is_file()
    assert (enc_dir / "sub" / "b.txt.enc").is_file()
    assert (enc_dir / "sub" / "deep" / "c.bin.enc").is_file()

    decrypt_stats = filecrypt.run_command(
        command=filecrypt.MODE_DECRYPT,
        paths=[enc_dir],
        recursive=True,
        output=tmp_path / "dec",
        overwrite=False,
        password=PASSWORD,
    )

    dec_dir = tmp_path / "dec" / "input.decrypted"

    assert decrypt_stats.processed == 3
    assert (dec_dir / "a.txt").read_bytes() == b"a"
    assert (dec_dir / "sub" / "b.txt").read_bytes() == b"b"
    assert (dec_dir / "sub" / "deep" / "c.bin").read_bytes() == b"c"


def test_directory_nonrecursive_decrypt_only_top_level(tmp_path):
    input_dir = make_tree(tmp_path)

    filecrypt.run_command(
        command=filecrypt.MODE_ENCRYPT,
        paths=[input_dir],
        recursive=True,
        output=tmp_path / "out",
        overwrite=False,
        password=PASSWORD,
    )

    enc_dir = tmp_path / "out" / "input.enc"

    stats = filecrypt.run_command(
        command=filecrypt.MODE_DECRYPT,
        paths=[enc_dir],
        recursive=False,
        output=tmp_path / "dec",
        overwrite=False,
        password=PASSWORD,
    )

    dec_dir = tmp_path / "dec" / "input.decrypted"

    assert stats.processed == 1
    assert (dec_dir / "a.txt").is_file()
    assert not (dec_dir / "sub").exists()


def test_directory_encrypt_skips_existing_enc_files(tmp_path):
    input_dir = make_tree(tmp_path)
    (input_dir / "already.enc").write_bytes(b"plaintext")

    stats = filecrypt.run_command(
        command=filecrypt.MODE_ENCRYPT,
        paths=[input_dir],
        recursive=True,
        output=tmp_path / "out",
        overwrite=False,
        password=PASSWORD,
    )

    enc_dir = tmp_path / "out" / "input.enc"

    assert stats.processed == 3
    assert stats.skipped == 1
    assert not (enc_dir / "already.enc.enc").exists()


def test_directory_decrypt_skips_non_enc_files(tmp_path):
    input_dir = make_tree(tmp_path)

    filecrypt.run_command(
        command=filecrypt.MODE_ENCRYPT,
        paths=[input_dir],
        recursive=True,
        output=tmp_path / "out",
        overwrite=False,
        password=PASSWORD,
    )

    enc_dir = tmp_path / "out" / "input.enc"
    (enc_dir / "note.txt").write_bytes(b"plain")

    stats = filecrypt.run_command(
        command=filecrypt.MODE_DECRYPT,
        paths=[enc_dir],
        recursive=True,
        output=tmp_path / "dec",
        overwrite=False,
        password=PASSWORD,
    )

    dec_dir = tmp_path / "dec" / "input.decrypted"

    assert stats.processed == 3
    assert stats.skipped == 1
    assert not (dec_dir / "note.txt").exists()


def test_output_inside_input_rejected(tmp_path):
    input_dir = make_tree(tmp_path)

    with pytest.raises(filecrypt.UsageError):
        filecrypt.run_command(
            command=filecrypt.MODE_ENCRYPT,
            paths=[input_dir],
            recursive=True,
            output=input_dir,
            overwrite=False,
            password=PASSWORD,
        )


def test_validate_output_inside_input(tmp_path):
    input_dir = make_tree(tmp_path)

    with pytest.raises(filecrypt.UsageError):
        filecrypt.validate_inputs(
            command=filecrypt.MODE_ENCRYPT,
            paths=[input_dir],
            output=input_dir,
        )


def test_recursive_skips_symlinks(tmp_path):
    input_dir = tmp_path / "in"
    input_dir.mkdir()

    target = input_dir / "a.txt"
    target.write_bytes(b"a")

    link = input_dir / "link.txt"

    try:
        link.symlink_to(target)
    except OSError:
        pytest.skip("Symlinks are not supported on this platform.")

    stats = filecrypt.run_command(
        command=filecrypt.MODE_ENCRYPT,
        paths=[input_dir],
        recursive=True,
        output=tmp_path / "out",
        overwrite=False,
        password=PASSWORD,
    )

    enc_dir = tmp_path / "out" / "in.enc"

    assert stats.processed == 1
    assert (enc_dir / "a.txt.enc").is_file()
    assert not (enc_dir / "link.txt.enc").exists()


def test_cli_file_roundtrip(tmp_path, monkeypatch):
    src = tmp_path / "cli.txt"
    src.write_bytes(b"cli")

    monkeypatch.setattr(filecrypt, "get_password", lambda confirm: PASSWORD)

    assert filecrypt.main(["encrypt", str(src)]) == 0

    enc = tmp_path / "cli.txt.enc"
    assert enc.exists()

    assert filecrypt.main(["decrypt", str(enc), "--output", str(tmp_path / "dec")]) == 0

    assert (tmp_path / "dec" / "cli.txt").read_bytes() == b"cli"


def test_cli_existing_output_requires_overwrite(tmp_path, monkeypatch):
    src = tmp_path / "file.txt"
    src.write_bytes(b"data")

    monkeypatch.setattr(filecrypt, "get_password", lambda confirm: PASSWORD)

    assert filecrypt.main(["encrypt", str(src)]) == 0
    assert filecrypt.main(["encrypt", str(src)]) == 1
    assert filecrypt.main(["encrypt", str(src), "--overwrite"]) == 0


def test_cli_recursive_folder(tmp_path, monkeypatch):
    input_dir = make_tree(tmp_path)

    monkeypatch.setattr(filecrypt, "get_password", lambda confirm: PASSWORD)

    rc = filecrypt.main(
        [
            "encrypt",
            str(input_dir),
            "--recursive",
            "--output",
            str(tmp_path / "cli_out"),
        ]
    )

    assert rc == 0

    enc_dir = tmp_path / "cli_out" / "input.enc"
    assert (enc_dir / "sub" / "b.txt.enc").is_file()


def test_cli_decrypt_non_enc_file_is_usage_error(tmp_path):
    src = tmp_path / "plain.txt"
    src.write_bytes(b"x")

    rc = filecrypt.main(["decrypt", str(src)])

    assert rc == 2


def test_get_password_empty(monkeypatch):
    monkeypatch.setattr(filecrypt.getpass, "getpass", lambda prompt: "")

    with pytest.raises(filecrypt.UsageError):
        filecrypt.get_password(False)


def test_get_password_mismatch(monkeypatch):
    responses = iter(["one", "two"])
    monkeypatch.setattr(
        filecrypt.getpass,
        "getpass",
        lambda prompt: next(responses),
    )

    with pytest.raises(filecrypt.UsageError):
        filecrypt.get_password(True)


def test_get_password_eof(monkeypatch):
    def eof(prompt):
        raise EOFError

    monkeypatch.setattr(filecrypt.getpass, "getpass", eof)

    with pytest.raises(filecrypt.UsageError):
        filecrypt.get_password(False)
