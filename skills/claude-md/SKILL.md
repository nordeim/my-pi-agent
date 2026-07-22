---
name: claude-md
description: Generate proper CLAUDE.md files for any codebase. Analyzes codebase structure, detects frameworks and languages, and produces a comprehensive CLAUDE.md following the Meticulous Approach framework.
version: 1.1.0
skills:
  - framework-templates
  - clean-code
  - designing-architecture
  - testing-patterns
trigger: "claude-md"
runtime: agent
subservices:
  create:
    description: Create a new CLAUDE.md for the current codebase
    trigger: "claude-md:create"
    process:
      - Run Step 1 analysis commands
      - Detect framework and language via Step 2
      - Select template based on project type
      - Generate CLAUDE.md customizing all sections
      - Validate completeness (Step 5 checklist)
      - Present for review
  analyze:
    description: Analyze existing CLAUDE.md for completeness and issues
    trigger: "claude-md:analyze"
    process:
      - Read existing CLAUDE.md
      - Check for all required sections
      - Verify framework-specific coverage
      - Detect missing conventions
      - Report gaps with severity ratings
  validate:
    description: Validate CLAUDE.md format and content standards
    trigger: "claude-md:validate"
    process:
      - Verify essential sections present
      - Check command accuracy against package.json/composer.json
      - Validate framework-specific sections
      - Ensure no contradictory guidance
      - Score completeness (0-100)
  update:
    description: Update existing CLAUDE.md when codebase evolves
    trigger: "claude-md:update"
    process:
      - Compare existing CLAUDE.md to current codebase
      - Identify outdated commands/patterns
      - Add new framework versions/features
      - Remove obsolete guidance
      - Preserve team-specific conventions
---

# Claude MD Generator

A skill for generating comprehensive CLAUDE.md files for any codebase. This skill guides coding agents through a systematic analysis and generation process to create CLAUDE.md files that properly instruct future Claude Code agents on project-specific conventions, standards, and workflows.

**Companion Skill**: For framework-specific CLAUDE.md sections (Next.js, Laravel, Rails, etc.), use the **`framework-templates`** skill which provides deep reference templates for 15+ frameworks.

## Purpose

CLAUDE.md is a project-level instruction file that sits at the root of a codebase (or in `.claude/`). It tailors Claude Code's behavior to the specific project context, ensuring consistent implementation quality, adherence to project conventions, and efficient task execution across all future work.

A well-crafted CLAUDE.md eliminates the need to repeat context across conversations, provides authoritative guidance on project-specific patterns, and captures institutional knowledge about why certain decisions were made.

## When to Use

- **New Project**: Creating a CLAUDE.md for a fresh codebase
- **Project Acquisition**: Onboarding to an existing codebase without CLAUDE.md
- **Template Migration**: Adapting a generic CLAUDE.md to a specific project
- **CLAUDE.md Audits**: Validating existing CLAUDE.md for completeness
- **Framework Migration**: Updating CLAUDE.md when upgrading major frameworks (e.g., Laravel 10 → 11)
- **Team Conventions**: Capturing team-specific standards not documented elsewhere

## Decision Matrix

Follow the path matching your scenario:

| Scenario | Path | Steps to Follow |
|----------|------|-----------------|
| Fresh project, no existing code | **Full Generation** | Steps 1 → 2 → 3 → 4 → 5 |
| Existing project with conventions | **Analysis + Customize** | Steps 1 → 2 → 4 (skip template) |
| CLAUDE.md exists, needs audit | **Validate Only** | Use `claude-md:validate` subservice |
| Framework upgrade needed | **Targeted Update** | Steps 1 → 2 → 4 → 5 (update affected sections) |
| Adding team conventions | **Incremental Add** | Add to existing CLAUDE.md sections |

## How to Use

### Step 1: Project Analysis

Before generating CLAUDE.md, thoroughly analyze the codebase:

