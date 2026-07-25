---
name: django-6
description: "Django 6.x (Python 3.12+, released August 2025 LTS) full-stack workflow skill. Covers the ORM with migrations (write Python, not SQL), Class-Based Views vs Function-Based Views decision, Django REST Framework (DRF) for APIs (Serializers, ViewSets, Routers), Django admin for free CRUD, async views with full async ORM support, Celery + Redis for background tasks, django-allauth for social auth, pytest-django for modern testing, split settings (base/dev/prod), ASGI deployment via Daphne/Uvicorn, WhiteNoise for static files, psycopg3 for PostgreSQL. Use when building any Python web application, API, or service on Django 6 — especially when the task involves migrations, ORM queries, DRF serializers/viewsets, async views, Celery tasks, or admin customization where idiomatic Django differs from generic Python patterns."
license: Proprietary. LICENSE.txt has complete terms
---

# Django 6 — Full-Stack Python Workflow Skill

> **Target:** Django 6.x (LTS through April 2028) on Python 3.12+. Django 6 continues the async-first direction started in Django 4-5: full async ORM support, async views, async middleware, async database operations. The psycopg3 driver is the recommended PostgreSQL adapter (replaces psycopg2). The `django-admin` CLI and `manage.py` are the universal entry points for everything.

## When to Use This Skill

Use this skill whenever the user is building, debugging, or extending a Django 6 application. Trigger phrases include "Django", "manage.py", "ORM", "migrations", "DRF", "Django REST Framework", "Class-Based View", "Celery", "django-allauth", "psycopg", "ASGI", "Daphne", "Uvicorn", "WhiteNoise", "pytest-django", and any reference to a `models.py`, `views.py`, `urls.py`, `settings.py`, or `admin.py` file structure.

Do **not** use this skill for:
- **Django ≤5.0** — async ORM support is partial; some patterns here require Django 5.1+
- **FastAPI / Flask / Starlette** — different mental models. See `python-patterns` for general Python framework selection guidance.
- **Wagtail / Django-CMS** — built ON Django but have their own conventions. This skill covers the underlying Django; their docs cover the CMS-specific layer.

Cross-reference: `python-patterns` skill has a brief Django section; this skill goes deep.

## Quick Start

```bash
# Create a new project (note the trailing dot to create in current dir)
mkdir myproject && cd myproject
pip install "django[psycopg3]" psycopg[binary]  # Django + PostgreSQL driver
django-admin startproject myproject .            # The first "myproject" is the project package

# Create the first app (Django projects are composed of multiple apps)
python manage.py startapp blog

# Apply default migrations (creates SQLite db.sqlite3 by default)
python manage.py migrate

# Create the superuser (for /admin/)
python manage.py createsuperuser

# Run the dev server
python manage.py runserver                       # http://127.0.0.1:8000
```

### Settings: the split settings pattern (recommended for any non-trivial project)

The default `myproject/settings.py` works for tutorials but doesn't scale. Replace it with a `settings/` package:

```
myproject/
├── settings/
│   ├── __init__.py
│   ├── base.py                  # Shared settings (INSTALLED_APPS, MIDDLEWARE, TEMPLATES)
│   ├── dev.py                   # Dev overrides (DEBUG=True, SQLite, django-debug-toolbar)
│   ├── prod.py                  # Prod overrides (DEBUG=False, Postgres, WhiteNoise)
│   └── test.py                  # Test overrides (in-memory DB, dummy cache)
├── asgi.py
├── wsgi.py
├── urls.py
└── __init__.py
```

Run with: `DJANGO_SETTINGS_MODULE=myproject.settings.dev python manage.py runserver`

