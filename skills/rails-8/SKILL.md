---
name: rails-8
description: "Ruby on Rails 8 (Ruby 3.2+) full-stack workflow skill. Covers Rails 8 new defaults: Solid Queue / Solid Cache / Solid Cable (Redis-free by default — backed by SQLite/Postgres/MySQL), Propshaft (replaces Sprockets), Kamal 2 (Docker-based deploys to any cloud), Thruster (Puma HTTP/2 proxy with TLS). MVC structure (Active Record models, controllers, ERB + Hotwire views), Active Record (migrations, validations, associations, callbacks — and when NOT to use callbacks), routing (resources, nested routes, member/collection, concerns), strong parameters, Hotwire (Turbo Drive for SPA-like nav without JS, Turbo Frames for partial page updates, Turbo Streams for server-pushed updates, Stimulus.js for light JS), Solid Queue (default) or Sidekiq for background jobs, Minitest (default) or RSpec for testing, Devise / bcrypt / has_secure_password for auth, Action Text for rich text, Action Mailer, Active Storage for file uploads. Use when building any Ruby web app on Rails 8 — especially when the task involves migrations, Active Record queries, Hotwire/Turbo, background jobs, or Kamal deployment where idiomatic Rails differs from generic Ruby or from other web frameworks."
license: Proprietary. LICENSE.txt has complete terms
---

# Ruby on Rails 8 — Full-Stack Ruby Workflow Skill

> **Target:** Rails 8.x (released November 2024) on Ruby 3.2+. Rails 8 ships with **Redis-free defaults**: Solid Queue (background jobs), Solid Cache (fragment caching), Solid Cable (WebSocket) all use your primary database (SQLite/Postgres/MySQL) instead of Redis. Propshaft replaces Sprockets for asset management. Kamal 2 is the default deploy tool (Docker-based, deploys to any cloud). Thruster is the default Puma HTTP/2 proxy with automatic TLS via Let's Encrypt.

## When to Use This Skill

Use this skill whenever the user is building, debugging, or extending a Rails 8 application. Trigger phrases include "Rails", "Ruby on Rails", "Active Record", "Bundler", "Gemfile", "rake", "rails generate", "rails server", "Hotwire", "Turbo", "Stimulus", "Solid Queue", "Kamal", "Devise", "RSpec", "Minitest", and any reference to a `app/models/`, `app/controllers/`, `app/views/`, `config/routes.rb`, `db/migrate/`, or `Gemfile` file structure.

Do **not** use this skill for:
- **Rails ≤7** — Solid Queue/Cache/Cable, Propshaft, Kamal 2 defaults, and Thruster are Rails 8+ only. Some patterns here require Rails 8.
- **Sinatra / Hanami / Roda** — different Ruby web frameworks with different conventions.
- **Plain Ruby** (scripts, CLIs, no web framework) — use general Ruby patterns instead.
- **Laravel / Django** — different languages and frameworks. See `laravel-12` and `django-6` skills.

Cross-reference: `framework-templates` has a Rails section; this skill goes deep.

## Quick Start

```bash
# Install Rails 8 (if not already installed)
gem install rails -v 8.0.0

# Create a new project
rails new myapp
# Rails 8 defaults: SQLite (dev), Solid Queue/Cache/Cable, Propshaft, Kamal 2, Thruster
# Prompts: Tailwind CSS? (Y), Devise? (N default), RuboCop? (Y), Brakeman? (Y)

cd myapp
bin/rails server                  # Dev server at http://127.0.0.1:3000

# Generate a scaffold (model + migration + controller + views + tests)
bin/rails generate scaffold Post title:string body:text status:string
bin/rails db:migrate              # Run the migration

# Open the Rails console (REPL with app booted)
bin/rails console                 # or: bin/rails c
```

### Key commands (the `bin/rails` prefix is preferred over plain `rails`)

```bash
bin/rails server                  # Start dev server (alias: bin/rails s)
bin/rails console                 # REPL with app booted (alias: bin/rails c)
bin/rails dbconsole               # DB client (alias: bin/rails db)
bin/rails generate <generator>    # Codegen (alias: bin/rails g)
bin/rails db:migrate              # Run pending migrations
bin/rails db:rollback             # Roll back last migration
bin/rails db:seed                 # Run db/seeds.rb
bin/rails db:reset                # Drop, create, migrate, seed (DESTRUCTIVE)
bin/rails test                    # Run Minitest suite
bin/rails routes                  # List all routes
bin/rails about                   # Show app info
bin/rails stats                   # Code statistics
bin/rails credentials:edit       # Edit encrypted credentials
bin/rails db:prepare              # Migrate + seed (safe for CI/CD — won't drop)
```