```bash
# Detect project type and framework
ls -la
cat package.json 2>/dev/null | head -30
cat composer.json 2>/dev/null | head -30
cat requirements.txt 2>/dev/null | head -30
cat pyproject.toml 2>/dev/null | head -30
cat go.mod 2>/dev/null | head -20
cat Cargo.toml 2>/dev/null | head -20

# Analyze directory structure
find . -maxdepth 3 -type d | head -40

# Identify key configuration files
find . -maxdepth 2 -name "*.config.*" -o -name "*.config.js" -o -name "*.config.ts" 2>/dev/null
find . -maxdepth 2 \( -name "vite.config.*" -o -name "next.config.*" -o -name "webpack.config.*" \) 2>/dev/null

# Check for existing documentation
cat README.md 2>/dev/null | head -50
cat CONTRIBUTING.md 2>/dev/null | head -30
ls -la *.md 2>/dev/null

# Verify build/test commands actually exist
cat package.json 2>/dev/null | jq '.scripts' 2>/dev/null || cat package.json 2>/dev/null | grep -A 20 '"scripts"'
cat composer.json 2>/dev/null | jq '.scripts' 2>/dev/null || cat composer.json 2>/dev/null | grep -A 20 '"scripts"'
```

### Step 2: Detect Framework & Language

#### Web Frameworks

| Detection Pattern | Framework | Key Indicators |
|-------------------|-----------|----------------|
| `package.json` + `next.config.js` | Next.js | React SSR framework |
| `package.json` + `vite.config.js` | Vite + React | Modern React SPA |
| `package.json` + `nuxt.config.ts` | Nuxt.js | Vue SSR framework |
| `composer.json` + `artisan` | Laravel | PHP full-stack |
| `composer.json` + `app/Http/` | Laravel | API + web |
| `requirements.txt` + `manage.py` | Django | Python full-stack |
| `pyproject.toml` + `app/` | FastAPI | Python API |
| `go.mod` + `cmd/` | Go | Microservices |
| `go.mod` + `internal/` | Go | Clean architecture |
| `Cargo.toml` + `src/` | Rust | Systems programming |
| `Gemfile` + `config.ru` | Ruby on Rails | Rails full-stack |

#### Mobile Frameworks

| Detection Pattern | Framework | Key Indicators |
|-------------------|-----------|----------------|
| `package.json` + `App.tsx` + `app.json` | React Native | Mobile app |
| `pubspec.yaml` + `lib/` | Flutter | Cross-platform mobile |
| `Podfile` + `ios/` + `AppDelegate.swift` | iOS native | Apple platform |
| `*.gradle` + `app/src/main/` | Android native | Java/Kotlin |

#### Desktop Frameworks

| Detection Pattern | Framework | Key Indicators |
|-------------------|-----------|----------------|
| `package.json` + `electron` | Electron | Desktop app |
| `*.csproj` + `Program.cs` | .NET | Windows desktop/web |
| `Cargo.toml` + `src-tauri/` | Tauri | Rust desktop |

### Step 3: Generate Section Content

For each CLAUDE.md section, derive content from:

| Section | Primary Sources | Secondary Sources |
|---------|-----------------|-------------------|
| Core Identity | project README, main config | package.json description |
| Foundational Principles | existing docs, .gitignore | CONTRIBUTING.md |
| Implementation Standards | existing code patterns | lint configs, tsconfig |
| Development Workflow | package.json scripts | Makefile, scripts/ |
| Testing Strategy | existing test files | test configs (jest, phpunit) |
| Code Quality | existing configs | .eslintrc, .prettierrc |
| Git & Version Control | git config, existing PRs | conventional commits |
| Error Handling | existing error patterns | middleware, interceptors |
| Security | security configs | .env.example, auth configs |
| Performance | performance configs | caching, CDN configs |

### Step 4: Document Project-Specific Conventions

```markdown
## Project Conventions (Generated from Codebase Analysis)

### File Organization
- `/src` - Source code
- `/tests` - Test files (mirrors src structure)
- `/docs` - Documentation
- `/scripts` - Build and deployment scripts

### Naming Conventions
- Components: PascalCase (e.g., UserProfile.tsx)
- Utilities: camelCase (e.g., formatDate.ts)
- Tests: *.test.ts or *.spec.ts
- Config files: kebab-case (e.g., lint-staged.config.js)

### State Management
- Local state: React useState/useReducer
- Cross-component: React Context
- Server state: TanStack Query (React Query)

### API Patterns
- REST: /api/{resource}/{id}
- GraphQL: /graphql endpoint
- Authentication: Bearer token in Authorization header
```

### Step 5: Validate Completeness

#### Validation Checklist

