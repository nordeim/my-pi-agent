---
name: dotnet-9
description: ".NET 9 (C# 13, released November 2024 LTS) + ASP.NET Core enterprise backend workflow skill. Covers the IoC container (Microsoft.Extensions.DependencyInjection — constructor injection, AddScoped/AddTransient/AddSingleton lifetimes, IHostApplicationBuilder), minimal APIs (MapGet/MapPost/MapPut/MapDelete with lambda handlers — the modern alternative to controllers), controller-based APIs (when to choose which), Entity Framework Core 9 (DbContext, DbSet, LINQ-to-SQL queries, migrations via dotnet ef, AsNoTracking for read-only queries, N+1 detection), ASP.NET Core Identity + JWT auth + ASP.NET Core OpenAPI (the built-in替代 Swashbuckle for .NET 9), Kestrel web server (cross-platform, production-grade), configuration via appsettings.json + environment variables + Azure Key Vault, the record type + pattern matching + nullable reference types story (C# 13), xUnit + Moq for testing, and the canonical deployment story (self-contained publish — single-file binary on Linux without .NET installed, Docker multi-stage build). Use when building any C# / .NET enterprise web app, REST API, or microservice on .NET 9 — especially when the task involves EF Core entity design, LINQ queries, DI lifetime choice, JWT auth, or self-contained deployment where idiomatic .NET differs from Java Spring Boot or other web frameworks."
license: Proprietary. LICENSE.txt has complete terms
---

# .NET 9 + ASP.NET Core — Enterprise C# Backend Workflow Skill

> **Target:** .NET 9 (released November 2024, LTS through May 2026) with C# 13. .NET 9 ships with **native AOT** for ASP.NET Core minimal APIs (smaller, faster cold-start for serverless), **ASP.NET Core OpenAPI** built-in (replaces Swashbuckle for .NET 9+), and **rate limiting + output caching + request decompression** as first-class middleware. EF Core 9 adds `EF.CompileAsyncQuery` for ahead-of-time compiled queries. Kestrel is the production web server (cross-platform — runs on Linux, macOS, Windows).

## When to Use This Skill

Use this skill whenever the user is building, debugging, or extending a .NET 9 / ASP.NET Core application. Trigger phrases include ".NET", "dotnet", "C#", "ASP.NET Core", "EF Core", "Entity Framework", "Kestrel", "Minimal API", "MapGet", "MapPost", "DbContext", "DbSet", "LINQ", "AddScoped", "AddTransient", "AddSingleton", "IHostApplicationBuilder", "appsettings.json", "Program.cs", "dotnet ef", "dotnet publish", "xUnit", "Moq", and any reference to a `.csproj` file or top-level-statements `Program.cs`.

Do **not** use this skill for:
- **.NET Framework 4.x** — Windows-only, different runtime, no minimal APIs, different DI container. Migrate to .NET 9 first.
- **.NET ≤8** — some features here (built-in OpenAPI, native AOT for minimal APIs) are .NET 9+.
- **Unity / MonoGame / Godot with C#** — different ecosystems (game engines, not web).
- **Java / Spring Boot** — see `spring-boot-3` skill (similar IoC model, different language and conventions).
- **Other backend languages** (Go, Rust, Node.js, Python, Ruby, PHP) — see `go-web`, `rust-web`, `laravel-12`, `rails-8`, `django-6`, `fastapi-sqlalchemy` skills.

## Quick Start

```bash
# Install .NET 9 SDK
# macOS: brew install --cask dotnet-sdk
# Linux: see https://learn.microsoft.com/dotnet/core/install/linux
# Windows: download from https://dotnet.microsoft.com/download

# Create a new Web API project (minimal APIs by default in .NET 9)
dotnet new webapi -n myapp -o myapp --use-minimal-apis
cd myapp

dotnet run                  # Dev server at http://localhost:5000
# Or with hot reload (file watcher):
dotnet watch run

# Test the endpoint
curl http://localhost:5000/weatherforecast
```

### Key commands

```bash
dotnet new <template>       # Create a project (webapi, web, mvc, console, classlib, xunit)
dotnet new list             # List available templates
dotnet build                # Compile
dotnet build -c Release     # Release build
dotnet run                  # Build + run
dotnet watch run            # Build + run with hot reload on file change
dotnet test                 # Run all tests
dotnet test --filter "FullyQualifiedName~UserController"  # Run tests matching filter
dotnet add package <name>   # Add a NuGet package
dotnet add reference <proj> # Add a project reference
dotnet restore              # Restore packages (usually auto)
dotnet ef migrations add <Name>   # Generate an EF Core migration
dotnet ef database update         # Apply migrations
dotnet ef database drop           # Drop the DB (DESTRUCTIVE)
dotnet ef migrations remove       # Remove the last migration (if not applied)
dotnet publish -c Release -o publish   # Publish for deployment
dotnet publish -c Release -r linux-x64 --self-contained   # Self-contained (no .NET on target)
dotnet publish -c Release -r linux-x64 --self-contained -p:PublishSingleFile=true   # Single file!
dotnet format               # Format code (install via: dotnet tool install -g dotnet-format)
dotnet tool list -g         # List global tools
dotnet tool install -g <id> # Install a global tool
```