---

## Project Structure (Rails 8 canonical layout)

Rails is **convention-over-configuration** — the directory structure IS the framework. Files must live where Rails expects them or the autoloader won't find them.

```
myapp/
├── app/
│   ├── models/                   # Active Record models (app/models/post.rb → class Post)
│   ├── controllers/              # Controllers (app/controllers/posts_controller.rb → PostsController)
│   ├── views/                    # ERB templates (app/views/posts/index.html.erb)
│   ├── helpers/                  # View helpers (rarely used in modern Rails)
│   ├── jobs/                     # Active Job / Solid Queue jobs (app/jobs/process_podcast.rb)
│   ├── mailers/                  # Action Mailer classes (app/mailers/user_mailer.rb)
│   ├── channels/                 # Action Cable channels (WebSocket)
│   ├── javascript/               # JS bundled by importmap / esbuild / bundler
│   │   ├── controllers/          # Stimulus controllers (auto-loaded)
│   │   └── application.js        # JS entry point
│   ├── assets/                   # CSS, images, fonts (Propshaft serves these)
│   │   ├── stylesheets/
│   │   └── images/
│   └── components/               # ViewComponent components (optional — gem required)
├── config/
│   ├── routes.rb                 # ← THE routing file
│   ├── database.yml              # DB config (SQLite dev, Postgres/MySQL prod)
│   ├── storage.yml               # Active Storage / Solid Queue / Solid Cache config
│   ├── environments/             # Per-env config (development.rb, production.rb, test.rb)
│   ├── importmap.rb              # JS import map (default in Rails 8)
│   ├── puma.rb                   # Puma server config
│   ├── deploy.yml                # ← NEW in Rails 8: Kamal 2 config
│   └── credentials.yml.enc       # Encrypted secrets (edited via bin/rails credentials:edit)
├── db/
│   ├── migrate/                  # Migration files (timestamped)
│   ├── schema.rb                 # Auto-generated current schema (DO NOT EDIT)
│   ├── seeds.rb                  # Seed data
│   └── cable.schema.rb           # ← NEW: Solid Cable schema
│   └── queue.schema.rb           # ← NEW: Solid Queue schema
│   └── cache.schema.rb           # ← NEW: Solid Cache schema
├── public/                       # Static files served as-is (404.html, 500.html, robots.txt)
├── test/                         # Minitest tests (default)
│   ├── models/
│   ├── controllers/
│   ├── system/                   # System tests (Capybara + Puma)
│   └── fixtures/                 # Test data (YAML)
├── bin/                          # Executables (rails, rake, puma, etc.)
├── lib/                          # Project-specific libraries
├── Gemfile                       # Ruby gem dependencies
├── Gemfile.lock                  # Locked gem versions
├── config.ru                     # Rack entry point
└── Rakefile                      # Rake task entry point
```

### Autoloader: Zeitwerk (the implicit contract)

Rails 8 uses Zeitwerk for autoloading. The contract: **file path = constant name**.

| File path | Constant |
|---|---|
| `app/models/post.rb` | `Post` |
| `app/models/blog/comment.rb` | `Blog::Comment` |
| `app/controllers/posts_controller.rb` | `PostsController` |
| `app/jobs/process_podcast_job.rb` | `ProcessPodcastJob` |

If you create a file without the matching constant (or vice versa), Zeitwerk throws an error at boot. Always name files to match constants exactly.

---

## Core Mental Model: Convention-over-Configuration + Active Record + Hotwire

Rails' distinctive paradigm is **opinionated defaults that make most decisions for you**. Three things differentiate Rails from other frameworks:

### 1. Active Record is the model AND the data access layer

Each model class **is** its database table. A `Post` instance maps directly to a `posts` table row. There is no separate repository, entity manager, or mapper. The model handles persistence, validations, associations, and callbacks all in one class.