```python
# myproject/settings/base.py
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent
SECRET_KEY = "django-insecure-change-me-in-prod"  # Override via env in prod.py
DEBUG = False                                     # Override to True in dev.py
ALLOWED_HOSTS: list[str] = []                     # Override per environment

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Third-party
    "rest_framework",
    "django_filters",
    "allauth",
    "allauth.account",
    # Local apps
    "blog",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",   # Static files in prod
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "allauth.account.middleware.AccountMiddleware",
]

ROOT_URLCONF = "myproject.urls"
WSGI_APPLICATION = "myproject.wsgi.application"
ASGI_APPLICATION = "myproject.asgi.application"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {"context_processors": [
            "django.template.context_processors.debug",
            "django.template.context_processors.request",
            "django.contrib.auth.context_processors.auth",
            "django.contrib.messages.context_processors.messages",
        ]},
    },
]

DATABASES = {"default": {"ENGINE": "django.db.backends.sqlite3", "NAME": BASE_DIR / "db.sqlite3"}}
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True
STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
MEDIA_URL = "media/"
MEDIA_ROOT = BASE_DIR / "media"
```

```python
# myproject/settings/prod.py
from .base import *  # noqa: F401,F403
import os

DEBUG = False
SECRET_KEY = os.environ["DJANGO_SECRET_KEY"]      # NEVER hardcode in prod
ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS", "").split(",")

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ["DB_NAME"],
        "USER": os.environ["DB_USER"],
        "PASSWORD": os.environ["DB_PASSWORD"],
        "HOST": os.environ.get("DB_HOST", "localhost"),
        "PORT": os.environ.get("DB_PORT", "5432"),
    }
}

# Cache via Redis (also serves as Celery broker)
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.redis.RedisCache",
        "LOCATION": os.environ.get("REDIS_URL", "redis://localhost:6379/1"),
    }
}

# Security hardening
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

# WhiteNoise for static files (no nginx required)
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
```

---

## Project Structure (Django canonical layout)

A Django project is a **collection of apps**. Each app is a self-contained module with models, views, URLs, admin, etc. The project package (`myproject/`) holds settings, root URL conf, and WSGI/ASGI entry points.

```
myproject/                       # Project root (where manage.py lives)
├── manage.py                    # CLI entry point (python manage.py <command>)
├── myproject/                   # Project package (same name as project)
│   ├── __init__.py
│   ├── settings/                # Split settings (see above)
│   ├── urls.py                  # Root URL config (includes each app's urls.py)
│   ├── asgi.py                  # ASGI entry (Daphne/Uvicorn)
│   ├── wsgi.py                  # WSGI entry (gunicorn)
│   └── celery.py                # Celery app definition (if using background tasks)
├── blog/                        # Example app
│   ├── __init__.py
│   ├── models.py                # ORM models
│   ├── views.py                 # Views (FBVs and/or CBVs)
│   ├── urls.py                  # App-level URL routing
│   ├── admin.py                 # Admin registrations
│   ├── serializers.py           # DRF serializers (if using DRF)
│   ├── viewsets.py              # DRF viewsets (if using DRF)
│   ├── forms.py                 # ModelForms (if using Django forms)
│   ├── migrations/              # Auto-generated migration files
│   ├── tests/                   # Tests (split into a package for scale)
│   │   ├── __init__.py
│   │   ├── test_models.py
│   │   ├── test_views.py
│   │   └── test_api.py
│   ├── apps.py                  # AppConfig (app label, ready hook for signals)
│   └── signals.py               # Signal handlers (post_save, pre_delete, etc.)
├── templates/                   # Project-wide templates (overridden by app templates)
│   ├── base.html
│   └── blog/
│       └── post_detail.html
├── static/                      # Project-wide static files
├── requirements/                # Split requirements (base.txt, dev.txt, prod.txt)
└── pytest.ini                   # pytest-django config
```

### Apps: the unit of modularity

Create apps with `python manage.py startapp <name>`. An app is a Python package with the conventional files above. Apps should be **loosely coupled** — avoid importing models from one app into another. If app B needs to react to changes in app A's models, use signals rather than direct imports.

---

## Core Mental Model: ORM with Migrations + Convention-over-Configuration Admin

Django's distinctive paradigm is **a single framework that includes ORM, admin, auth, sessions, forms, templating, and security in one cohesive whole**. Three things differentiate Django from Flask/FastAPI/SQLAlchemy stacks:

