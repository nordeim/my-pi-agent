---
name: rootless-postgresql
description: Install, initialize, and run a PostgreSQL server and client locally without root on Debian (trixie/sid), for a non-root user with a writable /home/project directory. Use when asked to install or start PostgreSQL without sudo, without systemd, or when apt install fails with permission errors. Resolves the major version dynamically, extracts .debs into a user-owned prefix, and provides idempotent start/stop/status scripts.
---

# Rootless PostgreSQL — User-Space Install & Run (Debian, No Root)

Installs PostgreSQL **server + client as a non-root user** by downloading
official Debian `.deb` packages and extracting them into a user-owned prefix.
No `sudo`, no `apt-get install`, no `systemd`, no writes outside
`/home/project/`. Produces a running cluster on a non-default port, ready for
any application via `DATABASE_URL`.

## 1. Scope

- **Target:** Debian GNU/Linux 13 (trixie) or later (verified on trixie and
  sid/forky). amd64, Unix domain sockets + TCP/IP, shell as `pete` (or any
  non-root user with write access to `/home/project/`).
- **In scope:** Downloading `.deb`s, extracting to a prefix, initializing a
  cluster, configuring `postgresql.conf`, lifecycle via `pg_ctl`, creating an
  application role/database, and wiring `DATABASE_URL`.
- **Out of scope:** `systemd` units, system-wide `apt` installation, replication/HA,
  non-Debian distros, major versions other than the one shipped by the host release.

## 2. Prerequisites & Environment Probe

Run these read-only checks first. **Every check must pass before proceeding.**
On failure, print the remediation and stop — do not guess past a failed probe.

```bash
set -euo pipefail

# 1. Must be non-root (this skill never uses root)
[ "$(id -u)" -ne 0 ] || { echo "FAIL: run as a non-root user"; exit 1; }

# 2. Target directory writable
mkdir -p /home/project && [ -w /home/project ] \
  || { echo "FAIL: /home/project is not writable by $(id -un)"; exit 1; }

# 3. Debian release (trixie ships PG 17, sid/forky ships PG 18 — version is resolved dynamically)
grep -qE '^(ID=debian)' /etc/os-release \
  || { echo "WARN: not Debian — package names may differ; adapt §4"; }

# 4. Required tools present
for t in apt-get apt-cache dpkg-deb ldd; do
  command -v "$t" >/dev/null || { echo "FAIL: missing tool: $t"; exit 1; }
done

# 5. Locale probe (minimal Debian images contain only C.utf8)
ls /usr/lib/locale | head -5
# Expected: C.utf8 present. initdb will use --locale=C.UTF-8 regardless.
```

Do not run `apt-get update` — it requires root and fails with
`Permission denied` on `/var/lib/apt/lists/lock`. The base image cache is
already populated; `apt-get download` reads from it and writes only to the
current directory.

## 3. Configuration

All tunables are environment variables. Defaults match the validated setup;
override by exporting before running or by editing the generated `start_pg.sh`.

| Variable | Default | Purpose |
|---|---|---|
| `PG_MAJOR` | *(auto-resolved, §4)* | PostgreSQL major version |
| `PG_ROOT` | `/home/project/pgroot` | Extraction prefix for `.deb` contents |
| `PG_DATA` | `/home/project/pgdata` | Database cluster directory |
| `PG_PORT` | `5435` | Non-default port — avoids collision with system Postgres on 5432 |
| `PG_ROLE` | `fashion_studio_user` | Application role to create |
| `PG_SECRET` | `fashion_studio_secret` | Role password (dev default) |
| `PG_DB` | `fashion_studio_dev` | Application database |
| `PG_DEB_DIR` | `/home/project/pgdeb` | Staging dir for downloaded `.deb`s |
| `APP_DIR` | `/home/project/moda-fashion-studio` | App whose `.env` receives `DATABASE_URL` |

`PG_SECRET` defaults to a dev-grade value because the cluster is bound to
`localhost` + a user-owned Unix socket. Override for anything shared; see §10.

## 4. Directory Layout

All persistent artifacts live under `/home/project/`:

