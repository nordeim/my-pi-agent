---
name: tauri-2
description: "Tauri 2 (Rust backend + system webview frontend, released October 2024) cross-platform desktop and mobile app workflow skill — the Electron alternative. Covers the architecture (Rust core process via tauri::Builder + system webview via WebView2/WKWebView/GTK WebKit — NOT bundled Chromium, so binaries are 3-10 MB vs Electron's 80-150 MB), the IPC model (Tauri commands — #[tauri::command] Rust functions invoked from frontend JS via invoke('command_name', { args }), with automatic serialization via serde), plugin system (official plugins for filesystem, dialog, notification, clipboard, http, shell, os, process, updater, global-shortcut, tray, deep-link; mobile plugins for camera, geolocation, biometric, haptics, NFC), the frontend-agnostic design (use React, Vue, Svelte, Solid, Lit, vanilla JS, or any web framework — Tauri doesn't care), Tauri 2 mobile support (iOS + Android from the same Rust core), permissions system (Capability-based security — declare which commands and plugins each window can access), the build pipeline (cargo build for Rust + npm run build for frontend → bundle into .dmg/.msi/.deb/.AppImage/.ipa/.apk), Tauri CLI (npm run tauri dev / tauri build / tauri mobile init / tauri ios dev / tauri android dev), and the auto-updater (built-in, signature-verified). Use when building any desktop app (macOS/Windows/Linux) or mobile app (iOS/Android) with a web frontend — especially when the task involves Tauri commands, plugin configuration, mobile migration, the permission/capability system, or comparing Tauri vs Electron where idiomatic Tauri (Rust + system webview + IPC commands) differs fundamentally from Electron (Node.js + bundled Chromium + main/renderer process)."
license: Proprietary. LICENSE.txt has complete terms
---

# Tauri 2 — Cross-Platform Desktop & Mobile App Framework

> **Target:** Tauri 2.0+ (released October 2024) with Rust 1.77+ backend and any web frontend (React/Vue/Svelte/Solid/vanilla JS). Tauri 2 introduced **mobile support** (iOS + Android from the same codebase), a **plugin system** with official plugins, and a **Capability-based permissions system**. Tauri uses the **system webview** (WebView2 on Windows, WKWebView on macOS/iOS, GTK WebKit on Linux) instead of bundling Chromium — resulting in binaries that are 3-10 MB vs Electron's 80-150 MB.

## When to Use This Skill

Use this skill whenever the user is building, debugging, or extending a Tauri application. Trigger phrases include "Tauri", "Tauri 2", "tauri::command", "invoke('", "tauri.conf.json", "Cargo.toml tauri", "tauri dev", "tauri build", "tauri mobile", "WebView2", "WKWebView", "Tauri plugin", "tauri-plugin-fs", "tauri-plugin-dialog", "tauri-plugin-notification", "tauri-plugin-clipboard-manager", "tauri-plugin-http", "tauri-plugin-shell", "tauri-plugin-updater", "tauri-plugin-global-shortcut", "tauri-plugin-deep-link", "Capability", "AppImage", ".dmg", ".msi", and any reference to a `src-tauri/` directory or the `#[tauri::command]` attribute.

Do **not** use this skill for:
- **Tauri 1.x** — the IPC, plugin, and permission APIs are different. Tauri 2 is a breaking-change release. Migrate via `tauri migrate` CLI command.
- **Electron** — different architecture (Node.js backend + bundled Chromium vs Rust + system webview). This skill doesn't apply.
- **Pure web apps** (no desktop packaging) — see React/Vue/Svelte/Next.js skills.
- **Native mobile only** (no desktop) — see `react-native-expo` or `flutter` skills (pure mobile focus).
- **Pure Rust desktop** (without web frontend) — see `rust-web` or use egui/iced directly.

Cross-reference: `flutter` covers cross-platform mobile + desktop with Dart (different language + rendering model). `react-native-expo` covers mobile with JS/TS (no desktop).

## Quick Start

```bash
# Install prerequisites:
# - Rust 1.77+ (curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh)
# - Node.js 20+ (for the frontend tooling)
# - Platform dependencies:
#   macOS: Xcode Command Line Tools (xcode-select --install)
#   Windows: Microsoft C++ Build Tools + WebView2 (preinstalled on Win 11)
#   Linux: webkit2gtk-4.1, libgtk-3-dev, libappindicator3-dev, librsvg2-dev

# Install Tauri CLI
npm install -D @tauri-apps/cli
# OR: cargo install tauri-cli --version "^2.0"

# Create a new project (interactive — pick frontend framework)
npm create tauri-app@latest
# Prompts: project name, package manager (npm/pnpm/yarn/bun), frontend language (TS/JS),
#          UI template (Vanilla/Vue/Svelte/React/Solid/Yew/Preact/Angular),
#          UI flavor (JavaScript/TypeScript for each)

cd myapp
npm install

# Dev mode — Rust + frontend hot reload
npm run tauri dev          # Opens the desktop window with HMR

# Build for production
npm run tauri build        # Outputs to src-tauri/target/release/bundle/

# Mobile (Tauri 2 — iOS + Android from the same codebase)
npm run tauri android init
npm run tauri android dev  # Run on Android emulator/device
npm run tauri ios init     # macOS only (requires Xcode)
npm run tauri ios dev      # Run on iOS simulator
```

