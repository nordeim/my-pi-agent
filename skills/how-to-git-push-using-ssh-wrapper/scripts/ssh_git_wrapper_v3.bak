#!/usr/bin/env python3
"""
Git SSH Wrapper using Paramiko
==============================
A production-grade drop-in replacement for OpenSSH when ``git push/fetch/clone``
is needed in environments without ``openssh-client`` (e.g., minimal containers,
distrolless images, or restricted sandboxes).

Usage
-----
Set as your Git SSH transport::

    export GIT_SSH_COMMAND="/path/to/ssh_git_wrapper.py"
    git push origin main

Or use the legacy ``GIT_SSH`` variable::

    export GIT_SSH="/path/to/ssh_git_wrapper.py"
    git push origin main

Requirements
------------
- Python 3.10+
- paramiko >= 3.0 (tested up to 5.x)

Features
--------
- Auto-detects Ed25519, ECDSA, and RSA private keys (via paramiko native resolution)
- SSH agent support (``ssh-agent`` / ``SSH_AUTH_SOCK``)
- Host-key verification via ``~/.ssh/known_hosts`` with OpenSSH-compatible policies
- Respects ``-p`` / ``-p2222`` (port), ``-i`` / ``-i/path`` (identity), ``-l`` / ``-luser`` (login), and ``-o`` (options)
- Supports glued single-letter flags for ``-p``, ``-i``, ``-l``, ``-o`` only (OpenSSH-compatible)
- Preserves argument boundaries with ``shlex.join()`` (paths with spaces)
- Forwards ``SendEnv`` variables with wildcard support (required for Git protocol v2)
- Non-blocking I/O with blocking final drain and 5-second timeout — prevents packfile truncation and indefinite hangs
- Connection keepalive for long transfers
- Graceful signal forwarding (SIGINT / SIGTERM) with immediate local termination
- Cross-platform (Linux, macOS, Windows)

Known Limitations
-----------------
- No ``ProxyJump`` / ``ProxyCommand`` support (``-J``, ``-W`` flags are parsed but ignored)
- No interactive password authentication (keys or agent only)
- No ``CertificateFile`` / SSH certificate support
- No SSH config file parsing (``-F`` flag is parsed but ignored)
- ``-o`` with space-separated values that themselves contain spaces (e.g., ``-o "Match exec ..."``) is not supported
- Windows: stdin forwarding uses blocking reads; daemon thread is joined on exit
"""

from __future__ import annotations

import fnmatch
import logging
import os
import select
import shlex
import signal
import socket
import sys
import threading
import time
from typing import Any

import paramiko

# ---------------------------------------------------------------------------
# Configuration constants
# ---------------------------------------------------------------------------
DEFAULT_PORT = 22
DEFAULT_USER = "git"
DEFAULT_CONNECT_TIMEOUT = 30
DEFAULT_KEEPALIVE_INTERVAL = 30
DEFAULT_DRAIN_TIMEOUT = 5.0
KNOWN_HOSTS_PATH = os.path.expanduser("~/.ssh/known_hosts")

# SSH flags that consume exactly one argument (space-separated form)
SSH_FLAGS_WITH_ARG = frozenset({
    "-i", "-p", "-l", "-F", "-o", "-b", "-c", "-E", "-I",
    "-J", "-L", "-R", "-D", "-w", "-m", "-O", "-S", "-W",
    "-K",  # deprecated in OpenSSH but still passed by some tools
})

# SSH flags that stand alone (no argument)
SSH_FLAGS_NO_ARG = frozenset({
    "-q", "-4", "-6", "-A", "-a", "-C",
    "-f", "-g", "-k", "-M", "-N", "-n", "-s", "-T", "-t",
    "-X", "-x", "-Y", "-y", "-G",
})

# OpenSSH allows glued form only for p, i, l, o (e.g., -p2222, -i/path, -luser, -oKey=Val)
_GLUEABLE_FLAGS = frozenset({"p", "i", "l", "o"})


def _set_option(config: dict[str, Any], key: str, value: str) -> None:
    """
    Store an SSH option, normalizing the key to lowercase.
    ``SendEnv`` values are accumulated into a list so that multiple
    ``-o SendEnv=...`` directives are preserved.
    """
    key = key.lower()
    if key == "sendenv":
        existing = config["options"].get("sendenv")
        if existing is None:
            config["options"]["sendenv"] = [value]
        elif isinstance(existing, list):
            existing.append(value)
        else:
            config["options"]["sendenv"] = [existing, value]
    else:
        config["options"][key] = value