| # | Section | Required | Status |
|---|---------|----------|--------|
| 1 | Core Identity & Purpose | Yes | [ ] |
| 2 | Foundational Principles | Yes | [ ] |
| 3 | Implementation Standards | Yes | [ ] |
| 4 | Development Workflow | Yes | [ ] |
| 5 | Testing Strategy | Yes | [ ] |
| 6 | Code Quality Standards | Yes | [ ] |
| 7 | Git & Version Control | Yes | [ ] |
| 8 | Error Handling & Debugging | Yes | [ ] |
| 9 | Communication & Documentation | Yes | [ ] |
| 10 | Project-Specific Standards | Yes | [ ] |
| 11 | Success Metrics | No | [ ] |
| 12 | System Integration | No | [ ] |
| 13 | Anti-Patterns to Avoid | No | [ ] |
| 14 | Continuous Improvement | No | [ ] |
| 15 | Frontmatter (optional) | No | [ ] |

#### Framework-Specific Checklist

| Framework | Required Sections | Validate Against |
|-----------|-------------------|------------------|
| Next.js | App Router, Image, Metadata | `next.config.js` |
| Laravel | Form Requests, Policies, Jobs, Events | `app/` structure |
| Django | Models, Views, Forms, Admin | `settings.py` |
| React Native | Platform modules, Navigation | `app.json` |
| Flutter | Widgets, State, Routing | `pubspec.yaml` |
| Rails | MVC, ActiveRecord, Concerns | `config/routes.rb` |
| FastAPI | Pydantic, Dependencies, Routers | `main.py` |

## The CLAUDE.md Template

Below is the comprehensive CLAUDE.md template following the Meticulous Approach framework. Sections marked with `<!-- REQUIRED -->` are mandatory; sections marked with `<!-- OPTIONAL -->` enhance quality but are not required.

```markdown
---
IMPORTANT: File is read fresh for every conversation. Be brief and practical.
---

# {Project Name}

<!-- REQUIRED -->
## Core Identity & Purpose

Brief description of the project's purpose, what problem it solves, and who maintains it.

<!-- REQUIRED -->
## Foundational Principles

<!-- REQUIRED -->
### Meticulous Approach (Six-Phase Workflow)

Follow this six-phase workflow for all implementation tasks:

1. **ANALYZE** - Deep, multi-dimensional requirement mining
   - Never make surface-level assumptions
   - Identify explicit requirements, implicit needs, and potential ambiguities
   - Explore multiple solution approaches
   - Perform risk assessment

2. **PLAN** - Structured execution roadmap
   - Create detailed plan with sequential phases
   - Present plan for explicit user confirmation
   - Never proceed without validation

3. **VALIDATE** - Explicit confirmation checkpoint
   - Obtain explicit user approval before implementation
   - Address any concerns or modifications

4. **IMPLEMENT** - Modular, tested, documented builds
   - Set up proper environment
   - Implement in logical, testable components
   - Create documentation alongside code

5. **VERIFY** - Rigorous QA against success criteria
   - Execute comprehensive testing
   - Review for best practices, security, performance
   - Consider edge cases and accessibility

6. **DELIVER** - Complete handoff with knowledge transfer
   - Provide complete solution with instructions
   - Document challenges and solutions
   - Suggest improvements and next steps

<!-- OPTIONAL: Add project-specific principles here -->
### Project-Specific Principles

{Add principles unique to this project}

<!-- REQUIRED -->
## Implementation Standards

### General Coding Practices
- **Early Returns**: Prefer early returns over deeply nested conditionals
- **Composition over Inheritance**: Favor composition patterns
- **Self-Documenting Code**: Clear naming and structure
- **Test-Driven Development**: Follow Red-Green-Refactor cycle

<!-- REQUIRED: Include language & framework specific guidelines -->
### Language & Framework Guidelines

{Insert language-specific standards here based on detected framework}

<!-- REQUIRED -->
## Development Workflow

### Environment Setup

```bash
{Insert environment setup commands}
```

### Build Commands

| Command | Purpose |
|---------|---------|
| `{dev_command}` | Start development server |
| `{build_command}` | Production build |
| `{test_command}` | Run tests |
| `{lint_command}` | Run linter |
| `{typecheck_command}` | Type checking |

<!-- REQUIRED -->
## Testing Strategy

### Test Pyramid
- **Unit Tests**: Individual functions and components
- **Integration Tests**: Component interactions
- **E2E Tests**: Critical user journeys

### Test Commands

```bash
{Insert test commands}
```

<!-- REQUIRED -->
## Code Quality Standards

### Linting & Formatting

```bash
{Insert lint commands}
```

<!-- REQUIRED -->
## Git & Version Control

### Branching Strategy
- `{branch_naming_convention}` - Feature branches
- `{branch_naming_convention}` - Bug fixes
- Short-lived branches (merge within 1-3 days)

### Commit Standards
- Follow Conventional Commits format
- Atomic commits (one logical change per commit)

<!-- REQUIRED -->
## Error Handling & Debugging

### Error Handling Approach
- Anticipate potential failures
- Graceful error recovery
- User-friendly error messages

### Debugging Tools
- {Insert debugging tools}

<!-- REQUIRED -->
## Communication & Documentation

### Documentation Standards
- Explain "why", not just "what"
- Document assumptions and constraints

<!-- REQUIRED: Framework-specific conventions -->
## Project-Specific Standards

### Architecture
{Describe key architectural patterns}

### API Design
{Describe API conventions}

### Database / Data Layer
{Describe data access patterns}

### Environment Variables
| Variable | Purpose | Example |
|----------|---------|---------|
| {var_name} | {purpose} | {example} |

<!-- OPTIONAL -->
## Success Metrics

You are successful when:
- Codebase health improves over time
- Features are delivered on time
- Development workflow is smooth

<!-- OPTIONAL -->
## System Integration

### Available Tools
- **bash**: Execute terminal operations
- **read**: Read files and directories
- **glob**: Find files by pattern
- **edit**: Make exact string replacements
- **write**: Write files to filesystem

<!-- OPTIONAL -->
## Anti-Patterns to Avoid

- **Over-Engineering**: Don't build for hypothetical needs
- **Premature Optimization**: Optimize only with measurements
- **Magic Numbers/Strings**: Use named constants
- **Hardcoding**: Use configuration
```

