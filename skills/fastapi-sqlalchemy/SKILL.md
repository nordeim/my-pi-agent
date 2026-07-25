---
name: fastapi-sqlalchemy
description: "FastAPI (0.115+) + SQLAlchemy 2.0 (async with asyncpg) + Pydantic v2 + Alembic modern Python async API workflow skill. Covers the async-first mental model (async def endpoints, async DB sessions, asyncpg driver), Pydantic v2 validation (type-driven with Annotated types, model_validator, field_validator, computed_field — Rust-powered, 5-50x faster than v1), SQLAlchemy 2.0 unified API (Session sync, AsyncSession async, Mapped[] type annotations, DeclarativeBase, select() statement API replacing legacy Query), dependency injection via Depends() for DB sessions, auth, rate limiting, the lifespan context manager (replacing on_event startup/shutdown), Alembic for migrations (async-compatible), OpenAPI/Swagger auto-generation (FastAPI's killer feature — request/response models auto-documented), the modern stack (uv for package management, Ruff for lint+format, pytest + httpx.AsyncClient for testing), and deployment via Uvicorn/Gunicorn workers or serverless. Use when building any Python async REST API, microservice, or modern backend with FastAPI — especially when the task involves async DB sessions, Pydantic v2 validation patterns, SQLAlchemy 2.0 Mapped[] types, dependency injection design, or async migrations where idiomatic FastAPI differs from Django sync patterns or from older FastAPI + SQLAlchemy 1.x code."
license: Proprietary. LICENSE.txt has complete terms
---

# FastAPI + SQLAlchemy 2.0 + Pydantic v2 — Modern Python Async API Workflow

> **Target:** FastAPI 0.115+ (released late 2024) on Python 3.12+, with **SQLAlchemy 2.0** (the unified sync/async API rewrite released January 2023), **Pydantic v2** (the Rust-powered rewrite released June 2023, 5-50x faster than v1), and **Alembic** for migrations. The modern stack uses **uv** for package management (10-100x faster than pip) and **Ruff** for linting + formatting (replaces Black, isort, flake8 in one tool).

## When to Use This Skill

Use this skill whenever the user is building, debugging, or extending a FastAPI application, especially with async SQLAlchemy. Trigger phrases include "FastAPI", "Pydantic v2", "SQLAlchemy 2", "AsyncSession", "asyncpg", "Alembic", "Uvicorn", "uvicorn", "Depends", "lifespan", "BaseModel", "model_validator", "field_validator", "Annotated", "select()", "DeclarativeBase", "Mapped", "uv package manager", "Ruff", "uvicorn --workers", and any reference to a `main.py` with `app = FastAPI()` or a `pyproject.toml` with `[tool.uv]` or `[tool.ruff]` config.

Do **not** use this skill for:
- **FastAPI + SQLAlchemy 1.4** — the legacy `Query` API and sync `Session` patterns differ. This skill assumes SQLAlchemy 2.0+.
- **Django / Django REST Framework** — see `django-6` skill (sync ORM, CBVs, admin, different mental model).
- **Flask** — sync-only by default, different ecosystem.
- **Pydantic v1** — v2 is a complete rewrite. v1 patterns (`.dict()` instead of `.model_dump()`, `Config` class instead of `model_config`) don't work in v2.
- **Other backend languages** (Go, Rust, Java, Ruby, PHP, JS) — see `go-web`, `rust-web`, `spring-boot-3`, `dotnet-9`, `rails-8`, `laravel-12`, `svelte-5-sveltekit`, `vue-3-nuxt` skills.

Cross-reference: `python-patterns` has a brief FastAPI section; this skill goes deep. `django-6` covers the sync Python web alternative.

## Quick Start

```bash
# Install uv (modern package manager — 10-100x faster than pip)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Create a new project
uv init myapp
cd myapp

# Add dependencies
uv add fastapi[standard] uvicorn[standard]
uv add sqlalchemy[asyncio] asyncpg alembic
uv add pydantic pydantic-settings
uv add python-jose[cryptography] passlib[bcrypt]   # for JWT auth
uv add --dev pytest pytest-asyncio httpx ruff

# Create the app
mkdir app tests
cat > app/main.py << 'EOF'
from contextlib import asynccontextmanager
from fastapi import FastAPI

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup (DB pool, cache connections, etc.)
    yield
    # Shutdown (cleanup)

app = FastAPI(lifespan=lifespan, title="My API", version="0.1.0")

@app.get("/health")
async def health():
    return {"status": "ok"}
EOF

# Run dev server
uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
# Visit http://localhost:8000/docs (interactive Swagger UI — auto-generated!)
# Visit http://localhost:8000/redoc (alternative docs UI)
```