### Key commands

```bash
# Development
npm run tauri dev                      # Dev mode (Rust + frontend HMR)
npm run tauri dev -- --release         # Release-mode dev (faster app, slower startup)
npm run tauri dev -- --no-watch        # Disable Rust recompile on file change

# Build
npm run tauri build                    # Build all bundle types for current OS
npm run tauri build -- --bundles dmg   # macOS only: build .dmg
npm run tauri build -- --bundles msi   # Windows only: build .msi
npm run tauri build -- --bundles deb   # Linux only: build .deb
npm run tauri build -- --bundles appimage  # Linux only: build .AppImage

# Mobile (Tauri 2)
npm run tauri android init             # Generate Android project (one-time)
npm run tauri android dev             # Run on Android
npm run tauri android build           # Build .apk / .aab
npm run tauri ios init                # Generate iOS project (macOS only, one-time)
npm run tauri ios dev                 # Run on iOS simulator
npm run tauri ios build               # Build .ipa (requires Apple Developer account)

# Plugins
npm run tauri add fs                  # Add tauri-plugin-fs (npm + cargo)
npm run tauri add dialog              # Add tauri-plugin-dialog
npm run tauri add notification        # Add tauri-plugin-notification
npm run tauri add updater             # Add tauri-plugin-updater (auto-updates)
npm run tauri add global-shortcut     # Add tauri-plugin-global-shortcut
npm run tauri add deep-link           # Add tauri-plugin-deep-link (custom URL scheme)

# Migration
npm run tauri migrate                 # Migrate Tauri 1.x project to 2.x
```

---

## Project Structure (Tauri 2 canonical layout)

Tauri projects have two parts: the **frontend** (any web framework, in the project root) and the **Rust backend** (in `src-tauri/`).

```
myapp/
├── src/                          # Frontend source (this example: Vite + React)
│   ├── App.tsx                   # React root component
│   ├── main.tsx                  # Frontend entry point
│   └── components/
├── public/                       # Frontend static assets
├── package.json                  # Frontend deps
├── vite.config.ts                # Vite config (or webpack/rollup/etc.)
├── tsconfig.json
├── index.html                    # Frontend HTML entry
├── src-tauri/                    # ← Rust backend (Tauri core)
│   ├── Cargo.toml                # Rust deps (tauri, serde, plugins)
│   ├── build.rs                  # Tauri build script (codegen for commands)
│   ├── tauri.conf.json           # ← THE Tauri config (app metadata, windows, plugins)
│   ├── icons/                    # App icons (multiple sizes for each platform)
│   │   ├── icon.ico              # Windows
│   │   ├── icon.icns             # macOS
│   │   ├── 32x32.png             # Linux
│   │   └── ...
│   ├── capabilities/             # ← NEW in Tauri 2: permission/capability declarations
│   │   └── default.json          # What commands + plugins each window can access
│   ├── gen/                      # Auto-generated (mobile project scaffolding)
│   │   ├── android/              # Android Studio project
│   │   └── apple/                # Xcode project (iOS + macOS)
│   └── src/
│       ├── main.rs               # Rust entry point (tauri::Builder)
│       ├── lib.rs                # Library root (testable, used by mobile)
│       ├── commands.rs           # Tauri commands (#[tauri::command] functions)
│       ├── menu.rs               # Native menu configuration
│       ├── tray.rs               # System tray configuration
│       └── state.rs              # App state (Mutex<AppState>, managed by Tauri)
└── README.md
```

### `tauri.conf.json` (the canonical config)