## Section Deep-Dive

### Core Identity & Purpose

The opening section sets the agent's context. Include:

- **Project name** (as specified by the team, not inferred)
- **What it does** in one or two sentences
- **Who maintains it** (team, individual, community)
- **Key technical decisions** that shape everything else

### Foundational Principles

This section establishes the operational philosophy. The Meticulous Approach (six-phase workflow) should always be present, but you can add project-specific principles:

**Example additions for a high-availability system:**
```markdown
- **Failure Recovery**: Design for failure at every layer
- **Observability First**: Add logging before features
- **Zero-Downtime**: Never require maintenance windows
```

**Example additions for a startup MVP:**
```markdown
- **Velocity Over Perfection**: Ship working code over perfect code
- **Technical Debt Tolerance**: Accept debt with explicit tracking
- **Feature Flags**: Guard incomplete features behind flags
```

### Implementation Standards

This is the most critical section. Derive content from:

1. **Language detection**: What languages are used?
2. **Framework detection**: What frameworks are in use?
3. **Existing code patterns**: What do the current files look like?

#### TypeScript/JavaScript Projects

```markdown
**TypeScript Strict Mode**
- Enable strict mode in tsconfig.json
- Never use `any` - prefer `unknown` instead
- Prefer `interface` for structural definitions, `type` for unions
- Explicit return types on public functions

**React Development**
- Handle all UI states: loading, error, empty, success
- Show loading state ONLY when no data exists
- Disable buttons during async operations
- Use library components (Shadcn, Radix, MUI) when available
- Apply bespoke styling only when necessary
```

#### Next.js Projects

```markdown
**Next.js 14+ Specific**
- Use App Router conventions (app/ directory)
- Server Components by default, Client Components with 'use client'
- Use Next.js Image component for all images
- Use next/font for font loading
- Metadata API for SEO
- Use Server Actions for form submissions
- Partial Prerendering (PPR) where applicable
```

#### Laravel/PHP Projects

```markdown
**Laravel 11+ Standards**
- Use Laravel Best Practices (tighten.co)
- Use Form Request classes for validation (not inline validation in controllers)
- Use Policy classes for authorization
- Use Eloquent relationships over raw queries
- Use Jobs for long-running operations
- Use Events for decoupled side effects
- Use Actions for business logic
- Follow Service Layer pattern for complex operations

**PHP 8.3+ Standards**
- Use named arguments for clarity
- Use constructor property promotion
- Use enums for fixed sets of values
- Use attributes over docblocks for metadata
- Never use `mixed` type - use Union types instead
```