### 1. The ORM is Active Record with migrations, and the migrations ARE your schema history

Unlike SQLAlchemy where you might use Alembic as a separate tool, Django migrations are first-class: every model change generates a migration file, and the migration history IS the source of truth for the database schema.

```python
# blog/models.py
from django.db import models
from django.contrib.auth.models import User

class Post(models.Model):
    class Status(models.TextChoices):
        DRAFT = "draft", "Draft"
        PUBLISHED = "published", "Published"
        ARCHIVED = "archived", "Archived"

    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, max_length=200)
    body = models.TextField()
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.DRAFT)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    published_at = models.DateTimeField(null=True, blank=True)
    metadata = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-published_at"]
        indexes = [
            models.Index(fields=["status", "-published_at"]),
        ]

    def __str__(self) -> str:
        return self.title


# After defining or changing a model:
# python manage.py makemigrations blog    # Generate migration file
# python manage.py migrate                # Apply all pending migrations
# python manage.py showmigrations         # See migration state
```

### 2. QuerySets are lazy and chainable

```python
# Queries are NOT executed until you evaluate them (list(), iteration, len(), bool())
qs = Post.objects.filter(status="published").select_related("author").prefetch_related("tags")

# This doesn't hit the DB:
print(qs.query)              # Shows the SQL that WOULD run

# This hits the DB:
posts = list(qs)             # Executes the query
first = qs.first()           # Executes a LIMIT 1 query
count = qs.count()           # Executes a COUNT(*) query
exists = qs.exists()         # Executes a SELECT 1 ... LIMIT 1

# Eager load relationships to avoid N+1
posts = Post.objects.select_related("author").all()         # FK / OneToOne (JOIN)
posts = Post.objects.prefetch_related("comments", "tags").all()  # M2M / reverse FK (2nd query)
```

**`select_related`** does a SQL JOIN (single query) — use for ForeignKey and OneToOne. **`prefetch_related`** does a second query and joins in Python — use for ManyToMany and reverse ForeignKey. Using the wrong one will either OOM the DB (JOINing too much) or trigger N+1 queries (forgetting to prefetch).

### 3. The admin is free CRUD — extend it, don't fight it

```python
# blog/admin.py
from django.contrib import admin
from .models import Post

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "status", "published_at", "created_at")
    list_filter = ("status", "created_at", "author")
    search_fields = ("title", "body", "author__username")
    prepopulated_fields = {"slug": ("title",)}            # Auto-fill slug from title
    date_hierarchy = "published_at"
    raw_id_fields = ("author",)                            # FK widget for large related tables
    readonly_fields = ("created_at", "updated_at")
    actions = ["publish_selected"]

    @admin.action(description="Publish selected posts")
    def publish_selected(self, request, queryset):
        updated = queryset.update(status="published", published_at=timezone.now())
        self.message_user(request, f"{updated} posts published.")
```

The admin saves you from writing CRUD for internal tools. Many teams ship with the admin as their internal backoffice. Customize via `ModelAdmin` subclasses — don't try to replace it.

---

## Views: Function-Based vs Class-Based

Django offers two view styles. Both are valid. The choice is per-view, not per-project.

### Function-Based Views (FBVs) — explicit, easy to read

```python
# blog/views.py
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from .models import Post
from .forms import PostForm

def post_list(request: HttpRequest) -> HttpResponse:
    posts = Post.objects.filter(status=Post.Status.PUBLISHED).select_related("author")
    return render(request, "blog/post_list.html", {"posts": posts})

def post_detail(request: HttpRequest, slug: str) -> HttpResponse:
    post = get_object_or_404(Post, slug=slug, status=Post.Status.PUBLISHED)
    return render(request, "blog/post_detail.html", {"post": post})

@login_required
def post_create(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            form.save_m2m()
            return redirect("blog:post_detail", slug=post.slug)
    else:
        form = PostForm()
    return render(request, "blog/post_form.html", {"form": form})
```

### Class-Based Views (CBVs) — reusable, but harder to debug