```jsonc
{
  "$schema": "https://schema.tauri.app/config/2",
  "productName": "MyApp",
  "version": "1.0.0",
  "identifier": "com.example.myapp",      // Unique app ID (reverse DNS)
  "build": {
    "beforeDevCommand": "npm run dev",    // Start frontend dev server
    "devUrl": "http://localhost:1420",    // Frontend dev URL
    "beforeBuildCommand": "npm run build", // Build frontend for production
    "frontendDist": "../dist"             // Built frontend location
  },
  "app": {
    "windows": [
      {
        "title": "MyApp",
        "width": 1024,
        "height": 768,
        "minWidth": 800,
        "minHeight": 600,
        "resizable": true,
        "fullscreen": false,
        "center": true,
        "decorations": true
      }
    ],
    "security": {
      "csp": "default-src 'self'; img-src 'self' data: https:; script-src 'self' 'unsafe-eval'; style-src 'self' 'unsafe-inline'"
    },
    "withGlobalTauri": false               // Expose Tauri API globally (false = import from @tauri-apps/api)
  },
  "bundle": {
    "active": true,
    "targets": "all",                      // Or ["dmg", "msi", "deb", "appimage"]
    "icon": [
      "icons/32x32.png",
      "icons/128x128.png",
      "icons/128x128@2x.png",
      "icons/icon.icns",
      "icons/icon.ico"
    ],
    "macOS": {
      "minimumSystemVersion": "10.15",
      "signingIdentity": null              // Set for distribution signing
    },
    "windows": {
      "wix": { "language": "en-US" }
    }
  }
}
```

---

## Core Mental Model: Rust Backend + System Webview + IPC Commands

Tauri's distinctive paradigm is **a Rust process hosting a system webview, communicating via serialized command invocations.** Four things differentiate Tauri from Electron:

### 1. Rust backend (no Node.js, no bundled Chromium)

```rust
// src-tauri/src/main.rs
#![cfg_attr(not(debug_assertions), windows_subsystem = "windows")] // Hide console on Windows release

fn main() {
    myapp_lib::run();
}
```

```rust
// src-tauri/src/lib.rs
use tauri::Manager;

#[cfg_attr(mobile, tauri::mobile_entry_point)]
pub fn run() {
    tauri::Builder::default()
        .plugin(tauri_plugin_fs::init())              // Register plugins
        .plugin(tauri_plugin_dialog::init())
        .plugin(tauri_plugin_notification::init())
        .plugin(tauri_plugin_shell::init())
        .plugin(tauri_plugin_clipboard_manager::init())
        .manage(AppState::default())                   // Register app state
        .invoke_handler(tauri::generate_handler![
            commands::greet,
            commands::get_user,
            commands::save_file,
            commands::read_config,
        ])
        .setup(|app| {
            // Runs once at app startup
            #[cfg(debug_assertions)]
            app.get_webview_window("main").unwrap().open_devtools();

            Ok(())
        })
        .run(tauri::generate_context!())               // Generates context from tauri.conf.json
        .expect("error while running tauri application");
}
```

The Rust process is the **host** — it owns the window, manages native APIs, and serves the webview. There's no Node.js runtime, no bundled Chromium. The binary is just Rust + the system webview library.

### 2. Tauri commands (the IPC mechanism)

Tauri commands are Rust functions callable from the frontend via `invoke()`. They're the primary way the frontend talks to native code.

```rust
// src-tauri/src/commands.rs
use serde::{Deserialize, Serialize};
use tauri::State;

#[derive(Debug, Serialize, Deserialize)]
pub struct User {
    pub id: u64,
    pub name: String,
    pub email: String,
}

// Simple command — takes serializable args, returns serializable result
#[tauri::command]
pub fn greet(name: &str) -> String {
    format!("Hello, {}!", name)
}

// Async command — returns a Future
#[tauri::command]
pub async fn get_user(id: u64, state: State<'_, AppState>) -> Result<User, String> {
    state.db.lock().unwrap()
        .get(id)
        .cloned()
        .ok_or_else(|| format!("User {} not found", id))
}

// Command with file I/O (uses tauri-plugin-fs)
#[tauri::command]
pub async fn save_file(path: String, content: String) -> Result<(), String> {
    std::fs::write(&path, content).map_err(|e| e.to_string())
}

// Command that emits an event to the frontend
#[tauri::command]
pub async fn process_large_file(
    path: String,
    app: tauri::AppHandle,
) -> Result<(), String> {
    for progress in 0..=100 {
        // ... process chunk ...
        app.emit("progress", progress).map_err(|e| e.to_string())?;
        tokio::time::sleep(std::time::Duration::from_millis(50)).await;
    }
    Ok(())
}
```

```typescript
// Frontend — call the commands
import { invoke } from '@tauri-apps/api/core';
import { listen } from '@tauri-apps/api/event';

// Sync-ish call (Rust async, but JS awaits)
const greeting = await invoke<string>('greet', { name: 'Alice' });
// greeting === "Hello, Alice!"

const user = await invoke<User>('get_user', { id: 42 });
// user is typed via the Rust return type

await invoke('save_file', { path: '/path/to/file', content: 'Hello' });

// Listen for events from Rust
const unlisten = await listen<number>('progress', (event) => {
  console.log(`Progress: ${event.payload}%`);
});

await invoke('process_large_file', { path: '/path/to/large/file' });
unlisten();
```

