---
name: phoenix-1-7
description: "Phoenix 1.7 (Elixir 1.16+ on the BEAM VM) full-stack functional web framework workflow skill. Covers the OTP supervision tree mental model (processes, GenServers, Supervisors — fault tolerance via 'let it crash'), Ecto 3 (the Elixir ORM with migrations, changesets for validation + data casting, Repo for queries, schemas with has_many/belongs_to), LiveView (the SPA-less real-time UI paradigm — server-rendered HTML that updates via WebSocket, no React/Vue/Svelte needed, no JS for most interactions), HEEx templates (HTML-aware EEx with ~H sigil and <.component> syntax), the new unified routes Phoenix.Router.scope/pipe_through (Phoenix 1.7 introduced verified routes ~p sigil and the new Phoenix.Component sigil ~H), Presence (track connected users), PubSub (the built-in pub/sub that powers LiveView and real-time features), Erlang Term Storage (ETS) for in-memory caching, Mnesia for distributed storage, the Mix build tool, ExUnit testing (built-in, async by default), and deployment via Elixir releases (self-contained BEAM bundles) + Fly.io (the canonical Elixir host). Use when building any Elixir/Phoenix web app, real-time app, or distributed system — especially when the task involves LiveView state management, Ecto changesets, OTP supervision, PubSub broadcasting, or release deployment where idiomatic Phoenix (functional + actor model + BEAM concurrency) differs fundamentally from object-oriented frameworks like Rails/Django/Spring Boot."
license: Proprietary. LICENSE.txt has complete terms
---

# Phoenix 1.7 (Elixir) — Functional Real-Time Web Framework