```ruby
# app/models/post.rb
class Post < ApplicationRecord
  # Validations
  validates :title, presence: true, length: { minimum: 3, maximum: 200 }
  validates :slug, presence: true, uniqueness: true

  # Associations
  belongs_to :author, class_name: "User", foreign_key: :user_id
  has_many :comments, dependent: :destroy
  has_many :tags, through: :post_tags
  has_one :featured_image, dependent: :destroy
  has_many_attached :images   # Active Storage

  # Scopes (reusable query fragments)
  scope :published, -> { where(status: "published").where.not(published_at: nil) }
  scope :recent, -> { order(created_at: :desc) }
  scope :by_author, ->(user) { where(author: user) }

  # Callbacks (use sparingly — see anti-patterns)
  before_save :generate_slug
  after_create :notify_subscribers

  # Enum
  enum status: { draft: 0, published: 1, archived: 2 }

  # Class methods
  def self.search(query)
    where("title ILIKE ? OR body ILIKE ?", "%#{query}%", "%#{query}%")
  end

  private

  def generate_slug
    self.slug ||= title.parameterize
  end

  def notify_subscribers
    PostNotificationJob.perform_later(id)
  end
end
```

### 2. Convention-over-Configuration means sensible defaults everywhere

Rails infers almost everything from naming:
- `Post` model → `posts` table (pluralized)
- `PostsController` → `app/controllers/posts_controller.rb`, routes to `/posts`
- `app/views/posts/index.html.erb` → rendered by `PostsController#index`
- `user_id` foreign key → `belongs_to :user` / `has_many :posts`
- `created_at` / `updated_at` columns → auto-managed timestamps

You only specify when you deviate from convention. The configuration is the exception, not the rule.

### 3. Hotwire replaces the SPA pattern for most apps

Rails 8's default frontend is **Hotwire**: Turbo Drive (SPA-like navigation without writing JS), Turbo Frames (partial page updates), Turbo Streams (server-pushed updates over WebSocket/SSE), and Stimulus.js (lightweight JS for behavior). You can build complex reactive apps without React, Vue, or a separate frontend codebase.

```erb
<!-- app/views/posts/show.html.erb -->
<%= turbo_frame_tag dom_id(@post) do %>
  <h1><%= @post.title %></h1>
  <p><%= @post.body %></p>

  <%= link_to "Edit", edit_post_path(@post), data: { turbo_frame: dom_id(@post) } %>
<% end %>

<!-- Clicking "Edit" fetches the edit form and swaps it into the frame — no full page reload, no JS -->
```

---

## Routing (`config/routes.rb`)

Rails routing is **resource-oriented**. The `resources` macro generates 7 RESTful routes at once.

```ruby
# config/routes.rb
Rails.application.routes.draw do
  root "posts#index"

  # 7 RESTful routes: index, new, create, show, edit, update, destroy
  resources :posts

  # Nested resources
  resources :posts do
    resources :comments, only: [:create, :destroy]
    member do
      patch :publish        # /posts/:id/publish
    end
    collection do
      get :search           # /posts/search
    end
  end

  # Shallow nesting (avoids deeply-nested URLs like /posts/1/comments/2)
  resources :posts, shallow: true do
    resources :comments     # /posts/1/comments (create) but /comments/2 (show/edit/destroy)
  end

  # Route concerns (reusable route groups)
  concern :commentable do
    resources :comments, only: [:create, :destroy]
  end

  resources :posts, concerns: [:commentable]
  resources :photos, concerns: [:commentable]

  # Named routes
  get "about", to: "pages#about", as: :about
  # about_path → "/about", about_url → "http://host/about"

  # Member vs Collection
  # member:    /posts/:id/publish
  # collection: /posts/search
end
```

```bash
bin/rails routes                  # List all routes
bin/rails routes -g posts         # Filter routes matching "posts"
bin/rails routes -c posts         # Filter by controller
```

### Route helpers (auto-generated)

| Route definition | Path helper | URL helper |
|---|---|---|
| `resources :posts` | `posts_path` | `posts_url` |
| `resources :posts` | `new_post_path` | `new_post_url` |
| `resources :posts` | `edit_post_path(@post)` | `edit_post_url(@post)` |
| `resources :posts` | `post_path(@post)` | `post_url(@post)` |
| `get "about", as: :about` | `about_path` | `about_url` |

Always use helpers, never hardcode paths. If you change a route, helpers update automatically; hardcoded paths don't.

---

## Active Record (the ORM)

### Migrations: write Ruby, not SQL

```bash
bin/rails generate migration CreatePosts title:string body:text
# OR via scaffold (generates migration + model + controller + views + tests):
bin/rails generate scaffold Post title:string body:text status:string
```

