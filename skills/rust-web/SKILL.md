---
name: rust-web
description: "Rust (1.80+) web backend workflow skill with Axum + Tokio + sqlx. Covers the ownership/borrow checker mental model (the #1 stumbling block for newcomers — borrow rules, lifetimes, `&` vs `&mut` vs owned), async/await with the Tokio runtime, the Axum web framework (Tower-based middleware, extractors for type-safe request parsing, IntoResponse for responses), sqlx for compile-time-checked SQL (macros verify queries against your DB at build time — catches SQL errors before runtime), serde for JSON serialization, the Result<T, E> error model (no exceptions — like Go but with the `?` operator), traits (Rust's interfaces — explicit, with associated types), the module system (mod.rs vs file-based modules), Cargo (the universal build tool + package manager), feature flags for conditional compilation, and the deployment story (single static binary like Go, plus musl for fully-static linking). Use when building any HTTP API, microservice, CLI with HTTP features, or backend service in Rust — especially when the task involves fighting the borrow checker, designing async handlers, choosing between Axum/Actix-web/poem, or wiring sqlx with compile-time checking where idiomatic Rust differs from Go/Node.js/Python patterns."
license: Proprietary. LICENSE.txt has complete terms
---

# Rust Web — Backend Workflow Skill (Axum + Tokio + sqlx)

> **Target:** Rust 1.80+ (released July 2024) with the **Axum 0.7+** web framework, **Tokio 1.x** async runtime, and **sqlx 0.8+** for database access. This skill is Axum-first: Axum is the most popular Rust web framework for new projects (built by the Tokio team, plays nicely with the Tower ecosystem). Actix-web is the older alternative — covered briefly for comparison.

## When to Use This Skill

Use this skill whenever the user is building, debugging, or extending a Rust web backend. Trigger phrases include "Rust", "Cargo", "axum", "tokio", "sqlx", "serde", "async/await", "borrow checker", "lifetime", "trait", "impl", "Result", "Option", "Arc", "Mutex", "RwLock", "Box<dyn Trait>", "Pin", "Send + Sync", and any reference to a `Cargo.toml` file, `src/main.rs` entry point, or `#[tokio::main]` attribute.

Do **not** use this skill for:
- **Rust ≤1.75** — some patterns here (async closures, return-position impl Trait in traits) require newer Rust.
- **Actix-web projects** — the framework-specific sections assume Axum. The ownership, async, and sqlx sections still apply.
- **Desktop/GUI Rust** (Tauri, egui, iced) — different domain. See Tauri docs.
- **Embedded/no-std Rust** — different constraints (no allocator, no Tokio).
- **Other backend languages** (Go, Node.js, Python, Ruby, Java) — see `go-web`, `laravel-12`, `rails-8`, `django-6`, `spring-boot-3` skills.

## Quick Start

```bash
# Install Rust via rustup (the canonical installer)
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
source $HOME/.cargo/env

# Create a new binary project
cargo new myapp --bin
cd myapp

# Add dependencies
cargo add axum --features "macros"
cargo add tokio --features "full"
cargo add serde --features "derive"
cargo add serde_json
cargo add tracing
cargo add tracing-subscriber

# Create src/main.rs
cat > src/main.rs << 'EOF'
use axum::{routing::get, Router, extract::Path, Json};
use serde::Serialize;

#[derive(Serialize)]
struct User { id: String, name: String }

async fn hello() -> &'static str {
    "Hello, World!"
}

async fn get_user(Path(id): Path<String>) -> Json<User> {
    Json(User { id, name: "Alice".into() })
}

#[tokio::main]
async fn main() {
    tracing_subscriber::fmt::init();

    let app = Router::new()
        .route("/", get(hello))
        .route("/users/:id", get(get_user));

    let listener = tokio::net::TcpListener::bind("0.0.0.0:8080").await.unwrap();
    tracing::info!("Listening on {}", listener.local_addr().unwrap());
    axum::serve(listener, app).await.unwrap();
}
EOF

cargo run                  # Build + run (dev mode)
# Visit http://localhost:8080 and http://localhost:8080/users/42

# Build for release (optimized)
cargo build --release
./target/release/myapp
```

### Key commands

