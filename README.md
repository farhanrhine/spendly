⚠️ **WARNING: This project is under development and not ready for production use.**

> **Note**: This project is developed collaboratively by a human creator(me) and Claude Code, combining strategic thinking with AI-assisted implementation. It's not vibe-coding, it's Spec-Driven Development.

| | |
|---|---|
| **Finlo- development Team** | [<img src="https://avatars.githubusercontent.com/u/124152754?v=4&s=100" width="100" height="100" style="border-radius: 50%;" />](https://github.com/farhanrhine) [<img src="https://www.scriptbyai.com/wp-content/uploads/2025/06/claude-code.png" width="100" height="100" />](https://claude.com/product/claude-code) |

---

# Finlo - Expense Tracker

A personal expense tracking application built with Flask.

## Current Status

**Completed:**
- Step 1: Database setup (users & expenses tables, seeding)
- Step 2: User registration feature
- Step 3: Login and logout authentication
- Step 4: Profile page
- Step 5: Connect profile page to database
- Step 6: Data filter for profile page (including security hardening & quick filters)

**In Progress:**
- Step 7: Add new expenses feature (Planning Phase)

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
├── .claude/
│   ├── agents/             # Custom subagents for testing and code review
│   ├── commands/           # Custom Claude commands
│   ├── plans/              # Implementation plans for each feature step
│   ├── skills/             # Custom skills
│   ├── specs/              # Feature specifications
│   ├── test-report/        # Test verification reports
│   └── settings.local.json
├── app.py                  # Flask application - all routes and main logic
├── database/               # Database layer
│   ├── __init__.py
│   ├── db.py               # SQLite helpers and database operations
│   └── queries.py          # Reusable database query functions
├── docs/                   # Documentation and learning materials
├── templates/              # Jinja2 HTML templates
│   ├── base.html           # Master layout template (base for all pages)
│   ├── landing.html        # Homepage
│   ├── login.html          # User login page
│   ├── profile.html        # User profile page
│   ├── register.html       # User registration page
│   ├── settings.html       # User settings page
│   ├── privacy.html        # Privacy policy page
│   └── terms.html          # Terms of service page
├── static/                 # Static assets
│   ├── css/
│   │   └── style.css       # Global styles (Flexbox-based responsive layout)
│   └── js/
│       └── main.js         # Client-side JavaScript (vanilla JS, no frameworks)
├── .claudeignore           # Claude ignore rules
├── .gitignore              # Git ignore rules
├── .python-version         # Python version specification
├── CLAUDE.md               # Claude Code development guide
├── AGENTS.md               # Agent registry for others besides Claude Code
├── Finlo.db                # SQLite database (seeded with demo data)
├── README.md               # This file
├── pyproject.toml          # Project dependencies (managed by uv)
├── seed_expenses_script.py # Script to seed database with demo data
└── uv.lock                 # Dependency lock file
```

**Key Files:**
- `app.py` - Single file containing all Flask routes (no blueprints)
- `database/db.py` - All database operations encapsulated here
- `database/queries.py` - Shared database query helpers
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
- Shared query helpers live in `database/queries.py`
- Templates use Jinja2 with `base.html` as the master layout
- CSS uses Flexbox for responsive layout (no Bootstrap, no Tailwind)
- Frontend uses Vanilla JavaScript only (no React, no jQuery, no npm)
- Password hashing via werkzeug, session management via Flask
- Custom agents live in `.claude/agents/` and are registered in `AGENTS.md`
- SDD workflow includes testing and code review phases via `/test-feature` and `/code-review-feature`
- Git workflow includes feature branches for each step