```ruby
# db/migrate/20250115000000_create_posts.rb
class CreatePosts < ActiveRecord::Migration[8.0]
  def change
    create_table :posts do |t|
      t.string :title, null: false
      t.text :body, null: false, default: ""
      t.string :status, null: false, default: "draft"
      t.string :slug, null: false
      t.references :user, null: false, foreign_key: true  # user_id FK
      t.datetime :published_at

      t.timestamps  # created_at, updated_at
    end

    add_index :posts, :slug, unique: true
    add_index :posts, [:status, :published_at]  # Composite index
    add_index :posts, :title, using: :gin    # PostgreSQL GIN index (for trigram search)
  end
end
```

```bash
bin/rails db:migrate              # Run pending migrations
bin/rails db:rollback             # Roll back the last migration
bin/rails db:rollback STEP=3      # Roll back 3 migrations
bin/rails db:migrate:status       # See which migrations have run
bin/rails db:schema:load          # Load schema.rb into a fresh DB (faster than migrating)
```

### Querying: chainable, lazy

```ruby
# Queries are NOT executed until you call .to_a, .each, .first, .count, etc.
posts = Post.where(status: "published").order(created_at: :desc).limit(10)
# No DB hit yet
posts = posts.where("published_at > ?", 1.week.ago)
# Still no DB hit
posts.each { |p| puts p.title }   # ← NOW it executes

# Find by ID
Post.find(1)                       # Raises ActiveRecord::RecordNotFound if missing
Post.find_by(id: 1)                # Returns nil if missing
Post.find_by!(slug: "hello-world") # Raises if missing

# Where
Post.where(status: "published")
Post.where("published_at > ?", 1.week.ago)
Post.where(status: ["draft", "published"])  # IN clause
Post.where.not(status: "archived")

# Order, limit, offset
Post.order(created_at: :desc).limit(10).offset(20)

# Joins and includes (avoid N+1)
Post.includes(:author, :comments).limit(10)   # Eager load (2-3 queries, not N+1)
Post.joins(:author).where(users: { active: true })  # INNER JOIN
Post.left_joins(:comments).where(comments: { id: nil })  # LEFT JOIN

# Aggregations
Post.count
Post.where(status: "published").count
Post.average(:view_count)
Post.group(:status).count  # { "draft" => 5, "published" => 20, "archived" => 3 }
Post.maximum(:published_at)

# Scopes (reusable query fragments)
Post.published.recent.limit(10)
Post.by_author(current_user).published
```

### Avoiding N+1 queries (the #1 Rails performance bug)

```ruby
# ❌ N+1: 1 query for posts + N queries for authors
Post.all.each { |p| puts p.author.name }   # Author query per post

# ✅ Eager load: 2 queries total
Post.includes(:author).each { |p| puts p.author.name }

# ✅ Eager load nested associations
Post.includes(author: :profile, comments: :user).each do |p|
  puts p.author.profile.bio
  p.comments.each { |c| puts c.user.name }
end

# ✅ Use Bullet gem in dev to detect N+1
# gem 'bullet', group: :development
```

---

## Controllers

```ruby
# app/controllers/posts_controller.rb
class PostsController < ApplicationController
  before_action :authenticate_user!         # Devise (if installed)
  before_action :set_post, only: [:show, :edit, :update, :destroy]
  before_action :authorize_user!, only: [:edit, :update, :destroy]

  def index
    @posts = Post.published.recent.page(params[:page]).per(15)
  end

  def show
    # @post set by set_post
  end

  def new
    @post = Post.new
  end

  def create
    @post = current_user.posts.build(post_params)

    if @post.save
      redirect_to @post, notice: "Post created successfully."
    else
      render :new, status: :unprocessable_entity  # 422 — required for Turbo
    end
  end

  def edit
    # @post set by set_post
  end

  def update
    if @post.update(post_params)
      redirect_to @post, notice: "Post updated."
    else
      render :edit, status: :unprocessable_entity
    end
  end

  def destroy
    @post.destroy
    redirect_to posts_path, notice: "Post deleted."
  end

  private

  def set_post
    @post = Post.find(params[:id])
  end

  def post_params
    # Strong parameters — only permit these fields through
    params.require(:post).permit(:title, :body, :status, :published_at)
  end

  def authorize_user!
    head :forbidden unless @post.author == current_user
  end
end
```

### Strong parameters (security: never trust params from the wild)

