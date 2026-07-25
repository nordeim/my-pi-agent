---
name: go-web
description: "Go (Golang 1.23+) web backend workflow skill. Covers the stdlib-first philosophy (net/http is production-grade — frameworks are optional thin wrappers), the four most popular router/middleware choices (net/http ServeMux (Go 1.22+ pattern routing), chi, Echo, Gin), sqlc for type-safe SQL codegen (preferred over ORM for most projects), pgx for native PostgreSQL drivers, the interface satisfaction model (implicit — no `implements` keyword), error-as-values (no exceptions), goroutines + channels for concurrency, context.Context for cancellation/timeouts, the standard project layout debate, testify for testing, table-driven tests, embedding assets via go:embed, Docker multi-stage builds, and the unique Go deployment story (single static binary — no runtime dependencies). Use when building any HTTP API, microservice, CLI with HTTP features, or backend service in Go — especially when the task involves choosing between stdlib and a framework, designing context-aware handlers, writing type-safe database access, or shipping a single-binary deployment where idiomatic Go differs from Node.js/Python/Ruby patterns."
license: Proprietary. LICENSE.txt has complete terms
---

# Go Web — Backend Workflow Skill

> **Target:** Go 1.23+ (released August 2024). The Go 1.22 release (February 2024) added method+pattern routing to the stdlib `net/http.ServeMux`, making a bare-stdlib web server viable for production. Go 1.23 enhanced the `range` loop semantics (per-iteration variables — fixes the classic loop-closure bug). This skill is stdlib-first: framework choices (chi/Echo/Gin) are presented as optional layers, not defaults.

## When to Use This Skill

Use this skill whenever the user is building, debugging, or extending a Go web backend. Trigger phrases include "Go", "Golang", "net/http", "ServeMux", "chi router", "Echo framework", "Gin framework", "sqlc", "pgx", "goroutine", "channel", "context.Context", "go:embed", "go mod", "table-driven test", "testify", and any reference to a `main.go` entry point, `go.mod` file, or `HandlerFunc` signature.

Do **not** use this skill for:
- **Go ≤1.21** — the stdlib `ServeMux` had no pattern routing; you needed a framework. Go 1.22+ patterns here assume the new routing.
- **CLI tools without HTTP** — only the concurrency, context, and testing sections apply.
- **Other backend languages** (Node.js, Python, Ruby, Java, Rust) — see `laravel-12`, `rails-8`, `django-6`, `rust-web`, `spring-boot-3` skills.

## Quick Start

```bash
# Initialize a new module (Go's dependency unit)
mkdir myapp && cd myapp
go mod init github.com/youruser/myapp

# Create main.go
cat > main.go << 'EOF'
package main

import (
    "log"
    "net/http"
)

func main() {
    mux := http.NewServeMux()
    mux.HandleFunc("GET /", func(w http.ResponseWriter, r *http.Request) {
        w.Write([]byte("Hello, World!"))
    })
    mux.HandleFunc("GET /users/{id}", func(w http.ResponseWriter, r *http.Request) {
        id := r.PathValue("id")
        w.Write([]byte("User: " + id))
    })

    log.Println("Listening on :8080")
    log.Fatal(http.ListenAndServe(":8080", mux))
}
EOF

go run main.go                 # Run dev server
# Visit http://localhost:8080 and http://localhost:8080/users/42

# Build a static binary
go build -o myapp main.go
./myapp                        # Run the binary (no runtime deps!)
```

### Key commands

```bash
go mod init <module-path>      # Initialize go.mod
go mod tidy                    # Add missing deps, remove unused
go get <package>               # Add a dependency
go build                       # Compile (outputs binary named after the directory)
go build -o bin/myapp          # Compile to a specific path
go run .                       # Compile + run (dev)
go test ./...                  # Run all tests
go test -v -run TestName       # Run a specific test verbosely
go test -race ./...            # Run with race detector (ALWAYS in CI)
go test -cover ./...           # With coverage
go vet ./...                   # Static analysis (built-in)
go fmt ./...                   # Format all files
golangci-lint run              # Run multiple linters (recommended for CI)
go tool pprof <binary> <prof>  # Profile CPU/memory
```