---

## Project Structure (.NET 9 canonical layout)

.NET 9 uses **top-level statements** in `Program.cs` (no `class Program { static void Main() }` boilerplate). The entire app startup is a sequence of statements.

```
myapp/
├── Program.cs                  # ← Entry point (top-level statements — the whole app config)
├── myapp.csproj                # ← Project file (deps, target framework, properties)
├── appsettings.json            # ← Main config
├── appsettings.Development.json # Dev overrides
├── appsettings.Production.json  # Prod overrides
├── Properties/
│   └── launchSettings.json     # IDE/debug profiles (don't commit if secrets)
├── Data/
│   └── ApplicationDbContext.cs # EF Core DbContext
├── Models/
│   ├── Entities/               # EF Core entities (User.cs, Post.cs)
│   └── Dtos/                   # Data Transfer Objects (UserDto.cs, CreateUserRequest.cs)
├── Services/                   # Business logic (UserService.cs, EmailService.cs)
├── Endpoints/                  # Minimal API endpoint definitions (UserEndpoints.cs)
├── Middleware/                 # Custom middleware (ExceptionHandlingMiddleware.cs)
├── Migrations/                 # EF Core migrations (auto-generated)
├── Tests/                      # Test project (separate .csproj)
│   └── myapp.Tests.csproj
├── Dockerfile
├── docker-compose.yml
└── README.md
```

### The `Program.cs` (top-level statements)

```csharp
// Program.cs — the entire app config in ~30 lines
using Microsoft.EntityFrameworkCore;
using myapp.Data;
using myapp.Services;
using myapp.Endpoints;

var builder = WebApplication.CreateBuilder(args);

// Register services (DI container)
builder.Services.AddDbContext<ApplicationDbContext>(options =>
    options.UseNpgsql(builder.Configuration.GetConnectionString("Default")));

builder.Services.AddScoped<IUserService, UserService>();
builder.Services.AddScoped<IEmailService, EmailService>();

builder.Services.AddAuthentication().AddJwtBearer(options =>
{
    options.TokenValidationParameters = new()
    {
        ValidateIssuer = true,
        ValidateAudience = true,
        ValidateLifetime = true,
        ValidIssuer = builder.Configuration["Jwt:Issuer"],
        ValidAudience = builder.Configuration["Jwt:Audience"],
        IssuerSigningKey = new SymmetricSecurityKey(
            Encoding.UTF8.GetBytes(builder.Configuration["Jwt:Key"]!))
    };
});

builder.Services.AddAuthorization();
builder.Services.AddOpenApi();      // .NET 9 built-in OpenAPI
builder.Services.AddProblemDetails(); // RFC 7807 problem details

var app = builder.Build();

// Middleware pipeline (ORDER MATTERS)
app.UseExceptionHandler();          // Global exception handler
app.UseStatusCodePages();

if (app.Environment.IsDevelopment())
{
    app.MapOpenApi();               // /openapi/v1.json
    app.MapSwaggerUI();             // /swagger (manual install: dotnet add package Swashbuckle.AspNetCore)
}

app.UseAuthentication();
app.UseAuthorization();

// Map endpoints
app.MapUserEndpoints();            // Extension method — see Endpoints/UserEndpoints.cs

app.Run();                         // Start Kestrel
```

### The `.csproj` file

```xml
<Project Sdk="Microsoft.NET.Sdk.Web">

  <PropertyGroup>
    <TargetFramework>net9.0</TargetFramework>
    <Nullable>enable</Nullable>          <!-- Nullable reference types ON -->
    <ImplicitUsings>enable</ImplicitUsings>  <!-- Auto-import common usings -->
    <TreatWarningsAsErrors>true</TreatWarningsAsErrors>
  </PropertyGroup>

  <ItemGroup>
    <PackageReference Include="Microsoft.EntityFrameworkCore.Design" Version="9.0.0">
      <PrivateAssets>all</PrivateAssets>
      <IncludeAssets>runtime; build; native; contentfiles; analyzers; buildtransitive</IncludeAssets>
    </PackageReference>
    <PackageReference Include="Npgsql.EntityFrameworkCore.PostgreSQL" Version="9.0.0" />
    <PackageReference Include="Microsoft.AspNetCore.Authentication.JwtBearer" Version="9.0.0" />
    <PackageReference Include="Microsoft.AspNetCore.OpenApi" Version="9.0.0" />
    <PackageReference Include="Swashbuckle.AspNetCore" Version="6.6.0" />
    <PackageReference Include="AspNetCoreRateLimit" Version="5.0.0" />
  </ItemGroup>

</Project>
```