```ruby
# Whitelist permitted fields
params.require(:post).permit(:title, :body, :status)

# Nested params
params.require(:post).permit(:title, comments_attributes: [:id, :body, :_destroy])

# Permit all scalar fields (last resort — discouraged)
params.require(:post).permit!
```

---

## Views: ERB + Hotwire

### ERB templates

```erb
<!-- app/views/posts/index.html.erb -->
<h1>Posts</h1>

<%= link_to "New Post", new_post_path, class: "btn btn-primary", data: { turbo_frame: "modal" } %>

<ul class="posts">
  <% @posts.each do |post| %>
    <li>
      <%= link_to post.title, post, data: { turbo_frame: "_top" } %>
      <span class="meta"><%= time_ago_in_words(post.published_at) %> ago</span>
    </li>
  <% end %>
</ul>

<%= paginate @posts %>  # Via kaminari or pagy gem
```

### Partials (reusable view fragments)

```erb
<!-- app/views/posts/_post.html.erb -->
<article class="post">
  <h2><%= link_to post.title, post %></h2>
  <p><%= truncate(post.body, length: 200) %></p>
  <footer>By <%= post.author.name %></footer>
</article>

<!-- Usage in another template -->
<%= render @posts %>            <!-- Auto-renders _post.html.erb for each post -->
<%= render partial: "post", locals: { post: @featured_post } %>
```

### Turbo Frames (partial page updates without JS)

```erb
<!-- app/views/posts/show.html.erb -->
<h1>Posts</h1>

<%= turbo_frame_tag dom_id(@post) do %>
  <h2><%= @post.title %></h2>
  <p><%= @post.body %></p>
  <%= link_to "Edit", edit_post_path(@post) %>
<% end %>

<!-- app/views/posts/edit.html.erb -->
<%= turbo_frame_tag dom_id(@post) do %>
  <%= form_with model: @post do |f| %>
    <%= f.text_field :title %>
    <%= f.text_area :body %>
    <%= f.submit "Save" %>
  <% end %>
<% end %>
```

Clicking "Edit" fetches the edit form and swaps it into the frame — **no full page reload, no JavaScript written by you**. Submitting the form updates the post and the frame swaps back to the show view.

### Turbo Streams (server-pushed updates over WebSocket)

```ruby
# app/controllers/posts_controller.rb
def create
  @post = current_user.posts.build(post_params)

  respond_to do |format|
    if @post.save
      format.html { redirect_to @post, notice: "Post created." }
      format.turbo_stream  # Renders create.turbo_stream.erb
    else
      format.html { render :new, status: :unprocessable_entity }
      format.turbo_stream { render :new, status: :unprocessable_entity }
    end
  end
end
```

```erb
<!-- app/views/posts/create.turbo_stream.erb -->
<%= turbo_stream.append "posts", partial: "posts/post", locals: { post: @post } %>
<%= turbo_stream.replace "new_post", "" %>
<%= turbo_stream.update "post_count", Post.count %>
```

Turbo Streams let the server push DOM updates to all connected clients (via Action Cable / Solid Cable) — great for real-time feeds, live updates, collaborative editing.

### Stimulus.js (lightweight JS for behavior)

```html
<!-- app/javascript/controllers/clipboard_controller.js -->
import { Controller } from "@hotwired/stimulus"

export default class extends Controller {
  static targets = ["source"]
  static classes = ["supported"]

  connect() {
    if (navigator.clipboard) {
      this.element.classList.add(this.supportedClass)
    }
  }

  copy(event) {
    event.preventDefault()
    navigator.clipboard.writeText(this.sourceTarget.value)
  }
}
```

```erb
<div data-controller="clipboard" data-clipboard-supported-class="clipboard--supported">
  <input type="text" value="Hello" data-clipboard-target="source" readonly>
  <button data-action="click->clipboard#copy">Copy</button>
</div>
```

Stimulus is the Rails answer to "I need a little JS for this widget". Use it instead of pulling in React/Vue for small interactions.

---

## Background Jobs (Solid Queue — Rails 8 default)

Rails 8 ships with **Solid Queue**, a database-backed job queue. No Redis required. For high-throughput production, you may switch to Sidekiq, but Solid Queue is sufficient for most apps.

```bash
bin/rails generate job ProcessPodcast
```

