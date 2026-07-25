---
name: laravel-12
description: "Laravel 12 (PHP 8.3+) full-stack workflow skill. Covers the streamlined 11+/12 app structure (no Kernel.php, bootstrap/app.php config), Eloquent ORM with factories/seeders, Artisan CLI, Blade + Livewire + Inertia frontend options, Sanctum API tokens, Breeze/Jetstream auth scaffolding, Queues with Redis/database, Pest testing, Vite asset build, Filament admin, Forge/Vapor deployment. Use when building any PHP web application, API, or console workload on Laravel 12 — especially when the task involves migrations, Eloquent queries, queued jobs, or auth flows where idiomatic Laravel differs from generic PHP patterns."
license: Proprietary. LICENSE.txt has complete terms
---

# Laravel 12 — Full-Stack PHP Workflow Skill

> **Target:** Laravel 12.x on PHP 8.3+. The streamlined app structure introduced in Laravel 11 is assumed throughout (no `app/Console/Kernel.php`, no `app/Http/Kernel.php`, no `app/Exceptions/Handler.php` — all configuration lives in `bootstrap/app.php`).

## When to Use This Skill

Use this skill whenever the user is building, debugging, or extending a Laravel 12 application. Trigger phrases include "Laravel", "PHP artisan", "Eloquent", "Composer require", "Blade template", "Livewire", "Filament admin", "Breeze", "Jetstream", "Sanctum", and any reference to a `routes/web.php`, `app/Models`, or `database/migrations` directory layout.

Do **not** use this skill for:
- Legacy Laravel ≤10 projects with the old Kernel.php structure — patterns here may not apply
- Pure PHP projects without Laravel (use generic PHP patterns instead)
- Other PHP frameworks (Symfony, CodeIgniter, Yii — different conventions)

## Quick Start

```bash
# Create a new project (two equivalent paths)
composer create-project laravel/laravel my-app
# OR via the Laravel installer (preferred — interactive prompts for starter kit, DB, etc.)
laravel new my-app

cd my-app
php artisan serve              # Dev server at http://127.0.0.1:8000
# OR use Herd (macOS) / Sail (Docker) / Valet (macOS) for local dev
```

### Starter kits (pick one at project creation)

| Starter kit | Use when |
|---|---|
| **Laravel Breeze** | Simple auth scaffolding (login, register, password reset). Blade + Tailwind, or Inertia + Vue/React/Svelte variants. Default choice. |
| **Laravel Jetstream** | Teams, 2FA, profile management, API tokens. Heavier. Comes in Livewire or Inertia flavors. |
| **Filament Starter** | Admin-heavy app — Filament is a TALL-stack admin panel that generates CRUD from models. |
| **None** | API-only project (no Blade/UI) — pair with Sanctum for token auth. |

### First-time setup after create

```bash
php artisan key:generate        # Generate APP_KEY in .env
php artisan migrate             # Run default migrations (users, password_reset_tokens, sessions, cache, jobs)
php artisan storage:link        # Symlink public/storage -> storage/app/public (for user-uploaded files)
npm install && npm run dev      # Build frontend assets via Vite (runs in background)
```

---

## Project Structure (Laravel 11+/12 streamlined layout)