```
/home/project/
├── pgdeb/                        # downloaded .deb packages (scratch — removable after extraction)
├── pgroot/                       # extracted package tree (binaries, libs, shared files)
│   └── usr/lib/postgresql/<N>/bin/  # server + client binaries (N = PG_MAJOR)
├── pgdata/                       # PostgreSQL data directory (the cluster)
│   ├── PG_VERSION
│   ├── postgresql.conf
│   ├── pg_hba.conf
│   └── .s.PGSQL.<PORT>           # Unix socket (when unix_socket_directories = PGDATA)
├── pglog/                        # server log files (user-owned)
└── scripts/                      # operational scripts (start, stop, status)
    ├── start_pg.sh
    ├── stop_pg.sh
    └── status_pg.sh
```

`pgdeb/` is scratch. `pgroot/`, `pgdata/`, `pglog/`, and `scripts/` are persistent.
No files are written under `/etc`, `/usr` (outside `pgroot`), or `/var`.

## 5. Procedure

### Step 1 — Create workspace directories

```bash
mkdir -p /home/project/{pgdeb,pgroot,pgdata,pglog,scripts}
```

### Step 2 — Resolve PostgreSQL major version dynamically

Hardcoding `17` breaks when the host ships `18` (sid/forky) or a future major.
Resolve from the apt cache:

```bash
PG_MAJOR=$(apt-cache search --names-only '^postgresql-[0-9]+$' \
  | grep -oE '[0-9]+' | sort -n | tail -1)
[ -n "$PG_MAJOR" ] || { echo "FAIL: no postgresql-N package found in apt cache"; exit 1; }
echo "Resolved PostgreSQL major: $PG_MAJOR"
```

### Step 3 — Download packages

Run from the staging directory. `apt-get download` requires no root.

```bash
mkdir -p /home/project/pgdeb && cd /home/project/pgdeb

apt-get download \
  "postgresql-${PG_MAJOR}" \
  "postgresql-client-${PG_MAJOR}" \
  postgresql-common \
  libpq5
```

Expected: four `.deb` files (e.g. `postgresql-17_17.11-…`, `postgresql-client-17_…`,
`postgresql-common_278_all.deb`, `libpq5_…`). If the command fails with
`Unable to locate package`, confirm the exact name via
`apt-cache search --names-only '^postgresql-[0-9]+$'` and retry — do not
attempt `apt-get update`.

### Step 4 — Extract packages

`dpkg-deb -x` extracts the data archive only — no maintainer scripts, no
registration, no root required.

```bash
cd /home/project/pgdeb
mkdir -p /home/project/pgroot
for f in *.deb; do
  dpkg-deb -x "$f" /home/project/pgroot/
done
```

Verify:

```bash
PGBIN="/home/project/pgroot/usr/lib/postgresql/${PG_MAJOR}/bin"
"$PGBIN/initdb" --version
# Expected: initdb (PostgreSQL) X.Y (Debian X.Y-...)
```

Try-out finding: on stock Debian (trixie and sid) the extracted binaries link
against system libraries (`libssl`, `libicu`, `liblz4`, etc.) — **no
`LD_LIBRARY_PATH` is needed**. If `initdb --version` fails with
`error while loading shared libraries`, set:

```bash
export LD_LIBRARY_PATH="/home/project/pgroot/usr/lib/postgresql/${PG_MAJOR}/lib:${LD_LIBRARY_PATH:-}"
```

and re-test. A persistent `not found` after that indicates a genuinely missing
system library — resolve by downloading the owning package (use
`ldd "$PGBIN/postgres" | grep 'not found'` to identify it).

### Step 5 — Initialize the cluster

`initdb` must run as the non-root user who will own the server process. It
refuses to run as root.

```bash
PGBIN="/home/project/pgroot/usr/lib/postgresql/${PG_MAJOR}/bin"
PGDATA="/home/project/pgdata"

chmod 700 "$PGDATA"
"$PGBIN/initdb" \
  -D "$PGDATA" \
  -U pete \
  --auth=trust \
  --encoding=UTF8 \
  --locale=C.UTF-8
```

Flags:
- `-D` — cluster data directory.
- `-U pete` — cluster superuser matching the OS user; Unix-socket auth works
  without a separate `postgres` role.
- `--auth=trust` — appropriate for a single-user dev cluster reachable only via
  a socket in a `0700` directory owned by `pete` (see §10). For TCP exposure,
  use `scram-sha-256` and set a password.
- `--encoding=UTF8` + `--locale=C.UTF-8` — `C.UTF-8` is the only locale
  guaranteed on a minimal Debian image (`C.utf8` in `/usr/lib/locale`).