#### Ruby on Rails Projects

```markdown
**Rails 7+ Standards**
- Follow Rails Conventions (CoC, DRY, Convention over Configuration)
- Use Concerns for shared behavior across models/controllers
- Use Service Objects for complex business logic
- Use Decorators (Draper) for view logic
- Use Presenters for multi-model view data
- Background jobs: Sidekiq with Active Job
- Use Turbo + Stimulus for reactive UIs

**Ruby 3.3+ Standards**
- Use Ractors for true parallelism (if needed)
- Type signatures with RBS (Ruby Signature)
- Use pattern matching (case/in) for complex conditionals
- Ractor-safe code for concurrent operations
```

#### Python Projects

```markdown
**Python 3.11+ Standards**
- Type hints on all public functions (PEP 484)
- Use dataclasses or Pydantic for data structures
- Use attrs for performance-critical objects
- Follow PEP 8 with Black formatting
- Use async/await for I/O operations
- Poetry or uv for dependency management
```

#### FastAPI Projects

```markdown
**FastAPI Standards**
- Use Pydantic models for all request/response validation
- Use dependency injection for shared logic
- Use routers for modular endpoint organization
- Use BackgroundTasks for deferred operations
- Use WebSockets for real-time features
```

#### React Native Projects

```markdown
**React Native Standards**
- Use TypeScript exclusively
- Platform modules: `Platform.select()` for platform-specific code
- Use `react-native-screens` and `react-native-safe-area-context` for navigation
- Native modules: Use TurboModules over Bridge (RN 0.76+)
- Assets: Use vector icons or generated image assets
- Debug: Flipper for debugging (legacy), Hermes console for RN 0.76+

**Navigation**
- Use React Navigation 6+
- Type-safe navigation with TypeScript
- Deep linking configuration required
```

#### Flutter Projects

```markdown
**Flutter Standards**
- Dart 3.4+ with null safety
- Use flutter_lints for code quality
- BLoC or Riverpod for state management
- GoRouter for declarative routing
- Freezed for immutable data classes
- Clean Architecture: Presentation → Domain → Data layers

**Platform-Specific**
- Platform channels for native features
- Use kIsWeb for web-specific logic
- Use `Platform.isIOS` / `Platform.isAndroid` sparingly
```

#### Go Projects

```markdown
**Go 1.22+ Standards**
- Use generics where appropriate (Go 1.18+)
- Error wrapping with `fmt.Errorf("context: %w", err)`
- Context propagation for request-scoped values
- Use `errgroup` for concurrent operations
- Structured logging with slog (Go 1.21+)

**Project Structure (Clean Architecture)**
```
cmd/        # Main applications
internal/   # Private application code
pkg/        # Public packages
api/        # Protocol definitions
```
```

### Development Workflow

Derive from `package.json`, `composer.json`, or project scripts. Verify commands exist before documenting:

```bash
# Verify commands before documenting
cat package.json | jq '.scripts' 2>/dev/null
cat composer.json | jq '.scripts' 2>/dev/null
```

### Testing Strategy

Detect testing setup:

| Framework | Config File | Test Location |
|-----------|-------------|---------------|
| Jest | `jest.config.js` | `*.test.js`, `*.spec.js` |
| Vitest | `vitest.config.js` | `*.test.js`, `*.spec.js` |
| PHPUnit | `phpunit.xml` | `tests/` |
| pytest | `pytest.ini` | `tests/` |
| RSpec | `.rspec` | `spec/` |
| Go test | `_test.go` | Same package |
| Flutter test | `*_test.dart` | `test/` |
| React Native | `jest.config.js` | `__tests__/` |

### Frontmatter Guidance

Some CLAUDE.md files include frontmatter for metadata:

```markdown
---
IMPORTANT: true
project_type: nextjs
version: 1.0.0
framework_version: "14.1"
last_updated: 2026-04-13
---
```

**When to use frontmatter:**
- Multi-version projects (track which version the CLAUDE.md targets)
- Project type classification (for tooling)
- Important flags (e.g., `IMPORTANT: true` for mandatory reading)

