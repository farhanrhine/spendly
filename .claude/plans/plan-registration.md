# Implementation Plan for Registration (02-registration.md)

## Overview
- **Purpose**: Implement user registration functionality with form handling, validation, and session management
- **Specification Dependency**: Builds on Step 1 (database setup); `users` table already exists
- **Key Components**: Form validation, password hashing, user creation, session management, error handling
- **Target Files**: 
  - `app.py` (add POST /register route)
  - `database/db.py` (add validation and user creation helpers)
  - `templates/register.html` (no changes needed; form + error display already in place)

---

## Current State Analysis

### Existing Route
- `GET /register` exists in `app.py` but only renders template
- No POST handler; no form processing, validation, or DB insertion
- Template already includes form fields: `name`, `email`, `password`
- Error block already exists: `{% if error %}`

### Database Schema (Ready)
```
users (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL,
  email TEXT NOT NULL UNIQUE,
  password_hash TEXT NOT NULL,
  created_at TEXT DEFAULT CURRENT_TIMESTAMP
)
```
- UNIQUE constraint on email (built-in duplicate detection)
- Werkzeug already imported in `database/db.py` for password hashing

### Template & Styling (Ready)
- Form fields: `name`, `email`, `password` (text inputs with placeholders)
- Error rendering: `.auth-error` CSS class
- Button: `.btn-submit` class
- All auth page styling complete: `.auth-container`, `.form-group`, `.form-input`

---

## Step-by-Step Implementation

### Phase 1: Database Helper Functions
**Location:** `database/db.py`

#### Step 1.1: Add Validation Helper Functions
- **`is_valid_email(email)`** → returns `bool`
  - Check: not empty AND contains `@` AND contains `.` after `@`
  - Example valid: `user@example.com`, `name@domain.co.uk`
  - Example invalid: `notanemail`, `user@`, `@domain.com`

- **`is_valid_password(password)`** → returns `bool`
  - Check: not empty AND length >= 8
  - Per template hint: "Min. 8 characters"

- **`email_exists(email)`** → returns `bool`
  - Query: `SELECT COUNT(*) FROM users WHERE email = ?` (parameterized)
  - Return True if count > 0

#### Step 1.2: Add User Creation Function
**Function:** `create_user(email, password)`
- **Returns:** `int` (user_id on success)
- **Raises:** `ValueError` on validation or duplicate email
- **Implementation:**
  1. Validate inputs:
     - If email empty → raise `ValueError("Email is required")`
     - If not valid email format → raise `ValueError("Please enter a valid email address")`
     - If email exists → raise `ValueError("Email already registered. Try logging in instead.")`
     - If password empty → raise `ValueError("Password is required")`
     - If password < 8 chars → raise `ValueError("Password must be at least 8 characters")`
  2. Extract name from email (part before `@`)
  3. Hash password: `from werkzeug.security import generate_password_hash; password_hash = generate_password_hash(password)`
  4. Open DB connection: `db = get_db()`
  5. Execute parameterized INSERT:
     ```
     INSERT INTO users (name, email, password_hash)
     VALUES (?, ?, ?)
     ```
  6. Commit transaction: `db.commit()`
  7. Return the inserted user's id (use `db.execute(...).lastrowid`)
  8. Handle `sqlite3.IntegrityError` (duplicate email) → raise `ValueError("Email already registered")`

---

### Phase 2: Route Handler
**Location:** `app.py`

#### Step 2.1: Enhance POST /register Route
**Current route:** `GET /register` (line ~25-26)
- Keep GET handler as-is
- **Add POST handler:**
  ```
  @app.route("/register", methods=["POST"])
  def register_post():
  ```

**Implementation:**
1. Extract form data:
   - `email = request.form.get('email', '').strip()`
   - `password = request.form.get('password', '').strip()`

2. Try to create user:
   ```
   try:
       user_id = create_user(email, password)
   ```

3. On success:
   - Set session: `session['user_id'] = user_id`
   - Redirect: `return redirect(url_for('landing'))`

4. On ValueError (validation error):
   - Extract error message from exception
   - Re-render template: `return render_template("register.html", error=str(e))`

5. On other exceptions (database errors):
   - Log exception
   - Return: `return render_template("register.html", error="Registration failed. Please try again.")`

6. Ensure method routing:
   - `GET /register` → renders blank form
   - `POST /register` → processes form and creates user

---

### Phase 3: Template Integration (Verification)
**Location:** `templates/register.html`
- **No changes needed**
- Verify form structure:
  - Form method: `POST`
  - Form action: `/register` (or empty, defaults to current URL)
  - Input names match extraction in route:
    - `name="email"`
    - `name="password"`
  - Error block exists: `{% if error %}<div>{{ error }}</div>{% endif %}`

---

## Detailed Validation Logic

### Email Validation
- **Required**: Email field cannot be empty
- **Format**: Must contain `@` and at least one `.` after `@`
- **Uniqueness**: Query database; reject if email already exists
- **Error Messages**:
  - Empty → `"Email is required"`
  - Invalid format → `"Please enter a valid email address"`
  - Already exists → `"Email already registered. Try logging in instead."`

### Password Validation
- **Required**: Password field cannot be empty
- **Length**: Minimum 8 characters (per template UX hint)
- **Hashing**: Use `werkzeug.security.generate_password_hash()`
- **Error Messages**:
  - Empty → `"Password is required"`
  - Too short → `"Password must be at least 8 characters"`

### Validation Order
1. Check email empty → stop and return error
2. Check email format → stop and return error
3. Check email exists → stop and return error
4. Check password empty → stop and return error
5. Check password length → stop and return error
6. If all pass → create user

---

## Files to Modify

