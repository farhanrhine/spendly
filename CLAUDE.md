# CLAUDE.md

## Developer Info

**Name:** Farhan  
**GitHub:** [@farhanrhine](https://github.com/farhanrhine)  
**Project:** Finlo - Personal Expense Tracker  

Farhan uses both Claude Code and Pi for development. Use friendly, conversational tone. Offer proactive suggestions and explain design decisions clearly.

---

## Project Overview

This file provides guidance to Claude Code and Pi when working with **Finlo**, a personal expense tracker built with Flask and SQLite.

**Status**: Under active development. See README.md for project status and implemented features.

---

## Architecture

```
finlo/
├── .claude/
│   ├── agents/                   # Custom subagents (test-writer, quality-reviewer, security-reviewer, test-runner)
│   ├── commands/                 # Custom Claude commands (create-spec, seed-user, seed-expense)
│   ├── plans/                    # Implementation plans for each feature step
│   ├── skills/                   # Custom skills (e.g., frontend-design/)
│   ├── specs/                    # Feature specifications for each step
│   ├── test-report/              # Test verification reports for each step
│   └── settings.local.json
├── app.py                        # All routes — single file, no blueprints
├── database/
│   ├── __init__.py
│   ├── db.py                     # SQLite helpers (supports configurable DATABASE path for testing)
│   └── queries.py                # Reusable database query functions
├── tests/                        # Pytest suite (feature-specific tests)
├── templates/
│   ├── base.html                 # Shared layout — all templates must extend this
│   ├── landing.html              # Homepage
│   ├── login.html                # Login page
│   ├── register.html             # Registration page
│   ├── profile.html              # User profile page
│   ├── settings.html             # User settings page
│   ├── privacy.html              # Privacy policy page
│   └── terms.html                # Terms of service page
├── static/
│   ├── css/
│   │   └── style.css             # Global styles using Flexbox
│   └── js/
│       └── main.js               # Vanilla JS only
├── .claudeignore                 # Files/folders ignored by Claude (e.g., docs/)
├── .python-version               # Python version specification
├── AGENTS.md                     # Agent registry — other then Claude Code
├── CLAUDE.md                     # This file — Claude Code guidance (you are here)
├── Finlo.db                      # SQLite database (with demo data on startup)
├── README.md                     # Project overview and getting started
├── pyproject.toml                # Project dependencies (managed with uv)
├── seed_expenses_script.py       # Script to seed database with demo data
└── uv.lock                       # Dependency lock file (managed by uv)
```

**Where things belong:**
- New routes → `app.py` only, no blueprints
- DB logic → `database/db.py` only, never inline in routes
- Reusable DB queries → `database/queries.py` for shared helper functions
- New pages → new `.html` file extending `base.html`
- Styles → `style.css` (single stylesheet with Flexbox layout)
- Feature specs → `.claude/specs/<number>-feature-name.md`
- Implementation plans → `.claude/plans/plan-<feature-name>.md` (auto-generated)
- Test reports → `.claude/test-report/<number>-feature-name-verification-report.md`
- Custom agents → `.claude/agents/<agent-name>.md` (test-writer, quality-reviewer, security-reviewer, test-runner)

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

# Commit changes with Claude and Pi as co-authors (recommended)
git commit -m $'your message\n\nCo-Authored-By: Claude <claude@anthropic.com>\nCo-Authored-By: Pi <noreply@pi.dev>'

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
- **Testing**: pytest is available; write and maintain tests in the `tests/` directory

---

## Custom Agents for Quality Assurance

Finlo uses specialized subagents to automate testing and code review after feature implementation:

| Agent | Purpose | Triggered by |
|-------|---------|--------------|
| `finlo-test-writer` | Writes spec-driven pytest test cases after feature implementation | Manual invoke after feature is complete |
| `finlo-test-runner` | Executes pytest suite and analyzes results (pass/fail, coverage, guardrails) | After test-writer completes (`/test-feature`) |
| `finlo-quality-reviewer` | Reviews code for clean, maintainable Flask patterns (architecture, naming, style) | `/code-review-feature` (parallel with security-reviewer) |
| `finlo-security-reviewer` | Reviews code for web vulnerabilities and security issues (SQL injection, auth, XSS) | `/code-review-feature` (parallel with quality-reviewer) |

**Workflow**: After implementing a feature → `/test-feature` → tests written → tests run → `/code-review-feature` → security + quality reviews → git commit & push

---

## SDD Workflow Phases

**Spec-Driven Development** workflow in Finlo follows these phases:

1. **Planning**: Read spec → understand requirements
2. **Implementation**: Write code (routes, DB helpers, templates)
3. **Quality Assurance**:
   - **Testing Phase** (`/test-feature`): test-writer creates tests → test-runner executes → analysis report
   - **Code Review Phase** (`/code-review-feature`): finlo-quality-reviewer + finlo-security-reviewer run in parallel → compressed summaries
4. **Integration**: Stage changes → commit with co-author → push to feature branch

---

## Warnings and Things to Avoid

- **Never use raw string returns** when a template should be rendered
- **Never hardcode URLs** in templates — always use `url_for()`
- **Never put DB logic in route functions** — it belongs in `database/db.py`
- **Never install new packages** without explicit instruction — keep `pyproject.toml` in sync
- **Never use JS frameworks** — the frontend is intentionally vanilla
- **Never wait for user reminders to commit** — perform incremental commits (with Co-Authored-By tag) after each logical step of a feature implementation
- **Never search in `.claudeignore` files** — `docs/` folder is excluded to optimize context window. Claude has no permission to access ignored files
- **Never modify route placeholders** without reading the spec first — each placeholder marks a step number

---

## Custom Claude Commands

Project-specific commands in `.claude/commands/`:

| Command | Purpose | Usage |
|---------|---------|-------|
| `/create-spec` | Create spec file + feature branch | `/create-spec 2 registration` |
| `/seed-user` | Create random Muslim user in DB | `/seed-user` (no args) |
| `/seed-expense` | Generate realistic dummy expenses | `/seed-expense <user_id> <count> <months>` |
| `/test-feature` | Run test-writer → test-runner pipeline | `/test-feature 2-registration` |
| `/code-review-feature` | Run parallel security + quality reviews | `/code-review-feature 2-registration` |

These commands are scoped to this project only and won't appear in other projects.

---