### Key commands (using `uv`)

```bash
uv add <package>             # Add a dependency (updates pyproject.toml + uv.lock)
uv add --dev <package>       # Add a dev dependency
uv remove <package>          # Remove a dependency
uv sync                      # Install all deps from uv.lock (reproducible)
uv lock                      # Regenerate uv.lock
uv run <command>             # Run a command in the project venv
uv run uvicorn app.main:app  # Run the API
uv run pytest                # Run tests
uv run ruff check            # Lint
uv run ruff format           # Format
uv run alembic upgrade head  # Apply migrations
uv run alembic revision --autogenerate -m "create users"  # Generate migration
```

### Traditional pip alternative (if uv is unavailable)

```bash
python -m venv .venv
source .venv/bin/activate
pip install fastapi[standard] sqlalchemy[asyncio] asyncpg alembic
pip install -r requirements.txt
uvicorn app.main:app --reload
```

---

## Project Structure (modern FastAPI layout)

```
myapp/
├── pyproject.toml              # ← THE config (deps, Ruff config, pytest config, all in one)
├── uv.lock                     # Locked dep versions (commit this)
├── README.md
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI app instance, lifespan, route includes
│   ├── config.py               # Settings (pydantic-settings BaseSettings)
│   ├── database.py             # AsyncEngine, async_sessionmaker, Base
│   ├── deps.py                 # Shared dependencies (get_db, get_current_user)
│   ├── models/                 # SQLAlchemy ORM models
│   │   ├── __init__.py
│   │   ├── base.py             # DeclarativeBase
│   │   ├── user.py
│   │   └── post.py
│   ├── schemas/                # Pydantic models (request/response DTOs)
│   │   ├── __init__.py
│   │   ├── user.py
│   │   └── post.py
│   ├── api/                    # Route handlers (routers)
│   │   ├── __init__.py
│   │   ├── deps.py             # API-specific deps
│   │   └── v1/
│   │       ├── __init__.py
│   │       ├── router.py       # Combines all v1 routers
│   │       └── endpoints/
│   │           ├── users.py
│   │           └── posts.py
│   ├── services/               # Business logic (between API and DB)
│   │   ├── user_service.py
│   │   └── post_service.py
│   ├── core/                   # Cross-cutting (security, logging, exceptions)
│   │   ├── security.py         # Password hashing, JWT creation
│   │   ├── exceptions.py       # Custom exceptions + handlers
│   │   └── logging.py
│   └── alembic/                # Migrations
│       ├── env.py              # Async-aware Alembic env
│       ├── script.py.mako
│       └── versions/           # Migration files
├── tests/
│   ├── __init__.py
│   ├── conftest.py             # Pytest fixtures (async client, test DB)
│   ├── test_users.py
│   └── test_posts.py
├── alembic.ini                 # Alembic config (points to app/alembic/)
└── Dockerfile
```

### `pyproject.toml` (the canonical config)

```toml
[project]
name = "myapp"
version = "0.1.0"
description = "A FastAPI application"
requires-python = ">=3.12"
dependencies = [
    "fastapi[standard]>=0.115.0",
    "sqlalchemy[asyncio]>=2.0.30",
    "asyncpg>=0.29.0",
    "alembic>=1.13.0",
    "pydantic>=2.7.0",
    "pydantic-settings>=2.3.0",
    "python-jose[cryptography]>=3.3.0",
    "passlib[bcrypt]>=1.7.4",
]

[project.optional-dependencies]
dev = [
    "pytest>=8.0",
    "pytest-asyncio>=0.23",
    "httpx>=0.27",
    "ruff>=0.5",
]

[tool.ruff]
line-length = 100
target-version = "py312"

[tool.ruff.lint]
select = ["E", "F", "I", "N", "W", "UP", "B", "SIM", "TCH"]

[tool.ruff.format]
quote-style = "double"

[tool.pytest.ini_options]
asyncio_mode = "auto"
testpaths = ["tests"]

[tool.uv]
dev-dependencies = [
    "pytest>=8.0",
    "pytest-asyncio>=0.23",
    "httpx>=0.27",
    "ruff>=0.5",
]
```

