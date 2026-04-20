---
# Spec: Login and Logout

## Overview
Implement user authentication flows for login and logout functionality, enabling users to securely access and exit their accounts. This feature is required as part of the core user management workflow following registration (step 2), allowing authenticated access to the expense tracker application.

## Depends on
- Registration system (step 2) must be fully implemented and functional. Users must be able to register before logging in.

## Routes
- GET /login — Display login form (public). Access level: not logged-in.
- POST /login — Handle user authentication via form submission with email and password. Access level: not logged-in.
- POST /logout — Terminate active session and redirect to landing page. Access level: logged-in.

## Database changes
No new tables, columns, or constraints required. Existing user authentication relies on the registration system's user data and database schema.

## Templates
- **Create:** login.html (new template extending base.html for login form).
- **Modify:** base.html — Add logout button in header/nav (visible only when logged in).

## Files to change
- app.py — Add route handlers for GET /login, POST /login, and POST /logout.
- database/db.py — Add helper functions: `get_user_by_email(email)` and `validate_user(email, password)`.
- templates/login.html — New template for login form.
- templates/base.html — Add logout button in header/nav (visible only when logged in).

## New dependencies
No new pip packages required.

## Rules for implementation
- All routes must use parameterized SQL queries for database interactions (via helpers in `database/db.py`).
- Passwords must be hashed using Werkzeug's `generate_password_hash` and `check_password_hash`.
- Session management must use Flask's built-in `session['user_id']` to track login state.
- All templates must extend `base.html` and use `url_for()` for all internal links and routes.
- Error handling: Display error messages for invalid email/password (do not expose whether email exists).
- Redirect to `/login` if non-logged-in user tries to access protected routes; redirect to `/` if logged-in user tries to access `/login`.
- No hardcoding of CSS values; use CSS variables for styling.
- No SQLAlchemy or ORM usage; raw SQLite3 must be used for all database operations.

## Definition of done
- [ ] New routes added to `app.py` for GET `/login`, POST `/login`, and POST `/logout`.
- [ ] DB helper functions added to `database/db.py`: `get_user_by_email()` and `validate_user()`.
- [ ] New template `templates/login.html` created and properly extending `base.html`.
- [ ] Logout button added to `templates/base.html` (visible only when logged in).
- [ ] Registration system (step 2) is fully functional and validated.
- [ ] Passwords are securely hashed during registration and verified during login.
- [ ] Session is properly managed: `session['user_id']` set on login, cleared on logout.
- [ ] Error messages displayed for invalid credentials (no email existence leak).
- [ ] Non-logged-in users redirected to `/login`; logged-in users redirected away from `/login`.
- [ ] Tests pass (if tests are written; if not, functionality verified manually).
- [ ] No console errors or HTTP 500 errors on login/logout flows.