# ---------------------------------------------------------------------------
# Custom host-key policies
# ---------------------------------------------------------------------------
class AcceptNewPolicy(paramiko.MissingHostKeyPolicy):
    """
    OpenSSH-compatible ``accept-new`` policy.

    Accepts unknown host keys on first use, saves them to ``known_hosts``,
    and rejects keys that have changed (already-present keys are validated
    by paramiko before ``missing_host_key`` is called).
    """

    def missing_host_key(self, client, hostname, key):
        logging.warning(
            "Adding new host key for %s (%s) to known_hosts",
            hostname, key.get_name(),
        )
        client.get_host_keys().add(hostname, key.get_name(), key)
        try:
            client.save_host_keys(KNOWN_HOSTS_PATH)
        except Exception as exc:
            logging.warning("Could not save host key: %s", exc)


# ---------------------------------------------------------------------------
# Argument parsing
# ---------------------------------------------------------------------------
def parse_args(args: list[str]) -> dict[str, Any]:
    """
    Parse an OpenSSH-style argv list into a structured configuration dict.

    Git invokes SSH with commands like::

        ssh -o SendEnv=GIT_PROTOCOL -p 2222 -i /path/key git@host git-receive-pack '/repo.git'

    This parser:
    - Handles both space-separated and glued single-letter flags
      (``-p 2222`` and ``-p2222``, ``-i /path`` and ``-i/path``).
      Only ``-p``, ``-i``, ``-l``, and ``-o`` are allowed in glued form,
      matching OpenSSH behavior.
    - Handles ``-o`` in both ``-oOption=Value`` and ``-o Option=Value`` forms.
      Option keys are normalized to lowercase. Multiple ``SendEnv`` values
      are accumulated into a list.
    - Decomposes the host string into username, hostname, and port,
      supporting IPv6 literals (``[::1]``) and ``host:port`` suffixes.
    - Reconstructs the remote shell command with ``shlex.join()`` so that
      argument boundaries (spaces in paths) are preserved.
    - Counts ``-v`` / ``-vv`` / ``-vvv`` flags to set log verbosity.
    """
    config: dict[str, Any] = {
        "host_str": None,
        "username": None,
        "hostname": None,
        "port": DEFAULT_PORT,
        "identity": None,
        "login_name": None,
        "options": {},
        "command": None,
        "verbose": 0,
    }

    i = 0
    while i < len(args):
        arg = args[i]

        # ------------------------------------------------------------------
        # Glued single-letter flags: -p2222, -i/path, -luser, -oKey=Val
        # Only p, i, l, o are glueable per OpenSSH semantics.
        # ------------------------------------------------------------------
        if (
            len(arg) > 2
            and arg.startswith("-")
            and not arg.startswith("--")
            and arg[1] in _GLUEABLE_FLAGS
        ):
            flag = arg[1]
            value = arg[2:]
            if flag == "p":
                try:
                    config["port"] = int(value)
                except ValueError:
                    sys.stderr.write(
                        f"ssh_git_wrapper: invalid port {value!r}, "
                        f"falling back to default {DEFAULT_PORT}\n"
                    )
            elif flag == "i":
                config["identity"] = os.path.expanduser(value)
            elif flag == "l":
                config["login_name"] = value
            elif flag == "o":
                if "=" in value:
                    key, val = value.split("=", 1)
                    _set_option(config, key, val)
                else:
                    _set_option(config, value, "")
            i += 1
            continue

        # ------------------------------------------------------------------
        # Space-separated flags that consume an argument
        # ------------------------------------------------------------------
        if arg in SSH_FLAGS_WITH_ARG:
            if i + 1 < len(args):
                value = args[i + 1]
                if arg == "-p":
                    try:
                        config["port"] = int(value)
                    except ValueError:
                        sys.stderr.write(
                            f"ssh_git_wrapper: invalid port {value!r}, "
                            f"falling back to default {DEFAULT_PORT}\n"
                        )
                elif arg == "-i":
                    config["identity"] = os.path.expanduser(value)
                elif arg == "-l":
                    config["login_name"] = value
                elif arg == "-o":
                    if "=" in value:
                        key, val = value.split("=", 1)
                        _set_option(config, key, val)
                    else:
                        _set_option(config, value, "")
                # All other flags are stored but ignored for now
            i += 2
            continue

        # ------------------------------------------------------------------
        # Standalone flags (no argument)
        # ------------------------------------------------------------------
        if arg.startswith("-"):
            if arg == "-v":
                config["verbose"] += 1
                i += 1
                continue
            if arg in ("-vv", "-vvv"):
                config["verbose"] += len(arg) - 1
                i += 1
                continue
            if arg in SSH_FLAGS_NO_ARG or arg.startswith("-v"):
                i += 1
                continue
            # Unrecognised flag — skip it defensively
            i += 1
            continue

        # ------------------------------------------------------------------
        # First non-flag argument is the target host
        # ------------------------------------------------------------------
        if config["host_str"] is None:
            config["host_str"] = arg
            # Everything remaining is the remote shell command.
            # Git typically passes the entire remote command as a single
            # argument (e.g. "git-receive-pack 'nordeim/stillwater.git'").
            # shlex.join() on a single-element list re-quotes the string,
            # which GitHub's git-shell rejects ("Invalid command").
            # Fix: normalise via shlex.split() → shlex.join() so the
            # quoting is canonical and matches what the remote shell expects.
            if i + 1 < len(args):
                raw_cmd = args[i + 1 :]
                if len(raw_cmd) == 1:
                    # Single string — split then re-join to normalise quotes
                    config["command"] = shlex.join(shlex.split(raw_cmd[0]))
                else:
                    config["command"] = shlex.join(raw_cmd)
            break

        i += 1

    # ------------------------------------------------------------------
    # Decompose host string: [user@]hostname[:port]
    # ------------------------------------------------------------------
    if config["host_str"]:
        host_str = config["host_str"]

        # user@host
        if "@" in host_str:
            config["username"], host_str = host_str.split("@", 1)

        # IPv6 literal: [addr] or [addr]:port
        if host_str.startswith("["):
            bracket_end = host_str.find("]")
            if bracket_end != -1:
                config["hostname"] = host_str[1:bracket_end]
                remainder = host_str[bracket_end + 1 :]
                if remainder.startswith(":"):
                    try:
                        config["port"] = int(remainder[1:])
                    except ValueError:
                        pass
            else:
                # Malformed IPv6 — pass through as-is and hope for the best
                config["hostname"] = host_str
        elif ":" in host_str:
            # Could be host:port or bare IPv6.  If there is more than one
            # colon we assume IPv6 and leave it untouched.
            if host_str.count(":") > 1:
                config["hostname"] = host_str
            else:
                parts = host_str.rsplit(":", 1)
                try:
                    config["port"] = int(parts[1])
                    config["hostname"] = parts[0]
                except ValueError:
                    config["hostname"] = host_str
        else:
            config["hostname"] = host_str

    # -l overrides user@host user, OpenSSH semantics
    if config["login_name"]:
        config["username"] = config["login_name"]
    if not config["username"]:
        config["username"] = DEFAULT_USER

    return config