```bash
cargo new <name> --bin        # New binary project (CLI/app)
cargo new <name> --lib        # New library project
cargo build                   # Debug build (fast compile, slow runtime)
cargo build --release         # Release build (slow compile, fast runtime)
cargo run                     # Build + run
cargo test                    # Run all tests
cargo test <test_name>        # Run a specific test
cargo test -- --nocapture     # Show println! output during tests
cargo check                   # Type-check without generating code (fastest feedback)
cargo clippy                  # Lints (ALWAYS run — catches real bugs)
cargo fmt                     # Format all files
cargo fmt -- --check          # Verify formatting (CI mode)
cargo add <crate>             # Add a dependency
cargo update                  # Update Cargo.lock within semver
cargo upgrade <crate>         # Bump to latest (requires cargo-edit or cargo upgrade)
cargo doc --open              # Generate + open docs for your crate and deps
cargo bench                   # Run benchmarks (requires nightly for some features)
cargo tree                    # Show dependency tree
cargo audit                   # Check for known vulnerabilities (install separately)
```

---

## Project Structure (Cargo canonical layout)

Cargo enforces a minimal but strict layout:

```
myapp/
├── Cargo.toml                 # ← THE config file (deps, metadata, features)
├── Cargo.lock                 # Locked dependency versions (commit this for bins, not for libs)
├── src/
│   ├── main.rs                # Binary entry point (fn main())
│   ├── lib.rs                 # Library root (if you have both bin + lib)
│   ├── bin/                   # Additional binaries (cargo run --bin <name>)
│   │   └── cli.rs
│   ├── api/                   # Your modules (one dir per logical area)
│   │   ├── mod.rs             # Module declaration (or use api.rs instead)
│   │   ├── handlers.rs        # HTTP handlers
│   │   ├── models.rs          # Domain types
│   │   └── error.rs           # Error types
│   ├── db/
│   │   ├── mod.rs
│   │   └── users.rs
│   └── config.rs
├── migrations/                # SQL migrations (if using sqlx)
│   ├── 20250115000000_create_users.sql
│   └── 20250116000000_add_posts.sql
├── tests/                     # Integration tests (test the public API of your crate)
│   ├── api_test.rs
│   └── common/mod.rs
├── benches/                   # Benchmarks (use criterion)
│   └── parsing.rs
├── examples/                  # Example binaries (cargo run --example <name>)
│   └── basic_server.rs
├── build.rs                   # Build script (runs before compilation)
├── .cargo/config.toml         # Cargo config (target-specific, env vars)
├── .env                       # Environment variables (DATABASE_URL for sqlx)
├── Dockerfile
└── README.md
```

### Module system: `mod.rs` vs file-based

Rust 2018+ supports both module styles. The modern preference is **file-based** (no `mod.rs`):

```
# Old style (still works, common in existing code)
src/api/mod.rs        # declares: pub mod handlers; pub mod models;
src/api/handlers.rs
src/api/models.rs

# New style (preferred for new projects)
src/api.rs            # declares: pub mod handlers; pub mod models;
src/api/handlers.rs
src/api/models.rs
```

Both are equivalent. Pick one and be consistent. The `mod` declaration in the parent file is mandatory in both styles — Rust does NOT auto-discover modules.

### `Cargo.toml` structure

```toml
[package]
name = "myapp"
version = "0.1.0"
edition = "2021"        # Rust edition (2021 is current; 2024 coming)
authors = ["You <you@example.com>"]
description = "A web backend"

[dependencies]
axum = { version = "0.7", features = ["macros"] }
tokio = { version = "1", features = ["full"] }
serde = { version = "1", features = ["derive"] }
serde_json = "1"
sqlx = { version = "0.8", features = ["runtime-tokio", "postgres", "uuid", "chrono"] }
uuid = { version = "1", features = ["v4", "serde"] }
chrono = { version = "0.4", features = ["serde"] }
tracing = "0.1"
tracing-subscriber = { version = "0.3", features = ["env-filter"] }
thiserror = "1"         # Ergonomic error enums
anyhow = "1"            # Dynamic error boxing (for apps, not libs)

[dev-dependencies]
tower = { version = "0.5", features = ["util"] }   # For testing handlers
http-body-util = "0.1"
mime = "0.3"

[profile.release]
opt-level = 3
lto = true              # Link-time optimization (smaller, faster binary)
codegen-units = 1       # Slower compile, faster runtime
strip = true            # Strip debug symbols from binary

[features]
default = []
# Feature flags for conditional compilation
graphql = ["dep:async-graphql"]
```

---