---

## Core Mental Model: DI Container + LINQ + Async/Await + Nullable Reference Types

.NET 9's distinctive paradigm is **a managed runtime with first-class dependency injection, language-integrated queries (LINQ), and async/await built into the language.** Four things differentiate .NET from other backend ecosystems:

### 1. The DI container is built into the framework

```csharp
// Register services in Program.cs
builder.Services.AddScoped<IUserService, UserService>();        // One instance per HTTP request
builder.Services.AddSingleton<IEmailService, EmailService>();   // One instance for the whole app
builder.Services.AddTransient<IPaymentService, PaymentService>(); // New instance every time

// Use them via constructor injection
public class UserController
{
    private readonly IUserService _userService;
    private readonly ILogger<UserController> _logger;

    public UserController(IUserService userService, ILogger<UserController> logger)
    {
        _userService = userService;
        _logger = logger;
    }

    public async Task<IResult> GetUser(Guid id)
    {
        _logger.LogInformation("Getting user {UserId}", id);
        var user = await _userService.GetByIdAsync(id);
        return user is null ? Results.NotFound() : Results.Ok(user);
    }
}
```

**DI lifetimes (memorize these):**

| Lifetime | When to use |
|---|---|
| `AddScoped` | One instance per HTTP request. Default for most services (DB contexts, repositories, business logic). |
| `AddSingleton` | One instance for the app's lifetime. Use for stateless services, caches, configuration. NEVER use for EF Core DbContext (it's not thread-safe). |
| `AddTransient` | New instance every time. Lightweight, stateless services where construction is cheap. |

**Captive dependency trap:** A singleton service that depends on a scoped/transient service "captures" the dependency for its whole lifetime. This is a bug — the scoped service becomes effectively singleton. The DI container does NOT warn about this by default. Fix: either make the singleton depend on `IServiceScopeFactory` (create a scope per use), or use `AddSingleton<IFoo, Foo>` with a factory that creates the dependency lazily.

### 2. LINQ — queries in the language

```csharp
// Query syntax (SQL-like)
var activeUsers = from u in dbContext.Users
                  where u.Status == UserStatus.Active
                  orderby u.CreatedAt descending
                  select u;

// Method syntax (fluent) — preferred for complex queries
var activeUsers = dbContext.Users
    .Where(u => u.Status == UserStatus.Active)
    .OrderByDescending(u => u.CreatedAt)
    .Select(u => new UserDto(u.Id, u.Email, u.Name))
    .AsNoTracking()           // Skip change tracking — faster for reads
    .ToList();

// Joins
var usersWithPosts = dbContext.Users
    .Join(dbContext.Posts,
        u => u.Id,
        p => p.AuthorId,
        (u, p) => new { User = u, Post = p })
    .ToList();

// Eager loading (avoid N+1)
var users = dbContext.Users
    .Include(u => u.Posts)              // JOIN
    .ThenInclude(p => p.Tags)           // Nested include
    .ToList();

// Async
var users = await dbContext.Users
    .Where(u => u.Status == UserStatus.Active)
    .ToListAsync();

// Projection (DTO) — generates efficient SQL, no entity materialization
var dtos = await dbContext.Users
    .Where(u => u.Status == UserStatus.Active)
    .Select(u => new UserDto(u.Id, u.Email, u.Name))
    .ToListAsync();
```

LINQ is translated to SQL by EF Core's provider. The query syntax and method syntax are equivalent — pick whichever is more readable for the specific query.

### 3. Async/await is pervasive and ergonomic

```csharp
public async Task<UserDto> GetUserAsync(Guid id, CancellationToken ct)
{
    var user = await _dbContext.Users
        .AsNoTracking()
        .FirstOrDefaultAsync(u => u.Id == id, ct);   // Pass CancellationToken everywhere

    if (user is null)
        throw new NotFoundException($"User {id} not found");

    return new UserDto(user.Id, user.Email, user.Name);
}
```

**Rules:**
1. **Async all the way down.** Don't mix sync and async — calling `.Result` or `.Wait()` on an async method causes thread-pool starvation in web apps.
2. **Pass `CancellationToken` to every async method** that does I/O. ASP.NET Core automatically cancels on client disconnect.
3. **Suffix async methods with `Async`** (e.g., `GetUserAsync`). This is a strong convention.
4. **`ValueTask<T>` over `Task<T>`** for hot paths where the result is often synchronous (e.g., cache hits).

### 4. Nullable reference types (NRTs) — opt-in compile-time null safety

```xml
<!-- In .csproj -->
<Nullable>enable</Nullable>
```