If `initdb` fails with `directory ... exists but is not empty`, the target must
be empty — remove contents only if no data is at risk, or choose a new path.
If it fails with `invalid locale settings`, run `locale -a` and confirm
`C.UTF-8`/`C.utf8` is listed; fall back to `--locale=C` with `--encoding=UTF8`.

### Step 6 — Configure the cluster

The default `unix_socket_directories = '/var/run/postgresql'` is **not writable
by a non-root user** — leaving it unchanged causes
`could not create lock file … No such file or directory` on start (confirmed in
try-out). Set it to the data directory. Use `sed` for deterministic, idempotent
edits.

```bash
PGDATA="/home/project/pgdata"
PG_PORT="5435"

# Port (non-default to avoid system Postgres on 5432)
sed -i "s/^#port = 5432/port = ${PG_PORT}/" "$PGDATA/postgresql.conf"

# Unix socket inside PGDATA — no system write needed
sed -i "s|^#unix_socket_directories = '/var/run/postgresql'|unix_socket_directories = '${PGDATA}'|" \
  "$PGDATA/postgresql.conf"

# TCP on localhost only (required for DATABASE_URL=...@localhost:PORT)
# Leave as localhost — do NOT set to '' unless Unix-socket-only operation is intended
sed -i "s/^#listen_addresses = 'localhost'/listen_addresses = 'localhost'/" \
  "$PGDATA/postgresql.conf"

# Logging to user-owned directory
sed -i "s|^#log_directory = 'log'|log_directory = '/home/project/pglog'|" \
  "$PGDATA/postgresql.conf"
sed -i "s/^#logging_collector = off/logging_collector = on/" \
  "$PGDATA/postgresql.conf"
```

Verify:

```bash
grep -E '^(port|unix_socket_directories|listen_addresses|log_directory|logging_collector)' \
  "$PGDATA/postgresql.conf"
```

If `unix_socket_directories` still points at `/var/run/postgresql`, start will
fail — re-apply the `sed` above.

### Step 7 — Create operational scripts

All scripts set `PATH` and `PGDATA`/`PGPORT` explicitly so they work from any
shell without requiring `~/.bashrc` to be sourced. They are idempotent.

**`/home/project/scripts/start_pg.sh`:**

```bash
#!/usr/bin/env bash
set -euo pipefail

PG_MAJOR="${PG_MAJOR:-$(apt-cache search --names-only '^postgresql-[0-9]+$' | grep -oE '[0-9]+' | sort -n | tail -1)}"
PG_ROOT="${PG_ROOT:-/home/project/pgroot}"
PG_DATA="${PG_DATA:-/home/project/pgdata}"
PG_PORT="${PG_PORT:-5435}"
PG_ROLE="${PG_ROLE:-fashion_studio_user}"
PG_SECRET="${PG_SECRET:-fashion_studio_secret}"
PG_DB="${PG_DB:-fashion_studio_dev}"

PGBIN="${PG_ROOT}/usr/lib/postgresql/${PG_MAJOR}/bin"
export PATH="${PGBIN}:${PATH}"
# LD_LIBRARY_PATH only if needed; harmless otherwise
export LD_LIBRARY_PATH="${PG_ROOT}/usr/lib/postgresql/${PG_MAJOR}/lib:${LD_LIBRARY_PATH:-}"

LOG_FILE="/home/project/pglog/postgres.log"
mkdir -p "$(dirname "$LOG_FILE")"

if [ ! -f "${PG_DATA}/PG_VERSION" ]; then
  echo "[pg] data directory not initialized; run initdb first (see Step 5)" >&2
  exit 1
fi

# Guard against double-start
if pg_ctl -D "$PG_DATA" status >/dev/null 2>&1; then
  echo "[pg] already running"
else
  echo "[pg] starting postgres on port ${PG_PORT}..."
  # -w waits until accepting connections; -t 30 timeout
  pg_ctl -D "$PG_DATA" -l "$LOG_FILE" -w -t 30 -o "-p ${PG_PORT}" start
  echo "[pg] server started"
fi

# Idempotent role / database bootstrap (trust auth on local socket)
if ! psql -h localhost -p "$PG_PORT" -U pete -d postgres -tAc \
    "SELECT 1 FROM pg_roles WHERE rolname='${PG_ROLE}'" | grep -q 1; then
  psql -h localhost -p "$PG_PORT" -U pete -d postgres \
    -c "CREATE ROLE \"${PG_ROLE}\" WITH LOGIN PASSWORD '${PG_SECRET}';"
fi

if ! psql -h localhost -p "$PG_PORT" -U pete -d postgres -tAc \
    "SELECT 1 FROM pg_database WHERE datname='${PG_DB}'" | grep -q 1; then
  psql -h localhost -p "$PG_PORT" -U pete -d postgres \
    -c "CREATE DATABASE \"${PG_DB}\" OWNER \"${PG_ROLE}\";"
fi

echo "[pg] ready: postgresql://${PG_ROLE}:${PG_SECRET}@localhost:${PG_PORT}/${PG_DB}"
```

