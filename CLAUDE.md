# CLAUDE.md

## Project Overview

This file provides guidance to Claude Code when working with **Finlo**, a personal expense tracker built with Flask and SQLite.

**Status**: Under active development. See README.md for project status and implemented features.

---

## Architecture

```
finlo/
├── .claude/
│   ├── commands/        # Custom Claude commands (create-spec, seed-user, seed-expense)
│   ├── specs/           # Feature specifications for each step
│   └── settings.local.json
├── app.py              # All routes — single file, no blueprints
├── database/
│   ├── __init__.py
│   └── db.py           # SQLite helpers and database operations (raw SQLite3)
├── templates/
│   ├── base.html       # Shared layout — all templates must extend this
│   ├── landing.html    # Homepage
│   ├── login.html      # Login page
│   ├── register.html   # Registration page
│   ├── settings.html   # User settings page
│   ├── privacy.html    # Privacy policy page
│   └── terms.html      # Terms of service page
├── static/
│   ├── css/
│   │   └── style.css   # Global styles using Flexbox
│   └── js/
│       └── main.js     # Vanilla JS only
└── pyproject.toml      # Project dependencies (managed with uv)
```

**Where things belong:**
- New routes → `app.py` only, no blueprints
- DB logic → `database/db.py` only, never inline in routes
- New pages → new `.html` file extending `base.html`
- Styles → `style.css` (single stylesheet with Flexbox layout)

---

## Code Style

- Python: PEP 8, snake_case for all variables and functions
- Templates: Jinja2 with `url_for()` for every internal link — never hardcode URLs
- Route functions: one responsibility only — fetch data, render template, done
- DB queries: use raw SQLite3 with parameterized queries using `?` placeholders (no SQLAlchemy ORM)
- Error handling: use `abort()` for HTTP errors, not bare `return "error string"`
- Authentication: handled through Flask session management

---

## Tech Stack & Constraints

- **Backend**: Flask only — no FastAPI, no Django, no other web frameworks
- **Database**: SQLite with raw SQLite3 (parameterized queries) — no ORMs, no PostgreSQL, no external databases
- **Frontend**: Vanilla JS only — no React, no jQuery, no npm packages
- **Styling**: CSS Flexbox for responsive layout — no Bootstrap, no Tailwind
- **Dependency Manager**: `uv` only — not pip
- **No new packages**: work within `pyproject.toml` as-is unless explicitly told otherwise
- Python 3.14+ assumed — f-strings and `match` statements are fine

---

## Common Development Commands

```bash
# Install or update dependencies
uv sync

# Run the development server (port 5000)
uv run app.py

# Stage all changes (use cautiously with large modifications)
git add .

# Commit changes with Claude as co-author (recommended)
git commit -m $'your message\n\nCo-Authored-By: Claude <claude@anthropic.com>'

# Push to feature branch
git push origin feature/<branch_name>

# Run tests (if writing test files)
pytest
```

---

## Implementation Guidelines

- **Session Management**: Authentication handled through Flask's built-in session management
- **Database Operations**: All DB logic encapsulated in `database/db.py` for clean separation
- **Templating**: Jinja2 with `base.html` as the master layout template
- **Responsive Design**: CSS Flexbox ensures mobile-friendly layouts
- **Git Workflow**: Use semantic versioning in commit messages, develop features in branches before merging to main
- **Database State**: `Finlo.db` is seeded with demo user (`demo@Finlo.com` / `demo123`) and 8 sample expenses on startup
- **Testing**: pytest is available; write tests in a `tests/` directory (not yet created)

---

## Warnings and Things to Avoid

- **Never use raw string returns** when a template should be rendered
- **Never hardcode URLs** in templates — always use `url_for()`
- **Never put DB logic in route functions** — it belongs in `database/db.py`
- **Never install new packages** without explicit instruction — keep `pyproject.toml` in sync
- **Never use JS frameworks** — the frontend is intentionally vanilla
- **Never commit without a meaningful message** — use conventional commit style + include Claude as co-author
- `.claudeignore` excludes the `docs/` directory to optimize context window — respect this when searching
- **Never modify route placeholders** without reading the spec first — each placeholder marks a step number

---

## Custom Claude Commands

Project-specific commands in `.claude/commands/`:

| Command | Purpose | Usage |
|---------|---------|-------|
| `/create-spec` | Create spec file + feature branch | `/create-spec 2 registration` |
| `/seed-user` | Create random Muslim user in DB | `/seed-user` (no args) |
| `/seed-expense` | Generate realistic dummy expenses | `/seed-expense <user_id> <count> <months>` |

These commands are scoped to this project only and won't appear in other projects.

---