The `invoke()` call is type-safe if you use the `tauri-specta` or `specta` crate for TypeScript bindings generation. Without it, you manually type the return.

### 3. System webview (no bundled Chromium)

| Platform | Webview engine | Bundled? |
|---|---|---|
| Windows | WebView2 (Edge/Chromium) | No — preinstalled on Windows 11, downloadable on 10 |
| macOS | WKWebView (Safari/WebKit) | No — ships with macOS |
| Linux | GTK WebKit (WebKitGTK) | No — installed via system package manager |
| iOS | WKWebView | No — ships with iOS |
| Android | Android System WebView | No — ships with Android |

Because the webview is **system-provided**, Tauri binaries are tiny. A minimal Tauri app is ~3 MB; a typical app with a React frontend is ~5-10 MB. The same app with Electron would be 80-150 MB (because Electron bundles the full Chromium + Node.js).

**Trade-off:** you're at the mercy of the system webview. Edge WebView2 and WKWebView are modern and well-maintained. WebKitGTK on Linux can lag (older distributions may have older WebKit). Test on all target platforms.

### 4. Capability-based permissions (Tauri 2 security model)

Tauri 2 replaced Tauri 1's allowlist with a **Capability-based** system. Each window/webview declares which commands and plugins it can access.

```jsonc
// src-tauri/capabilities/default.json
{
  "$schema": "../gen/schemas/desktop-schema.json",
  "identifier": "default",
  "description": "Capability for the main window",
  "windows": ["main"],
  "permissions": [
    "core:default",                          // Default core permissions
    "fs:allow-read-text-file",               // Specific fs permission
    "fs:allow-write-text-file",
    "dialog:allow-open",                     // File open dialog
    "dialog:allow-save",
    "notification:default",
    "shell:allow-open",                      // Open URLs in default browser
    "clipboard-manager:allow-read-text",
    "clipboard-manager:allow-write-text"
  ]
}
```

Each plugin exposes a set of permissions. You grant only what's needed — the frontend can't call a command or use a plugin API you didn't grant. This is principle-of-least-privilege at the framework level.

---

## Frontend: Tauri is frontend-agnostic

Tauri doesn't care what frontend framework you use. The webview loads your built frontend (HTML/CSS/JS) — whatever produces that.

### Common frontend setups

| Frontend | Use |
|---|---|
| **React + Vite** | Most popular, best DX |
| **Vue + Vite** | If team is Vue-fluent |
| **Svelte/SvelteKit + Vite** | If you want the smallest bundle |
| **Solid + Vite** | If you want signals-based reactivity |
| **Vanilla JS/TS** | Minimal, no framework |
| **Lit (web components)** | For design system / component library apps |
| **Yew (Rust → WebAssembly)** | Pure Rust frontend + backend |

### Frontend setup pattern (Vite + React example)

```typescript
// src/App.tsx
import { useState, useEffect } from 'react';
import { invoke } from '@tauri-apps/api/core';
import { open, save } from '@tauri-apps/plugin-dialog';
import { writeTextFile, readTextFile } from '@tauri-apps/plugin-fs';
import { listen } from '@tauri-apps/api/event';

function App() {
  const [greeting, setGreeting] = useState('');
  const [progress, setProgress] = useState(0);

  useEffect(() => {
    const unlisten = listen<number>('progress', (e) => setProgress(e.payload));
    return () => { unlisten.then(fn => fn()); };
  }, []);

  const handleGreet = async () => {
    const result = await invoke<string>('greet', { name: 'Alice' });
    setGreeting(result);
  };

  const handleOpen = async () => {
    const filePath = await open({
      filters: [{ name: 'Text', extensions: ['txt', 'md'] }],
    });
    if (filePath) {
      const content = await readTextFile(filePath as string);
      console.log(content);
    }
  };

  const handleSave = async () => {
    const filePath = await save({ defaultPath: 'untitled.txt' });
    if (filePath) {
      await writeTextFile(filePath, 'Hello, Tauri!');
    }
  };

  return (
    <div>
      <button onClick={handleGreet}>Greet</button>
      <p>{greeting}</p>
      <button onClick={handleOpen}>Open File</button>
      <button onClick={handleSave}>Save File</button>
      <progress value={progress} max="100" />
    </div>
  );
}

export default App;
```

The frontend uses the `@tauri-apps/api` and `@tauri-apps/plugin-*` packages to call into Rust. Everything else is standard web dev.

---

## Plugin System

Tauri 2 has a rich plugin ecosystem. Official plugins are maintained by the Tauri team.

### Common official plugins

