# Implementation Plan for Add New Expenses (07-add-new-expenses.md)

## Overview
- **Purpose**: Implement expense entry functionality allowing authenticated users to record new transactions with amount, category, description, and date
- **Specification Dependency**: Builds on Steps 1 (database setup), 3 (login/logout); `expenses` table already exists
- **Key Components**: Form rendering, input validation, category dropdown, date handling, database insertion, session management
- **Target Files**: 
  - `app.py` (add GET and POST `/expenses/add` routes)
  - `database/queries.py` (add `create_expense()` function)
  - `templates/add_expense.html` (create new template)

---

## Current State Analysis

### Existing Route
- `GET /expenses/add` exists in `app.py` (line ~108) as stub: `return "Add expense — coming in Step 7"`
- No POST handler; no form processing or DB insertion
- Will be completely replaced with full implementation

### Database Schema (Ready)
```
expenses (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  user_id INTEGER NOT NULL,
  amount REAL NOT NULL,
  category TEXT NOT NULL,
  date TEXT NOT NULL,
  description TEXT,
  created_at TEXT DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY(user_id) REFERENCES users(id)
)
```
- All required columns exist
- Foreign key constraint enforces user_id validity
- Created_at auto-populated with current timestamp

### Template & Styling (Ready)
- `base.html` exists with navigation bar and Flexbox layout
- `style.css` has CSS variables and responsive design patterns
- Existing form styles: `.auth-container`, `.form-group`, `.form-input`, `.btn-submit`
- Can reuse existing form styling patterns from login/register templates

### Predefined Categories
From spec: Food, Transport, Bills, Health, Entertainment, Other

---

## Step-by-Step Implementation

### Phase 1: Database Helper Function
**Location:** `database/queries.py`

#### Step 1.1: Add create_expense() Function
**Function signature:** `create_expense(user_id, amount, category, date, description=None)`
- **Returns:** `int` (expense_id on success)
- **Raises:** `ValueError` on validation errors
- **Implementation:**
  1. **Input validation:**
     - Validate `amount` is a positive number (> 0)
       - If invalid → raise `ValueError("Amount must be a positive number")`
     - Validate `category` is not empty and is in predefined list
       - If invalid → raise `ValueError("Invalid category selected")`
     - Validate `date` is in YYYY-MM-DD format and is a valid date
       - Use `datetime.strptime(date, '%Y-%m-%d')` to validate
       - If invalid → raise `ValueError("Invalid date format")`
  2. Open DB connection: `conn = get_db()`
  3. Execute parameterized INSERT:
     ```sql
     INSERT INTO expenses (user_id, amount, category, date, description)
     VALUES (?, ?, ?, ?, ?)
     ```
  4. Commit transaction: `conn.commit()`
  5. Return inserted expense id
  6. Close connection in finally block
  7. Handle exceptions gracefully

---

### Phase 2: Route Handlers
**Location:** `app.py`

#### Step 2.1: Replace GET /expenses/add Route
**Current code (line ~108):**
```python
@app.route("/expenses/add")
def add_expense():
    return "Add expense — coming in Step 7"
```

**New implementation:**
1. **Authentication guard:**
   - Check `session.get('user_id')`
   - If not authenticated → `redirect(url_for('login'))`
2. **Prepare context data:**
   - Define category list: `['Food', 'Transport', 'Bills', 'Health', 'Entertainment', 'Other']`
   - Get today's date in YYYY-MM-DD format: `datetime.now().strftime('%Y-%m-%d')`
   - Include in context as `default_date`
3. **Render template:**
   - `return render_template('add_expense.html', categories=categories, default_date=default_date)`

#### Step 2.2: Add POST /expenses/add Route
**New route implementation:**
```python
@app.route("/expenses/add", methods=["POST"])
def add_expense_post():
```

**Implementation steps:**
1. **Authentication guard:**
   - Check `session.get('user_id')`
   - If not authenticated → `redirect(url_for('login'))`
2. **Extract form data:**
   - `amount = request.form.get('amount', '').strip()`
   - `category = request.form.get('category', '').strip()`
   - `date = request.form.get('date', '').strip()`
   - `description = request.form.get('description', '').strip()`
3. **Convert and validate amount:**
   - Try to convert amount to float: `float(amount)`
   - If conversion fails → catch exception and re-render with error message
4. **Call create_expense():**
   - `try:` call `create_expense(user_id, amount, category, date, description)`
   - On success → `redirect(url_for('profile'))`
   - On `ValueError` → catch and re-render form with:
     - Error message
     - Preserved field values (amount, category, date, description)
     - Category list
5. **Error handling:**
   - Pass `error`, `categories`, `default_date`, and form values to template
   - Use same error display pattern as registration form

---

### Phase 3: Template Creation
**Location:** `templates/add_expense.html`

#### Step 3.1: Create add_expense.html Template
**Structure:**
1. **Extends base.html:**
   - `{% extends "base.html" %}`
   - `{% block content %}...{% endblock %}`