```ruby
# app/jobs/process_podcast_job.rb
class ProcessPodcastJob < ApplicationJob
  queue_as :default
  # Or: queue_as :audio (named queue)

  retry_on StandardError, wait: 30.seconds, attempts: 3
  discard_on ActiveJob::DeserializationError  # Don't retry if record was deleted

  def perform(podcast)
    processor = AudioProcessor.new
    processor.process(podcast)

    PodcastChannel.broadcast_to(podcast, {
      action: "processed",
      id: podcast.id
    })
  end
end

# Dispatch:
ProcessPodcastJob.perform_later(podcast)
ProcessPodcastJob.set(wait: 5.minutes).perform_later(podcast)
ProcessPodcastJob.set(queue: :high_priority).perform_later(podcast)
```

```bash
# Run the worker (production — use systemd or Kamal)
bin/jobs                # Solid Queue worker (Rails 8 default)
# OR with Sidekiq:
bundle exec sidekiq     # Sidekiq worker (if you've replaced Solid Queue)

# Monitor (Solid Queue has a built-in UI at /jobs if you mount it)
```

### Solid Queue config (database-backed)

Solid Queue uses your primary database. Migrations are auto-generated when you install it:

```bash
bin/rails solid_queue:install
bin/rails db:migrate
```

This creates `solid_queue_jobs`, `solid_queue_recurring_tasks`, etc. tables. No Redis needed.

---

## Testing (Minitest default, RSpec optional)

Rails 8 ships with **Minitest** as the default. RSpec is the popular alternative — install via `rspec-rails` gem if preferred.

### Minitest (default)

```ruby
# test/models/post_test.rb
require "test_helper"

class PostTest < ActiveSupport::TestCase
  # Fixtures (test data) auto-loaded from test/fixtures/posts.yml

  test "should not save post without title" do
    post = Post.new(body: "Hello")
    assert_not post.valid?
    assert_includes post.errors[:title], "can't be blank"
  end

  test "published scope returns only published posts" do
    published = posts(:one)  # From fixture
    published.update!(status: "published", published_at: Time.current)

    assert_includes Post.published, published
    assert_not_includes Post.published, posts(:draft)
  end
end

# test/controllers/posts_controller_test.rb
class PostsControllerTest < ActionDispatch::IntegrationTest
  test "should get index" do
    get posts_url
    assert_response :success
  end

  test "should create post when logged in" do
    sign_in users(:alice)  # Devise test helper
    post posts_url, params: { post: { title: "New", body: "Body" } }
    assert_redirected_to post_url(Post.last)
  end
end

# test/system/posts_test.rb (system test — Capybara + Puma)
class PostsTest < ApplicationSystemTestCase
  driven_by :selenium, using: :headless_chrome

  test "visiting posts index" do
    visit posts_url
    assert_selector "h1", text: "Posts"
  end
end
```

```bash
bin/rails test                    # Run all tests
bin/rails test test/models        # Run a directory
bin/rails test test/models/post_test.rb  # Run one file
bin/rails test test/models/post_test.rb:10  # Run one test (line 10)
bin/rails test:system             # Run system tests (slower — needs browser)
```

### RSpec (alternative)

```bash
# Gemfile
group :development, :test do
  gem 'rspec-rails'
end

bin/rails generate rspec:install
bin/rails spec                    # Run RSpec suite
```

Cross-reference: `testing-patterns` for general test pyramid / mocking strategies.

---

## Authentication

### Three auth surfaces (pick one)

| Option | Use |
|---|---|
| **`has_secure_password`** (built-in) | Simple email/password. Adds `password_digest`, `password`, `password_confirmation`. Use bcrypt gem. |
| **Devise** | Full auth solution: confirmable, recoverable, registerable, lockable, timeoutable, omniauthable. Industry standard for Rails. |
| **Authlogic / Clearance** | Lighter alternatives to Devise. |

### `has_secure_password` (built-in, minimal)

```ruby
# Gemfile
gem 'bcrypt'

# db/migrate
class AddPasswordDigestToUsers < ActiveRecord::Migration[8.0]
  def change
    add_column :users, :password_digest, :string
  end
end

# app/models/user.rb
class User < ApplicationRecord
  has_secure_password  # Adds password, password_confirmation, authenticate

  validates :email, presence: true, uniqueness: true
end

# Usage
user = User.create!(email: "alice@example.com", password: "secret123")
user.authenticate("wrong")   # → false
user.authenticate("secret123") # → user
```

### Devise (full-featured)

```bash
# Gemfile
gem 'devise'

bin/rails generate devise:install
bin/rails generate devise User
bin/rails db:migrate
```