| Plugin | Package | Use |
|---|---|---|
| Filesystem | `tauri-plugin-fs` | Read/write files |
| Dialog | `tauri-plugin-dialog` | Native file open/save/message dialogs |
| Notification | `tauri-plugin-notification` | OS notifications |
| Clipboard | `tauri-plugin-clipboard-manager` | Read/write system clipboard |
| HTTP | `tauri-plugin-http` | HTTP client (bypasses CORS — runs in Rust) |
| Shell | `tauri-plugin-shell` | Run external commands, open URLs/files |
| OS | `tauri-plugin-os` | OS info (platform, version, hostname) |
| Process | `tauri-plugin-process` | Exit/restart the app |
| Updater | `tauri-plugin-updater` | Auto-update with signature verification |
| Global Shortcut | `tauri-plugin-global-shortcut` | Register keyboard shortcuts |
| Tray Icon | `tauri-plugin-tray` | System tray icon + menu |
| Deep Link | `tauri-plugin-deep-link` | Custom URL scheme (`myapp://`) |
| Log | `tauri-plugin-log` | Structured logging |
| Store | `tauri-plugin-store` | Persistent key-value store |
| SQL | `tauri-plugin-sql` | SQLite/MySQL/PostgreSQL |
| HTTP Request | `tauri-plugin-http` | HTTP client from Rust |
| Window State | `tauri-plugin-window-state` | Remember window size/position |

### Mobile plugins (Tauri 2)

| Plugin | Use |
|---|---|
| `tauri-plugin-camera` | Camera access |
| `tauri-plugin-geolocation` | GPS |
| `tauri-plugin-biometric` | TouchID/FaceID/fingerprint |
| `tauri-plugin-haptics` | Vibration |
| `tauri-plugin-nfc` | NFC reading |
| `tauri-plugin-barcode-scanner` | Barcode/QR scanning |

### Adding a plugin

```bash
# Add via CLI (installs both npm + cargo packages, updates tauri.conf.json)
npm run tauri add fs
npm run tauri add dialog
npm run tauri add updater
```

```rust
// Register in Rust (src-tauri/src/lib.rs)
pub fn run() {
    tauri::Builder::default()
        .plugin(tauri_plugin_fs::init())
        .plugin(tauri_plugin_dialog::init())
        .plugin(tauri_plugin_updater::Builder::new().build())
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
```

```jsonc
// Grant permission in capabilities/default.json
{
  "permissions": [
    "fs:allow-read-text-file",
    "fs:allow-write-text-file",
    "dialog:allow-open",
    "dialog:allow-save",
    "updater:default"
  ]
}
```

```typescript
// Use from frontend
import { readTextFile, writeTextFile } from '@tauri-apps/plugin-fs';
import { open, save } from '@tauri-apps/plugin-dialog';
import { check } from '@tauri-apps/plugin-updater';

const content = await readTextFile('/path/to/file');
await writeTextFile('/path/to/file', 'new content');

const filePath = await open({ filters: [{ name: 'Text', extensions: ['txt'] }] });

const update = await check();
if (update) {
  await update.downloadAndInstall();
  await relaunch();
}
```

---

## Mobile Support (Tauri 2 — iOS + Android)

Tauri 2 added mobile support — the same Rust core + web frontend can target iOS and Android.

```bash
# Initialize mobile projects (one-time)
npm run tauri android init
npm run tauri ios init        # macOS only (requires Xcode)

# Dev on mobile
npm run tauri android dev     # Run on Android emulator/device
npm run tauri ios dev         # Run on iOS simulator

# Build for stores
npm run tauri android build   # Outputs .apk / .aab
npm run tauri ios build       # Outputs .ipa (requires Apple Developer account)
```

### Mobile-specific considerations

1. **Permissions** differ per platform. Android requires `AndroidManifest.xml` entries; iOS requires `Info.plist` entries. The mobile plugins handle this automatically when you `tauri add` them.

2. **The webview is the system webview** — Android System WebView (Chrome-based) or iOS WKWebView (Safari-based). Both are modern and well-maintained.

3. **Native UI** — Tauri doesn't provide native widgets. Your UI is HTML/CSS. For native-feeling UI, use a CSS framework that mimics native (e.g., `@ionic/react` for iOS/Android-style components).

4. **App Store / Play Store** review processes apply. Tauri apps are distributed like any other native app.

5. **Code sharing** — your Rust core + frontend are 95%+ shared between desktop and mobile. Only platform-specific code (e.g., mobile-only plugins like biometric) needs conditional compilation:

```rust
#[cfg(mobile)]
use tauri_plugin_biometric;

#[cfg(desktop)]
fn setup_desktop_only() { /* ... */ }
```

---

## App State Management

Tauri manages app state via the `State` extractor — thread-safe containers accessible from any command.

