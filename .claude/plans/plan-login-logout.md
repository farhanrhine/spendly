---
# Plan: Login and Logout Implementation

## Context
This feature implements secure user authentication flows (login and logout) for the Finlo expense tracker after the registration system (step 2) is in place. It enables users to access their account and manage expenses.

## Approach
1. **Add database helper functions** in `database/db.py`: `get_user_by_email(email)` and `validate_user(email, password)`.
2. **Add route handlers** in `app.py` for `GET /login` (display form), `POST /login` (authenticate), and `POST /logout` (clear session).
3. **Create login template** `templates/login.html` extending `base.html`.
4. **Modify base template** `templates/base.html` to add logout button in header/nav (visible only when logged in).
5. **Handle session management** using Flask's built-in `session['user_id']`.
6. **Secure password handling** using Werkzeug's `check_password_hash` (passwords hashed on registration).
7. **Ensure all links** use `url_for()` for internal routing.
8. **Add error handling** for invalid credentials without leaking email existence.

## Files to Modify
- `database/db.py` – Add helper functions `get_user_by_email()` and `validate_user()`.
- `app.py` – Add route handlers for GET `/login`, POST `/login`, and POST `/logout`.
- `templates/login.html` – New template for login form.
- `templates/base.html` – Add logout button in header/nav (conditionally visible).

## Tasks
- **Database Layer**:
  - Add `get_user_by_email(email)` – Query user by email, return user object or None.
  - Add `validate_user(email, password)` – Check credentials, return user_id on success or None on failure.
- **Route Implementation**: 
  - `GET /login` – Display login form (render `login.html`).
  - `POST /login` – Call `validate_user()`, set `session['user_id']` on success, show error on failure.
  - `POST /logout` – Clear session, redirect to landing page.
- **Template Creation**: 
  - `login.html` – Form with email/password fields, extending `base.html`, using `url_for()`.
- **Base Template Update**: 
  - Add logout button/link in header (visible only if `session.get('user_id')`).
- **Error Handling**: 
  - Display generic "Invalid email or password" message (no email existence leak).
- **Testing**: 
  - Run the app, manually verify login/logout flows work without errors.

## Verification
- Start server with `uv run app.py`.
- Navigate to `/login`, verify login form displays (GET /login).
- Submit valid credentials (demo@Finlo.com / demo123), verify `session['user_id']` is set and user is logged in.
- Submit invalid credentials, verify error message displays (generic, no email leak).
- Click logout button (or navigate to POST /logout), verify session cleared and redirected to landing page.
- Verify logged-in users cannot access `/login` (redirect away).
- Confirm no HTTP 500 errors or console exceptions.