## Core Mental Model: Ownership + Async + Traits + Zero-Cost Abstractions

Rust's distinctive paradigm is **memory safety without a garbage collector, via ownership and borrowing.** Four things differentiate Rust from Go/Node.js/Python:

### 1. Ownership and borrowing (the borrow checker)

Every value has exactly ONE owner. When the owner goes out of scope, the value is dropped. You can lend references (`&`) or mutable references (`&mut`), but with strict rules:

```rust
// Owned — moved (transfer of ownership)
let s1 = String::from("hello");
let s2 = s1;                  // s1 is moved — s1 is no longer usable
// println!("{}", s1);        // ❌ error: value borrowed after move
println!("{}", s2);           // ✅ OK

// Immutable borrow (&T) — many readers OK
let s = String::from("hello");
let r1 = &s;                  // Immutable borrow
let r2 = &s;                  // Another immutable borrow — OK
println!("{} {}", r1, r2);

// Mutable borrow (&mut T) — exclusive access
let mut s = String::from("hello");
let r = &mut s;               // Mutable borrow — s is now locked
r.push_str(" world");
// let r2 = &s;               // ❌ error: cannot borrow `s` as immutable while mutably borrowed
println!("{}", r);
```

**The borrow rules (memorize these):**
1. One mutable reference OR any number of immutable references (never both at once)
2. References must always point to valid data (no dangling pointers)
3. Mutable references must be exclusive

When you fight the borrow checker, the fix is usually one of:
- **Clone the data** (`s.clone()`) — explicit copy, avoids the borrow
- **Restructure scope** — release borrows before taking new ones
- **Use `Arc<Mutex<T>>`** for shared mutable state across threads
- **Return owned data** instead of references where possible
- **Use lifetimes** (`<'a>`) to express "this reference lives as long as that one"

### 2. Async/await with the Tokio runtime

Rust's async is **cooperative and zero-cost** — futures are state machines, not threads. The Tokio runtime is the de facto standard for async Rust.

```rust
#[tokio::main]                  // Initializes the Tokio runtime
async fn main() {
    // .await yields control to the runtime
    let result = fetch_data().await;
    println!("{:?}", result);
}

async fn fetch_data() -> Result<String, reqwest::Error> {
    let resp = reqwest::get("https://api.example.com/data").await?;
    resp.text().await
}

// Concurrent (parallel) execution
let (a, b, c) = tokio::join!(fetch_a(), fetch_b(), fetch_c());  // All at once

// Race — first to complete wins
let fastest = tokio::select! {
    r = fetch_a() => r,
    r = fetch_b() => r,
};
```

**Key difference from JavaScript/Python async:** Rust futures are **lazy** — they don't run until awaited. Calling `fetch_data()` without `.await` does nothing (you just get a future that hasn't started). This is the opposite of JS Promises which start eagerly.

**The `Send + Sync` boundary:** Tokio's multi-threaded scheduler requires futures to be `Send` (movable between threads). If you hit a "future is not Send" error, you're holding a non-Send type (like `Rc<T>` or `RefCell<T>`) across an `.await`. Fix: use `Arc<T>` and `Mutex<T>`/`RwLock<T>` instead.

### 3. Result<T, E> + the `?` operator (no exceptions)

Like Go, Rust has no exceptions. Unlike Go, the `?` operator makes error propagation ergonomic:

```rust
use thiserror::Error;

#[derive(Debug, Error)]
enum AppError {
    #[error("user not found: {0}")]
    NotFound(String),

    #[error("database error: {0}")]
    Database(#[from] sqlx::Error),

    #[error("unauthorized")]
    Unauthorized,
}

// The `?` operator returns early on Err, converting the error via `#[from]`
async fn get_user(pool: &PgPool, id: &str) -> Result<User, AppError> {
    let user: User = sqlx::query_as::<_, User>("SELECT id, name FROM users WHERE id = $1")
        .bind(id)
        .fetch_optional(pool)
        .await?               // ← converts sqlx::Error → AppError::Database
        .ok_or(AppError::NotFound(id.to_string()))?;
    Ok(user)
}