```rust
// src-tauri/src/state.rs
use std::sync::Mutex;
use std::collections::HashMap;

#[derive(Default)]
pub struct AppState {
    pub db: Mutex<HashMap<u64, User>>,
    pub current_user: Mutex<Option<User>>,
    pub settings: Mutex<Settings>,
}

#[derive(serde::Serialize, serde::Deserialize, Clone)]
pub struct User {
    pub id: u64,
    pub name: String,
}

#[derive(serde::Serialize, serde::Deserialize, Clone, Default)]
pub struct Settings {
    pub theme: String,
    pub auto_save: bool,
}
```

```rust
// Register in lib.rs
.manage(AppState::default())

// Use in commands
#[tauri::command]
pub async fn login(
    email: String,
    password: String,
    state: State<'_, AppState>,
) -> Result<User, String> {
    // ... validate ...
    let user = User { id: 1, name: "Alice".into() };
    *state.current_user.lock().unwrap() = Some(user.clone());
    Ok(user)
}

#[tauri::command]
pub fn get_current_user(state: State<'_, AppState>) -> Option<User> {
    state.current_user.lock().unwrap().clone()
}
```

Use `Mutex<T>` for interior mutability. Tauri's `State` is an `Arc` under the hood — multiple commands can access it concurrently, but `Mutex` ensures safe mutation.

---

## Auto-Updater

Tauri 2 has a built-in auto-updater with signature verification.

```jsonc
// tauri.conf.json — configure updater
{
  "plugins": {
    "updater": {
      "active": true,
      "endpoints": [
        "https://releases.example.com/myapp/{{target}}/{{current_version}}"
      ],
      "pubkey": "BASE64_PUBLIC_KEY"
    }
  }
}
```

```bash
# Generate a signing key pair (one-time)
npm run tauri signer generate -w ~/.tauri/myapp.key
# Saves: myapp.key (private) + myapp.key.pub (public — put in tauri.conf.json)
```

```rust
// src-tauri/src/lib.rs — register the updater plugin
.plugin(tauri_plugin_updater::Builder::new().build())
```

```typescript
// Frontend — check for updates
import { check } from '@tauri-apps/plugin-updater';
import { relaunch } from '@tauri-apps/plugin-process';

const update = await check();
if (update?.available) {
  const confirmed = confirm(`Update to ${update.version}?\n\n${update.body}`);
  if (confirmed) {
    await update.downloadAndInstall();
    await relaunch();
  }
}
```

The updater fetches a JSON manifest from your endpoint, verifies the signature with your public key, downloads the new bundle, and replaces the running app. The signature verification prevents MITM attacks.

---

## Testing

### Rust unit tests (standard `cargo test`)

```rust
// src-tauri/src/commands.rs
#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_greet() {
        assert_eq!(greet("Alice"), "Hello, Alice!");
    }

    #[tokio::test]
    async fn test_get_user_not_found() {
        let state = AppState::default();
        let result = get_user(999, tauri::State::from(&state)).await;
        assert!(result.is_err());
    }
}
```

```bash
cd src-tauri && cargo test
```

### Frontend tests (standard web testing)

Use whatever your frontend framework provides (Vitest + Testing Library for React, etc.). Mock `invoke()` to avoid calling Rust:

```typescript
// src/__tests__/App.test.tsx
import { render, screen } from '@testing-library/react';
import { invoke } from '@tauri-apps/api/core';
import App from './App';

vi.mock('@tauri-apps/api/core', () => ({
  invoke: vi.fn(),
}));

test('displays greeting after click', async () => {
  (invoke as any).mockResolvedValue('Hello, Alice!');
  render(<App />);
  await userEvent.click(screen.getByText('Greet'));
  expect(screen.getByText('Hello, Alice!')).toBeInTheDocument();
});
```

### E2E tests with WebDriver (tauri-driver)

Tauri ships `tauri-driver` — a WebDriver implementation for Tauri apps:

```bash
# Install
npm install -D @tauri-apps/driver

# Run (uses WebDriverIO or Selenium)
npx tauri-driver
```

```typescript
// tests/e2e.spec.ts (using WebDriverIO)
import { remote } from 'webdriverio';

test('app loads', async () => {
  const client = await remote({
    capabilities: {
      'tauri:options': {
        binary: '/path/to/myapp',
      },
    },
  });

  const title = await client.getTitle();
  expect(title).toBe('MyApp');

  await client.deleteSession();
});
```

Cross-reference: `testing-patterns` for general test pyramid / mocking strategies.

---

## Deployment

### Build for production

```bash
npm run tauri build
# Outputs to src-tauri/target/release/bundle/:
#   - macOS: .app, .dmg
#   - Windows: .exe, .msi
#   - Linux: .deb, .rpm, .AppImage
```

### Code signing (required for distribution)