**`/home/project/scripts/stop_pg.sh`:**

```bash
#!/usr/bin/env bash
set -euo pipefail
PG_MAJOR="${PG_MAJOR:-$(apt-cache search --names-only '^postgresql-[0-9]+$' | grep -oE '[0-9]+' | sort -n | tail -1)}"
PG_ROOT="${PG_ROOT:-/home/project/pgroot}"
PG_DATA="${PG_DATA:-/home/project/pgdata}"
PGBIN="${PG_ROOT}/usr/lib/postgresql/${PG_MAJOR}/bin"
export PATH="${PGBIN}:${PATH}"
pg_ctl -D "$PG_DATA" -m fast -w -t 30 stop
echo "[pg] stopped"
```

**`/home/project/scripts/status_pg.sh`:**

```bash
#!/usr/bin/env bash
set -euo pipefail
PG_MAJOR="${PG_MAJOR:-$(apt-cache search --names-only '^postgresql-[0-9]+$' | grep -oE '[0-9]+' | sort -n | tail -1)}"
PG_ROOT="${PG_ROOT:-/home/project/pgroot}"
PG_DATA="${PG_DATA:-/home/project/pgdata}"
PG_PORT="${PG_PORT:-5435}"
PGBIN="${PG_ROOT}/usr/lib/postgresql/${PG_MAJOR}/bin"
export PATH="${PGBIN}:${PATH}"
pg_ctl -D "$PG_DATA" status
pg_isready -h localhost -p "$PG_PORT" && echo "[pg] accepting connections" || echo "[pg] not ready"
```

Make executable:

```bash
chmod +x /home/project/scripts/*.sh
```

### Step 8 — Start the server

```bash
/home/project/scripts/start_pg.sh
```

Expected:

```
[pg] starting postgres on port 5435
waiting for server to start.... done
server started
[pg] ready: postgresql://fashion_studio_user:fashion_studio_secret@localhost:5435/fashion_studio_dev
```

`pg_ctl -w` waits until accepting connections. On timeout after 30 s, check
`/home/project/pglog/postgres.log`.

### Step 9 — Wire the application

```bash
APP_DIR="${APP_DIR:-/home/project/moda-fashion-studio}"
# Or the current project's directory — adjust as needed
cd "$APP_DIR"
[ -f .env ] || { [ -f .env.example ] && cp .env.example .env || touch .env; }
grep -q '^DATABASE_URL=' .env \
  && sed -i "s|^DATABASE_URL=.*|DATABASE_URL=postgresql://${PG_ROLE:-fashion_studio_user}:${PG_SECRET:-fashion_studio_secret}@localhost:${PG_PORT:-5435}/${PG_DB:-fashion_studio_dev}|" .env \
  || echo "DATABASE_URL=postgresql://${PG_ROLE:-fashion_studio_user}:${PG_SECRET:-fashion_studio_secret}@localhost:${PG_PORT:-5435}/${PG_DB:-fashion_studio_dev}" >> .env
```

Verify plumbing before migrations (fail fast with a clear cause):

```bash
PGBIN="/home/project/pgroot/usr/lib/postgresql/${PG_MAJOR}/bin"
"$PGBIN/pg_isready" -h localhost -p "${PG_PORT:-5435}"
cd "$APP_DIR" && npx tsx -e "import 'dotenv/config'; const u=process.env.DATABASE_URL; if(!u) throw new Error('DATABASE_URL not set'); console.log('DB URL set?', !!u)"
```

Only then:

```bash
cd "$APP_DIR" && npm run db:migrate && npm run db:seed
```

### Step 10 — Verify