```csharp
string name = "Alice";        // Non-nullable — compiler warns if you assign null
string? middleName = null;    // Nullable — OK to be null

public User GetUser(Guid id)
{
    User? user = _dbContext.Users.FirstOrDefault(u => u.Id == id);
    return user ?? throw new NotFoundException($"User {id}");  // ?? null-coalesces
}

// The ! (null-forgiving) operator — tells the compiler "I know this isn't null"
string name = possiblyNull!;   // Suppresses the warning (use sparingly)
```

When `<Nullable>enable</Nullable>` is set, the compiler tracks nullability and warns on potential `NullReferenceException`s. This is **one of the biggest advantages of C# over Java** — null safety is enforced at compile time. Always enable it for new projects.

---

## Minimal APIs vs Controllers

.NET 9 offers two API styles. Both are valid. The choice is per-project.

### Minimal APIs (modern, lightweight, recommended for new projects)

```csharp
// Endpoints/UserEndpoints.cs
public static class UserEndpoints
{
    public static IEndpointRouteBuilder MapUserEndpoints(this IEndpointRouteBuilder app)
    {
        var group = app.MapGroup("/api/users").WithTags("Users");

        group.MapGet("/", async (IUserService service, CancellationToken ct) =>
        {
            var users = await service.ListAsync(ct);
            return Results.Ok(users);
        });

        group.MapGet("/{id:guid}", async (Guid id, IUserService service, CancellationToken ct) =>
        {
            var user = await service.GetByIdAsync(id, ct);
            return user is null ? Results.NotFound() : Results.Ok(user);
        });

        group.MapPost("/", async (CreateUserRequest req, IUserService service, CancellationToken ct) =>
        {
            var user = await service.CreateAsync(req, ct);
            return Results.Created($"/api/users/{user.Id}", user);
        })
        .AddEndpointFilter<ValidationFilter<CreateUserRequest>>();

        group.MapDelete("/{id:guid}", async (Guid id, IUserService service, CancellationToken ct) =>
        {
            await service.DeleteAsync(id, ct);
            return Results.NoContent();
        })
        .RequireAuthorization("Admin");

        return app;
    }
}
```

Minimal APIs:
- Are lambda-based — handlers are inline functions
- Support **endpoint filters** (`AddEndpointFilter<T>`) for cross-cutting concerns (validation, logging, auth)
- Support **route groups** (`MapGroup`) for shared prefixes/tags/policies
- Are required for **native AOT** publishing (.NET 9+ — smaller, faster cold-start for serverless)
- Have less boilerplate than controllers
- Don't have a built-in `ModelState` validation equivalent — use endpoint filters or `IValidatableObject`

### Controllers (classic, more features, sometimes required)

```csharp
// Controllers/UserController.cs
[ApiController]
[Route("api/[controller]")]
public class UserController : ControllerBase
{
    private readonly IUserService _service;

    public UserController(IUserService service) => _service = service;

    [HttpGet]
    public async Task<ActionResult<IEnumerable<UserDto>>> List(CancellationToken ct)
        => Ok(await _service.ListAsync(ct));

    [HttpGet("{id:guid}")]
    public async Task<ActionResult<UserDto>> Get(Guid id, CancellationToken ct)
    {
        var user = await _service.GetByIdAsync(id, ct);
        return user is null ? NotFound() : Ok(user);
    }

    [HttpPost]
    public async Task<ActionResult<UserDto>> Create(
        [FromBody] CreateUserRequest request,
        CancellationToken ct)
    {
        if (!ModelState.IsValid)
            return BadRequest(ModelState);

        var user = await _service.CreateAsync(request, ct);
        return CreatedAtAction(nameof(Get), new { id = user.Id }, user);
    }

    [HttpDelete("{id:guid}")]
    [Authorize(Policy = "Admin")]
    public async Task<IActionResult> Delete(Guid id, CancellationToken ct)
    {
        await _service.DeleteAsync(id, ct);
        return NoContent();
    }
}
```

Controllers:
- Have `[ApiController]` attributes that enable automatic model validation, binding source inference, and problem details responses
- Have `ModelState.IsValid` for validation
- Support action filters, result filters, exception filters
- Are required for some advanced scenarios (e.g., `IAsyncActionFilter`, traditional MVC views)
- Have more boilerplate

### When to choose which

| Situation | Choose |
|---|---|
| New project, simple CRUD API | Minimal APIs |
| Serverless / Lambda (need native AOT) | Minimal APIs |
| Existing controller-based project | Stay with controllers |
| Heavy use of action filters | Controllers |
| Mixing API + MVC views | Controllers |
| Microservice with <20 endpoints | Minimal APIs |
| Large API with complex cross-cutting concerns | Either (minimal API endpoint filters can do most of what action filters do) |

**Opinionated default:** minimal APIs for new projects. Move to controllers only if you hit a wall with endpoint filters.

