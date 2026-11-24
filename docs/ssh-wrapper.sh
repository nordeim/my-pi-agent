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

        exit_status = channel.recv_exit_status()
        sys.exit(exit_status)
    finally:
        client.close()


if __name__ == "__main__":
    main()