> **Target:** Phoenix 1.7+ (released 2023, current as of 2025) on Elixir 1.16+ running on the **BEAM VM** (Erlang's virtual machine — designed for massive concurrency, fault tolerance, and soft real-time systems). Phoenix 1.7 introduced **verified routes** (`~p` sigil), **HEEx templates** as default, and the new **`Phoenix.Component`** module replacing `Phoenix.LiveView.Helpers`. The framework's killer feature is **LiveView** — server-rendered real-time UIs that replace client-side SPA frameworks for most use cases.

## When to Use This Skill

Use this skill whenever the user is building, debugging, or extending a Phoenix 1.7 / Elixir application. Trigger phrases include "Phoenix", "Elixir", "BEAM", "OTP", "GenServer", "Supervisor", "LiveView", "LiveComponent", "Ecto", "changeset", "HEEx", "HEEx templates", "~H sigil", "~p sigil", "verified routes", "PubSub", "Presence", "Mix", "ExUnit", "Phoenix.Pipeline", "Erlang Term Storage", "ETS", "Fly.io", "Mnesia", "release", and any reference to `lib/myapp_web/`, `lib/myapp/`, `mix.exs`, or `config/config.exs`.

Do **not** use this skill for:
- **Phoenix ≤1.6** — verified routes, HEEx defaults, and `Phoenix.Component` are 1.7+. Some patterns here require 1.7.
- **Plain Elixir / Erlang** (without Phoenix) — only the OTP/BEAM sections apply.
- **Ruby on Rails** — different language (Ruby vs Elixir), different paradigm (OO vs functional), different VM (no BEAM concurrency). See `rails-8` skill.
- **Other web frameworks** (Go, Rust, Java, Python, JS) — see `go-web`, `rust-web`, `spring-boot-3`, `dotnet-9`, `django-6`, `fastapi-sqlalchemy`, `laravel-12`, `nestjs` skills.

Cross-reference: `rails-8` is the closest comparable framework (Phoenix was created by former Rails core team member Chris McCord), but the paradigms are fundamentally different.

## Quick Start

```bash
# Install Elixir (which includes Erlang/OTP)
# macOS: brew install elixir
# Linux: see https://elixir-lang.org/install.html
# Windows: download installer from elixir-lang.org

# Install Phoenix 1.7 installer
mix archive.install hex phx_new

# Create a new project
mix phx.new myapp --database postgres
# Prompts: install dependencies (Y), configure database (Y)

cd myapp
mix deps.get

# Set up the database (requires Postgres running locally)
mix ecto.create

# Dev server
mix phx.server                  # http://localhost:4000
# OR with interactive Elixir shell (IEx):
iex -S mix phx.server           # Lets you call functions from the running app

# Interactive shell (without server)
iex -S mix                      # Open IEx with the app loaded
```

### Key Mix commands

```bash
mix phx.new <name>              # Create a new Phoenix project
mix phx.server                  # Start the dev server
mix phx.gen.live                # Generate a LiveView resource (CRUD + real-time)
mix phx.gen.html                # Generate an HTML (non-LiveView) resource
mix phx.gen.json                # Generate a JSON API resource
mix phx.gen.schema              # Generate just an Ecto schema + migration
mix phx.gen.context             # Generate a business logic context module
mix phx.gen.auth                # Generate authentication (phx.gen.auth)

mix ecto.create                 # Create the database
mix ecto.migrate                # Run migrations
mix ecto.rollback               # Roll back the last migration
mix ecto.reset                  # Drop, create, migrate, seed (DESTRUCTIVE)
mix ecto.gen.migration <Name>   # Generate a blank migration

mix test                        # Run all tests
mix test --only wip             # Run tests tagged :wip
mix test test/myapp_web/        # Run a directory
mix test test/some_file_test.exs:42  # Run a single test at line 42

mix format                      # Format all Elixir files
mix credo                       # Linter (install via: mix archive.install hex credo)
mix dialyzer                    # Type checker (install via: mix archive.install hex dialyxir)

mix phx.routes                  # List all routes (verified via ~p)
mix phx.server                  # Start server with Phoenix.Endpoint
mix release                     # Build a production release (self-contained BEAM bundle)
```

---

## Project Structure (Phoenix 1.7 canonical layout)

Phoenix projects have a clear separation between the **web layer** (`MyappWeb`) and the **business logic** (`Myapp`). This is enforced by convention.

```
myapp/
├── lib/
│   ├── myapp/                  # ← Business logic (domain)
│   │   ├── application.ex      # OTP Application module (starts supervision tree)
│   │   ├── repo.ex             # Ecto Repo (database connection)
│   │   ├── accounts.ex         # Context module (accounts business logic)
│   │   ├── blog.ex             # Context module (blog business logic)
│   │   ├── accounts/
│   │   │   ├── user.ex         # Ecto schema + changeset
│   │   │   └── token.ex        # Auth token schema
│   │   └── blog/
│   │       ├── post.ex         # Post schema + changeset
│   │       └── comment.ex      # Comment schema + changeset
│   └── myapp_web/              # ← Web layer (controllers, views, LiveViews)
│       ├── endpoint.ex         # Phoenix.Endpoint (HTTP entry point)
│       ├── router.ex           # Phoenix.Router (routes)
│       ├── telemetry.ex        # Telemetry metrics
│       ├── components/         # Reusable UI components (HEEx)
│       │   ├── core_components.ex  # Built-in button, form, etc. components
│       │   └── layouts/        # Layouts (app.ex, root.ex)
│       ├── controllers/        # Regular (non-LiveView) controllers
│       │   ├── page_html/      # Templates for PageController
│       │   │   └── index.html.heex
│       │   ├── page_controller.ex
│       │   ├── error_html.ex   # Error page rendering
│       │   └── error_json.ex   # JSON error rendering
│       ├── live/               # LiveView modules
│       │   ├── post_live/
│       │   │   ├── index.ex    # List posts (LiveView)
│       │   │   ├── show.ex     # Show a post (LiveView)
│       │   │   ├── form.ex     # Create/edit form (LiveView)
│       │   │   └── components.ex  # Reusable LiveComponents
│       │   └── user_live/
│       │       └── settings.ex
│       └── channels/           # WebSocket channels (if using sockets directly)
│           ├── user_socket.ex
│           └── room_channel.ex
├── priv/
│   ├── repo/
│   │   ├── migrations/         # Ecto migrations
│   │   │   └── 20250115120000_create_users.exs
│   │   └── seeds.exs           # Seed data
│   └── static/                 # Static assets (served as-is)
│       └── images/
├── config/
│   ├── config.exs              # Base config
│   ├── dev.exs                 # Dev overrides
│   ├── prod.exs                # Prod overrides
│   ├── runtime.exs             # Runtime config (env vars) — loaded at boot
│   └── test.exs                # Test overrides
├── test/
│   ├── support/                # Test helpers
│   │   ├── conn_case.ex        # HTTP test setup
│   │   └── data_case.ex        # DB test setup
│   ├── myapp_web/              # Web tests
│   │   └── controllers/
│   │       └── page_controller_test.exs
│   └── myapp/                  # Domain tests
│       └── accounts_test.exs
├── mix.exs                     # ← Mix project config (deps, version)
├── mix.lock                    # Locked dep versions (commit this)
├── .formatter.exs              # Elixir formatter config
└── Dockerfile
```

### The context pattern (enforced separation)

Phoenix enforces a **context boundary** between the web layer and business logic. The web layer (`MyappWeb`) calls context modules (`Myapp.Accounts`, `Myapp.Blog`), never the schemas directly.

```elixir
# lib/myapp/accounts.ex — Context module (the public API for accounts)
defmodule MyApp.Accounts do
  alias MyApp.Repo
  alias MyApp.Accounts.User

  def list_users, do: Repo.all(User)

  def get_user!(id), do: Repo.get!(User, id)

  def get_user(id) do
    case Repo.get(User, id) do
      nil -> {:error, :not_found}
      user -> {:ok, user}
    end
  end

  def create_user(attrs) do
    %User{}
    |> User.changeset(attrs)
    |> Repo.insert()
  end

  def update_user(%User{} = user, attrs) do
    user
    |> User.changeset(attrs)
    |> Repo.update()
  end

  def delete_user(%User{} = user), do: Repo.delete(user)
end
```

The controller / LiveView calls `MyApp.Accounts.create_user/1` — never `MyApp.Repo.insert/1` or `MyApp.Accounts.User.changeset/2` directly. This keeps the web layer decoupled from the data layer.

---

## Core Mental Model: Functional + Actor Model + Pattern Matching + Let-It-Crash

Elixir/Phoenix's distinctive paradigm is **functional programming on the BEAM VM with the actor model for concurrency.** Four things differentiate Phoenix from Rails/Django/Spring Boot:

### 1. Functional programming (no classes, no mutation, no loops)

```elixir
# No classes — modules + functions
defmodule MyApp.Math do
  def square(x), do: x * x

  # Pattern matching (replaces if/else and switch)
  def classify(0), do: :zero
  def classify(n) when n > 0, do: :positive
  def classify(n) when n < 0, do: :negative

  # No for-loops — use recursion or Enum/Stream
  def sum_list(list), do: Enum.sum(list)

  # Pipe operator |> (Elixir's killer feature)
  def process(text) do
    text
    |> String.downcase()
    |> String.trim()
    |> String.split(~r/\s+/)
    |> Enum.map(&String.length/1)
    |> Enum.sum()
  end
end
```

The pipe operator `|>` passes the result of the previous expression as the first argument to the next. This makes data transformation pipelines read top-to-bottom (like Unix pipes), instead of inside-out function calls.

### 2. Actor model (processes, not threads)

```elixir
# Spawn a process (BEAM process — NOT OS thread — ~2KB stack, millions possible)
pid = spawn(fn -> 
  receive do
    {:hello, from} -> send(from, :world)
    {:bye, _} -> exit(:normal)
  end
end)

# Send a message
send(pid, {:hello, self()})

# Receive a message (with timeout)
receive do
  :world -> IO.puts("Got :world")
after
  1000 -> IO.puts("Timed out")
end

# GenServer (the canonical stateful process)
defmodule MyApp.Counter do
  use GenServer

  # Client API
  def start_link(initial \\ 0), do: GenServer.start_link(__MODULE__, initial, name: __MODULE__)
  def increment, do: GenServer.cast(__MODULE__, :increment)
  def value, do: GenServer.call(__MODULE__, :value)

  # Server callbacks
  @impl true
  def init(initial), do: {:ok, initial}

  @impl true
  def handle_cast(:increment, state), do: {:noreply, state + 1}

  @impl true
  def handle_call(:value, _from, state), do: {:reply, state, state}
end
```

BEAM processes are:
- **Lightweight**: ~2KB stack each (you can have millions)
- **Isolated**: no shared memory, communicate via messages
- **Preemptive**: the BEAM scheduler interrupts long-running processes
- **Fault-tolerant**: a crash in one process doesn't crash others

### 3. Supervision trees (let it crash)

```elixir
# lib/myapp/application.ex — the OTP application starts a supervision tree
defmodule MyApp.Application do
  use Application

  @impl true
  def start(_type, _args) do
    children = [
      MyApp.Repo,                           # Ecto Repo (DB connection pool)
      MyAppWeb.Telemetry,                   # Telemetry
      {Phoenix.PubSub, name: MyApp.PubSub}, # PubSub (for LiveView, channels)
      MyAppWeb.Endpoint,                    # Phoenix HTTP endpoint
      {MyApp.Counter, 0},                   # Custom GenServer
      {MyApp.Cache, []},                    # Another custom GenServer
    ]

    opts = [strategy: :one_for_one, name: MyApp.Supervisor]
    Supervisor.start_link(children, opts)
  end
end
```

The supervision tree's job is to **restart processes when they crash**. Instead of defensive programming (try/catch everywhere), Elixir's philosophy is "let it crash" — a process crashes, the supervisor restarts it in a known-good state. This is the opposite of Java/Python/Ruby's defensive-programming culture.

Strategies:
- `:one_for_one` — restart only the crashed child
- `:one_for_all` — restart all children (when they're interdependent)
- `:rest_for_one` — restart the crashed child and all started after it

### 4. Pattern matching + immutability (no null pointer exceptions)

```elixir
# Pattern matching (replaces if/else and null checks)
case Repo.get(User, id) do
  nil -> {:error, :not_found}
  %User{} = user -> {:ok, user}
end

# The `!` suffix means "raise on not found" (use when you expect it to exist)
user = Repo.get!(User, id)   # Raises Ecto.NoResultsError if nil

# Immutability — data never changes, you transform it
# `%{user | name: "Alice"}` returns a NEW map with name updated
updated_user = %{user | name: "Alice", email: "alice@example.com"}

# No null pointer exceptions — `nil` is a value, not a missing reference
String.upcase(nil)   # Raises FunctionClauseError (clear, not a NullPointerException)
nil && "hello"       # Returns nil (short-circuit)
"hello" || "default" # Returns "hello" (truthy)
```

---

## Ecto 3 (the Elixir data layer)

Ecto is NOT an ORM in the Rails/Active Record sense — it's a wrapper around SQL with explicit schemas, changesets, and queries. The mental model is closer to a typed SQL DSL than an ORM.

### Schemas + changesets

```elixir
# lib/myapp/blog/post.ex
defmodule MyApp.Blog.Post do
  use Ecto.Schema
  import Ecto.Changeset

  schema "posts" do
    field :title, :string
    field :body, :string
    field :slug, :string
    field :status, Ecto.Enum, values: [:draft, :published, :archived], default: :draft
    field :published_at, :utc_datetime_usec
    field :view_count, :integer, default: 0
    field :metadata, :map, default: %{}

    belongs_to :author, MyApp.Accounts.User
    has_many :comments, MyApp.Blog.Comment

    timestamps()    # inserted_at, updated_at
  end

  @doc "Changeset for creating a post"
  def changeset(post, attrs) do
    post
    |> cast(attrs, [:title, :body, :status, :published_at, :author_id])
    |> validate_required([:title, :body, :author_id])
    |> validate_length(:title, min: 3, max: 200)
    |> validate_change(:published_at, fn :published_at, datetime ->
      if DateTime.compare(datetime, DateTime.utc_now()) == :gt do
        [published_at: "cannot be in the future"]
      else
        []
      end
    end)
    |> put_slug()
    |> unique_constraint(:slug)
  end

  defp put_slug(%{valid?: true, changes: %{title: title}} = changeset) do
    put_change(changeset, :slug, Slug.slugify(title))
  end

  defp put_slug(changeset), do: changeset
end
```

**Changesets** are the Elixir replacement for `validates` in Rails or `@Column` constraints in JPA. A changeset is:
- A data structure that wraps an entity + the changes you want to make
- Validates the changes against rules you define
- Returns either a valid changeset (ready for insert/update) or an invalid one (with errors)

```elixir
# Usage in a context
def create_post(attrs) do
  %Post{}
  |> Post.changeset(attrs)
  |> Repo.insert()    # Returns {:ok, post} or {:error, changeset}
end

# In a controller / LiveView
case Blog.create_post(attrs) do
  {:ok, post} -> 
    {:noreply, redirect(socket, to: ~p"/posts/#{post}")}
  {:error, changeset} -> 
    {:noreply, assign(socket, :changeset, changeset)}
end
```

### Queries (the `Ecto.Query` DSL)

```elixir
import Ecto.Query

# Simple query
posts = Repo.all(from p in Post, where: p.status == :published, order_by: [desc: p.inserted_at])

# Pipe-style query (preferred)
posts =
  Post
  |> where([p], p.status == :published)
  |> order_by([p], desc: p.inserted_at)
  |> limit(10)
  |> Repo.all()

# Without the binding (when querying a single schema — Elixir 1.17+ syntax)
posts =
  Post
  |> where(status: :published)
  |> order_by(desc: :inserted_at)
  |> Repo.all()

# Eager loading (avoid N+1)
posts =
  Post
  |> preload(:author)
  |> preload(comments: :author)
  |> Repo.all()

# Joins
posts =
  Post
  |> join(:inner, [p], a in assoc(p, :author))
  |> where([p, a], a.active == true)
  |> preload([p, a], author: a)
  |> Repo.all()

# Aggregation
counts =
  Post
  |> group_by([p], p.status)
  |> select([p], {p.status, count(p.id)})
  |> Repo.all()
# => [draft: 5, published: 20, archived: 3]

# Async (Ecto 3+ supports async queries)
async_task = Task.async(fn -> Repo.all(Post) end)
posts = Task.await(async_task)
```

### Migrations

```elixir
# priv/repo/migrations/20250115120000_create_posts.exs
defmodule MyApp.Repo.Migrations.CreatePosts do
  use Ecto.Migration

  def change do
    create table(:posts) do
      add :title, :string, null: false
      add :body, :text, null: false
      add :slug, :string, null: false
      add :status, :string, null: false, default: "draft"
      add :published_at, :utc_datetime_usec
      add :view_count, :integer, default: 0, null: false
      add :metadata, :map, default: %{}
      add :author_id, references(:users, on_delete: :delete_all), null: false

      timestamps()
    end

    create unique_index(:posts, [:slug])
    create index(:posts, [:status, :published_at])
  end
end
```

---

## LiveView (the SPA-less real-time UI)

LiveView is Phoenix's killer feature. Instead of writing a React/Vue/Svelte SPA, you write server-rendered HTML that updates in real-time via a WebSocket. **No JavaScript needed for most interactions.**

### A LiveView module

```elixir
# lib/myapp_web/live/post_live/index.ex
defmodule MyAppWeb.PostLive.Index do
  use MyAppWeb, :live_view

  alias MyApp.Blog
  alias MyApp.Blog.Post

  @impl true
  def mount(_params, _session, socket) do
    if connected?(socket), do: Blog.subscribe()    # Subscribe to PubSub for real-time updates

    {:ok, 
     socket
     |> assign(:posts, Blog.list_posts())
     |> stream(:posts, Blog.list_posts())}          # stream for efficient large lists
  end

  @impl true
  def handle_params(params, _url, socket) do
    {:noreply, apply_action(socket, socket.assigns.live_action, params)}
  end

  defp apply_action(socket, :edit, %{"id" => id}) do
    socket
    |> assign(:page_title, "Edit Post")
    |> assign(:post, Blog.get_post!(id))
  end

  defp apply_action(socket, :new, _params) do
    socket
    |> assign(:page_title, New Post")
    |> assign(:post, %Post{})
  end

  defp apply_action(socket, :index, _params) do
    socket
    |> assign(:page_title, "Listing Posts")
    |> assign(:post, nil)
  end

  @impl true
  def handle_info({:post_created, post}, socket) do
    {:noreply, stream_insert(socket, :posts, post, at: 0)}
  end

  @impl true
  def handle_info({:post_updated, post}, socket) do
    {:noreply, stream_insert(socket, :posts, post)}
  end

  @impl true
  def handle_event("delete", %{"id" => id}, socket) do
    post = Blog.get_post!(id)
    {:ok, _} = Blog.delete_post(post)

    {:noreply, stream_delete(socket, :posts, post)}
  end
end
```

### LiveView HEEx template

```elixir
# lib/myapp_web/live/post_live/index.html.heex
<.header>
  Listing Posts
  <:actions>
    <.link patch={~p"/posts/new"}>
      <.button>New Post</.button>
    </.link>
  </:actions>
</.header>

<.table id="posts" rows={@streams.posts}>
  <:col :let={{_dom_id, post}} label="Title">
    <.link navigate={~p"/posts/#{post}"}>{post.title}</.link>
  </:col>
  <:col :let={{_dom_id, post}} label="Status">{post.status}</:col>
  <:col :let={{_dom_id, post}} label="Published">
    {post.published_at && Calendar.strftime(post.published_at, "%B %d, %Y")}
  </:col>
  <:action :let={{_dom_id, post}}>
    <.link navigate={~p"/posts/#{post}/edit"}>Edit</.link>
  </:action>
  <:action :let={{_dom_id, post}}>
    <.link phx-click="delete" phx-value-id={post.id} data-confirm="Are you sure?">
      Delete
    </.link>
  </:action>
</.table>
```

### How LiveView works

1. User visits `/posts` — server renders full HTML and sends it (fast first paint, no JS framework load)
2. Client establishes a WebSocket connection (Phoenix.Socket)
3. User clicks "Delete" — a `phx-click="delete"` event is sent over the WebSocket
4. Server receives the event, runs `handle_event("delete", ..., socket)`
5. Server returns the new state via `{:noreply, stream_delete(socket, :posts, post)}`
6. Server computes the minimal DOM diff and sends only the changed HTML over the WebSocket
7. Client patches the DOM

**Key insight:** all state lives on the server. The client is a thin WebSocket + DOM patcher. No client-side state management, no React/Vue re-renders, no JSON API. Just server-rendered HTML fragments.

### LiveComponents (stateful reusable components)

```elixir
# lib/myapp_web/live/components/chart.ex
defmodule MyAppWeb.Live.Components.Chart do
  use MyAppWeb, :live_component

  def render(assigns) do
    ~H"""
    <div id={@id} class="chart" phx-hook="Chart">
      <canvas data-data={Jason.encode!(@data)}></canvas>
    </div>
    """
  end
end
```

```elixir
# Usage in a parent LiveView
~H"""
<.live_component module={MyAppWeb.Live.Components.Chart} id="sales-chart" data={@sales_data} />
"""
```

LiveComponents have their own state and `handle_event/3` — useful for self-contained widgets like charts, forms, modals.

---

## HEEx Templates (HTML-aware EEx)

Phoenix 1.7 uses **HEEx** (HTML-aware Embedded Elixir) as the default template language. HEEx is `~H` sigil — it parses HTML properly (not just string interpolation), so it catches unclosed tags and validates attributes.

```elixir
# lib/myapp_web/components/core_components.ex
defmodule MyAppWeb.CoreComponents do
  use Phoenix.Component

  attr :type, :atom, default: :button, values: [:button, :link]
  attr :class, :string, default: ""
  attr :rest, :global, include: ~w(href patch navigate method)
  slot :inner_block, required: true

  def button(assigns) do
    ~H"""
    <button
      type="button"
      class={["phx-submit-loading:opacity-75 rounded-lg bg-zinc-900 px-3 py-2", @class]}
      {@rest}
    >
      {render_slot(@inner_block)}
    </button>
    """
  end

  attr :title, :string, required: true
  attr :subtitle, :string, default: nil
  slot :actions
  slot :inner_block, required: true

  def header(assigns) do
    ~H"""
    <header class="border-b border-zinc-200">
      <div class="flex items-center justify-between">
        <div>
          <h1 class="text-lg font-semibold">{@title}</h1>
          {@subtitle && <p class="text-sm text-zinc-600">{@subtitle}</p>}
        </div>
        <div class="flex gap-2">
          {render_slot(@actions)}
        </div>
      </div>
      <div class="mt-4">
        {render_slot(@inner_block)}
      </div>
    </header>
    """
  end
end
```

### Function components + slots

Phoenix 1.7's `Phoenix.Component` provides:
- **`attr`** — declare typed component attributes (validated at compile time)
- **`slot`** — declare named slots (like Vue's slots or React's children, but typed)
- **`render_slot`** — render a slot's content
- **`~H`** sigil — HEEx template literal

```elixir
# Usage in another template or LiveView
~H"""
<.header title="Posts" subtitle="All published posts">
  <:actions>
    <.link patch={~p"/posts/new"}>
      <.button>New Post</.button>
    </.link>
  </:actions>

  <.table rows={@posts}>
    <:col :let={post} label="Title">{post.title}</:col>
  </.table>
</.header>
"""
```

### Verified routes (`~p` sigil)

Phoenix 1.7 introduced **verified routes** — the `~p` sigil is checked at compile time against your router. If you typo a path, the build fails.

```elixir
# lib/myapp_web/router.ex
defmodule MyAppWeb.Router do
  use MyAppWeb, :router

  scope "/", MyAppWeb do
    pipe_through :browser

    live "/posts", PostLive.Index, :index
    live "/posts/new", PostLive.Index, :new
    live "/posts/:id/edit", PostLive.Index, :edit
    live "/posts/:id", PostLive.Show, :show
  end
end
```

```elixir
# In a controller or LiveView — verified at compile time
redirect(conn, to: ~p"/posts/#{post}")           # ✅ OK
redirect(conn, to: ~p"/postz/#{post}")           # ❌ Build fails — route doesn't exist
```

This eliminates an entire class of runtime "route not found" bugs.

---

## PubSub + Presence (real-time)

```elixir
# Broadcast to all subscribers of a topic
Phoenix.PubSub.broadcast(MyApp.PubSub, "posts", {:post_created, post})

# Subscribe to a topic
Phoenix.PubSub.subscribe(MyApp.PubSub, "posts")

# In a GenServer or LiveView, receive broadcasts
def handle_info({:post_created, post}, socket) do
  {:noreply, stream_insert(socket, :posts, post, at: 0)}
end
```

### Presence (track connected users)

```elixir
# Track presence when a LiveView connects
defmodule MyAppWeb.Presence do
  use Phoenix.Presence,
    otp_app: :myapp,
    pubsub_server: MyApp.PubSub
end

# In a LiveView
def mount(_params, _session, socket) do
  if connected?(socket) do
    {:ok, _} = Presence.track(self(), "room:lobby", socket.assigns.current_user.id, %{
      online_at: System.system_time(:second)
    })
    Phoenix.PubSub.subscribe(MyApp.PubSub, "room:lobby")
  end

  {:ok, assign(socket, :presences, Presence.list("room:lobby"))}
end

def handle_info(%{event: "presence_diff"}, socket) do
  {:noreply, assign(socket, :presences, Presence.list("room:lobby"))}
end
```

Presence is built on CRDTs (conflict-free replicated data types) — it scales to millions of connected users without a single point of failure.

---

## Testing (ExUnit — built-in, async by default)

```elixir
# test/myapp/blog_test.exs
defmodule MyApp.BlogTest do
  use MyApp.DataCase, async: true    # async: true runs in parallel with other tests

  alias MyApp.Blog

  describe "posts" do
    test "create_post/1 with valid data creates a post" do
      user = user_fixture()
      valid_attrs = %{title: "Some title", body: "Some body", author_id: user.id}

      assert {:ok, %Post{} = post} = Blog.create_post(valid_attrs)
      assert post.title == "Some title"
      assert post.body == "Some body"
    end

    test "create_post/1 with invalid data returns error changeset" do
      assert {:error, %Ecto.Changeset{}} = Blog.create_post(%{title: nil, body: nil})
    end
  end
end
```

### LiveView tests

```elixir
# test/myapp_web/live/post_live_test.exs
defmodule MyAppWeb.PostLiveTest do
  use MyAppWeb.ConnCase, async: true

  import Phoenix.LiveViewTest

  describe "Index" do
    test "lists all posts", %{conn: conn} do
      {:ok, _index_live, html} = live(conn, ~p"/posts")

      assert html =~ "Listing Posts"
    end

    test "creates new post", %{conn: conn} do
      {:ok, index_live, _html} = live(conn, ~p"/posts")

      assert index_live |> element("a", "New Post") |> render_click() =~
               "New Post"

      assert_patch(index_live, ~p"/posts/new")

      assert index_live
             |> form("#post-form", post: %{title: "Test Post", body: "Body"})
             |> render_submit()

      assert_patch(index_live, ~p"/posts")

      html = render(index_live)
      assert html =~ "Test Post"
    end
  end
end
```

Cross-reference: `testing-patterns` for general test pyramid / mocking strategies.

---

## Deployment: Elixir Releases + Fly.io

### Build a release

```bash
# Set SECRET_KEY_BASE (required for prod)
export SECRET_KEY_BASE=$(mix phx.gen.secret)

# Build the release
MIX_ENV=prod mix assets.deploy    # Compile + minify assets
MIX_ENV=prod mix release          # Build self-contained BEAM bundle

# Output: _build/prod/rel/myapp/bin/myapp
# Run it:
_build/prod/rel/myapp/bin/myapp start
# OR:
_build/prod/rel/myapp/bin/myapp daemon    # Background
_build/prod/rel/myapp/bin/myapp remote    # Connect to running node (IEx)
```

A release is a **self-contained directory** containing the BEAM VM, all compiled Elixir/Erlang code, and your app. No Elixir install needed on the target — just copy the release and run.

### Fly.io (the canonical Elixir host)

Fly.io is the canonical Elixir host — they support BEAM clustering out of the box, which lets you run Phoenix across multiple regions with libcluster.

```bash
# Install flyctl
curl -L https://fly.io/install.sh | sh

# Launch the app on Fly.io
fly launch            # Generates Dockerfile + fly.toml

# Deploy
fly deploy

# Open a remote IEx shell on the deployed app
fly ssh console -C "/app/bin/myapp remote"

# Scale to multiple regions
fly scale count 3 --region sea,fra,syd
```

### Docker

```dockerfile
# Generated by `fly launch` or written manually
FROM hexpm/elixir:1.16.0-erlang-26.2.2-debian-bullseye-20231009-slim AS build

RUN apt-get update -y && apt-get install -y build-essential git
WORKDIR /app
RUN mix local.hex --force && mix local.rebar --force

ENV MIX_ENV=prod
COPY mix.exs mix.lock ./
RUN mix deps.get --only prod
RUN mkdir config
COPY config/config.exs config/prod.exs config/
RUN mix deps.compile

COPY lib lib
COPY priv priv
RUN mix compile

COPY config/runtime.exs config/
RUN mix release

FROM debian:bullseye-slim AS app
RUN apt-get update -y && apt-get install -y libstdc++6 openssl libncurses5 locales ca-certificates
RUN sed -i '/en_US.UTF-8/s/^# //g' /etc/locale.gen && locale-gen
ENV LANG=en_US.UTF-8

WORKDIR /app
RUN chown nobody /app
ENV MIX_ENV=prod

COPY --from=build --chown=nobody:root /app/_build/prod/rel/myapp ./
USER nobody

CMD ["/app/bin/server"]
```

---

## Top 10 Anti-Patterns (the most valuable section)

1. **Calling Ecto Repo directly from controllers/LiveViews.** Always go through a context module (`MyApp.Blog.create_post/1`), never `MyApp.Repo.insert/1` from the web layer. The context boundary is the single most important Phoenix convention — it keeps your web layer decoupled from your data layer and makes the business logic reusable (e.g., from a LiveView, a controller, a channel, a Mix task).

2. **Not using changesets for validation.** Changesets are Ecto's validation layer — they return either a valid changeset (ready for insert/update) or an invalid one (with errors). Don't validate in controllers, don't validate in LiveViews, don't validate with raw `if` statements. Always go through `Schema.changeset/2`.

3. **Blocking the LiveView process with slow work.** LiveView handlers (`handle_event/3`, `handle_params/3`) run in the LiveView process — a single BEAM process. If you do slow work (HTTP calls, complex computations) in a handler, the LiveView becomes unresponsive for that user. Offload to a `Task` (`Task.async/1` + `handle_info/2` for the result) or a GenServer.

4. **Using `Repo.all/1` for potentially large collections.** `Repo.all(Post)` loads every row into memory. Use pagination (`Repo.paginate/2` via `scrivener_ecto` or manual `limit/offset`), or use `Repo.stream/2` for processing large datasets without loading them all.

5. **N+1 queries via lazy association access.** `post.author.name` triggers a query if `:author` wasn't preloaded. Always `preload([:author, comments: :author])` in your context's list functions. Use `Ecto.Query.preload/2` — never access associations without preloading.

6. **Defensive programming (try/rescue everywhere).** Elixir's culture is "let it crash" — write happy-path code and let the supervision tree handle failures. If a `Repo.get!/1` raises `Ecto.NoResultsError`, that's usually the right behavior (returns 404 to the user). Don't wrap everything in `try/rescue` — that's a Java/Python habit that doesn't belong in Elixir.

7. **Using `cast/4` for fields that shouldn't be mass-assigned.** `cast(post, attrs, [:title, :body, :admin_flag])` lets users set `admin_flag` if it's in the attrs. Use `cast/4` only for user-settable fields; use `change/2` + `put_change/3` for server-set fields (like `admin_flag`, `view_count`).

8. **Not subscribing to PubSub in LiveView `mount/3`.** If a LiveView should react to real-time updates (e.g., new posts appear live), it must `Phoenix.PubSub.subscribe/2` in `mount/3` (guarded by `connected?(socket)` so dev mode doesn't subscribe twice). Without this, the LiveView is static.

9. **Ignoring `mix format`.** Elixir has a canonical formatter — `mix format` enforces a single style across the ecosystem. Configure it in `.formatter.exs`, run it on save (via editor integration), and enforce it in CI. Unformatted Elixir code is a code smell.

10. **Not using releases for production.** Running `mix phx.server` in production mixes dev and prod, doesn't compile optimizations, and requires Elixir installed on the server. Always build a release (`MIX_ENV=prod mix release`) — it's self-contained, precompiled, and starts in seconds. Releases also enable hot code reloading (no downtime deploys) — a BEAM feature no other ecosystem has.

---

## Cross-references

- `framework-templates` — CLAUDE.md generation template for Phoenix (project onboarding)
- `rails-8` — Ruby on Rails (Phoenix was created by a Rails core team member — similar MVC structure, but Phoenix is functional + BEAM-based, Rails is OO + MRI Ruby)
- `go-web` — Go web patterns (Go also has lightweight concurrency via goroutines, but no supervision tree, no LiveView equivalent)
- `django-6` — Python sync web framework (contrast: no real-time, no supervision tree, sync ORM)
- `api-and-interface-design` — Type contract design (relevant for context module APIs)
- `api-patterns` — REST API patterns (Phoenix controllers follow these)
- `security-and-hardening` — OWASP-aware hardening (Phoenix has CSRF + XSS protection built in)
- `clean-code` — General coding standards applicable to Elixir
- `testing-patterns` — Test pyramid, mocking strategies (ExUnit-specific syntax above; general principles there)
- `code-review-checklist` — 12-category code review checklist
- `git-workflow-and-versioning` — Branching/commit conventions for Elixir projects

---

## Dependencies

Required (installed via `mix phx.new`):
- **Elixir** 1.16+ (includes Mix build tool, IEx shell, ExUnit test framework)
- **Erlang/OTP** 26+ (the BEAM VM — bundled with Elixir installer)
- **Phoenix** 1.7+
- **Ecto** 3.11+ (data layer — wraps PostgreSQL via `postgrex`)
- **Phoenix LiveView** 0.20+ (real-time UI)
- **Phoenix HTML** 4+ (HTML helpers + HEEx)
- **Plug** 1.14+ (HTTP middleware — Phoenix is built on Plug)
- **Phoenix PubSub** 2+ (real-time pub/sub)

### Database

- **PostgreSQL** (default — install via `mix phx.new --database postgres`)
- **MySQL** (`mix phx.new --database mysql`)
- **SQLite3** (`mix phx.new --database sqlite3` — good for dev/embedded)
- **Ecto supports MSSQL, ClickHouse** via additional adapters

### Common additions (install via `mix deps.add` or edit `mix.exs`)

- `phoenix_live_reload` — auto-reload on file change (dev only)
- `credo` — linter (install: `mix archive.install hex credo`)
- `dialyxir` — static type checker via Dialyzer (install: `mix archive.install hex dialyxir`)
- `sobelow` — security scanner for Phoenix
- `ex_machina` — test factories (alternative to fixtures)
- `faker` — test data generation
- `mox` — mocks (when you need to mock external APIs)
- `broadway` — concurrent data processing pipelines (built on GenStage)
- `oban` — background jobs (PostgreSQL-backed — robust, no Redis needed)
- `finch` — HTTP client (modern, pooling)
- `tesla` — HTTP client with middleware (built on Finch or Hackney)
- `jason` — JSON encoding/decoding (the de facto standard)
- `timex` — date/time (richer than built-in `DateTime`)
- `ex_json_schema` — JSON schema validation
- `libcluster` — BEAM cluster formation (for multi-node apps)
- `horde` — distributed supervision tree (for clustered deployments)
- `nebulex` — distributed caching