```
my-app/
├── app/
│   ├── Models/                 # Eloquent models (Active Record)
│   ├── Http/
│   │   ├── Controllers/        # Route controllers
│   │   ├── Middleware/         # Custom middleware (rare — most is framework-provided)
│   │   └── Requests/           # Form Requests (validation + auth)
│   ├── Services/               # YOUR business logic goes here (not in controllers)
│   ├── Actions/                # Single-purpose action classes (alternative to Services)
│   ├── Events/                 # Events for decoupling
│   ├── Listeners/              # Event listeners (queued or sync)
│   ├── Jobs/                   # Queued jobs (async work)
│   ├── Mail/                   # Mailable classes
│   ├── Notifications/          # Notification classes (multi-channel)
│   ├── Policies/               # Authorization policies (model-level permissions)
│   ├── Providers/
│   │   └── AppServiceProvider.php  # Service container bindings, custom config
│   └── Console/
│       └── Commands/           # Custom Artisan commands (php artisan my:command)
├── bootstrap/
│   └── app.php                 # ← THE config file (replaces Kernel.php + Handler.php)
├── config/                     # Framework config (database, queue, cache, mail, etc.)
├── database/
│   ├── migrations/             # Schema changes (write PHP, not SQL)
│   ├── factories/              # Model factories (test data generation)
│   └── seeders/                # Database seeders (DatabaseSeeder.php is the entry point)
├── public/                     # Web root (index.php, compiled assets, .htaccess)
├── resources/
│   ├── views/                  # Blade templates (.blade.php)
│   ├── js/                     # Frontend JS (Inertia/Livewire/Laravel)
│   └── css/                    # Tailwind entry point
├── routes/
│   ├── web.php                 # Web routes (session, CSRF, web middleware)
│   ├── api.php                 # API routes (stateless, token auth, /api prefix)
│   ├── console.php             # Closure-based console commands
│   └── channels.php            # Broadcasting channels (WebSocket auth)
├── storage/                    # Logs, cache, sessions, user uploads (NOT web-accessible except via public/storage symlink)
├── tests/
│   ├── Feature/                # Feature tests (HTTP requests, DB)
│   └── Unit/                   # Unit tests (isolated classes)
├── .env                        # Environment config (NEVER commit)
├── artisan                     # The Artisan CLI executable
├── composer.json
└── vite.config.js              # Vite config for frontend build
```

### The `bootstrap/app.php` revolution (Laravel 11+)

The old `app/Http/Kernel.php` and `app/Console/Kernel.php` are GONE. All bootstrapping now lives in `bootstrap/app.php`:

```php
use Illuminate\Foundation\Application;
use Illuminate\Foundation\Configuration\Exceptions;
use Illuminate\Foundation\Configuration\Middleware;

return Application::configure(basePath: dirname(__DIR__))
    ->withRouting(
        web: __DIR__.'/../routes/web.php',
        api: __DIR__.'/../routes/api.php',      // API routes auto-prefixed with /api
        commands: __DIR__.'/../routes/console.php',
        health: '/up',                          // Built-in health check endpoint
    )
    ->withMiddleware(function (Middleware $middleware) {
        // Append custom middleware here
        // $middleware->append(ForceJsonResponse::class);
        // $middleware->statefulApi();   // Use Sanctum session-based API auth
    })
    ->withExceptions(function (Exceptions $exceptions) {
        // Custom exception rendering/reporting
    })->create();
```

---

## Core Mental Model

Laravel's distinctive paradigm is **convention-over-configuration with Active Record ORM and a powerful service container**. Three things differentiate Laravel from other frameworks:

### 1. Eloquent is Active Record, not Data Mapper

Each model class **is** its database row. A `User` instance maps directly to a `users` table row. There is no separate "repository" or "entity manager". This is the single biggest mental shift coming from Doctrine (PHP), SQLAlchemy (Python), or Prisma (TypeScript).

```php
// Create
$user = User::create(['name' => 'Alice', 'email' => 'alice@example.com']);

// Read
$alice = User::where('email', 'alice@example.com')->first();
$active = User::where('active', true)->orderBy('name')->get();

// Update
$alice->update(['last_login_at' => now()]);

// Delete
$alice->delete();

// Relationships are method calls, not separate queries
foreach ($alice->posts as $post) { /* ... */ }      // Lazy load
$alice->load('posts');                                // Eager load (avoid N+1)
User::with('posts')->get();                            // Eager load at query time (PREFERRED)
```

### 2. The Service Container does dependency injection automatically

Laravel's container resolves type-hinted dependencies. You rarely call `$container->make()` directly — just type-hint and Laravel wires it up:

