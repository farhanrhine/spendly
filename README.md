⚠️ **WARNING: This project is under development and not ready for production use.**

> **Note**: This project is developed collaboratively by a human creator and Claude Code, combining strategic thinking with AI-assisted implementation.

---

# Finlo - Expense Tracker

A modern web-based expense tracking application built with Flask, designed to help users manage their personal finances.

## Project Overview

Finlo is a Flask-powered expense tracker that allows users to:
- Register and authenticate accounts
- Track expenses with full CRUD operations (Create, Read, Update, Delete)
- View expense dashboards with clean, responsive UI
- Manage personal financial data securely

## Current Status

The project is currently in development: 

## Tech Stack

- **Backend**: Python 3.14 with Flask
- **Database**: SQLite with SQLAlchemy support
- **Frontend**: HTML5, CSS3, JavaScript (ES6)
- **Styling**: CSS Flexbox for layout
- **Authentication**: Custom session-based auth

## Project Structure

```
finlo/
├── app.py              # Flask application routes and logic
├── main.py             # Application entry point
├── database/           # Database-related modules
│   ├── __init__.py
│   └── db.py           # Database connection and operations
├── templates/          # HTML templates
│   ├── base.html       # Master layout template
│   ├── landing.html    # Homepage
│   ├── login.html      # Login page
│   ├── register.html   # Registration page
│   ├── settings.html   # User settings page
│   ├── privacy.html    # Privacy policy page
│   └── terms.html      # Terms of service page
├── static/             # Static assets
│   ├── css/style.css   # Application styles
│   └── js/main.js      # Client-side scripts
└── pyproject.toml      # Project dependencies
```

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

## Key Features

### User Authentication
- Secure login and registration
- Session-based authentication
- Protected routes for authenticated users

### Expense Management
- Add new expenses with amount, category, and description
- Edit existing expenses
- Delete unwanted expenses
- View expense history

### Dashboard
- Overview of all expenses
- Expense categorization
- Monthly/weekly expense summaries

## Development Notes

- The project follows a Flask MVC pattern
- Templates use Jinja2 templating engine
- CSS uses Flexbox for responsive layout
- Database operations are handled through helper functions
- Git workflow includes regular commits for feature branches