**When NOT to use frontmatter:**
- Simple projects with one active version
- Teams that don't want to maintain metadata

## Complete Examples

### Example 1: Next.js 14 Full-Stack Project

```markdown
---
IMPORTANT: File is read fresh for every conversation.
---

# Acme Dashboard

Internal analytics dashboard for the Acme team. Tracks user metrics, revenue, and engagement across all products.

**Tech Stack**: Next.js 14 (App Router), TypeScript, Tailwind CSS, Prisma, PostgreSQL, Vercel

## Foundational Principles

### Meticulous Approach (Six-Phase Workflow)

1. **ANALYZE** - Never make surface-level assumptions
2. **PLAN** - Create detailed plan, present for confirmation
3. **VALIDATE** - Get explicit user approval before coding
4. **IMPLEMENT** - Test each component before integration
5. **VERIFY** - Run all checks before delivery
6. **DELIVER** - Complete handoff with documentation

## Implementation Standards

### Next.js 14 Specific
- Use App Router conventions (app/ directory)
- Server Components by default, Client Components with 'use client'
- Use Next.js Image component for all images
- Use next/font for Google Fonts
- Metadata API for SEO (generateMetadata function)
- Server Actions for form submissions
- Route handlers for API endpoints

### TypeScript Strict Mode
- `strict: true` in tsconfig.json
- Never use `any` - use `unknown` instead
- Explicit types on all function parameters
- Use `interface` for object shapes, `type` for unions
- No implicit any from React or Prisma

### Tailwind CSS
- Use design tokens from tailwind.config.js
- No arbitrary values (extend theme instead)
- Mobile-first responsive design
- Dark mode via `next-themes`

## Development Workflow

### Environment Setup
```bash
npm install
npx prisma generate
npx prisma db push
cp .env.example .env.local
npm run dev
```

### Build Commands
| Command | Purpose |
|---------|---------|
| `npm run dev` | Start development server (port 3000) |
| `npm run build` | Production build |
| `npm run start` | Start production server |
| `npm run lint` | ESLint + Prettier |
| `npm run typecheck` | TypeScript checking |
| `npm run db:studio` | Open Prisma Studio |

### Database (Prisma)
```bash
npx prisma generate   # Generate Prisma client
npx prisma db push    # Push schema to database
npx prisma db seed    # Seed with sample data
```

## Testing Strategy

### Test Commands
```bash
npm test             # Run all tests
npm run test:watch   # Watch mode
npm run test:coverage  # Coverage report
```

### Testing Standards
- Jest for unit and integration tests
- Playwright for E2E tests
- Test files co-located: `Component.test.tsx` next to `Component.tsx`
- Mock Prisma client for unit tests
- Use `@testing-library/react` for component tests

## API Design

### Route Handlers
- Location: `app/api/{resource}/route.ts`
- Request validation: Zod schemas
- Response format: Consistent JSON structure
- Error handling: Custom error classes with HttpStatus codes

### API Response Format
```typescript
interface ApiResponse<T> {
  data: T;
  meta?: {
    page: number;
    total: number;
  };
}
```

## Environment Variables
| Variable | Purpose | Example |
|----------|---------|---------|
| `DATABASE_URL` | PostgreSQL connection | `postgresql://...` |
| `NEXTAUTH_SECRET` | Auth token signing | 32-char secret |
| `NEXTAUTH_URL` | Auth callback URL | `http://localhost:3000` |
```

### Example 2: Laravel 12 API Project

```markdown
---
IMPORTANT: File is read fresh for every conversation.
---

# Acme API

RESTful API for the Acme platform. Provides endpoints for user management, billing, and content delivery.

**Tech Stack**: Laravel 12, PHP 8.3, PostgreSQL, Redis, Laravel Reverb

## Foundational Principles

### Meticulous Approach (Six-Phase Workflow)

1. **ANALYZE** - Deep requirement mining
2. **PLAN** - Detailed roadmap with validation
3. **VALIDATE** - Explicit approval checkpoint
4. **IMPLEMENT** - Modular, tested builds
5. **VERIFY** - Comprehensive QA
6. **DELIVER** - Complete handoff

## Implementation Standards

