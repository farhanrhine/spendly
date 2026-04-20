---
# Spec: Login and Logout

## Overview
Implement user authentication flows for login and logout functionality, enabling users to securely access and exit their accounts. This feature is required as part of the core user management workflow following registration (step 2), allowing authenticated access to the expense tracker application.

## Depends on
- Registration system (step 2) must be fully implemented and functional. Users must be able to register before logging in.

## Routes
- POST /login — Handle user authentication via form submission with email and password. Access level: logged-in.
- POST /logout — Terminate active session and redirect to landing page. Access level: logged-in.

## Database changes
No new tables, columns, or constraints required. Existing user authentication relies on the registration system's user data and database schema.

## Templates
- **Create:** login.html (new template extending base.html), logout.html (new template extending base.html) — though logout may not require a dedicated template; this should be verified.
- **Modify:** None — existing templates may be used for logout confirmation if applicable.

## Files to change
- app.py — Add route handlers for /login and /logout.
- database/db.py — No changes required.
- templates/login.html — New template for login form.
- templates/logout.html — New template for logout confirmation (or modify existing settings template).

## New dependencies
No new pip packages required.

## Rules for implementation
- All routes must use parameterized SQL queries for database interactions.
- Passwords must be hashed using Werkzeug's `generate_password_hash` and `check_password_hash`.
- Session management must use Flask's built-in session.
- All templates must extend `base.html` and use `url_for()` for all internal links and routes.
- No hardcoding of CSS values; use CSS variables for styling.
- No SQLAlchemy or ORM usage; raw SQLite3 must be used for all database operations.

## Definition of done
- [ ] New routes added to `app.py` for `/login` and `/logout`.
- [ ] New templates `templates/login.html` and `templates/logout.html` created and properly extending `base.html`.
- [ ] Registration system (step 2) is fully functional and validated.
- [ ] Passwords are securely hashed during registration and verified during login.
- [ ] Session is properly managed during login and logout operations.
- [ ] Tests pass (if tests are written; if not, functionality verified manually).
- [ ] No console errors or HTTP 500 errors on login/logout flows.