// Callers propagate with `?`
async fn handler(State(state): State<AppState>, Path(id): Path<String>) -> Result<Json<User>, AppError> {
    let user = get_user(&state.pool, &id).await?;
    Ok(Json(user))
}
```

**`thiserror`** is for library errors (derives `Error` + `Display`). **`anyhow`** is for application errors (boxes any error, less type-safe but more ergonomic). Use `thiserror` for public APIs, `anyhow` for top-level application code.

### 4. Traits (Rust's interfaces — explicit, with associated types)

```rust
// Define a trait (like an interface)
#[async_trait]               // Required for async methods (until stable Rust supports async traits natively)
trait UserStore: Send + Sync {
    async fn get(&self, id: &str) -> Result<Option<User>, AppError>;
    async fn create(&self, user: &User) -> Result<User, AppError>;
}

// Implement it for a concrete type
struct PgUserStore { pool: PgPool }

#[async_trait]
impl UserStore for PgUserStore {
    async fn get(&self, id: &str) -> Result<Option<User>, AppError> {
        // ... sqlx query
    }
    async fn create(&self, user: &User) -> Result<User, AppError> {
        // ... sqlx insert
    }
}

// Use it via generics (static dispatch) or trait objects (dynamic dispatch)
// Static dispatch (preferred — zero-cost, monomorphized at compile time)
async fn get_user<S: UserStore>(store: &S, id: &str) -> Result<Option<User>, AppError> {
    store.get(id).await
}

// Dynamic dispatch (when you need to mix types at runtime, e.g., a vec of different stores)
async fn use_store(store: &dyn UserStore, id: &str) -> Result<Option<User>, AppError> {
    store.get(id).await
}

// OR with Arc for shared ownership
async fn use_shared(store: Arc<dyn UserStore + Send + Sync>, id: &str) -> Result<Option<User>, AppError> {
    store.get(id).await
}
```

**Static vs dynamic dispatch:** generic `<S: UserStore>` is zero-cost (compiler generates a copy per type used). `&dyn UserStore` is dynamic (vtable indirection, ~1ns slower). Prefer generics unless you need runtime polymorphism (e.g., a vector of different store types).

---

## Axum: Handlers, Extractors, Responses

Axum is built on Tower (the Rust HTTP middleware ecosystem). Its key idea: **handlers are async functions, arguments are extractors, return values are responses.**

### Hello world

```rust
use axum::{routing::get, Router};

#[tokio::main]
async fn main() {
    let app = Router::new().route("/", get(handler));

    let listener = tokio::net::TcpListener::bind("0.0.0.0:8080").await.unwrap();
    axum::serve(listener, app).await.unwrap();
}

async fn handler() -> &'static str {
    "Hello, World!"
}
```

### Extractors (type-safe request parsing)

Extractors are types that implement `FromRequest`. They appear as handler arguments:

```rust
use axum::{
    extract::{Path, Query, State},
    Json,
};
use serde::Deserialize;

#[derive(Deserialize)]
struct Pagination { limit: Option<u32>, offset: Option<u32> }

// Multiple extractors — order matters (last arg is the body)
async fn list_users(
    State(state): State<AppState>,            // Shared state
    Query(pagination): Query<Pagination>,     // ?limit=10&offset=20
) -> Json<Vec<User>> {
    let users = state.store.list(pagination.limit.unwrap_or(20)).await;
    Json(users)
}

async fn get_user(
    State(state): State<AppState>,
    Path(id): Path<String>,                    // /users/:id
) -> Result<Json<User>, AppError> {
    let user = state.store.get(&id).await?
        .ok_or(AppError::NotFound(id))?;
    Ok(Json(user))
}

#[derive(Deserialize)]
struct CreateUser { name: String, email: String }

async fn create_user(
    State(state): State<AppState>,
    Json(input): Json<CreateUser>,             // Request body (must be last)
) -> Result<(StatusCode, Json<User>), AppError> {
    let user = state.store.create(&input).await?;
    Ok((StatusCode::CREATED, Json(user)))
}

// Routes
let app = Router::new()
    .route("/users", get(list_users).post(create_user))
    .route("/users/:id", get(get_user))
    .with_state(state);
```

**Extractor order rule:** the body extractor (`Json<T>`, `String`, `Bytes`) MUST be the last argument. Other extractors can be in any order.

### Responses (IntoResponse trait)

Anything implementing `IntoResponse` can be returned from a handler:

```rust
// &'static str → 200 OK with text/plain
async fn hello() -> &'static str { "Hello" }

// (StatusCode, &str) → custom status
async fn created() -> (StatusCode, &'static str) {
    (StatusCode::CREATED, "Created")
}

