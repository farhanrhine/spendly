---
# Spec: Registration (Step 2)

## Overview
Adds user registration functionality with form handling, validation, and session management. Allows new users to create an account with email and password. This is the first authentication feature in Finlo and is required to enable login, profile, and expense management features.

## Depends on
Step 1 (database setup) must be complete. The `users` table already exists and is ready.

## Routes
- `GET /register` — render registration form (already exists, will be enhanced) — public
- `POST /register` — process registration form, create user, set session, redirect to landing — public

## Database changes
No database changes. The `users` table already exists from Step 1. Only database helper functions will be added to `database/db.py`.

## Templates
- **Modify:** `templates/register.html` — add email and password input fields, form submission handler, validation error messages, success message after submission.

## Files to change
- `app.py` — add POST handler for `/register` with form validation and error handling
- `database/db.py` — add `create_user(email, password)` helper function (handles password hashing)
- `templates/register.html` — add form fields for email and password with validation messages

## Files to create
None. All necessary files already exist.

## New dependencies
No new dependencies. `werkzeug` for password hashing is already in `pyproject.toml`.

## Rules for implementation
- No SQLAlchemy or ORMs; use raw SQLite3 with parameterized queries (`?`).
- Passwords must be hashed with `werkzeug.security.generate_password_hash`.
- All templates must extend `base.html`.
- Use CSS variables; never hard‑code hex values.

## Definition of done
- [ ] Registration page displays with email and password input fields
- [ ] Submitting form with valid email and password creates new user in DB with hashed password
- [ ] After successful registration, user session is set and user is redirected to landing page
- [ ] Attempting to register with existing email shows validation error
- [ ] Empty email or password fields show validation error
- [ ] Password is hashed using werkzeug before being stored
- [ ] Application starts without errors and registration page loads
---