```php
// In a controller method — Laravel auto-resolves both the User model
// (route-model binding) and the StripePaymentService (container binding)
public function store(StoreOrderRequest $request, User $user, StripePaymentService $payments)
{
    $order = $payments->charge($user, $request->validated());
    return redirect()->route('orders.show', $order);
}
```

### 3. Artisan is the universal CLI for everything

If you're editing a file by hand, ask if Artisan can do it for you:

```bash
php artisan make:model Post -mfsc        # Model + Migration + Factory + Seeder + Controller
php artisan make:migration add_status_to_posts_table --table=posts
php artisan make:controller PostController --resource --model=Post
php artisan make:request StorePostRequest
php artisan make:job ProcessPodcast
php artisan make:event OrderShipped
php artisan make:listener SendShipmentNotification --event=OrderShipped
php artisan make:mail OrderShipped --markdown=mail.orders.shipped
php artisan make:policy PostPolicy --model=Post
php artisan make:command SyncExternalData      # Custom console command
php artisan make:middleware EnsureUserIsAdmin
php artisan make:resource PostResource          # API serializer
php artisan make:notification InvoicePaid
php artisan tinker                             # REPL with app booted
```

---

## Routing & Request Lifecycle

Laravel's request lifecycle: `index.php` → bootstrap → global middleware → router → route middleware → controller (with Form Request validation, policy auth, DI) → response → middleware (reverse) → emit.

### Web routes (`routes/web.php`)

```php
use App\Http\Controllers\PostController;
use Illuminate\Support\Facades\Route;

Route::get('/', fn () => view('welcome'))->name('home');

Route::resource('posts', PostController::class);   // 7 RESTful routes
Route::post('posts/{post}/publish', [PostController::class, 'publish'])->name('posts.publish');

// Route model binding — {post} auto-resolves Post model from DB by ID
Route::get('posts/{post}', function (Post $post) {
    return view('posts.show', compact('post'));
});
```

### API routes (`routes/api.php`)

API routes are **stateless** — no session, no CSRF. They get the `/api` prefix automatically and use the `api` middleware stack. Use Sanctum for token-based auth.

---

## Data Layer (Eloquent ORM)

### Migrations: write PHP, not SQL

```bash
php artisan make:migration create_posts_table
```

```php
// database/migrations/2025_01_15_000000_create_posts_table.php
public function up(): void
{
    Schema::create('posts', function (Blueprint $table) {
        $table->id();
        $table->foreignId('user_id')->constrained()->cascadeOnDelete();
        $table->string('title');
        $table->string('slug')->unique();
        $table->longText('body');
        $table->enum('status', ['draft', 'published', 'archived'])->default('draft');
        $table->timestamp('published_at')->nullable();
        $table->json('metadata')->nullable();          // JSON column (PostgreSQL native, MySQL JSON)
        $table->timestamps();
        $table->softDeletes();                          // deleted_at column for soft deletes
    });

    Schema::table('posts', function (Blueprint $table) {
        $table->index(['status', 'published_at']);      // Composite index for common queries
    });
}
```

```bash
php artisan migrate              # Run pending migrations
php artisan migrate:rollback     # Roll back the last batch
php artisan migrate:fresh --seed # Drop all tables, re-migrate, re-seed (DESTRUCTIVE — dev only)
php artisan migrate:status       # See which migrations have run
```

### Models: Active Record in practice

```php
// app/Models/Post.php
namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\SoftDeletes;
use Illuminate\Database\Eloquent\Relations\BelongsTo;
use Illuminate\Database\Eloquent\Factories\HasFactory;

class Post extends Model
{
    use HasFactory, SoftDeletes;

    protected $fillable = ['title', 'slug', 'body', 'status', 'published_at', 'metadata'];

    protected $casts = [
        'published_at' => 'datetime',
        'metadata' => 'array',           // Auto-serialize JSON to/from array
    ];

    public function user(): BelongsTo
    {
        return $this->belongsTo(User::class);
    }

    // Local scope — reusable query filter
    public function scopePublished($query)
    {
        return $query->where('status', 'published')->whereNotNull('published_at');
    }
}
```