```python
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin

class PostListView(ListView):
    model = Post
    template_name = "blog/post_list.html"
    context_object_name = "posts"
    paginate_by = 15

    def get_queryset(self):
        return Post.objects.filter(status=Post.Status.PUBLISHED).select_related("author")

class PostDetailView(DetailView):
    model = Post
    template_name = "blog/post_detail.html"

    def get_queryset(self):
        return Post.objects.filter(status=Post.Status.PUBLISHED)

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = "blog/post_form.html"

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
```

### When to choose which

| Situation | Choose |
|---|---|
| Simple GET / POST handler, custom logic | FBV |
| Standard list / detail / create / update / delete | CBV (less boilerplate) |
| Need to override multiple extension points (get_queryset, get_context_data, form_valid) | CBV |
| Multiple mixins needed (LoginRequiredMixin, PermissionRequiredMixin, etc.) | CBV |
| Complex flow with branching logic | FBV (mixins become spaghetti) |
| Async view (Django 5+) | FBV (CBV async support is awkward) |

**Opinionated default:** start with FBVs. Move to CBVs when you see repetition across views that a CBV would consolidate. Avoid Generic CBVs with multiple mixins — they look elegant until you need to debug the MRO.

### Async views (Django 5+)

```python
import asyncio
import httpx
from django.http import HttpRequest, HttpResponse
from asgiref.sync import sync_to_async

async def async_post_list(request: HttpRequest) -> HttpResponse:
    # Async ORM queries (Django 5.1+ supports full async ORM)
    posts = await Post.objects.filter(status=Post.Status.PUBLISHED).select_related("author").afirst()
    # Parallel HTTP calls
    async with httpx.AsyncClient() as client:
        responses = await asyncio.gather(
            client.get("https://api.example.com/stats"),
            client.get("https://api.example.com/feed"),
        )
    # Sync ORM calls must be wrapped:
    user = await sync_to_async(lambda: request.user)()
    return render(request, "blog/post_list.html", {"posts": posts, "user": user})
```

**Async views are NOT a free speedup.** They help when the view spends most of its time waiting on I/O (HTTP calls to other services, slow DB queries that can run in parallel). For CPU-bound work or simple CRUD, async views add overhead. Benchmark before adopting.

---

## Django REST Framework (DRF)

For API-first projects, DRF is the canonical layer. It adds serializers, viewsets, routers, permissions, throttling, pagination, and a browsable API on top of Django.

```bash
pip install djangorestframework django-filter
# Add 'rest_framework' to INSTALLED_APPS in settings/base.py
```

### Serializers — convert models ↔ JSON

```python
# blog/serializers.py
from rest_framework import serializers
from .models import Post

class PostSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source="author.username")   # Read-only nested
    tags = serializers.StringRelatedField(many=True)               # M2M as string list

    class Meta:
        model = Post
        fields = ["id", "title", "slug", "body", "status", "author", "tags",
                  "published_at", "created_at"]
        read_only_fields = ["id", "slug", "created_at", "published_at"]

    def validate_title(self, value: str) -> str:
        if len(value) < 3:
            raise serializers.ValidationError("Title must be at least 3 characters.")
        return value
```

### ViewSets + Routers — CRUD in 10 lines

```python
# blog/viewsets.py
from rest_framework import viewsets, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Post
from .serializers import PostSerializer

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.select_related("author").prefetch_related("tags")
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["status", "author"]
    search_fields = ["title", "body"]
    ordering_fields = ["published_at", "created_at"]
    lookup_field = "slug"

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
```

```python
# blog/urls.py (or myproject/urls.py)
from rest_framework.routers import DefaultRouter
from .viewsets import PostViewSet

router = DefaultRouter()
router.register(r"posts", PostViewSet, basename="post")
# Generates: /posts/, /posts/<slug>/, /posts/<slug>/ (PUT/PATCH), /posts/<slug>/ (DELETE)

urlpatterns = router.urls
```