---

## Core Mental Model: Async-First + Type-Driven Validation + Dependency Injection

FastAPI's distinctive paradigm is **async-first I/O, type-driven request/response validation via Pydantic, and explicit dependency injection.** Three things differentiate FastAPI from Django/Flask:

### 1. Async-first (everything is `async def`)

```python
from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession

app = FastAPI()

@app.get("/users/{user_id}")
async def get_user(user_id: int, db: AsyncSession = Depends(get_db)):
    # Async DB query — uses asyncpg under the hood
    user = await db.get(User, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user
```

**Key difference from sync frameworks:** FastAPI runs on an async event loop (Uvicorn + asyncio). Long-running I/O (DB queries, HTTP calls) MUST be async — otherwise you block the event loop and stall other requests. CPU-bound work (image processing, ML inference) should be offloaded to a thread pool via `await run_in_threadpool(...)` or `asyncio.to_thread(...)`.

### 2. Type-driven validation (Pydantic v2)

FastAPI uses Python type annotations on function parameters to:
- Parse and validate the request (path params, query params, request body)
- Generate the OpenAPI schema automatically
- Provide editor autocomplete and static analysis

```python
from pydantic import BaseModel, EmailStr, Field, field_validator, model_validator
from typing import Annotated
from datetime import datetime

# Request schema (input validation)
class CreateUserRequest(BaseModel):
    email: EmailStr
    name: str = Field(min_length=2, max_length=100)
    password: str = Field(min_length=8, max_length=100)
    age: int = Field(ge=13, le=120)

    @field_validator("password")
    @classmethod
    def password_must_have_number(cls, v: str) -> str:
        if not any(c.isdigit() for c in v):
            raise ValueError("Password must contain at least one number")
        return v

    @model_validator(mode="after")
    def validate_model(self) -> "CreateUserRequest":
        if self.age < 18 and "@kids.com" not in self.email:
            raise ValueError("Users under 18 must use @kids.com email")
        return self

# Response schema (output serialization)
class UserResponse(BaseModel):
    model_config = {"from_attributes": True}   # Allows building from ORM objects (v2 syntax — replaces v1's orm_mode=True)

    id: int
    email: EmailStr
    name: str
    created_at: datetime

# In the endpoint — type hints ARE the validation
@app.post("/users", response_model=UserResponse, status_code=201)
async def create_user(
    request: CreateUserRequest,                      # Body — auto-parsed + validated
    db: AsyncSession = Depends(get_db),
):
    user = await user_service.create(db, request)
    return user                                      # FastAPI serializes via response_model
```

If validation fails, FastAPI returns a 422 with detailed error JSON automatically — you don't write any validation code in the endpoint.

### 3. Dependency injection via `Depends()`

```python
from fastapi import Depends

# Define a dependency
async def get_db() -> AsyncSession:
    async with async_session_maker() as session:
        try:
            yield session                            # yield = context manager (auto-commits/rolls back)
            await session.commit()
        except Exception:
            await session.rollback()
            raise

# Use it in an endpoint
@app.get("/users")
async def list_users(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User))
    return result.scalars().all()

# Dependencies can depend on other dependencies
async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db),
) -> User:
    # Validate token, fetch user
    ...

# Use a dependency for its side effect (e.g., require auth, discard return value)
@app.delete("/users/{id}")
async def delete_user(
    id: int,
    db: AsyncSession = Depends(get_db),
    _user: User = Depends(get_current_user),         # Just enforces auth
):
    ...

# Dependencies support caching per-request (use_cache=True — default)
# Multiple endpoints sharing the same dependency get the SAME instance per request
```

`Depends()` is FastAPI's superpower — it makes testing trivial (override dependencies with mocks) and keeps endpoints thin.

---

## SQLAlchemy 2.0 (the unified sync/async API)

### Setup: async engine + session