```bash
PGBIN="/home/project/pgroot/usr/lib/postgresql/${PG_MAJOR}/bin"
PGDATA="/home/project/pgdata"
PGPORT="5435"

# 1. Server process
pg_ctl -D "$PGDATA" status

# 2. Accepting connections (TCP + socket)
pg_isready -h localhost -p "$PGPORT"
pg_isready -h "$PGDATA" -p "$PGPORT"

# 3. Client version
psql --version

# 4. Superuser query
psql -h localhost -p "$PGPORT" -U pete -d postgres -c "SELECT version();"

# 5. Application role
PGPASSWORD=fashion_studio_secret psql -h localhost -p "$PGPORT" \
  -U fashion_studio_user -d fashion_studio_dev \
  -c "SELECT current_user, current_database();"
```

Expected: `server is running`, both `pg_isready` report `accepting connections`,
`psql (PostgreSQL) X.Y`, `SELECT version()` returns a row, and the application
role query returns `fashion_studio_user | fashion_studio_dev`.

## 6. Lifecycle

```bash
# Start (idempotent — safe to re-run after reboot/crash)
/home/project/scripts/start_pg.sh

# Status
/home/project/scripts/status_pg.sh

# Stop (fast = abort transactions, disconnect clients)
/home/project/scripts/stop_pg.sh
# Variants: -m smart (wait for clients) or -m immediate (risk of recovery on restart)

# Logs
tail -f /home/project/pglog/postgres.log

# Manual connect
psql -h localhost -p 5435 -U pete -d postgres
psql -h /home/project/pgdata -p 5435 -U pete -d postgres   # via Unix socket

# Cleanup scratch packages (safe after extraction)
rm -rf /home/project/pgdeb

# Full teardown (destructive — all data lost)
/home/project/scripts/stop_pg.sh
rm -rf /home/project/pgroot /home/project/pgdata /home/project/pglog
```

No `systemd` user units or `cron` entries are created. After a reboot, re-run
`start_pg.sh`. Do not use `pg_ctlcluster` — it manages clusters under
`/etc/postgresql/` and `/var/lib/postgresql/` and cannot handle a user-space
prefix.

## 7. Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| `Unable to locate package postgresql-17` | Wrong major for this release | Use §5 Step 2 dynamic resolution (`apt-cache search`) — trixie ships 17, sid ships 18 |
| `Could not open lock file … Permission denied` on `apt-get update` | `apt` needs root | Never run `apt-get update`/`install`; use `apt-get download` + `dpkg-deb -x` only |
| `error while loading shared libraries: libpq.so.5` | Missing `LD_LIBRARY_PATH` or system lib | Export `LD_LIBRARY_PATH` as in Step 4; run `ldd $PGBIN/postgres \| grep 'not found'` to identify orphan libs |
| `could not create lock file … No such file or directory` | `unix_socket_directories` still `/var/run/postgresql` | Re-apply Step 6 `sed` for `unix_socket_directories = '/home/project/pgdata'` |
| `could not bind … Address already in use` on port 5435 | Port occupied (system Postgres or prior instance) | Check `ss -tlnp \| grep 5435`; change `PG_PORT` in `postgresql.conf` and scripts |
| `FATAL: data directory … has group or world access` | `pgdata` permissions too open | `chmod 700 /home/project/pgdata` |
| `FATAL: Peer authentication failed` | Using system `psql` wrapper or wrong `pg_hba.conf` | Use direct binary `${PGBIN}/psql` and `--auth=trust` from `initdb` |
| `initdb: invalid locale` | Requested locale not installed | Always `--locale=C.UTF-8`; verify with `locale -a` |
| `postmaster.pid already exists` | Stale PID after crash | Confirm no process: `pgrep -u pete postgres`; then remove `pgdata/postmaster.pid` only if none running |
| `DATABASE_URL not set` in app | `.env` not loaded or wrong `cwd` | Run from `APP_DIR`; verify with the dotenv one-liner in Step 9 |

## 8. Hardening (Optional)

Default posture is a `localhost`-only dev cluster with `trust` auth gated by a
`0700` directory owned by `pete` and a socket inside it — only `pete` can
traverse to the socket. Before exposing beyond `localhost`:

```bash
PGBIN="/home/project/pgroot/usr/lib/postgresql/${PG_MAJOR}/bin"
PGDATA="/home/project/pgdata"
# Ensure a password is set, then require scram-sha-256
psql -h localhost -p 5435 -U pete -d postgres -c "ALTER ROLE fashion_studio_user PASSWORD '...';"
# Edit pg_hba.conf to use scram-sha-256 for host lines, then:
pg_ctl -D "$PGDATA" reload
```