---

## EF Core 9: the ORM

### DbContext + entities

```csharp
// Data/ApplicationDbContext.cs
public class ApplicationDbContext : DbContext
{
    public ApplicationDbContext(DbContextOptions<ApplicationDbContext> options) : base(options) {}

    public DbSet<User> Users => Set<User>();
    public DbSet<Post> Posts => Set<Post>();

    protected override void OnModelCreating(ModelBuilder modelBuilder)
    {
        modelBuilder.Entity<User>(e =>
        {
            e.HasKey(u => u.Id);
            e.HasIndex(u => u.Email).IsUnique();
            e.Property(u => u.Email).IsRequired().HasMaxLength(255);
            e.Property(u => u.Status).HasConversion<string>();
            e.HasMany(u => u.Posts).WithOne(p => p.Author).HasForeignKey(p => p.AuthorId);
        });

        modelBuilder.Entity<Post>(e =>
        {
            e.HasKey(p => p.Id);
            e.Property(p => p.Title).IsRequired().HasMaxLength(200);
            e.HasIndex(p => new { p.Status, p.PublishedAt });
        });

        // Global query filter (e.g., soft delete, multi-tenant)
        modelBuilder.Entity<User>().HasQueryFilter(u => !u.IsDeleted);
    }
}

// Models/Entities/User.cs
public class User
{
    public Guid Id { get; set; }
    public string Email { get; set; } = "";
    public string Name { get; set; } = "";
    public string PasswordHash { get; set; } = "";
    public UserStatus Status { get; set; } = UserStatus.Active;
    public bool IsDeleted { get; set; }
    public DateTimeOffset CreatedAt { get; set; } = DateTimeOffset.UtcNow;
    public DateTimeOffset UpdatedAt { get; set; }

    // Navigation properties
    public List<Post> Posts { get; set; } = new();
}

public enum UserStatus { Active, Suspended, Deleted }
```

### Migrations

```bash
# Install the EF Core CLI tool (one-time)
dotnet tool install --global dotnet-ef

# Generate a migration
dotnet ef migrations add CreateInitial

# Apply migrations
dotnet ef database update

# Roll back to a specific migration
dotnet ef database update PreviousMigrationName

# Remove the last migration (only if not applied to DB)
dotnet ef migrations remove

# Generate a SQL script instead of applying directly (for review)
dotnet ef migrations script --output migrate.sql
```

```csharp
// Migrations/20250115000000_CreateInitial.cs (auto-generated)
public partial class CreateInitial : Migration
{
    protected override void Up(MigrationBuilder migrationBuilder)
    {
        migrationBuilder.CreateTable(
            name: "Users",
            columns: table => new
            {
                Id = table.Column<Guid>(type: "uuid", nullable: false),
                Email = table.Column<string>(type: "character varying(255)", maxLength: 255, nullable: false),
                Name = table.Column<string>(type: "text", nullable: false),
                PasswordHash = table.Column<string>(type: "text", nullable: false),
                Status = table.Column<string>(type: "text", nullable: false),
                IsDeleted = table.Column<bool>(type: "boolean", nullable: false),
                CreatedAt = table.Column<DateTimeOffset>(type: "timestamp with time zone", nullable: false),
                UpdatedAt = table.Column<DateTimeOffset>(type: "timestamp with time zone", nullable: false)
            },
            constraints: table =>
            {
                table.PrimaryKey("PK_Users", x => x.Id);
                table.UniqueConstraint("AK_Users_Email", x => x.Email);
            });
    }

    protected override void Down(MigrationBuilder migrationBuilder)
    {
        migrationBuilder.DropTable(name: "Users");
    }
}
```

### Query patterns (and avoiding N+1)

```csharp
// ❌ N+1: 1 query for users + N queries for posts
var users = await _dbContext.Users.ToListAsync();
foreach (var u in users)
{
    var postCount = u.Posts.Count;   // Triggers a query per user
}

// ✅ Eager load with Include
var users = await _dbContext.Users
    .Include(u => u.Posts)
    .ToListAsync();

// ✅ Projection (most efficient — only fetch what you need)
var dtos = await _dbContext.Users
    .Select(u => new UserWithPostCountDto(u.Id, u.Email, u.Posts.Count))
    .ToListAsync();

// ✅ AsNoTracking for reads (faster — no change tracking)
var users = await _dbContext.Users
    .AsNoTracking()
    .Where(u => u.Status == UserStatus.Active)
    .ToListAsync();

// ✅ Split queries (multiple queries instead of one giant JOIN — avoids "cartesian explosion")
var users = await _dbContext.Users
    .Include(u => u.Posts)
    .ThenInclude(p => p.Tags)
    .AsSplitQuery()              // ← runs 3 queries instead of 1 giant JOIN
    .ToListAsync();
```

### Transactions