```python
# app/database.py
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass

# Async engine (asyncpg driver)
engine = create_async_engine(
    "postgresql+asyncpg://user:pass@localhost:5432/myapp",
    echo=False,                                      # SQL logging (False in prod)
    pool_size=20,
    max_overflow=10,
    pool_pre_ping=True,                              # Detect stale connections
)

# Async session factory
async_session_maker = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,                          # Don't expire objects after commit (prevents lazy-load crashes)
)
```

### Models (SQLAlchemy 2.0 `Mapped[]` API)

```python
# app/models/base.py
from sqlalchemy.orm import DeclarativeBase, MappedAsDataclass

class Base(DeclarativeBase):
    pass

# app/models/user.py
from sqlalchemy import String, ForeignKey, Enum as SAEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Optional
import enum

class UserStatus(enum.Enum):
    ACTIVE = "active"
    SUSPENDED = "suspended"
    DELETED = "deleted"

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    name: Mapped[str] = mapped_column(String(100))
    password_hash: Mapped[str] = mapped_column(String(255))
    status: Mapped[UserStatus] = mapped_column(SAEnum(UserStatus), default=UserStatus.ACTIVE)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    updated_at: Mapped[Optional[datetime]] = mapped_column(onupdate=datetime.utcnow)

    # Relationships
    posts: Mapped[list["Post"]] = relationship(back_populates="author", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"<User(id={self.id}, email={self.email!r})>"

class Post(Base):
    __tablename__ = "posts"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(200))
    body: Mapped[str] = mapped_column(Text)
    author_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    published_at: Mapped[Optional[datetime]] = mapped_column()

    author: Mapped["User"] = relationship(back_populates="posts")
```

The `Mapped[]` annotation is the SQLAlchemy 2.0 way — it gives you type safety (mypy/pyright understand it) and replaces the legacy `Column(Integer)` syntax.

### Queries (the `select()` API)

```python
from sqlalchemy import select, update, delete, func

# SELECT * FROM users WHERE id = ?
async def get_user(db: AsyncSession, user_id: int) -> User | None:
    return await db.get(User, user_id)               # Primary key lookup (simplest)

# SELECT * FROM users WHERE status = 'active' ORDER BY created_at DESC
async def list_active_users(db: AsyncSession) -> list[User]:
    result = await db.execute(
        select(User)
        .where(User.status == UserStatus.ACTIVE)
        .order_by(User.created_at.desc())
    )
    return list(result.scalars().all())

# Eager load relationships (avoid N+1)
async def list_users_with_posts(db: AsyncSession) -> list[User]:
    result = await db.execute(
        select(User)
        .options(selectinload(User.posts))            # Eager load via second query
    )
    return list(result.scalars().all())

# JOIN
async def list_users_with_published_posts(db: AsyncSession) -> list[tuple[User, Post]]:
    result = await db.execute(
        select(User, Post)
        .join(Post, User.id == Post.author_id)
        .where(Post.published_at.is_not(None))
    )
    return list(result.all())

# Aggregation
async def count_active_users(db: AsyncSession) -> int:
    result = await db.execute(
        select(func.count())
        .select_from(User)
        .where(User.status == UserStatus.ACTIVE)
    )
    return result.scalar_one()

# UPDATE
async def update_user_status(db: AsyncSession, user_id: int, status: UserStatus) -> None:
    await db.execute(
        update(User)
        .where(User.id == user_id)
        .values(status=status)
    )

# DELETE
async def delete_user(db: AsyncSession, user_id: int) -> None:
    await db.execute(delete(User).where(User.id == user_id))

# Bulk insert
async def bulk_create(db: AsyncSession, users: list[User]) -> None:
    db.add_all(users)
```

### The `selectinload` vs `joinedload` decision

| Loader | How it works | Use when |
|---|---|---|
| `selectinload` | Runs a second `SELECT ... WHERE id IN (...)` | Default for collections (`relationship` to many) |
| `joinedload` | JOINs in the same query | Single-valued relationships (many-to-one) — avoids second query |
| `subqueryload` | Subquery in a second SELECT | Legacy — `selectinload` is faster in almost all cases |
| `raiseload` | Raises `LazyLoadError` if accessed without eager loading | Strict N+1 prevention in tests/dev |