// Json<T> → 200 OK with application/json
async fn user() -> Json<User> { Json(User { /* ... */ }) }

// Result<T, E> → T's response on Ok, E's response on Err
async fn get() -> Result<Json<User>, AppError> { /* ... */ }

// Custom headers
use axum::response::IntoResponseParts;
use axum::http::header;
async fn with_headers() -> [(header::CONTENT_TYPE, "text/plain"), (header::CACHE_CONTROL, "no-cache")] {
    /* ... */
}

// Empty response
use axum::response::NoContent;
async fn delete() -> NoContent { NoContent }
```

### Implementing `IntoResponse` for your error type

```rust
use axum::{http::StatusCode, response::{IntoResponse, Response}, Json};

impl IntoResponse for AppError {
    fn into_response(self) -> Response {
        let (status, message) = match &self {
            AppError::NotFound(id) => (StatusCode::NOT_FOUND, format!("user not found: {}", id)),
            AppError::Database(e) => {
                tracing::error!(error = ?e, "database error");
                (StatusCode::INTERNAL_SERVER_ERROR, "internal error".to_string())
            }
            AppError::Unauthorized => (StatusCode::UNAUTHORIZED, "unauthorized".to_string()),
        };
        (status, Json(serde_json::json!({ "error": message }))).into_response()
    }
}
```

Now `Result<Json<T>, AppError>` works as a handler return type — errors automatically become proper HTTP responses.

---

## Middleware (Tower layers)

Axum middleware is Tower layers — composable, generic, framework-agnostic:

```rust
use axum::middleware::{self, Next};
use axum::extract::Request;
use tower_http::trace::TraceLayer;
use tower_http::cors::CorsLayer;
use tower_http::compression::CompressionLayer;

async fn auth_middleware(req: Request, next: Next) -> Result<Response, AppError> {
    let token = req.headers()
        .get("authorization")
        .and_then(|v| v.to_str().ok())
        .ok_or(AppError::Unauthorized)?;

    let user = validate_token(token).await?;

    // Insert user into request extensions for downstream handlers
    let mut req = req;
    req.extensions_mut().insert(user);

    Ok(next.run(req).await)
}

async fn logging_middleware(req: Request, next: Next) -> Response {
    let method = req.method().clone();
    let path = req.uri().path().to_string();
    let start = std::time::Instant::now();

    let response = next.run(req).await;

    tracing::info!(%method, %path, status = %response.status(), elapsed = ?start.elapsed());
    response
}

let app = Router::new()
    .route("/", get(handler))
    .route("/users/:id", get(get_user))
    .route_layer(middleware::from_fn(auth_middleware))   // Only these routes
    .layer(TraceLayer::new_for_http())                  // All routes
    .layer(CorsLayer::permissive())
    .layer(CompressionLayer::new())
    .layer(middleware::from_fn(logging_middleware));
```

The `tower-http` crate provides production-grade middleware: CORS, compression, tracing, timeouts, rate limiting, request ID, sensitive headers logging. Use these instead of hand-rolling.

### Shared state

```rust
use std::sync::Arc;

#[derive(Clone)]
struct AppState {
    pool: PgPool,
    store: Arc<dyn UserStore + Send + Sync>,
    config: Arc<Config>,
}

let state = AppState { /* ... */ };

let app = Router::new()
    .route("/", get(handler))
    .with_state(state);   // Must be the last call

// Extract via State extractor
async fn handler(State(state): State<AppState>) -> String {
    format!("Pool: {:?}", state.pool)
}
```

**State must be `Clone + Send + Sync`** (Axum wraps it in an `Arc` internally). Use `Arc<T>` for expensive-to-clone fields.

---

## Data Layer: sqlx with compile-time checking

sqlx is the canonical Rust SQL library. Its killer feature: **macros that verify your SQL against your database at compile time.** SQL errors are caught before runtime.

### Setup

```bash
cargo add sqlx --features "runtime-tokio postgres uuid chrono"
cargo add dotenvy       # For loading .env

# Install the sqlx-cli (for migrations + offline mode)
cargo install sqlx-cli --no-default-features --features postgres,rustls
```

```env
# .env
DATABASE_URL=postgres://user:pass@localhost:5432/myapp
```

### Migrations

```bash
sqlx migrate add create_users   # Creates migrations/<timestamp>_create_users.sql
```

```sql
-- migrations/20250115000000_create_users.sql
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email TEXT NOT NULL UNIQUE,
    name TEXT NOT NULL,
    password_hash TEXT NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