### Laravel 12 Specific
- Use Laravel Reverb for WebSocket connections
- Follow Laravel Best Practices (tighten.co)
- Use Form Request classes for ALL validation
- Use Policy classes for authorization
- Use Eloquent relationships exclusively
- Use Jobs for long-running operations
- Use Events for decoupled side effects
- Use Actions for business logic
- Follow Service Layer pattern

### PHP 8.3 Standards
- Constructor property promotion on all classes
- Named arguments when order matters
- Attributes for route/webhook/middleware metadata
- Use enums for status/type fields
- Strict types declaration in all files

## Development Workflow

### Environment Setup
```bash
composer install
cp .env.example .env
php artisan key:generate
php artisan migrate
php artisan db:seed
php artisan serve
```

### Artisan Commands
| Command | Purpose |
|---------|---------|
| `php artisan migrate` | Run migrations |
| `php artisan migrate:fresh --seed` | Reset database |
| `php artisan test` | Run tests |
| `php artisan test --parallel` | Parallel execution |
| `php artisan schedule:work` | Run scheduler |
| `php artisan queue:work` | Process queue |
| `php artisan db:studio` | Open database GUI |

## Service Layer

### When to Use Services
- Complex business logic spanning multiple models
- External API integrations
- Operations requiring transactions
- Reusable business operations

### Service Location
- `app/Services/` - Application services
- `app/Integrations/` - External API clients
- `app/Billing/` - Payment processing

## Testing

### Test Commands
```bash
php artisan test              # Run all tests
php artisan test --parallel   # Parallel execution
php artisan test --coverage   # Coverage report
```

### Testing Standards
- Pest PHP for testing
- Test files: `tests/Feature/` and `tests/Unit/`
- Use factory classes for test data
- Mock external services
- Test API endpoints with assertStatus
```

## Tips

### Generate, Don't Copy

Every CLAUDE.md should be derived from actual codebase analysis, not copied from templates. The agent should:

1. Run analysis commands to detect actual project structure
2. Read existing configuration files to understand actual conventions
3. Examine existing code to detect actual patterns
4. Document what exists, not what should exist

### Framework-Specific Depth

The more specialized the framework, the more specific the guidance:

**Generic project:**
```markdown
- Follow language best practices
- Use established patterns
```

**Laravel project:**
```markdown
- Use Form Request classes for validation (not `$request->validate()` in controllers)
- Use Policy classes for authorization (not `$this->authorize()` in controllers)
- Use Events for decoupled side effects (not direct method calls)
- Use Jobs for long-running operations (not synchronous processing)
- Use Eloquent scopes for reusable query logic
```

### Include Commands, Not Just Standards

Agents need executable commands. Every standard should have an associated command:

**Weak:**
```markdown
- Run tests before committing
```

**Strong:**
```markdown
- Run tests before committing:
  ```bash
  npm test
  ```
```

### Document Exceptions

If the project has intentional deviations from convention, document them:

```markdown
**Exceptions to Standard Patterns**

1. **Legacy Compatibility**: The `UserController` uses `$request->validate()` instead of Form Request classes because it predates the convention adoption. New controllers must use Form Request classes.

2. **Performance Critical Path**: The `ReportGenerator` service bypasses the standard service layer for performance reasons. Changes require performance testing.
```

### Version-Specific Guidance

If the project uses specific versions with known quirks:

```markdown
**Version-Specific Notes**

- **Next.js 14.1**: CSS Modules must be imported directly in server components; importing through a barrel file causes HMR issues
- **Laravel 11**: Service container binding syntax changed; use `Bind` attribute instead of `register()` method
```

## Anti-Examples

These patterns produce **ineffective** CLAUDE.md files:

### ❌ Too Generic
```markdown
## Implementation Standards
- Follow best practices
- Write clean code
- Test thoroughly
```
**Problem**: No actionable guidance, no project-specific details.

### ❌ Missing Commands
```markdown
## Development Workflow
- Set up the environment
- Run tests
- Build the project
```
**Problem**: Agent doesn't know HOW to do these things.

### ❌ Copy-Paste Template
```markdown
## Error Handling
- Anticipate potential failures
- Graceful error recovery
```
**Problem**: No actual error handling patterns from the codebase.

### ❌ Contradictory Guidance
```markdown
## TypeScript Standards
- Never use `any`
- But for legacy code, `any` is allowed
```
**Problem**: Agent confused about when rules apply.

### ✅ Effective CLAUDE.md
```markdown
## Implementation Standards