```ruby
# app/controllers/application_controller.rb
class ApplicationController < ActionController::Base
  before_action :authenticate_user!  # Require login for all controllers

  # Permit additional fields in sign-up form
  before_action :configure_permitted_parameters, if: :devise_controller?

  private

  def configure_permitted_parameters
    devise_parameter_sanitizer.permit(:sign_up, keys: [:name])
    devise_parameter_sanitizer.permit(:account_update, keys: [:name])
  end
end

# In views
<% if user_signed_in? %>
  Hello, <%= current_user.email %>
  <%= button_to "Sign out", destroy_user_session_path, method: :delete %>
<% else %>
  <%= link_to "Sign in", new_user_session_path %>
<% end %>
```

---

## Deployment: Kamal 2 (Rails 8 default)

Rails 8 ships with **Kamal 2**, a Docker-based deploy tool that pushes your app to any cloud server (AWS, DigitalOcean, Hetzner, your own VPS). No PaaS lock-in.

```bash
# Initial setup (creates config/deploy.yml)
bin/rails kamal:setup

# Deploy
kamal deploy

# Roll back to previous version
kamal app rollback

# Run a command on the server
kamal app exec "bin/rails console"

# Tail logs
kamal app logs -f
```

```yaml
# config/deploy.yml
service: myapp
image: myuser/myapp

servers:
  web:
    hosts:
      - 203.0.113.10
    options:
      network: "private"
  job:
    hosts:
      - 203.0.113.10
    cmd: bin/jobs

# Environment variables (set via kamal env push)
env:
  clear:
    DB_HOST: 10.0.0.2
    RAILS_SERVE_STATIC_FILES: true
  secret:
    - RAILS_MASTER_KEY
    - DATABASE_URL

# Asset/registry config
registry:
  server: ghcr.io
  username: myuser
  password:
    - KAMAL_REGISTRY_PASSWORD

# Traefik (default reverse proxy) config
traefik:
  options:
    publish:
      - "443:443"
    volume:
      - "/letsencrypt:/letsencrypt"
  args:
    entryPoints.web.address: ":80"
    entryPoints.websecure.address: ":443"
    certificatesResolvers.letsencrypt.acme.email: "you@example.com"
    certificatesResolvers.letsencrypt.acme.storage: "/letsencrypt/acme.json"
    certificatesResolvers.letsencrypt.acme.httpchallenge: true
    certificatesResolvers.letsencrypt.acme.httpchallenge.entrypoint: "web"
```

Kamal 2 builds a Docker image, pushes it to your registry, SSHes to your servers, pulls the image, starts new containers, waits for health checks, then switches traffic — zero-downtime. It also handles rolling back, running jobs, and SSH-ing into containers.

### Thruster (Rails 8 default HTTP/2 proxy)

Rails 8 includes **Thruster** — a lightweight HTTP/2 proxy that runs in front of Puma and handles:
- HTTP/2 with multiplexing
- Automatic TLS via Let's Encrypt (with ACME challenge)
- HTTP/1.1 to HTTP/2 upgrade
- Static file serving (faster than Puma for assets)

You don't configure Thruster — it just runs. `bin/rails server` starts Puma with Thruster in front automatically in production. For dev, it's skipped.

---

## Top 10 Anti-Patterns (the most valuable section)

1. **Fat controllers.** Controllers should be ~10-20 lines: set instance variables, call a model method, redirect/render. Business logic goes in models (or service objects in `app/services/`). The Rails mantra is "fat model, skinny controller" — but if a model gets too fat, extract service objects.

2. **N+1 queries.** Always use `.includes()` for associations you'll access. Install the `bullet` gem in development to get loud warnings when N+1 queries occur. This is the #1 Rails performance bug.

3. **Callbacks for cross-model side effects.** `after_create :send_welcome_email` is fine. `after_create :update_organization_stats` is not — it creates hidden coupling and makes testing painful. Use service objects or explicit method calls instead. **Rule of thumb:** if the callback touches another model, extract it.

4. **Using `update_all` / `delete_all` to skip callbacks.** These methods bypass validations AND callbacks. If you need to skip callbacks, do it explicitly with `update_columns` (skips callbacks) and document why. Don't reach for `update_all` as a default — it skips validations too.