This gives you a full CRUD API with filtering, search, ordering, pagination, and a browsable HTML UI at `/posts/` for free. Permission classes control access (DRF ships with `IsAuthenticated`, `IsAuthenticatedOrReadOnly`, `IsAdminUser`, `DjangoModelPermissions`; write custom ones for fine-grained control).

### DRF alternatives worth knowing

- **Django Ninja** — FastAPI-style API on top of Django. Type-hint-driven, async-native, less boilerplate than DRF for greenfield APIs. Good when you want FastAPI ergonomics with Django's ORM and admin.
- **Django REST Framework's `@api_view`** — function-based API views, lighter than ViewSets. Use for non-CRUD endpoints.

---

## Authentication

### Three auth surfaces

| Surface | Use |
|---|---|
| **`django.contrib.auth`** (built-in) | Username/password login via sessions. Always available. Default for browser apps with server-rendered templates. |
| **django-allauth** | Social auth (Google, GitHub, Facebook, etc.) + email-only login + 2FA via TOTP. Industry standard. |
| **DRF Token Auth / dj-rest-auth** | API token auth for mobile/SPA consumers. Pairs with django-allauth for the social login flow. |
| **django-oauth-toolkit** | Full OAuth2 provider. Only if YOU are the OAuth2 server. |

### django-allauth setup (the modern default)

```bash
pip install django-allauth
# Add to INSTALLED_APPS: "allauth", "allauth.account"
# Add to MIDDLEWARE: "allauth.account.middleware.AccountMiddleware"
# Configure in settings:
```

```python
# settings/base.py additions
AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",      # For admin login
    "allauth.account.auth_backends.AuthenticationBackend",  # For allauth
]
ACCOUNT_LOGIN_METHODS = {"email"}                    # Email-only login (no username)
ACCOUNT_SIGNUP_FIELDS = ["email*", "password1*", "password2*"]
ACCOUNT_EMAIL_VERIFICATION = "mandatory"             # Require email confirmation
ACCOUNT_SESSION_REMEMBER = True                      # Persist session after browser close
LOGIN_REDIRECT_URL = "/"
ACCOUNT_LOGOUT_REDIRECT_URL = "/"
```

For social providers, add `SOCIALACCOUNT_PROVIDERS = {"google": {"APP": {...}}}` and configure OAuth credentials per provider. Allauth handles the entire OAuth flow.

---

## Background Tasks (Celery + Redis)

For any work that doesn't need to happen in the HTTP request cycle (sending emails, processing uploads, scheduled jobs, calling slow APIs), use Celery with a Redis broker.

```bash
pip install celery redis
```

```python
# myproject/celery.py
import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "myproject.settings.prod")

app = Celery("myproject")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()  # Finds tasks.py in each app

@app.task(bind=True)
def debug_task(self):
    print(f"Request: {self.request!r}")
```

```python
# blog/tasks.py
from celery import shared_task
from django.core.mail import send_mail
from .models import Post

@shared_task(bind=True, max_retries=3, default_retry_delay=60)
def send_post_notification(self, post_id: int):
    try:
        post = Post.objects.select_related("author").get(pk=post_id)
        subscribers = post.author.profile.subscribers.all()
        for sub in subscribers:
            send_mail(
                subject=f"New post: {post.title}",
                message=post.body[:200],
                from_email="noreply@example.com",
                recipient_list=[sub.email],
            )
    except Post.DoesNotExist as exc:
        raise self.retry(exc=exc)  # Retry with backoff

# Call from a view or signal:
from blog.tasks import send_post_notification
send_post_notification.delay(post.id)   # .delay() = async dispatch
```

```bash
# Run the worker (production — use Supervisor or systemd)
celery -A myproject worker --loglevel=info --concurrency=4

# Run the scheduler (for periodic tasks via celery beat)
celery -A myproject beat --loglevel=info

# Monitor (Flower is the canonical dashboard)
pip install flower
celery -A myproject flower
```

Cross-reference: the `n8n-workflow-automation` skill is a no-code alternative for orchestration.

---

## Testing (pytest-django is the modern default)