2. **Container and heading:**
   - Main container: `.form-container` (reuse from login/register styling)
   - Heading: `<h1>Add New Expense</h1>`
3. **Error display (conditional):**
   - If `error` exists → render `.form-error` or `.auth-error` with error message
4. **Form element:**
   - `<form method="POST" action="{{ url_for('add_expense_post') }}">`
   - Or use route name: `action="{{ url_for('add_expense', _method='POST') }}"` (Flask magic)
5. **Form fields (in order):**
   - **Amount:**
     - `<label for="amount">Amount (₹)</label>`
     - `<input type="number" id="amount" name="amount" step="0.01" min="0" required>`
     - Placeholder: "Enter amount"
     - Preserve value: `value="{{ amount or '' }}"`
   - **Category:**
     - `<label for="category">Category</label>`
     - `<select id="category" name="category" required>`
     - Option: `<option value="">Select a category</option>`
     - For each category: `<option value="{{ cat }}" {% if category == cat %}selected{% endif %}>{{ cat }}</option>`
   - **Date:**
     - `<label for="date">Date</label>`
     - `<input type="date" id="date" name="date" required>`
     - Default value: `value="{{ default_date }}"`
   - **Description:**
     - `<label for="description">Description (Optional)</label>`
     - `<textarea id="description" name="description" rows="3" placeholder="Add notes about this expense"></textarea>`
     - Preserve value: `{{ description or '' }}`
6. **Submit button:**
   - `<button type="submit" class="btn-submit">Add Expense</button>`
   - Or `.btn-primary` if available
7. **Cancel/Back link:**
   - `<a href="{{ url_for('profile') }}" class="btn-secondary">Cancel</a>`
8. **Styling:**
   - Use `.form-group` for field grouping (existing class)
   - Use `.form-input` for input/select/textarea styling
   - Use Flexbox for layout consistency
   - Match form design from register.html and login.html
   - Apply CSS variables for colors and spacing (no hardcoded hex values)

---

## Implementation Checklist

### Routes (app.py)
- [ ] Replace GET `/expenses/add` stub with full implementation
  - [ ] Add authentication guard (redirect to login if not authenticated)
  - [ ] Prepare categories list and default date
  - [ ] Render template with context data
- [ ] Add POST `/expenses/add` route
  - [ ] Add authentication guard
  - [ ] Extract form data
  - [ ] Validate and convert amount to float
  - [ ] Call `create_expense()` function
  - [ ] Handle success: redirect to profile
  - [ ] Handle validation errors: re-render form with error message and preserved values

### Database Function (database/queries.py)
- [ ] Add `create_expense(user_id, amount, category, date, description=None)` function
  - [ ] Validate amount (positive number)
  - [ ] Validate category (in predefined list)
  - [ ] Validate date (YYYY-MM-DD format and valid date)
  - [ ] Insert into expenses table with parameterized query
  - [ ] Return inserted expense id
  - [ ] Handle exceptions gracefully

### Template (templates/add_expense.html)
- [ ] Create new file extending `base.html`
- [ ] Add page heading "Add New Expense"
- [ ] Add error message display (conditional)
- [ ] Add form with POST method pointing to `/expenses/add`
- [ ] Add amount input (number, step 0.01, min 0, required)
- [ ] Add category select with predefined options
- [ ] Add date input (date picker, required, defaults to today)
- [ ] Add description textarea (optional)
- [ ] Add submit button ("Add Expense")
- [ ] Add cancel link back to profile
- [ ] Style consistently with login/register forms
- [ ] Use CSS Flexbox for layout
- [ ] Use CSS variables for colors (no hardcoded hex values)

### Testing
- [ ] Test GET `/expenses/add` renders form with categories and default date
- [ ] Test form submission with valid data saves expense and redirects to profile
- [ ] Test validation error for missing amount
- [ ] Test validation error for invalid category
- [ ] Test validation error for invalid date
- [ ] Test validation error for non-positive amount
- [ ] Test form preserves field values on validation error
- [ ] Test unauthenticated user is redirected to login
- [ ] Test expense appears in profile page after being added

---

## Code Reuse & Style Guide

### CSS Classes to Reuse
- `.form-container` — main wrapper
- `.form-group` — field wrapper
- `.form-input` — input/select/textarea styling
- `.btn-submit` — submit button
- `.btn-secondary` — cancel/back link (if available, else create)
- `.auth-error` or `.form-error` — error message display

### CSS Variables (style.css)
- Colors: `--primary-color`, `--border-color`, `--text-color`, `--bg-light`, etc.
- Spacing: `--spacing-sm`, `--spacing-md`, `--spacing-lg`
- Font: `--font-size-base`, `--font-weight-bold`
- Never hardcode hex values

### Import Statements Required
```python
from datetime import datetime
from database.queries import create_expense
```

### Form Data Extraction Pattern
```python
email = request.form.get('email', '').strip()
```

---