```python
from sqlalchemy.orm import selectinload, joinedload, raiseload

# Good: selectinload for collections, joinedload for many-to-one
result = await db.execute(
    select(User)
    .options(
        selectinload(User.posts),                    # Collection — second query
        joinedload(User.profile),                    # Many-to-one — JOIN
    )
)
```

---

## Pydantic v2 (Rust-powered validation)

Pydantic v2 is a complete rewrite — the core is implemented in Rust, making it 5-50x faster than v1. The API also changed significantly.

### v1 → v2 migration cheat sheet

| v1 | v2 |
|---|---|
| `class Config: orm_mode = True` | `model_config = ConfigDict(from_attributes=True)` |
| `.dict()` | `.model_dump()` |
| `.json()` | `.model_dump_json()` |
| `@validator("field")` | `@field_validator("field")` |
| `@root_validator` | `@model_validator(mode="after")` |
| `Field(..., regex="...")` | `Field(..., pattern="...")` |
| `Optional[T] = None` | `T \| None = None` (or `Optional[T]` still works) |

### Schemas (request/response DTOs)

```python
from pydantic import BaseModel, EmailStr, Field, ConfigDict, field_validator, model_validator, computed_field
from datetime import datetime
from typing import Annotated

# Use Annotated types for reusable validation
PositiveInt = Annotated[int, Field(gt=0)]
NonEmptyStr = Annotated[str, Field(min_length=1)]

class UserBase(BaseModel):
    email: EmailStr
    name: NonEmptyStr

class CreateUserRequest(UserBase):
    password: str = Field(min_length=8, max_length=100)
    age: int = Field(ge=13, le=120)

    @field_validator("password")
    @classmethod
    def password_complexity(cls, v: str) -> str:
        if not any(c.isdigit() for c in v):
            raise ValueError("must contain a number")
        if not any(c.isupper() for c in v):
            raise ValueError("must contain an uppercase letter")
        return v

    @model_validator(mode="after")
    def check_age_email_consistency(self) -> "CreateUserRequest":
        if self.age < 18 and not self.email.endswith("@kids.com"):
            raise ValueError("minors must use @kids.com email")
        return self

class UpdateUserRequest(BaseModel):
    name: NonEmptyStr | None = None
    email: EmailStr | None = None

class UserResponse(UserBase):
    model_config = ConfigDict(from_attributes=True)   # Allows `.model_validate(orm_obj)`

    id: int
    status: str
    created_at: datetime

    @computed_field
    @property
    def is_active(self) -> bool:
        return self.status == "active"
```

### Settings management (pydantic-settings)

```python
# app/config.py
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    database_url: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/myapp"
    secret_key: str = "dev-secret-change-in-prod"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    cors_origins: list[str] = ["http://localhost:3000"]

settings = Settings()                                # Reads from env vars + .env file
```

```env
# .env
DATABASE_URL=postgresql+asyncpg://user:pass@db:5432/myapp
SECRET_KEY=super-secret
CORS_ORIGINS=["https://app.example.com","https://admin.example.com"]
```

---

## Endpoints (API routers)

```python
# app/api/v1/endpoints/users.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.deps import get_db, get_current_user
from app.schemas.user import CreateUserRequest, UpdateUserRequest, UserResponse
from app.services.user_service import UserService
from app.models.user import User

router = APIRouter(prefix="/users", tags=["users"])

@router.get("", response_model=list[UserResponse])
async def list_users(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
):
    return await UserService.list_users(db, skip=skip, limit=limit)

@router.get("/{user_id}", response_model=UserResponse)
async def get_user(user_id: int, db: AsyncSession = Depends(get_db)):
    user = await UserService.get_user(db, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.post("", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(
    request: CreateUserRequest,
    db: AsyncSession = Depends(get_db),
):
    if await UserService.email_exists(db, request.email):
        raise HTTPException(status_code=409, detail="Email already registered")
    return await UserService.create_user(db, request)

@router.put("/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: int,
    request: UpdateUserRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if user_id != current_user.id and not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Not authorized")
    return await UserService.update_user(db, user_id, request)

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    await UserService.delete_user(db, user_id)
    return None
```