| Platform | Tool | Notes |
|---|---|---|
| macOS | `codesign` + `xcrun notarytool` | Apple Developer ID required for distribution outside App Store |
| Windows | `signtool` (Windows SDK) | EV code signing certificate recommended (avoids SmartScreen warnings) |
| Linux | None (optional) | GPG signing for repositories |

### CI/CD (GitHub Actions)

Tauri provides an official GitHub Action for cross-platform builds:

```yaml
# .github/workflows/release.yml
name: Release
on:
  push:
    tags: ['v*']

jobs:
  build:
    strategy:
      matrix:
        include:
          - platform: macos-latest
            args: '--target aarch64-apple-darwin'
          - platform: macos-latest
            args: '--target x86_64-apple-darwin'
          - platform: ubuntu-22.04
            args: ''
          - platform: windows-latest
            args: ''

    runs-on: ${{ matrix.platform }}
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with: { node-version: 20 }
      - uses: dtolnay/rust-toolchain@stable
        with:
          targets: ${{ matrix.platform == 'macos-latest' && 'aarch64-apple-darwin,x86_64-apple-darwin' || '' }}
      - name: Install Linux deps
        if: matrix.platform == 'ubuntu-22.04'
        run: |
          sudo apt-get update
          sudo apt-get install -y libwebkit2gtk-4.1-dev libappindicator3-dev librsvg2-dev patchelf
      - run: npm install
      - uses: tauri-apps/tauri-action@v0
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
          # macOS signing
          APPLE_CERTIFICATE: ${{ secrets.APPLE_CERTIFICATE }}
          APPLE_CERTIFICATE_PASSWORD: ${{ secrets.APPLE_CERTIFICATE_PASSWORD }}
          APPLE_SIGNING_IDENTITY: ${{ secrets.APPLE_SIGNING_IDENTITY }}
          APPLE_ID: ${{ secrets.APPLE_ID }}
          APPLE_PASSWORD: ${{ secrets.APPLE_PASSWORD }}
          APPLE_TEAM_ID: ${{ secrets.APPLE_TEAM_ID }}
          # Updater signing
          TAURI_SIGNING_PRIVATE_KEY: ${{ secrets.TAURI_SIGNING_PRIVATE_KEY }}
        with:
          tagName: ${{ github.ref_name }}
          releaseName: 'MyApp ${{ github.ref_name }}'
          releaseDraft: true
          prerelease: false
          args: ${{ matrix.args }}
```

This builds for macOS (ARM + Intel), Linux, and Windows in parallel, signs the bundles, and uploads them to a GitHub Release.

---

## Top 10 Anti-Patterns (the most valuable section)

1. **Calling Node.js APIs from the frontend.** Tauri has no Node.js. The frontend runs in a webview — it only has browser APIs. If you need filesystem, OS, or native access, use Tauri commands (`invoke()`) or plugins (`@tauri-apps/plugin-*`). Don't `import 'fs'` — that's Electron thinking.

2. **Not using the Capability/permission system.** Tauri 2's security model requires you to explicitly grant each window access to commands and plugins. Skipping this ("just grant everything") defeats the security model. Grant only what each window needs — the principle of least privilege.

3. **Long-running commands blocking the UI.** Tauri commands run on a thread pool, but the frontend's `invoke()` is async — if the Rust function blocks for a long time, the frontend's `await` hangs. For long work, emit progress events via `app.emit()` and return early, or use a background task with a notification when done.

4. **Using `Mutex` incorrectly in app state.** `State<'_, T>` gives you a reference to the state. If `T` contains a `Mutex`, you must lock it to mutate. Forgetting the lock causes compile errors (good). Holding the lock across `.await` points (bad — can deadlock) requires `tokio::sync::Mutex` instead of `std::sync::Mutex`. Use `std::sync::Mutex` for sync code, `tokio::sync::Mutex` for async.

5. **Not testing on the target webview.** The system webview differs per platform. Edge WebView2 (Windows) and WKWebView (macOS) are modern. WebKitGTK (Linux) can lag — older distributions have older WebKit. Test on all target platforms. Use `browserslist` config to stay within webview-supported features.

6. **Bundling a full web server in the frontend.** Tauri's frontend is static HTML/CSS/JS — it's loaded from the local filesystem, not served. Don't bundle Express/Fastify/Next.js server mode — it won't work (no Node.js). Use a static build (`vite build`, `next export`, etc.).

7. **Hardcoding file paths.** Use `tauri::api::path` (Rust) or `@tauri-apps/api/path` (JS) to resolve platform-appropriate paths (app data dir, config dir, document dir). Hardcoded `/home/user/...` or `C:\Users\...` breaks cross-platform.