```csharp
using var transaction = await _dbContext.Database.BeginTransactionAsync();

try
{
    var from = await _dbContext.Accounts.FirstAsync(a => a.Id == fromId);
    var to = await _dbContext.Accounts.FirstAsync(a => a.Id == toId);

    from.Balance -= amount;
    to.Balance += amount;

    await _dbContext.SaveChangesAsync();
    await transaction.CommitAsync();
}
catch
{
    await transaction.RollbackAsync();
    throw;
}

// OR — simpler, with EF Core's automatic transaction:
// SaveChangesAsync() wraps all changes in a transaction by default
```

---

## Configuration

```json
// appsettings.json
{
  "ConnectionStrings": {
    "Default": "Host=localhost;Database=myapp;Username=postgres;Password=postgres"
  },
  "Jwt": {
    "Issuer": "myapp",
    "Audience": "myapp-users",
    "Key": ""  // Override via env: Jwt__Key (use secrets manager in prod)
  },
  "Logging": {
    "LogLevel": {
      "Default": "Information",
      "Microsoft.AspNetCore": "Warning"
    }
  },
  "AllowedHosts": "*"
}
```

```csharp
// Access configuration anywhere via IConfiguration (injected)
public class UserService
{
    private readonly string _defaultRole;

    public UserService(IConfiguration config)
    {
        _defaultRole = config["DefaultRole"] ?? "user";
    }
}

// OR use the Options pattern (typed config)
public class JwtOptions
{
    public string Issuer { get; set; } = "";
    public string Audience { get; set; } = "";
    public string Key { get; set; } = "";
    public int ExpiryMinutes { get; set; } = 60;
}

// Program.cs
builder.Services.Configure<JwtOptions>(builder.Configuration.GetSection("Jwt"));

// Usage
public class TokenService(IOptions<JwtOptions> options)
{
    private readonly JwtOptions _options = options.Value;
    // ...
}
```

### Environment variables override appsettings

`Jwt__Key` (double underscore = section separator) overrides `Jwt:Key` in appsettings.json.

### Secrets manager (Development only)

```bash
# Initialize user secrets (one-time per project)
dotnet user-secrets init

# Set a secret
dotnet user-secrets set "Jwt:Key" "super-secret-key-123"

# List secrets
dotnet user-secrets list
```

User secrets are stored in `~/.microsoft/usersecrets/<id>/secrets.json` — OUTSIDE the project directory, so they're never committed. Use Azure Key Vault or environment variables in production.

---

## Authentication: JWT + ASP.NET Core Identity

```csharp
// Program.cs
builder.Services.AddAuthentication(JwtBearerDefaults.AuthenticationScheme)
    .AddJwtBearer(options =>
    {
        options.TokenValidationParameters = new()
        {
            ValidateIssuer = true,
            ValidateAudience = true,
            ValidateLifetime = true,
            ValidateIssuerSigningKey = true,
            ValidIssuer = builder.Configuration["Jwt:Issuer"],
            ValidAudience = builder.Configuration["Jwt:Audience"],
            IssuerSigningKey = new SymmetricSecurityKey(
                Encoding.UTF8.GetBytes(builder.Configuration["Jwt:Key"]!))
        };
    });

builder.Services.AddAuthorization(options =>
{
    options.AddPolicy("Admin", p => p.RequireRole("Admin"));
    options.AddPolicy("Over18", p => p.Requirements.Add(new MinimumAgeRequirement(18)));
});

// In endpoints
app.MapDelete("/api/users/{id}", async (...) => { /* ... */ })
   .RequireAuthorization("Admin");
```

For ASP.NET Core Identity (built-in user management with EF Core storage, password hashing, 2FA, external login):

```csharp
builder.Services.AddIdentity<User, IdentityRole<Guid>>()
    .AddEntityFrameworkStores<ApplicationDbContext>()
    .AddDefaultTokenProviders();
```

---

## Testing: xUnit + Moq

### Unit tests

```csharp
// Tests/UserServiceTests.cs
public class UserServiceTests
{
    private readonly Mock<IUserRepository> _repoMock;
    private readonly UserService _service;

    public UserServiceTests()
    {
        _repoMock = new Mock<IUserRepository>();
        _service = new UserService(_repoMock.Object);
    }

    [Fact]
    public async Task GetByIdAsync_ReturnsUser_WhenExists()
    {
        // Arrange
        var user = new User { Id = Guid.NewGuid(), Email = "a@b.c", Name = "Alice" };
        _repoMock.Setup(r => r.GetByIdAsync(user.Id, It.IsAny<CancellationToken>()))
            .ReturnsAsync(user);

        // Act
        var result = await _service.GetByIdAsync(user.Id, CancellationToken.None);

        // Assert
        Assert.NotNull(result);
        Assert.Equal(user.Email, result.Email);
    }

    [Theory]
    [InlineData("")]
    [InlineData("not-an-email")]
    [InlineData("a@")]
    public async Task CreateAsync_Throws_WhenEmailInvalid(string email)
    {
        var request = new CreateUserRequest(email, "Alice", "Password123!");
        await Assert.ThrowsAsync<ValidationException>(() =>
            _service.CreateAsync(request, CancellationToken.None));
    }
}
```