### Eager loading (avoid the N+1 query problem)

```php
// ❌ N+1: 1 query for posts + N queries for users (one per post)
$posts = Post::all();
foreach ($posts as $post) {
    echo $post->user->name;        // Triggers a query each iteration
}

// ✅ Eager load: 2 queries total (posts + users)
$posts = Post::with('user')->get();
foreach ($posts as $post) {
    echo $post->user->name;        // No additional queries
}

// ✅ Nested eager loading
$posts = Post::with('user.profile', 'comments.author')->get();

// ✅ Conditional eager loading
$posts = Post::with(['user' => function ($q) {
    $q->select('id', 'name')->where('active', true);
}])->get();
```

Laravel detects N+1 queries in development and logs a warning. Always check your logs when iterating over collections.

### Factories & seeders (test data)

```php
// database/factories/PostFactory.php
class PostFactory extends Factory
{
    public function definition(): array
    {
        return [
            'title' => fake()->sentence(),
            'slug' => fake()->slug(),
            'body' => fake()->paragraphs(3, true),
            'status' => fake()->randomElement(['draft', 'published']),
            'published_at' => fake()->optional()->dateTimeThisYear(),
            'user_id' => User::factory(),
        ];
    }

    public function published(): static
    {
        return $this->state(fn (array $attrs) => ['status' => 'published', 'published_at' => now()]);
    }
}

// Usage in tests or seeders
Post::factory()->count(50)->create();
Post::factory()->published()->count(20)->create();
```

---

## Validation: Form Requests (NOT inline validation)

The Laravel idiom is to extract validation into a dedicated Form Request class. Do not validate inline in controllers.

```bash
php artisan make:request StorePostRequest
```

```php
// app/Http/Requests/StorePostRequest.php
class StorePostRequest extends FormRequest
{
    public function authorize(): bool
    {
        return $this->user()->can('create', Post::class);   // Policy check
    }

    public function rules(): array
    {
        return [
            'title' => ['required', 'string', 'max:255'],
            'body' => ['required', 'string'],
            'status' => ['required', 'in:draft,published'],
            'published_at' => ['nullable', 'date', 'after:now'],
        ];
    }

    public function messages(): array
    {
        return [
            'title.required' => 'A title is required.',
            'published_at.after' => 'Publish date must be in the future.',
        ];
    }
}

// Controller becomes trivially thin:
public function store(StorePostRequest $request)
{
    $post = Post::create($request->validated());
    return redirect()->route('posts.show', $post);
}
```

---

## Authentication & Authorization

### Three auth surfaces

| Surface | Use |
|---|---|
| **Breeze / Jetstream** | Web sessions (cookie + CSRF). Default for browser apps. |
| **Sanctum** | API tokens for first-party SPAs (cookie + CSRF, stateful) AND third-party API consumers (Bearer tokens). |
| **Passport** | Full OAuth2 server. Only if you're issuing third-party OAuth tokens. |

### Policies (model-level authorization)

```bash
php artisan make:policy PostPolicy --model=Post
```

```php
class PostPolicy
{
    public function update(User $user, Post $post): bool
    {
        return $user->id === $post->user_id || $user->isAdmin();
    }

    public function delete(User $user, Post $post): bool
    {
        return $this->update($user, $post);
    }
}

// In controller:
$this->authorize('update', $post);          // Throws 403 if not authorized
// OR in Blade:
@can('update', $post) <a href="...">Edit</a> @endcan
```

---

## Background Jobs (Queues)

For any work that doesn't need to happen in the HTTP request cycle (sending emails, processing uploads, calling slow APIs), use a queued job.

```bash
php artisan make:job ProcessPodcast
```