```python
# app/api/v1/router.py
from fastapi import APIRouter
from app.api.v1.endpoints import users, posts

api_router = APIRouter(prefix="/api/v1")
api_router.include_router(users.router)
api_router.include_router(posts.router)

# app/main.py
from fastapi import FastAPI
from app.api.v1.router import api_router
from app.core.exceptions import register_exception_handlers

app = FastAPI(title="My API", version="0.1.0")
app.include_router(api_router)
register_exception_handlers(app)
```

---

## Lifespan (replacing `on_event`)

FastAPI 0.93+ introduced the `lifespan` context manager, replacing the deprecated `@app.on_event("startup")` / `@app.on_event("shutdown")` decorators.

```python
from contextlib import asynccontextmanager
from fastapi import FastAPI

@asynccontextmanager
async def lifespan(app: FastAPI):
    # === STARTUP ===
    # Initialize DB pool, cache, ML models, etc.
    app.state.cache = await create_redis_cache()
    app.state.ml_model = load_model()
    yield
    # === SHUTDOWN ===
    # Clean up resources
    await app.state.cache.close()

app = FastAPI(lifespan=lifespan)
```

The `yield` is the boundary — everything before runs at startup, everything after runs at shutdown. Lifespan is more powerful than `on_event` because it shares local state between startup and shutdown.

---

## Authentication: JWT

```python
# app/core/security.py
from datetime import datetime, timedelta, timezone
from jose import jwt
from passlib.context import CryptContext
from app.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)

def create_access_token(subject: str, expires_delta: timedelta | None = None) -> str:
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=settings.access_token_expire_minutes))
    return jwt.encode(
        {"sub": subject, "exp": expire},
        settings.secret_key,
        algorithm=settings.algorithm,
    )

def decode_token(token: str) -> dict:
    return jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
```

```python
# app/deps.py
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.security import decode_token
from app.models.user import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db),
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = decode_token(token)
        user_id: str | None = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except Exception:
        raise credentials_exception

    user = await db.get(User, int(user_id))
    if user is None:
        raise credentials_exception
    return user

async def get_current_active_user(
    current_user: User = Depends(get_current_user),
) -> User:
    if current_user.status != UserStatus.ACTIVE:
        raise HTTPException(status_code=403, detail="Inactive user")
    return current_user

async def get_admin_user(
    current_user: User = Depends(get_current_user),
) -> User:
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Admin access required")
    return current_user
```

---

## Migrations: Alembic (async-compatible)

```bash
# Initialize Alembic (one-time)
uv run alembic init -t async app/alembic

# Generate a migration from model changes
uv run alembic revision --autogenerate -m "create users table"

# Apply migrations
uv run alembic upgrade head

# Roll back one migration
uv run alembic downgrade -1

# See current state
uv run alembic current
```

The `alembic init -t async` flag generates an async-aware `env.py` that uses the async engine. Without it, Alembic uses sync SQLAlchemy and can't run async migrations.

```python
# app/alembic/env.py (key parts — async-aware)
from alembic import context
from sqlalchemy.ext.asyncio import async_engine_from_config
from sqlalchemy import pool
import asyncio
from app.models.base import Base
from app.models import user, post  # noqa: F401 — ensure models are imported
from app.config import settings

config = context.config
config.set_main_option("sqlalchemy.url", settings.database_url)
target_metadata = Base.metadata

def do_run_migrations(connection):
    context.configure(connection=connection, target_metadata=target_metadata)
    with context.begin_transaction():
        context.run_migrations()

async def run_async_migrations():
    connectable = async_engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)
    await connectable.dispose()

def run_migrations_online():
    asyncio.run(run_async_migrations())

run_migrations_online()
```

---

## Testing (pytest + httpx.AsyncClient + pytest-asyncio)

```python
# tests/conftest.py
import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncSession
from app.main import app
from app.models.base import Base
from app.deps import get_db

@pytest_asyncio.fixture
async def test_db():
    """In-memory SQLite for fast tests (or use testcontainers for real Postgres)."""
    engine = create_async_engine("sqlite+aiosqlite:///:memory:")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    async def override_get_db():
        async with async_session() as session:
            yield session

    app.dependency_overrides[get_db] = override_get_db
    yield async_session
    app.dependency_overrides.clear()
    await engine.dispose()

@pytest_asyncio.fixture
async def client(test_db):
    """Async HTTP client for testing the API."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac
```