### Integration tests with `WebApplicationFactory`

```csharp
// Tests/UserApiTests.cs
public class UserApiTests : IClassFixture<WebApplicationFactory<Program>>
{
    private readonly HttpClient _client;

    public UserApiTests(WebApplicationFactory<Program> factory)
    {
        _client = factory
            .WithWebHostBuilder(builder =>
            {
                builder.ConfigureServices(services =>
                {
                    // Replace real DB with in-memory
                    services.RemoveAll<DbContextOptions<ApplicationDbContext>>();
                    services.AddDbContext<ApplicationDbContext>(o => o.UseInMemoryDatabase("Test"));
                });
            })
            .CreateClient();
    }

    [Fact]
    public async Task Post_User_Creates_And_Returns_201()
    {
        var body = new StringContent(
            """{"email":"alice@example.com","name":"Alice","password":"P@ssw0rd!"}""",
            Encoding.UTF8,
            "application/json");

        var response = await _client.PostAsync("/api/users", body);

        Assert.Equal(HttpStatusCode.Created, response.StatusCode);
    }
}
```

Cross-reference: `testing-patterns` for general test pyramid / mocking strategies.

---

## Deployment: self-contained publish + Docker

### Self-contained single-file binary (no .NET on target)

```bash
# Publish self-contained for Linux x64, single file, trimmed
dotnet publish -c Release \
  -r linux-x64 \
  --self-contained true \
  -p:PublishSingleFile=true \
  -p:IncludeNativeLibrariesForSelfExtract=true \
  -p:PublishTrimmed=true \
  -o publish
# Result: publish/myapp — a single ~30-80 MB executable that runs on any Linux x64
```

**Note on trimming:** trimming removes unused code at publish time. Reflection-based code (some serializers, EF Core lazy loading proxies) can break with trimming. Test thoroughly if you enable `PublishTrimmed`. For native AOT (.NET 9 minimal APIs), trimming is mandatory.

### Docker multi-stage build

```dockerfile
# Build stage
FROM mcr.microsoft.com/dotnet/sdk:9.0 AS build
WORKDIR /src
COPY myapp.csproj .
RUN dotnet restore
COPY . .
RUN dotnet publish -c Release -o /app/publish --no-restore

# Runtime stage — minimal runtime image
FROM mcr.microsoft.com/dotnet/aspnet:9.0 AS final
WORKDIR /app
COPY --from=build /app/publish .
EXPOSE 8080
ENV ASPNETCORE_URLS=http://+:8080
ENTRYPOINT ["dotnet", "myapp.dll"]
```

Final image size: ~120-200 MB (runtime + app). For smaller images, use self-contained single-file publish with the `runtime-deps:9.0-alpine` base image.

---

## Top 10 Anti-Patterns (the most valuable section)

1. **Captive dependencies.** A singleton service that depends on a scoped/transient service "captures" it for the app's lifetime. The scoped service (like a DbContext) becomes effectively singleton — corrupting data across requests. Fix: either make the singleton depend on `IServiceScopeFactory` (create a scope per use), or change the lifetime.

2. **Using `AddSingleton` for EF Core `DbContext`.** `DbContext` is NOT thread-safe. If you make it singleton, concurrent requests corrupt the context. Always use `AddDbContext` (which defaults to `Scoped` — one per request) or `AddDbContextFactory` (for scenarios where you need to create contexts manually).

3. **`.Result` / `.Wait()` on async methods.** This causes sync-over-async — the thread-pool thread blocks waiting for the async operation, which itself needs a thread-pool thread to resume. Under load, the thread pool starves and the app hangs. **Always `await`** async methods.

4. **N+1 queries via lazy loading.** EF Core's lazy loading proxies trigger a query per navigation property access. Either eager-load (`Include`) or disable lazy loading entirely (`optionsBuilder.UseLazyLoadingProxies(false)`). Use projection (`.Select()`) for read-only queries — it generates efficient SQL and skips entity materialization.

5. **Not using `AsNoTracking()` for reads.** EF Core tracks all entities by default, building a change tracker that's checked on every `SaveChanges`. For read-only queries, `AsNoTracking()` skips tracking — measurably faster. Even better: use projection to DTOs (`Select(u => new UserDto(...))`) so EF Core doesn't materialize entities at all.

