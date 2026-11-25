#!/usr/bin/env bash
# seed-playwright-browsers — expose image-baked browser builds to the user's
# writable cache (called from ws-shell on every workspace shell entry).
#
# Why symlinks: the image bakes browsers into read-only /opt so every
# workspace shares one copy (~750 MB). User-space tools expect them under
# $HOME. Projects pinning a different Playwright version need a different
# browser revision — those download normally into the writable home volume.
#
# Idempotent: existing entries (including newer revisions a project
# downloaded itself) are never overwritten or removed.
set -euo pipefail

link_all() {
    local src="$1" dst="$2"
    [ -d "$src" ] || return 0
    mkdir -p "$dst"
    local entry name
    for entry in "$src"/*; do
        [ -e "$entry" ] || continue
        name="$(basename "$entry")"
        if [ -e "$dst/$name" ]; then
            continue
        fi
        ln -s "$entry" "$dst/$name"
    done
}

# Playwright Chromium revisions (chromium-XXXX, chromium_headless_shell-XXXX, ffmpeg-XXXX)
link_all /opt/ms-playwright "$HOME/.cache/ms-playwright"

# agent-browser's own Chrome build (browsers/chrome-VERSION) — agent-browser
# ignores PLAYWRIGHT_BROWSERS_PATH and always looks in $HOME/.agent-browser.
link_all /opt/agent-browser-data/.agent-browser/browsers "$HOME/.agent-browser/browsers"