```python
# tests/test_users.py
import pytest

@pytest.mark.asyncio
async def test_create_user(client):
    response = await client.post("/api/v1/users", json={
        "email": "alice@example.com",
        "name": "Alice",
        "password": "Password123",
        "age": 30,
    })
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "alice@example.com"
    assert "id" in data
    assert "password" not in data                     # Sensitive fields not leaked

@pytest.mark.asyncio
async def test_create_user_invalid_email(client):
    response = await client.post("/api/v1/users", json={
        "email": "not-an-email",
        "name": "Alice",
        "password": "Password123",
        "age": 30,
    })
    assert response.status_code == 422                # FastAPI validation error
    assert "email" in response.json()["detail"][0]["loc"]

@pytest.mark.asyncio
async def test_get_user_not_found(client):
    response = await client.get("/api/v1/users/99999")
    assert response.status_code == 404
```

Cross-reference: `testing-patterns` for general test pyramid / mocking strategies.

---

## Deployment

### Uvicorn + Gunicorn (production)

```bash
# Install Gunicorn (Linux/macOS only)
uv add gunicorn

# Run with Gunicorn managing Uvicorn workers
uv run gunicorn app.main:app \
  -w 4 \                          # Number of worker processes (2-4 × CPU cores)
  -k uvicorn.workers.UvicornWorker \
  -b 0.0.0.0:8000 \
  --access-logfile - \
  --error-logfile -
```

### Docker multi-stage build

```dockerfile
# Build stage
FROM python:3.12-slim AS builder
WORKDIR /app
RUN pip install uv
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev
COPY . .

# Runtime stage
FROM python:3.12-slim
WORKDIR /app
COPY --from=builder /app /app
ENV PATH="/app/.venv/bin:$PATH"
EXPOSE 8000
CMD ["gunicorn", "app.main:app", "-w", "4", "-k", "uvicorn.workers.UvicornWorker", "-b", "0.0.0.0:8000"]
```

### Serverless (Vercel / AWS Lambda)

FastAPI runs on serverless platforms via Mangum or the platform's ASGI adapter:

```python
# For AWS Lambda
from mangum import Mangum
from app.main import app

handler = Mangum(app)
```

For serverless, use **synchronous DB drivers** (e.g., `psycopg2` instead of `asyncpg`) if the platform doesn't support async well, or use connection pooling services like PgBouncer / AWS RDS Proxy to handle cold-start DB connections.

---

## Top 10 Anti-Patterns (the most valuable section)

1. **Blocking the event loop with sync I/O.** FastAPI is async — calling sync libraries (e.g., `requests.get()`, `time.sleep()`, sync DB drivers) blocks the entire event loop, stalling all concurrent requests. Use async libraries (`httpx`, `asyncpg`, `aiosqlite`) or offload sync code via `await asyncio.to_thread(...)`.

2. **Using `expire_on_commit=True` (the default) with async sessions.** After `await session.commit()`, accessed attributes trigger a lazy refresh — but async lazy loading is unsupported, raising `MissingGreenlet` errors. **Always set `expire_on_commit=False`** when creating the async session maker.

3. **Forgetting `await session.commit()` after writes.** Unlike Django (which auto-commits at the end of a request), SQLAlchemy requires explicit commits. Forgetting means data isn't persisted. The `get_db` dependency should wrap in try/commit/except/rollback to handle this — see the dependency example above.

4. **N+1 queries via lazy loading.** SQLAlchemy relationships are lazy by default — accessing `user.posts` triggers a query. Use `selectinload(User.posts)` or `joinedload(User.profile)` in your `select()` to eager load. For strict N+1 prevention in tests, add `raiseload(User.posts)` to fail loudly on lazy access.

5. **Pydantic v1 patterns in v2 code.** v2 is a complete rewrite. `.dict()` (now `.model_dump()`), `class Config: orm_mode = True` (now `model_config = ConfigDict(from_attributes=True)`), `@validator` (now `@field_validator`) — these will silently break or emit deprecation warnings. Read the v2 migration guide once.

6. **Using `@app.on_event("startup")` (deprecated).** Use the `lifespan` context manager instead. `on_event` is deprecated in FastAPI 0.93+ and will be removed. Lifespan is more powerful (shares local state between startup and shutdown) and the only way to do graceful async cleanup.