6. **Mixing sync and async data access.** Calling synchronous EF Core methods (`FirstOrDefault`, `ToList`) in an async controller blocks a thread-pool thread. Always use the `Async` suffix variants (`FirstOrDefaultAsync`, `ToListAsync`). The compiler doesn't warn about this — discipline required.

7. **Catching `Exception` in middleware.** A catch-all `try-catch (Exception ex)` in middleware masks bugs — every unexpected error becomes a generic 500 with no useful logging. Use `app.UseExceptionHandler()` with `IProblemDetailsService` (built-in) which logs the full exception and returns an RFC 7807 problem details response. Catch specific exceptions you can handle meaningfully (404 for `NotFoundException`, 400 for `ValidationException`).

8. **`ModelState.IsValid` in minimal APIs.** Minimal APIs don't have `ModelState` — that's a controller feature. Use endpoint filters (`AddEndpointFilter<ValidationFilter<T>>()`) or `IValidatableObject` on the DTO with manual validation. Or use the `MinimalApis.Extensions` package for `IValidatableProperty` support.

9. **Not enabling nullable reference types.** `<Nullable>enable</Nullable>` is opt-in but should be on for every new project. It catches potential `NullReferenceException`s at compile time — one of C#'s biggest advantages over Java. The migration for existing projects can be gradual (file-by-file via `#nullable enable` directives).

10. **Hardcoding secrets in `appsettings.json`.** Use `dotnet user-secrets` in Development, environment variables in Staging/Production, and Azure Key Vault (or AWS Secrets Manager) for cloud. The `appsettings.json` should have placeholder values or empty strings — never real secrets. Commit `appsettings.json` but gitignore `appsettings.Development.json` if it has secrets (better: never put secrets in appsettings at all).

---

## Cross-references

- `framework-templates` — CLAUDE.md generation template for .NET (project onboarding)
- `spring-boot-3` — Java enterprise backend (similar IoC model, different language and conventions)
- `go-web` — Go web patterns (similar backend use case, no IoC container, no ORM)
- `rust-web` — Rust web patterns (similar backend use case, ownership + traits vs DI + LINQ)
- `api-and-interface-design` — Type contract design (relevant for C# interfaces and DTOs)
- `api-patterns` — REST API patterns (relevant for minimal API endpoint definitions)
- `security-and-hardening` — OWASP-aware hardening (ASP.NET Core has built-in CSRF, auth, CORS support)
- `clean-code` — General coding standards applicable to C#
- `testing-patterns` — Test pyramid, mocking strategies (.NET-specific syntax above; general principles there)
- `code-review-checklist` — 12-category code review checklist
- `git-workflow-and-versioning` — Branching/commit conventions for .NET projects

---

## Dependencies

Required (installed via `dotnet new` + `dotnet add package`):
- **.NET 9 SDK** (LTS through May 2026)
- **C# 13** (bundled with .NET 9)
- **ASP.NET Core 9** (bundled with .NET 9 SDK)
- **EF Core 9** (`Microsoft.EntityFrameworkCore` + provider package)
- **Kestrel** (bundled with ASP.NET Core — production-grade cross-platform web server)

### Database providers (add one)

| Provider | Use |
|---|---|
| `Npgsql.EntityFrameworkCore.PostgreSQL` | PostgreSQL |
| `Microsoft.EntityFrameworkCore.SqlServer` | SQL Server |
| `Microsoft.EntityFrameworkCore.MySql` (Pomelo) | MySQL / MariaDB |
| `Microsoft.EntityFrameworkCore.Sqlite` | SQLite (dev/test) |
| `Microsoft.EntityFrameworkCore.Cosmos` | Azure Cosmos DB |

### Common additions (install via `dotnet add package`)

- `Microsoft.AspNetCore.Authentication.JwtBearer` — JWT auth
- `Microsoft.AspNetCore.Identity.EntityFrameworkCore` — ASP.NET Core Identity
- `Microsoft.AspNetCore.OpenApi` — built-in OpenAPI (.NET 9+, replaces Swashbuckle)
- `Swashbuckle.AspNetCore` — Swagger UI (still widely used; .NET 9 built-in OpenAPI is newer)
- `AspNetCoreRateLimit` — rate limiting middleware (or use built-in .NET 7+ rate limiter)
- `Serilog.AspNetCore` — structured logging (preferred over built-in `ILogger` for production)
- `FluentValidation.AspNetCore` — alternative validation framework
- `AutoMapper.Extensions.Microsoft.DependencyInjection` — DTO ↔ Entity mapping
- `MediatR` — CQRS / mediator pattern (popular for clean architecture)
- `Polly` — resilience (circuit breaker, retry, timeout)
- `xUnit` + `Moq` + `FluentAssertions` — testing stack
- `Microsoft.AspNetCore.Mvc.Testing` — `WebApplicationFactory` for integration tests
- `Testcontainers.PostgreSql` — Docker-based integration tests with real Postgres