---

## Project Structure (the "standard layout" debate)

Go has NO enforced project structure. The much-debated [Standard Go Project Layout](https://github.com/golang-standards/project-layout) is **NOT** official — it's a community convention that many reject. The Go team's actual guidance: **start simple, grow as needed.**

### Recommended starting layout (small-to-medium services)

```
myapp/
├── main.go                     # Entry point — wire everything together
├── go.mod                      # Module declaration + dependencies
├── go.sum                      # Locked dependency hashes (commit this)
├── internal/                   # ← Private application code (Go enforces: only this module can import)
│   ├── handler/                # HTTP handlers (one file per resource: handler/user.go, handler/post.go)
│   ├── service/                # Business logic (use cases)
│   ├── repository/             # Data access (DB queries)
│   ├── model/                  # Domain types (structs, enums)
│   └── config/                 # Config loading (env vars, files)
├── pkg/                        # ← Public library code (safe to import by external modules)
│   └── validator/              # Reusable validators, formatters
├── migrations/                 # SQL migration files (run via golang-migrate or goose)
│   ├── 001_create_users.up.sql
│   └── 001_create_users.down.sql
├── sqlc.yaml                   # sqlc config (if using sqlc for type-safe SQL)
├── queries/                    # SQL queries (sqlc input)
│   └── user.sql
├── .env.example
├── Dockerfile                  # Multi-stage build
├── Makefile                    # Common tasks (build, test, lint, migrate)
└── README.md
```

**Key principle:** `internal/` is Go's enforced privacy boundary. Code under `internal/` can ONLY be imported by code within the same module. Use it for everything that shouldn't be reused. `pkg/` is for genuinely reusable libraries (rare — most code should be `internal/`).

### Do NOT create these directories unless you have a specific reason

- `src/` — Go doesn't use this convention. Don't import Java/TS habits.
- `pkg/` with generic sub-packages — only put code here that's actually reusable across projects.
- `app/`, `controllers/`, `models/`, `views/` — these are Rails/Laravel/Django conventions. Go is not MVC; don't impose it.

---

## Core Mental Model: Stdlib-First + Interfaces + Errors-as-Values + Goroutines

Go's distinctive paradigm is **a tiny standard library that's production-grade, implicit interfaces, explicit error handling, and lightweight concurrency.** Four things differentiate Go from Node.js/Python/Ruby backends:

### 1. The stdlib `net/http` is production-grade — frameworks are optional

```go
// Go 1.22+ — pattern routing in stdlib (no framework needed)
mux := http.NewServeMux()

// Method + path pattern
mux.HandleFunc("GET /users", listUsers)
mux.HandleFunc("POST /users", createUser)
mux.HandleFunc("GET /users/{id}", getUser)
mux.HandleFunc("DELETE /users/{id}", deleteUser)

// PathValue extracts URL params
func getUser(w http.ResponseWriter, r *http.Request) {
    id := r.PathValue("id")
    // ...
}

// Wildcard
mux.HandleFunc("GET /files/{path...}", serveFile)
```

The Go 1.22+ stdlib router handles method matching, path patterns, wildcards (`{id}`), and catch-all (`{path...}`). For most APIs, you don't need chi/Echo/Gin. Reach for a framework only when you need: middleware composition ergonomics, request binding/validation, or a built-in ORM.

### 2. Interfaces are satisfied implicitly (duck typing with compile-time safety)

```go
// Define an interface
type UserStore interface {
    Get(ctx context.Context, id string) (*User, error)
    Create(ctx context.Context, u *User) error
}

// Implement it — NO `implements` keyword, NO declaration
type PostgresUserStore struct { db *pgxpool.Pool }
func (s *PostgresUserStore) Get(ctx context.Context, id string) (*User, error) {
    // ... query pgx
}
func (s *PostgresUserStore) Create(ctx context.Context, u *User) error {
    // ... insert
}

// Use it — the store is accepted anywhere UserStore is expected
func NewHandler(store UserStore) *Handler { /* ... */ }
```

The `PostgresUserStore` satisfies `UserStore` automatically — Go checks at compile time that all methods are present with matching signatures. This enables the **accept interfaces, return structs** idiom: function parameters are interfaces (for testability), return values are concrete types (for clarity).

### 3. Errors are values, not exceptions

```go
// Go has NO try/catch. Errors are returned as the last value.
func GetUser(ctx context.Context, id string) (*User, error) {
    row := db.QueryRow(ctx, "SELECT id, name FROM users WHERE id = $1", id)
    var u User
    err := row.Scan(&u.ID, &u.Name)
    if err != nil {
        if errors.Is(err, pgx.ErrNoRows) {
            return nil, ErrUserNotFound   // Wrap in domain error
        }
        return nil, fmt.Errorf("querying user %s: %w", id, err)  // Wrap with %w
    }
    return &u, nil
}

// Caller checks explicitly
user, err := store.GetUser(ctx, id)
if err != nil {
    if errors.Is(err, ErrUserNotFound) {
        http.Error(w, "not found", http.StatusNotFound)
        return
    }
    log.Printf("getting user: %v", err)
    http.Error(w, "internal error", http.StatusInternalServerError)
    return
}
// use user
```

**Iron rule:** Always check errors. Never `_ = err`. Linters (`errcheck`) will catch this. Use `fmt.Errorf("context: %w", err)` to wrap with context while preserving the original error for `errors.Is()` / `errors.As()`.

### 4. Goroutines + channels for concurrency (no async/await)

```go
// goroutine: lightweight thread (2KB stack, scheduled by Go runtime)
go processInBackground(item)

// channel: typed communication between goroutines
results := make(chan Result, 10)  // buffered channel

for _, item := range items {
    go func(it Item) {  // ← pass `it` as parameter to avoid loop-closure bug
        result := process(it)
        results <- result
    }(item)
}

// Collect results
for i := 0; i < len(items); i++ {
    r := <-results
    // use r
}

// errgroup: like Promise.all — first error cancels the group
g, ctx := errgroup.WithContext(ctx)
for _, url := range urls {
    url := url  // ← capture loop variable
    g.Go(func() error {
        return fetch(ctx, url)
    })
}
if err := g.Wait(); err != nil {
    log.Fatal(err)
}
```

**Go 1.22+ fix:** the loop variable `url` is now per-iteration by default, so `url := url` is no longer required. But for older Go code or for clarity, the explicit capture is still common.

---

## Routing: stdlib vs chi vs Echo vs Gin

### stdlib `net/http.ServeMux` (Go 1.22+) — recommended default

```go
mux := http.NewServeMux()
mux.HandleFunc("GET /api/users", s.listUsers)
mux.HandleFunc("POST /api/users", s.createUser)
mux.HandleFunc("GET /api/users/{id}", s.getUser)
mux.HandleFunc("PUT /api/users/{id}", s.updateUser)
mux.HandleFunc("DELETE /api/users/{id}", s.deleteUser)

// Middleware: wrap the mux
handler := loggingMiddleware(authMiddleware(mux))

http.ListenAndServe(":8080", handler)
```

**Pros:** zero dependencies, Go team supported, no abstraction layer.
**Cons:** no built-in middleware chaining, no request binding, no JSON validation.

### chi (lightweight, stdlib-compatible, popular for APIs)

```bash
go get github.com/go-chi/chi/v5
```

```go
import "github.com/go-chi/chi/v5"
import "github.com/go-chi/chi/v5/middleware"

r := chi.NewRouter()
r.Use(middleware.Logger)
r.Use(middleware.Recoverer)
r.Use(authMiddleware)

r.Route("/api/users", func(r chi.Router) {
    r.Get("/", s.listUsers)
    r.Post("/", s.createUser)
    r.Get("/{id}", s.getUser)
    r.Put("/{id}", s.updateUser)
    r.Delete("/{id}", s.deleteUser)
})

http.ListenAndServe(":8080", r)
```

**Pros:** middleware composition, sub-routers, URL params via `chi.URLParam(r, "id")`, 100% `net/http` compatible.
**Cons:** slightly more verbose than Echo/Gin for simple APIs.

### Echo (ergonomic, fast, built-in binding)

```bash
go get github.com/labstack/echo/v4
```

```go
e := echo.New()
e.Use(middleware.Logger())
e.Use(middleware.Recover())

e.GET("/api/users", s.listUsers)
e.POST("/api/users", s.createUser)
e.GET("/api/users/:id", s.getUser)

// Start
e.Start(":8080")

// Handler signature is different (echo.Context, not http.ResponseWriter)
func (s *Server) listUsers(c echo.Context) error {
    users, err := s.store.List(c.Request().Context())
    if err != nil {
        return echo.NewHTTPError(500, "internal error")
    }
    return c.JSON(200, users)
}
```

**Pros:** ergonomic handler signature (`echo.Context`), built-in JSON binding/validation, automatic error handling.
**Cons:** NOT `net/http` compatible — handlers have a different signature, harder to mix with stdlib middleware.

### Gin (most popular, similar tradeoffs to Echo)

```bash
go get github.com/gin-gonic/gin
```

```go
r := gin.Default()
r.GET("/api/users", s.listUsers)
r.POST("/api/users", s.createUser)
r.GET("/api/users/:id", s.getUser)
r.Run(":8080")
```

Similar to Echo — `gin.Context` instead of `http.ResponseWriter`, built-in binding.

### Recommendation matrix

| Project profile | Use |
|---|---|
| New project, stdlib-first, simple API | **stdlib `ServeMux`** |
| New project, want middleware composition, stay `net/http`-compatible | **chi** |
| Existing Echo/Gin codebase | Stay with what you have |
| Need fast prototyping with binding/validation | **Echo or Gin** |
| Building a library that exposes an `http.Handler` | **stdlib or chi** (never Echo/Gin — they have incompatible signatures) |

**Opinionated default for new projects:** start with stdlib `ServeMux`. Add chi only when middleware composition becomes painful. Avoid Echo/Gin unless you specifically want their binding/validation ergonomics.

---

## Middleware (the `func(http.Handler) http.Handler` pattern)

Middleware in Go is just a function that wraps an `http.Handler`:

```go
// Logging middleware
func loggingMiddleware(next http.Handler) http.Handler {
    return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
        start := time.Now()
        next.ServeHTTP(w, r)
        log.Printf("%s %s %v", r.Method, r.URL.Path, time.Since(start))
    })
}

// Auth middleware
func authMiddleware(next http.Handler) http.Handler {
    return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
        token := r.Header.Get("Authorization")
        if token == "" {
            http.Error(w, "unauthorized", http.StatusUnauthorized)
            return
        }
        user, err := validateToken(token)
        if err != nil {
            http.Error(w, "invalid token", http.StatusUnauthorized)
            return
        }
        // Add user to context for downstream handlers
        ctx := context.WithValue(r.Context(), userKey{}, user)
        next.ServeHTTP(w, r.WithContext(ctx))
    })
}

// Recover from panics
func recoverMiddleware(next http.Handler) http.Handler {
    return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
        defer func() {
            if err := recover(); err != nil {
                log.Printf("panic: %v", err)
                http.Error(w, "internal error", http.StatusInternalServerError)
            }
        }()
        next.ServeHTTP(w, r)
    })
}

// Compose: outermost runs first
handler := recoverMiddleware(loggingMiddleware(authMiddleware(mux)))
```

### Getting values from context

```go
type userKey struct{}  // unexported type — prevents key collisions

// Set (in middleware)
ctx := context.WithValue(r.Context(), userKey{}, user)

// Get (in handler)
func getUser(w http.ResponseWriter, r *http.Request) {
    user, ok := r.Context().Value(userKey{}).(*User)
    if !ok || user == nil {
        http.Error(w, "no user in context", http.StatusInternalServerError)
        return
    }
    // use user
}
```

**Iron rule:** Always use an unexported struct type as the context key (`type userKey struct{}`). Using a string key (`context.WithValue(ctx, "user", u)`) can collide with other packages. The empty-struct type is a compile-time-unique key.

---

## Data Layer: sqlc (type-safe SQL) is the modern default

### Why sqlc over an ORM?

Go ORMs (GORM, ent, pop) exist but the Go community largely prefers **raw SQL with code generation**. The reasons:
- SQL is already a powerful, well-understood query language
- ORMs hide what queries actually run (the N+1 problem)
- Code generation gives you type safety without runtime reflection
- Generated code is debuggable

**sqlc** is the canonical tool: you write SQL, it generates type-safe Go code.

### sqlc setup

```bash
go install github.com/sqlc-dev/sqlc/cmd/sqlc@latest
```

```yaml
# sqlc.yaml
version: "2"
sql:
  - engine: "postgresql"
    queries: "queries/"
    schema: "migrations/"
    gen:
      go:
        package: "db"
        out: "internal/db"
        sql_package: "pgx/v5"   # Use pgx (preferred over database/sql)
        emit_json_tags: true
        emit_empty_slices: true  # Return [] instead of nil for empty results
```

```sql
-- queries/user.sql
-- name: GetUser :one
SELECT id, email, name, created_at FROM users WHERE id = $1;

-- name: ListUsers :many
SELECT id, email, name, created_at FROM users ORDER BY created_at DESC LIMIT $1 OFFSET $2;

-- name: CreateUser :one
INSERT INTO users (email, name, password_hash) VALUES ($1, $2, $3) RETURNING id, email, name, created_at;

-- name: UpdateUserName :exec
UPDATE users SET name = $2 WHERE id = $1;
```

```bash
sqlc generate    # Generates internal/db/*.go
```

```go
// Usage — fully type-safe
store := db.New(pool)
user, err := store.GetUser(ctx, "abc-123")
if err != nil {
    // err is *pgx.ErrNoRows if not found
}

users, err := store.ListUsers(ctx, db.ListUsersParams{Limit: 20, Offset: 0})

newUser, err := store.CreateUser(ctx, db.CreateUserParams{
    Email: "alice@example.com",
    Name: "Alice",
    PasswordHash: hashed,
})

err := store.UpdateUserName(ctx, db.UpdateUserNameParams{ID: "abc", Name: "Alice 2"})
```

### pgx (PostgreSQL native driver)

For PostgreSQL, **pgx** is the recommended driver — it's faster and exposes Postgres-specific features (LISTEN/NOTIFY, COPY, logical replication) that `database/sql` can't.

```bash
go get github.com/jackc/pgx/v5
```

```go
import "github.com/jackc/pgx/v5/pgxpool"

// Connection pool (production-grade)
pool, err := pgxpool.New(ctx, "postgres://user:pass@localhost:5432/myapp?sslmode=disable")
if err != nil {
    log.Fatal(err)
}
defer pool.Close()

// Direct query (when you don't have sqlc)
var name string
err = pool.QueryRow(ctx, "SELECT name FROM users WHERE id = $1", id).Scan(&name)
```

### Migration tools

```bash
# golang-migrate (most popular)
go install -tags 'postgres' github.com/golang-migrate/migrate/v4/cmd/migrate@latest
migrate -path migrations -database "postgres://..." up
migrate -path migrations -database "postgres://..." down 1

# goose (alternative)
go install github.com/pressly/goose/v3/cmd/goose@latest
goose -dir migrations postgres "postgres://..." up
```

```sql
-- migrations/001_create_users.up.sql
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email TEXT NOT NULL UNIQUE,
    name TEXT NOT NULL,
    password_hash TEXT NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
CREATE INDEX idx_users_email ON users(email);

-- migrations/001_create_users.down.sql
DROP TABLE users;
```

---

## Context: cancellation, timeouts, values

Every Go function that does I/O should take a `context.Context` as its first argument. This is non-negotiable in idiomatic Go.

```go
func (s *Server) GetUser(ctx context.Context, id string) (*User, error) {
    // ctx is checked at every I/O boundary (DB, HTTP, etc.)
    row := s.db.QueryRow(ctx, "SELECT ...", id)  // cancels if ctx is cancelled
    // ...
}

// HTTP handlers receive context from the request
func (s *Server) getUser(w http.ResponseWriter, r *http.Request) {
    ctx := r.Context()  // Cancelled when client disconnects

    user, err := s.store.GetUser(ctx, r.PathValue("id"))
    if err != nil {
        if errors.Is(err, context.Canceled) {
            // Client went away — no point writing a response
            return
        }
        http.Error(w, "not found", 404)
        return
    }
    json.NewEncoder(w).Encode(user)
}

// Set a timeout for a specific operation
ctx, cancel := context.WithTimeout(r.Context(), 5*time.Second)
defer cancel()  // ALWAYS cancel — releases resources

result, err := slowOperation(ctx, input)
```

### Context rules

1. **Always pass `ctx` as the first argument.** Not the last. Not omitted.
2. **Always `defer cancel()`** for contexts you create with `WithTimeout` / `WithCancel` / `WithValue`.
3. **Never store contexts in structs.** Pass them as function arguments.
4. **Never use `context.Background()` inside a request handler.** Use `r.Context()` so client disconnects cancel work.
5. **Context values are for request-scoped data only** (auth user, trace ID). Not for config or dependencies.

---

## JSON: encoding/json + struct tags

```go
type User struct {
    ID        string    `json:"id"`
    Email     string    `json:"email"`
    Name      string    `json:"name"`
    Password  string    `json:"-"`                  // Never serialize
    CreatedAt time.Time `json:"created_at"`
    UpdatedAt time.Time `json:"updated_at,omitempty"` // Omit if zero
}

// Encode
func (s *Server) getUser(w http.ResponseWriter, r *http.Request) {
    user, err := s.store.GetUser(r.Context(), r.PathValue("id"))
    if err != nil { /* ... */ }

    w.Header().Set("Content-Type", "application/json")
    json.NewEncoder(w).Encode(user)
}

// Decode
func (s *Server) createUser(w http.ResponseWriter, r *http.Request) {
    var input struct {
        Email    string `json:"email"`
        Name     string `json:"name"`
        Password string `json:"password"`
    }
    if err := json.NewDecoder(r.Body).Decode(&input); err != nil {
        http.Error(w, "invalid JSON", http.StatusBadRequest)
        return
    }
    // ...
}
```

For more advanced JSON needs (validation, custom marshallers), consider:
- **`encoding/json`** (stdlib) — fine for 90% of cases
- **`jsoniter`** — drop-in replacement, faster
- **`easyjson`** — codegen for maximum speed
- **`go-playground/validator`** — struct tag validation (`validate:"required,email"`)

---

## Testing: table-driven tests + testify

Go's testing is built into the toolchain. The idiom is **table-driven tests** — define a slice of test cases, loop over them.

```go
// internal/service/user_test.go
package service

import (
    "context"
    "testing"
    "github.com/stretchr/testify/assert"
    "github.com/stretchr/testify/require"
)

func TestGetUser(t *testing.T) {
    tests := []struct {
        name    string
        id      string
        wantErr error
        want    *User
    }{
        {name: "existing user", id: "abc", want: &User{ID: "abc", Name: "Alice"}},
        {name: "non-existent", id: "missing", wantErr: ErrUserNotFound},
        {name: "empty id", id: "", wantErr: ErrInvalidID},
    }

    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            // Use t.Parallel() for parallel execution
            t.Parallel()

            store := newMockStore()  // Mock implementing UserStore interface
            svc := New(store)

            got, err := svc.GetUser(context.Background(), tt.id)

            if tt.wantErr != nil {
                require.ErrorIs(t, err, tt.wantErr)
                assert.Nil(t, got)
                return
            }
            require.NoError(t, err)
            assert.Equal(t, tt.want, got)
        })
    }
}
```

### `testify` (assert + require + mock)

```bash
go get github.com/stretchr/testify
```

- `assert.Equal(t, expected, actual)` — continues on failure
- `require.NoError(t, err)` — stops test on failure (use for setup steps)
- `mock.Mock` — generate mocks via `mockgen` or `moq`

### HTTP handler tests (using `httptest`)

```go
func TestGetUserHandler(t *testing.T) {
    store := newMockStore()
    store.On("Get", mock.Anything, "abc").Return(&User{ID: "abc", Name: "Alice"}, nil)

    req := httptest.NewRequest("GET", "/users/abc", nil)
    req.SetPathValue("id", "abc")
    rec := httptest.NewRecorder()

    handler := NewHandler(store)
    handler.ServeHTTP(rec, req)

    assert.Equal(t, 200, rec.Code)
    assert.Contains(t, rec.Body.String(), "Alice")
}
```

### Race detector (ALWAYS in CI)

```bash
go test -race ./...   # Detects data races — run in CI, no exceptions
```

---

## Embedding assets with `go:embed`

Go 1.16+ lets you embed static files into the binary at compile time. No more separate asset directories.

```go
// main.go
package main

import (
    "embed"
    "io/fs"
    "net/http"
)

//go:embed static/*   // Embeds everything under static/
var staticFiles embed.FS

func main() {
    // Strip the "static/" prefix
    sub, _ := fs.Sub(staticFiles, "static")
    http.Handle("/static/", http.StripPrefix("/static/", http.FileServer(http.FS(sub))))
    http.ListenAndServe(":8080", nil)
}
```

This is invaluable for shipping a single binary that serves its own frontend assets.

---

## Deployment: the single-binary story

Go's killer feature for deployment: **one static binary, no runtime dependencies, no Docker required (though Docker is common).**

### Multi-stage Dockerfile (small image)

```dockerfile
# Build stage
FROM golang:1.23-alpine AS builder
WORKDIR /app
COPY go.mod go.sum ./
RUN go mod download
COPY . .
RUN CGO_ENABLED=0 GOOS=linux go build -ldflags="-s -w" -o /myapp .

# Runtime stage — scratch or alpine
FROM gcr.io/distroless/static-debian12
COPY --from=builder /myapp /myapp
EXPOSE 8080
USER nonroot:nonroot
ENTRYPOINT ["/myapp"]
```

Final image size: ~10-15 MB (vs 100s of MB for Node/Python).

### Direct binary deployment (no Docker)

```bash
# Build for Linux
CGO_ENABLED=0 GOOS=linux GOARCH=amd64 go build -o myapp-linux

# Upload to server
scp myapp-linux user@server:/opt/myapp/myapp
ssh user@server "systemctl restart myapp"

# Or use systemd to manage the process
```

### Graceful shutdown

```go
func main() {
    srv := &http.Server{Addr: ":8080", Handler: mux}

    // Start in background
    go func() {
        if err := srv.ListenAndServe(); err != nil && err != http.ErrServerClosed {
            log.Fatalf("listen: %v", err)
        }
    }()

    // Wait for interrupt signal
    quit := make(chan os.Signal, 1)
    signal.Notify(quit, syscall.SIGINT, syscall.SIGTERM)
    <-quit
    log.Println("Shutting down...")

    // Give requests 30 seconds to finish
    ctx, cancel := context.WithTimeout(context.Background(), 30*time.Second)
    defer cancel()
    if err := srv.Shutdown(ctx); err != nil {
        log.Fatal("Server forced to shutdown:", err)
    }
    log.Println("Server exiting")
}
```

---

## Top 10 Anti-Patterns (the most valuable section)

1. **Ignoring errors (`_ = err`).** Go has no exceptions — every error must be checked. Use `errcheck` linter to catch unchecked errors. Silent error swallowing is the #1 source of Go bugs in production.

2. **Loop variable capture (pre-Go 1.22).** Before Go 1.22, `for _, item := range items { go func() { use(item) }() }` — all goroutines see the same `item` (the last one). Fix: pass as parameter `go func(it Item) { use(it) }(item)` or upgrade to Go 1.22+ where this is fixed. Always test with `-race` to catch this.

3. **Not using `context.Context`.** Every I/O function should take `ctx` as the first argument. Without it, you can't cancel long-running operations on client disconnect, can't enforce timeouts, can't propagate trace IDs. Adding context later is a refactor; do it from day one.

4. **Storing context in a struct.** `type Service struct { ctx context.Context }` — don't. Context is per-request; structs are often long-lived. Pass `ctx` as a function argument instead.

5. **Using `context.Background()` inside a request handler.** Use `r.Context()` so client disconnects cancel the work. `context.Background()` is for `main()` and tests only.

6. **String context keys.** `context.WithValue(ctx, "user", u)` can collide with other packages. Always use an unexported struct type: `type userKey struct{}; context.WithValue(ctx, userKey{}, u)`.

7. **Returning interfaces instead of structs.** The idiom is **accept interfaces, return structs.** Returning an interface forces all callers to use that interface even if they want the concrete type. Return concrete types; let callers define their own interfaces for what they need.

8. **Using global state.** `var db *sql.DB` at package level is a global. It makes testing harder and creates hidden coupling. Inject dependencies via struct fields or function args. The only acceptable globals are constants and `init()` registrations.

9. **Not running `go vet` and `golangci-lint`.** Go's tooling catches real bugs (shadowed variables, unreachable code, struct tag mistakes). Run `go vet ./...` locally and `golangci-lint run` in CI. Fix all warnings — Go linters are higher signal than other languages'.

10. **Importing frameworks by default.** Before reaching for Gin/Echo/Fiber, check if the stdlib does what you need. `net/http` (Go 1.22+), `encoding/json`, `database/sql`, `html/template` are all production-grade. The "batteries included" philosophy is real — each framework you add is a dependency to maintain.

---

## Cross-references

- `framework-templates` — CLAUDE.md generation template for Go (project onboarding)
- `rust-web` — Rust web patterns (similar compiled-language backend, different ownership model)
- `spring-boot-3` — Java enterprise backend (similar JVM-adjacent ecosystem, very different idioms)
- `api-and-interface-design` — Type contract design (relevant for Go interface definitions)
- `api-patterns` — REST API patterns
- `security-and-hardening` — OWASP-aware hardening (Go has good defaults but no built-in CSRF/XSS for raw HTML)
- `clean-code` — General coding standards
- `testing-patterns` — Test pyramid, mocking strategies (Go-specific syntax above; general principles there)
- `code-review-checklist` — 12-category code review checklist
- `git-workflow-and-versioning` — Branching/commit conventions for Go projects

---

## Dependencies

Required (installed via `go mod`):
- **Go** 1.23+ (1.22 minimum for stdlib pattern routing)
- **stdlib** `net/http`, `encoding/json`, `database/sql`, `context`, `sync`, `testing` — all built-in

Common additions (install via `go get`):
- **github.com/jackc/pgx/v5** — PostgreSQL native driver (preferred over `database/sql` for Postgres)
- **github.com/go-chi/chi/v5** — lightweight router (stdlib-compatible)
- **github.com/labstack/echo/v4** — ergonomic framework (NOT stdlib-compatible)
- **github.com/gin-gonic/gin** — popular framework (NOT stdlib-compatible)
- **github.com/sqlc-dev/sqlc** — type-safe SQL codegen (CLI tool, install separately)
- **github.com/golang-migrate/migrate/v4** — database migrations
- **github.com/pressly/goose/v3** — alternative migration tool
- **github.com/stretchr/testify** — assertions and mocking
- **github.com/go-playground/validator/v10** — struct tag validation
- **golang.org/x/sync/errgroup** — `errgroup.Group` for parallel goroutine coordination
- **go.uber.org/zap** — structured logging (faster than `log`)
- **github.com/spf13/viper** — config loading (env vars, YAML, etc.)
- **github.com/jackc/pgx/v5/pgxpool** — connection pool (part of pgx)