# ---------------------------------------------------------------------------
# Host-key verification
# ---------------------------------------------------------------------------
def setup_host_key_policy(
    ssh: paramiko.SSHClient, options: dict[str, str]
) -> None:
    """
    Configure host-key verification based on ``-o StrictHostKeyChecking=...``
    and the presence of ``~/.ssh/known_hosts``.

    Policy hierarchy (matching OpenSSH semantics)::

        yes         → RejectPolicy (refuse unknown / changed keys)
        accept-new  → AcceptNewPolicy (accept new, save, reject changed)
        no          → WarningPolicy (warn but connect)
        <default>   → AcceptNewPolicy (auto-add new, save, reject changed)
    """
    strict = options.get("stricthostkeychecking", "").lower()

    # Always load known_hosts if it exists — required for accept-new
    # and for default validation of previously-seen keys.
    if os.path.exists(KNOWN_HOSTS_PATH):
        try:
            ssh.load_host_keys(KNOWN_HOSTS_PATH)
            logging.debug("Loaded known_hosts from %s", KNOWN_HOSTS_PATH)
        except Exception as exc:
            logging.warning("Could not load known_hosts: %s", exc)

    if strict == "yes":
        ssh.set_missing_host_key_policy(paramiko.RejectPolicy())
    elif strict == "accept-new":
        ssh.set_missing_host_key_policy(AcceptNewPolicy())
    elif strict == "no":
        ssh.set_missing_host_key_policy(paramiko.WarningPolicy())
    else:
        # Default to accept-new: auto-add genuinely new hosts (so Git flows
        # don't break) but REJECT changed keys (the real MITM risk). This
        # matches OpenSSH StrictHostKeyChecking=accept-new and is the secure
        # default for non-interactive Git. Known/changed keys are still
        # validated against loaded known_hosts and raise BadHostKeyException.
        ssh.set_missing_host_key_policy(AcceptNewPolicy())


