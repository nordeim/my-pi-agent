# shellcheck shell=sh
# /etc/profile.d/agent-env.sh — interactive login-shell setup for the dev user.
#
# Runtime environment for NON-interactive processes (proxy vars, browser path)
# is injected at `podman run` time by scripts/40-workspace.sh, so tools invoked
# by AI agents without a login shell still see the proxy. This file covers
# interactive niceties and PATH entries only.

# Per-user tool locations (Claude Code native installs, bun, uv fallbacks)
export PATH="$HOME/.local/bin:$HOME/.bun/bin:$PATH"

# Node >= 24 built-in fetch ignores proxy env vars unless this is set
# (NODE_USE_ENV_PROXY shipped in Node 24.0.0) — also set as image ENV and in
# ci-setup.sh. Without it, node-based tools that use global fetch try to go
# direct and fail closed against the no-route network (audit L-3).
export NODE_USE_ENV_PROXY=1

# Python tools venv baked into the image (playwright, etc.)
export PATH="/opt/py-tools/bin:$PATH"

# Playwright browsers: user-writable cache dir. Image-baked revisions are
# symlinked into it by seed-playwright-browsers (idempotent, runs from ws-shell).
export PLAYWRIGHT_BROWSERS_PATH="$HOME/.cache/ms-playwright"

# Sensible defaults for interactive agent sessions
export EDITOR=nano
export GIT_EDITOR=nano
export PAGER=less

# Optional git identity — set via the workspace env file if provided
if [ -n "${GIT_AUTHOR_NAME:-}" ]; then export GIT_COMMITTER_NAME="$GIT_AUTHOR_NAME"; fi
if [ -n "${GIT_AUTHOR_EMAIL:-}" ]; then export GIT_COMMITTER_EMAIL="$GIT_AUTHOR_EMAIL"; export EMAIL="$GIT_AUTHOR_EMAIL"; fi