```php
// app/Jobs/ProcessPodcast.php
class ProcessPodcast implements ShouldQueue
{
    use Dispatchable, InteractsWithQueue, Queueable, SerializesModels;

    public function __construct(
        public Podcast $podcast,
        public int $attempts = 3,
    ) {}

    public function handle(AudioProcessor $processor): void
    {
        $processor->process($this->podcast);
    }

    public function failed(\Throwable $exception): void
    {
        // Called after all retries exhausted
        Notification::route('slack', config('services.slack.webhook'))
            ->notify(new PodcastFailed($this->podcast, $exception));
    }
}

// Dispatch:
ProcessPodcast::dispatch($podcast)->delay(now()->addMinutes(5));
ProcessPodcast::dispatch($podcast)->onQueue('audio');   // Named queue
```

```bash
php artisan queue:work                # Process jobs (long-running, use Supervisor)
php artisan queue:listen              # Process jobs (auto-restart on code change — dev only)
php artisan queue:failed              # List failed jobs
php artisan queue:retry all           # Retry all failed jobs
php artisan horizon                   # Laravel Horizon (Redis only) — dashboard + auto-scaling
```

---

## Testing (Pest is the modern default)

Laravel 11+ ships with **Pest** as the default test framework. Pest is a more expressive layer over PHPUnit.

```bash
php artisan test                     # Run all tests
php artisan test --parallel          # Run tests in parallel (faster)
php artisan test --filter=PostTest   # Run a specific test file
php artisan test --coverage          # Generate coverage report
```

```php
// tests/Feature/PostTest.php
it('can create a post', function () {
    $user = User::factory()->create();

    $response = $this->actingAs($user)->post('/posts', [
        'title' => 'My First Post',
        'body' => 'Lorem ipsum...',
        'status' => 'draft',
    ]);

    $response->assertRedirect();
    expect(Post::where('title', 'My First Post')->exists())->toBeTrue();
});

it('prevents non-authors from editing', function () {
    $post = Post::factory()->create();
    $other = User::factory()->create();

    $this->actingAs($other)->get("/posts/{$post->id}/edit")
        ->assertForbidden();
});
```

Cross-reference: `testing-patterns` skill for general test pyramid / mocking strategies.

---

## Frontend: Blade vs Livewire vs Inertia

| Stack | When |
|---|---|
| **Blade + Alpine.js + Tailwind** | Server-rendered, minimal JS. Default for content sites, admin panels, simple CRUD. |
| **Livewire 3** | Reactive components that stay on the server. Good for complex forms, real-time UIs without writing JS. Pairs with Alpine for client-side bits. |
| **Inertia.js + Vue/React/Svelte** | SPA-feel app without writing a separate API. Best for apps that need client-side routing and rich interactivity. |
| **API-only (Sanctum)** | Mobile apps, third-party consumers, or when the frontend is a separate repo. |