# ---------------------------------------------------------------------------
# I/O forwarding
# ---------------------------------------------------------------------------
def forward_stdin(
    channel: paramiko.Channel, shutdown_event: threading.Event
) -> None:
    """
    Forward local stdin to the remote SSH channel in a background thread.

    Uses ``read1()`` when available (Python 3 BufferedIOBase) for efficient
    streaming without excessive buffering.  Falls back to ``read()``.

    On Unix TTYs, ``select`` is used to avoid blocking the thread when no
    data is available, allowing faster response to ``shutdown_event``.
    """
    read_func = getattr(sys.stdin.buffer, "read1", sys.stdin.buffer.read)

    try:
        while not shutdown_event.is_set():
            # On Unix TTYs, use select to avoid blocking the thread when
            # no data is available, allowing faster response to shutdown_event.
            if (
                hasattr(select, "select")
                and not sys.platform.startswith("win")
                and sys.stdin.isatty()
            ):
                readable, _, _ = select.select([sys.stdin], [], [], 0.1)
                if not readable:
                    continue

            data = read_func(65536)
            if not data:
                # EOF — signal the remote that we are done writing
                channel.shutdown_write()
                break
            channel.sendall(data)
    except (OSError, ValueError, EOFError) as exc:
        logging.debug("Stdin forwarding stopped: %s", exc)
    finally:
        try:
            channel.shutdown_write()
        except Exception:
            pass