### 1. `database/db.py`
- **Add imports**: `from werkzeug.security import generate_password_hash`
- **Add functions**:
  - `is_valid_email(email)`
  - `is_valid_password(password)`
  - `email_exists(email)`
  - `create_user(email, password)` (main orchestrator)

### 2. `app.py`
- **Add import** (if not already present): `from database.db import create_user`
- **Enhance existing route** (currently ~line 25-26):
  - Keep `GET /register` handler
  - **Add new** `POST /register` handler with form processing logic
  - Use `request.form.get()` for form field extraction
  - Use `session['user_id']` for authentication state
  - Use `redirect(url_for('landing'))` for post-registration redirect

### 3. `templates/register.html`
- **No changes needed**
- Verify existing form structure (form fields, error block, button)

---

## Dependencies

### Already Available
✅ `werkzeug` (3.1.8+) — provides `generate_password_hash()` and `check_password_hash()`
✅ `flask` (3.1.3+) — provides `session`, `request.form`, `redirect()`, `url_for()`
✅ SQLite3 (built-in Python) — parameterized queries with `?` placeholders

### No New Dependencies Required
All dependencies for Step 2 already exist in `pyproject.toml`

---

## Verification Checklist

### Unit Tests (if tests/ directory exists)
- [ ] `create_user()` with valid email and password creates user with hashed password
- [ ] `create_user()` raises `ValueError` with correct message on duplicate email
- [ ] `create_user()` raises `ValueError` on empty email
- [ ] `create_user()` raises `ValueError` on invalid email format
- [ ] `create_user()` raises `ValueError` on empty password
- [ ] `create_user()` raises `ValueError` on password < 8 chars
- [ ] `is_valid_email()` returns True for valid formats, False for invalid
- [ ] `is_valid_password()` returns True for 8+ chars, False for <8
- [ ] `email_exists()` returns False for new emails, True for registered

### Manual Functional Tests
1. **Test Form Rendering**
   - Navigate to `http://localhost:5000/register` 
   - Verify form renders with all fields visible
   - Verify error block is empty (no error displayed)

2. **Test Validation: Empty Email**
   - Leave email field empty
   - Fill password with "validpass1"
   - Click "Create account"
   - Verify error message: "Email is required"
   - Verify form reloaded with populated password field

3. **Test Validation: Invalid Email**
   - Enter "notanemail" (no @)
   - Enter password "validpass1"
   - Click "Create account"
   - Verify error message: "Please enter a valid email address"

4. **Test Validation: Empty Password**
   - Enter email "test@example.com"
   - Leave password empty
   - Click "Create account"
   - Verify error message: "Password is required"

5. **Test Validation: Short Password**
   - Enter email "test@example.com"
   - Enter password "short"
   - Click "Create account"
   - Verify error message: "Password must be at least 8 characters"

6. **Test Successful Registration**
   - Enter email "newuser@example.com"
   - Enter password "ValidPass1"
   - Click "Create account"
   - Verify redirect to landing page (`/`)
   - Verify no error message displayed

7. **Test Duplicate Email**
   - Register with "user@example.com" and "ValidPass1"
   - Try registering again with same email and different password
   - Verify error message: "Email already registered. Try logging in instead."

8. **Test Session Management**
   - After successful registration, open browser DevTools
   - Check Application → Cookies
   - Verify session cookie exists with `user_id`

9. **Test Database Persistence**
   - After registration, use SQLite CLI:
     ```
     sqlite3 Finlo.db
     SELECT * FROM users WHERE email = 'newuser@example.com';
     ```
   - Verify user exists with hashed password (not plaintext)
   - Verify name extracted from email correctly

10. **Test App Startup**
    - Run `uv run app.py`
    - Verify no import errors, no database errors
    - Verify `/register` route loads without errors

---

## Implementation Order (Dependencies)

1. **First**: Add validation functions to `database/db.py` (required by `create_user()`)
2. **Second**: Add `create_user()` to `database/db.py` (required by route)
3. **Third**: Add POST handler to `app.py` (consumes `create_user()`)
4. **Fourth**: Manual testing of all flows
5. **Fifth**: Verify database state after registrations

---

## Error Handling Strategy

### Validation Errors (ValueError)
- Expected and user-facing
- Return 200 response with re-rendered form + error message
- Error displayed in `.auth-error` styled div

### Database Errors (IntegrityError)
- Catch `sqlite3.IntegrityError` in `create_user()`
- Convert to `ValueError` with user-friendly message

### Unexpected Errors
- Return generic 500 error or "Registration failed. Please try again."
- Could implement logging (optional, not in spec)

---

## Key Design Decisions

1. **Auto-name from email**: User name extracted from email prefix (part before `@`)
   - Keeps registration form simple (no extra name input needed)
   - Justifies template hint "Farhan" as placeholder for auto-fill

2. **Stop-on-first-error validation**: Return first validation error, not all errors
   - Simpler UX: focus on fixing one issue at a time
   - Consistent with form behavior

3. **Parameterized queries**: All DB queries use `?` placeholders
   - Prevents SQL injection
   - Project convention (no ORM)

4. **Password hashing**: `werkzeug.security.generate_password_hash()`
   - Already imported in codebase (`seed_db()` uses it)
   - Industry standard, salts automatically

5. **Session-based auth**: Set `session['user_id']` after registration
   - Flask native support
   - Matches project's session management pattern

---

## Deliverables

Upon completion:
- ✅ `database/db.py` contains `is_valid_email()`, `is_valid_password()`, `email_exists()`, `create_user()`
- ✅ `app.py` contains POST handler for `/register` with error handling and session management
- ✅ `templates/register.html` renders form with error messages on validation failure
- ✅ Registration creates user in database with hashed password
- ✅ Session set and user redirected to landing page on success
- ✅ All validation error messages displayed in template
- ✅ Duplicate email registration rejected with user-friendly error