CREATE INDEX idx_users_email ON users(email);
```

```bash
sqlx migrate run               # Apply migrations
sqlx migrate revert            # Roll back the last one
```

### Compile-time-checked queries

```rust
use sqlx::postgres::PgPool;
use uuid::Uuid;
use chrono::{DateTime, Utc};

#[derive(sqlx::FromRow, serde::Serialize)]
struct User {
    id: Uuid,
    email: String,
    name: String,
    created_at: DateTime<Utc>,
}

async fn get_user(pool: &PgPool, id: Uuid) -> Result<Option<User>, sqlx::Error> {
    // query_as! macro — verified against your DB at compile time
    // If you typo a column name, change a type, or write invalid SQL, the BUILD FAILS
    let user = sqlx::query_as::<_, User>(
        "SELECT id, email, name, created_at FROM users WHERE id = $1"
    )
    .bind(id)
    .fetch_optional(pool)
    .await?;
    Ok(user)
}

async fn create_user(pool: &PgPool, email: &str, name: &str, password_hash: &str) -> Result<User, sqlx::Error> {
    sqlx::query_as::<_, User>(
        "INSERT INTO users (email, name, password_hash) VALUES ($1, $2, $3)
         RETURNING id, email, name, created_at"
    )
    .bind(email)
    .bind(name)
    .bind(password_hash)
    .fetch_one(pool)
    .await
}
```

**The compile-time check works by connecting to your `DATABASE_URL` database during `cargo build`.** If the DB is unreachable, the build fails. For CI/Docker, use **offline mode**:

```bash
cargo sqlx prepare              # Generates .sqlx/ directory with cached query data
# Commit the .sqlx/ directory to git
SQLX_OFFLINE=true cargo build   # Uses cached data — no DB connection needed
```

### Connection pooling

```rust
use sqlx::postgres::PgPoolOptions;

let pool = PgPoolOptions::new()
    .max_connections(20)
    .min_connections(5)
    .acquire_timeout(std::time::Duration::from_secs(3))
    .idle_timeout(Some(std::time::Duration::from_secs(600)))
    .connect(&database_url)
    .await?;
```

---

## Error Handling: thiserror + anyhow

### `thiserror` (for libraries, typed errors)

```rust
use thiserror::Error;

#[derive(Debug, Error)]
pub enum AppError {
    #[error("user not found: {0}")]
    NotFound(String),