def io_loop(channel: paramiko.Channel) -> int:
    """
    Bidirectional I/O loop: forwards remote stdout/stderr to local streams
    and local stdin to the remote channel.

    Returns the remote command's exit status code (or 255 if the channel
    closes without providing one).
    """
    shutdown_event = threading.Event()
    stdin_thread = threading.Thread(
        target=forward_stdin,
        args=(channel, shutdown_event),
        daemon=True,
    )
    stdin_thread.start()

    # ------------------------------------------------------------------
    # Signal handlers: forward to remote AND trigger local shutdown
    # ------------------------------------------------------------------
    def _signal_handler(signum: int, _frame: Any) -> None:
        logging.debug("Received signal %d, forwarding to remote", signum)
        try:
            channel.send_signal(signum)
        except Exception:
            pass
        shutdown_event.set()

    old_handlers: dict[int, Any] = {}
    if threading.current_thread() is threading.main_thread():
        for sig_name in ("SIGINT", "SIGTERM"):
            sig = getattr(signal, sig_name, None)
            if sig is None:
                continue
            try:
                old_handlers[sig] = signal.signal(sig, _signal_handler)
            except (ValueError, OSError):
                # Signal not supported on this platform (e.g., SIGTERM on Windows)
                pass

    try:
        while not shutdown_event.is_set():
            # --- stdout ---
            if channel.recv_ready():
                data = channel.recv(65536)
                if data:
                    sys.stdout.buffer.write(data)
                    sys.stdout.buffer.flush()

            # --- stderr ---
            if channel.recv_stderr_ready():
                data = channel.recv_stderr(65536)
                if data:
                    sys.stderr.buffer.write(data)
                    sys.stderr.buffer.flush()

            # --- exit status ---
            if channel.exit_status_ready():
                # Switch to blocking mode to ensure we drain ALL remaining
                # data from the OS socket buffer before collecting the code.
                # Set a finite timeout to prevent indefinite hangs from
                # buggy or malicious servers that never send EOF.
                channel.setblocking(1)
                channel.settimeout(DEFAULT_DRAIN_TIMEOUT)

                # Drain stdout until EOF
                while True:
                    try:
                        data = channel.recv(65536)
                    except socket.timeout:
                        logging.warning(
                            "Drain timeout (%ss) on stdout — possible data loss",
                            DEFAULT_DRAIN_TIMEOUT,
                        )
                        break
                    if not data:
                        break
                    sys.stdout.buffer.write(data)
                    sys.stdout.buffer.flush()

                # Drain stderr until EOF
                while True:
                    try:
                        data = channel.recv_stderr(65536)
                    except socket.timeout:
                        logging.warning(
                            "Drain timeout (%ss) on stderr — possible data loss",
                            DEFAULT_DRAIN_TIMEOUT,
                        )
                        break
                    if not data:
                        break
                    sys.stderr.buffer.write(data)
                    sys.stderr.buffer.flush()

                break

            # Only break on closed connection, NOT on eof_received.
            # eof_received means the remote sent SSH_MSG_CHANNEL_EOF (closed
            # its stdout), but data may still be in the buffer or the exit
            # status may still be pending. Breaking here would truncate data.
            if channel.closed:
                # Quick drain of any remaining bytes before giving up
                channel.setblocking(1)
                channel.settimeout(DEFAULT_DRAIN_TIMEOUT)
                for recv_func, stream in (
                    (channel.recv, sys.stdout.buffer),
                    (channel.recv_stderr, sys.stderr.buffer),
                ):
                    while True:
                        try:
                            data = recv_func(65536)
                        except socket.timeout:
                            break
                        if not data:
                            break
                        stream.write(data)
                        stream.flush()
                break

            # Prevent tight-spinning when no data is available.
            # time.sleep() can raise InterruptedError on Unix when a signal
            # arrives; we suppress it because the signal handler sets
            # shutdown_event, which will be checked on the next iteration.
            if not (channel.recv_ready() or channel.recv_stderr_ready()):
                try:
                    time.sleep(0.01)
                except InterruptedError:
                    pass

    except Exception as exc:
        # InterruptedError from time.sleep is handled above; anything else
        # here is a genuine I/O error.
        logging.error("I/O error: %s", exc)

    finally:
        # Restore original signal handlers before cleanup
        if threading.current_thread() is threading.main_thread():
            for sig, old_handler in old_handlers.items():
                try:
                    signal.signal(sig, old_handler)
                except (ValueError, OSError):
                    pass

        shutdown_event.set()
        stdin_thread.join(timeout=2.0)

    if channel.exit_status_ready():
        return channel.recv_exit_status()
    return 255