7. **Not overriding dependencies in tests.** The `Depends()` system makes testing trivial — `app.dependency_overrides[get_db] = override_get_db`. Not using this means tests hit the real database, making them slow and brittle. Override `get_db`, `get_current_user`, and any external service dependencies in tests.

8. **Catching `Exception` in endpoints.** FastAPI has built-in exception handling — return `HTTPException` for expected errors (404, 409, etc.) and let unexpected exceptions propagate to FastAPI's default 500 handler (which logs the traceback). A catch-all `try/except Exception` masks bugs. Use a custom exception handler (`@app.exception_handler(MyException)`) for domain-specific errors.

9. **Returning ORM objects directly without `response_model`.** Always specify `response_model=UserResponse` on endpoints — it ensures only whitelisted fields are serialized (no accidental password hash leaks). Without it, FastAPI serializes whatever the function returns, including sensitive fields.

10. **Using `pip` + `requirements.txt` instead of `uv` + `pyproject.toml` for new projects.** `uv` is 10-100x faster than pip, has built-in venv management, and `pyproject.toml` is the modern Python standard (replacing `setup.py` + `requirements.txt` + `requirements-dev.txt` fragmentation). Migrating existing projects is optional, but new projects should use the modern stack.

---

## Cross-references

- `framework-templates` — CLAUDE.md generation template for FastAPI (project onboarding)
- `django-6` — Sync Python web framework (different mental model — sync ORM, CBVs, admin, no async)
- `python-patterns` — General Python patterns (FastAPI section there is brief; this skill goes deep)
- `go-web` — Go web patterns (similar backend use case, no async/await, no ORM)
- `rust-web` — Rust web patterns (similar backend use case, ownership + traits vs async + Pydantic)
- `api-and-interface-design` — Type contract design (relevant for Pydantic schemas)
- `api-patterns` — REST API patterns (FastAPI auto-generates OpenAPI for these)
- `security-and-hardening` — OWASP-aware hardening (FastAPI has good defaults but no built-in CSRF — apps with cookie auth need it)
- `clean-code` — General coding standards applicable to Python
- `testing-patterns` — Test pyramid, mocking strategies (FastAPI-specific syntax above; general principles there)
- `code-review-checklist` — 12-category code review checklist
- `git-workflow-and-versioning` — Branching/commit conventions for Python projects

---

## Dependencies

Required (install via `uv add` or `pip install`):
- **Python** 3.12+ (3.11 minimum)
- **FastAPI** 0.115+ (`uv add fastapi[standard]`)
- **Uvicorn** 0.30+ (`uv add uvicorn[standard]`) — ASGI server
- **SQLAlchemy** 2.0+ (`uv add sqlalchemy[asyncio]`)
- **Pydantic** 2.7+ (bundled with FastAPI)
- **pydantic-settings** 2.3+ (`uv add pydantic-settings`) — for typed config
- **Alembic** 1.13+ (`uv add alembic`) — for migrations

### Database drivers (add one async driver)

| Driver | Use |
|---|---|
| `asyncpg` | PostgreSQL (preferred — fastest) |
| `aiomysql` | MySQL / MariaDB |
| `aiosqlite` | SQLite (dev/test) |
| `asyncpg` + `pgbouncer` | PostgreSQL with connection pooling (production) |

### Common additions (install via `uv add`)

- `python-jose[cryptography]` — JWT encoding/decoding (preferred over `pyjwt`)
- `passlib[bcrypt]` — password hashing
- `httpx` — async HTTP client (replaces `requests`)
- `redis[hiredis]` — async Redis client (caching, rate limiting, sessions)
- `celery[redis]` — background task queue (or use `arq` for async-native alternative)
- `python-multipart` — form parsing (required for OAuth2PasswordBearer form data)
- `slowapi` — rate limiting middleware
- `fastapi-pagination` — pagination utilities
- `sqlmodel` — Pydantic + SQLAlchemy fusion (alternative to separate schemas/models — opinionated)
- `pytest` + `pytest-asyncio` + `httpx` — testing stack
- `ruff` — lint + format (replaces Black, isort, flake8)
- `mypy` or `pyright` — static type checking
- `testcontainers[postgresql]` — Docker-based integration tests with real Postgres
- `uv` — package manager (10-100x faster than pip)