    #[error("database error")]
    Database(#[from] sqlx::Error),

    #[error("unauthorized")]
    Unauthorized,

    #[error("bad request: {0}")]
    BadRequest(String),

    #[error("internal error")]
    Internal(#[from] anyhow::Error),
}
```

The `#[from]` attribute auto-implements `From<sqlx::Error> for AppError`, enabling the `?` operator.

### `anyhow` (for applications, dynamic errors)

```rust
use anyhow::{Result, Context};

fn read_config() -> Result<Config> {
    let content = std::fs::read_to_string("config.toml")
        .context("failed to read config.toml")?;  // Adds context to the error
    let config: Config = toml::from_str(&content)
        .context("failed to parse config.toml")?;
    Ok(config)
}
```

`anyhow::Error` is a boxed trait object — it can hold ANY error type. Use `context()` to add human-readable context. Less type-safe than `thiserror` but much more ergonomic for application code where you don't need to match on specific error variants.

---

## Testing

Rust has built-in testing (no test framework to install):

### Unit tests (inline)

```rust
// src/api/models.rs
pub fn validate_email(email: &str) -> bool {
    email.contains('@') && email.contains('.')
}

#[cfg(test)]              // Only compiled in test builds
mod tests {
    use super::*;

    #[test]
    fn valid_email_passes() {
        assert!(validate_email("alice@example.com"));
    }

    #[test]
    fn missing_at_fails() {
        assert!(!validate_email("aliceexample.com"));
    }
}
```

### Async tests (with tokio)

```rust
#[tokio::test]            // Like #[tokio::main] but for tests
async fn get_user_returns_user() {
    let pool = setup_test_db().await;
    let user = get_user(&pool, Uuid::new_v4()).await.unwrap();
    assert!(user.is_none());  // Empty DB
}
```

### Integration tests (in `tests/`)

```rust
// tests/api_test.rs
use axum::{body::Body, http::{Request, StatusCode}, Router};
use tower::ServiceExt;  // For oneshot

#[tokio::test]
async fn get_user_returns_404_for_missing() {
    let app = setup_app().await;

    let response = app
        .oneshot(Request::builder().uri("/users/00000000-0000-0000-0000-000000000000").body(Body::empty()).unwrap())
        .await
        .unwrap();

    assert_eq!(response.status(), StatusCode::NOT_FOUND);
}
```

### Snapshot tests (insta crate)

```bash
cargo add insta --dev
```

```rust
#[test]
fn snapshot_user_response() {
    let user = User { /* ... */ };
    let json = serde_json::to_string_pretty(&user).unwrap();
    insta::assert_snapshot!(json);
}
```

Run `cargo insta review` to accept/reject snapshot changes.

---

## Deployment: single static binary (like Go, plus musl)

Rust's deployment story matches Go's: one static binary, no runtime deps. The Rust version is often smaller thanks to LTO + strip.

### Multi-stage Dockerfile

```dockerfile
# Build stage
FROM rust:1.80-slim AS builder
WORKDIR /app
COPY . .
# Use SQLX_OFFLINE=true so the build doesn't need a DB connection
ENV SQLX_OFFLINE=true
RUN cargo build --release

# Runtime stage — distroless for minimum size
FROM gcr.io/distroless/cc-debian12
COPY --from=builder /app/target/release/myapp /myapp
EXPOSE 8080
USER nonroot:nonroot
ENTRYPOINT ["/myapp"]
```

### Fully static binary (musl target)

```bash
rustup target add x86_64-unknown-linux-musl
cargo build --release --target x86_64-unknown-linux-musl
# Result: target/x86_64-unknown-linux-musl/release/myapp — fully static, runs on any Linux
```

Note: some crates (like `openssl`) don't compile cleanly with musl. Use `rustls` instead of `openssl` for TLS (most modern crates support both).

### Graceful shutdown

```rust
use tokio::signal;

async fn shutdown_signal() {
    let ctrl_c = async { signal::ctrl_c().await.expect("install Ctrl+C handler"); };

    #[cfg(unix)]
    let terminate = async {
        signal::unix::signal(signal::unix::SignalKind::terminate())
            .expect("install signal handler")
            .recv()
            .await;
    };

    #[cfg(not(unix))]
    let terminate = std::future::pending::<()>();

    tokio::select! {
        _ = ctrl_c => {},
        _ = terminate => {},
    }
}

// In main:
axum::serve(listener, app)
    .with_graceful_shutdown(shutdown_signal())
    .await
    .unwrap();
```

---

## Top 10 Anti-Patterns (the most valuable section)

1. **Fighting the borrow checker instead of restructuring.** When the borrow checker complains, the answer is rarely "fight harder". Common fixes: `.clone()` the data (it's cheap for small types), return owned data instead of references, use `Arc<Mutex<T>>` for shared mutable state across tasks, or restructure the function to release borrows before taking new ones.

2. **Using `Rc<T>` / `RefCell<T>` across `.await` points.** These are NOT `Send` — Tokio's multi-threaded runtime rejects the resulting future. Use `Arc<T>` and `Mutex<T>` / `RwLock<T>` instead. The compiler error "future is not Send" usually means this.

3. **Using `.unwrap()` / `.expect()` in production code paths.** These panic on `Err` / `None`. In a web server, a panic in a handler crashes that request (Axum catches panics per-handler with the `catch-panic` middleware, but it's still bad). Use `?` for propagation, or `match` for explicit handling. Reserve `.unwrap()` for tests and `main()` setup that "can't fail".

4. **Not running `cargo clippy`.** Clippy catches real bugs (inefficient clones, unnecessary `to_string()`, incorrect `if let` patterns, anti-idioms). Run it in CI as `cargo clippy -- -D warnings` (treat warnings as errors). Fix all clippy suggestions — they're almost always right.

5. **Using `String` everywhere when `&str` would do.** Function parameters should take `&str` (borrow) unless you need ownership. `fn validate(email: &str)` is cheaper than `fn validate(email: String)` because callers don't need to clone. Return `String` only when you create new data; return `&str` when you're slicing existing data.

6. **Overusing `Box<dyn Trait>` for dynamic dispatch.** Generic `<T: Trait>` is zero-cost (compiler generates a copy per type). `Box<dyn Trait>` adds vtable indirection. Use generics by default; reach for `Box<dyn Trait>` only when you need runtime polymorphism (e.g., a vector of different trait impls).

7. **Forgetting to `commit` the `.sqlx/` directory.** sqlx's compile-time checking needs your DB schema. The `.sqlx/` directory (generated by `cargo sqlx prepare`) caches query data so CI/Docker builds don't need a live DB. If you forget to commit it, CI builds fail with "missing .sqlx directory" or try to connect to a non-existent DB.

8. **Mixing `anyhow::Error` and `thiserror::Error` incorrectly.** Use `thiserror` for library public APIs (typed errors let users `match` on variants). Use `anyhow` for application code (where you don't need to match on variants). Don't leak `anyhow::Error` through a library's public API — it forces users to use `anyhow` too.

9. **Not setting up `tracing` from day one.** `println!` and `eprintln!` are fine for quick debugging but don't work in production (no structured logging, no log levels, no async tracing). Start with `tracing_subscriber::fmt::init()` and use `tracing::info!`, `tracing::error!`, etc. Adding tracing later is a refactor.

10. **Using `std::sync::Mutex` instead of `tokio::sync::Mutex` in async code.** `std::sync::Mutex` blocks the entire Tokio worker thread while waiting for the lock — kills throughput. Use `tokio::sync::Mutex` (or better, `tokio::sync::RwLock` for read-heavy workloads). For simple atomic operations, `Arc<AtomicU64>` is faster than either Mutex.

---

## Cross-references

- `framework-templates` — CLAUDE.md generation template for Rust (project onboarding)
- `go-web` — Go web patterns (similar compiled-language backend, no borrow checker)
- `spring-boot-3` — Java enterprise backend (similar backend use case, GC + IoC vs ownership + traits)
- `api-and-interface-design` — Type contract design (relevant for Rust trait definitions)
- `api-patterns` — REST API patterns
- `security-and-hardening` — OWASP-aware hardening (Rust's memory safety eliminates whole classes of vulnerabilities)
- `clean-code` — General coding standards
- `testing-patterns` — Test pyramid, mocking strategies (Rust-specific syntax above; general principles there)
- `code-review-checklist` — 12-category code review checklist
- `git-workflow-and-versioning` — Branching/commit conventions for Rust projects

---

## Dependencies

Required (installed via `cargo add`):
- **Rust** 1.80+ (install via `rustup`)
- **Cargo** (bundled with Rust)
- **tokio** (`cargo add tokio --features "full"`) — async runtime
- **axum** (`cargo add axum --features "macros"`) — web framework
- **serde** + **serde_json** (`cargo add serde --features "derive"`) — JSON serialization
- **tracing** + **tracing-subscriber** — structured logging

Common additions (install via `cargo add`):
- **sqlx** (`cargo add sqlx --features "runtime-tokio postgres uuid chrono"`) — compile-time-checked SQL
- **reqwest** (`cargo add reqwest --features "json"`) — HTTP client (the de facto standard)
- **thiserror** (`cargo add thiserror`) — ergonomic error enums for libraries
- **anyhow** (`cargo add anyhow`) — dynamic error boxing for applications
- **uuid** (`cargo add uuid --features "v4,serde"`) — UUID generation
- **chrono** (`cargo add chrono --features "serde"`) — date/time (or `time` for a newer alternative)
- **tower** + **tower-http** (`cargo add tower tower-http`) — middleware (CORS, compression, tracing, etc.)
- **jsonwebtoken** (`cargo add jsonwebtoken`) — JWT auth
- **argon2** (`cargo add argon2`) — password hashing (preferred over bcrypt)
- **validator** (`cargo add validator`) — struct validation
- **rustls** (`cargo add rustls`) — TLS (preferred over `openssl` for musl compatibility)
- **config** (`cargo add config`) — config loading (env, YAML, TOML)
- **insta** (`cargo add insta --dev`) — snapshot testing
- **sqlx-cli** (`cargo install sqlx-cli`) — migration tool (CLI)
- **cargo-watch** (`cargo install cargo-watch`) — auto-rebuild on file change (dev)
- **cargo-edit** (`cargo install cargo-edit`) — adds `cargo add` / `cargo upgrade` (now mostly in Cargo itself)
- **cargo-audit** (`cargo install cargo-audit`) — vulnerability scanning