The built-in `python manage.py test` works but uses unittest syntax. **pytest-django** is the modern choice — better fixtures, parametrization, and integration with the broader pytest ecosystem.

```bash
pip install pytest-django pytest-factoryboy model-bakery
```

```ini
# pytest.ini
[pytest]
DJANGO_SETTINGS_MODULE = myproject.settings.test
python_files = tests.py test_*.py *_tests.py
addopts = -v --tb=short --reuse-db
```

```python
# blog/tests/test_views.py
import pytest
from django.urls import reverse
from model_bakery import baker
from blog.models import Post

@pytest.mark.django_db
def test_post_list_shows_published_posts(client):
    published = baker.make(Post, status=Post.Status.PUBLISHED, _quantity=3)
    baker.make(Post, status=Post.Status.DRAFT)  # Should NOT appear

    response = client.get(reverse("blog:post_list"))

    assert response.status_code == 200
    assert len(response.context["posts"]) == 3
    assert all(p.status == Post.Status.PUBLISHED for p in response.context["posts"])

@pytest.mark.django_db
def test_post_create_requires_login(client):
    response = client.get(reverse("blog:post_create"))
    assert response.status_code == 302  # Redirect to login
    assert "/login" in response.url

@pytest.mark.django_db
def test_post_create_authenticated(client, django_user_model):
    user = django_user_model.objects.create_user(username="alice", password="secret")
    client.force_login(user)

    response = client.post(reverse("blog:post_create"), {
        "title": "My Post",
        "slug": "my-post",
        "body": "Hello world",
        "status": Post.Status.DRAFT,
    })

    assert response.status_code == 302
    assert Post.objects.filter(title="My Post", author=user).exists()
```

Cross-reference: `testing-patterns` skill for general test pyramid / mocking strategies.

---

## Deployment

```bash
# Collect static files (run BEFORE deploy)
python manage.py collectstatic --noinput

# Run migrations (run AFTER deploy code is on the server, BEFORE switching traffic)
python manage.py migrate

# ASGI server (Daphne or Uvicorn) — production
pip install daphne
daphne -b 0.0.0.0 -p 8000 myproject.asgi:application

# OR Uvicorn with multiple workers via gunicorn-style supervisor:
pip install uvicorn[standard]
uvicorn myproject.asgi:application --host 0.0.0.0 --port 8000 --workers 4

# OR gunicorn for WSGI-only (no async):
pip install gunicorn
gunicorn myproject.wsgi:application --workers 4 --bind 0.0.0.0:8000
```

### Canonical production stack

```
[Internet] → [nginx] → [Daphne/Uvicorn (ASGI)] → [Django app]
                ↓                                        ↓
        static files                          [PostgreSQL] + [Redis]
        (WhiteNoise or                                 (DB)         (cache + Celery broker)
         nginx directly)
                                                              ↓
                                                       [Celery worker]
                                                       (long-running process,
                                                        managed by Supervisor)
```

For managed hosting: **Railway**, **Render**, **Fly.io**, **Heroku** all support Django out of the box. For self-hosted Docker: pair `gunicorn`/`uvicorn` with the official `python:3.12-slim` image and a Postgres container.

---

## Top 10 Anti-Patterns (the most valuable section)

1. **Using `objects.all()` in views without pagination.** Tables grow. `Post.objects.all()` will OOM the server with 100k rows. Always paginate: `Post.objects.all()[0:15]` or use the DRF `PageNumberPagination` class.

2. **N+1 queries in templates.** Iterating `{% for post in posts %}{{ post.author.name }}{% endfor %}` triggers a query per iteration unless you used `select_related("author")`. Use `django-debug-toolbar` in dev to see query counts per request.

3. **Fat views with business logic.** Views should be ~10-30 lines: parse request, call a service function, render response. Business logic goes in `services.py` (a module you create per app) or as model methods — not in the view.

4. **Skipping migrations for schema changes.** Editing the DB directly via `psql` or a SQL client is the fastest way to lose sync between environments. Always `python manage.py makemigrations` — even for one-off changes. Migration history IS the source of truth.