8. **Not signing macOS/Windows builds.** Unsigned macOS apps show a scary "unidentified developer" warning. Unsigned Windows apps trigger SmartScreen. Both destroy user trust. Get an Apple Developer ID ($99/year) and a Windows EV code signing certificate (~$300/year) and configure signing in CI.

9. **Ignoring the updater's signature requirement.** The updater requires a signing key pair. If you don't set `TAURI_SIGNING_PRIVATE_KEY` in CI, the updater manifest won't be signed, and clients will reject the update. Set up the key pair on day one and store the private key as a CI secret.

10. **Treating Tauri like Electron.** Tauri is Rust + system webview + IPC commands. Electron is Node.js + bundled Chromium + main/renderer process. The mental models are different. Don't reach for Electron patterns (IPC via `ipcMain`/`ipcRenderer`, `require()` in the renderer, `electron-builder` configs). Learn the Tauri way: `#[tauri::command]` + `invoke()`, `@tauri-apps/api/*`, `tauri.conf.json` + `capabilities/`.

---

## Cross-references

- `framework-templates` — CLAUDE.md generation template for Tauri (project onboarding)
- `flutter` — Dart cross-platform mobile + desktop (different language, different rendering model — Flutter draws its own UI; Tauri uses the system webview)
- `react-native-expo` — React Native + Expo mobile (different focus — RN is mobile-only; Tauri is desktop + mobile)
- `rust-web` — Rust web backend patterns (relevant for the Rust core: ownership, async, error handling)
- `frontend-ui-engineering` — Production-quality UI build patterns (relevant for the web frontend)
- `api-and-interface-design` — Type contract design (relevant for Tauri command signatures)
- `security-and-hardening` — OWASP-aware hardening (Tauri's Capability system is the desktop equivalent)
- `clean-code` — General coding standards applicable to Rust + TypeScript
- `testing-patterns` — Test pyramid, mocking strategies
- `code-review-checklist` — 12-category code review checklist
- `git-workflow-and-versioning` — Branching/commit conventions for Tauri projects

---

## Dependencies

Required:
- **Rust** 1.77+ (with `cargo`)
- **Node.js** 20+ (for frontend tooling)
- **Tauri CLI** 2.0+ (`npm install -D @tauri-apps/cli` or `cargo install tauri-cli`)
- **Tauri framework** 2.0+ (`cargo add tauri` in `src-tauri/`)

### Platform-specific system dependencies

| Platform | Dependencies |
|---|---|
| **macOS** | Xcode Command Line Tools (`xcode-select --install`) |
| **Windows** | Microsoft C++ Build Tools, WebView2 (preinstalled on Windows 11) |
| **Linux** | `webkit2gtk-4.1`, `libgtk-3-dev`, `libappindicator3-dev`, `librsvg2-dev`, `patchelf` |
| **iOS** (mobile) | Xcode 15+, iOS 13+ SDK |
| **Android** (mobile) | Android Studio, Android SDK 24+ |

### Common official plugins (install via `npm run tauri add <name>`)

- `tauri-plugin-fs` — Filesystem access
- `tauri-plugin-dialog` — Native file/message dialogs
- `tauri-plugin-notification` — OS notifications
- `tauri-plugin-clipboard-manager` — System clipboard
- `tauri-plugin-http` — HTTP client (bypasses CORS)
- `tauri-plugin-shell` — Run external commands, open URLs
- `tauri-plugin-os` — OS info
- `tauri-plugin-process` — Exit/restart app
- `tauri-plugin-updater` — Auto-update with signature verification
- `tauri-plugin-global-shortcut` — System-wide keyboard shortcuts
- `tauri-plugin-tray` — System tray icon + menu
- `tauri-plugin-deep-link` — Custom URL scheme
- `tauri-plugin-log` — Structured logging
- `tauri-plugin-store` — Persistent key-value store
- `tauri-plugin-sql` — SQLite/MySQL/PostgreSQL
- `tauri-plugin-window-state` — Remember window size/position
- `tauri-plugin-http` — HTTP client from Rust

### Mobile plugins (Tauri 2)

- `tauri-plugin-camera` — Camera access
- `tauri-plugin-geolocation` — GPS
- `tauri-plugin-biometric` — TouchID/FaceID/fingerprint
- `tauri-plugin-haptics` — Vibration
- `tauri-plugin-nfc` — NFC reading
- `tauri-plugin-barcode-scanner` — Barcode/QR scanning

### Frontend packages (npm)

- `@tauri-apps/api` — Core Tauri JS API (`invoke`, `event`, `window`, etc.)
- `@tauri-apps/cli` — Tauri CLI (dev, build, mobile commands)
- `@tauri-apps/plugin-*` — Frontend bindings for each plugin (e.g., `@tauri-apps/plugin-fs`, `@tauri-apps/plugin-dialog`)