5. **Hardcoding secrets in source.** Use `bin/rails credentials:edit` (encrypted `config/credentials.yml.enc`) or environment variables (`ENV.fetch("STRIPE_SECRET_KEY")`). The `RAILS_MASTER_KEY` decrypts credentials — keep it OUT of git (it's in `.gitignore` by default).

6. **Skipping `db:schema:load` in favor of `db:migrate` for fresh setups.** When setting up a new environment (CI, new dev machine), `db:schema:load` is faster than running every migration from the project's history. `db:migrate` is for incremental changes; `db:schema:load` is for fresh setups. Never run `db:migrate` on a fresh DB unless you have a specific reason.

7. **Using `User.all` and iterating in memory.** `User.all.each` loads every user into memory. Use `User.find_each` (batches of 1000 by default) for any operation that might touch many records: `User.find_each { |u| u.do_something }`.

8. **Not returning `status: :unprocessable_entity` on validation failures.** Turbo expects a 422 status when a form submission has validation errors. Without it, Turbo doesn't know to re-render the form with errors. Always: `render :new, status: :unprocessable_entity`.

9. **Using `before_action` for business logic.** `before_action` is for setup (loading a record, checking auth) — not for executing business logic. If your `before_action` does complex work, move it into a service object called from the controller action itself.

10. **Forgetting to add indexes for foreign keys.** Rails 5+ auto-creates indexes for `t.references` (foreign keys), but if you add a FK manually via `add_column :posts, :user_id, :integer`, you must add the index yourself: `add_index :posts, :user_id`. Unindexed foreign keys cause slow JOINs and full table scans.

---

## Cross-references

- `framework-templates` — CLAUDE.md generation template for Rails (project onboarding)
- `laravel-12` — PHP framework with similar Active Record ORM (compare patterns)
- `django-6` — Python framework with different ORM (Data Mapper-ish via Django ORM)
- `api-and-interface-design` — Type contract design (relevant for Rails API controllers)
- `api-patterns` — REST API patterns (Rails `resources` macro generates these automatically)
- `security-and-hardening` — OWASP-aware hardening (Rails has CSRF, XSS, SQL injection protection built in via strong params + ERB escaping)
- `clean-code` — General coding standards applicable to Ruby
- `testing-patterns` — Test pyramid, mocking strategies (Rails-specific syntax above; general principles there)
- `code-review-checklist` — 12-category code review checklist
- `git-workflow-and-versioning` — Branching/commit conventions for Rails projects

---

## Dependencies

Required (installed by `rails new`):
- **Ruby** 3.2+ (Rails 8 minimum)
- **Rails** 8.x
- **Bundler** 2.x (gem dependency manager)
- **Puma** 6+ (web server — Rails default)
- **Thruster** (HTTP/2 proxy with auto-TLS — Rails 8 default)
- **Propshaft** (asset pipeline — Rails 8 default, replaces Sprockets)
- **Solid Queue** (background jobs — Rails 8 default, replaces Sidekiq/Redis requirement)
- **Solid Cache** (fragment caching — Rails 8 default)
- **Solid Cable** (WebSocket — Rails 8 default)
- **Kamal 2** (deploy tool — Rails 8 default)
- **SQLite** 3.39+ (default dev database; Rails 8 enables WAL mode and better concurrent reads)

Common additions (install on demand):
- **Devise** (`gem 'devise'`) — full-featured auth
- **bcrypt** (`gem 'bcrypt'`) — for `has_secure_password` (lighter alternative to Devise)
- **Sidekiq** (`gem 'sidekiq'`) — Redis-based job queue (replaces Solid Queue for high throughput)
- **RSpec Rails** (`gem 'rspec-rails'`) — alternative test framework
- **Factory Bot Rails** (`gem 'factory_bot_rails'`) — test data factories (alternative to fixtures)
- **Bullet** (`gem 'bullet', group: :development`) — N+1 query detection
- **Brakeman** (`gem 'brakeman', group: :development`) — security scanner
- **RuboCop Rails** (`gem 'rubocop-rails', group: :development`) — linter
- **Pagy** (`gem 'pagy'`) — pagination (faster than kaminari)
- **Draper** (`gem 'draper'`) — decorators (alternative to view helpers)
- **Active Model Serializers** or **jsonapi-serializer** — JSON API serialization
- **ViewComponent** (`gem 'view_component'`) — reusable view components (alternative to partials)
- **Hotwire / Turbo / Stimulus** — included by default in Rails 8
- **PostgreSQL adapter** (`gem 'pg'`) — for Postgres production
- **MySQL adapter** (`gem 'mysql2'`) — for MySQL production