Do not set `listen_addresses = '*'` or `trust` on TCP without an explicit
tradeoff note.

## 9. Design Decisions & Tradeoffs

- **`.deb` extraction vs. source compilation:** Compilation needs a toolchain,
  takes minutes, and may not match system libs. Extraction reuses Debian's
  tested binaries and installs in seconds. Tradeoff: not registered in `dpkg`,
  so upgrades require re-running download + extraction.
- **`trust` for local connections:** Gated by `0700` on `pgdata` + socket
  inside it — only `pete` can reach it, making `trust` equivalent to `peer` for
  this single-user dev case.
- **Port 5435:** Non-default to avoid collision with a system Postgres on
  5432. If 5435 is taken, change `PG_PORT` — the scripts and `postgresql.conf`
  are the two places to update.
- **`PGDATA` as socket dir:** Required — `/var/run/postgresql` is not writable
  by a non-root user and causes lock-file failures (confirmed in try-out).
- **No `postgresql-common` wrappers:** The `.deb` wrappers in `/usr/bin` rely on
  `postgresql-common` Perl routing with `@INC` paths that break under a
  non-standard prefix. Always use direct binaries in
  `$PG_ROOT/usr/lib/postgresql/<N>/bin/`.
- **No `LD_LIBRARY_PATH` by default:** Try-out on both trixie and sid showed
  zero `not found` libs — system libs satisfy the binaries. The variable is
  documented as a fallback, not a requirement.

## 10. Verification Ledger

| Check | Command (essence) | Pass criterion | Evidence |
|---|---|---|---|
| Packages downloaded | `ls /home/project/pgdeb/*.deb` | 4 `.deb` files | Verified (try-out, sid) |
| Binaries extracted | `ls $PGBIN/initdb` | file exists + executable | Verified (try-out) |
| `initdb --version` | `$PGBIN/initdb --version` | `initdb (PostgreSQL) X.Y` | Verified (try-out: 18.6) |
| No missing libs | `ldd $PGBIN/postgres \| grep 'not found'` | zero lines | Verified (try-out) |
| Cluster initialized | `ls $PGDATA/PG_VERSION` | file exists | Verified (try-out) |
| Server starts | `pg_ctl -D $PGDATA -l … -o "-p $PORT" start` | `server started`, `pg_isready` → `accepting connections` | Verified (try-out: 5444; 5435 occupied by system PG) |
| Socket location | `ls $PGDATA/.s.PGSQL.*` | socket exists in `PGDATA` | Verified (try-out) |
| Role created | `psql -c "CREATE ROLE …"` | `CREATE ROLE` | Verified (try-out) |
| Database created | `psql -c "CREATE DATABASE …"` | `CREATE DATABASE` | Verified (try-out) |
| App role connects | `PGPASSWORD=… psql -U fashion_studio_user -d fashion_studio_dev -c "SELECT …"` | `fashion_studio_user | fashion_studio_dev` | Verified (try-out) |
| `DATABASE_URL` wiring | `npx tsx -e "…process.env.DATABASE_URL"` | `DB URL set? true` | Reasoned (pattern from reference session) |
| `npm run db:migrate/seed` | `npm run db:migrate && npm run db:seed` | exit 0 | Reasoned (requires app checkout) |

**Not verified in this environment:** Full `npm run db:migrate` / `db:seed`
output depends on the application checkout at `APP_DIR`. The DB plumbing above
is verified end-to-end; run the migrate/seed commands from the application
directory to confirm table creation and seed row counts.

## 11. Definition of Done

- [x] PostgreSQL server + client installed under `/home/project/` with only `pete` privileges.
- [x] No writes outside `/home/project/`; no `sudo`, `systemd`, or `apt-get install`.
- [x] Single coherent procedure — no duplicated content; all three prior versions merged.
- [x] Dynamic major-version resolution (trixie/sid agnostic).
- [x] `unix_socket_directories` fix validated by try-out.
- [x] Scripts are syntactically valid Bash with `set -euo pipefail` and idempotent guards.
- [x] Troubleshooting covers every failure observed or documented in prior versions.
- [x] Secrets default to dev-only values and are not persisted outside `PGDATA` + `.env`.
- [x] Ledger labels each claim as Verified / Reasoned / Unverifiable with the command to reproduce.
