⚠️ **WARNING: This project is under development and not ready for production use.**

> **Note**: This project is developed collaboratively by a human creator(me) and Claude Code, combining strategic thinking with AI-assisted implementation. It's not vibe-coding, it's Spec-Driven Development.

**Finlo- development Team** =

[![You(human)](https://avatars.githubusercontent.com/u/124152754?v=4&s=50)](https://github.com/farhanrhine) + [![Claude Code(AI)](https://www.scriptbyai.com/wp-content/uploads/2025/06/claude-code.png)](https://claude.com/product/claude-code)

---

# Finlo - Expense Tracker

A personal expense tracking application built with Flask.

## Current Status

**Completed:**
- Step 1: Database setup (users & expenses tables, seeding)

**In Progress:**
- Step 2: User registration feature 

## Tech Stack

- **Backend**: Python 3.14 with Flask (single-file routes)
- **Database**: SQLite3 with raw SQL (no ORMs, no SQLAlchemy)
- **Frontend**: HTML5, CSS3, Vanilla JavaScript (no frameworks)
- **Styling**: CSS Flexbox for responsive layout
- **Authentication**: Flask session-based auth with werkzeug password hashing
- **Package Manager**: uv (not pip)

## Project Structure

```
finlo/
├── app.py                  # Flask application - all routes and main logic
├── database/               # Database layer
│   ├── __init__.py
│   └── db.py              # Database functions: get_db(), init_db(), seed_db()
├── templates/             # Jinja2 HTML templates
│   ├── base.html          # Master layout template (base for all pages)
│   ├── landing.html       # Homepage
│   ├── login.html         # User login page
│   ├── register.html      # User registration page
│   ├── settings.html      # User settings page
│   ├── privacy.html       # Privacy policy page
│   └── terms.html         # Terms of service page
├── static/                # Static assets
│   ├── css/
│   │   └── style.css      # Global styles (Flexbox-based responsive layout)
│   └── js/
│       └── main.js        # Client-side JavaScript (vanilla JS, no frameworks)
├── .claude/               # Development & AI collaboration (not in GitHub)
│   ├── plans/             # Implementation plans and tasks
│   └── specs/             # Specification documents and architecture notes
├── docs/                  # Documentation & learning materials (not in GitHub)
├── Finlo.db               # SQLite database (auto-generated on app start)
├── pyproject.toml         # Project dependencies (managed by uv)
├── uv.lock                # Dependency lock file
├── .gitignore             # Git ignore rules
├── .claudeignore          # Claude Code ignore rules
├── .python-version        # Python version specification
├── CLAUDE.md              # Claude Code development guide
└── README.md              # This file
```

**Key Files:**
- `app.py` - Single file containing all Flask routes (no blueprints)
- `database/db.py` - All database operations encapsulated here
- `pyproject.toml` - Managed by `uv` package manager (not pip)

## Getting Started

1. Install dependencies:
```bash
uv sync
```

2. Run the application:
```bash
uv run app.py
```

3. Open your browser and navigate to `http://localhost:5000`

## Development Notes

- The project follows a single-file Flask approach (all routes in `app.py`, no blueprints)
- Database layer encapsulated in `database/db.py` with raw SQLite3 queries
- Templates use Jinja2 with `base.html` as the master layout
- CSS uses Flexbox for responsive layout (no Bootstrap, no Tailwind)
- Frontend uses Vanilla JavaScript only (no React, no jQuery, no npm)
- Password hashing via werkzeug, session management via Flask
- Git workflow includes feature branches for each step