# ---------------------------------------------------------------------------
# Main entry point
# ---------------------------------------------------------------------------
def main() -> None:
    args = sys.argv[1:]
    config = parse_args(args)

    # ------------------------------------------------------------------
    # Validate minimum required arguments
    # ------------------------------------------------------------------
    if not config["hostname"]:
        logging.error("ERROR: No host specified")
        sys.exit(1)

    if not config["command"]:
        logging.error("ERROR: No remote command specified")
        sys.exit(1)

    # ------------------------------------------------------------------
    # Logging setup
    # ------------------------------------------------------------------
    # Determine log level from -v flags and LogLevel option.
    # -v / -vv / -vvv override LogLevel if present.
    verbose = config["verbose"]
    log_level_opt = config["options"].get("loglevel", "").upper()
    if verbose >= 3 or log_level_opt == "DEBUG":
        log_level = logging.DEBUG
    elif verbose >= 2 or log_level_opt == "INFO":
        log_level = logging.INFO
    elif verbose >= 1 or log_level_opt == "WARNING":
        log_level = logging.WARNING
    else:
        log_level = logging.ERROR

    logging.basicConfig(
        level=log_level,
        format="%(levelname)s: %(message)s",
        stream=sys.stderr,
    )

    logging.debug("Host:     %s", config["hostname"])
    logging.debug("Port:     %d", config["port"])
    logging.debug("User:     %s", config["username"])
    logging.debug("Command:  %s", config["command"])
    logging.debug("Identity: %s", config.get("identity") or "<auto>")
    logging.debug("Verbose:  %d", verbose)

    # ------------------------------------------------------------------
    # Validate explicit identity file early
    # ------------------------------------------------------------------
    key_filename = config.get("identity")
    if key_filename:
        if not os.path.exists(key_filename):
            logging.error("Key file not found: %s", key_filename)
            sys.exit(1)
        if not os.access(key_filename, os.R_OK):
            logging.error("Key file not readable: %s", key_filename)
            sys.exit(1)

    # ------------------------------------------------------------------
    # Validate connection timeout
    # ------------------------------------------------------------------
    try:
        timeout = int(
            config["options"].get("connecttimeout", str(DEFAULT_CONNECT_TIMEOUT))
        )
        if timeout <= 0:
            timeout = DEFAULT_CONNECT_TIMEOUT
    except ValueError:
        logging.warning(
            "Invalid ConnectTimeout '%s', using default %d",
            config["options"].get("connecttimeout"),
            DEFAULT_CONNECT_TIMEOUT,
        )
        timeout = DEFAULT_CONNECT_TIMEOUT

    # ------------------------------------------------------------------
    # Build SSH client
    # ------------------------------------------------------------------
    ssh = paramiko.SSHClient()
    setup_host_key_policy(ssh, config["options"])

    try:
        ssh.connect(
            config["hostname"],
            port=config["port"],
            username=config["username"],
            key_filename=key_filename,
            timeout=timeout,
            allow_agent=True,      # Let paramiko try all agent keys
            look_for_keys=True,    # Let paramiko search default key paths
        )
    except paramiko.BadHostKeyException as exc:
        logging.error(
            "HOST KEY VERIFICATION FAILED: %s\n"
            "This could indicate a man-in-the-middle attack or a server re-installation.\n"
            "Remove the old key from %s to accept the new one.",
            exc,
            KNOWN_HOSTS_PATH,
        )
        sys.exit(1)
    except paramiko.PasswordRequiredException:
        logging.error(
            "ERROR: Private key is encrypted. "
            "Interactive password input is not supported."
        )
        sys.exit(1)
    except paramiko.AuthenticationException as exc:
        logging.error("Authentication failed: %s", exc)
        sys.exit(1)
    except socket.timeout:
        logging.error("Connection timed out after %d seconds", timeout)
        sys.exit(1)
    except Exception as exc:
        logging.error("SSH connection error: %s", exc)
        sys.exit(1)

    # ------------------------------------------------------------------
    # Open channel, configure keepalive, forward environment variables
    # ------------------------------------------------------------------
    transport = ssh.get_transport()
    if transport is None:
        logging.error("Failed to obtain SSH transport")
        sys.exit(1)

    try:
        keepalive = int(
            config["options"].get(
                "serveraliveinterval", str(DEFAULT_KEEPALIVE_INTERVAL)
            )
        )
        if keepalive <= 0:
            keepalive = DEFAULT_KEEPALIVE_INTERVAL
    except ValueError:
        keepalive = DEFAULT_KEEPALIVE_INTERVAL
    transport.set_keepalive(keepalive)

    channel = transport.open_session()
    channel.setblocking(0)

    # Forward SendEnv variables (Git protocol v2 requires GIT_PROTOCOL).
    # Use fnmatch to support wildcards (e.g., LC_*) and only send variables
    # that are actually set in the local environment.
    send_env_patterns = config["options"].get("sendenv", [])
    if isinstance(send_env_patterns, str):
        send_env_patterns = send_env_patterns.split()
    if send_env_patterns:
        for var_name, var_value in os.environ.items():
            if any(
                fnmatch.fnmatch(var_name, pattern) for pattern in send_env_patterns
            ):
                try:
                    channel.set_environment_variable(var_name, var_value)
                except Exception:
                    # Server may not accept the variable; this is non-fatal
                    pass

    # Execute the remote command
    channel.exec_command(config["command"])

    # ------------------------------------------------------------------
    # Run I/O loop and propagate exit code
    # ------------------------------------------------------------------
    try:
        exit_code = io_loop(channel)
    except Exception as exc:
        logging.error("Command execution failed: %s", exc)
        sys.exit(1)
    finally:
        channel.close()
        ssh.close()

    sys.exit(exit_code)


if __name__ == "__main__":
    main()