5. **Using `DEBUG=True` in production.** This is the #1 Django security mistake. `DEBUG=True` exposes sensitive environment variables, source code paths, and stack traces to anyone who triggers an error. Always set `DEBUG=False` in `prod.py` and verify with `python manage.py check --deploy`.

6. **Not running `python manage.py check --deploy` before launch.** This built-in command checks for ~20 common production security misconfigurations (DEBUG, ALLOWED_HOSTS, SECURE_SSL_REDIRECT, HSTS, etc.). Run it as part of your CI/CD pipeline.

7. **Hardcoding secrets in `settings.py`.** Use environment variables via `os.environ["VAR_NAME"]` or a secrets manager (django-environ, dotenv). The `.env` file should be in `.gitignore`. Never commit `SECRET_KEY`, `DB_PASSWORD`, or API keys.

8. **Using the default `SessionMiddleware` for API tokens.** Django sessions are cookie-based. For API consumers (mobile, SPA on a different domain), use DRF's `TokenAuthentication` or JWT (via `djangorestframework-simplejwt`). Sessions + CSRF don't play well with cross-origin APIs.

9. **Importing models across apps at module top level.** If `blog/models.py` does `from shop.models import Product`, you've created a hard dependency. Use string references in ForeignKey (`"shop.Product"`) and signals for cross-app events. This keeps apps reusable.

10. **Not using `select_related` / `prefetch_related` correctly.** `select_related` is for FK / OneToOne (single JOIN query). `prefetch_related` is for M2M / reverse FK (second query). Using `select_related` on a M2M raises an error. Using `prefetch_related` on a FK works but is wasteful (extra query). Read the docs once and remember the distinction.

---

## Cross-references

- `framework-templates` — CLAUDE.md generation template for Django (project onboarding)
- `python-patterns` — General Python patterns (framework selection, async, type hints, project structure). Has a brief Django section; this skill goes deep.
- `api-patterns` — REST API design (relevant for DRF ViewSets and `@api_view` endpoints)
- `api-and-interface-design` — Type contract design
- `security-and-hardening` — OWASP-aware hardening (Django has CSRF, XSS, SQL injection, clickjacking protection built in; this skill covers what Django doesn't)
- `clean-code` — General coding standards applicable to Python
- `testing-patterns` — Test pyramid, mocking strategies (Django-specific syntax above; general principles there)
- `code-review-checklist` — 12-category code review checklist
- `n8n-workflow-automation` — No-code alternative to Celery for some orchestration use cases
- `git-workflow-and-versioning` — Branching/commit conventions for Django projects

---

## Dependencies

Required (install via pip):
- **Python** 3.12+ (Django 6 minimum)
- **Django** 6.x
- **psycopg** 3.x (with `[binary]` extra for pre-compiled wheels) — PostgreSQL driver (replaces psycopg2)

Common additions (install on demand):
- **djangorestframework** — REST API framework (Serializers, ViewSets, Routers)
- **django-filter** — DRF filtering backend
- **django-allauth** — Social auth + email login + 2FA
- **celery[redis]** + **redis** — Background task queue
- **django-cors-headers** — CORS headers for cross-origin API consumers
- **django-environ** or **python-dotenv** — Environment variable management
- **django-debug-toolbar** — Dev-only request inspector (queries, signals, templates)
- **django-extensions** — Extra management commands (shell_plus, runserver_plus, show_urls)
- **pytest-django** + **pytest-factoryboy** + **model-bakery** — Modern testing stack
- **whitenoise** — Static file serving in production (no nginx required)
- **gunicorn** or **uvicorn[standard]** or **daphne** — Production ASGI/WSGI server
- **djangorestframework-simplejwt** — JWT auth for DRF (alternative to token auth)
- **django-storages** — S3 / GCS / Azure Blob for media files
- **django-crispy-forms** + **crispy-bootstrap5** — Form rendering with Bootstrap 5
- **django-htmx** — HTMX integration for reactive UIs without writing JS