### Next.js 14
- Use App Router conventions (app/ directory)
- Server Components by default, use 'use client' for interactivity
- Use Next.js Image component for all images

### TypeScript Strict Mode
- `strict: true` in tsconfig.json
- Never use `any` - use `unknown` instead
- All API routes return typed responses

## Build Commands
| Command | Purpose |
|---------|---------|
| `npm run dev` | Development server |
| `npm run build` | Production build |
| `npm run lint` | ESLint + Prettier |
```

## Troubleshooting

### Generated CLAUDE.md is Too Generic

**Problem**: The CLAUDE.md contains obvious, template-level content without project-specific details.

**Solution**: Run deeper analysis:
```bash
# Find unique patterns in the codebase
grep -r "use Illuminate" --include="*.php" . | head -20
grep -r "from '" --include="*.js" --include="*.ts" . | grep -v node_modules | head -20

# Examine actual project structure
tree -L 3 -d .
find . -name "*.blade.php" -o -name "*.tsx" -o -name "*.vue" | head -30
```

### Missing Key Sections

**Problem**: Important sections are absent (e.g., no testing guidance for a test-heavy project).

**Solution**: Check for test directories and frameworks:
```bash
find . -type d -name "test*" -o -type d -name "spec*" 2>/dev/null
find . -name "jest.config.*" -o -name "vitest.config.*" -o -name "phpunit.xml*" 2>/dev/null
```

### Commands Are Wrong

**Problem**: Documented commands don't exist in package.json or composer.json.

**Solution**: Always verify commands:
```bash
cat package.json | jq '.scripts' 2>/dev/null
cat composer.json | jq '.scripts' 2>/dev/null
```

If commands are missing, either:
1. Document the command that should exist (recommendation)
2. Create an issue to add the command
3. Add the command to the CLAUDE.md as a TODO

### Framework Not Detected

**Problem**: Unable to determine the framework from file analysis.

**Solution**: Check for language-specific indicators:

**PHP:**
```bash
grep -r "<?php" --include="*.php" . 2>/dev/null | head -5
cat composer.json 2>/dev/null | grep require | head -10
```

**JavaScript/TypeScript:**
```bash
cat package.json 2>/dev/null | grep dependencies | head -20
find . -name "*.tsx" -o -name "*.jsx" 2>/dev/null | head -10
```

**Python:**
```bash
cat requirements.txt 2>/dev/null | head -20
cat pyproject.toml 2>/dev/null | head -30
find . -name "*.py" 2>/dev/null | head -10
```

**Ruby:**
```bash
cat Gemfile 2>/dev/null | head -30
find . -name "*.rb" 2>/dev/null | head -10
```

**Go:**
```bash
cat go.mod 2>/dev/null | head -20
find . -name "*.go" 2>/dev/null | head -10
```

**Rust:**
```bash
cat Cargo.toml 2>/dev/null | head -30
find . -name "*.rs" 2>/dev/null | head -10
```

## Related Skills

- **framework-templates**: **PRIMARY COMPANION** - Deep reference library with CLAUDE.md sections for Next.js, Laravel, Rails, Django, React Native, Flutter, Go, Rust, and 8 more frameworks. Use this for framework-specific templates and conventions.
- **clean-code**: For code quality standards and naming conventions
- **designing-architecture**: For system design and architectural patterns
- **testing-patterns**: For testing strategy and test structure guidance
- **lint-and-validate**: For linting and code quality enforcement

## Changelog

### 1.1.0 (2026-04-13)
- Added subservice implementations with detailed process steps
- Added mobile framework detection (React Native, Flutter)
- Added Ruby on Rails standards
- Added Go-specific standards
- Added Rust-specific standards
- Added .NET/C# standards
- Reduced template verbosity with REQUIRED/OPTIONAL markers
- Added decision matrix for path selection
- Added validation checklist in table format
- Added frontmatter guidance
- Added complete example files (not snippets)
- Added anti-examples section
- Fixed framework detection tables

### 1.0.0 (2026-04-12)
- Initial release
- Comprehensive CLAUDE.md template
- Framework-specific guidance for Next.js, Laravel, Python
- Step-by-step generation process
- Validation checklist