For new projects, default to **Blade** for content-heavy sites and **Inertia + Vue** (Breeze's default Inertia variant) for app-like experiences. Avoid Livewire if the team hasn't used it — it has a learning curve and its own conventions.

---

## Deployment

```bash
# Production build (Vite assets)
npm run build                       # Outputs to public/build/

# Optimize for production
php artisan config:cache            # Cache config (skip in dev — breaks .env changes)
php artisan route:cache             # Cache routes
php artisan view:cache              # Pre-compile Blade views
php artisan event:cache             # Cache event/listener discovery
php artisan optimize                # Runs all the above

# Run migrations safely
php artisan migrate --force         # --force skips the "running in production" prompt (for CI/CD)

# Queue worker via Supervisor (production)
# /etc/supervisor/conf.d/laravel-worker.conf:
# [program:laravel-worker]
# command=php /var/www/my-app/artisan queue:work redis --sleep=3 --tries=3 --max-time=3600
# numprocs=4
# autostart=true
# autorestart=true
# user=www-data
```

For managed hosting, **Laravel Forge** (servers) + **Laravel Vapor** (serverless on AWS) are the canonical options. **Envoyer** is the canonical zero-downtime deployment tool.

---

## Top 10 Anti-Patterns (the most valuable section)

1. **Fat controllers.** Controllers should be ~10-20 lines: validate (Form Request), call a service/action, return a response. Business logic goes in `app/Services/` or `app/Actions/`.

2. **Using `::all()` or `::get()` without pagination.** Tables grow. `Post::all()` will OOM the server when you have 100k posts. Use `Post::paginate(15)` or `Post::cursorPaginate(15)` (more efficient for large datasets).

3. **N+1 queries.** Always use `::with()` for relationships you'll access. Laravel logs N+1 warnings in dev — read your logs.

4. **Inline validation in controllers.** Use Form Requests. Even for "simple" validation — it keeps controllers thin and validation rules reusable.

5. **Mutating `$fillable` at runtime.** If you need mass-assignment of a field that should normally be protected, don't `array_push($this->fillable, 'field')`. Use `$model->forceFill([...])` instead, which is explicit and reviewable.

6. **Using `DB::raw()` when Eloquent has a method.** Eloquent has scopes, casts, accessors, mutators, and conditional clauses for almost everything. Reaching for `DB::raw()` is a code smell — you lose type safety and query logging.

7. **Putting business logic in Blade templates.** Blade is for presentation. If you need a computed value, put it in an accessor on the model or pass it from the controller. Never query the DB from a Blade template.

8. **Caching the wrong layer.** Don't cache individual model queries — cache the rendered HTML or the API response. Laravel's `Cache::remember()` is fine for hot paths but don't cache everything; cache invalidation is harder than the lookup you saved.

9. **Skipping migrations for schema changes.** Editing the DB directly via `php artisan tinker` or a SQL client is the fastest way to lose sync between environments. Always `php artisan make:migration` — even for one-off changes.

10. **Using `env()` outside config files.** Once you run `php artisan config:cache`, `env()` returns null outside config files. Always access config via `config('app.foo')` and put the `env()` call in `config/app.php`. This is the #1 production-only bug.

---

## Cross-references

- `framework-templates` — CLAUDE.md generation template for Laravel (project onboarding)
- `api-patterns` — REST API design (resource controllers, API resources, versioning)
- `security-and-hardening` — OWASP-aware hardening (Laravel has CSRF, XSS, SQL injection protection built in; this skill covers what Laravel doesn't)
- `clean-code` — General coding standards applicable to PHP
- `testing-patterns` — Test pyramid, mocking strategies (Laravel-specific syntax above; general principles there)
- `code-review-checklist` — 12-category code review checklist
- `git-workflow-and-versioning` — Branching/commit conventions for Laravel projects

---

## Dependencies

Required (installed by `composer create-project laravel/laravel`):
- **PHP 8.3+** (Laravel 12 minimum)
- **Composer** 2.x
- **Laravel framework** 12.x
- **Vite** + **Laravel Vite Plugin** (frontend build)

Common additions (install on demand):
- **Laravel Sanctum** (`composer require laravel/sanctum`) — API tokens
- **Laravel Breeze** (`composer require laravel/breeze --dev`) — auth scaffolding
- **Laravel Jetstream** (`composer require laravel/jetstream`) — teams + 2FA
- **Filament** (`composer require filament/filament`) — admin panel
- **Laravel Horizon** (`composer require laravel/horizon`) — Redis queue dashboard
- **Laravel Telescope** (`composer require laravel/telescope --dev`) — dev-only debug toolbar
- **Laravel IDE Helper** (`composer require --dev barryvdh/laravel-ide-helper`) — PhpStorm autocompletion
- **Pest** (`composer require pestphp/pest --dev`) — modern test framework (default in Laravel 11+)

Database drivers (install the one matching your DB):
- `ext-pdo_mysql` — MySQL / MariaDB
- `ext-pdo_pgsql` — PostgreSQL
- `ext-pdo_sqlsrv` — SQL Server
- `ext-pdo_sqlite` — SQLite (default for dev, ships with PHP)
